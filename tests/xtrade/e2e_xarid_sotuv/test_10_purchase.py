"""TC-E2E-10 — Закупка (zakazdan, a2 3-qadamli wizard). docs/e2e/E2E_test_cases.md ga qarang.
Oldindan: TC-09 (Заказ на закупку, ПРИНЯТО).
"""
import allure
import pytest

from config.servers import resolve_server

from .data import names, EXPECTED
from .pages.purchase_page import PurchasePage

pytestmark = [pytest.mark.e2e]


@allure.title("TC-E2E-10: Закупка (zakazdan) — Сумма 1 000 000, Завершено, Провести")
def test_10_purchase(e2e_page, e2e, rdate):
    server = resolve_server("xtrade")
    order = e2e.get("purchase_order")
    supplier = e2e.get("legal_person")
    assert order, "TC-09 ishlamagan — e2e['purchase_order'] yo'q"
    assert supplier, "TC-03 ishlamagan — e2e['legal_person'] yo'q"
    invoice = f"QA-SF-{rdate}"
    total = EXPECTED["purchase_sum"]        # 1 000 000
    pur = PurchasePage(e2e_page, server["base_url"])

    with allure.step(f"1 - Закупки → «Создать»; Step1: «Заказ на закупку» {order}, Номер СФ {invoice} → Далее"):
        pur.open_list()
        pur.open_create()
        pur.step1_from_order(order, invoice)

    with allure.step(f"2 - Step2: ТМЦ Сумма = {total}"):
        pur.step2_expect_sum(total)

    with allure.step("3 - Step3: Статус Завершено → «Провести»"):
        pur.step3_finish("Завершено")

    with allure.step(f"4 - Ro'yxatda: {supplier}, {total}, Завершено"):
        pur.expect_in_list(supplier, total, "Завершено")

    e2e["purchase"] = order
    e2e["invoice"] = invoice
    print(f"[E2E-10] Закупка: zakaz {order} — Сумма {total}, Завершено (СФ {invoice})")
