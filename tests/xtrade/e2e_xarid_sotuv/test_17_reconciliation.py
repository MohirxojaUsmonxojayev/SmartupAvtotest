"""TC-E2E-17 — Yakuniy solishtiruv: qoldiq va mijoz qarzi (zanjirning SO'NGGI qadami).
docs/e2e/E2E_test_cases.md (TC-E2E-17) ga qarang. Faqat read-only tekshiruvlar.
Oldindan: TC-01..16 (butun biznes sikli).

AVTOMATLASHTIRILGAN (ishonchli, to'g'ridan-to'g'ri ro'yxatlar):
  1. Остатки ТМЦ — В наличии = 75 (Приход 100 − Расход 30 + Возврат 5).
  2. Отчет по должникам — mijoz YO'Q (qarz 0, TC-16 da yopildi).
  3. Mijoz balansi = 0 (to'lov formasi «Баланс», TC-16 tasdig'i).
QO'LDA/alohida (murakkab parametrli hisobotlar — bu testга kiritilmagan): Взаиморасчеты с
  поставщиками (1 000 000 — xarid TC-10/11 da ИТОГО 1M bilan tasdiqlanган, ta'minotchiga to'lov
  qilinmagan), Материальный отчет, Проводки счетов (debet=kredit).
"""
import allure
import pytest

from config.servers import resolve_server

from .data import EXPECTED
from .pages.reports_page import ReportsPage
from .pages.client_payment_page import ClientPaymentPage

pytestmark = [pytest.mark.e2e]


@allure.title("TC-E2E-17: Yakuniy solishtiruv — Остаток В наличии 75, mijoz qarzi 0")
def test_17_reconciliation(e2e_page, e2e):
    server = resolve_server("xtrade")
    tmc = e2e.get("tmc_name")
    client = e2e.get("sale_order_client") or e2e.get("natural_person")
    assert tmc, "e2e['tmc_name'] yo'q (TC-01)"
    assert client, "e2e['sale_order_client'] yo'q (TC-12)"
    expected_stock = EXPECTED["stock_after_return"]   # 75
    rp = ReportsPage(e2e_page, server["base_url"])

    with allure.step(f"1 - Остатки ТМЦ: «{tmc}» В наличии = {expected_stock}"):
        st = rp.stock(tmc)
        assert st["on_hand"] == expected_stock, \
            f"В наличии kutilgan {expected_stock}, lekin {st['on_hand']} (to'liq: {st})"
        print(f"  [E2E-17] Остаток: В наличии {st['on_hand']}, Забронировано {st['reserved']}, "
              f"Доступно {st['available']}")

    with allure.step("2 - Отчет по должникам: mijoz YO'Q (qarz 0)"):
        assert not rp.is_debtor(client), \
            f"Mijoz «{client}» hali Отчет по должникам'да bor — qarz yopilmagan"

    with allure.step("3 - Mijoz balansi = 0 (to'lov formasi «Баланс»)"):
        pp = ClientPaymentPage(e2e_page, server["base_url"])
        bal = pp.read_client_balance(client)
        assert bal in ("0", "-0", ""), f"Mijoz balansi 0 bo'lishi kerak, lekin '{bal}'"

    print(f"[E2E-17] Yakuniy solishtiruv OK — Остаток В наличии {expected_stock}, mijoz qarzi 0. "
          f"BUTUN E2E ZANJIRI (Xarid→Sotuv→Qaytarish→To'lov) YAKUNLANDI.")
