import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit

import pytest


ROOT = Path(__file__).parents[3]
CAMPAIGN_DIR = ROOT / "operations" / "campaigns" / "legacy-written-raw-recovery-2026-07"
CI_PATH = ROOT / "operations" / "ci" / "validate_repository.py"
sys.path.insert(0, str(CI_PATH.parent))
SPEC = importlib.util.spec_from_file_location("legacy_raw_recovery_ci", CI_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(validator)


CAMPAIGN_PATHS = [
    "archive/raw/legacy-written-recovery/delta/SRC-OFF-EXAMPLE.html",
    "archive/provenance/legacy-written-recovery/delta/SRC-OFF-EXAMPLE.json",
    "archive/manifests/legacy-written-raw-recovery-2026-07.json",
    "operations/campaigns/legacy-written-raw-recovery-2026-07/validation-report.json",
    "operations/tests/legacy_written_raw_recovery/test_ci_contract.py",
    "operations/ci/validate_repository.py",
]


def test_campaign_paths_select_the_legacy_recovery_contract():
    assert validator.validate_forbidden_paths(CAMPAIGN_PATHS) == "legacy-written-raw-recovery-2026-07"


def test_campaign_contract_rejects_changes_outside_its_exact_paths():
    with pytest.raises(validator.ValidationFailure, match="forbidden-path"):
        validator.validate_forbidden_paths(CAMPAIGN_PATHS + ["knowledge/gameplay/SAGE.md"])


def test_similarly_named_manifest_does_not_select_the_campaign():
    with pytest.raises(validator.ValidationFailure, match="exactly one recognized campaign"):
        validator.validate_forbidden_paths(["archive/manifests/legacy-written-raw-recovery-draft.json"])


def test_campaign_validation_runs_twice_offline_and_checks_all_artifact_roots(monkeypatch):
    cycles = []
    commands = []

    def fake_run_cycle(command, root, exclusions, env=None):
        cycles.append((command, root, exclusions, env))
        return {"validation-report.json": "stable-checksum"}

    def fake_run(*args, **kwargs):
        commands.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(validator, "run_cycle", fake_run_cycle)
    monkeypatch.setattr(validator, "run", fake_run)

    validator.validate_legacy_written_raw_recovery_campaign()

    assert len(cycles) == 2
    assert cycles[0][0] == cycles[1][0]
    assert cycles[0][0][-1].replace("\\", "/").endswith(
        "operations/campaigns/legacy-written-raw-recovery-2026-07/validate_campaign.py"
    )
    assert cycles[0][3]["NO_NETWORK"] == "1"
    assert cycles[0][3]["STAR_ATLAS_OFFLINE_VALIDATION"] == "1"
    assert cycles[1][3]["NO_NETWORK"] == "1"
    assert cycles[1][3]["STAR_ATLAS_OFFLINE_VALIDATION"] == "1"

    diff_command = commands[-1]
    assert diff_command[:4] == ("git", "diff", "--exit-code", "--")
    normalized_diff_paths = {value.replace("\\", "/") for value in diff_command[4:]}
    assert "archive/raw/legacy-written-recovery" in normalized_diff_paths
    assert "archive/provenance/legacy-written-recovery" in normalized_diff_paths
    assert "archive/manifests/legacy-written-raw-recovery-2026-07.json" in normalized_diff_paths
    assert "operations/campaigns/legacy-written-raw-recovery-2026-07" in normalized_diff_paths
    assert "operations/tests/legacy_written_raw_recovery" in normalized_diff_paths


def test_campaign_validation_reports_nondeterministic_artifacts(monkeypatch):
    snapshots = iter(({"validation-report.json": "first"}, {"validation-report.json": "second"}))
    monkeypatch.setattr(validator, "run_cycle", lambda *args, **kwargs: next(snapshots))

    with pytest.raises(validator.ValidationFailure, match="not deterministic"):
        validator.validate_legacy_written_raw_recovery_campaign()


def test_aephia_expansion_selection_is_fixed_and_disjoint_from_pilot():
    selection = json.loads((CAMPAIGN_DIR / "expansion-aephia-selection.json").read_text(encoding="utf-8"))
    selected_ids = [item["source_id"] for item in selection["records"]]

    assert selection["batch_id"] == "aephia-family-remaining-59"
    assert len(selected_ids) == 59
    assert len(selected_ids) == len(set(selected_ids))
    assert not set(selected_ids).intersection(selection["pilot_source_ids_excluded"])
    assert all(urlsplit(item["retrieval_url"]).netloc == "aephia.com" for item in selection["records"])
    assert all(urlsplit(item["retrieval_url"]).path.startswith("/wp-json/wp/v2/") for item in selection["records"])
    assert all(item["retrieval_url_basis"] == "PRIOR_FINAL_URL" for item in selection["records"])


def test_aephia_expansion_has_complete_identity_matched_terminal_coverage():
    ledger_path = CAMPAIGN_DIR / "expansion-aephia-retrieval-ledger.jsonl"
    records = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line]

    assert len(records) == 59
    assert all(item["retrieval_batch_id"] == "aephia-family-remaining-59" for item in records)
    assert all(item["terminal_disposition"] == "CAPTURED_LIVE" for item in records)
    assert all(item["identity_status"] == "MATCH" for item in records)
    assert not any(item["manual_review_required"] for item in records)
    assert (CAMPAIGN_DIR / "expansion-aephia-manual-review-queue.jsonl").read_bytes() == b""


def test_hnn_completion_selection_is_fixed_and_reconciles_to_the_family():
    selection = json.loads((CAMPAIGN_DIR / "expansion-hnn-selection.json").read_text(encoding="utf-8"))
    selected_ids = [item["source_id"] for item in selection["records"]]

    assert selection["batch_id"] == "hnn-written-family-completion-156"
    assert selection["expected_record_count"] == 156
    assert selection["family_record_count"] == 157
    assert len(selected_ids) == len(set(selected_ids)) == 156
    assert selection["preserved_baseline_source_ids"] == ["SRC-HNN-04DD15F547F461E7"]
    assert len(selection["pilot_source_ids_repaired"]) == 4
    assert not set(selected_ids).intersection(selection["preserved_baseline_source_ids"])
    assert all(urlsplit(item["retrieval_url"]).netloc in {"medium.com", "web.archive.org"} for item in selection["records"])


def test_hnn_completion_has_full_preserved_coverage_and_no_manual_queue():
    ledger_path = CAMPAIGN_DIR / "expansion-hnn-retrieval-ledger.jsonl"
    records = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line]
    resolutions = [
        json.loads(line)
        for line in (CAMPAIGN_DIR / "expansion-hnn-archive-resolution-ledger.jsonl").read_text(encoding="utf-8").splitlines()
        if line
    ]

    assert len(records) == len({item["source_id"] for item in records}) == 156
    assert len(resolutions) == len({item["source_id"] for item in resolutions}) == 156
    assert all(item["retrieval_batch_id"] == "hnn-written-family-completion-156" for item in records)
    assert all(item["body_path"] and item["provenance_path"] for item in records)
    assert {item["terminal_disposition"] for item in records} == {"CAPTURED_ARCHIVE", "CAPTURED_LIVE"}
    assert sum(item["terminal_disposition"] == "CAPTURED_ARCHIVE" for item in records) == 144
    assert sum(item["terminal_disposition"] == "CAPTURED_LIVE" for item in records) == 12
    assert all(item["identity_status"] in {"MATCH", "CONSISTENT"} for item in records)
    assert not any(item["manual_review_required"] for item in records)
    assert (CAMPAIGN_DIR / "expansion-hnn-manual-review-queue.jsonl").read_bytes() == b""


def test_official_completion_selection_is_fixed_and_reconciles_to_the_family():
    selection = json.loads((CAMPAIGN_DIR / "expansion-official-selection.json").read_text(encoding="utf-8"))
    selected_ids = [item["source_id"] for item in selection["records"]]
    baseline_ids = selection["preserved_baseline_source_ids"]

    assert selection["batch_id"] == "official-written-family-completion-316"
    assert selection["expected_record_count"] == 316
    assert selection["family_record_count"] == 320
    assert len(selected_ids) == len(set(selected_ids)) == 316
    assert len(baseline_ids) == 4
    assert selection["pilot_source_ids_repaired"] == ["SRC-OFF-0333A5B22A207D88"]
    assert not set(selected_ids).intersection(baseline_ids)
    assert len(set(selected_ids).union(baseline_ids)) == 320
    assert all(
        urlsplit(item["retrieval_url"]).netloc
        in {
            "api.github.com",
            "build.staratlas.com",
            "experience.staratlas.com",
            "staratlas.com",
            "support.staratlas.com",
        }
        for item in selection["records"]
    )
    assert {item["retrieval_url_basis"] for item in selection["records"]} <= {
        "PRIOR_FINAL_URL",
        "PRIOR_REQUESTED_URL",
    }


def test_official_completion_has_full_preserved_coverage_and_immutable_github_carriers():
    ledger_path = CAMPAIGN_DIR / "expansion-official-retrieval-ledger.jsonl"
    records = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line]

    assert len(records) == len({item["source_id"] for item in records}) == 316
    assert all(item["retrieval_batch_id"] == "official-written-family-completion-316" for item in records)
    assert all(item["body_path"] and item["provenance_path"] for item in records)
    assert all(item["identity_status"] in {"MATCH", "CONSISTENT"} for item in records)
    assert not any(item["manual_review_required"] for item in records)
    assert (CAMPAIGN_DIR / "expansion-official-manual-review-queue.jsonl").read_bytes() == b""

    github_records = [item for item in records if item["retrieval_tier"] == "IMMUTABLE_GIT_COMMIT_OR_BLOB"]
    assert len(github_records) == 9
    for item in github_records:
        provenance = json.loads((ROOT / item["provenance_path"]).read_text(encoding="utf-8"))
        assert provenance["request"]["retrieval_url_basis"] == "IMMUTABLE_GITHUB_README_BLOB"
        assert len(provenance["snapshot_timestamp_or_git_sha"]) == 40
