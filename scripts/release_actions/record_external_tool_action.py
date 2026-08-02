#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,datetime as dt

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,o):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument('runtime_dir');ap.add_argument('action_id');ap.add_argument('authorization_json');ap.add_argument('tool_result_json');a=ap.parse_args()
rt=Path(a.runtime_dir).resolve();state=load(rt/'runtime.json');contract=Path(state['contract_root']);snap=load(contract/'authority/SNAPSHOT.json')['snapshot_id'];acts={x['id']:x for x in load(contract/'operations/ACTIONS.json')['actions']}
if a.action_id not in acts:raise SystemExit('unknown action')
auth=load(a.authorization_json);res=load(a.tool_result_json)
if auth.get('snapshot_id')!=snap or auth.get('action_id')!=a.action_id or auth.get('authorized_by')!='USER':raise SystemExit('current user authorization required')
for f in acts[a.action_id]['authorization_fields']:
 if f not in auth.get('authorized_fields',[]):raise SystemExit('missing authorized field '+f)
if res.get('snapshot_id')!=snap or res.get('action_id')!=a.action_id or res.get('status')!='PASS':raise SystemExit('tool result identity/status invalid')
for k in ('tool','mutation_record','readback','rollback'):
 if not res.get(k):raise SystemExit('tool result missing '+k)
rec={'action_id':a.action_id,'recorded_at':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS','authorization_sha256':sha(a.authorization_json),'tool_result_sha256':sha(a.tool_result_json),'detect':res.get('detect'),'action':res['mutation_record'],'readback':res['readback'],'rollback':res['rollback'],'idempotency_key':acts[a.action_id]['idempotency_key'],'tool':res['tool']}
dump(rt/'actions'/(a.action_id+'.json'),rec);state.setdefault('actions',{})[a.action_id]=rec;dump(rt/'runtime.json',state);print('ACTION_PASS');print(rt/'actions'/(a.action_id+'.json'))
