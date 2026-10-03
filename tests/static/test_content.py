from src.content import load_works, load_site, load_protected_artifacts
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
WORKS=ROOT/'content/works'

def load():
    return sorted((json.loads(p.read_text(encoding='utf8')) for p in WORKS.glob('*.json')),key=lambda x:x['order'])

def test_foundational_five_preserve_order_and_identity():
    slugs=[w['slug'] for w in load()]
    # Canonical slug is taroko-remixer; the old taroke-remixer slug is kept
    # only as a LEGACY redirect (src/build.py) so either value is accepted
    # at position five, but exactly one of them must be present.
    assert slugs[:4]==['the-black-bird','winter-road','unhappy-scenario','grave-machine']
    assert slugs[4] in ('taroko-remixer','taroke-remixer'), slugs
    assert len(slugs)>=5

def test_unique_order_and_identity():
    works=load(); assert len({w['order'] for w in works})==len(works); assert len({w['slug'] for w in works})==len(works)
    for w in works:
        assert w['responsibility'].strip() and w['summary'].strip() and w['meta_description'].strip()
        assert w['live_url'].startswith('https://') and w['repository_url'].startswith('https://github.com/')

def test_upstream_identity_facts_locked():
    by={w['slug']:w for w in load()}
    # Accept both the canonical taroko-remixer slug and the legacy
    # taroke-remixer slug for the fifth-work identity facts.
    fifth=by.get('taroko-remixer', by.get('taroke-remixer'))
    assert '5972b2b' in by['the-black-bird']['identity']['edition']
    assert 'v1.0.1' in by['winter-road']['identity']['edition']
    assert 'v2.6.0' in by['unhappy-scenario']['identity']['edition'] and '9f013ba' in by['unhappy-scenario']['identity']['edition']
    assert 'v1.1.1' in by['grave-machine']['identity']['edition'] and '6940d2e' in by['grave-machine']['identity']['edition']
    assert 'v1.0.4' in fifth['identity']['edition']

def test_citations_follow_one_pattern():
    # Zare, Mohammad (Mozare). *Title*. Version X, 2026. <URL>
    import re
    for w in load():
        c=w['citation']
        assert c['author']=='Zare, Mohammad (Mozare).', w['slug']
        assert re.fullmatch(r'Version [0-9][0-9.]*, 20[0-9]{2}\. https://\S+', c['rest']), (w['slug'], c['rest'])
        assert c['rest'].endswith(w['live_url']), w['slug']

def test_citation_titles_match_upstream_records():
    by={w['slug']:w for w in load()}
    assert by['the-black-bird']['citation']['title']=='The Black Bird: A Hypergraph Research Poem'
    assert by['winter-road']['citation']['title']=='Winter Road: A Haiga Space'
    assert by['unhappy-scenario']['citation']['title']=='UNHAPPY Scenario: An Internet Blackout Poem'
    assert by['grave-machine']['citation']['title']=='Grave-Machine: An Iranian Remix of Taroko Gorge'


def test_runtime_loader_validates_complete_current_content():
    assert len(load_works())>=5
    assert load_site()["documents"]["cv"]["path"]=="documents/Mohammad_Zare_AcademicCV.pdf"
    a=load_protected_artifacts()
    assert a["baseline_commit"]
    assert a["artifacts"]["academic_cv"]["git_blob_sha1"]
