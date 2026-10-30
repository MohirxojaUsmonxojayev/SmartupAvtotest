# SmartUp xtrade — tungi avtotest va biznes-simulyatsiya (Mac'da o'zi ishlaydi)

## Muammo va yechim

| Muammo | Nega shunday | Yechim shu loyihada |
|---|---|---|
| SmartUp sessiyasi bir necha soatdan keyin tugaydi, kechasi login sahifasi chiqadi | Claude'ning brauzer paneli siz kirgan sessiyaga tayanadi; Claude parol kiritmaydi | Login'ni **Mac'dagi Playwright skripti** qiladi: parol macOS **Keychain**'da, har kecha yangidan kiradi, sessiya yo'qolsa o'zi qayta kiradi (`relogin`) |
| Biznesni simulyatsiya qilish uchun bir nechta profil (rol) kerak | Har rol — alohida login/parol | `config/roles.json` da 4 rol; har biri o'z sessiyasi (`.auth/<rol>.json`) bilan ishlaydi |
| Claude'ning bulutdagi muhiti SmartUp serveriga ulana olmaydi | Tarmoq ruxsatnomasi (allowlist) — app3.greenwhite.uz yopiq | Testlar Mac'ning o'zida (uy/ofis tarmog'i) ishlaydi; Claude ertalab **natija fayllarini** tahlil qiladi |

Natija: kechasi 04:00 da Mac `launchd` orqali testlarni o'zi yuritadi (siz ham, Claude ham kerak emas). Ertalab 07:29 da Claude'ning rejalashtirilgan vazifasi natijalarni o'qib, yangi buglar uchun hisobot va test case yozadi.

```
04:00  launchd → scripts/nightly.sh
        ├─ setup  : har rol login (Keychain) → .auth/<rol>.json
        ├─ health : SMOKE — 226 ta a2 sahifa (admin): ochilish, 5xx, tarjima kalitlari, ko'rish, yaratish formasi, bo'sh saqlash, hisobot
        ├─ regression : smoke'dan KEYIN — 28.09 dagi 858 test case run_order tartibida (563 avtomat, qolgani sababi bilan Skip)
        ├─ access : har rol × 226 sahifa — OK / DENIED / ERROR matritsasi
        └─ sim    : 51 ssenariy (43 avtomat) — ma'lumotnoma → ombor → savdo → moliya…; SIM-<sana>- ma'lumotlar QOLADI
       → SmartUp_QA/3_Avtotest/Tungi_natijalar/<sana>/ (health.jsonl, regression.jsonl, access.jsonl, sim.jsonl, shots/, html/, results.json, DONE.json)
07:29  Claude (rejalashtirilgan vazifa) → scripts/analyze.py → candidates.json + SUMMARY.md
       → yangi buglar: hisobotlar/*.md + bug_test_cases.md/json/xlsx (night_report.py) → xabar
```

## Bir martalik o'rnatish (≈15 daqiqa)

**1. SmartUp'da rollar uchun foydalanuvchilar** (Главное → Пользователи → Создать) — o'zingiz yaratasiz, parolni o'zingiz qo'yasiz:

| Rol (`roles.json`) | Login (o'zgartirsangiz — roles.json ga ham yozing) | SmartUp roli | Штат / Организации |
|---|---|---|---|
| admin | mohir@xan (mavjud) | Админ | Toshkent |
| kladovshik | qa_kladovshik@xan | Кладовщик (ombor hujjatlari) | Toshkent, WH-Yashnobod ga ruxsat |
| buxgalter | qa_buxgalter@xan | Бухгалтер | Toshkent |
| agent | qa_agent@xan | Торговый представитель | Toshkent, Room - Yashnobod |

Yaratgach `config/roles.json` da o'sha rol uchun `"enabled": true` qiling. Hali yaratilmagan rol qadamlari admin bilan bajariladi va hisobotda «admin bilan (rol yo'q)» deb belgilanadi.

**2. Terminal** (loyiha papkasida):
```bash
cd ~/Desktop/Cowork/SmartUp_QA/3_Avtotest/SmartUp_Autotest
bash scripts/setup_mac.sh          # npm, Chromium, admin paroli → Keychain, login sinovi, launchd 04:00, pmset 03:55 uyg'onish
bash scripts/add_password.sh kladovshik   # har rol uchun (parol ekranda ko'rinmaydi)
bash scripts/add_password.sh buxgalter
bash scripts/add_password.sh agent
```

**3. Diskka to'liq kirish** (launchd Desktop'ga yozishi uchun): Системные настройки → Конфиденциальность и безопасность → Полный доступ к диску → «+» → `/bin/bash` va `which node` ko'rsatgan fayl.

**4. Kechasi:** Mac quvvatga ulangan, qopqoq ochiq (yoki tashqi monitor bilan), foydalanuvchi tizimdan chiqmagan (ekran qulflangan bo'lishi mumkin). Claude ilovasi 07:29 dagi tahlil uchun ochiq tursin.

## Smoke → Regression tartibi (qanday ta'minlangan)

- `scripts/nightly.sh` bosqichlarni **qat'iy ketma-ket** yuritadi: `setup → health (smoke) → regression → access → sim`. Har bosqich alohida `--no-deps` bilan ishga tushadi, shuning uchun smoke'da bug chiqsa ham regression **baribir** yuradi; faqat login bo'lmasa to'xtaydi.
- `playwright.config.js` da ham `regression` loyihasi `dependencies: ['health']` — ya'ni `npx playwright test --project=regression` (bog'liqliklar bilan) avval login va smoke'ni yuritadi.
- Regression ma'lumoti: `data/regression_cases.json` — 858 case, `phase`/`seq` bo'yicha tartiblangan (avval ma'lumotnomalar, keyin ular kerak bo'lgan hujjatlar). `auto=false` (qo'lda qadamli, «Not run», begona yozuvni o'zgartiradigan xavfli, foydalanuvchi boshqaruvi) — Skip, sababi `regression.jsonl` da.
- Natija talqini: oddiy case **Fail** → regressiya (kecha Pass edi) yoki yangi bug; **Bug** tipidagi case **Fail** → ma'lum bug hali bor; **Bug** case **Pass** → bug tuzatilgan. `analyze.py` shularni ajratib `SUMMARY.md` ga yozadi.

## Papka ko'chirilsa
```bash
bash scripts/launchd_install.sh   # 04:00 vazifasini yangi yo'l bilan qayta o'rnatadi
```

## Qo'lda ishga tushirish
```bash
npm run setup                     # faqat login
npm run smoke+regression          # login → smoke → regression (ketma-ket)
npm run regression                # faqat regression (login oldin qilingan bo'lsa)
CASES=TC-SPR-DIV-006,TC-SKL-VAN-008 npm run regression   # tanlangan case'lar
MODULES=Склад TYPES=Smoke,Validatsiya npm run regression # modul / tip bo'yicha
MODULES=Склад npm run health      # bitta modul
npm run access
SCENARIOS=SIM-SKL-IB-003 npm run headed:sim   # bitta ssenariy, brauzerni ko'rib turib
launchctl kickstart -k gui/$(id -u)/uz.smartup.nightly   # to'liq tungi yugurishni hozir
npx playwright show-report ../Tungi_natijalar/<sana>/html
```

## Fayllar
- `config/roles.json` — rollar va loginlar (parol yo'q). `config/expected_access.json` (ixtiyoriy) — `{ "agent": { "/xtrade/a2/...": "DENIED" } }`; farq bo'lsa bug.
- `lib/env.js` — Keychain'dan parol, natija papkasi, `relogin()`. `lib/smt.js` — SmartUp DOM yordamchilari va `test_cases.json` action lug'ati.
- `tests/auth.setup.js`, `health.spec.js` (smoke), `regression.spec.js`, `access.spec.js`, `sim.spec.js`.
- `data/regression_cases.json` — 858 regression case (28.09 test case'lari + 29.09 dagi test-ma'lumot tuzatishlari).
- `data/routes.json` (226 sahifa), `data/sim_scenarios.json` (28.09 dagi tasdiqlangan CRUD case'lardan; o'chirish qadamlari olib tashlangan), `data/known_bugs.json` (100 ta ma'lum bug).
- `scripts/nightly.sh`, `setup_mac.sh`, `add_password.sh`, `analyze.py`, `night_report.py`; `launchd/uz.smartup.nightly.plist`.

## Xavfsizlik
- Parol faqat Keychain'da (`security add-generic-password -s smartup-xtrade`), kodda/logda/hisobotda yo'q. `.auth/*.json` — sessiya cookie'lari: papkani hech kimga yubormang (git'ga qo'shmang).
- Testlar tashqi tizimlarga (WMS, Faktura/Soliq, Telegram, CRPT) yubormaydi, sozlama/huquqni saqlamaydi, begona hujjatni o'chirmaydi. `health` bo'sh formani saqlab ko'radi — agar saqlanib qolsa, bu `empty_save_leaked` bug sifatida yoziladi.
- Mock-server bilan sinalgan (login, qayta login, health, access, sim, analyze). Haqiqiy serverdagi birinchi yugurishda ba'zi selektorlarni moslash kerak bo'lishi mumkin — `npm run headed:sim` bilan ko'ring yoki natijani Claude'ga ko'rsating.
