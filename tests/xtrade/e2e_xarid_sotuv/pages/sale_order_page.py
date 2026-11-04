"""
Заказ (sotuv buyurtmasi) — a2 3-qadamli WIZARD page object (TC-E2E-12).
Ro'yxat: /a2/trade/tdeal/order/order_list ; create → title «Заказ (создание)».
DIQQAT: bu a2 (smt-*), ESKI UI EMAS. «Старый интерфейс» tugmasiga TEGILMAYDI.

Jonli tasdiqlangan (2026-11-04) — 3 qadam stepper (Основное / ТМЦ / Завершение):
  Step1 «Основное»: Дата отгрузки (date), Рабочая зона* (Room), Штат, Клиент* (zona bo'yicha
    filtrlanadi). → «Далее».
  Step2 «ТМЦ»: «Подбор» tugma → drawer «Заказ (подбор)». Drawer'да Склад* + Тип цены* tanlanadi →
    «Доступные» grid'да ТМЦ chiqadi (SHARTlar: narx «Цена с НДС и акцизом» + stok). Qatorда Кол-во
    yoziladi → qator «+» (svg-icon-plus) → ТМЦ «Выбранные» ga o'tadi. Drawer YUQORI-O'NG «X»
    (svg-icon-x-close) bilan yopilsa tanlov buyurtmaga QO'LLANADI; «Закрыть» esa BEKOR qiladi!
    So'ng grid'да qator (Цена/Остаток/Кол-во/Сумма) ko'rinadi, ИТОГО = Кол-во×Цена. → «Далее».
  Step3 «Завершение»: Тип оплаты, ТТН/СФ (ixtiyoriy), Статус* (Новый), «Заказ» raqam (avto).
    Finalize = «Сохранить».

MUHIM (sellability): ТМЦ Подбор'да ko'rinishi uchun «Sotish sum» narx turining «Цена с НДС и акцизом»
  ustuni to'ldirilган bo'lishi SHART (TC-02 set_price buni bajaradi) + omborда stok (TC-08..11).
"""
import datetime
import re

from playwright.sync_api import expect

from utils.base_page import BasePage


class SaleOrderPage:
    LIST_PATH = "/a2/trade/tdeal/order/order_list"
    RETURN_PATH = "/a2/anor/mdeal/order/return"   # «Возврат/Отказ» — deal_id bo'yicha

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    # ---- navigatsiya ----------------------------------------------------------------------------
    def open_list(self):
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.page.wait_for_timeout(800)

    def open_create(self):
        self.page.get_by_role("button", name="Создать", exact=True).first.click()
        self.b.expect_form_open("создани")
        self.page.wait_for_timeout(2_000)

    def _next(self):
        self.page.get_by_role("button", name="Далее", exact=True).first.click()
        self.page.wait_for_timeout(3_000)

    def _pick(self, label: str, text: str, *, exact: bool = False):
        """Asosiy forma smt-data-select: trigger → qidiruv → variant (ko'rinadigan pane'dan) → yopish.
        base.select ba'zi to'la-select'larда ishonchsiz; shu proven pattern'ни ishlatamiz."""
        self.b._open_select(label)
        self.page.wait_for_timeout(1_000)
        box = self.page.locator(".cdk-overlay-container input").first
        if box.count() > 0:
            box.fill(text)
            self.page.wait_for_timeout(1_800)
        self.page.locator(".cdk-overlay-pane").get_by_text(text, exact=exact).first.click()
        self.page.wait_for_timeout(400)
        self.b._close_overlay()

    # ---- Step 1 «Основное» ----------------------------------------------------------------------
    def step1_main(self, zona: str, shtat: str, client: str):
        """Дата отгрузки=bugun, Рабочая зона, Штат, Клиент → Далее."""
        today = datetime.date.today().strftime("%d.%m.%Y")
        el = self.b.control("Дата отгрузки").locator("input").first
        el.click(); el.press("ControlOrMeta+A"); el.press("Backspace"); el.fill(today)
        self.page.wait_for_timeout(200)
        self.page.locator("main").get_by_text("Дата заказа", exact=False).first.click()  # kalendar yopish
        self.page.wait_for_timeout(300)
        self._pick("Рабочая зона", zona)
        self.page.wait_for_timeout(1_500)
        self._pick("Штат", shtat)
        self.page.wait_for_timeout(600)
        self._pick("Клиент", client)
        self.page.wait_for_timeout(1_000)
        self._next()

    # ---- Step 2 «ТМЦ» (Подбор) ------------------------------------------------------------------
    def _dpick(self, label: str, text: str, *, exact: bool = True):
        """Drawer-safe select: ENG YANGI pane'da qidiradi, Escape ISHLATMAYDI (Escape drawer'ni yopadi)."""
        self.b.control(label).locator("smt-select-trigger, smt-data-select, input").first.click()
        self.page.wait_for_timeout(1_200)
        pane = self.page.locator(".cdk-overlay-pane").last
        box = pane.locator("input").first
        if box.count() > 0:
            box.fill(text)
            self.page.wait_for_timeout(1_800)
        pane.get_by_text(text, exact=exact).first.click()
        self.page.wait_for_timeout(1_500)

    def step2_podbor(self, sklad: str, price_type: str, product: str, qty: int) -> str:
        """«Подбор» drawer: Склад + Тип цены → qatorда Кол-во → «+» → X-close. ИТОГО (raqam) qaytaradi."""
        self.page.get_by_role("button", name="Подбор", exact=False).first.click()
        self.page.wait_for_timeout(3_000)
        self._dpick("Склад", sklad)
        self._dpick("Тип цены", price_type)
        self.page.wait_for_timeout(2_500)
        row = self.page.locator(".smt-data-row").filter(has_text=product).first
        expect(row).to_be_visible(timeout=15_000), \
            f"«{product}» Подбор'да yo'q — narx «Цена с НДС и акцизом» yoki stok yetishmaydi"
        # Кол-во input = «10 /бл» (Кол-во кейсов) placeholderli inputдан oldingi
        inps = row.locator("input[type=text]")
        kol_idx = 0
        for i in range(inps.count()):
            if (inps.nth(i).get_attribute("placeholder") or "").startswith("10"):
                kol_idx = i - 1
                break
        kol = inps.nth(kol_idx)
        kol.click(); kol.fill(str(qty)); kol.press("Tab")
        self.page.wait_for_timeout(1_500)
        row.locator("[class*=svg-icon-plus]").first.click()   # «Выбранные» ga qo'shish
        self.page.wait_for_timeout(1_800)
        # YUQORI-O'NG X bilan yopish → tanlov QO'LLANADI (Закрыть bekor qiladi!)
        self.page.locator(".cdk-overlay-pane [class*=svg-icon-x-close]").first.click()
        self.page.wait_for_timeout(2_500)
        return self._read_itogo()

    def _read_itogo(self) -> str:
        m = re.search(r"ИТОГО:\s*([\d\s ]+)", self.page.locator("body").inner_text())
        return re.sub(r"\D", "", m.group(1)) if m else ""

    # ---- Step 3 «Завершение» --------------------------------------------------------------------
    def step3_finish(self, payment_type: str, status: str = "Новый",
                     ttn: str | None = None, sf: str | None = None, number: str | None = None):
        """Тип оплаты, (ТТН/СФ ixtiyoriy), «Заказ» raqam (agar tahrirlansa), Статус → «Сохранить»."""
        self._next()  # ТМЦ → Завершение
        try:
            self._pick("Тип оплаты", payment_type)
        except Exception:
            print(f"  [sale] «Тип оплаты»={payment_type} tanlanmadi (default qoldi)")
            self.b._close_overlay()
        if ttn is not None:
            try:
                self.b.input(label="Номер товарно-транспортной накладной", value=ttn)
            except Exception:
                pass
        if sf is not None:
            try:
                self.b.input(label="Номер счет-фактуры", value=sf)
            except Exception:
                pass
        if number is not None:
            try:
                el = self.b.control("Заказ").locator("input").first
                if el.is_editable():
                    el.click(); el.press("ControlOrMeta+A"); el.press("Backspace"); el.fill(number)
            except Exception:
                pass
        try:
            self._pick("Статус", status, exact=True)
        except Exception:
            print(f"  [sale] «Статус»={status} tanlanmadi (default qoldi)")
            self.b._close_overlay()
        # finalize
        self.b.save()  # «Сохранить»
        self.page.wait_for_timeout(1_000)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(2_500)

    def _confirm_yes_if_any(self):
        try:
            dlg = self.page.locator("[role=dialog], .cdk-dialog-container").last
            btn = dlg.get_by_role("button", name="Да", exact=False).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                self.page.wait_for_timeout(600)
        except Exception:
            pass

    # ---- tekshirish -----------------------------------------------------------------------------
    # Sotuv buyurtma ro'yxatida matnli «номер» ustuni YO'Q (ustunlar: ТМЦ/Номер ТТН/Источник/
    # ИД заказа/Рабочая зона/Клиент/Штат/Дата.../Сумма/Статус). Buyurtma zanjirда KLIENT + «Новый»
    # holat orqali aniqlanadi (TC-13 Доставка Подбор'да klient/zona bo'yicha tanlaydi).
    def expect_in_list(self, client: str):
        self.open_list()
        self.b.search_list(client)
        self.page.wait_for_timeout(1_500)
        expect(self.page.locator("smt-data-table").get_by_text(client, exact=False).first
               ).to_be_visible(timeout=10_000)

    _STATUSES = ("Черновик", "Новый", "В обработке", "В ожидании", "Отгружен", "Доставлен", "Архив", "Отменен")

    def _row_status(self, row) -> str:
        """Qator matnidan joriy Статусni ajratadi."""
        txt = row.inner_text() or ""
        for st in self._STATUSES:
            if re.search(rf"(?<!\w){re.escape(st)}(?!\w)", txt):
                return st
        return ""

    def latest_status(self, client: str) -> str:
        """Klient bo'yicha qidirib, eng yangi buyurtma qatorining Статус hujayrasini qaytaradi."""
        self.open_list()
        self.b.search_list(client)
        self.page.wait_for_timeout(2_000)
        row = self.page.locator("smt-data-table .smt-data-row").first
        expect(row).to_be_visible(timeout=10_000)
        return self._row_status(row)

    def capture_id(self, client: str) -> str:
        """Klient bo'yicha eng yangi buyurtma qatoridan «ИД заказа» (5+ xonali raqam) ni qaytaradi.
        Статус-o'zgartirishда buyurtmani aniq nishonlash uchun (bir klientда bir necha buyurtma bo'lsa)."""
        self.open_list()
        self.b.search_list(client)
        self.page.wait_for_timeout(2_000)
        row = self.page.locator("smt-data-table .smt-data-row").first
        expect(row).to_be_visible(timeout=10_000)
        m = re.search(r"\d{5,}", (row.inner_text() or "").replace(" ", "").replace(" ", ""))
        # DIQQAT: Сумма (450000) probel bilan render bo'ladi; ИД ustuni Сумма'dan oldin keladi va
        # probelsiz raqam — probellarni olib tashlab birinchi 5+ xonali ketma-ketlikni olamiz.
        row_raw = row.inner_text() or ""
        m2 = re.search(r"(?<!\d)\d{5,7}(?!\d)", row_raw)
        return (m2.group(0) if m2 else (m.group(0) if m else ""))

    def _find_row(self, client: str, order_id: str):
        """Klient bo'yicha qidirib (ro'yxat qidiruvi ИД заказа BO'YICHA ishlamaydi!), qatorni
        «ИД заказа» matni bilan filtrlab topadi."""
        self.open_list()
        self.b.search_list(client)
        self.page.wait_for_timeout(2_000)
        row = self.page.locator("smt-data-table .smt-data-row").filter(has_text=order_id).first
        expect(row).to_be_visible(timeout=10_000)
        return row

    def change_status(self, client: str, order_id: str, to_status: str):
        """Buyurtmani (ИД заказа bo'yicha) `to_status` ga o'tkazadi: Статус hujayra dropdown →
        menuitem → «Изменить статус на …?» → «Да». Joriy status = to_status bo'lsa — o'tkazmaydi."""
        row = self._find_row(client, order_id)
        cur = self._row_status(row)
        if cur == to_status:
            return
        # Статус hujayra dropdown trigger = qatorда joriy status matni
        row.get_by_text(cur, exact=True).first.click()
        self.page.wait_for_timeout(1_500)
        self.page.locator(".cdk-overlay-pane").get_by_text(to_status, exact=True).first.click()
        self.page.wait_for_timeout(1_200)
        self._confirm_yes_if_any()   # «Изменить статус на …?» → Да
        self.page.wait_for_timeout(2_500)

    def expect_status(self, client: str, order_id: str, status: str):
        """ИД заказа bo'yicha qatorда kutilgan status borligini tekshiradi."""
        got = self._row_status(self._find_row(client, order_id))
        assert got == status, f"Buyurtma {order_id} holati kutilgan «{status}», lekin «{got}»"

    # ---- Qisman qaytarish («Отказ»/«Возврат») ---------------------------------------------------
    # Доставлен buyurtmadan qisman qaytarish — forma: /a2/anor/mdeal/order/return?deal_id=<ИД>.
    # a2 UI'да «Отказ» qator-amali to'g'ridan-to'g'ri ko'rinmaydi (Отказы ro'yxatida «Создать» yo'q,
    # order_view/toolbar'да ham yo'q) → forma deal_id (= «ИД заказа») bilan URL orqали ochiladi.
    # DIQQAT: a2 chuqur route'ni to'g'ridан goto qilish ba'zan bo'sh sahifa beradi — avval order_list
    # bilan SPA isitiladi, keyin return URL'ga o'tiladi.
    def _order_sum(self) -> str:
        """«Сумма заказа» (RO) maydon qiymati — raqamlar."""
        c = self.page.locator("smt-control").filter(has_text="Сумма заказа").first
        return re.sub(r"\D", "", c.locator("input").first.input_value() or "")

    def open_return(self, order_id: str):
        self.open_list()  # SPA'ni isitadi
        self.page.goto(f"{self.base_url}{self.RETURN_PATH}?deal_id={order_id}",
                       wait_until="commit", timeout=60_000)
        self.page.get_by_text("Причина возврата", exact=False).first.wait_for(state="visible", timeout=30_000)
        self.page.wait_for_timeout(2_000)
        expect(self.page.get_by_text("Возврат", exact=True).first).to_be_visible(timeout=10_000)

    def partial_return(self, order_id: str, return_qty: int, reason: str = "Обмен") -> str:
        """Доставлен buyurtmadan `return_qty` dona qaytaradi: grid «Возврат» ustunига qty yoziladi,
        Причина возврата tanlanadi, «Сохранить» → «Сохранить?» да. Qaytarishдан keyingi «Сумма
        заказа» (raqamlar) qaytaradi (kutilgan: dastlabki − return_qty×narx)."""
        self.open_return(order_id)
        # Возврат input = qatorдаgi yagona text input (search type=search chiqib ketadi)
        vinp = self.page.locator(".smt-data-row input[type=text], smt-data-table input[type=text]").first
        vinp.click(); vinp.press("ControlOrMeta+A"); vinp.press("Backspace")
        vinp.fill(str(return_qty)); vinp.press("Tab")
        self.page.wait_for_timeout(1_500)
        sum_after = self._order_sum()
        self._pick("Причина возврата", reason, exact=True)
        self.b.save()
        self.page.wait_for_timeout(1_000)
        self._confirm_yes_if_any()   # «Сохранить?» → Да
        self.page.wait_for_timeout(2_500)
        return sum_after

    def expect_return_persisted(self, order_id: str, expected_sum: int):
        """Qaytarish SAQLANGANini mustaqil tasdiqlaydi: return formани QAYTA ochib (yangi yuklash),
        «Сумма заказа» kutilgan (qaytarishдан keyingi) qiymatда ekanini tekshiradi — partial_return
        qiymatni saqlashдан OLDIN o'qigani uchun bu false-positivedan himoya qiladi."""
        self.open_return(order_id)
        got = self._order_sum()
        assert got == str(expected_sum), (
            f"Qaytarish saqlanmagan ko'rinadi: buyurtma {order_id} «Сумма заказа» yangi yuklashда "
            f"kutilgan {expected_sum}, lekin '{got}'.")
