# Phase 5 Foundational Publication Portfolio

Campaign ID: `phase-5-foundational-publication-portfolio-2026-07`

This campaign began with eleven draft articles and now implements the
operator-approved reader-first redesign. Human semantic review and publication
authorization are complete for Editorial Wave 1: seven articles are
`PUBLISHED` and seven prototypes remain `DRAFT`.

## Scope

- Preserve fourteen reader-facing articles and prototypes while publishing only
  the seven explicitly authorized Wave 1 articles.
- Define eight reader gateways and a thirty-page foundational narrative map.
- Apply an HNN-influenced, player-friendly editorial house style without
  inheriting unsupported speculation or promotional certainty.
- Inventory which planned pages can be drafted from reviewed Knowledge and
  which require targeted Knowledge development.
- Record deterministic dispositions for every prototype.
- Preserve the distinction between Archive, Knowledge and Publication.
- Populate the publication manifest with deterministic `DRAFT` and `PUBLISHED`
  entries.
- Record the operator's July 24, 2026 approval against the reviewed commit.
- Record the operator's separate July 24, 2026 publication authorization.
- Keep all seven remaining drafts outside the public build.
- Hide internal taxonomy and workflow metadata from article prose and remove
  top-of-page metadata boxes from the public Knowledge reader.
- Preserve human portfolio, semantic, narrative, SEO and comprehensiveness
  review as a completed, auditable gate.

No Archive evidence, canonical Knowledge or graph fact may change. The public
site may expose only entries whose manifest state is `PUBLISHED`.
Intergalactic Herald is not a central narrative source or profile in this
initial portfolio.

## Planning artifacts

- `publication-plan.json` — eight gateways, thirty foundational pages, deeper
  dossier series and research collections.
- `audience-navigation-map.md` — human-readable information architecture.
- `knowledge-readiness-audit.json` and `.md` — page-level readiness and
  supporting Knowledge.
- `targeted-knowledge-backlog.json` and `.md` — only the promotion work needed
  to support the planned Library.
- `prototype-dispositions.json` and `.md` — merge, split, rewrite or research
  disposition for all eleven prototypes.
- `EDITORIAL-HOUSE-STYLE.md` — the HNN-influenced Library voice and public
  metadata rules.

## Deterministic commands

```text
python operations/campaigns/phase-5-foundational-publication-portfolio-2026-07/build_campaign.py
python operations/campaigns/phase-5-foundational-publication-portfolio-2026-07/validate_campaign.py origin/main
python -m unittest discover operations/tests/phase5_publication_portfolio
```

`build_campaign.py` recalculates canonical UTF-8/LF content checksums, the
internal publication manifest and campaign summary. Line-ending normalization
keeps article identities deterministic across Windows and Linux checkouts.
`validate_campaign.py` checks article structure, front matter, knowledge inputs,
the complete publication plan, readiness and backlog reconciliation, prototype
dispositions, manifest state, hidden public metadata, community evidence limits
and protected paths.

## Completed gates

The editorial review gate and the separate publication-authorization gate are
complete. Seven articles enter the governed public build; seven drafts remain
excluded. Automated checks validate both records but cannot create or replace
either human decision.
