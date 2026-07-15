# Codex Ingestion Handoff

Ingest this prepared package into `warphoenix32/Star-Atlas-HNN-Archive`.

## Mission

Preserve and stage the Economic Forum, DAO, and Town Hall transcript collections without promoting claims into canonical knowledge.

## Required actions

1. Pull latest `main`.
2. Create a dedicated archival-ingestion branch.
3. Map each collection's:
   - `raw/` into a new campaign-specific location under `archive/raw/`
   - `normalized/` into `archive/normalized/`
   - `source-records/` into `archive/source-records/`
   - manifests, ledgers, and validation reports into `operations/campaigns/`
4. Preserve source IDs and checksums exactly.
5. Reconcile against existing repository source IDs and checksums before writing.
6. Do not overwrite or silently merge existing evidence.
7. Keep unknown speakers, missing URLs, and partial dates unresolved.
8. Add campaign-level validation for file counts, checksums, links, JSON parsing, source-ID uniqueness, and timestamp order.
9. Open a draft PR and stop.

## Prohibited

Do not modify:

- `knowledge/`
- `graph/`
- `publication/`

Do not perform semantic tagging or knowledge promotion in this ingestion PR.
