import importlib.util
import json
from collections import Counter
from pathlib import Path
import sys


ROOT = Path(__file__).parents[3]
BUILD_PATH = ROOT / "operations/campaigns/community-wallet-attribution-ingestion-2026-07/build_campaign.py"
SPEC = importlib.util.spec_from_file_location("community_wallet_attributions", BUILD_PATH)
builder = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


def records():
    rendered = builder.build_artifacts()[builder.NORMALIZED_RECORDS_REL.as_posix()]
    return [json.loads(line) for line in rendered.splitlines() if line]


def test_raw_workbook_checksum_and_dimensions():
    assert builder.sha256(builder.RAW_PATH) == builder.EXPECTED_SHA256
    sheet, rows = builder.load_source_rows()
    assert sheet == "SA Wallet List"
    assert len(rows) == 84


def test_records_preserve_source_values_and_rows():
    _, rows = builder.load_source_rows()
    normalized = records()
    assert [
        (item["address"], item["observed_label"], item["observed_major_group"], item["source"]["row_number"])
        for item in normalized
    ] == [
        (row["ADDRESS"], row["NAME"], row["Major Group"], int(row["_row_number"]))
        for row in rows
    ]


def test_addresses_and_ids_are_unique_and_syntactically_valid():
    normalized = records()
    assert len({item["record_id"] for item in normalized}) == 84
    assert len({item["address"] for item in normalized}) == 84
    assert all(item["address_format_status"] == "VALID_SOLANA_PUBLIC_KEY_SYNTAX" for item in normalized)


def test_group_counts_reconcile():
    assert Counter(item["observed_major_group"] for item in records()) == Counter(builder.EXPECTED_GROUP_COUNTS)


def test_attribution_never_becomes_verified_ownership():
    for item in records():
        assert item["relationship_claim"] == "COMMUNITY_ATTRIBUTED_ASSOCIATION"
        assert item["attribution"]["official_confirmation_status"] == "UNCONFIRMED"
        assert item["attribution"]["ownership_verification_status"] == "UNVERIFIED"
        assert item["attribution"]["control_verification_status"] == "UNVERIFIED"
        assert item["attribution"]["onchain_observation_status"] == "NOT_CHECKED"
        assert item["manual_review_required"] is True


def test_build_is_deterministic_and_source_record_is_paired():
    assert builder.build_artifacts() == builder.build_artifacts()
    rendered = builder.build_artifacts()
    assert builder.SOURCE_RECORD_JSON_REL.as_posix() in rendered
    assert builder.SOURCE_RECORD_MD_REL.as_posix() in rendered
