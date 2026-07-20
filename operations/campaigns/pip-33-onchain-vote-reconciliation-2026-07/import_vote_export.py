#!/usr/bin/env python3
"""Import an operator-provided PIP-33 vote export into normalized JSONL."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


CAMPAIGN_ID = "pip-33-onchain-vote-reconciliation-2026-07"
SOURCE_ID = "SRC-SOLANA-PIP-33-5EE6D3F844C4"
EXPECTED_SHA256 = "5ee6d3f844c4932db1195429aa191fe7c6ae21087c12520d636ebe3a4d8dfacb"
EXPECTED_PROPOSAL_ID = "397fee39-fd7c-42be-89e3-169094138257"
EXPECTED_PROPOSAL_HASH = "8c9cd4e467"
SIGGY_WALLET = "Ae8AjMQXZsZ7jMWSZTei3ycy4MmvLoPXpDn1w65MrA9U"
ROOT = Path(__file__).resolve().parents[3]
OUTPUT_REL = Path("archive/normalized/governance-votes/pip-33/vote-events.jsonl")
OUTPUT_PATH = ROOT / OUTPUT_REL
ROUNDING_QUANTUM = Decimal("0.00001")
MESSAGE_PATTERN = re.compile(
    r"^I (?P<wallet>\S+) vote (?P<vote>\S+) to PIP-33 with hash (?P<hash>\S+) "
    r"on (?P<timestamp>\S+) with (?P<locked_polis>[0-9.]+) POLIS locked until (?P<lock_until>\d+)$"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def round_five(value: str) -> str:
    return format(Decimal(value).quantize(ROUNDING_QUANTUM, rounding=ROUND_HALF_UP), "f")


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def normalize(record: dict[str, Any]) -> dict[str, Any]:
    message_match = MESSAGE_PATTERN.fullmatch(record["message"])
    if message_match is None:
        raise ValueError(f"unrecognized signed message for vote {record.get('id')}")
    message = message_match.groupdict()
    if message["wallet"] != record["walletPublicKey"]:
        raise ValueError(f"message wallet mismatch for vote {record['id']}")
    if message["vote"].lower() != record["voteResult"].lower():
        raise ValueError(f"message result mismatch for vote {record['id']}")
    if message["hash"] != record["proposalHash"]:
        raise ValueError(f"message proposal hash mismatch for vote {record['id']}")

    created = parse_timestamp(record["createdAt"])
    signed = parse_timestamp(message["timestamp"])
    lock_until = int(message["lock_until"])
    wallet = record["walletPublicKey"]
    return {
        "vote_event_id": record["id"],
        "schema_version": "1.0.0",
        "record_type": "solana_governance_vote_event",
        "network": "Solana",
        "proposal": {
            "pip_id": "PIP-33",
            "proposal_id": record["proposalId"],
            "proposal_hash": record["proposalHash"],
            "title": "ATMTA Historic Expense Reimbursement",
            "ballot_mechanism": "BINARY_PVP_WITH_ABSTAIN",
        },
        "wallet_public_key": wallet,
        "vote_result_raw": record["voteResult"],
        "vote_result_normalized": record["voteResult"].upper(),
        "voting_power_raw": record["votingPower"],
        "voting_power_rounded_5dp": round_five(record["votingPower"]),
        "signed_message": record["message"],
        "ballot_signed_at": message["timestamp"],
        "index_record_created_at": record["createdAt"],
        "index_minus_signed_seconds": format(Decimal(str((created - signed).total_seconds())).quantize(Decimal("0.001")), "f"),
        "locked_polis_raw": message["locked_polis"],
        "lock_expires_unix": lock_until,
        "lock_expires_at": datetime.fromtimestamp(lock_until, timezone.utc).isoformat().replace("+00:00", "Z"),
        "solana_validation_signature": record["signature"],
        "signature_semantics": "SOLANA_BLOCKCHAIN_VALIDATION_SIGNATURE",
        "signature_field_representation": "BASE64_SIGNED_TRANSACTION_PAYLOAD" if bool(record["memoProgramUsed"]) else "BASE64_SIGNATURE_BYTES",
        "signature_validation_status": "NOT_REPLAYED_IN_THIS_CAMPAIGN",
        "memo_program_used": bool(record["memoProgramUsed"]),
        "identity_enrichment": {
            "display_name_observed": "Siggy" if wallet == SIGGY_WALLET else None,
            "canonical_identity": "Siggy" if wallet == SIGGY_WALLET else None,
            "identity_attribution_status": "HUMAN_VERIFIED" if wallet == SIGGY_WALLET else "UNADJUDICATED",
            "adjudication_authority": "REPOSITORY_OPERATOR" if wallet == SIGGY_WALLET else None,
            "profile_selected_faction": None,
            "faction_evidence_status": "NOT_PRESENT_IN_ONCHAIN_EXPORT",
        },
        "source": {
            "source_id": SOURCE_ID,
            "source_type": "OPERATOR_PROVIDED_ONCHAIN_VOTE_EXPORT",
            "source_artifact_sha256": EXPECTED_SHA256,
            "raw_export_preservation": "OMITTED_BY_OPERATOR_SCOPE",
            "onchain_evidence_status": "ONCHAIN_VALIDATABLE",
        },
    }


def import_export(source: Path) -> list[dict[str, Any]]:
    if sha256(source) != EXPECTED_SHA256:
        raise ValueError("source SHA-256 does not match the reviewed PIP-33 export")
    payload = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or len(payload) != 220:
        raise ValueError("expected a 220-record JSON array")
    records = [normalize(item) for item in payload]
    if len({item["vote_event_id"] for item in records}) != 220:
        raise ValueError("vote event IDs are not unique")
    if {item["proposal"]["proposal_id"] for item in records} != {EXPECTED_PROPOSAL_ID}:
        raise ValueError("unexpected proposal ID")
    if {item["proposal"]["proposal_hash"] for item in records} != {EXPECTED_PROPOSAL_HASH}:
        raise ValueError("unexpected proposal hash")
    return records


def write_jsonl(records: list[dict[str, Any]]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in records)
    OUTPUT_PATH.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    records = import_export(args.source)
    write_jsonl(records)
    print(f"Imported {len(records)} PIP-33 on-chain vote events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
