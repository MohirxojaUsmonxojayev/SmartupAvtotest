"""
Yakuniy solishtiruv hisobotlari — a2 page object (TC-E2E-17, read-only).
  Остатки ТМЦ:        /a2/anor/mkw/balance/balance_list  (В наличии/Забронировано/Доступно)
  Отчет по должникам:  /a2/anor/rep/mdeal/offset/debtor_clients
DIQQAT: bu a2 (smt-*), ESKI UI EMAS. Faqat o'qish/tekshirish.
"""
import re

from playwright.sync_api import expect

from utils.base_page import BasePage


class ReportsPage:
    BALANCE_PATH = "/a2/anor/mkw/balance/balance_list"
    DEBTOR_PATH = "/a2/anor/rep/mdeal/offset/debtor_clients"

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    def stock(self, tmc_name: str) -> dict:
        """Остатки ТМЦ da ТМЦ qatorini topib {on_hand, reserved, available} (butun sonlar) qaytaradi.
        Ustunlar: Склад/Код/Название/Тип ТМЦ/Производитель/Регион/В наличии/Забронировано/Доступно/..."""
        self.page.goto(self.base_url + self.BALANCE_PATH, wait_until="commit", timeout=60_000)
        self.page.wait_for_selector("smt-data-table", timeout=30_000)
        self.page.wait_for_timeout(1_500)
        self.b.search_list(tmc_name)
        self.page.wait_for_timeout(2_500)
        row = self.page.locator("smt-data-table .smt-data-row").filter(has_text=tmc_name).first
        expect(row).to_be_visible(timeout=10_000)
        # faqat sof-son hujayralar (В наличии/Забронировано/Доступно). Код/nom raqamli matnlari
        # harf bilan birga bo'lgani uchun fullmatch'dan o'tmaydi → chiqib ketadi.
        nums = []
        for cell in row.locator("smt-cell-content").all():
            t = re.sub(r"\s", "", cell.inner_text() or "")
            if re.fullmatch(r"-?\d+", t):
                nums.append(int(t))
        return {
            "on_hand":   nums[0] if len(nums) > 0 else None,
            "reserved":  nums[1] if len(nums) > 1 else None,
            "available": nums[2] if len(nums) > 2 else None,
        }

    def is_debtor(self, client: str) -> bool:
        """Отчет по должникам da mijoz bor-yo'qligini qaytaradi (qarz 0 bo'lsa — yo'q)."""
        self.page.goto(self.base_url + self.DEBTOR_PATH, wait_until="commit", timeout=60_000)
        self.page.wait_for_timeout(4_000)
        try:
            self.page.wait_for_selector("smt-data-table", timeout=15_000)
        except Exception:
            pass
        self.page.wait_for_timeout(1_000)
        return self.page.get_by_text(client, exact=False).count() > 0
