from pathlib import Path
import hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]
AUTH=json.loads((ROOT/'content/protected_artifacts.json').read_text())
G=AUTH['artifacts']['grave_machine_runtime']; C=AUTH['artifacts']['academic_cv']

def git_blob_sha1(p):
    d=p.read_bytes(); return hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()

def test_protected_authority_manifest_is_complete():
    # Checks structure, not literal hash values — those are expected to change
    # whenever the CV or Grave-Machine runtime is intentionally updated. Run
    # `python scripts/update_protected_artifacts.py` after such a change to
    # keep this manifest in sync with the real files.
    assert AUTH['baseline_commit']
    for artifact in (G, C):
        assert artifact['size_bytes'] > 0
        assert artifact.get('sha256') or artifact.get('git_blob_sha1')

def test_build_check_refuses_package_before_protected_artifacts_are_inherited():
    gp=ROOT/G['source_path']; cp=ROOT/C['source_path']
    if gp.exists() and cp.exists():
        assert hashlib.sha256(gp.read_bytes()).hexdigest()==G['sha256']
        assert cp.stat().st_size==C['size_bytes'] and git_blob_sha1(cp)==C['git_blob_sha1']
    else:
        r=subprocess.run([sys.executable,'src/build.py','--check'],cwd=ROOT,capture_output=True,text=True)
        text=r.stdout+r.stderr
        assert r.returncode!=0
        assert ('missing protected Grave-Machine runtime' in text) or ('missing protected CV' in text)
