# Star Atlas Latest Documents — Ingestion and Semantic Schema

This package prepares the latest supplied institutional sources for repository ingestion:

1. **Star Atlas Discord Announcements Semantic Enrichment**
   - 1,071 announcements
   - preserved as the previously completed enrichment package

2. **Star Atlas DAO Council — PIP Tracker & Grading Rubric**
   - living Council-maintained spreadsheet
   - 39 operational tracker records
   - 80 rubric/process-guidance records
   - all source sheets preserved as CSV and JSON
   - normalized review workbook included

## Source authority

The Council spreadsheet is treated as `TIER_1_COUNCIL_OPERATIONAL_TRACKER`.
It is authoritative for the Council's own operational records and assessments, but:

- Council ROI statements remain attributed assessments;
- payment and implementation claims require reconciliation with primary evidence;
- a passed vote remains distinct from implementation;
- later withdrawal, termination, or cancellation does not rewrite the historical vote result.

## Recommended repository placement

```text
archive/raw/governance/council-pip-tracker/
archive/normalized/governance/council-pip-tracker/
archive/semantic/governance/council-pip-tracker/
operations/campaigns/council-pip-tracker-ingestion/
```

Keep the Discord announcements corpus in its own source domain and reconcile through shared
entities, PIP identifiers, event dates, and lifecycle assertions.

## Validation

- Tracker header detected: True
- Semantic tracker records: 39
- Rubric records: 80
- Normalized workbook created: True
- Status: PASS
