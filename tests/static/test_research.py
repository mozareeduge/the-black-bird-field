"""Research pages: cleared text stored as data, rendered in the About layout at /research/<slug>/."""
import json, re, subprocess, sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'
SLUG = 'taroko-gorge-ecosystem'
PAGE = DIST / 'research' / SLUG / 'index.html'
CLEARED = Path(r'C:/Users/Zarinpal/Documents/Personal Formal Documents/Apply/site-drafts/taroko-gorge-ecosystem.final.md')


def setup_module():
    subprocess.run([sys.executable, 'src/build.py', '--package-preview'], cwd=ROOT, check=True)


def soup(p):
    return BeautifulSoup(p.read_text(encoding='utf8'), 'html.parser')


def test_page_exists_with_title_canonical_and_og():
    assert PAGE.is_file()
    s = soup(PAGE)
    origin = json.loads((ROOT / 'content/site.json').read_text(encoding='utf8'))['site_origin']
    assert s.title.string == 'Taroko Gorge Ecosystem — The Black Bird Field'
    assert s.h1.get_text() == 'Taroko Gorge Ecosystem'
    assert s.find('link', rel='canonical')['href'] == f'{origin}/research/{SLUG}/'
    assert s.find('meta', property='og:url')['content'] == f'{origin}/research/{SLUG}/'
    assert s.find('meta', property='og:title')['content'] == s.title.string
    assert s.find('meta', property='og:image')['content'].startswith(origin + '/assets/')
    assert 'Taroko Gorge' in s.find('meta', attrs={'name': 'description'})['content']
    assert s.select_one('main .page-mast') and s.select_one('main .about-layout .about-copy')


def test_in_sitemap():
    origin = json.loads((ROOT / 'content/site.json').read_text(encoding='utf8'))['site_origin']
    assert f'<loc>{origin}/research/{SLUG}/</loc>' in (DIST / 'sitemap.xml').read_text(encoding='utf8')


def test_markdown_rendered_and_no_stray_markup():
    s = soup(PAGE); main = s.find('main')
    text = main.get_text(' ', strip=True)
    assert '*' not in text and '](' not in text and '`' not in text
    assert [e.get_text() for e in main.find_all('code')] == ['above', 'below']
    assert 'Tokyo Garage' in [e.get_text() for e in main.find_all('em')]
    hrefs = {a['href'] for a in main.find_all('a')}
    assert '../../works/grave-machine/index.html' in hrefs and '../../works/taroko-remixer/index.html' in hrefs
    assert 'https://github.com/mozareeduge/Taroko-Gorge-Ecosystem' in hrefs
    assert not re.search(r'TAROKE|RIMIXER', text)


def test_text_matches_cleared_source_when_available():
    if not CLEARED.is_file():
        return
    d = json.loads((ROOT / f'content/research/{SLUG}.json').read_text(encoding='utf8'))
    body = '# ' + d['title'] + '\n\n' + d['subtitle'] + '\n\n' + '\n\n'.join(d['paragraphs'])
    src = CLEARED.read_text(encoding='utf8')
    assert src.startswith(body)
    for row in d['record']:
        assert f"**{row['term']}:** {row['text']}" in src


def test_linked_from_about_and_taroko_work_pages():
    for rel, prefix in [('about/index.html', '../'), ('works/taroko-remixer/index.html', '../../'), ('works/grave-machine/index.html', '../../')]:
        hrefs = [a['href'] for a in soup(DIST / rel).find('main').find_all('a')]
        assert f'{prefix}research/{SLUG}/index.html' in hrefs, rel
