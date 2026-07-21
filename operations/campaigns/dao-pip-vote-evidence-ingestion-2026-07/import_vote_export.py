#!/usr/bin/env python3
"""Import the operator-provided PIP-1 through PIP-32 DAO vote export."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import shutil
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


CAMPAIGN_ID = "dao-pip-vote-evidence-ingestion-2026-07"
PACKAGE_SOURCE_ID = "SRC-SOLANA-DAO-PIP-VOTES-4E01123F31A2"
EXPECTED_PACKAGE_SHA256 = "4e01123f31a2531427fc1910841efae45e24b15f4472338fbbf174c2e5b52d08"
EXPECTED_PACKAGE_MEMBERS = {
    *(f"Star Atlas DAO PIP Votes/PIP-{number:02d}.json" for number in range(1, 33)),
    "Star Atlas DAO PIP Votes/PIP-33.txt",
}
ELECTION_PIPS = {6, 7, 11, 25, 27}
CAPTURED_AT = "2026-07-20"
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RAW_REL = Path("archive/raw/governance-votes/pip-01-32/Star Atlas DAO PIP Votes.zip")
RAW_PATH = ROOT / RAW_REL
NORMALIZED_ROOT_REL = Path("archive/normalized/governance-votes/pip-01-32")
NORMALIZED_ROOT = ROOT / NORMALIZED_ROOT_REL
PROVENANCE_REL = Path("archive/provenance/governance-votes/pip-01-32.json")
PROVENANCE_PATH = ROOT / PROVENANCE_REL
SOURCE_RECORD_ROOT_REL = Path("archive/source-records/governance-votes/pip-01-32")
SOURCE_RECORD_ROOT = ROOT / SOURCE_RECORD_ROOT_REL
LEDGER_PATH = ROOT / "knowledge/governance/PIP-Registry.json"
ROUNDING_QUANTUM = Decimal("0.00001")

BINARY_MESSAGE_PATTERN = re.compile(
    r"^I (?P<wallet>\S+) vote (?P<vote>\S+) to PIP-(?P<pip>\d+) with hash (?P<hash>\S+) "
    r"on (?P<timestamp>\S+) with (?P<locked_polis>[0-9.]+) POLIS locked until (?P<lock_until>\d+)$",
    re.IGNORECASE,
)
ELECTION_MESSAGE_PATTERN = re.compile(
    r"^I (?P<wallet>\S+) vote to rank (?P<rankings>.+?) as my "
    r"(?:first and only choice|choices from 1 to (?P<choice_count>\d+)) on the proposal "
    r"PIP-(?P<pip>\d+) with hash (?P<hash>\S+) on (?P<timestamp>\S+) with "
    r"(?P<locked_polis>[0-9.]+) POLIS locked until (?P<lock_until>\d+)$",
    re.IGNORECASE,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def round_five(value: Decimal | str) -> str:
    return format(Decimal(value).quantize(ROUNDING_QUANTUM, rounding=ROUND_HALF_UP), "f")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8", newline="\n")


def load_ledger_metadata() -> dict[int, dict[str, Any]]:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return {record["pip_number"]: record for record in ledger["records"]}


def source_id(pip_number: int, member_sha256: str) -> str:
    return f"SRC-SOLANA-PIP-{pip_number:02d}-{member_sha256[:12].upper()}"


def parse_message(record: dict[str, Any], pip_number: int, mechanism: str) -> dict[str, Any]:
    pattern = ELECTION_MESSAGE_PATTERN if mechanism == "RANKED_CHOICE_ELECTION" else BINARY_MESSAGE_PATTERN
    match = pattern.fullmatch(record["message"])
    if match is None:
        raise ValueError(f"unrecognized signed message in {record.get('id')}")
    parsed = match.groupdict()
    if parsed["wallet"] != record["walletPublicKey"]:
        raise ValueError(f"message wallet mismatch in {record['id']}")
    if int(parsed["pip"]) != pip_number:
        raise ValueError(f"message PIP mismatch in {record['id']}")
    if parsed["hash"] != record["proposalHash"]:
        raise ValueError(f"message proposal hash mismatch in {record['id']}")

    if mechanism == "RANKED_CHOICE_ELECTION":
        rankings = [value.strip() for value in parsed["rankings"].split(",") if value.strip()]
        raw_rankings = [value.strip() for value in record["voteResult"].split(",") if value.strip()]
        if rankings != raw_rankings:
            raise ValueError(f"ranked choices mismatch in {record['id']}")
        if parsed["choice_count"] is not None and int(parsed["choice_count"]) != len(rankings):
            raise ValueError(f"ranked choice count mismatch in {record['id']}")
        return {**parsed, "rankings_parsed": rankings}

    if parsed["vote"].upper() != str(record["voteResult"]).upper():
        raise ValueError(f"binary vote result mismatch in {record['id']}")
    return parsed


def normalize_record(
    record: dict[str, Any],
    pip_number: int,
    ledger_record: dict[str, Any],
    member_path: str,
    member_sha256: str,
) -> dict[str, Any]:
    mechanism = ledger_record["vote"]["mechanism"]
    parsed = parse_message(record, pip_number, mechanism)
    created = parse_timestamp(record["createdAt"])
    signed = parse_timestamp(parsed["timestamp"])
    skew = Decimal(str((created - signed).total_seconds())).quantize(Decimal("0.001"))
    signature_bytes = base64.b64decode(record["signature"], validate=True)
    memo_used = bool(record["memoProgramUsed"])
    if not memo_used and len(signature_bytes) != 64:
        raise ValueError(f"non-memo signature is not 64 bytes in {record['id']}")

    if mechanism == "RANKED_CHOICE_ELECTION":
        ballot = {
            "mechanism": "RANKED_CHOICE_ELECTION",
            "choice_raw": record["voteResult"],
            "binary_choice": None,
            "ranked_choices": [
                {"rank": index, "candidate_label_raw": label, "candidate_entity_id": None}
                for index, label in enumerate(parsed["rankings_parsed"], start=1)
            ],
        }
    else:
        ballot = {
            "mechanism": "BINARY_PVP_WITH_ABSTAIN",
            "choice_raw": record["voteResult"],
            "binary_choice": str(record["voteResult"]).upper(),
            "ranked_choices": [],
        }

    lock_until = int(parsed["lock_until"])
    return {
        "vote_event_id": record["id"],
        "schema_version": "1.0.0",
        "record_type": "solana_governance_vote_event",
        "network": "Solana",
        "proposal": {
            "pip_id": f"PIP-{pip_number:02d}",
            "pip_number": pip_number,
            "proposal_id": record["proposalId"],
            "proposal_hash": record["proposalHash"],
            "title": ledger_record["reviewed_title"] or ledger_record["title"],
        },
        "ballot": ballot,
        "wallet_public_key": record["walletPublicKey"],
        "voting_power_pvp_raw": record["votingPower"],
        "voting_power_pvp_rounded_5dp": round_five(record["votingPower"]),
        "signed_message": record["message"],
        "signed_message_timestamp": parsed["timestamp"],
        "portal_record_created_at": record["createdAt"],
        "portal_minus_signed_seconds": format(skew, "f"),
        "timestamp_integrity_status": "TIMESTAMP_ORDER_ANOMALY" if skew < 0 else "ORDERED",
        "locked_polis_raw": parsed["locked_polis"],
        "lock_expires_unix": lock_until,
        "lock_expires_at": datetime.fromtimestamp(lock_until, timezone.utc).isoformat().replace("+00:00", "Z"),
        "solana_validation_value": record["signature"],
        "solana_validation_value_encoding": "BASE64",
        "decoded_validation_value_bytes": len(signature_bytes),
        "validation_value_representation": (
            "BASE64_SERIALIZED_TRANSACTION_LIKE_PAYLOAD" if memo_used else "BASE64_ED25519_DETACHED_SIGNATURE_BYTES"
        ),
        "memo_program_used": memo_used,
        "independent_rpc_reverification_status": "NOT_PERFORMED",
        "identity_enrichment": {
            "display_name_observed": None,
            "canonical_identity": None,
            "identity_attribution_status": "UNADJUDICATED",
        },
        "source": {
            "package_source_id": PACKAGE_SOURCE_ID,
            "proposal_source_id": source_id(pip_number, member_sha256),
            "source_type": "OPERATOR_PROVIDED_PRIMARY_BLOCKCHAIN_DERIVED_OFFICIAL_DAO_EXPORT",
            "source_authority_class": "A1",
            "package_sha256": EXPECTED_PACKAGE_SHA256,
            "member_path": member_path,
            "member_sha256": member_sha256,
            "raw_archive_path": RAW_REL.as_posix(),
            "operator_confirmation": "VALID_SOLANA_BLOCKCHAIN_EVIDENCE_VIEWED_THROUGH_OFFICIAL_STAR_ATLAS_DAO_WEBSITE",
        },
    }


def build_summary(pip_number: int, ledger_record: dict[str, Any], rows: list[dict[str, Any]], member_sha256: str) -> dict[str, Any]:
    mechanism = ledger_record["vote"]["mechanism"]
    pvp_total = sum((Decimal(row["voting_power_pvp_raw"]) for row in rows), Decimal(0))
    summary: dict[str, Any] = {
        "pip_id": f"PIP-{pip_number:02d}",
        "pip_number": pip_number,
        "title": ledger_record["reviewed_title"] or ledger_record["title"],
        "proposal_id": rows[0]["proposal"]["proposal_id"],
        "proposal_hash": rows[0]["proposal"]["proposal_hash"],
        "source_id": source_id(pip_number, member_sha256),
        "ballot_mechanism": mechanism,
        "vote_event_count": len(rows),
        "effective_ballot_count": len(rows),
        "unique_wallet_count": len({row["wallet_public_key"] for row in rows}),
        "total_pvp_raw": str(pvp_total),
        "total_pvp_rounded_5dp": round_five(pvp_total),
        "signed_message_timestamp_min": min(row["signed_message_timestamp"] for row in rows),
        "signed_message_timestamp_max": max(row["signed_message_timestamp"] for row in rows),
        "portal_record_created_at_min": min(row["portal_record_created_at"] for row in rows),
        "portal_record_created_at_max": max(row["portal_record_created_at"] for row in rows),
        "timestamp_order_anomaly_count": sum(row["timestamp_integrity_status"] == "TIMESTAMP_ORDER_ANOMALY" for row in rows),
        "superseded_vote_event_count": 0,
        "independent_rpc_reverification_status": "NOT_PERFORMED",
    }
    if mechanism == "BINARY_PVP":
        counts: Counter[str] = Counter()
        pvp: defaultdict[str, Decimal] = defaultdict(Decimal)
        for row in rows:
            choice = row["ballot"]["binary_choice"]
            counts[choice] += 1
            pvp[choice] += Decimal(row["voting_power_pvp_raw"])
        yes = pvp["YES"]
        no = pvp["NO"]
        result = "PASSED" if yes > no else "FAILED" if no > yes else "TIED"
        summary["binary_result"] = {
            "ballot_counts": {key.lower(): counts[key] for key in ("YES", "NO", "ABSTAIN")},
            "pvp_raw": {key.lower(): str(pvp[key]) for key in ("YES", "NO", "ABSTAIN")},
            "pvp_rounded_5dp": {key.lower(): round_five(pvp[key]) for key in ("YES", "NO", "ABSTAIN")},
            "result": result,
            "result_rule": "REPOSITORY_OWNER_APPROVED_YES_GT_NO; ABSTAIN_RECORDED_NOT_DECISIVE",
            "result_rule_is_source_native": False,
        }
        summary["election_result"] = None
    else:
        first_counts: Counter[str] = Counter()
        first_pvp: defaultdict[str, Decimal] = defaultdict(Decimal)
        candidates: set[str] = set()
        for row in rows:
            rankings = row["ballot"]["ranked_choices"]
            candidates.update(item["candidate_label_raw"] for item in rankings)
            first = rankings[0]["candidate_label_raw"]
            first_counts[first] += 1
            first_pvp[first] += Decimal(row["voting_power_pvp_raw"])
        summary["binary_result"] = None
        summary["election_result"] = {
            "candidate_count_observed": len(candidates),
            "candidate_labels_raw": sorted(candidates),
            "first_preference_statistics": [
                {
                    "candidate_label_raw": candidate,
                    "ballot_count": first_counts[candidate],
                    "pvp_raw": str(first_pvp[candidate]),
                    "pvp_rounded_5dp": round_five(first_pvp[candidate]),
                    "interpretation": "DESCRIPTIVE_FIRST_PREFERENCE_ONLY_NOT_FINAL_STV_TALLY",
                }
                for candidate in sorted(candidates)
            ],
            "final_tally_status": "NOT_COMPUTED_STV_IMPLEMENTATION_RULES_NOT_CAPTURED",
            "winner_inference_performed": False,
        }
    return summary


def markdown_source_record(record: dict[str, Any], summary: dict[str, Any]) -> str:
    limitations = record["quality"]["limitations"]
    return "\n".join([
        f"# {record['title']}",
        "",
        "## Metadata",
        "",
        f"- Source ID: `{record['source_id']}`",
        f"- PIP: `{summary['pip_id']}`",
        f"- Proposal UUID: `{summary['proposal_id']}`",
        f"- Proposal hash: `{summary['proposal_hash']}`",
        f"- Ballot mechanism: `{summary['ballot_mechanism']}`",
        f"- Vote events: {summary['vote_event_count']}",
        f"- Unique wallets: {summary['unique_wallet_count']}",
        f"- Total PVP: {summary['total_pvp_rounded_5dp']}",
        "- Authority: `A1 — operator-confirmed primary blockchain-derived official DAO export`",
        "- Independent RPC reverification: `NOT_PERFORMED`",
        "",
        "## Provenance",
        "",
        f"The record was extracted from `{record['provenance']['original_member_path']}` inside the operator-supplied archive. The archive is preserved unchanged at `{RAW_REL.as_posix()}`.",
        "",
        "## Evidence scope",
        "",
        "This source establishes the supplied ballot records, wallet public keys, ordered selections, voting power, signed messages, lock metadata, validation payloads, and portal record timestamps. It does not establish implementation, treasury payment, or post-vote execution.",
        "",
        "## Known limitations",
        "",
        *(f"- {value}" for value in limitations),
        "",
        "## Artifact chain",
        "",
        f"- [Normalized vote events](../../../normalized/governance-votes/pip-01-32/vote-events.jsonl)",
        f"- [Proposal summaries](../../../normalized/governance-votes/pip-01-32/proposal-summaries.json)",
        f"- [Campaign reconciliation](../../../../operations/campaigns/{CAMPAIGN_ID}/reconciliation-report.md)",
        "",
    ])


def import_export(source: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    if sha256(source) != EXPECTED_PACKAGE_SHA256:
        raise ValueError("source ZIP SHA-256 does not match the reviewed package")
    ledger = load_ledger_metadata()
    events: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    member_manifest: list[dict[str, Any]] = []
    all_ids: set[str] = set()
    all_signatures: set[str] = set()

    with zipfile.ZipFile(source) as archive:
        members = {info.filename for info in archive.infolist() if not info.is_dir()}
        if members != EXPECTED_PACKAGE_MEMBERS:
            raise ValueError(f"unexpected ZIP member set: {sorted(members ^ EXPECTED_PACKAGE_MEMBERS)}")
        for pip_number in range(1, 33):
            member_path = f"Star Atlas DAO PIP Votes/PIP-{pip_number:02d}.json"
            info = archive.getinfo(member_path)
            member_bytes = archive.read(member_path)
            member_sha = sha256_bytes(member_bytes)
            rows = json.loads(member_bytes.decode("utf-8-sig"))
            if not isinstance(rows, list) or not rows:
                raise ValueError(f"{member_path} is not a non-empty JSON array")
            expected_keys = {
                "id", "proposalId", "walletPublicKey", "message", "signature", "voteResult",
                "votingPower", "proposalHash", "memoProgramUsed", "createdAt",
            }
            if any(set(row) != expected_keys for row in rows):
                raise ValueError(f"schema mismatch in {member_path}")
            ledger_record = ledger[pip_number]
            if {row["proposalId"] for row in rows} != {ledger_record["proposal_uuid"]}:
                raise ValueError(f"proposal UUID mismatch in {member_path}")
            if len({row["proposalHash"] for row in rows}) != 1:
                raise ValueError(f"multiple proposal hashes in {member_path}")
            normalized = [normalize_record(row, pip_number, ledger_record, member_path, member_sha) for row in rows]
            ids = {row["vote_event_id"] for row in normalized}
            signatures = {row["solana_validation_value"] for row in normalized}
            wallets = {row["wallet_public_key"] for row in normalized}
            if len(ids) != len(normalized) or all_ids.intersection(ids):
                raise ValueError(f"duplicate vote event ID in {member_path}")
            if len(signatures) != len(normalized) or all_signatures.intersection(signatures):
                raise ValueError(f"duplicate validation value in {member_path}")
            if len(wallets) != len(normalized):
                raise ValueError(f"multiple vote events for one wallet in {member_path}")
            all_ids.update(ids)
            all_signatures.update(signatures)
            events.extend(normalized)
            summaries.append(build_summary(pip_number, ledger_record, normalized, member_sha))
            member_manifest.append({
                "pip_id": f"PIP-{pip_number:02d}",
                "member_path": member_path,
                "uncompressed_bytes": info.file_size,
                "compressed_bytes": info.compress_size,
                "zip_member_timestamp": datetime(*info.date_time).isoformat(),
                "timestamp_interpretation": "EXPORT_FILE_TIMESTAMP_NOT_VOTE_DATE",
                "sha256": member_sha,
                "record_count": len(normalized),
                "source_id": source_id(pip_number, member_sha),
            })

        excluded_info = archive.getinfo("Star Atlas DAO PIP Votes/PIP-33.txt")
        excluded_bytes = archive.read(excluded_info)
        excluded_rows = json.loads(excluded_bytes.decode("utf-8-sig"))
        if not isinstance(excluded_rows, list) or len(excluded_rows) != 220:
            raise ValueError("excluded PIP-33 member does not match the reviewed 220-record export")
        excluded_member = {
            "pip_id": "PIP-33",
            "member_path": excluded_info.filename,
            "uncompressed_bytes": excluded_info.file_size,
            "compressed_bytes": excluded_info.compress_size,
            "zip_member_timestamp": datetime(*excluded_info.date_time).isoformat(),
            "timestamp_interpretation": "EXPORT_FILE_TIMESTAMP_NOT_VOTE_DATE",
            "sha256": sha256_bytes(excluded_bytes),
            "record_count": len(excluded_rows),
            "disposition": "EXCLUDED_ALREADY_INGESTED",
            "existing_campaign_id": "pip-33-onchain-vote-reconciliation-2026-07",
        }

    provenance = {
        "campaign_id": CAMPAIGN_ID,
        "package_source_id": PACKAGE_SOURCE_ID,
        "captured_at": CAPTURED_AT,
        "authority": {
            "source_authority_class": "A1",
            "source_type": "OPERATOR_PROVIDED_PRIMARY_BLOCKCHAIN_DERIVED_OFFICIAL_DAO_EXPORT",
            "operator_confirmation": "Valid evidence pulled directly from the Solana blockchain and viewed through the official Star Atlas DAO website.",
            "independent_rpc_reverification_status": "NOT_PERFORMED",
        },
        "source_artifact": {
            "original_filename": source.name,
            "preserved_in_repository": True,
            "repository_path": RAW_REL.as_posix(),
            "sha256": EXPECTED_PACKAGE_SHA256,
            "byte_length": source.stat().st_size,
            "internal_checksum_manifest_present": False,
        },
        "scope": {
            "ingested_pips": [f"PIP-{number:02d}" for number in range(1, 33)],
            "excluded_pips": ["PIP-33"],
            "excluded_reason": "PIP-33 already preserved by pip-33-onchain-vote-reconciliation-2026-07.",
            "vote_event_count": len(events),
        },
        "members": member_manifest,
        "excluded_member": excluded_member,
        "normalization": {
            "raw_decimal_strings_preserved": True,
            "display_rounding": "ROUND_HALF_UP_TO_5_DECIMALS",
            "effective_ballot_rule": "LATEST_PORTAL_RECORD_CREATED_AT_PER_PIP_AND_WALLET",
            "effective_ballot_result": "ONE_EVENT_PER_WALLET_IN_EVERY_SUPPLIED_PIP",
            "timestamp_rule": "PRESERVE_SIGNED_MESSAGE_AND_PORTAL_RECORD_TIMESTAMPS_SEPARATELY",
            "identity_rule": "NO_WALLET_TO_PERSON_IDENTITY_INFERENCE",
            "election_rule": "PRESERVE_ORDERED_BALLOTS; DO_NOT_INFER_STV_WINNERS_WITHOUT TALLY IMPLEMENTATION",
        },
    }
    return events, summaries, provenance


def write_outputs(source: Path, events: list[dict[str, Any]], summaries: list[dict[str, Any]], provenance: dict[str, Any]) -> None:
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != RAW_PATH.resolve():
        shutil.copyfile(source, RAW_PATH)
    write_jsonl(NORMALIZED_ROOT / "vote-events.jsonl", events)
    effective = [
        {
            "pip_id": row["proposal"]["pip_id"],
            "wallet_public_key": row["wallet_public_key"],
            "effective_vote_event_id": row["vote_event_id"],
            "selection_rule": "LATEST_PORTAL_RECORD_CREATED_AT_PER_PIP_AND_WALLET",
            "superseded_event_count": 0,
        }
        for row in events
    ]
    write_jsonl(NORMALIZED_ROOT / "effective-ballots.jsonl", effective)
    write_json(NORMALIZED_ROOT / "proposal-summaries.json", {
        "campaign_id": CAMPAIGN_ID,
        "proposal_count": len(summaries),
        "proposals": summaries,
    })
    write_json(PROVENANCE_PATH, provenance)

    SOURCE_RECORD_ROOT.mkdir(parents=True, exist_ok=True)
    members = {item["pip_id"]: item for item in provenance["members"]}
    for summary in summaries:
        member = members[summary["pip_id"]]
        record = {
            "source_id": summary["source_id"],
            "title": f"{summary['pip_id']} on-chain governance vote export",
            "document_type": "SOLANA_ONCHAIN_GOVERNANCE_VOTE_RECORD_SET",
            "source_type": "operator_provided_primary_blockchain_derived_official_dao_export",
            "publisher": "Solana blockchain; exported through the official Star Atlas DAO website",
            "creator": ["Individual Star Atlas DAO voters"],
            "canonical_url": None,
            "captured_at": CAPTURED_AT,
            "published_at_original": None,
            "published_at_normalized": None,
            "updated_at_original": None,
            "updated_at_normalized": None,
            "authority": {
                "classification": "A1_PRIMARY_BLOCKCHAIN_DERIVED_EVIDENCE",
                "operator_confirmation": "Valid evidence pulled directly from the Solana blockchain and viewed through the official Star Atlas DAO website.",
                "scope": "Ballot-event and vote-result evidence only; not implementation, payment, or post-vote execution evidence.",
                "independent_rpc_reverification_status": "NOT_PERFORMED",
            },
            "provenance": {
                "acquisition_method": "submitted directly by repository operator",
                "package_source_id": PACKAGE_SOURCE_ID,
                "original_package_filename": source.name,
                "original_member_path": member["member_path"],
                "package_sha256": EXPECTED_PACKAGE_SHA256,
                "member_sha256": member["sha256"],
                "source_artifact_preserved": True,
                "source_artifact_path": RAW_REL.as_posix(),
            },
            "quality": {
                "completeness": f"COMPLETE_FOR_SUPPLIED_{summary['pip_id']}_EXPORT",
                "extraction_confidence": "HIGH",
                "manual_review_required": summary["ballot_mechanism"] == "RANKED_CHOICE_ELECTION",
                "limitations": [
                    "Validation payloads are preserved exactly but were not independently replayed against a Solana RPC endpoint.",
                    "The export does not contain transaction IDs, slots, block times, cluster identifiers, RPC endpoints, or an internal checksum manifest.",
                    "Wallet public keys are not inferred to be named people or organizations.",
                    "This vote dataset does not establish proposal implementation, treasury payment, or post-vote execution.",
                    *(["Final STV election tallies and winners are not derived because the tally implementation is not captured in this package."] if summary["ballot_mechanism"] == "RANKED_CHOICE_ELECTION" else []),
                ],
            },
            "source_lineage": {
                "publication": "Solana blockchain / official Star Atlas DAO website",
                "publication_role": "ONCHAIN_VOTE_EVIDENCE",
                "relationship": "RECORDS_BALLOTS_FOR",
                "primary_sources": ["Individual signed Star Atlas DAO ballots"],
                "original_creators": ["Individual Star Atlas DAO voters"],
                "lineage_confidence": "HIGH",
            },
            "artifact_chain": {
                "raw_archive": RAW_REL.as_posix(),
                "normalized_vote_events": (NORMALIZED_ROOT_REL / "vote-events.jsonl").as_posix(),
                "effective_ballots": (NORMALIZED_ROOT_REL / "effective-ballots.jsonl").as_posix(),
                "proposal_summaries": (NORMALIZED_ROOT_REL / "proposal-summaries.json").as_posix(),
                "provenance": PROVENANCE_REL.as_posix(),
                "source_record_json": (SOURCE_RECORD_ROOT_REL / f"{summary['source_id']}.json").as_posix(),
                "source_record_markdown": (SOURCE_RECORD_ROOT_REL / f"{summary['source_id']}.md").as_posix(),
            },
        }
        write_json(SOURCE_RECORD_ROOT / f"{summary['source_id']}.json", record)
        (SOURCE_RECORD_ROOT / f"{summary['source_id']}.md").write_text(markdown_source_record(record, summary), encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    events, summaries, provenance = import_export(args.source)
    write_outputs(args.source, events, summaries, provenance)
    print(f"Imported {len(events)} vote events for PIP-1 through PIP-32; PIP-33 excluded as already ingested")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
