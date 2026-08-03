#!/usr/bin/env python3
"""Validate the GitHub Actions workflow topology (R-WORKFLOW-RELEASE, R-UNHAPPY-DOMAIN).

Checks Section 12.1: one quality job validates PRs and every branch push,
deployment happens only from a quality-passing push to main using the
current Pages action sequence, and CI is not duplicated across two
separate workflow files.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = ROOT / '.github' / 'workflows'

REQUIRED_DEPLOY_ACTIONS = (
    'actions/checkout@',
    'actions/setup-python@',
    'actions/configure-pages@',
    'actions/upload-pages-artifact@',
    'actions/deploy-pages@',
)


def main() -> int:
    errors: list[str] = []

    workflow_files = sorted(WORKFLOWS_DIR.glob('*.yml'))
    if len(workflow_files) != 1:
        errors.append(
            f'expected exactly one workflow file (quality+deploy consolidated), found {len(workflow_files)}: '
            + ', '.join(f.name for f in workflow_files)
        )

    pages_yml = WORKFLOWS_DIR / 'pages.yml'
    if not pages_yml.is_file():
        errors.append('missing .github/workflows/pages.yml')
        for e in errors:
            print(f'FAIL: {e}')
        return 1

    text = pages_yml.read_text(encoding='utf-8')

    for action in REQUIRED_DEPLOY_ACTIONS:
        if action not in text:
            errors.append(f'pages.yml missing required action: {action}')

    if 'pull_request' not in text:
        errors.append('pages.yml does not validate pull requests')

    deploy_idx = text.find('deploy:')
    if deploy_idx == -1:
        errors.append('pages.yml has no deploy job')
    else:
        deploy_block = text[deploy_idx:]
        if "github.event_name == 'push'" not in deploy_block or "github.ref == 'refs/heads/main'" not in deploy_block:
            errors.append('deploy job is not gated to push-to-main only')
        if 'needs: quality' not in deploy_block:
            errors.append('deploy job does not declare needs: quality')

    if 'pages: write' not in text or 'id-token: write' not in text:
        errors.append('deploy job missing pages:write / id-token:write permissions')

    requirements = ROOT / 'requirements-test.txt'
    if not requirements.is_file():
        errors.append('requirements-test.txt missing (test dependencies must be pinned)')
    elif 'pip install -r requirements-test.txt' not in text:
        errors.append('pages.yml does not install pinned requirements-test.txt')

    if errors:
        for e in errors:
            print(f'FAIL: {e}')
        return 1

    print('PASS: single consolidated quality+deploy workflow with pinned dependencies')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
