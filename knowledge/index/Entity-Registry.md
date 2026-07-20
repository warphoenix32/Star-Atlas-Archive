---
title: "Star Atlas Entity Registry"
seo_title: "Star Atlas Canonical Entity Registry"
seo_description: "A stable identity registry for Star Atlas institutions, products, tokens, assets, lore concepts, guilds, media, and people without collapsing lifecycle states."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 5
page_risk_class: R2
evidence_basis:
  - "knowledge/gameplay/Product-Registry.md"
  - "archive/normalized/lore/taxonomy.json"
  - "knowledge/organizations/Organization-and-Role-Registry.md"
known_limitations:
  - "The registry is not yet an exhaustive enumeration of every canonical entity or historical alias."
  - "Identity registration does not establish current lifecycle, ownership, authority, or activity."
research_gaps:
  - "Reconcile remaining aliases, entity splits, historical names, and community identities against evidence packets."
review_after: 2027-01-20
---

# Star Atlas Entity Registry

The Entity Registry gives major Star Atlas subjects stable identifiers so evidence from different periods can point to the same thing—or remain separate when the record shows they are different. Registration answers **what entity is this?** It does not answer whether a product is live, an organization is active, a person still holds a role, or a historical description remains current.

## Institutions

| ID | Preferred entity | Type | Identity note |
|---|---|---|---|
| `ORG-ATMTA` | ATMTA, Inc. | Operating company | Separate from the DAO, Foundation, and Council |
| `ORG-SA-DAO` | Star Atlas DAO | Governance system/electorate | POLIS-locking and PVP-weighted governance identity |
| `ORG-SA-FOUNDATION` | Star Atlas Foundation | Legal and administrative body | Separate institutional and role chronology |
| `ORG-SA-COUNCIL` | Star Atlas Council | Elected governance-process steward | Not the lore Council of Peace or a guild council |
| `ORG-SA-GITHUB` | `staratlasmeta` GitHub organization | Technical publisher | Repository identity does not prove deployment |

See the [Institutional Overview](../organizations/Institutional-Overview.md) and [Organization and Role Registry](../organizations/Organization-and-Role-Registry.md) for authority and role boundaries.

## Product and system identities

| ID | Preferred entity | Type | Lifecycle handling |
|---|---|---|---|
| `PRODUCT-PLAY` | PLAY | Account and asset hub | Current state belongs in the Product Registry |
| `PRODUCT-SCORE` | SCORE / Faction Fleet | Historical emissions program and associated surface | Emissions deprecation must not define unresolved residual functionality |
| `PRODUCT-SAGE` | SAGE product family | Product family | SAGE Labs, Starbased, SAGE 3D, C4, and other named stages retain narrower states |
| `PRODUCT-UE5` | Star Atlas Unreal Engine client family | High-fidelity client family | Showroom builds and later releases retain build-specific states |
| `PRODUCT-HOLOSIM` | Holosim | Browser fleet simulation | Feature and release history remains date-bound |
| `PRODUCT-MARKETPLACE-LEGACY` | Original Galactic Marketplace | Historical marketplace surface | Separate from the replacement surface introduced in 2022 |
| `PRODUCT-MARKETPLACE` | Galactic Marketplace replacement surface | Marketplace | Does not inherit every state of the 2021 surface |
| `PRODUCT-DAO-PORTAL` | Star Atlas DAO portal | Governance application | Interface state does not establish proposal execution |
| `PRODUCT-BUILD` | Star Atlas Build | Builder documentation hub | Current documentation is not proof of historical availability |

The [Product Registry](../gameplay/Product-Registry.md) is authoritative for lifecycle wording. Lifecycle attaches to the narrowest named build, feature, program, or surface—not automatically to the family listed here.

## Tokens and asset classes

| ID | Preferred entity | Type | Boundary |
|---|---|---|---|
| `TOKEN-ATLAS` | ATLAS | Utility/economic token | Token identity is separate from emissions programs and account balances |
| `TOKEN-POLIS` | POLIS | Governance token | Token identity is separate from locked POLIS and derived PVP |
| `ASSET-SHIPS` | Star Atlas ships | Asset class | Base templates are separate from individually modified ships |
| `ASSET-CREW` | Crew | Asset class | Product-specific availability remains lifecycle evidence |
| `ASSET-CLAIM-STAKES` | Claim Stakes | Asset/system class | Do not collapse asset identity with every associated mechanic |

## Lore taxonomy

The ingested Star Atlas Lore repository controls preferred in-universe taxonomy and nomenclature within its historical canonical-source snapshot. Official later lore can add newer concepts. Historical sources retain their original terms as aliases rather than being rewritten.

| ID | Preferred entity | Type |
|---|---|---|
| `LORE-GALIA` | Galia Expanse | Region |
| `LORE-FACTION-MUD` | MUD / Manus Ultima Divina | Major faction |
| `LORE-FACTION-ONI` | ONI Consortium | Major faction |
| `LORE-FACTION-USTUR` | Ustur | Major faction/species context requiring subtype care |
| `LORE-COUNCIL-PEACE` | Council of Peace | In-universe political institution |
| `LORE-CONVERGENCE-WAR` | Convergence War | Lore event |
| `LORE-CATACLYSM` | The Cataclysm | Lore/astronomical event |
| `LORE-IRIS` | Iris | Rogue planet |
| `LORE-TUFA` | Tufa | Species/beings |
| `LORE-CHARON-GOTTI-JR` | Charon Gotti Jr. | Character |

See the [Lore Canon Registry](../lore/Canon-Registry.md) for adopted classes, aliases, and unresolved hierarchy questions.

## Community identities

Guilds, publications, creators, and people use dedicated registries because affiliation, ownership, role, and active period require their own evidence:

- [Guild and DAC Master Index](../guilds/Guild-Master-Index.md)
- [Media and Creator Index](../media/Media-and-Creator-Index.md)
- [Major Actor Index](../people/Actor-Master-Index.md)
- [Community Publication Relationship Index](../media/Community-Publication-Relationship-Index.md)

## Identity rules

- An alias is an alternate name for the same object, not a lifecycle stage or successor product.
- A historical role is not a current role.
- A shared brand does not merge legal or governance institutions.
- A mirror or replay does not become the original publisher.
- Similar names do not merge lore, guild, and governance councils.
- Unknown identity stays unresolved until documentary or operator-approved evidence supports a merge.

## Review status

`QUALIFIED`. The major entity boundaries are stable enough for cross-linking. Exhaustive coverage and several alias/hierarchy migrations remain incomplete.
