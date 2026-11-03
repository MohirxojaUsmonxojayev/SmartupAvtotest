"""
Закупка (xarid, zakazdan) — a2 3-qadamli WIZARD page object (TC-E2E-10).
Ro'yxat: /a2/anor/mkw/purchase/purchase_list (create tugma «Создать закуп…»); create: purchase+add.

Jonli tasdiqlangan (mohir@xan, 2026-11-03):
  Step1: Дата закупки* (default), Дата поступления на склад, «Заказ на закупку» (smt-data-select —
    ПРИНЯТО buyurtmani QA-E2E-ZZ-<d> raqami bo'yicha qidirib tanlash → Поставщик/Валюта/ТМЦ/Шаблон
    auto-to'ladi), Шаблон операции* (auto/first), Договор/Тип оплаты/Проект, Валюта* (default),
    Номер счет-фактуры (input), Дата счет-фактуры (date). Switch: «С поступлением на склад» /
    «Внести дополнительные расходы» (o'chiq qoldiriladi — поступление alohida TC-11). → «Далее».
  Step2: ТМЦ grid (zakazdan to'la, faqat o'qish) — Сумма/ИТОГО = Кол-во×Цена = 1 000 000. → «Далее».
  Step3: Статус* (default «Завершено»), Поставщик/Договор/ИТОГО/Примечание. Tugmalar «Провести»/«Сохранить».
    «Провести» → Завершено + ta'minotchi qarzi +1 000 000.
"""
import datetime

from playwright.sync_api import expect

from utils.base_page import BasePage


class PurchasePage:
    LIST_PATH = "/a2/anor/mkw/purchase/purchase_list"
    SECTION = "Основная информация"

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    # ---- navigatsiya ----------------------------------------------------------------------------
    def open_list(self):
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.page.get_by_role("button", name="Создать закуп", exact=False).first.wait_for(state="visible", timeout=30_000)
        self.page.wait_for_timeout(800)

    def open_create(self):
        self.page.get_by_role("button", name="Создать закуп", exact=False).first.click()
        self.b.expect_form_open("создани")
        self.page.wait_for_timeout(2_000)

    def _next(self):
        self.page.get_by_role("button", name="Далее", exact=False).first.click()
        self.page.wait_for_timeout(2_800)

    def _confirm_yes_if_any(self):
        try:
            dlg = self.page.locator("[role=dialog], .cdk-dialog-container").last
            btn = dlg.get_by_role("button", name="Да", exact=False).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                self.page.wait_for_timeout(600)
        except Exception:
            pass

    def _date_main(self, label: str, value: str):
        el = self.b.control(label).locator("input").first
        el.click(); el.press("ControlOrMeta+A"); el.press("Backspace"); el.fill(value)
        self.page.wait_for_timeout(200)
        self.page.locator("main").get_by_text("Дата закупки", exact=False).first.click()  # kalendar yopish
        self.page.wait_for_timeout(200)

    # ---- Step 1 ---------------------------------------------------------------------------------
    def step1_from_order(self, order_number: str, invoice_no: str):
        """«Заказ на закупку» = order_number (ПРИНЯТО) tanlaydi; Шаблон/Номер СФ/Дата СФ to'ldiradi. → Далее."""
        self.b.select(label="Заказ на закупку", option=order_number, search=order_number, exact=False, timeout=15_000)
        self.page.wait_for_timeout(2_500)
        if not self.b.control("Шаблон операции").locator("input").first.input_value().strip():
            self.b.select_first("Шаблон операции")
            self.page.wait_for_timeout(400)
        try:
            self.b.input(label="Номер счет-фактуры", value=invoice_no)
        except Exception:
            print("  [закупка] «Номер счет-фактуры» topilmadi")
        self._date_main("Дата счет-фактуры", datetime.date.today().strftime("%d.%m.%Y"))
        self._next()

    # ---- Step 2 (Сумма) -------------------------------------------------------------------------
    def step2_expect_sum(self, total: int):
        """ТМЦ grid'ida ИТОГО/Сумма = total ekanini tasdiqlaydi. → Далее."""
        formatted = f"{total:,}".replace(",", " ")   # 1000000 -> «1 000 000»
        expect(self.page.get_by_text(formatted, exact=False).first).to_be_visible(timeout=10_000)
        self._next()

    # ---- Step 3 (Статус/Провести) ---------------------------------------------------------------
    def step3_finish(self, status: str = "Завершено"):
        """Статус = Завершено (default) → «Провести» (yoki «Сохранить»+«Провести»)."""
        try:
            cur = self.b.control("Статус").locator("input").first.input_value()
            if status.lower() not in (cur or "").lower():
                self.b.select(label="Статус", option=status, exact=False, timeout=6_000)
        except Exception:
            print(f"  [закупка] Статус={status} (default qoldi)")
            self.b._close_overlay()
        # «Провести» — yakunlaydi (Завершено + qarz)
        provesti = self.page.get_by_role("button", name="Провести", exact=False)
        if provesti.count() > 0 and provesti.first.is_visible():
            provesti.first.click()
        else:
            self.page.get_by_role("button", name="Сохранить", exact=False).first.click()
        self.page.wait_for_timeout(800)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(2_500)

    # ---- tekshirish -----------------------------------------------------------------------------
    def expect_in_list(self, supplier: str, total: int, status: str = "Завершено"):
        self.open_list()
        self.b.search_list(supplier)
        self.page.wait_for_timeout(1_500)
        table = self.page.locator("smt-data-table")
        expect(table.get_by_text(supplier, exact=False).first).to_be_visible(timeout=10_000)
        formatted = f"{total:,}".replace(",", " ")
        expect(table.get_by_text(formatted, exact=False).first).to_be_visible(timeout=10_000)
        expect(table.get_by_text(status, exact=False).first).to_be_visible(timeout=10_000)
