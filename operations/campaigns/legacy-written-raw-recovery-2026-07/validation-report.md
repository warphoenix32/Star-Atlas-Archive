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
| EXPANSION_SELECTION_DETERMINISTIC | PASS | batch=aephia-family-remaining-59 |
| EXPANSION_RECORD_COUNT | PASS | observed=59 expected=59 |
| EXPANSION_DISJOINT_FROM_PILOT | PASS | Expansion Source IDs exclude all 20 pilot records. |
| AEPHIA_FAMILY_COVERAGE | PASS | pilot=5 expansion=59 total=64 |
| EXPANSION_HOST_ALLOWLIST | PASS | allowed_host=aephia.com |
| EXPANSION_ENDPOINT_POLICY | PASS | path_prefix=/wp-json/wp/v2/; basis=PRIOR_FINAL_URL |
| HNN_SELECTION_DETERMINISTIC | PASS | batch=hnn-written-family-completion-156 |
| HNN_COMPLETION_RECORD_COUNT | PASS | observed=156 expected=156 |
| HNN_VERIFIED_BASELINE_DISJOINT | PASS | preserved_baseline=1 |
| HNN_FAMILY_SELECTION_COVERAGE | PASS | selection=156 baseline=1 family=157 |
| HNN_SOURCE_SURFACE_ALLOWLIST | PASS | allowed_hosts=['medium.com', 'web.archive.org']; basis=PRIOR_REQUESTED_URL |
| PILOT_LEDGERS_IMMUTABLE | PASS | All four approved pilot ledger hashes match the merged baseline. |
| PILOT_RAW_AND_PROVENANCE_IMMUTABLE | PASS | artifacts=30 aggregate_sha256=7370f2f123f157178cdba0acf115f00d7ffd6ad289106d7939c9bc9cd480c63e |
| TERMINAL_DISPOSITIONS | PASS | terminal_records=20 |
| RAW_BODY_CHECKSUMS | PASS | Every successful raw body exists and matches its ledger SHA-256. |
| PROVENANCE_RECONCILES | PASS | Every successful provenance record reconciles to its Source ID and body checksum. |
| REQUIRED_PROVENANCE_FIELDS | PASS | Every preserved response has the complete Phase 2 provenance field set. |
| MANUAL_REVIEW_QUEUE | PASS | Manual-review queue equals the flagged terminal records. |
| EXPANSION_TERMINAL_IDS | PASS | terminal_records=59 expected=59 |
| EXPANSION_RAW_BODY_CHECKSUMS | PASS | Every expansion raw body matches its ledger SHA-256. |
| EXPANSION_PROVENANCE_RECONCILES | PASS | Every expansion provenance record reconciles to its batch, Source ID, and body. |
| EXPANSION_REQUIRED_PROVENANCE_FIELDS | PASS | Every preserved expansion response has the complete provenance field set. |
| EXPANSION_MANUAL_REVIEW_QUEUE | PASS | Expansion manual-review queue equals its flagged terminal records. |
| EXPANSION_RETRY_SCOPE | PASS | attempt_records=59 |
| HNN_ARCHIVE_RESOLUTION_COVERAGE | PASS | resolved_records=156 expected=156 |
| HNN_ARCHIVE_CARRIER_POLICY | PASS | Every resolved HNN carrier is an exact timestamped public Wayback URL. |
| HNN_TERMINAL_IDS | PASS | terminal_records=156 expected=156 |
| HNN_RAW_BODY_CHECKSUMS | PASS | Every recovered HNN body matches its ledger SHA-256. |
| HNN_PROVENANCE_RECONCILES | PASS | Every recovered HNN record uses its declared exact-archive or public-live fallback tier and reconciles to its batch. |
| HNN_LIVE_FALLBACK_COMPLETENESS | PASS | Every Medium live fallback contains article publication metadata and structured body evidence. |
| HNN_REQUIRED_PROVENANCE_FIELDS | PASS | Every recovered HNN response has the complete provenance field set. |
| HNN_MANUAL_REVIEW_QUEUE | PASS | HNN manual-review queue equals its flagged terminal records. |
| HNN_RETRY_SCOPE | PASS | attempt_records=159 |
| CROSS_BATCH_SOURCE_IDS_UNIQUE | PASS | pilot=20 expansion=59 |
| HNN_PILOT_REPAIR_SCOPE | PASS | overlap=4 expected_repairs=4 |
| PROTECTED_EVIDENCE_UNCHANGED | PASS | Frozen extraction and Source Record checksums are unchanged. |
| OUTPUT_SCOPE | PASS | Every declared raw and provenance output remains under its approved repository layer. |
| NO_ORPHAN_RAW_OR_PROVENANCE | PASS | declared=460 actual=460 |
| ARCHIVE_MANIFEST_RECONCILES | PASS | artifact_count=460 |
| CONTROLLED_TERMINAL_DISPOSITIONS | PASS | Every terminal record uses the frozen Phase 2 disposition vocabulary. |
| CAMPAIGN_SUMMARY_RECONCILES | PASS | terminal_records=231 |
| PROTECTED_LAYERS_ABSENT_FROM_OUTPUTS | PASS | No declared output enters a protected evidence, knowledge, graph, or publication layer. |
