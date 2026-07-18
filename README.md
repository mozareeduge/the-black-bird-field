# The Black Bird Field

Portfolio site for four browser-native works by Mozare (Mohammad Zare).

**Works:** The Black Bird · Winter Road · Grave-Machine · TAROKE RIMIXER

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

Playwright uses the pre-installed Chromium binary at `/opt/pw-browsers/chromium`.

## Structure

```
src/          source (build script, config, page fragments)
public/       immutable inputs (CSS, JS, images, documents, Grave runtime)
dist/         generated output — not committed
tests/        static + browser + fixtures
scripts/      capture and validation utilities
.github/      CI workflows
docs/         domain migration decision and deployment notes
```

## Domain

| URL | Purpose |
|-----|---------|
| `https://theblackbirdfield.com/` | Portfolio (this repository) |
| `https://www.theblackbirdfield.com/` | Redirects to apex |
| `https://poem.theblackbirdfield.com/` | The Black Bird poem (`mozareeduge/the-black-bird`) |

The portfolio occupies the apex domain. The Black Bird poem lives on the
`poem` subdomain with its own GitHub Pages custom domain. See
[docs/DOMAIN_MIGRATION_DECISION.md](docs/DOMAIN_MIGRATION_DECISION.md) for
the full record.

## Routes

The build produces directory-style canonical routes (`/works/the-black-bird/`,
`/practice/`, etc.) and eight legacy redirect stubs at the old flat paths
(`/black-bird.html` → `/works/the-black-bird/`, etc.).