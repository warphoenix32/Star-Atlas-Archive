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


def test_search_index_covers_published_articles_and_the_knowledge_archive_once():
    index = json.loads((SITE / "assets" / "library-index.json").read_text(encoding="utf-8"))
    markdown = sorted(ROOT.glob("knowledge/**/*.md"))
    manifest = json.loads(
        (ROOT / "publication" / "manifests" / "publication-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    published = [
        entry
        for entry in manifest["entries"]
        if entry["status"] in manifest["build_policy"]["include_statuses"]
    ]
    archive_records = [record for record in index if record["layer"] == "archive"]
    library_records = [record for record in index if record["layer"] == "library"]
    assert len(index) == len(markdown) + len(published)
    assert len(archive_records) == len(markdown)
    assert len(library_records) == len(published)
    assert len({record["id"] for record in index}) == len(index)
    assert {record["path"] for record in archive_records} == {
        path.relative_to(ROOT).as_posix() for path in markdown
    }
    assert {record["publicationId"] for record in library_records} == {
        entry["publication_id"] for entry in published
    }
    assert all(record["url"].startswith("article.html?id=") for record in index)
    assert all(
        record["sourceUrl"].startswith(
            "https://github.com/warphoenix32/Star-Atlas-Archive/blob/main/"
        )
        for record in index
    )


def test_internal_reader_preserves_canonical_source_linkage():
    html = (SITE / "article.html").read_text(encoding="utf-8")
    script = (SITE / "article.js").read_text(encoding="utf-8")
    assert 'id="record-layer"' in html
    assert "Published Library article" in script
    assert "Research archive record" in script
    assert "assets/library-index.json" in script
    assert "content/" in script
    assert "sourceUrl" in script
    assert "renderMarkdown" in script


def test_github_pages_workflow_builds_publication_and_archive_layers():
    workflow = (ROOT / ".github" / "workflows" / "library-pages.yml").read_text(encoding="utf-8")
    builder = (SITE / "scripts" / "build-pages.mjs").read_text(encoding="utf-8")
    assert "actions/deploy-pages@v4" in workflow
    assert "actions/upload-pages-artifact@v4" in workflow
    assert 'path.join(repository, "knowledge")' in builder
    assert 'path.join(output, "content", "knowledge")' in builder
    assert "publication-manifest.json" in builder
    assert "publishedEntries" in builder


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
