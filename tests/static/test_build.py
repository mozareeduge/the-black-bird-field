import json, subprocess, sys, re
from pathlib import Path
from bs4 import BeautifulSoup
from src.content import load_works
ROOT=Path(__file__).resolve().parents[2]; DIST=ROOT/'dist'

def setup_module():
    subprocess.run([sys.executable,'src/build.py','--package-preview'],cwd=ROOT,check=True)

def works(): return load_works()
def slugs(): return [w['slug'] for w in works()]
def pages():
    return [DIST/'index.html',DIST/'works/index.html',*(DIST/f'works/{s}/index.html' for s in slugs()),DIST/'practice/index.html',DIST/'about/index.html',DIST/'contact/index.html']

def test_expected_pages_and_legacy_redirects():
    for p in pages(): assert p.is_file(),p
    for p in ['works.html','black-bird.html','winter-road.html','unhappy-scenario.html','grave-machine.html','taroke-remixer.html','practice.html','about.html','contact.html']:
        assert (DIST/p).is_file()

def test_one_h1_metadata_csp_and_safe_external_links():
    for p in pages():
        s=BeautifulSoup(p.read_text(encoding='utf8'),'html.parser')
        assert len(s.find_all('h1'))==1,p
        assert s.find('link',rel='canonical')
        assert s.find('meta',attrs={'name':'description'})['content'].strip()
        assert s.find('meta',attrs={'http-equiv':'Content-Security-Policy'})
        for a in s.find_all('a',target='_blank'):
            assert {'noopener','noreferrer'} <= set(a.get('rel',[])),(p,a.get('href'))
        for img in s.find_all('img'):
            assert img.get('alt','').strip(),(p,img.get('src'))

def test_all_local_references_resolve():
    bad=[]
    for p in pages():
        s=BeautifulSoup(p.read_text(encoding='utf8'),'html.parser')
        for tag,attr in [('a','href'),('img','src'),('script','src'),('link','href'),('source','srcset')]:
            for el in s.find_all(tag):
                ref=el.get(attr)
                if not ref or ref.startswith(('http:','https:','mailto:','tel:','#','data:')): continue
                ref=ref.split('?')[0].split('#')[0]
                t=(p.parent/ref).resolve()
                if t.is_dir(): t=t/'index.html'
                if not t.exists(): bad.append((str(p.relative_to(DIST)),ref))
    allowed={('about/index.html','../documents/Mohammad_Zare_AcademicCV.pdf')}
    assert set(bad) in (set(), allowed),bad

def test_home_preview_mapping_is_one_to_one_and_ordered():
    s=BeautifulSoup((DIST/'index.html').read_text(encoding='utf8'),'html.parser')
    links=s.select('[data-preview-index]'); frames=s.select('[data-preview-frame]')
    expected=slugs()
    assert len(links)==len(frames)==len(expected)
    assert [x['data-work-slug'] for x in links]==expected==[x['data-work-slug'] for x in frames]
    assert frames[0].get('class') and 'active' in frames[0]['class']
    assert sum('active' in x.get('class',[]) for x in frames)==1

def test_dynamic_count_copy_matches_manifest_count():
    n=len(works()); home=(DIST/'index.html').read_text(encoding='utf8')
    from src.renderers import num_word
    assert f'{num_word(n)} autonomous works' in home.lower()
    assert f'{num_word(n,True)} works' in BeautifulSoup(home,'html.parser').get_text(' ',strip=True)

def test_motion_is_only_authorized_threshold_media_and_review_ui_is_absent():
    corpus='\n'.join(p.read_text(encoding='utf8') for p in pages())
    assert 'motion-review' not in corpus.lower(); assert not re.search(r'\batlas\b',corpus,re.I)
    home=BeautifulSoup((DIST/'index.html').read_text(encoding='utf8'),'html.parser')
    motion_home=sum(bool((w.get('motion') or {}).get('enabled') and (w.get('motion') or {}).get('home_preview')) for w in works())
    assert len(home.select('.hero-preview video.motion-video'))==motion_home
    assert not home.select('.feature video')
    for w in works():
        page=BeautifulSoup((DIST/f"works/{w['slug']}/index.html").read_text(encoding='utf8'),'html.parser')
        expected=1 if (w.get('motion') or {}).get('enabled') and (w.get('motion') or {}).get('project_hero') else 0
        assert len(page.select('.project-hero-media video.motion-video'))==expected
        assert not page.select('.selected-views video')

def test_project_hero_motion_wrapper_has_explicit_fill_contract():
    css=(ROOT/'public/site.css').read_text(encoding='utf8')
    assert '.project-hero-media>.motion-media{width:100%;height:100%}' in css

def test_sitemap_has_every_canonical_page_once():
    site=json.loads((ROOT/'content/site.json').read_text()); xml=(DIST/'sitemap.xml').read_text()
    expected=['/','/works/']+[f"/works/{s}/" for s in slugs()]+['/practice/','/about/','/contact/']
    locs=re.findall(r'<loc>(.*?)</loc>',xml)
    assert locs==[site['site_origin']+route for route in expected]

def test_pages_deployment_markers():
    assert (DIST/'CNAME').read_text(encoding='utf8').strip()=='theblackbirdfield.com'
    assert (DIST/'.nojekyll').is_file()

def test_build_is_deterministic():
    import hashlib
    def fp():
        rows=[]
        for p in sorted(x for x in DIST.rglob('*') if x.is_file()): rows.append(str(p.relative_to(DIST))+':'+hashlib.sha256(p.read_bytes()).hexdigest())
        return hashlib.sha256('\n'.join(rows).encode()).hexdigest()
    before=fp(); subprocess.run([sys.executable,'src/build.py','--package-preview'],cwd=ROOT,check=True,capture_output=True,text=True); assert fp()==before
