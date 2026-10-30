# Faza 2 — JSON case'larni POM poydevorida yuritish

> **Ijrochi agentlar uchun:** MAJBURIY SUB-SKILL: `superpowers:subagent-driven-development`
> (tavsiya) yoki `superpowers:executing-plans` — rejani vazifa-vazifa bajaring.
> Qadamlar `- [ ]` katakcha sintaksisida.

**Maqsad:** `regression_cases.json` dagi 548 auto case'ni Faza 1 POM poydevorida yuritadigan
ijrochi qurish; assert'siz 245 case'ga `expected` matnidan assert generatsiya qilish; har
yiqilish uchun Jira'ga tayyor dalil (skrinshot, trace, qadam jurnali) yozish.

**Arxitektura:** JSON case'lar o'zgarmaydi — o'zgaruvchi faqat IJROCHI. `runner/actions.py`
31 ta action'ni POM chaqiruvlariga aylantiradi; POM komponentlari brauzer bilan gaplashadi.
Ijrochi natijani `regression.jsonl` ga **Faza 0 dagi AYNAN O'SHA formatda** yozadi, shuning
uchun mavjud `scripts/analyze.py` va `scripts/bug_report.py` o'zgarishsiz ishlaydi.

**Texnologiya:** Python 3.9, pytest 8.4.2, playwright (Python) 1.60, `tests/fake_page.py`
(brauzersiz test), `pytest-playwright` 0.7.1.

**Spetsifikatsiya:** `2026-09-29-pom-birlashtirish-design.md` (Faza 2 bo'limi)
**Faza 0 natijasi:** `2026-09-29-faza0-natija.md`
**Faza 1 rejasi:** `2026-09-30-faza1-poydevor-reja.md`

---

## Nima uchun bu faza aynan shunday

Faza 0 mavjud JS avtotestni bir marta real serverda yugurtirib o'lchadi. Xulosa:
**selektorlar sog'lom, muammo action qatlamida.** Selektor ishonchi 93–100%, lekin
`assert_buttons` 21%, `assert_api` 34%, `grid_fill` 0%, `menu_plus` 0%.

Faza 0 topgan 6 ta nuqsonning HAMMASI bir turda edi: hech narsa tashlamaydi, hech narsa
logga yozmaydi va natijani **doim optimistik tomonga og'diradi**. Eng yomoni: `expect.soft`
istisno tashlamagani uchun 548 tadan 173 ta natija (32%) noto'g'ri «Pass» deb yozilgan.

Faza 1 yakuniy sharhi shu naqshni poydevorda yana topdi: 74 mutatsiyadan 22 tasi tutilmagan,
overlay'da panelning markazi bosilardi, `Form.field()` fon sahifasini to'ldirardi, xato
faqat oyna ichida qidirilardi. Hammasi tuzatildi (206 test, 28/28 selektor mutatsiyada
tutiladi).

**Shuning uchun Faza 2 ning asosiy xavfi — soxta «Pass».** 548 case yuritiladi; agar
ijrochi bir joyda jimgina o'tib ketsa, natija ishonchsiz bo'ladi va butun ish behuda.

## Global Constraints

Bu talablar HAR vazifaga tegishli:

- `except Exception: pass` va unga o'xshash **jimgina yutuvchi kod TAQIQLANGAN**. Topilmasa
  xato tashlanadi. `.catch(() => {})` ekvivalentlari ham taqiqlanadi.
- **Hech narsa tasdiqlamaydigan assert — nuqson.** Ayniqsa: `if not value: return` naqshi
  (JS `assert_text` da aynan shu bor edi) TAQIQLANADI — qiymat bo'sh bo'lsa xato tashlanadi.
- **Yiqilish o'rniga SKIP berish TAQIQLANADI**, faqat case'ning o'zi `auto=false` bo'lsa
  yoki `manual` action bo'lsa skip qilinadi (aniq sabab bilan).
- Selektor matni faqat `UiDriver` da yashaydi. Komponent yoki ijrochi ichida qattiq yozilgan
  CSS/XPath selektor TAQIQLANADI. Yangi selektor kerak bo'lsa `UiDriver` ga maydon
  qo'shiladi VA `tests/test_ui_driver.py` dagi `A2_KUTILGAN` / `BIRUNI_KUTILGAN`
  lug'atlariga aniq qiymati yoziladi (aks holda ikkinchi test yiqiladi).
- Kod **«zakaz» emas «order»** deb nomlanadi (foydalanuvchi qoidasi).
- Izohlar, hujjatlar, commit xabarlari va xato matnlari **o'zbek tilida**. SmartUp UI
  matnlari (rus tilidagi tugma/ustun nomlari) o'z holida qoladi.
- `3_Avtotest/SmartUp_Autotest/` ga **TEGMA** — faqat o'qish (`data/*.json`).
  `Avtotest_POM/` dan tashqariga yozma.
- Parol/token kodga, hujjatga, logga yoki commit'ga **yozilmasin** — faqat
  `3_Avtotest/.env` dan o'qiladi (`SMARTUP_PW_ADMIN`).
- Har commit oxirida: `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`
- Boshlang'ich holat: **206 passed, 3 skipped**. Har vazifadan keyin butun to'plam o'tishi
  shart, son faqat oshadi.
- Mutatsiya isboti majburiy: har tuzatish/yangi mantiq uchun uni vaqtincha buzganda yangi
  test YIQILISHI ko'rsatilsin. Mutatsiya albatta qaytariladi.
- Bu muhitda Python bytecode loyihadan tashqarida keshlanadi va bir xil o'lchamdagi tez
  tahrirlar eski bytecode bilan noto'g'ri natija bergani kuzatilgan. Mutatsiya
  tekshiruvlarini `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -p no:cacheprovider` bilan
  yurit.

## O'lchangan faktlar (rejaga asos)

Bu sonlar `SmartUp_Autotest/data/regression_cases.json` dan hozir hisoblangan:

| Nima | Son |
|---|---|
| Jami case | 858 |
| `auto=true` | 548 |
| `auto=false` (qo'lda/xavfli) | 310 |
| Xil action | 31 |
| Auto case qadamlari | 2362 |
| Qadamda `expected` matni bor | 2188 (93%) |
| Assert qadami YO'Q auto case | **245** (45%) |

Action chastotasi (auto va non-auto birga):

| Action | Son | Action | Son | Action | Son |
|---|---|---|---|---|---|
| `nav` | 831 | `confirm` | 84 | `pick` | 13 |
| `click` | 819 | `assert_field` | 62 | `toggle` | 10 |
| `row_click` | 346 | `tab` | 55 | `menu_plus` | 7 |
| `manual` | 300 | `grid_fill` | 48 | `radio` | 6 |
| `row_action` | 272 | `sequence` | 41 | `open_url` | 6 |
| `assert_api` | 212 | `assert_row` | 33 | `assert_download` | 3 |
| `assert_text` | 171 | `fill_date` | 30 | `assert_value` | 3 |
| `fill` | 164 | `multiselect` | 26 | `assert_no_request` | 2 |
| `assert_buttons` | 147 | `observe` | 16 | `assert_disabled` | 1 |
| `assert_columns` | 145 | | | `dialog_close` | 1 |
| `select` | 127 | | | `remove_tag` | 1 |

Case'ning JSON shakli (kalitlar aynan shular):

```json
{
  "id": "TC-GL-FIL-002", "module": "Главное", "section": "Организации",
  "form": "Организации — ro'yxat", "title": "Qator bosilganda amal tugmalari chiqadi",
  "type": "UI", "priority": "P3", "seq": 2, "phase": "P01",
  "last_result": "Pass", "last_bug": "", "auto": true, "skip_reason": "",
  "steps": [
    {"action": "nav", "target": "Главное > Организации",
     "value": "/xtrade/a2/anor/mr/filial_list",
     "description": "Yuqori qora menyuda «Главное» ni bosing, ...",
     "expected": "«Организации» sahifasi ochiladi."}
  ]
}
```

Qadam kalitlari: `action`, `target`, `value`, `description`, `expected`, `ops`
(`ops` faqat `sequence` da).

## Faza 1 dan olingan ogohlantirishlar — qaysi vazifa yopadi

| # | Ogohlantirish | Vazifa |
|---|---|---|
| 1 | Tasdiqlash (assert) qatlami yo'q | 3 |
| 2 | Har test uchun yangi brauzer — 548 case uchun sekin, zanjirni buzadi | 11 |
| 3 | Yiqilish dalili avtomatik biriktirilmaydi | 10 |
| 4 | Qayta login yo'q — sessiya daqiqalarda tugaydi | 9 |
| 5 | Eski UI (BIRUNI) qoplamasi kam | 13 |
| 6 | `GenericPage` `route=None` — forma route'ni qayerdan oladi | 1 |
| 7 | `PYTHONDONTWRITEBYTECODE=1` tungi skriptga kerak | 11 |
| 8 | `save_data`/`load_data` kalitlari tozalanmaydi | 1 |

## Fayl tuzilmasi

Yangi `runner/` paketi — bu KUTUBXONA kodi, test emas. Spetsifikatsiya
`tests/json_driven/actions.py` deydi, lekin bu loyihada `tests/` faqat testlarni saqlaydi,
shuning uchun ijrochi `runner/` ga qo'yiladi. Bu ataylab chetlanish.

| Fayl | Mas'uliyati |
|---|---|
| `runner/__init__.py` | bo'sh |
| `runner/cases.py` | JSON o'qish, tartiblash, filtrlash |
| `runner/actions.py` | 31 action → POM chaqiruvlari (dispatcher) |
| `runner/record.py` | `regression.jsonl` yozuvi (Faza 0 formati) |
| `pages/components/assertions.py` | sahifa darajasidagi tasdiqlashlar |
| `utils/network.py` | tarmoq so'rovlarini yig'uvchi (`assert_api` uchun) |
| `utils/session.py` | login va qayta login |
| `utils/evidence.py` | skrinshot, trace, qadam jurnali |
| `scripts/generate_asserts.py` | `expected` dan assert generatsiya qilish |
| `tests/test_regression.py` | 548 case'ni yuritadigan parametrlangan test |
| `data/regression_cases.json` | generatsiyadan keyingi case'lar (yangi fayl) |

`pages/base_page.py` 100 qator chegarasida qoladi — sahifa darajasidagi assert'lar
`assertions.py` ga chiqariladi va `BasePage.expect` xossasi orqali beriladi.

---

### Vazifa 1: `runner/cases.py` — case'larni o'qish, tartiblash, filtrlash

**Fayllar:**
- Create: `runner/__init__.py` (bo'sh), `runner/cases.py`
- Test: `tests/test_runner_cases.py`

**Interfeyslar:**
- Consumes: hech narsa (mustaqil)
- Produces:
  - `Case` — `namedtuple`: `id, module, section, form, title, type, priority, seq, phase, last_result, last_bug, auto, skip_reason, steps`
  - `load_cases(path) -> list[Case]` — `phase`, keyin `seq` bo'yicha tartiblangan
  - `filter_cases(cases, ids=None, modules=None, types=None, auto_only=False) -> list[Case]`
  - `case_id(case) -> str` — pytest parametr identifikatori
  - `nav_route(case) -> str | None` — case'ning birinchi `nav` qadamidagi `value`

**Nega tartib muhim.** `run_order.json` tartibi ma'lumotnoma → hujjat bog'liqligini saqlaydi:
valyuta yaratilmasa, uni ishlatadigan hujjat case'i yiqiladi. Case'larda `phase` (`P01`…)
va `seq` maydonlari bor — tartib aynan shulardan chiqadi, alohida fayl kerak emas.

**Nega `nav_route` kerak.** Faza 1 sharhi so'radi: forma `route` ni qayerdan oladi?
Javob: `PageFactory` dan EMAS. Har case'ning birinchi `nav` qadamida `value` maydonida
to'liq route bor (masalan `/xtrade/a2/anor/mr/filial_list`). `GenericPage.route` `None`
bo'lib qoladi va `open()` route'siz chaqirilmaydi — navigatsiya doim `nav` orqali ketadi.
`nav_route` faqat DIAGNOSTIKA uchun: yiqilish yozuvida qaysi sahifa mo'ljallangani ko'rinadi.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_runner_cases.py`:

```python
# -*- coding: utf-8 -*-
import json

import pytest

from runner.cases import Case, case_id, filter_cases, load_cases, nav_route

XOM = {
    "generated": "2026-09-28",
    "cases": [
        {"id": "TC-B-002", "module": "Финансы", "section": "Валюты", "form": "Валюты",
         "title": "ikkinchi", "type": "UI", "priority": "P3", "seq": 2, "phase": "P02",
         "last_result": "Pass", "last_bug": "", "auto": True, "skip_reason": "",
         "steps": [{"action": "nav", "target": "Финансы > Валюты", "value": "/xtrade/a2/fin/cur"}]},
        {"id": "TC-A-001", "module": "Главное", "section": "Организации", "form": "Организации",
         "title": "birinchi", "type": "Smoke", "priority": "P1", "seq": 1, "phase": "P01",
         "last_result": "Fail", "last_bug": "BUG-7", "auto": True, "skip_reason": "",
         "steps": [{"action": "nav", "target": "Главное > Организации",
                    "value": "/xtrade/a2/anor/mr/filial_list"}]},
        {"id": "TC-C-003", "module": "Склад", "section": "Закупки", "form": "Закупка",
         "title": "qo'lda", "type": "Ijobiy", "priority": "P2", "seq": 1, "phase": "P03",
         "last_result": "Pass", "last_bug": "", "auto": False,
         "skip_reason": "haqiqiy pul harakati", "steps": []},
    ],
}


@pytest.fixture
def cases_fayli(tmp_path):
    yol = tmp_path / "regression_cases.json"
    yol.write_text(json.dumps(XOM, ensure_ascii=False), encoding="utf-8")
    return yol


def test_load_cases_phase_va_seq_boyicha_tartiblaydi(cases_fayli):
    """Tartib ma'lumotnoma → hujjat bog'liqligini saqlaydi: valyuta yaratilmasa
    uni ishlatadigan hujjat case'i yiqiladi."""
    cases = load_cases(cases_fayli)

    assert [c.id for c in cases] == ["TC-A-001", "TC-B-002", "TC-C-003"]
    assert isinstance(cases[0], Case)


def test_load_cases_barcha_maydonni_oqiydi(cases_fayli):
    c = load_cases(cases_fayli)[0]

    assert c.id == "TC-A-001" and c.module == "Главное" and c.section == "Организации"
    assert c.form == "Организации" and c.title == "birinchi" and c.type == "Smoke"
    assert c.priority == "P1" and c.seq == 1 and c.phase == "P01"
    assert c.last_result == "Fail" and c.last_bug == "BUG-7"
    assert c.auto is True and c.skip_reason == ""
    assert c.steps[0]["action"] == "nav"


def test_load_cases_yoq_fayl_xato_tashlaydi(tmp_path):
    """Jimgina bo'sh ro'yxat qaytarish TAQIQLANADI — butun yugurish «0 case, hammasi
    yashil» bo'lib ketardi."""
    with pytest.raises(FileNotFoundError):
        load_cases(tmp_path / "yoq.json")


def test_load_cases_bosh_royxat_xato_tashlaydi(tmp_path):
    yol = tmp_path / "bosh.json"
    yol.write_text(json.dumps({"cases": []}), encoding="utf-8")

    with pytest.raises(ValueError) as xato:
        load_cases(yol)

    assert "case yo'q" in str(xato.value)


def test_filter_auto_only(cases_fayli):
    cases = load_cases(cases_fayli)

    assert [c.id for c in filter_cases(cases, auto_only=True)] == ["TC-A-001", "TC-B-002"]


def test_filter_id_modul_va_tur_boyicha(cases_fayli):
    cases = load_cases(cases_fayli)

    assert [c.id for c in filter_cases(cases, ids=["TC-B-002"])] == ["TC-B-002"]
    assert [c.id for c in filter_cases(cases, modules=["Склад"])] == ["TC-C-003"]
    assert [c.id for c in filter_cases(cases, types=["Smoke"])] == ["TC-A-001"]


def test_filter_notogri_id_xato_tashlaydi(cases_fayli):
    """Xato yozilgan `CASES=` satri jimgina 0 case bermasligi kerak."""
    cases = load_cases(cases_fayli)

    with pytest.raises(ValueError) as xato:
        filter_cases(cases, ids=["TC-YOQ-999"])

    assert "TC-YOQ-999" in str(xato.value)


def test_case_id_modul_va_idni_beradi(cases_fayli):
    c = load_cases(cases_fayli)[0]

    assert case_id(c) == "P01-1-TC-A-001"


def test_nav_route_birinchi_nav_qadamidan_olinadi(cases_fayli):
    cases = load_cases(cases_fayli)

    assert nav_route(cases[0]) == "/xtrade/a2/anor/mr/filial_list"
    assert nav_route(cases[2]) is None   # qadamlari yo'q
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_runner_cases.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'runner'` — FAIL.

- [ ] **Qadam 3: `runner/cases.py` yozish**

`runner/__init__.py` — bo'sh fayl.

```python
# -*- coding: utf-8 -*-
"""JSON case'larni o'qish, tartiblash va filtrlash.

Case'lar `data/regression_cases.json` da yashaydi. Ijrochi ularni O'ZGARTIRMAYDI —
JSON qoladi, faqat ijrochi POM ga o'tadi (dizayn qarori).
"""
import collections
import json
from pathlib import Path

MAYDONLAR = ("id", "module", "section", "form", "title", "type", "priority", "seq",
             "phase", "last_result", "last_bug", "auto", "skip_reason", "steps")

Case = collections.namedtuple("Case", MAYDONLAR)


def load_cases(path):
    """`path` dan case'larni o'qib `phase`, keyin `seq` bo'yicha tartiblangan ro'yxat beradi.

    Fayl yo'q bo'lsa `FileNotFoundError`, case'lar bo'sh bo'lsa `ValueError`.
    Jimgina bo'sh ro'yxat qaytarish TAQIQLANADI: butun yugurish «0 case, hammasi
    yashil» bo'lib ketardi va hech kim sezmasdi.
    """
    xom = json.loads(Path(path).read_text(encoding="utf-8"))
    royxat = xom.get("cases") or []
    if not royxat:
        raise ValueError("Faylda case yo'q: %s" % path)
    cases = [Case(**{m: c.get(m, "" if m != "steps" else []) for m in MAYDONLAR})
             for c in royxat]
    return sorted(cases, key=lambda c: (str(c.phase), int(c.seq or 0), c.id))


def filter_cases(cases, ids=None, modules=None, types=None, auto_only=False):
    """Filtrlaydi. Berilgan `ids` dan birortasi topilmasa `ValueError`.

    Xato yozilgan `CASES=TC-XATO` satri jimgina 0 case bermasligi kerak — QA
    «hammasi o'tdi» deb o'ylab qolardi.
    """
    natija = list(cases)
    if auto_only:
        natija = [c for c in natija if c.auto]
    if modules:
        natija = [c for c in natija if c.module in modules]
    if types:
        natija = [c for c in natija if c.type in types]
    if ids:
        bor = {c.id for c in cases}
        yoq = [i for i in ids if i not in bor]
        if yoq:
            raise ValueError("Bunday case yo'q: %s" % ", ".join(yoq))
        natija = [c for c in natija if c.id in ids]
    return natija


def case_id(case):
    """pytest parametr identifikatori: tartib ko'rinib turishi uchun phase va seq bilan."""
    return "%s-%s-%s" % (case.phase, case.seq, case.id)


def nav_route(case):
    """Case'ning birinchi `nav` qadamidagi route (`value`) yoki `None`.

    Faqat DIAGNOSTIKA uchun: yiqilish yozuvida qaysi sahifa mo'ljallangani ko'rinadi.
    Navigatsiyaning o'zi `nav` action orqali ketadi, `BasePage.open()` orqali emas —
    shuning uchun `GenericPage.route` `None` bo'lib qolishi muammo emas.
    """
    for s in case.steps:
        if s.get("action") == "nav" and s.get("value"):
            return s["value"]
    return None
```

- [ ] **Qadam 4: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_runner_cases.py -v && .venv/bin/pytest
```

Kutilgan: `10 passed`; butun to'plam `216 passed, 3 skipped`.

- [ ] **Qadam 5: Haqiqiy fayl bilan tekshirish (aqldan tekshirish)**

```bash
.venv/bin/python -c "
from runner.cases import load_cases, filter_cases
c = load_cases('../SmartUp_Autotest/data/regression_cases.json')
a = filter_cases(c, auto_only=True)
print('jami', len(c), '· auto', len(a), '· birinchi', c[0].phase, c[0].seq, c[0].id)
"
```

Kutilgan: `jami 858 · auto 548`. Boshqa son chiqsa — to'xta va xabar ber.

- [ ] **Qadam 6: Commit**

```bash
git add runner/ tests/test_runner_cases.py
git commit -m "$(cat <<'EOF'
feat(faza2): case'larni o'qish, tartiblash va filtrlash

Tartib `phase` + `seq` dan chiqadi — ma'lumotnoma → hujjat bog'liqligi
saqlanadi. Bo'sh fayl va noto'g'ri `CASES=` satri XATO tashlaydi: jimgina
0 case «hammasi yashil» bo'lib ketardi.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 2: `utils/network.py` — tarmoq va konsol kuzatuvchisi

**Fayllar:**
- Create: `utils/network.py`
- Test: `tests/test_network.py`

**Interfeyslar:**
- Consumes: hech narsa
- Produces:
  - `Collector(page)` — `reset()`, `bad: list[dict]` (`{"status": int, "url": str}`),
    `console: list[str]`, `i18n_404() -> list[str]`, `http_errors() -> list[dict]`

**Nega kerak.** `assert_api` — 212 marta uchraydigan ikkinchi eng ko'p assert, va Faza 0 da
uning muvaffaqiyati **34%**. U sahifada element qidirmaydi — case bajarilishi davomida
**yig'ilgan tarmoq javoblariga** qaraydi. Shuning uchun kuzatuvchi case boshida
`reset()` qilinishi shart, aks holda oldingi case'ning xatosi keyingisiga o'tadi.

Manba: `SmartUp_Autotest/lib/smt.js:50-60` (`attachCollectors`). Shartlar aynan
ko'chiriladi: `status >= 500`, YOKI `status >= 400` va URL da `/xtrade/b/`, YOKI
`status == 404` va URL da `i18n`. URL dan so'rov qatori va host olib tashlanadi.

**Nega `i18n_404` alohida.** Faza 0 aniqladi: «har modulda `+add.json 404`» — bu
ma'lum, global bug (`analyze.py` dagi `GLOBAL_KNOWN`). U ILOVA_BUG emas, shuning uchun
`assert_api` uni alohida xabar bilan beradi va `bug_report.py` uni `MALUM` toifasiga
soladi.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_network.py`:

```python
# -*- coding: utf-8 -*-
from utils.network import Collector


class FakeResponse:
    def __init__(self, url, status):
        self._url = url
        self._status = status

    def url(self):
        return self._url

    def status(self):
        return self._status


class FakeConsoleMessage:
    def __init__(self, tur, matn):
        self._type = tur
        self._text = matn

    def type(self):
        return self._type

    def text(self):
        return self._text


class FakeEventPage:
    """`page.on(...)` ni yozib oladigan eng kichik taqlidchi."""

    def __init__(self):
        self.handlers = {}

    def on(self, hodisa, fn):
        self.handlers.setdefault(hodisa, []).append(fn)

    def emit(self, hodisa, arg):
        for fn in self.handlers.get(hodisa, []):
            fn(arg)


def test_500_yigiladi():
    page = FakeEventPage()
    col = Collector(page)

    page.emit("response", FakeResponse("https://app3.greenwhite.uz/xtrade/b/anor/save?x=1", 500))

    assert col.bad == [{"status": 500, "url": "/xtrade/b/anor/save"}]


def test_400_faqat_b_yolida_yigiladi():
    """`/xtrade/b/` — server API si. Boshqa 4xx (masalan statik fayl) bug emas."""
    page = FakeEventPage()
    col = Collector(page)

    page.emit("response", FakeResponse("https://app3.greenwhite.uz/xtrade/b/anor/x", 403))
    page.emit("response", FakeResponse("https://app3.greenwhite.uz/assets/logo.png", 404))

    assert [b["status"] for b in col.bad] == [403]


def test_i18n_404_alohida_beriladi():
    """Faza 0: «har modulda +add.json 404» — ma'lum global bug, ilova bug'i emas."""
    page = FakeEventPage()
    col = Collector(page)

    page.emit("response", FakeResponse("https://app3.greenwhite.uz/xtrade/a2/x/i18n/add.json", 404))

    assert col.i18n_404() == ["/xtrade/a2/x/i18n/add.json"]
    assert col.http_errors() == []


def test_http_errors_i18ni_chiqarib_tashlaydi():
    page = FakeEventPage()
    col = Collector(page)

    page.emit("response", FakeResponse("https://app3.greenwhite.uz/xtrade/b/a", 500))
    page.emit("response", FakeResponse("https://app3.greenwhite.uz/x/i18n/b.json", 404))

    assert [e["status"] for e in col.http_errors()] == [500]


def test_200_yigilmaydi():
    page = FakeEventPage()
    col = Collector(page)

    page.emit("response", FakeResponse("https://app3.greenwhite.uz/xtrade/b/ok", 200))

    assert col.bad == []


def test_konsol_xatosi_yigiladi_ogohlantirish_yoq():
    page = FakeEventPage()
    col = Collector(page)

    page.emit("console", FakeConsoleMessage("error", "TypeError: x"))
    page.emit("console", FakeConsoleMessage("warning", "eskirgan"))
    page.emit("pageerror", Exception("Uncaught ReferenceError"))

    assert col.console == ["TypeError: x", "Uncaught ReferenceError"]


def test_reset_hammasini_tozalaydi():
    """Case boshida tozalanmasa oldingi case'ning xatosi keyingisini yiqitadi."""
    page = FakeEventPage()
    col = Collector(page)
    page.emit("response", FakeResponse("https://app3.greenwhite.uz/xtrade/b/a", 500))
    page.emit("console", FakeConsoleMessage("error", "x"))

    col.reset()

    assert col.bad == [] and col.console == []


def test_uzun_konsol_xabari_kesiladi():
    page = FakeEventPage()
    col = Collector(page)

    page.emit("console", FakeConsoleMessage("error", "x" * 500))

    assert len(col.console[0]) == 200
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_network.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'utils.network'` — FAIL.

- [ ] **Qadam 3: `utils/network.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Case bajarilishi davomida tarmoq javoblari va konsol xatolarini yig'adi.

Manba: `SmartUp_Autotest/lib/smt.js:50-60` (`attachCollectors`). Shartlar aynan
ko'chirildi. `assert_api` 212 marta uchraydi va Faza 0 da muvaffaqiyati 34% edi —
u sahifada element qidirmaydi, aynan shu yig'ilgan ma'lumotga qaraydi.
"""
import re

HOST = re.compile(r"^https?://[^/]+")
SERVER_API = re.compile(r"/xtrade/b/")
I18N = re.compile(r"i18n")
XABAR_CHEGARASI = 200


def _qisqa_url(url):
    """So'rov qatori va host olib tashlanadi — yozuvlar taqqoslanadigan bo'lishi uchun."""
    return HOST.sub("", str(url).split("?")[0])


class Collector:
    """`page` hodisalariga ulanadi. Har case boshida `reset()` chaqirilishi SHART."""

    def __init__(self, page):
        self.bad = []
        self.console = []
        page.on("response", self._javob)
        page.on("pageerror", lambda e: self._konsol(str(e)))
        page.on("console", self._konsol_xabari)

    def _javob(self, r):
        status = r.status()
        url = _qisqa_url(r.url())
        yomon = (status >= 500
                 or (status >= 400 and SERVER_API.search(url))
                 or (status == 404 and I18N.search(url)))
        if yomon:
            self.bad.append({"status": status, "url": url})

    def _konsol_xabari(self, m):
        if m.type() == "error":
            self._konsol(m.text())

    def _konsol(self, matn):
        self.console.append(str(matn)[:XABAR_CHEGARASI])

    def reset(self):
        """Case boshida tozalaydi. Busiz oldingi case'ning xatosi keyingisini yiqitadi."""
        self.bad = []
        self.console = []

    def i18n_404(self):
        """«+add.json 404» turidagi tarjima fayli xatolari — Faza 0 aniqlagan global bug."""
        return [b["url"] for b in self.bad
                if b["status"] == 404 and I18N.search(b["url"])]

    def http_errors(self):
        """Haqiqiy server xatolari — `i18n 404` lardan tashqari."""
        return [b for b in self.bad
                if not (b["status"] == 404 and I18N.search(b["url"]))]
```

- [ ] **Qadam 4: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_network.py -v && .venv/bin/pytest
```

Kutilgan: `8 passed`; butun to'plam `224 passed, 3 skipped`.

- [ ] **Qadam 5: Mutatsiya isboti**

`SERVER_API` ni `re.compile(r"/hech-qachon/")` ga o'zgartir, yurit — `test_400_faqat_b_yolida_yigiladi`
yiqilishi kerak. `reset()` tanasini `pass` ga o'zgartir — `test_reset_hammasini_tozalaydi`
yiqilishi kerak. Ikkalasini ham qaytar.

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -p no:cacheprovider tests/test_network.py
```

- [ ] **Qadam 6: Commit**

```bash
git add utils/network.py tests/test_network.py
git commit -m "$(cat <<'EOF'
feat(faza2): tarmoq va konsol kuzatuvchisi

`assert_api` 212 marta uchraydi va Faza 0 da muvaffaqiyati 34% edi. U
sahifada element qidirmaydi — case davomida yig'ilgan tarmoq javoblariga
qaraydi, shuning uchun har case boshida `reset()` shart.

`i18n 404` alohida beriladi: Faza 0 uni global ma'lum bug deb aniqlagan,
ilova bug'i emas.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 3: tasdiqlash (assert) qatlami

**Fayllar:**
- Create: `pages/components/assertions.py`
- Modify: `pages/base_page.py` (`expect` xossasi), `pages/components/grid.py`
  (`expect_row`, `expect_count`), `pages/components/report.py`
  (`expect_required_errors`)
- Test: `tests/test_assertions.py`, `tests/test_components_grid.py` (qo'shiladi)

**Interfeyslar:**
- Consumes: Faza 1 dan `find_button(page, driver, text, scope=None, exact=False, aliases=True)`,
  `ButtonNotFound`, `UiDriver.error_container`, `UiDriver.required_error`,
  `BasePage.main`, `BasePage.heading()`
- Produces:
  - `AssertionFailed(AssertionError)` — barcha tasdiqlash xatolari uchun umumiy tur
  - `Assertions(page, driver, main_getter)` — `text(*items)`, `heading(expected)`,
    `buttons(*names)`, `url(pattern)`, `toast(pattern)`, `disabled(name)`, `enabled(name)`
  - `BasePage.expect` → `Assertions`
  - `Grid.expect_row(*cells)`, `Grid.expect_count(expected)`
  - `Report.expect_required_errors(minimum=1)`

**Nega bu eng muhim vazifa.** Faza 1 sharhi ogohlantirdi: tasdiqlash qatlami bo'lmasa case
muallifi `grid.count()` ni yozadi, u `None` qaytaradi, shart `None` ga bardosh beradi va
soxta «Pass» chiqadi. Faza 0 da aynan shu turdagi nuqson 548 tadan 173 ta natijani (32%)
noto'g'ri «Pass» qilgan.

**Qat'iy qoida — bo'sh tasdiqlash TAQIQLANADI.** JS `assert_text` da shunday edi:

```js
async assert_text(page, s) {
  if (!s.value) return;   // ← qiymat bo'sh bo'lsa JIMGINA o'tadi
```

Bizda bunday qadam `AssertionFailed` tashlaydi: tekshirmaydigan tasdiqlash — hech qanday
tasdiqlashdan YOMON, chunki u yashil belgi beradi.

**`text()` matnni qanday taqqoslaydi.** Sahifa matnidagi ketma-ket bo'shliqlar bitta
bo'shliqqa keltiriladi (`\s+` → `' '`), keyin har element `in` bilan qidiriladi. Bu
manbadagi (`smt.js` `assert_text`) xatti-harakat. Elementlarni tayyorlash (qavs ichini
tashlash, vergul bo'yicha bo'lish) ijrochining ishi, bu yerda emas — shuning uchun
`text()` **tayyor ro'yxat** oladi.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_assertions.py`:

```python
# -*- coding: utf-8 -*-
import pytest

from pages.components.assertions import AssertionFailed, Assertions
from pages.ui.a2 import A2
from tests.fake_page import FakePage


def _assertions(page, driver=A2):
    """`main_getter` — eng ustki `<main>` ni beruvchi funksiya (a2 da drawer OXIRGISI)."""
    return Assertions(page, driver, lambda: page.locator(driver.main).last)


def test_text_barcha_element_topilsa_otadi():
    page = FakePage(texts={"main >> last": "Организации  \n  Название   Код"})

    _assertions(page).text(["Организации", "Название"])


def test_text_topilmagan_elementni_nomlaydi():
    page = FakePage(texts={"main >> last": "Организации"})

    with pytest.raises(AssertionFailed) as xato:
        _assertions(page).text(["Организации", "Валюта", "Склад"])

    assert "Валюта" in str(xato.value) and "Склад" in str(xato.value)


def test_text_ketma_ket_boshliqni_bittaga_keltiradi():
    page = FakePage(texts={"main >> last": "Название    \n\n   Код"})

    _assertions(page).text(["Название Код"])


def test_text_bosh_royxat_XATO_tashlaydi():
    """JS `assert_text` da `if (!s.value) return;` bor edi — tekshirmaydigan
    tasdiqlash yashil belgi beradi, bu hech qanday tasdiqlashdan YOMON."""
    page = FakePage(texts={"main >> last": "hamma narsa"})

    with pytest.raises(AssertionFailed) as xato:
        _assertions(page).text([])

    assert "tekshiriladigan matn berilmadi" in str(xato.value)


def test_heading_mos_kelsa_otadi():
    page = FakePage(texts={"main >> last >> h1, h2, [role=heading]": "Организации"})

    _assertions(page).heading("Организации")


def test_heading_mos_kelmasa_ikkalasini_korsatadi():
    page = FakePage(texts={"main >> last >> h1, h2, [role=heading]": "Валюты"})

    with pytest.raises(AssertionFailed) as xato:
        _assertions(page).heading("Организации")

    assert "Организации" in str(xato.value) and "Валюты" in str(xato.value)


def test_buttons_hammasi_korinsa_otadi():
    kalit = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
             "[role=option]:visible >> filter(has_text='Создать') >> first")
    page = FakePage(counts={kalit: 1})

    _assertions(page).buttons(["Создать"])


def test_buttons_topilmagan_tugmani_nomlaydi():
    """Faza 0: `assert_buttons` muvaffaqiyati 21% — eng ko'p yiqiladigan assert.
    Shuning uchun xabar QAYSI tugma yo'qligini aniq aytishi shart."""
    page = FakePage(counts={})

    with pytest.raises(AssertionFailed) as xato:
        _assertions(page).buttons(["Создать", "Удалить"])

    assert "Создать" in str(xato.value) and "Удалить" in str(xato.value)


def test_buttons_bosh_royxat_XATO_tashlaydi():
    page = FakePage(counts={})

    with pytest.raises(AssertionFailed):
        _assertions(page).buttons([])


def test_url_naqsh_mos_kelsa_otadi():
    page = FakePage(url="https://app3.greenwhite.uz/xtrade/a2/anor/mr/filial%2Badd")

    _assertions(page).url("filial")


def test_url_mos_kelmasa_hozirgi_urlni_korsatadi():
    page = FakePage(url="https://app3.greenwhite.uz/xtrade/a2/fin/cur")

    with pytest.raises(AssertionFailed) as xato:
        _assertions(page).url("filial")

    assert "/fin/cur" in str(xato.value)


def test_toast_xato_joyidan_qaraydi():
    """`error_container` oynadan KENGROQ: a2 xatoni snackbar bilan ham ko'rsatadi."""
    page = FakePage(texts={A2.error_container: "Ошибка ORA-00001: unique constraint"})

    _assertions(page).toast("ORA-00001")


def test_toast_topilmasa_xato_joyidagi_matnni_korsatadi():
    page = FakePage(texts={A2.error_container: "Сохранено"})

    with pytest.raises(AssertionFailed) as xato:
        _assertions(page).toast("Ошибка")

    assert "Сохранено" in str(xato.value)


def test_disabled_tugma_nofaol_bolsa_otadi():
    kalit = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
             "[role=option]:visible >> filter(has_text='Сохранить') >> first")
    page = FakePage(counts={kalit: 1}, attrs={(kalit, "disabled"): "true"})

    _assertions(page).disabled("Сохранить")


def test_disabled_tugma_faol_bolsa_yiqiladi():
    kalit = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
             "[role=option]:visible >> filter(has_text='Сохранить') >> first")
    page = FakePage(counts={kalit: 1}, attrs={})

    with pytest.raises(AssertionFailed) as xato:
        _assertions(page).disabled("Сохранить")

    assert "faol" in str(xato.value)


def test_enabled_tugma_nofaol_bolsa_yiqiladi():
    kalit = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
             "[role=option]:visible >> filter(has_text='Сохранить') >> first")
    page = FakePage(counts={kalit: 1}, attrs={(kalit, "disabled"): "true"})

    with pytest.raises(AssertionFailed) as xato:
        _assertions(page).enabled("Сохранить")

    assert "nofaol" in str(xato.value)
```

`tests/test_components_grid.py` oxiriga qo'shiladi:

```python
def test_expect_row_har_katakni_ketma_ket_filtrlaydi():
    from pages.components.assertions import AssertionFailed

    kalit = ("main >> last >> .smt-data-row >> filter(has_text='QA-1') "
             ">> filter(has_text='Активный') >> first")
    page = FakePage(counts={kalit: 1})

    Grid(page, A2).expect_row(["QA-1", "Активный"])


def test_expect_row_topilmasa_barcha_katakni_korsatadi():
    from pages.components.assertions import AssertionFailed

    page = FakePage(counts={})

    with pytest.raises(AssertionFailed) as xato:
        Grid(page, A2).expect_row(["QA-1", "Активный"])

    assert "QA-1" in str(xato.value) and "Активный" in str(xato.value)


def test_expect_row_bosh_royxat_XATO_tashlaydi():
    from pages.components.assertions import AssertionFailed

    page = FakePage(counts={})

    with pytest.raises(AssertionFailed):
        Grid(page, A2).expect_row([])


def test_expect_count_mos_kelsa_otadi():
    page = FakePage(counts={"main >> last >> .smt-data-row": 3})

    Grid(page, A2).expect_count(3)


def test_expect_count_mos_kelmasa_ikki_sonni_korsatadi():
    from pages.components.assertions import AssertionFailed

    page = FakePage(counts={"main >> last >> .smt-data-row": 3})

    with pytest.raises(AssertionFailed) as xato:
        Grid(page, A2).expect_count(2)

    assert "2" in str(xato.value) and "3" in str(xato.value)
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_assertions.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'pages.components.assertions'` — FAIL.

- [ ] **Qadam 3: `pages/components/assertions.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Sahifa darajasidagi tasdiqlashlar.

Nega alohida fayl: `BasePage` 100 qator chegarasida qoladi (Faza 1 qoidasi), va sahifa
darajasidagi tasdiqlashlar bitta mas'uliyat.

QAT'IY QOIDA — bo'sh tasdiqlash TAQIQLANADI. JS `assert_text` da `if (!s.value) return;`
bor edi: qiymat bo'sh bo'lsa qadam JIMGINA o'tardi va yashil belgi berardi. Tekshirmaydigan
tasdiqlash hech qanday tasdiqlashdan YOMON. Faza 0 da shu turdagi nuqson 548 tadan 173 ta
natijani (32%) noto'g'ri «Pass» qilgan.
"""
import re

from pages.components.buttons import ButtonNotFound, find_button

HEADING = "h1, h2, [role=heading]"


class AssertionFailed(AssertionError):
    """Tasdiqlash bajarilmadi. `AssertionError` dan meros — pytest odatdagidek ko'rsatadi."""


def _bosh_emas(royxat, nima):
    """Bo'sh ro'yxat bilan tasdiqlashga urinish — nuqson, jimgina o'tish emas."""
    toza = [str(x).strip() for x in (royxat or []) if str(x).strip()]
    if not toza:
        raise AssertionFailed("Tasdiqlash uchun tekshiriladigan matn berilmadi (%s)" % nima)
    return toza


def _siqilgan(matn):
    """Ketma-ket bo'shliqlarni bittaga keltiradi — manba `smt.js` shunday taqqoslaydi."""
    return re.sub(r"\s+", " ", matn or "").strip()


class Assertions:
    def __init__(self, page, driver, main_getter):
        self.page = page
        self.driver = driver
        self._main = main_getter

    @property
    def main(self):
        return self._main()

    def text(self, items):
        """Sahifada berilgan matnlarning HAMMASI borligini tekshiradi."""
        kutilgan = _bosh_emas(items, "text")
        bor = _siqilgan(self.main.inner_text())
        yoq = [x for x in kutilgan if x not in bor]
        if yoq:
            raise AssertionFailed(
                "Sahifada bu matnlar yo'q: %s · sahifada: «%s»"
                % (", ".join(yoq[:6]), bor[:200]))

    def heading(self, expected):
        """Sahifa sarlavhasi berilgan matnni o'z ichiga olishini tekshiradi."""
        kutilgan = _bosh_emas([expected], "heading")[0]
        bor = _siqilgan(self.main.locator(HEADING).first.inner_text())
        if kutilgan not in bor:
            raise AssertionFailed(
                "Sarlavha mos kelmadi: kutilgan «%s», sahifada «%s»" % (kutilgan, bor))

    def buttons(self, names):
        """Berilgan tugmalarning HAMMASI mavjudligini tekshiradi.

        Faza 0: `assert_buttons` muvaffaqiyati 21% — eng ko'p yiqiladigan assert.
        Shuning uchun xabar qaysi tugma yo'qligini ANIQ aytadi.
        """
        kutilgan = _bosh_emas(names, "buttons")
        yoq = []
        for nom in kutilgan:
            try:
                find_button(self.page, self.driver, nom, scope=self.main)
            except ButtonNotFound:
                yoq.append(nom)
        if yoq:
            raise AssertionFailed("Bu tugmalar topilmadi: %s" % ", ".join(yoq))

    def url(self, pattern):
        """Hozirgi manzil naqshga mos kelishini tekshiradi."""
        naqsh = _bosh_emas([pattern], "url")[0]
        hozir = getattr(self.page, "url", "") or ""
        if not re.search(naqsh, hozir):
            raise AssertionFailed(
                "Manzil naqshga mos kelmadi: naqsh «%s», hozir «%s»" % (naqsh, hozir))

    def toast(self, pattern):
        """Xato KO'RSATILADIGAN joyda (oyna VA toast/snackbar) matn borligini tekshiradi.

        `driver.error_container` oynadan kengroq: a2 xatoni snackbar bilan ham beradi.
        """
        naqsh = _bosh_emas([pattern], "toast")[0]
        bor = _siqilgan(self.page.locator(self.driver.error_container).inner_text())
        if not re.search(naqsh, bor, re.IGNORECASE):
            raise AssertionFailed(
                "Xabar topilmadi: naqsh «%s», xato joyida «%s»" % (naqsh, bor[:200]))

    def disabled(self, name):
        """Tugma nofaol ekanini tekshiradi."""
        nom = _bosh_emas([name], "disabled")[0]
        tugma = find_button(self.page, self.driver, nom, scope=self.main)
        if tugma.get_attribute("disabled") is None:
            raise AssertionFailed("«%s» tugmasi nofaol emas — faol" % nom)

    def enabled(self, name):
        """Tugma faol ekanini tekshiradi."""
        nom = _bosh_emas([name], "enabled")[0]
        tugma = find_button(self.page, self.driver, nom, scope=self.main)
        if tugma.get_attribute("disabled") is not None:
            raise AssertionFailed("«%s» tugmasi faol emas — nofaol" % nom)
```

- [ ] **Qadam 4: `BasePage.expect` xossasini qo'shish**

`pages/base_page.py` ga (boshqa komponent xossalari yonига):

```python
    @property
    def expect(self):
        """Sahifa darajasidagi tasdiqlashlar. `main` funksiya bo'lib uzatiladi, chunki
        drawer ochilganda eng ustki `<main>` o'zgaradi — qiymat bir marta olinmasligi kerak."""
        from pages.components.assertions import Assertions

        return Assertions(self.page, self.ui, lambda: self.main)
```

- [ ] **Qadam 5: `Grid.expect_row` va `Grid.expect_count` qo'shish**

`pages/components/grid.py` ga:

```python
    def expect_row(self, cells):
        """Berilgan kataklarning HAMMASINI o'z ichiga olgan qator borligini tekshiradi.

        Kataklar KETMA-KET filtrlanadi (manba `smt.js` `assert_row`): har filtr
        natijani toraytiradi, shuning uchun «QA-1» va «Активный» bitta qatorda
        bo'lishi shart, turli qatorlarda bo'lsa yetmaydi.
        """
        from pages.components.assertions import AssertionFailed, _bosh_emas

        kutilgan = _bosh_emas(cells, "expect_row")
        loc = self.main.locator(self.driver.rows)
        for katak in kutilgan:
            loc = loc.filter(has_text=katak)
        if loc.first.count() == 0:
            raise AssertionFailed(
                "Bu kataklar bilan qator topilmadi: %s" % " | ".join(kutilgan))

    def expect_count(self, expected):
        """Qatorlar soni aynan `expected` ekanini tekshiradi."""
        from pages.components.assertions import AssertionFailed

        bor = self.count()
        if bor != int(expected):
            raise AssertionFailed(
                "Qatorlar soni mos kelmadi: kutilgan %s, bor %s" % (expected, bor))
```

- [ ] **Qadam 6: `Report.expect_required_errors` qo'shish**

`pages/components/report.py` ga:

```python
    def expect_required_errors(self, minimum=1):
        """To'ldirilmagan majburiy maydonlar belgisi borligini tekshiradi.

        Validatsiya case'larining asosiy tasdiqlashi: bo'sh forma saqlanmasligi kerak.
        `driver.required_error` — a2 da `outline-error`, eski UI da `ng-invalid`.
        """
        from pages.components.assertions import AssertionFailed

        bor = self.required_errors()
        if bor < int(minimum):
            raise AssertionFailed(
                "Majburiy maydon xatosi kutilgan (kamida %s), topilgan %s — bo'sh forma "
                "saqlanib ketgan bo'lishi mumkin" % (minimum, bor))
```

- [ ] **Qadam 7: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_assertions.py tests/test_components_grid.py -v && .venv/bin/pytest
```

Kutilgan: butun to'plam `249 passed, 3 skipped`.

- [ ] **Qadam 8: Mutatsiya isboti (MAJBURIY, 4 mutatsiya)**

Har birini alohida qo'llab, yurit, keyin qaytar:

1. `_bosh_emas` tanasini `return [str(x) for x in (royxat or [])]` ga o'zgartir
   (bo'sh ro'yxat endi o'tadi) → `test_text_bosh_royxat_XATO_tashlaydi`,
   `test_buttons_bosh_royxat_XATO_tashlaydi`, `test_expect_row_bosh_royxat_XATO_tashlaydi`
   yiqilishi kerak.
2. `text()` da `yoq` hisoblashni `yoq = []` ga o'zgartir →
   `test_text_topilmagan_elementni_nomlaydi` yiqilishi kerak.
3. `expect_row` da halqani olib tashla (faqat birinchi katakni filtrla) →
   `test_expect_row_har_katakni_ketma_ket_filtrlaydi` yiqilishi kerak.
4. `toast()` da `self.driver.error_container` ni `self.driver.dialog` ga o'zgartir →
   `test_toast_xato_joyidan_qaraydi` yiqilishi kerak.

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -p no:cacheprovider
```

- [ ] **Qadam 9: Commit**

```bash
git add pages/components/assertions.py pages/base_page.py pages/components/grid.py \
        pages/components/report.py tests/test_assertions.py tests/test_components_grid.py
git commit -m "$(cat <<'EOF'
feat(faza2): tasdiqlash qatlami — bo'sh assert TAQIQLANADI

Faza 1 sharhi ogohlantirdi: tasdiqlash qatlami bo'lmasa case muallifi
`grid.count()` yozadi, u None qaytaradi, shart None ga bardosh beradi va
soxta «Pass» chiqadi.

Asosiy qoida: bo'sh ro'yxat bilan tasdiqlash XATO tashlaydi. JS
`assert_text` da `if (!s.value) return;` bor edi — tekshirmaydigan
tasdiqlash yashil belgi beradi, bu hech qanday tasdiqlashdan yomon.

`toast()` `error_container` dan qaraydi, `dialog` dan emas: a2 xatoni
snackbar bilan ham beradi.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 4: yetishmayotgan POM amallari — `tab`, `grid_fill`, `remove_tag`

**Fayllar:**
- Create: `pages/components/tabs.py`
- Modify: `pages/ui/driver.py` (2 yangi maydon), `pages/ui/a2.py`, `pages/ui/biruni.py`,
  `tests/test_ui_driver.py` (mixlangan lug'atlar), `pages/base_page.py` (`tabs` xossasi),
  `pages/components/grid.py` (`fill_cell`), `pages/components/form.py` (`remove_tag`)
- Test: `tests/test_components_tabs.py`, `tests/test_components_grid.py` (qo'shiladi),
  `tests/test_components_form.py` (qo'shiladi)

**Interfeyslar:**
- Consumes: `UiDriver`, `Grid.main`, `Grid.row(text)`, `Form.field(label)`
- Produces:
  - `UiDriver.tab: str`, `UiDriver.tag_remove: str`
  - `Tabs(page, driver)` — `open(name)`
  - `BasePage.tabs` → `Tabs`
  - `Grid.fill_cell(row_text, column, value)`
  - `Form.remove_tag(label, value)`

**Nega `click` uchun yangi metod YOZILMAYDI.** `find_button(page, driver, text)` allaqachon
funksiya — ijrochi uni to'g'ridan-to'g'ri chaqiradi. Ustiga `BasePage.click` o'ramini
qo'shish takrorlash bo'lardi va `base_page.py` ni 100 qator chegarasidan chiqarardi.

**Nega `grid_fill` muhim.** Faza 0 da muvaffaqiyati **0%** — 48 marta uchraydi va hech
qachon ishlamagan. Manba (`smt.js` `grid_fill`) ustun sarlavhalari ro'yxatini olib, mos
indeksni topadi va qatorning shu indeksdagi bolasini bosadi. Bu mantiq shu yerga ko'chiriladi
va **ustun topilmasa xato tashlanadi** (manbada `findIndex` `-1` qaytarsa `nth(-1)` oxirgi
katakka tushardi — jimgina noto'g'ri katak).

**Yangi drayver maydonlari.** `UiDriver` ga qo'shilgan har maydon
`tests/test_ui_driver.py` dagi `A2_KUTILGAN` va `BIRUNI_KUTILGAN` lug'atlariga ham
yozilishi SHART — aks holda `test_mixlangan_royxat_barcha_maydonni_qamraydi` yiqiladi.
Bu ataylab: Faza 1 da mixlanmagan maydonlar himoyasiz qolgan edi.

Qiymatlar:

| Maydon | A2 | BIRUNI |
|---|---|---|
| `tab` | `[role=tab]` | `.nav-tabs a, ul.nav li a` |
| `tag_remove` | `.mat-mdc-chip-remove, [matchipremove]` | `.tag .remove, .chip .close` |

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_components_tabs.py`:

```python
# -*- coding: utf-8 -*-
import pytest

from pages.components.tabs import TabNotFound, Tabs
from pages.ui.a2 import A2
from tests.fake_page import FakePage


def test_tab_role_boyicha_bosiladi():
    kalit = "main >> last >> [role=tab] >> filter(has_text='Комментарии') >> first"
    page = FakePage(counts={kalit: 1})

    Tabs(page, A2).open("Комментарии")

    assert page.clicked() == [kalit]


def test_tab_topilmasa_XATO_tashlaydi():
    """Manba `smt.js` da `.catch(() => btn(...))` bor edi — tab topilmasa jimgina
    tugma qidirardi va u ham topilmasa xato YO'QOLARDI."""
    page = FakePage(counts={})

    with pytest.raises(TabNotFound) as xato:
        Tabs(page, A2).open("Комментарии")

    assert "Комментарии" in str(xato.value)
```

`tests/test_components_grid.py` oxiriga:

```python
def test_fill_cell_ustun_indeksini_sarlavhadan_topadi():
    """Manba `smt.js` `grid_fill`: ustun sarlavhalari ro'yxatidan mos indeks topiladi,
    keyin qatorning SHU indeksdagi bolasi bosiladi va to'ldiriladi."""
    grid = "main >> last >> .smt-data-row >> first >> xpath=ancestor::*[.//smt-cell-header][1]"
    page = FakePage(
        lists={grid + " >> smt-cell-header": ["Товар", "Количество", "Цена"]},
        counts={grid + " >> .smt-data-row >> filter(has_text='QA-1') >> first": 1},
    )

    Grid(page, A2).fill_cell("QA-1", "Количество", "5")

    katak = grid + " >> .smt-data-row >> filter(has_text='QA-1') >> first >> :scope > * >> nth(1)"
    assert katak in page.clicked()
    assert (katak + " >> input", "5") in page.filled()


def test_fill_cell_ustun_topilmasa_XATO_tashlaydi():
    """Manbada `findIndex` -1 qaytarsa `nth(-1)` OXIRGI katakka tushardi —
    jimgina noto'g'ri katak to'ldirilardi."""
    from pages.components.grid import ColumnNotFound

    grid = "main >> last >> .smt-data-row >> first >> xpath=ancestor::*[.//smt-cell-header][1]"
    page = FakePage(lists={grid + " >> smt-cell-header": ["Товар", "Цена"]})

    with pytest.raises(ColumnNotFound) as xato:
        Grid(page, A2).fill_cell("QA-1", "Количество", "5")

    assert "Количество" in str(xato.value)
    assert "Товар" in str(xato.value), "xabar mavjud ustunlarni ham ko'rsatishi kerak"


def test_fill_cell_ustun_prefiks_boyicha_topiladi():
    """Sarlavha «Количество, шт» bo'lishi mumkin — case'da «Количество» yozilgan."""
    grid = "main >> last >> .smt-data-row >> first >> xpath=ancestor::*[.//smt-cell-header][1]"
    page = FakePage(
        lists={grid + " >> smt-cell-header": ["Товар", "Количество, шт"]},
        counts={grid + " >> .smt-data-row >> filter(has_text='QA-1') >> first": 1},
    )

    Grid(page, A2).fill_cell("QA-1", "Количество", "5")

    assert any("nth(1)" in k for k in page.clicked())
```

`tests/test_components_form.py` oxiriga:

```python
def test_remove_tag_maydon_ichidagi_tegni_ochiradi():
    maydon = ("main >> last >> label >> filter(has_text='Склады') >> first "
              ">> xpath=ancestor::*[.//input or .//textarea or .//smt-select-trigger "
              "or .//smt-data-select or .//*[@role=\"switch\"]][1]")
    kalit = (maydon + " >> filter(has_text='Основной') >> first >> "
             ".mat-mdc-chip-remove, [matchipremove] >> first")
    page = FakePage(counts={kalit: 1})

    Form(page, A2).remove_tag("Склады", "Основной")

    assert page.clicked() == [kalit]


def test_remove_tag_teg_topilmasa_XATO_tashlaydi():
    from pages.components.form import TagNotFound

    page = FakePage(counts={})

    with pytest.raises(TagNotFound) as xato:
        Form(page, A2).remove_tag("Склады", "Основной")

    assert "Основной" in str(xato.value)
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_components_tabs.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'pages.components.tabs'` — FAIL.

- [ ] **Qadam 3: Drayverga `tab` va `tag_remove` maydonlarini qo'shish**

`pages/ui/driver.py` da maydonlar ro'yxatiga (`required_error` dan keyin):

```python
    tab: str             # varaq (tab) sarlavhasi
    tag_remove: str      # ko'p tanlovli maydondagi tegni o'chirish tugmasi
```

`pages/ui/a2.py` da:

```python
    tab="[role=tab]",
    tag_remove=".mat-mdc-chip-remove, [matchipremove]",
```

`pages/ui/biruni.py` da:

```python
    tab=".nav-tabs a, ul.nav li a",
    tag_remove=".tag .remove, .chip .close",
```

`tests/test_ui_driver.py` da `A2_KUTILGAN` ga:

```python
    "tab": "[role=tab]",
    "tag_remove": ".mat-mdc-chip-remove, [matchipremove]",
```

`BIRUNI_KUTILGAN` ga:

```python
    "tab": ".nav-tabs a, ul.nav li a",
    "tag_remove": ".tag .remove, .chip .close",
```

- [ ] **Qadam 4: `pages/components/tabs.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Forma ichidagi varaqlar (tab)."""


class TabNotFound(RuntimeError):
    """Varaq topilmadi.

    Manba (`smt.js` `tab`) da `.catch(() => btn(page, s.target).click())` bor edi:
    varaq topilmasa jimgina tugma qidirilardi va u ham topilmasa xato YO'QOLARDI.
    """


class Tabs:
    def __init__(self, page, driver):
        self.page = page
        self.driver = driver

    @property
    def main(self):
        loc = self.page.locator(self.driver.main)
        return loc.last if self.driver.main_last else loc.first

    def open(self, name):
        """Nomi bo'yicha varaqni ochadi. Topilmasa `TabNotFound`."""
        varaq = self.main.locator(self.driver.tab).filter(has_text=name).first
        if varaq.count() == 0:
            raise TabNotFound(
                "Varaq topilmadi: «%s» (selektor: %s)" % (name, self.driver.tab))
        varaq.click()
```

- [ ] **Qadam 5: `BasePage.tabs` xossasini qo'shish**

```python
    @property
    def tabs(self):
        from pages.components.tabs import Tabs

        return Tabs(self.page, self.ui)
```

- [ ] **Qadam 6: `Grid.fill_cell` yozish**

`pages/components/grid.py` ga (fayl boshiga `ColumnNotFound` sinfi):

```python
class ColumnNotFound(RuntimeError):
    """Jadval ustuni sarlavhalar orasida topilmadi.

    Manba (`smt.js` `grid_fill`) da `findIndex` `-1` qaytarsa `nth(-1)` OXIRGI katakka
    tushardi — jimgina noto'g'ri katak to'ldirilardi. Faza 0 da bu action'ning
    muvaffaqiyati 0% edi (48 marta uchraydi).
    """
```

```python
    def _grid_of_rows(self):
        """Qatorlarni saqlovchi jadval elementi — ustun sarlavhalari shu yerda."""
        return (self.main.locator(self.driver.rows).first
                .locator("xpath=ancestor::*[.//%s][1]" % self.driver.header))

    def fill_cell(self, row_text, column, value):
        """Jadval ichidagi katakni to'ldiradi (masalan «Количество» ustuni).

        Ustun indeksi sarlavhalar ro'yxatidan topiladi. Sarlavha to'liqroq bo'lishi
        mumkin («Количество, шт»), shuning uchun PREFIKS bo'yicha solishtiriladi —
        manba `smt.js` ham `startsWith` ishlatadi.
        """
        grid = self._grid_of_rows()
        sarlavhalar = [h.strip() for h in grid.locator(self.driver.header).all_inner_texts()]
        indeks = next((i for i, h in enumerate(sarlavhalar) if h.startswith(column)), None)
        if indeks is None:
            raise ColumnNotFound(
                "Ustun topilmadi: «%s» · mavjud ustunlar: %s" % (column, ", ".join(sarlavhalar)))
        qator = grid.locator(self.driver.rows).filter(has_text=row_text).first
        katak = qator.locator(":scope > *").nth(indeks)
        katak.click()
        katak.locator("input").fill(str(value))
```

- [ ] **Qadam 7: `Form.remove_tag` yozish**

`pages/components/form.py` ga:

```python
class TagNotFound(RuntimeError):
    """Ko'p tanlovli maydonda o'chirilishi kerak bo'lgan teg topilmadi."""
```

```python
    def remove_tag(self, label, value):
        """Ko'p tanlovli maydondan bitta tegni o'chiradi."""
        teg = (self.field(label).filter(has_text=value).first
               .locator(self.driver.tag_remove).first)
        if teg.count() == 0:
            raise TagNotFound(
                "Teg topilmadi: maydon «%s», teg «%s»" % (label, value))
        teg.click()
```

- [ ] **Qadam 8: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest
```

Kutilgan: `256 passed, 3 skipped`. `test_mixlangan_royxat_barcha_maydonni_qamraydi`
o'tishi SHART — o'tmasa mixlangan lug'atlarga yangi maydonlar yozilmagan.

- [ ] **Qadam 9: Mutatsiya isboti**

1. `ColumnNotFound` tashlashni `indeks = -1` ga o'zgartir →
   `test_fill_cell_ustun_topilmasa_XATO_tashlaydi` yiqilishi kerak.
2. `startswith(column)` ni `== column` ga o'zgartir →
   `test_fill_cell_ustun_prefiks_boyicha_topiladi` yiqilishi kerak.
3. `TabNotFound` tashlashni olib tashla → `test_tab_topilmasa_XATO_tashlaydi` yiqilishi kerak.
4. `A2.tab` ni `"BUZUQ"` ga o'zgartir → mixlangan test yiqilishi kerak.

Hammasini qaytar.

- [ ] **Qadam 10: Commit**

```bash
git add pages/ pages/components/tabs.py tests/
git commit -m "$(cat <<'EOF'
feat(faza2): tab, grid_fill va remove_tag amallari

`grid_fill` Faza 0 da 0% muvaffaqiyat ko'rsatgan (48 marta uchraydi).
Sabab: manbada `findIndex` -1 qaytarsa `nth(-1)` OXIRGI katakka tushardi —
jimgina noto'g'ri katak to'ldirilardi. Endi ustun topilmasa
`ColumnNotFound` tashlanadi va xabar mavjud ustunlarni ko'rsatadi.

`tab` da manbadagi `.catch(() => btn(...))` olib tashlandi: varaq
topilmasa jimgina tugma qidirilardi va xato yo'qolardi.

Drayverga `tab` va `tag_remove` maydonlari qo'shildi va mixlangan
lug'atlarga ham yozildi.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 5: ijrochi skeleti va navigatsiya/o'zaro ta'sir action'lari

**Fayllar:**
- Create: `runner/actions.py`
- Test: `tests/test_actions_navigatsiya.py`

**Interfeyslar:**
- Consumes: `BasePage`, `find_button`, `Grid`, `Tabs`, `Menu.nav`, `Menu.menu_plus`,
  `utils.network.Collector`
- Produces:
  - `Ctx(page, pom, net, data)` — ijro konteksti
  - `ActionNotImplemented(RuntimeError)`
  - `ManualStep(Exception)` — `manual` action uchun (ijrochi uni `pytest.skip` ga aylantiradi)
  - `ACTIONS: dict[str, callable]` — `action` nomi → `fn(ctx, step)`
  - `run_step(ctx, step)` — bitta qadamni bajaradi
  - Bu vazifada yoziladigan action'lar: `nav`, `open_url`, `click`, `row_click`,
    `row_action`, `tab`, `menu_plus`, `wait`, `observe`, `manual`

**Nega dispatcher lug'at.** 31 action bor. `if/elif` zanjiri o'qilmaydi va yangi action
qo'shishda eskisi buzilishi mumkin. Lug'at bilan har action alohida funksiya — alohida
test qilinadi. Noma'lum action **xato tashlaydi**: Faza 0 da `menu_plus` yozilmagani uchun
7 case jimgina yiqilgan, lekin sabab «action yozilmagan» deb ko'rinmagan.

**`click` ning `confirm:` qo'shimchasi.** Manbada (`smt.js` `click`) `value` maydoni
`confirm:Oyna matni|Да` ko'rinishida bo'lishi mumkin — tugma bosilgandan keyin tasdiq
oynasi chiqadi. Bu naqsh 84 ta `confirm` action'dan tashqarida qo'shimcha yo'l. Manbada
u `.catch()` bilan o'ralgan edi («oyna chiqmasligi ham mumkin») — bizda oyna KUTILADI:
`confirm:` yozilgan bo'lsa oyna chiqishi shart, aks holda case noto'g'ri yozilgan.

**`row_click` ning «birinchi qator» holati.** `target` `birinchi qator (...)` bilan
boshlansa birinchi ko'rinadigan qator olinadi (346 marta uchraydigan action'da keng
tarqalgan naqsh). Aks holda matn bo'yicha qidiriladi. `«»` qo'shtirnoqlari tozalanadi.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_actions_navigatsiya.py`:

```python
# -*- coding: utf-8 -*-
import pytest

from pages.base_page import BasePage
from pages.ui.a2 import A2
from runner.actions import ActionNotImplemented, Ctx, ManualStep, run_step
from tests.fake_page import FakePage


def _ctx(page):
    """Ijro konteksti. `net` bu testlarda kerak emas — `None` beriladi va
    faqat `assert_api` uni talab qiladi."""
    return Ctx(page=page, pom=BasePage(page, A2), net=None, data={})


def _a2_page(**kw):
    """a2 aniqlanishi uchun `detect` selektorlaridan bittasi mavjud bo'lishi shart."""
    counts = dict(kw.pop("counts", {}))
    counts.setdefault(".smt-data-row", 1)
    return FakePage(counts=counts, **kw)


def test_nav_value_berilsa_togridan_togri_otadi():
    """Case'ning `nav` qadamida `value` — to'liq route. Menyu bosishdan tez va barqaror."""
    page = _a2_page()

    run_step(_ctx(page), {"action": "nav", "target": "Главное > Организации",
                          "value": "/xtrade/a2/anor/mr/filial_list"})

    assert ("goto", "/xtrade/a2/anor/mr/filial_list") in page.calls


def test_nav_value_yoq_bolsa_menyu_orqali_otadi():
    """Eski UI sahifalariga URL bilan borib bo'lmaydi — route'da sessiyaga bog'liq
    token bor. Shuning uchun `value` yo'q bo'lsa menyu ishlatiladi."""
    birinchi = ("button:visible, a:visible, [role=menuitem]:visible, [role=option]:visible "
                ">> filter(has_text=regex(^\\s*Продажа\\s*$)) >> first")
    oxirgi = ("button:visible, a:visible, [role=menuitem]:visible, [role=option]:visible "
              ">> filter(has_text=regex(^\\s*Заказы\\s*$)) >> first")
    page = _a2_page(counts={birinchi: 1, oxirgi: 1})

    run_step(_ctx(page), {"action": "nav", "target": "Продажа > Продажа > Заказы"})

    assert page.clicked() == [birinchi, oxirgi]


def test_nav_value_shablon_bolsa_menyu_orqali_otadi():
    """`value` da `<` bo'lsa u shablon (masalan `<id>`), haqiqiy route emas —
    manba `smt.js` shu shartni ishlatadi."""
    birinchi = ("button:visible, a:visible, [role=menuitem]:visible, [role=option]:visible "
                ">> filter(has_text=regex(^\\s*Главное\\s*$)) >> first")
    page = _a2_page(counts={birinchi: 1})

    run_step(_ctx(page), {"action": "nav", "target": "Главное",
                          "value": "/xtrade/a2/x/<id>/edit"})

    assert page.calls == [] or all(c[0] != "goto" for c in page.calls)


def test_open_url_targetga_otadi():
    page = _a2_page()

    run_step(_ctx(page), {"action": "open_url", "target": "/xtrade/a2/fin/cur"})

    assert ("goto", "/xtrade/a2/fin/cur") in page.calls


def test_click_tugmani_bosadi():
    kalit = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
             "[role=option]:visible >> filter(has_text='Создать') >> first")
    page = _a2_page(counts={kalit: 1})

    run_step(_ctx(page), {"action": "click", "target": "Создать"})

    assert kalit in page.clicked()


def test_click_confirm_qoshimchasi_bilan_oynani_tasdiqlaydi():
    """Manba `smt.js` `click`: `value` = `confirm:Oyna matni|Да`."""
    tugma = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
             "[role=option]:visible >> filter(has_text='Удалить') >> first")
    oyna = "[role=dialog] >> filter(has_text='Удалить запись') >> first"
    ha = oyna + " >> button:visible, a:visible, .btn:visible"
    page = _a2_page(counts={tugma: 1, oyna: 1})

    run_step(_ctx(page), {"action": "click", "target": "Удалить",
                          "value": "confirm:Удалить запись?|Да"})

    assert tugma in page.clicked()
    assert any("Удалить запись" in k for k in page.clicked()), "tasdiq oynasi bosilmadi"


def test_row_click_birinchi_qator_holati():
    kalit = "main >> last >> .smt-data-row:visible >> first"
    page = _a2_page(counts={kalit: 1, kalit + " >> .text-start": 1})

    run_step(_ctx(page), {"action": "row_click", "target": "birinchi qator (—)"})

    assert any(k.startswith(kalit) for k in page.clicked())


def test_row_click_matn_boyicha_qidiradi():
    kalit = "main >> last >> .smt-data-row >> filter(has_text='QA-1') >> first"
    page = _a2_page(counts={kalit: 1})

    run_step(_ctx(page), {"action": "row_click", "target": "«QA-1»"})

    assert any("QA-1" in k for k in page.clicked())


def test_row_action_qator_ichidan_qidiradi():
    """Faza 1 sharhi: `row_action` butun sahifadan qidirsa toolbar'dagi bir xil
    nomli «Удалить» bosiladi, qator amali emas."""
    qator = "main >> last >> .smt-data-row >> filter(has_text='QA-1') >> first"
    amal = (qator + " >> button:visible, a:visible, [role=menuitem]:visible, "
            "[role=option]:visible >> filter(has_text='Изменить') >> first")
    page = _a2_page(counts={qator: 1, amal: 1})
    ctx = _ctx(page)

    run_step(ctx, {"action": "row_click", "target": "«QA-1»"})
    run_step(ctx, {"action": "row_action", "target": "Изменить"})

    assert amal in page.clicked()


def test_tab_varaqni_ochadi():
    kalit = "main >> last >> [role=tab] >> filter(has_text='Комментарии') >> first"
    page = _a2_page(counts={kalit: 1})

    run_step(_ctx(page), {"action": "tab", "target": "Комментарии"})

    assert kalit in page.clicked()


def test_menu_plus_bosiladi():
    """Faza 0: `menu_plus` YOZILMAGAN edi — 7 case jimgina yiqilgan."""
    page = _a2_page(counts={'button[aria-label="Организации"] >> first': 1})

    run_step(_ctx(page), {"action": "menu_plus", "target": "Организации"})

    assert 'button[aria-label="Организации"] >> first' in page.clicked()


def test_wait_kutadi():
    page = _a2_page()

    run_step(_ctx(page), {"action": "wait", "value": "2"})

    assert ("wait_for_timeout", 2000) in page.calls


def test_observe_hech_narsa_qilmaydi():
    """`observe` — qo'lda kuzatish qadami. Hech narsa qilmaydi, lekin XATO ham
    tashlamaydi: case'ning qolgan qadamlari bajarilishi kerak."""
    page = _a2_page()

    run_step(_ctx(page), {"action": "observe", "description": "Ekranni kuzating"})

    assert page.clicked() == []


def test_manual_ManualStep_tashlaydi():
    """`manual` 300 marta uchraydi. U jimgina o'tmasligi kerak — ijrochi uni
    aniq sabab bilan SKIP ga aylantiradi."""
    page = _a2_page()

    with pytest.raises(ManualStep) as xato:
        run_step(_ctx(page), {"action": "manual", "description": "Chekni qo'lda tekshiring"})

    assert "Chekni qo'lda tekshiring" in str(xato.value)


def test_nomalum_action_XATO_tashlaydi():
    """Faza 0: yozilmagan action'lar jimgina yiqilgan, lekin sabab ko'rinmagan."""
    page = _a2_page()

    with pytest.raises(ActionNotImplemented) as xato:
        run_step(_ctx(page), {"action": "hech_qachon", "target": "x"})

    assert "hech_qachon" in str(xato.value)
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_actions_navigatsiya.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'runner.actions'` — FAIL.

- [ ] **Qadam 3: `runner/actions.py` skeletini va shu guruh action'larini yozish**

```python
# -*- coding: utf-8 -*-
"""JSON case qadamlarini POM chaqiruvlariga aylantiruvchi ijrochi.

31 ta action bor, shuning uchun dispatcher LUG'AT: har action alohida funksiya va
alohida test qilinadi. Noma'lum action XATO tashlaydi — Faza 0 da `menu_plus`
yozilmagani uchun 7 case jimgina yiqilgan, lekin sabab «action yozilmagan» deb
ko'rinmagan.
"""
import re

from pages.components.buttons import find_button

BIRINCHI_QATOR = re.compile(r"^birinchi qator", re.IGNORECASE)
QOSHTIRNOQ = re.compile(r"[«»\"]")
CONFIRM_QOSH = re.compile(r"^confirm:(.+)\|(.+)$")
SHABLON = "<"


class ActionNotImplemented(RuntimeError):
    """Bu action ijrochida yozilmagan."""


class ManualStep(Exception):
    """Qadam qo'lda bajarilishi kerak. Ijrochi buni aniq sabab bilan SKIP ga aylantiradi."""


class Ctx:
    """Bitta case'ning ijro konteksti.

    `net` — `utils.network.Collector` (faqat `assert_api` ishlatadi).
    `data` — case ichida qiymat uzatish uchun lug'at (`sequence` va zanjirlar uchun).
    `row` — oxirgi `row_click` tanlagan qator: `row_action` aynan shu qator ichidan
    qidiradi, aks holda toolbar'dagi bir xil nomli tugma bosiladi.
    """

    def __init__(self, page, pom, net, data):
        self.page = page
        self.pom = pom
        self.net = net
        self.data = data
        self.row = None


def _matn(step, kalit="target"):
    return QOSHTIRNOQ.sub("", str(step.get(kalit) or "")).strip()


def _nav(ctx, step):
    """Menyu orqali yoki to'g'ridan-to'g'ri route bilan o'tadi.

    `value` da `<` bo'lsa u shablon (`<id>`), haqiqiy route emas — manba `smt.js`
    shu shartni ishlatadi. Eski UI sahifalariga URL bilan borib bo'lmaydi (route'da
    sessiyaga bog'liq token bor), shuning uchun `value` yo'q bo'lsa menyu ishlatiladi.
    """
    route = step.get("value")
    if route and SHABLON not in str(route):
        ctx.pom.menu.nav(step.get("target"), route=route)
    else:
        ctx.pom.menu.nav(step.get("target"))


def _open_url(ctx, step):
    ctx.page.goto(_matn(step))


def _click(ctx, step):
    """Tugmani bosadi. `value` `confirm:Oyna matni|Tugma` bo'lsa oyna ham tasdiqlanadi.

    Manbada bu `.catch()` bilan o'ralgan edi («oyna chiqmasligi ham mumkin») — bizda
    oyna KUTILADI: `confirm:` yozilgan bo'lsa u chiqishi shart, aks holda case
    noto'g'ri yozilgan va buni bilish kerak.
    """
    find_button(ctx.page, ctx.pom.ui, step.get("target"), scope=ctx.pom.main).click()
    m = CONFIRM_QOSH.match(str(step.get("value") or ""))
    if m:
        ctx.pom.dialog.confirm(m.group(1), m.group(2))


def _row_click(ctx, step):
    """Qatorni bosadi va uni `ctx.row` ga eslab qoladi (keyingi `row_action` uchun)."""
    tgt = _matn(step)
    grid = ctx.pom.grid
    if BIRINCHI_QATOR.match(tgt):
        ctx.row = grid.first_row()
    else:
        ctx.row = grid.row(tgt)
    grid.click_row(tgt) if not BIRINCHI_QATOR.match(tgt) else ctx.row.click()


def _row_action(ctx, step):
    """Qator amalini bosadi — AYNAN `ctx.row` ichidan qidiriladi.

    Faza 1 sharhi: butun sahifadan qidirsak toolbar'dagi bir xil nomli «Удалить»
    bosiladi, qator amali emas.
    """
    ctx.pom.grid.row_action(step.get("target"), row=ctx.row)


def _tab(ctx, step):
    ctx.pom.tabs.open(step.get("target"))


def _menu_plus(ctx, step):
    ctx.pom.menu.menu_plus(step.get("target"))


def _wait(ctx, step):
    ctx.page.wait_for_timeout(int(float(step.get("value") or 1) * 1000))


def _observe(ctx, step):
    """Qo'lda kuzatish qadami — hech narsa qilmaydi, lekin XATO ham tashlamaydi:
    case'ning qolgan qadamlari bajarilishi kerak."""


def _manual(ctx, step):
    raise ManualStep(step.get("description") or step.get("target") or "qo'lda bajariladi")


ACTIONS = {
    "nav": _nav,
    "open_url": _open_url,
    "click": _click,
    "row_click": _row_click,
    "row_action": _row_action,
    "tab": _tab,
    "menu_plus": _menu_plus,
    "wait": _wait,
    "observe": _observe,
    "manual": _manual,
}


def run_step(ctx, step):
    """Bitta qadamni bajaradi. Action yozilmagan bo'lsa `ActionNotImplemented`."""
    nom = step.get("action")
    fn = ACTIONS.get(nom)
    if fn is None:
        raise ActionNotImplemented(
            "«%s» action ijrochida yozilmagan: %s"
            % (nom, step.get("description") or step.get("target") or ""))
    fn(ctx, step)
```

- [ ] **Qadam 4: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_actions_navigatsiya.py -v && .venv/bin/pytest
```

Kutilgan: `15 passed`; butun to'plam `271 passed, 3 skipped`.

- [ ] **Qadam 5: Mutatsiya isboti**

1. `run_step` dagi `ActionNotImplemented` ni `return` ga o'zgartir →
   `test_nomalum_action_XATO_tashlaydi` yiqilishi kerak.
2. `_row_action` da `row=ctx.row` ni olib tashla →
   `test_row_action_qator_ichidan_qidiradi` yiqilishi kerak.
3. `_nav` da `SHABLON not in str(route)` shartini olib tashla →
   `test_nav_value_shablon_bolsa_menyu_orqali_otadi` yiqilishi kerak.
4. `_click` da `confirm` bo'lagini olib tashla →
   `test_click_confirm_qoshimchasi_bilan_oynani_tasdiqlaydi` yiqilishi kerak.

Hammasini qaytar.

- [ ] **Qadam 6: Commit**

```bash
git add runner/actions.py tests/test_actions_navigatsiya.py
git commit -m "$(cat <<'EOF'
feat(faza2): ijrochi skeleti va navigatsiya action'lari

Dispatcher lug'at: 31 action bor, `if/elif` zanjiri o'qilmaydi va yangi
action qo'shishda eskisi buziladi. Noma'lum action XATO tashlaydi — Faza 0
da `menu_plus` yozilmagani uchun 7 case jimgina yiqilgan, lekin sabab
ko'rinmagan.

`row_action` aynan oxirgi `row_click` tanlagan qator ichidan qidiradi,
aks holda toolbar'dagi bir xil nomli tugma bosiladi.

`nav` da `value` shablon (`<id>`) bo'lsa menyu ishlatiladi. Eski UI
sahifalariga URL bilan borib bo'lmaydi — route'da sessiyaga bog'liq
token bor.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 6: forma kiritish action'lari

**Fayllar:**
- Modify: `runner/actions.py`
- Test: `tests/test_actions_forma.py`

**Interfeyslar:**
- Consumes: 5-vazifadan `Ctx`, `run_step`, `ACTIONS`; Faza 1 dan `Form.fill`,
  `Form.fill_date`, `Form.select`, `Form.multiselect`, `Form.toggle`, `Form.radio`;
  4-vazifadan `Grid.fill_cell`, `Form.remove_tag`
- Produces: `ACTIONS` ga qo'shiladi: `fill`, `fill_date`, `select`, `multiselect`,
  `toggle`, `radio`, `grid_fill`, `remove_tag`

**`toggle` ning qiymati.** Case'da `value` `on` yoki `off`. Faza 1 da `Form.toggle(label, on)`
mantiqiy qiymat oladi, shuning uchun ijrochi `value == "on"` ga aylantiradi. Boshqa
qiymat (`"1"`, `"true"`, bo'sh) kelsa **xato tashlanadi** — jimgina `off` deb qabul qilish
noto'g'ri holatda davom etishga olib keladi.

**`grid_fill` ning `target` formati.** `Qator matni | Ustun` — vertikal chiziq bilan
ajratilgan (manba `smt.js`). Ikki bo'lak bo'lmasa xato tashlanadi.

**`multiselect` ning `value` formati.** Vergul bilan ajratilgan ro'yxat. Bo'sh element
tashlab yuboriladi, lekin HAMMASI bo'sh bo'lsa xato tashlanadi.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_actions_forma.py`:

```python
# -*- coding: utf-8 -*-
import pytest

from pages.base_page import BasePage
from pages.ui.a2 import A2
from runner.actions import Ctx, run_step
from tests.fake_page import FakePage

AJDOD = ("xpath=ancestor::*[.//input or .//textarea or .//smt-select-trigger "
         "or .//smt-data-select or .//*[@role=\"switch\"]][1]")


def _ctx(page):
    return Ctx(page=page, pom=BasePage(page, A2), net=None, data={})


def _a2_page(**kw):
    counts = dict(kw.pop("counts", {}))
    counts.setdefault(".smt-data-row", 1)
    return FakePage(counts=counts, **kw)


def _maydon(yorliq):
    return ("main >> last >> label >> filter(has_text='%s') >> first >> %s"
            % (yorliq, AJDOD))


def test_fill_maydonni_toldiradi():
    page = _a2_page()

    run_step(_ctx(page), {"action": "fill", "target": "Название", "value": "QA-1"})

    assert (_maydon("Название") + " >> input, textarea >> first", "QA-1") in page.filled()


def test_fill_date_klavishlar_bilan_kiritiladi():
    """Maskali sana maydoni `fill()` ni qabul qilmaydi — manba `press('ControlOrMeta+A')`
    va `press_sequentially` ishlatadi."""
    page = _a2_page()

    run_step(_ctx(page), {"action": "fill_date", "target": "Дата", "value": "01.10.2026"})

    kalit = _maydon("Дата") + " >> input >> first"
    assert (kalit, "ControlOrMeta+A") in page.pressed()
    assert (kalit, "01.10.2026") in page.typed_sequentially()


def test_select_qiymatni_yozib_tanlaydi():
    """Manba: trigger bosiladi, qiymat YOZILADI (ro'yxat filtrlanadi), keyin variant
    bosiladi. To'g'ridan-to'g'ri bosish 1000+ variantli ro'yxatda ishlamaydi."""
    page = _a2_page()

    run_step(_ctx(page), {"action": "select", "target": "Валюта", "value": "UZS"})

    assert any("smt-select-trigger" in k for k in page.clicked())
    assert ("type", "UZS") in page.keyboard_calls()
    assert any(".cdk-overlay-pane" in k and "UZS" in k for k in page.clicked())


def test_multiselect_har_qiymatni_tanlaydi():
    page = _a2_page()

    run_step(_ctx(page), {"action": "multiselect", "target": "Склады",
                          "value": "Основной, Резервный"})

    yozilgan = [v for a, v in page.keyboard_calls() if a == "type"]
    assert yozilgan == ["Основной", "Резервный"]
    assert ("press", "Escape") in page.keyboard_calls()


def test_multiselect_bosh_qiymat_XATO_tashlaydi():
    page = _a2_page()

    with pytest.raises(ValueError) as xato:
        run_step(_ctx(page), {"action": "multiselect", "target": "Склады", "value": " , "})

    assert "Склады" in str(xato.value)


def test_toggle_on_yoqadi():
    kalit = _maydon("Активный") + " >> [role=switch], [role=checkbox], input[type=checkbox] >> first"
    page = _a2_page(counts={kalit: 1}, attrs={(kalit, "aria-checked"): "false"})

    run_step(_ctx(page), {"action": "toggle", "target": "Активный", "value": "on"})

    assert kalit in page.clicked()


def test_toggle_allaqachon_yoqilgan_bolsa_bosmaydi():
    kalit = _maydon("Активный") + " >> [role=switch], [role=checkbox], input[type=checkbox] >> first"
    page = _a2_page(counts={kalit: 1}, attrs={(kalit, "aria-checked"): "true"})

    run_step(_ctx(page), {"action": "toggle", "target": "Активный", "value": "on"})

    assert page.clicked() == []


def test_toggle_notogri_qiymat_XATO_tashlaydi():
    """Jimgina `off` deb qabul qilish noto'g'ri holatda davom etishga olib keladi."""
    page = _a2_page()

    with pytest.raises(ValueError) as xato:
        run_step(_ctx(page), {"action": "toggle", "target": "Активный", "value": "1"})

    assert "on" in str(xato.value) and "off" in str(xato.value)


def test_radio_qiymatni_bosadi():
    page = _a2_page()

    run_step(_ctx(page), {"action": "radio", "target": "Тип", "value": "Оптовый"})

    assert any("Оптовый" in k for k in page.clicked())


def test_grid_fill_qator_va_ustunni_ajratadi():
    grid = "main >> last >> .smt-data-row >> first >> xpath=ancestor::*[.//smt-cell-header][1]"
    page = _a2_page(
        lists={grid + " >> smt-cell-header": ["Товар", "Количество"]},
        counts={grid + " >> .smt-data-row >> filter(has_text='QA-tovar') >> first": 1},
    )

    run_step(_ctx(page), {"action": "grid_fill", "target": "QA-tovar | Количество",
                          "value": "5"})

    assert any("nth(1)" in k for k in page.clicked())


def test_grid_fill_vertikal_chiziq_yoq_bolsa_XATO_tashlaydi():
    page = _a2_page()

    with pytest.raises(ValueError) as xato:
        run_step(_ctx(page), {"action": "grid_fill", "target": "faqat qator", "value": "5"})

    assert "|" in str(xato.value)


def test_remove_tag_tegni_ochiradi():
    kalit = (_maydon("Склады") + " >> filter(has_text='Основной') >> first >> "
             ".mat-mdc-chip-remove, [matchipremove] >> first")
    page = _a2_page(counts={kalit: 1})

    run_step(_ctx(page), {"action": "remove_tag", "target": "Склады", "value": "Основной"})

    assert kalit in page.clicked()
```

- [ ] **Qadam 1b: `FakePage` ga uch yordamchi qo'shish**

Tekshirildi (2026-09-30): `tests/fake_page.py` da `clicked()` va `filled()` BOR, lekin
`pressed()`, `typed_sequentially()` va `keyboard_calls()` YO'Q. Ular `calls` ro'yxatini
filtrlaydi.

`tests/fake_page.py` dagi `FakePage` ga:

```python
    def pressed(self):
        """`(kalit, klavisha)` juftliklari — `press()` chaqiruvlari."""
        return [(k, v) for a, k, v in self.calls if a == "press"]

    def typed_sequentially(self):
        """`(kalit, matn)` juftliklari — `press_sequentially()` chaqiruvlari."""
        return [(k, v) for a, k, v in self.calls if a == "press_sequentially"]

    def keyboard_calls(self):
        """`("type"|"press", qiymat)` juftliklari — klaviatura chaqiruvlari."""
        return [(a.replace("keyboard_", ""), v) for a, v in
                ((c[0], c[1]) for c in self.calls if len(c) == 2)
                if a.startswith("keyboard_")]
```

**Diqqat:** `calls` ro'yxatidagi yozuvlarning shakli (uzunligi 2 yoki 3) `FakeLocator`
va `FakePage` metodlarida qanday yozilganiga bog'liq. Avval `tests/fake_page.py` ni
o'qib, `press`, `press_sequentially` va klaviatura chaqiruvlari `calls` ga QANDAY
yozilganini ko'r, keyin yordamchilarni shunga moslab yoz. Shakl mos kelmasa —
yordamchilarni moslashtir, `calls` ning shaklini O'ZGARTIRMA (mavjud testlar unga
tayanadi).

`tests/test_fake_page.py` ga uch yordamchi uchun test qo'sh — masalan:

```python
def test_pressed_press_chaqiruvlarini_beradi():
    page = FakePage()

    page.locator("#x").first.press("Tab")

    assert page.pressed() == [("#x >> first", "Tab")]


def test_typed_sequentially_press_sequentially_ni_beradi():
    page = FakePage()

    page.locator("#x").first.press_sequentially("01.10.2026")

    assert page.typed_sequentially() == [("#x >> first", "01.10.2026")]


def test_keyboard_calls_type_va_pressni_beradi():
    page = FakePage()

    page.keyboard.type("UZS")
    page.keyboard.press("Escape")

    assert page.keyboard_calls() == [("type", "UZS"), ("press", "Escape")]
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_actions_forma.py -v
```

Kutilgan: `KeyError` yoki `ActionNotImplemented: «fill» action ijrochida yozilmagan` — FAIL.

- [ ] **Qadam 3: Action'larni yozish**

`runner/actions.py` ga:

```python
def _royxat(qiymat, nima):
    """Vergul bilan ajratilgan ro'yxat. HAMMASI bo'sh bo'lsa xato — jimgina
    hech narsa qilmaslik tasdiqlanmagan «Pass» beradi."""
    bolaklar = [x.strip() for x in str(qiymat or "").split(",") if x.strip()]
    if not bolaklar:
        raise ValueError("«%s» uchun qiymat berilmadi: %r" % (nima, qiymat))
    return bolaklar


def _fill(ctx, step):
    ctx.pom.form.fill(step.get("target"), step.get("value"))


def _fill_date(ctx, step):
    ctx.pom.form.fill_date(step.get("target"), step.get("value"))


def _select(ctx, step):
    ctx.pom.form.select(step.get("target"), step.get("value"))


def _multiselect(ctx, step):
    ctx.pom.form.multiselect(step.get("target"),
                             _royxat(step.get("value"), step.get("target")))


def _toggle(ctx, step):
    """`value` faqat `on` yoki `off`. Boshqa qiymatda XATO: jimgina `off` deb qabul
    qilish noto'g'ri holatda davom etishga olib keladi."""
    qiymat = str(step.get("value") or "").strip().lower()
    if qiymat not in ("on", "off"):
        raise ValueError(
            "`toggle` uchun qiymat `on` yoki `off` bo'lishi kerak, berilgan: %r (maydon «%s»)"
            % (step.get("value"), step.get("target")))
    ctx.pom.form.toggle(step.get("target"), qiymat == "on")


def _radio(ctx, step):
    ctx.pom.form.radio(step.get("target"), step.get("value"))


def _grid_fill(ctx, step):
    """`target` formati: `Qator matni | Ustun` (manba `smt.js`)."""
    bolaklar = [x.strip() for x in str(step.get("target") or "").split("|")]
    if len(bolaklar) != 2 or not all(bolaklar):
        raise ValueError(
            "`grid_fill` uchun `target` «Qator | Ustun» ko'rinishida bo'lishi kerak, "
            "berilgan: %r" % step.get("target"))
    ctx.pom.grid.fill_cell(bolaklar[0], bolaklar[1], step.get("value"))


def _remove_tag(ctx, step):
    ctx.pom.form.remove_tag(step.get("target"), step.get("value"))
```

`ACTIONS` lug'atiga qo'sh:

```python
    "fill": _fill,
    "fill_date": _fill_date,
    "select": _select,
    "multiselect": _multiselect,
    "toggle": _toggle,
    "radio": _radio,
    "grid_fill": _grid_fill,
    "remove_tag": _remove_tag,
```

- [ ] **Qadam 4: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_actions_forma.py -v && .venv/bin/pytest
```

Kutilgan: `12 passed`; butun to'plam `283 passed, 3 skipped`.

- [ ] **Qadam 5: Mutatsiya isboti**

1. `_toggle` da tekshiruvni olib tashla (`qiymat == "on"` to'g'ridan-to'g'ri) →
   `test_toggle_notogri_qiymat_XATO_tashlaydi` yiqilishi kerak.
2. `_royxat` da xato tashlashni olib tashla →
   `test_multiselect_bosh_qiymat_XATO_tashlaydi` yiqilishi kerak.
3. `_grid_fill` da uzunlik tekshiruvini olib tashla →
   `test_grid_fill_vertikal_chiziq_yoq_bolsa_XATO_tashlaydi` yiqilishi kerak.

Hammasini qaytar.

- [ ] **Qadam 6: Commit**

```bash
git add runner/actions.py tests/test_actions_forma.py tests/fake_page.py tests/test_fake_page.py
git commit -m "$(cat <<'EOF'
feat(faza2): forma kiritish action'lari

`toggle` faqat `on`/`off` qabul qiladi: boshqa qiymatni jimgina `off` deb
olish noto'g'ri holatda davom etishga olib keladi. `multiselect` va
`grid_fill` formatini buzgan case XATO beradi, jimgina hech narsa
qilmaydi emas — tasdiqlanmagan «Pass» eng yomon natija.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 7: assert action'lari

**Fayllar:**
- Modify: `runner/actions.py`
- Create: `runner/expected.py`
- Test: `tests/test_actions_assert.py`, `tests/test_expected.py`

**Interfeyslar:**
- Consumes: 3-vazifadan `Assertions` (`BasePage.expect`), `Grid.expect_row`,
  `Grid.expect_count`, `Grid.expect_columns`, `Form.expect_field`,
  `Report.expect_required_errors`, `AssertionFailed`; 2-vazifadan `Collector`
- Produces:
  - `runner/expected.py`: `matn_elementlari(text) -> list[str]`,
    `qator_kataklari(text) -> list[str]`
  - `ACTIONS` ga: `assert_text`, `assert_row`, `assert_field`, `assert_value`,
    `assert_columns`, `assert_buttons`, `assert_url`, `assert_disabled`, `assert_api`,
    `assert_download`, `assert_no_request`

**Nega `runner/expected.py` alohida.** Case'dagi `value` matni odam uchun yozilgan:
`«Название», «Код» (majburiy)` yoki `Просмотр / Изменить`. Uni tekshiriladigan
elementlarga aylantirish — alohida, SOF mantiq va brauzersiz to'liq test qilinadi.
Manba (`smt.js` `assert_text`) shu tozalashni inline qilgan va shuning uchun
tekshirilmagan.

Tozalash qoidalari (manbadan aynan):
- qavs ichi olib tashlanadi: `(majburiy)` → ``
- vergul VA ` / ` bo'yicha bo'linadi
- `«»"` va oxiridagi `*` olib tashlanadi
- 60 belgidan uzun element tashlab yuboriladi (u jumla, element emas)
- `yo'q`, `...`, `…` bo'lgan element tashlab yuboriladi (u inkor yoki qisqartma)
- **Hech narsa qolmasa XATO** — manbada `if (!s.value) return;` bor edi

`qator_kataklari` (manba `assert_row`): `|` bo'yicha bo'linadi, `…` va `<` bilan
boshlanadigan va sana ko'rinishidagi (`dd.mm.yyyy`) kataklar tashlanadi, dastlabki 3 tasi
olinadi.

**`assert_api` ikki rejimi.** `target` da `i18n` bo'lsa faqat `i18n 404` tekshiriladi
(Faza 0 aniqlagan global ma'lum bug). Aks holda HTTP xatolari tekshiriladi.
`ctx.net` `None` bo'lsa **xato tashlanadi** — kuzatuvchi ulanmagan bo'lsa bu assert
hech narsa tekshirmaydi va jimgina o'tib ketardi.

**`assert_download` va `assert_no_request`.** 3 va 2 marta uchraydi. `assert_download`
Playwright `expect_download` kontekst menejerini talab qiladi — lekin yuklab olish
tugmasi allaqachon bosilgan bo'ladi, shuning uchun bu yerda faqat oxirgi yuklab olish
`ctx.data["download"]` da borligini tekshiradi (uni `_click` emas, 8-vazifadagi
`sequence` o'rnatadi). Agar kontekst menejeri kerak bo'lsa — bu case'lar `manual`
sifatida belgilanadi va sabab yoziladi. `assert_no_request` `ctx.net.bad` bo'sh
ekanini tekshiradi.

- [ ] **Qadam 1: `runner/expected.py` uchun yiqiladigan testni yozish**

`tests/test_expected.py`:

```python
# -*- coding: utf-8 -*-
import pytest

from runner.expected import matn_elementlari, qator_kataklari


def test_vergul_boyicha_bolinadi():
    assert matn_elementlari("Название, Код") == ["Название", "Код"]


def test_slash_boyicha_ham_bolinadi():
    assert matn_elementlari("Просмотр / Изменить") == ["Просмотр", "Изменить"]


def test_qavs_ichi_olib_tashlanadi():
    assert matn_elementlari("Название (majburiy), Код") == ["Название", "Код"]


def test_qoshtirnoq_va_yulduz_olib_tashlanadi():
    assert matn_elementlari("«Название» *, \"Код\"") == ["Название", "Код"]


def test_uzun_element_tashlanadi():
    """60 belgidan uzun matn — jumla, tekshiriladigan element emas."""
    uzun = "a" * 70

    assert matn_elementlari("Код, " + uzun) == ["Код"]


def test_inkor_va_qisqartma_tashlanadi():
    assert matn_elementlari("Код, tugma yo'q, ...") == ["Код"]


def test_hech_narsa_qolmasa_XATO():
    """Manbada `if (!s.value) return;` bor edi — tekshirmaydigan assert yashil beradi."""
    with pytest.raises(ValueError) as xato:
        matn_elementlari("yo'q, ...")

    assert "tekshiriladigan" in str(xato.value)


def test_takror_element_bir_marta_qoladi():
    assert matn_elementlari("Код, Код") == ["Код"]


def test_qator_kataklari_vertikal_chiziq_boyicha():
    assert qator_kataklari("QA-1 | Активный | 100") == ["QA-1", "Активный", "100"]


def test_qator_kataklari_uchtadan_koprogini_tashlaydi():
    """Manba `assert_row` dastlabki 3 katakni oladi — ko'prog'i mo'rt qiladi."""
    assert qator_kataklari("a | b | c | d | e") == ["a", "b", "c"]


def test_qator_kataklari_sana_va_shablonni_tashlaydi():
    """Sana har yugurishda o'zgaradi, `<id>` esa shablon."""
    assert qator_kataklari("QA-1 | 01.10.2026 | <id> | … | Активный") == ["QA-1", "Активный"]


def test_qator_kataklari_hech_narsa_qolmasa_XATO():
    with pytest.raises(ValueError):
        qator_kataklari("01.10.2026 | …")
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_expected.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'runner.expected'` — FAIL.

- [ ] **Qadam 3: `runner/expected.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Case'dagi odam uchun yozilgan `value` matnini tekshiriladigan elementlarga aylantiradi.

Nega alohida modul: bu SOF mantiq, brauzer kerak emas, shuning uchun to'liq test
qilinadi. Manba (`smt.js` `assert_text`) shu tozalashni inline qilgan va shuning
uchun hech qachon tekshirilmagan.
"""
import re

QAVS = re.compile(r"\([^)]*\)")
QOSHTIRNOQ = re.compile(r"[«»\"]")
OXIRGI_YULDUZ = re.compile(r"\s*\*$")
BOSHLIQ = re.compile(r"\s+")
INKOR = re.compile(r"yo'q|\.\.\.|…")
SANA = re.compile(r"\d{2}\.\d{2}\.\d{4}")
UZUNLIK_CHEGARASI = 60
KATAK_CHEGARASI = 3


def _toza(x):
    return BOSHLIQ.sub(" ", OXIRGI_YULDUZ.sub("", QOSHTIRNOQ.sub("", x))).strip()


def matn_elementlari(text):
    """`assert_text` uchun: matnni tekshiriladigan bo'laklarga ajratadi.

    Hech narsa qolmasa `ValueError` — tekshirmaydigan assert yashil belgi beradi va
    bu hech qanday assert'dan yomon (Faza 0 ning 32% soxta «Pass» sababi).
    """
    xom = QAVS.sub("", str(text or ""))
    bolaklar = []
    for vergul in xom.split(","):
        bolaklar.extend(vergul.split(" / "))
    natija = []
    for b in bolaklar:
        t = _toza(b)
        if t and len(t) < UZUNLIK_CHEGARASI and not INKOR.search(t) and t not in natija:
            natija.append(t)
    if not natija:
        raise ValueError("Matndan tekshiriladigan element ajratilmadi: %r" % text)
    return natija


def qator_kataklari(text):
    """`assert_row` uchun: `|` bilan ajratilgan kataklardan barqarorlarini oladi.

    Sana tashlanadi (har yugurishda o'zgaradi), `<...>` tashlanadi (shablon),
    `…` tashlanadi. Dastlabki 3 katak olinadi — ko'prog'i tekshiruvni mo'rt qiladi
    (manba `smt.js` `assert_row` ham shunday).
    """
    natija = []
    for b in str(text or "").split("|"):
        t = _toza(b)
        if not t or t == "…" or t.startswith("<") or SANA.search(t):
            continue
        if t not in natija:
            natija.append(t)
    if not natija:
        raise ValueError("Qator kataklari ajratilmadi: %r" % text)
    return natija[:KATAK_CHEGARASI]
```

- [ ] **Qadam 4: Assert action'lari uchun yiqiladigan testni yozish**

`tests/test_actions_assert.py`:

```python
# -*- coding: utf-8 -*-
import pytest

from pages.base_page import BasePage
from pages.components.assertions import AssertionFailed
from pages.ui.a2 import A2
from runner.actions import Ctx, run_step
from tests.fake_page import FakePage
from tests.test_network import FakeEventPage, FakeResponse
from utils.network import Collector


def _ctx(page, net=None):
    return Ctx(page=page, pom=BasePage(page, A2), net=net, data={})


def _a2_page(**kw):
    counts = dict(kw.pop("counts", {}))
    counts.setdefault(".smt-data-row", 1)
    return FakePage(counts=counts, **kw)


def test_assert_text_sahifadagi_matnni_tekshiradi():
    page = _a2_page(texts={"main >> last": "Название Код"})

    run_step(_ctx(page), {"action": "assert_text", "value": "Название, Код"})


def test_assert_text_yoq_matnda_yiqiladi():
    page = _a2_page(texts={"main >> last": "Название"})

    with pytest.raises(AssertionFailed):
        run_step(_ctx(page), {"action": "assert_text", "value": "Название, Валюта"})


def test_assert_text_bosh_qiymatda_YIQILADI():
    """Manbada bu holat jimgina o'tardi."""
    page = _a2_page(texts={"main >> last": "hamma narsa"})

    with pytest.raises((AssertionFailed, ValueError)):
        run_step(_ctx(page), {"action": "assert_text", "value": ""})


def test_assert_columns_ustunlarni_tekshiradi():
    page = _a2_page(lists={"main >> last >> smt-cell-header": ["Название", "Код"]})

    run_step(_ctx(page), {"action": "assert_columns", "value": "Название, Код"})


def test_assert_buttons_tugmalarni_tekshiradi():
    kalit = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
             "[role=option]:visible >> filter(has_text='Создать') >> first")
    page = _a2_page(counts={kalit: 1})

    run_step(_ctx(page), {"action": "assert_buttons", "value": "Создать"})


def test_assert_row_qatorni_tekshiradi():
    kalit = "main >> last >> .smt-data-row >> filter(has_text='QA-1') >> first"
    page = _a2_page(counts={kalit: 1})

    run_step(_ctx(page), {"action": "assert_row", "value": "QA-1 | 01.10.2026"})


def test_assert_field_maydon_qiymatini_tekshiradi():
    AJDOD = ("xpath=ancestor::*[.//input or .//textarea or .//smt-select-trigger "
             "or .//smt-data-select or .//*[@role=\"switch\"]][1]")
    kalit = ("main >> last >> label >> filter(has_text='Название') >> first >> " + AJDOD)
    page = _a2_page(texts={kalit: "QA-1"})

    run_step(_ctx(page), {"action": "assert_field", "target": "Название", "value": "QA-1"})


def test_assert_value_assert_field_bilan_bir_xil():
    """Manbada `assert_value` → `assert_field` ga yo'naltirilgan."""
    from runner.actions import ACTIONS

    assert ACTIONS["assert_value"] is ACTIONS["assert_field"]


def test_assert_url_manzilni_tekshiradi():
    page = _a2_page(url="https://app3.greenwhite.uz/xtrade/a2/anor/mr/filial%2Badd")

    run_step(_ctx(page), {"action": "assert_url", "target": "filial"})


def test_assert_disabled_nofaol_tugmani_tekshiradi():
    kalit = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
             "[role=option]:visible >> filter(has_text='Сохранить') >> first")
    page = _a2_page(counts={kalit: 1}, attrs={(kalit, "disabled"): "true"})

    run_step(_ctx(page), {"action": "assert_disabled", "target": "Сохранить"})


def test_assert_api_500_da_yiqiladi():
    hodisa = FakeEventPage()
    net = Collector(hodisa)
    hodisa.emit("response", FakeResponse("https://app3.greenwhite.uz/xtrade/b/save", 500))
    page = _a2_page()

    with pytest.raises(AssertionFailed) as xato:
        run_step(_ctx(page, net), {"action": "assert_api", "target": "POST /xtrade/b/**"})

    assert "500" in str(xato.value)


def test_assert_api_i18n_rejimi():
    """Faza 0: «har modulda +add.json 404» — global ma'lum bug, alohida xabar."""
    hodisa = FakeEventPage()
    net = Collector(hodisa)
    hodisa.emit("response", FakeResponse("https://app3.greenwhite.uz/x/i18n/add.json", 404))
    page = _a2_page()

    with pytest.raises(AssertionFailed) as xato:
        run_step(_ctx(page, net), {"action": "assert_api", "target": "GET **/i18n/**"})

    assert "i18n" in str(xato.value)


def test_assert_api_toza_tarmoqda_otadi():
    net = Collector(FakeEventPage())
    page = _a2_page()

    run_step(_ctx(page, net), {"action": "assert_api", "target": "POST /xtrade/b/**"})


def test_assert_api_kuzatuvchi_yoq_bolsa_XATO():
    """Kuzatuvchi ulanmagan bo'lsa bu assert hech narsa tekshirmaydi — jimgina
    o'tib ketishi TAQIQLANADI."""
    page = _a2_page()

    with pytest.raises(RuntimeError) as xato:
        run_step(_ctx(page, None), {"action": "assert_api", "target": "POST /xtrade/b/**"})

    assert "kuzatuvchi" in str(xato.value)


def test_assert_no_request_yomon_sorov_bolsa_yiqiladi():
    hodisa = FakeEventPage()
    net = Collector(hodisa)
    hodisa.emit("response", FakeResponse("https://app3.greenwhite.uz/xtrade/b/x", 500))
    page = _a2_page()

    with pytest.raises(AssertionFailed):
        run_step(_ctx(page, net), {"action": "assert_no_request", "target": "**"})
```

- [ ] **Qadam 5: Assert action'larini yozish**

`runner/actions.py` ga:

```python
from pages.components.assertions import AssertionFailed
from runner.expected import matn_elementlari, qator_kataklari

I18N_REJIM = re.compile(r"i18n")


def _assert_text(ctx, step):
    ctx.pom.expect.text(matn_elementlari(step.get("value")))


def _assert_row(ctx, step):
    ctx.pom.grid.expect_row(qator_kataklari(step.get("value")))


def _assert_field(ctx, step):
    ctx.pom.form.expect_field(step.get("target"), step.get("value"))


def _assert_columns(ctx, step):
    ctx.pom.grid.expect_columns(*matn_elementlari(step.get("value")))


def _assert_buttons(ctx, step):
    ctx.pom.expect.buttons(matn_elementlari(step.get("value")))


def _assert_url(ctx, step):
    ctx.pom.expect.url(step.get("target"))


def _assert_disabled(ctx, step):
    ctx.pom.expect.disabled(step.get("target"))


def _net_kerak(ctx):
    """Kuzatuvchi ulanmagan bo'lsa assert hech narsa tekshirmaydi — bu jimgina
    o'tib ketishning aynan o'zi, shuning uchun XATO."""
    if ctx.net is None:
        raise RuntimeError(
            "Tarmoq kuzatuvchisi ulanmagan — `assert_api` hech narsa tekshira olmaydi")
    return ctx.net


def _assert_api(ctx, step):
    """Case davomida yig'ilgan tarmoq javoblarini tekshiradi.

    `target` da `i18n` bo'lsa faqat tarjima fayli 404 lari qaraladi — Faza 0 uni
    global ma'lum bug deb aniqlagan, ilova bug'i emas.
    """
    net = _net_kerak(ctx)
    if I18N_REJIM.search(str(step.get("target") or "")):
        yoq = net.i18n_404()
        if yoq:
            raise AssertionFailed("i18n 404: %s" % ", ".join(yoq[:3]))
        return
    xato = net.http_errors()
    if xato:
        raise AssertionFailed(
            "HTTP xatolari: %s"
            % "; ".join("%s %s" % (e["status"], e["url"]) for e in xato[:3]))


def _assert_no_request(ctx, step):
    net = _net_kerak(ctx)
    if net.bad:
        raise AssertionFailed(
            "So'rov bo'lmasligi kutilgan, lekin bor: %s"
            % "; ".join("%s %s" % (b["status"], b["url"]) for b in net.bad[:3]))


def _assert_download(ctx, step):
    """Yuklab olish sodir bo'lganini tekshiradi. Yuklab olishni `sequence` o'rnatadi."""
    if not ctx.data.get("download"):
        raise AssertionFailed(
            "Fayl yuklab olinmadi (kutilgan: %s)" % (step.get("value") or step.get("target")))
```

`ACTIONS` ga:

```python
    "assert_text": _assert_text,
    "assert_row": _assert_row,
    "assert_field": _assert_field,
    "assert_value": _assert_field,
    "assert_columns": _assert_columns,
    "assert_buttons": _assert_buttons,
    "assert_url": _assert_url,
    "assert_disabled": _assert_disabled,
    "assert_api": _assert_api,
    "assert_no_request": _assert_no_request,
    "assert_download": _assert_download,
```

- [ ] **Qadam 6: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_expected.py tests/test_actions_assert.py -v && .venv/bin/pytest
```

Kutilgan: butun to'plam `310 passed, 3 skipped`.

- [ ] **Qadam 7: Mutatsiya isboti**

1. `matn_elementlari` da `ValueError` tashlashni `return []` ga o'zgartir →
   `test_hech_narsa_qolmasa_XATO` va `test_assert_text_bosh_qiymatda_YIQILADI`
   yiqilishi kerak.
2. `_net_kerak` da tekshiruvni olib tashla →
   `test_assert_api_kuzatuvchi_yoq_bolsa_XATO` yiqilishi kerak.
3. `qator_kataklari` da `[:KATAK_CHEGARASI]` ni olib tashla →
   `test_qator_kataklari_uchtadan_koprogini_tashlaydi` yiqilishi kerak.
4. `_assert_api` da `i18n` shoxini olib tashla →
   `test_assert_api_i18n_rejimi` yiqilishi kerak.

Hammasini qaytar.

- [ ] **Qadam 8: Commit**

```bash
git add runner/ tests/test_expected.py tests/test_actions_assert.py
git commit -m "$(cat <<'EOF'
feat(faza2): assert action'lari va `expected` matnini tahlil qilish

`runner/expected.py` alohida modul: case'dagi odam uchun yozilgan matnni
tekshiriladigan elementlarga aylantirish sof mantiq va brauzersiz to'liq
test qilinadi. Manba bu tozalashni inline qilgan va shuning uchun hech
qachon tekshirilmagan.

Hech narsa ajratilmasa XATO tashlanadi. Manbada `if (!s.value) return;`
bor edi — tekshirmaydigan assert yashil belgi beradi, bu Faza 0 ning 32%
soxta «Pass» sababi.

`assert_api` kuzatuvchi ulanmagan bo'lsa XATO tashlaydi: busiz u hech
narsa tekshirmasdan jimgina o'tib ketardi.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 8: oyna va tarkibiy action'lar — `confirm`, `dialog_close`, `sequence`, `pick`

**Fayllar:**
- Modify: `runner/actions.py`
- Test: `tests/test_actions_oyna.py`

**Interfeyslar:**
- Consumes: 5–7 vazifalardan `Ctx`, `run_step`, `ACTIONS`; Faza 1 dan `Dialog.confirm`,
  `Dialog.close`; 4-vazifadan `Grid.fill_cell`
- Produces: `ACTIONS` ga: `confirm`, `dialog_close`, `sequence`, `pick`

**`sequence` nima.** 41 marta uchraydi. Qadamning `ops` maydonida qadamlar ro'yxati bor —
ular ketma-ket bajariladi. `ops` bo'sh bo'lsa **xato tashlanadi**: bo'sh `sequence`
jimgina o'tib, case «Pass» bo'lardi.

**`pick` nima.** 13 marta uchraydi — TMC (tovar) tanlash naqshi. Manba (`smt.js` `pick`)
to'rt amalni ketma-ket bajaradi: «Подбор» bosiladi, jadval katagi to'ldiriladi,
«Закрыть» bosiladi, «Выбрать ТМЦ» oynasi tasdiqlanadi. `value` formati `Ustun=qiymat`.

**Nega `pick` alohida funksiya, `sequence` emas.** Case'larda u bitta qadam sifatida
yozilgan va shu tartib o'zgarmaydi. Uni case'larga yozib chiqish 13 joyda takrorlash
bo'lardi.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_actions_oyna.py`:

```python
# -*- coding: utf-8 -*-
import pytest

from pages.base_page import BasePage
from pages.ui.a2 import A2
from runner.actions import Ctx, run_step
from tests.fake_page import FakePage


def _ctx(page):
    return Ctx(page=page, pom=BasePage(page, A2), net=None, data={})


def _a2_page(**kw):
    counts = dict(kw.pop("counts", {}))
    counts.setdefault(".smt-data-row", 1)
    return FakePage(counts=counts, **kw)


def test_confirm_oynani_tasdiqlaydi():
    oyna = "[role=dialog] >> filter(has_text='Удалить запись') >> first"
    page = _a2_page(counts={oyna: 1})

    run_step(_ctx(page), {"action": "confirm", "target": "Удалить запись?", "value": "Да"})

    assert any("Удалить запись" in k for k in page.clicked())


def test_confirm_sukut_boyicha_Da_bosadi():
    oyna = "[role=dialog] >> filter(has_text='Сохранить') >> first"
    page = _a2_page(counts={oyna: 1})

    run_step(_ctx(page), {"action": "confirm", "target": "Сохранить?"})

    assert page.clicked(), "hech narsa bosilmadi"


def test_dialog_close_oynani_yopadi():
    page = _a2_page(counts={"[role=dialog]": 1})

    run_step(_ctx(page), {"action": "dialog_close", "target": "Закрыть"})

    assert any("Закрыть" in k for k in page.clicked())


def test_sequence_har_opni_bajaradi():
    a = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
         "[role=option]:visible >> filter(has_text='Создать') >> first")
    b = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
         "[role=option]:visible >> filter(has_text='Отмена') >> first")
    page = _a2_page(counts={a: 1, b: 1})

    run_step(_ctx(page), {"action": "sequence", "ops": [
        {"action": "click", "target": "Создать"},
        {"action": "click", "target": "Отмена"},
    ]})

    assert page.clicked() == [a, b]


def test_sequence_bosh_ops_XATO_tashlaydi():
    """Bo'sh `sequence` jimgina o'tib, case «Pass» bo'lardi."""
    page = _a2_page()

    with pytest.raises(ValueError) as xato:
        run_step(_ctx(page), {"action": "sequence", "ops": []})

    assert "ops" in str(xato.value)


def test_sequence_ichki_xato_yuqoriga_chiqadi():
    """Ichki qadam yiqilsa `sequence` ham yiqilishi SHART."""
    from runner.actions import ActionNotImplemented

    page = _a2_page()

    with pytest.raises(ActionNotImplemented):
        run_step(_ctx(page), {"action": "sequence", "ops": [
            {"action": "hech_qachon", "target": "x"},
        ]})


def test_pick_tort_amalni_ketma_ket_bajaradi():
    """Manba `smt.js` `pick`: Подбор → jadval katagi → Закрыть → «Выбрать ТМЦ» tasdiq."""
    tugma = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
             "[role=option]:visible >> filter(has_text='%s') >> first")
    grid = "main >> last >> .smt-data-row >> first >> xpath=ancestor::*[.//smt-cell-header][1]"
    page = _a2_page(
        counts={tugma % "Подбор": 1, tugma % "Закрыть": 1,
                "[role=dialog] >> filter(has_text='Выбрать ТМЦ') >> first": 1,
                grid + " >> .smt-data-row >> filter(has_text='QA-tovar') >> first": 1},
        lists={grid + " >> smt-cell-header": ["Товар", "Количество"]},
    )

    run_step(_ctx(page), {"action": "pick", "target": "QA-tovar", "value": "Количество=5"})

    bosilgan = page.clicked()
    assert tugma % "Подбор" in bosilgan
    assert any("nth(1)" in k for k in bosilgan), "jadval katagi to'ldirilmadi"
    assert tugma % "Закрыть" in bosilgan
    assert any("Выбрать ТМЦ" in k for k in bosilgan)


def test_pick_notogri_value_XATO_tashlaydi():
    page = _a2_page()

    with pytest.raises(ValueError) as xato:
        run_step(_ctx(page), {"action": "pick", "target": "QA-tovar", "value": "5"})

    assert "=" in str(xato.value)
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_actions_oyna.py -v
```

Kutilgan: `ActionNotImplemented: «confirm» action ijrochida yozilmagan` — FAIL.

- [ ] **Qadam 3: Action'larni yozish**

`runner/actions.py` ga:

```python
def _confirm(ctx, step):
    ctx.pom.dialog.confirm(step.get("target"), step.get("value") or "Да")


def _dialog_close(ctx, step):
    ctx.pom.dialog.close(step.get("target") or "Закрыть")


def _sequence(ctx, step):
    """`ops` dagi qadamlarni ketma-ket bajaradi.

    Bo'sh `ops` XATO: jimgina o'tib ketsa case «Pass» bo'lardi, lekin hech narsa
    bajarilmagan bo'lardi.
    """
    ops = step.get("ops") or []
    if not ops:
        raise ValueError("`sequence` da `ops` bo'sh — bajariladigan qadam yo'q")
    for op in ops:
        run_step(ctx, op)


def _pick(ctx, step):
    """TMC (tovar) tanlash naqshi — manba `smt.js` `pick` dagi to'rt amal.

    `value` formati: `Ustun=qiymat` (masalan `Количество=5`).
    """
    xom = str(step.get("value") or "")
    if "=" not in xom:
        raise ValueError(
            "`pick` uchun `value` «Ustun=qiymat» ko'rinishida bo'lishi kerak, berilgan: %r"
            % step.get("value"))
    ustun, qiymat = (x.strip() for x in xom.split("=", 1))
    _click(ctx, {"target": "Подбор"})
    ctx.pom.grid.fill_cell(step.get("target"), ustun, qiymat)
    _click(ctx, {"target": "Закрыть"})
    ctx.pom.dialog.confirm("Выбрать ТМЦ", "Да")
```

`ACTIONS` ga:

```python
    "confirm": _confirm,
    "dialog_close": _dialog_close,
    "sequence": _sequence,
    "pick": _pick,
```

- [ ] **Qadam 4: 31 action to'liq qamrab olinganini tasdiqlash**

Bu tekshiruv `tests/test_actions_qamrov.py` da:

```python
# -*- coding: utf-8 -*-
"""Case'lardagi HAR action ijrochida yozilgan bo'lishi shart."""
import json
from pathlib import Path

from runner.actions import ACTIONS

CASES = (Path(__file__).resolve().parents[2]
         / "SmartUp_Autotest" / "data" / "regression_cases.json")


def test_barcha_action_yozilgan():
    """Faza 0: `menu_plus` yozilmagani uchun 7 case jimgina yiqilgan.
    Bu test yangi action paydo bo'lsa darhol ogohlantiradi."""
    xom = json.loads(CASES.read_text(encoding="utf-8"))

    kerakli = set()
    for c in xom["cases"]:
        for s in c.get("steps", []):
            kerakli.add(s["action"])
            for op in s.get("ops", []):
                kerakli.add(op["action"])

    yoq = sorted(kerakli - set(ACTIONS))

    assert not yoq, "Bu action'lar ijrochida yozilmagan: %s" % ", ".join(yoq)


def test_action_soni_kutilganidek():
    """31 xil action o'lchangan (2026-09-30). Son o'zgarsa case'lar o'zgargan —
    bu ataylab bo'lishi kerak."""
    xom = json.loads(CASES.read_text(encoding="utf-8"))
    kerakli = {s["action"] for c in xom["cases"] for s in c.get("steps", [])}

    assert len(kerakli) == 31, "action turlari soni o'zgardi: %d" % len(kerakli)
```

- [ ] **Qadam 5: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_actions_oyna.py tests/test_actions_qamrov.py -v && .venv/bin/pytest
```

Kutilgan: butun to'plam `320 passed, 3 skipped`. `test_barcha_action_yozilgan` o'tishi
SHART — o'tmasa qaysi action yozilmagani xabarda ko'rinadi.

- [ ] **Qadam 6: Mutatsiya isboti**

1. `_sequence` da bo'sh `ops` tekshiruvini olib tashla →
   `test_sequence_bosh_ops_XATO_tashlaydi` yiqilishi kerak.
2. `_pick` dan `Закрыть` bosishni olib tashla →
   `test_pick_tort_amalni_ketma_ket_bajaradi` yiqilishi kerak.
3. `ACTIONS` dan `"menu_plus"` ni olib tashla →
   `test_barcha_action_yozilgan` yiqilishi kerak.

Hammasini qaytar.

- [ ] **Qadam 7: Commit**

```bash
git add runner/actions.py tests/test_actions_oyna.py tests/test_actions_qamrov.py
git commit -m "$(cat <<'EOF'
feat(faza2): oyna va tarkibiy action'lar, 31/31 action qamrab olindi

Bo'sh `sequence` XATO tashlaydi: jimgina o'tib ketsa case «Pass» bo'lardi,
lekin hech narsa bajarilmagan bo'lardi.

`test_barcha_action_yozilgan` case fayllaridagi har action ijrochida
borligini tekshiradi. Faza 0 da `menu_plus` yozilmagani uchun 7 case
jimgina yiqilgan va sabab ko'rinmagan.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 9: sessiya — login va qayta login

**Fayllar:**
- Create: `utils/session.py`
- Test: `tests/test_session.py`

**Interfeyslar:**
- Consumes: `pages.ui.detect.SessionExpired`
- Produces:
  - `LOGIN_URL` (regex), `SessionError(RuntimeError)`
  - `parolni_ol(rol="ADMIN") -> str` — `SMARTUP_PW_<ROL>` muhit o'zgaruvchisidan
  - `login_sahifasimi(page) -> bool`
  - `login(page, base_url, foydalanuvchi, parol)`
  - `sessiyani_taminla(page, base_url, foydalanuvchi, rol="ADMIN") -> bool`
    (qayta login bo'lsa `True`)

**Nega kerak.** Faza 1 aniqladi: sessiya bo'sh turganda bir necha daqiqada tugaydi
(14:14 da login → 14:2x da `/xtrade/a2/auth/login`). Faza 2 da yuzlab case yuritiladi —
qayta login bo'lmasa birinchi uzoq yugurish sessiya tugashi bilan to'xtaydi va qolgan
case'lar «yiqilgan» deb yoziladi, aslida ular sinalmagan.

29.09 tungi yugurishida `relogin.jsonl` umuman yaratilmagan — 858 case davomida bironta
qayta login bo'lmagan, chunki yugurish serverga uzluksiz murojaat qilgan. Demak qayta
login KAM ishlaydi, lekin ishlamasa butun yugurish yo'qoladi.

**Parol qat'iy qoidasi.** Parol faqat `SMARTUP_PW_ADMIN` muhit o'zgaruvchisidan olinadi
(u `3_Avtotest/.env` dan yuklanadi). Kodda, testda, hujjatda yoki logda parol
YOZILMAYDI. O'zgaruvchi topilmasa **xato tashlanadi** — bo'sh parol bilan login urinishi
foydalanuvchini bloklashi mumkin.

**Nega `login.html` YETARLI EMAS.** JS `isLoginPage` faqat `/login\.html/` ni biladi,
lekin 30.09 da sessiya `/xtrade/a2/auth/login` ga otdi. Ikkala shakl ham tekshiriladi,
qo'shimcha `#password` maydoni ham.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_session.py`:

```python
# -*- coding: utf-8 -*-
import pytest

from tests.fake_page import FakePage
from utils.session import (SessionError, login, login_sahifasimi, parolni_ol,
                           sessiyani_taminla)


def test_login_sahifasimi_login_html_ni_taniydi():
    assert login_sahifasimi(FakePage(url="https://app3.greenwhite.uz/xtrade/login.html"))


def test_login_sahifasimi_a2_auth_login_ni_ham_taniydi():
    """JS `isLoginPage` faqat `login.html` ni biladi, lekin 30.09 da sessiya
    `/xtrade/a2/auth/login` ga otdi."""
    assert login_sahifasimi(FakePage(url="https://app3.greenwhite.uz/xtrade/a2/auth/login"))


def test_login_sahifasimi_parol_maydoni_boyicha_ham_taniydi():
    assert login_sahifasimi(FakePage(counts={"#password": 1},
                                     url="https://app3.greenwhite.uz/xtrade/a2/"))


def test_login_sahifasimi_oddiy_sahifada_False():
    assert not login_sahifasimi(
        FakePage(url="https://app3.greenwhite.uz/xtrade/a2/anor/mr/filial_list"))


def test_parolni_ol_muhit_ozgaruvchisidan_oqiydi(monkeypatch):
    monkeypatch.setenv("SMARTUP_PW_TEST", "x-test-x")

    assert parolni_ol("TEST") == "x-test-x"


def test_parolni_ol_ozgaruvchi_yoq_bolsa_XATO(monkeypatch):
    """Bo'sh parol bilan login urinishi foydalanuvchini bloklashi mumkin."""
    monkeypatch.delenv("SMARTUP_PW_YOQ", raising=False)

    with pytest.raises(SessionError) as xato:
        parolni_ol("YOQ")

    assert "SMARTUP_PW_YOQ" in str(xato.value)
    assert ".env" in str(xato.value), "xabar qayerdan olinishini aytishi kerak"


def test_parolni_ol_bosh_qiymat_ham_XATO(monkeypatch):
    monkeypatch.setenv("SMARTUP_PW_BOSH", "   ")

    with pytest.raises(SessionError):
        parolni_ol("BOSH")


def test_login_maydonlarni_toldiradi_va_bosadi():
    page = FakePage(url="https://app3.greenwhite.uz/xtrade/login.html")

    login(page, "https://app3.greenwhite.uz", "qa@test", "x-test-x")

    assert ("goto", "https://app3.greenwhite.uz/xtrade/login.html") in page.calls
    assert ("#login >> first", "qa@test") in page.filled()
    assert ("#password >> first", "x-test-x") in page.filled()
    assert "#sign_in >> first" in page.clicked()


def test_sessiyani_taminla_oddiy_sahifada_qayta_login_qilmaydi(monkeypatch):
    monkeypatch.setenv("SMARTUP_PW_ADMIN", "x-test-x")
    page = FakePage(url="https://app3.greenwhite.uz/xtrade/a2/anor/mr/filial_list")

    assert sessiyani_taminla(page, "https://app3.greenwhite.uz", "qa@test") is False
    assert page.filled() == []


def test_sessiyani_taminla_login_sahifasida_qayta_login_qiladi(monkeypatch):
    monkeypatch.setenv("SMARTUP_PW_ADMIN", "x-test-x")
    page = FakePage(url="https://app3.greenwhite.uz/xtrade/a2/auth/login")

    assert sessiyani_taminla(page, "https://app3.greenwhite.uz", "qa@test") is True
    assert ("#login >> first", "qa@test") in page.filled()


def test_sessiyani_taminla_parol_yoq_bolsa_XATO(monkeypatch):
    monkeypatch.delenv("SMARTUP_PW_ADMIN", raising=False)
    page = FakePage(url="https://app3.greenwhite.uz/xtrade/login.html")

    with pytest.raises(SessionError):
        sessiyani_taminla(page, "https://app3.greenwhite.uz", "qa@test")
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_session.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'utils.session'` — FAIL.

- [ ] **Qadam 3: `utils/session.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Login va qayta login.

Faza 1 aniqladi: sessiya bo'sh turganda bir necha daqiqada tugaydi. Faza 2 da yuzlab
case yuritiladi — qayta login bo'lmasa birinchi uzoq yugurish sessiya tugashi bilan
to'xtaydi va qolgan case'lar «yiqilgan» deb yoziladi, aslida ular SINALMAGAN.

Parol faqat `SMARTUP_PW_<ROL>` muhit o'zgaruvchisidan olinadi (u `3_Avtotest/.env` dan
yuklanadi). Kodda, testda, hujjatda yoki logda parol YOZILMAYDI.
"""
import os
import re

LOGIN_URL = re.compile(r"login\.html|/auth/login")


class SessionError(RuntimeError):
    """Sessiya bilan ishlashda xato (parol yo'q, login bajarilmadi)."""


def parolni_ol(rol="ADMIN"):
    """`SMARTUP_PW_<ROL>` muhit o'zgaruvchisidan parolni oladi.

    Topilmasa yoki bo'sh bo'lsa XATO: bo'sh parol bilan login urinishi
    foydalanuvchini bloklashi mumkin.
    """
    kalit = "SMARTUP_PW_%s" % str(rol).upper()
    qiymat = (os.environ.get(kalit) or "").strip()
    if not qiymat:
        raise SessionError(
            "%s muhit o'zgaruvchisi yo'q yoki bo'sh. Yuritishdan oldin: "
            "`set -a; . ../.env; set +a`" % kalit)
    return qiymat


def login_sahifasimi(page):
    """Sahifa login sahifasi ekanini aniqlaydi.

    Ikki URL shakli ham tekshiriladi: JS `isLoginPage` faqat `login.html` ni biladi,
    lekin 30.09 da sessiya `/xtrade/a2/auth/login` ga otdi.
    """
    url = getattr(page, "url", "") or ""
    if LOGIN_URL.search(url):
        return True
    return page.locator("#password").count() > 0


def login(page, base_url, foydalanuvchi, parol):
    """Login sahifasiga o'tib kiradi. Muvaffaqiyatsiz bo'lsa `SessionError`."""
    page.goto("%s/xtrade/login.html" % base_url.rstrip("/"))
    page.locator("#login").first.fill(foydalanuvchi)
    page.locator("#password").first.fill(parol)
    page.locator("#sign_in").first.click()


def sessiyani_taminla(page, base_url, foydalanuvchi, rol="ADMIN"):
    """Sahifa login sahifasida bo'lsa qayta login qiladi.

    Qayta login bo'lsa `True`, kerak bo'lmasa `False` qaytaradi — chaqiruvchi buni
    `relogin.jsonl` ga yozadi, shuning uchun qayta login soni ko'rinib turadi.
    """
    if not login_sahifasimi(page):
        return False
    login(page, base_url, foydalanuvchi, parolni_ol(rol))
    return True
```

- [ ] **Qadam 4: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_session.py -v && .venv/bin/pytest
```

Kutilgan: `12 passed`; butun to'plam `332 passed, 3 skipped`.

- [ ] **Qadam 5: Parol logga chiqmasligini tasdiqlash**

```bash
grep -rn "qwerty\|SMARTUP_PW_ADMIN *=" utils/ runner/ tests/ pages/ conftest.py || echo "TOZA"
```

Kutilgan: `TOZA` yoki faqat `os.environ.get(kalit)` ko'rinishidagi o'qish. Haqiqiy parol
matni chiqsa — DARHOL to'xta va xabar ber.

- [ ] **Qadam 6: Mutatsiya isboti**

1. `LOGIN_URL` dan `|/auth/login` ni olib tashla →
   `test_login_sahifasimi_a2_auth_login_ni_ham_taniydi` yiqilishi kerak.
2. `parolni_ol` da `.strip()` va bo'shlik tekshiruvini olib tashla →
   `test_parolni_ol_bosh_qiymat_ham_XATO` yiqilishi kerak.
3. `sessiyani_taminla` da `if not login_sahifasimi(page): return False` ni olib tashla →
   `test_sessiyani_taminla_oddiy_sahifada_qayta_login_qilmaydi` yiqilishi kerak.

Hammasini qaytar.

- [ ] **Qadam 7: Commit**

```bash
git add utils/session.py tests/test_session.py
git commit -m "$(cat <<'EOF'
feat(faza2): login va qayta login

Faza 1 aniqladi: sessiya bo'sh turganda bir necha daqiqada tugaydi. Faza 2
da yuzlab case yuritiladi — qayta login bo'lmasa birinchi uzoq yugurish
sessiya tugashi bilan to'xtaydi va qolgan case'lar «yiqilgan» deb
yoziladi, aslida ular sinalmagan.

`login_sahifasimi` ikki URL shaklini ham biladi: JS `isLoginPage` faqat
`login.html` ni bilardi, lekin 30.09 da sessiya `/xtrade/a2/auth/login`
ga otdi.

Parol faqat muhit o'zgaruvchisidan olinadi; topilmasa yoki bo'sh bo'lsa
xato — bo'sh parol bilan urinish foydalanuvchini bloklashi mumkin.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 10: natija yozuvi va yiqilish dalili

**Fayllar:**
- Create: `runner/record.py`, `utils/evidence.py`
- Test: `tests/test_record.py`, `tests/test_evidence.py`

**Interfeyslar:**
- Consumes: 1-vazifadan `Case`, `nav_route`; 2-vazifadan `Collector`;
  Faza 1 dan `TestLogger`
- Produces:
  - `runner/record.py`: `yangi_yozuv(case) -> dict`, `pass_deb_belgila(rec, steps_done)`,
    `fail_deb_belgila(rec, case, steps_done, xato, net=None, shot=None)`,
    `skip_deb_belgila(rec, sabab)`, `yoz(rec, jsonl_yoli)`
  - `utils/evidence.py`: `Evidence(results_dir, case_id)` — `shot_yoli()`,
    `skrinshot(page) -> str | None`, `jurnal(logger) -> Path`, `trace_yoli()`

**Nega format AYNAN Faza 0 dagidek.** Mavjud `scripts/analyze.py` va
`scripts/bug_report.py` `regression.jsonl` ni o'qiydi. Agar POM ijrochisi boshqa format
yozsa, ikkala vosita ham qayta yozilishi kerak bo'ladi. Format saqlansa — `bug_report.py`
o'zgarishsiz ishlaydi va Faza 2 natijasidan darhol Jira'ga tayyor hisobot chiqadi.

Yozuv kalitlari (Faza 0 dan aynan):

| Kalit | Nima |
|---|---|
| `id`, `module`, `section`, `form`, `title`, `type` | case'dan |
| `last_result`, `last_bug` | case'dan (28.09 qo'lda natijasi) |
| `result` | `Pass` / `Fail` / `Skip` |
| `steps_done` | muvaffaqiyatli bajarilgan qadamlar soni |
| `failed_step` | yiqilgan qadam raqami (1 dan) |
| `failed_desc`, `failed_expected` | yiqilgan qadamning `description`/`expected` |
| `error` | xato matni (3 qatorgacha, 500 belgigacha) |
| `soft_errors` | soft assert xatolari ro'yxati |
| `net` | yomon tarmoq so'rovlari (4 tagacha) |
| `shot` | `shots/REG-<id>.png` ko'rinishidagi nisbiy yo'l |
| `url` | case tugaganda sahifa manzili |
| `reason` | `Skip` sababi |
| `ts` | ISO vaqt belgisi |

**Nega `steps_done` muhim.** Faza 0 ning R9 nuqsoni: `failed_step` siz `Fail` qatori har
qadamni «ok» deb sanagan va muvaffaqiyatni sun'iy ko'targan. `steps_done` har qadamdan
KEYIN oshiriladi, shuning uchun `failed_step = steps_done + 1` doim to'g'ri.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_record.py`:

```python
# -*- coding: utf-8 -*-
import json

import pytest

from runner.cases import Case
from runner.record import (fail_deb_belgila, pass_deb_belgila, skip_deb_belgila,
                           yangi_yozuv, yoz)

CASE = Case(id="TC-GL-FIL-005", module="Главное", section="Организации",
            form="Организации (создание)", title="Bo'sh forma saqlanmaydi",
            type="Validatsiya", priority="P1", seq=5, phase="P01",
            last_result="Pass", last_bug="", auto=True, skip_reason="",
            steps=[{"action": "nav", "target": "Главное > Организации",
                    "description": "Menyudan o'tish", "expected": "Ro'yxat ochiladi"},
                   {"action": "click", "target": "Создать",
                    "description": "«Создать» ni bosing", "expected": "Forma ochiladi"},
                   {"action": "click", "target": "Сохранить",
                    "description": "«Сохранить» ni bosing",
                    "expected": "Majburiy maydonlar qizil bo'ladi"}])


def test_yangi_yozuv_case_maydonlarini_kochiradi():
    rec = yangi_yozuv(CASE)

    assert rec["id"] == "TC-GL-FIL-005" and rec["module"] == "Главное"
    assert rec["section"] == "Организации" and rec["form"] == "Организации (создание)"
    assert rec["title"] == "Bo'sh forma saqlanmaydi" and rec["type"] == "Validatsiya"
    assert rec["last_result"] == "Pass" and rec["last_bug"] == ""
    assert rec["steps_done"] == 0


def test_pass_deb_belgila():
    rec = pass_deb_belgila(yangi_yozuv(CASE), 3)

    assert rec["result"] == "Pass" and rec["steps_done"] == 3
    assert "failed_step" not in rec


def test_fail_deb_belgila_yiqilgan_qadamni_togri_hisoblaydi():
    """Faza 0 R9: `failed_step` siz Fail qatori har qadamni «ok» deb sanagan va
    muvaffaqiyatni sun'iy ko'targan."""
    rec = fail_deb_belgila(yangi_yozuv(CASE), CASE, steps_done=2,
                           xato=Exception("«Сохранить» topilmadi"))

    assert rec["result"] == "Fail"
    assert rec["steps_done"] == 2
    assert rec["failed_step"] == 3
    assert rec["failed_desc"] == "«Сохранить» ni bosing"
    assert rec["failed_expected"] == "Majburiy maydonlar qizil bo'ladi"
    assert "topilmadi" in rec["error"]


def test_fail_deb_belgila_qadamlar_tugagandan_keyin_ham_ishlaydi():
    """Validatsiya tekshiruvi oxirgi qadamdan KEYIN yiqilishi mumkin.
    Faza 0 da bu holat 3 qatorni «hisobga olinmagan» qilgan."""
    rec = fail_deb_belgila(yangi_yozuv(CASE), CASE, steps_done=3,
                           xato=Exception("forma yopildi"))

    assert rec["failed_step"] == 4
    assert rec["failed_desc"] == "" and rec["failed_expected"] == ""


def test_fail_deb_belgila_xatoni_uch_qatorga_kesadi():
    uzun = "\n".join("qator %d" % i for i in range(10))
    rec = fail_deb_belgila(yangi_yozuv(CASE), CASE, 0, Exception(uzun))

    assert rec["error"].count("qator") == 3
    assert len(rec["error"]) <= 500


def test_fail_deb_belgila_tarmoqni_tortta_bilan_cheklaydi():
    net = [{"status": 500, "url": "/x/%d" % i} for i in range(9)]
    rec = fail_deb_belgila(yangi_yozuv(CASE), CASE, 0, Exception("x"), net=net)

    assert len(rec["net"]) == 4


def test_fail_deb_belgila_shot_nisbiy_yol():
    rec = fail_deb_belgila(yangi_yozuv(CASE), CASE, 0, Exception("x"),
                           shot="shots/REG-TC-GL-FIL-005.png")

    assert rec["shot"] == "shots/REG-TC-GL-FIL-005.png"


def test_skip_deb_belgila_sababni_yozadi():
    rec = skip_deb_belgila(yangi_yozuv(CASE), "haqiqiy pul harakati")

    assert rec["result"] == "Skip" and rec["reason"] == "haqiqiy pul harakati"


def test_skip_sababsiz_XATO():
    """Sababsiz Skip — natija tahlilida «nega sinalmadi» savoliga javob qolmaydi."""
    with pytest.raises(ValueError):
        skip_deb_belgila(yangi_yozuv(CASE), "")


def test_yoz_jsonl_qatorini_qoshadi(tmp_path):
    yol = tmp_path / "regression.jsonl"

    yoz(pass_deb_belgila(yangi_yozuv(CASE), 3), yol)
    yoz(skip_deb_belgila(yangi_yozuv(CASE), "sabab"), yol)

    qatorlar = [json.loads(l) for l in yol.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert [q["result"] for q in qatorlar] == ["Pass", "Skip"]
    assert all("ts" in q for q in qatorlar)


def test_yoz_papkani_yaratadi(tmp_path):
    yol = tmp_path / "yangi" / "ichki" / "regression.jsonl"

    yoz(pass_deb_belgila(yangi_yozuv(CASE), 1), yol)

    assert yol.exists()
```

`tests/test_evidence.py`:

```python
# -*- coding: utf-8 -*-
import pytest

from utils.evidence import Evidence
from utils.logger import TestLogger


class FakeScreenshotPage:
    def __init__(self, xato=None):
        self.xato = xato
        self.calls = []

    def screenshot(self, path=None, full_page=False):
        self.calls.append((path, full_page))
        if self.xato:
            raise self.xato
        from pathlib import Path
        Path(path).write_bytes(b"PNG")


def test_shot_yoli_case_id_bilan(tmp_path):
    ev = Evidence(tmp_path, "TC-GL-FIL-005")

    assert ev.shot_yoli().name == "REG-TC-GL-FIL-005.png"
    assert ev.shot_yoli().parent.name == "shots"


def test_skrinshot_faylni_yozadi_va_nisbiy_yol_qaytaradi(tmp_path):
    ev = Evidence(tmp_path, "TC-GL-FIL-005")
    page = FakeScreenshotPage()

    natija = ev.skrinshot(page)

    assert natija == "shots/REG-TC-GL-FIL-005.png"
    assert (tmp_path / "shots" / "REG-TC-GL-FIL-005.png").read_bytes() == b"PNG"
    assert page.calls[0][1] is True, "to'liq sahifa olinishi kerak"


def test_skrinshot_yiqilsa_None_qaytaradi_LEKIN_XATONI_YOZADI(tmp_path):
    """Skrinshot olinmasligi case natijasini o'zgartirmasligi kerak (u allaqachon
    yiqilgan), lekin sabab YO'QOLMASLIGI kerak — `notes` ga yoziladi."""
    ev = Evidence(tmp_path, "TC-X")
    page = FakeScreenshotPage(xato=RuntimeError("brauzer yopilgan"))

    assert ev.skrinshot(page) is None
    assert any("brauzer yopilgan" in n for n in ev.notes)


def test_jurnal_faylga_yoziladi(tmp_path):
    ev = Evidence(tmp_path, "TC-GL-FIL-005")
    log = TestLogger("TC-GL-FIL-005", tmp_path / "logs")
    log.step("Menyudan o'tildi")
    log.fail("«Сохранить» topilmadi")

    yol = ev.jurnal(log)

    matn = yol.read_text(encoding="utf-8")
    assert "QADAM: Menyudan o'tildi" in matn and "XATO: «Сохранить»" in matn


def test_trace_yoli_case_id_bilan(tmp_path):
    ev = Evidence(tmp_path, "TC-GL-FIL-005")

    assert ev.trace_yoli().name == "TC-GL-FIL-005.zip"
    assert ev.trace_yoli().parent.name == "traces"
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_record.py tests/test_evidence.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'runner.record'` — FAIL.

- [ ] **Qadam 3: `runner/record.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Natija yozuvi — format AYNAN Faza 0 dagidek.

Nega: mavjud `scripts/analyze.py` va `scripts/bug_report.py` `regression.jsonl` ni
o'qiydi. Format saqlansa `bug_report.py` o'zgarishsiz ishlaydi va Faza 2 natijasidan
darhol Jira'ga tayyor hisobot chiqadi.
"""
import datetime
import json
from pathlib import Path

XATO_QATOR_CHEGARASI = 3
XATO_BELGI_CHEGARASI = 500
TARMOQ_CHEGARASI = 4


def yangi_yozuv(case):
    """Case boshida yozuvni tayyorlaydi. `steps_done` nol — har qadamdan KEYIN oshadi."""
    return {"id": case.id, "module": case.module, "section": case.section,
            "form": case.form, "title": case.title, "type": case.type,
            "last_result": case.last_result, "last_bug": case.last_bug,
            "steps_done": 0}


def pass_deb_belgila(rec, steps_done):
    rec["result"] = "Pass"
    rec["steps_done"] = int(steps_done)
    return rec


def fail_deb_belgila(rec, case, steps_done, xato, net=None, shot=None, soft_errors=None):
    """Yiqilishni yozadi.

    `failed_step = steps_done + 1` — Faza 0 ning R9 nuqsoni aynan shu hisobning
    yo'qligidan kelib chiqqan: `failed_step` siz `Fail` qatori har qadamni «ok» deb
    sanagan va muvaffaqiyatni sun'iy ko'targan.

    Qadamlar tugagandan keyin yiqilish ham bo'ladi (Validatsiya tekshiruvi) — bunda
    `failed_desc`/`failed_expected` bo'sh qoladi, lekin `failed_step` yoziladi.
    """
    rec["result"] = "Fail"
    rec["steps_done"] = int(steps_done)
    rec["failed_step"] = int(steps_done) + 1
    qadam = case.steps[steps_done] if steps_done < len(case.steps) else {}
    rec["failed_desc"] = qadam.get("description", "") or ""
    rec["failed_expected"] = qadam.get("expected", "") or ""
    rec["error"] = "\n".join(str(xato).split("\n")[:XATO_QATOR_CHEGARASI])[:XATO_BELGI_CHEGARASI]
    if net:
        rec["net"] = list(net)[:TARMOQ_CHEGARASI]
    if shot:
        rec["shot"] = shot
    if soft_errors:
        rec["soft_errors"] = list(soft_errors)
    return rec


def skip_deb_belgila(rec, sabab):
    """Skip yozadi. Sabab BO'SH bo'lishi TAQIQLANADI — natija tahlilida «nega
    sinalmadi» savoliga javob qolmaydi."""
    if not str(sabab or "").strip():
        raise ValueError("Skip sababi bo'sh bo'lishi mumkin emas: %s" % rec.get("id"))
    rec["result"] = "Skip"
    rec["reason"] = str(sabab).strip()
    return rec


def yoz(rec, jsonl_yoli):
    """Yozuvni `regression.jsonl` ga qo'shib yozadi."""
    yol = Path(jsonl_yoli)
    yol.parent.mkdir(parents=True, exist_ok=True)
    rec.setdefault("ts", datetime.datetime.now().isoformat(timespec="seconds"))
    with yol.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return yol
```

- [ ] **Qadam 4: `utils/evidence.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Yiqilish dalili: skrinshot, qadam jurnali, trace yo'llari.

Faza 1 sharhi ogohlantirdi: yuzlab case yiqilganda dalil bo'lmasa sabab tahlil
qilinmaydi. Foydalanuvchining talabi: har yiqilish uchun Jira'ga qo'yiladigan aniq
qadamlar va isbot bo'lishi kerak.
"""
from pathlib import Path


class Evidence:
    def __init__(self, results_dir, case_id):
        self.dir = Path(results_dir)
        self.case_id = str(case_id)
        self.notes = []

    def shot_yoli(self):
        return self.dir / "shots" / ("REG-%s.png" % self.case_id)

    def trace_yoli(self):
        return self.dir / "traces" / ("%s.zip" % self.case_id)

    def skrinshot(self, page):
        """To'liq sahifa skrinshotini oladi va NISBIY yo'lni qaytaradi.

        Yiqilsa `None` qaytaradi — case allaqachon yiqilgan, skrinshotning yo'qligi
        natijani o'zgartirmasligi kerak. LEKIN sabab `notes` ga yoziladi: jimgina
        yo'qotish taqiqlangan.
        """
        yol = self.shot_yoli()
        yol.parent.mkdir(parents=True, exist_ok=True)
        try:
            page.screenshot(path=str(yol), full_page=True)
        except Exception as e:      # noqa: BLE001 — sabab YOZILADI, yutilmaydi
            self.notes.append("skrinshot olinmadi (%s): %s" % (self.case_id, e))
            return None
        return "shots/%s" % yol.name

    def jurnal(self, logger):
        """Qadam jurnalini faylga yozadi va yo'lni qaytaradi."""
        return logger.write()
```

- [ ] **Qadam 5: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_record.py tests/test_evidence.py -v && .venv/bin/pytest
```

Kutilgan: butun to'plam `349 passed, 3 skipped`.

- [ ] **Qadam 6: `bug_report.py` mos kelishini tasdiqlash**

```bash
.venv/bin/python - <<'PY'
import json, tempfile, pathlib
from runner.cases import Case
from runner.record import yangi_yozuv, fail_deb_belgila, yoz
import scripts.bug_report as BR

c = Case(id="TC-X-001", module="Главное", section="s", form="f", title="t",
         type="Ijobiy", priority="P1", seq=1, phase="P01", last_result="Pass",
         last_bug="", auto=True, skip_reason="",
         steps=[{"action": "click", "target": "Сохранить",
                 "description": "«Сохранить» ni bosing", "expected": "Saqlanadi"}])
rec = fail_deb_belgila(yangi_yozuv(c), c, 0, Exception("HTTP 500"),
                       net=[{"status": 500, "url": "/xtrade/b/save"}],
                       shot="shots/REG-TC-X-001.png")
d = pathlib.Path(tempfile.mkdtemp())
yoz(rec, d / "regression.jsonl")
print("toifa:", BR.categorize(rec, {}))
print("jiddiylik:", BR.severity(rec, BR.categorize(rec, {})))
PY
```

Kutilgan: `bug_report.py` yozuvni toifaga ajratadi va xato tashlamaydi. Xato chiqsa —
yozuv formati mos kelmagan, to'xta va xabar ber.

- [ ] **Qadam 7: Mutatsiya isboti**

1. `fail_deb_belgila` da `+ 1` ni olib tashla →
   `test_fail_deb_belgila_yiqilgan_qadamni_togri_hisoblaydi` yiqilishi kerak.
2. `skip_deb_belgila` dagi bo'shlik tekshiruvini olib tashla →
   `test_skip_sababsiz_XATO` yiqilishi kerak.
3. `Evidence.skrinshot` dagi `self.notes.append(...)` ni olib tashla →
   `test_skrinshot_yiqilsa_None_qaytaradi_LEKIN_XATONI_YOZADI` yiqilishi kerak.

Hammasini qaytar.

- [ ] **Qadam 8: Commit**

```bash
git add runner/record.py utils/evidence.py tests/test_record.py tests/test_evidence.py
git commit -m "$(cat <<'EOF'
feat(faza2): natija yozuvi (Faza 0 formati) va yiqilish dalili

Format aynan Faza 0 dagidek: mavjud `analyze.py` va `bug_report.py`
o'zgarishsiz ishlaydi va Faza 2 natijasidan darhol Jira'ga tayyor hisobot
chiqadi.

`failed_step = steps_done + 1` — Faza 0 ning R9 nuqsoni aynan shu hisob
yo'qligidan kelib chiqqan: `failed_step` siz Fail qatori har qadamni «ok»
deb sanagan.

Skrinshot olinmasa `None` qaytariladi (case allaqachon yiqilgan), lekin
sabab `notes` ga yoziladi — jimgina yo'qotish taqiqlangan.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 11: yugurish testi va sessiya doirasidagi fixture'lar

**Fayllar:**
- Create: `tests/test_regression.py`
- Modify: `conftest.py`
- Test: `tests/test_conftest_faza2.py`

**Interfeyslar:**
- Consumes: 1–10 vazifalarning hammasi
- Produces:
  - `conftest.py` fixture'lari: `base_url` (sessiya), `results_dir` (sessiya),
    `brauzer_konteksti` (sessiya), `live_page` (funksiya), `net_collector` (funksiya)
  - `tests/test_regression.py` — `regression_cases.json` bo'yicha parametrlangan test
  - CLI: `--live`, `--cases`, `--modules`, `--types`, `--results`

**Brauzer doirasi qarori.** Faza 1 sharhi ogohlantirdi: har test uchun yangi brauzer
548 case uchun juda sekin (brauzer ishga tushishi ~1 s → 9 daqiqa behuda) va
`save_data`/`load_data` zanjirini buzadi.

Qaror: **brauzer va kontekst SESSIYA doirasida, sahifa har case uchun yangi.**
- brauzer sessiya doirasida → tez;
- kontekst sessiya doirasida → cookie va sessiya saqlanadi, zanjirli case'lar ishlaydi;
- sahifa har case uchun yangi → oldingi case'ning ochilgan drawer'i keyingisiga o'tmaydi.

**Qayta login qachon.** Har case boshida, birinchi navigatsiyadan KEYIN
`sessiyani_taminla()` chaqiriladi. Qayta login bo'lsa `relogin.jsonl` ga yoziladi —
shuning uchun tungi yugurishda qayta login soni ko'rinib turadi (29.09 da bu fayl umuman
yaratilmagan, ya'ni 858 case davomida sessiya tugamagan).

**Trace.** Kontekst darajasida `tracing.start(screenshots=True, snapshots=True)`.
Har case uchun `tracing.start_chunk()` / `stop_chunk(path=...)` — faqat YIQILGAN case'ning
trace'i saqlanadi, aks holda 548 trace diskni to'ldiradi.

**`PYTHONDONTWRITEBYTECODE`.** `conftest.py` da o'rnatilmaydi (kech bo'ladi — Python
allaqachon import qilgan). U yuritish buyrug'ida beriladi va bu README va tungi skriptda
yoziladi.

**`save_data` kalitlari.** Faza 1 sharhi: sessiya doirasidagi bitta lug'at kalitlarni
testlar orasida saqlaydi. Faza 2 da kalit nomlash konventsiyasi: `<CASE_ID>.<nom>`
(masalan `TC-GL-TSK-004.task_nomi`). Buni `Ctx.data` orqali ishlatish ijrochining ishi,
lekin konventsiya `conftest.py` izohida yoziladi.

- [ ] **Qadam 1: Fixture'lar uchun yiqiladigan testni yozish**

`tests/test_conftest_faza2.py`:

```python
# -*- coding: utf-8 -*-
"""Fixture'lar brauzersiz tekshiriladi: doira (scope) va CLI parametrlari."""
import pytest


def test_live_bayrogi_royxatdan_otgan(pytestconfig):
    assert pytestconfig.getoption("--live") is not None


def test_cases_bayrogi_royxatdan_otgan(pytestconfig):
    assert pytestconfig.getoption("--cases") is None or True


def test_modules_va_types_bayroqlari_bor(pytestconfig):
    pytestconfig.getoption("--modules")
    pytestconfig.getoption("--types")


def test_results_bayrogi_bor(pytestconfig):
    pytestconfig.getoption("--results")


def test_brauzer_konteksti_sessiya_doirasida():
    """548 case uchun har testda brauzer ishga tushirish ~9 daqiqa behuda ketadi,
    va yangi kontekst zanjirli case'larni buzadi."""
    import conftest

    assert conftest.brauzer_konteksti._pytestfixturefunction.scope == "session"


def test_live_page_funksiya_doirasida():
    """Oldingi case'ning ochilgan drawer'i keyingisiga o'tmasligi kerak."""
    import conftest

    assert conftest.live_page._pytestfixturefunction.scope in (None, "function")


def test_results_dir_sessiya_doirasida():
    import conftest

    assert conftest.results_dir._pytestfixturefunction.scope == "session"
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_conftest_faza2.py -v
```

Kutilgan: `ValueError: no option named '--cases'` — FAIL.

- [ ] **Qadam 3: `conftest.py` ga fixture'larni qo'shish**

`pytest_addoption` ga (mavjud `--live` yonига):

```python
    parser.addoption("--cases", action="store", default=None,
                     help="Faqat shu case'lar (vergul bilan): TC-GL-FIL-001,TC-FIN-CUR-006")
    parser.addoption("--modules", action="store", default=None,
                     help="Faqat shu modullar (vergul bilan): Склад,Финансы")
    parser.addoption("--types", action="store", default=None,
                     help="Faqat shu turlar (vergul bilan): Smoke,Validatsiya")
    parser.addoption("--results", action="store", default=None,
                     help="Natija papkasi (sukut: ../Tungi_natijalar/<sana>)")
```

Fayl oxiriga:

```python
BASE_URL = "https://app3.greenwhite.uz"
FOYDALANUVCHI = "mohir@xan"
FILIAL = "Toshkent"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def results_dir(request):
    """Natija papkasi. Sukut bo'yicha `../Tungi_natijalar/<bugun>`.

    Sessiya doirasida: bitta yugurishning barcha natijasi bitta papkada bo'lishi
    shart, aks holda `analyze.py` ularni taqqoslay olmaydi.
    """
    import datetime

    berilgan = request.config.getoption("--results")
    if berilgan:
        yol = Path(berilgan)
    else:
        kun = datetime.date.today().isoformat()
        yol = Path(__file__).resolve().parents[1] / "Tungi_natijalar" / kun
    yol.mkdir(parents=True, exist_ok=True)
    return yol


@pytest.fixture(scope="session")
def brauzer_konteksti(_playwright, request):
    """Brauzer va kontekst SESSIYA doirasida.

    Nega: 548 case uchun har testda brauzer ishga tushirish ~1 s × 548 ≈ 9 daqiqa
    behuda ketadi. Kontekst ham sessiya doirasida — cookie va sessiya saqlanadi,
    shuning uchun zanjirli case'lar (`save_data`/`load_data`) ishlaydi.

    `save_data` kalit konventsiyasi: `<CASE_ID>.<nom>` (masalan
    `TC-GL-TSK-004.task_nomi`). Sessiya doirasidagi bitta lug'at kalitlarni testlar
    orasida saqlaydi, shuning uchun case id prefiksi to'qnashuvni oldini oladi.
    """
    auth = (Path(__file__).resolve().parents[1]
            / "SmartUp_Autotest" / ".auth" / "admin.json")
    if not auth.exists():
        pytest.fail("Sessiya fayli yo'q: %s — avval `npx playwright test --project=setup`"
                    % auth)
    brauzer = _playwright.chromium.launch(headless=not os.environ.get("HEADED"))
    ctx = brauzer.new_context(storage_state=str(auth), locale="ru-RU",
                              viewport={"width": 1600, "height": 1000})
    ctx.tracing.start(screenshots=True, snapshots=True)
    try:
        yield ctx
    finally:
        ctx.tracing.stop()
        ctx.close()
        brauzer.close()


@pytest.fixture
def live_page(brauzer_konteksti):
    """Har case uchun YANGI sahifa — oldingi case'ning ochilgan drawer'i o'tmasligi
    uchun. Kontekst esa umumiy, shuning uchun sessiya saqlanadi."""
    page = brauzer_konteksti.new_page()
    page.set_default_navigation_timeout(90_000)
    page.set_default_timeout(30_000)
    try:
        yield page
    finally:
        page.close()


@pytest.fixture
def net_collector(live_page):
    """Tarmoq kuzatuvchisi. `assert_api` busiz XATO tashlaydi."""
    from utils.network import Collector

    return Collector(live_page)
```

`conftest.py` boshiga `import os` va `from pathlib import Path` allaqachon bor —
bo'lmasa qo'sh.

- [ ] **Qadam 4: `tests/test_regression.py` yozish**

```python
# -*- coding: utf-8 -*-
"""548 auto case'ni POM poydevorida yuritadi.

Natija `regression.jsonl` ga Faza 0 formatida yoziladi — mavjud `scripts/analyze.py`
va `scripts/bug_report.py` o'zgarishsiz ishlaydi.

Yuritish:
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest tests/test_regression.py --live
    ... --cases TC-GL-FIL-001,TC-GL-FIL-005
    ... --modules Склад --types Smoke
"""
from pathlib import Path

import pytest

from pages.base_page import BasePage
from runner.actions import Ctx, ManualStep, run_step
from runner.cases import case_id, filter_cases, load_cases
from runner.record import (fail_deb_belgila, pass_deb_belgila, skip_deb_belgila,
                           yangi_yozuv, yoz)
from utils.evidence import Evidence
from utils.logger import TestLogger
from utils.session import sessiyani_taminla

CASES_FAYLI = Path(__file__).resolve().parents[1] / "data" / "regression_cases.json"

pytestmark = pytest.mark.live


def _cases(config):
    """CLI filtrlarini qo'llab case'lar ro'yxatini beradi."""
    def bol(nom):
        xom = config.getoption(nom)
        return [x.strip() for x in xom.split(",") if x.strip()] if xom else None

    return filter_cases(load_cases(CASES_FAYLI), ids=bol("--cases"),
                        modules=bol("--modules"), types=bol("--types"))


def pytest_generate_tests(metafunc):
    """Case'lar `phase`+`seq` tartibida parametrga aylanadi — tartib
    ma'lumotnoma → hujjat bog'liqligini saqlaydi."""
    if "case" in metafunc.fixturenames:
        cases = _cases(metafunc.config)
        metafunc.parametrize("case", cases, ids=[case_id(c) for c in cases])


def test_case(case, live_page, net_collector, results_dir, base_url, save_data, load_data):
    rec = yangi_yozuv(case)
    jsonl = results_dir / "regression.jsonl"
    ev = Evidence(results_dir, case.id)
    log = TestLogger(case.id, results_dir / "logs")

    if not case.auto:
        yoz(skip_deb_belgila(rec, case.skip_reason or "auto=false"), jsonl)
        pytest.skip(case.skip_reason or "auto=false")

    ctx = Ctx(page=live_page, pom=BasePage(live_page), net=net_collector,
              data={"save": save_data, "load": load_data})
    live_page.context.tracing.start_chunk(title=case.id)
    bajarilgan = 0
    try:
        for i, step in enumerate(case.steps):
            if i == 1:
                # Birinchi navigatsiyadan KEYIN sessiya tekshiriladi: login sahifasiga
                # tushgan bo'lsak qayta kiramiz. Faza 1: sessiya bo'sh turganda bir
                # necha daqiqada tugaydi.
                if sessiyani_taminla(live_page, base_url, FOYDALANUVCHI):
                    yoz({"case": case.id}, results_dir / "relogin.jsonl")
                    net_collector.reset()
            log.step("%d. %s" % (i + 1, step.get("description") or step.get("action")))
            run_step(ctx, step)
            bajarilgan = i + 1
        yoz(pass_deb_belgila(rec, bajarilgan), jsonl)
        live_page.context.tracing.stop_chunk()
    except ManualStep as e:
        yoz(skip_deb_belgila(rec, "qo'lda bajariladi: %s" % e), jsonl)
        live_page.context.tracing.stop_chunk()
        pytest.skip("qo'lda bajariladi: %s" % e)
    except Exception as e:
        log.fail(str(e))
        shot = ev.skrinshot(live_page)
        ev.jurnal(log)
        ev.trace_yoli().parent.mkdir(parents=True, exist_ok=True)
        live_page.context.tracing.stop_chunk(path=str(ev.trace_yoli()))
        yoz(fail_deb_belgila(rec, case, bajarilgan, e,
                            net=net_collector.bad, shot=shot), jsonl)
        raise
    finally:
        rec["url"] = getattr(live_page, "url", "")
```

**Diqqat:** `FOYDALANUVCHI` `conftest.py` da ta'riflangan — uni `tests/test_regression.py`
ga `from conftest import FOYDALANUVCHI` bilan import qilma (pytest conftest'ni modul
sifatida import qilishni tavsiya qilmaydi). Buning o'rniga `conftest.py` da
`foydalanuvchi` nomli sessiya fixture'i qo'sh va testda uni parametr sifatida ol.

- [ ] **Qadam 5: Case fayli nusxasini yaratish**

`data/regression_cases.json` hozircha `SmartUp_Autotest/data/` dan nusxa. 12-vazifa
uni assert'lar bilan qayta yozadi.

```bash
mkdir -p data && cp ../SmartUp_Autotest/data/regression_cases.json data/
.venv/bin/python -c "
from runner.cases import load_cases, filter_cases
c = load_cases('data/regression_cases.json')
print('jami', len(c), '· auto', len(filter_cases(c, auto_only=True)))
"
```

Kutilgan: `jami 858 · auto 548`.

- [ ] **Qadam 6: Yig'ilishni tekshirish (brauzersiz)**

```bash
.venv/bin/pytest tests/test_regression.py --collect-only -q | tail -3
```

Kutilgan: 858 test yig'iladi (auto bo'lmaganlari skip bo'ladi). `--live` bayrog'isiz
hammasi skip.

```bash
.venv/bin/pytest tests/test_regression.py --collect-only -q --cases TC-GL-FIL-002 | tail -3
```

Kutilgan: 1 test.

- [ ] **Qadam 7: Butun to'plamni yuritish**

```bash
.venv/bin/pytest
```

Kutilgan: `356 passed, 861 skipped` atrofida (858 regression case `--live` siz skip).

**Diqqat:** skip soni juda katta bo'lib chiqsa yig'ilish to'g'ri ishlayapti. Agar
`356 passed` dan kam bo'lsa — oldingi testlar buzilgan.

- [ ] **Qadam 8: Commit**

```bash
git add conftest.py tests/test_regression.py tests/test_conftest_faza2.py data/
git commit -m "$(cat <<'EOF'
feat(faza2): yugurish testi va sessiya doirasidagi fixture'lar

Brauzer va kontekst SESSIYA doirasida, sahifa har case uchun yangi. Faza 1
sharhi ogohlantirdi: har testda brauzer ishga tushirish 548 case uchun ~9
daqiqa behuda ketadi va yangi kontekst zanjirli case'larni buzadi.

Har case boshida birinchi navigatsiyadan keyin sessiya tekshiriladi va
kerak bo'lsa qayta login qilinadi; qayta login `relogin.jsonl` ga
yoziladi. 29.09 da bu fayl umuman yaratilmagan — 858 case davomida
sessiya tugamagan, lekin tugasa butun yugurish yo'qolardi.

Trace faqat YIQILGAN case uchun saqlanadi — 548 trace diskni to'ldiradi.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 12: assert'siz 245 case'ga assert generatsiya qilish

**Fayllar:**
- Modify: `runner/actions.py` (3 yangi action)
- Create: `scripts/generate_asserts.py`
- Test: `tests/test_generate_asserts.py`, `tests/test_actions_assert.py` (qo'shiladi)

**Interfeyslar:**
- Consumes: 7-vazifadan `matn_elementlari`; 3-vazifadan `Grid.expect_count`,
  `Report.expect_required_errors`, `Assertions.enabled`
- Produces:
  - `ACTIONS` ga: `assert_required`, `assert_count`, `assert_enabled`
  - `scripts/generate_asserts.py`: `assert_yasa(step, oldingi) -> dict | None`,
    `case_ga_qosh(case) -> tuple[dict, bool]`, `main(argv=None) -> int`

**Nega kerak.** 548 auto case'dan **245 tasida (45%) hech qanday assert qadami yo'q** —
ular faqat amallarni bajaradi va oxirida hech narsa tekshirmaydi. Bunday case istisno
tashlanmasa «Pass» beradi, lekin **hech nimani isbotlamaydi**. Chiqish mezoni:
assert'li case ulushi 55% dan 100% ga chiqishi.

**Manba `expected` maydonida.** Qadamlarning 93% ida `expected` matni bor (o'lchandi:
2362 qadamdan 2188 tasida). Bu matn qo'lda test case'lardan ko'chirilgan va aynan
«nima bo'lishi kerak» ni aytadi. Shuning uchun `test_cases.md` ni qayta o'qish kerak
emas — dizayn spetsifikatsiyasidagi farazdan qulayroq.

**O'lchangan naqshlar** (assert'siz case'lardagi 818 `expected` matni bo'yicha):

| Naqsh | Son | Qanday assert |
|---|---|---|
| `... sahifasi ochiladi` / `ro'yxat ochiladi` | 223 | `assert_text` (qo'shtirnoq ichidagi nom) |
| `amal tugmalari chiqadi: X, Y` | 82 | `assert_buttons` value=`X, Y` |
| `... qizil ramka bilan belgilanadi` | 47 | `assert_required` |
| `ustunlar: ...` | 13 | `assert_columns` |
| `yopiladi` / `qaytadi` | 10 | `assert_text` (zaxira yo'l) |
| `nofaol` | 3 | `assert_disabled` |
| `faollashadi` | 1 | `assert_enabled` |
| qolgani | 439 | zaxira yo'l: `assert_text` (ajratilgan tokenlar) |

Zaxira yo'l 603/818 (74%) matndan token ajratadi. Token ajratilmagan 215 matnda ham
qo'shimcha naqshlar bor:
- `Maydonda X ko'rinadi` → `assert_field` (maydon nomi OLDINGI `fill`/`select` qadamidan)
- `Qator yo'qoladi (8/8 → 7/7)` → `assert_count` value=`7`

**Case darajasida: 245 tadan 244 tasi kamida bitta assert oladi.** Faqat
`TC-SKL-FMR-005` hech narsa bermaydi — u qo'lda ko'rib chiqiladi va hisobotda alohida
ko'rsatiladi.

**QAT'IY QOIDA — hech narsa generatsiya qilinmasa, JIMGINA o'tib ketmaydi.** Generator
bunday case'larni `QOLDA_KORISH.md` ga yozadi. Bo'sh `assert_text` yozish — Faza 0 ning
32% soxta «Pass» nuqsonini qaytarish bo'lardi.

**Chiqish fayli.** `data/regression_cases.json` qayta yoziladi.
`SmartUp_Autotest/data/` ga TEGILMAYDI (loyiha qoidasi).

- [ ] **Qadam 1: Uch yangi action uchun yiqiladigan testni yozish**

`tests/test_actions_assert.py` oxiriga:

```python
def test_assert_required_majburiy_maydon_xatosini_tekshiradi():
    page = _a2_page(counts={"main >> last >> [class*=outline-error]": 3})

    run_step(_ctx(page), {"action": "assert_required"})


def test_assert_required_xato_yoq_bolsa_yiqiladi():
    """Validatsiya case'ining asosiy tasdiqlashi: bo'sh forma saqlanmasligi kerak."""
    page = _a2_page(counts={"main >> last >> [class*=outline-error]": 0})

    with pytest.raises(AssertionFailed) as xato:
        run_step(_ctx(page), {"action": "assert_required"})

    assert "saqlanib ketgan" in str(xato.value)


def test_assert_count_qatorlar_sonini_tekshiradi():
    page = _a2_page(counts={"main >> last >> .smt-data-row": 7})

    run_step(_ctx(page), {"action": "assert_count", "value": "7"})


def test_assert_count_mos_kelmasa_yiqiladi():
    page = _a2_page(counts={"main >> last >> .smt-data-row": 8})

    with pytest.raises(AssertionFailed):
        run_step(_ctx(page), {"action": "assert_count", "value": "7"})


def test_assert_count_son_bolmasa_XATO():
    page = _a2_page()

    with pytest.raises(ValueError):
        run_step(_ctx(page), {"action": "assert_count", "value": "ko'p"})


def test_assert_enabled_faol_tugmani_tekshiradi():
    kalit = ("main >> last >> button:visible, a:visible, [role=menuitem]:visible, "
             "[role=option]:visible >> filter(has_text='Сохранить') >> first")
    page = _a2_page(counts={kalit: 1}, attrs={})

    run_step(_ctx(page), {"action": "assert_enabled", "target": "Сохранить"})
```

- [ ] **Qadam 2: Uch action'ni yozish**

`runner/actions.py` ga:

```python
def _assert_required(ctx, step):
    """To'ldirilmagan majburiy maydonlar belgilanganini tekshiradi.

    Validatsiya case'larining asosiy tasdiqlashi: bo'sh forma saqlanmasligi kerak.
    """
    ctx.pom.report.expect_required_errors(int(step.get("value") or 1))


def _assert_count(ctx, step):
    """Jadval qatorlari sonini tekshiradi."""
    xom = str(step.get("value") or "").strip()
    if not xom.isdigit():
        raise ValueError("`assert_count` uchun `value` son bo'lishi kerak, berilgan: %r"
                         % step.get("value"))
    ctx.pom.grid.expect_count(int(xom))


def _assert_enabled(ctx, step):
    ctx.pom.expect.enabled(step.get("target"))
```

`ACTIONS` ga:

```python
    "assert_required": _assert_required,
    "assert_count": _assert_count,
    "assert_enabled": _assert_enabled,
```

- [ ] **Qadam 3: Generator uchun yiqiladigan testni yozish**

`tests/test_generate_asserts.py`:

```python
# -*- coding: utf-8 -*-
import json

import pytest

from scripts.generate_asserts import assert_yasa, case_ga_qosh, main


def test_amal_tugmalari_naqshi():
    s = {"action": "row_click", "target": "birinchi qator",
         "expected": "Qator ostida amal tugmalari chiqadi: Просмотр, Изменить, Удалить."}

    a = assert_yasa(s, oldingi=None)

    assert a["action"] == "assert_buttons"
    assert a["value"] == "Просмотр, Изменить, Удалить"


def test_qizil_ramka_naqshi():
    s = {"action": "click", "target": "Сохранить",
         "expected": "Название *, Код * qizil ramka bilan belgilanadi; yozuv yaratilmaydi."}

    a = assert_yasa(s, oldingi=None)

    assert a["action"] == "assert_required"


def test_sahifa_ochiladi_naqshi():
    s = {"action": "nav", "target": "Главное > Организации",
         "expected": "«Организации» sahifasi ochiladi."}

    a = assert_yasa(s, oldingi=None)

    assert a["action"] == "assert_text" and a["value"] == "Организации"


def test_ustunlar_naqshi():
    s = {"action": "nav", "expected": "Ustunlar: Название, Код, Активный."}

    a = assert_yasa(s, oldingi=None)

    assert a["action"] == "assert_columns"
    assert "Название" in a["value"]


def test_nofaol_naqshi():
    s = {"action": "click", "expected": "«Сохранить» nofaol (sarlavha bo'sh)."}

    a = assert_yasa(s, oldingi=None)

    assert a["action"] == "assert_disabled" and a["target"] == "Сохранить"


def test_faollashadi_naqshi():
    s = {"action": "fill", "expected": "«Сохранить» faollashadi."}

    a = assert_yasa(s, oldingi=None)

    assert a["action"] == "assert_enabled" and a["target"] == "Сохранить"


def test_maydonda_korinadi_naqshi_oldingi_qadamdan_maydonni_oladi():
    """«Maydonda QA-CUR-1 ko'rinadi» — maydon nomi OLDINGI `fill` qadamida."""
    oldingi = {"action": "fill", "target": "Название", "value": "QA-CUR-1"}
    s = {"action": "observe", "expected": "Maydonda QA-CUR-1 ko'rinadi."}

    a = assert_yasa(s, oldingi=oldingi)

    assert a["action"] == "assert_field"
    assert a["target"] == "Название" and a["value"] == "QA-CUR-1"


def test_qator_yoqoladi_naqshi_yangi_sonni_oladi():
    s = {"action": "confirm", "expected": "Qator yo'qoladi (8/8 → 7/7)."}

    a = assert_yasa(s, oldingi=None)

    assert a["action"] == "assert_count" and a["value"] == "7"


def test_zaxira_yol_tokenlardan_assert_text():
    s = {"action": "click", "expected": "Статус «Новый», Чек-лист ko'rinadi."}

    a = assert_yasa(s, oldingi=None)

    assert a["action"] == "assert_text"
    assert "Новый" in a["value"]


def test_token_ajratilmasa_None():
    """Jimgina bo'sh `assert_text` yozish TAQIQLANADI — u yashil belgi berardi."""
    s = {"action": "observe", "expected": "Qator ostida amal tugmalari chiqadi."}

    assert assert_yasa(s, oldingi=None) is None


def test_expected_bosh_bolsa_None():
    assert assert_yasa({"action": "click", "expected": ""}, oldingi=None) is None


def test_case_ga_qosh_har_qadamdan_keyin_assert_qoyadi():
    case = {"id": "TC-X", "steps": [
        {"action": "nav", "target": "Главное > Организации",
         "expected": "«Организации» sahifasi ochiladi."},
        {"action": "row_click", "target": "birinchi qator",
         "expected": "Qator ostida amal tugmalari chiqadi: Просмотр."},
    ]}

    yangi, qamrab = case_ga_qosh(case)

    assert qamrab is True
    assert [s["action"] for s in yangi["steps"]] == [
        "nav", "assert_text", "row_click", "assert_buttons"]


def test_case_ga_qosh_assert_bor_case_ga_tegmaydi():
    case = {"id": "TC-Y", "steps": [
        {"action": "nav", "expected": "«X» sahifasi ochiladi."},
        {"action": "assert_text", "value": "X"},
    ]}

    yangi, qamrab = case_ga_qosh(case)

    assert yangi["steps"] == case["steps"], "allaqachon assert'i bor case o'zgarmasligi kerak"
    assert qamrab is True


def test_case_ga_qosh_hech_narsa_chiqmasa_False():
    case = {"id": "TC-Z", "steps": [{"action": "observe", "expected": "Qator yo'qoladi."}]}

    yangi, qamrab = case_ga_qosh(case)

    assert qamrab is False


def test_main_faylni_yozadi_va_hisobot_beradi(tmp_path):
    kirish = tmp_path / "kirish.json"
    kirish.write_text(json.dumps({"cases": [
        {"id": "TC-A", "auto": True, "steps": [
            {"action": "nav", "expected": "«Организации» sahifasi ochiladi."}]},
        {"id": "TC-B", "auto": True, "steps": [
            {"action": "observe", "expected": "Qator yo'qoladi."}]},
    ]}, ensure_ascii=False), encoding="utf-8")
    chiqish = tmp_path / "chiqish.json"

    kod = main(["--in", str(kirish), "--out", str(chiqish),
                "--report", str(tmp_path / "QOLDA_KORISH.md")])

    assert kod == 0
    yangi = json.loads(chiqish.read_text(encoding="utf-8"))
    assert [s["action"] for s in yangi["cases"][0]["steps"]] == ["nav", "assert_text"]
    hisobot = (tmp_path / "QOLDA_KORISH.md").read_text(encoding="utf-8")
    assert "TC-B" in hisobot, "qamrab olinmagan case hisobotda bo'lishi SHART"
    assert "TC-A" not in hisobot
```

- [ ] **Qadam 4: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_generate_asserts.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'scripts.generate_asserts'` — FAIL.

- [ ] **Qadam 5: `scripts/generate_asserts.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Qadamning `expected` matnidan assert qadami generatsiya qiladi.

Nega: 548 auto case'dan 245 tasida (45%) hech qanday assert yo'q — ular faqat
amallarni bajaradi va hech nimani tekshirmaydi. Bunday case istisno tashlanmasa
«Pass» beradi, lekin HECH NIMANI isbotlamaydi.

Manba `expected` maydonida: qadamlarning 93% ida u bor va aynan «nima bo'lishi kerak»
ni aytadi.

QAT'IY QOIDA: hech narsa ajratilmasa `None` qaytariladi va case `QOLDA_KORISH.md` ga
yoziladi. Bo'sh `assert_text` yozish — Faza 0 ning 32% soxta «Pass» nuqsonini
qaytarish bo'lardi.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runner.expected import matn_elementlari      # noqa: E402

AMAL_TUGMALARI = re.compile(r"amal tugmalari chiqadi\s*:\s*(.+?)\.?\s*$", re.IGNORECASE)
QIZIL_RAMKA = re.compile(r"qizil ramka", re.IGNORECASE)
SAHIFA = re.compile(r"[«\"]([^»\"]+)[»\"]\s*(?:sahifasi|ro'yxati|ro.yxati)?\s*ochiladi",
                    re.IGNORECASE)
USTUNLAR = re.compile(r"ustunlar\s*:\s*(.+?)\.?\s*$", re.IGNORECASE)
NOFAOL = re.compile(r"[«\"]([^»\"]+)[»\"]\s*nofaol", re.IGNORECASE)
FAOL = re.compile(r"[«\"]([^»\"]+)[»\"]\s*faollashadi", re.IGNORECASE)
MAYDONDA = re.compile(r"Maydonda\s+(\S+)\s+ko'rinadi", re.IGNORECASE)
QATOR_YOQOLADI = re.compile(r"Qator yo'qoladi\s*\([^)]*?(\d+)\s*/\s*\d+\s*\)", re.IGNORECASE)
MAYDON_BERUVCHI = ("fill", "fill_date", "select", "multiselect", "radio")


def assert_yasa(step, oldingi):
    """Qadamning `expected` matnidan assert qadami yasaydi yoki `None`.

    `oldingi` — shu qadamdan oldingi qadam: «Maydonda X ko'rinadi» naqshida maydon
    nomi aynan o'sha qadamdan olinadi.
    """
    e = str(step.get("expected") or "").strip()
    if not e:
        return None

    m = AMAL_TUGMALARI.search(e)
    if m:
        try:
            return {"action": "assert_buttons",
                    "value": ", ".join(matn_elementlari(m.group(1))),
                    "expected": e}
        except ValueError:
            return None

    if QIZIL_RAMKA.search(e):
        return {"action": "assert_required", "expected": e}

    m = USTUNLAR.search(e)
    if m:
        try:
            return {"action": "assert_columns",
                    "value": ", ".join(matn_elementlari(m.group(1))), "expected": e}
        except ValueError:
            return None

    m = NOFAOL.search(e)
    if m:
        return {"action": "assert_disabled", "target": m.group(1).strip(), "expected": e}

    m = FAOL.search(e)
    if m:
        return {"action": "assert_enabled", "target": m.group(1).strip(), "expected": e}

    m = QATOR_YOQOLADI.search(e)
    if m:
        return {"action": "assert_count", "value": m.group(1), "expected": e}

    m = MAYDONDA.search(e)
    if m and oldingi and oldingi.get("action") in MAYDON_BERUVCHI and oldingi.get("target"):
        return {"action": "assert_field", "target": oldingi["target"],
                "value": m.group(1).strip().rstrip(".,;"), "expected": e}

    m = SAHIFA.search(e)
    if m:
        return {"action": "assert_text", "value": m.group(1).strip(), "expected": e}

    # Zaxira yo'l: matndan tokenlar ajratiladi. Ajratilmasa `None` — bo'sh assert
    # yozilmaydi.
    try:
        return {"action": "assert_text", "value": ", ".join(matn_elementlari(e)),
                "expected": e}
    except ValueError:
        return None


def case_ga_qosh(case):
    """Case'ga assert qadamlarini qo'shadi. `(yangi_case, qamrab_olindimi)` qaytaradi.

    Allaqachon assert'i bor case O'ZGARMAYDI — qo'lda yozilgan assert generatsiya
    qilinganidan aniqroq.
    """
    qadamlar = case.get("steps") or []
    if any(str(s.get("action", "")).startswith("assert") for s in qadamlar):
        return dict(case), True

    yangi = []
    qoshildi = 0
    oldingi = None
    for s in qadamlar:
        yangi.append(s)
        a = assert_yasa(s, oldingi)
        if a:
            a["description"] = "Tekshirish: %s" % (a.get("expected") or "")
            yangi.append(a)
            qoshildi += 1
        oldingi = s
    natija = dict(case)
    natija["steps"] = yangi
    return natija, qoshildi > 0


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Assert'siz case'larga `expected` matnidan assert generatsiya qiladi")
    p.add_argument("--in", dest="kirish", required=True)
    p.add_argument("--out", dest="chiqish", required=True)
    p.add_argument("--report", dest="hisobot", required=True)
    a = p.parse_args(argv)

    xom = json.loads(Path(a.kirish).read_text(encoding="utf-8"))
    cases = xom.get("cases") or []
    if not cases:
        p.error("Kirish faylida case yo'q: %s" % a.kirish)

    yangilar, qamrab_olinmagan, qoshilgan = [], [], 0
    for c in cases:
        oldin = len(c.get("steps") or [])
        yangi, ok = case_ga_qosh(c)
        yangilar.append(yangi)
        qoshilgan += len(yangi.get("steps") or []) - oldin
        if c.get("auto") and not ok:
            qamrab_olinmagan.append(c)

    xom["cases"] = yangilar
    xom["asserts_generated"] = True
    Path(a.chiqish).write_text(json.dumps(xom, ensure_ascii=False, indent=1),
                               encoding="utf-8")

    satrlar = ["# Assert generatsiya qilinmagan case'lar", "",
               "Bu case'larning `expected` matnidan tekshiriladigan element ajratilmadi.",
               "Ular QO'LDA ko'rib chiqilishi kerak — bo'sh assert yozish yashil belgi",
               "berardi va bu hech qanday assert'dan yomon.", "",
               "Jami: %d" % len(qamrab_olinmagan), ""]
    for c in qamrab_olinmagan:
        satrlar.append("## %s — %s → %s" % (c.get("id"), c.get("module"), c.get("form")))
        satrlar.append("")
        for s in c.get("steps") or []:
            satrlar.append("- `%s` %s · kutilgan: %s"
                           % (s.get("action"), s.get("target") or "",
                              s.get("expected") or "—"))
        satrlar.append("")
    Path(a.hisobot).write_text("\n".join(satrlar), encoding="utf-8")

    print("case: %d · qo'shilgan assert qadami: %d · qamrab olinmagan: %d"
          % (len(cases), qoshilgan, len(qamrab_olinmagan)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Qadam 6: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_generate_asserts.py tests/test_actions_assert.py -v && .venv/bin/pytest
```

Kutilgan: butun to'plam `377 passed` atrofida (+ regression skip'lari).

- [ ] **Qadam 7: Haqiqiy case fayliga qo'llash**

```bash
.venv/bin/python scripts/generate_asserts.py \
  --in ../SmartUp_Autotest/data/regression_cases.json \
  --out data/regression_cases.json \
  --report data/QOLDA_KORISH.md
```

Kutilgan chiqish: `qamrab olinmagan: 1` (o'lchangan: faqat `TC-SKL-FMR-005`).
Boshqa son chiqsa — to'xta va xabar ber, bu naqshlar kutilganidek ishlamaganini bildiradi.

- [ ] **Qadam 8: Natijani o'lchash**

```bash
.venv/bin/python - <<'PY'
import json
d = json.load(open('data/regression_cases.json', encoding='utf-8'))
auto = [c for c in d['cases'] if c.get('auto')]
bor = [c for c in auto if any(str(s.get('action','')).startswith('assert') for s in c['steps'])]
print('auto case:', len(auto))
print('assert bilan:', len(bor), '(%.0f%%)' % (100*len(bor)/len(auto)))
PY
```

Kutilgan: `assert bilan: 547 (100%)` — chiqish mezoni 55% dan 100% ga.
547/548 = 99.8% bo'lib «100%» deb yumaloqlanadi; 1 case qo'lda ko'riladi.

- [ ] **Qadam 9: Generatsiya qilingan assert'lardan namunani QO'LDA ko'rib chiqish**

```bash
.venv/bin/python - <<'PY'
import json, random
d = json.load(open('data/regression_cases.json', encoding='utf-8'))
random.seed(7)
gen = [(c['id'], s) for c in d['cases'] for s in c['steps']
       if s.get('action','').startswith('assert') and s.get('description','').startswith('Tekshirish')]
for cid, s in random.sample(gen, 20):
    print('%-16s %-18s %s' % (cid, s['action'], (s.get('value') or s.get('target') or '—')[:60]))
    print('%16s kutilgan: %s' % ('', (s.get('expected') or '')[:70]))
PY
```

20 ta namunani o'qi. Agar assert `expected` matniga mos kelmasa (masalan `assert_text`
qiymatida rus tilidagi element emas, o'zbekcha jumla bo'lsa) — to'xta, naqshni tuzat va
generatsiyani qayta yurit. **Bu qadam avtomatlashtirilmaydi: generatsiya qilingan
tekshiruvning ma'nosini faqat odam baholaydi.**

- [ ] **Qadam 10: Action qamrovi hamon to'liq ekanini tasdiqlash**

Yangi case faylida 3 yangi action paydo bo'ldi (`assert_required`, `assert_count`,
`assert_enabled`). `tests/test_actions_qamrov.py` `SmartUp_Autotest/data/` ga qaraydi,
shuning uchun u o'zgarmaydi. Yangi fayl uchun alohida tekshiruv qo'sh:

```python
def test_yangi_case_faylining_action_lari_ham_yozilgan():
    """Generatsiyadan keyingi fayl `data/` da — u ham to'liq qamrab olinishi shart."""
    yol = Path(__file__).resolve().parents[1] / "data" / "regression_cases.json"
    if not yol.exists():
        pytest.skip("generatsiya hali yurgizilmagan")
    xom = json.loads(yol.read_text(encoding="utf-8"))

    kerakli = set()
    for c in xom["cases"]:
        for s in c.get("steps", []):
            kerakli.add(s["action"])
            for op in s.get("ops", []):
                kerakli.add(op["action"])

    yoq = sorted(kerakli - set(ACTIONS))

    assert not yoq, "Bu action'lar ijrochida yozilmagan: %s" % ", ".join(yoq)
```

- [ ] **Qadam 11: Commit**

```bash
git add runner/actions.py scripts/generate_asserts.py tests/ data/
git commit -m "$(cat <<'EOF'
feat(faza2): assert'siz 245 case'ga `expected` matnidan assert generatsiya

548 auto case'dan 245 tasida (45%) hech qanday assert yo'q edi — ular
faqat amallarni bajarib, hech nimani tekshirmasdi. Bunday case istisno
tashlanmasa «Pass» beradi, lekin hech nimani isbotlamaydi.

Manba `expected` maydonida: qadamlarning 93% ida u bor. Sakkiz naqsh
aniqlangan (amal tugmalari, qizil ramka, sahifa ochiladi, ustunlar,
nofaol/faollashadi, maydonda ko'rinadi, qator yo'qoladi) va zaxira yo'l
tokenlardan `assert_text` yasaydi.

Hech narsa ajratilmasa `None` qaytariladi va case `QOLDA_KORISH.md` ga
yoziladi. Bo'sh `assert_text` yozish Faza 0 ning 32% soxta «Pass»
nuqsonini qaytarish bo'lardi.

Natija: assert'li case ulushi 55% → 100% (1 case qo'lda ko'riladi).

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

### Vazifa 13: chiqish mezoni — 548 case'ni real serverda yuritish

**Fayllar:**
- Create: `scripts/faza2_taqqos.py`, `Hujjatlar/2026-XX-XX-faza2-natija.md`
- Modify: `README.md`

**Interfeyslar:**
- Consumes: 1–12 vazifalarning hammasi; Faza 0 baseline'i
  (`../Tungi_natijalar/2026-09-29/regression.jsonl`)
- Produces: `scripts/faza2_taqqos.py` — `taqqosla(yangi_jsonl, baseline_jsonl) -> dict`

**Chiqish mezoni (spetsifikatsiyadan):**
1. 548 auto case yuritiladi;
2. Faza 0 baseline'iga nisbatan **Fail soni oshmagan** (baseline: Fail 317 / Pass 231 /
   Skip 310);
3. assert'li case ulushi **100%** (12-vazifada bajarildi).

**Nega taqqoslash skripti kerak.** «Fail soni oshmagan» ni ko'z bilan tekshirish mumkin
emas: case'lar boshqacha (assert'lar qo'shilgan), shuning uchun yangi yiqilishlar paydo
bo'lishi TABIIY — qo'shilgan assert haqiqiy bug'ni topgan bo'lishi mumkin. Taqqoslash
har case'ni baseline'dagi holati bilan solishtirib **to'rt guruhga** ajratadi:

| Guruh | Ma'nosi |
|---|---|
| `YAXSHILANDI` | baseline Fail → hozir Pass |
| `YANGI_FAIL` | baseline Pass → hozir Fail — **eng muhim guruh** |
| `BIR_XIL` | ikkalasida ham bir xil |
| `YANGI_ASSERT_TOPDI` | baseline Pass → hozir Fail VA yiqilgan qadam generatsiya
qilingan assert |

Oxirgi guruh alohida: u **regressiya emas, yutuq** — avtotest ilgari ko'rmagan
muammoni topdi. Uni `YANGI_FAIL` ga qo'shib hisoblash chiqish mezonini noto'g'ri
buzardi.

- [ ] **Qadam 1: Taqqoslash skripti uchun yiqiladigan testni yozish**

`tests/test_faza2_taqqos.py`:

```python
# -*- coding: utf-8 -*-
import json

from scripts.faza2_taqqos import taqqosla


def _jsonl(yol, qatorlar):
    yol.write_text("\n".join(json.dumps(q, ensure_ascii=False) for q in qatorlar),
                   encoding="utf-8")
    return yol


def test_yaxshilangan_case_aniqlanadi(tmp_path):
    baza = _jsonl(tmp_path / "b.jsonl", [{"id": "TC-A", "result": "Fail"}])
    yangi = _jsonl(tmp_path / "y.jsonl", [{"id": "TC-A", "result": "Pass"}])

    n = taqqosla(yangi, baza)

    assert n["YAXSHILANDI"] == ["TC-A"]


def test_yangi_fail_aniqlanadi(tmp_path):
    baza = _jsonl(tmp_path / "b.jsonl", [{"id": "TC-A", "result": "Pass"}])
    yangi = _jsonl(tmp_path / "y.jsonl",
                   [{"id": "TC-A", "result": "Fail", "failed_desc": "«Создать» ni bosing"}])

    n = taqqosla(yangi, baza)

    assert n["YANGI_FAIL"] == ["TC-A"]


def test_generatsiya_qilingan_assert_topgan_fail_alohida(tmp_path):
    """Bu regressiya EMAS, yutuq: avtotest ilgari ko'rmagan muammoni topdi."""
    baza = _jsonl(tmp_path / "b.jsonl", [{"id": "TC-A", "result": "Pass"}])
    yangi = _jsonl(tmp_path / "y.jsonl",
                   [{"id": "TC-A", "result": "Fail",
                     "failed_desc": "Tekshirish: «Организации» sahifasi ochiladi."}])

    n = taqqosla(yangi, baza)

    assert n["YANGI_ASSERT_TOPDI"] == ["TC-A"]
    assert n["YANGI_FAIL"] == []


def test_takroriy_qator_oxirgisi_olinadi(tmp_path):
    """Qayta yuritish faylga qo'shib yozadi — oxirgi yozuv haqiqiy natija."""
    baza = _jsonl(tmp_path / "b.jsonl", [{"id": "TC-A", "result": "Pass"}])
    yangi = _jsonl(tmp_path / "y.jsonl", [{"id": "TC-A", "result": "Fail"},
                                          {"id": "TC-A", "result": "Pass"}])

    n = taqqosla(yangi, baza)

    assert n["YANGI_FAIL"] == [] and n["BIR_XIL"] == ["TC-A"]


def test_xulosa_sonlari(tmp_path):
    baza = _jsonl(tmp_path / "b.jsonl", [{"id": "TC-A", "result": "Fail"},
                                          {"id": "TC-B", "result": "Pass"}])
    yangi = _jsonl(tmp_path / "y.jsonl", [{"id": "TC-A", "result": "Pass"},
                                           {"id": "TC-B", "result": "Pass"}])

    n = taqqosla(yangi, baza)

    assert n["xulosa"]["yangi_fail"] == 0
    assert n["xulosa"]["yaxshilandi"] == 1
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_faza2_taqqos.py -v
```

Kutilgan: `ModuleNotFoundError` — FAIL.

- [ ] **Qadam 3: `scripts/faza2_taqqos.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Faza 2 natijasini Faza 0 baseline'i bilan taqqoslaydi.

Chiqish mezoni «Fail soni oshmagan» ni ko'z bilan tekshirish mumkin emas: case'lar
boshqacha (assert'lar qo'shilgan), shuning uchun yangi yiqilishlar paydo bo'lishi
TABIIY — qo'shilgan assert haqiqiy bug'ni topgan bo'lishi mumkin.

Ishlatish: python3 scripts/faza2_taqqos.py <yangi.jsonl> <baseline.jsonl>
"""
import argparse
import json
import sys
from pathlib import Path

GENERATSIYA_BELGISI = "Tekshirish:"


def _oxirgilar(yol):
    """Har `id` uchun OXIRGI yozuv. Qayta yuritish faylga qo'shib yozadi."""
    natija = {}
    for satr in Path(yol).read_text(encoding="utf-8").splitlines():
        if satr.strip():
            r = json.loads(satr)
            natija[r["id"]] = r
    return natija


def taqqosla(yangi_jsonl, baseline_jsonl):
    """To'rt guruhga ajratadi va xulosa sonlarini beradi."""
    yangi = _oxirgilar(yangi_jsonl)
    baza = _oxirgilar(baseline_jsonl)
    guruh = {"YAXSHILANDI": [], "YANGI_FAIL": [], "BIR_XIL": [],
             "YANGI_ASSERT_TOPDI": [], "FAQAT_YANGIDA": []}

    for cid, r in sorted(yangi.items()):
        b = baza.get(cid)
        if b is None:
            guruh["FAQAT_YANGIDA"].append(cid)
            continue
        if b.get("result") == r.get("result"):
            guruh["BIR_XIL"].append(cid)
        elif b.get("result") == "Fail" and r.get("result") == "Pass":
            guruh["YAXSHILANDI"].append(cid)
        elif r.get("result") == "Fail":
            # Generatsiya qilingan assert topgan yiqilish — regressiya EMAS, yutuq
            if str(r.get("failed_desc") or "").startswith(GENERATSIYA_BELGISI):
                guruh["YANGI_ASSERT_TOPDI"].append(cid)
            else:
                guruh["YANGI_FAIL"].append(cid)
        else:
            guruh["BIR_XIL"].append(cid)

    guruh["xulosa"] = {
        "yangi_case": len(yangi), "baseline_case": len(baza),
        "yangi_fail": len(guruh["YANGI_FAIL"]),
        "yaxshilandi": len(guruh["YAXSHILANDI"]),
        "yangi_assert_topdi": len(guruh["YANGI_ASSERT_TOPDI"]),
        "bir_xil": len(guruh["BIR_XIL"]),
    }
    return guruh


def main(argv=None):
    p = argparse.ArgumentParser(description="Faza 2 natijasini baseline bilan taqqoslaydi")
    p.add_argument("yangi")
    p.add_argument("baseline")
    a = p.parse_args(argv)

    n = taqqosla(a.yangi, a.baseline)
    print(json.dumps(n["xulosa"], ensure_ascii=False, indent=1))
    if n["YANGI_FAIL"]:
        print("\nYANGI FAIL (regressiya nomzodlari):")
        for cid in n["YANGI_FAIL"]:
            print("  -", cid)
    if n["YANGI_ASSERT_TOPDI"]:
        print("\nYANGI ASSERT TOPDI (yutuq, regressiya emas):")
        for cid in n["YANGI_ASSERT_TOPDI"][:20]:
            print("  -", cid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Qadam 4: Kichik to'plamda jonli sinash (10 case)**

```bash
cd ../SmartUp_Autotest && set -a; . ../.env; set +a && \
  RESULTS_DIR="$(cd .. && pwd)/Tungi_natijalar/_faza2_login" npx playwright test --project=setup
cd ../Avtotest_POM
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest tests/test_regression.py --live \
  --modules Главное --results /tmp/faza2-sinov -q 2>&1 | tail -20
```

Kutilgan: case'lar yuritiladi va `/tmp/faza2-sinov/regression.jsonl` paydo bo'ladi.
Hammasi yiqilsa — to'xta, sabab bitta (masalan sessiya yoki menyu) va uni tuzat.

```bash
head -2 /tmp/faza2-sinov/regression.jsonl | .venv/bin/python -m json.tool --json-lines 2>/dev/null \
  || head -2 /tmp/faza2-sinov/regression.jsonl
ls /tmp/faza2-sinov/shots/ | head -5
```

- [ ] **Qadam 5: `bug_report.py` ni yangi natijada yuritish**

```bash
.venv/bin/python scripts/bug_report.py /tmp/faza2-sinov \
  --cases data/regression_cases.json \
  --known ../SmartUp_Autotest/data/known_bugs.json
ls /tmp/faza2-sinov/Buglar/
```

Kutilgan: `XULOSA.md` va modul papkalari yaratiladi. Xato chiqsa yozuv formati mos
kelmagan — to'xta va xabar ber.

- [ ] **Qadam 6: To'liq yugurish (548 case)**

```bash
cd ../SmartUp_Autotest && set -a; . ../.env; set +a && \
  RESULTS_DIR="$(cd .. && pwd)/Tungi_natijalar/_faza2_login" npx playwright test --project=setup
cd ../Avtotest_POM
KUN=$(date +%F)
PYTHONDONTWRITEBYTECODE=1 nohup .venv/bin/pytest tests/test_regression.py --live \
  --results "../Tungi_natijalar/${KUN}_faza2" \
  > "../Tungi_natijalar/${KUN}_faza2-run.log" 2>&1 &
echo "boshlandi, log: ../Tungi_natijalar/${KUN}_faza2-run.log"
```

**Diqqat:** bu bir necha soat davom etadi. Yugurish davomida `Avtotest_POM/` yoki
`SmartUp_Autotest/` ichida `playwright install` YURITMA — ikki loyiha brauzer keshini
bo'lishmasligi uchun ajratilgan, lekin ehtiyot bo'l. Faza 1 da aynan shu 132 ta
ishlab turgan case'ni o'ldirgan.

- [ ] **Qadam 7: Taqqoslash va chiqish mezonini tekshirish**

```bash
KUN=$(date +%F)
.venv/bin/python scripts/faza2_taqqos.py \
  "../Tungi_natijalar/${KUN}_faza2/regression.jsonl" \
  ../Tungi_natijalar/2026-09-29/regression.jsonl
```

Chiqish mezoni: `yangi_fail` **0** bo'lishi kerak. Noldan katta bo'lsa har birini alohida
tekshir: yiqilish ijrochining nuqsonimi yoki haqiqiy regressiyami. Ijrochining nuqsoni
bo'lsa tuzat va qayta yurit; haqiqiy regressiya bo'lsa `bug_report.py` hisobotini
tekshirib foydalanuvchiga ko'rsat.

- [ ] **Qadam 8: Bug hisobotlarini generatsiya qilish**

```bash
KUN=$(date +%F)
.venv/bin/python scripts/bug_report.py "../Tungi_natijalar/${KUN}_faza2" \
  --cases data/regression_cases.json \
  --known ../SmartUp_Autotest/data/known_bugs.json
cat "../Tungi_natijalar/${KUN}_faza2/Buglar/XULOSA.md"
```

- [ ] **Qadam 9: Natija hujjatini yozish**

`Hujjatlar/<sana>-faza2-natija.md` — Faza 0 natija hujjati bilan bir xil shaklda:
maqsad, o'lchangan sonlar, taqqoslash guruhlari, topilgan nuqsonlar, yetkazilgan
artefaktlar, keyingi fazaga qolgan masalalar.

- [ ] **Qadam 10: README ni yangilash va commit**

`README.md` da «Hozirgi bosqich» ni Faza 2 ga o'zgartir; yuritish buyruqlariga
`PYTHONDONTWRITEBYTECODE=1` va `--cases`/`--modules`/`--types`/`--results`
bayroqlarini yoz.

```bash
git add scripts/faza2_taqqos.py tests/test_faza2_taqqos.py README.md
git commit -m "$(cat <<'EOF'
feat(faza2): baseline bilan taqqoslash va chiqish mezoni

«Fail soni oshmagan» ni ko'z bilan tekshirish mumkin emas: case'lar
o'zgargan (assert'lar qo'shilgan), shuning uchun yangi yiqilish tabiiy.
Taqqoslash to'rt guruhga ajratadi va generatsiya qilingan assert topgan
yiqilishni alohida hisoblaydi — u regressiya emas, yutuq.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Xavflar

| Xavf | Ehtimoli | Nima qilinadi |
|---|---|---|
| Sessiya uzoq yugurishda tugaydi | Yuqori | 9-vazifa: har case boshida qayta login; `relogin.jsonl` ga yoziladi |
| Generatsiya qilingan assert noto'g'ri («Pass» o'rniga soxta «Fail») | O'rta | 12-vazifa 9-qadam: 20 namunani QO'LDA ko'rish; 13-vazifa taqqoslashda ular alohida guruh |
| Eski UI (BIRUNI) case'lari ishlamaydi | O'rta | Eski UI ga faqat menyu orqali o'tiladi (Faza 1 qarori); yiqilsa `AVTOTEST` toifasida ko'rinadi |
| 548 case juda sekin | O'rta | 11-vazifa: brauzer va kontekst sessiya doirasida |
| Tarmoq uzilishi butun yugurishni bekor qiladi | O'rta | Faza 5 ga qoldirilgan (`retries`); hozir `--cases` bilan qayta yuritiladi |
| `bug_report.py` yangi formatni o'qimaydi | Past | 10-vazifa 6-qadam va 13-vazifa 5-qadamda tekshiriladi |

## Faza 3 ga qoldiriladigan masalalar

- `retries` va tarmoq uzilishiga qarshi himoya (Faza 5 reja bo'yicha)
- Allure hisoboti (`allure_helper.py` porti)
- Telegram xabarnomasi (`telegram.py` porti)
- Tungi zanjir (`nightly.sh` ekvivalenti) va eski loyihalarni `_arxiv/` ga ko'chirish
- `auto=false` 310 case'ni ko'rib chiqish: qaysi biri endi avtomatlashtirilishi mumkin

---

## O'z-o'zini tekshirish

**1. Spetsifikatsiya qamrovi.** Spetsifikatsiyaning Faza 2 bo'limi to'rt narsani talab
qiladi:

| Talab | Vazifa |
|---|---|
| 28 mavjud action → POM chaqiruvlari | 5, 6, 7, 8 (31 action, o'lchangan son) |
| Yetishmayotgan 5 action: `menu_plus`, `remove_tag`, `assert_download`, `assert_no_request`, `manual` | 5 (`menu_plus`, `manual`), 6 (`remove_tag`), 7 (`assert_download`, `assert_no_request`) |
| Assert'siz 245 case tuzatiladi | 12 |
| `run_order.json` tartibi saqlanadi | 1 (`phase`+`seq` bo'yicha tartiblash) |

Chiqish mezoni (548 case, Fail oshmagan, assert 100%) — 13-vazifa.

**Chetlanish:** spetsifikatsiya assert'lar `test_cases.md` dan generatsiya qilinadi
deydi. O'lchash ko'rsatdi: `expected` matni allaqachon JSON ichida (2362 qadamdan 2188
tasida). Shuning uchun generator JSON dan ishlaydi — bu sodda va tekshiriladigan.

**Chetlanish:** ijrochi `tests/json_driven/actions.py` emas, `runner/actions.py` da.
Sabab: bu kutubxona kodi, test emas; bu loyihada `tests/` faqat testlarni saqlaydi.

**2. Joy tutuvchi (placeholder) tekshiruvi.** «TBD», «TODO», «keyinroq», «shunga
o'xshash» iboralari yo'q. Har kod qadami to'liq kod bilan. 13-vazifaning 9-qadami
(natija hujjati) va 10-qadami (README) matn yozish — ular uchun aniq tarkib ko'rsatilgan.

**3. Tur (tip) mosligi.**

- `Case` namedtuple maydonlari 1-vazifada ta'riflangan va 10-vazifada (`yangi_yozuv`,
  `fail_deb_belgila`) hamda 11-vazifada ishlatilgan — nomlar bir xil.
- `Ctx(page, pom, net, data)` 5-vazifada ta'riflangan; 6, 7, 8 vazifalar shu imzoni
  ishlatadi; 11-vazifa `Ctx(page=..., pom=..., net=..., data=...)` deb chaqiradi.
- `Collector.bad` / `.console` / `.i18n_404()` / `.http_errors()` / `.reset()` —
  2-vazifada ta'riflangan, 7 va 11 vazifalarda ishlatilgan.
- `Assertions` metodlari `text(items)`, `buttons(names)` RO'YXAT oladi (satr emas) —
  7-vazifada `matn_elementlari(...)` natijasi uzatiladi.
- `Grid.expect_row(cells)` ro'yxat oladi — 7-vazifada `qator_kataklari(...)` uzatiladi.
- `Evidence.skrinshot()` NISBIY satr (`shots/REG-<id>.png`) qaytaradi — 10-vazifada
  `fail_deb_belgila(..., shot=...)` shu satrni oladi.
- `sessiyani_taminla(...)` `bool` qaytaradi — 11-vazifa shu qiymatga qarab
  `relogin.jsonl` yozadi.
- `assert_yasa(step, oldingi)` — 12-vazifada ta'riflangan va `case_ga_qosh` shu imzo
  bilan chaqiradi.

**Aniqlangan va tuzatilgan nomuvofiqlik:** 12-vazifa uch yangi action
(`assert_required`, `assert_count`, `assert_enabled`) talab qiladi, lekin ular 7-vazifada
yo'q edi. Shuning uchun 12-vazifaning 1 va 2-qadamlari ularni qo'shadi — generator
ulardan foydalanishdan OLDIN.

**Aniqlangan xavf:** 11-vazifada `tests/test_regression.py` `conftest.py` dagi
`FOYDALANUVCHI` konstantasini ishlatadi, lekin conftest'ni modul sifatida import qilish
noto'g'ri. Shuning uchun 11-vazifa 4-qadamida `foydalanuvchi` sessiya fixture'ini
qo'shish aniq ko'rsatilgan.

**Aniqlangan va tuzatilgan nomuvofiqlik:** 6-vazifa testlari `FakePage` da `pressed()`,
`typed_sequentially()` va `keyboard_calls()` yordamchilarini talab qiladi. Tekshirildi
(2026-09-30): `clicked()` va `filled()` bor, qolgan uchtasi YO'Q. Shuning uchun 6-vazifaga
`Qadam 1b` qo'shildi — u yordamchilarni kodi bilan qo'shadi va `tests/test_fake_page.py`
da test bilan qamraydi.

**Tekshirilgan farazlar:** `scripts/bug_report.py` da `categorize(row, known_routes)` va
`severity(row, category)` imzolari mavjud (10-vazifa 6-qadami va 13-vazifa 5-qadami
shularga tayanadi). `conftest.py` da `pytest_addoption`, `_playwright` fixture'i,
`import os` va `from pathlib import Path` allaqachon bor (11-vazifa shularga qo'shadi).
