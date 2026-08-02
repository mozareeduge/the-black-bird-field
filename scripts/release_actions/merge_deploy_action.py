#!/usr/bin/env python3
from action_common import *
mode=sys.argv[1]; branch=CFG['feature_branch']; origin=CFG['portfolio_origin']
def pr_data():
 rc,out,_=gh('pr','view',branch,'--json','number,state,mergeStateStatus,headRefOid,baseRefName,headRefName,url,statusCheckRollup,mergedAt,mergeCommit')
 return rc,(json.loads(out) if rc==0 else {})
def candidate_acceptance():
 evidence=require_release_evidence(); p=ROOT/'artifacts/release/DESIGN_ACCEPTANCE.json'
 if not p.is_file(): raise SystemExit('separate design acceptance record missing')
 acceptance=load(p)
 if acceptance.get('snapshot_id')!=CFG['snapshot_id'] or acceptance.get('status')!='ACCEPTED' or acceptance.get('accepted_by')!='USER': raise SystemExit('design acceptance identity/status invalid')
 if acceptance.get('candidate_identity')!=evidence.get('candidate_identity'): raise SystemExit('accepted candidate differs from release evidence')
 return evidence,acceptance
if mode=='detect':
 rc,data=pr_data(); ok=rc==0 and data.get('state')=='MERGED'
 if ok:
  try:
   with urllib.request.urlopen(origin+'/',timeout=30) as r: ok=r.status==200
  except Exception: ok=False
 json_out(data if data else {'state':'ABSENT'}); raise SystemExit(0 if ok else 1)
if mode=='apply':
 candidate_acceptance(); rc,data=pr_data()
 if rc or data.get('state')!='OPEN' or data.get('headRefName')!=branch or data.get('baseRefName')!=CFG['base_branch']: raise SystemExit('pull request identity invalid')
 if data.get('mergeStateStatus') not in {'CLEAN','HAS_HOOKS'}: raise SystemExit('pull request is not cleanly merge-ready')
 checks=data.get('statusCheckRollup') or []
 bad=[x for x in checks if x.get('status')!='COMPLETED' or x.get('conclusion') not in {'SUCCESS','NEUTRAL','SKIPPED'}]
 if bad: json_out({'failing_or_incomplete_checks':bad}); raise SystemExit('required checks are not complete and successful')
 raise SystemExit(gh('pr','merge',str(data['number']),'--squash','--delete-branch',timeout=600)[0])
if mode=='readback':
 rc,data=pr_data()
 if rc or data.get('state')!='MERGED' or not data.get('mergeCommit'): raise SystemExit(1)
 merge_sha=data['mergeCommit'].get('oid'); deadline=time.time()+1200; selected=None
 while time.time()<deadline:
  rc,out,_=gh('run','list','--workflow','Pages','--branch','main','--limit','10','--json','databaseId,headSha,status,conclusion,url,workflowName')
  if rc==0:
   runs=json.loads(out); selected=next((x for x in runs if x.get('headSha')==merge_sha),None)
   if selected and selected.get('status')=='completed': break
  time.sleep(15)
 if not selected or selected.get('conclusion')!='success': json_out({'pr':data,'pages_run':selected}); raise SystemExit(1)
 rc,out,err=run([sys.executable,'scripts/verify_live_release.py'],ROOT,900)
 json_out({'pr':data,'pages_run':selected,'live_readback_exit':rc,'live_readback_stdout':out[-8000:],'live_readback_stderr':err[-4000:]})
 raise SystemExit(0 if rc==0 else 1)
if mode=='rollback':
 print('Automatic rollback is intentionally disabled after merge. Use a separately authorized revert of the recorded merge commit and redeploy the previous known-good main candidate.',file=sys.stderr); raise SystemExit(1)
raise SystemExit('unknown mode')
