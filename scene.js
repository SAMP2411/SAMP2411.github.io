/* Pause decorative motion when requested, offscreen, or in a hidden tab. */
(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('.robotics-visual').forEach(scene => {
    const button = scene.querySelector('.scene-toggle');
    let manualPause = false;
    let inView = true;
    const update = () => {
      scene.classList.toggle('scene-paused', manualPause || reduced.matches || !inView || document.hidden);
      if (button) {
        button.hidden = reduced.matches;
        button.setAttribute('aria-pressed', String(manualPause));
        button.textContent = manualPause ? 'Resume motion' : 'Pause motion';
      }
    };
    button?.addEventListener('click', () => { manualPause = !manualPause; update(); });
    document.addEventListener('visibilitychange', update);
    if (reduced.addEventListener) reduced.addEventListener('change', update);
    else reduced.addListener(update);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => {
        inView = entries[0].isIntersecting;
        update();
      }, { threshold: 0.05 }).observe(scene);
    }
    update();
    scene.classList.add('scene-ready');
  });
})();
