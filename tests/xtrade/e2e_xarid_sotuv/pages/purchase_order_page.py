"""
Заказ на закупку (xarid buyurtmasi) — a2 4-qadamli WIZARD page object (TC-E2E-09).
Ro'yxat: /a2/anor/mkw/purchase/order_list ; create: order_add (title «Заказ на закупку (создание)»).
DIQQAT: bu a2 (smt-*), ESKI UI EMAS. «Старый интерфейс» tugmasiga TEGILMAYDI.

Jonli tasdiqlangan (mohir@xan, 2026-11-03) — 4 qadam stepper (Основное/ТМЦ/Поставщик/Завершение):
  Step1 «Основное»: Дата заказа* (default bugun), Дата поставки (date), Валюта* (default «Узбекский сум»). → «Далее».
  Step2 «ТМЦ»: «Поиск запроса на закупку» (placeholder search) → ZR tanlansa Дата запроса/Крайний срок/
    Примечание to'ladi va grid'ga zapros qatorlari (ТМЦ×Кол-во) tushadi. Qatorda smt-data-select:
    nth(0)=Название/ТМЦ (to'la), nth(1)=Поставщик, nth(2)=Договор → to'ldiriladi. «Дополнительный подбор
    ТМЦ» (Поиск ТМЦ) — ixtiyoriy. → «Далее».
  Step3 «Поставщик»: grid ustunlar Название/Ед.изм/Номер карточки/Кол-во/Цена/Скидка/НДС/ИТОГО.
    Цена kiritilsa ИТОГО = Кол-во×Цена avto. → «Далее».
  Step4 «Завершение»: Номер заказа, Статус (default/«Принято»), Примечание → «Завершить»/«Сохранить».
"""
import datetime
import re

from playwright.sync_api import expect

from utils.base_page import BasePage


class PurchaseOrderPage:
    LIST_PATH = "/a2/anor/mkw/purchase/order_list"
    SECTION = "Основное"

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
        self.page.wait_for_timeout(1_500)

    def _next(self):
        self.page.get_by_role("button", name="Далее", exact=False).first.click()
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

    # ---- Step 1 «Основное» ----------------------------------------------------------------------
    def step1_main(self):
        """Дата поставки = +7 kun (Дата заказа/Валюта default). → Далее."""
        due = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%d.%m.%Y")
        el = self.b.control("Дата поставки").locator("input").first
        el.click(); el.press("ControlOrMeta+A"); el.press("Backspace"); el.fill(due)
        self.page.wait_for_timeout(200)
        self.page.locator("main").get_by_text("Дата заказа", exact=False).first.click()  # kalendar yopish
        self.page.wait_for_timeout(300)
        self._next()

    # ---- Step 2 «ТМЦ» ---------------------------------------------------------------------------
    def _cell_select(self, grid, idx: int, value: str = None):
        """Grid-row smt-data-select (nth idx) ni value bo'yicha (yoki birinchi) tanlaydi."""
        sel = grid.locator("smt-data-select").nth(idx)
        sel.scroll_into_view_if_needed()
        sel.click()
        self.page.wait_for_timeout(900)
        ov = self.page.locator(".cdk-overlay-container")
        if value:
            self.b.filter_dropdown(sel, value)
        (ov.get_by_text(value, exact=False).first if value
         else ov.locator("li[data-option-index], ul li, li").first).click()
        self.page.wait_for_timeout(900)
        self.b._close_overlay()

    def step2_select_request(self, zr: str, supplier: str):
        """«Поиск запроса на закупку» → ZR tanlash; qatorda Поставщик + Договор. → Далее."""
        sb = self.page.get_by_placeholder("Поиск запроса на закупку").first
        sb.click(); sb.fill(zr)
        self.page.wait_for_timeout(2_000)
        self.page.locator(".cdk-overlay-pane").get_by_text(zr, exact=False).first.click()
        self.page.wait_for_timeout(2_500)
        # zapros grid'ga tushgani: Дата запроса to'ldi
        expect(self.b.control("Дата запроса").locator("input").first).not_to_have_value("")
        grid = self.page.locator("smt-data-table").first
        self._cell_select(grid, 1, supplier)   # Поставщик
        self._cell_select(grid, 2, None)       # Договор = birinchi variant
        self._next()

    # ---- Step 3 «Поставщик» (narx) --------------------------------------------------------------
    def step3_price(self, price: int, qty: int) -> str:
        """Цена kiritadi (Кол-во'dan keyingi input), ИТОГО avto-hisobini qaytaradi. → Далее."""
        grid = self.page.locator("smt-data-table").first
        texts = grid.locator("input[type=text]:not([placeholder='Тип цены'])")
        # Кол-во = value == qty; Цена = keyingi input
        n = texts.count()
        price_inp = None
        for i in range(n):
            v = (texts.nth(i).input_value() or "").strip()
            if v == str(qty):
                price_inp = texts.nth(i + 1)
                break
        assert price_inp is not None, "Кол-во input topilmadi (Цena pozitsiyasi aniqlanmadi)"
        price_inp.click()
        price_inp.press("ControlOrMeta+A"); price_inp.press("Backspace")
        price_inp.fill(str(price))
        price_inp.press("Tab")
        self.page.wait_for_timeout(1_000)
        # ИТОГО qiymati (grid row oxirgi hujayra yoki umumiy)
        itogo = ""
        try:
            cell = grid.get_by_text(re.compile(r"[\d\s ]{5,}")).last
            itogo = re.sub(r"\D", "", cell.inner_text() or "")
        except Exception:
            pass
        self._next()
        return itogo

    # ---- Step 4 «Завершение» --------------------------------------------------------------------
    def step4_finish(self, number: str, status: str = "Принято"):
        """Номер заказа, Статус; «Завершить»/«Сохранить»."""
        try:
            self.b.input(label="Номер заказа", value=number)
        except Exception:
            print("  [order] «Номер заказа» topilmadi/o'zgarmas")
        # Статус (ixtiyoriy — default bo'lishi mumkin)
        try:
            self.b.select(label="Статус", option=status, exact=False, timeout=6_000)
        except Exception:
            print(f"  [order] «Статус»={status} tanlanmadi (default qoldi)")
            self.b._close_overlay()
        # yakuniy tugma
        for name in ["Завершить", "Сохранить", "Далее"]:
            btn = self.page.get_by_role("button", name=name, exact=False)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                break
        self.page.wait_for_timeout(1_500)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(2_500)

    def set_status_accepted(self, number: str):
        """Wizard buyurtmani «Новый» holatida saqlaydi — ro'yxatда «Статус» → «Принято» ga o'tkazamiz
        (Закупка FAQAT Принято buyurtmadan yaratiladi). TC-08 request status-transition kabi."""
        self.open_list()
        self.b.search_list(number)
        self.page.wait_for_timeout(1_500)
        novy = self.page.locator("smt-data-table").get_by_text("Новый", exact=False)
        if novy.count() == 0:
            return  # allaqachon Принято/boshqa holat
        novy.first.click()
        self.page.wait_for_timeout(800)
        self.b.click_button("Статус", exact=False)
        self.page.wait_for_timeout(800)
        self.page.locator(".cdk-overlay-pane, [role=menu]").get_by_text("Принято", exact=True).first.click()
        self.page.wait_for_timeout(800)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(1_500)

    # ---- tekshirish -----------------------------------------------------------------------------
    def expect_in_list(self, supplier: str, total: int):
        self.open_list()
        self.b.search_list(supplier)
        self.page.wait_for_timeout(1_500)
        expect(self.page.locator("smt-data-table").get_by_text(supplier, exact=False).first).to_be_visible(timeout=10_000)
