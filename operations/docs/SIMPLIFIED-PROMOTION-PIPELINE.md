# Simplified Promotion Pipeline

## Purpose

The repository uses one visible four-stage workflow for evidence-backed knowledge work:

```text
PRESERVE -> DRAFT -> REVIEW -> PUBLISH
```

The workflow simplifies campaign operations without weakening evidence preservation. Detailed extraction, reconciliation, attribution, taxonomy, conflict detection, and research-gap checks support these stages; they are not independent approval gates unless risk requires them.

The Archive preserves the record. The Knowledge layer maintains the best reviewed, date-scoped synthesis of that record. The Library communicates that synthesis and exposes its evidence boundaries.

## Stages

### PRESERVE

Capture raw material, provenance, checksums, deterministic normalization, deduplication, and Source Records as one archival operation. Archive evidence is never automatically canonical.

### DRAFT

Create source-linked knowledge candidates. Every material claim must identify its claim type, temporal scope, supporting Source IDs or repository paths, and known limitations. Semantic output may assist discovery but cannot independently support promotion.

### REVIEW

Assign one risk class and review mode. A consolidated campaign report doubles as the promotion ledger and human-review queue. Separate evidence packets, conflict reports, or taxonomy migrations are required only when a candidate's risk or ambiguity needs them.

### PUBLISH

Place approved knowledge on a draft pull-request branch. Normal branch protection or a maintainer controls merge to `main`. Merged knowledge may trigger the Library build. Graph updates are optional, independently reviewed outputs and never block narrative publication.

## Risk and review modes

| Risk | Default mode | Treatment |
| --- | --- | --- |
| `R1` | `AUTOMATED` | May be promoted onto a draft PR only when every automatic-eligibility check passes. |
| `R2` | `BATCH` | Reviewed as a group at PR closeout; exceptions are surfaced individually. |
| `R3` | `INDIVIDUAL` | Requires an explicit human decision. |
| `R4` | `INDIVIDUAL` | Requires explicit authorization before approval. |
| `R5` | `ARCHIVE_ONLY` | Preserved for research and excluded from canonical knowledge. |

R1 automation is limited to direct, unambiguous evidence using established entities and taxonomy. It is prohibited for conflicts, identity resolution, financial, legal, treasury, reputational, governance-execution, sensitive, or inferred lifecycle claims. Current-state claims require an `as_of` date.

Automated approval means that an agent may write validated R1 knowledge to a draft campaign branch. It never authorizes direct publication, automatic merge, branch-protection bypass, or mutation of preserved evidence.

## Dispositions

Candidates use one of:

- `PENDING_REVIEW`
- `AUTO_APPROVED`
- `APPROVED`
- `REVISE`
- `DEFERRED`
- `REJECTED`
- `ARCHIVE_ONLY`

Unresolved R3 and R4 candidates must appear in `human_review_queue`. Each decision presents evidence, a recommendation, consequences, allowed options, and an explicit defer option. Decisions are surfaced as they arise and summarized again at PR closeout.

## Required campaign artifact

New campaigns adopting this workflow produce one `campaign-report.json` conforming to `operations/schema/PROMOTION-CAMPAIGN-v1.schema.json` and one concise human-readable companion based on `operations/templates/simplified-campaign-report.md`.

The report contains:

- campaign identity and current stage;
- preserved evidence summary;
- proposed knowledge candidates and material claims;
- risk class, review mode, eligibility checks, and disposition;
- human adjudications and unresolved decisions;
- research gaps and validation results;
- merge authority fixed to `HUMAN_OR_BRANCH_PROTECTION`.

Campaign-specific artifacts remain permissible when justified by elevated risk. They are not required by default.

## Operational ownership

The enforceable role boundaries are maintained in the [Repository Agent Contracts](../agents/README.md).

- **Archive Steward:** coordinates ingestion, preservation, provenance, normalization, and archive validation.
- **Knowledge Curator:** drafts evidence-qualified knowledge and invokes attribution and taxonomy validators.
- **Review Gate:** assigns risk, enforces automation boundaries, and routes human adjudication.
- **Library Publisher:** reads merged knowledge and reviewed provenance metadata; it cannot edit evidence.
- **Research Analyst:** maintains prioritized gaps asynchronously and does not block routine R1 work.

No role may approve its own R3 or R4 interpretation, rewrite archive evidence, or merge automatically.

Knowledge Curators must produce human-first, comprehensive, narratively coherent, search-friendly prose rather than semantic-record dumps. Machine taxonomy belongs in front matter or one consolidated reference section and is hidden from the public article body by default. The Review Gate evaluates narrative quality and taxonomy hygiene separately from citation validity; the Library Publisher cannot repair weak knowledge by silently rewriting it.

## Compatibility

The contract is opt-in and additive. Existing campaign reports and Repository Schema v2.1 artifacts remain valid. A campaign declares adoption with `pipeline_version: "1.0"`; CI then enforces this contract.
