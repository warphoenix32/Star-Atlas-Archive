# Human Adjudication Queue

## Blocking before Phase 2 collection

- `REVIEW-PHASE2-RAW-RECOVERY`: approve, revise, or defer the frozen 800-record legacy written raw-capture campaign. Approval authorizes only the public-source recovery boundary recorded in `recovery-campaign-schedule.md`.

## Deferred, non-blocking decisions

- `REVIEW-6E92B789AF1CEAB2`: observed Discord handle `Michael` remains unmerged with Michael Wagner, per operator decision `DEFERRED`.
- `REVIEW-A2599BBFBEA526F5`: display tag `EMP` remains unresolved, per operator decision `DEFERRED`.

## Decisions to surface before destructive cleanup

- Whether to delete the 44 remote topic branches already merged into `main`.
- Whether to retire `operations/migrations/validate_wave_1_5.py` or preserve it in a clearly historical location.
- Whether source-like campaign captures should move from `operations/` into `archive/raw/`; any move requires manifest and checksum migration.

These decisions do not block the evidence baseline. No deletion or relocation is performed by Phase 1 inventory.
