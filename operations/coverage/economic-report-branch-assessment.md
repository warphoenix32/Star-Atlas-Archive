# Economic-report Branch Assessment

Decision: **`CLASSIFIED_DEFERRED_TO_PHASE_2`**

Do not merge or cherry-pick `origin/ingestion/economic-reports-2022q2-2026q2`. Its 17 official report URLs are useful discovery seeds, but its two unique files do not form a conforming, auditable ingestion campaign.

## Deficiencies

- No paired report JSON and Markdown Source Records
- No titles, authors, publication dates, immutable raw PDFs, or content checksums
- No campaign manifest, deterministic generator, or validator
- Fourteen reports are described as parsed although the extracted text is not retained

## Phase 2 disposition

- Freeze the 17 URLs as discovery seeds without treating the stale registry as evidence
- Retrieve and hash every accessible PDF
- Preserve page order and use OCR only when necessary
- Generate conforming Source Records, manifest, campaign summary, and validation
- Reconcile the apparent Q2 2025 duplicate without discarding provenance

The branch may be retired only after: Retire only after every discovery URL has a terminal Phase 2 disposition and all unique metadata has been preserved.

No human adjudication is required for this classification.
