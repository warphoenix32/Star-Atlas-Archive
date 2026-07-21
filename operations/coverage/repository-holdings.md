# Repository Holdings Baseline

Snapshot: `19a447596c6cb3b5e72343a0e6ef9dd87b3e51ed` on 2026-07-20.

## Product domains

| Path | Files | Bytes |
| --- | --- | --- |
| archive | 8361 | 293254538 |
| knowledge | 81 | 850333 |
| graph | 5 | 2817 |
| operations | 719 | 22815652 |
| publication | 20 | 353141 |

## Archive areas

| Path | Files | Bytes |
| --- | --- | --- |
| archive/campaign-summaries | 12 | 545309 |
| archive/ingestion-packages | 980 | 62269857 |
| archive/manifests | 8 | 670076 |
| archive/normalized | 1968 | 76282222 |
| archive/proposed | 4 | 25678 |
| archive/provenance | 8 | 26172 |
| archive/raw | 607 | 87083234 |
| archive/reconciliation | 963 | 560693 |
| archive/semantic | 69 | 51249454 |
| archive/source-records | 3741 | 14540596 |

## Structural findings

- The immutable 3,232-row URL inventory now has a separate deterministic disposition overlay; 2,485 URLs remain explicitly unresolved.
- Twenty campaign directories are represented in the central campaign status register.
- Source Record formats differ by repository generation: Markdown-only, JSON-only, and paired JSON/Markdown all exist.
- No open pull requests existed at the baseline. Forty-four remote topic branches were already merged into main; four non-ancestor branches remain, with the economic-report branch classified for Phase 2 integration rather than merge.
