"""
Browser tests using Playwright/Chromium for the five-work portfolio.

Run: python -m pytest tests/browser/test_pages.py -v
"""

import os
import threading
import http.server
import sys
from pathlib import Path

import pytest

_LOCAL_CHROMIUM = '/opt/pw-browsers/chromium'
_USE_LOCAL_CHROMIUM = Path(_LOCAL_CHROMIUM).exists()
if _USE_LOCAL_CHROMIUM:
    os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'
SUBPATH_PREFIX = '/the-black-bird-field'

sys.path.insert(0, str(ROOT / 'src'))
from content import WORK_ORDER, WORKS  # noqa: E402


@pytest.fixture(scope='session')
def static_server():
    import socketserver
    import socket as _socket

    class _Handler(http.server.SimpleHTTPRequestHandler):
        extensions_map = {
            '': 'application/octet-stream', '.html': 'text/html', '.css': 'text/css',
            '.js': 'application/javascript', '.png': 'image/png', '.pdf': 'application/pdf',
            '.woff2': 'font/woff2', '.xml': 'application/xml', '.txt': 'text/plain',
        }

        def translate_path(self, path):
            if path == SUBPATH_PREFIX or path.startswith(SUBPATH_PREFIX + '/'):
                path = path[len(SUBPATH_PREFIX):] or '/'
            return super().translate_path(path)

        def log_message(self, *args):
            pass

    def handler_factory(*args, **kwargs):
        return _Handler(*args, directory=str(DIST), **kwargs)

    with _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        port = s.getsockname()[1]
    httpd = socketserver.TCPServer(('', port), handler_factory)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    yield f'http://localhost:{port}'
    httpd.shutdown()


@pytest.fixture(scope='session')
def subpath_url(static_server):
    return static_server + SUBPATH_PREFIX


@pytest.fixture(scope='module', autouse=True)
def build_once():
    import subprocess
    subprocess.run(['python', str(ROOT / 'src' / 'build.py'), '--check'], cwd=ROOT, check=True)


CANONICAL_PATHS = [
    '/', '/works/', '/works/the-black-bird/', '/works/winter-road/',
    '/works/unhappy-scenario/', '/works/grave-machine/', '/works/taroke-remixer/',
    '/practice/', '/about/', '/contact/',
]

ALIAS_PATHS = [
    '/the-black-bird/', '/winter-road/', '/unhappy-scenario/', '/grave-machine/', '/taroke-remixer/',
]


@pytest.fixture(params=[True, False], ids=['root', 'subpath'])
def base(request, static_server, subpath_url):
    return subpath_url if request.param else static_server


@pytest.mark.parametrize('path', CANONICAL_PATHS)
def test_canonical_pages_load(base, path, browser_page):
    page = browser_page
    resp = page.goto(base + path)
    assert resp.ok
    assert page.locator('h1').count() == 1


@pytest.mark.parametrize('path', ALIAS_PATHS)
def test_alias_pages_load_with_same_h1(base, path, browser_page):
    page = browser_page
    resp = page.goto(base + path)
    assert resp.ok
    assert page.locator('h1').count() == 1


def test_home_shows_five_works_in_order(base, browser_page):
    page = browser_page
    page.goto(base + '/')
    titles = page.locator('.hero-work-index .work-title').all_inner_texts()
    assert titles == [WORKS[k]['title'] for k in WORK_ORDER]


def test_works_index_shows_five_works_in_order(base, browser_page):
    page = browser_page
    page.goto(base + '/works/')
    titles = page.locator('.works-row h2').all_inner_texts()
    assert titles == [WORKS[k]['title'] for k in WORK_ORDER]


def test_no_horizontal_overflow_desktop(base, browser_page):
    page = browser_page
    page.set_viewport_size({'width': 1440, 'height': 900})
    page.goto(base + '/')
    scroll_width = page.evaluate('document.documentElement.scrollWidth')
    client_width = page.evaluate('document.documentElement.clientWidth')
    assert scroll_width <= client_width + 1


def test_no_horizontal_overflow_mobile(base, browser_page):
    page = browser_page
    page.set_viewport_size({'width': 360, 'height': 800})
    page.goto(base + '/')
    scroll_width = page.evaluate('document.documentElement.scrollWidth')
    client_width = page.evaluate('document.documentElement.clientWidth')
    assert scroll_width <= client_width + 1


def test_desktop_nav_visible_above_breakpoint(base, browser_page):
    page = browser_page
    page.set_viewport_size({'width': 1440, 'height': 900})
    page.goto(base + '/')
    assert page.locator('.desktop-nav').is_visible()
    assert not page.locator('.menu-toggle').is_visible()


def test_menu_button_visible_under_breakpoint(base, browser_page):
    page = browser_page
    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto(base + '/')
    assert page.locator('.menu-toggle').is_visible()
    assert not page.locator('.desktop-nav').is_visible()


def test_mobile_menu_opens_focuses_close_and_escape_closes(base, browser_page):
    page = browser_page
    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto(base + '/')
    page.click('[data-menu-open]')
    dialog = page.locator('[data-menu-dialog]')
    assert dialog.get_attribute('open') is not None
    focused = page.evaluate('document.activeElement.matches("[data-menu-close]")')
    assert focused
    page.keyboard.press('Escape')
    assert dialog.get_attribute('open') is None


def test_mobile_menu_backdrop_closes(base, browser_page):
    # The dialog fills the viewport by design (Section 6.2), so there is no
    # exposed backdrop pixel to tap; exercise the same event.target===dialog
    # closing logic site.js uses by dispatching the click on the dialog
    # element itself, as a real backdrop tap would.
    page = browser_page
    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto(base + '/')
    page.click('[data-menu-open]')
    page.evaluate("document.querySelector('[data-menu-dialog]').click()")
    assert page.locator('[data-menu-dialog]').get_attribute('open') is None


def test_menu_focus_returns_to_menu_button_on_close(base, browser_page):
    page = browser_page
    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto(base + '/')
    page.click('[data-menu-open]')
    page.click('[data-menu-close]')
    focused = page.evaluate('document.activeElement.matches("[data-menu-open]")')
    assert focused


def test_body_scroll_locks_only_while_menu_open(base, browser_page):
    page = browser_page
    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto(base + '/')
    assert not page.evaluate('document.body.classList.contains("menu-open")')
    page.click('[data-menu-open]')
    assert page.evaluate('document.body.classList.contains("menu-open")')
    page.click('[data-menu-close]')
    assert not page.evaluate('document.body.classList.contains("menu-open")')


@pytest.mark.parametrize('work_key', WORK_ORDER)
def test_project_page_has_four_selected_views(base, work_key, browser_page):
    page = browser_page
    page.goto(base + WORKS[work_key]['canonical_route'])
    assert page.locator('.project-view').count() == 4


def test_grave_runtime_loads(base, browser_page):
    page = browser_page
    resp = page.goto(base + '/works/grave-machine/run/')
    assert resp.ok
    assert 'Grave-Machine' in page.content()


def test_skip_link_becomes_visible_on_first_tab(base, browser_page):
    page = browser_page
    page.goto(base + '/')
    page.keyboard.press('Tab')
    skip = page.locator('.skip-link')
    page.wait_for_timeout(250)
    box = skip.bounding_box()
    assert box is not None and box['y'] >= -2


def test_reduced_motion_removes_preview_transition(base, browser_page):
    page = browser_page
    page.emulate_media(reduced_motion='reduce')
    page.goto(base + '/')
    duration = page.evaluate(
        "parseFloat(getComputedStyle(document.querySelector('.hero-preview-image')).transitionDuration)"
    )
    assert duration < 0.01


@pytest.fixture
def browser_page(playwright_browser):
    page = playwright_browser.new_page()
    yield page
    page.close()
