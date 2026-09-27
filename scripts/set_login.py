#!/usr/bin/env python3
"""Store the GitHub token for the editor login, encrypted with a password.

  python scripts/set_login.py --user mozare
Prompts for the GitHub token and the password (nothing is echoed or saved in plain text).
Writes public/admin/login/vault.json (AES-256-GCM, PBKDF2-SHA256 key). Use a long password:
the encrypted file is public, so its strength is the only protection of the token.
Env vars TBBF_TOKEN / TBBF_PASSWORD may be used instead of prompts (for automation).
"""
from __future__ import annotations
import argparse, base64, getpass, json, os
from pathlib import Path
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

VAULT = Path(__file__).resolve().parents[1] / 'public/admin/login/vault.json'
ITER = 1_200_000
b64 = lambda b: base64.b64encode(b).decode()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--user', default='mozare')
    a = ap.parse_args()
    token = os.environ.get('TBBF_TOKEN') or getpass.getpass('GitHub token: ')
    pw = os.environ.get('TBBF_PASSWORD') or getpass.getpass('Password: ')
    if len(pw) < 12: raise SystemExit('password must be at least 12 characters')
    salt, iv = os.urandom(16), os.urandom(12)
    key = pbkdf2_hmac('sha256', pw.encode(), salt, ITER, 32)
    data = AESGCM(key).encrypt(iv, token.strip().encode(), None)
    vault = json.loads(VAULT.read_text(encoding='utf-8')) if VAULT.exists() else {'users': {}}
    vault['users'][a.user.strip().lower()] = {'salt': b64(salt), 'iv': b64(iv), 'iterations': ITER, 'data': b64(data)}
    VAULT.write_text(json.dumps(vault, indent=2) + '\n', encoding='utf-8')
    print(f'Login saved for "{a.user}" -> {VAULT.name}. Publish to make it live.')


if __name__ == '__main__':
    main()
