"""Route and build-architecture tests (R-ROUTES-ALIASES, R-BUILD-ARCHITECTURE).

Run: python -m pytest tests/static/test_routes.py -v
"""
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'

sys.path.insert(0, str(ROOT / 'src'))
from content import WORK_ORDER, WORKS  # noqa: E402
from site_config import ROUTES, LEGACY_REDIRECTS, GRAVE_RUNTIME_OUTPUT  # noqa: E402


@pytest.fixture(scope='module', autouse=True)
def built():
    subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py'), '--check'], cwd=ROOT, check=True)


def canonical_routes():
    return {k: m for k, m in ROUTES.items() if m.get('sitemap', True)}


def alias_routes():
    return {k: m for k, m in ROUTES.items() if m.get('noindex')}


def test_all_canonical_pages_exist():
    canon = canonical_routes()
    assert len(canon) == 10, f'expected 10 canonical pages, got {len(canon)}'
    for meta in canon.values():
        assert (DIST / meta['output']).is_file(), meta['output']


def test_all_aliases_exist():
    aliases = alias_routes()
    assert len(aliases) == 5, f'expected 5 aliases, got {len(aliases)}'
    for meta in aliases.values():
        assert (DIST / meta['output']).is_file(), meta['output']


def test_all_legacy_stubs_exist():
    assert len(LEGACY_REDIRECTS) == 9
    for old_name, _ in LEGACY_REDIRECTS:
        assert (DIST / old_name).is_file(), old_name


def test_grave_runtime_exists():
    assert (DIST / GRAVE_RUNTIME_OUTPUT).is_file()


def test_total_html_count_is_25():
    html_files = list(DIST.rglob('*.html'))
    assert len(html_files) == 25, sorted(p.relative_to(DIST).as_posix() for p in html_files)


def test_sitemap_contains_exactly_ten_canonical_urls():
    xml = (DIST / 'sitemap.xml').read_text(encoding='utf-8')
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    root = ET.fromstring(xml)
    locs = {el.text for el in root.findall('.//s:loc', ns)}
    assert len(locs) == 10
    expected = {f'https://theblackbirdfield.com{m["route"]}' for m in canonical_routes().values()}
    assert locs == expected


def test_sitemap_excludes_aliases_stubs_and_runtime():
    xml = (DIST / 'sitemap.xml').read_text(encoding='utf-8')
    for meta in alias_routes().values():
        assert f'>https://theblackbirdfield.com{meta["route"]}<' not in xml


@pytest.mark.parametrize('key', [k for k in ROUTES if ROUTES[k].get('noindex')])
def test_alias_canonicalizes_to_works_page(key):
    meta = ROUTES[key]
    html = (DIST / meta['output']).read_text(encoding='utf-8')
    canonical_route = ROUTES[meta['canonical_key']]['route']
    assert f'<link rel="canonical" href="https://theblackbirdfield.com{canonical_route}">' in html
    assert 'noindex,follow' in html


def test_work_order_on_home():
    html = (DIST / 'index.html').read_text(encoding='utf-8')
    positions = [html.find(WORKS[k]['title']) for k in WORK_ORDER]
    assert all(p != -1 for p in positions), positions
    assert positions == sorted(positions)


def test_work_order_on_works_index():
    html = (DIST / 'works' / 'index.html').read_text(encoding='utf-8')
    positions = [html.find(WORKS[k]['title']) for k in WORK_ORDER]
    assert all(p != -1 for p in positions), positions
    assert positions == sorted(positions)


def test_two_builds_are_byte_identical():
    subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py')], cwd=ROOT, check=True)
    first = {p.relative_to(DIST): p.read_bytes() for p in DIST.rglob('*') if p.is_file()}
    subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py')], cwd=ROOT, check=True)
    second = {p.relative_to(DIST): p.read_bytes() for p in DIST.rglob('*') if p.is_file()}
    assert first == second
