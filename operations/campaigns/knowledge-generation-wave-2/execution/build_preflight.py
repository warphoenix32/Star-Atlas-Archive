"""Build the deterministic Wave 2A preflight inventory from repository state."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

PORTFOLIO = [
    ("knowledge/governance/PIP-Registry.md", "EXPAND", "Wave 2A", "A1/A3"),
    ("knowledge/governance/Star-Atlas-DAO.md", "CREATE", "Wave 2A", "A1"),
    ("knowledge/governance/Star-Atlas-Foundation.md", "CREATE", "Wave 2A", "A1"),
    ("knowledge/governance/Star-Atlas-Council.md", "CREATE", "Wave 2A", "A1/A3"),
    ("knowledge/governance/Ecosystem-Fund.md", "CREATE", "Wave 2A", "A1/A3"),
    ("knowledge/governance/PIP-Lifecycle-and-Legislative-Process.md", "CREATE", "Wave 2A", "A1"),
    ("knowledge/governance/Governance-Implementation-and-Evidence-States.md", "CREATE", "Wave 2A", "A1/A3"),
    ("knowledge/governance/Governance-and-Economy-Overview.md", "EXPAND", "Wave 2A", "A1/A2"),
    ("knowledge/governance/README.md", "EXPAND", "Wave 2A", "A1"),
    ("knowledge/organizations/Institutional-Overview.md", "EXPAND", "Wave 2A", "A1/A2"),
    ("knowledge/organizations/ATMTA.md", "CREATE", "Wave 2A", "A2"),
    ("knowledge/organizations/README.md", "EXPAND", "Wave 2A", "A1/A2"),
    ("knowledge/gameplay/Product-Registry.md", "EXPAND", "Wave 2A", "A2/B1"),
    ("knowledge/gameplay/SCORE-and-Faction-Fleet.md", "CREATE", "Wave 2A", "A2/B2"),
    ("knowledge/gameplay/SAGE.md", "CREATE", "Wave 2A", "A2/B1"),
    ("knowledge/gameplay/UE5-Showroom.md", "CREATE", "Wave 2A", "A2/B1"),
    ("knowledge/gameplay/Galactic-Marketplace.md", "CREATE", "Wave 2A", "A2"),
    ("knowledge/gameplay/README.md", "EXPAND", "Wave 2A", "A2"),
    ("knowledge/media/Official-Discord-Announcements-Profile.md", "DEFER", "PR #15 evidence is unmerged", "unavailable"),
    ("knowledge/media/Official-X-Account-Profile.md", "DEFER", "Page cap; retain for later source-profile wave", "A2 available"),
    ("knowledge/media/Star-Atlas-Medium-Publication-Profile.md", "RESEARCH_ONLY", "Complete article-level corpus review is absent", "partial"),
    ("knowledge/events/README.md", "DEFER", "Foundation portfolio uses the 18-output ceiling", "A2/B2 available"),
]


def main() -> None:
    existing = sorted(
        p.relative_to(ROOT).as_posix() for p in (ROOT / "knowledge").rglob("*") if p.is_file()
    )
    records = []
    for path, action, reason, evidence in PORTFOLIO:
        records.append(
            {
                "proposed_path": path,
                "page_action": action,
                "exists_on_main": path in existing,
                "disposition_reason": reason,
                "evidence_packet_status": "REQUIRED" if reason == "Wave 2A" else "NOT_DRAFTED",
                "evidence_availability": evidence,
            }
        )
    inventory = {
        "campaign_id": "knowledge-generation-wave-2a",
        "inventory_as_of": "2026-07-15",
        "base": "origin/main",
        "existing_knowledge_file_count": len(existing),
        "existing_knowledge_files": existing,
        "proposed_pages": records,
        "wave_2a_output_count": sum(x[2] == "Wave 2A" for x in PORTFOLIO),
        "actions": {a: sum(r["page_action"] == a for r in records) for a in ["CREATE", "EXPAND", "MERGE", "REDIRECT", "DEFER", "RESEARCH_ONLY"]},
    }
    (OUT / "page-inventory.json").write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")

    rows = "\n".join(
        f'| `{r["proposed_path"]}` | {r["page_action"]} | {r["disposition_reason"]} | {r["evidence_availability"]} |'
        for r in records
    )
    (OUT / "page-inventory.md").write_text(
        "# Wave 2A Page Inventory\n\n"
        "Inventory date: 2026-07-15. Base: `origin/main`. The repository contains "
        f"{len(existing)} existing files under `knowledge/`. No page may be drafted until its evidence packet is present.\n\n"
        "| Proposed path | Action | Disposition | Evidence |\n|---|---|---|---|\n"
        + rows
        + "\n\nThe selected portfolio contains 18 outputs: 11 creates and 7 substantive expansions. "
        "DAO, Foundation, and Council remain governance pages; organization indexes link to them instead of duplicating their procedural content.\n",
        encoding="utf-8",
    )

    availability = {
        "as_of": "2026-07-15",
        "available_on_main": [
            {"path": "archive/semantic/governance/pip-registry-semantic.json", "authority": ["A1", "A3"], "use": "33 captured PIPs, vote/result separation, Council-attributed operational fields"},
            {"path": "archive/semantic/governance/pip-source-reconciliation.json", "authority": ["A1", "A3"], "use": "portal and Council reconciliation"},
            {"path": "archive/source-records/social-governance-semantic-enrichment/governance/", "authority": ["A1"], "use": "captured PIP texts and provenance"},
            {"path": "archive/source-records/campaign-delta-official/", "authority": ["A2"], "use": "official product, support, and institutional publications"},
            {"path": "archive/semantic/atlas-brew/", "authority": ["B1", "C1"], "use": "timestamped product discussion; unknown speakers remain unattributed"},
            {"path": "archive/source-records/campaign-alpha-aephia/", "authority": ["B2"], "use": "sourced community chronology used only with attribution"},
            {"path": "knowledge/gameplay/Official-Current-State-Snapshot-2026-07-12.md", "authority": ["A2"], "use": "dated synthesis of captured official product positioning"},
        ],
        "unavailable_or_deferred": [
            {"dependency": "PR #15", "state": "OPEN_DRAFT", "impact": "Official Discord source profile deferred"},
            {"dependency": "complete Medium corpus review", "state": "ABSENT", "impact": "Medium profile remains research-only"},
        ],
        "rule": "No Wave 2A page relies on C1 or C2 evidence alone.",
    }
    (OUT / "evidence-availability.json").write_text(json.dumps(availability, indent=2) + "\n", encoding="utf-8")
    (OUT / "dependency-report.md").write_text(
        "# Wave 2A Dependency Report\n\n"
        "Wave 2A is based directly on `origin/main`. PR #12 and PR #13 are merged and their semantic/governance evidence is available on main. "
        "PR #14 remains a draft planning-only pull request and is not a code dependency. PR #15 remains an open draft and is not imported.\n\n"
        "Consequently, the Official Discord profile is deferred. The selected 18 outputs use only evidence already present on main. "
        "No semantic artifacts were copied from an unmerged branch. The implementation is independently mergeable once human semantic review is complete.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
