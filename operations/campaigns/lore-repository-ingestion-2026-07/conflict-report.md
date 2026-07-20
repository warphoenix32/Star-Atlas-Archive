# Lore Repository Conflict Report

## LRC-001-AUTHORITY-LABEL — Upstream identity and authority labeling

- Severity: `HIGH`
- Manual review: `FALSE`
- Finding: Repository API/default-branch metadata describes a fan-created encyclopedia, while main-branch and deployed-site metadata use an Official Star Atlas Lore Encyclopedia description.
- Disposition: CURATOR ADJUDICATED: Jose is a Star Atlas team member responsible for lore; the personal repository is ATMTA-affiliated canonical lore authority. Page-level authorship remains separately attributed.

## LRC-003-BRANCH-AUTHORITY — Default branch differs from active content branch

- Severity: `MEDIUM`
- Manual review: `FALSE`
- Finding: Default branch master points to d138c60a210e2afc2d898806ecf9b032a4f8c3a1; current content and deployment workflow use main at 22555f277eb1496e34c0839c8f1f382842bd1d2b.
- Disposition: MAIN_COMMIT_SELECTED_AND_ALL_BRANCH_IDENTITIES_PRESERVED.

## LRC-004-DEPLOYMENT-STALE — Live deployment does not match current main

- Severity: `MEDIUM`
- Manual review: `FALSE`
- Finding: The live gh-pages deployment declares source e1d87b0, preceding captured main 22555f277eb1496e34c0839c8f1f382842bd1d2b.
- Disposition: SOURCE_COMMIT_AND_LIVE_SITE_PROVENANCE_REMAIN_DISTINCT.

## LRC-005-MIRROR-DIVERGENCE — Canon authoring pages versus docs publication mirrors

- Severity: `HIGH`
- Manual review: `FALSE`
- Finding: 86 same-path Markdown mirrors differ after UTF-8/LF normalization; 1 canon pages have no same-path docs mirror; 0 non-index docs pages have no same-path canon source.
- Disposition: CURATOR_ADJUDICATED: CANON CONTROLS TAXONOMY; BOTH TEXT VARIANTS REMAIN PRESERVED.

## LRC-006-UPSTREAM-LINKS — Unresolved upstream relative links

- Severity: `MEDIUM`
- Manual review: `FALSE`
- Finding: 252 relative Markdown links do not resolve to a member of the pinned snapshot.
- Disposition: CURATOR_ADJUDICATED: SOURCE PRESERVED; REPAIR DEFERRED TO A SEPARATE LINK-REPAIR CAMPAIGN.

## LRC-007-NAVIGATION — MkDocs navigation resolution

- Severity: `MEDIUM`
- Manual review: `FALSE`
- Finding: 0 configured navigation targets are absent from the pinned docs tree; sitemap has 0 missing expected and 1 extra URLs.
- Disposition: CURATOR_ADJUDICATED: LIVE SITEMAP AND SOURCE NAVIGATION PRESERVED SEPARATELY; ONI/CSS PAGE CLASSIFIED AS A HISTORICAL CANONICAL-SOURCE SNAPSHOT.

## LRC-008-UPSTREAM-VERIFICATION — Upstream self-reported chronology and consistency findings

- Severity: `HIGH`
- Manual review: `FALSE`
- Finding: The upstream verification artifact reports 12 chronology errors, 20 possible contradictions, and 7 orphaned years.
- Disposition: PRESERVED_AS_UPSTREAM SELF-ASSESSMENT; NO CLAIM CORRECTIONS APPLIED.

## LRC-009-LOCAL-PATHS — Embedded workstation paths

- Severity: `LOW`
- Manual review: `FALSE`
- Finding: 2 canon lines contain absolute Windows user paths.
- Disposition: CURATOR_ADJUDICATED: PRESERVED IN IMMUTABLE RAW EVIDENCE; REDACTED FROM NORMALIZED RECORDS AND PUBLIC-FACING DERIVATIVES.
