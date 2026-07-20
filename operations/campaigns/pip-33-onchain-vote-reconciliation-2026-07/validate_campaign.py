#!/usr/bin/env python3
"""Validate the PIP-33 on-chain vote reconciliation campaign."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import build_campaign as builder


ROOT = builder.ROOT
CAMPAIGN_DIR = builder.CAMPAIGN_DIR
EXPECTED_COUNTS = {"YES": 141, "NO": 59, "ABSTAIN": 20}
EXPECTED_PVP = {"YES": "170240400.01174", "NO": "24857540.34942", "ABSTAIN": "83860459.54910"}
EXPECTED_TOTAL = "278958399.91025"
SIGGY_WALLET = "Ae8AjMQXZsZ7jMWSZTei3ycy4MmvLoPXpDn1w65MrA9U"
BASE64_TRANSACTION_RE = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")
QUANTUM = Decimal("0.00001")


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def parse_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def five(value: str | Decimal) -> str:
    return format(Decimal(value).quantize(QUANTUM, rounding=ROUND_HALF_UP), "f")


def validate() -> dict:
    expected = builder.build_artifacts()
    for relative, content in expected.items():
        path = ROOT / relative
        require(path.is_file(), f"missing generated artifact: {relative}")
        require(path.read_text(encoding="utf-8") == content, f"generated artifact does not reconcile: {relative}")

    events = parse_jsonl(ROOT / builder.VOTE_EVENTS_REL)
    ballots = parse_jsonl(ROOT / builder.EFFECTIVE_BALLOTS_REL)
    summary = json.loads((ROOT / builder.SUMMARY_REL).read_text(encoding="utf-8"))
    provenance = json.loads((ROOT / builder.PROVENANCE_REL).read_text(encoding="utf-8"))
    source_record = json.loads((ROOT / builder.SOURCE_RECORD_JSON_REL).read_text(encoding="utf-8"))
    reconciliation = json.loads((CAMPAIGN_DIR / "reconciliation-report.json").read_text(encoding="utf-8"))
    identity_policy = json.loads((CAMPAIGN_DIR / "identity-and-faction-policy.json").read_text(encoding="utf-8"))
    decisions = json.loads((CAMPAIGN_DIR / "curator-decisions.json").read_text(encoding="utf-8"))

    require(len(events) == 220, "expected 220 normalized vote events")
    require(len({item["vote_event_id"] for item in events}) == 220, "vote-event IDs must be unique")
    require(len({item["wallet_public_key"] for item in events}) == 220, "wallets must be unique in supplied export")
    require(len({item["solana_validation_signature"] for item in events}) == 220, "signatures must be unique")
    require(all(
        (item["signature_field_representation"] == "BASE64_SIGNATURE_BYTES" and len(item["solana_validation_signature"]) == 88 and BASE64_TRANSACTION_RE.fullmatch(item["solana_validation_signature"]))
        or (item["signature_field_representation"] == "BASE64_SIGNED_TRANSACTION_PAYLOAD" and len(item["solana_validation_signature"]) >= 400 and BASE64_TRANSACTION_RE.fullmatch(item["solana_validation_signature"]))
        for item in events
    ), "signature-field representation is invalid")
    require(Counter(item["signature_field_representation"] for item in events) == Counter({"BASE64_SIGNATURE_BYTES": 148, "BASE64_SIGNED_TRANSACTION_PAYLOAD": 72}), "signature-field representation counts do not reconcile")
    require({item["proposal"]["proposal_id"] for item in events} == {"397fee39-fd7c-42be-89e3-169094138257"}, "unexpected proposal ID")
    require({item["proposal"]["proposal_hash"] for item in events} == {"8c9cd4e467"}, "unexpected proposal hash")
    require(Counter(item["vote_result_normalized"] for item in events) == Counter(EXPECTED_COUNTS), "vote counts do not reconcile")
    require(Counter(str(item["memo_program_used"]).lower() for item in events) == Counter({"true": 72, "false": 148}), "memo-program counts do not reconcile")
    require(all(five(item["voting_power_raw"]) == item["voting_power_rounded_5dp"] for item in events), "five-decimal rounding does not reconcile")
    require(all(item["signature_validation_status"] == "NOT_REPLAYED_IN_THIS_CAMPAIGN" for item in events), "signature replay status is overstated")
    require(all(item["source"]["source_artifact_sha256"] == builder.SOURCE_SHA256 for item in events), "source checksum provenance mismatch")

    event_ids = {event["vote_event_id"] for event in events}
    require(len(ballots) == 220, "expected 220 effective ballots")
    require(all(not item["superseded_vote_event_ids"] for item in ballots), "superseded events were not expected in supplied export")
    require(all(item["effective_vote_event_id"] in event_ids for item in ballots), "orphan effective ballot")
    require(summary["ballot_counts"] == {key.lower(): value for key, value in EXPECTED_COUNTS.items()}, "summary ballot counts mismatch")
    require(summary["pvp_rounded_5dp"] == {key.lower(): value for key, value in EXPECTED_PVP.items()}, "summary PVP mismatch")
    require(summary["total_pvp_rounded_5dp"] == EXPECTED_TOTAL, "summary total PVP mismatch")
    require(summary["result"] == "PASSED", "PIP-33 result must be PASSED")
    require(summary["payment_or_implementation_evidence"] is False, "vote evidence must not imply payment or implementation")

    siggy = [item for item in events if item["wallet_public_key"] == SIGGY_WALLET]
    require(len(siggy) == 1, "expected one Siggy wallet ballot")
    require(siggy[0]["identity_enrichment"]["canonical_identity"] == "Siggy", "Siggy identity adjudication missing")
    require(siggy[0]["identity_enrichment"]["identity_attribution_status"] == "HUMAN_VERIFIED", "Siggy identity status mismatch")
    require(all(item["identity_enrichment"]["identity_attribution_status"] == "UNADJUDICATED" for item in events if item["wallet_public_key"] != SIGGY_WALLET), "unreviewed voter identity was inferred")
    require(identity_policy["faction_color_mapping"] == {"blue": "ONI", "red": "MUD", "white_or_uncolored": "NO_FACTION_SELECTED", "yellow": "USTUR"}, "faction color policy mismatch")

    require(reconciliation["result"] == "PASS", "canonical ledger reconciliation failed")
    require(all(item["status"] == "MATCH_AT_5_DECIMALS" for item in reconciliation["items"]), "reconciliation contains a conflict")
    require(reconciliation["canonical_knowledge_modified"] is False, "canonical knowledge must remain untouched")
    require(decisions["open_decision_count"] == 0, "unresolved human decision remains")
    require(len(decisions["decisions"]) == 8, "accepted adjudication count mismatch")
    require(provenance["source_artifact"]["preserved_in_repository"] is False, "raw export preservation decision mismatch")
    require(source_record["quality"]["signature_replay_performed"] is False, "Source Record overstates signature validation")
    require(not (ROOT / "archive/raw/governance-votes/pip-33/PIP-33.txt").exists(), "raw wrapper must remain omitted by operator scope")

    diff = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    require(not any(path == prefix or path.startswith(prefix + "/") for path in diff for prefix in ("knowledge", "graph", "publication")), "forbidden knowledge/graph/publication change detected")
    require(builder.build_artifacts() == builder.build_artifacts(), "campaign build is not deterministic")
    return {
        "campaign_id": builder.CAMPAIGN_ID,
        "result": "PASS",
        "checks": {
            "artifact_reconciliation": "PASS", "json_jsonl_parsing": "PASS", "vote_event_uniqueness": "PASS",
            "wallet_uniqueness": "PASS", "signature_field_representation": "PASS", "signed_message_structural_validation": "PASS_AT_IMPORT",
            "vote_counts_and_pvp": "PASS", "five_decimal_rounding": "PASS", "effective_ballot_reconciliation": "PASS",
            "canonical_ledger_reconciliation": "PASS", "identity_boundary": "PASS", "payment_implementation_boundary": "PASS",
            "deterministic_build": "PASS", "forbidden_paths": "PASS"
        },
        "counts": {"vote_events": 220, "effective_ballots": 220, "unique_wallets": 220, "unique_signatures": 220, "human_verified_identities": 1, "unadjudicated_identities": 219},
        "limitations": [
            "Signatures are retained but not independently replayed in this campaign.",
            "The raw export wrapper is omitted by operator decision.",
            "The dataset does not verify payment, treasury execution, or proposal implementation.",
            "All voter identity mappings except Siggy remain unadjudicated."
        ],
    }


def main() -> int:
    try:
        report = validate()
    except (ValidationFailure, ValueError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    (CAMPAIGN_DIR / "validation-report.json").write_text(builder.dump_json(report), encoding="utf-8", newline="\n")
    markdown = """# Validation Report

**Result: PASS**

- All 220 supplied vote events parse and retain unique event IDs, wallets, and Solana signatures.
- Signed-message wallet, vote, proposal hash, and timestamp structure were checked during import.
- The 220 effective ballots reproduce the supplied YES, NO, and abstain counts and PVP totals.
- The export reconciles with the canonical PIP ledger at five-decimal precision.
- Only the operator-verified Siggy wallet receives a canonical identity attribution.
- Signatures are preserved but were not independently replayed.
- No payment, implementation, or treasury-execution conclusion is made.
- Generated artifacts are deterministic.
- No `knowledge/`, `graph/`, or `publication/` files are changed.
"""
    (CAMPAIGN_DIR / "validation-report.md").write_text(markdown, encoding="utf-8", newline="\n")
    print("PASS PIP-33 on-chain vote reconciliation: 220/220 vote events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
