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

  const previewRoot = document.querySelector('[data-preview-root]');
  if (previewRoot) {
    const links = [...previewRoot.querySelectorAll('[data-preview-link]')];
    const frames = [...previewRoot.querySelectorAll('[data-preview-frame]')];
    const number = previewRoot.querySelector('[data-preview-number]');
    const label = previewRoot.querySelector('[data-preview-label]');
    const activate = (key, link) => {
      frames.forEach((frame) => frame.classList.toggle('is-active', frame.dataset.previewFrame === key));
      links.forEach((item) => item.classList.toggle('is-active', item === link));
      if (number) number.textContent = link.dataset.number || '';
      if (label) label.textContent = link.dataset.label || '';
    };
    links.forEach((link) => {
      const key = link.dataset.previewLink;
      link.addEventListener('mouseenter', () => activate(key, link));
      link.addEventListener('focus', () => activate(key, link));
    });
  }
})();
