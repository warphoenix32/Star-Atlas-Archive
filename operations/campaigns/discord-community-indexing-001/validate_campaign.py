#!/usr/bin/env python3
"""Validate the Discord community index and its generated-artifact fixed point."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from build_index import CAMPAIGN_ID, SCHEMA_VERSION, write_outputs


JSON_FILES = (
    "source-inventory.json", "alias-registry.json", "promotion-candidates.json",
    "conflict-report.json", "research-backlog.json", "tag-registry.json",
    "discord-channel-coverage.json", "discord-channel-gap-report.json",
    "discord-collection-backlog.json", "human-resolution-queue.json",
    "validation-report.json",
)
JSONL_FILES = (
    "identity-index.jsonl", "guild-index.jsonl", "organization-index.jsonl",
    "relationship-index.jsonl", "competition-index.jsonl",
)
GENERATED_FILES = tuple(name for name in JSON_FILES + JSONL_FILES if name != "validation-report.json")
ID_FIELDS = {
    "identity-index.jsonl": "identity_id",
    "guild-index.jsonl": "guild_id",
    "organization-index.jsonl": "organization_id",
    "relationship-index.jsonl": "relationship_id",
    "competition-index.jsonl": "competition_record_id",
}


def digest_map(directory: Path) -> dict[str, str]:
    return {
        name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
        for name in GENERATED_FILES if (directory / name).is_file()
    }


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> tuple[bool, str]:
    completed = subprocess.run(
        command, cwd=cwd, text=True, encoding="utf-8", errors="replace",
        capture_output=True, check=False, env=env,
    )
    detail = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0, detail[-6000:]


def changed_paths(repo_root: Path, base_ref: str) -> tuple[list[str], str | None]:
    values: set[str] = set()
    errors: list[str] = []
    commands = (
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
    )
    for command in commands:
        ok, detail = run(command, repo_root)
        if not ok:
            errors.append(detail)
            continue
        values.update(
            line.strip().replace("\\", "/") for line in detail.splitlines()
            if line.strip() and not line.casefold().startswith("warning:")
        )
    return sorted(values), "\n".join(errors) or None


def validate_scope(repo_root: Path, base_ref: str) -> tuple[bool, dict[str, object]]:
    paths, error = changed_paths(repo_root, base_ref)
    resolved_ok, resolved_detail = run(["git", "rev-parse", base_ref], repo_root)
    resolved_base_sha = next(
        (line.strip() for line in resolved_detail.splitlines() if re.fullmatch(r"[0-9a-fA-F]{40}", line.strip())),
        None,
    )
    allowed_prefixes = (
        "operations/campaigns/discord-community-indexing-001/",
        "operations/tests/discord_community_indexing/",
    )
    allowed_exact = {
        ".github/workflows/repository-consolidation.yml",
        "operations/ci/README.md",
        "operations/ci/validate_repository.py",
    }
    forbidden = [path for path in paths if path not in allowed_exact and not path.startswith(allowed_prefixes)]
    protected = [path for path in paths if path.startswith(("archive/", "knowledge/", "graph/", "publication/"))]
    resolution_error = None if resolved_ok and resolved_base_sha else resolved_detail
    return not error and not resolution_error and not forbidden and not protected, {
        "base_sha": resolved_base_sha, "changed_paths": paths, "forbidden_paths": forbidden,
        "protected_evidence_or_canonical_paths": protected, "git_error": error,
        "base_resolution_error": resolution_error,
    }


def parse_and_contract(campaign_dir: Path) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    counts = {"json_documents": 0, "jsonl_records": 0}
    for filename in JSON_FILES:
        try:
            payload = json.loads((campaign_dir / filename).read_text(encoding="utf-8"))
            counts["json_documents"] += 1
            if not isinstance(payload, dict):
                errors.append(f"{filename}: top level must be an object")
            elif payload.get("schema_version") != SCHEMA_VERSION or payload.get("campaign_id") != CAMPAIGN_ID:
                errors.append(f"{filename}: campaign/schema declaration mismatch")
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"{filename}: {error}")
    for filename in JSONL_FILES:
        identifiers: set[str] = set()
        try:
            lines = (campaign_dir / filename).read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as error:
            errors.append(f"{filename}: {error}")
            continue
        for number, line in enumerate(lines, 1):
            if not line.strip():
                errors.append(f"{filename}:{number}: blank JSONL record")
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(f"{filename}:{number}: {error}")
                continue
            counts["jsonl_records"] += 1
            field = ID_FIELDS[filename]
            identifier = payload.get(field) if isinstance(payload, dict) else None
            if not identifier:
                errors.append(f"{filename}:{number}: missing {field}")
            elif identifier in identifiers:
                errors.append(f"{filename}:{number}: duplicate {field} {identifier}")
            identifiers.add(identifier)
    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--base-ref", default="origin/main")
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    campaign_dir = Path(__file__).resolve().parent

    before = digest_map(campaign_dir)
    write_outputs(repo_root, campaign_dir)
    after = digest_map(campaign_dir)
    generated_reconciliation = before == after and len(after) == len(GENERATED_FILES)

    parse_errors, parse_counts = parse_and_contract(campaign_dir)
    with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
        first_dir, second_dir = Path(first), Path(second)
        write_outputs(repo_root, first_dir)
        write_outputs(repo_root, second_dir)
        deterministic = digest_map(first_dir) == digest_map(second_dir) == after

    test_env = os.environ.copy()
    pipeline_src = str(repo_root / "operations" / "pipeline" / "src")
    test_env["PYTHONPATH"] = pipeline_src + (os.pathsep + test_env["PYTHONPATH"] if test_env.get("PYTHONPATH") else "")
    tests_ok, tests_detail = run([sys.executable, "-m", "pytest", "-q", "operations/tests"], repo_root, test_env)
    tests_detail = re.sub(r"\bin\s+\d+(?:\.\d+)?s\b", "in <elapsed>", tests_detail)
    diff_ok, diff_detail = run(["git", "diff", "--check"], repo_root)
    if diff_ok:
        # Git's Windows line-ending notices are advisory stderr, not
        # whitespace defects, and depend on checkout configuration.
        diff_detail = ""
    scope_ok, scope_detail = validate_scope(repo_root, args.base_ref)

    report_path = campaign_dir / "validation-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["external_validation"] = {
        "json_jsonl_and_campaign_contracts": {"passed": not parse_errors, "details": {"errors": parse_errors, **parse_counts}},
        "generated_artifacts_reconcile_before_regeneration": {"passed": generated_reconciliation, "details": {"before": before, "after": after}},
        "regeneration_determinism": {"passed": deterministic, "details": after},
        "repository_tests": {"passed": tests_ok, "details": tests_detail},
        "forbidden_path_and_evidence_immutability": {"passed": scope_ok, "details": scope_detail},
        "git_diff_check": {"passed": diff_ok, "details": diff_detail},
    }
    internal_ok = all(check["passed"] for check in report["checks"])
    external_ok = all(value["passed"] for value in report["external_validation"].values())
    report["status"] = "pass" if internal_ok and external_ok else "fail"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"campaign_id": CAMPAIGN_ID, "status": report["status"]}, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
