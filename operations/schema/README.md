# Schemas

- [Repository Schema v2.1](REPOSITORY-SCHEMA-v2.1.md)
- [Ingestion Schema v2.1](INGESTION-SCHEMA-v2.1.md)
- [Schema compatibility](SCHEMA-v2.1-COMPATIBILITY.md)
- [Example v2.1 package](examples/ingestion-package-v2.1.json)
- [Simplified Promotion Campaign v1](PROMOTION-CAMPAIGN-v1.schema.json)
- [Promotion Campaign v1 example](examples/promotion-campaign-v1.json)
- [Publication Manifest v1](PUBLICATION-MANIFEST-v1.schema.json)
- [Publication Manifest v1 example](examples/publication-manifest-v1.json)

Schema v2.1 is additive; migration does not require rewriting Wave 1 evidence.

Promotion Campaign v1 is an opt-in operational contract. It does not replace Repository Schema v2.1 or rewrite older campaign reports.

Publication Manifest v1 governs the reviewed handoff from `knowledge/` into the
public Library. It is an editorial and build contract, not an evidence schema.
