# -*- coding: utf-8 -*-
"""Tungi qayta tekshiruv hisoboti generatori.
Kirish: findings.json  →  Chiqish: <out>/ (README.md, hisobotlar/*.md, screenshots/, bug_test_cases.md|json|xlsx, tekshiruv_jurnali.md)

findings.json tuzilmasi:
{
 "date": "2026-09-29", "started": "04:00", "finished": "05:10", "user": "mohir@xan", "filial": "Toshkent",
 "checked": [ {"module": "Склад", "page": "Закупки", "route": "/xtrade/a2/...", "checks": "smoke, view, create-form, empty-save", "status": "OK|BUG|SKIP", "note": ""} ],
 "known_status": [ {"id": "SKL-001", "status": "hali bor|tuzatilgan|tekshirilmadi", "note": ""} ],
 "new_bugs": [ {"id": "NEW-001", "module": "Склад", "page": "Закупки", "route": "/xtrade/a2/...", "severity": "Yuqori|O'rta|Past",
                "title": "…", "pre": ["…"], "data": ["…"], "steps": [["qadam", "kutilgan"], …], "fail_step": 2, "actual": "…", "tech": "…", "cleanup": ["…"], "shots": ["NEW-001.jpg"]} ]
}
Ishlatish: python3 night_report.py findings.json <out_dir> [shots_dir]
"""
import os, sys, json, shutil, re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

def slug(s):
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip(); return re.sub(r"[\s_]+", "-", s)[:50]

def bug_md(b):
    L = ["# %s — %s" % (b["id"], b["title"]), "", "| | |", "|---|---|",
         "| Modul / sahifa | %s → %s |" % (b["module"], b["page"]), "| URL | %s |" % b.get("route", ""),
         "| Jiddiylik | %s |" % b.get("severity", ""), "| Topildi | %s (tungi avtomatik qayta tekshiruv) |" % b.get("found", ""),
         "", "## Old shartlar"] + ["- " + p for p in b.get("pre", [])] + ["", "## Test ma'lumotlari"] + (["- " + d for d in b.get("data", [])] or ["- —"]) + \
        ["", "## Qadamlar", "", "| № | Qadam | Kutilgan natija |", "|---|---|---|"]
    for i, (d, e) in enumerate(b["steps"], 1):
        L.append("| %d%s | %s | %s |" % (i, " ❌" if i == b.get("fail_step") else "", d, e))
    L += ["", "## Haqiqiy natija", "", b.get("actual", "")]
    if b.get("tech"): L += ["", "## Texnik ma'lumot", "", "```", b["tech"], "```"]
    if b.get("cleanup"): L += ["", "## Tozalash"] + ["- " + c for c in b["cleanup"]]
    if b.get("shots"): L += ["", "## Skrinshotlar"] + ["![%s](../screenshots/%s)" % (s, s) for s in b["shots"]]
    return "\n".join(L)

def main(fj, out, shots_dir=None):
    F = json.load(open(fj)); os.makedirs(os.path.join(out, "hisobotlar"), exist_ok=True); os.makedirs(os.path.join(out, "screenshots"), exist_ok=True)
    bugs = F.get("new_bugs", []); checked = F.get("checked", []); known = F.get("known_status", [])
    for b in bugs:
        b.setdefault("found", F.get("date", ""))
        open(os.path.join(out, "hisobotlar", "%s_%s.md" % (b["id"], slug(b["title"]))), "w").write(bug_md(b))
        for s in b.get("shots", []):
            src = os.path.join(shots_dir or "", s)
            if shots_dir and os.path.exists(src): shutil.copy(src, os.path.join(out, "screenshots", s))
    # bug test case'lar
    tcs = []
    for i, b in enumerate(bugs, 1):
        tcs.append(dict(id="TC-NEW-%03d" % i, bug=b["id"], module=b["module"], form=b["page"], title=b["title"], type="Bug", priority={"Yuqori": "P1", "O'rta": "P2"}.get(b.get("severity"), "P3"),
                        pre=b.get("pre", []), data=b.get("data", []), steps=[dict(n=n, action="manual", d=d, e=e) for n, (d, e) in enumerate(b["steps"], 1)],
                        expected=b["steps"][b.get("fail_step", 1) - 1][1] if b.get("steps") else "", actual=b.get("actual", ""), fail_step=b.get("fail_step"), result="Fail", route=b.get("route", ""),
                        cleanup=b.get("cleanup", []), report="hisobotlar/%s_%s.md" % (b["id"], slug(b["title"]))))
    json.dump(dict(generated=F.get("date"), cases=tcs), open(os.path.join(out, "bug_test_cases.json"), "w"), ensure_ascii=False, indent=1)
    L = ["# Yangi buglar uchun test case'lar — %s" % F.get("date", ""), "", "Har case «Fail» — qadam ❌ da xato chiqadi. Bug tuzatilgach shu case regressiya sifatida yuritiladi.", ""]
    for t in tcs:
        L += ["## %s · %s · %s" % (t["id"], t["bug"], t["title"]), "", "Modul: %s → %s · Prioritet: %s · URL: %s" % (t["module"], t["form"], t["priority"], t["route"]), "",
              "Old shartlar: " + "; ".join(t["pre"]), "", "| № | Qadam | Kutilgan |", "|---|---|---|"]
        for s in t["steps"]:
            L.append("| %d%s | %s | %s |" % (s["n"], " ❌" if s["n"] == t["fail_step"] else "", s["d"], s["e"]))
        L += ["", "Haqiqiy natija: " + t["actual"], "", "Hisobot: [%s](%s)" % (t["bug"], t["report"]), ""]
    open(os.path.join(out, "bug_test_cases.md"), "w").write("\n".join(L))
    wb = Workbook(); ws = wb.active; ws.title = "Bug test case'lar"
    H = ["TC ID", "Bug", "Modul", "Sahifa", "Nomi", "Prioritet", "Old shartlar", "Qadamlar (№. qadam → kutilgan)", "Xato qadami", "Haqiqiy natija", "URL", "Natija"]
    ws.append(H)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="7B2D26"); c.alignment = Alignment(wrap_text=True, vertical="top")
    for t in tcs:
        ws.append([t["id"], t["bug"], t["module"], t["form"], t["title"], t["priority"], "\n".join(t["pre"]), "\n".join("%d. %s → %s" % (s["n"], s["d"], s["e"]) for s in t["steps"]), t["fail_step"], t["actual"], t["route"], t["result"]])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, w in enumerate([12, 10, 16, 24, 45, 9, 30, 70, 8, 50, 40, 8], 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws2 = wb.create_sheet("Tekshiruv jurnali"); ws2.append(["Modul", "Sahifa", "URL", "Tekshiruvlar", "Holat", "Izoh"])
    for c in ws2[1]: c.font = Font(bold=True)
    for r in checked: ws2.append([r.get("module"), r.get("page"), r.get("route"), r.get("checks"), r.get("status"), r.get("note")])
    for i, w in enumerate([18, 34, 50, 30, 8, 60], 1): ws2.column_dimensions[get_column_letter(i)].width = w
    ws3 = wb.create_sheet("Ma'lum buglar holati"); ws3.append(["Bug ID", "Holat", "Izoh"])
    for c in ws3[1]: c.font = Font(bold=True)
    for r in known: ws3.append([r.get("id"), r.get("status"), r.get("note")])
    wb.save(os.path.join(out, "bug_test_cases.xlsx"))
    # jurnal + README
    ok = sum(1 for r in checked if r.get("status") == "OK"); bad = sum(1 for r in checked if r.get("status") == "BUG"); sk = sum(1 for r in checked if r.get("status") == "SKIP")
    L = ["# Tungi qayta tekshiruv — %s (%s–%s)" % (F.get("date"), F.get("started", ""), F.get("finished", "")), "",
         "Muhit: https://app3.greenwhite.uz/xtrade, foydalanuvchi %s, filial %s. Tekshiruv turi: har sahifa — smoke (ochilish, ustunlar, tugmalar, 4xx/5xx), qator amallari, ko'rish, yaratish formasi, bo'sh saqlash validatsiyasi; ma'lumotnomalarda QA- yozuv bilan CRUD. Test case'lar faqat **yangi** buglar uchun yozildi." % (F.get("user", ""), F.get("filial", "")), "",
         "| Ko'rsatkich | Son |", "|---|---|", "| Tekshirilgan sahifalar | %d |" % len(checked), "| Xatosiz | %d |" % ok, "| Bug bilan | %d |" % bad, "| O'tkazib yuborilgan | %d |" % sk,
         "| Yangi buglar | %d |" % len(bugs), "| Ma'lum buglar: hali bor / tuzatilgan | %d / %d |" % (sum(1 for k in known if k.get("status") == "hali bor"), sum(1 for k in known if k.get("status") == "tuzatilgan")), "",
         "## Yangi buglar", "", "| ID | Jiddiylik | Modul → sahifa | Nomi | Hisobot | Test case |", "|---|---|---|---|---|---|"]
    for t, b in zip(tcs, bugs):
        L.append("| %s | %s | %s → %s | %s | [md](%s) | %s |" % (b["id"], b.get("severity", ""), b["module"], b["page"], b["title"], t["report"], t["id"]))
    if not bugs: L.append("| — | | | Yangi bug topilmadi | | |")
    L += ["", "## Tekshiruv jurnali", "", "| Modul | Sahifa | Tekshiruvlar | Holat | Izoh |", "|---|---|---|---|---|"]
    for r in checked: L.append("| %s | %s | %s | %s | %s |" % (r.get("module"), r.get("page"), r.get("checks"), r.get("status"), r.get("note", "")))
    if F.get("notes"): L += ["", "## Izohlar", ""] + ["- " + n for n in F["notes"]]
    open(os.path.join(out, "README.md"), "w").write("\n".join(L))
    print("OK:", out, "| sahifalar:", len(checked), "| yangi buglar:", len(bugs))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
