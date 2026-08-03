(() => {
  'use strict';
  document.querySelectorAll('[data-atlas]').forEach((atlas) => {
    const tabs = [...atlas.querySelectorAll('[role="tab"]')];
    const image = atlas.querySelector('[data-state-image]');
    const number = atlas.querySelector('[data-state-number]');
    const title = atlas.querySelector('[data-state-title]');
    const copy = atlas.querySelector('[data-state-copy]');
    if (!tabs.length || !image || !title || !copy) return;

    const activate = (tab, moveFocus = false) => {
      tabs.forEach((item) => {
        const selected = item === tab;
        item.setAttribute('aria-selected', String(selected));
        item.tabIndex = selected ? 0 : -1;
      });
      image.src = tab.dataset.image;
      image.alt = tab.dataset.alt || '';
      number.textContent = tab.dataset.number || '';
      title.textContent = tab.dataset.title || '';
      copy.textContent = tab.dataset.copy || '';
      if (moveFocus) tab.focus();
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', (event) => {
        let next = null;
        if (event.key === 'ArrowDown' || event.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
        if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') next = tabs[(index - 1 + tabs.length) % tabs.length];
        if (event.key === 'Home') next = tabs[0];
        if (event.key === 'End') next = tabs[tabs.length - 1];
        if (next) {
          event.preventDefault();
          activate(next, true);
        }
      });
    });
  });
})();
