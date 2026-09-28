/* Editor preview: draws the real page (site.css + the build's own markup, via preview-render.js)
   at a real device width, scaled to fit the preview pane. */
(function () {
  'use strict';
  const CMS = window.CMS, h = window.h, createClass = window.createClass, R = window.TBBFRender;
  if (!CMS || !h || !createClass || !R) { console.warn('TBBF preview: CMS preview API unavailable'); return; }

  const ORIGIN = location.origin;
  // Width × height of a real screen: the site sizes some sections by screen height (svh), so both matter.
  const DEVICES = [['desktop', 'Desktop', 1440, 900], ['tablet', 'Tablet', 1024, 768], ['mobile', 'Mobile', 390, 844]];
  const choice = { page: {}, device: 'desktop', tall: false };

  // Published site + works, written by src/build.py. Anything the editor has not opened comes from here.
  let snapshot = null;
  const snapshotReady = fetch('./preview-data.json', { cache: 'no-cache' })
    .then(r => r.ok ? r.json() : null).then(d => { snapshot = d; }).catch(() => {});

  const plain = v => (v && typeof v.toJS === 'function') ? v.toJS() : v;
  const clone = v => v === undefined ? v : JSON.parse(JSON.stringify(v));

  // Same rule as tidy_roles() in scripts/publish.py: a role typed as a filename or path becomes its slug.
  const slugRole = name => {
    let stem = String(name).split('?')[0].split(/[\\/]/).pop();
    const dot = stem.lastIndexOf('.'); if (dot > 0) stem = stem.slice(0, dot);
    stem = stem.toLowerCase().replace(/-(desktop|mobile)$/, '');
    return stem.replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'image';
  };
  const needsSlug = v => typeof v === 'string' && (/[/. ]/.test(v) || v !== v.toLowerCase());

  function tidyWork(w, typed) {
    const fix = v => { if (!needsSlug(v)) return v; const r = slugRole(v); typed[`${w.asset_slug}/${r}`] = v; return r; };
    w.feature_image = fix(w.feature_image);
    ((w.views || {}).items || []).forEach(v => { v.role = fix(v.role); });
    return w;
  }

  function pagesFor(collection, slug) {
    const site = [['home', 'Home'], ['works', 'Works list'], ['practice', 'Practice'], ['about', 'About'], ['contact', 'Contact']];
    if (collection === 'works') return [[`work:${slug}`, 'This work’s page'], ['home', 'Home'], ['works', 'Works list']];
    return site;
  }

  // Minimal DOM morph so typing updates text in place instead of reloading every image.
  function morph(from, to) {
    if (from.nodeType !== to.nodeType || from.nodeName !== to.nodeName) { from.replaceWith(to.cloneNode(true)); return; }
    if (from.nodeType === 3 || from.nodeType === 8) { if (from.data !== to.data) from.data = to.data; return; }
    if (from.nodeType === 1) {
      for (const a of [...from.attributes]) if (!to.hasAttribute(a.name)) from.removeAttribute(a.name);
      for (const a of [...to.attributes]) if (from.getAttribute(a.name) !== a.value) from.setAttribute(a.name, a.value);
    }
    morphChildren(from, to);
  }
  function morphChildren(from, to) {
    const fc = [...from.childNodes], tc = [...to.childNodes];
    tc.forEach((t, i) => { if (fc[i]) morph(fc[i], t); else from.appendChild(t.cloneNode(true)); });
    fc.slice(tc.length).forEach(n => n.remove());
  }

  const Preview = createClass({
    componentDidMount() { this.setup(); },
    componentDidUpdate() { this.draw(); },
    componentWillUnmount() { if (this.ro) this.ro.disconnect(); },

    host() { return this.el || (this.props.document && this.props.document.getElementById('tbbf-preview')); },

    setup() {
      const el = this.host(); if (!el) return;
      const doc = el.ownerDocument; this.doc = doc; this.win = doc.defaultView;
      const st = doc.createElement('style');
      st.textContent = 'html,body{margin:0!important;padding:0!important;overflow:hidden!important;background:#2b2a28}'
        + '#tbbf-preview{font:12px/1.3 system-ui,sans-serif;color:#eee8de}'
        + '.tbbf-bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:8px 10px;background:#1b1a19;border-bottom:1px solid #444}'
        + '.tbbf-bar select,.tbbf-bar button{font:inherit;color:#eee8de;background:#2f2d2a;border:1px solid #555;border-radius:4px;padding:4px 8px;cursor:pointer}'
        + '.tbbf-bar button[aria-pressed=true]{background:#eee8de;color:#0b0c0b;border-color:#eee8de}'
        + '.tbbf-note{margin-left:auto;opacity:.65}.tbbf-err{flex-basis:100%;color:#f0b37e}'
        + '.tbbf-stage{position:relative;overflow:hidden}.tbbf-stage iframe{position:absolute;top:0;border:0;background:#c7bfb2;transform-origin:0 0}';
      doc.head.appendChild(st);

      const bar = doc.createElement('div'); bar.className = 'tbbf-bar';
      const sel = doc.createElement('select'); sel.title = 'Which page to show';
      sel.addEventListener('change', () => { choice.page[this.key()] = sel.value; this.draw(true); });
      bar.appendChild(sel);
      this.devButtons = DEVICES.map(([id, label, w, ht]) => {
        const b = doc.createElement('button'); b.type = 'button'; b.textContent = `${label} ${w}×${ht}`;
        // Rebuild, not patch: a browser keeps the <picture> source it chose for the previous width.
        b.addEventListener('click', () => { choice.device = id; this.layout(); this.fresh = true; this.draw(true); });
        bar.appendChild(b); return [id, b];
      });
      const tall = doc.createElement('button'); tall.type = 'button'; tall.textContent = 'Taller view';
      tall.title = 'Fill the pane with more of the page. Sections sized to the screen height (the Home hero) then look taller than on a real screen.';
      tall.addEventListener('click', () => { choice.tall = !choice.tall; this.layout(); this.fresh = true; this.draw(true); });
      bar.appendChild(tall);
      const note = doc.createElement('span'); note.className = 'tbbf-note'; note.textContent = '';
      const err = doc.createElement('div'); err.className = 'tbbf-err'; err.hidden = true;
      bar.append(note, err);

      const stage = doc.createElement('div'); stage.className = 'tbbf-stage';
      const frame = doc.createElement('iframe'); frame.title = 'Page preview';
      stage.appendChild(frame);
      el.append(bar, stage);
      Object.assign(this, { sel, err, stage, frame, note, tall });

      const fd = frame.contentDocument;
      fd.open();
      fd.write(`<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><base href="${ORIGIN}/"><link rel="stylesheet" href="${ORIGIN}/site.css"></head><body></body></html>`);
      fd.close();
      this.fd = fd;
      // Links stay put: the preview is for looking, not navigating.
      fd.addEventListener('click', e => { if (e.target.closest && e.target.closest('a')) e.preventDefault(); }, true);
      // The two interactions site.js provides: the menu dialog and the home work index.
      fd.addEventListener('click', e => {
        const t = e.target.closest ? e.target : null; if (!t) return;
        const dlg = fd.querySelector('[data-menu]');
        if (t.closest('[data-menu-open]') && dlg && !dlg.open) dlg.showModal();
        else if (t.closest('[data-menu-close]') && dlg) dlg.close();
      });
      const hover = e => {
        const a = e.target.closest && e.target.closest('[data-preview-index]'); if (!a) return;
        const links = [...fd.querySelectorAll('[data-preview-index]')], i = links.indexOf(a);
        fd.querySelectorAll('[data-preview-frame]').forEach((f, n) => f.classList.toggle('active', n === i));
        const cap = fd.querySelector('[data-preview-caption]'); if (cap) cap.textContent = a.dataset.caption || '';
      };
      fd.addEventListener('mouseover', hover); fd.addEventListener('focusin', hover);

      this.ro = new this.win.ResizeObserver(() => this.layout());
      this.ro.observe(doc.documentElement);
      this.layout();
      snapshotReady.then(() => this.draw(true));
      this.draw(true);
    },

    key() { const e = this.props.entry; return `${e.get('collection')}/${e.get('slug')}`; },

    layout() {
      if (!this.stage) return;
      const [, , width, height] = DEVICES.find(d => d[0] === choice.device);
      const top = this.stage.getBoundingClientRect().top;
      const availW = this.doc.documentElement.clientWidth, availH = Math.max(200, this.win.innerHeight - top);
      // Real screen: the whole device screen fits the pane. Taller view: fit the width, fill the pane's height.
      const scale = Math.min(1, availW / width, choice.tall ? Infinity : (availH - 16) / height);
      const screenH = choice.tall ? Math.max(height, Math.floor((availH - 16) / scale)) : height;
      this.stage.style.height = availH + 'px';
      Object.assign(this.frame.style, {
        width: width + 'px', height: screenH + 'px', transform: `scale(${scale})`,
        left: Math.max(0, (availW - width * scale) / 2) + 'px', top: '8px',
      });
      this.devButtons.forEach(([id, b]) => b.setAttribute('aria-pressed', String(id === choice.device)));
      this.tall.setAttribute('aria-pressed', String(choice.tall));
      this.note.textContent = `${choice.tall ? `Taller ${width}×${screenH} view` : `Real ${width}×${height} screen`}${scale < 1 ? ` · shown at ${Math.round(scale * 100)}%` : ''} · scroll inside the page`;
    },

    data() {
      const e = this.props.entry, collection = e.get('collection'), slug = e.get('slug');
      const own = plain(e.get('data')) || {};
      let site = clone(snapshot && snapshot.site), works = clone((snapshot && snapshot.works) || []);
      const typed = {};
      if (collection === 'works') {
        const edited = tidyWork(clone(own), typed);
        const i = works.findIndex(w => w.slug === (edited.slug || slug));
        if (i >= 0) works[i] = edited; else works.push(edited);
      } else site = clone(own);
      works = works.map(w => tidyWork(w, typed)).sort((a, b) => (a.order || 0) - (b.order || 0));
      return { collection, slug: own.slug || slug, site, works, typed };
    },

    // An image uploaded in this session is not converted to WebP until publishing; show the upload itself.
    async resolveUpload(folder, role, typed) {
      const names = typed[`${folder}/${role}`] ? [typed[`${folder}/${role}`]] : [];
      ['jpg', 'jpeg', 'png', 'webp', 'JPG', 'JPEG', 'PNG'].forEach(x => names.push(`${role}.${x}`));
      for (const n of names) {
        const path = n.startsWith('/') ? n : `/assets/${folder}/${n.split('/').pop()}`;
        try {
          const a = await this.props.getAsset(path);
          const url = typeof a === 'string' ? a : a && (a.url || a.blobURL || (a.toString && a.toString()));
          if (url && !/^\[object/.test(url) && !/\/assets\/.*-(desktop|mobile)\.webp$/.test(url)) return url;
        } catch (e) { /* not found */ }
      }
      return null;
    },

    watchImages(typed) {
      this.fixed = this.fixed || {};
      this.fd.querySelectorAll('img').forEach(img => {
        if (img.dataset.tbbfWatch) return; img.dataset.tbbfWatch = '1';
        img.addEventListener('error', async () => {
          const m = /assets\/([^/]+)\/(.+)-(desktop|mobile)\.webp$/.exec(img.getAttribute('src') || '');
          if (!m) return;
          const url = await this.resolveUpload(m[1], m[2], typed);
          if (url) { this.fixed[`assets/${m[1]}/${m[2]}`] = url; this.draw(true); }
        });
      });
    },

    draw(force) {
      if (!this.fd) return;
      const d = this.data();
      const opts = pagesFor(d.collection, d.slug);
      const k = this.key();
      let page = choice.page[k];
      if (!opts.some(o => o[0] === page)) page = opts[0][0];
      if (this.sel.dataset.for !== k) {
        this.sel.innerHTML = ''; opts.forEach(([v, l]) => { const o = this.doc.createElement('option'); o.value = v; o.textContent = l; this.sel.appendChild(o); });
        this.sel.dataset.for = k;
      }
      this.sel.value = page;
      if (!d.site || !d.works.length) { this.showError('Waiting for the published site data (preview-data.json)…'); return; }
      let r;
      try { r = R.renderPage(page, d.site, d.works); }
      catch (e) { this.showError(`Preview paused — a field is incomplete (${e.message}). The last good version is shown.`); return; }
      this.showError('');
      const html = r.body.replace(/<noscript>[\s\S]*?<\/noscript>/g, '');
      const sig = page + choice.device + html;
      if (!force && sig === this.lastSig) return;
      this.lastSig = sig;

      const tpl = this.fd.createElement('template'); tpl.innerHTML = html;
      tpl.content.querySelectorAll('img').forEach(img => {
        const m = /assets\/([^/]+)\/(.+)-(desktop|mobile)\.webp$/.exec(img.getAttribute('src') || '');
        const url = m && this.fixed && this.fixed[`assets/${m[1]}/${m[2]}`];
        if (url) { img.setAttribute('src', url); img.parentNode.querySelectorAll('source').forEach(s => s.remove()); }
      });
      const base = this.fd.querySelector('base'), want = `${ORIGIN}/${r.folder}`;
      const moved = base.getAttribute('href') !== want;
      const body = this.fd.body, y = this.fd.defaultView.scrollY;
      // Empty the old page first, or its images re-request themselves against the new base.
      if (moved) body.innerHTML = '';
      base.setAttribute('href', want);
      body.className = r.bodyClass;
      if (moved || this.fresh) { body.innerHTML = ''; body.appendChild(tpl.content); if (moved) this.fd.defaultView.scrollTo(0, 0); else this.fd.defaultView.scrollTo(0, y); this.fresh = false; }
      else { morphChildren(body, tpl.content); this.fd.defaultView.scrollTo(0, y); }
      this.watchImages(d.typed);
    },

    showError(msg) { if (this.err) { this.err.textContent = msg; this.err.hidden = !msg; } },

    render() { return h('div', { id: 'tbbf-preview', ref: el => { this.el = el; } }); },
  });

  CMS.registerPreviewTemplate('works', Preview);
  CMS.registerPreviewTemplate('site_copy', Preview);
  CMS.registerPreviewTemplate('site', Preview);
})();
