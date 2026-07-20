# Governance Vote Source Assessment

## Sources reviewed

- The operator-provided PIP-33 on-chain vote export is the campaign's complete input evidence.
- The DecentraGuild SAWT vote interface is useful for proposal summaries, display-name observations, selected-faction colors, and voter-facing review.
- SAWT derives its proposal and vote data through Rogue Data Hub endpoints and applies a latest-event-per-wallet interpretation.

## Evidential use

The supplied export is used for wallet, selection, PVP, signed-message, timestamp, lock, memo-program, and signature fields. The live SAWT summary is corroborative: its displayed 220 ballots and rounded result totals reconcile with the export.

The latest indexed event per wallet is a defensible effective-ballot rule because it preserves vote changes without double-counting a wallet. Superseded events must remain in the event layer.

## Collection cautions

- Display names are ungoverned aliases, not canonical identities.
- Profile colors reflect a selected faction at capture time and are not permanent identity facts.
- UI pagination or API limits can make a web collection incomplete; a complete supplied export is preferred for ballot enumeration.
- Source status language does not establish treasury payment or implementation.
- The signature field is preserved exactly. It contains 148 base64 signature-byte values and 72 longer base64 signed-transaction payloads for memo-enabled records; cryptographic replay is outside this campaign.
