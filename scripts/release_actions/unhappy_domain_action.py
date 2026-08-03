#!/usr/bin/env python3
from action_common import *
mode=sys.argv[1]; domain=CFG['unhappy_domain']; repo=CFG['unhappy_repository']; zone=CFG['cloudflare_zone']; target=CFG['cloudflare_record_target']
PRE=PRESTATE/'A-CONFIGURE-UNHAPPY-DOMAIN.json'
def resolve(name):
 import socket
 try:return sorted({x[4][0] for x in socket.getaddrinfo(name,443,type=socket.SOCK_STREAM)})
 except Exception:return []
def cf_request(method,path,payload=None):
 token=os.environ.get('CLOUDFLARE_API_TOKEN')
 if not token: raise RuntimeError('CLOUDFLARE_API_TOKEN unavailable; use the connected Cloudflare tool and record the authorized action through the contract recorder')
 req=urllib.request.Request('https://api.cloudflare.com/client/v4'+path,method=method,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
 if payload is not None:req.data=json.dumps(payload).encode('utf-8')
 with urllib.request.urlopen(req,timeout=40) as r:
  data=json.loads(r.read())
 if data.get('success') is False: raise RuntimeError(json.dumps(data.get('errors') or data))
 return data
def zone_id():
 rs=(cf_request('GET','/zones?name='+urllib.parse.quote(zone)).get('result') or [])
 if len(rs)!=1: raise RuntimeError('Cloudflare zone not uniquely resolved')
 return rs[0]['id']
def dns_records():
 zid=zone_id(); rs=cf_request('GET',f'/zones/{zid}/dns_records?type=CNAME&name={urllib.parse.quote(domain)}').get('result') or []
 return zid,rs
def pages_get():
 rc,out,_=gh('api',f'repos/{repo}/pages',timeout=120)
 return rc,(json.loads(out) if rc==0 else {})
def pages_update(payload):
 rc,_,_=gh_api_json('PUT',f'repos/{repo}/pages',payload,timeout=180); return rc
def source_blob():
 rc,out,_=gh('api',f'repos/{repo}/contents/index.html','--jq','.sha',timeout=120)
 return out.strip() if rc==0 else ''
def canonical_status(html):
 import re
 hrefs=re.findall(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)',html,re.I)
 if not hrefs:
  hrefs=re.findall(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',html,re.I)
 return {'hrefs':hrefs,'conflict':any(not x.startswith('https://'+domain) for x in hrefs)}
def current_state():
 rc,pages=pages_get(); zid,records=dns_records(); return {'pages_exit':rc,'pages':pages,'zone_id':zid,'dns_records':records}
def live_readback():
 http={}; https={}
 try:
  req=urllib.request.Request('http://'+domain+'/',method='GET')
  with urllib.request.urlopen(req,timeout=30) as r:http={'status':r.status,'url':r.geturl()}
 except Exception as e:http={'error':str(e)}
 try:
  with urllib.request.urlopen('https://'+domain+'/',timeout=30) as r:
   body=r.read().decode('utf-8','ignore'); https={'status':r.status,'url':r.geturl(),'title_present':'UNHAPPY Scenario' in body,'canonical':canonical_status(body)}
 except Exception as e:https={'error':str(e)}
 return {'resolved':resolve(domain),'http':http,'https':https}
if mode=='detect':
 try:
  state=current_state(); live=live_readback(); pages=state['pages']; records=state['dns_records']; blob=source_blob()
  ok=blob==CFG['unhappy_index_blob_sha'] and state['pages_exit']==0 and pages.get('cname')==domain and pages.get('https_enforced') is True and any(x.get('content')==target and x.get('proxied') is False for x in records) and live['https'].get('status')==200 and live['https'].get('url','').startswith('https://'+domain) and live['https'].get('title_present') and not live['https'].get('canonical',{}).get('conflict')
  json_out({'source_blob':blob,'state':state,'live':live}); raise SystemExit(0 if ok else 1)
 except Exception as e: print(str(e),file=sys.stderr); raise SystemExit(1)
if mode=='apply':
 try:
  if source_blob()!=CFG['unhappy_index_blob_sha']: raise RuntimeError('UNHAPPY index blob differs from the approved release')
  state=current_state(); dump(PRE,state); zid=state['zone_id']; records=state['dns_records']; payload={'type':'CNAME','name':domain,'content':target,'ttl':1,'proxied':False}
  if records:
   keep=records[0]; cf_request('PUT',f'/zones/{zid}/dns_records/{keep["id"]}',payload)
   for extra in records[1:]: cf_request('DELETE',f'/zones/{zid}/dns_records/{extra["id"]}')
  else: cf_request('POST',f'/zones/{zid}/dns_records',payload)
  if pages_update({'cname':domain}): raise RuntimeError('GitHub Pages custom-domain update failed')
  deadline=time.time()+900; last={}; enforced=False
  while time.time()<deadline:
   rc,last=pages_get()
   if rc==0 and last.get('cname')==domain and pages_update({'cname':domain,'https_enforced':True})==0:
    enforced=True; break
   time.sleep(15)
  if last.get('cname')!=domain: raise RuntimeError('GitHub Pages did not retain the custom domain')
  if not enforced: raise RuntimeError('GitHub Pages HTTPS enforcement did not become available')
  raise SystemExit(0)
 except Exception as e: print(str(e),file=sys.stderr); raise SystemExit(3)
if mode=='readback':
 try:
  state=current_state(); live=live_readback(); pages=state['pages']; records=state['dns_records']; blob=source_blob()
  ok=blob==CFG['unhappy_index_blob_sha'] and state['pages_exit']==0 and pages.get('cname')==domain and pages.get('https_enforced') is True and any(x.get('content')==target and x.get('proxied') is False for x in records) and bool(live['resolved']) and live['http'].get('url','').startswith('https://'+domain) and live['https'].get('status')==200 and live['https'].get('url','').startswith('https://'+domain) and live['https'].get('title_present') and not live['https'].get('canonical',{}).get('conflict')
  json_out({'source_blob':blob,'state':state,'live':live}); raise SystemExit(0 if ok else 1)
 except Exception as e: print(str(e),file=sys.stderr); raise SystemExit(1)
if mode=='rollback':
 try:
  if not PRE.is_file(): raise RuntimeError('pre-action state missing; automatic rollback refused')
  previous=load(PRE); zid=zone_id(); _,current=dns_records()
  for rec in current: cf_request('DELETE',f'/zones/{zid}/dns_records/{rec["id"]}')
  for rec in previous.get('dns_records',[]):
   payload={k:rec[k] for k in ('type','name','content','ttl','proxied') if k in rec}
   cf_request('POST',f'/zones/{zid}/dns_records',payload)
  pages=previous.get('pages') or {}; payload={'cname':pages.get('cname'),'https_enforced':bool(pages.get('https_enforced'))}
  if pages_update(payload): raise RuntimeError('GitHub Pages prior-state restore failed')
  raise SystemExit(0)
 except Exception as e: print(str(e),file=sys.stderr); raise SystemExit(1)
raise SystemExit('unknown mode')
