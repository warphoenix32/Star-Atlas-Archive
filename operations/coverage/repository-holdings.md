# Repository Holdings Baseline

Snapshot: `9dc39e47393d707f60d792227cf9f150a1031b28` on 2026-07-20.

## Product domains

| Path | Files | Bytes |
| --- | --- | --- |
| archive | 8291 | 271719386 |
| knowledge | 81 | 862734 |
| graph | 5 | 2865 |
| operations | 684 | 22642338 |
| publication | 20 | 349442 |

## Archive areas

| Path | Files | Bytes |
| --- | --- | --- |
| archive/campaign-summaries | 12 | 556766 |
| archive/ingestion-packages | 980 | 63849453 |
| archive/manifests | 7 | 667048 |
| archive/normalized | 1965 | 53353249 |
| archive/proposed | 4 | 26916 |
| archive/provenance | 7 | 9016 |
| archive/raw | 606 | 85668880 |
| archive/reconciliation | 963 | 575249 |
| archive/semantic | 69 | 52461585 |
| archive/source-records | 3677 | 14549962 |

## Structural findings

- The normalized URL inventory contains 3,232 rows but all dispositions are stale: 902 `PENDING` and 2,330 `DEFERRED` despite later completed campaigns.
- Central manifests and campaign summaries cover only part of the 19 campaign directories; campaign status is fragmented.
- Source Record formats differ by repository generation: Markdown-only, JSON-only, and paired JSON/Markdown all exist.
- No open pull requests existed at the baseline. Forty-two remote branches were already merged into main; four non-ancestor branches require classification.
