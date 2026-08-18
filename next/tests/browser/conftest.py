"""Shared Playwright browser fixture for tests/browser/.

A single sync_playwright() context for the whole session avoids the
"Sync API inside the asyncio loop" conflict that occurs when multiple
browser test modules each try to open their own context.
"""
import os
from pathlib import Path

import pytest

_LOCAL_CHROMIUM = '/opt/pw-browsers/chromium'
_USE_LOCAL_CHROMIUM = Path(_LOCAL_CHROMIUM).exists()
if _USE_LOCAL_CHROMIUM:
    os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')


@pytest.fixture(scope='session')
def playwright_browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        kwargs = {'headless': True}
        if _USE_LOCAL_CHROMIUM:
            kwargs['executable_path'] = _LOCAL_CHROMIUM
        browser = p.chromium.launch(**kwargs)
        yield browser
        browser.close()
