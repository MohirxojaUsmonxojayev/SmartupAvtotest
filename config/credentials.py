"""
DEFAULT login/parollar — ENV orqali (parollar KODDA saqlanmaydi!).

Parollar:
  - lokalda  → .env fayldan (gitignore, repoga kirmaydi)
  - CI'da    → GitHub Secrets'dan (workflow env sifatida beradi)

Repo PUBLIC bo'lgani uchun hech qanday haqiqiy parol kodda yozilmaydi.
Login (email) — test-akkaunt identifikatori, maxfiy emas, qulaylik uchun default bor.

Test ichida istalgan payt boshqa login/parol:
    login(page, server, email="...", password="...")
    session.relogin(email="...", password="...")
"""
import os

from dotenv import load_dotenv

# .env ni env o'qishdan OLDIN yuklaymiz (CI'da .env yo'q — Secrets real env sifatida keladi,
# load_dotenv mavjud env'ni override qilmaydi, shuning uchun CI'da Secrets ustun turadi).
load_dotenv()


def _cred(email_default: str, email_env: str, pass_env: str) -> dict:
    return {
        "email": os.getenv(email_env, "").strip() or email_default,
        "password": os.getenv(pass_env, "").strip(),   # parol faqat env'dan
    }


# ----------------------------------------------------------------------------------------------------------------------
# SMARTUP ONLINE  (https://smartup.online)
# ----------------------------------------------------------------------------------------------------------------------
ONLINE = {
    "default": _cred("alibe@test", "ONLINE_LOGIN", "ONLINE_PASSWORD"),
    "admin":   _cred("admin@test", "ONLINE_ADMIN_LOGIN", "ONLINE_ADMIN_PASSWORD"),
}

# ----------------------------------------------------------------------------------------------------------------------
# XTRADE  (https://app3.greenwhite.uz/xtrade)
# ----------------------------------------------------------------------------------------------------------------------
XTRADE = {
    "default": _cred("moxir@novatrade", "XTRADE_LOGIN", "XTRADE_PASSWORD"),
    "admin":   _cred("admin@novatrade", "XTRADE_ADMIN_LOGIN", "XTRADE_ADMIN_PASSWORD"),
}
