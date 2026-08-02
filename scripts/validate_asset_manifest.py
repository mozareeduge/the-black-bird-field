#!/usr/bin/env python3
"""Validate docs/ASSET_MANIFEST.json against the files it describes.

Checks R-ASSET-AUTHENTICITY: every manifest path exists, hashes and
dimensions match, every work has all required asset roles, and no image
file is reused beyond the repetition budget.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / 'docs' / 'ASSET_MANIFEST.json'

REQUIRED_ROLES = {
    'project_hero', 'home_feature', 'works_index_thumbnail',
    'project_selected_view_01', 'project_selected_view_02',
    'project_selected_view_03', 'project_selected_view_04',
}
MAX_GLOBAL_USES = 3


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def png_dims(path: Path) -> tuple[int, int]:
    data = path.open('rb').read(33)
    w, h = struct.unpack('>II', data[16:24])
    return w, h


def main() -> int:
    if not MANIFEST_PATH.is_file():
        print('FAIL: docs/ASSET_MANIFEST.json is missing')
        return 1

    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    assets = manifest.get('assets', [])
    errors: list[str] = []

    roles_by_work: dict[str, set[str]] = {}
    surface_uses: dict[str, int] = {}

    for entry in assets:
        path = ROOT / entry['path']
        work = entry['work']
        roles_by_work.setdefault(work, set()).add(entry['role'])

        if not path.is_file():
            errors.append(f"missing file: {entry['path']}")
            continue

        actual_sha = sha256(path)
        if actual_sha != entry['sha256']:
            errors.append(f"sha256 mismatch for {entry['path']}: expected {entry['sha256']}, got {actual_sha}")

        actual_w, actual_h = png_dims(path)
        expected = entry['output_dimensions']
        if (actual_w, actual_h) != (expected['width'], expected['height']):
            errors.append(
                f"dimension mismatch for {entry['path']}: expected {expected}, got {{'width': {actual_w}, 'height': {actual_h}}}"
            )

        for surface in entry.get('portfolio_surfaces', []):
            key = f"{work}:{surface}"
            surface_uses[key] = surface_uses.get(key, 0) + 1

        surface_uses.setdefault(f'__file__{entry["path"]}', 0)
        surface_uses[f'__file__{entry["path"]}'] += len(entry.get('portfolio_surfaces', [])) or 1

    for work, roles in roles_by_work.items():
        missing = REQUIRED_ROLES - roles
        if missing:
            errors.append(f'{work}: missing asset roles {sorted(missing)}')

    for key, count in surface_uses.items():
        if key.startswith('__file__') and count > MAX_GLOBAL_USES:
            errors.append(f'{key[8:]} used on {count} surfaces, exceeds budget of {MAX_GLOBAL_USES}')

    if errors:
        for e in errors:
            print(f'FAIL: {e}')
        return 1

    print(f'PASS: {len(assets)} manifest entries validated across {len(roles_by_work)} works')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
