"""TC-E2E-04 — Физическое лицо (mijoz): barcha maydonlar + 6(+1) tab (GPS/Файлы mustasno).
docs/e2e/E2E_test_cases.md ga qarang. Oldindan: TC-E2E-03 (Юр.лицо — «Юридическое лицо» ulanishi uchun).
"""
import allure
from qase.pytest import qase
from utils.step import step
import pytest

from config.servers import resolve_server

from .data import natural_full
from .pages.natural_person_page import NaturalPersonPage

pytestmark = [pytest.mark.e2e]


@qase.id(5)  # TC-E2E-04
@allure.title("TC-E2E-04: Физическое лицо — maydonlar, tablar, dialoglar, saqlash, Просмотр, mijoz")
def test_04_natural_person(e2e_page, e2e, rdate):
    server = resolve_server("xtrade")
    d = natural_full(rdate, legal_person=e2e.get("legal_person", ""))
    np = NaturalPersonPage(e2e_page, server["base_url"])
    ident = d["first_name"]   # «Mijoz<DDMM>» — unikal, ro'yxat/view qidiruvi uchun

    with step("1 - Физ.лицо ro'yxati → «Создать»; UMUMIY 1 (bo'sh save bloklanadi)"):
        np.open_list()
        np.open_create()
        np.check_empty_save_blocked()

    with step("2 - Asosiy maydonlar (Пол, Имя autocomplete, Регион, Юр.лицо, checkboxlar)"):
        np.fill_main(d)

    with step("3a - Характеристики (Группа*/Категория* majburiy)"):
        np.fill_characteristics()

    with step("3b - Расчетный счет / Договор (dialoglar)"):
        np.add_bank_account(d)
        np.add_contract(d)

    with step("3c - Адреса доставки (Клиент tufayli) + Примечание + График доставки"):
        np.add_delivery_address(d)
        np.fill_note(d)
        np.fill_delivery_schedule()

    with step("4 - «Сохранить» (confirm «Да»)"):
        np.save()

    with step("5 - Ro'yxatda «Просмотр»: grid qatorida kalit qiymatlar (Код, Пол)"):
        np.verify_in_list(ident, code=d["code"], gender="Мужской")

    with step("6 - Справочники → Клиенты: mijoz avtomatik yaratilgan"):
        np.expect_client_created(ident)

    e2e["natural_person"] = d["first_name"]
    e2e["natural_code"] = d["code"]
    print(f"[E2E-04] Физ.лицо (mijoz) yaratildi: {d['surname']} {d['first_name']} {d['middle']}")
