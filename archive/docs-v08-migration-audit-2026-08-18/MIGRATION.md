# Migration from current production

This replacement is bound to audited `main` commit `c6fb375877daa47bd7c9061258efa61e73196da8`. That baseline is the emergency rollback to the four-work portfolio. If `main` has moved, stop and re-audit instead of forcing this package onto a different state.

## Safe local application

1. Clone or update a **clean** local checkout of `mozareeduge/the-black-bird-field` at the audited commit.
2. Run `python scripts/apply_to_current_repo.py <repo-path>` from this package (or the Windows `.cmd` wrapper).
3. The script verifies the origin, exact HEAD, clean tree, Grave-Machine SHA-256, and exact current CV blob before touching replacement-owned files.
4. It replaces the authoring/build/test/docs/workflow surfaces while excluding `public/works` and `public/documents` from replacement.
5. It verifies the protected bytes again, then runs a strict build and static tests.
6. Inspect `git diff --stat`, open `dist/`, and perform the final owner visual check before any commit or remote action.

The migration script cannot commit, push, open/merge a PR, deploy, or change DNS/Pages configuration.
