"""TC-E2E-05 — Поставщик (ta'minotchi): Изменить (НДС/Акциз) + ТМЦ ga ta'minotchini bog'lash (MAJBURIY).
docs/e2e/E2E_test_cases.md ga qarang. Oldindan: TC-E2E-01 (ТМЦ), TC-E2E-03 (ta'minotchi avto-yaratildi).
"""
import allure
from qase.pytest import qase
from utils.step import step
import pytest

from config.servers import resolve_server

from .pages.supplier_page import SupplierPage

pytestmark = [pytest.mark.e2e]


@qase.id(6)  # TC-E2E-05
@allure.title("TC-E2E-05: Поставщик — Изменить (НДС/Акциз=Нет) + ТМЦ «Поставщики» ga bog'lash")
def test_05_supplier(e2e_page, e2e):
    server = resolve_server("xtrade")
    supplier = e2e.get("legal_person")
    tmc = e2e.get("tmc_name")
    assert supplier, "TC-03 ishlamagan — e2e['legal_person'] yo'q"
    assert tmc, "TC-01 ishlamagan — e2e['tmc_name'] yo'q"
    sp = SupplierPage(e2e_page, server["base_url"])

    with step(f"1-4 - «{supplier}» ta'minotchi Изменить: НДС/Акциз yoqib-o'chirish + Умный поиск → Сохранить"):
        sp.edit_toggles_save(supplier)

    with step("5 - Tekshiruv: НДС = Нет, Акциз = Нет"):
        sp.expect_vat_off(supplier)

    with step(f"6 (MAJBURIY) - ТМЦ «{tmc}» → Изменить → «Поставщики» ga «{supplier}» qo'shish"):
        sp.link_supplier_to_tmc(tmc, supplier)
        sp.expect_tmc_has_supplier(tmc, supplier)

    e2e["supplier"] = supplier
    print(f"[E2E-05] Ta'minotchi «{supplier}» ТМЦ «{tmc}» ga bog'landi (НДС/Акциз = Нет)")
