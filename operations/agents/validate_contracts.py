#!/usr/bin/env python3
"""Validate the repository-local agent contract set."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "contracts.json"
REQUIRED_ROLES = {
    "LEAD_COORDINATOR": "ALL",
    "ARCHIVE_STEWARD": "PRESERVE",
    "KNOWLEDGE_CURATOR": "DRAFT",
    "RISK_REVIEW_AGENT": "REVIEW",
    "LIBRARY_PUBLISHER": "PUBLISH",
}


def main() -> int:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert payload["contract_version"] == "1.0"
    assert payload["pipeline"] == ["PRESERVE", "DRAFT", "REVIEW", "PUBLISH"]
    assert payload["merge_authority"] == "HUMAN_OR_BRANCH_PROTECTION"
    assert payload["human_review_as_arises"] is True

    roles = {role["role_id"]: role for role in payload["roles"]}
    assert set(roles) == set(REQUIRED_ROLES)
    for role_id, stage in REQUIRED_ROLES.items():
        role = roles[role_id]
        assert role["stage"] == stage
        contract = ROOT / role["contract"]
        assert contract.is_file(), f"missing contract for {role_id}: {contract.name}"
        text = contract.read_text(encoding="utf-8")
        assert "## Mission" in text
        assert "Do not merge" in text or "merge" in text.lower()

    for key in ("shared_contract", "specialist_registry"):
        assert (ROOT / payload[key]).is_file(), f"missing {key}"

    authoring = payload["knowledge_authoring"]
    assert all(authoring[key] is True for key in ("human_first", "engaging", "comprehensive", "narrative_required"))
    assert authoring["seo_mode"] == "ETHICAL_DISCOVERY"
    assert authoring["inline_machine_taxonomy"] == "PROHIBITED_BY_DEFAULT"
    assert set(authoring["public_taxonomy_placement"]) == {"HIDDEN_FRONT_MATTER", "CONSOLIDATED_SECTION"}

    curator = (ROOT / roles["KNOWLEDGE_CURATOR"]["contract"]).read_text(encoding="utf-8")
    publisher = (ROOT / roles["LIBRARY_PUBLISHER"]["contract"]).read_text(encoding="utf-8")
    for phrase in ("Human-first authoring standard", "Search and discovery standard", "Taxonomy presentation"):
        assert phrase in curator
    assert "Hide YAML front matter" in publisher
    assert "paragraph-level machine-taxonomy clutter" in publisher

    print(f"PASS agent-contracts: {len(roles)} core roles; four-stage boundary; human-first knowledge standard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
