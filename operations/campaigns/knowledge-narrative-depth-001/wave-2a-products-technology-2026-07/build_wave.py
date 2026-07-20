"""Build deterministic review artifacts for knowledge narrative depth Wave 2A."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKET_DIR = HERE / "evidence-packets"
CAMPAIGN_ID = "knowledge-narrative-depth-wave-2a-products-technology-2026-07"

PAGES = [
    {
        "path": "knowledge/gameplay/Galactic-Marketplace.md",
        "action": "REWRITE",
        "status": "QUALIFIED",
        "risk": "R2",
        "scope": "Marketplace identity, 2021 and 2022 surface succession, current access, and operational evidence boundary.",
        "claims": [
            ["K2A-MKT-001", "ATMTA published a release claim for the 2021 Galactic Marketplace on 2021-08-04.", "RELEASE_CLAIM", ["archive/source-records/campaign-delta-official/SRC-OFF-A465C97640C55838.md"]],
            ["K2A-MKT-002", "ATMTA introduced a new replacement marketplace on 2022-07-22.", "PRODUCT_SUCCESSION", ["archive/source-records/campaign-delta-official/SRC-OFF-0C5AA46E01E189EC.md"]],
            ["K2A-MKT-003", "Official late-2025 support records documented order and fee workflows for the later marketplace surface.", "DOCUMENTATION_STATE", ["archive/source-records/campaign-delta-official/SRC-OFF-1EE2242A6F7844FF.md", "archive/source-records/campaign-delta-official/SRC-OFF-B38AFD8A2122994F.md"]],
        ],
    },
    {
        "path": "knowledge/gameplay/UE5-Showroom.md",
        "action": "REWRITE",
        "status": "QUALIFIED",
        "risk": "R2",
        "scope": "Showroom pre-alpha and R2.1 build history, current Unreal-client boundary, and later-lineage gaps.",
        "claims": [
            ["K2A-UE5-001", "ATMTA published a UE5 Showroom pre-alpha release claim on 2022-09-30.", "RELEASE_CLAIM", ["archive/source-records/campaign-delta-official/SRC-OFF-C6B9C26055452AF8.md"]],
            ["K2A-UE5-002", "Showroom R2.1 was announced as a named release on 2023-06-02.", "PRODUCT_UPDATE", ["archive/source-records/campaign-delta-official/SRC-OFF-FC61779037A23908.md"]],
            ["K2A-UE5-003", "Atlas Brew discussions remain useful for recording-and-timestamp discovery without supporting named attribution where the speaker is unknown.", "EVIDENCE_BOUNDARY", ["archive/semantic/atlas-brew/segment-index.json"]],
        ],
    },
    {
        "path": "knowledge/technology/Technical-Platform.md",
        "action": "REWRITE",
        "status": "QUALIFIED",
        "risk": "R2",
        "scope": "Human-readable platform architecture and the distinction among documentation, source, deployment, integration, operation, and verification.",
        "claims": [
            ["K2A-TECH-001", "Official documentation identifies multiple Solana programs and game IDs as distinct technical surfaces.", "TECHNICAL_DESCRIPTION", ["archive/source-records/campaign-delta-official/SRC-OFF-F217B64FD0342839.md"]],
            ["K2A-TECH-002", "Official decoder support does not by itself prove current mainnet deployment.", "EVIDENCE_BOUNDARY", ["archive/source-records/campaign-delta-official/SRC-OFF-B3E826AFA52FB19B.md"]],
            ["K2A-TECH-003", "Official June 2026 support records establish C4 as a public test surface, not a general release.", "TESTING_STATE", ["archive/source-records/campaign-delta-official/SRC-OFF-E061D3A6454697AB.md", "archive/source-records/campaign-delta-official/SRC-OFF-952AB5D6D09DD6BF.md"]],
        ],
    },
    {"path": "knowledge/gameplay/Holosim.md", "action": "EXPAND_AND_STANDARDIZE", "status": "QUALIFIED", "risk": "R2", "scope": "SEO, review date, and preservation of the existing build-qualified history.", "claims": []},
    {"path": "knowledge/gameplay/Official-Current-State-Snapshot-2026-07-12.md", "action": "EXPAND_AND_STANDARDIZE", "status": "HISTORICAL", "risk": "R1", "scope": "Standard metadata and an explicit single-date official-positioning boundary.", "claims": []},
    {"path": "knowledge/gameplay/Product-Registry.md", "action": "STRUCTURED_REWORK", "status": "QUALIFIED", "risk": "R2", "scope": "Reader guidance, SEO, review status, and narrow lifecycle rows.", "claims": []},
    {"path": "knowledge/gameplay/README.md", "action": "INDEX_REDESIGN", "status": "CANONICAL", "risk": "R1", "scope": "Human-first navigation and lifecycle-language explanation.", "claims": []},
    {"path": "knowledge/gameplay/SAGE.md", "action": "EXPAND_AND_STANDARDIZE", "status": "QUALIFIED", "risk": "R2", "scope": "SEO and review status while retaining surface-specific SAGE lineage.", "claims": []},
    {"path": "knowledge/gameplay/SCORE-and-Faction-Fleet.md", "action": "EXPAND_AND_STANDARDIZE", "status": "HISTORICAL", "risk": "R2", "scope": "SEO and current review date while retaining announced-versus-executed deprecation distinctions.", "claims": []},
    {"path": "knowledge/technology/Official-Technical-Surface-Inventory.md", "action": "EXPAND_AND_STANDARDIZE", "status": "QUALIFIED", "risk": "R2", "scope": "SEO and reader-facing evidence notes for the detailed program registry.", "claims": []},
    {"path": "knowledge/technology/README.md", "action": "INDEX_REDESIGN", "status": "CANONICAL", "risk": "R1", "scope": "Human-first technical-domain navigation and evidence ladder.", "claims": []},
]


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def canonical_bytes(path: Path) -> bytes:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")


def page_id(path: str) -> str:
    return "KNOW-" + hashlib.sha256(path.encode()).hexdigest()[:16].upper()


def words(path: Path) -> int:
    return len(re.findall(r"\b[\w'-]+\b", path.read_text(encoding="utf-8")))


def main() -> None:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    inventory, ledger = [], []
    for item in PAGES:
        path = ROOT / item["path"]
        pid = page_id(item["path"])
        claims = []
        for claim_id, text, claim_type, sources in item["claims"]:
            claims.append({
                "claim_id": claim_id,
                "claim_text": text,
                "claim_type": claim_type,
                "temporal_scope": "DATE_BOUND",
                "lifecycle_state": "AS_STATED",
                "supporting_sources": sources,
                "source_authority": "A2",
                "corroboration_status": "SOURCE_LINKED",
                "contradiction_status": "NONE_IDENTIFIED",
                "attribution_required": True,
                "confidence": "HIGH",
                "allowed_in_page": True,
            })
        packet = {
            "campaign_id": CAMPAIGN_ID,
            "page_id": pid,
            "proposed_path": item["path"],
            "page_action": item["action"],
            "proposed_knowledge_status": item["status"],
            "page_risk_score": {"R1": 2, "R2": 5}[item["risk"]],
            "page_risk_class": item["risk"],
            "subject_entities": [],
            "aliases": [],
            "scope": item["scope"],
            "material_claims": claims,
            "known_limitations": ["Page-level metadata and prose retain their own claim-specific limitations."],
            "research_gaps": ["See the page's research-gaps metadata and missing-artifacts section."],
            "review_required": True,
            "review_after": "2027-01-20",
        }
        packet_name = f"{path.parent.name}-README.json" if path.stem == "README" else f"{path.stem}.json"
        dump(PACKET_DIR / packet_name, packet)
        inventory.append({
            "page_id": pid,
            "path": item["path"],
            "domain": item["path"].split("/")[1],
            "action": item["action"],
            "knowledge_status": item["status"],
            "risk_class": item["risk"],
            "word_count": words(path),
            "sha256_utf8_lf": hashlib.sha256(canonical_bytes(path)).hexdigest(),
        })
        ledger.append({"page_id": pid, "path": item["path"], "disposition": "ACCEPTED", "reason": item["scope"], "human_review_required": True})

    dump(HERE / "page-inventory.json", {"campaign_id": CAMPAIGN_ID, "page_count": len(inventory), "pages": inventory})
    dump(HERE / "revision-ledger.json", {"campaign_id": CAMPAIGN_ID, "accepted": len(ledger), "deferred": 2, "duplicate": 0, "rejected": 0, "records": ledger, "deferred_pages": [
        {"path": "knowledge/gameplay/Fleet-Command.md", "reason": "Dedicated build and release evidence packet remains incomplete."},
        {"path": "knowledge/gameplay/C4.md", "reason": "PTR evidence exists, but successor identity and general-release history remain incomplete."},
    ]})
    distribution = Counter(item["risk"] for item in PAGES)
    statuses = Counter(item["status"] for item in PAGES)
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "status": "READY_FOR_REVIEW",
        "pages_revised": len(PAGES),
        "pages_created": 0,
        "substantive_rewrites": 3,
        "indexes_redesigned": 2,
        "risk_distribution": dict(sorted(distribution.items())),
        "knowledge_status_distribution": dict(sorted(statuses.items())),
        "archive_evidence_rewritten": False,
        "semantic_evidence_rewritten": False,
        "graph_modified": False,
        "publication_modified": False,
    }
    dump(HERE / "campaign-summary.json", summary)
    (HERE / "campaign-summary.md").write_text("\n".join([
        "# Knowledge Narrative Depth Wave 2A", "", "**Status:** `READY_FOR_REVIEW`", "",
        "Eleven existing gameplay and technology pages were revised. The Galactic Marketplace, UE5 Showroom, and Technical Platform received substantive historian-oriented rewrites; two domain indexes were redesigned; six strong pages were standardized without weakening their evidence boundaries.", "",
        "- Pages revised: 11", "- New knowledge pages: 0", "- Risk: R1 = 3; R2 = 8", "- Status: CANONICAL = 2; HISTORICAL = 2; QUALIFIED = 7", "- Deferred standalone pages: Fleet Command and C4", "",
        "No archive, semantic, graph, or publication artifact was rewritten.", "",
    ]), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
