# Validation Report

**Result: PASS**

- All 220 supplied vote events parse and retain unique event IDs, wallets, and Solana signatures.
- Signed-message wallet, vote, proposal hash, and timestamp structure were checked during import.
- The 220 effective ballots reproduce the supplied YES, NO, and abstain counts and PVP totals.
- The export reconciles with the canonical PIP ledger at five-decimal precision.
- Only the operator-verified Siggy wallet receives a canonical identity attribution.
- Signatures are preserved but were not independently replayed.
- No payment, implementation, or treasury-execution conclusion is made.
- Generated artifacts are deterministic.
- No `knowledge/`, `graph/`, or `publication/` files are changed.
