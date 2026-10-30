# Faza 0 — Dalil yig'ish: implementatsiya rejasi

> **Agent ishchilar uchun:** MAJBURIY SUB-SKILL: bu rejani vazifa-ba-vazifa bajarish uchun
> `superpowers:subagent-driven-development` (tavsiya) yoki `superpowers:executing-plans`
> ishlating. Qadamlar `- [ ]` checkbox sintaksisida — belgilab boring.

**Maqsad:** Mavjud `3_Avtotest/SmartUp_Autotest/` (JavaScript) avtotestini bir marta real
serverda yuritib, a2 UI ning qaysi selektori va qaysi `action` i haqiqatan ishlashini
o'lchangan jadval sifatida qo'lga kiritish — Faza 1 da POM ni shu jadval ustiga qurish uchun.

**Arxitektura:** Ikki qism. (1) `Avtotest_POM/scripts/baseline.py` — yangi Python loyihaning
birinchi fayli; tungi yugurish natijalarini (`regression.jsonl`, `health.jsonl`) o'qib,
har bir `action` va har bir selektor uchun "necha marta ishladi / necha marta yiqildi"
jadvalini chiqaradi. (2) JS to'plamini real serverda bir marta yuritish. Analizator
avval TDD bilan yoziladi (fixture ma'lumotlarda, serversiz), keyin real natijaga qo'llanadi.

**Tech Stack:** Python 3.12+, pytest 8.4.2 (analizator); Node.js 24 + Playwright 1.55
(mavjud JS to'plami, o'zgartirilmaydi); macOS Keychain (parol).

**Spec:** `3_Avtotest/Hujjatlar/2026-09-29-pom-birlashtirish-design.md`

## Global cheklovlar

- Yangi loyiha manzili: `3_Avtotest/Avtotest_POM/` — avtotest fayllari faqat `3_Avtotest/` ichida (CLAUDE.md 1-qoida).
- Natija papkalari: `3_Avtotest/Tungi_natijalar/<YYYY-MM-DD>/` — ildizga yozilmaydi (CLAUDE.md 2-qoida).
- **Parol kiritilmaydi.** Keychain'ga parolni faqat foydalanuvchi o'zi qo'shadi (CLAUDE.md 4-qoida).
- Tashqi tizimlarga (WMS, Soliq, Faktura, Telegram biznes-oqimi, CRPT) hech narsa yuborilmaydi.
- Foydalanuvchi/huquq/sozlamalar o'zgartirilmaydi; faqat `QA-`/`SIM-` prefiksli yozuvlar o'chiriladi.
- Nomlash: kodda va hujjatda **`order`**, `zakaz` emas.
- `3_Avtotest/SmartUp_Autotest/` ning mavjud kodi **o'zgartirilmaydi** — faqat yuritiladi.
  Faza 0 da yoziladigan yangi kod `Avtotest_POM/` ga tushadi.
- Javoblar va hujjatlar o'zbek tilida (CLAUDE.md 5-qoida).
- Git commit xabarlari oxirida: `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

---

## Fayl tuzilmasi

| Fayl | Mas'uliyati |
|---|---|
| `Avtotest_POM/.gitignore` | `.venv/`, `__pycache__/`, `.pytest_cache/` ni git'dan chiqaradi |
| `Avtotest_POM/README.md` | Loyiha nima ekani, Faza 0 qanday yuritilishi |
| `Avtotest_POM/pytest.ini` | `pythonpath = .` — `from scripts.baseline import …` ishlashi uchun |
| `Avtotest_POM/requirements.txt` | Faza 0 uchun faqat `pytest` |
| `Avtotest_POM/scripts/__init__.py` | `scripts` ni paket qiladi |
| `Avtotest_POM/scripts/baseline.py` | **Yagona analizator.** jsonl o'qish · xato tasnifi · action statistikasi · selektor dalili · hisobot |
| `Avtotest_POM/tests/__init__.py` | `tests` paketi |
| `Avtotest_POM/tests/test_baseline.py` | `baseline.py` ning birligi testlari (serversiz, fixture ma'lumotda) |

`baseline.py` bitta faylda qoladi (~220 qator): u bir maqsadli — natija fayllarini o'qib
jadval chiqaradi. Faza 1 da uning `classify_error` qismi POM ning xato ishlov berish
qatlamiga ko'chadi, qolgani `scripts/` da qoladi.

---

## Vazifalar

### Vazifa 1: Loyiha skeleti va pytest ishlashi

**Fayllar:**
- Create: `3_Avtotest/Avtotest_POM/.gitignore`
- Create: `3_Avtotest/Avtotest_POM/README.md`
- Create: `3_Avtotest/Avtotest_POM/pytest.ini`
- Create: `3_Avtotest/Avtotest_POM/requirements.txt`
- Create: `3_Avtotest/Avtotest_POM/scripts/__init__.py`
- Create: `3_Avtotest/Avtotest_POM/tests/__init__.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_baseline.py`

**Interfeyslar:**
- Consumes: yo'q (birinchi vazifa)
- Produces: `scripts` va `tests` paketlari; `pytest` `Avtotest_POM/` ildizidan ishlaydi

- [ ] **Qadam 1: Papkalarni va git repozitoriyni yaratish**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest
mkdir -p Avtotest_POM/scripts Avtotest_POM/tests
cd Avtotest_POM
git init
```

- [ ] **Qadam 2: `.gitignore` yozish**

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
.auth/
test-results/
```

- [ ] **Qadam 3: `requirements.txt` yozish**

```
pytest==8.4.2
```

- [ ] **Qadam 4: `pytest.ini` yozish**

```ini
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
addopts = -q
```

- [ ] **Qadam 5: `README.md` yozish**

```markdown
# Avtotest_POM — SmartUp xtrade yagona avtotest loyihasi

Dizayn: `../Hujjatlar/2026-09-29-pom-birlashtirish-design.md`
Hozirgi bosqich: **Faza 0 — dalil yig'ish** (`../Hujjatlar/2026-09-29-faza0-dalil-yigish-reja.md`)

## Faza 0 nima qiladi

Mavjud `../SmartUp_Autotest/` (JavaScript) to'plami bir marta real serverda yuritiladi.
Natijalardan `scripts/baseline.py` a2 selektor va `action` larining ishlash jadvalini chiqaradi.
Shu jadval Faza 1 da `pages/ui/a2.py` ning asosi bo'ladi.

## Ishga tushirish

    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    pytest                                      # analizator testlari (server kerak emas)
    python3 scripts/baseline.py ../Tungi_natijalar/<sana>
```

- [ ] **Qadam 6: Bo'sh paket fayllarini yaratish**

```bash
touch scripts/__init__.py tests/__init__.py
```

- [ ] **Qadam 7: Birinchi yiqiladigan testni yozish**

`tests/test_baseline.py`:

```python
from scripts import baseline


def test_modul_import_qilinadi():
    assert hasattr(baseline, "classify_error")
```

- [ ] **Qadam 8: Testni yuritib, yiqilishini tasdiqlash**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/Avtotest_POM
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Kutilgan: `ImportError: cannot import name 'baseline' from 'scripts'` — FAIL.
(`scripts/__init__.py` bor, lekin `baseline.py` hali yo'q.)

- [ ] **Qadam 9: `scripts/baseline.py` ni minimal holda yaratish**

```python
# -*- coding: utf-8 -*-
"""Faza 0 — dalil yig'ish: tungi yugurish natijalaridan a2 selektor/action baseline jadvali."""


def classify_error(msg):
    return "boshqa"
```

- [ ] **Qadam 10: Testni yuritib, o'tishini tasdiqlash**

```bash
pytest
```

Kutilgan: `1 passed`.

- [ ] **Qadam 11: Commit**

```bash
git add .gitignore README.md pytest.ini requirements.txt scripts tests
git commit -m "$(cat <<'EOF'
feat(faza0): Avtotest_POM skeleti va baseline analizatori uchun pytest

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 2: Natija fayllarini o'qish (`load_jsonl`, `load_cases`)

**Fayllar:**
- Modify: `3_Avtotest/Avtotest_POM/scripts/baseline.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_baseline.py`

**Interfeyslar:**
- Consumes: Vazifa 1 dan `scripts.baseline` moduli
- Produces:
  - `load_jsonl(path: Path) -> list[dict]` — har qatori JSON bo'lgan fayl; fayl yo'q bo'lsa `[]`; buzuq qator tashlab ketiladi
  - `load_cases(path: Path) -> dict[str, dict]` — `regression_cases.json` dan `{case_id: case}`

- [ ] **Qadam 1: Yiqiladigan testlarni yozish**

`tests/test_baseline.py` ga qo'shish (yuqoridagi import testi qoladi):

```python
import json

from scripts import baseline


def test_load_jsonl_har_qatorni_oqiydi(tmp_path):
    f = tmp_path / "regression.jsonl"
    f.write_text('{"id": "TC-1", "result": "Pass"}\n{"id": "TC-2", "result": "Fail"}\n', encoding="utf-8")

    rows = baseline.load_jsonl(f)

    assert [r["id"] for r in rows] == ["TC-1", "TC-2"]


def test_load_jsonl_fayl_yoq_bolsa_bosh_royxat(tmp_path):
    assert baseline.load_jsonl(tmp_path / "yoq.jsonl") == []


def test_load_jsonl_buzuq_qatorni_tashlab_ketadi(tmp_path):
    f = tmp_path / "a.jsonl"
    f.write_text('{"id": "TC-1"}\nBUZUQ\n\n{"id": "TC-2"}\n', encoding="utf-8")

    assert [r["id"] for r in baseline.load_jsonl(f)] == ["TC-1", "TC-2"]


def test_load_cases_id_boyicha_lugat_qaytaradi(tmp_path):
    f = tmp_path / "cases.json"
    f.write_text(json.dumps({"cases": [
        {"id": "TC-1", "auto": True, "steps": [{"action": "nav"}]},
        {"id": "TC-2", "auto": False, "steps": []},
    ]}), encoding="utf-8")

    cases = baseline.load_cases(f)

    assert set(cases) == {"TC-1", "TC-2"}
    assert cases["TC-1"]["steps"][0]["action"] == "nav"
```

- [ ] **Qadam 2: Testlarni yuritib, yiqilishini tasdiqlash**

```bash
pytest
```

Kutilgan: 4 ta yangi test FAIL — `AttributeError: module 'scripts.baseline' has no attribute 'load_jsonl'`.

- [ ] **Qadam 3: Implementatsiya**

`scripts/baseline.py` ni to'liq almashtirish:

```python
# -*- coding: utf-8 -*-
"""Faza 0 — dalil yig'ish: tungi yugurish natijalaridan a2 selektor/action baseline jadvali.

Ishlatish:
    python3 scripts/baseline.py <kun_papkasi> [--cases <regression_cases.json>] [--out <papka>]
"""
import json
from pathlib import Path


def load_jsonl(path):
    """Har qatori JSON bo'lgan faylni o'qiydi. Fayl yo'q bo'lsa [] qaytaradi,
    buzuq qatorni tashlab ketadi (yugurish uzilganda oxirgi qator chala bo'lishi mumkin)."""
    path = Path(path)
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def load_cases(path):
    """regression_cases.json dan {case_id: case} lug'atini qaytaradi."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {c["id"]: c for c in data["cases"]}


def classify_error(msg):
    return "boshqa"
```

- [ ] **Qadam 4: Testlarni yuritib, o'tishini tasdiqlash**

```bash
pytest
```

Kutilgan: `5 passed`.

- [ ] **Qadam 5: Commit**

```bash
git add scripts/baseline.py tests/test_baseline.py
git commit -m "$(cat <<'EOF'
feat(faza0): natija fayllarini o'qish — load_jsonl va load_cases

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 3: Xato xabarini tasniflash (`classify_error`)

**Fayllar:**
- Modify: `3_Avtotest/Avtotest_POM/scripts/baseline.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_baseline.py`

**Interfeyslar:**
- Consumes: Vazifa 2 dan `scripts.baseline`
- Produces: `classify_error(msg: str | None) -> str` — quyidagi 8 ta kategoriyadan biri:
  `action_yozilmagan`, `selektor_topilmadi`, `xato_oynasi`, `assert_matn`,
  `assert_http`, `assert_expect`, `navigatsiya`, `boshqa`

Kategoriyalar `lib/smt.js` va `tests/regression.spec.js` chiqaradigan haqiqiy xabarlarga
asoslangan: `«{action}» avtomatlashtirilmagan`, `Xato oynasi: …`, `matn yo'q: …`,
`HTTP 500 /b/…`, `i18n 404: …`, Playwright ning `Timeout 20000ms exceeded` va
`strict mode violation` xabarlari.

- [ ] **Qadam 1: Yiqiladigan testlarni yozish**

`tests/test_baseline.py` ga qo'shish:

```python
import pytest


@pytest.mark.parametrize("msg, kutilgan", [
    ("«menu_plus» avtomatlashtirilmagan: Menyu yonidagi +", "action_yozilmagan"),
    ("locator.click: Timeout 20000ms exceeded.", "selektor_topilmadi"),
    ("strict mode violation: locator resolved to 3 elements", "selektor_topilmadi"),
    ("Xato oynasi: ORA-00001 unique constraint violated", "xato_oynasi"),
    ("matn yo'q: Наименование, Статус", "assert_matn"),
    ("HTTP 500 /xtrade/b/anor/mr/filial_list", "assert_http"),
    ("i18n 404: SKL-add.json", "assert_http"),
    ("expect(locator).toBeVisible() failed", "assert_expect"),
    ("page.goto: net::ERR_CONNECTION_REFUSED", "navigatsiya"),
    ("tushunarsiz nimadir", "boshqa"),
    ("", "boshqa"),
    (None, "boshqa"),
])
def test_classify_error(msg, kutilgan):
    assert baseline.classify_error(msg) == kutilgan


def test_action_yozilmagan_timeoutdan_ustun():
    """Ikkala naqsh ham mos kelsa, sababi aniqrog'i tanlanadi."""
    msg = "«menu_plus» avtomatlashtirilmagan — Timeout 20000ms exceeded"
    assert baseline.classify_error(msg) == "action_yozilmagan"
```

- [ ] **Qadam 2: Testlarni yuritib, yiqilishini tasdiqlash**

```bash
pytest
```

Kutilgan: jami 10 ta FAIL. 12 ta parametrlangan testdan 9 tasi yiqiladi — stub hamma
vaqt `"boshqa"` qaytargani uchun `"boshqa"` kutadigan 3 tasi (`tushunarsiz nimadir`,
`""`, `None`) allaqachon o'tadi. Ustiga `test_action_yozilmagan_timeoutdan_ustun` FAIL.

- [ ] **Qadam 3: Implementatsiya**

`scripts/baseline.py` da `import json` yonidan `import re` qo'shish va `classify_error` ni
almashtirish:

```python
import re

# Tartib muhim: yuqoridagi naqsh ustun turadi (bitta xabarga ikki naqsh mos kelishi mumkin).
ERROR_PATTERNS = [
    ("action_yozilmagan", r"avtomatlashtirilmagan"),
    ("xato_oynasi", r"Xato oynasi|Kutilgan xato kodi"),
    ("assert_matn", r"matn yo'q"),
    ("assert_http", r"\bHTTP \d{3}|i18n 404"),
    ("selektor_topilmadi", r"Timeout \d+ms exceeded|waiting for locator|strict mode violation|resolved to \d+ elements"),
    ("navigatsiya", r"net::|ERR_[A-Z_]+"),
    ("assert_expect", r"expect\(|toBeVisible|toContainText|toHaveURL|toBeDisabled|toBeTruthy"),
]


def classify_error(msg):
    """Xato xabarini sabab kategoriyasiga ajratadi. Bo'sh/None → 'boshqa'."""
    text = msg or ""
    for name, pattern in ERROR_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return name
    return "boshqa"
```

- [ ] **Qadam 4: Testlarni yuritib, o'tishini tasdiqlash**

```bash
pytest
```

Kutilgan: `18 passed`.

- [ ] **Qadam 5: Commit**

```bash
git add scripts/baseline.py tests/test_baseline.py
git commit -m "$(cat <<'EOF'
feat(faza0): xato xabarini 8 ta sabab kategoriyasiga tasniflash

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 4: Action statistikasi (`failed_action`, `action_stats`)

**Fayllar:**
- Modify: `3_Avtotest/Avtotest_POM/scripts/baseline.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_baseline.py`

**Interfeyslar:**
- Consumes: Vazifa 2 dan `load_cases`, Vazifa 3 dan `classify_error`
- Produces:
  - `failed_action(case: dict, failed_step: int | None) -> str | None` — `failed_step`
    **1 dan boshlanadi** (`regression.spec.js` uni `steps_done + 1` deb yozadi)
  - `ActionStat` — `dataclass` maydonlari: `action: str`, `ok: int`, `fail: int`,
    `errors: collections.Counter`
  - `action_stats(reg_rows: list[dict], cases: dict) -> dict[str, ActionStat]`

Hisoblash mantiqi: `result == "Pass"` bo'lgan case da **hamma** qadam bajarilgan →
har bir action `ok += 1`. `result == "Fail"` bo'lganda `failed_step` dan **oldingi**
qadamlar bajarilgan (`ok += 1`), `failed_step` dagi action yiqilgan (`fail += 1` va
sabab `errors` ga). `Skip` qatorlar hisobga olinmaydi. `Fail`, lekin `failed_step` yo'q bo'lgan qator ham
hisobga olinmaydi — qaysi qadam yiqilgani noma'lum bo'lsa, hech bir action haqida
xulosa chiqarib bo'lmaydi (kontroller rulingi R9).

- [ ] **Qadam 1: Yiqiladigan testlarni yozish**

`tests/test_baseline.py` ga qo'shish:

```python
CASES = {
    "TC-1": {"id": "TC-1", "steps": [
        {"action": "nav"}, {"action": "row_click"}, {"action": "assert_text"},
    ]},
    "TC-2": {"id": "TC-2", "steps": [
        {"action": "nav"}, {"action": "select"},
    ]},
}


def test_failed_action_bir_dan_boshlanadi():
    assert baseline.failed_action(CASES["TC-1"], 2) == "row_click"


def test_failed_action_chegaradan_tashqarida_none():
    assert baseline.failed_action(CASES["TC-1"], 0) is None
    assert baseline.failed_action(CASES["TC-1"], 9) is None
    assert baseline.failed_action(CASES["TC-1"], None) is None


def test_action_stats_pass_hamma_qadamni_ok_qiladi():
    stats = baseline.action_stats([{"id": "TC-1", "result": "Pass"}], CASES)

    assert stats["nav"].ok == 1
    assert stats["row_click"].ok == 1
    assert stats["assert_text"].ok == 1
    assert stats["nav"].fail == 0


def test_action_stats_fail_oldingilarni_ok_yiqilganini_fail_qiladi():
    rows = [{
        "id": "TC-1", "result": "Fail", "failed_step": 2,
        "error": "locator.click: Timeout 20000ms exceeded.",
    }]

    stats = baseline.action_stats(rows, CASES)

    assert stats["nav"].ok == 1
    assert stats["row_click"].fail == 1
    assert stats["row_click"].ok == 0
    assert stats["row_click"].errors["selektor_topilmadi"] == 1
    assert "assert_text" not in stats


def test_action_stats_skip_hisobga_olinmaydi():
    stats = baseline.action_stats([{"id": "TC-1", "result": "Skip"}], CASES)

    assert stats == {}


def test_action_stats_notanish_case_tashlab_ketiladi():
    stats = baseline.action_stats([{"id": "YOQ", "result": "Pass"}], CASES)

    assert stats == {}


def test_action_stats_bir_necha_case_yigiladi():
    rows = [
        {"id": "TC-1", "result": "Pass"},
        {"id": "TC-2", "result": "Fail", "failed_step": 2, "error": "matn yo'q: Статус"},
    ]

    stats = baseline.action_stats(rows, CASES)

    assert stats["nav"].ok == 2
    assert stats["select"].fail == 1
    assert stats["select"].errors["assert_matn"] == 1
```

- [ ] **Qadam 2: Testlarni yuritib, yiqilishini tasdiqlash**

```bash
pytest
```

Kutilgan: 8 ta yangi test FAIL — `AttributeError: … has no attribute 'failed_action'`.

- [ ] **Qadam 3: Implementatsiya**

`scripts/baseline.py` ning boshiga import qo'shish:

```python
from collections import Counter
from dataclasses import dataclass, field
```

va `classify_error` dan keyin qo'shish:

```python
@dataclass
class ActionStat:
    """Bitta `action` uchun yig'ma: necha marta muvaffaqiyatli bajarildi va necha marta yiqildi."""
    action: str
    ok: int = 0
    fail: int = 0
    errors: Counter = field(default_factory=Counter)

    @property
    def total(self):
        return self.ok + self.fail

    @property
    def success_rate(self):
        return self.ok / self.total if self.total else 0.0


def failed_action(case, failed_step):
    """Yiqilgan qadamdagi action nomi. `failed_step` 1 dan boshlanadi
    (regression.spec.js uni `steps_done + 1` deb yozadi). Chegaradan tashqarida — None."""
    steps = case.get("steps") or []
    if not failed_step or failed_step < 1 or failed_step > len(steps):
        return None
    return steps[failed_step - 1].get("action")


def action_stats(reg_rows, cases):
    """regression.jsonl qatorlaridan har bir action uchun ok/fail statistikasini yig'adi.

    Pass  → case ning hamma qadami bajarilgan.
    Fail  → failed_step dan oldingilari bajarilgan, failed_step dagisi yiqilgan.
    Fail, lekin failed_step yo'q → hech narsa hisoblanmaydi (qaysi qadam yiqilgani noma'lum).
    Skip  → hisobga olinmaydi.
    """
    stats = {}

    def stat(action):
        return stats.setdefault(action, ActionStat(action))

    for row in reg_rows:
        case = cases.get(row.get("id"))
        if case is None:
            continue
        steps = case.get("steps") or []
        result = row.get("result")

        if result == "Pass":
            for step in steps:
                stat(step["action"]).ok += 1
        elif result == "Fail":
            step_no = row.get("failed_step")
            if not step_no:
                # Qaysi qadam yiqilgani noma'lum — hech narsa hisoblanmaydi. Hamma qadamni
                # "ok" deb yozish yiqilgan case ning muvaffaqiyat foizini yolg'on ko'taradi.
                continue
            for step in steps[: max(step_no - 1, 0)]:
                stat(step["action"]).ok += 1
            action = failed_action(case, step_no)
            if action:
                entry = stat(action)
                entry.fail += 1
                entry.errors[classify_error(row.get("error"))] += 1

    return stats
```

- [ ] **Qadam 4: Testlarni yuritib, o'tishini tasdiqlash**

```bash
pytest
```

Kutilgan: `26 passed`.

- [ ] **Qadam 5: Commit**

```bash
git add scripts/baseline.py tests/test_baseline.py
git commit -m "$(cat <<'EOF'
feat(faza0): action bo'yicha ok/fail statistikasi va yiqilgan qadamni aniqlash

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 5: Selektor dalili (`selector_evidence`)

**Fayllar:**
- Modify: `3_Avtotest/Avtotest_POM/scripts/baseline.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_baseline.py`

**Interfeyslar:**
- Consumes: Vazifa 2 dan `load_jsonl`
- Produces:
  - `is_report(route: str) -> bool` — hisobot/dashboard route'imi (ularda grid bo'lmasligi normal)
  - `SelectorStat` — `dataclass`: `selector: str`, `ok: int`, `applicable: int`
  - `selector_evidence(health_rows: list[dict]) -> dict[str, SelectorStat]`

`health.spec.js` har sahifa uchun `health.jsonl` ga snapshot yozadi. Undan 6 ta asosiy
a2 selektori haqida bilvosita dalil chiqadi:

| Selektor | Qachon tegishli | Qachon "ishladi" |
|---|---|---|
| `main` (oxirgisi) | `list` kaliti bor | `list.title` bo'sh emas |
| `smt-cell-header` | `list` bor **va** hisobot route emas | `list.heads > 0` |
| `button:visible` | `list` bor | `list.btns` bo'sh emas |
| `.smt-data-row` | `rowActs` kaliti bor | `rowActs` bo'sh emas |
| `label` (forma maydoni) | `create` kaliti bor | `create.labels > 0` |
| `.cdk-overlay-pane` | `createMenu` kaliti bor | `createMenu` bo'sh emas |

- [ ] **Qadam 1: Yiqiladigan testlarni yozish**

`tests/test_baseline.py` ga qo'shish:

```python
def test_is_report():
    assert baseline.is_report("/xtrade/a2/trade/rep/sales_report") is True
    assert baseline.is_report("/xtrade/a2/anor/mr/dashboard") is True
    assert baseline.is_report("/xtrade/a2/anor/mr/filial_list") is False


def test_selector_evidence_royxat_selektorlari():
    rows = [
        {"route": "/xtrade/a2/anor/mr/filial_list",
         "list": {"title": "Организации", "heads": 7, "btns": ["Создать"]}},
        {"route": "/xtrade/a2/anor/mr/user_list",
         "list": {"title": "", "heads": 0, "btns": []}},
    ]

    ev = baseline.selector_evidence(rows)

    assert ev["main"].applicable == 2
    assert ev["main"].ok == 1
    assert ev["smt-cell-header"].applicable == 2
    assert ev["smt-cell-header"].ok == 1
    assert ev["button:visible"].ok == 1


def test_selector_evidence_hisobot_route_grid_dalilidan_chiqariladi():
    rows = [{"route": "/xtrade/a2/trade/rep/sales_report",
             "list": {"title": "Отчет", "heads": 0, "btns": ["Сформировать"]}}]

    ev = baseline.selector_evidence(rows)

    assert ev["smt-cell-header"].applicable == 0
    assert ev["main"].applicable == 1


def test_selector_evidence_qator_va_forma_selektorlari():
    rows = [
        {"route": "/a/b_list", "list": {"title": "T", "heads": 3, "btns": ["x"]},
         "rowActs": ["Просмотр", "Изменить"], "create": {"title": "C", "labels": 12}},
        {"route": "/a/c_list", "list": {"title": "T", "heads": 3, "btns": ["x"]},
         "rowActs": [], "create": {"title": "C", "labels": 0}},
        {"route": "/a/d_list", "list": {"title": "T", "heads": 3, "btns": ["x"]}},
    ]

    ev = baseline.selector_evidence(rows)

    assert ev[".smt-data-row"].applicable == 2
    assert ev[".smt-data-row"].ok == 1
    assert ev["label (forma maydoni)"].applicable == 2
    assert ev["label (forma maydoni)"].ok == 1


def test_selector_evidence_overlay_menyu():
    rows = [
        {"route": "/a/b_list", "list": {"title": "T", "heads": 1, "btns": ["x"]},
         "createMenu": ["Заказ", "Возврат"]},
        {"route": "/a/c_list", "list": {"title": "T", "heads": 1, "btns": ["x"]},
         "createMenu": []},
    ]

    ev = baseline.selector_evidence(rows)

    assert ev[".cdk-overlay-pane"].applicable == 2
    assert ev[".cdk-overlay-pane"].ok == 1
```

- [ ] **Qadam 2: Testlarni yuritib, yiqilishini tasdiqlash**

```bash
pytest
```

Kutilgan: 5 ta yangi test FAIL — `AttributeError: … has no attribute 'is_report'`.

- [ ] **Qadam 3: Implementatsiya**

`scripts/baseline.py` ga qo'shish (`action_stats` dan keyin):

```python
# health.spec.js dagi IS_REPORT bilan bir xil: bu sahifalarda grid bo'lmasligi normal
REPORT_ROUTE = re.compile(r"/rep/|dashboard|report", re.IGNORECASE)


def is_report(route):
    return bool(REPORT_ROUTE.search(route or ""))


@dataclass
class SelectorStat:
    """Bitta selektor uchun: necha sahifada tegishli bo'ldi va necha sahifada ishladi."""
    selector: str
    ok: int = 0
    applicable: int = 0

    @property
    def confidence(self):
        return self.ok / self.applicable if self.applicable else 0.0


# (selektor, tegishlimi?, ishladimi?) — health.jsonl yozuvidan bilvosita dalil
SELECTOR_PROBES = [
    ("main",
     lambda r: "list" in r,
     lambda r: bool(r["list"].get("title"))),
    ("smt-cell-header",
     lambda r: "list" in r and not is_report(r.get("route")),
     lambda r: (r["list"].get("heads") or 0) > 0),
    ("button:visible",
     lambda r: "list" in r,
     lambda r: bool(r["list"].get("btns"))),
    (".smt-data-row",
     lambda r: "rowActs" in r,
     lambda r: bool(r["rowActs"])),
    ("label (forma maydoni)",
     lambda r: "create" in r,
     lambda r: (r["create"].get("labels") or 0) > 0),
    (".cdk-overlay-pane",
     lambda r: "createMenu" in r,
     lambda r: bool(r["createMenu"])),
]


def selector_evidence(health_rows):
    """health.jsonl dan har bir asosiy a2 selektori uchun bilvosita dalil yig'adi.

    Bu isbot emas, ko'rsatkich: selektor ishlamasa health.spec.js bo'sh qiymat yozadi.
    Past ishonch — Faza 1 da qo'lda tekshirish kerakligini bildiradi.
    """
    stats = {name: SelectorStat(name) for name, _, _ in SELECTOR_PROBES}
    for row in health_rows:
        for name, applies, works in SELECTOR_PROBES:
            if not applies(row):
                continue
            stats[name].applicable += 1
            if works(row):
                stats[name].ok += 1
    return stats
```

- [ ] **Qadam 4: Testlarni yuritib, o'tishini tasdiqlash**

```bash
pytest
```

Kutilgan: `31 passed`.

- [ ] **Qadam 5: Commit**

```bash
git add scripts/baseline.py tests/test_baseline.py
git commit -m "$(cat <<'EOF'
feat(faza0): health.jsonl dan a2 selektorlari uchun bilvosita dalil

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 6: Hisobot va CLI (`render_markdown`, `main`)

**Fayllar:**
- Modify: `3_Avtotest/Avtotest_POM/scripts/baseline.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_baseline.py`

**Interfeyslar:**
- Consumes: Vazifa 4 dan `action_stats`/`ActionStat`, Vazifa 5 dan `selector_evidence`/`SelectorStat`
- Produces:
  - `render_markdown(astats: dict, sstats: dict, summary: dict) -> str`
  - `main(argv: list[str] | None = None) -> int` — `<kun_papkasi>/BASELINE.md` va
    `<kun_papkasi>/baseline.json` yozadi, 0 qaytaradi

- [ ] **Qadam 1: Yiqiladigan testlarni yozish**

`tests/test_baseline.py` ga qo'shish:

```python
def test_render_markdown_action_va_selektor_jadvallarini_chiqaradi():
    astats = {"nav": baseline.ActionStat("nav", ok=10, fail=2)}
    astats["nav"].errors["selektor_topilmadi"] = 2
    sstats = {"smt-cell-header": baseline.SelectorStat("smt-cell-header", ok=180, applicable=200)}
    summary = {"kun": "2026-09-30", "regression_jami": 12, "health_jami": 200}

    md = baseline.render_markdown(astats, sstats, summary)

    assert "2026-09-30" in md
    assert "| `nav` | 10 | 2 |" in md
    assert "83%" in md          # nav muvaffaqiyat: 10/12
    assert "selektor_topilmadi" in md
    assert "| `smt-cell-header` | 180 | 200 | 90% |" in md


def test_render_markdown_bosh_malumotda_ham_ishlaydi():
    md = baseline.render_markdown({}, {}, {"kun": "2026-09-30", "regression_jami": 0, "health_jami": 0})

    assert "ma'lumot yo'q" in md


def test_render_markdown_ishonchsiz_probe_belgilanadi():
    """`.cdk-overlay-pane` uchun health.spec.js «ishlamadi» holatini yozmaydi —
    jadval uni ishonch o'lchovi sifatida ko'rsatmasligi kerak."""
    sstats = {".cdk-overlay-pane": baseline.SelectorStat(".cdk-overlay-pane", ok=12, applicable=12)}
    summary = {"kun": "2026-09-30", "regression_jami": 0, "health_jami": 12}

    md = baseline.render_markdown({}, sstats, summary)

    assert "| `.cdk-overlay-pane`\\* | 12 | 12 | 100% |" in md
    assert "ishlamadi" in md


def test_main_bosh_papkada_ham_fayllarni_yozadi(tmp_path):
    cases = tmp_path / "cases.json"
    cases.write_text(json.dumps({"cases": [
        {"id": "TC-1", "steps": [{"action": "nav"}, {"action": "assert_text"}]},
    ]}), encoding="utf-8")
    day = tmp_path / "2026-09-30"
    day.mkdir()
    (day / "regression.jsonl").write_text(
        '{"id": "TC-1", "result": "Fail", "failed_step": 2, "error": "matn yo\'q: X"}\n',
        encoding="utf-8")
    (day / "health.jsonl").write_text(
        '{"route": "/a/b_list", "list": {"title": "T", "heads": 5, "btns": ["Создать"]}}\n',
        encoding="utf-8")

    rc = baseline.main([str(day), "--cases", str(cases)])

    assert rc == 0
    md = (day / "BASELINE.md").read_text(encoding="utf-8")
    assert "| `nav` | 1 | 0 |" in md
    assert "| `assert_text` | 0 | 1 |" in md
    data = json.loads((day / "baseline.json").read_text(encoding="utf-8"))
    assert data["actions"]["assert_text"]["fail"] == 1
    assert data["selectors"]["smt-cell-header"]["ok"] == 1
```

- [ ] **Qadam 2: Testlarni yuritib, yiqilishini tasdiqlash**

```bash
pytest
```

Kutilgan: 4 ta yangi test FAIL — `AttributeError: … has no attribute 'render_markdown'`.

- [ ] **Qadam 3: Implementatsiya**

`scripts/baseline.py` boshiga `import argparse` qo'shish va fayl oxiriga qo'shish:

```python
DEFAULT_CASES = (Path(__file__).resolve().parents[2]
                 / "SmartUp_Autotest" / "data" / "regression_cases.json")

# Bu selektorlar uchun "ishlamadi" holati QAYD ETILMAYDI: health.spec.js tegishli kalitni
# faqat natija bo'sh bo'lmaganda yozadi (`if (menu.length && ...) rec.createMenu = ...`).
# Ya'ni ularning ishonch foizi doim 100% chiqadi va hech narsani isbotlamaydi.
NO_NEGATIVE_EVIDENCE = {".cdk-overlay-pane"}


def _pct(x):
    return "%d%%" % round(x * 100)


def render_markdown(astats, sstats, summary):
    """Faza 1 da o'qish uchun mo'ljallangan baseline jadvali."""
    lines = [
        "# Faza 0 baseline — %s" % summary["kun"],
        "",
        "Manba: `regression.jsonl` (%d qator) va `health.jsonl` (%d qator)."
        % (summary["regression_jami"], summary["health_jami"]),
        "",
        "## Action lug'ati — nima ishlaydi",
        "",
        "| Action | Ishladi | Yiqildi | Muvaffaqiyat | Asosiy sabab |",
        "|---|---|---|---|---|",
    ]
    if astats:
        for stat in sorted(astats.values(), key=lambda s: (-s.fail, -s.total)):
            reason = stat.errors.most_common(1)[0][0] if stat.errors else "—"
            lines.append("| `%s` | %d | %d | %s | %s |"
                         % (stat.action, stat.ok, stat.fail, _pct(stat.success_rate), reason))
    else:
        lines.append("| — | — | — | — | ma'lumot yo'q |")

    lines += [
        "",
        "## a2 selektorlari — bilvosita dalil",
        "",
        "Bu isbot emas, ko'rsatkich. Ishonch past bo'lsa Faza 1 da qo'lda tekshiriladi.",
        "",
        "| Selektor | Ishladi | Tegishli sahifa | Ishonch |",
        "|---|---|---|---|",
    ]
    if sstats:
        for stat in sorted(sstats.values(), key=lambda s: s.confidence):
            mark = "\\*" if stat.selector in NO_NEGATIVE_EVIDENCE else ""
            lines.append("| `%s`%s | %d | %d | %s |"
                         % (stat.selector, mark, stat.ok, stat.applicable, _pct(stat.confidence)))
    else:
        lines.append("| — | — | — | ma'lumot yo'q |")

    if any(s in NO_NEGATIVE_EVIDENCE for s in sstats):
        lines += ["",
                  "\\* — bu selektor uchun «ishlamadi» holati qayd etilmaydi: `health.spec.js`",
                  "tegishli kalitni faqat natija bo'sh bo'lmaganda yozadi. Foiz bu yerda «necha",
                  "sahifada uchradi» degani, «qanchalik ishonchli» degani EMAS."]

    lines += ["", "## Faza 1 uchun xulosa", "",
              "- Muvaffaqiyati 80% dan past action lar `pages/components/` da qayta yoziladi.",
              "- Ishonchi 80% dan past selektorlar `pages/ui/a2.py` ga kiritilishdan oldin qo'lda tekshiriladi.",
              "- `action_yozilmagan` sababi — Faza 2 da yoziladigan action lar ro'yxati.", ""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Faza 0 baseline jadvali")
    parser.add_argument("day", help="Tungi natijalar kun papkasi")
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)

    day = Path(args.day)
    out = Path(args.out) if args.out else day
    out.mkdir(parents=True, exist_ok=True)

    reg_rows = load_jsonl(day / "regression.jsonl")
    health_rows = load_jsonl(day / "health.jsonl")
    cases = load_cases(args.cases)

    astats = action_stats(reg_rows, cases)
    sstats = selector_evidence(health_rows)
    summary = {"kun": day.name,
               "regression_jami": len(reg_rows),
               "health_jami": len(health_rows)}

    payload = {
        "summary": summary,
        "actions": {name: {"ok": s.ok, "fail": s.fail,
                           "success_rate": round(s.success_rate, 3),
                           "errors": dict(s.errors)}
                    for name, s in astats.items()},
        "selectors": {name: {"ok": s.ok, "applicable": s.applicable,
                             "confidence": round(s.confidence, 3)}
                      for name, s in sstats.items()},
    }
    (out / "baseline.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "BASELINE.md").write_text(
        render_markdown(astats, sstats, summary), encoding="utf-8")
    print("Yozildi: %s/BASELINE.md" % out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Qadam 4: Testlarni yuritib, o'tishini tasdiqlash**

```bash
pytest
```

Kutilgan: `35 passed`.

- [ ] **Qadam 5: Commit**

```bash
git add scripts/baseline.py tests/test_baseline.py
git commit -m "$(cat <<'EOF'
feat(faza0): baseline hisoboti (BASELINE.md + baseline.json) va CLI

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 7: JS muhitini tayyorlash va login sinovi

> **Diqqat:** bu vazifada real serverga ulanish bor. Parolni **faqat foydalanuvchi**
> kiritadi (CLAUDE.md 4-qoida). `3_Avtotest/SmartUp_Autotest/` kodiga o'zgartirish kiritilmaydi.

**Fayllar:**
- Modify: yo'q (faqat yuritish)
- Create: `3_Avtotest/Tungi_natijalar/_faza0_login/auth.json` (yuritish natijasi)

**Interfeyslar:**
- Consumes: yo'q
- Produces: `3_Avtotest/SmartUp_Autotest/.auth/admin.json` — keyingi vazifalar shu sessiyadan foydalanadi

- [ ] **Qadam 1: Node paketlari va Chromium o'rnatish**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/SmartUp_Autotest
npm install --no-audit --no-fund
npx playwright install chromium
```

Kutilgan: `node_modules/` to'ladi, Chromium yuklanadi (~150 MB).

- [ ] **Qadam 2: Keychain'da admin paroli bor-yo'qligini tekshirish**

```bash
security find-generic-password -s smartup-xtrade -a mohir@xan >/dev/null 2>&1 \
  && echo "parol bor" || echo "parol YO'Q — foydalanuvchi qo'shishi kerak"
```

- [ ] **Qadam 3: Parol yo'q bo'lsa — foydalanuvchidan so'rash**

Parol yo'q bo'lsa, foydalanuvchiga shu buyruqni **o'zi** yuritishini ayting
(terminalda `!` prefiksi bilan — parol interaktiv so'raladi va ekranda ko'rinmaydi):

```
! cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/SmartUp_Autotest && bash scripts/add_password.sh admin
```

Parol kiritilguncha keyingi qadamga o'tilmaydi. Parolni hech qachon o'zingiz kiritmang,
so'ramang va hech qayerga yozmang.

- [ ] **Qadam 4: Login sinovini yuritish**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/SmartUp_Autotest
RESULTS_DIR="$(cd .. && pwd)/Tungi_natijalar/_faza0_login" npx playwright test --project=setup
```

Kutilgan: `1 passed` (admin). Qolgan 3 rol `config/roles.json` da `enabled: false` —
ular `skip` bo'ladi.

- [ ] **Qadam 5: Natijani tasdiqlash**

```bash
cat ../Tungi_natijalar/_faza0_login/auth.json
ls -la .auth/
```

Kutilgan: `auth.json` da `"admin": {"ok": true, ...}`, `.auth/admin.json` mavjud.

Login yiqilsa — `../Tungi_natijalar/_faza0_login/shots/AUTH-admin.png` ni ko'ring va
**to'xtang**: sabab noto'g'ri parol, tarmoq, yoki login sahifasi o'zgargan bo'lishi mumkin.
Uchala holatda ham foydalanuvchidan so'rash kerak, o'zingiz urinib ko'rmang.

- [ ] **Qadam 6: Commit qilinmaydi**

Bu vazifa `Avtotest_POM/` ga fayl qo'shmaydi. `.auth/` va natija papkalari git'ga tushmaydi.

---

### Vazifa 8: Health (smoke) ni real serverda yuritish

**Fayllar:**
- Create: `3_Avtotest/Tungi_natijalar/<sana>/health.jsonl` (yuritish natijasi)

**Interfeyslar:**
- Consumes: Vazifa 7 dan `.auth/admin.json`
- Produces: `health.jsonl` — Vazifa 5 dagi `selector_evidence` uchun kirish ma'lumoti

- [ ] **Qadam 1: Avval bitta modulda sinab ko'rish**

226 route ~1.5–2 soat oladi. Avval bitta kichik modulda ishlashini tasdiqlang:

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/SmartUp_Autotest
DATE=$(TZ=Asia/Tashkent date +%F)
RESULTS_DIR="$(cd .. && pwd)/Tungi_natijalar/$DATE" \
  MODULES="Оборудование" npx playwright test --project=health --no-deps
```

Kutilgan: 10 ta test yuriladi (`routes.json` da `Оборудование` — 10 route), `health.jsonl` paydo bo'ladi.
Hammasi `ERROR` bo'lsa — to'xtang va sababni aniqlang, to'liq yugurishga o'tmang.

- [ ] **Qadam 2: `health.jsonl` tuzilishini tasdiqlash**

```bash
DATE=$(TZ=Asia/Tashkent date +%F)
head -1 "../Tungi_natijalar/$DATE/health.jsonl" | python3 -m json.tool | head -30
```

Kutilgan: `module`, `name`, `route`, `status`, `list` kalitlari bor. `list.heads` va
`list.btns` bo'sh bo'lmasligi kerak — bu a2 selektorlari ishlayotganini bildiradi.

- [ ] **Qadam 3: To'liq health ni yuritish**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/SmartUp_Autotest
DATE=$(TZ=Asia/Tashkent date +%F)
RESULTS_DIR="$(cd .. && pwd)/Tungi_natijalar/$DATE" \
  caffeinate -dims npx playwright test --project=health --no-deps
```

Kutilgan: 226 test, ~1.5–2 soat. Ba'zilari `BUG`/`ERROR` bo'lishi **normal** — Faza 0
ning maqsadi aynan shuni o'lchash.

- [ ] **Qadam 4: Natijani sanash**

```bash
DATE=$(TZ=Asia/Tashkent date +%F)
python3 -c "
import json, collections, sys
rows = [json.loads(l) for l in open('../Tungi_natijalar/$DATE/health.jsonl', encoding='utf-8') if l.strip()]
print('jami:', len(rows))
print(collections.Counter(r.get('status') for r in rows))
"
```

Kutilgan: jami ~226. `OK` + `BUG` yig'indisi `ERROR` dan sezilarli ko'p bo'lishi kerak.
Agar `ERROR` 50% dan oshsa — sessiya tugagan yoki selektorlar mos kelmagan; to'xtang va
`shots/` dagi skrinshotlarni ko'ring.

---

### Vazifa 9: Regression ni real serverda yuritish

**Fayllar:**
- Create: `3_Avtotest/Tungi_natijalar/<sana>/regression.jsonl` (yuritish natijasi)

**Interfeyslar:**
- Consumes: Vazifa 7 dan `.auth/admin.json`
- Produces: `regression.jsonl` — Vazifa 4 dagi `action_stats` uchun kirish ma'lumoti

- [ ] **Qadam 1: Avval bitta modulda sinab ko'rish**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/SmartUp_Autotest
DATE=$(TZ=Asia/Tashkent date +%F)
RESULTS_DIR="$(cd .. && pwd)/Tungi_natijalar/$DATE" \
  MODULES="Оборудование" npx playwright test --project=regression --no-deps
```

Kutilgan: `Оборудование` moduli 34 case. `regression.jsonl` ga Pass/Fail/Skip yoziladi.

- [ ] **Qadam 2: To'liq regression ni yuritish**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/SmartUp_Autotest
DATE=$(TZ=Asia/Tashkent date +%F)
RESULTS_DIR="$(cd .. && pwd)/Tungi_natijalar/$DATE" \
  caffeinate -dims npx playwright test --project=regression --no-deps
```

Kutilgan: 858 test (548 yuriladi, 310 `Skip`), ~3–5 soat.

**Muhim:** bu yugurish real ma'lumot yaratadi. `regression_cases.json` dagi case'lar
`QA-` prefiksli yozuvlar bilan ishlaydi — begona yozuvni o'zgartiradigan case'lar
allaqachon `auto: false` qilib belgilangan (28 ta). Yugurishdan keyin yaratilgan
`QA-` yozuvlarni o'chirish shart emas: keyingi yugurishlar ularni qayta ishlatadi.

- [ ] **Qadam 3: Natijani sanash**

```bash
DATE=$(TZ=Asia/Tashkent date +%F)
python3 -c "
import json, collections
rows = [json.loads(l) for l in open('../Tungi_natijalar/$DATE/regression.jsonl', encoding='utf-8') if l.strip()]
print('jami:', len(rows))
print(collections.Counter(r.get('result') for r in rows))
"
```

Kutilgan: jami ~858, `Skip` ~310. `Pass` va `Fail` nisbati Faza 0 ning asosiy natijasi —
qanday chiqsa ham to'g'ri, uni o'lchash maqsad edi.

---

### Vazifa 10: Baseline jadvalini chiqarish va Faza 1 ga xulosa

**Fayllar:**
- Create: `3_Avtotest/Tungi_natijalar/<sana>/BASELINE.md` (analizator natijasi)
- Create: `3_Avtotest/Tungi_natijalar/<sana>/baseline.json`
- Create: `3_Avtotest/Hujjatlar/<sana>-faza0-natija.md` (xulosa; `<sana>` — yugurish sanasi)

**Interfeyslar:**
- Consumes: Vazifa 6 dan `baseline.main`, Vazifa 8–9 dan `health.jsonl` va `regression.jsonl`
- Produces: Faza 1 rejasining kirish ma'lumoti — qaysi selektor/action ishonchli, qaysisi yo'q

- [ ] **Qadam 1: Analizatorni real natijaga yuritish**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/Avtotest_POM
source .venv/bin/activate
DATE=$(TZ=Asia/Tashkent date +%F)
python3 scripts/baseline.py "../Tungi_natijalar/$DATE"
```

Kutilgan: `Yozildi: ../Tungi_natijalar/<sana>/BASELINE.md`

- [ ] **Qadam 2: Jadvalni ko'rish**

```bash
DATE=$(TZ=Asia/Tashkent date +%F)
cat "../Tungi_natijalar/$DATE/BASELINE.md"
```

- [ ] **Qadam 3: Mavjud `analyze.py` ni ham yuritish (bug nomzodlari uchun)**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/SmartUp_Autotest
DATE=$(TZ=Asia/Tashkent date +%F)
python3 scripts/analyze.py "../Tungi_natijalar/$DATE"
```

Kutilgan: shu papkada `SUMMARY.md` va `candidates.json`. Bu Faza 0 ning qo'shimcha
foydasi: yugurish yangi buglarni ham topadi.

- [ ] **Qadam 4: Xulosa hujjatini yozish**

`3_Avtotest/Hujjatlar/<sana>-faza0-natija.md` fayliga quyidagi bo'limlar bilan:

1. **Yugurish ma'lumoti** — sana, davomiyligi, health/regression jami va natija taqsimoti
2. **Action jadvali** — `BASELINE.md` dan ko'chirilgan, 80% dan past bo'lganlari ajratilgan
3. **Selektor jadvali** — `BASELINE.md` dan, past ishonchlilari ajratilgan
4. **Faza 1 ga kiradigan qarorlar** — har bir past ko'rsatkichli action/selektor uchun:
   POM da qanday yoziladi (qayta yozish / ALIAS qo'shish / qo'lda tekshirish)
5. **Topilgan yangi buglar** — `candidates.json` dan `YANGI` statusdagilar; ular
   `1_Smoke_2026-09-28/Buglar/<modul>/` ga hisobot sifatida yoziladi

- [ ] **Qadam 5: Commit**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/Avtotest_POM
git add -A
git commit -m "$(cat <<'EOF'
docs(faza0): baseline natijalari va Faza 1 uchun xulosa

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Qadam 6: Faza 0 chiqish mezonini tekshirish**

Spec `§5 Faza 0` bo'yicha chiqish mezoni: *"har bir `smt.js` selektori uchun
'ishlaydi / ishlamaydi / noma'lum' belgisi bor jadval"*.

Tasdiqlash:

```bash
DATE=$(TZ=Asia/Tashkent date +%F)
python3 -c "
import json
d = json.load(open('../Tungi_natijalar/$DATE/baseline.json', encoding='utf-8'))
print('selektorlar:', len(d['selectors']), '· actionlar:', len(d['actions']))
noaniq = [k for k, v in d['selectors'].items() if v['applicable'] == 0]
print('noma\'lum (dalil yo\'q):', noaniq or 'yo\'q')
"
```

Kutilgan: 6 ta selektor va 20+ action jadvalda. `applicable == 0` bo'lganlar
"noma'lum" deb belgilanadi va Faza 1 da qo'lda tekshiriladi.

---

## Faza 0 tugagach

Natija: `BASELINE.md` jadvali + xulosa hujjati. Faza 1 (poydevor) rejasi shu jadval
asosida yoziladi — `pages/ui/a2.py` ga faqat ishonchi tasdiqlangan selektorlar kiradi,
qolganlari uchun qo'lda tekshirish vazifalari qo'shiladi.
