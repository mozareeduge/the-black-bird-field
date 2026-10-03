"""Writing edition: Ten Research Poems (ده شعر پژوهشی), Persian RTL at /writing/ten-research-poems/."""
import hashlib, json, re, subprocess, sys, unicodedata
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'
SLUG = 'ten-research-poems'
PAGE = DIST / 'writing' / SLUG / 'index.html'
DATA = json.loads((ROOT / f'content/writing/{SLUG}.json').read_text(encoding='utf8'))
ORIGIN = json.loads((ROOT / 'content/site.json').read_text(encoding='utf8'))['site_origin']
DOCX = Path(r'C:/Users/Zarinpal/Documents/Personal Formal Documents/Artworks/ده_شعر_پژوهشی_محمد_زارع.docx')
BLOCK = 'h1,h2,h3,p,li,span.trp-line,span.trp-poem-label,span.trp-xref'


def setup_module():
    subprocess.run([sys.executable, 'src/build.py', '--package-preview'], cwd=ROOT, check=True)


def soup(p=PAGE):
    return BeautifulSoup(p.read_text(encoding='utf8'), 'html.parser')


def edition_blocks(s):
    """Text blocks of the edition body in document order, edition apparatus (TOC, cover meta, links) removed."""
    art = s.select_one('article#edition')
    for x in art.select('[data-apparatus]'):
        x.decompose()
    els = art.select(BLOCK); sel = set(map(id, els))
    return [e.get_text() for e in els if not any(id(p) in sel for p in e.parents)]


def stored_blocks():
    t = DATA['text']
    out = [t['title'], t['author'], t['mark'], t['intro']['heading'], *t['intro']['paragraphs']]
    for s in t['sequences']:
        out.append(s['heading'])
        out += [x['text'] for x in s['source']]
        out.append(t['separator'])
        out += [x['text'] for x in s['poem'] if x['type'] != 'break']
    out.append(t['bibliography_heading'])
    for s in t['sequences']:
        out.append(s['bibliography']['heading'])
        out += [e['text'] for e in s['bibliography']['entries']]
    return out


def test_page_is_persian_rtl_with_metadata():
    s = soup()
    assert s.html['lang'] == 'fa' and s.html['dir'] == 'rtl'
    assert s.find('link', rel='canonical')['href'] == f'{ORIGIN}/writing/{SLUG}/'
    assert s.find('meta', property='og:url')['content'] == f'{ORIGIN}/writing/{SLUG}/'
    assert s.find('meta', property='og:image')['content'] == f'{ORIGIN}/writing-assets/ten-research-poems-share.webp'
    assert 'ده شعر پژوهشی' in s.title.string and 'Ten Research Poems' in s.title.string
    assert s.h1.get_text() == 'ده شعر پژوهشی' and len(s.find_all('h1')) == 1
    ld = json.loads(s.find('script', type='application/ld+json').string)
    assert ld['@type'] == 'Book' and ld['inLanguage'] == 'fa' and ld['datePublished'] == '2026-10-03'
    assert ld['author']['name'] == 'Mohammad Zare' and ld['license'] and len(ld['hasPart']) == 10
    # English site chrome stays LTR inside the RTL document
    assert s.select_one('header.site-header')['dir'] == 'ltr' and s.select_one('footer.site-footer')['dir'] == 'ltr'
    assert s.select_one('#english')['dir'] == 'ltr' and s.select_one('#english')['lang'] == 'en'


def test_ten_sequences_with_stable_anchors_and_toc():
    s = soup()
    ids = [x['id'] for x in s.select('section.trp-seq')]
    assert ids == [f'poem-{n}' for n in range(1, 11)]
    assert [a['href'] for a in s.select('nav.trp-toc ol a')] == [f'#poem-{n}' for n in range(1, 11)]
    assert len(s.select('.trp-seq .trp-sep')) == 10
    assert len(s.select('.trp-bib-group')) == 10


def test_rendered_text_equals_stored_text_exactly():
    assert edition_blocks(soup()) == stored_blocks()


def test_rendered_text_equals_docx_when_available():
    import importlib.util, pytest
    if not DOCX.is_file() or importlib.util.find_spec('docx') is None:
        pytest.skip('author docx or python-docx not available on this machine')
    sys.path.insert(0, str(ROOT / 'scripts'))
    import extract_ten_research_poems as X
    src = X.source_texts(DOCX)
    got = edition_blocks(soup())
    assert got == src  # exact, block by block
    norm = lambda xs: re.sub(r'\s+', ' ', unicodedata.normalize('NFC', ' '.join(xs))).strip()
    assert norm(got) == norm(src)
    assert sum(t.count('\u200c') for t in got) == sum(t.count('\u200c') for t in src) > 200
    assert X.extract(DOCX) == DATA['text']


def test_publication_essentials():
    s = soup(); text = s.get_text(' ')
    assert '© ۲۰۲۵–۲۰۲۶ محمد زارع — همهٔ حقوق محفوظ است' in text
    assert '© 2025–2026 Mohammad Zare. All rights reserved.' in text
    assert '3 October 2026' in text and 'Version' in text
    assert f'{ORIGIN}/writing/{SLUG}/' in s.select_one('#colophon').get_text(' ')
    pdf = DIST / DATA['pdf']['path']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == DATA['pdf']['sha256']
    assert DATA['pdf']['sha256'] in text
    assert all(a['href'] == '../../' + DATA['pdf']['path'] for a in s.select('a[download]'))
    assert (DIST / 'fonts/vazirmatn/OFL.txt').is_file() and (DIST / 'fonts/vazirmatn/Vazirmatn-wght.woff2').is_file()


def test_owner_wording_rules():
    # The edition's own apparatus (cover, colophon, English note, metadata); the bibliography may cite translated sources.
    s = soup()
    for x in s.select('.trp-bib'):
        x.decompose()
    text = s.select_one('main').get_text(' ') + ' ' + s.title.string + ' ' + s.find('meta', attrs={'name': 'description'})['content']
    for banned in ('unpublished', 'manuscript', 'translat', 'OWNER', 'Asadollahi', 'ترجمه', 'منتشرنشده', 'دست‌نوشته'):
        assert banned.lower() not in text.lower(), banned
    assert 'published here in full in Persian' in text.replace('Published', 'published')


def test_in_sitemap_and_linked_from_about_and_practice():
    assert f'<loc>{ORIGIN}/writing/{SLUG}/</loc>' in (DIST / 'sitemap.xml').read_text(encoding='utf8')
    for rel in ('about/index.html', 'practice/index.html'):
        hrefs = [a['href'] for a in soup(DIST / rel).find('main').find_all('a')]
        assert f'../writing/{SLUG}/index.html' in hrefs, rel


def test_not_a_work():
    assert SLUG not in [p.stem for p in (ROOT / 'content/works').glob('*.json')]
    assert 'ten-research-poems' not in (DIST / 'works/index.html').read_text(encoding='utf8')
