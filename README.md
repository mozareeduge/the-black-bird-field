# The Black Bird Field

Portfolio site for five browser-native works by Mozare (Mohammad Zare).

**Works, in order:** The Black Bird — *Traverse* · Winter Road — *Approach* ·
UNHAPPY Scenario — *Attempt* · Grave-Machine — *Remain* · TAROKE RIMIXER — *Compose*

## Authority

This repository's current authorities live at:

- `docs/authority/CANONICAL_COPY.md` — sole source for visitor-facing text.
- `docs/authority/` — content, route, and design-token registries consumed
  by `src/build.py`.
- `docs/DEPLOYMENT.md` — build, test, and release runbook.
- `CLAUDE.md` — repository boundaries and safety rules for agent sessions.

Historical documents (including `docs/DOMAIN_MIGRATION_DECISION.md`) record
completed decisions and are not active instructions.

## Local development

```bash
python src/build.py          # builds to dist/
python src/build.py --check  # build + checksum verification
python -m http.server 8080 --directory dist   # local preview
```

## Testing

```bash
python -m pytest tests/static/   # static checks (no browser)
python -m pytest tests/browser/  # Playwright browser tests
```

Playwright uses a pre-installed Chromium binary when `/opt/pw-browsers/chromium`
is present (the Claude Code remote execution environment); otherwise it falls
back to Playwright's own managed browser install.

## Structure

```
src/          source (build script, config, page fragments)
public/       immutable inputs (CSS, JS, images, documents, Grave runtime)
dist/         generated output — not committed
tests/        static + browser + fixtures
scripts/      capture and validation utilities
.github/      CI workflows
docs/         current authorities, runbook, and historical decision records
artifacts/    generated evidence (baseline, capture, release) — not source
```

## Repository map

| Work or layer | Repository | Status |
|---|---|---|
| Portfolio | `mozareeduge/the-black-bird-field` | Canonical host and documentation layer |
| The Black Bird | `mozareeduge/the-black-bird` | Canonical public source archive |
| The Black Bird development lab | `mozareeduge/black-bird-lab` | Development and experiment history |
| Winter Road | `mozareeduge/winter-road` | Canonical public source archive |
| UNHAPPY Scenario | `mozareeduge/UNHAPPY-scenario` | Canonical public source archive; standalone HTTPS release |
| Grave-Machine | `mozareeduge/grave-machine` | Canonical public source archive; live runtime remains in the portfolio |
| TAROKE RIMIXER | `mozareeduge/taroke-remixer` | Canonical public source archive |

## Domain

| URL | Purpose |
|-----|---------|
| `https://theblackbirdfield.com/` | Portfolio (this repository) |
| `https://www.theblackbirdfield.com/` | Redirects to apex |
| `https://poem.theblackbirdfield.com/` | The Black Bird poem (`mozareeduge/the-black-bird`) |
| `https://unhappy.theblackbirdfield.com/` | UNHAPPY Scenario (`mozareeduge/UNHAPPY-scenario`) |

See [docs/DOMAIN_MIGRATION_DECISION.md](docs/DOMAIN_MIGRATION_DECISION.md)
(historical record) for the portfolio/poem split, and
[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the current domain and release
runbook, including the UNHAPPY Scenario subdomain.

## Routes

The build produces directory-style canonical routes (`/works/the-black-bird/`,
`/practice/`, etc.), five full root aliases (`/the-black-bird/`, etc.), and
compatibility stubs at the historical flat paths. See
[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the complete route table.
