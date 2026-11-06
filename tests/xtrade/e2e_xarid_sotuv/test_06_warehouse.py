"""TC-E2E-06 — Склад yaratish (barcha maydonlar, Объем hisobi). docs/e2e/E2E_test_cases.md ga qarang."""
import allure
from qase.pytest import qase
import pytest

from config.servers import resolve_server

from .data import warehouse_full
from .pages.warehouse_page import WarehousePage

pytestmark = [pytest.mark.e2e]


@qase.id(7)  # TC-E2E-06
@allure.title("TC-E2E-06: Склад yaratish — maydonlar, Объем 600, saqlash, Просмотр")
def test_06_warehouse(e2e_page, e2e, rdate):
    server = resolve_server("xtrade")
    d = warehouse_full(rdate)
    wh = WarehousePage(e2e_page, server["base_url"])

    with allure.step("1 - Склад ro'yxati → «Создать»; UMUMIY 1 (bo'sh save bloklanadi)"):
        wh.open_list()
        wh.open_create()
        wh.check_empty_save_blocked()

    with allure.step("2 - Barcha maydonlarni to'ldirish; Объем = 3×10×20 = 600"):
        vol = wh.fill_main(d)
        assert vol == "600", f"Объем kutilgan 600, lekin '{vol}'"

    with allure.step("3 - «Сохранить» → ro'yxatda qidirib «Просмотр»"):
        wh.save()
        wh.open_view(d["name"])

    e2e["warehouse"] = d["name"]
    print(f"[E2E-06] Склад yaratildi: {d['name']} (Объем {vol})")
