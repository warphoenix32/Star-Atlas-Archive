---
title: "Ships, Assets, and Ownership"
seo_title: "Star Atlas Ships and Assets: Ownership, Markets, and Game Utility"
seo_description: "A source-qualified guide separating Star Atlas asset identity, token ownership, marketplace listing, base-ship data, and product-specific utility."
knowledge_status: QUALIFIED
as_of: 2026-07-23
confidence: MEDIUM
page_risk_score: 7
page_risk_class: R3
evidence_basis:
  - "knowledge/gameplay/Galactic-Marketplace.md"
  - "knowledge/gameplay/Ship-and-Manufacturer-Registry.md"
  - "knowledge/gameplay/SCORE-and-Faction-Fleet.md"
  - "knowledge/gameplay/SAGE.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-B2C1AA5D0C8E9D15.md"
known_limitations:
  - "The repository does not yet contain a complete mint, collection, owner, marketplace, rental, component, and product-utility ledger."
  - "Token possession does not independently establish beneficial ownership, identity, current accessibility, or use in every product."
research_gaps:
  - "Reconcile mints, collections, editions, metadata revisions, owners, listings, rentals, burns, migrations, components, and build-qualified utility."
review_after: 2026-10-23
---

# Ships, Assets, and Ownership

Star Atlas ships can be stories, designs, tokens, marketplace listings, base game templates, fleet entries, or individually configured vehicles. These forms are related, but one does not prove the others. A token can exist without current game utility; a ship can appear in a product without proving that every edition is accessible; a marketplace listing does not prove a completed sale; and a base stat sheet does not describe every component-modified instance.

## Asset issuance and identity

The 2021 Galactic Asset Offering formally introduced an early generation of Star Atlas NFTs. Official publications connected ships and other assets to scarcity, ownership, trading, and planned utility. The offering establishes an issuance program and public claims; each collection, mint, edition, and later migration still requires its own record. [SRC-OFF-B2C1AA5D0C8E9D15](../../archive/source-records/campaign-delta-official/SRC-OFF-B2C1AA5D0C8E9D15.md)

A robust asset identity should preserve:

- canonical product or collection name;
- mint or collection address;
- edition and supply;
- metadata URI and revision history;
- manufacturer and model when explicitly sourced;
- marketplace and observed URLs;
- lifecycle and product-utility evidence;
- aliases and legacy classifications.

## Ownership is a chain state, not a biography

An address holding a token is direct evidence of control at an observed slot. It does not automatically identify the person or organization behind the address. Community wallet attributions can be highly plausible while remaining unconfirmed by the attributed party. Custody, multisignature control, delegation, rentals, escrow, and marketplaces can further separate possession from beneficial ownership or active use.

Historical claims therefore require a timestamp or slot. "Owned" should mean observed or otherwise supported at a specific time, not permanent ownership.

## Marketplace listing and sale

The Galactic Marketplace provides a user-facing trading surface. A listing is an offer; an order is not necessarily filled; a displayed price is not a completed transaction; and an official asset announcement is not proof of settlement. The 2021 marketplace and its 2022 replacement also remain separate lifecycle entities. [Galactic Marketplace](../gameplay/Galactic-Marketplace.md)

## Utility changes by product

Ship utility developed in stages:

- SCORE/Faction Fleet allowed ships to be enlisted in an ATLAS-emissions loop.
- Escape Velocity used ships for active on-chain movement and resource discovery.
- SAGE Labs and Starbased used fleet characteristics in mining, movement, transport, crafting, and strategy systems.
- the Showroom provided visual, flight, racing, photography, marketplace, and combat-related experiences in named builds.
- Holosim uses its own simulation values.
- C4 PTR documents a separate testing state.

A ship's utility in one surface cannot be copied into another without build-specific evidence.

## Base templates and individual ships

The [Ship and Manufacturer Registry](../gameplay/Ship-and-Manufacturer-Registry.md) preserves 63 base templates intended for SAGE and C4. Those records explicitly exclude Holosim's value system and future component modifications. If components modify an individual ship, the resulting instance needs a separate versioned state rather than an overwrite of the base design.

## Current-state caution

Present ownership, listing, and accessibility are volatile. A complete current statement requires fresh evidence from the relevant chain accounts, marketplace, game client, and product configuration. Historical pages should preserve earlier states even when an asset is later migrated, delisted, rebased, rented, or given new utility.

## Review status

`QUALIFIED`. The conceptual distinctions and major utility transitions are well supported. A complete asset registry and transaction-level ownership history require additional chain, marketplace, metadata, and product-version datasets.
