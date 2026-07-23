"""Validate the frozen Phase 2 freshness closeout artifacts offline."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, detail: object) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    filenames = [
        "discovery-snapshot.json",
        "discovery-candidate-queue.json",
        "artifact-blocked-carry-forward.json",
        "campaign-summary.json",
    ]
    parsed: dict[str, dict] = {}
    errors: list[str] = []
    for name in filenames:
        try:
            parsed[name] = load(name)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {exc}")
    check("json_parses", not errors, errors)

    snapshot = parsed.get("discovery-snapshot.json", {})
    surfaces = snapshot.get("surfaces", [])
    expected_surfaces = {
        "OFFICIAL-NEWSROOM",
        "OFFICIAL-SUPPORT",
        "OFFICIAL-GOVERNANCE",
        "OFFICIAL-MEDIUM",
        "OFFICIAL-X",
        "OFFICIAL-DISCORD",
        "OFFICIAL-GITHUB",
    }
    check(
        "required_surfaces_checked",
        {row.get("surface_id") for row in surfaces} == expected_surfaces,
        [row.get("surface_id") for row in surfaces],
    )

    queue = parsed.get("discovery-candidate-queue.json", {})
    candidates = queue.get("candidates", [])
    ids = [row.get("candidate_id") for row in candidates]
    urls = [row.get("url") for row in candidates]
    check("candidate_count_reconciles", queue.get("candidate_count") == len(candidates) == 10, len(candidates))
    check("candidate_ids_unique", len(ids) == len(set(ids)) and all(ids), ids)
    check("candidate_urls_unique", len(urls) == len(set(urls)) and all(urls), urls)
    check(
        "candidate_dispositions_terminal_for_gate",
        all(row.get("disposition") == "PENDING_PHASE_3_ACQUISITION" for row in candidates),
        sorted({row.get("disposition") for row in candidates}),
    )

    carry = parsed.get("artifact-blocked-carry-forward.json", {})
    carry_items = carry.get("items", [])
    check(
        "artifact_gaps_carried_without_false_completion",
        len(carry_items) == 5
        and carry.get("phase_2_blocking_count") == 0
        and all(row.get("status") == "DEFERRED_MISSING_OPERATOR_ARTIFACT" for row in carry_items)
        and all(row.get("phase_3_effect") == "NON_BLOCKING" for row in carry_items),
        carry_items,
    )

    summary = parsed.get("campaign-summary.json", {})
    check(
        "summary_reconciles",
        summary.get("surfaces_checked") == len(surfaces)
        and summary.get("candidates_queued") == len(candidates)
        and summary.get("artifact_blocked_items_carried_forward") == len(carry_items)
        and summary.get("status") == "PHASE_2_GATE_COMPLETE",
        summary,
    )
    check(
        "scope_boundaries",
        summary.get("ingestion_performed") is False
        and summary.get("archive_evidence_modified") is False
        and summary.get("knowledge_modified") is False
        and summary.get("graph_modified") is False
        and summary.get("publication_modified") is False,
        {
            key: summary.get(key)
            for key in [
                "ingestion_performed",
                "archive_evidence_modified",
                "knowledge_modified",
                "graph_modified",
                "publication_modified",
            ]
        },
    )

    passed = all(row["passed"] for row in checks)
    report = {
        "schema_version": "1.0.0",
        "campaign_id": "phase-2-official-freshness-closeout-2026-07",
        "result": "PASS" if passed else "FAIL",
        "checks": checks,
    }
    (HERE / "validation-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 2 Official Freshness Closeout Validation",
        "",
        f"**Result:** `{report['result']}`",
        "",
    ]
    lines.extend(
        f"- **{'PASS' if row['passed'] else 'FAIL'} — {row['name']}:** {row['detail']}"
        for row in checks
    )
    (HERE / "validation-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{report['result']}: {sum(row['passed'] for row in checks)}/{len(checks)} checks")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
