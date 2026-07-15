from __future__ import annotations

import hashlib
import json
import py_compile
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SEMANTIC_ROOT = ROOT / "archive" / "semantic" / "star-atlas-transcripts"
SOURCE_ROOT = ROOT / "archive" / "source-records" / "star-atlas-transcripts-ingestion-2026-07"
OPS_ROOT = ROOT / "operations" / "campaigns" / "star-atlas-transcripts-semantic-2026-07"
GENERATOR = OPS_ROOT / "generate_semantic_index.py"
CAPTION_RE = re.compile(r"^\[(\d{2}:\d{2}:\d{2})\]\s+(.*)$")
EXPECTED_ARTIFACTS = {
    "collection-index.json", "source-index.json", "segment-index.json", "topic-index.json",
    "concept-index.json", "entity-links.json", "quote-index.json", "timeline-candidates.json",
    "promotion-candidates.json", "promotion-candidate-decisions.json",
    "timeline-candidate-decisions.json", "duplicate-clusters.json", "research-gaps.json",
    "quality-report.json",
}
ALLOWED_PREFIXES = (
    "archive/semantic/star-atlas-transcripts/",
    "operations/campaigns/star-atlas-transcripts-semantic-2026-07/",
)


def seconds(timestamp: str) -> int:
    hour, minute, second = (int(value) for value in timestamp.split(":"))
    return hour * 3600 + minute * 60 + second


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, env=env)


def main() -> None:
    errors: list[str] = []
    warnings = [
        "All speaker attribution remains UNKNOWN.",
        "Original URLs are absent and publication dates are incomplete for 33 sources.",
        "Candidate confidence measures extraction quality, not factual truth.",
        "Automated transcript text may contain recognition errors.",
        "Repository Wave 1.5 validation has inherited fixed-count drift: 962 reconciliation records versus an expected 960.",
    ]
    checks: dict[str, object] = {}
    documents = {}
    for path in sorted(SEMANTIC_ROOT.glob("*.json")):
        try:
            documents[path.name] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON {path}: {exc}")
    checks["json_documents_parsed"] = len(documents)
    if set(documents) != EXPECTED_ARTIFACTS:
        errors.append(f"semantic artifact set mismatch: {sorted(set(documents) ^ EXPECTED_ARTIFACTS)}")
    if errors:
        finish(errors, warnings, checks)

    source_doc = documents["source-index.json"]
    segment_doc = documents["segment-index.json"]
    sources = source_doc["sources"]
    segments = segment_doc["segments"]
    source_ids = [source["source_id"] for source in sources]
    segment_ids = [segment["segment_id"] for segment in segments]
    source_map = {source["source_id"]: source for source in sources}
    segment_map = {segment["segment_id"]: segment for segment in segments}
    checks.update({"source_ids_reconciled": len(sources), "source_ids_unique": len(source_ids) == len(set(source_ids)), "segment_ids_reconciled": len(segments), "segment_ids_unique": len(segment_ids) == len(set(segment_ids))})
    if len(sources) != 36 or not checks["source_ids_unique"]: errors.append("36 unique source IDs not preserved")
    if len(segments) != 1910 or not checks["segment_ids_unique"]: errors.append("1,910 unique segment IDs not preserved")
    package_source_ids = {json.loads(path.read_text(encoding="utf-8"))["source_id"] for path in SOURCE_ROOT.rglob("*.json")}
    if set(source_ids) != package_source_ids: errors.append("semantic source IDs do not reconcile to package records")

    topics = set(segment_doc["topic_taxonomy"])
    statements = set(segment_doc["statement_taxonomy"])
    lifecycles = set(segment_doc["product_lifecycle_taxonomy"])
    evidence = set(segment_doc["evidence_taxonomy"])
    segments_by_source: dict[str, list[dict]] = defaultdict(list)
    transcript_cache: dict[str, list[str]] = {}
    caption_total = 0

    def verify_caption(segment: dict, ref: dict, label: str) -> None:
        path = str(segment["transcript_reference"]["path"])
        lines = transcript_cache.setdefault(path, (ROOT / path).read_text(encoding="utf-8").splitlines())
        line_number = int(ref["line"])
        if not (1 <= line_number <= len(lines)):
            errors.append(f"{label} line out of range: {segment['segment_id']}"); return
        expected = f"[{ref['timestamp']}] {ref['text']}"
        if lines[line_number - 1] != expected:
            errors.append(f"{label} not verbatim at recorded line: {segment['segment_id']}:{line_number}")
        start = int(segment["transcript_reference"]["line_start"]); end = int(segment["transcript_reference"]["line_end"])
        if not start <= line_number <= end: errors.append(f"{label} outside segment: {segment['segment_id']}:{line_number}")

    for segment in segments:
        if segment["source_id"] not in source_map: errors.append(f"orphan segment source: {segment['segment_id']}"); continue
        segments_by_source[segment["source_id"]].append(segment)
        reference = segment["transcript_reference"]
        transcript = ROOT / reference["path"]
        if not transcript.exists(): errors.append(f"missing transcript: {transcript}"); continue
        lines = transcript_cache.setdefault(reference["path"], transcript.read_text(encoding="utf-8").splitlines())
        start_line, end_line = int(reference["line_start"]), int(reference["line_end"])
        if not 1 <= start_line <= end_line <= len(lines): errors.append(f"invalid line range: {segment['segment_id']}"); continue
        caption_lines = []
        for line_number in range(start_line, end_line + 1):
            match = CAPTION_RE.match(lines[line_number - 1])
            if match: caption_lines.append((line_number, match.group(1), match.group(2)))
        if len(caption_lines) != reference["caption_lines"]: errors.append(f"caption line mismatch: {segment['segment_id']}")
        elif caption_lines and (caption_lines[0][1] != segment["start_timestamp"] or caption_lines[-1][1] != segment["end_timestamp"]): errors.append(f"timestamp mismatch: {segment['segment_id']}")
        if seconds(segment["start_timestamp"]) > seconds(segment["end_timestamp"]): errors.append(f"timestamp regression: {segment['segment_id']}")
        caption_total += int(reference["caption_lines"])
        if not set(segment["topic_tags"]) <= topics: errors.append(f"uncontrolled topic: {segment['segment_id']}")
        if not set(segment["statement_classifications"]) <= statements: errors.append(f"uncontrolled statement: {segment['segment_id']}")
        if not set(segment["product_lifecycle"]) <= lifecycles: errors.append(f"uncontrolled lifecycle: {segment['segment_id']}")
        if not set(segment["evidence_classifications"]) <= evidence: errors.append(f"uncontrolled evidence: {segment['segment_id']}")
        if segment["speaker"] != "UNKNOWN" or segment["speaker_confidence"] != "UNKNOWN": errors.append(f"speaker inferred: {segment['segment_id']}")
        lifecycle_states = {item["state"] for item in segment["lifecycle_evidence"]}
        if lifecycle_states != set(segment["product_lifecycle"]): errors.append(f"lifecycle evidence mismatch: {segment['segment_id']}")
        for item in segment["lifecycle_evidence"]:
            if not item.get("entity") or item.get("confidence") not in {"HIGH", "MEDIUM", "LOW"}: errors.append(f"invalid lifecycle evidence: {segment['segment_id']}")
            verify_caption(segment, item["supporting_caption"], "lifecycle evidence")
        quote_decision = segment["candidate_decisions"]["quote_candidate_decision"]
        if quote_decision["eligible"] and not quote_decision.get("supporting_caption"): errors.append(f"eligible quote lacks support: {segment['segment_id']}")
        if quote_decision.get("supporting_caption"): verify_caption(segment, quote_decision["supporting_caption"], "quote decision")

    for source in sources:
        source_segments = sorted(segments_by_source[source["source_id"]], key=lambda item: item["transcript_reference"]["line_start"])
        if [segment["segment_id"] for segment in source_segments] != source["segment_ids"]: errors.append(f"source segment index mismatch: {source['source_id']}")
        if sum(segment["transcript_reference"]["caption_lines"] for segment in source_segments) != source["caption_lines"]: errors.append(f"source caption coverage mismatch: {source['source_id']}")
        for previous, current in zip(source_segments, source_segments[1:]):
            if previous["transcript_reference"]["line_end"] >= current["transcript_reference"]["line_start"]: errors.append(f"overlapping segments: {previous['segment_id']} / {current['segment_id']}")
    checks.update({"caption_lines_covered": caption_total, "segment_line_ranges_valid": not any("line range" in e for e in errors), "segment_timestamps_valid": not any("timestamp" in e for e in errors), "segment_ranges_non_overlapping": not any("overlapping" in e for e in errors), "controlled_taxonomies_only": not any("uncontrolled" in e for e in errors), "no_speaker_identity_inferred": not any("speaker inferred" in e for e in errors)})
    if caption_total != 78752: errors.append(f"global caption coverage mismatch: {caption_total}")

    links = documents["entity-links.json"]["links"]
    if {link["segment_id"] for link in links} != set(segment_ids): errors.append("entity-link coverage mismatch")
    registry_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in (ROOT / "knowledge").rglob("*.md"))
    linked_entity_ids = {entity["entity_id"] for link in links for entity in link["canonical_entities"]}
    for entity_id in linked_entity_ids:
        if entity_id not in registry_text: errors.append(f"unregistered entity ID: {entity_id}")
    checks.update({"entity_link_records_reconciled": len(links), "canonical_entity_ids_registered": not any("unregistered entity" in e for e in errors)})

    quotes = documents["quote-index.json"]["quotes"]
    for quote in quotes:
        segment = segment_map.get(quote["segment_id"])
        if segment is None or segment["source_id"] != quote["source_id"]: errors.append(f"orphan quote: {quote['quote_id']}"); continue
        if quote["speaker"] != "UNKNOWN" or not quote["manual_review_required"]: errors.append(f"invalid quote attribution/review: {quote['quote_id']}")
        if quote["quote_confidence"] not in {"HIGH", "MEDIUM", "LOW"}: errors.append(f"invalid quote confidence: {quote['quote_id']}")
        verify_caption(segment, {"timestamp": quote["timestamp"], "line": next(ref["line"] for ref in quote["quote_context"] if ref["timestamp"] == quote["timestamp"] and ref["text"] == quote["verbatim_quote"]), "text": quote["verbatim_quote"]}, "quote")
    checks["quotes_verbatim"] = len(quotes)

    promotion_candidates = documents["promotion-candidates.json"]["candidates"]
    timeline_candidates = documents["timeline-candidates.json"]["candidates"]
    promotion_ids = {candidate["candidate_id"] for candidate in promotion_candidates}
    timeline_ids = {candidate["candidate_id"] for candidate in timeline_candidates}
    for candidate in promotion_candidates:
        segment = segment_map.get(candidate["segment_id"])
        if segment is None or segment["source_id"] != candidate["source_id"]: errors.append(f"orphan promotion candidate: {candidate['candidate_id']}"); continue
        if not candidate["supporting_captions"] or not candidate["candidate_reasons"] or candidate["candidate_confidence"] not in {"HIGH", "MEDIUM", "LOW"} or candidate["review_priority"] not in {"HIGH_PRIORITY", "MEDIUM_PRIORITY", "LOW_PRIORITY"}: errors.append(f"incomplete promotion evidence: {candidate['candidate_id']}")
        for ref in candidate["supporting_captions"]: verify_caption(segment, ref, "promotion support")
    for candidate in timeline_candidates:
        segment = segment_map.get(candidate["segment_id"])
        if segment is None or segment["source_id"] != candidate["source_id"]: errors.append(f"orphan timeline candidate: {candidate['candidate_id']}"); continue
        if not candidate["supporting_captions"] or not candidate["date_basis"] or not candidate["event_type"] or candidate["timeline_confidence"] not in {"HIGH", "MEDIUM", "LOW"}: errors.append(f"incomplete timeline evidence: {candidate['candidate_id']}")
        for ref in candidate["supporting_captions"]: verify_caption(segment, ref, "timeline support")
    checks.update({"promotion_candidates_reconciled": len(promotion_candidates), "timeline_candidates_reconciled": len(timeline_candidates), "every_promotion_candidate_has_support": not any("promotion evidence" in e or "promotion support" in e for e in errors), "every_timeline_candidate_has_support_and_date_basis": not any("timeline evidence" in e or "timeline support" in e for e in errors)})

    promotion_decisions = documents["promotion-candidate-decisions.json"]["decisions"]
    timeline_decisions = documents["timeline-candidate-decisions.json"]["decisions"]
    if len(promotion_decisions) != 1910 or {d["segment_id"] for d in promotion_decisions} != set(segment_ids): errors.append("promotion decision coverage mismatch")
    if len(timeline_decisions) != 1910 or {d["segment_id"] for d in timeline_decisions} != set(segment_ids): errors.append("timeline decision coverage mismatch")
    for label, decisions, candidate_ids in (("promotion", promotion_decisions, promotion_ids), ("timeline", timeline_decisions, timeline_ids)):
        for decision in decisions:
            if decision["eligible"]:
                if decision["candidate_id"] not in candidate_ids: errors.append(f"eligible {label} decision lacks candidate: {decision['decision_id']}")
            elif not decision["exclusion_reason"]:
                errors.append(f"excluded {label} decision lacks reason: {decision['decision_id']}")
            for ref in decision.get("supporting_captions", []): verify_caption(segment_map[decision["segment_id"]], ref, f"{label} decision support")
    checks.update({"promotion_decisions_reconciled": len(promotion_decisions), "timeline_decisions_reconciled": len(timeline_decisions), "every_exclusion_has_reason": not any("lacks reason" in e for e in errors), "all_candidate_ids_reconcile": not any("lacks candidate" in e or "orphan" in e for e in errors)})

    clusters = documents["duplicate-clusters.json"]["clusters"]
    clustered_members = set()
    for cluster in clusters:
        members = set(cluster["member_candidate_ids"]); clustered_members |= members
        if not members <= promotion_ids or cluster["strongest_candidate_id"] not in members: errors.append(f"invalid duplicate cluster: {cluster['duplicate_cluster_id']}")
        for candidate in promotion_candidates:
            if candidate["candidate_id"] in members and (candidate["duplicate_cluster_id"] != cluster["duplicate_cluster_id"] or candidate["strongest_candidate_id"] != cluster["strongest_candidate_id"]): errors.append(f"duplicate annotation mismatch: {candidate['candidate_id']}")
    checks.update({"duplicate_clusters_reconciled": len(clusters), "clustered_candidates": len(clustered_members)})

    research = documents["research-gaps.json"]
    if {gap["source_id"] for gap in research["source_gaps"]} != set(source_ids): errors.append("source research-gap coverage mismatch")
    valid_candidate_ids = promotion_ids | timeline_ids
    if any(gap["candidate_id"] not in valid_candidate_ids or not gap["gap_type"] for gap in research["candidate_gaps"]): errors.append("candidate research-gap mismatch")
    checks.update({"research_gap_sources_reconciled": len(research["source_gaps"]), "candidate_research_gaps_typed": len(research["candidate_gaps"])})

    for topic, record in documents["topic-index.json"]["topics"].items():
        expected = {segment["segment_id"] for segment in segments if topic in segment["topic_tags"]}
        if set(record["segment_ids"]) != expected or record["segment_count"] != len(expected): errors.append(f"topic index mismatch: {topic}")

    quality = documents["quality-report.json"]
    for artifact in quality["manifest"]["artifacts"]:
        path = ROOT / artifact["path"]
        if not path.exists() or path.stat().st_size != artifact["size_bytes"] or sha256(path) != artifact["sha256"]: errors.append(f"quality-manifest mismatch: {artifact['path']}")
    checks["quality_manifest_checksums_match"] = not any("quality-manifest" in e for e in errors)

    before_hashes = {path.relative_to(ROOT).as_posix(): sha256(path) for path in sorted(SEMANTIC_ROOT.glob("*.json"))}
    before_hashes.update({path.relative_to(ROOT).as_posix(): sha256(path) for path in (OPS_ROOT / "campaign-summary.json", OPS_ROOT / "campaign-summary.md")})
    generated = run([sys.executable, str(GENERATOR)])
    after_hashes = {ROOT.joinpath(path).relative_to(ROOT).as_posix(): sha256(ROOT / path) for path in before_hashes}
    deterministic = generated.returncode == 0 and before_hashes == after_hashes
    if not deterministic: errors.append("generator is not byte-deterministic")
    checks["generator_deterministic"] = deterministic

    try:
        py_compile.compile(str(GENERATOR), doraise=True); py_compile.compile(str(Path(__file__)), doraise=True)
        checks["python_sources_compile"] = True
    except py_compile.PyCompileError as exc:
        checks["python_sources_compile"] = False; errors.append(f"Python compilation failed: {exc}")

    schema = run([sys.executable, "operations/tests/schema/test_schema_compatibility.py"])
    checks["schema_tests_pass"] = schema.returncode == 0
    if schema.returncode: errors.append("schema compatibility tests failed")
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "operations" / "pipeline" / "src"))
    try:
        from operations.tests.pipeline.test_inventory import test_audiovisual_content_is_retained_as_deferred_metadata, test_flatten_deduplicates_and_preserves_provenance
        from operations.tests.pipeline.test_normalize import test_does_not_merge_http_and_https_without_evidence, test_normalizes_youtube_variants, test_removes_tracking_and_fragment_and_sorts_query
        functions = [test_flatten_deduplicates_and_preserves_provenance, test_audiovisual_content_is_retained_as_deferred_metadata, test_removes_tracking_and_fragment_and_sorts_query, test_normalizes_youtube_variants, test_does_not_merge_http_and_https_without_evidence]
        for function in functions: function()
        checks["pipeline_tests_pass"] = True
    except Exception as exc:
        checks["pipeline_tests_pass"] = False; errors.append(f"pipeline tests failed: {exc}")

    committed = run(["git", "diff", "--name-only", "origin/main...HEAD"])
    working = run(["git", "status", "--porcelain"])
    paths = [line.strip() for line in committed.stdout.splitlines() if line.strip()]
    paths.extend(line[3:].strip().strip('"') for line in working.stdout.splitlines() if len(line) >= 4)
    forbidden = sorted({path for path in paths if not path.startswith(ALLOWED_PREFIXES)})
    checks["allowed_paths_only"] = not forbidden
    checks["canonical_layers_modified"] = any(path.startswith(("knowledge/", "graph/", "publication/", "archive/raw/", "archive/normalized/", "archive/source-records/")) for path in paths)
    if forbidden: errors.append("files outside allowed paths: " + ", ".join(forbidden))
    diff_check = run(["git", "diff", "--check"])
    checks["git_diff_check_pass"] = diff_check.returncode == 0
    if diff_check.returncode: errors.append("git diff --check failed: " + diff_check.stdout.strip())
    finish(errors, warnings, checks)


def finish(errors: list[str], warnings: list[str], checks: dict[str, object]) -> None:
    status = "PASS" if not errors else "FAIL"
    report = {"campaign_id": "star-atlas-transcripts-semantic-2026-07", "status": status, "checks": checks, "warnings": warnings, "errors": errors}
    (OPS_ROOT / "validation-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Semantic Validation Report — Revised", "", f"Status: **{status}**", "", "## Checks", ""]
    lines.extend(f"- `{name}`: {value}" for name, value in checks.items())
    lines += ["", "## Warnings", ""] + [f"- {warning}" for warning in warnings]
    if errors: lines += ["", "## Errors", ""] + [f"- {error}" for error in errors]
    (OPS_ROOT / "validation-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"json_documents={checks.get('json_documents_parsed', 0)}")
    print(f"sources={checks.get('source_ids_reconciled', 0)}")
    print(f"segments={checks.get('segment_ids_reconciled', 0)}")
    print(f"caption_lines={checks.get('caption_lines_covered', 0)}")
    print(f"promotion_candidates={checks.get('promotion_candidates_reconciled', 0)}")
    print(f"timeline_candidates={checks.get('timeline_candidates_reconciled', 0)}")
    print("SEMANTIC_VALIDATION_OK" if not errors else "SEMANTIC_VALIDATION_FAILED")
    if errors: raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
