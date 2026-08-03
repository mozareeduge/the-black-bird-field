## Summary

Finalizes The Black Bird Field as a five-work portfolio (adding UNHAPPY
Scenario) per `BLACK-BIRD-FIELD-FIVE-WORK-FINALIZATION@1.0.1`:

- New structured content authority (`src/content.py`, transcribed verbatim
  from `docs/authority/CANONICAL_COPY.md`) and one generic renderer per
  surface — no more per-work templates or fragments.
- Route registry generates 10 canonical pages, 5 full root aliases, and 9
  legacy stubs from the work order; Grave-Machine's checksum-locked
  runtime is unchanged and re-verified.
- All portfolio media recaptured from the real released works (see
  `docs/CAPTURE_REPORT.md`) and bound to a validated asset manifest
  (`docs/ASSET_MANIFEST.json`).
- Final visual system: semantic tokens, self-hosted Source Serif 4 / IBM
  Plex Sans / IBM Plex Mono / Estedad, the full responsive breakpoint
  matrix, and Encounter Score / State Atlas fully removed.
- Single `site.js` (menu + wide-screen preview only); CSP, referrer
  policy, JSON-LD, and direct CV download; core content and navigation
  verified with JavaScript disabled.
- CI consolidated into one quality+deploy Pages workflow; release-action
  scripts installed (not executed) for the gated push/PR, UNHAPPY-domain,
  and merge/deploy steps.

## Test plan

- [x] `python src/build.py --check` — build + Grave-Machine checksum
- [x] `python -m pytest tests/static/ tests/browser/ -v` — 250 passed
- [x] `python scripts/validate_authority_environment.py`
- [x] `python scripts/validate_asset_manifest.py`
- [x] `python scripts/validate_test_authority.py`
- [x] `python scripts/validate_workflows.py`
- [x] `python scripts/validate_release_evidence.py`
- [ ] Human visual/curatorial review (`C-VISUAL-REVIEW`) — reserved for
      the repository owner; automated checks passing is not artistic
      acceptance.

See `artifacts/release/RELEASE_EVIDENCE.json` for the complete candidate
identity, check results, budgets, and the explicit deviations list.
