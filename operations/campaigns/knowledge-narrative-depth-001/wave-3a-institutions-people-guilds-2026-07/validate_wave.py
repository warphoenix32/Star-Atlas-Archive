"""Validate Knowledge Narrative Depth Wave 3A."""
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
REQUIRED = {
    "title", "seo_title", "seo_description", "knowledge_status", "as_of", "confidence",
    "evidence_basis", "known_limitations", "research_gaps", "review_after",
}


def sha(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(text.encode()).hexdigest()


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)


def metadata_keys(text: str) -> set[str]:
    if not text.startswith("---\n"):
        return set()
    return set(re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):", text.split("---", 2)[1], re.MULTILINE))


def main() -> int:
    errors: list[str] = []
    inventory = json.loads((HERE / "page-inventory.json").read_text(encoding="utf-8"))
    pages = [ROOT / item["path"] for item in inventory["pages"]]
    generated = sorted(HERE.glob("*.json")) + sorted((HERE / "evidence-packets").glob("*.json"))
    before = {str(path): sha(path) for path in generated}
    first = run(sys.executable, str(BUILD))
    middle = {str(path): sha(path) for path in generated}
    second = run(sys.executable, str(BUILD))
    after = {str(path): sha(path) for path in generated}
    packets = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((HERE / "evidence-packets").glob("*.json"))]

    checks = {
        "deterministic_generation": first.returncode == second.returncode == 0 and before == middle == after,
        "page_count": len(pages) == 9,
        "required_metadata": all(REQUIRED <= metadata_keys(path.read_text(encoding="utf-8")) for path in pages),
        "review_sections": all("## Review status" in path.read_text(encoding="utf-8") for path in pages),
        "packet_count": len(packets) == 9,
        "source_linked_packets": all(packet.get("material_claims") and all(claim.get("supporting_sources") for claim in packet["material_claims"]) for packet in packets),
        "operator_boundary": "operator-confirmed" in (ROOT / "knowledge/guilds/Guild-Master-Index.md").read_text(encoding="utf-8").lower(),
        "unknown_speaker_boundary": "does not erase the historical value" in (ROOT / "knowledge/people/Actor-Master-Index.md").read_text(encoding="utf-8"),
    }

    broken: list[str] = []
    for page in pages:
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", page.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#")):
                continue
            clean = target.split("#", 1)[0]
            if clean and not (page.parent / clean).resolve().exists():
                broken.append(f"{page.relative_to(ROOT)} -> {target}")
    checks["internal_links"] = not broken
    committed = set(run("git", "diff", "--name-only", "origin/main...HEAD").stdout.splitlines())
    working = set(run("git", "diff", "--name-only").stdout.splitlines())
    changed = committed | working
    checks["scope"] = not any(path.startswith(("archive/", "graph/", "publication/")) for path in changed)
    checks["git_diff_check"] = run("git", "diff", "--check").returncode == 0

    errors.extend(f"failed check: {name}" for name, passed in checks.items() if not passed)
    errors.extend(broken)
    status = "PASS" if not errors else "FAIL"
    report = {"campaign_id": "knowledge-narrative-depth-wave-3a-institutions-people-guilds-2026-07", "status": status, "checks": checks, "errors": errors}
    (HERE / "validation-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    (HERE / "validation-report.md").write_text(
        "# Wave 3A Validation\n\n**Result:** `" + status + "`\n\n" +
        "\n".join(f"- {'PASS' if passed else 'FAIL'}: {name}" for name, passed in checks.items()) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
