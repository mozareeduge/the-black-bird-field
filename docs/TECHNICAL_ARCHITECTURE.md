# Technical architecture — The Black Bird Field v08.1

## Runtime shape

The portfolio is a generated static site. There is no application backend, database, login, analytics dependency, or client-side semantic data store.

```text
content/site.json + content/works/*.json
              ↓
       src/content.py
              ↓
       src/renderers.py
              ↓
         src/build.py
              ↓
             dist/
              ↓
        GitHub Pages
```

`dist/` is generated output, never a second semantic implementation.

## Source authority

- Shared visitor copy, identity and site links: `content/site.json`.
- One work = one manifest: `content/works/<slug>.json`.
- Work schema: `content/work.schema.json`.
- HTML structure and route derivation: `src/renderers.py` + `src/build.py`.
- Visual system and responsive transformations: `public/site.css`.
- Menu, Home preview selection and progressive motion: `public/site.js`.
- Still/video source media: `public/assets/<asset_slug>/`.
- Protected inherited runtime/CV identities: `content/protected_artifacts.json`.

## Canonical public surface

Canonical pages are `/`, `/works/`, five `/works/<slug>/` pages, `/practice/`, `/about/`, and `/contact/`. Root `.html` compatibility outputs are redirects only and remain out of the canonical sitemap.

The Grave-Machine live runtime and academic CV are protected current-production artifacts. Migration preserves their source bytes exactly; the portfolio build copies them to their declared output paths during strict production build.

## Motion architecture

Motion is manifest capability data, not a site-wide mode. Current works opt into `home_preview` and `project_hero` only. Home owns one selected video source at a time. Selection unloads the previous source. Project video pauses off viewport. `prefers-reduced-motion`, Save Data, no-JS and failed/unloaded video expose the manifest-declared still poster.

Motion never becomes a second source of work identity, copy, route order, or state.

## Extension rule

Adding a future work is normally:

1. one new work manifest with unique slug/order;
2. required responsive still assets;
3. optional motion block + desktop/mobile loop files;
4. build/tests.

Shared layout, existing manifests and design tokens do not change merely because work count changes. `tests/static/test_add_work_scaling.py` guards this property.

## Release / rollback

Repository replacement is applied to a clean clone of audited production through `scripts/apply_to_current_repo.py`. It verifies exact target HEAD, origin and protected bytes before and after copying replacement-owned surfaces. It does not commit, push, create a PR, merge or deploy.

Old production is archived by exact annotated Git tag, not by keeping a duplicate old site tree inside the new public product. Rollback remains normal Git history/revert/tag checkout; force rewriting history is prohibited.

## Work-count scaling

Work count is derived from manifests across Home, Works, project routes, sitemap, metadata/count copy, browser QA routes and motion checks. A 12-work disposable build guards against hidden five-work assumptions. Visual curation of a very long Home index remains an experience decision, not a data/build limitation.
