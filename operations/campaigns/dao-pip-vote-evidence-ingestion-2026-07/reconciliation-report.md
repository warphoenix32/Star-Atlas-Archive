# PIP-1 through PIP-32 Vote Evidence Reconciliation

The supplied primary blockchain-derived ballot export reconciles against the existing canonical PIP ledger without rewriting that ledger.

- Proposals compared: 32
- Proposals matching: 32
- Conflicting fields: 0
- Ranked-choice elections without reproducible final STV tally rules: 5
- PIP-33: excluded because it is already preserved by the existing PIP-33 vote campaign
- Canonical knowledge changed: no

## Proposal reconciliation

| PIP | Mechanism | Aggregate reconciliation | Election tally treatment |
|---|---|---|---|
| PIP-01 | BINARY_PVP | MATCH | Not applicable |
| PIP-02 | BINARY_PVP | MATCH | Not applicable |
| PIP-03 | BINARY_PVP | MATCH | Not applicable |
| PIP-04 | BINARY_PVP | MATCH | Not applicable |
| PIP-05 | BINARY_PVP | MATCH | Not applicable |
| PIP-06 | RANKED_CHOICE_ELECTION | MATCH | NOT_COMPUTED_STV_IMPLEMENTATION_RULES_NOT_CAPTURED |
| PIP-07 | RANKED_CHOICE_ELECTION | MATCH | NOT_COMPUTED_STV_IMPLEMENTATION_RULES_NOT_CAPTURED |
| PIP-08 | BINARY_PVP | MATCH | Not applicable |
| PIP-09 | BINARY_PVP | MATCH | Not applicable |
| PIP-10 | BINARY_PVP | MATCH | Not applicable |
| PIP-11 | RANKED_CHOICE_ELECTION | MATCH | NOT_COMPUTED_STV_IMPLEMENTATION_RULES_NOT_CAPTURED |
| PIP-12 | BINARY_PVP | MATCH | Not applicable |
| PIP-13 | BINARY_PVP | MATCH | Not applicable |
| PIP-14 | BINARY_PVP | MATCH | Not applicable |
| PIP-15 | BINARY_PVP | MATCH | Not applicable |
| PIP-16 | BINARY_PVP | MATCH | Not applicable |
| PIP-17 | BINARY_PVP | MATCH | Not applicable |
| PIP-18 | BINARY_PVP | MATCH | Not applicable |
| PIP-19 | BINARY_PVP | MATCH | Not applicable |
| PIP-20 | BINARY_PVP | MATCH | Not applicable |
| PIP-21 | BINARY_PVP | MATCH | Not applicable |
| PIP-22 | BINARY_PVP | MATCH | Not applicable |
| PIP-23 | BINARY_PVP | MATCH | Not applicable |
| PIP-24 | BINARY_PVP | MATCH | Not applicable |
| PIP-25 | RANKED_CHOICE_ELECTION | MATCH | NOT_COMPUTED_STV_IMPLEMENTATION_RULES_NOT_CAPTURED |
| PIP-26 | BINARY_PVP | MATCH | Not applicable |
| PIP-27 | RANKED_CHOICE_ELECTION | MATCH | NOT_COMPUTED_STV_IMPLEMENTATION_RULES_NOT_CAPTURED |
| PIP-28 | BINARY_PVP | MATCH | Not applicable |
| PIP-29 | BINARY_PVP | MATCH | Not applicable |
| PIP-30 | BINARY_PVP | MATCH | Not applicable |
| PIP-31 | BINARY_PVP | MATCH | Not applicable |
| PIP-32 | BINARY_PVP | MATCH | Not applicable |

## Interpretation boundary

Binary ballot counts and PVP totals match the existing ledger at five-decimal display precision. PIP-9 contains zero observed abstain records; this does not establish whether the interface offered an abstain option, so the ledger's capture limitation remains valid.

For PIP-6, PIP-7, PIP-11, PIP-25, and PIP-27, ordered ballots and first-preference statistics are preserved. Final STV tallies and winner identities are not recomputed because the exact tally implementation, quota, transfer, exhaustion, and tie-break rules are not supplied. Existing official outcome records remain separate evidence.

The ballot export does not establish authorization implementation, treasury payment, or post-vote execution.
