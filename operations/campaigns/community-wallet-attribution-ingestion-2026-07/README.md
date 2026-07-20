# Community Wallet Attribution Ingestion 2026-07

This campaign preserves the operator-submitted `Star Atlas Team Wallets.xlsx` byte-for-byte and normalizes all 84 supplied Solana address associations as qualified community attributions.

The repository operator assesses the associations as highly likely. That assessment is not represented as official confirmation or verified ownership/control. The workbook contains labels spanning Team, Rewards, DAO, Liquidity, FTX, and Private Sale groups; it must not be read as a homogeneous register of ATMTA-owned accounts.

## Evidence boundary

- Source class: `COMMUNITY_EFFORT`
- Operator assessment: `HIGH_LIKELIHOOD`
- Official confirmation: `UNCONFIRMED`
- Ownership/control verification: `UNVERIFIED`
- On-chain observation: `NOT_CHECKED`
- Compiler, methodology, source location, and dates: `UNKNOWN`

Syntactic validation confirms only that every address decodes as a 32-byte Solana public key. It does not establish identity, ownership, control, purpose, activity, or temporal duration.

## Outputs

- Immutable workbook: `archive/raw/community-wallet-attributions/Star Atlas Team Wallets.xlsx`
- Custody record: `archive/provenance/community-wallet-attributions/star-atlas-team-wallets.json`
- Normalized register: `archive/normalized/community-wallet-attributions/wallet-attributions.jsonl`
- Collection metadata: `archive/normalized/community-wallet-attributions/metadata.json`
- Paired Source Records: `archive/source-records/community-wallet-attributions/`
- Archive and campaign manifests
- Accepted curator-decision ledger, campaign summary, and validation reports

No `knowledge/`, `graph/`, or `publication/` output is created.

## Reproduction

Run from the repository root:

```powershell
python operations/campaigns/community-wallet-attribution-ingestion-2026-07/build_campaign.py
python operations/campaigns/community-wallet-attribution-ingestion-2026-07/validate_campaign.py
```

## Human adjudication

WAL-001 through WAL-004 were accepted by the repository operator on 2026-07-20. No campaign-blocking human decision remains. All 84 row-level associations retain manual-review status because the underlying attribution evidence and verification dataset are unavailable.
