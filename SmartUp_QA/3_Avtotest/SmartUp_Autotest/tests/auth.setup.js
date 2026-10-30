// P00: har rol uchun login → .auth/<rol>.json (storageState). Parol Keychain'dan olinadi, hech qayerga yozilmaydi.
const fs = require('fs');
const { test, expect } = require('@playwright/test');
const E = require('../lib/env');
const S = require('../lib/smt');

const status = {};
E.ensureDir(E.AUTH_DIR);

for (const r of E.CFG.roles) {
  test(`login: ${r.role} (${r.login})`, async ({ browser }) => {
    test.skip(!r.enabled, `rol o'chirilgan (config/roles.json: enabled=false)`);
    const ctx = await browser.newContext({ baseURL: E.CFG.baseURL });
    const page = await ctx.newPage();
    try {
      await S.login(page, E.CFG.baseURL, r.login, E.getPassword(r.role));
      expect(await S.isLoginPage(page), 'login muvaffaqiyatsiz (hali login sahifasida)').toBeFalsy();
      await page.goto('/xtrade/a2/trade/tvt/plan/room_list');
      await S.idle(page, 2500);
      const fil = await S.switchFilial(page, E.CFG.filial).catch(() => S.currentFilial(page));
      await ctx.storageState({ path: E.authFile(r.role) });
      status[r.role] = { ok: true, login: r.login, filial: fil };
    } catch (e) {
      status[r.role] = { ok: false, login: r.login, error: String(e.message).split('\n')[0].slice(0, 300) };
      await page.screenshot({ path: `${E.ensureDir(E.RESULTS_DIR + '/shots')}/AUTH-${r.role}.png` }).catch(() => {});
      throw e;
    } finally {
      E.writeJson('auth.json', status);
      await ctx.close();
    }
  });
}
