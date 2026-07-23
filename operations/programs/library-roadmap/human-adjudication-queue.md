# Human Adjudication Queue

## Blocking decisions

None for the closed written-recovery milestone.

## Closed decisions

- `REVIEW-PHASE2-RAW-RECOVERY`: `CLOSED_SELECTED_SCOPE_COMPLETE`. Aephia, HNN, and Official are complete at 541/541 selected records. Five Herald pilot captures are preserved; the remaining 254 Herald records are deferred by the operator.

## Deferred, non-blocking decisions

- `REVIEW-6E92B789AF1CEAB2`: observed Discord handle `Michael` remains unmerged with Michael Wagner, per operator decision `DEFERRED`.
- `REVIEW-A2599BBFBEA526F5`: display tag `EMP` remains unresolved, per operator decision `DEFERRED`.

## Decisions to surface before destructive cleanup

- Whether to delete the 44 remote topic branches already merged into `main`.
- Whether to retire `operations/migrations/validate_wave_1_5.py` or preserve it in a clearly historical location.
- Whether source-like campaign captures should move from `operations/` into `archive/raw/`; any move requires manifest and checksum migration.

These decisions do not block the evidence baseline. No deletion or relocation is performed by Phase 1 inventory.
