"""
Поступление ТМЦ на склад (goods receipt) — a2 3-qadamli WIZARD page object (TC-E2E-11).
Ro'yxat: /a2/anor/mkw/input/input_list («Создать»); create: input+add.

Jonli tasdiqlangan (mohir@xan, 2026-11-03):
  Step1 «Основное»: Номер (input), Дата* (default), Склад* (data-select — DEFAULT «WH-Yashnobod»
    bilan to'la, × bilan tozalab QA-E2E Sklad tanlanadi), Валюта для учета остатков* (default
    «Доллар США» → «Узбекский сум»). Switch «Внести дополнительные расходы». → «Далее».
  Step2 «Закупки»: «Поиск закупки» (placeholder search) — YOZIB qidirish FILTRLAMAYDI; to'liq ro'yxatdan
    invoice/supplier matnli variantni tanlanadi → grid'ga ТМЦ qatori (Кол-во input placeholder «100 / 100»
    = max). Кол-во = 100. → «Далее».
  Step3 «Завершение»: Статус (default «Новое») → «Завершено» → «Завершить» → «Да».
  Natija: Остатки ТМЦ (QA-E2E Sklad) da QA-E2E-TMS = 100.
"""
import datetime

from playwright.sync_api import expect

from utils.base_page import BasePage


class InputPage:
    LIST_PATH = "/a2/anor/mkw/input/input_list"

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    def open_list(self):
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.page.wait_for_timeout(800)

    def open_create(self):
        self.page.get_by_role("button", name="Создать", exact=True).first.click()
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

    # ---- Step 1 ---------------------------------------------------------------------------------
    def step1_main(self, number: str, warehouse: str):
        try:
            self.b.input(label="Номер", value=number)
        except Exception:
            print("  [поступление] «Номер» o'zgarmas")
        # To'liq nom bilan qidiramiz: umumiy prefiks ro'yxatni toraytirmaydi, pastdagi variant esa
        # aylantirib bosilganda tanlanmay qoladi (maydonda yozilgan matn qolib ketadi).
        self.b.select_change("Склад", warehouse, search=warehouse, exact=False)
        self.page.wait_for_timeout(500)
        self.b.select_change("Валюта для учета остатков", "Узбекский сум", exact=False)
        self.page.wait_for_timeout(500)
        self._next()

    # ---- Step 2 ---------------------------------------------------------------------------------
    def step2_from_purchase(self, invoice: str, qty: int):
        """«Поиск закупки» ro'yxatidan invoice matnli zakupkani tanlab, Кол-во = qty. → Далее."""
        sb = self.page.get_by_placeholder("Поиск закупки").first
        sb.click()
        self.page.wait_for_timeout(2_000)  # yozmaymiz — qidiruv filtrlamaydi
        self.b.click_option(self.page.locator(".cdk-overlay-pane").get_by_text(invoice, exact=False).first)
        self.page.wait_for_timeout(3_000)
        # Кол-во = grid birinchi text input (placeholder «100 / 100» = max)
        qinp = self.page.locator("smt-data-table input[type=text]").first
        qinp.click()
        qinp.press("ControlOrMeta+A"); qinp.press("Backspace")
        qinp.fill(str(qty))
        qinp.press("Tab")
        self.page.wait_for_timeout(800)
        self._next()

    # ---- Step 3 ---------------------------------------------------------------------------------
    def step3_finish(self, status: str = "Завершено"):
        try:
            cur = self.b.control("Статус").locator("input").first.input_value()
            if status.lower() not in (cur or "").lower():
                self.b.select(label="Статус", option=status, exact=False, timeout=6_000)
        except Exception:
            print(f"  [поступление] Статус={status} (default qoldi)")
            self.b._close_overlay()
        for name in ["Завершить", "Провести", "Сохранить"]:
            btn = self.page.get_by_role("button", name=name, exact=False)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                break
        self.page.wait_for_timeout(800)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(2_500)

    def set_status_completed(self, number: str):
        """Wizard поступлениени «Новое» holatida saqlaydi — ro'yxatда «Статус» → «Завершено» (qoldiq posted).
        (TC-09 buyurtma status-transition kabi.)"""
        self.open_list()
        self.b.search_list(number)
        self.page.wait_for_timeout(1_500)
        novoe = self.page.locator("smt-data-table").get_by_text("Новое", exact=False)
        if novoe.count() == 0:
            return  # allaqachon Завершено
        # grid status katakchasi «Новое» = dropdown trigger → menyu (Черновик/Принято/Завершено menuitem)
        novoe.first.click()
        self.page.wait_for_timeout(1_000)
        item = self.page.get_by_role("menuitem", name="Завершено", exact=False)
        if item.count() == 0:
            item = self.page.locator(".cdk-overlay-container").get_by_text("Завершено", exact=False)
        item.first.click()
        self.page.wait_for_timeout(800)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(1_500)

    # ---- tekshirish -----------------------------------------------------------------------------
    def expect_in_list(self, number: str, status: str = "Завершено"):
        self.open_list()
        self.b.search_list(number)
        self.page.wait_for_timeout(1_500)
        table = self.page.locator("smt-data-table")
        expect(table.get_by_text(number, exact=False).first).to_be_visible(timeout=10_000)
        expect(table.get_by_text(status, exact=False).first).to_be_visible(timeout=10_000)
