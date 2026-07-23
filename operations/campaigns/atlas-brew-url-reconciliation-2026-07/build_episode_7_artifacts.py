#!/usr/bin/env python3
"""Build and validate qualified Atlas Brew #7 recovery artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ID = "SRC-ATLAS-BREW-YOUTUBE-YB8LZZZBHE"
VIDEO_ID = "Yb8lZZ_zbhE"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"
TITLE = "The Atlas Brew #7 Community Development."
PUBLISHED_AT = "2022-03-23T17:36:22-07:00"
CAMPAIGN_ID = "atlas-brew-url-reconciliation-2026-07"
SNAPSHOT_DATE = "2026-07-22"

RAW_PATH = (
    ROOT
    / "archive"
    / "raw"
    / "atlas-brew-youtube-recovery"
    / f"{SOURCE_ID}.asr.json"
)
NORMALIZED_PATH = (
    ROOT
    / "archive"
    / "normalized"
    / "atlas-brew-youtube-recovery"
    / f"{SOURCE_ID}.md"
)
PROVENANCE_PATH = (
    ROOT
    / "archive"
    / "provenance"
    / "atlas-brew-youtube-recovery"
    / f"{SOURCE_ID}.json"
)
SOURCE_RECORD_JSON_PATH = (
    ROOT
    / "archive"
    / "source-records"
    / "atlas-brew-youtube-recovery"
    / f"{SOURCE_ID}.json"
)
SOURCE_RECORD_MD_PATH = SOURCE_RECORD_JSON_PATH.with_suffix(".md")
PACKAGE_PATH = (
    ROOT
    / "archive"
    / "ingestion-packages"
    / "atlas-brew-youtube-recovery"
    / f"{SOURCE_ID}.json"
)
MANIFEST_PATH = (
    ROOT / "archive" / "manifests" / "atlas-brew-youtube-recovery-2026-07.json"
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def write_json(path: Path, value: Any) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_raw() -> dict[str, Any]:
    return json.loads(RAW_PATH.read_text(encoding="utf-8"))


def render_normalized(raw: dict[str, Any]) -> str:
    transcription = raw["transcription"]
    segments = raw["segments"]
    lines = [
        "---",
        f"source_id: {SOURCE_ID}",
        f'title: "{TITLE}"',
        "series: Atlas Brew",
        "episode_number: 7",
        "source_type: transcript",
        f"publication_date: {PUBLISHED_AT[:10]}",
        "publication_date_basis: youtube-player-microformat",
        "publisher: VBTV",
        "speaker_attribution: unknown",
        "transcript_origin: machine-generated-from-public-audio",
        f"transcription_engine: {transcription['engine']} {transcription['engine_version']}",
        f"transcription_model: {transcription['model']}",
        f"segment_count: {len(segments)}",
        f"last_timestamp: {segments[-1]['end_timestamp']}",
        "extraction_confidence: MEDIUM",
        "---",
        "",
        f"# {TITLE}",
        "",
        (
            "> Qualified machine-generated transcript recovered from the public "
            "YouTube audio because the video exposes no manual or automatic "
            "caption track. Speaker identities are not assigned. Wording may "
            "contain recognition errors; use the timestamps to verify important "
            "passages against the recording."
        ),
        "",
    ]
    lines.extend(
        f"[{segment['start_timestamp']}] {segment['text']}" for segment in segments
    )
    return "\n".join(lines) + "\n"


def quality_metrics(raw: dict[str, Any]) -> dict[str, Any]:
    segments = raw["segments"]
    duration = raw["transcription"]["duration_seconds"]
    last_end = segments[-1]["end_seconds"]
    return {
        "segment_count": len(segments),
        "first_timestamp": segments[0]["start_timestamp"],
        "last_timestamp": segments[-1]["end_timestamp"],
        "recording_duration_seconds": duration,
        "transcript_last_end_seconds": last_end,
        "untranscribed_tail_seconds": round(duration - last_end, 3),
        "average_log_probability": round(
            statistics.mean(segment["avg_logprob"] for segment in segments), 6
        ),
        "segments_with_no_speech_probability_gte_0_5": sum(
            segment["no_speech_prob"] >= 0.5 for segment in segments
        ),
        "empty_segments": sum(not segment["text"].strip() for segment in segments),
    }


def generate() -> None:
    raw = load_raw()
    normalized = render_normalized(raw)
    write_text(NORMALIZED_PATH, normalized)
    metrics = quality_metrics(raw)

    provenance = {
        "schema_version": "1.0",
        "campaign_id": CAMPAIGN_ID,
        "source_id": SOURCE_ID,
        "source": {
            "video_id": VIDEO_ID,
            "canonical_url": VIDEO_URL,
            "title": TITLE,
            "channel_id": "UCElCan0ISZn68l7b341yxLA",
            "channel_name": "VBTV",
            "published_at_original": PUBLISHED_AT,
            "published_at_normalized": PUBLISHED_AT[:10],
            "duration_seconds": 4999,
            "description": (
                "The Atlas Brew hosted today by Santi and ZeSKK, is all about "
                "community development. Amazing Alpha from the whole community! "
                "3 Unofficial arcade mini-games inspired by Star Atlas; re-supply "
                "tool by The Club; DAOcaster DAOmadness updates; Star Atlas TV "
                "announcement."
            ),
        },
        "retrieval": {
            "retrieval_date": SNAPSHOT_DATE,
            "caption_track_status": "NO_MANUAL_OR_AUTOMATIC_CAPTIONS",
            "caption_checks": [
                "YouTube public watch-page player response",
                "yt-dlp --list-subs",
            ],
            "audio_capture": {
                "method": "YOUTUBE_PUBLIC_AUDIO_STREAM",
                "format_id": 140,
                "mime_type": 'audio/mp4; codecs="mp4a.40.2"',
                "bytes": raw["capture"]["audio_bytes"],
                "sha256": raw["capture"]["audio_sha256"],
                "preserved_in_repository": False,
                "omission_reason": (
                    "The 77 MiB audio binary is a transient transcription input; "
                    "the canonical public recording URL and exact audio checksum "
                    "are preserved."
                ),
            },
            "retrieval_tool": {
                "name": "yt-dlp",
                "executable_sha256": (
                    "52fe3c26dcf71fbdc85b528589020bb0b8e383155cfa81b64dd447bbe35e24b8"
                ),
            },
        },
        "derivation": {
            "raw_asr_path": rel(RAW_PATH),
            "normalized_transcript_path": rel(NORMALIZED_PATH),
            "transcription": raw["transcription"],
            "quality_metrics": metrics,
        },
        "authority": {
            "recording_identity": "HIGH",
            "publication_metadata": "HIGH",
            "transcript_wording": "MEDIUM",
            "speaker_identity": "UNKNOWN",
        },
        "limitations": [
            "No source-provided caption track exists.",
            "The transcript is machine-generated and has not received line-by-line human correction.",
            "Speaker turns and identities are not assigned.",
            "The final 38.677 seconds contain no recovered speech and appear to be outro audio or silence.",
            "Community statements are not automatically official Star Atlas claims.",
        ],
    }
    write_json(PROVENANCE_PATH, provenance)

    raw_sha256 = sha256_path(RAW_PATH)
    normalized_sha256 = sha256_path(NORMALIZED_PATH)
    source_record = {
        "source_id": SOURCE_ID,
        "collection": "atlas-brew-youtube-recovery",
        "title": TITLE,
        "series": "Atlas Brew",
        "episode_number": 7,
        "source_type": "transcript",
        "classification": "COMMUNITY_EVENT_RECORDING",
        "publication_date": PUBLISHED_AT[:10],
        "publication_date_original": PUBLISHED_AT,
        "publication_date_basis": "youtube-player-microformat",
        "publisher": "VBTV",
        "channel_id": "UCElCan0ISZn68l7b341yxLA",
        "documented_hosts": ["Santi", "ZeSKK"],
        "documented_hosts_basis": "YouTube video description",
        "speaker_attribution": "UNKNOWN",
        "original_url": VIDEO_URL,
        "youtube_video_id": VIDEO_ID,
        "evidence_tier": "QUALIFIED_MACHINE_TRANSCRIPT",
        "raw_path": rel(RAW_PATH),
        "normalized_path": rel(NORMALIZED_PATH),
        "provenance_path": rel(PROVENANCE_PATH),
        "raw_sha256": raw_sha256,
        "normalized_sha256": normalized_sha256,
        "caption_count": metrics["segment_count"],
        "first_timestamp": metrics["first_timestamp"],
        "last_timestamp": metrics["last_timestamp"],
        "extraction_confidence": "MEDIUM",
        "manual_review_required": False,
        "manual_review_recommended": True,
        "human_correction_status": "NOT_PERFORMED",
        "normalization_actions": [
            "Transcribed public audio with faster-whisper 1.2.1 small.en",
            "Preserved machine-generated wording without editorial correction",
            "Rendered one timestamped line per ASR segment",
            "Preserved segment-level quality metrics in the raw ASR artifact",
        ],
        "limitations": provenance["limitations"],
        "ingestion_status": "QUALIFIED_ARCHIVAL_RECOVERY",
    }
    write_json(SOURCE_RECORD_JSON_PATH, source_record)
    write_text(
        SOURCE_RECORD_MD_PATH,
        "\n".join(
            [
                f"# {TITLE}",
                "",
                "## Metadata",
                "",
                f"- **Source ID:** `{SOURCE_ID}`",
                "- **Series / episode:** Atlas Brew #7",
                f"- **Publisher / upload channel:** VBTV (`{provenance['source']['channel_id']}`)",
                f"- **Publication date:** `{PUBLISHED_AT}`",
                f"- **Original recording:** {VIDEO_URL}",
                "- **Document type:** Qualified machine-generated transcript",
                "- **Extraction confidence:** `MEDIUM`",
                "- **Speaker attribution:** `UNKNOWN`",
                "",
                "## Provenance",
                "",
                (
                    "YouTube exposed no manual or automatic caption track. The "
                    "public audio stream was captured as a transient input and "
                    "transcribed locally. The audio binary is not stored, but its "
                    f"SHA-256 is `{raw['capture']['audio_sha256']}`."
                ),
                "",
                f"- **Raw ASR artifact:** `{rel(RAW_PATH)}`",
                f"- **Normalized transcript:** `{rel(NORMALIZED_PATH)}`",
                f"- **Provenance record:** `{rel(PROVENANCE_PATH)}`",
                f"- **Raw ASR SHA-256:** `{raw_sha256}`",
                f"- **Normalized SHA-256:** `{normalized_sha256}`",
                "",
                "## Transcription Method",
                "",
                (
                    "The recovery used `faster-whisper 1.2.1`, model `small.en`, "
                    "CPU `int8`, twelve CPU threads, deterministic temperature "
                    "zero, single-beam decoding, and voice-activity filtering."
                ),
                "",
                f"- **Timestamped segments:** {metrics['segment_count']}",
                f"- **Coverage:** `{metrics['first_timestamp']}` through `{metrics['last_timestamp']}`",
                f"- **Recording duration:** {metrics['recording_duration_seconds']:.3f} seconds",
                f"- **Untranscribed tail:** {metrics['untranscribed_tail_seconds']:.3f} seconds",
                "",
                "## Source Lineage",
                "",
                "- **Publication:** VBTV YouTube channel",
                "- **Publication role:** Community event recording",
                "- **Relationship:** Records Atlas Brew #7",
                "- **Primary source:** Public audiovisual recording",
                "- **Documented hosts:** Santi and ZeSKK (video-description attribution only)",
                "- **Lineage confidence:** `HIGH` for recording identity; `MEDIUM` for transcript wording",
                "",
                "## Limitations",
                "",
                *[f"- {item}" for item in provenance["limitations"]],
                "",
                "Important passages should be checked against the public recording "
                "at the preserved timestamp before knowledge promotion.",
                "",
            ]
        ),
    )

    package = {
        "schema_version": "2.1",
        "campaign_id": CAMPAIGN_ID,
        "source_id": SOURCE_ID,
        "document_type": "TRANSCRIPT",
        "source_record_path": rel(SOURCE_RECORD_JSON_PATH),
        "raw_artifact_path": rel(RAW_PATH),
        "normalized_artifact_path": rel(NORMALIZED_PATH),
        "provenance_path": rel(PROVENANCE_PATH),
        "content": {
            "segment_count": metrics["segment_count"],
            "first_timestamp": metrics["first_timestamp"],
            "last_timestamp": metrics["last_timestamp"],
            "language": raw["transcription"]["language"],
            "machine_generated": True,
        },
        "semantic_extraction": {
            "performed": False,
            "reason": "URL reconciliation and transcript recovery only",
        },
        "checksums": {
            "raw_sha256": raw_sha256,
            "normalized_sha256": normalized_sha256,
        },
        "status": "QUALIFIED_ARCHIVAL_RECOVERY",
    }
    write_json(PACKAGE_PATH, package)

    artifact_paths = [
        RAW_PATH,
        NORMALIZED_PATH,
        PROVENANCE_PATH,
        SOURCE_RECORD_JSON_PATH,
        SOURCE_RECORD_MD_PATH,
        PACKAGE_PATH,
    ]
    manifest = {
        "campaign_id": CAMPAIGN_ID,
        "recovery_id": "atlas-brew-7-youtube-audio-recovery",
        "source_id": SOURCE_ID,
        "generated_on": SNAPSHOT_DATE,
        "status": "QUALIFIED_ARCHIVAL_RECOVERY",
        "artifact_count": len(artifact_paths),
        "artifacts": [
            {
                "path": rel(path),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_path(path),
            }
            for path in artifact_paths
        ],
        "boundaries": {
            "combined_transcript_rewritten": False,
            "existing_combined_source_records_rewritten": False,
            "semantic_enrichment_performed": False,
            "speaker_identity_inferred": False,
        },
    }
    write_json(MANIFEST_PATH, manifest)
    validate()


def validate() -> None:
    errors: list[str] = []
    paths = [
        RAW_PATH,
        NORMALIZED_PATH,
        PROVENANCE_PATH,
        SOURCE_RECORD_JSON_PATH,
        SOURCE_RECORD_MD_PATH,
        PACKAGE_PATH,
        MANIFEST_PATH,
    ]
    for path in paths:
        if not path.is_file():
            errors.append(f"missing artifact: {rel(path)}")

    if errors:
        raise SystemExit("\n".join(errors))

    raw = load_raw()
    provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
    record = json.loads(SOURCE_RECORD_JSON_PATH.read_text(encoding="utf-8"))
    package = json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    segments = raw.get("segments", [])

    if raw.get("source_id") != SOURCE_ID:
        errors.append("raw source_id mismatch")
    if raw.get("video_id") != VIDEO_ID:
        errors.append("raw video_id mismatch")
    if not segments:
        errors.append("no transcript segments")
    if segments and [segment.get("sequence") for segment in segments] != list(
        range(1, len(segments) + 1)
    ):
        errors.append("segment sequence is not contiguous")
    if any(not segment.get("text", "").strip() for segment in segments):
        errors.append("empty transcript segment")
    if any(
        current["start_seconds"] < previous["start_seconds"]
        for previous, current in zip(segments, segments[1:])
    ):
        errors.append("segment timestamps are not ordered")
    if quality_metrics(raw)["untranscribed_tail_seconds"] > 60:
        errors.append("untranscribed tail exceeds 60 seconds")
    if record.get("raw_sha256") != sha256_path(RAW_PATH):
        errors.append("source record raw checksum mismatch")
    if record.get("normalized_sha256") != sha256_path(NORMALIZED_PATH):
        errors.append("source record normalized checksum mismatch")
    if package.get("checksums", {}).get("raw_sha256") != sha256_path(RAW_PATH):
        errors.append("ingestion package raw checksum mismatch")
    if provenance.get("authority", {}).get("speaker_identity") != "UNKNOWN":
        errors.append("speaker identity must remain UNKNOWN")

    manifest_entries = {item["path"]: item for item in manifest.get("artifacts", [])}
    for path in paths[:-1]:
        entry = manifest_entries.get(rel(path))
        if not entry:
            errors.append(f"manifest omission: {rel(path)}")
        elif entry.get("sha256") != sha256_path(path):
            errors.append(f"manifest checksum mismatch: {rel(path)}")

    if errors:
        raise SystemExit("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["generate", "validate"])
    args = parser.parse_args()
    if args.command == "generate":
        generate()
    else:
        validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
