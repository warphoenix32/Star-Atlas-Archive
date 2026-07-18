#!/usr/bin/env python3
"""Run external validation and update the campaign validation report."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from build_index import CAMPAIGN_ID, build, write_outputs


JSON_FILES = (
    "source-inventory.json", "alias-registry.json", "promotion-candidates.json",
    "conflict-report.json", "research-backlog.json", "validation-report.json",
)
JSONL_FILES = ("identity-index.jsonl", "guild-index.jsonl", "relationship-index.jsonl")


def digest_map(directory: Path) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.iterdir()) if path.name in JSON_FILES + JSONL_FILES and path.name != "validation-report.json"
    }


def run(command: list[str], cwd: Path) -> tuple[bool, str]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    detail = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0, detail[-4000:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    campaign_dir = Path(__file__).resolve().parent
    write_outputs(repo_root, campaign_dir)

    parse_errors = []
    for filename in JSON_FILES:
        try:
            json.loads((campaign_dir / filename).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            parse_errors.append(f"{filename}: {error}")
    for filename in JSONL_FILES:
        for number, line in enumerate((campaign_dir / filename).read_text(encoding="utf-8").splitlines(), 1):
            try:
                json.loads(line)
            except json.JSONDecodeError as error:
                parse_errors.append(f"{filename}:{number}: {error}")

    with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
        first_dir, second_dir = Path(first), Path(second)
        write_outputs(repo_root, first_dir)
        write_outputs(repo_root, second_dir)
        deterministic = digest_map(first_dir) == digest_map(second_dir) == digest_map(campaign_dir)

    tests_ok, tests_detail = run([sys.executable, "-m", "pytest", "-q", "operations/tests/discord_community_indexing"], repo_root)
    diff_ok, diff_detail = run(["git", "diff", "--check"], repo_root)
    report_path = campaign_dir / "validation-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["external_validation"] = {
        "json_and_jsonl_parse": {"passed": not parse_errors, "details": parse_errors},
        "regeneration_determinism": {"passed": deterministic, "details": digest_map(campaign_dir)},
        "tests": {"passed": tests_ok, "details": tests_detail},
        "git_diff_check": {"passed": diff_ok, "details": diff_detail},
    }
    internal_ok = all(check["passed"] for check in report["checks"])
    external_ok = all(value["passed"] for value in report["external_validation"].values())
    report["status"] = "pass" if internal_ok and external_ok else "fail"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"campaign_id": CAMPAIGN_ID, "status": report["status"]}, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
