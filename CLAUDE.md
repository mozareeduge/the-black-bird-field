# The Black Bird Field — repository authority

This file is a short pointer, not the specification. It exists so a fresh
session knows where current authority lives and what is off-limits. It does
not become a generic control plane and it is not a substitute for the active
task-specific instructions a session is given.

## Authority order

1. The explicit instructions given in the active session.
2. `docs/authority/CANONICAL_COPY.md` — sole source for visitor-facing text,
   captions, alternatives, labels, and release identifiers.
3. `docs/authority/` content and route registries consumed by `src/build.py`.
4. `docs/DEPLOYMENT.md` — current build, test, and release runbook.
5. This file, for boundaries and safety only.

Historical documents, superseded tests, old commit-message narratives, and
previous agent session summaries are **not** operative authority unless one
of the documents above explicitly says they are preserved. Do not infer an
active task or workload from Git history, stale branches, or old reports.

## Protected artifacts — never edit

- `public/works/grave-machine/index.html` — checksum-locked artwork runtime.
  Its hash is enforced by `tests/fixtures/checksums.json` and the build's
  `--check` verification. Do not modify this file for any reason; if the
  approved Grave-Machine release changes, that requires a separately
  authorized update to the checksum fixture with new capture evidence, not
  an in-place edit.
- The five works' own repositories (`the-black-bird`, `winter-road`,
  `grave-machine`, `taroke-remixer`, `UNHAPPY-scenario`) are autonomous.
  This portfolio contextualizes and links to them; it does not vendor or
  modify their runtimes.

## Build and check commands

```bash
python src/build.py           # build to dist/
python src/build.py --check   # build + Grave checksum verification
python -m pytest tests/static  -q   # static checks, no browser
python -m pytest tests/browser -q   # Playwright browser checks
```

## Branch and external-action safety

- Never push, open, edit, or merge a pull request, change GitHub Pages
  configuration, change Cloudflare DNS, or deploy/revert production without
  the explicit authorization the active session has been given for that
  specific action. Implementation and local commits are not, by themselves,
  authorization for any of the above.
- Do not delete remote branches without explicit authorization.
- Do not install `.claude/`, a relay or workload directory, a reusable
  compiler/kernel package, or any other persistent generic control plane in
  this repository.
