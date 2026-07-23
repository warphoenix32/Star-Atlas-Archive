import json
from pathlib import Path


ROOT = Path(__file__).parents[3]
SITE = ROOT / "publication" / "site"


def test_approved_landing_copy_and_semantics_are_present():
    html = (SITE / "index.html").read_text(encoding="utf-8")
    required = {
        "The Living Record of Star Atlas",
        "Explore the people, worlds, decisions, and ideas that shaped a civilization.",
        "Where would you like to begin?",
        "Enter the Library",
        "Explore the Timeline",
        "Discover the Archive",
        "Follow the Evidence",
    }
    assert all(value in html for value in required)
    assert "<main" in html
    assert "<nav" in html
    assert "<dialog" in html
    assert "aria-live" in html


def test_search_index_covers_the_current_knowledge_tree_once():
    index = json.loads((SITE / "assets" / "library-index.json").read_text(encoding="utf-8"))
    markdown = sorted(ROOT.glob("knowledge/**/*.md"))
    assert len(index) == len(markdown) == 88
    assert len({record["id"] for record in index}) == len(index)
    assert {record["path"] for record in index} == {path.relative_to(ROOT).as_posix() for path in markdown}
    assert all(record["url"].startswith("article.html?id=") for record in index)
    assert all(record["sourceUrl"].startswith("https://github.com/warphoenix32/Star-Atlas-Archive/blob/main/knowledge/") for record in index)


def test_internal_reader_preserves_canonical_source_linkage():
    html = (SITE / "article.html").read_text(encoding="utf-8")
    script = (SITE / "article.js").read_text(encoding="utf-8")
    assert "Canonical repository knowledge" in html
    assert "assets/library-index.json" in script
    assert "content/" in script
    assert "sourceUrl" in script
    assert "renderMarkdown" in script


def test_github_pages_workflow_builds_the_repository_knowledge_tree():
    workflow = (ROOT / ".github" / "workflows" / "library-pages.yml").read_text(encoding="utf-8")
    builder = (SITE / "scripts" / "build-pages.mjs").read_text(encoding="utf-8")
    assert "actions/deploy-pages@v4" in workflow
    assert "actions/upload-pages-artifact@v4" in workflow
    assert 'path.join(repository, "knowledge")' in builder
    assert 'path.join(output, "content")' in builder


def test_frontend_is_portable_and_does_not_embed_local_paths():
    for name in ("index.html", "article.html", "styles.css", "article.css", "app.js", "article.js", "README.md"):
        text = (SITE / name).read_text(encoding="utf-8")
        assert "C:/Users/" not in text
        assert "C:\\Users\\" not in text
    assert not (SITE / "vercel.json").exists()
    assert not (SITE / "node_modules").exists()


def test_visual_asset_is_web_optimized_and_motion_is_accessible():
    asset = SITE / "assets" / "library-portal.webp"
    assert asset.stat().st_size < 500_000
    css = (SITE / "styles.css").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in css
    assert ":focus-visible" in css
    assert "assets/library-portal.webp" in css
