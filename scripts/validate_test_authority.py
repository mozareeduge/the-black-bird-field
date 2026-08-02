#!/usr/bin/env python3
"""Validate the test suite against the sealed test-authority registry.

Checks R-TEST-MIGRATION: no skip/xfail/weakened coverage, superseded
files are actually gone, and every current-acceptance test file exists.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_MARKERS = re.compile(r'@pytest\.mark\.(skip|xfail)\b|pytest\.skip\(|test\.skip\(')

REQUIRED_CURRENT_TESTS = [
    'tests/static/test_build.py',
    'tests/static/test_copy_contract.py',
    'tests/static/test_routes.py',
    'tests/static/test_assets.py',
    'tests/static/test_security.py',
    'tests/browser/test_pages.py',
    'tests/browser/test_accessibility.py',
    'tests/browser/test_responsive_matrix.py',
    'tests/browser/test_no_javascript.py',
    'tests/browser/test_performance_budget.py',
    'tests/fixtures/checksums.json',
]

FORBIDDEN_PATHS = [
    'public/assets/js/atlas.js',
    'dist/assets/js/cv-download.js',
    '.claude',
    'workload',
]


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_CURRENT_TESTS:
        if not (ROOT / rel).is_file():
            errors.append(f'missing required current-acceptance file: {rel}')

    for rel in FORBIDDEN_PATHS:
        if (ROOT / rel).exists():
            errors.append(f'superseded path still present: {rel}')

    for test_file in (ROOT / 'tests').rglob('test_*.py'):
        text = test_file.read_text(encoding='utf-8')
        m = FORBIDDEN_MARKERS.search(text)
        if m:
            rel = test_file.relative_to(ROOT)
            errors.append(f'{rel}: forbidden skip/xfail marker ({m.group(0)!r})')

    if errors:
        for e in errors:
            print(f'FAIL: {e}')
        return 1

    print(f'PASS: {len(REQUIRED_CURRENT_TESTS)} current-acceptance files present, '
          f'{len(FORBIDDEN_PATHS)} superseded paths absent, no skip/xfail markers')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
