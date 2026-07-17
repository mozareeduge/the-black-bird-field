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

See [ARCHITECTURE.md](ARCHITECTURE.md) for full decisions.

## Domain

`www.theblackbirdfield.com` is currently owned by `mozareeduge/the-black-bird`.
See [docs/DOMAIN_MIGRATION_DECISION.md](docs/DOMAIN_MIGRATION_DECISION.md) for
the migration comparison and recommendation awaiting approval.