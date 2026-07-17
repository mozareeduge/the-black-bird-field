SITE_TITLE = 'The Black Bird Field'
SITE_ORIGIN = 'https://theblackbirdfield.com'
ARTISTIC_NAME = 'Mozare'
FORMAL_NAME = 'Mohammad Zare'
CV_FILENAME = 'Mohammad_Zare_AcademicCV.pdf'
LINKEDIN_URL = 'https://www.linkedin.com/in/mohammad-zare-287997215/'
GITHUB_URL = 'https://github.com/mozareeduge'
EMAIL = 'mozare1997@gmail.com'

# Work repository URLs (always absolute)
WORK_REPO_URLS = {
    'black-bird':     'https://github.com/mozareeduge/the-black-bird',
    'winter-road':    'https://github.com/mozareeduge/winter-road',
    'grave-machine':  'https://github.com/mozareeduge/the-black-bird-field',
    'taroke-remixer': 'https://github.com/mozareeduge/taroke-remixer',
}

# Primary navigation entries: (route-key, display-label)
# Hrefs are computed at render time using the route registry and page prefix.
PRIMARY_NAV = [
    ('works',    'Works'),
    ('practice', 'Practice'),
    ('about',    'About'),
]

# ---------------------------------------------------------------------------
# Route registry
# Each entry defines:
#   route       — canonical public URL path
#   output      — path relative to dist/
#   title       — <title> and og:title
#   description — meta description and og:description
#   current     — navigation identity key
#   class       — <body> class attribute
#   fragment    — source fragment filename in src/pages/
#   atlas       — True if atlas.js is needed (optional)
#   og_image    — site-relative asset path for OG image (optional)
#   sitemap     — False to exclude from sitemap (default True)
# ---------------------------------------------------------------------------
ROUTES = {
    'home': {
        'route':       '/',
        'output':      'index.html',
        'title':       'The Black Bird Field — Works by Mozare',
        'description': 'The online field of four browser-native works by Mozare, the artistic name used by Mohammad Zare.',
        'current':     'home',
        'class':       'home-page',
        'fragment':    'home.html',
        'og_image':    'assets/black-bird/06_desktop_mno_reader.png',
    },
    'works': {
        'route':       '/works/',
        'output':      'works/index.html',
        'title':       'Works — The Black Bird Field',
        'description': 'The Black Bird, Winter Road, Grave-Machine, and TAROKE RIMIXER: four browser-native works by Mozare.',
        'current':     'works',
        'class':       'works-page',
        'fragment':    'works.html',
        'og_image':    'assets/black-bird/06_desktop_mno_reader.png',
    },
    'black-bird': {
        'route':       '/works/the-black-bird/',
        'output':      'works/the-black-bird/index.html',
        'title':       'The Black Bird — A Hypergraph Research Poem',
        'description': 'The Black Bird is a hypergraph research poem by Mozare. The reader moves between a field of linked materials and the text held in its Reader.',
        'current':     'works',
        'class':       'project-page black-bird-page',
        'fragment':    'black-bird.html',
        'atlas':       True,
        'og_image':    'assets/black-bird/06_desktop_mno_reader.png',
    },
    'winter-road': {
        'route':       '/works/winter-road/',
        'output':      'works/winter-road/index.html',
        'title':       'Winter Road — A Digital Haiga Space',
        'description': 'Winter Road is a digital haiga space by Mozare in which nine haiku are found through movement and held only for a time.',
        'current':     'works',
        'class':       'project-page winter-road-page',
        'fragment':    'winter-road.html',
        'atlas':       True,
        'og_image':    'assets/winter-road/walkthrough/03-desktop-kept-relation.png',
    },
    'grave-machine': {
        'route':       '/works/grave-machine/',
        'output':      'works/grave-machine/index.html',
        'title':       'Grave-Machine — An Iranian Remix of Taroko Gorge',
        'description': 'Grave-Machine is a generative e-poem by Mozare that carries material from the play Grave into the remix lineage of Taroko Gorge.',
        'current':     'works',
        'class':       'project-page grave-machine-page',
        'fragment':    'grave-machine.html',
        'atlas':       True,
        'og_image':    'assets/grave-machine/bilingual/desktop_22s.png',
    },
    'taroke-remixer': {
        'route':       '/works/taroke-remixer/',
        'output':      'works/taroke-remixer/index.html',
        'title':       'TAROKE RIMIXER — A Work for Generative Literature',
        'description': 'TAROKE RIMIXER is a browser-native creative work by Mozare that makes the composition of a generative poem visible and editable.',
        'current':     'works',
        'class':       'project-page taroke-page',
        'fragment':    'taroke-remixer.html',
        'atlas':       True,
        'og_image':    'assets/taroke-remixer/01_workbench.png',
    },
    'practice': {
        'route':       '/practice/',
        'output':      'practice/index.html',
        'title':       'Practice — The Black Bird Field',
        'description': 'Mozare develops browser-native literary forms through research, generative writing, and the design of reading conditions.',
        'current':     'practice',
        'class':       'practice-page',
        'fragment':    'practice.html',
        'og_image':    'assets/grave-machine/bilingual/desktop_22s.png',
    },
    'about': {
        'route':       '/about/',
        'output':      'about/index.html',
        'title':       'About — The Black Bird Field',
        'description': 'About Mozare and Mohammad Zare, an Iranian poet and researcher working across dramatic literature and born-digital form.',
        'current':     'about',
        'class':       'about-page',
        'fragment':    'about.html',
        'og_image':    'assets/black-bird/06_desktop_mno_reader.png',
    },
    'contact': {
        'route':       '/contact/',
        'output':      'contact/index.html',
        'title':       'Contact — The Black Bird Field',
        'description': 'Contact Mozare regarding the works, related research, and collaboration.',
        'current':     'contact',
        'class':       'contact-page',
        'fragment':    'contact.html',
    },
}

# Grave runtime: not a portfolio page, not sitemap-indexed.
# The build places the byte-identical HTML at this output path.
GRAVE_RUNTIME_OUTPUT = 'works/grave-machine/run/index.html'

# Root-relative path segments for each route (used to build relative URLs).
# The root_prefix() helper in build.py computes ../ repetitions from depth.
ROUTE_PATHS = {
    'home':             '',
    'works':            'works/',
    'black-bird':       'works/the-black-bird/',
    'winter-road':      'works/winter-road/',
    'grave-machine':    'works/grave-machine/',
    'taroke-remixer':   'works/taroke-remixer/',
    'grave-machine-run':'works/grave-machine/run/',
    'practice':         'practice/',
    'about':            'about/',
    'contact':          'contact/',
}

# Legacy flat-file routes that now redirect to canonical directory routes.
# Each entry: (old_output, new_route_key)
LEGACY_REDIRECTS = [
    ('works.html',         'works'),
    ('black-bird.html',    'black-bird'),
    ('winter-road.html',   'winter-road'),
    ('grave-machine.html', 'grave-machine'),
    ('taroke-remixer.html','taroke-remixer'),
    ('practice.html',      'practice'),
    ('about.html',         'about'),
    ('contact.html',       'contact'),
]
