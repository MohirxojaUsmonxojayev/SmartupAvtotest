import allure


class SoftAssert:
    """
    Soft assertion — bitta tekshiruv xatosi test'ni to'xtatmaydi.
    Barcha xatolar yig'ilib, assert_all() da bitta AssertionError sifatida chiqariladi.
    Har bir xatoda screenshot + URL Allure'ga biriktiriladi.

    Ishlatish (odatda `soft` fixture orqali):
        def test_x(page, soft):
            soft.check(condition, "❌ [Modul] 'Element' topilmadi")
            ...
        # fixture teardown'da assert_all() avtomatik chaqiriladi
    """

    def __init__(self, page=None) -> None:
        self.failures: list[str] = []
        self._page = page

    def check(self, condition: bool, message: str) -> None:
        """Xato bo'lsa (condition=False) failures ga qo'shadi, to'xtamaydi."""
        if condition:
            return
        self.failures.append(message)
        try:
            allure.attach(message, name="soft-fail", attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass
        if self._page:
            try:
                screenshot = self._page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"soft-fail: {message[:50]}",
                    attachment_type=allure.attachment_type.PNG,
                )
                allure.attach(
                    self._page.url,
                    name=f"url: {message[:50]}",
                    attachment_type=allure.attachment_type.TEXT,
                )
            except Exception:
                pass

    def assert_all(self) -> None:
        """Test oxirida chaqiriladi. Xatolar bo'lsa AssertionError chiqaradi."""
        if not self.failures:
            summary = "✅ Barcha soft tekshiruvlar muvaffaqiyatli"
        else:
            lines = [f"🔴 XATOLAR SONI: {len(self.failures)}"] + self.failures
            summary = "\n".join(lines)

        try:
            allure.attach(summary, name="Soft-assert yakuniy natija", attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass

        if self.failures:
            raise AssertionError(summary)
