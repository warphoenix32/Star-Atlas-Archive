"""Build the deterministic Phase 5 draft publication manifest and reports."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = Path(__file__).resolve().parent
PORTFOLIO_PATH = CAMPAIGN / "portfolio.json"
PUBLICATION_PLAN_PATH = CAMPAIGN / "publication-plan.json"
PROTOTYPE_DISPOSITIONS_PATH = CAMPAIGN / "prototype-dispositions.json"
MANIFEST_PATH = ROOT / "publication/manifests/publication-manifest.json"
SUMMARY_JSON = CAMPAIGN / "campaign-summary.json"
SUMMARY_MD = CAMPAIGN / "campaign-summary.md"
AUDIENCE_MAP_MD = CAMPAIGN / "audience-navigation-map.md"
READINESS_JSON = CAMPAIGN / "knowledge-readiness-audit.json"
READINESS_MD = CAMPAIGN / "knowledge-readiness-audit.md"
BACKLOG_JSON = CAMPAIGN / "targeted-knowledge-backlog.json"
BACKLOG_MD = CAMPAIGN / "targeted-knowledge-backlog.md"
PROTOTYPE_DISPOSITIONS_MD = CAMPAIGN / "prototype-dispositions.md"
EDITORIAL_REVIEW_JSON = CAMPAIGN / "editorial-wave-1-review.json"
EDITORIAL_REVIEW_MD = CAMPAIGN / "editorial-wave-1-review.md"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    canonical = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def word_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^---.*?---", "", text, count=1, flags=re.DOTALL)
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def build_manifest(portfolio: dict[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for article in portfolio["articles"]:
        content_path = ROOT / article["content_path"]
        entries.append(
            {
                "publication_id": article["publication_id"],
                "slug": article["slug"],
                "title": article["title"],
                "type": "ARTICLE",
                "status": article.get("status", "DRAFT"),
                "audience": article["audience"],
                "content_path": article["content_path"],
                "source_knowledge_paths": article["source_knowledge_paths"],
                "as_of": portfolio["as_of"],
                "editorial": {
                    "human_first": True,
                    "narrative_review": False,
                    "seo_review": False,
                    "comprehensiveness_review": False,
                    "approval_record": None,
                },
                "evidence": {
                    "material_claims_reviewed": False,
                    "references_resolve": True,
                    "conflicts_disclosed": True,
                    "limitations_disclosed": True,
                },
                "presentation": {
                    "summary": article["summary"],
                    "description": article["description"],
                    "primary_topic": article["primary_topic"],
                    "related_topics": article["related_topics"],
                },
                "provenance": {
                    "content_sha256": sha256(content_path),
                    "manifested_at": portfolio["as_of"],
                    "manifested_by": portfolio["campaign_id"],
                },
                "visibility": {
                    "taxonomy": "HIDDEN",
                    "source_ids": "EVIDENCE_PANEL",
                    "workflow_metadata": "HIDDEN",
                },
                "related_publication_ids": article["related_publication_ids"],
                "revision_history": article.get("revision_history", []),
            }
        )
    entries.sort(key=lambda value: value["publication_id"])
    return {
        "manifest_version": "1.0",
        "manifest_id": "publication-manifest-star-atlas-library",
        "as_of": portfolio["as_of"],
        "lifecycle_phase": "PORTFOLIO_DEVELOPMENT",
        "public_base_path": "/library/",
        "source_of_truth": {
            "archive_root": "archive/",
            "knowledge_root": "knowledge/",
            "publication_root": "publication/",
        },
        "build_policy": {
            "include_statuses": ["PUBLISHED"],
            "exclude_internal_fields": [
                "editorial",
                "evidence",
                "provenance",
                "revision_history",
            ],
            "taxonomy_presentation": "HIDDEN",
            "ordering": "publication_id",
        },
        "entries": entries,
    }


def build_readiness(plan: dict[str, Any]) -> dict[str, Any]:
    pages = sorted(plan["foundational_pages"], key=lambda item: item["candidate_id"])
    return {
        "plan_id": plan["plan_id"],
        "as_of": plan["as_of"],
        "status": "COMPLETE",
        "foundational_page_count": len(pages),
        "readiness_counts": dict(
            sorted(Counter(page["readiness"] for page in pages).items())
        ),
        "collection_counts": dict(
            sorted(Counter(page["collection"] for page in pages).items())
        ),
        "pages": [
            {
                "candidate_id": page["candidate_id"],
                "working_title": page["working_title"],
                "collection": page["collection"],
                "priority": page["priority"],
                "readiness": page["readiness"],
                "risk_class": page["risk_class"],
                "knowledge_inputs": page["knowledge_inputs"],
                "missing_requirements": page["missing_requirements"],
            }
            for page in pages
        ],
    }


def build_backlog(plan: dict[str, Any]) -> dict[str, Any]:
    blocked = [
        page
        for page in plan["foundational_pages"]
        if page["readiness"] != "READY_TO_DRAFT"
    ]
    blocked.sort(key=lambda item: (item["priority"], item["candidate_id"]))
    return {
        "plan_id": plan["plan_id"],
        "as_of": plan["as_of"],
        "status": "OPEN",
        "backlog_item_count": len(blocked),
        "items": [
            {
                "rank": rank,
                "candidate_id": page["candidate_id"],
                "working_title": page["working_title"],
                "readiness": page["readiness"],
                "risk_class": page["risk_class"],
                "required_work": page["missing_requirements"],
                "knowledge_inputs": page["knowledge_inputs"],
            }
            for rank, page in enumerate(blocked, start=1)
        ],
    }


def build_summary(
    portfolio: dict[str, Any],
    manifest: dict[str, Any],
    plan: dict[str, Any],
    readiness: dict[str, Any],
    backlog: dict[str, Any],
) -> dict[str, Any]:
    words = {
        article["publication_id"]: word_count(ROOT / article["content_path"])
        for article in portfolio["articles"]
    }
    risk_counts = Counter(article["risk_class"] for article in portfolio["articles"])
    topic_counts = Counter(article["primary_topic"] for article in portfolio["articles"])
    return {
        "campaign_id": portfolio["campaign_id"],
        "as_of": portfolio["as_of"],
        "status": "EDITORIAL_WAVE_1_AWAITING_HUMAN_SEMANTIC_REVIEW",
        "portfolio": {
            "articles_drafted": len(portfolio["articles"]),
            "manifest_entries": len(manifest["entries"]),
            "draft_entries": sum(
                entry["status"] == "DRAFT" for entry in manifest["entries"]
            ),
            "in_review_entries": sum(
                entry["status"] == "IN_REVIEW" for entry in manifest["entries"]
            ),
            "published_entries": sum(
                entry["status"] == "PUBLISHED" for entry in manifest["entries"]
            ),
            "total_words": sum(words.values()),
            "word_counts": words,
            "risk_class_counts": dict(sorted(risk_counts.items())),
            "primary_topic_counts": dict(sorted(topic_counts.items())),
        },
        "portfolio_redesign": {
            "reader_gateways": len(plan["gateways"]),
            "foundational_pages_planned": len(plan["foundational_pages"]),
            "ready_to_draft": readiness["readiness_counts"].get(
                "READY_TO_DRAFT", 0
            ),
            "knowledge_promotion_required": readiness["readiness_counts"].get(
                "KNOWLEDGE_PROMOTION_REQUIRED", 0
            ),
            "targeted_backlog_items": backlog["backlog_item_count"],
            "prototype_dispositions": len(
                load_json(PROTOTYPE_DISPOSITIONS_PATH)["dispositions"]
            ),
            "house_style": (
                "HNN-inspired immediacy and community awareness with "
                "Archive evidence discipline"
            ),
        },
        "community_extension": {
            "publication_id": "PUB-011",
            "evidence_packet": (
                "operations/campaigns/phase-5-foundational-publication-portfolio-2026-07/"
                "community-evidence-development.json"
            ),
            "decision": "SUFFICIENT_FOR_BOUNDED_OVERVIEW",
            "future_knowledge_work_required_for_exhaustive_profiles": True,
        },
        "boundaries": {
            "archive_evidence_modified": False,
            "knowledge_modified": False,
            "graph_modified": False,
            "publication_site_modified": False,
            "publication_site_change": "No site or deployment change in Editorial Wave 1",
            "drafts_in_public_build": False,
            "intergalactic_herald_profile_included": False,
        },
        "human_adjudication_required": True,
        "human_review_scope": [
            "Review the seven Wave 1 articles for narrative accuracy and completeness",
            "Confirm lifecycle distinctions remain understandable to ordinary readers",
            "Confirm lore and community qualifications are proportionate",
            "Approve, revise or defer each article before publication",
        ],
        "next_gate": "Human semantic review of the seven Wave 1 articles",
    }


def write_editorial_review(
    portfolio: dict[str, Any], manifest: dict[str, Any]
) -> None:
    review_entries = [
        {
            "publication_id": entry["publication_id"],
            "title": entry["title"],
            "content_path": entry["content_path"],
            "status": entry["status"],
            "risk_class": next(
                article["risk_class"]
                for article in portfolio["articles"]
                if article["publication_id"] == entry["publication_id"]
            ),
            "human_approval": None,
            "review_questions": [
                "Is the narrative accurate, useful and sufficiently comprehensive?",
                "Are uncertainty and lifecycle distinctions visible without dominating the story?",
                "Is any material claim missing necessary context or qualification?",
            ],
        }
        for entry in manifest["entries"]
        if entry["status"] == "IN_REVIEW"
    ]
    review = {
        "campaign_id": portfolio["campaign_id"],
        "review_id": "phase-5-editorial-wave-1",
        "as_of": portfolio["as_of"],
        "status": "AWAITING_HUMAN_SEMANTIC_REVIEW",
        "publication_status": "UNPUBLISHED",
        "deployment_status": "NOT_STARTED",
        "articles": review_entries,
        "deferred": [
            {
                "subject": "Showroom and Holosim",
                "reason": "The existing combined prototype must be split into distinct product histories.",
            },
            {
                "subject": "SAGE product family",
                "reason": "Later articles must preserve distinct SAGE Labs, Starbased, SAGE 3D and C4 lifecycle states.",
            },
            {
                "subject": "Governance and institutional histories",
                "reason": "These remain outside Wave 1 while reader-first consolidation is planned.",
            },
        ],
        "human_adjudication_required": True,
    }
    EDITORIAL_REVIEW_JSON.write_text(
        json.dumps(review, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rows = "\n".join(
        f"| {item['publication_id']} | [{item['title']}](../../../{item['content_path']}) | "
        f"{item['risk_class']} | {item['status']} | Pending |"
        for item in review_entries
    )
    EDITORIAL_REVIEW_MD.write_text(
        "# Phase 5 Editorial Wave 1 Review\n\n"
        "Seven reader-first articles are ready for human semantic review. They "
        "remain outside the public build, have no approval record and have not "
        "been deployed.\n\n"
        "| ID | Article | Risk | State | Human decision |\n"
        "| --- | --- | --- | --- | --- |\n"
        f"{rows}\n\n"
        "## Review questions\n\n"
        "1. Is each narrative accurate, engaging and sufficiently comprehensive?\n"
        "2. Are lifecycle and evidence distinctions clear without overwhelming the story?\n"
        "3. Does any material claim need additional context, qualification or removal?\n"
        "4. Should the article be approved, revised or deferred?\n\n"
        "## Deferred from Wave 1\n\n"
        "- Split the combined Showroom and Holosim prototype into distinct histories.\n"
        "- Preserve distinct SAGE Labs, Starbased, SAGE 3D and C4 lifecycle narratives.\n"
        "- Consolidate governance and institutional prototypes in a later editorial wave.\n",
        encoding="utf-8",
        newline="\n",
    )


def write_planning_reports(
    plan: dict[str, Any],
    readiness: dict[str, Any],
    backlog: dict[str, Any],
    dispositions: dict[str, Any],
) -> None:
    collection_pages: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for page in plan["foundational_pages"]:
        collection_pages[page["collection"]].append(page)

    gateway_rows = "\n".join(
        f"| {gateway['title']} | {gateway['reader_purpose']} |"
        for gateway in plan["gateways"]
    )
    collection_sections = []
    for collection, pages in collection_pages.items():
        rows = "\n".join(
            "| {id} | {title} | {readiness} | {risk} |".format(
                id=page["candidate_id"],
                title=page["working_title"],
                readiness=page["readiness"],
                risk=page["risk_class"],
            )
            for page in sorted(pages, key=lambda item: item["priority"])
        )
        collection_sections.append(
            f"## {collection}\n\n"
            "| ID | Working title | Readiness | Risk |\n"
            "| --- | --- | --- | --- |\n"
            f"{rows}"
        )
    AUDIENCE_MAP_MD.write_text(
        "# Star Atlas Library Audience and Navigation Map\n\n"
        "The public Library begins with reader questions, not repository folders. "
        "Eight gateways lead into a planned thirty-page foundational narrative "
        "portfolio. Detailed dossiers and research records remain available below "
        "that introductory layer.\n\n"
        "## Reader gateways\n\n"
        "| Gateway | Reader purpose |\n"
        "| --- | --- |\n"
        f"{gateway_rows}\n\n"
        + "\n\n".join(collection_sections)
        + "\n\n## Deeper layers\n\n"
        "Entity dossiers cover lore, products, ships, people, guilds and events "
        "only after their evidence and canonical identities are ready. Ledgers, "
        "registries and evidence-state reports remain in the researcher-facing "
        "collection rather than the main visitor journey.\n",
        encoding="utf-8",
        newline="\n",
    )

    readiness_rows = "\n".join(
        "| {id} | {title} | {collection} | {readiness} | {risk} |".format(
            id=page["candidate_id"],
            title=page["working_title"],
            collection=page["collection"],
            readiness=page["readiness"],
            risk=page["risk_class"],
        )
        for page in readiness["pages"]
    )
    READINESS_MD.write_text(
        "# Phase 5 Knowledge Readiness Audit\n\n"
        f"- Foundational pages planned: {readiness['foundational_page_count']}\n"
        f"- Readiness distribution: `{json.dumps(readiness['readiness_counts'], sort_keys=True)}`\n"
        f"- Collection distribution: `{json.dumps(readiness['collection_counts'], sort_keys=True)}`\n\n"
        "| ID | Working title | Collection | Readiness | Risk |\n"
        "| --- | --- | --- | --- | --- |\n"
        f"{readiness_rows}\n\n"
        "`READY_TO_DRAFT` means reviewed Knowledge can support a new narrative. "
        "It is not publication approval. Every other page remains blocked on the "
        "specific Knowledge development recorded in the machine-readable audit.\n",
        encoding="utf-8",
        newline="\n",
    )

    backlog_sections = []
    for item in backlog["items"]:
        requirements = "\n".join(f"- {value}" for value in item["required_work"])
        backlog_sections.append(
            f"## {item['rank']}. {item['working_title']} ({item['candidate_id']})\n\n"
            f"Readiness: `{item['readiness']}`\n\n"
            f"Risk: `{item['risk_class']}`\n\n"
            f"{requirements}"
        )
    BACKLOG_MD.write_text(
        "# Targeted Knowledge Development Backlog\n\n"
        "This backlog contains only work required to support the planned public "
        "portfolio. It is not permission to ingest unrelated sources or create "
        "speculative Knowledge.\n\n"
        + "\n\n".join(backlog_sections)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    disposition_rows = "\n".join(
        "| {id} | {title} | {disposition} | {targets} |".format(
            id=item["publication_id"],
            title=item["title"],
            disposition=item["disposition"],
            targets=", ".join(item["target_candidate_ids"]),
        )
        for item in dispositions["dispositions"]
    )
    PROTOTYPE_DISPOSITIONS_MD.write_text(
        "# Phase 5 Prototype Dispositions\n\n"
        "The eleven existing articles remain unpublished editorial prototypes. "
        "Their useful reporting and evidence links are retained while the final "
        "portfolio is redesigned.\n\n"
        "| Prototype | Title | Disposition | Planned destination |\n"
        "| --- | --- | --- | --- |\n"
        f"{disposition_rows}\n",
        encoding="utf-8",
        newline="\n",
    )


def write_markdown(summary: dict[str, Any], portfolio: dict[str, Any]) -> None:
    article_rows = "\n".join(
        "| {id} | [{title}](../../../{path}) | {risk} | {words} | {status} |".format(
            id=article["publication_id"],
            title=article["title"],
            path=article["content_path"],
            risk=article["risk_class"],
            words=summary["portfolio"]["word_counts"][article["publication_id"]],
            status=article.get("status", "DRAFT"),
        )
        for article in portfolio["articles"]
    )
    markdown = f"""# Phase 5 Reader-First Editorial Campaign

Status: **{summary['status']}**

The approved redesign defines eight reader gateways and a thirty-page
foundational narrative map. Editorial Wave 1 advances seven reader-first
articles to human review while seven other prototypes remain drafts.

| ID | Prototype | Risk | Words | State |
| --- | --- | ---: | ---: | --- |
{article_rows}

## Portfolio metrics

- Manifest entries: {summary['portfolio']['manifest_entries']}
- Draft entries: {summary['portfolio']['draft_entries']}
- In-review entries: {summary['portfolio']['in_review_entries']}
- Total narrative words: {summary['portfolio']['total_words']}
- Published entries: {summary['portfolio']['published_entries']}
- Risk distribution: {json.dumps(summary['portfolio']['risk_class_counts'], sort_keys=True)}

## Redesigned portfolio

- Reader gateways: {summary['portfolio_redesign']['reader_gateways']}
- Foundational pages planned: {summary['portfolio_redesign']['foundational_pages_planned']}
- Ready to draft: {summary['portfolio_redesign']['ready_to_draft']}
- Knowledge promotion required: {summary['portfolio_redesign']['knowledge_promotion_required']}
- Targeted backlog items: {summary['portfolio_redesign']['targeted_backlog_items']}

The house style adopts HNN-inspired immediacy, active voice and community
awareness while preserving the Archive's stricter evidence boundaries. Articles
must explain Star Atlas first; detailed repository process belongs in evidence
panels and researcher views.

## Community foundation

The operator added an eleventh article on players, guilds, creators and community
memory. The campaign completed a supplemental evidence assessment and found the
reviewed Knowledge sufficient for a bounded overview. Exhaustive biographies,
guild rosters and rivalry case studies remain future Knowledge work.

Intergalactic Herald is not a central source or profile in this portfolio.

## Presentation change

The public Knowledge reader no longer renders workflow metadata, confidence or
taxonomy boxes at the top of a page. Front matter remains available internally
for search and validation. No article was published.

## Boundaries

No Archive evidence, canonical Knowledge or graph fact changed. The manifest
continues to exclude all non-`PUBLISHED` entries from the public build.

## Human gate

Human semantic review is required for all seven Wave 1 articles. Reviewers
should assess narrative accuracy, comprehensiveness, lifecycle distinctions
and proportional treatment of uncertainty. The Library Publisher must not
publish or self-approve any article.
"""
    SUMMARY_MD.write_text(markdown, encoding="utf-8", newline="\n")


def main() -> int:
    portfolio = load_json(PORTFOLIO_PATH)
    plan = load_json(PUBLICATION_PLAN_PATH)
    dispositions = load_json(PROTOTYPE_DISPOSITIONS_PATH)
    manifest = build_manifest(portfolio)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    readiness = build_readiness(plan)
    backlog = build_backlog(plan)
    READINESS_JSON.write_text(
        json.dumps(readiness, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    BACKLOG_JSON.write_text(
        json.dumps(backlog, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    write_planning_reports(plan, readiness, backlog, dispositions)
    summary = build_summary(portfolio, manifest, plan, readiness, backlog)
    SUMMARY_JSON.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    write_markdown(summary, portfolio)
    write_editorial_review(portfolio, manifest)
    print(
        f"BUILT {len(plan['foundational_pages'])} planned pages; "
        f"{summary['portfolio_redesign']['ready_to_draft']} ready to draft; "
        f"{summary['portfolio']['in_review_entries']} articles in review; "
        f"{summary['portfolio']['published_entries']} published"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
