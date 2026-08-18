"""
Static performance budget checks (Section 10.4).

Run: python -m pytest tests/browser/test_performance_budget.py -v

These are lab-independent, file-size budgets checkable without a full
browser trace. They are release targets, not a substitute for measuring
LCP/CLS in a real browser before claiming them publicly.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'

HTML_BUDGET = 120 * 1024
CSS_BUDGET = 85 * 1024
JS_BUDGET = 12 * 1024
FONTS_BUDGET = 300 * 1024
LCP_DESKTOP_BUDGET = 350 * 1024
LCP_MOBILE_BUDGET = 180 * 1024
OTHER_DESKTOP_IMAGE_BUDGET = 300 * 1024
OTHER_MOBILE_IMAGE_BUDGET = 160 * 1024

CANONICAL_HTML = [
    'index.html', 'works/index.html', 'works/the-black-bird/index.html',
    'works/winter-road/index.html', 'works/unhappy-scenario/index.html',
    'works/grave-machine/index.html', 'works/taroke-remixer/index.html',
    'practice/index.html', 'about/index.html', 'contact/index.html',
]


@pytest.fixture(scope='module', autouse=True)
def build_once():
    subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py')], cwd=ROOT, check=True)


@pytest.mark.parametrize('rel', CANONICAL_HTML)
def test_html_budget(rel):
    size = (DIST / rel).stat().st_size
    assert size <= HTML_BUDGET, f'{rel}: {size} bytes exceeds {HTML_BUDGET}'


def test_css_budget():
    total = sum((DIST / 'assets' / 'css' / f).stat().st_size for f in
                ('tokens.css', 'base.css', 'components.css', 'pages.css', 'responsive.css'))
    assert total <= CSS_BUDGET, f'{total} bytes exceeds {CSS_BUDGET}'


def test_js_budget():
    total = sum(f.stat().st_size for f in (DIST / 'assets' / 'js').glob('*.js'))
    assert total <= JS_BUDGET, f'{total} bytes exceeds {JS_BUDGET}'


def test_fonts_budget():
    total = sum(f.stat().st_size for f in (DIST / 'assets' / 'fonts').glob('*.woff2'))
    assert total <= FONTS_BUDGET, f'{total} bytes exceeds {FONTS_BUDGET}'


PAGES_WITH_LCP_HERO = [
    'index.html', 'works/the-black-bird/index.html', 'works/winter-road/index.html',
    'works/unhappy-scenario/index.html', 'works/grave-machine/index.html',
    'works/taroke-remixer/index.html',
]


def test_lcp_hero_images_within_desktop_budget():
    import re
    for rel in PAGES_WITH_LCP_HERO:
        html = (DIST / rel).read_text(encoding='utf-8')
        m = re.search(r'src="([^"]+)"[^>]*fetchpriority="high"', html)
        assert m, f'{rel}: no fetchpriority=high hero image'
        resolved = (DIST / rel).parent.joinpath(m.group(1)).resolve()
        size = resolved.stat().st_size
        assert size <= LCP_DESKTOP_BUDGET, f'{rel} {m.group(1)}: {size} bytes exceeds {LCP_DESKTOP_BUDGET}'


def test_only_one_image_has_fetchpriority_high_on_lcp_pages():
    for rel in PAGES_WITH_LCP_HERO:
        html = (DIST / rel).read_text(encoding='utf-8')
        assert html.count('fetchpriority="high"') == 1, rel


def test_no_fetchpriority_high_on_pages_without_a_designated_hero():
    for rel in ('works/index.html', 'practice/index.html', 'about/index.html', 'contact/index.html'):
        html = (DIST / rel).read_text(encoding='utf-8')
        assert 'fetchpriority="high"' not in html, rel
