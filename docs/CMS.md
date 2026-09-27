# Portfolio editor

## What is ready

`/admin/` hosts Sveltia CMS 0.221.1 (MIT licensed) from a pinned CDN URL. It edits the existing `content/site.json` and the current `content/works/*.json` records. The Asset Library points to `public/assets/`, including each work's image folder. The Python build copies the admin page into `dist/`; the existing GitHub Actions workflow still tests and deploys `dist/`.

The form uses plain text fields because the site renders authored text literally, without Markdown processing. Reading conditions, selected views, and About facts use labeled records, so the editor can show each part separately. The work slug, asset folder, site address, and generated image role conventions are read only in the form. `protected_artifacts.json` is outside the CMS.

## Publication status and use

GitHub Actions is blocked on this account (billing/spending-limit error before any step), so the site is served from the `gh-pages` branch and published **from this computer** by `scripts/publish.py`. It pulls CMS saves from `main`, converts uploaded images into the required WebP pairs, builds, runs the static tests, and only then updates `gh-pages`. A failing build publishes nothing; the live site keeps its last good version. Windows Task Scheduler runs it every 10 minutes (task `TBBF Publish`) while the computer is on; `Publish now.bat` on the Desktop runs it immediately. The last result is in `publish-status.txt`, the history in `publish.log`. The `gh-pages` worktree lives at `../the-black-bird-field-live`. Do not switch Pages to `main` / root; that contains source, not the built site. If Actions is restored later, switch Pages back to workflow deployment and disable the scheduled task.

Image uploads: upload any JPG/PNG/WebP into the work's folder in the Asset Library and type its name (without extension, e.g. `my-photo` for `My Photo.jpg`) as the view's image role. The publisher crops it to the desktop (1600×1000) and mobile (750×1334) WebP pair and normalizes a role typed as a filename or path.

Visit the editor, choose **Sign In with GitHub**, and sign in as `mozare` with the editor password. That page (`/admin/login/`) decrypts a GitHub token stored in `public/admin/login/vault.json` (AES-GCM, PBKDF2 1.2M rounds); change the token or password with `Set editor login.bat` on the Desktop or `python scripts/set_login.py --user mozare`. Alternatively choose **Sign In Using Access Token**. Use the GitHub token flow shown by Sveltia for an account with write access to `mozareeduge/the-black-bird-field`. Keep the token in the browser only; never put it in a repository file. Saves appear on the live site within about 10 minutes (or immediately after `Publish now.bat`).

For local editing, run `python src/build.py --check`, then `python -m http.server 8000 --directory dist`. Open `http://localhost:8000/admin/` in Chrome or Edge and choose **Work with Local Repository**. Select the `the-black-bird-field` repository folder. After saving locally, run the build and tests, then commit and push through Git. Local mode needs no token.

## Media and new works

The Asset Library can browse work subfolders and upload images. A work image role needs two WebP files, `<role>-desktop.webp` and `<role>-mobile.webp`, in `public/assets/<asset_slug>/`. For example, `view-midpoint-desktop.webp` and `view-midpoint-mobile.webp`. The form's `feature_image` and view `role` fields hold the role name only; uploading one image or a JPG under a different name will not satisfy the build. Keep both responsive variants and meaningful alt text. Motion files have their own size and provenance rules in `docs/MOTION_MEDIA.md`.

Creating and deleting work entries is disabled in the browser editor because a partial new entry would make the production build fail. Use `scripts/add_work.py` and `docs/ADDING_A_WORK.md` to prepare a complete new work with its paired media before adding it to `main`. Once present, its copy is editable in the CMS.

The editor commits directly to `main` after token sign-in. Save finished edits only. The local publisher rebuilds and publishes a valid change; an invalid one is reported in `publish-status.txt` and the live site keeps the last good version. The admin page is publicly reachable, while writing requires repository access. `noindex` controls search indexing, not access.
