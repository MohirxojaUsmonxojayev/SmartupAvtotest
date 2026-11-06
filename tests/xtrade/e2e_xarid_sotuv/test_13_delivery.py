"""TC-E2E-13 — Buyurtmani yetkazib berish: Новый → В обработке → Отгружен → Доставлен.
docs/e2e/E2E_test_cases.md (TC-E2E-13) ga qarang.
Oldindan: TC-12 (sotuv buyurtmasi «Новый» yaratilgan — e2e['sale_order_id']).
DIQQAT: bu a2 forma (spec «eski UI» deydi, LEKIN hamma a2 — status Статус-ustun dropdown orqali).
"""
from qase.pytest import qase
from utils.step import step, title
import pytest

from config.servers import resolve_server

from .pages.sale_order_page import SaleOrderPage

pytestmark = [pytest.mark.e2e]


@qase.id(14)  # TC-E2E-13
@title("TC-E2E-13: Yetkazish — Новый → В обработке → Отгружен → Доставлен")
def test_13_delivery(e2e_page, e2e):
    server = resolve_server("xtrade")
    client = e2e.get("sale_order_client") or e2e.get("natural_person")
    assert client, "TC-12 ishlamagan — e2e['sale_order_client']/['natural_person'] yo'q"
    so = SaleOrderPage(e2e_page, server["base_url"])

    # Buyurtma ИД (TC-12 saqlagan; bo'lmasa — klientning eng yangi buyurtmasidan olamiz)
    order_id = e2e.get("sale_order_id") or so.capture_id(client)
    assert order_id, "Sotuv buyurtmasi ИД topilmadi (TC-12 tekshiring)"

    with step(f"1 - Buyurtma {order_id}: Статус → «В обработке» → Да"):
        so.change_status(client, order_id, "В обработке")
        so.expect_status(client, order_id, "В обработке")

    with step(f"2 - Buyurtma {order_id}: Статус → «Отгружен» → Да"):
        so.change_status(client, order_id, "Отгружен")
        so.expect_status(client, order_id, "Отгружен")

    with step(f"3 - Buyurtma {order_id}: Статус → «Доставлен» → Да"):
        so.change_status(client, order_id, "Доставлен")
        so.expect_status(client, order_id, "Доставлен")

    e2e["sale_order_status"] = "Доставлен"
    print(f"[E2E-13] Buyurtma {order_id} yetkazildi: Новый → В обработке → Отгружен → Доставлен")
