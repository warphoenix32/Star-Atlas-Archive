---
title: "Canonical PIP and Governance Ledger"
knowledge_status: QUALIFIED
as_of: 2026-07-18
confidence: MEDIUM
page_risk_score: 7
page_risk_class: R3
ledger_status: DRAFT_FOR_REVIEW
review_status: HUMAN_REVIEW_REQUIRED
evidence_basis:
  - "archive/raw/social-governance-semantic-enrichment/governance/pip-captures/"
  - "archive/semantic/governance/pip-registry-semantic.json"
  - "archive/semantic/governance/pip-source-reconciliation.json"
  - "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"
known_limitations:
  - "Election candidate-level PVP is absent from the preserved portal captures."
  - "Council payment and implementation fields are attributed and are not independently verified."
  - "No on-chain treasury verification was performed because the required dataset was not supplied."
research_gaps:
  - "Official winner records remain missing for PIP-11, PIP-25, and PIP-27."
  - "Transaction and deliverable evidence remains incomplete."
review_after: 2026-10-18
---

# Canonical PIP and Governance Ledger

This draft ledger reconciles the 33 numbered official portal captures available in the repository. It is canonical in scope—one record per PIP from PIP-1 through PIP-33—but remains `QUALIFIED` and `DRAFT_FOR_REVIEW` until human approval. It does not rewrite any source record.

The machine-readable companion is [PIP-Registry.json](PIP-Registry.json). Conflicts and required follow-up evidence are maintained under the [ledger campaign](../../operations/campaigns/canonical-pip-governance-ledger-2026-07/README.md).

## Interpretation policy

- Proposal publication, voting, result, authorization, payment, implementation, and independent verification are separate states.
- Completed binary results use an **owner-approved repository editorial adjudication**: YES PVP greater than NO PVP is reviewed as passed; otherwise failed. This rule is not asserted as text contained in PIP-1. Abstentions remain visible and non-decisive.
- Ranked-choice elections never use binary fields. The preserved captures contain only aggregate election ballots/PVP. Candidate-level PVP is explicitly missing for PIP-6, PIP-7, PIP-11, PIP-25, and PIP-27.
- PIP-6 names first-round advancing candidates; PIP-7 names final elected officeholders. PIP-11, PIP-25, and PIP-27 preserve Council-reported passage while winner identity remains unresolved.
- Council tracker milestone, payment, termination, cancellation, withdrawal, and ROI fields are Council-authored operational assessments. They are not independent verification.
- No on-chain payment verification is performed or implied. Treasury state values are restricted to `REQUESTED`, `AUTHORIZED`, `COUNCIL_REPORTED`, `UNVERIFIED`, `MISSING_ONCHAIN_EVIDENCE`, or null when not applicable.

## Ledger

Vote entries use `ballots / PVP`. Full-text links point to immutable raw portal captures.

| PIP | Title / author / category | Publication and vote window | Mechanism and vote evidence | Result and authorization | Implementation and payment | Reconciliation | Full text |
|---|---|---|---|---|---|---|---|
| PIP-01 | Star Atlas DAO<br>The Star Atlas Foundation<br>PROCESS | published 2024-07-08T17:20:59.959Z<br>vote 2024-07-10T16:00:00.000Z to 2024-07-23T16:00:00.000Z | YES 782 / 118466246.60769610459579546; NO 101 / 50624407.96816817681977; abstain 11 / 6267862.71859572403818; total PVP 175358517.29446000545374546 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-01-bc8475e4-0525-4fba-b4f8-b848ccde7a9d.json) |
| PIP-02 | Star Atlas Foundation<br>The Star Atlas Foundation<br>PROCESS | published 2024-07-08T17:21:02.359Z<br>vote 2024-07-10T16:00:00.000Z to 2024-07-23T16:00:00.000Z | YES 674 / 99759835.192889974963643; NO 151 / 69015468.838133753132146; abstain 27 / 7292070.45769785662487; total PVP 176067374.488721584720659 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment UNVERIFIED<br>on-chain UNVERIFIED | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>1 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-02-1e2d7066-ec44-46e0-945f-b2e56b1e61b0.json) |
| PIP-03 | Star Atlas Council<br>The Star Atlas Foundation<br>FUNDING | published 2024-07-08T17:21:04.293Z<br>vote 2024-07-24T16:00:00.000Z to 2024-08-06T16:00:00.000Z | YES 461 / 84678191.7025254745560149; NO 13 / 12482711.012724072681; abstain 5 / 164557.6936920700218; total PVP 97325460.4089416172588149 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment UNVERIFIED<br>on-chain UNVERIFIED | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>1 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-03-f5e7cde1-9a02-4670-ae40-1c932a4b8dad.json) |
| PIP-04 | Star Atlas Ecosystem Fund<br>The Star Atlas Foundation<br>FUNDING | published 2024-07-08T17:21:06.160Z<br>vote 2024-07-24T16:00:00.000Z to 2024-08-06T16:00:00.000Z | YES 421 / 81843902.5128978026084949; NO 33 / 14242581.31620796885365; abstain 6 / 203935.9438189091918; total PVP 96290419.7729246806539449 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment UNVERIFIED<br>on-chain UNVERIFIED | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>1 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-04-ad1945d8-60dc-4ed7-b52a-63dd33f97415.json) |
| PIP-05 | Co-Sponsor the Naabathon<br>The Star Atlas Foundation<br>FUNDING | published 2024-07-26T09:14:17.852Z<br>vote 2024-07-26T16:00:00.000Z to 2024-08-09T16:00:00.000Z | YES 333 / 80521366.4547641016774636; NO 69 / 19930351.43958932936537; abstain 9 / 740849.600510022811696; total PVP 101192567.4948634538545296 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-05-c248d280-15fb-4071-ba5d-2afaa6e1af41.json) |
| PIP-06 | Council Election #1 - First Round<br>unresolved identity; public key BVJESvrDeXZcSX5UVdK2Tt57Lur9gyakgCfdX45pVQ1V<br>COUNCIL | published 2024-08-23T13:33:50.299Z<br>vote 2024-09-14T16:00:00.000Z to 2024-09-21T05:00:00.000Z | RCV aggregate 587 ballots / 161327889.08397183 PVP; 22 candidates; candidate PVP missing | FIRST_ROUND_ADVANCEMENT_RECORDED<br>NOT_APPLICABLE_ELECTION | NOT_APPLICABLE_ELECTION<br>independent implementation verification NOT_APPLICABLE_ELECTION<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-06-1b792551-83e1-4998-99a4-6637caa69df8.json) |
| PIP-07 | Council Election #1 - Second Round<br>unresolved identity; public key BVJESvrDeXZcSX5UVdK2Tt57Lur9gyakgCfdX45pVQ1V<br>COUNCIL | published 2024-09-26T12:01:36.608Z<br>vote 2024-09-27T16:00:00.000Z to 2024-10-11T16:00:00.000Z | RCV aggregate 575 ballots / 174532321.58451426 PVP; 12 candidates; candidate PVP missing | ELECTED_OFFICEHOLDERS_RECORDED<br>NOT_APPLICABLE_ELECTION | NOT_APPLICABLE_ELECTION<br>independent implementation verification NOT_APPLICABLE_ELECTION<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-07-91652743-f916-4566-99af-421a557f7c3d.json) |
| PIP-08 | Star Atlas Comet: Community Meetup at Gamescom 2025<br>Shaddix, VB, Kiwimi<br>FUNDING | published 2025-02-19T18:21:12.823Z<br>vote 2025-02-19T23:59:59.999Z to 2025-02-26T23:59:59.999Z | YES 228 / 72275594.601401963230528; NO 54 / 12007878.97275774668268; abstain 3 / 455574.89674787142; total PVP 84739048.470907581333208 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-08-62506041-933e-4b3e-a450-a2596c15a801.json) |
| PIP-09 | Adjust STV Backup Vote Handling to Prevent Unintended Vote Redistribution<br>Funcracker<br>DAO | published 2025-02-26T12:12:27.813Z<br>vote 2025-02-27T23:59:59.999Z to 2025-03-06T23:59:59.999Z | YES 124 / 60315831.190417026347813; NO 3 / 433700.540831377589; abstain not captured; total PVP 60749531.731248403936813 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>1 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-09-1cc4bb6f-269b-46fa-b60b-a17f01b41ffa.json) |
| PIP-10 | Star Atlas Council: Second Term & Beyond<br>DAO Council (1st Term)<br>COUNCIL | published 2025-02-26T12:12:30.590Z<br>vote 2025-02-27T23:59:59.999Z to 2025-03-13T23:59:59.999Z | YES 209 / 84997000.833444787727335; NO 1 / 786061.9883146426; abstain 1 / 249133.7265861902; total PVP 86032196.548345620527335 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>1 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-10-ed887a4e-344e-44d6-8a47-c815d9e8ec8e.json) |
| PIP-11 | Council Election #2<br>unresolved identity; public key BVJESvrDeXZcSX5UVdK2Tt57Lur9gyakgCfdX45pVQ1V<br>COUNCIL | published 2025-03-21T16:02:25.537Z<br>vote 2025-03-23T23:59:59.999Z to 2025-04-06T23:59:59.999Z | RCV aggregate 348 ballots / 150046997.08184665 PVP; 7 candidates; candidate PVP missing | COUNCIL_REPORTED_PASSAGE_WINNERS_UNRESOLVED<br>NOT_APPLICABLE_ELECTION | NOT_APPLICABLE_ELECTION<br>independent implementation verification NOT_APPLICABLE_ELECTION<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED_WITH_UNRESOLVED_WINNER<br>3 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-11-7b48a62d-13c3-4a1e-8565-6ea7bfb4b4dc.json) |
| PIP-12 | Iris’s Bounty: The Feast<br>DAO Council (1st Term)<br>FUNDING | published 2025-04-11T13:07:47.033Z<br>vote 2025-04-13T23:59:59.999Z to 2025-04-27T23:59:59.999Z | YES 87 / 55090441.7203514144207; NO 50 / 16325703.81751238282035; abstain 6 / 12866654.63466089975274; total PVP 84282800.17252469699379 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-12-f15380c9-8d3f-4849-8185-c29f4c72e961.json) |
| PIP-13 | Implementing Term Limits for Star Atlas DAO Council Members<br>Bohemian<br>DAO, COUNCIL | published 2025-04-11T13:07:52.103Z<br>vote 2025-04-14T23:59:59.999Z to 2025-04-28T23:59:59.999Z | YES 83 / 23247451.44933094120451; NO 57 / 58144044.192175563558886; abstain 21 / 3519692.3295073641949; total PVP 84911187.971013868958296 | FAILED<br>NOT_AUTHORIZED | NOT_APPLICABLE_NO_AUTHORIZATION<br>independent implementation verification NOT_APPLICABLE_NO_AUTHORIZATION<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-13-b721d8e7-9ca1-4a85-b627-472c108b3acb.json) |
| PIP-14 | Deepening THEO Integration into the Star Atlas Economy<br>Dr. John Ennis, CEO of Tulle (https://tulle.ai/)<br>FUNDING | published 2025-04-15T08:06:25.670Z<br>vote 2025-04-16T23:59:59.999Z to 2025-04-30T23:59:59.999Z | YES 141 / 100079948.791721847185027; NO 28 / 7476976.93945939219146; abstain 7 / 462089.7904602649105; total PVP 108019015.521641504286987 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_TERMINATED<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-14-fed98016-e7b6-4a5b-8120-4f0ec90cfa77.json) |
| PIP-15 | In-Person Community Meetups Platform<br>Matt (Intergalactic Herald)<br>FUNDING | published 2025-05-07T19:50:27.545Z<br>vote 2025-05-08T23:59:59.999Z to 2025-05-22T23:59:59.999Z | YES 46 / 38791006.98713182319328; NO 102 / 62013412.28960679431876; abstain 13 / 2909806.64480605553269; total PVP 103714225.92154467304473 | FAILED<br>NOT_AUTHORIZED | NOT_APPLICABLE_NO_AUTHORIZATION<br>independent implementation verification NOT_APPLICABLE_NO_AUTHORIZATION<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-15-bd065ad2-5e75-4e47-a696-a1efe06382da.json) |
| PIP-16 | Ryden Systems<br>Developed by “Risingson”<br>FUNDING | published 2025-05-07T19:50:30.679Z<br>vote 2025-05-08T23:59:59.999Z to 2025-05-22T23:59:59.999Z | YES 167 / 81056806.2882333337242; NO 21 / 6979915.86406552204061; abstain 14 / 18804169.14759858997284256; total PVP 106840891.29989744573765256 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-16-b11ced4b-a6a5-4211-a0e6-060eadc4bd22.json) |
| PIP-17 | Star Atlas Ecosystem Media Expansion<br>LordRaspyIII<br>FUNDING | published 2025-05-23T20:32:15.279Z<br>vote 2025-05-29T23:59:59.999Z to 2025-06-12T23:59:59.999Z | YES 120 / 67357600.78706531183462; NO 70 / 43163339.0227892540245; abstain 4 / 606649.965859209597; total PVP 111127589.77571377545612 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_CANCELED<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-17-4df4c199-e888-4fdc-a666-7f82d6cf2de7.json) |
| PIP-18 | Marketing & Merch Expansion for Gamescom 2025<br>Kiwimi, VB, Shaddix<br>FUNDING | published 2025-07-03T14:38:14.743Z<br>vote 2025-07-03T23:59:59.999Z to 2025-07-17T23:59:59.999Z | YES 98 / 40993696.92844893998568; NO 14 / 11339350.4512077565853; abstain 4 / 2209311.33068470117; total PVP 54542358.71034139774098 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-18-18750a6a-f36d-44ba-990a-07769c5c589b.json) |
| PIP-19 | Funding Independent Economic Research and Maintenance of Critical Data Resources<br>Steven Sabol<br>FUNDING | published 2025-09-20T07:31:38.204Z<br>vote 2025-09-21T23:59:59.999Z to 2025-10-05T23:59:59.999Z | YES 43 / 59388884.17306768517726; NO 105 / 83100564.474068210577573; abstain 9 / 1050954.3007301348069; total PVP 143540402.947866030561733 | FAILED<br>NOT_AUTHORIZED | NOT_APPLICABLE_NO_AUTHORIZATION<br>independent implementation verification NOT_APPLICABLE_NO_AUTHORIZATION<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-19-1eb3d15e-645e-4c34-8a69-00d304ecfc4f.json) |
| PIP-20 | Establishment of the DAO Casters Program — Elected Content Creators for Star Atlas Ecosystem Promotion<br>Signal<br>FUNDING | published 2025-09-29T18:37:48.441Z<br>vote 2025-10-01T23:59:59.999Z to 2025-10-15T23:59:59.999Z | YES 111 / 106030687.38355558354421; NO 32 / 15940622.26160213707314; abstain 7 / 516503.5315026251029; total PVP 122487813.17666034572025 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_PARTIAL_OR_IN_PROGRESS<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-20-159cb743-f8cf-4932-8e01-e6f1a0b479ff.json) |
| PIP-21 | Rogue Data Hub<br>Lorddo, Solwalker<br>FUNDING | published 2025-09-29T18:37:50.635Z<br>vote 2025-10-01T23:59:59.999Z to 2025-10-15T23:59:59.999Z | YES 124 / 76880541.93730371407713; NO 56 / 55012100.13793423692155; abstain 4 / 14689624.66066018158; total PVP 146582266.73589813257868 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_PARTIAL_OR_IN_PROGRESS<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-21-49cad7e4-f467-4c88-978a-e3cac1633cf1.json) |
| PIP-22 | Iris Bounty - The Arena<br>King Bryan, Santi, Signal<br>FUNDING | published 2025-11-03T14:48:11.104Z<br>vote 2025-11-04T23:59:59.999Z to 2025-11-18T23:59:59.999Z | YES 98 / 137797850.987275790285793; NO 9 / 2670497.9552498631134; abstain 2 / 392044.78070359304; total PVP 140860393.723229246439193 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_PARTIAL_OR_IN_PROGRESS<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-22-d5d61e64-5489-4530-93a5-b65bf1bf8079.json) |
| PIP-23 | Refresh of PIP-4 the Ecosystem Fund<br>the Star Atlas Council #2 (SAC-2): Lanzer, Bodhi, Signal, Emperor, DrumCarl05<br>FUNDING | published 2025-11-03T14:48:14.351Z<br>vote 2025-11-04T23:59:59.999Z to 2025-11-18T23:59:59.999Z | YES 77 / 86030422.02705529060743; NO 34 / 24262645.413694593485593; abstain 6 / 792710.919943480742; total PVP 111085778.360693364835023 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment UNVERIFIED<br>on-chain UNVERIFIED | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>1 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-23-0ecf2928-15df-497e-8b67-d87eda030d5a.json) |
| PIP-24 | DAO-Supported Hosting Service for SLY Assistant<br>Arty<br>FUNDING | published 2025-11-07T11:03:44.775Z<br>vote 2025-11-08T23:59:59.999Z to 2025-11-22T23:59:59.999Z | YES 79 / 64002012.602125027599097; NO 55 / 43346187.830609256463269; abstain 6 / 1036464.8531316944778; total PVP 108384665.285865978540166 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_MILESTONES_COMPLETE<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment UNVERIFIED<br>on-chain UNVERIFIED | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>1 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-24-8cc6b298-2708-40c6-9b9d-867f0cba8ea5.json) |
| PIP-25 | Council Election #3<br>unresolved identity; public key BVJESvrDeXZcSX5UVdK2Tt57Lur9gyakgCfdX45pVQ1V<br>COUNCIL | published 2025-11-26T09:14:38.127Z<br>vote 2025-11-26T23:59:59.999Z to 2025-12-10T23:59:59.999Z | RCV aggregate 176 ballots / 111777631.5099522 PVP; 6 candidates; candidate PVP missing | COUNCIL_REPORTED_PASSAGE_WINNERS_UNRESOLVED<br>NOT_APPLICABLE_ELECTION | NOT_APPLICABLE_ELECTION<br>independent implementation verification NOT_APPLICABLE_ELECTION<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED_WITH_UNRESOLVED_WINNER<br>4 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-25-91cc73fa-0af7-41ea-86c5-bab7ffcfcb4f.json) |
| PIP-26 | Star Atlas Crew Adventure Series – Season Production <br>Hammerhead<br>FUNDING | published 2026-01-20T14:35:51.298Z<br>vote 2026-01-22T23:59:59.999Z to 2026-02-05T23:59:59.999Z | YES 49 / 50845898.39810709547066; NO 90 / 87903394.3874796963789652; abstain 8 / 28396587.00898292271; total PVP 167145879.7945697145596252 | FAILED<br>NOT_AUTHORIZED | NOT_APPLICABLE_NO_AUTHORIZATION<br>independent implementation verification NOT_APPLICABLE_NO_AUTHORIZATION<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-26-b70ac545-6c01-486d-b943-dee434d9abf3.json) |
| PIP-27 | DAO Casters Election: Term 1<br>Star Atlas DAO Council (SAC-3)<br>GOVERNANCE | published 2026-02-18T19:56:54.221Z<br>vote 2026-02-20T23:59:59.999Z to 2026-03-06T23:59:59.999Z | RCV aggregate 128 ballots / 146708785.8400328 PVP; 13 candidates; candidate PVP missing | COUNCIL_REPORTED_PASSAGE_WINNERS_UNRESOLVED<br>NOT_APPLICABLE_ELECTION | NOT_APPLICABLE_ELECTION<br>independent implementation verification NOT_APPLICABLE_ELECTION<br>payment not applicable<br>on-chain not applicable | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED_WITH_UNRESOLVED_WINNER<br>5 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-27-064d252c-be76-494a-8f19-f650c2a3dab6.json) |
| PIP-28 | Temporary DAO Funding to Preserve Core Lore, Design, and Community Functions<br>José - Noot<br>FUNDING | published 2026-02-18T19:57:07.999Z<br>vote 2026-02-20T23:59:59.999Z to 2026-03-06T23:59:59.999Z | YES 113 / 132748518.60220010378223; NO 26 / 8344270.1804614863808; abstain 6 / 2121225.55133310946; total PVP 143214014.33399469962303 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_PARTIAL_OR_IN_PROGRESS<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment UNVERIFIED<br>on-chain UNVERIFIED | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>1 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-28-d0a5dc75-4e1c-4a70-a8af-a5f3636d0139.json) |
| PIP-29 | Star Atlas Relay Program (Pilot)<br>Funcracker (Star Atlas community member; liaison to Aephia Industries)<br>FUNDING | published 2026-03-16T15:16:39.390Z<br>vote 2026-03-18T23:59:59.999Z to 2026-04-01T23:59:59.999Z | YES 90 / 156894218.6758377942159; NO 13 / 4778188.438956892994; abstain 2 / 1002028.05157705216; total PVP 162674435.1663717393699 | PASSED<br>AUTHORIZED | IMPLEMENTATION_UNVERIFIED<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-29-8e761702-ee81-4509-b627-9cadb5897c1b.json) |
| PIP-30 | ATOM Cloud Infrastructure Sustainability — DAO Funding Pilot<br>Sim (Star Atlas community member; ATOM team member)<br>FUNDING | published 2026-03-16T15:16:41.119Z<br>vote 2026-03-18T23:59:59.999Z to 2026-04-01T23:59:59.999Z | YES 147 / 111241682.08665644280279; NO 55 / 70230624.8482863139085; abstain 3 / 1284009.94459085913; total PVP 182756316.87953361584129 | PASSED<br>AUTHORIZED | IMPLEMENTATION_UNVERIFIED<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment COUNCIL_REPORTED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>2 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-30-3ba029f2-65e8-4637-b6ad-ae86284ff714.json) |
| PIP-31 | Star Seekers 2 — Mobile Game DAO Funding Proposal<br>PG Metaverse OG<br>FUNDING | published 2026-04-15T21:30:20.572Z<br>vote 2026-04-17T23:59:59.999Z to 2026-05-01T23:59:59.999Z | YES 66 / 53854461.85725857028707; NO 64 / 46566240.1818730930898; abstain 11 / 34127227.0874592923208; total PVP 134547929.12659095569767 | PASSED<br>AUTHORIZED | COUNCIL_REPORTED_WITHDRAWN_AFTER_PASSAGE_NOT_IMPLEMENTED<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment UNVERIFIED<br>on-chain UNVERIFIED | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>1 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-31-e71fb1a7-6d19-4565-8ff8-b4e79a3f8c16.json) |
| PIP-32 | Igniting the Star Atlas Triad Tournament - A Super Phoenix Sports Live Esports Event<br>Money, Lanzer, Njord<br>FUNDING | published 2026-05-26T02:15:05.244Z<br>vote 2026-05-28T23:59:59.999Z to 2026-06-11T23:59:59.999Z | YES 90 / 88329391.65101292166224; NO 21 / 13539439.5083802807377; abstain 7 / 17343533.14818180349; total PVP 119212364.30757500588994 | PASSED<br>AUTHORIZED | IMPLEMENTATION_UNVERIFIED<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment UNVERIFIED<br>on-chain UNVERIFIED | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>1 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-32-0b04ff9b-ff04-45f5-a458-696fea70eda2.json) |
| PIP-33 | ATMTA Historic Expense Reimbursement<br>Michael Wagner, on behalf of ATMTA, Inc.<br>FUNDING | published 2026-06-24T22:02:13.644Z<br>vote 2026-06-26T23:59:59.999Z to 2026-07-10T23:59:59.999Z | YES 141 / 170240400.01173955829543; NO 59 / 24857540.3494159807778; abstain 20 / 83860459.549096303435; total PVP 278958399.91025184250823 | PASSED<br>AUTHORIZED | IMPLEMENTATION_UNVERIFIED<br>independent implementation verification MISSING_INDEPENDENT_PRIMARY_EVIDENCE<br>payment UNVERIFIED<br>on-chain MISSING_ONCHAIN_EVIDENCE | OPEN_DOCUMENTED_CONFLICTS<br>vote/result: RECONCILED<br>5 documented conflict links | [raw capture](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-33-397fee39-fd7c-42be-89e3-169094138257.json) |

## Election detail

### PIP-06 — Council Election #1 - First Round

- Stage: `FIRST_ROUND`
- Outcome: `ADVANCEMENT_TO_FINAL_ROUND`
- Aggregate: 587 ballots / 161327889.08397183 PVP
- Configured winners: 12; maximum choices: 22; candidates: 22
- Winner identification: `IDENTIFIED`
- Candidate totals: `MISSING_FROM_CAPTURE`; every candidate PVP field remains null.

| Candidate ID | Display name | Outcome | Candidate PVP |
|---|---|---|---|
| rome_i_emperor | ROME I Emperor | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| jith_blade | Jith Blade | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| drumcarl05 | DRUMCARL05 | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| notcatz | Notcatz | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| bolerzwam | bolerZwam | NOT_SELECTED | MISSING_FROM_CAPTURE |
| krigs | Krigs | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| dmark | Dmark | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| jp | JP | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| bodhi_tree | Bodhi [TREE] | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| kucheto | Kucheto | NOT_SELECTED | MISSING_FROM_CAPTURE |
| xalexus | xAlexus | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| sawyn | 🆂🅰🆆🆈🅽 | NOT_SELECTED | MISSING_FROM_CAPTURE |
| king_bryan | King Bryan | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| folarihn_topboi | Folarihn TopBoi | NOT_SELECTED | MISSING_FROM_CAPTURE |
| sai_kirito | [SAI]Kirito | NOT_SELECTED | MISSING_FROM_CAPTURE |
| z | Z | NOT_SELECTED | MISSING_FROM_CAPTURE |
| dextrin | Dextrin | NOT_SELECTED | MISSING_FROM_CAPTURE |
| sim | Sim | NOT_SELECTED | MISSING_FROM_CAPTURE |
| funcracker | Funcracker | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |
| onigiri0732_91801 | onigiri0732_91801 | NOT_SELECTED | MISSING_FROM_CAPTURE |
| bilal_sous | Bilal Sous | NOT_SELECTED | MISSING_FROM_CAPTURE |
| ajota_lrnr | AJOTA.lrnr | ADVANCED_TO_FINAL_ROUND | MISSING_FROM_CAPTURE |

### PIP-07 — Council Election #1 - Second Round

- Stage: `FINAL_ROUND`
- Outcome: `ELECTED_COUNCIL_MEMBERS`
- Aggregate: 575 ballots / 174532321.58451426 PVP
- Configured winners: 5; maximum choices: 12; candidates: 12
- Winner identification: `IDENTIFIED`
- Candidate totals: `MISSING_FROM_CAPTURE`; every candidate PVP field remains null.

| Candidate ID | Display name | Outcome | Candidate PVP |
|---|---|---|---|
| rome_i_emperor | ROME I Emperor | NOT_SELECTED | MISSING_FROM_CAPTURE |
| jith_blade | Jith Blade | NOT_SELECTED | MISSING_FROM_CAPTURE |
| drumcarl05 | DRUMCARL05 | ELECTED | MISSING_FROM_CAPTURE |
| notcatz | Notcatz | NOT_SELECTED | MISSING_FROM_CAPTURE |
| dmark | Dmark | NOT_SELECTED | MISSING_FROM_CAPTURE |
| jp | JP | ELECTED | MISSING_FROM_CAPTURE |
| bodhi_tree | Bodhi [TREE] | ELECTED | MISSING_FROM_CAPTURE |
| xalexus | xAlexus | NOT_SELECTED | MISSING_FROM_CAPTURE |
| king_bryan | King Bryan | ELECTED | MISSING_FROM_CAPTURE |
| funcracker | Funcracker | ELECTED | MISSING_FROM_CAPTURE |
| ajota_lrnr | AJOTA.lrnr | NOT_SELECTED | MISSING_FROM_CAPTURE |
| krigs | Krigs (dropped out) | NOT_SELECTED | MISSING_FROM_CAPTURE |

### PIP-11 — Council Election #2

- Stage: `SINGLE_ROUND`
- Outcome: `WINNERS_UNRESOLVED`
- Aggregate: 348 ballots / 150046997.08184665 PVP
- Configured winners: 5; maximum choices: 7; candidates: 7
- Winner identification: `UNRESOLVED`
- Candidate totals: `MISSING_FROM_CAPTURE`; every candidate PVP field remains null.

| Candidate ID | Display name | Outcome | Candidate PVP |
|---|---|---|---|
| emperor | Emperor ===[] | UNRESOLVED | MISSING_FROM_CAPTURE |
| drumcarl05 | DRUMCARL05 | UNRESOLVED | MISSING_FROM_CAPTURE |
| jithblade | [EMP] jith blade | UNRESOLVED | MISSING_FROM_CAPTURE |
| bodhitree | bodhitree_ | UNRESOLVED | MISSING_FROM_CAPTURE |
| signal | ROME \| Signal | UNRESOLVED | MISSING_FROM_CAPTURE |
| lanzer | Lanzer | UNRESOLVED | MISSING_FROM_CAPTURE |
| marshalza | [MERC]★★★\|MARSHAL\|★★★[ZA] | UNRESOLVED | MISSING_FROM_CAPTURE |

### PIP-25 — Council Election #3

- Stage: `SINGLE_ROUND`
- Outcome: `WINNERS_UNRESOLVED`
- Aggregate: 176 ballots / 111777631.5099522 PVP
- Configured winners: 5; maximum choices: 6; candidates: 6
- Winner identification: `UNRESOLVED`
- Candidate totals: `MISSING_FROM_CAPTURE`; every candidate PVP field remains null.

| Candidate ID | Display name | Outcome | Candidate PVP |
|---|---|---|---|
| emperor | Emperor ===[] | UNRESOLVED | MISSING_FROM_CAPTURE |
| atlas_freeks | [ECL] YassFreeks | UNRESOLVED | MISSING_FROM_CAPTURE |
| winston | ROME \| Winston | UNRESOLVED | MISSING_FROM_CAPTURE |
| jith_blade | [EMP] jith blade | UNRESOLVED | MISSING_FROM_CAPTURE |
| lanzer | LANZER | UNRESOLVED | MISSING_FROM_CAPTURE |
| morango | Q \| Morangø | UNRESOLVED | MISSING_FROM_CAPTURE |

### PIP-27 — DAO Casters Election: Term 1

- Stage: `SINGLE_ROUND`
- Outcome: `WINNERS_UNRESOLVED`
- Aggregate: 128 ballots / 146708785.8400328 PVP
- Configured winners: 5; maximum choices: 6; candidates: 13
- Winner identification: `UNRESOLVED`
- Candidate totals: `MISSING_FROM_CAPTURE`; every candidate PVP field remains null.

| Candidate ID | Display name | Outcome | Candidate PVP |
|---|---|---|---|
| odvb | ODVB | UNRESOLVED | MISSING_FROM_CAPTURE |
| spikecollects | SpikeCollects | UNRESOLVED | MISSING_FROM_CAPTURE |
| chet_roberts | Chet Roberts | UNRESOLVED | MISSING_FROM_CAPTURE |
| umg_cliper | UMG\| Cliper | UNRESOLVED | MISSING_FROM_CAPTURE |
| morpheus426 | Morpheus426 | UNRESOLVED | MISSING_FROM_CAPTURE |
| winston7026 | Winston7026 | UNRESOLVED | MISSING_FROM_CAPTURE |
| azzarycryptearn | Azzarycryptearn | UNRESOLVED | MISSING_FROM_CAPTURE |
| neon_slika11 | [NEON] Slika11 | UNRESOLVED | MISSING_FROM_CAPTURE |
| a_neo_aarmstrong_ec | [Λ] Neo_AArmstrong [EC] | UNRESOLVED | MISSING_FROM_CAPTURE |
| keplernet | Keplernet | UNRESOLVED | MISSING_FROM_CAPTURE |
| funcracker | Funcracker | UNRESOLVED | MISSING_FROM_CAPTURE |
| sakaleynx | Sakaleynx | UNRESOLVED | MISSING_FROM_CAPTURE |
| alicesarcade | AlicesArcade | UNRESOLVED | MISSING_FROM_CAPTURE |

## Relationships

| From | Relationship | To | Evidence |
|---|---|---|---|
| PIP-6 | ELECTION_FIRST_ROUND_UNDER | PIP-3 | [PIP-06-FULL-TEXT](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-06-1b792551-83e1-4998-99a4-6637caa69df8.json) |
| PIP-7 | ELECTION_FINAL_ROUND_UNDER | PIP-3 | [PIP-07-FULL-TEXT](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-07-91652743-f916-4566-99af-421a557f7c3d.json) |
| PIP-10 | MODIFIES_AND_EXTENDS | PIP-3 | [SRC-PIP-10-ED887A4E](../../archive/semantic/governance/pip-supersession-index.json) |
| PIP-23 | SUPERSEDES | PIP-4 | [SRC-PIP-23-0ECF2928](../../archive/semantic/governance/pip-supersession-index.json) |
| PIP-7 | FINAL_ROUND_OF | PIP-6 | [PIP-07-FULL-TEXT](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-07-91652743-f916-4566-99af-421a557f7c3d.json) |
| PIP-8 | EXPANDED_BY | PIP-18 | [SRC-PIP-08-62506041](../../archive/semantic/governance/pip-supersession-index.json) |
| PIP-9 | GOVERNS_STV_METHOD_USED_BY | PIP-27 | [SRC-PIP-09-1CC4BB6F](../../archive/semantic/governance/pip-supersession-index.json) |
| PIP-11 | COUNCIL_ELECTION_UNDER | PIP-10 | [PIP-11-FULL-TEXT](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-11-7b48a62d-13c3-4a1e-8565-6ea7bfb4b4dc.json) |
| PIP-13 | FAILED_ATTEMPT_TO_MODIFY | PIP-10 | [SRC-PIP-13-B721D8E7](../../archive/semantic/governance/pip-supersession-index.json) |
| PIP-25 | COUNCIL_ELECTION_UNDER | PIP-10 | [PIP-25-FULL-TEXT](../../archive/raw/social-governance-semantic-enrichment/governance/pip-captures/pip-25-91cc73fa-0af7-41ea-86c5-bab7ffcfcb4f.json) |
| PIP-20 | ESTABLISHES_PROGRAM_FOR | PIP-27 | [SRC-PIP-20-159CB743](../../archive/semantic/governance/pip-supersession-index.json) |

## PIP-33 financial-term preservation

PIP-33 authorized a stated maximum of **$469,513.53** through two displayed tranches of **$234,756.76**. Each tranche is **$176,067.57 USDC (75%)** plus **$58,689.19 ATLAS-equivalent (25%)**. The first tranche was scheduled for T+14 days. The second was scheduled for T+194 days—180 days after the first—and was conditional on retaining sufficient DAO Treasury capital for an additional year of Foundation/DAO operating costs.

The displayed tranches total **$469513.52**, one cent below the stated total. Their USDC components total **$352135.14**, one cent below the stated USDC aggregate. Both discrepancies are preserved; neither is silently corrected. Authorization and schedule do not prove payment: `payment_state` remains `UNVERIFIED`, while `onchain_verification_state` is `MISSING_ONCHAIN_EVIDENCE`.

## Conflict register

| Conflict | PIPs | Finding | Treatment | Status |
|---|---|---|---|---|
| GOV-CONFLICT-PORTAL-STATUS-001 | PIP-1, PIP-2, PIP-3, PIP-4, PIP-5, PIP-6, PIP-7, PIP-8, PIP-9, PIP-10, PIP-11, PIP-12, PIP-13, PIP-14, PIP-15, PIP-16, PIP-17, PIP-18, PIP-19, PIP-20, PIP-21, PIP-22, PIP-23, PIP-24, PIP-25, PIP-26, PIP-27, PIP-28, PIP-29, PIP-30, PIP-31, PIP-32, PIP-33 | Every captured portal object remains Proposal_Activated_Pending_Open_Voting after its recorded vote end. | Preserve the portal value as source metadata; derive no result or implementation state from it. | OPEN_DOCUMENTED |
| GOV-CONFLICT-ELECTION-WALLET-PLACEHOLDERS-001 | PIP-25, PIP-27 | The portal captures repeat the Solana sentinel value 11111111111111111111111111111111 across candidate wallet fields; it is not treated as a candidate identity. | Preserve the captured value separately, set normalized wallet_public_key to null, and require an official candidate-to-wallet mapping. | OPEN_DOCUMENTED |
| GOV-CONFLICT-FAILED-MILESTONES-001 | PIP-13, PIP-15, PIP-19, PIP-26 | The Council tracker reports milestone completion for four failed proposals that supplied no authorization. | Preserve the attributed tracker value but set implementation.state and implementation.independent_verification_state to NOT_APPLICABLE_NO_AUTHORIZATION. | RESOLVED_BY_ADJUDICATION |
| GOV-CONFLICT-ELECTION-WINNERS-001 | PIP-11, PIP-25, PIP-27 | Council-reported passage exists, but the preserved portal captures contain no electionResults winner list. | Retain aggregate ballots/PVP and unresolved winner identity; infer no officeholder or program winner. | OPEN_DOCUMENTED |
| GOV-CONFLICT-ELECTION-CANDIDATE-PVP-001 | PIP-6, PIP-7, PIP-11, PIP-25, PIP-27 | The portal captures preserve only aggregate ranked-choice ballots and PVP, not candidate-level PVP. | List captured candidates and set every candidate PVP field to null with MISSING_FROM_CAPTURE status. | OPEN_DOCUMENTED |
| GOV-CONFLICT-PIP-027-BALLOT-CONFIG-001 | PIP-27 | PIP-27 records five winners, six maximum choices, and thirteen candidates while the proposal text describes five winners. | Preserve all captured values and do not normalize the maximum-choice field. | OPEN_DOCUMENTED |
| GOV-CONFLICT-PIP-033-FUNDING-SOURCE-001 | PIP-33 | The semantic source labels PIP-33 as Ecosystem Fund, while the proposal identifies an extraordinary direct DAO Treasury measure and the Council tracker marks ecosystem_fund NO. | Use DIRECT_DAO_TREASURY_MEASURE and retain the semantic label as a rejected conflict. | RESOLVED_BY_ADJUDICATION |
| GOV-CONFLICT-PIP-033-RESULT-001 | PIP-33 | The Council tracker result is null, while completed portal PVP supports the repository-reviewed PASSED result. | Preserve the tracker null and use the explicitly labeled repository editorial vote adjudication. | OPEN_DOCUMENTED |
| GOV-CONFLICT-PIP-033-ARITHMETIC-001 | PIP-33 | Two displayed tranches sum to $469,513.52 versus the stated $469,513.53 total; displayed USDC portions sum to $352,135.14 versus the stated $352,135.15 aggregate. | Preserve both one-cent discrepancies without silent correction. | OPEN_DOCUMENTED |
| GOV-CONFLICT-TREASURY-VERIFICATION-001 | PIP-5, PIP-8, PIP-12, PIP-14, PIP-16, PIP-17, PIP-18, PIP-20, PIP-21, PIP-22, PIP-29, PIP-30, PIP-33 | Council-reported payment values and PIP-33 authorization lack transaction-level on-chain evidence in the repository; PIP-33 payment occurrence remains UNVERIFIED. | Use COUNCIL_REPORTED only for attributed tracker values, keep PIP-33 payment_state UNVERIFIED, and use MISSING_ONCHAIN_EVIDENCE only for on-chain verification; never mark paid or verified. | OPEN_DOCUMENTED |
| GOV-CONFLICT-PIP-001-QUORUM-001 | PIP-1 | PIP-1 mentions quorum but supplies no numeric threshold; the completed-binary YES-versus-NO rule is an owner-approved repository editorial adjudication. | Label the adjudication as repository-editorial and never assert that it appears in PIP-1. | RESOLVED_BY_ADJUDICATION |

## Prioritized governance research backlog

| Priority | Research item | PIPs | Required artifacts | Prohibited inference |
|---|---|---|---|---|
| P0 | GOV-RESEARCH-001: Who won the unresolved Council and DAO Casters elections, and what were the candidate-level totals? | PIP-11, PIP-25, PIP-27 | Official STV tabulation export, Official final winner announcement, Per-candidate PVP and transfer-round data | Do not infer winners from later Council membership, social posts, or tracker passage alone. |
| P0 | GOV-RESEARCH-002: Which authorized or Council-reported payments occurred on-chain? | PIP-5, PIP-8, PIP-12, PIP-14, PIP-16, PIP-17, PIP-18, PIP-20, PIP-21, PIP-22, PIP-29, PIP-30, PIP-33 | Transaction signatures, DAO/Foundation source accounts, Recipient token accounts, Mint and decimals metadata, Block timestamps, Proposal-to-transfer mapping | Do not treat Council tracker amounts, vote passage, or a payment schedule as proof of transfer. |
| P1 | GOV-RESEARCH-003: What primary records establish termination, cancellation, or withdrawal after passage? | PIP-14, PIP-17, PIP-31 | Council or Foundation termination notice, Author withdrawal notice, Contract or milestone closeout record | Do not convert Council tracker terminology into independently verified completion or non-performance findings. |
| P1 | GOV-RESEARCH-004: What independent evidence supports implementation or deliverable completion for each authorized non-election proposal? | PIP-1, PIP-2, PIP-3, PIP-4, PIP-5, PIP-8, PIP-9, PIP-10, PIP-12, PIP-14, PIP-16, PIP-17, PIP-18, PIP-20, PIP-21, PIP-22, PIP-23, PIP-24, PIP-28, PIP-29, PIP-30, PIP-31, PIP-32, PIP-33 | Proposal-specific deliverables, Foundation execution notices, Contracts or releases, Independent outcome evidence | Do not equate 1/1 tracker milestones with independent implementation verification. |
| P1 | GOV-RESEARCH-007: Which candidate wallet belongs to each captured PIP-25 and PIP-27 candidate? | PIP-25, PIP-27 | Official candidate-to-wallet mapping, Signed candidate registration record or official ballot export | Do not assign the repeated Solana sentinel value to any candidate and do not infer wallets from names or later officeholding. |
| P2 | GOV-RESEARCH-005: Can historical portal state transitions be recovered? | PIP-1, PIP-2, PIP-3, PIP-4, PIP-5, PIP-6, PIP-7, PIP-8, PIP-9, PIP-10, PIP-11, PIP-12, PIP-13, PIP-14, PIP-15, PIP-16, PIP-17, PIP-18, PIP-19, PIP-20, PIP-21, PIP-22, PIP-23, PIP-24, PIP-25, PIP-26, PIP-27, PIP-28, PIP-29, PIP-30, PIP-31, PIP-32, PIP-33 | Timestamped proposal-state snapshots, Portal event log, Official lifecycle export | Do not infer state-transition dates solely from vote windows. |
| P1 | GOV-RESEARCH-006: Which PIP-33 figures control the authorized and conditional tranche payments? | PIP-33 | Author or Foundation arithmetic correction, Executed payment instruction, Second-tranche reserve assessment | Do not silently choose a corrected cent value or infer that either tranche was paid. |

## Evidence and review status

- [Machine ledger](PIP-Registry.json)
- [Official portal semantic registry](../../archive/semantic/governance/pip-registry-semantic.json)
- [Portal/Council reconciliation](../../archive/semantic/governance/pip-source-reconciliation.json)
- [Election outcome adjudications](../../archive/semantic/governance/pip-election-round-outcomes.json)
- [Relationship index](../../archive/semantic/governance/pip-supersession-index.json)
- [Campaign conflict report](../../operations/campaigns/canonical-pip-governance-ledger-2026-07/conflict-report.md)
- [Campaign research backlog](../../operations/campaigns/canonical-pip-governance-ledger-2026-07/governance-research-backlog.md)

The ledger remains draft and requires human governance review. Validation establishes structural and evidentiary consistency; it does not establish the truth of Council assessments, implementation, payment, or on-chain execution.
