/* Small, framework-free enhancements. Project pages and navigation remain plain links. */
(() => {
  'use strict';
  const navToggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('primary-nav');
  if (navToggle && nav) {
    const setOpen = (open) => {
      navToggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    };
    navToggle.hidden = false;
    navToggle.setAttribute('aria-controls', nav.id);
    setOpen(false);
    navToggle.addEventListener('click', () => setOpen(navToggle.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && navToggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        navToggle.focus();
      }
    });
    document.addEventListener('click', (event) => {
      if (!nav.contains(event.target) && !navToggle.contains(event.target)) setOpen(false);
    });
    document.documentElement.classList.add('nav-ready');
  }

  const filters = [...document.querySelectorAll('button[data-filter]')];
  const cards = [...document.querySelectorAll('[data-domains]')];
  const count = document.getElementById('project-count');
  if (filters.length && cards.length) {
    const allowed = new Set(filters.map((button) => button.dataset.filter));
    const applyFilter = (requested, updateURL = false) => {
      const active = allowed.has(requested) ? requested : 'all';
      let visible = 0;
      cards.forEach((card) => {
        const matches = active === 'all' || card.dataset.domains.toLowerCase().split(/\s+/).includes(active);
        card.hidden = !matches;
        if (matches) visible += 1;
      });
      filters.forEach((button) => {
        const selected = button.dataset.filter === active;
        button.setAttribute('aria-pressed', String(selected));
        button.classList.toggle('is-active', selected);
      });
      if (count) count.textContent = `${visible} ${visible === 1 ? 'project' : 'projects'}`;
      if (updateURL) {
        const url = new URL(window.location.href);
        if (active === 'all') url.searchParams.delete('domain');
        else url.searchParams.set('domain', active);
        window.history.replaceState(null, '', url);
      }
    };
    filters.forEach((button) => {
      button.disabled = false;
      button.addEventListener('click', () => applyFilter(button.dataset.filter, true));
    });
    applyFilter(new URL(window.location.href).searchParams.get('domain') || 'all');
    window.addEventListener('popstate', () => applyFilter(new URL(window.location.href).searchParams.get('domain') || 'all'));
  }

  const dialog = document.getElementById('project-dialog');
  const content = dialog?.querySelector('.dialog-content');
  const source = document.getElementById('project-data');
  if (!dialog || !content || !source || typeof dialog.showModal !== 'function') return;
  let projects;
  try { projects = JSON.parse(source.textContent); } catch { return; }
  if (!Array.isArray(projects)) return;
  let opener = null;
  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text != null) node.textContent = String(text);
    if (className) node.className = className;
    return node;
  };
  document.querySelectorAll('[data-quick-view]').forEach((trigger) => {
    const project = projects.find((item) => item && item.slug === trigger.dataset.quickView);
    if (!project || !/^[a-z0-9-]+$/.test(project.slug)) return;
    trigger.hidden = false;
    trigger.addEventListener('click', (event) => {
      event.preventDefault();
      opener = trigger;
      content.replaceChildren();
      if (project.image) {
        let imageURL;
        try { imageURL = new URL(project.image, window.location.href); } catch { /* Optional image must not prevent opening a project. */ }
        if (imageURL && imageURL.origin === window.location.origin && ['http:', 'https:', 'file:'].includes(imageURL.protocol)) {
          const image = element('img', null, 'dialog-image');
          image.src = imageURL.href;
          image.alt = '';
          image.decoding = 'async';
          content.append(image);
        }
      }
      if (project.status) content.append(element('p', project.status, 'eyebrow'));
      const title = element('h2', project.title);
      title.id = 'dialog-project-title';
      title.tabIndex = -1;
      content.append(title);
      dialog.setAttribute('aria-labelledby', title.id);
      content.append(element('p', project.summary, 'dialog-summary'));
      if (Array.isArray(project.tags) && project.tags.length) {
        const tags = element('ul', null, 'tags');
        tags.setAttribute('aria-label', 'Technologies');
        project.tags.forEach((tag) => tags.append(element('li', tag)));
        content.append(tags);
      }
      if (Array.isArray(project.contributions) && project.contributions.length) {
        content.append(element('h3', 'My contribution'));
        const list = element('ul', null, 'contribution-list');
        project.contributions.forEach((item) => list.append(element('li', item)));
        content.append(list);
      }
      const link = element('a', 'Read project details →', 'button primary');
      link.href = `project/${project.slug}.html`;
      content.append(link);
      dialog.showModal();
      title.focus();
    });
  });
  dialog.querySelector('.dialog-close')?.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    if (opener?.isConnected) opener.focus();
  });
})();
