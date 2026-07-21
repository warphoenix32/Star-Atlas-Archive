# Star Atlas DAO PIP Vote Evidence Ingestion

This campaign preserves and normalizes the operator-supplied Star Atlas DAO vote archive for PIP-1 through PIP-32. PIP-33 is present in the package but is deliberately excluded because `pip-33-onchain-vote-reconciliation-2026-07` already preserves and reconciles it.

## Authority and scope

The repository operator confirmed that the records were pulled directly from the Solana blockchain and viewed through the official Star Atlas DAO website. They are treated as `A1` primary blockchain-derived vote evidence for ballot selections, PVP, signed messages, wallet public keys, POLIS lock metadata, validation payloads, and portal record timestamps.

This campaign does not claim independent RPC replay. The package does not contain conventional transaction IDs, Solana slots, block heights, cluster or RPC identifiers, or an internal checksum manifest. Exact source bytes and every validation payload are preserved so later cryptographic or RPC verification remains possible.

Ballot evidence does not prove proposal implementation, treasury payment, program execution, or delivery.

## Outputs

- Immutable source ZIP under `archive/raw/governance-votes/pip-01-32/`.
- One normalized vote-event record for each of 8,404 supplied ballots.
- A compact effective-ballot index; every supplied proposal has one event per wallet, so no event is superseded.
- Thirty-two proposal summaries.
- One provenance record with ZIP and member checksums.
- Paired JSON and Markdown Source Records for every included PIP.
- Reconciliation, campaign summary, manifests, and validation reports.

## Election boundary

PIP-6, PIP-7, PIP-11, PIP-25, and PIP-27 contain ranked ballots. Their ordered candidate labels and descriptive first-preference statistics are preserved. Final Single Transferable Vote tallies are not recomputed because the supplied package does not establish the exact quota, transfer, exhaustion, and tie-break implementation. No winner is inferred.

## Timestamp boundary

Every event retains both the timestamp embedded in the signed message and the portal record's `createdAt` value. In 278 records, the portal timestamp precedes the signed-message timestamp. Those records are marked `TIMESTAMP_ORDER_ANOMALY`; neither timestamp is silently corrected or discarded.

## Reproduction

```text
python operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/import_vote_export.py --source "Star Atlas DAO PIP Votes.zip"
python operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/build_campaign.py
python operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/validate_campaign.py
```

The importer requires the exact reviewed ZIP with SHA-256 `4e01123f31a2531427fc1910841efae45e24b15f4472338fbbf174c2e5b52d08`.

## Repository boundary

This is an archive-evidence campaign. It does not modify `knowledge/`, `graph/`, or `publication/`. The reconciliation report shows how the supplied ballot aggregates compare with the existing draft canonical PIP ledger; later knowledge promotion may add the new evidence references without rewriting source records.
