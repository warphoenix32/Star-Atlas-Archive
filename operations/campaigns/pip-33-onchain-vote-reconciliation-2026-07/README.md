# PIP-33 On-Chain Vote Reconciliation

This evidence-ingestion campaign preserves and reconciles the complete 220-record PIP-33 vote export supplied by the repository operator. It adds vote evidence without changing canonical knowledge, graph facts, or publication outputs.

## Evidence model

- `vote-events.jsonl` retains one normalized record per supplied vote event, including the original voting-power string, five-decimal display value, signed message, signed timestamp, index timestamp, POLIS lock data, memo-program indicator, and exact exported Solana validation value. The export uses 88-character base64 signature bytes for 148 records and longer base64 signed-transaction payloads for 72 memo-enabled records; both representations are retained without coercion.
- `effective-ballots.jsonl` selects the latest indexed event per wallet without deleting superseded evidence. The supplied export contains one event per wallet, so no event is superseded.
- `proposal-summary.json` aggregates counts and PVP and applies the operator-adjudicated binary rule: YES PVP greater than NO PVP passes; NO PVP greater than YES PVP fails. Abstentions remain recorded but are not decisive. Equality is retained as `TIED`, not inferred as passage or failure.
- `reconciliation-report.*` compares the export with the existing canonical PIP ledger at the operator-approved five-decimal precision.

## Identity and faction boundary

Wallet public keys are stable ballot identities. Display names are self-selected aliases, so canonical identity mappings require human validation. The only mapping promoted here is the operator-verified `Siggy` wallet. Later campaigns may reuse that adjudication when the wallet matches and no contrary evidence exists.

Profile-name colors are separate UI evidence: red is MUD, blue is ONI, yellow is Ustur, and white or uncolored means no faction was selected. The supplied on-chain export contains no profile colors, so no ballot receives a faction enrichment.

## Preservation decision

The source was supplied as `PIP-33.txt` with SHA-256 `5ee6d3f844c4932db1195429aa191fe7c6ae21087c12520d636ebe3a4d8dfacb`. By operator decision, the recallable raw wrapper is not preserved. The normalized vote evidence retains the source checksum and exact per-record signatures.

## Reproduction

When the reviewed source export is locally available:

```text
python operations/campaigns/pip-33-onchain-vote-reconciliation-2026-07/import_vote_export.py --source PIP-33.txt
python operations/campaigns/pip-33-onchain-vote-reconciliation-2026-07/build_campaign.py
python operations/campaigns/pip-33-onchain-vote-reconciliation-2026-07/validate_campaign.py
```

Normal CI uses the committed normalized evidence and does not require the operator's local source wrapper.

## Limits

- Signatures are retained exactly but are not replayed against Solana in this campaign.
- This is ballot evidence only. It does not establish PIP-33 payment, treasury execution, implementation, or delivery.
- The export does not contain display names or profile-color observations.
