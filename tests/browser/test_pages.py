"""
Browser tests using Playwright/Chromium.

Run: python -m pytest tests/browser/ -v
Requires: pip install playwright pytest-playwright

In the Claude Code remote execution environment, Chromium is pre-installed at
/opt/pw-browsers/chromium and we use it directly. On CI (GitHub Actions) the
workflow runs `playwright install chromium --with-deps` which puts the browser
in Playwright's default cache; we let Playwright discover it automatically.
"""

import os
import threading
import http.server
import pytest
from pathlib import Path

# Pre-built binary path used in the Claude Code remote execution environment.
_LOCAL_CHROMIUM = '/opt/pw-browsers/chromium'
_USE_LOCAL_CHROMIUM = Path(_LOCAL_CHROMIUM).exists()

if _USE_LOCAL_CHROMIUM:
    os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'

# GitHub Pages project subpath — the live deployment base.
SUBPATH_PREFIX = '/the-black-bird-field'

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope='session')
def static_server():
    """Serve dist/ on a randomly assigned free port.

    Handles requests at both / (root) and /the-black-bird-field/ (the live
    GitHub Pages project subpath), so tests can exercise both origins against
    the same build without a second server process.
    """
    import socketserver
    import socket as _socket

    class _Handler(http.server.SimpleHTTPRequestHandler):
        extensions_map = {
            '': 'application/octet-stream',
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.png': 'image/png',
            '.pdf': 'application/pdf',
        }

        def translate_path(self, path):
            # Serve dist/ at both / and /the-black-bird-field/.
            if path == SUBPATH_PREFIX or path.startswith(SUBPATH_PREFIX + '/'):
                path = path[len(SUBPATH_PREFIX):] or '/'
            return super().translate_path(path)

        def log_message(self, *args):
            pass

    os.chdir(str(DIST))
    with _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        port = s.getsockname()[1]

    httpd = socketserver.TCPServer(('', port), _Handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    yield f'http://localhost:{port}'
    httpd.shutdown()


@pytest.fixture(scope='session')
def subpath_url(static_server):
    """The subpath base URL that mirrors the live GitHub Pages deployment."""
    return static_server + SUBPATH_PREFIX


@pytest.fixture(scope='session')
def browser_context(static_server):
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    launch_kwargs = {'executable_path': _LOCAL_CHROMIUM} if _USE_LOCAL_CHROMIUM else {}
    browser = pw.chromium.launch(**launch_kwargs)
    context = browser.new_context()
    yield context
    context.close()
    browser.close()
    pw.stop()


@pytest.fixture
def page(browser_context):
    p = browser_context.new_page()
    yield p
    p.close()


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------

class TestHomePage:
    def test_title(self, page, static_server):
        page.goto(static_server + '/')
        assert page.title() == 'The Black Bird Field — Works by Mozare'

    def test_h1(self, page, static_server):
        page.goto(static_server + '/')
        assert page.locator('h1').first.inner_text() == 'The Black Bird Field'

    def test_four_works_listed(self, page, static_server):
        page.goto(static_server + '/')
        body = page.locator('body').inner_text()
        for work in ['The Black Bird', 'Winter Road', 'Grave-Machine', 'TAROKE RIMIXER']:
            assert work in body

    def test_sticky_header_visible(self, page, static_server):
        page.goto(static_server + '/')
        assert page.locator('header.site-header').is_visible()

    def test_skip_link_accessible(self, page, static_server):
        page.goto(static_server + '/')
        skip = page.locator('a.skip-link')
        assert skip.count() == 1

    def test_grave_launch_link_target(self, page, static_server):
        # Grave-Machine launch link from home goes to the runtime, not the project page.
        page.goto(static_server + '/')
        links = page.locator('a[href="works/grave-machine/run/"]')
        assert links.count() >= 1

    def test_grave_project_page_link_present(self, page, static_server):
        page.goto(static_server + '/')
        links = page.locator('a[href="works/grave-machine/"]')
        assert links.count() >= 1


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

class TestNavigation:
    def test_works_page_reachable(self, page, static_server):
        page.goto(static_server + '/')
        page.locator('a[href="works/"]').first.click()
        page.wait_for_load_state('load')
        assert 'Works' in page.title()

    def test_black_bird_page_reachable(self, page, static_server):
        page.goto(static_server + '/works/the-black-bird/')
        assert page.locator('h1').first.inner_text() == 'The Black Bird'

    def test_grave_machine_page_reachable(self, page, static_server):
        page.goto(static_server + '/works/grave-machine/')
        assert 'Grave-Machine' in page.title()

    def test_grave_runtime_loads(self, page, static_server):
        page.goto(static_server + '/works/grave-machine/run/')
        assert 'Grave-Machine' in page.title()
        assert 'گور' in page.title()

    def test_works_page_has_four_entries(self, page, static_server):
        page.goto(static_server + '/works/')
        work_nos = page.locator('.work-no')
        assert work_nos.count() >= 4

    def test_wordmark_returns_home(self, page, static_server):
        page.goto(static_server + '/works/')
        page.locator('a.wordmark').first.click()
        page.wait_for_load_state('load')
        assert page.title() == 'The Black Bird Field — Works by Mozare'


# ---------------------------------------------------------------------------
# Mobile menu
# ---------------------------------------------------------------------------

class TestMobileMenu:
    def test_menu_toggle_visible_at_mobile(self, page, static_server):
        page.set_viewport_size({'width': 375, 'height': 812})
        page.goto(static_server + '/')
        toggle = page.locator('button[data-menu-open]')
        assert toggle.is_visible()

    def test_menu_opens(self, page, static_server):
        page.set_viewport_size({'width': 375, 'height': 812})
        page.goto(static_server + '/')
        page.locator('button[data-menu-open]').click()
        page.wait_for_selector('dialog[data-menu-dialog][open]', timeout=3000)
        assert page.locator('dialog[data-menu-dialog]').is_visible()

    def test_menu_closes(self, page, static_server):
        page.set_viewport_size({'width': 375, 'height': 812})
        page.goto(static_server + '/')
        page.locator('button[data-menu-open]').click()
        page.wait_for_selector('dialog[data-menu-dialog][open]', timeout=3000)
        page.locator('button[data-menu-close]').click()
        toggle = page.locator('button[data-menu-open]')
        page.wait_for_function(
            "() => document.querySelector('[data-menu-open]').getAttribute('aria-expanded') === 'false'",
            timeout=3000,
        )
        assert toggle.get_attribute('aria-expanded') == 'false'

    def test_desktop_nav_hidden_at_mobile(self, page, static_server):
        page.set_viewport_size({'width': 375, 'height': 812})
        page.goto(static_server + '/')
        desktop_nav = page.locator('nav.desktop-nav')
        assert not desktop_nav.is_visible()


# ---------------------------------------------------------------------------
# CV download
# ---------------------------------------------------------------------------

class TestCVDownload:
    def test_cv_download_link_present_on_home(self, page, static_server):
        page.set_viewport_size({'width': 1280, 'height': 800})
        page.goto(static_server + '/')
        cv_links = page.locator('[data-cv-download]')
        assert cv_links.count() >= 1

    def test_cv_not_present_on_contact(self, page, static_server):
        page.set_viewport_size({'width': 1280, 'height': 800})
        page.goto(static_server + '/contact/')
        cv_in_header = page.locator('header [data-cv-download]')
        assert cv_in_header.count() == 0

    def test_cv_download_does_not_navigate(self, page, static_server):
        page.set_viewport_size({'width': 1280, 'height': 800})
        page.goto(static_server + '/')
        original_url = page.url
        downloads = []
        page.on('download', lambda d: downloads.append(d))
        cv_link = page.locator('[data-cv-download]').first
        cv_link.click()
        page.wait_for_timeout(1500)
        assert page.url == original_url, 'CV click should not navigate'
        assert len(downloads) == 1, f'Expected 1 download, got {len(downloads)}'


# ---------------------------------------------------------------------------
# Accessibility
# ---------------------------------------------------------------------------

class TestAccessibility:
    def test_focus_visible_skip_link(self, page, static_server):
        page.goto(static_server + '/')
        page.keyboard.press('Tab')
        skip = page.locator('a.skip-link')
        assert skip.is_visible()

    def test_all_images_have_alt(self, page, static_server):
        page.goto(static_server + '/')
        imgs = page.locator('img')
        for i in range(imgs.count()):
            alt = imgs.nth(i).get_attribute('alt')
            assert alt is not None, f'img #{i} missing alt attribute'

    def test_aria_current_on_nav(self, page, static_server):
        page.goto(static_server + '/works/')
        current = page.locator('[aria-current="page"]')
        assert current.count() >= 1


# ---------------------------------------------------------------------------
# State atlas
# ---------------------------------------------------------------------------

class TestStateAtlas:
    def test_atlas_tabs_present_on_black_bird(self, page, static_server):
        page.goto(static_server + '/works/the-black-bird/')
        tabs = page.locator('[role="tab"]')
        assert tabs.count() >= 3

    def test_atlas_tab_switch(self, page, static_server):
        page.goto(static_server + '/works/the-black-bird/')
        tabs = page.locator('[role="tab"]')
        initial_src = page.locator('[data-state-image]').first.get_attribute('src')
        if tabs.count() > 1:
            tabs.nth(1).click()
            new_src = page.locator('[data-state-image]').first.get_attribute('src')
            assert new_src != initial_src, 'Atlas image did not change on tab click'


# ---------------------------------------------------------------------------
# Links and routes
# ---------------------------------------------------------------------------

class TestLinksAndRoutes:
    def test_work_pages_all_load(self, page, static_server):
        pages = [
            '/works/the-black-bird/', '/works/winter-road/',
            '/works/grave-machine/', '/works/taroke-remixer/',
        ]
        for path in pages:
            page.goto(static_server + path)
            assert page.locator('h1').first.is_visible(), f'{path}: h1 not visible'

    def test_linkedin_link_present(self, page, static_server):
        page.goto(static_server + '/')
        li = page.locator('a[href*="linkedin.com"]')
        assert li.count() >= 1

    def test_black_bird_poem_subdomain_link_present(self, page, static_server):
        # The Black Bird launch link must point to the custom poem subdomain.
        page.goto(static_server + '/works/the-black-bird/')
        link = page.locator('a[href="https://poem.theblackbirdfield.com/"]')
        assert link.count() >= 1

    def test_taroke_external_link_present(self, page, static_server):
        page.goto(static_server + '/works/taroke-remixer/')
        link = page.locator('a[href="https://mozareeduge.github.io/taroke-remixer/"]')
        assert link.count() >= 1

    def test_legacy_stubs_redirect_within_site(self, page, static_server):
        # Each legacy stub should redirect (via JS) before Playwright's load event.
        stubs = {
            '/works.html': '/works/',
            '/about.html': '/about/',
            '/practice.html': '/practice/',
        }
        for stub, expected_suffix in stubs.items():
            page.goto(static_server + stub, wait_until='networkidle')
            assert page.url.endswith(expected_suffix), (
                f'{stub} did not redirect to {expected_suffix}; final URL: {page.url}'
            )


# ---------------------------------------------------------------------------
# Subpath deployment verification
# Mirrors the live GitHub Pages URL: /the-black-bird-field/
# ---------------------------------------------------------------------------

class TestSubpathDeployment:
    """Verify the full site operates correctly under /the-black-bird-field/.

    All asset references in the generated HTML are document-relative, so they
    resolve correctly whether the page is served at / or at a project subpath.
    These tests confirm that invariant holds in a live browser against the
    same build artifact that CI and GitHub Pages use.
    """

    def test_home_title_at_subpath(self, page, subpath_url):
        page.goto(subpath_url + '/')
        assert page.title() == 'The Black Bird Field — Works by Mozare'

    def test_header_visible_at_subpath(self, page, subpath_url):
        page.goto(subpath_url + '/')
        assert page.locator('header.site-header').is_visible()

    def test_four_works_at_subpath(self, page, subpath_url):
        page.goto(subpath_url + '/')
        body = page.locator('body').inner_text()
        for work in ['The Black Bird', 'Winter Road', 'Grave-Machine', 'TAROKE RIMIXER']:
            assert work in body

    def test_all_portfolio_pages_load_at_subpath(self, page, subpath_url):
        paths = [
            '/works/', '/works/the-black-bird/', '/works/winter-road/',
            '/works/grave-machine/', '/works/taroke-remixer/',
            '/practice/', '/about/', '/contact/',
        ]
        for path in paths:
            page.goto(subpath_url + path)
            assert page.locator('h1').first.is_visible(), f'{path}: h1 not visible at subpath'

    def test_grave_runtime_loads_at_subpath(self, page, subpath_url):
        page.goto(subpath_url + '/works/grave-machine/run/')
        assert 'Grave-Machine' in page.title()
        assert 'گور' in page.title()

    def test_nav_links_resolve_at_subpath(self, page, subpath_url):
        page.goto(subpath_url + '/')
        page.locator('a[href="works/"]').first.click()
        page.wait_for_load_state('load')
        assert 'Works' in page.title()
        # Navigate back via the wordmark
        page.locator('a.wordmark').first.click()
        page.wait_for_load_state('load')
        assert page.title() == 'The Black Bird Field — Works by Mozare'

    def test_grave_launch_link_resolves_at_subpath(self, page, subpath_url):
        page.goto(subpath_url + '/')
        links = page.locator('a[href="works/grave-machine/run/"]')
        assert links.count() >= 1

    def test_cv_download_at_subpath(self, page, subpath_url):
        page.set_viewport_size({'width': 1280, 'height': 800})
        page.goto(subpath_url + '/')
        original_url = page.url
        downloads = []
        page.on('download', lambda d: downloads.append(d))
        page.locator('[data-cv-download]').first.click()
        page.wait_for_timeout(1500)
        assert page.url == original_url, 'CV click should not navigate at subpath'
        assert len(downloads) == 1, f'Expected 1 download, got {len(downloads)}'

    def test_no_failed_asset_requests_at_subpath(self, page, subpath_url):
        failed = []
        page.on('response', lambda r: failed.append((r.url, r.status)) if r.status >= 400 else None)
        page.goto(subpath_url + '/')
        page.wait_for_load_state('networkidle')
        assert not failed, f'Failed asset requests under subpath: {failed}'

    def test_skip_link_at_subpath(self, page, subpath_url):
        page.goto(subpath_url + '/')
        assert page.locator('a.skip-link').count() == 1

    def test_mobile_menu_at_subpath(self, page, subpath_url):
        page.set_viewport_size({'width': 375, 'height': 812})
        page.goto(subpath_url + '/')
        page.locator('button[data-menu-open]').click()
        page.wait_for_selector('dialog[data-menu-dialog][open]', timeout=3000)
        assert page.locator('dialog[data-menu-dialog]').is_visible()
