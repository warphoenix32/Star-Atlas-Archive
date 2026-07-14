"""Validate the Wave 1.5 human-first repository migration."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_COUNTS = {
    "source_records": 800,
    "extractions": 800,
    "reconciliation": 960,
    "campaign_summary_files": 8,
    "schema_packages": 2,
}
REQUIRED_TOP_LEVEL = ("archive", "knowledge", "graph", "operations", "publication")
REMOVED_TOP_LEVEL = ("data", "kb", "pipeline", "templates", "docs", "tests", "examples")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def files(pattern: str) -> list[Path]:
    return sorted(ROOT.glob(pattern))


def count_artifacts() -> dict[str, int]:
    return {
        "source_records": len(files("archive/source-records/*/*.md")),
        "extractions": len(files("archive/ingestion-packages/*/extractions/*.json")),
        "reconciliation": len(files("archive/reconciliation/*/*.json")),
        "campaign_summary_files": len(files("archive/campaign-summaries/*/campaign-summary.*")),
        "schema_packages": len(files("archive/ingestion-packages/schema-v2.1/*.json")),
    }


def validate_layout(errors: list[str]) -> None:
    for name in REQUIRED_TOP_LEVEL:
        if not (ROOT / name).is_dir():
            errors.append(f"missing required top-level directory: {name}/")
    for name in REMOVED_TOP_LEVEL:
        if (ROOT / name).exists():
            errors.append(f"obsolete top-level path remains: {name}/")


def validate_counts(errors: list[str]) -> dict[str, int]:
    counts = count_artifacts()
    for key, expected in EXPECTED_COUNTS.items():
        if counts[key] != expected:
            errors.append(f"{key}: expected {expected}, found {counts[key]}")
    return counts


def validate_json(errors: list[str]) -> tuple[int, int]:
    json_count = 0
    jsonl_record_count = 0
    for path in files("**/*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
        except Exception as exc:  # noqa: BLE001 - validation should report every parse failure
            errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")
    for path in files("**/*.jsonl"):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                json.loads(line)
                jsonl_record_count += 1
            except Exception as exc:  # noqa: BLE001
                errors.append(f"invalid JSONL: {path.relative_to(ROOT)}:{number}: {exc}")
    return json_count, jsonl_record_count


def validate_campaign_pairs(errors: list[str]) -> None:
    package_root = ROOT / "archive" / "ingestion-packages"
    record_root = ROOT / "archive" / "source-records"
    for campaign in sorted(path.name for path in record_root.iterdir() if path.is_dir()):
        json_ids = {path.stem for path in (package_root / campaign / "extractions").glob("*.json")}
        markdown_ids = {path.stem for path in (record_root / campaign).glob("*.md")}
        for source_id in sorted(json_ids - markdown_ids):
            errors.append(f"missing Markdown source record: {campaign}/{source_id}")
        for source_id in sorted(markdown_ids - json_ids):
            errors.append(f"missing JSON extraction: {campaign}/{source_id}")

    all_ids = [path.stem for path in files("archive/ingestion-packages/*/extractions/*.json")]
    duplicates = sorted(source_id for source_id, count in Counter(all_ids).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate source IDs: {', '.join(duplicates)}")


def markdown_files_for_link_check() -> list[Path]:
    paths = [ROOT / "README.md"]
    for area in ("knowledge", "graph", "operations", "publication", "archive"):
        paths.extend(files(f"{area}/**/*.md"))
    return [
        path
        for path in sorted(set(paths))
        if "archive/source-records" not in path.as_posix()
        and "archive/campaign-summaries" not in path.as_posix()
    ]


def validate_markdown_links(errors: list[str]) -> int:
    checked = 0
    for path in markdown_files_for_link_check():
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip().strip("<>").split()[0]
            if not target or target.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            target = unquote(target.split("#", 1)[0])
            resolved = (path.parent / target).resolve()
            checked += 1
            if not resolved.exists():
                errors.append(
                    f"broken Markdown link: {path.relative_to(ROOT)} -> {match.group(1)}"
                )
    return checked


def main() -> int:
    errors: list[str] = []
    validate_layout(errors)
    counts = validate_counts(errors)
    json_count, jsonl_records = validate_json(errors)
    validate_campaign_pairs(errors)
    links_checked = validate_markdown_links(errors)

    print("Wave 1.5 migration validation")
    for key, value in counts.items():
        print(f"- {key}: {value}")
    print(f"- JSON documents parsed: {json_count}")
    print(f"- JSONL records parsed: {jsonl_records}")
    print(f"- local Markdown links checked: {links_checked}")
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
