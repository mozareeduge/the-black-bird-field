"""
Static build integrity tests — no browser required.
Run: python -m pytest tests/static/ -v
"""

import json
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'
SRC = ROOT / 'src'
PUBLIC = ROOT / 'public'
FIXTURES = ROOT / 'tests' / 'fixtures'


def _sha256(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


class TestBuildProducesExpectedFiles:
    def test_nine_html_pages(self):
        pages = list(DIST.glob('*.html'))
        assert len(pages) == 9, f'Expected 9 HTML pages, got {len(pages)}: {pages}'

    def test_expected_page_names(self):
        expected = {
            'index.html', 'works.html', 'black-bird.html', 'winter-road.html',
            'grave-machine.html', 'taroke-remixer.html', 'practice.html',
            'about.html', 'contact.html',
        }
        actual = {p.name for p in DIST.glob('*.html')}
        assert expected == actual

    def test_five_css_files(self):
        css = list((DIST / 'assets' / 'css').glob('*.css'))
        assert len(css) == 5

    def test_three_js_files(self):
        js = list((DIST / 'assets' / 'js').glob('*.js'))
        names = {f.name for f in js}
        assert names == {'site.js', 'atlas.js', 'cv-download.js'}

    def test_grave_runtime_present(self):
        grave = DIST / 'works' / 'grave-machine' / 'index.html'
        assert grave.exists(), 'Grave-Machine runtime missing from dist'

    def test_cv_pdf_present(self):
        cv = DIST / 'Mohammad_Zare_AcademicCV.pdf'
        assert cv.exists(), 'CV PDF missing from dist'


class TestGraveRuntimeChecksum:
    def test_grave_byte_identical(self):
        checksums = json.loads((FIXTURES / 'checksums.json').read_text())
        expected = checksums['grave_machine_bilingual_v1_1']
        actual = _sha256(DIST / 'works' / 'grave-machine' / 'index.html')
        assert actual == expected, (
            f'Grave-Machine runtime checksum mismatch:\n'
            f'  expected: {expected}\n'
            f'  actual:   {actual}'
        )

    def test_public_grave_matches_dist(self):
        src_hash = _sha256(PUBLIC / 'works' / 'grave-machine' / 'index.html')
        dst_hash = _sha256(DIST / 'works' / 'grave-machine' / 'index.html')
        assert src_hash == dst_hash, 'public/ and dist/ Grave runtimes differ'


class TestPublicPrivateBoundary:
    """Verify no private Grave working materials entered the repository."""

    def test_no_taroke_json_in_repo(self):
        matches = list(ROOT.rglob('*.taroke.json'))
        # Allow only if inside .claude/ relay workload area
        public_matches = [m for m in matches if '.claude' not in str(m) and 'workload' not in str(m)]
        assert not public_matches, f'taroke.json files found outside private area: {public_matches}'

    def test_no_editing_workbook_in_repo(self):
        matches = list(ROOT.rglob('*Editing_Workbook*'))
        assert not matches, f'Editing workbook files found: {matches}'

    def test_no_diagnostic_report_in_repo(self):
        matches = list(ROOT.rglob('*Diagnostic_and_QA*'))
        assert not matches, f'Diagnostic files found: {matches}'

    def test_grave_public_dir_contains_only_index(self):
        grave_public = PUBLIC / 'works' / 'grave-machine'
        files = list(grave_public.iterdir())
        assert [f.name for f in files] == ['index.html'], (
            f'Unexpected files in public/works/grave-machine/: {files}'
        )


class TestPageStructure:
    def _read(self, name):
        return (DIST / name).read_text(encoding='utf-8')

    def test_index_has_correct_title(self):
        html = self._read('index.html')
        assert '<title>The Black Bird Field — Works by Mozare</title>' in html

    def test_index_has_four_works(self):
        html = self._read('index.html')
        for work in ['The Black Bird', 'Winter Road', 'Grave-Machine', 'TAROKE RIMIXER']:
            assert work in html, f'Work not found in index: {work}'

    def test_grave_link_points_to_runtime(self):
        html = self._read('index.html')
        assert 'works/grave-machine/' in html

    def test_no_stale_grave_build_reference(self):
        for page in DIST.glob('*.html'):
            html = page.read_text()
            assert 'grave-current-build' not in html, (
                f'Stale grave-current-build reference in {page.name}'
            )

    def test_no_fresh_image_references_in_dist(self):
        for page in DIST.glob('*.html'):
            html = page.read_text()
            assert 'grave-machine/fresh/' not in html, (
                f'Old fresh/ image path still in {page.name}'
            )

    def test_sticky_header_present(self):
        for page in DIST.glob('*.html'):
            html = page.read_text()
            assert 'data-site-header' in html, f'site-header missing from {page.name}'

    def test_skip_link_present(self):
        for page in DIST.glob('*.html'):
            html = page.read_text()
            assert 'skip-link' in html, f'Skip link missing from {page.name}'

    def test_cv_download_attribute_present(self):
        for page in DIST.glob('*.html'):
            if page.name == 'contact.html':
                continue
            html = page.read_text()
            assert 'data-cv-download' in html, f'data-cv-download missing from {page.name}'

    def test_no_colophon_page(self):
        assert not (DIST / 'colophon.html').exists()

    def test_grave_machine_page_bilingual_language(self):
        html = self._read('grave-machine.html')
        assert 'English / Persian' in html, 'Bilingual language not noted on grave-machine page'

    def test_no_redundant_page_title(self):
        # Each page should have exactly one <h1>
        for page in DIST.glob('*.html'):
            html = page.read_text()
            count = html.count('<h1')
            assert count == 1, f'{page.name} has {count} h1 elements (expected 1)'

    def test_mozare_artistic_name_in_header(self):
        html = self._read('index.html')
        assert 'works by Mozare' in html

    def test_mohammad_zare_in_footer(self):
        html = self._read('index.html')
        assert 'Mohammad Zare' in html

    def test_linkedin_link_present(self):
        html = self._read('index.html')
        assert 'linkedin.com/in/mohammad-zare' in html


class TestBuildIsDeterministic:
    def test_rebuild_produces_same_pages(self):
        """Rebuild and compare page contents."""
        import subprocess
        first = (DIST / 'works.html').read_bytes()
        subprocess.run([sys.executable, str(SRC / 'build.py')], check=True, capture_output=True)
        second = (DIST / 'works.html').read_bytes()
        # The CV blob encoding varies only if the PDF changes; content should be identical
        # We compare only the HTML pages (not cv-download.js which embeds the PDF)
        assert first == second, 'Build is not deterministic for works.html'


class TestImageAssets:
    def test_bilingual_screenshots_in_dist(self):
        bilingual = DIST / 'assets' / 'grave-machine' / 'bilingual'
        assert bilingual.exists()
        images = list(bilingual.glob('*.png'))
        assert len(images) >= 6, f'Expected ≥6 bilingual screenshots, found {len(images)}'

    def test_black_bird_assets_present(self):
        bb = DIST / 'assets' / 'black-bird'
        assert bb.exists()
        pngs = list(bb.glob('*.png'))
        assert len(pngs) >= 10

    def test_winter_road_walkthrough_present(self):
        wr = DIST / 'assets' / 'winter-road' / 'walkthrough'
        assert wr.exists()
        pngs = list(wr.glob('*.png'))
        assert len(pngs) >= 5
