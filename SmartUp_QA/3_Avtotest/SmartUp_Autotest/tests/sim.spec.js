// Biznes-jarayon simulyatsiyasi: data/sim_scenarios.json dagi ssenariylar run_order bo'yicha, har biri o'z roli bilan.
// SIM-<RUN>- prefiksli ma'lumotlar tizimda QOLADI (test server). Rol hali yaratilmagan bo'lsa — admin bilan, belgi qo'yiladi.
const fs = require('fs');
const path = require('path');
const { test } = require('@playwright/test');
const E = require('../lib/env');
const S = require('../lib/smt');

const DATA = JSON.parse(fs.readFileSync(process.env.SIM_FILE || path.join(E.ROOT, 'data', 'sim_scenarios.json'), 'utf8'));
const ONLY = process.env.SCENARIOS ? process.env.SCENARIOS.split(',') : null;
const tpl = (v) => (typeof v === 'string' ? v.replace(/\{\{RUN\}\}/g, E.SIM_RUN) : v);
const fill = (s) => ({ ...s, target: tpl(s.target), value: tpl(s.value), ops: s.ops && s.ops.map(fill) });

for (const sc of DATA.scenarios) {
  if (ONLY && !ONLY.includes(sc.id)) continue;
  (sc.runnable ? test : test.fixme)(`${sc.id} [${sc.role}] ${sc.module} → ${sc.form}: ${sc.title}`, async ({ browser }) => {
    test.setTimeout(240_000);
    const role = E.CFG.roles.find((x) => x.role === sc.role && x.enabled) && fs.existsSync(E.authFile(sc.role)) ? sc.role : 'admin';
    const ctx = await browser.newContext({ baseURL: E.CFG.baseURL, storageState: E.authFile(role) });
    const page = await ctx.newPage();
    const col = S.attachCollectors(page);
    const rec = { id: sc.id, source_case: sc.source_case, module: sc.module, section: sc.section, form: sc.form, title: sc.title, role_planned: sc.role, role_used: role, known_bug: sc.known_bug, run: E.SIM_RUN, steps_done: 0, steps_total: sc.steps.length };
    try {
      await page.goto('/xtrade/a2/trade/tvt/plan/room_list'); await S.idle(page, 1500);
      if (await S.isLoginPage(page)) await E.relogin(page, role);
      for (const [i, raw] of sc.steps.entries()) {
        const s = fill(raw);
        await test.step(`${i + 1}. ${s.description || s.action + ' ' + (s.target || '')}`, async () => {
          if (await S.isLoginPage(page)) throw new Error('sessiya yo\'q (login sahifasi)');
          await S.run(page, s);
          await S.failOnErrorDialog(page);
        });
        rec.steps_done = i + 1;
      }
      rec.status = 'OK';
    } catch (e) {
      rec.status = 'FAIL';
      rec.failed_step = rec.steps_done + 1;
      const st = fill(sc.steps[rec.steps_done] || {});
      rec.failed_desc = st.description; rec.failed_expected = st.expected;
      rec.error = String(e.message).split('\n').slice(0, 3).join(' ').slice(0, 500);
      rec.net = col.net.slice(0, 4);
      const shot = `SIM-${sc.id}.png`.replace(/[^\w.-]+/g, '_');
      await page.screenshot({ path: path.join(E.ensureDir(path.join(E.RESULTS_DIR, 'shots')), shot), fullPage: false }).catch(() => {});
      rec.shot = 'shots/' + shot;
      throw e;
    } finally {
      rec.url = page.url();
      E.appendJsonl('sim.jsonl', rec);
      await ctx.close();
    }
  });
}
