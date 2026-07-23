---
title: "Star Atlas Economic Report Catalog"
seo_title: "Star Atlas Economic Reports: Complete Quarterly Catalog"
seo_description: "A date-by-date catalog of official Star Atlas economic reports from 2022 Q2 through 2026 Q2, with methodology cautions, archive status, and research gaps."
knowledge_status: QUALIFIED
as_of: 2026-07-23
confidence: HIGH
page_risk_score: 6
page_risk_class: R2
evidence_basis:
  - "archive/campaign-summaries/campaign-delta-official/campaign-summary.json"
  - "archive/normalized/social-governance-semantic-enrichment/social-media/staratlas-posts.jsonl"
  - "archive/manifests/official-economic-reports-pdf-ingestion-2026-07.json"
  - "operations/campaigns/official-economic-reports-pdf-ingestion-2026-07/campaign-summary.json"
known_limitations:
  - "The 17 quarterly PDFs and one economics paper are preserved and text-extracted, but no longitudinal semantic metric series has been promoted."
  - "Report dates and archive labels establish publication chronology, not independent accuracy or methodological continuity."
research_gaps:
  - "Build a versioned metric dictionary and identify every material methodology change across the 17 preserved quarters."
  - "Reconcile appendix references and archive aliases to the preserved PDFs without treating duplicate listings as additional reports."
review_after: 2026-10-20
---

# Star Atlas Economic Report Catalog

**Official archive:** https://govern.staratlas.com/economy/economic-reports
**Legacy archive:** https://experience.staratlas.com/newsroom/economic-reports

The Star Atlas economic-report series is an official recurring research corpus covering the project's economy. Reports are useful primary sources for historical metrics, methodology, policy discussion, and the official interpretation of economic activity. They should not be treated as warranties of accuracy or predictions of future performance.

The series is most valuable when read longitudinally. Individual editions show what Star Atlas institutions or commissioned researchers chose to measure at a particular moment; changes in terminology, method, scope, and data availability can be historically significant in their own right. The catalog therefore preserves publication order before attempting to combine any figures.

## How to use this catalog

Readers should distinguish three levels of evidence:

- **Catalog evidence** establishes that an official archive listed a report for a period and date.
- **Document evidence** begins once the exact PDF or appendix is preserved, hashed, and reviewed.
- **Metric evidence** requires the table, definition, methodology, time window, units, and revision history needed to interpret a number responsibly.

The repository now establishes the first two levels across the listed series.
The operator-provided ingestion package preserves **17 quarterly report PDFs**
from 2022 Q2 through 2026 Q2 plus one 2021 economics paper. All 18 documents
have immutable PDF captures, checksums, text extractions, normalized records,
Source Records, and ingestion packages. The remaining work is metric-level
interpretation and longitudinal reconciliation, not document acquisition.

## Report series

| Period | Official publication date | Notes |
|---|---:|---|
| 2022 Q2 | 2022-06-30 | Earliest report currently linked in the official archive |
| 2022 Q3 | 2022-09-30 | Separate appendix also indexed |
| 2022 Q4 | 2023-01-03 | Separate appendix dated 2022-12-31 |
| 2023 Q1 | 2023-03-31 | Quarterly report |
| 2023 Q2 | 2023-06-30 | Quarterly report |
| 2023 Q3 | 2023-09-29 | Quarterly report |
| 2023 Q4 | 2023-12-22 | Quarterly report |
| 2024 Q1 | 2024-03-29 | Quarterly report |
| 2024 Q2 | 2024-07-01 | Quarterly report |
| 2024 Q3 | 2024-10-01 | Quarterly report |
| 2024 Q4 | 2024-12-20 | Quarterly report |
| 2025 Q1 | 2025-03-31 | Quarterly report |
| 2025 Q2 | 2025-06-30 | One operator-provided quarterly PDF is preserved; multiple archive labels must not be counted as additional documents without distinct checksums |
| 2025 Q3 | 2025-10-03 | Quarterly report |
| 2025 Q4 | 2025-12-19 | Quarterly report |
| 2026 Q1 | 2026-04-01 | Quarterly report |
| 2026 Q2 | 2026-07-01 | Most recent report visible during the 2026-07-12 sweep |

## Official disclaimer summary

The archive states that the papers are academic publications intended to inform public discussion. The DAO or Foundation may request or commission them, and authors may include ATMTA researchers, employees, consultants, or service providers. ATMTA disclaims warranties concerning accuracy and identifies non-historical statements as forward-looking and uncertain.

That disclaimer does not make the reports low-value. It defines their proper authority: they are strong primary evidence for the publisher's measurements, methods, and institutional interpretation at publication time, while independent economic accuracy and later outcomes remain separate questions.

## Current infrastructure status

The DAO economic-report page states that community dashboards are offline while the project moves to an internal data solution powered by Star Atlas infrastructure. This status is time-sensitive and was observed on 2026-07-12.

## Preserved document corpus

The PDF campaign accepted 18 valid, unique documents: 17 quarterly reports and
one economics paper. Together they contain 294 pages and 390,574 extracted text
characters. Representative page rendering passed visual review. The campaign
did not fetch article URLs for body text because the operator-provided PDFs are
the preserved document bodies; URLs remain identifiers and cross-references.

The accidentally uploaded file labeled `q4-2026.pdf` was excluded by operator
adjudication. No Q4 2026 Source Record exists, and the catalog does not imply
that a report for that future period was published.

Text extraction makes the reports searchable, but it does not by itself
normalize tables, reconcile definitions, or verify the publisher’s economic
measurements. A metric can enter a longitudinal series only after its source
page, units, observation window, methodology, and revision state are recorded.

## Policy chronology anchor: R4 liberalization

An official announcement dated 2023-06-08 described a planned transition toward player-driven R4 supply: Escape Velocity loot was to rise to nearly eight times its baseline and unlimited DAO R4 sales were to end after a finite 30-day supply. Atlas Brew discussed the same transition as an economy change affecting Claim Stakes and Escape Velocity. These sources establish an announced policy and contemporaneous community discussion; they do not, without later measurement or transaction evidence, establish the exact execution date or economic effect. [SRC-OFF-D023F6DAFA12F9AA](../../archive/source-records/campaign-delta-official/SRC-OFF-D023F6DAFA12F9AA.md) [SRC-ATLAS-BREW-0026, 00:11:21–00:13:08; SEG-ATLAS-BREW-0026-0009](../../archive/semantic/atlas-brew/segment-index.json)

## Metric-consolidation requirements

For each preserved report:

- confirm title, authors, publication date, page count, and methodology against the PDF;
- extract headline metrics and definitions without detaching them from their time period or page;
- identify revisions to methodology across quarters;
- distinguish nominal dollar values, token amounts, on-chain volume, GDP estimates, player counts, emissions, sinks, and treasury data;
- retain corrections, appendices, and duplicated archive entries;
- link referenced community reporting when an official paper cites it;
- record whether figures are measured, modeled, estimated, or forward-looking.

## Open work

- Compare table definitions and methodology between quarters.
- Build a metric dictionary so similarly named figures are not falsely treated as continuous series.
- Extract the economic-policy chronology, including resource liberalization, emissions, sinks, marketplace behavior, and SAGE-related activity.
- Reconcile the multiple 2025 Q2 archive labels to the single preserved quarterly PDF and any genuinely distinct appendix.
- Record corrections, replacements, and silent PDF revisions through checksum comparison.
- Link each preserved metric to the report page, table, units, and applicable observation period.

## Related pages

- [ATLAS Token History](ATLAS-Token-History.md)
- [POLIS Token History](POLIS-Token-History.md)
- [Treasury Authorization and Reported Payment Ledger](Treasury-Authorization-and-Payment-Ledger.md)
- [Governance and Economy Overview](../governance/Governance-and-Economy-Overview.md)

## Review status

This R2 catalog is ready for publication as a qualified inventory of the 18
preserved documents. It does not claim that every economic report has been
discovered, that the measurements are independently accurate, or that similarly
named metrics form a continuous series until their definitions and observation
periods are reconciled.
