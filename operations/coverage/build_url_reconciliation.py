"""Build a deterministic disposition overlay for the immutable URL inventory."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "archive/normalized/manifests/normalized-urls.jsonl"
AS_OF = "2026-07-20"
BASELINE_SHA = "19a447596c6cb3b5e72343a0e6ef9dd87b3e51ed"
INVENTORY_SHA256 = "ea23f3cc334c7d883d60a6ddbbcb09002b0a49f6da24346277630610c0579e83"
CAMPAIGNS = {
    "campaign-alpha-aephia": ROOT / "archive/campaign-summaries/campaign-alpha-aephia/campaign-summary.json",
    "campaign-bravo-intergalactic-herald": ROOT / "archive/campaign-summaries/campaign-bravo-intergalactic-herald/campaign-summary.json",
    "campaign-charlie-hnn": ROOT / "archive/campaign-summaries/campaign-charlie-hnn/campaign-summary.json",
}
SOURCE_RECORD_DIRS = {
    campaign_id: ROOT / "archive/source-records" / campaign_id for campaign_id in CAMPAIGNS
}
HNN_CREATORS = {"Kr1gs", "Hologram News Network"}
HNN_AUDIOVISUAL_PLATFORMS = {"youtube", "spotify", "twitch", "tiktok"}
HNN_NAVIGATION_URLS = {
    "https://thehologram.io/",
    "https://hologramnews.com/",
    "https://medium.com/the-hologram/newsletters/holoreport",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build() -> tuple[list[dict], dict]:
    inventory_blob = subprocess.check_output(
        ["git", "show", f"{BASELINE_SHA}:{INVENTORY.relative_to(ROOT).as_posix()}"], cwd=ROOT
    )
    raw_lines = [line for line in inventory_blob.decode("utf-8").splitlines() if line.strip()]
    inventory = [json.loads(line) for line in raw_lines]
    if sha256(inventory_blob) != INVENTORY_SHA256:
        raise ValueError("normalized URL inventory checksum changed")
    if len(inventory) != 3232:
        raise ValueError(f"expected 3,232 inventory rows, found {len(inventory)}")
    if len({row["url_id"] for row in inventory}) != len(inventory):
        raise ValueError("normalized URL inventory contains duplicate url_id values")
    if len({row["canonical_url"] for row in inventory}) != len(inventory):
        raise ValueError("normalized URL inventory contains duplicate canonical URLs")

    base_hashes = {row["url_id"]: sha256(line.encode("utf-8")) for row, line in zip(inventory, raw_lines)}
    base_lines = {row["url_id"]: index for index, row in enumerate(inventory, start=1)}
    campaign_results: dict[str, dict] = {}
    content_hashes: dict[str, list[str]] = defaultdict(list)
    for campaign_id, path in CAMPAIGNS.items():
        for index, result in enumerate(read_json(path).get("results", [])):
            url_id = result.get("url_id")
            if not url_id:
                continue
            if url_id in campaign_results:
                raise ValueError(f"URL appears in multiple written-corpus campaign results: {url_id}")
            campaign_results[url_id] = {
                "campaign_id": campaign_id,
                "evidence_path": path.relative_to(ROOT).as_posix(),
                "json_pointer": f"/results/{index}",
                "result": result,
            }
            if result.get("status") == "SUCCESS" and result.get("content_hash"):
                content_hashes[result["content_hash"]].append(url_id)

    duplicate_clusters = {
        url_id: f"DUP-CONTENT-{content_hash[:16].upper()}"
        for content_hash, url_ids in content_hashes.items()
        if len(url_ids) > 1
        for url_id in url_ids
    }

    records: list[dict] = []
    for row in inventory:
        url_id = row["url_id"]
        canonical_url = row["canonical_url"]
        parsed = urlsplit(canonical_url)
        host = (parsed.hostname or "").lower()
        creators = set(row.get("creators", []))
        platforms = set(row.get("platforms", []))
        match = campaign_results.get(url_id)
        campaign_family = None
        source_ids: list[str] = []
        artifact_paths: list[str] = []
        evidence = [{
            "path": INVENTORY.relative_to(ROOT).as_posix(),
            "json_pointer": None,
            "record_locator": {"line": base_lines[url_id], "url_id": url_id},
            "evidence_type": "IMMUTABLE_DISCOVERY_RECORD",
        }]
        exclusion_reason = None
        resolved_url = None
        manual_review = False

        if match:
            result = match["result"]
            campaign_family = match["campaign_id"]
            disposition = "INGESTED_CONFIRMED" if result.get("status") == "SUCCESS" else "RETRIEVAL_FAILED"
            method = "EXACT_CAMPAIGN_RESULT_URL_ID"
            evidence.append({
                "path": match["evidence_path"],
                "json_pointer": match["json_pointer"],
                "evidence_type": "ITEM_LEVEL_CAMPAIGN_RESULT",
            })
            if result.get("source_id"):
                source_ids = [result["source_id"]]
                source_path = SOURCE_RECORD_DIRS[campaign_family] / f"{result['source_id']}.md"
                if not source_path.exists():
                    raise ValueError(f"missing Source Record for {url_id}: {source_path}")
                artifact_paths = [source_path.relative_to(ROOT).as_posix()]
            observed = result.get("url")
            if observed and observed != canonical_url:
                resolved_url = observed
            manual_review = disposition == "RETRIEVAL_FAILED"
        elif "Intergalactic Herald" in creators:
            campaign_family = "campaign-bravo-intergalactic-herald"
            evidence.append({
                "path": CAMPAIGNS[campaign_family].relative_to(ROOT).as_posix(),
                "json_pointer": "/excluded",
                "evidence_type": "AGGREGATE_EXCLUSION_RECONCILIATION",
            })
            if parsed.path.startswith("/podcast"):
                disposition = "EXCLUDED_NON_WRITTEN"
                exclusion_reason = "PODCAST_OUTSIDE_WRITTEN_CAMPAIGN"
                method = "CREATOR_AND_PATH_SELECTOR_RECONCILED_TO_CAMPAIGN_TOTAL"
            elif parsed.path in {"", "/"}:
                disposition = "EXCLUDED_NAVIGATION"
                exclusion_reason = "PUBLICATION_LANDING_PAGE"
                method = "CREATOR_AND_PATH_SELECTOR_RECONCILED_TO_CAMPAIGN_TOTAL"
            else:
                raise ValueError(f"unreconciled Herald candidate: {url_id}")
        elif creators & HNN_CREATORS:
            campaign_family = "campaign-charlie-hnn"
            evidence.append({
                "path": CAMPAIGNS[campaign_family].relative_to(ROOT).as_posix(),
                "json_pointer": "/excluded",
                "evidence_type": "AGGREGATE_EXCLUSION_RECONCILIATION",
            })
            if platforms & HNN_AUDIOVISUAL_PLATFORMS:
                disposition = "EXCLUDED_NON_WRITTEN"
                exclusion_reason = "AUDIOVISUAL_OUTSIDE_WRITTEN_CAMPAIGN"
            elif canonical_url in HNN_NAVIGATION_URLS:
                disposition = "EXCLUDED_NAVIGATION"
                exclusion_reason = "LANDING_OR_NEWSLETTER_NAVIGATION_PAGE"
            else:
                disposition = "EXCLUDED_EXTERNAL_WRITTEN"
                exclusion_reason = "WRITTEN_PAGE_OUTSIDE_HNN_PUBLICATION_IDENTITY"
            method = "CREATOR_AND_SURFACE_SELECTOR_RECONCILED_TO_CAMPAIGN_TOTAL"
        else:
            disposition = f"{row['processing_status']}_UNRECONCILED"
            method = "HISTORICAL_STATUS_PRESERVED_NO_ITEM_LEVEL_CAMPAIGN_EVIDENCE"
            manual_review = True

        records.append({
            "url_id": url_id,
            "base_record_sha256": base_hashes[url_id],
            "historical_processing_status": row["processing_status"],
            "historical_network_status": row["network_status"],
            "current_disposition": disposition,
            "campaign_family": campaign_family,
            "host_family": host,
            "source_ids": source_ids,
            "artifact_paths": artifact_paths,
            "evidence": evidence,
            "reconciliation_method": method,
            "exclusion_reason": exclusion_reason,
            "resolved_url": resolved_url,
            "duplicate_cluster_id": duplicate_clusters.get(url_id),
            "manual_review_required": manual_review,
        })

    records.sort(key=lambda item: item["url_id"])
    counts = Counter(row["current_disposition"] for row in records)
    expected = {
        "INGESTED_CONFIRMED": 480,
        "EXCLUDED_NON_WRITTEN": 247,
        "EXCLUDED_NAVIGATION": 4,
        "EXCLUDED_EXTERNAL_WRITTEN": 12,
        "RETRIEVAL_FAILED": 4,
        "PENDING_UNRECONCILED": 251,
        "DEFERRED_UNRECONCILED": 2234,
    }
    if dict(counts) != expected:
        raise ValueError(f"disposition reconciliation changed: {dict(counts)}")

    unresolved = [row for row in records if row["current_disposition"].endswith("_UNRECONCILED")]
    platform_counts: Counter[str] = Counter()
    inventory_by_id = {row["url_id"]: row for row in inventory}
    for record in unresolved:
        platform_counts.update(inventory_by_id[record["url_id"]].get("platforms", []))

    summary = {
        "schema_version": "1.0",
        "as_of": AS_OF,
        "baseline_sha": BASELINE_SHA,
        "source_inventory_path": INVENTORY.relative_to(ROOT).as_posix(),
        "source_inventory_sha256": INVENTORY_SHA256,
        "source_inventory_rows": len(inventory),
        "current_disposition_counts": dict(counts),
        "unreconciled": {
            "count": len(unresolved),
            "platform_counts": dict(platform_counts.most_common()),
            "status": "PHASE_2_CANDIDATE_REVIEW_REQUIRED",
        },
        "duplicate_clusters": len(set(duplicate_clusters.values())),
        "interpretation": [
            "The source inventory is unchanged; its processing and network statuses remain historical evidence.",
            "The overlay reconciles repository campaign state and does not establish complete external coverage.",
            "HNN and Herald exclusions are deterministic aggregate reconciliations because the historical campaigns did not ledger every excluded URL ID.",
            "Unreconciled URLs are not labeled retrieval failures or absent material.",
        ],
    }
    return records, summary


def write_outputs(directory: Path) -> None:
    records, summary = build()
    (directory / "url-disposition-overlay.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in records),
        encoding="utf-8",
    )
    (directory / "url-disposition-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# URL Disposition Reconciliation",
        "",
        f"Snapshot: `{summary['baseline_sha']}` on {summary['as_of']}.",
        "",
        "The original 3,232-row inventory is unchanged. This overlay records later campaign outcomes without claiming complete external coverage.",
        "",
        "## Current dispositions",
        "",
        "| Disposition | URLs |",
        "| --- | ---: |",
    ]
    lines.extend(f"| `{key}` | {value} |" for key, value in summary["current_disposition_counts"].items())
    lines += [
        "",
        "## Evidence boundary",
        "",
        "- All 480 ingested records and four failures are supported by exact campaign result URL IDs.",
        "- All 480 ingested records resolve to a preserved Markdown Source Record.",
        "- Herald and HNN exclusions reproduce their published aggregate counts with deterministic creator and surface selectors; the campaigns did not preserve item-level exclusion ledgers.",
        "- One duplicate content cluster is retained as two distinct Herald URL records.",
        "- The 2,485 unreconciled rows retain historical `PENDING` or `DEFERRED` status and require bounded Phase 2 review.",
        "- The 2,119 unreconciled YouTube URLs are not assumed absent from transcript holdings because those packages often lack source URLs and video IDs.",
        "",
    ]
    (directory / "url-disposition-summary.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    write_outputs(Path(__file__).resolve().parent)
