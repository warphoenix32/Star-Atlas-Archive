# Star Atlas Historical Archive

This repository preserves the public historical record of Star Atlas and organizes it into a human-readable, evidence-grounded knowledge system. It retains original source context, attribution, uncertainty, and chronology while keeping archival evidence separate from reviewed knowledge.

## Start here

Researchers should begin with the [Knowledge overview](knowledge/README.md), then use the [Master timeline](knowledge/timeline/README.md) or a topic index:

- [People](knowledge/people/README.md)
- [Organizations](knowledge/organizations/README.md)
- [Guilds](knowledge/guilds/README.md)
- [Governance](knowledge/governance/README.md)
- [Economy](knowledge/economy/README.md)
- [Gameplay and products](knowledge/gameplay/README.md)
- [Technology](knowledge/technology/README.md)
- [Lore](knowledge/lore/README.md)
- [Media and creators](knowledge/media/README.md)
- [Events](knowledge/events/README.md)
- [Controversies and disputes](knowledge/controversies/README.md)
- [Research backlog](knowledge/research/README.md)

## Five-layer architecture

```text
archive/      Preserved evidence, source records, extraction packages, and provenance
knowledge/    Human-readable, reviewed historical knowledge and navigation
graph/        Machine-readable entity, relationship, and timeline conventions
operations/   Schemas, templates, pipeline code, tests, campaigns, and migrations
publication/  Workspace for articles, briefs, reports, and datasets
```

The [archive](archive/README.md) is the evidence layer. A record’s presence there means it was preserved; it does not mean every claim in it has been accepted as fact. The [knowledge](knowledge/README.md) layer contains reviewed synthesis and registries. Promotion from evidence to knowledge requires human review and does not erase older or conflicting evidence.

## Ingestion and review flow

```text
source
  -> archive/raw
  -> archive/normalized
  -> archive/source-records and archive/ingestion-packages
  -> proposed knowledge updates
  -> proposed graph updates
  -> human review
  -> knowledge/ and graph/
```

Ingestion campaigns stop in the archive by default. They do not automatically update canonical knowledge or the relationship graph. Engineering instructions and commands live in [operations](operations/README.md); the active ingestion package schema is [Repository Schema v2.1](operations/schema/REPOSITORY-SCHEMA-v2.1.md).

## Evidence and operations

- [Source records](archive/source-records/README.md)
- [Ingestion packages](archive/ingestion-packages/README.md)
- [Campaign summaries](archive/campaign-summaries/README.md)
- [Reconciliation records](archive/reconciliation/README.md)
- [Repository operations](operations/README.md)
- [Wave 1.5 migration map](operations/migrations/WAVE-1.5-ARCHITECTURE-MIGRATION.md)

## Repository principles

- Separate official statements from independently verified facts.
- Distinguish announcements, plans, approvals, releases, and execution.
- Preserve source lineage and contemporary understanding.
- Keep uncertainty, dissent, supersession, and open questions visible.
- Never treat archived evidence as automatically canonical.
- Exclude private, confidential, or improperly obtained material.

## Current status

Wave 1 evidence from Aephia, Intergalactic Herald, Hologram News Network, and official Star Atlas sources is preserved in `archive/`. Repository Schema v2.1 remains additive: existing Wave 1 artifacts were moved without being rewritten to the newer schema.
