# Repository Holdings Baseline

Snapshot: `9dc39e47393d707f60d792227cf9f150a1031b28` on 2026-07-20.

## Product domains

| Path | Files | Bytes |
| --- | --- | --- |
| archive | 8291 | 267075970 |
| knowledge | 81 | 850333 |
| graph | 5 | 2817 |
| operations | 684 | 22523265 |
| publication | 20 | 344682 |

## Archive areas

| Path | Files | Bytes |
| --- | --- | --- |
| archive/campaign-summaries | 12 | 545309 |
| archive/ingestion-packages | 980 | 62269857 |
| archive/manifests | 7 | 652500 |
| archive/normalized | 1965 | 52456184 |
| archive/proposed | 4 | 25678 |
| archive/provenance | 7 | 8820 |
| archive/raw | 606 | 84930144 |
| archive/reconciliation | 963 | 560693 |
| archive/semantic | 69 | 51249454 |
| archive/source-records | 3677 | 14376084 |

## Structural findings

- The normalized URL inventory contains 3,232 rows but all dispositions are stale: 902 `PENDING` and 2,330 `DEFERRED` despite later completed campaigns.
- Central manifests and campaign summaries cover only part of the 19 campaign directories; campaign status is fragmented.
- Source Record formats differ by repository generation: Markdown-only, JSON-only, and paired JSON/Markdown all exist.
- No open pull requests existed at the baseline. Forty-two remote branches were already merged into main; four non-ancestor branches require classification.
