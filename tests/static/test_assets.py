"""Asset manifest and image-budget checks (R-ASSET-AUTHENTICITY, R-PERFORMANCE).

Run: python -m pytest tests/static/test_assets.py -v
"""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'

OTHER_DESKTOP_IMAGE_BUDGET = 300 * 1024
OTHER_MOBILE_IMAGE_BUDGET = 160 * 1024


@pytest.fixture(scope='module', autouse=True)
def built():
    subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py')], cwd=ROOT, check=True)


def test_validate_asset_manifest_script_passes():
    result = subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'validate_asset_manifest.py')],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.startswith('PASS')


def test_desktop_portfolio_images_within_budget():
    for path in (DIST / 'assets').glob('*/portfolio/*.png'):
        if 'mobile' in path.name:
            continue
        assert path.stat().st_size <= OTHER_DESKTOP_IMAGE_BUDGET, (
            f'{path.relative_to(DIST)}: {path.stat().st_size} bytes exceeds {OTHER_DESKTOP_IMAGE_BUDGET}'
        )


def test_mobile_portfolio_images_within_budget():
    for path in (DIST / 'assets').glob('*/portfolio/*mobile*.png'):
        assert path.stat().st_size <= OTHER_MOBILE_IMAGE_BUDGET, (
            f'{path.relative_to(DIST)}: {path.stat().st_size} bytes exceeds {OTHER_MOBILE_IMAGE_BUDGET}'
        )
