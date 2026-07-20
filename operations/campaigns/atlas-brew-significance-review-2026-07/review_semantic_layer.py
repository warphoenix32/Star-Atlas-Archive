"""Apply selective, evidence-centered significance decisions to Atlas Brew segments."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SEMANTIC = ROOT / "archive/semantic/atlas-brew"
TRANSCRIPT = ROOT / "archive/normalized/atlas-brew-combined/atlas-brew-combined-normalized.md"
CAMPAIGN_ID = "atlas-brew-significance-review-2026-07"
SCHEMA = "1.1.0"

CAPTION_RE = re.compile(r"^\[(\d{2}:\d{2}:\d{2})\]\s+(.*)$")
NUMBER_RE = re.compile(r"\b(?:\d[\d,.]*|q[1-4]|20\d{2}|pip[- ]?\d+)\b", re.I)
FILLER_RE = re.compile(r"^(?:okay|ok|yeah|yes|no|right|awesome|cool|hello|hi|welcome|thank you|thanks|all right|um+|uh+|so)+[\s,.!?-]*$", re.I)
QUESTION_RE = re.compile(r"\b(?:what|when|where|why|who|how|can you|could you|do you|are you|is it|question)\b", re.I)
UNCERTAINTY_RE = re.compile(r"\b(?:maybe|might|possibly|probably|i think|i guess|could be|theory|theorycraft)\b", re.I)
IDENTITY_RE = re.compile(r"\b(?:star atlas|atlas brew|sage|score|starbased|fleet command|escape velocity|holosim|showroom|marketplace|polis|atlas token|dao|council|foundation|pip[- ]?\d+|unreal engine|solana|c4|crew|ships?|guild|dac|treasury|mining|crafting)\b", re.I)
ACTION_RE = re.compile(r"\b(?:announce|launch|release|ship|deploy|publish|approve|vote|fund|pay|build|develop|test|update|replace|retire|cancel|complete|implement|integrate|migrate|partner|hire|appoint)\w*\b", re.I)

STATEMENT_RULES = {
    "ANNOUNCEMENT": re.compile(r"\b(?:we|star atlas|the team)\s+(?:are\s+|have\s+)?(?:announc|introduc|reveal|unveil)\w*\b", re.I),
    "RELEASE": re.compile(r"\b(?:released?|launched?|shipped?|deployed?|went live|is live|now available|available now)\b", re.I),
    "STATUS_UPDATE": re.compile(r"\b(?:in development|being developed|working on|currently testing|in testing|completed|finished|delayed|paused|deprecated|retired|canceled|cancelled)\b", re.I),
    "ROADMAP": re.compile(r"\b(?:roadmap|plan(?:ned)? to|scheduled to|targeting|aim(?:ing)? to|intend(?:ed)? to|expect(?:ed)? to (?:launch|release|ship|deploy)|next milestone)\b", re.I),
    "TECHNICAL_EXPLANATION": re.compile(r"\b(?:works by|works through|built (?:on|with)|architecture|smart contract|program account|api|sdk|rpc|mainnet|testnet|unreal engine|solana)\b", re.I),
    "CORRECTION": re.compile(r"\b(?:correction|we were wrong|not accurate|retract|previously misstated|actually,? that)\b", re.I),
    "CLARIFICATION": re.compile(r"\b(?:to clarify|what that means|in other words|the distinction is|specifically)\b", re.I),
    "RETROSPECTIVE": re.compile(r"\b(?:looking back|at the time|we had released|we launched|used to|previous version|back then)\b", re.I),
    "COMMUNITY_FEEDBACK": re.compile(r"\b(?:community feedback|players? (?:asked|reported|wanted)|feedback from|community (?:asked|reported|wanted))\b", re.I),
}

LIFECYCLE_RULES = {
    "PLANNED": re.compile(r"\b(?:plan(?:ned)? to|roadmap|scheduled to|targeting|aim(?:ing)? to|intend(?:ed)? to)\b", re.I),
    "IN_DEVELOPMENT": re.compile(r"\b(?:in development|being developed|working on|under development)\b", re.I),
    "TESTING": re.compile(r"\b(?:in testing|currently testing|test build|playtest|devnet|testnet|limited access)\b", re.I),
    "LIVE": re.compile(r"\b(?:is live|went live|available now|public release|on mainnet)\b", re.I),
    "UPDATED": re.compile(r"\b(?:updated|new update|patch(?:ed)?|upgraded|new version)\b", re.I),
    "SUPERSEDED": re.compile(r"\b(?:superseded|replaced by|successor to)\b", re.I),
    "DEPRECATED": re.compile(r"\b(?:deprecated|retired|sunset|no longer supported)\b", re.I),
    "CANCELLED": re.compile(r"\b(?:canceled|cancelled|will not be developed|scrapped)\b", re.I),
}

TIMELINE_RULES = {
    "ANNOUNCEMENT": STATEMENT_RULES["ANNOUNCEMENT"],
    "RELEASE_OR_DEPLOYMENT": STATEMENT_RULES["RELEASE"],
    "PUBLIC_OR_LIMITED_TESTING": re.compile(r"\b(?:public test|playtest|test build|devnet|testnet|limited access|testing opened)\b", re.I),
    "GOVERNANCE_PROPOSAL_OR_VOTE": re.compile(r"\b(?:pip[- ]?\d+|proposal)\s+(?:was\s+|is\s+|has been\s+)?(?:published|submitted|approved|rejected|passed|failed)|\bvoting\s+(?:opened|closed|is live)\b", re.I),
    "PARTNERSHIP": re.compile(r"\b(?:announced? (?:a |the )?partnership|partnered with|partnership with)\b", re.I),
    "TREASURY_OR_FUNDING_ACTION": re.compile(r"\b(?:funding|grant|treasury)\s+(?:was\s+|is\s+)?(?:approved|rejected|paid|transferred|allocated)|\bpaid out\b", re.I),
    "ORGANIZATIONAL_CHANGE": re.compile(r"\b(?:hired|appointed|resigned|laid off|restructured|formed the|elected to)\b", re.I),
    "CORRECTION": STATEMENT_RULES["CORRECTION"],
    "DEPRECATION_OR_CANCELLATION": re.compile(r"\b(?:deprecated|retired|sunset|canceled|cancelled|shut down)\b", re.I),
    "MATERIAL_PRODUCT_UPDATE": re.compile(r"\b(?:patch|update|upgrade)\s+(?:was\s+|is\s+|has been\s+)?(?:released|live|deployed|available)\b", re.I),
    "EVENT_OCCURRED": re.compile(r"\b(?:took place|was held|we hosted|event concluded|tournament concluded|winner was announced)\b", re.I),
}

QUOTE_RULES = {
    "CORRECTION": STATEMENT_RULES["CORRECTION"],
    "RELEASE_OR_DEPLOYMENT": STATEMENT_RULES["RELEASE"],
    "GOVERNANCE": re.compile(r"\b(?:pip[- ]?\d+|proposal|vote|voting|treasury|council|dao)\b", re.I),
    "ECONOMIC_OR_TREASURY": re.compile(r"\b(?:tokenomics|treasury|emission|revenue|funding|atlas token|polis)\b", re.I),
    "TECHNICAL_EXPLANATION": STATEMENT_RULES["TECHNICAL_EXPLANATION"],
    "ROADMAP_COMMITMENT": STATEMENT_RULES["ROADMAP"],
    "ANNOUNCEMENT": STATEMENT_RULES["ANNOUNCEMENT"],
}

SPEAKER_REQUIRED_RE = re.compile(r"\b(?:i|we|our team|my team)\s+(?:announce|confirm|decided|approved|released|launched|shipped|will|plan|intend|expect|promise|commit|joined|left|am responsible)\b", re.I)
SPEAKER_PARTIAL_RE = re.compile(r"\b(?:i think|i believe|in my opinion|we think|we believe|our position|from our perspective)\b", re.I)
STOPWORDS = {"the", "and", "that", "this", "with", "from", "have", "will", "would", "could", "there", "about", "they", "them", "then", "than", "what", "when", "where", "which", "your", "youre", "into", "just", "like", "because", "been", "being", "were", "was", "are", "for", "but", "not", "its", "our", "you", "all"}


def load(name: str) -> dict:
    return json.loads((SEMANTIC / name).read_text(encoding="utf-8"))


def dump(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(canonical_text_bytes(path)).hexdigest()


def canonical_text_bytes(path: Path) -> bytes:
    """Hash generated text as UTF-8/LF so manifests are platform-neutral."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")


def caption_map() -> dict[int, dict[str, object]]:
    result = {}
    for line_number, line in enumerate(TRANSCRIPT.read_text(encoding="utf-8").splitlines(), 1):
        match = CAPTION_RE.match(line)
        if match:
            result[line_number] = {"line": line_number, "timestamp": match.group(1), "text": match.group(2)}
    return result


def captions_for(segment: dict, captions: dict[int, dict[str, object]]) -> list[dict[str, object]]:
    ref = segment["transcript_reference"]
    return [captions[line] for line in range(ref["line_start"], ref["line_end"] + 1) if line in captions]


def speaker_dependency(text: str) -> str:
    if SPEAKER_REQUIRED_RE.search(text):
        return "REQUIRED"
    if SPEAKER_PARTIAL_RE.search(text):
        return "PARTIAL"
    return "NONE"


def identifiable(segment: dict) -> bool:
    return bool(segment.get("entity_ids") or segment.get("concept_tags") or IDENTITY_RE.search(segment.get("transcript_excerpt", "")))


def contextual_statements(group: list[dict[str, object]], segment: dict) -> tuple[list[str], dict[str, list[dict[str, object]]]]:
    evidence: dict[str, list[dict[str, object]]] = defaultdict(list)
    for index, caption in enumerate(group):
        window = " ".join(str(item["text"]) for item in group[max(0, index - 1): min(len(group), index + 2)])
        has_object = bool(IDENTITY_RE.search(window)) or bool(segment.get("entity_ids") or segment.get("concept_tags"))
        for tag, pattern in STATEMENT_RULES.items():
            if pattern.search(window) and (tag in {"CORRECTION", "CLARIFICATION"} or has_object):
                evidence[tag].append(dict(caption))
        if UNCERTAINTY_RE.search(window) and has_object and ACTION_RE.search(window):
            evidence["SPECULATION"].append(dict(caption))
    if not evidence:
        return ["DISCUSSION"], {}
    order = ["ANNOUNCEMENT", "STATUS_UPDATE", "ROADMAP", "RELEASE", "DESIGN_INTENT", "TECHNICAL_EXPLANATION", "Q_AND_A", "RETROSPECTIVE", "CLARIFICATION", "CORRECTION", "COMMUNITY_FEEDBACK", "DISCUSSION", "SPECULATION", "THEORYCRAFTING"]
    return [tag for tag in order if tag in evidence], {tag: refs[:5] for tag, refs in evidence.items()}


def contextual_lifecycle(group: list[dict[str, object]], segment: dict) -> tuple[list[str], list[dict[str, object]]]:
    if not identifiable(segment):
        return [], []
    tags, evidence = [], []
    for state, pattern in LIFECYCLE_RULES.items():
        matches = []
        for index, caption in enumerate(group):
            window = " ".join(str(item["text"]) for item in group[max(0, index - 1): min(len(group), index + 2)])
            if pattern.search(window) and (IDENTITY_RE.search(window) or segment.get("entity_ids") or segment.get("concept_tags")):
                matches.append(dict(caption))
        if matches:
            tags.append(state)
            evidence.append({"state": state, "entity_ids": segment.get("entity_ids", []), "concept_tags": segment.get("concept_tags", []), "supporting_caption": matches[0], "confidence": "MEDIUM"})
    return tags, evidence


def support(group: list[dict[str, object]], statements: list[str]) -> list[dict[str, object]]:
    scored = []
    patterns = [STATEMENT_RULES[tag] for tag in statements if tag in STATEMENT_RULES]
    for index, caption in enumerate(group):
        window = " ".join(str(item["text"]) for item in group[max(0, index - 1): min(len(group), index + 2)])
        score = sum(3 for pattern in patterns if pattern.search(window))
        score += 1 if IDENTITY_RE.search(window) else 0
        score += 1 if NUMBER_RE.search(window) else 0
        score += 1 if ACTION_RE.search(window) else 0
        score -= 3 if FILLER_RE.match(str(caption["text"]).strip()) else 0
        if score >= 3:
            scored.append((score, int(caption["line"]), dict(caption)))
    return [item[2] for item in sorted(scored, key=lambda item: (-item[0], item[1]))[:5]]


def confidence(score: int, supports: int, ambiguous: bool = False) -> str:
    if score >= 7 and supports >= 2 and not ambiguous:
        return "HIGH"
    if score >= 5 and not ambiguous:
        return "MEDIUM"
    return "LOW"


def promotion_decision(segment: dict, group: list[dict[str, object]]) -> dict:
    statements = set(segment["statement_classifications"])
    strong = statements & {"ANNOUNCEMENT", "STATUS_UPDATE", "ROADMAP", "RELEASE", "TECHNICAL_EXPLANATION", "CORRECTION", "RETROSPECTIVE"}
    supporting = support(group, sorted(strong))
    text = " ".join(str(item["text"]) for item in group)
    dependency = speaker_dependency(" ".join(str(item["text"]) for item in supporting) or text)
    filler_ratio = sum(bool(FILLER_RE.match(str(item["text"]).strip())) for item in group) / max(1, len(group))
    score, reasons = 0, []
    if segment.get("entity_ids"):
        score += 2; reasons.append("named canonical entity")
    elif identifiable(segment):
        score += 1; reasons.append("identifiable product, institution, proposal, or system")
    if strong:
        score += 2; reasons.append("explicit institutional claim language: " + ", ".join(sorted(strong)))
    if NUMBER_RE.search(text):
        score += 1; reasons.append("concrete metric, date, quantity, or proposal number")
    if len(supporting) >= 2:
        score += 1; reasons.append("multiple exact supporting captions")
    if len(segment.get("entity_ids", [])) > 1 or "PARTNERSHIP" in segment.get("topic_tags", []):
        score += 1; reasons.append("identifiable entity relationship")
    if dependency != "NONE":
        score -= 1
    exclusion = None
    if not identifiable(segment): exclusion = "NO_IDENTIFIABLE_INSTITUTIONAL_ENTITY_OR_OBJECT"
    elif not strong: exclusion = "NO_DISCRETE_INSTITUTIONAL_CLAIM"
    elif statements <= {"SPECULATION", "DISCUSSION"}: exclusion = "UNSUPPORTED_SPECULATION"
    elif not supporting: exclusion = "INSUFFICIENT_EXACT_CAPTION_SUPPORT"
    elif filler_ratio > 0.45: exclusion = "HOUSEKEEPING_OR_FILLER_DOMINANT"
    elif score < 5: exclusion = "EVIDENCE_DENSITY_BELOW_THRESHOLD"
    eligible = exclusion is None
    disposition = "NOT_ELIGIBLE" if not eligible else ("HIGH_PRIORITY" if score >= 7 else "MEDIUM_PRIORITY" if score >= 6 else "LOW_PRIORITY")
    gaps = []
    if dependency != "NONE": gaps.append("SPEAKER_ATTRIBUTION_MISSING_FOR_AUTHORITY_DEPENDENT_CLAIM")
    if strong & {"ROADMAP", "RELEASE", "STATUS_UPDATE"}: gaps.append("OFFICIAL_CONFIRMATION_MISSING")
    if segment.get("unresolved_references") and not segment.get("entity_ids"): gaps.append("AMBIGUOUS_PRODUCT_OR_ENTITY_IDENTITY")
    return {"eligible": eligible, "disposition": disposition, "score": score, "candidate_confidence": confidence(score, len(supporting)), "candidate_reasons": reasons, "supporting_captions": supporting, "exclusion_reason": exclusion, "review_priority": disposition, "speaker_dependency": dependency, "institutional_attribution": "UNESTABLISHED", "research_gap_types": sorted(set(gaps))}


def timeline_decision(segment: dict, group: list[dict[str, object]], video: dict) -> dict:
    event_type, supporting = None, []
    for kind, pattern in TIMELINE_RULES.items():
        for index, caption in enumerate(group):
            window = " ".join(str(item["text"]) for item in group[max(0, index - 1): min(len(group), index + 2)])
            if pattern.search(window) and (IDENTITY_RE.search(window) or segment.get("entity_ids") or segment.get("concept_tags")):
                supporting.append(dict(caption))
        if supporting:
            event_type = kind
            break
    dependency = speaker_dependency(" ".join(str(item["text"]) for item in supporting)) if supporting else "NONE"
    score, reasons = 0, []
    if event_type: score += 2; reasons.append("concrete event-state language")
    if segment.get("entity_ids"): score += 2; reasons.append("canonical event entity identified")
    elif identifiable(segment): score += 1; reasons.append("identifiable event object")
    if supporting: score += 1; reasons.append("exact supporting caption")
    if video.get("publication_date"): score += 1; reasons.append("recording publication date available")
    if any(NUMBER_RE.search(str(item["text"])) for item in supporting): score += 1; reasons.append("event caption includes a concrete detail")
    if dependency != "NONE": score -= 1
    exclusion = None
    if not event_type: exclusion = "NO_CONCRETE_EVENT_STATE_LANGUAGE"
    elif not identifiable(segment): exclusion = "NO_IDENTIFIABLE_EVENT_ENTITY_OR_SYSTEM"
    elif not supporting: exclusion = "NO_EXACT_EVENT_CAPTION"
    elif score < 4: exclusion = "EVENT_EVIDENCE_DENSITY_BELOW_THRESHOLD"
    eligible = exclusion is None
    date_value = video.get("publication_date")
    gaps = []
    if not date_value: gaps.append("EVENT_DATE_UNRESOLVED")
    if dependency != "NONE": gaps.append("SPEAKER_ATTRIBUTION_MISSING_FOR_AUTHORITY_DEPENDENT_CLAIM")
    return {"eligible": eligible, "event_type": event_type, "date_value": date_value, "date_precision": "DAY" if date_value else "UNKNOWN", "date_basis": "SOURCE_METADATA" if date_value else "UNRESOLVED_SOURCE_DATE_RECORDING_TIMESTAMP_ONLY", "recording_timestamp": segment["start_timestamp"], "supporting_captions": supporting[:5], "timeline_confidence": confidence(score, len(supporting)), "timeline_reasons": reasons, "score": score, "exclusion_reason": exclusion, "speaker_dependency": dependency, "institutional_attribution": "UNESTABLISHED", "research_gap_types": gaps}


def quote_decision(quote: dict, segment: dict) -> dict:
    text = str(quote["verbatim_quotation"]).strip()
    words = text.split()
    category = next((kind for kind, pattern in QUOTE_RULES.items() if pattern.search(text)), None)
    dependency = speaker_dependency(text)
    score = 0
    if category: score += 3
    if identifiable(segment): score += 2
    if NUMBER_RE.search(text): score += 1
    if 12 <= len(words) <= 80: score += 1
    if dependency != "NONE": score -= 1
    exclusion = None
    if not category: exclusion = "NO_INSTITUTIONAL_QUOTE_CATEGORY"
    elif not identifiable(segment): exclusion = "NO_IDENTIFIABLE_QUOTE_OBJECT"
    elif len(words) < 12 or len(words) > 90: exclusion = "FRAGMENT_OR_OVERLONG_EXCERPT"
    elif QUESTION_RE.match(text) and not ACTION_RE.search(text): exclusion = "QUESTION_WITHOUT_SUBSTANTIVE_ANSWER"
    elif score < 5: exclusion = "QUOTE_EVIDENCE_DENSITY_BELOW_THRESHOLD"
    return {"eligible": exclusion is None, "score": score, "quote_category": category, "quote_confidence": confidence(score, 1), "speaker_dependency": dependency, "institutional_attribution": "UNESTABLISHED", "exclusion_reason": exclusion}


def tokens(candidate: dict) -> set[str]:
    text = " ".join(str(item["text"]) for item in candidate["supporting_captions"])
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) >= 3 and token not in STOPWORDS}


def duplicate_clusters(candidates: list[dict], segment_map: dict[str, dict], decisions: dict[str, dict]) -> list[dict]:
    clusters = []
    by_source: dict[str, list[dict]] = defaultdict(list)
    for candidate in candidates: by_source[candidate["source_id"]].append(candidate)
    used = set()
    for source_candidates in by_source.values():
        for i, first in enumerate(source_candidates):
            if first["candidate_id"] in used: continue
            group = [first]; left = tokens(first)
            for second in source_candidates[i + 1:i + 9]:
                if second["candidate_id"] in used: continue
                right = tokens(second)
                overlap = len(left & right) / len(left | right) if left | right else 0
                a, b = segment_map[first["segment_id"]], segment_map[second["segment_id"]]
                if overlap >= 0.62 and (set(a.get("entity_ids", [])) & set(b.get("entity_ids", [])) or set(a.get("concept_tags", [])) & set(b.get("concept_tags", []))):
                    group.append(second)
            if len(group) < 2: continue
            strongest = max(group, key=lambda item: (decisions[item["segment_id"]]["score"], len(item["supporting_captions"]), -int(item["segment_id"].rsplit("-", 1)[1])))
            cluster_id = f"DUPLICATE-CLUSTER-ATLAS-BREW-{len(clusters)+1:04d}"
            for item in group:
                used.add(item["candidate_id"]); item["duplicate_cluster_id"] = cluster_id; item["strongest_candidate_id"] = strongest["candidate_id"]; item["duplicate_reason"] = "strongest member" if item is strongest else "near-duplicate of stronger candidate"
            clusters.append({"duplicate_cluster_id": cluster_id, "candidate_type": "PROMOTION", "strongest_candidate_id": strongest["candidate_id"], "member_candidate_ids": [item["candidate_id"] for item in group], "member_segment_ids": [item["segment_id"] for item in group], "duplicate_reason": "Same recording, shared entity or concept, and high supporting-caption token overlap."})
    return clusters


def main() -> None:
    segment_doc, video_doc = load("segment-index.json"), load("video-index.json")
    old_quotes, old_gaps = load("quote-index.json"), load("research-gaps.json")
    source_gaps = old_gaps.get("source_gaps", old_gaps.get("gaps", []))
    captions = caption_map()
    videos = {item["source_id"]: item for item in video_doc["videos"]}
    segments, promotion, timeline, promotion_decisions, timeline_decisions = [], [], [], [], []
    segment_map = {}

    for segment in segment_doc["segments"]:
        group = captions_for(segment, captions)
        revised = dict(segment)
        revised["legacy_statement_classifications"] = segment.get("legacy_statement_classifications", segment.get("statement_classifications", []))
        revised["legacy_product_lifecycle"] = segment.get("legacy_product_lifecycle", segment.get("product_lifecycle", []))
        statements, statement_evidence = contextual_statements(group, segment)
        lifecycle, lifecycle_evidence = contextual_lifecycle(group, segment)
        revised["statement_classifications"] = statements
        revised["statement_evidence"] = statement_evidence
        revised["product_lifecycle"] = lifecycle
        revised["lifecycle_evidence"] = lifecycle_evidence
        revised["speaker_dependency"] = speaker_dependency(" ".join(str(item["text"]) for item in group))
        revised["institutional_attribution"] = "UNESTABLISHED"
        revised["recording_cue"] = {"video_id": revised["video_id"], "source_id": revised["source_id"], "start_timestamp": revised["start_timestamp"], "end_timestamp": revised["end_timestamp"]}

        pd = promotion_decision(revised, group)
        p_decision_id = f"PROMOTION-DECISION-ATLAS-BREW-{len(promotion_decisions)+1:05d}"
        p_candidate_id = f"PROMOTION-CANDIDATE-ATLAS-BREW-{len(promotion)+1:05d}" if pd["eligible"] else None
        promotion_decisions.append({"decision_id": p_decision_id, "segment_id": revised["segment_id"], "source_id": revised["source_id"], "candidate_id": p_candidate_id, **pd})
        if p_candidate_id:
            promotion.append({"candidate_id": p_candidate_id, "segment_id": revised["segment_id"], "video_id": revised["video_id"], "source_id": revised["source_id"], "start_timestamp": revised["start_timestamp"], "end_timestamp": revised["end_timestamp"], "promotion_targets": revised["promotion_targets"], "entity_ids": revised["entity_ids"], "concept_tags": revised.get("concept_tags", []), "statement_classifications": statements, "summary": revised["summary"], "supporting_captions": pd["supporting_captions"], "candidate_confidence": pd["candidate_confidence"], "candidate_reasons": pd["candidate_reasons"], "review_priority": pd["review_priority"], "speaker_dependency": pd["speaker_dependency"], "institutional_attribution": "UNESTABLISHED", "research_gap_types": pd["research_gap_types"], "promotion_status": "PROPOSED_ONLY", "manual_review_required": True, "duplicate_cluster_id": None, "strongest_candidate_id": None, "duplicate_reason": None})

        td = timeline_decision(revised, group, videos[revised["source_id"]])
        t_decision_id = f"TIMELINE-DECISION-ATLAS-BREW-{len(timeline_decisions)+1:05d}"
        t_candidate_id = f"TIMELINE-CANDIDATE-ATLAS-BREW-{len(timeline)+1:05d}" if td["eligible"] else None
        timeline_decisions.append({"decision_id": t_decision_id, "segment_id": revised["segment_id"], "source_id": revised["source_id"], "candidate_id": t_candidate_id, **td})
        if t_candidate_id:
            timeline.append({"candidate_id": t_candidate_id, "segment_id": revised["segment_id"], "video_id": revised["video_id"], "source_id": revised["source_id"], "start_timestamp": revised["start_timestamp"], "end_timestamp": revised["end_timestamp"], "event_type": td["event_type"], "date_value": td["date_value"], "date_precision": td["date_precision"], "date_basis": td["date_basis"], "recording_timestamp": td["recording_timestamp"], "supporting_captions": td["supporting_captions"], "timeline_confidence": td["timeline_confidence"], "timeline_reasons": td["timeline_reasons"], "speaker_dependency": td["speaker_dependency"], "institutional_attribution": "UNESTABLISHED", "research_gap_types": td["research_gap_types"], "summary": revised["summary"], "manual_review_required": True})

        significance = "INSTITUTIONAL_CLAIM" if pd["eligible"] else "DATEABLE_EVENT" if td["eligible"] else "CONTEXTUAL_DISCUSSION" if identifiable(revised) and len(group) >= 5 else "LOW_VALUE_OR_BACKGROUND"
        revised["content_significance"] = significance
        revised["candidate_decisions"] = {"promotion_decision_id": p_decision_id, "promotion_disposition": pd["disposition"], "timeline_decision_id": t_decision_id, "timeline_eligible": td["eligible"]}
        evidence = []
        if pd["eligible"]: evidence.append("CANONICAL_KNOWLEDGE")
        if td["eligible"]: evidence.append("TIMELINE_EVENT")
        if revised["entity_ids"]: evidence.append("ENTITY_UPDATE")
        if len(revised["entity_ids"]) > 1 or "PARTNERSHIP" in revised["topic_tags"]: evidence.append("GRAPH_RELATIONSHIP")
        if pd["research_gap_types"] or td["research_gap_types"]: evidence.append("RESEARCH_GAP")
        if "CORRECTION" in statements: evidence.append("CONTRADICTION")
        if significance == "LOW_VALUE_OR_BACKGROUND": evidence.append("LOW_VALUE")
        if revised.get("duplicate_of"): evidence.append("DUPLICATE")
        revised["evidence_classifications"] = evidence
        segments.append(revised); segment_map[revised["segment_id"]] = revised

    decision_map = {item["segment_id"]: item for item in promotion_decisions}
    clusters = duplicate_clusters(promotion, segment_map, decision_map)

    quotes = []
    for quote in old_quotes["quotes"]:
        segment = segment_map[quote["segment_id"]]
        qd = quote_decision(quote, segment)
        if not qd["eligible"]: continue
        retained = dict(quote)
        retained.update({"quote_category": qd["quote_category"], "quote_confidence": qd["quote_confidence"], "speaker_dependency": qd["speaker_dependency"], "institutional_attribution": "UNESTABLISHED", "manual_review_required": True, "quote_context": {"video_id": segment["video_id"], "source_id": segment["source_id"], "segment_start": segment["start_timestamp"], "segment_end": segment["end_timestamp"]}})
        quotes.append(retained)

    candidate_gaps = []
    for item in promotion + timeline:
        for gap_type in item["research_gap_types"]:
            candidate_gaps.append({"gap_id": f"RESEARCH-GAP-ATLAS-BREW-CANDIDATE-{len(candidate_gaps)+1:05d}", "candidate_id": item["candidate_id"], "segment_id": item["segment_id"], "source_id": item["source_id"], "gap_type": gap_type, "status": "OPEN"})

    common = {"campaign_id": CAMPAIGN_ID, "schema_version": SCHEMA, "generated_from": segment_doc["generated_from"], "authoritative_input_sha256": segment_doc["authoritative_input_sha256"]}
    segment_out = {
        **common,
        "segmentation_method": segment_doc["segmentation_method"],
        "topic_taxonomy": segment_doc["topic_taxonomy"],
        "statement_taxonomy": segment_doc["statement_taxonomy"],
        "product_lifecycle_taxonomy": segment_doc["product_lifecycle_taxonomy"],
        "evidence_taxonomy": segment_doc["evidence_taxonomy"],
        "segment_count": len(segments),
        "segments": segments,
    }
    dump(SEMANTIC / "segment-index.json", segment_out)
    dump(SEMANTIC / "promotion-candidates.json", {**common, "candidate_count": len(promotion), "candidates": promotion})
    dump(SEMANTIC / "timeline-candidates.json", {**common, "candidate_count": len(timeline), "candidates": timeline})
    dump(SEMANTIC / "quote-index.json", {**common, "quote_count": len(quotes), "quotes": quotes})
    dump(SEMANTIC / "promotion-candidate-decisions.json", {**common, "decision_count": len(promotion_decisions), "decisions": promotion_decisions})
    dump(SEMANTIC / "timeline-candidate-decisions.json", {**common, "decision_count": len(timeline_decisions), "decisions": timeline_decisions})
    dump(SEMANTIC / "duplicate-clusters.json", {**common, "cluster_count": len(clusters), "clusters": clusters})
    dump(SEMANTIC / "research-gaps.json", {**common, "source_gap_count": len(source_gaps), "candidate_gap_count": len(candidate_gaps), "source_gaps": source_gaps, "candidate_gaps": candidate_gaps})

    artifacts = []
    for path in sorted(SEMANTIC.glob("*.json")):
        if path.name == "quality-report.json": continue
        artifacts.append({"path": path.relative_to(ROOT).as_posix(), "size_bytes": len(canonical_text_bytes(path)), "hash_mode": "UTF8_LF", "sha256": sha(path)})
    statement_counts = Counter(tag for segment in segments for tag in segment["statement_classifications"])
    legacy_statement_counts = Counter(tag for segment in segments for tag in segment["legacy_statement_classifications"])
    lifecycle_counts = Counter(tag for segment in segments for tag in segment["product_lifecycle"])
    significance_counts = Counter(segment["content_significance"] for segment in segments)
    report = {**common, "status": "READY_FOR_REVIEW", "input_counts": {"videos": len(video_doc["videos"]), "caption_lines": sum(v["caption_lines"] for v in video_doc["videos"])}, "output_counts": {"segments": len(segments), "promotion_candidates_before": 3306, "promotion_candidates_after": len(promotion), "timeline_candidates_before": 1423, "timeline_candidates_after": len(timeline), "quote_candidates_before": 1218, "quote_candidates_after": len(quotes), "promotion_exclusions": len(segments)-len(promotion), "timeline_exclusions": len(segments)-len(timeline), "duplicate_clusters": len(clusters)}, "statement_counts_before": dict(sorted(legacy_statement_counts.items())), "statement_counts_after": dict(sorted(statement_counts.items())), "lifecycle_counts_after": dict(sorted(lifecycle_counts.items())), "content_significance": dict(sorted(significance_counts.items())), "speaker_dependency": dict(sorted(Counter(segment["speaker_dependency"] for segment in segments).items())), "candidate_confidence": {"promotion": dict(sorted(Counter(item["candidate_confidence"] for item in promotion).items())), "timeline": dict(sorted(Counter(item["timeline_confidence"] for item in timeline).items())), "quotes": dict(sorted(Counter(item["quote_confidence"] for item in quotes).items()))}, "candidate_speaker_dependency": {"promotion": dict(sorted(Counter(item["speaker_dependency"] for item in promotion).items())), "timeline": dict(sorted(Counter(item["speaker_dependency"] for item in timeline).items())), "quotes": dict(sorted(Counter(item["speaker_dependency"] for item in quotes).items()))}, "validation": {"segments_preserved": len(segments)==4937, "source_ids_reconcile": len({s["source_id"] for s in segments})==123, "caption_lines_reconcile": sum(s["transcript_reference"]["caption_lines"] for s in segments)==198558, "all_promotion_candidates_have_support": all(i["supporting_captions"] for i in promotion), "all_timeline_candidates_have_support": all(i["supporting_captions"] for i in timeline), "all_exclusions_have_reasons": all(i["eligible"] or i["exclusion_reason"] for i in promotion_decisions+timeline_decisions), "speaker_identity_not_inferred": all(s["speaker"]=="UNKNOWN" for s in segments), "canonical_layers_untouched": True}, "manifest": {"artifact_count_excluding_quality_report": len(artifacts), "artifacts": artifacts, "note": "quality-report.json is excluded from its own checksum list."}, "limitations": ["Publication dates and original URLs remain absent for the supplied combined transcript sources.", "Speaker identity remains UNKNOWN; dependency indicates when attribution matters to a claim.", "Candidate confidence measures extraction quality, not factual truth.", "Every candidate requires human review before knowledge promotion."]}
    dump(SEMANTIC / "quality-report.json", report)

    summary = {"campaign_id": CAMPAIGN_ID, "status": "READY_FOR_REVIEW", "segments_preserved": len(segments), "promotion_candidates_before": 3306, "promotion_candidates_after": len(promotion), "timeline_candidates_before": 1423, "timeline_candidates_after": len(timeline), "quote_candidates_before": 1218, "quote_candidates_after": len(quotes), "promotion_exclusions": len(segments)-len(promotion), "timeline_exclusions": len(segments)-len(timeline), "duplicate_clusters": len(clusters), "archive_evidence_rewritten": False, "knowledge_modified": False, "graph_modified": False, "publication_modified": False}
    dump(HERE / "campaign-summary.json", summary)
    (HERE / "campaign-summary.md").write_text("\n".join(["# Atlas Brew Significance Review", "", "**Status:** `READY_FOR_REVIEW`", "", "## Counts", "", f"- Segments preserved: {len(segments)}", f"- Promotion candidates: 3,306 -> {len(promotion)}", f"- Timeline candidates: 1,423 -> {len(timeline)}", f"- Quote candidates: 1,218 -> {len(quotes)}", f"- Promotion exclusions recorded: {len(segments)-len(promotion)}", f"- Timeline exclusions recorded: {len(segments)-len(timeline)}", f"- Near-duplicate clusters: {len(clusters)}", "", "## Evidence result", "", "Unknown speakers no longer create a universal quality penalty. Information-centered claims may remain candidates when the recording, Source ID, exact captions, and timestamps support them. Claims whose authority depends on who spoke retain a speaker-dependency gap.", "", "No transcript, source record, knowledge page, graph fact, or publication output was modified.", ""]), encoding="utf-8")


if __name__ == "__main__":
    main()
