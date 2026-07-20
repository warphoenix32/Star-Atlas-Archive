---
title: "SCORE-to-Starbased Transition"
seo_title: "Star Atlas SCORE and Faction Fleet to Starbased History"
seo_description: "A careful history of SCORE, Faction Fleet rewards, the Starbased transition, announced emissions deprecation, and the execution evidence still missing."
knowledge_status: HISTORICAL
as_of: 2026-07-20
confidence: MEDIUM
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-19357309E964FAF8.md"
  - "archive/source-records/campaign-delta-official/SRC-OFF-0333A5B22A207D88.md"
  - "knowledge/gameplay/Official-Current-State-Snapshot-2026-07-12.md"
known_limitations:
  - "The April 2024 emissions shutdown is supported as an announced plan, not independently verified execution."
  - "Program listing, user-interface availability, reward emissions, and residual contract functionality are separate states."
research_gaps:
  - "Recover the post-April-16 shutdown confirmation, final reward block, transaction evidence, and current user-interface test."
  - "Verify SCORE program upgrade authority and residual on-chain functionality."
review_after: 2027-01-17
---

# SCORE-to-Starbased Transition

SCORE, also presented as Faction Fleet, was an early Star Atlas fleet-management and ATLAS-emissions surface. Starbased later introduced an active SAGE-centered reward model and announced the reduction and shutdown of older passive emissions. The archive supports the release and transition announcements, but not final execution of every scheduled deprecation.

## Identity and scope

The history contains several narrow objects:

- **SCORE/Faction Fleet application surface** — browser/user-facing fleet enlistment;
- **SCORE mainnet program** — the separately documented on-chain program;
- **Faction Fleet ATLAS-emissions program** — the reward stream associated with participation;
- **R4 consumption and Faction Claims** — related but distinct resource systems;
- **SAGE Labs legacy game ID** — configuration targeted by the announced transition;
- **Starbased update/game ID** — the later SAGE Labs economic and faction-infrastructure surface.

Official materials described sending ships on missions through Faction Fleet, consuming resources, and receiving ATLAS. [SRC-OFF-0AED270D51ACD552](../../archive/source-records/campaign-delta-official/SRC-OFF-0AED270D51ACD552.md)

## Lifecycle chronology

| Date | Object and state | Finding |
|---|---|---|
| 2021-12-16/17 | SCORE/Faction Fleet `LIVE` | Aephia reports December 16 availability; ATMTA’s official release publication is dated December 17. Preserve the one-day wording/publication difference. [Community record](../../archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-21D7FE432327A762.md) [Official record](../../archive/source-records/campaign-delta-official/SRC-OFF-0AED270D51ACD552.md) |
| 2024-03-26 | transition `ANNOUNCED` | Official Discord planned a 50% Faction Fleet emissions reduction at Starbased launch and planned to set older game-ID economic variables to zero on April 16. This is plan evidence. [SA-DISCORD-ANN-9FFFF91025488D09](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-9FFFF91025488D09.json) |
| 2024-04-02 | Starbased `DELAYED` | Deployment issues delayed the announced April 2 release; the next-day target is not release proof. [SA-DISCORD-ANN-76D9861DCB3FE798](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-76D9861DCB3FE798.json) |
| 2024-04-04 | Starbased `LIVE` | Official Discord stated Starbased was live, while qualifying the first epoch as zero ATLAS and disabling LP deposits. Product availability and full economic activation remained distinct. [SA-DISCORD-ANN-CCF4600A4C08F697](../../archive/normalized/discord-announcements/messages/SA-DISCORD-ANN-CCF4600A4C08F697.json) |
| 2024-04-15 | Faction Fleet emissions `DEPRECATION_ANNOUNCED` | Aephia stated in future tense that emissions would end “this Tuesday,” April 16. It is not post-event confirmation. [SRC-AEPHIA-19357309E964FAF8](../../archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-19357309E964FAF8.md) |
| 2026-04-16 documentation | SCORE program `DOCUMENTED` | Official Mainnet Program IDs still lists the SCORE program. Listing does not prove active emissions or user-facing availability, but prevents collapsing program existence into reward deprecation. [SRC-OFF-F217B64FD0342839](../../archive/source-records/campaign-delta-official/SRC-OFF-F217B64FD0342839.md) |

## Transition mechanics and evidence limits

The March announcement describes economic migration intent: reduce passive Faction Fleet emissions, move rewards toward Starbased activity, and later zero variables on an older game ID. The April 4 record establishes Starbased availability. Neither record independently proves the April 16 parameter changes or final Faction Fleet reward block.

Aephia’s Starbased guide provides detailed community-maintained mechanics but was updated after publication. It is useful B2 operational context and must be version-qualified. [SRC-AEPHIA-BF39BD68F68A5FB2](../../archive/source-records/campaign-alpha-aephia/SRC-AEPHIA-BF39BD68F68A5FB2.md)

SCORE's historical role should not be collapsed into SAGE. The products are connected in the evolution of browser and on-chain gameplay, but each has its own mechanics, dates, and evidence states.

## Current state

As of 2026-07-17:

- original SCORE/Faction Fleet reward design: `HISTORICAL`;
- Faction Fleet emissions: `DEPRECATION_ANNOUNCED / EXECUTION_UNVERIFIED`;
- residual application surface: `UNKNOWN`;
- SCORE mainnet program: `DOCUMENTED` in April 2026, with operational state `UNKNOWN`;
- Starbased: stated `LIVE` on 2024-04-04, without proof that every transition step executed.

## Missing artifacts

Required evidence includes a post-April-16 official confirmation, final reward transaction or block, parameter-change transaction, old/new game-ID state history, current UI test, program deployment and upgrade history, and upgrade authority.

## Review status

`HISTORICAL` and evidence-qualified. The earlier page collapsed an announced plan into confirmed execution; this revision records deprecation as announced and execution as unverified.

## Related pages

- [SAGE Product-Family History](SAGE.md)
- [Product Registry](Product-Registry.md)
