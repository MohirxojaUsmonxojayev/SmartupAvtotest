"""
Root conftest — browser/context/page fixture'lari, server tanlash va `auth` fixture.

Server tanlash:
  - tests/online/ va tests/xtrade/ papkalaridagi conftest `server` fixture'ni majburlaydi.
  - Aks holda `--server=online|xtrade` CLI opsiyasi ishlatiladi (default: online).
"""
import os
import sys
from typing import Any, Generator

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from config.servers import resolve_server
from flows.auth_flow import authorize, logout, Session

load_dotenv()  # .env dan TELEGRAM_*, HEADLESS va h.k. o'qiladi

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TRACE_DIR = "test-results/traces"


def _is_headless() -> bool:
    """CI'da HEADLESS=1 (ko'rinmas), lokalda 0 (ko'rinadigan)."""
    return os.getenv("HEADLESS", "0").strip().lower() in {"1", "true", "yes", "on"}


# ======================================================================================================================
# SERVER TANLASH
# ======================================================================================================================

def pytest_addoption(parser):
    parser.addoption(
        "--server",
        action="store",
        default="online",
        choices=["online", "xtrade"],
        help="Qaysi serverda ishlash: 'online' yoki 'xtrade' (tests/online, tests/xtrade papkalari buni majburlaydi).",
    )
    parser.addoption(
        "--email",
        action="store",
        default=None,
        help="Default login'ni almashtirish (masalan noto'g'ri data bilan test uchun).",
    )
    parser.addoption(
        "--password",
        action="store",
        default=None,
        help="Default parolni almashtirish (masalan noto'g'ri data bilan test uchun).",
    )


@pytest.fixture
def server(request) -> dict:
    """Server config. tests/online va tests/xtrade conftest'lari buni override qiladi."""
    name = request.config.getoption("--server")
    cfg = resolve_server(
        name,
        request.config.getoption("--email"),
        request.config.getoption("--password"),
    )
    print(f"\n[CONFIG] Server: {name} | {cfg['base_url']}")
    return cfg


# ======================================================================================================================
# BROWSER / CONTEXT / PAGE
# ======================================================================================================================

@pytest.fixture(scope="session")
def browser() -> Generator[Browser, Any, None]:
    headless = _is_headless()
    args = [] if headless else ["--start-maximized"]
    with sync_playwright() as p:
        browser_obj = p.chromium.launch(headless=headless, args=args)
        yield browser_obj
        browser_obj.close()


@pytest.fixture
def context(browser: Browser, request) -> Generator[BrowserContext, Any, None]:
    # Headless'da keng viewport majburiy — aks holda Smartup responsive header
    # desktop elementlarni (org-switcher) yashiradi va mobil hamburger chiqadi.
    # Headed'da esa --start-maximized bilan no_viewport ishlatamiz.
    if _is_headless():
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
    else:
        ctx = browser.new_context(no_viewport=True)
    os.makedirs(TRACE_DIR, exist_ok=True)
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield ctx

    safe = (
        request.node.nodeid
        .replace("/", "_").replace("\\", "_")
        .replace("::", "__").replace("[", "_").replace("]", "_")
    )
    try:
        ctx.tracing.stop(path=os.path.join(TRACE_DIR, f"{safe}.zip"))
    except Exception:
        pass
    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, Any, None]:
    pg = context.new_page()
    yield pg
    pg.close()


# ======================================================================================================================
# YIQILGANDA ALLURE'GA SCREENSHOT + URL + HTML BIRIKTIRISH
# ======================================================================================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Test yiqilsa — joriy sahifa screenshot'i, URL va HTML'ini Allure'ga biriktiradi.
    Shunda Allure hisobotida muammo aynan nimada ekani ko'rinadi.
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            try:
                allure.attach(
                    page.screenshot(full_page=True),
                    name="screenshot_yiqilganda",
                    attachment_type=allure.attachment_type.PNG,
                )
                allure.attach(page.url, name="URL", attachment_type=allure.attachment_type.TEXT)
                allure.attach(
                    page.content(),
                    name="page_html",
                    attachment_type=allure.attachment_type.HTML,
                )
            except Exception:
                pass


# ======================================================================================================================
# AUTH FIXTURE — boshqa testlar login/logout ICHIDA yoziladi
# ======================================================================================================================

@pytest.fixture
def auth(page: Page, server: dict) -> Generator[Session, Any, None]:
    """
    Testdan oldin login qiladi (default login/parol), test tugagach logout.
    Qaytaradi: Session — test ichida .switch_filial(...) va .relogin(...) mavjud.

    Ishlatilishi:
        def test_x(auth):
            auth.switch_filial("...")      # istalgancha
            auth.relogin(email=..., password=...)
            ...                            # test tanasi
        # test tugagach avtomatik logout
    """
    authorize(page, server)
    session = Session(page, server)
    yield session
    try:
        logout(page, server)
    except Exception:
        pass
