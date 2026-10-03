/* JS twin of src/renderers.py for the editor preview.
   Output must match the Python renderer byte for byte; tests/static/test_preview_parity.py enforces it.
   When a renderer in src/renderers.py changes, change the same function here. */
(function (root) {
  'use strict';
  const NUMBERS = ['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty'];
  const cap1 = s => s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
  const numWord = (n, cap) => { const s = NUMBERS[n] !== undefined ? NUMBERS[n] : String(n); return cap ? cap1(s) : s; };
  const pathPrefix = output => '../'.repeat(output.split('/').length - 1);
  const workPath = w => `works/${w.slug}/index.html`;
  const str = v => (v === null || v === undefined) ? 'None' : (typeof v === 'boolean' ? (v ? 'True' : 'False') : String(v));
  const esc = v => str(v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;');
  const get = (o, k, d) => (o && o[k] !== undefined && o[k] !== null) ? o[k] : d;

  function fmt(text, works) {
    const n = works.length;
    const last = n ? works[n - 1].title : '';
    const titles = n > 1 ? works.slice(0, -1).map(w => w.title).join(', ') + (n > 2 ? ', and ' : ' and ') + last : last;
    const vals = { count: String(n), count_word: numWord(n), Count_word: numWord(n, true), work_titles: titles };
    return str(text).replace(/\{\{|\}\}|\{(\w+)\}/g, (m, k) => m === '{{' ? '{' : m === '}}' ? '}' : (k in vals ? vals[k] : m));
  }

  function picture(prefix, work, role, alt, cls, caption, eager) {
    const asset = work.asset_slug;
    const desktop = `${prefix}assets/${asset}/${role}-desktop.webp`;
    const mobile = `${prefix}assets/${asset}/${role}-mobile.webp`;
    const attr = eager ? ' fetchpriority="high"' : '';
    let inner = `<picture><source media="(max-width:760px)" srcset="${esc(mobile)}"><img alt="${esc(alt)}" src="${esc(desktop)}"${attr}></picture>`;
    if (caption) inner += `<div class="caption"><span>${esc(caption[0])}</span><span>${esc(caption[1])}</span></div>`;
    return `<div class="picture${cls ? ' ' + cls : ''}">${inner}</div>`;
  }

  function motionPicture(prefix, work, alt, cls, caption, eager, surface) {
    const motion = work.motion || {};
    const role = motion.fallback_role || work.feature_image;
    const asset = work.asset_slug;
    const desktop = `${prefix}assets/${asset}/${role}-desktop.webp`;
    const mobile = `${prefix}assets/${asset}/${role}-mobile.webp`;
    const attr = eager ? ' fetchpriority="high"' : '';
    let inner = `<picture class="motion-poster"><source media="(max-width:760px)" srcset="${esc(mobile)}"><img alt="${esc(alt)}" src="${esc(desktop)}"${attr}></picture>`;
    if (motion.enabled) {
      const vd = `${prefix}assets/${asset}/${motion.desktop_file}`;
      const vm = `${prefix}assets/${asset}/${motion.mobile_file}`;
      inner += `<video class="motion-video" muted loop playsinline preload="none" data-motion-video data-motion-desktop="${esc(vd)}" data-motion-mobile="${esc(vm)}" aria-hidden="true"></video>`;
    }
    if (caption) inner += `<div class="caption"><span>${esc(caption[0])}</span><span>${esc(caption[1])}</span></div>`;
    return `<div class="picture motion-media${cls ? ' ' + cls : ''}" data-motion-surface="${esc(surface || 'project')}">${inner}</div>`;
  }

  function header(prefix, current, site) {
    const curr = key => current === key ? ' aria-current="page"' : '';
    return `<a class="skip" href="#main">Skip to main content</a><header class="site-header"><a class="wordmark" href="${prefix}index.html"><strong>${esc(site.site_title)}</strong><small>works by ${esc(site.artistic_name)}</small></a><nav aria-label="Primary" class="nav"><a${curr('works')} href="${prefix}works/index.html">Works</a><a${curr('practice')} href="${prefix}practice/index.html">Practice</a><a${curr('about')} href="${prefix}about/index.html">About</a></nav><nav aria-label="Utility" class="utility"><a${curr('contact')} href="${prefix}contact/index.html">Contact</a></nav><button aria-controls="site-menu" aria-expanded="false" class="menu-toggle" data-menu-open>Menu</button></header><noscript><nav aria-label="Primary navigation — JavaScript unavailable" class="noscript-nav"><a href="${prefix}works/index.html">Works</a><a href="${prefix}practice/index.html">Practice</a><a href="${prefix}about/index.html">About</a><a href="${prefix}contact/index.html">Contact</a></nav></noscript><dialog aria-labelledby="site-menu-title" class="menu" data-menu id="site-menu"><div class="menu-shell"><div class="menu-head"><strong id="site-menu-title">${esc(site.site_title)}</strong><button class="menu-close" data-menu-close>Close</button></div><nav aria-label="Menu" class="menu-links"><a href="${prefix}works/index.html"><span>01</span><strong>Works</strong><small>Open</small></a><a href="${prefix}practice/index.html"><span>02</span><strong>Practice</strong><small>Open</small></a><a href="${prefix}about/index.html"><span>03</span><strong>About</strong><small>Open</small></a><a href="${prefix}contact/index.html"><span>04</span><strong>Contact</strong><small>Open</small></a></nav><div class="menu-foot"><span>Artistic work: ${esc(site.artistic_name)}.</span><span>${esc(site.shared.menu_name_boundary)}</span></div></div></dialog>`;
  }

  function footer(prefix, site, works) {
    return `<footer class="site-footer"><div class="footer-identity"><strong>${esc(site.artistic_name)}</strong><p>${esc(site.shared.footer_identity)}</p><small>${esc(site.shared.name_boundary)}</small></div><nav aria-label="Footer"><a href="${prefix}works/index.html">Works</a><a href="${prefix}practice/index.html">Practice</a><a href="${prefix}about/index.html">About</a><a href="${prefix}contact/index.html">Contact</a><a href="${esc(site.github_profile)}" target="_blank" rel="noopener noreferrer">GitHub ↗</a></nav><div class="footer-meta"><p>${esc(fmt('The Black Bird Field presents {count_word} autonomous browser-native works.', works))}</p><p>© ${esc(site.year)} ${esc(site.formal_name)}.</p></div></footer>`;
  }

  function renderHome(site, works) {
    const n = works.length;
    const resp = works.map(w => w.responsibility);
    let responsibilities;
    if (resp.length === 1) responsibilities = resp[0];
    else if (resp.length === 2) responsibilities = `${resp[0]} and ${resp[1]}`;
    else responsibilities = resp.slice(0, -1).join('; ') + `; and ${resp[resp.length - 1]}`;
    const heroIntro = `The field gathers ${numWord(n)} autonomous works. Each gives the browser another literary responsibility: ${responsibilities}.`;
    const pad = i => String(i).padStart(2, '0');
    const frames = works.map((w, i) => `<div class="preview-frame${i === 0 ? ' active' : ''}" data-preview-frame data-work-slug="${esc(w.slug)}">${motionPicture('', w, `${w.title} primary surface`, '', null, i === 0, 'home')}</div>`);
    const index = works.map((w, i) => `<a data-caption="${pad(i + 1)} · ${esc(w.title)}" data-preview-index data-work-slug="${esc(w.slug)}" href="${workPath(w)}"><span>${pad(i + 1)}</span><b>${esc(w.title)}</b><small>${esc(w.mode)}</small></a>`);
    const features = works.map((w, i) => {
      const media = picture('', w, w.feature_image, `${w.title} selected view`, '', [w.form, w.feature_caption]);
      return `<article class="feature"><div class="work-no">${pad(i + 1)}</div><div class="feature-media">${media}</div><div class="feature-copy"><p class="eyebrow">${esc(w.form)} · ${esc(w.year)}</p><h2>${esc(w.title)}</h2><p>${esc(w.summary)}</p><div class="action-group"><a class="action primary" href="${esc(w.live_url)}" target="_blank" rel="noopener noreferrer"><span>Enter the work</span><span>↗</span></a><a class="action secondary" href="${workPath(w)}"><span>About the work</span><span>→</span></a></div></div></article>`;
    });
    const mods = site.practice.modules.map(m => `<article><span class="work-no">${m.index}</span><h3>${esc(m.home_title)}</h3><p>${esc(m.home_text)}</p></article>`).join('');
    const main = `<section class="hero"><div class="hero-copy"><h1>${esc(site.site_title)}</h1><p class="hero-deck">${esc(site.shared.deck)}</p><p class="hero-intro">${esc(heroIntro)}</p><div class="action-group"><a class="action primary" href="works/index.html"><span>View all works</span><span>→</span></a><a class="action secondary" href="practice/index.html"><span>About the practice</span><span>→</span></a></div></div><div class="hero-preview">${frames.join('')}<div class="preview-caption"><span data-preview-caption>01 · ${esc(works[0].title)}</span><span>Work preview</span></div></div><nav aria-label="Works" class="hero-index"><p>${esc(numWord(n, true))} works</p>${index.join('')}</nav><div class="hero-ledger"><span>${esc(site.artistic_name)}</span><span>${esc(numWord(n, true))} browser-native works</span><span>${esc(site.year)}</span></div></section><section class="section-lead"><span class="section-no">01 / WORKS</span><div><h2>${esc(numWord(n, true))} ways to enter the writing</h2><p>${esc(site.shared.section_intro)}</p></div></section><section class="features inverse">${features.join('')}</section><section class="practice-teaser inverse"><div class="section-lead"><span class="section-no">02 / PRACTICE</span><div><h2>${esc(site.practice.home_teaser.title)}</h2><p>${esc(site.practice.home_teaser.text)}</p></div></div><div class="practice-grid">${mods}</div></section><section class="about-strip"><span class="section-no">03 / ABOUT</span><p>${esc(site.shared.about_strip)}</p><div class="about-strip-action"><a class="action primary" href="about/index.html"><span>About Mozare</span><span>→</span></a></div></section>`;
    return { output: 'index.html', bodyClass: 'home-page', current: 'home', main };
  }

  function renderWorks(site, works) {
    const pad = i => String(i).padStart(2, '0');
    const rows = works.map((w, i) => {
      const role = w.feature_image, asset = w.asset_slug, href = `${w.slug}/index.html`;
      return `<article class="work-row"><div class="work-no">${pad(i + 1)}</div><div><h2>${esc(w.title)}</h2><div class="form">${esc(w.form)} · ${esc(w.year)}</div><div class="version">${esc(w.feature_caption)}</div></div><div><p>${esc(w.summary)}</p><div class="action-group"><a class="action secondary" href="${esc(href)}"><span>View work page</span><span>→</span></a></div></div><a class="thumb picture" href="${esc(href)}"><picture><source media="(max-width:760px)" srcset="../assets/${esc(asset)}/${esc(role)}-mobile.webp"><img alt="${esc(w.title)} selected view" src="../assets/${esc(asset)}/${esc(role)}-desktop.webp"></picture></a></article>`;
    });
    const main = `<section class="page-mast"><h1>Works</h1><p>${esc(numWord(works.length, true))} autonomous browser-native works by Mozare. Each gives reading another condition and asks the browser to carry it in another way.</p></section><section class="works-list">${rows.join('')}</section>`;
    return { output: 'works/index.html', bodyClass: 'works-page', current: 'works', main };
  }

  function renderProject(site, works, w) {
    const p = '../../';
    const bodyClass = 'project-page' + (get(w, 'body_class', '') ? ' ' + w.body_class : '');
    const parts = get(w, 'title_parts', [w.title]);
    const titleHtml = parts.length > 1 ? parts.map(x => `<span>${esc(x)}</span>`).join('') : esc(w.title);
    const heroPic = motionPicture(p, w, `${w.title} threshold or primary surface`, '', ['Primary surface', w.poster_caption], true, 'project');
    const conditions = w.prelude.items.map(c => `<article><span class="step">${esc(c.label)}</span><h2>${esc(c.title)}</h2>${c.note ? `<p>${esc(c.note)}</p>` : ''}</article>`).join('');
    const views = w.views.items.map(v => {
      const asset = w.asset_slug;
      const img = `<picture><source media="(max-width:760px)" srcset="${p}assets/${esc(asset)}/${esc(v.role)}-mobile.webp"><img alt="${esc(v.alt)}" src="${p}assets/${esc(asset)}/${esc(v.role)}-desktop.webp"></picture>`;
      return `<article class="view-plate"><div class="view-image">${img}</div><div class="view-copy"><span class="view-no">${esc(v.number)}</span><h3>${esc(v.title)}</h3><p>${esc(v.text)}</p></div></article>`;
    }).join('');
    const context = w.context.paragraphs.map(x => `<p>${esc(x)}</p>`).join('');
    const coda = w.context.coda ? `<p class="context-coda">${esc(w.context.coda)}</p>` : '';
    let annex = '';
    if (w.annex) {
      const ax = w.annex;
      const axParas = ax.paragraphs.map(x => `<p>${esc(x)}</p>`).join('');
      const axLinks = get(ax, 'links', []).map(l => `<a class="action secondary" href="${esc(l.url)}" target="_blank" rel="noopener noreferrer"><span>${esc(l.label)}</span><span>↗</span></a>`).join('');
      const axActions = axLinks ? `<div class="action-group context-actions">${axLinks}</div>` : '';
      annex = `<section class="project-context project-annex"><div class="context-inner"><span class="section-no">${esc(ax.label)}</span><h2>${esc(ax.title)}</h2><div class="context-prose">${axParas}</div>${axActions}</div></section>`;
    }
    const cite = w.citation;
    const citation = `${esc(cite.author)} <em>${esc(cite.title)}</em>. ${esc(cite.rest)}`;
    const cells = [
      ['Form', esc(w.form)], ['Artist', esc(site.artistic_name)], ['Citation name', esc(site.formal_name)], ['Edition / build', esc(w.identity.edition)], ['Language', esc(w.identity.language)], ['Encounter', esc(w.identity.encounter)],
      ['Live work', `<a href="${esc(w.live_url)}" target="_blank" rel="noopener noreferrer">Open work ↗</a>`], ['Repository', `<a href="${esc(w.repository_url)}" target="_blank" rel="noopener noreferrer">Open source record ↗</a>`], ['Citation', citation]];
    const cellsHtml = cells.map(([label, value]) => `<div class="edition-cell"><span class="meta-label">${esc(label)}</span>${value.startsWith('<a') ? value : `<strong>${value}</strong>`}</div>`).join('');
    const main = `<section class="project-hero inverse"><div class="project-hero-inner"><div class="project-copy"><p class="project-form">${esc(w.form)} · by ${esc(site.artistic_name)} · ${esc(w.year)}</p><h1>${titleHtml}</h1><p class="lead">${esc(w.hero_lead)}</p><div class="action-group"><a class="action primary" href="${esc(w.live_url)}" target="_blank" rel="noopener noreferrer"><span>Enter the work</span><span>↗</span></a><a class="action secondary" href="${esc(w.repository_url)}" target="_blank" rel="noopener noreferrer"><span>Source and rights</span><span>↗</span></a></div></div><div class="project-hero-media">${heroPic}</div></div></section><section class="prelude"><span class="section-no">${esc(w.prelude.label)}</span>${conditions}</section><section class="selected-views"><div class="views-inner"><div class="views-head"><span class="section-no">SELECTED VIEWS</span><h2>${esc(w.views.title)}</h2><p>${esc(w.views.intro)}</p></div>${views}</div></section><section class="project-context"><div class="context-inner"><span class="section-no">CONTEXT</span><h2>${esc(w.context.title)}</h2><div class="context-prose">${context}</div>${coda}</div></section>${annex}<section class="edition inverse"><div class="edition-inner"><div class="edition-head"><span class="section-no">EDITION AND ACCESS</span><h2>Work identity</h2></div><div class="edition-grid">${cellsHtml}</div></div></section>`;
    return { output: `works/${w.slug}/index.html`, bodyClass, current: 'works', main };
  }

  function renderPractice(site, works) {
    const p = site.practice;
    const idx = p.modules.map(m => `<a href="#${esc(m.id)}">${esc(m.index)} · ${esc(m.title)}</a>`).join('');
    const intro = p.intro.map(x => `<p>${esc(x)}</p>`).join('');
    const mods = p.modules.map(m => `<article class="practice-module" id="${esc(m.id)}"><header><span class="work-no">${esc(m.index)}</span><h2>${esc(m.title)}</h2></header><div class="reading"><p>${esc(m.text)}</p></div><figure><img alt="${esc(m.alt)}" src="../${esc(m.image)}"><figcaption>${esc(m.caption)}</figcaption></figure></article>`).join('');
    const main = `<section class="page-mast"><h1>Practice</h1><p>${esc(fmt(p.mast, works))}</p></section><section class="practice-intro"><div class="practice-index">${idx}</div><div class="practice-reading">${intro}</div></section><section class="practice-modules">${mods}</section>`;
    return { output: 'practice/index.html', bodyClass: 'practice-page', current: 'practice', main };
  }

  function renderAbout(site, works) {
    const a = site.about;
    const paras = a.paragraphs.map(x => `<p>${esc(fmt(x, works))}</p>`).join('');
    const facts = a.facts.map(f => {
      const lines = str(f.detail).split('\n').map(esc).join('<br>');
      const dd = f.url ? `<a href="${esc(f.url)}" target="_blank" rel="noopener noreferrer">${lines}</a>` : lines;
      return `<div class="fact"><dt>${esc(f.term)}</dt><dd>${dd}</dd></div>`;
    }).join('');
    const cv = site.documents.cv;
    const cvHref = site.site_origin.replace(/\/+$/, '') + '/' + cv.path.replace(/^\/+/, '');
    const cvLink = `<div class="action-group about-actions"><a class="action primary" href="${esc(cvHref)}" download="Mohammad_Zare_AcademicCV.pdf"><span>${esc(cv.label)}</span><span>↓</span></a></div>`;
    const main = `<section class="page-mast"><h1>About</h1><p>${esc(a.mast)}</p></section><section class="about-layout"><div class="about-copy">${paras}${cvLink}</div><aside class="about-facts"><dl>${facts}</dl></aside></section>`;
    return { output: 'about/index.html', bodyClass: 'about-page', current: 'about', main };
  }

  function renderContact(site) {
    const main = `<section class="page-mast"><h1>Contact</h1><p>${esc(site.contact.mast)}</p></section><section class="contact-layout"><div class="contact-list"><a class="contact-row" href="mailto:${esc(site.email)}"><span>Email</span><strong>${esc(site.email)}</strong><b>→</b></a><a class="contact-row" href="${esc(site.github_profile)}" target="_blank" rel="noopener noreferrer"><span>GitHub</span><strong>mozareeduge</strong><b>↗</b></a><a class="contact-row" href="${esc(site.linkedin)}" target="_blank" rel="noopener noreferrer"><span>LinkedIn</span><strong>${esc(site.formal_name)}</strong><b>↗</b></a></div></section>`;
    return { output: 'contact/index.html', bodyClass: 'contact-page', current: 'contact', main };
  }

  /* page: 'home' | 'works' | 'practice' | 'about' | 'contact' | 'work:<slug>'.
     Returns what document() in renderers.py puts inside <body>, plus the page's own folder. */
  function renderPage(page, site, works) {
    let r;
    if (page === 'home') r = renderHome(site, works);
    else if (page === 'works') r = renderWorks(site, works);
    else if (page === 'practice') r = renderPractice(site, works);
    else if (page === 'about') r = renderAbout(site, works);
    else if (page === 'contact') r = renderContact(site, works);
    else if (page.startsWith('work:')) {
      const w = works.find(x => x.slug === page.slice(5));
      if (!w) throw new Error(`No work with slug ${page.slice(5)}`);
      r = renderProject(site, works, w);
    } else throw new Error(`Unknown page ${page}`);
    const prefix = pathPrefix(r.output);
    r.body = header(prefix, r.current, site) + `<main id="main">${r.main}</main>` + footer(prefix, site, works);
    r.folder = r.output.replace(/index\.html$/, '');
    return r;
  }

  const api = { renderPage, esc, fmt };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.TBBFRender = api;
})(typeof window !== 'undefined' ? window : globalThis);
