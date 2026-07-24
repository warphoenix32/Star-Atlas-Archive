"""Validate the Phase 5 Knowledge readiness wave."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

from build_campaign import HERE, PAGES, ROOT, frontmatter


LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REQUIRED = {
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
ALLOWED_RISK = {"R1", "R2", "R3"}


def resolve_link(page: Path, raw: str) -> Path | None:
    target = unquote(raw.split("#", 1)[0].strip())
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    return (page.parent / target).resolve()


def main() -> int:
    subprocess.run([sys.executable, str(HERE / "build_campaign.py")], cwd=ROOT, check=True)
    failures: list[str] = []
    summary = json.loads((HERE / "campaign-summary.json").read_text(encoding="utf-8"))
    if summary["planned_gap_count"] != 13 or len(summary["outputs"]) != 13:
        failures.append("portfolio must reconcile exactly 13 approved Phase 5 gaps")
    if {item["plan_id"] for item in summary["outputs"]} != {item[0] for item in PAGES}:
        failures.append("summary plan IDs do not reconcile with the fixed portfolio")

    for plan_id, rel, _ in PAGES:
        page = ROOT / rel
        if not page.is_file():
            failures.append(f"{plan_id}: missing {rel}")
            continue
        meta = frontmatter(page)
        missing = sorted(REQUIRED - set(meta))
        if missing:
            failures.append(f"{rel}: missing metadata {missing}")
            continue
        if meta["knowledge_status"] not in ALLOWED_STATUS:
            failures.append(f"{rel}: invalid knowledge status")
        if meta["page_risk_class"] not in ALLOWED_RISK:
            failures.append(f"{rel}: invalid or prohibited risk class")
        if not meta["known_limitations"] or not meta["research_gaps"]:
            failures.append(f"{rel}: limitations and research gaps are required")
        for source in meta["evidence_basis"]:
            if not (ROOT / source).exists():
                failures.append(f"{rel}: missing evidence path {source}")
        text = page.read_text(encoding="utf-8")
        if len(text.split()) < 350:
            failures.append(f"{rel}: narrative is too thin for a Knowledge dossier")
        for raw in LINK_RE.findall(text):
            target = resolve_link(page, raw)
            if target is not None and not target.exists():
                failures.append(f"{rel}: broken link {raw}")

    packet_count = len(list((HERE / "evidence-packets").glob("*.json")))
    if packet_count != 13:
        failures.append(f"expected 13 evidence packets, found {packet_count}")

    changed = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    forbidden = [
        path for path in changed
        if path.startswith(("archive/", "graph/", "publication/"))
    ]
    if forbidden:
        failures.append("forbidden evidence or publication paths changed: " + ", ".join(forbidden))

    result = "PASS" if not failures else "FAIL"
    report = {
        "campaign_id": "phase-5-knowledge-readiness-2026-07",
        "validated_at": "2026-07-23",
        "result": result,
        "checks": {
            "portfolio_reconciles": len(summary["outputs"]) == 13,
            "evidence_packets": packet_count,
            "metadata_and_links": "PASS" if not failures else "SEE_FAILURES",
            "forbidden_paths": forbidden,
        },
        "failures": failures,
        "human_semantic_review_required": True,
    }
    (HERE / "validation-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    lines = [
        "# Phase 5 Knowledge Readiness Validation",
        "",
        f"**Result:** `{result}`",
        "",
        f"- Knowledge dossiers: {len(summary['outputs'])}",
        f"- Evidence packets: {packet_count}",
        f"- Forbidden paths changed: {len(forbidden)}",
        "- Human semantic review required: yes",
        "",
        "## Failures",
        "",
    ]
    lines.extend(f"- {failure}" for failure in failures)
    if not failures:
        lines.append("- None.")
    (HERE / "validation-report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"{result} phase-5-knowledge-readiness-2026-07")
    for failure in failures:
        print(f"FAIL {failure}")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
