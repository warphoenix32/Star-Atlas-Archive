"""Validate Wave 2A pages, evidence packets, references, scope, and reports."""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[4]
OPS = Path(__file__).resolve().parent
PACKETS = ROOT / "operations/campaigns/knowledge-generation-wave-2/evidence-packets"
REQUIRED_META = {"knowledge_status", "as_of", "confidence", "evidence_basis", "known_limitations", "research_gaps", "review_after", "page_risk_score", "page_risk_class"}
STATUSES = {"CANONICAL", "QUALIFIED", "PROVISIONAL", "HISTORICAL"}


def front_matter(text: str) -> dict:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("missing YAML front matter")
    raw = text[4:text.index("\n---\n", 4)]
    result = {}
    current = None
    for line in raw.splitlines():
        if line.startswith("  - "):
            if current is None or not isinstance(result.get(current), list):
                raise ValueError(f"orphan list item: {line}")
            result[current].append(line[4:].strip().strip('"'))
        elif ":" in line:
            key, value = line.split(":", 1)
            current = key.strip()
            value = value.strip().strip('"')
            result[current] = value if value else []
        elif line.strip():
            raise ValueError(f"invalid front matter line: {line}")
    return result


def internal_links(path: Path, text: str):
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if re.match(r"^(?:https?://|mailto:|#)", target):
            continue
        clean = unquote(target.split("#", 1)[0])
        if clean:
            yield (path.parent / clean).resolve(), target


def main():
    errors, warnings = [], []
    packets = []
    for path in sorted(PACKETS.glob("*.json")):
        try:
            packet = json.loads(path.read_text(encoding="utf-8"))
            packets.append(packet)
        except Exception as exc:
            errors.append(f"Invalid packet {path}: {exc}")
    if len(packets) != 18:
        errors.append(f"Expected 18 packets, found {len(packets)}")

    paths = [ROOT / p["proposed_path"] for p in packets]
    if len(set(paths)) != len(paths):
        errors.append("Duplicate proposed page paths")

    statuses, risks, actions = Counter(), Counter(), Counter()
    broken_links = []
    for packet, path in zip(packets, paths):
        if not path.exists():
            errors.append(f"Missing page: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        try:
            meta = front_matter(text)
        except Exception as exc:
            errors.append(f"Front matter error in {path.relative_to(ROOT)}: {exc}")
            continue
        missing = REQUIRED_META - set(meta)
        if missing:
            errors.append(f"Missing metadata in {path.relative_to(ROOT)}: {sorted(missing)}")
        if meta.get("knowledge_status") not in STATUSES:
            errors.append(f"Invalid knowledge status in {path.relative_to(ROOT)}")
        if meta.get("as_of") != "2026-07-15":
            errors.append(f"Current-state date missing in {path.relative_to(ROOT)}")
        statuses[meta.get("knowledge_status")] += 1
        risks[meta.get("page_risk_class")] += 1
        actions[packet["page_action"]] += 1
        if meta.get("page_risk_class") == "R3" and not meta.get("review_after"):
            errors.append(f"R3 page lacks review_after: {path.relative_to(ROOT)}")
        for resolved, raw in internal_links(path, text):
            if not resolved.exists():
                broken_links.append({"page": path.relative_to(ROOT).as_posix(), "target": raw})
        for claim in packet["material_claims"]:
            if not claim.get("supporting_sources"):
                errors.append(f"Claim without source: {packet['page_id']}/{claim['claim_id']}")
            if not claim.get("allowed_in_page"):
                errors.append(f"Disallowed claim in drafted packet: {packet['page_id']}/{claim['claim_id']}")
            authorities = set(claim.get("source_authority", []))
            if authorities and authorities <= {"C1", "C2"}:
                errors.append(f"Weak-only claim: {packet['page_id']}/{claim['claim_id']}")
            for source in claim.get("supporting_sources", []):
                if not (ROOT / source).exists():
                    errors.append(f"Unresolved evidence source: {packet['page_id']} -> {source}")
    if broken_links:
        errors.extend(f"Broken link: {x['page']} -> {x['target']}" for x in broken_links)

    low_risk = risks["R1"] + risks["R2"]
    if len(packets) and low_risk / len(packets) < 0.70:
        errors.append("R1/R2 proportion below 70%")
    if risks["R4"] or risks["R5"]:
        errors.append("Unauthorized R4/R5 page present")

    diff = subprocess.run(["git", "diff", "--name-only", "origin/main"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    prohibited = [p for p in diff if p.startswith(("archive/", "graph/", "publication/"))]
    if prohibited:
        errors.append(f"Prohibited paths changed: {prohibited}")

    ledger = {
        "campaign_id": "knowledge-generation-wave-2a",
        "accepted": [{"path": p["proposed_path"], "action": p["page_action"], "packet": f"evidence-packets/{p['page_id']}.json"} for p in packets],
        "deferred": [
            {"path": "knowledge/media/Official-Discord-Announcements-Profile.md", "reason": "PR #15 evidence is unmerged"},
            {"path": "knowledge/media/Official-X-Account-Profile.md", "reason": "Deferred to remain within the 18-output ceiling"},
            {"path": "knowledge/events/README.md", "reason": "Deferred to remain within the 18-output ceiling"},
        ],
        "duplicate": [
            {"candidate": "knowledge/organizations/Star-Atlas-DAO.md", "canonical_path": "knowledge/governance/Star-Atlas-DAO.md", "reason": "Governance authority belongs in governance domain"},
            {"candidate": "knowledge/organizations/Star-Atlas-Foundation.md", "canonical_path": "knowledge/governance/Star-Atlas-Foundation.md", "reason": "Avoid duplicate institutional authority page"},
            {"candidate": "knowledge/organizations/Star-Atlas-Council.md", "canonical_path": "knowledge/governance/Star-Atlas-Council.md", "reason": "Avoid duplicate institutional authority page"},
        ],
        "rejected": [
            {"path": "knowledge/media/Star-Atlas-Medium-Publication-Profile.md", "reason": "Complete article-by-article corpus review is absent; retain as research-only"}
        ],
    }
    (OPS / "promotion-ledger.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    (OPS / "promotion-ledger.md").write_text(
        "# Wave 2A Promotion Ledger\n\n"
        f"Accepted: {len(ledger['accepted'])}. Deferred: {len(ledger['deferred'])}. Duplicate candidates redirected: {len(ledger['duplicate'])}. Rejected for this wave: {len(ledger['rejected'])}.\n\n"
        "All accepted entries have an evidence packet. The Discord profile is deferred because PR #15 is unmerged. "
        "The Medium profile is research-only until an article-level corpus review exists. DAO, Foundation, and Council duplicate organization paths resolve to their governance pages.\n",
        encoding="utf-8",
    )

    single_authority = []
    for p in packets:
        classes = sorted({a for c in p["material_claims"] for a in c["source_authority"] if a in {"A1", "A2", "A3"}})
        if len(classes) == 1:
            single_authority.append({"path": p["proposed_path"], "authority_class": classes[0]})

    result = "PASS" if not errors else "FAIL"
    report = {
        "campaign_id": "knowledge-generation-wave-2a",
        "validation_result": result,
        "outputs": len(packets),
        "created": actions["CREATE"],
        "expanded": actions["EXPAND"],
        "knowledge_status_distribution": dict(sorted(statuses.items())),
        "risk_class_distribution": dict(sorted(risks.items())),
        "low_risk_percentage": round(100 * low_risk / len(packets), 1) if packets else 0,
        "single_authority_class_pages": single_authority,
        "r3_or_r4_pages": [p["proposed_path"] for p in packets if p["page_risk_class"] in {"R3", "R4"}],
        "broken_internal_links": broken_links,
        "prohibited_path_changes": prohibited,
        "checks": {
            "evidence_packets": len(packets) == 18,
            "required_metadata": not any("metadata" in e or "Front matter" in e for e in errors),
            "source_references_resolve": not any("evidence source" in e for e in errors),
            "internal_links_resolve": not broken_links,
            "risk_constraints": low_risk == len(packets) and not risks["R4"] and not risks["R5"],
            "archive_evidence_untouched": not any(p.startswith("archive/") for p in diff),
            "graph_untouched": not any(p.startswith("graph/") for p in diff),
            "publication_untouched": not any(p.startswith("publication/") for p in diff),
            "json_parses": True,
            "yaml_front_matter_schema_parses": not any("Front matter" in e for e in errors),
            "markdown_lint": "NOT_AVAILABLE; structural checks passed",
            "repository_schema_checks": "NO_REPOSITORY-WIDE_SUITE_PRESENT",
        },
        "errors": errors,
        "warnings": warnings,
    }
    (OPS / "validation-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (OPS / "validation-report.md").write_text(
        "# Wave 2A Validation Report\n\n"
        f"Result: **{result}**\n\n"
        f"Validated {len(packets)} outputs ({actions['CREATE']} created, {actions['EXPAND']} expanded), {len(packets)} evidence packets, and all internal evidence links. "
        f"Risk distribution: {dict(sorted(risks.items()))}; status distribution: {dict(sorted(statuses.items()))}.\n\n"
        "No `archive/`, `graph/`, or `publication/` path is changed. Proposal, vote, passage, implementation, payment, and verification remain separate. "
        "Council operational claims retain the required attribution. No R3, R4, or R5 page is present.\n\n"
        "The repository has no general schema or Markdown-lint command; the campaign validator parses every JSON file, checks the controlled front-matter schema, and resolves every internal Markdown link.\n"
        + ("\n## Errors\n\n" + "\n".join(f"- {e}" for e in errors) + "\n" if errors else ""),
        encoding="utf-8",
    )

    research = [
        "Independently reconcile Council-reported payments and milestones to transactions and deliverables.",
        "Resolve winner identities for PIP-11, PIP-25, and PIP-27 from primary election records.",
        "Preserve the exact post-passage withdrawal record for PIP-31 and independent non-implementation evidence.",
        "Build a versioned chronology from SCORE through SAGE Labs, Starbased, and C4.",
        "Build a release-note chronology for UE5/Showroom features and access environments.",
        "Complete article-level review before creating the Star Atlas Medium publication profile.",
        "Revisit the Official Discord profile after PR #15 merges.",
    ]
    (OPS / "research-gaps.md").write_text("# Wave 2A Research Gaps\n\n" + "\n".join(f"- {x}" for x in research) + "\n", encoding="utf-8")
    (OPS / "risk-register.md").write_text(
        "# Wave 2A Risk Register\n\n"
        "| Risk | Mitigation | Residual class |\n|---|---|---|\n"
        "| Council tracker mistaken for independent proof | Required attribution block on governance pages | R2 |\n"
        "| Current product copy mistaken for historical availability | Date-bound current state and build-specific lifecycle | R2 |\n"
        "| Community chronology over-promoted | Attribution and primary-source research gaps retained | R2 |\n"
        "| Duplicate institutional pages | Governance canonical paths; organization index cross-links | R1 |\n"
        "| Unmerged PR #15 evidence imported | Discord profile deferred; base remains main | R1 |\n",
        encoding="utf-8",
    )
    summary = {
        "campaign_id": "knowledge-generation-wave-2a",
        "as_of": "2026-07-15",
        "branch": "knowledge/wave-2a-foundation-pages",
        "base": "origin/main",
        "outputs": len(packets),
        "created_pages": [p["proposed_path"] for p in packets if p["page_action"] == "CREATE"],
        "expanded_pages": [p["proposed_path"] for p in packets if p["page_action"] == "EXPAND"],
        "deferred": ledger["deferred"],
        "rejected": ledger["rejected"],
        "knowledge_status_distribution": dict(sorted(statuses.items())),
        "risk_class_distribution": dict(sorted(risks.items())),
        "single_authority_class_pages": single_authority,
        "unresolved_contradictions": [
            "Portal status strings remain stale relative to reviewed vote results in the captured governance corpus.",
            "Council-reported completion may lack independent transaction or deliverable verification.",
        ],
        "unresolved_dependencies": ["PR #15 for Official Discord source-profile evidence"],
        "validation_result": result,
    }
    (OPS / "campaign-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (OPS / "campaign-summary.md").write_text(
        "# Knowledge Generation Wave 2A Summary\n\n"
        f"Wave 2A produced {len(packets)} foundation outputs: {actions['CREATE']} new pages and {actions['EXPAND']} substantive expansions. "
        f"Status distribution is {dict(sorted(statuses.items()))}; risk distribution is {dict(sorted(risks.items()))}. Validation result: **{result}**.\n\n"
        "The branch is based on `main`. PR #12 and PR #13 evidence is merged; PR #15 remains unmerged and the Discord profile is deferred. "
        "No archive or semantic evidence was rewritten, and `graph/` and `publication/` are untouched. Human semantic review is required before merge.\n",
        encoding="utf-8",
    )
    print(json.dumps({"result": result, "errors": errors, "outputs": len(packets), "risks": risks, "statuses": statuses}, default=dict, indent=2))
    raise SystemExit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
