"""
Build script for The Black Bird Field portfolio.

Usage:
    python src/build.py              # builds to dist/
    python src/build.py --check      # build + verify checksums

Output: dist/ — complete deployable site. Broken source references fail the build.

All internal links and asset references use document-relative paths derived
from each page's output depth, so the same build works under both:
  https://theblackbirdfield.com/         (custom domain)
  /the-black-bird-field/                 (GitHub Pages project subpath)
"""

import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from html import escape

_src = Path(__file__).resolve().parent
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from content import WORK_ORDER, WORKS, SITE_COPY, CV_FILENAME, SITE_TITLE, SITE_ORIGIN, FORMAL_NAME
from site_config import ROUTES, ROUTE_PATHS, GRAVE_RUNTIME_OUTPUT, LEGACY_REDIRECTS, CNAME_DOMAIN
from components import header, footer
import renderers as R

ROOT = _src.parent
PUBLIC = ROOT / 'public'
DIST = ROOT / 'dist'
CHECKSUMS_FILE = ROOT / 'tests' / 'fixtures' / 'checksums.json'

CSP = (
    "default-src 'self'; base-uri 'self'; object-src 'none'; script-src 'self'; "
    "style-src 'self'; font-src 'self'; img-src 'self' data:; media-src 'self'; "
    "connect-src 'none'; frame-src 'none'; worker-src 'none'; form-action 'self'"
)

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def root_prefix(output_path):
    """Relative path prefix from this page's directory back to site root."""
    depth = len(Path(output_path).parts) - 1
    return '../' * depth


def _assert_exists(path, label):
    if not path.exists():
        sys.exit(f'ERROR: required {label} not found: {path}')


def _sha256(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Meta helpers
# ---------------------------------------------------------------------------

def og_image_url(meta):
    img = meta.get('og_image')
    if not img:
        return None
    return f'{SITE_ORIGIN}/{img}'


def meta_tags(key, meta):
    """Canonical/OG/Twitter metadata. Aliases canonicalize to their work's
    /works/ route and carry noindex,follow (D-ALIAS-RENDERING)."""
    canonical_key = meta.get('canonical_key', key)
    canonical_route = ROUTES[canonical_key]['route']
    canonical = SITE_ORIGIN + canonical_route
    robots = '\n  <meta name="robots" content="noindex,follow">' if meta.get('noindex') else ''
    img_url = og_image_url(meta)
    img_tags = ''
    if img_url:
        img_tags = (
            f'\n  <meta property="og:image" content="{escape(img_url)}">'
            f'\n  <meta name="twitter:image" content="{escape(img_url)}">'
        )
    return (
        f'  <link rel="canonical" href="{escape(canonical)}">{robots}\n'
        f'  <meta property="og:title" content="{escape(meta["title"])}">\n'
        f'  <meta property="og:description" content="{escape(meta["description"])}">\n'
        f'  <meta property="og:url" content="{escape(canonical)}">\n'
        f'  <meta property="og:type" content="website">\n'
        f'  <meta property="og:site_name" content="{escape(SITE_TITLE)}">'
        f'{img_tags}\n'
        f'  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{escape(meta["title"])}">\n'
        f'  <meta name="twitter:description" content="{escape(meta["description"])}">'
    )


def structured_data(key, meta):
    """JSON-LD CreativeWork block for canonical project pages only."""
    work_key = meta.get('work_key')
    if meta.get('renderer') != 'project' or meta.get('noindex') or not work_key:
        return ''
    work = WORKS[work_key]
    data = {
        '@context': 'https://schema.org',
        '@type': 'CreativeWork',
        'name': work['title'],
        'creator': {'@type': 'Person', 'name': FORMAL_NAME, 'alternateName': 'Mozare'},
        'dateCreated': str(work['year']),
        'inLanguage': 'en',
        'url': SITE_ORIGIN + work['canonical_route'],
        'sameAs': [work['live_url'], work['repo_url']] if work['live_url'].startswith('http') else [work['repo_url']],
    }
    return f'\n  <script type="application/ld+json">{json.dumps(data)}</script>'


# ---------------------------------------------------------------------------
# Page body dispatch
# ---------------------------------------------------------------------------

def render_body(meta, prefix):
    renderer = meta['renderer']
    if renderer == 'home':
        return R.render_home(SITE_COPY, WORKS, WORK_ORDER, prefix)
    if renderer == 'works':
        return R.render_works_index(SITE_COPY, WORKS, WORK_ORDER, prefix)
    if renderer == 'project':
        work_key = meta['work_key']
        return R.render_project(work_key, WORKS[work_key], prefix, is_alias=bool(meta.get('canonical_key')))
    if renderer == 'practice':
        return R.render_practice(SITE_COPY)
    if renderer == 'about':
        return R.render_about(SITE_COPY, prefix)
    if renderer == 'contact':
        return R.render_contact(SITE_COPY)
    sys.exit(f'ERROR: unknown renderer {renderer!r}')


def build_page(key, meta):
    output = meta['output']
    prefix = root_prefix(output)

    body = render_body(meta, prefix)

    css_files = ('tokens.css', 'base.css', 'components.css', 'pages.css', 'responsive.css')
    css = ''.join(
        f'<link rel="stylesheet" href="{prefix}assets/css/{f}">'
        for f in css_files
    )
    scripts = f'<script defer src="{prefix}assets/js/site.js"></script>'

    favicon = (
        f'<link id="dynamic-favicon" rel="icon" href="{prefix}assets/favicon/favicon-32.png" sizes="32x32" type="image/png">'
        f'<link rel="icon" href="{prefix}assets/favicon/favicon-16.png" sizes="16x16" type="image/png">'
        f'<link rel="icon" href="{prefix}assets/favicon/favicon-48.png" sizes="48x48" type="image/png">'
        f'<link rel="apple-touch-icon" href="{prefix}assets/favicon/favicon-180.png" sizes="180x180">'
        f'<script src="{prefix}assets/favicon/favicon.js" defer></script>'
    )

    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="description" content="{escape(meta['description'])}">
  <meta name="color-scheme" content="light">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{escape(meta['title'])}</title>
{meta_tags(key, meta)}
  {favicon}
  {css}
  {scripts}{structured_data(key, meta)}
</head>
<body class="{meta['class']}">
{header(meta['current'], prefix)}
<main id="main">{body}</main>
{footer(meta['current'], prefix)}
</body>
</html>'''

    out = DIST / output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')


# ---------------------------------------------------------------------------
# Legacy redirect stubs
# ---------------------------------------------------------------------------

def build_legacy_redirects():
    for old_name, route_key in LEGACY_REDIRECTS:
        meta = ROUTES[route_key]
        canonical = SITE_ORIGIN + meta['route']
        rel_target = ROUTE_PATHS[route_key]
        html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <link rel="canonical" href="{escape(canonical)}">
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0;url={rel_target}">
  <title>Redirecting — {escape(SITE_TITLE)}</title>
</head>
<body>
  <script>
    (function () {{
      var t = '{rel_target}';
      var qs = location.search || '';
      var hash = location.hash || '';
      location.replace(t + qs + hash);
    }})();
  </script>
  <p>This page has moved. <a href="{rel_target}">Continue →</a></p>
</body>
</html>'''
        out = DIST / old_name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding='utf-8')


# ---------------------------------------------------------------------------
# Sitemap and robots
# ---------------------------------------------------------------------------

def build_sitemap():
    urls = '\n'.join(
        f'  <url>\n    <loc>{SITE_ORIGIN}{meta["route"]}</loc>\n  </url>'
        for meta in ROUTES.values()
        if meta.get('sitemap', True)
    )
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
'''
    (DIST / 'sitemap.xml').write_text(xml, encoding='utf-8')


def build_robots():
    txt = f'User-agent: *\nAllow: /\nSitemap: {SITE_ORIGIN}/sitemap.xml\n'
    (DIST / 'robots.txt').write_text(txt, encoding='utf-8')


# ---------------------------------------------------------------------------
# Public asset copying
# ---------------------------------------------------------------------------

def copy_public_assets():
    assets_src = PUBLIC / 'assets'
    _assert_exists(assets_src, 'public/assets')
    assets_dst = DIST / 'assets'
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    shutil.copytree(assets_src, assets_dst)

    # Grave-Machine runtime at canonical run/ path (byte-identical)
    grave_src = PUBLIC / 'works' / 'grave-machine' / 'index.html'
    _assert_exists(grave_src, 'Grave-Machine runtime')
    grave_dst = DIST / GRAVE_RUNTIME_OUTPUT
    grave_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(grave_src, grave_dst)

    # Grave-Machine's own favicon/ folder, relative to the byte-identical
    # runtime copy above (index.html links to it with a relative path).
    grave_favicon_src = PUBLIC / 'works' / 'grave-machine' / 'favicon'
    if grave_favicon_src.exists():
        grave_favicon_dst = grave_dst.parent / 'favicon'
        if grave_favicon_dst.exists():
            shutil.rmtree(grave_favicon_dst)
        shutil.copytree(grave_favicon_src, grave_favicon_dst)

    # CV document — ordinary same-origin download, no base64 embedding.
    cv_src = PUBLIC / 'documents' / CV_FILENAME
    _assert_exists(cv_src, 'CV PDF')
    shutil.copy2(cv_src, DIST / CV_FILENAME)

    # CNAME — required so the custom domain persists across Actions-based
    # Pages deployments.
    cname_src = ROOT / 'CNAME'
    if cname_src.exists():
        shutil.copy2(cname_src, DIST / 'CNAME')


# ---------------------------------------------------------------------------
# Checksum verification
# ---------------------------------------------------------------------------

def verify_checksums():
    if not CHECKSUMS_FILE.exists():
        print('WARNING: checksums.json not found; skipping checksum verification')
        return
    expected = json.loads(CHECKSUMS_FILE.read_text())
    grave_key = 'grave_machine_bilingual_v1_1'
    if grave_key in expected:
        actual = _sha256(DIST / GRAVE_RUNTIME_OUTPUT)
        if actual != expected[grave_key]:
            sys.exit(
                f'CHECKSUM MISMATCH for Grave-Machine runtime:\n'
                f'  expected: {expected[grave_key]}\n'
                f'  actual:   {actual}'
            )
        print(f'  checksum OK: {grave_key}')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='verify checksums after build')
    args = parser.parse_args()

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    print('Copying public assets...')
    copy_public_assets()

    print('Building canonical and alias pages...')
    for key, meta in ROUTES.items():
        build_page(key, meta)
        print(f'  {meta["output"]}')

    print('Building legacy redirect stubs...')
    for old_name, _ in LEGACY_REDIRECTS:
        print(f'  {old_name}')
    build_legacy_redirects()

    print('Generating sitemap.xml and robots.txt...')
    build_sitemap()
    build_robots()

    if args.check:
        print('Verifying checksums...')
        verify_checksums()

    page_count = len(list(DIST.rglob('*.html')))
    print(f'\nBuild complete: {page_count} HTML files → {DIST}')


if __name__ == '__main__':
    main()
