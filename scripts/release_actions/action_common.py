#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, os, subprocess, sys, tempfile, time, urllib.parse, urllib.request
ROOT=Path.cwd().resolve()
CFG_PATH=ROOT/'docs/authority/PROJECT_ACTION_CONFIG.json'
if not CFG_PATH.is_file(): raise SystemExit('project release action config missing')
CFG=json.loads(CFG_PATH.read_text(encoding='utf-8'))
PRESTATE=ROOT/'artifacts/release/external-prestate'
PRESTATE.mkdir(parents=True,exist_ok=True)
def run(argv,cwd=None,timeout=120,input_text=None):
 p=subprocess.run(argv,cwd=cwd or ROOT,text=True,input=input_text,capture_output=True,timeout=timeout)
 if p.stdout: print(p.stdout,end='')
 if p.stderr: print(p.stderr,end='',file=sys.stderr)
 return p.returncode,p.stdout,p.stderr
def gh(*args,timeout=120,input_text=None): return run(['gh',*args],ROOT,timeout,input_text)
def git(*args,timeout=120): return run(['git',*args],ROOT,timeout)
def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def dump(path,obj):
 path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha_file(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def json_out(obj): print(json.dumps(obj,indent=2,ensure_ascii=False))
def gh_api_json(method,path,payload=None,timeout=120):
 args=['api','--method',method,path]
 if payload is not None: args += ['--input','-']
 return gh(*args,timeout=timeout,input_text=(json.dumps(payload) if payload is not None else None))
def require_release_evidence():
 p=ROOT/'artifacts/release/RELEASE_EVIDENCE.json'
 if not p.is_file(): raise SystemExit('release evidence missing')
 data=load(p)
 if data.get('snapshot_id')!=CFG['snapshot_id'] or not data.get('candidate_identity'): raise SystemExit('release evidence identity invalid')
 return data
