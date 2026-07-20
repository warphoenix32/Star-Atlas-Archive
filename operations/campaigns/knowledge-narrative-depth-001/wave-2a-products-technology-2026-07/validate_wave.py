"""Validate knowledge narrative depth Wave 2A."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BUILD = HERE / "build_wave.py"
REQUIRED_METADATA = {"title", "seo_title", "seo_description", "knowledge_status", "as_of", "confidence", "evidence_basis", "known_limitations", "research_gaps", "review_after"}


def sha(path: Path) -> str:
    data = path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)


def metadata(text: str) -> set[str]:
    if not text.startswith("---\n"):
        return set()
    block = text.split("---", 2)[1]
    return {match.group(1) for match in re.finditer(r"^([A-Za-z_][A-Za-z0-9_-]*):", block, re.M)}


def main() -> int:
    errors = []
    inventory = json.loads((HERE / "page-inventory.json").read_text(encoding="utf-8"))
    paths = [ROOT / item["path"] for item in inventory["pages"]]
    generated = sorted(HERE.glob("*.json")) + sorted((HERE / "evidence-packets").glob("*.json"))
    before = {path.relative_to(ROOT).as_posix(): sha(path) for path in generated}
    first = run(sys.executable, BUILD.relative_to(ROOT).as_posix())
    middle = {path.relative_to(ROOT).as_posix(): sha(path) for path in generated}
    second = run(sys.executable, BUILD.relative_to(ROOT).as_posix())
    after = {path.relative_to(ROOT).as_posix(): sha(path) for path in generated}
    checks = {"deterministic_generation": first.returncode == second.returncode == 0 and before == middle == after}

    checks["page_count"] = len(paths) == 11
    checks["pages_exist"] = all(path.is_file() for path in paths)
    checks["required_metadata"] = all(REQUIRED_METADATA <= metadata(path.read_text(encoding="utf-8")) for path in paths)
    checks["review_sections"] = all("## Review status" in path.read_text(encoding="utf-8") for path in paths)
    checks["no_internal_marker_clusters"] = all(not re.search(r"\[(?:EV|CONF|TIME|PUB)-", path.read_text(encoding="utf-8")) for path in paths)
    checks["packets_reconcile"] = len(list((HERE / "evidence-packets").glob("*.json"))) == 11

    link_errors = []
    for path in paths:
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#")):
                continue
            clean = target.split("#", 1)[0]
            if clean and not (path.parent / clean).resolve().exists():
                link_errors.append(f"{path.relative_to(ROOT)} -> {target}")
    checks["internal_links"] = not link_errors

    source_errors = []
    for packet_path in (HERE / "evidence-packets").glob("*.json"):
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        for claim in packet["material_claims"]:
            for source in claim["supporting_sources"]:
                if not (ROOT / source).exists():
                    source_errors.append(f"{packet_path.name} -> {source}")
    checks["evidence_references"] = not source_errors
    checks["risk_distribution"] = sum(1 for item in inventory["pages"] if item["risk_class"] in {"R1", "R2"}) == 11

    changed = set(run("git", "diff", "--name-only", "origin/main...HEAD").stdout.splitlines())
    changed.update(run("git", "diff", "--name-only").stdout.splitlines())
    forbidden = sorted(path for path in changed if path.startswith(("archive/", "graph/", "publication/")))
    checks["scope"] = not forbidden
    checks["git_diff_check"] = run("git", "diff", "--check").returncode == 0

    for name, passed in checks.items():
        if not passed:
            errors.append(f"failed check: {name}")
    errors.extend(link_errors)
    errors.extend(source_errors)
    status = "PASS" if not errors else "FAIL"
    report = {"campaign_id": "knowledge-narrative-depth-wave-2a-products-technology-2026-07", "status": status, "checks": checks, "errors": errors}
    (HERE / "validation-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (HERE / "validation-report.md").write_text("\n".join(["# Wave 2A Validation", "", f"**Result:** `{status}`", "", *[f"- {'PASS' if value else 'FAIL'}: {name}" for name, value in checks.items()], "", "## Errors", "", *([f"- {item}" for item in errors] if errors else ["- None."]), ""]), encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
