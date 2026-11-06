"""TC-E2E-07 — Клиент (TC-04 da avto-yaratilgan): Изменить + Просмотр. docs/e2e/E2E_test_cases.md ga qarang."""
import allure
from qase.pytest import qase
from utils.step import step
import pytest

from config.servers import resolve_server

from .pages.client_page import ClientPage

pytestmark = [pytest.mark.e2e]


@qase.id(8)  # TC-E2E-07
@allure.title("TC-E2E-07: Клиент — avto-yaratilgan mijoz Изменить + Просмотр (tablar/qiymatlar)")
def test_07_client(e2e_page, e2e):
    server = resolve_server("xtrade")
    mijoz = e2e.get("natural_person")
    assert mijoz, "TC-04 ishlamagan — e2e['natural_person'] yo'q"
    cp = ClientPage(e2e_page, server["base_url"])

    with step(f"1-3 - «{mijoz}» client «Изменить»: Тип клиента/Название to'la → Сохранить"):
        cp.edit_and_save(mijoz)

    with step("4 - «Просмотреть»: Основная/Задачи/История tablar + nom"):
        cp.view_and_verify(mijoz)

    e2e["client"] = mijoz
    print(f"[E2E-07] Клиент (mijoz) tasdiqlandi: {mijoz}")
