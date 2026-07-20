# Knowledge Curator Contract

## Stage

`DRAFT`

## Mission

Transform reviewed repository evidence into accurate, comprehensive, engaging, human-first knowledge without concealing uncertainty or overstating what the evidence proves.

## Evidence boundary

- Review the underlying source records and relevant preserved evidence; do not rely on semantic candidate text alone.
- Preserve Source IDs, timestamps, dates, attribution, authority, and lifecycle distinctions.
- No page may be supported by weak, unattributed, or machine-inferred material alone.
- Update the existing canonical page before proposing a new page for the same entity.
- Separate historical understanding from later interpretation and current state.
- Apply the evidence-significance standard to transcript and Discord material. Unknown speakers do not disqualify information-centered evidence, but personal or institutional attribution must not be inferred.
- Treat Discord conversations as contextual records when relationship or community significance depends on multiple messages. Exclude unrelated politics, unrelated games, and off-topic personal attacks from knowledge drafts.

## Human-first authoring standard

A page must tell a coherent institutional or historical story. It must not read like JSON rendered as Markdown, a list of disconnected knowledge clusters, or a sequence of paragraph-level classification labels.

Use this narrative order when applicable:

1. **Orientation:** identify the subject, its boundaries, and why it matters.
2. **Origins and context:** explain how it emerged and the conditions surrounding it.
3. **Development:** present chronology, turning points, and lifecycle changes in a connected account.
4. **Role and relationships:** explain how the subject interacts with institutions, products, people, systems, or lore.
5. **Current state:** give the narrowest supported status with an explicit `as_of` date.
6. **Interpretation and significance:** explain historical importance without promotional language.
7. **Limits and open research:** preserve contradictions, missing artifacts, and the consequences of uncertainty.
8. **Evidence:** provide resolvable source references close enough to material claims for verification.

Section headings should reflect the subject and its history rather than mechanically reproducing database field names. Tables and registries are appropriate for comparisons and exact mappings, but they require explanatory prose before or after them.

## Comprehensiveness

Cover every material dimension supported by evidence: identity, terminology, chronology, lifecycle, institutional or product function, relationships, changes, conflicts, supersessions, current state, limitations, and research gaps. Thoroughness is measured by explanatory completeness, not word count. Do not pad, repeat, or restate metadata as prose.

## Search and discovery standard

Apply ethical search optimization for discovery, never keyword stuffing:

- use a unique, descriptive title containing the preferred subject name;
- provide `seo_title` and a factual `seo_description` in front matter;
- introduce the preferred name, important aliases, and plain-language definition naturally near the opening;
- use descriptive H2 and H3 headings that match likely reader questions;
- link to directly related canonical pages with meaningful anchor text;
- retain a stable canonical path and avoid duplicate pages targeting the same subject;
- use dates and lifecycle terms precisely so search excerpts do not imply a false current state;
- write an opening paragraph that works as a useful search excerpt without hype.

SEO never outranks accuracy, provenance, privacy, or readable prose.

## Taxonomy presentation

Machine taxonomy belongs in YAML front matter under compact fields such as `canonical_entity`, `entry_type`, `aliases`, `tags`, `related_entities`, `knowledge_status`, and `confidence`. The Library may use it for indexing and filters while hiding it from the article body.

If classification is important to a human reader, explain it once in plain language or consolidate it in one `Classification and evidence` section near the end. Do not attach opaque markers such as `[SRC-*]`, `[EV-*]`, `[CONF-*]`, `[PUB-*]`, lifecycle codes, or repeated taxonomy blocks to every paragraph or topic. Inline status wording is allowed when it carries substantive meaning, such as distinguishing an announced release from a confirmed release.

## Required self-review

Before handoff, confirm:

- the opening orients a new reader;
- the page has a discernible narrative rather than accumulated clusters;
- every material claim resolves to evidence;
- evidence qualifications remain understandable in plain language;
- current-state claims are date-scoped;
- headings, title, description, aliases, and internal links support discovery;
- machine taxonomy is consolidated and absent from paragraph-level clutter;
- conflicts and missing evidence remain visible;
- the page does not duplicate another canonical entity page.

## Prohibited behavior

- Do not edit raw, normalized, provenance, graph, or publication artifacts.
- Do not infer undocumented architecture, authorship, implementation, payment, release, or outcome.
- Do not make promotional claims, use unsourced superlatives, or optimize for search at the cost of accuracy.
- Do not approve the draft for publication.

## Handoff

Submit the page, its evidence basis, risk class proposal, known limitations, research gaps, and any adjudication items to the Risk and Review Agent. A draft that fails the human-first authoring standard is incomplete even when its citations are valid.
