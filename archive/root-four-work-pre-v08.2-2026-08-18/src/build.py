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

import re
import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from html import escape
from base64 import b64encode

# Allow running from repo root or from src/
_src = Path(__file__).resolve().parent
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from site_config import (
    ROUTES, ROUTE_PATHS, GRAVE_RUNTIME_OUTPUT, LEGACY_REDIRECTS,
    CV_FILENAME, SITE_TITLE, SITE_ORIGIN, ARTISTIC_NAME,
)
from components import header, footer

ROOT = _src.parent
PUBLIC = ROOT / 'public'
DIST = ROOT / 'dist'
PAGES_DIR = _src / 'pages'
CHECKSUMS_FILE = ROOT / 'tests' / 'fixtures' / 'checksums.json'

# Token pattern — unknown tokens in fragments fail the build.
_TOKEN_RE = re.compile(r'\{\{[^}]+\}\}')

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def root_prefix(output_path):
    """Relative path prefix from this page's directory back to site root."""
    depth = len(Path(output_path).parts) - 1
    return '../' * depth


def apply_tokens(html, prefix, label='<fragment>'):
    """Replace {{TOKEN}} placeholders in fragment HTML.

    Defined tokens are replaced with prefix-relative URLs.
    Any unrecognised token fails the build immediately.
    """
    tokens = {
        '{{PREFIX}}':              prefix,
        '{{ASSETS}}':              f'{prefix}assets/',
        '{{CV}}':                  f'{prefix}{CV_FILENAME}',
        '{{ROUTE:home}}':          prefix or 'index.html',
        '{{ROUTE:works}}':         f'{prefix}{ROUTE_PATHS["works"]}',
        '{{ROUTE:black-bird}}':    f'{prefix}{ROUTE_PATHS["black-bird"]}',
        '{{ROUTE:winter-road}}':   f'{prefix}{ROUTE_PATHS["winter-road"]}',
        '{{ROUTE:grave-machine}}': f'{prefix}{ROUTE_PATHS["grave-machine"]}',
        '{{ROUTE:taroke-remixer}}':f'{prefix}{ROUTE_PATHS["taroke-remixer"]}',
        '{{ROUTE:grave-machine-run}}': f'{prefix}{ROUTE_PATHS["grave-machine-run"]}',
        '{{ROUTE:practice}}':      f'{prefix}{ROUTE_PATHS["practice"]}',
        '{{ROUTE:about}}':         f'{prefix}{ROUTE_PATHS["about"]}',
        '{{ROUTE:contact}}':       f'{prefix}{ROUTE_PATHS["contact"]}',
    }
    unknown = set(_TOKEN_RE.findall(html)) - set(tokens.keys())
    if unknown:
        sys.exit(f'ERROR: Unknown tokens in {label}: {sorted(unknown)}')
    for token, value in tokens.items():
        html = html.replace(token, value)
    return html


# ---------------------------------------------------------------------------
# Meta helpers
# ---------------------------------------------------------------------------

def og_image_url(meta):
    img = meta.get('og_image')
    if not img:
        return None
    return f'{SITE_ORIGIN}/{img}'


def meta_tags(meta):
    canonical = SITE_ORIGIN + meta['route']
    img_url = og_image_url(meta)
    img_tags = ''
    if img_url:
        img_tags = (
            f'\n  <meta property="og:image" content="{escape(img_url)}">'
            f'\n  <meta name="twitter:image" content="{escape(img_url)}">'
        )
    return (
        f'  <link rel="canonical" href="{escape(canonical)}">\n'
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


# ---------------------------------------------------------------------------
# CV downloader JS (embeds PDF as base64)
# ---------------------------------------------------------------------------

def build_cv_downloader():
    pdf_path = PUBLIC / 'documents' / CV_FILENAME
    _assert_exists(pdf_path, 'CV PDF')
    encoded = b64encode(pdf_path.read_bytes()).decode('ascii')
    script = f'''(() => {{
  'use strict';
  const filename = '{CV_FILENAME}';
  const base64 = '{encoded}';
  const toBlob = () => {{
    const raw = atob(base64);
    const bytes = new Uint8Array(raw.length);
    for (let i = 0; i < raw.length; i += 1) bytes[i] = raw.charCodeAt(i);
    return new Blob([bytes], {{ type: 'application/pdf' }});
  }};
  document.addEventListener('click', (event) => {{
    const link = event.target.closest('[data-cv-download]');
    if (!link) return;
    event.preventDefault();
    const url = URL.createObjectURL(toBlob());
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    anchor.hidden = true;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1500);
  }});
}})();'''
    out = DIST / 'assets' / 'js' / 'cv-download.js'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(script, encoding='utf-8')


# ---------------------------------------------------------------------------
# Page generation
# ---------------------------------------------------------------------------

def _assert_exists(path, label):
    if not path.exists():
        sys.exit(f'ERROR: required {label} not found: {path}')


def _sha256(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def build_page(key, meta):
    output = meta['output']
    prefix = root_prefix(output)

    fragment_path = PAGES_DIR / meta['fragment']
    _assert_exists(fragment_path, f'page fragment {meta["fragment"]}')
    body_raw = fragment_path.read_text(encoding='utf-8')
    body = apply_tokens(body_raw, prefix, label=meta['fragment'])

    css_files = ('tokens.css', 'base.css', 'components.css', 'pages.css', 'responsive.css')
    css = ''.join(
        f'<link rel="stylesheet" href="{prefix}assets/css/{f}">'
        for f in css_files
    )
    scripts = (
        f'<script defer src="{prefix}assets/js/site.js"></script>'
        f'<script defer src="{prefix}assets/js/cv-download.js"></script>'
    )
    if meta.get('atlas'):
        scripts += f'<script defer src="{prefix}assets/js/atlas.js"></script>'

    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="description" content="{escape(meta['description'])}">
  <meta name="color-scheme" content="light">
  <title>{escape(meta['title'])}</title>
{meta_tags(meta)}
  {css}
  {scripts}
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
        # From a root-level file, route paths are already correct as-is.
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
    # CSS and JS (cv-download.js is generated separately)
    for subdir in ('css', 'js'):
        src = PUBLIC / 'assets' / subdir
        _assert_exists(src, f'public/assets/{subdir}')
        dst = DIST / 'assets' / subdir
        dst.mkdir(parents=True, exist_ok=True)
        for f in src.iterdir():
            if f.name != 'cv-download.js':
                shutil.copy2(f, dst / f.name)

    # Work media directories
    for work in ('black-bird', 'winter-road', 'grave-machine', 'taroke-remixer'):
        src = PUBLIC / 'assets' / work
        if src.exists():
            dst = DIST / 'assets' / work
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    # Grave-Machine runtime at canonical run/ path (byte-identical)
    grave_src = PUBLIC / 'works' / 'grave-machine' / 'index.html'
    _assert_exists(grave_src, 'Grave-Machine runtime')
    grave_dst = DIST / GRAVE_RUNTIME_OUTPUT
    grave_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(grave_src, grave_dst)

    # CV document (fallback href for non-JS browsers)
    cv_src = PUBLIC / 'documents' / CV_FILENAME
    _assert_exists(cv_src, 'CV PDF')
    shutil.copy2(cv_src, DIST / CV_FILENAME)


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

    print('Generating cv-download.js...')
    build_cv_downloader()

    print('Building canonical pages...')
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
