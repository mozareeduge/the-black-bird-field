# Domain Migration Decision

**Status: complete — Option A implemented and live as of 2026-07-17.**

## Final state

| URL | Repository | Purpose |
|-----|-----------|---------|
| `https://theblackbirdfield.com/` | `mozareeduge/the-black-bird-field` | Portfolio |
| `https://www.theblackbirdfield.com/` | — | Redirects to apex via Cloudflare |
| `https://poem.theblackbirdfield.com/` | `mozareeduge/the-black-bird` | The Black Bird poem |

DNS is managed via Cloudflare. HTTPS certificates are provisioned by GitHub
Pages. Both deployments serve from the `main` branch of their respective
repositories via GitHub Actions.

---

## Decision record

Option A (subdomain for The Black Bird) was chosen and implemented.

---

## Option A — Subdomain for The Black Bird

**Routing:** `www.theblackbirdfield.com` → this portfolio  
**The Black Bird poem:** `poem.theblackbirdfield.com` (or `black-bird.theblackbirdfield.com`)

### What this requires

1. Add `CNAME` to this repository pointing to `www.theblackbirdfield.com`.
2. Create a new Cloudflare CNAME DNS record: `poem` → `mozareeduge.github.io`.
3. In `mozareeduge/the-black-bird`, change `CNAME` to `poem.theblackbirdfield.com`.
4. Enable GitHub Pages custom domain in the `the-black-bird` repository settings.
5. Remove/update the custom domain in `the-black-bird` GitHub Pages settings once the subdomain propagates.
6. Update this portfolio's `site_config.py` `WORK_URLS['black-bird']` from the GitHub Pages URL to `https://poem.theblackbirdfield.com/`.

### Benefits
- The Black Bird retains a stable, meaningful URL under the same domain family.
- No content relocation; the poem repository is self-contained.
- Clean separation: portfolio at root, poem at a named subdomain.
- Citation continuity: a redirect from the old GitHub Pages URL can be added via a `_redirects` file or Cloudflare redirect rule.
- Rollback: revert `CNAME` files and DNS records; no data is moved.

### Risks
- Requires a brief DNS propagation gap (typically minutes to hours with Cloudflare proxying).
- Existing citations or links pointing to `www.theblackbirdfield.com/` (the poem's current address) must be handled by a server-side redirect. GitHub Pages does not support server-side redirects natively; a `<meta http-equiv="refresh">` page or Cloudflare redirect rule is needed.
- HTTPS is provisioned per-domain on GitHub Pages; the subdomain needs its own certificate. GitHub handles this automatically once the custom domain propagates.

---

## Option B — Portfolio-hosted Black Bird subpath

**Routing:** `www.theblackbirdfield.com/works/the-black-bird/` → vendored poem  
**The Black Bird poem:** vendored into this portfolio under `public/works/the-black-bird/` (or linked as submodule)

### What this requires

1. Copy or submodule the poem's browser-native runtime into this repository.
2. Add the poem under `public/works/the-black-bird/index.html`.
3. Update `build.py` to copy it to `dist/works/the-black-bird/`.
4. Point `www.theblackbirdfield.com` to this portfolio.
5. Retire the `mozareeduge/the-black-bird` GitHub Pages custom domain.
6. Update `site_config.py` `WORK_URLS['black-bird']` to `works/the-black-bird/`.

### Benefits
- Single-domain deployment; no subdomain DNS records needed.
- Unified HTTPS certificate.
- All works available at one canonical origin.

### Risks
- **Repository autonomy violated:** The Black Bird is an autonomous work with its own release history and repository. Vendoring it into the portfolio couples two independent development cycles.
- **Citation continuity harder:** The poem's current canonical URL (`www.theblackbirdfield.com/` or its GitHub Pages form) disappears and must be redirected.
- **Maintenance complexity:** Portfolio releases would need to track poem updates; divergence between the vendored copy and the canonical `the-black-bird` repository would be confusing.
- **REQ-PRESERVE-001 tension:** The requirement to keep autonomous work repositories canonical argues against this approach.

---

## Recommendation

**Option A — Subdomain.**

It is the simpler path with the lower risk surface. The Black Bird retains its own repository and release cadence. The domain family is coherent: `www.theblackbirdfield.com` is the field, `poem.theblackbirdfield.com` is the poem within it. Citation continuity can be achieved with a single Cloudflare redirect rule from the old root URL to the subdomain.

The implementation is already route-configurable in `src/site_config.py`: changing `WORK_URLS['black-bird']` to the approved subdomain URL takes effect on the next build.

---

## Rollback plan

At any point before propagation settles, reverting the `CNAME` files in both repositories and removing the new DNS record restores the current state within one TTL cycle. No data is moved under either option; rollback is clean.

---

## What needs approval before Claude proceeds

1. **Which option?** (Recommendation: Option A)
2. **Subdomain name for The Black Bird?** (Suggestion: `poem.theblackbirdfield.com`)
3. **Cloudflare credentials/access:** Claude does not have access to the Cloudflare dashboard. A human must add the DNS CNAME record and, optionally, the redirect rule.
4. **GitHub Pages settings:** Claude can update the `CNAME` files and push, but enabling/disabling GitHub Pages custom domains requires GitHub repository settings access.

Once approved, the implementation is: update two `CNAME` files, update one line in `site_config.py`, rebuild, and push.

---

## Current portfolio deployment before approval

The portfolio preview is available at the GitHub Pages project URL for this repository (`mozareeduge.github.io/the-black-bird-field`) once the draft PR is merged and Pages is enabled. The poem remains accessible at `www.theblackbirdfield.com` (via `mozareeduge/the-black-bird`) until explicit approval to migrate.
