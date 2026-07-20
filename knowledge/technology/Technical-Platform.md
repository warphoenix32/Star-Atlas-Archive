---
title: "Star Atlas Technical Platform"
seo_title: "Star Atlas Technical Platform: Solana, APIs and Unreal Tools"
seo_description: "A research-oriented guide to the Star Atlas technical platform, separating Solana programs, game IDs, APIs, repositories, Unreal tooling, testing, and verified deployment evidence."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 5
page_risk_class: R2
evidence_basis:
  - "archive/source-records/campaign-delta-official/SRC-OFF-F217B64FD0342839.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-B3E826AFA52FB19B.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-3974380BE9CB23D7.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-E061D3A6454697AB.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-952AB5D6D09DD6BF.md"
known_limitations:
  - "Documentation and source-code presence do not independently establish deployment, uptime, security, adoption, or historical availability."
  - "Program-specific deployment, upgrade-authority, audit, and remediation evidence remains incomplete."
research_gaps:
  - "Map every documented program and game ID to deployments, authorities, source releases, IDLs, audits, migrations, and consuming products."
  - "Recover versioned API schemas, service-level history, deprecations, and Atlasnet architecture."
review_after: 2027-01-20
---

# Star Atlas Technical Platform

Star Atlas is not one technical object. Its documented platform spans Solana programs, product-specific game IDs, tokens and accounts, APIs, open-source libraries, Unreal Engine tooling, browser applications, test environments, and institutional developer support. The most important archival rule is to keep those surfaces distinct.

Official documentation establishes what ATMTA exposed or described at a particular date. It does not, by itself, prove that a program was deployed when first discussed, that an API remained continuously available, that a repository version matches a deployed binary, or that a generic security claim applies to every historical release.

## Platform layers

### Solana programs and accounts

The official Mainnet Program IDs record lists programs for SAGE, Cargo, Crafting, Crew, Galactic Marketplace, Fleet Rentals, Player Profile, profile vault and faction functions, points, SCORE, claim stakes, DAO reward and locking functions, and other systems. It also lists legacy programs and active or legacy game IDs. [SRC-OFF-F217B64FD0342839](../../archive/source-records/campaign-delta-official/SRC-OFF-F217B64FD0342839.md)

An address listed in that document is **documented first-party configuration evidence**. It is not automatically:

- the first deployment date;
- proof of continuous operation;
- proof that its upgrade authority is unchanged;
- evidence that a consumer interface is currently accessible;
- a guarantee that all source code is public; or
- proof that every transaction succeeded.

The [Technology and Program Registry](Official-Technical-Surface-Inventory.md) preserves the identifiers and their narrower qualifications.

### Game IDs and product configuration

Game IDs are not aliases for programs or product families. The official registry distinguishes, for example, a SAGE program from Starbased and legacy SAGE game IDs. A game ID can carry product-specific state while the underlying program remains documented. This is why an economic parameter change, product launch, and program migration must be recorded as separate events.

### APIs and indexed data

Star Atlas Build exposes APIs and data documentation, including Galaxy API material. Documentation supports the existence of an official integration surface at the evidence date. Endpoint availability, authentication, freshness, retention, pagination, schema compatibility, and deprecation require versioned operational evidence.

### Open-source libraries and repositories

The verified `staratlasmeta` organization displayed 43 public repositories during the July 2026 sweep. Visible projects included Star Frame, Star Atlas decoders, the Star Atlas Cookbook, Factory, F-KIT-related resources, Atlasnet Explorer, Build documentation, profile-key management, and governance-related tooling.

Repository metadata is valuable provenance, but repository activity must be interpreted carefully:

- a commit is not a deployed release;
- a decoder is not proof that the decoded program is live;
- a tagged package is not proof that every consumer upgraded;
- a public source repository may cover only part of a production system; and
- “active” development language is a first-party status claim until corroborated by release and deployment evidence.

The official decoder record maps a `sage-holosim` address not present in the captured Mainnet Program IDs page. The repository retains that difference as an unresolved deployment or documentation question rather than selecting one source as proof of live mainnet status. [SRC-OFF-B3E826AFA52FB19B](../../archive/source-records/campaign-delta-official/SRC-OFF-B3E826AFA52FB19B.md)

### Unreal Engine tooling and client builds

The technical platform includes developer-facing Unreal tooling such as F-KIT and blueprint documentation, while the [UE5 Showroom](../gameplay/UE5-Showroom.md) is a consumer-facing client history. These should not be merged. A developer SDK can be released or updated independently of a particular game build, and a client feature does not prove that a public SDK exposes the same system.

### Test environments

Official support records document a C4 Public Test Realm and mining systems in that test environment in June 2026. Those records support `TESTING` for the named PTR surface. They do not prove general release, production-network execution, or completion of the broader C4 roadmap. [SRC-OFF-E061D3A6454697AB](../../archive/source-records/campaign-delta-official/SRC-OFF-E061D3A6454697AB.md) [SRC-OFF-952AB5D6D09DD6BF](../../archive/source-records/campaign-delta-official/SRC-OFF-952AB5D6D09DD6BF.md)

Holosim likewise has a documented browser simulation and pre-mainnet testing role. A Holosim feature may be live inside Holosim while still absent from mainnet or another product.

## Developer-support infrastructure

The Developer RPC Initiative is an institutional support program described by Star Atlas Build. It offers qualifying open-source or publicly accessible projects access to production-grade Solana RPC infrastructure and related guidance. The archive treats it separately from DAO grants, commercial partnerships, and product releases. Eligibility language and offered support are documented; launch history, recipients, costs, uptime, and outcomes remain research gaps.

## Security and audit evidence

Official documentation states that Star Atlas programs receive internal review and third-party audits before release. This is a publisher-attributed process claim. It cannot be converted into a program-specific assurance without the audit firm, report, scope, deployed version or commit, findings, remediation record, and relevant authority state.

Likewise, open-source availability does not prove deployed-byte equivalence. Future chain evidence should link program addresses to executable-data hashes, deployment slots, upgrade transactions, and authorities before the repository records stronger implementation conclusions.

## How technical evidence is promoted

The Archive uses a staged ladder:

1. **Documented** — an official page, repository, or support article names the surface.
2. **Source released** — code or a package is available with a version or commit.
3. **Deployed** — chain or infrastructure evidence identifies a deployment.
4. **Product integrated** — a dated product record connects a deployed surface to a user-facing build.
5. **Operationally observed** — reproducible evidence confirms behavior at a stated time.
6. **Independently verified** — an external audit, test, or reconciled dataset supports the specific claim.

These stages are cumulative only when evidence explicitly connects them. They are not inferred from documentation density.

## Current state

As of 2026-07-20, the repository supports a broad, actively documented first-party developer platform spanning Solana and Unreal-related surfaces. Confidence is high in the existence and wording of captured official documentation, and lower for unresolved deployment history, current authorities, service operation, adoption, and binary-level security.

## Related knowledge

- [Technology and Program Registry](Official-Technical-Surface-Inventory.md)
- [Star Atlas Product Registry](../gameplay/Product-Registry.md)
- [UE5 Showroom History](../gameplay/UE5-Showroom.md)
- [SAGE Product-Family History](../gameplay/SAGE.md)
- [Holosim Release and Feature History](../gameplay/Holosim.md)
- [Governance Implementation and Evidence States](../governance/Governance-Implementation-and-Evidence-States.md)

## Missing artifacts and research priorities

The highest-value missing artifacts are deployment and upgrade transactions; current authorities; executable hashes; versioned IDLs; program-specific audit and remediation reports; API schemas and deprecation notices; package and repository release histories; incident reports; Atlasnet design documentation; RPC Initiative recipient records; and mappings from product builds to program and API versions.

## Review status

`QUALIFIED`, last reviewed 2026-07-20. The platform map and first-party documentation state are well supported. Deployment, operation, security, and adoption remain narrower claims requiring additional evidence.
