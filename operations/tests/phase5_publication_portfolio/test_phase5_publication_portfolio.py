from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = (
    ROOT
    / "operations/campaigns/phase-5-foundational-publication-portfolio-2026-07"
    / "validate_campaign.py"
)
SPEC = importlib.util.spec_from_file_location("phase5_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class Phase5PublicationPortfolioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.portfolio = VALIDATOR.load_json(VALIDATOR.PORTFOLIO_PATH)
        self.plan = VALIDATOR.load_json(VALIDATOR.PUBLICATION_PLAN_PATH)
        self.readiness = VALIDATOR.load_json(VALIDATOR.READINESS_PATH)
        self.backlog = VALIDATOR.load_json(VALIDATOR.BACKLOG_PATH)
        self.manifest = VALIDATOR.load_json(VALIDATOR.MANIFEST_PATH)

    def test_editorial_wave_publication_counts(self) -> None:
        failures, metrics = VALIDATOR.validate_manifest(
            self.portfolio, self.manifest
        )
        self.assertEqual([], failures)
        self.assertEqual(14, metrics["entries"])
        self.assertEqual(7, metrics["drafts"])
        self.assertEqual(0, metrics["in_review"])
        self.assertEqual(0, metrics["approved"])
        self.assertEqual(7, metrics["published"])

    def test_articles_are_human_first_and_linked(self) -> None:
        failures, metrics = VALIDATOR.validate_articles(self.portfolio)
        self.assertEqual([], failures)
        self.assertGreaterEqual(metrics["total_words"], 9000)
        self.assertGreaterEqual(metrics["links_checked"], 45)

    def test_community_scope_is_bounded(self) -> None:
        self.assertEqual([], VALIDATOR.validate_community_packet())

    def test_manifest_public_build_contains_only_authorized_articles(self) -> None:
        self.assertEqual(
            ["PUBLISHED"],
            self.manifest["build_policy"]["include_statuses"],
        )
        self.assertTrue(
            all(
                entry["status"] in {"DRAFT", "PUBLISHED"}
                for entry in self.manifest["entries"]
            )
        )
        self.assertEqual(
            7,
            sum(
                entry["status"] == "PUBLISHED"
                for entry in self.manifest["entries"]
            ),
        )
        self.assertTrue(all(
            entry["editorial"]["approval_record"]
            for entry in self.manifest["entries"]
            if entry["status"] == "PUBLISHED"
        ))

    def test_editorial_review_gate_reconciles(self) -> None:
        self.assertEqual(
            [],
            VALIDATOR.validate_editorial_review(self.manifest),
        )

    def test_complete_reader_first_portfolio_map(self) -> None:
        failures, metrics = VALIDATOR.validate_publication_plan(
            self.portfolio,
            self.plan,
            self.readiness,
            self.backlog,
        )
        self.assertEqual([], failures)
        self.assertEqual(8, metrics["reader_gateways"])
        self.assertEqual(30, metrics["foundational_pages_planned"])
        self.assertEqual(11, metrics["prototype_dispositions"])

    def test_public_reader_hides_machine_metadata(self) -> None:
        self.assertEqual([], VALIDATOR.validate_public_presentation())


if __name__ == "__main__":
    unittest.main()
