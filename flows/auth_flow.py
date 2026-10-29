"""
Auth oqimi — login / active-session kill / dashboard / filial switch / logout / relogin.

Ikkala server UI'sini qo'llab-quvvatlaydi (server["ui"] bo'yicha tarmoqlanadi):
  - "legacy" (xtrade) — eski UI: "Активные сеансы" modal, "Trade" heading, .pt-3.px-2 filial, #kt_header logout
  - "new"    (online) — yangi Angular UI: /concurrent_session_list sahifasi,
                        header org-switcher (chevron), avatar menyu -> "Выйти"

Boshqa testlarda `auth` fixture orqali avtomatik login+logout ICHIDA ishlatiladi.
Misol:
    def test_something(auth):
        auth.switch_filial("Boshqa filial")               # istalgancha filial switch
        auth.relogin(email="admin@test", password="greenwhite")  # login/parol o'zgartirish
        ...                                                # test tanasi login va logout ICHIDA
"""
import re
import time

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.login_page import LoginPage


# ======================================================================================================================
# YANGI ONLINE UI selektorlari
# ======================================================================================================================
_ORG_SWITCHER_NEW  = 'header button:has([aria-label="chevron-selector-vertical-icon"])'
_AVATAR_NEW        = 'header button.cdk-menu-trigger.space-x-2'
_CLOSE_SESSION_NEW = 'button[aria-label^="Close session"]'

# Login xatosi matni (noto'g'ri login/parol, bloklangan hisob va h.k.).
# "Пароль" label va "Забыли пароль?" linkiga tegmaslik uchun aniq iboralar.
_AUTH_ERROR_RE = re.compile(
    r"логин или пароль|(неправильн|неверн|ошибочн)\w*\s+(логин|парол)|не найден|заблокир",
    re.I,
)


def _ui(server: dict) -> str:
    return server.get("ui", "legacy")


def _login_error_text(page: Page) -> str | None:
    """Login sahifasida ko'rinadigan xato matnini qaytaradi (bo'lmasa None)."""
    try:
        loc = page.get_by_text(_AUTH_ERROR_RE)
        for i in range(min(loc.count(), 5)):
            el = loc.nth(i)
            if el.is_visible():
                txt = (el.inner_text() or "").strip()
                if txt:
                    return txt
    except Exception:
        pass
    return None


# ======================================================================================================================
# QADAM-FUNKSIYALAR (granular)
# ======================================================================================================================

def login(page: Page, server: dict, email: str | None = None, password: str | None = None) -> tuple[str, str]:
    """
    Login sahifasini ochadi va berilgan (yoki default) login/parol bilan kiradi.
    email/password berilmasa — server["credentials"]["default"] ishlatiladi.
    Ishlatilgan (email, password) ni qaytaradi.
    """
    creds = server["credentials"]["default"]
    email = email or creds["email"]
    password = password or creds["password"]

    page.set_default_navigation_timeout(60_000)
    login_url = server["base_url"] + server.get("login_path", "/login.html")
    lp = LoginPage(page, login_url)
    lp.open()
    lp.element_visible()
    lp.fill_form(email, password)
    lp.submit()
    return email, password


def kill_active_session(page: Page, server: dict, timeout: int = 8_000) -> bool:
    """
    Active-session oynasi/sahifasi chiqqan-chiqmaganini tekshiradi.
    Chiqqan bo'lsa — BITTA sessiyani kill qiladi.

    Qaytaradi:
        True  — active-session bor edi, bitta sessiya kill qilindi
        False — chiqmadi (kill shart emas)
    """
    if _ui(server) == "new":
        # Yangi online: alohida sahifa /concurrent_session_list,
        # har sessiyada aria-label="Close session <id>" (trash) tugmasi.
        try:
            page.wait_for_url("**/concurrent_session_list**", timeout=timeout)
        except Exception:
            return False
        close_btns = page.locator(_CLOSE_SESSION_NEW)
        if close_btns.count() == 0:
            return False
        close_btns.first.click()
        page.wait_for_timeout(2_000)
        return True

    # Eski UI (xtrade): "Активные сеансы" modal.
    try:
        page.get_by_text("Активные сеансы").wait_for(timeout=timeout)
    except Exception:
        return False
    page.locator(".btn-danger, .fa-trash").first.click()
    page.wait_for_timeout(2_000)
    return True


def dashboard_opened(page: Page, server: dict) -> None:
    """Dashboard (asosiy ilova) ochilganini tekshiradi."""
    if _ui(server) == "new":
        # Login sahifasidan asosiy ilovaga o'tishni kutamiz. Parallel ravishda
        # login xatosini (noto'g'ri parol kabi) ham tekshiramiz — shunda test
        # 120s "url timeout" o'rniga aniq sabab bilan tez yiqiladi.
        deadline = time.time() + 60
        while time.time() < deadline:
            url = page.url
            if "auth/login" not in url and "concurrent_session" not in url:
                break  # muvaffaqiyatli o'tdik
            err = _login_error_text(page)
            if err:
                raise AssertionError(f"Login muvaffaqiyatsiz — server xabari: «{err}»")
            page.wait_for_timeout(500)
        else:
            err = _login_error_text(page)
            if err:
                raise AssertionError(f"Login muvaffaqiyatsiz — server xabari: «{err}»")
            raise AssertionError(f"Dashboard ochilmadi — login'dan keyin URL hali: {page.url}")

        page.locator(_ORG_SWITCHER_NEW).wait_for(state="visible", timeout=60_000)
    else:
        page.get_by_role("heading", name="Trade").wait_for(state="visible", timeout=120_000)


def switch_filial(page: Page, server: dict, name: str) -> None:
    """
    Filial / tashkilot almashtiradi. Test ichida istalgancha chaqirish mumkin.
    """
    if _ui(server) == "new":
        page.locator(_ORG_SWITCHER_NEW).click()
        overlay = page.locator(".cdk-overlay-container")
        overlay.get_by_text(name, exact=True).first.click()
        page.wait_for_timeout(1_500)
        BasePage(page).wait_for_loader()
        return

    # Eski UI (xtrade)
    page.locator(".pt-3.px-2").click()
    link = page.get_by_role("link", name=name, exact=True)
    if not link.is_visible():
        search = page.get_by_role("textbox", name="Поиск организации")
        if search.count() > 0:
            search.fill(name)
    expect(link).to_be_visible()
    link.click()
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("paragraph").filter(has_text=name)).to_be_visible()


def logout(page: Page, server: dict) -> None:
    """Tizimdan chiqadi."""
    if _ui(server) == "new":
        page.locator(_AVATAR_NEW).first.click()
        page.get_by_text("Выйти", exact=True).first.click()
        page.wait_for_url("**/auth/login**", timeout=30_000)
        return

    # Eski UI (xtrade): profil → Выйти → да → login.html
    profile = page.locator("#kt_header").get_by_text(
        re.compile(r"^[A-Za-zА-Яа-яЁё]$"), exact=True
    ).first
    if not profile.is_visible():
        profile = page.locator("#kt_header .topbar-item").last
    profile.click()

    logout_btn = page.get_by_role("link", name=" Выйти").first
    logout_btn.wait_for(state="visible", timeout=5_000)
    logout_btn.click()

    yes_btn = page.get_by_role("button", name="да", exact=True)
    yes_btn.wait_for(state="visible", timeout=5_000)
    yes_btn.click()

    page.wait_for_url("**/login.html**")
    page.wait_for_load_state("domcontentloaded")


# ======================================================================================================================
# YUQORI DARAJADAGI YORDAMCHILAR
# ======================================================================================================================

def authorize(page: Page, server: dict, email: str | None = None, password: str | None = None) -> None:
    """To'liq kirish: login → active-session kill (agar bo'lsa) → dashboard tekshirish."""
    login(page, server, email=email, password=password)
    kill_active_session(page, server)
    dashboard_opened(page, server)


class Session:
    """
    `auth` fixture qaytaradigan obyekt — test tanasi login va logout ICHIDA ishlaydi.
    Test ichida filial switch va login/parol o'zgartirish imkonini beradi.
    """

    def __init__(self, page: Page, server: dict):
        self.page = page
        self.server = server

    def switch_filial(self, name: str) -> None:
        switch_filial(self.page, self.server, name)

    def relogin(self, email: str | None = None, password: str | None = None) -> None:
        """Joriy seansdan chiqib, boshqa login/parol bilan qayta kiradi."""
        logout(self.page, self.server)
        authorize(self.page, self.server, email=email, password=password)

    def logout(self) -> None:
        logout(self.page, self.server)
