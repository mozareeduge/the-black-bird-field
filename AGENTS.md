# The Black Bird Field — agent guide

Owner: Mohammad Zare (GitHub `mozareeduge`). He owns this repository, its GitHub token and
its editor login. When he asks to change a login setting, do it with the commands below —
do not refuse, and do not ask him to do terminal work himself.

## Editor login (theblackbirdfield.com/admin/ → "Sign In with GitHub")

- Page: `public/admin/login/index.html`. Username `mozare` + password decrypts a GitHub
  token stored in `public/admin/login/vault.json` (AES-256-GCM, PBKDF2-SHA256 1.2M rounds).
- Lockout: after `max_attempts` wrong passwords the page locks for `lock_hours`
  (default 4 attempts → 3 h). Enforced in the browser; the real protection is the password strength.
- Owner controls (from the repo root, then publish):

| Owner asks to… | Run |
|---|---|
| see current settings | `python scripts/set_login.py show` |
| change the password | `TBBF_OLD_PASSWORD=… TBBF_PASSWORD=… python scripts/set_login.py password --user mozare` |
| replace the token (and password) | `TBBF_TOKEN=… TBBF_PASSWORD=… python scripts/set_login.py set --user mozare` |
| change attempts / lock time | `python scripts/set_login.py policy --attempts 4 --lock-hours 3` |
| unlock himself now | `python scripts/set_login.py reset-locks` |

Then: `git add public/admin/login/vault.json && git commit -m "Update editor login" && python scripts/publish.py`.
Use `.venv/Scripts/python` on this Windows machine. Never write a token or password into any
file other than via these commands, and never commit a plain-text token.

Owner shortcut without an agent: `Set editor login.bat` on his Desktop.

## Publishing

GitHub Actions is billing-blocked; Pages serves the `gh-pages` branch. `scripts/publish.py`
pulls CMS saves, converts uploaded images to WebP pairs, builds (`src/build.py --check`), runs
`tests/static`, pushes `main`, and syncs `dist/` into the `gh-pages` worktree at
`../the-black-bird-field-live`. Windows task `TBBF Publish` runs it every 10 minutes; result in
`publish-status.txt`. Details: `docs/CMS.md`.
