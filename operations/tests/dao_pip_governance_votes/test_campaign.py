import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = ROOT / "operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07"


class DaoPipGovernanceVotesTest(unittest.TestCase):
    def test_campaign_validation(self):
        result = subprocess.run(
            [sys.executable, str(HERE / "validate_campaign.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_pip_33_is_excluded(self):
        summaries = json.loads(
            (ROOT / "archive/normalized/governance-votes/pip-01-32/proposal-summaries.json").read_text(encoding="utf-8")
        )["proposals"]
        self.assertEqual([item["pip_number"] for item in summaries], list(range(1, 33)))

    def test_ranked_elections_are_not_forced_binary(self):
        summaries = json.loads(
            (ROOT / "archive/normalized/governance-votes/pip-01-32/proposal-summaries.json").read_text(encoding="utf-8")
        )["proposals"]
        elections = {item["pip_number"] for item in summaries if item["ballot_mechanism"] == "RANKED_CHOICE_ELECTION"}
        self.assertEqual(elections, {6, 7, 11, 25, 27})
        for item in summaries:
            if item["pip_number"] in elections:
                self.assertIsNone(item["binary_result"])
                self.assertFalse(item["election_result"]["winner_inference_performed"])


if __name__ == "__main__":
    unittest.main()
