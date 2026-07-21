# DAO Vote Evidence Source Assessment

## Source reviewed

- Operator-supplied archive: `Star Atlas DAO PIP Votes.zip`
- SHA-256: `4e01123f31a2531427fc1910841efae45e24b15f4472338fbbf174c2e5b52d08`
- Included in this campaign: PIP-1 through PIP-32
- Excluded: PIP-33, already ingested by the dedicated PIP-33 campaign

The repository operator states that the export represents the complete Star Atlas DAO vote record, pulled directly from Solana and viewed through the official Star Atlas DAO website. This campaign therefore assigns `A1` source authority for the supplied ballot evidence.

## Structural findings

- 32 included JSON files parse successfully.
- 8,404 vote records have unique UUIDs and unique validation values.
- Each PIP has exactly one proposal UUID and one proposal hash.
- No wallet appears more than once within a PIP.
- Every signed message agrees with its record's wallet, PIP number, proposal hash, and ballot selection.
- 27 proposals use binary YES/NO/ABSTAIN ballots.
- Five proposals use ordered ranked-choice ballots: PIP-6, PIP-7, PIP-11, PIP-25, and PIP-27.

## Validation payloads

All validation values are valid base64. For 5,977 non-memo records, they decode to 64-byte detached-signature representations. For 2,427 memo-enabled records, they decode to longer serialized transaction-like payloads. The latter are not mislabeled as conventional Solana transaction signatures.

The package does not include transaction IDs, slots, block heights, block timestamps, program or account addresses, cluster identifiers, RPC provenance, or an internal checksum manifest. Independent replay is recorded as `NOT_PERFORMED`.

## Timestamp finding

The signed message and portal record timestamp are separate evidence. In 278 records, the portal's `createdAt` precedes the embedded signed-message timestamp, with the largest observed reversal exceeding two hours. This may represent client-clock or persistence skew, but the campaign does not adjudicate the cause. Both values are preserved and the ordering anomaly is flagged.

## Evidential use

The export supports:

- individual ballot selections and ranking order;
- wallet-level ballot identity;
- exact raw PVP values;
- signed-message content and timestamp;
- raw POLIS lock amount and expiry;
- exact validation payloads and memo-program indicator;
- proposal-level aggregate reconciliation.

It does not, by itself, support:

- named-person identity attribution;
- final STV reconstruction without the tally implementation;
- proposal implementation or completion;
- treasury authorization beyond the vote result;
- treasury payment or on-chain transfer verification;
- later operational outcomes.
