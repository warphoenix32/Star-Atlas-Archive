# Starbased Ship States Ingestion 2026-07

This campaign preserves the operator-submitted `rydn_starbased_ships_20260718.csv` byte-for-byte and publishes a qualified normalization of the 63 base-ship rows included in that export. It does not claim the export is complete, current, or independently verified against its asserted upstream Star Atlas document.

## Evidence and scope

- The immutable CSV is at `archive/raw/starbased-ship-states/rydn_starbased_ships_20260718.csv`.
- Custody and qualified lineage metadata are at `archive/provenance/starbased-ship-states/rydn_starbased_ships_20260718.json`.
- Ryden Systems is the observed distributor and derivative source. Star Atlas is the upstream authority asserted by the repository operator. The upstream document URL/version remain `UNKNOWN`; this lineage is not independently verified.
- The normalized collection is only “the 63 base-ship rows included in the 2026-07-18 Ryden export.” Collection completeness and current availability remain `UNKNOWN`.
- Captured values are modeled as base-template values intended to be common across SAGE and C4 on the basis of `OPERATOR_SUPPLIED_CONTEXT`. Future rebasing is possible.
- Holosim uses a different value system and is out of scope.
- Future component modifiers belong to individual ship instances. No hypothetical modifier is applied to these base templates.

## Normalization policy

Ship shorthand codes, ship names, and specialization labels are preserved exactly as captured. Shorthand codes usually align with marketplace ship IDs according to operator context, but exact per-row equivalence is unverified. Marketplace hyperlinks are missing and remain unrecovered; no URLs are invented.

The concise normalized record includes 20 captured metric fields. Three semantically unknown duplicate/derived fields are omitted:

- `USDC /Cargo Capacity`;
- `USDC /Mining Rate`;
- `Cargo /Warp Fuel`.

Their exact values remain in the immutable raw CSV, and each omission appears in `normalization-map.json` and the normalized metadata field-disposition ledger.

Warp speed is interpreted literally as `100000` astronomical units per second for all 63 rows under operator-supplied context. Ship-specific warp cooldowns are retained. Other unit labels and values are preserved as captured where their native scales remain unresolved.

## Outputs

- `archive/normalized/starbased-ship-states/base-ships.jsonl`: 63 qualified base-template records.
- `archive/normalized/starbased-ship-states/metadata.json`: collection scope, lineage qualifications, field-disposition ledger, and review gaps.
- `normalized-preview.jsonl`: deterministic campaign-local copy of the qualified records.
- `source-profile.json`: structural, lineage, scope, and data-quality profile.
- `normalization-map.json`: complete 26-column mapping and disposition ledger.
- `context-questions.json`: all eight curator answers, decision authority, status, and retained gaps.
- `manifest.json`, `campaign-summary.json`, and `validation-report.json`: reproducibility and validation evidence.

No files under `knowledge/`, `graph/`, or `publication/` are changed.

## Reproduction

Run from the repository root:

```powershell
python operations/campaigns/starbased-ship-states-ingestion-2026-07/build_campaign.py
python operations/campaigns/starbased-ship-states-ingestion-2026-07/validate_campaign.py
```

## Retained research gaps

Qualified record-level normalization is allowed, but manual review remains required for:

1. the missing upstream Star Atlas document URL/version and unverified lineage;
2. unknown collection completeness/current availability;
3. unverified marketplace ID alignment and missing hyperlinks;
4. unresolved units/scales outside the explicit warp-speed/AU decision.
