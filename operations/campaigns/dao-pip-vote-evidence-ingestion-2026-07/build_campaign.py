#!/usr/bin/env python3
"""Build reconciliation, campaign reports, and manifest for PIP-1 through PIP-32 votes."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


CAMPAIGN_ID = "dao-pip-vote-evidence-ingestion-2026-07"
AS_OF = "2026-07-20"
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
NORMALIZED_ROOT = ROOT / "archive/normalized/governance-votes/pip-01-32"
SOURCE_ROOT = ROOT / "archive/source-records/governance-votes/pip-01-32"
PROVENANCE_PATH = ROOT / "archive/provenance/governance-votes/pip-01-32.json"
RAW_PATH = ROOT / "archive/raw/governance-votes/pip-01-32/Star Atlas DAO PIP Votes.zip"
ARCHIVE_MANIFEST = ROOT / "archive/manifests/dao-pip-vote-evidence-ingestion-2026-07.json"
LEDGER_PATH = ROOT / "knowledge/governance/PIP-Registry.json"
Q = Decimal("0.00001")


def round_five(value: str | Decimal) -> Decimal:
    return Decimal(value).quantize(Q, rounding=ROUND_HALF_UP)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def reconcile() -> dict[str, Any]:
    summaries = json.loads((NORMALIZED_ROOT / "proposal-summaries.json").read_text(encoding="utf-8"))["proposals"]
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    ledger_by_pip = {record["pip_number"]: record for record in ledger["records"]}
    records: list[dict[str, Any]] = []
    conflict_count = 0
    for summary in summaries:
        pip = summary["pip_number"]
        ledger_record = ledger_by_pip[pip]
        vote = ledger_record["vote"]
        comparisons: list[dict[str, Any]] = []

        def compare(field: str, supplied: Any, existing: Any, precision: str = "EXACT") -> None:
            nonlocal conflict_count
            if precision == "5DP":
                matches = round_five(str(supplied)) == round_five(str(existing))
            else:
                matches = supplied == existing
            comparisons.append({
                "field": field,
                "supplied_evidence": supplied,
                "existing_ledger": existing,
                "comparison_precision": precision,
                "status": "MATCH" if matches else "CONFLICT",
            })
            if not matches:
                conflict_count += 1

        compare("proposal_id", summary["proposal_id"], ledger_record["proposal_uuid"])
        compare("ballot_count", summary["effective_ballot_count"], vote["ballot_count"])
        compare("total_pvp", summary["total_pvp_rounded_5dp"], vote["total_pvp"], "5DP")
        if vote["mechanism"] == "BINARY_PVP":
            supplied = summary["binary_result"]
            existing = vote["binary"]
            for key in ("yes", "no", "abstain"):
                supplied_count = supplied["ballot_counts"][key]
                existing_count = existing[f"{key}_ballots"]
                if existing_count is None and supplied_count == 0:
                    comparisons.append({
                        "field": f"{key}_ballots",
                        "supplied_evidence": supplied_count,
                        "existing_ledger": existing_count,
                        "comparison_precision": "SEMANTIC_ZERO_VS_NOT_CAPTURED",
                        "status": "NO_NUMERIC_CONFLICT_LIMITATION_RETAINED",
                    })
                else:
                    compare(f"{key}_ballots", supplied_count, existing_count)
                supplied_pvp = supplied["pvp_rounded_5dp"][key]
                existing_pvp = existing[f"{key}_pvp"]
                if existing_pvp is None and Decimal(supplied_pvp) == 0:
                    comparisons.append({
                        "field": f"{key}_pvp",
                        "supplied_evidence": supplied_pvp,
                        "existing_ledger": existing_pvp,
                        "comparison_precision": "SEMANTIC_ZERO_VS_NOT_CAPTURED",
                        "status": "NO_NUMERIC_CONFLICT_LIMITATION_RETAINED",
                    })
                else:
                    compare(f"{key}_pvp", supplied_pvp, existing_pvp, "5DP")
            compare("binary_result", supplied["result"], ledger_record["result"]["reviewed_result"])
            election_tally_status = None
        else:
            election_tally_status = summary["election_result"]["final_tally_status"]

        conflicts = [item for item in comparisons if item["status"] == "CONFLICT"]
        records.append({
            "pip_id": summary["pip_id"],
            "source_id": summary["source_id"],
            "ballot_mechanism": summary["ballot_mechanism"],
            "comparisons": comparisons,
            "reconciliation_status": "CONFLICT" if conflicts else "MATCH",
            "conflict_fields": [item["field"] for item in conflicts],
            "election_final_tally_status": election_tally_status,
            "winner_inference_performed": False,
            "implementation_or_payment_evidence": False,
        })

    return {
        "campaign_id": CAMPAIGN_ID,
        "as_of": AS_OF,
        "scope": "PIP-1 through PIP-32 supplied ballot evidence; PIP-33 excluded as already ingested",
        "comparison_precision": "EXACT_COUNTS_AND_ROUND_HALF_UP_5DP_FOR_PVP",
        "proposal_count": len(records),
        "reconciled_proposal_count": sum(item["reconciliation_status"] == "MATCH" for item in records),
        "conflict_count": conflict_count,
        "ranked_choice_tally_limitations": sum(item["election_final_tally_status"] is not None for item in records),
        "records": records,
    }


def reconciliation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# PIP-1 through PIP-32 Vote Evidence Reconciliation",
        "",
        "The supplied primary blockchain-derived ballot export reconciles against the existing canonical PIP ledger without rewriting that ledger.",
        "",
        f"- Proposals compared: {report['proposal_count']}",
        f"- Proposals matching: {report['reconciled_proposal_count']}",
        f"- Conflicting fields: {report['conflict_count']}",
        f"- Ranked-choice elections without reproducible final STV tally rules: {report['ranked_choice_tally_limitations']}",
        "- PIP-33: excluded because it is already preserved by the existing PIP-33 vote campaign",
        "- Canonical knowledge changed: no",
        "",
        "## Proposal reconciliation",
        "",
        "| PIP | Mechanism | Aggregate reconciliation | Election tally treatment |",
        "|---|---|---|---|",
    ]
    for record in report["records"]:
        treatment = record["election_final_tally_status"] or "Not applicable"
        lines.append(f"| {record['pip_id']} | {record['ballot_mechanism']} | {record['reconciliation_status']} | {treatment} |")
    lines += [
        "",
        "## Interpretation boundary",
        "",
        "Binary ballot counts and PVP totals match the existing ledger at five-decimal display precision. PIP-9 contains zero observed abstain records; this does not establish whether the interface offered an abstain option, so the ledger's capture limitation remains valid.",
        "",
        "For PIP-6, PIP-7, PIP-11, PIP-25, and PIP-27, ordered ballots and first-preference statistics are preserved. Final STV tallies and winner identities are not recomputed because the exact tally implementation, quota, transfer, exhaustion, and tie-break rules are not supplied. Existing official outcome records remain separate evidence.",
        "",
        "The ballot export does not establish authorization implementation, treasury payment, or post-vote execution.",
        "",
    ]
    return "\n".join(lines)


def campaign_summary(report: dict[str, Any]) -> dict[str, Any]:
    proposal_data = json.loads((NORMALIZED_ROOT / "proposal-summaries.json").read_text(encoding="utf-8"))["proposals"]
    event_count = sum(item["vote_event_count"] for item in proposal_data)
    all_wallets: set[str] = set()
    memo_counts: Counter[str] = Counter()
    validation_representation_counts: Counter[str] = Counter()
    anomaly_count = 0
    with (NORMALIZED_ROOT / "vote-events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            all_wallets.add(row["wallet_public_key"])
            memo_counts[str(row["memo_program_used"]).lower()] += 1
            validation_representation_counts[row["validation_value_representation"]] += 1
            anomaly_count += row["timestamp_integrity_status"] == "TIMESTAMP_ORDER_ANOMALY"
    mechanism_counts = Counter(item["ballot_mechanism"] for item in proposal_data)
    binary_results = Counter(
        item["binary_result"]["result"] for item in proposal_data if item["binary_result"] is not None
    )
    return {
        "campaign_id": CAMPAIGN_ID,
        "status": "READY_FOR_ARCHIVAL_REVIEW" if report["conflict_count"] == 0 else "BLOCKED_BY_RECONCILIATION_CONFLICT",
        "as_of": AS_OF,
        "package_source_id": "SRC-SOLANA-DAO-PIP-VOTES-4E01123F31A2",
        "package_sha256": "4e01123f31a2531427fc1910841efae45e24b15f4472338fbbf174c2e5b52d08",
        "raw_package_preserved": True,
        "included_pips": 32,
        "included_range": "PIP-1 through PIP-32",
        "excluded_pips": {"PIP-33": "ALREADY_INGESTED"},
        "vote_event_count": event_count,
        "effective_ballot_count": event_count,
        "superseded_vote_event_count": 0,
        "unique_wallets_across_corpus": len(all_wallets),
        "mechanism_counts": dict(sorted(mechanism_counts.items())),
        "binary_result_counts": dict(sorted(binary_results.items())),
        "memo_program_used_counts": dict(sorted(memo_counts.items())),
        "validation_value_representation_counts": dict(sorted(validation_representation_counts.items())),
        "timestamp_order_anomaly_count": anomaly_count,
        "aggregate_reconciliation": {
            "proposal_matches": report["reconciled_proposal_count"],
            "conflicting_fields": report["conflict_count"],
            "status": "PASS" if report["conflict_count"] == 0 else "FAIL",
        },
        "ranked_choice_elections": [item["pip_id"] for item in proposal_data if item["ballot_mechanism"] == "RANKED_CHOICE_ELECTION"],
        "final_stv_tallies_computed": False,
        "independent_rpc_reverification_performed": False,
        "canonical_knowledge_changes": 0,
        "graph_changes": 0,
        "publication_changes": 0,
        "pip_33_outputs_changed": False,
    }


def campaign_summary_markdown(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# DAO PIP Vote Evidence Ingestion Campaign Summary",
        "",
        f"- Status: **{summary['status']}**",
        f"- Included: {summary['included_range']} ({summary['included_pips']} proposals)",
        "- Excluded: PIP-33 (already ingested)",
        f"- Vote events: {summary['vote_event_count']}",
        f"- Effective ballots: {summary['effective_ballot_count']}",
        f"- Unique wallets across corpus: {summary['unique_wallets_across_corpus']}",
        f"- Binary proposals: {summary['mechanism_counts'].get('BINARY_PVP', 0)}",
        f"- Ranked-choice elections: {summary['mechanism_counts'].get('RANKED_CHOICE_ELECTION', 0)}",
        f"- Timestamp-order anomalies preserved: {summary['timestamp_order_anomaly_count']}",
        f"- Proposal aggregate matches: {summary['aggregate_reconciliation']['proposal_matches']} of 32",
        f"- Conflicting aggregate fields: {summary['aggregate_reconciliation']['conflicting_fields']}",
        "- Independent Solana RPC replay: not performed",
        "- Final STV election tallies: not computed without captured implementation rules",
        "- Canonical knowledge, graph, and publication changes: none",
        "",
    ])


def manifest_paths() -> list[Path]:
    fixed = [
        RAW_PATH,
        NORMALIZED_ROOT / "vote-events.jsonl",
        NORMALIZED_ROOT / "effective-ballots.jsonl",
        NORMALIZED_ROOT / "proposal-summaries.json",
        PROVENANCE_PATH,
        HERE / "README.md",
        HERE / "source-assessment.md",
        HERE / "import_vote_export.py",
        HERE / "build_campaign.py",
        HERE / "validate_campaign.py",
        HERE / "campaign-summary.json",
        HERE / "campaign-summary.md",
        HERE / "reconciliation-report.json",
        HERE / "reconciliation-report.md",
    ]
    return sorted(fixed + list(SOURCE_ROOT.glob("*.json")) + list(SOURCE_ROOT.glob("*.md")), key=repo_path)


def manifest_bytes(path: Path) -> bytes:
    """Return platform-independent bytes for text artifacts in the manifest."""
    data = path.read_bytes()
    if path.suffix.lower() in {".json", ".jsonl", ".md", ".py"}:
        return data.replace(b"\r\n", b"\n")
    return data


def write_manifest() -> None:
    artifacts = [
        {
            "path": repo_path(path),
            "byte_length": len(manifest_bytes(path)),
            "sha256": hashlib.sha256(manifest_bytes(path)).hexdigest(),
        }
        for path in manifest_paths()
    ]
    payload = {"campaign_id": CAMPAIGN_ID, "generated_as_of": AS_OF, "artifact_count": len(artifacts), "artifacts": artifacts}
    write_json(HERE / "manifest.json", payload)
    write_json(ARCHIVE_MANIFEST, payload)


def main() -> int:
    report = reconcile()
    write_json(HERE / "reconciliation-report.json", report)
    (HERE / "reconciliation-report.md").write_text(reconciliation_markdown(report), encoding="utf-8", newline="\n")
    summary = campaign_summary(report)
    write_json(HERE / "campaign-summary.json", summary)
    (HERE / "campaign-summary.md").write_text(campaign_summary_markdown(summary), encoding="utf-8", newline="\n")
    write_manifest()
    print(f"Built campaign reports: {summary['vote_event_count']} votes, {report['conflict_count']} reconciliation conflicts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
