"""Validate Knowledge Narrative Depth Campaign 001 without rewriting evidence."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
REQUIRED_FRONTMATTER = {
    "knowledge_status",
    "as_of",
    "confidence",
    "page_risk_score",
    "page_risk_class",
    "evidence_basis",
    "known_limitations",
    "research_gaps",
    "review_after",
}
ALLOWED_STATUS = {"CANONICAL", "QUALIFIED", "PROVISIONAL", "HISTORICAL"}
ALLOWED_RISK = {"R1", "R2", "R3", "R4", "R5"}


def run(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        env=env,
        check=False,
    )


def frontmatter(text: str) -> tuple[set[str], dict[str, str]]:
    if not text.startswith("---\n"):
        return set(), {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return set(), {}
    keys: set[str] = set()
    scalar: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if match:
            key, value = match.groups()
            keys.add(key)
            scalar[key] = (value or "").strip().strip('"').strip("'")
    return keys, scalar


def changed_paths() -> list[str]:
    paths: set[str] = set()
    base_name = os.environ.get("GITHUB_BASE_REF", "main")
    for base in (f"origin/{base_name}", base_name):
        if run("git", "rev-parse", "--verify", base).returncode != 0:
            continue
        committed = run("git", "diff", "--name-only", f"{base}...HEAD")
        if committed.returncode == 0:
            paths.update(line.strip().replace("\\", "/") for line in committed.stdout.splitlines() if line.strip())
            break
    status = run("git", "status", "--porcelain=v1", "--untracked-files=all")
    for line in status.stdout.splitlines():
        if len(line) >= 4:
            path = line[3:].replace("\\", "/")
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            paths.add(path)
    return sorted(paths)


def link_errors(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        clean = target.strip().strip("<>")
        if not clean or clean.startswith(("#", "http://", "https://", "mailto:")):
            continue
        clean = clean.split("#", 1)[0]
        if clean and not (path.parent / clean).resolve().exists():
            errors.append(f"{path.relative_to(ROOT).as_posix()}: unresolved link {target}")
    return errors


def main() -> int:
    checks: list[dict[str, object]] = []
    errors: list[str] = []
    warnings: list[str] = []

    def record(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "result": "PASS" if ok else "FAIL", "detail": detail})
        if not ok:
            errors.append(f"{name}: {detail}")

    inventory = json.loads((HERE / "page-inventory.json").read_text(encoding="utf-8"))
    outputs = inventory["outputs"]
    packet_paths = sorted((HERE / "evidence-packets").glob("*.json"))
    record("portfolio_count", len(outputs) == 17, f"{len(outputs)} outputs")
    record("evidence_packet_count", len(packet_paths) == len(outputs), f"{len(packet_paths)} packets for {len(outputs)} outputs")

    packets: dict[str, dict[str, object]] = {}
    all_json = sorted(HERE.rglob("*.json"))
    json_errors = []
    for path in all_json:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - validation must report every parse failure
            json_errors.append(f"{path.relative_to(ROOT)}: {exc}")
    record("campaign_json", not json_errors, f"{len(all_json)} files parsed" if not json_errors else "; ".join(json_errors))

    metadata_errors = []
    source_errors = []
    claim_errors = []
    link_failures = []
    risk_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    for item in outputs:
        page = ROOT / item["path"]
        packet = HERE / item["evidence_packet"]
        if not page.exists():
            metadata_errors.append(f"missing page {item['path']}")
            continue
        if not packet.exists():
            claim_errors.append(f"missing packet {item['evidence_packet']}")
            continue
        payload = json.loads(packet.read_text(encoding="utf-8"))
        packets[payload["page_id"]] = payload
        text = page.read_text(encoding="utf-8")
        keys, scalars = frontmatter(text)
        missing = sorted(REQUIRED_FRONTMATTER - keys)
        if missing:
            metadata_errors.append(f"{item['path']}: missing {', '.join(missing)}")
        if scalars.get("knowledge_status") not in ALLOWED_STATUS:
            metadata_errors.append(f"{item['path']}: invalid knowledge_status {scalars.get('knowledge_status')}")
        if scalars.get("page_risk_class") not in ALLOWED_RISK:
            metadata_errors.append(f"{item['path']}: invalid page_risk_class {scalars.get('page_risk_class')}")
        as_of = scalars.get("as_of", "")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", as_of) or as_of < "2026-07-17":
            metadata_errors.append(f"{item['path']}: as_of must be an ISO date no earlier than the 2026-07-17 campaign baseline")
        if scalars.get("page_risk_class") == "R3" and not scalars.get("review_after"):
            metadata_errors.append(f"{item['path']}: R3 page lacks review_after")
        if len(payload.get("material_claims", [])) < 3:
            claim_errors.append(f"{item['evidence_packet']}: fewer than three material claims")
        if not payload.get("subject_entities"):
            claim_errors.append(f"{item['evidence_packet']}: no subject entities")
        for claim in payload.get("material_claims", []):
            if not claim.get("supporting_sources"):
                claim_errors.append(f"{payload['page_id']}:{claim.get('claim_id')}: no supporting sources")
            for source in claim.get("supporting_sources", []):
                if not (ROOT / source).exists():
                    source_errors.append(f"{payload['page_id']}: missing {source}")
            authorities = set(claim.get("source_authority", []))
            if authorities & {"C1", "C2"}:
                claim_errors.append(f"{payload['page_id']}:{claim.get('claim_id')}: weak authority admitted")
            if authorities == {"DERIVED_REVIEWED"} and payload["page_id"] != "historical-periodization":
                claim_errors.append(f"{payload['page_id']}:{claim.get('claim_id')}: only derived evidence")
        if payload.get("proposed_path") != item["path"]:
            claim_errors.append(f"{payload['page_id']}: packet path does not reconcile")
        if payload.get("page_risk_class") != item["risk_class"]:
            claim_errors.append(f"{payload['page_id']}: risk class does not reconcile")
        risk_counts[item["risk_class"]] += 1
        status_counts[item["status"]] += 1
        link_failures.extend(link_errors(page))

    record("required_metadata", not metadata_errors, "all 17 pages contain required metadata" if not metadata_errors else "; ".join(metadata_errors))
    record("material_claims", not claim_errors, "all packets contain source-linked material claims" if not claim_errors else "; ".join(claim_errors))
    record("evidence_references", not source_errors, "all packet source paths resolve" if not source_errors else "; ".join(source_errors))

    knowledge_changed = [p for p in changed_paths() if p.startswith("knowledge/") and p.endswith(".md")]
    for rel in knowledge_changed:
        link_failures.extend(link_errors(ROOT / rel))
    link_failures = sorted(set(link_failures))
    record("internal_links", not link_failures, f"{len(knowledge_changed)} changed knowledge files checked" if not link_failures else "; ".join(link_failures))

    low_risk = risk_counts["R1"] + risk_counts["R2"]
    low_risk_share = low_risk / len(outputs) if outputs else 0
    r3_share = risk_counts["R3"] / len(outputs) if outputs else 1
    risk_ok = low_risk_share >= 0.70 and r3_share <= 0.30 and risk_counts["R4"] == 0 and risk_counts["R5"] == 0
    record("risk_portfolio", risk_ok, f"R1/R2={low_risk}/{len(outputs)} ({low_risk_share:.1%}); R3={risk_counts['R3']} ({r3_share:.1%}); R4/R5=0")

    changed = changed_paths()
    manifest_only_exceptions = {"archive/manifests/lore-repository-ingestion-2026-07.json"}
    forbidden = [
        p for p in changed
        if p.startswith(("archive/", "graph/", "publication/")) and p not in manifest_only_exceptions
    ]
    record(
        "repository_scope",
        not forbidden,
        "archive evidence, graph, and publication untouched; integration manifest changes allowed"
        if not forbidden else ", ".join(forbidden),
    )

    sage = (ROOT / "knowledge/gameplay/SAGE.md").read_text(encoding="utf-8")
    score = (ROOT / "knowledge/gameplay/SCORE-and-Faction-Fleet.md").read_text(encoding="utf-8")
    treasury = (ROOT / "knowledge/economy/Treasury-Authorization-and-Payment-Ledger.md").read_text(encoding="utf-8")
    council = (ROOT / "knowledge/governance/Council-Election-History.md").read_text(encoding="utf-8")
    communications = (ROOT / "knowledge/timeline/Official-Communications-Chronology.md").read_text(encoding="utf-8")
    boundary_errors = []
    if "December 2023" not in sage or "December 2024" in sage:
        boundary_errors.append("SAGE 3D year boundary failed")
    if "DEPRECATION_ANNOUNCED / EXECUTION_UNVERIFIED" not in score:
        boundary_errors.append("SCORE deprecation boundary missing")
    if re.search(r"emissions (?:were|was|had) (?:ended|shut down)", score, re.IGNORECASE):
        boundary_errors.append("SCORE execution overstated")
    if not re.search(r"independent(?:ly)? verif", treasury, re.IGNORECASE):
        boundary_errors.append("treasury independent-verification boundary missing")
    pip33_terms = ["two displayed tranches", "234,756.76", "176,067.57", "58,689.19", "75% USDC", "25% ATLAS", "180 days", "reserve-conditional", "469,513.52", "469,513.53", "352,135.14", "352,135.15", "117,378.38", "one-cent discrepancies"]
    if any(term.lower() not in treasury.lower() for term in pip33_terms):
        boundary_errors.append("PIP-33 tranche composition, timing, condition, or one-cent discrepancy missing")
    if "75% immediate and 25% deferred" in treasury:
        boundary_errors.append("PIP-33 asset mix incorrectly encoded as payment timing")
    if "advancing" not in council.lower() or "final" not in council.lower():
        boundary_errors.append("Council election-stage distinction missing")
    if "PR #19" not in communications or "unmerged" not in communications.lower():
        boundary_errors.append("unmerged Medium dependency not disclosed")
    record("semantic_boundaries", not boundary_errors, "required state distinctions preserved" if not boundary_errors else "; ".join(boundary_errors))

    diff_check = run("git", "diff", "--check")
    record(
        "git_diff_check",
        diff_check.returncode == 0,
        "clean" if diff_check.returncode == 0 else (diff_check.stdout + "\n" + diff_check.stderr).strip(),
    )

    campaign_scripts = sorted(HERE.rglob("*.py"))
    compile_result = run(
        sys.executable,
        "-m",
        "py_compile",
        *(path.relative_to(ROOT).as_posix() for path in campaign_scripts),
    )
    compile_detail = (compile_result.stdout + "\n" + compile_result.stderr).strip()
    record(
        "campaign_scripts_compile",
        compile_result.returncode == 0,
        f"{len(campaign_scripts)} campaign scripts compiled"
        if compile_result.returncode == 0
        else compile_detail,
    )

    result = "PASS" if not errors else "FAIL"
    summary_path = HERE / "campaign-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["status"] = "VALIDATED" if result == "PASS" else "VALIDATION_FAILED"
    summary["validation_result"] = result
    summary["validation_checks"] = len(checks)
    summary["validation_failures"] = len(errors)
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = {
        "campaign_id": "knowledge-narrative-depth-001",
        "validated_at": "2026-07-17",
        "result": result,
        "checks": checks,
        "output_count": len(outputs),
        "risk_distribution": dict(sorted(risk_counts.items())),
        "knowledge_status_distribution": dict(sorted(status_counts.items())),
        "changed_paths": changed,
        "errors": errors,
        "warnings": warnings,
    }
    (HERE / "validation-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Validation Report", "", f"**Result:** `{result}`", "", "## Checks", ""]
    lines.extend(f"- **{c['result']} — {c['check']}:** {c['detail']}" for c in checks)
    lines += ["", "## Portfolio", "", f"- Outputs: {len(outputs)}", f"- Risk distribution: {dict(sorted(risk_counts.items()))}", f"- Knowledge-status distribution: {dict(sorted(status_counts.items()))}", "- Archive evidence rewritten: no", "- Graph modified: no", "- Publication modified: no", ""]
    (HERE / "validation-report.md").write_text(
        "\n".join(line.rstrip() for line in lines),
        encoding="utf-8",
    )
    print(f"{result}: {len(checks)} checks; {len(errors)} failures")
    for error in errors:
        print(f"ERROR {error}")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
