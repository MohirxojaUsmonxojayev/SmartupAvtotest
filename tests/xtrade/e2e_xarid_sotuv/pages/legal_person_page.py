"""
Юридическое лицо (ta'minotchi) — a2 page object (TC-E2E-03).
Ro'yxat route: /a2/anor/mr/person/legal_person_list ; create: …+add (title «Юридическое лицо (создание)»).
Supplier (poставщик) ro'yxati: /a2/anor/mkw/supplier_list.

Jonli tasdiqlangan struktura (mohir@xan, 2026-11-02):
  Main: Полное название* (input), Код/Штрих-код/Почтовый индекс/Веб-сайт/Альтернативное название/
    Телефон/Телеграм/Email/ИНН/ОКЭД/Рег.код НДС (input), Собственник/Руководитель (data-select),
    Рабочие зоны/Виды деятельности (multi-select), Регион (TREE-select — «Toshkent» LOTIN),
    GPS (readonly — SKIP), Адрес/Ориентир/Почтовый адрес (textarea),
    checkbox «Сохранить в качестве поставщика»/«…клиента».
  8 tab: Характеристики (qa xyu* majburiy data-select + Группа/Категория/Тип/AAA/BBB/CCC),
    Расчетный счет (dialog: Название счета*/МФО/Банк*(select)/Расчетный счет*/Основной/Статус/Валюта*(select)/Примечание),
    Контактные лица (dialog: Ф.И.О.*/Должность(select)/Телефон/Дата рождения(date)/Примечание),
    Файлы (SKIP), Договор (dialog: Название*/Номер*/Дата оформления*(date)/Код/Дата окончания(date)/
    Валюта*(select)/Сумма/Примечание/Основной/Статус), Примечание (textarea),
    Руководящие должности (Директор Имя/Фамилия/Отчество/ИНН + Бухгалтер Имя/Фамилия/Отчество — label'lar takror → nth),
    График доставки (Рабочие дни Пн..Вс tugmalar + Временное окно).
  Har saqlash «Подтверждение — Сохранить? Да/Нет» chiqaradi → «Да».
  МФО 00014 Банк'ni AVTO to'ldirmaydi → Банк* select_first.
"""
import datetime

from playwright.sync_api import expect

from utils.base_page import BasePage


class LegalPersonPage:
    LIST_PATH = "/a2/anor/mr/person/legal_person_list"
    SUPPLIER_LIST = "/a2/anor/mkw/supplier_list"

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    # ---- navigatsiya ----------------------------------------------------------------------------
    def open_list(self):
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.b.expect_form_open("Юридическ")
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)

    def open_create(self):
        self.page.get_by_role("button", name="Создать", exact=True).first.click()
        self.b.expect_form_open("создани")
        self.page.wait_for_timeout(1_500)

    # ---- UMUMIY tekshiruv -----------------------------------------------------------------------
    def check_empty_save_blocked(self):
        """UMUMIY 1: bo'sh forma «Сохранить» → majburiy maydonlar qizil, create formada qoladi."""
        self.b.save()
        self.page.wait_for_timeout(800)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(800)
        assert "add" in self.page.url or "создани" in self.page.title().lower(), \
            f"Bo'sh forma saqlandi? URL={self.page.url}, title={self.page.title()}"

    # ---- main maydonlar -------------------------------------------------------------------------
    def fill_main(self, d: dict):
        self.b.input(label="Полное название", value=d["full_name"])    # *
        self.b.input(label="Альтернативное название", value=d["alt_name"])
        self.b.input(label="Код", value=d["code"])
        self.b.input(label="Штрих-код", value=d["barcode"])
        self.b.input(label="Почтовый индекс", value=d["zip"])
        self.b.input(label="Веб-сайт", value=d["web"])
        self.b.input(label="Телефон", value=d["phone"])
        self.b.input(label="Телеграм", value=d["telegram"])
        self.b.input(label="Email", value=d["email"])
        self.b.input(label="ИНН", value=d["inn"])                      # yonidagi «Поиск» BOSILMAYDI
        self.b.input(label="ОКЭД", value=d["oked"])
        self.b.input(label="Регистрационный код плательщика НДС", value=d["vat"])
        self.b.input(label="Адрес", value=d["address"])
        self.b.input(label="Ориентир", value=d["orientir"])
        self.b.input(label="Почтовый адрес", value=d["post_addr"])
        self.b.select_first("Собственник")
        self.b.select_first("Руководитель")
        self.b.multiselect_first("Рабочие зоны")
        self.b.tree_select("Регион", d["region"])                      # «Toshkent» (lotin)
        # «Виды деятельности» — tizimda qiymat yo'q (spec), o'tkazamiz
        # GPS — mustasno (spec)
        # checkboxlar
        self.b.checkbox("Сохранить в качестве поставщика", True)       # ta'minotchi avto-yaratiladi
        self.b.checkbox("Сохранить в качестве клиента", True)          # bosib ko'rib...
        self.b.checkbox("Сохранить в качестве клиента", False)         # ...qaytaramiz

    def fill_characteristics(self):
        self.b.open_tab("Характеристики")
        self.page.wait_for_timeout(800)
        self.b.select_first("qa xyu")   # * majburiy (grid-dropdown: birinchi <li>)
        for lbl in ["Группа", "Категория", "Тип", "Характеристика AAA",
                    "Характеристика BBB", "Характеристика CCC"]:
            try:
                self.b.select_first(lbl, timeout=4_000)
            except Exception:
                print(f"  [характеристики] '{lbl}' — variant yo'q, o'tkazildi")
                self.b._close_overlay()  # bo'sh dropdown overlay'ini yopamiz (keyingi amalni to'smasin)

    # ---- dialog helperlari ----------------------------------------------------------------------
    def _dlg(self):
        return self.page.locator("[role=dialog][aria-modal]").first

    def _open_tab_create(self, tab: str):
        self.b.open_tab(tab)
        self.page.wait_for_timeout(700)
        self.page.locator("main").get_by_role("button", name="Создать", exact=True).last.click()
        dlg = self._dlg()
        dlg.wait_for(state="visible", timeout=10_000)
        return dlg

    def _d_input(self, dlg, label: str, value: str):
        el = dlg.locator("smt-control").filter(has_text=label).locator("input, textarea").first
        el.scroll_into_view_if_needed()
        el.click()
        el.press("ControlOrMeta+A")
        el.press("Backspace")
        el.fill(str(value))

    def _d_select_first(self, dlg, label: str, *, timeout: int = 15_000):
        self.b._close_overlay()
        dlg.locator("smt-control").filter(has_text=label).locator("smt-data-select, input").first.click()
        opt = self.page.locator(".cdk-overlay-container").locator(self.b._OPTION).first
        expect(opt).to_be_visible(timeout=timeout)
        self.b.click_option(opt)
        self.b._close_overlay()

    def _d_select(self, dlg, label: str, option: str, *, exact: bool = True, timeout: int = 15_000):
        self.b._close_overlay()
        dlg.locator("smt-control").filter(has_text=label).locator("smt-data-select, input").first.click()
        opt = self.page.locator(".cdk-overlay-container").get_by_text(option, exact=exact).first
        expect(opt).to_be_visible(timeout=timeout)
        self.b.click_option(opt)
        self.b._close_overlay()

    def _d_select_if_empty(self, dlg, label: str, option: str, *, exact: bool = False):
        """Dialog select'ni FAQAT bo'sh bo'lsa to'ldiradi (masalan «Валюта» default «Узбекский сум» bo'ladi)."""
        val = dlg.locator("smt-control").filter(has_text=label).locator("input").first.input_value()
        if val.strip():
            return
        self._d_select(dlg, label, option, exact=exact)

    def _d_date(self, dlg, label: str, value: str):
        """smt-date-picker: input'ga sana yozib, kalendar overlay'ni YOPADI.
        DIQQAT: kalendar Escape bilan YOPILMAYDI — dialog sarlavhasiga klik yopadi (jonli, 2026-11-02)."""
        el = dlg.locator("smt-control").filter(has_text=label).locator("input").first
        el.click()
        el.press("ControlOrMeta+A")
        el.press("Backspace")
        el.fill(value)
        self.page.wait_for_timeout(200)
        dlg.get_by_role("heading").first.click()  # neytral — kalendarni yopadi
        self.page.wait_for_timeout(200)

    def _dialog_create_close(self):
        """Dialog footer'idagi «Создать и закрыть» (text bilan — backdrop aria-label «Закрыть» EMAS).
        Ba'zan «Подтверждение — Создать? Да/Нет» chiqadi → «Да»."""
        dlg = self._dlg()
        dlg.locator("button").filter(has_text="Создать и закрыть").first.click()
        self.page.wait_for_timeout(600)
        self._confirm_yes_if_any()
        self._wait_dialog_closed()

    def _wait_dialog_closed(self, timeout: int = 10_000):
        try:
            self._dlg().wait_for(state="hidden", timeout=timeout)
        except Exception:
            pass
        self.page.wait_for_timeout(500)

    # ---- tab dialoglar --------------------------------------------------------------------------
    def add_bank_account(self, d: dict):
        dlg = self._open_tab_create("Расчетный счет")
        self._d_input(dlg, "Название счета", d["bank_acc_name"])        # *
        self._d_input(dlg, "МФО", d["bank_mfo"])
        # Банк* — MFO AVTO-to'ldirmaydi; dropdown grid (ustun sarlavha «Банк»/«МФО») → NOM bo'yicha tanlaymiz
        self._d_select(dlg, "Банк", d["bank_name"], exact=False)        # *
        self._d_input(dlg, "Расчетный счет", d["bank_acc_no"])          # *
        self._d_select_if_empty(dlg, "Валюта", "Узбекский сум")        # * (default to'ladi)
        self._d_input(dlg, "Примечание", d["bank_note"])
        self._dialog_create_close()

    def add_contact(self, d: dict):
        dlg = self._open_tab_create("Контактные лица")
        self._d_input(dlg, "Ф.И.О.", d["contact_fio"])                 # *
        try:
            self._d_select_first(dlg, "Должность", timeout=4_000)
        except Exception:
            # «Должность» bo'sh (spec: «Добавить» bilan yaratiladi) — ochiq dropdown overlay'ini yopamiz
            print("  [контакт] «Должность» varianti yo'q, o'tkazildi")
            self.page.keyboard.press("Escape")
            self.b._close_overlay()
            self.page.wait_for_timeout(300)
        self._d_input(dlg, "Телефон", d["contact_phone"])
        self._d_date(dlg, "Дата рождения", d["contact_bday"])
        self._dialog_create_close()

    def add_contract(self, d: dict):
        today = datetime.date.today()
        end = today.replace(year=today.year + 1)
        dlg = self._open_tab_create("Договор")
        self._d_input(dlg, "Название", d["contract_name"])             # *
        self._d_input(dlg, "Номер", d["contract_no"])                  # *
        self._d_date(dlg, "Дата оформления", today.strftime("%d.%m.%Y"))   # *
        self._d_date(dlg, "Дата окончания", end.strftime("%d.%m.%Y"))
        self._d_select_if_empty(dlg, "Валюта", "Узбекский сум")        # * (default to'ladi)
        self._d_input(dlg, "Сумма", d["contract_sum"])
        self._d_input(dlg, "Примечание", d["note"])
        self._dialog_create_close()

    # ---- inline tablar --------------------------------------------------------------------------
    def fill_note(self, d: dict):
        self.b.open_tab("Примечание")
        self.page.wait_for_timeout(600)
        ta = self.page.locator("main textarea").last
        ta.scroll_into_view_if_needed()
        ta.click()
        ta.fill(d["note"])

    def fill_leadership(self, d: dict):
        """Руководящие должности: Директор (nth 0) + Бухгалтер (nth 1) — label'lar takrorlanadi."""
        self.b.open_tab("Руководящие должности")
        self.page.wait_for_timeout(800)
        for label, (dv, av) in {
            "Имя": (d["dir_first"], d["acc_first"]),
            "Фамилия": (d["dir_last"], d["acc_last"]),
            "Отчество": (d["dir_middle"], d["acc_middle"]),
        }.items():
            inputs = self.page.locator("smt-control").filter(
                has=self.page.get_by_text(label, exact=True)).locator("input")
            # Direktor = 0, Buxgalter = 1 (mavjud bo'lsa)
            inputs.nth(0).fill(dv)
            if inputs.count() > 1:
                inputs.nth(1).fill(av)

    def fill_delivery(self):
        """График доставки: ish kunlari Пн–Пт ni belgilaydi (tolerant smoke)."""
        self.b.open_tab("График доставки")
        self.page.wait_for_timeout(800)
        for day in ["Пн", "Вт", "Ср", "Чт", "Пт"]:
            try:
                self.page.locator("main").get_by_role("button", name=day, exact=True).first.click()
                self.page.wait_for_timeout(150)
            except Exception:
                print(f"  [график] '{day}' bosilmadi, o'tkazildi")

    # ---- saqlash / tekshirish -------------------------------------------------------------------
    def _confirm_yes_if_any(self):
        try:
            dlg = self.page.locator("[role=dialog], .cdk-dialog-container").last
            btn = dlg.get_by_role("button", name="Да", exact=False).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                self.page.wait_for_timeout(600)
        except Exception:
            pass

    def save(self):
        self.b.save()
        self.page.wait_for_timeout(600)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(2_000)

    def find_in_list(self, name: str):
        self.open_list()
        self.b.search_list(name)
        self.page.wait_for_timeout(1_500)
        self.b.grid_row(name)

    def open_view(self, name: str):
        self.find_in_list(name)
        self.b.grid_row(name).click()
        self.page.wait_for_timeout(500)
        self.b.click_button("Просмотреть", exact=False)
        self.page.wait_for_timeout(2_000)
        assert self.page.get_by_text(name, exact=False).first.is_visible() \
            or "legal_person_view" in self.page.url, \
            f"Просмотр ochilmadi (URL={self.page.url})"

    def expect_supplier_created(self, name: str):
        """TC-03/6: «Сохранить в качестве поставщика» tufayli Склад→Поставщики ro'yxatida paydo bo'ladi."""
        self.page.goto(self.base_url + self.SUPPLIER_LIST, wait_until="commit", timeout=60_000)
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.b.search_list(name)
        self.page.wait_for_timeout(1_500)
        expect(self.page.locator("smt-data-table").get_by_text(name, exact=False).first).to_be_visible(timeout=15_000)
