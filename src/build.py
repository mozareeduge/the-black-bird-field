from __future__ import annotations
import argparse, hashlib, shutil
from pathlib import Path
from html import escape
from content import load_site, load_works, load_protected_artifacts
from renderers import document, render_home, render_works, render_project, render_practice, render_about, render_contact

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'; DIST=ROOT/'dist'
LEGACY={
 'works.html':'works/index.html','black-bird.html':'works/the-black-bird/index.html','winter-road.html':'works/winter-road/index.html',
 'unhappy-scenario.html':'works/unhappy-scenario/index.html','grave-machine.html':'works/grave-machine/index.html','taroke-remixer.html':'works/taroke-remixer/index.html',
 'practice.html':'practice/index.html','about.html':'about/index.html','contact.html':'contact/index.html',
}

def sha256(path:Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git_blob_sha1(path:Path) -> str:
    data=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()

def write(rel,text):
    p=DIST/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')

def legacy_stub(old,target,origin):
    canonical=origin+'/'+target.replace('index.html','')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{escape(canonical)}"><meta http-equiv="refresh" content="0;url={escape(target)}"><title>Redirecting — The Black Bird Field</title></head><body><script>(function(){{var t={target!r};location.replace(t+(location.search||'')+(location.hash||''));}})();</script><p>This page has moved. <a href="{escape(target)}">Continue →</a></p></body></html>'''

def asset(role,work): return f"assets/{work['asset_slug']}/{role}-desktop.webp"

def protected_paths(authority:dict):
    a=authority['artifacts']
    grave=a['grave_machine_runtime']; cv=a['academic_cv']
    return (ROOT/grave['source_path'], grave, ROOT/cv['source_path'], cv)

def validate_sources(site,works,authority,strict_protected=True):
    errors=[]
    def walk(value, where):
        if isinstance(value, dict):
            for k,v in value.items(): walk(v, f'{where}.{k}')
        elif isinstance(value, list):
            for i,v in enumerate(value): walk(v, f'{where}[{i}]')
        elif isinstance(value, str) and 'TODO' in value:
            errors.append(f'unresolved TODO: {where}')
    walk(site,'site')
    for w in works:
        walk(w, w['slug'])
        roles=['poster',w['feature_image']]+[x[3] for x in w['views']['items']]
        for role in set(roles):
            for size in ('desktop','mobile'):
                p=PUBLIC/'assets'/w['asset_slug']/f'{role}-{size}.webp'
                if not p.is_file(): errors.append(f'missing asset: {p.relative_to(ROOT)}')
        motion=w.get('motion') or {}
        if motion.get('enabled'):
            for key in ('desktop_file','mobile_file'):
                mp=PUBLIC/'assets'/w['asset_slug']/motion[key]
                if not mp.is_file(): errors.append(f'missing motion asset: {mp.relative_to(ROOT)}')
                elif mp.stat().st_size>1_500_000: errors.append(f'motion asset exceeds 1.5 MB budget: {mp.relative_to(ROOT)}')
    grave_path,grave,cv_path,cv=protected_paths(authority)
    if strict_protected:
        if not grave_path.is_file():
            errors.append(f"missing protected Grave-Machine runtime: {grave['source_path']}")
        else:
            if grave_path.stat().st_size!=grave['size_bytes']: errors.append(f"protected Grave-Machine runtime size mismatch: {grave_path.stat().st_size}")
            actual=sha256(grave_path)
            if actual!=grave['sha256']: errors.append(f'protected Grave-Machine runtime checksum mismatch: {actual}')
            blob=git_blob_sha1(grave_path)
            if blob!=grave['git_blob_sha1']: errors.append(f'protected Grave-Machine git-blob checksum mismatch: {blob}')
        if not cv_path.is_file():
            errors.append(f"missing protected CV: {cv['source_path']}")
        else:
            if cv_path.stat().st_size!=cv['size_bytes']:
                errors.append(f"protected CV size mismatch: {cv_path.stat().st_size}")
            actual=git_blob_sha1(cv_path)
            if actual!=cv['git_blob_sha1']:
                errors.append(f'protected CV git-blob checksum mismatch: {actual}')
    if errors: raise SystemExit('SOURCE VALIDATION FAILED\n- '+'\n- '.join(errors))

def build(strict_protected=True):
    site=load_site(); works=load_works(); authority=load_protected_artifacts()
    validate_sources(site,works,authority,strict_protected)
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copy2(PUBLIC/'site.css',DIST/'site.css'); shutil.copy2(PUBLIC/'site.js',DIST/'site.js')
    shutil.copy2(PUBLIC/'favicon.svg',DIST/'favicon.svg'); shutil.copy2(PUBLIC/'favicon.ico',DIST/'favicon.ico')
    shutil.copytree(PUBLIC/'assets',DIST/'assets')
    (DIST/'.nojekyll').write_text('',encoding='utf8')
    (DIST/'CNAME').write_text(site['site_origin'].removeprefix('https://').removeprefix('http://')+'\n',encoding='utf8')
    grave_path,grave,cv_path,cv=protected_paths(authority)
    if cv_path.is_file():
        cvout=DIST/cv['output_path']; cvout.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(cv_path,cvout)
    if grave_path.is_file():
        out=DIST/grave['output_path']; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(grave_path,out)
    output,title,desc,main=render_home(site,works)
    write(output,document(output=output,title=title,description=desc,canonical=site['site_origin']+'/',body_class='home-page',current='home',main=main,site=site,works=works,og_image=asset('poster',works[0])))
    output,title,desc,main=render_works(site,works)
    write(output,document(output=output,title=title,description=desc,canonical=site['site_origin']+'/works/',body_class='works-page',current='works',main=main,site=site,works=works,og_image=asset(works[0]['feature_image'],works[0])))
    for w in works:
        output,title,desc,main,cls=render_project(site,works,w)
        write(output,document(output=output,title=title,description=desc,canonical=site['site_origin']+f"/works/{w['slug']}/",body_class=cls,current='works',main=main,site=site,works=works,og_image=asset('poster',w)))
    for renderer,key,cls in [(render_practice,'practice','practice-page'),(render_about,'about','about-page'),(render_contact,'contact','contact-page')]:
        output,title,desc,main=renderer(site,works)
        write(output,document(output=output,title=title,description=desc,canonical=site['site_origin']+f'/{key}/',body_class=cls,current=key,main=main,site=site,works=works,og_image=asset('poster',works[0]) if key!='contact' else None))
    for old,target in LEGACY.items(): write(old,legacy_stub(old,target,site['site_origin']))
    urls=['/','/works/']+[f"/works/{w['slug']}/" for w in works]+['/practice/','/about/','/contact/']
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{escape(site["site_origin"]+u)}</loc></url>\n' for u in urls)+'</urlset>\n'
    write('sitemap.xml',xml); write('robots.txt',f'User-agent: *\nAllow: /\nSitemap: {site["site_origin"]}/sitemap.xml\n')
    return site,works

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--package-preview',action='store_true',help='build portfolio shell before protected current-production binaries are inherited'); ap.add_argument('--check',action='store_true')
    a=ap.parse_args(); strict=not a.package_preview
    if a.check and not strict: raise SystemExit('--check cannot be combined with --package-preview')
    site,works=build(strict_protected=strict)
    print(f'Built {len(works)}-work portfolio → {DIST}')
    if not strict: print('PACKAGE PREVIEW ONLY: protected Grave runtime and CV are intentionally inherited during migration into the current clone.')
if __name__=='__main__': main()
