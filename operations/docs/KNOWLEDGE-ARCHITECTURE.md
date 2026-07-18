# Knowledge Architecture

## Purpose

This repository is a living research system rather than a static encyclopedia. It supports historical reconstruction, current reporting, governance analysis, community intelligence, and official lore research.

## Archival depth standard

Knowledge pages are durable research records, not short summaries. Each page should preserve enough context that a future reader can understand the subject, its chronology, its institutional or product role, the evidence behind material conclusions, and the limits of the surviving record without first reconstructing the entire source corpus.

Thoroughness is substantive rather than length-based. A complete page should address every applicable dimension of its subject:

- identity, aliases, scope, and terminology;
- historical origin and chronological development;
- institutional, economic, technical, social, or product function;
- dated lifecycle states and present status;
- relationships to other entities, systems, proposals, and publications;
- contemporary understanding and later interpretation where they differ;
- disputes, contradictions, corrections, supersessions, and abandoned plans;
- claim-level provenance and source-authority boundaries;
- known limitations, missing evidence, and a concrete research queue;
- revision context when a later source changes an earlier conclusion.

Concise prose is welcome, but brevity must never remove material context or conceal uncertainty. Semantic records may accelerate discovery; they do not substitute for source review or human synthesis. A page may remain incomplete only when its missing evidence and consequences are stated plainly.

The architecture has three layers:

1. **Source layer** — what was said or recorded, where, when, and by whom.
2. **Knowledge layer** — the best current synthesis of the available evidence.
3. **Publication layer** — material that is sufficiently verified, contextualized, and safe to publish.

## Top-level structure

| Path | Purpose |
|---|---|
| `operations/docs/` | Research rules, attribution, evidence, and editorial preferences |
| `knowledge/index/` | Entity, alias, topic, source, and relationship registries |
| `knowledge/timeline/` | Master timeline and annual histories |
| `knowledge/organizations/` | ATMTA, Star Atlas Foundation, DAO, councils, and related institutions |
| `knowledge/gameplay/` | Showroom, SAGE lineage, C4, Holosim, and other products |
| `knowledge/economy/` | ATLAS, POLIS, ships, land, resources, markets, emissions, and sinks |
| `knowledge/governance/` | Proposals, votes, treasury, governance systems, and precedents |
| `knowledge/research/` | Community-history gaps, disputed timelines, and research queues |
| `knowledge/guilds/` | Guild profiles, alliances, rivalries, and organizational history |
| `knowledge/people/` | Executives, developers, guild leaders, creators, analysts, and builders |
| `knowledge/lore/` | Official canon, chronology, factions, species, locations, and continuity |
| `knowledge/technology/` | Solana programs, APIs, repositories, Unreal tooling, and Atlasnet |
| `knowledge/media/` | HNN and other publications, creators, podcasts, and broadcasts |
| `knowledge/controversies/` | Major disputes, conflicting accounts, and trust events |
| `knowledge/events/` | Town halls, competitions, ceremonies, memes, and cultural milestones |
| `knowledge/index/source-registry/` | Source registries and provenance assessments |
| `publication/` | Article, briefing, report, and dataset workspaces |

## Persistent entity IDs

Important entities should receive stable IDs that do not change when names, roles, or affiliations change.

Examples:

```text
ORG-ATMTA
ORG-SA-FOUNDATION
ORG-SA-DAO
GUILD-AEPHIA
GUILD-ROME
ACTOR-MICHAEL-WAGNER
ACTOR-KRIGS
PRODUCT-SAGE-LABS
PRODUCT-C4
TOKEN-ATLAS
TOKEN-POLIS
LORE-FACTION-MUD
LORE-FACTION-ONI
LORE-FACTION-USTUR
```

Aliases remain permanently searchable in an alias registry.

## Internal marker labels

### Source class

```text
[SRC-OFFICIAL]   ATMTA, Star Atlas, Foundation, or official project publication
[SRC-EXEC]       Executive or senior institutional statement
[SRC-DEV]        Developer, employee, or contractor statement
[SRC-DAO]        Governance proposal, vote, or DAO document
[SRC-CHAIN]      On-chain evidence
[SRC-LEGAL]      Legal filing, registration, or opinion
[SRC-FIN]        Financial report or transaction evidence
[SRC-COMMUNITY]  General community source
[SRC-GUILD]      Guild or DAC source
[SRC-MEDIA]      Independent media or creator source
[SRC-KRIGS]      Firsthand context supplied by Krigs
[SRC-ARCHIVE]    Recovered historical material
[SRC-SECONDARY]  External reporting or third-party summary
```

### Evidence status

```text
[EV-VERIFIED]
[EV-DOCUMENTED]
[EV-ATTRIBUTED]
[EV-CORROBORATED]
[EV-INFERRED]
[EV-DISPUTED]
[EV-UNVERIFIED]
[EV-INCOMPLETE]
[EV-CONTRADICTED]
```

### Confidence

```text
[CONF-HIGH]
[CONF-MEDIUM]
[CONF-LOW]
[CONF-UNKNOWN]
```

### Publication status

```text
[PUB-SAFE]
[PUB-ATTRIBUTE]
[PUB-CONTEXT-ONLY]
[PUB-NEEDS-VERIFY]
[PUB-NOT-FOR-PUBLICATION]
```

### Lifecycle status

```text
[STATUS-ACTIVE]
[STATUS-DORMANT]
[STATUS-DEPRECATED]
[STATUS-CANCELLED]
[STATUS-COMPLETE]
[STATUS-ONGOING]
[STATUS-UNKNOWN]
```

## Guild and DAC records

Each guild should have a separate profile covering:

- founding date and founders;
- aliases and tags;
- faction alignment;
- leadership history;
- membership and structure;
- economic or gameplay specialization;
- tools, media, games, and other contributions;
- governance participation;
- alliances, mergers, splinters, and rivalries;
- attributable controversies;
- present status and open questions.

Relationship markers may include:

```text
[GREL-ALLY]
[GREL-COALITION]
[GREL-PARTNER]
[GREL-RIVAL]
[GREL-SPLINTER]
[GREL-MERGER]
[GREL-SHARED-LEADERSHIP]
[GREL-DISPUTED]
```

## Major actor records

Actor profiles may include executives, developers, Foundation or council members, guild leaders, creators, journalists, analysts, builders, moderators, and event organizers.

Each record should explain why the actor matters, their role history, major contributions, public positions, affiliations, reliability boundaries, disputes, and source record.

## Lore and canon

Lore must remain separate from project and community history.

Canon markers:

```text
[CANON-PRIMARY]
[CANON-OFFICIAL]
[CANON-SUPPLEMENTAL]
[CANON-PROMOTIONAL]
[CANON-AMBIGUOUS]
[CANON-RETCONNED]
[CANON-CONTRADICTED]
[CANON-NONCANON]
[CANON-COMMUNITY]
```

Every lore entry should preserve both:

- the in-universe chronology;
- the real-world publication chronology.

Officially licensed community work should not automatically be treated as primary canon.

## Raw-source ingestion workflow

```text
Raw source
→ source registration
→ cleaning and deduplication
→ entity and event extraction
→ claim and evidence classification
→ synthesis into readable knowledge
→ contradiction and gap review
→ Markdown update
→ publication-ready summary when requested
```

Raw exports are retained for verification but should not become the user-facing knowledge base. Duplicate quotations, bot traffic, irrelevant chatter, and formatting noise should be removed while preserving meaningful context, dissent, chronology, and provenance.

## Adaptability rules

- Create new categories when repeated material no longer fits existing retrieval patterns.
- Preserve old interpretations when evidence changes; add revision context instead of silently overwriting history.
- Record structural changes in a future architecture changelog.
- Keep the default branch limited to the current accepted knowledge state.
- Use issues or research branches for unresolved investigations.
