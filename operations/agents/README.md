# Repository Agent Contracts

These contracts assign ownership within the repository's four-stage workflow:

```text
PRESERVE -> DRAFT -> REVIEW -> PUBLISH
```

They are operating boundaries, not autonomous permissions. An agent may work only within the authority granted by the current task, repository policy, branch protection, and these contracts. No contract authorizes a direct merge, rewriting preserved evidence, or silently resolving a matter reserved for human adjudication.

## Core roles

| Role | Primary stage | Contract |
| --- | --- | --- |
| Lead Coordinator | all | [Coordination Contract](COORDINATION-CONTRACT.md) |
| Archive Steward | PRESERVE | [Archive Steward Contract](ARCHIVE-STEWARD-CONTRACT.md) |
| Knowledge Curator | DRAFT | [Knowledge Curator Contract](KNOWLEDGE-CURATOR-CONTRACT.md) |
| Risk and Review Agent | REVIEW | [Risk and Review Contract](RISK-REVIEW-CONTRACT.md) |
| Library Publisher | PUBLISH | [Library Publisher Contract](LIBRARY-PUBLISHER-CONTRACT.md) |

The [Shared Operating Contract](SHARED-OPERATING-CONTRACT.md) applies to every role. The [Evidence Significance Standard](EVIDENCE-SIGNIFICANCE-STANDARD.md) governs transcript and conversational review without adding a fifth pipeline stage. On-demand specialists and their activation boundaries are defined in the [Specialist Registry](SPECIALIST-REGISTRY.md). The [Research and Gap Analyst](RESEARCH-GAP-ANALYST-CONTRACT.md) additionally owns the cross-source coverage register, acquisition backlog, and recurring-source freshness queue.

## Reader-first publication rule

Knowledge is written for people. A knowledge page must read as a coherent, evidence-qualified account rather than a concatenation of semantic records. It must be comprehensive enough for research use, engaging without becoming promotional, and structured so readers and search engines can understand its subject.

Controlled taxonomy, workflow labels, and machine confidence belong in YAML front matter or one consolidated reference section. The public Library hides front matter by default. Repeated taxonomy markers must not be attached to individual paragraphs unless a visible qualification is necessary to prevent a material misunderstanding; in that case, use plain-language attribution or an evidence note instead of opaque codes.

## Human authority

Agents must surface decisions needing human review as soon as they arise and summarize unresolved decisions again at PR closeout. Each decision must include the evidence, recommendation, consequence, allowed options, and an explicit defer option.
