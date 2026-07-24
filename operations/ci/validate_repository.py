"""Deterministic, network-free repository and campaign validation for CI."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

from promotion_contract import validate_campaign_report


ROOT = Path(__file__).resolve().parents[2]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SCHEMA_VERSIONS = {"2.0", "2.1"}


class ValidationFailure(RuntimeError):
    pass


def run(*args: str, check: bool = False, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        env=env,
        check=False,
    )
    if check and result.returncode:
        raise ValidationFailure(f"command failed ({' '.join(args)}):\n{result.stdout}{result.stderr}")
    return result


def tracked_files(*suffixes: str) -> list[Path]:
    result = run("git", "ls-files", check=True)
    return [ROOT / value for value in result.stdout.splitlines() if value.endswith(suffixes)]


def changed_paths(base_ref: str) -> list[str]:
    if not base_ref:
        raise ValidationFailure("base ref is required for diff-scoped validation")
    result = run("git", "diff", "--name-only", f"{base_ref}...HEAD", check=True)
    return sorted(line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip())


def parse_json_corpus() -> tuple[int, int]:
    documents = 0
    records = 0
    failures: list[str] = []
    for path in tracked_files(".json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            documents += 1
        except Exception as exc:  # noqa: BLE001 - report every parse defect
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
    for path in tracked_files(".jsonl"):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                json.loads(line)
                records += 1
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{path.relative_to(ROOT)}:{line_number}: {exc}")
    if failures:
        raise ValidationFailure("invalid JSON/JSONL:\n" + "\n".join(failures))
    return documents, records


def validate_declared_schemas() -> int:
    checked = 0
    failures: list[str] = []
    for path in tracked_files(".json"):
        if "archive/ingestion-packages/" not in path.as_posix():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        metadata = payload.get("metadata")
        if not isinstance(metadata, dict) or "repository_schema" not in metadata:
            continue
        checked += 1
        version = str(metadata.get("repository_schema"))
        if version not in SCHEMA_VERSIONS:
            failures.append(f"{path.relative_to(ROOT)}: unsupported repository_schema {version}")
        if not isinstance(payload.get("sources"), list):
            failures.append(f"{path.relative_to(ROOT)}: declared ingestion package lacks sources list")
    if failures:
        raise ValidationFailure("schema contract failures:\n" + "\n".join(failures))
    return checked


def validate_source_identity() -> tuple[int, int]:
    extraction_paths = sorted(ROOT.glob("archive/ingestion-packages/*/extractions/*.json"))
    ids = [path.stem for path in extraction_paths]
    duplicates = sorted(value for value, count in Counter(ids).items() if count > 1)
    failures: list[str] = []
    if duplicates:
        failures.append("duplicate extraction Source IDs: " + ", ".join(duplicates))

    record_markdown: dict[str, list[Path]] = {}
    record_json: dict[str, list[Path]] = {}
    for path in ROOT.glob("archive/source-records/**/*.md"):
        record_markdown.setdefault(path.stem, []).append(path)
    for path in ROOT.glob("archive/source-records/**/*.json"):
        if path.name in {"source-records.json", "campaign-summary.json"}:
            continue
        record_json.setdefault(path.stem, []).append(path)

    for path in extraction_paths:
        source_id = path.stem
        payload = json.loads(path.read_text(encoding="utf-8"))
        embedded = payload.get("source_id") if isinstance(payload, dict) else None
        if embedded and embedded != source_id:
            failures.append(f"{path.relative_to(ROOT)}: source_id {embedded} does not match filename {source_id}")
        markdown_matches = record_markdown.get(source_id, [])
        if len(markdown_matches) != 1:
            failures.append(f"{source_id}: expected one Markdown Source Record, found {len(markdown_matches)}")
        for record_path in record_json.get(source_id, []):
            record = json.loads(record_path.read_text(encoding="utf-8"))
            if isinstance(record, dict) and record.get("source_id") not in {None, source_id}:
                failures.append(f"{record_path.relative_to(ROOT)}: Source Record ID does not match filename")

    if failures:
        raise ValidationFailure("Source-ID reconciliation failures:\n" + "\n".join(failures))
    return len(extraction_paths), sum(len(value) for value in record_markdown.values())


def validate_markdown_links() -> int:
    checked = 0
    failures: list[str] = []
    for path in tracked_files(".md"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("archive/source-records/", "archive/campaign-summaries/", "archive/normalized/lore/pages/")):
            continue
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip().strip("<>").split()[0]
            if not target or target.startswith("#") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            target = unquote(target.split("#", 1)[0])
            checked += 1
            if not (path.parent / target).resolve().exists():
                failures.append(f"{rel} -> {match.group(1)}")
    if failures:
        raise ValidationFailure("broken local Markdown links:\n" + "\n".join(failures))
    return checked


def validate_simplified_promotion_reports() -> int:
    """Validate campaign reports that explicitly adopt pipeline version 1.0."""
    checked = 0
    failures: list[str] = []
    for path in tracked_files("campaign-report.json"):
        if not path.relative_to(ROOT).as_posix().startswith("operations/campaigns/"):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("pipeline_version") != "1.0":
            continue
        checked += 1
        for failure in validate_campaign_report(payload, root=ROOT):
            failures.append(f"{path.relative_to(ROOT)}: {failure}")
    if failures:
        raise ValidationFailure("simplified promotion contract failures:\n" + "\n".join(failures))
    return checked


def validate_forbidden_paths(changes: list[str]) -> str:
    phase5_publication_portfolio = any(path.startswith((
        "publication/articles/",
        "operations/campaigns/phase-5-foundational-publication-portfolio-2026-07/",
        "operations/tests/phase5_publication_portfolio/",
    )) for path in changes)
    phase4_knowledge_consolidation = not phase5_publication_portfolio and any(path.startswith((
        "operations/campaigns/phase-4-knowledge-consolidation-2026-07/",
        "operations/tests/phase4_knowledge_consolidation/",
    )) for path in changes)
    publication_contract_campaign = not phase5_publication_portfolio and any(path.startswith((
        "publication/manifests/",
        "operations/campaigns/phase-3-publication-contract-2026-07/",
        "operations/tests/publication_contract/",
    )) or path in {
        "publication/PUBLICATION-CONTRACT.md",
        "operations/schema/PUBLICATION-MANIFEST-v1.schema.json",
        "operations/schema/examples/publication-manifest-v1.json",
    } for path in changes)
    legacy_written_raw_recovery = any(path.startswith((
        "archive/raw/legacy-written-recovery/",
        "archive/provenance/legacy-written-recovery/",
        "operations/campaigns/legacy-written-raw-recovery-2026-07/",
        "operations/tests/legacy_written_raw_recovery/",
    )) or path == "archive/manifests/legacy-written-raw-recovery-2026-07.json" for path in changes)
    phase_one_inventory = not (
        legacy_written_raw_recovery
        or publication_contract_campaign
        or phase4_knowledge_consolidation
        or phase5_publication_portfolio
    ) and any(path.startswith((
        "operations/coverage/",
        "operations/programs/library-roadmap/",
    )) for path in changes)
    knowledge_campaign_marker = any(
        path.startswith("operations/campaigns/knowledge-narrative-depth-001/") for path in changes
    )
    ledger_campaign = any(path.startswith((
        "operations/campaigns/canonical-pip-governance-ledger-2026-07/",
        "knowledge/governance/PIP-Registry.",
    )) for path in changes) and not knowledge_campaign_marker
    transcript_semantic_campaign = any(path.startswith((
        "archive/semantic/star-atlas-transcripts/",
        "operations/campaigns/star-atlas-transcripts-semantic-2026-07/",
    )) for path in changes)
    atlas_brew_semantic_campaign = any(path.startswith((
        "archive/semantic/atlas-brew/",
        "operations/campaigns/atlas-brew-significance-review-2026-07/",
    )) for path in changes)
    atlas_brew_url_reconciliation = any(path.startswith((
        "operations/campaigns/atlas-brew-url-reconciliation-2026-07/",
        "operations/tests/atlas_brew_url_reconciliation/",
    )) or path in {
        "archive/provenance/atlas-brew-combined/youtube-playlist-manifest.json",
        "archive/reconciliation/atlas-brew-combined/youtube-url-reconciliation.json",
        "archive/reconciliation/atlas-brew-combined/youtube-source-metadata-patch.json",
    } for path in changes)
    knowledge_campaign = not phase4_knowledge_consolidation and any(path.startswith(("knowledge/", "operations/campaigns/knowledge-narrative-depth-001/")) for path in changes)
    medium_campaign = any("star-atlas-medium" in path or path.startswith(("archive/raw/medium/", "archive/normalized/medium/", "archive/source-records/medium/")) for path in changes)
    economic_reports_campaign = any(path.startswith((
        "archive/raw/economic-reports/",
        "archive/provenance/economic-reports/",
        "archive/normalized/economic-reports/",
        "archive/source-records/economic-reports/",
        "archive/ingestion-packages/economic-reports-official/",
        "operations/campaigns/official-economic-reports-pdf-ingestion-2026-07/",
        "operations/tests/economic_reports/",
    )) or path == "archive/manifests/official-economic-reports-pdf-ingestion-2026-07.json" for path in changes)
    ship_campaign = any(path.startswith((
        "archive/raw/starbased-ship-states/",
        "archive/provenance/starbased-ship-states/",
        "archive/normalized/starbased-ship-states/",
        "operations/campaigns/starbased-ship-states-ingestion-2026-07/",
        "operations/tests/starbased_ship_states/",
    )) for path in changes)
    wallet_campaign = any(path.startswith((
        "archive/raw/community-wallet-attributions/",
        "archive/provenance/community-wallet-attributions/",
        "archive/normalized/community-wallet-attributions/",
        "archive/source-records/community-wallet-attributions/",
        "operations/campaigns/community-wallet-attribution-ingestion-2026-07/",
        "operations/tests/community_wallet_attributions/",
    )) or path == "archive/manifests/community-wallet-attribution-ingestion-2026-07.json" for path in changes)
    dao_pip_vote_campaign = any(path.startswith((
        "archive/raw/governance-votes/pip-01-32/",
        "archive/normalized/governance-votes/pip-01-32/",
        "archive/source-records/governance-votes/pip-01-32/",
        "operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/",
        "operations/tests/dao_pip_governance_votes/",
    )) or path in {
        "archive/provenance/governance-votes/pip-01-32.json",
        "archive/manifests/dao-pip-vote-evidence-ingestion-2026-07.json",
    } for path in changes)
    pip33_vote_campaign = not dao_pip_vote_campaign and any(path.startswith((
        "archive/normalized/governance-votes/pip-33/",
        "operations/campaigns/pip-33-onchain-vote-reconciliation-2026-07/",
        "operations/tests/pip33_governance_votes/",
    )) or path in {
        "archive/provenance/governance-votes/pip-33.json",
        "archive/manifests/pip-33-onchain-vote-reconciliation-2026-07.json",
        "archive/source-records/governance-votes/SRC-SOLANA-PIP-33-5EE6D3F844C4.json",
        "archive/source-records/governance-votes/SRC-SOLANA-PIP-33-5EE6D3F844C4.md",
    } for path in changes)
    foundation_council_campaign = any(path.startswith((
        "archive/raw/discord/star-atlas/foundation-room/",
        "archive/raw/discord/star-atlas/fr-chat/",
        "archive/provenance/discord/star-atlas/",
        "archive/normalized/discord/star-atlas/",
        "archive/source-records/discord/star-atlas/",
        "archive/raw/governance/council-pip-tracker/snapshots/2026-07-23/",
        "archive/normalized/governance/council-pip-tracker/snapshots/2026-07-23/",
        "archive/source-records/governance/council-pip-tracker/snapshots/2026-07-23/",
        "operations/campaigns/foundation-room-council-evidence-ingestion-2026-07/",
    )) or path in {
        "archive/provenance/governance/council-pip-tracker/snapshots/2026-07-23.json",
        "archive/manifests/foundation-room-council-evidence-ingestion-2026-07.json",
    } for path in changes)
    discord_campaign = any(path.startswith(("operations/campaigns/discord-community-indexing-001/", "operations/tests/discord_community_indexing/")) for path in changes)
    library_frontend = not (
        publication_contract_campaign or phase4_knowledge_consolidation
    ) and any(
        path.startswith(("publication/site/", "operations/tests/library_frontend/"))
        or path == "publication/README.md"
        for path in changes
    )
    lore_campaign = any(path.startswith((
        "archive/raw/lore-repository/",
        "archive/provenance/lore-repository/",
        "archive/normalized/lore/",
        "archive/source-records/lore-repository/",
        "archive/ingestion-packages/lore-repository/",
        "operations/campaigns/lore-repository-ingestion-2026-07/",
        "operations/tests/lore_repository/",
    )) or path == "archive/manifests/lore-repository-ingestion-2026-07.json" for path in changes)
    pipeline_framework = any(path in {
        "operations/docs/SIMPLIFIED-PROMOTION-PIPELINE.md",
        "operations/schema/PROMOTION-CAMPAIGN-v1.schema.json",
        "operations/schema/examples/promotion-campaign-v1.json",
        "operations/templates/simplified-campaign-report.json",
        "operations/templates/simplified-campaign-report.md",
    } or path.startswith("operations/tests/promotion_pipeline/") for path in changes)
    agent_contracts = any(path.startswith((
        "operations/agents/",
        "operations/tests/agent_contracts/",
    )) or path in {
        "operations/docs/KNOWLEDGE-ARCHITECTURE.md",
        "operations/templates/knowledge-entry-template.md",
    } for path in changes)
    common = (".github/workflows/", "operations/ci/")
    selected = 1 if legacy_written_raw_recovery else sum((phase5_publication_portfolio, phase4_knowledge_consolidation, publication_contract_campaign, phase_one_inventory, ledger_campaign, transcript_semantic_campaign, atlas_brew_semantic_campaign, atlas_brew_url_reconciliation, knowledge_campaign and not ledger_campaign, medium_campaign, economic_reports_campaign, ship_campaign, wallet_campaign, dao_pip_vote_campaign, pip33_vote_campaign, foundation_council_campaign, discord_campaign, library_frontend and not phase5_publication_portfolio, lore_campaign and not (wallet_campaign or dao_pip_vote_campaign or pip33_vote_campaign or foundation_council_campaign or transcript_semantic_campaign or atlas_brew_semantic_campaign or atlas_brew_url_reconciliation or knowledge_campaign), pipeline_framework and not agent_contracts, agent_contracts))
    if selected != 1:
        raise ValidationFailure("unable to select exactly one recognized campaign path contract")
    if phase5_publication_portfolio:
        allowed = common + (
            "publication/articles/",
            "publication/manifests/publication-manifest.json",
            "publication/site/article.css",
            "publication/site/article.html",
            "publication/site/article.js",
            "publication/site/scripts/validate-site.mjs",
            "operations/campaigns/phase-5-foundational-publication-portfolio-2026-07/",
            "operations/tests/phase5_publication_portfolio/",
            "operations/tests/phase4_knowledge_consolidation/test_phase4_knowledge_consolidation.py",
            "operations/programs/library-roadmap/",
            "operations/coverage/campaign-status-register.json",
            "operations/coverage/campaign-status-register.md",
        )
        label = "phase-5-foundational-publication-portfolio-2026-07"
    elif phase4_knowledge_consolidation:
        allowed = common + (
            "knowledge/",
            "operations/campaigns/phase-4-knowledge-consolidation-2026-07/",
            "operations/tests/phase4_knowledge_consolidation/",
            "operations/tests/library_frontend/test_frontend.py",
            "operations/programs/library-roadmap/",
            "operations/coverage/campaign-status-register.json",
            "operations/coverage/campaign-status-register.md",
            "publication/site/assets/library-index.json",
        )
        label = "phase-4-knowledge-consolidation-2026-07"
    elif publication_contract_campaign:
        allowed = common + (
            "publication/PUBLICATION-CONTRACT.md",
            "publication/README.md",
            "publication/articles/README.md",
            "publication/briefs/README.md",
            "publication/datasets/README.md",
            "publication/reports/README.md",
            "publication/manifests/",
            "operations/schema/README.md",
            "operations/schema/PUBLICATION-MANIFEST-v1.schema.json",
            "operations/schema/examples/publication-manifest-v1.json",
            "operations/campaigns/phase-3-publication-contract-2026-07/",
            "operations/tests/publication_contract/",
            "operations/programs/library-roadmap/",
            "operations/coverage/acquisition-backlog.json",
            "operations/coverage/acquisition-backlog.md",
            "operations/coverage/campaign-status-register.json",
            "operations/coverage/campaign-status-register.md",
            "operations/coverage/cleanup-register.json",
            "operations/coverage/cleanup-register.md",
            "operations/coverage/source-coverage-register.json",
            "operations/coverage/source-coverage-register.md",
        )
        label = "phase-3-publication-contract-2026-07"
    elif legacy_written_raw_recovery:
        allowed = common + (
            ".gitattributes",
            "archive/raw/legacy-written-recovery/",
            "archive/provenance/legacy-written-recovery/",
            "archive/manifests/legacy-written-raw-recovery-2026-07.json",
            "operations/campaigns/legacy-written-raw-recovery-2026-07/",
            "operations/tests/legacy_written_raw_recovery/",
        )
        label = "legacy-written-raw-recovery-2026-07"
    elif phase_one_inventory:
        allowed = common + (
            "operations/README.md",
            "operations/coverage/",
            "operations/programs/library-roadmap/",
            "operations/campaigns/phase-2-official-freshness-closeout-2026-07/",
            "operations/campaigns/knowledge-narrative-depth-001/validate_campaign.py",
            "operations/campaigns/knowledge-narrative-depth-001/validation-report.json",
            "operations/campaigns/knowledge-narrative-depth-001/validation-report.md",
            "operations/campaigns/social-governance-semantic-enrichment/build_campaign.py",
            "operations/campaigns/social-governance-semantic-enrichment/campaign-summary.json",
            "operations/campaigns/social-governance-semantic-enrichment/campaign-summary.md",
            "operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/validate_campaign.py",
            "operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/build_campaign.py",
            "operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/validation-report.json",
            "operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/validation-report.md",
            "operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/manifest.json",
            "archive/manifests/dao-pip-vote-evidence-ingestion-2026-07.json",
            "operations/campaigns/lore-repository-ingestion-2026-07/manifest.json",
            "operations/campaigns/lore-repository-ingestion-2026-07/build_campaign.py",
            "operations/campaigns/lore-repository-ingestion-2026-07/validation-report.json",
            "operations/campaigns/lore-repository-ingestion-2026-07/validation-report.md",
            "archive/manifests/lore-repository-ingestion-2026-07.json",
            "publication/site/assets/library-index.json",
        )
        label = "phase-one-repository-baseline"
    elif ledger_campaign:
        allowed = common + (
            "knowledge/governance/PIP-Registry.md",
            "knowledge/governance/PIP-Registry.json",
            "knowledge/governance/README.md",
            "operations/campaigns/canonical-pip-governance-ledger-2026-07/",
        )
        label = "canonical-pip-governance-ledger-2026-07"
    elif transcript_semantic_campaign:
        allowed = common + (
            "archive/semantic/star-atlas-transcripts/",
            "archive/manifests/lore-repository-ingestion-2026-07.json",
            "operations/campaigns/star-atlas-transcripts-semantic-2026-07/",
            "operations/campaigns/lore-repository-ingestion-2026-07/manifest.json",
        )
        label = "star-atlas-transcripts-semantic-2026-07"
    elif atlas_brew_semantic_campaign:
        allowed = common + (
            "archive/semantic/atlas-brew/",
            "archive/manifests/lore-repository-ingestion-2026-07.json",
            "operations/campaigns/atlas-brew-significance-review-2026-07/",
            "operations/campaigns/lore-repository-ingestion-2026-07/manifest.json",
        )
        label = "atlas-brew-significance-review-2026-07"
    elif atlas_brew_url_reconciliation:
        allowed = common + (
            "archive/provenance/atlas-brew-combined/youtube-playlist-manifest.json",
            "archive/reconciliation/atlas-brew-combined/youtube-url-reconciliation.json",
            "archive/reconciliation/atlas-brew-combined/youtube-source-metadata-patch.json",
            "archive/raw/atlas-brew-youtube-recovery/",
            "archive/provenance/atlas-brew-youtube-recovery/",
            "archive/normalized/atlas-brew-youtube-recovery/",
            "archive/source-records/atlas-brew-youtube-recovery/",
            "archive/ingestion-packages/atlas-brew-youtube-recovery/",
            "archive/manifests/atlas-brew-youtube-recovery-2026-07.json",
            "operations/campaigns/atlas-brew-url-reconciliation-2026-07/",
            "operations/tests/atlas_brew_url_reconciliation/",
        )
        label = "atlas-brew-url-reconciliation-2026-07"
    elif knowledge_campaign:
        allowed = common + (
            "knowledge/",
            "operations/campaigns/knowledge-narrative-depth-001/",
            "archive/manifests/lore-repository-ingestion-2026-07.json",
            "operations/campaigns/lore-repository-ingestion-2026-07/manifest.json",
        )
        label = "knowledge-narrative-depth-001"
    elif medium_campaign:
        allowed = common + (
            "archive/raw/medium/star-atlas/",
            "archive/normalized/medium/star-atlas/",
            "archive/source-records/medium/star-atlas/",
            "archive/ingestion-packages/star-atlas-medium/",
            "archive/manifests/",
            "archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/",
            "operations/campaigns/star-atlas-medium-ingestion-2026-07/",
            "operations/tests/star_atlas_medium/",
        )
        label = "star-atlas-medium-ingestion-2026-07"
    elif economic_reports_campaign:
        allowed = common + (
            "archive/raw/economic-reports/",
            "archive/provenance/economic-reports/",
            "archive/normalized/economic-reports/",
            "archive/source-records/economic-reports/",
            "archive/ingestion-packages/economic-reports-official/",
            "archive/manifests/official-economic-reports-pdf-ingestion-2026-07.json",
            "operations/campaigns/official-economic-reports-pdf-ingestion-2026-07/",
            "operations/tests/economic_reports/",
        )
        label = "official-economic-reports-pdf-ingestion-2026-07"
    elif ship_campaign:
        allowed = common + (
            "archive/raw/starbased-ship-states/",
            "archive/provenance/starbased-ship-states/",
            "archive/normalized/starbased-ship-states/",
            "operations/campaigns/starbased-ship-states-ingestion-2026-07/",
            "operations/tests/starbased_ship_states/",
        )
        label = "starbased-ship-states-ingestion-2026-07"
    elif wallet_campaign:
        allowed = common + (
            "archive/raw/community-wallet-attributions/",
            "archive/provenance/community-wallet-attributions/",
            "archive/normalized/community-wallet-attributions/",
            "archive/source-records/community-wallet-attributions/",
            "archive/manifests/community-wallet-attribution-ingestion-2026-07.json",
            "archive/manifests/lore-repository-ingestion-2026-07.json",
            "operations/campaigns/community-wallet-attribution-ingestion-2026-07/",
            "operations/campaigns/lore-repository-ingestion-2026-07/manifest.json",
            "operations/tests/community_wallet_attributions/",
        )
        label = "community-wallet-attribution-ingestion-2026-07"
    elif pip33_vote_campaign:
        allowed = common + (
            "archive/normalized/governance-votes/pip-33/",
            "archive/provenance/governance-votes/pip-33.json",
            "archive/source-records/governance-votes/",
            "archive/manifests/pip-33-onchain-vote-reconciliation-2026-07.json",
            "archive/manifests/lore-repository-ingestion-2026-07.json",
            "operations/campaigns/pip-33-onchain-vote-reconciliation-2026-07/",
            "operations/campaigns/lore-repository-ingestion-2026-07/manifest.json",
            "operations/tests/pip33_governance_votes/",
        )
        label = "pip-33-onchain-vote-reconciliation-2026-07"
    elif dao_pip_vote_campaign:
        allowed = common + (
            "archive/raw/governance-votes/pip-01-32/",
            "archive/normalized/governance-votes/pip-01-32/",
            "archive/provenance/governance-votes/pip-01-32.json",
            "archive/source-records/governance-votes/pip-01-32/",
            "archive/manifests/dao-pip-vote-evidence-ingestion-2026-07.json",
            "archive/manifests/lore-repository-ingestion-2026-07.json",
            "operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/",
            "operations/campaigns/lore-repository-ingestion-2026-07/manifest.json",
            "operations/tests/dao_pip_governance_votes/",
        )
        label = "dao-pip-vote-evidence-ingestion-2026-07"
    elif foundation_council_campaign:
        allowed = common + (
            ".gitattributes",
            "archive/raw/discord/star-atlas/foundation-room/",
            "archive/raw/discord/star-atlas/fr-chat/",
            "archive/provenance/discord/star-atlas/",
            "archive/normalized/discord/star-atlas/",
            "archive/source-records/discord/star-atlas/",
            "archive/raw/governance/council-pip-tracker/snapshots/2026-07-23/",
            "archive/provenance/governance/council-pip-tracker/snapshots/2026-07-23.json",
            "archive/normalized/governance/council-pip-tracker/snapshots/2026-07-23/",
            "archive/source-records/governance/council-pip-tracker/snapshots/2026-07-23/",
            "archive/manifests/foundation-room-council-evidence-ingestion-2026-07.json",
            "operations/campaigns/foundation-room-council-evidence-ingestion-2026-07/",
        )
        label = "foundation-room-council-evidence-ingestion-2026-07"
    elif discord_campaign:
        allowed = common + (
            "operations/campaigns/discord-community-indexing-001/",
            "operations/tests/discord_community_indexing/",
        )
        label = "discord-community-indexing-001"
    elif library_frontend:
        allowed = common + (
            "publication/README.md",
            "publication/site/",
            "operations/tests/library_frontend/",
        )
        label = "star-atlas-library-frontend"
    elif lore_campaign:
        allowed = common + (
            "archive/raw/lore-repository/",
            "archive/provenance/lore-repository/",
            "archive/normalized/lore/",
            "archive/source-records/lore-repository/",
            "archive/ingestion-packages/lore-repository/",
            "archive/manifests/lore-repository-ingestion-2026-07.json",
            "operations/campaigns/lore-repository-ingestion-2026-07/",
            "operations/tests/lore_repository/",
        )
        label = "lore-repository-ingestion-2026-07"
    elif pipeline_framework and not agent_contracts:
        allowed = common + (
            "README.md",
            "operations/README.md",
            "operations/campaigns/README.md",
            "operations/ci/README.md",
            "operations/docs/README.md",
            "operations/docs/SIMPLIFIED-PROMOTION-PIPELINE.md",
            "operations/schema/README.md",
            "operations/schema/PROMOTION-CAMPAIGN-v1.schema.json",
            "operations/schema/examples/promotion-campaign-v1.json",
            "operations/templates/README.md",
            "operations/templates/simplified-campaign-report.json",
            "operations/templates/simplified-campaign-report.md",
            "operations/tests/README.md",
            "operations/tests/promotion_pipeline/",
        )
        label = "simplified-knowledge-pipeline"
    elif agent_contracts:
        allowed = common + (
            "operations/README.md",
            "operations/agents/",
            "operations/docs/KNOWLEDGE-ARCHITECTURE.md",
            "operations/docs/SIMPLIFIED-PROMOTION-PIPELINE.md",
            "operations/templates/knowledge-entry-template.md",
            "operations/tests/README.md",
            "operations/tests/agent_contracts/",
        )
        label = "repository-agent-contracts"
    forbidden = [path for path in changes if not path.startswith(allowed)]
    if forbidden:
        raise ValidationFailure(f"{label} forbidden-path changes:\n" + "\n".join(forbidden))
    return label


def sha_tree(root: Path, exclusions: set[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        rel = path.relative_to(root).as_posix()
        if rel in exclusions or path.suffix == ".pyc" or "__pycache__" in path.parts:
            continue
        values[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return values


def run_cycle(command: list[str], root: Path, exclusions: set[str], env: dict[str, str] | None = None) -> dict[str, str]:
    run(*command, check=True, env=env)
    return sha_tree(root, exclusions)


def validate_knowledge_campaign() -> None:
    campaign = ROOT / "operations/campaigns/knowledge-narrative-depth-001"
    env = os.environ.copy()
    env.setdefault("GITHUB_BASE_REF", "main")
    command = [sys.executable, str(campaign / "build_campaign.py")]
    validate = [sys.executable, str(campaign / "validate_campaign.py")]

    # Establish a platform-local fixed point before comparing cycles. The
    # campaign manifest observes validator-generated reports, so a Linux CI
    # checkout may need one pass to normalize files produced on Windows.
    run(*command, check=True, env=env)
    run(*validate, check=True, env=env)
    run(*command, check=True, env=env)
    first = run_cycle(validate, campaign, {"build_campaign.py", "validate_campaign.py", "README.md"}, env)
    run(*command, check=True, env=env)
    second = run_cycle(validate, campaign, {"build_campaign.py", "validate_campaign.py", "README.md"}, env)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("knowledge campaign output is not deterministic: " + ", ".join(differing))
    diff = run("git", "diff", "--exit-code", "--", str(campaign.relative_to(ROOT)))
    if diff.returncode:
        raise ValidationFailure("knowledge campaign generated artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_medium_campaign() -> None:
    campaign = ROOT / "operations/campaigns/star-atlas-medium-ingestion-2026-07"
    command = [sys.executable, str(campaign / "medium_campaign.py"), "validate"]
    first = run_cycle(command, campaign, {"medium_campaign.py", "README.md"})
    second = run_cycle(command, campaign, {"medium_campaign.py", "README.md"})
    if first != second:
        raise ValidationFailure("Medium campaign validation outputs are not deterministic")
    diff = run("git", "diff", "--exit-code", "--", str(campaign.relative_to(ROOT)), "archive/manifests", "archive/campaign-summaries/star-atlas-medium-ingestion-2026-07")
    if diff.returncode:
        raise ValidationFailure("Medium campaign validation artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_economic_reports_campaign() -> None:
    campaign = ROOT / "operations/campaigns/official-economic-reports-pdf-ingestion-2026-07"
    command = [sys.executable, str(campaign / "validate_campaign.py")]
    exclusions = {"build_campaign.py", "validate_campaign.py", "README.md", "requirements.txt"}
    first = run_cycle(command, campaign, exclusions)
    second = run_cycle(command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("Economic-report campaign validation is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        "archive/raw/economic-reports",
        "archive/provenance/economic-reports",
        "archive/normalized/economic-reports",
        "archive/source-records/economic-reports",
        "archive/ingestion-packages/economic-reports-official",
        "archive/manifests/official-economic-reports-pdf-ingestion-2026-07.json",
        str(campaign.relative_to(ROOT)),
        "operations/tests/economic_reports",
    )
    if diff.returncode:
        raise ValidationFailure("Economic-report campaign artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_atlas_brew_semantic_campaign() -> None:
    campaign = ROOT / "operations/campaigns/atlas-brew-significance-review-2026-07"
    semantic = ROOT / "archive/semantic/atlas-brew"
    generate = [sys.executable, str(campaign / "review_semantic_layer.py")]
    validate = [sys.executable, str(campaign / "validate_review.py")]

    def snapshot() -> dict[str, str]:
        values = {f"semantic/{key}": value for key, value in sha_tree(semantic, set()).items()}
        values.update({f"campaign/{key}": value for key, value in sha_tree(campaign, {"review_semantic_layer.py", "validate_review.py", "README.md"}).items()})
        return values

    run(*generate, check=True)
    run(*validate, check=True)
    first = snapshot()
    run(*generate, check=True)
    run(*validate, check=True)
    second = snapshot()
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("Atlas Brew significance review is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(semantic.relative_to(ROOT)), str(campaign.relative_to(ROOT)),
    )
    if diff.returncode:
        raise ValidationFailure("Atlas Brew significance review differs after deterministic regeneration:\n" + diff.stdout + diff.stderr)


def validate_atlas_brew_url_reconciliation_campaign() -> None:
    campaign = ROOT / "operations/campaigns/atlas-brew-url-reconciliation-2026-07"
    command = [sys.executable, str(campaign / "reconcile_playlist.py"), "validate"]
    build = [sys.executable, str(campaign / "build_episode_7_artifacts.py"), "generate"]
    validate_recovery = [
        sys.executable,
        str(campaign / "build_episode_7_artifacts.py"),
        "validate",
    ]
    exclusions = {"reconcile_playlist.py", "README.md"}

    recovery_roots = [
        ROOT / "archive/raw/atlas-brew-youtube-recovery",
        ROOT / "archive/provenance/atlas-brew-youtube-recovery",
        ROOT / "archive/normalized/atlas-brew-youtube-recovery",
        ROOT / "archive/source-records/atlas-brew-youtube-recovery",
        ROOT / "archive/ingestion-packages/atlas-brew-youtube-recovery",
    ]

    def recovery_snapshot() -> dict[str, str]:
        values: dict[str, str] = {}
        for root in recovery_roots:
            values.update(
                {
                    f"{root.relative_to(ROOT).as_posix()}/{key}": value
                    for key, value in sha_tree(root, set()).items()
                }
            )
        manifest = ROOT / "archive/manifests/atlas-brew-youtube-recovery-2026-07.json"
        values[manifest.relative_to(ROOT).as_posix()] = hashlib.sha256(
            manifest.read_bytes()
        ).hexdigest()
        return values

    run(*build, check=True)
    run(*validate_recovery, check=True)
    recovery_first = recovery_snapshot()
    run(*build, check=True)
    run(*validate_recovery, check=True)
    recovery_second = recovery_snapshot()
    if recovery_first != recovery_second:
        differing = sorted(
            path
            for path in set(recovery_first) | set(recovery_second)
            if recovery_first.get(path) != recovery_second.get(path)
        )
        raise ValidationFailure(
            "Atlas Brew #7 recovery is not deterministic: " + ", ".join(differing)
        )

    first = run_cycle(command, campaign, exclusions)
    second = run_cycle(command, campaign, exclusions)
    if first != second:
        differing = sorted(
            path
            for path in set(first) | set(second)
            if first.get(path) != second.get(path)
        )
        raise ValidationFailure(
            "Atlas Brew URL reconciliation validation is not deterministic: "
            + ", ".join(differing)
        )
    diff = run(
        "git",
        "diff",
        "--exit-code",
        "--",
        str(campaign.relative_to(ROOT)),
        "archive/provenance/atlas-brew-combined/youtube-playlist-manifest.json",
        "archive/reconciliation/atlas-brew-combined/youtube-url-reconciliation.json",
        "archive/reconciliation/atlas-brew-combined/youtube-source-metadata-patch.json",
        "archive/raw/atlas-brew-youtube-recovery",
        "archive/provenance/atlas-brew-youtube-recovery",
        "archive/normalized/atlas-brew-youtube-recovery",
        "archive/source-records/atlas-brew-youtube-recovery",
        "archive/ingestion-packages/atlas-brew-youtube-recovery",
        "archive/manifests/atlas-brew-youtube-recovery-2026-07.json",
        "operations/tests/atlas_brew_url_reconciliation",
    )
    if diff.returncode:
        raise ValidationFailure(
            "Atlas Brew URL reconciliation artifacts do not reconcile with committed files:\n"
            + diff.stdout
        )


def validate_discord_campaign(base_ref: str) -> None:
    campaign = ROOT / "operations/campaigns/discord-community-indexing-001"
    command = [sys.executable, str(campaign / "validate_campaign.py"), "--base-ref", base_ref]
    exclusions = {"build_index.py", "validate_campaign.py", "README.md"}
    first = run_cycle(command, campaign, exclusions)
    second = run_cycle(command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("Discord campaign output is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(campaign.relative_to(ROOT)), "operations/tests/discord_community_indexing",
    )
    if diff.returncode:
        raise ValidationFailure("Discord campaign generated artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_foundation_council_campaign() -> None:
    campaign = ROOT / "operations/campaigns/foundation-room-council-evidence-ingestion-2026-07"
    command = [sys.executable, str(campaign / "validate_campaign.py")]
    exclusions = {"build_campaign.py", "validate_campaign.py", "README.md"}
    first = run_cycle(command, campaign, exclusions)
    second = run_cycle(command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure(
            "Foundation Room/Council campaign output is not deterministic: " + ", ".join(differing)
        )


def validate_pip_ledger_campaign() -> None:
    campaign = ROOT / "operations/campaigns/canonical-pip-governance-ledger-2026-07"
    command = [sys.executable, str(campaign / "validate_ledger.py")]
    exclusions = {"build_ledger.py", "validate_ledger.py", "README.md", "canonical-pip-governance-ledger.schema.json"}
    run(*command, check=True)
    first = run_cycle(command, campaign, exclusions)
    second = run_cycle(command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("PIP ledger campaign output is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(campaign.relative_to(ROOT)),
        "knowledge/governance/PIP-Registry.json",
        "knowledge/governance/PIP-Registry.md",
    )
    if diff.returncode:
        raise ValidationFailure("PIP ledger generated artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_phase4_knowledge_consolidation(base_ref: str) -> None:
    campaign = ROOT / "operations/campaigns/phase-4-knowledge-consolidation-2026-07"
    command = [sys.executable, str(campaign / "validate_campaign.py"), base_ref]
    exclusions = {"validate_campaign.py", "README.md"}
    first = run_cycle(command, campaign, exclusions)
    second = run_cycle(command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure(
            "Phase 4 knowledge validation is not deterministic: " + ", ".join(differing)
        )
    run(
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "operations/tests/phase4_knowledge_consolidation",
        check=True,
    )


def validate_phase5_publication_portfolio(base_ref: str) -> None:
    campaign = (
        ROOT
        / "operations/campaigns/phase-5-foundational-publication-portfolio-2026-07"
    )
    build_command = [sys.executable, str(campaign / "build_campaign.py")]
    validate_command = [
        sys.executable,
        str(campaign / "validate_campaign.py"),
        base_ref,
    ]
    exclusions = {"build_campaign.py", "validate_campaign.py", "README.md"}
    run(*build_command, check=True)
    first = run_cycle(validate_command, campaign, exclusions)
    run(*build_command, check=True)
    second = run_cycle(validate_command, campaign, exclusions)
    if first != second:
        differing = sorted(
            path
            for path in set(first) | set(second)
            if first.get(path) != second.get(path)
        )
        raise ValidationFailure(
            "Phase 5 publication validation is not deterministic: "
            + ", ".join(differing)
        )
    run(
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "operations/tests/phase5_publication_portfolio",
        check=True,
    )
    diff = run(
        "git",
        "diff",
        "--exit-code",
        "--",
        "publication/articles/",
        "publication/manifests/publication-manifest.json",
        str(campaign.relative_to(ROOT)),
        "operations/tests/phase5_publication_portfolio/",
        "operations/programs/library-roadmap/",
        "operations/coverage/campaign-status-register.json",
        "operations/coverage/campaign-status-register.md",
    )
    if diff.returncode:
        raise ValidationFailure(
            "Phase 5 generated artifacts do not reconcile with committed files:\n"
            + diff.stdout
        )


def validate_publication_contract_campaign(base_ref: str) -> None:
    campaign = ROOT / "operations/campaigns/phase-3-publication-contract-2026-07"
    command = [sys.executable, str(campaign / "validate_campaign.py"), base_ref]
    exclusions = {"validate_campaign.py", "README.md"}
    first = run_cycle(command, campaign, exclusions)
    second = run_cycle(command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure(
            "publication contract validation is not deterministic: " + ", ".join(differing)
        )
    run(
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "operations/tests/publication_contract",
        check=True,
    )


def validate_library_frontend() -> None:
    site = ROOT / "publication/site"
    run("node", str(site / "scripts/build-search-index.mjs"), "--check", check=True)
    run("node", str(site / "scripts/validate-site.mjs"), check=True)
    before = sha_tree(site, set())
    run("node", str(site / "scripts/build-search-index.mjs"), "--check", check=True)
    run("node", str(site / "scripts/validate-site.mjs"), check=True)
    after = sha_tree(site, set())
    if before != after:
        differing = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
        raise ValidationFailure("library frontend validation is not deterministic: " + ", ".join(differing))


def validate_starbased_ship_campaign() -> None:
    campaign = ROOT / "operations/campaigns/starbased-ship-states-ingestion-2026-07"
    command = [sys.executable, str(campaign / "validate_campaign.py")]
    exclusions = {"build_campaign.py", "validate_campaign.py", "README.md"}
    first = run_cycle(command, campaign, exclusions)
    second = run_cycle(command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("Starbased ship campaign output is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(campaign.relative_to(ROOT)),
        "archive/raw/starbased-ship-states",
        "archive/provenance/starbased-ship-states",
        "archive/normalized/starbased-ship-states",
        "operations/tests/starbased_ship_states",
    )
    if diff.returncode:
        raise ValidationFailure("Starbased ship campaign artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_lore_repository_campaign() -> None:
    campaign = ROOT / "operations/campaigns/lore-repository-ingestion-2026-07"
    build_command = [sys.executable, str(campaign / "build_campaign.py")]
    validate_command = [sys.executable, str(campaign / "validate_campaign.py")]
    exclusions = {"build_campaign.py", "validate_campaign.py", "README.md"}
    run(*build_command, check=True)
    first = run_cycle(validate_command, campaign, exclusions)
    run(*build_command, check=True)
    second = run_cycle(validate_command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("Lore repository campaign output is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(campaign.relative_to(ROOT)),
        "archive/raw/lore-repository",
        "archive/provenance/lore-repository",
        "archive/normalized/lore",
        "archive/source-records/lore-repository",
        "archive/ingestion-packages/lore-repository",
        "archive/manifests/lore-repository-ingestion-2026-07.json",
        "operations/tests/lore_repository",
    )
    if diff.returncode:
        raise ValidationFailure("Lore repository campaign artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_community_wallet_campaign() -> None:
    campaign = ROOT / "operations/campaigns/community-wallet-attribution-ingestion-2026-07"
    build_command = [sys.executable, str(campaign / "build_campaign.py")]
    validate_command = [sys.executable, str(campaign / "validate_campaign.py")]
    exclusions = {"build_campaign.py", "validate_campaign.py", "README.md"}
    run(*build_command, check=True)
    first = run_cycle(validate_command, campaign, exclusions)
    run(*build_command, check=True)
    second = run_cycle(validate_command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("Community wallet campaign output is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(campaign.relative_to(ROOT)),
        "archive/raw/community-wallet-attributions",
        "archive/provenance/community-wallet-attributions",
        "archive/normalized/community-wallet-attributions",
        "archive/source-records/community-wallet-attributions",
        "archive/manifests/community-wallet-attribution-ingestion-2026-07.json",
        "operations/tests/community_wallet_attributions",
    )
    if diff.returncode:
        raise ValidationFailure("Community wallet campaign artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_pip33_vote_campaign() -> None:
    campaign = ROOT / "operations/campaigns/pip-33-onchain-vote-reconciliation-2026-07"
    build_command = [sys.executable, str(campaign / "build_campaign.py")]
    validate_command = [sys.executable, str(campaign / "validate_campaign.py")]
    exclusions = {"import_vote_export.py", "build_campaign.py", "validate_campaign.py", "README.md", "source-assessment.md"}
    run(*build_command, check=True)
    first = run_cycle(validate_command, campaign, exclusions)
    run(*build_command, check=True)
    second = run_cycle(validate_command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("PIP-33 vote campaign output is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(campaign.relative_to(ROOT)),
        "archive/normalized/governance-votes/pip-33",
        "archive/provenance/governance-votes/pip-33.json",
        "archive/source-records/governance-votes",
        "archive/manifests/pip-33-onchain-vote-reconciliation-2026-07.json",
        "operations/tests/pip33_governance_votes",
    )
    if diff.returncode:
        raise ValidationFailure("PIP-33 vote campaign artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_dao_pip_vote_campaign() -> None:
    campaign = ROOT / "operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07"
    validate_command = [sys.executable, str(campaign / "validate_campaign.py")]
    exclusions = {"import_vote_export.py", "build_campaign.py", "validate_campaign.py", "README.md", "source-assessment.md"}
    first = run_cycle(validate_command, campaign, exclusions)
    second = run_cycle(validate_command, campaign, exclusions)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("DAO PIP vote campaign output is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(campaign.relative_to(ROOT)),
        "archive/raw/governance-votes/pip-01-32",
        "archive/normalized/governance-votes/pip-01-32",
        "archive/provenance/governance-votes/pip-01-32.json",
        "archive/source-records/governance-votes/pip-01-32",
        "archive/manifests/dao-pip-vote-evidence-ingestion-2026-07.json",
        "operations/tests/dao_pip_governance_votes",
    )
    if diff.returncode:
        raise ValidationFailure("DAO PIP vote campaign artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_promotion_framework() -> None:
    example = ROOT / "operations/schema/examples/promotion-campaign-v1.json"
    payload = json.loads(example.read_text(encoding="utf-8"))
    failures = validate_campaign_report(payload, root=ROOT)
    if failures:
        raise ValidationFailure("simplified promotion example is invalid:\n" + "\n".join(failures))


def validate_phase_one_inventory() -> None:
    coverage = ROOT / "operations/coverage"
    program = ROOT / "operations/programs/library-roadmap"
    command = [sys.executable, str(coverage / "validate_inventory.py")]
    exclusions = {"build_inventory.py", "validate_inventory.py", "README.md"}
    first = run_cycle(command, coverage, exclusions)
    first.update({f"program/{key}": value for key, value in sha_tree(program, set()).items()})
    second = run_cycle(command, coverage, exclusions)
    second.update({f"program/{key}": value for key, value in sha_tree(program, set()).items()})
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("Phase 1 inventory output is not deterministic: " + ", ".join(differing))
    closeout = ROOT / "operations/campaigns/phase-2-official-freshness-closeout-2026-07"
    closeout_command = [sys.executable, str(closeout / "validate_campaign.py")]
    closeout_first = run_cycle(closeout_command, closeout, {"validate_campaign.py"})
    closeout_second = run_cycle(closeout_command, closeout, {"validate_campaign.py"})
    if closeout_first != closeout_second:
        differing = sorted(
            path
            for path in set(closeout_first) | set(closeout_second)
            if closeout_first.get(path) != closeout_second.get(path)
        )
        raise ValidationFailure("Phase 2 closeout validation is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        str(coverage.relative_to(ROOT)),
        str(program.relative_to(ROOT)),
        str(closeout.relative_to(ROOT)),
        "publication/site/assets/library-index.json",
    )
    if diff.returncode:
        raise ValidationFailure("Phase 1 generated artifacts do not reconcile with committed files:\n" + diff.stdout)


def validate_legacy_written_raw_recovery_campaign() -> None:
    """Validate preserved recovery artifacts twice without invoking retrieval."""
    campaign = ROOT / "operations/campaigns/legacy-written-raw-recovery-2026-07"
    command = [sys.executable, str(campaign / "validate_campaign.py")]
    exclusions = {"validate_campaign.py"}
    env = os.environ.copy()
    env["NO_NETWORK"] = "1"
    env["STAR_ATLAS_OFFLINE_VALIDATION"] = "1"

    first = run_cycle(command, campaign, exclusions, env)
    second = run_cycle(command, campaign, exclusions, env)
    if first != second:
        differing = sorted(path for path in set(first) | set(second) if first.get(path) != second.get(path))
        raise ValidationFailure("Legacy written raw-recovery validation is not deterministic: " + ", ".join(differing))
    diff = run(
        "git", "diff", "--exit-code", "--",
        "archive/raw/legacy-written-recovery",
        "archive/provenance/legacy-written-recovery",
        "archive/manifests/legacy-written-raw-recovery-2026-07.json",
        str(campaign.relative_to(ROOT)),
        "operations/tests/legacy_written_raw_recovery",
    )
    if diff.returncode:
        raise ValidationFailure("Legacy written raw-recovery artifacts do not reconcile with committed files:\n" + diff.stdout)


def repository_mode(base_ref: str) -> None:
    documents, records = parse_json_corpus()
    schemas = validate_declared_schemas()
    extractions, markdown = validate_source_identity()
    links = validate_markdown_links()
    promotion_reports = validate_simplified_promotion_reports()
    changes = changed_paths(base_ref)
    contract = validate_forbidden_paths(changes)
    diff = run("git", "diff", "--check", f"{base_ref}...HEAD")
    if diff.returncode:
        raise ValidationFailure("git diff --check failed:\n" + diff.stdout + diff.stderr)
    print(f"PASS repository-integrity: {documents} JSON; {records} JSONL records; {schemas} schema packages; {extractions} unique extractions; {markdown} Markdown Source Records; {links} links; {promotion_reports} simplified promotion reports; contract={contract}")


def campaign_mode(base_ref: str) -> None:
    changes = changed_paths(base_ref)
    contract = validate_forbidden_paths(changes)
    if contract == "phase-5-foundational-publication-portfolio-2026-07":
        validate_phase5_publication_portfolio(base_ref)
    elif contract == "phase-4-knowledge-consolidation-2026-07":
        validate_phase4_knowledge_consolidation(base_ref)
    elif contract == "phase-3-publication-contract-2026-07":
        validate_publication_contract_campaign(base_ref)
    elif contract == "legacy-written-raw-recovery-2026-07":
        validate_legacy_written_raw_recovery_campaign()
    elif contract == "phase-one-repository-baseline":
        validate_phase_one_inventory()
    elif contract == "knowledge-narrative-depth-001":
        validate_knowledge_campaign()
    elif contract == "star-atlas-medium-ingestion-2026-07":
        validate_medium_campaign()
    elif contract == "official-economic-reports-pdf-ingestion-2026-07":
        validate_economic_reports_campaign()
    elif contract == "atlas-brew-significance-review-2026-07":
        validate_atlas_brew_semantic_campaign()
    elif contract == "atlas-brew-url-reconciliation-2026-07":
        validate_atlas_brew_url_reconciliation_campaign()
    elif contract == "discord-community-indexing-001":
        validate_discord_campaign(base_ref)
    elif contract == "foundation-room-council-evidence-ingestion-2026-07":
        validate_foundation_council_campaign()
    elif contract == "canonical-pip-governance-ledger-2026-07":
        validate_pip_ledger_campaign()
    elif contract == "star-atlas-library-frontend":
        validate_library_frontend()
    elif contract == "starbased-ship-states-ingestion-2026-07":
        validate_starbased_ship_campaign()
    elif contract == "community-wallet-attribution-ingestion-2026-07":
        validate_community_wallet_campaign()
    elif contract == "pip-33-onchain-vote-reconciliation-2026-07":
        validate_pip33_vote_campaign()
    elif contract == "dao-pip-vote-evidence-ingestion-2026-07":
        validate_dao_pip_vote_campaign()
    elif contract == "lore-repository-ingestion-2026-07":
        validate_lore_repository_campaign()
    elif contract == "simplified-knowledge-pipeline":
        validate_promotion_framework()
    elif contract == "repository-agent-contracts":
        run(sys.executable, "operations/agents/validate_contracts.py", check=True)
    print(f"PASS campaign-contracts: {contract}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("repository", "campaign"), required=True)
    parser.add_argument("--base-ref", default=os.environ.get("CI_BASE_REF", "origin/main"))
    args = parser.parse_args()
    try:
        (repository_mode if args.mode == "repository" else campaign_mode)(args.base_ref)
    except ValidationFailure as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
