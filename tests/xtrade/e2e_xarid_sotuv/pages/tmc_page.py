"""
ТМЦ (Товарно-материальные ценности) — a2 forma page object (TC-E2E-01).
Route: /a2/anor/mr/product/inventory_list

Jonli tasdiqlangan struktura (mohir@xan, 2026-10-30):
  Main: Статус (smt-switch), Название* (smt-input), Ед. изм.* (smt-data-select),
    Альтернативное название, Производители (select), Наборы ТМЦ* (multi-select),
    Типы ТМЦ (chip: Товар/Продукция/Сырье/...), Тип кейса 1/2 (select) + Кол-во в кейсе 1/2,
    Штрих-коды, Код, Порядковый номер, IKPU, Артикул код, ТН ВЭД, Вес нетто/брутто, Литр.
  Tablar: Вес, Характеристики, Штрих-коды (Добавить+grid), Файлы (Добавить+grid),
    Ед. изм. маркированных товаров, GTIN.
"""
import os

from playwright.sync_api import expect

from utils.base_page import BasePage

FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "files")


class TmcPage:
    LIST_PATH = "/a2/anor/mr/product/inventory_list"

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    # ---- navigatsiya ----------------------------------------------------------------------------
    def open_list(self):
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.b.expect_form_open("ТМЦ")

    def open_create(self):
        # a2 list kontenti async yuklanadi — «Создать» tugmasini kutamiz
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.b.click_button("Создать", exact=True)
        self.b.expect_form_open("создани")

    # ---- UMUMIY tekshiruvlar --------------------------------------------------------------------
    def check_empty_save_blocked(self):
        """UMUMIY 1: bo'sh forma «Сохранить» → saqlanmaydi (create formada qoladi)."""
        self.b.save()
        self.page.wait_for_timeout(1_000)
        # Saqlanmagan bo'lsa URL hali «add» da yoki title «создание» (ro'yxatga ketmaydi)
        assert "add" in self.page.url or "создани" in self.page.title().lower(), \
            f"Bo'sh forma saqlandi? URL={self.page.url}, title={self.page.title()}"

    def check_case2_disabled_before_case1(self):
        """UMUMIY/3: «Кол-во в кейсе (2 уровень)» 1-daraja tanlanmasdan nofaol (readonly)."""
        self.b.expect_field_locked("Кол-во в кейсе (2 уровень)")

    # ---- to'ldirish -----------------------------------------------------------------------------
    def fill_main(self, d: dict):
        """Asosiy maydonlarni to'ldiradi (majburiy* + ishonchli optional)."""
        self.b.input(label="Название", value=d["name"])          # *
        self.b.select(label="Ед. изм.", option=d["unit"])         # *
        self.b.multiselect_first("Наборы ТМЦ")                    # *
        self.b.input(label="Альтернативное название", value=d["alt_name"])
        self.b.input(label="Штрих-коды", value=d["barcode1"])
        self.b.input(label="Код", value=d["code"])
        self.b.input(label="Порядковый номер", value=d["order_no"])
        self.b.input(label="IKPU", value=d["ikpu"])
        self.b.input(label="Артикул код", value=d["article"])
        self.b.input(label="ТН ВЭД", value=d["tnved"])
        self.b.input(label="Вес нетто (кг)", value=d["weight_net"])
        self.b.input(label="Вес брутто (кг)", value=d["weight_gross"])
        self.b.input(label="Литр/Дециметр куб.", value=d["liter"])
        # dropdownlar — Товар reflow'idan OLDIN
        self.b.select_first("Производители")
        self.b.select_first("Тип кейса (1 уровень)")
        self.b.input(label="Кол-во в кейсе (1 уровень)", value=d["case1_qty"])
        self.b.select_first("Тип кейса (2 уровень)")
        self.b.input(label="Кол-во в кейсе (2 уровень)", value=d["case2_qty"])
        self.b.chip(d["tip"])                                     # Типы ТМЦ → Товар (OXIRGI — reflow qiladi)
        # qolgan: _
        #   Товар tanlangach reflow bo'ladi, dropdown trigger'i o'zgaradi.

    def add_image(self):
        """ТМЦ rasmini yuklaydi: file input → cropper oynasida «Сохранить»."""
        inp = self.page.locator("main input[type=file][accept*=image]").first
        inp.set_input_files(os.path.join(FILES_DIR, "qa.png"))
        self.page.wait_for_timeout(1_500)
        # cropper overlay (ichida «Сменить изображение») → «Сохранить» (faol bo'lsa)
        cropper = self.page.locator(".cdk-overlay-pane").filter(has_text="Сменить изображение")
        save = cropper.get_by_role("button", name="Сохранить").first
        if save.is_enabled():
            save.click()
        else:
            print("  [rasm] cropper «Сохранить» nofaol — «Закрыть» bilan yopiladi")
            cropper.get_by_role("button", name="Закрыть").first.click()
        self.page.wait_for_timeout(1_000)

    def fill_characteristics(self):
        """Tab «Характеристики»: dropdownlarda birinchi qiymatlarni tanlaydi.
        Ba'zi PG dropdownlari bo'sh bo'lishi mumkin — ular o'tkazib yuboriladi (log bilan)."""
        self.b.open_tab("Характеристики")
        self.page.wait_for_timeout(1_000)
        for lbl in ["Категория", "Торговая марка", "My_Type",
                    "PG6", "PG7", "PG8", "PG9", "PG10", "PG11", "PG12", "PG13"]:
            try:
                self.b.select_first(lbl, timeout=4_000)
            except Exception:
                print(f"  [характеристики] '{lbl}' — variant yo'q yoki topilmadi, o'tkazildi")

    # ---- tablar (dialog/upload — jonli aniqlangan) ----------------------------------------------
    def add_second_barcode(self, code: str):
        """Tab «Штрих-коды» → «Добавить» → dialog «Добавление штрих-кода» → kod → «Сохранить и закрыть»."""
        self.b.open_tab("Штрих-коды")
        self.page.wait_for_timeout(500)
        self.page.locator("main").get_by_role("button", name="Добавить").last.click()
        dlg = self.page.locator("[role=dialog][aria-modal]").first
        dlg.locator("input[type=text]").first.fill(code)
        dlg.get_by_role("button", name="Сохранить и закрыть", exact=False).click()
        self._wait_dialog_closed()

    def add_file(self, note: str = "QA fayl"):
        """Tab «Файлы» → «Добавить» → dialog: .pdf yuklab, MAJBURIY «Название *» + «Примечание» → «Сохранить и закрыть».

        Jonli aniqlangan (2026-11-02): dialogda majburiy «Название *» (birinchi text input) bor;
        u bo'sh bo'lsa dialog yopilmaydi — PDF/fayl o'zi muammo emas (208 B qa.pdf 100% yuklanadi).
        Maydonlar: «Название *» (text), «Примечание» (textarea), «Статус» (checkbox, default faol)."""
        self.b.open_tab("Файлы")
        self.page.wait_for_timeout(500)
        self.page.locator("main").get_by_role("button", name="Добавить").last.click()
        dlg = self.page.locator("[role=dialog][aria-modal]").first
        dlg.wait_for(state="visible", timeout=10_000)
        dlg.locator("input[type=file]").first.set_input_files(os.path.join(FILES_DIR, "qa.pdf"))
        self.page.wait_for_timeout(1_500)  # upload 100% bo'lishini kutamiz
        file_title = "QA-E2E fayl"
        dlg.locator("input[type=text]").first.fill(file_title)  # «Название *» (majburiy)
        ta = dlg.locator("textarea")
        if ta.count() > 0:
            ta.first.fill(note)  # «Примечание»
        self.page.wait_for_timeout(300)
        dlg.get_by_role("button", name="Сохранить и закрыть", exact=False).click()
        self._wait_dialog_closed()
        # dialog hali ochiq bo'lsa — majburiy maydon/validatsiya sababli yopilmagan → xatoni ko'rsatib yiqilamiz
        open_dlg = self.page.locator("[role=dialog][aria-modal]")
        if open_dlg.count() > 0 and open_dlg.first.is_visible():
            try:
                errs = open_dlg.first.locator("[class*=error],[class*=invalid],.text-red-500").all_inner_texts()
            except Exception:
                errs = []
            raise AssertionError(f"Файлы dialogi «Сохранить и закрыть» bilan yopilmadi (errs={errs})")
        # muvaffaqiyat tekshiruvi: Файлы grid'ida qo'shilgan fayl qatori ko'rinadi
        expect(self.page.locator("main").get_by_text(file_title, exact=False).first).to_be_visible(timeout=10_000)

    def _wait_dialog_closed(self, timeout: int = 10_000):
        """Modal dialog yopilishini kutadi (keyingi forma save'i to'silmasligi uchun)."""
        try:
            self.page.locator("[role=dialog][aria-modal]").first.wait_for(state="hidden", timeout=timeout)
        except Exception:
            pass
        self.page.wait_for_timeout(500)

    def open_tabs_smoke(self):
        """Har tabni ochib ko'rish (xatosiz ochilishini tekshirish)."""
        for t in ["Вес", "Характеристики", "Штрих-коды", "Файлы",
                  "Ед. изм. маркированных товаров", "GTIN"]:
            self.b.open_tab(t)
            self.page.wait_for_timeout(300)

    # ---- saqlash / tekshirish -------------------------------------------------------------------
    def save(self):
        # ochiq modal dialog qolsa yopamiz (forma «Сохранить»ini to'smasligi uchun)
        dlg = self.page.locator("[role=dialog][aria-modal]")
        if dlg.count() > 0 and dlg.first.is_visible():
            try:
                dlg.first.get_by_role("button", name="Закрыть").first.click(timeout=3_000)
            except Exception:
                pass
            self.page.wait_for_timeout(500)
        # Qat'iy kutish yetmaydi: fayl yuklash + saqlash 3 s dan oshishi mumkin, shu payt qilingan goto
        # ilovaning o'z navigatsiyasi bilan to'qnashib ERR_ABORTED beradi. Javob va ro'yxatni kutamiz.
        with self.page.expect_response(
            lambda r: r.request.method == "POST" and "/product/inventory+" in r.url and "$save" in r.url,
            timeout=60_000,
        ) as save_info:
            self.b.save()
        response = save_info.value
        assert response.ok, f"ТМЦ saqlanmadi: HTTP {response.status} ({response.url})"
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)

    def find_in_list(self, name: str):
        self.open_list()
        # grid toolbar yuklanishini kutamiz (async)
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.b.search_list(name)
        self.page.wait_for_timeout(2_000)
        self.b.grid_row(name)

    def open_view(self, name: str):
        """Ro'yxatda qatorni ochib «Просмотр» ga o'tadi."""
        self.find_in_list(name)
        self.b.grid_row(name).click()
        self.page.wait_for_timeout(500)
        self.b.click_button("Просмотр", exact=False)
        self.page.wait_for_timeout(2_000)
        # Просмотр ochilganini tekshiramiz: nom ko'rinadi YOKI list'dan ketdik (view URL)
        name_visible = self.page.get_by_text(name, exact=False).first.is_visible()
        assert name_visible or "inventory_list" not in self.page.url, \
            f"Просмотр ochilmadi (nom ko'rinmadi, URL={self.page.url})"

    def _confirm_yes(self):
        """«Подтверждение — Изменить статус … Да/Нет» dialogida «Да» bosadi.
        Status o'zgartirish har doim shu tasdiq oynasini chiqaradi (jonli, 2026-11-02)."""
        dlg = self.page.locator("[role=dialog], .cdk-dialog-container").last
        btn = dlg.get_by_role("button", name="Да", exact=False).first
        try:
            btn.wait_for(state="visible", timeout=8_000)
            btn.click()
            self.page.wait_for_timeout(600)
        except Exception:
            pass  # tasdiq chiqmagan bo'lsa (ehtimoli past) — davom etamiz

    def _show_all_in_list(self):
        """Ro'yxat filtri: «Показать все» → nofaol yozuvlar ham ko'rinadi.
        Jonli (2026-11-02): smt-data-table-filter funnel → panelda «Показать все» BITTA bosish bilan
        qo'llanadi («Применить» shart emas)."""
        self.page.locator("smt-data-table-filter button").first.click()
        self.page.wait_for_timeout(1_000)
        self.page.get_by_role("button", name="Показать все", exact=False).first.click()
        self.page.wait_for_timeout(1_500)

    def toggle_status_in_list(self, name: str):
        """Ro'yxatda: «Неактивный» → («Показать все» filtri) → «Активный». Oxiri Активный — zanjir uchun SHART.

        Jonli aniqlangan oqim (2026-11-02):
          - qator tanlangach amal tugmalari: «Неактивный»/«Активный» (bevosita tugma);
          - har o'zgartirish «Подтверждение … Да/Нет» tasdiq oynasini chiqaradi → «Да»;
          - «Неактивный» qilingach qator faol (default) ro'yxatdan DARHOL filtrlanadi → qayta aktivlash
            uchun «Показать все» filtri yoqilib, qidirib topiladi."""
        # --- Неактивный (qator hozircha faol, default ro'yxatda) ---
        self.find_in_list(name)
        self.b.grid_row(name).click()
        self.page.wait_for_timeout(800)
        self.b.click_button("Неактивный", exact=False)
        self._confirm_yes()
        self.page.wait_for_timeout(1_500)
        # --- qayta Активный: «Показать все» bilan nofaolni topib ---
        self.open_list()
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self._show_all_in_list()
        self.b.search_list(name)
        self.page.wait_for_timeout(1_500)
        self.b.grid_row(name).click()
        self.page.wait_for_timeout(800)
        self.b.click_button("Активный", exact=False)
        self._confirm_yes()
        self.page.wait_for_timeout(1_500)
        # tasdiq: endi aktiv → DEFAULT (faol) ro'yxatda qayta ko'rinadi (zanjir uchun SHART)
        self.find_in_list(name)

    def edit_order_no(self, name: str, new_value: str):
        """«Изменить» → Порядковый номер o'zgartirib saqlaydi."""
        self.find_in_list(name)
        self.b.grid_row(name).click()
        self.page.wait_for_timeout(500)
        self.b.click_button("Изменить", exact=False)
        self.b.expect_form_open()
        self.b.input(label="Порядковый номер", value=new_value)
        self.save()
