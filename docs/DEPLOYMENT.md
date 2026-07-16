# Deployment

## Preview deployment (current)

The portfolio is deployed to GitHub Pages from the `dist/` build output. GitHub Pages is configured to serve the `dist/` branch or directory once the PR is merged.

**Preview URL:** `https://mozareeduge.github.io/the-black-bird-field/`

To enable GitHub Pages for this repository:
1. Go to Settings → Pages in the `mozareeduge/the-black-bird-field` repository.
2. Set Source to "GitHub Actions" (recommended) or set Branch to `main`, folder to `/dist`.
3. The CI workflow uploads `dist/` as an artifact; a separate deploy step can publish it.

## Build locally

```bash
python src/build.py          # outputs to dist/
python src/build.py --check  # outputs to dist/ and verifies checksums
python -m http.server 8080 --directory dist
```

## GitHub Actions CI

`.github/workflows/ci.yml` runs on every push and PR:
1. Builds the site with `python src/build.py --check`
2. Runs static tests: `python -m pytest tests/static/ -v`
3. Runs browser tests: `python -m pytest tests/browser/ -v`
4. Uploads `dist/` as a build artifact

## Domain

See [DOMAIN_MIGRATION_DECISION.md](DOMAIN_MIGRATION_DECISION.md) for the pending domain migration.

**Do not** add a CNAME file to this repository, remove the `CNAME` from `mozareeduge/the-black-bird`, or edit Cloudflare DNS until the domain decision is explicitly approved.

## Adding a new work

1. Add the work URL to `WORK_URLS` in `src/site_config.py`.
2. Add a page entry to `PAGES` in `src/site_config.py`.
3. Create `src/pages/<work-slug>.html` for the project page content.
4. Add representative images to `public/assets/<work-slug>/`.
5. If the work is hosted under the portfolio (like Grave-Machine), add its runtime to `public/works/<work-slug>/`.
6. Run `python src/build.py` and `python -m pytest`.
