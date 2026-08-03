"""Security and privacy checks (R-SECURITY-PRIVACY, Section 10.3).

Run: python -m pytest tests/static/test_security.py -v
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'

EXTERNAL_SRC_RE = re.compile(r'(?:src|href)="(https?://[^"]+)"')
ANALYTICS_PATTERNS = ('gtag(', 'ga(', 'analytics', 'plausible', 'google-analytics', 'googletagmanager')
INLINE_HANDLER_RE = re.compile(r'\son[a-z]+\s*=\s*"', re.IGNORECASE)

ALLOWED_EXTERNAL_HOSTS = (
    'theblackbirdfield.com', 'poem.theblackbirdfield.com', 'unhappy.theblackbirdfield.com',
    'mozareeduge.github.io', 'github.com', 'www.linkedin.com', 'linkedin.com',
    'www.w3.org',
)

# The Grave-Machine runtime is a protected, checksum-locked artwork file
# (D-GRAVE-PRESERVATION) — it is never edited and is excluded from these
# portfolio-authored checks.
GRAVE_RUNTIME_OUTPUT = 'works/grave-machine/run/index.html'


@pytest.fixture(scope='module', autouse=True)
def built():
    subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py')], cwd=ROOT, check=True)


def all_html_files():
    return sorted(
        p for p in DIST.rglob('*.html')
        if p.relative_to(DIST).as_posix() != GRAVE_RUNTIME_OUTPUT
    )


def test_csp_present_on_all_canonical_and_alias_pages():
    sys.path.insert(0, str(ROOT / 'src'))
    from site_config import ROUTES  # noqa: E402
    for meta in ROUTES.values():
        html = (DIST / meta['output']).read_text(encoding='utf-8')
        assert 'Content-Security-Policy' in html, meta['output']
        assert "connect-src 'none'" in html, meta['output']
        assert 'name="referrer"' in html, meta['output']


def test_no_unexpected_external_origins():
    for path in all_html_files():
        html = path.read_text(encoding='utf-8')
        for url in EXTERNAL_SRC_RE.findall(html):
            host = url.split('/')[2]
            assert host in ALLOWED_EXTERNAL_HOSTS, f'{path.relative_to(DIST)}: unexpected external host {host}'


def test_no_analytics_identifiers():
    for path in all_html_files():
        html = path.read_text(encoding='utf-8').lower()
        for pattern in ANALYTICS_PATTERNS:
            assert pattern not in html, f'{pattern!r} found in {path.relative_to(DIST)}'


def test_no_inline_event_handlers():
    for path in all_html_files():
        html = path.read_text(encoding='utf-8')
        assert not INLINE_HANDLER_RE.search(html), f'inline event handler found in {path.relative_to(DIST)}'


def test_no_base64_pdf_data():
    for path in all_html_files():
        html = path.read_text(encoding='utf-8')
        assert 'application/pdf;base64' not in html, path.relative_to(DIST)
        assert 'atob(' not in html, path.relative_to(DIST)


def test_external_links_use_noopener():
    for path in all_html_files():
        html = path.read_text(encoding='utf-8')
        for m in re.finditer(r'<a\b[^>]*target="_blank"[^>]*>', html):
            assert 'noopener' in m.group(0), f'{path.relative_to(DIST)}: {m.group(0)}'


def test_no_cookies_or_storage_calls_in_scripts():
    js_dir = DIST / 'assets' / 'js'
    for js_file in js_dir.glob('*.js'):
        text = js_file.read_text(encoding='utf-8')
        assert 'document.cookie' not in text, js_file.name
        assert 'localStorage' not in text, js_file.name
        assert 'sessionStorage' not in text, js_file.name
