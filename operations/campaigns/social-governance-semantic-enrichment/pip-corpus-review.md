# Star Atlas PIP Governance Corpus Review

**Corpus:** PIP-1 through PIP-33  
**Official source:** `govern.staratlas.com` portal payloads preserved in this campaign  
**Review posture:** Institutional analysis by the Star Atlas Chief of Staff and Knowledge Curator  
**Canonical status:** Review conclusions only; promotion into `knowledge/` requires a separate reviewed promotion campaign

## Executive assessment

The PIP corpus documents the transition of Star Atlas governance from a Foundation-administered constitutional framework into an operating community funding institution.

The governance system rests on four interacting bodies:

1. **POLIS holders / Star Atlas DAO** — exercise voting authority through PVP-weighted PIPs.
2. **Star Atlas Foundation** — legal and administrative implementation body, treasury custodian, portal administrator, and safety/compliance gate.
3. **Star Atlas Council** — elected process steward that assists authors, manages governance operations, administers programs, and recommends proposals for advancement.
4. **ATMTA and community service providers** — implement software, events, media, infrastructure, research, and other approved work.

The corpus is dominated by funding proposals. The DAO evolved from defining its own constitutional and administrative machinery into using the Ecosystem Fund as its principal policy instrument. Most later PIPs fund community-created infrastructure, media, events, research, automation, or product-adjacent services rather than modify game rules directly.

## Governing rules established by the corpus

### Voting result rule

For completed binary PIPs:

- `YES PVP > NO PVP` → `PASSED`
- `NO PVP >= YES PVP` → `FAILED`
- Abstentions are reported but do not change the comparison.

Ranked-choice elections are resolved through the portal election result where available. A passed proposal is not, by itself, evidence of implementation.

### Proposal lifecycle

The corpus supports these separate states:

`DRAFT → PENDING → VOTING → PASSED/FAILED → IMPLEMENTATION PENDING → PARTIALLY IMPLEMENTED/IMPLEMENTED`

The portal's recurring `Proposal_Activated_Pending_Open_Voting` value is stale for completed votes and must not be treated as the authoritative lifecycle result.

### Institutional authority

- The DAO expresses policy through PIPs and controls treasury allocations.
- The Foundation may screen proposals, administer voting, hold legal rights, contract with service providers, control treasury multisigs, and refuse unsafe or unlawful implementation with a public explanation.
- The Council is an administrative and facilitative body, not a sovereign substitute for POLIS holders.
- Council discretion expands in later program PIPs, especially for application review, milestone validation, payment release, exceptions, and program administration.

## PIP-by-PIP institutional index

| PIP | Title | Result | Institutional significance |
|---:|---|---|---|
| 1 | Star Atlas DAO | Passed | Foundational charter. Defines DAO scope, PIP categories and drafting requirements, Foundation administration, POLIS/PVP voting, treasury programs, and implementation referral. |
| 2 | Star Atlas Foundation | Passed | Ratifies the Cayman Foundation as the DAO's legal and operational agent; delegates screening, implementation, contracting, multisig, and maintenance authority; approves up to $100,000 annual operating budget. |
| 3 | Star Atlas Council | Passed | Creates a five-seat community administrative council, initially for six months, to guide PIP drafting and governance participation. |
| 4 | Star Atlas Ecosystem Fund | Passed | Creates the principal community-funding mechanism using 20% of eligible treasury assets and a 5% per-recipient/proposal ceiling. Later replaced by PIP-23. |
| 5 | Co-Sponsor the Naabathon | Passed | First major applied ecosystem grant: 6,000,000 ATLAS for hackathon prizes and DAO sponsorship visibility. |
| 6 | Council Election #1 — First Round | Election | First-stage ranked-choice election reducing 22 candidates to 12. Procedural election record rather than policy. |
| 7 | Council Election #1 — Second Round | Election complete | Elects JP, Funcracker, King Bryan, Bodhi TREE, and DRUMCARL05 to the first Council. |
| 8 | Star Atlas Comet at Gamescom 2025 | Passed | Funds a community-led physical event in Cologne, establishing real-world event sponsorship as a recurring DAO use case. |
| 9 | Adjust STV Backup Vote Handling | Passed | Technical governance reform correcting vote-transfer amplification in the STV implementation; linked to a concrete GitHub PR. |
| 10 | Council: Second Term & Beyond | Passed | Establishes five seats, nine-month terms, single-round STV elections, and a one-month member-elect overlap beginning with Term 3. |
| 11 | Council Election #2 | Election result unresolved in captured payload | Elects the second Council for April 2025–January 2026, but the captured portal payload lacks the conclusive winner field. Requires reconciliation from another official record. |
| 12 | Iris's Bounty: The Feast | Passed | Creates a Council-administered microgrant program for local social events using a dedicated multisig and simplified applications. |
| 13 | Council Term Limits | Failed | Attempted to replace unlimited re-election with a two-consecutive-term limit and one-term break. Failure leaves PIP-10's no-term-limit rule intact. |
| 14 | Deepening THEO Integration | Passed | Funds AI economic-assistant development, DAO knowledge-base RAG, integration readiness, repayment from transaction fees, and long-term revenue share. |
| 15 | In-Person Community Meetups Platform | Failed | Proposed a privately operated global meetup and ticketing platform. Rejection is important evidence that the DAO distinguishes direct event funding from platform/business-model funding. |
| 16 | Ryden Systems | Passed | Supports continued development of Eveeye/Ryden Systems with 5% of the Ecosystem Fund, reflecting willingness to subsidize proven community infrastructure. |
| 17 | Star Atlas Ecosystem Media Expansion | Passed | Initial 10,000,000 ATLAS tranche for media, educational assets, music integrations, community activity, and a film project; later tranches required separate votes. |
| 18 | Gamescom Marketing & Merch Expansion | Passed | Extends PIP-8 with merchandise, print, onboarding keys, banners, and professional media documentation. |
| 19 | Independent Economic Research and Data Resources | Failed | Proposed 44.8M ATLAS over four phases, with the first 11.2M tranche for economic research and data migration. Failure shows resistance to high recurring research/infrastructure commitments. |
| 20 | DAO Casters Program | Passed | Establishes five elected content creators for a three-month term, combining compensation with controlled promotional budgets. |
| 21 | Rogue Data Hub | Passed | Funds an open, community-operated Star Atlas data indexer/API as replacement infrastructure after Flipside discontinuation. |
| 22 | Iris's Bounty: The Arena | Passed | Creates a tournament co-funding program using a 2:1 DAO match, post-event validation, sponsorship requirements, and Council administration. |
| 23 | Refresh of PIP-4 | Passed | Replaces PIP-4. Clarifies refill formulas, wallet addresses, 5% ceiling, ATLAS-only payment, USDC conversion, 12-month maximum duration, and Council responsibilities. Includes direct on-chain evidence of prior fund refills. |
| 24 | DAO-Supported Hosting for SLY Assistant | Passed | Funds a three-month, usage-based hosting subsidy pilot, with monthly reporting and renewal contingent on adoption. |
| 25 | Council Election #3 | Election result unresolved in captured payload | Election for January–October 2026 Council term. Portal payload lists six candidates but lacks conclusive winners; reconcile from an official Council or Foundation announcement. |
| 26 | Crew Adventure Series | Failed | Requests the Ecosystem Fund ceiling for an AI-generated lore video season. Failure is relevant to policy around creator compensation, AI media, IP alignment, and maximum-fund asks. |
| 27 | DAO Casters Election: Term 1 | Election result unresolved in captured payload | Elects five of thirteen creators under PIP-20 and PIP-9 STV rules. Portal winner data requires reconciliation. |
| 28 | Temporary Funding for Lore, Design, and Community Functions | Passed | Exceptional direct treasury support for a former ATMTA contributor to remain embedded at ATMTA for six months. Establishes a precedent for DAO-funded preservation of core company capacity during layoffs. |
| 29 | Star Atlas Relay Program | Passed | Funds a bounded community gameplay-video incentive and distribution pilot; Aephia supplies the platform and hosting at no cost during the pilot. |
| 30 | ATOM Cloud Infrastructure Sustainability | Passed | Four-month operating-cost pilot preserving community automation infrastructure through C4, with early termination and return of funds if C4 releases first. |
| 31 | Star Seekers 2 Mobile Game | Passed | Funds completion and dual-store launch of an independently owned mobile game used as a Star Atlas onboarding channel; milestone payments but private ownership retained. |
| 32 | Star Atlas Triad Tournament | Passed | Funds professional production of a three-mode UE5 esports event, with milestone payments, conflict recusals, post-event reporting, and 1% revenue return to the DAO. |
| 33 | ATMTA Historic Expense Reimbursement | Passed | Extraordinary $469,513.53 treasury reimbursement to ATMTA for taxes and professional services, split 75% USDC/25% ATLAS across two tranches with treasury reserve protection and direct conflict disclosure. |

## Governance evolution

### Phase 1 — Constitutional formation: PIP-1 to PIP-4

The first four proposals form the constitutional core:

- PIP-1 defines the DAO and proposal process.
- PIP-2 supplies the legal entity and implementation bridge.
- PIP-3 creates a community administrative layer.
- PIP-4 creates the funding mechanism that becomes the dominant instrument of governance.

The architecture is deliberately hybrid. POLIS holders make formal decisions, while the Foundation supplies legal personality, custody, administration, and implementation capacity.

### Phase 2 — First operations and elections: PIP-5 to PIP-11

The DAO begins spending, electing administrators, and repairing voting mechanics:

- Naabathon tests treasury-funded ecosystem development.
- Council elections operationalize representative administration.
- PIP-9 demonstrates that governance software itself is amendable through PIPs.
- PIP-10 converts the Council from an experiment into a durable institution.

### Phase 3 — Programmatic community funding: PIP-12 to PIP-24

The Ecosystem Fund becomes a portfolio of programs and service contracts:

- micro-events and tournaments;
- AI assistants and community tools;
- developer and data infrastructure;
- media and creator programs;
- physical events and marketing;
- hosting subsidies.

The key change is administrative delegation. Rather than voting on every small payment, POLIS holders approve a bounded program and the Council administers applications, milestones, and disbursements.

### Phase 4 — Governance as operational continuity: PIP-25 to PIP-33

The later corpus responds to organizational and market pressure:

- Council and DAO Caster elections maintain governance capacity.
- PIP-28 supports a displaced ATMTA contributor.
- PIP-30 preserves community infrastructure until C4.
- PIP-33 reimburses ATMTA for historic DAO obligations and explicitly links the payment to company runway.

The DAO is no longer only funding ecosystem growth; it is also functioning as a continuity and resilience mechanism for the wider Star Atlas institution.

## Treasury doctrine derived from the corpus

### Funding sources

Two funding channels must be distinguished:

- **Ecosystem Fund:** bounded community development funding under PIP-23.
- **DAO Treasury:** extraordinary or institutional obligations outside normal Ecosystem Fund limits, as in PIP-28 and PIP-33.

### Ecosystem Fund rules after PIP-23

- Target allocation: 20% of combined eligible treasury assets.
- USDC allocation applies only to the amount above the $500,000 reserve threshold.
- Ecosystem Fund requests are denominated in USDC but paid in ATLAS.
- A proposal may not exceed 5% of the fund's balance after its latest refill.
- A funded proposal may not run longer than 12 months.
- The Council stewards proposals, implementation tracking, and payments but does not execute refills, perform KYC/KYB, authorize legal contracts, or approve PIPs before the vote.

### Recurring accountability patterns

Later PIPs increasingly rely on:

- dedicated Squads multisigs;
- milestone-based payments;
- post-event or monthly reports;
- unused-fund return clauses;
- Council verification;
- public wallets and transaction evidence;
- recusal for Council conflicts;
- pilot periods before renewal;
- separate follow-on PIPs for expansion.

These should become reusable canonical governance patterns in the user-level database.

## Institutional tensions and policy signals

### Foundation discretion versus DAO sovereignty

The DAO has voting authority, but the Foundation retains important gatekeeping and implementation discretion. This is not fully autonomous governance; it is a legally mediated DAO model.

### Council influence without formal sovereignty

The Council does not replace the DAO, yet its practical authority grows substantially through program administration, proposal review, milestone confirmation, and payment recommendations. The Council should be modeled as an **administrative governance body**, not a legislative chamber.

### Public funding versus private ownership

Several approved PIPs fund privately owned products or media while providing public benefit, sponsorship credit, revenue sharing, or ecosystem access. Examples include THEO, Ryden Systems, Star Seekers 2, and creator/media initiatives. The corpus does not impose a single ownership doctrine; voters judge each bargain independently.

### Community infrastructure as a public good

Approvals for Ryden Systems, Rogue Data Hub, SLY hosting, ATOM Cloud, and the Relay Program show a recurring doctrine: the DAO may subsidize tools that reduce player friction or replace missing shared infrastructure.

### Selectivity in media and creator spending

The DAO approved PIP-17, PIP-20, PIP-29, and PIP-32, but rejected PIP-26 and the privately operated meetup platform in PIP-15. This suggests that voters prefer bounded, measurable, community-distributed programs over broad creator compensation or privately controlled platforms without sufficiently persuasive accountability.

## Canonical promotion recommendations

A subsequent knowledge-promotion campaign should create or substantially expand:

1. `knowledge/governance/Star-Atlas-DAO.md`
   - constitutional principles;
   - DAO scope and limits;
   - PIP lifecycle;
   - PVP voting;
   - relationship to Foundation and Council.

2. `knowledge/governance/Star-Atlas-Foundation.md`
   - Cayman entity role;
   - legal and implementation authority;
   - treasury and multisig responsibility;
   - discretion and transparency obligations.

3. `knowledge/governance/Star-Atlas-Council.md`
   - creation, terms, elections, overlap, administrative powers;
   - Term 1–3 chronology;
   - unresolved election-result gaps.

4. `knowledge/economy/Ecosystem-Fund.md`
   - PIP-4 origin;
   - PIP-23 replacement;
   - refill formula, wallets, cap, duration, payment denomination;
   - funded-program registry.

5. `knowledge/governance/PIP-Registry.md`
   - all 33 proposals;
   - category, author, dates, result, dependencies, supersession, implementation evidence.

6. `knowledge/governance/Governance-Programs.md`
   - Iris's Bounty programs;
   - DAO Casters;
   - Council elections;
   - recurring program governance patterns.

7. `knowledge/timeline/`
   - proposal publication and vote completion dates;
   - Council election terms;
   - PIP-4/PIP-23 fund milestones;
   - only implementation events supported by independent evidence.

## Required graph relationships after promotion

Examples of reviewed candidate relationships:

- `STAR_ATLAS_DAO GOVERNED_BY POLIS_HOLDERS`
- `STAR_ATLAS_FOUNDATION IMPLEMENTS DECISIONS_OF STAR_ATLAS_DAO`
- `STAR_ATLAS_FOUNDATION CUSTODIAN_OF DAO_TREASURY`
- `STAR_ATLAS_COUNCIL ADMINISTERS PIP_PROCESS`
- `PIP_23 SUPERSEDES PIP_4`
- `PIP_10 MODIFIES PIP_3`
- `PIP_13 ATTEMPTS_TO_MODIFY PIP_10` with result `FAILED`
- `PIP_20 ESTABLISHES DAO_CASTERS_PROGRAM`
- `PIP_27 ELECTS_MEMBERS_OF DAO_CASTERS_PROGRAM`
- `PIP_22 ESTABLISHES IRIS_BOUNTY_ARENA`
- `PIP_12 ESTABLISHES IRIS_BOUNTY_FEAST`
- `PIP_33 BENEFICIARY ATMTA`

Graph facts must be generated only after canonical promotion and evidence review.

## Research and reconciliation gaps

1. **Council Election #2 winners:** PIP-11 capture lacks a conclusive election result.
2. **Council Election #3 winners:** PIP-25 capture lacks a conclusive election result.
3. **DAO Caster Term 1 winners:** PIP-27 capture lacks a conclusive election result.
4. **Implementation evidence:** proposal payloads do not independently prove execution for most passed PIPs.
5. **PIP-1 quorum language:** the original text mentions quorum, while current operating guidance supplied by the repository owner defines completed binary results by YES-versus-NO comparison. Preserve both as historical text and current operating rule rather than silently rewriting PIP-1.
6. **Portal lifecycle status:** stale status values should be stored as portal metadata, not canonical result state.
7. **Supersession:** PIP-23 explicitly replaces PIP-4; PIP-10 modifies and extends PIP-3; failed PIP-13 does not modify PIP-10.
8. **Funding implementation:** payment transactions, multisig records, deliverable reports, and program pages should be ingested as separate execution evidence.

## Final disposition

The PIP corpus is sufficiently complete to support a major governance knowledge-promotion campaign.

The highest-confidence canonical conclusions are:

- the constitutional roles of the DAO, Foundation, and Council;
- the PIP lifecycle and voting model;
- the origin and current rules of the Ecosystem Fund;
- proposal outcomes based on official vote data;
- formal supersession and dependency relationships;
- the evolution from constitutional formation to programmatic funding and institutional continuity.

Implementation claims remain separate and require transaction, report, deployment, or other primary evidence.