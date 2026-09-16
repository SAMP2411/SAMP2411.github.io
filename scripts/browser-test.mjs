/** Run against a static server: npm install --no-save playwright @axe-core/playwright
 *  npx playwright install chromium; node scripts/browser-test.mjs */
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const base = new URL(process.env.BASE_URL || 'http://localhost:8000/');
const out = path.resolve(process.env.QA_OUTPUT || 'qa-output');
await fs.mkdir(out, { recursive: true });
const failures = [];
const checks = [];
const measurements = [];
const fallbackChecks = [];
const notFoundChecks = [];
function assert(condition, message) { if (!condition) failures.push(message); }
const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
const page = await context.newPage();
page.on('pageerror', error => failures.push(`JS: ${page.url()}: ${error.message}`));
page.on('console', message => { if (message.type() === 'error') failures.push(`Console: ${page.url()}: ${message.text()}`); });
page.on('response', response => {
  if (new URL(response.url()).origin === base.origin && response.status() >= 400)
    failures.push(`HTTP ${response.status()}: ${response.url()}`);
});
page.on('requestfailed', request => {
  if (new URL(request.url()).origin === base.origin) failures.push(`Failed request: ${request.url()}: ${request.failure()?.errorText}`);
});
const queue = [base.href];
const visited = new Set();
const sitemapResponse = await context.request.get(new URL('sitemap.xml', base).href);
if (sitemapResponse.ok()) {
  for (const [, location] of (await sitemapResponse.text()).matchAll(/<loc>\s*([^<]+)\s*<\/loc>/g)) {
    const original = new URL(location.trim());
    queue.push(new URL(original.pathname.replace(/^\//, ''), base).href);
  }
}
try {
  while (queue.length) {
    const address = new URL(queue.shift()); address.search = ''; address.hash = '';
    if (visited.has(address.href)) continue;
    visited.add(address.href);
    const response = await page.goto(address.href, { waitUntil: 'networkidle' });
    assert(response?.ok(), `Page status: ${address.href}: ${response?.status()}`);
    const links = await page.locator('a[href]').evaluateAll(nodes => nodes.map(node => node.href));
    for (const link of links) {
      const url = new URL(link);
      if (url.origin === base.origin && (url.pathname.endsWith('.html') || url.pathname.endsWith('/'))) queue.push(url.href);
    }
    // Force lazy images to load, then return to the top for screenshots.
    await page.evaluate(async () => {
      for (const image of document.images) { image.loading = 'eager'; }
      await Promise.all([...document.images].map(image => image.decode().catch(() => {})));
    });
    const broken = await page.locator('img').evaluateAll(nodes => nodes.filter(n => !n.complete || !n.naturalWidth || !n.naturalHeight).map(n => n.currentSrc || n.src));
    assert(!broken.length, `${address.pathname}: broken images: ${broken.join(', ')}`);
    measurements.push(await page.evaluate(() => {
      const navigation = performance.getEntriesByType('navigation')[0];
      return {
        url: location.href,
        measurementType: 'Browser navigation timings and DOM inventory; not Lighthouse or field Core Web Vitals',
        domElements: document.getElementsByTagName('*').length,
        resourceCount: performance.getEntriesByType('resource').length,
        navigation: navigation ? { domContentLoadedMs: navigation.domContentLoadedEventEnd, loadMs: navigation.loadEventEnd, responseEndMs: navigation.responseEnd, transferBytes: navigation.transferSize } : null,
        images: [...document.images].map(image => ({ src: image.currentSrc || image.src, naturalWidth: image.naturalWidth, naturalHeight: image.naturalHeight, renderedWidth: Math.round(image.getBoundingClientRect().width), renderedHeight: Math.round(image.getBoundingClientRect().height) })),
      };
    }));
    const missingAnchors = await page.locator('a[href]').evaluateAll(nodes => nodes.filter(node => {
      const url = new URL(node.href);
      return url.origin === location.origin && url.pathname === location.pathname && url.hash && !document.getElementById(decodeURIComponent(url.hash.slice(1)));
    }).map(n => n.getAttribute('href')));
    assert(!missingAnchors.length, `${address.pathname}: missing anchors: ${missingAnchors}`);
    for (const width of [390, 768, 1440]) {
      await page.setViewportSize({ width, height: 1000 });
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${address.pathname}: horizontal overflow at ${width}px`);
      await page.screenshot({ path: path.join(out, `${address.pathname.replace(/[^a-z0-9]/gi, '_') || 'home'}-${width}.png`), fullPage: true, animations: 'disabled' });
    }
    const axe = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
    failures.push(...axe.violations.map(v => `${address.pathname}: accessibility ${v.id}: ${v.nodes.map(n => n.target.join(' ')).join(', ')}`));
    await page.setViewportSize({ width: 390, height: 844 });
    const skip = page.locator('.skip-link');
    if (await skip.count()) {
      await skip.focus();
      assert(await skip.evaluate(n => {
        const rect = n.getBoundingClientRect();
        const style = getComputedStyle(n);
        return n === document.activeElement && rect.top >= 0 && rect.bottom <= innerHeight && style.visibility !== 'hidden';
      }), `${address.pathname}: focused skip link is not onscreen`);
      await page.keyboard.press('Enter');
      assert(await page.evaluate(() => document.activeElement === document.querySelector('main') || document.querySelector('main')?.contains(document.activeElement) || location.hash === '#main'), `${address.pathname}: skip link does not reach main`);
    }
    const toggle = page.locator('.nav-toggle');
    if (await toggle.isVisible()) {
      await toggle.focus(); await page.keyboard.press('Enter');
      assert(await toggle.getAttribute('aria-expanded') === 'true', `${address.pathname}: keyboard menu did not open`);
      await page.keyboard.press('Tab');
      assert(await page.evaluate(() => !!document.activeElement.closest('#primary-nav')), `${address.pathname}: Tab did not enter menu`);
      await page.keyboard.press('Escape');
      assert(await toggle.getAttribute('aria-expanded') === 'false', `${address.pathname}: Escape did not close menu`);
      assert(await toggle.evaluate(n => n === document.activeElement), `${address.pathname}: menu focus not restored`);
    }
    for (const filter of await page.locator('button[data-filter]').all()) {
      await filter.click();
      const domain = await filter.getAttribute('data-filter');
      assert(await filter.getAttribute('aria-pressed') === 'true', `${address.pathname}: filter ${domain} not selected`);
      assert(await page.locator('[data-domains]').evaluateAll((nodes, selected) => nodes.every(n => n.hidden === !(selected === 'all' || n.dataset.domains.toLowerCase().split(/\s+/).includes(selected))), domain), `${address.pathname}: incorrect ${domain} results`);
    }
    const all = page.locator('button[data-filter="all"]');
    if (await all.count()) await all.click();
    const quick = page.locator('[data-quick-view]:visible').first();
    if (await quick.count()) {
      await quick.click();
      const dialog = page.locator('#project-dialog');
      assert(await dialog.evaluate(n => n.open), `${address.pathname}: quick view not open`);
      assert(await dialog.locator('h2').textContent(), `${address.pathname}: dialog missing title`);
      assert(await dialog.locator('h2').evaluate(n => n === document.activeElement), `${address.pathname}: dialog title lacks initial focus`);
      await page.keyboard.press('Tab');
      assert(await page.evaluate(() => !!document.activeElement.closest('#project-dialog')), `${address.pathname}: dialog Tab escapes`);
      for (let tab = 0; tab < 5; tab++) {
        await page.keyboard.press('Shift+Tab');
        assert(await page.evaluate(() => !!document.activeElement.closest('#project-dialog')), `${address.pathname}: dialog reverse Tab escapes`);
      }
      await page.keyboard.press('Escape');
      await page.waitForFunction(() => !document.querySelector('#project-dialog').open);
      assert(await quick.evaluate(n => n === document.activeElement), `${address.pathname}: dialog focus not restored`);
    }
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    const scenes = page.locator('.robotics-visual');
    for (const scene of await scenes.all()) {
      assert(await scene.evaluate(n => n.classList.contains('scene-paused')), `${address.pathname}: reduced-motion scene not paused`);
      assert(await scene.locator('.scene-toggle').isHidden(), `${address.pathname}: reduced-motion toggle visible`);
    }
    await page.emulateMedia({ reducedMotion: 'no-preference' });
    for (const scene of await scenes.all()) {
      await scene.scrollIntoViewIfNeeded();
      const pause = scene.locator('.scene-toggle');
      if (await pause.isVisible()) {
        await pause.click();
        assert(await scene.evaluate(n => n.classList.contains('scene-paused')), `${address.pathname}: manual pause failed`);
        assert(await pause.getAttribute('aria-pressed') === 'true', `${address.pathname}: pause state missing`);
        await pause.click();
        assert(await pause.getAttribute('aria-pressed') === 'false', `${address.pathname}: resume state missing`);
      }
    }
    checks.push(address.href);
  }
  const noJSContext = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
  const fallback = await noJSContext.newPage();
  fallback.on('response', response => {
    if (new URL(response.url()).origin === base.origin && response.status() >= 400) failures.push(`No-JS HTTP ${response.status()}: ${response.url()}`);
  });
  for (const file of ['', 'projects.html']) {
    const url = new URL(file, base).href;
    const response = await fallback.goto(url, { waitUntil: 'networkidle' });
    assert(response?.ok(), `No-JS page failed: ${url}`);
    assert((await fallback.locator('main').innerText()).trim().length > 100, `No-JS content missing: ${url}`);
    assert(await fallback.locator('#primary-nav a[href]:visible').count() > 0, `No-JS navigation unavailable: ${url}`);
    const cards = fallback.locator('[data-domains]');
    assert(await cards.count() > 0, `No-JS project cards missing: ${url}`);
    for (const card of await cards.all()) {
      assert(await card.isVisible(), `No-JS hidden project card: ${url}`);
      assert(await card.locator('a[href]:not([aria-hidden="true"])').count() > 0, `No-JS project has no accessible text link: ${url}`);
    }
    await fallback.evaluate(async () => {
      for (const image of document.images) image.loading = 'eager';
      await Promise.all([...document.images].map(image => image.decode().catch(() => {})));
    });
    const failedImages = await fallback.locator('img').evaluateAll(images => images.filter(image => !image.naturalWidth || !image.naturalHeight).map(image => image.src));
    assert(!failedImages.length, `No-JS broken images: ${url}: ${failedImages.join(', ')}`);
    assert(await fallback.locator('[data-quick-view]:visible').count() === 0, `No-JS inert quick-view controls visible: ${url}`);
    fallbackChecks.push({ url, projectCards: await cards.count(), brokenImages: failedImages });
    await fallback.screenshot({ path: path.join(out, `no-js-${file || 'home'}.png`), fullPage: true });
  }
  await noJSContext.close();
  // Isolate expected 404 responses from the ordinary-page error listeners.
  const errorPage = await context.newPage();
  const custom404 = await errorPage.goto(new URL('404.html', base).href, { waitUntil: 'networkidle' });
  assert(custom404 && [200, 404].includes(custom404.status()), 'Custom 404 document unavailable');
  assert(await errorPage.locator('h1').count() === 1, 'Custom 404 document has no unique heading');
  assert(await errorPage.locator('a[href]').count() > 0, 'Custom 404 document has no recovery link');
  notFoundChecks.push({ url: errorPage.url(), status: custom404?.status(), type: 'custom document' });
  const missingURL = new URL(`__qa_missing_${Date.now()}.html`, base).href;
  const missing = await context.request.get(missingURL);
  assert(missing.status() === 404, `Unknown URL must return HTTP 404, received ${missing.status()}`);
  notFoundChecks.push({ url: missingURL, status: missing.status(), type: 'unknown route' });
  await errorPage.close();
} catch (error) { failures.push(error.stack || String(error)); }
finally { await browser.close(); }
const report = { base: base.href, pages: checks, measurements, noJavaScript: fallbackChecks, notFound: notFoundChecks, failures: [...new Set(failures)] };
await fs.writeFile(path.join(out, 'report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
process.exitCode = report.failures.length ? 1 : 0;
