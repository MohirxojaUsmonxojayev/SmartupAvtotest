"""Qadam va sarlavha — ham Allure hisobotiga, ham Qase TestOps natijasiga yoziladi.

Ishlatish (``allure.step`` / ``allure.title`` o'rniga):

    from utils.step import step, title

    @title("TC-E2E-01: ТМЦ yaratish")
    def test_01_tmc(...):
        with step("1 - Login"):
            ...

Qase plugin'i o'chiq bo'lsa (lokal run, QASE_MODE berilmagan) ``qase.step`` jim
o'tib ketadi — natija faqat Allure'da qoladi. Qadam ichidagi xato Allure'da ham,
Qase'da ham shu qadamni "failed" deb belgilaydi va odatdagidek yuqoriga ko'tariladi.
"""
from contextlib import contextmanager

import allure
from qase.pytest import qase


@contextmanager
def step(title: str, expected: str | None = None):
    with allure.step(title), qase.step(title, expected):
        yield


def title(text: str):
    """Test sarlavhasi: Allure (``allure.title``) va Qase run'idagi natija nomi (``qase.title``)."""
    def decorator(func):
        return qase.title(text)(allure.title(text)(func))
    return decorator
