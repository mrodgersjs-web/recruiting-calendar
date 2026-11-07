import { test } from '@e2e-dev/web';
import { expect } from 'e2e';
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
const SITE = process.env.RIG_E2E_RC_SITE || '/Users/rig128gb/Developer/recruiting-calendar/site';
const BASE = process.env.RIG_E2E_RC_BASE || 'http://127.0.0.1:4519';
const TRAP = () => { (window as any).__errs = []; const o = console.error; console.error = (...a: any[]) => { (window as any).__errs.push(a.map(String).join(' ')); o(...a); }; addEventListener('error', e => (window as any).__errs.push('uncaught: ' + e.message)); addEventListener('unhandledrejection', e => (window as any).__errs.push('rejection: ' + String((e as any).reason))); };
function pages(): string[] { const out = ['/']; const walk = (d: string, p: string) => { for (const n of readdirSync(d)) { const f = d + '/' + n; if (statSync(f).isDirectory()) { if (existsSync(f + '/index.html')) out.push(p + n + '/'); walk(f, p + n + '/'); } else if (n.endsWith('.html') && n !== 'index.html') out.push(p + n); } }; walk(SITE, '/'); return out; }
const RING = '[data-ring], .sr__stage, story-ring, .ring';
async function go(app: any, browser: any, path: string, w = 1440) { await browser.setViewport({ width: w, height: w > 500 ? 900 : 844 }); await browser.addInitScript(TRAP); await browser.goto(BASE + path); await browser.evaluate(() => new Promise(r => setTimeout(r, 800))); }

test('home ring loads and autoplay rotates', { tags: ['smoke', 'ring'] }, async ({ app, browser }) => {
  await go(app, browser, '/');
  await expect(browser.locator(RING).first()).toBeVisible();
  const a = await browser.evaluate(() => document.querySelector('[data-live],.sr__hero.is-on,[aria-current]')?.textContent ?? document.querySelector('.is-on')?.outerHTML?.slice(0, 200) ?? '');
  await browser.evaluate(() => new Promise(r => setTimeout(r, 6500)));
  const b = await browser.evaluate(() => document.querySelector('[data-live],.sr__hero.is-on,[aria-current]')?.textContent ?? document.querySelector('.is-on')?.outerHTML?.slice(0, 200) ?? '');
  expect(a, 'active athlete must change after 5s autoplay').not.toBe(b);
});

test('athlete pick opens a story with scroll beats', { tags: ['story'] }, async ({ app, browser }) => {
  await go(app, browser, '/');
  await browser.locator('[data-read], .sr__read, a[href*="story"]').first().click();
  await browser.evaluate(() => new Promise(r => setTimeout(r, 1200)));
  expect(await browser.url()).toMatch(/story/);
  const n = await browser.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += innerHeight / 2) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } return [...document.querySelectorAll('.beat, [data-beat]')].filter(e => (e as HTMLElement).offsetHeight > 0 && getComputedStyle(e).visibility !== 'hidden').length; });
  expect(n, 'visible scroll beats').toBeGreaterThanOrEqual(2);
});

test('playbook Add updates the bag', { tags: ['bag'] }, async ({ app, browser }) => {
  await go(app, browser, '/');
  const before = await browser.evaluate(() => document.querySelector('[data-bag-count]')?.textContent ?? 'MISSING');
  expect(before, 'bag counter exists').not.toBe('MISSING');
  await browser.locator('[data-add], .sr__add').first().click();
  const after = await browser.evaluate(() => document.querySelector('[data-bag-count]')?.textContent);
  expect(Number(after)).toBe(Number(before) + 1);
});

test('checkout button reaches the test endpoint', { tags: ['checkout'] }, async ({ app, browser }) => {
  const hits: string[] = [];
  await browser.route(BASE + '/api/checkout', async (route: any) => { hits.push(route.request.method + ' ' + (route.request.postData || '')); await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ url: BASE + '/#test-checkout' }) }); });
  await go(app, browser, '/');
  const n = await browser.evaluate(() => document.querySelectorAll('[data-offer]').length);
  expect(n, '[data-offer] buttons on home').toBeGreaterThan(0);
  await browser.locator('[data-offer]').first().click();
  await browser.evaluate(() => new Promise(r => setTimeout(r, 1500)));
  expect(hits.length, 'POST /api/checkout fired').toBeGreaterThan(0);
  expect(hits[0]).toMatch(/^POST/);
  expect(await browser.url()).not.toMatch(/cs_live/);
});

for (const w of [1440, 390]) test(`every page: no console errors, no horizontal overflow @${w}`, { tags: ['smoke', 'pages'] }, async ({ app, browser }) => {
  const bad: string[] = [];
  for (const p of pages()) {
    await go(app, browser, p, w);
    const r = await browser.evaluate(() => ({ errs: (window as any).__errs || [], ov: document.documentElement.scrollWidth - innerWidth, wide: [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.right > innerWidth + 1 && getComputedStyle(e).position !== 'fixed'; }).slice(0, 3).map(e => e.tagName + '.' + (e as HTMLElement).className) }));
    if (r.errs.length) bad.push(`${p} console: ${r.errs.slice(0, 2).join(' | ')}`);
    if (r.ov > 1) bad.push(`${p} overflow ${r.ov}px: ${r.wide.join(',')}`);
  }
  expect(bad, bad.join('\n')).toEqual([]);
});

test('every rule on screen has a citation link', { tags: ['smoke', 'citations'] }, async ({ app, browser }) => {
  const bad: string[] = [];
  for (const p of pages()) {
    await go(app, browser, p);
    const miss = await browser.evaluate(() => [...document.querySelectorAll('[data-rule], .rule, tr[data-bylaw], .evrow, [data-fact]')].filter(e => !e.querySelector('a[href^="http"]') && !(e.closest('[data-rule]') || e).querySelector('a[href^="http"]')).slice(0, 3).map(e => (e.textContent || '').trim().slice(0, 60)));
    const bylawTxt = await browser.evaluate(() => [...document.querySelectorAll('p,li,td,span')].filter(e => /Bylaw\s+\d/i.test(e.textContent || '') && e.children.length < 6 && !e.closest('*:has(a[href^="http"])')).slice(0, 2).map(e => (e.textContent || '').trim().slice(0, 60)));
    for (const m of [...miss, ...bylawTxt]) bad.push(`${p}: "${m}"`);
  }
  expect(bad, bad.join('\n')).toEqual([]);
});

test('no real person gets a generated likeness (IMAGES.json)', { tags: ['smoke', 'likeness'] }, async ({ app, browser }) => {
  const cands = ['/Users/rig128gb/Developer/recruiting-calendar/v3/W2-images/IMAGES.json', SITE + '/IMAGES.json', SITE + '/assets/IMAGES.json', SITE + '/img/IMAGES.json'];
  const f = cands.find(existsSync); expect(f, 'IMAGES.json must exist in site/ when any generated image ships').toBeTruthy();
  const raw = JSON.parse(readFileSync(f!, 'utf8')); const list: any[] = Array.isArray(raw) ? raw : raw.images ?? Object.values(raw);
  const bad = list.filter(i => /generat|ai|illustration/i.test(String(i.source ?? i.kind ?? i.label ?? '')) && (i.real === true || /real/i.test(String(i.subject ?? i.athlete_type ?? '')) || !/composite/i.test(JSON.stringify(i))));
  expect(bad.map(i => i.file ?? i.src), 'generated images bound to non-composite subjects').toEqual([]);
  const gen = new Set(list.filter(i => /generat|ai/i.test(JSON.stringify(i))).map(i => String(i.file ?? i.src).split('/').pop()));
  const unl: string[] = [];
  for (const p of pages()) { await go(app, browser, p); const s = await browser.evaluate(() => [...document.querySelectorAll('img,video')].map(e => ({ src: ((e as any).currentSrc || (e as any).src || '').split('/').pop(), lab: (e.closest('figure')?.textContent || '') + (e.getAttribute('alt') || '') + (e.parentElement?.textContent || '') }))); for (const x of s) if (gen.has(x.src) && !/illustration/i.test(x.lab)) unl.push(`${p} ${x.src}`); }
  expect(unl, 'generated media shown without "Illustration" label').toEqual([]);
});
