"""TC-E2E-15 — Buyurtmani arxivga o'tkazish (+ mijoz qarzi arxivда «Задолженность»ga o'tadi).
docs/e2e/E2E_test_cases.md (TC-E2E-15) ga qarang.
Oldindan: TC-14 (buyurtma «Доставлен», qisman qaytarilган — Сумма 375 000, e2e['sale_order_id']).
DIQQAT: a2 — status «Архив» Статус-ustun dropdown orqали (TC-13 mexanizmi). Архив заказов =
/a2/trade/tdeal/order/order_history_list. Дата отгрузки bugun bo'lgani uchun «A02-16-049 Дата
доставки больше системного» xatosi chiqmasligi kerak.
"""
import allure
import pytest

from config.servers import resolve_server

from .data import EXPECTED
from .pages.sale_order_page import SaleOrderPage

pytestmark = [pytest.mark.e2e]


@allure.title("TC-E2E-15: Arxivga o'tkazish — Статус «Архив»; Архив заказов'да Сумма 375 000")
def test_15_archive(e2e_page, e2e):
    server = resolve_server("xtrade")
    client = e2e.get("sale_order_client") or e2e.get("natural_person")
    order_id = e2e.get("sale_order_id")
    assert order_id, "TC-12..14 ishlamagan — e2e['sale_order_id'] yo'q"
    archived_sum = e2e.get("order_sum_after_return", EXPECTED["order_sum"] - EXPECTED["return_sum"])  # 375 000
    so = SaleOrderPage(e2e_page, server["base_url"])

    with allure.step(f"1 - Buyurtma {order_id}: Статус → «Архив» → Да (asosiy ro'yxatdan chiqadi)"):
        so.change_status(client, order_id, "Архив")
        so.expect_not_in_main_list(client, order_id)

    with allure.step(f"2 - «Архив заказов» (order_history_list) da buyurtma {order_id}, Сумма {archived_sum}"):
        so.expect_in_archive(client, order_id, archived_sum)

    e2e["sale_order_status"] = "Архив"
    e2e["client_debt"] = archived_sum
    print(f"[E2E-15] Buyurtma {order_id} arxivlandi — Архив заказов'да Сумма {archived_sum} "
          f"(mijoz qarzi «Задолженность»ga o'tdi)")
