#!/usr/bin/env python3
"""Validate the Star Atlas Lore Repository ingestion campaign."""

from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path
from typing import Any

from build_campaign import (
    ARCHIVE_MANIFEST_REL,
    CAMPAIGN_DIR,
    CAMPAIGN_ID,
    CAMPAIGN_REL,
    EXPECTED_ZIP_BYTES,
    EXPECTED_ZIP_SHA256,
    NORMALIZED_REL,
    PACKAGE_REL,
    RAW_ZIP_REL,
    ROOT,
    SOURCE_RECORDS_REL,
    SUPPORTED_REPOSITORY_TYPES,
    UPSTREAM_COMMIT,
    build,
    repository_text_bytes,
)


EXPECTED_COUNTS = {
    "repository_files_preserved": 526,
    "markdown_pages_inventoried": 490,
    "canon_pages": 192,
    "published_docs_pages": 201,
    "working_material_pages_preserved_excluded": 97,
    "normalized_source_pages": 192,
    "entities_extracted": 4632,
    "relationships_extracted": 3798,
    "media_inventoried": 2,
    "canon_media_extracted": 1,
    "mirror_divergences": 86,
    "unresolved_internal_links": 252,
    "unresolved_navigation_targets": 0,
    "migration_mappings": 9,
    "migration_mappings_requiring_review": 5,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "detail": detail}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def changed_paths() -> list[str]:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={ROOT.as_posix()}", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    paths = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path.replace("\\", "/"))
    return sorted(paths)


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    raw_zip = ROOT / RAW_ZIP_REL
    checks.append(check("raw_commit_archive_sha256", raw_zip.is_file() and sha256(raw_zip) == EXPECTED_ZIP_SHA256, sha256(raw_zip) if raw_zip.is_file() else None))
    checks.append(check("raw_commit_archive_byte_length", raw_zip.is_file() and raw_zip.stat().st_size == EXPECTED_ZIP_BYTES, raw_zip.stat().st_size if raw_zip.is_file() else None))

    with zipfile.ZipFile(raw_zip) as archive:
        names = [name for name in archive.namelist() if not name.endswith("/")]
        utf8_failures = []
        for name in names:
            if name.endswith((".md", ".json", ".jsonl", ".csv", ".py", ".yml", ".yaml", ".html", ".css", ".ps1", ".gitignore")):
                try:
                    archive.read(name).decode("utf-8-sig")
                except UnicodeDecodeError as exc:
                    utf8_failures.append({"path": name, "error": str(exc)})
    checks.append(check("source_snapshot_file_count", len(names) == EXPECTED_COUNTS["repository_files_preserved"], len(names)))
    checks.append(check("source_text_utf8", not utf8_failures, utf8_failures))

    expected = build()
    missing = []
    mismatched = []
    for relative_path, expected_bytes in expected.items():
        path = ROOT / relative_path
        if not path.is_file():
            missing.append(relative_path)
        elif path.read_bytes() != expected_bytes:
            mismatched.append(relative_path)
    checks.append(check("generated_artifacts_fixed_point", not missing and not mismatched, {"generated": len(expected), "missing": missing, "mismatched": mismatched}))
    checks.append(check("deterministic_build", expected == build(), len(expected)))

    json_failures = []
    jsonl_failures = []
    for relative_path, data in expected.items():
        if not relative_path.endswith((".json", ".jsonl", ".md")):
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            json_failures.append({"path": relative_path, "error": f"UTF-8: {exc}"})
            continue
        if relative_path.endswith(".json"):
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                json_failures.append({"path": relative_path, "error": str(exc)})
        elif relative_path.endswith(".jsonl"):
            for line_number, line in enumerate(text.splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    json.loads(line)
                except json.JSONDecodeError as exc:
                    jsonl_failures.append({"path": relative_path, "line": line_number, "error": str(exc)})
    checks.append(check("all_generated_json_parses", not json_failures, json_failures))
    checks.append(check("all_generated_jsonl_parses", not jsonl_failures, jsonl_failures))

    summary = json.loads((CAMPAIGN_DIR / "campaign-summary.json").read_text(encoding="utf-8"))
    count_mismatches = {key: {"expected": value, "observed": summary.get(key)} for key, value in EXPECTED_COUNTS.items() if summary.get(key) != value}
    checks.append(check("campaign_counts_reconcile", not count_mismatches, count_mismatches or EXPECTED_COUNTS))
    checks.append(check("upstream_commit_pinned", summary["upstream_commit"] == UPSTREAM_COMMIT, summary["upstream_commit"]))

    pages = load_jsonl(ROOT / NORMALIZED_REL / "pages.jsonl")
    page_ids = [item["source_id"] for item in pages]
    normalized_json = sorted((ROOT / NORMALIZED_REL / "pages").glob("*.json"))
    normalized_md = sorted((ROOT / NORMALIZED_REL / "pages").glob("*.md"))
    source_json = sorted((ROOT / SOURCE_RECORDS_REL).glob("*.json"))
    source_md = sorted((ROOT / SOURCE_RECORDS_REL).glob("*.md"))
    checks.append(check("source_ids_unique", len(page_ids) == len(set(page_ids)) == EXPECTED_COUNTS["normalized_source_pages"], len(page_ids)))
    checks.append(check("normalized_page_pairs_complete", len(normalized_json) == len(normalized_md) == len(pages), {"json": len(normalized_json), "markdown": len(normalized_md)}))
    checks.append(check("source_record_pairs_complete", len(source_json) == len(source_md) == len(pages), {"json": len(source_json), "markdown": len(source_md)}))
    pair_failures = []
    for page in pages:
        sid = page["source_id"]
        expected_paths = [
            ROOT / NORMALIZED_REL / "pages" / f"{sid}.json",
            ROOT / NORMALIZED_REL / "pages" / f"{sid}.md",
            ROOT / SOURCE_RECORDS_REL / f"{sid}.json",
            ROOT / SOURCE_RECORDS_REL / f"{sid}.md",
        ]
        if not all(path.is_file() for path in expected_paths):
            pair_failures.append(sid)
    checks.append(check("every_page_has_complete_artifact_chain", not pair_failures, pair_failures))

    entities = load_jsonl(ROOT / NORMALIZED_REL / "entities.jsonl")
    entity_ids = [item["entity_id"] for item in entities]
    entity_source_failures = [item["entity_id"] for item in entities if not item["source_ids"] or not set(item["source_ids"]).issubset(page_ids)]
    repository_type_failures = [item["entity_id"] for item in entities if item["repository_entity_type"] not in SUPPORTED_REPOSITORY_TYPES]
    checks.append(check("entity_ids_unique", len(entity_ids) == len(set(entity_ids)) == EXPECTED_COUNTS["entities_extracted"], len(entity_ids)))
    checks.append(check("entity_sources_reconcile", not entity_source_failures, entity_source_failures))
    checks.append(check("repository_entity_types_schema_compatible", not repository_type_failures, repository_type_failures))

    taxonomy = json.loads((ROOT / NORMALIZED_REL / "taxonomy.json").read_text(encoding="utf-8"))
    allowed_lore_types = {item for values in taxonomy["hierarchy"].values() for item in values}
    lore_type_failures = [item["entity_id"] for item in entities if item["lore_type"] not in allowed_lore_types]
    checks.append(check("controlled_lore_taxonomy_only", not lore_type_failures, lore_type_failures))
    checks.append(check(
        "authority_boundary_explicit",
        taxonomy["authority"]["scope"] == "IN_UNIVERSE_LORE_ONLY"
        and "ATMTA authorship or official publication status" in taxonomy["authority"]["does_not_establish"],
        taxonomy["authority"],
    ))

    relationships = load_jsonl(ROOT / NORMALIZED_REL / "relationships.jsonl")
    relationship_ids = [item["relationship_id"] for item in relationships]
    relationship_source_failures = [item["relationship_id"] for item in relationships if item["source_id"] not in page_ids]
    checks.append(check("relationship_ids_unique", len(relationship_ids) == len(set(relationship_ids)) == EXPECTED_COUNTS["relationships_extracted"], len(relationship_ids)))
    checks.append(check("relationship_sources_reconcile", not relationship_source_failures, relationship_source_failures))
    checks.append(check("relationships_are_evidence_bound_references", all(item["relationship_type"] == "REFERENCES" and item["provenance"]["line"] for item in relationships), len(relationships)))

    unresolved = json.loads((CAMPAIGN_DIR / "unresolved-reference-ledger.json").read_text(encoding="utf-8"))
    unresolved_relations = [item for item in relationships if item["resolution_status"] == "UNRESOLVED"]
    checks.append(check("unresolved_references_documented", len(unresolved_relations) == len(unresolved["relationships"]) == EXPECTED_COUNTS["unresolved_internal_links"], len(unresolved_relations)))

    inventory = json.loads((CAMPAIGN_DIR / "source-inventory.json").read_text(encoding="utf-8"))["files"]
    page_inventory = json.loads((CAMPAIGN_DIR / "page-inventory.json").read_text(encoding="utf-8"))["pages"]
    checks.append(check("repository_file_inventory_complete", len(inventory) == len(names) and len({item["path"] for item in inventory}) == len(names), len(inventory)))
    checks.append(check("every_markdown_page_inventoried", len(page_inventory) == EXPECTED_COUNTS["markdown_pages_inventoried"] and len({item["path"] for item in page_inventory}) == len(page_inventory), len(page_inventory)))
    checks.append(check("working_material_excluded_not_lost", sum(item["scope"] == "WORKING_DESIGN_MATERIAL" for item in page_inventory) == 97 and all(item["disposition"] == "PRESERVED_EXCLUDED_FROM_CANONICAL_LORE_NORMALIZATION" for item in page_inventory if item["scope"] == "WORKING_DESIGN_MATERIAL"), 97))

    media = load_jsonl(ROOT / NORMALIZED_REL / "media.jsonl")
    media_failures = []
    for item in media:
        if item["extracted_path"]:
            path = ROOT / item["extracted_path"]
            if not path.is_file() or sha256(path) != item["sha256"]:
                media_failures.append(item["media_id"])
    checks.append(check("media_inventory_and_extraction_reconcile", len(media) == 2 and not media_failures, {"count": len(media), "failures": media_failures}))

    migration = json.loads((CAMPAIGN_DIR / "taxonomy-migration-report.json").read_text(encoding="utf-8"))
    mappings = migration["migration_mappings"]
    checks.append(check("existing_lore_ids_all_mapped_or_deferred", len(mappings) == 9 and len({item["existing_id"] for item in mappings}) == 9 and all(item["status"] in {"MAPPED_ONE_TO_ONE", "AMBIGUOUS_MULTIPLE_TARGETS", "UNRESOLVED_NO_DIRECT_PAGE"} for item in mappings), len(mappings)))
    checks.append(check("historical_rewrites_prohibited", migration["automatic_historical_rewrites"] == 0 and all(not item["automatic_rewrite_allowed"] for item in mappings), 0))

    provenance = json.loads((ROOT / "archive/provenance/lore-repository/upstream-snapshot.json").read_text(encoding="utf-8"))
    checks.append(check(
        "provenance_branch_and_deployment_distinct",
        provenance["custody"]["selected_branch"] == "main"
        and provenance["custody"]["default_branch_at_capture"] == "master"
        and provenance["custody"]["deployment_branch"] == "gh-pages"
        and provenance["custody"]["commit"] == UPSTREAM_COMMIT,
        provenance["custody"],
    ))
    checks.append(check("license_uncertainty_preserved", provenance["license"]["status"] == "NO_LICENSE_DECLARED_AT_CAPTURE" and provenance["license"]["manual_review_required"], provenance["license"]))
    checks.append(check("official_affiliation_not_inferred", provenance["identity_observations"]["atmta_affiliation_independently_verified"] is False, provenance["identity_observations"]))

    package = json.loads((ROOT / PACKAGE_REL / "lore-repository-corpus.json").read_text(encoding="utf-8"))
    package_entity_failures = [item["entity_id"] for item in package["entities"] if item["entity_type"] not in SUPPORTED_REPOSITORY_TYPES or not item.get("canonical_name")]
    checks.append(check("schema_v21_package_minimum", package["metadata"]["repository_schema"] == "2.1" and isinstance(package["sources"], list) and not package_entity_failures, package_entity_failures))
    checks.append(check("ingestion_did_not_promote_knowledge_or_graph", package["metadata"]["promotion_status"] == "ARCHIVED_NOT_KNOWLEDGE_OR_GRAPH_PROMOTED" and not package["knowledge_delta"], package["metadata"]["promotion_status"]))

    manifest = json.loads((CAMPAIGN_DIR / "manifest.json").read_text(encoding="utf-8"))
    archive_manifest = json.loads((ROOT / ARCHIVE_MANIFEST_REL).read_text(encoding="utf-8"))
    manifest_failures = []
    for item in manifest["files"]:
        path = ROOT / item["path"]
        if not path.is_file():
            manifest_failures.append(item["path"])
            continue
        data = repository_text_bytes(path) if item.get("hash_mode") == "UTF8_LF" else path.read_bytes()
        if len(data) != item["byte_length"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            manifest_failures.append(item["path"])
    checks.append(check("campaign_and_archive_manifests_match", manifest == archive_manifest, len(manifest["files"])))
    checks.append(check("manifest_checksums_reconcile", not manifest_failures, manifest_failures))

    paths = changed_paths()
    prohibited = [path for path in paths if path.startswith(("knowledge/", "graph/", "publication/"))]
    allowed_prefixes = (
        "archive/raw/lore-repository/",
        "archive/provenance/lore-repository/",
        "archive/normalized/lore/",
        "archive/source-records/lore-repository/",
        "archive/ingestion-packages/lore-repository/",
        f"archive/manifests/{CAMPAIGN_ID}.json",
        f"operations/campaigns/{CAMPAIGN_ID}/",
        "operations/tests/lore_repository/",
        "operations/ci/validate_repository.py",
    )
    unexpected = [path for path in paths if not path.startswith(allowed_prefixes)]
    checks.append(check("prohibited_repository_domains_untouched", not prohibited, prohibited))
    checks.append(check("changed_paths_within_campaign_scope", not unexpected, unexpected))

    diff_check = subprocess.run(
        ["git", "-c", f"safe.directory={ROOT.as_posix()}", "diff", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    diff_detail = "clean" if diff_check.returncode == 0 else diff_check.stdout + diff_check.stderr
    checks.append(check("git_diff_check", diff_check.returncode == 0, diff_detail))

    status = "pass" if all(item["passed"] for item in checks) else "fail"
    return {
        "campaign_id": CAMPAIGN_ID,
        "status": status,
        "checks": checks,
        "summary": {
            "checks_passed": sum(item["passed"] for item in checks),
            "checks_total": len(checks),
            "generated_artifacts": len(expected),
            "source_pages": len(pages),
            "entities": len(entities),
            "relationships": len(relationships),
            "documented_upstream_warnings": json.loads((CAMPAIGN_DIR / "campaign-summary.json").read_text(encoding="utf-8"))["manual_review_conflicts"],
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Lore Repository Ingestion Validation",
        "",
        f"- Result: `{report['status'].upper()}`",
        f"- Checks passed: {report['summary']['checks_passed']} / {report['summary']['checks_total']}",
        f"- Source pages: {report['summary']['source_pages']}",
        f"- Entities: {report['summary']['entities']}",
        f"- Relationships: {report['summary']['relationships']}",
        f"- Documented upstream warning groups: {report['summary']['documented_upstream_warnings']}",
        "",
        "## Checks",
        "",
    ]
    for item in report["checks"]:
        lines.append(f"- [{'x' if item['passed'] else ' '}] `{item['name']}`")
    lines.extend([
        "",
        "## Interpretation",
        "",
        "A passing result means the preserved snapshot, generated artifact chains, controlled taxonomy, identifiers, manifests, and repository boundaries reconcile. It does not resolve the documented upstream identity, license, mirror, chronology, link, or legacy-mapping warnings.",
        "",
    ])
    return "\n".join(lines)


if __name__ == "__main__":
    report = validate()
    (CAMPAIGN_DIR / "validation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (CAMPAIGN_DIR / "validation-report.md").write_text(render_markdown(report), encoding="utf-8", newline="\n")
    print(json.dumps({"campaign_id": CAMPAIGN_ID, "status": report["status"], "checks": report["summary"]["checks_total"]}))
    raise SystemExit(0 if report["status"] == "pass" else 1)
