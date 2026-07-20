---
title: "Organization and Role Registry"
seo_title: "Star Atlas Organization and Role Registry"
seo_description: "A structured registry of Star Atlas institutions, offices, delegated roles, identity boundaries, and unresolved leadership history."
knowledge_status: QUALIFIED
as_of: 2026-07-20
confidence: HIGH
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-01-BC8475E4.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-02-1E2D7066.json"
  - "archive/source-records/social-governance-semantic-enrichment/governance/SRC-PIP-03-F5E7CDE1.json"
  - "knowledge/index/Entity-Registry.md"
known_limitations:
  - "The repository does not yet contain a complete corporate, Foundation-officer, Council, or staff role chronology."
  - "Current titles are not inferred from historical event appearances or undated profile language."
research_gaps:
  - "Acquire corporate filings, Foundation officer/director records, later Council winner rosters, role start/end notices, and delegation instruments."
review_after: 2027-01-17
---

# Organization and Role Registry

An organization is not the same thing as the people who serve it, the office they hold, or the authority delegated to them. This registry keeps those layers separate. It complements the [Entity Registry](../index/Entity-Registry.md): the Entity Registry supplies stable identities, while this page records institutional roles, authority boundaries, and what remains unknown about their chronology.

## Core institutional entities

| Entity | Type | Supported role | Authority boundary | Current-state qualification |
|---|---|---|---|---|
| [ATMTA, Inc.](ATMTA.md) | Operating company | Product developer/operator and official publisher associated with Star Atlas | Not the DAO electorate, Foundation, or Council | Corporate structure and full leadership chronology incomplete. |
| Star Atlas brand/ecosystem | Public identity/ecosystem | Umbrella for products, lore, communications, and institutions | Not a legal entity inferred by this archive | Use only where a narrower publisher or institution is unavailable. |
| [Star Atlas DAO](../governance/Star-Atlas-DAO.md) | Governance system/electorate | Locked-POLIS, PVP-weighted proposal voting | Passage does not execute code, transfer funds, or prove outcome | Formal charter captured in PIP-1; current participation distribution unresolved. |
| [Star Atlas Foundation](../governance/Star-Atlas-Foundation.md) | Legal/administrative body | Governance administration, legal/compliance mediation, and safe/lawful implementation within captured rules | Not an independent legislature; may decline unsafe implementation under stated conditions | Current officers, signers, and delegated duties require dated records. |
| [Star Atlas Council](../governance/Star-Atlas-Council.md) | Elected governance-process steward | Author assistance, process operations, delegated program administration, and Council-authored assessments | Not a sovereign legislature; tracker assessments are not independent verification | Only first elected roster is resolved in archive. |
| Ecosystem Fund | Bounded treasury mechanism and wallet | Finances eligible passed proposals under controlling policy | Not the entire DAO Treasury or a separate organization | PIP-23 controls captured policy as of review date. |

## From institution to action

Institutional history becomes clearer when an action is followed through the role chain rather than assigned to the broad Star Atlas brand. A person or organization may author a proposal; voters may approve it; the Foundation may administer it; the Council may perform a delegated assessment; ATMTA or another operator may implement a product change; and a recipient may later receive payment. Evidence for one step does not prove the others.

## Constitutional role chain

| Role | Holder type | Evidence of role | What must remain separate |
|---|---|---|---|
| Proposal author | Person or organization | Named in a PIP | Authorship is not approval. |
| POLIS voter | Address/controller with locked POLIS/PVP | Vote record | Address does not establish personal identity. |
| Foundation administrator | Institutional body/delegate | PIP-1/PIP-2 and later operational record | Administration is not voter sovereignty. |
| Council steward | Elected individual acting through Council | Election result plus service evidence | Election is not proof of uninterrupted current service. |
| Program recipient | Person/organization named by funding PIP | Proposal and recipient record | Authorization is not payment or completion. |
| Product developer/operator | ATMTA or another evidenced organization | First-party publication, repository, contract, or corporate record | Brand association alone is insufficient. |
| Publisher/replay publisher | Publication, account, or channel | Source metadata | Republishing does not transfer original authorship. |

## Council roster states

PIP-6 identifies twelve first-round advancing candidates and must not be treated as the elected roster. PIP-7 identifies the first final Council members: `jp`, `funcracker`, `king_bryan`, `bodhi_tree`, and `drumcarl05`. Later election PIPs 11 and 25 have unresolved winner identity in the captured archive. [Council Election History](../governance/Council-Election-History.md)

The registry therefore uses:

- `ELECTED_FIRST_TERM` for the PIP-7 final roster, without claiming present service;
- `ADVANCED_NOT_ELECTED_BY_THIS_STAGE` for PIP-6-only candidates;
- `WINNER_IDENTITY_UNRESOLVED` for PIP-11 and PIP-25;
- `CURRENT_ROLE_UNKNOWN` where no dated service evidence exists.

## Identity collision controls

- Star Atlas Council is not the lore Council of Peace.
- It is not the Ustur Security Council or Dark Matter's "Dark Council."
- Hologram News Network, The Hologram, and Kr1gs are distinct publication/brand/person identities.
- Town Hall and Atlas Brew are distinct event formats.
- Star Atlas TV/VBTV can be a replay publisher without originating an event.
- ATMTA publication does not merge ATMTA with the Foundation, DAO, or Council.

## Role-ledger schema for future records

Each role entry should preserve `organization_id`, `actor_id`, source-native title, normalized role, role state, start and end values with precision, source IDs, authority class, conflict notes, and `as_of`. Historical, intended, elected, appointed, acting, departed, and current states must not be collapsed.

## Missing artifacts

Priority acquisitions include ATMTA corporate filings and ownership history, Foundation incorporation and current officers, multisig signer records, Council seating/resignation/replacement notices, election 2/3 results, staff appointment/departure announcements, formal delegation instruments, and original publisher/replay metadata for recurring events.

## Related knowledge

- [Star Atlas Institutional Overview](Institutional-Overview.md)
- [Actor Master Index](../people/Actor-Master-Index.md)
- [Guild and DAC Master Index](../guilds/Guild-Master-Index.md)
- [Governance Implementation and Evidence States](../governance/Governance-Implementation-and-Evidence-States.md)

## Review status

`QUALIFIED`. Core institutional boundaries are high confidence; individual and current role chronology is incomplete.
