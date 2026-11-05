"""
Цены / ТМЦ ga narx o'rnatish — a2 page object (TC-E2E-02).
Ro'yxat route: /a2/anor/mkr/price_type_list  (title «Цены»)
«Установка цен» route: /a2/anor/mkf/product_price?price_type_id=...  (title «Цены (установка)»)

Jonli tasdiqlangan struktura (mohir@xan, 2026-11-02):
  Цены ro'yxati: ustunlar Название/Альтернативное/Валюта/Тип цены/.../Статус; narx turi qatorlari
    «Sotish sum» (Цена продажи, Узбекский сум), «Olish sum» (Цена закупа) va boshqalar.
    Qator amallari: Просмотр, Изменить, Ценник, «Установка цен», Прикрепление, Настройка.
  Tablar (breadcrumb-link): Цены / Типы оплат / Скидки/наценки.
  «Установка цен»: grid (ustunlar №/Код/ТМЦ/Группа/Категория/Торговая марка/Средняя Приходная цена/
    «Цена с НДС и акцизом»=tahrirlanadigan YAGONA input). Tepada «Сохранить»/«Закрыть», ТМЦ/Услуга
    toggle, «Поиск...» (grid filtri). Narx yozib «Сохранить» → «Подтверждение — Сохранить? Да/Нет» →
    «Да» → Цены ro'yxatiga qaytadi. Qiymat «15 000» ko'rinishida (probel bilan guruhlanadi) saqlanadi.

  SOTUVGA TAYYORLIK (2026-11-04 topildi): ТМЦ sotuv buyurtmasining «Подбор» grid'ида ko'rinishi uchun
    «Sotish sum» narx turining AYNAN «Цена с НДС и акцизом» ustuni to'ldirilган bo'lishi SHART — stok
    bo'lsa ham, bu ustun bo'sh bo'lsa ТМЦ Подбор'да umuman chiqmaydi. set_price() shu ustunga yozadi va
    saqlangach bo'sh emasligini tekshiradi. (Jonli tasdiq: narx+stok birga bo'lган ТМЦ «100/100» bilan
    Подбор'да chiqdi.)
"""
import re

from playwright.sync_api import expect

from utils.base_page import BasePage


class PricePage:
    LIST_PATH = "/a2/anor/mkr/price_type_list"

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    # ---- navigatsiya ----------------------------------------------------------------------------
    def open_list(self):
        """Цены ro'yxatini ochadi va grid yuklanishini kutadi (a2 kontenti async)."""
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.b.expect_form_open("Цены")
        self.page.wait_for_selector("smt-data-table", timeout=30_000)
        self.page.wait_for_timeout(1_500)

    def open_tabs_smoke(self):
        """TC-02/1: breadcrumb tablari («Типы оплат», «Скидки/наценки») <a> link — har birini
        Цены sahifasidan bosib, mos ro'yxat xatosiz ochilishini tekshiradi, so'ng Цены ga qaytadi.
        (Tab bar shu bog'liq sahifalarda umumiy; ishonchli uchun har safar Цены'dan bosamiz.)"""
        for name, frag in [("Типы оплат", "payment_type_list"), ("Скидки/наценки", "margin_list")]:
            self.open_list()  # Цены — bu yerda barcha tab linklari mavjud
            link = self.page.get_by_role("link", name=name, exact=True).first
            link.wait_for(state="visible", timeout=10_000)
            link.click()
            self.page.wait_for_url(f"**/{frag}**", timeout=20_000)
            self.page.wait_for_selector("smt-data-table", timeout=30_000)
            self.page.wait_for_timeout(500)
            assert "smartup online" not in self.page.title().strip().lower(), f"«{name}» tab ochilmadi"
        self.open_list()  # Цены holatiga qaytamiz

    # ---- «Установка цен» ------------------------------------------------------------------------
    def open_ustanovka(self, price_type: str):
        """Цены ro'yxatida narx turi qatorini tanlab «Установка цен» sahifasini ochadi."""
        self.open_list()
        self.b.search_list(price_type)
        self.page.wait_for_timeout(800)
        self.page.locator("smt-data-table").get_by_text(price_type, exact=True).first.click()
        self.page.wait_for_timeout(800)
        self.b.click_button("Установка цен", exact=False)
        # Sarlavha «Установка цен: <narx turi>» — katta harf bilan, shuning uchun registrga qaramaymiz.
        expect(self.page).to_have_title(re.compile("установка", re.IGNORECASE), timeout=60_000)
        self.page.wait_for_selector("smt-data-table", timeout=30_000)
        self.page.wait_for_timeout(1_500)

    # «Установка цен» grid'ida tahrirlanadigan yagona ustun — AYNAN shu. Mahsulot sotuvда (buyurtma
    # «Подбор») chiqishi uchun shu ustun to'ldirilgan bo'lishi SHART (narx + stok birga). Qarang:
    # test_12 sotuv — narx shu ustunda bo'lmasa, ТМЦ Подбор grid'ida umuman ko'rinmaydi.
    PRICE_COLUMN = "Цена с НДС и акцизом"

    def _price_input(self, product: str):
        """«Установка цен» grid'ida mahsulotni qidirib, aniq SHU qatorning «Цена с НДС и акцизом»
        narx input'ini qaytaradi.

        Grid ichida 2 xil input: «Поиск...» (type=search) va narx (type=text). Grid'да yagona
        tahrirlanadigan ustun «Цена с НДС и акцизом» — qidiruv bitta qatorга filtrlangach
        `smt-data-table input[type=text]` aynan shu bitta narx input bo'ladi. Ustun sarlavhasini ham
        tekshiramiz: forma o'zgarib boshqa tahrirlanadigan ustun qo'shilsa, test jim xato yozmasdan
        baland ovozда yiqilsin."""
        # tahrirlanadigan ustun haqiqatan «Цена с НДС и акцизом» ekanini tasdiqlaymiz (intent + guard)
        expect(self.page.locator("smt-cell-header").get_by_text(self.PRICE_COLUMN, exact=False).first
               ).to_be_visible(timeout=15_000)
        self.b.search_list(product)
        inp = self.page.locator("smt-data-table input[type=text]")
        for _ in range(20):  # filtr joylashishini kutamiz (~10s)
            if inp.count() == 1:
                break
            self.page.wait_for_timeout(500)
        expect(inp).to_have_count(1)
        # qidiruv aynan shu mahsulotni topganini tasdiqlaymiz
        expect(self.page.locator("smt-data-table").get_by_text(product, exact=False).first).to_be_visible()
        return inp.first

    def _confirm_yes(self):
        """«Подтверждение — Сохранить? Да/Нет» dialogida «Да» bosadi."""
        dlg = self.page.locator("[role=dialog], .cdk-dialog-container").last
        btn = dlg.get_by_role("button", name="Да", exact=False).first
        btn.wait_for(state="visible", timeout=8_000)
        btn.click()
        self.page.wait_for_timeout(600)

    def set_price(self, price_type: str, product: str, amount: int):
        """Narx turi × ТМЦ uchun «Цена с НДС и акцизом» ni o'rnatadi va saqlaydi.
        «Сохранить» → «Да» → Цены ro'yxatiga qaytadi.

        MUHIM: Sotish narxi (price_type=«Sotish sum») shu ustunga yozilmasa, ТМЦ sotuv buyurtmasining
        «Подбор» grid'ida umuman ko'rinmaydi (stok bo'lsa ham). Shu sabab saqlashdan so'ng qiymat
        haqiqatan yozilganini (bo'sh emasligini) darhol tekshiramiz."""
        self.open_ustanovka(price_type)
        inp = self._price_input(product)
        inp.click()
        inp.press("ControlOrMeta+A")
        inp.press("Backspace")
        inp.fill(str(amount))
        inp.press("Tab")
        self.page.wait_for_timeout(300)
        self.b.save()          # «Сохранить»
        self._confirm_yes()    # «Сохранить?» → «Да»
        self.page.wait_for_timeout(2_000)
        # sotuvga tayyorlik kafolati: «Цена с НДС и акцизом» bo'sh qolmaganiga ishonch hosil qilamiz
        self.open_ustanovka(price_type)
        saved = re.sub(r"\D", "", self._price_input(product).input_value())
        assert saved == str(amount), (
            f"«{self.PRICE_COLUMN}» saqlanmadi: {price_type} × {product} — kutilgan {amount}, "
            f"maydonda raqamlar '{saved}'. Bu ustun bo'sh bo'lsa ТМЦ sotuvда (Подбор) chiqmaydi.")

    def expect_price(self, price_type: str, product: str, amount: int):
        """Narx turi «Установка цен» ni qayta ochib, saqlangan narxni tekshiradi (probel/format tolerant)."""
        self.open_ustanovka(price_type)
        inp = self._price_input(product)
        got = inp.input_value()
        digits = re.sub(r"\D", "", got)
        assert digits == str(amount), \
            f"{price_type} × {product}: kutilgan narx {amount}, lekin maydonda '{got}' (raqamlar: '{digits}')"
