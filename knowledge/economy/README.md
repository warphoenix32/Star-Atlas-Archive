---
title: "Star Atlas Economy"
seo_title: "Star Atlas Economy: Tokens, Treasury, Reports, and Governance"
seo_description: "A reader's guide to the Star Atlas economy, including ATLAS, POLIS, voting power, treasury accounts, funding authorizations, and official economic reports."
knowledge_status: QUALIFIED
as_of: 2026-07-23
confidence: HIGH
page_risk_score: 4
page_risk_class: R2
evidence_basis:
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json"
  - "archive/campaign-summaries/campaign-delta-official/campaign-summary.json"
known_limitations:
  - "The archive does not yet contain a complete independently reconciled history of token supply, emissions, burns, balances, or treasury transactions."
  - "Official economic reports and Council tracker entries establish dated institutional claims, not independent audits."
research_gaps:
  - "Acquire and reconcile token genesis, emissions, burn, vesting, holder, and treasury transaction datasets."
  - "Complete report-level metric extraction and document methodology changes across the economic-report series."
review_after: 2027-01-20
---

# Star Atlas Economy

The Star Atlas economy is not one system or one balance sheet. It is a changing network of tokens, game economies, locking programs, governance mechanisms, treasury accounts, marketplaces, emissions programs, and official research publications. Understanding that history requires following each component on its own timeline.

This section is organized for readers first. It explains how the principal economic instruments fit together, while preserving the Archive's stricter evidence boundary: a design statement is not a launch, a scheduled payment is not a transfer, a Council report is not an independently verified transaction, and a historical supply claim is not a current supply measurement.

## Begin with the two tokens

[Foundational Dossiers](../Foundational-Dossiers.md) places this economic history beside its governance, treasury, and product contexts.

[ATLAS](ATLAS-Token-History.md) is documented as the ecosystem's transferable utility and exchange token. Across different periods it has appeared in marketplace transactions, gameplay rewards and costs, locking programs, treasury holdings, and proposal payment terms. Those roles should not be collapsed into a single claim about the token's current utility or emissions.

[POLIS](POLIS-Token-History.md) is the governance token. Locked POLIS positions contribute to [POLIS Voting Power](PVP-Voting-Power.md), but the transferable token, a locked position, the locker program, a voting snapshot, and the derived PVP value are distinct objects. This matters when reading vote results or historical statements about governance concentration.

## Treasury and public spending

The [DAO Treasury Architecture](DAO-Treasury-Architecture.md) describes the wider institutional and account system. Within it, the **DAO Treasury account** is one specifically named Solana account. The Ecosystem Fund wallet, token lockers, emissions accounts, and sales accounts remain separate entities even when they participate in a common financial process.

The [Treasury Authorization and Reported Payment Ledger](Treasury-Authorization-and-Payment-Ledger.md) follows spending claims through separate states:

1. a proposal requests authority;
2. a vote may approve or reject it;
3. approval may authorize a payment;
4. the Council or another institution may report operational progress;
5. a primary transaction may verify asset movement;
6. separate evidence may verify delivery or completion.

No earlier state automatically proves a later one. This is especially important for mixed ATLAS/USDC requests and milestone-based awards, where nominal values, token quantities, payment timing, and deliverable acceptance may all require different artifacts.

## Official economic research

The [Economic Report Catalog](Economic-Report-Catalog.md) inventories the
official quarterly series beginning in 2022 Q2. The Archive preserves 17
quarterly PDFs through 2026 Q2 plus one economics paper. These reports are
valuable historical sources for metrics, methods, policy discussion, and the
publisher's interpretation of economic activity. They are not warranties of
accuracy, and figures from different quarters should not be joined into a time
series until their definitions and methodology have been reconciled.

The catalog also records incomplete work: PDF-level preservation, appendix review, duplicate resolution, metric definitions, and methodology changes. That distinction lets readers use the reports now without mistaking the presence of a publication for a completed economic dataset.

## How to read economic claims

Economic pages use four practical questions:

- **What object is being discussed?** A token, account, wallet, program, reward schedule, market surface, or simulated currency may share a name without being the same entity.
- **What date does the claim describe?** Tokenomics, program rules, balances, and market structures change.
- **Who made the claim?** Official publications establish what Star Atlas institutions stated; Council trackers establish attributed operational assessments; community reporting can add context but does not replace primary evidence.
- **What evidence state was reached?** Announcement, authorization, reported execution, transaction verification, and outcome verification are different.

## Related governance context

Economic authority is intertwined with governance. The [Governance and Economy Overview](../governance/Governance-and-Economy-Overview.md) explains the roles of the DAO, Foundation, Council, and Ecosystem Fund. The [PIP Registry](../governance/PIP-Registry.md) provides proposal-specific vote and lifecycle records.

## Current limits and research priorities

As of 2026-07-20, the repository supports a strong documentary history but not a complete economic audit. The highest-value missing artifacts are token mint and distribution records, emissions and burn transactions, dated treasury balances, proposal-linked payment signatures, recipient and signer evidence, report PDFs and appendices, and versioned definitions for recurring economic metrics.

Until those artifacts are reconciled, the knowledge base preserves official quantities as dated claims and avoids presenting them as independently verified current facts.

## Review status

This economy index is ready for publication as a qualified guide. Its linked histories preserve the distinction among reported measurements, authorization, payment, transaction verification, and independently assessed outcomes.
