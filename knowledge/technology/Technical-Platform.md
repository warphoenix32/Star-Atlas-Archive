---
title: Star Atlas Technical Platform
entry_type: technical-overview
status: active
updated: 2026-07-12
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
