"""TC-E2E-16 — Mijozdan to'lov qabul qilish, qarz yopilishi.
docs/e2e/E2E_test_cases.md (TC-E2E-16) ga qarang.
Oldindan: TC-15 (buyurtma arxivlanган, mijoz qarzi 375 000 — e2e['sale_order_client']).
DIQQAT: a2 — Финансы → Оплаты от клиентов → «Создать» (/a2/trade/tcs/cashin+add).
Ikki to'lov: PAY1=200 000 → balans −175 000; PAY2=175 000 → balans 0.
"""
import allure
from qase.pytest import qase
from utils.step import step
import pytest

from config.servers import resolve_server

from .data import names, ENV, EXPECTED
from .pages.client_payment_page import ClientPaymentPage

pytestmark = [pytest.mark.e2e]


@qase.id(17)  # TC-E2E-16
@allure.title("TC-E2E-16: Mijozdan to'lov — PAY1 200 000 → −175 000; PAY2 175 000 → 0")
def test_16_payment(e2e_page, e2e, rdate):
    server = resolve_server("xtrade")
    client = e2e.get("sale_order_client") or e2e.get("natural_person")
    assert client, "TC-12..15 ishlamagan — e2e['sale_order_client'] yo'q"
    debt = e2e.get("client_debt", EXPECTED["order_sum"] - EXPECTED["return_sum"])  # 375 000
    pay1 = EXPECTED["pay1"]       # 200 000
    pay2 = EXPECTED["pay2"]       # 175 000
    n = names(rdate)
    pp = ClientPaymentPage(e2e_page, server["base_url"])

    with step(f"1 - To'lovдан oldin mijoz balansi −{debt}"):
        bal0 = pp.read_client_balance(client)
        assert bal0 == f"-{debt}", f"Boshlang'ich balans kutilgan -{debt}, lekin '{bal0}'"

    with step(f"2 - PAY1 «{n['pay1']}» = {pay1}, «Провести взаимозачёт» → Провести → Да"):
        before1 = pp.create_payment(n["pay1"], pay1, client, kassa="Основная касса")
        assert before1 == f"-{debt}", f"PAY1 oldidan balans -{debt} bo'lishi kerak, lekin '{before1}'"

    with step(f"3 - PAY1'dан keyin balans −{debt - pay1}"):
        bal1 = pp.read_client_balance(client)
        assert bal1 == f"-{debt - pay1}", f"PAY1'dан keyin balans kutilgan -{debt - pay1}, lekin '{bal1}'"

    with step(f"4 - PAY2 «{n['pay2']}» = {pay2} → Провести → Да"):
        pp.create_payment(n["pay2"], pay2, client, kassa="Основная касса")

    with step("5 - PAY2'dан keyin balans 0 (qarz yopildi)"):
        bal2 = pp.read_client_balance(client)
        assert bal2 in ("0", "-0", ""), f"PAY2'dан keyin balans 0 bo'lishi kerak, lekin '{bal2}'"

    e2e["pay1"] = pay1
    e2e["pay2"] = pay2
    e2e["client_debt"] = 0
    print(f"[E2E-16] Mijoz to'lovlari: PAY1 {pay1} + PAY2 {pay2} = {pay1 + pay2}; "
          f"balans −{debt} → {bal1} → {bal2} (qarz yopildi)")
