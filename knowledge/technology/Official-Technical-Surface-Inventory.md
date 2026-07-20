---
title: "Technology and Program Registry"
seo_title: "Star Atlas Program IDs, APIs and Technology Registry"
seo_description: "A source-linked registry of Star Atlas Solana programs, game IDs, APIs, repositories, Unreal tools, developer infrastructure, and unresolved deployment evidence."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/source-records/campaign-delta-official/SRC-OFF-F217B64FD0342839.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-B3E826AFA52FB19B.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-3974380BE9CB23D7.md"
known_limitations:
  - "Documentation presence is not proof of deployment, uptime, adoption, or current upgrade authority."
  - "The repository does not preserve program-specific audit reports for the broad official audit claim."
research_gaps:
  - "Recover deployment and upgrade transactions, IDL versions, authorities, audit reports, remediation records, and release histories."
  - "Resolve Atlas Prime versus ATLAS Fee Payer naming and Holosim decoder versus mainnet-registry coverage."
review_after: 2027-01-17
---

# Technology and Program Registry

This registry separates on-chain programs, token mints, game IDs, APIs, frameworks, libraries, repositories, Unreal Engine tooling, and institutional support initiatives. Shared subject matter does not make these surfaces aliases, and documentation does not automatically establish deployment.

**Primary source:** https://build.staratlas.com/

**Evidence note:** The registry uses high-confidence first-party documentation for identifiers and official terminology. Deployment and operation remain separate questions.

## On-chain program and game-ID snapshot

The following addresses are transcribed from official Mainnet Program IDs documentation updated 2026-04-16. `DOCUMENTED_CURRENT` means the address appeared under the current-program heading on that date; it does not establish original deployment date, uninterrupted operation, immutable code, or current authority. [SRC-OFF-F217B64FD0342839](../../archive/source-records/campaign-delta-official/SRC-OFF-F217B64FD0342839.md)

| Surface | Type | Identifier | Documented state | Qualification |
|---|---|---|---|---|
| Crew | On-chain program | `CREWiq8qbxvo4SKkAFpVnc6t7CRQC4tAAscsNAENXgrJ` | `DOCUMENTED_CURRENT` | Deployment and upgrade history missing. |
| Galactic Marketplace | On-chain program | `traderDnaR5w6Tcoi3NFm53i48FTDNbGjBSZwWXDRrg` | `DOCUMENTED_CURRENT` | Current listing is not historical release proof. |
| SAGE | On-chain program | `SAGE2HAwep459SNq61LHvjxPk4pLPEJLoMETef7f7EE` | `DOCUMENTED_CURRENT` | Distinct from SAGE product-family aggregate. |
| Crafting | On-chain program | `CRAFT2RPXPJWCEix4WpJST3E7NLf79GTqZUL75wngXo5` | `DOCUMENTED_CURRENT` | Legacy address separately listed. |
| Cargo | On-chain program | `Cargo2VNTPPTi9c1vq1Jw5d3BWUNr18MjRtSupAghKEk` | `DOCUMENTED_CURRENT` | Legacy address separately listed. |
| Fleet Rentals | On-chain program | `SRSLY1fq9TJqCk1gNSE7VZL2bztvTn9wm4VR8u8jMKT` | `DOCUMENTED_CURRENT` | Product adoption and contract status unverified. |
| Player Profile | On-chain program | `pprofELXjL5Kck7Jn5hCpwAL82DpTkSYBENzahVtbc9` | `DOCUMENTED_CURRENT` | Profile Vault and Profile Faction remain separate. |
| Profile Vault | On-chain program | `pv1ttom8tbyh83C1AVh6QH2naGRdVQUVt3HY1Yst5sv` | `DOCUMENTED_CURRENT` | No authority record captured. |
| Profile Faction | On-chain program | `pFACSRuobDmvfMKq1bAzwj27t6d2GJhSCHb1VcfnRmq` | `DOCUMENTED_CURRENT` | No authority record captured. |
| Points | On-chain program | `Point2iBvz7j5TMVef8nEgpmz4pDr7tU7v3RjAfkQbM` | `DOCUMENTED_CURRENT` | Points Store is a separate program. |
| Points Store | On-chain program | `PsToRxhEPScGt1Bxpm7zNDRzaMk31t8Aox7fyewoVse` | `DOCUMENTED_CURRENT` | Availability by product unresolved. |
| Atlas Prime / ATLAS Fee Payer | On-chain program | `APR1MEny25pKupwn72oVqMH4qpDouArsX8zX4VwwfoXD` | `DOCUMENTED_CURRENT`; label conflict | Mainnet page says Atlas Prime; decoder README says ATLAS Fee Payer. Do not choose an alias without reconciliation. |
| Claim Stakes | On-chain program | `STAKEr4Bh8sbBMoAVmTDBRqouPzgdocVrvtjmhJhd65` | `DOCUMENTED_CURRENT` | User-facing utility chronology separate. |
| SCORE | On-chain program | `FLEET1qqzpexyaDpqb2DGsSzE2sDCizewCg9WjrA6DBW` | `DOCUMENTED_CURRENT` | Listing does not prove active Faction Fleet emissions. |
| Escape Velocity | On-chain test program | `TESTWCwvEv2idx6eZVQrFFdvEJqGHfVA1soApk2NFKQ` | `DOCUMENTED_CURRENT` | Historical test/supersession state remains product-specific. |
| DAO Proxy Rewarder | Governance program | `gateVwTnKyFrE8nxUUgfzoZTPKgJQZUbLsEidpG4Dp2` | `DOCUMENTED_CURRENT` | Also named in PIP-1. |
| ATLAS Locker | Locking program | `ATLocKpzDbTokxgvnLew3d7drZkEzLzDpzwgrgWKDbmc` | `DOCUMENTED_CURRENT` | Distinct from ATLAS token and DAO Treasury. |
| POLIS Locker | Governance/locking program | `Lock7kBijGCQLEFAmXcengzXKA88iDNQPriQ7TbgeyG` | `DOCUMENTED_CURRENT` | Distinct from POLIS token and PVP. |
| POLIS Locker Snapshots | Snapshot program | `snapNQkxsiqDWdbNfz8KVB7e3NPzLwtHHA6WV8kKgUc` | `DOCUMENTED_CURRENT` | Historical snapshots not yet preserved. |
| Faction Enlistment | On-chain program | `FACTNmq2FhA2QNTnGM2aWJH3i7zT3cND5CgvjYTjyVYe` | `DOCUMENTED_CURRENT` | Product lifecycle unresolved. |
| Legacy SAGE | Legacy on-chain program | `SAGEqqFewepDHH6hMDcmWy7yjHPpyKLDnRXKb3Ki8e6` | `DOCUMENTED_LEGACY` | “Legacy” does not supply deactivation date. |
| Legacy Cargo | Legacy on-chain program | `Cargo8a1e6NkGyrjy4BQEW4ASGKs9KSyDyUrXMfpJoiH` | `DOCUMENTED_LEGACY` | Migration evidence missing. |
| Legacy Crafting | Legacy on-chain program | `Craftf1EGzEoPFJ1rpaTSQG1F6hhRRBAf4gRo9hdSZjR` | `DOCUMENTED_LEGACY` | Migration evidence missing. |
| SAGE: Starbased | Game ID | `GAMEzqJehF8yAnKiTARUuhZMvLvkZVAsCVri5vSfemLr` | `DOCUMENTED_ACTIVE_GAME_ID` | Game ID is not the SAGE program or product family. |
| Legacy SAGE | Game ID | `GameYNgVLn9kd8BQcbHm8jNMqJHWhcZ1YTNy6Pn3FXo5` | `DOCUMENTED_LEGACY_GAME_ID` | Deactivation transaction/state missing. |

## Decoder and deployment distinction

The first-party decoder repository maps additional programs, including a `sage-holosim` decoder for `SAgEeT8u14TE69JXtanGSgNkEdoPUcLabeyZD2uw8x9`. That address is absent from the captured mainnet registry. Decoder support proves that official tooling can decode the identified account format; it does not prove production deployment or current mainnet status. [SRC-OFF-B3E826AFA52FB19B](../../archive/source-records/campaign-delta-official/SRC-OFF-B3E826AFA52FB19B.md)

## Frameworks, APIs, and tooling

| Surface | Type | Dated evidence | Boundary |
|---|---|---|---|
| Star Frame | Solana program framework/repository | Official repository record published 2024-01-23, updated 2026-06-15 | Active-development claim is first-party; adoption and release versions require repository review. |
| Star Atlas decoders | Rust libraries/repository | Published 2025-09-23, updated 2026-01-21 | Decoder presence is not program deployment. |
| APIs and Data / Galaxy API | Documentation/API family | Build documentation updated 2026-04-16 | Documentation presence is not uptime or backward-compatibility proof. |
| F-KIT | Unreal Engine integration tooling | Official announcement 2022-09-29; current docs snapshot 2026-04-16 | Release claim and current docs do not establish every intermediate version. |
| Star Atlas Cookbook | Examples/repository | Repository record published 2024-04-11, updated 2025-02-28 | Examples are not production guarantees. |
| Developer RPC Initiative | Institutional infrastructure program | Current description updated 2026-04-16 | Eligibility and benefit claims are documented; launch date, awards, cost, and outcomes unresolved. |

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

This is an attributed publisher claim about the security process. Individual audit firms, reports, scope, dates, findings, remediation, deployed program versions, and upgrade-authority status must be verified program by program before recording a specific contract as audited.

## Registry evidence rules

- `DOCUMENTED` is not `DEPLOYED`.
- `DEPLOYED` is not proof of user-facing release or present activity.
- A decoder or IDL is not proof the program is live.
- A repository update is not a product release.
- `LEGACY` is a documentation label, not a deactivation transaction.
- One address with two official labels remains a conflict until reconciled.
- A generic audit statement cannot be attached to a specific deployed binary without report, scope, version, and remediation evidence.

## Known conflicts and missing artifacts

The Atlas Prime/ATLAS Fee Payer label conflict, Holosim decoder/mainnet-registry mismatch, and continued SCORE listing after announced emissions deprecation require review. Missing artifacts include program deployment and upgrade transactions, upgrade authorities, versioned IDLs, program-specific audits, remediation records, API schemas and deprecation history, GitHub tags/releases, Atlasnet architecture, and RPC Initiative award history.

## Review status

`QUALIFIED`. Address transcription and documentation state are high confidence as of their source updates; deployment, security, and lifecycle interpretation remain incomplete.

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
