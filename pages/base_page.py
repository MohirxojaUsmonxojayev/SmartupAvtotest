from playwright.sync_api import Page, Locator


class BasePage:
    """Barcha page-object'lar uchun umumiy asos (POM)."""

    def __init__(self, page: Page):
        self.page = page

    # ------------------------------------------------------------------------------------------------------------------
    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def navigate(self, url: str) -> None:
        self.page.goto(url)

    def wait_for(self, locator: Locator, timeout: int = 60_000) -> None:
        locator.wait_for(state="visible", timeout=timeout)

    # ------------------------------------------------------------------------------------------------------------------
    def wait_for_loader(self, timeout: int = 120_000) -> None:
        """Loader (overlay) paydo bo'lib keyin yo'qolishini kutadi."""
        overlay = self.page.locator(".block-ui-overlay")
        try:
            overlay.wait_for(state="visible", timeout=2_000)
        except Exception:
            return  # loader 2s ichida chiqmasa — jarayon tugagan yoki juda tez o'tgan
        overlay.wait_for(state="hidden", timeout=timeout)
