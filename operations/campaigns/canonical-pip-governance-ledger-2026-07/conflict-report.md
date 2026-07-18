# Canonical PIP Ledger Conflict Report

Every conflict is preserved rather than resolved by inference.

## GOV-CONFLICT-PORTAL-STATUS-001

- PIPs: PIP-1, PIP-2, PIP-3, PIP-4, PIP-5, PIP-6, PIP-7, PIP-8, PIP-9, PIP-10, PIP-11, PIP-12, PIP-13, PIP-14, PIP-15, PIP-16, PIP-17, PIP-18, PIP-19, PIP-20, PIP-21, PIP-22, PIP-23, PIP-24, PIP-25, PIP-26, PIP-27, PIP-28, PIP-29, PIP-30, PIP-31, PIP-32, PIP-33
- Classification: `STALE_PORTAL_STATE`
- Severity: `MATERIAL`
- Status: `OPEN_DOCUMENTED`
- Finding: Every captured portal object remains Proposal_Activated_Pending_Open_Voting after its recorded vote end.
- Treatment: Preserve the portal value as source metadata; derive no result or implementation state from it.
- Required artifacts: Timestamped official portal history or corrected proposal-state exports for PIP-1 through PIP-33.

## GOV-CONFLICT-ELECTION-WALLET-PLACEHOLDERS-001

- PIPs: PIP-25, PIP-27
- Classification: `PLACEHOLDER_WALLET_VALUE_IN_CAPTURE`
- Severity: `MATERIAL`
- Status: `OPEN_DOCUMENTED`
- Finding: The portal captures repeat the Solana sentinel value 11111111111111111111111111111111 across candidate wallet fields; it is not treated as a candidate identity.
- Treatment: Preserve the captured value separately, set normalized wallet_public_key to null, and require an official candidate-to-wallet mapping.
- Required artifacts: Official candidate-to-wallet mapping for PIP-25 and PIP-27.

## GOV-CONFLICT-FAILED-MILESTONES-001

- PIPs: PIP-13, PIP-15, PIP-19, PIP-26
- Classification: `NO_AUTHORIZATION_VS_TRACKER_MILESTONES`
- Severity: `MATERIAL`
- Status: `RESOLVED_BY_ADJUDICATION`
- Finding: The Council tracker reports milestone completion for four failed proposals that supplied no authorization.
- Treatment: Preserve the attributed tracker value but set ledger implementation to NOT_APPLICABLE_NO_AUTHORIZATION.
- Required artifacts: Corrected Council tracker rows or Council-authored explanation for the milestone values.

## GOV-CONFLICT-ELECTION-WINNERS-001

- PIPs: PIP-11, PIP-25, PIP-27
- Classification: `ELECTION_OUTCOME_MISSING`
- Severity: `MATERIAL`
- Status: `OPEN_DOCUMENTED`
- Finding: Council-reported passage exists, but the preserved portal captures contain no electionResults winner list.
- Treatment: Retain aggregate ballots/PVP and unresolved winner identity; infer no officeholder or program winner.
- Required artifacts: Official final ranked-choice result export identifying winners and candidate-level totals for PIP-11, PIP-25, and PIP-27.

## GOV-CONFLICT-ELECTION-CANDIDATE-PVP-001

- PIPs: PIP-6, PIP-7, PIP-11, PIP-25, PIP-27
- Classification: `CANDIDATE_TOTALS_MISSING`
- Severity: `MATERIAL`
- Status: `OPEN_DOCUMENTED`
- Finding: The portal captures preserve only aggregate ranked-choice ballots and PVP, not candidate-level PVP.
- Treatment: List captured candidates and set every candidate PVP field to null with MISSING_FROM_CAPTURE status.
- Required artifacts: Official per-candidate ranked-choice result exports for all five election PIPs.

## GOV-CONFLICT-PIP-027-BALLOT-CONFIG-001

- PIPs: PIP-27
- Classification: `PORTAL_BALLOT_CONFIGURATION_DISCREPANCY`
- Severity: `MATERIAL`
- Status: `OPEN_DOCUMENTED`
- Finding: PIP-27 records five winners, six maximum choices, and thirteen candidates while the proposal text describes five winners.
- Treatment: Preserve all captured values and do not normalize the maximum-choice field.
- Required artifacts: Official PIP-27 ballot configuration and final STV tabulation export.

## GOV-CONFLICT-PIP-033-FUNDING-SOURCE-001

- PIPs: PIP-33
- Classification: `DERIVED_SOURCE_MISCLASSIFICATION`
- Severity: `MATERIAL`
- Status: `RESOLVED_BY_ADJUDICATION`
- Finding: The semantic source labels PIP-33 as Ecosystem Fund, while the proposal identifies an extraordinary direct DAO Treasury measure and the Council tracker marks ecosystem_fund NO.
- Treatment: Use DIRECT_DAO_TREASURY_MEASURE and retain the semantic label as a rejected conflict.
- Required artifacts: None; resolved from existing evidence.

## GOV-CONFLICT-PIP-033-RESULT-001

- PIPs: PIP-33
- Classification: `TRACKER_RESULT_MISSING`
- Severity: `MATERIAL`
- Status: `OPEN_DOCUMENTED`
- Finding: The Council tracker result is null, while completed portal PVP supports the repository-reviewed PASSED result.
- Treatment: Preserve the tracker null and use the explicitly labeled repository editorial vote adjudication.
- Required artifacts: Corrected Council tracker result or an official final result record linked to PIP-33.

## GOV-CONFLICT-PIP-033-ARITHMETIC-001

- PIPs: PIP-33
- Classification: `SOURCE_ARITHMETIC_DISCREPANCY`
- Severity: `MATERIAL`
- Status: `OPEN_DOCUMENTED`
- Finding: Two displayed tranches sum to $469,513.52 versus the stated $469,513.53 total; displayed USDC portions sum to $352,135.14 versus the stated $352,135.15 aggregate.
- Treatment: Preserve both one-cent discrepancies without silent correction.
- Required artifacts: Author or Foundation correction identifying controlling PIP-33 payment amounts.

## GOV-CONFLICT-TREASURY-VERIFICATION-001

- PIPs: PIP-5, PIP-8, PIP-12, PIP-14, PIP-16, PIP-17, PIP-18, PIP-20, PIP-21, PIP-22, PIP-29, PIP-30, PIP-33
- Classification: `MISSING_ONCHAIN_DATASET`
- Severity: `MATERIAL`
- Status: `OPEN_DOCUMENTED`
- Finding: Council-reported payment values and PIP-33 authorization lack transaction-level on-chain evidence in the repository.
- Treatment: Use COUNCIL_REPORTED only for attributed tracker values and MISSING_ONCHAIN_EVIDENCE for verification; never mark paid or verified.
- Required artifacts: Transaction signatures, token-account addresses, mint/decimals metadata, block times, and proposal-to-transfer mapping.

## GOV-CONFLICT-PIP-001-QUORUM-001

- PIPs: PIP-1
- Classification: `EDITORIAL_RULE_NOT_SOURCE_NATIVE`
- Severity: `MATERIAL`
- Status: `RESOLVED_BY_ADJUDICATION`
- Finding: PIP-1 mentions quorum but supplies no numeric threshold; the completed-binary YES-versus-NO rule is an owner-approved repository editorial adjudication.
- Treatment: Label the adjudication as repository-editorial and never assert that it appears in PIP-1.
- Required artifacts: Source-native numeric quorum rule, if one governed these historical votes.
