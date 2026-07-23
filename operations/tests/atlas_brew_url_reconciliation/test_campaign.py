import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).parents[3]
CAMPAIGN = ROOT / "operations" / "campaigns" / "atlas-brew-url-reconciliation-2026-07"
SCRIPT = CAMPAIGN / "reconcile_playlist.py"
SPEC = importlib.util.spec_from_file_location("atlas_brew_url_reconciliation", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def load(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def test_snapshot_counts_and_dispositions():
    manifest = load(
        "archive/provenance/atlas-brew-combined/youtube-playlist-manifest.json"
    )
    reconciliation = load(
        "archive/reconciliation/atlas-brew-combined/youtube-url-reconciliation.json"
    )
    assert manifest["item_count"] == 124
    assert reconciliation["source_record_count"] == 123
    assert reconciliation["status_counts"] == {"MATCHED": 123}
    assert reconciliation["match_confidence_counts"] == {"HIGH": 123}
    assert [item["video_id"] for item in reconciliation["playlist_only"]] == [
        "Yb8lZZ_zbhE"
    ]


def test_every_match_has_stable_url_date_and_unique_video_id():
    reconciliation = load(
        "archive/reconciliation/atlas-brew-combined/youtube-url-reconciliation.json"
    )
    decisions = reconciliation["decisions"]
    assert len({item["source_id"] for item in decisions}) == 123
    assert len({item["matched_video_id"] for item in decisions}) == 123
    assert all(
        item["canonical_url"]
        == f"https://www.youtube.com/watch?v={item['matched_video_id']}"
        for item in decisions
    )
    assert all(item["published_at"] for item in decisions)


def test_duplicate_episode_numbers_resolve_by_title_and_duration():
    reconciliation = load(
        "archive/reconciliation/atlas-brew-combined/youtube-url-reconciliation.json"
    )
    by_source = {item["source_id"]: item for item in reconciliation["decisions"]}
    expected = {
        "SRC-ATLAS-BREW-0003": "f1zOXj2rAEA",
        "SRC-ATLAS-BREW-0005": "F3YwFOGH8bA",
        "SRC-ATLAS-BREW-0017": "kL5QupAn8qI",
        "SRC-ATLAS-BREW-0021": "BVUXUbdqAEQ",
        "SRC-ATLAS-BREW-0040": "UMRHIK6Q8s4",
    }
    assert {
        source_id: by_source[source_id]["matched_video_id"]
        for source_id in expected
    } == expected
    assert all(
        by_source[source_id]["match_confidence"] == "HIGH"
        for source_id in expected
    )


def test_metadata_patch_is_additive_and_complete():
    patch = load(
        "archive/reconciliation/atlas-brew-combined/youtube-source-metadata-patch.json"
    )
    assert patch["purpose"] == "ADDITIVE_METADATA_PATCH; SOURCE RECORDS NOT REWRITTEN"
    assert len(patch["records"]) == 123
    assert all(item["match_confidence"] == "HIGH" for item in patch["records"])


def test_title_normalization_and_episode_parsing():
    assert module.episode_number("The Atlas Brew #190") == 190
    assert module.episode_number("Star Atlas Brew No.10 all about the ships") == 10
    assert module.episode_number("Metagravity Stress test brew") is None
    assert (
        module.normalize_title("🔴 LIVE — Atlas Brew #187")
        == module.normalize_title("The Atlas Brew #187")
    )
