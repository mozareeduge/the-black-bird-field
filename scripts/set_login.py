#!/usr/bin/env python3
"""Owner controls for the editor login (theblackbirdfield.com/admin/).

The GitHub token is stored encrypted in public/admin/login/vault.json; the login
policy (wrong-attempt limit, lock duration) sits next to it in plain text.
After any change, publish:  python scripts/publish.py

Commands (run from the repository root):
  python scripts/set_login.py show
  python scripts/set_login.py set --user mozare         new token + password
  python scripts/set_login.py password --user mozare    change password, keep token
  python scripts/set_login.py policy --attempts 4 --lock-hours 3
  python scripts/set_login.py reset-locks               lift every current lock

Secrets are prompted without echo. For non-interactive agents use environment
variables instead: TBBF_TOKEN, TBBF_PASSWORD, TBBF_OLD_PASSWORD.
"""
from __future__ import annotations
import argparse, base64, getpass, json, os, secrets
from pathlib import Path
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

VAULT = Path(__file__).resolve().parents[1] / 'public/admin/login/vault.json'
ITER = 1_200_000
DEFAULT_POLICY = {'max_attempts': 4, 'lock_hours': 3}
enc = lambda b: base64.b64encode(b).decode()
dec = base64.b64decode


def load() -> dict:
    v = json.loads(VAULT.read_text(encoding='utf-8')) if VAULT.exists() else {}
    v.setdefault('users', {})
    pol = v.setdefault('policy', {})
    for k, d in DEFAULT_POLICY.items(): pol.setdefault(k, d)
    pol.setdefault('reset_id', secrets.token_hex(4))
    return v


def save(v: dict):
    VAULT.parent.mkdir(parents=True, exist_ok=True)
    VAULT.write_text(json.dumps(v, indent=2) + '\n', encoding='utf-8')


def secret(env: str, prompt: str) -> str:
    return os.environ.get(env) or getpass.getpass(prompt)


def seal(token: str, pw: str) -> dict:
    if len(pw) < 8: raise SystemExit('password must be at least 8 characters')
    salt, iv = os.urandom(16), os.urandom(12)
    key = pbkdf2_hmac('sha256', pw.encode(), salt, ITER, 32)
    return {'salt': enc(salt), 'iv': enc(iv), 'iterations': ITER,
            'data': enc(AESGCM(key).encrypt(iv, token.strip().encode(), None))}


def open_(rec: dict, pw: str) -> str:
    key = pbkdf2_hmac('sha256', pw.encode(), dec(rec['salt']), rec['iterations'], 32)
    try: return AESGCM(key).decrypt(dec(rec['iv']), dec(rec['data']), None).decode()
    except Exception: raise SystemExit('old password is wrong')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd')
    sub.add_parser('show')
    for name in ('set', 'password'):
        s = sub.add_parser(name); s.add_argument('--user', default='mozare')
    p = sub.add_parser('policy'); p.add_argument('--attempts', type=int); p.add_argument('--lock-hours', type=float)
    sub.add_parser('reset-locks')
    a = ap.parse_args(); cmd = a.cmd or 'set'
    v = load()
    if cmd == 'show':
        print('users:', ', '.join(v['users']) or '(none)'); print('policy:', v['policy']); return
    if cmd == 'set':
        user = getattr(a, 'user', 'mozare').strip().lower()
        v['users'][user] = seal(secret('TBBF_TOKEN', 'GitHub token: '), secret('TBBF_PASSWORD', 'New password: '))
        msg = f'token + password set for "{user}"'
    elif cmd == 'password':
        user = a.user.strip().lower()
        if user not in v['users']: raise SystemExit(f'no login for "{user}"; use: set --user {user}')
        token = open_(v['users'][user], secret('TBBF_OLD_PASSWORD', 'Current password: '))
        v['users'][user] = seal(token, secret('TBBF_PASSWORD', 'New password: '))
        msg = f'password changed for "{user}"'
    elif cmd == 'policy':
        if a.attempts is not None:
            if a.attempts < 1: raise SystemExit('attempts must be >= 1')
            v['policy']['max_attempts'] = a.attempts
        if a.lock_hours is not None:
            if a.lock_hours < 0: raise SystemExit('lock hours must be >= 0')
            v['policy']['lock_hours'] = a.lock_hours
        msg = f"policy: {v['policy']['max_attempts']} wrong attempts -> {v['policy']['lock_hours']} h lock"
    elif cmd == 'reset-locks':
        v['policy']['reset_id'] = secrets.token_hex(4); msg = 'all current locks lifted'
    save(v)
    print(msg + '. Publish to make it live: python scripts/publish.py')


if __name__ == '__main__':
    main()
