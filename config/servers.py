"""
Server konfiguratsiyasi — online va xtrade uchun base_url, credentials va default filial.
`--server` CLI opsiyasi yoki tests/online, tests/xtrade papkalaridagi conftest shu dict'ni tanlaydi.
"""
import copy

from config.credentials import ONLINE, XTRADE

SERVERS = {
    "online": {
        "name":           "online",
        "base_url":       "https://smartup.online",
        "login_path":     "/a2/auth/login",           # yangi Angular UI (login.html shu yerga redirect)
        "ui":             "new",                       # yangi UI (dashboard/filial/logout boshqacha)
        "credentials":    ONLINE,
        "default_filial": "Manual Test company",       # online'da tashkilot/kompaniya switcher
    },
    "xtrade": {
        "name":           "xtrade",
        "base_url":       "https://app3.greenwhite.uz/xtrade",
        "login_path":     "/a2/auth/login",            # yangi Angular UI (online bilan bir xil)
        "ui":             "new",
        "credentials":    XTRADE,
        "default_filial": "NovaTrade - Toshkent Filiali",
    },
}


def resolve_server(name: str, email: str | None = None, password: str | None = None) -> dict:
    """
    Server config'ining nusxasini qaytaradi. email/password berilsa — default
    login/parolni almashtiradi (masalan `--email` / `--password` CLI orqali
    noto'g'ri data bilan test ishga tushirish uchun).
    """
    cfg = copy.deepcopy(SERVERS[name])
    if email or password:
        d = cfg["credentials"]["default"]
        cfg["credentials"]["default"] = {
            "email": email or d["email"],
            "password": password or d["password"],
        }
    return cfg
