from pathlib import Path
import hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]
AUTH=json.loads((ROOT/'content/protected_artifacts.json').read_text())
G=AUTH['artifacts']['grave_machine_runtime']; C=AUTH['artifacts']['academic_cv']

def git_blob_sha1(p):
    d=p.read_bytes(); return hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()

def test_protected_authority_matches_audited_current_repository():
    assert AUTH['baseline_commit']=='c6fb375877daa47bd7c9061258efa61e73196da8'
    assert G['sha256']=='e6052d2b770614add5473657c8c0e2bd628b0874f0199a3c2651e63b86731359'
    assert C['git_blob_sha1']=='8d2de052d73890c4a48afd7f4b4ea83cf9269394'
    assert C['size_bytes']==54724

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
