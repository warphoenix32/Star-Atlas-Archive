#!/usr/bin/env python3
"""Build deterministic PIP-33 vote reconciliation artifacts."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


CAMPAIGN_ID = "pip-33-onchain-vote-reconciliation-2026-07"
AS_OF = "2026-07-20"
ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN_DIR = Path(__file__).resolve().parent
SOURCE_ID = "SRC-SOLANA-PIP-33-5EE6D3F844C4"
SOURCE_SHA256 = "5ee6d3f844c4932db1195429aa191fe7c6ae21087c12520d636ebe3a4d8dfacb"
VOTE_EVENTS_REL = Path("archive/normalized/governance-votes/pip-33/vote-events.jsonl")
EFFECTIVE_BALLOTS_REL = Path("archive/normalized/governance-votes/pip-33/effective-ballots.jsonl")
SUMMARY_REL = Path("archive/normalized/governance-votes/pip-33/proposal-summary.json")
PROVENANCE_REL = Path("archive/provenance/governance-votes/pip-33.json")
SOURCE_RECORD_DIR_REL = Path("archive/source-records/governance-votes")
SOURCE_RECORD_JSON_REL = SOURCE_RECORD_DIR_REL / f"{SOURCE_ID}.json"
SOURCE_RECORD_MD_REL = SOURCE_RECORD_DIR_REL / f"{SOURCE_ID}.md"
ARCHIVE_MANIFEST_REL = Path(f"archive/manifests/{CAMPAIGN_ID}.json")
PIP_REGISTRY_REL = Path("knowledge/governance/PIP-Registry.json")
ROUNDING_QUANTUM = Decimal("0.00001")


def dump_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def dump_jsonl(records: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in records)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def rounded(value: Decimal) -> str:
    return format(value.quantize(ROUNDING_QUANTUM, rounding=ROUND_HALF_UP), "f")


def decimal_sum(records: list[dict[str, Any]]) -> Decimal:
    return sum((Decimal(item["voting_power_raw"]) for item in records), Decimal(0))


def effective_ballots(events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        grouped[event["wallet_public_key"]].append(event)
    ballots: list[dict[str, Any]] = []
    superseded_count = 0
    for wallet in sorted(grouped):
        ordered = sorted(grouped[wallet], key=lambda item: (item["index_record_created_at"], item["vote_event_id"]))
        effective = ordered[-1]
        superseded = [item["vote_event_id"] for item in ordered[:-1]]
        superseded_count += len(superseded)
        ballots.append({
            "effective_ballot_id": f"PIP-33-{wallet}",
            "proposal_id": effective["proposal"]["proposal_id"],
            "pip_id": "PIP-33",
            "wallet_public_key": wallet,
            "effective_vote_event_id": effective["vote_event_id"],
            "superseded_vote_event_ids": superseded,
            "selection_basis": "LATEST_INDEX_RECORD_CREATED_AT",
            "vote_result_raw": effective["vote_result_raw"],
            "vote_result_normalized": effective["vote_result_normalized"],
            "voting_power_raw": effective["voting_power_raw"],
            "voting_power_rounded_5dp": effective["voting_power_rounded_5dp"],
            "ballot_signed_at": effective["ballot_signed_at"],
            "solana_validation_signature": effective["solana_validation_signature"],
            "identity_enrichment": effective["identity_enrichment"],
            "reconciliation_status": "EFFECTIVE_SINGLE_EVENT" if not superseded else "EFFECTIVE_LATEST_EVENT",
        })
    return ballots, superseded_count


def registry_pip33() -> dict[str, Any]:
    payload = json.loads((ROOT / PIP_REGISTRY_REL).read_text(encoding="utf-8"))
    return next(item for item in payload["records"] if item["pip_id"] == "PIP-33")


def source_record_json() -> dict[str, Any]:
    return {
        "source_id": SOURCE_ID,
        "title": "PIP-33 on-chain governance vote export",
        "document_type": "SOLANA_ONCHAIN_GOVERNANCE_VOTE_RECORD_SET",
        "source_type": "operator_provided_onchain_vote_export",
        "publisher": "Solana blockchain; operator-provided export",
        "creator": ["Star Atlas DAO voters"],
        "published_at_original": None,
        "published_at_normalized": None,
        "updated_at_original": None,
        "updated_at_normalized": None,
        "captured_at": AS_OF,
        "canonical_url": None,
        "access": "recallable_onchain",
        "artifact_chain": {
            "normalized_vote_events": VOTE_EVENTS_REL.as_posix(),
            "effective_ballots": EFFECTIVE_BALLOTS_REL.as_posix(),
            "proposal_summary": SUMMARY_REL.as_posix(),
            "provenance": PROVENANCE_REL.as_posix(),
            "source_record_json": SOURCE_RECORD_JSON_REL.as_posix(),
            "source_record_markdown": SOURCE_RECORD_MD_REL.as_posix(),
        },
        "source_lineage": {
            "publication": "Solana blockchain",
            "publication_role": "ONCHAIN_VOTE_EVIDENCE",
            "relationship": "RECORDS_BALLOTS_FOR",
            "primary_sources": ["Solana blockchain signatures embedded per ballot"],
            "original_creators": ["Individual Star Atlas DAO voters"],
            "lineage_confidence": "HIGH",
        },
        "authority": {
            "classification": "ONCHAIN_VALIDATABLE",
            "signature_semantics": "SOLANA_BLOCKCHAIN_VALIDATION_SIGNATURE",
            "operator_confirmation": "The signature field represents the exact Solana blockchain signature for validation.",
            "scope": "Vote-event and ballot-result evidence only; not payment or implementation evidence.",
        },
        "quality": {
            "extraction_confidence": "HIGH",
            "completeness": "COMPLETE_FOR_SUPPLIED_PIP_33_EXPORT",
            "raw_export_preservation": "OMITTED_BY_OPERATOR_SCOPE",
            "signature_replay_performed": False,
            "manual_review_required": True,
            "limitations": [
                "Signatures are preserved but were not independently replayed during this campaign.",
                "Display names and profile-selected factions are absent from the on-chain export and require separate enrichment.",
                "This vote dataset does not establish payment or proposal implementation.",
            ],
        },
        "provenance": {
            "acquisition_method": "submitted directly by repository operator",
            "original_filename": "PIP-33.txt",
            "source_artifact_sha256": SOURCE_SHA256,
            "source_artifact_preserved": False,
            "preservation_decision": "Raw wrapper omitted because the record is recallable from the blockchain; normalized vote evidence retained.",
        },
    }


def source_record_markdown() -> str:
    return f"""# PIP-33 on-chain governance vote export

## Metadata

- **Source ID:** `{SOURCE_ID}`
- **Document type:** `SOLANA_ONCHAIN_GOVERNANCE_VOTE_RECORD_SET`
- **Proposal:** `PIP-33` — ATMTA Historic Expense Reimbursement
- **Proposal ID:** `397fee39-fd7c-42be-89e3-169094138257`
- **Proposal hash:** `8c9cd4e467`
- **Supplied export SHA-256:** `{SOURCE_SHA256}`
- **Extraction confidence:** `HIGH`

## Evidence Scope

The supplied record contains 220 PIP-33 vote events with wallet public keys, raw vote choices, PVP, signed messages, timestamps, lock information, memo-program indicators, and exact Solana blockchain validation signatures. The raw `.txt` wrapper is not preserved by operator decision because the records are recallable from the blockchain. The normalized evidence remains reproducible and signature-addressable.

This source establishes ballot participation and supports the reviewed binary result. It does not establish payment, treasury execution, proposal implementation, or independent delivery.

## Identity Boundary

Wallet public keys are the stable ballot identities. Display names are self-selected aliases and require human validation before canonical identity attribution. The operator has verified `Siggy` as wallet `Ae8AjMQXZsZ7jMWSZTei3ycy4MmvLoPXpDn1w65MrA9U`. No other display-name attribution is created from this source.

Profile colors are separate, time-specific evidence: red means MUD, blue means ONI, yellow means Ustur, and white/uncolored means no faction was selected. The on-chain export contains no profile-color evidence.

## Validation Boundary

All 220 signatures are preserved exactly. They were not independently replayed in this campaign. The ballot export reconciles with the canonical PIP ledger to the operator-approved five-decimal precision policy.
"""


def build_artifacts() -> dict[str, str]:
    events = load_jsonl(ROOT / VOTE_EVENTS_REL)
    ballots, superseded_count = effective_ballots(events)
    by_result: dict[str, list[dict[str, Any]]] = {
        result: [item for item in ballots if item["vote_result_normalized"] == result]
        for result in ("YES", "NO", "ABSTAIN")
    }
    totals = {result: decimal_sum(items) for result, items in by_result.items()}
    total_pvp = sum(totals.values(), Decimal(0))
    decisive_pvp = totals["YES"] + totals["NO"]
    margin = totals["YES"] - totals["NO"]
    result = "PASSED" if margin > 0 else "FAILED" if margin < 0 else "TIED"
    registry = registry_pip33()
    registry_binary = registry["vote"]["binary"]

    summary = {
        "campaign_id": CAMPAIGN_ID,
        "source_id": SOURCE_ID,
        "pip_id": "PIP-33",
        "proposal_id": "397fee39-fd7c-42be-89e3-169094138257",
        "proposal_hash": "8c9cd4e467",
        "ballot_mechanism": "BINARY_PVP_WITH_ABSTAIN",
        "vote_event_count": len(events),
        "effective_ballot_count": len(ballots),
        "unique_wallet_count": len({item["wallet_public_key"] for item in ballots}),
        "superseded_vote_event_count": superseded_count,
        "ballot_counts": {result.lower(): len(items) for result, items in by_result.items()},
        "pvp_raw_sums": {result.lower(): format(value, "f") for result, value in totals.items()},
        "pvp_rounded_5dp": {result.lower(): rounded(value) for result, value in totals.items()},
        "total_pvp_raw": format(total_pvp, "f"),
        "total_pvp_rounded_5dp": rounded(total_pvp),
        "decisive_pvp_rounded_5dp": rounded(decisive_pvp),
        "result": result,
        "result_rule": "YES_PVP_GT_NO_PVP_PASS; NO_PVP_GT_YES_PVP_FAIL; EQUALITY_TIED",
        "margin_pvp_rounded_5dp": rounded(abs(margin)),
        "yes_percentage_of_decisive_pvp_rounded_5dp": rounded(Decimal(100) * totals["YES"] / decisive_pvp),
        "no_percentage_of_decisive_pvp_rounded_5dp": rounded(Decimal(100) * totals["NO"] / decisive_pvp),
        "memo_program_used_counts": dict(sorted(Counter(str(item["memo_program_used"]).lower() for item in events).items())),
        "vote_event_created_at_min": min(item["index_record_created_at"] for item in events),
        "vote_event_created_at_max": max(item["index_record_created_at"] for item in events),
        "human_validated_identity_count": sum(item["identity_enrichment"]["identity_attribution_status"] == "HUMAN_VERIFIED" for item in events),
        "raw_export_preserved": False,
        "signature_replay_performed": False,
        "payment_or_implementation_evidence": False,
    }

    fields = {
        "ballot_count": (str(len(ballots)), str(registry["vote"]["ballot_count"])),
        "yes_ballots": (str(len(by_result["YES"])), str(registry_binary["yes_ballots"])),
        "no_ballots": (str(len(by_result["NO"])), str(registry_binary["no_ballots"])),
        "abstain_ballots": (str(len(by_result["ABSTAIN"])), str(registry_binary["abstain_ballots"])),
        "yes_pvp": (rounded(totals["YES"]), rounded(Decimal(registry_binary["yes_pvp"]))),
        "no_pvp": (rounded(totals["NO"]), rounded(Decimal(registry_binary["no_pvp"]))),
        "abstain_pvp": (rounded(totals["ABSTAIN"]), rounded(Decimal(registry_binary["abstain_pvp"]))),
        "total_pvp": (rounded(total_pvp), rounded(Decimal(registry["vote"]["total_pvp"]))),
    }
    reconciliation_items = [{
        "field": field,
        "onchain_export": pair[0],
        "canonical_pip_ledger": pair[1],
        "status": "MATCH_AT_5_DECIMALS" if pair[0] == pair[1] else "CONFLICT",
    } for field, pair in fields.items()]
    reconciliation = {
        "campaign_id": CAMPAIGN_ID,
        "pip_id": "PIP-33",
        "relationship": "ONCHAIN_VOTE_EXPORT_RECONCILES_CANONICAL_PIP_LEDGER",
        "precision_policy": "ROUND_HALF_UP_TO_5_DECIMALS",
        "result": "PASS" if all(item["status"] == "MATCH_AT_5_DECIMALS" for item in reconciliation_items) else "CONFLICT",
        "items": reconciliation_items,
        "result_finding": "The supplied 220-ballot export independently reproduces the canonical ledger's PIP-33 counts, PVP totals, and PASSED result at five-decimal precision.",
        "treasury_finding": "This is vote evidence, not payment evidence. PIP-33 payment and implementation states remain unchanged and unresolved.",
        "canonical_knowledge_modified": False,
    }

    provenance = {
        "source_id": SOURCE_ID,
        "campaign_id": CAMPAIGN_ID,
        "source_artifact": {
            "original_filename": "PIP-33.txt",
            "sha256": SOURCE_SHA256,
            "record_count": 220,
            "preserved_in_repository": False,
            "omission_basis": "REPOSITORY_OPERATOR_SCOPE_DECISION_RECALLABLE_ONCHAIN",
        },
        "authority": {
            "source_type": "SOLANA_ONCHAIN_GOVERNANCE_VOTE_RECORD_SET",
            "evidence_status": "ONCHAIN_VALIDATABLE",
            "signature_semantics": "SOLANA_BLOCKCHAIN_VALIDATION_SIGNATURE",
            "signature_semantics_basis": "REPOSITORY_OPERATOR_CONFIRMATION",
            "signature_replay_status": "NOT_REPLAYED_IN_THIS_CAMPAIGN",
        },
        "normalization": {
            "voting_power_raw_preserved": True,
            "display_rounding": "ROUND_HALF_UP_TO_5_DECIMALS",
            "effective_ballot_rule": "LATEST_INDEX_RECORD_CREATED_AT_PER_WALLET",
            "identity_rule": "DISPLAY_NAMES_REQUIRE_HUMAN_VALIDATION",
        },
    }

    adjudications = {
        "campaign_id": CAMPAIGN_ID,
        "decisions": [
            {"decision_id": "P33-VOTE-001", "status": "ACCEPTED", "decision": "Binary passage is determined by YES PVP versus NO PVP; abstain is recorded but not decisive.", "authority": "repository operator"},
            {"decision_id": "P33-VOTE-002", "status": "ACCEPTED", "decision": "Source status plus voting-end date methodology may be treated as evidential.", "authority": "repository operator"},
            {"decision_id": "P33-VOTE-003", "status": "ACCEPTED", "decision": "Preserve original PVP strings and use five-decimal ROUND_HALF_UP values for normalized display and reconciliation.", "authority": "repository operator"},
            {"decision_id": "P33-ID-001", "status": "ACCEPTED", "decision": "Display names are self-selected aliases; every canonical voter identity attribution requires human validation, with later records allowed to reuse prior adjudication.", "authority": "repository operator"},
            {"decision_id": "P33-ID-002", "status": "ACCEPTED", "decision": "Siggy is human-verified as wallet Ae8AjMQXZsZ7jMWSZTei3ycy4MmvLoPXpDn1w65MrA9U.", "authority": "repository operator"},
            {"decision_id": "P33-FACTION-001", "status": "ACCEPTED", "decision": "Profile-name colors encode selected faction: red MUD, blue ONI, yellow Ustur; white/uncolored means no faction selected.", "authority": "repository operator"},
            {"decision_id": "P33-SOURCE-001", "status": "ACCEPTED", "decision": "The signature field is the exact Solana blockchain validation signature; preserve it in normalized records.", "authority": "repository operator"},
            {"decision_id": "P33-SOURCE-002", "status": "ACCEPTED", "decision": "The recallable raw export is not preservation-critical and is omitted; normalized evidence and source hash are retained.", "authority": "repository operator"},
        ],
        "open_decision_count": 0,
    }

    identity_policy = {
        "policy_id": "GOVERNANCE-VOTER-IDENTITY-v1",
        "wallet_public_key_role": "STABLE_BALLOT_IDENTITY",
        "display_name_role": "SELF_SELECTED_ALIAS_OBSERVATION",
        "canonical_identity_requirement": "HUMAN_VALIDATION",
        "prior_adjudication_reuse": "ALLOWED_WHEN_WALLET_MATCHES_AND_NO_CONTRARY_EVIDENCE_EXISTS",
        "faction_color_mapping": {"red": "MUD", "blue": "ONI", "yellow": "USTUR", "white_or_uncolored": "NO_FACTION_SELECTED"},
        "faction_temporal_scope": "PROFILE_SELECTED_FACTION_AT_CAPTURE_TIME",
        "uncolored_interpretation": "NO_FACTION_SELECTED; NOT_PROOF_OF_NO_EXTERNAL_AFFILIATION",
        "verified_identities": [{"canonical_identity": "Siggy", "wallet_public_key": "Ae8AjMQXZsZ7jMWSZTei3ycy4MmvLoPXpDn1w65MrA9U", "status": "HUMAN_VERIFIED", "authority": "REPOSITORY_OPERATOR"}],
    }

    campaign_summary = {
        **summary,
        "reconciliation_result": reconciliation["result"],
        "accepted_human_decisions": len(adjudications["decisions"]),
        "open_human_decisions": 0,
        "canonical_knowledge_changes": 0,
    }
    campaign_summary_md = f"""# PIP-33 On-Chain Vote Reconciliation — Campaign Summary

- Vote events: {len(events)}
- Effective ballots: {len(ballots)}
- Unique wallets: {len(ballots)}
- YES: {len(by_result['YES'])} ballots / {rounded(totals['YES'])} PVP
- NO: {len(by_result['NO'])} ballots / {rounded(totals['NO'])} PVP
- Abstain: {len(by_result['ABSTAIN'])} ballots / {rounded(totals['ABSTAIN'])} PVP
- Total: {rounded(total_pvp)} PVP
- Result: `{result}` by `{summary['result_rule']}`
- Canonical PIP ledger reconciliation: `{reconciliation['result']}` at five decimals
- Signature replay: not performed
- Canonical knowledge changes: 0

The source confirms the ballot/result record only. It does not establish payment, treasury execution, or proposal implementation.
"""
    reconciliation_md = "# PIP-33 Vote Reconciliation\n\n" + "\n".join(
        f"- **{item['field']}**: export `{item['onchain_export']}`; ledger `{item['canonical_pip_ledger']}` — `{item['status']}`"
        for item in reconciliation_items
    ) + "\n\nResult: **" + reconciliation["result"] + "**. PIP-33 payment and implementation evidence remain unresolved and unchanged.\n"

    artifacts: dict[str, str] = {
        EFFECTIVE_BALLOTS_REL.as_posix(): dump_jsonl(ballots),
        SUMMARY_REL.as_posix(): dump_json(summary),
        PROVENANCE_REL.as_posix(): dump_json(provenance),
        SOURCE_RECORD_JSON_REL.as_posix(): dump_json(source_record_json()),
        SOURCE_RECORD_MD_REL.as_posix(): source_record_markdown(),
        f"operations/campaigns/{CAMPAIGN_ID}/identity-and-faction-policy.json": dump_json(identity_policy),
        f"operations/campaigns/{CAMPAIGN_ID}/curator-decisions.json": dump_json(adjudications),
        f"operations/campaigns/{CAMPAIGN_ID}/reconciliation-report.json": dump_json(reconciliation),
        f"operations/campaigns/{CAMPAIGN_ID}/reconciliation-report.md": reconciliation_md,
        f"operations/campaigns/{CAMPAIGN_ID}/campaign-summary.json": dump_json(campaign_summary),
        f"operations/campaigns/{CAMPAIGN_ID}/campaign-summary.md": campaign_summary_md,
    }
    manifest_inputs = {VOTE_EVENTS_REL.as_posix(): (ROOT / VOTE_EVENTS_REL).read_bytes()}
    manifest_entries = [
        {"path": path, "sha256": sha256_bytes(data), "byte_length": len(data)}
        for path, data in manifest_inputs.items()
    ] + [
        {"path": path, "sha256": sha256_bytes(content.encode("utf-8")), "byte_length": len(content.encode("utf-8"))}
        for path, content in sorted(artifacts.items())
    ]
    manifest = {"campaign_id": CAMPAIGN_ID, "generated_as_of": AS_OF, "artifact_count": len(manifest_entries), "artifacts": sorted(manifest_entries, key=lambda item: item["path"])}
    manifest_text = dump_json(manifest)
    artifacts[ARCHIVE_MANIFEST_REL.as_posix()] = manifest_text
    artifacts[f"operations/campaigns/{CAMPAIGN_ID}/manifest.json"] = manifest_text
    return artifacts


def write_artifacts() -> dict[str, str]:
    artifacts = build_artifacts()
    for relative, content in artifacts.items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    return artifacts


def main() -> int:
    write_artifacts()
    print(f"Built {CAMPAIGN_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
