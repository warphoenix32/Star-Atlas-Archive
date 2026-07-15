---
title: Star Atlas Technical Platform
entry_type: technical-overview
status: active
updated: 2026-07-14
publication_status: public
---

# Star Atlas Technical Platform

## Platform summary

Official builder documentation describes Star Atlas as a Solana-powered, multi-product game ecosystem and permissionless builder platform. Its architecture combines consumer applications, on-chain programs, APIs, open-source libraries and Unreal Engine tooling.

## Documented technical surfaces

### On-chain systems

The current builder index includes documentation for:

- SAGE
- Cargo
- Crafting
- Player Profile
- Profile Faction
- Claim Stakes
- Galactic Marketplace
- Faction Fleet
- Fleet Rentals
- Fees
- Atlas Prime
- Factory
- Crew
- Tokens and items

The presence of documentation establishes an official integration surface; it does not by itself prove feature completeness, usage levels or current security status.

### APIs and data

Star Atlas Build identifies APIs and data resources, including the Galaxy API, as supported builder surfaces. Specific endpoints, authentication requirements, data freshness and deprecation policy require separate records.

### Unreal Engine tooling

The builder hub references F-Kit, blueprint support and Unreal Engine production workflows. These tools should be indexed separately from the consumer UE5 client.

### C4 public test surface

Atlas Brew preserved a C4 deep-dive and question-and-answer discussion about intended systems, including asteroid mining. Because that material describes design intent and carries no normalized speaker labels, it is roadmap evidence rather than proof of a deployed system. [SRC-ATLAS-BREW-0101, 00:02:35–00:06:35; SEG-ATLAS-BREW-0101-0002](../../archive/semantic/atlas-brew/segment-index.json) [SRC-ATLAS-BREW-0101, 00:38:07–00:39:04; SEG-ATLAS-BREW-0101-0024](../../archive/semantic/atlas-brew/segment-index.json)

Official support records dated June 2026 document a C4 Public Test Realm and mining implemented in that test environment, with explicit warnings that requirements could change during development. The supported lifecycle state is therefore **testing**; the records do not prove a general release or production-network execution. [SRC-OFF-E061D3A6454697AB](../../archive/source-records/campaign-delta-official/SRC-OFF-E061D3A6454697AB.md) [SRC-OFF-952AB5D6D09DD6BF](../../archive/source-records/campaign-delta-official/SRC-OFF-952AB5D6D09DD6BF.md)

### Developer infrastructure

The builder hub describes a Developer RPC Initiative intended to support teams building products around the ecosystem. Terms, eligibility and historical availability remain to be documented.

## Official open-source organization

The verified `staratlasmeta` GitHub organization controls the `staratlas.com` domain and displayed 43 public repositories during the July 2026 sweep.

Notable repositories visible in the official organization include:

| Repository | Documented purpose |
|---|---|
| `star_frame` | High-performance modular Solana program framework |
| `star-atlas-cookbook` | Examples using Star Atlas open-source tooling |
| `FoundationKit` | Foundation-level development kit; specific scope requires repository review |
| `factory` | Transaction construction targeting Star Atlas Solana programs |
| `star-atlas-decoders` | Rust decoders for Star Atlas Solana programs |
| `atlasnet-explorer` | Explorer for Atlasnet clusters |
| `build-staratlas` | Source associated with the builder documentation hub |
| `profile-key-management` | Authorized-key management for player profiles |
| `stv` | Governance vote-verification tooling; exact scope requires code review |

Repository descriptions and update dates are useful discovery evidence, but code history, releases and deployed addresses must be checked before drawing implementation conclusions.

## Technical evidence priorities

- Mainnet program IDs and upgrade authorities.
- Security audits and disclosures.
- Program deployment and migration history.
- Atlasnet purpose, architecture and relationship to Solana mainnet.
- API schemas, uptime and deprecations.
- Open-source license inventory.
- Active versus archived repositories.
- Third-party integrations and builder dependencies.
- Differences between documented systems and live production behavior.

## Sources

- https://build.staratlas.com/
- https://build.staratlas.com/dev-resources/on-chain-game-systems
- https://github.com/staratlasmeta
