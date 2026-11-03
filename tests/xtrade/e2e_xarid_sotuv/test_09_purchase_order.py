"""TC-E2E-09 — Заказ на закупку (a2 4-qadamli wizard, zaprosdan). docs/e2e/E2E_test_cases.md ga qarang.
Oldindan: TC-08 (Запрос на закупку, Принято), TC-03 (ta'minotchi), TC-05 (ТМЦ ga ta'minotchi bog'langan).
DIQQAT: bu a2 forma (ESKI UI EMAS — «Старый интерфейс» test uchun, tegilmaydi).
"""
import allure
import pytest

from config.servers import resolve_server

from .data import names, ENV, EXPECTED
from .pages.purchase_order_page import PurchaseOrderPage

pytestmark = [pytest.mark.e2e]


@allure.title("TC-E2E-09: Заказ на закупку — 4 qadam (zaprosdan, Цена 10000, ИТОГО 1 000 000)")
def test_09_purchase_order(e2e_page, e2e, rdate):
    server = resolve_server("xtrade")
    zr = e2e.get("purchase_req")
    supplier = e2e.get("legal_person")
    assert zr, "TC-08 ishlamagan — e2e['purchase_req'] yo'q"
    assert supplier, "TC-03 ishlamagan — e2e['legal_person'] yo'q"
    number = names(rdate)["purchase_order"]      # QA-E2E-ZZ-<DDMM>
    qty = EXPECTED["req_qty"]                     # 100
    price = ENV["price_buy"]                      # 10 000
    total = EXPECTED["purchase_sum"]              # 1 000 000
    po = PurchaseOrderPage(e2e_page, server["base_url"])

    with allure.step("1 - Заказы на закупку → «Создать»; Step1 «Основное» (Дата поставки +7) → Далее"):
        po.open_list()
        po.open_create()
        po.step1_main()

    with allure.step(f"2 - Step2 «ТМЦ»: «{zr}» tanlash; qatorda Поставщик «{supplier}» + Договор → Далее"):
        po.step2_select_request(zr, supplier)

    with allure.step(f"3 - Step3 «Поставщик»: Цена {price} → ИТОГО {total}"):
        itogo = po.step3_price(price, qty)
        assert itogo == str(total), f"ИТОГО kutilgan {total}, lekin '{itogo}'"

    with allure.step(f"4 - Step4 «Завершение»: Номер {number}, Статус Принято → Завершить"):
        po.step4_finish(number, status="Принято")

    with allure.step("5 - Ro'yxatda ta'minotchi/jami ko'rinadi"):
        po.expect_in_list(supplier, total)

    e2e["purchase_order"] = number
    print(f"[E2E-09] Заказ на закупку: {number} — {supplier}, ИТОГО {total}")
