import re
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
CSS=(ROOT/'public/site.css').read_text(encoding='utf-8')
DIST=ROOT/'dist'

def test_v8_microtype_tokens_and_no_sub_11_authored_text():
    assert '--micro:12px' in CSS
    assert '--micro-tight:11px' in CSS
    assert '--micro-muted:#514b43' in CSS
    assert '--micro-signal:#684216' in CSS
    # v08.1 deliberately closes the old 8/9/10px authored-text tier.
    scrub=re.sub(r'clamp\([^)]*\)','',CSS)
    assert not re.search(r'font(?:-size)?\s*:[^;}]*\b(?:8|9|10)px\b',scrub)

def test_light_field_micro_colors_clear_45_contrast():
    def lum(h):
        vals=[int(h[i:i+2],16)/255 for i in (1,3,5)]
        vals=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals]
        return .2126*vals[0]+.7152*vals[1]+.0722*vals[2]
    def cr(a,b):
        x,y=sorted([lum(a),lum(b)],reverse=True);return (x+.05)/(y+.05)
    assert cr('#514b43','#c7bfb2')>=4.5
    assert cr('#684216','#c7bfb2')>=4.5

def test_home_about_strip_removes_redundant_display_identity():
    s=BeautifulSoup((DIST/'index.html').read_text(encoding='utf-8'),'html.parser')
    strip=s.select_one('.about-strip'); assert strip
    assert not strip.find('h2')
    assert strip.select_one('.section-no').get_text(' ',strip=True)=='03 / ABOUT'
    assert strip.select_one('.about-strip-action a')

def test_works_first_row_has_no_redundant_top_rule():
    assert '.work-row:first-child{border-top' not in CSS

def test_contact_is_key_value_action_row_not_far_edge_arrow():
    assert 'grid-template-columns:112px minmax(0,max-content) auto 1fr' in CSS
    assert 'font:clamp(21px,1.55vw,27px)/1.2 var(--serif)' in CSS
    s=BeautifulSoup((DIST/'contact/index.html').read_text(encoding='utf-8'),'html.parser')
    rows=s.select('.contact-row'); assert len(rows)==3
    for row in rows:
        children=[x.name for x in row.find_all(recursive=False)]
        assert children==['span','strong','b']

def test_all_motion_assets_resolve_and_budget():
    import json
    for p in (ROOT/'content/works').glob('*.json'):
        w=json.loads(p.read_text()); m=w.get('motion') or {}
        if not m.get('enabled'): continue
        for key in ('desktop_file','mobile_file'):
            f=ROOT/'public/assets'/w['asset_slug']/m[key]
            assert f.is_file() and 0<f.stat().st_size<=1_500_000,f

def test_owner_locked_fallbacks():
    import json
    expected={'winter-road':'view-midpoint','unhappy-scenario':'view-reconnecting','grave-machine':'view-midpoint'}
    for slug,role in expected.items():
        w=json.loads((ROOT/f'content/works/{slug}.json').read_text())
        assert w['motion']['fallback_role']==role
        page=BeautifulSoup((DIST/f'works/{slug}/index.html').read_text(),'html.parser')
        poster=page.select_one('.project-hero-media .motion-poster source[media]')
        assert role in poster['srcset']


def test_about_cv_uses_final_public_url():
    s=BeautifulSoup((DIST/'about/index.html').read_text(encoding='utf-8'),'html.parser')
    a=next(x for x in s.select('a') if x.get_text(' ',strip=True).startswith('Download CV'))
    assert a['href']=='https://theblackbirdfield.com/documents/Mohammad_Zare_AcademicCV.pdf'


def test_taroke_desktop_capture_identity_glyph_is_normalized():
    from PIL import Image
    source=(57,16,66,35); target=(82,16,91,35)
    def mask(im,box): return [px>30 for px in im.crop(box).convert('L').get_flattened_data()]
    def iou(a,b):
        inter=sum(x and y for x,y in zip(a,b)); union=sum(x or y for x,y in zip(a,b))
        return inter/union if union else 1.0
    d=ROOT/'public/assets/taroke-remixer'
    for name in ['poster-desktop.webp','view-first_change-desktop.webp','view-midpoint-desktop.webp','view-last_change-desktop.webp']:
        im=Image.open(d/name)
        assert iou(mask(im,source),mask(im,target))>=.90,name


def test_migration_owns_primary_handoff_files():
    script=(ROOT/'scripts/apply_to_current_repo.py').read_text(encoding='utf-8')
    for name in ['00_START_HERE.md','CHANGELOG.md','CLAUDE_CODE_EXECUTION_INTAKE.md','requirements-tools.txt']:
        assert repr(name) in script,name
