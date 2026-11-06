"""Bitta qadam — ham Allure hisobotiga, ham Qase TestOps natijasiga yoziladi.

Ishlatish (``allure.step`` o'rniga):

    from utils.step import step

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
