# Phase 2 Legacy Written Raw-capture Schedule

Status: **`READY_FOR_CAMPAIGN_APPROVAL`**. No collection has started.

The first recommended Phase 2 campaign freezes exactly 800 successful Alpha–Delta Source Records. It captures public live pages, proven first-party replacements, immutable Git objects, or public web-archive snapshots without rewriting existing normalized evidence.

## Batches

| Batch | Source family | Records | Priority |
| --- | --- | --- | --- |
| R0.1 | HNN written corpus | 157 | P0 |
| R0.2 | Aephia | 64 | P0 |
| R0.3 | Intergalactic Herald | 259 | P0 |
| R0.4 | Official Campaign Delta | 320 | P0 |

A preliminary 20-record pilot uses five records from each campaign to prove identity matching, checksums, and deterministic reruns.

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
