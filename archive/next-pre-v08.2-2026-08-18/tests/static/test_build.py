"""Build-architecture invariants (R-BUILD-ARCHITECTURE, R-GRAVE-LOCK).

Route-count, sitemap, and copy-contract assertions live in
test_routes.py / test_copy_contract.py; this file covers the rest of the
generated output: asset counts, non-page files, and the Grave lock.

Run: python -m pytest tests/static/test_build.py -v
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'
GRAVE_RUNTIME_OUTPUT = 'works/grave-machine/run/index.html'
GRAVE_KEY = 'grave_machine_bilingual_v1_1'


@pytest.fixture(scope='module', autouse=True)
def built():
    result = subprocess.run(
        [sys.executable, str(ROOT / 'src' / 'build.py'), '--check'],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result


def test_build_check_reports_checksum_ok(built):
    assert f'checksum OK: {GRAVE_KEY}' in built.stdout


def test_no_unresolved_template_tokens_anywhere():
    for path in DIST.rglob('*.html'):
        assert '{{' not in path.read_text(encoding='utf-8'), path.relative_to(DIST)


def test_exactly_five_css_files():
    css_files = sorted(p.name for p in (DIST / 'assets' / 'css').glob('*.css'))
    assert css_files == ['base.css', 'components.css', 'pages.css', 'responsive.css', 'tokens.css']


def test_exactly_one_public_js_file():
    js_files = list((DIST / 'assets' / 'js').glob('*.js'))
    assert [f.name for f in js_files] == ['site.js']


def test_grave_runtime_matches_locked_checksum():
    expected = json.loads((ROOT / 'tests' / 'fixtures' / 'checksums.json').read_text())[GRAVE_KEY]
    actual = hashlib.sha256((DIST / GRAVE_RUNTIME_OUTPUT).read_bytes()).hexdigest()
    assert actual == expected


def test_cname_copied_for_custom_domain():
    assert (DIST / 'CNAME').read_text(encoding='utf-8').strip() == 'theblackbirdfield.com'


def test_cv_document_copied_unchanged():
    src = (ROOT / 'public' / 'documents' / 'Mohammad_Zare_AcademicCV.pdf').read_bytes()
    dst = (DIST / 'Mohammad_Zare_AcademicCV.pdf').read_bytes()
    assert src == dst


def test_fonts_copied():
    fonts = sorted(p.name for p in (DIST / 'assets' / 'fonts').glob('*.woff2'))
    assert len(fonts) == 8


def test_sitemap_and_robots_exist():
    assert (DIST / 'sitemap.xml').is_file()
    assert 'Sitemap:' in (DIST / 'robots.txt').read_text(encoding='utf-8')
