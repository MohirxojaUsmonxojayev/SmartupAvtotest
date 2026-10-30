// Rollar bo'yicha kirish matritsasi: har rol (admin'dan tashqari) har sahifani ochadi va natijani yozadi.
// Kutilgan huquqlar config/expected_access.json da bo'lsa — farqlar bug sifatida belgilanadi.
const fs = require('fs');
const path = require('path');
const { test } = require('@playwright/test');
const E = require('../lib/env');
const S = require('../lib/smt');

const routes = JSON.parse(fs.readFileSync(process.env.ROUTES_FILE || path.join(E.ROOT, 'data', 'routes.json'), 'utf8'));
let expected = {};
try { expected = JSON.parse(fs.readFileSync(path.join(E.ROOT, 'config', 'expected_access.json'), 'utf8')); } catch {}

for (const r of E.CFG.roles.filter((x) => x.role !== 'admin')) {
  test(`kirish matritsasi: ${r.role}`, async ({ browser }) => {
    test.skip(!r.enabled || !fs.existsSync(E.authFile(r.role)), `rol yo'q yoki login bo'lmagan: ${r.role}`);
    test.setTimeout(routes.length * 20_000);
    const ctx = await browser.newContext({ baseURL: E.CFG.baseURL, storageState: E.authFile(r.role) });
    const page = await ctx.newPage();
    const col = S.attachCollectors(page);
    for (const rt of routes) {
      col.reset();
      const rec = { role: r.role, module: rt.module, name: rt.name, route: rt.route };
      try {
        await page.goto(rt.route); await S.idle(page, 1800);
        if (await S.isLoginPage(page)) { await E.relogin(page, r.role); await page.goto(rt.route); await S.idle(page, 1800); }
        if (await S.isLoginPage(page)) { rec.result = 'SESSION_LOST'; E.appendJsonl('access.jsonl', rec); break; }
        const L = await S.snapshot(page);
        const body = await S.main(page).innerText().catch(() => '');
        rec.title = L.title;
        rec.result = /недоступ|нет доступа|доступ запрещ|только администратор/i.test(body) ? 'DENIED'
          : L.failed || L.errDialogs.length || col.net.some((x) => x.s >= 500) ? 'ERROR' : 'OK';
        if (rec.result === 'ERROR') rec.detail = (L.errDialogs[0] || '') + ' ' + JSON.stringify(col.net.slice(0, 2));
        const exp = expected[r.role]?.[rt.route];
        if (exp && exp !== rec.result) rec.mismatch = `kutilgan ${exp}, haqiqiy ${rec.result}`;
      } catch (e) { rec.result = 'EXCEPTION'; rec.detail = String(e.message).split('\n')[0].slice(0, 200); }
      E.appendJsonl('access.jsonl', rec);
    }
    await ctx.close();
  });
}
