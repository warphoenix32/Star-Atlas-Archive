import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTRACTS = ROOT / "operations" / "agents"


class AgentContractTests(unittest.TestCase):
    def test_contract_validator(self):
        result = subprocess.run(
            [sys.executable, str(CONTRACTS / "validate_contracts.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_manifest_preserves_human_publication_boundary(self):
        payload = json.loads((CONTRACTS / "contracts.json").read_text(encoding="utf-8"))
        authoring = payload["knowledge_authoring"]
        self.assertTrue(authoring["human_first"])
        self.assertTrue(authoring["narrative_required"])
        self.assertEqual(authoring["inline_machine_taxonomy"], "PROHIBITED_BY_DEFAULT")
        self.assertEqual(payload["merge_authority"], "HUMAN_OR_BRANCH_PROTECTION")


if __name__ == "__main__":
    unittest.main()
