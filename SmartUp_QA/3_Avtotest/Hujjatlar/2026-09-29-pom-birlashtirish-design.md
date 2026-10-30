# 5 ta avtotest loyihasini yagona POM arxitekturasiga birlashtirish — dizayn

**Sana:** 29.09.2026
**Muallif:** QA (mohir) + Claude
**Holat:** tasdiqlangan (dizayn), implementatsiya rejasi kutilmoqda

---

## 1. Maqsad

Hozir SmartUp xtrade uchun **5 ta alohida avtotest loyihasi** bor. Ularning hech biri to'liq emas,
uchtasi bir daraxtning shoxlari, to'rttasi endi ishlatilmaydigan UI ni testlaydi.

Yakuniy natija — **bitta loyiha**: `3_Avtotest/Avtotest_POM/`, Page Object Model arxitekturasida,
Python + pytest + Playwright da, a2 (yangi Angular) UI ni asosiy nishon qilib oladi, eski
AngularJS formalarni esa avtomatik aniqlanadigan adapter orqali qo'llab-quvvatlaydi.

---

## 2. Hozirgi holat (o'lchangan dalillar, 29.09.2026)

### 2.1 `3_Avtotest/SmartUp_Autotest/` — JavaScript, kecha-bugun yozilgan

| O'lcham | Qiymat |
|---|---|
| Qo'lda yozilgan case (`1_Smoke_2026-09-28/.../test_cases.md`, 198 forma) | 831 noyob ID |
| `data/regression_cases.json` | 858 case — **831 manual ID ning hammasi bor (ID qamrovi 100%)** |
| `auto: true` (haqiqatda bajariladi) | **548 (64%)** |
| `auto: false` (skip) | 310 (36%) |
| Smoke (`health.spec.js`) | 226 route |

**Aniqlangan kamchiliklar:**

1. **245 ta `auto` case da (548 dan 45%) birorta `assert_*` qadami yo'q.** Ular faqat sahifa
   bo'ylab bosib o'tadi; xato oynasi chiqmasa Pass qaytaradi. Haqiqiy tekshiruvli case ~303 ta.
2. **`lib/smt.js` da 5 ta action yozilmagan**, lekin case'larda ishlatiladi:
   `manual` (300 marta), `menu_plus` (7), `assert_download` (3), `assert_no_request` (2),
   `remove_tag` (1). Shundan **3 ta `auto` case** ishga tushishi bilan
   `«...» avtomatlashtirilmagan` xatosi bilan yiqiladi.
3. **Kod hech qachon ishlatilmagan.** `Tungi_natijalar/` bo'sh, `.auth/` yo'q,
   Playwright CLI o'rnatilmagan. 40 563 qatorlik JSON hali bironta ham real brauzerda sinalmagan.
4. POM yo'q: bitta 256 qatorlik `lib/smt.js` action lug'ati + JSON.

### 2.2 Eski 4 loyiha — Python/pytest

| Loyiha | Mazmuni | `base_page.py` | Oxirgi commit |
|---|---|---|---|
| `SmartupAuto_repo` | **Smoke eng boy** — 69 fayl, 57 test, 48 `run_*` flow | **791 qator (eng yangi)** | 18.07.2026 |
| `smartup_reg` | **Regression eng boy** — 88 test: 23 bug_fix (5 sprint), 5 KPI, 5 restriction, 30 test_setup, 7 gap_pending | 715 | 19.07.2026 |
| `Smartupauto` | Ikkalasining eski birlashgan nusxasi, 82 test | 715 (`smartup_reg` bilan **aynan bir xil**) | 19.07.2026 |
| `playwright_original` | Eng kichik, 4 test; noyobi: `form_opening_check` (226 forma), `configs/` (ko'p-server) | 29 | 18.07.2026 |

Git tarixi nasabni tasdiqlaydi: `SmartupAuto_repo` da
`chore: remove regression suite, extracted to smartup_reg` commiti bor. Ya'ni
`SmartupAuto_repo` → ajralib `smartup_reg`, `Smartupauto` esa ikkalasining oldingi snapshoti.

**Ikki muhim fakt:**

1. **Hech biri POM emas.** `pages/` papkasi faqat `playwright_original` da bor va u 3 ta mitti
   klass (jami 61 qator). Qolgan uchtasida arxitektura — 700–790 qatorlik `BasePage`
   "xudo-obyekti" + `flow_*.py` funksiyalar + testlar ichidagi `run_*()` funksiyalari.
   Bu POM emas, *helper-driven* uslub.

2. **Eski 4 loyiha va `3_Avtotest` boshqa-boshqa ilovani testlaydi:**

   ```
   playwright_original · smartup_reg · Smartupauto · SmartupAuto_repo
      → b-grid · .tbl-row · b-grid-controller · b-input · ng-model · #biruniConfirm
      → a2 selektori: 0 ta

   3_Avtotest/SmartUp_Autotest
      → smt-data-row · smt-cell-header · .cdk-overlay-pane · [role=dialog] · /xtrade/a2/
      → eski UI selektori: 0 ta
   ```

   Umumiy selektor **nol**. Demak "ko'chirish" — nusxa-ko'chirish emas, **qayta yozish**.
   Ko'chadigan narsa: biznes-mantiq (qaysi forma, qanday ketma-ketlik, nimani tekshirish).

### 2.3 Takrorlanishni chiqarib tashlagandagi haqiqiy hajm

- **~150 noyob test funksiyasi** (109 noyob fayl nomi)
- **~100 qayta ishlatiladigan `run_*` flow**
- **858 JSON case** (548 auto)

---

## 3. Qabul qilingan qarorlar

| № | Savol | Qaror | Sabab |
|---|---|---|---|
| 1 | Qaysi UI? | **Asosiy — a2.** Eski AngularJS formalar (masalan order formasi — «Заказы») kam, lekin bor; ular ham testlanadi | Foydalanuvchi tasdiqladi: "ba'zi formalar eski angularjs da qolgan… bunday formalar juda kam" |
| 2 | Stack? | **Python + pytest + Playwright** | 4 loyihadagi ~150 test mantiqi, Allure, Telegram bot, CI, conftest fixture'lari saqlanadi. JSON (858 case) tilga bog'liq emas — Python runner ham o'qiydi |
| 3 | 858 JSON case? | **JSON qoladi, ijrochi POM bo'ladi** | QA JSON ni oson tahrirlaydi; 858 tani qo'lda POM testi qilib yozish ~3 hafta ortiqcha ish beradi, foydasi esa yo'q |
| 4 | Migratsiya tartibi? | **A yo'li: avval dalil (Faza 0), keyin poydevor, keyin port** | Mavjud kod hech qachon ishlamagan; POM ni tekshirilmagan taxminlar ustiga qurish ikki qatlamni birdan qayta ishlash xatarini beradi |
| 5 | Manzil? | `3_Avtotest/Avtotest_POM/` | CLAUDE.md 1-qoida: avtotest faqat `3_Avtotest/` da |
| 6 | Eski loyihalar? | Migratsiya tugagach `3_Avtotest/_arxiv/` ga ko'chiriladi | GitHub repolari o'chmaydi, faqat mahalliy papkalar ko'chadi |
| 7 | Nomlash tili? | Kod, fayl va hujjatlarda **`order`** (`zakaz` emas). Umuman: modul/forma nomlari inglizcha transliteratsiyada | "zakaz" og'zaki nutqda ishlatiladi, kodda emas |

---

## 4. Arxitektura

```
3_Avtotest/Avtotest_POM/
├── conftest.py              fixture: page, code, save_data/load_data, soft_assert, logger, ui
├── pytest.ini               markerlar: smoke, regression, bug, json_driven, module(...)
├── requirements.txt
├── .env.example
│
├── pages/
│   ├── base_page.py         ~100 qator: open, heading, xato oynasi, loader kutish
│   ├── ui/                  ◀── UI ADAPTER QATLAMI
│   │   ├── driver.py            UiDriver protokoli (umumiy interfeys)
│   │   ├── a2.py                yangi Angular selektorlari
│   │   ├── biruni.py            eski AngularJS selektorlari
│   │   └── detect.py            sahifani ochgandan keyin qaysi drayver kerakligini aniqlaydi
│   ├── components/
│   │   ├── grid.py          click_row, row_action, columns, search, expand, settings
│   │   ├── form.py          field, fill, fill_date, select, multiselect, toggle, radio, save
│   │   ├── dialog.py        confirm, close, error_text, is_error
│   │   ├── menu.py          nav, menu_plus, filial almashtirish
│   │   └── report.py        filtr, generatsiya, yuklab olish
│   ├── modules/             forma-darajali sahifalar (9 modul, 198 forma)
│   │   ├── sklad/ · torg_marketing/ · savdo/ · spravochnik/ · oborudovanie/
│   │   ├── proizvodstvo/ · kadry/ · finansy/ · glavnoe/
│   └── factory.py           PageFactory: forma nomi / route → Page klassi
│
├── tests/
│   ├── smoke/               ◀ SmartupAuto_repo + playwright_original/form_opening_check
│   ├── regression/          ◀ smartup_reg + Smartupauto noyoblari
│   │   ├── bug_fix/sprint_56..60/
│   │   ├── kpi/ · restrictions/ · setup/ · gap_pending/
│   └── json_driven/
│       ├── test_cases.py    858 case parametrize
│       └── actions.py       action lug'ati → POM chaqiruvlari
│
├── data/     routes.json · regression_cases.json · known_bugs.json
│             sim_scenarios.json · run_order.json · roles.json
├── utils/    allure_helper.py · telegram.py · soft_assert.py · logger.py · run_logger.py
├── scripts/  nightly.sh · analyze.py · night_report.py · setup_mac.sh
└── launchd/  uz.smartup.nightly.plist
```

### 4.1 UI adapter qatlami — eski formalar qanday hal bo'ladi

`UiDriver` — protokol (interfeys). Ikki implementatsiyasi bor:

| Tushuncha | `a2.py` (yangi) | `biruni.py` (eski) |
|---|---|---|
| Asosiy konteyner | `page.locator("main").last` | `b-page` |
| Grid qatori | `.smt-data-row` | `b-grid .tbl-row` |
| Ustun sarlavhasi | `smt-cell-header` | `b-grid-controller` ichidagi sarlavhalar |
| Qidiruv | grid controller tugmasi | `input[ng-model="o.searchValue"]` |
| Maydon konteyneri | `label` → ancestor (input/select/switch bor) | `b-input:has(input[ng-model="..."])` |
| Variant paneli | `.cdk-overlay-pane` | `b-input` ichidagi dropdown |
| Dialog | `[role=dialog]` | `#biruniConfirm`, `.modal.show` |

**Aniqlash avtomatik.** Sahifa ochilgandan keyin `detect.py` DOM ga qaraydi:
`smt-data-row` yoki `smt-cell-header` topilsa → `A2Driver`, `b-grid` yoki `b-page` topilsa
→ `BiruniDriver`. Natija sahifa obyekti umrida keshlanadi.

Test kodi ikkala holatda ham **bir xil**:

```python
order = OrderPage(page).open()
order.grid.click_row("QA-ORD-1")      # drayver o'zi qaysi selektorni ishlatishni biladi
order.form.fill("Клиент", "QA mijoz")
order.save().expect_saved()
```

Eski formalar kam bo'lgani uchun `biruni.py` kichik qoladi (~150 qator) — u
`smartup_reg/utils/base_page.py` dan faqat haqiqatan kerakli qismlarni oladi
(`grid_row`, `grid_controller`, `confirm_biruni`, `b_input_by_label`, `select_b_input`).

### 4.2 Komponentlar — mas'uliyat chegaralari

Har bir komponent bitta ishni qiladi va faqat `UiDriver` orqali DOM ga tegadi.
Hech bir komponent boshqasining ichki holatini bilmaydi.

| Komponent | Nima qiladi | Nimaga bog'liq |
|---|---|---|
| `Grid` | ro'yxat: qator topish/bosish, amal tugmalari, ustunlar, qidiruv, kengaytirish, sozlamalar | `UiDriver` |
| `Form` | maydonlar: yozish, sana, tanlash, ko'p tanlash, switch, radio, saqlash, validatsiya xatolari | `UiDriver` |
| `Dialog` | tasdiq/xato oynalari: matnni o'qish, tugma bosish, yopish | `UiDriver` |
| `Menu` | yuqori menyu orqali o'tish, menyu yonidagi `+`, filial almashtirish | `UiDriver` |
| `Report` | hisobot formalari: filtr to'ldirish, generatsiya, yuklab olish | `UiDriver`, `Form` |

`BasePage` — 100 qatordan oshmaydi: `open()`, `heading()`, `wait_for_loader()`,
`expect_no_error()`, va komponentlarni yig'ib beradi (`self.grid`, `self.form`, …).
Hozirgi 791 qatorlik `BasePage` shu komponentlarga bo'linadi — bu dizaynning asosiy yutug'i.

### 4.3 Reliz-barqarorlik: ALIAS qatlami

29.09 relizida tugma nomlari o'zgargan: `Просмотреть`→`Просмотр`, `Создать`→`Добавить`.
`smt.js` da buning uchun `ALIAS` xaritasi bor. POM da bu `components/` darajasiga
ko'tariladi: `Grid.row_action("Просмотреть")` topilmasa muqobil nomni sinaydi.
Aks holda har relizda yuzlab case yiqiladi.

### 4.4 JSON-driven ijrochi

`tests/json_driven/actions.py` — `lib/smt.js` ning A-lug'ati POM chaqiruvlariga o'tkazilgan nusxasi:

```python
# tests/json_driven/test_cases.py
@pytest.mark.parametrize("case", load_cases(), ids=case_id)
def test_case(case, page, soft_assert):
    if not case.auto:
        pytest.skip(case.skip_reason)
    ctx = PageFactory(page).for_form(case.module, case.form)
    for i, step in enumerate(case.steps, 1):
        with allure.step(f"{i}. {step.description}"):
            ACTIONS[step.action](ctx, step)

# tests/json_driven/actions.py
def row_click(ctx, s):  ctx.grid.click_row(s.target)
def fill(ctx, s):       ctx.form.field(s.target).fill(s.value)
def confirm(ctx, s):    ctx.dialog.confirm(s.target, s.value)
def assert_columns(ctx, s): ctx.grid.expect_columns(*split(s.value))
```

`PageFactory` forma nomi/route bo'yicha aniq Page klassini qaytaradi; klass topilmasa
komponentlardan yig'ilgan umumiy `GenericPage` beradi. Shu tufayli 198 ta Page klassini
birdaniga yozish shart emas — JSON case'lar `GenericPage` da ham ishlaydi, aniq klasslar
esa qo'lda yozilgan testlar uchun bosqichma-bosqich qo'shiladi.

---

## 5. Migratsiya bosqichlari

### Faza 0 — Dalil yig'ish (1–2 kun)

Maqsad: POM ni qurishdan oldin mavjud a2 taxminlari to'g'riligini bilish.

- `3_Avtotest/SmartUp_Autotest/` da `npm i` + `npx playwright install chromium`
- Keychain orqali login (`auth.setup.js`) — parol kiritilmaydi
- `health` (226 route) bir marta yuritiladi → qaysi route ochiladi, qaysi 5xx beradi
- `regression` (548 auto case) bir marta yuritiladi → qaysi action/selektor ishlaydi
- Natija: `3_Avtotest/Tungi_natijalar/<sana>/` + baseline hisobot

**Chiqish mezoni:** har bir `smt.js` selektori uchun "ishlaydi / ishlamaydi / noma'lum"
belgisi bor jadval. Shu jadval `pages/ui/a2.py` ning asosi bo'ladi.

### Faza 1 — Poydevor (3–5 kun)

- Loyiha skeleti, `pytest.ini`, `requirements.txt`, `.env.example`
- `conftest.py`: `page`, `code`, `save_data`/`load_data`, `soft_assert`, `logger`, `ui` fixture'lari
  (asos: `smartup_reg/tests/regression/conftest.py`, 646 qator → ~250 qatorga qisqartiriladi)
- `pages/ui/`: `driver.py`, `a2.py` (Faza 0 jadvalidan), `biruni.py`, `detect.py`
- `pages/components/`: `grid.py`, `form.py`, `dialog.py`, `menu.py`, `report.py`
- `pages/base_page.py`, `pages/factory.py` + `GenericPage`
- `utils/` port: `soft_assert.py`, `logger.py`, `run_logger.py`, `telegram.py`, `allure_helper.py`
- `data/` ko'chirish: `routes.json`, `regression_cases.json`, `known_bugs.json`,
  `sim_scenarios.json`, `run_order.json`, `roles.json`

**Chiqish mezoni:** bitta qo'lda yozilgan smoke testi (`Организации` ro'yxati ochiladi va
ustunlar tekshiriladi) a2 da yashil o'tadi; bitta eski-UI testi (order formasi)
`BiruniDriver` bilan yashil o'tadi.

### Faza 2 — JSON-driven POM ustida (5–8 kun)

- `tests/json_driven/actions.py`: 28 ta mavjud action → POM chaqiruvlari
- **Yetishmayotgan 5 ta action yoziladi:** `menu_plus`, `remove_tag`, `assert_download`,
  `assert_no_request`; `manual` → tushunarli sabab bilan `pytest.skip`
- **Assert'siz 245 case tuzatiladi:** qo'lda yozilgan `test_cases.md` dagi `expected`
  matnidan `assert_text` / `assert_columns` / `assert_row` qadamlari generatsiya qilinadi;
  generatsiya natijasi `Avtotest_POM/data/regression_cases.json` ga yoziladi (eski
  `SmartUp_Autotest/data/` ga tegilmaydi) va qo'lda ko'rib chiqiladi
- `run_order.json` tartibi saqlanadi (ma'lumotnoma → hujjat bog'liqligi)

**Chiqish mezoni:** 548 auto case yuritiladi; Faza 0 baseline'iga nisbatan Fail soni
oshmagan; assert'li case ulushi 55% dan **100%** ga chiqqan.

### Faza 3 — Smoke port (5–7 kun)

Manba: `SmartupAuto_repo/tests/smoke/` (57 test + 48 flow) va
`playwright_original/form_opening_check/` (226 forma ochilishi).

- `test_setup/` zanjiri: company → filial → legal/natural person → user → role → room →
  price_type → payment_type → product → license (19 fayl)
- `test_groups/` A/B/C/report (18 fayl): order, shartnoma, aksiya, integratsiya hisobotlari
- `test_life_cycle/`: `test_a2_admin_forms.py`, `test_a2_new_forms.py`, `test_order.py`,
  `init_balance.py` — **bular allaqachon a2 ga qaratilgan, port eng oson shular**
- `Smartupauto` dan noyob: `flows/flow_inventory/flow_init_balance.py`
- `form_opening_check` → `tests/smoke/test_form_opening.py`, ro'yxat `data/routes.json` dan olinadi
- `pytest.ini` markerlari saqlanadi: `user_setup`, `smoke_group(name)`

**Chiqish mezoni:** smoke to'plami boshidan oxirigacha bir sessiyada o'tadi;
setup zanjiri yiqilsa keyingi guruhlar `skip` bo'ladi (hozirgi xatti-harakat saqlanadi).

### Faza 4 — Regression port (8–12 kun)

Manba: `smartup_reg/tests/regression/` (88 test).

| Bo'lim | Fayl | Izoh |
|---|---|---|
| `bug_fix/` | 23 (sprint 56–60) | Har biri Jira raqamiga bog'langan; `known_bugs.json` bilan bog'lanadi |
| `kpi/` | 5 | KPI dashboard, shablon, mijoz/tashkilot/ish zonasi bo'yicha |
| `restrictions/` | 5 | Qarz summasi, mijoz xarakteristikasi, konsignatsiya sanasi, oylik summa, rol |
| `test_setup/` | 30 | Kassa, mijoz, shartnoma, valyuta, kirim, chiqim, inventarizatsiya, xarid… |
| `gap_pending/` | 7 | USD narx turi, avans tahriri, min summa validatsiyasi, sub-filial… |
| `Smartupauto` noyoblari | 3 | `test_license.py`, `test_first_order_creation.py`, `test_check_forms_opening.py` |

**Chiqish mezoni:** har bir port qilingan test a2 da (yoki kerak bo'lsa eski UI da) yashil
yoki `known_bugs.json` da ro'yxatdan o'tgan ma'lum bug sababli qizil.

### Faza 5 — Yakun (2–3 kun)

- `scripts/nightly.sh` Python ga moslashtiriladi (setup → smoke → regression → access → sim)
- `launchd/uz.smartup.nightly.plist` yangi manzilga
- Telegram hisoboti (`utils/telegram.py` + `scripts/night_report.py`)
- `scripts/analyze.py` — natijalarni tahlil qilib `candidates.json` + `SUMMARY.md`
- Allure hisoboti
- Eski 5 loyiha → `3_Avtotest/_arxiv/`
- `README.md` va ildizdagi `CLAUDE.md` yangilanadi

---

## 6. Xato bilan ishlash

| Holat | Xatti-harakat |
|---|---|
| Kutilmagan xato oynasi (`Ошибка`, `ORA-`, `violated`) | Test darhol Fail, screenshot + tarmoq so'rovlari yoziladi |
| Kutilgan xato (salbiy case, `expected` da xato kodi bor) | Kod mos kelsa Pass; kod boshqa bo'lsa Fail |
| Ma'lum bug (`known_bugs.json`) | Fail bo'ladi, lekin `xfail` markeri bilan — hisobotda alohida ajratiladi |
| Sessiya tugagan (login sahifasi) | Avtomatik qayta login (`relogin`), test qaytadan boshlanadi |
| Selektor topilmadi | ALIAS muqobil nomi sinaladi; u ham topilmasa Fail + DOM snapshot |
| Soft assert | `soft_assert` fixture — bir testda bir nechta tekshiruv yig'iladi, oxirida birga chiqadi |

---

## 7. Muvaffaqiyat mezonlari

1. **Bitta loyiha:** `3_Avtotest/Avtotest_POM/`; qolgan 5 tasi `_arxiv/` da.
2. **`BasePage` 100 qatordan oshmaydi**, mantiq 5 ta komponentga bo'lingan.
3. **Barcha 831 qo'lda yozilgan case** JSON-driven to'plamda ID bo'yicha mavjud;
   `auto` case'larning **100% ida kamida bitta assert** bor (hozir 55%).
4. **Eski UI formalar** (order va sh.k.) bir xil test kodi bilan, adapter orqali ishlaydi.
5. **~150 noyob legacy test** port qilingan, har biri a2 da yashil yoki ma'lum bug bilan `xfail`.
6. **Tungi ish zanjiri** `launchd` orqali o'zi yuriladi, ertalab Telegram'ga hisobot keladi.
7. Yangi forma qo'shish = 1 ta Page klass + JSON case; `BasePage` ga tegilmaydi.

---

## 8. Qamrab olinmaydi (non-goals)

- **310 ta `auto: false` case** to'liq avtomatlashtirilmaydi. Ular "qo'lda qadam bor" (167),
  "xavfli/qo'lda" (57), "begona yozuvni o'zgartiradi" (28) sabablari bilan qo'lda qoladi.
  Avtomatlashtirish natijasida bu son ~200 gacha tushishi kutiladi, nolga emas.
- **Tashqi tizimlar** (WMS, Soliq, Faktura, Telegram biznes-oqimi, CRPT) ga yuborish —
  CLAUDE.md 4-qoida bo'yicha taqiqlangan.
- **Foydalanuvchi/huquq/sozlamalarni o'zgartirish** — taqiqlangan; shu sababli
  4 ta case ("foydalanuvchi boshqaruvi") doimo skip qoladi.
- **Mobil ilova** testlari.
- **Yuklama (performance) testlari.**

---

## 9. Xatarlar

| Xatar | Ta'sir | Kamaytirish |
|---|---|---|
| `3_Avtotest` kodi hali bironta ham real brauzerda ishlamagan | POM noto'g'ri taxmin ustiga qurilishi mumkin | **Faza 0** — avval yuritib, selektor jadvalini olish |
| a2 tez-tez o'zgaradi (29.09 relizda tugma nomlari almashgan) | Har relizda yuzlab case yiqiladi | ALIAS qatlami `components/` darajasida; selektorlar bitta joyda (`ui/a2.py`) |
| 245 case ga assert generatsiya qilish — `expected` matni erkin shaklda | Noto'g'ri assert yolg'on Fail beradi | Generatsiya natijasi qo'lda ko'rib chiqiladi; shubhali hollarda `assert_text` (yumshoq) ishlatiladi |
| Legacy testlar eski UI ga yozilgan, a2 da forma tuzilishi boshqacha bo'lishi mumkin | Port qilingan test mantiqan mos kelmasligi mumkin | Har bir port qilingan test bir marta qo'lda ko'zdan kechiriladi; forma o'zgargan bo'lsa case yangilanadi |
| Parol | CLAUDE.md 4-qoida: parol kiritilmaydi | Login Keychain orqali; parol kodda ham, logda ham ko'rinmaydi |
| Tungi ishlash Mac ga bog'liq (tarmoq allowlist) | CI da ishlamaydi | Hozirgi yechim saqlanadi: `launchd` + mahalliy Mac; natijalar fayl orqali tahlil qilinadi |

---

## 10. Taxminiy hajm

| Faza | Kun |
|---|---|
| 0 — Dalil | 1–2 |
| 1 — Poydevor | 3–5 |
| 2 — JSON-driven POM ustida | 5–8 |
| 3 — Smoke port | 5–7 |
| 4 — Regression port | 8–12 |
| 5 — Yakun | 2–3 |
| **JAMI** | **24–37 ish kuni** |

Baholar taxminiy: Faza 0 natijasi (qancha selektor ishlashi) Faza 1–2 ni sezilarli
o'zgartirishi mumkin.

Hajmi katta bo'lgani uchun implementatsiya rejasi **bitta katta reja emas, har faza uchun
alohida reja** sifatida yoziladi: har fazaning chiqish mezoni bajarilgach keyingisi
rejalashtiriladi. Faza 0 natijasi Faza 1 rejasining kirish ma'lumoti bo'ladi.

---

## 11. Manbalar xaritasi — nima qayerdan keladi

| Yangi joy | Manba |
|---|---|
| `pages/ui/a2.py` | `3_Avtotest/SmartUp_Autotest/lib/smt.js` + Faza 0 selektor jadvali |
| `pages/ui/biruni.py` | `smartup_reg/utils/base_page.py` (grid_row, grid_controller, confirm_biruni, b_input_by_label) |
| `pages/components/*` | `SmartupAuto_repo/utils/base_page.py` (791 q.) bo'lib tashlanadi + `smt.js` A-lug'ati |
| `pages/base_page.py` | `SmartupAuto_repo/utils/base_page.py` dan navigate_to/expect_page/switch_filial |
| `conftest.py` | `smartup_reg/tests/regression/conftest.py` + `SmartupAuto_repo/tests/smoke/conftest.py` |
| `tests/smoke/` | `SmartupAuto_repo/tests/smoke/` + `Smartupauto` flow_inventory + `playwright_original/form_opening_check` |
| `tests/regression/` | `smartup_reg/tests/regression/` + `Smartupauto` noyoblari |
| `tests/json_driven/` | `3_Avtotest/SmartUp_Autotest/tests/regression.spec.js` + `lib/smt.js` |
| `data/` | `3_Avtotest/SmartUp_Autotest/data/` + `Ketma-ketlik/run_order.json` + `config/roles.json` |
| `utils/telegram.py` | `playwright_original/utils/telegram_reporter.py` (187 q., eng to'lig'i) + `SmartupAuto_repo/utils/telegram_bot.py` (201 q.) |
| `utils/soft_assert.py` | `Smartupauto/utils/soft_assert.py` (113 q. — eng to'lig'i) |
| `scripts/` | `3_Avtotest/SmartUp_Autotest/scripts/` + `smartup_reg/scripts/analyze_test_result.py` |
