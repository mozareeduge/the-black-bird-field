#!/usr/bin/env python3
"""Create exactly one new work manifest and its asset directory.
It does not invent curatorial copy or images; TODO fields must be authored before build can pass.
"""
from __future__ import annotations
import argparse, json, re
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; WORKS=ROOT/'content/works'; ASSETS=ROOT/'public/assets'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--slug',required=True); ap.add_argument('--title',required=True); ap.add_argument('--form',required=True); ap.add_argument('--mode',required=True); ap.add_argument('--year',type=int,default=date.today().year)
    args=ap.parse_args(); slug=args.slug.strip().lower()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug): raise SystemExit('slug must be lowercase kebab-case')
    out=WORKS/f'{slug}.json'; ad=ASSETS/slug
    if out.exists() or ad.exists(): raise SystemExit(f'work or asset directory already exists for slug: {slug}')
    current=[json.loads(p.read_text(encoding='utf8')) for p in WORKS.glob('*.json')]
    order=max([x['order'] for x in current],default=0)+1
    data={
      'schema_version':'1.0.0','slug':slug,'asset_slug':slug,'order':order,'title':args.title,'title_parts':[args.title],
      'mode':args.mode,'form':args.form,'year':args.year,'summary':'TODO: concise portfolio summary.','responsibility':'TODO: what new literary responsibility this work gives the browser','meta_description':'TODO: project-specific metadata description.',
      'live_url':'TODO: https://…','repository_url':'TODO: https://github.com/…','poster_caption':'TODO: release/build identity','feature_caption':'TODO: release/build identity','feature_image':'view-02',
      'hero_lead':'TODO: project-page lead.',
      'prelude':{'label':'READING CONDITIONS','items':[['01 / CONDITION','TODO',''],['02 / CONDITION','TODO',''],['03 / CONDITION','TODO','']]},
      'views':{'title':'Three views','intro':'Three images hold distinct reading conditions without reducing the work to a single representative screen.','items':[['01','TODO','TODO','view-01',f'{args.title}: TODO'],['02','TODO','TODO','view-02',f'{args.title}: TODO'],['03','TODO','TODO','view-03',f'{args.title}: TODO']]},
      'context':{'title':'TODO','paragraphs':['TODO','TODO'],'coda':''},
      'identity':{'edition':'TODO: exact release/build identity','language':'TODO','encounter':'TODO'},
      'citation':{'author':'Mohammad Zare.','title':args.title,'rest':'TODO: citation remainder.'}
    }
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    ad.mkdir(parents=True,exist_ok=False)
    (ad/'README.txt').write_text('Required image pairs before build can pass:\nposter-desktop.webp / poster-mobile.webp\nview-01-desktop.webp / view-01-mobile.webp\nview-02-desktop.webp / view-02-mobile.webp\nview-03-desktop.webp / view-03-mobile.webp\n',encoding='utf8')
    print(f'Created work {order:02d}: {out.relative_to(ROOT)}')
    print(f'Created asset directory: {ad.relative_to(ROOT)}')
    print('Complete TODO fields and add the required WebP pairs, then run: python src/build.py --check')
if __name__=='__main__': main()
