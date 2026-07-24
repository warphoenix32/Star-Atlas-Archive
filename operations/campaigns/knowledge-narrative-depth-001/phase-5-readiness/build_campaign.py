"""Build deterministic evidence packets for the Phase 5 Knowledge readiness wave."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PACKETS = HERE / "evidence-packets"
AS_OF = "2026-07-23"
PROMOTION_STATE = "HUMAN_SEMANTIC_REVIEW_APPROVED"

PAGES = [
    ("PLAN-001", "knowledge/Star-Atlas-Identity-and-Scope.md", "CREATE"),
    ("PLAN-004", "knowledge/timeline/Turning-Points-in-Star-Atlas-History.md", "CREATE"),
    ("PLAN-018", "knowledge/gameplay/Ship-and-Manufacturer-Registry.md", "CREATE"),
    ("PLAN-020", "knowledge/economy/Player-Economy-History.md", "CREATE"),
    ("PLAN-024", "knowledge/guilds/Guild-and-DAC-History.md", "CREATE"),
    ("PLAN-016", "knowledge/gameplay/Escape-Velocity.md", "CREATE"),
    ("PLAN-021", "knowledge/economy/Resource-Mining-Crafting-and-Trade.md", "CREATE"),
    ("PLAN-010", "knowledge/lore/Powers-and-Organizations-of-Galia.md", "CREATE"),
    ("PLAN-027", "knowledge/events/Community-Events-and-Traditions.md", "CREATE"),
    ("PLAN-022", "knowledge/economy/Ships-Assets-and-Ownership.md", "CREATE"),
    ("PLAN-011", "knowledge/lore/Lore-and-Canon-Publication-History.md", "CREATE"),
    ("PLAN-029", "knowledge/governance/Proposal-Impact-Casebook.md", "CREATE"),
    ("PLAN-030", "knowledge/technology/Reader-Technology-and-Program-Registry.md", "CREATE"),
]

FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def frontmatter(path: Path) -> dict[str, object]:
    match = FRONT_RE.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"missing front matter: {path}")
    data: dict[str, object] = {}
    current_list: str | None = None
    for raw in match.group(1).splitlines():
        if raw.startswith("  - ") and current_list:
            value = raw[4:].strip().strip('"')
            cast = data.setdefault(current_list, [])
            assert isinstance(cast, list)
            cast.append(value)
            continue
        if ":" not in raw or raw.startswith(" "):
            continue
        key, value = raw.split(":", 1)
        value = value.strip().strip('"')
        if value:
            if value.isdigit():
                data[key] = int(value)
            else:
                data[key] = value
            current_list = None
        else:
            data[key] = []
            current_list = key
    return data


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    PACKETS.mkdir(parents=True, exist_ok=True)
    expected = set()
    outputs = []
    for plan_id, rel, action in PAGES:
        page = ROOT / rel
        meta = frontmatter(page)
        packet_name = f"{plan_id.lower()}-{page.stem.lower()}.json"
        expected.add(packet_name)
        packet = {
            "packet_schema": "phase5-knowledge-readiness-v1",
            "plan_id": plan_id,
            "page_path": rel,
            "page_action": action,
            "knowledge_status": meta["knowledge_status"],
            "as_of": meta["as_of"],
            "confidence": meta["confidence"],
            "risk_score": meta["page_risk_score"],
            "risk_class": meta["page_risk_class"],
            "evidence_basis": meta["evidence_basis"],
            "known_limitations": meta["known_limitations"],
            "research_gaps": meta["research_gaps"],
            "review_after": meta["review_after"],
            "promotion_state": PROMOTION_STATE,
            "archive_evidence_modified": False,
            "graph_modified": False,
            "publication_modified": False,
        }
        write_json(PACKETS / packet_name, packet)
        outputs.append(
            {
                "plan_id": plan_id,
                "page_path": rel,
                "evidence_packet": f"evidence-packets/{packet_name}",
                "promotion_state": packet["promotion_state"],
                "risk_class": packet["risk_class"],
                "knowledge_status": packet["knowledge_status"],
            }
        )

    for stale in PACKETS.glob("*.json"):
        if stale.name not in expected:
            stale.unlink()

    risk = Counter(item["risk_class"] for item in outputs)
    status = Counter(item["knowledge_status"] for item in outputs)
    summary = {
        "campaign_id": "phase-5-knowledge-readiness-2026-07",
        "as_of": AS_OF,
        "status": "READY_FOR_MERGE",
        "planned_gap_count": 13,
        "knowledge_pages_created": len(outputs),
        "promotion_state": PROMOTION_STATE,
        "human_semantic_review_completed": True,
        "human_adjudications": [
            "PH5-ADJ-001_MANUFACTURER_FAMILIES",
            "PH5-ADJ-002_FTX_CORROBORATION",
            "PH5-ADJ-003_CURRENT_MEMBERSHIP_INFERENCE",
            "PH5-ADJ-004_LORE_SNAPSHOT_TREATMENT",
        ],
        "risk_distribution": dict(sorted(risk.items())),
        "knowledge_status_distribution": dict(sorted(status.items())),
        "outputs": outputs,
        "archive_evidence_modified": False,
        "graph_modified": False,
        "publication_modified": False,
    }
    write_json(HERE / "campaign-summary.json", summary)

    lines = [
        "# Phase 5 Knowledge Readiness Summary",
        "",
        f"- Targeted gaps: {summary['planned_gap_count']}",
        f"- Knowledge dossiers created: {summary['knowledge_pages_created']}",
        f"- Risk distribution: `{json.dumps(summary['risk_distribution'], sort_keys=True)}`",
        f"- Status distribution: `{json.dumps(summary['knowledge_status_distribution'], sort_keys=True)}`",
        "- Human semantic review: complete",
        f"- Human adjudications incorporated: {len(summary['human_adjudications'])}",
        "- Archive evidence modified: no",
        "- Graph modified: no",
        "- Publication modified: no",
        "",
        "## Outputs",
        "",
    ]
    lines.extend(
        f"- `{item['plan_id']}` - [{Path(item['page_path']).stem.replace('-', ' ')}]"
        f"(../../../../{item['page_path']}) - `{item['promotion_state']}`"
        for item in outputs
    )
    lines += [
        "",
        "## Gate",
        "",
        "Human semantic review is complete. The four recorded adjudications are incorporated, and the dossiers are approved as future publication inputs.",
        "",
    ]
    (HERE / "campaign-summary.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )
    print(f"BUILT {len(outputs)} Phase 5 Knowledge readiness dossiers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
