# PIP-03 on-chain governance vote export

## Metadata

- Source ID: `SRC-SOLANA-PIP-03-D2B581A805EF`
- PIP: `PIP-03`
- Proposal UUID: `f5e7cde1-9a02-4670-ae40-1c932a4b8dad`
- Proposal hash: `676cfbc6bf`
- Ballot mechanism: `BINARY_PVP`
- Vote events: 479
- Unique wallets: 479
- Total PVP: 97325460.40894
- Authority: `A1 — operator-confirmed primary blockchain-derived official DAO export`
- Independent RPC reverification: `NOT_PERFORMED`

## Provenance

The record was extracted from `Star Atlas DAO PIP Votes/PIP-03.json` inside the operator-supplied archive. The archive is preserved unchanged at `archive/raw/governance-votes/pip-01-32/Star Atlas DAO PIP Votes.zip`.

## Evidence scope

This source establishes the supplied ballot records, wallet public keys, ordered selections, voting power, signed messages, lock metadata, validation payloads, and portal record timestamps. It does not establish implementation, treasury payment, or post-vote execution.

## Known limitations

- Validation payloads are preserved exactly but were not independently replayed against a Solana RPC endpoint.
- The export does not contain transaction IDs, slots, block times, cluster identifiers, RPC endpoints, or an internal checksum manifest.
- Wallet public keys are not inferred to be named people or organizations.
- This vote dataset does not establish proposal implementation, treasury payment, or post-vote execution.

## Artifact chain

- [Normalized vote events](../../../normalized/governance-votes/pip-01-32/vote-events.jsonl)
- [Proposal summaries](../../../normalized/governance-votes/pip-01-32/proposal-summaries.json)
- [Campaign reconciliation](../../../../operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/reconciliation-report.md)
