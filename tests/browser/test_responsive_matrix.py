"""Responsive matrix checks across the required viewport set (Section 11.3).

Run: python -m pytest tests/browser/test_responsive_matrix.py -v
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

VIEWPORTS = [
    {'width': 360, 'height': 800}, {'width': 390, 'height': 844}, {'width': 412, 'height': 915},
    {'width': 768, 'height': 1024}, {'width': 1024, 'height': 768}, {'width': 1440, 'height': 900},
    {'width': 1920, 'height': 1080},
]
VIEWPORT_IDS = [f"{v['width']}x{v['height']}" for v in VIEWPORTS]

CANONICAL_PATHS = [
    '/', '/works/', '/works/the-black-bird/', '/works/winter-road/',
    '/works/unhappy-scenario/', '/works/grave-machine/', '/works/taroke-remixer/',
    '/practice/', '/about/', '/contact/',
]


@pytest.fixture(scope='module', autouse=True)
def build_once():
    subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py'), '--check'], cwd=ROOT, check=True)


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


@pytest.mark.parametrize('path', CANONICAL_PATHS)
@pytest.mark.parametrize('viewport', VIEWPORTS, ids=VIEWPORT_IDS)
def test_no_horizontal_overflow(playwright_browser, server, path, viewport):
    page = playwright_browser.new_page(viewport=viewport)
    page.goto(server + path)
    scroll_width = page.evaluate('document.documentElement.scrollWidth')
    client_width = page.evaluate('document.documentElement.clientWidth')
    assert scroll_width <= client_width + 1, f'{path} @ {viewport}: {scroll_width} > {client_width}'
    assert page.locator('h1').count() == 1
    page.close()


@pytest.mark.parametrize('viewport', VIEWPORTS, ids=VIEWPORT_IDS)
def test_home_nav_pattern_matches_breakpoint(playwright_browser, server, viewport):
    page = playwright_browser.new_page(viewport=viewport)
    page.goto(server + '/')
    wide = viewport['width'] > 1100
    assert page.locator('.desktop-nav').is_visible() == wide
    assert page.locator('.menu-toggle').is_visible() != wide
    page.close()


@pytest.mark.parametrize('viewport', VIEWPORTS, ids=VIEWPORT_IDS)
def test_home_hero_preview_hidden_at_760_and_below(playwright_browser, server, viewport):
    page = playwright_browser.new_page(viewport=viewport)
    page.goto(server + '/')
    if viewport['width'] <= 760:
        assert not page.locator('.hero-preview').is_visible()
    else:
        assert page.locator('.hero-preview').is_visible()
    page.close()
