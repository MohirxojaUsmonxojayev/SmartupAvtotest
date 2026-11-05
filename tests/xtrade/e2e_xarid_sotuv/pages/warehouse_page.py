"""
Склад (ombor) — a2 page object (TC-E2E-06).
Ro'yxat: /a2/anor/mkw/warehouse_list ; create: …+add (title «Склад (создание)»). Tab YO'Q (bitta forma).

Jonli tasdiqlangan (mohir@xan, 2026-11-03):
  Название* (input), Тип склада* (data-select), Материально ответственное лицо (data-select),
  Рабочие зоны (multi), Автотранспорт (multi), Код (input), Порядковый номер (input),
  Примечание (textarea), «Параметры объема склада» (RADIO: Прямые углы=R default / Округленные углы=C),
  Высота (м)/Ширина (м)/Длина (м)/Объем (м3) (input — Объем AVTO-hisoblanmaydi, qo'lda),
  Адрес (textarea), Температурный режим / Влажность помещения (data-select), Регион (tree),
  GPS (readonly — SKIP), Ориентир (textarea). Majburiy: Название*, Тип склада*.
"""
import re

from playwright.sync_api import expect

from utils.base_page import BasePage


class WarehousePage:
    LIST_PATH = "/a2/anor/mkw/warehouse_list"

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

    def _confirm_yes_if_any(self):
        try:
            dlg = self.page.locator("[role=dialog], .cdk-dialog-container").last
            btn = dlg.get_by_role("button", name="Да", exact=False).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                self.page.wait_for_timeout(600)
        except Exception:
            pass

    # ---- UMUMIY -------------------------------------------------------------------------------
    def check_empty_save_blocked(self):
        """UMUMIY 1: bo'sh forma «Сохранить» → Название/Тип склада qizil, create formada qoladi."""
        self.b.save()
        self.page.wait_for_timeout(800)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(800)
        assert "add" in self.page.url or "создани" in self.page.title().lower(), \
            f"Bo'sh forma saqlandi? URL={self.page.url}, title={self.page.title()}"

    # ---- to'ldirish ---------------------------------------------------------------------------
    def _set_angles(self, text: str):
        """«Параметры объема склада» radio: «Прямые углы»/«Округленные углы» (matn main'да unikal)."""
        self.page.locator("main").get_by_text(text, exact=True).first.click()
        self.page.wait_for_timeout(300)

    def _ensure_select(self, label: str, timeout: int = 5_000):
        """smt-data-select'ni FAQAT bo'sh bo'lsa to'ldiradi (ba'zilari default bilan keladi)."""
        val = self.b.control(label).locator("input").first.input_value()
        if val.strip():
            return
        try:
            self.b.select_first(label, timeout=timeout)
        except Exception:
            print(f"  [склад] '{label}' varianti yo'q, o'tkazildi"); self.b._close_overlay()

    def fill_main(self, d: dict) -> str:
        """Barcha maydonlarni to'ldiradi. Hisoblangan Объ (м3) ni qaytaradi.
        «Тип склада» (default «Main») va «Автотранспорт» (default «Весь автотранспорт») — oldindan to'la."""
        self.b.input(label="Название", value=d["name"])             # *
        self.b.input(label="Код", value=d["code"])
        self.b.input(label="Порядковый номер", value=d["order_no"])
        self._ensure_select("Тип склада")                           # * (default «Main» — o'tkaziladi)
        self._ensure_select("Материально ответственное лицо")
        # Рабочие зоны = «Room - Yashnobod» (sotuvda ТМЦ shu zona bo'yicha FILTRLANADI — ombor shu zonaga bog'lansin)
        self.b.multiselect("Рабочие зоны", "Room - Yashnobod", exact=False)
        # «Автотранспорт» default «Весь автотранспорт» — o'tkazamiz
        self.b.input(label="Примечание", value=d["note"])
        # Параметры объема: Прямые углы → o'lchamlar; Округленные углы ga o'tib qaytaramiz
        self._set_angles("Прямые углы")
        self.b.input(label="Высота (м)", value=d["height"])
        self.b.input(label="Ширина (м)", value=d["width"])
        self.b.input(label="Длина (м)", value=d["length"], press_tab=True)
        self.page.wait_for_timeout(600)
        vol = self.b.control("Объем (м3)").locator("input").first
        if not (vol.input_value() or "").strip():
            vol.click(); vol.fill(d["volume"])   # avto-hisoblanmaydi → qo'lda 600
        got_vol = re.sub(r"\D", "", vol.input_value() or "")
        self._set_angles("Округленные углы"); self._set_angles("Прямые углы")  # toggle (smoke)
        self.b.input(label="Адрес", value=d["address"])
        self.b.input(label="Ориентир", value=d["orientir"])
        self.b.tree_select("Регион", d["region"])
        self._ensure_select("Температурный режим")
        self._ensure_select("Влажность помещения")
        return got_vol

    # ---- saqlash / tekshirish -----------------------------------------------------------------
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
        for label in ["Просмотреть", "Просмотр"]:
            btn = self.page.get_by_role("button", name=label, exact=False)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                break
        self.page.wait_for_timeout(2_000)
        assert self.page.get_by_text(name, exact=False).first.is_visible() \
            or "warehouse_view" in self.page.url, \
            f"Просмотр ochilmadi (URL={self.page.url})"
