# Legacy Written Raw Recovery Validation

Status: **PASS**

| Check | Status | Detail |
|---|---|---|
| FROZEN_MANIFEST_EXISTS | PASS | operations/campaigns/legacy-written-raw-recovery-2026-07/frozen-manifest.json |
| FROZEN_MANIFEST_DETERMINISTIC | PASS | Generated manifest equals the current 800-record extraction inventory. |
| FROZEN_RECORD_COUNT | PASS | observed=800 expected=800 |
| UNIQUE_SOURCE_IDS | PASS | unique=800 total=800 |
| PILOT_SOURCE_IDS | PASS | Approved 20-record pilot is frozen exactly. |
| EXTRACTION_CHECKSUMS | PASS | All frozen extraction checksums reconcile. |
| SOURCE_RECORD_REFERENCES | PASS | Every declared Source Record path and frozen SHA-256 reconcile. |
| PILOT_SELECTION_RECONCILES | PASS | selection_ids=20 expected=20 |
| TERMINAL_DISPOSITIONS | PASS | terminal_records=20 |
| RAW_BODY_CHECKSUMS | PASS | Every successful raw body exists and matches its ledger SHA-256. |
| PROVENANCE_RECONCILES | PASS | Every successful provenance record reconciles to its Source ID and body checksum. |
| REQUIRED_PROVENANCE_FIELDS | PASS | Every preserved response has the complete Phase 2 provenance field set. |
| MANUAL_REVIEW_QUEUE | PASS | Manual-review queue equals the flagged terminal records. |
| PROTECTED_EVIDENCE_UNCHANGED | PASS | Frozen extraction and Source Record checksums are unchanged. |
| OUTPUT_SCOPE | PASS | Every declared raw and provenance output remains under its approved repository layer. |
| ARCHIVE_MANIFEST_RECONCILES | PASS | artifact_count=30 |
| CONTROLLED_TERMINAL_DISPOSITIONS | PASS | Every pilot record uses the frozen Phase 2 disposition vocabulary. |
| PROTECTED_LAYERS_ABSENT_FROM_OUTPUTS | PASS | No declared output enters a protected evidence, knowledge, graph, or publication layer. |
