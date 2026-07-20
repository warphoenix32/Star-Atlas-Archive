---
title: "UE5 Showroom History"
seo_title: "Star Atlas UE5 Showroom: Release and Build History"
seo_description: "A source-linked history of the Star Atlas Unreal Engine 5 Showroom, including pre-alpha access, its 2022 launch, Showroom R2.1, and unresolved later build lineage."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 4
page_risk_class: R2
canonical_entity: PRODUCT-UE5
aliases:
  - "Showroom"
  - "Star Atlas Showroom"
evidence_basis:
  - "archive/source-records/campaign-delta-official/SRC-OFF-340128795CCA03A9.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-57027457FD1317B4.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-C6B9C26055452AF8.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-FC61779037A23908.md"
  - "archive/semantic/atlas-brew/segment-index.json"
known_limitations:
  - "The repository does not yet preserve a complete release-note series after Showroom R2.1."
  - "Atlas Brew speaker identity remains unknown; its segments are useful for recording-and-timestamp discovery, not named attribution."
research_gaps:
  - "Recover every Showroom build, patch note, access condition, and deprecation or successor notice."
  - "Reconcile Showroom, later UE5 client terminology, C4, and any successor build without treating them as aliases by default."
review_after: 2027-01-20
---

# UE5 Showroom History

The Showroom was Star Atlas's first publicly documented Unreal Engine 5 client environment. It began as a pre-alpha presentation and gameplay surface distributed through the Epic Games Store, then acquired named revisions such as Showroom R2.1. It should be read as a build history—not as proof that every feature ever discussed for the Star Atlas Unreal client existed from launch.

## Identity and scope

“UE5” describes the technology family; “Showroom” names a product surface. Later Star Atlas Unreal builds may descend from, replace, or substantially change that surface, but they are not automatically aliases. This page therefore uses **UE5 Showroom** for the 2022–2023 client records and leaves later product lineage qualified until explicit release or migration evidence connects it.

Official material associated the Showroom with high-fidelity ships and environments, Epic Games Store distribution, and expanding gameplay tests. Those descriptions establish publisher positioning and named build content. They do not establish feature completeness, uninterrupted access, performance, or delivery of the wider MMO roadmap.

## Lifecycle chronology

| Date | Evidence state | Archival finding |
|---|---|---|
| 2022-09-29 | `ACCESS_INSTRUCTIONS / PRE_ALPHA` | ATMTA published instructions for entering the pre-alpha Showroom and separately framed it as a handcrafted metaverse journey. These records establish the intended access path and contemporary positioning. [SRC-OFF-340128795CCA03A9](../../archive/source-records/campaign-delta-official/SRC-OFF-340128795CCA03A9.md) [SRC-OFF-57027457FD1317B4](../../archive/source-records/campaign-delta-official/SRC-OFF-57027457FD1317B4.md) |
| 2022-09-30 | `RELEASE_CLAIMED / PRE_ALPHA` | An official announcement stated that the Unreal Engine 5-powered pre-alpha Showroom had launched on the Epic Games Store. This is strong first-party release evidence for that named pre-alpha build. [SRC-OFF-C6B9C26055452AF8](../../archive/source-records/campaign-delta-official/SRC-OFF-C6B9C26055452AF8.md) |
| 2023-06-02 | `UPDATED / R2.1` | ATMTA announced Showroom 2.1 as a game release connected to a racing season. The record supports a named revision and dated content expansion; it does not imply that all later UE5 roadmap systems were delivered. [SRC-OFF-FC61779037A23908](../../archive/source-records/campaign-delta-official/SRC-OFF-FC61779037A23908.md) |
| 2026-07-12 | current official UE access `OBSERVED` | The official homepage linked an Unreal Engine client through the Epic Games Store and described a broader set of gameplay experiences. Because the captured page did not establish that every statement applied to the historical Showroom lineage, the repository does not silently merge the current client with every earlier build. [Official current-state snapshot](Official-Current-State-Snapshot-2026-07-12.md) |

## Build-qualified feature treatment

The archive follows four rules when reading Showroom evidence:

1. A feature described in a launch article belongs to that article's named or dated build unless later evidence broadens it.
2. Test or early-access availability is not general release.
3. A roadmap discussion is not a shipped feature, even when a speaker uses confident future tense.
4. A later build may supersede an earlier build without making every old mechanic active in the successor.

Atlas Brew preserves extensive Showroom and Unreal discussions with exact recording and timestamp references. Those segments can identify when a topic was discussed and direct a researcher to the external video. Because normalized speakers remain `UNKNOWN`, a segment cannot support a named personal commitment unless independent attribution is recovered. Information about a product or build can still be useful when the wording, source recording, and timestamps are clear. [Atlas Brew segment index](../../archive/semantic/atlas-brew/segment-index.json)

## Current state

As of 2026-07-20, the historical Showroom has strong evidence for `PRE_ALPHA_RELEASED` in September 2022 and `UPDATED` through R2.1 in June 2023. The repository does not yet have enough versioned evidence to assign a precise current lifecycle state to the historical Showroom entity itself. The broader Unreal client had an official access path in July 2026, but its exact relationship to each Showroom build remains under review.

This distinction avoids two errors: declaring the entire Unreal product merely “testing” forever, and declaring every Unreal roadmap feature live because a later client exists.

## Relationship to C4 and other products

C4 is documented separately as a Public Test Realm in 2026. SAGE, Holosim, Fleet Command, and the Galactic Marketplace also have independent product and lifecycle records. Shared ships, lore, accounts, interfaces, or technical components do not prove identical code lineage or synchronized release states.

## Historical value

The Showroom marks the transition from Star Atlas's early asset, marketplace, and browser/on-chain surfaces into a publicly accessible high-fidelity Unreal environment. Its pre-alpha label is historically important: it records both genuine public access and the narrow maturity claim made at release.

## Known limitations and missing artifacts

The archive still needs every post-R2.1 release note; build numbers and checksums; Epic Games Store version history; access requirements by build; outage and deprecation notices; and an explicit successor or migration statement connecting the Showroom to later Unreal and C4 terminology.

## Related pages

- [Star Atlas Product Registry](Product-Registry.md)
- [Official Current-State Snapshot](Official-Current-State-Snapshot-2026-07-12.md)
- [Star Atlas Technical Platform](../technology/Technical-Platform.md)
- [Product Timeline](../timeline/Product-Timeline.md)

## Review status

`QUALIFIED`, last reviewed 2026-07-20. The dated pre-alpha and R2.1 records are high-confidence first-party evidence. Later lineage and current-state continuity remain unresolved rather than inferred.
