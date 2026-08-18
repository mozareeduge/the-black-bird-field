"""
Automated accessibility checks (axe-core via axe-playwright-python).

Run: python -m pytest tests/browser/test_accessibility.py -v

Zero serious/critical violations is the release gate (Section 8.5).
Automated results never substitute for manual keyboard/focus/zoom/
screen-reader inspection.
"""

import subprocess
import sys
import threading
import http.server
import socketserver
import socket as _socket
from pathlib import Path

import pytest
from axe_playwright_python.sync_playwright import Axe

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'

CANONICAL_PATHS = [
    '/', '/works/', '/works/the-black-bird/', '/works/winter-road/',
    '/works/unhappy-scenario/', '/works/grave-machine/', '/works/taroke-remixer/',
    '/practice/', '/about/', '/contact/',
]
VIEWPORTS = [{'width': 1440, 'height': 900}, {'width': 390, 'height': 844}]


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


@pytest.mark.parametrize('path', CANONICAL_PATHS)
@pytest.mark.parametrize('viewport', VIEWPORTS, ids=['desktop', 'mobile'])
def test_zero_serious_or_critical_violations(playwright_browser, server, path, viewport):
    page = playwright_browser.new_page(viewport=viewport)
    page.goto(server + path)
    axe = Axe()
    results = axe.run(page)
    violations = results.response.get('violations', [])
    serious_critical = [v for v in violations if v['impact'] in ('serious', 'critical')]
    assert not serious_critical, (
        f'{path} @ {viewport}: '
        + '; '.join(f"{v['id']} ({v['impact']}): {v['help']}" for v in serious_critical)
    )
    page.close()
