"""
Capture representative desktop and mobile screenshots from the
Grave-Machine bilingual v1.1 runtime.

Usage:
    python scripts/capture_grave.py

Requires: playwright (pip install playwright)
Output: public/assets/grave-machine/bilingual/
"""

import os
import sys
import time
from pathlib import Path

os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')

ROOT = Path(__file__).resolve().parents[1]
GRAVE_HTML = ROOT / 'public' / 'works' / 'grave-machine' / 'index.html'
OUT_DIR = ROOT / 'public' / 'assets' / 'grave-machine' / 'bilingual'


def capture():
    from playwright.sync_api import sync_playwright

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    url = GRAVE_HTML.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')

        # Desktop captures
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto(url)
        page.wait_for_load_state('networkidle')
        time.sleep(4)
        page.screenshot(path=str(OUT_DIR / 'desktop_04s.png'))
        print('  desktop_04s.png')

        time.sleep(10)
        page.screenshot(path=str(OUT_DIR / 'desktop_14s.png'))
        print('  desktop_14s.png')

        time.sleep(8)
        page.screenshot(path=str(OUT_DIR / 'desktop_22s.png'))
        print('  desktop_22s.png')

        # Open statement if possible
        statement_btn = page.locator('[data-statement-toggle], #statement-toggle, .statement-toggle').first
        if statement_btn.is_visible():
            statement_btn.click()
            time.sleep(1)
            page.screenshot(path=str(OUT_DIR / 'desktop_statement.png'))
            print('  desktop_statement.png')

        # Mobile captures
        page.set_viewport_size({'width': 390, 'height': 844})
        page.goto(url)
        page.wait_for_load_state('networkidle')
        time.sleep(4)
        page.screenshot(path=str(OUT_DIR / 'mobile_04s.png'))
        print('  mobile_04s.png')

        time.sleep(10)
        page.screenshot(path=str(OUT_DIR / 'mobile_14s.png'))
        print('  mobile_14s.png')

        time.sleep(6)
        page.screenshot(path=str(OUT_DIR / 'mobile_20s.png'))
        print('  mobile_20s.png')

        browser.close()

    print(f'\nCaptured to: {OUT_DIR}')
    print('Update src/pages/grave-machine.html atlas image paths if needed.')


if __name__ == '__main__':
    capture()
