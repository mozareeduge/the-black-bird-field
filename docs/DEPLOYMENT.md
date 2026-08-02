# Deployment

## GitHub Pages deployment

The portfolio deploys to `https://theblackbirdfield.com/` (custom domain) via
`.github/workflows/pages.yml`. A root `CNAME` file is copied into `dist/` by
the build so the custom domain persists across Actions-based Pages
deployments; GitHub Pages and Cloudflare handle HTTPS automatically.

The site uses document-relative asset paths throughout, so it also works
correctly under the `/the-black-bird-field/` GitHub Pages project subpath —
the browser tests verify both origins against the same build artifact.

UNHAPPY Scenario is a separate, autonomous repository
(`mozareeduge/UNHAPPY-scenario`) released unchanged at its own custom
subdomain, `https://unhappy.theblackbirdfield.com/`, via GitHub Pages on
that repository. This portfolio only links to it; it does not build, host,
or modify that runtime.

## Workflows

### `.github/workflows/pages.yml` (quality + deploy)

Runs the quality job (build, static tests, browser tests) on pull requests
and pushes to `main`, and deploys to GitHub Pages only after a
quality-passing push to `main`. Pull request builds build and test but never
publish to the production Pages site.

### `.github/workflows/ci.yml` (pull request / branch quality)

Runs the same quality job on pull requests and non-`main` pushes for
inspection, without deploying. See `docs/authority/` for the exact job
definition shared between the two workflows.

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

See [DOMAIN_MIGRATION_DECISION.md](DOMAIN_MIGRATION_DECISION.md) (historical
record) for the original portfolio/poem domain split. Current live domains:

| URL | Repository |
|-----|-----------|
| `https://theblackbirdfield.com/` | `mozareeduge/the-black-bird-field` (this repository) |
| `https://poem.theblackbirdfield.com/` | `mozareeduge/the-black-bird` |
| `https://unhappy.theblackbirdfield.com/` | `mozareeduge/UNHAPPY-scenario` |

## Routes

Canonical pages are generated as directory indexes from the content/route
registry under `docs/authority/`: home, the works index, one project page
per work, practice, about, and contact — ten canonical pages in total. Each
project also has a full root alias (for example `/the-black-bird/` renders
the same project page as `/works/the-black-bird/`, with alias-appropriate
canonical/`noindex` metadata). Historical flat-path stubs
(`/about.html` etc.) redirect to the canonical directory routes with
`meta-refresh` and `location.replace()`. The Grave-Machine runtime keeps its
own unchanged route and is excluded from the sitemap.

The exact generated table is produced by `src/build.py` from the registry;
run `python src/build.py --check` to see every output path.

## Adding a new work

1. Add the work's content record (copy, metadata, image roles, actions) to
   the content authority under `docs/authority/`.
2. Add representative images to `public/assets/<work-slug>/` and register
   them in the asset manifest.
3. If the work is hosted under the portfolio (like Grave-Machine), add its
   runtime to `public/works/<work-slug>/` and register the runtime route.
4. Run `python src/build.py --check` and `python -m pytest`.

This procedure adds a work through the shared content registry and generic
project renderer — it does not create a new per-work template or a
work-specific token branch in `src/build.py`.
