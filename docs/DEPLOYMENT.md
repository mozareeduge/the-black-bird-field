# Deployment

## GitHub Pages deployment

The portfolio deploys to `https://mozareeduge.github.io/the-black-bird-field/` via `.github/workflows/pages.yml`.

**To enable Pages after the PR is merged:**
1. Go to Settings → Pages in the `mozareeduge/the-black-bird-field` repository.
2. Set Source to **GitHub Actions**.
3. The next push to `main` triggers the Pages workflow and publishes `dist/`.

The site uses document-relative asset paths throughout, so it works correctly under the `/the-black-bird-field/` project subpath without any base-path configuration.

## Workflows

### `.github/workflows/pages.yml` (deployment)

Runs on pushes and pull requests targeting `main`:

1. Builds the site: `python src/build.py --check`
2. Runs static tests: `python -m pytest tests/static/ -v`
3. Runs browser tests at both `/` and `/the-black-bird-field/`: `python -m pytest tests/browser/ -v`
4. Uploads `dist/` via `actions/upload-pages-artifact`
5. **Deploys to GitHub Pages** only when `github.event_name == 'push'` and `github.ref == 'refs/heads/main'` — pull request builds build and test but never publish to the production Pages site.

### `.github/workflows/ci.yml` (all-branch CI)

Runs on every push and pull request to any branch. Builds, tests, and uploads `dist/` as a downloadable artifact for inspection. Does not deploy to Pages.

## Build locally

```bash
python src/build.py          # outputs to dist/
python src/build.py --check  # outputs to dist/ and verifies checksums
python -m http.server 8080 --directory dist
```

Visit `http://localhost:8080/` to see the site at root, or
`http://localhost:8080/the-black-bird-field/` to test under the project subpath
(the browser test server handles both).

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
