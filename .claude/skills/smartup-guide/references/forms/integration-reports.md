# Integration reportlar (trade/rep/integration/*) — umumiy bilim

Bu fayl Report group'dagi integration reportlarni jamlaydi. Ular **menyuda yo'q**, URL orqali ochiladi:
`#/<session_token>/trade/rep/integration/<name>` (token login'dan keyingi `page.url` dan olinadi). Hammasi **admin login** talab qiladi. Download'lar Playwright `page.expect_download` bilan tekshiriladi (umumiy helper: `test_report_grup/report_helpers.py`).

Alohida dossierlar: [cislink.md](cislink.md), [integration-three.md](integration-three.md).

## b-input tanlash (umumiy)

`select_b_input_option(page, name, option)`: `b-input[name="..."]` → Поиск'ni bos → fill(option) → `.hint-body, div.hint` ichidan `get_by_text(option, exact=True)` ni bos. Option container `.hint-body` yoki `div.hint` bo'lishi mumkin (b-input konfiguratsiyasiga qarab).

## SalesWork (`saleswork`) — sales_work.zip ✅

- Tugmalar: **Экспорт** (`generate()`), **Шаблоны** (`selectTemplate()`).
- Flow: Шаблоны → template list (`saleswork_template_list`) → **Создать** (`add()`) → `saleswork_template+add`: `d.name` + `product_groups`=Группа → Сохранить (`save()`).
- Save'dan keyin SalesWork'ga qaytadi va shablon **avto-tanlanadi**: `input[ng-model="d.template_name"]` = yaratilgan nom (assert).
- **Экспорт** (`generate()`) → `sales_work.zip` yuklanadi.

## Optimum (`optimum`) — optimum.zip ✅ (qisman)

- Tugmalar: **Сформировать** (`generate()`), **Настройки** (`q.show_setting = true`), save `button[ng-click="save()"]`.
- Settings: `product_groups`=Группа (`Продуктовое группа*`) + 8 ta prefiks `input[ng-model="d.prefix_<key>"]` (transfer_out=1 … production_receipt=8).
- **Сформировать** (barcha filial, `q.is_all_filials` default checked) → `optimum.zip`.
- ⚠️ **GAP**: 1-generate'dan keyin turg'un `.block-ui-overlay` qoladi → "Все филиалы"ni toggle qilib bitta filial bo'yicha 2-generate qilish bloklanadi. Test faqat all-filials generate'ni tekshiradi.

## Spot 2d (`spot`) — Spot2D.zip ✅ (soddalashtirilgan)

- Tugmalar: **Сформировать** (`run()`), **Настройки** (`setting()`), **Шаблоны** (`selectSpotTemplate()`).
- Flow: Шаблоны → template list → **Создать** (`add()`) → `d.name` + `product_groups`=Группа → save (`button[b-hotkey="save"]` — `ng-click="save()"` da "Оцените нас" feedback modalining save'i ham bor, strict violation; b-hotkey ishlatiladi).
- Save'dan keyin Spot'ga qaytadi → **Сформировать** (`run()`) → `Spot2D.zip`.
- ⚠️ **GAP**: checklistdagi "template listdan find_row → close → Настройки → Очистить настройки" qadamlari olib tashlandi (close tugmasi `page.close()` ng-hide, clear-settings noaniq). Yadro: template yaratish + Spot2D.zip.

## Integration Two (`integration_two`) — 4 xml ⚠️ SKIP (muhitga bog'liq)

- Title "Интеграция с системой монолит". Tugmalar: **Генерировать** (`generate()`), **Настройки** (`q.show_setting = true`), save `button[ng-click="save()"]`.
- Settings: `d.company_id`, `d.user_name`*, `d.url`*, `d.unit_of_quant_measurement`*, `d.unit_of_box_measurement`* (checklistda yo'q, lekin majburiy!), `price_types`* , `product_groups`* (Характеристика ТМЦ); checkboxlar `d.edit_person`/`d.ignore_updated_deals`/`d.show_owner_person_code`/`d.send_all_deals`.
- Exchange mode radiolari `input[ng-model="d.exchange_mode"][value="..."]`: **CRMOrder**=import_order, **CRMDespatch**=export_order, **CRMOrderStatus**=import_order_status, **CRMInput**=export_input (CRMWhBalance=4 commentlangan, CRMMovement=6).
- ⚠️ **SKIP sababi (muhit)**: `integration_two` report **filial-pw5963'da yoqilmagan** (faqat company default filialida ochiladi — switch_filial qilinsa sahifa "Дашборд"da qolib yuklanmaydi). Lekin `Price Type UZB-pw5963` faqat filial-pw5963'da. Default filialda price_types server-search bilan ishlaydi va mos data yo'q. Test kodi `test_integration_two.py` da tayyor — `integration_two` yoqilgan va price-type/data mos filialli muhitda ishlaydi.

## Eslatmalar

- Admin parol: autotest uchun `greenwhite` (`CREATED_COMPANY_PASSWORD`).
- Yuklangan fayllar `test-results/downloads/` ga saqlanadi.
- Testlar: `tests/smoke/test_groups/test_report_grup/` — Report-03..06; runner `test_05_report_group_runner` (all-runner). IntTwo chain'da emas, standalone wrapper'da `@pytest.mark.skip`.
