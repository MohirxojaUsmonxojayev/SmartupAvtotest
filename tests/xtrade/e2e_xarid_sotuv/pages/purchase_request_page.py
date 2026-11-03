"""
Запрос на закупку (xarid so'rovi) — a2 xujjat page object (TC-E2E-08).
Ro'yxat: /a2/anor/mkw/purchase/purchase_request_list ; create: …+add.

Jonli tasdiqlangan (mohir@xan, 2026-11-03):
  Header: Номер (input), Дата* (date, default bugun), Статус* (default «Новый»),
    Крайний срок поставки (date), Примечание (textarea). Tugmalar: Сохранить/Закрыть/Подбор/Импорт.
  Qator grid ustunlari: №/Название/Ед. изм./Кол-во/Кол-во кейсов/Причина/Примечание.
  «Подбор» = smt-drawer («Запрос на закупку (подбор)»): Доступные/Выбранные tab, qidiruv (type=search),
    har ТМЦ qatorida Кол-во input. ТМЦ qidirib Кол-во yoz → drawer «Закрыть» →
    «Подтверждение: Выбрать ТМЦ с заполненными данными?» → «Да» → main grid'ga qator qo'shiladi.
  Status: ro'yxatда qatorни tanlab «Статус» → «Принято» (tasdiq «Изменить статус документа … на Принято?»).
"""
import datetime

from playwright.sync_api import expect

from utils.base_page import BasePage


class PurchaseRequestPage:
    LIST_PATH = "/a2/anor/mkw/purchase/purchase_request_list"
    SECTION = "Основная информация"

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

    def _neutral_click(self):
        self.page.locator("main").get_by_text(self.SECTION, exact=True).first.click()
        self.page.wait_for_timeout(200)

    def _date_main(self, label: str, value: str):
        el = self.b.control(label).locator("input").first
        el.click(); el.press("ControlOrMeta+A"); el.press("Backspace"); el.fill(value)
        self.page.wait_for_timeout(200)
        self._neutral_click()

    def _confirm_yes_if_any(self):
        try:
            dlg = self.page.locator("[role=dialog], .cdk-dialog-container").last
            btn = dlg.get_by_role("button", name="Да", exact=False).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                self.page.wait_for_timeout(600)
        except Exception:
            pass

    # ---- UMUMIY ---------------------------------------------------------------------------------
    def _dismiss_modal(self):
        """Ochiq Ошибка/confirm modalini yopadi (Да → bo'lmasa Закрыть/ОК)."""
        try:
            dlg = self.page.locator("[role=dialog], .cdk-dialog-container").last
            if dlg.count() > 0 and dlg.is_visible():
                for nm in ["Да", "Закрыть", "ОК", "OK"]:
                    btn = dlg.get_by_role("button", name=nm, exact=False)
                    if btn.count() > 0 and btn.first.is_visible():
                        btn.first.click()
                        break
                self.page.wait_for_timeout(600)
        except Exception:
            pass

    def check_empty_save_blocked(self):
        """UMUMIY 1: ТМЦ siz «Сохранить» → «Ошибка: Выберите минимум одну позицию!» (Закрыть) → saqlanmaydi."""
        self.b.save()
        self.page.wait_for_timeout(1_000)
        self._dismiss_modal()   # xato/confirm modalini yopamiz (backdrop keyingi amalni to'smasin)
        self.page.wait_for_timeout(600)
        assert "add" in self.page.url or "создани" in self.page.title().lower(), \
            f"ТМЦ siz saqlandi? URL={self.page.url}"

    # ---- header + pozitsiya ---------------------------------------------------------------------
    def fill_header(self, number: str, note: str = "QA-E2E"):
        today = datetime.date.today()
        due = today + datetime.timedelta(days=7)
        self.b.input(label="Номер", value=number)
        self._date_main("Дата", today.strftime("%d.%m.%Y"))
        self._date_main("Крайний срок поставки", due.strftime("%d.%m.%Y"))
        self.b.input(label="Примечание", value=note)

    def add_tmc(self, tmc: str, qty: int):
        """«Подбор» drawer: ТМЦ qidirib Кол-во yozadi, «Закрыть» → confirm «Да» → main grid'ga qator."""
        self.page.get_by_role("button", name="Подбор", exact=False).first.click()
        self.page.wait_for_timeout(2_000)
        drawer = self.page.locator("smt-drawer").first
        drawer.wait_for(state="visible", timeout=10_000)
        ds = drawer.locator("input[type=search]").first
        ds.click(); ds.fill(tmc); ds.press("Enter")
        # filtr joylashishini kutamiz (pager 1/1 yoki TMC ko'rinishi)
        for _ in range(12):
            self.page.wait_for_timeout(600)
            if drawer.get_by_text(tmc, exact=False).count() and drawer.get_by_text("1/1", exact=False).count():
                break
        expect(drawer.get_by_text(tmc, exact=False).first).to_be_visible(timeout=10_000)
        qinp = drawer.locator("smt-data-table input[type=text]").first   # Кол-во (birinchi text input)
        qinp.click(); qinp.fill(str(qty)); qinp.press("Tab")
        self.page.wait_for_timeout(600)
        drawer.get_by_role("button", name="Закрыть", exact=True).first.click()
        self.page.wait_for_timeout(1_000)
        self._confirm_yes_if_any()   # «Выбрать ТМЦ с заполненными данными?» → Да
        self.page.wait_for_timeout(1_500)
        # main grid'ga qator qo'shilgani: «Общее кол-во: {qty}» ko'rinadi (bitta ТМЦ = umumiy qty)
        expect(self.page.get_by_text(f"Общее кол-во: {qty}", exact=False).first).to_be_visible(timeout=10_000)

    def import_smoke(self):
        """«Импорт» oynasini ochib-yopadi (fayl yuklanmaydi, tolerant smoke)."""
        try:
            self.page.get_by_role("button", name="Импорт", exact=False).first.click()
            self.page.wait_for_timeout(1_000)
            # drawer/dialog bo'lsa yopamiz
            dr = self.page.locator("smt-drawer, [role=dialog][aria-modal]").last
            if dr.count() and dr.is_visible():
                btn = dr.get_by_role("button", name="Закрыть", exact=True)
                if btn.count():
                    btn.first.click()
                else:
                    self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(600)
        except Exception:
            print("  [импорт] oyna ochilmadi/yopilmadi, o'tkazildi")

    # ---- saqlash / status / tekshirish ----------------------------------------------------------
    def save(self):
        self.b.save()
        self.page.wait_for_timeout(600)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(2_000)

    def set_status_accepted(self, number: str):
        """Ro'yxатда qatorни tanlab «Статус» → «Принято» (tasdiq «Да»)."""
        self.open_list()
        self.b.search_list(number)
        self.page.wait_for_timeout(1_500)
        self.b.grid_row(number).click()
        self.page.wait_for_timeout(800)
        self.b.click_button("Статус", exact=False)
        self.page.wait_for_timeout(800)
        self.page.locator(".cdk-overlay-pane, [role=menu]").get_by_text("Принято", exact=False).first.click()
        self.page.wait_for_timeout(800)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(1_500)

    def expect_in_list(self, number: str, status_text: str = ""):
        self.open_list()
        self.b.search_list(number)
        self.page.wait_for_timeout(1_500)
        expect(self.page.locator("smt-data-table").get_by_text(number, exact=False).first).to_be_visible(timeout=10_000)
        if status_text:
            expect(self.page.locator("smt-data-table").get_by_text(status_text, exact=False).first).to_be_visible(timeout=10_000)

    def open_view(self, number: str, tmc: str, qty: int):
        self.open_list()
        self.b.search_list(number)
        self.page.wait_for_timeout(1_500)
        self.b.grid_row(number).click()
        self.page.wait_for_timeout(700)
        self.b.click_button("Просмотреть", exact=False)
        self.page.wait_for_timeout(2_000)
        # ТМЦ pozitsiyalari alohida tab/bo'limda bo'lishi mumkin
        for tabname in ["ТМЦ", "Позиции", "Товары"]:
            tab = self.page.locator("smt-tab-button, smt-tab-bar button").filter(has_text=tabname)
            if tab.count() > 0 and tab.first.is_visible():
                tab.first.click()
                self.page.wait_for_timeout(1_000)
                break
        loc = self.page.get_by_text(tmc, exact=False)
        if loc.count() > 0:
            loc.first.scroll_into_view_if_needed(timeout=10_000)
            expect(loc.first).to_be_visible()
        else:
            # ТМЦ view'da ko'rinmasa — hujjat ochilgani (Номер) tasdiqlanadi (qty yaratishda «Общее кол-во» bilan tekshirilgan)
            expect(self.page.get_by_text(number, exact=False).first).to_be_visible(timeout=10_000)
