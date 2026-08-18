# Deployment

## GitHub Pages deployment

The portfolio deploys to `https://theblackbirdfield.com/` (custom domain) via
`.github/workflows/pages.yml`. The CNAME file in this repository points to
`theblackbirdfield.com`; GitHub Pages and Cloudflare handle HTTPS automatically.

The site uses document-relative asset paths throughout, so it also works
correctly under the `/the-black-bird-field/` GitHub Pages project subpath — the
browser tests verify both origins against the same build artifact.

## Workflows

### `.github/workflows/pages.yml` (deployment)

Runs on pushes and pull requests targeting `main`:

1. Builds the site and runs its static + browser tests
   (`src/build.py --check`, `tests/static/`, `tests/browser/`)
2. Uploads `dist/` via `actions/upload-pages-artifact`
3. **Deploys to GitHub Pages** only when `github.event_name == 'push'` and `github.ref == 'refs/heads/main'` — pull request builds build and test but never publish to the production Pages site.

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

See [DOMAIN_MIGRATION_DECISION.md](DOMAIN_MIGRATION_DECISION.md) for the full
migration record. The migration is complete: `theblackbirdfield.com` now serves
the portfolio and `poem.theblackbirdfield.com` serves The Black Bird poem.

## Routes

Canonical pages are generated as directory indexes:

| Route | Output |
|-------|--------|
| `/` | `index.html` |
| `/works/` | `works/index.html` |
| `/works/the-black-bird/` | `works/the-black-bird/index.html` |
| `/works/winter-road/` | `works/winter-road/index.html` |
| `/works/unhappy-scenario/` | `works/unhappy-scenario/index.html` |
| `/works/grave-machine/` | `works/grave-machine/index.html` |
| `/works/taroke-remixer/` | `works/taroke-remixer/index.html` |
| `/works/grave-machine/run/` | `works/grave-machine/run/index.html` (Grave runtime, noindex) |
| `/practice/` | `practice/index.html` |
| `/about/` | `about/index.html` |
| `/contact/` | `contact/index.html` |

Eight legacy redirect stubs at the old flat paths (`/about.html` etc.) redirect
to the canonical directory routes with `meta-refresh` and `location.replace()`.

## Adding a new work

See [ADDING_A_WORK.md](ADDING_A_WORK.md).
