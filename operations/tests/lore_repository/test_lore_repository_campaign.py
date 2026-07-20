import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN_DIR = ROOT / "operations" / "campaigns" / "lore-repository-ingestion-2026-07"


def load_validator():
    sys.path.insert(0, str(CAMPAIGN_DIR))
    spec = importlib.util.spec_from_file_location("lore_repository_validate", CAMPAIGN_DIR / "validate_campaign.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class LoreRepositoryCampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()
        cls.report = cls.validator.validate()

    def test_campaign_validation_passes(self):
        failures = [item for item in self.report["checks"] if not item["passed"]]
        self.assertEqual([], failures)

    def test_expected_corpus_dimensions(self):
        self.assertEqual(192, self.report["summary"]["source_pages"])
        self.assertEqual(4632, self.report["summary"]["entities"])
        self.assertEqual(3798, self.report["summary"]["relationships"])

    def test_curator_adjudications_and_redactions_pass(self):
        checks = {item["name"]: item for item in self.report["checks"]}
        self.assertTrue(checks["human_review_register_curator_adjudicated"]["passed"])
        self.assertTrue(checks["oni_css_historical_snapshot_not_current_taxonomy"]["passed"])
        self.assertTrue(checks["workstation_paths_redacted_from_normalized_and_public_derivatives"]["passed"])


if __name__ == "__main__":
    unittest.main()
