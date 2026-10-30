# Наборы ТМЦ (Sector) — yaratish

Sector = **Набор ТМЦ** — mahsulot guruhi, product va room'ni birlashtiradi.

## Navigatsiya

- Menyu: **Справочники → ТМЦ → Наборы ТМЦ**
  - ТМЦ menyusiga kirgach `Наборы ТМЦ` link ko'rinadi
- Ro'yxat heading: `Наборы ТМЦ`
- Forma heading: `Набор ТМЦ (создание)`

## Forma maydonlari

Locatorlar oddiy — `get_by_role("textbox")` tartib bilan ishlaydi:

| # | Maydon | Locator | Qiymat |
|---|---|---|---|
| 1 | Kod | `textbox.first` | `code_sector_pw{code}` |
| 2 | Название | `textbox.nth(1)` | `sector-pw{code}` |
| 3 | Рабочие зоны | `get_by_role("textbox", name="Поиск")` → `get_by_text(f"room-pw{code}")` | `room-pw{code}` |

## Saqlash

`save_and_expect_heading("Наборы ТМЦ")` — biruni confirm yo'q.

Natija ro'yxatda:
- `code_sector_pw{code}` ko'rinadi
- `sector-pw{code}` ko'rinadi

## Dependency

- **Kerak bo'ladi:** room-pw{code} avval yaratilgan bo'lishi kerak
- **Downstream:** `test_product.py` — product yaratishda `sector-pw{code}` ko'rinishi kutiladi

## Test

- `tests/smoke/test_setup/test_sector.py` → `run_sector(page, code)`
