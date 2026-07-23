from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = (
    ROOT
    / "operations/campaigns/phase-3-publication-contract-2026-07"
    / "validate_campaign.py"
)
SPEC = importlib.util.spec_from_file_location("publication_contract_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class PublicationContractTests(unittest.TestCase):
    def test_checked_in_manifest_is_valid(self) -> None:
        payload = json.loads(
            (ROOT / "publication/manifests/publication-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], VALIDATOR.validate_manifest(payload))

    def test_duplicate_slug_is_rejected(self) -> None:
        payload = json.loads(
            (ROOT / "operations/schema/examples/publication-manifest-v1.json").read_text(
                encoding="utf-8"
            )
        )
        duplicate = copy.deepcopy(payload["entries"][0])
        duplicate["publication_id"] = "PUB-SAGE-PRODUCT-HISTORY-SECOND"
        payload["entries"].append(duplicate)
        failures = VALIDATOR.validate_manifest(payload)
        self.assertIn("duplicate slug", failures)

    def test_published_entry_requires_editorial_and_evidence_approval(self) -> None:
        payload = json.loads(
            (ROOT / "operations/schema/examples/publication-manifest-v1.json").read_text(
                encoding="utf-8"
            )
        )
        payload["entries"][0]["status"] = "PUBLISHED"
        failures = VALIDATOR.validate_manifest(payload)
        self.assertTrue(any("approved content_path" in failure for failure in failures))
        self.assertTrue(any("editorial approvals" in failure for failure in failures))
        self.assertTrue(any("evidence review" in failure for failure in failures))

    def test_freshness_queue_is_byte_identical(self) -> None:
        self.assertEqual(
            VALIDATOR.FRESHNESS_BLOB_SHA256,
            hashlib.sha256(
                VALIDATOR.git_blob("HEAD", VALIDATOR.FRESHNESS_REPOSITORY_PATH)
            ).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
