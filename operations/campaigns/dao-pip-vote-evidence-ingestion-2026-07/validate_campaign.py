#!/usr/bin/env python3
"""Validate the PIP-1 through PIP-32 vote evidence campaign."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


CAMPAIGN_ID = "dao-pip-vote-evidence-ingestion-2026-07"
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RAW_PATH = ROOT / "archive/raw/governance-votes/pip-01-32/Star Atlas DAO PIP Votes.zip"
NORMALIZED_ROOT = ROOT / "archive/normalized/governance-votes/pip-01-32"
SOURCE_ROOT = ROOT / "archive/source-records/governance-votes/pip-01-32"
PROVENANCE_PATH = ROOT / "archive/provenance/governance-votes/pip-01-32.json"
ARCHIVE_MANIFEST = ROOT / "archive/manifests/dao-pip-vote-evidence-ingestion-2026-07.json"
EXPECTED_PACKAGE_SHA256 = "4e01123f31a2531427fc1910841efae45e24b15f4472338fbbf174c2e5b52d08"
EXPECTED_ELECTION_PIPS = {"PIP-06", "PIP-07", "PIP-11", "PIP-25", "PIP-27"}
ALLOWED_PREFIXES = (
    "archive/raw/governance-votes/pip-01-32/",
    "archive/normalized/governance-votes/pip-01-32/",
    "archive/provenance/governance-votes/pip-01-32.json",
    "archive/source-records/governance-votes/pip-01-32/",
    "archive/manifests/dao-pip-vote-evidence-ingestion-2026-07.json",
    f"operations/campaigns/{CAMPAIGN_ID}/",
    "operations/tests/dao_pip_governance_votes/",
    "operations/ci/validate_repository.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def validate() -> tuple[dict[str, Any], list[str]]:
    checks: dict[str, Any] = {}
    failures: list[str] = []

    def check(name: str, passed: bool, detail: Any = None) -> None:
        checks[name] = {"passed": passed, "detail": detail}
        if not passed:
            failures.append(f"{name}: {detail}")

    required_json = [
        NORMALIZED_ROOT / "proposal-summaries.json",
        PROVENANCE_PATH,
        HERE / "campaign-summary.json",
        HERE / "reconciliation-report.json",
        HERE / "manifest.json",
        ARCHIVE_MANIFEST,
        *SOURCE_ROOT.glob("*.json"),
    ]
    parse_errors = []
    for path in required_json:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            parse_errors.append(f"{path.relative_to(ROOT).as_posix()}: {exc}")
    check("json_parse", not parse_errors, parse_errors)

    events = read_jsonl(NORMALIZED_ROOT / "vote-events.jsonl")
    effective = read_jsonl(NORMALIZED_ROOT / "effective-ballots.jsonl")
    check("vote_event_count", len(events) == 8404, len(events))
    check("effective_ballot_count", len(effective) == 8404, len(effective))
    check("unique_vote_event_ids", len({row["vote_event_id"] for row in events}) == 8404)
    check("unique_validation_values", len({row["solana_validation_value"] for row in events}) == 8404)
    check("unique_pip_wallet_pairs", len({(row["proposal"]["pip_id"], row["wallet_public_key"]) for row in events}) == 8404)
    check("effective_event_references", {row["effective_vote_event_id"] for row in effective} == {row["vote_event_id"] for row in events})
    check("pip_scope", {row["proposal"]["pip_id"] for row in events} == {f"PIP-{number:02d}" for number in range(1, 33)})
    check("pip_33_excluded", not any(row["proposal"]["pip_id"] == "PIP-33" for row in events))

    summaries = json.loads((NORMALIZED_ROOT / "proposal-summaries.json").read_text(encoding="utf-8"))["proposals"]
    check("proposal_summary_count", len(summaries) == 32, len(summaries))
    check("mechanism_partition", Counter(item["ballot_mechanism"] for item in summaries) == Counter({"BINARY_PVP": 27, "RANKED_CHOICE_ELECTION": 5}))
    election_pips = {item["pip_id"] for item in summaries if item["ballot_mechanism"] == "RANKED_CHOICE_ELECTION"}
    check("election_pips", election_pips == EXPECTED_ELECTION_PIPS, sorted(election_pips))
    check("election_winners_not_inferred", all(
        item["election_result"]["winner_inference_performed"] is False
        and item["election_result"]["final_tally_status"] == "NOT_COMPUTED_STV_IMPLEMENTATION_RULES_NOT_CAPTURED"
        for item in summaries if item["ballot_mechanism"] == "RANKED_CHOICE_ELECTION"
    ))
    check("binary_result_rule_attributed", all(
        item["binary_result"]["result_rule_is_source_native"] is False
        for item in summaries if item["ballot_mechanism"] == "BINARY_PVP"
    ))

    anomalies = [row for row in events if row["timestamp_integrity_status"] == "TIMESTAMP_ORDER_ANOMALY"]
    check("timestamp_anomalies_preserved", len(anomalies) == 278, len(anomalies))
    check("timestamp_anomaly_values_negative", all(float(row["portal_minus_signed_seconds"]) < 0 for row in anomalies))
    check("both_timestamps_preserved", all(row["signed_message_timestamp"] and row["portal_record_created_at"] for row in events))

    representation_counts = Counter(row["validation_value_representation"] for row in events)
    check("validation_representation_counts", representation_counts == Counter({
        "BASE64_ED25519_DETACHED_SIGNATURE_BYTES": 5977,
        "BASE64_SERIALIZED_TRANSACTION_LIKE_PAYLOAD": 2427,
    }), dict(representation_counts))
    check("rpc_reverification_not_inferred", all(row["independent_rpc_reverification_status"] == "NOT_PERFORMED" for row in events))
    check("identity_not_inferred", all(row["identity_enrichment"]["canonical_identity"] is None for row in events))

    json_records = sorted(SOURCE_ROOT.glob("*.json"))
    markdown_records = sorted(SOURCE_ROOT.glob("*.md"))
    check("source_record_pairs", len(json_records) == 32 and len(markdown_records) == 32, {"json": len(json_records), "markdown": len(markdown_records)})
    source_ids = [json.loads(path.read_text(encoding="utf-8"))["source_id"] for path in json_records]
    check("unique_source_ids", len(source_ids) == len(set(source_ids)) == 32)

    provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
    check("raw_package_preserved", RAW_PATH.exists() and sha256(RAW_PATH) == EXPECTED_PACKAGE_SHA256, sha256(RAW_PATH) if RAW_PATH.exists() else None)
    check("package_provenance", provenance["source_artifact"]["sha256"] == EXPECTED_PACKAGE_SHA256 and provenance["source_artifact"]["preserved_in_repository"] is True)
    check("pip_33_exclusion_documented", provenance["excluded_member"]["disposition"] == "EXCLUDED_ALREADY_INGESTED")

    reconciliation = json.loads((HERE / "reconciliation-report.json").read_text(encoding="utf-8"))
    check("ledger_aggregate_reconciliation", reconciliation["proposal_count"] == 32 and reconciliation["reconciled_proposal_count"] == 32 and reconciliation["conflict_count"] == 0)
    check("payment_and_implementation_not_inferred", all(record["implementation_or_payment_evidence"] is False for record in reconciliation["records"]))

    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    archive_manifest = json.loads(ARCHIVE_MANIFEST.read_text(encoding="utf-8"))
    check("manifest_copies_match", manifest == archive_manifest)
    manifest_errors = []
    for item in manifest["artifacts"]:
        path = ROOT / item["path"]
        if not path.exists() or path.stat().st_size != item["byte_length"] or sha256(path) != item["sha256"]:
            manifest_errors.append(item["path"])
    check("manifest_checksums", not manifest_errors, manifest_errors)
    check("manifest_count", manifest["artifact_count"] == len(manifest["artifacts"]), manifest["artifact_count"])

    diff_names = run("git", "diff", "--name-only", "origin/main").stdout.splitlines()
    unexpected_paths = [path for path in diff_names if not path.startswith(ALLOWED_PREFIXES)]
    check("allowed_paths_only", not unexpected_paths, unexpected_paths)
    protected_changes = [path for path in diff_names if path.startswith(("knowledge/", "graph/", "publication/", "archive/normalized/governance-votes/pip-33/"))]
    check("protected_layers_unchanged", not protected_changes, protected_changes)

    before = {item["path"]: item["sha256"] for item in manifest["artifacts"]}
    imported = run(sys.executable, str(HERE / "import_vote_export.py"), "--source", str(RAW_PATH))
    built = run(sys.executable, str(HERE / "build_campaign.py"))
    regenerated_manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    after = {item["path"]: item["sha256"] for item in regenerated_manifest["artifacts"]}
    check("deterministic_regeneration", imported.returncode == 0 and built.returncode == 0 and before == after, {
        "import_returncode": imported.returncode,
        "build_returncode": built.returncode,
        "import_stderr": imported.stderr,
        "build_stderr": built.stderr,
        "changed_artifacts": sorted(set(before) | set(after)) if before != after else [],
    })

    diff_check = run("git", "diff", "--check")
    check("git_diff_check", diff_check.returncode == 0, "" if diff_check.returncode == 0 else diff_check.stdout + diff_check.stderr)
    return checks, failures


def write_report(checks: dict[str, Any], failures: list[str]) -> None:
    payload = {
        "campaign_id": CAMPAIGN_ID,
        "status": "PASS" if not failures else "FAIL",
        "as_of": "2026-07-20",
        "checks": checks,
        "failures": failures,
        "warnings": [
            "Independent Solana RPC replay was not performed; the operator-confirmed source and exact validation payloads are preserved.",
            "The 278 timestamp-order anomalies are retained without choosing one timestamp as authoritative.",
            "Final STV tallies are not computed without the exact election implementation rules.",
            "Ballot evidence does not establish implementation, payment, or post-vote execution.",
        ],
    }
    (HERE / "validation-report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    lines = [
        "# DAO PIP Vote Evidence Validation Report",
        "",
        f"- Status: **{payload['status']}**",
        f"- Checks passed: {sum(item['passed'] for item in checks.values())} of {len(checks)}",
        f"- Failures: {len(failures)}",
        "",
        "## Warnings",
        "",
        *(f"- {warning}" for warning in payload["warnings"]),
        "",
    ]
    if failures:
        lines += ["## Failures", "", *(f"- {failure}" for failure in failures), ""]
    (HERE / "validation-report.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    checks, failures = validate()
    write_report(checks, failures)
    print(f"Validation {'PASS' if not failures else 'FAIL'}: {sum(item['passed'] for item in checks.values())}/{len(checks)} checks")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
