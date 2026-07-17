from site_config import (
    SITE_TITLE, ARTISTIC_NAME, FORMAL_NAME, CV_FILENAME,
    LINKEDIN_URL, GITHUB_URL, PRIMARY_NAV, ROUTE_PATHS,
)


def current_attr(current, key):
    return ' aria-current="page"' if current == key else ''


def route_url(key, prefix):
    """Relative URL from the current page to the named route."""
    return prefix + ROUTE_PATHS[key]


def cv_link(prefix, label='CV', css_class='', arrow='↓'):
    href = prefix + CV_FILENAME
    class_attr = f' class="{css_class}"' if css_class else ''
    return (
        f'<a{class_attr} href="{href}" download="{CV_FILENAME}" '
        f'data-cv-download><span>{label}</span><span aria-hidden="true">{arrow}</span>'
        f'<span class="sr-only"> PDF download</span></a>'
    )


def header(current, prefix):
    home_url = route_url('home', prefix) or 'index.html'
    contact_url = route_url('contact', prefix)
    primary = ''.join(
        f'<a href="{route_url(key, prefix)}"{current_attr(current, key)}>{label}</a>'
        for key, label in PRIMARY_NAV
    )
    mobile_primary = ''.join(
        f'<a href="{route_url(key, prefix)}"{current_attr(current, key)}>'
        f'<span>0{i}</span><strong>{label}</strong><small>Open</small></a>'
        for i, (key, label) in enumerate(PRIMARY_NAV, 1)
    )
    cv_desktop = '' if current == 'contact' else cv_link(prefix, 'CV')
    cv_mobile = '' if current == 'contact' else cv_link(prefix, 'Download CV', arrow='↓')
    return f'''<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header" data-site-header>
  <a class="wordmark" href="{home_url}" aria-label="{SITE_TITLE} home">
    <span>{SITE_TITLE}</span><small>works by {ARTISTIC_NAME}</small>
  </a>
  <nav class="desktop-nav" aria-label="Primary">{primary}</nav>
  <nav class="utility-nav" aria-label="Utility">
    <a href="{contact_url}"{current_attr(current, 'contact')}>Contact</a>
    <a href="{LINKEDIN_URL}" target="_blank" rel="noopener">LinkedIn<span class="sr-only"> (opens in new tab)</span></a>
    {cv_desktop}
  </nav>
  <button class="menu-toggle" type="button" data-menu-open aria-controls="site-menu" aria-expanded="false">Menu</button>
</header>
<dialog class="menu-dialog" id="site-menu" data-menu-dialog aria-labelledby="menu-title">
  <div class="menu-shell">
    <div class="menu-head">
      <div><strong id="menu-title">{SITE_TITLE}</strong><small>works by {ARTISTIC_NAME}</small></div>
      <button class="menu-close" type="button" data-menu-close>Close</button>
    </div>
    <div class="menu-body">
      <nav class="menu-primary" aria-label="Primary mobile navigation">{mobile_primary}</nav>
      <nav class="menu-utility" aria-label="Utility mobile navigation">
        <a href="{contact_url}"{current_attr(current, 'contact')}>Contact <span aria-hidden="true">→</span></a>
        {cv_mobile}
        <a href="{LINKEDIN_URL}" target="_blank" rel="noopener">LinkedIn <span aria-hidden="true">↗</span><span class="sr-only"> opens in new tab</span></a>
      </nav>
    </div>
    <div class="menu-foot">
      <span>Artistic work: {ARTISTIC_NAME}.</span>
      <span>Academic records, citations, and rights: {FORMAL_NAME}.</span>
    </div>
  </div>
</dialog>'''


def footer(current, prefix):
    cv = '' if current == 'contact' else cv_link(prefix, 'CV')
    return f'''<footer class="site-footer">
  <div class="footer-identity"><strong>{ARTISTIC_NAME}</strong><p>Browser-native literary works shaped through research and generative writing.</p><small>Academic records, citations, and rights: {FORMAL_NAME}.</small></div>
  <nav aria-label="Footer navigation">
    <a href="{route_url('works', prefix)}"{current_attr(current, 'works')}>Works</a>
    <a href="{route_url('practice', prefix)}"{current_attr(current, 'practice')}>Practice</a>
    <a href="{route_url('about', prefix)}"{current_attr(current, 'about')}>About</a>
    <a href="{route_url('contact', prefix)}"{current_attr(current, 'contact')}>Contact</a>
    <a href="{LINKEDIN_URL}" target="_blank" rel="noopener">LinkedIn ↗</a>
    {cv}
    <a href="{GITHUB_URL}" target="_blank" rel="noopener">GitHub ↗</a>
  </nav>
  <div class="footer-meta"><p>{SITE_TITLE} presents four autonomous browser-native works.</p><p>© 2026 {FORMAL_NAME}.</p></div>
</footer>'''
