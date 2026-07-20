---
title: "Galactic Marketplace History"
seo_title: "Star Atlas Galactic Marketplace: History and Evidence"
seo_description: "An evidence-qualified history of the Star Atlas Galactic Marketplace, from the 2021 trading surface through the 2022 replacement and later support documentation."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 4
page_risk_class: R2
canonical_entity: PRODUCT-MARKETPLACE
aliases:
  - "Star Atlas Marketplace"
evidence_basis:
  - "archive/source-records/campaign-delta-official/SRC-OFF-A465C97640C55838.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-0C5AA46E01E189EC.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-1EE2242A6F7844FF.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-B38AFD8A2122994F.md"
  - "knowledge/gameplay/Official-Current-State-Snapshot-2026-07-12.md"
known_limitations:
  - "Official release language does not independently verify uninterrupted operation, liquidity, pricing, settlement, or user adoption."
  - "The exact contract and interface migration history between the 2021 and 2022 surfaces remains incomplete."
research_gaps:
  - "Recover dated interface captures and deployment records for both marketplace generations."
  - "Reconcile program upgrades, fee changes, asset support, outages, and deprecations against on-chain and release evidence."
review_after: 2027-01-20
---

# Galactic Marketplace History

The Galactic Marketplace is Star Atlas's official asset-trading surface. Its history is not one uninterrupted product state: the archive preserves a 2021 Project Serum-era release, a separately announced replacement in July 2022, and later operational guidance for the newer marketplace. Treating those records as one timeless interface would erase a material product transition.

As of 2026-07-20, official current-state material still presents the marketplace as an accessible Star Atlas product. That supports a qualified `LIVE` state for the 2022 replacement surface. It does not establish continuous uptime, market depth, trade outcomes, or the availability of every historically advertised asset.

## What the marketplace is

The marketplace connects Star Atlas accounts and assets to a trading interface. Official records associate it with ship and asset ownership, buy and sell orders, fees, and ATLAS-related economic mechanics. It is therefore both a consumer product and a user-facing surface over narrower on-chain systems.

Those layers must remain separate:

- the **marketplace interface** is the product a user visits;
- the **Galactic Marketplace program** is a documented on-chain program;
- **orders and transactions** are individual economic events;
- **fees and ATLAS locking** are policy or mechanism layers that may change independently;
- **liquidity, volume, and settlement quality** are outcomes requiring their own evidence.

A product page or support article can establish official instructions and positioning without independently proving those operational outcomes.

## Lifecycle chronology

| Date | Surface and evidence state | Archival finding |
|---|---|---|
| 2021-08-04 | 2021 marketplace `RELEASE_CLAIMED` | ATMTA published that the Solana-powered Galactic Marketplace had become fully operational. The record establishes an official release claim for the then-current Project Serum-era surface. [SRC-OFF-A465C97640C55838](../../archive/source-records/campaign-delta-official/SRC-OFF-A465C97640C55838.md) |
| 2022-07-22 | replacement marketplace `ANNOUNCED / RELEASE_CLAIMED` | ATMTA introduced “The New Galactic Marketplace.” The archive treats this as a replacement generation, not a routine update to an undifferentiated entity. [SRC-OFF-0C5AA46E01E189EC](../../archive/source-records/campaign-delta-official/SRC-OFF-0C5AA46E01E189EC.md) |
| 2025-12-03 to 2025-12-08 | operational guidance `DOCUMENTED` | Official support records described creating buy and sell orders and explained marketplace fees and ATLAS locking. These dated guides establish documented workflows in late 2025, not the first date those mechanics existed. [SRC-OFF-1EE2242A6F7844FF](../../archive/source-records/campaign-delta-official/SRC-OFF-1EE2242A6F7844FF.md) [SRC-OFF-B38AFD8A2122994F](../../archive/source-records/campaign-delta-official/SRC-OFF-B38AFD8A2122994F.md) |
| 2026-07-12 | current access path `OBSERVED` | The captured official homepage linked the Galactic Marketplace through `play.staratlas.com`. This establishes discoverability at the capture date, not historical uptime. [Official current-state snapshot](Official-Current-State-Snapshot-2026-07-12.md) |

## Two marketplace generations

The 2021 and 2022 marketplace records should not be collapsed. The repository currently models the 2021 surface as `SUPERSEDED` and the 2022 replacement as the canonical current marketplace entity. This distinction is supported by the explicit “new marketplace” framing, but the archive still lacks a complete contract-by-contract migration record.

The replacement relationship also does not justify rewriting older sources. Historical publications that described the 2021 interface retain their original terminology and context. Alias and succession mappings belong in the knowledge layer, while source text remains unchanged.

## Current state and evidence boundary

The strongest supported aggregate statement is:

> As of July 2026, ATMTA maintained an official access path and current product description for the post-2022 Galactic Marketplace.

The archive does **not** currently establish:

- uninterrupted availability since either release announcement;
- the exact deployment instant or migration transaction for the 2022 replacement;
- complete program upgrade and authority history;
- independent verification of published volume or economic counters;
- successful execution of every order;
- continuous support for every historical asset class; or
- the effect of every fee or locking-policy revision.

Marketplace mentions inside SAGE, Holosim, or other products do not prove that those environments use the same interface, contracts, liquidity, or settlement rules.

## Related systems

- [Star Atlas Product Registry](Product-Registry.md)
- [SAGE Product-Family History](SAGE.md)
- [Technology and Program Registry](../technology/Official-Technical-Surface-Inventory.md)
- [Governance and Economy Overview](../governance/Governance-and-Economy-Overview.md)
- [Product Timeline](../timeline/Product-Timeline.md)

## Known conflicts, gaps, and missing artifacts

The next high-value artifacts are dated screenshots or web captures for each major interface generation; program deployment and upgrade transactions; IDL and repository release history; fee-policy change records; incident and outage notices; and evidence tying named interfaces to specific program versions.

No conflict presently requires choosing between two incompatible release dates. The material uncertainty is narrower: official announcements support publisher-stated availability, while independent deployment and continuity evidence remains incomplete.

## Review status

`QUALIFIED`, last reviewed 2026-07-20. Identity, the 2021-to-2022 succession, late-2025 support documentation, and the July 2026 access path are well supported. Operational continuity and detailed technical lineage remain open research questions.
