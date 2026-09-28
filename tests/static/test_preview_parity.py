"""The editor preview (public/admin/preview-render.js) must produce exactly the markup the build publishes."""
import json, re, shutil, subprocess, sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from content import load_site, load_works  # noqa: E402
from renderers import document, render_home, render_works, render_project, render_practice, render_about, render_contact  # noqa: E402

NODE = shutil.which('node')
SCRIPT = r'''
const r = require(process.argv[1]);
const data = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const out = {};
for (const page of data.pages) { const x = r.renderPage(page, data.site, data.works); out[page] = {body: x.body, bodyClass: x.bodyClass, folder: x.folder}; }
process.stdout.write(JSON.stringify(out));
'''


def python_pages(site, works):
    pages = {}
    def add(key, output, main, cls, current):
        html = document(output=output, title='', description='', canonical='', body_class=cls, current=current, main=main, site=site, works=works)
        m = re.search(r'<body class="([^"]*)">(.*)<script src="[^"]*site\.js"></script></body>', html, re.S)
        pages[key] = {'body': m.group(2), 'bodyClass': m.group(1), 'folder': output.removesuffix('index.html')}
    o, _, _, main = render_home(site, works); add('home', o, main, 'home-page', 'home')
    o, _, _, main = render_works(site, works); add('works', o, main, 'works-page', 'works')
    for w in works:
        o, _, _, main, cls = render_project(site, works, w); add(f"work:{w['slug']}", o, main, cls, 'works')
    for fn, key, cls in [(render_practice, 'practice', 'practice-page'), (render_about, 'about', 'about-page'), (render_contact, 'contact', 'contact-page')]:
        o, _, _, main = fn(site, works); add(key, o, main, cls, key)
    return pages


def js_pages(site, works, pages):
    payload = json.dumps({'site': site, 'works': works, 'pages': pages})
    res = subprocess.run([NODE, '-e', SCRIPT, str(ROOT / 'public/admin/preview-render.js')], input=payload, capture_output=True, text=True, encoding='utf-8', check=True)
    return json.loads(res.stdout)


def variants(site, works):
    yield 'current content', site, works
    # Optional fields absent or empty, as an editor might leave them.
    w2 = [dict(w) for w in works]
    for w in w2:
        w.pop('motion', None); w.pop('body_class', None); w['title_parts'] = []
        w['context'] = {**w['context'], 'coda': ''}
    yield 'optional fields empty', site, w2
    yield 'single work', site, works[:1]
    yield 'two works', site, works[:2]


@pytest.mark.skipif(NODE is None, reason='node is not installed')
def test_preview_renderer_matches_build_for_every_page():
    site, works = load_site(), load_works()
    for label, s, ws in variants(site, works):
        expected = python_pages(s, ws)
        actual = js_pages(s, ws, list(expected))
        for page, want in expected.items():
            got = actual[page]
            assert got['bodyClass'] == want['bodyClass'], (label, page)
            assert got['folder'] == want['folder'], (label, page)
            if got['body'] != want['body']:
                i = next(i for i, (a, b) in enumerate(zip(got['body'], want['body'])) if a != b) if any(a != b for a, b in zip(got['body'], want['body'])) else min(len(got['body']), len(want['body']))
                pytest.fail(f"{label} / {page}: JS preview differs from build at char {i}:\n JS: {got['body'][max(0,i-80):i+80]!r}\n PY: {want['body'][max(0,i-80):i+80]!r}")


def test_admin_loads_preview_scripts():
    html = (ROOT / 'public/admin/index.html').read_text(encoding='utf-8')
    cms = html.index('sveltia-cms.js')
    assert cms < html.index('./preview-render.js') < html.index('./preview.js')
