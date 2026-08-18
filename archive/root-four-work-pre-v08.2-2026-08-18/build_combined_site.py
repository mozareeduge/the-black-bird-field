#!/usr/bin/env python3
"""Build the live site plus the /next/ preview into one dist/.

Two independent builds:
  src/build.py       -> dist/       (production, the live four-work portfolio)
  next/src/build.py  -> next/dist/  (the five-work portfolio, awaiting approval)

The preview build is copied under dist/next/ so it can be viewed at
https://theblackbirdfield.com/next/ without touching the production pages,
and is marked noindex,nofollow so it stays out of search engines while it
awaits approval. Once approved, dist/next/ becomes the production build and
this script is retired (see docs/DEPLOYMENT.md).

Run: python scripts/build_combined_site.py [--check]
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
NEXT_ROOT = ROOT / 'next'
NEXT_DIST = NEXT_ROOT / 'dist'
PREVIEW_TARGET = DIST / 'next'

NOINDEX_TAG = '  <meta name="robots" content="noindex,nofollow">\n'
HEAD_MARKER = '<meta charset="utf-8">\n'


def run_build(build_script, cwd, check):
    cmd = [sys.executable, str(build_script)]
    if check:
        cmd.append('--check')
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def inject_noindex(html_path):
    text = html_path.read_text(encoding='utf-8')
    if 'name="robots"' in text:
        return  # alias pages already carry a robots tag
    idx = text.find(HEAD_MARKER)
    if idx == -1:
        sys.exit(f'ERROR: could not find head marker in {html_path}')
    insert_at = idx + len(HEAD_MARKER)
    html_path.write_text(text[:insert_at] + NOINDEX_TAG + text[insert_at:], encoding='utf-8')


def disallow_preview_in_robots():
    robots = DIST / 'robots.txt'
    text = robots.read_text(encoding='utf-8')
    if 'Disallow: /next/' not in text:
        text = text.replace('Allow: /\n', 'Allow: /\nDisallow: /next/\n', 1)
        robots.write_text(text, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='verify checksums after each build')
    args = parser.parse_args()

    print('Building production site (four-work) -> dist/')
    run_build(ROOT / 'src' / 'build.py', ROOT, args.check)

    print('Building /next/ preview (five-work) -> next/dist/')
    run_build(NEXT_ROOT / 'src' / 'build.py', NEXT_ROOT, args.check)

    if PREVIEW_TARGET.exists():
        shutil.rmtree(PREVIEW_TARGET)
    shutil.copytree(NEXT_DIST, PREVIEW_TARGET)

    for html_path in PREVIEW_TARGET.rglob('*.html'):
        inject_noindex(html_path)

    # The preview build's own sitemap/robots.txt describe production-origin
    # URLs, which aren't meaningful under /next/, so drop them.
    for stray in ('sitemap.xml', 'robots.txt'):
        stray_path = PREVIEW_TARGET / stray
        if stray_path.exists():
            stray_path.unlink()

    disallow_preview_in_robots()

    print(f'\nCombined build complete: production at {DIST}, preview at {PREVIEW_TARGET}')


if __name__ == '__main__':
    main()
