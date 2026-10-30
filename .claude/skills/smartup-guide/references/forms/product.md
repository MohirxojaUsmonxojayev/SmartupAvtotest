# ТМЦ (Product) — yaratish va narx belgilash

Product = **ТМЦ** (Товарно-материальная ценность). Smoke testda bitta product yaratiladi va unga 7000 UZS narx qo'yiladi.

## Navigatsiya

- Menyu: **Справочники → ТМЦ**
- Ro'yxat heading: `ТМЦ`
- Yaratish heading: `ТМЦ (создание)`
- Narx belgilash heading: `ТМЦ (установка цен)`

## Forma maydonlari (yaratish)

| Maydon | Locator | Qiymat |
|---|---|---|
| Название | `#anor66-input-text-name` textbox | `product-pw{code}` |
| Ед. изм (o'lchov) | `#anor66-input-text-measure_short_name` Поиск → `шт` | `шт` |
| Код | `.col-sm-12.mb-4 > .form-control` | `code_product-pw{code}` |
| Тип ТМЦ | `get_by_text("Товар", exact=True).click()` | `Товар` |

**Precondition tekshiruvi:** forma ichida `sector-pw{code}` ko'rinishi kerak — sector yaratilmagan bo'lsa product to'g'ri guruhlanmaydi.

## Saqlash pattern

```python
BasePage(page).save_and_expect_heading("ТМЦ", ...)
# biruni confirm yo'q yaratishda
```

Ro'yxatda: `code_product-pw{code}` ko'rinadi.

## Narx belgilash (ikkinchi qadam)

Yaratilgan product qatori bosilgach:

```
"Установить цены" button → "ТМЦ (установка цен)" heading
→ b-pg-grid textbox.fill("7000")
→ save_and_expect_heading("ТМЦ", confirm_text="Сохранить?")
```

Narx = **7000** (UZS). Bu qiymat C-group aksiya testida ishlatiladi: 10 × 7000 = 70 000, 10% skidka → 63 000.

## Downstream ta'siri

- `action.md` C-01/C-02: `product-pw{code}` x10 = 70 000; 10% skidka = 63 000
- `order-add.md`: product sifatida ishlatiladi

## Test

- `tests/smoke/test_setup/test_product.py` → `run_product(page, code)`
