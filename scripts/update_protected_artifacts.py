#!/usr/bin/env python3
"""Recompute content/protected_artifacts.json after an intentional change
to the Grave-Machine runtime or the CV.

The build refuses (by design) when these two files don't match the hashes
recorded here — that's real protection against an accidental overwrite.
When you mean to change one of them, run this script afterward instead of
hand-editing hashes:

    python scripts/update_protected_artifacts.py
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'content' / 'protected_artifacts.json'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def main() -> None:
    auth = json.loads(MANIFEST.read_text(encoding='utf-8'))
    for key, artifact in auth['artifacts'].items():
        path = ROOT / artifact['source_path']
        if not path.is_file():
            raise SystemExit(f'Missing {key}: {path}')
        data = path.read_bytes()
        artifact['size_bytes'] = len(data)
        artifact['git_blob_sha1'] = git_blob_sha1(path)
        if 'sha256' in artifact:
            artifact['sha256'] = sha256(path)
        print(f'{key}: {len(data)} bytes, git_blob_sha1={artifact["git_blob_sha1"]}')
    MANIFEST.write_text(json.dumps(auth, indent=2) + '\n', encoding='utf-8')
    print(f'Updated {MANIFEST.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
