# Wave 1.5 Architecture Migration

## Executive summary

Wave 1.5 reorganizes the existing repository into five durable layers: `archive/`, `knowledge/`, `graph/`, `operations/`, and `publication/`. The migration changes paths and navigation without rewriting Wave 1 source evidence or the 27 pre-existing canonical knowledge records.

The migration began from `main` at `2721407`, after Repository Schema v2.1 and its Town Hall example packages were merged. Schema v2.1 remains additive; existing Wave 1 records were not upgraded or rewritten during this migration.

## Old-to-new path map

| Old path | New path | Decision |
| --- | --- | --- |
| `data/manifests/<inventory>.json` | `archive/raw/manifests/<inventory>.json` | Original input inventory |
| `data/manifests/normalized-urls.jsonl` | `archive/normalized/manifests/normalized-urls.jsonl` | Deterministic normalized manifest |
| `data/manifests/*.provenance.json` | `archive/provenance/manifests/` | Input provenance |
| `data/ingestion-packages/` | `archive/ingestion-packages/schema-v2.1/` | Schema v2.0/v2.1 packages retained together |
| `data/staging/<campaign>/extractions/` | `archive/ingestion-packages/<campaign>/extractions/` | Structured campaign extraction packages |
| `data/staging/<campaign>/source-records/` | `archive/source-records/<campaign>/` | Human-readable archival records |
| `data/staging/<campaign>/reconciliation/` | `archive/reconciliation/<campaign>/` | Official/community reconciliation |
| `data/staging/<campaign>/campaign-summary.*` | `archive/campaign-summaries/<campaign>/` | Campaign reports |
| `kb/01-master-index/` | `knowledge/index/` | Entity and repository indexes |
| `kb/02-chronology/` | `knowledge/timeline/` | Canonical chronology |
| `kb/03-atmta-and-institutions/` | `knowledge/organizations/` | Institutions and organizations |
| `kb/04-game-and-product-history/` | `knowledge/gameplay/` | Gameplay and products |
| `kb/05-economy-and-assets/` | `knowledge/economy/` | Economy and assets |
| `kb/06-governance-and-dao/` | `knowledge/governance/` | Governance and DAO |
| `kb/08-guilds-and-dacs/` | `knowledge/guilds/` | Guilds and DACs |
| `kb/09-major-actors/` | `knowledge/people/` | People and actor profiles |
| `kb/10-lore-and-canon/` | `knowledge/lore/` | Lore and canon |
| `kb/11-technology*/` | `knowledge/technology/` | Combined deterministic technology topics |
| `kb/12-media-and-creators/` | `knowledge/media/` | Media and creators |
| `kb/15-source-registry/` | `knowledge/index/source-registry/` | Reviewed source registries |
| `kb/16-open-questions/` | `knowledge/research/` | Research queues |
| `pipeline/` | `operations/pipeline/` | Ingestion code and package configuration |
| `pipeline/tests/` | `operations/tests/pipeline/` | Pipeline tests centralized under operations |
| `tests/` | `operations/tests/schema/` | Schema compatibility tests |
| `templates/` | `operations/templates/` | Operational templates |
| `docs/` | `operations/docs/`, `operations/schema/`, `operations/migrations/`, or `operations/campaigns/` | Routed by function |
| `examples/` | `operations/schema/examples/` | Schema examples |
| `promotion-wave-1.md` | `operations/campaigns/promotion-wave-1.md` | Campaign-operation record |

## Files moved and preserved

Before and after counts are identical for the major archival artifact classes:

| Artifact type | Before | After |
| --- | ---: | ---: |
| JSON extraction records | 800 | 800 |
| Markdown source records | 800 | 800 |
| Reconciliation JSON records | 960 | 960 |
| Campaign summary files | 8 | 8 |
| Schema v2.0/v2.1 ingestion packages | 2 | 2 |
| Inventory/provenance manifest files | 3 | 3 |
| Existing canonical knowledge files | 27 | 27 |

In total, 2,573 files from the former `data/` tree were compared against their new locations using Git blob hashes after line-ending normalization; all matched. The 27 former `kb/` files were checked the same way; all matched. Twenty-one existing operational files were moved from `pipeline/`, `templates/`, `docs/`, `examples/`, `tests/`, and the root promotion marker, with path-sensitive documentation and tests updated where necessary.

## Files created

- Human landing pages for the repository and every required knowledge topic.
- Archive directory guides explaining preservation and promotion boundaries.
- `graph/` conventions for IDs, types, relationships, lifecycle, updates, and provenance.
- `publication/` workspace guides without publication content.
- Operations landing pages and `validate_wave_1_5.py`.
- This migration record.

No new historical claims, graph facts, source records, extraction packages, or publication articles were created.

## Files and paths removed

The obsolete top-level `data/`, `kb/`, `pipeline/`, `templates/`, `docs/`, `tests/`, and `examples/` paths were removed after their contents were moved. Duplicate canonical copies were not retained.

## Compatibility decisions

- Repository Schema v2.1 was incorporated from merged PR #2 before migration; Wave 1 artifacts remain valid without destructive schema conversion.
- Pipeline imports and package name are unchanged. Only the package location and test paths changed.
- Future pipeline examples target `archive/raw`, `archive/normalized`, and `archive/provenance`.
- Internal navigation links were updated to the new architecture.
- Archived source text was not rewritten merely because it contains relative links from the source publication’s original context.
- Git moves and unchanged blob content preserve history detection where practical.

## Known limitations

- External websites, bookmarks, and historical GitHub permalinks that reference former repository paths cannot be redirected by a Git-only migration. This map is the compatibility reference.
- The graph directories define governance and provenance requirements but are intentionally not populated from existing extractions without review.
- The events and controversies indexes are landing pages only; Wave 1.5 did not synthesize new canonical entries.
- Archived evidence may contain source-publication-relative links that resolve only in the original publication context.

## Validation

The migration-specific validator checks required/obsolete paths, preservation counts, every repository JSON document, every normalized-manifest JSONL row, unique and paired campaign record IDs, and local Markdown navigation outside immutable archived source text.

Validation commands:

```bash
python -m pytest -c operations/pipeline/pyproject.toml operations/tests/pipeline
python operations/tests/schema/test_schema_compatibility.py
python operations/migrations/validate_wave_1_5.py
git diff --check origin/main...HEAD
```

Recorded migration validation:

- 800 extraction JSON files and 800 matching source-record Markdown files preserved.
- 960 reconciliation records preserved.
- Eight campaign summaries and two schema packages preserved.
- 1,769 JSON documents parse successfully.
- 3,232 JSONL records parse successfully.
- Five pipeline tests and three schema compatibility tests pass.
- The relocated CLI reproduces 3,232 normalized records from the preserved raw manifest.
- The migration validator resolves 107 repository-local Markdown links outside immutable archived source text.
- 2,573 moved archive files and 27 moved knowledge files have zero content mismatches against pre-migration Git blobs.
- Final diff and working-tree results are recorded in the pull request.

## Rollback guidance

Before merge, discard the migration branch and return to `main`. After merge, use normal `git revert` commits for the Wave 1.5 migration commits so the rollback remains auditable; do not rewrite shared history. Because source contents and Git blobs are preserved, the old path layout can be reconstructed from the old-to-new map without re-ingestion.

## Preservation statement

No Wave 1 source evidence was discarded. Archived evidence and canonical knowledge remain separate, and promotion into `knowledge/` or `graph/` continues to require human review.
