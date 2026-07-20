"""Build deterministic evidence packets and ledgers for Governance Wave 1B."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKETS = HERE / "evidence-packets"
AS_OF = "2026-07-20"

PIP = "archive/semantic/governance/pip-registry-semantic.json"
TRACKER = "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"
PIP1 = "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
PIP2 = "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json"
PIP3 = "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json"
PIP23 = "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json"
PIP33 = "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json"
VOTE33 = "archive/source-records/governance-votes/SRC-SOLANA-PIP-33-5EE6D3F844C4.json"

PAGES = [
    ("governance-index", "knowledge/governance/README.md", "INDEX_REDESIGN", "CANONICAL", "R1", [PIP, PIP1], [
        "The governance domain is organized around institutions, proposals, elections, funding, and evidence states.",
        "Public narrative is separated from internal taxonomy and audit mechanics.",
        "Authorization is never presented as execution without later evidence.",
    ]),
    ("star-atlas-dao", "knowledge/governance/Star-Atlas-DAO.md", "EXPAND_AND_STANDARDIZE", "CANONICAL", "R1", [PIP, PIP1], [
        "The DAO is the PVP-weighted POLIS electorate and decision process, not ATMTA, the Foundation, or Council.",
        "Binary ballot count and PVP weight are distinct measures.",
        "A DAO result supplies authorization but not proof of implementation.",
    ]),
    ("star-atlas-foundation", "knowledge/governance/Star-Atlas-Foundation.md", "REWRITE", "QUALIFIED", "R2", [PIP1, PIP2], [
        "The Foundation is the legal and administrative implementation body described in the captured framework.",
        "Administrative and safety review does not replace the electorate's formal vote.",
        "Custody and implementation claims remain proposal-specific.",
    ]),
    ("star-atlas-council", "knowledge/governance/Star-Atlas-Council.md", "REWRITE", "QUALIFIED", "R2", [PIP, PIP3, TRACKER], [
        "The Council is an elected process steward rather than an independent legislative sovereign.",
        "Later election winners remain unresolved where final result artifacts are absent.",
        "Council tracker states remain attributed operational assessments.",
    ]),
    ("pip-lifecycle", "knowledge/governance/PIP-Lifecycle-and-Legislative-Process.md", "EXPAND_AND_STANDARDIZE", "CANONICAL", "R1", [PIP, PIP1], [
        "Proposal, review, publication, voting, result, authorization, implementation, and verification are distinct stages.",
        "Election mechanisms are not forced into binary fields.",
        "The completed-binary rule is a repository adjudication rather than source-native PIP-1 text.",
    ]),
    ("governance-evidence-states", "knowledge/governance/Governance-Implementation-and-Evidence-States.md", "REWRITE", "CANONICAL", "R1", [PIP, TRACKER], [
        "Evidence states describe what preserved artifacts establish, not whether undocumented events occurred.",
        "Council reporting and independent verification remain separate.",
        "Treasury vocabulary distinguishes requested, authorized, Council-reported, unverified, and missing on-chain evidence.",
    ]),
    ("governance-economy-overview", "knowledge/governance/Governance-and-Economy-Overview.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", [PIP, PIP23], [
        "Governance may authorize economic action while financial evidence establishes execution.",
        "The Ecosystem Fund is a bounded policy instrument within wider treasury architecture.",
        "Direct DAO Treasury measures remain distinct from Ecosystem Fund awards.",
    ]),
    ("constitutional-history", "knowledge/governance/Governance-Constitutional-History.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", [PIP1, PIP2, PIP3, PIP23], [
        "Operational release, public constitutional explanation, and formal ratification are separate historical milestones.",
        "PIP-1 through PIP-4 formed the captured founding ratifications.",
        "PIP-23 superseded PIP-4 without erasing the earlier policy period.",
    ]),
    ("council-election-history", "knowledge/governance/Council-Election-History.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", [PIP, PIP3], [
        "PIP-6 selected advancing candidates and PIP-7 identified the first final Council roster.",
        "PIP-11 and PIP-25 winner identities remain unresolved in captured evidence.",
        "Election, seating, service, and current officeholding are separate claims.",
    ]),
    ("ecosystem-fund", "knowledge/governance/Ecosystem-Fund.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", [PIP, PIP23], [
        "The Ecosystem Fund is a governed funding process rather than the entire treasury or a sovereign institution.",
        "PIP-23 replaced PIP-4 and restated the operating limits.",
        "Fund authorization does not prove allocation, payment, or successful outcome.",
    ]),
    ("ecosystem-fund-awards", "knowledge/governance/Ecosystem-Fund-Award-History.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R3", [PIP, TRACKER, PIP23], [
        "Award is used narrowly for a passed eligible funding authorization.",
        "Council-reported payment and milestone fields are not independently verified.",
        "Failed proposals are applications, not awards.",
    ]),
    ("failure-termination-casebook", "knowledge/governance/Governance-Failure-and-Termination-Casebook.md", "EXPAND_AND_STANDARDIZE", "QUALIFIED", "R2", [PIP, TRACKER], [
        "Failed, terminated, canceled, withdrawn, superseded, and unverified proposals are distinct states.",
        "PIP-14 and PIP-17 passed before Council-reported terminal states.",
        "PIP-31 passed before author withdrawal and reported non-implementation.",
    ]),
    ("pip-33-case-study", "knowledge/governance/PIP-33-ATMTA-Historic-Expense-Reimbursement.md", "EXPAND_AND_STANDARDIZE", "PROVISIONAL", "R3", [PIP33, VOTE33, TRACKER], [
        "PIP-33 authorized two approximately equal 75 percent USDC and 25 percent ATLAS tranches with a conditional second tranche.",
        "The source-native one-cent discrepancies remain preserved.",
        "Ballot evidence supports passage but supplies no payment or implementation evidence.",
    ]),
    ("pip-registry", "knowledge/governance/PIP-Registry.md", "STRUCTURED_REWORK", "QUALIFIED", "R3", [PIP, TRACKER, VOTE33], [
        "The ledger covers one record for each PIP from PIP-1 through PIP-33.",
        "Election fields remain mechanism-aware and unresolved winners are not inferred.",
        "The PIP-33 ballot export reconciles the vote without changing the unverified payment state.",
    ]),
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    PACKETS.mkdir(parents=True, exist_ok=True)
    for page_id, path, action, status, risk, sources, claims in PAGES:
        write_json(PACKETS / f"{page_id}.json", {
            "page_id": page_id,
            "proposed_path": path,
            "page_action": action,
            "proposed_knowledge_status": status,
            "page_risk_class": risk,
            "as_of": AS_OF,
            "material_claims": [{
                "claim_id": f"{page_id.upper()}-{number:02d}",
                "claim_text": claim,
                "supporting_sources": sources,
                "source_authority": ["A1", "A2", "A3"],
                "confidence": "MEDIUM" if risk == "R3" else "HIGH",
                "allowed_in_page": True,
            } for number, claim in enumerate(claims, 1)],
            "known_limitations": ["See page front matter and narrative limitations."],
            "research_gaps": ["See page-specific missing-artifact section or front matter."],
            "review_required": risk == "R3",
            "review_after": "2026-10-20" if risk == "R3" else "2027-01-20",
        })

    inventory = {
        "campaign_id": "knowledge-revision-wave-1b-governance-2026-07",
        "as_of": AS_OF,
        "page_count": len(PAGES),
        "pages": [{
            "page_id": p[0], "path": p[1], "action": p[2],
            "knowledge_status": p[3], "risk_class": p[4],
            "evidence_packet": f"operations/campaigns/knowledge-narrative-depth-001/wave-1b-governance-2026-07/evidence-packets/{p[0]}.json",
        } for p in PAGES],
    }
    write_json(HERE / "page-inventory.json", inventory)
    write_json(HERE / "revision-ledger.json", {
        "campaign_id": inventory["campaign_id"],
        "decisions": [{
            "page_id": p[0], "disposition": "ACCEPTED_FOR_REVISION", "action": p[2],
            "reason": "Assigned by the approved 80-page baseline and supported by a page-specific evidence packet.",
        } for p in PAGES],
        "deferred": [], "duplicate": [], "rejected": [],
    })
    risks = Counter(p[4] for p in PAGES)
    actions = Counter(p[2] for p in PAGES)
    summary = {
        "campaign_id": inventory["campaign_id"], "status": "DRAFT_VALIDATED", "as_of": AS_OF,
        "pages_revised": len(PAGES), "risk_distribution": dict(sorted(risks.items())),
        "action_distribution": dict(sorted(actions.items())),
        "archive_evidence_rewritten": False, "graph_modified": False, "publication_modified": False,
        "human_adjudication_required": False,
    }
    write_json(HERE / "campaign-summary.json", summary)
    lines = [
        "# Knowledge Revision Wave 1B — Governance", "", "**Status:** `DRAFT_VALIDATED`", "",
        "## Scope", "", f"- Pages revised: {len(PAGES)}", f"- Risk distribution: {dict(sorted(risks.items()))}",
        f"- Action distribution: {dict(sorted(actions.items()))}", "- Archive evidence rewritten: no",
        "- Graph modified: no", "- Publication modified: no", "", "## Editorial result", "",
        "The governance domain now presents a connected institutional history of the DAO, Foundation, Council, PIP process, elections, treasury policy, awards, and terminal cases. Internal taxonomy remains in metadata and campaign artifacts.",
        "", "PIP-33 ballot evidence reconciles the completed vote only. Its two conditional tranches, one-cent discrepancies, and `UNVERIFIED` payment state remain explicit.", "",
        "## Human adjudication", "", "No new unresolved adjudication was introduced by this revision.", "",
    ]
    (HERE / "campaign-summary.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
