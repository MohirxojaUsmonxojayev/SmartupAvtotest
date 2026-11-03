"""
Физическое лицо (mijoz) — a2 page object (TC-E2E-04).
Ro'yxat route: /a2/anor/mr/person/natural_person_list ; create: …+add (title «Физическое лицо (создание)»).
Mijoz (Клиент) ro'yxati: /a2/anor/mrf/client_list.

Jonli tasdiqlangan struktura (mohir@xan, 2026-11-03):
  Main: Пол (RADIO-GROUP M=Мужской/F=Женский), Фамилия (input), Имя* (DATA-SELECT autocomplete — erkin
    matn, «Ничего не найдено» overlay heading-klik bilan yopiladi), Отчество (input), Код (input),
    Дата рождения (date — Escape YOPMAYDI, neytral klik), Серийный номер паспорта (input),
    Статус (switch), Регион (tree «Toshkent»), Адрес/Почтовый адрес (textarea),
    Юридическое лицо (data-select), Телефон/ИНН-ПНФЛ/Телеграм/Email/Веб-сайт (input),
    Рабочие зоны (multi), GPS (readonly — SKIP), Ответственный (data-select),
    checkbox Клиент/Поставщик/Сотрудник.
  Majburiy: Имя*, Группа*, Категория* (oxirgi ikki — Характеристики tab).
  Tablar: Характеристики, Расчетный счет, Файлы(SKIP), Договор, Примечание, График доставки.
    «Клиент» belgilangач +«Адреса доставки» tab (dialog: Код, Адрес доставки короткий*, Адрес доставки
    полный*, GPS, Статус, «Адрес доставки по умолчанию»).
  Har saqlash «Подтверждение — Сохранить? Да/Нет» → «Да». Email/Телефон/ПНФЛ/паспорт UNIQUE.
"""
import datetime

from playwright.sync_api import expect

from utils.base_page import BasePage


class NaturalPersonPage:
    LIST_PATH = "/a2/anor/mr/person/natural_person_list"
    CLIENT_LIST = "/a2/anor/mrf/client_list"
    SECTION = "Основная информация"  # neytral klik nishoni (kalendar/autocomplete overlay yopish)

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    # ---- navigatsiya ----------------------------------------------------------------------------
    def open_list(self):
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.b.expect_form_open("Физическ")
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)

    def open_create(self):
        self.page.get_by_role("button", name="Создать", exact=True).first.click()
        self.b.expect_form_open("создани")
        self.page.wait_for_timeout(1_500)

    def _neutral_click(self):
        """Overlay (kalendar/autocomplete) yopish uchun forma sarlavhasiga neytral klik."""
        self.page.locator("main").get_by_text(self.SECTION, exact=True).first.click()
        self.page.wait_for_timeout(200)

    # ---- UMUMIY tekshiruv -----------------------------------------------------------------------
    def check_empty_save_blocked(self):
        """UMUMIY 1: bo'sh forma «Сохранить» → Имя/Группа/Категория qizil, create formada qoladi."""
        self.b.save()
        self.page.wait_for_timeout(800)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(800)
        assert "add" in self.page.url or "создани" in self.page.title().lower(), \
            f"Bo'sh forma saqlandi? URL={self.page.url}, title={self.page.title()}"

    # ---- main maydonlar -------------------------------------------------------------------------
    def _set_gender(self, text: str):
        self.b.control("Пол").get_by_text(text, exact=True).first.click()
        self.page.wait_for_timeout(200)

    def _fill_name_autocomplete(self, value: str):
        """Имя* — data-select autocomplete: erkin matn yoziladi, «Ничего не найдено» overlay neytral
        klik bilan yopiladi (Enter/Escape yopmaydi)."""
        inp = self.b.control("Имя").locator("input").first
        inp.click()
        inp.fill(value)
        self.page.wait_for_timeout(800)
        self._neutral_click()

    def _date_main(self, label: str, value: str):
        """Main-forma smt-date-picker: sana yozib, kalendar overlay'ni neytral klik bilan yopadi."""
        el = self.b.control(label).locator("input").first
        el.click()
        el.press("ControlOrMeta+A")
        el.press("Backspace")
        el.fill(value)
        self.page.wait_for_timeout(200)
        self._neutral_click()

    def fill_main(self, d: dict):
        self._set_gender("Женский")          # Пол: Женский ga o'tkazib...
        self._set_gender("Мужской")          # ...qaytaramiz (oxiri Мужской)
        self.b.input(label="Фамилия", value=d["surname"])
        self._fill_name_autocomplete(d["first_name"])   # Имя * (autocomplete)
        self.b.input(label="Отчество", value=d["middle"])
        self.b.input(label="Код", value=d["code"])
        self._date_main("Дата рождения", d["bday"])
        self.b.input(label="Серийный номер паспорта", value=d["passport"])
        self.b.tree_select("Регион", d["region"])
        self.b.input(label="Адрес", value=d["address"])
        self.b.input(label="Почтовый адрес", value=d["post_addr"])
        if d.get("legal_person"):
            try:
                self.b.select(label="Юридическое лицо", option=d["legal_person"], exact=False, timeout=8_000)
            except Exception:
                print(f"  [юр.лицо] '{d['legal_person']}' topilmadi — birinchi variant")
                self.b._close_overlay()
                self.b.select_first("Юридическое лицо")
        else:
            self.b.select_first("Юридическое лицо")
        self.b.input(label="Телефон", value=d["phone"])
        self.b.input(label="ИНН/ПНФЛ", value=d["pnfl"])          # UNIQUE
        self.b.input(label="Телеграм", value=d["telegram"])
        self.b.input(label="Email", value=d["email"])
        self.b.input(label="Веб-сайт", value=d["web"])
        # Рабочие зоны = «Room - Yashnobod» (sotuv buyurtmasida mijoz shu zona bo'yicha FILTRLANADI — SHART)
        try:
            self.b.multiselect("Рабочие зоны", "Room - Yashnobod", exact=False)
        except Exception:
            print("  [раб.зоны] «Room - Yashnobod» topilmadi — birinchi variant")
            self.b._close_overlay()
            self.b.multiselect_first("Рабочие зоны")
        self.b.select_first("Ответственный")
        # GPS — mustasno (spec)
        # checkboxlar: Клиент=Да (mijoz avto-yaratiladi); Поставщик/Сотрудник — yoqib-o'chirib ko'rish
        self.b.checkbox("Поставщик", True); self.b.checkbox("Поставщик", False)
        self.b.checkbox("Сотрудник", True); self.b.checkbox("Сотрудник", False)
        self.b.checkbox("Клиент", True)

    def fill_characteristics(self):
        self.b.open_tab("Характеристики")
        self.page.wait_for_timeout(800)
        self.b.select_first("Группа")        # *
        self.b.select_first("Категория")     # *
        try:
            self.b.select_first("Тип", timeout=4_000)
        except Exception:
            print("  [характеристики] «Тип» varianti yo'q, o'tkazildi")
            self.b._close_overlay()

    # ---- dialog helperlari (TC-03 pattern) ------------------------------------------------------
    def _dlg(self):
        return self.page.locator("[role=dialog][aria-modal]").first

    def _open_tab_create(self, tab: str):
        """Natural person tab-grid'larida add tugmasi «Добавить» (legal person'da «Создать» edi)."""
        self.b.open_tab(tab)
        self.page.wait_for_timeout(700)
        self.page.locator("main").get_by_role("button", name="Добавить", exact=True).last.click()
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

    def _d_select(self, dlg, label: str, option: str, *, exact: bool = False, timeout: int = 15_000):
        self.b._close_overlay()
        dlg.locator("smt-control").filter(has_text=label).locator("smt-data-select, input").first.click()
        opt = self.page.locator(".cdk-overlay-container").get_by_text(option, exact=exact).first
        expect(opt).to_be_visible(timeout=timeout)
        opt.scroll_into_view_if_needed()
        opt.click()
        self.b._close_overlay()

    def _d_select_if_empty(self, dlg, label: str, option: str):
        val = dlg.locator("smt-control").filter(has_text=label).locator("input").first.input_value()
        if not val.strip():
            self._d_select(dlg, label, option)

    def _d_date(self, dlg, label: str, value: str):
        el = dlg.locator("smt-control").filter(has_text=label).locator("input").first
        el.click()
        el.press("ControlOrMeta+A")
        el.press("Backspace")
        el.fill(value)
        self.page.wait_for_timeout(200)
        dlg.get_by_role("heading").first.click()
        self.page.wait_for_timeout(200)

    def _dialog_create_close(self):
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
        self._d_input(dlg, "Название", d["bank_acc_name"])      # natural person: «Название *» (legal: «Название счета»)
        self._d_input(dlg, "МФО", d["bank_mfo"])
        self._d_select(dlg, "Банк", d["bank_name"])
        self._d_input(dlg, "Расчетный счет", d["bank_acc_no"])
        self._d_select_if_empty(dlg, "Валюта", "Узбекский сум")
        self._d_input(dlg, "Примечание", d["bank_note"])
        self._dialog_create_close()

    def add_contract(self, d: dict):
        today = datetime.date.today()
        end = today.replace(year=today.year + 1)
        dlg = self._open_tab_create("Договор")
        self._d_input(dlg, "Название", d["contract_name"])
        self._d_input(dlg, "Номер", d["contract_no"])
        self._d_date(dlg, "Дата оформления", today.strftime("%d.%m.%Y"))
        self._d_date(dlg, "Дата окончания", end.strftime("%d.%m.%Y"))
        self._d_select_if_empty(dlg, "Валюта", "Узбекский сум")
        self._d_input(dlg, "Сумма", d["contract_sum"])
        self._d_input(dlg, "Примечание", d["note"])
        self._dialog_create_close()

    def add_delivery_address(self, d: dict):
        """«Адреса доставки» tab (Клиент belgilangach): короткий* + полный* → «Создать и закрыть»."""
        dlg = self._open_tab_create("Адреса доставки")
        # labellarда ikki nuqta bor: «Адрес доставки: короткий *» / «: полный *» → distinktiv substring
        self._d_input(dlg, "короткий", d["deliv_short"])
        self._d_input(dlg, "полный", d["deliv_full"])
        self._dialog_create_close()

    # ---- inline tablar --------------------------------------------------------------------------
    def fill_note(self, d: dict):
        self.b.open_tab("Примечание")
        self.page.wait_for_timeout(600)
        ta = self.page.locator("main textarea").last
        ta.scroll_into_view_if_needed()
        ta.click()
        ta.fill(d["note"])

    def fill_delivery_schedule(self):
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

    def verify_in_list(self, name: str, code: str = "", gender: str = ""):
        """TC-04/3 «Просмотр»: natural person listда alohida «Просмотреть» amali YO'Q — grid qatorining
        o'zi barcha ustun qiymatlarini ko'rsatadi (Код/ИНН-ПНФЛ/Пол/Группа/Категория/Статус).
        Qatorni topib kalit qiymatlar o'sha gridда ko'rinishini tasdiqlaydi."""
        self.find_in_list(name)
        table = self.page.locator("smt-data-table")
        if code:
            expect(table.get_by_text(code, exact=False).first).to_be_visible(timeout=10_000)
        if gender:
            expect(table.get_by_text(gender, exact=False).first).to_be_visible(timeout=10_000)

    def expect_client_created(self, name: str):
        """TC-04/4: «☑ Клиент» tufayli Справочники→Клиенты ro'yxatida paydo bo'ladi."""
        self.page.goto(self.base_url + self.CLIENT_LIST, wait_until="commit", timeout=60_000)
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.b.search_list(name)
        self.page.wait_for_timeout(1_500)
        expect(self.page.locator("smt-data-table").get_by_text(name, exact=False).first).to_be_visible(timeout=15_000)
