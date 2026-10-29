"""
XTRADE — login testi.

Server: yangi Angular UI (/a2) — https://app3.greenwhite.uz/xtrade/a2/auth/login

Ssenariy (spetsifikatsiya bo'yicha):
    1. Login page'da login qilish (default: moxir@novatrade / 1)
    2. Active-session sahifasini tekshirish — ochilgan bo'lsa BITTA sessiyani kill qilish
    3. Dashboard ochilganini tekshirish
    4. Filial tanlash (default: "NovaTrade - Toshkent Filiali") — yoki admin filialda qolish
    5. Logout qilish

Eslatma: active-session (concurrent_session_list) dashboard'dan OLDIN chiqadi,
shuning uchun u dashboard tekshiruvidan oldin hal qilinadi.
"""
import allure
from playwright.sync_api import Page

from flows.auth_flow import login, kill_active_session, dashboard_opened, switch_filial, logout

pytestmark = [
    allure.epic("Xtrade"),
    allure.feature("Auth"),
    allure.story("Login"),
]


@allure.title("Xtrade: login → active session → dashboard → filial → logout")
def test_login(page: Page, server: dict):
    with allure.step("1 - Login (default: moxir@novatrade / 1)"):
        email, _ = login(page, server)
        print(f"[LOGIN] {email} @ {server['base_url']}")

    with allure.step("2 - Active session oynasini tekshirish, bo'lsa bitta sessiyani kill qilish"):
        killed = kill_active_session(page, server)
        print("[SESSION]", "chiqdi — bitta sessiya kill qilindi" if killed else "chiqmadi")

    with allure.step("3 - Dashboard ochilganini tekshirish"):
        dashboard_opened(page, server)

    with allure.step(f"4 - Filial tanlash: {server['default_filial']}"):
        switch_filial(page, server, server["default_filial"])

    with allure.step("5 - Logout"):
        logout(page, server)
