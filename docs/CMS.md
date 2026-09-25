# Portfolio editor

## What is ready

`/admin/` hosts Sveltia CMS 0.221.1 (MIT licensed) from a pinned CDN URL. It edits the existing `content/site.json` and the current `content/works/*.json` records. The Asset Library points to `public/assets/`, including each work's image folder. The Python build copies the admin page into `dist/`; the existing GitHub Actions workflow still tests and deploys `dist/`.

The form uses plain text fields because the site renders authored text literally, without Markdown processing. Reading conditions, selected views, and About facts use labeled records, so the editor can show each part separately. The work slug, asset folder, site address, and generated image role conventions are read only in the form. `protected_artifacts.json` is outside the CMS.

## Finish and use

1. After the candidate is reviewed and merged, push `main`. GitHub Pages will publish `/admin/` through the existing tested workflow.
2. Visit `https://theblackbirdfield.com/admin/` and choose **Sign In Using Access Token**. Use the GitHub token flow shown by Sveltia for an account with write access to `mozareeduge/the-black-bird-field`. Keep the token in the browser only; never put it in a repository file.
3. Open **Site and pages** or **Works**, make a small copy edit, and save. Confirm the GitHub Actions build passes and the published page shows the change. This is the final account and browser check; it cannot be completed from the repository alone.

For local editing, run `python src/build.py --check`, then `python -m http.server 8000 --directory dist`. Open `http://localhost:8000/admin/` in Chrome or Edge and choose **Work with Local Repository**. Select the `the-black-bird-field` repository folder. After saving locally, run the build and tests, then commit and push through Git. Local mode needs no token.

## Media and new works

The Asset Library can browse work subfolders and upload images. A work image role needs two WebP files, `<role>-desktop.webp` and `<role>-mobile.webp`, in `public/assets/<asset_slug>/`. For example, `view-midpoint-desktop.webp` and `view-midpoint-mobile.webp`. The form's `feature_image` and view `role` fields hold the role name only; uploading one image or a JPG under a different name will not satisfy the build. Keep both responsive variants and meaningful alt text. Motion files have their own size and provenance rules in `docs/MOTION_MEDIA.md`.

Creating and deleting work entries is disabled in the browser editor because a partial new entry would make the production build fail. Use `scripts/add_work.py` and `docs/ADDING_A_WORK.md` to prepare a complete new work with its paired media before adding it to `main`. Once present, its copy is editable in the CMS.

The editor commits directly to `main` after token sign-in. Save finished edits only; an invalid content change will fail CI and Pages will retain its last successful deployment. Restore or correct the content in GitHub if that happens. The admin page is publicly reachable, while writing requires repository access. `noindex` controls search indexing, not access.
