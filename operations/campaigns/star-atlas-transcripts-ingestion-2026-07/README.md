# Star Atlas Transcript Archival Ingestion Package

This package prepares three transcript collections for repository ingestion:

| Collection | Transcripts | Timestamped captions |
|---|---:|---:|
| Economic Forum | 11 | 16,295 |
| DAO | 11 | 23,713 |
| Town Hall | 14 | 38,744 |
| **Total** | **36** | **78,752** |

## Ingestion disposition

**READY FOR ARCHIVAL INGESTION**

The package contains preserved raw files, normalized Markdown transcripts, stable source records, checksums, manifests, normalization ledgers, and validation reports.

## Required repository handling

Ingest evidence into the archive and campaign-operations layers only. Do not write directly to `knowledge/`, `graph/`, or `publication/`.

After archival ingestion, run separate semantic-enrichment campaigns using the controlled Star Atlas taxonomy. Treat semantic output as candidates requiring review before knowledge promotion.

## Known research gaps

- Original source URLs were not included.
- Speaker labels were not included.
- Several DAO and Town Hall filenames lack complete publication dates.
- Transcript wording may contain automated-recognition errors.
- Filename-derived titles and dates require later reconciliation against original publications.
