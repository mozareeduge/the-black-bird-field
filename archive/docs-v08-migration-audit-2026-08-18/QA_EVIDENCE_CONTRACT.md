# QA / evidence contract — v08.1

The candidate is judged against `docs/PRODUCT_DESIGN_AUTHORITY.md`, `docs/DESIGN_SYSTEM.md`, the canonical content manifests, and explicit owner decisions. Tests are evidence, not authority.

## Required distinction

- **PRODUCT DEFECT:** candidate behavior contradicts accepted authority.
- **PROOF GAP:** behavior may be correct but evidence is insufficient.
- **STALE TEST/DOC:** an oracle or description conflicts with accepted truth.
- **HEURISTIC QUALITY RISK:** professional/visual judgment not elevated into a contractual defect.

## Candidate-bound gates

Detached handoff candidate:

```bash
python src/build.py --package-preview
python -m pytest tests/static -q
python validation/check_motion_media.py
python validation/validate_v8_craft.py
python validation/validate_candidate.py
python validation/run_v8_canaries.py
```

Real migrated repository candidate additionally runs strict build and browser tests after protected artifacts are present:

```bash
python src/build.py --check
python -m pytest tests/browser -q
```

## Evidence classes

- static source/manifest checks for identity, copy, paths, file budgets and token invariants;
- Chromium execution for rendered geometry, overflow, focus/menu behavior and preview selection;
- media technical inspection for codec/duration/audio/dimensions;
- before/after screenshots for owner visual comparison;
- canaries/negative controls to show critical tests fail when the protected behavior is deliberately sabotaged.

A screenshot does not prove timing. A simulation does not prove production deployment. Owner artistic acceptance remains separate from automated engineering PASS.

## Environment limitation

This sandbox blocks normal Chromium navigation to localhost. `validation/validate_candidate.py` therefore executes the exact candidate HTML/CSS/JS/image bytes in Chromium through an in-memory document while static tests validate the relative file graph. The actual target/CI must still run the HTTP browser suite.
