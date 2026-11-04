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
        """select: trigger → (Загрузка bo'lsa matn yozilgach yuklanadi) → ko'rinadigan pane'dan tanlash."""
        self.b._open_select(label)
        self.page.wait_for_timeout(1_200)
        box = self.page.locator(".cdk-overlay-container input").first
        if box.count() > 0:
            box.fill(text)
            self.page.wait_for_timeout(2_000)   # «Загрузка…» tugashi uchun
        self.page.locator(".cdk-overlay-pane").get_by_text(text, exact=exact).first.click()
        self.page.wait_for_timeout(500)
        self.b._close_overlay()

    def _balance(self) -> str:
        c = self.page.locator("smt-control").filter(has_text="Баланс").first
        return re.sub(r"[^\d-]", "", c.locator("input").first.input_value() or "")

    def create_payment(self, number: str, amount: int, client: str,
                       kassa: str = "Основная касса", with_offset: bool = True) -> str:
        """To'lov yaratib «Провести» qiladi. Qaytaradi: to'lovдан OLDIN ko'rilган Баланс (raqam).
        Ketma-ketlik: Номер → Сумма → Тип оплаты «Наличные деньги» → Касса → Клиент (Баланс to'ladi)
        → «Провести взаимозачёт» ✓ → «Провести» → «Провести?» Да."""
        self.open_create()
        self.b.input(label="Номер оплаты", value=number)
        self.b.input(label="Сумма", value=str(amount))
        self._pick("Тип оплаты", "Наличные деньги", exact=True)
        self.page.wait_for_timeout(1_000)
        self._pick("Касса", kassa, exact=False)
        self._pick("Клиент", client, exact=False)
        self.page.wait_for_timeout(1_500)
        balance_before = self._balance()
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
        self.page.wait_for_timeout(1_500)
        bal = self._balance()
        self.page.get_by_role("button", name="Закрыть", exact=True).first.click()
        self.page.wait_for_timeout(800)
        return bal
