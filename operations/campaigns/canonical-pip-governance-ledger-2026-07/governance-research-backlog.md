# Governance Research Backlog

This backlog identifies the exact evidence needed to promote unresolved fields. New acquisition is not performed in this campaign.

## GOV-RESEARCH-001 — P0

- PIPs: PIP-11, PIP-25, PIP-27
- Question: Who won the unresolved Council and DAO Casters elections, and what were the candidate-level totals?
- Missing artifacts: Official STV tabulation export; Official final winner announcement; Per-candidate PVP and transfer-round data
- Acceptance criteria: Winner identities reconcile to an official artifact; Candidate totals preserve the election mechanism; No candidate is inferred from later role occupancy
- On-chain dataset required: no
- Prohibited inference: Do not infer winners from later Council membership, social posts, or tracker passage alone.

## GOV-RESEARCH-002 — P0

- PIPs: PIP-5, PIP-8, PIP-12, PIP-14, PIP-16, PIP-17, PIP-18, PIP-20, PIP-21, PIP-22, PIP-29, PIP-30, PIP-33
- Question: Which authorized or Council-reported payments occurred on-chain?
- Missing artifacts: Transaction signatures; DAO/Foundation source accounts; Recipient token accounts; Mint and decimals metadata; Block timestamps; Proposal-to-transfer mapping
- Acceptance criteria: Every asserted transfer resolves to a transaction; Token amounts are decoded using the correct mint decimals; PIP authorization is not conflated with payment
- On-chain dataset required: yes
- Prohibited inference: Do not treat Council tracker amounts, vote passage, or a payment schedule as proof of transfer.

## GOV-RESEARCH-003 — P1

- PIPs: PIP-14, PIP-17, PIP-31
- Question: What primary records establish termination, cancellation, or withdrawal after passage?
- Missing artifacts: Council or Foundation termination notice; Author withdrawal notice; Contract or milestone closeout record
- Acceptance criteria: Terminal state has a dated primary record; Passage remains historically preserved; Payment and implementation remain separate
- On-chain dataset required: no
- Prohibited inference: Do not convert Council tracker terminology into independently verified completion or non-performance findings.

## GOV-RESEARCH-004 — P1

- PIPs: PIP-1, PIP-2, PIP-3, PIP-4, PIP-5, PIP-8, PIP-9, PIP-10, PIP-12, PIP-14, PIP-16, PIP-17, PIP-18, PIP-20, PIP-21, PIP-22, PIP-23, PIP-24, PIP-28, PIP-29, PIP-30, PIP-31, PIP-32, PIP-33
- Question: What independent evidence supports implementation or deliverable completion for each authorized non-election proposal?
- Missing artifacts: Proposal-specific deliverables; Foundation execution notices; Contracts or releases; Independent outcome evidence
- Acceptance criteria: Each implementation claim links to a primary artifact; Milestone reporting remains attributed; Failed proposals remain not authorized
- On-chain dataset required: no
- Prohibited inference: Do not equate 1/1 tracker milestones with independent implementation verification.

## GOV-RESEARCH-006 — P1

- PIPs: PIP-33
- Question: Which PIP-33 figures control the authorized and conditional tranche payments?
- Missing artifacts: Author or Foundation arithmetic correction; Executed payment instruction; Second-tranche reserve assessment
- Acceptance criteria: Both one-cent discrepancies are explicitly resolved; Each tranche remains 75% USDC and 25% ATLAS; Second-tranche reserve condition is preserved; Resolution does not imply payment
- On-chain dataset required: yes
- Prohibited inference: Do not silently choose a corrected cent value or infer that either tranche was paid.

## GOV-RESEARCH-007 — P1

- PIPs: PIP-25, PIP-27
- Question: Which candidate wallet belongs to each captured PIP-25 and PIP-27 candidate?
- Missing artifacts: Official candidate-to-wallet mapping; Signed candidate registration record or official ballot export
- Acceptance criteria: Each normalized wallet resolves to an official candidate record; The repeated sentinel remains preserved only as a captured placeholder
- On-chain dataset required: no
- Prohibited inference: Do not assign the repeated Solana sentinel value to any candidate and do not infer wallets from names or later officeholding.

## GOV-RESEARCH-005 — P2

- PIPs: PIP-1, PIP-2, PIP-3, PIP-4, PIP-5, PIP-6, PIP-7, PIP-8, PIP-9, PIP-10, PIP-11, PIP-12, PIP-13, PIP-14, PIP-15, PIP-16, PIP-17, PIP-18, PIP-19, PIP-20, PIP-21, PIP-22, PIP-23, PIP-24, PIP-25, PIP-26, PIP-27, PIP-28, PIP-29, PIP-30, PIP-31, PIP-32, PIP-33
- Question: Can historical portal state transitions be recovered?
- Missing artifacts: Timestamped proposal-state snapshots; Portal event log; Official lifecycle export
- Acceptance criteria: Publication, voting, result, and later lifecycle states have dated evidence; Portal state is not used as implementation proof
- On-chain dataset required: no
- Prohibited inference: Do not infer state-transition dates solely from vote windows.
