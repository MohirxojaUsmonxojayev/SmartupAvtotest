"""
E2E test ma'lumotlari — docs/e2e/E2E_test_cases.md dan.
Nomlardagi {d} → yugurish sanasi <DDMM> (rdate fixture).
"""


def names(d: str) -> dict:
    """QA-E2E-...-<DDMM> nomlar (d = rdate)."""
    return {
        "tmc":            f"QA-E2E-TMS-{d}",
        "tmc_code":       f"QA-E2E-{d}",
        "legal_person":   f"QA-E2E Postavshik MChJ {d}",
        "legal_code":     f"QA-E2E-YUR-{d}",
        "natural_person": f"QA-E2E Mijoz{d}",
        "natural_code":   f"QA-E2E-FIZ-{d}",
        "warehouse":      f"QA-E2E Sklad {d}",
        "purchase_req":   f"QA-E2E-ZR-{d}",
        "purchase_order": f"QA-E2E-ZZ-{d}",
        "purchase":       f"QA-E2E-ZK-{d}",
        "input_doc":      f"QA-E2E-PS-{d}",
        "contract":       f"QA-E2E-DOG-{d}",
        "pay1":           f"QA-E2E-PAY1-{d}",
        "pay2":           f"QA-E2E-PAY2-{d}",
    }


def tmc_full(d: str) -> dict:
    """TC-E2E-01 ТМЦ to'liq ma'lumoti (dropdownlar birinchi variant: muhitga bog'liq emas)."""
    return {
        "name":        f"QA-E2E-TMS-{d}",
        "unit":        "шт",
        "alt_name":    f"QA-E2E TMS alt {d}",
        "barcode1":    f"4780000{d}01",
        "barcode2":    f"4780000{d}02",
        "code":        f"QA-E2E-{d}",
        "order_no":    "999",
        "order_no_edit": "998",
        "ikpu":        "00000000000000001",
        "article":     f"QA-ART-{d}",
        "tnved":       "0000000000",
        "case1_qty":   "10",
        "case2_qty":   "5",
        "weight_net":  "1.2",
        "weight_gross": "1.5",
        "liter":       "0.75",
        "tip":         "Товар",     # Типы ТМЦ chip
    }


def legal_full(d: str) -> dict:
    """TC-E2E-03 Юридическое лицо (ta'minotchi) to'liq ma'lumoti. GPS/Файлы — mustasno (spec)."""
    return {
        "full_name":  f"QA-E2E Postavshik MChJ {d}",
        "alt_name":   "QA-E2E Postavshik",
        "code":       f"QA-E2E-YUR-{d}",
        "barcode":    f"4780000{d}11",
        "zip":        "100000",
        "web":        "qa-e2e.uz",
        "phone":      f"+99890{d[1:]}",        # UNIQUE, +998+9 raqam (dup_val_on_index oldini oladi)
        "telegram":   f"@qa_e2e_{d}",          # UNIQUE
        "email":      f"qa.e2e.{d}@example.com",  # UNIQUE
        "inn":        f"3{d}",                 # UNIQUE, 9 raqam (ИНН должен быть уникальным!)
        "oked":       "46900",
        "vat":        f"326{d}0",              # UNIQUE, 12 raqam (НДС дубликат bo'lmasin)
        "region":     "Toshkent",
        "address":    "Toshkent, QA ko'chasi 1",
        "orientir":   "QA mo'ljal",
        "post_addr":  "100000, Toshkent",
        # Расчетный счет (dialog)
        "bank_acc_name": "QA-E2E hisob",
        "bank_mfo":      "00014",
        "bank_name":     "Расчетно-кассовый центр Центрального банка по г. Ташкенту",  # МФО 00014
        "bank_acc_no":   f"202080009{d}000",   # UNIQUE, 20 raqam
        "bank_note":     "QA",
        # Контактные лица (dialog)
        "contact_fio":   "QA Kontakt",
        "contact_phone": "+998900000002",
        "contact_bday":  "01.01.1990",
        # Договор (dialog)
        "contract_name": f"QA-E2E shartnoma {d}",
        "contract_no":   f"QA-E2E-DOG-{d}",
        "contract_sum":  "10000000",
        # Примечание
        "note":          "QA-E2E izoh",
        # Руководящие должности
        "dir_first":  "Direktor", "dir_last": "QA", "dir_middle": "Testovich",
        "acc_first":  "Buxgalter", "acc_last": "QA", "acc_middle": "Testovna",
    }


def natural_full(d: str, legal_person: str = "") -> dict:
    """TC-E2E-04 Физическое лицо (mijoz) to'liq ma'lumoti. GPS/Файлы — mustasno.
    legal_person — «Юридическое лицо» ulanishi (TC-03 ta'minotchi); bo'sh bo'lsa select_first."""
    return {
        "surname":    "QA-E2E",
        "first_name": f"Mijoz{d}",             # Имя * (autocomplete, erkin matn)
        "middle":     "Testovich",
        "code":       f"QA-E2E-FIZ-{d}",
        "bday":       "01.01.1995",
        "passport":   f"AA{d[1:]}",            # 2 harf + 7 raqam (UNIQUE)
        "region":     "Toshkent",
        "address":    "Toshkent, QA 2",
        "post_addr":  "100000",
        "legal_person": legal_person,
        "phone":      f"+99891{d[1:]}",        # UNIQUE (legal'dan farqli prefiks)
        "pnfl":       f"3{d}00000",            # ПНФЛ 14 raqam (UNIQUE)
        "telegram":   f"@qa_mijoz_{d}",        # UNIQUE
        "email":      f"qa.mijoz.{d}@example.com",  # UNIQUE
        "web":        "qa-mijoz.uz",
        # Расчетный счет (TC-03 kabi)
        "bank_acc_name": "QA-E2E hisob FIZ",
        "bank_mfo":      "00014",
        "bank_name":     "Расчетно-кассовый центр Центрального банка по г. Ташкенту",
        "bank_acc_no":   f"202080009{d}001",   # UNIQUE 20 raqam
        "bank_note":     "QA",
        # Договор
        "contract_name": f"QA-E2E shartnoma FIZ {d}",
        "contract_no":   f"QA-E2E-DOGF-{d}",
        "contract_sum":  "5000000",
        # Примечание / Адреса доставки
        "note":          "QA-E2E mijoz izoh",
        "deliv_short":   f"QA yetkazish {d}",
        "deliv_full":    "Toshkent, QA yetkazish ko'chasi 2",
    }


# Doimiy qiymatlar (muhit ma'lumotiga tayanadi — kerak bo'lsa moslanadi)
ENV = {
    "unit":          "шт",                     # Ед. изм.
    "room":          "Room - Yashnobod",        # Рабочая зона (buyurtma uchun shart)
    "price_sell":    15000,                      # Sotish sum (Цена продажи)
    "price_buy":     10000,                      # Olish sum / xarid narxi (Цена закупа)
    "price_type_sell": "Sotish sum",             # TC-02: narx turi (Цена продажи, Узбекский сум)
    "price_type_buy":  "Olish sum",              # TC-02: narx turi (Цена закупа, Узбекский сум)
    "payment_type":  "Наличные деньги",
    "currency":      "Узбекский сум",
}

# Kutilgan raqamlar (har qadamда FARQ sifatida assert qilinadi)
EXPECTED = {
    "req_qty":        100,        # запрос miqdori
    "purchase_sum":   1_000_000,  # закупка (100 × 10 000)
    "order_qty":      30,          # sotuv buyurtmasi
    "order_sum":      450_000,     # 30 × 15 000
    "return_qty":     5,           # qaytarish
    "return_sum":     75_000,      # 5 × 15 000
    "pay1":           200_000,
    "pay2":           175_000,
    # qoldiq: 100 → (sotuvdan keyin доступно 70) → qaytarishdan keyin 75
    "stock_after_input":  100,
    "stock_after_return": 75,
    # mijoz qarzi: 450 000 → 375 000 (qaytarish) → 175 000 (pay1) → 0 (pay2)
    "client_debt_steps":  [450_000, 375_000, 175_000, 0],
    "supplier_debt":      1_000_000,
}
