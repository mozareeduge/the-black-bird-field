from __future__ import annotations
from html import escape
from pathlib import Path

NUMBERS = {0:"zero",1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",10:"ten",11:"eleven",12:"twelve",13:"thirteen",14:"fourteen",15:"fifteen",16:"sixteen",17:"seventeen",18:"eighteen",19:"nineteen",20:"twenty"}

def num_word(n:int, cap:bool=False) -> str:
    s = NUMBERS.get(n, str(n))
    return s.capitalize() if cap else s

def path_prefix(output: str) -> str:
    depth = len(Path(output).parent.parts)
    return "../" * depth

def work_path(work:dict) -> str:
    return f"works/{work['slug']}/index.html"

def ext_attrs(url:str) -> str:
    return ' target="_blank" rel="noopener noreferrer"' if url.startswith(("http://","https://")) else ""

def esc(s) -> str:
    return escape(str(s), quote=True)

def fmt(text:str, works:list[dict]) -> str:
    n=len(works); titles=", ".join(w["title"] for w in works[:-1]) + ((", and " if n>2 else " and ") + works[-1]["title"] if n>1 else works[0]["title"])
    return text.format(count=n,count_word=num_word(n),Count_word=num_word(n,True),work_titles=titles)

def picture(prefix:str, work:dict, role:str, alt:str, cls:str="", caption:tuple[str,str]|None=None, eager:bool=False) -> str:
    asset=work["asset_slug"]
    desktop=f"{prefix}assets/{asset}/{role}-desktop.webp"
    mobile=f"{prefix}assets/{asset}/{role}-mobile.webp"
    attr=' fetchpriority="high"' if eager else ''
    inner=f'<picture><source media="(max-width:760px)" srcset="{esc(mobile)}"><img alt="{esc(alt)}" src="{esc(desktop)}"{attr}></picture>'
    if caption:
        inner += f'<div class="caption"><span>{esc(caption[0])}</span><span>{esc(caption[1])}</span></div>'
    return f'<div class="picture{(" "+cls) if cls else ""}">{inner}</div>'

def motion_picture(prefix:str, work:dict, alt:str, cls:str="", caption:tuple[str,str]|None=None, eager:bool=False, surface:str="project") -> str:
    motion=work.get("motion") or {}
    role=motion.get("fallback_role") or work["feature_image"]
    asset=work["asset_slug"]
    desktop=f"{prefix}assets/{asset}/{role}-desktop.webp"
    mobile=f"{prefix}assets/{asset}/{role}-mobile.webp"
    attr=' fetchpriority="high"' if eager else ''
    inner=f'<picture class="motion-poster"><source media="(max-width:760px)" srcset="{esc(mobile)}"><img alt="{esc(alt)}" src="{esc(desktop)}"{attr}></picture>'
    if motion.get("enabled"):
        vd=f"{prefix}assets/{asset}/{motion['desktop_file']}"
        vm=f"{prefix}assets/{asset}/{motion['mobile_file']}"
        inner += f'<video class="motion-video" muted loop playsinline preload="none" data-motion-video data-motion-desktop="{esc(vd)}" data-motion-mobile="{esc(vm)}" aria-hidden="true"></video>'
    if caption:
        inner += f'<div class="caption"><span>{esc(caption[0])}</span><span>{esc(caption[1])}</span></div>'
    return f'<div class="picture motion-media{(" "+cls) if cls else ""}" data-motion-surface="{esc(surface)}">{inner}</div>'

def header(prefix:str,current:str,site:dict) -> str:
    def curr(key): return ' aria-current="page"' if current==key else ''
    return f'''<a class="skip" href="#main">Skip to main content</a><header class="site-header"><a class="wordmark" href="{prefix}index.html"><strong>{esc(site['site_title'])}</strong><small>works by {esc(site['artistic_name'])}</small></a><nav aria-label="Primary" class="nav"><a{curr('works')} href="{prefix}works/index.html">Works</a><a{curr('practice')} href="{prefix}practice/index.html">Practice</a><a{curr('about')} href="{prefix}about/index.html">About</a></nav><nav aria-label="Utility" class="utility"><a{curr('contact')} href="{prefix}contact/index.html">Contact</a></nav><button aria-controls="site-menu" aria-expanded="false" class="menu-toggle" data-menu-open>Menu</button></header><noscript><nav aria-label="Primary navigation — JavaScript unavailable" class="noscript-nav"><a href="{prefix}works/index.html">Works</a><a href="{prefix}practice/index.html">Practice</a><a href="{prefix}about/index.html">About</a><a href="{prefix}contact/index.html">Contact</a></nav></noscript><dialog aria-labelledby="site-menu-title" class="menu" data-menu id="site-menu"><div class="menu-shell"><div class="menu-head"><strong id="site-menu-title">{esc(site['site_title'])}</strong><button class="menu-close" data-menu-close>Close</button></div><nav aria-label="Menu" class="menu-links"><a href="{prefix}works/index.html"><span>01</span><strong>Works</strong><small>Open</small></a><a href="{prefix}practice/index.html"><span>02</span><strong>Practice</strong><small>Open</small></a><a href="{prefix}about/index.html"><span>03</span><strong>About</strong><small>Open</small></a><a href="{prefix}contact/index.html"><span>04</span><strong>Contact</strong><small>Open</small></a></nav><div class="menu-foot"><span>Artistic work: {esc(site['artistic_name'])}.</span><span>{esc(site['shared']['menu_name_boundary'])}</span></div></div></dialog>'''

def footer(prefix:str,site:dict,works:list[dict]) -> str:
    return f'''<footer class="site-footer"><div class="footer-identity"><strong>{esc(site['artistic_name'])}</strong><p>{esc(site['shared']['footer_identity'])}</p><small>{esc(site['shared']['name_boundary'])}</small></div><nav aria-label="Footer"><a href="{prefix}works/index.html">Works</a><a href="{prefix}practice/index.html">Practice</a><a href="{prefix}about/index.html">About</a><a href="{prefix}contact/index.html">Contact</a><a href="{esc(site['github_profile'])}" target="_blank" rel="noopener noreferrer">GitHub ↗</a></nav><div class="footer-meta"><p>{esc(fmt('The Black Bird Field presents {count_word} autonomous browser-native works.',works))}</p><p>© {esc(site['year'])} {esc(site['formal_name'])}.</p></div></footer>'''

def document(*,output:str,title:str,description:str,canonical:str,body_class:str,current:str,main:str,site:dict,works:list[dict],og_image:str|None=None,robots:str|None=None) -> str:
    prefix=path_prefix(output)
    img = f'<meta property="og:image" content="{esc(site["site_origin"]+"/"+og_image)}"><meta name="twitter:image" content="{esc(site["site_origin"]+"/"+og_image)}">' if og_image else ''
    robot = f'<meta name="robots" content="{esc(robots)}">' if robots else ''
    csp="default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'"
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="stylesheet" href="{prefix}site.css"><link rel="canonical" href="{esc(canonical)}"><meta http-equiv="Content-Security-Policy" content="{esc(csp)}"><meta name="referrer" content="strict-origin-when-cross-origin">{robot}<meta property="og:type" content="website"><meta property="og:url" content="{esc(canonical)}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">{img}<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"></head><body class="{esc(body_class)}">{header(prefix,current,site)}<main id="main">{main}</main>{footer(prefix,site,works)}<script src="{prefix}site.js"></script></body></html>'''

def render_home(site:dict,works:list[dict]) -> tuple[str,str,str,str]:
    prefix=""; n=len(works)
    resp=[w['responsibility'] for w in works]
    if len(resp)==1: responsibilities=resp[0]
    elif len(resp)==2: responsibilities=f"{resp[0]} and {resp[1]}"
    else: responsibilities="; ".join(resp[:-1])+f"; and {resp[-1]}"
    hero_intro=f"The field gathers {num_word(n)} autonomous works. Each gives the browser another literary responsibility: {responsibilities}."
    # Critical: frames deliberately use the SAME order as index links. JS activates by index.
    frames=[]
    for i,w in enumerate(works):
        active=' active' if i==0 else ''
        media=motion_picture('',w,f"{w['title']} primary surface",eager=(i==0),surface='home')
        frames.append(f'<div class="preview-frame{active}" data-preview-frame data-work-slug="{esc(w["slug"])}">{media}</div>')
    index=[]
    for i,w in enumerate(works,1):
        index.append(f'<a data-caption="{i:02d} · {esc(w["title"])}" data-preview-index data-work-slug="{esc(w["slug"])}" href="{work_path(w)}"><span>{i:02d}</span><b>{esc(w["title"])}</b><small>{esc(w["mode"])}</small></a>')
    features=[]
    for i,w in enumerate(works,1):
        media=picture('',w,w['feature_image'],f"{w['title']} selected view",caption=(w['form'],w['feature_caption']))
        features.append(f'''<article class="feature"><div class="work-no">{i:02d}</div><div class="feature-media">{media}</div><div class="feature-copy"><p class="eyebrow">{esc(w['form'])} · {esc(w['year'])}</p><h2>{esc(w['title'])}</h2><p>{esc(w['summary'])}</p><div class="action-group"><a class="action primary" href="{esc(w['live_url'])}" target="_blank" rel="noopener noreferrer"><span>Enter the work</span><span>↗</span></a><a class="action secondary" href="{work_path(w)}"><span>About the work</span><span>→</span></a></div></div></article>''')
    mods=''.join(f'<article><span class="work-no">{m["index"]}</span><h3>{esc(m["home_title"])}</h3><p>{esc(m["home_text"])}</p></article>' for m in site['practice']['modules'])
    main=f'''<section class="hero"><div class="hero-copy"><h1>{esc(site['site_title'])}</h1><p class="hero-deck">{esc(site['shared']['deck'])}</p><p class="hero-intro">{esc(hero_intro)}</p><div class="action-group"><a class="action primary" href="works/index.html"><span>View all works</span><span>→</span></a><a class="action secondary" href="practice/index.html"><span>About the practice</span><span>→</span></a></div></div><div class="hero-preview">{''.join(frames)}<div class="preview-caption"><span data-preview-caption>01 · {esc(works[0]['title'])}</span><span>Work preview</span></div></div><nav aria-label="Works" class="hero-index"><p>{esc(num_word(n,True))} works</p>{''.join(index)}</nav><div class="hero-ledger"><span>{esc(site['artistic_name'])}</span><span>{esc(num_word(n,True))} browser-native works</span><span>{esc(site['year'])}</span></div></section><section class="section-lead"><span class="section-no">01 / WORKS</span><div><h2>{esc(num_word(n,True))} ways to enter the writing</h2><p>{esc(site['shared']['section_intro'])}</p></div></section><section class="features inverse">{''.join(features)}</section><section class="practice-teaser inverse"><div class="section-lead"><span class="section-no">02 / PRACTICE</span><div><h2>{esc(site['practice']['home_teaser']['title'])}</h2><p>{esc(site['practice']['home_teaser']['text'])}</p></div></div><div class="practice-grid">{mods}</div></section><section class="about-strip"><span class="section-no">03 / ABOUT</span><p>{esc(site['shared']['about_strip'])}</p><div class="about-strip-action"><a class="action primary" href="about/index.html"><span>About Mozare</span><span>→</span></a></div></section>'''
    return "index.html",f"Works by Mozare — {site['site_title']}",fmt(site['metadata']['home'],works),main

def render_works(site,works):
    rows=[]
    for i,w in enumerate(works,1):
        role=w['feature_image']; asset=w['asset_slug']; href=f"{w['slug']}/index.html"
        rows.append(f'''<article class="work-row"><div class="work-no">{i:02d}</div><div><h2>{esc(w['title'])}</h2><div class="form">{esc(w['form'])} · {esc(w['year'])}</div><div class="version">{esc(w['feature_caption'])}</div></div><div><p>{esc(w['summary'])}</p><div class="action-group"><a class="action secondary" href="{esc(href)}"><span>View work page</span><span>→</span></a></div></div><a class="thumb picture" href="{esc(href)}"><picture><source media="(max-width:760px)" srcset="../assets/{esc(asset)}/{esc(role)}-mobile.webp"><img alt="{esc(w['title'])} selected view" src="../assets/{esc(asset)}/{esc(role)}-desktop.webp"></picture></a></article>''')
    main=f'<section class="page-mast"><h1>Works</h1><p>{esc(num_word(len(works),True))} autonomous browser-native works by Mozare. Each gives reading another condition and asks the browser to carry it in another way.</p></section><section class="works-list">{"".join(rows)}</section>'
    return "works/index.html",f"Works — {site['site_title']}",fmt(site['metadata']['works'],works),main

def render_project(site,works,w):
    p="../../"; cls="project-page"+(" "+w.get('body_class','') if w.get('body_class') else '')
    title_html=''.join(f'<span>{esc(x)}</span>' for x in w.get('title_parts',[w['title']])) if len(w.get('title_parts',[w['title']]))>1 else esc(w['title'])
    hero_pic=motion_picture(p,w,f"{w['title']} threshold or primary surface",caption=("Primary surface",w['poster_caption']),eager=True,surface='project')
    conditions=''.join(f'<article><span class="step">{esc(x[0])}</span><h2>{esc(x[1])}</h2>{f"<p>{esc(x[2])}</p>" if x[2] else ""}</article>' for x in w['prelude']['items'])
    view_articles=[]
    for no,title,text,role,alt in w['views']['items']:
        asset=w['asset_slug']; img=f'<picture><source media="(max-width:760px)" srcset="{p}assets/{esc(asset)}/{esc(role)}-mobile.webp"><img alt="{esc(alt)}" src="{p}assets/{esc(asset)}/{esc(role)}-desktop.webp"></picture>'
        view_articles.append(f'<article class="view-plate"><div class="view-image">{img}</div><div class="view-copy"><span class="view-no">{esc(no)}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></div></article>')
    context=''.join(f'<p>{esc(x)}</p>' for x in w['context']['paragraphs'])
    coda=f'<p class="context-coda">{esc(w["context"]["coda"])}</p>' if w['context'].get('coda') else ''
    cite=w['citation']; citation=f'{esc(cite["author"])} <em>{esc(cite["title"])}</em>. {esc(cite["rest"])}'
    cells=[
      ("Form",esc(w['form'])),("Artist",esc(site['artistic_name'])),("Citation name",esc(site['formal_name'])),("Edition / build",esc(w['identity']['edition'])),("Language",esc(w['identity']['language'])),("Encounter",esc(w['identity']['encounter'])),
      ("Live work",f'<a href="{esc(w["live_url"])}" target="_blank" rel="noopener noreferrer">Open work ↗</a>'),("Repository",f'<a href="{esc(w["repository_url"])}" target="_blank" rel="noopener noreferrer">Open source record ↗</a>'),("Citation",citation)]
    cells_html=''.join(f'<div class="edition-cell"><span class="meta-label">{esc(label)}</span>{value if value.startswith("<a") else f"<strong>{value}</strong>"}</div>' for label,value in cells)
    main=f'''<section class="project-hero inverse"><div class="project-hero-inner"><div class="project-copy"><p class="project-form">{esc(w['form'])} · by {esc(site['artistic_name'])} · {esc(w['year'])}</p><h1>{title_html}</h1><p class="lead">{esc(w['hero_lead'])}</p><div class="action-group"><a class="action primary" href="{esc(w['live_url'])}" target="_blank" rel="noopener noreferrer"><span>Enter the work</span><span>↗</span></a><a class="action secondary" href="{esc(w['repository_url'])}" target="_blank" rel="noopener noreferrer"><span>Source and rights</span><span>↗</span></a></div></div><div class="project-hero-media">{hero_pic}</div></div></section><section class="prelude"><span class="section-no">{esc(w['prelude']['label'])}</span>{conditions}</section><section class="selected-views"><div class="views-inner"><div class="views-head"><span class="section-no">SELECTED VIEWS</span><h2>{esc(w['views']['title'])}</h2><p>{esc(w['views']['intro'])}</p></div>{''.join(view_articles)}</div></section><section class="project-context"><div class="context-inner"><span class="section-no">CONTEXT</span><h2>{esc(w['context']['title'])}</h2><div class="context-prose">{context}</div>{coda}</div></section><section class="edition inverse"><div class="edition-inner"><div class="edition-head"><span class="section-no">EDITION AND ACCESS</span><h2>Work identity</h2></div><div class="edition-grid">{cells_html}</div></div></section>'''
    return f"works/{w['slug']}/index.html",f"{w['title']} — {site['site_title']}",w['meta_description'],main,cls

def render_practice(site,works):
    p=site['practice']; idx=''.join(f'<a href="#{esc(m["id"])}">{esc(m["index"])} · {esc(m["title"])}</a>' for m in p['modules'])
    intro=''.join(f'<p>{esc(x)}</p>' for x in p['intro'])
    mods=''.join(f'''<article class="practice-module" id="{esc(m['id'])}"><header><span class="work-no">{esc(m['index'])}</span><h2>{esc(m['title'])}</h2></header><div class="reading"><p>{esc(m['text'])}</p></div><figure><img alt="{esc(m['alt'])}" src="../{esc(m['image'])}"><figcaption>{esc(m['caption'])}</figcaption></figure></article>''' for m in p['modules'])
    main=f'<section class="page-mast"><h1>Practice</h1><p>{esc(fmt(p["mast"],works))}</p></section><section class="practice-intro"><div class="practice-index">{idx}</div><div class="practice-reading">{intro}</div></section><section class="practice-modules">{mods}</section>'
    return "practice/index.html",f"Practice — {site['site_title']}",site['metadata']['practice'],main

def render_about(site,works):
    a=site['about']; paras=''.join(f'<p>{esc(fmt(x,works))}</p>' for x in a['paragraphs'])
    facts=[]
    for dt,dd in a['facts']:
        facts.append(f'<div class="fact"><dt>{esc(dt)}</dt><dd>{"<br>".join(esc(x) for x in dd.split(chr(10)))}</dd></div>')
    cv=site["documents"]["cv"]
    cv_href=site['site_origin'].rstrip('/')+'/'+cv['path'].lstrip('/')
    cv_link=f'<div class="action-group about-actions"><a class="action primary" href="{esc(cv_href)}" download="Mohammad_Zare_AcademicCV.pdf"><span>{esc(cv["label"])}</span><span>↓</span></a></div>'
    main=f'<section class="page-mast"><h1>About</h1><p>{esc(a["mast"])}</p></section><section class="about-layout"><div class="about-copy">{paras}{cv_link}</div><aside class="about-facts"><dl>{"".join(facts)}</dl></aside></section>'
    return "about/index.html",f"About — {site['site_title']}",site['metadata']['about'],main

def render_contact(site,works):
    main=f'''<section class="page-mast"><h1>Contact</h1><p>{esc(site['contact']['mast'])}</p></section><section class="contact-layout"><div class="contact-list"><a class="contact-row" href="mailto:{esc(site['email'])}"><span>Email</span><strong>{esc(site['email'])}</strong><b>→</b></a><a class="contact-row" href="{esc(site['github_profile'])}" target="_blank" rel="noopener noreferrer"><span>GitHub</span><strong>mozareeduge</strong><b>↗</b></a><a class="contact-row" href="{esc(site['linkedin'])}" target="_blank" rel="noopener noreferrer"><span>LinkedIn</span><strong>{esc(site['formal_name'])}</strong><b>↗</b></a></div></section>'''
    return "contact/index.html",f"Contact — {site['site_title']}",site['metadata']['contact'],main
