import csv
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).parents[3]
CAMPAIGN = ROOT / "operations" / "campaigns" / "starbased-ship-states-ingestion-2026-07"
BUILD_PATH = CAMPAIGN / "build_campaign.py"
SPEC = importlib.util.spec_from_file_location("starbased_ship_states", BUILD_PATH)
builder = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


def generated_jsonl(rendered, relative_path):
    return [json.loads(line) for line in rendered[relative_path].splitlines() if line.strip()]


def test_raw_artifact_is_preserved_with_expected_checksum():
    assert builder.RAW_PATH.is_file()
    assert builder.sha256(builder.RAW_PATH) == builder.EXPECTED_SHA256


def test_source_has_expected_dimensions_and_unique_identifiers():
    with builder.RAW_PATH.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        headers = list(reader.fieldnames or [])
    assert (len(rows), len(headers)) == (63, 26)
    assert headers[0] == ""
    assert len({row[headers[0]] for row in rows}) == 63
    assert len({row["NameLinks to Marketplace"] for row in rows}) == 63


def test_build_is_deterministic_and_preview_matches_normalized():
    first = builder.build()
    second = builder.build()
    assert first == second
    preview = generated_jsonl(first, f"operations/campaigns/{builder.CAMPAIGN_ID}/normalized-preview.jsonl")
    normalized = generated_jsonl(first, builder.NORMALIZED_RECORDS_REL.as_posix())
    assert len(preview) == 63
    assert preview == normalized


def test_normalized_records_are_qualified_base_templates():
    rendered = builder.build()
    normalized = generated_jsonl(rendered, builder.NORMALIZED_RECORDS_REL.as_posix())
    assert all(item["record_type"] == "base_ship_template" for item in normalized)
    assert all(item["applicability"]["collection_completeness"] == "UNKNOWN" for item in normalized)
    assert all(item["applicability"]["current_availability"] == "UNKNOWN" for item in normalized)
    assert all(item["applicability"]["holosim"] == "OUT_OF_SCOPE_DIFFERENT_VALUE_SYSTEM" for item in normalized)
    assert all(item["applicability"]["component_modifiers"] == "NOT_APPLIED_INSTANCE_LEVEL_FUTURE_CONSIDERATION" for item in normalized)
    assert all(len(item["manual_review_flags"]) == 4 for item in normalized)


def test_concise_metrics_omit_only_documented_unknown_duplicates():
    rendered = builder.build()
    normalized = generated_jsonl(rendered, builder.NORMALIZED_RECORDS_REL.as_posix())
    mapping = json.loads(rendered[f"operations/campaigns/{builder.CAMPAIGN_ID}/normalization-map.json"])["columns"]
    omitted = [item for item in mapping if item["disposition"] == "omit_from_concise_normalized"]
    assert {item["source_header"] for item in omitted} == builder.OMITTED_SOURCE_HEADERS
    assert all(item["curator_decision"] == "OMIT_WITH_PROVENANCE" for item in omitted)
    omitted_targets = {item["normalized_field"] for item in omitted}
    assert all(len(item["metrics"]) == 20 for item in normalized)
    assert all(not omitted_targets.intersection(item["metrics"]) for item in normalized)


def test_warp_speed_is_literal_and_cooldowns_vary():
    normalized = generated_jsonl(builder.build(), builder.NORMALIZED_RECORDS_REL.as_posix())
    assert all(item["metrics"]["warp_speed_au_per_second"] == 100000 for item in normalized)
    assert len({item["metrics"]["warp_cooldown_seconds"] for item in normalized}) > 1


def test_mapping_covers_each_source_column_once():
    rendered = builder.build()
    mapping = json.loads(rendered[f"operations/campaigns/{builder.CAMPAIGN_ID}/normalization-map.json"])["columns"]
    source_headers = [item[0] for item in builder.COLUMN_MAP]
    assert [item["source_header"] for item in mapping] == source_headers
    assert len({item["normalized_field"] for item in mapping}) == 26


def test_curator_answers_are_complete_with_retained_research_gaps():
    questions = json.loads(builder.build()[f"operations/campaigns/{builder.CAMPAIGN_ID}/context-questions.json"])
    assert len(questions["questions"]) == 8
    assert questions["answered_question_count"] == 8
    assert questions["blocking_question_count"] == 0
    assert questions["research_gap_count"] == 4
    assert all(item["answer"] for item in questions["questions"])
    assert all(item["decision_status"] != "OPEN" for item in questions["questions"])
    assert all(item["decision_authority"] and item["evidence_class"] for item in questions["questions"])
