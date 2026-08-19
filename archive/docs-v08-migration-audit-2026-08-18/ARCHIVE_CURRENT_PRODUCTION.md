# Archive current production before v08.1 replacement

Audited production baseline:

`c6fb375877daa47bd7c9061258efa61e73196da8`

Before replacement, verify `main` still resolves to that exact SHA. If it moved, stop and audit only the bounded `baseline..HEAD` diff; do not force-apply this package.

Local archive preparation:

```bash
git fetch origin --tags --prune
git switch main
git pull --ff-only origin main
git rev-parse HEAD

git tag -a archive/portfolio-pre-v08.1-2026-08-15 \
  c6fb375877daa47bd7c9061258efa61e73196da8 \
  -m "Archive: production portfolio before v08.1 replacement (2026-08-15)"

git show --no-patch --decorate archive/portfolio-pre-v08.1-2026-08-15
```

Creating the local tag is preparation only. Pushing the tag or creating a historical GitHub Release requires separate authorization. The archive release, if created, is historical and **not latest**.
