# Economic Forum Transcript Ingestion Package

This package prepares 11 timestamped transcripts for archival ingestion.

## Contents

- `raw/`: immutable copies of the supplied transcript files, renamed by stable source ID.
- `normalized/`: Markdown transcripts with auditable metadata and one normalized caption per timestamp.
- `source-records/`: structured provenance and limitation records.
- `manifest.json`: collection-level counts, checksums, and file inventory.
- `operations/normalization-ledger.md`: transformations applied during preparation.
- `operations/validation-report.md`: ingestion-readiness checks.

## Boundary

No transcript claim has been promoted into canonical knowledge. Speaker identity, original URLs, and unresolved dates remain explicit research gaps.
