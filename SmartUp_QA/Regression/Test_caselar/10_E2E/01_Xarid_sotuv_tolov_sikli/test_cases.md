# E2E — Xarid → Sotuv → Qaytarish → To'lov (to'liq biznes sikli) — Regression test case'lar

Muhit: https://app3.greenwhite.uz/xtrade (a2 = yangi UI `/xtrade/a2/…`, eski UI = `/xtrade/#/!<sessiya>/…`), filial **Toshkent**, foydalanuvchi mohir@xan.
Tuzilgan: 30.10.2026 (formalar xtrade'da ochib ko'rilgan, hech narsa saqlanmagan).
Maqsad: smoke emas — **har formadagi barcha input, tanlov, kalit (switch), checkbox, tab, ichki jadval va tugma** ishlashini tekshirib, so'ng hujjatlar zanjirini oxirigacha o'tkazish va har qadamda qoldiq/summa/qarzni tekshirish.

## Test case'lar ro'yxati

1-qo'lda yugurish: **30.10.2026**, mohir@xan, Toshkent (Chrome). Yozuvlar nomida `<DDMM>` = 3010.

| ID | Sarlavha | Modul | UI | Muhimlik | 30.10 natija | Bug |
|---|---|---|---|---|---|---|
| [TC-E2E-01](#tc-e2e-01) | ТМЦ yaratish — barcha maydonlar va 6 ta tab | Справочники | a2 | P1 | Pass (rasm/fayl yuklanmadi) |  |
| [TC-E2E-02](#tc-e2e-02) | ТМЦ ga narx o'rnatish (Установка цен) | Справочники | a2 | P1 | Pass |  |
| [TC-E2E-03](#tc-e2e-03) | Юридическое лицо (ta'minotchi) — barcha maydonlar va 8 ta tab | Справочники | a2 | P1 | Pass (GPS/файл bundan mustasno) |  |
| [TC-E2E-04](#tc-e2e-04) | Физическое лицо (mijoz) — barcha maydonlar va 7 ta tab | Справочники | a2 | P1 | Pass |  |
| [TC-E2E-05](#tc-e2e-05) | Поставщик + ТМЦ ga ta'minotchini bog'lash | Склад | a2 | P1 | Pass |  |
| [TC-E2E-06](#tc-e2e-06) | Склад yaratish — barcha maydonlar | Склад | a2 | P1 | Pass |  |
| [TC-E2E-07](#tc-e2e-07) | Клиент (avtomatik yaratilgani) | Справочники | a2 | P1 | Pass |  |
| [TC-E2E-08](#tc-e2e-08) | Запрос на закупку | Склад | a2 | P1 | Pass |  |
| [TC-E2E-09](#tc-e2e-09) | Заказ на закупку (zaprosdan, 4 qadamli wizard) | Склад | eski | P1 | Pass |  |
| [TC-E2E-10](#tc-e2e-10) | Закупка (zakazdan) | Склад | a2 | P1 | Pass (kuzatuv) |  |
| [TC-E2E-11](#tc-e2e-11) | Поступление ТМЦ на склад | Склад | a2 | P1 | Pass |  |
| [TC-E2E-12](#tc-e2e-12) | Sotuv buyurtmasi (Заказ) yaratish | Продажа | eski | P1 | Fail | BUG-183, BUG-185 |
| [TC-E2E-13](#tc-e2e-13) | Buyurtma yetkazib berish: В обработке → Отгружен → Доставлен | Продажа | eski | P1 | Pass |  |
| [TC-E2E-14](#tc-e2e-14) | Buyurtmaning bir qismini qaytarish («Отказ») | Продажа | eski | P1 | Pass |  |
| [TC-E2E-15](#tc-e2e-15) | Buyurtmani arxivga o'tkazish, mijoz qarzi | Продажа | eski | P1 | Fail | BUG-184 |
| [TC-E2E-16](#tc-e2e-16) | Mijozdan to'lov qabul qilish, qarz yopilishi | Финансы | a2 | P1 | Pass |  |
| [TC-E2E-17](#tc-e2e-17) | Yakuniy solishtiruv: qoldiq, qarzlar, hisobotlar | Склад/Финансы | a2+eski | P1 | Pass (1–4) |  |
| [TC-E2E-18](#tc-e2e-18) | Tozalash (teskari tartibda) | — | — | P2 | To'xtatilgan (30.10 qarori: ma'lumotlar saqlanadi) |  |

## Umumiy qoidalar (har case uchun)

**Oldindan shartlar**
- Tizimga mohir@xan bilan kirilgan, filial «Toshkent». Parolni foydalanuvchi o'zi kiritadi.
- Har yozuv nomi **«QA-E2E-»** bilan boshlanadi va yugurish sanasi qo'shiladi (masalan `QA-E2E-TMS-3010`). Quyida `<DDMM>` — shu sana.
- Tashqi tizimga ketadigan tugmalar **bosilmaydi**: ИНН/ПНФЛ yonidagi «Поиск», «Синхронизировать наличие маркировки», Faktura/Soliq/WMS/CRPT/Telegram'ga yuborish.
- Boshqa foydalanuvchilarning hujjatlariga tegilmaydi.

**Har formada umumiy tekshiruvlar** (har case'ning «Forma tekshiruvi» qismida qisqa qilib «UMUMIY» deb ko'rsatilgan):
1. Bo'sh formada «Сохранить» / «Далее» → barcha `*` maydonlar qizil ramka bilan, yozuv yaratilmaydi, «Ошибка» oynasi (`/xtrade/b/…`) chiqmaydi.
2. Har tanlov (select) ro'yxati ochiladi, qidiruvga matn yozilsa filtrlaydi, tanlangan qiymat maydonda ko'rinadi, «×» bilan tozalanadi.
3. Har switch/checkbox bosilganda holati o'zgaradi va qayta bosilganda qaytadi; bog'liq maydonlar paydo bo'ladi/yo'qoladi.
4. Har tab ochiladi, tab ichidagi «Создать/Добавить» dialog/qatorni ochadi, qator qo'shiladi va o'chiriladi.
5. «Закрыть» / «Назад» saqlamasdan chiqadi (ro'yxat hisoblagichi o'zgarmaydi).
6. Saqlangandan keyin: ro'yxatda qator bor, qidiruvda nom bo'yicha topiladi; «Просмотр» da **kiritilgan har bir qiymat** ko'rinadi; «Изменить» da qiymatlar oldindan to'ldirilgan, bitta maydonni o'zgartirib saqlansa o'zgarish ko'rinadi.
7. Brauzer konsolida xato yo'q, tarmoqda 4xx/5xx yo'q, tarjima fayllari (`i18n/**.json`) 404 emas.

---

## TC-E2E-01

**ТМЦ yaratish — barcha maydonlar va 6 ta tab**

- Yo'l: Справочники → ТМЦ → «Создать» (`/xtrade/a2/anor/mr/product/inventory+add`)

**Test ma'lumotlari**

| Maydon | Qiymat |
|---|---|
| Название * | QA-E2E-TMS-<DDMM> |
| Ед. изм. * | шт |
| Альтернативное название | QA-E2E TMS alt |
| Производители | TMS maker |
| Наборы ТМЦ * | ro'yxatdagi birinchi to'plam |
| Типы ТМЦ | ☑ Товар (qolganlari: belgilab ko'rib, olib tashlang) |
| Тип кейса (1 уровень) | ro'yxatdagi birinchi kейс → «Кол-во в кейсе (1 уровень)» = 10 |
| Тип кейса (2 уровень) | 1-daraja tanlangach faollashadi → birinchi qiymat, kol-vo = 5 |
| Штрих-коды | 4780000<DDMM>01 |
| Код | QA-E2E-<DDMM> |
| Порядковый номер | 999 |
| IKPU | 00000000000000001 |
| Артикул код | QA-ART-<DDMM> |
| ТН ВЭД | 0000000000 |
| Группа маркированных товаров | **bo'sh** (CRPT bilan bog'liq) |
| Поставщики | TMS maker |
| Статус | Активный |
| Rasm | 1 ta .png (Добавить изображение) |
| Tab «Вес» | Вес нетто 1.2, Вес брутто 1.5, Литр 0.75 |
| Tab «Характеристики» | Категория, Торговая марка, My_Type, PG6–PG13 — har biridan birinchi qiymat |
| Tab «Штрих-коды» | «Добавить» → 4780000<DDMM>02 (2-shtrix-kod) |
| Tab «Файлы» | «Добавить» → .pdf, Примечание «QA fayl» |
| Tab «Ед. изм. маркированных товаров» | ochib ko'rish (qator qo'shilmaydi) |
| Tab «GTIN» | ochib ko'rish; 14 belgi haqidagi ogohlantirish matni ko'rinadi |

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | Справочники → ТМЦ → «Создать». | «ТМЦ (создание)» ochiladi; Статус = Активный; 6 ta tab tugmasi bor. |
| 2 | UMUMIY 1: bo'sh forma «Сохранить». | Название, Ед. изм., Наборы ТМЦ qizil; saqlanmaydi. |
| 3 | «Тип кейса (2 уровень)» ni 1-daraja tanlanmasdan bosing. | Maydon nofaol (disabled). |
| 4 | Jadvaldagi barcha maydonlarni to'ldiring (Типы ТМЦ checkbox'larini birma-bir yoqib-o'chirib, oxirida faqat «Товар»). | Har qiymat maydonda ko'rinadi; 1-daraja tanlangach 2-daraja faollashadi. |
| 5 | Rasm qo'shing, so'ng «Нет фото» bilan olib tashlab, qayta qo'shing. | Rasm almashadi, xato yo'q. |
| 6 | 6 ta tabni navbat bilan oching va jadvaldagi qiymatlarni kiriting; «Штрих-коды» va «Файлы» da qator qo'shib, bittasini o'chirib, qayta qo'shing. | Har tab ochiladi; qatorlar grid'da paydo bo'ladi/yo'qoladi. |
| 7 | «Сохранить». | Ro'yxatga qaytadi, xabar/xato oynasi yo'q. |
| 8 | Ro'yxatda «QA-E2E-TMS-<DDMM>» ni qidiring → qator → «Просмотр». | Barcha maydonlar va tablar kiritilgan qiymatlar bilan; 2 ta shtrix-kod, fayl, vazn. |
| 9 | «Изменить» → Порядковый номер 998 → saqlang. | Ko'rishda 998. Tahrir formasida qo'shimcha «Новинка» checkbox'i bor. |
| 10 | Ro'yxatda qatorni bosing: «Неактивный» → «Активный». | Status o'zgaradi va qaytadi. |

**30.10 izoh:** «Кол-во в кейсе (1/2 уровень)» kейс turi tanlangach majburiy (*) bo'ladi. «Штрих-коды» tabidagi «Добавить» dialogi shtrix-kod rasmini ko'rsatadi, yangi kod asosiy maydonga ham qo'shiladi. Ko'rish sahifasining «Основная информация»sida Ед. изм., shtrix-kodlar, IKPU, Артикул, ТН ВЭД ko'rinmaydi. To'g'ridan URL bilan ochilgan create formalar saqlangach dashboard'ga qaytadi (barcha a2 formalarda).

---

## TC-E2E-02

**ТМЦ ga narx o'rnatish (Установка цен)**

- Yo'l: Справочники → Цены (`/xtrade/a2/anor/mkr/price_type_list`)
- Oldindan: TC-E2E-01.

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | Ro'yxatda tablarni oching: Цены / Типы оплат / Скидки/наценки. | Har tab xatosiz. |
| 2 | «Sotish sum» qatorini bosing. | Amallar: Просмотр, Изменить, Ценник, Установка цен, Прикрепление, Настройка. |
| 3 | «Установка цен» → QA-E2E-TMS-<DDMM> uchun narx **15 000** → saqlang. | Saqlanadi. |
| 4 | «Olish sum» → «Установка цен» → **10 000**. | Saqlanadi. |
| 5 | «Sotish sum» → «Просмотр». | QA-E2E-TMS narxi 15 000. |

---

## TC-E2E-03

**Юридическое лицо (ta'minotchi) — barcha maydonlar va 8 ta tab**

- Yo'l: Справочники → Юридические лица → «Создать» (`/xtrade/a2/anor/mr/person/legal_person+add`)

**Test ma'lumotlari**

| Maydon | Qiymat |
|---|---|
| Полное название * | QA-E2E Postavshik MChJ <DDMM> |
| Альтернативное название | QA-E2E Postavshik |
| Код / Штрих-код / Почтовый индекс | QA-E2E-YUR-<DDMM> / 4780000<DDMM>11 / 100000 |
| Веб-сайт / Телефон / Телеграм / Email | qa-e2e.uz / +998900000001 / @qa_e2e / qa.e2e@example.com |
| Собственник / Руководитель | ro'yxatdagi birinchi qiymat |
| Рабочие зоны | Room - Yashnobod |
| ИНН / ОКЭД / Рег. код НДС | 309990001 / 46900 / 326000000001 (ИНН yonidagi «Поиск» **bosilmaydi**) |
| Виды деятельности / Регион | birinchi qiymat / Toshkent |
| GPS | xarita tugmasi orqali nuqta tanlash, so'ng 🗑 bilan tozalab qayta tanlash |
| Адрес / Ориентир / Почтовый адрес | Toshkent, QA ko'chasi 1 / QA mo'ljal / 100000, Toshkent |
| ☑ Сохранить в качестве поставщика | ha |
| ☐ Сохранить в качестве клиента | yo'q (bosib ko'rib, qaytarish) |
| Rasm | «Выбрать файл» → .png |
| Tab Характеристики | **qa xyu * (majburiy)**, Группа, Категория, Тип, Характеристика AAA/BBB/CCC — birinchi qiymatlar |
| Tab Расчетный счет | «Создать» → dialog: Название счета * «QA-E2E hisob», МФО 00014, Банк * birinchi, Расчетный счет * 20208000900000000001, Основной = Да, Статус = Активный, Валюта * Узбекский сум, Примечание «QA» → «Создать и закрыть» |
| Tab Контактные лица | «Создать» → Ф.И.О. QA Kontakt, Должность, Телефон, Дата рождения 01.01.1990, Примечание |
| Tab Файлы | 1 ta .pdf |
| Tab Договор | «Создать» → Номер QA-E2E-DOG-<DDMM>, sana bugun, Сумма 10 000 000, Срок +1 yil, Основной |
| Tab Примечание | «QA-E2E izoh» |
| Tab Руководящие должности | Директор: Имя/Фамилия/Отчество; Бухгалтер: Имя/Фамилия/Отчество («Поиск» bosilmaydi) |
| Tab График доставки | Пн–Пт belgilash, Временное окно 09:00–18:00 |

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | Formani oching; UMUMIY 1. | «Полное название» va «qa xyu» qizil. |
| 2 | Asosiy maydonlarni to'ldiring; GPS tanlash/tozalash. | Qiymatlar ko'rinadi; GPS maydoni faqat o'qish uchun. |
| 3 | 8 ta tabni navbat bilan to'ldiring. Rasch. hisob dialogida avval «Закрыть» (saqlamasdan), keyin «Создать» (dialog ochiq qoladi), so'ng «Создать и закрыть». | Har tab ochiladi; dialog tugmalari to'g'ri ishlaydi; gridlarda qatorlar. |
| 4 | «Сохранить». | Saqlanadi. |
| 5 | Ro'yxatda qidirib «Просмотр». | Barcha maydon va tab qiymatlari saqlangan. |
| 6 | Склад → Поставщики ro'yxatida qidiring. | «Сохранить в качестве поставщика» tufayli ta'minotchi avtomatik yaratiladi (30.10: supplier_id 405210). |

**30.10 izoh:** «Собственник» tanlanganda «Материально ответственное лицо» kaliti paydo bo'ladi. «Виды деятельности» ro'yxati bo'sh (tizimda qiymat yo'q). Kontakt dialogida sana maydoniga harf ham yoziladi (qizil ramka bilan). Har saqlashda «Подтверждение — Сохранить?» oynasi chiqadi.

---

## TC-E2E-04

**Физическое лицо (mijoz) — barcha maydonlar va 6 ta tab**

- Yo'l: Справочники → Физические лица → «Создать» (`/xtrade/a2/anor/mr/person/natural_person+add`)

| Maydon | Qiymat |
|---|---|
| Пол | Мужской (Женский ga o'tkazib, qaytaring) |
| Фамилия / Имя * / Отчество | QA-E2E / Mijoz<DDMM> / Testovich |
| Код | QA-E2E-FIZ-<DDMM> |
| Дата рождения | 01.01.1995 |
| Серийный номер паспорта | AA0000001 |
| Статус | Активный |
| Регион / Адрес / Почтовый адрес | Toshkent / Toshkent, QA 2 / 100000 |
| Юридическое лицо | QA-E2E Postavshik MChJ <DDMM> |
| Телефон / ИНН/ПНФЛ / Телеграм / Email / Веб-сайт | +998900000002 / 30101950000001 / @qa_mijoz / qa.mijoz@example.com / qa-mijoz.uz |
| Рабочие зоны | **Room - Yashnobod** (buyurtma uchun shart) |
| GPS | «Карта» → nuqta; «Сбросить» → qayta tanlash |
| Ответственный | birinchi qiymat |
| ☑ Клиент, ☐ Поставщик, ☐ Сотрудник | Клиент belgilanadi (qolganlarini yoqib-o'chirib ko'rish) |
| Avatar | «Выбрать файл» → .png |
| Tab Характеристики | **Группа *, Категория *** (majburiy), Тип |
| Tab Расчетный счет / Файлы / Договор / Примечание / График доставки | TC-E2E-03 dagi kabi bittadan yozuv |

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | Formani oching; UMUMIY 1. | Имя, Группа, Категория qizil. |
| 2 | Barcha maydon va tablarni to'ldiring; «Сохранить». | Saqlanadi. |
| 3 | «Просмотр» → barcha qiymatlarni solishtiring. | Mos. |
| 4 | Справочники → Клиенты ro'yxatida qidiring. | «☑ Клиент» tufayli mijoz avtomatik yaratiladi (30.10: 405211). |

**30.10 izoh:** «Имя» — autocomplete; erkin matn saqlanadi, lekin «Ничего не найдено» paneli fokus ketgach ham ochiq qoladi (sahifaning bo'sh joyini bosish kerak). «☑ Клиент» belgilansa 7-tab «Адреса доставки» paydo bo'ladi — «Добавить» dialogi: Код, *Адрес доставки короткий, *Адрес доставки полный, GPS, Статус, «Адрес доставки по умолчанию» (Да → buyurtmada avtomatik tanlanadi).

---

## TC-E2E-05

**Поставщик yaratish**

- Yo'l: Склад → Поставщики → «Создать» (`/xtrade/a2/anor/mkw/supplier+add`)
- Agar TC-E2E-03 da ta'minotchi avtomatik yaratilgan bo'lsa — bu case «Изменить» orqali o'tkaziladi.

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | Формани oching; UMUMIY 1. | «Название *» qizil. |
| 2 | «Тип поставщика»: Физическое лицо → Юридическое лицо. | «Название» ro'yxati tanlangan turdagi shaxslarni ko'rsatadi. |
| 3 | Название = QA-E2E Postavshik MChJ <DDMM>; НДС = yoqing → o'chiring → yoqing; Акциз = yoqib-o'chiring (oxiri o'chiq). | Kalitlar holati o'zgaradi. |
| 4 | «Умный поиск» tugmasini bosib ko'ring, keyin yoping. | Panel ochiladi/yopiladi. |
| 5 | «Сохранить» → ro'yxat → «Просмотр». | НДС = Нет, Акциз = Нет (30.10: arifmetikani soddalashtirish uchun НДС o'chiq qoldirildi; yoqilganda «НДС (%)» maydoni chiqadi). |
| 6 | **Majburiy:** Справочники → ТМЦ → QA-E2E-TMS → «Изменить» → «Поставщики» ga QA-E2E Postavshik qo'shing → saqlang. | Aks holda «Заказ на закупку»dagi qator «Поставщик» ro'yxatida faqat ТМЦ kartochkasidagi ta'minotchilar chiqadi va yangi ta'minotchini tanlab bo'lmaydi. |

---

## TC-E2E-06

**Склад yaratish — barcha maydonlar**

- Yo'l: Склад → Склады → «Создать» (`/xtrade/a2/anor/mkw/warehouse+add`)

| Maydon | Qiymat |
|---|---|
| Основной | o'chiq (yoqib-o'chirib ko'rish) |
| Название * / Код / Порядковый номер | QA-E2E Sklad <DDMM> / QA-E2E-WH / 999 |
| Тип склада * | birinchi qiymat |
| Материально ответственное лицо | birinchi qiymat |
| Рабочие зоны | Room - Yashnobod |
| Автотранспорт | birinchi qiymat |
| Примечание | QA-E2E ombor |
| Параметры объема | «Прямые углы» → Высота 3, Ширина 10, Длина 20 → Объем 600 (avto bo'lsa tekshiring); «Округленные углы» ga o'tib, qaytaring |
| Адрес / Ориентир / Регион / GPS | Toshkent, QA 3 / mo'ljal / Toshkent / xarita |
| Температурный режим / Влажность помещения | birinchi qiymatlar |

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | UMUMIY 1. | Название, Тип склада qizil. |
| 2 | Barcha maydonlarni to'ldiring; Объем hisobini tekshiring. | 3 × 10 × 20 = 600 (avtomatik hisoblansa). |
| 3 | «Сохранить» → «Просмотр». | Barcha qiymatlar saqlangan. |

---

## TC-E2E-07

**Клиент yaratish**

- Yo'l: Справочники → Клиенты → «Создать» (`/xtrade/a2/anor/mrf/client+add`). TC-E2E-04 da avtomatik yaratilgan bo'lsa — «Просмотр»/«Изменить» bilan tekshiriladi.

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | UMUMIY 1. | «Название *» qizil. |
| 2 | Тип клиента: Юридическое → Физическое лицо; Название = QA-E2E Mijoz<DDMM>. | Tanlanadi. |
| 3 | «Сохранить»; ro'yxatda qatorni bosing. | Amallar: Просмотреть, Изменить, Неактивный, Удалить. |
| 4 | «Просмотреть». | Tablar: Основная информация, Задачи, История изменений; Название, Тип клиента, Статус, Client ID, Создал, sana. |

---

## TC-E2E-08

**Запрос на закупку**

- Yo'l: Склад → Запросы на закупку → «Создать» (`/xtrade/a2/anor/mkw/purchase/purchase_request+add`)

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | UMUMIY 1 (ТМЦ siz ham). | Дата, Статус majburiy; ТМЦ siz saqlanmaydi. |
| 2 | Номер QA-E2E-ZR-<DDMM>, Дата bugun, Крайний срок поставки +7 kun, Примечание «QA-E2E». | Qiymatlar ko'rinadi. |
| 3 | «Подбор» → QA-E2E-TMS-<DDMM> ni tanlab yoping («Выбрать ТМЦ с заполненными данными?» → Да). | Qator qo'shiladi. |
| 4 | Qatorda Кол-во **100**, Кол-во кейсов avtomatik (100/10 = 10), Причина, Примечание. | Кейс soni qayta hisoblanadi. |
| 5 | «Импорт» tugmasini ochib, yoping (fayl yuklanmaydi). | Oyna ochiladi/yopiladi. |
| 6 | Статус = Новый → saqlang; so'ng ro'yxatda qatorni bosib «Статус ▾» → **Принято**. | Tasdiq: «Изменить статус документа QA-E2E-ZR-… на "Принято"?»; ro'yxatda «Принят». ТМЦ siz saqlash: «H02-ANOR497-001 Выберите минимум одну позицию!». «Причина» ro'yxati bo'sh. |
| 7 | «Просмотр». | ТМЦ 100 шт, barcha maydonlar. |

---

## TC-E2E-09

**Заказ на закупку (zaprosdan, 4 qadamli wizard)**

- Yo'l: eski UI — Склад → Заказы на закупку → «СОЗДАТЬ» (`#/!<sessiya>/anor/mkw/purchase/order_add`)

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | 1-qadam «Основное»: Дата заказа (avto), Дата поставки +7 kun, Валюта = Узбекский сум → «ДАЛЕЕ». | 2-qadam. |
| 2 | Avval «ЗАКРЫТЬ» ni sinab ko'ring (yangi oynada). | Saqlamasdan ro'yxatga qaytadi, yozuv qo'shilmaydi. |
| 3 | 2-qadam «ТМЦ»: «Запросы на закупку» qidiruvida QA-E2E-ZR-<DDMM> ni tanlang. | Дата запроса, Крайний срок, Примечание to'ladi; jadvalda QA-E2E-TMS × 100. |
| 4 | Qatordagi «Поставщик» = QA-E2E Postavshik, «Договор» = QA-E2E-DOG-<DDMM>. | Tanlanadi. |
| 5 | «Дополнительный подбор ТМЦ»: «Поиск ТМЦ» bilan TMS-1 × 1 qo'shing va 🗑 bilan o'chiring. | Qator qo'shiladi va o'chadi. |
| 6 | «ДАЛЕЕ» → 3-qadam «Поставщик»: Цена **10 000**, Номер карточки QA-1, Скидка/наценка 0, НДС 0. | ИТОГО = 1 000 000. |
| 7 | Скидка −10 % kiritib ИТОГО 900 000 ekanini ko'ring, so'ng 0 ga qaytaring. | Qayta hisoblanadi. |
| 8 | «НАЗАД» → 2-qadam → «ДАЛЕЕ». | Kiritilgan qiymatlar yo'qolmaydi. |
| 9 | 4-qadam «Завершение»: Номер заказа QA-E2E-ZZ-<DDMM>, Статус **Принято**, Примечание; ta'minotchi bo'limida Дата поставки, Общая скидка 0, Примечание. | ИТОГО в валюте 1 000 000; jamlar mos. |
| 10 | «ЗАВЕРШИТЬ». | Ro'yxatda: QA-E2E Postavshik, Узбекский сум, 1 000 000, Принято. |
| 11 | Запросы на закупку ro'yxatida QA-E2E-ZR holati. | Zakazga bog'langan holat (Завершено yoki shunga o'xshash) — qayd etiladi. |

---

## TC-E2E-10

**Закупка (zakazdan)**

- Yo'l: Склад → Закупки → «Создать» (`/xtrade/a2/anor/mkw/purchase/purchase+add`)
- Ta'minotchi qarzi boshlang'ich qiymati yozib olinadi: Склад → Взаиморасчеты с поставщиками → QA-E2E Postavshik (yangi bo'lsa 0).

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | UMUMIY 1 (1-qadam). | Дата закупки, Шаблон операции, Поставщик, Валюта qizil. |
| 2 | «Заказ на закупку» = QA-E2E-ZZ-<DDMM>. | Поставщик, Валюта, ТМЦ zakazdan to'ladi. |
| 3 | Шаблон операции (birinchi), Договор QA-E2E-DOG, Тип оплаты, Проект, Номер счет-фактуры QA-SF-<DDMM>, Дата счет-фактуры bugun. | Qiymatlar ko'rinadi. |
| 4 | «С поступлением на склад» ni yoqing → *Валюта для учета остатков va *Склад chiqadi → yana **o'chiring** (поступление alohida qilinadi). | Maydonlar paydo bo'ladi/yo'qoladi. |
| 5 | «Внести дополнительные расходы» ni yoqib-o'chiring (o'chiq qoladi). | — |
| 6 | 2-qadam: QA-E2E-TMS × 100 × 10 000; qator «Копировать»/🗑 tugmalarini sinang (oxiri bitta qator). | Сумма 1 000 000. |
| 7 | 3-qadam: Статус **Завершено** → «Сохранить» → «Провести» (agar alohida bo'lsa). | Ro'yxatda Завершено, 1 000 000. |
| 8 | Взаиморасчеты с поставщиками → QA-E2E Postavshik. | Qarz +1 000 000. |
| 9 | Закупка → «Просмотр»: Основная информация, ТМЦ, Поступления tablari. | Поступления bo'sh; «Заказ на закупку» ko'rsatilgan. |

**30.10 izoh:** zakazdan kelgan qator faqat o'qish uchun va «Кол-во кейсов» bo'sh (nusxa qatorda 10/бл chiqadi). «Проект» ixtiyoriy — keyingi hujjatlarni cheklamasligi uchun tanlanmadi. 3-qadam tugmalari: «Провести» va «Сохранить»; Статус standart «Завершено».

---

## TC-E2E-11

**Поступление ТМЦ на склад**

- Yo'l: Склад → Поступления ТМЦ на склад → «Создать» (`/xtrade/a2/anor/mkw/input/input+add`)
- Boshlang'ich: Остатки ТМЦ da QA-E2E-TMS (QA-E2E Sklad) = 0.

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | UMUMIY 1. | Дата, Склад, Валюта для учета остатков qizil. |
| 2 | Номер QA-E2E-PS-<DDMM>, Дата bugun, Склад QA-E2E Sklad, Валюта для учета остатков Узбекский сум; «Внести дополнительные расходы» yoqib-o'chiring. | — |
| 3 | 2-qadam «Закупки»: QA-SF закупкасini tanlang. | Jadval: Название, Номер карточки, Серийный номер, Балансовый, Срок годности, Кол-во, Кол-во кейсов, Цена, Скидка/Наценка, НДС, Сумма доп. расходов, Сумма. |
| 4 | Кол-во 120 yozing. | 100 ga cheklanadi yoki xabar (закупкадан ko'p emas). |
| 5 | Кол-во 100, Срок годности +1 yil, Серийный номер bo'sh. | Сумма 1 000 000, Цена 10 000. |
| 6 | 3-qadam: Статус (standart «Новое») → **Завершено** → «Завершить» → «Да». | Ro'yxatda Завершено. 30.10: закупка tanlanganda «Договор» bo'sh ko'rinadi (закупкада bor). |
| 7 | Остатки ТМЦ → QA-E2E Sklad. | QA-E2E-TMS = **100**. |
| 8 | Закупка → «Просмотр» → Поступления. | QA-E2E-PS ko'rinadi; ikkinchi поступление uchun qolgan 0. |

---

## TC-E2E-12

**Sotuv buyurtmasi (Заказ) yaratish**

- Yo'l: eski UI — Продажа → Заказы → «СОЗДАТЬ» (`#/!<sessiya>/anor/mdeal/order/order+add`)
- Oldindan: mijozning Рабочая зона = Room - Yashnobod; QA-E2E Sklad Room - Yashnobod ga bog'langan; Sotish sum narxi 15 000.
- Boshlang'ich: Взаиморасчеты с клиентами → QA-E2E Mijoz qarzi (0).

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | Ro'yxat tugmalarini tekshiring. | СОЗДАТЬ, СОЗДАТЬ (BETA), СОЗДАТЬ РОЗНИЧНЫЙ ЗАКАЗ, НАСТРОЙКИ ЗАКАЗА, ЧАТЫ; tablar Заказы/Отказы/Розничная продажа/Детали задолженности. |
| 2 | «СОЗДАТЬ» → bo'sh holda «ДАЛЕЕ». | Рабочая зона, Штат, Клиент qizil; Штат va Клиент zona tanlanmaguncha nofaol. |
| 3 | Дата заказа (avto), **Дата отгрузки = BUGUN** (standart +2 kun qolsa TC-E2E-15 da arxivlab bo'lmaydi: «A02-16-049 Дата доставки больше системного»), Заявка bo'sh, Рабочая зона Room - Yashnobod, Штат Main Manager, Клиент QA-E2E Mijoz<DDMM>, Проект, Договор. «Баланс клиента» → «Показать неоплаченные заказы?» → нет. | «Торговый представитель» avto = Usmonxo'jayev Mohir. |
| 4 | «ДАЛЕЕ» → 2-qadam: tablarni (Товар, Сырье, Продукция, Запасная часть, Услуга, Нагрузка, Рекомендации, Акции, Промо, Обмен) navbat bilan oching. | Har biri xatosiz. |
| 5 | «Товар» qidiruvida «QA-E2E» yozing; keyin «TMS» → **QA-E2E Sklad / Sotish sum** variantini tanlang. | «QA-E2E» bilan ham topilishi kerak — 30.10: topilmadi (**BUG-183**). Цена 15 000, Остаток 100. |
| 6 | Кол-во 150 yozing. | Qoldiqdan ko'p — xabar yoki 100 ga cheklash. 30.10: katakda jim 15 qoldi (**BUG-185**). |
| 7 | Кол-во **30**; Кол-во кейсов 3 ekanini tekshiring; Скидка −10 % → Сумма 405 000, so'ng 0 ga qaytaring. | Сумма 450 000; pastda Кол-во 30, ИТОГО 450 000, vazn 30×1.2 / 30×1.5. |
| 8 | «Подбор» va «Импорт» ni ochib-yoping. | Xato yo'q. |
| 9 | «ДАЛЕЕ» → 3-qadam: Тип оплаты (Наличные), Скидка к заказу 0, Номер ТТН QA-TTN-<DDMM>, Номер счет-фактуры QA-SF-S-<DDMM>, Экспедитор, Адрес доставки (mijoz manzili), Ориентир, Метод кодов маркировки = Заказ, Автотранспорт, Примечание «QA-E2E sotuv», Статус **Новый**. | ИТОГО 450 000; o'ngda mijoz/zona/штат to'g'ri. |
| 10 | «НАЗАД» → «ДАЛЕЕ». | Qiymatlar saqlanib qolgan. |
| 11 | «СОХРАНИТЬ». | Ro'yxatda: QA-E2E-TMS, QA-TTN, Room - Yashnobod, QA-E2E Mijoz, Main Manager, 450 000, **Новый**; pastki «Новый» kartochkasi +450 000. |
| 12 | Buyurtmani oching (ko'rish). | Barcha 3-qadam maydonlari saqlangan. |
| 13 | Остатки ТМЦ (a2). | «Новый» buyurtma bron qiladi: В наличии 100, Забронировано 30, Доступно 70. |

**30.10 izoh:** 3-qadamda yetkazish manzili mijozning standart manzilidan avtomatik qo'yiladi; «Консигнация для организации запрещена» ogohlantirishi doim ko'rinadi. Admin buyurtmani «Новый»da saqlay oldi. Natija: buyurtma 571967.

---

## TC-E2E-13

**Buyurtma yetkazib berish: В обработке → Отгружен → Доставлен**

- Yo'l: eski UI — Заказы ro'yxati → qatorni bosish → qator amallari «Изменить статус ▾» (yoki checkbox → yuqoridagi «ИЗМЕНИТЬ СТАТУС ▾»)
- Qator amallari (Новый): Просмотр ▾, Редактировать ▾, Редактировать (Beta), Изменить статус ▾, Накладные ▾, Копировать, Чат. (Доставлен): Просмотр, Отказ, Изменить статус, Накладные, Faktura.uz, Фискализация, Копировать, Чат — **Faktura.uz / Фискализация bosilmaydi** (tashqi).

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | Qatorni bosing → «Изменить статус» ro'yxatini oching. | Joriy statusdan boshqa variantlar: Черновик, Новый, В обработке, В ожидании, Отгружен, Доставлен, Архив, Отменен. Har safar «Status — Теперь изменить статус можно сразу здесь» maslahat oynasi chiqadi (birinchi bosish uni yopadi; «Больше не показывать» bosilmaydi — sozlama). |
| 2 | «В обработке» → «Изменить статус на В обработке?» → да. | «Статус успешно изменён»; pastki «В обработке» kartochkasi +450 000. |
| 3 | «Накладные ▾» ni ochib ko'ring. | Ro'yxat xatosiz. |
| 4 | «Отгружен». | Остатки: В наличии 70, Забронировано 0, Доступно 70. |
| 5 | «Доставлен». | Status Доставлен. |
| 6 | Взаиморасчеты с клиентами → QA-E2E Mijoz. | Задолженность 0, **Заказ 450 000**, Баланс −450 000. |

**30.10:** administrator (mohir@xan) barcha statuslarni o'tkaza oldi — cheklov yo'q.

---

## TC-E2E-14

**Buyurtmaning bir qismini qaytarish («Отказ»)**

- Yo'l: eski UI — Заказы → «Доставлен» buyurtma qatori → **«Отказ»** → «Возврат» oynasi (`#/!<sessiya>/anor/mdeal/order/return?deal_id=<ID>`).
- 30.10: a2 «Продажа → Возвраты → Создать» dagi «ИД заказа» ro'yxatida Доставлен buyurtma **chiqmaydi** (faqat arxivlanganlar) — shuning uchun yetkazilgan buyurtmadan qisman qaytarish «Отказ» orqali qilinadi. a2 «Возвраты» formasi (ИД заказа, Рабочая зона*, Штат*, Склад*, Клиент*, 4 qadam) — arxivlangan buyurtma qaytarishi uchun alohida case.

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | Qatorni bosing → «Отказ». | «Возврат» oynasi: Клиент, Дата, Дата доставки, Торговый представитель, Статус «Доставлен», Сумма заказа 450 000, Валюта (RO), Причина возврата; tablar ТМЦ / Нагрузка / Акции; grid: Название, Серийный номер, Тип ТМЦ, Склад, Кол-во 30, **Возврат**, Цена, Скидка, Сумма, ИТОГО. |
| 2 | «Возврат» = **40**. | 30 ga cheklanadi (Сумма 0). |
| 3 | «Возврат» = **5**. | Сумма заказа 375 000. |
| 4 | Причина возврата = «Обмен» (yagona variant) → «СОХРАНИТЬ» → «Сохранить?» да. | Ro'yxatga qaytadi; «Наличные деньги» kartochkasi −75 000. |
| 5 | Остатки ТМЦ QA-E2E Sklad. | **75** (70 + 5). |
| 6 | Взаиморасчеты с клиентами. | Заказ 375 000, Баланс −375 000 (Задолженность hali 0). |

---

## TC-E2E-15

**Buyurtmani arxivga o'tkazish, mijoz qarzi**

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | Заказы → QA-E2E buyurtma → «Изменить статус» → «Архив». | Buyurtma asosiy ro'yxatdan chiqadi. Agar Дата отгрузки kelajakda bo'lsa: «A02-16-049 — Дата доставки больше системного» (to'g'ri qoida). |
| 1a | (Faqat 1-qadam rad etilsa) Status → «Новый» → «Редактировать» → Дата отгрузки = bugun → 2-, 3-qadamlarda ИТОГО ni tekshiring → «СОХРАНИТЬ» → Отгружен → Доставлен → Архив. | Tahrirda ИТОГО 375 000 bo'lishi kerak — 30.10: 450 000 ko'rsatildi (**BUG-184**); saqlangach ro'yxatda 375 000, qaytarish saqlanadi. |
| 2 | Продажа → Архив заказов (`order_history_list`): «Шаблон», «Добавить параметры», «Применить», «Показать все» tugmalari; QA-E2E buyurtmani toping. | Qator: Дата, Сумма 375 000, ИД заказа, Рабочая зона, Клиент, Штат, Тип оплаты «Наличные деньги», Валюта. |
| 3 | Взаиморасчеты с клиентами → QA-E2E Mijoz. | **Задолженность 375 000**, Заказ 0, Баланс −375 000 (qarz «Заказ»dan «Задолженность»ga arxivda o'tadi). |
| 4 | «ДЕБИТОРЫ» va «ИСТОРИЯ ВЗАИМОРАСЧЕТОВ». | Mijoz qarzdorlar ro'yxatida; tarixda buyurtma +450 000, qaytarish −75 000. |
| 5 | Finansy → Отчет по должникам. | QA-E2E Mijoz 375 000. |

---

## TC-E2E-16

**Mijozdan to'lov qabul qilish, qarz yopilishi**

- Yo'l: Финансы → Оплаты от клиентов → «Создать» (`/xtrade/a2/trade/tcs/cashin+add`)

| № | Qadam | Kutilgan natija |
|---|---|---|
| 1 | Ro'yxat ustunlari va qator amallarini tekshiring (begona qatorlarda Провести/Отменить bosilmaydi). | — |
| 2 | «Создать» → bo'sh «Сохранить». | Дата и время, Валюта, Сумма, Тип оплаты, Клиент qizil. |
| 3 | Сумма −100 va 0. | Rad etiladi. |
| 4 | Номер оплаты QA-E2E-PAY1-<DDMM>, Дата hozir, Валюта Узбекский сум, Сумма **200 000**, Тип оплаты «Наличные деньги» (→ paydo bo'ladigan **Касса *** = Основная касса), Проект, Клиент QA-E2E Mijoz, Договор, Инкассатор, Торговый представитель, Примечание. | «Баланс» maydonida −375 000 ko'rinadi. 30.10: «Тип оплаты» birinchi ochilganda «Загрузка…» osilib qoldi, matn yozilgach yuklandi. |
| 5 | «Провести взаимозачёт» ni yoqing. | Qo'shimcha belgilar: С учётом компенсации, По договору ✓, По типу оплаты ✓, По проекту ✓. |
| 6 | «Провести» → «Провести?» Да. | Forma ochiq qoladi (Тип оплаты/Касса saqlanadi), pastdagi jadvalda to'lov «Проведён: Да». |
| 7 | Mijozni qayta tanlab «Баланс» ni ko'ring. | −175 000. |
| 8 | 2-to'lov QA-E2E-PAY2: **175 000** → Провести. | Jadvalda ikkita to'lov. Взаиморасчеты с клиентами (eski UI) — **F5 bilan qayta yuklang** (30.10: oddiy o'tishda eski 375 000 ko'rindi) → mijoz ro'yxatda yo'q (qarz 0). |
| 9 | To'lov → «Просмотр»: Номер, ИД, Проведено, Касса, Сумма, Клиент, Договор, Инкассатор, Торговый представитель, Назначение, Примечание; tablar Редактировать / Основная информация / История изменений. | Mos. |

---

## TC-E2E-17

**Yakuniy solishtiruv: qoldiq, qarzlar, hisobotlar**

| № | Tekshiruv | Kutilgan natija |
|---|---|---|
| 1 | Остатки ТМЦ (QA-E2E Sklad, QA-E2E-TMS). | 75 |
| 2 | Материальный отчет / Общий отчет по складам (bugun). | Приход 100, Расход 30, Возврат +5, Остаток 75 — Остатки bilan bir xil. |
| 3 | Взаиморасчеты с поставщиками (QA-E2E Postavshik). | Qarz 1 000 000 (ta'minotchiga to'lov qilinmagan). |
| 4 | Взаиморасчеты с клиентами (QA-E2E Mijoz). | 0 |
| 5 | Заказы ro'yxati pastki status kartochkalari. | QA-E2E buyurtma hech bir faol statusda yo'q. |
| 6 | Отчет по должникам. | QA-E2E Mijoz yo'q. |
| 7 | Проводки счетов (bugun, QA-E2E hujjatlari). | Har hujjatga provodka bor; debet = kredit. |

---

## TC-E2E-18

**Tozalash (teskari tartibda)**

> 30.10.2026 qarori: test ma'lumotlari hisobot tekshiruvlari uchun **o'chirilmaydi**; bu case barcha hisobotlar tekshirilib, doimiy ma'lumotlar ro'yxati tasdiqlangandan keyin qayta ko'rib chiqiladi. Faqat QA-TMP- yozuvlari tozalanishi mumkin.

Faqat QA-E2E yozuvlari, foydalanuvchi ruxsati bilan: to'lovlar (Отменить → Удалить) → qaytarish → buyurtma (Отменен) → поступление → закупка → заказ на закупку → запрос → mijoz/ta'minotchi/ombor/ТМЦ «Неактивный». O'chirib bo'lmaydiganlari nofaol qilinadi va ro'yxatga yoziladi.

---

## Ochiq savollar — 30.10 javoblari
1. Admin (mohir@xan) buyurtmani Новый/В обработке/Отгружен/Доставлен/Архив ga o'tkaza oladi — **ha**.
2. Доставлен'da summa «Заказ» ustunida (Баланс manfiy), **Архив**da «Задолженность»ga o'tadi.
3. «Сохранить в качестве поставщика» / «Клиент» checkbox'lari Поставщик/Клиентни **avtomatik yaratadi**.
4. Yetkazilgan buyurtmadan qisman qaytarish — «Отказ» oynasida, alohida status yo'q (saqlash bilan qo'llanadi).
5. «Отказ»da buyurtmadagidan ko'p miqdor (40 > 30) **30 ga cheklanadi**.

## 30.10 yugurishida yaratilgan yozuvlar (tozalash uchun)
ТМЦ QA-E2E-TMS-3010 (140464); narx Sotish sum 15 000 / Olish sum 10 000; Юр.лицо QA-E2E Postavshik MChJ 3010 + Поставщик 405210; Физ.лицо QA-E2E Mijoz3010 + Клиент 405211; Склад QA-E2E Sklad 3010; Запрос QA-E2E-ZR-3010 (1649); Заказ на закупку QA-E2E-ZZ-3010; Закупка QA-E2E-ZK-3010; Поступление QA-E2E-PS-3010; Заказ 571967 (Архив); Оплаты QA-E2E-PAY1-3010, QA-E2E-PAY2-3010. Qoldiq QA-E2E Sklad = 75; ta'minotchi qarzi 1 000 000; mijoz qarzi 0.
