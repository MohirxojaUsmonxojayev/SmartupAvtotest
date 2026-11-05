"""
Поставщик (ta'minotchi) — a2 page object (TC-E2E-05).
Ro'yxat: /a2/anor/mkw/supplier_list. TC-03 da «Сохранить в качестве поставщика» tufayli AVTO-yaratiladi,
shuning uchun bu case «Изменить» orqali (НДС/Акциз kalitlari) + Просмотр.

Jonli tasdiqlangan (mohir@xan, 2026-11-03):
  Supplier Изменить form: Тип поставщика (select), Название (select — shaxs), НДС (switch, default Нет),
    Акциз (switch, default Нет). Tugmalar: Сохранить/Закрыть. Qator amali «Прикрепить ТМЦ» ham bor.
  ТМЦ edit main formda «Поставщики» = SMT-MULTI-DATA-SELECT — ta'minotchi shu yerda qo'shiladi
    (ТМЦ Изменить tab'larida alohida «Поставщики» tab YO'Q).
"""
from playwright.sync_api import expect

from utils.base_page import BasePage


class SupplierPage:
    LIST_PATH = "/a2/anor/mkw/supplier_list"
    TMC_LIST = "/a2/anor/mr/product/inventory_list"

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    # ---- navigatsiya ----------------------------------------------------------------------------
    def open_list(self):
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.page.wait_for_timeout(1_000)

    def open_edit(self, name: str):
        self.open_list()
        self.b.search_list(name)
        self.page.wait_for_timeout(1_500)
        self.b.grid_row(name).click()
        self.page.wait_for_timeout(700)
        self.b.click_button("Изменить", exact=False)
        self.b.expect_form_open("изменени")
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

    def _save(self):
        self.b.save()
        self.page.wait_for_timeout(600)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(2_000)

    # ---- TC-05 asosiy oqimi ---------------------------------------------------------------------
    def toggle_vat_excise(self):
        """НДС/Акциз kalitlarini yoqib-o'chirib ko'radi; OXIRI IKKALASI O'CHIQ (Нет) —
        30.10 qarori: arifmetikani soddalashtirish uchun НДС o'chiq qoladi."""
        self.b.switch_set("НДС", True); self.page.wait_for_timeout(300)
        self.b.switch_set("НДС", False)
        self.b.switch_set("Акциз", True); self.page.wait_for_timeout(300)
        self.b.switch_set("Акциз", False)

    def smart_search_smoke(self):
        """«Умный поиск» tugmasi bo'lsa bosib-yopib ko'radi (tolerant smoke)."""
        try:
            btn = self.page.get_by_role("button", name="Умный поиск", exact=False).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                self.page.wait_for_timeout(800)
                self.page.keyboard.press("Escape")
                self.page.wait_for_timeout(400)
        except Exception:
            print("  [умный поиск] tugma yo'q/ochilmadi, o'tkazildi")

    def expect_vat_off(self, name: str):
        """Saqlangandan keyin qayta Изменить ochib НДС/Акциз = Нет ekanini tasdiqlaydi (Просмотр o'rnini bosadi)."""
        self.open_edit(name)
        assert not self.b.switch_state("НДС"), "НДС yoqilgan qoldi — kutilgan Нет"
        assert not self.b.switch_state("Акциз"), "Акциз yoqilgan qoldi — kutilgan Нет"

    def edit_toggles_save(self, name: str):
        self.open_edit(name)
        self.toggle_vat_excise()
        self.smart_search_smoke()
        self._save()

    # ---- MAJBURIY: ТМЦ ga ta'minotchini bog'lash ------------------------------------------------
    def link_supplier_to_tmc(self, tmc: str, supplier: str):
        """ТМЦ Изменить → main «Поставщики» (multi-select) ga ta'minotchini qo'shib saqlaydi.
        (Заказ на закупку'da ta'minotchi tanlash uchun SHART — spec TC-05/6.)"""
        self.page.goto(self.base_url + self.TMC_LIST, wait_until="commit", timeout=60_000)
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.b.search_list(tmc)
        self.page.wait_for_timeout(1_500)
        self.b.grid_row(tmc).click()
        self.page.wait_for_timeout(700)
        self.b.click_button("Изменить", exact=False)
        self.b.expect_form_open("изменени")
        self.page.wait_for_timeout(1_500)
        # «Поставщики» multiselect: trigger → qidiruv → variant.
        # Har run yangi ta'minotchi qo'shadi va u to'la ro'yxatda pastga tushadi; aylantirib darhol
        # bosish tanlovni yozmaydi (supplier_id bo'sh saqlanadi). Shuning uchun filtrlab bosamiz.
        self.b._close_overlay()
        pos = self.b.control("Поставщики")
        pos.locator("smt-multi-data-select, smt-data-select, input").first.click()
        with self.page.expect_response(
            lambda r: "inventory+edit:suppliers" in r.url and "esearch" in (r.request.post_data or ""),
            timeout=15_000,
        ):
            pos.locator("input").first.fill(supplier)
        opt = self.page.locator(".cdk-overlay-pane li").filter(has_text=supplier).first
        expect(opt).to_be_visible(timeout=15_000)
        self.page.wait_for_timeout(200)
        opt.click()
        # Saqlashdan oldin tanlov formaga yozilganini tasdiqlaymiz
        expect(pos.locator("smt-tag").filter(has_text=supplier).first).to_be_visible(timeout=10_000)
        self.b._close_overlay()
        self._save()

    def expect_tmc_has_supplier(self, tmc: str, supplier: str):
        """ТМЦ Изменित ochib «Поставщики» da ta'minotchi borligini tasdiqlaydi."""
        self.page.goto(self.base_url + self.TMC_LIST, wait_until="commit", timeout=60_000)
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.b.search_list(tmc)
        self.page.wait_for_timeout(1_500)
        self.b.grid_row(tmc).click()
        self.page.wait_for_timeout(700)
        self.b.click_button("Изменить", exact=False)
        self.b.expect_form_open("изменени")
        self.page.wait_for_timeout(1_500)
        expect(self.b.control("Поставщики").get_by_text(supplier, exact=False).first).to_be_visible(timeout=10_000)
