# Evidence Significance Standard

## Purpose

This standard governs the `DRAFT` and `REVIEW` stages for transcripts and conversational records. It distinguishes preservation from significance: the Archive retains the supplied record, while knowledge promotion selects only material that helps explain Star Atlas products, institutions, events, organizations, communities, or historical relationships.

Significance adjudication is not a fifth pipeline stage. It is the substantive decision inside `DRAFT -> REVIEW`.

## Transcript evidence

The default evidence unit is information-centered rather than speaker-centered. Preserve:

- recording, episode, or video identity;
- Source ID and authoritative normalized transcript path;
- exact start and end timestamps;
- exact supporting captions and line references;
- a neutral claim or discussion description;
- named and unresolved entities;
- lifecycle or event-state wording;
- corroboration, contradiction, and research-gap status;
- the original or external video URL when already known.

Never invent a URL or speaker. Unknown attribution is not a universal confidence penalty. Each candidate must declare:

- `speaker_attribution`: observed value or `UNKNOWN`;
- `speaker_dependency`: `NONE`, `PARTIAL`, or `REQUIRED`;
- `institutional_attribution`: `UNESTABLISHED`, `CORROBORATED`, or `SOURCE_EXPLICIT`;
- transcript-integrity and claim-extraction confidence;
- corroboration status.

`NONE` means the informational claim remains useful without identifying the speaker. `PARTIAL` means attribution affects institutional weight but not the ability to preserve the discussion. `REQUIRED` means the claim is a personal position, promise, responsibility, or other assertion whose meaning materially depends on who spoke. Unknown attribution blocks named-person quotations and authoritative-position claims when dependency is `REQUIRED`; it does not block timestamped information-centered evidence.

## Discord evidence

Retain the message-level index, but evaluate significant conversations as contextual windows rather than isolated keyword matches. A reviewable conversation record should preserve, when available:

- channel, thread, and native identifiers;
- start and end timestamps;
- every included Source ID;
- observed participants and display names without silently resolving identity;
- reply, mention, or chronological linkage;
- topic continuity and relevant preceding or following messages;
- guild, organization, product, governance, event, or community links;
- recurrence, escalation, resolution, or relationship change;
- exact excerpts and omissions.

Supported interaction descriptions include `DISAGREEMENT`, `COMPETITIVE_RIVALRY`, `POLICY_CONFLICT`, `GUILD_DISPUTE`, `ACCUSATION`, `ESCALATION`, `REPEATED_ANTAGONISM`, `RECONCILIATION`, `ALLIANCE_FORMATION`, `ALLIANCE_BREAKDOWN`, `COORDINATION`, `PUBLIC_SUPPORT`, `BANTER_OR_PERFORMANCE`, and `AMBIGUOUS_INTERACTION`.

These labels describe observed conversation structure; they do not establish motive, character, truth, guilt, or a permanent relationship.

## Scope boundary

Raw evidence remains immutable even when content is not suitable for evaluation.

Exclude from semantic and knowledge promotion:

- real-world politics unrelated to Star Atlas;
- culture-war discussion and unrelated games;
- off-topic personal commentary;
- personal attacks that do not materially concern Star Atlas conduct or history;
- isolated insults, provocation, or sentiment without contextual significance.

Star Atlas-related interpersonal material may be considered only when it materially concerns guild conduct, governance, competition, transactions, leadership, moderation, alliances, institutional decisions, or documented in-game or community actions. Preserve the minimum adjacent off-topic text needed to understand an otherwise in-scope exchange. Use `OUT_OF_SCOPE_OR_AMBIGUOUS` when the boundary cannot be resolved safely.

## Significance assessment

Message count, keyword density, sentiment, or model confidence cannot establish significance. Assess candidates across:

- historical importance;
- institutional consequence;
- product, governance, economic, or technical relevance;
- relationship significance and recurrence;
- context completeness;
- novelty versus stronger existing evidence;
- corroboration or contradiction;
- researcher utility;
- reputational sensitivity.

Use `PROMOTE`, `PROMOTE_AS_CONTEXT`, `MERGE_WITH_STRONGER_EVIDENCE`, `NEEDS_CORROBORATION`, `RESEARCH_GAP`, `DUPLICATE`, or `ARCHIVE_ONLY` as review recommendations. They do not bypass the repository risk model or authorize publication.

## Reputational safeguard

Do not infer hostility, animosity, misconduct, motive, or guild relationships from sentiment alone. Distinguish disagreement from hostility and banter from antagonism. A reputationally adverse interpretation about an identifiable person or organization is at least `R3`, requires exact context and counterevidence, and must be presented for individual human adjudication before entering canonical knowledge or public narrative.

## Human review packet

Present consequential clusters one at a time with:

- a stable decision ID;
- exact Source IDs, timestamps, excerpts, and context boundaries;
- observed participants and unresolved identities;
- the proposed historical finding;
- speaker dependency and attribution limits;
- corroboration, conflicts, and plausible alternative readings;
- proposed knowledge destination and risk class;
- a recommendation;
- `ACCEPT`, `ACCEPT_WITH_QUALIFICATION`, `DEFER`, and `REJECT` options.
