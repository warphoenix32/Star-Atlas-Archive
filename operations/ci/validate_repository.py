"""Deterministic, network-free repository and campaign validation for CI."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SCHEMA_VERSIONS = {"2.0", "2.1"}


class ValidationFailure(RuntimeError):
    pass


def run(*args: str, check: bool = False, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        env=env,
        check=False,
    )
    if check and result.returncode:
        raise ValidationFailure(f"command failed ({' '.join(args)}):\n{result.stdout}{result.stderr}")
    return result


def tracked_files(*suffixes: str) -> list[Path]:
    result = run("git", "ls-files", check=True)
    return [ROOT / value for value in result.stdout.splitlines() if value.endswith(suffixes)]


def changed_paths(base_ref: str) -> list[str]:
    if not base_ref:
        raise ValidationFailure("base ref is required for diff-scoped validation")
    result = run("git", "diff", "--name-only", f"{base_ref}...HEAD", check=True)
    return sorted(line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip())


def parse_json_corpus() -> tuple[int, int]:
    documents = 0
    records = 0
    failures: list[str] = []
    for path in tracked_files(".json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            documents += 1
        except Exception as exc:  # noqa: BLE001 - report every parse defect
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
    for path in tracked_files(".jsonl"):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                json.loads(line)
                records += 1
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{path.relative_to(ROOT)}:{line_number}: {exc}")
    if failures:
        raise ValidationFailure("invalid JSON/JSONL:\n" + "\n".join(failures))
    return documents, records


def validate_declared_schemas() -> int:
    checked = 0
    failures: list[str] = []
    for path in tracked_files(".json"):
        if "archive/ingestion-packages/" not in path.as_posix():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        metadata = payload.get("metadata")
        if not isinstance(metadata, dict) or "repository_schema" not in metadata:
            continue
        checked += 1
        version = str(metadata.get("repository_schema"))
        if version not in SCHEMA_VERSIONS:
            failures.append(f"{path.relative_to(ROOT)}: unsupported repository_schema {version}")
        if not isinstance(payload.get("sources"), list):
            failures.append(f"{path.relative_to(ROOT)}: declared ingestion package lacks sources list")
    if failures:
        raise ValidationFailure("schema contract failures:\n" + "\n".join(failures))
    return checked


def validate_source_identity() -> tuple[int, int]:
    extraction_paths = sorted(ROOT.glob("archive/ingestion-packages/*/extractions/*.json"))
    ids = [path.stem for path in extraction_paths]
    duplicates = sorted(value for value, count in Counter(ids).items() if count > 1)
    failures: list[str] = []
    if duplicates:
        failures.append("duplicate extraction Source IDs: " + ", ".join(duplicates))

    record_markdown: dict[str, list[Path]] = {}
    record_json: dict[str, list[Path]] = {}
    for path in ROOT.glob("archive/source-records/**/*.md"):
        record_markdown.setdefault(path.stem, []).append(path)
    for path in ROOT.glob("archive/source-records/**/*.json"):
        if path.name in {"source-records.json", "campaign-summary.json"}:
            continue
        record_json.setdefault(path.stem, []).append(path)

    for path in extraction_paths:
        source_id = path.stem
        payload = json.loads(path.read_text(encoding="utf-8"))
        embedded = payload.get("source_id") if isinstance(payload, dict) else None
        if embedded and embedded != source_id:
            failures.append(f"{path.relative_to(ROOT)}: source_id {embedded} does not match filename {source_id}")
        markdown_matches = record_markdown.get(source_id, [])
        if len(markdown_matches) != 1:
            failures.append(f"{source_id}: expected one Markdown Source Record, found {len(markdown_matches)}")
        for record_path in record_json.get(source_id, []):
            record = json.loads(record_path.read_text(encoding="utf-8"))
            if isinstance(record, dict) and record.get("source_id") not in {None, source_id}:
                failures.append(f"{record_path.relative_to(ROOT)}: Source Record ID does not match filename")

    if failures:
        raise ValidationFailure("Source-ID reconciliation failures:\n" + "\n".join(failures))
    return len(extraction_paths), sum(len(value) for value in record_markdown.values())


def validate_markdown_links() -> int:
    checked = 0
    failures: list[str] = []
    for path in tracked_files(".md"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("archive/source-records/", "archive/campaign-summaries/")):
            continue
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip().strip("<>").split()[0]
            if not target or target.startswith("#") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            target = unquote(target.split("#", 1)[0])
            checked += 1
            if not (path.parent / target).resolve().exists():
                failures.append(f"{rel} -> {match.group(1)}")
    if failures:
        raise ValidationFailure("broken local Markdown links:\n" + "\n".join(failures))
    return checked


def validate_forbidden_paths(changes: list[str]) -> str:
    ledger_campaign = any(path.startswith((
        "operations/campaigns/canonical-pip-governance-ledger-2026-07/",
        "knowledge/governance/PIP-Registry.",
    )) for path in changes)
    knowledge_campaign = any(path.startswith(("knowledge/", "operations/campaigns/knowledge-narrative-depth-001/")) for path in changes)
    medium_campaign = any("star-atlas-medium" in path or path.startswith(("archive/raw/medium/", "archive/normalized/medium/", "archive/source-records/medium/")) for path in changes)
    discord_campaign = any(path.startswith(("operations/campaigns/discord-community-indexing-001/", "operations/tests/discord_community_indexing/")) for path in changes)
    common = (".github/workflows/", "operations/ci/")
    selected = sum((ledger_campaign, knowledge_campaign and not ledger_campaign, medium_campaign, discord_campaign))
    if selected != 1:
        raise ValidationFailure("unable to select exactly one recognized campaign path contract")
    if ledger_campaign:
        allowed = common + (
            "knowledge/governance/PIP-Registry.md",
            "knowledge/governance/PIP-Registry.json",
            "knowledge/governance/README.md",
            "operations/campaigns/canonical-pip-governance-ledger-2026-07/",
        )
        label = "canonical-pip-governance-ledger-2026-07"
    elif knowledge_campaign:
        allowed = common + ("knowledge/", "operations/campaigns/knowledge-narrative-depth-001/")
        label = "knowledge-narrative-depth-001"
    elif medium_campaign:
        allowed = common + (
            "archive/raw/medium/star-atlas/",
            "archive/normalized/medium/star-atlas/",
            "archive/source-records/medium/star-atlas/",
            "archive/ingestion-packages/star-atlas-medium/",
            "archive/manifests/",
            "archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/",
            "operations/campaigns/star-atlas-medium-ingestion-2026-07/",
        )
        label = "star-atlas-medium-ingestion-2026-07"
    elif discord_campaign:
        allowed = common + (
            "operations/campaigns/discord-community-indexing-001/",
            "operations/tests/discord_community_indexing/",
        )
        label = "discord-community-indexing-001"
    forbidden = [path for path in changes if not path.startswith(allowed)]
    if forbidden:
        raise ValidationFailure(f"{label} forbidden-path changes:\n" + "\n".join(forbidden))
    return label


def sha_tree(root: Path, exclusions: set[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        rel = path.relative_to(root).as_posix()
        if rel in exclusions or path.suffix == ".pyc" or "__pycache__" in path.parts:
            continue
        values[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return values


def run_cycle(command: list[str], root: Path, exclusions: set[str], env: dict[str, str] | None = None) -> dict[str, str]:
    run(*command, check=True, env=env)
    return sha_tree(root, exclusions)


def validate_knowledge_campaign() -> None:
    campaign = ROOT / "operations/campaigns/knowledge-narrative-depth-001"
    env = os.environ.copy()
    env.setdefault("GITHUB_BASE_REF", "main")
    command = [sys.executable, str(campaign / "build_campaign.py")]
    validate = [sys.executable, str(campaign / "validate_campaign.py")]

    # Establish a platform-local fixed point before comparing cycles. The
    # campaign manifest observes validator-generated reports, so a Linux CI
    # checkout may need one pass to normalize files produced on Windows.
    run(*command, check=True, env=env)
    run(*validate, check=True, env=env)
    run(*command, check=True, env=env)
    first = run_cycle(validate, campaign, {"build_campaign.py", "validate_campaign.py", "README.md"}, env)
    run(*command, check=True, env=env)
    second = run_cycle(validate, campaign, {"build_campaign.py", "validate_campaign.py", "README.md"}, env)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("knowledge campaign output is not deterministic: " + ", ".join(differing))
    diff = run("git", "diff", "--exit-code", "--", str(campaign.relative_to(ROOT)))
    if diff.returncode:
        raise ValidationFailure("knowledge campaign generated artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_medium_campaign() -> None:
    campaign = ROOT / "operations/campaigns/star-atlas-medium-ingestion-2026-07"
    command = [sys.executable, str(campaign / "medium_campaign.py"), "validate"]
    first = run_cycle(command, campaign, {"medium_campaign.py", "README.md"})
    second = run_cycle(command, campaign, {"medium_campaign.py", "README.md"})
    if first != second:
        raise ValidationFailure("Medium campaign validation outputs are not deterministic")
    diff = run("git", "diff", "--exit-code", "--", str(campaign.relative_to(ROOT)), "archive/manifests", "archive/campaign-summaries/star-atlas-medium-ingestion-2026-07")
    if diff.returncode:
        raise ValidationFailure("Medium campaign validation artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_discord_campaign(base_ref: str) -> None:
    campaign = ROOT / "operations/campaigns/discord-community-indexing-001"
    command = [sys.executable, str(campaign / "validate_campaign.py"), "--base-ref", base_ref]
    exclusions = {"build_index.py", "validate_campaign.py", "README.md"}
    first = run_cycle(command, campaign, exclusions)
    second = run_cycle(command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("Discord campaign output is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(campaign.relative_to(ROOT)), "operations/tests/discord_community_indexing",
    )
    if diff.returncode:
        raise ValidationFailure("Discord campaign generated artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_pip_ledger_campaign() -> None:
    campaign = ROOT / "operations/campaigns/canonical-pip-governance-ledger-2026-07"
    command = [sys.executable, str(campaign / "validate_ledger.py")]
    exclusions = {"build_ledger.py", "validate_ledger.py", "README.md", "canonical-pip-governance-ledger.schema.json"}
    run(*command, check=True)
    first = run_cycle(command, campaign, exclusions)
    second = run_cycle(command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("PIP ledger campaign output is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(campaign.relative_to(ROOT)),
        "knowledge/governance/PIP-Registry.json",
        "knowledge/governance/PIP-Registry.md",
    )
    if diff.returncode:
        raise ValidationFailure("PIP ledger generated artifacts do not reconcile with committed files:\n" + diff.stdout)


def repository_mode(base_ref: str) -> None:
    documents, records = parse_json_corpus()
    schemas = validate_declared_schemas()
    extractions, markdown = validate_source_identity()
    links = validate_markdown_links()
    changes = changed_paths(base_ref)
    contract = validate_forbidden_paths(changes)
    diff = run("git", "diff", "--check", f"{base_ref}...HEAD")
    if diff.returncode:
        raise ValidationFailure("git diff --check failed:\n" + diff.stdout + diff.stderr)
    print(f"PASS repository-integrity: {documents} JSON; {records} JSONL records; {schemas} schema packages; {extractions} unique extractions; {markdown} Markdown Source Records; {links} links; contract={contract}")


def campaign_mode(base_ref: str) -> None:
    changes = changed_paths(base_ref)
    contract = validate_forbidden_paths(changes)
    if contract == "knowledge-narrative-depth-001":
        validate_knowledge_campaign()
    elif contract == "star-atlas-medium-ingestion-2026-07":
        validate_medium_campaign()
    elif contract == "discord-community-indexing-001":
        validate_discord_campaign(base_ref)
    elif contract == "canonical-pip-governance-ledger-2026-07":
        validate_pip_ledger_campaign()
    print(f"PASS campaign-contracts: {contract}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("repository", "campaign"), required=True)
    parser.add_argument("--base-ref", default=os.environ.get("CI_BASE_REF", "origin/main"))
    args = parser.parse_args()
    try:
        (repository_mode if args.mode == "repository" else campaign_mode)(args.base_ref)
    except ValidationFailure as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
