"""Build deterministic evidence packets and ledgers for Narrative Depth Campaign 001."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PACKETS = HERE / "evidence-packets"
AS_OF = "2026-07-17"

SPECS = [
    {
        "id": "governance-constitutional-history", "path": "knowledge/governance/Governance-Constitutional-History.md", "action": "CREATE", "status": "QUALIFIED", "risk": (6, "R2"),
        "sources": ["archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json"],
        "claims": ["Governance developed through operational release, public design, formal ratification, and later amendments rather than one founding event.", "PIP-1, PIP-2, and PIP-3 establish distinct DAO, Foundation, and Council roles.", "PIP-23 supersedes PIP-4 without erasing the earlier policy history."],
    },
    {
        "id": "council-election-history", "path": "knowledge/governance/Council-Election-History.md", "action": "CREATE", "status": "QUALIFIED", "risk": (6, "R2"),
        "sources": ["archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-06-1B792551.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-07-91652743.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-11-7B48A62D.json"],
        "claims": ["PIP-6 identifies first-round advancing candidates rather than elected members.", "PIP-7 identifies the five final first-Council winners.", "Later Council-election winners remain unresolved in the captured portal records."],
    },
    {
        "id": "governance-failure-casebook", "path": "knowledge/governance/Governance-Failure-and-Termination-Casebook.md", "action": "CREATE", "status": "QUALIFIED", "risk": (6, "R2"),
        "sources": ["archive/semantic/governance/pip-registry-semantic.json", "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"],
        "claims": ["Failed PIPs supply no implementation authority.", "PIPs 14 and 17 passed before Council-reported termination or cancellation.", "PIP-31 passed before author withdrawal and reported non-implementation."],
    },
    {
        "id": "treasury-authorization-payment-ledger", "path": "knowledge/economy/Treasury-Authorization-and-Payment-Ledger.md", "action": "CREATE", "status": "QUALIFIED", "risk": (8, "R3"),
        "sources": ["archive/semantic/governance/pip-registry-semantic.json", "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json"],
        "claims": ["Proposal passage and Council-reported payment are separate evidence states.", "Mixed ATLAS and USDC tracker values cannot be summed without transaction reconciliation.", "PIP-33 is a direct DAO Treasury authorization whose payment remains unverified.", "PIP-33 displays two approximately equal USD 234,756.76 tranches, each composed of USD 176,067.57 USDC (75%) and USD 58,689.19 in ATLAS-equivalent value (25%); tranche 2 is scheduled 180 days later and reserve-conditional. The two displayed tranche totals sum to USD 469,513.52 rather than the stated USD 469,513.53 total, and their USDC portions sum to USD 352,135.14 rather than the stated USD 352,135.15 USDC total."],
    },
    {
        "id": "ecosystem-fund-award-history", "path": "knowledge/governance/Ecosystem-Fund-Award-History.md", "action": "CREATE", "status": "QUALIFIED", "risk": (7, "R3"),
        "sources": ["archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json", "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"],
        "claims": ["An award is defined as a passed eligible authorization rather than payment or completion.", "Failed applications are excluded from the award registry.", "PIP-23 is policy and PIP-33 is a direct treasury measure, so neither is a recipient award."],
    },
    {
        "id": "atlas-token-history", "path": "knowledge/economy/ATLAS-Token-History.md", "action": "CREATE", "status": "QUALIFIED", "risk": (5, "R2"),
        "sources": ["archive/source-records/campaign-delta-official/SRC-OFF-927F495C3F49A56F.md", "archive/source-records/campaign-delta-official/SRC-OFF-0333A5B22A207D88.md", "archive/source-records/campaign-delta-official/SRC-OFF-D07F401D77E9CA13.md"],
        "claims": ["Historical sale terms are source-dated and not present-supply facts.", "ATLAS token, ATLAS Locker, DAO Treasury holdings, and Holosim zATLAS are distinct.", "Official emissions and utility statements do not replace an on-chain supply and transaction history."],
    },
    {
        "id": "polis-token-history", "path": "knowledge/economy/POLIS-Token-History.md", "action": "CREATE", "status": "QUALIFIED", "risk": (5, "R2"),
        "sources": ["archive/source-records/campaign-delta-official/SRC-OFF-927F495C3F49A56F.md", "archive/source-records/campaign-delta-official/SRC-OFF-E5AEFD6B36E3CE06.md", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"],
        "claims": ["POLIS token, locked positions, POLIS Locker, snapshots, reward emissions, and PVP are distinct.", "The DAO/POLIS-locking release predates formal PIP-1 ratification.", "Historical PVP concentration statements are not current ownership evidence."],
    },
    {
        "id": "sage-product-family-history", "path": "knowledge/gameplay/SAGE.md", "action": "EXPAND", "status": "QUALIFIED", "risk": (5, "R2"),
        "sources": ["archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-A37A8B7B245E7776.json", "archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-C9AE050CD9C1886D.md", "archive/source-records/campaign-delta-official/SRC-OFF-F217B64FD0342839.md"],
        "claims": ["SAGE family stages and technical identifiers receive separate lifecycle states.", "Aephia places the community-reported SAGE 3D release in December 2023, not 2024.", "Current and legacy program labels do not establish migration or deactivation dates."],
    },
    {
        "id": "score-starbased-transition", "path": "knowledge/gameplay/SCORE-and-Faction-Fleet.md", "action": "EXPAND", "status": "HISTORICAL", "risk": (6, "R2"),
        "sources": ["archive/source-records/campaign-delta-official/SRC-OFF-0AED270D51ACD552.md", "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-9FFFF91025488D09.json", "archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-19357309E964FAF8.md"],
        "claims": ["SCORE application, on-chain program, ATLAS emissions, and residual functionality are separate objects.", "April 2024 sources announce emissions deprecation but do not prove execution.", "SCORE remains documented as a mainnet program in April 2026 without proving active rewards."],
    },
    {
        "id": "holosim-release-feature-history", "path": "knowledge/gameplay/Holosim.md", "action": "EXPAND", "status": "QUALIFIED", "risk": (5, "R2"),
        "sources": ["archive/source-records/campaign-delta-official/SRC-OFF-4850F98FBD1F1541.md", "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-D8337FA27E0A550A.json", "archive/source-records/campaign-delta-official/SRC-OFF-B3E826AFA52FB19B.md"],
        "claims": ["Holosim public test, Chapter 1, delay, reschedule, and Chapter 2 are distinct lifecycle events.", "Feature claims are assigned to dated builds rather than the product for all time.", "Decoder support and publisher-reported RPC migration are not deployment audits."],
    },
    {
        "id": "official-communications-chronology", "path": "knowledge/timeline/Official-Communications-Chronology.md", "action": "CREATE", "status": "QUALIFIED", "risk": (5, "R2"),
        "sources": ["archive/campaign-summaries/campaign-delta-official/campaign-summary.json", "operations/campaigns/discord-announcements-semantic-enrichment/campaign-summary.json", "archive/source-records/campaign-delta-official/SRC-OFF-2A930EF6763F8490.md", "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-D27B5214B5BAC6AA.json"],
        "claims": ["Official communication spans multiple incomplete publication surfaces.", "Cross-surface repetition is not independent execution evidence.", "The unmerged Medium campaign is excluded from this main-based knowledge campaign."],
    },
    {
        "id": "historical-periodization", "path": "knowledge/timeline/Star-Atlas-Historical-Periodization.md", "action": "CREATE", "status": "QUALIFIED", "risk": (7, "R3"),
        "sources": ["knowledge/timeline/Master-Timeline.md", "knowledge/timeline/Product-Timeline.md", "knowledge/timeline/Governance-Timeline.md"],
        "claims": ["Historical periods are curator synthesis rather than source-native events.", "Boundaries are proposed where product, economy, governance, and communications change together.", "Alternative periods remain research hypotheses pending stronger primary evidence."],
    },
    {
        "id": "town-hall-history", "path": "knowledge/media/Star-Atlas-Town-Hall-History.md", "action": "CREATE", "status": "QUALIFIED", "risk": (7, "R3"),
        "sources": ["archive/semantic/star-atlas-transcripts/source-index.json", "archive/source-records/campaign-delta-official/SRC-OFF-DD9175EF794C1F8D.md", "archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-3D3AC774A6A30EE3.md"],
        "claims": ["Official publications establish Town Hall as a recurring format by May 2021.", "The 14-source transcript package is incomplete and largely undated.", "Transcript names do not establish speaker attribution without diarization."],
    },
    {
        "id": "atlas-brew-history", "path": "knowledge/media/Atlas-Brew-History.md", "action": "CREATE", "status": "QUALIFIED", "risk": (7, "R3"),
        "sources": ["archive/semantic/atlas-brew/video-index.json", "archive/source-records/atlas-brew-combined/source-records.json", "archive/source-records/campaign-delta-official/SRC-OFF-2E4DE78B3C355FA9.md"],
        "claims": ["Official records describe Atlas Brew as a recurring live community discussion format.", "The 123-source transcript corpus has episode-number, date, URL, and speaker gaps.", "Event origin and replay publisher must remain separate."],
    },
    {
        "id": "technology-program-registry", "path": "knowledge/technology/Official-Technical-Surface-Inventory.md", "action": "EXPAND", "status": "QUALIFIED", "risk": (6, "R2"),
        "sources": ["archive/source-records/campaign-delta-official/SRC-OFF-F217B64FD0342839.md", "archive/source-records/campaign-delta-official/SRC-OFF-B3E826AFA52FB19B.md", "archive/source-records/campaign-delta-official/SRC-OFF-3974380BE9CB23D7.md"],
        "claims": ["Programs, game IDs, APIs, frameworks, repositories, and support initiatives are separate technical surfaces.", "Documented and decoder-supported states do not prove deployment.", "Atlas Prime naming and Holosim program coverage remain unresolved conflicts."],
    },
    {
        "id": "organization-role-registry", "path": "knowledge/organizations/Organization-and-Role-Registry.md", "action": "CREATE", "status": "QUALIFIED", "risk": (6, "R2"),
        "sources": ["archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json", "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json"],
        "claims": ["ATMTA, DAO, Foundation, and Council are distinct institutions.", "Election, service, intended term, and current role are distinct states.", "Publisher, event originator, and replay publisher are separate provenance roles."],
    },
    {
        "id": "event-evidence-registry", "path": "knowledge/events/Event-Evidence-Registry.md", "action": "CREATE", "status": "QUALIFIED", "risk": (6, "R2"),
        "sources": ["archive/source-records/campaign-delta-official/SRC-OFF-AB9BE32532D219C9.md", "archive/source-records/campaign-delta-official/SRC-OFF-E89CAA2834793DCC.md", "archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-3D3AC774A6A30EE3.md"],
        "claims": ["Event announcement, schedule, occurrence, recording, and result are distinct states.", "COPA 2022 has a staged official announcement-to-result record.", "Community Week and 426LIVE remain source-qualified case studies with missing artifacts."],
    },
]

CORRECTIONS = [
    {"path": "knowledge/gameplay/Product-Registry.md", "action": "CORRECT", "reason": "Narrow SAGE 3D date and Faction Fleet deprecation state."},
    {"path": "knowledge/timeline/Product-Timeline.md", "action": "CORRECT", "reason": "Correct community-reported SAGE 3D year to 2023."},
    {"path": "knowledge/timeline/Master-Timeline.md", "action": "CORRECT", "reason": "Correct SAGE 3D year and ground first PIP results in official captures."},
]

INDEXES = [
    "knowledge/README.md", "knowledge/governance/README.md", "knowledge/economy/README.md",
    "knowledge/gameplay/README.md", "knowledge/media/README.md", "knowledge/timeline/README.md",
    "knowledge/technology/README.md", "knowledge/organizations/README.md", "knowledge/events/README.md",
    "knowledge/research/README.md",
]

BACKLOG = [
    ("P0", "Treasury transaction reconciliation", "Transaction signatures, block times, source/recipient wallets, token mints/decimals, payment dates, conversion basis, and signer authority for every Council-reported amount."),
    ("P0", "Council elections 2 and 3", "Official final tallies, winner announcements, seating, resignations, replacements, and term-end evidence."),
    ("P0", "SCORE emissions execution", "Post-April-16 confirmation, final reward transaction/block, parameter-change transaction, current UI test, and program authority."),
    ("P0", "Program deployment and security", "Deployment/upgrade transactions, authorities, versioned IDLs, program-specific audit reports, findings, remediation, and deployed hashes."),
    ("P1", "SAGE 3D and SAGE Labs V2", "First-party release artifacts, exact dates, build/version history, migration records, and feature matrix."),
    ("P1", "Atlas Brew and Town Hall provenance", "Original URLs/video IDs, dates, complete episode ledgers, hosts/guests, speaker diarization, and replay lineage."),
    ("P1", "Official Medium dependency", "Review and merge the separate article-level ingestion campaign before knowledge promotion; reconcile revisions and redirects."),
    ("P1", "ATLAS and POLIS ledgers", "Economics paper, genesis/mint transactions, vesting, emissions, burns, holders, treasury balances, and sale settlement records."),
    ("P2", "Organization and role chronology", "Corporate filings, Foundation officers, current Council roster, staff appointments/departures, and delegation instruments."),
    ("P2", "Event occurrence and results", "Complete COPA, Community Week, 426LIVE, Gamescom, Town Hall, Atlas Brew, and Joni Awards evidence chains."),
]

SUBJECTS = {
    "governance-constitutional-history": ["Star Atlas DAO", "Star Atlas Foundation", "Star Atlas Council", "PIP process", "Ecosystem Fund"],
    "council-election-history": ["Star Atlas Council", "PIP-6", "PIP-7", "PIP-11", "PIP-25"],
    "governance-failure-casebook": ["PIP-13", "PIP-14", "PIP-15", "PIP-17", "PIP-19", "PIP-26", "PIP-31"],
    "treasury-authorization-payment-ledger": ["DAO Treasury account", "Ecosystem Fund wallet", "Star Atlas Council", "Star Atlas Foundation"],
    "ecosystem-fund-award-history": ["Ecosystem Fund", "PIP-4", "PIP-23", "Star Atlas Council"],
    "atlas-token-history": ["ATLAS", "ATLAS Locker", "DAO Treasury account", "zATLAS"],
    "polis-token-history": ["POLIS", "POLIS Locker", "PVP", "Star Atlas DAO"],
    "sage-product-family-history": ["SAGE", "SAGE Labs", "SAGE 3D", "Starbased", "C4", "Project S.C.R.E.A.M."],
    "score-starbased-transition": ["SCORE", "Faction Fleet", "Faction Fleet emissions", "Starbased"],
    "holosim-release-feature-history": ["Holosim", "Holosim Chapter 1", "Holosim Chapter 2", "zATLAS"],
    "official-communications-chronology": ["Star Atlas newsroom", "Official Discord", "Official X account", "Official Medium", "governance portal"],
    "historical-periodization": ["Star Atlas institutional history"],
    "town-hall-history": ["Star Atlas Town Hall"],
    "atlas-brew-history": ["Atlas Brew"],
    "technology-program-registry": ["Star Atlas mainnet programs", "Star Atlas game IDs", "SFT", "F-KIT", "Build API", "Unreal Engine tooling"],
    "organization-role-registry": ["ATMTA, Inc.", "Star Atlas DAO", "Star Atlas Foundation", "Star Atlas Council", "Ecosystem Fund"],
    "event-evidence-registry": ["COPA Festival", "Community Week", "426LIVE", "Town Hall", "Atlas Brew", "Gamescom", "Joni Awards"],
}

ALIASES = {
    "score-starbased-transition": ["SCORE", "Faction Fleet"],
    "polis-token-history": ["Star Atlas DAO governance token"],
    "atlas-token-history": ["Star Atlas utility token"],
    "town-hall-history": ["Star Atlas Town Hall"],
}

PAGE_GAPS = {
    "governance-constitutional-history": "Recover and compare the full 2023 PIP-1 publication, explanatory series, versioned framework texts, and proposal-specific implementation records.",
    "council-election-history": "Acquire official final tallies, winner announcements, seating, resignations, replacements, and term-end evidence for later Council elections.",
    "governance-failure-casebook": "Recover proposal-specific termination, withdrawal, payment, deliverable, and implementation records for every terminal case.",
    "treasury-authorization-payment-ledger": "Reconcile every reported amount to transaction signatures, block times, wallets, mints, decimals, recipients, conversion bases, milestones, and acceptance records.",
    "ecosystem-fund-award-history": "Recover transaction and deliverable chains for every passed authorization, including mixed-denomination accounting conventions.",
    "atlas-token-history": "Acquire the economics paper, genesis and mint records, emissions and burn ledger, vesting history, sale settlement, and dated treasury balances.",
    "polis-token-history": "Acquire genesis and distribution records, reward-emission history, dated holder concentration, and locker/governance program upgrade history.",
    "sage-product-family-history": "Recover first-party SAGE 3D and SAGE Labs V2 release artifacts, exact dates, build matrix, migrations, deployment transactions, authorities, and versioned IDLs.",
    "score-starbased-transition": "Recover post-April-16 execution confirmation, final reward block, parameter-change transaction, current UI test, and program authority.",
    "holosim-release-feature-history": "Acquire build manifests, release notes, deployment identifiers, decoder version history, RPC migration evidence, and incident-resolution records.",
    "official-communications-chronology": "Complete Medium review after PR #19 merges and recover deleted or edited posts, attachments, correction chains, and pre-2024 X history.",
    "historical-periodization": "Test proposed period boundaries against a more complete official and community publication corpus and document competing curator models.",
    "town-hall-history": "Recover original URLs, video IDs, dates, hosts, guests, agendas, speaker diarization, and complete episode numbering.",
    "atlas-brew-history": "Recover original URLs, dates, hosts, guests, duplicate-number resolution, speaker diarization, and replay lineage for all 123 records.",
    "technology-program-registry": "Acquire deployment and upgrade transactions, authorities, versioned IDLs, deployed hashes, program-specific audits, findings, and remediation evidence.",
    "organization-role-registry": "Acquire corporate filings, Foundation officers, current Council roster, staff appointment and departure records, and delegation instruments.",
    "event-evidence-registry": "Recover occurrence pages, agendas, rosters, recordings, results, prize transactions, cancellations, reschedules, and correction notices.",
}


def claim_type(page_id: str) -> str:
    if page_id in {"sage-product-family-history", "score-starbased-transition", "holosim-release-feature-history"}:
        return "PRODUCT_LIFECYCLE"
    if page_id in {"atlas-token-history", "polis-token-history", "treasury-authorization-payment-ledger"}:
        return "ECONOMIC_HISTORY"
    if page_id in {"technology-program-registry"}:
        return "TECHNICAL_REGISTRY"
    if page_id in {"official-communications-chronology", "town-hall-history", "atlas-brew-history"}:
        return "COMMUNICATIONS_HISTORY"
    if page_id == "event-evidence-registry":
        return "EVENT_HISTORY"
    return "INSTITUTIONAL_HISTORY"


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def authority(source: str) -> str:
    if "/social-governance-semantic-enrichment/governance/SRC-PIP-" in source:
        return "A1"
    if "council-pip-tracker" in source:
        return "A3"
    if source.startswith("knowledge/") or source.startswith("operations/") or "/semantic/" in source or "campaign-summary" in source:
        return "DERIVED_REVIEWED"
    if "/campaign-alpha-aephia/" in source:
        return "B2"
    return "A2"


def main() -> None:
    PACKETS.mkdir(parents=True, exist_ok=True)
    for spec in SPECS:
        details = [{"source": s, "source_authority": authority(s), "source_role": "EVIDENCE_SOURCE" if authority(s) != "DERIVED_REVIEWED" else "DERIVED_RESEARCH_AID"} for s in spec["sources"]]
        claims = []
        for i, text in enumerate(spec["claims"], 1):
            claims.append({
                "claim_id": f"{spec['id'].upper()}-{i:02d}", "claim_text": text,
                "claim_type": claim_type(spec["id"]), "temporal_scope": "DATE_BOUND",
                "lifecycle_state": "EXPLICITLY_SEPARATED_WHERE_APPLICABLE",
                "supporting_sources": spec["sources"], "supporting_source_details": details,
                "source_authority": sorted({d["source_authority"] for d in details}),
                "corroboration_status": "REVIEWED", "contradiction_status": "DISCLOSED_WHERE_PRESENT",
                "attribution_required": True, "confidence": "MEDIUM" if spec["risk"][1] == "R3" else "HIGH",
                "allowed_in_page": True,
            })
        packet = {
            "page_id": spec["id"], "proposed_path": spec["path"], "page_action": spec["action"],
            "proposed_knowledge_status": spec["status"], "page_risk_score": spec["risk"][0], "page_risk_class": spec["risk"][1],
            "subject_entities": SUBJECTS[spec["id"]], "aliases": ALIASES.get(spec["id"], []),
            "scope": f"Evidence-qualified history for {', '.join(SUBJECTS[spec['id']])} from artifacts merged on main.",
            "material_claims": claims,
            "known_limitations": ["Source authority does not imply independent factual verification.", "Current-state claims are date-bound.", "Missing evidence is preserved as a gap and is not resolved by inference."],
            "research_gaps": [PAGE_GAPS[spec["id"]]],
            "review_required": True, "review_after": "2026-10-17" if spec["risk"][1] == "R3" else "2027-01-17",
        }
        write_json(PACKETS / f"{spec['id']}.json", packet)

    inventory = {
        "campaign_id": "knowledge-narrative-depth-001", "as_of": AS_OF, "output_count": len(SPECS),
        "outputs": [{"page_id": s["id"], "path": s["path"], "action": s["action"], "status": s["status"], "risk_score": s["risk"][0], "risk_class": s["risk"][1], "evidence_packet": f"evidence-packets/{s['id']}.json"} for s in SPECS],
        "corrections": CORRECTIONS, "index_updates": INDEXES,
    }
    write_json(HERE / "page-inventory.json", inventory)
    (HERE / "page-inventory.md").write_text(
        "# Page Inventory\n\n" + "\n".join(f"- `{x['action']}` [{x['page_id']}](../../../{x['path']}) — {x['status']}, {x['risk_class']}" for x in inventory["outputs"]) +
        "\n\n## Corrections\n\n" + "\n".join(f"- `{x['path']}` — {x['reason']}" for x in CORRECTIONS) + "\n", encoding="utf-8")

    ledger = {
        "campaign_id": "knowledge-narrative-depth-001",
        "accepted": [{"candidate": s["id"], "path": s["path"], "action": s["action"], "evidence_packet": f"evidence-packets/{s['id']}.json"} for s in SPECS] + CORRECTIONS + [{"path": p, "action": "INDEX_UPDATE"} for p in INDEXES],
        "deferred": [
            {"candidate": "Later Council winner rosters", "reason": "Official final-result artifacts missing."},
            {"candidate": "Verified recipient payment ledger", "reason": "Council values lack transaction reconciliation."},
            {"candidate": "Complete Medium communications history", "reason": "PR #19 is unmerged and excluded from this main-based campaign."},
            {"candidate": "Joni Awards results", "reason": "Recording/prediction evidence does not establish a complete result ledger."},
        ],
        "duplicate": [
            {"candidate": "Standalone SAGE-family entity page", "canonical_path": "knowledge/gameplay/SAGE.md", "reason": "Existing canonical page expanded."},
            {"candidate": "Standalone Holosim history entity", "canonical_path": "knowledge/gameplay/Holosim.md", "reason": "Existing canonical page expanded."},
            {"candidate": "Second technical registry", "canonical_path": "knowledge/technology/Official-Technical-Surface-Inventory.md", "reason": "Existing inventory retitled and expanded."},
        ],
        "rejected": [
            {"candidate": "Faction Fleet emissions confirmed ended", "reason": "Only future-tense deprecation announcements are preserved; execution unverified."},
            {"candidate": "SAGE 3D released December 2024", "reason": "Cited Aephia source places the report under December 2023."},
            {"candidate": "Council tracker completion for failed PIPs", "reason": "Failed votes supplied no implementation authority."},
            {"candidate": "PIP-33 as Ecosystem Fund award", "reason": "Primary proposal and tracker identify a direct DAO Treasury measure."},
        ],
    }
    write_json(HERE / "promotion-ledger.json", ledger)
    (HERE / "promotion-ledger.md").write_text(
        "# Promotion Ledger\n\n## Accepted\n\n" + "\n".join(f"- `{x.get('action')}` `{x.get('path')}`" for x in ledger["accepted"]) +
        "\n\n## Deferred\n\n" + "\n".join(f"- {x['candidate']}: {x['reason']}" for x in ledger["deferred"]) +
        "\n\n## Duplicate\n\n" + "\n".join(f"- {x['candidate']} → `{x['canonical_path']}`: {x['reason']}" for x in ledger["duplicate"]) +
        "\n\n## Rejected\n\n" + "\n".join(f"- {x['candidate']}: {x['reason']}" for x in ledger["rejected"]) + "\n", encoding="utf-8")

    write_json(HERE / "research-backlog.json", {"campaign_id": "knowledge-narrative-depth-001", "items": [{"priority": p, "research_area": n, "required_artifacts": a} for p, n, a in BACKLOG]})
    (HERE / "research-backlog.md").write_text("# Prioritized Research Backlog\n\n" + "\n".join(f"## {p} — {n}\n\n{a}\n" for p, n, a in BACKLOG), encoding="utf-8")

    risk_counts = {risk: sum(1 for s in SPECS if s["risk"][1] == risk) for risk in ("R1", "R2", "R3", "R4", "R5")}
    status_counts = {status: sum(1 for s in SPECS if s["status"] == status) for status in sorted({s["status"] for s in SPECS})}
    summary = {
        "campaign_id": "knowledge-narrative-depth-001", "status": "READY_FOR_VALIDATION", "as_of": AS_OF,
        "outputs": len(SPECS), "created": sum(s["action"] == "CREATE" for s in SPECS), "expanded": sum(s["action"] == "EXPAND" for s in SPECS),
        "corrections": len(CORRECTIONS), "risk_distribution": risk_counts, "knowledge_status_distribution": status_counts,
        "evidence_packets": len(SPECS), "archive_evidence_modified": False, "graph_modified": False, "publication_modified": False,
        "unmerged_dependencies_used": False, "excluded_dependency": "PR #19 Medium ingestion remains unmerged and was not used.",
    }
    write_json(HERE / "campaign-summary.json", summary)
    (HERE / "campaign-summary.md").write_text(
        f"# Campaign Summary\n\nCreated {summary['created']} pages and substantively expanded {summary['expanded']} pages across governance, economy, products, communications, technology, organizations, events, and historical interpretation. Generated {summary['evidence_packets']} evidence packets and recorded {summary['corrections']} source-driven corrections.\n\n"
        f"Risk distribution: {risk_counts}. Knowledge status distribution: {status_counts}. No archive, graph, or publication evidence was modified. PR #19 remains an excluded unmerged dependency.\n", encoding="utf-8")
    (HERE / "risk-register.md").write_text(
        "# Risk Register\n\n- **R3 treasury and awards:** authorization is strong; payment and outcome verification is weak.\n"
        "- **R3 periodization:** boundaries are curator synthesis and require future revision.\n"
        "- **R3 transcript histories:** dates, URLs, speakers, and episode completeness are unresolved.\n"
        "- **R2 product lifecycle:** SAGE 3D is community-dated; SCORE deprecation execution is unverified.\n"
        "- **R2 technology:** documentation and decoders do not prove deployment, audits, or authority.\n", encoding="utf-8")


if __name__ == "__main__":
    main()
