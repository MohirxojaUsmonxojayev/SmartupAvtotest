# Рабочая зона (Room) — yaratish va prikreplenie

Room = **Рабочая зона**. Test: `tests/smoke/test_setup/test_room.py` (`run_room`, `run_room_attachment`).

## Navigatsiya

- Ro'yxat: **Справочники → Рабочие зоны** (user menyusida; admin'da filialga o'tilgach ko'rinadi). URL: `.../trade/trf/room_list`.
- Yaratish: `Создать` → `Рабочая зона (создание)`; code + nom + `Активный`.
- Prikreplenie: room qatorini bosib → **`Прикрепление`** tugmasi → `Рабочая зона (прикрепление): room-pw{code}` (`.../anor/mrf/room_attachment?room_id=<id>`).

## Create Form Locator/Loader Notes

Tags: room, locator, loader, helper
- 2026-06-26 debug: `Создать` bosilgandan keyin `room+add` sahifasida blocking loader/title kech yuklanishi mumkin; heading assertdan oldin `BasePage(page).wait_for_loader()` chaqirilsin.
- Label helper: `Код` va `Название` ketma-ket maydonlar. Keng card/col konteyneridagi birinchi inputni olish `Название` qiymatini `Код` inputiga yozib yuboradi. `BasePage.input(...)` labeldan keyingi birinchi real inputni target qilishi kerak.
- Screenshot: `references/forms/screenshots/room/room__add-loader__desktop-20260626.png`.

## Прикрепление tablari (link role)

`Штаты`, **`Тип цены`**, `Типы оплат`, `Наборы ТМЦ`, `Скидки/наценки`, `Склады`, `Кассы`, `Расчетные счета`, `Проект`, `Юридические лица`, `Физические лица`, `Акции`, `Ограничения`, `Опросник`, `Технологические карты`.

`run_room_attachment` ulaydigan: Типы оплат, Склады, Кассы, Физические лица (mijoz), **Тип цены (Акция)**.

### Oddiy tablar patterni (Типы оплат / Склады / Кассы / Физические лица)
`link → expect b-page text → "Доступные" → (grid checkall yoki kerakli qatorni bosish) → "Прикрепить" → confirm_biruni("Прикрепить N?" / "...nomi?") → "Прикрепленные"da tekshirish`.

### "Тип цены" tab — ikki bosqichli ulash (MUHIM, MCP bilan 2026-06-16 tasdiqlangan)
"Доступные" boshida **bo'sh** (нет данных) — narx turini avval katalogdan room'ga qo'shish kerak. Shuning uchun ulash 2 bosqich:

1. **Katalogdan Доступныега qo'shish**: `Тип цены` link → `Доступные` → **`Создать тип цены`** (→ `Цены (прикрепление)` sahifa, `.../anor/mkr/price_type_list+attach`, katalog: Промо/Акция/Возврат/Передача забаланс/Обмен) → kerakli qatorni (mas. `Акция`) bosish → qatorda **`Прикрепить`** → `confirm_biruni("Прикрепить Акция?")`. Bu room_attachment'ga qaytaradi va `Акция`ni **Доступные**ga qo'shadi.
2. **Доступныеdan Прикрепленныега**: `Тип цены` link → `Доступные` → `Акция` qatorini bosish → qatorda **`Прикрепить`** → `confirm_biruni("Прикрепить Акция?")`. Endi `Прикрепленные`da `Акция` (PRCT:2) ko'rinadi.

⚠️ Faqat 1-bosqich qilinsa, `Акция` Доступныеда qoladi (Прикрепленныеда faqat setup'dagi `Price Type UZB-pw{code}` bo'ladi) — order'da aksiya chegirmasi ishlamaydi.

Setupdagi `Price Type UZB-pw{code}` room'ga narx turi FORMASI orqali ("Выбранных" rooms) ulanadi — bu Тип цены prikreplenie tabidan boshqa, alohida bog'lanish.

## Nega kerak
Room'ga `Акция` narx turi ulanmasa, C-group aksiya chegirmasi order'ning "Акции" tabида `Тип цены акции не прикреплен к рабочей зоне...` xatosi bilan ishlamaydi. To'liq aksiya zanjiri: [action.md].
