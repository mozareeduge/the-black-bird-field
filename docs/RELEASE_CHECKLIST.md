# Release checklist

Local implementation and commits are not, by themselves, authorization to
push, open a pull request, change domain configuration, merge, or deploy
(see `CLAUDE.md` § Branch and external-action safety). Each stage below
requires its own explicit authorization before the corresponding
`scripts/release_actions/*.py` script runs in `apply` mode.

## 1. Implementation complete

- [ ] `python src/build.py --check` passes (build + Grave checksum).
- [ ] `python -m pytest tests/static/ tests/browser/ -v` passes in full.
- [ ] `python scripts/validate_authority_environment.py` passes.
- [ ] `python scripts/validate_asset_manifest.py` passes.
- [ ] `python scripts/validate_test_authority.py` passes.
- [ ] `python scripts/validate_workflows.py` passes.
- [ ] `artifacts/release/` evidence set is complete and validated
      (`python scripts/validate_release_evidence.py`).
- [ ] Working tree is clean and every change is committed on the feature branch.

## 2. Candidate-bound evidence review

- [ ] `artifacts/release/RELEASE_EVIDENCE.json` names the exact snapshot,
      repository start, and candidate identity used throughout.
- [ ] Desktop, compact, mobile, menu, project, and alias screenshots are
      present for every required viewport and state.
- [ ] Deviations list is explicit (empty list if none) — nothing is
      silently different from the sealed specification.

## 3. External authorization gate — pull request

- [ ] User explicitly authorizes opening the PR, naming repository,
      feature branch, base branch, and PR title.
- [ ] `python scripts/release_actions/open_pr_action.py apply` (pushes
      the branch, opens the PR from `artifacts/release/PR_BODY.md`).
- [ ] CI is green on the PR.

## 4. External authorization gate — UNHAPPY domain (independent of merge)

- [ ] User explicitly authorizes domain configuration, naming the
      UNHAPPY repository, domain, Cloudflare zone, record target, and
      proxy state.
- [ ] `python scripts/release_actions/unhappy_domain_action.py apply`.
- [ ] `unhappy_domain_action.py readback` confirms DNS, HTTPS, the
      unchanged source checksum, and no conflicting canonical metadata.

## 5. Design/visual acceptance

- [ ] The complete evidence set is presented for human review
      (`C-VISUAL-REVIEW`). Automated checks passing is not artistic
      acceptance — curatorial coherence, visual rhythm, image selection,
      and conceptual restraint are judged by the repository owner.
- [ ] `artifacts/release/DESIGN_ACCEPTANCE.json` is recorded with
      `status: ACCEPTED` and `accepted_by: USER`.

## 6. External authorization gate — merge and deploy

- [ ] User explicitly authorizes merge and deployment, naming the
      repository, pull request, merge method, deploy origin, and the
      exact reviewed candidate identity (must equal the accepted
      candidate from step 5).
- [ ] `python scripts/release_actions/merge_deploy_action.py apply`
      (squash-merges and deletes the branch).
- [ ] `merge_deploy_action.py readback` confirms the Pages workflow run
      for the merge commit succeeded and runs
      `scripts/verify_live_release.py` against production.

## 7. Production verification

- [ ] Canonical and alias URLs resolve at the live domain.
- [ ] Sitemap and robots.txt are correct in production.
- [ ] All portfolio assets load with no failed requests.
- [ ] Zero third-party runtime requests.
- [ ] Grave-Machine runtime checksum unchanged in production.

See `docs/ROLLBACK.md` if any stage needs to be reversed.
