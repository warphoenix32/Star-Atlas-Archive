---
title: "Star Atlas DAO Treasury Architecture"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: HIGH
page_risk_score: 6
page_risk_class: R2
canonical_entity: SYSTEM-STAR-ATLAS-TREASURY-ARCHITECTURE
aliases:
  - "Star Atlas DAO treasury architecture"
named_accounts:
  - "DAO Treasury account — CuwnarNh7FEqZMmffFjRyWj54RecyS7zwFg1CxfzNudi"
first_seen: 2024-07-08
last_reviewed: 2026-07-17
source_priority:
  - A1
  - A2
  - A3
related_entities:
  - Star Atlas DAO
  - Star Atlas Foundation
  - Star Atlas Council
  - Ecosystem Fund
depends_on:
  - knowledge/governance/Ecosystem-Fund.md
  - knowledge/governance/Governance-Implementation-and-Evidence-States.md
supersedes: []
superseded_by: []
evidence_basis:
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json"
  - "archive/source-records/governance/council-pip-tracker/SA-COUNCIL-TRACKER-D1DADF7EB8437119.json"
  - "operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl"
  - "archive/source-records/campaign-delta-official/SRC-OFF-4312E3B0005E60A3.md"
known_limitations:
  - "This page describes the captured governance design, not current balances, signers, or independently verified control of every account."
  - "Council tracker payment and milestone fields remain attributed operational assessments."
research_gaps:
  - "Verify current multisig signers, upgrade authorities, account ownership, and transaction history on-chain."
  - "Reconcile every Council-reported payment to a transaction and every milestone to a deliverable."
review_after: 2027-01-17
---

# Star Atlas DAO Treasury Architecture

The **Star Atlas DAO treasury architecture** is the wider system of governed accounts, programs, and institutional responsibilities used to authorize and execute DAO financial actions. Within that architecture, the **DAO Treasury account** is one specific named Solana account: `CuwnarNh7FEqZMmffFjRyWj54RecyS7zwFg1CxfzNudi`. The POLIS Locker, DAO Emissions account, DAO Sales Account, ATLAS Locker, and Ecosystem Fund wallet are separate components and must not be merged into that account's canonical identity.

A proposal can authorize spending from or through the treasury architecture without proving that a transfer occurred or that funded work was completed.

This page documents the architecture represented in the repository's captured sources. It is not a balance sheet, transaction ledger, or legal opinion. Wallet labels and program descriptions are source-attributed; the repository has not independently proved present-day control, upgrade authority, or custody.

## Constitutional framework

PIP-1 identifies a DAO Treasury account among the programs and accounts comprising the governance system and requires on-chain DAO approval before treasury disbursements. It assigns successful PIPs to the Star Atlas Foundation for implementation. [PIP-1; SRC-PIP-01-BC8475E4](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json)

PIP-2 describes the Foundation as the DAO's legal and operational agent and supports administrative, contracting, multisig, and implementation functions within the proposal's limits. Those institutional powers do not remove the requirement to distinguish authorization from execution. [PIP-2; SRC-PIP-02-1E2D7066](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json)

PIP-2 also approved a recurring annual budget capped at USD 100,000 for basic Foundation operations, including director, supervisor, registered-office, secretary, and related service costs. Costs beyond basic operations require separate advance DAO approval. That ceiling is an authorization, not evidence of annual expenditure. The Council tracker contains an unknown (`?`) USDC-paid value for PIP-2, so this archive cannot responsibly state an amount paid. [PIP-2; SRC-PIP-02-1E2D7066](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json) [Council tracker semantic records](../../operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl)

## Identified accounts and programs

PIP-1 names the following Solana mainnet components. The table records the proposal's identifiers verbatim; readers should verify live account ownership and program state on-chain before relying on them operationally.

| Component | Identifier in PIP-1 | Archival interpretation |
|---|---|---|
| POLIS Locker | `Lock7kBijGCQLEFAmXcengzXKA88iDNQPriQ7TbgeyG` | Locks POLIS used to derive voting weight. |
| POLIS Locker Snapshots | `snapNQkxsiqDWdbNfz8KVB7e3NPzLwtHHA6WV8kKgUc` | Snapshot component named by the charter. |
| DAO Proxy Rewarder | `gateVwTnKyFrE8nxUUgfzoZTPKgJQZUbLsEidpG4Dp2` | Rewarder component named by the charter. |
| DAO Treasury account | `CuwnarNh7FEqZMmffFjRyWj54RecyS7zwFg1CxfzNudi` | Specific general treasury account named by PIP-1 and PIP-23; not a label for the entire architecture. |
| DAO Emissions | `5MPLVoZ2cJHy8gkvFu9tCTuqu9P8Fm8xz8Swpo6TfjDu` | Emissions account named by the charter. |
| DAO Sales Account | `NPCxfjPxh6pvRJbGbWZjxfkqWfGBvKkqPbtiJar3mom` | Sales account named by PIP-1; also referenced in PIP-33's R4-sales appendix. |
| ATLAS Locker | `ATLocKpzDbTokxgvnLew3d7drZkEzLzDpzwgrgWKDbmc` | ATLAS locking component named by the charter. |
| Ecosystem Fund wallet | `BxKehkp298nQunu8BWxh5U6VvfphFyjEB3t7USst7Uag` | Separate bounded fund wallet identified by PIP-23. |

The architecture also names the ATLAS and POLIS token mints. Their inclusion in the governance specification does not imply that every asset held at a named address is unrestricted treasury capital.

## On-chain execution layer

Official support documentation describes a Goki smart wallet as an m-of-n multisig capable of executing Solana transactions and a Tribeca governor program that manages proposal lifecycle and queues approved actions for execution. This is official technical description as of its 2025 update; current deployment, signers, and upgrade authority require direct verification. [SRC-OFF-4312E3B0005E60A3](../../archive/source-records/campaign-delta-official/SRC-OFF-4312E3B0005E60A3.md)

The resulting authority chain must be read in stages:

1. a PIP specifies an action and requested authority;
2. PVP-weighted voting produces a result under the applicable mechanism;
3. a successful PIP is referred to the Foundation for safe and lawful implementation;
4. an authorized signer set may execute a transaction;
5. the transaction proves asset movement, but not necessarily acceptance of a milestone or success of the funded work;
6. outcome claims require additional deliverable or operational evidence.

PIP-1 and PIP-2 allow the Foundation to decline unsafe, unlawful, misleading, or otherwise improper implementation while providing an explanation. This is an implementation safeguard; it is not an independent legislative veto that changes the recorded vote result.

## Ecosystem Fund relationship

PIP-23 is the controlling captured Ecosystem Fund framework. It specifies the named DAO Treasury account and the separate Ecosystem Fund wallet, allocation and refill formulas, the USDC reserve threshold, USDC-denominated requests, ATLAS payments, and Council stewardship boundaries. The proposal includes transaction references for prior refills, but each transaction and later payment still requires claim-specific reconciliation. [PIP-23; SRC-PIP-23-0ECF2928](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-23-0ECF2928.json)

The Ecosystem Fund is a bounded suballocation within the wider treasury architecture, not the only route by which POLIS holders may authorize a treasury obligation. PIP-33 expressly presents its reimbursement request as a direct, extraordinary measure against the named DAO Treasury account outside the standard Ecosystem Fund cap. The Council tracker semantic record also marks the proposal as not using the Ecosystem Fund. The semantic registry's contrary `STAR_ATLAS_ECOSYSTEM_FUND` funding-source label is therefore not promoted into knowledge. [PIP-33; SRC-PIP-33-397FEE39](../../archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-33-397FEE39.json) [Council tracker semantic records](../../operations/campaigns/social-governance-semantic-enrichment/input-council-tracker/council-pip-tracker-semantic-records.jsonl)

## Evidence states

The repository uses separate states for requested funding, passage, implementation pending, reported payment, partial implementation, completion, termination, cancellation, withdrawal, and independent verification. Council tracker fields use:

```yaml
assessment_source: STAR_ATLAS_COUNCIL_TRACKER
assessment_type: COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT
independent_verification_status: UNKNOWN
```

For treasury research, the minimum evidentiary chain is therefore: proposal text -> completed vote record -> implementation instruction or Foundation record -> transaction -> recipient/milestone evidence. Missing links are recorded as gaps rather than inferred from later summaries. A transaction reference embedded in a later proposal is useful primary-source attribution, but it still requires transaction-level reconciliation before the archive labels it independently verified.

## Known source conflicts

- The PIP registry semantic layer labels PIP-33 with an Ecosystem Fund funding source, while the primary proposal names the DAO Treasury account, states that the request exceeds the Ecosystem Fund cap, and the Council tracker marks `ecosystem_fund: NO`. This page follows the primary proposal and preserves the semantic label as a rejected conflict.
- The governance portal capture's generic status fields do not by themselves encode implementation. Vote totals, proposal text, Council operational assessments, and transfer evidence must be evaluated separately.
- Council tracker milestone counts are Council-authored operational assessments. A value such as `1/1` is not automatically a transaction receipt or independent proof of completion.

## Current state

As of 2026-07-17, the archive supports the institutional and program architecture above and the identity of the named DAO Treasury account. It does not establish live balances, current signers, or transaction-level verification of every disbursement. See [PIP-33 ATMTA Historic Expense Reimbursement](../governance/PIP-33-ATMTA-Historic-Expense-Reimbursement.md) for the direct-account case and its unresolved payment state.
