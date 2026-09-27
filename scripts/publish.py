#!/usr/bin/env python3
"""Publish the site without GitHub Actions (no-payment path).

One run does everything, and never publishes a broken build:
  1. commit any local content edits (content/, public/assets/)
  2. pull CMS saves from origin/main
  3. convert any uploaded image (jpg/png/webp/...) into the required
     <role>-desktop.webp + <role>-mobile.webp pair, and tidy role fields
  4. build + static tests
  5. push main, then copy dist/ onto the gh-pages worktree and push it

Usage:  python scripts/publish.py            (publish if anything changed)
        python scripts/publish.py --dry-run  (build/test only, push nothing)
Status of the last run: publish-status.txt at the repository root.
"""
from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys, time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT.parent / 'the-black-bird-field-live'   # gh-pages worktree
ASSETS = ROOT / 'public' / 'assets'
WORKS = ROOT / 'content' / 'works'
STATUS = ROOT / 'publish-status.txt'
LOCK = ROOT / '.publish.lock'
PY = sys.executable
IMAGE_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.bmp', '.heic'}
SIZES = {'desktop': (1600, 1000), 'mobile': (750, 1334)}


def log(msg: str):
    line = f'[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}'
    print(line, flush=True)
    with open(ROOT / 'publish.log', 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def run(*cmd, cwd=ROOT, check=True) -> str:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(cmd)} failed:\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
    return r.stdout.strip()


def git(*a, cwd=ROOT, check=True) -> str:
    return run('git', *a, cwd=cwd, check=check)


def slug_role(name: str) -> str:
    stem = Path(name.split('?')[0]).stem.lower()
    stem = re.sub(r'-(desktop|mobile)$', '', stem)
    return re.sub(r'[^a-z0-9]+', '-', stem).strip('-') or 'image'


def cover(img, size):
    from PIL import ImageOps
    return ImageOps.fit(img, size, method=3, centering=(0.5, 0.5))


def convert_uploads() -> list[str]:
    """Turn any uploaded image into a desktop/mobile WebP pair named by role."""
    from PIL import Image, ImageOps
    done = []
    for f in sorted(ASSETS.glob('*/*')):
        if not f.is_file() or f.suffix.lower() not in IMAGE_EXT:
            continue
        if re.search(r'-(desktop|mobile)\.webp$', f.name):
            continue
        role = slug_role(f.name)
        try:
            with Image.open(f) as im:
                im = ImageOps.exif_transpose(im).convert('RGB')
                for size, dims in SIZES.items():
                    cover(im, dims).save(f.parent / f'{role}-{size}.webp', 'WEBP', quality=84, method=6)
        except Exception as e:  # unreadable file: leave it, build will report
            log(f'could not convert {f.relative_to(ROOT)}: {e}')
            continue
        f.unlink()
        done.append(f'{f.parent.name}/{f.name} -> {role}')
    return done


def tidy_roles() -> list[str]:
    """Accept a role typed as a filename or path ('/assets/x/My Photo.jpg' -> 'my-photo')."""
    fixed = []
    for p in sorted(WORKS.glob('*.json')):
        data = json.loads(p.read_text(encoding='utf-8'))
        changed = False
        def norm(v):
            return slug_role(v) if isinstance(v, str) and ('/' in v or '.' in v or ' ' in v or v != v.lower()) else v
        v = norm(data.get('feature_image'))
        if v != data.get('feature_image'):
            data['feature_image'] = v; changed = True
        for item in data.get('views', {}).get('items', []):
            v = norm(item.get('role'))
            if v != item.get('role'):
                item['role'] = v; changed = True
        if changed:
            p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            fixed.append(p.name)
    return fixed


def ensure_live_worktree():
    if (LIVE / '.git').exists():
        git('checkout', '-q', 'gh-pages', cwd=LIVE)
        git('pull', '-q', '--ff-only', 'origin', 'gh-pages', cwd=LIVE)
        return
    git('fetch', '-q', 'origin', 'gh-pages')
    git('worktree', 'add', str(LIVE), 'gh-pages')


def sync_live(message: str) -> bool:
    for child in LIVE.iterdir():
        if child.name == '.git':
            continue
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    shutil.copytree(ROOT / 'dist', LIVE, dirs_exist_ok=True)
    git('add', '-A', cwd=LIVE)
    if not git('status', '--porcelain', cwd=LIVE):
        return False
    git('commit', '-q', '-m', message, cwd=LIVE)
    git('push', '-q', 'origin', 'gh-pages', cwd=LIVE)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    if LOCK.exists() and time.time() - LOCK.stat().st_mtime < 1800:
        print('Another publish is running.'); return 0
    LOCK.write_text(str(time.time()))
    try:
        if git('rev-parse', '--abbrev-ref', 'HEAD') != 'main':
            raise RuntimeError('repository is not on main')
        # 1. local edits (e.g. CMS "Work with Local Repository")
        git('add', '-A', '--', 'content', 'public/assets')
        if git('diff', '--cached', '--name-only'):
            git('commit', '-q', '-m', 'Content edit (local)')
            log('committed local content edits')
        other = [l for l in git('status', '--porcelain', '--untracked-files=no').splitlines() if l.strip()]
        if other:
            raise RuntimeError('uncommitted non-content changes; leaving them alone:\n' + '\n'.join(other))
        # 2. CMS saves
        git('fetch', '-q', 'origin')
        git('pull', '-q', '--rebase', 'origin', 'main')
        # 3. images + roles
        conv, roles = convert_uploads(), tidy_roles()
        if conv or roles:
            git('add', '-A', '--', 'content', 'public/assets')
            git('commit', '-q', '-m', 'Prepare uploaded images: ' + '; '.join(conv + roles)[:200])
            log('prepared images: ' + '; '.join(conv + roles))
        # 4. build + tests (a failure publishes nothing; the live site keeps the last good version)
        run(PY, 'src/build.py', '--check')
        run(PY, '-m', 'pytest', 'tests/static', '-q', '-p', 'no:cacheprovider')
        head = git('rev-parse', '--short', 'HEAD')
        if args.dry_run:
            STATUS.write_text(f'DRY RUN OK {datetime.now():%Y-%m-%d %H:%M} at {head}\n', encoding='utf-8')
            log(f'dry run ok at {head}'); return 0
        # 5. publish
        if git('rev-list', '--count', 'origin/main..HEAD') != '0':
            git('push', '-q', 'origin', 'main')
        ensure_live_worktree()
        changed = sync_live(f'Publish {head}')
        msg = f'PUBLISHED {head}' if changed else f'UP TO DATE {head}'
        STATUS.write_text(f'{msg} {datetime.now():%Y-%m-%d %H:%M}\n', encoding='utf-8')
        log(msg); return 0
    except Exception as e:
        STATUS.write_text(f'FAILED {datetime.now():%Y-%m-%d %H:%M} — live site unchanged\n{e}\n', encoding='utf-8')
        log(f'FAILED: {e}')
        if 'rebase' in str(e):
            git('rebase', '--abort', check=False)
        return 1
    finally:
        LOCK.unlink(missing_ok=True)


if __name__ == '__main__':
    sys.exit(main())
