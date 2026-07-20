---
title: "Holosim Release and Feature History"
seo_title: "Star Atlas Holosim: Release, Chapter and Feature History"
seo_description: "An evidence-qualified history of Holosim, from its 2025 public test through seasonal chapters, delays, browser systems, rewards claims, and mainnet boundaries."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 4
page_risk_class: R2
canonical_entity: PRODUCT-HOLOSIM
aliases:
  - "HoloSim"
  - "Star Atlas Holosim"
first_seen: 2025-06-04
last_reviewed: 2026-07-20
source_priority:
  - A2
related_entities:
  - Fleet Command
  - Star Atlas
  - zATLAS
depends_on:
  - knowledge/gameplay/Product-Registry.md
supersedes: []
superseded_by: []
evidence_basis:
  - "archive/source-records/campaign-delta-official/SRC-OFF-4850F98FBD1F1541.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-5E3C884FBE440C33.md"
  - "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-6DC571942A250D14.json"
  - "archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-D8337FA27E0A550A.json"
  - "knowledge/gameplay/Official-Current-State-Snapshot-2026-07-12.md"
known_limitations:
  - "The principal product page has no preserved publication or update date."
  - "Official current copy does not independently establish historical launch timing, user counts, economic outcomes, or delivery of every related Fleet Command feature."
  - "The X export preserves post text and point-in-time engagement, but linked media was not downloaded and the posts remain marked for semantic review."
research_gaps:
  - "Reconcile Holosim, Fleet Command, and later product terminology by build and environment."
  - "Preserve a versioned feature matrix for the June 2025 test, Chapter 1, Chapter 2, and later builds."
review_after: 2027-01-17
---

# Holosim Release and Feature History

Holosim is an official browser-based Star Atlas fleet simulation introduced publicly in June 2025 as a free-to-play test environment. First-party records distinguish that public test from later seasonal releases and from deployment to Star Atlas mainnet systems. The archived evidence supports a live browser product as of 2026-07-17; it does not support treating Holosim as the release of Fleet Command, C4, or every system tested within it.

## Identity and scope

The captured official product page describes Holosim as bringing Fleet Command-style strategic fleet gameplay to a browser, with fleet management, resource management, tactical combat, and an optional path toward the broader Star Atlas economy. These are official product claims, not independent measurements of depth, progression, or economic connection. [SRC-OFF-4850F98FBD1F1541](../../archive/source-records/campaign-delta-official/SRC-OFF-4850F98FBD1F1541.md)

Official support documentation separately states that no crypto wallet is required to start and that the game is designed for direct browser access. [SRC-OFF-5E3C884FBE440C33](../../archive/source-records/campaign-delta-official/SRC-OFF-5E3C884FBE440C33.md)

This page uses **Holosim** for the simulation itself and **Season 1, Chapter 1/2** for dated releases within it. "Fleet Command" is retained as an adjacent official product label, not an alias that proves identical software or lifecycle.

## Lifecycle chronology

| Date | Evidence state | Archival finding |
|---|---|---|
| 2025-06-04 | `TESTING` / public access | `SRC-X-STARATLAS-1930380671010385958` introduced Holosim and said its test phase was live. This is the earliest dated first-party lifecycle record in the repository, not necessarily the first development work. |
| 2025-06-04 | test purpose and feature claims | `SRC-X-STARATLAS-1930380673174647013` said Holosim was used to test features before they went live on mainnet. It named combat, a SAGE-branded AI assistant, route management, tutorials, and quests. Those claims establish the test build's stated scope; they do not establish later mainnet delivery. |
| 2025-08-19 | `ANNOUNCEMENT` / scheduled event | `SRC-X-STARATLAS-1957894973908779360` announced that Season 1, Chapter 1 would begin the next day and advertised $35,000 in rewards. The amount is an official program statement, not a verified payout total. |
| 2025-08-20 | `LIVE` / Chapter 1 | `SRC-X-STARATLAS-1958322079927079252` stated that Season 1, Chapter 1 was live. This is a chapter release within Holosim, not evidence of mainnet deployment. |
| 2026-02-18 | `DELAYED` | `SRC-X-STARATLAS-2024197285215948920` said technical difficulties would cause the planned February 19 Chapter 2 launch to be missed. February 19 is therefore a failed plan, not a release date. |
| 2026-03-04 | `PLANNED` / rescheduled | `SA-DISCORD-ANN-6DC571942A250D14` rescheduled Chapter 2 for March 10 and credited playtesters with finding late issues. This supports testing before release, but no independent quality result. |
| 2026-03-10 | `LIVE / UPDATED` / Chapter 2 | `SRC-X-STARATLAS-2031445052623606253` and `SA-DISCORD-ANN-D8337FA27E0A550A` stated that Chapter 2 was live. The Discord record describes the released build in greater operational detail. |

The official website snapshot captured on 2026-07-12 linked an active Holosim portal and described the product as available. Together, the dated records support `LIVE / UPDATED` for the browser surface as of the capture date. They do not establish that every adjacent Fleet Command roadmap feature was delivered. [Official current-state snapshot](Official-Current-State-Snapshot-2026-07-12.md)

## Documented systems by evidence date

The December 2025 support corpus is a dated operational snapshot, not proof that each mechanic existed in the June test or at initial release. It documents:

- fleet formation and management, including ships, crew, cargo, docking, orders, and settings ([SRC-OFF-C38C56C97A26AB91](../../archive/source-records/campaign-delta-official/SRC-OFF-C38C56C97A26AB91.md); [SRC-OFF-4D11337D80379C85](../../archive/source-records/campaign-delta-official/SRC-OFF-4D11337D80379C85.md));
- mining, transport, crafting, quests, and automation ([SRC-OFF-B263E0E5565CB9ED](../../archive/source-records/campaign-delta-official/SRC-OFF-B263E0E5565CB9ED.md); [SRC-OFF-6A9A3D6A006E3C8E](../../archive/source-records/campaign-delta-official/SRC-OFF-6A9A3D6A006E3C8E.md); [SRC-OFF-7E2651A64522DACE](../../archive/source-records/campaign-delta-official/SRC-OFF-7E2651A64522DACE.md); [SRC-OFF-854CB512DFE80EA1](../../archive/source-records/campaign-delta-official/SRC-OFF-854CB512DFE80EA1.md));
- tactical combat and conditions for protection from attack ([SRC-OFF-0BFA050EF12E2E17](../../archive/source-records/campaign-delta-official/SRC-OFF-0BFA050EF12E2E17.md); [SRC-OFF-61C2E976FF41FD91](../../archive/source-records/campaign-delta-official/SRC-OFF-61C2E976FF41FD91.md)); and
- simulated `zATLAS`, browser persistence, and character creation ([SRC-OFF-0449B94A36A8B803](../../archive/source-records/campaign-delta-official/SRC-OFF-0449B94A36A8B803.md); [SRC-OFF-9A02CD416A9E0A34](../../archive/source-records/campaign-delta-official/SRC-OFF-9A02CD416A9E0A34.md); [SRC-OFF-92912CC09853EF08](../../archive/source-records/campaign-delta-official/SRC-OFF-92912CC09853EF08.md)).

The Chapter 2 launch record adds faction-specific storylines, territory control measured through Dominion Points, mining achievements, NPC marketplace orders, notifications, a battle log and revised combat interface. It also reports a technical migration from the Starcomm v2 relay to direct RPC data. These are first-party release claims for the March 10 build; the archive does not independently benchmark reliability or verify every claimed behavior. [SA-DISCORD-ANN-D8337FA27E0A550A](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-D8337FA27E0A550A.json)

## Build-qualified feature ledger

| Feature or claim | Earliest supported surface in this archive | State and limitation |
|---|---|---|
| Browser/no-wallet entry | Official product and support copy | Documented by late 2025; not necessarily present in every earlier test build. |
| Combat, routes, tutorial, quests, SAGE-branded assistant | June 2025 public test statement | `TESTING`; does not prove later mainnet delivery or relationship to the SAGE product family. |
| Season 1 rewards | Chapter 1 announcement | USD 35,000 advertised; payout completion unverified. |
| Fleet, mining, crafting, transport, automation | December 2025 support suite | Dated functional snapshot; first availability unresolved. |
| Dominion Points, faction storylines, NPC marketplace orders | Chapter 2 live statement | `LIVE` in the March 10 build as officially stated; behavior not independently benchmarked. |
| Starcomm v2 to direct RPC migration | Chapter 2 Discord release statement | Publisher-reported technical migration; code/deployment evidence absent. |
| `sage-holosim` decoder and program mapping | First-party decoder repository record | Decoder support does not prove current deployment or mainnet status. [SRC-OFF-B3E826AFA52FB19B](../../archive/source-records/campaign-delta-official/SRC-OFF-B3E826AFA52FB19B.md) |

## Economic and persistence boundary

`zATLAS` is documented as an in-simulation currency. It must not be conflated with the on-chain ATLAS token or treated as evidence of transferable value. Likewise, the June 2025 statement that Holosim tests features "before mainnet" makes the simulation/mainnet boundary explicit. The archived sources support a route from a no-wallet entry experience toward the wider Star Atlas ecosystem, but not a claim that Holosim progress, assets, or rewards universally transfer on-chain.

Holosim's relationship to Fleet Command is a product relationship stated by official copy; it is not evidence that the separate Fleet Command roadmap surface reached general release. Chapter 2's use of marketplace orders and subscription-linked progression also should not be generalized beyond that build without later evidence.

## Current state

As of 2026-07-17, the supported lifecycle state is `LIVE / UPDATED` for the browser surface. Feature status remains build-specific, and Holosim test availability is not evidence of mainnet deployment.

## Historical value

Holosim records a distinct institutional strategy: a no-wallet browser simulation used both as a public acquisition surface and as a pre-mainnet test environment. Its sequence is unusually well preserved because the archive contains a first-party test announcement, a later chapter release, a documented delay and reschedule, a second release, and dated support documentation. That sequence permits future researchers to distinguish product availability from promised integration and advertised outcomes.

## Conflicts and missing artifacts

The decoder repository maps a `sage-holosim` program, but the captured Mainnet Program IDs page does not list that address. This is an unresolved documentation mismatch, not evidence that the program is absent or live. Required artifacts include versioned release notes, deployment and upgrade transactions, program authority, reward payment records, the Starcomm retirement/migration record, feature telemetry, and an authoritative product relationship among Holosim, Fleet Command, SAGE, and C4.

## Review status

`QUALIFIED`. The public test, Chapter 1, delay, reschedule, and Chapter 2 release chronology is strong. Mainnet relationship, reward outcomes, and technical deployment remain unresolved.

## Evidence references

- [Official Holosim page record](../../archive/source-records/campaign-delta-official/SRC-OFF-4850F98FBD1F1541.md)
- [Official X normalized records](../../archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl)
- [Chapter 2 rescheduling record](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-6DC571942A250D14.json)
- [Chapter 2 live record](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-D8337FA27E0A550A.json)
- [Product Registry](Product-Registry.md)
