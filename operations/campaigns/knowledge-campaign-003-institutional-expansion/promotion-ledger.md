# Knowledge Promotion Campaign 003 — Promotion Ledger

**Campaign ID:** `knowledge-promotion-campaign-003-institutional-expansion`

**Issue:** #9

**Review date:** 2026-07-14

**Input:** `archive/semantic/atlas-brew/promotion-candidates.json`

## Disposition summary

| Disposition | Candidates | Meaning |
|---|---:|---|
| Accepted | 10 | Promoted with source IDs, Atlas Brew timestamps, and explicit evidence-state boundaries. |
| Deferred | 3,289 | Seven individually reviewed candidates need stronger evidence; 3,282 candidates remain outside the individually adjudicated priority clusters. |
| Duplicate | 4 | Substantively covered by stronger accepted evidence. |
| Rejected | 3 | Speculative, opinion-based, or unsafe automated lifecycle interpretation. |
| **Total** | **3,306** | Reconciles to the semantic promotion-candidate input. |

The JSON ledger is authoritative for candidate-level decisions. Its batch rule deterministically assigns every input candidate not among the 24 individually reviewed entries to `DEFERRED`; no unreviewed candidate is silently promoted.

## Accepted candidates

| Candidate | Source and timestamp | Promoted finding | Destination |
|---|---|---|---|
| `PROMOTION-CANDIDATE-00989` | `SRC-ATLAS-BREW-0034` `00:02:33-00:04:33` | SAGE Labs release framing, without speaker attribution | Product Registry; Actor Master Index |
| `PROMOTION-CANDIDATE-01896` | `SRC-ATLAS-BREW-0069` `01:32:25-01:35:24` | Fleet Command development discussion, not release | Product Registry |
| `PROMOTION-CANDIDATE-02678` | `SRC-ATLAS-BREW-0101` `00:09:55-00:10:58` | Holosim availability, without a calendar launch date | Product Registry |
| `PROMOTION-CANDIDATE-02676` | `SRC-ATLAS-BREW-0101` `00:02:35-00:06:35` | C4 design and roadmap discussion | Product Registry; Technical Platform |
| `PROMOTION-CANDIDATE-02695` | `SRC-ATLAS-BREW-0101` `00:38:07-00:39:04` | Intended C4 mining behavior, not implementation | Product Registry; Technical Platform |
| `PROMOTION-CANDIDATE-00754` | `SRC-ATLAS-BREW-0026` `00:11:21-00:13:08` | Announced R4 transition and community discussion, not measured effect | Economic Report Catalog |
| `PROMOTION-CANDIDATE-00684` | `SRC-ATLAS-BREW-0024` `00:13:14-00:15:09` | PIP-1 proposal-stage discussion | Governance Overview; PIP Registry |
| `PROMOTION-CANDIDATE-02521` | `SRC-ATLAS-BREW-0094` `00:09:46-00:11:25` | PIP-14 proposal discussion, with numbering and outcome unresolved | PIP Registry |
| `PROMOTION-CANDIDATE-02843` | `SRC-ATLAS-BREW-0106` `00:48:36-00:50:52` | Conditional PIP-19 roadmap discussion | PIP Registry |
| `PROMOTION-CANDIDATE-01662` | `SRC-ATLAS-BREW-0060` `00:17:53-00:19:02` | Foundation-role discussion as community context, not authority proof | Governance Overview; Institutional Overview |

## Individually deferred

- `PROMOTION-CANDIDATE-02037`: PIP-2 allocation or transfer requires transaction evidence.
- `PROMOTION-CANDIDATE-01138` and `PROMOTION-CANDIDATE-01139`: MetaGravity and stress-test claims require dated first-party technical evidence.
- `PROMOTION-CANDIDATE-00877`: Starbased migration detail requires an official migration or build record.
- `PROMOTION-CANDIDATE-02157`: Fleet Command build access conflicts with current in-development documentation.
- `PROMOTION-CANDIDATE-03161`: Holosim-to-C4 architecture claim lacks speaker attribution and technical documentation.
- `PROMOTION-CANDIDATE-02549`: PIP-13 outcome requires the official proposal and vote record.

## Duplicates and rejections

- Duplicates: `PROMOTION-CANDIDATE-00493`, `PROMOTION-CANDIDATE-00507`, `PROMOTION-CANDIDATE-00761`, and `PROMOTION-CANDIDATE-02807`.
- Rejected: `PROMOTION-CANDIDATE-00879`, `PROMOTION-CANDIDATE-02216`, and `PROMOTION-CANDIDATE-03155`.

## Preserved gaps

- No speaker-level attribution exists in the normalized Atlas Brew semantic layer.
- No Atlas Brew semantic candidate references PIP-33.
- PIP approval and implementation evidence remains incomplete for several reviewed proposals.
- A PTR or menu-accessible build does not establish general product release.
- Current official documentation does not establish historical availability by itself.
