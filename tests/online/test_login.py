"""
SMARTUP ONLINE — login testi.

Server: yangi Angular UI (/a2) — https://smartup.online/a2/auth/login

Ssenariy (spetsifikatsiya bo'yicha):
    1. Login page'da login qilish (default: alibe@test / 111111)
    2. Active-session sahifasini tekshirish — ochilgan bo'lsa BITTA sessiyani kill qilish
    3. Dashboard ochilganini tekshirish
    4. Filial tanlash (default: "Manual Test company") — yoki admin filialda qolish
    5. Logout qilish

Eslatma: active-session (concurrent_session_list) dashboard'dan OLDIN chiqadi,
shuning uchun u dashboard tekshiruvidan oldin hal qilinadi.
"""
import allure
from playwright.sync_api import Page

from flows.auth_flow import login, kill_active_session, dashboard_opened, switch_filial, logout

pytestmark = [
    allure.epic("Smartup Online"),
    allure.feature("Auth"),
    allure.story("Login"),
]


@allure.title("Online: login → active session → dashboard → filial → logout")
def test_login(page: Page, server: dict):
    with allure.step("1 - Login (default: alibe@test / 111111)"):
        email, _ = login(page, server)
        print(f"[LOGIN] {email} @ {server['base_url']}")

    with allure.step("2 - Active session oynasini/sahifasini tekshirish, bo'lsa bitta sessiyani kill qilish"):
        killed = kill_active_session(page, server)
        print("[SESSION]", "chiqdi — bitta sessiya kill qilindi" if killed else "chiqmadi")

    with allure.step("3 - Dashboard ochilganini tekshirish"):
        dashboard_opened(page, server)

    with allure.step(f"4 - Filial tanlash: {server['default_filial']}"):
        switch_filial(page, server, server["default_filial"])

    with allure.step("5 - Logout"):
        logout(page, server)
