#!/usr/bin/env python3
"""
allure-results papkasidan qisqa HTML summary chiqaradi (Telegram uchun):
  - nechta ✅ passed / ❌ failed / ⚠️ skipped
  - yiqilgan testlar nomi + xato matnining 1-qatori

Ishlatilishi: python scripts/ci_summary.py [allure-results-dir]
"""
import glob
import html
import json
import os
import sys


def main() -> None:
    d = sys.argv[1] if len(sys.argv) > 1 else "allure-results"
    results = []
    for f in glob.glob(os.path.join(d, "*-result.json")):
        try:
            with open(f, encoding="utf-8") as fh:
                results.append(json.load(fh))
        except Exception:
            pass

    counts = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "unknown": 0}
    failed = []
    for r in results:
        st = r.get("status", "unknown")
        counts[st] = counts.get(st, 0) + 1
        if st in ("failed", "broken"):
            name = r.get("name", "?")
            msg = ((r.get("statusDetails") or {}).get("message") or "").strip()
            first = msg.splitlines()[0] if msg else ""
            failed.append((name, first))

    total = len(results)
    bad = counts["failed"] + counts["broken"]
    lines = [f"📦 Jami: {total}  |  ✅ {counts['passed']}  |  ❌ {bad}  |  ⚠️ {counts['skipped']}"]
    for name, msg in failed[:10]:
        line = f"❌ <code>{html.escape(name)}</code>"
        if msg:
            m = msg if len(msg) <= 200 else msg[:200] + "…"
            line += f"\n   └ {html.escape(m)}"
        lines.append(line)
    if len(failed) > 10:
        lines.append(f"… va yana {len(failed) - 10} ta (Allure'da)")

    # UTF-8 bytes — konsol kodlanishiga bog'liq bo'lmasin (Windows/CI)
    sys.stdout.buffer.write("\n".join(lines).encode("utf-8"))


if __name__ == "__main__":
    main()
