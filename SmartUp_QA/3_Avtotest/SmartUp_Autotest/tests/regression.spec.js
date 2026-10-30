// REGRESSION: 28.09 dagi barcha test case'lar (data/regression_cases.json) run_order tartibida, smoke (health) dan KEYIN.
// auto=false case'lar skip (sababi bilan) — ular qo'lda yoki xavfli. Natija: regression.jsonl (+ results.json).
// Filtr: CASES=TC-SPR-DIV-006,... | MODULES=Склад,Финансы | TYPES=Smoke,Validatsiya
const fs = require('fs');
const path = require('path');
const { test, expect } = require('@playwright/test');
const E = require('../lib/env');
const S = require('../lib/smt');

const DATA = JSON.parse(fs.readFileSync(process.env.REG_FILE || path.join(E.ROOT, 'data', 'regression_cases.json'), 'utf8'));
const CASES = process.env.CASES ? process.env.CASES.split(',') : null;
const MODULES = process.env.MODULES ? process.env.MODULES.split(',') : null;
const TYPES = process.env.TYPES ? process.env.TYPES.split(',') : null;

test.use({ storageState: E.authFile('admin') });

for (const c of DATA.cases) {
  if (CASES && !CASES.includes(c.id)) continue;
  if (MODULES && !MODULES.includes(c.module)) continue;
  if (TYPES && !TYPES.includes(c.type)) continue;
  const title = `[${c.phase}·${c.seq}] ${c.id} ${c.module} → ${c.form}: ${c.title}`;
  if (!c.auto) {
    test(title, () => {
      E.appendJsonl('regression.jsonl', { id: c.id, module: c.module, section: c.section, form: c.form, title: c.title, type: c.type, result: 'Skip', reason: c.skip_reason, last_result: c.last_result });
      test.skip(true, c.skip_reason || 'auto=false');
    });
    continue;
  }
  test(title, async ({ page }) => {
    test.setTimeout(180_000);
    const col = S.attachCollectors(page);
    const ctx = { col };
    const rec = { id: c.id, module: c.module, section: c.section, form: c.form, title: c.title, type: c.type, last_result: c.last_result, last_bug: c.last_bug };
    try {
      await page.goto('/xtrade/a2/trade/tvt/plan/room_list'); await S.idle(page, 1200);
      if (await S.isLoginPage(page)) await E.relogin(page, 'admin');
      col.reset();
      for (const [i, s] of c.steps.entries()) {
        // `assert_columns` va `assert_buttons` `expect.soft` ishlatadi — soft assertion
        // istisno TASHLAMAYDI: Playwright testni yiqilgan deb belgilaydi, lekin catch bloki
        // ishlamaydi va isbot (failed_step, screenshot) yozilmaydi. 29.09 yugurishida shu
        // sababli 82 ta yiqilish «Pass» deb yozilgan. Shuning uchun har qadamdan keyin
        // yangi soft xato paydo bo'lganini tekshiramiz va aynan o'sha qadamda to'xtatamiz.
        const softBefore = (test.info().errors || []).length;
        await test.step(`${i + 1}. ${s.description || s.action + ' ' + (s.target || '')}`, async () => {
          await S.run(page, s, ctx);
          if (!/^assert/.test(s.action)) await S.failOnErrorDialog(page, s);
        });
        const softAfter = test.info().errors || [];
        if (softAfter.length > softBefore) {
          rec.soft_errors = softAfter.slice(softBefore)
            .map((x) => String(x.message || '').replace(/\u001b\[\d+m/g, '').split('\n')[0].slice(0, 300));
          throw new Error('soft assert: ' + rec.soft_errors.join(' | ').slice(0, 300));
        }
        rec.steps_done = i + 1;
      }
      if (c.type === 'Validatsiya') {
        const first = (await S.main(page).innerText().catch(() => '')).slice(0, 150);
        const onForm = /%2Badd|\+add|%2Bedit|\+edit/.test(page.url()) || /создание|изменение/i.test(first) || (await page.locator('main [class*=outline-error]').count()) > 0;
        expect(onForm, 'Validatsiya: forma yopildi yoki bo\'sh forma saqlandi').toBeTruthy();
      }
      rec.result = 'Pass';
    } catch (e) {
      rec.result = 'Fail';
      rec.failed_step = (rec.steps_done || 0) + 1;
      const st = c.steps[rec.steps_done || 0] || {};
      rec.failed_desc = st.description; rec.failed_expected = st.expected;
      rec.error = String(e.message).split('\n').slice(0, 3).join(' ').slice(0, 500);
      rec.net = col.net.slice(0, 4);
      const shot = `REG-${c.id}.png`;
      await page.screenshot({ path: path.join(E.ensureDir(path.join(E.RESULTS_DIR, 'shots')), shot) }).catch(() => {});
      rec.shot = 'shots/' + shot;
      // Bug tipidagi case: Fail = bug hali bor (kutilgan), Pass = tuzatilgan
      if (c.type === 'Bug') rec.note = 'Bug case Fail — ma\'lum bug hali bor';
      throw e;
    } finally {
      rec.url = page.url();
      E.appendJsonl('regression.jsonl', rec);
    }
  });
}
