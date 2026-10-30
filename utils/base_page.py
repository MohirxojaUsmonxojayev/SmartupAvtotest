"""
Smartup YANGI /a2 UI uchun forma helperlari (jonli xtrade'da o'rganib yozilgan, 2026-10-30).

a2 forma strukturasi:
    <smt-control>
        <label>Фамилия</label>
        <smt-input><input></smt-input>   # yoki smt-data-select / smt-date-picker / smt-switch / smt-tree-select
    </smt-control>

Ishlatish:
    from utils.base_page import BasePage
    base = BasePage(page)
    base.input(label="Код", value="A123")
    base.select(label="Юридическое лицо", option="NovaTrade")
    base.save()

Komponentlar: smt-input (text), smt-data-select (dropdown), smt-date-picker (sana),
smt-switch (toggle), smt-tree-select (daraxt), smt-data-table (grid), smt-tab-button (tab).
Sahifa ochilgani signali: document.title "Smartup Online" (shell) dan forma nomiga aylanadi.

Eslatma: murakkab holatlar (tree-select, switch holati, confirm dialog) test yozishda
jonli tasdiqlanadi — pastdagi izohlarга qarang.
"""
import re

from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ==================================================================================================================
    # Navigatsiya / sahifa holati
    # ==================================================================================================================
    def open_form(self, url: str) -> None:
        """a2 formani to'liq URL bilan ochadi va yuklanishini kutadi."""
        self.page.goto(url, wait_until="commit", timeout=60_000)
        self.expect_form_open()

    def expect_form_open(self, title: str | None = None, timeout: int = 60_000) -> None:
        """Forma ochilganini tekshiradi — title 'Smartup Online' (shell) dan forma nomiga aylanadi."""
        expect(self.page).not_to_have_title("Smartup Online", timeout=timeout)
        if title:
            expect(self.page).to_have_title(re.compile(re.escape(title)), timeout=timeout)

    # ==================================================================================================================
    # Maydonni label orqali topish
    # ==================================================================================================================
    def _label_re(self, label: str):
        # " Фамилия ", "Имя *", "Код" — oldi/keyin probel va majburiy '*' hisobga olinadi
        return re.compile(rf"^\s*{re.escape(label)}\s*\*?\s*$", re.IGNORECASE)

    def control(self, label: str) -> Locator:
        """Label matni bo'yicha smt-control konteynerini qaytaradi (ichida input/select/...)."""
        lab = self.page.locator("smt-control label").filter(has_text=self._label_re(label))
        return lab.locator("xpath=ancestor::smt-control[1]").first

    # ==================================================================================================================
    # Text input (smt-input)
    # ==================================================================================================================
    def input(
        self,
        value=None,
        *,
        label: str | None = None,
        placeholder: str | None = None,
        locator=None,
        expect_value=None,
        return_value: bool = False,
        clear: bool = True,
        press_tab: bool = False,
        index: int = 0,
    ):
        """Text input bilan ishlash. Topish (bittasini bering): label / placeholder / locator."""
        if label is not None:
            el = self.control(label).locator("input, textarea").first
        elif placeholder is not None:
            el = self.page.get_by_placeholder(placeholder).nth(index)
        elif locator is not None:
            el = self.page.locator(locator).nth(index) if isinstance(locator, str) else locator
        else:
            raise ValueError("input(): label, placeholder yoki locator dan bittasini bering")

        expect(el).to_be_visible()
        if value is not None:
            el.click()
            if clear:
                el.press("ControlOrMeta+A")
                el.press("Backspace")
            el.fill(str(value))
            if press_tab:
                el.press("Tab")
        if expect_value is not None:
            expect(el).to_have_value(str(expect_value))
        if return_value:
            return el.input_value()
        return el

    # ==================================================================================================================
    # Dropdown (smt-data-select)
    # ==================================================================================================================
    def select(self, label: str, option: str, *, search: str | None = None, exact: bool = True, timeout: int = 30_000):
        """
        smt-data-select dropdown'dan variant tanlaydi: trigger'ni bosadi, (kerak bo'lsa qidiradi),
        cdk overlay'dagi variantni bosadi.
        """
        trigger = self.control(label).locator("smt-select-trigger, smt-data-select").first
        trigger.click()
        overlay = self.page.locator(".cdk-overlay-container")
        if search is not None:
            box = overlay.locator("input").first
            if box.count() > 0:
                box.fill(search)
        option_el = overlay.get_by_text(option, exact=exact).first
        expect(option_el).to_be_visible(timeout=timeout)
        option_el.click()

    def select_first(self, label: str, *, timeout: int = 30_000):
        """smt-data-select dropdown'dan BIRINCHI variantni tanlaydi (matn noma'lum bo'lganda)."""
        self.control(label).locator("smt-select-trigger, smt-data-select").first.click()
        overlay = self.page.locator(".cdk-overlay-container")
        opt = overlay.locator(
            "[role=option], .cdk-overlay-pane li, .cdk-overlay-pane [class*=option], .cdk-overlay-pane span"
        ).first
        expect(opt).to_be_visible(timeout=timeout)
        opt.click()

    # ==================================================================================================================
    # Sana (smt-date-picker)
    # ==================================================================================================================
    def date(self, label: str, value: str):
        """smt-date-picker ichidagi inputga sana (DD.MM.YYYY) yozadi."""
        el = self.control(label).locator("input").first
        expect(el).to_be_visible()
        el.click()
        el.press("ControlOrMeta+A")
        el.press("Backspace")
        el.fill(value)
        el.press("Escape")

    # ==================================================================================================================
    # Switch (smt-switch) — IZOH: holatni o'qish aniq emas, hozircha bosadi (test yozishda tasdiqlang)
    # ==================================================================================================================
    def switch(self, label: str):
        """smt-switch toggle'ini bosadi (holatni o'zgartiradi)."""
        self.control(label).locator("smt-switch").first.click()

    # ==================================================================================================================
    # Tugmalar / saqlash
    # ==================================================================================================================
    def click_button(self, name: str, *, exact: bool = True):
        btn = self.page.get_by_role("button", name=name, exact=exact).first
        expect(btn).to_be_visible()
        btn.click()

    def save(self):
        """"Сохранить" (ba'zan ikonка bilan, shuning uchun exact=False)."""
        self.click_button("Сохранить", exact=False)

    def close(self):
        self.click_button("Закрыть", exact=False)

    # ==================================================================================================================
    # Tab (smt-tab-button) — forma ichidagi bo'limlar
    # ==================================================================================================================
    def open_tab(self, name: str):
        self.page.locator("smt-tab-button, smt-tab-bar button").filter(has_text=name).first.click()

    # ==================================================================================================================
    # List / grid (smt-data-table)
    # ==================================================================================================================
    def search_list(self, text: str):
        """List tepasidagi "Поиск..." maydoniga yozib Enter bosadi."""
        box = self.page.get_by_placeholder("Поиск...").first
        expect(box).to_be_visible()
        box.fill(text)
        box.press("Enter")
        self.page.wait_for_timeout(1_500)

    def grid_row(self, text: str) -> Locator:
        """smt-data-table ichida `text` ni o'z ichiga olgan qatorni (cell) qaytaradi."""
        row = self.page.locator("smt-data-table").get_by_text(text, exact=False).first
        expect(row).to_be_visible()
        return row

    def open_row(self, text: str):
        """`text` bo'yicha qidirib, birinchi qatorni ochadi (double-click — edit/view formasi)."""
        self.search_list(text)
        self.grid_row(text).dblclick()

    # ==================================================================================================================
    # Confirm dialog (cdk) — IZOH: tugma nomi (Да/Сохранить/Удалить) formaga qarab farq qiladi
    # ==================================================================================================================
    def confirm(self, name: str = "Да", *, exact: bool = False):
        """cdk confirm dialog'ida tugmani bosadi. Tugma nomini amal turiga qarab bering."""
        dialog = self.page.locator("[role=dialog], .cdk-dialog-container").last
        btn = dialog.get_by_role("button", name=name, exact=exact).first
        expect(btn).to_be_visible()
        btn.click()
