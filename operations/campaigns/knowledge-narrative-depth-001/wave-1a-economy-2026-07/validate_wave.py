"""Validate Economy Wave 1A and write deterministic validation reports."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
GENERATOR = HERE / "build_wave.py"
REQUIRED_KEYS = {
    "title", "seo_title", "seo_description", "knowledge_status", "as_of", "confidence",
    "page_risk_score", "page_risk_class", "evidence_basis", "known_limitations",
    "research_gaps", "review_after",
}


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metadata_keys(text: str) -> set[str]:
    if not text.startswith("---\n"):
        return set()
    end = text.find("\n---\n", 4)
    if end < 0:
        return set()
    return {match.group(1) for match in re.finditer(r"^([A-Za-z_][A-Za-z0-9_-]*):", text[4:end], re.MULTILINE)}


def link_errors(path: Path) -> list[str]:
    errors: list[str] = []
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        clean = target.strip().strip("<>")
        if not clean or clean.startswith(("#", "http://", "https://", "mailto:")):
            continue
        clean = clean.split("#", 1)[0]
        if clean and not (path.parent / clean).resolve().exists():
            errors.append(f"{path.relative_to(ROOT).as_posix()}: unresolved link {target}")
    return errors


def main() -> int:
    inventory = json.loads((HERE / "page-inventory.json").read_text(encoding="utf-8"))
    pages = inventory["pages"]
    errors: list[str] = []
    checks: dict[str, object] = {}

    generated = sorted(HERE.glob("*.json")) + sorted((HERE / "evidence-packets").glob("*.json"))
    generated = [path for path in generated if path.name != "validation-report.json"]
    generated.append(HERE / "campaign-summary.md")
    before = {path.relative_to(ROOT).as_posix(): sha256(path) for path in generated}
    regen = run(sys.executable, GENERATOR.relative_to(ROOT).as_posix())
    after = {path.relative_to(ROOT).as_posix(): sha256(path) for path in generated}
    checks["deterministic_generation"] = regen.returncode == 0 and before == after
    if not checks["deterministic_generation"]:
        errors.append("generated artifacts are not byte-deterministic")

    metadata_failures: list[str] = []
    source_failures: list[str] = []
    links: list[str] = []
    narrative_failures: list[str] = []
    for item in pages:
        page = ROOT / item["path"]
        packet = ROOT / item["evidence_packet"]
        if not page.exists() or not packet.exists():
            errors.append(f"missing page or packet for {item['page_id']}")
            continue
        text = page.read_text(encoding="utf-8")
        missing = sorted(REQUIRED_KEYS - metadata_keys(text))
        if missing:
            metadata_failures.append(f"{item['path']}: {', '.join(missing)}")
        word_count = len(re.findall(r"\b[\w'-]+\b", re.sub(r"^---.*?---", "", text, flags=re.DOTALL)))
        section_count = len(re.findall(r"^## ", text, re.MULTILINE))
        if word_count < 500 or section_count < 4:
            narrative_failures.append(f"{item['path']}: {word_count} words, {section_count} sections")
        payload = json.loads(packet.read_text(encoding="utf-8"))
        if payload["proposed_path"] != item["path"] or len(payload["material_claims"]) < 3:
            errors.append(f"evidence packet does not reconcile for {item['page_id']}")
        for claim in payload["material_claims"]:
            for source in claim["supporting_sources"]:
                if not (ROOT / source).exists():
                    source_failures.append(f"{item['page_id']}: {source}")
        links.extend(link_errors(page))

    checks["page_count"] = len(pages) == 7
    checks["required_metadata"] = not metadata_failures
    checks["narrative_depth"] = not narrative_failures
    checks["evidence_paths_resolve"] = not source_failures
    checks["internal_links_resolve"] = not links
    if not checks["page_count"]: errors.append(f"expected 7 pages, found {len(pages)}")
    if metadata_failures: errors.extend(metadata_failures)
    if narrative_failures: errors.extend(narrative_failures)
    if source_failures: errors.extend(source_failures)
    if links: errors.extend(links)

    pvp = (ROOT / "knowledge/economy/PVP-Voting-Power.md").read_text(encoding="utf-8")
    ledger = (ROOT / "knowledge/economy/Treasury-Authorization-and-Payment-Ledger.md").read_text(encoding="utf-8")
    boundary_terms = ["220 effective wallets", "87.25894%", "no payment or implementation evidence"]
    checks["pip33_vote_boundary"] = all(term.lower() in (pvp + ledger).lower() for term in boundary_terms) and "PAYMENT_UNVERIFIED" in ledger
    if not checks["pip33_vote_boundary"]:
        errors.append("PIP-33 vote/payment boundary is incomplete")

    scope = run("git", "diff", "--name-only", "origin/main...HEAD")
    changed = [line.strip().replace("\\", "/") for line in scope.stdout.splitlines() if line.strip()]
    forbidden = [path for path in changed if path.startswith(("archive/", "graph/", "publication/"))]
    checks["repository_scope"] = not forbidden
    if forbidden: errors.append("forbidden paths changed: " + ", ".join(forbidden))
    diff_check = run("git", "diff", "--check")
    checks["git_diff_check"] = diff_check.returncode == 0
    if diff_check.returncode: errors.append(diff_check.stdout.strip())

    status = "PASS" if not errors else "FAIL"
    report = {"campaign_id": inventory["campaign_id"], "status": status, "checks": checks, "errors": errors}
    (HERE / "validation-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Economy Wave 1A Validation", "", f"**Result:** `{status}`", "", "## Checks", ""]
    lines.extend(f"- **{'PASS' if value else 'FAIL'} — {name}:** {value}" for name, value in checks.items())
    lines += ["", "## Errors", ""] + ([f"- {error}" for error in errors] if errors else ["- None."])
    (HERE / "validation-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
