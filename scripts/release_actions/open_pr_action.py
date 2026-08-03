#!/usr/bin/env python3
from action_common import *
mode=sys.argv[1]; branch=CFG['feature_branch']; base=CFG['base_branch']
def view():
 rc,out,_=gh('pr','view',branch,'--json','number,state,headRefName,baseRefName,url,headRefOid,statusCheckRollup')
 return rc,(json.loads(out) if rc==0 else {})
if mode=='detect':
 rc,data=view(); json_out(data if data else {'state':'ABSENT'}); raise SystemExit(0 if rc==0 and data.get('state')=='OPEN' and data.get('headRefName')==branch and data.get('baseRefName')==base else 1)
if mode=='apply':
 require_release_evidence()
 rc,b,_=git('branch','--show-current')
 if rc or b.strip()!=branch: raise SystemExit('wrong feature branch')
 if git('status','--porcelain')[1].strip(): raise SystemExit('worktree must be clean and committed')
 if git('push','-u','origin',branch,timeout=600)[0]: raise SystemExit(1)
 body=ROOT/'artifacts/release/PR_BODY.md'
 if not body.is_file(): raise SystemExit('candidate-bound PR body missing')
 args=['pr','create','--base',base,'--head',branch,'--title',CFG['pr_title'],'--body-file',str(body)]
 raise SystemExit(gh(*args,timeout=300)[0])
if mode=='readback':
 rc,data=view(); ok=rc==0 and data.get('state')=='OPEN' and data.get('headRefName')==branch and data.get('baseRefName')==base
 json_out(data); raise SystemExit(0 if ok else 1)
if mode=='rollback':
 rc,data=view()
 if rc: raise SystemExit(0)
 if data.get('state')=='OPEN': raise SystemExit(gh('pr','close',str(data['number']),timeout=180)[0])
 raise SystemExit(0)
raise SystemExit('unknown mode')
