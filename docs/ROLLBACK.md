# Rollback

## Portfolio (theblackbirdfield.com)

The portfolio is a static build from one commit on `main`. Rolling back
is redeploying a previous known-good commit:

1. Identify the last known-good `main` commit (before the candidate that
   needs reverting).
2. Push a revert commit or reset `main` to that commit through the normal
   PR process — do not force-push `main` directly.
3. The Pages workflow (`.github/workflows/pages.yml`) redeploys
   automatically from the new `main` head.
4. No DNS records need to change. The root aliases and canonical routes
   are build outputs, not stored data — reverting the commit removes them
   without touching any artwork repository.

`scripts/release_actions/merge_deploy_action.py rollback` is
intentionally disabled after a merge completes: use the explicit revert
path above instead of an automatic rollback of a published merge.

## UNHAPPY Scenario domain

`scripts/release_actions/unhappy_domain_action.py rollback` restores the
exact pre-action Cloudflare DNS records and GitHub Pages custom-domain
setting recorded at `artifacts/release/external-prestate/A-CONFIGURE-UNHAPPY-DOMAIN.json`
when the domain configuration was first applied. It refuses to run if
that pre-action snapshot is missing.

Manually, rollback is:

1. Remove the `unhappy` CNAME record from the `theblackbirdfield.com`
   Cloudflare zone.
2. Remove the custom domain from `mozareeduge/UNHAPPY-scenario`'s GitHub
   Pages settings.
3. Leave the repository's release files and the GitHub Pages default URL
   (`mozareeduge.github.io/UNHAPPY-scenario`) unchanged — the artwork
   itself is never modified by domain rollback.

## Pull request

Before merge, closing the PR (`gh pr close`, or
`scripts/release_actions/open_pr_action.py rollback`) is sufficient —
nothing has been published yet.

## What rollback never does

- It never edits `public/works/grave-machine/index.html` or any other
  artwork runtime.
- It never deletes or force-pushes an artwork repository's own branches.
- It never removes the `poem`/`unhappy` DNS records for domains that were
  not part of the rolled-back change.
