# Discord Community Indexing 001

This campaign is a deterministic, evidence-linked **rolling discovery system** for Discord community records already preserved in the repository. It inventories supported Discord raw and normalized files, reconciles repeated representations of the same message, and emits review-oriented identity, organization, relationship, competition, coverage, and research artifacts.

It is not a canonical people registry, a guild registry, a completed Discord corpus, or an automatic knowledge-promotion system. It does not write to `archive/`, `knowledge/`, `graph/`, or `publication/`.

## Current coverage and its limits

The present corpus contains one independently supplied conversation export represented three ways: one raw Markdown aggregate, one normalized JSONL aggregate, and 1,071 normalized per-message JSON records. The derived CSV index is inventoried but is not parsed as another message export. The three evidence representations reconcile to 1,071 unique Source IDs and 3,213 parsed occurrences.

The imported messages run from `2021-03-16T14:34:21` through `2026-07-12T15:18:19`. Every month within those bounds has at least one preserved message, but this is not evidence that every message or channel was collected. The acquisition metadata states that collection was incomplete and that a 180-minute historical runtime limit prevented reaching the requested start. Native server, channel, message, and author IDs are absent. The raw export header is preserved as the observed channel label—`Compromised Discord Account of EX Team Member,`—without treating that label as a verified canonical Discord channel.

The coverage ledger therefore reports:

- one independent export unit;
- one repository-designated Star Atlas community;
- zero native Discord servers identified;
- zero native Discord channels identified;
- one unresolved channel export;
- partial historical coverage through the last captured message.

Mentioned but not imported channels and channel families remain in `discord-collection-backlog.json`, including `Foundation Room`, `Foundation Room Chat`, the operator-observed spelling `Foudnation Room`, `Atlas Amphitheater`, `Atlas Brew Lounge`, `dao-announcements`, and guild, faction, economics, governance, general, and support channels.

## Message identity and deduplication

The index uses the strongest available identity in this order:

1. a native Discord message ID, when supplied;
2. the stable archive Source ID;
3. an exact normalized message fingerprint;
4. content-compatible raw and normalized representations.

Author plus timestamp is never a deduplication key. Two different messages by the same author at the same timestamp are retained. Content-compatible reconciliation is limited to raw-versus-normalized representations with the same author and timestamp, and requires equal text or substantive containment after removing only export framing such as a terminal Markdown delimiter. Every reconciled message retains all source paths and content-variant checksums. Incompatible records sharing a Source ID or native message ID are preserved separately and sent to the human resolution queue.

## Evidence and attribution model

Every archive-derived claim carries its Source ID, timestamp, available native identifiers, display name, source paths, exact quoted excerpt, evidence location, and evidence channel. The controlled attribution taxonomy is:

- `observed_authorship`: the display name attached to an exported message;
- `direct_self_identification`: a speaker explicitly states their own role;
- `explicit_third_party_attribution`: message text explicitly names another person or role;
- `repeated_independent_attribution`: corroborating independent attributions, when present;
- `display_name_guild_tag`: a tag or pipe component observed in a public handle;
- `operator_confirmed_alias`: an operator adjudication, not archive evidence;
- `inferred_alias`: a weak exporter or formatting inference retained visibly;
- `unresolved_similarity`: a fuzzy resemblance that does not authorize a merge.

`observed_authorship` proves only that an export associates a display label with a message; it does not independently prove a legal identity. Fuzzy similarity never merges identities.

Repository-operator confirmations are kept in a separate `operator_confirmation` evidence channel. Those records use `source_id: null`, `operator_assertion: true`, a review note, and no fabricated archive citation. A null Source ID is not permitted for archive evidence. Confirmed operator aliases include the reviewed identity families for King Bryan, Bodhi, Michael Wagner, and Jose. Unresolved names remain separate seeded records.

## Organizations, display tags, and roles

Organization types are controlled as:

- `guild`;
- `guild_alliance`;
- `community_organization`;
- `official_team`;
- `informal_group`;
- `community_meme`;
- `unresolved_tag`.

The operator-confirmed entities currently include Aephia (`AEP`, `Aephia Industries`) and BULK as guilds; Intergalactic Alliance (`IA`) as a guild alliance; Star Atlas Italia (`SAI`) as a community organization; and `426` as a community meme. BULK is never expanded into an invented long form.

A display tag is association evidence, not membership proof. A leading confirmed guild tag may produce `possible_member_of` for human review. A pipe-separated guild component such as `[IA] Dodger | BULK` produces `associated_with_guild`, not membership. `IA` produces `associated_with_alliance`, `SAI` produces `associated_with_organization`, and `426` produces only `has_display_tag`. Unknown tags remain unresolved and enter the queue.

Role dimensions remain separate. Guild founder, guild leader, guild officer, alliance leader, DAO Council service, official team membership, creator/builder activity, community organizing, and historical significance are not interchangeable. DAO Council service does not increase guild-leadership confidence. Operator-confirmed roles for Funcracker and Eoganacht remain visibly separate from archive-derived role evidence.

Identity rows without a native author ID or confirmed alias are explicitly `observed_handle_cluster` records rather than silently asserted canonical people. Seeded unresolved identities remain `seeded_unresolved_identity` records.

## Competition records

Competition extraction is a dedicated typed pass. A placement record stores event, placement, participant, participant type, timestamp, Source ID, exact evidence, and resolution status. Only confirmed organizations or identities are resolved automatically. Unrecognized participants remain unresolved. Prize tiers, dollar amounts, category labels, and malformed lines are never created as guilds or people; they are retained as review records. Placement relationships are emitted only for resolved participants.

## Human review and promotion boundary

`human-resolution-queue.json` is the durable operator workspace. It includes suspected duplicates, possible aliases, unknown tags, uncertain organization types, possible guild memberships, malformed competition rows, unresolved participants, missing channel identity, historical source gaps, and the required seeded unresolved names. Each item records observed values, candidate resolution, confidence, evidence, why review is required, allowed decisions, a null operator decision, and `OPEN` status.

`promotion-candidates.json` is review-oriented only. It contains explicit score dimensions and controlled review statuses; it never emits a bare `promote` recommendation. Message volume alone has no authority, and machine confidence does not establish factual truth.

## Commands

Run from the repository root:

```powershell
python operations/campaigns/discord-community-indexing-001/build_index.py build
python operations/campaigns/discord-community-indexing-001/validate_campaign.py --base-ref origin/main
python operations/campaigns/discord-community-indexing-001/build_index.py search "AEP"
python operations/campaigns/discord-community-indexing-001/build_index.py search "Funcracker" --threshold 0.70
```

The build uses only the Python standard library. Validation also runs the repository test suite through `pytest`.

### Rolling update procedure

1. Preserve a new raw Discord export under the repository’s existing archive-ingestion process; do not edit prior evidence.
2. Normalize and register the messages using the source-ingestion campaign responsible for archive evidence.
3. Run this campaign’s build command. The index discovers eligible Discord evidence under `archive/raw/` and `archive/normalized/` and regenerates deterministic outputs.
4. Review new duplicate candidates, coverage changes, unresolved tags, identities, organizations, and competition rows.
5. Record operator decisions through the campaign’s explicit resolution data model; do not disguise them as archive evidence.
6. Run campaign validation and repository CI. Commit generated artifacts only when the fixed-point and source reconciliation checks pass.

## Outputs

- `source-inventory.json`: file-level provenance, checksums, representation roles, parse counts, date bounds, and the distinction between source files, parsed occurrences, and independent exports.
- `alias-registry.json`: confirmed aliases, observed handles, operator adjudications, fuzzy conflicts, and merge authorization.
- `identity-index.jsonl`: resolved identities, observed author identities, observed handle clusters, seeded unresolved identities, roles, dates, and evidence.
- `guild-index.jsonl`: the guild-only compatibility view.
- `organization-index.jsonl`: all controlled organization and community entity types.
- `relationship-index.jsonl`: dated, typed archive relationships plus separately marked operator-confirmed relationships.
- `competition-index.jsonl`: typed competition placements, unresolved participants, and malformed prize/category records.
- `tag-registry.json`: confirmed and unresolved display-tag meanings and resolution bases.
- `promotion-candidates.json`: review status and independent score dimensions without automatic promotion.
- `conflict-report.json`: identity non-merge conflicts, duplicate-review candidates, and missing native identifiers.
- `human-resolution-queue.json`: structured unresolved decisions with allowed operator actions.
- `discord-channel-coverage.json`: export-scoped server/community/channel coverage and timestamp bounds.
- `discord-channel-gap-report.json`: known temporal and identity gaps without false completeness claims.
- `discord-collection-backlog.json`: prioritized acquisition targets and required artifacts.
- `research-backlog.json`: broader identity, role, and organization research needs.
- `validation-report.json`: internal evidence checks plus JSON/JSONL, contracts, uniqueness, deterministic generation, repository tests, forbidden paths, and whitespace checks.

## Validation contract

Validation confirms controlled evidence and organization taxonomies, unique record IDs, resolvable Source IDs, retained exact quotations, dated archive relationships, distinct operator evidence, safe tag semantics, typed competition participants, source-record reconciliation, derived coverage bounds, deterministic regeneration, generated-artifact reconciliation, repository tests, campaign path boundaries, and `git diff --check`.

No archive evidence, canonical knowledge, graph fact, or publication output is rewritten by this campaign.
