# Claude Code uchun prompt — E2E «Xarid → Sotuv → Qaytarish → To'lov» avtotesti (Playwright MCP + Python POM)

> Quyidagi matnni Claude Code'ga (PyCharm, ishchi papka `3_Avtotest/Avtotest_POM`) to'liq joylang.

---

Sen SmartUp xtrade uchun avtotest yozuvchi QA muhandisisan. Javoblar o'zbek tilida, qisqa.

## 0. Avval o'qi (o'zgartirma)
1. `../CLAUDE.md` — qoidalar (maxfiy ma'lumot faqat `../.env`, tashqi tizimlarga yuborish taqiqlangan va h.k.).
2. `README.md` va `../Hujjatlar/2026-09-29-pom-birlashtirish-design.md` — POM tuzilishi: `UiDriver` (a2 / biruni adapterlari), `pages/components/*`, `utils/SoftAssert`, `TestLogger`.
3. **Manual test case'lar (asosiy manba):** `../../Regression/Test_caselar/10_E2E/01_Xarid_sotuv_tolov_sikli/test_cases.md` (TC-E2E-01…18). Har qadam va kutilgan natija shu fayldan olinadi. Faylni o'zgartirma.
4. Mavjud lokator yozuvlari: `../Lokatorlar/01_Склад.md`, `03_Продажа.md`, `04_Справочники.md`, `08_Финансы.md`.

## 1. Maqsad
TC-E2E-01…17 ni bitta ketma-ket (ordered) jonli test to'plami qilib avtomatlashtir. Bu **smoke emas, regression**: har formada barcha input, select, switch, checkbox, radio, tab, ichki grid (qator qo'shish/o'chirish), dialog tugmalari (Создать / Создать и закрыть / Закрыть), «Назад/Закрыть/Далее» ishlashi tekshiriladi; so'ng hujjatlar zanjiri oxirigacha o'tkaziladi va har qadamda qoldiq, summa va qarz assert qilinadi.

## 2. Ish tartibi (bosqichma-bosqich, har bosqich oxirida menga qisqa hisobot ber)

**Bosqich A — Lokatorlarni Playwright MCP bilan topish (faqat o'qish/ko'rish)**

- Playwright MCP bilan `https://app3.greenwhite.uz/xtrade/a2/` ni och. Login: men o'zim kiraman yoki sessiya `../SmartUp_Autotest/.auth/admin.json` dan; parolni hech qayerga yozma.
- Har forma uchun (test_cases.md dagi yo'llar): `browser_snapshot` bilan accessibility daraxtini ol, har maydon uchun **barqaror lokator** tanla. Afzallik tartibi:
    1. `get_by_role(..., name=...)` / `get_by_label("Название")` (yorliq matni + `*` olib tashlangan),
    2. yorliq konteyneri orqali: `label:has-text("…") >> xpath=..` ichidagi `smt-input input` / `smt-select-trigger` / `textarea` / `[role=switch]` / `[role=checkbox]`,
    3. matn bo'yicha tugma: `main button:has-text("Сохранить")`.
    - Koordinata, `nth()` indeks va dinamik Angular atributlar (`_ngcontent-*`, `ng-tns-*`) **ishlatma**.
- Formada saqlash/provodka tugmasini bu bosqichda **bosma**. Wizard'larni keyingi qadamga o'tkazish uchun to'ldirish mumkin, lekin oxirida «Закрыть/ЗАКРЫТЬ» bilan saqlamasdan chiq.
- Natija: `../Lokatorlar/10_E2E.md` — har forma bo'limi: maydon | lokator | turi (inp/sel/msel/sw/chk/radio/date/txt) | majburiy | izoh. Mavjud lokator lug'atiga mos yoz.
- Ma'lum xususiyatlar (formalarni o'rganishda aniqlangan):
    - a2: grid qatorlari `main .smt-data-row`, sarlavhalar `.smt-grid-header > *`, dialoglar `.cdk-overlay-container [role=dialog]`, tanlov `smt-select-trigger` → yozish → variant `.cdk-overlay-pane` dan; tasdiq oynasi «Да».
    - a2 formalarida pastki tablar oddiy `button` (role=tab emas); tab almashganda sahifa balandligi o'zgaradi — tabni har safar matn bo'yicha qayta top.
    - Юридическое лицо «Характеристики» tabida **«qa xyu» majburiy**; Физическое лицо'da «Группа», «Категория» majburiy.
    - Eski UI (Заказ на закупку, Заказы, Взаиморасчеты с клиентами, Архив заказов): URL'da sessiya tokeni bor — **faqat menyu orqali o'tiladi** (README). Eski UI'da autocomplete: maydonni bosish → `type()` (keyboard, `fill` emas) → ro'yxatdan variant matn bo'yicha. Smoke'da «avtomatlashtirilgan klaviatura kiritish ishlamadi» deb yozilgan — `press_sequentially` + `blur` bilan sinab ko'r; ishlamasa sababini yoz va to'xta.
    - Заказы ro'yxatida status: qatorni checkbox bilan belgilash → «ИЗМЕНИТЬ СТАТУС ▾» → variant.

**Bosqich B — Page Object'lar**

- `pages/e2e/` ichida har forma uchun bitta klass (masalan `TmcFormPage`, `LegalPersonFormPage`, `PurchaseOrderWizard`, `SalesOrderWizard`, `ReturnWizard`, `CashinFormPage`, `StockBalancePage`, `ClientOffsetPage`). Mavjud `pages/components/*` (form, grid, tabs, dialog, menu, buttons) va `UiDriver` dan foydalan; yangi umumiy usul kerak bo'lsa komponentga qo'sh va `tests/test_ui_driver.py` / komponent testlarida selektorini mixla (README talabi).
- Har klassda: `open()`, `fill_all(data)`, `check_required_validation()`, `check_tabs()`, `save()`, `open_view(name)`, `read_values()`.
- `except Exception: pass` va jimgina yutish **taqiqlangan**.

**Bosqich C — Test ma'lumotlari**

- `data/e2e_xarid_sotuv.json`: test_cases.md dagi jadvallardagi barcha qiymatlar. Nomlarda `<DDMM>` → yugurish sanasi (masalan `QA-E2E-TMS-3010`). Hamma nom `QA-E2E-` bilan boshlanadi.
- Raqamlar: ТМЦ narxi sotish 15 000 / xarid 10 000; запрос 100 dona; закупка 1 000 000; buyurtma 30 dona = 450 000; qaytarish 5 dona = 75 000; to'lovlar 200 000 + 175 000. Kutilgan qoldiq: 100 → 70 → 75; mijoz qarzi 450 000 → 375 000 → 175 000 → 0; ta'minotchi qarzi +1 000 000.

**Bosqich D — Testlar**

- `tests/live/test_e2e_xarid_sotuv.py`, marker `@pytest.mark.live` va `@pytest.mark.regression`. Testlar ketma-ket (TC-E2E-01 → 17), umumiy holat (yaratilgan ID'lar, raqamlar) session fixture'da va `../Tungi_natijalar/<sana>_pom/e2e_state.json` ga yoziladi — yiqilgan joydan `--e2e-from TC-E2E-12` bilan davom ettirish mumkin bo'lsin.
- Har case boshida boshlang'ich qiymatni (qoldiq/qarz) o'qib ol va natijani **farq** sifatida assert qil (bazadagi boshqa ma'lumotga bog'lanma).
- Har saqlashda `page.wait_for_response(lambda r: ':save' in r.url or '$save' in r.url)` va status 200; «Ошибка» dialogi (`[role=dialog]` ichida «Ошибка» / «URL: /xtrade/b/…») chiqsa test darhol yiqilsin, skrinshot + matn logga.
- Har formada «UMUMIY» tekshiruvlar (test_cases.md boshida 1–7): majburiy maydon validatsiyasi, select tozalash, switch/checkbox holati, tablar, Закрыть saqlamasligi (ro'yxat hisoblagichi o'zgarmasligi), Просмотр'da har kiritilgan qiymat, Изменить → bitta maydon o'zgarishi.
- Konsol xatolari va 4xx/5xx so'rovlarni yig'ib, case oxirida SoftAssert bilan tekshir; `i18n/**.json` 404 ni alohida qayd et.
- Fayl yuklash maydonlari uchun `data/files/qa.png`, `qa.pdf` (o'zing yaratib qo'y, kichik).

**Bosqich E — Tozalash**

- `tests/live/test_e2e_cleanup.py` (alohida, faqat `--e2e-cleanup` bilan): faqat `e2e_state.json` dagi `QA-E2E-` yozuvlari, teskari tartibda (TC-E2E-18). O'chirib bo'lmaganlarini «Неактивный» qil va ro'yxatini chiqar.

## 3. Qat'iy cheklovlar
- Bosilmaydi: ИНН/ПНФЛ yonidagi «Поиск», «Синхронизировать наличие маркировки», Faktura/Soliq/WMS/CRPT/Telegram'ga yuborish, «Группа маркированных товаров» to'ldirilmaydi.
- Boshqa foydalanuvchilarning hujjatlari va sozlamalar/huquqlar o'zgartirilmaydi. Faqat `QA-E2E-` yozuvlari yaratiladi/o'chiriladi.
- Tugma bosish va qiymat kiritish faqat Playwright amallari bilan (`click`, `fill`, `press_sequentially`), `page.evaluate` bilan DOM'ni o'zgartirish yoki JS click — yo'q (JS faqat o'qish uchun).
- Parol/token kod, log, commit, hujjatga yozilmaydi.
- `../../_Claude/`, `../../Smoke/`, `../../Regression/` papkalariga yozma (faqat o'qi).

## 4. To'xtab, menga yozish kerak bo'lgan holatlar
- Administrator buyurtmani Отгружен/Доставлен/Архив ga o'tkaza olmasa («Проведение транзакции администратором невозможно…») — TC-E2E-13 dan keyingilarni `skip(reason="BLOCKED: admin")` qil va menga boshqa foydalanuvchi kerakligini ayt.
- Kutilgan natija test_cases.md dagidan farq qilsa — testni o'zgartirib moslashtirma; yiqilgan holicha qoldir, farqni (kutilgan / haqiqiy / skrinshot) hisobotga yoz. Bu bug yoki hujjatdagi xato ekanini men hal qilaman.
- test_cases.md oxiridagi «Ochiq savollar» 1–5 ga birinchi yugurishda javob topilsa — hisobotga yoz.
- Bir lokator 3 marta urinishda topilmasa.

## 5. Yakuniy natija
1. `../Lokatorlar/10_E2E.md`
2. `pages/e2e/*.py`, `data/e2e_xarid_sotuv.json`, `tests/live/test_e2e_xarid_sotuv.py`, `tests/live/test_e2e_cleanup.py` (+ komponentlarga qo'shimchalar va ularning brauzersiz testlari).
3. Brauzersiz testlar yashil: `PYTHONDONTWRITEBYTECODE=1 pytest`.
4. Bitta jonli yugurish: `PYTHONDONTWRITEBYTECODE=1 pytest tests/live/test_e2e_xarid_sotuv.py --live` — natija `../Tungi_natijalar/<sana>_pom/`.
5. Qisqa hisobot: har TC — Pass/Fail/Blocked, yiqilganlar sababi, ochiq savollarga javoblar, yaratilgan QA-E2E yozuvlar ro'yxati.

## 6. 30.10.2026 qo'lda yugurishdan aniqlanganlar (testni shunga moslab yoz)
- Admin (mohir@xan) buyurtmani barcha statuslarga o'tkaza oladi — «BLOCKED: admin» skip'i kerak emas, lekin tekshiruv qolsin.
- ТМЦ kartochkasidagi «Поставщики» ga QA ta'minotchini qo'shish SHART (TC-E2E-05, 6-qadam), aks holda «Заказ на закупку» qatorida ta'minotchi chiqmaydi.
- «Сохранить в качестве поставщика» / «Клиент» checkbox'lari Поставщик/Клиентни avtomatik yaratadi — TC-E2E-05/07 da yangi yaratma, mavjudini tekshir.
- Sotuv buyurtmasida «Дата отгрузки» = bugun bo'lsin (standart +2 kun → Архив'da «A02-16-049»).
- Buyurtma ТМЦ qidiruvida defisli so'rov ishlamaydi (BUG-183) — ТМЦ ni «TMS»/«E2E» kabi defissiz qism bilan qidir, test esa «QA-E2E» qidiruvini alohida assert qilib yiqilsin.
- Miqdor katagi qoldiqdan katta qiymatni jim qisqartiradi (BUG-185) — kiritilgan qiymatni o'qib assert qil.
- Qisman qaytarish: Доставлен buyurtma qatoridagi «Отказ» → `anor/mdeal/order/return?deal_id=<ID>` («Возврат» ustuni). a2 «Возвраты → ИД заказа» Доставлен buyurtmani ko'rsatmaydi.
- Buyurtma qator amallarida «Faktura.uz», «Фискализация» — hech qachon bosilmasin.
- «Изменить статус» bosilganda har safar «Status» maslahat oynasi chiqadi — birinchi bosish uni yopadi; «Больше не показывать» bosilmaydi (sozlama).
- Eski UI «Взаиморасчеты с клиентами» — qiymatni o'qishdan oldin sahifani to'liq qayta yukla (reload), aks holda eski ma'lumot.
- Qarz «Заказ» ustunidan «Задолженность»ga Архивда o'tadi; arxivdan keyin 375 000, to'lovlardan keyin mijoz ro'yxatdan chiqadi (0).
- «Оплата от клиента»: «Наличные деньги» tanlanganda «Касса *» chiqadi; «Провести»dan keyin forma ochiq qoladi va pastki jadvalda to'lov ko'rinadi; «Тип оплаты» ro'yxati birinchi ochilishda osilishi mumkin — matn yozib qayta yukla.
- a2 create formalari to'g'ridan URL bilan ochilsa saqlangach dashboard'ga qaytadi — saqlashni «:save» javobi va ro'yxat qidiruvi bilan tasdiqla.
