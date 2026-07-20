"""Build deterministic Wave 3C review artifacts."""
from __future__ import annotations
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKETS = HERE / "evidence-packets"
CAMPAIGN_ID = "knowledge-narrative-depth-wave-3c-indexes-registries-2026-07"
PAGES = [
    ("knowledge/index/Entity-Registry.md", "STRUCTURED_REWORK", "QUALIFIED", "R2", "Stable identity without broad lifecycle collapse."),
    ("knowledge/index/README.md", "INDEX_REDESIGN", "CANONICAL", "R1", "Human-first index-domain navigation."),
    ("knowledge/index/source-registry/Audited-Community-Source-Profiles.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", "Audited community source identities and claim-level boundaries."),
    ("knowledge/index/source-registry/Community-Content-URL-Inventory-2026-07-12.md", "STRUCTURED_REWORK", "HISTORICAL", "R2", "Static Discord-derived URL discovery snapshot."),
    ("knowledge/index/source-registry/Official-Newsroom-Extraction-Batch-001.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", "Selected official article extractions without corpus claims."),
    ("knowledge/index/source-registry/Official-Newsroom-Index.md", "STRUCTURED_REWORK", "QUALIFIED", "R2", "Captured newsroom chronology with explicit date-range limits."),
    ("knowledge/index/source-registry/Public-Source-Registry.md", "STRUCTURED_REWORK", "QUALIFIED", "R2", "Source-family authority, coverage, and completeness vocabulary."),
]


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def pid(path: str) -> str:
    return "KNOW-" + hashlib.sha256(path.encode()).hexdigest()[:16].upper()


def main() -> None:
    PACKETS.mkdir(parents=True, exist_ok=True)
    inventory = []
    ledger = []
    for path_text, action, status, risk, scope in PAGES:
        path = ROOT / path_text
        identifier = pid(path_text)
        raw_name = path.parent.name + "-README" if path.stem == "README" else path.stem
        name = (raw_name if len(raw_name) <= 36 else raw_name[:24] + "-" + identifier[-8:]) + ".json"
        sources = ["knowledge/index/source-registry/Public-Source-Registry.md"]
        if path_text.endswith("Entity-Registry.md"):
            sources = ["knowledge/gameplay/Product-Registry.md", "archive/normalized/lore/taxonomy.json"]
        elif "Community-Content" in path_text:
            sources = ["archive/normalized/manifests/normalized-urls.jsonl"]
        elif "Newsroom" in path_text:
            sources = ["archive/campaign-summaries/campaign-delta-official/campaign-summary.json"]
        packet = {
            "campaign_id": CAMPAIGN_ID,
            "page_id": identifier,
            "proposed_path": path_text,
            "page_action": action,
            "proposed_knowledge_status": status,
            "page_risk_score": 2 if risk == "R1" else 5,
            "page_risk_class": risk,
            "subject_entities": [], "aliases": [], "scope": scope,
            "material_claims": [{"claim_id": identifier + "-C01", "claim_text": scope, "claim_type": "REGISTRY_SCOPE", "temporal_scope": "AS_OF_2026-07-20", "lifecycle_state": "UNKNOWN", "supporting_sources": sources, "source_authority": "MIXED_A2_B2", "corroboration_status": "QUALIFIED", "contradiction_status": "NONE_IDENTIFIED", "attribution_required": True, "confidence": "HIGH" if risk == "R1" else "MEDIUM", "allowed_in_page": True}],
            "known_limitations": ["Registry inclusion does not establish source completeness, current lifecycle, or claim truth."],
            "research_gaps": ["See page-specific identity, source, and coverage gaps."],
            "review_required": True, "review_after": "2027-01-20",
        }
        dump(PACKETS / name, packet)
        normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        inventory.append({"page_id": identifier, "path": path_text, "action": action, "knowledge_status": status, "risk_class": risk, "word_count": len(re.findall(r"\b[\w'-]+\b", normalized)), "sha256_utf8_lf": hashlib.sha256(normalized.encode()).hexdigest()})
        ledger.append({"page_id": identifier, "path": path_text, "disposition": "ACCEPTED", "reason": scope, "human_review_required": True})
    dump(HERE / "page-inventory.json", {"campaign_id": CAMPAIGN_ID, "page_count": 7, "pages": inventory})
    dump(HERE / "revision-ledger.json", {"campaign_id": CAMPAIGN_ID, "accepted": 7, "deferred": 0, "duplicate": 0, "rejected": 0, "records": ledger})
    dump(HERE / "campaign-summary.json", {"campaign_id": CAMPAIGN_ID, "status": "READY_FOR_REVIEW", "pages_revised": 7, "pages_created": 0, "risk_distribution": dict(sorted(Counter(row[3] for row in PAGES).items())), "knowledge_status_distribution": dict(sorted(Counter(row[2] for row in PAGES).items())), "archive_evidence_rewritten": False, "semantic_evidence_rewritten": False, "graph_modified": False, "publication_modified": False})
    (HERE / "campaign-summary.md").write_text("# Knowledge Narrative Depth Wave 3C\n\n**Status:** `READY_FOR_REVIEW`\n\nSeven identity and source indexes were revised. Broad entity-registry lifecycle labels were removed, and the Medium source-family status was corrected.\n\n- Risk: R1 = 1; R2 = 6\n- Knowledge status: CANONICAL = 1; HISTORICAL = 1; QUALIFIED = 5\n- Archive, semantic, graph, and publication changes: none\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
