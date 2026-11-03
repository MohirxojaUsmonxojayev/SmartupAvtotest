"""TC-E2E-08 — Запрос на закупку (xujjat): Подбор ТМЦ 100, Новый → Принято, Просмотр.
docs/e2e/E2E_test_cases.md ga qarang. Oldindan: TC-E2E-01 (ТМЦ).
"""
import allure
import pytest

from config.servers import resolve_server

from .data import names, EXPECTED
from .pages.purchase_request_page import PurchaseRequestPage

pytestmark = [pytest.mark.e2e]


@allure.title("TC-E2E-08: Запрос на закупку — Подбор ТМЦ 100, Новый→Принято, Просмотр")
def test_08_purchase_request(e2e_page, e2e, rdate):
    server = resolve_server("xtrade")
    tmc = e2e.get("tmc_name")
    assert tmc, "TC-01 ishlamagan — e2e['tmc_name'] yo'q"
    number = names(rdate)["purchase_req"]        # QA-E2E-ZR-<DDMM>
    qty = EXPECTED["req_qty"]                     # 100
    pr = PurchaseRequestPage(e2e_page, server["base_url"])

    with allure.step("1 - Запрос ro'yxati → «Создать»; UMUMIY 1 (ТМЦ siz saqlanmaydi)"):
        pr.open_list()
        pr.open_create()
        pr.check_empty_save_blocked()

    with allure.step(f"2 - Header: Номер {number}, Дата bugun, Крайний срок +7, Примечание"):
        pr.fill_header(number)

    with allure.step(f"3-4 - «Подбор» → {tmc}, Кол-во {qty}"):
        pr.add_tmc(tmc, qty)

    with allure.step("5 - «Импорт» oynasi smoke"):
        pr.import_smoke()

    with allure.step("6a - «Сохранить» (Статус Новый)"):
        pr.save()
        pr.expect_in_list(number)

    with allure.step("6b - «Статус» → Принято"):
        pr.set_status_accepted(number)
        pr.expect_in_list(number, status_text="Принят")

    with allure.step(f"7 - «Просмотр»: {tmc} {qty} шт"):
        pr.open_view(number, tmc, qty)

    e2e["purchase_req"] = number
    print(f"[E2E-08] Запрос на закупку: {number} — {tmc} × {qty} (Принято)")
