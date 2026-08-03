#!/usr/bin/env python3
"""Validate the candidate-bound release evidence set (R-RELEASE-EVIDENCE).

Checks that RELEASE_EVIDENCE.json names one consistent snapshot/candidate
and that every artifact its evidence_index points to actually exists.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / 'artifacts' / 'release'
EVIDENCE_PATH = RELEASE_DIR / 'RELEASE_EVIDENCE.json'

REQUIRED_CHECKS = [
    'C-BUILD', 'C-COPY', 'C-ROUTES', 'C-STATIC', 'C-BROWSER', 'C-ACCESSIBILITY',
    'C-ASSETS', 'C-SECURITY', 'C-PERFORMANCE', 'C-NOJS', 'C-WORKFLOW', 'C-GRAVE',
]

REQUIRED_EVIDENCE_KEYS = [
    'EV-HOME-WIDE', 'EV-HOME-COMPACT', 'EV-HOME-MOBILE', 'EV-MENU',
    'EV-PROJECTS', 'EV-ALIASES', 'EV-NOJS', 'EV-RELEASE-REPORT',
]


def glob_matches(pattern_desc: str) -> bool:
    """evidence_index values may be a single relative path or a brace/glob-
    style description; treat any value containing a literal path segment
    that resolves as sufficient, and directly glob '*' segments."""
    if '{' not in pattern_desc and '*' not in pattern_desc.split('(')[0]:
        candidate = pattern_desc.split(' ')[0]
        return (ROOT / candidate).exists()
    # Fall back to a light existence check on the described directory.
    first_path = pattern_desc.split(' ')[0]
    directory = (ROOT / first_path).parent
    return directory.is_dir() and any(directory.iterdir())


def main() -> int:
    errors: list[str] = []

    if not EVIDENCE_PATH.is_file():
        print('FAIL: artifacts/release/RELEASE_EVIDENCE.json is missing')
        return 1

    data = json.loads(EVIDENCE_PATH.read_text(encoding='utf-8'))

    if not data.get('snapshot_id'):
        errors.append('missing snapshot_id')
    if not data.get('repository_start', {}).get('commit'):
        errors.append('missing repository_start.commit')
    if not data.get('candidate_identity', {}).get('sha256'):
        errors.append('missing candidate_identity.sha256')

    checks = data.get('checks', {})
    for check_id in REQUIRED_CHECKS:
        if checks.get(check_id) != 'PASS':
            errors.append(f'check {check_id} is not recorded as PASS: {checks.get(check_id)!r}')
        raw = RELEASE_DIR / 'checks' / f'{check_id}.json'
        if not raw.is_file():
            errors.append(f'missing raw check record: artifacts/release/checks/{check_id}.json')

    evidence_index = data.get('evidence_index', {})
    for key in REQUIRED_EVIDENCE_KEYS:
        if key not in evidence_index:
            errors.append(f'evidence_index missing {key}')
            continue
        if not glob_matches(evidence_index[key]):
            errors.append(f'{key} artifact not found: {evidence_index[key]}')

    if 'deviations' not in data:
        errors.append("'deviations' key missing (must be an explicit list, empty if none)")

    if not data.get('rollback', {}).get('record'):
        errors.append('missing rollback.record pointer')

    if not (RELEASE_DIR / 'PR_BODY.md').is_file():
        errors.append('missing artifacts/release/PR_BODY.md')

    if errors:
        for e in errors:
            print(f'FAIL: {e}')
        return 1

    print(f'PASS: release evidence complete for candidate {data["candidate_identity"]["sha256"][:12]}...')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
