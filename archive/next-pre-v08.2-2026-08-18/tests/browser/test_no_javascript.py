"""Core content and navigation must work with JavaScript disabled
(R-JS-PROGRESSIVE, R-ACCESSIBILITY, Section 8.2).

Run: python -m pytest tests/browser/test_no_javascript.py -v
"""
import subprocess
import sys
import threading
import http.server
import socketserver
import socket as _socket
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'


@pytest.fixture(scope='module', autouse=True)
def build_once():
    subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py')], cwd=ROOT, check=True)


@pytest.fixture(scope='module')
def server():
    def handler_factory(*args, **kwargs):
        return http.server.SimpleHTTPRequestHandler(*args, directory=str(DIST), **kwargs)
    with _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        port = s.getsockname()[1]
    httpd = socketserver.TCPServer(('', port), handler_factory)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f'http://localhost:{port}'
    httpd.shutdown()


@pytest.fixture
def no_js_page(playwright_browser, server):
    context = playwright_browser.new_context(java_script_enabled=False)
    page = context.new_page()
    yield page
    context.close()


def test_navigation_links_reachable_without_js(server, no_js_page):
    page = no_js_page
    page.goto(server + '/')
    assert page.locator('h1').count() == 1
    href = page.locator('.desktop-nav a, .hero-work-index a').first.get_attribute('href')
    assert href


def test_project_page_loads_and_shows_selected_views_without_js(server, no_js_page):
    page = no_js_page
    page.goto(server + '/works/the-black-bird/')
    assert page.locator('.project-view').count() == 4
    # No inline atlas/tab JS exists to break; all four figures are plain HTML.
    for img in page.locator('.project-view-image').all():
        assert img.get_attribute('src')


def test_mobile_menu_dialog_still_present_and_links_reachable(server, no_js_page):
    page = no_js_page
    page.goto(server + '/')
    # Without JS the dialog cannot be opened via the button, but its links
    # remain valid, reachable anchors in the document.
    links = page.locator('.menu-primary a')
    assert links.count() >= 3
    for i in range(links.count()):
        assert links.nth(i).get_attribute('href')


def test_cv_download_is_a_plain_link_without_js(server, no_js_page):
    page = no_js_page
    page.goto(server + '/about/')
    cv = page.locator('a[download]').first
    href = cv.get_attribute('href')
    assert href and href.endswith('.pdf')


def test_no_script_errors_thrown_when_js_disabled(server, no_js_page):
    page = no_js_page
    errors = []
    page.on('pageerror', lambda exc: errors.append(str(exc)))
    page.goto(server + '/')
    page.goto(server + '/works/')
    assert errors == []
