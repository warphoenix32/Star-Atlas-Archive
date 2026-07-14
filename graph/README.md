# Relationship Graph

This layer defines machine-readable identities and relationships. Wave 1.5 establishes conventions but does not infer or bulk-populate graph facts from archival text.

## Canonical entity IDs

New IDs are registry-controlled, type-prefixed, stable, and never recycled (for example `PERSON-000001`, `ORG-000008`, `EVENT-000117`). Existing semantic IDs remain valid legacy aliases. Ingestion must use an unresolved label instead of inventing a permanent ID when the registry is unavailable.

## Entity types

Repository Schema v2.1 defines people, organizations, DAOs, corporations, tokens, features, technologies, game systems, game modes, ships, locations, resources, events, documents, products, communities, and guilds. Type additions require a documented schema change.

## Relationship types

Relationships use stable, directional verbs and explicit endpoints. Examples include `MEMBER_OF`, `CREATED_BY`, `PUBLISHED_BY`, `REPORTS_ON`, `REFERENCES`, `SUPERSEDES`, and source-lineage relationships defined by campaign schemas. Unknown relationships remain `UNKNOWN`; direction must not be guessed.

## Lifecycle states

Supported lifecycle states are `ANNOUNCED`, `PLANNED`, `IN_DEVELOPMENT`, `IN_TESTING`, `RELEASED`, `LIVE`, `DEPRECATED`, `CANCELLED`, and `SUPERSEDED`. State changes append dated evidence rather than overwriting history.

## Update rules

1. Resolve entities against the canonical registry before assigning permanent IDs.
2. Preserve legacy IDs as aliases.
3. Add relationships only when evidence supports both endpoints and direction.
4. Append lifecycle observations with dates; do not collapse plans into releases.
5. Stage proposed graph updates for human review before promotion.

## Provenance requirements

Every promoted relationship or lifecycle observation must identify one or more source IDs, the evidence location when available, extraction confidence, and the reviewing decision. Conflicts remain visible and linked to all supporting or contradicting sources.

- [`entities/`](entities/README.md)
- [`relationships/`](relationships/README.md)
- [`timelines/`](timelines/README.md)
- [`indexes/`](indexes/README.md)
