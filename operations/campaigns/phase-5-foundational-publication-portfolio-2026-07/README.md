# Phase 5 Foundational Publication Portfolio

Campaign ID: `phase-5-foundational-publication-portfolio-2026-07`

This campaign began with eleven draft articles and now implements the
operator-approved reader-first redesign. The original drafts remain unpublished
prototypes while the campaign defines the complete navigation, foundational
portfolio, editorial house style, Knowledge-readiness audit and targeted
development backlog.

## Scope

- Preserve eleven reader-facing prototypes without publishing them.
- Define eight reader gateways and a thirty-page foundational narrative map.
- Apply an HNN-influenced, player-friendly editorial house style without
  inheriting unsupported speculation or promotional certainty.
- Inventory which planned pages can be drafted from reviewed Knowledge and
  which require targeted Knowledge development.
- Record deterministic dispositions for every prototype.
- Preserve the distinction between Archive, Knowledge and Publication.
- Populate the publication manifest with deterministic `DRAFT` entries.
- Keep all drafts outside the public build.
- Hide internal taxonomy and workflow metadata from article prose and remove
  top-of-page metadata boxes from the public Knowledge reader.
- Require human portfolio, semantic, narrative, SEO and comprehensiveness
  review.

No Archive evidence, canonical Knowledge or graph fact may change. The only
site change permitted in this planning gate is removal of the public metadata
box.
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

## Stop gate

The current gate stops after the portfolio map and readiness audit are
validated. Automated checks cannot approve editorial judgment. A human must
review the eight gateways, thirty planned pages, prototype dispositions and
house style before targeted Knowledge development and redrafting proceed.
