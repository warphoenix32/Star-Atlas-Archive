import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ENTITY_TYPES = {
    "PERSON", "ORGANIZATION", "DAO", "CORPORATION", "TOKEN", "FEATURE",
    "TECHNOLOGY", "GAME_SYSTEM", "GAME_MODE", "SHIP", "LOCATION",
    "RESOURCE", "EVENT", "DOCUMENT", "PRODUCT", "COMMUNITY", "GUILD",
}
LIFECYCLE = {
    "ANNOUNCED", "PLANNED", "IN_DEVELOPMENT", "IN_TESTING", "RELEASED",
    "LIVE", "DEPRECATED", "CANCELLED", "SUPERSEDED",
}


def validate_package(package):
    schema = package.get("metadata", {}).get("repository_schema")
    if schema not in {"2.0", "2.1"}:
        raise ValueError("unsupported repository schema")
    if not isinstance(package.get("sources"), list):
        raise ValueError("sources must be a list")
    for key in ("entities", "claims", "events", "quotes", "relationships", "timeline_updates", "research_tasks"):
        if key in package and not isinstance(package[key], list):
            raise ValueError(f"{key} must be a list")
    if schema == "2.1":
        for entity in package.get("entities", []):
            if "canonical_name" not in entity:
                raise ValueError("v2.1 entities require canonical_name")
            if entity.get("entity_type") not in ENTITY_TYPES:
                raise ValueError("invalid entity_type")
        for claim in package.get("claims", []):
            if claim.get("status") and claim["status"] not in LIFECYCLE:
                raise ValueError("invalid claim lifecycle")
            provenance = claim.get("provenance")
            if provenance is not None:
                required = {"source_id", "speaker", "timestamp_start", "timestamp_end", "confidence"}
                if not required.issubset(provenance):
                    raise ValueError("incomplete provenance")
    return True


class SchemaCompatibilityTests(unittest.TestCase):
    def test_v20_remains_valid(self):
        package = {
            "metadata": {"repository_schema": "2.0"},
            "sources": [],
            "entities": [{"entity_id": "ENT-OLD", "name": "Legacy Entity"}],
            "claims": [],
            "events": [],
            "quotes": [],
            "relationships": [],
            "timeline_updates": [],
            "research_tasks": [],
        }
        self.assertTrue(validate_package(package))

    def test_v21_example_is_valid(self):
        path = ROOT / "operations" / "schema" / "examples" / "ingestion-package-v2.1.json"
        package = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(validate_package(package))

    def test_unknown_schema_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_package({"metadata": {"repository_schema": "3.0"}, "sources": []})


if __name__ == "__main__":
    unittest.main()
