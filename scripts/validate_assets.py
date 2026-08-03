"""
Validate that all image paths referenced in page fragments exist in public/assets.

Usage:
    python scripts/validate_assets.py

Exit code 0 = all references resolved.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / 'src' / 'pages'
PUBLIC = ROOT / 'public'


def main():
    pattern = re.compile(r'(?:src|srcset)="([^"]*assets/[^"]+\.(?:png|jpg|jpeg|webp|svg))"')
    missing = []

    for page in sorted(PAGES.glob('*.html')):
        text = page.read_text(encoding='utf-8')
        for match in pattern.finditer(text):
            ref = match.group(1)
            asset = PUBLIC / ref
            if not asset.exists():
                missing.append(f'{page.name}: {ref}')

    if missing:
        print(f'MISSING ASSETS ({len(missing)}):')
        for m in missing:
            print(f'  {m}')
        sys.exit(1)
    else:
        print(f'All asset references resolved ({sum(1 for p in PAGES.glob("*.html") for _ in pattern.finditer(p.read_text())) } images across {len(list(PAGES.glob("*.html")))} pages)')


if __name__ == '__main__':
    main()
