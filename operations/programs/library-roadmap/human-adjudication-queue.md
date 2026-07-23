# Human Adjudication Queue

## Blocking decisions

None. Phase 4 is closed and Phase 5 may begin editorial drafting without a blocking adjudication.

## Closed decisions

- `REVIEW-PHASE2-RAW-RECOVERY`: `CLOSED_SELECTED_SCOPE_COMPLETE`. Aephia, HNN, and Official are complete at 541/541 selected records. Five Herald pilot captures are preserved; the remaining 254 Herald records are deferred by the operator.
- `REVIEW-PHASE2-ECONOMIC-REPORTS`: `CLOSED_INGESTION_COMPLETE`. Eighteen operator-provided PDFs are preserved; the mislabeled Q4 2026 upload is excluded.
- `REVIEW-PHASE2-FRESHNESS`: `CLOSED_QUEUE_CREATED`. Seven official surfaces were checked and ten unmatched candidates were queued without ingestion.
- `REVIEW-PHASE3-PUBLICATION-CONTRACT`: `CLOSED_CONTRACT_VALIDATED`. The publication manifest and editorial boundary are stable; no public article or site change was made.
- `REVIEW-ATLAS-BREW-METADATA`: `CLOSED_PUBLIC_PLAYLIST_RECONCILED`. The 123 combined transcript records map at high confidence to the 124-item public playlist; Atlas Brew #7 is preserved separately as qualified machine transcription.
- `REVIEW-PHASE4-GATE1-EVIDENCE-DRIFT`: `CLOSED_EVIDENCE_RECONCILED`. Medium, Atlas Brew, and economic-report knowledge now reflects merged evidence while retaining completeness, event-date, speaker, and independent-verification limits.
- `REVIEW-PHASE4-GATE2-DOSSIER-EVIDENCE`: `CLOSED_PACKETS_COMPLETE`. All ten selected dossiers have reviewed evidence packets; no new source, identity, payment, election, lifecycle, or canon adjudication was required.
- `REVIEW-PHASE4-GATE3-DOSSIER-CONSOLIDATION`: `CLOSED_PUBLICATION_REVIEW_READY`. Ten dossier routes and seven lore foundations are consolidated. Council of Peace and Convergence War source divergence remains explicitly qualified rather than silently adjudicated.

## Deferred, non-blocking decisions

- `REVIEW-6E92B789AF1CEAB2`: observed Discord handle `Michael` remains unmerged with Michael Wagner, per operator decision `DEFERRED`.
- `REVIEW-A2599BBFBEA526F5`: display tag `EMP` remains unresolved, per operator decision `DEFERRED`.

## Decisions to surface before destructive cleanup

- Whether to delete the 44 remote topic branches already merged into `main`.
- Whether to retire `operations/migrations/validate_wave_1_5.py` or preserve it in a clearly historical location.
- Whether source-like campaign captures should move from `operations/` into `archive/raw/`; any move requires manifest and checksum migration.

These decisions do not block Phase 4. No deletion or relocation is performed by this closeout.
