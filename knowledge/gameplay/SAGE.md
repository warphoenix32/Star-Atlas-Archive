---
title: "SAGE"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 5
page_risk_class: R2
canonical_entity: PRODUCT-SAGE
aliases:
  - "Star Atlas: Golden Era"
  - "SAGE Labs"
  - "SAGE Labs Starbased"
  - "Project S.C.R.E.A.M."
first_seen: 2022-04-29
last_reviewed: 2026-07-17
source_priority:
  - A2
  - B1
  - B2
evidence_basis:
  - "archive/source-records/campaign-delta-official/SRC-OFF-0A646AE069AFFBA5.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-22181D98D7A1B870.md"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-F863D82FBAF30DF9.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-6DF1790F1F2402FA.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-A37A8B7B245E7776.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-9FFFF91025488D09.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-76D9861DCB3FE798.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-CCF4600A4C08F697.json"
known_limitations:
  - "The page synthesizes a product family whose named phases and interfaces changed over time."
  - "Current support documentation establishes a late-2025 functional snapshot, not the first availability date of each mechanic."
  - "Community evidence for SAGE 3D remains month-level and does not establish an exact official release date."
research_gaps:
  - "Resolve the exact public release date, distribution surface, and lifecycle of SAGE 3D."
  - "Map feature availability by SAGE Labs, Starbased, SAGE 3D, and C4 build without inferring undocumented architecture."
  - "Identify authoritative deprecation dates for earlier game IDs and interfaces."
review_after: 2027-01-17
---

# SAGE

SAGE—Star Atlas: Golden Era—is the browser-based, on-chain strategy product family developed from the earlier Project S.C.R.E.A.M. concept. The archive documents several distinguishable stages: a prototype-era S.C.R.E.A.M. presentation, the SAGE roadmap and naming transition, the 2023 SAGE Labs release, the 2024 Starbased economic and faction-infrastructure update, a community-reported SAGE 3D release, and later C4 testing. These labels must not be collapsed into a single release event or assumed to describe the same interface and feature set.

## Identity and institutional role

Official late-2025 support documentation describes SAGE Labs as a browser-based 4X strategy game built on Solana. Its stated loop includes fleet formation, exploration, mining, crafting, transport, faction competition, and an on-chain economy using ATLAS. This is first-party documentation of the supported product at the capture date; it does not independently verify economic outcomes, uninterrupted availability, or the first appearance of each mechanic. [SRC-OFF-0A646AE069AFFBA5](../../archive/source-records/campaign-delta-official/SRC-OFF-0A646AE069AFFBA5.md)

SAGE is best treated as a product family rather than an immutable build:

- **Project S.C.R.E.A.M.** is the early development name preserved in 2022 prototype and roadmap evidence.
- **SAGE / Star Atlas: Golden Era** is the umbrella identity announced in November 2022.
- **SAGE Labs** is the browser release stated live on 2023-09-21.
- **Starbased** is an update to SAGE Labs centered on shared starbases, Loyalty Points, Council Rank XP, epochs, and revised emissions.
- **SAGE 3D** is a later interface/build reported by Aephia; the archive lacks an exact official launch record.
- **C4 PTR** is a later testing surface with its own lifecycle and must not be treated as general release or as proof that all SAGE roadmap elements shipped.

## Lifecycle chronology

| Date | Evidence state | Archival finding |
|---|---|---|
| 2022-04-29 | `IN_DEVELOPMENT` / prototype | Official Discord invited users to view what S.C.R.E.A.M. would look like and explicitly described the project as in a "PROTOTYPING" stage (`SA-DISCORD-ANN-F863D82FBAF30DF9`). This establishes public prototype disclosure, not playable release. |
| 2022-11-07 | `ROADMAP` / renamed | ATMTA's Breakpoint publication presented Project S.C.R.E.A.M. as Star Atlas: Golden Era and described a wider product roadmap. It is the principal archived naming transition, not a launch. [SRC-OFF-22181D98D7A1B870](../../archive/source-records/campaign-delta-official/SRC-OFF-22181D98D7A1B870.md) |
| 2023-09-15 | `ANNOUNCEMENT` / scheduled | Official Discord announced that SAGE Labs would launch September 21 (`SA-DISCORD-ANN-6DF1790F1F2402FA`). The plan is preserved separately from execution. |
| 2023-09-21 | `LIVE` / SAGE Labs | Official Discord stated that SAGE Labs was live (`SA-DISCORD-ANN-A37A8B7B245E7776`). This is the strongest first-party release anchor in the repository. |
| 2024-03-26 | `ANNOUNCEMENT` / Starbased | Official Discord announced Starbased for April 2 as a SAGE Labs update introducing starbase upgrading and upkeep, Loyalty Points and revised emissions (`SA-DISCORD-ANN-9FFFF91025488D09`). |
| 2024-04-02 | `DELAYED` | Official Discord delayed the launch to the following day because of failed transactions and transaction times during program deployment (`SA-DISCORD-ANN-76D9861DCB3FE798`). The announced next-day target is not itself proof of release. |
| 2024-04-04 | `LIVE / UPDATED` / Starbased | Official Discord stated that Starbased was live (`SA-DISCORD-ANN-CCF4600A4C08F697`). The release began with zero ATLAS in its first epoch and no LP deposits, an important limitation on what "live" meant at launch. |
| estimated 2024-12 | community-reported release / SAGE 3D | Aephia's year-end review reports a mid-December SAGE 3D launch while also describing missing quality-of-life features and continuing relevance for SAGE Labs. [SRC-AEPHIA-C9AE050CD9C1886D](../../archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-C9AE050CD9C1886D.md) The exact day and official release record remain unresolved. |
| 2026-06-02 | `TESTING` / C4 PTR documentation | Official support records document user-accessible C4 PTR mechanics. PTR evidence is not mainnet or general-release evidence. [SRC-OFF-E061D3A6454697AB](../../archive/source-records/campaign-delta-official/SRC-OFF-E061D3A6454697AB.md) |

Atlas Brew also discussed SAGE Labs in release language at `SRC-ATLAS-BREW-0034`, 00:02:33–00:04:33 (`SEG-ATLAS-BREW-0034-0002`). Because speaker identity is not normalized, the segment supports public discussion and chronology but no named-speaker attribution. [Segment evidence](../../archive/semantic/atlas-brew/segment-index.json)

## Starbased transition and economic significance

The March 2024 announcement described Starbased as more than a cosmetic release. It introduced faction-level starbase construction and upkeep, Loyalty Points and epoch rewards, and changes to pre-existing emissions. The source states that Faction Fleet emissions would be reduced at launch and that the prior game ID's economic variables would later be set to zero. Those are announced transition rules; the April 4 live post establishes the new surface's availability but does not independently prove that every scheduled deprecation occurred exactly as planned.

The April 4 release record also qualifies the initial implementation: the first epoch carried zero ATLAS rewards and LP could be earned but not deposited. Researchers should therefore distinguish **software availability**, **feature activation**, and **economic execution** rather than describing the entire announced economy as fully operational on launch day.

Late-2025 official support documentation describes the mature Starbased surface as including collaborative starbase upkeep, Loyalty Points, Council Rank XP, epochs, local markets, mining and crafting. Those records are authoritative for what support documentation stated by December 2025, not proof of continuous operation or original launch timing. [SRC-OFF-A6A4A97A9D09AA1E](../../archive/source-records/campaign-delta-official/SRC-OFF-A6A4A97A9D09AA1E.md) [SRC-OFF-EF4F170FCDBC4B94](../../archive/source-records/campaign-delta-official/SRC-OFF-EF4F170FCDBC4B94.md) [SRC-OFF-1206858B54C3E67E](../../archive/source-records/campaign-delta-official/SRC-OFF-1206858B54C3E67E.md)

## Product and evidence boundaries

- **Roadmap is not release.** The 2022 SAGE naming and roadmap record cannot establish the 2023 build's availability.
- **Launch announcement is not launch.** September 15 and March 26 are scheduling evidence; September 21 and April 4 are the corresponding live statements.
- **Delay is not execution.** The April 2 delay named a new target but the repository's supported Starbased live date is April 4.
- **Testing is not production.** Escape Velocity and C4 PTR are related experiments or testing surfaces, not evidence that every SAGE system was generally available.
- **Documentation is not historical proof.** December 2025 support pages establish a dated functional baseline without backdating mechanics to 2023 or 2024.
- **Product naming is not architecture.** The public labels reveal institutional product positioning but do not prove code inheritance or shared technical architecture.

## Current state

As of 2026-07-17, first-party archived material supports `LIVE / UPDATED` for the SAGE product family: SAGE Labs was stated live on 2023-09-21, Starbased was stated live on 2024-04-04, and official support documentation described a functioning Starbased surface in December 2025. C4 is supported only as `TESTING` in PTR evidence. The corpus does not establish that every roadmap phase, interoperability claim, announced economic transition, or proposed mechanic has shipped or remains active.

## Historical value

SAGE is central to Star Atlas institutional history because its surviving records span product conception, renaming, public release, economic redesign, partial deprecation of an older reward surface, and later test environments. The record also shows why a single "launch date" is inadequate: different dates attach to the family name, SAGE Labs, Starbased, SAGE 3D, and C4 PTR.

## Related pages

- [Product Registry](Product-Registry.md)
- [Product Timeline](../timeline/Product-Timeline.md)
- [SCORE and Faction Fleet](SCORE-and-Faction-Fleet.md)
- [Official Discord announcement corpus](../../archive/normalized/discord-announcements/messages/)
