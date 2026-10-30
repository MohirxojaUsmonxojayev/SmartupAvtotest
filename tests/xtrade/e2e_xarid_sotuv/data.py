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


# Doimiy qiymatlar (muhit ma'lumotiga tayanadi — kerak bo'lsa moslanadi)
ENV = {
    "unit":          "шт",                     # Ед. изм.
    "room":          "Room - Yashnobod",        # Рабочая зона (buyurtma uchun shart)
    "price_sell":    15000,                      # Sotish sum
    "price_buy":     10000,                      # Olish sum / xarid narxi
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
