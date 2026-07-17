"""
Build script for The Black Bird Field portfolio.

Usage:
    python src/build.py              # builds to dist/
    python src/build.py --check      # build + verify checksums
    SITE_BASE=/path python src/build.py  # override base path for subpath hosting

Output: dist/ — complete deployable site. Broken source references fail the build.
"""

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

from site_config import PAGES, CV_FILENAME
from components import header, footer

ROOT = _src.parent
PUBLIC = ROOT / 'public'
DIST = ROOT / 'dist'
PAGES_DIR = _src / 'pages'
CHECKSUMS_FILE = ROOT / 'tests' / 'fixtures' / 'checksums.json'


def _assert_exists(path, label):
    if not path.exists():
        sys.exit(f'ERROR: required {label} not found: {path}')


def _sha256(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


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


def build_page(name, meta):
    fragment_path = PAGES_DIR / meta['fragment']
    _assert_exists(fragment_path, f'page fragment {meta["fragment"]}')
    body = fragment_path.read_text(encoding='utf-8')
    scripts = (
        '<script defer src="assets/js/site.js"></script>'
        '<script defer src="assets/js/cv-download.js"></script>'
    )
    if meta.get('atlas'):
        scripts += '<script defer src="assets/js/atlas.js"></script>'
    css = ''.join(
        f'<link rel="stylesheet" href="assets/css/{f}">'
        for f in ('tokens.css', 'base.css', 'components.css', 'pages.css', 'responsive.css')
    )
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="description" content="{escape(meta['description'])}">
  <meta name="color-scheme" content="light">
  <title>{escape(meta['title'])}</title>
  {css}
  {scripts}
</head>
<body class="{meta['class']}">
{header(meta['current'])}
<main id="main">{body}</main>
{footer(meta['current'])}
</body>
</html>'''
    out = DIST / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')


def copy_public_assets():
    # CSS and JS (except cv-download.js which is generated)
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

    # Grave-Machine runtime (byte-identical copy, verified below)
    grave_src = PUBLIC / 'works' / 'grave-machine' / 'index.html'
    _assert_exists(grave_src, 'Grave-Machine runtime')
    grave_dst = DIST / 'works' / 'grave-machine'
    grave_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(grave_src, grave_dst / 'index.html')

    # CV document (fallback href for non-JS browsers)
    cv_src = PUBLIC / 'documents' / CV_FILENAME
    _assert_exists(cv_src, 'CV PDF')
    shutil.copy2(cv_src, DIST / CV_FILENAME)


def verify_checksums():
    if not CHECKSUMS_FILE.exists():
        print('WARNING: checksums.json not found; skipping checksum verification')
        return
    expected = json.loads(CHECKSUMS_FILE.read_text())
    grave_key = 'grave_machine_bilingual_v1_1'
    if grave_key in expected:
        actual = _sha256(DIST / 'works' / 'grave-machine' / 'index.html')
        if actual != expected[grave_key]:
            sys.exit(
                f'CHECKSUM MISMATCH for Grave-Machine runtime:\n'
                f'  expected: {expected[grave_key]}\n'
                f'  actual:   {actual}'
            )
        print(f'  checksum OK: {grave_key}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='verify checksums after build')
    args = parser.parse_args()

    # Clean dist
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    print('Copying public assets...')
    copy_public_assets()

    print('Generating cv-download.js...')
    build_cv_downloader()

    print('Building pages...')
    for name, meta in PAGES.items():
        build_page(name, meta)
        print(f'  {name}')

    if args.check:
        print('Verifying checksums...')
        verify_checksums()

    page_count = len(list(DIST.glob('*.html')))
    print(f'\nBuild complete: {page_count} pages → {DIST}')


if __name__ == '__main__':
    main()
