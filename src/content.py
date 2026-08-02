"""Structured five-work content authority for The Black Bird Field.

Every visitor-facing string here is transcribed verbatim from
docs/authority/CANONICAL_COPY.md, the sole source for visitor-facing copy
(D-COPY-AUTHORITY). This module imports no HTML and performs no I/O; it is
consumed by src/renderers.py and src/build.py.

Paragraph strings may contain single-asterisk emphasis markers (*word*),
resolved to <em> by renderers.emphasize(). This is not a general Markdown
runtime: no other Markdown syntax is recognised or supported.
"""

from __future__ import annotations

SITE_TITLE = 'The Black Bird Field'
SITE_ORIGIN = 'https://theblackbirdfield.com'
ARTISTIC_NAME = 'Mozare'
FORMAL_NAME = 'Mohammad Zare'
CV_FILENAME = 'Mohammad_Zare_AcademicCV.pdf'
LINKEDIN_URL = 'https://www.linkedin.com/in/mohammad-zare-287997215/'
GITHUB_URL = 'https://github.com/mozareeduge'
EMAIL = 'mozare1997@gmail.com'

# ---------------------------------------------------------------------------
# Shared site copy (header, mobile menu, footer)
# ---------------------------------------------------------------------------

SHARED = {
    'header': {
        'wordmark': SITE_TITLE,
        'wordmark_subline': f'works by {ARTISTIC_NAME}',
        'primary_nav': (
            ('works', 'Works'),
            ('practice', 'Practice'),
            ('about', 'About'),
        ),
        'utility_nav_label': 'Contact / LinkedIn / CV',
        'menu_control': 'Menu',
        'skip_link': 'Skip to main content',
    },
    'mobile_menu': {
        'title': SITE_TITLE,
        'subline': f'works by {ARTISTIC_NAME}',
        'close': 'Close',
        'utility_contact': 'Contact ->',
        'utility_cv': 'Download CV',
        'utility_linkedin': 'LinkedIn ↗',
        'identity_note_1': f'Artistic work: {ARTISTIC_NAME}.',
        'identity_note_2': f'Academic records, citations, rights, and professional records: {FORMAL_NAME}.',
    },
    'footer': {
        'identity': ARTISTIC_NAME,
        'practice_line': 'Research, poetry, procedure, and the browser, brought into form together.',
        'formal_name_line': f'Academic records, citations, rights, and professional records: {FORMAL_NAME}.',
        'portfolio_statement': f'{SITE_TITLE} is the online exhibition and archive of works by {ARTISTIC_NAME}.',
        'copyright': f'© 2026 {FORMAL_NAME}.',
    },
}

# ---------------------------------------------------------------------------
# Work order — fixed, never derived from filesystem or title sorting.
# ---------------------------------------------------------------------------

WORK_ORDER = (
    'black-bird',
    'winter-road',
    'unhappy-scenario',
    'grave-machine',
    'taroke-remixer',
)

# ---------------------------------------------------------------------------
# Per-work content
# ---------------------------------------------------------------------------

WORKS = {
    'black-bird': {
        'order': 1,
        'title': 'The Black Bird',
        'operative': 'Traverse',
        'form': 'Hypergraph research poem',
        'year': 2026,
        'subtitle': None,
        'live_url': 'https://poem.theblackbirdfield.com/',
        'repo_url': 'https://github.com/mozareeduge/the-black-bird',
        'canonical_route': '/works/the-black-bird/',
        'alias_route': '/the-black-bird/',
        'meta': {
            'title': 'The Black Bird - A Hypergraph Research Poem',
            'description': 'The Black Bird is a hypergraph research poem by Mozare that gathers sources, names, relations, poem-nodes, and reader routes into a born-digital literary field.',
            'og_image_alt': 'The Black Bird graph beside a Mapping Note Object in the Reader.',
        },
        'home_feature': {
            'form_line': 'Hypergraph research poem · 2026',
            'title': 'The Black Bird',
            'subtitle': None,
            'copy': 'A black bird beside a body becomes the point from which a field of research and poetry opens. Scriptural, mythic, linguistic, behavioral, poetic, and forensic materials keep their distinct forms while the hypergraph lets their crossings become part of the poem.',
            'image_alt': 'The Black Bird graph beside a Mapping Note Object held in the Reader.',
            'frame_caption': 'Typed objects / relational field',
            'actions': (
                ('Enter the work ↗', 'https://poem.theblackbirdfield.com/'),
                ('About the work ->', '/works/the-black-bird/'),
            ),
        },
        'works_index': {
            'form_line': 'Hypergraph research poem · 2026',
            'work_note': 'A black bird and a body become the centre of a field where scenes, names, sources, poem-nodes, and reader routes can meet while keeping their differences. The typed hypergraph gives every return an address.',
            'image_alt': 'A Research Note Object open beside The Black Bird graph.',
            'action_label': 'View work page ->',
        },
        'project': {
            'form_line': 'A hypergraph research poem · by Mozare · 2026',
            'subtitle': None,
            'lead': "A black bird appears beside a body, and the scene begins to gather other scenes around it. *The Black Bird* gives sources, names, references, poem-nodes, and relations distinct bodies within a typed hypergraph, where the reader's movement also becomes part of the work.",
            'actions': (
                ('Enter the work ↗', 'https://poem.theblackbirdfield.com/'),
                ('Source and rights ↗', 'https://github.com/mozareeduge/the-black-bird'),
            ),
            'hero_image_alt': 'The Black Bird graph beside a Mapping Note Object held in the Reader.',
            'hero_frame_caption': 'Graph / Reader / Mapping Note Object',
            'context_heading': 'Where a black bird meets a body',
            'context_paragraphs': (
                'A black bird beside a body carries centuries of different attention. In scriptural narrative, myth, language, observed animal behavior, poetry, and forensic knowledge, the contact means differently and rests on different kinds of support. *The Black Bird* brings these appearances into one field while keeping their distances legible.',
                'An object grammar gives each material a working body. A Research Note carries a source-bearing scene; a Mapping Note draws several pressures into a local surface. Name, Reference, Field, and Relation Objects hold linguistic form, citation, recurrence, and connection. Through these types, the field remembers how a material arrived and how a reader may reach it again.',
                'The graph makes contact visible before explanation settles it. The Reader slows one selected object down; the Index opens the inventory; View changes the visible field; Route keeps the path of attention. Provenance, poetic pressure, and reader movement can therefore remain present at the same time.',
                'Speculative research poetry takes form here as a practice of holding relations at the level they can honestly bear. A source keeps its provenance; a poetic connection keeps its provisional force; a reader may follow, question, or leave it. The poem lives through these partial encounters and through the space that remains between them.',
            ),
            'selected_views': (
                {'view': '01 - Field and Reader', 'caption': 'The graph holds the current relation while the Reader gives one object textual duration.', 'alt': 'The Black Bird graph beside an open Research Note Object in the Reader.'},
                {'view': '02 - Mapping Note', 'caption': 'A Mapping Note condenses a charged relation and returns its linked objects to the field.', 'alt': 'A Mapping Note Object open beside connected nodes in The Black Bird graph.'},
                {'view': '03 - Mobile Field', 'caption': 'The mobile Field preserves spatial selection before the object enters sustained reading.', 'alt': 'A selected object held in The Black Bird mobile Field.'},
                {'view': '04 - Mobile Read', 'caption': 'The Read chamber gives the selected object the full height of the phone while preserving its field identity.', 'alt': 'The Black Bird mobile Read chamber displaying a selected object.'},
            ),
            'details': (
                ('Form', 'Born-digital hypergraph research poem'),
                ('Artist', 'Mozare'),
                ('Citation name', 'Mohammad Zare'),
                ('Language', 'English with source-language Name Objects'),
                ('Core structure', 'Typed hypergraph, Reader, Index, View, Route, and About'),
                ('Live work', 'https://poem.theblackbirdfield.com/'),
                ('Research annex', 'https://poem.theblackbirdfield.com/research/'),
                ('Repository', 'https://github.com/mozareeduge/the-black-bird'),
                ('Citation', 'Mohammad Zare. *The Black Bird: A Hypergraph Research Poem*. Born-digital web work, 2026.'),
                ('Rights', 'Copyright © 2026 Mohammad Zare. See the repository rights notice.'),
            ),
        },
    },
    'winter-road': {
        'order': 2,
        'title': 'Winter Road',
        'operative': 'Approach',
        'form': 'Digital haiga space',
        'year': 2026,
        'subtitle': None,
        'live_url': 'https://mozareeduge.github.io/winter-road/',
        'repo_url': 'https://github.com/mozareeduge/winter-road',
        'canonical_route': '/works/winter-road/',
        'alias_route': '/winter-road/',
        'meta': {
            'title': 'Winter Road - A Digital Haiga Space',
            'description': 'Winter Road is a digital haiga space by Mozare: nine English haiku developed through permutation and dispersed across a near-black field.',
            'og_image_alt': 'Two Winter Road haiku visible at different strengths in the near-black field.',
        },
        'home_feature': {
            'form_line': 'Digital haiga space · 2026',
            'title': 'Winter Road',
            'subtitle': None,
            'copy': 'Nine haiku, all descended from the phrase *winter road*, are held apart in a near-black field. Their kinship appears through distance, brief illumination, and the changing relation between one poem and another.',
            'image_alt': 'Two Winter Road haiku visible at different strengths within the near-black field.',
            'frame_caption': 'Distance / temporary relation',
            'actions': (
                ('Enter the work ↗', 'https://mozareeduge.github.io/winter-road/'),
                ('About the work ->', '/works/winter-road/'),
            ),
        },
        'works_index': {
            'form_line': 'Digital haiga space · 2026',
            'work_note': 'Nine haiku share the verbal ground of *winter road*, yet each holds its own weather. Their family resemblance becomes visible through distance, gradual illumination, and temporary proximity.',
            'image_alt': 'A Winter Road haiku emerging through proximity in the dark field.',
            'action_label': 'View work page ->',
        },
        'project': {
            'form_line': 'Nine poems in one winter field · by Mozare · 2026',
            'subtitle': None,
            'lead': 'Nine English haiku grew from two words: *winter road*. They remain complete poems, yet the browser lets their kinship appear through darkness, distance, and the brief time one poem can stay near another.',
            'actions': (
                ('Enter the work ↗', 'https://mozareeduge.github.io/winter-road/'),
                ('Source and rights ↗', 'https://github.com/mozareeduge/winter-road'),
            ),
            'hero_image_alt': 'Two Winter Road haiku held at different strengths within the near-black field.',
            'hero_frame_caption': 'Kept relation / distance / gradual visibility',
            'context_heading': 'Nine poems in one winter field',
            'context_paragraphs': (
                'The phrase *winter road* was turned, cut, and recomposed until it opened toward absence, wind, darkness, whiteness, and silence. Nine haiku emerged from that sustained rewriting. They share a verbal ancestry, though each has its own weather and its own closure.',
                "Haiga gives a poem an image-bearing companion. Here the near-black field takes that role through distance, gradual illumination, and the reader's movement. Image arises across the relation between a poem and the darkness that withholds or releases it.",
                'Each haiku keeps its own completion. Yet a held poem may remain while another begins to brighten, making a temporary composition that belongs to this movement through the field. Darkness gives the poems enough distance to approach one another while each stays distinct.',
                "The phrase *digital haiga space* names this particular arrangement: language, darkness, placement, and movement sharing the work of image-making. The image is neither fixed nor elsewhere; it gathers for a time around the reader's approach.",
            ),
            'selected_views': (
                {'view': '01 - Dark field', 'caption': 'The root phrase establishes the field while the nine haiku remain dispersed beyond immediate view.', 'alt': 'Winter Road at entry with the root phrase visible in a near-black field.'},
                {'view': '02 - Discovery', 'caption': 'Gradual illumination gives the approach to a poem its own duration.', 'alt': 'A Winter Road haiku becoming legible through proximity.'},
                {'view': '03 - Kept relation', 'caption': 'A held poem and an emerging poem form a temporary composition across the field.', 'alt': 'One Winter Road haiku held while another begins to appear.'},
                {'view': '04 - Mobile relation', 'caption': 'Touch movement preserves the same relation among distance, discovery, and temporary presence.', 'alt': 'Two Winter Road haiku visible at different strengths on a mobile screen.'},
            ),
            'details': (
                ('Form', 'Born-digital haiga space'),
                ('Artist', 'Mozare'),
                ('Citation name', 'Mohammad Zare'),
                ('Language', 'English'),
                ('Poems', 'Nine haiku'),
                ('Composition', 'Authored semantic grid with four spatial rotations'),
                ('Live work', 'https://mozareeduge.github.io/winter-road/'),
                ('Repository', 'https://github.com/mozareeduge/winter-road'),
                ('Release', 'v1.0.1'),
                ('Citation', 'Mohammad Zare. *Winter Road: A Haiga Space*. Version 1.0.1, 2026.'),
                ('Rights', 'Copyright © 2026 Mohammad Zare. See the repository rights notice.'),
            ),
        },
    },
    'unhappy-scenario': {
        'order': 3,
        'title': 'UNHAPPY Scenario',
        'operative': 'Attempt',
        'form': 'Internet blackout poem',
        'year': 2026,
        'subtitle': 'An Internet Blackout Poem',
        'live_url': 'https://unhappy.theblackbirdfield.com/',
        'repo_url': 'https://github.com/mozareeduge/UNHAPPY-scenario',
        'canonical_route': '/works/unhappy-scenario/',
        'alias_route': '/unhappy-scenario/',
        'meta': {
            'title': 'UNHAPPY Scenario - An Internet Blackout Poem',
            'description': 'UNHAPPY Scenario is a browser-native found-interface poem by Mozare, composed in relation to repeated internet blackouts in Iran.',
            'og_image_alt': 'The UNHAPPY Scenario messenger apparatus beside its accumulated poem field.',
        },
        'home_feature': {
            'form_line': 'Internet blackout poem · 2026',
            'title': 'UNHAPPY Scenario',
            'subtitle': 'An Internet Blackout Poem',
            'copy': 'The calm phrases through which software names interrupted communication are carried into the memory of repeated internet blackouts in Iran. Their promise of recovery thins with each return, exposing deferred contact and an accountability that remains out of reach.',
            'image_alt': 'The UNHAPPY Scenario messenger apparatus beside an accumulated field of system-message lines.',
            'frame_caption': 'Failed transmission / accumulated procedure',
            'actions': (
                ('Enter the work ↗', 'https://unhappy.theblackbirdfield.com/'),
                ('About the work ->', '/works/unhappy-scenario/'),
            ),
        },
        'works_index': {
            'form_line': 'Internet blackout poem · 2026',
            'work_note': "Software's calm notices of failed communication move through a deterministic chain of attempted recovery. In relation to internet blackouts in Iran, repetition makes their ordinary language carry isolation, delay, and unreachable accountability.",
            'image_alt': 'UNHAPPY Scenario showing ordered black procedural shells beside the poem field.',
            'action_label': 'View work page ->',
        },
        'project': {
            'form_line': 'An internet blackout poem · by Mozare · English edition · v2.6.0 · 2026',
            'subtitle': 'An Internet Blackout Poem',
            'lead': 'Software calls the route away from success an unhappy scenario. The poem takes that calm technical phrase seriously, carrying the language of failure and promised recovery into the memory of repeated internet blackouts in Iran.',
            'actions': (
                ('Enter the work ↗', 'https://unhappy.theblackbirdfield.com/'),
                ('Source and rights ↗', 'https://github.com/mozareeduge/UNHAPPY-scenario'),
            ),
            'hero_image_alt': 'The UNHAPPY Scenario messenger apparatus beside system-message lines accumulated in the poem field.',
            'hero_frame_caption': 'Messenger / procedural shells / poem field',
            'context_heading': 'The calm voice of interrupted connection',
            'context_paragraphs': (
                'In software language, an unhappy scenario is the route an operation takes when it leaves the expected path. The phrase places interruption inside a manageable plan: name the branch, provide recovery, return the user to continuity.',
                'The poem composes this procedural vocabulary as found material. Upload, sending, reconnection, and reporting pass from one promised remedy to the next obstruction. The voice stays calm. Repetition makes that calmness increasingly charged, as the system continues to speak in the grammar of temporary inconvenience.',
                'Repeated internet blackouts in Iran give this language its remembered ground. A failed connection reaches into intimate contact, access to information, work, and the possibility of reporting harm. The small vocabulary of system notices begins to carry a much larger condition: separation, suspended time, and accountability held beyond reach.',
                'Two connected surfaces hold the interruption. The communication apparatus continues to offer procedures; the poem field receives what those procedures say. A surviving message, an active shell, its dark residues, and the accumulating lines register different durations of the same blocked passage. In the browser, the promise of return is allowed to spend itself completely.',
            ),
            'selected_views': (
                {'view': '01 - Failed sending', 'caption': 'The outgoing message remains in place as the first procedural failure enters the encounter.', 'alt': 'UNHAPPY Scenario after message sending fails, with the outgoing message still visible.'},
                {'view': '02 - Historical pressure', 'caption': 'Ordered black residues register accumulated attempts while one procedural shell remains active.', 'alt': 'UNHAPPY Scenario with six historical black shells receding behind the active shell.'},
                {'view': '03 - Reporting failed', 'caption': 'The route toward accountability returns institutional failure to the poem field.', 'alt': 'UNHAPPY Scenario at Reporting failed with the accumulated poem visible beside the messenger.'},
                {'view': '04 - Mobile underfield', 'caption': 'The fault-latch expands the poem underfield while preserving the messenger above it.', 'alt': 'UNHAPPY Scenario on mobile with the poem underfield expanded beneath the messenger.'},
            ),
            'details': (
                ('Form', 'Browser-native found-interface poem'),
                ('Artist', 'Mozare'),
                ('Citation name', 'Mohammad Zare'),
                ('Language', 'English'),
                ('Edition', 'v2.6.0'),
                ('Release date', '30 July 2026'),
                ('Core structure', 'Deterministic finite-state procedure, messenger apparatus, and accumulating poem field'),
                ('Privacy', 'Self-contained static artwork with zero external runtime requests and zero persistent storage'),
                ('Live work', 'https://unhappy.theblackbirdfield.com/'),
                ('Repository', 'https://github.com/mozareeduge/UNHAPPY-scenario'),
                ('Citation', 'Mohammad Zare. *UNHAPPY Scenario: An Internet Blackout Poem*. Version 2.6.0, 2026.'),
                ('Rights', 'Copyright © 2026 Mohammad Zare. See the repository rights notice.'),
            ),
            'locked_textual_authority': (
                "The artwork's eight system messages retain their exact wording, order, punctuation, and Unicode ellipses. "
                '`Try again` remains an interface action. The portfolio page presents contextual prose and selected '
                'documentation; the poem itself remains in the live work.'
            ),
        },
    },
    'grave-machine': {
        'order': 4,
        'title': 'Grave-Machine',
        'operative': 'Remain',
        'form': 'Generative electronic poem',
        'year': 2026,
        'subtitle': 'An Iranian Remix of Taroko Gorge',
        'live_url': '/works/grave-machine/run/',
        'repo_url': 'https://github.com/mozareeduge/grave-machine',
        'canonical_route': '/works/grave-machine/',
        'alias_route': '/grave-machine/',
        'meta': {
            'title': 'Grave-Machine - An Iranian Remix of Taroko Gorge',
            'description': 'Grave-Machine is a bilingual generative electronic poem by Mozare, grounded in the play Grave and composed within the remix lineage of Taroko Gorge.',
            'og_image_alt': 'Grave-Machine generated lines beside a runtime trace.',
        },
        'home_feature': {
            'form_line': 'Generative electronic poem · 2026',
            'title': 'Grave-Machine',
            'subtitle': 'An Iranian Remix of Taroko Gorge',
            'copy': 'The bodily and bureaucratic world of the play *Grave* returns through the remix lineage of *Taroko Gorge*. English and Persian lines recur beside the procedural receipt of their making, so burial, paperwork, and generation remain under the same pressure.',
            'image_alt': 'Grave-Machine generated lines beside a runtime receipt that records their construction.',
            'frame_caption': 'Generated surface / procedural trace',
            'actions': (
                ('Enter the work ↗', '/works/grave-machine/run/'),
                ('About the work ->', '/works/grave-machine/'),
            ),
        },
        'works_index': {
            'form_line': 'Generative electronic poem · 2026',
            'work_note': 'The dramatic world of *Grave* returns as a bilingual poem-machine within the remix lineage of *Taroko Gorge*. Each line appears beside a quieter receipt of the route and material that brought it forward.',
            'image_alt': 'Grave-Machine with accumulated Persian generated lines and a runtime trace.',
            'action_label': 'View work page ->',
        },
        'project': {
            'form_line': 'A bilingual generative electronic poem · by Mozare · 2026',
            'subtitle': 'An Iranian Remix of Taroko Gorge',
            'lead': "The bodily and bureaucratic world of Mohammad Zare's play *Grave* returns inside the walking engine inherited from Nick Montfort's *Taroko Gorge*. English and Persian lines gather beside a runtime receipt, keeping each recurrence close to the procedure that made it.",
            'actions': (
                ('Enter the work ↗', '/works/grave-machine/run/'),
                ('Source and rights ↗', 'https://github.com/mozareeduge/grave-machine'),
            ),
            'hero_image_alt': 'Grave-Machine with accumulated generated lines beside the current runtime receipt.',
            'hero_frame_caption': 'Bilingual surface / runtime receipt',
            'context_heading': 'A body enters the ledger',
            'context_paragraphs': (
                "*Grave* was written as the practical component of Mohammad Zare's MA in Dramatic Literature. In its dramatic world, burial is already surrounded by forms, folders, rooms, and administrative labor. A body enters a system of handling, naming, delay, and procedure.",
                '*Taroko Gorge* offers a small engine whose movement has travelled through many remixes. *Grave-Machine* asks that engine to carry another dramatic ground. Bodies, documents, rooms, and actions return in English and Persian, altered by each arrangement yet held inside the same unfinished labor.',
                'A quieter runtime receipt sits beside the generated poem like a ledger. It records the material and route behind the current line, keeping construction within the public form of the work. Recurrence can be read in the language and in the procedure that has carried the language forward.',
                'Remix becomes a form of carrying. An earlier poem-engine enters a new linguistic, dramatic, and historical environment; its familiar movement bends under the weight of bodies, records, and translation. Return remains active, but each return arrives marked by the labor that produced it.',
            ),
            'selected_views': (
                {'view': '01 - First event', 'caption': 'One line and one receipt establish the relation between generated language and procedural evidence.', 'alt': 'Grave-Machine showing its first generated line beside the first runtime receipt.'},
                {'view': '02 - English accumulation', 'caption': 'Recurring bodies, documents, and actions form a temporary English field across several cycles.', 'alt': 'Grave-Machine with several English generated lines accumulated beside the runtime trace.'},
                {'view': '03 - Persian accumulation', 'caption': 'Direction, typography, interface language, and generated material change together in the Persian work.', 'alt': 'Grave-Machine with accumulated Persian generated lines and Persian interface text.'},
                {'view': '04 - Statement and runtime', 'caption': 'Lineage and dramatic ground remain connected to the running work beneath the statement.', 'alt': 'Grave-Machine statement open above the bilingual runtime.'},
            ),
            'details': (
                ('Form', 'Bilingual generative electronic poem'),
                ('Artist', 'Mozare'),
                ('Citation name', 'Mohammad Zare'),
                ('Languages', 'English / Persian'),
                ('Dramatic ground', "Mohammad Zare's play *Grave*"),
                ('Lineage', "After Nick Montfort's *Taroko Gorge*"),
                ('Live work', 'https://theblackbirdfield.com/works/grave-machine/run/'),
                ('Repository', 'https://github.com/mozareeduge/grave-machine'),
                ('Release', 'Bilingual v1.1'),
                ('Citation', 'Mohammad Zare. *Grave-Machine / گور-ماشین*. Bilingual generative electronic poem, 2026.'),
                ('Rights', 'Copyright © 2026 Mohammad Zare. See the repository rights notice.'),
            ),
        },
    },
    'taroke-remixer': {
        'order': 5,
        'title': 'TAROKE RIMIXER',
        'operative': 'Compose',
        'form': 'Work for generative literature',
        'year': 2026,
        'subtitle': None,
        'live_url': 'https://mozareeduge.github.io/taroke-remixer/',
        'repo_url': 'https://github.com/mozareeduge/taroke-remixer',
        'canonical_route': '/works/taroke-remixer/',
        'alias_route': '/taroke-remixer/',
        'meta': {
            'title': 'TAROKE RIMIXER - A Work for Generative Literature',
            'description': 'TAROKE RIMIXER is a browser-native creative work by Mozare for composing constrained generative literature through authored materials, rules, runtime, and revision.',
            'og_image_alt': 'TAROKE RIMIXER showing authored materials and a readable line-making route.',
        },
        'home_feature': {
            'form_line': 'Work for generative literature · 2026',
            'title': 'TAROKE RIMIXER',
            'subtitle': None,
            'copy': '*TAROKE RIMIXER* places the labor of generative writing on the worktable. A writer shapes material, grammar, recurrence, and duration, then reads the lines produced as evidence for revision.',
            'image_alt': 'TAROKE RIMIXER showing a readable line-making route beside authored material and constraint controls.',
            'frame_caption': 'Authored constraints / visible routes',
            'actions': (
                ('Open the work ↗', 'https://mozareeduge.github.io/taroke-remixer/'),
                ('About the work ->', '/works/taroke-remixer/'),
            ),
        },
        'works_index': {
            'form_line': 'Work for generative literature · 2026',
            'work_note': 'A poem-machine appears here as something a writer can build, test, and revise. Material banks, grammatical operations, line routes, recurrence, and runtime evidence become connected acts of composition.',
            'image_alt': 'TAROKE RIMIXER Run chamber showing generated lines and inspectable line evidence.',
            'action_label': 'View work page ->',
        },
        'project': {
            'form_line': 'A work for generative literature · by Mozare · 2026',
            'subtitle': None,
            'lead': '*TAROKE RIMIXER* opens the making of a generative poem as a literary environment. Material, grammar, line routes, recurrence, and runtime evidence remain close enough to be composed, tested, and revised together.',
            'actions': (
                ('Open the work ↗', 'https://mozareeduge.github.io/taroke-remixer/'),
                ('Source repository ↗', 'https://github.com/mozareeduge/taroke-remixer'),
            ),
            'hero_image_alt': 'TAROKE RIMIXER showing the Devices chamber with an authored line-making route in view.',
            'hero_frame_caption': 'Materials / routes / recurrence',
            'context_heading': 'Writing the machine that writes',
            'context_paragraphs': (
                'Every generative poem begins before its first generated line. Someone chooses the material, defines the possible movements, and decides how recurrence will occupy time. *TAROKE RIMIXER* gathers that labor into a compositional field where banks, inflection, line devices, stanza, flow, triggers, and surface settings can be written as parts of the work.',
                'Inside the workbench, every constraint has a literary address. A bank establishes available material and its relative pressure. A route composes syntactic relation. Stanza and flow shape recurrence across time. Runtime evidence brings generated lines back for judgment. Each layer offers the writer a different scale of attention.',
                "The name carries the remix lineage opened by Nick Montfort's *Taroko Gorge*, whose compact generator invited writers to replace its material and redirect its movement. *TAROKE RIMIXER* extends that invitation into a fuller environment for constructing a poem-machine and releasing it as an autonomous browser work.",
                'Authorship travels across selection, rule, timing, judgment, and revision. Probabilistic generation draws only from the material and constraints the writer has prepared. The lines that appear are therefore both poems and evidence: occasions to listen again to the language, then return to the machine and alter what it can do.',
            ),
            'selected_views': (
                {'view': '01 - Material banks', 'caption': "Named banks give the poem's available language a visible structure and relative weight.", 'alt': 'TAROKE RIMIXER Samples chamber showing named material banks and weighted entries.'},
                {'view': '02 - Readable route', 'caption': 'A line-making route presents grammar as an authored sequence of slots, forms, and probabilities.', 'alt': 'TAROKE RIMIXER Devices chamber showing a readable route template and slot controls.'},
                {'view': '03 - Runtime evidence', 'caption': 'Generated lines return to the writer with inspectable recipes that support keeping, repair, and revision.', 'alt': 'TAROKE RIMIXER Run chamber with generated lines and an open line recipe.'},
                {'view': '04 - Mobile chamber', 'caption': 'One compositional chamber receives the width of the phone while the wider project structure remains reachable.', 'alt': 'TAROKE RIMIXER on mobile with the Devices chamber open and chamber navigation visible.'},
            ),
            'details': (
                ('Form', 'Browser-native work for generative literature'),
                ('Artist', 'Mozare'),
                ('Citation name', 'Mohammad Zare'),
                ('Lineage', 'Taroko-style constrained generative poetry'),
                ('Generation', 'Probabilistic selection from authored materials and constraints'),
                ('Project form', 'Editable project data with standalone playable HTML export'),
                ('Storage', 'Local browser draft recovery and user-controlled exported files'),
                ('Live work', 'https://mozareeduge.github.io/taroke-remixer/'),
                ('Repository', 'https://github.com/mozareeduge/taroke-remixer'),
                ('Public state', 'v07.8 release checkpoint'),
                ('Rights', 'Copyright © 2026 Mohammad Zare. See the repository rights notice.'),
            ),
        },
    },
}

# ---------------------------------------------------------------------------
# Shared page copy: home, works index, practice, about, contact
# ---------------------------------------------------------------------------

SITE_COPY = {
    'home': {
        'meta': {
            'canonical_url': f'{SITE_ORIGIN}/',
            'title': f'{SITE_TITLE} - Works by {ARTISTIC_NAME}',
            'description': f'The online exhibition and archive of five browser-native works by {ARTISTIC_NAME}, shaped through artistic research, procedural writing, and interface design.',
            'og_title': f'{SITE_TITLE} - Works by {ARTISTIC_NAME}',
            'og_description': 'Five browser-native works in which research, writing, interface, and code take form together.',
            'og_image_alt': f'Five browser-native works presented across {SITE_TITLE} portfolio.',
        },
        'hero': {
            'h1': SITE_TITLE,
            'deck': 'Creative-critical works made where language meets the structures that carry, interrupt, and transform it.',
            'introduction': (
                "The Black Bird Field gathers five browser-native works by Mozare. Each grew around a different "
                "difficulty: how a source can enter a poem and still answer for where it came from; how nine short "
                "poems can be separated by darkness; how software's calm language changes when connection, "
                "recovery, and complaint all fail; how a play can return as a generative machine; and how the "
                "making of that machine can itself become a literary work. In the browser, these questions acquire "
                "space, duration, sequence, and touch."
            ),
            'actions': (
                ('View all works ->', '/works/'),
                ('About the practice ->', '/practice/'),
            ),
            'ledger': f'{ARTISTIC_NAME} / Five browser-native works / 2026',
        },
        'works_lead': {
            'section_label': '01 / WORKS',
            'h2': 'Five ways for language to take place',
            'body': 'Across the field, text arrives through relation, distance, interrupted transmission, recurrence, and composition. Each work asks attention to move at a different pace and leaves a different kind of trace.',
        },
        'practice_teaser': {
            'section_label': '02 / PRACTICE',
            'h2': 'Form begins by listening to the material',
            'body': 'A source arrives with provenance; a phrase with memory; a dramatic scene with the pressure of its first form; a set of rules with consequences across time. Each work builds the local structure these conditions ask for, allowing research, writing, interface, and code to change one another.',
            'propositions': (
                {'number': '01', 'title': 'Materials carry histories', 'body': 'Sources, phrases, translations, and dramatic scenes bring histories that continue to shape what they can become.'},
                {'number': '02', 'title': 'Procedures organize change', 'body': 'Rules of visibility, recurrence, failure, and generation turn time into a field of compositional decisions.'},
                {'number': '03', 'title': 'Interfaces compose attention', 'body': 'Space, duration, and reader action shape how language approaches, persists, and returns.'},
            ),
            'action': 'Read about the practice ->',
        },
        'about_strip': {
            'section_label': '03 / ABOUT',
            'h2': ARTISTIC_NAME,
            'body': f'{ARTISTIC_NAME} is the artistic name under which {FORMAL_NAME} presents literary and born-digital works. {FORMAL_NAME} remains the name attached to research records, citation, rights, and professional work.',
            'actions': (
                ('About Mozare ->', '/about/'),
                ('Download CV', CV_FILENAME),
            ),
        },
    },
    'works': {
        'meta': {
            'canonical_url': f'{SITE_ORIGIN}/works/',
            'title': f'Works - {SITE_TITLE}',
            'description': 'The Black Bird, Winter Road, UNHAPPY Scenario, Grave-Machine, and TAROKE RIMIXER: five browser-native works by Mozare.',
            'og_image_alt': 'Selected views from five browser-native works by Mozare.',
        },
        'mast': {
            'h1': 'Works',
            'body': 'Five browser-native works by Mozare. Each gives a different pressure in language its own space, duration, and procedure.',
        },
    },
    'practice': {
        'meta': {
            'canonical_url': f'{SITE_ORIGIN}/practice/',
            'title': f'Practice - {SITE_TITLE}',
            'description': 'Mozare develops browser-native literary forms by composing the conditions carried by sources, language, procedures, interfaces, and reader actions.',
            'og_image_alt': f'Selected materials, procedures, and interfaces from works in {SITE_TITLE}.',
        },
        'mast': {
            'h1': 'Practice',
            'body': 'Research, poetry, procedure, interface, and code are composed anew around the demands of each work.',
        },
        'introduction': (
            'Many works here begin when a material starts pressing against the form that first held it. A source wants to enter poetic relation while keeping the marks of where it came from. Nine haiku ask for darkness between them. A system phrase carries the memory of public infrastructure failing in private life. A dramatic scene finds another duration through generation. A poem-machine asks to expose the labor of its own construction.',
            'Method follows that pressure. A graph, a dark field, a deterministic loop, a bilingual generator, and a workbench are local answers to different materials. Their technical structures matter because they preserve literary distinctions, make particular actions possible, and leave traces a reader can return to.',
        ),
        'index': (
            {'number': '01', 'section': 'Materials arrive with conditions', 'anchor': '#materials'},
            {'number': '02', 'section': 'Procedures organize change', 'anchor': '#procedures'},
            {'number': '03', 'section': 'The interface composes attention', 'anchor': '#interface'},
            {'number': '04', 'section': 'Research remains answerable', 'anchor': '#research'},
            {'number': '05', 'section': 'Language and location remain situated', 'anchor': '#language'},
        ),
        'modules': (
            {
                'number': '01', 'anchor': 'materials', 'heading': 'Materials arrive with conditions',
                'paragraphs': (
                    'A source, a translation, a system phrase, a dramatic fragment, and a line of verse arrive through different histories. Provenance clings to a source. Translation holds one language against another. A system phrase carries an operational promise. A dramatic fragment remembers the stage and pressure from which it came.',
                    'Composition begins by giving these differences somewhere to live. In *The Black Bird*, object types govern how scenes, names, citations, and relations enter the field. In *UNHAPPY Scenario*, system messages keep their procedural register while repetition changes what that register can carry. Material history becomes active inside the form.',
                ),
            },
            {
                'number': '02', 'anchor': 'procedures', 'heading': 'Procedures organize change',
                'paragraphs': (
                    'A procedure gives consequence to an event: this change opens one possibility, delays another, or leaves a trace that will shape what follows. Across the field, procedures govern visibility, recurrence, failure, generation, and return. Their literary force gathers through time.',
                    'A proximity rule lets a haiku brighten. A deterministic sequence wears down the promise of recovery. A generative route brings prepared words into relation. A runtime receipt keeps the construction of a line close to the line itself. Authorship moves through material, rule, timing, and the patient revision of what those choices produce.',
                ),
            },
            {
                'number': '03', 'anchor': 'interface', 'heading': 'The interface composes attention',
                'paragraphs': (
                    "An interface distributes visibility, duration, adjacency, and action. It decides what can be held together, what asks for approach, what fades after attention moves, and what a reader's gesture adds to the work.",
                    'The graph and Reader of *The Black Bird* coordinate spatial relation with textual duration. The near-black field of *Winter Road* gives distance a reading function. *UNHAPPY Scenario* places procedural failure beside the field that receives its language. *Grave-Machine* keeps generated lines beside their evidence. *TAROKE RIMIXER* turns the construction of recurrence into a place of writing.',
                    'The browser enters the practice through concrete capacities: state, timing, focus, persistence, input, and responsive space. Design becomes literary when those capacities are tuned toward a precise consequence in language and attention.',
                ),
            },
            {
                'number': '04', 'anchor': 'research', 'heading': 'Research remains answerable',
                'paragraphs': (
                    'Speculative research poetry gives a possible relation a place before certainty closes around it. The relation may carry enough pressure to enter poetic form while still showing the support on which it rests. A reader can approach it, follow it elsewhere, or leave it open.',
                    'Citation, source routes, object types, runtime evidence, and release records make return possible. They lead back toward the material behind a relation and mark how far a claim may travel from that ground. Accountability becomes a formal practice built into the work from the beginning.',
                ),
            },
            {
                'number': '05', 'anchor': 'language', 'heading': 'Language and location remain situated',
                'paragraphs': (
                    'The languages of the field carry different histories. Several works are English; *Grave-Machine* moves between English and Persian; source-language names remain visible when their written form carries part of a relation. This unevenness belongs to the present life and location of the works.',
                    'Typography, translation, direction, and naming are authored wherever another script enters. Translation creates a new linguistic composition. A source-language name may keep its form inside an English field. A work in one language can state the boundary of its current edition. Language remains a material choice with historical and formal weight.',
                ),
            },
        ),
        'closing': 'Across the field, technical structure earns its place by carrying a literary distinction that would otherwise be lost. Each work tries to reveal its conditions at the scale its material requires, then leaves enough air for a reader to make a partial route of their own.',
    },
    'about': {
        'meta': {
            'canonical_url': f'{SITE_ORIGIN}/about/',
            'title': f'About - {SITE_TITLE}',
            'description': 'About Mozare and Mohammad Zare, an Iranian poet, researcher, and product/interface practitioner working across dramatic literature and born-digital form.',
        },
        'mast': {
            'h1': 'About',
            'body': f'{ARTISTIC_NAME} is the artistic name carried by the works. {FORMAL_NAME} is the name attached to academic records, citation, rights, and professional practice.',
        },
        'biography': (
            'Mohammad Zare is an Iranian poet, researcher, and product/interface practitioner. Under the artistic name Mozare, he makes literary works in which sources, procedures, interfaces, and reader actions remain active within the form.',
            'He studied Industrial Engineering at Sharif University of Technology and completed an MA in Dramatic Literature at the University of Art, Tehran. His MA research examined ugliness in the plays of Abbas Nalbandian through Deleuze and Guattari\'s concept of minor literature. Its practical component was the original play *Grave*, developed beside the theoretical research as an autonomous dramatic work.',
            "His path into browser-native literature runs through playwriting, speculative research poetry, translation, and critical writing. These practices meet in works that give research materials, poetic relations, and generative procedures their own public bodies.",
            "Product and interface work adds another discipline: data structures have to hold together, complex behavior has to survive testing, and a surface has to reveal enough of its structure to be used with care. *The Black Bird Field* gathers the works in which this discipline meets his literary and research practice.",
        ),
        'identity_ledger': (
            ('Artistic name', ARTISTIC_NAME),
            ('Formal name', FORMAL_NAME),
            ('Education', 'MA Dramatic Literature, University of Art, Tehran'),
            ('Education', 'BSc Industrial Engineering, Sharif University of Technology'),
            ('Current practice', 'Born-digital literature / speculative research poetry / generative writing / interface practice'),
        ),
        'actions': (
            ('Download CV', CV_FILENAME),
            ('LinkedIn profile ↗', LINKEDIN_URL),
            ('Contact ->', '/contact/'),
        ),
    },
    'contact': {
        'meta': {
            'canonical_url': f'{SITE_ORIGIN}/contact/',
            'title': f'Contact - {SITE_TITLE}',
            'description': 'Contact Mozare regarding the works, their research, publication, exhibition, or possible collaboration.',
        },
        'mast': {
            'h1': 'Contact',
            'body': 'For enquiries about a work, its research, publication or exhibition, and for possible collaborations, write to Mozare.',
        },
        'links': (
            {'label': 'Email', 'value': EMAIL, 'href': f'mailto:{EMAIL}'},
            {'label': 'LinkedIn', 'value': 'Mohammad Zare', 'href': LINKEDIN_URL},
        ),
    },
}

# ---------------------------------------------------------------------------
# Prohibited rhetorical formulas — visitor-facing copy must contain zero.
# ---------------------------------------------------------------------------

PROHIBITED_FORMULAS = (
    'not merely', 'rather than', 'instead of', 'unlike traditional',
    'at the intersection of', 'groundbreaking', 'cutting-edge', 'innovative project',
)
