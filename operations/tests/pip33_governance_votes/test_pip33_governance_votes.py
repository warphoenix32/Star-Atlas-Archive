#!/usr/bin/env python3
"""Unit tests for PIP-33 governance vote reconciliation."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = ROOT / "operations/campaigns/pip-33-onchain-vote-reconciliation-2026-07"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


builder = load_module("pip33_builder", CAMPAIGN / "build_campaign.py")


class Pip33VoteCampaignTests(unittest.TestCase):
    def test_deterministic_artifacts(self) -> None:
        self.assertEqual(builder.build_artifacts(), builder.build_artifacts())

    def test_summary_and_reconciliation(self) -> None:
        artifacts = builder.build_artifacts()
        summary = json.loads(artifacts[builder.SUMMARY_REL.as_posix()])
        reconciliation = json.loads(artifacts[f"operations/campaigns/{builder.CAMPAIGN_ID}/reconciliation-report.json"])
        self.assertEqual(summary["vote_event_count"], 220)
        self.assertEqual(summary["effective_ballot_count"], 220)
        self.assertEqual(summary["ballot_counts"], {"abstain": 20, "no": 59, "yes": 141})
        self.assertEqual(summary["total_pvp_rounded_5dp"], "278958399.91025")
        self.assertEqual(summary["result"], "PASSED")
        self.assertFalse(summary["payment_or_implementation_evidence"])
        self.assertEqual(reconciliation["result"], "PASS")

    def test_identity_boundary(self) -> None:
        events = builder.load_jsonl(ROOT / builder.VOTE_EVENTS_REL)
        verified = [event for event in events if event["identity_enrichment"]["identity_attribution_status"] == "HUMAN_VERIFIED"]
        self.assertEqual(len(verified), 1)
        self.assertEqual(verified[0]["identity_enrichment"]["canonical_identity"], "Siggy")
        self.assertEqual(verified[0]["wallet_public_key"], "Ae8AjMQXZsZ7jMWSZTei3ycy4MmvLoPXpDn1w65MrA9U")


if __name__ == "__main__":
    unittest.main()
