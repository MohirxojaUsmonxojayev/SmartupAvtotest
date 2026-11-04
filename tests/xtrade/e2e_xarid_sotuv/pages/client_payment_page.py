"""
Оплата от клиента (mijozdan to'lov) — a2 page object (TC-E2E-16).
Ro'yxat: /a2/trade/tcs/cashin_list ; create → title «Оплата от клиента / Создание» (cashin+add).
DIQQAT: bu a2 (smt-*), ESKI UI EMAS.

Jonli tasdiqlangan (2026-11-04):
  Forma maydonlar: Номер оплаты, Дата и время* (default hozir), «Провести взаимозачёт» (CHECKBOX,
    yuqori-chap), Валюта* (default «Узбекский сум»), Сумма*, Тип оплаты* (select — birinchi ochilганда
    «Загрузка…», matn yozilgач yuklanadi), «Наличные деньги» tanlansa **Касса*** paydo bo'ladi (search
    select → «Основная касса»), Проект, Клиент* (select — tanlansa Баланс + Договор avto to'ladi),
    Баланс (RO), Договор (avto), Инкассатор, Торговый представитель, Примечание.
  Buttonlar: Сохранить / Провести / Закрыть. «Провести» → «Провести?» → Да (forma ochiq qoladi).
  Баланс: to'lovдан oldin −375 000; взаимозачёт bilan Провести → mijoz balansi kamayadi.
"""
import re

from playwright.sync_api import expect

from utils.base_page import BasePage


class ClientPaymentPage:
    LIST_PATH = "/a2/trade/tcs/cashin_list"

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    def open_create(self):
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.page.wait_for_timeout(800)
        self.page.get_by_role("button", name="Создать", exact=True).first.click()
        self.b.expect_form_open("Создание")   # title «Оплата от клиента / Создание» (katta С)
        self.page.wait_for_timeout(2_000)

    def _pick(self, label: str, text: str, *, exact: bool = False):
        """select: (shartли maydon bo'lsa — control ko'rinishini kutadi) → trigger → matn → variant
        KO'RINISHINI KUTIB tanlaydi. «Тип оплаты»/«Касса» «Загрузка…» sekin bo'lsa ham barqaror:
        fiks kutish o'rniga variant visible bo'lguncha (15s) kutamiz."""
        expect(self.b.control(label)).to_be_visible(timeout=15_000)  # shartли maydon paydo bo'lishi
        self.b._open_select(label)
        self.page.wait_for_timeout(1_000)
        box = self.page.locator(".cdk-overlay-container input").first
        if box.count() > 0:
            box.fill(text)
        opt = self.page.locator(".cdk-overlay-pane").get_by_text(text, exact=exact).first
        expect(opt).to_be_visible(timeout=15_000)   # «Загрузка…» tugashini kutadi
        opt.scroll_into_view_if_needed()
        opt.click()
        self.page.wait_for_timeout(500)
        self.b._close_overlay()

    def _balance(self, *, wait: bool = False) -> str:
        """«Баланс» (RO) qiymatini o'qiydi. wait=True → maydon to'lguncha (bo'sh bo'lmaguncha, ~8s)
        kutadi — Клиент tanlangач Баланс async to'lgani uchun (eski/bo'sh qiymatni o'qib qolmaslik)."""
        c = self.page.locator("smt-control").filter(has_text="Баланс").first
        inp = c.locator("input").first
        if wait:
            for _ in range(20):   # ~8s
                if (inp.input_value() or "").strip():
                    break
                self.page.wait_for_timeout(400)
        return re.sub(r"[^\d-]", "", inp.input_value() or "")

    def create_payment(self, number: str, amount: int, client: str,
                       kassa: str = "Основная касса", with_offset: bool = True) -> str:
        """To'lov yaratib «Провести» qiladi. Qaytaradi: to'lovдан OLDIN ko'rilган Баланс (raqam).
        Ketma-ketlik: Номер → Сумма → Тип оплаты «Наличные деньги» → Касса → Клиент (Баланс to'ladi)
        → «Провести взаимозачёт» ✓ → «Провести» → «Провести?» Да."""
        self.open_create()
        self.b.input(label="Номер оплаты", value=number)
        self.b.input(label="Сумма", value=str(amount))
        self._pick("Тип оплаты", "Наличные деньги", exact=True)
        self._pick("Касса", kassa, exact=False)   # _pick Касса control paydo bo'lishini kutadi
        self._pick("Клиент", client, exact=False)
        balance_before = self._balance(wait=True)   # Баланс async to'lishini kutadi
        if with_offset:
            self.b.checkbox("Провести взаимозачёт", True, exact=False)
            self.page.wait_for_timeout(800)
        self.page.get_by_role("button", name="Провести", exact=True).first.click()
        self.page.wait_for_timeout(1_000)
        self._confirm_yes()
        self.page.wait_for_timeout(2_500)
        return balance_before

    def _confirm_yes(self):
        """«Провести?» dialogida «Да» bosadi."""
        dlg = self.page.locator("[role=dialog], .cdk-dialog-container").last
        btn = dlg.get_by_role("button", name="Да", exact=False).first
        try:
            btn.wait_for(state="visible", timeout=8_000)
            btn.click()
            self.page.wait_for_timeout(600)
        except Exception:
            pass

    def read_client_balance(self, client: str) -> str:
        """Yangi forma ochib, mijozni tanlab «Баланс» qiymatini o'qiydi (saqlamaydi). Raqam (manfiy)."""
        self.open_create()
        self._pick("Клиент", client, exact=False)
        bal = self._balance(wait=True)
        self.page.get_by_role("button", name="Закрыть", exact=True).first.click()
        self.page.wait_for_timeout(800)
        return bal
