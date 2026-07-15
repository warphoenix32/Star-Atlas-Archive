# Social Media and PIP Semantic Enrichment Campaign

## Executive summary

The campaign preserved the supplied export without rewriting it, enriched all **796** unique `@staratlas` posts, captured and enriched **33** official PIP portal records, and produced review-only promotion candidates. No canonical knowledge, graph, or publication files were modified.

## Evidence preserved

- Raw export rows: 799
- Unique social posts: 796
- Original `@staratlas` posts: 528
- Explicit retweets/reshared context: 268
- Documented duplicate export rows: 3
- Official PIP records: 33 (PIP-1 through PIP-33)
- Portal raw captures: 33
- Date coverage: 2024-11-05 through 2026-07-14

## Semantic enrichment

- Social topic assignments: {'COMMUNITY': 383, 'CORPORATE': 34, 'ECONOMY': 94, 'EVENT': 56, 'GAMEPLAY': 208, 'GOVERNANCE': 35, 'GUILD': 13, 'LORE': 64, 'MARKETING': 29, 'OPERATIONS': 39, 'PARTNERSHIP': 16, 'PEOPLE': 10, 'PRODUCT': 312, 'TECHNOLOGY': 96}
- Statement type assignments: {'ANNOUNCEMENT': 17, 'CLARIFICATION': 1, 'COMMUNITY_FEEDBACK': 5, 'DESIGN_INTENT': 1, 'DISCUSSION': 652, 'Q_AND_A': 14, 'RELEASE': 14, 'RETROSPECTIVE': 6, 'ROADMAP': 13, 'SPECULATION': 10, 'STATUS_UPDATE': 87, 'TECHNICAL_EXPLANATION': 5, 'THEORYCRAFTING': 10}
- Lifecycle assignments (wording-supported only): {'IN_DEVELOPMENT': 21, 'LIVE': 14, 'PLANNED': 12, 'TESTING': 6, 'UPDATED': 43}
- Evidence-class assignments: {'CANONICAL_KNOWLEDGE_CANDIDATE': 28, 'DUPLICATE': 57, 'ENTITY_UPDATE_CANDIDATE': 28, 'GRAPH_RELATIONSHIP_CANDIDATE': 136, 'LOW_VALUE': 768, 'RESEARCH_GAP': 537, 'TIMELINE_CANDIDATE': 26}
- Social promotion candidates: 345 before; **28** after
- Social promotion exclusions: 768
- Social timeline candidates: 65 before; **26** after
- Social timeline exclusions: 770
- Promotion confidence: {'HIGH': 7, 'MEDIUM': 21}
- Promotion dispositions: {'HIGH_PRIORITY': 7, 'LOW_PRIORITY': 1, 'MEDIUM_PRIORITY': 20, 'NOT_ELIGIBLE': 768}
- Timeline confidence: {'HIGH': 4, 'MEDIUM': 22}
- Duplicate clusters: 25
- Social records with unresolved references or media gaps: 674

## Governance findings

- Human-reviewed results: {'ELECTION_RESULT_RECORDED': 2, 'FAILED': 4, 'PASSED': 24, 'UNKNOWN': 3}
- Passed binary PIPs: [1, 2, 3, 4, 5, 8, 9, 10, 12, 14, 16, 17, 18, 20, 21, 22, 23, 24, 28, 29, 30, 31, 32, 33]
- Failed binary PIPs: [13, 15, 19, 26]
- Election/nonbinary PIPs: [6, 7, 11, 25, 27]
- Unresolved election PIPs: [11, 25, 27]
- Approval states: {'APPROVED': 24, 'ELECTION_RESULT_RECORDED': 2, 'FAILED': 4, 'UNKNOWN': 3}
- Execution states: {'IMPLEMENTATION_PENDING': 26, 'UNKNOWN': 7}
- Implementation gaps requiring primary evidence: 33
- Supersession/dependency relationships: [{'from': 23, 'relation': 'SUPERSEDES', 'to': 4}, {'from': 10, 'relation': 'MODIFIES_AND_EXTENDS', 'to': 3}, {'from': 13, 'relation': 'FAILED_ATTEMPT_TO_MODIFY', 'to': 10}, {'from': 20, 'relation': 'ESTABLISHES_PROGRAM_FOR', 'to': 27}, {'from': 9, 'relation': 'GOVERNS_STV_METHOD_USED_BY', 'to': 27}, {'from': 8, 'relation': 'EXPANDED_BY', 'to': 18}]

Completed binary results use the owner-approved formula `YES PVP > NO PVP => PASSED; NO PVP >= YES PVP => FAILED`; abstentions are recorded but non-decisive and no quorum is imposed. Elections use only the official portal `electionResults` field. `PASSED`/`APPROVED` records are not treated as implemented, and every PIP retains an implementation-evidence gap until separate primary evidence is captured.

All 33 PIPs are reconciled to the governing human corpus review and carry `human_review_status: REVIEWED`. Raw portal status, machine computation, reviewed result, approval, and execution fields remain distinct. PIP-13, PIP-15, PIP-19, and PIP-26 remain failed. PIP-11, PIP-25, and PIP-27 remain unresolved elections.

## Canonical-promotion recommendations

- `knowledge/governance/Star-Atlas-DAO.md`
- `knowledge/governance/Star-Atlas-Foundation.md`
- `knowledge/governance/Star-Atlas-Council.md`
- `knowledge/economy/Ecosystem-Fund.md`
- `knowledge/governance/PIP-Registry.md`
- `knowledge/governance/Governance-Programs.md`
- `knowledge/timeline/`

These remain review-only inputs; this campaign does not modify canonical knowledge or graph facts.

## Review posture

All promotion targets are candidates only. Retweets preserve the fact of resharing and are excluded from first-party promotion candidates. Engagement metrics were not used as evidence. Linked media absent from the package is retained as a research gap.

## Validation

Validation status: **PASS**. See `validation-report.md` for the complete checks.
