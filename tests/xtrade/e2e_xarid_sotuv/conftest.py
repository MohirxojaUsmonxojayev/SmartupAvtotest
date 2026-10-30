"""
E2E ssenariy uchun umumiy sessiya + holat.
Barcha test_NN fayllari bitta brauzer sessiyasini va `e2e` holatini birga ishlatadi (tartibli).
"""
import datetime
import json
import os

import pytest
from playwright.sync_api import sync_playwright

from config.servers import resolve_server
from flows.auth_flow import login, kill_active_session, dashboard_opened, switch_filial

STATE_PATH = "test-results/e2e_state.json"


def _headless() -> bool:
    return os.getenv("HEADLESS", "0").strip().lower() in {"1", "true", "yes", "on"}


@pytest.fixture(scope="session")
def rdate() -> str:
    """Yugurish belgisi <DDMMHHMM> — har run UNIQUE (kod/nom to'qnashmasligi uchun).
    (Ssenariyда <DDMM> edi; avtomatlashtirishda takror run'lar bir xil kod yaratmasligi uchun vaqt qo'shildi.)"""
    return datetime.datetime.now().strftime("%d%m%H%M")


@pytest.fixture(scope="session")
def e2e() -> dict:
    """Yaratilgan ID/raqamlar — testlar orasida umumiy, JSON ga yoziladi (resume uchun)."""
    data = {}
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    yield data
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@pytest.fixture(scope="session")
def e2e_page():
    """Bitta brauzer sessiyasi: login + operatsion filial. Barcha E2E testlar birga ishlatadi."""
    server = resolve_server("xtrade")
    headless = _headless()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=[] if headless else ["--start-maximized"])
        if headless:
            ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        else:
            ctx = browser.new_context(no_viewport=True)
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = ctx.new_page()

        login(page, server)
        kill_active_session(page, server)
        dashboard_opened(page, server)
        switch_filial(page, server, server["default_filial"])

        yield page

        os.makedirs("test-results/traces", exist_ok=True)
        try:
            ctx.tracing.stop(path="test-results/traces/e2e_xarid_sotuv.zip")
        except Exception:
            pass
        try:
            ctx.close()
            browser.close()
        except Exception:
            pass
