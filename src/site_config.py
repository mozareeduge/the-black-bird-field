SITE_TITLE = 'The Black Bird Field'
ARTISTIC_NAME = 'Mozare'
FORMAL_NAME = 'Mohammad Zare'
CV_FILENAME = 'Mohammad_Zare_AcademicCV.pdf'
LINKEDIN_URL = 'https://www.linkedin.com/in/mohammad-zare-287997215/'
GITHUB_URL = 'https://github.com/mozareeduge'
EMAIL = 'mozare1997@gmail.com'

# Work launch URLs — all configurable from this file.
# Before domain approval: external works use their own GitHub Pages origins;
# Grave-Machine is hosted under the portfolio at works/grave-machine/.
# After domain approval: update GRAVE_RUNTIME_URL and, if subpath is chosen,
# update the three external URLs to match the new routing.
GRAVE_RUNTIME_URL = 'works/grave-machine/'

WORK_URLS = {
    'black-bird':      'https://mozareeduge.github.io/the-black-bird/',
    'winter-road':     'https://mozareeduge.github.io/winter-road/',
    'grave-machine':   GRAVE_RUNTIME_URL,
    'taroke-remixer':  'https://mozareeduge.github.io/taroke-remixer/',
}

WORK_REPO_URLS = {
    'black-bird':      'https://github.com/mozareeduge/the-black-bird',
    'winter-road':     'https://github.com/mozareeduge/winter-road',
    'grave-machine':   'https://github.com/mozareeduge/the-black-bird-field',
    'taroke-remixer':  'https://github.com/mozareeduge/taroke-remixer',
}

PRIMARY_NAV = [
    ('works',    'Works',    'works.html'),
    ('practice', 'Practice', 'practice.html'),
    ('about',    'About',    'about.html'),
]

PAGES = {
    'index.html': {
        'title':       'The Black Bird Field — Works by Mozare',
        'description': 'The online field of four browser-native works by Mozare, the artistic name used by Mohammad Zare.',
        'current': 'home', 'class': 'home-page', 'fragment': 'home.html',
    },
    'works.html': {
        'title':       'Works — The Black Bird Field',
        'description': 'The Black Bird, Winter Road, Grave-Machine, and TAROKE RIMIXER: four browser-native works by Mozare.',
        'current': 'works', 'class': 'works-page', 'fragment': 'works.html',
    },
    'black-bird.html': {
        'title':       'The Black Bird — A Hypergraph Research Poem',
        'description': 'The Black Bird is a hypergraph research poem by Mozare. The reader moves between a field of linked materials and the text held in its Reader.',
        'current': 'works', 'class': 'project-page black-bird-page', 'fragment': 'black-bird.html', 'atlas': True,
    },
    'winter-road.html': {
        'title':       'Winter Road — A Digital Haiga Space',
        'description': 'Winter Road is a digital haiga space by Mozare in which nine haiku are found through movement and held only for a time.',
        'current': 'works', 'class': 'project-page winter-road-page', 'fragment': 'winter-road.html', 'atlas': True,
    },
    'grave-machine.html': {
        'title':       'Grave-Machine — An Iranian Remix of Taroko Gorge',
        'description': 'Grave-Machine is a generative e-poem by Mozare that carries material from the play Grave into the remix lineage of Taroko Gorge.',
        'current': 'works', 'class': 'project-page grave-machine-page', 'fragment': 'grave-machine.html', 'atlas': True,
    },
    'taroke-remixer.html': {
        'title':       'TAROKE RIMIXER — A Work for Generative Literature',
        'description': 'TAROKE RIMIXER is a browser-native creative work by Mozare that makes the composition of a generative poem visible and editable.',
        'current': 'works', 'class': 'project-page taroke-page', 'fragment': 'taroke-remixer.html', 'atlas': True,
    },
    'practice.html': {
        'title':       'Practice — The Black Bird Field',
        'description': 'Mozare develops browser-native literary forms through research, generative writing, and the design of reading conditions.',
        'current': 'practice', 'class': 'practice-page', 'fragment': 'practice.html',
    },
    'about.html': {
        'title':       'About — The Black Bird Field',
        'description': 'About Mozare and Mohammad Zare, an Iranian poet and researcher working across dramatic literature and born-digital form.',
        'current': 'about', 'class': 'about-page', 'fragment': 'about.html',
    },
    'contact.html': {
        'title':       'Contact — The Black Bird Field',
        'description': 'Contact Mozare regarding the works, related research, and collaboration.',
        'current': 'contact', 'class': 'contact-page', 'fragment': 'contact.html',
    },
}
