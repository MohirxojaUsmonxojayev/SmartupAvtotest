// Barcha a2 sahifalarni admin bilan qayta tekshirish (test case yozilmaydi — natija health.jsonl ga).
// Har sahifa: ochilish, xato/5xx, tarjima kalitlari, qator amallari, ko'rish sahifasi, yaratish formasi, bo'sh forma bilan saqlash.
const fs = require('fs');
const path = require('path');
const { test, expect } = require('@playwright/test');
const E = require('../lib/env');
const S = require('../lib/smt');

const routes = JSON.parse(fs.readFileSync(process.env.ROUTES_FILE || path.join(E.ROOT, 'data', 'routes.json'), 'utf8'));
const ONLY = process.env.MODULES ? process.env.MODULES.split(',') : null;
// Tashqi tizim / sozlama / huquq sahifalari: faqat ochiladi, hech narsa bosilmaydi
const SMOKE_ONLY = /wms|external|telegram|marking|sign_document|user_list|filial_list|subfilial|bonus|revaluation|offset|recalculate|spread_balance|system_setting|audit|rule_run|dashboard|kanban|calendar/i;
const IS_REPORT = /\/rep\/|dashboard|report/i;

test.use({ storageState: E.authFile('admin') });

for (const r of routes) {
  if (ONLY && !ONLY.includes(r.module)) continue;
  test(`[${r.module}] ${r.name}`, async ({ page }) => {
    test.setTimeout(120_000);
    const col = S.attachCollectors(page);
    const rec = { module: r.module, name: r.name, route: r.route, issues: [] };
    const issue = (kind, detail) => rec.issues.push({ kind, detail });
    try {
      await page.goto(r.route);
      await S.idle(page, 2500);
      if (await S.isLoginPage(page)) { await E.relogin(page, 'admin'); await page.goto(r.route); await S.idle(page, 2500); }
      if (await S.isLoginPage(page)) { rec.status = 'SKIP'; issue('auth', 'qayta login ham ishlamadi'); return; }
      const L = await S.snapshot(page);
      rec.list = { title: L.title, heads: L.heads.length, counter: L.counter, btns: L.btns.slice(0, 12) };
      if (L.failed) issue('load', `«Не удалось загрузить» — ${L.title}`);
      if (L.errDialogs.length) issue('error_dialog', L.errDialogs[0]);
      if (L.keys.length) issue('i18n_key', L.keys.join(', '));
      if (!SMOKE_ONLY.test(r.route) && !L.failed) {
        // qator amallari + ko'rish
        const acts = await S.rowActions(page).catch(() => null);
        rec.rowActs = acts;
        const view = (acts || []).find((a) => /^Просмотр/.test(a));
        if (view) {
          col.reset();
          await S.btn(page, view).click();
          await S.idle(page, 2500);
          const V = await S.snapshot(page);
          rec.view = { title: V.title, labels: V.labels.length };
          if (V.failed) issue('view_load', V.title);
          if (V.errDialogs.length) issue('view_error_dialog', V.errDialogs[0]);
          if (V.keys.length) issue('view_i18n_key', V.keys.join(', '));
          for (const t of (await page.locator('main [role=tab]:visible').all()).slice(1, 10)) {
            const name = (await t.innerText()).trim();
            col.reset(); await t.click().catch(() => {}); await S.idle(page, 1200);
            const T = await S.snapshot(page);
            if (col.net.some((x) => x.s >= 500) || T.errDialogs.length) issue('view_tab_error', `${name}: ${JSON.stringify(col.net.slice(0, 2))} ${T.errDialogs[0] || ''}`);
            await S.closeDialogs(page);
          }
          await page.goto(r.route); await S.idle(page, 2000);
        }
        // yaratish formasi + bo'sh saqlash
        const create = S.btn(page, 'Создать', S.main(page));
        const add = S.btn(page, 'Добавить', S.main(page));
        const cb = (await create.count()) ? create : ((await add.count()) ? add : null);
        if (cb && !IS_REPORT.test(r.route)) {
          const c0 = (await S.snapshot(page)).counter;
          col.reset();
          await cb.click(); await S.idle(page, 2500);
          const menu = await page.locator('.cdk-overlay-pane [role=menuitem]:visible, .cdk-overlay-pane button:visible').allInnerTexts().catch(() => []);
          if (menu.length && page.url().includes(r.route.split('?')[0].replace('+', '%2B'))) {
            rec.createMenu = menu.map((x) => x.trim()).slice(0, 20);
            await page.keyboard.press('Escape');
          } else {
            const C = await S.snapshot(page);
            rec.create = { title: C.title, labels: C.labels.length, required: C.labels.filter((x) => x.endsWith('*')).length };
            const i18n404 = col.net.filter((x) => x.s === 404 && /i18n/.test(x.u));
            if (i18n404.length) issue('i18n_404', i18n404.map((x) => x.u.split('/').pop()).join(', '));
            if (C.keys.length) issue('create_i18n_key', C.keys.join(', '));
            if (C.errDialogs.length) issue('create_error_dialog', C.errDialogs[0]);
            const save = S.btn(page, 'Сохранить', S.main(page));
            if (rec.create.required && (await save.count()) && (await save.isEnabled().catch(() => false))) {
              const formUrl = page.url();
              col.reset();
              await save.click(); await S.idle(page, 2000);
              const ask = page.locator('[role=dialog]').filter({ hasText: /Сохранить\?/ });
              if (await ask.count()) { await ask.locator('button').filter({ hasText: S.YES }).first().click(); await S.idle(page, 2000); }
              const after = await S.snapshot(page);
              if (after.errDialogs.length) issue('empty_save_error', after.errDialogs[0]);
              if (col.net.some((x) => x.s >= 500)) issue('empty_save_5xx', JSON.stringify(col.net.slice(0, 2)));
              if (page.url() !== formUrl) issue('empty_save_left_form', `bo'sh forma saqlandi yoki forma yopildi: ${page.url()}`);
              await S.closeDialogs(page);
            }
            const close = S.btn(page, 'Закрыть', S.main(page));
            if (await close.count()) { await close.click().catch(() => {}); await page.waitForTimeout(800); const d = page.locator('[role=dialog] button').filter({ hasText: S.YES }); if (await d.count()) await d.first().click(); }
            await page.goto(r.route); await S.idle(page, 2000);
            const c1 = (await S.snapshot(page)).counter;
            if (c0 && c1 && c0 !== c1) issue('empty_save_leaked', `hisoblagich ${c0} → ${c1}`);
          }
        }
      }
      if (IS_REPORT.test(r.route)) {
        const gen = S.btn(page, 'Сформировать', S.main(page));
        if ((await gen.count()) && !SMOKE_ONLY.test(r.route)) {
          col.reset(); await gen.click(); await S.idle(page, 5000);
          const G = await S.snapshot(page);
          if (G.errDialogs.length) issue('report_error', G.errDialogs[0]);
          if (col.net.some((x) => x.s >= 500)) issue('report_5xx', JSON.stringify(col.net.slice(0, 2)));
          rec.report = { requiredRed: await page.locator('main [class*=outline-error]:visible').count() };
        }
      }
      const five = col.net.filter((x) => x.s >= 500 || (x.s >= 400 && x.s !== 404));
      if (five.length) issue('http_error', JSON.stringify(five.slice(0, 3)));
      rec.status = rec.issues.length ? 'BUG' : 'OK';
    } catch (e) {
      rec.status = 'ERROR'; issue('exception', String(e.message).split('\n')[0].slice(0, 300));
    } finally {
      if (rec.status !== 'OK') {
        const shot = `HEALTH-${r.module}-${r.name}`.replace(/[^\wА-Яа-яЁё-]+/g, '_').slice(0, 90) + '.png';
        await page.screenshot({ path: path.join(E.ensureDir(path.join(E.RESULTS_DIR, 'shots')), shot) }).catch(() => {});
        rec.shot = 'shots/' + shot;
      }
      rec.console = col.cons.slice(0, 3);
      E.appendJsonl('health.jsonl', rec);
    }
    expect.soft(rec.issues, rec.issues.map((x) => `${x.kind}: ${x.detail}`).join('\n')).toEqual([]);
  });
}
