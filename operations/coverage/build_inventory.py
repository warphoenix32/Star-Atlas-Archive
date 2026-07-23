"""Build the repository coverage and roadmap baseline.

The register is a snapshot of canonical ``main`` at BASELINE_SHA.  Counts are
derived from repository paths where practical; completeness statements remain
curator-authored because file counts cannot establish external completeness.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from build_url_reconciliation import write_outputs as write_url_reconciliation


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PROGRAM = ROOT / "operations" / "programs" / "library-roadmap"
AS_OF = "2026-07-22"
BASELINE_SHA = "1b47c2bdaf1aa683b5b8905323abe24cf0a02525"


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def file_count(path: str) -> int:
    root = ROOT / path
    return sum(1 for item in root.rglob("*") if item.is_file()) if root.exists() else 0


def tree_stats(path: str) -> tuple[int, int]:
    """Return tracked file count and Git-blob bytes at the audited baseline.

    Working-tree byte sizes vary with Git line-ending conversion.  Git tree
    objects are the repository's platform-independent stored representation.
    """
    result = subprocess.run(
        ["git", "ls-tree", "-r", "-l", BASELINE_SHA, "--", path],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    sizes = []
    for line in result.stdout.splitlines():
        metadata, _separator, _name = line.partition("\t")
        fields = metadata.split()
        if len(fields) >= 4 and fields[1] == "blob":
            sizes.append(int(fields[3]))
    return len(sizes), sum(sizes)


def coverage_record(
    coverage_id: str,
    source_family: str,
    medium: str,
    authority: str,
    counts: dict[str, int],
    first: str | None,
    last: str | None,
    statuses: list[str],
    basis: str,
    limits: list[str],
    evidence: list[str],
    gaps: list[str],
    refresh: str,
) -> dict[str, object]:
    return {
        "coverage_id": coverage_id,
        "source_family": source_family,
        "medium": medium,
        "authority": authority,
        "counts": counts,
        "first_supported_date": first,
        "last_supported_date": last,
        "coverage_statuses": statuses,
        "completeness_basis": basis,
        "limitations": limits,
        "evidence_paths": evidence,
        "gap_ids": gaps,
        "refresh_class": refresh,
        "last_verified": AS_OF,
        "next_review_date": (
            "2026-07-29"
            if refresh == "HIGH_FREQUENCY"
            else "2026-08-21"
            if refresh == "MEDIUM_FREQUENCY"
            else "2026-10-20"
        ),
    }


def build_coverage() -> list[dict[str, object]]:
    return [
        coverage_record(
            "COV-AEPHIA-WRITTEN", "Aephia", "written articles", "COMMUNITY_PUBLICATION",
            {"raw_files": 64, "normalized_records": 0, "source_records": 64, "semantic_records": 0, "ingestion_package_records": 64},
            "2021-12-17", "2026-07-06", ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "RAW_RECOVERY_COMPLETE", "MANUAL_REVIEW_PENDING"],
            "All 64 URLs in the normalized Campaign Alpha inventory were extracted and now have checksum-bound raw recovery bodies and provenance.",
            ["Recovered bytes are later public recaptures, not publication-date snapshots.", "All 64 records retain temporal-review warnings from the original extraction campaign."],
            ["archive/campaign-summaries/campaign-alpha-aephia/campaign-summary.json", "archive/source-records/campaign-alpha-aephia/", "archive/provenance/legacy-written-recovery/aephia/"],
            ["GAP-LEGACY-REVIEW"], "LOW_FREQUENCY",
        ),
        coverage_record(
            "COV-HERALD-WRITTEN", "Intergalactic Herald", "written articles", "COMMUNITY_PUBLICATION",
            {"raw_files": 5, "normalized_records": 0, "source_records": 259, "semantic_records": 0, "ingestion_package_records": 259},
            "2022-12-11", "2026-07-03", ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "RAW_RECOVERY_DEFERRED_BY_OPERATOR", "MANUAL_REVIEW_PENDING"],
            "259 written URLs were extracted; 151 podcasts and one landing page were excluded.",
            ["Five pilot raw captures are preserved; the remaining 254 records were not selected for recovery.", "The operator explicitly deferred Intergalactic Herald at this stage.", "Campaign summary reports 254 records requiring manual review and two duplicate articles."],
            ["archive/campaign-summaries/campaign-bravo-intergalactic-herald/campaign-summary.json", "archive/source-records/campaign-bravo-intergalactic-herald/", "archive/provenance/legacy-written-recovery/intergalactic-herald/"],
            ["GAP-HERALD-RAW-DEFERRED", "GAP-LEGACY-REVIEW"], "LOW_FREQUENCY",
        ),
        coverage_record(
            "COV-HNN-WRITTEN", "Hologram News Network", "written articles", "COMMUNITY_PUBLICATION",
            {"raw_files": 157, "normalized_records": 0, "source_records": 157, "semantic_records": 0, "ingestion_package_records": 157},
            "2022-04-08", "2025-11-11", ["PARTIAL_DATE_COVERAGE", "RAW_RECOVERY_COMPLETE", "MANUAL_REVIEW_PENDING"],
            "All 157 successfully extracted HNN Source Records now have checksum-bound raw recovery bodies and provenance.",
            ["Four original Campaign Charlie retrieval failures remain outside the frozen successful-record recovery set.", "Twelve Medium-hosted records use qualified live fallbacks because no public archive snapshot was available.", "Fifty-five original extraction records retain manual-review flags."],
            ["archive/campaign-summaries/campaign-charlie-hnn/campaign-summary.json", "archive/source-records/campaign-charlie-hnn/", "archive/provenance/legacy-written-recovery/hologram-news-network/"],
            ["GAP-HNN-WRITTEN-FAILURES"], "LOW_FREQUENCY",
        ),
        coverage_record(
            "COV-OFFICIAL-DELTA", "Official Star Atlas web corpus", "web publications and documentation", "OFFICIAL_FIRST_PARTY",
            {"raw_files": 320, "normalized_records": 0, "source_records": 320, "semantic_records": 0, "ingestion_package_records": 320},
            "2021-03-16", "2026-07-10", ["PARTIAL_DATE_COVERAGE", "CURRENT_TO_CAPTURE_DATE", "RAW_RECOVERY_COMPLETE", "MANUAL_REVIEW_PENDING"],
            "All 320 successfully extracted official Source Records now have checksum-bound raw recovery bodies and provenance across newsroom, support, build, governance, staratlas.com, and GitHub surfaces.",
            ["One original Campaign Delta retrieval failure remains outside the frozen successful-record recovery set.", "The campaign reports 1,172 reconciliation/manual-review items.", "Live recaptures are not represented as publication-date bytes; nine GitHub documents are immutable commit captures."],
            ["archive/campaign-summaries/campaign-delta-official/campaign-summary.json", "archive/source-records/campaign-delta-official/", "archive/reconciliation/campaign-delta-official/", "archive/provenance/legacy-written-recovery/official-star-atlas/"],
            ["GAP-OFFICIAL-FRESHNESS", "GAP-DELETED-OFFICIAL"], "HIGH_FREQUENCY",
        ),
        coverage_record(
            "COV-OFFICIAL-MEDIUM", "Official Star Atlas Medium", "written articles", "OFFICIAL_FIRST_PARTY",
            {"raw_files": file_count("archive/raw/medium/star-atlas"), "normalized_records": 181, "source_records": 181, "semantic_records": 0, "ingestion_package_records": 181},
            "2021-01-15", "2025-10-10", ["CONFIRMED_ARTICLE_INGESTION_COMPLETE", "PARTIAL_DATE_COVERAGE", "PUBLICATION_DISCOVERY_INCOMPLETE"],
            "All 181 confirmed included articles are ingested; all 216 review candidates have terminal dispositions, while publication discovery remains explicitly incomplete.",
            ["The 2020 publication surfaces were searched with no confirmed 2020 article included.", "No 2026 article was confirmed in the frozen manifest.", "Deleted or unindexed stories may remain undiscoverable."],
            ["archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.json", "archive/manifests/star-atlas-medium-ingestion-2026-07.json"],
            ["GAP-MEDIUM-DISCOVERY", "GAP-OFFICIAL-FRESHNESS"], "MEDIUM_FREQUENCY",
        ),
        coverage_record(
            "COV-OFFICIAL-ECONOMIC-REPORTS", "Official Star Atlas economic reports", "PDF reports and economics paper", "OFFICIAL_FIRST_PARTY",
            {"raw_files": 18, "normalized_records": 18, "source_records": 18, "semantic_records": 0, "ingestion_package_records": 18},
            "2021-08-17", "2026-07-01", ["INGESTION_COMPLETE", "OPERATOR_PROVIDED_PDF_PACKAGE", "QUARTERLY_SEQUENCE_COMPLETE_Q2_2022_TO_Q2_2026"],
            "Eighteen operator-provided official PDFs were ingested: seventeen quarterly reports from Q2 2022 through Q2 2026 and the Star Atlas economics paper.",
            ["The operator-confirmed mislabeled Q4 2026 file was excluded.", "No report body was fetched from a URL.", "Ingestion does not independently verify economic measurements."],
            ["operations/campaigns/official-economic-reports-pdf-ingestion-2026-07/campaign-summary.json", "archive/manifests/official-economic-reports-pdf-ingestion-2026-07.json"],
            ["GAP-OFFICIAL-FRESHNESS"], "MEDIUM_FREQUENCY",
        ),
        coverage_record(
            "COV-OFFICIAL-DISCORD", "Star Atlas Discord, repository-designated announcements export", "Discord messages", "OFFICIAL_COMMUNICATION_SURFACE_IDENTITY_UNRESOLVED",
            {"raw_files": file_count("archive/raw/discord-announcements"), "normalized_records": 1071, "source_records": 1071, "semantic_records": 1071, "ingestion_package_records": 0},
            "2021-03-16", "2026-07-12", ["CONTINUOUS_REPRESENTED_INTERVAL", "CURRENT_TO_CAPTURE_DATE", "PARTIAL_DATE_COVERAGE"],
            "One imported export contains 1,071 unique messages and at least one message in every represented month.",
            ["No native server, channel, message, or author IDs were captured.", "The filename title is the first-message title, not a native channel name.", "A 180-minute acquisition limit was reached.", "Fourteen no-text or attachment-only records require review.", "No other Discord channel is ingested."],
            ["operations/campaigns/discord-community-indexing-001/discord-channel-coverage.json", "operations/campaigns/discord-community-indexing-001/discord-channel-gap-report.json"],
            ["GAP-DISCORD-CHANNELS", "GAP-DISCORD-NATIVE-IDS", "GAP-DISCORD-ATTACHMENTS", "GAP-OFFICIAL-FRESHNESS"], "HIGH_FREQUENCY",
        ),
        coverage_record(
            "COV-OFFICIAL-X", "Official @staratlas X account", "social posts", "OFFICIAL_FIRST_PARTY_ACCOUNT",
            {"raw_files": file_count("archive/raw/social-governance-semantic-enrichment/social-media"), "normalized_records": 796, "source_records": 796, "semantic_records": 796, "ingestion_package_records": 0},
            "2024-11-05", "2026-07-14", ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "PARTIAL_DATE_COVERAGE", "FRESHNESS_CANDIDATES_QUEUED"],
            "The supplied export contains 799 rows and 796 unique posts.",
            ["The export does not establish complete account history before 2024-11-05.", "Linked media binaries are absent.", "Nine official posts visible after 2026-07-14 are queued but not yet preserved."],
            ["operations/campaigns/social-governance-semantic-enrichment/campaign-summary.json", "archive/semantic/social-media/", "operations/campaigns/phase-2-official-freshness-closeout-2026-07/discovery-candidate-queue.json"],
            ["GAP-X-HISTORY", "GAP-OFFICIAL-FRESHNESS"], "HIGH_FREQUENCY",
        ),
        coverage_record(
            "COV-ATLAS-BREW", "Atlas Brew", "video transcripts", "COMMUNITY_BROADCAST",
            {"raw_files": 1, "normalized_records": 123, "source_records": 123, "semantic_records": 4937, "ingestion_package_records": 123},
            None, None, ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "MISSING_REQUIRED_ARTIFACT", "MANUAL_REVIEW_PENDING"],
            "All 123 sources in the supplied combined transcript were preserved and segmented.",
            ["Original URLs and publication dates are absent for all 123 sources.", "Speaker identity is normally UNKNOWN under the approved significance policy."],
            ["operations/campaigns/atlas-brew-combined/campaign-summary.json", "operations/campaigns/atlas-brew-significance-review-2026-07/campaign-summary.json", "archive/semantic/atlas-brew/"],
            ["GAP-ATLAS-BREW-METADATA"], "MEDIUM_FREQUENCY",
        ),
        coverage_record(
            "COV-HNN-TRANSCRIPTS", "HNN combined transcript", "video transcripts", "COMMUNITY_BROADCAST",
            {"raw_files": 1, "normalized_records": 85, "source_records": 85, "semantic_records": 0, "ingestion_package_records": 85},
            None, None, ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "MISSING_REQUIRED_ARTIFACT"],
            "All 85 sources in the supplied combined transcript were preserved.",
            ["Original URLs and publication dates are absent for all 85 sources.", "No dedicated HNN transcript semantic evaluation exists."],
            ["operations/campaigns/hnn-combined-transcript/campaign-summary.json", "archive/source-records/hnn-combined-transcript/"],
            ["GAP-HNN-TRANSCRIPT-METADATA", "GAP-HNN-TRANSCRIPT-SEMANTICS"], "LOW_FREQUENCY",
        ),
        coverage_record(
            "COV-OFFICIAL-TRANSCRIPTS", "Town Hall, DAO, and Economic Forum transcript package", "video transcripts", "MIXED_OFFICIAL_BROADCAST",
            {"raw_files": 36, "normalized_records": 36, "source_records": 36, "semantic_records": 1910, "ingestion_package_records": 0},
            None, None, ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "PARTIAL_DATE_COVERAGE", "MISSING_REQUIRED_ARTIFACT"],
            "All 36 supplied transcripts and 78,752 caption lines were preserved.",
            ["Original URLs are absent.", "Only three sources have exact publication dates; 18 dates are unknown and the remainder have partial precision."],
            ["operations/campaigns/star-atlas-transcripts-ingestion-2026-07/campaign-summary.json", "archive/semantic/star-atlas-transcripts/"],
            ["GAP-OFFICIAL-TRANSCRIPT-METADATA", "GAP-OFFICIAL-BROADCAST-INVENTORY"], "MEDIUM_FREQUENCY",
        ),
        coverage_record(
            "COV-LORE-REPOSITORY", "Star Atlas Lore Repository", "GitHub documentation and lore pages", "ATMTA_AFFILIATED_CANONICAL_LORE_AUTHORITY",
            {"raw_files": 526, "normalized_records": 192, "source_records": 192, "semantic_records": 0, "structured_entity_relationship_records": 8430, "ingestion_package_records": 192},
            None, "2026-06-29", ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "CURRENT_TO_CAPTURE_DATE"],
            "Immutable upstream commit 22555f277eb1496e34c0839c8f1f382842bd1d2b was preserved; 192 canonical source pages were normalized.",
            ["Eighty-six mirror divergences and 252 unresolved internal links remain documented.", "Ninety-seven working-material pages were preserved but excluded."],
            ["operations/campaigns/lore-repository-ingestion-2026-07/campaign-summary.json", "archive/manifests/lore-repository-ingestion-2026-07.json"],
            ["GAP-LORE-REFERENCES", "GAP-OFFICIAL-FRESHNESS"], "LOW_FREQUENCY",
        ),
        coverage_record(
            "COV-GOVERNANCE-PIPS", "Star Atlas governance and Council PIP tracker", "governance records and spreadsheet", "OFFICIAL_AND_COUNCIL_OPERATIONAL",
            {"raw_files": file_count("archive/raw/governance") + file_count("archive/raw/social-governance-semantic-enrichment/governance"), "normalized_records": 152, "source_records": 152, "semantic_records": 152, "ingestion_package_records": 0},
            None, "2026-07-10", ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "MANUAL_REVIEW_PENDING", "CURRENT_TO_CAPTURE_DATE"],
            "PIP-1 through PIP-33 and 119 Council tracker/rubric records are represented.",
            ["Implementation evidence is missing for all 33 PIPs.", "Council-reported status remains distinct from independent verification.", "Election winner identities for PIP-11, PIP-25, and PIP-27 remain unresolved."],
            ["operations/campaigns/canonical-pip-governance-ledger-2026-07/campaign-summary.json", "operations/campaigns/council-pip-tracker-ingestion/campaign-summary.json"],
            ["GAP-GOVERNANCE-IMPLEMENTATION", "GAP-ONCHAIN-EVIDENCE", "GAP-OFFICIAL-FRESHNESS"], "HIGH_FREQUENCY",
        ),
        coverage_record(
            "COV-PIP33-VOTES", "PIP-33 vote event reconciliation", "Solana vote export", "OPERATOR_SUPPLIED_CHAIN_DERIVED_DATA",
            {"raw_files": 1, "normalized_records": 220, "source_records": 1, "semantic_records": 0, "ingestion_package_records": 0},
            "2026-06-27", "2026-07-10", ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "PROVENANCE_METADATA_CORRECTION_PENDING"],
            "All 220 effective ballot records in the supplied normalized dataset were reconciled.",
            ["The exact PIP-33 source artifact is preserved as a member of the later PIP-1 through PIP-32 raw ZIP, but the older per-PIP provenance sidecar still predates that preservation.", "Signature replay and payment or implementation verification were not performed."],
            ["operations/campaigns/pip-33-onchain-vote-reconciliation-2026-07/campaign-summary.json", "archive/provenance/governance-votes/pip-33.json", "archive/raw/governance-votes/pip-01-32/Star Atlas DAO PIP Votes.zip"],
            ["GAP-PIP33-PROVENANCE-CORRECTION", "GAP-ONCHAIN-EVIDENCE"], "HIGH_FREQUENCY",
        ),
        coverage_record(
            "COV-DAO-PIP-VOTE-EVIDENCE", "DAO PIP-1 through PIP-32 vote evidence", "Solana vote export", "OPERATOR_SUPPLIED_CHAIN_DERIVED_DATA",
            {"raw_files": 1, "normalized_records": 8404, "source_records": 32, "semantic_records": 0, "ingestion_package_records": 0},
            "2024-07-10", "2026-06-11", ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "MANUAL_REVIEW_PENDING"],
            "The operator-supplied ZIP, 8,404 vote events, 32 proposal summaries, and 32 paired Source Records are preserved.",
            ["Five ranked-choice elections retain candidate-level totals without final STV recomputation.", "The campaign reports 278 timestamp-order anomalies.", "No independent RPC re-verification, payment inference, or implementation inference was performed."],
            ["operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/campaign-summary.json", "archive/manifests/dao-pip-vote-evidence-ingestion-2026-07.json"],
            ["GAP-ONCHAIN-EVIDENCE", "GAP-GOVERNANCE-IMPLEMENTATION"], "HIGH_FREQUENCY",
        ),
        coverage_record(
            "COV-SHIP-STATES", "Starbased base ship states", "spreadsheet/CSV", "COMMUNITY_COPY_OF_OFFICIAL_BASE_VALUES",
            {"raw_files": file_count("archive/raw/starbased-ship-states"), "normalized_records": 63, "source_records": 0, "semantic_records": 0, "ingestion_package_records": 0},
            None, "2026-07-18", ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "MANUAL_REVIEW_PENDING"],
            "All 63 supplied base-ship rows were normalized.",
            ["Authoritative Star Atlas URL/version is missing.", "Future rebasing is expected; Holosim uses a different value system.", "Marketplace ID linkage and several units remain unresolved."],
            ["operations/campaigns/starbased-ship-states-ingestion-2026-07/campaign-summary.json", "archive/provenance/starbased-ship-states/"],
            ["GAP-SHIP-UPSTREAM"], "LOW_FREQUENCY",
        ),
        coverage_record(
            "COV-COMMUNITY-WALLETS", "Community wallet attributions", "spreadsheet", "COMMUNITY_ATTRIBUTION_UNCONFIRMED",
            {"raw_files": 1, "normalized_records": 84, "source_records": 1, "semantic_records": 0, "ingestion_package_records": 0},
            None, "2026-07-19", ["PRESERVED_COMPLETE_FOR_PROVIDED_PACKAGE", "MANUAL_REVIEW_PENDING"],
            "All 84 unique addresses in the supplied workbook were normalized.",
            ["All ownership/control attributions remain unverified.", "No on-chain analysis was performed.", "Compiler, method, and compilation date are unknown."],
            ["operations/campaigns/community-wallet-attribution-ingestion-2026-07/campaign-summary.json", "archive/manifests/community-wallet-attribution-ingestion-2026-07.json"],
            ["GAP-WALLET-ATTRIBUTION", "GAP-ONCHAIN-EVIDENCE"], "LOW_FREQUENCY",
        ),
    ]


def build_backlog() -> list[dict[str, object]]:
    rows = [
        ("GAP-RAW-WRITTEN", "P0", "Legacy Alpha-Delta immutable raw captures", "Maintain the closed selected-scope recovery baseline: Aephia 64/64, HNN 157/157, and Official 320/320; five Herald pilot captures remain preserved separately.", "Archive Steward", "CLOSED_SELECTED_SCOPE_COMPLETE"),
        ("GAP-HERALD-RAW-DEFERRED", "P2", "Intergalactic Herald raw recovery", "Retain the frozen 259-record inventory and five preserved pilot captures; do not recover the remaining 254 records unless the operator reopens this source family.", "Archive Steward", "DEFERRED_BY_OPERATOR"),
        ("GAP-DISCORD-CHANNELS", "P0", "Additional Star Atlas Discord channels", "Provide privacy-reviewed native exports for Atlas Amphitheater, Atlas Brew Lounge, DAO announcements, economics, faction, Foundation Room, general, governance, guild, and support channels.", "Ingestion Coordinator", "DEFERRED_MISSING_OPERATOR_ARTIFACT"),
        ("GAP-OFFICIAL-FRESHNESS", "P0", "Recurring official-source freshness", "Acquire the ten candidates from the 2026-07-22 queue, then repeat read-only discovery on the cadence in refresh-policy.json.", "Research and Gap Analyst", "CHECK_COMPLETE_10_CANDIDATES_QUEUED"),
        ("GAP-URL-INVENTORY", "P0", "Historical normalized URL dispositions", "Retain the immutable inventory and refresh the deterministic overlay when a relevant campaign closes.", "Archive Steward", "CLOSED_BY_RECONCILIATION_OVERLAY"),
        ("GAP-ATLAS-BREW-METADATA", "P1", "Atlas Brew URLs and dates", "Provide or discover an authoritative 123-episode mapping of video ID, URL, and publication date; speaker mapping remains optional.", "Research and Gap Analyst", "DEFERRED_MISSING_OPERATOR_ARTIFACT"),
        ("GAP-OFFICIAL-TRANSCRIPT-METADATA", "P1", "Town Hall/DAO/Economic Forum URLs and dates", "Provide program inventories or source URLs for all 36 supplied transcripts.", "Research and Gap Analyst", "DEFERRED_MISSING_OPERATOR_ARTIFACT"),
        ("GAP-OFFICIAL-BROADCAST-INVENTORY", "P1", "Complete official broadcast inventories", "Build bounded episode inventories for Town Halls, DAO discussions, Economic Forums, and other official broadcast programs when source mappings are available.", "Research and Gap Analyst", "DEFERRED_TO_PHASE_3_RESEARCH"),
        ("GAP-HNN-TRANSCRIPT-METADATA", "P1", "HNN transcript URLs and dates", "Provide an 85-source episode map or authoritative channel inventory.", "Research and Gap Analyst", "DEFERRED_MISSING_OPERATOR_ARTIFACT"),
        ("GAP-HNN-TRANSCRIPT-SEMANTICS", "P1", "HNN transcript significance evaluation", "Run the approved context-sensitive transcript policy against the preserved normalized corpus in a future evidence-prioritized campaign.", "Knowledge Curator", "DEFERRED_TO_FUTURE_SEMANTIC_CAMPAIGN"),
        ("GAP-MEDIUM-DISCOVERY", "P1", "Medium publication discovery", "Maintain the 181 confirmed-article corpus and repeat publication-native discovery; all 216 prior review candidates now have terminal dispositions.", "Ingestion Coordinator", "CURRENT_CHECK_NO_NEW_RSS_CANDIDATE"),
        ("GAP-PIP33-RAW", "P1", "Original PIP-33 vote export", "Retain the checksum-identical PIP-33 member preserved inside the later DAO PIP vote ZIP.", "Archive Steward", "CLOSED_ARTIFACT_PRESERVED_IN_PR49_CONTAINER"),
        ("GAP-PIP33-PROVENANCE-CORRECTION", "P2", "PIP-33 provenance sidecar predates raw preservation", "Correct the per-PIP provenance sidecar in a manifest-aware campaign without rewriting vote evidence.", "Archive Steward", "KNOWN_METADATA_DEBT"),
        ("GAP-ONCHAIN-EVIDENCE", "P1", "Treasury/payment/execution evidence", "Provide scoped Solana transaction, account, program, and slot data before any on-chain verification claim.", "Solana Evidence Specialist", "MISSING_REQUIRED_ARTIFACT"),
        ("GAP-ECONOMIC-REPORT-BRANCH", "P1", "Unmerged economic-report discovery registry", "Retire the obsolete discovery branch after PR #57 preserved the complete operator-provided 18-PDF corpus and every 17-URL quarterly seed through Q2 2026.", "Lead Coordinator", "CLOSED_REPLACED_BY_PR57"),
        ("GAP-X-HISTORY", "P2", "Official X history before 2024-11-05", "Provide an earlier account export or bounded archive discovery manifest.", "Ingestion Coordinator", "PARTIAL_DATE_COVERAGE"),
        ("GAP-DISCORD-NATIVE-IDS", "P2", "Discord native identifiers", "Provide privacy-reviewed exports retaining server, channel, message, author IDs, and timezone offsets.", "Archive Steward", "DEFERRED_MISSING_OPERATOR_ARTIFACT"),
        ("GAP-DISCORD-ATTACHMENTS", "P2", "Fourteen Discord attachment-only placeholders", "Provide attachment metadata or a corrected export.", "Archive Steward", "MANUAL_REVIEW_PENDING"),
        ("GAP-LORE-REFERENCES", "P2", "Lore upstream link and mirror reconciliation", "Review 252 unresolved links and 86 mirror divergences without rewriting the immutable snapshot.", "Taxonomy Steward", "MANUAL_REVIEW_PENDING"),
        ("GAP-LEGACY-REVIEW", "P2", "Legacy article review queues", "Normalize the meaning and disposition of Alpha, Bravo, and Delta campaign review flags.", "Risk and Review Agent", "MANUAL_REVIEW_PENDING"),
        ("GAP-HNN-WRITTEN-FAILURES", "P2", "Four HNN written retrieval failures", "Retry or locate archived snapshots for the documented failed URLs.", "Ingestion Coordinator", "MISSING_REQUIRED_ARTIFACT"),
        ("GAP-DELETED-OFFICIAL", "P2", "Deleted or moved official pages", "Run archive-index discovery and retain live/archive provenance separately.", "Ingestion Coordinator", "UNKNOWN"),
        ("GAP-GOVERNANCE-IMPLEMENTATION", "P2", "PIP implementation evidence", "Resolve the seven prioritized governance research items and retain Council reports as attributed evidence.", "Research and Gap Analyst", "MISSING_REQUIRED_ARTIFACT"),
        ("GAP-SHIP-UPSTREAM", "P3", "Authoritative ship-state version", "Provide official document URL/version and marketplace ID mapping when available.", "Research and Gap Analyst", "MISSING_REQUIRED_ARTIFACT"),
        ("GAP-WALLET-ATTRIBUTION", "P3", "Community wallet methodology", "Identify compiler, method, and date; preserve all ownership claims as community attribution until independently supported.", "Research and Gap Analyst", "MANUAL_REVIEW_PENDING"),
        ("GAP-CROSS-PLATFORM-LINE-ENDINGS", "P3", "Cross-platform generated-artifact line endings", "Adopt a scoped line-ending policy for deterministic generated lore artifacts without bulk-renormalizing preserved evidence.", "Archive Steward", "KNOWN_VALIDATION_LIMITATION"),
    ]
    return [
        {"gap_id": gid, "priority": priority, "title": title, "required_artifact_or_action": action, "owner": owner, "status": status, "tracking_issue": 31, "last_verified": AS_OF}
        for gid, priority, title, action, owner, status in rows
    ]


def build_campaigns() -> list[dict[str, object]]:
    rows = [
        ("atlas-brew-combined", "READY_FOR_REVIEW", "operations/campaigns/atlas-brew-combined/campaign-summary.json", "Promoted evidence exists; campaign state is stale."),
        ("atlas-brew-significance-review-2026-07", "READY_FOR_REVIEW", "operations/campaigns/atlas-brew-significance-review-2026-07/campaign-summary.json", "Selective candidates remain review inputs."),
        ("canonical-pip-governance-ledger-2026-07", "DRAFT_FOR_REVIEW", "operations/campaigns/canonical-pip-governance-ledger-2026-07/campaign-summary.json", "Eleven conflicts and seven research items remain documented."),
        ("community-wallet-attribution-ingestion-2026-07", "COMPLETE_WITH_RETAINED_RESEARCH_GAPS", "operations/campaigns/community-wallet-attribution-ingestion-2026-07/campaign-summary.json", "All 84 attribution records remain unverified."),
        ("council-pip-tracker-ingestion", "GENERATED", "operations/campaigns/council-pip-tracker-ingestion/campaign-summary.json", "Council reporting is not independent implementation verification."),
        ("dao-pip-vote-evidence-ingestion-2026-07", "READY_FOR_ARCHIVAL_REVIEW", "operations/campaigns/dao-pip-vote-evidence-ingestion-2026-07/campaign-summary.json", "8,404 vote events and 32 proposal summaries are preserved; STV, RPC, payment, and implementation limits remain."),
        ("discord-announcements-semantic-enrichment", "GENERATED_WITH_CORRECTIONS", "operations/campaigns/discord-announcements-semantic-enrichment/review-correction-status.json", "Twenty-four generated event sequences were withdrawn; effective count is zero."),
        ("discord-community-indexing-001", "VALIDATED_WITH_DEFERRED_IDENTITIES", "operations/campaigns/discord-community-indexing-001/validation-report.json", "Michael and EMP remain explicitly deferred; no native channel identity is established."),
        ("hnn-combined-transcript", "READY_FOR_REVIEW", "operations/campaigns/hnn-combined-transcript/campaign-summary.json", "Metadata and semantic gaps remain."),
        ("knowledge-campaign-003-institutional-expansion", "COMPLETED_HISTORICAL", "operations/campaigns/knowledge-campaign-003-institutional-expansion/campaign-summary.md", "Ten candidates were accepted; the remaining candidate queue was preserved."),
        ("knowledge-context-refresh-2026-07-17", "PASS_WITH_RETAINED_GAPS", "operations/campaigns/knowledge-context-refresh-2026-07-17/campaign-summary.json", "Fourteen knowledge outputs were created or expanded with evidence packets."),
        ("knowledge-generation-wave-2", "PASS_WITH_CURATOR_APPROVED_SCOPE_EXTENSION", "operations/campaigns/knowledge-generation-wave-2/execution/campaign-summary.json", "Planning and Wave 2A execution artifacts are retained as completed campaign history."),
        ("knowledge-narrative-depth-001", "MERGED_VALIDATION_REPAIRED", "operations/campaigns/knowledge-narrative-depth-001/closeout-2026-07/campaign-summary.json", "All 80 pages were reviewed; branch-relative validator repaired in this baseline."),
        ("legacy-written-raw-recovery-2026-07", "SELECTED_SCOPE_COMPLETE", "operations/campaigns/legacy-written-raw-recovery-2026-07/campaign-summary.json", "Aephia 64/64, HNN 157/157, and Official 320/320 are preserved; five Herald pilot captures remain and the family is otherwise deferred by operator direction."),
        ("lore-repository-ingestion-2026-07", "ARCHIVED_NORMALIZED_CURATOR_ADJUDICATED", "operations/campaigns/lore-repository-ingestion-2026-07/campaign-summary.json", "Upstream link and mirror gaps retained."),
        ("official-economic-reports-pdf-ingestion-2026-07", "INGESTION_COMPLETE", "operations/campaigns/official-economic-reports-pdf-ingestion-2026-07/campaign-summary.json", "Eighteen operator-provided official PDFs were ingested; the mislabeled Q4 2026 upload was excluded."),
        ("phase-2-official-freshness-closeout-2026-07", "PHASE_2_GATE_COMPLETE", "operations/campaigns/phase-2-official-freshness-closeout-2026-07/campaign-summary.json", "Seven official surfaces were checked; ten unmatched candidates were queued without ingestion."),
        ("pip-33-onchain-vote-reconciliation-2026-07", "PASS_WITH_RAW_EXPORT_GAP", "operations/campaigns/pip-33-onchain-vote-reconciliation-2026-07/campaign-summary.json", "No payment, implementation, or signature replay claim."),
        ("social-governance-semantic-enrichment", "PASS", "operations/campaigns/social-governance-semantic-enrichment/validation-report.json", "Stale top-level FAIL corrected in this baseline."),
        ("star-atlas-medium-ingestion-2026-07", "CONFIRMED_ARTICLE_INGESTION_COMPLETE_PUBLICATION_DISCOVERY_INCOMPLETE", "archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.json", "All 181 confirmed articles are ingested; all 216 review candidates have terminal dispositions, while external discovery remains incomplete."),
        ("star-atlas-transcripts-ingestion-2026-07", "READY_FOR_ARCHIVAL_REVIEW", "operations/campaigns/star-atlas-transcripts-ingestion-2026-07/campaign-summary.json", "Program-level completeness and source metadata remain unresolved."),
        ("star-atlas-transcripts-semantic-2026-07", "READY_FOR_SEMANTIC_REVIEW", "operations/campaigns/star-atlas-transcripts-semantic-2026-07/campaign-summary.json", "Selective candidate layer validated."),
        ("starbased-ship-states-ingestion-2026-07", "QUALIFIED_NORMALIZATION", "operations/campaigns/starbased-ship-states-ingestion-2026-07/campaign-summary.json", "Four research gaps retained."),
    ]
    return [{"campaign_id": cid, "status": status, "status_evidence": path, "note": note} for cid, status, path, note in rows]


def build_cleanup() -> list[dict[str, object]]:
    return [
        {"cleanup_id": "CLN-001", "classification": "REPAIR", "paths": ["publication/site/assets/library-index.json"], "finding": "Committed generated index was stale and blocked Pages.", "action": "Regenerate now; keep until publication architecture changes."},
        {"cleanup_id": "CLN-002", "classification": "RETIRE_AFTER_REPLACEMENT", "paths": ["operations/migrations/validate_wave_1_5.py", "operations/tests/README.md"], "finding": "Snapshot validator hard-codes obsolete counts and is still advertised as current.", "action": "Remove from active test guidance; retain as clearly historical until manifest-based replacement is complete."},
        {"cleanup_id": "CLN-003", "classification": "CONDENSE_AFTER_REFERENCE_MIGRATION", "paths": ["archive/normalized/discord-announcements/messages/"], "finding": "1,071 per-message JSON files duplicate the aggregate JSONL as a generated access form.", "action": "Do not delete until every individual-path citation migrates and deterministic regeneration is proven."},
        {"cleanup_id": "CLN-004", "classification": "RETAIN_PROVENANCE", "paths": ["operations/campaigns/star-atlas-medium-ingestion-2026-07/discovery-captures/profile-rss-medium.xml", "operations/campaigns/star-atlas-medium-ingestion-2026-07/discovery-captures/profile-rss.xml"], "finding": "Byte-identical captures represent separately observed endpoints and are both manifest-bound.", "action": "Retain unless a schema migration preserves endpoint provenance another way."},
        {"cleanup_id": "CLN-005", "classification": "RELOCATE_NOT_DELETE", "paths": ["operations/campaigns/star-atlas-medium-ingestion-2026-07/discovery-captures/", "operations/campaigns/star-atlas-medium-ingestion-2026-07/identity-captures/", "operations/campaigns/discord-announcements-semantic-enrichment/input-package/"], "finding": "Approximately 11.9 MB of source-like captures live under operations.", "action": "Move only in a dedicated manifest/checksum migration."},
        {"cleanup_id": "CLN-006", "classification": "CONDENSE_DURING_PUBLICATION_REWRITE", "paths": ["publication/articles/README.md", "publication/briefs/README.md", "publication/datasets/README.md", "publication/reports/README.md"], "finding": "Four placeholder files can become one publication contract when the new publication layer is implemented.", "action": "Retain during the current GitHub Pages transition."},
        {"cleanup_id": "CLN-007", "classification": "ARCHIVE_RETAIN", "paths": ["operations/campaigns/knowledge-generation-wave-2/", "operations/campaigns/knowledge-context-refresh-2026-07-17/", "operations/campaigns/knowledge-narrative-depth-001/"], "finding": "Older and nested campaign artifacts preserve evidence packets, decisions, and closeout history.", "action": "Index as completed legacy work; do not bulk-delete."},
        {"cleanup_id": "CLN-008", "classification": "BRANCH_HYGIENE", "paths": ["merged remote topic branches", "origin/ingestion/economic-reports-2022q2-2026q2"], "finding": "Merged branch refs remain; the obsolete economic-report discovery branch has now been superseded by PR #57.", "action": "The economic-report branch is eligible for retirement because all unique discovery value is preserved; delete remote refs only under branch-cleanup authority."},
        {"cleanup_id": "CLN-009", "classification": "RETAIN_COMPATIBILITY", "paths": ["archive/manifests/*", "operations/campaigns/*/manifest.json", "campaign-local normalized previews"], "finding": "Several byte-identical files serve distinct archive, campaign, or review roles.", "action": "Retain until a documented schema migration removes the compatibility role."},
        {"cleanup_id": "CLN-010", "classification": "REPAIR_LATER", "paths": [".gitattributes", "archive/raw/lore-repository/", "archive/normalized/lore/"], "finding": "Windows Git line-ending conversion makes one lore fixed-point test fail locally although Linux repository CI passes.", "action": "Add a scoped line-ending contract in a dedicated compatibility change; do not bulk-renormalize preserved lore evidence in Phase 1."},
    ]


def build_economic_branch_assessment() -> dict[str, object]:
    return {
        "assessment_id": "ECONOMIC-REPORT-BRANCH-PHASE-1",
        "as_of": AS_OF,
        "baseline_sha": BASELINE_SHA,
        "branch": "origin/ingestion/economic-reports-2022q2-2026q2",
        "fork_point": "add2221f",
        "unique_commits": ["1cd5d25", "215029c"],
        "commits_behind_main": 126,
        "unique_files": [
            "archive/source-records/economic-reports/economic-report-registry.json",
            "operations/campaigns/economic-reports-complete-ingestion-2026-07-18/README.md",
        ],
        "discovery_urls": 17,
        "coverage": "Q2 2022 through Q2 2026",
        "decision": "CLOSED_REPLACED_BY_PR57",
        "merge_or_cherry_pick": False,
        "human_adjudication_required": False,
        "reason": "PR #57 ingested the operator-provided official PDF package, including all seventeen quarterly periods represented by the discovery seed through Q2 2026 plus the economics paper.",
        "deficiencies": [
            "No paired report JSON and Markdown Source Records",
            "No titles, authors, publication dates, immutable raw PDFs, or content checksums",
            "No campaign manifest, deterministic generator, or validator",
            "Fourteen reports are described as parsed although the extracted text is not retained",
        ],
        "phase_2_requirements": [
            "SATISFIED: all seventeen quarterly periods have immutable operator-provided PDFs",
            "SATISFIED: raw files, normalized records, paired Source Records, ingestion package, manifest, and validation are present",
            "SATISFIED: the operator-confirmed mislabeled Q4 2026 file is excluded and documented",
            "SATISFIED: no exact duplicate document was introduced",
        ],
        "branch_retirement_condition": "SATISFIED_BY_PR57; remote branch retirement is repository hygiene and does not affect preserved evidence.",
    }


def build_recovery_schedule() -> dict[str, object]:
    return {
        "schedule_id": "PHASE-2-LEGACY-WRITTEN-RAW-RECOVERY",
        "as_of": AS_OF,
        "status": "SELECTED_SCOPE_COMPLETE",
        "collection_started": True,
        "milestone_closed": True,
        "frozen_scope_records": 800,
        "selected_scope_records": 541,
        "selected_scope_completed_records": 541,
        "additional_preserved_herald_pilot_records": 5,
        "total_raw_bodies_preserved": 546,
        "pilot_records": 20,
        "batches": [
            {"batch_id": "R0.1", "source_family": "HNN written corpus", "records": 157, "captured_records": 157, "status": "COMPLETE", "priority": "P0", "reason": "Highest link-rot risk"},
            {"batch_id": "R0.2", "source_family": "Aephia", "records": 64, "captured_records": 64, "status": "COMPLETE", "priority": "P0"},
            {"batch_id": "R0.3", "source_family": "Intergalactic Herald", "records": 259, "captured_records": 5, "status": "DEFERRED_BY_OPERATOR", "priority": "P0", "note": "Five pilot captures are retained; the remaining 254 records are outside the selected completion scope."},
            {"batch_id": "R0.4", "source_family": "Official Campaign Delta", "records": 320, "captured_records": 320, "status": "COMPLETE", "priority": "P0", "sub_batches": ["support", "newsroom and experience", "build, governance, and main site", "immutable staratlasmeta GitHub documentation"]},
        ],
        "scope_decision": "The milestone is closed for the operator-approved 541-record Aephia, HNN, and Official scope. Intergalactic Herald remains frozen and deferred; it is not represented as recovered.",
        "retrieval_tiers": [
            "EXACT_PUBLIC_LIVE_CANONICAL",
            "PROVEN_FIRST_PARTY_REDIRECT_OR_REPLACEMENT",
            "IMMUTABLE_GIT_COMMIT_OR_BLOB",
            "PUBLIC_WEB_ARCHIVE_EXACT_URL",
            "ARCHIVED_PREDECESSOR_WITH_IDENTITY_PROOF",
        ],
        "terminal_dispositions": [
            "CAPTURED_LIVE",
            "CAPTURED_ARCHIVE",
            "CAPTURED_IMMUTABLE_GIT",
            "NOT_FOUND_EXHAUSTED",
            "AMBIGUOUS_MANUAL_REVIEW",
            "BLOCKED_ACCESS_OR_POLICY",
        ],
        "required_capture_fields": [
            "source_id", "original_url", "final_url", "retrieval_tier", "capture_utc",
            "http_status", "content_type", "byte_count", "headers", "redirect_chain",
            "raw_sha256", "snapshot_timestamp_or_git_sha", "identity_comparison", "temporal_qualifier",
        ],
        "stop_rules": [
            "Every frozen Source ID must receive exactly one terminal disposition.",
            "Three consecutive host-level 403, 429, or challenge responses stop that host batch without bypass.",
            "Identity mismatch, conflicting historic versions, or checksum failure stops only that item for review.",
            "New articles enter an out-of-scope discovery ledger and are not retrieved under this campaign.",
            "Nondeterministic identifiers, manifests, or checksums block campaign promotion.",
        ],
        "provenance_boundary": [
            "A live recapture is not represented as historical publication-date bytes.",
            "A web archive is a preservation carrier, not the publisher.",
            "Existing normalized evidence and Source Records remain unchanged.",
            "Search engines and aggregators are discovery-only and cannot supply the preserved article body.",
        ],
        "human_approval_points": [
            "Use of authenticated or restricted sources",
            "Ambiguous Source ID or URL identity matches",
            "Selection among conflicting historical versions",
            "Expansion to newly discovered articles",
        ],
    }


def markdown_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in rows)
    return lines


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    PROGRAM.mkdir(parents=True, exist_ok=True)
    write_url_reconciliation(HERE)
    archive_parts = ["campaign-summaries", "ingestion-packages", "manifests", "normalized", "proposed", "provenance", "raw", "reconciliation", "semantic", "source-records"]
    # Domain totals use the audited Git tree rather than platform-sensitive
    # working-tree sizes. They therefore remain fixed across Windows and Linux.
    domains = []
    for path in ("archive", "knowledge", "graph", "operations", "publication"):
        files, size = tree_stats(path)
        domains.append({"path": path, "files": files, "bytes": size})
    holdings = {
        "baseline_sha": BASELINE_SHA,
        "as_of": AS_OF,
        "domains": domains,
        "archive_areas": [
            {"path": f"archive/{name}", "files": stats[0], "bytes": stats[1]}
            for name in archive_parts
            for stats in [tree_stats(f"archive/{name}")]
        ],
        "normalized_url_inventory": {
            "records": 3232,
            "historical_pending": 902,
            "historical_deferred": 2330,
            "status": "RECONCILED_BY_OVERLAY",
            "path": "archive/normalized/manifests/normalized-urls.jsonl",
            "overlay_path": "operations/coverage/url-disposition-overlay.jsonl",
            "current_dispositions": {"INGESTED_CONFIRMED": 480, "DOCUMENTED_EXCLUSIONS": 263, "RETRIEVAL_FAILED": 4, "UNRECONCILED": 2485},
        },
        "open_pull_requests": 0,
        "remote_topic_branches_merged_into_main": 52,
        "remote_branches_not_ancestors_of_main": ["ingestion/discord-announcements-council-tracker", "ingestion/economic-reports-2022q2-2026q2", "knowledge/wave-2a-foundation-pages", "planning/knowledge-generation-wave-2"],
    }
    coverage = build_coverage()
    backlog = build_backlog()
    campaigns = build_campaigns()
    cleanup = build_cleanup()

    write_json(HERE / "repository-holdings.json", holdings)
    write_json(HERE / "source-coverage-register.json", {"schema_version": "1.0", "as_of": AS_OF, "baseline_sha": BASELINE_SHA, "records": coverage})
    write_json(HERE / "acquisition-backlog.json", {"schema_version": "1.0", "as_of": AS_OF, "items": backlog})
    write_json(HERE / "campaign-status-register.json", {"schema_version": "1.0", "as_of": AS_OF, "campaigns": campaigns})
    write_json(HERE / "cleanup-register.json", {"schema_version": "1.0", "as_of": AS_OF, "immediate_safe_repository_deletions": [], "items": cleanup})
    economic_assessment = build_economic_branch_assessment()
    write_json(HERE / "economic-report-branch-assessment.json", economic_assessment)
    recovery_schedule = build_recovery_schedule()
    write_json(PROGRAM / "recovery-campaign-schedule.json", recovery_schedule)
    write_json(HERE / "refresh-policy.json", {
        "schema_version": "1.0", "as_of": AS_OF, "mode": "READ_ONLY_DISCOVERY_ONLY",
        "classes": {
            "HIGH_FREQUENCY": {"cadence_days": 7, "sources": ["official newsroom", "support", "governance", "Discord", "X"]},
            "MEDIUM_FREQUENCY": {"cadence_days": 30, "sources": ["Medium", "official GitHub documentation", "release notes", "roadmaps", "economic reports", "Town Halls", "Atlas Brew"]},
            "LOW_FREQUENCY": {"cadence_days": 90, "sources": ["historical community publications", "archived sites", "lore snapshots", "completed events"]},
        },
        "rules": ["A check may create or refresh a queue item only.", "No automatic ingestion, evidence mutation, knowledge promotion, or merge.", "Adapter failure is CHECK_FAILED, never no new material."],
        "implementation_status": "MANUAL_BOUNDED_CHECK_EXECUTED_AUTOMATED_ADAPTERS_NOT_IMPLEMENTED",
    })

    holdings_md = ["# Repository Holdings Baseline", "", f"Snapshot: `{BASELINE_SHA}` on {AS_OF}.", "", "## Product domains", ""]
    holdings_md += markdown_table(["Path", "Files", "Bytes"], [[x["path"], x["files"], x["bytes"]] for x in holdings["domains"]])
    holdings_md += ["", "## Archive areas", ""] + markdown_table(["Path", "Files", "Bytes"], [[x["path"], x["files"], x["bytes"]] for x in holdings["archive_areas"]])
    holdings_md += ["", "## Structural findings", "", "- The immutable 3,232-row URL inventory has a separate deterministic disposition overlay; 2,485 URLs remain explicitly unresolved.", f"- {len(campaigns)} campaigns are represented in the central campaign status register.", "- Source Record formats differ by repository generation: Markdown-only, JSON-only, and paired JSON/Markdown all exist.", "- The selected written raw-recovery scope is closed at 541/541 records, with five additional Herald pilot captures preserved and the remaining Herald family explicitly deferred.", "- The official economic-report corpus is ingested from the operator-provided PDF package; the older discovery branch is superseded and eligible for retirement.", "- The Phase 2 freshness queue contains ten unpreserved candidates for later acquisition.", ""]
    (HERE / "repository-holdings.md").write_text("\n".join(holdings_md), encoding="utf-8")

    coverage_md = ["# Source Coverage Register", "", f"Evidence baseline at `{BASELINE_SHA}` on {AS_OF}. Package completeness never implies complete external history.", "", "## Medium-by-time matrix", ""]
    coverage_md += markdown_table(["Source", "Medium", "Supported interval", "Logical records", "Status", "Priority gaps"], [[r["source_family"], r["medium"], f"{r['first_supported_date'] or 'unknown'} to {r['last_supported_date'] or 'unknown'}", max(r["counts"].values()), ", ".join(r["coverage_statuses"]), ", ".join(r["gap_ids"])] for r in coverage])
    coverage_md += ["", "## Critical interpretation", "", "- The repository contains only one Discord export family, designated as announcements by repository path; no native channel identity was captured.", "- All 181 confirmed Medium articles are ingested and all 216 review candidates have terminal dispositions, but publication discovery is incomplete.", "- Eighteen official economic PDFs are preserved; this does not independently verify publisher-reported measurements.", "- Aephia, HNN, and Official successful Source Records have raw recovery bodies and provenance; recovered live bytes remain later recaptures rather than publication-date snapshots.", "- Intergalactic Herald has five preserved pilot captures and is otherwise deferred by operator direction.", "- Transcript-package completeness is distinct from complete program or episode coverage.", "- Council-reported governance state is not independent implementation or payment evidence.", "- Ten official freshness candidates are queued but are not yet archive evidence.", ""]
    (HERE / "source-coverage-register.md").write_text("\n".join(coverage_md), encoding="utf-8")

    backlog_md = ["# Prioritized Acquisition and Research Backlog", "", "No item authorizes collection by itself.", ""] + markdown_table(["Priority", "Gap", "Need", "Owner", "Status"], [[r["priority"], r["gap_id"], r["required_artifact_or_action"], r["owner"], r["status"]] for r in backlog]) + [""]
    (HERE / "acquisition-backlog.md").write_text("\n".join(backlog_md), encoding="utf-8")

    campaign_md = ["# Campaign Status Register", "", "Recorded campaign states are normalized here without rewriting historical campaign reports.", ""] + markdown_table(["Campaign", "Current assessment", "Evidence", "Note"], [[r["campaign_id"], r["status"], f"`{r['status_evidence']}`", r["note"]] for r in campaigns]) + [""]
    (HERE / "campaign-status-register.md").write_text("\n".join(campaign_md), encoding="utf-8")

    cleanup_md = ["# Repository Cleanup Register", "", "No tracked repository file is approved for unconditional deletion in this baseline. Preserved evidence, provenance, manifests, failures, and adjudications remain protected.", ""] + markdown_table(["ID", "Class", "Paths", "Finding", "Recommended action"], [[r["cleanup_id"], r["classification"], "; ".join(r["paths"]), r["finding"], r["action"]] for r in cleanup]) + [""]
    (HERE / "cleanup-register.md").write_text("\n".join(cleanup_md), encoding="utf-8")

    economic_md = [
        "# Economic-report Branch Assessment", "",
        f"Decision: **`{economic_assessment['decision']}`**", "",
        "Do not merge or cherry-pick `origin/ingestion/economic-reports-2022q2-2026q2`. PR #57 superseded it with a conforming ingestion of the operator-provided official PDFs.", "",
        "## Deficiencies", "",
    ] + [f"- {item}" for item in economic_assessment["deficiencies"]] + [
        "", "## Closeout disposition", "",
    ] + [f"- {item}" for item in economic_assessment["phase_2_requirements"]] + [
        "", f"Branch retirement condition: {economic_assessment['branch_retirement_condition']}", "",
        "No human adjudication is required for this classification.", "",
    ]
    (HERE / "economic-report-branch-assessment.md").write_text("\n".join(economic_md), encoding="utf-8")

    recovery_md = [
        "# Phase 2 Legacy Written Raw-capture Schedule", "",
        "Status: **`SELECTED_SCOPE_COMPLETE`**. The written-recovery milestone is closed for the operator-selected scope.", "",
        "The immutable inventory contains 800 successful Alpha–Delta Source Records. Recovery completed for all 541 selected Aephia, HNN, and Official records. Five Intergalactic Herald pilot captures are preserved; the remaining 254 Herald records are explicitly deferred by the operator and are not counted as recovered.", "",
        "## Batches", "",
    ] + markdown_table(["Batch", "Source family", "Frozen records", "Captured", "Disposition"], [[row["batch_id"], row["source_family"], row["records"], row["captured_records"], row["status"]] for row in recovery_schedule["batches"]]) + [
        "", "The preliminary pilot captures remain preserved. Subsequent recovery completed the selected Aephia, HNN, and Official families; Herald recovery stopped after its five-record pilot under the operator's deferral.", "",
        "## Stop rules", "",
    ] + [f"- {item}" for item in recovery_schedule["stop_rules"]] + [
        "", "## Human approval points", "",
    ] + [f"- {item}" for item in recovery_schedule["human_approval_points"]] + [
        "", "Unambiguous recovery from public live or public archive sources needs no item-by-item approval when provenance is retained.", "",
    ]
    (PROGRAM / "recovery-campaign-schedule.md").write_text("\n".join(recovery_md), encoding="utf-8")

    phases = [
        {"phase": 1, "name": "Repository and evidence baseline", "status": "COMPLETE", "percent_complete": 100, "remaining_gate_items": []},
        {"phase": 2, "name": "Priority ingestion", "status": "COMPLETE", "percent_complete": 100, "remaining_gate_items": []},
        {"phase": 3, "name": "Targeted architecture refinement", "status": "READY_TO_START", "percent_complete": 0, "remaining_gate_items": ["Define the publication manifest without rewriting evidence", "Implement only architecture changes justified by validated repository gaps", "Preserve the ten freshness candidates as an acquisition queue until a separately scoped campaign runs"]},
        {"phase": 4, "name": "Knowledge consolidation", "status": "NOT_STARTED", "percent_complete": 0, "remaining_gate_items": ["Complete priority evidence packets", "Select historically valuable dossiers"]},
        {"phase": 5, "name": "Publication layer", "status": "NOT_STARTED", "percent_complete": 0, "remaining_gate_items": ["Stable publication contract", "Initial ten-article portfolio"]},
        {"phase": 6, "name": "Vercel implementation", "status": "NOT_STARTED", "percent_complete": 0, "remaining_gate_items": ["Publication layer approved", "Read-only Vercel connection test"]},
        {"phase": 7, "name": "Preview, validation, and deployment", "status": "NOT_STARTED", "percent_complete": 0, "remaining_gate_items": ["Cross-repository preview", "Launch acceptance"]},
    ]
    program_status = {
        "program_id": "star-atlas-library-roadmap",
        "as_of": AS_OF,
        "baseline_sha": BASELINE_SHA,
        "current_phase": 3,
        "phases": phases,
        "phase_2_progress_basis": "All five Phase 2 workstreams have terminal gate dispositions: Medium ingestion, selected written raw recovery, official economic-report PDF ingestion, official-source freshness discovery, and non-blocking carry-forward of artifact-dependent Discord/transcript gaps.",
        "phase_2_closeout_evidence": [
            "archive/campaign-summaries/star-atlas-medium-ingestion-2026-07/campaign-summary.json",
            "operations/campaigns/legacy-written-raw-recovery-2026-07/campaign-summary.json",
            "operations/campaigns/official-economic-reports-pdf-ingestion-2026-07/campaign-summary.json",
            "operations/campaigns/phase-2-official-freshness-closeout-2026-07/campaign-summary.json",
        ],
        "roadmap_deviation_policy": "Advise the operator before work changes phase order, product boundaries, or completion gates.",
        "campaign_closeout_rule": "Every campaign closeout updates this status, coverage, campaign registry, backlog, and human-review queue when affected.",
        "baseline_ci": {
            "repository_integrity": "PASS",
            "campaign_contracts": "PASS",
            "pages_build": "PASS",
            "pages_deploy": "PASS",
            "verified_at_main_sha": BASELINE_SHA,
            "repairs_in_gate_closeout": [
                "DAO campaign path-scope validation delegated to the central repository path contract so unrelated later PRs cannot rewrite the preserved campaign report",
            ],
        },
    }
    write_json(PROGRAM / "program-status.json", program_status)
    write_json(PROGRAM / "phase-gates.json", {"schema_version": "1.0", "as_of": AS_OF, "phases": phases})
    write_json(PROGRAM / "dependency-register.json", {"schema_version": "1.0", "as_of": AS_OF, "dependencies": [
        {"dependency_id": "DEP-001", "from": "Phase 2", "to": "Phase 1", "status": "SATISFIED", "reason": "Phase 1 is complete and the selected written raw-recovery milestone is closed."},
        {"dependency_id": "DEP-002", "from": "Phase 5", "to": "Phase 3", "status": "PENDING", "reason": "Publication requires stable disposition and manifest contracts."},
        {"dependency_id": "DEP-003", "from": "Phase 6", "to": "Phase 5", "status": "PENDING", "reason": "Vercel is the delivery layer, not the place to resolve editorial scope."},
        {"dependency_id": "DEP-004", "from": "Economic report ingestion", "to": "ingestion/economic-reports-2022q2-2026q2", "status": "SATISFIED_SUPERSEDED_BY_PR57", "reason": "The operator-provided 18-PDF campaign preserves all seventeen quarterly periods through Q2 2026 plus the economics paper; the stale branch is not needed."},
        {"dependency_id": "DEP-005", "from": "Phase 3", "to": "Phase 2", "status": "SATISFIED", "reason": "Phase 2 is complete. Artifact-dependent Discord and transcript gaps remain explicit, non-blocking backlog items."},
    ]})
    program_md = ["# Star Atlas Library Roadmap Status", "", f"Current phase: **Phase 3 — Targeted architecture refinement, ready to start**. Snapshot `{BASELINE_SHA}` on {AS_OF}.", "", "This report must be refreshed at every campaign closeout. Any deviation from phase order, product boundaries, or completion gates must be stated explicitly.", "", "## Phase status", ""] + markdown_table(["Phase", "Status", "Complete", "Remaining gate"], [[f"{p['phase']}. {p['name']}", p["status"], f"{p['percent_complete']}%", "; ".join(p["remaining_gate_items"])] for p in phases]) + ["", "## Phase 2 closeout", "", "Phase 2 is complete. The 181-article Medium corpus, the 541-record selected written-recovery scope, and the 18-document official economic-report package are preserved. A bounded freshness check queued ten unpreserved candidates. Discord and transcript metadata gaps remain explicit but require new operator artifacts and do not block Phase 3.", "", "## Current recommendation", "", "Begin Phase 3 with the publication-manifest contract and only the narrow architecture changes justified by the validated coverage gaps. Do not ingest the ten freshness candidates or rewrite evidence under the architecture campaign.", ""]
    (PROGRAM / "program-status.md").write_text("\n".join(program_md), encoding="utf-8")
    (PROGRAM / "human-adjudication-queue.md").write_text("""# Human Adjudication Queue

## Blocking decisions

None. Phase 2 is closed and Phase 3 is ready to start.

## Closed decisions

- `REVIEW-PHASE2-RAW-RECOVERY`: `CLOSED_SELECTED_SCOPE_COMPLETE`. Aephia, HNN, and Official are complete at 541/541 selected records. Five Herald pilot captures are preserved; the remaining 254 Herald records are deferred by the operator.
- `REVIEW-PHASE2-ECONOMIC-REPORTS`: `CLOSED_INGESTION_COMPLETE`. Eighteen operator-provided PDFs are preserved; the mislabeled Q4 2026 upload is excluded.
- `REVIEW-PHASE2-FRESHNESS`: `CLOSED_QUEUE_CREATED`. Seven official surfaces were checked and ten unmatched candidates were queued without ingestion.

## Deferred, non-blocking decisions

- `REVIEW-6E92B789AF1CEAB2`: observed Discord handle `Michael` remains unmerged with Michael Wagner, per operator decision `DEFERRED`.
- `REVIEW-A2599BBFBEA526F5`: display tag `EMP` remains unresolved, per operator decision `DEFERRED`.

## Decisions to surface before destructive cleanup

- Whether to delete the 44 remote topic branches already merged into `main`.
- Whether to retire `operations/migrations/validate_wave_1_5.py` or preserve it in a clearly historical location.
- Whether source-like campaign captures should move from `operations/` into `archive/raw/`; any move requires manifest and checksum migration.

These decisions do not block Phase 3. No deletion or relocation is performed by this closeout.
""", encoding="utf-8")
    (PROGRAM / "README.md").write_text("""# Star Atlas Library Roadmap

This directory is the operational source of truth for the seven-phase Archive → Knowledge → Library roadmap. GitHub remains authoritative for the underlying evidence and campaign work.

At every campaign closeout, the Lead Coordinator updates the program status and any affected coverage, campaign, dependency, backlog, and human-adjudication records. A campaign that does not affect a field records `NO_CHANGE`; it must not silently leave the roadmap stale.

Phase 2 is closed. Phase 3 begins with a publication-manifest contract and
targeted architecture changes; freshness candidates and artifact-dependent
source gaps remain separate acquisition inputs.

The detailed evidence baseline is maintained in [`../../coverage/`](../../coverage/).
""", encoding="utf-8")


if __name__ == "__main__":
    main()
