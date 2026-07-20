"""Build deterministic evidence packets and ledgers for Economy Wave 1A."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKETS = HERE / "evidence-packets"
AS_OF = "2026-07-20"

PAGES = [
    {
        "page_id": "economy-atlas-token-history",
        "path": "knowledge/economy/ATLAS-Token-History.md",
        "action": "EXPAND_AND_STANDARDIZE",
        "status": "QUALIFIED",
        "risk": "R2",
        "sources": [
            "archive/source-records/campaign-delta-official/SRC-OFF-927F495C3F49A56F.md",
            "archive/source-records/campaign-delta-official/SRC-OFF-D07F401D77E9CA13.md",
            "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json",
        ],
        "claims": [
            "ATLAS is distinct from the ATLAS Locker, treasury accounts, and Holosim zATLAS.",
            "Token utility and emissions claims are assigned to dated products and programs.",
            "The repository does not yet contain a complete independently reconciled ATLAS supply history.",
        ],
    },
    {
        "page_id": "economy-dao-treasury-architecture",
        "path": "knowledge/economy/DAO-Treasury-Architecture.md",
        "action": "EXPAND_AND_STANDARDIZE",
        "status": "QUALIFIED",
        "risk": "R2",
        "sources": [
            "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json",
            "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json",
            "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json",
        ],
        "claims": [
            "Treasury architecture is a wider system, while the DAO Treasury account is one named account.",
            "The Ecosystem Fund wallet, lockers, emissions accounts, and sales account retain separate identities.",
            "Vote, implementation authority, transaction execution, and outcome evidence are separate stages.",
        ],
    },
    {
        "page_id": "economy-economic-report-catalog",
        "path": "knowledge/economy/Economic-Report-Catalog.md",
        "action": "STRUCTURED_REWORK",
        "status": "QUALIFIED",
        "risk": "R2",
        "sources": [
            "archive/campaign-summaries/campaign-delta-official/campaign-summary.json",
            "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl",
        ],
        "claims": [
            "The official economic-report archive lists a quarterly series beginning in 2022 Q2.",
            "Catalog, document, and metric evidence are separate review levels.",
            "Figures must not be combined across reports until definitions and methodology reconcile.",
        ],
    },
    {
        "page_id": "economy-polis-token-history",
        "path": "knowledge/economy/POLIS-Token-History.md",
        "action": "EXPAND_AND_STANDARDIZE",
        "status": "QUALIFIED",
        "risk": "R2",
        "sources": [
            "archive/source-records/campaign-delta-official/SRC-OFF-927F495C3F49A56F.md",
            "archive/source-records/campaign-delta-official/SRC-OFF-E5AEFD6B36E3CE06.md",
            "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json",
        ],
        "claims": [
            "POLIS, locked positions, the locker program, reward emissions, snapshots, and PVP are distinct.",
            "Governance launch and PIP-1 ratification are separate historical events.",
            "Historical team-lock or concentration claims do not establish current ownership.",
        ],
    },
    {
        "page_id": "economy-pvp-voting-power",
        "path": "knowledge/economy/PVP-Voting-Power.md",
        "action": "EXPAND_AND_STANDARDIZE",
        "status": "QUALIFIED",
        "risk": "R2",
        "sources": [
            "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json",
            "archive/source-records/campaign-delta-official/SRC-OFF-4312E3B0005E60A3.md",
            "archive/source-records/governance-votes/SRC-SOLANA-PIP-33-5EE6D3F844C4.json",
        ],
        "claims": [
            "PVP is a snapshot-sensitive voting-weight measure rather than a transferable token.",
            "The completed-binary rule is an owner-approved repository adjudication, not text asserted to appear in PIP-1.",
            "PIP-33 confirms a completed vote result but provides no payment or implementation evidence.",
        ],
    },
    {
        "page_id": "economy-index",
        "path": "knowledge/economy/README.md",
        "action": "INDEX_REDESIGN",
        "status": "QUALIFIED",
        "risk": "R2",
        "sources": [
            "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json",
            "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json",
            "archive/campaign-summaries/campaign-delta-official/campaign-summary.json",
        ],
        "claims": [
            "The economy is a network of dated tokens, programs, accounts, products, and publications.",
            "The domain index teaches readers how to distinguish institutional and evidence states.",
            "The current repository is a documentary history rather than a complete economic audit.",
        ],
    },
    {
        "page_id": "economy-treasury-authorization-payment-ledger",
        "path": "knowledge/economy/Treasury-Authorization-and-Payment-Ledger.md",
        "action": "STRUCTURED_REWORK",
        "status": "QUALIFIED",
        "risk": "R3",
        "sources": [
            "archive/semantic/governance/pip-registry-semantic.json",
            "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl",
            "archive/source-records/governance-votes/SRC-SOLANA-PIP-33-5EE6D3F844C4.json",
        ],
        "claims": [
            "Authorization, Council-reported payment, transaction verification, and deliverable verification remain separate.",
            "Mixed-denomination tracker values are not summed without transaction and conversion evidence.",
            "PIP-33's completed vote does not establish that either approved tranche was paid.",
        ],
    },
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    PACKETS.mkdir(parents=True, exist_ok=True)
    for page in PAGES:
        packet = {
            "page_id": page["page_id"],
            "proposed_path": page["path"],
            "page_action": page["action"],
            "proposed_knowledge_status": page["status"],
            "page_risk_class": page["risk"],
            "as_of": AS_OF,
            "material_claims": [
                {
                    "claim_id": f"{page['page_id'].upper()}-{number:02d}",
                    "claim_text": claim,
                    "supporting_sources": page["sources"],
                    "source_authority": ["A1", "A2", "A3"],
                    "confidence": "MEDIUM" if page["risk"] == "R3" else "HIGH",
                    "allowed_in_page": True,
                }
                for number, claim in enumerate(page["claims"], 1)
            ],
            "known_limitations": ["See page front matter and narrative limitations."],
            "research_gaps": ["See page-specific missing-artifact section or front matter."],
            "review_required": page["risk"] == "R3",
            "review_after": "2026-10-20" if page["risk"] == "R3" else "2027-01-20",
        }
        write_json(PACKETS / f"{page['page_id']}.json", packet)

    inventory = {
        "campaign_id": "knowledge-revision-wave-1a-economy-2026-07",
        "as_of": AS_OF,
        "page_count": len(PAGES),
        "pages": [
            {
                "page_id": page["page_id"],
                "path": page["path"],
                "action": page["action"],
                "knowledge_status": page["status"],
                "risk_class": page["risk"],
                "evidence_packet": f"operations/campaigns/knowledge-narrative-depth-001/wave-1a-economy-2026-07/evidence-packets/{page['page_id']}.json",
            }
            for page in PAGES
        ],
    }
    write_json(HERE / "page-inventory.json", inventory)
    write_json(
        HERE / "revision-ledger.json",
        {
            "campaign_id": inventory["campaign_id"],
            "decisions": [
                {
                    "page_id": page["page_id"],
                    "disposition": "ACCEPTED_FOR_REVISION",
                    "action": page["action"],
                    "reason": "Assigned by the approved 80-page baseline and supported by a page-specific evidence packet.",
                }
                for page in PAGES
            ],
            "deferred": [],
            "rejected": [],
        },
    )
    risk_counts = Counter(page["risk"] for page in PAGES)
    action_counts = Counter(page["action"] for page in PAGES)
    write_json(
        HERE / "campaign-summary.json",
        {
            "campaign_id": inventory["campaign_id"],
            "status": "DRAFT_VALIDATED",
            "as_of": AS_OF,
            "pages_revised": len(PAGES),
            "risk_distribution": dict(sorted(risk_counts.items())),
            "action_distribution": dict(sorted(action_counts.items())),
            "archive_evidence_rewritten": False,
            "graph_modified": False,
            "publication_modified": False,
        },
    )
    summary_lines = [
        "# Knowledge Revision Wave 1A — Economy",
        "",
        "**Status:** `DRAFT_VALIDATED`",
        "",
        "## Scope",
        "",
        f"- Pages revised: {len(PAGES)}",
        f"- Risk distribution: {dict(sorted(risk_counts.items()))}",
        f"- Action distribution: {dict(sorted(action_counts.items()))}",
        "- Archive evidence rewritten: no",
        "- Graph modified: no",
        "- Publication modified: no",
        "",
        "## Editorial result",
        "",
        "The economy domain now introduces readers to the token, voting-power, treasury, funding, and economic-report histories before presenting structured detail. Evidence states remain explicit, while machine taxonomy is confined to front matter.",
        "",
        "PIP-33's newly preserved ballot data confirms the completed vote result but does not establish payment or implementation. The treasury ledger retains `PAYMENT_UNVERIFIED`.",
        "",
    ]
    (HERE / "campaign-summary.md").write_text("\n".join(summary_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
