"""TC-E2E-12 — Заказ (sotuv buyurtmasi, a2 3-qadamli wizard). docs/e2e/E2E_test_cases.md ga qarang.
Oldindan:
  - TC-01 ТМЦ, TC-02 narx («Цена с НДС и акцизом» to'ldirilган — SOTUVGA TAYYORLIK SHARTI),
  - TC-04 mijoz (Рабочая зона = Room - Yashnobod), TC-06 ombor (zona'ga bog'langan),
  - TC-08..11 xarid→kirim (omborда stok > 0).
DIQQAT: bu a2 forma (ESKI UI EMAS — «Старый интерфейс» test uchun, tegilmaydi).
"""
import allure
from qase.pytest import qase
import pytest

from config.servers import resolve_server

from .data import ENV, EXPECTED
from .pages.sale_order_page import SaleOrderPage

pytestmark = [pytest.mark.e2e]


@qase.id(13)  # TC-E2E-12
@allure.title("TC-E2E-12: Заказ (sotuv) — 3 qadam; Подбор Кол-во 30 → ИТОГО 450 000, Статус Новый")
def test_12_sale_order(e2e_page, e2e):
    server = resolve_server("xtrade")
    tmc = e2e.get("tmc_name")
    client = e2e.get("natural_person")
    sklad = e2e.get("warehouse")
    assert tmc, "TC-01 ishlamagan — e2e['tmc_name'] yo'q"
    assert client, "TC-04 ishlamagan — e2e['natural_person'] yo'q"
    assert sklad, "TC-06 ishlamagan — e2e['warehouse'] yo'q"
    qty = EXPECTED["order_qty"]            # 30
    total = EXPECTED["order_sum"]          # 450 000
    so = SaleOrderPage(e2e_page, server["base_url"])

    with allure.step(f"1 - Заказы → «Создать»; Step1 «Основное»: зона «{ENV['room']}», Клиент «{client}» → Далее"):
        so.open_list()
        so.open_create()
        so.step1_main(ENV["room"], "Main Manager", client)

    with allure.step(f"2 - Step2 «ТМЦ»: Подбор (Склад «{sklad}», Тип цены «{ENV['price_type_sell']}»), "
                     f"{tmc} × {qty} → ИТОГО {total}"):
        itogo = so.step2_podbor(sklad, ENV["price_type_sell"], tmc, qty)
        assert itogo == str(total), f"ИТОГО kutilgan {total}, lekin '{itogo}'"

    with allure.step(f"3 - Step3 «Завершение»: Тип оплаты «{ENV['payment_type']}», Статус Новый → Сохранить"):
        so.step3_finish(ENV["payment_type"], status="Новый")

    with allure.step("4 - Ro'yxatда buyurtma mavjud + Статус «Новый» + ИД olish"):
        so.expect_in_list(client)
        status = so.latest_status(client)
        assert status == "Новый", f"Buyurtma holati kutilgan «Новый», lekin «{status}»"
        order_id = so.capture_id(client)

    # Zanjir identifikatori: matnli номер yo'q → «ИД заказа» (TC-13 status-transition uchun) + klient
    e2e["sale_order_id"] = order_id
    e2e["sale_order_client"] = client
    e2e["sale_order_status"] = status
    e2e["order_qty"] = qty
    e2e["order_sum"] = total
    print(f"[E2E-12] Sotuv buyurtmasi yaratildi — ИД {order_id}, {client}, {tmc} × {qty}, "
          f"ИТОГО {total}, Статус {status}")
