(() => {
  'use strict';

  const dialog = document.querySelector('[data-menu-dialog]');
  const openButton = document.querySelector('[data-menu-open]');
  const closeButton = document.querySelector('[data-menu-close]');

  if (dialog && openButton && closeButton) {
    const openMenu = () => {
      if (typeof dialog.showModal === 'function') dialog.showModal();
      else dialog.setAttribute('open', '');
      document.body.classList.add('menu-open');
      openButton.setAttribute('aria-expanded', 'true');
      requestAnimationFrame(() => closeButton.focus());
    };
    const closeMenu = () => {
      if (typeof dialog.close === 'function') dialog.close();
      else dialog.removeAttribute('open');
      document.body.classList.remove('menu-open');
      openButton.setAttribute('aria-expanded', 'false');
      openButton.focus();
    };
    openButton.addEventListener('click', openMenu);
    closeButton.addEventListener('click', closeMenu);
    dialog.addEventListener('cancel', (event) => {
      event.preventDefault();
      closeMenu();
    });
    dialog.addEventListener('click', (event) => {
      if (event.target === dialog) closeMenu();
    });
    dialog.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        document.body.classList.remove('menu-open');
        openButton.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Home hero preview — wide-screen hover/keyboard-focus enhancement only
  // (Section 4.2.1). The first frame and caption are already correct in
  // HTML; this only switches the active frame. No aria-live: decorative
  // image switching must not be announced.
  const previewRoot = document.querySelector('[data-home-preview]');
  if (previewRoot) {
    const images = [...previewRoot.querySelectorAll('[data-preview-index]')];
    const caption = previewRoot.querySelector('[data-preview-caption]');
    const links = [...document.querySelectorAll('.hero-work-index [data-preview-index]')];
    const activate = (index) => {
      images.forEach((img) => img.classList.toggle('is-inactive', img.dataset.previewIndex !== index));
      const active = images.find((img) => img.dataset.previewIndex === index);
      if (active && caption) caption.textContent = active.dataset.caption || '';
    };
    links.forEach((link) => {
      const index = link.dataset.previewIndex;
      link.addEventListener('mouseenter', () => activate(index));
      link.addEventListener('focus', () => activate(index));
    });
  }
})();
