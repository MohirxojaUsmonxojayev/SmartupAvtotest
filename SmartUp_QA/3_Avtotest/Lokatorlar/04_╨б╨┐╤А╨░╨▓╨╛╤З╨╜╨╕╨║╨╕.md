# Справочники — locators, API va route'lar

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
| tmc | `/xtrade/a2/anor/mr/product/inventory_list` |
| prc | `/xtrade/a2/anor/mkr/price_type_list` |
| srv | `/xtrade/a2/anor/mr/product/service_list` |
| mrg | `/xtrade/a2/anor/mkr/margin_list` |
| prd | `/xtrade/a2/anor/mr/product/producer_list` |
| pht | `/xtrade/a2/core/mvt/photo_type_list` |
| vdt | `/xtrade/a2/core/mvt/video_type_list` |
| cmt | `/xtrade/a2/core/mvt/comment_list` |
| qzs | `/xtrade/a2/anor/mqzm/quiz_set_list` |
| reg | `/xtrade/a2/anor/mr/region_list` |
| dvq | `/xtrade/a2/core/mqz/dv_quiz_list` |
| dvs | `/xtrade/a2/core/mqz/dv_quiz_set_list` |
| prs | `/xtrade/a2/trade/tr/presentation_list` |
| slr | `/xtrade/a2/trade/tr/store_seller_list` |
| npr | `/xtrade/a2/anor/mr/person/natural_person_list` |
| lpr | `/xtrade/a2/anor/mr/person/legal_person_list` |
| div | `/xtrade/a2/anor/mhr/division_list` |
| job | `/xtrade/a2/anor/mhr/job_list` |
| room | `/xtrade/a2/trade/trf/room_list` |
| rob | `/xtrade/a2/anor/mrf/robot_list` |
| cli | `/xtrade/a2/anor/mrf/client_list` |
| ntf | `/xtrade/a2/trade/tr/notification_list` |
| act | `/xtrade/a2/anor/mcg/action_list` |
| ovl | `/xtrade/a2/anor/mcg/overload_list` |
| rec | `/xtrade/a2/anor/mcg/recommend_list` |
| pst | `/xtrade/a2/anor/mrf/product_set_list` |
| kit | `/xtrade/a2/anor/mr/product_kit_list` |
| cqz | `/xtrade/a2/anor/mcg/categorization/quiz_list` |
| cnp | `/xtrade/a2/anor/mcg/categorization/natural_person_list` |
| clp | `/xtrade/a2/anor/mcg/categorization/legal_person_list` |
| crs | `/xtrade/a2/anor/mcg/categorization/result_list` |
| crp | `/xtrade/a2/anor/rep/mcg/category_results` |
| tgb | `/xtrade/a2/trade/txs/telegram/notification_list` |
| mml | `/xtrade/a2/anor/mcg/mml_list` |
| ors | `/xtrade/#/!<hash>/anor/mcg/order_restriction_list` |
| opl | `/xtrade/#/!<hash>/anor/mcg/order_product_limit/order_product_limit_list` |
