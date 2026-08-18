import json, shutil, subprocess, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]

def test_sixth_work_is_one_record_plus_assets(tmp_path):
    clone=tmp_path/'repo'
    shutil.copytree(ROOT,clone,ignore=shutil.ignore_patterns('dist','validation','.pytest_cache','__pycache__'))
    subprocess.run([sys.executable,'scripts/add_work.py','--slug','test-sixth','--title','Test Sixth','--form','A test work','--mode','Test'],cwd=clone,check=True,capture_output=True,text=True)
    p=clone/'content/works/test-sixth.json'; d=json.loads(p.read_text(encoding='utf8'))
    def resolve(v):
        if isinstance(v,dict): return {k:resolve(x) for k,x in v.items()}
        if isinstance(v,list): return [resolve(x) for x in v]
        if isinstance(v,str) and 'TODO' in v: return v.replace('TODO: ','').replace('TODO','Test authored value')
        return v
    d=resolve(d); d['live_url']='https://example.com/test-sixth/'; d['repository_url']='https://github.com/example/test-sixth'
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    src=clone/'public/assets/black-bird'; dst=clone/'public/assets/test-sixth'
    for role,source_role in [('poster','poster'),('view-01','view-first_frame'),('view-02','view-midpoint'),('view-03','view-last_change')]:
        for size in ('desktop','mobile'):
            shutil.copy2(src/f'{source_role}-{size}.webp',dst/f'{role}-{size}.webp')
    subprocess.run([sys.executable,'src/build.py','--package-preview'],cwd=clone,check=True,capture_output=True,text=True)
    home=BeautifulSoup((clone/'dist/index.html').read_text(encoding='utf8'),'html.parser')
    assert len(home.select('[data-preview-index]'))==6
    assert len(home.select('[data-preview-frame]'))==6
    assert [x['data-work-slug'] for x in home.select('[data-preview-index]')]==[x['data-work-slug'] for x in home.select('[data-preview-frame]')]
    assert 'Six works' in home.get_text(' ',strip=True)
    assert (clone/'dist/works/test-sixth/index.html').is_file()
    assert 'https://theblackbirdfield.com/works/test-sixth/' in (clone/'dist/sitemap.xml').read_text()


def test_twelve_works_build_from_manifests_without_shared_code_changes(tmp_path):
    clone=tmp_path/'repo12'
    shutil.copytree(ROOT,clone,ignore=shutil.ignore_patterns('dist','validation','.pytest_cache','__pycache__'))
    src=clone/'public/assets/black-bird'
    for n in range(6,13):
        slug=f'test-work-{n}'
        subprocess.run([sys.executable,'scripts/add_work.py','--slug',slug,'--title',f'Test Work {n}','--form','A test work','--mode','Test'],cwd=clone,check=True,capture_output=True,text=True)
        p=clone/f'content/works/{slug}.json'; d=json.loads(p.read_text(encoding='utf8'))
        def resolve(v):
            if isinstance(v,dict): return {k:resolve(x) for k,x in v.items()}
            if isinstance(v,list): return [resolve(x) for x in v]
            if isinstance(v,str) and 'TODO' in v: return v.replace('TODO: ','').replace('TODO','Test authored value')
            return v
        d=resolve(d); d['live_url']=f'https://example.com/{slug}/'; d['repository_url']=f'https://github.com/example/{slug}'
        p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        dst=clone/f'public/assets/{slug}'
        for role,source_role in [('poster','poster'),('view-01','view-first_frame'),('view-02','view-midpoint'),('view-03','view-last_change')]:
            for size in ('desktop','mobile'): shutil.copy2(src/f'{source_role}-{size}.webp',dst/f'{role}-{size}.webp')
    subprocess.run([sys.executable,'src/build.py','--package-preview'],cwd=clone,check=True,capture_output=True,text=True)
    home=BeautifulSoup((clone/'dist/index.html').read_text(encoding='utf8'),'html.parser')
    assert len(home.select('[data-preview-index]'))==12
    assert len(home.select('[data-preview-frame]'))==12
    assert 'Twelve works' in home.get_text(' ',strip=True)
    assert all((clone/f'dist/works/test-work-{n}/index.html').is_file() for n in range(6,13))
