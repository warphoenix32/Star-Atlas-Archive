---
id: MEDIA-VBTV-RECORDING-INDEX
title: VBTV / Star Atlas TV Recording Index
entry_type: video-archive-index
status: active
created: 2026-07-12
updated: 2026-07-12
confidence: medium
source_class:
  - community
  - media
  - firsthand-context
tags:
  - star-atlas
  - video
  - community-events
  - vbtv
  - star-atlas-tv
aliases:
  - VBTV
  - Star Atlas TV
related_entities:
  - MEDIA-VBTV
publication_status: public
---

# VBTV / Star Atlas TV Recording Index

## Purpose

This file is the master reverse-chronological index for recordings published by **VBTV**, formerly **Star Atlas TV**. The channel is operated by **ODVB**, commonly called **VB**, and preserves a large archive of recurring Star Atlas community events.

**Current channel:** https://youtube.com/@vbtv-77  
**Former public identity:** Star Atlas TV  
**Current public identity:** VBTV  
**Rebrand timing:** Early July 2026, based on firsthand context from Krigs.  
**Markers:** `[SRC-COMMUNITY] [SRC-MEDIA] [SRC-KRIGS] [EV-ATTRIBUTED] [CONF-MEDIUM]`

## Current inventory status

The channel identity and URL have been confirmed by Krigs. During the initial indexing attempt, the available public web-retrieval tools could not enumerate the YouTube channel's Videos or Live tabs, and search-engine results had not yet indexed the recent VBTV rebrand. Therefore, no recording titles or dates are entered below until they can be retrieved directly and verified.

This is an access limitation, not evidence that the archive is unavailable.

## Reverse-chronological recording inventory

> Entries will be added newest first. Do not infer dates, guests, event types or episode relationships from thumbnails alone.

| Published | Event date | Title | Series / event | Video ID | Duration | Speakers | Transcript | Processing status |
|---|---|---|---|---|---|---|---|---|
| — | — | Inventory pending direct channel enumeration | — | — | — | — | — | `[PUB-NEEDS-VERIFY]` |

## Recording-entry standard

Each indexed recording should include:

```yaml
published_date: YYYY-MM-DD
event_date: YYYY-MM-DD | unknown
title: Exact YouTube title
video_id: YouTube video ID
url: Canonical watch URL
duration: HH:MM:SS
series: Atlas Brew | Town Hall | Community Event | Interview | Other
host:
  - ACTOR-ID or displayed name
guests:
  - ACTOR-ID or displayed name
transcript_status: platform-captions | generated | manual | unavailable
processing_status: metadata-only | summarized | transcript-cleaned | fully-ingested
confidence: high | medium | low
```

### Required notes

- Distinguish upload date from the date the event occurred.
- Preserve exact historical branding shown on the recording.
- Record whether the video originally appeared under Star Atlas TV before the VBTV rebrand.
- Attribute executive, developer, Foundation, Council or guild statements to the speaker.
- Add timestamps for consequential announcements, disputes or historical claims.
- Link resulting facts to the chronology, product registry, guild index, actor index, governance files or lore registry as applicable.
- Treat jokes, speculation and live-chat sentiment as context, not established fact.

## Processing sequence

1. Enumerate all channel uploads and livestream archives.
2. Deduplicate streams, edited reposts, shorts and clips derived from longer recordings.
3. Sort by YouTube publication timestamp descending.
4. Capture stable metadata before transcript work.
5. Process the newest complete weekly-event recording first.
6. Continue backward without skipping inaccessible items; mark them as unavailable or metadata-only.
7. Update topical knowledge files after each recording rather than waiting for the full channel to be completed.

## Source and access notes

- `[SRC-KRIGS]`: Krigs identified VBTV as the recently rebranded Star Atlas TV channel and identified ODVB / VB as its owner-operator.
- `[EV-INCOMPLETE]`: The recording inventory is currently incomplete because direct enumeration was not available through the retrieval path used on 2026-07-12.
- `[Q-HIGH]`: Obtain the channel's complete upload and livestream metadata, ideally through a YouTube channel export, RSS/API access, or a locally generated `yt-dlp --flat-playlist` listing.

## Open questions

- What was the exact date of the Star Atlas TV → VBTV rebrand?
- Did the rebrand alter the channel handle, display name only, or both?
- Which recurring shows and weekly events are represented in the archive?
- Are any recordings unlisted, private, deleted or duplicated on another channel?
- Does the channel maintain original descriptions, chapters, guest lists or caption tracks for older broadcasts?
