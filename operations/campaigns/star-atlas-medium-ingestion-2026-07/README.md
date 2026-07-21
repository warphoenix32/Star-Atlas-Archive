# Official Star Atlas Medium Ingestion Campaign

This campaign preserves written stories belonging to the official **Star Atlas** Medium publication. It is an archival ingestion campaign only: it does not create semantic candidates or modify `knowledge/`, `graph/`, or `publication/`.

## Workflow

Run from the repository root:

```powershell
python operations/campaigns/star-atlas-medium-ingestion-2026-07/medium_campaign.py discover
python operations/campaigns/star-atlas-medium-ingestion-2026-07/medium_campaign.py adjudicate
python operations/campaigns/star-atlas-medium-ingestion-2026-07/medium_campaign.py retrieve
python operations/campaigns/star-atlas-medium-ingestion-2026-07/medium_campaign.py validate
python operations/campaigns/star-atlas-medium-ingestion-2026-07/medium_gate.py audit
python operations/campaigns/star-atlas-medium-ingestion-2026-07/medium_gate.py determinism
python operations/campaigns/star-atlas-medium-ingestion-2026-07/medium_gate.py validate
```

Install the campaign-local Python dependencies first:

```powershell
python -m pip install -r operations/campaigns/star-atlas-medium-ingestion-2026-07/requirements.txt
```

The direct collector uses Beautiful Soup. Rendered discovery and retrieval fallback use the campaign-local `medium_browser.js` helper with Playwright. Set `MEDIUM_NODE` when `node` is not on `PATH`, `NODE_PATH` when Playwright is installed in a nonstandard package directory, and `MEDIUM_CHROME` when Chrome is not installed in a standard Windows location.

## Command boundaries

- `discover` queries every year from 2020 through the current UTC year, captures discovery surfaces, reconciles repository/social/archive leads, probes publication identity, and writes a frozen disposition manifest. It does not download article media or generate Source Records.
- `adjudicate` resolves obvious assets, navigation, unrelated accounts, and duplicate URL variants from the frozen candidate set, while explicitly deferring genuine unresolved article leads with the exact artifact and action needed. It performs no network retrieval.
- `retrieve` reads only the frozen manifest. Successful articles receive immutable HTML, normalized JSON and Markdown, paired Source Records, schema-v2.1 ingestion packages, and URL-only media manifests.
- `validate` checks disposition completeness, stable IDs, artifact parity, provenance, checksums, relative links, UTF-8/JSON validity, deterministic normalized output, and prohibited-path scope.

## Inclusion boundary

An article is included only when captured article metadata establishes membership in the official `Star Atlas` publication. The actual author is preserved separately from the publisher. Reposts, responses, comments, activity events, recommendations, unrelated Medium accounts, and navigation surfaces remain visible in the exclusion or manual-review ledgers.

Publication/profile URLs that resolve to one Medium post ID are one article with multiple observed URLs. Live, RSS, and archived-snapshot evidence remain separate provenance tiers.

## Stable identifiers

The preferred identifier is:

```text
SRC-MEDIUM-STARATLAS-{MEDIUM_POST_ID_UPPER}
```

When no Medium post ID is recoverable, the suffix is the first 16 uppercase hexadecimal characters of the canonical-URL SHA-256 and the record requires manual review.

## Text-only operator scope

The operator narrowed this campaign to text-only ingestion after the initial retrieval checkpoint. Article images are not downloaded or committed. Image and embed URLs may remain in normalized metadata to preserve placement and provenance, but no media binaries are part of the campaign.

## Retrieval tiers

1. Live direct HTML with structured metadata and complete article DOM.
2. Live Playwright-rendered DOM when direct HTML is incomplete.
3. RSS `content:encoded` only when completeness is demonstrable.
4. Public archived snapshot when the live article is unavailable.

The selected tier and every attempted tier are retained. Evidence from different tiers is never silently merged.

## Completeness limits

Ingestion and exact raw-to-normalized full-body auditing are complete for the 181 confirmed official-publication articles in the frozen included set. The completion gate has no pending human-adjudication items. Four historical Medium shortlinks remain documented as terminal external-evidence gaps because neither their live Branch pages nor public archive indexes expose a surviving target.

Publication-level discovery remains incomplete: Medium's historical surfaces are non-exhaustive, so the campaign does not assert that undiscoverable or deleted stories never existed. The bounded gate status is `COMPLETE_WITH_DOCUMENTED_EXTERNAL_EVIDENCE_GAPS`; a bare corpus-level `COMPLETE` label is not used.

The collector queried the 2020 publication surfaces. No 2020 Star Atlas publication article was confirmed or included; preserved coverage begins with the earliest confirmed 2021 article rather than implying 2020 article coverage.

Medium RSS is recent-item oriented and is not the completeness authority. Current publication pages may omit deleted, moved, or unlisted stories. Repository Discord/X records and public web-archive indexes are therefore discovery sources, not independent proof of publication authorship or article publication dates.

See [completion-gate-report.md](completion-gate-report.md), [full-body-audit.md](full-body-audit.md), and [completion-gate-validation.md](completion-gate-validation.md) for the closed candidate ledger, full-text verification, and final gate result.

See [upstream-scraper-assessment.md](upstream-scraper-assessment.md) for the decision not to use the 2018 tag scraper.
