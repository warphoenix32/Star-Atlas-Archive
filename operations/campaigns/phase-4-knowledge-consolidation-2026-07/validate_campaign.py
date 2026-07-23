"""Validate Phase 4 Gate 1 knowledge consolidation."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = Path(__file__).resolve().parent
UPDATED_KNOWLEDGE = [
    "knowledge/Entity-Relationship-Map.md",
    "knowledge/economy/Economic-Report-Catalog.md",
    "knowledge/economy/README.md",
    "knowledge/index/source-registry/Public-Source-Registry.md",
    "knowledge/media/Atlas-Brew-History.md",
    "knowledge/media/Media-and-Creator-Index.md",
    "knowledge/media/README.md",
    "knowledge/media/Star-Atlas-Medium-Publication-Profile.md",
    "knowledge/research/Research-Backlog.md",
    "knowledge/timeline/Official-Communications-Chronology.md",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def changed_paths(base_ref: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode:
        return []
    return [line.replace("\\", "/") for line in result.stdout.splitlines() if line]


def run_validation(base_ref: str = "origin/main") -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    failures: list[str] = []

    json_paths = sorted(CAMPAIGN.rglob("*.json"))
    for path in json_paths:
        try:
            load_json(path)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{path.relative_to(ROOT).as_posix()}: {exc}")
    checks.append({"check": "campaign_json_parse", "status": "PASS" if not failures else "FAIL"})

    inventory = load_json(CAMPAIGN / "corpus-inventory.json")
    knowledge_files = [path for path in (ROOT / "knowledge").rglob("*") if path.is_file()]
    markdown_files = [path for path in knowledge_files if path.suffix.lower() == ".md"]
    json_files = [path for path in knowledge_files if path.suffix.lower() == ".json"]
    inventory_ok = (
        len(knowledge_files) == inventory["knowledge_files"]["total"] == 81
        and len(markdown_files) == inventory["knowledge_files"]["markdown"] == 80
        and len(json_files) == inventory["knowledge_files"]["json"] == 1
    )
    checks.append({"check": "knowledge_inventory", "status": "PASS" if inventory_ok else "FAIL"})
    if not inventory_ok:
        failures.append("knowledge inventory count does not reconcile")

    portfolio = load_json(CAMPAIGN / "dossier-portfolio.json")
    dossiers = portfolio["dossiers"]
    dossier_ids = [item["dossier_id"] for item in dossiers]
    dossier_ok = len(dossiers) == 10 and len(dossier_ids) == len(set(dossier_ids))
    for dossier in dossiers:
        for value in dossier["knowledge_paths"]:
            if not (ROOT / value).is_file():
                dossier_ok = False
                failures.append(f"missing dossier knowledge path: {value}")
    checks.append({"check": "dossier_portfolio", "status": "PASS" if dossier_ok else "FAIL"})
    if not dossier_ok and not any("dossier" in item for item in failures):
        failures.append("dossier portfolio count or identity does not reconcile")

    packet_paths = sorted((CAMPAIGN / "evidence-packets").glob("*.json"))
    packet_ok = len(packet_paths) == 3
    for path in packet_paths:
        packet = load_json(path)
        if packet.get("status") != "REVIEWED_FOR_KNOWLEDGE_UPDATE":
            packet_ok = False
            failures.append(f"{path.name}: packet is not reviewed")
        for source_path in packet.get("source_paths", []):
            if not (ROOT / source_path).exists():
                packet_ok = False
                failures.append(f"{path.name}: missing source path {source_path}")
        for claim in packet.get("material_claims", []):
            if claim.get("allowed") is False and not claim.get("reason"):
                packet_ok = False
                failures.append(f"{path.name}: rejected claim lacks reason")
    checks.append({"check": "evidence_packets", "status": "PASS" if packet_ok else "FAIL"})
    if not packet_ok and not any("packet" in item for item in failures):
        failures.append("expected three reviewed evidence packets")

    pages_ok = True
    for value in UPDATED_KNOWLEDGE:
        path = ROOT / value
        text = path.read_text(encoding="utf-8")
        if not re.search(r"^as_of: 2026-07-23$", text, re.MULTILINE):
            pages_ok = False
            failures.append(f"{value}: as_of is not 2026-07-23")
        if not all(field in text for field in (
            "knowledge_status:",
            "confidence:",
            "evidence_basis:",
            "known_limitations:",
            "research_gaps:",
            "review_after:",
        )):
            pages_ok = False
            failures.append(f"{value}: required knowledge metadata missing")
    checks.append({"check": "updated_knowledge_metadata", "status": "PASS" if pages_ok else "FAIL"})

    corpus_text = "\n".join(
        (ROOT / value).read_text(encoding="utf-8") for value in UPDATED_KNOWLEDGE
    )
    truth_ok = (
        "181 confirmed articles" in corpus_text
        and "216" in corpus_text
        and "124-item public" in corpus_text
        and "17 quarterly" in corpus_text
        and "publication discovery remains incomplete" in corpus_text
        and "live-event" in corpus_text
        and "independently accurate" in corpus_text
    )
    checks.append({"check": "evidence_qualified_wording", "status": "PASS" if truth_ok else "FAIL"})
    if not truth_ok:
        failures.append("updated knowledge does not preserve required qualified wording")

    manifest = load_json(ROOT / "publication/manifests/publication-manifest.json")
    publication_ok = manifest["lifecycle_phase"] == "CONTRACT_ONLY" and manifest["entries"] == []
    checks.append({"check": "publication_gate_preserved", "status": "PASS" if publication_ok else "FAIL"})
    if not publication_ok:
        failures.append("publication manifest changed before Phase 5")

    changes = changed_paths(base_ref)
    forbidden = [
        path
        for path in changes
        if path.startswith(("archive/", "graph/", "publication/"))
    ]
    scope_ok = not forbidden
    checks.append({"check": "protected_paths", "status": "PASS" if scope_ok else "FAIL"})
    if forbidden:
        failures.append("protected path changes: " + ", ".join(forbidden))

    return {
        "campaign_id": "phase-4-knowledge-consolidation-2026-07",
        "as_of": "2026-07-23",
        "status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "metrics": {
            "knowledge_files_inventoried": len(knowledge_files),
            "dossiers_selected": len(dossiers),
            "evidence_packets_completed": len(packet_paths),
            "knowledge_pages_updated": len(UPDATED_KNOWLEDGE),
            "protected_path_changes": len(forbidden),
        },
        "failures": failures,
        "human_adjudication_required": False,
        "next_gate": "Complete the seven remaining dossier evidence packets",
    }


def write_reports(result: dict[str, Any]) -> None:
    (CAMPAIGN / "validation-report.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rows = "\n".join(f"| {item['check']} | {item['status']} |" for item in result["checks"])
    failure_lines = "\n".join(f"- {item}" for item in result["failures"]) or "- None."
    markdown = f"""# Phase 4 Gate 1 Validation

Result: **{result['status']}**

| Check | Status |
| --- | --- |
{rows}

## Metrics

- Knowledge files inventoried: {result['metrics']['knowledge_files_inventoried']}
- Dossiers selected: {result['metrics']['dossiers_selected']}
- Evidence packets complete: {result['metrics']['evidence_packets_completed']}
- Knowledge pages updated: {result['metrics']['knowledge_pages_updated']}
- Protected-path changes: {result['metrics']['protected_path_changes']}

## Failures

{failure_lines}
"""
    (CAMPAIGN / "validation-report.md").write_text(markdown, encoding="utf-8", newline="\n")


def main() -> int:
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    result = run_validation(base_ref)
    write_reports(result)
    print(f"{result['status']} phase-4-knowledge-consolidation-2026-07")
    for failure in result["failures"]:
        print(f"FAIL {failure}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
