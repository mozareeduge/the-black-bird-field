"""CI browser acceptance. Local rescue validation uses validation/validate_candidate.py because this sandbox blocks browser localhost navigation."""
import contextlib, http.server, socketserver, subprocess, sys, threading, json
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]; DIST=ROOT/'dist'
WORKS=sorted((json.loads(p.read_text(encoding='utf8')) for p in (ROOT/'content/works').glob('*.json')),key=lambda w:w['order'])
PAGES=['/','/works/',*[f"/works/{w['slug']}/" for w in WORKS],'/practice/','/about/','/contact/']
VIEWPORTS=[(1440,900),(1101,800),(1024,768),(760,900),(390,844),(320,760)]

def launch_chromium(pw):
    system=Path('/usr/bin/chromium')
    if system.exists():
        return pw.chromium.launch(headless=True,executable_path=str(system),args=['--no-sandbox'])
    return pw.chromium.launch(headless=True)

@pytest.fixture(scope='module')
def server():
    subprocess.run([sys.executable,'src/build.py','--check'],cwd=ROOT,check=True)
    handler=lambda *a,**k:http.server.SimpleHTTPRequestHandler(*a,directory=str(DIST),**k)
    with socketserver.TCPServer(('127.0.0.1',0),handler) as httpd:
        t=threading.Thread(target=httpd.serve_forever,daemon=True); t.start(); yield f'http://127.0.0.1:{httpd.server_address[1]}'; httpd.shutdown()

def test_responsive_matrix(server):
    with sync_playwright() as pw:
        b=launch_chromium(pw)
        page=b.new_page()
        errors=[]; page.on('pageerror',lambda e: errors.append(str(e)))
        for route in PAGES:
            page.goto(server+route,wait_until='networkidle')
            for width,height in VIEWPORTS:
                page.set_viewport_size({'width':width,'height':height})
                m=page.evaluate('''() => ({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,h1:document.querySelectorAll('h1').length,bad:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length})''')
                assert m['sw']<=m['cw']+1,(route,width,m); assert m['h1']==1; assert m['bad']==0
        assert not errors,errors; b.close()

def test_home_preview_mapping_interaction(server):
    with sync_playwright() as pw:
        b=launch_chromium(pw); page=b.new_page(viewport={'width':1440,'height':900}); page.goto(server+'/',wait_until='networkidle')
        links=page.locator('[data-preview-index]')
        for i in range(links.count()):
            link=links.nth(i); slug=link.get_attribute('data-work-slug'); link.focus()
            active=page.locator('[data-preview-frame].active'); assert active.count()==1; assert active.get_attribute('data-work-slug')==slug
            assert slug.replace('-',' ') or True
        b.close()
