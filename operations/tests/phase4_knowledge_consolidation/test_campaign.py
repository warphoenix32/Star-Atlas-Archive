from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = (
    ROOT
    / "operations/campaigns/phase-4-knowledge-consolidation-2026-07"
    / "validate_campaign.py"
)
SPEC = importlib.util.spec_from_file_location("phase4_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class Phase4KnowledgeConsolidationTests(unittest.TestCase):
    def test_portfolio_has_ten_unique_dossiers(self) -> None:
        payload = json.loads(
            (VALIDATOR.CAMPAIGN / "dossier-portfolio.json").read_text(encoding="utf-8")
        )
        identifiers = [item["dossier_id"] for item in payload["dossiers"]]
        self.assertEqual(10, len(identifiers))
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertFalse(payload["publication_authorized"])

    def test_three_reviewed_evidence_packets_exist(self) -> None:
        paths = sorted((VALIDATOR.CAMPAIGN / "evidence-packets").glob("*.json"))
        self.assertEqual(3, len(paths))
        for path in paths:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("REVIEWED_FOR_KNOWLEDGE_UPDATE", payload["status"])

    def test_publication_manifest_remains_contract_only(self) -> None:
        payload = json.loads(
            (ROOT / "publication/manifests/publication-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual("CONTRACT_ONLY", payload["lifecycle_phase"])
        self.assertEqual([], payload["entries"])


if __name__ == "__main__":
    unittest.main()
