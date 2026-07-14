# Archive

The archive is the machine-oriented evidence and preservation layer. Its contents retain source identity, provenance, extraction output, campaign boundaries, and reconciliation context. Archived material is evidence for review, not automatically canonical knowledge.

- [`raw/`](raw/README.md): immutable or minimally handled source captures and input inventories
- [`normalized/`](normalized/README.md): deterministic normalized manifests or transcripts
- [`ingestion-packages/`](ingestion-packages/README.md): structured JSON extractions and schema packages
- [`source-records/`](source-records/README.md): human-readable source records
- [`provenance/`](provenance/README.md): custody and source-origin metadata
- [`reconciliation/`](reconciliation/README.md): official/community comparison records
- [`manifests/hnn-combined-transcript.json`](manifests/hnn-combined-transcript.json): checksummed HNN transcript campaign manifest
- [`proposed/`](proposed/): staged, non-canonical knowledge and graph deltas awaiting review
- [`campaign-summaries/`](campaign-summaries/README.md): campaign coverage and validation reports

Promotion into [`knowledge/`](../knowledge/README.md) or [`graph/`](../graph/README.md) requires human review.
