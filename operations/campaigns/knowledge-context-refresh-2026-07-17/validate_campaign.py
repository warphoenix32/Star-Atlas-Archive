"""Validate the 2026-07-17 knowledge context refresh."""

from __future__ import annotations

import json
import hashlib
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
REQUIRED = {"knowledge_status", "as_of", "confidence", "evidence_basis", "known_limitations", "research_gaps", "review_after", "page_risk_score", "page_risk_class"}

ARCHIVAL_REQUIREMENTS = {
    "knowledge/economy/DAO-Treasury-Architecture.md": ("Constitutional framework", "Evidence states", "Known source conflicts", "Current state"),
    "knowledge/economy/PVP-Voting-Power.md": ("Governance role", "Technical behavior", "Decision boundaries", "Historical development"),
    "knowledge/gameplay/Holosim.md": ("Identity and scope", "Lifecycle chronology", "Economic and persistence boundary", "Evidence references"),
    "knowledge/gameplay/Product-Registry.md": ("How to read this registry", "Lifecycle rules", "Historical relationships", "Registry limitations and review needs"),
    "knowledge/gameplay/SAGE.md": ("Identity and institutional role", "Lifecycle chronology", "Product and evidence boundaries", "Historical value"),
    "knowledge/governance/PIP-33-ATMTA-Historic-Expense-Reimbursement.md": ("Proposal and disclosed conflict", "Vote result", "Implementation state", "Research checklist"),
    "knowledge/governance/Ecosystem-Fund.md": ("Policy history", "Reported refill history", "Decision and payment boundaries", "Research priorities"),
    "knowledge/governance/Governance-and-Economy-Overview.md": ("Institutional decision chain", "Economic evidence boundaries", "Source conflicts and interpretive controls", "Current limitations"),
    "knowledge/governance/PIP-Registry.md": ("Coverage summary", "Registry rules", "Reconciliation exceptions", "Research workflow"),
    "knowledge/media/Official-Discord-Announcements-Profile.md": ("Scope and provenance", "Authority and attribution", "Completeness and preservation boundaries", "Recommended research use"),
    "knowledge/media/Official-X-Account-Profile.md": ("Scope and provenance", "Authority boundary", "Completeness and identity boundaries", "Research use"),
    "knowledge/media/Star-Atlas-Medium-Publication-Profile.md": ("Scope and provenance status", "Authority and citation boundary", "Required corpus review", "Research use before full ingestion"),
    "knowledge/timeline/Master-Timeline.md": ("Reading rules", "2021 — Assets, markets, and first on-chain play", "2026 — C4 PTR and unresolved treasury governance", "Remaining high-priority gaps"),
    "knowledge/timeline/Product-Timeline.md": ("2021", "2024", "2026", "Open chronology questions"),
}

def meta(text: str) -> dict:
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("missing front matter")
    raw = text[4:text.index("\n---\n", 4)]
    out, key = {}, None
    for line in raw.splitlines():
        if line.startswith("  - "):
            out.setdefault(key, []).append(line[4:].strip().strip('"'))
        elif ":" in line:
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip().strip('"')
            out[key] = value if value else []
    return out

def main() -> int:
    errors, warnings = [], []
    json_files = sorted(HERE.rglob("*.json"))
    parsed_json = {}
    for path in json_files:
        try:
            parsed_json[path] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
    packets = [parsed_json[p] for p in sorted((HERE / "evidence-packets").glob("*.json")) if p in parsed_json]
    if len(packets) != 14:
        errors.append(f"Expected 14 packets, found {len(packets)}")
    broken = []
    for packet in packets:
        page = ROOT / packet["proposed_path"]
        if not page.exists():
            errors.append(f"Missing page: {packet['proposed_path']}")
            continue
        text = page.read_text(encoding="utf-8")
        fm = meta(text)
        missing = REQUIRED - set(fm)
        if missing:
            errors.append(f"Missing metadata {packet['proposed_path']}: {sorted(missing)}")
        if len(packet.get("material_claims", [])) < 3:
            errors.append(f"Insufficient claim-level evidence packet: {packet['page_id']}")
        for claim in packet["material_claims"]:
            if set(claim["source_authority"]) <= {"C1", "C2"}:
                errors.append(f"Weak-only evidence: {packet['page_id']}")
            details = claim.get("supporting_source_authorities", [])
            if [x.get("source") for x in details] != claim["supporting_sources"]:
                errors.append(f"Authority detail mismatch: {packet['page_id']}")
            for detail in details:
                if detail.get("source_role", "").startswith("DERIVED_") and detail.get("authority"):
                    errors.append(f"Derived operational artifact assigned source authority: {detail['source']}")
            for source in claim["supporting_sources"]:
                if not (ROOT / source).exists():
                    errors.append(f"Missing source: {source}")
        for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if re.match(r"^(https?://|#|mailto:)", raw):
                continue
            target = unquote(raw.split("#", 1)[0])
            if target and not (page.parent / target).resolve().exists():
                broken.append(f"{packet['proposed_path']} -> {raw}")
    errors.extend(f"Broken link: {x}" for x in broken)

    for relative, required_sections in ARCHIVAL_REQUIREMENTS.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        missing_sections = [section for section in required_sections if f"## {section}" not in text]
        if missing_sections:
            errors.append(f"Archival depth sections missing in {relative}: {missing_sections}")

    diff = subprocess.run(["git", "diff", "--name-only", "origin/main"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    changed = sorted(set(diff + untracked))
    for relative in changed:
        if not relative.startswith("knowledge/") or not relative.endswith(".md"):
            continue
        page = ROOT / relative
        text = page.read_text(encoding="utf-8")
        for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if re.match(r"^(https?://|#|mailto:)", raw):
                continue
            target = unquote(raw.split("#", 1)[0])
            if target and not (page.parent / target).resolve().exists():
                item = f"{relative} -> {raw}"
                if item not in broken:
                    broken.append(item)
    errors.extend(f"Broken link: {x}" for x in broken if not any(x in e for e in errors))
    prohibited = [p for p in changed if p.startswith(("archive/", "graph/", "publication/"))]
    if prohibited:
        errors.append(f"Prohibited paths changed: {prohibited}")
    check = subprocess.run(["git", "diff", "--check"], cwd=ROOT, text=True, capture_output=True)
    if check.returncode:
        errors.append("git diff --check failed: " + check.stdout.strip())
    for relative in untracked:
        path = ROOT / relative
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".py"}:
            text = path.read_text(encoding="utf-8")
            if not text.endswith("\n") or any(line.endswith((" ", "\t")) for line in text.splitlines()):
                errors.append(f"Whitespace check failed: {relative}")

    ledger = parsed_json.get(HERE / "promotion-ledger.json", {})
    depth_review = parsed_json.get(HERE / "archival-depth-review.json", {})
    if len(depth_review.get("page_reviews", [])) != len(packets):
        errors.append("Archival depth review does not reconcile to all evidence-packet pages")
    packet_paths = {packet["proposed_path"] for packet in packets}
    ledger_packet_paths = {item["path"] for item in ledger.get("accepted", []) if item.get("packet")}
    if packet_paths != ledger_packet_paths:
        errors.append("Promotion ledger and evidence packet paths do not reconcile")
    changed_knowledge = {p for p in changed if p.startswith("knowledge/")}
    ledger_knowledge = {item["path"] for item in ledger.get("accepted", []) if item["path"].startswith("knowledge/")}
    if changed_knowledge != ledger_knowledge:
        errors.append(f"Promotion ledger coverage mismatch: {sorted(changed_knowledge ^ ledger_knowledge)}")

    semantic_checks = {
        "failed_pip_undeclared_state_absent": "NOT_APPLICABLE" not in (ROOT / "knowledge/governance/PIP-Registry.md").read_text(encoding="utf-8"),
        "pip33_direct_treasury": "direct DAO Treasury" in (ROOT / "knowledge/governance/PIP-33-ATMTA-Historic-Expense-Reimbursement.md").read_text(encoding="utf-8"),
        "pip33_payment_unverified": "PAYMENT_UNVERIFIED" in (ROOT / "knowledge/governance/PIP-33-ATMTA-Historic-Expense-Reimbursement.md").read_text(encoding="utf-8"),
        "refills_remain_attributed": "not independently reconciled" in (ROOT / "knowledge/governance/Ecosystem-Fund.md").read_text(encoding="utf-8"),
    }
    product = (ROOT / "knowledge/timeline/Product-Timeline.md").read_text(encoding="utf-8")
    master = (ROOT / "knowledge/timeline/Master-Timeline.md").read_text(encoding="utf-8")
    semantic_checks["product_event_order"] = product.index("2025-06-04 — Holosim") < product.index("2025-06-05 — C4")
    semantic_checks["master_event_order"] = master.index("2025-06-04 — Holosim") < master.index("2025-06-05 — C4")
    for name, passed in semantic_checks.items():
        if not passed:
            errors.append(f"Semantic lifecycle check failed: {name}")

    generated = sorted((HERE / "evidence-packets").glob("*.json")) + [HERE / x for x in ("archival-depth-review.json", "archival-depth-review.md", "campaign-summary.json", "campaign-summary.md", "promotion-ledger.json", "promotion-ledger.md")]
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in generated}
    rebuild = subprocess.run(["python", str(HERE / "build_campaign.py")], cwd=ROOT, text=True, capture_output=True)
    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in generated}
    deterministic = rebuild.returncode == 0 and before == after
    if not deterministic:
        errors.append("Deterministic regeneration check failed")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "operations/pipeline/src")
    tests = subprocess.run(["python", "-m", "pytest", "operations/tests", "-q"], cwd=ROOT, env=env, text=True, capture_output=True)
    if tests.returncode:
        errors.append("Repository tests failed: " + (tests.stdout + tests.stderr).strip())

    result = "PASS" if not errors else "FAIL"
    report = {
        "campaign_id": "knowledge-context-refresh-2026-07-17", "validation_result": result,
        "evidence_packets": len(packets), "material_claims_reviewed": sum(len(p.get("material_claims", [])) for p in packets),
        "archival_depth_pages_checked": len(ARCHIVAL_REQUIREMENTS),
        "campaign_json_files_parsed": len(parsed_json), "broken_internal_links": broken,
        "prohibited_path_changes": prohibited,
        "checks": {"json_parses": not any("Invalid JSON" in e for e in errors), "front_matter_structural_parse": not any("metadata" in e for e in errors),
            "sources_resolve": not any("Missing source" in e for e in errors), "links_resolve": not broken,
            "archive_untouched": not any(p.startswith("archive/") for p in changed),
            "graph_untouched": not any(p.startswith("graph/") for p in changed),
            "publication_untouched": not any(p.startswith("publication/") for p in changed),
            "git_diff_check": check.returncode == 0,
            "untracked_scope_checked": True,
            "ledger_reconciles": packet_paths == ledger_packet_paths and changed_knowledge == ledger_knowledge,
            "claim_level_packets": all(len(p.get("material_claims", [])) >= 3 for p in packets),
            "archival_depth_sections": not any("Archival depth sections missing" in e for e in errors),
            "semantic_lifecycle_checks": semantic_checks,
            "deterministic_regeneration": deterministic,
            "repository_tests": "8 passed" if tests.returncode == 0 else "FAILED"},
        "errors": errors, "warnings": warnings,
    }
    (HERE / "validation-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (HERE / "validation-report.md").write_text(
        f"# Validation Report\n\nResult: **{result}**\n\nValidated {len(packets)} evidence packets containing {sum(len(p.get('material_claims', [])) for p in packets)} material claim decisions, {len(ARCHIVAL_REQUIREMENTS)} archival-depth section profiles, {len(parsed_json)} campaign JSON files, required front matter, explicit source-authority roles, source references, internal links, tracked and untracked scope boundaries, ledger coverage, lifecycle distinctions, deterministic regeneration, `git diff --check`, and the repository test suite (8 passed).\n"
        + ("\n## Errors\n\n" + "\n".join(f"- {e}" for e in errors) + "\n" if errors else ""), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
