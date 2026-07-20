#!/usr/bin/env python3
"""Validate the community wallet-attribution ingestion campaign."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import build_campaign as builder


ROOT = builder.ROOT
CAMPAIGN_DIR = builder.CAMPAIGN_DIR


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def parse_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate() -> dict:
    require(builder.RAW_PATH.is_file(), "raw workbook is missing")
    require(builder.sha256(builder.RAW_PATH) == builder.EXPECTED_SHA256, "raw workbook checksum mismatch")
    sheet_name, source_rows = builder.load_source_rows()
    require(sheet_name == "SA Wallet List", "unexpected worksheet name")
    require(len(source_rows) == 84, "expected 84 workbook data rows")

    expected = builder.build_artifacts()
    for relative, content in expected.items():
        path = ROOT / relative
        require(path.is_file(), f"missing generated artifact: {relative}")
        require(path.read_text(encoding="utf-8") == content, f"generated artifact does not reconcile: {relative}")

    records = parse_jsonl(ROOT / builder.NORMALIZED_RECORDS_REL)
    require(len(records) == 84, "normalized record count must be 84")
    require(len({item["record_id"] for item in records}) == 84, "record IDs must be unique")
    require(len({item["address"] for item in records}) == 84, "addresses must be unique")
    require(all(item["address_format_status"] == "VALID_SOLANA_PUBLIC_KEY_SYNTAX" for item in records), "every address must be a syntactically valid 32-byte Solana public key")
    require(Counter(item["observed_major_group"] for item in records) == Counter(builder.EXPECTED_GROUP_COUNTS), "major-group counts do not reconcile")
    require(all(item["attribution"]["official_confirmation_status"] == "UNCONFIRMED" for item in records), "official confirmation must remain UNCONFIRMED")
    require(all(item["attribution"]["ownership_verification_status"] == "UNVERIFIED" for item in records), "ownership must remain UNVERIFIED")
    require(all(item["attribution"]["control_verification_status"] == "UNVERIFIED" for item in records), "control must remain UNVERIFIED")
    require(all(item["attribution"]["onchain_observation_status"] == "NOT_CHECKED" for item in records), "on-chain observation must remain NOT_CHECKED")
    require(all(item["manual_review_required"] is True for item in records), "every attribution record must retain manual review")

    observed = [(item["address"], item["observed_label"], item["observed_major_group"], item["source"]["row_number"]) for item in records]
    supplied = [(row["ADDRESS"], row["NAME"], row["Major Group"], int(row["_row_number"])) for row in source_rows]
    require(observed == supplied, "normalized values or row provenance differ from the workbook")
    require((ROOT / builder.SOURCE_RECORD_JSON_REL).is_file() and (ROOT / builder.SOURCE_RECORD_MD_REL).is_file(), "paired Source Records are required")

    forbidden = ["knowledge", "graph", "publication"]
    diff = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    require(not any(path == prefix or path.startswith(prefix + "/") for path in diff for prefix in forbidden), "forbidden knowledge/graph/publication change detected")

    first = builder.build_artifacts()
    second = builder.build_artifacts()
    require(first == second, "campaign build is not deterministic")
    return {
        "campaign_id": builder.CAMPAIGN_ID,
        "result": "PASS",
        "checks": {
            "raw_checksum": "PASS",
            "workbook_dimensions": "PASS",
            "source_value_fidelity": "PASS",
            "unique_record_ids": "PASS",
            "unique_addresses": "PASS",
            "solana_address_syntax": "PASS",
            "qualified_attribution_semantics": "PASS",
            "source_record_pairing": "PASS",
            "deterministic_build": "PASS",
            "forbidden_paths": "PASS",
        },
        "counts": {"records": 84, "unique_addresses": 84, "manual_review_records": 84},
        "limitations": [gap["description"] for gap in builder.RESEARCH_GAPS],
    }


def main() -> int:
    try:
        report = validate()
    except (ValidationFailure, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    report_path = CAMPAIGN_DIR / "validation-report.json"
    report_path.write_text(builder.dump_json(report), encoding="utf-8", newline="\n")
    markdown = """# Validation Report

**Result: PASS**

- Raw workbook checksum reconciles.
- All 84 source rows reconcile exactly to 84 unique normalized records.
- All 84 addresses decode as syntactically valid 32-byte Solana public keys.
- Official confirmation remains `UNCONFIRMED`; ownership and control remain `UNVERIFIED`.
- On-chain observation remains `NOT_CHECKED`.
- Paired JSON and Markdown Source Records are present.
- Generated artifacts are deterministic.
- No `knowledge/`, `graph/`, or `publication/` files are changed.

Syntactic address validity is not ownership, control, purpose, activity, or historical-duration verification.
"""
    (CAMPAIGN_DIR / "validation-report.md").write_text(markdown, encoding="utf-8", newline="\n")
    print("PASS community wallet-attribution campaign: 84/84 qualified records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
