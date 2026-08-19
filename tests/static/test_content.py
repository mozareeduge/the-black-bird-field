from src.content import load_works, load_site, load_protected_artifacts
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
WORKS=ROOT/'content/works'

def load():
    return sorted((json.loads(p.read_text(encoding='utf8')) for p in WORKS.glob('*.json')),key=lambda x:x['order'])

def test_foundational_five_preserve_order_and_identity():
    slugs=[w['slug'] for w in load()]
    assert slugs[:5]==['the-black-bird','winter-road','unhappy-scenario','grave-machine','taroke-remixer']
    assert len(slugs)>=5

def test_unique_order_and_identity():
    works=load(); assert len({w['order'] for w in works})==len(works); assert len({w['slug'] for w in works})==len(works)
    for w in works:
        assert w['responsibility'].strip() and w['summary'].strip() and w['meta_description'].strip()
        assert w['live_url'].startswith('https://') and w['repository_url'].startswith('https://github.com/')

def test_upstream_identity_facts_locked():
    by={w['slug']:w for w in load()}
    assert '5972b2b' in by['the-black-bird']['identity']['edition']
    assert 'v1.0.1' in by['winter-road']['identity']['edition']
    assert 'v2.6.0' in by['unhappy-scenario']['identity']['edition'] and '9f013ba' in by['unhappy-scenario']['identity']['edition']
    assert 'v1.1.0' in by['grave-machine']['identity']['edition'] and 'b948455' in by['grave-machine']['identity']['edition']
    assert 'development line' in by['taroke-remixer']['identity']['edition'] and 'cb8e5f3' in by['taroke-remixer']['identity']['edition']

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
