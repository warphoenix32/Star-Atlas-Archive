---
title: "Atlas Brew History"
knowledge_status: QUALIFIED
as_of: 2026-07-17
confidence: MEDIUM
page_risk_score: 7
page_risk_class: R3
evidence_basis:
  - "archive/source-records/atlas-brew-combined/source-records.json"
  - "archive/semantic/atlas-brew/video-index.json"
  - "archive/source-records/campaign-delta-official/SRC-OFF-2E4DE78B3C355FA9.md"
known_limitations:
  - "The 123-source transcript package lacks publication dates, original URLs, and resolved speaker labels."
  - "Episode numbering contains duplicates, gaps, and non-monotonic source order."
research_gaps:
  - "Recover a complete official episode ledger, original recordings, dates, hosts, guests, and replay provenance."
  - "Re-review high-value semantic segments under the newer selective candidate methodology."
review_after: 2026-10-17
---

# Atlas Brew History

Atlas Brew is an official team-hosted community discussion format documented in 2022 as a weekly live Discord audio chat for questions, theorycrafting, product discussion, and community updates. The repository preserves a large transcript corpus, but not a complete or reliably dated episode history.

## Institutional identity and cadence

*Atlas Star Issue #10*, published 2022-08-26, calls Atlas Brew a weekly community event and lists episodes #23 through #26. The Breakpoint roadmap publication of 2022-11-07 describes a live Discord audio chat on Wednesdays at 3 PM ET. A January 2023 retrospective reports 44 theorycrafting sessions without a missed week since the event began, but does not establish the founding date. [Weekly-event record](../../archive/source-records/campaign-delta-official/SRC-OFF-2E4DE78B3C355FA9.md) [Format record](../../archive/source-records/campaign-delta-official/SRC-OFF-22181D98D7A1B870.md) [Retrospective](../../archive/source-records/campaign-delta-official/SRC-OFF-4A9FCC4E28487231.md)

Later official newsletters bracket episode groups #46–50, #59–62, and #64–68 in early and mid-2023. Those references help recover chronology but do not substitute for original episode pages.

## Preserved corpus

The combined package contains 123 source records, 198,558 caption lines, and 4,937 semantic segments. Titles span episode labels #8 through #196, but only 120 episode numbers are unique; #10 and #73 are duplicated, one record is unnumbered, numerous episode numbers are absent, and file/source order is not chronological.

Every source record lacks a publication date and original URL. The publisher field states “Star Atlas community event; rebroadcast source not established by transcript.” All segment speaker labels are `UNKNOWN`.

| Evidence anchor | What it supports | What remains unresolved |
|---|---|---|
| `SRC-ATLAS-BREW-0017`, 00:02:17–00:02:23 | Unknown speaker describes Brew as a main Wednesday Star Atlas event | Speaker, date, original recording |
| `SRC-ATLAS-BREW-0043`, 00:02:38–00:03:09 | Episode #100 introduction and co-host discussion | Exact event date and host identities |
| `SRC-ATLAS-BREW-0034`, 00:02:33–00:04:33 / `SEG-ATLAS-BREW-0034-0002` | Guest introduction and SAGE discussion | Named-speaker attribution is not normalized |
| `SRC-ATLAS-BREW-0101`, 00:02:35–00:06:35 and 00:38:07–00:39:04 | C4 design and Q&A discussion | Institutional authority and speaker identity |
| `SRC-ATLAS-BREW-0120` | Highest preserved episode label, #196 | Publication date; not the final source in file order |

## Semantic-layer boundary

The Atlas Brew semantic layer retains all 4,937 segments but is highly permissive: it produces thousands of promotion and timeline candidates, labels all speakers unknown, and marks every segment with a research-gap classification. Candidate existence is not promotion authority. Claims require exact transcript review, source/date recovery where material, and corroboration appropriate to the claim state.

## Event origin, recording, and replay

Atlas Brew’s official team-hosted event identity must remain separate from recording and rebroadcast identity. Intergalactic Herald frequently points to Star Atlas TV/VBTV replays. A replay preserves access but does not transfer authorship of the event or statements. Future records should capture event organizer, host, guest, original platform, recording publisher, replay publisher, and transcript source separately.

## Historical role

Atlas Brew functions as an institutional interpretation layer between formal announcements and community understanding. It can preserve early product discussion, design rationale, governance explanation, community feedback, and retrospective statements. Its conversational nature also makes roadmap language, speculation, questions, and unattributed claims especially easy to over-promote.

## Missing artifacts

Required recovery includes original URLs and video IDs, event and upload dates, complete episode numbers and titles, host/guest rosters, speaker diarization, descriptions, chapters, replay lineage, edited versions, and corrections. Duplicate #10/#73 and conflicting later episode labels must be reconciled by stable recording ID rather than number alone.

## Review status

`QUALIFIED`, risk class `R3`. Corpus preservation is extensive; chronology, identity, and candidate precision require further archival review.

## Evidence references

- [Video index](../../archive/semantic/atlas-brew/video-index.json)
- [Segment index](../../archive/semantic/atlas-brew/segment-index.json)
- [Combined source records](../../archive/source-records/atlas-brew-combined/source-records.json)
