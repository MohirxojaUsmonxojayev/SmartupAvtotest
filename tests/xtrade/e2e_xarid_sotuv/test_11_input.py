"""TC-E2E-11 — Поступление ТМЦ на склад (zakupkadan). docs/e2e/E2E_test_cases.md ga qarang.
Oldindan: TC-06 (Склад), TC-10 (Закупка, Завершено). Natija: ombor qoldig'i 100.
"""
import allure
import pytest

from config.servers import resolve_server

from .data import names, EXPECTED
from .pages.input_page import InputPage

pytestmark = [pytest.mark.e2e]


@allure.title("TC-E2E-11: Поступление ТМЦ на склад — zakupkadan, Кол-во 100, Завершено")
def test_11_input(e2e_page, e2e, rdate):
    server = resolve_server("xtrade")
    warehouse = e2e.get("warehouse")
    invoice = e2e.get("invoice")
    assert warehouse, "TC-06 ishlamagan — e2e['warehouse'] yo'q"
    assert invoice, "TC-10 ishlamagan — e2e['invoice'] yo'q"
    number = names(rdate)["input_doc"]       # QA-E2E-PS-<DDMM>
    qty = EXPECTED["stock_after_input"]       # 100
    inp = InputPage(e2e_page, server["base_url"])

    with allure.step(f"1 - Поступления → «Создать»; Step1: Номер {number}, Склад {warehouse}, Валюта Узбекский сум → Далее"):
        inp.open_list()
        inp.open_create()
        inp.step1_main(number, warehouse)

    with allure.step(f"2 - Step2 «Закупки»: {invoice} tanlash, Кол-во {qty} → Далее"):
        inp.step2_from_purchase(invoice, qty)

    with allure.step("3 - Step3: Завершить (Новое holatda saqlanadi)"):
        inp.step3_finish("Завершено")

    with allure.step("4 - Ro'yxatда «Статус» → Завершено (qoldiq posted)"):
        inp.set_status_completed(number)
        inp.expect_in_list(number, "Завершено")

    e2e["input_doc"] = number
    print(f"[E2E-11] Поступление: {number} — {warehouse}, Кол-во {qty}, Завершено")
