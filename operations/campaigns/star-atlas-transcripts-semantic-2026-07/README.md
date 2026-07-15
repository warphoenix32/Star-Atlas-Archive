# Star Atlas Transcript Semantic Enrichment 2026-07

This campaign creates a review-only semantic evidence layer for the 36 Economic Forum, DAO, and Town Hall transcripts preserved by `star-atlas-transcripts-ingestion-2026-07`.

## Method

Segments are selected using lexical topic signatures, explicit conversational transitions, transcript time gaps, and maximum-coherence safeguards. They are not fixed timestamp slices.

The segment index is the recall-oriented research layer. Candidate eligibility is a separate decision: detecting a topic or statement tag does not make a segment promotable, dateable, or quotable. The generator records a decision for every segment in `promotion-candidate-decisions.json` and `timeline-candidate-decisions.json`, including exact caption support and an exclusion reason when rejected.

Each segment preserves:

- Source ID and recording ID
- Start and end timestamps
- Exact transcript path and line range
- Caption count and content checksum
- Unknown speaker status
- Controlled topics and statement classifications
- Product lifecycle language
- Canonical entity mentions and unresolved references
- Evidence classifications and promotion targets

## Candidate decisions

Promotion eligibility requires an identifiable institutional object plus a discrete claim signal grounded in exact captions. Strong signals include release, deployment, testing, proposal, vote, correction, deprecation, technical capability, organizational action, a concrete date or metric, or a relationship between identifiable entities. Greetings, logistics, generic discussion, unanswered questions, unsupported speculation, vague future language, and weak keyword collisions are excluded.

Promotion scoring is deterministic:

- +2 identifiable entity or institutional object
- +2 strong statement or event language
- +1 concrete action or capability
- +1 each for multiple supporting captions, numeric/date detail, and complete source metadata
- -1 each for transcript ambiguity, speculative wording, or unknown speaker
- -2 when clustered as a weaker near-duplicate

Eligible records are assigned `HIGH_PRIORITY` at 7 or more points, `MEDIUM_PRIORITY` at 5–6, and carefully justified `LOW_PRIORITY` at 3–4. Confidence is `HIGH` at 7 or more, `MEDIUM` at 4–6, and `LOW` below 4. Confidence measures extraction quality, not factual truth.

Timeline eligibility independently requires a concrete institutional event, an identifiable entity or system, event-state language, exact captions, and either a normalized date or an explicit unresolved-date basis. Generic roadmap discussion, aspirations, hypothetical examples, questions, recurring logistics, and undated background explanations remain excluded even when their segment tags are retained.

Quote eligibility requires a concise, verbatim caption containing institutional value: an announcement, release/deployment statement, concrete roadmap commitment, correction, governance action, technical explanation, economic statement, or institutional rationale. Fragments, questions without answers, filler, generic claims, low-context excerpts, and transcription artifacts are excluded. Speakers remain `UNKNOWN` unless the transcript explicitly supplies attribution.

## Contextual classification

`ROADMAP`, `SPECULATION`, `RELEASE`, `LIVE`, and `Q_AND_A` require contextual qualification. Future tense alone is not a roadmap; uncertainty words alone are not speculation; release language requires a nearby product or feature; testing and limited access remain distinct from public release; and the word “question” alone is not Q&A. Lifecycle states also require an identifiable product, feature, proposal, or system and retain their exact caption evidence.

## Duplicate handling

Evidence is never deleted. Deterministic near-duplicate clustering uses normalized claim signatures, source/entity/statement combinations, token overlap, and adjacent repeated segments. Each cluster records its strongest candidate and why the other evidence is related. Candidate strength favors clearer wording, tighter timestamps, stronger entity identification, higher evidence density, and better date context.

## Research gaps

Research gaps are typed rather than assigned generically. Supported types include missing speaker attribution, missing original URL, incomplete publication date, ambiguous product identity, unclear proposal number, uncertain lifecycle state, missing official confirmation, missing execution evidence, and transcript-recognition uncertainty.

## Controlled topics

`PRODUCT`, `GAMEPLAY`, `GOVERNANCE`, `ECONOMY`, `TECHNOLOGY`, `LORE`, `CORPORATE`, `PEOPLE`, `COMMUNITY`, `PARTNERSHIP`, `GUILD`, `EVENT`, `MARKETING`, `OPERATIONS`

## Statement classifications

`ANNOUNCEMENT`, `STATUS_UPDATE`, `ROADMAP`, `RELEASE`, `DESIGN_INTENT`, `TECHNICAL_EXPLANATION`, `Q_AND_A`, `RETROSPECTIVE`, `CLARIFICATION`, `CORRECTION`, `COMMUNITY_FEEDBACK`, `DISCUSSION`, `SPECULATION`, `THEORYCRAFTING`

## Evidence safety

- All promotion candidates remain `PROPOSED_ONLY` and require manual review.
- Lifecycle tags describe transcript wording; they do not prove release, execution, or current status.
- PIP tags establish mentions or discussions, not proposal outcomes.
- Quotations are preserved with `speaker: UNKNOWN` and require attribution review.
- No `FIRST_MENTION` tag is assigned because corpus ordering and partial dates cannot establish historical priority.
- No canonical knowledge, graph fact, or publication output is changed.

## Reproduction

From the repository root:

```text
python operations/campaigns/star-atlas-transcripts-semantic-2026-07/generate_semantic_index.py
python operations/campaigns/star-atlas-transcripts-semantic-2026-07/validate_semantic_index.py
```
