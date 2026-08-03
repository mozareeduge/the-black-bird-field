# Adding a work

The portfolio renders every work from one structured content source and
one generic renderer per surface (D-CONTENT-ARCHITECTURE, D-GENERIC-RENDERER).
There is no per-work template or fragment to copy.

1. **Content.** Add the work's entry to `WORKS` in `src/content.py`
   (`title`, `operative` word, `form`, `year`, `subtitle`, `live_url`,
   `repo_url`, `canonical_route`, `alias_route`, `meta`, `home_feature`,
   `works_index`, `project`) and append its key to `WORK_ORDER`. Every
   visitor-facing string must come from `docs/authority/CANONICAL_COPY.md`
   — do not paraphrase or invent copy in `content.py`.
2. **Assets.** Capture real states of the work per
   `references/DESIGN_UIUX_TECH_SPEC.md` § 7 (or its successor spec for
   later work), following the method in `docs/CAPTURE_REPORT.md`: clone
   the work's own source repository and render its real UI locally
   wherever possible, rather than fetching a live URL. Add the images
   under `public/assets/<work-slug>/portfolio/` and add a corresponding
   `'assets'` block to the work's `WORKS` entry in `content.py` (`hero`,
   `hero_preview`, `home_feature`, `works_thumb`, `views` — four images).
   Add every new file to `docs/ASSET_MANIFEST.json` with its provenance,
   captured state, sha256, and bound portfolio surfaces, then run
   `python scripts/validate_asset_manifest.py`.
3. **Routes.** `src/site_config.py` generates the canonical route, root
   alias, and legacy stub automatically from `WORK_ORDER`/`WORKS` — no
   manual route registry edit is needed. Add the new legacy stub filename
   to `LEGACY_REDIRECTS` if the work should also get a flat-path
   compatibility redirect.
4. **Build and verify.**
   ```bash
   python src/build.py --check
   python -m pytest tests/static/ tests/browser/ -v
   ```
   The route, copy-contract, security, and accessibility suites will all
   pick up the new work automatically since they iterate `WORK_ORDER`.
5. **If the work's runtime is hosted under the portfolio** (like
   Grave-Machine), add the runtime file under `public/works/<work-slug>/`,
   add a checksum entry to `tests/fixtures/checksums.json`, and wire the
   runtime output path in `src/build.py`'s asset-copy step. This is the
   only case where portfolio and artwork deployment are coupled; every
   other work stays on its own autonomous repository and release cadence
   (D-REPOSITORY-AUTONOMY).

Do not create a new per-work CSS class, a duplicate project template, or
a work-specific token branch in the build. If the shared renderer cannot
represent the new work faithfully, that is a design-specification gap to
resolve in the specification, not a reason to special-case the build.
