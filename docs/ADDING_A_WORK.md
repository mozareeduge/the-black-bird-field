# Adding a work — bounded procedure

The architecture is intentionally designed so a sixth work is an addition, not another portfolio rebuild.

## 1. Verify the work first

Before writing portfolio copy, read the work's canonical repository/release record. Record the exact public title, release/build identity, live URL, repository URL, language, encounter mode, and citation. Do not infer a version number from a development branch.

## 2. Scaffold one record

```bash
python scripts/add_work.py \
  --slug new-work \
  --title "New Work" \
  --form "A …" \
  --mode "Read"
```

Optional: `--year 2027`. The command creates only `content/works/new-work.json` and `public/assets/new-work/`, using the next contiguous order number.

## 3. Author the manifest

Replace every `TODO`. The record owns the work’s portfolio title, form, summary, Home responsibility phrase, project metadata, live/source URLs, release/build identity, project lead, three reading conditions, three selected views, context, language/encounter, and citation.

Do **not** edit Home, Works, footer, sitemap, route registries, repeated work counts, or a separate project HTML file. They are generated.

## 4. Add four responsive image pairs

Default scaffold:

```text
poster-desktop.webp       poster-mobile.webp
view-01-desktop.webp      view-01-mobile.webp
view-02-desktop.webp      view-02-mobile.webp
view-03-desktop.webp      view-03-mobile.webp
```

`feature_image` must name one of the three selected-view roles. Images must be authentic captures or authored portfolio media for the work, not generated substitutes.

## 5. Build and test

```bash
python src/build.py --check
python -m pytest tests/static -q
python -m pytest tests/browser -q
```

The generator updates the Home preview/index, Home feature sequence, all dynamic work-count language, Works index, `/works/<slug>/`, metadata, sitemap, and footer. Tests enforce that Home preview frames and links share the same ordered slug sequence.

## 6. Curatorial review only where the new work genuinely changes a claim

`Practice` is not algorithmically rewritten. Review its prose only if the new work changes the portfolio’s actual practice-level proposition. This is editorial judgment, not a technical dependency.


## Count scaling and current proof

The source/build/test path is count-agnostic. Current identity tests protect the original five as the stable prefix rather than asserting that the portfolio must contain exactly five works. Browser routes, sitemap expectations, Home preview mapping, motion counts and generated work-count language derive from the manifests.

A disposable test now builds **12 works from manifests without editing shared renderer/CSS/JS code**. This proves technical addition, not indefinite curatorial fitness: once the Home work index becomes visually dense (roughly beyond one comfortable viewport), review its presentation as a design decision rather than hiding works or hard-coding a new limit. The Works page and individual project generation themselves remain linear.

## Acceptance

A work is complete when its identity is source-verified, every manifest field is authored, all required images exist, automated checks pass, and its desktop/mobile page has been visually reviewed. Never compensate for an incomplete work record by hard-coding the work elsewhere.

## v08.1 visual-system guard

A new work must not introduce a smaller apparatus tier. Use the shared 12px semantic / 11px tight microtype system. Motion is optional: add it only when a still materially misrepresents the work's temporal identity. Do not add motion to documentary/index surfaces merely for consistency.
