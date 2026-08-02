"""Route, metadata, and navigation registry for The Black Bird Field.

Canonical and alias routes are generated from src/content.py so the work
registry has exactly one source. See docs/authority/CANONICAL_COPY.md
(Section "Copy authority and use") and the design specification's route
tables (Sections 3.2-3.3) for the frozen route architecture.
"""

from content import (
    SITE_TITLE, SITE_ORIGIN, ARTISTIC_NAME, FORMAL_NAME, CV_FILENAME,
    LINKEDIN_URL, GITHUB_URL, EMAIL, WORK_ORDER, WORKS, SITE_COPY,
)

# Primary navigation entries: (route-key, display-label)
PRIMARY_NAV = [
    ('works', 'Works'),
    ('practice', 'Practice'),
    ('about', 'About'),
]

CNAME_DOMAIN = 'theblackbirdfield.com'

# ---------------------------------------------------------------------------
# Route registry
#
# Each entry:
#   route       — canonical public URL path
#   output      — path relative to dist/
#   title / description — <title> / meta description / og values
#   current     — navigation identity key
#   class       — <body> class attribute
#   renderer    — renderer key consumed by build.py
#   work_key    — populated for project/alias routes
#   canonical_key — for aliases, the route key holding the canonical URL
#   noindex     — True for aliases
#   sitemap     — False to exclude from sitemap (default True)
#   og_image    — site-relative asset path for OG image (optional)
# ---------------------------------------------------------------------------

ROUTES = {
    'home': {
        'route': '/',
        'output': 'index.html',
        'title': SITE_COPY['home']['meta']['title'],
        'description': SITE_COPY['home']['meta']['description'],
        'current': 'home',
        'class': 'home-page',
        'renderer': 'home',
        'og_image': f'assets/{WORK_ORDER[0]}/_placeholder.png',
    },
    'works': {
        'route': '/works/',
        'output': 'works/index.html',
        'title': SITE_COPY['works']['meta']['title'],
        'description': SITE_COPY['works']['meta']['description'],
        'current': 'works',
        'class': 'works-page',
        'renderer': 'works',
        'og_image': f'assets/{WORK_ORDER[0]}/_placeholder.png',
    },
    'practice': {
        'route': '/practice/',
        'output': 'practice/index.html',
        'title': SITE_COPY['practice']['meta']['title'],
        'description': SITE_COPY['practice']['meta']['description'],
        'current': 'practice',
        'class': 'practice-page',
        'renderer': 'practice',
    },
    'about': {
        'route': '/about/',
        'output': 'about/index.html',
        'title': SITE_COPY['about']['meta']['title'],
        'description': SITE_COPY['about']['meta']['description'],
        'current': 'about',
        'class': 'about-page',
        'renderer': 'about',
    },
    'contact': {
        'route': '/contact/',
        'output': 'contact/index.html',
        'title': SITE_COPY['contact']['meta']['title'],
        'description': SITE_COPY['contact']['meta']['description'],
        'current': 'contact',
        'class': 'contact-page',
        'renderer': 'contact',
    },
}

for _key in WORK_ORDER:
    _work = WORKS[_key]
    ROUTES[_key] = {
        'route': _work['canonical_route'],
        'output': _work['canonical_route'].strip('/') + '/index.html',
        'title': _work['meta']['title'],
        'description': _work['meta']['description'],
        'current': 'works',
        'class': f'project-page project-page--{_key}',
        'renderer': 'project',
        'work_key': _key,
        'og_image': _work.get('assets', {}).get('hero', f'assets/{_key}/_placeholder.png'),
    }
    ROUTES[f'{_key}-alias'] = {
        'route': _work['alias_route'],
        'output': _work['alias_route'].strip('/') + '/index.html',
        'title': _work['meta']['title'],
        'description': _work['meta']['description'],
        'current': 'works',
        'class': f'project-page project-page--{_key} project-page--alias',
        'renderer': 'project',
        'work_key': _key,
        'canonical_key': _key,
        'noindex': True,
        'sitemap': False,
        'og_image': _work.get('assets', {}).get('hero', f'assets/{_key}/_placeholder.png'),
    }

# Grave runtime: not a portfolio page, not sitemap-indexed.
GRAVE_RUNTIME_OUTPUT = 'works/grave-machine/run/index.html'
GRAVE_RUNTIME_ROUTE = '/works/grave-machine/run/'

# Root-relative path segments for each route (relative to site root).
ROUTE_PATHS = {key: meta['route'].lstrip('/') for key, meta in ROUTES.items()}
ROUTE_PATHS['grave-machine-run'] = GRAVE_RUNTIME_ROUTE.lstrip('/')

# Legacy flat-file routes that redirect to canonical directory routes.
# Each entry: (old_output, route_key)
LEGACY_REDIRECTS = [
    ('works.html', 'works'),
    ('black-bird.html', 'black-bird'),
    ('winter-road.html', 'winter-road'),
    ('unhappy-scenario.html', 'unhappy-scenario'),
    ('grave-machine.html', 'grave-machine'),
    ('taroke-remixer.html', 'taroke-remixer'),
    ('practice.html', 'practice'),
    ('about.html', 'about'),
    ('contact.html', 'contact'),
]
