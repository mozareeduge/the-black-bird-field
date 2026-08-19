#!/usr/bin/env python3
"""Apply this audited replacement to a clean clone of the audited production baseline.

The script is intentionally conservative: it refuses a moved HEAD, dirty tree,
missing/mutated protected Grave runtime, or missing/mutated CV. It changes only
working-tree files. It never commits, pushes, opens/merges a PR, changes Pages,
changes DNS, or deploys.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, sys
from pathlib import Path

PACKAGE=Path(__file__).resolve().parents[1]
AUTH=json.loads((PACKAGE/'content/protected_artifacts.json').read_text(encoding='utf-8'))
EXPECTED_BASE=AUTH['baseline_commit']
ART=AUTH['artifacts']
CONTROL_DIRS=['content','src','tests','scripts','docs','.github/workflows','public/assets']
CONTROL_FILES=['00_START_HERE.md','README.md','CHANGELOG.md','CLAUDE.md','CLAUDE_CODE_EXECUTION_INTAKE.md','.gitignore','pyproject.toml','requirements-test.txt','requirements-tools.txt','public/site.css','public/site.js']


def run(cmd,cwd,check=True):
    return subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,check=check)

def sha256(p:Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git_blob_sha1(p:Path) -> str:
    data=p.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()

def verify_protected(repo:Path) -> None:
    grave=ART['grave_machine_runtime']; gp=repo/grave['source_path']
    if not gp.is_file(): raise SystemExit(f"Missing protected runtime: {grave['source_path']}")
    if gp.stat().st_size!=grave['size_bytes']: raise SystemExit(f"Protected Grave-Machine size mismatch: {gp.stat().st_size}")
    actual=sha256(gp)
    if actual!=grave['sha256']: raise SystemExit(f'Protected Grave-Machine checksum mismatch: {actual}')
    blob=git_blob_sha1(gp)
    if blob!=grave['git_blob_sha1']: raise SystemExit(f'Protected Grave-Machine git-blob checksum mismatch: {blob}')
    cv=ART['academic_cv']; cp=repo/cv['source_path']
    if not cp.is_file(): raise SystemExit(f"Missing protected CV: {cv['source_path']}")
    if cp.stat().st_size!=cv['size_bytes']: raise SystemExit(f"Protected CV size mismatch: {cp.stat().st_size}")
    actual=git_blob_sha1(cp)
    if actual!=cv['git_blob_sha1']: raise SystemExit(f'Protected CV git-blob checksum mismatch: {actual}')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('repo',type=Path,help='clean local clone of mozareeduge/the-black-bird-field at the audited baseline')
    ap.add_argument('--skip-tests',action='store_true',help='apply files without running post-apply build/static checks')
    a=ap.parse_args(); repo=a.repo.resolve()
    if not (repo/'.git').exists(): raise SystemExit(f'Not a Git clone: {repo}')
    remote=run(['git','remote','get-url','origin'],repo,check=False).stdout.strip()
    allowed_remotes={
        'https://github.com/mozareeduge/the-black-bird-field.git',
        'https://github.com/mozareeduge/the-black-bird-field',
        'git@github.com:mozareeduge/the-black-bird-field.git',
    }
    if remote not in allowed_remotes:
        raise SystemExit(f'Unexpected origin remote: {remote!r}')
    head=run(['git','rev-parse','HEAD'],repo).stdout.strip()
    if head!=EXPECTED_BASE:
        raise SystemExit(f'Baseline moved: expected {EXPECTED_BASE}, got {head}. Stop and re-audit instead of forcing this package onto a different repository state.')
    dirty=run(['git','status','--porcelain'],repo).stdout.strip()
    if dirty: raise SystemExit('Working tree is not clean. Commit/stash/discard changes before migration.')
    verify_protected(repo)

    # Replacement-owned surfaces. public/works and public/documents are excluded
    # deliberately so the verified runtime and CV remain byte-identical.
    for rel in CONTROL_DIRS:
        dst=repo/rel
        if dst.exists(): shutil.rmtree(dst)
        src=PACKAGE/rel
        if src.exists(): shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
    for rel in CONTROL_FILES:
        src=PACKAGE/rel
        if not src.is_file(): raise SystemExit(f'Package missing controlled file: {rel}')
        dst=repo/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)

    verify_protected(repo)
    print('Applied repository replacement to the local working tree.')
    print('No commit, push, PR, merge, Pages/DNS change, or deployment was performed.')
    if not a.skip_tests:
        subprocess.run([sys.executable,'src/build.py','--check'],cwd=repo,check=True)
        subprocess.run([sys.executable,'-m','pytest','tests/static','-q'],cwd=repo,check=True)
        print('PASS: protected artifacts unchanged and source/static gates completed.')
    else:
        print('PASS: protected artifacts unchanged. Post-apply build/tests were explicitly skipped.')
    print('Next: inspect `git diff --stat`, review the rendered site, then choose separately whether to commit/push/PR/deploy.')

if __name__=='__main__': main()
