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
import time

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
    def _close_overlay(self):
        """Ochiq cdk dropdown overlay'ni yopadi. a2 multi-select Escape bilan yopilmaydi —
        neytral joyga (forma sarlavha qatori) bosish ishonchli yopadi."""
        pane = self.page.locator(".cdk-overlay-pane")
        try:
            if pane.count() == 0:
                return
            # Escape + Tab (xavfsiz: navigatsiya yo'q). a2 multi-select ba'zan faqat Tab bilan yopiladi.
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(150)
            for _ in range(3):
                if not pane.first.is_visible():
                    break
                self.page.keyboard.press("Tab")
                self.page.wait_for_timeout(200)
        except Exception:
            pass

    # a2 smt-data-select variantlari <ul><li data-option-index> ichida; ustun sarlavhalari
    # («Название»/«Код») alohida <div>/<span> — shuning uchun generic `span` KIRMAYDI, aks holda
    # `.first` sarlavhani bosib qoladi (grid-dropdown: qa xyu/Банк/Группа va h.k.).
    _OPTION = "[role=option], .cdk-overlay-pane li[data-option-index], .cdk-overlay-pane ul li, .cdk-overlay-pane li"

    def _open_select(self, label: str):
        """Dropdown trigger'ni ochadi: oldingi overlay'ni tozalab, trigger'ni ko'rinishga keltirib bosadi."""
        self._close_overlay()
        trigger = self.control(label).locator("smt-select-trigger, smt-data-select, input").first
        trigger.scroll_into_view_if_needed()
        trigger.click()

    def filter_dropdown(self, field: Locator, text: str, wait_ms: int = 1_300):
        """Ochiq dropdown ro'yxatini qidiruv bilan toraytiradi.
        a2'da qidiruv input'i overlay'da emas, maydonning o'zida; faqat overlay'ni tekshirsak
        qidiruv jim o'tib ketadi va variant to'la ro'yxatdan (10 tadan sahifalangan) izlanadi."""
        box = field.locator("input").first
        if box.count() == 0:
            box = self.page.locator(".cdk-overlay-pane").last.locator("input").first
        if box.count() > 0 and box.is_editable():
            box.fill(text)
            self.page.wait_for_timeout(wait_ms)

    def _settle_options(self, timeout_ms: int = 5_000):
        """Ochiq ro'yxat o'zgarishdan to'xtaguncha kutadi: keyingi sahifa kelib qator qayta chizilayotgan
        paytdagi bosish xatosiz o'tadi-yu, tanlovni yozmaydi."""
        items = self.page.locator(".cdk-overlay-pane li")
        last, stable = None, 0
        deadline = time.monotonic() + timeout_ms / 1000
        while stable < 3 and time.monotonic() < deadline:
            cur = items.evaluate_all("els => els.map(e => e.textContent).join('|')")
            stable = stable + 1 if cur == last else 0
            last = cur
            self.page.wait_for_timeout(150)

    def click_option(self, option: Locator):
        """Dropdown variantini xavfsiz bosadi: ro'yxat tingach aylantiradi, yana tingach bosadi."""
        self._settle_options()
        option.scroll_into_view_if_needed()
        self._settle_options()
        option.click()

    def expect_selected(self, field: Locator, text: str | None = None, timeout: int = 10_000):
        """Tanlov formaga haqiqatan yozilganini tasdiqlaydi. Input qiymati yetarli emas: tanlanmagan
        qidiruv matni ham unda qoladi. Multi-select'da smt-tag, oddiy select'da tozalash («x») ikonkasi chiqadi."""
        if field.locator("smt-multi-data-select").count() > 0:
            tag = field.locator("smt-tag")
            expect((tag.filter(has_text=text) if text else tag).first).to_be_visible(timeout=timeout)
            return
        expect(field.locator('svg-icon[aria-label="x-01-icon"], svg-icon[class*="x-01"]').first
               ).to_be_visible(timeout=timeout)
        if text:
            # Tanlangan matn ba'zi maydonda input'da, ba'zisida (masalan «Статус») alohida elementda turadi.
            wanted = text.casefold()
            shown = ""
            inputs = field.locator("input")
            deadline = time.monotonic() + timeout / 1000
            while time.monotonic() < deadline:
                value = inputs.first.input_value() if inputs.count() > 0 else ""
                shown = f"{value} {field.inner_text()}"
                if wanted in shown.casefold():
                    return
                self.page.wait_for_timeout(200)
            raise AssertionError(f"Tanlovda «{text}» ko'rinmadi, maydonda: {shown!r}")

    def select(self, label: str, option: str, *, search: str | None = None, exact: bool = True, timeout: int = 30_000):
        """smt-data-select dropdown'dan variant tanlaydi (trigger → qidiruv → variant → tekshiruv).
        Qidiruv doim ishlaydi: yangi yozuv to'la ro'yxatda pastda yoki keyingi sahifada bo'lishi mumkin."""
        self._open_select(label)
        field = self.control(label)
        self.filter_dropdown(field, search or option)
        # variant FAQAT ko'rinadigan dropdown'dan (.cdk-overlay-pane) — container'da trigger qiymati
        # yoki boshqa pane'lar ham bo'lishi mumkin, .first ko'rinmas elementga tushib qoladi.
        option_el = self.page.locator(".cdk-overlay-pane").get_by_text(option, exact=exact).first
        expect(option_el).to_be_visible(timeout=timeout)
        self.click_option(option_el)
        self.expect_selected(field, option)
        self._close_overlay()

    def select_change(self, label: str, option: str, *, search: str | None = None,
                      exact: bool = True, timeout: int = 30_000):
        """To'la smt-data-select'ni (default qiymatli) o'zgartiradi: avval «×» bilan tozalab, keyin tanlaydi.
        To'la select trigger'i oddiy klik bilan OCHILMAYDI — avval tozalash kerak. «×» ba'zan dropdown'ni
        o'zi ochadi, shuning uchun ochilishini inline boshqaramiz."""
        ctrl = self.control(label)
        if (ctrl.locator("input").first.input_value() or "").strip():
            clr = ctrl.locator("svg-icon[class*=x], [aria-label*=clear], [aria-label*=close]")
            try:
                clr.last.click(timeout=3_000)
                self.page.wait_for_timeout(500)
            except Exception:
                pass
        if self.page.locator(".cdk-overlay-pane").count() == 0:
            ctrl.locator("smt-data-select, input").first.click()
            self.page.wait_for_timeout(600)
        overlay = self.page.locator(".cdk-overlay-container")
        self.filter_dropdown(ctrl, search or option)
        opt = overlay.get_by_text(option, exact=exact).first
        expect(opt).to_be_visible(timeout=timeout)
        self.click_option(opt)
        self.expect_selected(ctrl, option)
        self._close_overlay()

    def multiselect(self, label: str, *options: str, exact: bool = True, timeout: int = 30_000):
        """smt-multi-data-select: bir yoki bir nechta variant tanlaydi, oxirida yopadi."""
        self._open_select(label)
        pane = self.page.locator(".cdk-overlay-pane")   # faqat ko'rinadigan dropdown
        field = self.control(label)
        for opt in options:
            self.filter_dropdown(field, opt)
            el = pane.get_by_text(opt, exact=exact).first
            expect(el).to_be_visible(timeout=timeout)
            self.click_option(el)
            self.expect_selected(field, opt)
        self._close_overlay()

    def multiselect_first(self, label: str, *, timeout: int = 30_000):
        """smt-multi-data-select: BIRINCHI variantni tanlaydi (matn noma'lum)."""
        self._open_select(label)
        opt = self.page.locator(".cdk-overlay-container").locator(self._OPTION).first
        expect(opt).to_be_visible(timeout=timeout)
        self.click_option(opt)
        self.expect_selected(self.control(label))
        self._close_overlay()

    def chip(self, text: str, *, exact: bool = True):
        """Belgilanadigan chip/checkbox'ni matn bo'yicha bosadi (masalan «Типы ТМЦ» → «Товар»).
        Clickable element — matnli span'ning `cursor-pointer` o'rovchi div'i."""
        self._close_overlay()
        span = self.page.locator("main").get_by_text(text, exact=exact).first
        wrapper = span.locator("xpath=ancestor::div[contains(@class,'cursor-pointer')][1]")
        (wrapper.first if wrapper.count() > 0 else span).click()

    def expect_field_locked(self, label: str):
        """Label'li maydon nofaol ekanini tekshiradi (a2'da ko'pincha readonly, ba'zan disabled)."""
        expect(self.control(label).locator("input").first).not_to_be_editable()

    def select_first(self, label: str, *, timeout: int = 30_000):
        """smt-data-select dropdown'dan BIRINCHI variantni tanlaydi (matn noma'lum bo'lganda)."""
        self._open_select(label)
        opt = self.page.locator(".cdk-overlay-container").locator(self._OPTION).first
        expect(opt).to_be_visible(timeout=timeout)
        self.click_option(opt)
        self.expect_selected(self.control(label))
        self._close_overlay()

    def tree_select(self, label: str, option: str, *, exact: bool = True, timeout: int = 30_000):
        """smt-tree-select (masalan «Регион»): trigger'ni ochib overlay'dan variantni tanlaydi.
        DIQQAT: variant matni tizimdagi yozuvga mos bo'lsin (masalan «Toshkent» LOTIN, «Тошкент» EMAS)."""
        self._close_overlay()
        self.control(label).locator("smt-tree-select").first.click()
        opt = self.page.locator(".cdk-overlay-pane").get_by_text(option, exact=exact).first
        expect(opt).to_be_visible(timeout=timeout)
        self.click_option(opt)
        self.page.wait_for_timeout(300)
        self._close_overlay()

    def checkbox(self, text: str, checked: bool = True, *, exact: bool = True):
        """a2 smt-checkbox (`<label smt-checkbox>` + yashirin input + `span[aria-checked]`) ni
        istalgan holatga keltiradi. Clickable = yonidagi matn (`<p>`); holat `aria-labelledby`
        orqali bog'langan span'dan o'qiladi. Allaqachon kerakli holatda bo'lsa — bosmaydi."""
        txt = self.page.get_by_text(text, exact=exact).first
        txt.wait_for(state="visible", timeout=10_000)
        state = self.page.evaluate(
            """(t) => {
                const lab=[...document.querySelectorAll('p,span,label')].find(
                    e => e.children.length===0 && (e.innerText||'').trim()===t);
                if(!lab) return null;
                let box = lab.id ? document.querySelector(`[aria-labelledby="${lab.id}"]`) : null;
                if(!box){ const r=lab.closest('div'); box = r ? r.parentElement.querySelector('[aria-checked]') : null; }
                return box ? box.getAttribute('aria-checked') : null;
            }""", text)
        if (state == "true") != checked:
            txt.click()
            self.page.wait_for_timeout(300)

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

    def switch_state(self, label: str) -> bool:
        """smt-switch holati (True=yoqilgan). `<div role=switch aria-checked>` dan o'qiladi."""
        return self.control(label).locator("[role=switch]").first.get_attribute("aria-checked") == "true"

    def switch_set(self, label: str, on: bool = True):
        """smt-switch'ni istalgan holatga keltiradi (allaqachon shunday bo'lsa bosmaydi)."""
        if self.switch_state(label) != on:
            self.control(label).locator("smt-switch").first.click()
            self.page.wait_for_timeout(300)

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
