# Lore Repository Ingestion — 2026-07

This campaign preserves and normalizes the public `JoseEduardonoot/star-atlas-lore` repository as an operator-designated authority for Star Atlas lore taxonomy and preferred nomenclature. The Archive remains the system of record.

## Authority boundary

The authority designation is limited to in-universe taxonomy, classification, and preferred names. It does not make the upstream repository an ATMTA publication, independently verify every narrative claim, or override non-lore governance and historical evidence. The upstream repository metadata describes the project as fan-created, while the `main` branch and deployed site use an "Official Star Atlas Lore Encyclopedia" description. That identity discrepancy is preserved for review.

The campaign uses the immutable `main` commit `22555f277eb1496e34c0839c8f1f382842bd1d2b`. The repository default branch was `master` at capture time, but the live site was deployed from the separate `gh-pages` branch. All branch and deployment identities remain explicit in provenance.

## Processing model

1. Preserve the commit-pinned GitHub source archive and live-site inventory captures.
2. Inventory every repository file and every Markdown page.
3. Treat `canon/**/*.md` as the upstream canonical authoring corpus.
4. Treat `docs/**/*.md` as the published presentation layer, recording exact, divergent, missing, and presentation-only mirrors.
5. Preserve but exclude `c4-internal/**` working material from canonical lore normalization.
6. Normalize page metadata, headings, links, media references, taxonomy, source-local entities, and evidence-bound reference relationships.
7. Produce compatibility mappings for existing Archive lore IDs without rewriting historical evidence.

Text normalization is deliberately mechanical: UTF-8 BOM removal, LF line endings, trailing line-whitespace removal, and one final newline. The immutable commit archive retains the upstream bytes and remains the authority for exact historical wording and formatting.

Campaign manifests hash tracked integration text in an explicit `UTF8_LF` mode so the same commit validates identically on Windows and Linux. Immutable raw captures and generated binary artifacts remain byte-hashed.

## Identifier policy

- Page Source IDs are deterministic hashes of the upstream scope and repository-relative path.
- Lore taxonomy entity IDs use the `LRTX-` namespace. They are source-taxonomy identifiers, not allocations from the repository-wide canonical entity registry.
- Existing Archive lore IDs remain unchanged and are connected through the taxonomy migration mapping.

## Schema compatibility

Repository Schema v2.1 broad entity types remain unchanged. The normalized lore layer adds a controlled `lore_type` refinement. For example, `SPECIES` refines `COMMUNITY`, `FACTION` refines `ORGANIZATION`, and `PLANET`, `WORLD`, `SECTOR`, and `STAR_SYSTEM` refine `LOCATION`. The explicit compatibility map is stored in `archive/normalized/lore/taxonomy.json`.

## Deterministic commands

```text
python operations/campaigns/lore-repository-ingestion-2026-07/build_campaign.py
python operations/campaigns/lore-repository-ingestion-2026-07/validate_campaign.py
```

The builder reads only the preserved commit archive and the two preserved live-site captures. It performs no network access.

## Review boundaries

- No `knowledge/`, `graph/`, or `publication/` file is changed.
- No upstream wording is rewritten.
- Broken upstream links, divergent publication mirrors, unresolved identity mappings, missing licensing metadata, and embedded workstation paths are documented rather than silently corrected.
- This campaign is archival ingestion only. Claim-level semantic promotion requires a later reviewed campaign.
