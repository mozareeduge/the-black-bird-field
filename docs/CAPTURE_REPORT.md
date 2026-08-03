# Portfolio media capture report

Governed by `docs/ASSET_MANIFEST.json` and the evidence rule in
`references/DESIGN_UIUX_TECH_SPEC.md` Section 7.1: every portfolio image
must originate from the real released work, rendered locally. No
AI-generated, reconstructed, hand-composited, or simulated screenshots
were produced for this candidate.

## The Black Bird

- Source: `mozareeduge/the-black-bird` at commit `5972b2b2e4a70b2b2f457b6345f84894af95ef2a` (shallow clone).
- Method: the repository's own Playwright evidence suite
  (`tests/black-bird-evidence.spec.js`, run via `npx playwright test`) for
  the two mobile-Field/Read states, plus an ad hoc extension
  (`tests/portfolio-capture.cjs`) reusing its `gotoField`/`clickNode`
  helpers to open specific Research Note and Mapping Note objects in the
  Reader, matching the exact copy-authority alt text for each surface.
- Local static server (`tests/static-server.cjs`), no network egress
  beyond `npm install` from the pinned `registry.npmjs.org`.

## Winter Road

- Source: `mozareeduge/winter-road` at commit `316f6406d31f027a90654f6bd2abf4f4c15026b5`.
- Method: the release's own `window.__winterRoadDiagnostics` diagnostic
  hook (`pinById`, `revealById`) driving the real runtime through a
  minimal local static server. No screenshots existed in this repository
  before capture.

## UNHAPPY Scenario

- Source: `mozareeduge/UNHAPPY-scenario` at commit `9f013baed8f94216f290fbeab8942b8cf4428f8d`.
- Method: none — the repository already ships checksum-verified per-state
  screenshots at `docs/screenshots/` from its own `tests/render_visuals.py`.
  Each file used here was checked against `checksums.sha256` in that
  repository before use. Per-state files are not watermarked (only the
  composite contact sheets are); no re-rendering was necessary or
  performed.
- Index blob at capture: sha1 `fb67ebce1bcce965e4f91f4e8e2e0e36d910abae`,
  matching `references/UNHAPPY_RELEASE_DOMAIN_FACTS.md`.

## Grave-Machine

- Source: `public/works/grave-machine/index.html` in this repository
  (checksum-locked, bilingual v1.1, sha256
  `0e1cfd0097cf261f169c0e52a88d39f1541f04f07d179b1f009ff2cc311eb385`,
  unchanged by this candidate).
- Method: the existing `scripts/capture_grave.py` timed English captures
  (already present in `public/assets/grave-machine/bilingual/`), plus one
  additional ad hoc capture of the same runtime with the فارسی (Persian)
  tab selected, since no Persian-language capture existed yet. No network
  access — the runtime file is local and self-contained.

## TAROKE RIMIXER

- Source: `mozareeduge/taroke-remixer` at commit `cb8e5f3beea0784d5a6690afbae41896a68647b8` (`package.json` version `0.7.8`, matching the copy authority's "v07.8 release checkpoint").
- Method: an ad hoc Playwright script driving the repository's own
  `index.html` (plain static HTML/CSS/JS, no build step) through its
  visible chamber navigation (Samples, Devices, Run) and the
  `window.TarokeDebug.setStep()` debug hook for the mobile
  chamber-navigation shot that touch scrolling made unreliable to hit
  directly. The repository's `docs/screenshots/` history was inspected
  first; it was not reused because several of its checkpoints (notably
  `v07_8/*`) are from a "stripped functional workbench" debug build
  without the shipped visual styling, which would misrepresent the
  released work.

## Repetition and reuse

`scripts/validate_asset_manifest.py` enforces: every work has all seven
required asset roles; no image file is used on more than three portfolio
surfaces. Cross-page reuse (e.g. the same capture serving both a home
surface and a project page) is recorded explicitly in each manifest
entry's `portfolio_surfaces` list.

## Known deviation

Design specification Section 7.2 describes optimized WebP variants under
`public/assets/<work>/portfolio/`. This candidate ships the original PNG
captures directly; WebP conversion and responsive `srcset` variants are
deferred to T-VISUAL-SYSTEM / T-PROGRESSIVE-METADATA, which own the
responsive-image and performance-budget requirements. This is recorded
here as an explicit, not-silent deviation.
