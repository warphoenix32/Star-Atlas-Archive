---
title: "Star Atlas Product Registry"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 5
page_risk_class: R2
evidence_basis:
  - "archive/semantic/atlas-brew/segment-index.json"
  - "archive/source-records/campaign-delta-official/"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-F863D82FBAF30DF9.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-6DF1790F1F2402FA.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-A37A8B7B245E7776.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-9FFFF91025488D09.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-76D9861DCB3FE798.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-CCF4600A4C08F697.json"
  - "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl"
  - "knowledge/gameplay/Official-Current-State-Snapshot-2026-07-12.md"
known_limitations:
  - "Current-state statements are date-bound."
  - "Absence of evidence is not evidence of non-occurrence."
research_gaps:
  - "Independent execution evidence remains incomplete where explicitly noted."
review_after: 2027-01-15
---

# Star Atlas Product Registry
This registry is an evidence-qualified map of major Star Atlas product surfaces. It is not a marketing catalog and does not assume that products sharing terminology, lore, interfaces, or mechanics share a single codebase. Lifecycle labels are current only as of 2026-07-17 and do not convert roadmap language into delivery.

## How to read this registry

Each row identifies the strongest state supported for the named surface, not the completion of every feature ever associated with it. `LIVE` means that first-party or sufficiently corroborated evidence states that a public product was available. `UPDATED` means a later named release or documented revision exists. `TESTING` identifies limited, pre-release, early-access, or PTR availability. An official current page without a publication date can support current positioning when paired with a dated capture, but it cannot establish historical launch timing.

## Registry

| Product | Entity ID | Supported lifecycle | Earliest or decisive evidence | Qualification |
|---|---|---|---|---|
| PLAY | PRODUCT-PLAY | `LIVE` | Dated current-state capture, 2026-07-12 | Official account and asset hub. Capture confirms discoverability, not continuous historical uptime. |
| [SCORE / Faction Fleet](SCORE-and-Faction-Fleet.md) | PRODUCT-SCORE | `DEPRECATED` | Official release publication, 2021-12-17; Aephia reports 2021-12-16 availability | Historical fleet-staking surface. Its economic role was later wound down during Starbased; software and emissions deprecation should remain distinct. |
| [SAGE / SAGE Labs](SAGE.md) | PRODUCT-SAGE | `LIVE / UPDATED` | SAGE Labs stated live, 2023-09-21; Starbased stated live, 2024-04-04 | S.C.R.E.A.M., SAGE Labs, Starbased, SAGE 3D and C4 are separate lifecycle stages or surfaces. |
| [UE5 / Showroom](UE5-Showroom.md) | PRODUCT-UE5 | `TESTING / UPDATED` | Pre-alpha access 2022-09-29; launch statement 2022-09-30; R2.1 release 2023-06-02 | Early-access client with build-specific capabilities. Planned features are not assumed delivered. |
| Fleet Command | PRODUCT-FLEET-COMMAND | `IN_DEVELOPMENT` | Undated official page in 2026-07-12 capture | Official page describes development and the product registry labels it coming soon. No general release is asserted. |
| [Holosim](Holosim.md) | PRODUCT-HOLOSIM | `LIVE / UPDATED` | Public test live 2025-06-04; Chapter 1 live 2025-08-20; Chapter 2 live 2026-03-10 | A browser simulation and pre-mainnet test environment. It is related to, but does not prove release of, Fleet Command. |
| C4 / C4 PTR | unresolved | `TESTING` | Official PTR documentation, 2026-06-02 | Support records establish user-accessible PTR mining and test systems, not mainnet or general release. |
| Escape Velocity | unresolved | `SUPERSEDED` | Limited public alpha reported 2023-04-26; official technology description 2023-04-27 | Historical, time-bounded on-chain movement test. It preceded SAGE Labs and is not a current SAGE release. |
| [Galactic Marketplace](Galactic-Marketplace.md) | PRODUCT-MARKETPLACE | `LIVE / UPDATED` | Operational release claimed 2021-08-04; replacement marketplace announced 2022-07-22 | The 2021 marketplace and 2022 replacement are separate lifecycle events. |
| DAO portal | PRODUCT-DAO-PORTAL | `LIVE / UPDATED` | Governance and locking platform launched 2022-07-21; formal PIP system followed in 2023 | Portal availability does not establish proposal passage, implementation, or payment. |
| Star Atlas Build | PRODUCT-BUILD | `LIVE` | Official developer documentation in current corpus | Documentation and resource hub; documentation dates do not prove historical feature availability. |

## Lifecycle rules

The controlled states are FIRST_MENTION, PLANNED, IN_DEVELOPMENT, TESTING, LIVE, UPDATED, DEGRADED, RESOLVED, SUPERSEDED, DEPRECATED, CANCELED, and UNKNOWN. A state is assigned to a named product or feature and a dated evidence record. Announcement, test access, public release, and delivery of all promised features remain separate.

For products with multiple surfaces, the lifecycle attaches to the narrowest named object supported by evidence. For example:

- SAGE Labs can be `LIVE` while SAGE 3D's exact release date remains unresolved and C4 remains `TESTING`.
- Holosim Chapter 2 can be `LIVE` without making Fleet Command or Holosim-tested features `LIVE` on mainnet.
- A marketplace replacement can be `ANNOUNCED` even though the preceding marketplace was already `LIVE`.
- A support article can document a feature as of late 2025 without proving that it shipped at the product's first release.

## Historical relationships

The product record contains two especially important succession chains. SCORE/Faction Fleet supplied an early passive ship-enlistment and reward surface; Starbased later reduced that reward role while redirecting incentives toward active SAGE play. Separately, S.C.R.E.A.M. became the SAGE roadmap identity, followed by SAGE Labs and the Starbased update, while later SAGE 3D and C4 records require build-specific treatment.

Holosim sits beside those chains rather than cleanly inside either one. Official copy positions it as a browser-accessible fleet simulation and says it tests features before mainnet. That makes it useful evidence of product experimentation, but insufficient evidence for undocumented code lineage among Holosim, Fleet Command, SAGE, and C4.

## Registry limitations and review needs

- The registry is selective; absence does not mean that a product, build, or service never existed.
- `unresolved` entity IDs are retained until the repository establishes a canonical entity rather than inventing one here.
- Availability, uptime, adoption, payouts, and technical performance are separate questions. A release statement establishes the publisher's public release claim, not independent operational success.
- Complete post-R2.1 Showroom, SAGE 3D, C4, and Fleet Command chronologies remain research priorities.

## Evidence references

- [Official current-state snapshot](Official-Current-State-Snapshot-2026-07-12.md)
- [Atlas Brew semantic segments](../../archive/semantic/atlas-brew/segment-index.json)
- [Official source records](../../archive/source-records/campaign-delta-official/)
- [Product Timeline](../timeline/Product-Timeline.md)
