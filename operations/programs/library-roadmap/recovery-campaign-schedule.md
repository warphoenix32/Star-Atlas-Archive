# Phase 2 Legacy Written Raw-capture Schedule

Status: **`SELECTED_SCOPE_COMPLETE`**. The written-recovery milestone is closed for the operator-selected scope.

The immutable inventory contains 800 successful Alpha–Delta Source Records. Recovery completed for all 541 selected Aephia, HNN, and Official records. Five Intergalactic Herald pilot captures are preserved; the remaining 254 Herald records are explicitly deferred by the operator and are not counted as recovered.

## Batches

| Batch | Source family | Frozen records | Captured | Disposition |
| --- | --- | --- | --- | --- |
| R0.1 | HNN written corpus | 157 | 157 | COMPLETE |
| R0.2 | Aephia | 64 | 64 | COMPLETE |
| R0.3 | Intergalactic Herald | 259 | 5 | DEFERRED_BY_OPERATOR |
| R0.4 | Official Campaign Delta | 320 | 320 | COMPLETE |

The preliminary pilot captures remain preserved. Subsequent recovery completed the selected Aephia, HNN, and Official families; Herald recovery stopped after its five-record pilot under the operator's deferral.

## Stop rules

- Every frozen Source ID must receive exactly one terminal disposition.
- Three consecutive host-level 403, 429, or challenge responses stop that host batch without bypass.
- Identity mismatch, conflicting historic versions, or checksum failure stops only that item for review.
- New articles enter an out-of-scope discovery ledger and are not retrieved under this campaign.
- Nondeterministic identifiers, manifests, or checksums block campaign promotion.

## Human approval points

- Use of authenticated or restricted sources
- Ambiguous Source ID or URL identity matches
- Selection among conflicting historical versions
- Expansion to newly discovered articles

Unambiguous recovery from public live or public archive sources needs no item-by-item approval when provenance is retained.
