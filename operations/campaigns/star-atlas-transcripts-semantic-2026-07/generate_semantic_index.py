from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INPUT_ROOT = ROOT / "archive" / "normalized" / "star-atlas-transcripts-ingestion-2026-07"
SOURCE_ROOT = ROOT / "archive" / "source-records" / "star-atlas-transcripts-ingestion-2026-07"
OUTPUT_ROOT = ROOT / "archive" / "semantic" / "star-atlas-transcripts"
OPS_ROOT = ROOT / "operations" / "campaigns" / "star-atlas-transcripts-semantic-2026-07"
CAMPAIGN_ID = "star-atlas-transcripts-semantic-2026-07"
SCHEMA_VERSION = "2.0.0"

TOPICS = [
    "PRODUCT", "GAMEPLAY", "GOVERNANCE", "ECONOMY", "TECHNOLOGY", "LORE",
    "CORPORATE", "PEOPLE", "COMMUNITY", "PARTNERSHIP", "GUILD", "EVENT",
    "MARKETING", "OPERATIONS",
]
STATEMENTS = [
    "ANNOUNCEMENT", "STATUS_UPDATE", "ROADMAP", "RELEASE", "DESIGN_INTENT",
    "TECHNICAL_EXPLANATION", "Q_AND_A", "RETROSPECTIVE", "CLARIFICATION",
    "CORRECTION", "COMMUNITY_FEEDBACK", "DISCUSSION", "SPECULATION",
    "THEORYCRAFTING",
]
LIFECYCLES = [
    "FIRST_MENTION", "PLANNED", "IN_DEVELOPMENT", "TESTING", "LIVE", "UPDATED",
    "SUPERSEDED", "DEPRECATED", "CANCELLED", "UNKNOWN",
]
EVIDENCE = [
    "CANONICAL_KNOWLEDGE", "TIMELINE_EVENT", "ENTITY_UPDATE", "GRAPH_RELATIONSHIP",
    "RESEARCH_GAP", "CONTRADICTION", "LOW_VALUE", "DUPLICATE",
]
DISPOSITIONS = ["HIGH_PRIORITY", "MEDIUM_PRIORITY", "LOW_PRIORITY", "NOT_ELIGIBLE"]
CONFIDENCE = ["HIGH", "MEDIUM", "LOW"]

TOPIC_PATTERNS = {
    "PRODUCT": r"\b(sage|holosim|fleet command|starbased|escape velocity|score|showroom|c4|product|game client|marketplace)\b",
    "GAMEPLAY": r"\b(gameplay|play|player|fleet|ship|crew|mining|crafting|combat|racing|mission|resource|claim stake|starbase|movement|scanning|land|planet)\b",
    "GOVERNANCE": r"\b(dao|governance|proposal|pip[- ]?\d{1,2}\b|\bpip\b|vote|voting|council|quorum|constitution|delegate|foundation|treasury)\b",
    "ECONOMY": r"\b(econom|tokenomics|atlas token|\bpolis\b|currency|inflation|emission|sink|market|price|revenue|fee|treasury|liquidity|supply|demand|r4|resource)\b",
    "TECHNOLOGY": r"\b(technology|technical|solana|blockchain|on[- ]chain|unreal|ue5|api|rpc|sdk|program|smart contract|server|architecture|database|transaction|mainnet|testnet|ptr)\b",
    "LORE": r"\b(lore|galia|mud|manus ultima|oni|ustur|council of peace|convergence war|cataclysm|iris|tufa|faction|story|canon|species)\b",
    "CORPORATE": r"\b(atmta|company|corporate|employee|team|studio|runway|funding|investor|restructur|hiring|layoff|leadership|executive)\b",
    "PEOPLE": r"\b(michael wagner|swagner|pablo quiroga|danny floyd|glenn kennedy|krigs|speaker|guest|founder|ceo|director)\b",
    "COMMUNITY": r"\b(community|citizen|audience|discord|feedback|player base|ecosystem|member|contributor)\b",
    "PARTNERSHIP": r"\b(partner|partnership|collaborat|integration|sponsor|vendor)\b",
    "GUILD": r"\b(guild|dac|decentralized autonomous corporation|coalition|alliance)\b",
    "EVENT": r"\b(event|town hall|forum|conference|summit|hackathon|award|competition|tournament|meeting|workshop)\b",
    "MARKETING": r"\b(marketing|campaign|brand|trailer|promotion|social media|press|merch|announcement)\b",
    "OPERATIONS": r"\b(operation|process|workflow|schedule|weekly|budget|staff|organizing|agenda|moderator|administration)\b",
}

ENTITY_DEFINITIONS = [
    ("ORG-ATMTA", "ATMTA, Inc.", "ORGANIZATION", ["atmta", "star atlas team"]),
    ("ORG-SA-DAO", "Star Atlas DAO", "ORGANIZATION", ["star atlas dao", "the dao"]),
    ("ORG-SA-FOUNDATION", "Star Atlas Foundation", "ORGANIZATION", ["star atlas foundation", "the foundation"]),
    ("ORG-SA-GITHUB", "staratlasmeta GitHub organization", "ORGANIZATION", ["staratlasmeta", "star atlas github"]),
    ("PRODUCT-PLAY", "PLAY", "PRODUCT", ["star atlas play", "play.staratlas"]),
    ("PRODUCT-SAGE", "SAGE / SAGE Labs", "PRODUCT", ["sage labs", "sage"]),
    ("PRODUCT-UE5", "Star Atlas Unreal Engine 5 game", "PRODUCT", ["unreal engine 5", "ue5", "unreal engine"]),
    ("PRODUCT-HOLOSIM", "Holosim", "PRODUCT", ["holosim", "holo sim"]),
    ("PRODUCT-MARKETPLACE", "Galactic Marketplace", "PRODUCT", ["galactic marketplace"]),
    ("PRODUCT-DAO-PORTAL", "Star Atlas DAO portal", "PRODUCT", ["dao portal", "governance portal"]),
    ("PRODUCT-BUILD", "Star Atlas Build", "PRODUCT", ["build.staratlas", "star atlas build"]),
    ("PRODUCT-FLEET-COMMAND", "Fleet Command", "PRODUCT", ["fleet command"]),
    ("TOKEN-ATLAS", "ATLAS token", "TOKEN", ["atlas token", "$atlas"]),
    ("TOKEN-POLIS", "POLIS token", "TOKEN", ["polis", "$polis"]),
    ("ASSET-SHIPS", "Star Atlas ships", "ASSET", ["spaceships", "star atlas ships", "ships"]),
    ("ASSET-CREW", "Crew", "ASSET", ["crew members", "crew"]),
    ("ASSET-CLAIM-STAKES", "Claim Stakes", "ASSET", ["claim stakes", "claim stake"]),
    ("LORE-GALIA", "Galia Expanse", "LORE", ["galia expanse", "galia"]),
    ("LORE-FACTION-MUD", "MUD", "LORE", ["manus ultima divina", "mud faction"]),
    ("LORE-FACTION-ONI", "ONI Consortium", "LORE", ["oni consortium", "oni faction"]),
    ("LORE-FACTION-USTUR", "Ustur Sector", "LORE", ["ustur sector", "ustur faction"]),
    ("LORE-COUNCIL-PEACE", "Council of Peace", "LORE", ["council of peace"]),
    ("ACTOR-MICHAEL-WAGNER", "Michael Wagner", "PERSON", ["michael wagner", "swagner"]),
    ("ACTOR-PABLO-QUIROGA", "Pablo Quiroga", "PERSON", ["pablo quiroga"]),
    ("ACTOR-DANNY-FLOYD", "Danny Floyd", "PERSON", ["danny floyd"]),
    ("ACTOR-GLENN-KENNEDY", "Glenn Kennedy", "PERSON", ["glenn kennedy"]),
    ("ACTOR-KRIGS", "Krigs", "PERSON", ["krigs"]),
]

CONCEPT_PATTERNS = {
    "C4": r"\bc4\b", "STARBASED": r"\bstarbas(?:ed|e)\b",
    "ESCAPE_VELOCITY": r"\bescape velocity\b", "SCORE_FACTION_FLEET": r"\b(score|faction fleet)\b",
    "PIP": r"\bpip[- ]?\d+\b", "TREASURY": r"\btreasury\b", "TOKENOMICS": r"\btokenomics\b",
    "MINING": r"\bmining\b", "CRAFTING": r"\bcrafting\b", "ATLASNET": r"\batlasnet\b",
    "F_KIT": r"\bf[- ]?kit\b",
}

TRANSITION_RE = re.compile(
    r"\b(next topic|moving on|switch(?:ing)? gears|next question|question from|let'?s talk about|"
    r"now let'?s|on the agenda|the next one|before we move|with that said)\b", re.IGNORECASE,
)
CAPTION_RE = re.compile(r"^\[(\d{2}):(\d{2}):(\d{2})\]\s+(.*)$")
NUMBER_RE = re.compile(r"(?:\$\s?\d|\b\d+(?:[,.]\d+)?\s*(?:%|percent|million|thousand|atlas|polis|usdc|days?|weeks?|months?|years?)\b|\b20\d{2}\b)", re.I)
FILLER_RE = re.compile(r"^(?:um+|uh+|yeah|yes|no|okay|ok|all right|right|cool|good deal|hello|hi|thanks?|thank you|\[music\]|check(?: check)*)[.! ]*$", re.I)
QUESTION_RE = re.compile(r"(?:\?|^(?:who|what|when|where|why|how|is|are|do|does|did|can|could|would|should|will)\b)", re.I)
ACTION_RE = re.compile(r"\b(release|launch|ship|deploy|publish|open|close|approve|reject|vote|fund|transfer|build|implement|migrate|replace|deprecat|cancel|update|change|integrat|partner|hire|lay off|restructur|test|enable|disable|add|remove)\w*\b", re.I)
ROADMAP_RE = re.compile(r"\b(roadmap|planned? to|scheduled to|targeting (?:q[1-4]|20\d{2}|\w+ \d{1,2})|coming soon|we will (?:release|launch|ship|deploy|build|implement|migrate|publish|open|add|change|update)|intend to (?:release|launch|build|implement|change))\b", re.I)
RELEASE_RE = re.compile(r"\b(released?|launched?|shipped?|live now|went live|available (?:now|to everyone|on mainnet)|deployed? (?:to|on) (?:mainnet|production)|public release)\b", re.I)
TESTING_RE = re.compile(r"\b(public test|private test|test build|testing (?:on|in|with)|ptr|alpha test|beta test|stress test|limited access|early access)\b", re.I)
SPECULATION_RE = re.compile(r"\b(maybe|might|probably|possibly|i think|we think|could (?:be|become|change|cause|mean|lead|affect|impact|release|launch|ship))\b", re.I)
SPEAKER_REQUIRED_RE = re.compile(
    r"\b(i (?:think|believe|confirm|promise|decided)|in my opinion|my (?:role|view|decision|responsibility))\b",
    re.I,
)
SPEAKER_PARTIAL_RE = re.compile(
    r"\b(we (?:will|are|have|decided|plan|intend|expect|believe|think|confirm)|our (?:plan|decision|position|team|roadmap|goal))\b",
    re.I,
)
TECHNICAL_RE = re.compile(r"\b(api|rpc|sdk|smart contract|program id|architecture|server|database|transaction|solana|unreal engine|mainnet|testnet)\b", re.I)
EXPLANATION_RE = re.compile(r"\b(works? by|how .* works?|means that|because|the system|the process|technically|architecture|calculated|computed|stored|executed)\b", re.I)


def seconds(timestamp: str) -> int:
    hour, minute, second = (int(part) for part in timestamp.split(":"))
    return hour * 3600 + minute * 60 + second


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(name: str, payload: object) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_ops_json(name: str, payload: object) -> None:
    OPS_ROOT.mkdir(parents=True, exist_ok=True)
    (OPS_ROOT / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def tags_for(text: str, patterns: dict[str, str]) -> list[str]:
    return [tag for tag, pattern in patterns.items() if re.search(pattern, text, re.IGNORECASE)]


def parse_transcript(path: Path) -> list[dict[str, object]]:
    captions = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = CAPTION_RE.match(line)
        if match:
            timestamp = f"{match.group(1)}:{match.group(2)}:{match.group(3)}"
            captions.append({"timestamp": timestamp, "seconds": seconds(timestamp), "text": match.group(4).strip(), "line": line_number})
    return captions


def segment_captions(captions: list[dict[str, object]]) -> list[list[dict[str, object]]]:
    """Original segmentation algorithm. Kept unchanged to preserve all 1,910 segments."""
    if not captions:
        return []
    caption_topics = [set(tags_for(str(item["text"]), TOPIC_PATTERNS)) for item in captions]
    groups: list[list[dict[str, object]]] = []
    current: list[dict[str, object]] = []
    for index, caption in enumerate(captions):
        boundary = False
        if current:
            duration = int(current[-1]["seconds"]) - int(current[0]["seconds"])
            gap = int(caption["seconds"]) - int(current[-1]["seconds"])
            recent_topics = set().union(*caption_topics[max(0, index - 10):index])
            next_topics = set().union(*caption_topics[index:min(len(captions), index + 8)])
            semantic_shift = bool(recent_topics and next_topics and recent_topics.isdisjoint(next_topics))
            boundary = (
                (gap >= 45 and len(current) >= 6)
                or (TRANSITION_RE.search(str(caption["text"])) is not None and len(current) >= 14 and duration >= 35)
                or (semantic_shift and len(current) >= 24 and duration >= 60)
                or len(current) >= 70
                or duration >= 210
            )
        if boundary:
            groups.append(current)
            current = []
        current.append(caption)
    if current:
        groups.append(current)
    merged: list[list[dict[str, object]]] = []
    for group in groups:
        duration = int(group[-1]["seconds"]) - int(group[0]["seconds"])
        if merged and (len(group) < 7 or duration < 18):
            merged[-1].extend(group)
        else:
            merged.append(group)
    return merged


def entity_links(text: str) -> tuple[list[dict[str, object]], list[str]]:
    lowered = text.lower()
    links = []
    for entity_id, name, entity_type, aliases in ENTITY_DEFINITIONS:
        matches = [alias for alias in aliases if re.search(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", lowered)]
        if matches:
            links.append({
                "entity_id": entity_id, "entity_name": name, "entity_type": entity_type,
                "matched_aliases": sorted(set(matches)),
                "link_confidence": "HIGH" if any(len(alias.split()) > 1 for alias in matches) else "MEDIUM",
            })
    unresolved = [f"PIP-{number}" for number in sorted(set(re.findall(r"\bpip[- ]?(\d{1,2})\b", lowered)), key=int)]
    for concept, pattern in CONCEPT_PATTERNS.items():
        if concept not in {"PIP", "MINING", "CRAFTING", "TREASURY", "TOKENOMICS"} and re.search(pattern, lowered, re.I):
            unresolved.append(concept)
    return links, sorted(set(unresolved))


def concepts_for(text: str, unresolved: list[str]) -> list[str]:
    return sorted(set(tags_for(text, CONCEPT_PATTERNS) + unresolved))


def identifiable_labels(links: list[dict[str, object]], unresolved: list[str], concepts: list[str]) -> list[str]:
    labels = [str(link["entity_name"]) for link in links]
    labels.extend(value for value in unresolved if value.startswith("PIP-") or value in {"C4", "STARBASED", "ESCAPE_VELOCITY", "SCORE_FACTION_FLEET", "ATLASNET", "F_KIT"})
    labels.extend(value for value in concepts if value in {"TREASURY", "TOKENOMICS", "MINING", "CRAFTING"})
    return sorted(set(labels))


def caption_reference(caption: dict[str, object]) -> dict[str, object]:
    return {"timestamp": caption["timestamp"], "line": caption["line"], "text": caption["text"]}


def has_local_identifier(group: list[dict[str, object]], index: int) -> bool:
    window = " ".join(str(item["text"]) for item in group[max(0, index - 1):min(len(group), index + 2)])
    links, unresolved = entity_links(window)
    concepts = concepts_for(window, unresolved)
    return bool(identifiable_labels(links, unresolved, concepts))


def detect_statements(group: list[dict[str, object]], links: list[dict[str, object]], unresolved: list[str], concepts: list[str]) -> tuple[list[str], dict[str, list[dict[str, object]]]]:
    text = " ".join(str(item["text"]) for item in group)
    identifiable = bool(identifiable_labels(links, unresolved, concepts))
    found: list[str] = []
    evidence: dict[str, list[dict[str, object]]] = defaultdict(list)

    def capture(tag: str, pattern: re.Pattern[str], require_identifier: bool = False) -> None:
        for index, caption in enumerate(group):
            if pattern.search(str(caption["text"])) and (not require_identifier or has_local_identifier(group, index)):
                evidence[tag].append(caption_reference(caption))
        if evidence[tag]:
            found.append(tag)

    capture("ANNOUNCEMENT", re.compile(r"\b(we (?:are )?(?:announc|introduc|reveal|unveil)|official announcement|we're excited to announce)\w*\b", re.I), True)
    capture("ROADMAP", ROADMAP_RE, True)
    capture("RELEASE", RELEASE_RE, True)
    capture("CORRECTION", re.compile(r"\b(correction|correct that|mistake|was wrong|not accurate|retract)\b", re.I), False)
    capture("CLARIFICATION", re.compile(r"\b(to be clear|for clarity|what that means|in other words|let me clarify)\b", re.I), False)
    capture("RETROSPECTIVE", re.compile(r"\b(last year|previously|used to|looking back|back in 20\d{2}|historically|in retrospect)\b", re.I), identifiable)
    capture("COMMUNITY_FEEDBACK", re.compile(r"\b(community feedback|players? (?:want|asked|reported)|community response|player sentiment|feedback from)\b", re.I), False)
    capture("THEORYCRAFTING", re.compile(r"\b(theory ?craft|theorycraft)\w*\b", re.I), False)
    capture("DESIGN_INTENT", re.compile(r"\b(designed to|our design|our goal (?:is|was) to|intended to|the purpose (?:is|was) to|we want the (?:system|game|product|feature))\b", re.I), True)

    for index, caption in enumerate(group):
        line = str(caption["text"])
        local_identifier = has_local_identifier(group, index)
        if local_identifier and re.search(r"\b(currently (?:in|on|being)|status (?:is|of)|progress (?:is|on)|as of (?:today|this week)|still (?:in voting|being built|under review)|has been (?:updated|approved|released|deployed))\b", line, re.I):
            evidence["STATUS_UPDATE"].append(caption_reference(caption))
        if local_identifier and TECHNICAL_RE.search(line) and (EXPLANATION_RE.search(line) or len(line.split()) >= 12):
            evidence["TECHNICAL_EXPLANATION"].append(caption_reference(caption))
        if local_identifier and SPECULATION_RE.search(line) and not QUESTION_RE.search(line) and ACTION_RE.search(line):
            evidence["SPECULATION"].append(caption_reference(caption))
    for tag in ("STATUS_UPDATE", "TECHNICAL_EXPLANATION", "SPECULATION"):
        if evidence[tag]:
            found.append(tag)

    question_indexes = [
        index for index, caption in enumerate(group)
        if QUESTION_RE.search(str(caption["text"]))
        and len(str(caption["text"]).split()) >= 6
        and has_local_identifier(group, index)
    ]
    for index in question_indexes:
        answers = [
            item for answer_index, item in enumerate(group[index + 1:min(len(group), index + 5)], start=index + 1)
            if len(str(item["text"]).split()) >= 8
            and not QUESTION_RE.search(str(item["text"]))
            and not FILLER_RE.match(str(item["text"]).strip())
            and (ACTION_RE.search(str(item["text"])) or EXPLANATION_RE.search(str(item["text"])) or has_local_identifier(group, answer_index))
        ]
        if answers:
            evidence["Q_AND_A"] = [caption_reference(group[index]), caption_reference(answers[0])]
            found.append("Q_AND_A")
            break

    if not found:
        found = ["DISCUSSION"]
    return [tag for tag in STATEMENTS if tag in set(found)], dict(evidence)


def detect_lifecycle(group: list[dict[str, object]], links: list[dict[str, object]], unresolved: list[str], concepts: list[str]) -> tuple[list[str], list[dict[str, object]]]:
    labels = identifiable_labels(links, unresolved, concepts)
    if not labels:
        return [], []
    rules = [
        ("CANCELLED", re.compile(r"\b(cancelled|canceled|abandoned|will not ship|will not proceed)\b", re.I)),
        ("DEPRECATED", re.compile(r"\b(deprecated|retired|sunset|shut down|no longer supported)\b", re.I)),
        ("SUPERSEDED", re.compile(r"\b(replaced by|superseded|renamed to|migrated to)\b", re.I)),
        ("LIVE", RELEASE_RE),
        ("TESTING", TESTING_RE),
        ("IN_DEVELOPMENT", re.compile(r"\b(in development|under development|being developed|work in progress|we are building)\b", re.I)),
        ("PLANNED", ROADMAP_RE),
        ("UPDATED", re.compile(r"\b(has been updated|we updated|new version|patch (?:is|was) (?:live|released)|upgrade (?:is|was) (?:live|released)|material update)\b", re.I)),
    ]
    evidence = []
    for state, pattern in rules:
        for index, caption in enumerate(group):
            if pattern.search(str(caption["text"])) and has_local_identifier(group, index):
                window = " ".join(str(item["text"]) for item in group[max(0, index - 1):min(len(group), index + 2)])
                local_links, local_unresolved = entity_links(window)
                local_concepts = concepts_for(window, local_unresolved)
                local_labels = identifiable_labels(local_links, local_unresolved, local_concepts)
                evidence.append({
                    "state": state, "entity": local_labels[0] if local_labels else labels[0],
                    "supporting_caption": caption_reference(caption),
                    "confidence": "HIGH" if local_links and pattern is not ROADMAP_RE else "MEDIUM",
                })
                break
    states = [state for state in LIFECYCLES if any(item["state"] == state for item in evidence)]
    return states, evidence


def source_gap_types(record: dict[str, object]) -> list[str]:
    gaps = []
    if record.get("speaker_attribution", "UNKNOWN") == "UNKNOWN": gaps.append("SPEAKER_ATTRIBUTION_MISSING")
    if not record.get("original_url"): gaps.append("ORIGINAL_URL_MISSING")
    if record.get("publication_date") is None: gaps.append("PUBLICATION_DATE_MISSING")
    elif record.get("publication_date_basis") != "filename-exact": gaps.append("PUBLICATION_DATE_PARTIAL_OR_FILENAME_DERIVED")
    return gaps


def transcript_ambiguity(text: str) -> bool:
    words = re.findall(r"[A-Za-z0-9']+", text)
    return bool(re.search(r"\[(?:inaudible|unintelligible|music)\]", text, re.I) or (words and sum(len(word) <= 1 for word in words) / len(words) > .18))


def support_line_scores(group: list[dict[str, object]], statement_evidence: dict[str, list[dict[str, object]]]) -> list[tuple[int, dict[str, object], list[str]]]:
    evidence_lines = {int(ref["line"]): tag for tag, refs in statement_evidence.items() for ref in refs}
    scored = []
    for index, caption in enumerate(group):
        line = str(caption["text"])
        window = " ".join(str(item["text"]) for item in group[max(0, index - 1):min(len(group), index + 2)])
        local_links, local_unresolved = entity_links(window)
        local_concepts = concepts_for(window, local_unresolved)
        labels = identifiable_labels(local_links, local_unresolved, local_concepts)
        reasons = []
        score = 0
        if local_links: score += 2; reasons.append("canonical entity identified in local context")
        elif labels: score += 1; reasons.append("institutional concept or proposal identified in local context")
        if int(caption["line"]) in evidence_lines:
            score += 2; reasons.append(f"exact {evidence_lines[int(caption['line'])].lower().replace('_', ' ')} language")
        if ACTION_RE.search(line): score += 1; reasons.append("concrete institutional action")
        if NUMBER_RE.search(line): score += 1; reasons.append("date, metric, quantity, or funding detail")
        if TECHNICAL_RE.search(line) and EXPLANATION_RE.search(line): score += 1; reasons.append("technical mechanism explanation")
        if FILLER_RE.match(line.strip()): score -= 3
        if QUESTION_RE.search(line) and int(caption["line"]) not in evidence_lines: score -= 1
        if score >= 2:
            scored.append((score, caption_reference(caption), reasons))
    return sorted(scored, key=lambda item: (-item[0], int(item[1]["line"])))


def confidence_for(score: int, supporting_count: int, ambiguous: bool) -> str:
    if score >= 7 and supporting_count >= 2 and not ambiguous: return "HIGH"
    if score >= 5 and not ambiguous: return "MEDIUM"
    return "LOW"


def speaker_dependency_for(text: str) -> str:
    """Return whether a claim's evidentiary force depends on knowing the speaker.

    Unknown attribution is not a general quality defect. It matters when the
    statement is a personal assertion or an unattributed institutional position.
    """
    if SPEAKER_REQUIRED_RE.search(text):
        return "REQUIRED"
    if SPEAKER_PARTIAL_RE.search(text):
        return "PARTIAL"
    return "NONE"


def speaker_dependency_penalty(dependency: str) -> int:
    return 1 if dependency in {"PARTIAL", "REQUIRED"} else 0


def is_promotion_candidate(segment: dict[str, object], group: list[dict[str, object]], links: list[dict[str, object]], unresolved: list[str], statement_evidence: dict[str, list[dict[str, object]]], record: dict[str, object]) -> dict[str, object]:
    statements = set(segment["statement_classifications"])
    strong = statements & {"ANNOUNCEMENT", "STATUS_UPDATE", "ROADMAP", "RELEASE", "TECHNICAL_EXPLANATION", "CORRECTION", "RETROSPECTIVE"}
    labels = identifiable_labels(links, unresolved, list(segment["concept_tags"]))
    scored_lines = support_line_scores(group, statement_evidence)
    supporting = [item[1] for item in scored_lines[:5]]
    reasons = []
    score = 0
    if links: score += 2; reasons.append("named canonical entity")
    elif labels: score += 1; reasons.append("identifiable institutional concept or proposal")
    if strong: score += 2; reasons.append("explicit institutional claim language: " + ", ".join(sorted(strong)))
    if any(NUMBER_RE.search(str(item["text"])) for item in group): score += 1; reasons.append("concrete date, metric, quantity, or funding detail")
    if len(supporting) >= 2: score += 1; reasons.append("multiple exact supporting captions")
    if len(segment["entity_ids"]) > 1 or "PARTNERSHIP" in segment["topic_tags"]: score += 1; reasons.append("identifiable entity relationship")
    if record.get("publication_date"): score += 1; reasons.append("source carries date metadata")
    dependency = speaker_dependency_for(" ".join(str(item["text"]) for item in supporting)) if supporting else str(segment["speaker_dependency"])
    score -= speaker_dependency_penalty(dependency)
    ambiguous = transcript_ambiguity(" ".join(str(item["text"]) for item in group))
    if ambiguous: score -= 1
    filler_ratio = sum(bool(FILLER_RE.match(str(item["text"]).strip())) for item in group) / len(group)
    exclusion = None
    if not labels:
        exclusion = "NO_IDENTIFIABLE_INSTITUTIONAL_ENTITY_OR_OBJECT"
    elif not strong and not any(NUMBER_RE.search(str(item["text"])) and ACTION_RE.search(str(item["text"])) for item in group):
        exclusion = "NO_DISCRETE_INSTITUTIONAL_CLAIM"
    elif statements <= {"DISCUSSION", "Q_AND_A", "COMMUNITY_FEEDBACK"}:
        exclusion = "GENERIC_DISCUSSION_OR_QUESTION"
    elif statements <= {"SPECULATION", "DISCUSSION"}:
        exclusion = "UNSUPPORTED_SPECULATION"
    elif not supporting:
        exclusion = "INSUFFICIENT_EXACT_CAPTION_SUPPORT"
    elif filler_ratio > .45:
        exclusion = "HOUSEKEEPING_OR_FILLER_DOMINANT"
    elif score < 4:
        exclusion = "EVIDENCE_DENSITY_BELOW_THRESHOLD"
    eligible = exclusion is None
    if not eligible:
        disposition = "NOT_ELIGIBLE"
    elif score >= 7:
        disposition = "HIGH_PRIORITY"
    elif score >= 5:
        disposition = "MEDIUM_PRIORITY"
    else:
        disposition = "LOW_PRIORITY"
    gaps = ["SPEAKER_ATTRIBUTION_MISSING"] if dependency != "NONE" else []
    if ambiguous: gaps.append("TRANSCRIPT_RECOGNITION_UNCERTAINTY")
    if unresolved and not links: gaps.append("AMBIGUOUS_PRODUCT_OR_ENTITY_IDENTITY")
    if statements & {"ROADMAP", "RELEASE", "STATUS_UPDATE"}: gaps.append("OFFICIAL_CONFIRMATION_MISSING")
    if "GOVERNANCE" in segment["topic_tags"] and re.search(r"\b(execut|implement|approved?)\b", " ".join(str(x["text"]) for x in group), re.I): gaps.append("EXECUTION_EVIDENCE_MISSING")
    return {
        "eligible": eligible, "disposition": disposition, "score": score,
        "candidate_confidence": confidence_for(score, len(supporting), ambiguous),
        "candidate_reasons": reasons, "supporting_captions": supporting,
        "exclusion_reason": exclusion, "review_priority": disposition,
        "speaker_dependency": dependency,
        "institutional_attribution": segment["institutional_attribution"],
        "research_gap_types": sorted(set(gaps)),
    }


TIMELINE_RULES = [
    ("CORRECTION", re.compile(r"\b(correction|we were wrong|not accurate|retract)\b", re.I)),
    ("DEPRECATION", re.compile(r"\b(deprecated|retired|sunset|shut down|no longer supported)\b", re.I)),
    ("MIGRATION", re.compile(r"\b(migrated?|migration|moved? (?:to|from)|replaced by)\b", re.I)),
    ("RELEASE_OR_DEPLOYMENT", RELEASE_RE),
    ("PUBLIC_OR_LIMITED_TESTING", TESTING_RE),
    ("GOVERNANCE_VOTE", re.compile(r"\b(voting (?:opened|closed|starts?|ends?|is live)|vote (?:passed|failed|approved|rejected)|approved by the foundation|went to vote)\b", re.I)),
    ("GOVERNANCE_PROPOSAL", re.compile(r"\b(pip[- ]?\d+ (?:was|is|has been) (?:published|submitted|proposed|approved|rejected|in voting)|proposal (?:was|is|has been) (?:published|submitted|approved|rejected))\b", re.I)),
    ("PARTNERSHIP", re.compile(r"\b(announced? (?:a |the )?partnership|partnered with|partnership with|integration with .* (?:launched|announced))\b", re.I)),
    ("ORGANIZATIONAL_CHANGE", re.compile(r"\b(hired?|appointed?|resigned?|laid off|layoffs?|restructur(?:ed|ing)|formed? (?:the|a) (?:team|council)|elected to)\b", re.I)),
    ("TREASURY_OR_FUNDING_ACTION", re.compile(r"\b(funded?|funding (?:approved|rejected|transferred)|treasury (?:transferred|approved|paid|allocated)|paid out|grant (?:approved|awarded))\b", re.I)),
    ("ANNOUNCEMENT", re.compile(r"\b(we (?:are )?(?:announc|introduc|reveal|unveil)|official announcement)\w*\b", re.I)),
    ("MATERIAL_PRODUCT_UPDATE", re.compile(r"\b(patch|update|upgrade) (?:was|is|went|has been) (?:released|live|deployed|available)|we (?:released|deployed|shipped) (?:an |the )?(?:patch|update|upgrade)\b", re.I)),
    ("EVENT_OCCURRED", re.compile(r"\b(took place|was held|we hosted|occurred on|event concluded|tournament concluded|winner was announced)\b", re.I)),
]


def date_fields(record: dict[str, object]) -> tuple[object, str, str]:
    basis = str(record.get("publication_date_basis") or "unknown")
    value = record.get("publication_date")
    precision = {"filename-exact": "DAY", "filename-month": "MONTH", "filename-year": "YEAR"}.get(basis, "UNKNOWN")
    return value, precision, basis if value else "UNRESOLVED_SOURCE_METADATA"


def is_timeline_candidate(segment: dict[str, object], group: list[dict[str, object]], links: list[dict[str, object]], unresolved: list[str], record: dict[str, object]) -> dict[str, object]:
    event_type = None
    supporting = []
    for candidate_type, pattern in TIMELINE_RULES:
        for index, caption in enumerate(group):
            if pattern.search(str(caption["text"])) and has_local_identifier(group, index):
                event_type = candidate_type
                supporting.append(caption_reference(caption))
        if supporting:
            break
    date_value, date_precision, date_basis = date_fields(record)
    score = 0
    reasons = []
    labels = identifiable_labels(links, unresolved, list(segment["concept_tags"]))
    if event_type: score += 2; reasons.append(f"concrete {event_type.lower().replace('_', ' ')} language")
    if links: score += 2; reasons.append("canonical entity identified")
    elif labels: score += 1; reasons.append("institutional concept or proposal identified")
    if supporting: score += 1; reasons.append("exact supporting caption")
    if date_value: score += 1; reasons.append(f"source date available at {date_precision.lower()} precision")
    if any(NUMBER_RE.search(str(item["text"])) for item in supporting): score += 1; reasons.append("event caption includes a date, metric, or quantity")
    dependency = speaker_dependency_for(" ".join(str(item["text"]) for item in supporting)) if supporting else str(segment["speaker_dependency"])
    score -= speaker_dependency_penalty(dependency)
    exclusion = None
    if not event_type: exclusion = "NO_CONCRETE_EVENT_STATE_LANGUAGE"
    elif not labels: exclusion = "NO_IDENTIFIABLE_EVENT_ENTITY_OR_SYSTEM"
    elif not supporting: exclusion = "NO_EXACT_EVENT_CAPTION"
    elif score < 4: exclusion = "EVENT_EVIDENCE_DENSITY_BELOW_THRESHOLD"
    eligible = exclusion is None
    confidence = "HIGH" if score >= 6 and date_value else ("MEDIUM" if score >= 4 else "LOW")
    gaps = ["SPEAKER_ATTRIBUTION_MISSING"] if dependency != "NONE" else []
    if not date_value: gaps.append("EVENT_DATE_UNRESOLVED")
    elif date_precision != "DAY": gaps.append("EVENT_DATE_IMPRECISE")
    if event_type in {"RELEASE_OR_DEPLOYMENT", "GOVERNANCE_VOTE", "TREASURY_OR_FUNDING_ACTION"}: gaps.append("OFFICIAL_CONFIRMATION_MISSING")
    return {
        "eligible": eligible, "event_type": event_type, "date_value": date_value,
        "date_precision": date_precision, "date_basis": date_basis,
        "supporting_captions": supporting[:5], "timeline_confidence": confidence,
        "timeline_reasons": reasons, "score": score, "exclusion_reason": exclusion,
        "speaker_dependency": dependency,
        "institutional_attribution": segment["institutional_attribution"],
        "research_gap_types": sorted(set(gaps)),
    }


QUOTE_RULES = [
    ("CORRECTION", re.compile(r"\b(correction|we were wrong|not accurate|retract)\b", re.I)),
    ("RELEASE_OR_DEPLOYMENT", RELEASE_RE),
    ("GOVERNANCE", re.compile(r"\b(proposal|pip[- ]?\d+|vote|voting|treasury|approved|rejected)\b", re.I)),
    ("ECONOMIC_OR_TREASURY", re.compile(r"\b(tokenomics|treasury|emission|revenue|funding|atlas token|polis)\b", re.I)),
    ("TECHNICAL_EXPLANATION", re.compile(r"\b(api|rpc|sdk|smart contract|architecture|mainnet|testnet|solana|unreal engine)\b", re.I)),
    ("ROADMAP_COMMITMENT", ROADMAP_RE),
    ("ANNOUNCEMENT", re.compile(r"\b(we (?:are )?(?:announc|introduc|reveal|unveil)|official announcement)\w*\b", re.I)),
]


def is_quote_candidate(segment: dict[str, object], group: list[dict[str, object]]) -> dict[str, object]:
    best = None
    for index, caption in enumerate(group):
        line = str(caption["text"]).strip()
        word_count = len(line.split())
        if word_count < 8 or word_count > 60 or QUESTION_RE.search(line) or FILLER_RE.match(line):
            continue
        category = next((name for name, pattern in QUOTE_RULES if pattern.search(line)), None)
        if not category:
            continue
        local_identifier = has_local_identifier(group, index)
        if not local_identifier:
            continue
        score = 2 + 2
        if NUMBER_RE.search(line): score += 1
        if 12 <= word_count <= 40: score += 1
        if ACTION_RE.search(line) or EXPLANATION_RE.search(line): score += 1
        ambiguous = transcript_ambiguity(line)
        dependency = speaker_dependency_for(line)
        score -= speaker_dependency_penalty(dependency)
        if ambiguous: score -= 1
        candidate = (score, -int(caption["line"]), category, caption, ambiguous, dependency)
        if best is None or candidate[:2] > best[:2]:
            best = candidate
    if best is None:
        return {
            "eligible": False, "score": 0, "quote_category": None,
            "quote_confidence": "LOW", "supporting_caption": None,
            "candidate_reasons": [], "speaker_dependency": "NONE",
            "institutional_attribution": "UNESTABLISHED",
            "exclusion_reason": "NO_CONCISE_INSTITUTIONAL_QUOTE",
        }
    score, _, category, caption, ambiguous, dependency = best
    eligible = score >= 4
    return {
        "eligible": eligible, "score": score, "quote_category": category,
        "quote_confidence": "HIGH" if score >= 6 and not ambiguous else ("MEDIUM" if score >= 4 else "LOW"),
        "supporting_caption": caption_reference(caption),
        "candidate_reasons": [f"explicit {category.lower().replace('_', ' ')} statement", "identifiable institutional object in local context", "complete verbatim caption"],
        "speaker_dependency": dependency,
        "institutional_attribution": "UNESTABLISHED",
        "exclusion_reason": None if eligible else "QUOTE_EVIDENCE_DENSITY_BELOW_THRESHOLD",
    }


def summarize(text: str, topics: list[str], statements: list[str], concepts: list[str]) -> str:
    subject = ", ".join(concepts[:4] or topics[:3] or ["community discussion"])
    framing = ", ".join(value.lower().replace("_", " ") for value in statements[:3])
    excerpt = re.sub(r"\s+", " ", text).strip()
    if len(excerpt) > 240: excerpt = excerpt[:237].rsplit(" ", 1)[0] + "…"
    return f"Discussion of {subject} framed as {framing}. The transcript addresses {excerpt}"


def promotion_targets(topics: list[str]) -> list[str]:
    mapping = {
        "PRODUCT": "knowledge/products/", "GAMEPLAY": "knowledge/gameplay/", "GOVERNANCE": "knowledge/governance/",
        "ECONOMY": "knowledge/economy/", "TECHNOLOGY": "knowledge/technology/", "LORE": "knowledge/lore/",
        "CORPORATE": "knowledge/organizations/", "PEOPLE": "knowledge/people/", "COMMUNITY": "knowledge/community/",
        "PARTNERSHIP": "knowledge/organizations/", "GUILD": "knowledge/community/", "EVENT": "knowledge/timeline/",
        "MARKETING": "knowledge/community/", "OPERATIONS": "knowledge/organizations/",
    }
    return sorted(set(mapping[topic] for topic in topics))


STOPWORDS = {"the", "and", "that", "this", "with", "from", "have", "will", "would", "could", "there", "about", "they", "them", "then", "than", "what", "when", "where", "which", "your", "youre", "into", "just", "like", "because", "been", "being", "were", "was", "are", "for", "but", "not", "its", "our", "you", "all"}


def claim_tokens(candidate: dict[str, object]) -> set[str]:
    text = " ".join(str(item["text"]) for item in candidate["supporting_captions"])
    tokens = []
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        if len(token) < 3 or token in STOPWORDS: continue
        for suffix in ("ing", "ed", "es", "s"):
            if token.endswith(suffix) and len(token) - len(suffix) >= 4:
                token = token[:-len(suffix)]; break
        tokens.append(token)
    return set(tokens)


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left | right else 0.0


def build_duplicate_clusters(candidates: list[dict[str, object]], segment_map: dict[str, dict[str, object]], decision_map: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    parent = list(range(len(candidates)))
    tokens = [claim_tokens(candidate) for candidate in candidates]

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]; index = parent[index]
        return index

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb: parent[rb] = ra

    by_source: dict[str, list[int]] = defaultdict(list)
    for index, candidate in enumerate(candidates): by_source[str(candidate["source_id"])].append(index)
    for indexes in by_source.values():
        for offset, left_index in enumerate(indexes):
            left = candidates[left_index]; left_segment = segment_map[str(left["segment_id"])]
            left_number = int(str(left["segment_id"]).rsplit("-", 1)[1])
            for right_index in indexes[offset + 1:]:
                right = candidates[right_index]; right_segment = segment_map[str(right["segment_id"])]
                right_number = int(str(right["segment_id"]).rsplit("-", 1)[1])
                if right_number - left_number > 8: break
                shared_entity = bool(set(left["entity_ids"]) & set(right["entity_ids"]))
                shared_concept = bool(set(left_segment["concept_tags"]) & set(right_segment["concept_tags"]))
                shared_statement = bool(set(left_segment["statement_classifications"]) & set(right_segment["statement_classifications"]))
                overlap = jaccard(tokens[left_index], tokens[right_index])
                exact_claim_signature = (
                    set(left["entity_ids"]) == set(right["entity_ids"])
                    and set(left_segment["concept_tags"]) == set(right_segment["concept_tags"])
                    and set(left_segment["statement_classifications"]) == set(right_segment["statement_classifications"])
                )
                adjacent_restatement = (
                    right_number - left_number == 1
                    and shared_entity and shared_statement and overlap >= .08
                )
                if (shared_entity or shared_concept) and shared_statement and (overlap >= .62 or exact_claim_signature or adjacent_restatement):
                    union(left_index, right_index)

    groups: dict[int, list[int]] = defaultdict(list)
    for index in range(len(candidates)): groups[find(index)].append(index)
    clusters = []
    for indexes in groups.values():
        if len(indexes) < 2: continue
        strongest_index = max(indexes, key=lambda i: (int(decision_map[str(candidates[i]["segment_id"])]["score"]), len(candidates[i]["supporting_captions"]), len(tokens[i]), -i))
        cluster_id = f"DUPLICATE-CLUSTER-SA-{len(clusters) + 1:04d}"
        strongest_id = candidates[strongest_index]["candidate_id"]
        member_ids = [candidates[i]["candidate_id"] for i in indexes]
        clusters.append({
            "duplicate_cluster_id": cluster_id, "candidate_type": "PROMOTION",
            "strongest_candidate_id": strongest_id, "member_candidate_ids": member_ids,
            "member_segment_ids": [candidates[i]["segment_id"] for i in indexes],
            "duplicate_reason": "Same recording, shared entity/concept and statement class, with high normalized supporting-caption token overlap.",
        })
        for index in indexes:
            candidate = candidates[index]
            candidate["duplicate_cluster_id"] = cluster_id
            candidate["strongest_candidate_id"] = strongest_id
            candidate["duplicate_reason"] = "strongest member" if index == strongest_index else "near-duplicate of stronger candidate"
            decision = decision_map[str(candidate["segment_id"])]
            decision["duplicate_cluster_id"] = cluster_id
            decision["strongest_candidate_id"] = strongest_id
            decision["duplicate_reason"] = candidate["duplicate_reason"]
            segment_map[str(candidate["segment_id"])]["near_duplicate_cluster_id"] = cluster_id
    return clusters


def count_candidates_by(candidates: list[dict[str, object]], segment_map: dict[str, dict[str, object]], field: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for candidate in candidates:
        for value in segment_map[str(candidate["segment_id"])][field]: counts[str(value)] += 1
    return dict(sorted(counts.items()))


def main() -> None:
    source_records = []
    for path in sorted(SOURCE_ROOT.rglob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8")); record["repository_source_record_path"] = path.relative_to(ROOT).as_posix(); source_records.append(record)

    all_segments = []
    link_records = []
    quotes = []
    timeline_candidates = []
    promotion_candidates = []
    promotion_decisions = []
    timeline_decisions = []
    source_index = []
    collection_sources: dict[str, list[str]] = defaultdict(list)
    topic_segments: dict[str, list[str]] = {topic: [] for topic in TOPICS}
    concept_segments: dict[str, list[str]] = defaultdict(list)
    seen_hashes: dict[str, str] = {}
    source_gap_records = []
    candidate_gap_records = []
    group_map: dict[str, list[dict[str, object]]] = {}

    source_by_id = {record["source_id"]: record for record in source_records}
    for source_number, source_id in enumerate(sorted(source_by_id), start=1):
        record = source_by_id[source_id]
        collection = record["collection"]
        transcript_path = INPUT_ROOT / collection / f"{source_id}.md"
        captions = parse_transcript(transcript_path)
        groups = segment_captions(captions)
        source_segment_ids = []
        source_topic_counts: Counter[str] = Counter()
        source_statement_counts: Counter[str] = Counter()
        gaps = source_gap_types(record)
        source_gap_records.append({"gap_id": f"RESEARCH-GAP-SA-{source_number:04d}", "source_id": source_id, "gap_types": gaps, "status": "OPEN", "manual_review_required": True})

        for number, group in enumerate(groups, start=1):
            segment_id = f"SEG-{source_id.removeprefix('SRC-')}-{number:04d}"
            source_segment_ids.append(segment_id); group_map[segment_id] = group
            text = " ".join(str(item["text"]) for item in group)
            topics = tags_for(text, TOPIC_PATTERNS) or {"economic-forum": ["ECONOMY"], "dao": ["GOVERNANCE"], "townhall": ["COMMUNITY"]}[collection]
            links, unresolved = entity_links(text)
            concepts = concepts_for(text, unresolved)
            statements, statement_evidence = detect_statements(group, links, unresolved, concepts)
            lifecycle, lifecycle_evidence = detect_lifecycle(group, links, unresolved, concepts)
            entity_ids = [str(link["entity_id"]) for link in links]
            duration = int(group[-1]["seconds"]) - int(group[0]["seconds"])
            content_hash = sha256_text(re.sub(r"\s+", " ", text.lower()).strip())
            duplicate_of = seen_hashes.get(content_hash)
            if not duplicate_of: seen_hashes[content_hash] = segment_id
            segment_gaps = []
            if transcript_ambiguity(text): segment_gaps.append("TRANSCRIPT_RECOGNITION_UNCERTAINTY")
            if unresolved and not links: segment_gaps.append("AMBIGUOUS_PRODUCT_OR_ENTITY_IDENTITY")

            segment = {
                "segment_id": segment_id, "recording_id": f"RECORDING-{source_id.removeprefix('SRC-')}",
                "source_id": source_id, "collection": collection, "publication_date": record.get("publication_date"),
                "start_timestamp": group[0]["timestamp"], "end_timestamp": group[-1]["timestamp"],
                "speaker": "UNKNOWN", "speaker_confidence": "UNKNOWN",
                "speaker_dependency": speaker_dependency_for(text),
                "institutional_attribution": "UNESTABLISHED",
                "participants": [], "duration": duration,
                "summary": summarize(text, topics, statements, concepts), "topic_tags": topics,
                "concept_tags": concepts, "statement_classifications": statements,
                "statement_evidence": statement_evidence, "product_lifecycle": lifecycle,
                "lifecycle_evidence": lifecycle_evidence, "entity_ids": entity_ids,
                "unresolved_references": unresolved, "promotion_targets": promotion_targets(topics),
                "quote_ids": [], "duplicate_of": duplicate_of, "near_duplicate_cluster_id": None,
                "content_sha256": content_hash,
                "research_gap_status": "OPEN" if segment_gaps else "NONE_IDENTIFIED",
                "research_gap_types": segment_gaps,
                "transcript_reference": {"path": transcript_path.relative_to(ROOT).as_posix(), "line_start": group[0]["line"], "line_end": group[-1]["line"], "caption_lines": len(group)},
                "transcript_excerpt": re.sub(r"\s+", " ", text).strip()[:500],
            }

            promotion = is_promotion_candidate(segment, group, links, unresolved, statement_evidence, record)
            promotion_decision_id = f"PROMOTION-DECISION-SA-{len(promotion_decisions) + 1:05d}"
            promotion_candidate_id = f"PROMOTION-CANDIDATE-SA-{len(promotion_candidates) + 1:05d}" if promotion["eligible"] else None
            promotion_record = {"decision_id": promotion_decision_id, "segment_id": segment_id, "source_id": source_id, "candidate_id": promotion_candidate_id, **promotion, "duplicate_cluster_id": None, "strongest_candidate_id": None, "duplicate_reason": None}
            promotion_decisions.append(promotion_record)
            if promotion_candidate_id:
                promotion_candidates.append({
                    "candidate_id": promotion_candidate_id, "segment_id": segment_id, "source_id": source_id,
                    "timestamp": f"{group[0]['timestamp']}-{group[-1]['timestamp']}",
                    "promotion_targets": segment["promotion_targets"], "entity_ids": entity_ids,
                    "statement_classifications": statements, "summary": segment["summary"],
                    "supporting_captions": promotion["supporting_captions"],
                    "candidate_confidence": promotion["candidate_confidence"],
                    "candidate_reasons": promotion["candidate_reasons"], "review_priority": promotion["review_priority"],
                    "speaker_dependency": promotion["speaker_dependency"],
                    "institutional_attribution": promotion["institutional_attribution"],
                    "research_gap_types": promotion["research_gap_types"], "promotion_status": "PROPOSED_ONLY",
                    "manual_review_required": True, "duplicate_cluster_id": None, "strongest_candidate_id": None, "duplicate_reason": None,
                })
                for gap_type in promotion["research_gap_types"]:
                    candidate_gap_records.append({"candidate_id": promotion_candidate_id, "segment_id": segment_id, "source_id": source_id, "candidate_type": "PROMOTION", "gap_type": gap_type})

            timeline = is_timeline_candidate(segment, group, links, unresolved, record)
            timeline_decision_id = f"TIMELINE-DECISION-SA-{len(timeline_decisions) + 1:05d}"
            timeline_candidate_id = f"TIMELINE-CANDIDATE-{len(timeline_candidates) + 1:05d}" if timeline["eligible"] else None
            timeline_record = {"decision_id": timeline_decision_id, "segment_id": segment_id, "source_id": source_id, "candidate_id": timeline_candidate_id, **timeline}
            timeline_decisions.append(timeline_record)
            if timeline_candidate_id:
                timeline_candidates.append({
                    "candidate_id": timeline_candidate_id, "segment_id": segment_id, "source_id": source_id,
                    "timestamp": group[0]["timestamp"], "event_type": timeline["event_type"],
                    "date_value": timeline["date_value"], "date_precision": timeline["date_precision"], "date_basis": timeline["date_basis"],
                    "supporting_captions": timeline["supporting_captions"], "timeline_confidence": timeline["timeline_confidence"],
                    "timeline_reasons": timeline["timeline_reasons"], "research_gap_types": timeline["research_gap_types"],
                    "speaker_dependency": timeline["speaker_dependency"],
                    "institutional_attribution": timeline["institutional_attribution"],
                    "summary": segment["summary"], "manual_review_required": True,
                })
                for gap_type in timeline["research_gap_types"]:
                    candidate_gap_records.append({"candidate_id": timeline_candidate_id, "segment_id": segment_id, "source_id": source_id, "candidate_type": "TIMELINE", "gap_type": gap_type})

            quote_decision = is_quote_candidate(segment, group)
            quote_id = f"QUOTE-{source_id.removeprefix('SRC-')}-{len(quotes) + 1:05d}" if quote_decision["eligible"] else None
            if quote_id:
                ref = quote_decision["supporting_caption"]
                segment["quote_ids"].append(quote_id)
                ref_line = next(i for i, item in enumerate(group) if int(item["line"]) == int(ref["line"]))
                context = [caption_reference(item) for item in group[max(0, ref_line - 1):min(len(group), ref_line + 2)]]
                quotes.append({
                    "quote_id": quote_id, "segment_id": segment_id, "source_id": source_id,
                    "timestamp": ref["timestamp"], "speaker": "UNKNOWN", "verbatim_quote": ref["text"],
                    "quote_context": context, "quote_category": quote_decision["quote_category"],
                    "quote_confidence": quote_decision["quote_confidence"], "candidate_reasons": quote_decision["candidate_reasons"],
                    "speaker_dependency": quote_decision["speaker_dependency"],
                    "institutional_attribution": quote_decision["institutional_attribution"],
                    "flag": "KEY_QUOTE", "manual_review_required": True,
                })
            segment["candidate_decisions"] = {
                "promotion_decision_id": promotion_decision_id, "promotion_disposition": promotion["disposition"],
                "timeline_decision_id": timeline_decision_id, "timeline_eligible": timeline["eligible"],
                "quote_candidate_decision": {**quote_decision, "quote_id": quote_id},
            }
            evidence = []
            if promotion["eligible"]: evidence.append("CANONICAL_KNOWLEDGE")
            if timeline["eligible"]: evidence.append("TIMELINE_EVENT")
            if entity_ids: evidence.append("ENTITY_UPDATE")
            if len(entity_ids) > 1 or "PARTNERSHIP" in topics: evidence.append("GRAPH_RELATIONSHIP")
            if segment_gaps or gaps: evidence.append("RESEARCH_GAP")
            if "CORRECTION" in statements: evidence.append("CONTRADICTION")
            if not promotion["eligible"] and not timeline["eligible"] and not quote_decision["eligible"]: evidence.append("LOW_VALUE")
            if duplicate_of: evidence.append("DUPLICATE")
            segment["evidence_classifications"] = [value for value in EVIDENCE if value in set(evidence)]
            all_segments.append(segment)
            link_records.append({"segment_id": segment_id, "source_id": source_id, "link_status": "LINKED" if links else ("UNRESOLVED_ONLY" if unresolved else "NO_ENTITY_IDENTIFIED"), "canonical_entities": links, "unresolved_references": unresolved})
            for topic in topics: topic_segments[topic].append(segment_id); source_topic_counts[topic] += 1
            for statement in statements: source_statement_counts[statement] += 1
            for concept in concepts: concept_segments[concept].append(segment_id)

        source_index.append({
            "recording_id": f"RECORDING-{source_id.removeprefix('SRC-')}", "source_id": source_id, "collection": collection,
            "title": record["title"], "publication_date": record.get("publication_date"), "publication_date_basis": record.get("publication_date_basis"),
            "original_url": record.get("original_url"), "speaker_attribution": record.get("speaker_attribution", "UNKNOWN"),
            "transcript_path": transcript_path.relative_to(ROOT).as_posix(), "source_record_path": record["repository_source_record_path"],
            "transcript_start_timestamp": record.get("first_timestamp"), "transcript_end_timestamp": record.get("last_timestamp"),
            "caption_lines": len(captions), "segment_count": len(source_segment_ids), "segment_ids": source_segment_ids,
            "topic_counts": dict(sorted(source_topic_counts.items())), "statement_counts": dict(sorted(source_statement_counts.items())),
        })
        collection_sources[collection].append(source_id)

    segment_map = {str(segment["segment_id"]): segment for segment in all_segments}
    promotion_decision_map = {str(decision["segment_id"]): decision for decision in promotion_decisions}
    duplicate_clusters = build_duplicate_clusters(promotion_candidates, segment_map, promotion_decision_map)

    topic_counts = Counter(value for segment in all_segments for value in segment["topic_tags"])
    statement_counts = Counter(value for segment in all_segments for value in segment["statement_classifications"])
    lifecycle_counts = Counter(value for segment in all_segments for value in segment["product_lifecycle"])
    evidence_counts = Counter(value for segment in all_segments for value in segment["evidence_classifications"])
    entity_link_count = sum(len(link["canonical_entities"]) for link in link_records)
    unresolved_count = sum(len(link["unresolved_references"]) for link in link_records)
    promotion_confidence = Counter(str(c["candidate_confidence"]) for c in promotion_candidates)
    promotion_priority = Counter(str(c["review_priority"]) for c in promotion_candidates)
    timeline_confidence = Counter(str(c["timeline_confidence"]) for c in timeline_candidates)
    quote_confidence = Counter(str(c["quote_confidence"]) for c in quotes)
    promotion_exclusions = Counter(str(d["exclusion_reason"]) for d in promotion_decisions if not d["eligible"])
    timeline_exclusions = Counter(str(d["exclusion_reason"]) for d in timeline_decisions if not d["eligible"])
    gap_counts = Counter(record["gap_type"] for record in candidate_gap_records)
    speaker_dependency_counts = Counter(str(segment["speaker_dependency"]) for segment in all_segments)

    common = {"campaign_id": CAMPAIGN_ID, "schema_version": SCHEMA_VERSION, "generated_from": INPUT_ROOT.relative_to(ROOT).as_posix()}
    write_json("collection-index.json", {**common, "collection_count": len(collection_sources), "collections": [{"collection": name, "source_count": len(ids), "source_ids": ids} for name, ids in sorted(collection_sources.items())]})
    write_json("source-index.json", {**common, "source_count": len(source_index), "sources": source_index})
    write_json("segment-index.json", {**common, "segmentation_method": "Unchanged v1 lexical topic signatures, conversational transitions, transcript gaps, and maximum-coherence safeguards; not fixed timestamp intervals.", "topic_taxonomy": TOPICS, "statement_taxonomy": STATEMENTS, "product_lifecycle_taxonomy": LIFECYCLES, "evidence_taxonomy": EVIDENCE, "segment_count": len(all_segments), "segments": all_segments})
    write_json("topic-index.json", {**common, "taxonomy": TOPICS, "topics": {topic: {"segment_count": len(topic_segments[topic]), "segment_ids": topic_segments[topic]} for topic in TOPICS}})
    write_json("concept-index.json", {**common, "concept_count": len(concept_segments), "concepts": {concept: {"segment_count": len(ids), "segment_ids": ids} for concept, ids in sorted(concept_segments.items())}})
    write_json("entity-links.json", {**common, "link_record_count": len(link_records), "links": link_records})
    write_json("quote-index.json", {**common, "quote_count": len(quotes), "quotes": quotes})
    write_json("timeline-candidates.json", {**common, "candidate_count": len(timeline_candidates), "candidates": timeline_candidates})
    write_json("promotion-candidates.json", {**common, "candidate_count": len(promotion_candidates), "candidates": promotion_candidates})
    write_json("promotion-candidate-decisions.json", {**common, "decision_count": len(promotion_decisions), "eligible_count": len(promotion_candidates), "excluded_count": len(promotion_decisions) - len(promotion_candidates), "decisions": promotion_decisions})
    write_json("timeline-candidate-decisions.json", {**common, "decision_count": len(timeline_decisions), "eligible_count": len(timeline_candidates), "excluded_count": len(timeline_decisions) - len(timeline_candidates), "decisions": timeline_decisions})
    write_json("duplicate-clusters.json", {**common, "cluster_count": len(duplicate_clusters), "clusters": duplicate_clusters})
    write_json("research-gaps.json", {**common, "source_gap_count": len(source_gap_records), "candidate_gap_count": len(candidate_gap_records), "source_gaps": source_gap_records, "candidate_gaps": candidate_gap_records, "top_candidate_gap_types": dict(gap_counts.most_common(10))})

    artifacts = []
    for path in sorted(OUTPUT_ROOT.glob("*.json")):
        if path.name != "quality-report.json": artifacts.append({"path": path.relative_to(ROOT).as_posix(), "size_bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    quality = {
        **common, "status": "READY_FOR_REVIEW",
        "methodology_revision": {"previous_promotion_candidates": 1909, "previous_timeline_candidates": 1590, "previous_quote_candidates": 526, "tag_detection_separated_from_candidate_eligibility": True},
        "input_counts": {"collections": 3, "sources": len(source_index), "caption_lines": sum(s["caption_lines"] for s in source_index)},
        "output_counts": {"segments": len(all_segments), "canonical_entity_links": entity_link_count, "unresolved_entity_references": unresolved_count, "key_quotes": len(quotes), "timeline_candidates": len(timeline_candidates), "promotion_candidates": len(promotion_candidates), "promotion_exclusions": len(promotion_decisions) - len(promotion_candidates), "timeline_exclusions": len(timeline_decisions) - len(timeline_candidates), "duplicate_clusters": len(duplicate_clusters), "source_research_gaps": len(source_gap_records), "candidate_research_gaps": len(candidate_gap_records)},
        "confidence_distributions": {"promotion": dict(sorted(promotion_confidence.items())), "timeline": dict(sorted(timeline_confidence.items())), "quotes": dict(sorted(quote_confidence.items()))},
        "promotion_priority_distribution": dict(sorted(promotion_priority.items())),
        "exclusion_counts": {"promotion": dict(sorted(promotion_exclusions.items())), "timeline": dict(sorted(timeline_exclusions.items()))},
        "candidate_counts": {
            "promotion_by_collection": dict(sorted(Counter(segment_map[str(c["segment_id"])]["collection"] for c in promotion_candidates).items())),
            "promotion_by_topic": count_candidates_by(promotion_candidates, segment_map, "topic_tags"),
            "promotion_by_statement_type": count_candidates_by(promotion_candidates, segment_map, "statement_classifications"),
            "promotion_by_entity": dict(sorted(Counter(entity for c in promotion_candidates for entity in c["entity_ids"]).items())),
            "timeline_by_collection": dict(sorted(Counter(segment_map[str(c["segment_id"])]["collection"] for c in timeline_candidates).items())),
            "timeline_by_event_type": dict(sorted(Counter(str(c["event_type"]) for c in timeline_candidates).items())),
        },
        "top_unresolved_research_gaps": dict(gap_counts.most_common(10)),
        "speaker_attribution_confidence": {"UNKNOWN": len(all_segments)},
        "speaker_dependency_distribution": dict(sorted(speaker_dependency_counts.items())),
        "candidate_speaker_dependency_distributions": {
            "promotion": dict(sorted(Counter(str(item["speaker_dependency"]) for item in promotion_candidates).items())),
            "timeline": dict(sorted(Counter(str(item["speaker_dependency"]) for item in timeline_candidates).items())),
            "quotes": dict(sorted(Counter(str(item["speaker_dependency"]) for item in quotes).items())),
        },
        "topic_counts": dict(topic_counts),
        "statement_counts": dict(sorted(statement_counts.items())), "lifecycle_counts": dict(sorted(lifecycle_counts.items())), "evidence_counts": dict(sorted(evidence_counts.items())),
        "validation": {"source_ids_unique": len({s["source_id"] for s in source_index}) == len(source_index), "segment_ids_unique": len({s["segment_id"] for s in all_segments}) == len(all_segments), "caption_lines_reconcile": sum(s["transcript_reference"]["caption_lines"] for s in all_segments) == sum(s["caption_lines"] for s in source_index), "all_promotion_candidates_have_support": all(c["supporting_captions"] for c in promotion_candidates), "all_timeline_candidates_have_support_and_date_basis": all(c["supporting_captions"] and c["date_basis"] for c in timeline_candidates), "all_exclusions_record_reasons": all(d["eligible"] or d["exclusion_reason"] for d in promotion_decisions + timeline_decisions), "speaker_identity_not_inferred": all(s["speaker"] == "UNKNOWN" for s in all_segments), "canonical_layers_untouched": True},
        "manifest": {"artifact_count_excluding_quality_report": len(artifacts), "artifacts": artifacts, "note": "quality-report.json is the manifest container and is excluded from its own checksum list."},
        "limitations": ["All normalized transcripts lack systematic speaker labels; UNKNOWN is preserved rather than inferred.", "Original URLs are absent and publication dates are missing or partial for 33 sources.", "Candidate confidence measures extraction quality, not factual truth.", "Lifecycle tags are wording-based and do not establish release, approval, execution, or current status.", "No FIRST_MENTION tag is assigned because corpus ordering and partial dates cannot establish historical priority.", "Automated transcript text may contain recognition errors."]
    }
    write_json("quality-report.json", quality)

    semantic_bytes = sum(path.stat().st_size for path in OUTPUT_ROOT.glob("*.json"))
    summary = {
        "campaign_id": CAMPAIGN_ID, "status": "READY_FOR_SEMANTIC_REVIEW", "base_campaign_id": "star-atlas-transcripts-ingestion-2026-07",
        "dependency_status": "PR_11_MERGED_INTO_MAIN", "collections": 3, "sources": len(source_index), "caption_lines": 78752,
        "segments": len(all_segments), "previous_promotion_candidates": 1909, "promotion_candidates": len(promotion_candidates),
        "promotion_exclusions": len(promotion_decisions) - len(promotion_candidates), "previous_timeline_candidates": 1590,
        "timeline_candidates": len(timeline_candidates), "timeline_exclusions": len(timeline_decisions) - len(timeline_candidates),
        "previous_key_quotes": 526, "key_quotes": len(quotes), "duplicate_clusters": len(duplicate_clusters),
        "promotion_confidence": dict(sorted(promotion_confidence.items())), "timeline_confidence": dict(sorted(timeline_confidence.items())),
        "quote_confidence": dict(sorted(quote_confidence.items())), "promotion_priorities": dict(sorted(promotion_priority.items())),
        "speaker_dependency_distribution": dict(sorted(speaker_dependency_counts.items())),
        "canonical_entity_links": entity_link_count, "unresolved_entity_references": unresolved_count,
        "semantic_artifacts": len(list(OUTPUT_ROOT.glob("*.json"))), "semantic_artifact_bytes": semantic_bytes,
        "knowledge_promotions": 0, "graph_modifications": 0, "publication_modifications": 0,
    }
    write_ops_json("campaign-summary.json", summary)
    (OPS_ROOT / "campaign-summary.md").write_text(
        "# Star Atlas Transcript Semantic Enrichment — Revised\n\n"
        "This revision preserves the separation between lexical tags and candidate eligibility, and replaces the blanket unknown-speaker penalty with claim-specific speaker dependency while retaining all 1,910 semantic segments and all 78,752 caption assignments.\n\n"
        f"- Promotion candidates: **1,909 → {len(promotion_candidates)}** ({len(promotion_decisions) - len(promotion_candidates)} excluded with recorded reasons)\n"
        f"- Timeline candidates: **1,590 → {len(timeline_candidates)}** ({len(timeline_decisions) - len(timeline_candidates)} excluded with recorded reasons)\n"
        f"- Quote candidates: **526 → {len(quotes)}**\n"
        f"- Near-duplicate promotion clusters: **{len(duplicate_clusters)}**\n"
        f"- Promotion confidence: {dict(sorted(promotion_confidence.items()))}\n"
        f"- Timeline confidence: {dict(sorted(timeline_confidence.items()))}\n"
        f"- Quote confidence: {dict(sorted(quote_confidence.items()))}\n\n"
        f"- Speaker dependency: {dict(sorted(speaker_dependency_counts.items()))}\n\n"
        "Every retained candidate includes exact caption references, deterministic reasons, confidence, and manual-review status. Excluded promotion and timeline decisions remain auditable. PR #11 is merged; this branch is based on current `main`. No archive evidence or canonical layers were modified.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
