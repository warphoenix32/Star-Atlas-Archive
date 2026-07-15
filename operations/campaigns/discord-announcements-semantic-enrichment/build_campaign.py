#!/usr/bin/env python3
"""Build the repository-native Discord announcement semantic and reconciliation layers."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OPS = Path(__file__).resolve().parent
RAW = REPO / "archive/raw/discord-announcements/star-atlas-discord-announcements.md"
NORMALIZED = REPO / "archive/normalized/discord-announcements/messages.jsonl"
BASELINE = OPS / "input-package/baseline-semantic-records.jsonl"
SOURCE_RECORDS = REPO / "archive/source-records/discord-announcements"
SEMANTIC = REPO / "archive/semantic/discord-announcements"
RECON = REPO / "archive/semantic/reconciliation"
CAMPAIGN_ID = "discord-announcements-semantic-enrichment"

URL_RE = re.compile(r"https?://\S+", re.I)
WORD_RE = re.compile(r"[a-z0-9][a-z0-9_-]+", re.I)
PIP_RE = re.compile(r"\bPIP[-\s#]*(\d{1,3})\b", re.I)
RELEASE_RE = re.compile(r"\b(now live|is live|available now|released?|launch(?:ed|es|ing)?|out now|play now|download now|deployed|mainnet)\b", re.I)
INCIDENT_RE = re.compile(r"\b(compromis|incident|outage|degraded|exploit|hack|breach|unavailable|down\b|maintenance|issue)\w*", re.I)
RESOLUTION_RE = re.compile(r"\b(resolved|restored|fixed|back online|operational again|all clear)\b", re.I)
GOV_RE = re.compile(r"\b(PIP[-\s#]*\d+|proposal|vote|voting|governance|council|treasury)\b", re.I)
GOV_STATE_RE = re.compile(r"\b(passed|failed|approved|rejected|result|opens?|closed?|concluded|executed|withdrawn|canceled|cancelled)\b", re.I)
PARTNER_RE = re.compile(r"\b(partnership|partner(?:ed|ing)? with|collaboration with|joins? forces)\b", re.I)
CORRECTION_RE = re.compile(r"\b(correction|clarif(?:y|ication)|previously stated|incorrect|erroneous|update:)\b", re.I)
SECURITY_RE = re.compile(r"\b(security|scam|phishing|compromis|hack|breach|malicious|never share|wallet drain)\w*", re.I)
PLAN_RE = re.compile(r"\b(planned|roadmap|in development|target(?:ing)?|scheduled|coming (?:soon|in)|will (?:release|launch|deploy|introduce))\b", re.I)
METRIC_RE = re.compile(r"(?:\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|\$\s?\d|\b\d+(?:\.\d+)?\s?(?:atlas|usdc|usd|%|million|billion|hours?|days?|weeks?|months?)\b)", re.I)
LOW_RE = re.compile(r"\b(giveaway|retweet|like and share|gm\b|good morning|meme|who'?s ready|join us|tune in|reminder|set your reminder|town\s*hall|atlas brew|ama\b|spaces?\b|community call|happy (?:friday|monday)|contest)\b", re.I)
MEDIA_NOTICE_RE = re.compile(r"(?:town\s*hall|atlas brew|ama).{0,80}(?:youtube|confirmed|about to start|available now)|newsletter.{0,50}(?:out now|is out)", re.I | re.S)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, values: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n" for value in values), encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text: str) -> set[str]:
    stop = {"this", "that", "with", "from", "your", "have", "will", "star", "atlas", "https", "http", "www", "com", "the", "and", "for", "you", "our", "are"}
    return {w.lower() for w in WORD_RE.findall(URL_RE.sub(" ", text)) if len(w) > 2 and w.lower() not in stop}


def normalized_signature(text: str) -> str:
    text = URL_RE.sub(" URL ", text.lower())
    return " ".join(sorted(words(text)))


def exact_support(message: dict) -> list[dict]:
    return [{"timestamp": message["timestamp_iso"], "text": message["content"]}]


def evaluate(message: dict, baseline: dict) -> tuple[dict, dict]:
    text = message["content"].strip()
    semantic = baseline["semantic"]
    entities = semantic.get("entities", [])
    types = set(semantic.get("statement_types", []))
    substantive = len(words(text)) >= 7
    url_only = bool(text) and not URL_RE.sub("", text).strip()
    routine = bool(LOW_RE.search(text))
    signals: list[str] = []
    category = None
    score = 0
    if entities:
        signals.append("IDENTIFIABLE_ENTITY_OR_PRODUCT"); score += 2
    if "SECURITY_ALERT" in types and SECURITY_RE.search(text):
        category = "SECURITY_ADVISORY"; signals.append("EXPLICIT_SECURITY_ADVISORY"); score += 5
    elif ("RESOLUTION" in types or RESOLUTION_RE.search(text)) and RESOLUTION_RE.search(text):
        category = "INCIDENT_RESOLUTION"; signals.append("EXPLICIT_RESOLUTION_STATE"); score += 5
    elif ("CORRECTION_OR_CLARIFICATION" in types or CORRECTION_RE.search(text)) and CORRECTION_RE.search(text):
        category = "CORRECTION_OR_CLARIFICATION"; signals.append("EXPLICIT_CORRECTION_OR_CLARIFICATION"); score += 5
    elif "PARTNERSHIP_ANNOUNCEMENT" in types and PARTNER_RE.search(text):
        category = "PARTNERSHIP_ANNOUNCEMENT"; signals.append("EXPLICIT_PARTNERSHIP_RELATIONSHIP"); score += 4
    elif "RELEASE" in types and RELEASE_RE.search(text) and not re.search(r"\b(?:once|when|after)\b.{0,60}\breleas|\bwill be released|\breleasing later", text, re.I | re.S):
        category = "PRODUCT_OR_ASSET_RELEASE"; signals.append("EXPLICIT_AVAILABILITY_OR_DEPLOYMENT_LANGUAGE"); score += 4
    elif "GOVERNANCE_UPDATE" in types and GOV_RE.search(text) and GOV_STATE_RE.search(text):
        category = "GOVERNANCE_EVENT"; signals.append("GOVERNANCE_OBJECT_WITH_EVENT_STATE"); score += 4
    elif "INCIDENT_UPDATE" in types and INCIDENT_RE.search(text):
        category = "SERVICE_INCIDENT"; signals.append("IDENTIFIABLE_INCIDENT_STATE"); score += 4
    elif PLAN_RE.search(text) and entities and substantive and (METRIC_RE.search(text) or re.search(r"\b(?:Q[1-4]|20\d{2}|january|february|march|april|may|june|july|august|september|october|november|december)\b", text, re.I)):
        category = "DATED_ROADMAP_COMMITMENT"; signals.append("CONTEXTUAL_ROADMAP_WITH_DATE_OR_METRIC"); score += 3
    if METRIC_RE.search(text):
        signals.append("CONCRETE_METRIC_OR_QUANTITY"); score += 1
    if substantive:
        score += 1

    exclusion = None
    if url_only:
        exclusion = "URL_ONLY_WITHOUT_PRESERVED_CLAIM_TEXT"
    elif (routine and len(words(text)) < 35 or MEDIA_NOTICE_RE.search(text)) and category not in {"SECURITY_ADVISORY", "INCIDENT_RESOLUTION", "CORRECTION_OR_CLARIFICATION", "GOVERNANCE_EVENT"}:
        exclusion = "ROUTINE_EVENT_PROMOTION_OR_COMMUNITY_ENGAGEMENT"
    elif not entities and category not in {"SECURITY_ADVISORY", "INCIDENT_RESOLUTION"}:
        exclusion = "NO_IDENTIFIABLE_INSTITUTIONAL_ENTITY_OR_PRODUCT"
    elif category is None:
        exclusion = "NO_DISCRETE_EVIDENCE_BEARING_INSTITUTIONAL_CLAIM"
    elif not substantive and category not in {"SECURITY_ADVISORY", "INCIDENT_RESOLUTION"}:
        exclusion = "INSUFFICIENT_EVIDENCE_DENSITY"
    eligible = exclusion is None and score >= 5
    if not eligible and exclusion is None:
        exclusion = "INSUFFICIENT_MULTI_SIGNAL_CONFIDENCE"
    confidence = "HIGH" if score >= 8 else "MEDIUM" if score >= 5 else "LOW"
    priority = "HIGH_PRIORITY" if score >= 8 else "MEDIUM_PRIORITY" if score >= 6 else "LOW_PRIORITY" if eligible else "NOT_ELIGIBLE"
    promotion = {
        "source_id": message["source_id"], "sequence": message["sequence"], "eligible": eligible,
        "disposition": priority, "candidate_confidence": confidence, "candidate_reasons": signals if eligible else [],
        "supporting_captions": exact_support(message), "exclusion_reason": None if eligible else exclusion,
        "manual_review_required": eligible, "candidate_category": category,
    }

    timeline_category = category if category in {"SECURITY_ADVISORY", "INCIDENT_RESOLUTION", "CORRECTION_OR_CLARIFICATION", "PARTNERSHIP_ANNOUNCEMENT", "PRODUCT_OR_ASSET_RELEASE", "GOVERNANCE_EVENT", "SERVICE_INCIDENT"} else None
    timeline_eligible = eligible and timeline_category is not None
    timeline_exclusion = None if timeline_eligible else (exclusion or "ROADMAP_OR_STATUS_LANGUAGE_IS_NOT_A_COMPLETED_DATEABLE_EVENT")
    timeline = {
        "source_id": message["source_id"], "sequence": message["sequence"], "eligible": timeline_eligible,
        "event_type": timeline_category if timeline_eligible else None,
        "date_value": message["timestamp_iso"][:10] if timeline_eligible else None,
        "date_precision": "DAY" if timeline_eligible else None,
        "date_basis": "DISCORD_MESSAGE_TIMESTAMP" if timeline_eligible else None,
        "supporting_captions": exact_support(message), "timeline_confidence": confidence if timeline_eligible else "LOW",
        "timeline_reasons": signals if timeline_eligible else [], "exclusion_reason": timeline_exclusion,
    }
    return promotion, timeline


def duplicate_clusters(records: list[dict]) -> tuple[list[dict], dict[str, str]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        signature = normalized_signature(record["content"])
        if signature:
            groups[signature].append(record)
    clusters, membership = [], {}
    for members in sorted((v for v in groups.values() if len(v) > 1), key=lambda v: (v[0]["sequence"], v[0]["source_id"])):
        ordered = sorted(members, key=lambda x: (-len(words(x["content"])), x["sequence"], x["source_id"]))
        cluster_id = f"DISCORD-DUP-{len(clusters)+1:04d}"
        strongest = ordered[0]["source_id"]
        for member in members: membership[member["source_id"]] = cluster_id
        clusters.append({"duplicate_cluster_id": cluster_id, "strongest_candidate_id": strongest, "member_source_ids": [m["source_id"] for m in sorted(members, key=lambda x: x["sequence"])], "duplicate_reason": "NORMALIZED_EXACT_CLAIM_SIGNATURE", "evidence_preserved": True})
    return clusters, membership


def build_event_sequences(records: list[dict], decisions: dict[str, dict]) -> list[dict]:
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for record in records:
        decision = decisions[record["source_id"]]
        category = decision.get("candidate_category")
        if category not in {"SECURITY_ADVISORY", "SERVICE_INCIDENT", "INCIDENT_RESOLUTION", "GOVERNANCE_EVENT", "PRODUCT_OR_ASSET_RELEASE", "CORRECTION_OR_CLARIFICATION"}: continue
        entity = next(iter(record["entities"]), "UNRESOLVED_ENTITY")
        groups[(category, entity)].append(record)
    sequences = []
    for (category, entity), members in sorted(groups.items()):
        members.sort(key=lambda x: (x["timestamp_iso"], x["source_id"]))
        if len(members) < 2: continue
        sequences.append({"event_sequence_id": f"DISCORD-EVENT-{len(sequences)+1:04d}", "event_type": category, "entity": entity, "first_timestamp": members[0]["timestamp_iso"], "last_timestamp": members[-1]["timestamp_iso"], "source_ids": [x["source_id"] for x in members], "relationship": "UPDATES", "canonical_graph_status": "REVIEW_ONLY"})
    return sequences


def cross_reconcile(records: list[dict], promotions: list[dict]) -> dict[str, list[dict]]:
    social = read_jsonl(REPO / "archive/semantic/social-media/staratlas-posts-semantic.jsonl")
    pips = json.loads((REPO / "archive/semantic/governance/pip-registry-semantic.json").read_text(encoding="utf-8"))["proposals"]
    council = read_jsonl(REPO / "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl")
    social_by_url = defaultdict(list)
    for item in social:
        for url in URL_RE.findall(item.get("content", "")): social_by_url[url.rstrip(".,)")].append(item)
    social_links = []
    for record in records:
        linked = {item["source_id"] for url in record["urls"] for item in social_by_url.get(url.rstrip(".,)"), [])}
        if linked:
            social_links.append({"discord_source_id": record["source_id"], "social_source_ids": sorted(linked), "relationship": "DUPLICATES", "basis": "EXACT_SHARED_URL", "canonical_graph_status": "REVIEW_ONLY"})
    pip_by_number = {x["pip_number"]: x for x in pips}
    pip_links = []
    for record in records:
        for number in sorted({int(x) for x in PIP_RE.findall(record["content"]) if int(x) in pip_by_number}):
            pip_links.append({"discord_source_id": record["source_id"], "pip_source_id": pip_by_number[number]["source_id"], "pip_number": number, "relationship": "ANNOUNCES_VOTE" if re.search(r"\bvote|voting\b", record["content"], re.I) else "REQUIRES_RECONCILIATION", "basis": "EXPLICIT_PIP_IDENTIFIER", "canonical_graph_status": "REVIEW_ONLY"})
    product_links = []
    for record in records:
        if record["lifecycle_states"] != ["NOT_APPLICABLE"]:
            for entity in record["entities"]:
                product_links.append({"discord_source_id": record["source_id"], "entity": entity, "lifecycle_states": record["lifecycle_states"], "relationship": "UPDATES", "canonical_graph_status": "REVIEW_ONLY"})
    council_links = [{"council_tracker_source_id": item["source_id"], "pip_source_id": pip_by_number[item["pip_number"]]["source_id"] if item["pip_number"] in pip_by_number else None, "pip_number": item["pip_number"], "relationship": "COUNCIL_REPORTS_MILESTONE", "reported_implementation_state": item["implementation_state"], "attribution_required": True, "canonical_graph_status": "REVIEW_ONLY"} for item in council]
    promo_links = []
    linked_discord = {x["discord_source_id"] for x in social_links + pip_links}
    for candidate in promotions:
        promo_links.append({"discord_source_id": candidate["source_id"], "relationship": "CORROBORATES" if candidate["source_id"] in linked_discord else "REQUIRES_RECONCILIATION", "promotion_disposition": candidate["disposition"], "promotion_targets": ["knowledge/timeline/", "knowledge/products/"], "manual_review_required": True, "canonical_promotion_status": "PROPOSED_ONLY"})
    return {
        "discord-social-governance-event-links.json": social_links,
        "discord-pip-links.json": pip_links,
        "discord-product-lifecycle-links.json": product_links,
        "council-tracker-pip-links.json": council_links,
        "cross-source-contradictions.json": [],
        "cross-source-promotion-candidates.json": promo_links,
    }


def main() -> None:
    messages = read_jsonl(NORMALIZED)
    baseline = {item["source_id"]: item for item in read_jsonl(BASELINE)}
    if len(messages) != 1071 or set(baseline) != {m["source_id"] for m in messages}: raise SystemExit("Discord input reconciliation failed")
    semantic_records, promotion_decisions, timeline_decisions = [], [], []
    for message in messages:
        base = baseline[message["source_id"]]
        promotion, timeline = evaluate(message, base)
        sem = base["semantic"]
        gaps = ["AUTHOR_ATTRIBUTION_INFERRED_FROM_EXPORT_GROUPING", "SOURCE_EXPORT_COLLECTION_COMPLETE_FALSE_WARNING_PRESERVED"]
        if message["attachments"]: gaps.append("ATTACHMENT_BINARY_NOT_IN_PACKAGE")
        record = {**message, "timestamp": message["timestamp_iso"], "author_attribution_status": "INFERRED_FROM_EXPORT_GROUPING_NOT_INDEPENDENTLY_VERIFIED", "content_checksum": message["content_sha256"], "topics": sem["topics"], "entities": sem["entities"], "statement_types": sem["statement_types"], "lifecycle_states": sem["lifecycle_states"], "evidence_classes": sem["evidence_classes"], "confidence": promotion["candidate_confidence"], "promotion_decision": promotion, "timeline_decision": timeline, "research_gaps": gaps}
        semantic_records.append(record); promotion_decisions.append(promotion); timeline_decisions.append(timeline)
        write_json(SOURCE_RECORDS / f"{message['source_id']}.json", {"source_id": message["source_id"], "source_class": "TIER_1_OFFICIAL_DISCORD_ANNOUNCEMENT_EXPORT", "sequence": message["sequence"], "timestamp": message["timestamp_iso"], "author": message["author"], "author_attribution_status": record["author_attribution_status"], "content_checksum": message["content_sha256"], "raw_collection": "archive/raw/discord-announcements/star-atlas-discord-announcements.md", "normalized_collection": "archive/normalized/discord-announcements/messages.jsonl", "provenance_warning": "Collection complete: no; authorship grouping is not independently verified."})
    clusters, membership = duplicate_clusters(semantic_records)
    for decision in promotion_decisions:
        if decision["eligible"] and decision["source_id"] in membership:
            cluster = next(x for x in clusters if x["duplicate_cluster_id"] == membership[decision["source_id"]])
            decision["duplicate_cluster_id"] = cluster["duplicate_cluster_id"]
            decision["strongest_candidate_id"] = cluster["strongest_candidate_id"]
            if decision["source_id"] != cluster["strongest_candidate_id"]:
                decision.update({"eligible": False, "disposition": "NOT_ELIGIBLE", "exclusion_reason": "WEAKER_NEAR_DUPLICATE_CANDIDATE", "candidate_reasons": []})
    promotion_by_id = {x["source_id"]: x for x in promotion_decisions}
    for record in semantic_records: record["promotion_decision"] = promotion_by_id[record["source_id"]]
    promotions = [x for x in promotion_decisions if x["eligible"]]
    timelines = [x for x in timeline_decisions if x["eligible"] and promotion_by_id[x["source_id"]]["eligible"]]
    timeline_ids = {x["source_id"] for x in timelines}
    for decision in timeline_decisions:
        if decision["eligible"] and decision["source_id"] not in timeline_ids:
            decision.update({"eligible": False, "event_type": None, "date_value": None, "date_precision": None, "date_basis": None, "timeline_reasons": [], "exclusion_reason": "WEAKER_NEAR_DUPLICATE_CANDIDATE"})
    write_jsonl(SEMANTIC / "announcement-semantic-records.jsonl", semantic_records)
    write_jsonl(SEMANTIC / "promotion-candidate-decisions.jsonl", promotion_decisions)
    write_jsonl(SEMANTIC / "timeline-candidate-decisions.jsonl", timeline_decisions)
    write_json(SEMANTIC / "promotion-candidates.json", {"campaign_id": CAMPAIGN_ID, "candidate_count": len(promotions), "candidates": promotions})
    write_json(SEMANTIC / "timeline-candidates.json", {"campaign_id": CAMPAIGN_ID, "candidate_count": len(timelines), "candidates": timelines})
    write_json(SEMANTIC / "duplicate-clusters.json", {"campaign_id": CAMPAIGN_ID, "cluster_count": len(clusters), "clusters": clusters})
    sequences = build_event_sequences(semantic_records, promotion_by_id)
    write_json(SEMANTIC / "event-sequences.json", {"campaign_id": CAMPAIGN_ID, "sequence_count": len(sequences), "sequences": sequences})
    links = [{"source_id": r["source_id"], "entities": r["entities"]} for r in semantic_records if r["entities"]]
    write_json(SEMANTIC / "entity-links.json", {"campaign_id": CAMPAIGN_ID, "link_record_count": len(links), "records": links})
    security = [r for r in semantic_records if "SECURITY_ALERT" in r["statement_types"]]
    incidents = [r for r in semantic_records if set(r["statement_types"]) & {"INCIDENT_UPDATE", "RESOLUTION"}]
    write_json(SEMANTIC / "security-alerts.json", {"campaign_id": CAMPAIGN_ID, "record_count": len(security), "records": [{"source_id": r["source_id"], "timestamp": r["timestamp"], "content": r["content"]} for r in security]})
    write_json(SEMANTIC / "incidents-and-resolutions.json", {"campaign_id": CAMPAIGN_ID, "record_count": len(incidents), "records": [{"source_id": r["source_id"], "timestamp": r["timestamp"], "statement_types": r["statement_types"], "content": r["content"]} for r in incidents]})
    topic_index = {topic: [r["source_id"] for r in semantic_records if topic in r["topics"]] for topic in sorted({t for r in semantic_records for t in r["topics"]})}
    write_json(SEMANTIC / "topic-index.json", {"campaign_id": CAMPAIGN_ID, "topic_counts": {k: len(v) for k, v in topic_index.items()}, "topics": topic_index})
    gaps = [{"source_id": r["source_id"], "gap_types": r["research_gaps"]} for r in semantic_records]
    write_json(SEMANTIC / "research-gaps.json", {"campaign_id": CAMPAIGN_ID, "record_count": len(gaps), "records": gaps})
    for name, values in cross_reconcile(semantic_records, promotions).items():
        write_json(RECON / name, {"campaign_id": CAMPAIGN_ID, "record_count": len(values), "records": values})
    summary = {"campaign_id": CAMPAIGN_ID, "status": "GENERATED", "source_messages": len(messages), "semantic_records": len(semantic_records), "promotion_candidates": len(promotions), "promotion_exclusions": len(messages)-len(promotions), "timeline_candidates": len(timelines), "timeline_exclusions": len(messages)-len(timelines), "duplicate_clusters": len(clusters), "event_sequences": len(sequences), "security_alerts": len(security), "incidents_and_resolutions": len(incidents), "earliest_message": min(r["timestamp"] for r in semantic_records), "latest_message": max(r["timestamp"] for r in semantic_records), "collection_complete_warning": "no", "author_attribution": "inferred_not_independently_verified"}
    write_json(OPS / "campaign-summary.json", summary)
    (OPS / "campaign-summary.md").write_text("# Discord Announcements Semantic Enrichment\n\n" + "\n".join(f"- {key.replace('_',' ').title()}: **{value}**" for key, value in summary.items() if key not in {"campaign_id"}) + "\n\nThe supplied `Collection complete: no` warning is preserved. The user designates this as the complete available channel export, while grouped author labels remain unverified attribution. Candidate counts are precision-oriented review inputs, not canonical promotion.\n", encoding="utf-8")
    (OPS / "README.md").write_text("# Discord Announcements Semantic Enrichment\n\nDeterministic precision rules require multiple signals: an identifiable entity or system, discrete event-state language, sufficient evidence density, and exact supporting text. Routine reminders, Town Hall/AMA notices, giveaways, generic engagement, URL-only messages, weak roadmap wording, and weaker duplicate variants are excluded. Announcement, release, roadmap, incident, resolution, correction, security, event, vote, and implementation states remain distinct. Confidence measures extraction quality only.\n\nRun `python operations/campaigns/discord-announcements-semantic-enrichment/build_campaign.py` then `python operations/campaigns/discord-announcements-semantic-enrichment/validate_campaign.py`.\n", encoding="utf-8")
    inputs = sorted([RAW, NORMALIZED, BASELINE, *[p for p in (OPS / "input-package").glob("*") if p.is_file()]])
    outputs = sorted([p for root in (SOURCE_RECORDS, SEMANTIC, RECON, OPS) for p in root.rglob("*") if p.is_file() and p.name not in {"manifest.json", "validation-report.json", "validation-report.md"} and (OPS / "input-package") not in p.parents and p.suffix != ".pyc"])
    write_json(OPS / "manifest.json", {"campaign_id": CAMPAIGN_ID, "status": "GENERATED", "preserved_inputs": [{"path": p.relative_to(REPO).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p)} for p in inputs], "generated_outputs": [{"path": p.relative_to(REPO).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p)} for p in outputs]})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__": main()
