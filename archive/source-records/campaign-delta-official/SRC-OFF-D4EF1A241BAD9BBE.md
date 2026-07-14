# configs README

## Metadata

- Source ID: `SRC-OFF-D4EF1A241BAD9BBE`
- URL: https://github.com/staratlasmeta/configs#readme
- Publication date: 2024-10-28T20:25:28Z
- Updated date: 2026-02-27T01:20:09Z
- Original date text: 2024-10-28T20:25:28Z
- Author: ATMTA / Star Atlas official publisher
- Publisher: staratlasmeta GitHub organization
- Document classification: `TECHNICAL_DOCUMENTATION`
- Extraction confidence: `HIGH`

## Official Authority Boundary

This record establishes what the named official publisher publicly stated and when. It does not by itself prove execution, independent economic accuracy, historical completeness, or absence of contrary evidence.

## Archival Abstract

Official technical documentation titled “configs README.” This record preserves what staratlasmeta GitHub organization publicly stated at the recorded publication time; claims about delivery, economics, or outcomes remain limited to the wording of the source.

## Products

- ATLAS

## Actors and Organizations

- None identified.

## Governance

- None identified.

## Lore

- None identified.

## Classified Claims

- # @staratlas/configs  Shared configuration package for Star Atlas projects.
- This package supports multiple toolchains (`oxc`, `vite`, `typescript`, plus legacy `eslint`/`prettier` exports), but you do not need to use all of it.
- ## Get Exactly What You Need (Important)  ### What is actually minimal?
- `Usage size` (what your project actually imports/extends) 2.
- `Install size` (what the package manager downloads)  This package is a single npm package, so install-time contents are **not tree-shaken**.
- What you can minimize very effectively is the **usage surface** by using subpath exports.
- - `@staratlas/configs` is one package, so install-time contents are shared.
- - Peer deps are marked optional, so you can skip unrelated tools.
- ## Use Subpath Exports (Recommended)  Use only the subpaths you need instead of importing broad modules.
- ### OXC-only project (recommended default)  ```bash pnpm add -D @staratlas/configs oxlint oxfmt typescript ```  ### Vite library project (non-Solid)  ```bash pnpm add -D @staratlas/configs vite typescript ```  Add Vite plugin peers only if you use helpers that need them.
- ### Solid + Vite project  ```bash pnpm add -D @staratlas/configs vite typescript solid-js vite-plugin-solid-oxc solid-jsx-oxc vite-plugin-solid-svg ```  ## How to Reduce Size / Complexity Further  ### 1.
- Prefer subpaths over broad usage  Good:  - `@staratlas/configs/oxc/oxlint-master.json` - `@staratlas/configs/base.json` - `@staratlas/configs/vite`  Avoid (when unnecessary):  - importing/using multiple surfaces if you only need one - adding ESLint/Prettier dependencies if you are standardizing on OXC  ### 2.
- Keep tooling local to the project that needs it  In a monorepo, only install Vite/Solid deps in frontend packages (or root if shared by policy).
- Copy configs locally if you need zero package coupling  If a project must minimize dependency coupling, copy the exported JSON config into that repo and pin your own tool versions.
- You lose centralized updates, but gain maximum independence.

## Official Cross-References

- None identified.

## Temporal Validity

- Status: `CURRENT_DOCUMENTATION`
- Current validity: `CURRENT_PAGE_NOT_HISTORICAL_PROOF`
- Warning: Official publication does not independently prove successful execution, completeness, or continued current validity.

## Open Questions

- Which claims are independently corroborated or later superseded?

## Preserved Official Text

# @staratlas/configs

Shared configuration package for Star Atlas projects.

This package supports multiple toolchains (`oxc`, `vite`, `typescript`, plus legacy `eslint`/`prettier` exports), but you do not need to use all of it.

## Get Exactly What You Need (Important)

### What is actually minimal?

There are two different kinds of “size”:

1. `Usage size` (what your project actually imports/extends)
2. `Install size` (what the package manager downloads)

This package is a single npm package, so install-time contents are **not tree-shaken**.

What you can minimize very effectively is the **usage surface** by using subpath exports.

### Fast Matrix: Install Only What You Need

| You need | Install | Use |
| --- | --- | --- |
| OXC lint + format only | `@staratlas/configs` `oxlint` `oxfmt` `typescript` | `@staratlas/configs/oxc/oxlint-master.json` + `@staratlas/configs/oxc/oxfmt-master.json` |
| OXC lint (React) | `@staratlas/configs` `oxlint` `typescript` | `@staratlas/configs/oxc/oxlint-react.json` |
| OXC lint (Next) | `@staratlas/configs` `oxlint` `typescript` | `@staratlas/configs/oxc/oxlint-next.json` |
| TypeScript base only | `@staratlas/configs` `typescript` | `@staratlas/configs/base.json` |
| TypeScript + Solid JSX | `@staratlas/configs` `typescript` | `@staratlas/configs/base.json` + `@staratlas/configs/solid.json` |
| Vite helpers (library/site config helpers) | `@staratlas/configs` `vite` `typescript` | `@staratlas/configs/vite` |
| Vite + Solid (OXC plugin) | `@staratlas/configs` `vite` `typescript` `solid-js` `vite-plugin-solid-oxc` `solid-jsx-oxc` `vite-plugin-solid-svg` | `@staratlas/configs/vite` + `solidConfig()` |

Notes:

- This matrix minimizes **what your project uses**, not what npm/pnpm downloads.
- `@staratlas/configs` is one package, so install-time contents are shared.
- Peer deps are marked optional, so you can skip unrelated tools.

## Use Subpath Exports (Recommended)

Use only the subpaths you need instead of importing broad modules.

### OXC only (smallest usage surface)

Use these files directly:

- `@staratlas/configs/oxc/oxlint-master.json`
- `@staratlas/configs/oxc/oxlint-react.json`
- `@staratlas/configs/oxc/oxlint-next.json`
- `@staratlas/configs/oxc/oxfmt-master.json`

Example `package.json` scripts:

```json
{
  "scripts": {
    "lint": "oxlint -c ./node_modules/@staratlas/configs/oxc/oxlint-master.json .",
    "format": "oxfmt --check -c ./node_modules/@staratlas/configs/oxc/oxfmt-master.json .",
    "format:fix": "oxfmt -c ./node_modules/@staratlas/configs/oxc/oxfmt-master.json ."
  }
}
```

If you are using React or Next, swap the lint config:

- React: `oxlint-react.json`
- Next: `oxlint-next.json`

### TypeScript only

Use TS config subpaths only:

- `@staratlas/configs/base.json`
- `@staratlas/configs/solid.json` (only if using Solid)

Example `tsconfig.json` (library/app):

```json
{
  "extends": ["@staratlas/configs/base.json"],
  "include": ["src"]
}
```

Example Solid project:

```json
{
  "extends": ["@staratlas/configs/base.json", "@staratlas/configs/solid.json"],
  "include": ["src"]
}
```

### Vite helpers only

Import only `@staratlas/configs/vite`:

```ts
import { combineConfigs, libConfig, cleanupConfig } from '@staratlas/configs/vite';
import type { UserConfig } from 'vite';

export default combineConfigs(
  libConfig('src/index.ts'),
  cleanupConfig(),
) satisfies UserConfig;
```

Solid (OXC plugin) example:

```ts
import { combineConfigs, libConfig, cleanupConfig, solidConfig } from '@staratlas/configs/vite';
import type { UserConfig } from 'vite';

export default combineConfigs(
  libConfig('src/index.tsx'),
  cleanupConfig(),
  solidConfig({
    solidPlugin: {
      hydratable: true
    }
  }),
) satisfies UserConfig;
```

## Install Only the Tooling You Use

`@staratlas/configs` exposes multiple surfaces, but its peers are marked optional so you can install only the tools you actually run.

### OXC-only project (recommended default)

```bash
pnpm add -D @staratlas/configs oxlint oxfmt typescript
```

### Vite library project (non-Solid)

```bash
pnpm add -D @staratlas/configs vite typescript
```

Add Vite plugin peers only if you use helpers that need them.

### Solid + Vite project

```bash
pnpm add -D @staratlas/configs vite typescript solid-js vite-plugin-solid-oxc solid-jsx-oxc vite-plugin-solid-svg
```

## How to Reduce Size / Complexity Further

### 1. Prefer subpaths over broad usage

Good:

- `@staratlas/configs/oxc/oxlint-master.json`
- `@staratlas/configs/base.json`
- `@staratlas/configs/vite`

Avoid (when unnecessary):

- importing/using multiple surfaces if you only need one
- adding ESLint/Prettier dependencies if you are standardizing on OXC

### 2. Keep tooling local to the project that needs it

In a monorepo, only install Vite/Solid deps in frontend packages (or root if shared by policy). Backend/CLI packages can use only TS + OXC.

### 3. Copy configs locally if you need zero package coupling

If a project must minimize dependency coupling, copy the exported JSON config into that repo and pin your own tool versions. You lose centralized updates, but gain maximum independence.

## Current Exports

### OXC

- `@staratlas/configs/oxc/oxlint-master.json` (framework-neutral strict anti-tech-debt baseline)
- `@staratlas/configs/oxc/oxlint-react.json` (React + JSX a11y strict variant)
- `@staratlas/configs/oxc/oxlint-next.json` (Next strict variant)
- `@staratlas/configs/oxc/oxfmt-master.json`

### TypeScript

- `@staratlas/configs/base.json`
- `@staratlas/configs/solid.json`

### Vite

- `@staratlas/configs/vite`

### Legacy (still supported)

- `@staratlas/configs/eslint`
- `@staratlas/configs/prettier`

These remain for compatibility. OXC is the default lint/format path for this package.

## Quick Start Recipes

### Minimal OXC + TS project

```bash
pnpm add -D @staratlas/configs oxlint oxfmt typescript
```

`package.json`

```json
{
  "scripts": {
    "lint": "oxlint -c ./node_modules/@staratlas/configs/oxc/oxlint-master.json .",
    "format": "oxfmt --check -c ./node_modules/@staratlas/configs/oxc/oxfmt-master.json .",
    "format:fix": "oxfmt -c ./node_modules/@staratlas/configs/oxc/oxfmt-master.json ."
  }
}
```

`tsconfig.json`

```json
{
  "extends": ["@staratlas/configs/base.json"],
  "include": ["src"]
}
```

### Minimal Vite library

```bash
pnpm add -D @staratlas/configs vite typescript
```

`vite.config.ts`

```ts
import { cleanupConfig, combineConfigs, libConfig } from '@staratlas/configs/vite';

export default combineConfigs(libConfig('src/index.ts'), cleanupConfig());
```

## Maintainers (this package)

This package itself is OXC-first:

- `pnpm lint` -> `oxlint`
- `pnpm format` -> `oxfmt --check`

Legacy build/export surfaces (`eslint`, `prettier`) are still published for downstream compatibility.

