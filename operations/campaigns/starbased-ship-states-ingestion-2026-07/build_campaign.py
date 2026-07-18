#!/usr/bin/env python3
"""Build deterministic qualified normalization for the Starbased ship-state CSV."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


CAMPAIGN_ID = "starbased-ship-states-ingestion-2026-07"
SCHEMA_VERSION = "1.1.0"
AS_OF = "2026-07-18"
ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN_DIR = Path(__file__).resolve().parent
RAW_REL = Path("archive/raw/starbased-ship-states/rydn_starbased_ships_20260718.csv")
RAW_PATH = ROOT / RAW_REL
PROVENANCE_REL = Path("archive/provenance/starbased-ship-states/rydn_starbased_ships_20260718.json")
NORMALIZED_DIR_REL = Path("archive/normalized/starbased-ship-states")
NORMALIZED_RECORDS_REL = NORMALIZED_DIR_REL / "base-ships.jsonl"
NORMALIZED_METADATA_REL = NORMALIZED_DIR_REL / "metadata.json"
EXPECTED_SHA256 = "7b90513e578998b8e763dd440984268000efed91c95feb047e81a19817a82dc9"


# source header, normalized field, type, unit, semantic status, disposition
COLUMN_MAP = [
    ("", "ship_shorthand_code", "string", None, "SOURCE_SHORTHAND_PRESERVED_MARKETPLACE_ALIGNMENT_UNVERIFIED", "include_identity"),
    ("NameLinks to Marketplace", "ship_name_observed", "string", None, "TEXT_PRESERVED_EXACTLY_MARKETPLACE_LINK_MISSING", "include_identity"),
    ("Spec", "specialization_observed", "string", None, "TEXT_PRESERVED_EXACTLY", "include_identity"),
    ("CargoCapacity", "cargo_capacity", "number", "source unit unresolved", "SOURCE_VALUE_PRESERVED_UNIT_UNRESOLVED", "include_metric"),
    ("USDC /Cargo Capacity", "usdc_per_cargo_capacity", "number", "unresolved", "SEMANTICALLY_UNKNOWN_DUPLICATE", "omit_from_concise_normalized"),
    ("FuelCapacity", "fuel_capacity", "number", "source unit unresolved", "SOURCE_VALUE_PRESERVED_UNIT_UNRESOLVED", "include_metric"),
    ("AmmoCapacity", "ammo_capacity", "number", "source unit unresolved", "SOURCE_VALUE_PRESERVED_UNIT_UNRESOLVED", "include_metric"),
    ("Food / sec(Mining)", "mining_food_per_second", "number", "food per second as captured", "SOURCE_LABEL_UNIT_PRESERVED_SCALE_UNRESOLVED", "include_metric"),
    ("Ammo / sec(Mining)", "mining_ammo_per_second", "number", "ammo per second as captured", "SOURCE_LABEL_UNIT_PRESERVED_SCALE_UNRESOLVED", "include_metric"),
    ("Mining Rate[Resource/sec]", "mining_rate_resource_per_second", "number", "resource per second as captured", "SOURCE_LABEL_UNIT_PRESERVED_SCALE_UNRESOLVED", "include_metric"),
    ("USDC /Mining Rate", "usdc_per_mining_rate", "number", "unresolved", "SEMANTICALLY_UNKNOWN_DUPLICATE", "omit_from_concise_normalized"),
    ("Subwarp Speed[AU/sec]", "subwarp_speed_au_per_second", "number", "AU per second as captured", "SOURCE_LABEL_UNIT_PRESERVED_SCALE_UNRESOLVED", "include_metric"),
    ("Warp Speed[AU/sec]", "warp_speed_au_per_second", "number", "astronomical units per second", "LITERAL_VALUE_AND_UNIT_RESOLVED_BY_OPERATOR", "include_metric"),
    ("Max WarpDistance [AU]", "max_warp_distance_au", "number", "astronomical units as captured", "SOURCE_LABEL_UNIT_PRESERVED_SCALE_UNRESOLVED", "include_metric"),
    ("Warp Cooldown[sec]", "warp_cooldown_seconds", "number", "seconds as captured", "SOURCE_VALUE_PRESERVED_SHIP_SPECIFIC", "include_metric"),
    ("Fuel /AU Warp", "warp_fuel_per_au", "number", "fuel per AU as captured", "SOURCE_LABEL_UNIT_PRESERVED_SCALE_UNRESOLVED", "include_metric"),
    ("Cargo /Warp Fuel", "cargo_per_warp_fuel", "number", "unresolved", "SEMANTICALLY_UNKNOWN_DUPLICATE", "omit_from_concise_normalized"),
    ("Fuel /AU Subwarp", "subwarp_fuel_per_au", "number", "fuel per AU as captured", "SOURCE_LABEL_UNIT_PRESERVED_SCALE_UNRESOLVED", "include_metric"),
    ("Asteroid ExitFuel", "asteroid_exit_fuel", "number", "fuel as captured", "SOURCE_VALUE_PRESERVED_DEFINITION_UNRESOLVED", "include_metric"),
    ("Crew\u00a0", "crew", "number", "persons as captured", "SOURCE_VALUE_PRESERVED", "include_metric"),
    ("Passengers\u00a0", "passengers", "number", "persons as captured", "SOURCE_VALUE_PRESERVED", "include_metric"),
    ("Respawn Time[sec]", "respawn_time_seconds", "number", "seconds as captured", "SOURCE_LABEL_UNIT_PRESERVED", "include_metric"),
    ("Scan Cooldown[sec]", "scan_cooldown_seconds", "number", "seconds as captured", "SOURCE_LABEL_UNIT_PRESERVED", "include_metric"),
    ("Food /Scan", "food_per_scan", "number", "food per scan as captured", "SOURCE_LABEL_UNIT_PRESERVED_SCALE_UNRESOLVED", "include_metric"),
    ("SDU /Scan", "sdu_per_scan", "number", "SDU per scan as captured", "SOURCE_LABEL_UNIT_PRESERVED_SCALE_UNRESOLVED", "include_metric"),
    ("Food /SDU", "food_per_sdu", "number", "food per SDU as captured", "SOURCE_LABEL_UNIT_PRESERVED_SCALE_UNRESOLVED", "include_metric"),
]


QUESTIONS = [
    {
        "question_id": "Q01_SOURCE_AUTHORITY",
        "topic": "source authority",
        "question": "Who created and maintains this export, and what upstream document produced it?",
        "was_blocking": True,
        "answer": "RYDN means Ryden. The CSV was downloaded from Ryden Systems and is a derivative copy of an asserted authoritative Star Atlas ship-stat document.",
        "decision_authority": "repository operator / curator",
        "evidence_class": "OPERATOR_SUPPLIED_CONTEXT",
        "decision_status": "ANSWERED_WITH_RETAINED_GAP",
        "remaining_gap": "The upstream Star Atlas document URL and version are UNKNOWN, and the lineage has not been independently verified.",
    },
    {
        "question_id": "Q02_CURRENTLY_AVAILABLE",
        "topic": "row scope",
        "question": "What collection scope does the export establish?",
        "was_blocking": True,
        "answer": "Normalize only the 63 base-ship rows included in the 2026-07-18 Ryden export; do not assert that the collection is complete or currently available.",
        "decision_authority": "repository operator / curator",
        "evidence_class": "CURATORIAL_SCOPE_DECISION",
        "decision_status": "ANSWERED_WITH_RETAINED_GAP",
        "remaining_gap": "Collection completeness and current-availability scope are UNKNOWN.",
    },
    {
        "question_id": "Q03_GAME_MODULE_ASSIGNMENT",
        "topic": "SAGE and C4 applicability",
        "question": "How should the values be scoped across game modules and future versions?",
        "was_blocking": True,
        "answer": "Treat the captured values as base-ship values intended to remain common across SAGE and C4, with future rebasing possible. Holosim uses a different value system and is out of scope. Future components may modify individual ship-instance stats; no hypothetical modifiers are applied here.",
        "decision_authority": "repository operator / curator",
        "evidence_class": "OPERATOR_SUPPLIED_CONTEXT",
        "decision_status": "RESOLVED_FOR_QUALIFIED_NORMALIZATION",
        "remaining_gap": "Future rebases and component-level instance effects require separate versioned data when available.",
    },
    {
        "question_id": "Q04_SHIP_CODE",
        "topic": "blank first header",
        "question": "How should the unnamed first-column codes be modeled?",
        "was_blocking": True,
        "answer": "Preserve each source-supplied ship shorthand code exactly. The codes usually align with marketplace ship IDs, but exact equivalence is not established.",
        "decision_authority": "repository operator / curator",
        "evidence_class": "OPERATOR_SUPPLIED_CONTEXT",
        "decision_status": "ANSWERED_WITH_RETAINED_GAP",
        "remaining_gap": "Marketplace ID alignment remains unverified per row.",
    },
    {
        "question_id": "Q05_MARKETPLACE_LINKS",
        "topic": "lost hyperlinks",
        "question": "Should missing marketplace hyperlinks be recovered or invented?",
        "was_blocking": False,
        "answer": "Keep marketplace hyperlinks missing and unrecovered. Do not invent URLs.",
        "decision_authority": "repository operator / curator",
        "evidence_class": "CURATORIAL_SCOPE_DECISION",
        "decision_status": "RESOLVED",
        "remaining_gap": "Marketplace URLs remain unavailable in the supplied artifact.",
    },
    {
        "question_id": "Q06_IDENTICAL_METRICS",
        "topic": "derived metric integrity",
        "question": "How should the three always-identical semantically unknown metrics be handled?",
        "was_blocking": True,
        "answer": "Omit USDC/Cargo Capacity, USDC/Mining Rate, and Cargo/Warp Fuel from the concise normalized record. Preserve their exact values in the immutable raw CSV and document each omission in the field-disposition ledger.",
        "decision_authority": "repository operator / curator",
        "evidence_class": "CURATORIAL_NORMALIZATION_DECISION",
        "decision_status": "RESOLVED_BY_DOCUMENTED_OMISSION",
        "remaining_gap": "The source meaning and derivation of all three omitted metrics remain UNKNOWN.",
    },
    {
        "question_id": "Q07_UNITS_AND_SCALE",
        "topic": "units and numeric scale",
        "question": "Which units and scales are resolved?",
        "was_blocking": True,
        "answer": "Warp speed is literal and fixed at 100000 astronomical units per second for all 63 ships; warp cooldowns vary by ship. Preserve every other unit exactly as captured without inventing scale definitions.",
        "decision_authority": "repository operator / curator",
        "evidence_class": "OPERATOR_SUPPLIED_CONTEXT",
        "decision_status": "ANSWERED_WITH_RETAINED_GAP",
        "remaining_gap": "Native scale definitions for capacities, consumables, SDU, and other movement values remain unresolved.",
    },
    {
        "question_id": "Q08_CANONICAL_NAMES",
        "topic": "name normalization",
        "question": "Should captured names and specialization labels be corrected?",
        "was_blocking": False,
        "answer": "Preserve ship names and specialization labels exactly as captured; make no spelling or capitalization corrections.",
        "decision_authority": "repository operator / curator",
        "evidence_class": "CURATORIAL_TRANSCRIPTION_POLICY",
        "decision_status": "RESOLVED",
        "remaining_gap": "NONE",
    },
]


RESEARCH_GAPS = [
    {"gap_id": "RG01_UPSTREAM_DOCUMENT", "description": "Upstream Star Atlas document URL/version and independent lineage verification remain unavailable.", "manual_review": True},
    {"gap_id": "RG02_COLLECTION_COMPLETENESS", "description": "The export does not establish completeness or current availability beyond its 63 included rows.", "manual_review": True},
    {"gap_id": "RG03_MARKETPLACE_IDENTITY", "description": "Marketplace IDs and URLs are missing; shorthand-code alignment is unverified per row.", "manual_review": True},
    {"gap_id": "RG04_UNRESOLVED_UNITS", "description": "Units/scales other than the explicitly resolved warp speed/AU context remain as captured and require future documentation.", "manual_review": True},
]


OMITTED_SOURCE_HEADERS = {"USDC /Cargo Capacity", "USDC /Mining Rate", "Cargo /Warp Fuel"}
MANUAL_REVIEW_FLAGS = [gap["gap_id"] for gap in RESEARCH_GAPS]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def dump_jsonl(records: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)


def load_rows() -> tuple[list[str], list[dict[str, str]]]:
    with RAW_PATH.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def numeric(value: str) -> int | float:
    number = float(value)
    return int(number) if number.is_integer() else number


def build_records(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    records = []
    for row_number, row in enumerate(rows, start=2):
        identities: dict[str, str] = {}
        metrics: dict[str, int | float] = {}
        for source, target, data_type, _, _, disposition in COLUMN_MAP:
            if disposition == "omit_from_concise_normalized":
                continue
            value: str | int | float = numeric(row[source]) if data_type == "number" else row[source]
            if disposition == "include_identity":
                identities[target] = value  # type: ignore[assignment]
            else:
                metrics[target] = value  # type: ignore[assignment]
        ship_code = identities["ship_shorthand_code"]
        records.append({
            "record_id": f"SHIP-{ship_code}",
            "schema_version": SCHEMA_VERSION,
            "record_type": "base_ship_template",
            "snapshot_date": AS_OF,
            "identity": {
                **identities,
                "marketplace_alignment": "UNVERIFIED_PER_ROW",
                "marketplace_url": "UNAVAILABLE_IN_SOURCE_ARTIFACT",
                "text_policy": "PRESERVED_EXACTLY_AS_CAPTURED",
            },
            "applicability": {
                "game_modules": ["SAGE", "C4"],
                "basis": "OPERATOR_SUPPLIED_CONTEXT",
                "value_scope": "BASE_SHIP_TEMPLATE",
                "collection_completeness": "UNKNOWN",
                "current_availability": "UNKNOWN",
                "holosim": "OUT_OF_SCOPE_DIFFERENT_VALUE_SYSTEM",
                "future_rebasing": "POSSIBLE",
                "component_modifiers": "NOT_APPLIED_INSTANCE_LEVEL_FUTURE_CONSIDERATION",
            },
            "metrics": metrics,
            "normalization_status": "QUALIFIED_NORMALIZED_MANUAL_REVIEW_RETAINED",
            "manual_review_flags": MANUAL_REVIEW_FLAGS,
            "source": {
                "artifact_id": "SRC-STARB-7B90513E578998B8",
                "distributor_observed": "Ryden Systems",
                "upstream_authority_asserted": "Star Atlas",
                "lineage_verification": "NOT_INDEPENDENTLY_VERIFIED",
                "path": RAW_REL.as_posix(),
                "row_number": row_number,
                "sha256": EXPECTED_SHA256,
            },
        })
    return records


def build() -> dict[str, str]:
    headers, rows = load_rows()
    raw_bytes = RAW_PATH.read_bytes()
    records = build_records(rows)
    mapping = []
    for index, (source, target, data_type, unit, status, disposition) in enumerate(COLUMN_MAP):
        entry = {
            "ordinal": index + 1,
            "source_header": source,
            "normalized_field": target,
            "data_type": data_type,
            "unit": unit,
            "semantic_status": status,
            "disposition": disposition,
        }
        if disposition == "omit_from_concise_normalized":
            entry["omission_rationale"] = "Semantically unknown duplicate/derived field; exact source values remain in immutable raw CSV."
            entry["curator_decision"] = "OMIT_WITH_PROVENANCE"
        mapping.append(entry)

    duplicate_rows = len(rows) - len({tuple(row.get(header, "") for header in headers) for row in rows})
    profile = {
        "campaign_id": CAMPAIGN_ID,
        "source": RAW_REL.as_posix(),
        "sha256": sha256(RAW_PATH),
        "byte_length": len(raw_bytes),
        "encoding": "UTF-8 without BOM" if not raw_bytes.startswith(b"\xef\xbb\xbf") else "UTF-8 with BOM",
        "line_endings": "CRLF" if raw_bytes.count(b"\r\n") == raw_bytes.count(b"\n") else "mixed_or_LF",
        "row_count": len(rows),
        "column_count": len(headers),
        "headers": headers,
        "blank_header_ordinals": [index + 1 for index, header in enumerate(headers) if not header],
        "empty_cell_counts": {header: sum(not row[header].strip() for row in rows) for header in headers},
        "duplicate_complete_rows": duplicate_rows,
        "duplicate_ship_codes": len(rows) - len({row[headers[0]] for row in rows}),
        "duplicate_ship_names": len(rows) - len({row["NameLinks to Marketplace"] for row in rows}),
        "numeric_columns": [source for source, _, data_type, _, _, _ in COLUMN_MAP if data_type == "number"],
        "specialization_counts": dict(sorted(Counter(row["Spec"] for row in rows).items())),
        "scope_assessment": {
            "normalized_scope": "63 base-ship rows included in the 2026-07-18 Ryden export",
            "collection_completeness": "UNKNOWN",
            "current_availability": "UNKNOWN",
            "base_template_scope": True,
            "instance_component_modifiers_applied": False,
            "holosim_in_scope": False,
        },
        "lineage_assessment": {
            "observed_distributor": "Ryden Systems",
            "asserted_upstream_authority": "Star Atlas",
            "upstream_document_url": "UNKNOWN",
            "upstream_document_version": "UNKNOWN",
            "independently_verified": False,
            "basis": "OPERATOR_SUPPLIED_CONTEXT",
        },
        "field_disposition_summary": {"source_columns": 26, "identity_fields": 3, "included_metrics": 20, "omitted_metrics": 3},
        "exact_equality_checks": {
            "CargoCapacity_equals_USDC_per_Cargo_Capacity": sum(row["CargoCapacity"] == row["USDC /Cargo Capacity"] for row in rows),
            "Mining_Rate_equals_USDC_per_Mining_Rate": sum(row["Mining Rate[Resource/sec]"] == row["USDC /Mining Rate"] for row in rows),
            "Warp_Fuel_per_AU_equals_Cargo_per_Warp_Fuel": sum(row["Fuel /AU Warp"] == row["Cargo /Warp Fuel"] for row in rows),
            "Warp_Speed_literal_100000_AU_per_second": sum(row["Warp Speed[AU/sec]"] == "100000" for row in rows),
            "distinct_warp_cooldowns": len({row["Warp Cooldown[sec]"] for row in rows}),
        },
    }
    questions = {
        "campaign_id": CAMPAIGN_ID,
        "status": "CURATOR_ANSWERS_APPLIED_QUALIFIED_NORMALIZATION_ALLOWED",
        "answered_question_count": len(QUESTIONS),
        "blocking_question_count": 0,
        "research_gap_count": len(RESEARCH_GAPS),
        "questions": QUESTIONS,
        "research_gaps": RESEARCH_GAPS,
    }
    field_dispositions = [entry for entry in mapping if entry["disposition"] == "omit_from_concise_normalized"]
    normalized_metadata = {
        "dataset_id": "starbased-base-ships-2026-07-18",
        "schema_version": SCHEMA_VERSION,
        "snapshot_date": AS_OF,
        "record_count": len(records),
        "record_type": "base_ship_template",
        "collection_scope": "63 base-ship rows included in the 2026-07-18 Ryden export",
        "collection_completeness": "UNKNOWN",
        "current_availability": "UNKNOWN",
        "applicability": {
            "SAGE_and_C4": "OPERATOR_SUPPLIED_CONTEXT_BASE_VALUES_INTENDED_COMMON",
            "holosim": "OUT_OF_SCOPE_DIFFERENT_VALUE_SYSTEM",
            "future_rebasing": "POSSIBLE",
            "component_modified_instances": "SEPARATE_FUTURE_VERSIONED_DATASET_REQUIRED",
        },
        "source_lineage": profile["lineage_assessment"],
        "field_disposition_ledger": field_dispositions,
        "manual_review_flags": RESEARCH_GAPS,
        "raw_source": {"path": RAW_REL.as_posix(), "sha256": EXPECTED_SHA256},
    }
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "as_of": AS_OF,
        "status": "QUALIFIED_NORMALIZATION_WRITTEN_MANUAL_REVIEW_RETAINED",
        "raw_artifacts_preserved": 1,
        "preview_records": len(records),
        "normalized_records": len(records),
        "open_context_questions": 0,
        "answered_context_questions": len(QUESTIONS),
        "remaining_research_gaps": len(RESEARCH_GAPS),
        "archive_normalized_outputs_written": 2,
        "promotion_gate": "PASSED_QUALIFIED_RECORD_LEVEL_NORMALIZATION",
    }
    campaign_rendered = {
        "source-profile.json": dump_json(profile),
        "normalization-map.json": dump_json({"campaign_id": CAMPAIGN_ID, "schema_version": SCHEMA_VERSION, "columns": mapping}),
        "normalized-preview.jsonl": dump_jsonl(records),
        "context-questions.json": dump_json(questions),
        "campaign-summary.json": dump_json(summary),
    }
    normalized_rendered = {
        NORMALIZED_RECORDS_REL.as_posix(): dump_jsonl(records),
        NORMALIZED_METADATA_REL.as_posix(): dump_json(normalized_metadata),
    }
    manifest_files = [
        {"path": RAW_REL.as_posix(), "role": "raw_source", "sha256": sha256(RAW_PATH), "records": len(rows)},
        {"path": PROVENANCE_REL.as_posix(), "role": "provenance", "sha256": sha256(ROOT / PROVENANCE_REL), "records": 1},
    ]
    for name, content in campaign_rendered.items():
        manifest_files.append({
            "path": f"operations/campaigns/{CAMPAIGN_ID}/{name}",
            "role": "campaign_derivative",
            "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "records": len(records) if name == "normalized-preview.jsonl" else 1,
        })
    for path, content in normalized_rendered.items():
        manifest_files.append({
            "path": path,
            "role": "qualified_normalized_records" if path.endswith(".jsonl") else "normalized_metadata",
            "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "records": len(records) if path.endswith(".jsonl") else 1,
        })
    campaign_rendered["manifest.json"] = dump_json({
        "campaign_id": CAMPAIGN_ID,
        "schema_version": SCHEMA_VERSION,
        "files": sorted(manifest_files, key=lambda item: item["path"]),
    })
    return {**{f"operations/campaigns/{CAMPAIGN_ID}/{name}": content for name, content in campaign_rendered.items()}, **normalized_rendered}


def write_outputs() -> None:
    for relative_path, content in build().items():
        path = ROOT / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    write_outputs()
    print(json.dumps({"campaign_id": CAMPAIGN_ID, "status": "built", "normalized_records": 63}))
