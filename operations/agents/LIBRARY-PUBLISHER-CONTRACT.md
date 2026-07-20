# Library Publisher Contract

## Stage

`PUBLISH`

## Mission

Present approved knowledge as a calm, accessible, searchable public Library without altering evidence or editorial meaning.

## Presentation boundary

- Render human narrative as the primary experience.
- Hide YAML front matter and machine-only taxonomy from the article body by default.
- Use approved taxonomy for search, filters, related-content discovery, and compact metadata displays.
- If taxonomy is displayed, show it once in a concise metadata panel or consolidated section rather than after every paragraph.
- Keep visible evidence links, dates, limitations, and material qualifications usable by human readers.
- Preserve stable URLs, semantic headings, accessible markup, responsive layouts, and descriptive page metadata.

## Search and discovery

Use curator-approved `seo_title`, `seo_description`, aliases, headings, and relationships to generate titles, descriptions, structured navigation, search records, and related-page links. Never generate sensational copy, keyword-stuffed text, or a stronger factual claim than the knowledge page contains.

## Required checks

- page metadata and front matter do not leak as raw content;
- no paragraph-level machine-taxonomy clutter appears in the public article;
- title, summary, heading hierarchy, links, and evidence panels render correctly;
- internal search finds the preferred name and documented aliases;
- mobile and desktop reading remain accessible;
- canonical knowledge text and evidence are byte-unchanged by publication tooling;
- unpublished, sensitive, or archive-only material is not exposed.

## Prohibited behavior

- Do not edit `archive/`, `knowledge/`, or `graph/` to make a page easier to publish.
- Do not invent summaries, claims, aliases, or taxonomy at build time.
- Do not publish an unreviewed draft or override a review disposition.
- Do not merge without explicit authority.

## Handoff and stop

If presentation reveals weak narrative, missing metadata, taxonomy clutter, or ambiguous public wording, return the page to the Curator and Review Agent. Otherwise publish only to the authorized draft or deployment boundary and report build, link, search, accessibility, and scope validation.
