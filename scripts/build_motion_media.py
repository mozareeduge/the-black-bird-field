#!/usr/bin/env python3
"""Build restrained, authentic-state motion loops for The Black Bird Field.

The loops are made from manifest-declared authentic captured states.  Optical
movement is deliberately minute; temporal meaning comes from the relation
between real states, not from invented interface animation.
"""
from __future__ import annotations
import json, subprocess, tempfile
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'public/assets'; WORKS=ROOT/'content/works'
FPS=30; SEG=3.10; TRANSITION=.72; MAX_BYTES=1_500_000
DRIFT={
 'the-black-bird':[1.000,1.012,1.007,1.000],
 'winter-road':[1.000,1.016,1.008,1.000],
 'unhappy-scenario':[1.000,1.010,1.012,1.000],
 'grave-machine':[1.000,1.008,1.010,1.000],
 'taroke-remixer':[1.000,1.010,1.014,1.000],
}

def works(): return sorted((json.loads(p.read_text(encoding='utf-8')) for p in WORKS.glob('*.json')),key=lambda x:x['order'])
def even(n): return n if n%2==0 else n-1
def dim(p):
    with Image.open(p) as im:return even(im.width),even(im.height)
def run(cmd): subprocess.run(cmd,check=True)

def segment(src:Path,out:Path,size:tuple[int,int],zmax:float,reverse=False):
    w,h=size; frames=max(1,round(SEG*FPS)); delta=zmax-1
    if reverse:
        zexpr=f'{zmax:.6f}-{delta:.6f}*on/{frames-1}'
    else:
        zexpr=f'1+{delta:.6f}*on/{frames-1}'
    # Centered drift only: enough to avoid dead slideshow quality without inventing spatial semantics.
    vf=f"scale={w}:{h}:flags=lanczos,zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS},format=yuv420p"
    run(['ffmpeg','-y','-loglevel','error','-i',str(src),'-vf',vf,'-an','-r',str(FPS),'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',str(out)])

def build_one(w,size):
    m=w['motion']; roles=list(m['source_roles']); roles=[roles[0],roles[1],roles[2],roles[0]]
    sources=[ASSETS/w['asset_slug']/f'{r}-{size}.webp' for r in roles]
    if any(not p.exists() for p in sources): raise SystemExit(f'missing state: {w["slug"]}/{size}')
    wh=dim(sources[0])
    out=ASSETS/w['asset_slug']/m[f'{size}_file']
    with tempfile.TemporaryDirectory(prefix='bbf-motion-') as td:
        td=Path(td); segs=[]
        for i,(src,z) in enumerate(zip(sources,DRIFT[w['slug']])):
            sp=td/f's{i}.mp4'; segment(src,sp,wh,z,reverse=(i==3)); segs.append(sp)
        # All intermediate segments are CFR H264; xfade is now deterministic.
        filt=(f'[0:v][1:v]xfade=transition=fade:duration={TRANSITION}:offset={SEG-TRANSITION}[x1];'
              f'[x1][2:v]xfade=transition=fade:duration={TRANSITION}:offset={2*(SEG-TRANSITION)}[x2];'
              f'[x2][3:v]xfade=transition=fade:duration={TRANSITION}:offset={3*(SEG-TRANSITION)},format=yuv420p[out]')
        cmd=['ffmpeg','-y','-loglevel','error']
        for sp in segs:cmd+=['-i',str(sp)]
        cmd+=['-filter_complex',filt,'-map','[out]','-an','-r',str(FPS),'-c:v','libx264','-preset','slow','-crf','19','-profile:v','high','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
        run(cmd)
        if out.stat().st_size>MAX_BYTES:
            cmd[cmd.index('19')]='22';run(cmd)
    if out.stat().st_size>MAX_BYTES:raise SystemExit(f'over budget {out} {out.stat().st_size}')
    return {'work':w['slug'],'size':size,'file':str(out.relative_to(ROOT)),'bytes':out.stat().st_size,'dimensions':list(wh)}

def main():
    rows=[]
    for w in works():
        if w.get('motion',{}).get('enabled'):
            for size in ('desktop','mobile'): rows.append(build_one(w,size))
    report={'version':'1.1','fps':FPS,'segment_seconds':SEG,'transition_seconds':TRANSITION,'nominal_duration_seconds':round(4*SEG-3*TRANSITION,2),'encoder':'H.264 libx264 slow CRF19; CRF22 only if budget enforcement required','max_bytes_each':MAX_BYTES,'method':'authentic captured states + minute centered optical drift + cross-dissolve; return to first state for seamless loop','files':rows}
    (ROOT/'validation').mkdir(exist_ok=True);(ROOT/'validation/MOTION_MEDIA_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
