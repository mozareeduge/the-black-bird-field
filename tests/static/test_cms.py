"""CMS field coverage protects JSON content from silent loss on editor saves."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / 'public/admin/config.json').read_text(encoding='utf-8'))


def covered(value, fields, path=''):
    by_name = {field['name']: field for field in fields}
    assert set(value) <= set(by_name), f'unmapped CMS fields at {path}: {set(value) - set(by_name)}'
    for name, child in value.items():
        field = by_name[name]
        if isinstance(child, dict):
            assert field['widget'] == 'object', f'{path}.{name}'
            covered(child, field['fields'], f'{path}.{name}')
        elif isinstance(child, list):
            assert field['widget'] == 'list', f'{path}.{name}'
            for item in child:
                if isinstance(item, dict):
                    covered(item, field['fields'], f'{path}.{name}[]')
                else:
                    assert 'field' in field, f'{path}.{name}[] needs a scalar subfield'


def test_cms_maps_current_site_and_every_work_field():
    site = CONFIG['collections'][0]['files'][0]
    assert site['file'] == 'content/site.json'
    covered(json.loads((ROOT / site['file']).read_text(encoding='utf-8')), site['fields'], 'site')
    works = CONFIG['collections'][1]
    assert works['folder'] == 'content/works'
    assert works['create'] is False and works['delete'] is False
    for path in (ROOT / works['folder']).glob('*.json'):
        covered(json.loads(path.read_text(encoding='utf-8')), works['fields'], path.name)
    assert 'protected_artifacts.json' not in json.dumps(CONFIG)


def test_admin_uses_token_auth_and_existing_asset_folder():
    assert CONFIG['backend']['repo'] == 'mozareeduge/the-black-bird-field'
    assert CONFIG['backend']['auth_methods'] == ['token']
    assert CONFIG['media_folder'] == '/public/assets'
    assert CONFIG['public_folder'] == '/assets'
    assert (ROOT / 'dist/admin/index.html').is_file()
    assert (ROOT / 'dist/admin/config.json').read_bytes() == (ROOT / 'public/admin/config.json').read_bytes()
