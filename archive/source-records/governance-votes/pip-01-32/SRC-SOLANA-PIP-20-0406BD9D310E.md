# PIP-20 on-chain governance vote export

## Metadata

- Source ID: `SRC-SOLANA-PIP-20-0406BD9D310E`
- PIP: `PIP-20`
- Proposal UUID: `159cb743-f8cf-4932-8e01-e6f1a0b479ff`
- Proposal hash: `d02751e097`
- Ballot mechanism: `BINARY_PVP`
- Vote events: 150
- Unique wallets: 150
- Total PVP: 122487813.17666
- Authority: `A1 — operator-confirmed primary blockchain-derived official DAO export`
- Independent RPC reverification: `NOT_PERFORMED`

## Provenance

The record was extracted from `Star Atlas DAO PIP Votes/PIP-20.json` inside the operator-supplied archive. The archive is preserved unchanged at `archive/raw/governance-votes/pip-01-32/Star Atlas DAO PIP Votes.zip`.

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
