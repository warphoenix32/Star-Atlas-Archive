---
title: "Star Atlas Entity Relationship Map"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 4
page_risk_class: R2
canonical_entity: STAR-ATLAS-ECOSYSTEM
aliases:
  - "Star Atlas institutional map"
  - "Star Atlas knowledge ontology"
first_seen: 2026-07-15
last_reviewed: 2026-07-17
source_priority:
  - A1
  - A2
  - A3
related_entities:
  - Star Atlas DAO
  - Star Atlas Foundation
  - Star Atlas Council
  - ATMTA
  - Ecosystem Fund
  - SAGE
  - SCORE / Faction Fleet
  - UE5 Showroom
  - Galactic Marketplace
  - Holosim
  - DAO Treasury
  - PVP
depends_on:
  - knowledge/governance/PIP-Registry.md
  - knowledge/organizations/Institutional-Overview.md
  - knowledge/gameplay/Product-Registry.md
supersedes: []
superseded_by: []
evidence_basis:
  - "knowledge/governance/PIP-Registry.md"
  - "knowledge/governance/Governance-and-Economy-Overview.md"
  - "knowledge/organizations/Institutional-Overview.md"
  - "knowledge/gameplay/Product-Registry.md"
known_limitations:
  - "This is a navigational ontology, not a canonical graph export."
  - "Relationships are summarized from reviewed knowledge pages and remain subject to each linked page's evidence qualifications."
research_gaps:
  - "Current staff, service-provider, and product relationships require periodic review."
  - "Official social collections remain incomplete outside their captured date ranges and linked media binaries."
review_after: 2027-01-15
---

# Star Atlas Entity Relationship Map

This page is the human-readable ontology for the repository. It shows how the principal institutions, governance instruments, products, technical surfaces, sources, and programs relate without replacing the evidence-bearing pages or the future machine-readable graph layer.

## Institutional core

| Entity | Primary role | Key relationships |
| --- | --- | --- |
| [Star Atlas DAO](governance/Star-Atlas-DAO.md) | POLIS-based collective decision system | votes on PIPs; elects Council members; authorizes treasury and policy actions |
| [Star Atlas Foundation](governance/Star-Atlas-Foundation.md) | legal and administrative implementation body | administers proposal compliance; mediates lawful implementation; remains distinct from the electorate |
| [Star Atlas Council](governance/Star-Atlas-Council.md) | elected governance-process steward | assists authors; administers delegated programs; reports milestones and payments where assigned |
| [ATMTA](organizations/ATMTA.md) | principal developer and operating company | develops Star Atlas products; may implement or support approved ecosystem work |
| [Ecosystem Fund](governance/Ecosystem-Fund.md) | DAO funding policy instrument | governed by PIP-23; supports approved ecosystem proposals; administered through defined institutional roles |

## Governance relationships

```text
POLIS holders / Star Atlas DAO
  ├─ vote on → PIPs
  ├─ elect through → Council election PIPs
  └─ authorize → treasury and policy actions

Star Atlas Foundation
  ├─ reviews → proposal compliance
  ├─ administers → governance procedures where assigned
  └─ implements or declines → authorized actions subject to legal and safety constraints

Star Atlas Council
  ├─ assists → PIP authors
  ├─ stewards → governance operations
  ├─ administers → delegated programs
  └─ reports or verifies → milestones and payments where delegated

PIP-23
  └─ supersedes → PIP-4
```

The [PIP Lifecycle and Legislative Process](governance/PIP-Lifecycle-and-Legislative-Process.md) defines how proposals move from draft to result. [Governance Implementation and Evidence States](governance/Governance-Implementation-and-Evidence-States.md) defines why passage, payment, implementation, and independently verified completion remain separate.

## Product and gameplay relationships

| Product or system | Relationship to the ecosystem |
| --- | --- |
| [SCORE / Faction Fleet](gameplay/SCORE-and-Faction-Fleet.md) | early fleet-management and reward system; historical predecessor context for later strategic gameplay |
| [SAGE](gameplay/SAGE.md) | strategy and economic gameplay family; related to fleet, resource, marketplace, and progression systems |
| [UE5 Showroom](gameplay/UE5-Showroom.md) | Unreal Engine client surface for ship and environment experiences |
| [Galactic Marketplace](gameplay/Galactic-Marketplace.md) | asset and economic exchange surface connected to ships, resources, and the broader token economy |
| [Holosim](gameplay/Holosim.md) | browser fleet simulation with dated test, Chapter 1, and Chapter 2 lifecycle evidence |

The [Product Registry](gameplay/Product-Registry.md) is the canonical navigation layer for product identities, aliases, and lifecycle states. Product relationships do not imply that all announced integrations or roadmap features were delivered.

## Economy and infrastructure relationships

- The [Governance and Economy Overview](governance/Governance-and-Economy-Overview.md) connects POLIS voting, treasury policy, and ecosystem funding while preserving evidence boundaries.
- [PVP Voting Power](economy/PVP-Voting-Power.md) defines vote weight; [DAO Treasury Architecture](economy/DAO-Treasury-Architecture.md) distinguishes the general treasury from the bounded Ecosystem Fund.
- The [Economy index](economy/README.md) contains economic reports and token-focused knowledge.
- The [Technology index](technology/README.md) contains platform and infrastructure surfaces supporting products and services.
- Council-reported payments and milestones remain attributed operational records unless independently reconciled to transactions or deliverables.

## Communications and evidence relationships

| Source domain | Knowledge role |
| --- | --- |
| Official PIP portal captures | proposal text, vote mechanism, vote totals, and formal governance design |
| Council PIP tracker | attributed operational status, milestone, payment, and accomplishment assessments |
| Official social posts | announcement, release, event, and lifecycle evidence after semantic review |
| Reviewed transcripts | contextual explanation and attributed statements when speaker identity is known |
| [Official Discord announcements](media/Official-Discord-Announcements-Profile.md) | qualified profile of the merged archive and semantic corpus; author inference and missing attachments remain visible limitations |
| [Official X account](media/Official-X-Account-Profile.md) | official statements within the captured period; retweets retain secondary-source attribution |
| [Official Medium publication](media/Star-Atlas-Medium-Publication-Profile.md) | qualified source profile only until an exhaustive article-level corpus review is completed |

## Navigation by question

- **Who has authority?** Start with [Governance Knowledge](governance/README.md).
- **Which organization performed an action?** Start with [Organizations](organizations/README.md).
- **What product or game system is involved?** Start with [Gameplay and Products](gameplay/README.md).
- **When did something happen?** Start with the [Living Timeline](timeline/README.md).
- **What evidence supports a claim?** Follow the evidence references on the relevant page into the archive and semantic layers.

## Known limitations

This map summarizes reviewed relationships; it does not create canonical graph triples. A linked page's status, date scope, source authority, contradictions, and research gaps govern the interpretation of each relationship.

## See Also

- [Knowledge Overview](README.md)
- [Governance Knowledge](governance/README.md)
- [Organizations](organizations/README.md)
- [Gameplay and Products](gameplay/README.md)
- [Master Timeline](timeline/README.md)
- [Entity and Source Indexes](index/README.md)
