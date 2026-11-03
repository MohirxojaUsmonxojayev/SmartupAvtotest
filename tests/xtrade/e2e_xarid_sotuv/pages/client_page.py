"""
Клиент (mijoz) — a2 page object (TC-E2E-07).
Ro'yxat: /a2/anor/mrf/client_list. TC-04 da «☑ Клиент» tufayli AVTO-yaratiladi → «Просмотр»/«Изменить» bilan tekshiriladi.

Jonli tasdiqlangan (mohir@xan, 2026-11-03):
  Qator amallari: Просмотреть, Изменить, Неактивный, Удалить.
  Изменить form (title «Клиент (изменение)»): Тип клиента (select), Название (select) — Сохранить/Закрыть.
  Просмотр (title «Клиент (просмотр)») tablar: Основная информация, Задачи, История изменений;
    maydonlar: Название, Тип клиента, Статус, Client ID, Создал/Изменил, sanalar.
"""
from playwright.sync_api import expect

from utils.base_page import BasePage


class ClientPage:
    LIST_PATH = "/a2/anor/mrf/client_list"

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.b = BasePage(page)

    def open_list(self):
        self.page.goto(self.base_url + self.LIST_PATH, wait_until="commit", timeout=60_000)
        self.page.get_by_role("button", name="Создать", exact=True).first.wait_for(state="visible", timeout=30_000)
        self.page.wait_for_timeout(800)

    def _select_row(self, name: str):
        self.open_list()
        self.b.search_list(name)
        self.page.wait_for_timeout(1_500)
        self.b.grid_row(name).click()
        self.page.wait_for_timeout(700)

    def _confirm_yes_if_any(self):
        try:
            dlg = self.page.locator("[role=dialog], .cdk-dialog-container").last
            btn = dlg.get_by_role("button", name="Да", exact=False).first
            if btn.count() > 0 and btn.is_visible():
                btn.click()
                self.page.wait_for_timeout(600)
        except Exception:
            pass

    def edit_and_save(self, name: str):
        """TC-07/2-3: «Изменить» ochib Тип клиента/Название to'ldirilganini tekshiradi va saqlaydi."""
        self._select_row(name)
        self.b.click_button("Изменить", exact=False)
        self.b.expect_form_open("изменени")
        self.page.wait_for_timeout(1_500)
        # Название (mijoz) bo'sh emas — avto-yaratilgan client
        expect(self.b.control("Название").locator("input").first).not_to_have_value("")
        expect(self.b.control("Тип клиента").locator("input").first).not_to_have_value("")
        self.b.save()
        self.page.wait_for_timeout(600)
        self._confirm_yes_if_any()
        self.page.wait_for_timeout(2_000)

    def view_and_verify(self, name: str):
        """TC-07/4: «Просмотреть» → tablar (Основная/Задачи/История) + Название ko'rinadi."""
        self._select_row(name)
        self.b.click_button("Просмотреть", exact=False)
        self.b.expect_form_open("просмотр")
        self.page.wait_for_timeout(1_500)
        for tab in ["Основная информация", "Задачи", "История изменений"]:
            expect(self.page.locator("main").get_by_text(tab, exact=False).first).to_be_visible(timeout=10_000)
        assert self.page.get_by_text(name, exact=False).first.is_visible() \
            or "client_view" in self.page.url, f"Просмотр'da nom ko'rinmadi (URL={self.page.url})"
