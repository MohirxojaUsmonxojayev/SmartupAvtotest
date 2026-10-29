from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Login muvaffaqiyatli bo'lgach ochiladigan asosiy sahifa."""

    def is_opened(self) -> None:
        """Dashboard ochilganini tekshiradi ('Trade' sarlavhasi ko'rinadi)."""
        self.wait_for(self.page.get_by_role("heading", name="Trade"), timeout=120_000)
