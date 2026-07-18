#!/usr/bin/env python3
"""Build the evidence-qualified PIP-1 through PIP-33 governance ledger."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
AS_OF = "2026-07-18"
LEDGER_JSON = ROOT / "knowledge/governance/PIP-Registry.json"
LEDGER_MD = ROOT / "knowledge/governance/PIP-Registry.md"
SEMANTIC_PATH = ROOT / "archive/semantic/governance/pip-registry-semantic.json"
RECONCILIATION_PATH = ROOT / "archive/semantic/governance/pip-source-reconciliation.json"
RELATIONSHIPS_PATH = ROOT / "archive/semantic/governance/pip-supersession-index.json"
ELECTION_OUTCOMES_PATH = ROOT / "archive/semantic/governance/pip-election-round-outcomes.json"
TRACKER_SEMANTIC_PATH = ROOT / "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"
RAW_ROOT = ROOT / "archive/raw/social-governance-semantic-enrichment/governance/pip-captures"
SOURCE_RECORD_ROOT = ROOT / "archive/source-records/social-governance-semantic-enrichment/governance"
TRACKER_RECORD_ROOT = ROOT / "archive/source-records/governance/council-pip-tracker"

TREASURY_STATES = {
    "REQUESTED",
    "AUTHORIZED",
    "COUNCIL_REPORTED",
    "UNVERIFIED",
    "MISSING_ONCHAIN_EVIDENCE",
}
SOLANA_SENTINEL_WALLET = "11111111111111111111111111111111"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def decimal_sum(values: list[str | None]) -> str:
    total = sum((Decimal(value) for value in values if value is not None), Decimal(0))
    return format(total, "f")


def meaningful_money(value: Any) -> bool:
    if value is None:
        return False
    text = str(value).strip().upper()
    return text not in {"", "?", "N/A", "NA", "NONE", "NULL"}


def source_lifecycle_flags(pip: dict[str, Any]) -> tuple[bool, bool, bool]:
    """Return mechanism/result states from source-backed semantic fields."""
    is_election = pip["vote_mechanism"] == "RANKED_CHOICE_ELECTION"
    is_failed = pip["reviewed_result"] == "FAILED"
    is_passed = pip["reviewed_result"] == "PASSED"
    return is_election, is_failed, is_passed


def proposal_partitions(proposals: list[dict[str, Any]]) -> tuple[list[int], list[int], list[int]]:
    elections: list[int] = []
    failed: list[int] = []
    passed_non_elections: list[int] = []
    for pip in proposals:
        is_election, is_failed, is_passed = source_lifecycle_flags(pip)
        if is_election:
            elections.append(pip["pip_number"])
        elif is_failed:
            failed.append(pip["pip_number"])
        elif is_passed:
            passed_non_elections.append(pip["pip_number"])
    return sorted(elections), sorted(failed), sorted(passed_non_elections)


def is_treasury_relevant(pip: dict[str, Any]) -> bool:
    is_election, _, _ = source_lifecycle_flags(pip)
    if is_election:
        return False
    funding_category = any(str(value).upper() == "FUNDING" for value in pip.get("proposal_category") or [])
    explicit_request = bool(pip.get("requested_funding"))
    return funding_category or explicit_request


def has_concrete_council_payment_report(pip: dict[str, Any]) -> bool:
    payment_fields = (pip.get("council_tracker") or {}).get("payment_fields") or {}
    return any(meaningful_money(payment_fields.get(key)) for key in ("paid_usdc", "paid_atlas"))


def treasury_verification_scope(proposals: list[dict[str, Any]]) -> list[int]:
    result: list[int] = []
    for pip in proposals:
        is_election, _, is_passed = source_lifecycle_flags(pip)
        if is_passed and not is_election and is_treasury_relevant(pip):
            if has_concrete_council_payment_report(pip) or pip["pip_number"] == 33:
                result.append(pip["pip_number"])
    return sorted(result)


def unresolved_election_scope(proposals: list[dict[str, Any]]) -> list[int]:
    return sorted(
        pip["pip_number"]
        for pip in proposals
        if source_lifecycle_flags(pip)[0] and not (pip.get("election_winners") or [])
    )


def placeholder_election_wallet_scope(proposals: list[dict[str, Any]]) -> list[int]:
    result: list[int] = []
    for pip in proposals:
        if not source_lifecycle_flags(pip)[0]:
            continue
        raw = read_json(raw_path_for(pip))
        if any(option.get("walletPublicKey") == SOLANA_SENTINEL_WALLET for option in raw.get("voteOptions") or []):
            result.append(pip["pip_number"])
    return sorted(result)


def categories(source_values: list[str]) -> list[str]:
    result: list[str] = []
    for value in source_values:
        normalized = value.strip().upper().replace(" ", "_")
        if normalized not in result:
            result.append(normalized)
    return result or ["UNKNOWN"]


def author_record(pip: dict[str, Any]) -> dict[str, Any]:
    public_key = pip.get("author_public_key")
    public_key_only = pip["pip_number"] in {6, 7, 11, 25}
    return {
        "display_name": None if public_key_only else pip.get("author"),
        "captured_value": pip.get("author"),
        "public_key": public_key,
        "identification_status": "PUBLIC_KEY_ONLY" if public_key_only else "IDENTIFIED",
    }


def raw_path_for(pip: dict[str, Any]) -> Path:
    expected = RAW_ROOT / f"pip-{pip['pip_number']:02d}-{pip['proposal_uuid']}.json"
    if not expected.exists():
        raise FileNotFoundError(expected)
    return expected


def source_record_path_for(pip: dict[str, Any]) -> Path:
    return SOURCE_RECORD_ROOT / f"{pip['source_id']}.json"


def tracker_path_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in TRACKER_RECORD_ROOT.glob("*.json"):
        data = read_json(path)
        source_id = data.get("source_id")
        if source_id:
            result[source_id] = repo_path(path)
    return result


def build_relationships() -> dict[int, list[dict[str, Any]]]:
    by_pip: dict[int, list[dict[str, Any]]] = defaultdict(list)
    relationships = read_json(RELATIONSHIPS_PATH)["relationships"]
    for item in relationships:
        record = {
            "relationship": item["relationship"],
            "from_pip": item["from_pip"],
            "to_pip": item["to_pip"],
            "evidence_source_id": item["source_id"],
            "evidence_path": repo_path(RELATIONSHIPS_PATH),
            "review_status": item["human_review_status"],
        }
        by_pip[item["from_pip"]].append(record)
        by_pip[item["to_pip"]].append(record)

    # These stage/dependency edges are explicit in the preserved election texts.
    explicit_edges = [
        (6, "ELECTION_FIRST_ROUND_UNDER", 3),
        (7, "FINAL_ROUND_OF", 6),
        (7, "ELECTION_FINAL_ROUND_UNDER", 3),
        (11, "COUNCIL_ELECTION_UNDER", 10),
        (25, "COUNCIL_ELECTION_UNDER", 10),
    ]
    for from_pip, relationship, to_pip in explicit_edges:
        source = next(RAW_ROOT.glob(f"pip-{from_pip:02d}-*.json"))
        record = {
            "relationship": relationship,
            "from_pip": from_pip,
            "to_pip": to_pip,
            "evidence_source_id": f"PIP-{from_pip:02d}-FULL-TEXT",
            "evidence_path": repo_path(source),
            "review_status": "REVIEWED_EXPLICIT_TEXT",
        }
        by_pip[from_pip].append(record)
        by_pip[to_pip].append(record)

    for values in by_pip.values():
        values.sort(key=lambda item: (item["from_pip"], item["to_pip"], item["relationship"]))
    return by_pip


def build_conflicts(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    election_pips, failed_pips, _ = proposal_partitions(proposals)
    proposal_numbers = sorted(pip["pip_number"] for pip in proposals)
    unresolved_election_pips = unresolved_election_scope(proposals)
    placeholder_wallet_pips = placeholder_election_wallet_scope(proposals)
    treasury_scope = treasury_verification_scope(proposals)

    conflicts.append({
        "conflict_id": "GOV-CONFLICT-PORTAL-STATUS-001",
        "pip_numbers": proposal_numbers,
        "field_path": "reconciliation.portal_current_status",
        "classification": "STALE_PORTAL_STATE",
        "severity": "MATERIAL",
        "finding": "Every captured portal object remains Proposal_Activated_Pending_Open_Voting after its recorded vote end.",
        "treatment": "Preserve the portal value as source metadata; derive no result or implementation state from it.",
        "status": "OPEN_DOCUMENTED",
        "required_artifacts": ["Timestamped official portal history or corrected proposal-state exports for PIP-1 through PIP-33."],
        "blocks_validation": False,
        "manual_review_required": True,
    })
    conflicts.append({
        "conflict_id": "GOV-CONFLICT-ELECTION-WALLET-PLACEHOLDERS-001",
        "pip_numbers": placeholder_wallet_pips,
        "field_path": "vote.election.candidates[].wallet_public_key",
        "classification": "PLACEHOLDER_WALLET_VALUE_IN_CAPTURE",
        "severity": "MATERIAL",
        "finding": "The portal captures repeat the Solana sentinel value 11111111111111111111111111111111 across candidate wallet fields; it is not treated as a candidate identity.",
        "treatment": "Preserve the captured value separately, set normalized wallet_public_key to null, and require an official candidate-to-wallet mapping.",
        "status": "OPEN_DOCUMENTED",
        "required_artifacts": ["Official candidate-to-wallet mapping for every captured placeholder candidate-wallet value."],
        "blocks_validation": False,
        "manual_review_required": True,
    })
    conflicts.append({
        "conflict_id": "GOV-CONFLICT-FAILED-MILESTONES-001",
        "pip_numbers": failed_pips,
        "field_path": "implementation.council_reported_state",
        "classification": "NO_AUTHORIZATION_VS_TRACKER_MILESTONES",
        "severity": "MATERIAL",
        "finding": "The Council tracker reports milestone completion for four failed proposals that supplied no authorization.",
        "treatment": "Preserve the attributed tracker value but set implementation.state and implementation.independent_verification_state to NOT_APPLICABLE_NO_AUTHORIZATION.",
        "status": "RESOLVED_BY_ADJUDICATION",
        "required_artifacts": ["Corrected Council tracker rows or Council-authored explanation for the milestone values."],
        "blocks_validation": False,
        "manual_review_required": True,
    })
    conflicts.append({
        "conflict_id": "GOV-CONFLICT-ELECTION-WINNERS-001",
        "pip_numbers": unresolved_election_pips,
        "field_path": "vote.election.official_outcome_names",
        "classification": "ELECTION_OUTCOME_MISSING",
        "severity": "MATERIAL",
        "finding": "Council-reported passage exists, but the preserved portal captures contain no electionResults winner list.",
        "treatment": "Retain aggregate ballots/PVP and unresolved winner identity; infer no officeholder or program winner.",
        "status": "OPEN_DOCUMENTED",
        "required_artifacts": ["Official final ranked-choice result export identifying winners and candidate-level totals for every unresolved election."],
        "blocks_validation": False,
        "manual_review_required": True,
    })
    conflicts.append({
        "conflict_id": "GOV-CONFLICT-ELECTION-CANDIDATE-PVP-001",
        "pip_numbers": election_pips,
        "field_path": "vote.election.candidates[].candidate_pvp",
        "classification": "CANDIDATE_TOTALS_MISSING",
        "severity": "MATERIAL",
        "finding": "The portal captures preserve only aggregate ranked-choice ballots and PVP, not candidate-level PVP.",
        "treatment": "List captured candidates and set every candidate PVP field to null with MISSING_FROM_CAPTURE status.",
        "status": "OPEN_DOCUMENTED",
        "required_artifacts": ["Official per-candidate ranked-choice result exports for all five election PIPs."],
        "blocks_validation": False,
        "manual_review_required": True,
    })
    conflicts.append({
        "conflict_id": "GOV-CONFLICT-PIP-027-BALLOT-CONFIG-001",
        "pip_numbers": [27],
        "field_path": "vote.election.max_choices",
        "classification": "PORTAL_BALLOT_CONFIGURATION_DISCREPANCY",
        "severity": "MATERIAL",
        "finding": "PIP-27 records five winners, six maximum choices, and thirteen candidates while the proposal text describes five winners.",
        "treatment": "Preserve all captured values and do not normalize the maximum-choice field.",
        "status": "OPEN_DOCUMENTED",
        "required_artifacts": ["Official PIP-27 ballot configuration and final STV tabulation export."],
        "blocks_validation": False,
        "manual_review_required": True,
    })
    conflicts.append({
        "conflict_id": "GOV-CONFLICT-PIP-033-FUNDING-SOURCE-001",
        "pip_numbers": [33],
        "field_path": "funding_scope",
        "classification": "DERIVED_SOURCE_MISCLASSIFICATION",
        "severity": "MATERIAL",
        "finding": "The semantic source labels PIP-33 as Ecosystem Fund, while the proposal identifies an extraordinary direct DAO Treasury measure and the Council tracker marks ecosystem_fund NO.",
        "treatment": "Use DIRECT_DAO_TREASURY_MEASURE and retain the semantic label as a rejected conflict.",
        "status": "RESOLVED_BY_ADJUDICATION",
        "required_artifacts": [],
        "blocks_validation": False,
        "manual_review_required": True,
    })
    conflicts.append({
        "conflict_id": "GOV-CONFLICT-PIP-033-RESULT-001",
        "pip_numbers": [33],
        "field_path": "result.council_reported_result",
        "classification": "TRACKER_RESULT_MISSING",
        "severity": "MATERIAL",
        "finding": "The Council tracker result is null, while completed portal PVP supports the repository-reviewed PASSED result.",
        "treatment": "Preserve the tracker null and use the explicitly labeled repository editorial vote adjudication.",
        "status": "OPEN_DOCUMENTED",
        "required_artifacts": ["Corrected Council tracker result or an official final result record linked to PIP-33."],
        "blocks_validation": False,
        "manual_review_required": True,
    })
    conflicts.append({
        "conflict_id": "GOV-CONFLICT-PIP-033-ARITHMETIC-001",
        "pip_numbers": [33],
        "field_path": "financial_terms.arithmetic_discrepancies",
        "classification": "SOURCE_ARITHMETIC_DISCREPANCY",
        "severity": "MATERIAL",
        "finding": "Two displayed tranches sum to $469,513.52 versus the stated $469,513.53 total; displayed USDC portions sum to $352,135.14 versus the stated $352,135.15 aggregate.",
        "treatment": "Preserve both one-cent discrepancies without silent correction.",
        "status": "OPEN_DOCUMENTED",
        "required_artifacts": ["Author or Foundation correction identifying controlling PIP-33 payment amounts."],
        "blocks_validation": False,
        "manual_review_required": True,
    })
    conflicts.append({
        "conflict_id": "GOV-CONFLICT-TREASURY-VERIFICATION-001",
        "pip_numbers": treasury_scope,
        "field_path": "treasury_states.onchain_verification_state",
        "classification": "MISSING_ONCHAIN_DATASET",
        "severity": "MATERIAL",
        "finding": "Council-reported payment values and PIP-33 authorization lack transaction-level on-chain evidence in the repository; PIP-33 payment occurrence remains UNVERIFIED.",
        "treatment": "Use COUNCIL_REPORTED only for attributed tracker values, keep PIP-33 payment_state UNVERIFIED, and use MISSING_ONCHAIN_EVIDENCE only for on-chain verification; never mark paid or verified.",
        "status": "OPEN_DOCUMENTED",
        "required_artifacts": ["Transaction signatures, token-account addresses, mint/decimals metadata, block times, and proposal-to-transfer mapping."],
        "blocks_validation": False,
        "manual_review_required": True,
    })
    conflicts.append({
        "conflict_id": "GOV-CONFLICT-PIP-001-QUORUM-001",
        "pip_numbers": [1],
        "field_path": "result.decision_rule",
        "classification": "EDITORIAL_RULE_NOT_SOURCE_NATIVE",
        "severity": "MATERIAL",
        "finding": "PIP-1 mentions quorum but supplies no numeric threshold; the completed-binary YES-versus-NO rule is an owner-approved repository editorial adjudication.",
        "treatment": "Label the adjudication as repository-editorial and never assert that it appears in PIP-1.",
        "status": "RESOLVED_BY_ADJUDICATION",
        "required_artifacts": ["Source-native numeric quorum rule, if one governed these historical votes."],
        "blocks_validation": False,
        "manual_review_required": True,
    })

    return conflicts


def build_backlog(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    _, _, passed_non_election_pips = proposal_partitions(proposals)
    unresolved_election_pips = unresolved_election_scope(proposals)
    placeholder_wallet_pips = placeholder_election_wallet_scope(proposals)
    treasury_scope = treasury_verification_scope(proposals)
    terminal_state_pips = sorted(
        pip["pip_number"]
        for pip in proposals
        if pip.get("execution_state") in {"TERMINATED", "CANCELED", "WITHDRAWN_AFTER_PASSAGE_NOT_IMPLEMENTED"}
    )
    proposal_numbers = sorted(pip["pip_number"] for pip in proposals)
    return [
        {
            "research_id": "GOV-RESEARCH-001",
            "priority": "P0",
            "pip_numbers": unresolved_election_pips,
            "question": "Who won the unresolved Council and DAO Casters elections, and what were the candidate-level totals?",
            "blocked_fields": ["vote.election.official_outcome_names", "vote.election.candidates[].candidate_pvp"],
            "missing_artifacts": ["Official STV tabulation export", "Official final winner announcement", "Per-candidate PVP and transfer-round data"],
            "acceptance_criteria": ["Winner identities reconcile to an official artifact", "Candidate totals preserve the election mechanism", "No candidate is inferred from later role occupancy"],
            "status": "OPEN",
            "onchain_dataset_required": False,
            "prohibited_inference": "Do not infer winners from later Council membership, social posts, or tracker passage alone.",
            "related_conflict_ids": ["GOV-CONFLICT-ELECTION-WINNERS-001", "GOV-CONFLICT-ELECTION-CANDIDATE-PVP-001", "GOV-CONFLICT-PIP-027-BALLOT-CONFIG-001"],
        },
        {
            "research_id": "GOV-RESEARCH-002",
            "priority": "P0",
            "pip_numbers": treasury_scope,
            "question": "Which authorized or Council-reported payments occurred on-chain?",
            "blocked_fields": ["treasury_states.onchain_verification_state", "treasury_states.payment_state"],
            "missing_artifacts": ["Transaction signatures", "DAO/Foundation source accounts", "Recipient token accounts", "Mint and decimals metadata", "Block timestamps", "Proposal-to-transfer mapping"],
            "acceptance_criteria": ["Every asserted transfer resolves to a transaction", "Token amounts are decoded using the correct mint decimals", "PIP authorization is not conflated with payment"],
            "status": "OPEN",
            "onchain_dataset_required": True,
            "prohibited_inference": "Do not treat Council tracker amounts, vote passage, or a payment schedule as proof of transfer.",
            "related_conflict_ids": ["GOV-CONFLICT-TREASURY-VERIFICATION-001"],
        },
        {
            "research_id": "GOV-RESEARCH-003",
            "priority": "P1",
            "pip_numbers": terminal_state_pips,
            "question": "What primary records establish termination, cancellation, or withdrawal after passage?",
            "blocked_fields": ["implementation.state", "implementation.independent_verification_state"],
            "missing_artifacts": ["Council or Foundation termination notice", "Author withdrawal notice", "Contract or milestone closeout record"],
            "acceptance_criteria": ["Terminal state has a dated primary record", "Passage remains historically preserved", "Payment and implementation remain separate"],
            "status": "OPEN",
            "onchain_dataset_required": False,
            "prohibited_inference": "Do not convert Council tracker terminology into independently verified completion or non-performance findings.",
            "related_conflict_ids": [],
        },
        {
            "research_id": "GOV-RESEARCH-004",
            "priority": "P1",
            "pip_numbers": passed_non_election_pips,
            "question": "What independent evidence supports implementation or deliverable completion for each authorized non-election proposal?",
            "blocked_fields": ["implementation.independent_verification_state"],
            "missing_artifacts": ["Proposal-specific deliverables", "Foundation execution notices", "Contracts or releases", "Independent outcome evidence"],
            "acceptance_criteria": ["Each implementation claim links to a primary artifact", "Milestone reporting remains attributed", "Failed proposals remain not authorized"],
            "status": "OPEN",
            "onchain_dataset_required": False,
            "prohibited_inference": "Do not equate 1/1 tracker milestones with independent implementation verification.",
            "related_conflict_ids": ["GOV-CONFLICT-FAILED-MILESTONES-001"],
        },
        {
            "research_id": "GOV-RESEARCH-007",
            "priority": "P1",
            "pip_numbers": placeholder_wallet_pips,
            "question": "Which candidate wallet belongs to each captured PIP-25 and PIP-27 candidate?",
            "blocked_fields": ["vote.election.candidates[].wallet_public_key"],
            "missing_artifacts": ["Official candidate-to-wallet mapping", "Signed candidate registration record or official ballot export"],
            "acceptance_criteria": ["Each normalized wallet resolves to an official candidate record", "The repeated sentinel remains preserved only as a captured placeholder"],
            "status": "OPEN",
            "onchain_dataset_required": False,
            "prohibited_inference": "Do not assign the repeated Solana sentinel value to any candidate and do not infer wallets from names or later officeholding.",
            "related_conflict_ids": ["GOV-CONFLICT-ELECTION-WALLET-PLACEHOLDERS-001"],
        },
        {
            "research_id": "GOV-RESEARCH-005",
            "priority": "P2",
            "pip_numbers": proposal_numbers,
            "question": "Can historical portal state transitions be recovered?",
            "blocked_fields": ["reconciliation.portal_current_status"],
            "missing_artifacts": ["Timestamped proposal-state snapshots", "Portal event log", "Official lifecycle export"],
            "acceptance_criteria": ["Publication, voting, result, and later lifecycle states have dated evidence", "Portal state is not used as implementation proof"],
            "status": "OPEN",
            "onchain_dataset_required": False,
            "prohibited_inference": "Do not infer state-transition dates solely from vote windows.",
            "related_conflict_ids": ["GOV-CONFLICT-PORTAL-STATUS-001"],
        },
        {
            "research_id": "GOV-RESEARCH-006",
            "priority": "P1",
            "pip_numbers": [33],
            "question": "Which PIP-33 figures control the authorized and conditional tranche payments?",
            "blocked_fields": ["financial_terms.arithmetic_discrepancies"],
            "missing_artifacts": ["Author or Foundation arithmetic correction", "Executed payment instruction", "Second-tranche reserve assessment"],
            "acceptance_criteria": ["Both one-cent discrepancies are explicitly resolved", "Each tranche remains 75% USDC and 25% ATLAS", "Second-tranche reserve condition is preserved", "Resolution does not imply payment"],
            "status": "OPEN",
            "onchain_dataset_required": True,
            "prohibited_inference": "Do not silently choose a corrected cent value or infer that either tranche was paid.",
            "related_conflict_ids": ["GOV-CONFLICT-PIP-033-ARITHMETIC-001", "GOV-CONFLICT-PIP-033-RESULT-001"],
        },
    ]


def implementation_state(pip: dict[str, Any]) -> str:
    is_election, is_failed, is_passed = source_lifecycle_flags(pip)
    if is_election:
        return "NOT_APPLICABLE_ELECTION"
    if is_failed:
        return "NOT_APPLICABLE_NO_AUTHORIZATION"
    if not is_passed:
        raise ValueError(f"PIP-{pip['pip_number']} has no supported non-election result state")
    state = pip.get("execution_state")
    council = pip.get("council_reported_implementation_state")
    if state == "TERMINATED":
        return "COUNCIL_REPORTED_TERMINATED"
    if state == "CANCELED":
        return "COUNCIL_REPORTED_CANCELED"
    if state == "WITHDRAWN_AFTER_PASSAGE_NOT_IMPLEMENTED":
        return "COUNCIL_REPORTED_WITHDRAWN_AFTER_PASSAGE_NOT_IMPLEMENTED"
    if council == "PARTIAL_OR_IN_PROGRESS":
        return "COUNCIL_REPORTED_PARTIAL_OR_IN_PROGRESS"
    if council == "MILESTONES_REPORTED_COMPLETE":
        return "COUNCIL_REPORTED_MILESTONES_COMPLETE"
    return "IMPLEMENTATION_UNVERIFIED"


def implementation_verification_state(pip: dict[str, Any]) -> str:
    is_election, is_failed, is_passed = source_lifecycle_flags(pip)
    if is_election:
        return "NOT_APPLICABLE_ELECTION"
    if is_failed:
        return "NOT_APPLICABLE_NO_AUTHORIZATION"
    if is_passed:
        return "MISSING_INDEPENDENT_PRIMARY_EVIDENCE"
    raise ValueError(f"PIP-{pip['pip_number']} has no supported implementation-verification state")


def result_record(pip: dict[str, Any]) -> dict[str, Any]:
    number = pip["pip_number"]
    if pip["vote_mechanism"] == "BINARY_PVP":
        return {
            "reviewed_result": pip["reviewed_result"],
            "portal_result": pip.get("portal_result"),
            "council_reported_result": pip.get("council_reported_result"),
            "basis": pip.get("reviewed_result_basis"),
            "decision_rule": "YES_PVP_GT_NO_PVP_PASS; NO_PVP_GTE_YES_PVP_FAIL; ABSTAIN_RECORDED_NOT_DECISIVE",
            "adjudication_source": "REPOSITORY_OWNER_APPROVED_EDITORIAL_RULE",
            "source_native_rule": False,
            "source_native_quorum_threshold": None,
        }
    if number == 6:
        reviewed = "FIRST_ROUND_ADVANCEMENT_RECORDED"
    elif number == 7:
        reviewed = "ELECTED_OFFICEHOLDERS_RECORDED"
    else:
        reviewed = "COUNCIL_REPORTED_PASSAGE_WINNERS_UNRESOLVED"
    return {
        "reviewed_result": reviewed,
        "portal_result": pip.get("portal_result"),
        "council_reported_result": pip.get("council_reported_result"),
        "basis": pip.get("reviewed_result_basis"),
        "decision_rule": "OFFICIAL_ELECTION_RESULTS_ONLY; COUNCIL_TRACKER_MAY_REPORT_PASSAGE_BUT_CANNOT_SUPPLY_MISSING_WINNERS",
        "adjudication_source": "MECHANISM_AWARE_EVIDENCE_RECONCILIATION",
        "source_native_rule": False,
        "source_native_quorum_threshold": None,
    }


def election_record(pip: dict[str, Any], raw: dict[str, Any]) -> dict[str, Any]:
    number = pip["pip_number"]
    outcomes = {6: ("FIRST_ROUND", "ADVANCEMENT_TO_FINAL_ROUND", "IDENTIFIED"), 7: ("FINAL_ROUND", "ELECTED_COUNCIL_MEMBERS", "IDENTIFIED")}
    stage, outcome_type, status = outcomes.get(number, ("SINGLE_ROUND", "WINNERS_UNRESOLVED", "UNRESOLVED"))
    winners = set(pip.get("election_winners") or [])
    candidates = []
    for option in raw.get("voteOptions") or []:
        value = option.get("value")
        if number == 6 and value in winners:
            outcome = "ADVANCED_TO_FINAL_ROUND"
        elif number == 7 and value in winners:
            outcome = "ELECTED"
        elif status == "UNRESOLVED":
            outcome = "UNRESOLVED"
        else:
            outcome = "NOT_SELECTED"
        captured_wallet = option.get("walletPublicKey")
        wallet_is_placeholder = captured_wallet == SOLANA_SENTINEL_WALLET
        candidates.append({
            "candidate_id": value,
            "display_name": option.get("displayValue"),
            "wallet_public_key": None if wallet_is_placeholder else captured_wallet,
            "captured_wallet_value": captured_wallet,
            "wallet_identification_status": "PLACEHOLDER_IN_CAPTURE" if wallet_is_placeholder else ("IDENTIFIED_FROM_CAPTURE" if captured_wallet else "MISSING_FROM_CAPTURE"),
            "candidate_ballots": None,
            "candidate_pvp": None,
            "candidate_total_status": "MISSING_FROM_CAPTURE",
            "outcome": outcome,
        })
    aggregate = (raw.get("proposalVoteData") or {}).get("voteSums") or []
    ranked = next((item for item in aggregate if str(item.get("option")).lower() == "rankedchoice"), None) or {}
    return {
        "stage": stage,
        "outcome_type": outcome_type,
        "winner_count_configured": raw.get("voteWinners"),
        "max_choices": raw.get("voteOptionsMaxChoices"),
        "candidate_count": len(candidates),
        "candidate_totals_status": "MISSING_FROM_CAPTURE",
        "candidates": candidates,
        "official_outcome_names": list(pip.get("election_winners") or []),
        "outcome_identification_status": status,
        "aggregate_ballots": int(ranked["count"]) if ranked.get("count") is not None else None,
        "aggregate_pvp": ranked.get("pvp"),
    }


def vote_record(pip: dict[str, Any], raw: dict[str, Any]) -> dict[str, Any]:
    if pip["vote_mechanism"] == "RANKED_CHOICE_ELECTION":
        election = election_record(pip, raw)
        return {
            "mechanism": "RANKED_CHOICE_ELECTION",
            "ballot_count": election["aggregate_ballots"],
            "total_pvp": election["aggregate_pvp"],
            "binary": None,
            "election": election,
        }
    yes = pip.get("vote_for") or {"ballots": None, "voting_power": None}
    no = pip.get("vote_against") or {"ballots": None, "voting_power": None}
    abstain = pip.get("vote_abstain")
    ballot_values = [yes.get("ballots"), no.get("ballots"), (abstain or {}).get("ballots")]
    return {
        "mechanism": "BINARY_PVP",
        "ballot_count": sum(int(value) for value in ballot_values if value is not None),
        "total_pvp": decimal_sum([yes.get("voting_power"), no.get("voting_power"), (abstain or {}).get("voting_power")]),
        "binary": {
            "yes_ballots": int(yes["ballots"]) if yes.get("ballots") is not None else None,
            "no_ballots": int(no["ballots"]) if no.get("ballots") is not None else None,
            "abstain_ballots": int(abstain["ballots"]) if abstain and abstain.get("ballots") is not None else None,
            "yes_pvp": yes.get("voting_power"),
            "no_pvp": no.get("voting_power"),
            "abstain_pvp": abstain.get("voting_power") if abstain else None,
            "abstain_capture_status": "CAPTURED" if abstain else "NOT_CAPTURED_OR_NOT_OFFERED",
        },
        "election": None,
    }


def treasury_states(pip: dict[str, Any]) -> tuple[dict[str, Any], str]:
    number = pip["pip_number"]
    is_election, _, is_passed = source_lifecycle_flags(pip)
    relevant = is_treasury_relevant(pip)
    if not relevant:
        return ({"request_state": None, "authorization_state": None, "payment_state": None, "onchain_verification_state": None}, "NOT_TREASURY_CLASSIFIED")

    concrete_report = has_concrete_council_payment_report(pip)
    if not is_passed:
        return ({
            "request_state": "REQUESTED",
            "authorization_state": None,
            "payment_state": None,
            "onchain_verification_state": None,
        }, pip.get("funding_source") or "TREASURY_RELEVANT_PROPOSAL")
    elif concrete_report:
        payment_state = "COUNCIL_REPORTED"
    else:
        payment_state = "UNVERIFIED"
    scope = "DIRECT_DAO_TREASURY_MEASURE" if number == 33 else pip.get("funding_source") or "TREASURY_RELEVANT_PROPOSAL"
    return ({
        "request_state": "REQUESTED",
        "authorization_state": "AUTHORIZED",
        "payment_state": payment_state,
        "onchain_verification_state": "MISSING_ONCHAIN_EVIDENCE" if is_passed and (concrete_report or number == 33) else "UNVERIFIED",
    }, scope)


def financial_terms(pip_number: int) -> dict[str, Any] | None:
    if pip_number != 33:
        return None
    return {
        "evidence_character": "AUTHORIZED_SCHEDULE_NOT_PAYMENT_EVIDENCE",
        "stated_total_usd": "469513.53",
        "stated_composition": {"usdc_percent": 75, "atlas_percent": 25, "stated_usdc_total": "352135.15", "stated_atlas_equivalent_total": "117378.38"},
        "tranches": [
            {"sequence": 1, "amount_usd": "234756.76", "usdc_percent": 75, "usdc_amount": "176067.57", "atlas_percent": 25, "atlas_equivalent_usd": "58689.19", "timing": "T_PLUS_14_DAYS_AFTER_PASSAGE"},
            {"sequence": 2, "amount_usd": "234756.76", "usdc_percent": 75, "usdc_amount": "176067.57", "atlas_percent": 25, "atlas_equivalent_usd": "58689.19", "timing": "180_DAYS_AFTER_TRANCHE_1", "source_schedule": "T_PLUS_194_DAYS_AFTER_PASSAGE", "condition": "DAO_TREASURY_MUST_RETAIN_CAPITAL_FOR_AN_ADDITIONAL_YEAR_OF_FOUNDATION_DAO_OPERATING_COSTS"},
        ],
        "arithmetic_discrepancies": [
            {"field": "tranche_total", "displayed_sum": "469513.52", "stated_total": "469513.53", "difference_usd": "0.01"},
            {"field": "usdc_total", "displayed_sum": "352135.14", "stated_total": "352135.15", "difference_usd": "0.01"},
        ],
        "payment_verified": False,
    }


def authorization_state(pip: dict[str, Any]) -> str:
    is_election, is_failed, is_passed = source_lifecycle_flags(pip)
    if is_election:
        return "NOT_APPLICABLE_ELECTION"
    if is_failed:
        return "NOT_AUTHORIZED"
    if is_passed:
        return "AUTHORIZED"
    raise ValueError(f"PIP-{pip['pip_number']} has no supported authorization state")


def build_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    proposals = read_json(SEMANTIC_PATH)["proposals"]
    reconciliation = {item["pip_number"]: item for item in read_json(RECONCILIATION_PATH)["records"]}
    relations = build_relationships()
    tracker_paths = tracker_path_map()
    conflicts = build_conflicts(proposals)
    conflict_by_pip: dict[int, list[str]] = defaultdict(list)
    conflict_status_by_id = {item["conflict_id"]: item["status"] for item in conflicts}
    for conflict in conflicts:
        for number in conflict["pip_numbers"]:
            conflict_by_pip[number].append(conflict["conflict_id"])
    backlog = build_backlog(proposals)
    research_by_pip: dict[int, list[str]] = defaultdict(list)
    for item in backlog:
        for number in item["pip_numbers"]:
            research_by_pip[number].append(item["research_id"])

    records: list[dict[str, Any]] = []
    for pip in sorted(proposals, key=lambda item: item["pip_number"]):
        number = pip["pip_number"]
        raw_path = raw_path_for(pip)
        raw = read_json(raw_path)
        source_record_path = source_record_path_for(pip)
        source_record = read_json(source_record_path)
        tracker_source_id = (pip.get("council_tracker") or {}).get("source_id")
        is_election, _, _ = source_lifecycle_flags(pip)
        treasury, scope = treasury_states(pip)
        record_conflict_ids = sorted(conflict_by_pip.get(number, []))
        open_conflicts = [conflict_id for conflict_id in record_conflict_ids if conflict_status_by_id[conflict_id] == "OPEN_DOCUMENTED"]
        record = {
            "pip_id": f"PIP-{number:02d}",
            "pip_number": number,
            "source_id": pip["source_id"],
            "proposal_uuid": pip["proposal_uuid"],
            "title": pip["title"],
            "reviewed_title": pip.get("reviewed_title"),
            "author": author_record(pip),
            "category": {"source_values": pip.get("proposal_category") or [], "normalized": categories(pip.get("proposal_category") or [])},
            "dates": {
                "publication": pip.get("publication_date"),
                "updated": pip.get("updated_date"),
                "vote_start": pip.get("vote_start"),
                "vote_end": pip.get("vote_end"),
            },
            "sources": {
                "portal_url": pip.get("proposal_url"),
                "full_text_source_path": repo_path(raw_path),
                "source_record_path": repo_path(source_record_path),
                "semantic_record_path": repo_path(SEMANTIC_PATH),
                "reconciliation_path": repo_path(RECONCILIATION_PATH),
                "council_tracker_source_id": tracker_source_id,
                "council_tracker_source_path": tracker_paths.get(tracker_source_id),
                "raw_content_sha256": source_record.get("content_sha256"),
            },
            "vote": vote_record(pip, raw),
            "result": result_record(pip),
            "relationships": relations.get(number, []),
            "authorization": {"state": authorization_state(pip), "basis": "NOT_APPLICABLE_TO_ELECTION_OUTCOME" if is_election else "REVIEWED_BINARY_RESULT"},
            "implementation": {
                "state": implementation_state(pip),
                "council_reported_state": pip.get("council_reported_implementation_state"),
                "attribution": "STAR_ATLAS_COUNCIL_TRACKER" if tracker_source_id else None,
                "independent_verification_state": implementation_verification_state(pip),
            },
            "funding_scope": scope,
            "treasury_states": treasury,
            "financial_terms": financial_terms(number),
            "reconciliation": {
                "overall_status": "OPEN_DOCUMENTED_CONFLICTS" if open_conflicts else "RECONCILED_NO_OPEN_CONFLICTS",
                "vote_result_reconciliation_status": pip.get("cross_source_reconciliation_status"),
                "portal_current_status": pip.get("portal_current_status") or pip.get("portal_status"),
                "portal_status_interpretation": "STALE_COMPLETED_VOTE_WINDOW",
                "council_result": pip.get("council_reported_result"),
                "contradictions": pip.get("contradictions") or [],
                "notes": pip.get("reconciliation_notes") or [],
                "independently_verified": reconciliation[number].get("independently_verified", False),
            },
            "conflict_ids": record_conflict_ids,
            "research_backlog_ids": sorted(research_by_pip.get(number, [])),
            "known_limitations": sorted(set((pip.get("limitations") or []) + (pip.get("research_gaps") or []))),
            "review_status": "HUMAN_REVIEW_REQUIRED",
        }
        records.append(record)
    return records, conflicts, backlog


def md_cell(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\n", " ")


def relative_knowledge_link(path: str) -> str:
    return "../../" + path


def vote_summary(record: dict[str, Any]) -> str:
    vote = record["vote"]
    if vote["mechanism"] == "BINARY_PVP":
        binary = vote["binary"]
        abstain = "not captured" if binary["abstain_pvp"] is None else f"{binary['abstain_ballots']} / {binary['abstain_pvp']}"
        return f"YES {binary['yes_ballots']} / {binary['yes_pvp']}; NO {binary['no_ballots']} / {binary['no_pvp']}; abstain {abstain}; total PVP {vote['total_pvp']}"
    election = vote["election"]
    return f"RCV aggregate {election['aggregate_ballots']} ballots / {election['aggregate_pvp']} PVP; {election['candidate_count']} candidates; candidate PVP missing"


def build_markdown(ledger: dict[str, Any], conflicts: list[dict[str, Any]], backlog: list[dict[str, Any]]) -> str:
    records = ledger["records"]
    lines = [
        "---",
        'title: "Canonical PIP and Governance Ledger"',
        "knowledge_status: QUALIFIED",
        f"as_of: {AS_OF}",
        "confidence: MEDIUM",
        "page_risk_score: 7",
        "page_risk_class: R3",
        "ledger_status: DRAFT_FOR_REVIEW",
        "review_status: HUMAN_REVIEW_REQUIRED",
        "evidence_basis:",
        '  - "archive/raw/social-governance-semantic-enrichment/governance/pip-captures/"',
        '  - "archive/semantic/governance/pip-registry-semantic.json"',
        '  - "archive/semantic/governance/pip-source-reconciliation.json"',
        '  - "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"',
        "known_limitations:",
        '  - "Election candidate-level PVP is absent from the preserved portal captures."',
        '  - "Council payment and implementation fields are attributed and are not independently verified."',
        '  - "No on-chain treasury verification was performed because the required dataset was not supplied."',
        "research_gaps:",
        '  - "Official winner records remain missing for PIP-11, PIP-25, and PIP-27."',
        '  - "Transaction and deliverable evidence remains incomplete."',
        "review_after: 2026-10-18",
        "---",
        "",
        "# Canonical PIP and Governance Ledger",
        "",
        "This draft ledger reconciles the 33 numbered official portal captures available in the repository. It is canonical in scope—one record per PIP from PIP-1 through PIP-33—but remains `QUALIFIED` and `DRAFT_FOR_REVIEW` until human approval. It does not rewrite any source record.",
        "",
        "The machine-readable companion is [PIP-Registry.json](PIP-Registry.json). Conflicts and required follow-up evidence are maintained under the [ledger campaign](../../operations/campaigns/canonical-pip-governance-ledger-2026-07/README.md).",
        "",
        "## Interpretation policy",
        "",
        "- Proposal publication, voting, result, authorization, payment, implementation, and independent verification are separate states.",
        "- Completed binary results use an **owner-approved repository editorial adjudication**: YES PVP greater than NO PVP is reviewed as passed; otherwise failed. This rule is not asserted as text contained in PIP-1. Abstentions remain visible and non-decisive.",
        "- Ranked-choice elections never use binary fields. The preserved captures contain only aggregate election ballots/PVP. Candidate-level PVP is explicitly missing for PIP-6, PIP-7, PIP-11, PIP-25, and PIP-27.",
        "- PIP-6 names first-round advancing candidates; PIP-7 names final elected officeholders. PIP-11, PIP-25, and PIP-27 preserve Council-reported passage while winner identity remains unresolved.",
        "- Council tracker milestone, payment, termination, cancellation, withdrawal, and ROI fields are Council-authored operational assessments. They are not independent verification.",
        "- No on-chain payment verification is performed or implied. Treasury state values are restricted to `REQUESTED`, `AUTHORIZED`, `COUNCIL_REPORTED`, `UNVERIFIED`, `MISSING_ONCHAIN_EVIDENCE`, or null when not applicable.",
        "",
        "## Ledger",
        "",
        "Vote entries use `ballots / PVP`. Full-text links point to immutable raw portal captures.",
        "",
        "| PIP | Title / author / category | Publication and vote window | Mechanism and vote evidence | Result and authorization | Implementation and payment | Reconciliation | Full text |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for record in records:
        author = record["author"]["display_name"] or f"unresolved identity; public key {record['author']['public_key']}"
        identity = f"{record['title']}<br>{author}<br>{', '.join(record['category']['normalized'])}"
        dates = f"published {record['dates']['publication']}<br>vote {record['dates']['vote_start']} to {record['dates']['vote_end']}"
        decision = f"{record['result']['reviewed_result']}<br>{record['authorization']['state']}"
        treasury = record["treasury_states"]
        state = f"{record['implementation']['state']}<br>independent implementation verification {record['implementation']['independent_verification_state']}<br>payment {treasury['payment_state'] or 'not applicable'}<br>on-chain {treasury['onchain_verification_state'] or 'not applicable'}"
        reconciliation = f"{record['reconciliation']['overall_status']}<br>vote/result: {record['reconciliation']['vote_result_reconciliation_status']}<br>{len(record['conflict_ids'])} documented conflict links"
        full_text = f"[raw capture]({relative_knowledge_link(record['sources']['full_text_source_path'])})"
        lines.append("| " + " | ".join(md_cell(value) for value in [record["pip_id"], identity, dates, vote_summary(record), decision, state, reconciliation, full_text]) + " |")

    lines += ["", "## Election detail", ""]
    for record in records:
        election = record["vote"]["election"]
        if not election:
            continue
        lines += [
            f"### {record['pip_id']} — {record['title']}",
            "",
            f"- Stage: `{election['stage']}`",
            f"- Outcome: `{election['outcome_type']}`",
            f"- Aggregate: {election['aggregate_ballots']} ballots / {election['aggregate_pvp']} PVP",
            f"- Configured winners: {election['winner_count_configured']}; maximum choices: {election['max_choices']}; candidates: {election['candidate_count']}",
            f"- Winner identification: `{election['outcome_identification_status']}`",
            "- Candidate totals: `MISSING_FROM_CAPTURE`; every candidate PVP field remains null.",
            "",
            "| Candidate ID | Display name | Outcome | Candidate PVP |",
            "|---|---|---|---|",
        ]
        for candidate in election["candidates"]:
            lines.append(f"| {md_cell(candidate['candidate_id'])} | {md_cell(candidate['display_name'])} | {candidate['outcome']} | MISSING_FROM_CAPTURE |")
        lines.append("")

    lines += [
        "## Relationships",
        "",
        "| From | Relationship | To | Evidence |",
        "|---|---|---|---|",
    ]
    seen: set[tuple[int, str, int]] = set()
    for record in records:
        for relationship in record["relationships"]:
            key = (relationship["from_pip"], relationship["relationship"], relationship["to_pip"])
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"| PIP-{key[0]} | {key[1]} | PIP-{key[2]} | [{relationship['evidence_source_id']}]({relative_knowledge_link(relationship['evidence_path'])}) |")

    pip33 = next(record for record in records if record["pip_number"] == 33)
    terms = pip33["financial_terms"]
    lines += [
        "",
        "## PIP-33 financial-term preservation",
        "",
        "PIP-33 authorized a stated maximum of **$469,513.53** through two displayed tranches of **$234,756.76**. Each tranche is **$176,067.57 USDC (75%)** plus **$58,689.19 ATLAS-equivalent (25%)**. The first tranche was scheduled for T+14 days. The second was scheduled for T+194 days—180 days after the first—and was conditional on retaining sufficient DAO Treasury capital for an additional year of Foundation/DAO operating costs.",
        "",
        f"The displayed tranches total **${terms['arithmetic_discrepancies'][0]['displayed_sum']}**, one cent below the stated total. Their USDC components total **${terms['arithmetic_discrepancies'][1]['displayed_sum']}**, one cent below the stated USDC aggregate. Both discrepancies are preserved; neither is silently corrected. Authorization and schedule do not prove payment: `payment_state` remains `UNVERIFIED`, while `onchain_verification_state` is `MISSING_ONCHAIN_EVIDENCE`.",
        "",
        "## Conflict register",
        "",
        "| Conflict | PIPs | Finding | Treatment | Status |",
        "|---|---|---|---|---|",
    ]
    for item in conflicts:
        pips = ", ".join(f"PIP-{number}" for number in item["pip_numbers"])
        lines.append(f"| {item['conflict_id']} | {pips} | {md_cell(item['finding'])} | {md_cell(item['treatment'])} | {item['status']} |")

    lines += ["", "## Prioritized governance research backlog", "", "| Priority | Research item | PIPs | Required artifacts | Prohibited inference |", "|---|---|---|---|---|"]
    for item in backlog:
        pips = ", ".join(f"PIP-{number}" for number in item["pip_numbers"])
        lines.append(f"| {item['priority']} | {item['research_id']}: {md_cell(item['question'])} | {pips} | {md_cell(item['missing_artifacts'])} | {md_cell(item['prohibited_inference'])} |")

    lines += [
        "",
        "## Evidence and review status",
        "",
        "- [Machine ledger](PIP-Registry.json)",
        "- [Official portal semantic registry](../../archive/semantic/governance/pip-registry-semantic.json)",
        "- [Portal/Council reconciliation](../../archive/semantic/governance/pip-source-reconciliation.json)",
        "- [Election outcome adjudications](../../archive/semantic/governance/pip-election-round-outcomes.json)",
        "- [Relationship index](../../archive/semantic/governance/pip-supersession-index.json)",
        "- [Campaign conflict report](../../operations/campaigns/canonical-pip-governance-ledger-2026-07/conflict-report.md)",
        "- [Campaign research backlog](../../operations/campaigns/canonical-pip-governance-ledger-2026-07/governance-research-backlog.md)",
        "",
        "The ledger remains draft and requires human governance review. Validation establishes structural and evidentiary consistency; it does not establish the truth of Council assessments, implementation, payment, or on-chain execution.",
        "",
    ]
    return "\n".join(lines)


def conflict_markdown(conflicts: list[dict[str, Any]]) -> str:
    lines = ["# Canonical PIP Ledger Conflict Report", "", "Every conflict is preserved rather than resolved by inference.", ""]
    for item in conflicts:
        lines += [
            f"## {item['conflict_id']}",
            "",
            f"- PIPs: {', '.join('PIP-' + str(n) for n in item['pip_numbers'])}",
            f"- Classification: `{item['classification']}`",
            f"- Severity: `{item['severity']}`",
            f"- Status: `{item['status']}`",
            f"- Finding: {item['finding']}",
            f"- Treatment: {item['treatment']}",
            f"- Required artifacts: {'; '.join(item['required_artifacts']) or 'None; resolved from existing evidence.'}",
            "",
        ]
    return "\n".join(lines)


def backlog_markdown(backlog: list[dict[str, Any]]) -> str:
    lines = ["# Governance Research Backlog", "", "This backlog identifies the exact evidence needed to promote unresolved fields. New acquisition is not performed in this campaign.", ""]
    for item in sorted(backlog, key=lambda value: (value["priority"], value["research_id"])):
        lines += [
            f"## {item['research_id']} — {item['priority']}",
            "",
            f"- PIPs: {', '.join('PIP-' + str(n) for n in item['pip_numbers'])}",
            f"- Question: {item['question']}",
            f"- Missing artifacts: {'; '.join(item['missing_artifacts'])}",
            f"- Acceptance criteria: {'; '.join(item['acceptance_criteria'])}",
            f"- On-chain dataset required: {'yes' if item['onchain_dataset_required'] else 'no'}",
            f"- Prohibited inference: {item['prohibited_inference']}",
            "",
        ]
    return "\n".join(lines)


def main() -> None:
    records, conflicts, backlog = build_records()
    result_counts = Counter(record["result"]["reviewed_result"] for record in records)
    mechanism_counts = Counter(record["vote"]["mechanism"] for record in records)
    implementation_counts = Counter(record["implementation"]["state"] for record in records)
    implementation_verification_counts = Counter(record["implementation"]["independent_verification_state"] for record in records)
    failed_pips = sorted(record["pip_number"] for record in records if record["result"]["reviewed_result"] == "FAILED")
    unresolved_election_outcomes = sorted(
        record["pip_number"]
        for record in records
        if record["vote"]["mechanism"] == "RANKED_CHOICE_ELECTION"
        and record["vote"]["election"]["outcome_identification_status"] == "UNRESOLVED"
    )
    ledger = {
        "ledger_id": "CANONICAL-PIP-GOVERNANCE-LEDGER",
        "schema_version": "1.0.0",
        "as_of": AS_OF,
        "ledger_status": "DRAFT_FOR_REVIEW",
        "review_status": "HUMAN_REVIEW_REQUIRED",
        "knowledge_status": "QUALIFIED",
        "scope": {"first_pip": 1, "last_pip": 33, "record_count": len(records)},
        "interpretation_policy": {
            "completed_binary_rule": "YES_PVP_GT_NO_PVP_PASS; NO_PVP_GTE_YES_PVP_FAIL; ABSTAIN_RECORDED_NOT_DECISIVE",
            "completed_binary_rule_authority": "REPOSITORY_OWNER_APPROVED_EDITORIAL_ADJUDICATION",
            "completed_binary_rule_is_source_native_pip_1_text": False,
            "election_rule": "OFFICIAL_ELECTION_RESULTS_ONLY; MISSING_WINNERS_REMAIN_UNRESOLVED",
            "candidate_level_pvp_in_capture": False,
            "onchain_verification_performed": False,
            "council_tracker_attribution": "COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT",
            "independent_verification_status": "UNKNOWN",
        },
        "controlled_treasury_state_values": sorted(TREASURY_STATES),
        "source_inputs": [
            repo_path(SEMANTIC_PATH),
            repo_path(RECONCILIATION_PATH),
            repo_path(RELATIONSHIPS_PATH),
            repo_path(ELECTION_OUTCOMES_PATH),
            repo_path(TRACKER_SEMANTIC_PATH),
            repo_path(RAW_ROOT),
            repo_path(SOURCE_RECORD_ROOT),
        ],
        "summary": {
            "mechanism_counts": dict(sorted(mechanism_counts.items())),
            "result_counts": dict(sorted(result_counts.items())),
            "implementation_state_counts": dict(sorted(implementation_counts.items())),
            "implementation_verification_state_counts": dict(sorted(implementation_verification_counts.items())),
            "documented_conflicts": len(conflicts),
            "research_backlog_items": len(backlog),
        },
        "records": records,
    }
    write_json(LEDGER_JSON, ledger)
    LEDGER_MD.write_text(build_markdown(ledger, conflicts, backlog), encoding="utf-8")
    write_json(HERE / "conflict-report.json", {"ledger_id": ledger["ledger_id"], "as_of": AS_OF, "conflict_count": len(conflicts), "conflicts": conflicts})
    (HERE / "conflict-report.md").write_text(conflict_markdown(conflicts), encoding="utf-8")
    write_json(HERE / "governance-research-backlog.json", {"ledger_id": ledger["ledger_id"], "as_of": AS_OF, "item_count": len(backlog), "items": backlog})
    (HERE / "governance-research-backlog.md").write_text(backlog_markdown(backlog), encoding="utf-8")
    summary = {
        "campaign_id": "canonical-pip-governance-ledger-2026-07",
        "status": "DRAFT_FOR_REVIEW",
        "as_of": AS_OF,
        "records": len(records),
        "binary_pips": mechanism_counts["BINARY_PVP"],
        "election_pips": mechanism_counts["RANKED_CHOICE_ELECTION"],
        "failed_pips": failed_pips,
        "unresolved_election_outcomes": unresolved_election_outcomes,
        "lifecycle_generation_basis": "SOURCE_BACKED_VOTE_MECHANISM_AND_REVIEWED_RESULT",
        "pip_33_treasury_states": {
            "payment_state": records[32]["treasury_states"]["payment_state"],
            "onchain_verification_state": records[32]["treasury_states"]["onchain_verification_state"],
            "payment_implied": False,
        },
        "documented_conflicts": len(conflicts),
        "research_backlog_items": len(backlog),
        "onchain_verification_performed": False,
        "source_records_rewritten": False,
    }
    write_json(HERE / "campaign-summary.json", summary)
    (HERE / "campaign-summary.md").write_text(
        "# Canonical PIP and Governance Ledger Campaign Summary\n\n"
        f"- Status: **{summary['status']}**\n"
        f"- Records: {len(records)} (PIP-1 through PIP-33)\n"
        f"- Binary PIPs: {summary['binary_pips']}\n"
        f"- Ranked-choice election PIPs: {summary['election_pips']}\n"
        f"- Failed/no-authorization PIPs: {', '.join('PIP-' + str(n) for n in summary['failed_pips'])}\n"
        f"- Unresolved election outcomes: {', '.join('PIP-' + str(n) for n in summary['unresolved_election_outcomes'])}\n"
        f"- Lifecycle generation basis: {summary['lifecycle_generation_basis']}\n"
        f"- PIP-33 payment state: {summary['pip_33_treasury_states']['payment_state']}\n"
        f"- PIP-33 on-chain verification state: {summary['pip_33_treasury_states']['onchain_verification_state']}\n"
        "- PIP-33 payment implied: no\n"
        f"- Documented conflict clusters: {len(conflicts)}\n"
        f"- Research backlog items: {len(backlog)}\n"
        "- On-chain verification performed: no\n"
        "- Source records rewritten: no\n",
        encoding="utf-8",
    )
    print(f"Built {len(records)} PIP ledger records, {len(conflicts)} conflict clusters, and {len(backlog)} research items")


if __name__ == "__main__":
    main()
