"""Generate the reviewed Wave 2A evidence packets."""

from __future__ import annotations

import json
from pathlib import Path


OUT = Path(__file__).resolve().parent
PIP = "archive/semantic/governance/pip-registry-semantic.json"
PIP_SRC = "archive/source-records/social-governance-semantic-enrichment/governance/"
OFF = "archive/source-records/campaign-delta-official/"
AB = "archive/semantic/atlas-brew/segment-index.json"
SNAP = "knowledge/gameplay/Official-Current-State-Snapshot-2026-07-12.md"


def claim(cid, text, ctype, state, sources, authority, confidence="HIGH", limitation=None):
    return {
        "claim_id": cid,
        "claim_text": text,
        "claim_type": ctype,
        "temporal_scope": "as of 2026-07-15" if ctype == "CURRENT_STATE" else "historical/institutional",
        "lifecycle_state": state,
        "supporting_sources": sources,
        "source_authority": authority,
        "corroboration_status": "DIRECT_PRIMARY" if "A1" in authority or "A2" in authority else "ATTRIBUTED",
        "contradiction_status": "NONE_IDENTIFIED" if not limitation else limitation,
        "attribution_required": "A3" in authority or "B2" in authority,
        "confidence": confidence,
        "allowed_in_page": True,
    }


PAGES = [
    ("pip-registry", "knowledge/governance/PIP-Registry.md", "EXPAND", "QUALIFIED", 6, ["Star Atlas DAO", "PIPs"], [
        claim("PIPREG-1", "The captured corpus contains 33 numbered PIPs with proposal and vote states kept separate.", "REGISTRY_SCOPE", "HISTORICAL", [PIP, PIP_SRC], ["A1"]),
        claim("PIPREG-2", "Council-reported lifecycle and payment fields are attributed assessments, not independent verification.", "EVIDENCE_QUALIFICATION", "UNKNOWN", [PIP], ["A3"]),
    ]),
    ("star-atlas-dao", "knowledge/governance/Star-Atlas-DAO.md", "CREATE", "CANONICAL", 3, ["Star Atlas DAO", "POLIS"], [
        claim("DAO-1", "PIP-1 defines the DAO as the program-based system through which persons locking and voting POLIS form consensus.", "INSTITUTIONAL_ROLE", "LIVE", [PIP, PIP_SRC + "SRC-PIP-01-BC8475E4.json"], ["A1"]),
        claim("DAO-2", "A passing vote is not itself evidence that an approved action was implemented.", "EVIDENCE_RULE", "UNKNOWN", [PIP], ["A1"]),
    ]),
    ("star-atlas-foundation", "knowledge/governance/Star-Atlas-Foundation.md", "CREATE", "QUALIFIED", 5, ["Star Atlas Foundation"], [
        claim("FOUND-1", "PIP-1 assigns proposal-compliance review and advancement duties to the Foundation or a delegated administrator.", "INSTITUTIONAL_ROLE", "LIVE", [PIP_SRC + "SRC-PIP-01-BC8475E4.json"], ["A1"]),
        claim("FOUND-2", "The Foundation's implementation discretion is bounded by legal, safety, compliance, and public-reasoning language in the captured governance text.", "INSTITUTIONAL_BOUNDARY", "LIVE", [PIP_SRC + "SRC-PIP-01-BC8475E4.json"], ["A1"], "MEDIUM"),
    ]),
    ("star-atlas-council", "knowledge/governance/Star-Atlas-Council.md", "CREATE", "QUALIFIED", 6, ["Star Atlas Council"], [
        claim("COUNCIL-1", "The Council is an elected governance-process steward rather than a separate legislative sovereign.", "INSTITUTIONAL_ROLE", "LIVE", [PIP, PIP_SRC + "SRC-PIP-03-F5E7CDE1.json"], ["A1"]),
        claim("COUNCIL-2", "Council tracker lifecycle, milestone, and payment statements require Council attribution and lack independent verification unless another primary record is cited.", "EVIDENCE_QUALIFICATION", "UNKNOWN", [PIP], ["A3"]),
    ]),
    ("ecosystem-fund", "knowledge/governance/Ecosystem-Fund.md", "CREATE", "QUALIFIED", 6, ["Ecosystem Fund", "Star Atlas DAO", "Star Atlas Council"], [
        claim("FUND-1", "PIP-23 continues the Ecosystem Fund, replaces PIP-4, and establishes a 20% treasury budget subject to its terms.", "GOVERNANCE_POLICY", "UPDATED", [PIP, PIP_SRC + "SRC-PIP-23-0ECF2928.json"], ["A1"]),
        claim("FUND-2", "Approval of a grant proposal remains separate from payment, milestone acceptance, and completed delivery.", "EVIDENCE_RULE", "UNKNOWN", [PIP], ["A1", "A3"]),
        claim("FUND-3", "PIP-23 requires funding requests to be denominated in USDC, payments in ATLAS, a 5% last-refill-balance ceiling, and a maximum 12-month duration.", "GOVERNANCE_POLICY", "LIVE", [PIP_SRC + "SRC-PIP-23-0ECF2928.json"], ["A1"]),
    ]),
    ("pip-lifecycle", "knowledge/governance/PIP-Lifecycle-and-Legislative-Process.md", "CREATE", "CANONICAL", 3, ["PIPs", "Star Atlas DAO"], [
        claim("LIFE-1", "The captured PIP-1 process distinguishes drafting, administrative review, pending publication, voting, result, and implementation.", "PROCESS", "LIVE", [PIP_SRC + "SRC-PIP-01-BC8475E4.json"], ["A1"]),
        claim("LIFE-2", "Election rounds and proposal votes require mechanism-specific interpretation.", "PROCESS", "LIVE", [PIP], ["A1"]),
    ]),
    ("governance-evidence-states", "knowledge/governance/Governance-Implementation-and-Evidence-States.md", "CREATE", "CANONICAL", 3, ["PIPs", "evidence states"], [
        claim("EVID-1", "Proposal, vote, passage, announced implementation, execution, payment, and verified completion are distinct evidence states.", "EVIDENCE_MODEL", "LIVE", [PIP], ["A1", "A3"]),
        claim("EVID-2", "Council operational assessments are attributable records and do not constitute independent verification.", "EVIDENCE_MODEL", "UNKNOWN", [PIP], ["A3"]),
    ]),
    ("governance-economy-overview", "knowledge/governance/Governance-and-Economy-Overview.md", "EXPAND", "QUALIFIED", 5, ["Star Atlas DAO", "POLIS", "Ecosystem Fund"], [
        claim("GEO-1", "POLIS voting authority and treasury policy connect governance decisions to economic administration.", "INSTITUTIONAL_RELATIONSHIP", "LIVE", [PIP], ["A1"]),
        claim("GEO-2", "Economic proposals must keep requested funding, approval, payment, and outcome separate.", "EVIDENCE_RULE", "UNKNOWN", [PIP], ["A1", "A3"]),
    ]),
    ("governance-index", "knowledge/governance/README.md", "EXPAND", "CANONICAL", 2, ["governance knowledge domain"], [
        claim("GOVINDEX-1", "The governance knowledge domain separates institutions, process, evidence states, registry, and economic policy.", "INFORMATION_ARCHITECTURE", "LIVE", [PIP], ["A1"]),
    ]),
    ("institutional-overview", "knowledge/organizations/Institutional-Overview.md", "EXPAND", "QUALIFIED", 5, ["ATMTA", "Star Atlas DAO", "Star Atlas Foundation", "Star Atlas Council"], [
        claim("INST-1", "ATMTA, the DAO, Foundation, and Council are related but distinct institutional actors.", "INSTITUTIONAL_RELATIONSHIP", "LIVE", [PIP, OFF], ["A1", "A2"]),
        claim("INST-2", "Governance procedure belongs in governance pages; this page records identity and relationships.", "SCOPE_RULE", "LIVE", [PIP], ["A1"]),
    ]),
    ("atmta", "knowledge/organizations/ATMTA.md", "CREATE", "QUALIFIED", 5, ["ATMTA, Inc.", "Star Atlas"], [
        claim("ATMTA-1", "ATMTA is the operating company identified in official Star Atlas publications and product records.", "ORGANIZATION_IDENTITY", "LIVE", [OFF, SNAP], ["A2"]),
        claim("ATMTA-2", "ATMTA's product-development role does not make it identical to the DAO, Foundation, or Council.", "INSTITUTIONAL_BOUNDARY", "LIVE", [PIP, OFF], ["A1", "A2"]),
    ]),
    ("organizations-index", "knowledge/organizations/README.md", "EXPAND", "CANONICAL", 2, ["organization knowledge domain"], [
        claim("ORGINDEX-1", "The organization index links identities to governance pages without duplicating procedural authority.", "INFORMATION_ARCHITECTURE", "LIVE", [PIP, OFF], ["A1", "A2"]),
    ]),
    ("product-registry", "knowledge/gameplay/Product-Registry.md", "EXPAND", "QUALIFIED", 5, ["Star Atlas products"], [
        claim("PRODREG-1", "Product lifecycle labels are evidence-qualified and date-bound.", "REGISTRY_RULE", "LIVE", [OFF, AB, SNAP], ["A2", "B1"]),
        claim("PRODREG-2", "Roadmap, testing, release, and delivery are not interchangeable.", "EVIDENCE_RULE", "UNKNOWN", [OFF, AB], ["A2", "B1"]),
    ]),
    ("score-faction-fleet", "knowledge/gameplay/SCORE-and-Faction-Fleet.md", "CREATE", "HISTORICAL", 6, ["SCORE", "Faction Fleet"], [
        claim("SCORE-1", "SCORE/Faction Fleet was an asset-management and emissions program exposed through PLAY.", "PRODUCT_IDENTITY", "HISTORICAL", [OFF + "SRC-OFF-0333A5B22A207D88.md", SNAP], ["A2"]),
        claim("SCORE-2", "Aephia reported that Faction Fleet ATLAS emissions ended in April 2024; this remains attributed community chronology rather than direct transaction proof.", "LIFECYCLE_EVENT", "DEPRECATED", ["archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-19357309E964FAF8.md"], ["B2"], "MEDIUM"),
    ]),
    ("sage", "knowledge/gameplay/SAGE.md", "CREATE", "QUALIFIED", 5, ["SAGE", "SAGE Labs", "Starbased"], [
        claim("SAGE-1", "Official support material documents SAGE Labs as a browser-based, on-chain 4X economic strategy surface.", "PRODUCT_IDENTITY", "LIVE", [OFF + "SRC-OFF-0A646AE069AFFBA5.md"], ["A2"]),
        claim("SAGE-2", "The 2022 renamed-SAGE roadmap is planning evidence, not proof that later SAGE phases were delivered.", "LIFECYCLE_EVENT", "PLANNED", [OFF + "SRC-OFF-22181D98D7A1B870.md"], ["A2"]),
    ]),
    ("ue5-showroom", "knowledge/gameplay/UE5-Showroom.md", "CREATE", "QUALIFIED", 5, ["Unreal Engine 5 game", "Showroom"], [
        claim("UE5-1", "Official records present the Unreal Engine 5 client as an early-access, evolving game surface.", "PRODUCT_IDENTITY", "TESTING", [SNAP, OFF], ["A2"]),
        claim("UE5-2", "Roadmap feature lists and test events do not establish general delivery of every described feature.", "EVIDENCE_RULE", "UNKNOWN", [OFF, AB], ["A2", "B1"]),
    ]),
    ("galactic-marketplace", "knowledge/gameplay/Galactic-Marketplace.md", "CREATE", "QUALIFIED", 4, ["Galactic Marketplace", "PLAY"], [
        claim("MARKET-1", "Official product records identify the Galactic Marketplace as a trading surface for Star Atlas assets.", "PRODUCT_IDENTITY", "LIVE", [SNAP, OFF], ["A2"]),
        claim("MARKET-2", "Marketplace availability does not independently verify individual trades, liquidity, or economic outcomes.", "EVIDENCE_LIMIT", "UNKNOWN", [OFF], ["A2"]),
    ]),
    ("gameplay-index", "knowledge/gameplay/README.md", "EXPAND", "CANONICAL", 2, ["gameplay knowledge domain"], [
        claim("GAMEINDEX-1", "The gameplay index distinguishes product identity, lifecycle history, and current-state snapshots.", "INFORMATION_ARCHITECTURE", "LIVE", [SNAP, OFF], ["A2"]),
    ]),
]


def main():
    for page_id, path, action, status, score, entities, claims in PAGES:
        packet = {
            "page_id": page_id,
            "proposed_path": path,
            "page_action": action,
            "proposed_knowledge_status": status,
            "page_risk_score": score,
            "page_risk_class": "R1" if score <= 3 else "R2" if score <= 6 else "R3",
            "subject_entities": entities,
            "aliases": [],
            "scope": "Foundation synthesis constrained to evidence available on main as of 2026-07-15.",
            "material_claims": claims,
            "known_limitations": ["Current-state statements are date-bound.", "Absence of evidence is not evidence of non-occurrence."],
            "research_gaps": ["Independent execution evidence remains incomplete where explicitly noted."],
            "review_required": True,
            "review_after": "2027-01-15" if status in {"QUALIFIED", "HISTORICAL"} else "2027-07-15",
        }
        (OUT / f"{page_id}.json").write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
