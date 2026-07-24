---
title: "Star Atlas Technology and Program Registry"
seo_title: "Star Atlas Technology: Solana Programs, Unreal Engine, APIs, and Tools"
seo_description: "A reader-level map of the Star Atlas technology stack, separating products, Solana programs, game IDs, APIs, repositories, Unreal tools, and test environments."
knowledge_status: QUALIFIED
as_of: 2026-07-23
confidence: HIGH
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "knowledge/technology/Technical-Platform.md"
  - "knowledge/technology/Official-Technical-Surface-Inventory.md"
  - "knowledge/gameplay/UE5-Showroom.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-F217B64FD0342839.md"
known_limitations:
  - "Documentation, source code, decoder support, and a listed address do not independently prove deployment, uptime, audit status, or product integration."
  - "Program version, upgrade authority, executable hash, and consuming build are incomplete for many surfaces."
research_gaps:
  - "Map every program and game ID to deployments, upgrades, IDLs, audits, product builds, API versions, incidents, and deprecations."
review_after: 2027-01-23
---

# Star Atlas Technology and Program Registry

Star Atlas is built from several technical layers rather than one monolithic game server. The public platform includes Solana programs and accounts, product-specific game IDs, browser applications, an Unreal Engine client, APIs, indexed data services, open-source libraries, developer tooling, and test environments.

The central rule is simple: documentation is evidence that a surface was described; it is not automatically proof that the surface was deployed, integrated, continuously available, or secure.

## Product surfaces

Players encounter technology through products: the Galactic Marketplace, SCORE/Faction Fleet, Escape Velocity, SAGE Labs, Starbased, the UE5 Showroom, Holosim, and C4 PTR. Each product has its own lifecycle and can use a different combination of programs, game IDs, APIs, and client code.

## Solana programs

The official Mainnet Program IDs documentation lists programs for SAGE, Cargo, Crafting, Crew, Galactic Marketplace, Fleet Rentals, Player Profile, faction and profile-vault functions, points, SCORE, Claim Stakes, DAO rewards, and locking. [SRC-OFF-F217B64FD0342839](../../archive/source-records/campaign-delta-official/SRC-OFF-F217B64FD0342839.md)

A listed address supports `DOCUMENTED_CURRENT` at the capture date. Stronger statements need:

- deployment transaction and slot;
- executable hash and version;
- current upgrade authority;
- IDL or interface version;
- audit scope and remediation;
- consuming product and build;
- observed operation.

## Game IDs and configuration

A game ID identifies a particular configured game state and is not an alias for its underlying program. Starbased and legacy SAGE IDs can coexist in documentation while having different lifecycle states. A parameter change at one game ID should not be generalized to the whole SAGE family.

## APIs and indexed data

Official Build documentation describes Galaxy APIs and other integration surfaces. API documentation establishes an intended interface. It does not prove endpoint uptime, historical availability, complete retention, freshness, pagination behavior, or compatibility across versions.

## Open-source repositories and tools

The verified `staratlasmeta` organization exposed dozens of public repositories during the 2026 sweep, including decoders, Star Frame, Cookbook material, F-KIT resources, Atlasnet tools, documentation, profile-key management, and governance-related work.

Repositories provide strong provenance for published source code. They still require careful interpretation:

- a commit is not a deployed release;
- a decoder can support an address not present in another official registry;
- a package release does not prove every consumer upgraded;
- public code may represent only part of production.

## Unreal Engine and F-KIT

The [UE5 Showroom](../gameplay/UE5-Showroom.md) is a consumer-facing client history. F-KIT and blueprint documentation are developer-facing tools. They can change independently. A Showroom feature is not proof that F-KIT exposes the same feature, and an SDK release is not proof that a named game build shipped.

## Test and simulation environments

Holosim is a browser simulation with its own balances and feature chronology. C4 PTR is a public test environment. A feature can be live inside Holosim or testable in PTR without being generally released on mainnet.

## Evidence ladder

Technical claims advance through narrower stages:

1. `DOCUMENTED`
2. `SOURCE_RELEASED`
3. `DEPLOYED`
4. `PRODUCT_INTEGRATED`
5. `OPERATIONALLY_OBSERVED`
6. `INDEPENDENTLY_VERIFIED`

No stage is inferred solely from the density of documentation.

## Review status

`QUALIFIED`. The platform layers and documented official surfaces are well supported. Deployment history, authorities, version mapping, audits, service operation, and adoption require deeper technical evidence.
