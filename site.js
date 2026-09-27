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
        window.history.replaceState(history.state, '', url);
      }
    };
    filters.forEach((button) => {
      button.disabled = false;
      button.addEventListener('click', () => applyFilter(button.dataset.filter, true));
    });
    applyFilter(new URL(window.location.href).searchParams.get('domain') || 'all');
    window.addEventListener('popstate', () => applyFilter(new URL(window.location.href).searchParams.get('domain') || 'all'));
  }

  const views = [...document.querySelectorAll('[data-view]')];
  const grids = [...document.querySelectorAll('.compact-projects')];
  const applyView = () => {
    const active = new URL(location.href).searchParams.get('view') === 'gallery' ? 'gallery' : 'overview';
    grids.forEach(grid => grid.classList.toggle('gallery-view', active === 'gallery'));
    views.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === active)));
  };
  views.forEach(button => {
    button.disabled = false;
    button.addEventListener('click', () => {
      const url = new URL(location.href);
      if (button.dataset.view === 'gallery') url.searchParams.set('view', 'gallery');
      else url.searchParams.delete('view');
      history.replaceState(history.state, '', url);
      applyView();
    });
  });
  applyView();
  window.addEventListener('popstate', applyView);

  const dialog = document.getElementById('project-dialog');
  const content = dialog?.querySelector('.dialog-content');
  const source = document.getElementById('project-data');
  if (!dialog || !content || !source || typeof dialog.showModal !== 'function') return;
  let projects;
  try { projects = JSON.parse(source.textContent); } catch { return; }
  if (!Array.isArray(projects)) return;
  let opener = null;
  let scrollPosition = 0;
  let ownsHistoryEntry = false;
  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text != null) node.textContent = String(text);
    if (className) node.className = className;
    return node;
  };
  const openProject = (project, trigger = null) => {
    if (!dialog.open) scrollPosition = window.scrollY;
    opener = trigger || document.querySelector(`[data-quick-view="${project.slug}"]`);
    content.replaceChildren();
    content.append(element('p', project.status, 'eyebrow'));
    const title = element('h2', project.title);
    title.id = 'dialog-project-title';
    title.tabIndex = -1;
    content.append(title);
    dialog.setAttribute('aria-labelledby', title.id);
    content.append(element('p', project.summary, 'dialog-summary'));
    if (project.image) {
      const imageURL = new URL(project.image, location.href);
      if (imageURL.origin === location.origin) {
        const image = element('img', null, 'dialog-image');
        image.src = imageURL.href;
        image.alt = `${project.title}: ${project.image_kind || 'illustrative visualization'}`;
        image.decoding = 'async';
        content.append(image, element('p', project.image_kind || 'Illustrative visualization', 'image-provenance'));
      }
    }
    content.append(element('h3', 'The problem'), element('p', project.objective));
    if (Array.isArray(project.contributions) && project.contributions.length) {
      content.append(element('h3', 'My contribution'));
      const list = element('ul', null, 'contribution-list');
      project.contributions.forEach(item => list.append(element('li', item)));
      content.append(list);
    }
    content.append(element('h3', 'Validation'), element('p', project.validation));
    content.append(element('h3', 'Outcome & boundaries'), element('p', project.outcome));
    if (Array.isArray(project.tags)) {
      const tags = element('ul', null, 'tags');
      tags.setAttribute('aria-label', 'Technologies');
      project.tags.forEach(tag => tags.append(element('li', tag)));
      content.append(tags);
    }
    const actions = element('div', null, 'dialog-links');
    const link = element('a', 'Full case study →', 'button primary');
    link.href = `project/${project.slug}.html`;
    actions.append(link);
    (project.links || []).forEach(sourceLink => {
      let url;
      try { url = new URL(sourceLink.url); } catch { return; }
      if (url.protocol !== 'https:') return;
      const source = element('a', `${sourceLink.label} ↗`, 'button');
      source.href = url.href;
      actions.append(source);
    });
    content.append(actions);
    document.body.classList.add('preview-open');
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
    title.focus({ preventScroll: true });
  };
  const requestedProject = () => {
    const slug = new URL(location.href).searchParams.get('project');
    return projects.find(item => item.slug === slug && /^[a-z0-9-]+$/.test(item.slug));
  };
  const closePreview = () => {
    if (ownsHistoryEntry) {
      history.back();
    } else {
      const url = new URL(location.href);
      url.searchParams.delete('project');
      history.replaceState(history.state, '', url);
      dialog.close();
    }
  };
  document.querySelectorAll('[data-quick-view]').forEach(trigger => {
    const project = projects.find(item => item.slug === trigger.dataset.quickView);
    if (!project) return;
    trigger.setAttribute('aria-haspopup', 'dialog');
    trigger.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const url = new URL(location.href);
      url.searchParams.set('project', project.slug);
      history.pushState({ portfolioPreview: true }, '', url);
      ownsHistoryEntry = true;
      openProject(project, trigger);
    });
  });
  dialog.querySelector('.dialog-close')?.addEventListener('click', closePreview);
  dialog.addEventListener('cancel', event => { event.preventDefault(); closePreview(); });
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const controls = [...dialog.querySelectorAll('a[href], button:not([disabled]), [tabindex="0"]')]
      .filter(node => node.getClientRects().length > 0);
    if (!controls.length) return;
    const first = controls[0], last = controls[controls.length - 1];
    if (event.shiftKey && (document.activeElement === first || !controls.includes(document.activeElement))) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault(); first.focus();
    }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) closePreview();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('preview-open');
    ownsHistoryEntry = false;
    if (opener?.isConnected && !opener.closest('[hidden]')) opener.focus({ preventScroll: true });
    window.scrollTo({ top: scrollPosition, behavior: 'instant' });
  });
  window.addEventListener('popstate', () => {
    const project = requestedProject();
    ownsHistoryEntry = !!history.state?.portfolioPreview;
    if (project) openProject(project);
    else if (dialog.open) dialog.close();
  });
  const initial = requestedProject();
  if (initial) openProject(initial);
})();
