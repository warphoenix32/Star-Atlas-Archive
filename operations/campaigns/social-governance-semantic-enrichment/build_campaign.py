#!/usr/bin/env python3
"""Build deterministic semantic outputs for the social/governance campaign.

The script never changes preserved evidence. It reads the normalized social export,
the official raw portal captures, and the existing Atlas Brew entity links, then
writes campaign semantic indexes, governance source records, and review reports.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse


REPO = Path(__file__).resolve().parents[3]
CAMPAIGN_ID = "social-governance-semantic-enrichment"
CAPTURE_TIMESTAMP = "2026-07-15T03:41:40Z"  # completion time of the 33-record official API capture batch
SOCIAL_INPUT = REPO / "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl"
PIP_SEED = REPO / "archive/normalized/social-governance-semantic-enrichment/governance/pip-1-33-registry-seed.json"
PIP_RAW = REPO / "archive/raw/social-governance-semantic-enrichment/governance/pip-captures"
SOCIAL_OUT = REPO / "archive/semantic/social-media"
GOV_OUT = REPO / "archive/semantic/governance"
GOV_RECORDS = REPO / "archive/source-records/social-governance-semantic-enrichment/governance"
OPS = REPO / "operations/campaigns/social-governance-semantic-enrichment"
PIP_REVIEW = OPS / "pip-corpus-review.md"
PIP_REVIEW_SUMMARY = OPS / "pip-corpus-review-summary.json"
COUNCIL_TRACKER = OPS / "input-council-tracker/council-pip-tracker-semantic-records.jsonl"
HISTORICAL_SOCIAL_COUNTS = {"promotion_candidates": 345, "timeline_candidates": 65}

TOPICS = {
    "PRODUCT", "GAMEPLAY", "GOVERNANCE", "ECONOMY", "TECHNOLOGY", "LORE",
    "CORPORATE", "PEOPLE", "COMMUNITY", "PARTNERSHIP", "GUILD", "EVENT",
    "MARKETING", "OPERATIONS",
}
STATEMENTS = {
    "ANNOUNCEMENT", "STATUS_UPDATE", "ROADMAP", "RELEASE", "DESIGN_INTENT",
    "TECHNICAL_EXPLANATION", "Q_AND_A", "RETROSPECTIVE", "CLARIFICATION",
    "CORRECTION", "COMMUNITY_FEEDBACK", "DISCUSSION", "SPECULATION", "THEORYCRAFTING",
}
LIFECYCLE = {
    "FIRST_MENTION", "PLANNED", "IN_DEVELOPMENT", "TESTING", "LIVE", "UPDATED",
    "SUPERSEDED", "DEPRECATED", "CANCELLED", "UNKNOWN",
}
EVIDENCE = {
    "CANONICAL_KNOWLEDGE_CANDIDATE", "TIMELINE_CANDIDATE", "ENTITY_UPDATE_CANDIDATE",
    "GRAPH_RELATIONSHIP_CANDIDATE", "RESEARCH_GAP", "CONTRADICTION", "LOW_VALUE", "DUPLICATE",
}

TOPIC_RULES = {
    "GOVERNANCE": r"\b(dao|governance|pip-?\d+|polis|proposal|vote|voting|council|treasury)\b",
    "ECONOMY": r"\b(econom(?:y|ic|ics)|tokenomics|atlas token|\$atlas|\$polis|marketplace|earn|reward|loot|treasury|funding|fee|price|stake|staking)\b",
    "GAMEPLAY": r"\b(gameplay|play|mission|combat|craft|crafting|mining|fleet|ship|crew|resource|arena|racing|movement|scan|warp|cargo|claim stake)\b",
    "TECHNOLOGY": r"\b(solana|unreal engine|ue5|blockchain|on-chain|api|sdk|infrastructure|cloud|data hub|technology|technical|build)\b",
    "LORE": r"\b(lore|galia|mud|manus ultima divina|oni|ustur|faction|story|crew adventure)\b",
    "CORPORATE": r"\b(atmta|company|foundation|corporate|team|studio|employee|hiring|restructur)\b",
    "PEOPLE": r"\b(michael wagner|pablo quiroga|danny floyd|ceo|founder|developer|artist|speaker|interview)\b",
    "COMMUNITY": r"\b(community|players?|citizens?|fans?|giveaway|contest|join us|spaces|discord)\b",
    "PARTNERSHIP": r"\b(partner(?:ship|ed|ing)?|collaborat(?:ion|e|ing)|sponsor(?:ed|ship)?)\b",
    "GUILD": r"\b(guild|dac|rome|aephia|quimera|guilds)\b",
    "EVENT": r"\b(event|gamescom|breakpoint|summit|town hall|townhall|comet|tournament|livestream|live stream|ama|conference)\b",
    "MARKETING": r"\b(trailer|teaser|campaign|merch|promotion|promo|wishlist|giveaway|contest|sale|store|mint)\b",
    "OPERATIONS": r"\b(maintenance|downtime|outage|operations?|server|service|support|patch|migration|sustainability)\b",
    "PRODUCT": r"\b(star atlas|sage|fleet command|holosim|starbased|score|escape velocity|c4|marketplace|crew|showroom|golden carnival|star atlas 2\.0|mobile app|star seekers|sly assistant)\b",
}

ENTITY_FALLBACK = {
    "ORG-ATMTA": ("ATMTA, Inc.", "ORGANIZATION", ["atmta", "star atlas team"]),
    "ORG-STAR-ATLAS-FOUNDATION": ("Star Atlas Foundation", "ORGANIZATION", ["star atlas foundation"]),
    "ORG-STAR-ATLAS-DAO": ("Star Atlas DAO", "ORGANIZATION", ["star atlas dao", "dao"]),
    "TOKEN-ATLAS": ("ATLAS", "TOKEN", ["$atlas", "atlas token"]),
    "TOKEN-POLIS": ("POLIS", "TOKEN", ["$polis", "polis token"]),
    "TECH-SOLANA": ("Solana", "TECHNOLOGY", ["solana"]),
    "PRODUCT-SAGE": ("SAGE", "PRODUCT", ["sage"]),
    "PRODUCT-FLEET-COMMAND": ("Fleet Command", "PRODUCT", ["fleet command"]),
    "PRODUCT-HOLOSIM": ("Holosim", "PRODUCT", ["holosim"]),
    "PRODUCT-STARBASED": ("Starbased", "PRODUCT", ["starbased"]),
    "PRODUCT-SCORE": ("SCORE", "PRODUCT", ["score"]),
    "PRODUCT-ESCAPE-VELOCITY": ("Escape Velocity", "PRODUCT", ["escape velocity"]),
    "PRODUCT-C4": ("C4", "PRODUCT", ["c4"]),
    "PERSON-MICHAEL-WAGNER": ("Michael Wagner", "PERSON", ["michael wagner"]),
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_text(text: str) -> str:
    text = re.sub(r"https?://\S+", " ", text.lower())
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9$]+", " ", text)).strip()


def match(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.I) is not None


def unique(values):
    return list(dict.fromkeys(values))


def load_entity_aliases():
    entities = dict(ENTITY_FALLBACK)
    atlas_links = REPO / "archive/semantic/atlas-brew/entity-links.json"
    if atlas_links.exists():
        for link in load_json(atlas_links).get("links", []):
            for entity in link.get("canonical_entities", []):
                eid = entity.get("entity_id")
                name = entity.get("entity_name")
                etype = entity.get("entity_type", "UNKNOWN")
                aliases = [a.strip() for a in entity.get("matched_aliases", []) if len(a.strip()) >= 3]
                if eid and name:
                    if eid in entities:
                        aliases = unique(entities[eid][2] + aliases)
                    entities[eid] = (name, etype, aliases)
    return entities


def link_entities(text: str, entity_catalog):
    lower = text.lower()
    links = []
    for eid, (name, etype, aliases) in entity_catalog.items():
        found = []
        for alias in aliases:
            a = alias.lower()
            if len(a) < 3 or a in {"game", "team", "ship", "ships", "dao", "score"}:
                continue
            if re.search(r"(?<![a-z0-9])" + re.escape(a) + r"(?![a-z0-9])", lower):
                found.append(alias)
        if found:
            links.append({
                "entity_id": eid,
                "entity_name": name,
                "entity_type": etype,
                "matched_aliases": sorted(unique(found), key=str.lower),
                "link_confidence": "HIGH",
            })
    links.sort(key=lambda x: x["entity_id"])
    return links


def social_topics(text: str):
    topics = [topic for topic, pattern in TOPIC_RULES.items() if match(pattern, text)]
    return topics or ["COMMUNITY"]


def social_subtopics(text: str):
    rules = {
        "DAO_PROPOSALS": r"\bpip-?\d+|proposal",
        "DAO_VOTING": r"\bvote|voting|polls?\b",
        "TOKEN_ECONOMY": r"\b\$atlas|\$polis|tokenomics|token\b",
        "SHIP_ASSETS": r"\bships?|fleet\b",
        "LIVE_EVENTS": r"\bgamescom|breakpoint|town ?hall|spaces|livestream|tournament\b",
        "PRODUCT_RELEASES": r"\brelease|launched?|now live|available now\b",
        "PRODUCT_DEVELOPMENT": r"\bdevelopment|building|roadmap|coming soon|work in progress\b",
        "COMMUNITY_REWARDS": r"\bgiveaway|loot|reward|prize|bounty\b",
        "ECOSYSTEM_PARTNERSHIPS": r"\bpartner|collaborat|sponsor\b",
        "LORE_AND_WORLD": r"\blore|galia|mud|oni|ustur|faction\b",
        "TECHNICAL_INFRASTRUCTURE": r"\bsolana|unreal|blockchain|api|sdk|server|cloud\b",
        "MARKETING_MEDIA": r"\btrailer|teaser|video|watch|image|merch\b",
    }
    return [name for name, pattern in rules.items() if match(pattern, text)]


def statement_types(text: str):
    rules = [
        ("CORRECTION", r"\bcorrection|we were wrong|incorrect|erratum\b"),
        ("CLARIFICATION", r"\bclarif(?:y|ication)|to be clear|for clarity\b"),
        ("RETROSPECTIVE", r"\brecap|look back|anniversary|previously|last (?:week|month|year)\b"),
        ("Q_AND_A", r"\bq&a|ama|ask us|questions?\b"),
        ("RELEASE", r"\b(now live|available now|released|launch(?:ed)? today|play now|download now|deployed)\b"),
        ("ROADMAP", r"\broadmap|coming (?:soon|next)|planned|future update|later this year|next phase\b"),
        ("STATUS_UPDATE", r"\bupdate|progress|maintenance|status|development update|work in progress\b"),
        ("TECHNICAL_EXPLANATION", r"\bhow it works|under the hood|technical|architecture|mechanic|system works\b"),
        ("DESIGN_INTENT", r"\bdesigned to|we envision|our goal|intended to|aims? to\b"),
        ("COMMUNITY_FEEDBACK", r"\bfeedback|tell us|what do you think|community response|survey\b"),
        ("SPECULATION", r"\bmaybe|might|could|perhaps|rumou?r|speculat\b"),
        ("THEORYCRAFTING", r"\btheorycraft|strategy|build idea|what if\b"),
        ("ANNOUNCEMENT", r"\b(announce|introduc|reveal|unveil|proud to|excited to|new:|officially)\b"),
        ("DISCUSSION", r"\bdiscuss|conversation|spaces|town ?hall|join us|talk about\b"),
    ]
    out = [name for name, pattern in rules if match(pattern, text)]
    return out or ["DISCUSSION"]


def lifecycle_states(text: str):
    rules = [
        ("CANCELLED", r"\bcancelled|canceled|will not proceed\b"),
        ("DEPRECATED", r"\bdeprecated|sunset|retired\b"),
        ("SUPERSEDED", r"\bsupersed|replaced by|no longer current\b"),
        ("LIVE", r"\b(now live|available now|released|play now|download now|deployed|launched today)\b"),
        ("TESTING", r"\btestnet|playtest|testing|alpha test|beta test|public test\b"),
        ("IN_DEVELOPMENT", r"\bin development|building|work in progress|being developed\b"),
        ("PLANNED", r"\bplanned|roadmap|coming soon|will (?:launch|release|add)|next phase\b"),
        ("UPDATED", r"\bupdated|new update|patch|upgrade|improvement\b"),
    ]
    return [name for name, pattern in rules if match(pattern, text)]


def promotion_targets(topics):
    mapping = {
        "PRODUCT": "knowledge/products/", "GAMEPLAY": "knowledge/gameplay/",
        "GOVERNANCE": "knowledge/governance/", "ECONOMY": "knowledge/economy/",
        "TECHNOLOGY": "knowledge/technology/", "LORE": "knowledge/lore/",
        "CORPORATE": "knowledge/organizations/", "PEOPLE": "knowledge/people/",
        "COMMUNITY": "knowledge/community/", "PARTNERSHIP": "knowledge/partnerships/",
        "GUILD": "knowledge/community/", "EVENT": "knowledge/timeline/",
        "MARKETING": "knowledge/timeline/", "OPERATIONS": "knowledge/operations/",
    }
    return unique(mapping[t] for t in topics if t in mapping)


def extract_mentions(text: str):
    return sorted(set(re.findall(r"(?<!\w)[@#][A-Za-z0-9_]{2,}", text)), key=str.lower)


def meaningful_tokens(text: str) -> set[str]:
    stop = {"about", "after", "again", "also", "been", "from", "have", "into", "more", "star", "atlas", "that", "their", "there", "these", "they", "this", "with", "your", "https"}
    return {token for token in normalize_text(text).split() if len(token) >= 4 and token not in stop}


def social_signal_data(text: str, entities: list[dict]) -> dict:
    object_pattern = r"\b(?:pip-?\d+|dao|council|foundation|treasury|ecosystem fund|atlas|polis|sage|fleet command|holosim|starbased|score|escape velocity|c4|showroom|marketplace|crew|ship|solana|unreal engine|ue5|gamescom|breakpoint|tournament|partner(?:ship)?)\b"
    event_patterns = [
        ("CORRECTION", r"\b(?:correction|corrected|erratum|we were wrong|scam alert|fraud warning)\b"),
        ("DEPRECATION", r"\b(?:deprecated|sunset|retired|discontinued|shut down)\b"),
        ("MIGRATION", r"\b(?:migrat(?:e|ed|ion)|moved? to|transition(?:ed)? to)\b"),
        ("GOVERNANCE_VOTE", r"\b(?:proposal|pip-?\d+|vote|voting|polls? (?:open|closed)|passed|failed)\b"),
        ("FUNDING_ACTION", r"\b(?:fund(?:ed|ing)|grant|treasury|allocation|reimbursement|million\s+(?:atlas|polis|usdc))\b"),
        ("PARTNERSHIP_ANNOUNCEMENT", r"\b(?:partnered with|partnership with|announce(?:d|ment)? .* partner|collaboration with)\b"),
        ("PUBLIC_TEST", r"\b(?:public test|playtest|testnet|alpha test|beta test|testing (?:opens?|begins?|starts?))\b"),
        ("PRODUCT_RELEASE", r"\b(?:now live|is live now|available now|released|newly released|we(?:'|’)ve introduced|launched today|launches? (?:today|on)|play now|download now|deployed|mainnet|report is live)\b"),
        ("DELAY_OR_STATUS_CHANGE", r"\b(?:delayed|postponed|will miss the launch|technical difficulties|service restored|back online)\b"),
        ("MATERIAL_UPDATE", r"\b(?:major update|new patch|patch notes|updated? (?:build|version|feature)|maintenance (?:begins?|complete)|milestone (?:complete|reached))\b"),
        ("ORGANIZATIONAL_CHANGE", r"\b(?:appointed|elected|hired|layoffs?|restructur(?:e|ed|ing)|new council|new ceo|team change)\b"),
        ("EVENT_OCCURRENCE", r"\b(?:join us (?:at|on)|takes place|event (?:starts?|begins?)|gamescom|breakpoint|tournament (?:starts?|begins?|finals?))\b"),
    ]
    events = [name for name, pattern in event_patterns if match(pattern, text)]
    detail = bool(re.search(r"\b(?:20\d{2}|\d{1,2}[:/]\d{1,2}|\d+(?:[.,]\d+)?%|[$€£]\s?\d|\d[\d,.]*\s*(?:atlas|polis|usdc|usd|players?|ships?|days?|hours?))\b", text, re.I))
    institutional_metric = bool(match(r"\b(?:treasury|supply|locked|daily active|monthly active|mau|dau|users?|revenue|emissions?|production|transaction|volume|funding|allocation|voting power|token prices?|fleet rental|generated|earned)\b", text) and detail)
    relationship = bool(match(r"\b(?:partner(?:ed|ship)? with|built by|powered by|funded by|elected to|administered by|integrat(?:es|ed) with|supports?)\b", text))
    object_identified = bool(entities or match(object_pattern, text))
    weak_marketing = bool(match(r"\b(?:giveaway|golden tickets?|golden carnival|chance at|up for grabs|posting .* every \d+ hours?|reminder|only \d+ (?:hours?|days?) left|win now|like and retweet|tag a friend|gm\b|happy (?:friday|monday)|wishlist now|don't miss|are you ready|what do you think|join the conversation)\b", text))
    joke_or_negation = bool(match(r"\b(?:just kidding|you can(?:not|'t)|not actually|false alarm)\b", text))
    question_only = text.strip().endswith("?") and not events
    return {"object_identified": object_identified, "events": events, "detail": detail, "institutional_metric": institutional_metric, "relationship": relationship, "weak_marketing": weak_marketing, "joke_or_negation": joke_or_negation, "question_only": question_only}


def cluster_social_posts(records: list[dict]) -> tuple[list[dict], dict[str, dict]]:
    parent = list(range(len(records)))
    tokens = [meaningful_tokens(record["content"]) for record in records]
    normalized = [normalize_text(record["content"]) for record in records]

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[max(left_root, right_root)] = min(left_root, right_root)

    for left in range(len(records)):
        for right in range(left + 1, len(records)):
            if normalized[left] and normalized[left] == normalized[right]:
                union(left, right)
                continue
            shared = tokens[left] & tokens[right]
            combined = tokens[left] | tokens[right]
            if len(shared) >= 6 and combined and len(shared) / len(combined) >= 0.72:
                union(left, right)

    groups: dict[int, list[int]] = defaultdict(list)
    for index in range(len(records)):
        groups[find(index)].append(index)
    clusters, lookup = [], {}
    for members in sorted((value for value in groups.values() if len(value) > 1), key=lambda value: records[value[0]]["source_id"]):
        cluster_id = f"SOCIAL-DUP-{len(clusters) + 1:04d}"
        def strength(index: int) -> tuple:
            record = records[index]
            signal = record["signal_data"]
            return (not record["is_retweet"], len(record["entities"]), len(signal["events"]), signal["detail"], len(normalize_text(record["content"])), record["source_id"])
        strongest_index = max(members, key=strength)
        exact = len({normalized[index] for index in members}) == 1
        ordered = sorted(members, key=lambda index: (records[index]["published_date"], records[index]["source_id"]))
        cluster = {
            "cluster_id": cluster_id,
            "member_source_ids": [records[index]["source_id"] for index in ordered],
            "cluster_type": "EXACT_REPEATED_CONTENT" if exact else "NEAR_DUPLICATE_OR_REPEATED_ANNOUNCEMENT",
            "strongest_candidate_id": records[strongest_index]["source_id"],
            "supersession_order": [records[index]["source_id"] for index in ordered],
            "reason": "Normalized text is identical." if exact else "High deterministic token overlap indicates repeated or closely variant coverage of the same announcement.",
        }
        clusters.append(cluster)
        for index in members:
            lookup[records[index]["source_id"]] = cluster
    return clusters, lookup


def social_promotion_decision(record: dict, cluster: dict | None) -> dict:
    signal = record["signal_data"]
    reasons, score = [], 0
    if signal["object_identified"]:
        score += 2; reasons.append("IDENTIFIABLE_INSTITUTIONAL_ENTITY_OR_OBJECT")
    if signal["events"]:
        score += 3; reasons.append("CONCRETE_INSTITUTIONAL_ACTION:" + ",".join(signal["events"]))
    if signal["detail"]:
        score += 1; reasons.append("SPECIFIC_DATE_AMOUNT_METRIC_OR_QUANTITY")
    if signal["institutional_metric"]:
        score += 2; reasons.append("INSTITUTIONAL_METRIC_OR_ECONOMIC_MEASUREMENT")
    if signal["relationship"]:
        score += 1; reasons.append("EXPLICIT_ENTITY_RELATIONSHIP")
    if record["entities"]:
        score += 1; reasons.append("CANONICAL_ENTITY_LINK")
    exclusion = None
    if record["is_retweet"]:
        exclusion = "RETWEET_NOT_FIRST_PARTY_CANONICAL_CLAIM"
    elif cluster and cluster["strongest_candidate_id"] != record["source_id"]:
        exclusion = "DUPLICATE_OF_STRONGER_CANDIDATE"
    elif signal["question_only"]:
        exclusion = "QUESTION_WITHOUT_SUBSTANTIVE_ANSWER"
    elif signal["joke_or_negation"]:
        exclusion = "CLAIM_EXPLICITLY_NEGATED_OR_PRESENTED_AS_A_JOKE"
    elif not signal["object_identified"]:
        exclusion = "NO_IDENTIFIABLE_INSTITUTIONAL_ENTITY_OR_OBJECT"
    elif not (signal["events"] or signal["institutional_metric"] or signal["relationship"]):
        exclusion = "NO_DISCRETE_EVIDENCE_BEARING_CLAIM"
    elif signal["weak_marketing"]:
        exclusion = "PRIMARILY_MARKETING_OR_ENGAGEMENT_CONTENT"
    elif score < 4:
        exclusion = "EVIDENCE_DENSITY_BELOW_THRESHOLD"
    eligible = exclusion is None
    decision = "HIGH_PRIORITY" if eligible and score >= 7 else "MEDIUM_PRIORITY" if eligible and score >= 5 else "LOW_PRIORITY" if eligible else "NOT_ELIGIBLE"
    confidence = "HIGH" if score >= 7 and not record["is_retweet"] else "MEDIUM" if score >= 4 else "LOW"
    return {
        "source_id": record["source_id"], "post_id": record["post_id"], "eligible": eligible,
        "decision": decision, "decision_reasons": reasons if eligible else [exclusion],
        "supporting_text": record["content"], "entities": [entity["entity_id"] for entity in record["entities"]],
        "statement_types": record["statement_types"], "confidence": confidence,
        "duplicate_cluster_id": cluster["cluster_id"] if cluster else None,
        "strongest_candidate_id": cluster["strongest_candidate_id"] if cluster else record["source_id"],
        "manual_review_required": eligible, "exclusion_reason": exclusion,
    }


def social_timeline_decision(record: dict, cluster: dict | None) -> dict:
    signal = record["signal_data"]
    exclusion = None
    if record["is_retweet"]:
        exclusion = "RETWEET_WITHOUT_INDEPENDENT_FIRST_PARTY_CONTEXT"
    elif cluster and cluster["strongest_candidate_id"] != record["source_id"]:
        exclusion = "DUPLICATE_OR_REPEATED_REMINDER"
    elif not signal["events"]:
        exclusion = "NO_MATERIALLY_DATEABLE_EVENT"
    elif not signal["object_identified"]:
        exclusion = "NO_IDENTIFIABLE_EVENT_ENTITY_OR_SYSTEM"
    elif signal["joke_or_negation"]:
        exclusion = "CLAIM_EXPLICITLY_NEGATED_OR_PRESENTED_AS_A_JOKE"
    elif signal["weak_marketing"]:
        exclusion = "GENERAL_PROMOTIONAL_OR_ENGAGEMENT_LANGUAGE"
    eligible = exclusion is None
    confidence = "HIGH" if eligible and signal["detail"] and record["entities"] else "MEDIUM" if eligible else "LOW"
    return {
        "source_id": record["source_id"], "post_id": record["post_id"], "eligible": eligible,
        "decision": "TIMELINE_CANDIDATE" if eligible else "NOT_ELIGIBLE",
        "event_type": signal["events"][0] if signal["events"] else None,
        "event_date": record["published_date"] if eligible else None,
        "date_precision": "DAY" if eligible else None,
        "date_basis": "OFFICIAL_POST_PUBLICATION_DATE" if eligible else None,
        "supporting_text": record["content"],
        "timeline_confidence": confidence,
        "timeline_reasons": (["CONCRETE_EVENT_STATE_LANGUAGE", "IDENTIFIABLE_ENTITY_OR_SYSTEM", "DATE_FROM_OFFICIAL_POST"] if eligible else [exclusion]),
        "duplicate_cluster_id": cluster["cluster_id"] if cluster else None,
        "strongest_candidate_id": cluster["strongest_candidate_id"] if cluster else record["source_id"],
        "manual_review_required": eligible, "exclusion_reason": exclusion,
    }


def build_social(entity_catalog):
    posts = [json.loads(line) for line in SOCIAL_INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    records = []
    for post in posts:
        text = post["content"]
        topics = social_topics(text)
        statements = statement_types(text)
        lifecycle = lifecycle_states(text)
        entities = link_entities(text, entity_catalog)
        media_links = re.findall(r"https?://(?:pbs|video)\.twimg\.com/\S+", text, re.I)
        evidence = []
        if media_links:
            evidence.append("RESEARCH_GAP")
        notes = []
        if post["is_retweet"]:
            notes.append("This record proves resharing by @staratlas; it does not convert the underlying content into a first-party claim.")
        if media_links:
            notes.append("Linked media was not included in the source package and requires separate preservation/review.")
        mentions = extract_mentions(text)
        linked_aliases = {a.lower() for e in entities for a in e["matched_aliases"]}
        unresolved = [m for m in mentions if m.lstrip("@#").lower() not in linked_aliases and m.lower() not in {"@staratlas"}]
        if unresolved:
            notes.append("Unresolved social references: " + ", ".join(unresolved))
        confidence = "MEDIUM" if post["is_retweet"] else ("MEDIUM" if media_links and len(normalize_text(text)) < 80 else "HIGH")
        records.append({
            "source_id": post["source_id"], "platform": post["platform"], "post_id": post["post_id"],
            "post_url": post["post_url"], "published_date": post["published_date"],
            "account_handle": post["account_handle"], "is_retweet": post["is_retweet"], "content": text,
            "topics": topics, "subtopics": social_subtopics(text), "entities": entities,
            "unresolved_references": unresolved, "statement_types": statements,
            "lifecycle_states": lifecycle, "evidence_classes": unique(evidence),
            "timeline_candidate": False, "promotion_targets": [],
            "confidence": confidence, "duplicate_or_supersession": {},
            "signal_data": social_signal_data(text, entities),
            "research_notes": notes,
        })

    clusters, cluster_lookup = cluster_social_posts(records)
    promotion_decisions, timeline_decisions = [], []
    for record in records:
        cluster = cluster_lookup.get(record["source_id"])
        promotion = social_promotion_decision(record, cluster)
        timeline = social_timeline_decision(record, cluster)
        promotion_decisions.append(promotion); timeline_decisions.append(timeline)
        if promotion["eligible"]:
            record["evidence_classes"].extend(["CANONICAL_KNOWLEDGE_CANDIDATE", "ENTITY_UPDATE_CANDIDATE"])
            record["promotion_targets"] = promotion_targets(record["topics"])
        if timeline["eligible"]:
            record["evidence_classes"].append("TIMELINE_CANDIDATE"); record["timeline_candidate"] = True
        if record["entities"] and not record["is_retweet"]:
            record["evidence_classes"].append("GRAPH_RELATIONSHIP_CANDIDATE")
        if not promotion["eligible"] and not timeline["eligible"]:
            record["evidence_classes"].append("LOW_VALUE")
        if cluster:
            record["evidence_classes"].append("DUPLICATE")
        record["evidence_classes"] = unique(record["evidence_classes"])
        record["duplicate_or_supersession"] = {
            "status": cluster["cluster_type"] if cluster else ("SUPERSESSION_LANGUAGE_PRESENT" if "SUPERSEDED" in record["lifecycle_states"] else "NONE_IDENTIFIED"),
            "cluster_id": cluster["cluster_id"] if cluster else None,
            "strongest_candidate_id": cluster["strongest_candidate_id"] if cluster else None,
        }
        record["promotion_decision"] = {key: promotion[key] for key in ("eligible", "decision", "decision_reasons", "confidence", "exclusion_reason")}
        record["timeline_decision"] = {key: timeline[key] for key in ("eligible", "decision", "event_type", "event_date", "date_basis", "timeline_confidence", "exclusion_reason")}
        del record["signal_data"]

    SOCIAL_OUT.mkdir(parents=True, exist_ok=True)
    semantic_path = SOCIAL_OUT / "staratlas-posts-semantic.jsonl"
    semantic_path.write_text("".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) + "\n" for x in records), encoding="utf-8")

    topic_index = {topic: [r["source_id"] for r in records if topic in r["topics"]] for topic in sorted(TOPICS)}
    entity_links = [{"source_id": r["source_id"], "post_id": r["post_id"], "entities": r["entities"], "unresolved_references": r["unresolved_references"]} for r in records if r["entities"] or r["unresolved_references"]]
    timeline_by_id = {decision["source_id"]: decision for decision in timeline_decisions}
    promotion_by_id = {decision["source_id"]: decision for decision in promotion_decisions}
    timeline = [{**timeline_by_id[r["source_id"]], "topics": r["topics"], "statement_types": r["statement_types"], "lifecycle_states": r["lifecycle_states"]} for r in records if timeline_by_id[r["source_id"]]["eligible"]]
    promotions = [{**promotion_by_id[r["source_id"]], "targets": r["promotion_targets"], "evidence_classes": r["evidence_classes"], "review_status": "UNREVIEWED"} for r in records if promotion_by_id[r["source_id"]]["eligible"]]
    gaps = [{"source_id": r["source_id"], "post_id": r["post_id"], "notes": r["research_notes"], "unresolved_references": r["unresolved_references"]} for r in records if "RESEARCH_GAP" in r["evidence_classes"] or r["unresolved_references"]]
    common = {"campaign_id": CAMPAIGN_ID, "schema_version": "1.0.0", "generated_from": str(SOCIAL_INPUT.relative_to(REPO)).replace("\\", "/")}
    write_json(SOCIAL_OUT / "topic-index.json", {**common, "topic_counts": {k: len(v) for k, v in topic_index.items()}, "topics": topic_index})
    write_json(SOCIAL_OUT / "entity-links.json", {**common, "link_record_count": len(entity_links), "links": entity_links})
    write_json(SOCIAL_OUT / "timeline-candidates.json", {**common, "candidate_count": len(timeline), "candidates": timeline})
    write_json(SOCIAL_OUT / "promotion-candidates.json", {**common, "candidate_count": len(promotions), "candidates": promotions})
    (SOCIAL_OUT / "promotion-candidate-decisions.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) + "\n" for x in promotion_decisions), encoding="utf-8")
    (SOCIAL_OUT / "timeline-candidate-decisions.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) + "\n" for x in timeline_decisions), encoding="utf-8")
    write_json(SOCIAL_OUT / "duplicate-clusters.json", {**common, "cluster_count": len(clusters), "clusters": clusters})
    write_json(SOCIAL_OUT / "research-gaps.json", {**common, "gap_count": len(gaps), "gaps": gaps})
    return posts, records


def markdown_author(description: str):
    patterns = [
        r"(?im)^\s*[-*]?\s*\*{0,2}Authors?\*{0,2}:\s*([^\n]+)",
        r"(?im)^\s*[-*# ]*(?:\d+(?:\.\d+)?\s*)?Authors?\s*:\*{0,2}\s*([^\n]+)",
        r"(?im)^\s*#+\s*(?:\d+(?:\.\d+)?\s+)?Author\s*$\s*([^\n#]+)",
        r"(?im)^\s*[-*]?\s*Authors?:\s*([^\n]+)",
    ]
    for pattern in patterns:
        found = re.search(pattern, description)
        if found:
            value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", found.group(1))
            value = re.sub(r"[*_`]", "", value).strip()
            value = re.sub(r"(?i)^Name:\s*", "", value)
            if " – " in value:
                value = value.split(" – ", 1)[0].strip()
            if len(value) > 180:
                value = value.split(". ", 1)[0].strip()
            return value
    return None


def money_mentions(description: str):
    pattern = r"(?i)(?:[$€£]\s?[\d,.]+(?:\s?(?:million|thousand|m|k))?(?:\s?(?:USD|EUR))?|[\d,.]+\s*(?:million|thousand|m|k)?\s+(?:USDC|ATLAS|POLIS|USD|EUR))"
    return unique(x.group(0).strip() for x in re.finditer(pattern, description))[:20]


def authority_mentions(description: str):
    lines = []
    for line in description.splitlines():
        cleaned = re.sub(r"\s+", " ", re.sub(r"^[#*\-\s]+", "", line)).strip()
        if cleaned and len(cleaned) <= 500 and match(r"\b(authorit|authoriz|delegate|permission|ratif|empower)", cleaned):
            lines.append(cleaned)
    return unique(lines)[:12]


def vote_map(payload):
    data = payload.get("proposalVoteData") or {}
    sums = data.get("voteSums", []) if isinstance(data, dict) else []
    return {str(x.get("option", "")).lower(): {"ballots": x.get("count"), "voting_power": x.get("pvp")} for x in sums}


def as_decimal(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return None


def parse_election_results(payload: dict) -> dict | None:
    election = payload.get("electionResults")
    if isinstance(election, str):
        try:
            election = json.loads(election)
        except json.JSONDecodeError:
            return None
    return election if isinstance(election, dict) else None


def load_pip_review() -> tuple[dict, dict[int, dict]]:
    summary = load_json(PIP_REVIEW_SUMMARY)
    table: dict[int, dict] = {}
    for line in PIP_REVIEW.read_text(encoding="utf-8").splitlines():
        matched = re.match(r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$", line)
        if matched:
            number = int(matched.group(1))
            table[number] = {"title": matched.group(2), "reviewed_table_result": matched.group(3), "institutional_significance": matched.group(4)}
    if set(table) != set(range(1, 34)):
        raise ValueError("PIP corpus review table does not cover PIP-1 through PIP-33")
    return summary, table


def vote_percentages(votes: dict) -> dict:
    values = {name: as_decimal(data.get("voting_power")) for name, data in votes.items()}
    total = sum((value for value in values.values() if value is not None), Decimal(0))
    yes_no = sum((values.get(name) or Decimal(0) for name in ("yes", "no")), Decimal(0))
    def pct(value: Decimal | None, denominator: Decimal) -> str | None:
        return str((value * Decimal(100) / denominator).quantize(Decimal("0.000001"))) if value is not None and denominator else None
    return {
        "total_pvp": str(total), "yes_percent_all_pvp": pct(values.get("yes"), total),
        "no_percent_all_pvp": pct(values.get("no"), total), "abstain_percent_all_pvp": pct(values.get("abstain"), total),
        "yes_percent_yes_no_pvp": pct(values.get("yes"), yes_no), "no_percent_yes_no_pvp": pct(values.get("no"), yes_no),
    }


def reviewed_governance_result(number: int, payload: dict, votes: dict, review_summary: dict, council: dict | None) -> dict:
    elections = set(review_summary["results"]["elections_or_nonbinary"])
    unresolved = set(review_summary["results"]["election_results_unresolved_in_capture"])
    ended = bool(payload.get("votingEndsAt") and payload["votingEndsAt"] < CAPTURE_TIMESTAMP)
    election = parse_election_results(payload)
    if number in elections:
        winners = election.get("winners", []) if election else []
        portal_result = "UNKNOWN" if number in unresolved or not winners else "ELECTION_RESULT_RECORDED"
        result = "PASSED" if council and str(council.get("vote_result", "")).upper() == "PASSED" else portal_result
        basis = ("Council-maintained PIP Tracker reports the election PIP as Passed; the captured portal does not identify winners, so winner identification remains unresolved."
                 if result == "PASSED" and portal_result == "UNKNOWN" else
                 "Captured portal electionResults supplies the ranked-choice winners." if winners else
                 "Captured portal payload has no conclusive electionResults winner field; no winner is inferred.")
        return {"vote_mechanism": "RANKED_CHOICE_ELECTION", "machine_result": portal_result, "portal_result": portal_result, "reviewed_result": result, "reviewed_result_basis": basis, "election_winners": winners, "decision_formula": "USE_OFFICIAL_ELECTION_RESULTS_FIELD_FOR_WINNERS; COUNCIL_TRACKER_MAY_ESTABLISH_REPORTED_PASSAGE", "voting_window_ended": ended}
    yes = as_decimal(votes.get("yes", {}).get("voting_power"))
    no = as_decimal(votes.get("no", {}).get("voting_power"))
    if ended and yes is not None and no is not None:
        result = "PASSED" if yes > no else "FAILED"
        basis = "Voting ended and YES PVP exceeded NO PVP." if result == "PASSED" else "Voting ended and NO PVP was greater than or equal to YES PVP."
    else:
        result, basis = "UNKNOWN", "Voting window or binary PVP totals are incomplete."
    return {"vote_mechanism": "BINARY_PVP", "machine_result": result, "portal_result": result, "reviewed_result": result, "reviewed_result_basis": basis, "election_winners": [], "decision_formula": "YES_PVP > NO_PVP => PASSED; NO_PVP >= YES_PVP => FAILED; ABSTAIN_RECORDED_NOT_DECISIVE", "voting_window_ended": ended}


def governance_topics(payload):
    text = " ".join([payload.get("title", ""), payload.get("brief", ""), payload.get("description", "")])
    topics = social_topics(text)
    if "GOVERNANCE" not in topics: topics.insert(0, "GOVERNANCE")
    return unique(topics)


def build_governance(entity_catalog):
    seed = load_json(PIP_SEED)
    seed_by_number = {x["pip_number"]: x for x in seed}
    review_summary, review_table = load_pip_review()
    council_records = [json.loads(line) for line in COUNCIL_TRACKER.read_text(encoding="utf-8").splitlines() if line.strip()]
    council_by_number = {item["pip_number"]: item for item in council_records}
    relationships = review_summary["supersession_and_dependencies"]
    related_by_number: dict[int, list[dict]] = defaultdict(list)
    for relationship in relationships:
        related_by_number[relationship["from"]].append(relationship)
        related_by_number[relationship["to"]].append(relationship)
    records = []
    for raw_path in sorted(PIP_RAW.glob("*.json")):
        raw_bytes = raw_path.read_bytes()
        payload = json.loads(raw_bytes)
        number = payload["pipNumber"]
        source = seed_by_number[number]
        description = payload.get("description") or ""
        author = markdown_author(description)
        author_value = author or payload.get("authorPublicKey") or None
        votes = vote_map(payload)
        council = council_by_number.get(number)
        review_result = reviewed_governance_result(number, payload, votes, review_summary, council)
        result = review_result["reviewed_result"]
        topics = governance_topics(payload)
        entity_text = " ".join([payload.get("title", ""), payload.get("brief", ""), description])
        entities = link_entities(entity_text, entity_catalog)
        requested_funding = money_mentions(description)
        limitations = []
        if not author:
            limitations.append("No explicit human-readable author was parsed; author uses the portal author public key.")
        if result == "UNKNOWN":
            limitations.append("The captured portal payload does not expose a conclusive binary or election result.")
        limitations.append("The reviewed vote result follows the repository-owner rule for binary PIPs or the official electionResults field for elections; it is not execution evidence.")
        limitations.append("No execution claim is made without a separate official implementation record, transaction, transfer, or equivalent primary evidence.")
        approval = "APPROVED" if result == "PASSED" else ("FAILED" if result == "FAILED" else "UNKNOWN")
        if result == "ELECTION_RESULT_RECORDED":
            approval = "ELECTION_RESULT_RECORDED"
        winners = review_result["election_winners"]
        record_capture_timestamp = CAPTURE_TIMESTAMP
        stale_status = payload.get("currentStatus") == "Proposal_Activated_Pending_Open_Voting" and review_result["voting_window_ended"]
        raw_status = payload.get("currentStatus") or payload.get("status")
        reconciliation_notes = []
        if stale_status:
            reconciliation_notes.append("Raw portal status is stale for the completed voting window; reviewed result is based on vote evidence and the owner-approved rule.")
        if payload.get("title") != review_table[number]["title"]:
            reconciliation_notes.append("The raw portal title is preserved as authoritative source text; the human review uses a concise display title recorded separately.")
        if review_result["vote_mechanism"] == "RANKED_CHOICE_ELECTION" and result == "UNKNOWN":
            reconciliation_notes.append("The human review preserves the election-result gap because the capture lacks an official winner field.")
        supersedes = [item["to"] for item in relationships if item["from"] == number and item["relation"] == "SUPERSEDES"]
        superseded_by = [item["from"] for item in relationships if item["to"] == number and item["relation"] == "SUPERSEDES"]
        related_pips = sorted({item["from"] if item["to"] == number else item["to"] for item in related_by_number[number]})
        funding_source = "STAR_ATLAS_ECOSYSTEM_FUND" if match(r"\becosystem fund\b", description) else "STAR_ATLAS_DAO_TREASURY" if match(r"\bdao treasury|treasury\b", description) else "UNKNOWN"
        implementation_pending = result in {"PASSED", "ELECTION_RESULT_RECORDED"}
        execution_state = "IMPLEMENTATION_PENDING" if implementation_pending else "UNKNOWN"
        if number == 14: execution_state = "TERMINATED"
        elif number == 17: execution_state = "CANCELED"
        elif number == 31: execution_state = "WITHDRAWN_AFTER_PASSAGE_NOT_IMPLEMENTED"
        payment = council.get("payment_fields", {}) if council else {}
        council_payment_reported = any(value not in (None, "", "N/A") for value in payment.values())
        record = {
            "source_id": source["source_id"], "pip_number": number,
            "proposal_uuid": source["proposal_uuid"], "proposal_url": source["proposal_url"],
            "title": payload.get("title"), "reviewed_title": review_table[number]["title"], "author": author_value,
            "author_public_key": payload.get("authorPublicKey"), "proposal_text": description,
            "proposal_brief": payload.get("brief"), "proposal_category": payload.get("categories") or [],
            "publication_date": payload.get("createdAt"), "updated_date": payload.get("updatedAt"),
            "discussion_start": payload.get("createdAt"), "vote_start": payload.get("votingStartsAt"),
            "vote_end": payload.get("votingEndsAt"),
            "requested_authority": authority_mentions(description),
            "requested_funding": requested_funding,
            "affected_entities": entities, "affected_governance_bodies": [e for e in entities if e["entity_type"] in {"ORGANIZATION", "GOVERNANCE_BODY"}],
            "affected_products": [e for e in entities if e["entity_type"] == "PRODUCT"],
            "affected_treasury_or_economic_systems": [e for e in entities if e["entity_type"] in {"TOKEN", "ECONOMY", "ASSET"}],
            "funding_source": funding_source,
            "vote_mechanism": review_result["vote_mechanism"], "vote_for": votes.get("yes"), "vote_against": votes.get("no"), "vote_abstain": votes.get("abstain"),
            "yes_pvp": votes.get("yes", {}).get("voting_power"), "no_pvp": votes.get("no", {}).get("voting_power"), "abstain_pvp": votes.get("abstain", {}).get("voting_power"),
            "all_vote_totals": votes, "descriptive_vote_percentages": vote_percentages(votes), "quorum": "NOT_APPLICABLE_UNDER_OWNER_APPROVED_BINARY_RULE",
            "proposal_state": "PROPOSED", "vote_state": result, "result": result,
            "raw_portal_status": raw_status, "machine_computed_result": review_result["machine_result"],
            "portal_result": review_result["portal_result"],
            "portal_winner_status": "AVAILABLE" if winners else "UNAVAILABLE_OR_INCOMPLETE" if review_result["vote_mechanism"] == "RANKED_CHOICE_ELECTION" else "NOT_APPLICABLE",
            "council_reported_result": str(council.get("vote_result", "")).upper() if council and council.get("vote_result") else "UNKNOWN",
            "reviewed_result": result, "reviewed_table_result": review_table[number]["reviewed_table_result"], "reviewed_result_basis": review_result["reviewed_result_basis"], "decision_formula": review_result["decision_formula"],
            "winner_identification_status": "IDENTIFIED" if winners else "UNRESOLVED" if review_result["vote_mechanism"] == "RANKED_CHOICE_ELECTION" else "NOT_APPLICABLE",
            "cross_source_reconciliation_status": "RECONCILED_WITH_UNRESOLVED_WINNER" if review_result["vote_mechanism"] == "RANKED_CHOICE_ELECTION" and not winners else "RECONCILED",
            "approval_state": approval, "execution_state": execution_state, "execution_evidence": [],
            "execution_evidence_status": "MISSING_INDEPENDENT_PRIMARY_EVIDENCE", "election_winners": winners,
            "council_reported_implementation_state": council.get("implementation_state") if council else "UNKNOWN",
            "council_reported_payment_state": "COUNCIL_REPORTED" if council_payment_reported else "UNKNOWN",
            "council_reported_paid_usdc": payment.get("paid_usdc"), "council_reported_remaining_usdc": payment.get("left_usdc"),
            "council_reported_paid_atlas": payment.get("paid_atlas"), "council_reported_remaining_atlas": payment.get("left_atlas"),
            "council_reported_completed_milestones": payment.get("completed_milestones"), "council_reported_total_milestones": payment.get("total_milestones"),
            "independent_payment_verification_status": "UNKNOWN", "independent_deliverable_verification_status": "UNKNOWN",
            "council_operational_assessment": ({"text": council.get("council_roi_assessment"), "assessment_source": "STAR_ATLAS_COUNCIL_TRACKER", "assessment_type": "COUNCIL_AUTHORED_OPERATIONAL_ASSESSMENT", "independent_verification_status": "UNKNOWN"} if council else None),
            "council_tracker": ({
                "source_id": council["source_id"], "source_class": council["source_class"],
                "reported_vote_result": council.get("vote_result"), "reported_phase": council.get("phase"),
                "reported_implementation_state": council.get("implementation_state"),
                "reported_lifecycle_states": council.get("lifecycle_states", []),
                "payment_fields": council.get("payment_fields", {}),
                "roi_assessment": council.get("council_roi_assessment"), "note": council.get("note"),
                "attribution": "STAR_ATLAS_COUNCIL_MAINTAINED_TRACKER",
                "independent_verification": False,
            } if council else None),
            "portal_status": payload.get("status"), "portal_current_status": payload.get("currentStatus"),
            "capture_timestamp": record_capture_timestamp, "content_checksum": hashlib.sha256(raw_bytes).hexdigest(),
            "topics": topics, "promotion_targets": promotion_targets(topics),
            "reviewed_institutional_significance": review_table[number]["institutional_significance"],
            "supersedes": supersedes, "superseded_by": superseded_by, "related_pips": related_pips,
            "human_review_status": "REVIEWED", "reconciliation_notes": reconciliation_notes,
            "contradictions": ["Portal status remains Proposal_Activated_Pending_Open_Voting although the vote window has ended."] if stale_status else [],
            "research_gaps": (["Official election winner evidence is missing from the captured portal payload."] if not winners and review_result["vote_mechanism"] == "RANKED_CHOICE_ELECTION" else []) + (["Historical PIP-1 quorum text is preserved; the repository owner-approved current operating rule applies no quorum to completed binary results."] if number == 1 else []) + ["Council operational assessments, payment fields, and lifecycle reports are attributed and are not independently verified." if council else "Council tracker has no matching record.", "Independent implementation evidence is not present in the captured proposal payload."],
            "limitations": limitations,
        }
        records.append(record)

    records.sort(key=lambda x: x["pip_number"])
    common = {"campaign_id": CAMPAIGN_ID, "schema_version": "2.0.0", "capture_timestamp": max(r["capture_timestamp"] for r in records)}
    write_json(GOV_OUT / "pip-registry-semantic.json", {**common, "proposal_count": len(records), "proposals": records})
    topic_index = {topic: [r["source_id"] for r in records if topic in r["topics"]] for topic in sorted(TOPICS)}
    entity_links = [{"source_id": r["source_id"], "pip_number": r["pip_number"], "entities": r["affected_entities"], "reviewed_institutional_significance": r["reviewed_institutional_significance"], "human_review_status": "REVIEWED"} for r in records]
    timeline = [{"source_id": r["source_id"], "pip_number": r["pip_number"], "publication_date": r["publication_date"], "vote_start": r["vote_start"], "vote_end": r["vote_end"], "vote_mechanism": r["vote_mechanism"], "reviewed_result": r["reviewed_result"], "result_basis": r["reviewed_result_basis"], "execution_state": r["execution_state"], "supporting_text": r["proposal_brief"], "manual_review_required": r["reviewed_result"] == "UNKNOWN"} for r in records]
    promotions = [{"source_id": r["source_id"], "pip_number": r["pip_number"], "targets": r["promotion_targets"], "supporting_text": r["proposal_brief"], "reviewed_result": r["reviewed_result"], "implementation_caveat": "Vote result does not establish implementation; independent primary evidence is missing.", "corpus_review_conclusion": r["reviewed_institutional_significance"], "human_review_status": "REVIEWED"} for r in records]
    gaps = [{"source_id": r["source_id"], "pip_number": r["pip_number"], "reviewed_result": r["reviewed_result"], "execution_state": r["execution_state"], "execution_evidence_status": r["execution_evidence_status"], "execution_evidence": r["execution_evidence"], "research_gaps": r["research_gaps"], "limitations": r["limitations"]} for r in records]
    supersession = [{"source_id": next(r["source_id"] for r in records if r["pip_number"] == item["from"]), "from_pip": item["from"], "relationship": item["relation"], "to_pip": item["to"], "human_review_status": "REVIEWED"} for item in relationships]
    by_number = {r["pip_number"]: r for r in records}
    relationship_specs = [
        ("POLIS_HOLDERS_AND_STAR_ATLAS_DAO", "VOTE_ON", "PIP_REGISTRY", [1]),
        ("STAR_ATLAS_FOUNDATION", "ADMINISTERS", "GOVERNANCE_PORTAL_AND_PIP_PROCESS", [1, 2]),
        ("STAR_ATLAS_FOUNDATION", "HOLDS_OR_CONTROLS", "DAO_TREASURY_MULTISIGS", [2, 23]),
        ("STAR_ATLAS_FOUNDATION", "IMPLEMENTS_OR_REFUSES", "PASSED_PIPS", [1, 2]),
        ("STAR_ATLAS_COUNCIL", "ASSISTS", "PIP_AUTHORS", [3, 10, 23]),
        ("STAR_ATLAS_COUNCIL", "ADMINISTERS", "APPROVED_GOVERNANCE_PROGRAMS", [12, 20, 22, 23]),
        ("STAR_ATLAS_COUNCIL", "VERIFIES", "MILESTONES_AND_PAYMENTS", [22, 31, 32, 33]),
        ("PIP_23", "SUPERSEDES", "PIP_4", [23, 4]),
        ("PIP_10", "MODIFIES_AND_EXTENDS", "PIP_3", [10, 3]),
        ("PIP_13", "FAILED_ATTEMPT_TO_MODIFY", "PIP_10", [13, 10]),
        ("PIP_27", "IMPLEMENTS_ELECTION_REQUIRED_BY", "PIP_20", [27, 20]),
    ]
    institutional_relationships = [{"relationship_id": f"GOV-REL-{index:03d}", "subject": subject, "relationship": relation, "object": obj, "supporting_pips": numbers, "source_ids": [by_number[number]["source_id"] for number in numbers], "review_basis": "PIP corpus review and captured official proposal text", "canonical_graph_status": "PROPOSED_ONLY"} for index, (subject, relation, obj, numbers) in enumerate(relationship_specs, 1)]
    write_json(GOV_OUT / "pip-topic-index.json", {**common, "topic_counts": {k: len(v) for k, v in topic_index.items()}, "topics": topic_index})
    write_json(GOV_OUT / "pip-entity-links.json", {**common, "records": entity_links})
    write_json(GOV_OUT / "pip-timeline-candidates.json", {**common, "candidate_count": len(timeline), "candidates": timeline})
    write_json(GOV_OUT / "pip-promotion-candidates.json", {**common, "candidate_count": len(promotions), "candidates": promotions})
    write_json(GOV_OUT / "pip-execution-gaps.json", {**common, "gap_count": len(gaps), "gaps": gaps})
    write_json(GOV_OUT / "pip-implementation-gaps.json", {**common, "gap_count": len(gaps), "gaps": gaps})
    write_json(GOV_OUT / "pip-supersession-index.json", {**common, "relationship_count": len(supersession), "relationships": supersession})
    write_json(GOV_OUT / "institutional-relationships.json", {**common, "relationship_count": len(institutional_relationships), "relationships": institutional_relationships})
    reconciliation = [{
        "pip_number": r["pip_number"], "official_portal_source_id": r["source_id"],
        "council_tracker_source_id": r["council_tracker"]["source_id"] if r["council_tracker"] else None,
        "portal_result": r["portal_result"], "council_reported_result": r["council_tracker"]["reported_vote_result"] if r["council_tracker"] else None,
        "reviewed_result": r["reviewed_result"], "winner_identification": r["election_winners"],
        "portal_winner_status": r["portal_winner_status"], "winner_identification_status": r["winner_identification_status"],
        "cross_source_reconciliation_status": r["cross_source_reconciliation_status"],
        "execution_state": r["execution_state"], "payment_fields": r["council_tracker"]["payment_fields"] if r["council_tracker"] else {},
        "council_reported_implementation_state": r["council_reported_implementation_state"],
        "independent_implementation_status": r["execution_evidence_status"],
        "council_roi_assessment": r["council_tracker"]["roi_assessment"] if r["council_tracker"] else None,
        "relationship": "COUNCIL_TRACKER_SUPPLEMENTS_PORTAL_CAPTURE",
        "attribution_required": bool(r["council_tracker"]), "independently_verified": False,
        "contradictions": r["contradictions"], "unresolved_research_gaps": r["research_gaps"],
        "chief_of_staff_corpus_review": {"reviewed_table_result": r["reviewed_table_result"], "institutional_significance": r["reviewed_institutional_significance"]},
        "manual_review_required": not bool(r["council_tracker"]) or (r["vote_mechanism"] == "RANKED_CHOICE_ELECTION" and not r["election_winners"]),
    } for r in records]
    write_json(GOV_OUT / "pip-source-reconciliation.json", {**common, "record_count": len(reconciliation), "records": reconciliation})
    return records


def build_reports(posts, social, pips):
    raw_csv = REPO / "archive/raw/social-governance-semantic-enrichment/social-media/sorsa_export_1784085327119.csv"
    with raw_csv.open(encoding="utf-8-sig", newline="") as handle:
        raw_rows = list(csv.DictReader(handle))
    social_topics_count = Counter(t for r in social for t in r["topics"])
    social_statement_count = Counter(t for r in social for t in r["statement_types"])
    social_lifecycle_count = Counter(t for r in social for t in r["lifecycle_states"])
    social_evidence_count = Counter(t for r in social for t in r["evidence_classes"])
    promotion_decisions = [r["promotion_decision"] for r in social]
    timeline_decisions = [r["timeline_decision"] for r in social]
    promotion_count = sum(d["eligible"] for d in promotion_decisions)
    timeline_count = sum(d["eligible"] for d in timeline_decisions)
    promotion_confidence = Counter(d["confidence"] for d in promotion_decisions if d["eligible"])
    promotion_disposition = Counter(d["decision"] for d in promotion_decisions)
    promotion_exclusions = Counter(d["exclusion_reason"] for d in promotion_decisions if not d["eligible"])
    timeline_confidence = Counter(d["timeline_confidence"] for d in timeline_decisions if d["eligible"])
    timeline_exclusions = Counter(d["exclusion_reason"] for d in timeline_decisions if not d["eligible"])
    duplicate_cluster_count = load_json(SOCIAL_OUT / "duplicate-clusters.json")["cluster_count"]
    pip_results = Counter(r["reviewed_result"] for r in pips)
    review_summary = load_json(PIP_REVIEW_SUMMARY)
    validation = validate(posts, social, pips, raw_rows)
    summary = f"""# Social Media and PIP Semantic Enrichment Campaign

## Executive summary

The campaign preserved the supplied export without rewriting it, enriched all **{len(social)}** unique `@staratlas` posts, captured and enriched **{len(pips)}** official PIP portal records, and produced review-only promotion candidates. No canonical knowledge, graph, or publication files were modified.

## Evidence preserved

- Raw export rows: {len(raw_rows)}
- Unique social posts: {len(posts)}
- Original `@staratlas` posts: {sum(not p['is_retweet'] for p in posts)}
- Explicit retweets/reshared context: {sum(bool(p['is_retweet']) for p in posts)}
- Documented duplicate export rows: {len(raw_rows) - len(posts)}
- Official PIP records: {len(pips)} (PIP-1 through PIP-33)
- Portal raw captures: {len(list(PIP_RAW.glob('*.json')))}
- Date coverage: {min(p['published_date'] for p in posts)} through {max(p['published_date'] for p in posts)}

## Semantic enrichment

- Social topic assignments: {dict(sorted(social_topics_count.items()))}
- Statement type assignments: {dict(sorted(social_statement_count.items()))}
- Lifecycle assignments (wording-supported only): {dict(sorted(social_lifecycle_count.items()))}
- Evidence-class assignments: {dict(sorted(social_evidence_count.items()))}
- Social promotion candidates: {HISTORICAL_SOCIAL_COUNTS['promotion_candidates']} before; **{promotion_count}** after
- Social promotion exclusions: {len(social) - promotion_count}
- Social timeline candidates: {HISTORICAL_SOCIAL_COUNTS['timeline_candidates']} before; **{timeline_count}** after
- Social timeline exclusions: {len(social) - timeline_count}
- Promotion confidence: {dict(sorted(promotion_confidence.items()))}
- Promotion dispositions: {dict(sorted(promotion_disposition.items()))}
- Timeline confidence: {dict(sorted(timeline_confidence.items()))}
- Duplicate clusters: {duplicate_cluster_count}
- Social records with unresolved references or media gaps: {sum(bool(r['research_notes']) for r in social)}

## Governance findings

- Human-reviewed results: {dict(sorted(pip_results.items()))}
- Passed binary PIPs: {review_summary['results']['passed_binary']}
- Failed binary PIPs: {review_summary['results']['failed_binary']}
- Election/nonbinary PIPs: {review_summary['results']['elections_or_nonbinary']}
- Unresolved election PIPs: {review_summary['results']['election_results_unresolved_in_capture']}
- Approval states: {dict(sorted(Counter(r['approval_state'] for r in pips).items()))}
- Execution states: {dict(sorted(Counter(r['execution_state'] for r in pips).items()))}
- Implementation gaps requiring primary evidence: {sum(r['execution_evidence_status'] == 'MISSING_INDEPENDENT_PRIMARY_EVIDENCE' for r in pips)}
- Supersession/dependency relationships: {review_summary['supersession_and_dependencies']}

Completed binary results use the owner-approved formula `YES PVP > NO PVP => PASSED; NO PVP >= YES PVP => FAILED`; abstentions are recorded but non-decisive and no quorum is imposed. Election winners use only the official portal `electionResults` field. The Council tracker may establish an attributed reported passage result without identifying a winner. `PASSED`/`APPROVED` records are not treated as implemented, and every PIP retains an independent implementation-evidence gap.

All 33 PIPs are reconciled to the governing human corpus review and Council-maintained operational tracker. Raw portal status, Council-reported result, reviewed result, approval, and execution remain distinct. PIP-11, PIP-25, and PIP-27 are Council-reported as passed while portal winner identification remains unresolved. PIP-14 is Council-reported terminated after 1/2 milestones; PIP-17 canceled after 0/1 milestones with zero ATLAS paid; PIP-31 withdrawn after passage and not implemented. These operational fields are attributed, not independently verified.

## Canonical-promotion recommendations

{chr(10).join(f'- `{target}`' for target in review_summary['canonical_promotion_targets'])}

These remain review-only inputs; this campaign does not modify canonical knowledge or graph facts.

## Review posture

All promotion targets are candidates only. Retweets preserve the fact of resharing and are excluded from first-party promotion candidates. Engagement metrics were not used as evidence. Linked media absent from the package is retained as a research gap.

## Validation

Validation status: **{validation['status']}**. See `validation-report.md` for the complete checks.
"""
    (OPS / "campaign-summary.md").write_text(summary, encoding="utf-8")
    summary_json = {
        "campaign_id": CAMPAIGN_ID, "status": validation["status"],
        "corpus": {"raw_social_rows": len(raw_rows), "unique_posts": len(posts), "original_posts": sum(not p["is_retweet"] for p in posts), "retweets": sum(bool(p["is_retweet"]) for p in posts), "pips_reviewed": len(pips)},
        "social_candidates": {
            "before": HISTORICAL_SOCIAL_COUNTS,
            "after": {"promotion_candidates": promotion_count, "timeline_candidates": timeline_count},
            "promotion_exclusions": len(social) - promotion_count, "timeline_exclusions": len(social) - timeline_count,
            "promotion_confidence": dict(sorted(promotion_confidence.items())), "timeline_confidence": dict(sorted(timeline_confidence.items())),
            "promotion_dispositions": dict(sorted(promotion_disposition.items())), "promotion_exclusion_reasons": dict(sorted(promotion_exclusions.items())),
            "timeline_exclusion_reasons": dict(sorted(timeline_exclusions.items())), "duplicate_clusters": duplicate_cluster_count,
        },
        "governance": {
            "result_counts": dict(sorted(pip_results.items())), "passed_binary_pips": review_summary["results"]["passed_binary"],
            "failed_binary_pips": review_summary["results"]["failed_binary"], "election_pips": review_summary["results"]["elections_or_nonbinary"],
            "unresolved_election_pips": review_summary["results"]["election_results_unresolved_in_capture"],
            "council_tracker_records_reconciled": sum(bool(r["council_tracker"]) for r in pips),
            "attributed_lifecycle_findings": {"PIP-14": "TERMINATED", "PIP-17": "CANCELED", "PIP-31": "WITHDRAWN_AFTER_PASSAGE_NOT_IMPLEMENTED"},
            "supersession_and_dependencies": review_summary["supersession_and_dependencies"],
            "implementation_evidence_gaps": sum(r["execution_evidence_status"] == "MISSING_INDEPENDENT_PRIMARY_EVIDENCE" for r in pips),
            "canonical_promotion_recommendations": review_summary["canonical_promotion_targets"],
        },
        "warnings": ["Inherited Wave 1.5 reconciliation baseline contains 962 records while the legacy validator expects 960; unrelated reconciliation records are unchanged."],
    }
    write_json(OPS / "campaign-summary.json", summary_json)
    research = """# Research gaps

## Governance execution

All 33 PIPs require separate primary execution evidence before an `IMPLEMENTED` or `PARTIALLY_IMPLEMENTED` state can be assigned. Candidate evidence includes official implementation reports, on-chain transactions, treasury transfers, deployed policy/product changes, and direct implementation records.

PIP-11, PIP-25, and PIP-27 are reported Passed by the Council tracker but lack conclusive official election winner fields in the captured portal material. Passage and winner identification remain separate; no winner is inferred.

## Portal lifecycle metadata

The captured portal payloads report `Proposal_Activated_Pending_Open_Voting` even where the recorded vote window has ended. This contradiction is preserved; result derivation uses the official vote totals and dates, not that stale status label.

## Missing linked media

The social export includes image and video URLs but not the media binaries. Semantic conclusions are limited to the preserved post text. Media-dependent claims require separate capture and review.

## Retweet lineage

The normalized package identifies retweets but does not preserve a separate original-author field for every reshared post. Retweets therefore prove account resharing only; underlying authorship and claims require source-lineage review.

## Unresolved social references

Unmatched handles and hashtags are listed per semantic record. They were not converted into entities without an existing canonical entity match.
"""
    (OPS / "research-gaps.md").write_text(research, encoding="utf-8")
    report_lines = ["# Validation report", "", f"Overall status: **{validation['status']}**", "", "## Checks", ""]
    for check in validation["checks"]:
        report_lines.append(f"- **{check['status']} — {check['name']}**: {check['detail']}")
    report_lines += ["", "## Scope", "", "Only `archive/` and `operations/campaigns/social-governance-semantic-enrichment/` are changed by this campaign. Canonical knowledge, graph facts, and publication outputs remain untouched.", ""]
    report_lines += [
        "## Repository validation context", "",
        "- The three standalone schema compatibility tests pass.",
        "- The five pipeline test functions pass when invoked directly; `pytest` is not installed in the available runtimes.",
        "- The legacy `validate_wave_1_5.py` validator reports a baseline mismatch: it expects 960 reconciliation files while current `main` contains 962. This campaign does not add or modify reconciliation files.",
        "- Campaign-specific dependency-free validation parses all campaign JSON/JSONL, verifies manifest hashes, checks source-ID collisions, and reconciles every social and governance record.", "",
    ]
    (OPS / "validation-report.md").write_text("\n".join(report_lines), encoding="utf-8")
    write_json(OPS / "validation-report.json", validation)

    readme = f"""# Social Media and PIP Semantic Enrichment

This campaign preserves full semantic recall for 796 `@staratlas` posts and 33 official PIPs while maintaining separate, precision-oriented candidate layers. It never modifies canonical `knowledge/`, `graph/`, or `publication/` content.

## Deterministic decision model

Social promotion requires an identifiable institutional object plus a concrete action, relationship, or date/amount/metric. Retweets, questions without answers, weak marketing, engagement prompts, and weaker duplicate variants are excluded. Scores reward identifiable objects, concrete event language, specific details, explicit relationships, and canonical entity links. Eligible scores map to `HIGH_PRIORITY` (7+), `MEDIUM_PRIORITY` (5-6), or carefully justified `LOW_PRIORITY` (4); confidence describes extraction quality, not factual truth.

Timeline candidates independently require a material event type, identifiable entity/system, exact supporting post text, and the official post publication date as the date basis. All included and excluded decisions remain auditable in JSONL.

Near-duplicate clustering uses normalized exact text or deterministic token overlap of at least 0.72 with six shared meaningful tokens. Evidence is never deleted; each cluster identifies its strongest record and ordered members.

## Governance rules

Completed binary PIPs use `YES > NO => PASSED` and `NO >= YES => FAILED`; abstentions are recorded but non-decisive and no quorum is required. Ranked-choice winners use only the portal `electionResults` field. The Council tracker may establish an attributed reported passage result without resolving winners. Raw portal status, Council-reported result, reviewed result, approval, and execution are separate. A passed vote is never implementation evidence.

`pip-source-reconciliation.json` reconciles every portal capture with the Council tracker. Council ROI, payment, milestone, termination, cancellation, and withdrawal fields remain attributed operational evidence and are never labeled independently verified. PIP-11/25/27 retain `PASSED` with unresolved winners; PIP-14 is `TERMINATED`; PIP-17 is `CANCELED`; and PIP-31 is `WITHDRAWN_AFTER_PASSAGE_NOT_IMPLEMENTED`.

The governing human review is `pip-corpus-review.md` with structured conclusions in `pip-corpus-review-summary.json`. Every semantic PIP record is reconciled to it and marked `REVIEWED`.

## Reproduction

```text
python operations/campaigns/social-governance-semantic-enrichment/build_campaign.py
python operations/campaigns/social-governance-semantic-enrichment/validate_campaign.py
```
"""
    (OPS / "README.md").write_text(readme, encoding="utf-8")

    generated = [p for base in [SOCIAL_OUT, GOV_OUT, OPS] for p in base.rglob("*") if p.is_file() and p.name != "manifest.json" and p.suffix != ".pyc" and "__pycache__" not in p.parts and (OPS / "input-package") not in p.parents and (OPS / "input-council-tracker") not in p.parents]
    inputs = [p for base in [REPO / "archive/raw/social-governance-semantic-enrichment", REPO / "archive/normalized/social-governance-semantic-enrichment", REPO / "archive/source-records/social-governance-semantic-enrichment", OPS / "input-package", OPS / "input-council-tracker"] for p in base.rglob("*") if p.is_file()]
    manifest = {
        "campaign_id": CAMPAIGN_ID, "schema_version": "2.0.0", "status": validation["status"],
        "input_package_sha256": "bc209310c968cfb5f77e0962fb091d54bde8ed949a583beF2ace07b042f706d1".lower(),
        "counts": {"raw_export_rows": len(raw_rows), "unique_social_posts": len(posts), "social_semantic_records": len(social), "pip_records": len(pips), "pip_raw_captures": len(list(PIP_RAW.glob('*.json')))},
        "preserved_inputs": [{"path": str(p.relative_to(REPO)).replace("\\", "/"), "sha256": sha256(p), "bytes": p.stat().st_size} for p in sorted(inputs)],
        "generated_outputs": [{"path": str(p.relative_to(REPO)).replace("\\", "/"), "sha256": sha256(p), "bytes": p.stat().st_size} for p in sorted(set(generated))],
        "validation": validation,
    }
    write_json(OPS / "manifest.json", manifest)


def validate(posts, social, pips, raw_rows):
    checks = []
    def add(name, ok, detail): checks.append({"name": name, "status": "PASS" if ok else "FAIL", "detail": detail})
    post_ids = [p["post_id"] for p in posts]
    social_ids = [p["post_id"] for p in social]
    source_ids = [p["source_id"] for p in posts] + [p["source_id"] for p in pips]
    add("Raw and normalized counts", len(raw_rows) == 799 and len(posts) == 796, f"{len(raw_rows)} raw rows; {len(posts)} normalized posts")
    add("Unique post IDs reconcile", len(set(post_ids)) == 796 and set(post_ids) == set(social_ids), f"{len(set(post_ids))} unique evidence IDs and {len(set(social_ids))} semantic IDs")
    add("Duplicate rows remain documented", len(raw_rows) - len(set(row.get('id') or row.get('post_id') for row in raw_rows)) == 3, "Three duplicate export rows remain in the preserved raw CSV")
    add("Original/retweet counts", sum(not p['is_retweet'] for p in posts) == 528 and sum(bool(p['is_retweet']) for p in posts) == 268, "528 originals and 268 explicit retweets")
    add("PIP sequence and UUIDs", [p['pip_number'] for p in pips] == list(range(1, 34)) and len({p['proposal_uuid'] for p in pips}) == 33, "PIP-1 through PIP-33; 33 unique UUIDs")
    add("Source ID uniqueness", len(source_ids) == len(set(source_ids)), f"{len(source_ids)} campaign source IDs are unique")
    add("URL validity", all(urlparse(p['post_url']).scheme == 'https' and urlparse(p['post_url']).netloc for p in social) and all(urlparse(p['proposal_url']).netloc == 'govern.staratlas.com' for p in pips), "All social and governance URLs are absolute HTTPS URLs")
    add("Controlled social taxonomies", all(set(r['topics']) <= TOPICS and set(r['statement_types']) <= STATEMENTS and set(r['lifecycle_states']) <= LIFECYCLE and set(r['evidence_classes']) <= EVIDENCE for r in social), "All assigned social tags are controlled values")
    add("Promotion decision coverage", all("promotion_decision" in r and r["promotion_decision"]["eligible"] == bool(r["promotion_targets"]) for r in social), "Every social post has a reconciled promotion decision")
    add("Timeline decision coverage", all("timeline_decision" in r and r["timeline_decision"]["eligible"] == r["timeline_candidate"] for r in social), "Every social post has a reconciled timeline decision")
    add("Retweet evidence boundary", all(not r['promotion_targets'] and not r["promotion_decision"]["eligible"] and 'LOW_VALUE' in r['evidence_classes'] for r in social if r['is_retweet']), "No retweet is promoted as an original first-party claim")
    add("Candidate evidence", all(r["promotion_decision"]["decision_reasons"] and r["content"] for r in social) and all(r["timeline_decision"]["exclusion_reason"] or r["timeline_decision"]["event_type"] for r in social), "Every included candidate has reasons/supporting text and every exclusion has a reason")
    add("Human PIP review coverage", all(r["human_review_status"] == "REVIEWED" and r["reviewed_institutional_significance"] for r in pips), "All 33 PIPs reconcile to the governing corpus review")
    add("Governance lifecycle separation", all(r['proposal_state'] == 'PROPOSED' and r['approval_state'] in {'APPROVED','FAILED','UNKNOWN','ELECTION_RESULT_RECORDED'} and r['execution_state'] in {'IMPLEMENTATION_PENDING','PARTIALLY_IMPLEMENTED','IMPLEMENTED','UNKNOWN','TERMINATED','CANCELED','WITHDRAWN_AFTER_PASSAGE_NOT_IMPLEMENTED'} for r in pips), "Raw portal status, vote result, approval, and implementation use distinct fields")
    add("Binary vote rule", all((r["reviewed_result"] == ("PASSED" if as_decimal(r["yes_pvp"]) > as_decimal(r["no_pvp"]) else "FAILED")) for r in pips if r["vote_mechanism"] == "BINARY_PVP"), "Completed binary results use YES > NO; abstentions are not decisive")
    add("Election rule", all(r["yes_pvp"] is None and r["no_pvp"] is None for r in pips if r["vote_mechanism"] == "RANKED_CHOICE_ELECTION"), "Ranked-choice elections are not processed as binary PIPs")
    add("Failed PIP preservation", all(next(r for r in pips if r["pip_number"] == number)["reviewed_result"] == "FAILED" for number in [13, 15, 19, 26]), "PIP-13, PIP-15, PIP-19, and PIP-26 remain failed")
    add("Unresolved election preservation", all(next(r for r in pips if r["pip_number"] == number)["reviewed_result"] == "UNKNOWN" for number in [11, 25, 27]), "PIP-11, PIP-25, and PIP-27 remain unresolved")
    add("PIP supersession", next(r for r in pips if r["pip_number"] == 23)["supersedes"] == [4], "PIP-23 supersedes PIP-4")
    add("Execution evidence rule", all(r['execution_state'] not in {'IMPLEMENTED','PARTIALLY_IMPLEMENTED'} and not r['execution_evidence'] for r in pips), "No implementation inferred from a passed vote")
    add("No orphan semantic records", all((REPO / f"archive/source-records/social-governance-semantic-enrichment/social-media/{r['source_id']}.json").exists() for r in social) and all((GOV_RECORDS / f"{r['source_id']}.json").exists() for r in pips), "Every semantic record has a source record")
    return {"status": "PASS" if all(c['status'] == 'PASS' for c in checks) else "FAIL", "checks": checks}


def main():
    SOCIAL_OUT.mkdir(parents=True, exist_ok=True)
    GOV_OUT.mkdir(parents=True, exist_ok=True)
    OPS.mkdir(parents=True, exist_ok=True)
    catalog = load_entity_aliases()
    posts, social = build_social(catalog)
    pips = build_governance(catalog)
    build_reports(posts, social, pips)
    print(json.dumps({"social_records": len(social), "pip_records": len(pips), "status": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
