"""Validate Knowledge Narrative Depth Wave 3C."""
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
REQUIRED = {"title", "seo_title", "seo_description", "knowledge_status", "as_of", "confidence", "evidence_basis", "known_limitations", "research_gaps", "review_after"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()).hexdigest()


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)


def metadata(text: str) -> set[str]:
    return set(re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):", text.split("---", 2)[1], re.MULTILINE)) if text.startswith("---\n") else set()


def main() -> int:
    errors = []
    inventory = json.loads((HERE / "page-inventory.json").read_text(encoding="utf-8"))
    pages = [ROOT / item["path"] for item in inventory["pages"]]
    generated = sorted(HERE.glob("*.json")) + sorted((HERE / "evidence-packets").glob("*.json"))
    before = {str(path): sha(path) for path in generated}
    first = run(sys.executable, str(BUILD)); middle = {str(path): sha(path) for path in generated}
    second = run(sys.executable, str(BUILD)); after = {str(path): sha(path) for path in generated}
    entity = (ROOT / "knowledge/index/Entity-Registry.md").read_text(encoding="utf-8")
    public = (ROOT / "knowledge/index/source-registry/Public-Source-Registry.md").read_text(encoding="utf-8")
    checks = {
        "deterministic_generation": first.returncode == second.returncode == 0 and before == middle == after,
        "page_count": len(pages) == 7,
        "required_metadata": all(REQUIRED <= metadata(path.read_text(encoding="utf-8")) for path in pages),
        "review_sections": all("## Review status" in path.read_text(encoding="utf-8") for path in pages),
        "packet_count": len(list((HERE / "evidence-packets").glob("*.json"))) == 7,
        "narrow_lifecycle_boundary": "Lifecycle attaches to the narrowest named build" in entity and "Identity registration does not establish current lifecycle" in entity,
        "medium_registry_current": "173 confirmed articles fully ingested" in public and "51 explicitly deferred Medium" in public,
    }
    broken = []
    for page in pages:
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", page.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#")):
                continue
            clean = target.split("#", 1)[0]
            if clean and not (page.parent / clean).resolve().exists():
                broken.append(f"{page.relative_to(ROOT)} -> {target}")
    checks["internal_links"] = not broken
    changed = set(run("git", "diff", "--name-only", "origin/main...HEAD").stdout.splitlines()) | set(run("git", "diff", "--name-only").stdout.splitlines())
    checks["scope"] = not any(path.startswith(("archive/", "graph/", "publication/")) for path in changed)
    checks["git_diff_check"] = run("git", "diff", "--check").returncode == 0
    errors.extend(f"failed check: {name}" for name, passed in checks.items() if not passed); errors.extend(broken)
    status = "PASS" if not errors else "FAIL"
    report = {"campaign_id": "knowledge-narrative-depth-wave-3c-indexes-registries-2026-07", "status": status, "checks": checks, "errors": errors}
    (HERE / "validation-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    (HERE / "validation-report.md").write_text("# Wave 3C Validation\n\n**Result:** `" + status + "`\n\n" + "\n".join(f"- {'PASS' if passed else 'FAIL'}: {name}" for name, passed in checks.items()) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report)); return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
