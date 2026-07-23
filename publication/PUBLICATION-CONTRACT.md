# Star Atlas Library Publication Contract

## Purpose

The publication layer is the reader-facing editorial product of the Star Atlas
Archive. It presents approved knowledge as clear, engaging, evidence-qualified
narrative without exposing repository mechanics as the primary reading
experience.

This contract keeps the three products distinct:

```text
Archive evidence -> reviewed Knowledge -> reader-facing Publication
```

The Archive proves what was preserved. Knowledge records the best reviewed
institutional understanding. Publication teaches that understanding to a public
audience. Publication cannot create facts, silently resolve conflicts, or
rewrite either upstream layer.

## Publication boundary

Publication may:

- synthesize one or more approved knowledge pages into a coherent narrative;
- improve structure, transitions, definitions, accessibility, and search
  metadata;
- present citations and provenance through human-readable evidence panels;
- consolidate taxonomy into front matter, a glossary, or a single reference
  section;
- link readers to deeper Knowledge and Archive material.

Publication may not:

- use raw or normalized archive artifacts as its only editorial source;
- promote a semantic candidate merely because it exists;
- change a claim's lifecycle, authority, confidence, or temporal scope;
- convert an announcement into a release, a vote into implementation, or a
  plan into delivery;
- infer speaker identity, ownership, outcome, payment, or execution;
- hide a material conflict or current-state limitation;
- modify `archive/`, `knowledge/`, or `graph/`.

## Reader experience

Published pages follow a human-first standard. They should orient a new reader,
tell a coherent historical or institutional story, explain why the subject
matters, and make uncertainty understandable without forcing the reader to
decode internal labels.

Every published narrative should provide:

1. an accurate title and concise opening;
2. scope and terminology;
3. connected chronology or lifecycle;
4. significance and relationships;
5. a date-scoped current state when supportable;
6. material conflicts, limitations, and open questions;
7. related reading;
8. a human-readable evidence panel.

Search metadata must be descriptive rather than promotional. SEO titles and
descriptions should identify the subject, Star Atlas context, and historical
value without keyword stuffing.

## Internal metadata visibility

Repository metadata remains available for auditing but is not repeated through
the public narrative.

- Source IDs may appear in a collapsible evidence panel or researcher view, not
  as paragraph prefixes.
- Campaign IDs, schema versions, confidence codes, workflow states, and
  machine-only taxonomy are hidden from the article body.
- Taxonomy is consolidated at the top, bottom, or hidden in the public view.
- Plain-language qualifications remain visible wherever they affect meaning.
- A publication page may link to Knowledge and Archive views without presenting
  those internal structures as the main Library experience.

## Manifest

The internal publication manifest is
[`manifests/publication-manifest.json`](manifests/publication-manifest.json).
It conforms to
[`operations/schema/PUBLICATION-MANIFEST-v1.schema.json`](../operations/schema/PUBLICATION-MANIFEST-v1.schema.json).

The manifest is a controlled publication ledger, not a knowledge database. Each
entry binds a stable public identity and slug to:

- one publication artifact;
- one or more reviewed Knowledge inputs;
- editorial, evidence, review, and presentation states;
- a date-scoped provenance snapshot;
- public metadata and internal-field visibility rules.

The checked-in manifest is internal. A future site build may generate a reduced
public index containing only approved human-readable fields. The public index
must never become the repository source of truth.

## Entry states

| State | Meaning | Public build |
| --- | --- | --- |
| `PLANNED` | Portfolio candidate; no publication artifact required. | Excluded |
| `DRAFT` | Narrative exists but has not passed review. | Excluded |
| `IN_REVIEW` | Editorial and evidence review is active. | Excluded |
| `APPROVED` | Human approval is recorded and the artifact is release-ready. | Excluded until explicitly published |
| `PUBLISHED` | Approved artifact is eligible for the public build. | Included |
| `WITHDRAWN` | Entry was removed before or after publication with reason retained. | Excluded |
| `ARCHIVED` | Superseded publication remains historically traceable. | Excluded from default discovery |

Only `PUBLISHED` entries are included in the default public build. Approval and
publication remain separate actions.

## Entry requirements

Every non-planned entry must have:

- a unique `PUB-*` identifier and unique slug;
- a publication artifact under `publication/`;
- at least one existing source path under `knowledge/`;
- an `as_of` date for the narrative's evidence horizon;
- SEO title, description, and public excerpt;
- editorial and evidence review states;
- human-readable provenance and evidence-panel policies;
- explicit taxonomy and internal-field visibility settings.

An `APPROVED` or `PUBLISHED` entry additionally requires:

- editorial review status `APPROVED`;
- citation resolution and evidence-boundary checks to pass;
- all current-state dates to be present;
- all material conflicts to be disclosed;
- a human approval record;
- a content checksum and knowledge-input revision.

## Deterministic behavior

The manifest is ordered by `publication_id`. IDs and slugs are never recycled.
Related publication IDs must resolve within the manifest. Generated public
indexes sort by featured rank, title, and publication ID. A repeated build from
the same manifest and publication artifacts must produce identical output.

## Lifecycle and corrections

Published prose is not silently overwritten when a correction changes material
meaning. The entry retains revision history, prior publication date, correction
reason, and supersession relationship. Minor grammar or accessibility repairs
may update in place when they do not alter claims.

`WITHDRAWN` and `ARCHIVED` records remain in the internal manifest. Their public
URLs should resolve to a plain-language status notice or a documented
replacement rather than disappearing without explanation.

## Evidence and authority

Publication inherits authority and limitations from Knowledge. It must preserve:

- proposal, vote, passage, authorization, payment, implementation, and
  independent verification as distinct states;
- announcement, testing, release, feature completeness, and delivery as
  distinct states;
- source-native claims, community interpretation, curator adjudication, and
  derived inference as distinct forms of evidence;
- current and historical states with explicit dates.

A publication may simplify wording, but not the evidence boundary.

## Validation and approval

Automated validation checks paths, IDs, slugs, checksums, state requirements,
cross-links, deterministic order, and internal-field policies. Automation does
not approve editorial judgment.

The Library Publisher may assemble and validate a draft portfolio. It may not:

- approve its own R3 or R4 interpretation;
- repair weak Knowledge by inventing stronger wording;
- bypass human approval;
- publish directly from Archive or semantic artifacts.

## Current transition

Phase 3 defines this contract and an empty, valid manifest. It does not create
public articles or change the existing GitHub Pages build. Phase 4 will
consolidate Knowledge and select evidence-supported dossiers. Phase 5 will
populate the initial publication portfolio and connect the public build to
approved manifest entries.
