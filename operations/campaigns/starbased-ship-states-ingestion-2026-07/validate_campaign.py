#!/usr/bin/env python3
"""Validate qualified Starbased ship-state preservation and normalization."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from build_campaign import (
    CAMPAIGN_ID,
    COLUMN_MAP,
    EXPECTED_SHA256,
    NORMALIZED_METADATA_REL,
    NORMALIZED_RECORDS_REL,
    OMITTED_SOURCE_HEADERS,
    PROVENANCE_REL,
    RAW_PATH,
    ROOT,
    build,
)


CAMPAIGN_DIR = Path(__file__).resolve().parent


def check(name: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "detail": detail}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(path: Path) -> str:
    """Hash repository-managed text with canonical UTF-8/LF line endings."""
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate() -> dict[str, Any]:
    generated = build()
    checks: list[dict[str, Any]] = []

    checks.append(check("raw_artifact_checksum", sha256(RAW_PATH) == EXPECTED_SHA256, sha256(RAW_PATH)))
    provenance = json.loads((ROOT / PROVENANCE_REL).read_text(encoding="utf-8"))
    checks.append(check(
        "provenance_reconciles_to_raw",
        provenance["raw_artifact"]["sha256"] == EXPECTED_SHA256
        and provenance["raw_artifact"]["byte_length"] == RAW_PATH.stat().st_size,
        provenance["raw_artifact"],
    ))
    checks.append(check(
        "qualified_lineage_is_nonassertive",
        provenance["custody"]["observed_distributor"] == "Ryden Systems"
        and provenance["custody"]["asserted_upstream_authority"] == "Star Atlas"
        and provenance["custody"]["lineage_verification"] == "NOT_INDEPENDENTLY_VERIFIED"
        and provenance["custody"]["upstream_document_url"] == "UNKNOWN"
        and provenance["custody"]["upstream_document_version"] == "UNKNOWN",
        provenance["custody"],
    ))
    checks.append(check(
        "provenance_excludes_local_personal_path",
        "Users/" not in json.dumps(provenance) and "Users\\" not in json.dumps(provenance),
        provenance["custody"]["original_filename"],
    ))

    with RAW_PATH.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        headers = list(reader.fieldnames or [])
    expected_headers = [item[0] for item in COLUMN_MAP]
    checks.append(check("exact_header_contract", headers == expected_headers, headers))
    checks.append(check("source_dimensions", len(rows) == 63 and len(headers) == 26, {"rows": len(rows), "columns": len(headers)}))
    checks.append(check("blank_first_header_only", headers[0] == "" and all(headers[1:]), headers[0]))
    checks.append(check("complete_cells", all(all(row[header].strip() for header in headers) for row in rows), None))
    checks.append(check("unique_ship_codes", len({row[headers[0]] for row in rows}) == len(rows), len(rows)))
    checks.append(check("unique_ship_names", len({row["NameLinks to Marketplace"] for row in rows}) == len(rows), len(rows)))
    checks.append(check("unique_complete_rows", len({tuple(row[header] for header in headers) for row in rows}) == len(rows), len(rows)))
    numeric_headers = [source for source, _, data_type, _, _, _ in COLUMN_MAP if data_type == "number"]
    numeric_failures = []
    for row_number, row in enumerate(rows, start=2):
        for header in numeric_headers:
            try:
                float(row[header])
            except ValueError:
                numeric_failures.append({"row": row_number, "header": header, "value": row[header]})
    checks.append(check("numeric_metric_cells", not numeric_failures, numeric_failures))

    for relative_path, expected_content in generated.items():
        path = ROOT / relative_path
        checks.append(check(
            f"generated_{relative_path.replace('/', '_')}_fixed_point",
            path.is_file() and path.read_text(encoding="utf-8") == expected_content,
            relative_path,
        ))
    checks.append(check("deterministic_build", generated == build(), sorted(generated)))

    preview = load_jsonl(CAMPAIGN_DIR / "normalized-preview.jsonl")
    normalized = load_jsonl(ROOT / NORMALIZED_RECORDS_REL)
    checks.append(check("preview_record_count", len(preview) == 63, len(preview)))
    checks.append(check("normalized_record_count", len(normalized) == 63, len(normalized)))
    checks.append(check("preview_exactly_reconciles_to_normalized", preview == normalized, len(normalized)))
    checks.append(check("normalized_record_ids_unique", len({item["record_id"] for item in normalized}) == 63, len(normalized)))
    checks.append(check(
        "normalized_source_rows_resolve",
        [item["source"]["row_number"] for item in normalized] == list(range(2, 65))
        and all(item["source"]["sha256"] == EXPECTED_SHA256 for item in normalized),
        {"first": normalized[0]["source"]["row_number"], "last": normalized[-1]["source"]["row_number"]},
    ))
    checks.append(check(
        "base_template_scope_and_module_qualifications",
        all(
            item["record_type"] == "base_ship_template"
            and item["applicability"]["value_scope"] == "BASE_SHIP_TEMPLATE"
            and item["applicability"]["basis"] == "OPERATOR_SUPPLIED_CONTEXT"
            and item["applicability"]["collection_completeness"] == "UNKNOWN"
            and item["applicability"]["current_availability"] == "UNKNOWN"
            and item["applicability"]["holosim"] == "OUT_OF_SCOPE_DIFFERENT_VALUE_SYSTEM"
            and item["applicability"]["component_modifiers"] == "NOT_APPLIED_INSTANCE_LEVEL_FUTURE_CONSIDERATION"
            for item in normalized
        ),
        len(normalized),
    ))
    checks.append(check(
        "manual_review_flags_retained",
        all(set(item["manual_review_flags"]) == {"RG01_UPSTREAM_DOCUMENT", "RG02_COLLECTION_COMPLETENESS", "RG03_MARKETPLACE_IDENTITY", "RG04_UNRESOLVED_UNITS"} for item in normalized),
        4,
    ))
    checks.append(check(
        "captured_identity_text_preserved",
        all(
            item["identity"]["ship_shorthand_code"] == row[headers[0]]
            and item["identity"]["ship_name_observed"] == row["NameLinks to Marketplace"]
            and item["identity"]["specialization_observed"] == row["Spec"]
            and item["identity"]["marketplace_alignment"] == "UNVERIFIED_PER_ROW"
            and item["identity"]["marketplace_url"] == "UNAVAILABLE_IN_SOURCE_ARTIFACT"
            for item, row in zip(normalized, rows)
        ),
        len(normalized),
    ))
    omitted_targets = {target for source, target, _, _, _, disposition in COLUMN_MAP if disposition == "omit_from_concise_normalized"}
    checks.append(check(
        "concise_metrics_and_omissions",
        all(len(item["metrics"]) == 20 and not omitted_targets.intersection(item["metrics"]) for item in normalized),
        {"included_metrics": 20, "omitted_metrics": sorted(omitted_targets)},
    ))
    checks.append(check(
        "literal_warp_speed_and_variable_cooldowns",
        all(item["metrics"]["warp_speed_au_per_second"] == 100000 for item in normalized)
        and len({item["metrics"]["warp_cooldown_seconds"] for item in normalized}) > 1,
        {"warp_speed": 100000, "distinct_cooldowns": len({item["metrics"]["warp_cooldown_seconds"] for item in normalized})},
    ))

    mapping = json.loads((CAMPAIGN_DIR / "normalization-map.json").read_text(encoding="utf-8"))
    omitted_entries = [item for item in mapping["columns"] if item["disposition"] == "omit_from_concise_normalized"]
    checks.append(check(
        "mapping_is_complete_and_non_circular",
        len(mapping["columns"]) == 26
        and [item["source_header"] for item in mapping["columns"]] == headers
        and len({item["normalized_field"] for item in mapping["columns"]}) == 26,
        len(mapping["columns"]),
    ))
    checks.append(check(
        "omitted_field_ledger_exact",
        {item["source_header"] for item in omitted_entries} == OMITTED_SOURCE_HEADERS
        and all(item["curator_decision"] == "OMIT_WITH_PROVENANCE" and item["omission_rationale"] for item in omitted_entries),
        [item["source_header"] for item in omitted_entries],
    ))
    questions = json.loads((CAMPAIGN_DIR / "context-questions.json").read_text(encoding="utf-8"))
    checks.append(check(
        "curator_answers_complete",
        len(questions["questions"]) == 8
        and questions["answered_question_count"] == 8
        and questions["blocking_question_count"] == 0
        and all(item["answer"] and item["decision_authority"] and item["evidence_class"] and item["decision_status"] != "OPEN" and item["remaining_gap"] for item in questions["questions"]),
        {"answered": questions["answered_question_count"], "blocking": questions["blocking_question_count"]},
    ))
    checks.append(check(
        "research_gaps_retained",
        questions["research_gap_count"] == 4
        and len(questions["research_gaps"]) == 4
        and all(item["manual_review"] for item in questions["research_gaps"]),
        [item["gap_id"] for item in questions["research_gaps"]],
    ))
    metadata = json.loads((ROOT / NORMALIZED_METADATA_REL).read_text(encoding="utf-8"))
    checks.append(check(
        "normalized_metadata_qualifies_scope",
        metadata["record_count"] == 63
        and metadata["collection_completeness"] == "UNKNOWN"
        and metadata["current_availability"] == "UNKNOWN"
        and metadata["source_lineage"]["independently_verified"] is False
        and len(metadata["field_disposition_ledger"]) == 3
        and len(metadata["manual_review_flags"]) == 4,
        {"records": metadata["record_count"], "research_gaps": len(metadata["manual_review_flags"])},
    ))

    manifest = json.loads((CAMPAIGN_DIR / "manifest.json").read_text(encoding="utf-8"))
    manifest_failures = []
    for item in manifest["files"]:
        path = ROOT / item["path"]
        observed_sha256 = sha256_text(path) if item["path"] == PROVENANCE_REL.as_posix() else sha256(path)
        if not path.is_file() or observed_sha256 != item["sha256"]:
            manifest_failures.append(item["path"])
    checks.append(check("manifest_checksums_resolve", not manifest_failures, manifest_failures))

    status = "pass" if all(item["passed"] for item in checks) else "fail"
    return {
        "campaign_id": CAMPAIGN_ID,
        "status": status,
        "checks": checks,
        "summary": {
            "checks_passed": sum(item["passed"] for item in checks),
            "checks_total": len(checks),
            "raw_artifacts": 1,
            "preview_records": len(preview),
            "normalized_records": len(normalized),
            "answered_context_questions": len(questions["questions"]),
            "blocking_context_questions": questions["blocking_question_count"],
            "remaining_research_gaps": questions["research_gap_count"],
        },
    }


if __name__ == "__main__":
    report = validate()
    (CAMPAIGN_DIR / "validation-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"campaign_id": CAMPAIGN_ID, "status": report["status"], "checks": report["summary"]["checks_total"]}))
    raise SystemExit(0 if report["status"] == "pass" else 1)
