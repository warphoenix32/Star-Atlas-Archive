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
- Evidence-class assignments: {'CANONICAL_KNOWLEDGE_CANDIDATE': 345, 'DUPLICATE': 43, 'ENTITY_UPDATE_CANDIDATE': 345, 'GRAPH_RELATIONSHIP_CANDIDATE': 136, 'LOW_VALUE': 451, 'RESEARCH_GAP': 537, 'TIMELINE_CANDIDATE': 65}
- Social timeline candidates: 65
- Social promotion candidates: 345
- Social records with unresolved references or media gaps: 674

## Governance findings

- Vote results derived from completed official vote records: {'FAILED': 4, 'PASSED': 26, 'UNKNOWN': 3}
- Approval states: {'APPROVED': 26, 'FAILED': 4, 'UNKNOWN': 3}
- Execution states: {'UNKNOWN': 33}
- Execution gaps requiring primary evidence: 33

`PASSED`/`APPROVED` records are not treated as executed. Every proposal remains `execution_state: UNKNOWN` because the proposal payloads do not contain a separate implementation record, on-chain transaction, treasury transfer, deployed change, or equivalent primary evidence.

## Review posture

All promotion targets are candidates only. Retweets preserve the fact of resharing and are excluded from first-party promotion candidates. Engagement metrics were not used as evidence. Linked media absent from the package is retained as a research gap.

## Validation

Validation status: **PASS**. See `validation-report.md` for the complete checks.
