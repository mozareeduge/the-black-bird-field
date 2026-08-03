#!/usr/bin/env python3
"""Verify the live production release (R-WORKFLOW-RELEASE, Section 15).

Run only after a merge has deployed (called automatically by
scripts/release_actions/merge_deploy_action.py in readback mode, or
manually: python scripts/verify_live_release.py).

Requires live network access to the production domain, which this
implementation environment's network policy does not grant — this script
is installed and ready for use in an environment (e.g. the Actions
runner, or a session with broader network access) that can reach
https://theblackbirdfield.com/.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://theblackbirdfield.com'

CANONICAL_PATHS = [
    '/', '/works/', '/works/the-black-bird/', '/works/winter-road/',
    '/works/unhappy-scenario/', '/works/grave-machine/', '/works/taroke-remixer/',
    '/practice/', '/about/', '/contact/',
]
ALIAS_PATHS = ['/the-black-bird/', '/winter-road/', '/unhappy-scenario/', '/grave-machine/', '/taroke-remixer/']


def fetch(path: str, timeout: int = 20):
    req = urllib.request.Request(ORIGIN + path, method='GET')
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', 'ignore'), dict(r.headers)


def main() -> int:
    errors: list[str] = []
    checked = []

    for path in CANONICAL_PATHS + ALIAS_PATHS:
        try:
            status, body, _ = fetch(path)
            checked.append({'path': path, 'status': status})
            if status != 200:
                errors.append(f'{path}: HTTP {status}')
            elif '<h1' not in body:
                errors.append(f'{path}: no <h1> found')
        except Exception as e:  # noqa: BLE001
            errors.append(f'{path}: {e}')

    try:
        status, sitemap, _ = fetch('/sitemap.xml')
        if status != 200 or '<urlset' not in sitemap:
            errors.append('sitemap.xml not served correctly')
    except Exception as e:  # noqa: BLE001
        errors.append(f'sitemap.xml: {e}')

    try:
        status, robots, _ = fetch('/robots.txt')
        if status != 200 or 'Sitemap:' not in robots:
            errors.append('robots.txt not served correctly')
    except Exception as e:  # noqa: BLE001
        errors.append(f'robots.txt: {e}')

    try:
        req = urllib.request.Request(ORIGIN + '/works/grave-machine/run/', method='GET')
        with urllib.request.urlopen(req, timeout=20) as r:
            grave_body = r.read()
        import hashlib
        expected = json.loads((ROOT / 'tests' / 'fixtures' / 'checksums.json').read_text())[
            'grave_machine_bilingual_v1_1'
        ]
        actual = hashlib.sha256(grave_body).hexdigest()
        if actual != expected:
            errors.append(f'Grave-Machine live checksum mismatch: {actual} != {expected}')
    except Exception as e:  # noqa: BLE001
        errors.append(f'grave-machine/run: {e}')

    result = {'origin': ORIGIN, 'checked': checked, 'errors': errors}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
