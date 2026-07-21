#!/usr/bin/env python3
"""Validate the knowledge baseline inventory and fixed point."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

from build_inventory import ROOT, OUT, build, main as rebuild


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> int:
    inventory_path = OUT / "page-inventory.json"
    markdown_path = OUT / "page-inventory.md"
    before = {path.name: digest(path) for path in (inventory_path, markdown_path)}
    rebuild()
    after = {path.name: digest(path) for path in (inventory_path, markdown_path)}
    payload = json.loads(inventory_path.read_text(encoding="utf-8"))
    actual = sorted(path.relative_to(ROOT).as_posix() for path in (ROOT / "knowledge").rglob("*.md"))
    indexed = sorted(page["path"] for page in payload["pages"])
    changed = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False,
    ).stdout.splitlines()
    checks = {
        "deterministic": before == after,
        "all_pages_indexed_once": actual == indexed and len(indexed) == len(set(indexed)),
        "all_pages_have_revision_action": all(page["recommended_action"] for page in payload["pages"]),
        "all_pages_assigned_to_wave": all(page["revision_wave"] in {1, 2, 3, 4} for page in payload["pages"]),
        "page_count_reconciles": payload["page_count"] == len(actual) == 80,
        "revision_scope_valid": all(
            path.replace("\\", "/").startswith(("knowledge/", "operations/campaigns/knowledge-narrative-depth-001/"))
            for path in changed
        ),
        "git_diff_check": subprocess.run(["git", "diff", "--check"], cwd=ROOT).returncode == 0,
    }
    report = {"campaign_id": payload["campaign_id"], "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "page_count": len(actual)}
    (OUT / "validation-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(run())
