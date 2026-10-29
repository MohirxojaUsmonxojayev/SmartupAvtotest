#!/usr/bin/env python3
"""
Telegram xabar yuborish/tahrirlash — CI progress uchun.

Ishlatilishi (matn STDIN'dan — uzun/HTML matn uchun xavfsiz):
    echo "matn" | python scripts/tg_notify.py send         -> message_id ni chiqaradi
    echo "matn" | python scripts/tg_notify.py edit <msg_id>

ENV: TELEGRAM_BOT_TOKEN, TG_CHAT
Hech qachon xato bermaydi (CI step'ni yiqitmaslik uchun).
"""
import json
import os
import sys
import urllib.request

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT = os.environ.get("TG_CHAT", "").strip()


def _api(method: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TOKEN}/{method}",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> None:
    if not TOKEN or not CHAT:
        return
    mode = sys.argv[1] if len(sys.argv) > 1 else "send"
    # UTF-8 bytes — konsol/locale kodlanishiga bog'liq bo'lmasin
    text = sys.stdin.buffer.read().decode("utf-8", "replace").strip() or "..."
    base = {"chat_id": CHAT, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}

    if mode == "edit" and len(sys.argv) > 2 and sys.argv[2]:
        try:
            _api("editMessageText", {**base, "message_id": sys.argv[2]})
            return
        except Exception:
            pass  # tahrir bo'lmasa (masalan xabar o'chirilgan) — yangi yuboramiz
    res = _api("sendMessage", base)
    print(res.get("result", {}).get("message_id", ""))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
