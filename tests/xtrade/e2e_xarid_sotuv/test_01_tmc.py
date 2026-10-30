"""TC-E2E-01 — ТМЦ yaratish (a2). docs/e2e/E2E_test_cases.md ga qarang."""
import allure
import pytest

from config.servers import resolve_server

from .data import names, ENV
from .pages.tmc_page import TmcPage

pytestmark = [pytest.mark.e2e]


@allure.title("TC-E2E-01: ТМЦ yaratish")
def test_01_tmc(e2e_page, e2e, rdate):
    server = resolve_server("xtrade")
    nm = names(rdate)
    tmc = TmcPage(e2e_page, server["base_url"])

    with allure.step("1 - ТМЦ ro'yxatini ochish va «Создать»"):
        tmc.open_list()
        tmc.open_create()

    with allure.step(f"2 - Majburiy maydonlar + Код, saqlash ({nm['tmc']})"):
        tmc.create_minimal(name=nm["tmc"], unit=ENV["unit"], code=nm["tmc_code"])

    with allure.step("3 - Ro'yxatda nom bo'yicha topish"):
        tmc.verify_in_list(nm["tmc"])

    # Holatni keyingi testlarга uzatamiz
    e2e["tmc_name"] = nm["tmc"]
    e2e["tmc_code"] = nm["tmc_code"]
    print(f"[E2E-01] ТМЦ yaratildi: {nm['tmc']}")
