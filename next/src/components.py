from content import SHARED, CV_FILENAME, LINKEDIN_URL, GITHUB_URL
from renderers import escape, resolve_href
from site_config import PRIMARY_NAV, ROUTE_PATHS


def current_attr(current, key):
    return ' aria-current="page"' if current == key else ''


def route_url(key, prefix):
    """Relative URL from the current page to the named route."""
    return prefix + ROUTE_PATHS[key]


def cv_link(prefix, label='CV', css_class=''):
    href = resolve_href(f'/{CV_FILENAME}', prefix)
    class_attr = f' class="{css_class}"' if css_class else ''
    return (
        f'<a{class_attr} href="{href}" download="{CV_FILENAME}">'
        f'<span>{escape(label)}</span><span aria-hidden="true">↓</span>'
        f'<span class="sr-only"> PDF download</span></a>'
    )


def header(current, prefix):
    h = SHARED['header']
    home_url = route_url('home', prefix) or 'index.html'
    contact_url = route_url('contact', prefix)
    primary = ''.join(
        f'<a href="{route_url(key, prefix)}"{current_attr(current, key)}>{escape(label)}</a>'
        for key, label in PRIMARY_NAV
    )
    mobile_primary = ''.join(
        f'<a href="{route_url(key, prefix)}"{current_attr(current, key)}>'
        f'<span>0{i}</span><strong>{escape(label)}</strong></a>'
        for i, (key, label) in enumerate(PRIMARY_NAV, 1)
    )
    cv_desktop = '' if current == 'contact' else cv_link(prefix, 'CV')
    cv_mobile = '' if current == 'contact' else cv_link(prefix, SHARED['mobile_menu']['utility_cv'])
    m = SHARED['mobile_menu']
    return f'''<a class="skip-link" href="#main">{escape(h["skip_link"])}</a>
<header class="site-header" data-site-header>
  <a class="wordmark" href="{home_url}" aria-label="{escape(h["wordmark"])} home">
    <span>{escape(h["wordmark"])}</span><small>{escape(h["wordmark_subline"])}</small>
  </a>
  <nav class="desktop-nav" aria-label="Primary">{primary}</nav>
  <nav class="utility-nav" aria-label="Utility">
    <a href="{contact_url}"{current_attr(current, 'contact')}>Contact</a>
    <a href="{LINKEDIN_URL}" target="_blank" rel="noopener">LinkedIn<span class="sr-only"> (opens in new tab)</span></a>
    {cv_desktop}
  </nav>
  <button class="menu-toggle" type="button" data-menu-open aria-controls="site-menu" aria-expanded="false">{escape(h["menu_control"])}</button>
</header>
<dialog class="menu-dialog" id="site-menu" data-menu-dialog aria-labelledby="menu-title">
  <div class="menu-shell">
    <div class="menu-head">
      <div><strong id="menu-title">{escape(m["title"])}</strong><small>{escape(m["subline"])}</small></div>
      <button class="menu-close" type="button" data-menu-close>{escape(m["close"])}</button>
    </div>
    <div class="menu-body">
      <nav class="menu-primary" aria-label="Primary mobile navigation">{mobile_primary}</nav>
      <nav class="menu-utility" aria-label="Utility mobile navigation">
        <a href="{contact_url}"{current_attr(current, 'contact')}>{escape(m["utility_contact"])}</a>
        {cv_mobile}
        <a href="{LINKEDIN_URL}" target="_blank" rel="noopener">{escape(m["utility_linkedin"])}<span class="sr-only"> opens in new tab</span></a>
      </nav>
    </div>
    <div class="menu-foot">
      <span>{escape(m["identity_note_1"])}</span>
      <span>{escape(m["identity_note_2"])}</span>
    </div>
  </div>
</dialog>'''


def footer(current, prefix):
    f = SHARED['footer']
    cv = '' if current == 'contact' else cv_link(prefix, 'CV')
    return f'''<footer class="site-footer">
  <div class="footer-identity"><strong>{escape(f["identity"])}</strong><p>{escape(f["practice_line"])}</p><small>{escape(f["formal_name_line"])}</small></div>
  <nav aria-label="Footer navigation">
    <a href="{route_url('works', prefix)}"{current_attr(current, 'works')}>Works</a>
    <a href="{route_url('practice', prefix)}"{current_attr(current, 'practice')}>Practice</a>
    <a href="{route_url('about', prefix)}"{current_attr(current, 'about')}>About</a>
    <a href="{route_url('contact', prefix)}"{current_attr(current, 'contact')}>Contact</a>
    <a href="{LINKEDIN_URL}" target="_blank" rel="noopener">LinkedIn ↗</a>
    {cv}
    <a href="{GITHUB_URL}" target="_blank" rel="noopener">GitHub ↗</a>
  </nav>
  <div class="footer-meta"><p>{escape(f["portfolio_statement"])}</p><p>{escape(f["copyright"])}</p></div>
</footer>'''
