# Legacy Written Raw Recovery — Phase 2 Aephia and HNN Gates

## Purpose

Campaigns Alpha through Delta preserved 800 successful written-source extractions and their Source Records, but most of those campaigns did not preserve the immutable HTTP response that underlay each extraction. This campaign uses bounded, explicitly authorized batches rather than enabling corpus-wide acquisition.

The existing extraction and Source Record layers remain frozen. Recovery adds only exact public HTTP response bytes and provenance. It does not re-extract, normalize, classify, semantically enrich, or promote knowledge.

## Scope

The freeze inventory contains:

| Campaign | Source family | Successful records |
|---|---|---:|
| Alpha | Aephia | 64 |
| Bravo | Intergalactic Herald | 259 |
| Charlie | Hologram News Network | 157 |
| Delta | Official Star Atlas web corpus | 320 |
| **Total** |  | **800** |

The retrieval pilot was limited to 20 curator-selected records: five from each source family. The first post-pilot gate recovered the 59 remaining Aephia records. The HNN gate recovered 156 records: 152 non-pilot records and four pilot exceptions that previously lacked raw bodies. One HNN pilot snapshot remains the verified baseline, producing complete 157-record family coverage. Intergalactic Herald remains excluded by operator direction, and official-source expansion remains a later gate. Full-corpus retrieval is intentionally unavailable.

## Commands

Run from the repository root:

```text
python operations/campaigns/legacy-written-raw-recovery-2026-07/recovery_campaign.py freeze
python operations/campaigns/legacy-written-raw-recovery-2026-07/recovery_campaign.py retrieve --pilot
python operations/campaigns/legacy-written-raw-recovery-2026-07/recovery_campaign.py retrieve --batch aephia-family-remaining-59
python operations/campaigns/legacy-written-raw-recovery-2026-07/recovery_campaign.py retrieve --batch hnn-written-family-completion-156
python operations/campaigns/legacy-written-raw-recovery-2026-07/recovery_campaign.py validate
```

`freeze` reads only the existing extraction JSON and deterministically writes `frozen-manifest.json`, `expansion-aephia-selection.json`, and `expansion-hnn-selection.json`. It requires exactly 64 Alpha, 259 Bravo, 157 Charlie, and 320 Delta records. The Aephia selection remains fixed at its 59 non-pilot WordPress API records. The HNN selection includes every HNN Source ID except the one verified pilot snapshot already preserved.

`retrieve --pilot` performs the already completed 20-record pilot. The two `--batch` values are fixed allowlisted selections and cannot accept arbitrary families or Source IDs. Aephia uses its frozen public WordPress endpoints. HNN reuses 74 exact prior Wayback requests and resolves 82 Medium-hosted records—including four pilot repairs—to the earliest discoverable public 200-status HTML snapshot. The resolution ledger remains separate from the raw evidence and records the chosen timestamp, digest, index checksum, and any missing snapshot. Of the 156 completion records, 144 were recovered from exact Wayback snapshots. The 12 Medium records with no public archive snapshot were recovered from their current public, unauthenticated full-article pages using a campaign-local curl transport fallback; their missing-snapshot state remains explicit in the resolution ledger. All retrieval uses unauthenticated public HTTP with pacing, checkpoint reuse, three attempts, and the existing host stop rule.

Every terminal result is checkpointed. A normal rerun reuses both successful captures and documented access/failure outcomes without changing timestamps or ledgers. A later operator may explicitly use `--retry-failures` after the blocking condition changes; that option is not part of deterministic CI.

`validate` checks the fixed point of all selections, extraction checksums, Source Record references, immutable pilot baselines, exact Aephia and HNN family coverage, Wayback carrier resolution, full-article signals for the bounded Medium live fallbacks, stable Medium post-ID redirects, terminal dispositions, raw-body checksums, provenance reconciliation, manual-review routing, orphan detection, and repository path boundaries.

CI may invoke the equivalent thin offline entry point:

```text
python operations/campaigns/legacy-written-raw-recovery-2026-07/validate_campaign.py
```

Validation performs no HTTP requests.

## Recovery output

Successful retrievals preserve:

```text
archive/raw/legacy-written-recovery/<source-family>/<source-id>/
└── response-body.bin

archive/provenance/legacy-written-recovery/<source-family>/
└── <source-id>.json
```

`response-body.bin` is the exact byte stream returned by the public endpoint. Its generic extension is deliberate: content type is recorded in provenance and no transformation is applied to the bytes.

Each provenance record includes:

- frozen Source ID and source family;
- request URL and its selection basis;
- capture timestamp and user agent;
- HTTP status, selected response headers, final URL, and redirect chain;
- content type, byte length, and SHA-256;
- observed canonical URL or document title when exposed by HTML or JSON;
- explicit identity comparison against the frozen source URL;
- terminal disposition and manual-review status.

Campaign-local ledgers include:

- `frozen-manifest.json`;
- `retrieval-ledger.jsonl`;
- `retry-ledger.jsonl`;
- `manual-review-queue.jsonl`;
- `expansion-aephia-selection.json`;
- `expansion-aephia-retrieval-ledger.jsonl`;
- `expansion-aephia-retry-ledger.jsonl`;
- `expansion-aephia-manual-review-queue.jsonl`;
- `expansion-hnn-selection.json`;
- `expansion-hnn-archive-resolution-ledger.jsonl`;
- `expansion-hnn-retrieval-ledger.jsonl`;
- `expansion-hnn-retry-ledger.jsonl`;
- `expansion-hnn-manual-review-queue.jsonl`;
- campaign summary JSON and Markdown;
- validation report JSON and Markdown.

## Identity and retrieval rules

Recovery does not assume that a successful HTTP response is the intended publication. A response is identity-matched only when its canonical/final identity agrees with the frozen source, when a preserved Internet Archive capture explicitly contains the expected origin, or when the original and observed Medium URLs expose the same stable 12-character post ID. Medium post-ID matches are recorded as `CONSISTENT` publication-path changes rather than exact URL matches. Responses lacking enough identity metadata are preserved but receive `AMBIGUOUS_MANUAL_REVIEW`; mismatches are never silently accepted.

Redirects, mirrors, WordPress APIs, successor HNN locations, and archived snapshots remain distinct provenance surfaces. Recovery does not merge their identities.

The checkpoint is a body plus provenance file whose Source ID and SHA-256 reconcile. A later pilot rerun reuses such a checkpoint without changing the capture timestamp or downloading the body again. Failed records receive a terminal failure ledger entry and remain visible for review.

## Protected boundaries

This campaign may write only:

```text
archive/raw/legacy-written-recovery/
archive/provenance/legacy-written-recovery/
archive/manifests/legacy-written-raw-recovery-2026-07.json
operations/campaigns/legacy-written-raw-recovery-2026-07/
```

It must not modify:

```text
archive/normalized/
archive/source-records/
archive/semantic/
knowledge/
graph/
publication/
```

No recovered body is promoted merely because it was retrieved. The pilot measured recoverability, identity confidence, redirect behavior, and manual-review burden. The Aephia and HNN families remain independent reviewable gates; Intergalactic Herald is excluded and the official family remains a later Phase 2 decision.
