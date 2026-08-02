"""Exact copy contract tests (R-COPY-EXACT, R-FIVE-WORK-IA).

Run: python -m pytest tests/static/test_copy_contract.py -v
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'

sys.path.insert(0, str(ROOT / 'src'))
from content import WORK_ORDER, WORKS, PROHIBITED_FORMULAS  # noqa: E402
from site_config import ROUTES  # noqa: E402

STALE_PHRASES = ('State Atlas', 'Encounter Score', 'Four works', 'four browser-native works')


@pytest.fixture(scope='module', autouse=True)
def built():
    subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py')], cwd=ROOT, check=True)


def all_html_files():
    return sorted(DIST.rglob('*.html'))


def canonical_and_alias_pages():
    return {k: m for k, m in ROUTES.items()}


def test_all_five_titles_on_home_and_works():
    for output in ('index.html', 'works/index.html'):
        html = (DIST / output).read_text(encoding='utf-8')
        for key in WORK_ORDER:
            assert WORKS[key]['title'] in html, f'{WORKS[key]["title"]} missing from {output}'


def test_operative_words_match_copy_authority():
    html = (DIST / 'index.html').read_text(encoding='utf-8')
    for key in WORK_ORDER:
        assert WORKS[key]['operative'] in html, key


@pytest.mark.parametrize('key,meta', list(canonical_and_alias_pages().items()))
def test_one_h1_per_page(key, meta):
    html = (DIST / meta['output']).read_text(encoding='utf-8')
    assert len(re.findall(r'<h1[ >]', html)) == 1, f'{key}: expected exactly one <h1>'


def test_unique_titles_and_descriptions_for_canonical_pages():
    canon = {k: m for k, m in ROUTES.items() if m.get('sitemap', True)}
    titles = [m['title'] for m in canon.values()]
    descriptions = [m['description'] for m in canon.values()]
    assert len(titles) == len(set(titles)), titles
    assert len(descriptions) == len(set(descriptions)), descriptions


def test_no_unresolved_template_tokens():
    for path in all_html_files():
        html = path.read_text(encoding='utf-8')
        assert '{{' not in html, f'unresolved token in {path.relative_to(DIST)}'


def test_no_stale_phrases():
    for path in all_html_files():
        html = path.read_text(encoding='utf-8')
        for phrase in STALE_PHRASES:
            assert phrase.lower() not in html.lower(), f'{phrase!r} found in {path.relative_to(DIST)}'


def test_no_prohibited_rhetorical_formulas():
    for path in all_html_files():
        html = path.read_text(encoding='utf-8').lower()
        for formula in PROHIBITED_FORMULAS:
            assert formula not in html, f'{formula!r} found in {path.relative_to(DIST)}'


def test_no_exact_paragraph_reuse_across_designated_surfaces():
    """Home feature copy, Works-index notes, project leads, and project
    contexts must be four separate authored texts per work."""
    for key in WORK_ORDER:
        w = WORKS[key]
        surfaces = {
            'home_feature': w['home_feature']['copy'],
            'works_index_note': w['works_index']['work_note'],
            'project_lead': w['project']['lead'],
        }
        values = list(surfaces.values())
        assert len(values) == len(set(values)), (key, surfaces)
        for para in w['project']['context_paragraphs']:
            assert para not in values, (key, para)


def test_every_work_link_uses_canonical_current_url():
    html = (DIST / 'works' / 'the-black-bird' / 'index.html').read_text(encoding='utf-8')
    assert 'https://poem.theblackbirdfield.com/' in html
    html = (DIST / 'works' / 'unhappy-scenario' / 'index.html').read_text(encoding='utf-8')
    assert 'https://unhappy.theblackbirdfield.com/' in html


def test_unhappy_locked_message_fixture_matches_release_source():
    """The eight system messages are locked inside the artwork itself; the
    portfolio keeps only a byte-identical validation fixture, never a
    rendered copy (R-COPY-EXACT)."""
    fixture = ROOT / 'tests' / 'fixtures' / 'unhappy_procedure_text.txt'
    text = fixture.read_text(encoding='utf-8')
    for line in (
        'Upload failed', 'Sending the message failed', 'Connection attempt failed',
        'Reconnecting…', 'Failed', 'Do you want to report the problem?',
        'Reporting the problem…', 'Reporting failed',
    ):
        assert line in text, line
    assert 'Try again' in text
    import hashlib
    assert hashlib.sha256(fixture.read_bytes()).hexdigest() == (
        'd3ec2fead5ef9a3dff6ab96576d07df506c270153c74e8eddc3a42564ea0cb70'
    )


def test_try_again_separated_from_locked_messages_in_fixture():
    """'Try again' is an interface action outside the eight-message poem
    core; the fixture must keep it in a clearly separate section rather
    than mixed into the locked message list (Section 11.2)."""
    fixture = ROOT / 'tests' / 'fixtures' / 'unhappy_procedure_text.txt'
    text = fixture.read_text(encoding='utf-8')
    messages_section, _, action_section = text.partition('Interface action outside the poem:')
    assert 'Try again' not in messages_section
    assert 'Try again' in action_section
