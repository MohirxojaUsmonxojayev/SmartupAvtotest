"""TC-E2E-01 — ТМЦ yaratish (a2, chuqurlashtirilgan). docs/e2e/E2E_test_cases.md ga qarang."""
import allure
import pytest

from config.servers import resolve_server

from .data import tmc_full
from .pages.tmc_page import TmcPage

pytestmark = [pytest.mark.e2e]


@allure.title("TC-E2E-01: ТМЦ yaratish — maydonlar, tablar, validatsiya, Просмотр, Изменить")
def test_01_tmc(e2e_page, e2e, rdate):
    server = resolve_server("xtrade")
    d = tmc_full(rdate)
    tmc = TmcPage(e2e_page, server["base_url"])

    with allure.step("1 - ТМЦ ro'yxati → «Создать» (create forma ochiladi)"):
        tmc.open_list()
        tmc.open_create()

    with allure.step("2 - UMUMIY 1: bo'sh forma «Сохранить» → saqlanmaydi"):
        tmc.check_empty_save_blocked()

    with allure.step("3 - «Кол-во в кейсе (2 уровень)» 1-daraja tanlanmasdan nofaol"):
        tmc.check_case2_disabled_before_case1()

    with allure.step("4 - Barcha asosiy maydonlarni to'ldirish + rasm"):
        tmc.fill_main(d)
        tmc.add_image()

    with allure.step("5 - 6 ta tabni ochib ko'rish + Характеристики to'ldirish"):
        tmc.open_tabs_smoke()
        tmc.fill_characteristics()

    with allure.step("5b - 2-shtrix-kod qo'shish (dialog)"):
        tmc.add_second_barcode(d["barcode2"])
        # TODO (fayl biriktirish): Файлы «Добавить» dialogi minimal PDF bilan yopilmaydi
        #   (dialog error holatida qoladi) — haqiqiy/kattaroq PDF yoki dialog preview bilan
        #   jonli aniqlanadi. tmc.add_file() metodi tayyor, yoqilgach ishlaydi.

    with allure.step("6 - «Сохранить»"):
        tmc.save()

    with allure.step("7 - Ro'yxatda nom bo'yicha topish"):
        tmc.find_in_list(d["name"])

    with allure.step("8 - «Просмотр» ochish"):
        tmc.open_view(d["name"])

    with allure.step("9 - «Изменить» → Порядковый номер 998"):
        tmc.edit_order_no(d["name"], d["order_no_edit"])

    # TODO (status toggle): «Неактивный» qilingach qator FAOL-ro'yxatdan DARHOL filtrlanadi
    #   (qayta-qidiruvsiz ham) — qayta «Активный» uchun list'da "nofaollarни ko'rsat" filtri kerak.
    #   a2 filtr mexanizmini aniqlagach `tmc.toggle_status_in_list()` yoqiladi (metod tayyor).

    e2e["tmc_name"] = d["name"]
    e2e["tmc_code"] = d["code"]
    print(f"[E2E-01] ТМЦ yaratildi: {d['name']}")
