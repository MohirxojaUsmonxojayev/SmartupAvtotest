"""TC-E2E-14 — Buyurtmaning bir qismini qaytarish («Отказ»/«Возврат»).
docs/e2e/E2E_test_cases.md (TC-E2E-14) ga qarang.
Oldindan: TC-13 (buyurtma «Доставлен» — e2e['sale_order_id']).
DIQQAT: a2 — qaytarish formasi /a2/anor/mdeal/order/return?deal_id=<ИД> (URL orqali; «Отказ»
qator-amali a2 UI'да to'g'ridан ko'rinmaydi). Foydalanuvchi: TC-14 «Отказ» EMAS, aslida «Возврат».
"""
import allure
from qase.pytest import qase
from utils.step import step
import pytest

from config.servers import resolve_server

from .data import EXPECTED
from .pages.sale_order_page import SaleOrderPage

pytestmark = [pytest.mark.e2e]


@qase.id(15)  # TC-E2E-14
@allure.title("TC-E2E-14: Qisman qaytarish — Возврат 5, Причина «Обмен» → Сумма заказа 375 000")
def test_14_return(e2e_page, e2e):
    server = resolve_server("xtrade")
    client = e2e.get("sale_order_client") or e2e.get("natural_person")
    order_id = e2e.get("sale_order_id")
    assert order_id, "TC-12/13 ishlamagan — e2e['sale_order_id'] yo'q"
    ret_qty = EXPECTED["return_qty"]                              # 5
    ret_sum = EXPECTED["return_sum"]                             # 75 000
    sum_after_expected = EXPECTED["order_sum"] - ret_sum          # 450 000 − 75 000 = 375 000
    so = SaleOrderPage(e2e_page, server["base_url"])

    with step(f"1 - Buyurtma {order_id} «Доставлен» ekanini tekshirish"):
        so.expect_status(client, order_id, "Доставлен")

    with step(f"2-4 - Возврат формаси: Возврат={ret_qty}, Причина «Обмен» → Сохранить → Да; "
                     f"Сумма заказа {EXPECTED['order_sum']} → {sum_after_expected}"):
        sum_after = so.partial_return(order_id, ret_qty, reason="Обмен")
        assert sum_after == str(sum_after_expected), \
            f"Qaytarishдан keyин Сумма заказа kutilgan {sum_after_expected}, lekin '{sum_after}' " \
            f"(qaytarilган summa {ret_sum} bo'lishi kerak)"

    with step(f"5 - Saqlanganini mustaqil tasdiqlash: Сумма заказа = {sum_after_expected} (qayta yuklash)"):
        so.expect_return_persisted(order_id, sum_after_expected)

    e2e["return_qty"] = ret_qty
    e2e["return_sum"] = ret_sum
    e2e["order_sum_after_return"] = sum_after_expected
    print(f"[E2E-14] Qisman qaytarish: buyurtma {order_id} — Возврат {ret_qty} ({ret_sum}), "
          f"Сумма заказа → {sum_after}")
