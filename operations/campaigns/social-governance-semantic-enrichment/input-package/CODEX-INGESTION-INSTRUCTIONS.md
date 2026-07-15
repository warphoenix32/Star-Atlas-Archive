# Codex Ingestion Handoff

Ingest this package into `warphoenix32/Star-Atlas-HNN-Archive`.

## Social media

Preserve the raw CSV, normalized JSONL/Markdown, individual source records, and manifest under campaign-specific archive and operations paths. Reconcile post IDs and URLs against existing records. Preserve the three documented duplicate export rows without creating duplicate source records.

Retweets must remain marked as reshared context and must not be treated automatically as first-party claims.

## Governance

Ingest the PIP 1–33 URL/UUID seed registry into archive and operations layers. Prepare a follow-on capture campaign for each official proposal page. Capture, when retrievable:

- PIP number and UUID
- title and author
- full proposal text
- publication and voting dates
- requested authority or funding
- vote totals and quorum
- result
- execution evidence
- checksum and capture timestamp

Keep proposal, voting, approval, and execution as separate states.

## Scope

Allowed: `archive/` and `operations/campaigns/`.

Prohibited: `knowledge/`, `graph/`, and `publication/`.

Run count, checksum, JSON, URL, source-ID, and link validation. Open a draft PR and stop.
