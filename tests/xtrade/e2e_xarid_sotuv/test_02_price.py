"""TC-E2E-02 — ТМЦ ga narx o'rnatish (Установка цен). docs/e2e/E2E_test_cases.md ga qarang.

Oldindan: TC-E2E-01 (ТМЦ yaratilgan). ТМЦ nomi `e2e["tmc_name"]` da (testlar orasida JSON).
"""
import allure
from qase.pytest import qase
import pytest

from config.servers import resolve_server

from .data import ENV
from .pages.price_page import PricePage

pytestmark = [pytest.mark.e2e]


@qase.id(3)  # TC-E2E-02
@allure.title("TC-E2E-02: ТМЦ ga narx — «Sotish sum» 15 000, «Olish sum» 10 000, Просмотр tekshiruvi")
def test_02_price(e2e_page, e2e):
    server = resolve_server("xtrade")
    tmc = e2e.get("tmc_name")
    assert tmc, "TC-01 ishlamagan — e2e['tmc_name'] yo'q (avval test_01_tmc ni ishga tushiring)"
    price = PricePage(e2e_page, server["base_url"])

    with allure.step("1 - Цены ro'yxati + tablar (Цены/Типы оплат/Скидки) xatosiz ochiladi"):
        price.open_list()
        price.open_tabs_smoke()

    with allure.step(f"2-3 - «{ENV['price_type_sell']}» → Установка цен → {tmc} = {ENV['price_sell']}"):
        price.set_price(ENV["price_type_sell"], tmc, ENV["price_sell"])

    with allure.step(f"4 - «{ENV['price_type_buy']}» → Установка цен → {tmc} = {ENV['price_buy']}"):
        price.set_price(ENV["price_type_buy"], tmc, ENV["price_buy"])

    with allure.step(f"5 - Tekshiruv: «{ENV['price_type_sell']}» narxi {ENV['price_sell']}"):
        price.expect_price(ENV["price_type_sell"], tmc, ENV["price_sell"])
        price.expect_price(ENV["price_type_buy"], tmc, ENV["price_buy"])

    e2e["price_sell"] = ENV["price_sell"]
    e2e["price_buy"] = ENV["price_buy"]
    print(f"[E2E-02] Narx o'rnatildi: {tmc} — sotish {ENV['price_sell']}, olish {ENV['price_buy']}")
