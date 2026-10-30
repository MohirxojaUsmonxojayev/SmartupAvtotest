// SmartUp xtrade tungi avtotest. Loyihalar: setup (login) → health (admin) + access (rollar) → sim (biznes-simulyatsiya).
const path = require('path');
const { defineConfig } = require('@playwright/test');
const E = require('./lib/env');

module.exports = defineConfig({
  testDir: './tests',
  outputDir: path.join(E.RESULTS_DIR, `artifacts-${process.env.PHASE || 'all'}`),
  timeout: 120_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  workers: 1,                 // sessiya va ma'lumot bir-biriga halaqit bermasligi uchun ketma-ket
  retries: 0,
  reporter: [
    ['list'],
    ['json', { outputFile: path.join(E.RESULTS_DIR, `results-${process.env.PHASE || 'all'}.json`) }],
    ['html', { outputFolder: path.join(E.RESULTS_DIR, `html-${process.env.PHASE || 'all'}`), open: 'never' }],
  ],
  use: {
    baseURL: E.CFG.baseURL,
    viewport: { width: 1600, height: 1000 },
    locale: 'ru-RU',
    timezoneId: 'Asia/Tashkent',
    headless: process.env.HEADED ? false : true,
    launchOptions: process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {},
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
    actionTimeout: 20_000,
    navigationTimeout: 45_000,
  },
  projects: [
    { name: 'setup', testMatch: /auth\.setup\.js/ },
    { name: 'health', testMatch: /health\.spec\.js/, dependencies: ['setup'] },          // SMOKE
    { name: 'regression', testMatch: /regression\.spec\.js/, dependencies: ['health'] }, // smoke'dan KEYIN
    { name: 'access', testMatch: /access\.spec\.js/, dependencies: ['setup'] },
    { name: 'sim', testMatch: /sim\.spec\.js/, dependencies: ['setup'] },
  ],
});
