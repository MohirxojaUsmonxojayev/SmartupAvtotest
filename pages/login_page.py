import re

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Smartup login sahifasi — ikkala server ham yangi Angular UI (/a2/auth/login):
      - online : https://smartup.online/a2/auth/login
      - xtrade : https://app3.greenwhite.uz/xtrade/a2/auth/login

    Barqaror selektorlar: input#login, input#password; submit "Войти" tugmasi.
    (Angular UI'da `smt-input#login` wrapper ham bor, shuning uchun aniq `input`.)
    """

    def __init__(self, page, login_url: str):
        super().__init__(page)
        self.login_url = login_url

    # ------------------------------------------------------------------------------------------------------------------
    def open(self) -> None:
        # "commit" — navigatsiya boshlangach darhol davom etadi (SPA redirect "load"/
        # "domcontentloaded" ni ishonchli chiqarmaydi). Keyin input#login kutiladi.
        self.page.goto(self.login_url, wait_until="commit", timeout=60_000)

    def element_visible(self) -> None:
        """Login formasi yuklanganini tekshiradi — input#login ikkala UI'da ham bor."""
        self.wait_for(self.locator("input#login"))

    def fill_form(self, email: str, password: str) -> None:
        self.locator("input#login").fill(email)
        self.locator("input#password").fill(password)

    def submit(self) -> None:
        # Asosiy "Войти"/"ВОЙТИ" tugmasi (uzun "Войти через ..." tugmalaridan farqli).
        # Katta/kichik harf farqi (xtrade'da CSS uppercase) uchun case-insensitive regex.
        btn = self.page.get_by_role("button", name=re.compile(r"^\s*войти\s*$", re.I))
        if btn.count() > 0:
            btn.first.click()
        else:
            # Fallback: parol maydonida Enter — forma submit bo'ladi.
            self.locator("input#password").press("Enter")
        try:
            self.page.wait_for_load_state("networkidle", timeout=60_000)
        except PlaywrightTimeoutError:
            # SPA doimiy so'rov yuboradi — networkidle kelmasligi mumkin. Keyingi
            # qadamlar (active-session / dashboard) aniq elementni tekshiradi.
            pass
