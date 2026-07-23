#!/usr/bin/env python3
"""Create a timestamped, machine-generated recovery transcript for Atlas Brew #7.

The public YouTube video has no manual or automatic caption tracks. This
targeted recovery utility transcribes a locally supplied audio capture and
records the model, inference settings, source checksum, and segment-level
quality signals needed to audit the derived transcript.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


VIDEO_ID = "Yb8lZZ_zbhE"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"
SOURCE_ID = "SRC-ATLAS-BREW-YOUTUBE-YB8LZZZBHE"
TITLE = "The Atlas Brew #7 Community Development."
PUBLISHED_AT = "2022-03-23T17:36:22-07:00"
TRANSCRIPTION_RUN_AT = "2026-07-22T00:00:00Z"


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def format_timestamp(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def transcribe(
    audio_path: Path,
    output_path: Path,
    *,
    model_name: str,
    device: str,
    compute_type: str,
    cpu_threads: int,
) -> None:
    from faster_whisper import WhisperModel

    model = WhisperModel(
        model_name,
        device=device,
        compute_type=compute_type,
        cpu_threads=cpu_threads,
        num_workers=1,
    )
    segments, info = model.transcribe(
        str(audio_path),
        language="en",
        beam_size=1,
        best_of=1,
        temperature=0.0,
        vad_filter=True,
        condition_on_previous_text=True,
        word_timestamps=False,
    )

    captured_segments: list[dict[str, Any]] = []
    for index, segment in enumerate(segments, start=1):
        captured_segments.append(
            {
                "sequence": index,
                "start_seconds": round(segment.start, 3),
                "end_seconds": round(segment.end, 3),
                "start_timestamp": format_timestamp(segment.start),
                "end_timestamp": format_timestamp(segment.end),
                "text": segment.text.strip(),
                "avg_logprob": round(segment.avg_logprob, 6),
                "compression_ratio": round(segment.compression_ratio, 6),
                "no_speech_prob": round(segment.no_speech_prob, 6),
            }
        )
        if index % 10 == 0:
            print(
                f"captured {index} segments through "
                f"{format_timestamp(segment.end)}",
                flush=True,
            )

    payload = {
        "schema_version": "1.0",
        "source_id": SOURCE_ID,
        "video_id": VIDEO_ID,
        "canonical_url": VIDEO_URL,
        "title": TITLE,
        "published_at": PUBLISHED_AT,
        "capture": {
            "method": "YOUTUBE_PUBLIC_AUDIO_STREAM",
            "audio_filename": audio_path.name,
            "audio_sha256": sha256_path(audio_path),
            "audio_bytes": audio_path.stat().st_size,
            "captions_available": False,
            "caption_check_result": (
                "YouTube public player metadata and yt-dlp both reported no "
                "manual or automatic caption tracks."
            ),
        },
        "transcription": {
            "engine": "faster-whisper",
            "engine_version": "1.2.1",
                "model": model_name,
                "device": device,
                "compute_type": compute_type,
                "cpu_threads": cpu_threads,
            "language": info.language,
            "language_probability": round(info.language_probability, 6),
            "duration_seconds": round(info.duration, 3),
            "duration_after_vad_seconds": round(info.duration_after_vad, 3),
            "settings": {
                "beam_size": 1,
                "best_of": 1,
                "temperature": 0.0,
                "vad_filter": True,
                "condition_on_previous_text": True,
                "word_timestamps": False,
            },
            "speaker_attribution": "UNKNOWN",
            "machine_generated": True,
        },
        "segments": captured_segments,
        "generated_at": TRANSCRIPTION_RUN_AT,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {len(captured_segments)} segments to {output_path}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_path", type=Path)
    parser.add_argument("output_path", type=Path)
    parser.add_argument("--model", default="small.en")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument("--cpu-threads", type=int, default=12)
    args = parser.parse_args()

    if not args.audio_path.is_file():
        parser.error(f"audio file does not exist: {args.audio_path}")
    transcribe(
        args.audio_path,
        args.output_path,
        model_name=args.model,
        device=args.device,
        compute_type=args.compute_type,
        cpu_threads=args.cpu_threads,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
