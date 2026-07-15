# Codex Execution Contract — Knowledge Generation Wave 2

## Role

Codex is the bulk execution engine. It does not independently decide that available semantic evidence becomes canonical truth.

The Chief of Staff / Institutional Knowledge Curator owns:

- page authorization;
- page risk classification;
- evidence interpretation;
- contradiction resolution;
- lifecycle meaning;
- final knowledge status;
- final promotion approval.

Codex owns:

- repository inventory;
- evidence-packet assembly;
- page drafting at scale;
- deterministic metadata and citation generation;
- index and cross-link maintenance;
- validation;
- applying review corrections;
- clean branch and PR execution.

## Start condition

Do not begin implementation until explicitly instructed to execute this campaign.

At execution time:

1. fetch latest `main`;
2. inspect open and recently merged semantic PRs;
3. determine which evidence packages are present on `main`;
4. identify any approved evidence still confined to unmerged branches;
5. report dependencies before drafting pages;
6. do not silently copy unmerged evidence into the campaign.

## Required preflight inventory

Produce:

```text
operations/campaigns/knowledge-generation-wave-2/execution/page-inventory.json
operations/campaigns/knowledge-generation-wave-2/execution/page-inventory.md
operations/campaigns/knowledge-generation-wave-2/execution/evidence-availability.json
operations/campaigns/knowledge-generation-wave-2/execution/dependency-report.md
```

Inventory:

- every existing `knowledge/` page;
- every proposed page in `generation-plan.md`;
- overlapping or duplicate entity pages;
- relevant semantic promotion candidates;
- relevant archive/source records;
- missing evidence dependencies;
- existing incoming links and index entries;
- likely page action: `CREATE`, `EXPAND`, `MERGE`, `REDIRECT`, `DEFER`, or `RESEARCH_ONLY`.

## Evidence packet requirement

Before drafting a page, create a structured evidence packet containing:

```yaml
page_id:
proposed_path:
page_action:
proposed_knowledge_status:
page_risk_score:
page_risk_class:
subject_entities:
aliases:
scope:
material_claims:
  - claim_id:
    claim_text:
    claim_type:
    temporal_scope:
    lifecycle_state:
    supporting_sources:
    source_authority:
    corroboration_status:
    contradiction_status:
    attribution_required:
    confidence:
    allowed_in_page:
known_limitations:
research_gaps:
review_required:
review_after:
```

Store evidence packets under:

```text
operations/campaigns/knowledge-generation-wave-2/evidence-packets/
```

No page may be drafted without an evidence packet.

## Page drafting rules

Every page must:

- use the metadata defined in the campaign README;
- cite material claims using stable repository evidence paths or source IDs;
- distinguish current and historical state;
- preserve source attribution;
- surface contradictions and unknowns;
- avoid repetitive boilerplate that obscures the subject;
- link to parent indexes and related pages;
- contain a concise scope statement;
- identify aliases where relevant;
- identify supersession, predecessor, successor, and dependency relationships where supported;
- avoid raw semantic-record dumping.

A page may be incomplete. Use an explicit `Known limitations` or `Open questions` section instead of fabricating completeness.

## Knowledge-status rules

### CANONICAL

Use only when:

- page risk is R1 or approved low R2;
- material claims are direct and well-supported;
- contradictions are absent or resolved;
- current-state claims are fresh and date-scoped.

### QUALIFIED

Use when:

- page risk is R2;
- one authoritative source supports the claim;
- attributed operational claims are included;
- minor discrepancies or implementation gaps remain.

### PROVISIONAL

Use when:

- page risk is R3;
- the page is useful despite incomplete evidence;
- all uncertainty is visible;
- a review date is assigned.

### HISTORICAL

Use when:

- the page primarily documents a past or superseded state;
- current applicability is not implied;
- historical context is useful despite incomplete modern reconciliation.

R4 material requires explicit curator approval. R5 material must not enter `knowledge/`.

## Initial implementation scope

The first Codex implementation PR should execute Wave A only:

- 12–18 pages or substantive expansions;
- governance foundation pages;
- principal organization pages;
- PIP lifecycle and registry expansion;
- Product Registry expansion;
- major product pages with strongest evidence;
- events index expansion;
- official communication source profiles.

Do not attempt all 45–65 pages in a single PR.

## Branch and PR strategy

Create one implementation branch per wave:

```text
knowledge/wave-2a-foundation-pages
knowledge/wave-2b-program-histories
knowledge/wave-2c-breadth-and-provisional
```

Each branch should normally target current `main`. Stack only when a later wave directly depends on unmerged files from the previous wave, and state that dependency explicitly.

Keep implementation PRs draft until semantic review completes.

## Wave A priority order

1. Expand PIP Registry.
2. Create DAO, Foundation, Council, and Ecosystem Fund pages.
3. Create PIP lifecycle and governance implementation-state pages.
4. Expand Institutional Overview.
5. Expand Product Registry.
6. Create the strongest-supported major product pages.
7. Expand Events index.
8. Create official Discord and official X source profiles.
9. Create a qualified Medium publication profile without asserting corpus completeness.
10. Update relevant indexes and master timeline links.

## Allowed paths for implementation

```text
knowledge/
operations/campaigns/knowledge-generation-wave-2/
```

`archive/`, `archive/semantic/`, `graph/`, and `publication/` are prohibited implementation paths. Update them only in a later separately authorized campaign. This campaign creates human-first knowledge pages and their campaign records under the two allowed path roots above.

When evidence required for a page exists only on an unmerged PR, either stack explicitly on the narrowest evidence branch or defer the page. The default for Wave 2A is current `main`; do not stack on this planning branch.

Do not rewrite archive or semantic source evidence unless a genuine integrity defect is found and separately documented.

## Validation requirements

Validate:

- every page has required metadata;
- every material claim has at least one citation;
- every citation resolves;
- no R5 claim appears in knowledge;
- R4 pages have explicit approval evidence;
- current-state claims have `as_of` dates;
- provisional pages have `review_after` dates;
- lifecycle distinctions are not collapsed;
- Council claims remain attributed;
- announcement and release remain distinct;
- vote result and implementation remain distinct;
- event announcement and occurrence remain distinct;
- no duplicate canonical entity pages are introduced;
- index and cross-links resolve;
- no orphan pages exist;
- markdown lint and repository tests pass;
- `git diff --check` passes;
- working tree is clean;
- campaign summary reports pages by status and risk.

## Required campaign reports

```text
operations/campaigns/knowledge-generation-wave-2/execution/campaign-summary.md
operations/campaigns/knowledge-generation-wave-2/execution/campaign-summary.json
operations/campaigns/knowledge-generation-wave-2/execution/risk-register.md
operations/campaigns/knowledge-generation-wave-2/execution/validation-report.md
operations/campaigns/knowledge-generation-wave-2/execution/validation-report.json
operations/campaigns/knowledge-generation-wave-2/execution/research-gaps.md
```

Report:

- pages created;
- pages expanded;
- pages deferred;
- pages by knowledge status;
- pages by risk class;
- claims by source-authority class;
- unresolved contradictions;
- stale current-state claims;
- research gaps;
- validation results.

## Human review gate

After drafting and validation:

1. stop and leave the PR draft;
2. return the complete page list and risk classifications;
3. identify every R3 or R4 page;
4. identify every material contradiction;
5. identify every page relying on a single source;
6. identify every current-state page and its `as_of` date;
7. wait for semantic review.

Do not mark the PR ready and do not merge.

## Stop condition

Stop when the authorized wave has been drafted, validated, pushed, and opened as a draft PR. Return:

- branch and head SHA;
- PR URL;
- pages created and expanded;
- status and risk distributions;
- deferred pages and reasons;
- unresolved contradictions;
- validation status;
- confirmation that archive evidence was not rewritten and graph/publication were untouched.
