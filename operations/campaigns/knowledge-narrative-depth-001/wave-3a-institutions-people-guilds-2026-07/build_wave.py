"""Build deterministic Wave 3A review artifacts."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKETS = HERE / "evidence-packets"
CAMPAIGN_ID = "knowledge-narrative-depth-wave-3a-institutions-people-guilds-2026-07"

PAGES = [
    {
        "path": "knowledge/organizations/ATMTA.md",
        "action": "REWRITE",
        "status": "QUALIFIED",
        "risk": "R2",
        "scope": "ATMTA operating and publishing role without merging company, DAO, Foundation, or Council identity.",
        "sources": ["archive/source-records/campaign-delta-official/", "archive/semantic/governance/pip-registry-semantic.json"],
    },
    {
        "path": "knowledge/organizations/Institutional-Overview.md",
        "action": "REWRITE",
        "status": "QUALIFIED",
        "risk": "R2",
        "scope": "Institutional map separating company, governance, administration, Council, and treasury mechanisms.",
        "sources": ["archive/semantic/governance/pip-registry-semantic.json", "knowledge/governance/Governance-Constitutional-History.md"],
    },
    {
        "path": "knowledge/organizations/Organization-and-Role-Registry.md",
        "action": "STRUCTURED_REWORK",
        "status": "QUALIFIED",
        "risk": "R2",
        "scope": "Institution, role, office, delegation, and current-state distinctions.",
        "sources": ["archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json", "knowledge/index/Entity-Registry.md"],
    },
    {
        "path": "knowledge/organizations/README.md",
        "action": "INDEX_REDESIGN",
        "status": "CANONICAL",
        "risk": "R1",
        "scope": "Human-first organization-domain navigation.",
        "sources": ["knowledge/organizations/Institutional-Overview.md", "knowledge/organizations/Organization-and-Role-Registry.md"],
    },
    {
        "path": "knowledge/guilds/Guild-Master-Index.md",
        "action": "STRUCTURED_REWORK",
        "status": "QUALIFIED",
        "risk": "R2",
        "scope": "Guild identities, tags, faction relationships, and operator-confirmed context without inferred current membership.",
        "sources": ["operations/campaigns/discord-community-indexing-001/alias-registry.json", "operations/campaigns/discord-community-indexing-001/curator-decisions.json"],
    },
    {
        "path": "knowledge/guilds/README.md",
        "action": "INDEX_REDESIGN",
        "status": "CANONICAL",
        "risk": "R1",
        "scope": "Human-first guild-domain navigation and evidence standard.",
        "sources": ["knowledge/guilds/Guild-Master-Index.md"],
    },
    {
        "path": "knowledge/people/Actor-Master-Index.md",
        "action": "STRUCTURED_REWORK",
        "status": "QUALIFIED",
        "risk": "R2",
        "scope": "People, aliases, dated roles, transcript attribution limits, and reviewed operator decisions.",
        "sources": ["operations/campaigns/discord-community-indexing-001/alias-registry.json", "operations/campaigns/discord-community-indexing-001/curator-decisions.json"],
    },
    {
        "path": "knowledge/people/Krigs-Source-Profile.md",
        "action": "REWRITE",
        "status": "QUALIFIED",
        "risk": "R2",
        "scope": "Krigs and the distinct HNN, Hologram, archive-site, and personal publication identities.",
        "sources": ["archive/source-records/campaign-charlie-hnn/", "knowledge/media/Community-Publication-Relationship-Index.md"],
    },
    {
        "path": "knowledge/people/README.md",
        "action": "INDEX_REDESIGN",
        "status": "CANONICAL",
        "risk": "R1",
        "scope": "Human-first people-domain navigation and attribution boundaries.",
        "sources": ["knowledge/people/Actor-Master-Index.md"],
    },
]

RISK_SCORE = {"R1": 2, "R2": 5, "R3": 7}


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()


def page_id(path: str) -> str:
    return "KNOW-" + hashlib.sha256(path.encode()).hexdigest()[:16].upper()


def packet_name(path: Path) -> str:
    return (path.parent.name + "-README" if path.stem == "README" else path.stem) + ".json"


def main() -> None:
    PACKETS.mkdir(parents=True, exist_ok=True)
    inventory = []
    ledger = []
    for page in PAGES:
        path = ROOT / page["path"]
        identifier = page_id(page["path"])
        claim = {
            "claim_id": identifier + "-C01",
            "claim_text": page["scope"],
            "claim_type": "INSTITUTIONAL_DESCRIPTION",
            "temporal_scope": "AS_OF_2026-07-20",
            "lifecycle_state": "UNKNOWN",
            "supporting_sources": page["sources"],
            "source_authority": "MIXED_A2_B2_OPERATOR_CONFIRMATION_WHERE_EXPLICIT",
            "corroboration_status": "QUALIFIED",
            "contradiction_status": "NONE_IDENTIFIED",
            "attribution_required": True,
            "confidence": "HIGH" if page["risk"] == "R1" else "MEDIUM",
            "allowed_in_page": True,
        }
        packet = {
            "campaign_id": CAMPAIGN_ID,
            "page_id": identifier,
            "proposed_path": page["path"],
            "page_action": page["action"],
            "proposed_knowledge_status": page["status"],
            "page_risk_score": RISK_SCORE[page["risk"]],
            "page_risk_class": page["risk"],
            "subject_entities": [],
            "aliases": [],
            "scope": page["scope"],
            "material_claims": [claim],
            "known_limitations": ["Current roles and relationships are not inferred from historical appearances."],
            "research_gaps": ["See the page's dated role, identity, and evidence-acquisition gaps."],
            "review_required": True,
            "review_after": "2027-01-20",
        }
        dump(PACKETS / packet_name(path), packet)
        inventory.append({
            "page_id": identifier,
            "path": page["path"],
            "action": page["action"],
            "knowledge_status": page["status"],
            "risk_class": page["risk"],
            "word_count": len(re.findall(r"\b[\w'-]+\b", path.read_text(encoding="utf-8"))),
            "sha256_utf8_lf": hashlib.sha256(normalized_bytes(path)).hexdigest(),
        })
        ledger.append({
            "page_id": identifier,
            "path": page["path"],
            "disposition": "ACCEPTED",
            "reason": page["scope"],
            "human_review_required": True,
        })

    dump(HERE / "page-inventory.json", {"campaign_id": CAMPAIGN_ID, "page_count": len(inventory), "pages": inventory})
    dump(HERE / "revision-ledger.json", {"campaign_id": CAMPAIGN_ID, "accepted": 9, "deferred": 0, "duplicate": 0, "rejected": 0, "records": ledger})
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "status": "READY_FOR_REVIEW",
        "pages_revised": 9,
        "pages_created": 0,
        "risk_distribution": dict(sorted(Counter(page["risk"] for page in PAGES).items())),
        "knowledge_status_distribution": dict(sorted(Counter(page["status"] for page in PAGES).items())),
        "archive_evidence_rewritten": False,
        "semantic_evidence_rewritten": False,
        "graph_modified": False,
        "publication_modified": False,
    }
    dump(HERE / "campaign-summary.json", summary)
    (HERE / "campaign-summary.md").write_text(
        "# Knowledge Narrative Depth Wave 3A\n\n"
        "**Status:** `READY_FOR_REVIEW`\n\n"
        "Nine organization, guild, and people pages were revised. Operator-confirmed identity context remains visibly separate from archive evidence.\n\n"
        "- Risk: R1 = 3; R2 = 6\n"
        "- Knowledge status: CANONICAL = 3; QUALIFIED = 6\n"
        "- New knowledge pages: 0\n"
        "- Archive, semantic, graph, and publication changes: none\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()

