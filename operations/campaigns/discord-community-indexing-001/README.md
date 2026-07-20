# Discord Community Indexing 001

This campaign is a deterministic, evidence-linked **rolling discovery system** for Discord community records already preserved in the repository. It inventories supported Discord raw and normalized files, reconciles repeated representations of the same message, and emits review-oriented identity, organization, relationship, competition, coverage, and research artifacts.

It is not a canonical people registry, a guild registry, a completed Discord corpus, or an automatic knowledge-promotion system. It does not write to `archive/`, `knowledge/`, `graph/`, or `publication/`.

## Conversation significance boundary

Message preservation and knowledge significance are separate decisions. Future conversational exports are reviewed as contextual windows with exact Source IDs, timestamps, participants, reply or chronological linkage, topic continuity, recurrence, and counterevidence. Message volume, keyword density, or sentiment alone cannot establish historical importance or animosity.

Unrelated real-world politics, culture-war discussion, unrelated games, off-topic personal commentary, and personal attacks unrelated to Star Atlas conduct or history remain archive-only. Star Atlas-related interpersonal material may be evaluated only when it materially concerns guild conduct, governance, competition, transactions, leadership, moderation, alliances, institutional decisions, or documented in-game or community actions. Ambiguous boundaries use `OUT_OF_SCOPE_OR_AMBIGUOUS`. Reputationally adverse interpretations about identifiable people or organizations are at least R3 and require individual human adjudication.

The current 1,071-message corpus cannot safely support conversation clustering: native channel and message identifiers and trustworthy native channel context are absent. The campaign therefore retains its message-level indexes and emits no interaction finding. This is an evidence limitation, not a claim that no significant conversations exist.

## Current coverage and its limits

The present corpus contains one independently supplied conversation export represented three ways: one raw Markdown aggregate, one normalized JSONL aggregate, and 1,071 normalized per-message JSON records. The derived CSV index is inventoried but is not parsed as another message export. The three evidence representations reconcile to 1,071 unique Source IDs and 3,213 parsed occurrences.

The imported messages run from `2021-03-16T14:34:21` through `2026-07-12T15:18:19`. The repository operator establishes March 2021 as the canonical beginning of the Star Atlas Discord and confirms that no Discord history predates that formation. Every month within the captured bounds has at least one preserved message, but this is not evidence that every message within the period or every channel was collected. Native server, channel, message, and author IDs are absent. The observed export title—`Compromised Discord Account of EX Team Member,`—is preserved as a collection-tool artifact: because the collector was not configured for an announcement channel, it used the first collected message as the file title. It is not treated as a native channel name.

The coverage ledger therefore reports:

- one independent export unit;
- one repository-designated Star Atlas community;
- zero native Discord servers identified;
- zero native Discord channels identified;
- one partially captured export whose native channel identity remains unavailable;
- a canonical community beginning of March 2021, with partial collection coverage within the period through the last captured message.

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

Repository-operator confirmations are kept in a separate `operator_confirmation` evidence channel. Those records use `source_id: null`, `operator_assertion: true`, a review note, and no fabricated archive citation. A null Source ID is not permitted for archive evidence. `curator-decisions.json` preserves all 41 adjudications through 2026-07-19, including confirmations, deferrals, ignored candidates, the approved Funcracker promotion, and the non-person software classification. Unresolved names remain separate records.

The operator resolves `Chri.z` to **Chris Kaczmarczyk-Smith**, Head of Star Atlas Game Economy. Statements actually attributed to him within that subject-matter scope are classified as authoritative first-party institutional evidence. This authority classification does not erase the statement's date or wording and does not convert plans, estimates, testing, approvals, or announcements into release or execution evidence.

Deleted-user identities and tags are excluded from the public identity and promotion views. Their source messages remain available only as contextual evidence for other public community subjects. Public handles and community roles are retained; private personal information is not added.

## Organizations, display tags, and roles

Organization types are controlled as:

- `guild`;
- `guild_alliance`;
- `community_organization`;
- `official_team`;
- `informal_group`;
- `community_meme`;
- `software_agent`;
- `unresolved_tag`.

The operator-confirmed guilds now include Aephia (`AEP`, `Aephia Industries`), Ágora/Agora, BULK, Dark Matter, Rome, The Club Guild (`The Club`), Coexist (`COEX`), Eclypse (`EC`), Deep Profits (`DEEP`), and The Vanguard. The Vanguard's display tag is `VΛ`: a Latin `V` followed by uppercase Greek lambda. The standalone `Λ` tag usually indicates association with Agora, but does not prove membership by itself. Dark Matter is classified as a guild/DAC aligned with the Ustur faction. Intergalactic Alliance (`IA`) remains a guild alliance; Star Atlas Italia (`SAI`), Polaris Fuel, Star Atlas TV, and Ryden Systems/EveEye are community organizations; `426` is a community meme. The Star Atlas AI App is a software agent and is excluded from person promotion. BULK is never expanded into an invented long form.

The operator supplied Agora's Portuguese guild description and public invite. Its preserved English archival translation describes a collaborative Star Atlas guild centered on mutual growth, continuous learning, organized information, coordinated logistics and strategy, and a welcoming community. The description explicitly identifies **SAWYN** and **Neo_AArmstrong** as guild leaders and supplies `https://discord.gg/69HsqtZ22N`. Those two leadership and membership relationships are operator-confirmed; the general `Λ` tag remains association-only.

A display tag is association evidence, not membership proof. A leading confirmed guild tag may produce `possible_member_of` for human review. A pipe-separated guild component such as `[IA] Dodger | BULK` produces `associated_with_guild`, not membership. `IA` produces `associated_with_alliance`, `SAI` produces `associated_with_organization`, and `426` produces only `has_display_tag`. Unknown tags remain unresolved and enter the queue.

Role dimensions remain separate. Guild founder, guild leader, guild officer, alliance leader, DAO Council service, official team membership, creator/builder activity, community organizing, and historical significance are not interchangeable. DAO Council service does not increase guild-leadership confidence. All operator-confirmed roles remain visibly separate from archive-derived role evidence. The available archive independently supports the 2025 Joni awards, MagicPuncher's gameplay-engineer attribution, Dom's event work, ZeSKK's lore activity, The Club's guild status, and several display-tag associations.

Identity rows without a native author ID or confirmed alias are explicitly `observed_handle_cluster` records rather than silently asserted canonical people. Seeded unresolved identities remain `seeded_unresolved_identity` records.

## Competition records

Competition extraction is a dedicated typed pass. A placement record stores event, placement, participant, participant type, timestamp, Source ID, exact evidence, and resolution status. Only confirmed organizations or identities are resolved automatically. Unrecognized participants remain unresolved. Prize tiers, dollar amounts, and category labels are deterministically classified as non-participants rather than created as guilds or people; genuinely malformed or ambiguous lines remain review records. URL-slug ordinal collisions are excluded. Placement relationships are emitted only for resolved participants.

## Human review and promotion boundary

`human-resolution-queue.json` is the durable workspace for issues that remain open after adjudication. Each item records observed values, candidate resolution, confidence, evidence, why review is required, allowed decisions, a null operator decision, and `OPEN` status. The observed `Michael` handle remains unresolved and is not merged with Michael Wagner. The `EMP` display tag also remains unresolved. Rome chronology dates are explicitly deferred as unknown and low priority, so the supplied undated sequence remains operator context rather than an active blocking review item.

The 2026-07-19 adjudication also resolves `Agent_Solace` to **Agent Solace**, and the legacy spellings `Virtuwaal` and `Virtuwuul` to the preferred **Virtuwul**. Virtuwul is operator-confirmed as a Rome member and Rainbow Phi owner; existing HNN, Aephia, and Discord-derived repository records are retained as corroborating artifacts rather than rewritten. Shaddix is operator-confirmed as a Star Atlas music content creator, former moderator, and Aephia/AEP member.

`promotion-candidates.json` contains explicit score dimensions and controlled review statuses; it never emits a bare machine-generated `promote` recommendation. Funcracker is marked `OPERATOR_APPROVED_FOR_PROMOTION` based on the supplied human decision. Diego_Diaz08 and inti are omitted from promotion review, and the software bot is not eligible. Resolved identity and role metadata for Chris Kaczmarczyk-Smith, Shaddix, Agent Solace, The Vanguard, and Virtuwul remains subject to the repository's normal knowledge-promotion workflow. Message volume alone has no authority, and machine confidence does not establish factual truth.

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
- `curator-decisions.json`: the complete 41-item human adjudication record applied by this revision.
- `conversation-significance-policy.json`: controlled scope, interaction, disposition, and reputational-review rules for conversational evidence.
- `conversation-significance-assessment.json`: corpus-level readiness decision; the current export remains message-index-only because conversation structure cannot be reconstructed reliably.
- `discord-channel-coverage.json`: export-scoped server/community/channel coverage and timestamp bounds.
- `discord-channel-gap-report.json`: known temporal and identity gaps without false completeness claims.
- `discord-collection-backlog.json`: prioritized acquisition targets and required artifacts.
- `research-backlog.json`: broader identity, role, and organization research needs.
- `validation-report.json`: internal evidence checks plus JSON/JSONL, contracts, uniqueness, deterministic generation, repository tests, forbidden paths, and whitespace checks.

## Validation contract

Validation confirms controlled evidence and organization taxonomies, unique record IDs, resolvable Source IDs, retained exact quotations, dated archive relationships, distinct operator evidence, safe tag semantics, typed competition participants, source-record reconciliation, derived coverage bounds, deterministic regeneration, generated-artifact reconciliation, repository tests, campaign path boundaries, and `git diff --check`.

No archive evidence, canonical knowledge, graph fact, or publication output is rewritten by this campaign.
