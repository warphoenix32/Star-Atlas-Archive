#!/usr/bin/env python3
"""Close the evidence-bounded completeness gate for the Star Atlas Medium corpus."""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("star_atlas_medium_campaign", HERE / "medium_campaign.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load medium_campaign.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mc = load_campaign_module()

GATE_REPORT = HERE / "completion-gate-report.json"
GATE_REPORT_MD = HERE / "completion-gate-report.md"
BODY_AUDIT = HERE / "full-body-audit.json"
BODY_AUDIT_MD = HERE / "full-body-audit.md"
UNRESOLVED_LEDGER = HERE / "unresolved-evidence-ledger.json"


PROMOTIONS: dict[str, dict[str, str]] = {
    "https://medium.com/star-atlas/the-truth-about-gerio-part-i-star-atlas-roadmap-scan-16-25df4fc5ac8": {
        "post_id": "25df4fc5ac8",
        "title": "The Truth about Gerio — Part I: Star Atlas Roadmap Scan #16",
    },
    "http://medium.com/star-atlas/2022-inaugural-spaceship-nft-drop-golden-age-of-space-exploration-759328e6949": {
        "post_id": "759328e6949",
        "canonical_url": "https://medium.com/star-atlas/2022-inaugural-spaceship-nft-drop-golden-age-of-space-exploration-759328e6949",
        "title": "Equipping the World for the Golden Age of Space Exploration: Inaugural 2022 Spaceship NFT Drop",
    },
    "https://medium.com/star-atlas/star-atlas-3rd-generation-ship-configuration-system-9c067d2e681": {
        "post_id": "9c067d2e681",
        "title": "Star Atlas Reveals the Third Generation of the Ship Configuration System",
    },
    "http://medium.com/star-atlas/firmam3ntal-star-makers-digital-fashion-collection-star-atlas-the-fabricant-f95b87d1c34": {
        "post_id": "f95b87d1c34",
        "canonical_url": "https://medium.com/star-atlas/firmam3ntal-star-makers-digital-fashion-collection-star-atlas-the-fabricant-f95b87d1c34",
        "title": "FIRMAM3NTAL: STAR✶MAKERS — Inaugural Collection by Star Atlas and The Fabricant Levels Up World’s Digital Fashion",
    },
    "https://medium.com/star-atlas/star-atlas-releases-its-inaugural-triple-a-state-of-the-economy-report-b06f3b8d9b4": {
        "post_id": "b06f3b8d9b4",
        "title": "Star Atlas Releases its Inaugural Triple-A State of the Economy Report",
    },
    "https://medium.com/star-atlas/star-atlas-nft-ancient-artifact-ustur-de789d607b7": {
        "post_id": "de789d607b7",
        "title": "Star Atlas NFT Cosmos: The Hunt for an Ancient Artifact — Part II",
    },
    "https://medium.com/star-atlas/thrilling-to-the-core-star-atlas-releases-epic-graphic-novel-dc499866cc2": {
        "post_id": "dc499866cc2",
        "title": "Thrilling to the CORE — Star Atlas Releases Epic Graphic Novel",
    },
    "https://medium.com/star-atlas/the-council-of-peace-academy-mission-showroom-star-atlas-roadmap-scan-21-36f38988861": {
        "post_id": "36f38988861",
        "title": "The Council of Peace Academy — Mission Showroom: Star Atlas Roadmap Scan #21",
    },
}


PROFILE_ONLY_EXCLUSIONS = {
    "https://staratlasgame.medium.com/intriguing-47f657cda3ee": "MEDIUM_RESPONSE_NOT_PUBLICATION_ARTICLE",
    "https://staratlasgame.medium.com/also-the-assets-in-the-whitepaper-are-placeholder-and-the-whitepaper-is-still-version-0-9-0-507177d91e19": "MEDIUM_RESPONSE_NOT_PUBLICATION_ARTICLE",
    "https://staratlasgame.medium.com/a-metaverse-meld-the-star-atlas-the-sandbox-unite-for-a-game-jam-contest-8abae8d00bcb": "PROFILE_ONLY_STORY_NOT_STAR_ATLAS_PUBLICATION_ARTICLE",
    "https://staratlasgame.medium.com/the-4-rs-of-spaceship-maintenance-e7cdd0d8cc98": "MEDIUM_RESPONSE_NOT_PUBLICATION_ARTICLE",
    "https://staratlasgame.medium.com/rest-assured-all-assets-within-the-game-will-be-of-unique-design-ea8d9aa5689e": "MEDIUM_RESPONSE_NOT_PUBLICATION_ARTICLE",
}


DUPLICATE_TARGETS = {
    "https://link.medium.com/cCduh3UCunb": "SRC-MEDIUM-STARATLAS-6CA8802140AB",
    "https://link.medium.com/qwos2ITw8gb": "SRC-MEDIUM-STARATLAS-347373550343",
    "https://link.medium.com/aD57RTDFSrb": "SRC-MEDIUM-STARATLAS-B4ECA8191D8C",
    "http://medium.com/star-atlas/star-atlas-animoca-brands-3-mil": "SRC-MEDIUM-STARATLAS-CF86A8057F8D",
    "http://medium.com/star-atlas/galactic-marketplace-solana-serum-powered-core-of-star-atlas-nft-trading-7a18d2d3337126": "SRC-MEDIUM-STARATLAS-7A18D2D33371",
    "https://medium.com/star-atlas/animoca-brands-joins-star-atlas-partnership-revolutionize-future-entertai": "SRC-MEDIUM-STARATLAS-B0FC33E9E8A5",
    "https://medium.com/star-atlas/yield-guild-games-commits-1-mil": "SRC-MEDIUM-STARATLAS-441076DA533E",
    "https://medium.com/star-atlas/star-atlas-joins-blockchain-game-al": "SRC-MEDIUM-STARATLAS-3CBD81910C71",
    "https://medium.com/star-atlas/never-alone-a-shared-social-adventure-across-the-star-atlas-galaxy": "SRC-MEDIUM-STARATLAS-89CD90627234",
    "http://medium.com/star-atlas/star-atlas-token-sale-details-revealed-857bf7505f%C4%91": "SRC-MEDIUM-STARATLAS-857BF7505FDD",
    "http://medium.com/star-atlas/star-atlas-partners-with-sperasoft-immersive-metaverse-exploration-ga": "SRC-MEDIUM-STARATLAS-2037AE0D6666",
    "http://medium.com/star-atlas/a-metaverse-col": "SRC-MEDIUM-STARATLAS-CBB7DFE74C89",
    "https://medium.com/star-atlas/star-atlas-releases-its-inaugural-triple-a-state-of-the-economy": "SRC-MEDIUM-STARATLAS-B06F3B8D9B4",
    "https://medium.com/star-atlas/join-the-fleet-star-atlas-launches-its-inaugural-on-chain-gameplay-exper": "SRC-MEDIUM-STARATLAS-7661221574A1",
}


NEWSLETTER_SURFACES = {"https://link.medium.com/GU7Oiufwjzb"}


UNRESOLVED_SHORTLINKS = {
    "https://link.medium.com/KklcuPPChDb",
    "https://link.medium.com/lkwxbjr9Enb",
    "https://link.medium.com/9bdLazeJpEb",
    "https://link.medium.com/ZER0IEOBYrb",
}


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def refresh_campaign_reports() -> None:
    """Reconcile campaign and outer manifests after gate-local artifacts change."""
    manifest = read_json(mc.URL_MANIFEST, {}) or {}
    results = (read_json(mc.RETRIEVAL_LEDGER, {}) or {}).get("results", [])
    if manifest.get("records") and results:
        mc.generate_reports(manifest, results)


def excluded(record: dict[str, Any], reason: str) -> None:
    mc.excluded(record, reason)
    record["completion_gate_disposition"] = reason
    record["completion_gate_review_required"] = False


def apply_adjudications() -> int:
    manifest = read_json(mc.URL_MANIFEST, {}) or {}
    records = manifest.get("records", [])
    queue = read_json(mc.MANUAL_REVIEW, {}) or {}
    deferred = queue.get("records", [])
    if not deferred:
        deferred = [item for item in records if item.get("inclusion_status") == "DEFERRED"]
    by_url = {item["canonical_url"]: item for item in records}
    by_source = {item["source_id"]: item for item in records}
    prior_report = read_json(GATE_REPORT, {}) or {}
    completed_at = prior_report.get("completed_at") or mc.now_iso()
    decisions: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []

    for prior in sorted(deferred, key=lambda item: item["canonical_url"]):
        url = prior["canonical_url"]
        record = by_url.get(url)
        if record is None:
            raise RuntimeError(f"Deferred record disappeared from manifest: {url}")
        original_source_id = record["source_id"]
        decision: dict[str, Any] = {
            "candidate_source_id": original_source_id,
            "candidate_url": url,
            "prior_status": record.get("inclusion_status"),
        }

        if url in PROMOTIONS:
            details = PROMOTIONS[url]
            canonical = details.get("canonical_url", url).replace("http://medium.com/", "https://medium.com/")
            post_id = details["post_id"]
            new_source_id = mc.source_id(post_id, canonical)
            record["canonical_url"] = canonical
            record["medium_post_id"] = post_id
            record["recovered_post_id"] = post_id
            record["source_id"] = new_source_id
            record["title"] = details["title"]
            record["identity_status"] = "OFFICIAL_PUBLICATION_ARTICLE_CONFIRMED_FOR_RETRIEVAL"
            record["inclusion_status"] = "INCLUDED"
            record["exclusion_reason"] = None
            record["manual_review_required"] = False
            record["manual_review_reasons"] = []
            record["retrieval_status"] = "PENDING"
            record["retrieval_method"] = None
            record["adjudication_status"] = "RESOLVED_INCLUDED"
            record["completion_gate_disposition"] = "PROMOTED_AFTER_LIVE_ARTICLE_IDENTITY_RECOVERY"
            record["completion_gate_review_required"] = False
            record["observed_urls"] = sorted(set(record.get("observed_urls", [])) | {url, canonical})
            record["discovery_sources"] = sorted(set(record.get("discovery_sources", [])) | {"completion_gate:live_article_identity"})
            for field in ("deferral_reason", "required_artifact", "next_action"):
                record.pop(field, None)
            decision.update(
                {
                    "final_status": "INCLUDED",
                    "disposition": record["completion_gate_disposition"],
                    "promoted_source_id": new_source_id,
                    "medium_post_id": post_id,
                    "evidence": [canonical, "LIVE_ARTICLE_METADATA_AND_COMPLETE_BODY_REQUIRED_DURING_RETRIEVAL"],
                }
            )
            by_source[new_source_id] = record
        elif url in PROFILE_ONLY_EXCLUSIONS:
            reason = PROFILE_ONLY_EXCLUSIONS[url]
            excluded(record, reason)
            decision.update({"final_status": "EXCLUDED", "disposition": reason, "evidence": [url, "PUBLICATION_MEMBERSHIP_NOT_ESTABLISHED"]})
        elif url in DUPLICATE_TARGETS:
            target_id = DUPLICATE_TARGETS[url]
            target = by_source.get(target_id)
            if target is None:
                raise RuntimeError(f"Duplicate target is absent: {url} -> {target_id}")
            target["observed_urls"] = sorted(set(target.get("observed_urls", [])) | set(record.get("observed_urls", [])) | {url})
            record["duplicate_of_source_id"] = target_id
            reason = "RESOLVED_VARIANT_OR_SHORTLINK_DUPLICATES_INCLUDED_ARTICLE"
            excluded(record, reason)
            decision.update(
                {
                    "final_status": "EXCLUDED",
                    "disposition": reason,
                    "duplicate_of_source_id": target_id,
                    "evidence": [url, "SURVIVING_SOURCE_CONTEXT_OR_DISTINCTIVE_SLUG_MATCH"],
                }
            )
        elif url in NEWSLETTER_SURFACES:
            reason = "NEWSLETTER_SIGNUP_SURFACE_NOT_ARTICLE"
            excluded(record, reason)
            decision.update({"final_status": "EXCLUDED", "disposition": reason, "evidence": [url, "SURVIVING_SOURCE_CONTEXT_IDENTIFIES_NEWSLETTER_SIGNUP"]})
        elif url in UNRESOLVED_SHORTLINKS:
            reason = "UNRESOLVED_SHORTLINK_NO_SURVIVING_TARGET_OR_PUBLICATION_IDENTITY"
            excluded(record, reason)
            record["evidence_gap"] = True
            record["future_artifact_trigger"] = "A historical redirect capture or original message embed exposing the target URL."
            gap = {
                "candidate_source_id": original_source_id,
                "url": url,
                "gap_type": "MISSING_HISTORICAL_SHORTLINK_TARGET",
                "last_live_result": "GENERIC_BRANCH_LANDING_PAGE_WITHOUT_TARGET",
                "required_artifact": record["future_artifact_trigger"],
                "corpus_effect": "Not included because official Star Atlas publication membership cannot be established.",
            }
            unresolved.append(gap)
            decision.update({"final_status": "EXCLUDED", "disposition": reason, "evidence_gap": gap})
        else:
            reason = "MALFORMED_WAYBACK_CRAWL_ARTIFACT_WITHOUT_STABLE_ARTICLE_IDENTITY"
            excluded(record, reason)
            decision.update(
                {
                    "final_status": "EXCLUDED",
                    "disposition": reason,
                    "evidence": [
                        url,
                        "WAYBACK_CDX_ORIGINAL_URL_CONTAINS_TRUNCATION_POLLUTION_OR_NO_MEDIUM_POST_ID",
                    ],
                }
            )
        decisions.append(decision)

    records.sort(key=lambda item: (item["source_id"], item["canonical_url"]))
    manifest["records"] = records
    counts = collections.Counter(item.get("inclusion_status") for item in records)
    manifest["adjudication"] = {
        **manifest.get("adjudication", {}),
        "method": "DETERMINISTIC_OFFLINE_CANDIDATE_ADJUDICATION_V2_WITH_COMPLETION_GATE",
        "completion_gate_completed_at": completed_at,
        "completion_gate_decisions": len(decisions),
        "counts": dict(sorted(counts.items())),
    }
    core = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    manifest["manifest_sha256"] = mc.sha256_bytes(json.dumps(core, ensure_ascii=False, sort_keys=True).encode())
    write_json(mc.URL_MANIFEST, manifest)

    write_json(mc.EXCLUSION_LEDGER, {"campaign_id": mc.CAMPAIGN_ID, "records": [item for item in records if item.get("inclusion_status") == "EXCLUDED"]})
    write_json(
        mc.MANUAL_REVIEW,
        {
            "campaign_id": mc.CAMPAIGN_ID,
            "queue_status": "CLOSED_NO_HUMAN_ADJUDICATION_PENDING",
            "records": [item for item in records if item.get("manual_review_required")],
        },
    )
    clusters = [
        {
            "medium_post_id": item.get("medium_post_id"),
            "source_id": item["source_id"],
            "canonical_url": item["canonical_url"],
            "observed_urls": item.get("observed_urls", []),
            "redirect_chain": item.get("redirect_chain", []),
            "duplicate_basis": "MEDIUM_POST_ID" if len(item.get("observed_urls", [])) > 1 else None,
        }
        for item in records
        if len(item.get("observed_urls", [])) > 1 or item.get("redirect_chain")
    ]
    write_json(mc.DUPLICATE_LEDGER, {"campaign_id": mc.CAMPAIGN_ID, "clusters": clusters})
    write_json(
        UNRESOLVED_LEDGER,
        {
            "campaign_id": mc.CAMPAIGN_ID,
            "gate_status": "TERMINAL_EXTERNAL_EVIDENCE_GAPS_DOCUMENTED",
            "records": unresolved,
        },
    )

    adjudication = read_json(mc.ADJUDICATION_LEDGER, {}) or {}
    historical_decisions = adjudication.get("decisions", [])
    completion_by_url = {item["candidate_url"]: item for item in decisions}
    for item in historical_decisions:
        update = completion_by_url.get(item.get("canonical_url"))
        if not update:
            continue
        item["final_inclusion_status"] = update["final_status"]
        item["adjudication_status"] = "RESOLVED_INCLUDED" if update["final_status"] == "INCLUDED" else "RESOLVED_EXCLUDED"
        item["reason"] = update["disposition"]
        item["promoted_source_id"] = update.get("promoted_source_id")
        item["duplicate_of_source_id"] = update.get("duplicate_of_source_id")
        item["required_artifact"] = (update.get("evidence_gap") or {}).get("required_artifact")
        item["next_action"] = "Reopen only if the named external artifact is supplied." if update.get("evidence_gap") else None
        item["last_attempt"] = "MEDIUM_COMPLETION_GATE_2026-07-21"
    status_counts = collections.Counter(item.get("final_inclusion_status") for item in historical_decisions)
    adjudication.update(
        {
            "decisions": historical_decisions,
            "explicitly_deferred": status_counts.get("DEFERRED", 0),
            "resolved_excluded": status_counts.get("EXCLUDED", 0),
            "resolved_included": status_counts.get("INCLUDED", 0),
            "completion_gate_decisions": len(decisions),
        }
    )
    write_json(mc.ADJUDICATION_LEDGER, adjudication)

    report = {
        "campaign_id": mc.CAMPAIGN_ID,
        "completed_at": completed_at,
        "gate_status": "ADJUDICATION_COMPLETE_RETRIEVAL_AND_BODY_AUDIT_PENDING",
        "prior_confirmed_articles": 173,
        "newly_confirmed_articles": len(PROMOTIONS),
        "expected_confirmed_articles": 173 + len(PROMOTIONS),
        "deferred_candidates_reviewed": len(decisions),
        "candidate_decision_counts": dict(sorted(collections.Counter(item["disposition"] for item in decisions).items())),
        "manifest_disposition_counts": dict(sorted(counts.items())),
        "human_adjudication_pending": 0,
        "external_evidence_gaps": len(unresolved),
        "publication_completeness_claim": "NOT_ASSERTED_MEDIUM_DISCOVERY_SURFACES_ARE_NONEXHAUSTIVE",
        "decisions": decisions,
    }
    write_json(GATE_REPORT, report)
    render_gate_report(report)
    print(f"Completion adjudication applied: {len(decisions)} decisions; {counts.get('INCLUDED', 0)} included; {len(unresolved)} terminal external gaps")
    return 0


def render_gate_report(report: dict[str, Any]) -> None:
    counts = report.get("manifest_disposition_counts", {})
    expected = report.get("expected_confirmed_articles", report.get("full_body_audit", {}).get("articles_audited", "PENDING"))
    lines = [
        "# Star Atlas Medium Completion Gate",
        "",
        f"- Gate status: **{report['gate_status']}**",
        f"- Confirmed official-publication articles expected: **{expected}**",
        f"- Newly confirmed articles: **{report.get('newly_confirmed_articles', 'PENDING')}**",
        f"- Deferred candidates reviewed: **{report.get('deferred_candidates_reviewed', 'PENDING')}**",
        f"- Remaining human adjudication: **{report.get('human_adjudication_pending', 'PENDING')}**",
        f"- Terminal external-evidence gaps: **{report.get('external_evidence_gaps', 'PENDING')}**",
        f"- Manifest dispositions: `{json.dumps(counts, sort_keys=True)}`",
        "",
        "## Boundary",
        "",
        "The gate closes every known candidate with an evidence-qualified terminal disposition. It does not claim that Medium's non-exhaustive historical surfaces prove that no undiscovered or deleted publication story exists.",
        "",
        "Profile-only stories and responses remain documented but outside the approved official-publication corpus boundary.",
    ]
    write_text(GATE_REPORT_MD, "\n".join(lines))


def full_body_audit() -> int:
    manifest = read_json(mc.URL_MANIFEST, {}) or {}
    included = [item for item in manifest.get("records", []) if item.get("inclusion_status") == "INCLUDED"]
    results: list[dict[str, Any]] = []
    errors: list[str] = []
    for record in included:
        sid = record["source_id"]
        raw_dir = mc.RAW_ROOT / sid
        retrieval = read_json(raw_dir / "retrieval.json", {}) or {}
        normalized = read_json(mc.NORMALIZED_ROOT / f"{sid}.json", {}) or {}
        source_record = read_json(mc.SOURCE_RECORD_ROOT / f"{sid}.json", {}) or {}
        package = read_json(mc.EXTRACTION_ROOT / f"{sid}.json", {}) or {}
        raw_value = retrieval.get("selected_raw_path")
        raw_path = mc.REPO_ROOT / raw_value if raw_value else None
        checks: dict[str, bool] = {
            "raw_exists": bool(raw_path and raw_path.exists()),
            "normalized_json_exists": bool(normalized),
            "normalized_markdown_exists": (mc.NORMALIZED_ROOT / f"{sid}.md").exists(),
            "source_record_json_exists": bool(source_record),
            "source_record_markdown_exists": (mc.SOURCE_RECORD_ROOT / f"{sid}.md").exists(),
            "ingestion_package_exists": bool(package),
        }
        extracted_text = ""
        if raw_path and raw_path.exists():
            checks["raw_sha256_matches"] = mc.sha256_file(raw_path) == retrieval.get("raw_sha256")
            selected = {
                "final_url": retrieval.get("final_url", record["canonical_url"]),
                "requested_url": retrieval.get("requested_url", record["canonical_url"]),
                "status": retrieval.get("http_status"),
                "retrieval_tier": retrieval.get("selected_tier"),
            }
            regenerated = mc.extract_article(raw_path.read_text(encoding="utf-8"), record, selected)
            extracted_text = regenerated.get("article_text", "")
            checks["raw_reextract_matches_normalized_text"] = extracted_text == normalized.get("article_text")
            checks["raw_reextract_hash_matches"] = regenerated.get("content_sha256") == normalized.get("content_sha256")
        checks["content_hash_matches_text"] = hashlib.sha256(normalized.get("article_text", "").encode()).hexdigest() == normalized.get("content_sha256")
        checks["post_id_matches"] = normalized.get("source", {}).get("medium_post_id") == record.get("medium_post_id")
        checks["source_id_matches"] = normalized.get("source", {}).get("source_id") == sid == source_record.get("source_id")
        checks["complete_body_marker"] = normalized.get("quality", {}).get("completeness") == "COMPLETE_ARTICLE_DOM"
        checks["substantive_text"] = len(extracted_text or normalized.get("article_text", "")) >= 400
        failed = sorted(name for name, passed in checks.items() if not passed)
        if failed:
            errors.append(f"{sid}: {', '.join(failed)}")
        results.append(
            {
                "source_id": sid,
                "medium_post_id": record.get("medium_post_id"),
                "canonical_url": record.get("canonical_url"),
                "title": normalized.get("source", {}).get("title"),
                "text_characters": len(normalized.get("article_text", "")),
                "text_words": len(normalized.get("article_text", "").split()),
                "retrieval_tier": retrieval.get("selected_tier"),
                "checks": checks,
                "result": "PASS" if not failed else "FAIL",
                "failures": failed,
            }
        )
    report = {
        "campaign_id": mc.CAMPAIGN_ID,
        "audit_scope": "ALL_CONFIRMED_OFFICIAL_PUBLICATION_ARTICLES",
        "articles_audited": len(results),
        "articles_passed": sum(item["result"] == "PASS" for item in results),
        "articles_failed": sum(item["result"] == "FAIL" for item in results),
        "result": "PASS" if not errors else "FAIL",
        "errors": errors,
        "records": results,
    }
    write_json(BODY_AUDIT, report)
    lines = [
        "# Star Atlas Medium Full-Body Audit",
        "",
        f"**Result: {report['result']}**",
        "",
        f"- Articles audited: {report['articles_audited']}",
        f"- Articles passed: {report['articles_passed']}",
        f"- Articles failed: {report['articles_failed']}",
        "",
        "Each raw HTML capture was checksum-verified, re-extracted, and compared exactly against its normalized article text and content checksum. Paired Markdown, Source Record, and ingestion-package artifacts were also required.",
    ]
    if errors:
        lines += ["", "## Errors", ""] + [f"- {item}" for item in errors]
    write_text(BODY_AUDIT_MD, "\n".join(lines))
    gate = read_json(GATE_REPORT, {}) or {}
    gate["full_body_audit"] = {key: report[key] for key in ("articles_audited", "articles_passed", "articles_failed", "result")}
    gate["gate_status"] = "COMPLETE_WITH_DOCUMENTED_EXTERNAL_EVIDENCE_GAPS" if not errors else "BLOCKED_BODY_AUDIT_FAILED"
    write_json(GATE_REPORT, gate)
    render_gate_report(gate)
    refresh_campaign_reports()
    print(f"Full-body audit {report['result']}: {report['articles_passed']}/{report['articles_audited']}")
    return 0 if not errors else 2


def verify_determinism() -> int:
    before = mc.normalized_output_fingerprint()
    result = mc.retrieve()
    after = mc.normalized_output_fingerprint()
    report = {
        "campaign_id": mc.CAMPAIGN_ID,
        "method": "SHA-256 over sorted relative paths and bytes, before and after a cached retrieve rerun",
        "output_roots": [mc.rel(mc.NORMALIZED_ROOT), mc.rel(mc.SOURCE_RECORD_ROOT), mc.rel(mc.PACKAGE_ROOT)],
        "before_sha256": before,
        "after_sha256": after,
        "match": before == after,
        "verified_at": mc.now_iso(),
        "cached_retrieve_exit_code": result,
    }
    write_json(HERE / "determinism-report.json", report)
    refresh_campaign_reports()
    print(f"Determinism {'PASS' if report['match'] and result == 0 else 'FAIL'}: {before} -> {after}")
    return 0 if report["match"] and result == 0 else 2


def validate_gate() -> int:
    errors: list[str] = []
    manifest = read_json(mc.URL_MANIFEST, {}) or {}
    records = manifest.get("records", [])
    included = [item for item in records if item.get("inclusion_status") == "INCLUDED"]
    deferred = [item for item in records if item.get("inclusion_status") == "DEFERRED"]
    queue = (read_json(mc.MANUAL_REVIEW, {}) or {}).get("records", [])
    gate = read_json(GATE_REPORT, {}) or {}
    body = read_json(BODY_AUDIT, {}) or {}
    unresolved = (read_json(UNRESOLVED_LEDGER, {}) or {}).get("records", [])
    expected_ids = {f"SRC-MEDIUM-STARATLAS-{item['post_id'].upper()}" for item in PROMOTIONS.values()}
    found_ids = {item["source_id"] for item in included}
    if len(included) != 181:
        errors.append(f"Expected 181 included articles, found {len(included)}")
    if deferred:
        errors.append(f"Deferred candidates remain: {len(deferred)}")
    if queue:
        errors.append(f"Manual-review queue is not closed: {len(queue)}")
    if not expected_ids <= found_ids:
        errors.append(f"Newly recovered article IDs missing: {sorted(expected_ids - found_ids)}")
    if body.get("result") != "PASS" or body.get("articles_audited") != len(included):
        errors.append("Full-body audit does not pass for every included article")
    if len(unresolved) != len(UNRESOLVED_SHORTLINKS):
        errors.append("Unresolved shortlink ledger does not reconcile")
    if gate.get("gate_status") != "COMPLETE_WITH_DOCUMENTED_EXTERNAL_EVIDENCE_GAPS":
        errors.append(f"Unexpected completion gate status: {gate.get('gate_status')}")
    changed = subprocess.run(
        ["git", "diff", "--name-only", "origin/main"],
        cwd=mc.REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    prohibited = [path for path in changed if path.startswith(("knowledge/", "graph/", "publication/"))]
    if prohibited:
        errors.append(f"Prohibited paths changed: {prohibited}")
    report = {
        "campaign_id": mc.CAMPAIGN_ID,
        "result": "PASS" if not errors else "FAIL",
        "included_articles": len(included),
        "deferred_candidates": len(deferred),
        "manual_review_items": len(queue),
        "external_evidence_gaps": len(unresolved),
        "full_body_audit_result": body.get("result"),
        "prohibited_path_changes": prohibited,
        "errors": errors,
    }
    write_json(HERE / "completion-gate-validation.json", report)
    write_text(
        HERE / "completion-gate-validation.md",
        "\n".join(
            [
                "# Star Atlas Medium Completion Gate Validation",
                "",
                f"**Result: {report['result']}**",
                "",
                f"- Included articles: {len(included)}",
                f"- Deferred candidates: {len(deferred)}",
                f"- Manual-review items: {len(queue)}",
                f"- External-evidence gaps: {len(unresolved)}",
                f"- Full-body audit: {body.get('result')}",
                f"- Prohibited path changes: {len(prohibited)}",
            ]
            + (["", "## Errors", ""] + [f"- {item}" for item in errors] if errors else [])
        ),
    )
    refresh_campaign_reports()
    print(f"Completion gate validation {report['result']}: {len(errors)} errors")
    return 0 if not errors else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("adjudicate", "audit", "determinism", "validate"))
    args = parser.parse_args()
    if args.command == "adjudicate":
        return apply_adjudications()
    if args.command == "audit":
        return full_body_audit()
    if args.command == "determinism":
        return verify_determinism()
    return validate_gate()


if __name__ == "__main__":
    raise SystemExit(main())
