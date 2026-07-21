import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN_DIR = ROOT / "operations" / "campaigns" / "star-atlas-medium-ingestion-2026-07"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("star_atlas_medium_campaign_test", CAMPAIGN_DIR / "medium_campaign.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json(name: str):
    return json.loads((CAMPAIGN_DIR / name).read_text(encoding="utf-8"))


def test_html_escaped_suffix_is_not_part_of_observed_url():
    campaign = load_campaign_module()
    value = "https://medium.com/star-atlas/example-037b651761e2&quot;&gt;published"
    assert campaign.clean_url_tail(value) == "https://medium.com/star-atlas/example-037b651761e2"


def test_signin_query_does_not_supply_article_post_id():
    campaign = load_campaign_module()
    signin = (
        "https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fstar-atlas%2F"
        "example-037b651761e2"
    )
    assert campaign.post_id_from_url(signin) is None
    assert campaign.post_id_from_url("https://medium.com/star-atlas/example-037b651761e2") == "037b651761e2"


def test_completion_gate_reconciles_every_confirmed_article():
    manifest = read_json("url-manifest.json")
    gate = read_json("completion-gate-report.json")
    body = read_json("full-body-audit.json")
    queue = read_json("manual-review-queue.json")
    gaps = read_json("unresolved-evidence-ledger.json")

    included = [item for item in manifest["records"] if item["inclusion_status"] == "INCLUDED"]
    deferred = [item for item in manifest["records"] if item["inclusion_status"] == "DEFERRED"]

    assert len(included) == 181
    assert deferred == []
    assert queue["records"] == []
    assert len(gaps["records"]) == 4
    assert body["result"] == "PASS"
    assert body["articles_audited"] == body["articles_passed"] == 181
    assert gate["gate_status"] == "COMPLETE_WITH_DOCUMENTED_EXTERNAL_EVIDENCE_GAPS"
