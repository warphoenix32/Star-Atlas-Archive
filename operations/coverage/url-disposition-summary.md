# URL Disposition Reconciliation

Snapshot: `19a447596c6cb3b5e72343a0e6ef9dd87b3e51ed` on 2026-07-20.

The original 3,232-row inventory is unchanged. This overlay records later campaign outcomes without claiming complete external coverage.

## Current dispositions

| Disposition | URLs |
| --- | ---: |
| `DEFERRED_UNRECONCILED` | 2234 |
| `INGESTED_CONFIRMED` | 480 |
| `EXCLUDED_NON_WRITTEN` | 247 |
| `PENDING_UNRECONCILED` | 251 |
| `EXCLUDED_EXTERNAL_WRITTEN` | 12 |
| `EXCLUDED_NAVIGATION` | 4 |
| `RETRIEVAL_FAILED` | 4 |

## Evidence boundary

- All 480 ingested records and four failures are supported by exact campaign result URL IDs.
- All 480 ingested records resolve to a preserved Markdown Source Record.
- Herald and HNN exclusions reproduce their published aggregate counts with deterministic creator and surface selectors; the campaigns did not preserve item-level exclusion ledgers.
- One duplicate content cluster is retained as two distinct Herald URL records.
- The 2,485 unreconciled rows retain historical `PENDING` or `DEFERRED` status and require bounded Phase 2 review.
- The 2,119 unreconciled YouTube URLs are not assumed absent from transcript holdings because those packages often lack source URLs and video IDs.
