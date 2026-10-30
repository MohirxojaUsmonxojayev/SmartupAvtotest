# E2E — Xarid → Sotuv → Qaytarish → To'lov (bitta ssenariy)

Manba: `docs/e2e/E2E_test_cases.md` (TC-E2E-01…18, 30.10.2026 qo'lda yugurishdan).

## Dizayn: bitta forma = bitta test, birlashganda 1 ssenariy

Har bir forma alohida fayl (`test_01_...` … `test_17_...`). Fayl nomidagi raqam **tartibni**
belgilaydi (pytest alfavit bo'yicha yuritadi) — birgalikda to'liq biznes sikli hosil bo'ladi.

| Fayl | TC | Forma | UI |
|------|-----|-------|-----|
| test_01_tmc.py | 01 | ТМЦ yaratish | a2 |
| test_02_price.py | 02 | Narx o'rnatish | a2 |
| test_03_legal_person.py | 03 | Юр. лицо (ta'minotchi) | a2 |
| test_04_natural_person.py | 04 | Физ. лицо (mijoz) | a2 |
| test_05_supplier.py | 05 | Поставщик + ТМЦ bog'lash | a2 |
| test_06_warehouse.py | 06 | Склад | a2 |
| test_07_client.py | 07 | Клиент (avto) | a2 |
| test_08_purchase_request.py | 08 | Запрос на закупку | a2 |
| test_09_purchase_order.py | 09 | Заказ на закупку (wizard) | **eski** |
| test_10_purchase.py | 10 | Закупка | a2 |
| test_11_input.py | 11 | Поступление ТМЦ | a2 |
| test_12_sales_order.py | 12 | Sotuv buyurtmasi (wizard) | **eski** |
| test_13_delivery.py | 13 | Yetkazish (status) | **eski** |
| test_14_return.py | 14 | Qisman qaytarish | **eski** |
| test_15_archive.py | 15 | Arxiv + qarz | **eski** |
| test_16_payment.py | 16 | Mijozdan to'lov | a2 |
| test_17_verify.py | 17 | Yakuniy solishtiruv | a2+eski |

## Umumiy holat va sessiya
- `e2e_page` — bitta brauzer sessiyasi (login + filial), barcha testlar birga ishlatadi (fixture `conftest.py`).
- `e2e` — yaratilgan ID/raqamlar (`test-results/e2e_state.json` ga yoziladi) — yiqilgan joydan davom etish uchun.
- `rdate` — yugurish sanasi `<DDMM>` (nomlarда `QA-E2E-...-<DDMM>`).
- Har qadamда qoldiq/summa/qarz **farq** sifatida assert qilinadi (TC-E2E-01…17 kutilgan raqamlar `data.py` da).

## Eslatma
- `test_09/12/13/14/15` — **eski UI** (wizard, sessiya-token URL). Bular uchun Biruni helper kerak bo'ladi
  (hozir a2 `utils/base_page.py` bor; eski UI'ga kelganda qo'shamiz).
- Ssenariy oldindan mavjud ma'lumotga tayanadi (Room - Yashnobod, narx turlari va h.k.) — test ma'lumoti
  `data.py` da, kerak bo'lsa moslanadi.
- Ishga tushirish: `pytest tests/xtrade/e2e_xarid_sotuv -m e2e` (yoki bitta forma: `pytest .../test_01_tmc.py`).
