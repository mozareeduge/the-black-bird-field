"""
Static build integrity tests — no browser required.
Run: python -m pytest tests/static/ -v
"""

import json
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'
SRC = ROOT / 'src'
PUBLIC = ROOT / 'public'
FIXTURES = ROOT / 'tests' / 'fixtures'

# Canonical pages: 9 directory-index pages (the indexed, canonical URLs)
_CANONICAL_PAGES = [
    'index.html',
    'works/index.html',
    'works/the-black-bird/index.html',
    'works/winter-road/index.html',
    'works/grave-machine/index.html',
    'works/taroke-remixer/index.html',
    'practice/index.html',
    'about/index.html',
    'contact/index.html',
]

# Legacy compatibility stubs: 8 flat-path redirects at root
_LEGACY_STUBS = [
    'works.html', 'black-bird.html', 'winter-road.html', 'grave-machine.html',
    'taroke-remixer.html', 'practice.html', 'about.html', 'contact.html',
]

# Grave-Machine runtime (byte-identical copy, not indexed)
_GRAVE_RUNTIME = 'works/grave-machine/run/index.html'

# Expected canonical URL for each page (matches SITE_ORIGIN + route)
_CANONICAL_URLS = {
    'index.html':                          'https://theblackbirdfield.com/',
    'works/index.html':                    'https://theblackbirdfield.com/works/',
    'works/the-black-bird/index.html':     'https://theblackbirdfield.com/works/the-black-bird/',
    'works/winter-road/index.html':        'https://theblackbirdfield.com/works/winter-road/',
    'works/grave-machine/index.html':      'https://theblackbirdfield.com/works/grave-machine/',
    'works/taroke-remixer/index.html':     'https://theblackbirdfield.com/works/taroke-remixer/',
    'practice/index.html':                 'https://theblackbirdfield.com/practice/',
    'about/index.html':                    'https://theblackbirdfield.com/about/',
    'contact/index.html':                  'https://theblackbirdfield.com/contact/',
}

# Expected legacy redirect targets (relative URLs from stub at root)
_LEGACY_TARGETS = {
    'works.html':           'works/',
    'black-bird.html':      'works/the-black-bird/',
    'winter-road.html':     'works/winter-road/',
    'grave-machine.html':   'works/grave-machine/',
    'taroke-remixer.html':  'works/taroke-remixer/',
    'practice.html':        'practice/',
    'about.html':           'about/',
    'contact.html':         'contact/',
}


def _sha256(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _read(rel_path):
    return (DIST / rel_path).read_text(encoding='utf-8')


def _all_canonical_paths():
    return [DIST / p for p in _CANONICAL_PAGES]


def _all_output_html():
    """All HTML files the build produces (canonical + stubs + runtime)."""
    return list(DIST.rglob('*.html'))


# ---------------------------------------------------------------------------
# Expected output files
# ---------------------------------------------------------------------------

class TestBuildProducesExpectedFiles:
    def test_nine_canonical_pages(self):
        for rel in _CANONICAL_PAGES:
            assert (DIST / rel).exists(), f'Canonical page missing: {rel}'

    def test_eight_legacy_stubs(self):
        for rel in _LEGACY_STUBS:
            assert (DIST / rel).exists(), f'Legacy stub missing: {rel}'

    def test_grave_runtime_present(self):
        assert (DIST / _GRAVE_RUNTIME).exists(), f'Grave runtime missing: {_GRAVE_RUNTIME}'

    def test_total_html_count(self):
        # 9 canonical + 8 legacy stubs + 1 Grave runtime = 18
        all_html = list(DIST.rglob('*.html'))
        assert len(all_html) == 18, (
            f'Expected 18 HTML files, got {len(all_html)}:\n' +
            '\n'.join(str(p.relative_to(DIST)) for p in sorted(all_html))
        )

    def test_five_css_files(self):
        css = list((DIST / 'assets' / 'css').glob('*.css'))
        assert len(css) == 5

    def test_three_js_files(self):
        js = list((DIST / 'assets' / 'js').glob('*.js'))
        names = {f.name for f in js}
        assert names == {'site.js', 'atlas.js', 'cv-download.js'}

    def test_cv_pdf_present(self):
        cv = DIST / 'Mohammad_Zare_AcademicCV.pdf'
        assert cv.exists(), 'CV PDF missing from dist'

    def test_sitemap_present(self):
        assert (DIST / 'sitemap.xml').exists()

    def test_robots_present(self):
        assert (DIST / 'robots.txt').exists()


# ---------------------------------------------------------------------------
# Grave-Machine checksum
# ---------------------------------------------------------------------------

class TestGraveRuntimeChecksum:
    def test_grave_byte_identical(self):
        checksums = json.loads((FIXTURES / 'checksums.json').read_text())
        expected = checksums['grave_machine_bilingual_v1_1']
        actual = _sha256(DIST / _GRAVE_RUNTIME)
        assert actual == expected, (
            f'Grave-Machine runtime checksum mismatch:\n'
            f'  expected: {expected}\n'
            f'  actual:   {actual}'
        )

    def test_public_grave_matches_dist(self):
        src_hash = _sha256(PUBLIC / 'works' / 'grave-machine' / 'index.html')
        dst_hash = _sha256(DIST / _GRAVE_RUNTIME)
        assert src_hash == dst_hash, 'public/ and dist/ Grave runtimes differ'


# ---------------------------------------------------------------------------
# Private / public boundary
# ---------------------------------------------------------------------------

class TestPublicPrivateBoundary:
    def test_no_taroke_json_in_repo(self):
        matches = list(ROOT.rglob('*.taroke.json'))
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


# ---------------------------------------------------------------------------
# Page structure — canonical pages
# ---------------------------------------------------------------------------

class TestPageStructure:
    def test_index_has_correct_title(self):
        html = _read('index.html')
        assert '<title>The Black Bird Field — Works by Mozare</title>' in html

    def test_index_has_four_works(self):
        html = _read('index.html')
        for work in ['The Black Bird', 'Winter Road', 'Grave-Machine', 'TAROKE RIMIXER']:
            assert work in html, f'Work not found in index: {work}'

    def test_grave_launch_link_points_to_runtime(self):
        html = _read('index.html')
        assert 'works/grave-machine/run/' in html, (
            'Home page must link to Grave-Machine runtime at works/grave-machine/run/'
        )

    def test_no_stale_grave_build_reference(self):
        for page in _all_output_html():
            html = page.read_text()
            assert 'grave-current-build' not in html, (
                f'Stale grave-current-build reference in {page.relative_to(DIST)}'
            )

    def test_no_fresh_image_references_in_dist(self):
        for page in _all_output_html():
            html = page.read_text()
            assert 'grave-machine/fresh/' not in html, (
                f'Old fresh/ image path in {page.relative_to(DIST)}'
            )

    def test_sticky_header_present_on_canonical_pages(self):
        for path in _all_canonical_paths():
            html = path.read_text()
            assert 'data-site-header' in html, f'site-header missing from {path.relative_to(DIST)}'

    def test_skip_link_present_on_canonical_pages(self):
        for path in _all_canonical_paths():
            html = path.read_text()
            assert 'skip-link' in html, f'Skip link missing from {path.relative_to(DIST)}'

    def test_cv_download_attribute_on_canonical_pages(self):
        for path in _all_canonical_paths():
            rel = path.relative_to(DIST)
            if str(rel) == 'contact/index.html':
                continue
            html = path.read_text()
            assert 'data-cv-download' in html, f'data-cv-download missing from {rel}'

    def test_no_colophon_page(self):
        assert not (DIST / 'colophon.html').exists()
        assert not (DIST / 'colophon' / 'index.html').exists()

    def test_grave_machine_page_bilingual_language(self):
        html = _read('works/grave-machine/index.html')
        assert 'English / Persian' in html, 'Bilingual language not noted on grave-machine page'

    def test_one_h1_per_canonical_page(self):
        for path in _all_canonical_paths():
            html = path.read_text()
            count = html.count('<h1')
            assert count == 1, (
                f'{path.relative_to(DIST)} has {count} h1 elements (expected 1)'
            )

    def test_mozare_artistic_name_in_header(self):
        html = _read('index.html')
        assert 'works by Mozare' in html

    def test_mohammad_zare_in_footer(self):
        html = _read('index.html')
        assert 'Mohammad Zare' in html

    def test_linkedin_link_present(self):
        html = _read('index.html')
        assert 'linkedin.com/in/mohammad-zare' in html

    def test_no_unresolved_template_tokens(self):
        token_re = re.compile(r'\{\{[^}]+\}\}')
        for page in _all_output_html():
            html = page.read_text()
            found = token_re.findall(html)
            assert not found, (
                f'Unresolved template tokens in {page.relative_to(DIST)}: {found}'
            )

    def test_no_path_traversal_in_canonical_pages(self):
        # Canonical pages should use '../../' style prefixes, not absolute /
        # paths or external asset references pointing to the wrong host.
        # We only guard against obvious traversal past the repo root.
        for path in _all_canonical_paths():
            html = path.read_text()
            assert '../../../assets/' not in html, (
                f'Potential over-traversal in {path.relative_to(DIST)}'
            )

    def test_no_stale_flat_links_in_canonical_pages(self):
        # Canonical pages must not link to the legacy flat-file names.
        stale = [
            'href="works.html"', 'href="black-bird.html"', 'href="winter-road.html"',
            'href="grave-machine.html"', 'href="taroke-remixer.html"',
            'href="practice.html"', 'href="about.html"', 'href="contact.html"',
        ]
        for path in _all_canonical_paths():
            html = path.read_text()
            for s in stale:
                assert s not in html, (
                    f'Stale flat link {s!r} found in canonical page {path.relative_to(DIST)}'
                )

    def test_no_stale_black_bird_github_pages_url(self):
        stale = 'mozareeduge.github.io/the-black-bird'
        for path in _all_canonical_paths():
            html = path.read_text()
            assert stale not in html, (
                f'Stale Black Bird GitHub Pages URL in {path.relative_to(DIST)}'
            )

    def test_black_bird_links_to_poem_subdomain(self):
        html = _read('works/the-black-bird/index.html')
        assert 'https://poem.theblackbirdfield.com/' in html, (
            'Black Bird page must link to poem.theblackbirdfield.com'
        )


# ---------------------------------------------------------------------------
# Canonical URL metadata
# ---------------------------------------------------------------------------

class TestCanonicalMetadata:
    def test_canonical_link_per_page(self):
        for rel, url in _CANONICAL_URLS.items():
            html = _read(rel)
            tag = f'<link rel="canonical" href="{url}">'
            assert tag in html, f'{rel}: missing or wrong canonical tag (expected {url})'

    def test_og_url_per_page(self):
        for rel, url in _CANONICAL_URLS.items():
            html = _read(rel)
            tag = f'<meta property="og:url" content="{url}">'
            assert tag in html, f'{rel}: missing or wrong og:url (expected {url})'

    def test_unique_titles(self):
        titles = {}
        for rel in _CANONICAL_PAGES:
            html = _read(rel)
            m = re.search(r'<title>([^<]+)</title>', html)
            assert m, f'{rel}: no <title> tag found'
            title = m.group(1)
            assert title not in titles, (
                f'Duplicate title {title!r} in {rel} and {titles[title]}'
            )
            titles[title] = rel

    def test_og_title_present_per_page(self):
        for rel in _CANONICAL_PAGES:
            html = _read(rel)
            assert '<meta property="og:title"' in html, f'{rel}: missing og:title'

    def test_twitter_card_present_per_page(self):
        for rel in _CANONICAL_PAGES:
            html = _read(rel)
            assert '<meta name="twitter:card"' in html, f'{rel}: missing twitter:card'

    def test_canonical_not_on_legacy_stubs(self):
        # Legacy stubs should have canonical pointing to the new directory URL,
        # but also noindex so they are not themselves indexed.
        for stub, target in _LEGACY_TARGETS.items():
            html = _read(stub)
            assert 'noindex' in html, f'{stub}: missing noindex directive'
            # canonical points to the live URL on theblackbirdfield.com
            assert 'theblackbirdfield.com' in html, f'{stub}: no canonical domain in stub'


# ---------------------------------------------------------------------------
# Sitemap and robots
# ---------------------------------------------------------------------------

class TestSitemap:
    def test_sitemap_has_nine_urls(self):
        xml = (DIST / 'sitemap.xml').read_text()
        locs = re.findall(r'<loc>([^<]+)</loc>', xml)
        assert len(locs) == 9, f'Expected 9 sitemap URLs, got {len(locs)}: {locs}'

    def test_sitemap_urls_use_correct_domain(self):
        xml = (DIST / 'sitemap.xml').read_text()
        locs = re.findall(r'<loc>([^<]+)</loc>', xml)
        for loc in locs:
            assert loc.startswith('https://theblackbirdfield.com/'), (
                f'Sitemap URL uses wrong domain: {loc}'
            )

    def test_sitemap_urls_match_canonical_routes(self):
        xml = (DIST / 'sitemap.xml').read_text()
        locs = set(re.findall(r'<loc>([^<]+)</loc>', xml))
        expected = set(_CANONICAL_URLS.values())
        assert locs == expected, (
            f'Sitemap mismatch.\nExtra in sitemap: {locs - expected}\n'
            f'Missing from sitemap: {expected - locs}'
        )

    def test_sitemap_does_not_include_runtime(self):
        xml = (DIST / 'sitemap.xml').read_text()
        assert 'grave-machine/run' not in xml, 'Grave runtime URL must not appear in sitemap'

    def test_sitemap_does_not_include_legacy_stubs(self):
        xml = (DIST / 'sitemap.xml').read_text()
        for stub in _LEGACY_STUBS:
            assert stub not in xml, f'Legacy stub {stub} must not appear in sitemap'


class TestRobots:
    def test_robots_points_to_sitemap(self):
        txt = (DIST / 'robots.txt').read_text()
        assert 'Sitemap: https://theblackbirdfield.com/sitemap.xml' in txt

    def test_robots_allows_all(self):
        txt = (DIST / 'robots.txt').read_text()
        assert 'Allow: /' in txt


# ---------------------------------------------------------------------------
# Legacy redirect stubs
# ---------------------------------------------------------------------------

class TestLegacyRedirects:
    def test_each_stub_has_meta_refresh(self):
        for stub, target in _LEGACY_TARGETS.items():
            html = _read(stub)
            assert f'content="0;url={target}"' in html, (
                f'{stub}: meta-refresh not pointing to {target}'
            )

    def test_each_stub_has_location_replace(self):
        for stub, target in _LEGACY_TARGETS.items():
            html = _read(stub)
            assert f"'{target}'" in html, (
                f"{stub}: location.replace not found for target {target}"
            )

    def test_each_stub_has_noindex(self):
        for stub in _LEGACY_STUBS:
            html = _read(stub)
            assert 'noindex' in html, f'{stub}: missing noindex directive'

    def test_each_stub_has_fallback_link(self):
        for stub, target in _LEGACY_TARGETS.items():
            html = _read(stub)
            assert f'href="{target}"' in html, (
                f'{stub}: no fallback <a href="{target}"> found'
            )


# ---------------------------------------------------------------------------
# Build determinism
# ---------------------------------------------------------------------------

class TestBuildIsDeterministic:
    def test_rebuild_produces_same_pages(self):
        first = (DIST / 'works' / 'index.html').read_bytes()
        subprocess.run([sys.executable, str(SRC / 'build.py')], check=True, capture_output=True)
        second = (DIST / 'works' / 'index.html').read_bytes()
        assert first == second, 'Build is not deterministic for works/index.html'


# ---------------------------------------------------------------------------
# Image assets
# ---------------------------------------------------------------------------

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
