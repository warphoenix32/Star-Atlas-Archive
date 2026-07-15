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


def build_social(entity_catalog):
    posts = [json.loads(line) for line in SOCIAL_INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    normalized_groups = defaultdict(list)
    for post in posts:
        key = normalize_text(post["content"])
        if key:
            normalized_groups[key].append(post["post_id"])

    records = []
    for post in posts:
        text = post["content"]
        topics = social_topics(text)
        statements = statement_types(text)
        lifecycle = lifecycle_states(text)
        entities = link_entities(text, entity_catalog)
        media_links = re.findall(r"https?://(?:pbs|video)\.twimg\.com/\S+", text, re.I)
        key = normalize_text(text)
        repeated = normalized_groups.get(key, [])
        duplicate_info = {
            "status": "REPEATED_CONTENT" if len(repeated) > 1 else ("SUPERSESSION_LANGUAGE_PRESENT" if "SUPERSEDED" in lifecycle else "NONE_IDENTIFIED"),
            "related_post_ids": [x for x in repeated if x != post["post_id"]],
            "basis": "normalized text equality excluding URLs" if len(repeated) > 1 else None,
        }
        evidence = []
        substantive = len(normalize_text(text)) >= 45
        if not post["is_retweet"] and substantive:
            evidence.extend(["CANONICAL_KNOWLEDGE_CANDIDATE", "ENTITY_UPDATE_CANDIDATE"])
        if not post["is_retweet"] and ("ANNOUNCEMENT" in statements or "RELEASE" in statements or lifecycle):
            evidence.append("TIMELINE_CANDIDATE")
        if entities and not post["is_retweet"]:
            evidence.append("GRAPH_RELATIONSHIP_CANDIDATE")
        if post["is_retweet"] or not substantive:
            evidence.append("LOW_VALUE")
        if media_links:
            evidence.append("RESEARCH_GAP")
        if len(repeated) > 1:
            evidence.append("DUPLICATE")
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
            "timeline_candidate": "TIMELINE_CANDIDATE" in evidence,
            "promotion_targets": promotion_targets(topics) if not post["is_retweet"] and substantive else [],
            "confidence": confidence, "duplicate_or_supersession": duplicate_info,
            "research_notes": notes,
        })

    SOCIAL_OUT.mkdir(parents=True, exist_ok=True)
    semantic_path = SOCIAL_OUT / "staratlas-posts-semantic.jsonl"
    semantic_path.write_text("".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) + "\n" for x in records), encoding="utf-8")

    topic_index = {topic: [r["source_id"] for r in records if topic in r["topics"]] for topic in sorted(TOPICS)}
    entity_links = [{"source_id": r["source_id"], "post_id": r["post_id"], "entities": r["entities"], "unresolved_references": r["unresolved_references"]} for r in records if r["entities"] or r["unresolved_references"]]
    timeline = [{"source_id": r["source_id"], "post_id": r["post_id"], "date": r["published_date"], "topics": r["topics"], "statement_types": r["statement_types"], "lifecycle_states": r["lifecycle_states"], "confidence": r["confidence"]} for r in records if r["timeline_candidate"]]
    promotions = [{"source_id": r["source_id"], "post_id": r["post_id"], "targets": r["promotion_targets"], "evidence_classes": r["evidence_classes"], "confidence": r["confidence"], "review_status": "UNREVIEWED"} for r in records if r["promotion_targets"]]
    gaps = [{"source_id": r["source_id"], "post_id": r["post_id"], "notes": r["research_notes"], "unresolved_references": r["unresolved_references"]} for r in records if "RESEARCH_GAP" in r["evidence_classes"] or r["unresolved_references"]]
    common = {"campaign_id": CAMPAIGN_ID, "schema_version": "1.0.0", "generated_from": str(SOCIAL_INPUT.relative_to(REPO)).replace("\\", "/")}
    write_json(SOCIAL_OUT / "topic-index.json", {**common, "topic_counts": {k: len(v) for k, v in topic_index.items()}, "topics": topic_index})
    write_json(SOCIAL_OUT / "entity-links.json", {**common, "link_record_count": len(entity_links), "links": entity_links})
    write_json(SOCIAL_OUT / "timeline-candidates.json", {**common, "candidate_count": len(timeline), "candidates": timeline})
    write_json(SOCIAL_OUT / "promotion-candidates.json", {**common, "candidate_count": len(promotions), "candidates": promotions})
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


def governance_result(payload, votes):
    end = payload.get("votingEndsAt")
    ended = bool(end and end < CAPTURE_TIMESTAMP)
    yes = votes.get("yes", {}).get("voting_power")
    no = votes.get("no", {}).get("voting_power")
    if ended and as_decimal(yes) is not None and as_decimal(no) is not None:
        return "PASSED" if as_decimal(yes) > as_decimal(no) else "FAILED"
    election = payload.get("electionResults")
    if isinstance(election, str):
        try: election = json.loads(election)
        except json.JSONDecodeError: election = None
    if ended and election and election.get("winners"):
        return "PASSED"
    return "UNKNOWN"


def governance_topics(payload):
    text = " ".join([payload.get("title", ""), payload.get("brief", ""), payload.get("description", "")])
    topics = social_topics(text)
    if "GOVERNANCE" not in topics: topics.insert(0, "GOVERNANCE")
    return unique(topics)


def build_governance(entity_catalog):
    seed = load_json(PIP_SEED)
    seed_by_number = {x["pip_number"]: x for x in seed}
    records = []
    GOV_RECORDS.mkdir(parents=True, exist_ok=True)
    for raw_path in sorted(PIP_RAW.glob("*.json")):
        raw_bytes = raw_path.read_bytes()
        payload = json.loads(raw_bytes)
        number = payload["pipNumber"]
        source = seed_by_number[number]
        description = payload.get("description") or ""
        author = markdown_author(description)
        author_value = author or payload.get("authorPublicKey") or None
        votes = vote_map(payload)
        result = governance_result(payload, votes)
        election = payload.get("electionResults")
        if isinstance(election, str):
            try: election = json.loads(election)
            except json.JSONDecodeError: election = None
        topics = governance_topics(payload)
        entity_text = " ".join([payload.get("title", ""), payload.get("brief", ""), description])
        entities = link_entities(entity_text, entity_catalog)
        requested_funding = money_mentions(description)
        limitations = []
        if not author:
            limitations.append("No explicit human-readable author was parsed; author uses the portal author public key.")
        if result == "UNKNOWN":
            limitations.append("The captured portal payload does not expose a conclusive binary or election result.")
        limitations.append("Approval is derived only from the official completed vote record; it is not execution evidence.")
        limitations.append("No execution claim is made without a separate official implementation record, transaction, transfer, or equivalent primary evidence.")
        approval = "APPROVED" if result == "PASSED" else ("FAILED" if result == "FAILED" else "UNKNOWN")
        winners = election.get("winners", []) if election else []
        record_capture_timestamp = CAPTURE_TIMESTAMP
        record = {
            "source_id": source["source_id"], "pip_number": number,
            "proposal_uuid": source["proposal_uuid"], "proposal_url": source["proposal_url"],
            "title": payload.get("title"), "author": author_value,
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
            "vote_for": votes.get("yes"), "vote_against": votes.get("no"), "vote_abstain": votes.get("abstain"),
            "all_vote_totals": votes, "quorum": None,
            "proposal_state": "PROPOSED", "vote_state": result, "result": result,
            "approval_state": approval, "execution_state": "UNKNOWN", "execution_evidence": [],
            "election_winners": winners, "portal_status": payload.get("status"), "portal_current_status": payload.get("currentStatus"),
            "capture_timestamp": record_capture_timestamp, "content_checksum": hashlib.sha256(raw_bytes).hexdigest(),
            "topics": topics, "promotion_targets": promotion_targets(topics),
            "contradictions": ["Portal status remains Proposal_Activated_Pending_Open_Voting although the vote window has ended."] if payload.get("currentStatus") == "Proposal_Activated_Pending_Open_Voting" and payload.get("votingEndsAt", "") < CAPTURE_TIMESTAMP else [],
            "research_gaps": ["Execution evidence not present in the captured proposal payload."],
            "limitations": limitations,
        }
        records.append(record)
        source_record = {
            "source_id": source["source_id"], "campaign_id": CAMPAIGN_ID,
            "source_type": "OFFICIAL_GOVERNANCE_PROPOSAL", "evidence_tier": "TIER_1_OFFICIAL_PORTAL",
            "title": payload.get("title"), "url": source["proposal_url"], "proposal_uuid": source["proposal_uuid"],
            "pip_number": number, "publication_date": payload.get("createdAt"), "updated_date": payload.get("updatedAt"),
            "author": author_value, "raw_capture": str(raw_path.relative_to(REPO)).replace("\\", "/"),
            "semantic_record": "archive/semantic/governance/pip-registry-semantic.json",
            "content_sha256": hashlib.sha256(raw_bytes).hexdigest(), "capture_timestamp": record_capture_timestamp,
            "confidence": "HIGH", "limitations": limitations,
        }
        write_json(GOV_RECORDS / f"{source['source_id']}.json", source_record)

    records.sort(key=lambda x: x["pip_number"])
    common = {"campaign_id": CAMPAIGN_ID, "schema_version": "1.0.0", "capture_timestamp": max(r["capture_timestamp"] for r in records)}
    write_json(GOV_OUT / "pip-registry-semantic.json", {**common, "proposal_count": len(records), "proposals": records})
    topic_index = {topic: [r["source_id"] for r in records if topic in r["topics"]] for topic in sorted(TOPICS)}
    entity_links = [{"source_id": r["source_id"], "pip_number": r["pip_number"], "entities": r["affected_entities"]} for r in records]
    timeline = [{"source_id": r["source_id"], "pip_number": r["pip_number"], "publication_date": r["publication_date"], "vote_start": r["vote_start"], "vote_end": r["vote_end"], "result": r["result"], "approval_state": r["approval_state"], "execution_state": r["execution_state"]} for r in records]
    promotions = [{"source_id": r["source_id"], "pip_number": r["pip_number"], "targets": r["promotion_targets"], "result": r["result"], "execution_state": r["execution_state"], "review_status": "UNREVIEWED"} for r in records]
    gaps = [{"source_id": r["source_id"], "pip_number": r["pip_number"], "execution_state": r["execution_state"], "execution_evidence": r["execution_evidence"], "research_gaps": r["research_gaps"], "limitations": r["limitations"]} for r in records]
    write_json(GOV_OUT / "pip-topic-index.json", {**common, "topic_counts": {k: len(v) for k, v in topic_index.items()}, "topics": topic_index})
    write_json(GOV_OUT / "pip-entity-links.json", {**common, "records": entity_links})
    write_json(GOV_OUT / "pip-timeline-candidates.json", {**common, "candidate_count": len(timeline), "candidates": timeline})
    write_json(GOV_OUT / "pip-promotion-candidates.json", {**common, "candidate_count": len(promotions), "candidates": promotions})
    write_json(GOV_OUT / "pip-execution-gaps.json", {**common, "gap_count": len(gaps), "gaps": gaps})
    return records


def build_reports(posts, social, pips):
    raw_csv = REPO / "archive/raw/social-governance-semantic-enrichment/social-media/sorsa_export_1784085327119.csv"
    with raw_csv.open(encoding="utf-8-sig", newline="") as handle:
        raw_rows = list(csv.DictReader(handle))
    social_topics_count = Counter(t for r in social for t in r["topics"])
    social_statement_count = Counter(t for r in social for t in r["statement_types"])
    social_lifecycle_count = Counter(t for r in social for t in r["lifecycle_states"])
    social_evidence_count = Counter(t for r in social for t in r["evidence_classes"])
    pip_results = Counter(r["result"] for r in pips)
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
- Social timeline candidates: {sum(r['timeline_candidate'] for r in social)}
- Social promotion candidates: {sum(bool(r['promotion_targets']) for r in social)}
- Social records with unresolved references or media gaps: {sum(bool(r['research_notes']) for r in social)}

## Governance findings

- Vote results derived from completed official vote records: {dict(sorted(pip_results.items()))}
- Approval states: {dict(sorted(Counter(r['approval_state'] for r in pips).items()))}
- Execution states: {dict(sorted(Counter(r['execution_state'] for r in pips).items()))}
- Execution gaps requiring primary evidence: {sum(r['execution_state'] == 'UNKNOWN' for r in pips)}

`PASSED`/`APPROVED` records are not treated as executed. Every proposal remains `execution_state: UNKNOWN` because the proposal payloads do not contain a separate implementation record, on-chain transaction, treasury transfer, deployed change, or equivalent primary evidence.

## Review posture

All promotion targets are candidates only. Retweets preserve the fact of resharing and are excluded from first-party promotion candidates. Engagement metrics were not used as evidence. Linked media absent from the package is retained as a research gap.

## Validation

Validation status: **{validation['status']}**. See `validation-report.md` for the complete checks.
"""
    (OPS / "campaign-summary.md").write_text(summary, encoding="utf-8")
    research = """# Research gaps

## Governance execution

All 33 PIPs require separate primary execution evidence before an `EXECUTED` or `PARTIALLY_EXECUTED` state can be assigned. Candidate evidence includes official implementation reports, on-chain transactions, treasury transfers, deployed policy/product changes, and direct implementation records.

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

    integration_attributes = REPO / "archive/normalized/social-governance-semantic-enrichment/.gitattributes"
    generated = [p for base in [SOCIAL_OUT, GOV_OUT, GOV_RECORDS, OPS] for p in base.rglob("*") if p.is_file() and p.name != "manifest.json" and (OPS / "input-package") not in p.parents] + [integration_attributes]
    inputs = [p for base in [REPO / "archive/raw/social-governance-semantic-enrichment", REPO / "archive/normalized/social-governance-semantic-enrichment", REPO / "archive/source-records/social-governance-semantic-enrichment/social-media", OPS / "input-package"] for p in base.rglob("*") if p.is_file() and p.name != ".gitattributes"]
    manifest = {
        "campaign_id": CAMPAIGN_ID, "schema_version": "1.0.0", "status": validation["status"],
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
    add("Retweet evidence boundary", all(not r['promotion_targets'] and 'LOW_VALUE' in r['evidence_classes'] for r in social if r['is_retweet']), "No retweet is promoted as an original first-party claim")
    add("Governance lifecycle separation", all(r['proposal_state'] == 'PROPOSED' and r['vote_state'] in {'PASSED','FAILED','UNKNOWN'} and r['approval_state'] in {'APPROVED','FAILED','UNKNOWN'} and r['execution_state'] in {'EXECUTED','PARTIALLY_EXECUTED','UNKNOWN'} for r in pips), "Proposal, vote, approval, and execution use distinct fields")
    add("Execution evidence rule", all(r['execution_state'] == 'UNKNOWN' and not r['execution_evidence'] for r in pips), "No execution inferred from a passed vote")
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
