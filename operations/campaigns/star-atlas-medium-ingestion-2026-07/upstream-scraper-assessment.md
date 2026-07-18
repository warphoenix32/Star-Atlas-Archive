# Upstream Scraper Assessment

## Evaluated project

- Project: `harrisonjansma/Medium_Scraper`
- Evaluated revision: `1ec9652beca595f70c42a91f5c5579465c47dac3`
- License: Apache-2.0
- Operational disposition: **NOT ADOPTED**

## Findings

The project was designed for Medium tag-archive research rather than publication preservation. Its master script walks daily `/tag/{tag}/archive/{date}` pages, and its scraper exports story-card metadata such as title, subtitle, author, reading time, claps, and URL. It does not preserve complete article bodies or article media.

The implementation also depends on Selenium, a separately managed ChromeDriver, and generated Medium CSS selectors from the 2018 site. Those selectors are not a durable interface for the current Medium application.

## Replacement decision

This campaign uses a publication-native collector instead:

1. Discover the official Star Atlas publication through year archives, publication/profile pages, RSS, sitemaps, repository evidence, official social links, and web-archive indexes.
2. Deduplicate by Medium post ID while preserving every observed URL and referrer.
3. Freeze the classified URL manifest.
4. Retrieve complete article text evidence from that manifest; preserve image/embed URLs without downloading binaries.
5. Use direct HTTP and semantic metadata first, with Playwright only for rendered pagination or article fallback.

The upstream project is documented as an evaluated alternative. No upstream code is vendored and the campaign has no runtime dependency on it.
