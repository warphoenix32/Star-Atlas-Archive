"""Validate the Phase 5 foundational publication portfolio without a network."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = Path(__file__).resolve().parent
PORTFOLIO_PATH = CAMPAIGN / "portfolio.json"
PUBLICATION_PLAN_PATH = CAMPAIGN / "publication-plan.json"
PROTOTYPE_DISPOSITIONS_PATH = CAMPAIGN / "prototype-dispositions.json"
MANIFEST_PATH = ROOT / "publication/manifests/publication-manifest.json"
SUMMARY_PATH = CAMPAIGN / "campaign-summary.json"
READINESS_PATH = CAMPAIGN / "knowledge-readiness-audit.json"
BACKLOG_PATH = CAMPAIGN / "targeted-knowledge-backlog.json"
VALIDATION_JSON = CAMPAIGN / "validation-report.json"
VALIDATION_MD = CAMPAIGN / "validation-report.md"
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
INTERNAL_BODY_TERMS = (
    "campaign_id:",
    "source_id:",
    "knowledge_status:",
    "assessment_source:",
    "[SRC-",
    "SA-DISCORD-ANN-",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    canonical = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def git_changed_paths(base_ref: str) -> list[str]:
    paths: set[str] = set()
    for args in (
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ):
        result = subprocess.run(
            args,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode == 0:
            paths.update(
                line.strip().replace("\\", "/")
                for line in result.stdout.splitlines()
                if line.strip()
            )
    return sorted(paths)


def parse_front_matter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("\"'")
    return fields, text[match.end() :]


def word_count(body: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", body, flags=re.UNICODE))


def validate_manifest(
    portfolio: dict[str, Any], manifest: dict[str, Any]
) -> tuple[list[str], dict[str, int]]:
    failures: list[str] = []
    metrics = {"entries": 0, "drafts": 0, "published": 0}
    if manifest.get("manifest_id") != "publication-manifest-star-atlas-library":
        failures.append("manifest_id does not satisfy the schema-compatible stable ID")
    if manifest.get("lifecycle_phase") != "PORTFOLIO_DEVELOPMENT":
        failures.append("manifest lifecycle_phase must be PORTFOLIO_DEVELOPMENT")
    if manifest.get("build_policy", {}).get("include_statuses") != ["PUBLISHED"]:
        failures.append("public build policy must include only PUBLISHED entries")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return failures + ["manifest entries must be an array"], metrics
    metrics["entries"] = len(entries)
    metrics["drafts"] = sum(entry.get("status") == "DRAFT" for entry in entries)
    metrics["published"] = sum(entry.get("status") == "PUBLISHED" for entry in entries)
    if len(entries) != 11:
        failures.append(f"expected 11 manifest entries, found {len(entries)}")
    ids = [entry.get("publication_id") for entry in entries]
    slugs = [entry.get("slug") for entry in entries]
    if ids != sorted(ids):
        failures.append("manifest entries are not sorted by publication_id")
    if len(ids) != len(set(ids)):
        failures.append("duplicate publication_id")
    if len(slugs) != len(set(slugs)):
        failures.append("duplicate publication slug")
    if any(entry.get("status") != "DRAFT" for entry in entries):
        failures.append("every initial portfolio entry must remain DRAFT")

    portfolio_by_id = {
        article["publication_id"]: article for article in portfolio.get("articles", [])
    }
    all_ids = set(ids)
    for entry in entries:
        publication_id = entry.get("publication_id", "UNKNOWN")
        article = portfolio_by_id.get(publication_id)
        if article is None:
            failures.append(f"{publication_id}: no portfolio source")
            continue
        content_value = entry.get("content_path")
        content_path = ROOT / content_value if isinstance(content_value, str) else None
        if content_path is None or not content_path.is_file():
            failures.append(f"{publication_id}: missing content path")
        else:
            expected_hash = entry.get("provenance", {}).get("content_sha256")
            if expected_hash != sha256(content_path):
                failures.append(f"{publication_id}: content checksum mismatch")
        for knowledge_path in entry.get("source_knowledge_paths", []):
            if not knowledge_path.startswith("knowledge/") or not (
                ROOT / knowledge_path
            ).is_file():
                failures.append(
                    f"{publication_id}: unresolved Knowledge input {knowledge_path}"
                )
        for related_id in entry.get("related_publication_ids", []):
            if related_id not in all_ids:
                failures.append(
                    f"{publication_id}: unresolved related publication {related_id}"
                )
        editorial = entry.get("editorial", {})
        evidence = entry.get("evidence", {})
        if editorial.get("human_first") is not True:
            failures.append(f"{publication_id}: human_first must be true")
        if any(
            editorial.get(field) is not False
            for field in (
                "narrative_review",
                "seo_review",
                "comprehensiveness_review",
            )
        ):
            failures.append(
                f"{publication_id}: human review flags must remain false before review"
            )
        if editorial.get("approval_record") is not None:
            failures.append(f"{publication_id}: draft must not have approval record")
        if evidence.get("material_claims_reviewed") is not False:
            failures.append(
                f"{publication_id}: material claim review must remain pending"
            )
        visibility = entry.get("visibility", {})
        if visibility != {
            "taxonomy": "HIDDEN",
            "source_ids": "EVIDENCE_PANEL",
            "workflow_metadata": "HIDDEN",
        }:
            failures.append(f"{publication_id}: visibility policy mismatch")
    return failures, metrics


def validate_articles(
    portfolio: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    word_counts: dict[str, int] = {}
    links_checked = 0
    for article in portfolio.get("articles", []):
        publication_id = article["publication_id"]
        path = ROOT / article["content_path"]
        if not path.is_file():
            failures.append(f"{publication_id}: missing article")
            continue
        fields, body = parse_front_matter(path)
        expected = {
            "publication_id": publication_id,
            "slug": article["slug"],
            "title": article["title"],
            "status": "DRAFT",
            "as_of": portfolio["as_of"],
        }
        for key, value in expected.items():
            if fields.get(key) != value:
                failures.append(
                    f"{publication_id}: front matter {key}={fields.get(key)!r}, expected {value!r}"
                )
        words = word_count(body)
        word_counts[publication_id] = words
        if words < 650:
            failures.append(f"{publication_id}: only {words} narrative words")
        if body.count("\n## ") < 4:
            failures.append(f"{publication_id}: insufficient narrative structure")
        if "## Explore the evidence" not in body:
            failures.append(f"{publication_id}: missing human-readable evidence panel")
        for term in INTERNAL_BODY_TERMS:
            if term.lower() in body.lower():
                failures.append(
                    f"{publication_id}: internal repository term leaked into narrative: {term}"
                )
        for match in LINK_RE.finditer(body):
            target = match.group(1).strip().strip("<>").split()[0]
            if not target or target.startswith("#") or re.match(
                r"^[A-Za-z][A-Za-z0-9+.-]*:", target
            ):
                continue
            links_checked += 1
            target_path = unquote(target.split("#", 1)[0])
            if not (path.parent / target_path).resolve().is_file():
                failures.append(
                    f"{publication_id}: broken link {match.group(1)}"
                )
    return failures, {
        "word_counts": dict(sorted(word_counts.items())),
        "total_words": sum(word_counts.values()),
        "links_checked": links_checked,
    }


def validate_scope(base_ref: str) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    changes = git_changed_paths(base_ref)
    prohibited = [
        path
        for path in changes
        if path.startswith(("archive/", "knowledge/", "graph/"))
    ]
    if prohibited:
        failures.append("prohibited path changes: " + ", ".join(prohibited))
    allowed_roots = (
        ".github/workflows/",
        "operations/ci/",
        "operations/campaigns/phase-5-foundational-publication-portfolio-2026-07/",
        "operations/tests/phase5_publication_portfolio/",
        "operations/tests/phase4_knowledge_consolidation/test_phase4_knowledge_consolidation.py",
        "operations/programs/library-roadmap/",
        "operations/coverage/campaign-status-register.json",
        "operations/coverage/campaign-status-register.md",
        "publication/articles/",
        "publication/manifests/publication-manifest.json",
        "publication/site/article.css",
        "publication/site/article.html",
        "publication/site/article.js",
        "publication/site/scripts/validate-site.mjs",
    )
    unexpected = [
        path for path in changes if not any(path.startswith(root) for root in allowed_roots)
    ]
    if unexpected:
        failures.append("unexpected path changes: " + ", ".join(unexpected))
    return failures, {
        "changed_paths": len(changes),
        "prohibited_path_changes": len(prohibited),
    }


def validate_community_packet() -> list[str]:
    packet = load_json(CAMPAIGN / "community-evidence-development.json")
    failures: list[str] = []
    if packet.get("decision") != "SUFFICIENT_FOR_BOUNDED_OVERVIEW":
        failures.append("community evidence decision is not bounded")
    if packet.get("human_semantic_review_required") is not True:
        failures.append("community article must require human semantic review")
    if not any(
        "Intergalactic Herald" in item
        for item in packet.get("explicit_exclusions", [])
    ):
        failures.append("operator exclusion for Intergalactic Herald is missing")
    for path in packet.get("knowledge_inputs", []):
        if not (ROOT / path).is_file():
            failures.append(f"community evidence input does not resolve: {path}")
    return failures


def validate_publication_plan(
    portfolio: dict[str, Any],
    plan: dict[str, Any],
    readiness: dict[str, Any],
    backlog: dict[str, Any],
) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    if (
        portfolio.get("portfolio_status")
        != "UNPUBLISHED_PROTOTYPES_SUPERSEDED_BY_PORTFOLIO_PLAN"
    ):
        failures.append("prototype portfolio status does not reflect the redesign")
    gateways = plan.get("gateways", [])
    pages = plan.get("foundational_pages", [])
    if len(gateways) != 8:
        failures.append(f"expected 8 reader gateways, found {len(gateways)}")
    if len(pages) != 30:
        failures.append(f"expected 30 foundational pages, found {len(pages)}")

    gateway_ids = [item.get("gateway_id") for item in gateways]
    page_ids = [item.get("candidate_id") for item in pages]
    if len(gateway_ids) != len(set(gateway_ids)):
        failures.append("duplicate reader gateway ID")
    if len(page_ids) != len(set(page_ids)):
        failures.append("duplicate foundational candidate ID")
    expected_ids = [f"PLAN-{number:03d}" for number in range(1, 31)]
    if sorted(page_ids) != expected_ids:
        failures.append("foundational candidate IDs do not reconcile to PLAN-001..030")

    controlled_readiness = {
        "READY_TO_DRAFT",
        "KNOWLEDGE_PROMOTION_REQUIRED",
        "ADDITIONAL_INGESTION_REQUIRED",
        "RESEARCH_COLLECTION",
        "DEFERRED",
    }
    for page in pages:
        candidate_id = page.get("candidate_id", "UNKNOWN")
        if page.get("readiness") not in controlled_readiness:
            failures.append(f"{candidate_id}: invalid readiness")
        if page.get("risk_class") not in {"R1", "R2", "R3", "R4", "R5"}:
            failures.append(f"{candidate_id}: invalid risk class")
        if not page.get("reader_question"):
            failures.append(f"{candidate_id}: missing reader question")
        if not page.get("missing_requirements"):
            failures.append(f"{candidate_id}: missing requirements are not explicit")
        for path_value in page.get("knowledge_inputs", []):
            if not (ROOT / path_value).exists():
                failures.append(f"{candidate_id}: unresolved input {path_value}")
        for path_value in page.get("prototype_inputs", []):
            if not (ROOT / path_value).is_file():
                failures.append(f"{candidate_id}: unresolved prototype {path_value}")

    expected_readiness = dict(
        sorted(Counter(page["readiness"] for page in pages).items())
    )
    if readiness.get("readiness_counts") != expected_readiness:
        failures.append("readiness audit counts do not reconcile to publication plan")
    if readiness.get("foundational_page_count") != len(pages):
        failures.append("readiness audit page count does not reconcile")
    readiness_ids = [item.get("candidate_id") for item in readiness.get("pages", [])]
    if sorted(readiness_ids) != sorted(page_ids):
        failures.append("readiness audit candidate IDs do not reconcile")

    blocked_ids = {
        page["candidate_id"]
        for page in pages
        if page["readiness"] != "READY_TO_DRAFT"
    }
    backlog_ids = {item.get("candidate_id") for item in backlog.get("items", [])}
    if backlog_ids != blocked_ids:
        failures.append("targeted Knowledge backlog does not reconcile to blocked pages")
    if backlog.get("backlog_item_count") != len(blocked_ids):
        failures.append("targeted Knowledge backlog count does not reconcile")

    dispositions = load_json(PROTOTYPE_DISPOSITIONS_PATH).get("dispositions", [])
    prototype_ids = {
        article["publication_id"] for article in portfolio.get("articles", [])
    }
    disposition_ids = {item.get("publication_id") for item in dispositions}
    if disposition_ids != prototype_ids:
        failures.append("prototype dispositions do not cover all and only prototypes")
    for item in dispositions:
        for target_id in item.get("target_candidate_ids", []):
            if target_id not in set(page_ids):
                failures.append(
                    f"{item.get('publication_id')}: unresolved planned destination {target_id}"
                )

    return failures, {
        "reader_gateways": len(gateways),
        "foundational_pages_planned": len(pages),
        "readiness_counts": expected_readiness,
        "knowledge_backlog_items": len(blocked_ids),
        "prototype_dispositions": len(dispositions),
    }


def validate_public_presentation() -> list[str]:
    failures: list[str] = []
    article_html = (ROOT / "publication/site/article.html").read_text(
        encoding="utf-8"
    )
    article_script = (ROOT / "publication/site/article.js").read_text(
        encoding="utf-8"
    )
    article_css = (ROOT / "publication/site/article.css").read_text(
        encoding="utf-8"
    )
    combined = "\n".join((article_html, article_script, article_css))
    for forbidden in ("record-metadata", "renderMetadata", "knowledge_status"):
        if forbidden in combined:
            failures.append(
                f"public knowledge reader still exposes machine metadata: {forbidden}"
            )
    if "stripFrontMatter" not in article_script:
        failures.append("public knowledge reader does not strip internal front matter")
    house_style = (CAMPAIGN / "EDITORIAL-HOUSE-STYLE.md").read_text(
        encoding="utf-8"
    )
    for required in (
        "Hologram News Network",
        "The main article is about Star Atlas",
        "must never render as a box at the top",
        "unsupported speculation",
    ):
        if required not in house_style:
            failures.append(f"editorial house style missing requirement: {required}")
    return failures


def run_validation(base_ref: str = "origin/main") -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    failures: list[str] = []
    metrics: dict[str, Any] = {}

    for name, path in (
        ("portfolio_json", PORTFOLIO_PATH),
        ("publication_plan_json", PUBLICATION_PLAN_PATH),
        ("prototype_dispositions_json", PROTOTYPE_DISPOSITIONS_PATH),
        ("manifest_json", MANIFEST_PATH),
        ("campaign_summary_json", SUMMARY_PATH),
        ("knowledge_readiness_json", READINESS_PATH),
        ("targeted_knowledge_backlog_json", BACKLOG_PATH),
        ("community_evidence_json", CAMPAIGN / "community-evidence-development.json"),
    ):
        try:
            load_json(path)
            checks.append({"check": name, "status": "PASS"})
        except Exception as exc:  # noqa: BLE001
            checks.append({"check": name, "status": "FAIL"})
            failures.append(f"{name}: {exc}")

    portfolio = load_json(PORTFOLIO_PATH)
    plan = load_json(PUBLICATION_PLAN_PATH)
    readiness = load_json(READINESS_PATH)
    backlog = load_json(BACKLOG_PATH)
    manifest = load_json(MANIFEST_PATH)
    manifest_failures, manifest_metrics = validate_manifest(portfolio, manifest)
    checks.append(
        {
            "check": "publication_manifest",
            "status": "PASS" if not manifest_failures else "FAIL",
        }
    )
    failures.extend(manifest_failures)
    metrics.update(manifest_metrics)

    article_failures, article_metrics = validate_articles(portfolio)
    checks.append(
        {
            "check": "article_structure_and_links",
            "status": "PASS" if not article_failures else "FAIL",
        }
    )
    failures.extend(article_failures)
    metrics.update(article_metrics)

    community_failures = validate_community_packet()
    checks.append(
        {
            "check": "community_evidence_boundary",
            "status": "PASS" if not community_failures else "FAIL",
        }
    )
    failures.extend(community_failures)

    plan_failures, plan_metrics = validate_publication_plan(
        portfolio, plan, readiness, backlog
    )
    checks.append(
        {
            "check": "publication_plan_and_readiness",
            "status": "PASS" if not plan_failures else "FAIL",
        }
    )
    failures.extend(plan_failures)
    metrics.update(plan_metrics)

    presentation_failures = validate_public_presentation()
    checks.append(
        {
            "check": "reader_first_public_presentation",
            "status": "PASS" if not presentation_failures else "FAIL",
        }
    )
    failures.extend(presentation_failures)

    scope_failures, scope_metrics = validate_scope(base_ref)
    checks.append(
        {
            "check": "repository_scope",
            "status": "PASS" if not scope_failures else "FAIL",
        }
    )
    failures.extend(scope_failures)
    metrics.update(scope_metrics)

    risk_counts = Counter(
        article["risk_class"] for article in portfolio.get("articles", [])
    )
    metrics["risk_class_counts"] = dict(sorted(risk_counts.items()))
    return {
        "campaign_id": portfolio["campaign_id"],
        "as_of": portfolio["as_of"],
        "status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "metrics": metrics,
        "failures": failures,
        "human_adjudication_required": True,
        "next_gate": "Human review of the complete portfolio map and readiness audit",
    }


def write_reports(result: dict[str, Any]) -> None:
    VALIDATION_JSON.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rows = "\n".join(
        f"| {item['check']} | {item['status']} |" for item in result["checks"]
    )
    failures = "\n".join(f"- {item}" for item in result["failures"]) or "- None."
    markdown = f"""# Phase 5 Publication Portfolio Validation

Result: **{result['status']}**

| Check | Status |
| --- | --- |
{rows}

## Metrics

- Manifest entries: {result['metrics']['entries']}
- Draft entries: {result['metrics']['drafts']}
- Published entries: {result['metrics']['published']}
- Narrative words: {result['metrics']['total_words']}
- Local evidence links checked: {result['metrics']['links_checked']}
- Prohibited path changes: {result['metrics']['prohibited_path_changes']}
- Risk classes: {json.dumps(result['metrics']['risk_class_counts'], sort_keys=True)}

## Failures

{failures}

Automated validation does not approve editorial judgment. All eleven articles
remain drafts outside the public build pending human semantic review.
"""
    VALIDATION_MD.write_text(markdown, encoding="utf-8", newline="\n")


def main() -> int:
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    result = run_validation(base_ref)
    write_reports(result)
    print(f"{result['status']} phase-5-foundational-publication-portfolio-2026-07")
    for failure in result["failures"]:
        print(f"FAIL {failure}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
