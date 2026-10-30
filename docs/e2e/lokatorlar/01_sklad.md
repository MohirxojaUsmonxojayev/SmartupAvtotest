# Склад — locators, API va route'lar

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
| init_balance_list | `/xtrade/a2/anor/mkw/init_balance/init_inventory_balance_list` |
| init_balance_add | `/xtrade/a2/anor/mkw/init_balance/init_inventory_balance+add` |
| init_balance_view | `/xtrade/a2/anor/mkw/init_balance/init_inventory_balance_view?balance_id=<ID>` |
| purchase_request_list | `/xtrade/a2/anor/mkw/purchase/purchase_request_list` |
| purchase_request_add | `/xtrade/a2/anor/mkw/purchase/purchase_request+add` |
| purchase_request_view | `/xtrade/a2/anor/mkw/purchase/purchase_request_view?request_id=<ID>` |
| purchase_list | `/xtrade/a2/anor/mkw/purchase/purchase_list` |
| purchase_add | `/xtrade/a2/anor/mkw/purchase/purchase+add` |
| order_list | `/xtrade/#/!<hash>/anor/mkw/purchase/order_list` |
| input_list | `/xtrade/a2/anor/mkw/input/input_list` |
| input_add | `/xtrade/a2/anor/mkw/input/input+add` |
| extra_cost_list | `/xtrade/a2/anor/mkw/extra_cost_list` |
| extra_cost_add | `/xtrade/a2/anor/mkw/extra_cost+add` |
| return_list | `/xtrade/a2/anor/mkw/return/return_list` |
| return_add | `/xtrade/a2/anor/mkw/return/return+add` |
| return_view | `/xtrade/a2/anor/mkw/return/return_view?return_id=<ID>` |
| writeoff_list | `/xtrade/a2/anor/mkw/writeoff/writeoff_list` |
| writeoff_add | `/xtrade/a2/anor/mkw/writeoff/writeoff+add` |
| writeoff_view | `/xtrade/a2/anor/mkw/writeoff/writeoff_view?writeoff_id=<ID>` |
| writeoff_edit | `/xtrade/a2/anor/mkw/writeoff/writeoff+edit?writeoff_id=<ID>` |
| stocktaking_list | `/xtrade/a2/anor/mkw/stocktaking/stocktaking_list` |
| stocktaking_add | `/xtrade/a2/anor/mkw/stocktaking/stocktaking+add` |
| revaluation_list | `/xtrade/a2/anor/mkw/revaluation/revaluation_list` |
| revaluation_edit | `/xtrade/a2/anor/mkw/revaluation/revaluation+edit?revaluation_id=<ID>` |
| offset_list | `/xtrade/a2/anor/mkw/purchase/offset/offset_list` |
| recalculate_input | `/xtrade/a2/anor/mkw/recalculate_input` |
| aggregation_list | `/xtrade/a2/anor/mkw/marking/aggregation_list` |
| disaggregation_list | `/xtrade/a2/anor/mkw/marking/disaggregation_list` |
| withdraw_list | `/xtrade/a2/anor/mkw/marking/withdraw_list` |
| withdraw_add | `/xtrade/a2/anor/mkw/marking/withdraw+add` |
| forecast_list | `/xtrade/a2/anor/mfc/forecast_list` |
| forecast_add | `/xtrade/a2/anor/mfc/forecast+add` |
| movement_request_list | `/xtrade/a2/anor/mkw/movement/movement_request_list` |
| movement_request_add | `/xtrade/a2/anor/mkw/movement/movement_request+add` |
| movement_list | `/xtrade/a2/anor/mkw/movement/movement_list` |
| movement_add | `/xtrade/a2/anor/mkw/movement/movement+add` |
| movement_view | `/xtrade/a2/anor/mkw/movement/movement_view?movement_id=<ID>` |
| spread_balance_movement | `/xtrade/a2/anor/mkw/movement/spread_balance_movement` |
| from_movement_request_list | `/xtrade/a2/anor/mfm/from_movement_request_list` |
| from_movement_request_add | `/xtrade/a2/anor/mfm/from_movement_request+add` |
| to_movement_request_list | `/xtrade/a2/anor/mfm/to_movement_request_list` |
| from_movement_list | `/xtrade/a2/anor/mfm/from_movement_list` |
| from_movement_add | `/xtrade/a2/anor/mfm/from_movement+add` |
| from_movement_view | `/xtrade/a2/anor/mfm/from_movement_view?movement_id=<ID>` |
| to_movement_list | `/xtrade/a2/anor/mfm/to_movement_list` |
| from_movement_history_list | `/xtrade/a2/anor/mfm/from_movement_history_list` |
| cancelled_from_movement_list | `/xtrade/a2/anor/mfm/cancelled_from_movement_list` |
| supplier_list | `/xtrade/a2/anor/mkw/supplier_list` |
| supplier_add | `/xtrade/a2/anor/mkw/supplier+add` |
| supplier_view | `/xtrade/a2/anor/mkw/supplier_view?supplier_id=<ID>` |
| van_list | `/xtrade/a2/anor/mrf/van_list` |
| van_add | `/xtrade/a2/anor/mrf/van+add` |
| van_marking_balance | `/xtrade/a2/trade/tdeal/van_marking_balance?van_id=<ID>&van_name=<NAME>` |
| warehouse_list | `/xtrade/a2/anor/mkw/warehouse_list` |
| warehouse_add | `/xtrade/a2/anor/mkw/warehouse+add` |
| warehouse_view | `/xtrade/a2/anor/mkw/warehouse_view?warehouse_id=<ID>` |
| balance_list | `/xtrade/a2/anor/mkw/balance/balance_list` |
| expiration_date | `/xtrade/a2/anor/pref/expiration_date` |
| marking_balance | `/xtrade/a2/anor/mm/marking_balance` |
| product_serials | `/xtrade/a2/anor/mkw/product_serials` |
| wms | `/xtrade/a2/anor/mxsx/wms/document_list` |
| logistics_list | `/xtrade/a2/trade/tdeal/logistics_list` |
| logistics_add | `/xtrade/a2/trade/tdeal/logistics+add` |
| rep_inventories | `/xtrade/a2/anor/rep/mkw/warehouse_inventories` |
| rep_warehouse_balance | `/xtrade/a2/anor/rep/mkw/warehouse_balance/warehouse_balance` |
| rep_mbi_movement | `/xtrade/a2/anor/rep/mbi/mkw/movement` |
| rep_mbi_purchase_request | `/xtrade/a2/anor/rep/mbi/mkw/purchase_request` |
| rep_mbi_purchase | `/xtrade/a2/anor/rep/mbi/mkw/purchase` |
| rep_mbi_input | `/xtrade/a2/anor/rep/mbi/mkw/input` |
| rep_mbi_writeoff | `/xtrade/a2/anor/rep/mbi/mkw/writeoff` |
| rep_mbi_mfm_request | `/xtrade/a2/anor/rep/mbi/mfm/movement_request` |
| rep_mbi_mfm_movement | `/xtrade/a2/anor/rep/mbi/mfm/movement` |
| rep_shipment | `/xtrade/a2/trade/rep/warehouse_and_delivery` |
