---
publication_id: PUB-003
slug: following-the-treasury
title: "Following the Treasury: Authority, Funding and Payment Evidence"
seo_title: "Star Atlas Treasury History: Authority, Ecosystem Funding and Payment Evidence"
seo_description: "A guide to Star Atlas treasury architecture, Ecosystem Fund awards and the evidence needed to distinguish requests, authorization, payment and outcomes."
status: DRAFT
as_of: 2026-07-23
audience: "Readers following Star Atlas DAO funding and treasury history"
---

# Following the Treasury

Money creates some of the strongest claims—and the easiest misunderstandings—in a governance archive. A proposal may request funds, voters may approve it, a Council tracker may report a payment and a project may describe itself as complete. Those are four different pieces of evidence.

The Star Atlas record becomes much clearer once two similarly named concepts are separated. **Treasury architecture** is the wider institutional and account system through which governance assets, programs and payments are described. The **DAO Treasury account** is one specific named address within that architecture. The Ecosystem Fund wallet, lockers, emissions accounts and sales accounts are not aliases of that treasury account.

## The named accounts

The captured governance framework identifies the DAO Treasury account as:

`CuwnarNh7FEqZMmffFjRyWj54RecyS7zwFg1CxfzNudi`

PIP-23 identifies a separate Ecosystem Fund wallet:

`BxKehkp298nQunu8BWxh5U6VvfphFyjEB3t7USst7Uag`

Keeping those entities distinct prevents later research from treating every governed asset flow as movement through one wallet. It also matters for on-chain verification: a transaction can only be reconciled correctly when the source account, destination account, token mint, amount and authority are known.

## The Ecosystem Fund as a bounded program

The Ecosystem Fund is a policy instrument for financing community work, not the whole DAO Treasury. PIP-4 created its original framework. PIP-23 later replaced that policy in full.

Under the captured PIP-23 terms, applications state their request in USDC while the fund pays in ATLAS. A single award is limited by a formula tied to the balance after the latest refill, and a project may not exceed the stated duration. The policy also describes reserve treatment, quarterly review and Council responsibilities.

These rules define what may be requested and administered. They do not establish that the fund was replenished on schedule or that every authorized award was paid.

## Three kinds of evidence

A reliable funding history separates:

1. **Proposal and vote evidence.** This establishes the requested purpose, amount and whether voters authorized it.
2. **Operational reporting.** Council records may report amounts paid, milestones reached, balances remaining or a lifecycle such as complete or terminated.
3. **Primary execution evidence.** Transaction signatures and deliverable records can establish asset movement and work performed.

The current ledger is strongest at the first level. It contains valuable Council-authored assessments at the second level. It has not yet reconciled the full ledger to primary Solana transactions or independently reviewed every deliverable.

## What the award history shows

The captured Ecosystem Fund record includes community events, media, infrastructure, software, tournaments and other initiatives. Some entries are reported complete. Others are reported partial, terminated, canceled, withdrawn or of unknown lifecycle.

Mixed denomination fields require special caution. A tracker may contain both USDC and ATLAS values without establishing whether they represent separate payments, a conversion, a request amount and a settlement amount, or duplicated valuation. Adding those numbers would manufacture a total that the evidence does not support.

Similarly, a blank field is not proof that no payment occurred. It means the reviewed record did not establish one.

## PIP-33: an extraordinary direct authorization

PIP-33 sits outside the ordinary Ecosystem Fund award mechanism. It authorized a historic-expense reimbursement to ATMTA directly from the DAO Treasury under terms exceeding the fund’s ordinary cap.

The proposal states a total of **$469,513.53** divided into two approximately equal displayed tranches of **$234,756.76** each. Each tranche is composed of **75% USDC and 25% ATLAS-equivalent value**. The second tranche is scheduled 180 days later and is conditional on the treasury retaining the stated reserve.

The arithmetic contains preserved one-cent discrepancies. The two displayed tranche totals add to $469,513.52, one cent below the stated total. The displayed USDC portions also add one cent below the proposal’s stated USDC total. The archive records the discrepancy rather than silently correcting the source.

The vote evidence supports passage. It does not prove that either tranche was transferred.

## Refills are not awards

PIP-23 reports two Ecosystem Fund refills, one in October 2024 and another in July 2025. The proposal includes transaction references and balance calculations. Those references make the claims stronger than an unsupported summary, but they have not yet been independently reconciled in the archive.

A refill is movement into the bounded fund. It is not payment to a recipient, and it does not prove that any funded project produced an accepted result.

## What would close the gaps

A transaction-level ledger needs signatures, block times, source and destination accounts, token mints and decimals, exact quantities, signer context, recipient identity and any currency-conversion basis. A project-outcome ledger separately needs milestone definitions, submissions, acceptance authority, acceptance dates and surviving deliverables.

Until those artifacts are available, the responsible vocabulary remains **requested**, **authorized**, **Council-reported**, **unverified** or **missing on-chain evidence**. The treasury history is already significant, but significance does not require overstating its certainty.

## Explore the evidence

- [DAO Treasury Architecture](../../knowledge/economy/DAO-Treasury-Architecture.md)
- [Treasury Authorization and Reported Payment Ledger](../../knowledge/economy/Treasury-Authorization-and-Payment-Ledger.md)
- [Ecosystem Fund Award History](../../knowledge/governance/Ecosystem-Fund-Award-History.md)
- [Star Atlas Ecosystem Fund](../../knowledge/governance/Ecosystem-Fund.md)
- [PIP-33 Historic Expense Reimbursement](../../knowledge/governance/PIP-33-ATMTA-Historic-Expense-Reimbursement.md)

This draft does not perform or imply on-chain treasury verification.
