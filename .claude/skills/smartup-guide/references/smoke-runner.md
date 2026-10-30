# Smoke Runner Setup Chain

## Qidiruv Kalitlari

Tags: smoke, setup, runner, dependency, data-store, license, balance, tmc, room, user

### 2026-05-25 Run Natijasi
Tags: smoke, run-result, sandbox
- Buyruq: `./.venv/bin/pytest tests/smoke/test_all_runner.py -v --tb=short`
- Natija: 21 passed, 0 failed, umumiy vaqt 196.22s.
- Session code: `1384`; `test_01_authorization` `test-results/data/data_store.json` ichidagi `code` qiymatini yangiladi.
- `data_store.json` ichidagi A-group `contract_*` va `order_id` qiymatlari bu runnerda yangilanmadi; ular avvalgi run code qiymatlariga tegishli bo'lishi mumkin.
- Trace: `test-results/traces/smoke_trace.zip` saqlandi.
- Eslatma: sandbox ichida Chromium Crashpad permission xatosi bilan browser ochilmadi; sandboxdan tashqarida xuddi shu runner passed bo'ldi.

### Runner Qoidasi
Tags: smoke, setup, dependency, data-store
- `tests/smoke/test_all_runner.py` barcha runnerlarni jamlaydi: user setup, keyin A/B/... group runnerlar.
- Umumiy runner pytest `test_*` funksiyalarini import qilib chaqirmaydi; runnerlar `run_*_chain` va biznes `run_*` funksiyalarini setup -> A -> B -> ... tartibida chaqiradi.
- `tests/smoke/test_setup/test_setup_runner.py` ichidagi testlar bitta `session_page` bilan ketma-ket ishlaydi; UI state va login holati testlar orasida saqlanadi.
- `.env` ishlatilmaydi; `--url` har doim majburiy.
- Mavjud company bilan run qilish uchun `--url <server_url> --company-code <code> --company-password <password>` beriladi; company testi suitega qo'shilmaydi.
- Yangi company bilan run qilish uchun `--url <server_url> --create-company --head-email <email> --head-password <password>` beriladi; head profil credentiallari flag orqali majburiy beriladi.
- `--create-company` bilan `--company-code` va `--company-password` berilmaydi; company code test tomonidan `autotest<code>` ko'rinishida yaratiladi.
- Test user paroli kod ichida hardcode; head/company admin paroli bilan aralashtirilmaydi.
- `00 - Company` suitega URLga qarab emas, explicit yangi company yaratish flagi orqali qo'shiladi.
- Company testi run bo'lsa, `data_store.json`ga saqlangan `company_code` keyingi loginlarda `--company-code` o'rniga ishlatiladi; company testi run bo'lmasa stale `company_code` tozalanadi.
- License policy yoqiq qolsa, yangi company license flow uchun head viewdagi `Активация для лицензии` shart emas; `Политика лицензирования` yoqiq bo'lishi yetarli va `Buy License` qadamida flow davom etishi kerak.
- `--create-company --disable-license-policy` ishlatilsa yangi companyda license policy off qilinadi va setupdagi `Buy License` / `Attach License` qadamlari o'tkazib yuboriladi.
- `--create-company` full runnerda A/B group loginlari ham yaratilgan `company_code`ni ishlatadi; setup zanjirida user/role/password/license kabi user login precondition qadamlari o'chirilgan bo'lsa `user-pw{code}@<company_code>` yaratilmaydi va group login `login.html`da qolib ketadi.
- Har bir group boshida user bir marta login qiladi; group ichidagi test/flowlar shu oynada davom etadi va group tugaganda yoki failed/skip bo'lganda fixture oynani yopadi.
- Full runnerda har group uchun alohida `group_page` ochiladi; alohida group runner faylida testlar `group_user_page` module-scoped fixture bilan bitta login/page ishlatadi.
- Har bir group runner ichida `*_GROUP_TEST_SCENARIO` ko'rinishida group-level test ssenariy yoziladi va `run_*_group_chain` uni Allure description'ga beradi; foydalanuvchi group qaysi biznes ssenariyni qamrab olishini runnerdan ko'rishi kerak.
- B-group leaf testlari bittadan pytest testli alohida fayllarda turadi; `test_b_group_runner.py` ularni `run_*` helper funksiyalari orqali bitta B-group zanjiriga yig'adi.
- `code` fixture full/setup runnerda yoki `--new-code` bilan yangi random 4 xonali qiymat beradi; yakka/group debugda `--reuse-code` yoki default orqali `test-results/data/data_store.json` dan o'qiladi.
- `test_01_authorization` `save_data("code", code)` orqali yangi code ni keyingi yakka/debug testlar uchun saqlaydi.
- Smoke runner `data_store.json` ni tozalab qayta yaratmaydi; faqat `code` yozadi. Shu sabab group testlardan qolgan eski `contract_*` yoki `order_id` qiymatlarini smoke setupning hozirgi code qiymati bilan bir xil deb qabul qilmaslik kerak.

- Setup zanjiri buzilsa keyingi testlar ham precondition yo'qligi sabab yiqilishi mumkin; yakka testdan oldin to'liq runner yoki mos precondition ma'lumotlari kerak.
- Directory/default collection duplicate business flow yurmasligi uchun default holatda faqat mos runner fayllarini qoldiradi; leaf testlarni collect qilish kerak bo'lsa `--include-leaf-tests` ishlatiladi.
- Cross-platform asosiy run: `python scripts/run_tests.py --url {server_url} --company-code {code} --company-password {password}` yoki `python scripts/run_tests.py --url {server_url} --create-company --head-email {email} --head-password {password}`; Mac/Linux wrapper: `./run_tests.sh ...`.
- Runner debug mode'lari: `all`, `setup`, `company`, `group-a`, `group-b`; foydalanuvchi odatda bo'laklarga bo'lib run qilmaydi, normal run doim full suite.
- Test scope mode global bo'ladi: all/setup/group runnerlar smoke yoki regression mode bilan yuradi va bu mode `run_*_chain` -> `run_*` flowlarga uzatiladi.
- Yangi testlar bitta biznes flow ichida ikki scope bilan yoziladi: smoke branch minimal data va asosiy list/assertlar, regression branch optional data, kengroq tab/view assertlar va edge case tekshiruvlarni bajaradi.

### Smoke Credentiallari Majburiy
Tags: setup, runner, credential
- Qoida: mavjud company uchun `--company-code/--company-password` majburiy; yangi company yaratish uchun `--create-company --head-email/--head-password` majburiy. Yangi company code `autotest<code>`, admin login `admin@autotest<code>`, admin password test ichidagi default qiymat.

### Smoke/Regression Scope Arxitekturasi
Tags: smoke, regression, scope, runner, write-test, data-store
- Scope butun suite uchun global: `scripts/run_tests.py` default `smoke`, `--regression` yoki `--scope regression` esa pytestga `--scope <mode>` qilib uzatiladi; pytestda `test_scope` fixture shu qiymatni qaytaradi.
- Scope berilmasa default `smoke`; pytest bevosita yurgizilganda `--scope=regression` yoki env `TEST_SCOPE=regression` ishlatiladi.
- Runnerlar `test_scope` ni chain funksiyalarga uzatadi: `test_all_runner.py` -> `run_setup_chain/run_*_group_chain` -> biznes `run_*` funksiyalar. Yangi runner/testlarda ham shu propagation buzilmasin.
- Bitta testni alohida smoke va regression faylga bo'lma; bitta `run_*` funksiyada `scope: str = "smoke"` parametr bo'lsin, smoke va regression branchlar shu parametr bilan ajralsin.
- Smoke branch minimal bo'ladi: formaning yurishi uchun kerakli majburiy maydonlar, downstream uchun zarur data-store keylar, save, listdagi asosiy `code/name/status` tekshiruvlar.
- Regression branch foydalanuvchi aytganda `full` ma'nosini beradi: real add formadagi mavjud barcha muhim input/switch/tab/modal maydonlar to'ldiriladi, Faker bilan mantiqli real qiymatlar ishlatiladi, kerakli dependency entitylar yaratiladi, list va view tekshiriladi.
- Regression view tekshiruvi faqat view ochilganini ko'rish emas: addda yozilgan qiymatlar viewdagi mos card/tablarda ko'rinishini tekshir; formaga xos product/module/permission tablari bo'lsa ularning holatini ham tekshir.
- Hech qachon add form fieldlarini taxmin qilib yozma. Regression qilishdan oldin browserda real forma ochiladi, screenshot va field state olinadi, keyin `smartup-guide/references/forms/<form-slug>.md` va `screenshots/<form-slug>/` yangilanadi.
- Data store smoke va regressionda toza ajratilsin: smoke faqat keyingi testlarga kerak minimal keylarni yozadi va regression-only keylarni stale bo'lib qolmasligi uchun `None`/null bilan tozalaydi; regression qo'shimcha view/list assertlar uchun kerak bo'lgan hamma muhim keylarni saqlaydi.
- Scope ishidan keyin kamida tegishli runner ikki mode bilan tekshiriladi: `python scripts/run_tests.py --url <server_url>` va `python scripts/run_tests.py --url <server_url> --regression`.

### Entity Naming
Tags: smoke, entity, naming
- Company server code: `autotest{code}`; login suffix sifatida `@autotest{code}` ishlatiladi.
- Legal person: `cod_lg_pw{code}` / Faker company name + `legal_person-pw{code}` suffix.
- Legal person owner: `cod_owner_lg_pw{code}` / Faker company name + `legal_owner-pw{code}` suffix.
- Legal person director: `director_np_pw{code}` natural person, Faker F.I.O.; Legal Person regression buni Natural Person helper orqali yaratadi.
- Employee natural person code: `natural_person_pw{code}`; ko'rinadigan nom: `natural_person-pw{code}`.
- Client natural person code: `natural_client_pw{code}`; ko'rinadigan nom: `natural_client-pw{code}`.
- Legal person contact position: `contact_position_pw{code}` / `Директор по развитию-pw{code}`.
- Filial/organization: `filial-pw{code}`; yuridik shaxs `cod_lg_pw{code}` ga ulanadi.
- Room/work zone: `code_room_pw{code}` / `room-pw{code}`.
- Robot/staff: `code_robot-pw{code}` / `robot-pw{code}`.
- User: `user-pw{code}@<active_company_code>`; active company code company testi yaratgan `company_code`, bo'lmasa `--company-code`; password kod ichidagi test user default qiymati.
- Price type: `code_price_type_uzb_pw{code}` / `Price Type UZB-pw{code}`.
- Sector/TMC set: `code_sector_pw{code}` / `sector-pw{code}`.
- Product/TMC: `code_product-pw{code}` / `product-pw{code}`; price `7000`.
- Init balance document number: `{code}`; quantity `100`, price `5000`, expected posting sum `500 000`.

## Testlar Tartibi Va Vazifasi

### 00 Company
Tags: company, setup, head, data-store
- Fayl: `tests/smoke/test_setup/test_company.py`.
- Ishga tushirish: faqat explicit yangi company yaratish flagi berilganda suitega qo'shiladi.
- Guard: company yaratish URLga qarab avtomatik qo'shilmaydi; flag yo'q bo'lsa skip/deselect qilinadi.
- Login: `--head-email` / `--head-password` orqali majburiy berilgan head profil credentiallari.
- Navigation: `Главное` -> `Компании`.
- Nima qiladi: `Код сервера` sifatida `autotest{code}` kiritadi, visible required maydonlarni minimal to'ldiradi, Products card ichida `trade` va child productlarni yoqadi, saqlaydi va listda code bo'yicha tekshiradi.
- License activation: yangi company uchun license sotib olishdan oldin `Активация для лицензии` talab qilinmaydi; test bu tabni majburiy precondition sifatida ishlatmasin.
- License policy: `--create-company --disable-license-policy` berilsa company viewdagi `Безопасность`/Security tabda `Политика лицензирования` off qilinadi va setupdagi license xaridi/ulash qadamlari o'tkazib yuboriladi; flag bo'lmasa default holatda qoldiriladi.
- Nima saqlaydi: `company_code`.

### 01 Authorization
Tags: authorization, data-store
- Fayl/flow: `tests/smoke/test_setup/test_setup_runner.py`, `tests/smoke/flows/flow_authorization.py`.
- Nima qiladi: admin sifatida login qiladi va `Trade` dashboard headingini kutadi.
- Nima saqlaydi: session `code` qiymatini `data_store.json` ga yozadi; company setup ishlamagan bo'lsa stale `company_code`ni `null` qiladi.

### 02 Legal Person
Tags: legal-person, setup, owner, director, data-store
- Fayl: `tests/smoke/test_setup/test_legal_person.py`.
- Navigation: `Справочники` -> `Юридические лица`.
- Smoke: minimal branch. Faqat `cod_lg_pw{code}` va `legal_person-pw{code}` uchun asosiy maydonlar to'ldiriladi, saqlanadi va listda `Код`, `Название`, `Активный` tekshiriladi.
- Regression: to'liq branch. Avval `Собственник` (`cod_owner_lg_pw{code}`), Natural Person helper orqali `Руководитель` (`director_np_pw{code}`) va `contact_position_pw{code}` yaratiladi, so‘ng asosiy legal personga bog'lanadi. `Собственник`, `Руководитель`, `GPS`, bank, kontakt, qo'shimcha tablar to'ldiriladi.
- GPS: map modalida `41.2994958,69.2400734` search qilib `d.latlng=41.2994958,69.2400734,12` saqlanadi.
- Bank account: `МФО=00001` yozib `Tab` bosilganda bank auto-fill `Центр расчетов Центрального банка по г. Ташкенту`; valyuta `Узбекский сум`.
- Data store: smoke rejimda `legal_person_code/name` va regression uchun owner/director/accountant, `tin`, `phone`, `email`, `region`, `gps`, bank account va contact person/lavozim qiymatlari saqlanadi (smoke branch uchun regression-only kalitlar nullga o'chiriladi).
- Tekshiruv: smoke mode ro'yxatda `Код`, `Название`, `Активный`ni tekshiradi. Regression mode qo'shimcha:
  - ro'yxatda `Альтернативное название` ham ko'rinadi;
  - viewda `Основная информация`, `Дополнительная информация`, `Расчетный счет`, `Контактные лица` tablaridagi qo'shilgan qiymatlar tekshiriladi.

### 03 Filial
Tags: filial, organization, legal-person
- Fayl: `tests/smoke/test_setup/test_filial.py`.
- Navigation: `Главное` -> `Организации`.
- Smoke: minimal branch. `filial-pw{code}` tashkilot yaratiladi, valyuta `Узбекский сум` va `cod_lg_pw{code}` yuridik shaxs bilan ulanadi.
- Regression: qo'shimcha tekshiruv: row click + `Просмотреть` orqali view ochiladi; viewda filial nomi, valyuta, status (`Активный`) va legal person code ko'riladi; agar `legal_person_name` data-store’da bo'lsa u ham tekshiriladi.
- Har ikki rejimda: ro'yxatda filial va legal person code ni tekshirib, reload + loader kutiladi.
- Data store: `filial_name`, `filial_code`, `filial_currency`, `filial_legal_person_code`, va agar mavjud bo'lsa `filial_legal_person_name` saqlanadi.

### 04 Room
Tags: room, filial, work-zone
- Fayl: `tests/smoke/test_setup/test_room.py`.
- Precondition: `switch_filial(page, name=f"filial-pw{code}")`.
- Navigation: `Справочники` -> `Рабочие зоны`.
- Nima yaratadi: `code_room_pw{code}` / `room-pw{code}` ish zonasi.
- Tekshiruv: saqlagandan keyin `Рабочие зоны` ro'yxatida code va nom ko'rinadi.

### 05 Robot
Tags: robot, staff, room
- Fayl: `tests/smoke/test_setup/test_robot.py`.
- Navigation: `Справочники` -> `Штат`.
- Nima yaratadi: `code_robot-pw{code}` / `robot-pw{code}` xodim.
- Bog'lanish: `Админ` tanlanadi va `room-pw{code}` ish zonasi ulanadi.

### 06 Natural Person
Tags: natural-person, employee
- Fayl: `tests/smoke/test_setup/test_natural_person.py`.
- Precondition: `filial-pw{code}` filialiga o'tadi.
- Navigation: `Справочники` -> `Физические лица`.
- Nima yaratadi: xodim uchun `natural_person_pw{code}` code va `natural_person-pw{code}` ko'rinadigan nomli jismoniy shaxs.
- Smoke: majburiy `d.first_name`, `d.code` va `Активный` minimal path; list va viewda nom/status tekshiriladi.
- Regression: birthday, passport, region, address/post address, phone, tin, telegram, email, web to'ldiriladi; viewda asosiy kiritilgan qiymatlar tekshiriladi.
- Arxitektura: Natural Person helperlari shu test faylida turadi; Legal Person direktor yaratishda shu helperlarni import qiladi.

### 07 User
Tags: user, robot, natural-person
- Fayl: `tests/smoke/test_setup/test_user.py`.
- Navigation: `Главное` -> `Пользователи`.
- Nima yaratadi: `user-pw{code}@<active_company_code>` loginli user.
- Bog'lanish: `robot-pw{code}` va `natural_person-pw{code}` ulanadi; password kod ichidagi test user default qiymati.
- Tekshiruv: user ro'yxatida natural person va login ko'rinadi.

### 08 User Attach Form
Tags: user, permissions, forms
- Fayl: `tests/smoke/test_setup/test_user.py`.
- Nima qiladi: user view ichida `Формы` sahifasini ochib `Формы`, `Отчеты`, `Накладные`, `Внешние системы` tablaridagi mavjud elementlarni userga ulaydi.
- Muhim pattern: har bir tabda page size `1000` qilinadi, `BasePage.click_first_visible_checkbox()` orqali real checkbox/select all bosiladi, `#biruniConfirm` orqali tasdiqlanadi.
- Qayta run: bo'limda `нет данных` bo'lsa attach qadam no-op bo'lib o'tadi; bu qadam mavjud companyda permissionlarni qayta qo'llash uchun idempotent bo'lishi kerak.
- Tekshiruv: har bo'limda `Доступные` ro'yxati `нет данных` bo'lishi kerak.

### 09 Role
Tags: role, permissions
- Fayl: `tests/smoke/test_setup/test_user.py`.
- Navigation: `Пользователи` sahifasidan `Роли`.
- Nima qiladi: `Админ` rolini edit qilib, `.switch span` ichidagi barcha `нет` switchlarni yoqadi.
- Muhim pattern: onboarding launcher JS orqali yashiriladi; saqlashdan keyin loader 600s gacha kutiladi.

### 10 Role Attach Form
Tags: role, forms, permissions
- Fayl: `tests/smoke/test_setup/test_user.py`.
- Nima qiladi: `Админ` rol viewidagi `Формы` bo'limida `Доступ ко всем формам` -> `Разрешить` qiladi.
- Tekshiruv: `Доступные` ro'yxati `нет данных` bo'ladi.

### 11 Buy License
Tags: license, admin, balance
- Fayl: `tests/smoke/test_setup/test_license.py`.
- `--disable-license-policy` bo'lsa bu qadam real license flowga kirmaydi va Allure/logga skip sababini yozib davom etadi.
- Nima qiladi: logout qilib admin sifatida qayta kiradi, `Администрирование` filialiga o'tadi, `Главное` -> `Лицензии` sahifasida balans musbatligini tekshiradi va `Smartup ERP` uchun kerakli license sotib oladi.
- Oyning boshida yoki shu oy uchun birinchi xaridda `Smartup ERP: Базовый пользователь (Обязательный)` alohida row chiqadi; bu rowda quantity `5` disabled/auto-filled bo'ladi, avval shu majburiy license olinadi, keyin oddiy `Smartup ERP: Базовый пользователь` rowdan 1 ta license olinadi. Shu oy keyingi runlarda majburiy row chiqmasligi mumkin.
- Standalone `test_buy_license` blank `page` bilan boshlanishi mumkin; faol sessiya headeri ko'rinsa logout qilinadi, aks holda logout skip qilinib admin login qilinadi.
- Kerakli ma'lumotlar: payer `AUTOTEST GWS`, contract `Договор № bn от 01.01.2025`, begin date today.
- Debug note: payer/contract `b-input` bo'sh bo'lsa `.edit` clear icon `ng-hide` bo'ladi; optionlar ko'rinib turgan bo'lsa ham yashirin `.edit`ni bosish `Locator.click TimeoutError` beradi. `clear=True` helperlari `.edit` faqat visible bo'lsa bosishi kerak.
- Log: balans musbat bo'lsa `Balans musbat — Success`, sotib olinsa `Litsenziya olindi`.

### 12 Attach License
Tags: license, user
- Fayl: `tests/smoke/test_setup/test_license.py`.
- `--disable-license-policy` bo'lsa bu qadam real attach flowga kirmaydi va Allure/logga skip sababini yozib davom etadi.
- Nima qiladi: `Лицензии и документы` ichida `ERP users` license ochiladi, mavjud attached users bo'lsa ajratiladi, `natural_person-pw{code}` userga ulanadi.
- Muhim pattern: `PlaywrightTimeoutError` orqali `нет данных` bo'lmasa hammasini select qilib `Открепить` qiladi.

### 13 Change Password
Tags: user, password
- Fayl: `tests/smoke/test_setup/test_user.py`.
- Nima qiladi: yangi `user-pw{code}@<active_company_code>` login bilan kiradi; majburiy password change alert chiqishini kutadi.
- Amaliyot: current/new/rewrite password maydonlariga kod ichidagi test user default paroli kiritilib `Подтвердить` va confirm `да` bosiladi.

### 14 Price Type
Tags: price-type, room, nps
- Fayl: `tests/smoke/test_setup/test_price_type.py`.
- Nima qiladi: NPS Survey modal chiqsa 10 ball bilan yuboradi; `Справочники` -> `Цены` sahifasida UZB price type yaratadi.
- Bog'lanish: `room-pw{code}` ish zonasi ulanadi; `Цена продажи` ko'rinishi tekshiriladi.
- Tekshiruv: `Price Type UZB-pw{code}` searchdan keyin ro'yxatda ko'rinadi.

### 15 Payment Type
Tags: payment-type, room-attachment
- Fayl: `tests/smoke/test_setup/test_payment_type.py`.
- Nima qiladi: `Цены` -> `Типы оплат` ichida `Прикрепление` orqali barcha 4 payment typeni tizimga ulaydi.
- Tekshiruv: `Наличные деньги`, `Перечисление`, `Терминал`, `Чековая книжка` ro'yxatda ko'rinadi.

### 16 Sector
Tags: tmc, sector, room
- Fayl: `tests/smoke/test_setup/test_sector.py`.
- Nima yaratadi: `Наборы ТМЦ` ichida `code_sector_pw{code}` / `sector-pw{code}` TMC to'plami.
- Bog'lanish: `room-pw{code}` tanlanadi.

### 17 Product
Tags: tmc, product, price
- Fayl: `tests/smoke/test_setup/test_product.py`.
- Nima yaratadi: `ТМЦ` ichida `code_product-pw{code}` / `product-pw{code}` mahsulot.
- Bog'lanish: measure `шт`, product type `Товар`, sahifada `sector-pw{code}` ko'rinishi precondition sifatida tekshiriladi.
- Qo'shimcha: `Установить цены` orqali gridga `7000` narx yozib saqlaydi.

### 18 Natural Person For Client 1
Tags: natural-person, client
- Fayl: `tests/smoke/test_setup/test_natural_person.py`.
- Nima yaratadi: `natural_client_pw{code}` code va `natural_client-pw{code}` ko'rinadigan nomli jismoniy shaxs, `Клиент` belgisi yoqiladi.
- Tekshiruv: avval `Физические лица` list va `Просмотр` viewda nom/status tekshiriladi, keyin `Клиенты` ro'yxatida ko'rinadi; regressionda natural person qo'shimcha maydonlari ham to'ldiriladi.

### 19 Room Attachment
Tags: room, payment-type, warehouse, cashbox, client
- Fayl: `tests/smoke/test_setup/test_room.py`.
- Nima qiladi: yangi user sifatida kirib `room-pw{code}` ish zonasi `Прикрепление` sahifasiga kiradi.
- Bog'lanishlar: 4 payment type, 1 warehouse, 1 cashbox va `natural_client-pw{code}` client ish zonasiga ulanadi.
- Tekshiruv: payment/warehouse/cashbox available listlari `нет данных`; client attached listida `natural_client-pw{code}` ko'rinadi.

### 20 Init Balance
Tags: inventory, init-balance, product
- Fayl: `tests/smoke/test_life_cycle/init_balance.py`.
- Nima qiladi: `authorization_user(page, code)` bilan user sifatida kiradi, `Склад` -> `Ввод начальных остатков ТМЦ` sahifasida boshlang'ich qoldiq hujjati yaratadi.
- Formda `Склад` display text auto-fill ko'rinsa ham `warehouse_id` backendga set bo'lmasligi mumkin; test `d.warehouse_name` b-inputida `Основной склад`ni real dropdown orqali qayta tanlaydi.
- Hujjat: number `{code}`, product `code_product-pw{code}`, quantity `100`, price `5000`.
- Tekshiruv: hujjat o'tkazilgandan keyin `Проводки` popupida `100` va `500 000` borligi tekshiriladi.

### 21 Balance
Tags: inventory, balance, product
- Fayl: `tests/smoke/test_life_cycle/balance.py`.
- Navigation: `Склад` -> `Остатки ТМЦ`.
- Tekshiruv: qoldiq sahifasida `code_product-pw{code}` ko'rinadi.
