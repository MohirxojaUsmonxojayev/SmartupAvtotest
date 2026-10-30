"""
ТМЦ (Товарно-материальные ценности) — a2 forma page object.
Route: /a2/anor/mr/product/inventory_list  (yangi /a2 UI, smt-* komponentlar).

Jonli tasdiqlangan maydonlar (mohir@xan, 2026-10-30):
  Название* (smt-input), Ед. изм.* (smt-data-select), Наборы ТМЦ* (majburiy),
  Код, Альтернативное название, Штрих-коды, IKPU, Артикул код, ТН ВЭД (smt-input),
  Производители, Тип кейса (1/2 уровень) (smt-data-select).
  Tablar: Вес, Характеристики, Штрих-коды, Файлы, Ед. изм. маркированных товаров, GTIN.
"""
from utils.base_page import BasePage


class TmcPage:
    LIST_PATH = "/a2/anor/mr/product/inventory_list"

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    # ------------------------------------------------------------------------------------------------------------------
    def open_list(self):
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.b.expect_form_open("ТМЦ")

    def open_create(self):
        self.b.click_button("Создать", exact=True)
        self.b.expect_form_open("создани")

    # ------------------------------------------------------------------------------------------------------------------
    def create_minimal(self, *, name: str, unit: str, code: str):
        """Majburiy maydonlar bilan ТМЦ yaratadi (Название, Ед. изм., Наборы ТМЦ) + Код."""
        self.b.input(label="Название", value=name)
        self.b.select(label="Ед. изм.", option=unit)
        self.b.select_first("Наборы ТМЦ")      # "ro'yxatdagi birinchi to'plam"
        self.b.input(label="Код", value=code)
        self.b.save()

    def verify_in_list(self, name: str):
        """Saqlangandan keyin ro'yxatda nom bo'yicha topilishini tekshiradi."""
        self.open_list()
        self.b.search_list(name)
        self.b.grid_row(name)
