# Knowledge Generation Wave 2

## Mission

Expand the human-first canonical knowledge layer using the archive and semantic evidence already acquired across official websites, PIPs, Council records, Discord announcements, social media, transcripts, economic reports, technical inventories, and reviewed community sources.

This planning branch defines campaign scope, risk tolerance, page portfolio, review gates, and the later Codex execution contract. It does not itself promote claims into `knowledge/`, `graph/`, or `publication/`.

## Operating model

- Chief of Staff / Institutional Knowledge Curator owns meaning, page authorization, evidence interpretation, risk classification, contradiction resolution, and final promotion approval.
- Codex owns bulk repository execution, evidence-packet assembly, page drafting, front matter, citations, indexes, cross-links, validation, and revision application.
- Canonical promotion remains review-gated.

Workflow:

1. Inventory existing knowledge coverage and promotion candidates.
2. Resolve candidate pages against this approved portfolio.
3. Assemble claim-level evidence packets.
4. Draft pages with explicit epistemic status.
5. Run structural, citation, lifecycle, duplication, and contradiction validation.
6. Submit draft pages for semantic review.
7. Apply review corrections.
8. Promote only approved pages.

## Campaign objective

Target 45–65 new pages or substantive expansions while increasing useful coverage without collapsing uncertainty.

Expected portfolio:

- 35–45% `CANONICAL`
- 30–40% `QUALIFIED`
- 15–25% `PROVISIONAL`
- 5–10% `HISTORICAL` or research-facing synthesis
- 0% archive-only claims promoted as knowledge

## Required page metadata

Every new or substantially revised page must include:

```yaml
knowledge_status: CANONICAL | QUALIFIED | PROVISIONAL | HISTORICAL
as_of: YYYY-MM-DD
confidence: HIGH | MEDIUM | LOW
evidence_basis:
  - source IDs or stable repository paths
known_limitations:
  - explicit limitations
research_gaps:
  - unresolved questions
review_after: YYYY-MM-DD | null
```

## Non-negotiable distinctions

- proposal is not a vote;
- passed is not implemented;
- announcement is not release;
- roadmap is not delivery;
- Council-reported outcome is not independent verification;
- historical state is not current state;
- attributed interpretation is not fact;
- unresolved contradiction must remain visible;
- unknown speaker identity must remain unknown;
- accusation or reputational claim requires exceptionally strong evidence.

## Campaign documents

- `generation-plan.md` — authorized portfolio and sequencing
- `risk-assessment-matrix.md` — claim and page risk scoring
- `codex-execution-contract.md` — later execution instructions and stop conditions

## Current dependency posture

PR #12 and PR #13 remain open semantic-enrichment inputs. This planning PR may merge independently because it changes only campaign framework files. The later knowledge-generation implementation branch must inventory the merged state of `main` and any still-open semantic PRs before execution, and must not silently depend on unmerged evidence.