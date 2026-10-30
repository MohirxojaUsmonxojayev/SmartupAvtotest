# Торговый маркетинг — locators, API va route'lar

## Selektorlar

| Element | Selektor / usul | Izoh |
|---|---|---|
| Yuqori menyu | `page.getByRole('link'\|'button', { name: '<Menyu>' })` | Bosilganda bo'limlar ro'yxati ochiladi. |
| Menyu «+» | `button[aria-label="<Band> (создание)"]` | Menyu ochilgandan keyin ko'rinadi (hover shart emas). |
| Ro'yxat qatori | `.smt-data-row (filter hasText)` | Qatorni tanlash: ichidagi .text-start katakni bosish. |
| Qator amallari | `qatordan keyin chiqadigan button'lar (matn bo'yicha)` | Просмотреть / Изменить / Удалить / Статус … |
| Ustun sarlavhalari | `smt-cell-header` | assert_columns uchun. |
| Tanlov ro'yxati | `smt-select-trigger / smt-data-select` | Ishonchli usul: bosish → matn yozish → ArrowDown → Enter. |
| Variantlar | `.cdk-overlay-pane` | Ro'yxat overlay'da; ba'zi «Создать» menyulari [role=menuitem] (overlay'siz). |
| Switch | `[role=switch]` | aria-checked bo'yicha holat. |
| Checkbox | `label[smt-checkbox] [role=checkbox]` |  |
| Tab / wizard qadami | `[role=tab]` |  |
| Tasdiqlash oynasi | `[role=dialog] → «Да»/«да»` | Matn: «Сохранить?», «Удалить …?», «Провести?», «Изменить статус …?». |
| Xato oynasi | `[role=dialog] ichida «Ошибка» + «URL: /xtrade/b/…»` | Avtotestda: bunday oyna chiqsa test yiqilsin. |
| Подбор paneli | `o'ngdan chiquvchi panel, sarlavha «… (подбор)», tablar Доступные/Выбранные` | Yopishda «Выбрать ТМЦ с заполненными данными?» → «Да». |
| Hisobot natijasi | `«Сформировать» → «Просмотр» tabi (iframe) yoki yangi oyna / download` | rt=htmla\|xlsx\|csv |
| API: model | `POST /xtrade/b/<route>:model` | Forma/sahifa ma'lumoti. |
| API: ro'yxat | `POST /xtrade/b/<route>:table` | Jadval ma'lumoti. |
| API: saqlash | `POST /xtrade/b/<route>:save yoki $save` | Kutish: page.waitForResponse(r => r.url().includes(':save')). |
| API: o'chirish/status | `POST /xtrade/b/<route>$delete \| $change_state \| $attach \| $detach` |  |
| API: hisobot | `/xtrade/b/<route>:run?rt=htmla\|xlsx\|csv\|xml` |  |
| Tarjima fayllari | `GET …/i18n/**.json` | 404 bo'lmasligi kerak (BUG-036 / TM-016). |
| Sessiya | `sessiya tugaganda /xtrade/login.html ga yo'naltirish kutiladi` | BUG-003. |

## Action lug'ati (JSON `steps[].action`)

| action | Ma'nosi |
|---|---|
| `nav` | Yuqori menyu orqali o'tish. target = "Menyu > [Bo'lim >] Band", value = route (bo'sh bo'lsa — menyu orqali). |
| `open_url` | page.goto(BASE_URL + target). |
| `menu_plus` | Menyu bandi yonidagi «+»: button[aria-label="<value>"] (menyu ochilgandan keyin ko'rinadi). |
| `click` | Ko'rinadigan matn bo'yicha tugma/havola. value = "confirm:<matn>\|<tugma>" bo'lsa, keyin tasdiqlash oynasida <tugma> bosiladi. |
| `row_click` | Ro'yxatda matni target ga mos .smt-data-row ichidagi .text-start katakni bosish (amal tugmalari chiqadi). |
| `row_action` | Bosilgan qator ostidagi amal tugmasi (target = tugma matni). |
| `fill` | Yorlig'i target bo'lgan input/textarea ga value yozish. |
| `fill_date` | Sana maydoni: bosish, Ctrl+A, value (dd.mm.yyyy) yozish, Escape. |
| `select` | smt-select / smt-data-select: bosish, value yozish, ArrowDown, Enter (variantlar .cdk-overlay-pane da). |
| `multiselect` | smt-multi-data-select: har bir value uchun select, oxirida Escape. |
| `remove_tag` | Teg yonidagi «×». |
| `toggle` | [role=switch] (yoki label[smt-checkbox] [role=checkbox]) holatini value (on/off) ga keltirish. |
| `radio` | Guruh target ichida value matnli radio. |
| `grid_fill` | Jadval: target = "<qator matni> \| <ustun sarlavhasi>", katakka value yozish (Подбор panelida ham). |
| `pick` | «Подбор» → panelda target qatori, value = "ustun=miqdor" → «Закрыть» → «Выбрать ТМЦ с заполненными данными?» → «Да». |
| `tab` | [role=tab] yoki wizard qadami, matni target. |
| `confirm` | [role=dialog] da target matni borligini tekshirib, value tugmasini bosish (odatda «Да»). |
| `dialog_close` | Ochiq xato/axborot oynasini target tugmasi bilan yopish. |
| `sequence` | Bir nechta atomar amal ketma-ket: «ops» ro'yxatidagi har bir element — yuqoridagi action'lardan biri. |
| `assert_text` | target joyida value matni borligini tekshirish. |
| `assert_row` | Ro'yxatda value ustun qiymatlari (\| bilan ajratilgan) bor qator mavjud. |
| `assert_field` | Ko'rish/tahrir sahifasida target yorlig'i yonidagi qiymat = value. |
| `assert_columns` | smt-cell-header matnlari value ro'yxatini o'z ichiga oladi. |
| `assert_buttons` | Ko'rinadigan tugmalar value ro'yxatiga mos. |
| `assert_api` | page.waitForResponse: URL target ga mos (masalan "**:save"), status = value. |
| `assert_no_request` | Amal paytida target ga mos so'rov yuborilmagan. |
| `assert_download` | page.waitForEvent('download'); fayl turi = value. |
| `assert_url` | URL target ni o'z ichiga oladi. |
| `observe` | Vizual/natijaviy tekshiruv: qadamning «expected» matni bo'yicha assertion yoziladi. |
| `wait` | Kutish (sekund). |
| `manual` | Avtomatlashtirish qiyin yoki bir necha sahifadan iborat qadam — description bo'yicha qo'lda yoki alohida helper bilan. |

## Route'lar

| Kalit | Route |
|---|---|
| setting_list | `/xtrade/a2/trade/tmcgf/setting_list` |
| setting_add | `/xtrade/a2/trade/tmcgf/setting+add` |
| setting_view | `/xtrade/a2/trade/tmcgf/setting_view?setting_id=<ID>` |
| setting_edit | `/xtrade/a2/trade/tmcgf/setting+edit?setting_id=<ID>` |
| setting_person | `/xtrade/a2/trade/tmcgf/setting_person_list?setting_id=<ID>&person_type_id=<ID>&mode=attached` |
| merch_list | `/xtrade/a2/trade/tvt/visit/merchandising_list` |
| merch_view | `/xtrade/a2/trade/tvt/visit/merchandising_view?merchandising_id=<ID>` |
| merch_edit | `/xtrade/a2/trade/tvt/visit/merchandising+edit?merchandising_id=<ID>` |
| robot_list | `/xtrade/a2/anor/mkpi/robot_plan_list` |
| robot_add | `/xtrade/a2/anor/mkpi/robot_plan+add` |
| robot_view | `/xtrade/a2/anor/mkpi/robot_plan_view?plan_id=<ID>&…` |
| room_list | `/xtrade/a2/anor/mkpi/room_plan_list` |
| room_add | `/xtrade/a2/anor/mkpi/room_plan+add` |
| room_view | `/xtrade/a2/anor/mkpi/room_plan_view?room_id=<ID>&plan_date=<dd.mm.yyyy>&…` |
| rp_list | `/xtrade/a2/anor/mkpi/room_product_plan_list` |
| rp_add | `/xtrade/a2/anor/mkpi/room_product_plan+add` |
| rpt_list | `/xtrade/a2/anor/mkpi/room_product_type_plan_list` |
| rpt_add | `/xtrade/a2/anor/mkpi/room_product_type_plan+add` |
| cl_list | `/xtrade/a2/anor/mkpi/client_plan_list` |
| cl_add | `/xtrade/a2/anor/mkpi/client_plan+add` |
| cp_list | `/xtrade/a2/anor/mkpi/client_product_plan_list` |
| cp_add | `/xtrade/a2/anor/mkpi/client_product_plan+add` |
| cpt_list | `/xtrade/a2/anor/mkpi/client_product_type_plan_list` |
| cpt_add | `/xtrade/a2/anor/mkpi/client_product_type_plan+add` |
| ctpt_list | `/xtrade/a2/anor/mkpi/client_type_product_type_plan_list` |
| ctpt_add | `/xtrade/a2/anor/mkpi/client_type_product_type_plan+add?group_mode=true&client_type=L` |
| tpl | `/xtrade/a2/anor/mkpi/plan_template` |
| tpl_set | `/xtrade/a2/anor/mkpi/plan_template_settings?kpi_kind=R` |
| bon_list | `/xtrade/a2/trade/tkpi/bonus_setting_list` |
| bon_add | `/xtrade/a2/trade/tkpi/bonus_setting+add` |
| bon_view | `/xtrade/a2/trade/tkpi/bonus_setting_view?bonus_setting_id=<ID>` |
| dash | `/xtrade/a2/anor/mkpi/kpi_dashboard` |
| pt_list | `/xtrade/a2/trade/tmcg/person_type_list` |
| pt_add | `/xtrade/a2/anor/mr/person/person_type+add?person_group_id=2383` |
| pt_edit | `/xtrade/a2/anor/mr/person/person_type+edit?person_group_id=2383&person_type_id=<ID>` |
| pt_bind | `/xtrade/a2/anor/mr/person/legal_person_type_bind_list?person_group_id=2383&person_type_id=<ID>` |
| mml_list | `/xtrade/a2/anor/mcg/mml_list` |
| mml_add | `/xtrade/a2/anor/mcg/mml+add` |
| mml_pt | `/xtrade/a2/anor/mcg/mml_person_type_list?mml_id=<ID>` |
| as_list | `/xtrade/a2/trade/tmcg/assortment_list` |
| as_add | `/xtrade/a2/trade/tmcg/assortment+add` |
| pg_list | `/xtrade/a2/trade/tmcg/planogram_sample_list` |
| pg_attach | `/xtrade/a2/trade/tmcg/planogram_sample_list+attach` |
| pg_view | `/xtrade/a2/trade/tmcg/planogram_sample_view?sample_id=<ID>` |
| pos_list | `/xtrade/a2/trade/tmcg/display_list` |
| rr_list | `/xtrade/a2/trade/tmcg/refuse_reason_list` |
| rr_add | `/xtrade/a2/trade/tmcg/refuse_reason+add` |
| rr_view | `/xtrade/a2/trade/tmcg/refuse_reason_view?reason_id=<ID>` |
| cmp_list | `/xtrade/a2/trade/tmcg/competitor_list` |
| qt_list | `/xtrade/a2/trade/rep/tvt/quiz/template_list` |
| qt_add | `/xtrade/a2/trade/rep/tvt/quiz/template+add` |
| qt_report | `/xtrade/a2/trade/rep/tvt/quiz/report?template_id=<ID>` |
| ci_list | `/xtrade/a2/trade/tmcg/competitor_inventory_list` |
| st_list | `/xtrade/a2/trade/tmcg/status_list` |
| rep_shelf_share | `/xtrade/a2/trade/tmcg/rep/shelf_share` |
| rep_assortment | `/xtrade/a2/trade/tmcg/rep/assortment` |
| rep_planogram | `/xtrade/a2/trade/tmcg/rep/planogram` |
| rep_shelf_price | `/xtrade/a2/trade/tmcg/rep/shelf_price` |
| rep_display | `/xtrade/a2/trade/tmcg/rep/display` |
| rep_score | `/xtrade/a2/trade/tmcg/rep/score` |
| rep_unavailable | `/xtrade/a2/trade/tmcg/rep/unavailable_inventories` |
| rep_price_cmp | `/xtrade/a2/trade/tmcg/rep/price_comparison` |
| rep_merch | `/xtrade/a2/trade/rep/tmcg/merchandising` |
| rep_photo | `/xtrade/a2/trade/rep/tvt/photo` |
| rep_competitors | `/xtrade/a2/trade/tmcg/rep/competitors` |
| rep_status | `/xtrade/a2/trade/tmcg/rep/status` |
| rep_mbi | `/xtrade/a2/trade/rep/mbi/tmcg/shelf_share` |
