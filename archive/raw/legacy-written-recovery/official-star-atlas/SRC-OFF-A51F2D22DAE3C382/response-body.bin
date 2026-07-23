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
