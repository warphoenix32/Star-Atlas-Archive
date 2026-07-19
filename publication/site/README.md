# Star Atlas Library front end

This folder contains the first visual front end for the Star Atlas Library. It is an intentionally isolated, dependency-free static site: the archive and knowledge layers remain canonical, while this surface provides a calm entrance into them.

## Experience contract

- The landing page is a cinematic threshold, not a dashboard.
- Search and the library dialog reveal repository knowledge only after a visitor chooses to explore.
- Repository knowledge remains source-linked; the front end does not silently rewrite or promote claims.
- The generated search index reads `knowledge/**/*.md`; every result opens in an internal Library reader while retaining a direct link to its canonical GitHub source path.
- The background image is a presentation asset. All text, controls, focus states, and responsive behavior are real HTML/CSS/JavaScript.

## Local development

From this directory:

```text
npm run index
npm run check
npm run dev
```

Then open `http://127.0.0.1:4173`.

No dependency installation is required.

## GitHub Pages

The `Publish Star Atlas Library` workflow validates the interface, copies the reviewed `knowledge/` tree into the static deployment artifact, and publishes it through GitHub Pages whenever relevant files reach `main`. The deployed reader never changes canonical knowledge: it renders a synchronized, source-linked copy and exposes the preserved GitHub file for every record.

The expected public address is:

`https://warphoenix32.github.io/Star-Atlas-Archive/`

## Vercel migration

The site is kept under one portable directory so it can later become the root of a dedicated Vercel project. For a future migration:

1. move or extract `publication/site/` into the dedicated website repository;
2. replace the current GitHub knowledge URLs with the website's internal content routes;
3. connect a reviewed content API or build-time knowledge adapter;
4. configure Vercel only in the dedicated website repository;
5. retain source IDs, provenance, and evidence status when rendering deeper pages.

No Vercel configuration or deployment is introduced in this repository yet.

## Asset provenance

`assets/library-portal.webp` is a project-bound visual generated with OpenAI's built-in image-generation workflow from the approved Star Atlas Library landing-page mock-up. The prompt requested a text-free, interface-free future-Hellenic library atrium with a celestial portal, centered negative space, dark stone, aged bronze, and restrained archival light.
