"""Pure HTML rendering functions for The Black Bird Field.

Functions here return HTML strings. Plain-text content values are escaped
by default; the only permitted markup transform is `emphasize()`, which
resolves the single-asterisk emphasis markers used in src/content.py into
<em> tags. This is a narrow, closed transform (it recognises nothing else)
rather than a general Markdown runtime.
"""

from __future__ import annotations

import json
import re
from html import escape as _escape
from pathlib import Path

_EMPHASIS_RE = re.compile(r'\*([^*]+)\*')

_MANIFEST_PATH = Path(__file__).resolve().parents[1] / 'docs' / 'ASSET_MANIFEST.json'
_DIMENSIONS_BY_PATH: dict[str, tuple[int, int]] = {}
if _MANIFEST_PATH.is_file():
    for _entry in json.loads(_MANIFEST_PATH.read_text(encoding='utf-8')).get('assets', []):
        _dims = _entry['output_dimensions']
        _site_path = _entry['path'].removeprefix('public/')
        _DIMENSIONS_BY_PATH[_site_path] = (_dims['width'], _dims['height'])


def escape(text: str) -> str:
    return _escape(str(text), quote=True)


_ARABIC_SCRIPT_RUN_RE = re.compile(r'[؀-ۿ][؀-ۿ\s]*[؀-ۿ]|[؀-ۿ]')


def wrap_script_runs(escaped_text: str) -> str:
    """Wrap contiguous Arabic-script (Persian) runs in explicit lang/dir
    (D-TYPOGRAPHY: 'Persian content receives explicit language and
    direction'). Input must already be HTML-escaped."""
    return _ARABIC_SCRIPT_RUN_RE.sub(
        lambda m: f'<span lang="fa" dir="rtl" class="script-fa">{m.group(0)}</span>', escaped_text
    )


def emphasize(text: str) -> str:
    """Escape text, resolve *word* markers into <em>word</em>, and wrap any
    Persian script runs with explicit lang/dir."""
    escaped = escape(text)
    escaped = wrap_script_runs(escaped)
    return _EMPHASIS_RE.sub(lambda m: f'<em>{m.group(1)}</em>', escaped)


def resolve_href(href: str, prefix: str) -> str:
    """Resolve a content-authority href against the current page's prefix."""
    if href.startswith(('http://', 'https://', 'mailto:', '#')):
        return href
    return prefix + href.lstrip('/')


def is_external(href: str) -> bool:
    return href.startswith(('http://', 'https://'))


def render_action(label: str, href: str, prefix: str, css_class: str = 'action') -> str:
    target = resolve_href(href, prefix)
    extra = ''
    if is_external(href):
        extra = ' target="_blank" rel="noopener"'
        sr = '<span class="sr-only"> (opens in new tab)</span>'
    else:
        sr = ''
    return f'<a class="{css_class}" href="{escape(target)}"{extra}>{escape(label)}{sr}</a>'


def render_actions(actions, prefix: str, css_class: str = 'actions', item_class: str = 'action') -> str:
    items = ''.join(render_action(label, href, prefix, item_class) for label, href in actions)
    return f'<div class="{css_class}">{items}</div>'


def render_ledger(rows, css_class: str = 'ledger') -> str:
    """Render (label, value) pairs as a <dl>. Values may be a URL, which
    becomes a link with a human label rather than a raw protocol string.
    """
    items = []
    for label, value in rows:
        value_html = emphasize(value)
        if isinstance(value, str) and value.startswith(('http://', 'https://')):
            value_html = f'<a href="{escape(value)}" target="_blank" rel="noopener">{escape(value)}<span class="sr-only"> (opens in new tab)</span></a>'
        items.append(f'<div class="ledger-row"><dt>{escape(label)}</dt><dd>{value_html}</dd></div>')
    return f'<dl class="{css_class}">{"".join(items)}</dl>'


def render_picture(image_path: str, alt: str, prefix: str, css_class: str = '', loading: str = 'lazy', fetchpriority: str = None) -> str:
    """Render a single-source <img> with intrinsic dimensions.

    Width/height come from docs/ASSET_MANIFEST.json so the browser can
    reserve layout space before the image loads (R-PERFORMANCE, CLS).
    A future responsive-image pass may add <picture> sources / srcset;
    this already renders a fully working, dimensioned <img>.
    """
    src = resolve_href(image_path, prefix)
    cls = f' class="{escape(css_class)}"' if css_class else ''
    prio = f' fetchpriority="{fetchpriority}"' if fetchpriority else ''
    decoding = ' decoding="async"'
    dims = _DIMENSIONS_BY_PATH.get(image_path)
    size_attrs = f' width="{dims[0]}" height="{dims[1]}"' if dims else ''
    return f'<img{cls} src="{escape(src)}"{size_attrs} alt="{escape(alt)}" loading="{loading}"{decoding}{prio}>'


def render_selected_views(views, images, prefix: str) -> str:
    """views: content.WORKS[key]['project']['selected_views']
    images: list of asset paths (site-root relative), aligned by index.
    """
    figures = []
    for i, view in enumerate(views):
        number = view['view'].split(' - ')[0]
        img = images[i] if i < len(images) else images[-1]
        picture = render_picture(img, view['alt'], prefix, css_class='project-view-image')
        figures.append(
            f'<figure class="project-view project-view--{number}">'
            f'{picture}'
            f'<figcaption><span class="view-number">{escape(number)}</span>'
            f'<span class="view-caption">{emphasize(view["caption"])}</span></figcaption>'
            f'</figure>'
        )
    return f'<div class="selected-views-grid">{"".join(figures)}</div>'


def render_project(work_key: str, work: dict, prefix: str, is_alias: bool = False) -> str:
    project = work['project']
    subtitle_html = f'<p class="project-subtitle">{escape(project["subtitle"])}</p>' if project.get('subtitle') else ''
    hero_image = work['assets']['hero']
    context_paragraphs = ''.join(f'<p>{emphasize(p)}</p>' for p in project['context_paragraphs'])
    view_images = work['assets']['views']
    locked = project.get('locked_textual_authority')
    locked_html = f'<p class="locked-note">{emphasize(locked)}</p>' if locked else ''

    return f'''
<article class="project-hero inverse">
  <div class="project-hero-copy">
    <p class="form-line">{escape(project["form_line"])}</p>
    <h1>{escape(work["title"])}</h1>
    {subtitle_html}
    <p class="lead">{emphasize(project["lead"])}</p>
    {render_actions(project["actions"], prefix)}
  </div>
  <figure class="project-hero-media">
    {render_picture(hero_image, project["hero_image_alt"], prefix, css_class="project-hero-image", loading="eager", fetchpriority="high")}
    <figcaption>{escape(project["hero_frame_caption"])}</figcaption>
  </figure>
</article>
<section class="project-context" aria-labelledby="context-heading">
  <p class="section-label">CONTEXT</p>
  <h2 id="context-heading">{escape(project["context_heading"])}</h2>
  <div class="context-essay">{context_paragraphs}</div>
</section>
<section class="selected-views" aria-labelledby="views-heading">
  <p class="section-label">SELECTED VIEWS</p>
  <h2 id="views-heading">A relation, held long enough to read</h2>
  {render_selected_views(project["selected_views"], view_images, prefix)}
</section>
<section class="work-details inverse" aria-labelledby="details-heading">
  <h2 id="details-heading">Work details</h2>
  {render_ledger(project["details"])}
  {locked_html}
</section>
'''


def render_home_hero(hero: dict, works, work_order, prefix: str) -> str:
    index_rows = ''.join(
        f'<li><a href="{escape(resolve_href(works[k]["canonical_route"], prefix))}" data-preview-index="{i}">'
        f'<span class="work-no">{i:02d}</span>'
        f'<span class="work-title">{escape(works[k]["title"])}</span>'
        f'<span class="work-operative">{escape(works[k]["operative"])}</span></a></li>'
        for i, k in enumerate(work_order, 1)
    )

    def preview_image(i, k):
        img = render_picture(
            works[k]['assets']['hero_preview'],
            works[k]['home_feature']['image_alt'], prefix,
            css_class='hero-preview-image' + ('' if i == 1 else ' is-inactive'),
            loading='eager' if i == 1 else 'lazy',
            fetchpriority='high' if i == 1 else None,
        )
        caption = escape(works[k]['home_feature']['frame_caption'])
        return img[:-1] + f' data-preview-index="{i}" data-caption="{caption}">'

    return f'''
<section class="hero-field">
  <div class="hero-copy">
    <h1>{escape(hero["h1"])}</h1>
    <p class="hero-deck">{escape(hero["deck"])}</p>
    <p class="hero-introduction">{emphasize(hero["introduction"])}</p>
    {render_actions(hero["actions"], prefix)}
  </div>
  <div class="hero-preview" data-home-preview>
    {"".join(preview_image(i, k) for i, k in enumerate(work_order, 1))}
    <p class="hero-preview-caption" data-preview-caption>{escape(works[work_order[0]]['home_feature']['frame_caption'])}</p>
  </div>
  <nav class="hero-work-index" aria-label="Works">
    <ol>{index_rows}</ol>
  </nav>
  <p class="hero-ledger">{escape(hero["ledger"])}</p>
</section>
'''


def render_home_features(works, work_order, prefix: str) -> str:
    features = []
    for i, k in enumerate(work_order, 1):
        w = works[k]
        f = w['home_feature']
        subtitle_html = f'<p class="feature-subtitle">{escape(f["subtitle"])}</p>' if f.get('subtitle') else ''
        img = w['assets']['home_feature']
        features.append(f'''
<article class="home-feature home-feature--{i:02d}">
  <figure class="feature-media">
    {render_picture(img, f["image_alt"], prefix, css_class="feature-image")}
    <figcaption>{escape(f["frame_caption"])}</figcaption>
  </figure>
  <div class="feature-copy">
    <p class="form-line">{escape(f["form_line"])}</p>
    <h3>{escape(f["title"])}</h3>
    {subtitle_html}
    <p>{emphasize(f["copy"])}</p>
    {render_actions(f["actions"], prefix, item_class="action action--secondary")}
  </div>
</article>''')
    return f'<div class="home-feature-sequence inverse">{"".join(features)}</div>'


def render_home(site_copy: dict, works, work_order, prefix: str) -> str:
    home = site_copy['home']
    lead = home['works_lead']
    teaser = home['practice_teaser']
    about = home['about_strip']
    propositions = ''.join(
        f'<div class="proposition"><p class="proposition-number">{escape(p["number"])}</p>'
        f'<h3>{escape(p["title"])}</h3><p>{escape(p["body"])}</p></div>'
        for p in teaser['propositions']
    )
    return f'''
{render_home_hero(home["hero"], works, work_order, prefix)}
<section class="works-lead">
  <p class="section-label">{escape(lead["section_label"])}</p>
  <h2>{escape(lead["h2"])}</h2>
  <p>{escape(lead["body"])}</p>
</section>
{render_home_features(works, work_order, prefix)}
<section class="practice-teaser inverse">
  <p class="section-label">{escape(teaser["section_label"])}</p>
  <h2>{escape(teaser["h2"])}</h2>
  <p>{escape(teaser["body"])}</p>
  <div class="propositions">{propositions}</div>
  <a class="action" href="{escape(resolve_href('/practice/', prefix))}">{escape(teaser["action"])}</a>
</section>
<section class="about-strip">
  <p class="section-label">{escape(about["section_label"])}</p>
  <h2>{escape(about["h2"])}</h2>
  <p>{escape(about["body"])}</p>
  {render_actions(about["actions"], prefix)}
</section>
'''


def render_works_index(site_copy: dict, works, work_order, prefix: str) -> str:
    mast = site_copy['works']['mast']
    rows = []
    for i, k in enumerate(work_order, 1):
        w = works[k]
        idx = w['works_index']
        img = w['assets']['works_thumb']
        rows.append(f'''
<article class="works-row">
  <span class="work-no">{i:02d}</span>
  <div class="work-title-block">
    <h2>{escape(w["title"])}</h2>
    <p class="form-line">{escape(idx["form_line"])}</p>
  </div>
  <div class="work-note">
    <p>{emphasize(idx["work_note"])}</p>
    <a class="action" href="{escape(resolve_href(w["canonical_route"], prefix))}">{escape(idx["action_label"])}</a>
  </div>
  {render_picture(img, idx["image_alt"], prefix, css_class="works-thumb")}
</article>''')
    return f'''
<section class="works-mast">
  <h1>{escape(mast["h1"])}</h1>
  <p>{escape(mast["body"])}</p>
</section>
<div class="works-list">{"".join(rows)}</div>
'''


def render_practice(site_copy: dict) -> str:
    practice = site_copy['practice']
    index_items = ''.join(
        f'<li><a href="{escape(item["anchor"])}"><span>{escape(item["number"])}</span>{escape(item["section"])}</a></li>'
        for item in practice['index']
    )
    intro = ''.join(f'<p>{escape(p)}</p>' for p in practice['introduction'])
    modules = ''.join(
        f'<section class="practice-module" id="{escape(m["anchor"])}" aria-labelledby="module-{escape(m["anchor"])}">'
        f'<p class="module-number">{escape(m["number"])}</p>'
        f'<h2 id="module-{escape(m["anchor"])}">{escape(m["heading"])}</h2>'
        f'{"".join(f"<p>{emphasize(p)}</p>" for p in m["paragraphs"])}'
        f'</section>'
        for m in practice['modules']
    )
    return f'''
<section class="practice-mast">
  <h1>{escape(practice["mast"]["h1"])}</h1>
  <p>{escape(practice["mast"]["body"])}</p>
</section>
<div class="practice-introduction">{intro}</div>
<nav class="practice-index" aria-label="Practice sections"><ol>{index_items}</ol></nav>
<div class="practice-modules">{modules}</div>
<p class="practice-closing">{escape(practice["closing"])}</p>
'''


def render_about(site_copy: dict, prefix: str) -> str:
    about = site_copy['about']
    bio = ''.join(f'<p>{emphasize(p)}</p>' for p in about['biography'])
    return f'''
<section class="about-mast">
  <h1>{escape(about["mast"]["h1"])}</h1>
  <p>{escape(about["mast"]["body"])}</p>
</section>
<div class="about-biography">{bio}</div>
{render_ledger(about["identity_ledger"], css_class="ledger identity-ledger")}
{render_actions(about["actions"], prefix)}
'''


def render_contact(site_copy: dict) -> str:
    contact = site_copy['contact']
    links = ''.join(
        f'<a class="contact-row" href="{escape(link["href"])}">'
        f'<span class="contact-label">{escape(link["label"])}</span>'
        f'<span class="contact-value">{escape(link["value"])}</span>'
        f'<span class="contact-arrow" aria-hidden="true">→</span></a>'
        for link in contact['links']
    )
    return f'''
<section class="contact-mast">
  <h1>{escape(contact["mast"]["h1"])}</h1>
  <p>{escape(contact["mast"]["body"])}</p>
</section>
<div class="contact-links">{links}</div>
'''
