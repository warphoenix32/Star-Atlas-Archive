"""Validate the Atlas Brew significance review."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SEMANTIC = ROOT / "archive/semantic/atlas-brew"
GENERATOR = HERE / "review_semantic_layer.py"


def sha(path: Path) -> str:
    return hashlib.sha256(canonical_text_bytes(path)).hexdigest()


def canonical_text_bytes(path: Path) -> bytes:
    """Hash generated text as UTF-8/LF so checks agree on Windows and Linux."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)


def main() -> int:
    errors = []
    files = sorted(SEMANTIC.glob("*.json")) + [HERE / "campaign-summary.json", HERE / "campaign-summary.md"]
    before = {p.relative_to(ROOT).as_posix(): sha(p) for p in files}
    first = run(sys.executable, GENERATOR.relative_to(ROOT).as_posix())
    middle = {p.relative_to(ROOT).as_posix(): sha(p) for p in files}
    second = run(sys.executable, GENERATOR.relative_to(ROOT).as_posix())
    after = {p.relative_to(ROOT).as_posix(): sha(p) for p in files}
    checks = {"deterministic_generation": first.returncode == second.returncode == 0 and before == middle == after}
    if not checks["deterministic_generation"]: errors.append("semantic review output is not byte-deterministic")

    for path in files:
        if path.suffix == ".json":
            try: json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc: errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
    checks["all_json_parses"] = not any(item.startswith("invalid JSON") for item in errors)

    segments = json.loads((SEMANTIC / "segment-index.json").read_text(encoding="utf-8"))["segments"]
    videos = json.loads((SEMANTIC / "video-index.json").read_text(encoding="utf-8"))["videos"]
    promotion = json.loads((SEMANTIC / "promotion-candidates.json").read_text(encoding="utf-8"))["candidates"]
    timeline = json.loads((SEMANTIC / "timeline-candidates.json").read_text(encoding="utf-8"))["candidates"]
    quotes = json.loads((SEMANTIC / "quote-index.json").read_text(encoding="utf-8"))["quotes"]
    pdec = json.loads((SEMANTIC / "promotion-candidate-decisions.json").read_text(encoding="utf-8"))["decisions"]
    tdec = json.loads((SEMANTIC / "timeline-candidate-decisions.json").read_text(encoding="utf-8"))["decisions"]
    clusters = json.loads((SEMANTIC / "duplicate-clusters.json").read_text(encoding="utf-8"))["clusters"]
    ids, source_ids = {s["segment_id"] for s in segments}, {v["source_id"] for v in videos}
    checks.update({
        "segments_preserved": len(segments) == len(ids) == 4937,
        "sources_reconcile": len(source_ids) == 123 and {s["source_id"] for s in segments} == source_ids,
        "captions_reconcile": sum(s["transcript_reference"]["caption_lines"] for s in segments) == 198558,
        "decision_coverage": len(pdec) == len(tdec) == 4937 and {d["segment_id"] for d in pdec} == ids and {d["segment_id"] for d in tdec} == ids,
        "candidate_references": all(i["segment_id"] in ids and i["supporting_captions"] for i in promotion + timeline),
        "exclusions_explained": all(i["eligible"] or i["exclusion_reason"] for i in pdec + tdec),
        "quotes_traceable": all(i["segment_id"] in ids and i["source_id"] in source_ids and i["speaker"] == "UNKNOWN" for i in quotes),
        "speaker_identity_not_inferred": all(s["speaker"] == "UNKNOWN" and s["institutional_attribution"] == "UNESTABLISHED" for s in segments),
        "selective_outputs": len(promotion) < 3306 and len(timeline) < 1423 and len(quotes) < 1218,
        "duplicate_clusters_reconcile": all(set(c["member_segment_ids"]) <= ids for c in clusters),
    })
    for name, passed in list(checks.items()):
        if not passed and name != "all_json_parses": errors.append(f"failed check: {name}")

    quality = json.loads((SEMANTIC / "quality-report.json").read_text(encoding="utf-8"))
    manifest_failures = []
    for item in quality["manifest"]["artifacts"]:
        path = ROOT / item["path"]
        if not path.is_file() or len(canonical_text_bytes(path)) != item["size_bytes"] or sha(path) != item["sha256"]:
            manifest_failures.append(item["path"])
    checks["manifest_reconciles"] = not manifest_failures
    if manifest_failures: errors.append("manifest mismatch: " + ", ".join(manifest_failures))

    changed = run("git", "diff", "--name-only", "origin/main...HEAD").stdout.splitlines()
    forbidden = [p for p in changed if p.startswith(("archive/raw/", "archive/normalized/", "archive/source-records/", "knowledge/", "graph/", "publication/"))]
    checks["repository_scope"] = not forbidden
    if forbidden: errors.append("forbidden paths changed: " + ", ".join(forbidden))
    diff_check = run("git", "diff", "--check")
    checks["git_diff_check"] = diff_check.returncode == 0
    if diff_check.returncode: errors.append(diff_check.stdout.strip())

    status = "PASS" if not errors else "FAIL"
    report = {"campaign_id": "atlas-brew-significance-review-2026-07", "status": status, "checks": checks, "errors": errors}
    (HERE / "validation-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (HERE / "validation-report.md").write_text("\n".join(["# Atlas Brew Significance Review Validation", "", f"**Result:** `{status}`", "", "## Checks", "", *[f"- **{'PASS' if value else 'FAIL'} - {name}:** {value}" for name, value in checks.items()], "", "## Errors", "", *([f"- {error}" for error in errors] if errors else ["- None."]), ""]), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
