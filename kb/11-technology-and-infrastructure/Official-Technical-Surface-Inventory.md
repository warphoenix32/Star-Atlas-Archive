---
title: Official Star Atlas Technical Surface Inventory
entry_type: technical-index
status: active
updated: 2026-07-12
publication_status: public
---

# Official Star Atlas Technical Surface Inventory

This inventory records technical systems and builder surfaces explicitly listed in current official Star Atlas Build documentation.

**Primary source:** https://build.staratlas.com/
**Source class:** [SRC-OFFICIAL] [EV-DOCUMENTED] [CONF-HIGH]

## Documented development surfaces

### Core framework and access

- Star Frame — described by the official GitHub organization as a high-performance modular Solana program framework.
- Mainnet Program IDs — production address lookup for supported programs.
- APIs and Data — data endpoints, Galaxy API references, and integration surfaces.
- Developer RPC Initiative — infrastructure program covering production-grade Solana RPC costs for qualifying community projects.
- Star Atlas Cookbook — open-source examples for Star Atlas tooling.

### Indexed protocol and data documentation

The Build navigation currently exposes documentation for:

- Crew
- Data Source
- SAGE
- Cargo
- Crafting
- Profile Faction
- Player Profile
- Atlas Prime
- Claim Stakes
- Factory
- Galaxy API
- Items
- Tokens
- Showroom
- Galactic Marketplace
- Fleet Rentals
- Faction Fleet
- Marketplace fees

Documentation presence establishes an official integration surface, not necessarily feature completeness, decentralization, or production adoption.

### Unreal Engine tooling

- F-Kit setup documentation
- F-Kit Blueprint usage
- F-Kit reference documentation

### Creative and legal layer

The builder hub includes official IP guidance, creative assets, creator requirements, monetization rules, royalties, and the Powered by the People program.

## Developer RPC Initiative

The initiative states that Star Atlas covers Solana RPC infrastructure costs for qualifying projects. Listed benefits include production-grade endpoints, access guidance, tutorials, and cookbook examples. Eligibility requires a project to be open source or publicly accessible. This is an official builder-support program and should be tracked separately from grants or DAO funding.

## Program-security claim

Current official documentation states that, before release, all Star Atlas programs are internally reviewed by ATMTA and fully audited by third parties.

**Evidence treatment:** [EV-ATTRIBUTED] [PUB-ATTRIBUTE]

The statement is an official security-process claim. Individual audit firms, reports, scope, dates, findings, remediation, deployed program versions, and upgrade-authority status must be verified program by program before recording a specific contract as audited.

## Official GitHub organization snapshot

The `staratlasmeta` organization is verified by GitHub as controlling `staratlas.com`. During the 2026-07-12 sweep, GitHub displayed 43 public repositories. Visible repositories included:

- `star_frame`
- `configs`
- `star-atlas-cookbook`
- `FoundationKit`
- `factory`
- `sa-landing-page`
- `star-atlas-decoders`
- `atlasnet-explorer`
- `build-staratlas`
- `profile-key-management`
- `stv`

Observed repository descriptions identify:

- `factory` as tooling for constructing transactions targeting Star Atlas Solana programs;
- `star-atlas-decoders` as Rust decoders for Star Atlas Solana programs;
- `atlasnet-explorer` as an explorer for Atlasnet clusters;
- `profile-key-management` as a tool allowing connected wallets to manage authorized profile keys;
- `stv` as governance-related tooling requiring further repository-level review.

## Research queue

- Export metadata for all public repositories, including creation date, last update, license, archived status, releases, and default branch.
- Distinguish ATMTA-authored code from forks and configuration repositories.
- Map program IDs to source repositories, deployed versions, authorities, audits, and live products.
- Recover and index third-party audit reports.
- Establish the history and present purpose of Atlasnet.
- Determine whether `stv` is the vote-verification tool previously identified and document its exact function.
- Track which repositories are active, dormant, deprecated, experimental, or infrastructure-only.
