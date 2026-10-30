# PROMPT — Ko'p rolli E2E biznes senariy va doimiy test ma'lumotlari strategiyasi

> Holat: **vazifa (bajarilmagan)**. Yozilgan: 30.10.2026. Ijrochi: Cowork'dagi Claude (qo'lda qism, rejalar) va Claude Code (avtotest qismi, `3_Avtotest`).
> Asos: 30.10 dagi bitta-akkauntli E2E yugurish — `Regression/Test_caselar/10_E2E/01_Xarid_sotuv_tolov_sikli/test_cases.md`, `_Claude/tarix/2026-10-30_e2e_senariy/yugurish.md`.

---

## A. Muammo

1. 30.10 dagi E2E senariyni **mohir@xan** (to'liq huquqli administrator) bajardi. Shuning uchun real biznesdagi rol cheklovlari va topshirish nuqtalari tekshirilmadi: kim yaratadi, kim tasdiqlaydi, kim nimani ko'ra oladi, kim nimani qila olmaydi.
2. Hisobot/dashboard tekshiruvlari uchun **bir necha hafta to'plangan haqiqiy ma'lumot** kerak (masalan 20 kunlik sotuv, 10 ta arxiv zakazning ИТОГО summasi, qaytarishli va aksiyali zakazlar). Har testdan keyin ma'lumot o'chirilsa, bularni tekshirib bo'lmaydi.

## B. Hozirgi qaror (foydalanuvchi, 30.10)

- QA tomonidan yaratilgan **test ma'lumotlari hozircha o'chirilmaydi** (manual ham, avtotest ham). TC-E2E-18 «Tozalash» to'xtatildi.
- Barcha hisobotlar bir marta tekshirib chiqilgandan keyin qaysi ma'lumotlar doimiy qolishi kerakligi aniqlanadi (D-7 bo'lim). Faqat shundan keyin tozalash qoidasi yoziladi.
- Arxivga o'tganda qarzdorlik «Задолженность»ga yozilishi — **to'g'ri xatti-harakat** (tasdiqlandi).

---

## C. 1-vazifa: ko'p rolli E2E senariy

### C-1. Rollar va QA foydalanuvchilar

| Rol (kod) | Login (taklif) | Biznesdagi vazifasi senariyda | Holat |
|---|---|---|---|
| admin | mohir@xan | Faqat ma'lumotnomalar va sozlama (huquq taqqoslash uchun nazorat) | bor |
| kladovshik | qa_kladovshik@xan | Запрос на закупку yaratadi; Поступление qabul qiladi; buyurtmani yig'ib «Отгружен» qiladi, nakladnoy | roles.json da, user yo'q |
| snabjenets | qa_snabjenets@xan | Запросни tasdiqlaydi (Принято); Заказ на закупку; Закупка + Провести | yangi |
| operator | qa_operator@xan | Buyurtmani tekshiradi (Новый → В обработке); yetkazilgandan keyin «Архив»; tozalash | yangi |
| agent | qa_agent@xan | Mijozga buyurtma yaratadi (Новый); faqat o'z zonasidagi mijozlarni ko'radi | roles.json da, user yo'q |
| ekspeditor | qa_ekspeditor@xan | Отгружен → Доставлен; mijozda qisman qaytarish («Отказ») | yangi |
| buxgalter | qa_buxgalter@xan | Оплата от клиента, Провести, взаимозачёт, qarz nazorati, Акт сверки | roles.json da, user yo'q |

**Muhim cheklov:** Claude foydalanuvchi/rol/huquq yaratmaydi va parol kiritmaydi (CLAUDE.md §6). Shuning uchun:

1. Claude har bir rol uchun **kerakli huquqlar ro'yxatini** (forma + amal: ko'rish/yaratish/tahrir/status/provodka) jadval qilib tayyorlaydi — `Главное → Пользователи` va rol sozlamasidagi haqiqiy nomlar bo'yicha (faqat o'qib, hech narsani o'zgartirmasdan).
2. Foydalanuvchi userlarni o'zi yaratadi (yoki aniq ruxsat beradi), har birini kerakli Штат/Рабочая зона/Склад/Касса ga bog'laydi:
    - agent → Штат (Торговый представитель), Рабочая зона «QA-REF zona»;
    - ekspeditor → Экспедитор ro'yxatida chiqishi uchun jismoniy shaxs + rol;
    - kladovshik → «QA-REF Sklad» ga MOL;
    - buxgalter → «Основная касса» (yoki QA-REF kassa).
3. Parollar faqat `3_Avtotest/.env` (`SMARTUP_PW_<ROL>`) yoki macOS Keychain'da. `config/roles.json` da `enabled: true` qilinadi va yangi rollar qo'shiladi.

### C-2. Senariy (har qadam — kim bajaradi)

| № | Qadam | Rol | Tekshiruv |
|---|---|---|---|
| 1 | Запрос на закупку (Новый) | kladovshik | Kladovshik «Принято» qila olmasligi (yoki qila olishi — huquq jadvaliga mos) |
| 2 | Запрос → Принято; Заказ на закупку | snabjenets | — |
| 3 | Закупка → Провести | snabjenets | Ta'minotchi qarzi |
| 4 | Поступление → Завершено | kladovshik | Qoldiq; snabjenets поступление qila olmasligi |
| 5 | Заказ (Новый) | agent | Agent faqat o'z zonasi mijozlarini va o'z omboridagi ТМЦ ni ko'radi; «Отгружен»/«Архив» qila olmaydi |
| 6 | Новый → В обработке | operator | — |
| 7 | В обработке → Отгружен, nakladnoy | kladovshik | Qoldiq kamayadi |
| 8 | Отгружен → Доставлен; «Отказ» (qisman qaytarish) | ekspeditor | Ekspeditor narxni o'zgartira olmaydi |
| 9 | Доставлен → Архив | operator | Задолженность paydo bo'ladi |
| 10 | Оплата от клиента → Провести (2 ta to'lov) | buxgalter | Agent to'lovni o'tkaza olmaydi (yoki faqat qoralama) |
| 11 | Hisobotlar: Взаиморасчеты, Акт сверки, Отчет по должникам | buxgalter | Raqamlar ledger bilan mos |

**Har rol uchun salbiy (RBAC) case'lar:** ruxsat etilmagan amal tugmasi ko'rinmaydi yoki bosilganda tushunarli xabar chiqadi (xom «Ошибка URL: /xtrade/b/…» emas); boshqa zonaning ma'lumoti ko'rinmaydi; menyuda ortiqcha bo'limlar yo'q. Natija — `Regression/Test_caselar/10_E2E/02_Kop_rolli_sikl/test_cases.md` (yangi) + rollar × amallar matritsasi.

**Mobil qism:** real biznesda agent va ekspeditor odatda mobil ilovada (SFA) ishlaydi. Hozircha web versiyada bajariladi; mobil versiya alohida case sifatida belgilanadi.

---

## D. 2-vazifa: doimiy test ma'lumotlari strategiyasi

### D-1. Uch qatlamli nomlash

| Prefiks | Nima | Hayoti |
|---|---|---|
| `QA-REF-` | Ma'lumotnomalar: QA zona, QA ombor, 3–5 ТМЦ, 3–4 mijoz (yuridik/jismoniy, turli narx turi va to'lov turi bilan), 2 ta'minotchi, shartnomalar, narxlar | **Hech qachon o'chirilmaydi.** Bir marta yaratiladi, har kuni qayta ishlatiladi |
| `QA-E2E-` / `SIM-` | Har kuni yaratiladigan tranzaksiyalar (xarid, buyurtma, qaytarish, to'lov) | Hozircha o'chirilmaydi; D-7 dan keyin qaror |
| `QA-TMP-` | Bir martalik salbiy/validatsiya tekshiruvlari, qoralamalar | Testning o'zida o'chirilishi mumkin |

- Har kuni yangi ТМЦ/mijoz **yaratilmaydi** — ma'lumotnomalar shishib ketmasligi uchun faqat `QA-REF-` ishlatiladi. Forma regression'ini tekshirish uchun yaratilgan ma'lumotnomalar (TC-E2E-01…07) — `QA-TMP-` (yoki nofaol qilinadi).
- 30.10 da yaratilgan `QA-E2E-*-3010` yozuvlari to'plamning **1-kuni** hisoblanadi; QA-E2E Sklad / Mijoz / ТМЦ `QA-REF-` sifatida qayta nomlanishi yoki shundayligicha ishlatilishi mumkin (qaror Claude'da, foydalanuvchiga aytiladi).
- **Izolyatsiya:** barcha QA tranzaksiyalari faqat QA-REF zona, ombor va mijozlarida. Shunda har bir hisobotni «Склад = QA-REF…» yoki «Клиент = QA-REF…» filtri bilan begona ma'lumotsiz tekshirish mumkin.

### D-2. Kunlik ma'lumot «partiyasi» (har ish kuni, kamida 1 oy)

Har kuni bir xil miqdorda, turlicha holatlarni qamrab oladigan to'plam yaratiladi (avtotest — tungi yugurishda; avtotest tayyor bo'lguncha — qo'lda yoki Cowork rejali vazifasi orqali):

| Tur | Soni/kun | Maqsad (qaysi hisobot/case) |
|---|---|---|
| Oddiy buyurtma → Архив, to'liq to'langan | 2 | Sotuv hisobotlari, arxiv ИТОГО |
| Qisman qaytarishli («Отказ») → Архив | 1 | Arxiv ИТОГО qaytarishni hisobga oladimi |
| Aksiya/chegirmali buyurtma | 1 | Aksiya summasi ИТОГОda ko'rinadimi |
| Qarzga qolgan (to'lanmagan) buyurtma | 1 | Должники, qarz muddati (aging) |
| Qisman to'langan buyurtma | 1 | Взаиморасчеты, Акт сверки |
| Bekor qilingan (Отменен) buyurtma | 0.5 (kunora) | Отмененные заказы, hisobotdan chiqishi |
| Turli to'lov turi (Наличные / Перечисление / Терминал) | aralash | Дашборд kartochkalari |
| Xarid zanjiri (закупка + поступление), ba'zan qaytarish ta'minotchiga | 1 | Материальный отчет, ta'minotchi qarzi |
| Ichki ko'chirish yoki spisaniye | 0.5 | Остатки, Общий отчет по складам |
| Mijozdan oldindan to'lov (предоплата) | kunora | Предоплата, взаимозачёт |

- Sanalar: buyurtma sanasi = shu kun, «Дата отгрузки» = shu kun (A02-16-049). Qaysi hujjatlarda o'tgan sana ruxsat etilishi alohida tekshirilsin; ruxsat etilsa — qarz «aging»i uchun bir nechta orqa sanali hujjat.
- Qoldiq yetishi uchun xarid hajmi sotuvdan katta bo'lsin (masalan haftasiga 1 katta поступление).

### D-3. Ledger — «kutilgan natija» daftari

Har yaratilgan hujjat (manual va avto) bitta qator qilib yoziladi — keyin hisobotlar shu bilan solishtiriladi:

```json
{"sana":"2026-10-30","manba":"manual|auto","rol":"agent","hujjat":"Заказ","id":"571967","nomer":"QA-TTN-3010",
 "mijoz":"QA-E2E Mijoz3010","sklad":"QA-E2E Sklad 3010","tmc":[{"kod":"QA-E2E-3010","kol":30,"narx":15000,"qaytarish":5,"chegirma":0}],
 "summa":450000,"qaytarish_summa":75000,"aksiya_summa":0,"itogo":375000,"tolov_turi":"Наличные","status":"Архив","tolangan":375000,"qarz":0}
```

- Joylashuv: avtotest — `3_Avtotest/data/ledger/ledger_<YYYY-MM>.jsonl`; qo'lda (Cowork) — `_Claude/test_data/ledger_manual.jsonl`. Sxema bir xil; hisobot tekshiruvida ikkalasi birlashtiriladi.
- 30.10 dagi yugurish ledger'ga birinchi qatorlar bo'lib kiritiladi (ma'lumot `yugurish.md` da).
- Har oy oxirida ledger'dan «kutilgan raqamlar» jadvali (kun, mijoz, ombor kesimida) generatsiya qilinadi.

### D-4. Hisobotlar ↔ ma'lumot matritsasi

Claude barcha hisobot/dashboard formalarini (Smoke test case'lardagi «Отчеты», «Дашборд», «Конструктор» bo'limlari) ro'yxat qiladi va har biri uchun yozadi: qaysi filtr bilan QA ma'lumoti ajratiladi, qaysi ledger maydonlari bilan solishtiriladi, kamida necha kunlik ma'lumot kerak. Fayl: `_Claude/test_data/hisobot_matritsa.md`. Masalan:

| Hisobot | Filtr | Solishtirish | Kerakli davr |
|---|---|---|---|
| Архив заказов (ИТОГО) | Клиент = QA-REF… | Σ itogo (qaytarish va aksiya bilan) | 10+ zakaz |
| Общий отчет по продажам | Склад = QA-REF | kun bo'yicha Σ summa | 20 kun |
| Задолженность по срокам | Клиент = QA-REF… | qarz va sana | 30+ kun |
| Материальный отчет / Остатки | Склад = QA-REF | приход/расход/qoldiq | 1 oy |
| Акт сверки | QA-REF mijoz/ta'minotchi | Σ hujjat va to'lov | 1 oy |

### D-5. Avtotestga talablar (Claude Code)

- Avtotest yaratgan ma'lumotni **o'chirmaydi** (cleanup testlari faqat `--e2e-cleanup` bilan va faqat `QA-TMP-` uchun).
- Har yaratilgan hujjat ledger'ga yoziladi (D-3).
- Bir kunda ikki marta yurganda dublikat yaratmaslik uchun — ledger'da shu kun uchun partiya bor-yo'qligini tekshiradi (`--force` bo'lmasa).
- Rollar `config/roles.json` dan; user `enabled: false` bo'lsa — qadam admin bilan bajariladi va hisobotda «rol simulyatsiya qilindi» deb belgilanadi (simulation_plan.md dagi qoida).
- Tungi tahlil (`analyze.py`) ledger'dagi kunlik partiya to'liq yaratilganini ham tekshiradi.

### D-6. Xavfsizlik va tozalikni saqlash

- Faqat QA-REF ma'lumotnomalari va QA zona/omborida ishlanadi; begona mijoz/omborga hujjat yaratilmaydi.
- Tashqi tizimlar (Faktura.uz, Фискализация, Soliq, WMS, CRPT, Telegram) — hech qachon.
- Hajm nazorati: oyiga taxminan 150–250 hujjat. Bundan oshsa — foydalanuvchiga xabar.

### D-7. Keyingi qaror nuqtasi

Barcha hisobotlar matritsa bo'yicha bir marta tekshirilgach, Claude foydalanuvchiga quyidagi ro'yxatni beradi: (a) doimiy qoladigan ma'lumotlar, (b) N kundan keyin arxivlansa/o'chirilsa bo'ladiganlar, (c) darhol o'chiriladiganlar. Tasdiqlangandan keyin CLAUDE.md va avtotestdagi tozalash qoidasi yangilanadi.

---

## E. Bajarish tartibi

1. (Claude, Cowork) Rollar × huquqlar jadvalini tayyorlash (faqat o'qish) → foydalanuvchiga berish.
2. (Foydalanuvchi) QA userlarni yaratish va bog'lash; parollarni `.env`/Keychain'ga.
3. (Claude, Cowork) `QA-REF-` ma'lumotnomalarini yaratish (30.10 dagi QA-E2E yozuvlarini qayta ishlatish imkoni bilan) → ledger va `_Claude/test_data/` papkasini boshlash.
4. (Claude, Cowork) Ko'p rolli senariyni qo'lda bir marta o'tkazish (foydalanuvchi har rol bilan kirib beradi yoki kirish sessiyasi tayyor bo'ladi) → `02_Kop_rolli_sikl/test_cases.md`, buglar.
5. (Claude Code) `claude_code_prompt_E2E.md` + shu hujjat asosida ko'p rolli avtotest va kunlik partiya generatori; ledger yozuvi.
6. (Avto, har kuni) Kunlik partiya — kamida 1 oy.
7. (Claude, Cowork) Hisobot matritsasi bo'yicha tekshiruv → D-7 qarori.
