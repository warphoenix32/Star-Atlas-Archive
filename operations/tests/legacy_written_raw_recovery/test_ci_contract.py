import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).parents[3]
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
