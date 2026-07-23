# Star Atlas Decoders

<p align="center">
  <a href="https://github.com/staratlasmeta/star-atlas-decoders/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/staratlasmeta/star-atlas-decoders/ci.yml?logo=GitHub" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-Apache%202.0-blue" />
  </a>
</p>

<p align="center">
  <a href="https://crates.io/crates/carbon-sage-starbased-decoder">
    <img src="https://img.shields.io/crates/v/carbon-sage-starbased-decoder?logo=rust&label=sage-starbased" />
  </a>
  <a href="https://crates.io/crates/carbon-sage-holosim-decoder">
    <img src="https://img.shields.io/crates/v/carbon-sage-holosim-decoder?logo=rust&label=sage-holosim" />
  </a>
  <a href="https://crates.io/crates/carbon-atlas-staking-decoder">
    <img src="https://img.shields.io/crates/v/carbon-atlas-staking-decoder?logo=rust&label=atlas-staking" />
  </a>
  <a href="https://crates.io/crates/carbon-locked-voter-decoder">
    <img src="https://img.shields.io/crates/v/carbon-locked-voter-decoder?logo=rust&label=locked-voter" />
  </a>
  <a href="https://crates.io/crates/carbon-marketplace-decoder">
    <img src="https://img.shields.io/crates/v/carbon-marketplace-decoder?logo=rust&label=marketplace" />
  </a>
  <a href="https://crates.io/crates/carbon-atlas-fee-payer-decoder">
    <img src="https://img.shields.io/crates/v/carbon-atlas-fee-payer-decoder?logo=rust&label=atlas-fee-payer" />
  </a>
  <a href="https://crates.io/crates/carbon-cargo-decoder">
    <img src="https://img.shields.io/crates/v/carbon-cargo-decoder?logo=rust&label=cargo" />
  </a>
  <a href="https://crates.io/crates/carbon-crafting-decoder">
    <img src="https://img.shields.io/crates/v/carbon-crafting-decoder?logo=rust&label=crafting" />
  </a>
  <a href="https://crates.io/crates/carbon-crew-decoder">
    <img src="https://img.shields.io/crates/v/carbon-crew-decoder?logo=rust&label=crew" />
  </a>
  <a href="https://crates.io/crates/carbon-profile-vault-decoder">
    <img src="https://img.shields.io/crates/v/carbon-profile-vault-decoder?logo=rust&label=profile-vault" />
  </a>
  <a href="https://crates.io/crates/carbon-srsly-decoder">
    <img src="https://img.shields.io/crates/v/carbon-srsly-decoder?logo=rust&label=srsly" />
  </a>
  <a href="https://crates.io/crates/carbon-tcomp-decoder">
    <img src="https://img.shields.io/crates/v/carbon-tcomp-decoder?logo=rust&label=tcomp" />
  </a>
  <a href="https://crates.io/crates/carbon-player-profile-decoder">
    <img src="https://img.shields.io/crates/v/carbon-player-profile-decoder?logo=rust&label=player-profile" />
  </a>
  <a href="https://crates.io/crates/carbon-points-decoder">
    <img src="https://img.shields.io/crates/v/carbon-points-decoder?logo=rust&label=points" />
  </a>
  <a href="https://crates.io/crates/carbon-points-store-decoder">
    <img src="https://img.shields.io/crates/v/carbon-points-store-decoder?logo=rust&label=points-store" />
  </a>
  <a href="https://crates.io/crates/carbon-profile-faction-decoder">
    <img src="https://img.shields.io/crates/v/carbon-profile-faction-decoder?logo=rust&label=profile-faction" />
  </a>
  <a href="https://crates.io/crates/carbon-score-decoder">
    <img src="https://img.shields.io/crates/v/carbon-score-decoder?logo=rust&label=score" />
  </a>
  <a href="https://crates.io/crates/carbon-claim-stake-decoder">
    <img src="https://img.shields.io/crates/v/carbon-claim-stake-decoder?logo=rust&label=claim-stake" />
  </a>
  <a href="https://crates.io/crates/carbon-proxy-rewarder-decoder">
    <img src="https://img.shields.io/crates/v/carbon-proxy-rewarder-decoder?logo=rust&label=proxy-rewarder" />
  </a>
  <a href="https://crates.io/crates/carbon-snapshots-decoder">
    <img src="https://img.shields.io/crates/v/carbon-snapshots-decoder?logo=rust&label=snapshots" />
  </a>
</p>

Rust decoders for Star Atlas Solana programs, generated from IDLs using Carbon CLI with custom patches for complex account deserialization.

## Overview

This project generates and maintains Rust decoders for Star Atlas programs on Solana. It uses [Carbon CLI](https://github.com/sevenlabs-hq/carbon) to generate initial decoder code from program IDLs, then applies custom patches to handle complex account structures that require manual deserialization logic.

### Supported Decoders

- **sage-starbased**: SAGE Starbase program (`SAGE2HAwep459SNq61LHvjxPk4pLPEJLoMETef7f7EE`)
  - Fleet and starbase management for Star Atlas
  - Custom patches for remaining data deserialization

- **sage-holosim**: SAGE Holosim program (`SAgEeT8u14TE69JXtanGSgNkEdoPUcLabeyZD2uw8x9`)
  - Fleet and starbase management for Star Atlas (uses local IDL)
  - Custom patches for remaining data deserialization

- **atlas-staking**: Atlas Staking program (`ATLocKpzDbTokxgvnLew3d7drZkEzLzDpzwgrgWKDbmc`)
  - ATLAS token staking with configurable rewards and cooldown periods
  - Minimal patches for serialization support

- **locked-voter**: Locked Voter program (`Lock7kBijGCQLEFAmXcengzXKA88iDNQPriQ7TbgeyG`)
  - POLIS governance and voting with escrow and whitelist controls
  - Minimal patches for serialization support

- **marketplace**: Galactic Marketplace program (`traderDnaR5w6Tcoi3NFm53i48FTDNbGjBSZwWXDRrg`)
  - NFT marketplace with order books, currency management, and royalty tiers
  - Minimal patches for serialization support

- **atlas-fee-payer**: ATLAS Fee Payer program (`APR1MEny25pKupwn72oVqMH4qpDouArsX8zX4VwwfoXD`)
  - Fee payment management for Star Atlas transactions
  - Minimal patches for serialization support

- **cargo**: Cargo program (`Cargo2VNTPPTi9c1vq1Jw5d3BWUNr18MjRtSupAghKEk`)
  - Resource container management with dynamic stat tracking
  - Custom patches for remaining data deserialization

- **crafting**: Crafting program (`CRAFT2RPXPJWCEix4WpJST3E7NLf79GTqZUL75wngXo5`)
  - Recipe-based item crafting with facilities and process tracking
  - Custom patches for type-safe enum handling and remaining data deserialization

- **crew**: Crew Management program (`CREWiq8qbxvo4SKkAFpVnc6t7CRQC4tAAscsNAENXgrJ`)
  - Crew management for Star Atlas ships and operations
  - Minimal patches for serialization support

- **profile-vault**: Profile Vault program (`pv1ttom8tbyh83C1AVh6QH2naGRdVQUVt3HY1Yst5sv`)
  - Profile vault management for Star Atlas player profiles
  - Minimal patches for serialization support

- **srsly**: Fleet Rentals (SRSLY) program (`SRSLY1fq9TJqCk1gNSE7VZL2bztvTn9wm4VR8u8jMKT`)
  - Fleet rental contracts and automated payment processing
  - Custom patches for numeric field handling

- **tcomp**: Tensor cNFT Compressed program (`TCMPhJdwDryooaGtiocG1u3xcYbRpiJzb283XfCZsDp`)
  - Compressed NFT marketplace for trading cNFTs
  - Minimal patches for serialization support

- **player-profile**: Player Profile program (`pprofELXjL5Kck7Jn5hCpwAL82DpTkSYBENzahVtbc9`)
  - Player identity and role-based access control for Star Atlas
  - Custom patches for remaining data deserialization

- **points**: Points program (`Point2iBvz7j5TMVef8nEgpmz4pDr7tU7v3RjAfkQbM`)
  - Player progression with points, levels, and token-gated unlocks
  - Custom patches for remaining data deserialization (point category levels)

- **points-store**: Points Store program (`PsToRxhEPScGt1Bxpm7zNDRzaMk31t8Aox7fyewoVse`)
  - Token purchases and redemptions using points
  - Custom patches for remaining data deserialization (redemption config epochs)

- **profile-faction**: Profile Faction program (`pFACSRuobDmvfMKq1bAzwj27t6d2GJhSCHb1VcfnRmq`)
  - Player faction affiliation management for Star Atlas universe
  - Custom patches for type-safe faction handling

- **score**: SCORE Fleet Staking program (`FLEET1qqzpexyaDpqb2DGsSzE2sDCizewCg9WjrA6DBW`)
  - Legacy fleet staking system for Star Atlas ships
  - Minimal patches for serialization support

- **claim-stake**: Claim Stake program (`STAKEr4Bh8sbBMoAVmTDBRqouPzgdocVrvtjmhJhd65`)
  - Staking and claim management for Star Atlas rewards
  - Minimal patches for serialization support

- **proxy-rewarder**: Proxy Rewarder program (`gateVwTnKyFrE8nxUUgfzoZTPKgJQZUbLsEidpG4Dp2`)
  - Proxy-based reward distribution for locked token holders
  - Minimal patches for serialization support

- **snapshots**: Snapshots program (`snapNQkxsiqDWdbNfz8KVB7e3NPzLwtHHA6WV8kKgUc`)
  - Historical state snapshots for escrow and locker accounts
  - Minimal patches for serialization support

## Prerequisites

Run `./scripts/check-tools.sh` to verify all required tools are installed:

- **Rust** (1.85+ for edition 2024)
- **Carbon CLI**: `cargo install --git https://github.com/sevenlabs-hq/carbon.git carbon-cli`
- **Just**: `cargo install just` or `brew install just`
- **Git** and standard Unix tools (sed, find)

## Quick Start

```bash
# Check required tools
./scripts/check-tools.sh

# Build all decoders and run CI checks
./scripts/ci.sh
```

## Project Structure

```
star-atlas-decoders/
├── carbon-decoders/         # Published decoder crates
├── dist/                    # Temporary build directory (gitignored)
├── patches/                 # Custom patches for decoders
├── idl/                     # Local IDL files
├── scripts/                 # CI and utility scripts
│   ├── ci-clean.sh          # Full CI pipeline
│   ├── ci.sh                # GitHub CI pipeline
│   └── check-tools.sh       # Tool verification
├── docs/                    # Documentation
│   ├── adding-new-decoder.md
│   ├── patch-development-workflow.md
│   └── readmes/             # Individual decoder READMEs
├── tools/                   # Development tools
│   └── decoder-explorer/    # Test decoders against live accounts
└── justfile                 # Build automation
```

## Development Workflow

### Building Decoders

The build process follows these stages:

1. **Generate**: Fetch IDL and generate initial decoder code
2. **Prepare**: Fix compilation issues (array sizes, workspace refs)
3. **Patch**: Apply custom implementations for complex accounts
4. **Publish**: Move to workspace and verify compilation

```bash
# Full pipeline for a decoder
just all-sage-starbased

# Individual steps
just generate-sage-starbased   # Generate from IDL
just build-sage-starbased      # Clean + generate + prepare
just apply-patches-sage-starbased  # Apply custom patches
just publish-sage-starbased    # Move to workspace
```

### Creating Custom Patches

Some accounts require custom deserialization for "remaining data" fields or dynamic arrays not in the IDL:

```bash
# 1. Build clean decoder
just build-sage-starbased

# 2. Apply existing patches
just apply-patches-sage-starbased

# 3. Edit files in dist/sage-starbased/
cd dist/sage-starbased
# Make your changes
vim src/accounts/fleet.rs

# 4. Test changes
cargo check

# 5. Create patch
just create-patch-sage-starbased my-change

# 6. Publish to workspace
just publish-sage-starbased
```

See [docs/patch-development-workflow.md](docs/patch-development-workflow.md) for detailed instructions.

### Patch Naming Convention

When multiple patches need specific ordering, use numbered prefixes:
- `sage-starbased-01-accounts.patch` (applied first)
- `sage-starbased-02-instructions.patch` (applied second)

## Common Commands

### CI and Testing

```bash
# Run full CI pipeline
./scripts/ci.sh

# Run clippy
# cargo clippy --all-targets --all-features -- -D warnings

# Run tests
cargo test --all
```

### Maintenance

```bash
# Clean build artifacts
just clean-all

# List available patches
just list-patches
```

## Custom Implementations

The decoders include custom deserialization for accounts with:

- **Variable-length "remaining data" fields**: e.g., Fleet's `fleet_state`, CargoType's `cargo_stats`, CargoPod's `cargo_contents`
- **Dynamic arrays not in IDL**: e.g., StarbasePlayer's `ship_escrows`, Profile's `profile_keys`
- **Complex nested structures**: Custom BorshDeserialize implementations

Example accounts with custom deserialization:
- `Fleet`: Includes `fleet_state` enum for current fleet activity
- `StarbasePlayer`: Includes dynamic `ship_escrows` list
- `CargoType`: Includes `cargo_stats` array (length = `stats_count`)
- `CargoPod`: Includes `cargo_contents` array of u64 values

> For detailed patch implementations, see the `patches/` directory and individual decoder READMEs in `docs/readmes/`.

## Technical Details

- **Rust Edition**: 2024 (requires Rust 1.85.0+)
- **Carbon Version**: 0.12.0 (available on [crates.io](https://crates.io/crates/carbon-core))
- **Solana SDK**: 3.x
- **Platform**: macOS and Linux compatible

## Tools

### [Decoder Explorer](tools/decoder-explorer/README.md)

CLI tool for testing and debugging Carbon decoders against live Solana accounts. Fetches all program accounts and analyzes decoder success rates, type distributions, and failure patterns.

```bash
cd tools/decoder-explorer
RPC_URL="https://api.mainnet-beta.solana.com" cargo run --release --features cargo
```

## Contributing

1. Follow the existing patch workflow for modifications
2. Ensure all changes pass `./scripts/ci.sh`
3. Document any new custom deserializations
4. Use numbered patch prefixes when order matters

## License

This project is licensed under the [Apache-2.0](LICENSE) license.

## Resources

- [Carbon CLI Documentation](https://github.com/sevenlabs-hq/carbon)
- [Star Atlas Build](https://build.staratlas.com/)
