# build-staratlas README

## Metadata

- Source ID: `SRC-OFF-A51F2D22DAE3C382`
- URL: https://github.com/staratlasmeta/build-staratlas#readme
- Publication date: 2026-04-10T06:40:03Z
- Updated date: 2026-04-16T16:32:44Z
- Original date text: 2026-04-10T06:40:03Z
- Author: ATMTA / Star Atlas official publisher
- Publisher: staratlasmeta GitHub organization
- Document classification: `TECHNICAL_DOCUMENTATION`
- Extraction confidence: `HIGH`

## Official Authority Boundary

This record establishes what the named official publisher publicly stated and when. It does not by itself prove execution, independent economic accuracy, historical completeness, or absence of contrary evidence.

## Archival Abstract

Official technical documentation titled “build-staratlas README.” This record preserves what staratlasmeta GitHub organization publicly stated at the recorded publication time; claims about delivery, economics, or outcomes remain limited to the wording of the source.

## Products

- ATLAS

## Actors and Organizations

- None identified.

## Governance

- None identified.

## Lore

- None identified.

## Classified Claims

- # Star Atlas Build Docs  Official VitePress source for [build.staratlas.com](https://build.staratlas.com).
- ## Source of truth  This repository is the canonical home for the Star Atlas Build docs.
- Updates should be made directly in this repo and deployed through GitHub Pages.
- GitHub Actions builds and deploys the VitePress output.
- GitHub Pages serves the site at `build.staratlas.com`.
- ## Custom domain notes  This repo already ships `docs/public/CNAME` with:  ```txt build.staratlas.com ```  Typical DNS setup:  - `CNAME` record for `build` pointing to your GitHub Pages host, or - the equivalent records recommended by GitHub for your org or user setup  After DNS changes, re-save the custom domain in GitHub Pages settings if GitHub asks for confirmation.
- ## Preview and path assumptions  The config is tuned for the final custom domain at the site root.
- If you want to preview the built site under a temporary GitHub Pages subpath, adjust the VitePress `base` setting first.

## Official Cross-References

- None identified.

## Temporal Validity

- Status: `CURRENT_DOCUMENTATION`
- Current validity: `CURRENT_PAGE_NOT_HISTORICAL_PROOF`
- Warning: Official publication does not independently prove successful execution, completeness, or continued current validity.

## Open Questions

- Which claims are independently corroborated or later superseded?

## Preserved Official Text

# Star Atlas Build Docs

Official VitePress source for [build.staratlas.com](https://build.staratlas.com).

## Source of truth

This repository is the canonical home for the Star Atlas Build docs.
Updates should be made directly in this repo and deployed through GitHub Pages.

## What this repo includes

- VitePress site scaffold with a dark, Star Atlas-inspired theme
- Markdown docs maintained directly in this repository
- Generated sidebar and top navigation
- GitHub Pages deployment workflow
- `CNAME` support for `build.staratlas.com`
- A lightweight redirect strategy for common legacy URL variants like `.md`

## Quick start

```bash
npm install
npm run dev
```

## Scripts

- `npm run dev` - start the local VitePress dev server
- `npm run build` - build the static site
- `npm run preview` - preview the production build locally

## Publishing on GitHub Pages

1. Push changes to `main`.
2. GitHub Actions builds and deploys the VitePress output.
3. GitHub Pages serves the site at `build.staratlas.com`.

## Custom domain notes

This repo already ships `docs/public/CNAME` with:

```txt
build.staratlas.com
```

Typical DNS setup:

- `CNAME` record for `build` pointing to your GitHub Pages host, or
- the equivalent records recommended by GitHub for your org or user setup

After DNS changes, re-save the custom domain in GitHub Pages settings if GitHub asks for confirmation.

## Preview and path assumptions

The config is tuned for the final custom domain at the site root. If you want to preview the built site under a temporary GitHub Pages subpath, adjust the VitePress `base` setting first.

