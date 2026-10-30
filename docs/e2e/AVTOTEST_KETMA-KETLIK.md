# SmartUp xtrade — avtotest ketma-ketligi (Playwright uchun)

Manba: `SmartUp_QA/1_Smoke_2026-09-28/Test_caselar` (qo'lda) va `SmartUp_QA/3_Avtotest/Test_caselar_json` (JSON) dagi 858 ta test case, 9 modul. Bu hujjat case'larni **bog'liqlik bo'yicha** 15 bosqichga ajratadi va har bosqich ichida aniq tartib beradi. Ketma-ketlik `run_order.json` (mashina uchun) va `run_order.xlsx` (filtr bilan) fayllarida ham bor.

## 1. Nima uchun aynan shu tartib

- **Ma'lumotnoma → hujjat → hisobot.** Hujjat formalari (Закупка, Заказ, Оплата…) select'larda ma'lumotnoma yozuvlarini talab qiladi; hisobotlar esa hujjatlar bo'lmasa bo'sh chiqadi. Shuning uchun P02–P05 (ma'lumotnomalar/sozlamalar) → P06–P11 (hujjatlar) → P12 (hisobotlar).
- **Qoldiq zanjiri.** Ombor hujjatlari bir-birining natijasiga tayanadi: qoldiqsiz Списание/Перемещение/Возврат o'tmaydi. P06 ichidagi tartib shuning uchun qat'iy.
- **Bir formaning ichida:** Smoke → UI → Validatsiya (bo'sh saqlash) → Salbiy → Ijobiy (oddiy) → Ijobiy CRUD → Regressiya → Bug. Sabab: UI/validatsiya case'lari ma'lumot yaratmaydi va forma buzilgan bo'lsa CRUD ni boshlamaslik kerak; CRUD o'zi yaratgan yozuvini o'zi o'chiradi.
- **Bug case'lari (P13)** mustaqil — ular ma'lumotni o'z ichida yaratadi yoki faqat o'qiydi; alohida project qilib istalgan vaqtda, parallel yuritish mumkin.

## 2. Bosqichlar

| Bosqich | Nomi | Rejim | Case'lar | Bog'liqlik / izoh |
|---|---|---|---|---|
| P00 | Muhit tayyorlash (globalSetup, seed) | setup | 0 | Login (storageState), filial «Toshkent», RUN_ID va QA- prefiks; hech qanday test yozilmaydi — faqat mavjudlik tekshiruvi va find-or-create. |
| P01 | Главное — tizim darajasidagi smoke va tashkilot | serial | 64 | Ma'lumot yaratmaydi (Задачи CRUD dan tashqari). Boshqa bosqichlarga bog'liq emas; hamma narsadan oldin tizim tirikligini tasdiqlaydi. |
| P02 | Bazaviy ma'lumotnomalar — moliya asoslari | serial | 21 | Valyuta, hisoblar rejasi, operatsiya turlari, daromad/xarajat moddalari. Ularsiz hujjatlar formalarida select'lar bo'sh bo'ladi. |
| P03 | Bazaviy ma'lumotnomalar — Справочники (tashkiliy tuzilma va kontragentlar) | serial | 59 | Tartib muhim: Отделы → Должности → Рабочие зоны → Штат (shtat bo'lim/lavozim/zonaga tayanadi); Физ.лица → Юр.лица → Клиенты; Регионы mustaqil. |
| P04 | Bazaviy ma'lumotnomalar — ТМЦ, narx, ombor, yetkazib beruvchi | serial | 119 | Производители → ТМЦ → Услуги → Цены → Скидки; Склады, Автотранспорт, Поставщики (SKL). Ishlab chiqarish ma'lumotnomalari ТМЦ ga tayanadi. |
| P05 | Marketing va savdo sozlamalari (ma'lumotnomalar ustiga) | serial | 176 | Клиенты, Штат, ТМЦ mavjud bo'lgandan keyin: aksiyalar, kategoriyalar, MOA, KPI sozlamalari, merchandayzing konstruktori, TM ma'lumotnomalari. |
| P06 | Склад — hujjatlar (qoldiq hosil qilish) | serial | 124 | Tartib qat'iy: Ввод начальных остатков (qoldiq paydo bo'ladi) → Запросы на закупку → Закупки → Поступления → Доп. расходы → Возвраты поставщику → Списания → Инвентаризации → Переоценки → Пересчет → ichki/ tashkilotlararo ko'chirishlar → Маркировка → Прогноз. Har hujjat oldingisining natijasiga (qoldiq) tayanadi. |
| P07 | Производство (ombor qoldig'i ustiga) | serial | 32 | Spetsifikatsiya/tex. karta P04 da tayyor. Tartib: План → Журнал плана → Заказ на производство → Технологические операции → Производственные задания → Отчет о нанесении/Заказы КМ → Ввод произв. остатков → hisobotlar. |
| P08 | Продажа (qoldiq + mijoz + shtat ustiga) | serial | 42 | Заявки → Заказы → Возвраты (buyurtmaga tayanadi) → Взаиморасчеты; tashriflar va rejalar mustaqil, lekin shtat/mijoz kerak. |
| P09 | Оборудование (mijoz, ombor, xarakteristika ustiga) | serial | 21 | Заявки на оборудование (установить) → Заявки на перемещения → Межорг. перемещение → Заявки на ремонт → Остатки → Конструктор. |
| P10 | Финансы — hujjatlar (buyurtma/xarid/xodim ustiga) | serial | 66 | Оплаты от клиентов (buyurtma kerak) → Оплаты поставщикам (xarid kerak) → Кассовые → Банковские → Чековая книжка → Платежные → Мои заявки → Согласование → Оплаты (ДП) → Запросы об оплате → Ручные операции → Уставный капитал → Взаиморасчеты → Перекидка → Переоценка валют → Документооборот. |
| P11 | Кадры и зарплата — hisob-kitob (xodim + turlar ustiga) | serial | 16 | Расчеты зарплаты → Выплаты (hisob-kitobga tayanadi) → Бонусная система. |
| P12 | Hisobotlar (barcha modullar) — ma'lumot yig'ilgandan keyin | parallel | 84 | Faqat o'qiydi. Parallel ishga tushirish mumkin (workers > 1), lekin P06–P11 tugagandan keyin, aks holda hisobotlar bo'sh chiqadi. |
| P13 | Umumiy va bug-regressiya (mustaqil) | parallel | 34 | «Umumiy» bo'limlari va Bug tipidagi case'lar — ma'lumotga bog'liq emas (yoki o'z ichida yaratadi). Alohida project, istalgan vaqtda, parallel. |
| P14 | Tozalash (globalTeardown) | teardown | 0 | RUN_ID prefiksli barcha yozuvlarni teskari tartibda o'chirish: hujjatlar (P10→P06) → sozlamalar (P05) → ma'lumotnomalar (P04→P02). Provodka qilingan hujjat avval bekor qilinadi. |

Rejimlar: `setup` — globalSetup; `serial` — bitta worker, faylda `test.describe.configure({ mode: 'serial' })`; `parallel` — workers > 1 mumkin; `teardown` — globalTeardown.

## 3. P00 — seed (globalSetup) ro'yxati

Bu obyektlar **RUN_ID siz**, doimiy nom bilan, find-or-create tartibida yaratiladi va teardown'da o'chirilmaydi (keyingi run'lar qayta ishlatadi). Test ichida yaratiladigan hamma narsa esa `QA-<RUN_ID>-…` prefiksi bilan.

| Obyekt | Nom / qiymat | Qayerda |
|---|---|---|
| Валюта | Узбекский сум (базовая) — mavjud | FIN → Валюты |
| План счетов | 0000. Остатки, 5010, 6310 — mavjud | FIN → План счетов |
| Регион | QA-SEED-REGION | Справочники → Регионы |
| Отдел / Должность | QA-SEED-DIV, QA-SEED-JOB | Справочники → Отделы, Должности |
| Рабочая зона | Room - Yashnobod (mavjud) yoki QA-SEED-ROOM | Справочники → Рабочие зоны |
| Штат | Main Manager (mavjud) yoki QA-SEED-STAFF | Справочники → Штат |
| Физическое / Юридическое лицо | QA-SEED-PERSON, QA-SEED-LEGAL | Справочники → Физические/Юридические лица |
| Клиент | Client-2/Yashnobod (mavjud) yoki QA-SEED-CLIENT | Справочники → Клиенты |
| Поставщик | TMS maker (mavjud) yoki QA-SEED-SUPPLIER | Склад → Поставщики |
| Склад | WH-Yashnobod (mavjud) yoki QA-SEED-WH | Склад → Склады |
| Производитель / ТМЦ | QA-SEED-PRODUCER, QA-SEED-ITEM-1..3 (Тип ТМЦ, Ед. изм. bilan) | Справочники → Производители, ТМЦ |
| Тип цены / Цена | QA-SEED-PRICE (ТМЦ uchun narx) | Справочники → Цены |
| Договор | QA-SEED-CONTRACT (mijoz bilan) | Финансы → Договоры |
| Начальный остаток | QA-SEED-ITEM-1..3 uchun 100 dona (Ввод начальных остатков, provodka) | Склад → Ввод начальных остатков |
| Сотрудник | QA-SEED-EMP (jismoniy shaxsdan) | Кадры → Сотрудники |
| Спецификация / Тех. карта | QA-SEED-SPEC, QA-SEED-STEP | Производство |

## 4. Playwright loyihasini tashkil qilish

```
playwright.config.js:
  fullyParallel: false,
  workers: process.env.CI ? 1 : 1,          // hujjat bosqichlari uchun 1; P12/P13 uchun alohida project'da 4
  retries: 0,                                // qayta run — faqat qo'lda, RUN_ID yangilanadi
  projects: [
    { name: 'setup',  testMatch: /global\.setup\.js/ },                       // P00: login → storageState, seed
    { name: 'p01-glavnoe', dependencies: ['setup'], testMatch: /p01-.*\.spec\.js/ },
    { name: 'p02-fin-base', dependencies: ['p01-glavnoe'], ... },              // har bosqich oldingisiga dependencies
    ...
    { name: 'p12-reports', dependencies: ['p11-hr'], workers: 4, fullyParallel: true },
    { name: 'p13-bugs',   dependencies: ['setup'], workers: 4, fullyParallel: true },  // mustaqil
    { name: 'teardown',   dependencies: ['p12-reports'], testMatch: /global\.teardown\.js/ },
  ]
```

**Fayl tuzilmasi:** `tests/<bosqich>/<modul>-<forma>.spec.js` — bir bo'lim = bir fayl; fayl ichida `test.describe.configure({ mode: 'serial' })` va testlar `run_order.json` dagi `seq` tartibida (`test(`[${seq}] ${id} ${title}`)`).

**Ma'lumot izolyatsiyasi:**
- `RUN_ID = Date.now().toString(36)`; har yaratilgan yozuv nomi `QA-${RUN_ID}-<forma>-<n>` — bir necha run ustma-ust tushsa ham to'qnashmaydi, ro'yxatda qidiruv aynan shu nom bilan.
- Yaratilgan ID/nomlar `.qa-data/${RUN_ID}.json` ga yoziladi (`test.info().annotations` emas — fayl, chunki keyingi bosqich boshqa worker'da). Keyingi bosqich `needs` ro'yxatini shu fayldan oladi; topilmasa — `test.skip('prerequisite yo'q: …')`, xato emas.
- Bir xil ketma-ketlikni har xil tartibda qayta run qilish kerak bo'lsa: faqat **bitta bosqich ichida** aralashtirish mumkin (`--shard` yoki `--grep @p05`); bosqichlar orasidagi tartib buzilmasin.

**Login:** parol kodda saqlanmaydi; `global.setup.js` `process.env.SMARTUP_LOGIN/PASSWORD` dan foydalanadi va `storageState` ni `.auth/user.json` ga yozadi; barcha project'lar `use: { storageState: '.auth/user.json' }`. Filial har spec boshida tekshiriladi (`TRADE / Toshkent`), boshqa bo'lsa `__switchFilial('Toshkent')`.

**Xavfli amallar (avtotestda ham):** `Провести`, `Проводки`, `Завершить`, `Утвердить/Отклонить`, tashqi tizimlarga yuborish (WMS, Faktura, Soliq, Telegram), `Пересчет`, bonus hisoblash — faqat **o'z RUN_ID hujjatlari** ustida va faqat test muhitida; begona yozuvga tegilmaydi. Foydalanuvchi yaratish/parol kiritish avtotestga kiritilmaydi.

**Teardown (P14):** `.qa-data/${RUN_ID}.json` dagi ro'yxat teskari tartibda o'chiriladi: provodka qilingan hujjat → `Отменить`/`Черновик` → `Удалить`; keyin ma'lumotnomalar. O'chirib bo'lmaydigan (tarixga kirgan) yozuv `Неактивный` qilinadi va hisobotga yoziladi.

## 5. To'liq ketma-ketlik

Quyida barcha 858 ta case bosqich va bo'lim bo'yicha. `+` — case ma'lumot yaratadi (CRUD). To'liq ustunlar (`serial_group`, tag) — `run_order.xlsx`.


### P01 · Главное · Организации

1. `TC-GL-FIL-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
2. `TC-GL-FIL-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
3. `TC-GL-FIL-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
4. `TC-GL-FIL-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
5. `TC-GL-FIL-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P01 · Главное · Пользователи

6. `TC-GL-USR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
7. `TC-GL-USR-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
8. `TC-GL-USR-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
9. `TC-GL-USR-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
10. `TC-GL-USR-006` [Salbiy, P2] Salbiy: mavjud login bilan foydalanuvchi yaratish
11. `TC-GL-USR-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P01 · Главное · Проекты

12. `TC-GL-SUB-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
13. `TC-GL-SUB-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
14. `TC-GL-SUB-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
15. `TC-GL-SUB-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
16. `TC-GL-SUB-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P01 · Главное · История изменений

17. `TC-GL-AUD-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P01 · Главное · Шаги визита

18. `TC-GL-ROL-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
19. `TC-GL-ROL-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi

### P01 · Главное · Настройки интеграции

20. `TC-GL-EXT-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
21. `TC-GL-EXT-002` [Ijobiy, P3] Ijobiy: sozlamani o'zgartirib saqlash

### P01 · Главное · Объекты

22. `TC-GL-ENT-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
23. `TC-GL-ENT-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi

### P01 · Главное · Динамичные поля

24. `TC-GL-FLD-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
25. `TC-GL-FLD-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
26. `TC-GL-FLD-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P01 · Главное · Отчeты

27. `TC-GL-REP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
28. `TC-GL-REP-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi

### P01 · Главное · Задачи

29. `TC-GL-TSK-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
30. `TC-GL-TSK-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
31. `TC-GL-TSK-006` [UI, P3] UI: forma yorliqlari ruscha
32. `TC-GL-TSK-005` [Validatsiya, P1] Validatsiya: sarlavhasiz — «Сохранить» nofaol
33. `TC-GL-TSK-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
34. `TC-GL-TSK-007` [Ijobiy, P3] Ijobiy: «Копировать» va «Состояния»
35. + `TC-GL-TSK-004` [Ijobiy, P1] CRUD: yaratish → ko'rish → izoh qo'shish → o'chirish

### P01 · Главное · Канбан

36. `TC-GL-KAN-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P01 · Главное · Календарь задач

37. `TC-GL-CAL-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P01 · Главное · Бэклог продукта

38. `TC-GL-BKL-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
39. `TC-GL-BKL-002` [UI, P3] Loyiha tanlanmaganda yo'riqnoma

### P01 · Главное · Спринты

40. `TC-GL-SPR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P01 · Главное · Отчёты по задачам

41. `TC-GL-TRP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
42. `TC-GL-TRP-002` [UI, P3] Admin bo'lmagan foydalanuvchi uchun «Сводка»

### P01 · Главное · Проекты (задачи)

43. `TC-GL-TPR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
44. `TC-GL-TPR-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
45. `TC-GL-TPR-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
46. `TC-GL-TPR-004` [Ijobiy, P2] Ijobiy: QA- loyiha → Бэклог/Спринты da tanlash → o'chirish

### P01 · Главное · Состояния задач

47. `TC-GL-TST-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
48. `TC-GL-TST-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
49. `TC-GL-TST-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P01 · Главное · Дополнительные поля

50. `TC-GL-TCF-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
51. `TC-GL-TCF-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi

### P01 · Главное · Шаблоны задач

52. `TC-GL-TTP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
53. `TC-GL-TTP-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar

### P01 · Главное · Характеристики задач

54. `TC-GL-TGR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
55. `TC-GL-TGR-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
56. `TC-GL-TGR-003` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
57. `TC-GL-TGR-004` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
58. + `TC-GL-TGR-005` [Ijobiy, P3] Ijobiy: QA- xarakteristika yaratish

### P01 · Главное · Запуски правил

59. `TC-GL-RUN-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P01 · Главное · Шаблоны накладных

60. `TC-GL-TPL-001` [Smoke, P2] Smoke: ro'yxat (eski sahifa)
61. `TC-GL-TPL-002` [Validatsiya, P2] Validatsiya: bo'sh forma «СОХРАНИТЬ»

### P01 · Главное · Настройки системы

62. `TC-GL-SYS-001` [Smoke, P2] Smoke: tablar ochiladi (saqlamasdan)

### P01 · Главное · Umumiy

63. `TC-GL-GEN-001` [Bug, P3] Tarjima fayllari (+add.json, kernel-overlay) yuklanadi
64. `TC-GL-GEN-002` [Bug, P3] Sarlavha va yorliqlar bir xil

### P02 · Финансы · Валюты

65. `TC-FIN-CUR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
66. `TC-FIN-CUR-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
67. `TC-FIN-CUR-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
68. `TC-FIN-CUR-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
69. `TC-FIN-CUR-007` [Salbiy, P2] Salbiy: mavjud kod (398) bilan valyuta yaratish
70. `TC-FIN-CUR-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
71. + `TC-FIN-CUR-006` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P02 · Финансы · План счетов

72. `TC-FIN-COA-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
73. `TC-FIN-COA-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
74. `TC-FIN-COA-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
75. `TC-FIN-COA-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
76. `TC-FIN-COA-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P02 · Финансы · Виды операций

77. `TC-FIN-CFR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
78. `TC-FIN-CFR-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
79. `TC-FIN-CFR-003` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
80. `TC-FIN-CFR-004` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
81. + `TC-FIN-CFR-005` [Ijobiy, P1] CRUD: yaratish → tahrir → o'chirish

### P02 · Финансы · Статьи доходов

82. `TC-FIN-INA-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P02 · Финансы · Статьи расходов

83. `TC-FIN-EXA-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
84. `TC-FIN-EXA-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
85. `TC-FIN-EXA-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P03 · Справочники · Регионы

86. `TC-SPR-REG-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
87. `TC-SPR-REG-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
88. `TC-SPR-REG-003` [Bug, P1] Yangi mamlakat/viloyat yaratish

### P03 · Справочники · Отделы

89. `TC-SPR-DIV-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
90. `TC-SPR-DIV-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
91. `TC-SPR-DIV-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
92. `TC-SPR-DIV-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
93. `TC-SPR-DIV-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
94. + `TC-SPR-DIV-006` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P03 · Справочники · Должности

95. `TC-SPR-JOB-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
96. `TC-SPR-JOB-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
97. `TC-SPR-JOB-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
98. `TC-SPR-JOB-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
99. `TC-SPR-JOB-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
100. + `TC-SPR-JOB-006` [Ijobiy, P1] CRUD: yaratish → ko'rish → o'chirish
101. `TC-SPR-JOB-007` [Bug, P1] Tahrir: nomni o'zgartirib saqlash

### P03 · Справочники · Рабочие зоны

102. `TC-SPR-ROOM-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
103. `TC-SPR-ROOM-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
104. `TC-SPR-ROOM-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
105. `TC-SPR-ROOM-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
106. `TC-SPR-ROOM-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
107. + `TC-SPR-ROOM-006` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P03 · Справочники · Штат

108. `TC-SPR-ROB-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
109. `TC-SPR-ROB-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
110. `TC-SPR-ROB-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
111. `TC-SPR-ROB-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
112. `TC-SPR-ROB-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
113. + `TC-SPR-ROB-006` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P03 · Справочники · Физические лица

114. `TC-SPR-NPR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
115. `TC-SPR-NPR-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
116. `TC-SPR-NPR-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
117. `TC-SPR-NPR-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
118. `TC-SPR-NPR-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
119. + `TC-SPR-NPR-006` [Ijobiy, P2] Yaratish (Имя, Группа, Категория) → ko'rish → o'chirish

### P03 · Справочники · Юридические лица

120. `TC-SPR-LPR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
121. `TC-SPR-LPR-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
122. `TC-SPR-LPR-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
123. `TC-SPR-LPR-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
124. `TC-SPR-LPR-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
125. + `TC-SPR-LPR-006` [Ijobiy, P2] Yaratish (Полное название + Регион) va o'chirish

### P03 · Справочники · Клиенты

126. `TC-SPR-CLI-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
127. `TC-SPR-CLI-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
128. `TC-SPR-CLI-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
129. `TC-SPR-CLI-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
130. `TC-SPR-CLI-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
131. `TC-SPR-CLI-006` [Bug, P2] Ustunlar takrorlanmaydi; ko'rish yorliqlari ruscha

### P03 · Справочники · Продавцы

132. `TC-SPR-SLR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P03 · Справочники · Уведомления

133. `TC-SPR-NTF-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
134. `TC-SPR-NTF-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
135. `TC-SPR-NTF-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P03 · Кадры и зарплата · Отделы

136. `TC-KDR-DIV-001` [Smoke, P3] Smoke: Кадры menyusidan ochish (Справочники bilan bir xil sahifa)

### P03 · Кадры и зарплата · Должности

137. `TC-KDR-JOB-001` [Smoke, P3] Smoke: Кадры menyusidan ochish (Справочники bilan bir xil sahifa)

### P03 · Кадры и зарплата · Сотрудники

138. `TC-KDR-EMP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
139. `TC-KDR-EMP-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
140. `TC-KDR-EMP-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
141. `TC-KDR-EMP-005` [Validatsiya, P1] Validatsiya: «Физическое лицо» siz saqlash
142. `TC-KDR-EMP-006` [Salbiy, P2] Salbiy: ПИНФЛ/ИНПС maydoniga harf kiritish
143. `TC-KDR-EMP-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
144. + `TC-KDR-EMP-007` [Ijobiy, P1] Ijobiy: mavjud jismoniy shaxsdan xodim yaratish → tahrir → o'chirish

### P04 · Справочники · Производители

145. `TC-SPR-PRD-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
146. `TC-SPR-PRD-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
147. `TC-SPR-PRD-003` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
148. `TC-SPR-PRD-004` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
149. + `TC-SPR-PRD-005` [Ijobiy, P1] CRUD: yangi nom → «Добавить» → Юридическое лицо dialogi → saqlash → tahrir → o'chirish

### P04 · Справочники · ТМЦ

150. `TC-SPR-TMC-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
151. `TC-SPR-TMC-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
152. `TC-SPR-TMC-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
153. `TC-SPR-TMC-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
154. `TC-SPR-TMC-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P04 · Справочники · Услуги

155. `TC-SPR-SRV-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
156. `TC-SPR-SRV-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
157. `TC-SPR-SRV-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P04 · Справочники · Цены

158. `TC-SPR-PRC-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
159. `TC-SPR-PRC-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
160. `TC-SPR-PRC-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
161. `TC-SPR-PRC-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
162. `TC-SPR-PRC-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P04 · Справочники · Скидки/наценки

163. `TC-SPR-MRG-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
164. `TC-SPR-MRG-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi

### P04 · Справочники · Сеты ТМЦ

165. `TC-SPR-KIT-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
166. `TC-SPR-KIT-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
167. `TC-SPR-KIT-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
168. + `TC-SPR-KIT-004` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P04 · Склад · Склады

169. `TC-SKL-WH-009` [UI, P3] Tab ustun nomlari to'g'ri
170. `TC-SKL-WH-001` [Validatsiya, P2] Validatsiya: majburiy maydonlar
171. `TC-SKL-WH-002` [Ijobiy, P2] Hajm hisoblash: to'g'ri burchak 2.5×10×20=500; yumaloq (Диаметр 2, Высота 10) ≈ 31.42
172. `TC-SKL-WH-004` [Ijobiy, P2] Tahrir: barcha maydonlar yuklanadi; o'zgarishlar (МОЛ tozalash, zona, shakl, GPS) saqlanadi
173. `TC-SKL-WH-005` [Ijobiy, P2] Narx turini biriktirish/ajratish
174. + `TC-SKL-WH-003` [Ijobiy, P1] Yaratish (barcha maydonlar) → ro'yxat → ko'rish (13 tab)
175. + `TC-SKL-WH-006` [Ijobiy, P2] Неактивный; o'chirish
176. `TC-SKL-WH-007` [Bug, P2] «Остатки» tabi ustunlari normal, «Номер карточки» bor
177. `TC-SKL-WH-008` [Bug, P3] Xarita oynasi: sarlavha tarjima qilingan, konsol xatosiz

### P04 · Склад · Автотранспорт

178. `TC-SKL-VAN-005` [UI, P3] Sahifa yorliqlari tarjima qilingan, qaysi transport ekani ko'rinadi
179. `TC-SKL-VAN-001` [Validatsiya, P2] Validatsiya: majburiy maydonlar qizil
180. `TC-SKL-VAN-006` [Salbiy, P3] Takroriy «Гос. номер» — ogohlantirish
181. `TC-SKL-VAN-003` [Ijobiy, P2] Nomi/sig'imi/hajmi/turi/izoh o'zgarishi saqlanadi
182. `TC-SKL-VAN-004` [Ijobiy, P2] Haydovchini biriktirish/ajratish
183. `TC-SKL-VAN-007` [Ijobiy, P2] Неактивный; o'chirish
184. + `TC-SKL-VAN-002` [Ijobiy, P1] Yaratish → ro'yxat → ko'rish
185. `TC-SKL-VAN-008` [Bug, P3] Takroriy «Код» — tushunarli xabar
186. `TC-SKL-VAN-009` [Bug, P2] Bo'sh kod bilan «Прикрепить» bloklanadi

### P04 · Склад · Поставщики

187. `TC-SKL-SUP-001` [Validatsiya, P2] Validatsiya: Название bo'sh
188. `TC-SKL-SUP-003` [Ijobiy, P2] НДС 12 → 15 saqlanadi
189. `TC-SKL-SUP-004` [Ijobiy, P2] ТМЦ biriktirish / ajratish
190. `TC-SKL-SUP-005` [Ijobiy, P2] Неактивный → Активный; o'chirish
191. + `TC-SKL-SUP-002` [Ijobiy, P1] Yaratish (НДС 12%) → ro'yxat → ko'rish
192. `TC-SKL-SUP-006` [Bug, P2] Validatsiya: НДС 0–100 oralig'ida
193. `TC-SKL-SUP-007` [Bug, P2] «Закупки» tabi yuklanadi

### P04 · Склад · Boshqa ro'yxatlar

194. `TC-SKL-OTH-003` [Validatsiya, P3] Sahifa ochiladi; majburiy maydonlarsiz «Расчет» rad etiladi
195. `TC-SKL-OTH-001` [Ijobiy, P3] Ro'yxat: ustunlar va qidiruv
196. `TC-SKL-OTH-002` [Ijobiy, P3] Ro'yxat va «Настройка» oynasi
197. + `TC-SKL-OTH-004` [Ijobiy, P2] Hisoblash → tavsiya etilgan miqdorlar → «Далее» bilan перемещение yaratish

### P04 · Финансы · Договоры

198. `TC-FIN-CON-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
199. `TC-FIN-CON-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
200. `TC-FIN-CON-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
201. `TC-FIN-CON-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
202. `TC-FIN-CON-007` [Salbiy, P2] Salbiy: «Дата окончания» < «Дата оформления»
203. `TC-FIN-CON-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
204. + `TC-FIN-CON-006` [Ijobiy, P2] Ijobiy: QA- shartnoma yaratish → ko'rish → o'chirish

### P04 · Производство · Ресурсы/доп.затраты

205. `TC-PRZ-XCS-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
206. `TC-PRZ-XCS-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
207. `TC-PRZ-XCS-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
208. `TC-PRZ-XCS-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
209. `TC-PRZ-XCS-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
210. `TC-PRZ-XCS-007` [Ijobiy, P3] Holat: «Неактивный» → «Активный»
211. + `TC-PRZ-XCS-006` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P04 · Производство · Оборудование (производство)

212. `TC-PRZ-EQP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
213. `TC-PRZ-EQP-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
214. `TC-PRZ-EQP-003` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
215. `TC-PRZ-EQP-004` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
216. `TC-PRZ-EQP-006` [Salbiy, P3] Salbiy: takroriy nom/kod bilan qo'shish
217. + `TC-PRZ-EQP-005` [Ijobiy, P1] CRUD: qo'shish → tahrir → o'chirish

### P04 · Производство · Спецификация

218. `TC-PRZ-SPC-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
219. `TC-PRZ-SPC-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
220. `TC-PRZ-SPC-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
221. `TC-PRZ-SPC-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
222. `TC-PRZ-SPC-006` [Salbiy, P2] Salbiy: ТМЦ qatorlarisiz saqlash
223. `TC-PRZ-SPC-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
224. + `TC-PRZ-SPC-007` [Ijobiy, P2] Ijobiy: xom ashyo + natija ТМЦ bilan yaratish, keyin o'chirish
225. `TC-PRZ-SPC-008` [Ijobiy, P3] «Копировать» — tanlangan spetsifikatsiyadan nusxa

### P04 · Производство · Технологическая карта

226. `TC-PRZ-STP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
227. `TC-PRZ-STP-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
228. `TC-PRZ-STP-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
229. `TC-PRZ-STP-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
230. `TC-PRZ-STP-006` [Salbiy, P2] Salbiy: bosqich/ТМЦ siz saqlash
231. `TC-PRZ-STP-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
232. + `TC-PRZ-STP-007` [Ijobiy, P2] Ijobiy: bosqich + spetsifikatsiya bilan yaratish, keyin o'chirish

### P04 · Оборудование · Характеристики оборудования

233. `TC-OBR-GRP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
234. `TC-OBR-GRP-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
235. `TC-OBR-GRP-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
236. `TC-OBR-GRP-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
237. `TC-OBR-GRP-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
238. + `TC-OBR-GRP-006` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P04 · Оборудование · Неисправности оборудования

239. `TC-OBR-BRK-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P04 · Кадры и зарплата · Виды начислений

240. `TC-KDR-ACC-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
241. `TC-KDR-ACC-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
242. `TC-KDR-ACC-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
243. `TC-KDR-ACC-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
244. `TC-KDR-ACC-008` [Salbiy, P3] Salbiy: takroriy «Код» bilan yaratish
245. `TC-KDR-ACC-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
246. `TC-KDR-ACC-007` [Ijobiy, P3] Ko'rish: «По виду начисления» tanlanganda Счет дебит/кредит maydonlari chiqadi
247. + `TC-KDR-ACC-006` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P04 · Кадры и зарплата · Виды удержаний

248. `TC-KDR-DED-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
249. `TC-KDR-DED-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
250. `TC-KDR-DED-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
251. `TC-KDR-DED-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
252. `TC-KDR-DED-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
253. + `TC-KDR-DED-006` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P04 · Кадры и зарплата · Виды выплат

254. `TC-KDR-PYT-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
255. `TC-KDR-PYT-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
256. `TC-KDR-PYT-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
257. `TC-KDR-PYT-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
258. `TC-KDR-PYT-007` [Salbiy, P2] Salbiy: «Счёт дебет» tanlanmasa saqlanmaydi
259. `TC-KDR-PYT-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
260. + `TC-KDR-PYT-006` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P04 · Продажа · Причины возврата

261. `TC-PRD-RRS-001` [Smoke, P2] Ro'yxat (Возвраты → «Причины возврата» tabi)
262. `TC-PRD-RRS-002` [Validatsiya, P2] Validatsiya: Название bo'sh
263. + `TC-PRD-RRS-003` [Ijobiy, P1] CRUD: yaratish → tahrir → Неактивный → o'chirish

### P05 · Справочники · Акции

264. `TC-SPR-ACT-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
265. `TC-SPR-ACT-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
266. `TC-SPR-ACT-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
267. `TC-SPR-ACT-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
268. `TC-SPR-ACT-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P05 · Справочники · Нагрузки

269. `TC-SPR-OVL-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
270. `TC-SPR-OVL-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
271. `TC-SPR-OVL-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
272. `TC-SPR-OVL-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
273. `TC-SPR-OVL-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P05 · Справочники · Рекомендации

274. `TC-SPR-REC-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
275. `TC-SPR-REC-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
276. `TC-SPR-REC-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P05 · Справочники · Продуктовая корзина

277. `TC-SPR-PST-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
278. `TC-SPR-PST-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
279. `TC-SPR-PST-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
280. + `TC-SPR-PST-004` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P05 · Справочники · Категоризация

281. `TC-SPR-CLP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
282. `TC-SPR-CNP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
283. `TC-SPR-CQZ-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
284. `TC-SPR-CRP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
285. `TC-SPR-CRS-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
286. `TC-SPR-CLP-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
287. `TC-SPR-CNP-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
288. `TC-SPR-CQZ-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
289. `TC-SPR-CQZ-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
290. + `TC-SPR-CQZ-004` [Ijobiy, P1] CRUD: nom + javob → saqlash → tahrir → o'chirish
291. `TC-SPR-CQZ-005` [Bug, P3] Javobsiz saqlash — sababi ko'rsatiladi

### P05 · Справочники · Минимальные обязательные ассортименты

292. `TC-SPR-MML-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
293. `TC-SPR-MML-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
294. `TC-SPR-MML-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
295. `TC-SPR-MML-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
296. `TC-SPR-MML-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P05 · Справочники · Правила ограничений

297. `TC-SPR-ORS-001` [Smoke, P3] Sahifa ochiladi

### P05 · Справочники · Лимитирование ТМЦ

298. `TC-SPR-OPL-001` [Smoke, P3] Sahifa ochiladi

### P05 · Справочники · Презентации

299. `TC-SPR-PRS-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
300. `TC-SPR-PRS-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
301. `TC-SPR-PRS-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P05 · Справочники · Опросники

302. `TC-SPR-QZS-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P05 · Справочники · Вопросы двойного визита

303. `TC-SPR-DVQ-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
304. `TC-SPR-DVQ-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
305. `TC-SPR-DVQ-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
306. + `TC-SPR-DVQ-004` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P05 · Справочники · Опросники двойных визитов

307. `TC-SPR-DVS-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
308. `TC-SPR-DVS-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
309. `TC-SPR-DVS-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
310. + `TC-SPR-DVS-004` [Ijobiy, P1] CRUD: yaratish → ko'rish → tahrir → o'chirish

### P05 · Справочники · Комментарии

311. `TC-SPR-CMT-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P05 · Справочники · Типы фото- и видео-отчетов

312. `TC-SPR-PHT-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
313. `TC-SPR-VDT-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P05 · Справочники · Публикация в бот

314. `TC-SPR-TGB-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
315. `TC-SPR-TGB-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
316. `TC-SPR-TGB-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P05 · Торговый маркетинг · Справочники: Настройка характеристики

317. `TC-TM-PT-001` [Smoke, P1] Ro'yxat ochiladi
318. `TC-TM-PT-002` [Validatsiya, P2] Yaratish: «Название» bo'sh
319. + `TC-TM-PT-003` [Ijobiy, P1] Yaratish: to'g'ri ma'lumot
320. `TC-TM-PT-004` [Ijobiy, P1] Mijozni biriktirish va ajratish
321. `TC-TM-PT-005` [Ijobiy, P3] Tahrirlash va nofaol qilish (URL orqali)
322. `TC-TM-PT-006` [Bug, P3] To'g'ridan URL bilan ochilgan formadan saqlash

### P05 · Торговый маркетинг · Справочники: Минимальные обязательные ассортименты

323. `TC-TM-MML-001` [Smoke, P1] Ro'yxat ochiladi
324. `TC-TM-MML-002` [Validatsiya, P2] Yaratish formasi va majburiy maydonlar
325. + `TC-TM-MML-003` [Ijobiy, P1] Yaratish: to'g'ri ma'lumot
326. `TC-TM-MML-004` [Ijobiy, P2] Ko'rish
327. `TC-TM-MML-005` [Ijobiy, P1] Tahrirlash: nom va sanalar
328. `TC-TM-MML-007` [Ijobiy, P2] «Настроить»: podtiplar ro'yxati
329. `TC-TM-MML-008` [Ijobiy, P1] Podtipga ТМЦ biriktirish
330. `TC-TM-MML-009` [Ijobiy, P3] «Дашборд по MML» va «Копировать из главного списка»
331. `TC-TM-MML-010` [Ijobiy, P2] O'chirish
332. `TC-TM-MML-006` [Bug, P2] Validatsiya: boshlanish sanasi tugash sanasidan keyin

### P05 · Торговый маркетинг · Справочники: Ассортименты

333. `TC-TM-AS-001` [Smoke, P1] Ro'yxat ochiladi
334. + `TC-TM-AS-002` [Ijobiy, P1] Yaratish: «Набор ТМЦ» orqali ТМЦ qo'shish
335. `TC-TM-AS-003` [Ijobiy, P2] Ko'rish: 4 tab
336. `TC-TM-AS-004` [Ijobiy, P1] Tahrirlash: nom va bitta ТМЦ ni olib tashlash
337. `TC-TM-AS-005` [Ijobiy, P2] Status va filtr
338. `TC-TM-AS-006` [Ijobiy, P2] O'chirish
339. `TC-TM-AS-007` [Ijobiy, P3] «Прикрепление» sahifasi

### P05 · Торговый маркетинг · Справочники: Планограммы

340. `TC-TM-PG-001` [Smoke, P1] Ro'yxat ochiladi
341. `TC-TM-PG-002` [Ijobiy, P1] Kompaniya planogrammasini filialga biriktirish
342. `TC-TM-PG-003` [Ijobiy, P2] Planogrammani ko'rish: 5 tab
343. `TC-TM-PG-004` [Ijobiy, P2] Ajratish

### P05 · Торговый маркетинг · Справочники: POS-материалы

344. `TC-TM-POS-001` [Smoke, P2] Ro'yxat va «Прикрепление» sahifasi ochiladi
345. `TC-TM-POS-002` [Ijobiy, P2] Kompaniya yozuvini filialga biriktirish va ajratish

### P05 · Торговый маркетинг · Справочники: Конкуренты

346. `TC-TM-CMP-001` [Smoke, P2] Ro'yxat va «Прикрепление» sahifasi ochiladi
347. `TC-TM-CMP-002` [Ijobiy, P2] Kompaniya yozuvini filialga biriktirish va ajratish

### P05 · Торговый маркетинг · Справочники: Продукты конкурентов

348. `TC-TM-CI-001` [Smoke, P3] Ro'yxat ochiladi

### P05 · Торговый маркетинг · Справочники: Статусы мерчандайзинга

349. `TC-TM-ST-001` [Smoke, P2] Ro'yxat va «Прикрепление» sahifasi ochiladi
350. `TC-TM-ST-002` [Ijobiy, P2] Kompaniya yozuvini filialga biriktirish va ajratish

### P05 · Торговый маркетинг · Справочники: Причины несоответствия

351. `TC-TM-RR-001` [Smoke, P1] Ro'yxat ochiladi
352. + `TC-TM-RR-003` [Ijobiy, P2] Yangi sabab yaratish (menyu «+»)
353. `TC-TM-RR-004` [Ijobiy, P2] Sababni biriktirish va ajratish
354. `TC-TM-RR-002` [Regressiya, P2] Ko'rish: nom, ИД, status ko'rsatiladi

### P05 · Торговый маркетинг · Справочники: Шаблон отчета по опросам

355. `TC-TM-QT-001` [Smoke, P1] Ro'yxat ochiladi
356. `TC-TM-QT-007` [UI, P3] Shablon turini almashtirish — savollar ogohlantirishsiz o'chadi
357. `TC-TM-QT-002` [Validatsiya, P1] Validatsiya: savol tanlanmagan
358. `TC-TM-QT-003` [Validatsiya, P2] Validatsiya: «По вопросам» turi uchun 2 ta savol
359. + `TC-TM-QT-004` [Ijobiy, P1] Yaratish: to'g'ri ma'lumot
360. `TC-TM-QT-005` [Ijobiy, P1] «Открыть» → hisobotni shakllantirish
361. `TC-TM-QT-006` [Ijobiy, P1] Tahrirlash
362. `TC-TM-QT-008` [Ijobiy, P2] O'chirish

### P05 · Торговый маркетинг · Конструктор: Настройки мерчандайзинга

363. `TC-TM-SET-001` [Smoke, P1] Ro'yxat ochiladi: ustunlar, tugmalar, qator amallari
364. `TC-TM-SET-012` [UI, P3] Barcha modullar yoqilganda tablar mazmuni
365. `TC-TM-SET-003` [Validatsiya, P2] Yaratish: majburiy maydonlar bo'sh — saqlanmaydi
366. `TC-TM-SET-004` [Validatsiya, P2] Yaratish: birorta modul yoqilmagan — xato xabari
367. `TC-TM-SET-002` [Ijobiy, P2] Mavjud sozlamani ko'rish: 4 tab va qiymatlar
368. + `TC-TM-SET-006` [Ijobiy, P1] Yaratish: to'g'ri ma'lumot bilan saqlash
369. `TC-TM-SET-007` [Ijobiy, P2] Yaratilgan sozlamani ko'rish
370. `TC-TM-SET-008` [Ijobiy, P1] Tahrirlash («Настройка»): nom va tartib raqami saqlanadi
371. `TC-TM-SET-009` [Ijobiy, P2] «Прикрепить»: mijozlarni biriktirish sahifasi
372. `TC-TM-SET-010` [Ijobiy, P2] Statusni «Неактивный» va qaytadan «Активный» qilish
373. `TC-TM-SET-011` [Ijobiy, P2] O'chirish
374. `TC-TM-SET-005` [Bug, P1] Yaratish: modul yoqilgan, «в баллах» bo'sh — frontda to'xtatilishi kerak

### P05 · Торговый маркетинг · Конструктор: Мерчандайзинг

375. `TC-TM-MER-001` [Smoke, P1] Ro'yxat: ustunlar va vizit qatorlari
376. `TC-TM-MER-002` [Ijobiy, P2] Vizitni ko'rish: 3 tab
377. `TC-TM-MER-003` [Ijobiy, P3] Tahrirlash formasi ochiladi va «Закрыть» bilan chiqiladi
378. `TC-TM-MER-004` [Ijobiy, P3] «Изменить статус» menyusi
379. `TC-TM-MER-005` [Ijobiy, P2] Vizit statusini «Завершено» qilish

### P05 · Торговый маркетинг · КПЭ: Шаблон КПЭ

380. `TC-TM-TPL-001` [Smoke, P1] Sahifa ochiladi
381. `TC-TM-TPL-002` [Validatsiya, P2] Validatsiya: foizlar yig'indisi 100 emas
382. `TC-TM-TPL-003` [Ijobiy, P1] Saqlash: 60/40 va qayta yuklash
383. `TC-TM-TPL-004` [Ijobiy, P2] «Рассчитать» — tarixiy ma'lumotdan hisoblash (saqlamasdan)
384. `TC-TM-TPL-005` [Ijobiy, P3] «Настройка» sahifasi

### P05 · Торговый маркетинг · КПЭ: КПЭ по штатам

385. `TC-TM-RB-001` [Smoke, P1] Ro'yxat ochiladi
386. `TC-TM-RB-003` [UI, P2] Yaratish formasi: maydonlar va «Тип КПЭ» variantlari
387. `TC-TM-RB-007` [UI, P3] Ko'rish → «Штаты» tabida faqat biznes ustunlari
388. `TC-TM-RB-004` [Validatsiya, P1] Validatsiya: har bir shtat qatorida «Цель» majburiy
389. + `TC-TM-RB-005` [Ijobiy, P1] Yaratish: to'g'ri ma'lumot bilan
390. `TC-TM-RB-006` [Ijobiy, P2] Ko'rish: maydonlar va tablar
391. `TC-TM-RB-008` [Ijobiy, P1] Tahrirlash: nom va Цель saqlanadi
392. `TC-TM-RB-009` [Ijobiy, P2] Status «Неактивный» va o'chirish
393. `TC-TM-RB-002` [Regressiya, P2] Ro'yxatda «Статус» ustuni ko'rinadi (eski versiyadagidek)

### P05 · Торговый маркетинг · КПЭ: КПЭ по рабочим зонам

394. `TC-TM-RZ-001` [Smoke, P1] Ro'yxat ochiladi
395. `TC-TM-RZ-006` [Validatsiya, P2] Validatsiya: «Рабочая зона» tanlanmagan
396. `TC-TM-RZ-007` [Validatsiya, P3] Validatsiya: manfiy / harfli qiymat
397. + `TC-TM-RZ-002` [Ijobiy, P1] Yaratish: zona bo'yicha plan
398. `TC-TM-RZ-003` [Ijobiy, P2] Ko'rish: qiymatlar bazadan o'qiladi
399. `TC-TM-RZ-004` [Ijobiy, P1] Tahrirlash va o'zgarishlar tarixi
400. `TC-TM-RZ-005` [Ijobiy, P2] O'chirish

### P05 · Торговый маркетинг · КПЭ: КПЭ по ТМЦ

401. `TC-TM-RP-001` [Smoke, P1] Ro'yxat ochiladi
402. `TC-TM-RP-006` [UI, P3] Jadvaldagi «№» ustuni qator raqamini ko'rsatadi
403. + `TC-TM-RP-002` [Ijobiy, P1] Yaratish: zona + ТМЦ bo'yicha plan
404. `TC-TM-RP-003` [Ijobiy, P2] Ko'rish
405. `TC-TM-RP-004` [Ijobiy, P1] Tahrirlash
406. `TC-TM-RP-005` [Ijobiy, P2] O'chirish

### P05 · Торговый маркетинг · КПЭ: КПЭ по характеристикам ТМЦ

407. `TC-TM-RPT-001` [Smoke, P1] Ro'yxat ochiladi
408. + `TC-TM-RPT-002` [Ijobiy, P1] Yaratish: zona + ТМЦ xarakteristikasi bo'yicha
409. `TC-TM-RPT-003` [Ijobiy, P1] Ko'rish va tahrirlash
410. `TC-TM-RPT-004` [Ijobiy, P2] O'chirish

### P05 · Торговый маркетинг · КПЭ: КПЭ по клиентам

411. `TC-TM-CL-001` [Smoke, P1] Ro'yxat ochiladi (mavjud plan bilan)
412. `TC-TM-CL-002` [Ijobiy, P2] «Настройки мобильного дашборда»: saqlash va qayta ochish
413. + `TC-TM-CL-003` [Ijobiy, P1] Yaratish: mijoz bo'yicha plan
414. `TC-TM-CL-004` [Ijobiy, P1] Ko'rish va tahrirlash
415. `TC-TM-CL-005` [Ijobiy, P2] O'chirish

### P05 · Торговый маркетинг · КПЭ: КПЭ клиентов по ТМЦ

416. `TC-TM-CP-001` [Smoke, P1] Ro'yxat ochiladi
417. + `TC-TM-CP-002` [Ijobiy, P1] Yaratish: mijoz + ТМЦ
418. `TC-TM-CP-003` [Ijobiy, P1] Ko'rish va tahrirlash
419. `TC-TM-CP-004` [Ijobiy, P2] O'chirish

### P05 · Торговый маркетинг · КПЭ: КПЭ клиентов по характеристикам ТМЦ

420. `TC-TM-CPT-001` [Smoke, P1] Ro'yxat ochiladi
421. + `TC-TM-CPT-002` [Ijobiy, P1] Yaratish, ko'rish, tahrirlash, o'chirish

### P05 · Торговый маркетинг · КПЭ: КПЭ на категорию клиентов

422. `TC-TM-CTPT-001` [Smoke, P1] Ro'yxat va «Создать» menyusi
423. + `TC-TM-CTPT-002` [Ijobiy, P1] Yaratish (Юр. лицо): xarakteristika bo'yicha guruh rejimi
424. `TC-TM-CTPT-003` [Ijobiy, P1] Ko'rish va tahrirlash
425. `TC-TM-CTPT-004` [Ijobiy, P2] O'chirish
426. + `TC-TM-CTPT-005` [Ijobiy, P2] Yaratish (Физ. лицо)
427. `TC-TM-CTPT-006` [Ijobiy, P3] Импорт

### P05 · Торговый маркетинг · КПЭ: Настройки бонуса

428. `TC-TM-BON-001` [Smoke, P1] Ro'yxat ochiladi
429. `TC-TM-BON-002` [Ijobiy, P2] Mavjud sozlamani ko'rish: 3 tab
430. `TC-TM-BON-003` [Ijobiy, P2] Hisoblangan bonuslarni Excel ga eksport
431. + `TC-TM-BON-004` [Ijobiy, P1] Yaratish: to'g'ri ma'lumot bilan
432. `TC-TM-BON-005` [Ijobiy, P1] Ko'rish va tahrirlash
433. `TC-TM-BON-006` [Ijobiy, P2] O'chirish
434. `TC-TM-BON-009` [Ijobiy, P1] Bonusni hisoblash («Рассчитать бонус»)
435. `TC-TM-BON-007` [Bug, P2] «Создать копию» → o'zgartirmasdan saqlash (dublikat)
436. `TC-TM-BON-008` [Bug, P2] «Создать копию» → zona almashtirish

### P05 · Оборудование · Цели для рекламного оборудования

437. `TC-OBR-TGT-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
438. `TC-OBR-TGT-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
439. `TC-OBR-TGT-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P06 · Склад · Ввод начальных остатков

440. `TC-SKL-IB-001` [Smoke, P2] Ro'yxat ochiladi, ustunlar va «Создать» bor
441. `TC-SKL-IB-002` [Validatsiya, P2] Validatsiya: Склад va ТМЦ tanlanmasdan saqlash
442. `TC-SKL-IB-008` [Salbiy, P3] Hujjat raqamlari takrorlanmaydi
443. `TC-SKL-IB-004` [Ijobiy, P2] Ko'rish: barcha maydonlar formadagidek
444. `TC-SKL-IB-005` [Ijobiy, P2] Tahrir: miqdorni o'zgartirish saqlanadi
445. `TC-SKL-IB-006` [Ijobiy, P1] Провести → qoldiq oshadi; bekor qilish → qaytadi
446. `TC-SKL-IB-007` [Ijobiy, P3] «Проводки» oynasi ochiladi
447. + `TC-SKL-IB-003` [Ijobiy, P1] Yaratish → saqlash → ro'yxatda qator (Черновик)
448. + `TC-SKL-IB-009` [Ijobiy, P2] O'chirish

### P06 · Склад · Запросы на закупку

449. `TC-SKL-PR-001` [UI, P3] Forma: maydonlar va standart qiymatlar
450. `TC-SKL-PR-002` [Validatsiya, P2] Validatsiya: ТМЦ siz saqlash
451. `TC-SKL-PR-003` [Validatsiya, P3] «Крайний срок поставки» da o'tgan sanalar tanlanmaydi
452. `TC-SKL-PR-005` [Ijobiy, P2] Ko'rish va tahrir (Новый holatida)
453. `TC-SKL-PR-006` [Ijobiy, P2] Status: Новый → Принято (tasdiq bilan); ro'yxat amallari o'zgaradi
454. + `TC-SKL-PR-004` [Ijobiy, P1] Yaratish: Подбор → saqlash → ro'yxat
455. + `TC-SKL-PR-007` [Ijobiy, P2] O'chirish
456. `TC-SKL-PR-008` [Bug, P1] «Принят» so'rov tahrirlanmaydi va Черновик ga qaytarilmaydi

### P06 · Склад · Закупки

457. `TC-SKL-PUR-003` [UI, P2] «С поступлением на склад» yoqilganda qo'shimcha maydonlar
458. `TC-SKL-PUR-001` [Validatsiya, P2] Validatsiya: поставщик tanlanmasa «Далее» o'tmaydi
459. `TC-SKL-PUR-002` [Validatsiya, P2] Validatsiya: ТМЦ siz saqlash
460. `TC-SKL-PUR-005` [Ijobiy, P2] Ko'rish: tablar va maydonlar
461. `TC-SKL-PUR-006` [Ijobiy, P2] Tahrir saqlanadi
462. `TC-SKL-PUR-007` [Ijobiy, P1] Provodka: «С поступлением на склад» bilan Провести → Поступление yaratiladi, qoldiq oshadi
463. + `TC-SKL-PUR-004` [Ijobiy, P1] Qoralama закупка: Сохранить (Черновик) → ro'yxatda qator
464. `TC-SKL-PUR-008` [Bug, P2] Копировать: nusxa asl hujjat maydonlarini saqlaydi
465. `TC-SKL-PUR-009` [Bug, P3] O'chirish tasdiq oynasi rus tilida
466. `TC-SKL-PUR-010` [Bug, P3] Jadvaldagi ТМЦ ro'yxati keng, nomlar to'liq
467. `TC-SKL-PUR-011` [Bug, P3] Menyu «Заказы на закупку» yangi (a2) sahifani ochadi

### P06 · Склад · Поступления ТМЦ

468. `TC-SKL-INP-003` [UI, P3] Status o'zgartirish tasdiq oynasi matni
469. `TC-SKL-INP-004` [UI, P3] «Сумма» ustuni turli valyutalarni valyuta ustunisiz aralashtirmaydi
470. `TC-SKL-INP-002` [Ijobiy, P2] Ko'rish: tablar xatosiz
471. + `TC-SKL-INP-001` [Ijobiy, P1] Закупкадан поступление yaratish; miqdor qoldiq bilan cheklanadi
472. + `TC-SKL-INP-005` [Ijobiy, P2] O'chirish

### P06 · Склад · Дополнительные расходы

473. `TC-SKL-EC-001` [Validatsiya, P2] Validatsiya: majburiy maydonlar
474. `TC-SKL-EC-003` [Ijobiy, P2] Ko'rish, Провести, «Распределить», bekor qilish
475. + `TC-SKL-EC-002` [Ijobiy, P1] Yaratish: «Вид движения» tanlanganda «Расход» maydoni chiqadi; saqlash
476. `TC-SKL-EC-004` [Bug, P3] НДС summadan katta bo'lsa rad etiladi; ko'rishda formatlangan

### P06 · Склад · Возвраты поставщику

477. `TC-SKL-RET-001` [Validatsiya, P2] Validatsiya: 1-qadam majburiy maydonlari
478. `TC-SKL-RET-003` [Ijobiy, P3] Ko'rish tablari xatosiz
479. + `TC-SKL-RET-002` [Ijobiy, P1] To'liq sikl: Завершить → qoldiq −1; Черновик → qaytadi; o'chirish
480. `TC-SKL-RET-004` [Bug, P3] 2-qadam ustunlari siqilmagan
481. `TC-SKL-RET-005` [Bug, P3] Dublikat maydon va noto'g'ri «Дата закупа» yo'q
482. `TC-SKL-RET-006` [Bug, P2] Validatsiya: «Цена» bo'sh bo'lsa yakunlash rad etiladi

### P06 · Склад · Списания

483. `TC-SKL-WO-002` [UI, P3] Подбор paneli: ustunlar va qoldiqlar
484. `TC-SKL-WO-009` [UI, P3] Status tasdiq matni to'g'ri
485. `TC-SKL-WO-001` [Validatsiya, P2] Validatsiya: Склад tanlanmasa Подбор yo'q, saqlash rad etiladi
486. `TC-SKL-WO-005` [Validatsiya, P2] Validatsiya: formadagi miqdor mavjuddan ko'p — aniq xabar
487. `TC-SKL-WO-003` [Ijobiy, P1] To'liq sikl: Подбор → Провести → qoldiq −1 → В сборке → Черновик (qoldiq qaytadi)
488. `TC-SKL-WO-004` [Ijobiy, P2] Tahrir: qator o'chirish, miqdor va izoh o'zgarishi saqlanadi
489. + `TC-SKL-WO-008` [Ijobiy, P2] O'chirish (Черновик)
490. `TC-SKL-WO-006` [Bug, P2] Mavjuddan ko'p miqdor — xabar, qator yo'qolmaydi
491. `TC-SKL-WO-007` [Bug, P2] Ko'rishda hujjat sanasi ko'rinadi

### P06 · Склад · Инвентаризации

492. `TC-SKL-ST-005` [UI, P3] Status tasdiq va yorliq matnlari to'g'ri
493. `TC-SKL-ST-001` [Validatsiya, P2] Validatsiya: majburiy maydonlar / ТМЦ siz
494. `TC-SKL-ST-003` [Ijobiy, P2] Tahrir: barcha maydonlar yuklanadi, miqdor o'zgarishi saqlanadi
495. `TC-SKL-ST-004` [Ijobiy, P1] Провести → qoldiq +2; bekor → qaytadi
496. + `TC-SKL-ST-002` [Ijobiy, P1] Ortiqcha (излишек) bilan: Подбор → narx → saqlash → ko'rish

### P06 · Склад · Переоценки себестоимости

497. `TC-SKL-RV-001` [Validatsiya, P2] Validatsiya: ТМЦ siz saqlash
498. `TC-SKL-RV-004` [Ijobiy, P2] Провести → tannarx o'zgaradi; bekor qilish; o'chirish
499. + `TC-SKL-RV-002` [Ijobiy, P1] Yaratish: yangi narx → farq hisoblanadi → saqlash → ro'yxat va ko'rish
500. `TC-SKL-RV-003` [Bug, P1] Tahrirdan keyin saqlash ishlaydi

### P06 · Склад · Пересчет приходных цен

501. `TC-SKL-RCI-001` [Validatsiya, P2] Validatsiya: majburiy sanalar
502. `TC-SKL-RCI-002` [Validatsiya, P2] Validatsiya: boshlanish sanasi tugashdan keyin
503. `TC-SKL-RCI-003` [Ijobiy, P3] To'g'ri davr: bajarilgach natija xabari

### P06 · Склад · Запросы на внутр. перемещения

504. `TC-SKL-MR-001` [Validatsiya, P2] Validatsiya: majburiy maydonlar va ТМЦ
505. `TC-SKL-MR-002` [Salbiy, P3] «Со склада» ro'yxatida «На склад» dagi ombor taklif qilinmaydi
506. `TC-SKL-MR-006` [Salbiy, P3] Bog'liq перемещение «Завершено» bo'lganda so'rov yopiladi
507. `TC-SKL-MR-004` [Ijobiy, P2] Status Новый → Принято; ko'rishda «Изменить» yo'q
508. + `TC-SKL-MR-003` [Ijobiy, P1] Yaratish → ro'yxat → ko'rish → tahrir
509. + `TC-SKL-MR-007` [Ijobiy, P2] O'chirish (Новый ga qaytarib)
510. `TC-SKL-MR-005` [Bug, P3] Status o'zgargandan keyin amal paneli yangilanadi

### P06 · Склад · Внутренние перемещения

511. `TC-SKL-MV-001` [Validatsiya, P2] Validatsiya: 1-qadam majburiy maydonlari
512. `TC-SKL-MV-003` [Validatsiya, P2] Validatsiya: 3-qadamda Статус bo'sh bo'lsa «Завершить» — xabar
513. `TC-SKL-MV-005` [Salbiy, P3] Подбор so'rov ТМЦ bo'yicha filtrlanadi, «Кол-во по запросу» to'ldiriladi
514. `TC-SKL-MV-004` [Ijobiy, P1] To'liq sikl: so'rov asosida → Новый → Ожидает отгрузку → В пути → Завершено; qoldiqlar
515. `TC-SKL-MV-008` [Ijobiy, P3] Hisobotlar va «Проводки»
516. `TC-SKL-MV-002` [Bug, P2] «Запрос» maydoni ochilganda bo'sh
517. `TC-SKL-MV-006` [Bug, P2] Jami vazn miqdorga ko'paytiriladi
518. `TC-SKL-MV-007` [Bug, P2] ТМЦ tabi normal ko'rinadi

### P06 · Склад · Межорг. перемещения: запросы

519. `TC-SKL-FMR-005` [Smoke, P3] Qabul qilingan so'rovlar ro'yxati ochiladi
520. `TC-SKL-FMR-001` [Validatsiya, P2] Validatsiya
521. + `TC-SKL-FMR-002` [Ijobiy, P1] Yaratish → ro'yxat → ko'rish → tahrir
522. + `TC-SKL-FMR-004` [Ijobiy, P2] O'chirish
523. `TC-SKL-FMR-003` [Bug, P2] Status o'zgarishi tasdiq bilan

### P06 · Склад · Межорг. перемещения

524. `TC-SKL-FM-008` [Smoke, P3] Arxiv va bekor qilinganlar ro'yxatlari ochiladi
525. `TC-SKL-FM-006` [UI, P3] Status menyusida joriy status ko'rsatilmaydi
526. `TC-SKL-FM-001` [Validatsiya, P2] Validatsiya: 1-qadam majburiy maydonlari
527. `TC-SKL-FM-005` [Ijobiy, P3] Qator amallari: Изменить проект / Изменить тип цены / Отчеты / Soliq.uz
528. `TC-SKL-FM-007` [Ijobiy, P2] Qabul qilish (qabul qiluvchi tashkilot tomonidan)
529. + `TC-SKL-FM-003` [Ijobiy, P1] To'liq sikl: Отправлено → qoldiq −2; Отменено → qaytadi; o'chirish
530. `TC-SKL-FM-002` [Bug, P2] «Тип оплаты» majburiy — 1-qadamda tekshiriladi
531. `TC-SKL-FM-004` [Bug, P2] Ko'rishda sanalar ko'rinadi

### P06 · Склад · Маркировка (КМ)

532. `TC-SKL-KM-008` [Smoke, P3] Ro'yxat ochiladi
533. `TC-SKL-KM-003` [UI, P2] Forma: maydonlar keng ekranda ko'rinadi
534. `TC-SKL-KM-001` [Validatsiya, P2] Validatsiya: guruh tanlanmasa xabar
535. + `TC-SKL-KM-002` [Ijobiy, P2] Markirovkalangan tovar bilan agregatsiya yaratish
536. `TC-SKL-KM-005` [Ijobiy, P3] Import va saqlash
537. `TC-SKL-KM-004` [Bug, P3] Tor ekranda (≤768 px) fayl bloklari kesilmaydi
538. `TC-SKL-KM-006` [Bug, P3] Sahifa ochiladi, konsol xatosiz
539. `TC-SKL-KM-007` [Bug, P3] «Генерировать»: mavjud bo'lmagan/bo'sh kod — tushunarli xabar

### P06 · Склад · Прогноз для закупки

540. `TC-SKL-FC-001` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz «Получить данные»
541. `TC-SKL-FC-003` [Validatsiya, P2] Validatsiya: «Данные пользователя» sanalari bo'sh bo'lsa «Рассчитать» — aniq xabar
542. `TC-SKL-FC-002` [Ijobiy, P1] «Получить данные» — tahlil qilinadigan ma'lumot yuklanadi
543. `TC-SKL-FC-005` [Ijobiy, P3] Hisobotlar: Отчет (xlsx) / Отчет (html)
544. + `TC-SKL-FC-004` [Ijobiy, P1] To'liq: sanalar → Рассчитать → Сохранить → ro'yxat
545. `TC-SKL-FC-006` [Bug, P1] «С исключениями = Нет» saqlangandan keyin ham Нет
546. `TC-SKL-FC-007` [Bug, P1] «Итоговый прогноз → Кол-во» saqlashdan keyin o'zgarmaydi

### P06 · Склад · Взаиморасчеты с поставщиками

547. `TC-SKL-OFS-002` [UI, P3] Pastki yakun formati va valyutasi jadvaldagidek
548. `TC-SKL-OFS-003` [UI, P3] Filtrda takroriy maydon yo'q, matnlar to'g'ri
549. `TC-SKL-OFS-001` [Ijobiy, P2] Ro'yxat, «Детали» va «История» ochiladi
550. `TC-SKL-OFS-004` [Ijobiy, P3] «Подтвердить» oynasi ochiladi (bajarilmaydi)

### P06 · Склад · Остатки ТМЦ

551. `TC-SKL-BAL-002` [UI, P3] «В наличии» formatlangan (2 030) va o'ngga tekislangan
552. `TC-SKL-BAL-007` [UI, P3] Filtr panelidagi «Тип ТМЦ» variantlari tarjima qilingan
553. `TC-SKL-BAL-004` [Validatsiya, P3] Validatsiya: Умеренный < Критический — xabar
554. `TC-SKL-BAL-006` [Salbiy, P3] «Открыть коды маркировки» tanlangan ТМЦ bilan ochiladi
555. `TC-SKL-BAL-001` [Ijobiy, P1] Ro'yxat: qoldiqlar, filtr va qidiruv
556. `TC-SKL-BAL-003` [Ijobiy, P2] Detal sahifasi va yakun qatori
557. `TC-SKL-BAL-005` [Ijobiy, P3] To'g'ri qiymatlar (40/10/0) saqlanadi

### P06 · Склад · Логистика

558. `TC-SKL-LOG-001` [Smoke, P2] Ro'yxat ochiladi; tugmalar Создать / Планирование маршрутов
559. `TC-SKL-LOG-002` [Ijobiy, P2] Oyna: transport tanlanganda Гос. номер va sig'im avtomatik
560. `TC-SKL-LOG-006` [Ijobiy, P2] Reysga buyurtmalar qo'shib saqlash
561. `TC-SKL-LOG-003` [Bug, P1] Menyu «+» sahifani xatosiz ochadi
562. `TC-SKL-LOG-004` [Bug, P2] Oyna yopiladi, tarjima va birlik to'g'ri
563. `TC-SKL-LOG-005` [Bug, P3] Ro'yxat ustunlari va mavjud reys tahriri

### P07 · Производство · План производства

564. `TC-PRZ-PLN-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
565. `TC-PRZ-PLN-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
566. `TC-PRZ-PLN-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P07 · Производство · Журнал план производства

567. `TC-PRZ-OPL-001` [Smoke, P2] Smoke: ro'yxat ochiladi
568. `TC-PRZ-OPL-002` [UI, P2] Yaratish formasi: yorliqlar ruscha
569. `TC-PRZ-OPL-003` [Validatsiya, P2] Validatsiya: bo'sh forma «СОХРАНИТЬ»

### P07 · Производство · Заказ на производство

570. `TC-PRZ-MOR-001` [Smoke, P2] Smoke: ro'yxat ochiladi
571. `TC-PRZ-MOR-002` [Salbiy, P2] Salbiy: ТМЦ siz saqlash
572. `TC-PRZ-MOR-003` [Ijobiy, P2] Ijobiy: ТМЦ + tex. karta bilan buyurtma, keyin o'chirish

### P07 · Производство · Технологические операции

573. `TC-PRZ-MNF-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
574. `TC-PRZ-MNF-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
575. `TC-PRZ-MNF-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
576. `TC-PRZ-MNF-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
577. `TC-PRZ-MNF-006` [Validatsiya, P2] Salbiy: majburiy maydonlarsiz «Черновик»
578. `TC-PRZ-MNF-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
579. + `TC-PRZ-MNF-007` [Ijobiy, P2] Ijobiy: QA- qoralama yaratish va o'chirish (Завершить/Проводки siz)

### P07 · Производство · Производственные задания

580. `TC-PRZ-TSK-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
581. `TC-PRZ-TSK-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
582. `TC-PRZ-TSK-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P07 · Производство · Заказы кодов маркировки

583. `TC-PRZ-MKO-001` [Smoke, P2] Smoke: ro'yxat ochiladi
584. `TC-PRZ-MKO-002` [UI, P2] Yaratish formasi: yorliqlar ruscha
585. `TC-PRZ-MKO-003` [Validatsiya, P2] Validatsiya: guruh tanlanmasa saqlanmaydi

### P07 · Производство · Отчет о нанесении

586. `TC-PRZ-MUR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
587. `TC-PRZ-MUR-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
588. `TC-PRZ-MUR-004` [UI, P3] Formada saqlash tugmasi
589. `TC-PRZ-MUR-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P07 · Производство · Ввод производственных остатков ТМЦ

590. `TC-PRZ-IMB-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
591. `TC-PRZ-IMB-002` [UI, P3] Yaratish tugmasi mavjudligi

### P07 · Производство · Обеспечение производства

592. `TC-PRZ-ANL-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P07 · Производство · Движение ТМЦ в производстве

593. `TC-PRZ-PRC-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
594. `TC-PRZ-PRC-002` [Validatsiya, P2] Validatsiya: «Номер заказа на производство» bo'sh — «Сформировать»
595. `TC-PRZ-PRC-003` [Ijobiy, P2] Ijobiy: mavjud buyurtma bo'yicha hisobot (HTML/EXCEL)

### P08 · Продажа · Планирование визитов

596. `TC-PRD-VPL-001` [Ijobiy, P2] Ro'yxat va «Установка плана» sahifasi
597. `TC-PRD-VPL-002` [Ijobiy, P3] Import (Excel shablon)

### P08 · Продажа · Планы

598. `TC-PRD-PLN-001` [Ijobiy, P2] Ro'yxat va «Установить план» — biriktirilgan/mavjud mijozlar
599. `TC-PRD-PLN-002` [Ijobiy, P2] Mijozni rejaga biriktirish va ajratish

### P08 · Продажа · Автоформирование плана визитов

600. `TC-PRD-AGP-001` [Smoke, P2] Forma: parametrlar va tugmalar
601. `TC-PRD-AGP-002` [Validatsiya, P3] Validatsiya: ish zonasi tanlanmasa «Продолжить»
602. `TC-PRD-AGP-003` [Ijobiy, P3] Reja taklifi hisoblanadi (saqlamasdan)

### P08 · Продажа · Визиты

603. `TC-PRD-VIS-001` [Smoke, P1] Ro'yxat ochiladi: ustunlar, hisoblagich, qator amallari
604. `TC-PRD-VIS-002` [Ijobiy, P1] Ko'rish sahifasi: asosiy maydonlar va 16 ta tab xatosiz
605. `TC-PRD-VIS-003` [Ijobiy, P2] Qidiruv va filtr (Клиент, Статус) bo'yicha saralash
606. + `TC-PRD-VIS-004` [Ijobiy, P2] Vizit statusini o'zgartirish va izoh qo'shish

### P08 · Продажа · Архив визитов

607. `TC-PRD-VAR-001` [Smoke, P2] Arxiv ro'yxati va ko'rish
608. `TC-PRD-VAR-002` [Ijobiy, P3] «Восстановить» — vizit arxivdan qaytadi

### P08 · Продажа · Фото- и видеоотчеты

609. `TC-PRD-PVG-001` [Smoke, P2] Galereya: filtr maydonlari va tablar
610. `TC-PRD-PVG-002` [Ijobiy, P3] Filtr → Применить: fotolar ko'rsatiladi, rasmni kattalashtirish

### P08 · Продажа · Отслеживание пользователей

611. `TC-PRD-ULOC-001` [Smoke, P2] Sahifa: majburiy parametrlar va tablar
612. `TC-PRD-ULOC-002` [Validatsiya, P3] Validatsiya: «Пользователи *» bo'sh bo'lsa «Обновить»
613. `TC-PRD-ULOC-003` [Ijobiy, P2] Foydalanuvchi va sana tanlab — xaritada marshrut/vizitlar

### P08 · Продажа · Отслеживание мобильных представителей

614. `TC-PRD-UTR-001` [Smoke, P3] Sahifa ochiladi

### P08 · Продажа · Отслеживание оборудования

615. `TC-PRD-EQR-001` [Ijobiy, P2] Ro'yxat va ko'rish (tablar)
616. `TC-PRD-EQR-002` [Ijobiy, P3] «Архивировать успешные» — muammosiz tekshiruvlar arxivga o'tadi

### P08 · Продажа · Заявки на заказ

617. `TC-PRD-ORQ-001` [Smoke, P2] Ro'yxat ochiladi

### P08 · Продажа · Заказы

618. `TC-PRD-ORD-001` [Smoke, P1] Ro'yxat ochiladi, yaratish tugmalari
619. `TC-PRD-ORD-002` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz «Далее»
620. + `TC-PRD-ORD-003` [Ijobiy, P1] Qoralama buyurtma: yaratish → ko'rish → tahrir → bekor/o'chirish

### P08 · Продажа · Архив и отмененные заказы

621. `TC-PRD-ORH-001` [Smoke, P3] Arxiv ro'yxati va filtr paneli
622. `TC-PRD-ORH-002` [Smoke, P3] Bekor qilingan buyurtmalar ro'yxati

### P08 · Продажа · Возвраты

623. `TC-PRD-RET-001` [Smoke, P1] Ro'yxat, qator amallari (Черновик)
624. `TC-PRD-RET-007` [UI, P3] Status menyusi: Архив / Отправлено
625. `TC-PRD-RET-009` [UI, P3] Jadval kataklarida sana/vaqt butun ko'rinadi
626. `TC-PRD-RET-014` [UI, P3] Tarjima fayli (return+add.json) yuklanadi
627. `TC-PRD-RET-002` [Validatsiya, P1] Validatsiya: 1-qadam majburiy maydonlari
628. `TC-PRD-RET-003` [Validatsiya, P1] Validatsiya: ТМЦ qo'shilmasa «Далее»
629. `TC-PRD-RET-005` [Ijobiy, P1] Ko'rish: asosiy maydonlar va ТМЦ jadvali
630. `TC-PRD-RET-006` [Ijobiy, P2] Tahrir: faqat Примечание o'zgartiriladi → saqlanadi
631. + `TC-PRD-RET-004` [Ijobiy, P1] Yaratish: Тип цены → narx avtomatik → Черновик → ro'yxat
632. + `TC-PRD-RET-008` [Ijobiy, P1] Qoralama qaytarishni o'chirish
633. `TC-PRD-RET-010` [Bug, P2] Validatsiya: narx yo'q bo'lsa tushunarli xabar
634. `TC-PRD-RET-011` [Bug, P1] ТМЦ miqdorini o'zgartirib saqlash
635. `TC-PRD-RET-012` [Bug, P2] Ko'rishda Примечание va qo'shimcha maydonlar ko'rinadi
636. `TC-PRD-RET-013` [Bug, P3] Штат ro'yxati sarlavhalari tarjima qilingan

### P08 · Продажа · Взаиморасчеты с клиентами

637. `TC-PRD-OFS-001` [Smoke, P2] Ro'yxat, «Дебиторы», «История взаиморасчетов»

### P09 · Оборудование · Заявки на оборудование

638. `TC-OBR-REQ-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
639. `TC-OBR-REQ-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
640. `TC-OBR-REQ-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
641. + `TC-OBR-REQ-004` [Ijobiy, P2] «Установить» / «Демонтировать» — o'rnatish/yechish so'rovi yaratish

### P09 · Оборудование · Заявки на перемещения

642. `TC-OBR-MOV-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
643. `TC-OBR-MOV-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
644. `TC-OBR-MOV-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
645. `TC-OBR-MOV-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
646. `TC-OBR-MOV-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
647. + `TC-OBR-MOV-006` [Ijobiy, P2] Yaratish: mijozdan mijozga uskuna ko'chirish

### P09 · Оборудование · Межорг. перемещение оборудования

648. `TC-OBR-FMV-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
649. `TC-OBR-TMV-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
650. `TC-OBR-FMV-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
651. `TC-OBR-FMV-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P09 · Оборудование · Заявки на ремонт

652. `TC-OBR-RPR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
653. `TC-OBR-RPR-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
654. `TC-OBR-RPR-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P09 · Оборудование · Остатки по рекламному оборудованию

655. `TC-OBR-BAL-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
656. `TC-OBR-BAL-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi

### P09 · Оборудование · Конструктор отчетов по заявкам

657. `TC-OBR-RPT-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
658. `TC-OBR-RPT-002` [Validatsiya, P3] Validatsiya: satr/ustun tanlanmasa HTML

### P10 · Финансы · Оплаты от клиентов

659. `TC-FIN-CIN-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
660. `TC-FIN-CIN-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
661. `TC-FIN-CIN-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
662. `TC-FIN-CIN-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
663. `TC-FIN-CIN-006` [Salbiy, P2] Salbiy: manfiy/nol summa
664. `TC-FIN-CIN-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P10 · Финансы · Оплаты поставщикам

665. `TC-FIN-COU-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
666. `TC-FIN-COU-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
667. `TC-FIN-COU-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
668. `TC-FIN-COU-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
669. `TC-FIN-COU-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P10 · Финансы · Кассовые документы

670. `TC-FIN-CSH-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
671. `TC-FIN-CSH-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
672. `TC-FIN-CSH-004` [UI, P3] «Создать» menyusi variantlari
673. `TC-FIN-CSH-005` [Validatsiya, P1] Validatsiya: bo'sh forma «Сохранить»
674. `TC-FIN-CSH-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
675. + `TC-FIN-CSH-006` [Ijobiy, P2] Ijobiy: QA- hujjat yaratish (provodkasiz) va o'chirish

### P10 · Финансы · Банковские выписки

676. `TC-FIN-BNK-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
677. `TC-FIN-BNK-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
678. `TC-FIN-BNK-004` [UI, P3] «Создать» menyusi variantlari
679. `TC-FIN-BNK-005` [Validatsiya, P1] Validatsiya: bo'sh forma «Сохранить»
680. `TC-FIN-BNK-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
681. + `TC-FIN-BNK-006` [Ijobiy, P2] Ijobiy: QA- hujjat yaratish (provodkasiz) va o'chirish

### P10 · Финансы · Документы чековой книжки

682. `TC-FIN-CHB-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
683. `TC-FIN-CHB-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
684. `TC-FIN-CHB-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P10 · Финансы · Платежные поручения

685. `TC-FIN-APE-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
686. `TC-FIN-APE-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
687. `TC-FIN-APE-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P10 · Финансы · Платежные требования

688. `TC-FIN-API-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
689. `TC-FIN-API-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
690. `TC-FIN-API-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P10 · Финансы · Мои заявки

691. `TC-FIN-MRQ-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
692. `TC-FIN-MRQ-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
693. `TC-FIN-MRQ-004` [UI, P3] «Создать» menyusi variantlari
694. `TC-FIN-MRQ-005` [Validatsiya, P1] Validatsiya: bo'sh forma «Сохранить»
695. `TC-FIN-MRQ-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
696. + `TC-FIN-MRQ-006` [Ijobiy, P2] Ijobiy: QA- hujjat yaratish (provodkasiz) va o'chirish

### P10 · Финансы · Согласование

697. `TC-FIN-APR-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
698. `TC-FIN-APR-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
699. `TC-FIN-APR-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P10 · Финансы · Оплаты (денежный поток)

700. `TC-FIN-RPY-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
701. `TC-FIN-RPY-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
702. `TC-FIN-RPY-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P10 · Финансы · Запросы об оплате

703. `TC-FIN-PRQ-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
704. `TC-FIN-PRQ-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
705. `TC-FIN-PRQ-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P10 · Финансы · Ручные операции

706. `TC-FIN-MOP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
707. `TC-FIN-MOP-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
708. `TC-FIN-MOP-004` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
709. `TC-FIN-MOP-005` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi
710. `TC-FIN-MOP-006` [Salbiy, P2] Salbiy: Дебет = Кредит (bir xil hisob)
711. `TC-FIN-MOP-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P10 · Финансы · Уставный капитал

712. `TC-FIN-CAP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
713. `TC-FIN-CAP-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
714. `TC-FIN-CAP-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P10 · Финансы · Взаиморасчеты

715. `TC-FIN-OFS-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
716. `TC-FIN-OFS-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
717. `TC-FIN-OFS-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P10 · Финансы · Перекидка аванса

718. `TC-FIN-RAL-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
719. `TC-FIN-RAL-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
720. `TC-FIN-RAL-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P10 · Финансы · Переоценки валют

721. `TC-FIN-REV-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
722. `TC-FIN-REV-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
723. `TC-FIN-REV-003` [Validatsiya, P2] Validatsiya: majburiy maydonlarsiz saqlash rad etiladi

### P10 · Финансы · Документооборот

724. `TC-FIN-SGN-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar

### P11 · Кадры и зарплата · Расчеты зарплаты

725. `TC-KDR-BOK-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
726. `TC-KDR-BOK-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
727. `TC-KDR-BOK-004` [UI, P3] «Создать» menyusi variantlari
728. `TC-KDR-BOK-005` [Validatsiya, P1] Validatsiya: xodimlarsiz saqlash
729. `TC-KDR-BOK-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar
730. + `TC-KDR-BOK-006` [Ijobiy, P2] Ijobiy: QA- hisob-kitob (Провести siz) yaratish va o'chirish

### P11 · Кадры и зарплата · Выплаты

731. `TC-KDR-PAY-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
732. `TC-KDR-PAY-002` [UI, P3] Qator bosilganda amal tugmalari chiqadi
733. `TC-KDR-PAY-004` [UI, P3] «Создать» menyusi variantlari
734. `TC-KDR-PAY-006` [UI, P3] «Добавить аванс» formasi ochiladi
735. `TC-KDR-PAY-005` [Validatsiya, P1] Validatsiya: «Касса» siz saqlash
736. `TC-KDR-PAY-003` [Ijobiy, P2] Ko'rish sahifasi: maydonlar va tablar

### P11 · Кадры и зарплата · Бонусная система

737. `TC-KDR-BON-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
738. `TC-KDR-BON-002` [UI, P2] Yaratish formasi: maydonlar, majburiy belgilar, tugmalar
739. `TC-KDR-BON-004` [UI, P3] «Результат бонусной системы» tabi
740. `TC-KDR-BON-003` [Validatsiya, P2] Validatsiya: bo'sh saqlash

### P12 · Склад · Hisobotlar

741. `TC-SKL-REP-004` [UI, P3] Sozlama yorliqlari tarjima qilingan
742. `TC-SKL-REP-007` [Validatsiya, P2] Validatsiya: satr/ustun tanlanmasa xabar
743. `TC-SKL-REP-012` [Salbiy, P3] «История» tabi faqat shu hisobot yozuvlarini ko'rsatadi
744. `TC-SKL-REP-001` [Ijobiy, P1] Excel (Кол-во) — qiymatlar Остатки ТМЦ ga mos
745. `TC-SKL-REP-002` [Ijobiy, P3] Summa varianti
746. `TC-SKL-REP-005` [Ijobiy, P1] Hisobot ma'lumot bilan yaratiladi
747. `TC-SKL-REP-008` [Ijobiy, P1] HTML/EXCEL natija ma'lumotlarga mos
748. `TC-SKL-REP-009` [Ijobiy, P2] Shablon: saqlash / yuklash / o'chirish
749. `TC-SKL-REP-011` [Ijobiy, P2] Sahifada va Excelda hisobot
750. `TC-SKL-REP-003` [Bug, P2] TMS-2 bron qiymati Остатки ТМЦ ga mos
751. `TC-SKL-REP-006` [Bug, P2] Validatsiya: davr teskari
752. `TC-SKL-REP-010` [Bug, P3] Toolbar va yorliqlar bir xil

### P12 · Торговый маркетинг · Отчеты

753. `TC-TM-REP-GEN-001` [Validatsiya, P2] Validatsiya: boshlanish sanasi tugash sanasidan keyin
754. `TC-TM-REP-MBI-001` [Validatsiya, P2] Validatsiya: hech narsa tanlanmagan
755. `TC-TM-REP-ASS-001` [Ijobiy, P1] Hisobotni shakllantirish (HTML)
756. `TC-TM-REP-CMP-001` [Ijobiy, P1] Hisobotni shakllantirish (HTML)
757. `TC-TM-REP-DSP-001` [Ijobiy, P1] Hisobotni shakllantirish (HTML)
758. `TC-TM-REP-MBI-002` [Ijobiy, P2] Konstruktorda hisobot tuzish (drag-drop)
759. `TC-TM-REP-MER-001` [Ijobiy, P2] Клиенты / Визиты / КПЭ — CSV fayllar
760. `TC-TM-REP-PHO-001` [Ijobiy, P2] Foto/video eksporti (zip)
761. `TC-TM-REP-PLG-001` [Ijobiy, P1] Hisobotni shakllantirish (HTML)
762. `TC-TM-REP-PRC-001` [Ijobiy, P1] Hisobotni shakllantirish (HTML)
763. `TC-TM-REP-SCR-001` [Ijobiy, P1] Hisobotni shakllantirish (HTML)
764. `TC-TM-REP-SHP-001` [Ijobiy, P1] Hisobotni shakllantirish (HTML)
765. `TC-TM-REP-SHS-001` [Ijobiy, P1] Hisobotni shakllantirish (HTML)
766. `TC-TM-REP-SHS-002` [Ijobiy, P2] EXCEL / CSV / XML / HTML formatlari
767. `TC-TM-REP-STS-001` [Ijobiy, P1] Hisobotni shakllantirish (HTML)
768. `TC-TM-REP-UNA-001` [Bug, P3] Hisobot sarlavhalari tarjima qilingan

### P12 · Торговый маркетинг · КПЭ: Дашборд по КПЭ

769. `TC-TM-DSH-001` [Ijobiy, P1] Joriy oy uchun dashboard
770. `TC-TM-DSH-002` [Ijobiy, P2] Boshqa oy uchun (Июнь 2026)
771. `TC-TM-DSH-003` [Regressiya, P2] Eski versiya bilan solishtirish

### P12 · Продажа · Отчеты по продажам

772. `TC-PRD-REP-002` [Smoke, P3] Sahifa va «Сформировать»
773. `TC-PRD-REP-008` [Smoke, P3] Konstruktor ochiladi
774. `TC-PRD-REP-004` [Validatsiya, P2] Validatsiya: boshlanish > tugash (Tab bilan kiritilganda)
775. `TC-PRD-REP-009` [Validatsiya, P2] Validatsiya: majburiy sana bo'sh bo'lsa xabar
776. `TC-PRD-REP-001` [Ijobiy, P2] Savdo dashboardi: parametrlar va «Сформировать»
777. `TC-PRD-REP-003` [Ijobiy, P1] Hisobot: 01.09–28.09 standart davr
778. `TC-PRD-REP-006` [Ijobiy, P2] Excel hisobot (Дата = bugun)
779. `TC-PRD-REP-007` [Ijobiy, P2] Excel hisobot (01.09–28.09)
780. `TC-PRD-REP-005` [Bug, P2] Sana yozib Esc bosilganda ko'rinadigan va ishlatiladigan qiymat bir xil

### P12 · Продажа · Отчеты по визитам

781. `TC-PRD-REPV-001` [Ijobiy, P2] Hisobot (01.09–28.09)
782. `TC-PRD-REPV-002` [Ijobiy, P2] Hisobot (01.09–28.09)
783. `TC-PRD-REPV-003` [Ijobiy, P2] Hisobot yangi oynada (htmla)
784. `TC-PRD-REPV-004` [Ijobiy, P3] Hisobot (Дата = bugun)
785. `TC-PRD-REPV-005` [Ijobiy, P3] Konstruktor: validatsiya va HTML

### P12 · Кадры и зарплата · Отчёт по начислениям и выплатам персоналу

786. `TC-KDR-REP-001` [Smoke, P2] Sahifa xatosiz ochiladi: ustunlar/parametrlar va tugmalar
787. `TC-KDR-REP-003` [Validatsiya, P3] Validatsiya: «Месяц» bo'sh bo'lsa
788. `TC-KDR-REP-002` [Ijobiy, P1] Ijobiy: joriy oy bo'yicha hisobot

### P12 · Финансы · Дашборд по финансам

789. `TC-FIN-DSH-001` [Smoke, P2] Smoke: parametrlar va tugmalar

### P12 · Финансы · Конструктор отчетов по финансам

790. `TC-FIN-MBI-001` [Smoke, P2] Smoke: parametrlar va tugmalar

### P12 · Финансы · Акт-сверки

791. `TC-FIN-RCA-001` [Smoke, P2] Smoke: parametrlar va tugmalar
792. `TC-FIN-RCA-003` [Validatsiya, P2] Validatsiya: «Контрагент» tanlanmasa
793. `TC-FIN-RCA-002` [Ijobiy, P2] Ijobiy: majburiy parametrlar bilan «Сформировать»

### P12 · Финансы · Оборотно-сальдовая ведомость

794. `TC-FIN-OSV-001` [Smoke, P2] Smoke: parametrlar va tugmalar
795. `TC-FIN-OSV-002` [Ijobiy, P1] Ijobiy: standart parametrlar bilan «Сформировать»

### P12 · Финансы · Оборотно-сальдовая ведомость(BETA)

796. `TC-FIN-OSB-001` [Smoke, P2] Smoke: parametrlar va tugmalar
797. `TC-FIN-OSB-002` [Ijobiy, P1] Ijobiy: standart parametrlar bilan «Сформировать»

### P12 · Финансы · Оборотно-сальдовая ведомость по счету

798. `TC-FIN-OSC-001` [Smoke, P2] Smoke: parametrlar va tugmalar
799. `TC-FIN-OSC-002` [Ijobiy, P2] Ijobiy: majburiy parametrlar bilan «Сформировать»

### P12 · Финансы · Проводки счетов

800. `TC-FIN-TRN-001` [Smoke, P2] Smoke: parametrlar va tugmalar
801. `TC-FIN-TRN-002` [Ijobiy, P2] Ijobiy: majburiy parametrlar bilan «Сформировать»

### P12 · Финансы · Карточка счета

802. `TC-FIN-CCD-001` [Smoke, P2] Smoke: parametrlar va tugmalar
803. `TC-FIN-CCD-002` [Ijobiy, P2] Ijobiy: majburiy parametrlar bilan «Сформировать»

### P12 · Финансы · Анализ счета

804. `TC-FIN-CAN-001` [Smoke, P2] Smoke: parametrlar va tugmalar
805. `TC-FIN-CAN-002` [Ijobiy, P2] Ijobiy: majburiy parametrlar bilan «Сформировать»

### P12 · Финансы · Прибыль и убыток (PnL)

806. `TC-FIN-PNL-001` [Smoke, P2] Smoke: parametrlar va tugmalar
807. `TC-FIN-PNL-002` [Ijobiy, P1] Ijobiy: standart parametrlar bilan «Сформировать»

### P12 · Финансы · Отчет о прибылях и убытках (БЕТА)

808. `TC-FIN-PL2-001` [Smoke, P2] Smoke: parametrlar va tugmalar
809. `TC-FIN-PL2-002` [Ijobiy, P2] Ijobiy: majburiy parametrlar bilan «Сформировать»

### P12 · Финансы · Отчет о прибылях и убытках

810. `TC-FIN-PL3-001` [Smoke, P2] Smoke: parametrlar va tugmalar

### P12 · Финансы · Отчет о движении денежных средств (БЕТА)

811. `TC-FIN-SCF-001` [Smoke, P2] Smoke: parametrlar va tugmalar
812. `TC-FIN-SCF-002` [Ijobiy, P1] Ijobiy: standart parametrlar bilan «Сформировать»

### P12 · Финансы · Денежный поток

813. `TC-FIN-CFL-001` [Smoke, P2] Smoke: parametrlar va tugmalar
814. `TC-FIN-CFL-002` [Ijobiy, P1] Ijobiy: standart parametrlar bilan «Сформировать»

### P12 · Финансы · Оплаты (отчет)

815. `TC-FIN-RPM-001` [Smoke, P2] Smoke: parametrlar va tugmalar
816. `TC-FIN-RPM-002` [Ijobiy, P2] Ijobiy: majburiy parametrlar bilan «Сформировать»

### P12 · Финансы · Отчет по должникам

817. `TC-FIN-DBT-001` [Smoke, P2] Smoke: parametrlar va tugmalar
818. `TC-FIN-DBT-003` [Validatsiya, P2] Validatsiya: «Дата» bo'sh — «Сформировать»
819. `TC-FIN-DBT-002` [Ijobiy, P2] Ijobiy: majburiy parametrlar bilan «Сформировать»

### P12 · Финансы · Обороты по контрагентам

820. `TC-FIN-PTO-001` [Smoke, P2] Smoke: parametrlar va tugmalar
821. `TC-FIN-PTO-002` [Ijobiy, P2] Ijobiy: majburiy parametrlar bilan «Сформировать»

### P12 · Финансы · Бухгалтерский баланс

822. `TC-FIN-BLS-001` [Smoke, P2] Smoke: parametrlar va tugmalar
823. `TC-FIN-BLS-002` [Ijobiy, P1] Ijobiy: standart parametrlar bilan «Сформировать»

### P12 · Финансы · Журнал документов

824. `TC-FIN-JRN-001` [Smoke, P2] Smoke: parametrlar va tugmalar

### P13 · Склад · Umumiy

825. `TC-SKL-GEN-001` [Smoke, P1] Smoke: «Склад» menyusidagi barcha sahifalar xatosiz ochiladi
826. `TC-SKL-GEN-002` [Smoke, P2] Menyu bandlari yonidagi «+» yaratish formalarini ochadi
827. `TC-SKL-GEN-004` [Validatsiya, P1] Majburiy maydonlarsiz saqlash rad etiladi (umumiy qoida)
828. `TC-SKL-GEN-003` [Ijobiy, P2] Ro'yxat: qidiruv, filtr, saralash, sahifalash
829. `TC-SKL-GEN-005` [Ijobiy, P3] Saqlanmagan formadan «Закрыть» — ro'yxatga qaytadi, hech narsa saqlanmaydi
830. `TC-SKL-GEN-006` [Bug, P2] Sessiya tugaganda login sahifasiga yo'naltiradi
831. `TC-SKL-GEN-007` [Bug, P2] URL orqali ochilgan formada «Закрыть» bor, saqlashdan keyin ro'yxatga qaytadi
832. `TC-SKL-GEN-008` [Bug, P2] So'z/sonlar o'rtasidan bo'linmaydi
833. `TC-SKL-GEN-009` [Bug, P2] Barcha formalarda son formati bir xil
834. `TC-SKL-GEN-010` [Bug, P3] Tugma bosilganda sabab aytiladi (3 joy)
835. `TC-SKL-GEN-011` [Bug, P3] Tarjima qilinmagan matnlar va i18n 404 yo'q
836. `TC-SKL-GEN-012` [Bug, P3] Matn va grammatika xatolari yo'q

### P13 · Торговый маркетинг · Umumiy

837. `TC-TM-GEN-001` [Smoke, P1] Smoke: modul menyusidagi barcha 36 sahifa xatosiz ochiladi
838. `TC-TM-GEN-002` [Smoke, P2] Menyudagi «+» tugmalari yaratish formalarini ochadi (12 ta)
839. `TC-TM-GEN-003` [UI, P3] Menyu «+» orqali ochilgan formada «Закрыть» tugmasi bor
840. `TC-TM-GEN-004` [UI, P3] Menyu «+» nomi, forma sarlavhasi va menyu bandi bir xil
841. `TC-TM-GEN-005` [UI, P3] «+add» formalar uchun tarjima fayllari yuklanadi (404 yo'q)
842. `TC-TM-GEN-006` [UI, P3] Tasdiqlash oynalari rus tilida va bir xil ko'rinishda
843. `TC-TM-GEN-007` [UI, P3] Tarjimasiz kalitlar va imlo xatolari yo'q
844. `TC-TM-GEN-008` [Salbiy, P2] Sessiya tugaganda login / parol oynasi chiqadi

### P13 · Продажа · Umumiy

845. `TC-PRD-GEN-001` [Smoke, P1] Smoke: modulning 26 ta menyu sahifasi xatosiz ochiladi
846. `TC-PRD-GEN-002` [Bug, P3] Sarlavha va tugma matnlari bir xil va to'g'ri

### P13 · Справочники · Umumiy

847. `TC-SPR-GEN-003` [Smoke, P1] Smoke: modulning 36 ta menyu sahifasi xatosiz ochiladi
848. `TC-SPR-GEN-001` [Bug, P3] Tarjima fayllari (+add.json) yuklanadi
849. `TC-SPR-GEN-002` [Bug, P3] Sarlavha/yorliq/amal nomlari bir xil

### P13 · Оборудование · Umumiy

850. `TC-OBR-GEN-001` [Bug, P3] Menyu band nomi imlo xatosiz
851. `TC-OBR-GEN-002` [Bug, P3] Tarjima fayllari (+add.json) yuklanadi
852. `TC-OBR-GEN-003` [Bug, P3] Sarlavha/amal nomlari bir xil

### P13 · Производство · Umumiy

853. `TC-PRZ-GEN-001` [Bug, P3] Tarjima fayllari (+add.json) yuklanadi
854. `TC-PRZ-GEN-002` [Bug, P3] Sarlavha va yorliqlar imlo xatosiz

### P13 · Кадры и зарплата · Umumiy

855. `TC-KDR-GEN-001` [Bug, P3] Tarjima fayllari (+add.json) yuklanadi
856. `TC-KDR-GEN-002` [Bug, P3] Yorliq va sarlavhalar imlo xatosiz

### P13 · Финансы · Umumiy

857. `TC-FIN-GEN-001` [Bug, P3] Tarjima fayllari (+add.json) yuklanadi
858. `TC-FIN-GEN-002` [Bug, P3] Sarlavha, yorliq va amal nomlari bir xil va xatosiz