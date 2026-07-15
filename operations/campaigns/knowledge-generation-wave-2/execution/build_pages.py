"""Generate Wave 2A foundation pages from reviewed evidence packets."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PACKETS = ROOT / "operations/campaigns/knowledge-generation-wave-2/evidence-packets"
PIP_REGISTRY = ROOT / "archive/semantic/governance/pip-registry-semantic.json"


def front(page_id: str, title: str) -> str:
    p = json.loads((PACKETS / f"{page_id}.json").read_text(encoding="utf-8"))
    basis = sorted({s for c in p["material_claims"] for s in c["supporting_sources"]})
    lines = [
        "---", f'title: "{title}"', f'knowledge_status: {p["proposed_knowledge_status"]}',
        "as_of: 2026-07-15", "confidence: HIGH" if p["page_risk_score"] <= 4 else "confidence: MEDIUM",
        f'page_risk_score: {p["page_risk_score"]}', f'page_risk_class: {p["page_risk_class"]}',
        "evidence_basis:", *[f'  - "{x}"' for x in basis],
        "known_limitations:", *[f'  - "{x}"' for x in p["known_limitations"]],
        "research_gaps:", *[f'  - "{x}"' for x in p["research_gaps"]],
        f'review_after: {p["review_after"]}', "---", "", f"# {title}", "",
    ]
    return "\n".join(lines)


PAGES = {
"star-atlas-dao": ("Star Atlas DAO", """The Star Atlas DAO is the on-chain governance system through which participants who lock and vote with POLIS form collective decisions about the Star Atlas ecosystem. It is not interchangeable with ATMTA, the Star Atlas Foundation, or the Star Atlas Council.

## Scope and authority

The captured text of PIP-1 defines the DAO as a decentralized, program-based governance system deployed on Solana. Its formal decision authority is expressed through proposal procedures and PVP-weighted POLIS voting. The PIP establishes what the institution was designed to do; a later proposal result or portal label must be consulted before asserting that any particular policy was approved. [PIP-1; SRC-PIP-01-BC8475E4](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

The DAO's role is legislative and allocative: participants can consider proposals, select Council members through the applicable election mechanism, and approve treasury or policy actions. Administrative review and lawful implementation are assigned elsewhere. See [Star Atlas Foundation](Star-Atlas-Foundation.md) and [Star Atlas Council](Star-Atlas-Council.md).

## Decision boundaries

A published PIP is a request. An open vote is a decision process. A passing result is authorization. None of those states, by itself, proves payment, deployment, or completed delivery. The [PIP Registry](PIP-Registry.md) therefore records passage separately from Council-reported operations and independent execution evidence.

## Current state

As of 2026-07-15, the archive supports the DAO's institutional identity and preserved proposal corpus. It does not establish that every approved proposal was executed or that the corpus is independently complete beyond the 33 captured PIPs.

## Evidence references

- [Captured PIP registry](../../archive/semantic/governance/pip-registry-semantic.json)
- [PIP-1 source record](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)
- [PIP lifecycle](PIP-Lifecycle-and-Legislative-Process.md)
"""),
"star-atlas-foundation": ("Star Atlas Foundation", """The Star Atlas Foundation is the legal and administrative implementation body described in the captured governance framework. It is distinct from the POLIS electorate and from the elected Council.

## Institutional role

PIP-1 assigns the Foundation, or a delegated administrator, responsibility for reviewing submitted PIPs for procedural compliance, requesting revisions, rejecting noncompliant submissions with public reasoning, and advancing compliant proposals. The same governance text places implementation inside legal, safety, and compliance constraints. [PIP-1; SRC-PIP-01-BC8475E4](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

PIP-2 is the dedicated Foundation proposal in the captured corpus. Its passing result supports institutional ratification; it does not make every later operational act independently verified. [PIP registry](../../archive/semantic/governance/pip-registry-semantic.json)

## Boundaries

The Foundation is not the DAO's electorate and does not replace PVP-weighted voting. The framework permits administrative judgment over proposal compliance and implementation safety, but that role should not be described as an independent legislative sovereignty. Delegation to the Council does not erase the distinction between the two institutions.

## Current state

As of 2026-07-15, the captured governance record supports proposal administration and legal/operational mediation. Treasury-custody or portal-administration claims should be tied to the particular PIP or operational record that establishes them; the archive does not justify an unlimited general mandate.

## Evidence references

- [PIP-1 source record](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)
- [PIP-2 source record](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json)
- [Star Atlas DAO](Star-Atlas-DAO.md)
"""),
"star-atlas-council": ("Star Atlas Council", """The Star Atlas Council is an elected steward of the DAO's governance process. Its documented work includes author assistance, governance operations, program administration, and delegated review of milestones or payments. It is not a separate legislative sovereign.

## Establishment and elections

PIP-3 established the Council framework. PIP-6 was the first election's advancing round: its top twelve were candidates for the next round, not final Council winners. PIP-7 was the final round and identifies the five elected members. Later election PIPs 11 and 25 are recorded as passed, but the preserved reconciliation leaves winner identity unresolved; PIP-27 has the same limitation for the DAO Casters election. [PIP registry](../../archive/semantic/governance/pip-registry-semantic.json)

## Operational assessments

Council tracker evidence is preserved with the following qualification:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

Accordingly, statements about milestones, payments, termination, cancellation, or implementation are written as “the Council tracker reports” unless another primary record independently establishes the event. A Council-reported completed milestone is not automatically an independently verified deliverable.

## Current state

As of 2026-07-15, the archive supports the Council's process-steward and delegated administrative roles. It does not establish a current membership roster for elections whose winners remain unresolved in the captured evidence.

## Evidence references

- [PIP-3 source record](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json)
- [Governance semantic registry](../../archive/semantic/governance/pip-registry-semantic.json)
- [Governance evidence states](Governance-Implementation-and-Evidence-States.md)
"""),
"ecosystem-fund": ("Star Atlas Ecosystem Fund", """The Ecosystem Fund is a DAO policy instrument for financing ecosystem work. Its controlling captured framework is PIP-23, which refreshes and supersedes PIP-4.

## Policy history

PIP-4 proposed the original fund, including a budget linked to 20% of the DAO treasury and a stated USD limitation. PIP-23 later continued the fund and expressly replaced PIP-4. Historical references to PIP-4 remain useful, but current interpretation must begin with PIP-23. [PIP-4 and PIP-23](../../archive/semantic/governance/pip-registry-semantic.json)

PIP-23 allocates 20% of ATLAS and 20% of USDC above a $500,000 DAO-treasury reserve threshold. It calls for quarterly refills when the fund falls below those formulas. Funding applications must state their request in USDC, while the fund pays only in ATLAS; the text also calls for received USDC to be converted to ATLAS while USDC remains an insignificant treasury component. No single PIP may exceed 5% of the “Balance After” value from the last refill transaction or run longer than 12 months. [PIP-23; SRC-PIP-23-0ECF2928](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json)

The Council's specified duties are to review and steward eligible proposals, coordinate special approval where needed, implement passed PIPs, and track payments. The same text says the Council does not authorize legally binding contracts, execute fund-refill transactions, conduct KYC/KYB, or approve a PIP before voting. These are policy assignments, not proof that a particular transfer occurred.

## Decision and payment boundaries

An approved grant proposal authorizes an action under the applicable policy. It does not by itself establish that funds were transferred, milestones were accepted, or deliverables were completed. Council tracker fields are retained as attributed operational assessments:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

## Current state

As of 2026-07-15, PIP-23 is the supported superseding policy. Independent payment and deliverable verification remains incomplete for many funded PIPs.

## Evidence references

- [PIP registry](PIP-Registry.md)
- [PIP-23 source record](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json)
"""),
"pip-lifecycle": ("PIP Lifecycle and Legislative Process", """A POLIS Improvement Proposal moves through distinct documentary, voting, and operational states. This page defines the minimum vocabulary used across the knowledge base.

## Legislative sequence

1. **Draft or discussion:** an author develops a proposal. No DAO decision exists.
2. **Administrative review:** the Foundation or delegated administrator checks the captured PIP-1 requirements and may request revision, reject, or advance the text.
3. **Pending/publication:** the proposal becomes visible for community review. Publication is not approval.
4. **Voting:** eligible POLIS voting power participates under the proposal's specified mechanism and dates.
5. **Result:** the applicable formula produces a pass, fail, or election outcome. A result must be read using its mechanism.
6. **Implementation:** an authorized body may act. An announcement of implementation is not completion.
7. **Execution evidence:** transactions, deployed changes, accepted milestones, or equivalent records may establish later states.

The captured PIP-1 text supports the process through voting and administration. [PIP-1; SRC-PIP-01-BC8475E4](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

## Mechanism-specific interpretation

Election PIPs require special care. PIP-6 selected advancing candidates; it did not elect the final first Council. PIP-7 conducted the final round. A “passed” portal label on an election does not substitute for a preserved winner list. Similarly, a funding PIP's passage does not prove payment.

## Evidence rules

Every registry entry should preserve proposal number, title, mechanism, dates, result, supersession, implementation evidence, and gaps. The archive's [implementation-state model](Governance-Implementation-and-Evidence-States.md) is applied after the legislative result rather than collapsed into it.

## Evidence references

- [Governance semantic registry](../../archive/semantic/governance/pip-registry-semantic.json)
- [Star Atlas DAO](Star-Atlas-DAO.md)
"""),
"governance-evidence-states": ("Governance Implementation and Evidence States", """Governance records answer different questions at different stages. This model prevents an approved proposal from being reported as a completed outcome without execution evidence.

## State model

| State | What the evidence establishes | What it does not establish |
|---|---|---|
| PROPOSED | A request was published | approval or execution |
| VOTING | A decision process opened | final result |
| PASSED / FAILED | The applicable vote result | payment, deployment, or completion |
| IMPLEMENTATION_ANNOUNCED | An actor stated that implementation would begin | completed action |
| PARTIAL_OR_IN_PROGRESS | Attributed operational work is reported | full delivery |
| PAID | A payment record is identified | successful deliverables |
| EXECUTED | A concrete action is evidenced | every promised outcome |
| TERMINATED / CANCELED / WITHDRAWN | Later activity ended or authorization was withdrawn | reversal of the historical vote |
| INDEPENDENTLY_VERIFIED | A separate primary record corroborates the claimed operation | universal correctness beyond its scope |

## Council tracker treatment

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

The tracker may be the best available operational account, but it is the Council's own assessment. PIP-14's reported termination, PIP-17's reported cancellation, and PIP-31's post-passage withdrawal/non-implementation are therefore preserved as Council-attributed lifecycle findings unless independent evidence is linked. [Governance registry](../../archive/semantic/governance/pip-registry-semantic.json)

## Use in knowledge pages

Pages must name the source of an operational assessment and retain uncertainty. Payment, implementation, and completion require separate evidence fields. “No independent evidence identified” means the archive review did not find it; it is not proof that the event never occurred.

## Related pages

- [PIP Registry](PIP-Registry.md)
- [PIP lifecycle](PIP-Lifecycle-and-Legislative-Process.md)
"""),
"governance-economy-overview": ("Governance and Economy Overview", """Star Atlas governance connects POLIS-based decision making to treasury policy and ecosystem funding. The connection is institutional, not evidentiary shorthand: a vote can authorize an economic action without proving a payment or outcome.

## Institutions and instruments

POLIS holders exercise formal PVP-weighted voting authority through the [Star Atlas DAO](Star-Atlas-DAO.md). The [Star Atlas Foundation](Star-Atlas-Foundation.md) performs legal and administrative functions described in the captured PIPs, while the [Star Atlas Council](Star-Atlas-Council.md) stewards process and delegated programs. The [Ecosystem Fund](Ecosystem-Fund.md) is a policy instrument rather than a separate sovereign body.

## Economic evidence boundaries

For each funding PIP, the archive distinguishes requested amount, denomination, vote result, authorized maximum, payment report, and deliverable state. A requested dollar value is not a verified transaction. An ATLAS-denominated payment is not silently converted into a historical USD value. Repeated announcements are not independent corroboration.

PIP-23 supersedes PIP-4 and is the supported current fund framework as of 2026-07-15. The captured registry also contains passed, failed, in-progress, terminated, canceled, and non-implemented proposals; those states remain distinct. [Governance semantic registry](../../archive/semantic/governance/pip-registry-semantic.json)

## Current limitations

The repository does not yet independently reconcile every Council-reported payment to a transaction or every milestone to an accepted deliverable. Economic measurements and institutional statements remain source-attributed.

## Related pages

- [PIP Registry](PIP-Registry.md)
- [Governance evidence states](Governance-Implementation-and-Evidence-States.md)
- [Economy index](../economy/README.md)
"""),
"institutional-overview": ("Star Atlas Institutional Overview", """Star Atlas is represented in the archive by several related institutions with different roles. Treating them as one actor obscures who proposed, voted, administered, developed, or assessed an action.

## Institutional map

| Institution | Identity and principal role | Boundary |
|---|---|---|
| [ATMTA, Inc.](ATMTA.md) | Operating company associated with Star Atlas product development and official publications | Not identical to the DAO electorate |
| [Star Atlas DAO](../governance/Star-Atlas-DAO.md) | POLIS-locking and PVP-weighted governance system | Passage does not prove execution |
| [Star Atlas Foundation](../governance/Star-Atlas-Foundation.md) | Legal and administrative implementation body in the captured framework | Administrative discretion is not separate legislative sovereignty |
| [Star Atlas Council](../governance/Star-Atlas-Council.md) | Elected governance-process steward and delegated program administrator | Council assessments are not independent verification |

## Relationships

ATMTA may develop products or publish official statements while the DAO considers policy and treasury proposals. The Foundation administers the legal and procedural framework described in PIPs. The Council assists authors, operates governance processes, and may verify milestones or payments where delegated. These roles can interact without merging institutional identity.

## Current state

As of 2026-07-15, the strongest institutional evidence is the captured PIP corpus and official source archive. Current officeholders, corporate structure, and delegated authority can change; claims should be dated and linked to the governing record.

## Evidence references

- [Governance semantic registry](../../archive/semantic/governance/pip-registry-semantic.json)
- [Official source-record collection](../../archive/source-records/campaign-delta-official/)
"""),
"atmta": ("ATMTA, Inc.", """ATMTA, Inc. is the operating company identified across official Star Atlas product and institutional records. This page covers organizational identity and relationships, not the full history of every product or governance act.

## Role

Official Star Atlas publications associate ATMTA with development, operation, and communication around the Star Atlas product family. The dated [official current-state snapshot](../gameplay/Official-Current-State-Snapshot-2026-07-12.md) records the public product positioning captured from official surfaces. That positioning is evidence of what the company published at the time, not independent verification of every feature or performance claim.

ATMTA also appears as an affected entity or participant in governance proposals. Such participation does not make ATMTA identical to the [Star Atlas DAO](../governance/Star-Atlas-DAO.md), [Foundation](../governance/Star-Atlas-Foundation.md), or [Council](../governance/Star-Atlas-Council.md).

## Relationships

- **Products:** development and official communication are documented across the official source-record collection.
- **DAO:** policy and treasury authorization belongs to the POLIS governance process where specified.
- **Foundation:** the captured governance framework assigns legal and administrative functions to the Foundation.
- **Council:** Council operations and assessments must remain attributed to the Council.

## Current limitations

As of 2026-07-15, this page does not attempt a legal corporate history, current capitalization table, or exhaustive leadership roster. Historical roles should not be treated as current without a dated official record.

## Evidence references

- [Official source records](../../archive/source-records/campaign-delta-official/)
- [Institutional overview](Institutional-Overview.md)
"""),
"product-registry": ("Star Atlas Product Registry", """This registry is an evidence-qualified map of major Star Atlas product surfaces. Lifecycle labels are current only as of 2026-07-15 and do not convert roadmap language into delivery.

## Registry

| Product | Entity ID | Supported lifecycle | Evidence note |
|---|---|---|---|
| PLAY | PRODUCT-PLAY | LIVE | Official account and asset hub in the dated current-state capture. |
| [SCORE / Faction Fleet](SCORE-and-Faction-Fleet.md) | PRODUCT-SCORE | HISTORICAL / DEPRECATED | Earlier fleet-staking surface; community chronology reports emissions ended in 2024. |
| [SAGE / SAGE Labs](SAGE.md) | PRODUCT-SAGE | LIVE / UPDATED | Official support record documents a browser-based on-chain 4X surface; earlier roadmap phases remain historical. |
| [UE5 / Showroom](UE5-Showroom.md) | PRODUCT-UE5 | TESTING / UPDATED | Early-access client with build-specific capabilities; planned features are not assumed delivered. |
| Fleet Command | PRODUCT-FLEET-COMMAND | IN_DEVELOPMENT | Captured official page describes development; no general release is asserted. |
| Holosim | PRODUCT-HOLOSIM | LIVE | Official page documents browser availability. |
| C4 / C4 PTR | unresolved | TESTING | June 2026 support records establish PTR mining, not a mainnet or general release. |
| [Galactic Marketplace](Galactic-Marketplace.md) | PRODUCT-MARKETPLACE | LIVE | Official product surfaces describe asset trading. |
| DAO portal | PRODUCT-DAO-PORTAL | LIVE | Proposal voting and POLIS governance surface. |
| Star Atlas Build | PRODUCT-BUILD | LIVE | Builder documentation and developer-resource hub. |

## Lifecycle rules

The controlled states are FIRST_MENTION, PLANNED, IN_DEVELOPMENT, TESTING, LIVE, UPDATED, DEGRADED, RESOLVED, SUPERSEDED, DEPRECATED, CANCELED, and UNKNOWN. A state is assigned to a named product or feature and a dated evidence record. Announcement, test access, public release, and delivery of all promised features remain separate.

## Evidence references

- [Official current-state snapshot](Official-Current-State-Snapshot-2026-07-12.md)
- [Atlas Brew semantic segments](../../archive/semantic/atlas-brew/segment-index.json)
- [Official source records](../../archive/source-records/campaign-delta-official/)
"""),
"score-faction-fleet": ("SCORE and Faction Fleet", """SCORE, also presented as Faction Fleet, was an early Star Atlas fleet-management and emissions program. This is a historical page: it does not imply that the program's original rewards remain current.

## Identity and scope

Official materials described sending ships on missions through Faction Fleet and exposed the surface through PLAY. The program linked ship participation and resource consumption with ATLAS emissions. [SRC-OFF-0333A5B22A207D88](../../archive/source-records/campaign-delta-official/SRC-OFF-0333A5B22A207D88.md)

## Lifecycle

The preserved official record establishes the product identity and earlier availability. Aephia later reported that Faction Fleet ATLAS emissions ended in April 2024 after more than two years of operation. That statement is useful sourced community chronology, but it is not a substitute for a direct on-chain emissions or transaction audit. [SRC-AEPHIA-19357309E964FAF8](../../archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-19357309E964FAF8.md)

SCORE's historical role should not be collapsed into SAGE. The products are connected in the evolution of browser and on-chain gameplay, but each has its own mechanics, dates, and evidence states.

## Current state

As of 2026-07-15, this archive treats the emissions program as DEPRECATED/HISTORICAL. The precise shutdown transaction, final emissions block, and residual non-reward functionality remain research gaps.

## Related pages

- [SAGE](SAGE.md)
- [Product Registry](Product-Registry.md)
"""),
"sage": ("SAGE", """SAGE is the Star Atlas browser-based, on-chain strategy product family. SAGE Labs and later named phases belong to that family, but roadmap labels and shipped builds must be kept separate.

## Identity and scope

An official support record documents SAGE Labs as a browser-based 4X economic strategy surface involving mining, crafting, resource movement, and faction competition on Solana. That record supports availability at its captured date. [SRC-OFF-0A646AE069AFFBA5](../../archive/source-records/campaign-delta-official/SRC-OFF-0A646AE069AFFBA5.md)

## Lifecycle

Official 2022 material described the renamed SAGE program as roadmap work. It establishes planning and terminology, not delivery of the later SAGE Labs build. [SRC-OFF-22181D98D7A1B870](../../archive/source-records/campaign-delta-official/SRC-OFF-22181D98D7A1B870.md)

Atlas Brew later discussed SAGE Labs in release language at `SRC-ATLAS-BREW-0034`, 00:02:33–00:04:33 (`SEG-ATLAS-BREW-0034-0002`). Because speaker identity is not normalized, the segment supports public discussion and chronology but no named-speaker attribution. [Segment evidence](../../archive/semantic/atlas-brew/segment-index.json)

## Current state

As of 2026-07-15, official captured material supports LIVE/UPDATED for SAGE Labs as a product surface. It does not prove that every roadmap phase, interoperability claim, or proposed mechanic has shipped.

## Research gaps

The chronology from Escape Velocity through SAGE Labs, Starbased, C4, and any superseding name requires build-level reconciliation. Feature status should be tied to a specific environment and date.

## Related pages

- [Product Registry](Product-Registry.md)
- [SCORE and Faction Fleet](SCORE-and-Faction-Fleet.md)
"""),
"ue5-showroom": ("UE5 Showroom", """The UE5 Showroom is the early Star Atlas Unreal Engine 5 client and presentation environment. “UE5,” “Showroom,” and later build labels can overlap, but they should not be used as proof that every announced feature exists in every build.

## Identity and scope

Official captured materials present an evolving high-fidelity client distributed through Epic Games, with build-specific flight, racing, combat, crew, exploration, and testing capabilities. The [official current-state snapshot](Official-Current-State-Snapshot-2026-07-12.md) records positioning as of 2026-07-12, not historical availability for every feature.

## Lifecycle

The Showroom began as a limited Unreal presentation and gameplay surface and subsequently received tests and updates. Atlas Brew discussions preserve build and design commentary, but unknown speaker labels prevent named attribution. Test participation establishes access to that test environment; it does not establish a general release.

Official roadmap records describe planned UE5 capabilities. Those plans remain PLANNED unless a dated build, release note, or support record establishes TESTING, LIVE, or UPDATED. Marketing repetition is not independent corroboration.

## Current state

As of 2026-07-15, the supported state is TESTING/UPDATED and early access. The archive does not support a claim that all roadmap careers, locations, multiplayer modes, or SAGE interoperability have been delivered.

## Evidence references

- [Official current-state snapshot](Official-Current-State-Snapshot-2026-07-12.md)
- [Official source records](../../archive/source-records/campaign-delta-official/)
- [Atlas Brew semantic segments](../../archive/semantic/atlas-brew/segment-index.json)
"""),
"galactic-marketplace": ("Galactic Marketplace", """The Galactic Marketplace is the Star Atlas asset-trading surface identified in official product records. It is related to PLAY and on-chain economic systems but is not itself evidence of any particular trade or market outcome.

## Identity and role

Official current-state material lists the marketplace among the asset-management capabilities available through the Star Atlas product ecosystem. Builder documentation also treats marketplace systems as part of the on-chain game economy. [Official current-state snapshot](Official-Current-State-Snapshot-2026-07-12.md)

## Lifecycle and platform

As of 2026-07-15, the captured official record supports LIVE for the marketplace surface. That status means an official access path and product description were available; it does not independently establish liquidity, volume, pricing accuracy, settlement success for every transaction, or availability of every asset class.

References to future localized markets or interoperability are roadmap or design evidence until a release record establishes delivery. Marketplace mentions inside another product do not automatically mean the same interface, contracts, or access conditions apply.

## Related systems

- [Product Registry](Product-Registry.md)
- [SAGE](SAGE.md)
- [Governance and Economy Overview](../governance/Governance-and-Economy-Overview.md)

## Research gaps

The archive still needs a dated contract/interface history, deprecated-marketplace lineage, and independent reconciliation of major operational changes.
"""),
}


INDEXES = {
"governance-index": ("Governance Knowledge", """This domain documents Star Atlas governance institutions, procedures, proposal history, and evidence states. It keeps authorization separate from execution.

## Foundations

- [Star Atlas DAO](Star-Atlas-DAO.md) — POLIS electorate and formal voting authority.
- [Star Atlas Foundation](Star-Atlas-Foundation.md) — legal and administrative implementation body.
- [Star Atlas Council](Star-Atlas-Council.md) — elected process steward and delegated administrator.
- [PIP Lifecycle and Legislative Process](PIP-Lifecycle-and-Legislative-Process.md) — proposal-to-result sequence.
- [Governance Implementation and Evidence States](Governance-Implementation-and-Evidence-States.md) — passage, payment, implementation, and verification boundaries.
- [PIP Registry](PIP-Registry.md) — evidence-qualified captured proposal corpus.
- [Ecosystem Fund](Ecosystem-Fund.md) — PIP-23 policy and funding boundaries.
- [Governance and Economy Overview](Governance-and-Economy-Overview.md) — treasury and economic relationship.
- The [Governance and Economy Overview](Governance-and-Economy-Overview.md) records POLIS and treasury relationships without creating unsupported duplicate entity pages.

## Editorial rule

Current-state claims are dated. Council tracker statements retain Council attribution. Proposal, vote, passage, announced implementation, payment, and independently verified completion are not collapsed.
"""),
"organizations-index": ("Organizations Knowledge", """This domain records institutional identity, history, aliases, relationships, and lifecycle. Governance authority and procedure remain in the governance domain.

## Foundation pages

- [Institutional Overview](Institutional-Overview.md)
- [ATMTA, Inc.](ATMTA.md)
- Community-publication identity remains preserved in the archive until dedicated organization pages receive evidence packets.

## Governance institutions

- [Star Atlas DAO](../governance/Star-Atlas-DAO.md)
- [Star Atlas Foundation](../governance/Star-Atlas-Foundation.md)
- [Star Atlas Council](../governance/Star-Atlas-Council.md)

These links are intentional: organization pages describe identity and relationships, while governance pages define authority, procedure, voting, treasury, and implementation boundaries.
"""),
"gameplay-index": ("Gameplay and Product Knowledge", """This domain documents product identity, build-specific lifecycle history, and evidence-qualified current state.

## Foundation pages

- [Product Registry](Product-Registry.md)
- [Official Current-State Snapshot — 2026-07-12](Official-Current-State-Snapshot-2026-07-12.md)
- [SCORE and Faction Fleet](SCORE-and-Faction-Fleet.md)
- [SAGE](SAGE.md)
- [UE5 Showroom](UE5-Showroom.md)
- [Galactic Marketplace](Galactic-Marketplace.md)
- Fleet Command, Holosim, and C4 remain qualified registry entries pending dedicated-page evidence packets.

## Lifecycle rule

The domain uses FIRST_MENTION, PLANNED, IN_DEVELOPMENT, TESTING, LIVE, UPDATED, DEGRADED, RESOLVED, SUPERSEDED, DEPRECATED, CANCELED, and UNKNOWN. Announcement is not release; test access is not general availability; release does not establish delivery of all roadmap features.
"""),
}


def build_pip_registry() -> str:
    data = json.loads(PIP_REGISTRY.read_text(encoding="utf-8"))
    special = {
        4: "Superseded by PIP-23.", 6: "First-round advancing candidates; not final winners.",
        7: "Final first-Council election; winners identified.", 11: "Council-reported passage; winners unresolved.",
        13: "Failed.", 14: "Passed; Council tracker later reports termination.", 15: "Failed.",
        17: "Passed; Council tracker later reports cancellation/termination.", 19: "Failed.",
        23: "Supersedes PIP-4.", 25: "Council-reported passage; winners unresolved.",
        26: "Failed.", 27: "Council-reported passage; winners unresolved.",
        31: "Passed, later withdrawn after passage; Council tracker reports not implemented.",
    }
    rows = []
    for p in data["proposals"]:
        n = p["pip_number"]
        result = p.get("reviewed_result") or "UNKNOWN"
        mechanism = ", ".join(p.get("proposal_category") or []) or "UNKNOWN"
        impl = p.get("council_reported_implementation_state") or "UNKNOWN"
        note = special.get(n, "Council lifecycle remains attributed; verify execution independently.")
        src = f"SRC-PIP-{n:02d}-{p['proposal_uuid'][:8].upper()}"
        link = f"../../archive/source-records/social-governance-semantic-enrichment/governance/{src}.json"
        rows.append(f"| [PIP-{n}]({link}) | {p['reviewed_title']} | {result} | {mechanism} | {impl} | {note} |")
    return """The PIP Registry is the evidence-qualified index of the 33 proposals captured on `main` as of 2026-07-15. It preserves proposal, vote, result, supersession, election meaning, Council-reported lifecycle, execution evidence, and research gaps as separate fields.

## Interpretation

`Result` is the reviewed vote or election result. `Council-reported lifecycle` is an attributed operational assessment, not independent verification:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

## Captured proposals

| PIP | Title | Result | Mechanism/category | Council-reported lifecycle | Qualification |
|---|---|---|---|---|---|
""" + "\n".join(rows) + """

## Registry rules

- Publication establishes a proposal, not approval.
- Passage establishes a DAO result, not payment or implementation.
- PIP-6 advancing candidates are not PIP-7's final winners.
- PIP-11, PIP-25, and PIP-27 retain unresolved winner identity.
- PIP-14, PIP-17, and PIP-31 preserve their passing vote and later Council-reported terminal state.
- PIP-23 supersedes PIP-4 without erasing PIP-4's historical record.

## Evidence references

- [Structured PIP registry](../../archive/semantic/governance/pip-registry-semantic.json)
- [PIP source reconciliation](../../archive/semantic/governance/pip-source-reconciliation.json)
- [PIP lifecycle](PIP-Lifecycle-and-Legislative-Process.md)
"""


def main():
    mapping = {pid: body for pid, body in PAGES.items()} | {pid: body for pid, body in INDEXES.items()}
    mapping["pip-registry"] = ("Star Atlas PIP Registry", build_pip_registry())
    paths = {json.loads(p.read_text(encoding="utf-8"))["page_id"]: json.loads(p.read_text(encoding="utf-8"))["proposed_path"] for p in PACKETS.glob("*.json")}
    for page_id, (title, body) in mapping.items():
        target = ROOT / paths[page_id]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(front(page_id, title) + body.strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
