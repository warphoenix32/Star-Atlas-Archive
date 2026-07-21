# PIP-11 on-chain governance vote export

## Metadata

- Source ID: `SRC-SOLANA-PIP-11-9DD733601F08`
- PIP: `PIP-11`
- Proposal UUID: `7b48a62d-13c3-4a1e-8565-6ea7bfb4b4dc`
- Proposal hash: `42e2e01186`
- Ballot mechanism: `RANKED_CHOICE_ELECTION`
- Vote events: 348
- Unique wallets: 348
- Total PVP: 150046997.08185
- Authority: `A1 — operator-confirmed primary blockchain-derived official DAO export`
- Independent RPC reverification: `NOT_PERFORMED`

## Provenance

The record was extracted from `Star Atlas DAO PIP Votes/PIP-11.json` inside the operator-supplied archive. The archive is preserved unchanged at `archive/raw/governance-votes/pip-01-32/Star Atlas DAO PIP Votes.zip`.

## Evidence scope

This source establishes the supplied ballot records, wallet public keys, ordered selections, voting power, signed messages, lock metadata, validation payloads, and portal record timestamps. It does not establish implementation, treasury payment, or post-vote execution.

## Known limitations

- Validation payloads are preserved exactly but were not independently replayed against a Solana RPC endpoint.
- The export does not contain transaction IDs, slots, block times, cluster identifiers, RPC endpoints, or an internal checksum manifest.
- Wallet public keys are not inferred to be named people or organizations.
- This vote dataset does not establish proposal implementation, treasury payment, or post-vote execution.
- Final STV election tallies and winners are not derived because the tally implementation is not captured in this package.

## Artifact chain

- [Normalized vote events](../../../normalized/governance-votes/pip-01-32/vote-events.jsonl)
- [Proposal summaries](../../../normalized/governance-votes/pip-01-32/proposal-summaries.json)
- [Campaign reconciliation](../../../../operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/reconciliation-report.md)
