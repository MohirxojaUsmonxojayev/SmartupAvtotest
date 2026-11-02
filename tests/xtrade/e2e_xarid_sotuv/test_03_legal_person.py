"""TC-E2E-03 — Юридическое лицо (ta'minotchi): barcha maydonlar + 8 tab (GPS/Файлы mustasno).
docs/e2e/E2E_test_cases.md ga qarang. Oldindan: TC-E2E-01.
"""
import allure
import pytest

from config.servers import resolve_server

from .data import legal_full
from .pages.legal_person_page import LegalPersonPage

pytestmark = [pytest.mark.e2e]


@allure.title("TC-E2E-03: Юридическое лицо — maydonlar, 8 tab, dialoglar, saqlash, Просмотр, ta'minotchi")
def test_03_legal_person(e2e_page, e2e, rdate):
    server = resolve_server("xtrade")
    d = legal_full(rdate)
    lp = LegalPersonPage(e2e_page, server["base_url"])

    with allure.step("1 - Юр.лицо ro'yxati → «Создать»; UMUMIY 1 (bo'sh save bloklanadi)"):
        lp.open_list()
        lp.open_create()
        lp.check_empty_save_blocked()

    with allure.step("2 - Asosiy maydonlar + Регион + checkboxlar (поставщик=Да, клиент toggle)"):
        lp.fill_main(d)

    with allure.step("3a - Характеристики (qa xyu* majburiy)"):
        lp.fill_characteristics()

    with allure.step("3b - Расчетный счет (dialog)"):
        lp.add_bank_account(d)

    with allure.step("3c - Контактные лица (dialog)"):
        lp.add_contact(d)

    with allure.step("3d - Договор (dialog)"):
        lp.add_contract(d)

    with allure.step("3e - Примечание / Руководящие должности / График доставки"):
        lp.fill_note(d)
        lp.fill_leadership(d)
        lp.fill_delivery()

    with allure.step("4 - «Сохранить» (confirm «Да»)"):
        lp.save()

    with allure.step("5 - Ro'yxatda qidirib «Просмотр»"):
        lp.open_view(d["full_name"])

    with allure.step("6 - Склад → Поставщики: ta'minotchi avtomatik yaratilgan"):
        lp.expect_supplier_created(d["full_name"])

    e2e["legal_person"] = d["full_name"]
    e2e["legal_code"] = d["code"]
    print(f"[E2E-03] Юр.лицо (ta'minotchi) yaratildi: {d['full_name']}")
