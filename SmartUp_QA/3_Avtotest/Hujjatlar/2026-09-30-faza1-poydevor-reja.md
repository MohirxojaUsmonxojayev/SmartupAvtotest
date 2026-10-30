# Faza 1 — Poydevor: implementatsiya rejasi

> **Agent ishchilar uchun:** MAJBURIY SUB-SKILL: bu rejani vazifa-ba-vazifa bajarish uchun
> `superpowers:subagent-driven-development` (tavsiya) yoki `superpowers:executing-plans`
> ishlating. Qadamlar `- [ ]` checkbox sintaksisida.

**Maqsad:** `Avtotest_POM/` da POM poydevorini qurish — `UiDriver` selektor qatlami
(a2 + eski biruni UI), 5 ta komponent (Grid, Form, Dialog, Menu, Report), `BasePage`,
`PageFactory` va `conftest` fixture'lari — shunda Faza 2 (858 JSON case) va Faza 3–4
(legacy testlar porti) shu poydevor ustiga qurilsin.

**Arxitektura:** `UiDriver` — sof `dataclass`, selektor **matnlarini** saqlaydi, `Locator`
qaytarmaydi va brauzerga tegmaydi. Komponentlar `(page, driver)` juftligini oladi va DOM ga
faqat `driver` selektorlari orqali murojaat qiladi. Shu sababli butun poydevor brauzersiz,
`FakePage` bilan test qilinadi (testlar sekundlarda yuradi). Jonli tekshiruv alohida
`@pytest.mark.live` markeri bilan, faqat so'ralganda yuriladi.

**Tech Stack:** Python 3.12+, pytest 8.4.2, Playwright (Python), `python-dotenv`,
`allure-pytest`.

**Spec:** `3_Avtotest/Hujjatlar/2026-09-29-pom-birlashtirish-design.md`
**Faza 0 natijasi (selektor dalillari):** `3_Avtotest/Tungi_natijalar/2026-09-29/BASELINE.md`

## Global cheklovlar

- Avtotest fayllari faqat `3_Avtotest/` ichida (CLAUDE.md 1-qoida).
- Maxfiy ma'lumotlar: `3_Avtotest/.env` (namuna `.env.example`, `chmod 600`). Parol/token
  kod, hujjat, log yoki commit'ga **yozilmaydi** (CLAUDE.md 4-qoida).
- Natija papkalari: `3_Avtotest/Tungi_natijalar/<YYYY-MM-DD>/` (CLAUDE.md 2-qoida).
- Tashqi tizimlarga (WMS, Soliq, Faktura, Telegram biznes-oqimi, CRPT) hech narsa yuborilmaydi.
- Foydalanuvchi/huquq/sozlamalar o'zgartirilmaydi; faqat `QA-`/`SIM-` yozuvlar o'chiriladi.
- Nomlash: kodda va hujjatda **`order`**, `zakaz` emas.
- `3_Avtotest/SmartUp_Autotest/` — faqat o'qish (manba ma'lumot: `data/*.json`).
- Hujjat, izoh va test nomlari o'zbek tilida. SmartUp UI matnlari rus tilida qoladi.
- Git commit xabarlari oxirida: `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

### Faza 0 dan kelgan majburiy qoida — JIMGINA YUTISH TAQIQLANADI

Faza 0 uchta nuqson topdi va uchalasi bir xil sinfda edi: **kod ishlamay turgan, lekin
hech narsa demagan.**

| Nuqson | Natijasi |
|---|---|
| `switchFilial` eski selektorda, chaqiruv `.catch()` da | butun yugurish noto'g'ri filialda, 7 sahifa soxta 403 |
| `expect.soft` istisno tashlamaydi | 82 yiqilish `Pass` deb yozilgan, isbotsiz |
| `analyze.py` URL normalizatsiyasi bir tomonlama | 19 ma'lum bug «YANGI» deb ko'rsatilgan |

Shuning uchun bu fazada:

1. **`except Exception: pass` va `.catch(() => ...)` ekvivalenti ishlatilmaydi.** Selektor
   topilmasa — xato tashlanadi yoki hech bo'lmaganda `logger` ga yoziladi.
2. **Har bir "topilmasa muqobilini sina" yo'li aniq nomlanadi** (`ALIAS`) va sinash natijasi
   ham topilmasa — xato tashlanadi.
3. **Har bir avtomatik aniqlash (`detect`) muvaffaqiyatsiz bo'lsa xato tashlaydi**, sukut
   bo'yicha birortasiga o'tib ketmaydi.

---

## Fayl tuzilmasi

| Fayl | Mas'uliyati |
|---|---|
| `requirements.txt` | Playwright, dotenv, allure qo'shiladi |
| `pytest.ini` | markerlar: `live`, `smoke`, `regression`, `bug`, `json_driven` |
| `conftest.py` | `.env` yuklash, `--live` bayrog'i, `page`/`ui`/`soft` fixture'lari |
| `tests/fake_page.py` | `FakePage` / `FakeLocator` — brauzersiz test infratuzilmasi |
| `pages/ui/driver.py` | `UiDriver` dataclass — selektor to'plamining shakli |
| `pages/ui/a2.py` | `A2` — yangi Angular selektorlari (Faza 0 da o'lchangan) |
| `pages/ui/biruni.py` | `BIRUNI` — eski AngularJS selektorlari (legacy `base_page.py` dan) |
| `pages/ui/detect.py` | `detect(page)` — qaysi UI ekanini aniqlaydi, topolmasa xato tashlaydi |
| `pages/components/buttons.py` | `find_button()` + `ALIAS` qo'llash (reliz nomlari o'zgarishi) |
| `pages/components/grid.py` | ro'yxat: qator, amal tugmasi, ustunlar, qidiruv |
| `pages/components/form.py` | maydonlar: yozish, sana, tanlash, switch, radio, saqlash |
| `pages/components/dialog.py` | tasdiq/xato oynalari |
| `pages/components/menu.py` | menyu navigatsiyasi, `+`, filial almashtirish |
| `pages/components/report.py` | hisobot formalari: generatsiya, yuklab olish |
| `pages/base_page.py` | ~100 qator: `open`, `heading`, `main`, komponentlarni yig'ish |
| `pages/factory.py` | `PageFactory` + `GenericPage` |
| `utils/soft_assert.py` | `SoftAssert` porti (Smartupauto'dan, Telegram bog'liqligi olib tashlangan) |
| `tests/live/test_live_smoke.py` | 2 ta jonli tekshiruv: a2 ro'yxat + eski UI forma |

Har komponent bitta faylda va 150 qatordan oshmaydi. `BasePage` 100 qatordan oshmaydi —
bu spec ning muvaffaqiyat mezoni (hozirgi legacy `base_page.py` 791 qator).

---

## Vazifa 1: Muhit — Playwright, `.env` yuklash, markerlar

**Fayllar:**
- Modify: `3_Avtotest/Avtotest_POM/requirements.txt`
- Modify: `3_Avtotest/Avtotest_POM/pytest.ini`
- Create: `3_Avtotest/Avtotest_POM/conftest.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_conftest_env.py`

**Interfeyslar:**
- Consumes: yo'q
- Produces:
  - `load_env(path: Path) -> dict[str, str]` — `.env` faylini o'qib `os.environ` ga qo'yadi
    va qo'yilgan kalitlarni qaytaradi; fayl yo'q bo'lsa `{}`
  - `pytest.ini` markerlari: `live`, `smoke`, `regression`, `bug`, `json_driven`
  - `--live` bayrog'i: berilmasa `live` markerli testlar `skip`

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_conftest_env.py`:

```python
import os

from conftest import load_env


def test_load_env_faylni_oqib_environga_qoyadi(tmp_path, monkeypatch):
    f = tmp_path / ".env"
    f.write_text("# izoh\nA_KALIT=qiymat1\nB_KALIT=qiymat2\n\n", encoding="utf-8")
    monkeypatch.delenv("A_KALIT", raising=False)
    monkeypatch.delenv("B_KALIT", raising=False)

    qoyilgan = load_env(f)

    assert qoyilgan == {"A_KALIT": "qiymat1", "B_KALIT": "qiymat2"}
    assert os.environ["A_KALIT"] == "qiymat1"


def test_load_env_mavjud_qiymatni_ustidan_yozmaydi(tmp_path, monkeypatch):
    """Muhit o'zgaruvchisi allaqachon berilgan bo'lsa (masalan CI da) u ustun turadi."""
    f = tmp_path / ".env"
    f.write_text("A_KALIT=fayldan\n", encoding="utf-8")
    monkeypatch.setenv("A_KALIT", "muhitdan")

    qoyilgan = load_env(f)

    assert qoyilgan == {}
    assert os.environ["A_KALIT"] == "muhitdan"


def test_load_env_fayl_yoq_bolsa_bosh(tmp_path):
    assert load_env(tmp_path / "yoq.env") == {}
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/Avtotest_POM
.venv/bin/pytest tests/test_conftest_env.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'conftest'` yoki
`ImportError: cannot import name 'load_env'` — FAIL.

- [ ] **Qadam 3: `conftest.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Umumiy fixture'lar va muhit sozlamalari.

Maxfiy ma'lumotlar `3_Avtotest/.env` da (CLAUDE.md 4-qoida) — u hech qanday git
repozitoriysi ichida emas, shuning uchun uni bu papkaga KO'CHIRMA.
"""
import os
from pathlib import Path

import pytest

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def load_env(path=ENV_FILE):
    """`KALIT=qiymat` satrlarini o'qib `os.environ` ga qo'yadi.

    Allaqachon berilgan muhit o'zgaruvchisi ustun turadi (CI da qiymat tashqaridan
    keladi). Fayl yo'q bo'lsa {} qaytaradi — bu xato emas, lekin login ishlamaydi.
    Qaytaradi: aynan shu chaqiruvda qo'yilgan kalitlar.
    """
    path = Path(path)
    if not path.exists():
        return {}
    qoyilgan = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        kalit, _, qiymat = line.partition("=")
        kalit, qiymat = kalit.strip(), qiymat.strip()
        if not kalit or kalit in os.environ:
            continue
        os.environ[kalit] = qiymat
        qoyilgan[kalit] = qiymat
    return qoyilgan


def pytest_addoption(parser):
    parser.addoption("--live", action="store_true", default=False,
                     help="jonli (brauzer + server) testlarni ham yurit")


def pytest_configure(config):
    load_env()


def pytest_collection_modifyitems(config, items):
    if config.getoption("--live"):
        return
    sabab = pytest.mark.skip(reason="jonli test — `--live` bayrog'i bilan yuriladi")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(sabab)
```

- [ ] **Qadam 4: `pytest.ini` ni yangilash**

```ini
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
addopts = -q
markers =
    live: brauzer va real serverni talab qiladi (`--live` bilan yuriladi)
    smoke: smoke to'plami
    regression: regression to'plami
    bug: ma'lum bug uchun test
    json_driven: regression_cases.json dan yuritiladigan case
```

- [ ] **Qadam 5: `requirements.txt` ni yangilash**

```
pytest==8.4.2
playwright==1.60.0
pytest-playwright==0.7.1
allure-pytest==2.15.3
```

**Versiyalar haqida.** `pytest-playwright==0.7.2` PyPI da YO'Q (eng yangisi `0.7.1`).
`playwright` uchun Python maksimumi `1.60.0`, JS to'plami esa `@playwright/test 1.63.0`
ishlatadi — ular tenglashmaydi. Shu sababli brauzerlar ALOHIDA papkada saqlanadi
(quyidagi 8-qadam), aks holda bir loyihaning `playwright install` i boshqasining
brauzerini «ishlatilmayapti» deb o'chirib yuboradi. 30.09 da aynan shunday bo'lgan:
Python o'rnatishi yugurib turgan JS to'plamini buzdi va 132 case yo'qoldi.

`python-dotenv` QO'SHILMAYDI — `load_env()` 20 qator va bizga kerakli aniq xatti-harakatni
beradi (mavjud muhit o'zgaruvchisi ustun turadi), tashqi bog'liqlik ortiqcha.

- [ ] **Qadam 6: Paketlarni o'rnatish va testni yuritish**

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium
.venv/bin/pytest -q
```

Kutilgan: `92 passed` (89 mavjud + 3 yangi). Mavjud 89 tadan birortasi buzilsa TO'XTA.

- [ ] **Qadam 7: Commit**

```bash
git add requirements.txt pytest.ini conftest.py tests/test_conftest_env.py
git commit -m "$(cat <<'EOF'
feat(faza1): muhit — Playwright, .env yuklash, live markeri

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Vazifa 2: `FakePage` — brauzersiz test infratuzilmasi

**Fayllar:**
- Create: `3_Avtotest/Avtotest_POM/tests/fake_page.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_fake_page.py`

**Interfeyslar:**
- Consumes: yo'q
- Produces:
  - `FakePage(counts: dict[str, int] | None = None, texts: dict[str, str] | None = None, lists: dict[str, list[str]] | None = None)`
    — `locator(sel) -> FakeLocator`, `url: str`, `calls: list[tuple]`
  - `FakeLocator` — `locator()`, `filter(**kw)`, `.first`, `.last`, `count()`, `click()`,
    `fill(v)`, `press(k)`, `inner_text()`, `all_inner_texts()`, `wait_for()`,
    `is_visible()`, `get_attribute(name)`; `key` — zanjirning matn ko'rinishi

**Nega kerak.** Faza 0 ning darsi: pytest ichida o'tgan 88 test skriptni CLI da ishga
tushirmagani uchun `ModuleNotFoundError` ni ushlamadi. Komponentlar uchun ham xuddi shunday
xavf bor — brauzer kerak bo'lsa test yozilmaydi, yozilmasa nuqson ko'rinmaydi.
`FakePage` DOM ni taqlid qilmaydi; u faqat **qaysi selektor so'ralgani va qaysi ketma-ketlikda
amal bajarilgani** ni qayd etadi. Selektor xaritasi aynan shu joyda buziladi.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_fake_page.py`:

```python
from tests.fake_page import FakePage


def test_locator_zanjiri_kalit_yasaydi():
    page = FakePage()

    loc = page.locator("main").last.locator(".smt-data-row").first

    assert loc.key == "main >> last >> .smt-data-row >> first"


def test_count_berilgan_qiymatni_qaytaradi():
    page = FakePage(counts={"main >> last": 1, ".yoq": 0})

    assert page.locator("main").last.count() == 1
    assert page.locator(".yoq").count() == 0
    assert page.locator(".hech-qachon-berilmagan").count() == 0


def test_click_va_fill_qayd_etiladi():
    page = FakePage()

    page.locator("button").first.click()
    page.locator("input").fill("QA-1")

    assert ("click", "button >> first") in page.calls
    assert ("fill", "input", "QA-1") in page.calls


def test_filter_kaliti_barqaror():
    page = FakePage()

    a = page.locator("button").filter(has_text="Создать")
    b = page.locator("button").filter(has_text="Создать")

    assert a.key == b.key
    assert "has_text='Создать'" in a.key


def test_inner_text_va_all_inner_texts():
    page = FakePage(texts={"main >> last": "Организации"},
                    lists={"main >> last >> smt-cell-header": ["№", "Название"]})

    assert page.locator("main").last.inner_text() == "Организации"
    assert page.locator("main").last.locator("smt-cell-header").all_inner_texts() == ["№", "Название"]
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_fake_page.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'tests.fake_page'` — FAIL.

- [ ] **Qadam 3: `tests/fake_page.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Brauzersiz test uchun Playwright `Page`/`Locator` taqlidi.

DOM ni taqlid QILMAYDI — faqat qaysi selektor so'ralgani va qaysi amal bajarilgani
qayd etiladi. Komponentlarning selektor xaritasi aynan shu joyda tekshiriladi.
"""


class FakeLocator:
    def __init__(self, page, path):
        self.page = page
        self.path = tuple(path)

    # ---------------------------------------------------------------- zanjir
    @property
    def key(self):
        return " >> ".join(self.path)

    def locator(self, selector):
        return FakeLocator(self.page, self.path + (selector,))

    def filter(self, **kwargs):
        tag = "filter(%s)" % ", ".join("%s=%r" % (k, v) for k, v in sorted(kwargs.items()))
        return FakeLocator(self.page, self.path + (tag,))

    def nth(self, index):
        return FakeLocator(self.page, self.path + ("nth(%d)" % index,))

    @property
    def first(self):
        return FakeLocator(self.page, self.path + ("first",))

    @property
    def last(self):
        return FakeLocator(self.page, self.path + ("last",))

    # ---------------------------------------------------------------- so'rovlar
    def count(self):
        self.page.calls.append(("count", self.key))
        return self.page.counts.get(self.key, 0)

    def inner_text(self):
        self.page.calls.append(("inner_text", self.key))
        return self.page.texts.get(self.key, "")

    def all_inner_texts(self):
        self.page.calls.append(("all_inner_texts", self.key))
        return list(self.page.lists.get(self.key, []))

    def is_visible(self):
        self.page.calls.append(("is_visible", self.key))
        return self.page.counts.get(self.key, 0) > 0

    def get_attribute(self, name):
        self.page.calls.append(("get_attribute", self.key, name))
        return self.page.attrs.get((self.key, name))

    # ---------------------------------------------------------------- amallar
    def click(self, **kwargs):
        self.page.calls.append(("click", self.key))

    def fill(self, value, **kwargs):
        self.page.calls.append(("fill", self.key, value))

    def press(self, key, **kwargs):
        self.page.calls.append(("press", self.key, key))

    def wait_for(self, **kwargs):
        self.page.calls.append(("wait_for", self.key))


class FakePage:
    def __init__(self, counts=None, texts=None, lists=None, attrs=None, url=""):
        self.counts = dict(counts or {})
        self.texts = dict(texts or {})
        self.lists = dict(lists or {})
        self.attrs = dict(attrs or {})
        self.url = url
        self.calls = []

    def locator(self, selector):
        return FakeLocator(self, (selector,))

    def goto(self, url, **kwargs):
        self.calls.append(("goto", url))
        self.url = url

    def wait_for_timeout(self, ms):
        self.calls.append(("wait_for_timeout", ms))

    def keyboard_press(self, key):
        self.calls.append(("keyboard_press", key))

    # `calls` ni o'qishni osonlashtiruvchi yordamchilar
    def clicked(self):
        return [k for (a, k, *_) in self.calls if a == "click"]

    def filled(self):
        return [(k, v) for (a, k, *rest) in self.calls if a == "fill" for v in rest[:1]]
```

- [ ] **Qadam 4: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_fake_page.py -v
```

Kutilgan: `5 passed`. Keyin butun to'plam: `.venv/bin/pytest -q` → `98 passed`.

- [ ] **Qadam 5: Commit**

```bash
git add tests/fake_page.py tests/test_fake_page.py
git commit -m "$(cat <<'EOF'
feat(faza1): FakePage — komponentlarni brauzersiz test qilish infratuzilmasi

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Vazifa 3: `UiDriver` + `A2` + `BIRUNI` selektor to'plamlari

**Fayllar:**
- Create: `3_Avtotest/Avtotest_POM/pages/__init__.py`
- Create: `3_Avtotest/Avtotest_POM/pages/ui/__init__.py`
- Create: `3_Avtotest/Avtotest_POM/pages/ui/driver.py`
- Create: `3_Avtotest/Avtotest_POM/pages/ui/a2.py`
- Create: `3_Avtotest/Avtotest_POM/pages/ui/biruni.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_ui_driver.py`

**Interfeyslar:**
- Consumes: yo'q
- Produces:
  - `UiDriver` — `frozen=True` dataclass, maydonlari:
    `name: str`, `main: str`, `main_last: bool`, `rows: str`, `header: str`,
    `dialog: str`, `error_text: str`, `option_pane: str`, `switch: str`,
    `search_input: str`, `select_trigger: str`, `field_ancestor: str`,
    `detect: tuple[str, ...]`, `aliases: dict[str, str]`
  - `A2: UiDriver`, `BIRUNI: UiDriver`
  - `UiDriver.alias_of(text: str) -> str | None`

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_ui_driver.py`:

```python
import dataclasses

from pages.ui.a2 import A2
from pages.ui.biruni import BIRUNI
from pages.ui.driver import UiDriver


def test_ikkala_drayver_ham_bir_xil_maydonlarni_toldiradi():
    """Komponentlar faqat UiDriver maydonlariga tayanadi — biri bo'sh qolsa
    o'sha komponent jimgina ishlamay qoladi."""
    maydonlar = [f.name for f in dataclasses.fields(UiDriver)]

    for drayver in (A2, BIRUNI):
        for nom in maydonlar:
            qiymat = getattr(drayver, nom)
            assert qiymat not in (None, "", ()), "%s.%s bo'sh" % (drayver.name, nom)


def test_a2_selektorlari_faza0_da_olchangan_qiymatlar():
    assert A2.name == "a2"
    assert A2.rows == ".smt-data-row"
    assert A2.header == "smt-cell-header"
    assert A2.dialog == "[role=dialog]"
    assert A2.option_pane == ".cdk-overlay-pane"
    assert A2.main == "main" and A2.main_last is True
    assert ".smt-data-row" in A2.detect


def test_biruni_selektorlari_eski_ui():
    assert BIRUNI.name == "biruni"
    assert BIRUNI.rows == "b-grid .tbl-row"
    assert BIRUNI.main == "b-page" and BIRUNI.main_last is False
    assert "b-grid" in BIRUNI.detect


def test_drayver_ozgarmas():
    """Selektorlar ish vaqtida o'zgarmasligi kerak — aks holda bir test
    boshqasiga ta'sir qiladi."""
    try:
        A2.rows = ".boshqa"
    except dataclasses.FrozenInstanceError:
        return
    raise AssertionError("UiDriver frozen emas")


def test_alias_of_reliz_nomlarini_qaytaradi():
    """29.09 relizida tugma nomlari o'zgargan: Просмотреть→Просмотр, Создать→Добавить."""
    assert A2.alias_of("Просмотреть") == "Просмотр"
    assert A2.alias_of("Просмотр") == "Просмотреть"
    assert A2.alias_of("Создать") == "Добавить"
    assert A2.alias_of("Добавить") == "Создать"
    assert A2.alias_of("Сохранить") is None
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_ui_driver.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'pages'` — FAIL.

- [ ] **Qadam 3: Paket fayllarini va `driver.py` ni yozish**

```bash
mkdir -p pages/ui pages/components
touch pages/__init__.py pages/ui/__init__.py pages/components/__init__.py
```

`pages/ui/driver.py`:

```python
# -*- coding: utf-8 -*-
"""UI selektor to'plamining shakli.

`UiDriver` — SOF MA'LUMOT: faqat selektor matnlari. Brauzerga tegmaydi, `Locator`
qaytarmaydi. Shu sababli komponentlarning selektor xaritasini brauzersiz test qilish
mumkin (`tests/fake_page.py`).
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class UiDriver:
    """Bitta UI ning selektorlari.

    `main_last` — a2 da drawer/overlay o'z `<main>` i bilan ochiladi, shuning uchun eng
    ustki oyna = OXIRGI `<main>`. Eski UI da bitta `b-page` bo'ladi, birinchisi olinadi.
    `detect` — shu selektorlardan birortasi topilsa, sahifa shu UI da.
    `aliases` — reliz nomi o'zgarganda sinaladigan muqobil (masalan Просмотреть→Просмотр).
    """
    name: str
    main: str
    main_last: bool
    rows: str
    header: str
    dialog: str
    error_text: str
    option_pane: str
    switch: str
    search_input: str
    select_trigger: str
    field_ancestor: str
    detect: tuple
    aliases: dict = field(default_factory=dict)

    def alias_of(self, text):
        """Tugma matnining muqobil nomi yoki None."""
        return self.aliases.get(text)
```

- [ ] **Qadam 4: `pages/ui/a2.py` yozish**

```python
# -*- coding: utf-8 -*-
"""a2 (yangi Angular) UI selektorlari.

Faza 0 (2026-09-29, 226 sahifa) o'lchagan ishonch — `Tungi_natijalar/2026-09-29/BASELINE.md`:

    main               225/226  100%
    button:visible     222/226   98%
    label (maydon)      80/82    98%
    .smt-data-row       86/91    95%
    smt-cell-header    150/162   93%
    .cdk-overlay-pane    7/7     — «ishlamadi» holati qayd etilmaydi, o'lchov ishonchsiz

Faza 0 da O'LCHANMAGAN va Vazifa 9 (jonli tekshiruv) da sinaladigan selektorlar:
`search_input`, `switch`, `select_trigger`, `error_text`.
"""
from pages.ui.driver import UiDriver

# 29.09 relizida tugma nomlari o'zgargan. Muqobil nom sinaladi, u ham topilmasa
# `find_button` xato tashlaydi — jimgina o'tib ketmaydi.
A2_ALIASES = {
    "Просмотреть": "Просмотр",
    "Просмотр": "Просмотреть",
    "Создать": "Добавить",
    "Добавить": "Создать",
}

A2 = UiDriver(
    name="a2",
    main="main",
    main_last=True,
    rows=".smt-data-row",
    header="smt-cell-header",
    dialog="[role=dialog]",
    error_text=r"Ошибка|Не удалось|ORA-|violated|Exception",
    option_pane=".cdk-overlay-pane",
    switch='[role=switch], [role=checkbox], input[type=checkbox]',
    search_input='input[type=search], input[placeholder*="Поиск"]',
    select_trigger="smt-select-trigger, smt-data-select, smt-multi-data-select",
    field_ancestor=(
        'xpath=ancestor::*[.//input or .//textarea or .//smt-select-trigger '
        'or .//smt-data-select or .//*[@role="switch"]][1]'
    ),
    detect=(".smt-data-row", "smt-cell-header"),
    aliases=A2_ALIASES,
)
```

- [ ] **Qadam 5: `pages/ui/biruni.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Eski AngularJS («biruni») UI selektorlari.

Foydalanuvchi tasdiqlagan: a2 asosiy, lekin ba'zi formalar (masalan order formasi)
eski UI da qolgan. Bunday formalar kam, shuning uchun bu fayl kichik qoladi.

Manbasi: `smartup_reg/utils/base_page.py` (grid_row, grid_controller, confirm_biruni,
b_input_by_label) — u yerda selektorlar 700+ qatorlik god-obyekt ichida tarqalgan edi.
"""
from pages.ui.driver import UiDriver

BIRUNI = UiDriver(
    name="biruni",
    main="b-page",
    main_last=False,
    rows="b-grid .tbl-row",
    header=".tbl-header-cell",
    dialog="#biruniConfirm, .modal.show",
    error_text=r"Ошибка|ORA-|violated|Exception",
    option_pane="b-input div.hint",
    switch="input[type='checkbox'], [role='switch']",
    search_input='input[ng-model="o.searchValue"]',
    select_trigger="b-input",
    field_ancestor="xpath=following::b-input[.//input][1]",
    detect=("b-grid", "b-page"),
    aliases={},
)
```

- [ ] **Qadam 6: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_ui_driver.py -v && .venv/bin/pytest -q
```

Kutilgan: `tests/test_ui_driver.py` — `5 passed`; butun to'plam `103 passed`.

- [ ] **Qadam 7: Commit**

```bash
git add pages tests/test_ui_driver.py
git commit -m "$(cat <<'EOF'
feat(faza1): UiDriver selektor qatlami — A2 (Faza 0 o'lchovi) va BIRUNI

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Vazifa 4: `detect` — UI ni avtomatik aniqlash, jimgina fallback YO'Q

**Fayllar:**
- Create: `3_Avtotest/Avtotest_POM/pages/ui/detect.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_ui_detect.py`

**Interfeyslar:**
- Consumes: Vazifa 3 dan `A2`, `BIRUNI`, `UiDriver`
- Produces:
  - `UiNotDetected(RuntimeError)`
  - `detect(page, drivers=(A2, BIRUNI)) -> UiDriver`

**Nega xato tashlaydi.** `switchFilial` nuqsoni aynan shundan kelib chiqqan: kod
topolmaganda jimgina davom etdi. Agar `detect` sukut bo'yicha `A2` ga o'tib ketsa, eski UI
formasida barcha selektorlar mos kelmaydi va test «selektor topilmadi» deb yiqiladi —
sabab esa yashirin qoladi. Shuning uchun aniqlanmasa **darhol tushunarli xato**.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_ui_detect.py`:

```python
import pytest

from pages.ui.a2 import A2
from pages.ui.biruni import BIRUNI
from pages.ui.detect import UiNotDetected, detect
from tests.fake_page import FakePage


def test_a2_aniqlanadi():
    page = FakePage(counts={".smt-data-row": 7})

    assert detect(page) is A2


def test_biruni_aniqlanadi():
    page = FakePage(counts={"b-grid": 1})

    assert detect(page) is BIRUNI


def test_smt_cell_header_ham_a2_ni_beradi():
    """Grid bo'sh bo'lsa `.smt-data-row` topilmaydi, lekin ustun sarlavhasi qoladi."""
    page = FakePage(counts={"smt-cell-header": 5})

    assert detect(page) is A2


def test_hech_biri_topilmasa_xato_tashlanadi():
    """Jimgina A2 ga o'tib ketish TAQIQLANADI — sabab yashirin qolmasin."""
    page = FakePage(counts={}, url="https://app3.greenwhite.uz/xtrade/a2/anor/mr/filial_list")

    with pytest.raises(UiNotDetected) as xato:
        detect(page)

    assert "filial_list" in str(xato.value)
    assert "a2" in str(xato.value) and "biruni" in str(xato.value)


def test_tartib_muhim_a2_birinchi_sinaladi():
    """Ikkala UI belgisi ham bo'lsa (o'tish davri sahifasi) a2 ustun turadi."""
    page = FakePage(counts={".smt-data-row": 3, "b-grid": 1})

    assert detect(page) is A2
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_ui_detect.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'pages.ui.detect'` — FAIL.

- [ ] **Qadam 3: `pages/ui/detect.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Sahifa qaysi UI da ekanini aniqlaydi.

Faza 0 darsi: aniqlanmaganda jimgina birortasiga o'tib ketish TAQIQLANADI.
`switchFilial` nuqsoni aynan shundan kelib chiqqan — kod topolmadi, lekin hech
narsa demadi va butun yugurish noto'g'ri holatda ketdi.
"""
from pages.ui.a2 import A2
from pages.ui.biruni import BIRUNI


class UiNotDetected(RuntimeError):
    """Sahifada na a2, na eski UI belgisi topilmadi."""


def detect(page, drivers=(A2, BIRUNI)):
    """Sahifadagi belgilarga qarab `UiDriver` qaytaradi.

    Tartib muhim: `drivers` ketma-ketligida birinchi mos kelgani g'olib. a2 birinchi
    turadi, chunki o'tish davrida sahifada ikkala UI belgisi ham bo'lishi mumkin.
    Hech biri topilmasa `UiNotDetected` tashlaydi.
    """
    for drayver in drivers:
        for selektor in drayver.detect:
            if page.locator(selektor).count() > 0:
                return drayver
    nomlar = ", ".join(d.name for d in drivers)
    sinalgan = ", ".join(s for d in drivers for s in d.detect)
    raise UiNotDetected(
        "Sahifa UI si aniqlanmadi (%s). URL: %s · sinalgan selektorlar: %s"
        % (nomlar, getattr(page, "url", "?"), sinalgan)
    )
```

- [ ] **Qadam 4: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_ui_detect.py -v && .venv/bin/pytest -q
```

Kutilgan: `5 passed`; butun to'plam `108 passed`.

- [ ] **Qadam 5: Commit**

```bash
git add pages/ui/detect.py tests/test_ui_detect.py
git commit -m "$(cat <<'EOF'
feat(faza1): detect — UI ni aniqlash, aniqlanmasa xato tashlaydi

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Vazifa 5: `find_button` + `Grid` komponenti

**Fayllar:**
- Create: `3_Avtotest/Avtotest_POM/pages/components/__init__.py` (Vazifa 3 da yaratilgan)
- Create: `3_Avtotest/Avtotest_POM/pages/components/buttons.py`
- Create: `3_Avtotest/Avtotest_POM/pages/components/grid.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_components_grid.py`

**Interfeyslar:**
- Consumes: Vazifa 3 dan `UiDriver`, `A2`; Vazifa 2 dan `FakePage`
- Produces:
  - `ButtonNotFound(RuntimeError)`
  - `find_button(page, driver, text, scope=None) -> locator` — overlay birinchi, keyin
    sahifa; topilmasa `ALIAS` muqobili; u ham topilmasa `ButtonNotFound`
  - `Grid(page, driver)` metodlari: `rows()`, `row(text)`, `first_row()`,
    `click_row(text)`, `row_action(text)`, `columns() -> list[str]`,
    `expect_columns(*names)`, `search(text)`, `count() -> int`

**Tugma qidirish tartibi (sabab bilan).** a2 da drawer/dialog ochilganda sahifada va
drawer'da **bir xil nomli tugma** bo'ladi (masalan «Закрыть»). Shuning uchun avval
overlay ichi, keyin sahifa. Bu `smt.js` dagi `btnTop()` mantig'i.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_components_grid.py`:

```python
import pytest

from pages.components.buttons import ButtonNotFound, find_button
from pages.components.grid import Grid
from pages.ui.a2 import A2
from tests.fake_page import FakePage


def _page(**kw):
    return FakePage(**kw)


# ---------------------------------------------------------------- find_button
def test_find_button_overlay_ichini_birinchi_qaraydi():
    """Drawer ochiq bo'lsa sahifada va drawer'da bir xil «Закрыть» bo'ladi."""
    page = _page(counts={".cdk-overlay-pane >> filter(has_text='Закрыть') >> first": 1})

    loc = find_button(page, A2, "Закрыть")

    assert loc.key.startswith(".cdk-overlay-pane")


def test_find_button_overlayda_yoq_bolsa_sahifadan_qidiradi():
    page = _page(counts={"button:visible >> filter(has_text='Сохранить') >> first": 1})

    loc = find_button(page, A2, "Сохранить")

    assert loc.key.startswith("button:visible")


def test_find_button_alias_muqobilini_sinaydi():
    """29.09 relizida «Просмотреть» → «Просмотр» bo'lgan."""
    page = _page(counts={"button:visible >> filter(has_text='Просмотр') >> first": 1})

    loc = find_button(page, A2, "Просмотреть")

    assert "Просмотр'" in loc.key


def test_find_button_topilmasa_xato_tashlaydi():
    """Jimgina bo'sh locator qaytarish TAQIQLANADI."""
    page = _page(counts={})

    with pytest.raises(ButtonNotFound) as xato:
        find_button(page, A2, "Создать")

    assert "Создать" in str(xato.value)
    assert "Добавить" in str(xato.value)      # sinalgan muqobil ham ko'rinadi


# ---------------------------------------------------------------- Grid
def test_grid_ustunlarni_qaytaradi():
    page = _page(lists={"main >> last >> smt-cell-header": [" № ", "Название", ""]})

    assert Grid(page, A2).columns() == ["№", "Название"]


def test_grid_expect_columns_yetishmasa_xato():
    page = _page(lists={"main >> last >> smt-cell-header": ["№", "Название"]})

    with pytest.raises(AssertionError) as xato:
        Grid(page, A2).expect_columns("№", "Поставщик")

    assert "Поставщик" in str(xato.value)


def test_grid_click_row_matn_boyicha_qatorni_bosadi():
    page = _page(counts={"main >> last >> .smt-data-row >> filter(has_text='QA-1') >> first": 1})

    Grid(page, A2).click_row("QA-1")

    assert any("QA-1" in k for k in page.clicked())


def test_grid_click_row_birinchi_qator():
    page = _page(counts={"main >> last >> .smt-data-row >> first": 1})

    Grid(page, A2).click_row("birinchi qator")

    assert "main >> last >> .smt-data-row >> first" in page.clicked()


def test_grid_count_hisoblagichdan_olinadi():
    page = _page(texts={"main >> last": "Организации\n7/7\nСоздать"})

    assert Grid(page, A2).count() == 7


def test_grid_count_hisoblagich_yoq_bolsa_none():
    page = _page(texts={"main >> last": "Отчет"})

    assert Grid(page, A2).count() is None
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_components_grid.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'pages.components.buttons'` — FAIL.

- [ ] **Qadam 3: `pages/components/buttons.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Tugma qidirish — overlay ustun, keyin ALIAS muqobili, topilmasa XATO."""
import re

BUTTON_SELECTOR = "button:visible, a:visible, [role=menuitem]:visible, [role=option]:visible"


class ButtonNotFound(RuntimeError):
    """Tugma na asl nomi, na muqobil nomi bilan topilmadi."""


def _aniq(text):
    """Faqat shu matnli elementni tanlaydigan regex (qisman moslikdan saqlaydi)."""
    return re.compile(r"^\s*%s\s*$" % re.escape(text), re.IGNORECASE)


def find_button(page, driver, text, scope=None):
    """Tugma locatorini qaytaradi.

    Tartib: (1) overlay/drawer ichi — a2 da sahifada va drawer'da bir xil nomli tugma
    bo'ladi; (2) sahifa (yoki berilgan `scope`); (3) `driver.aliases` muqobili bilan
    yana shu ikki joy. Topilmasa `ButtonNotFound` — jimgina bo'sh locator QAYTARILMAYDI.
    """
    nomlar = [text]
    muqobil = driver.alias_of(text)
    if muqobil:
        nomlar.append(muqobil)

    for nom in nomlar:
        overlay = page.locator(driver.option_pane).filter(has_text=nom).first
        if overlay.count() > 0:
            return overlay
        asos = (scope or page).locator(BUTTON_SELECTOR).filter(has_text=nom).first
        if asos.count() > 0:
            return asos

    raise ButtonNotFound(
        "Tugma topilmadi: %s (sinalgan nomlar: %s · selektor: %s)"
        % (text, ", ".join(nomlar), BUTTON_SELECTOR)
    )
```

**Diqqat:** `filter(has_text=nom)` da `nom` — oddiy matn (regex emas), chunki `FakePage`
kaliti barqaror bo'lishi kerak va testlar aynan shunga tayanadi. Playwright `has_text` ni
qisman moslik deb qabul qiladi; aniq moslik kerak bo'lgan joyda `_aniq()` ishlatiladi
(Vazifa 7 dagi `Dialog.confirm`).

- [ ] **Qadam 4: `pages/components/grid.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Ro'yxat (grid) komponenti: qator, amal tugmasi, ustunlar, qidiruv."""
import re

from pages.components.buttons import find_button

BIRINCHI_QATOR = re.compile(r"^\s*birinchi qator", re.IGNORECASE)
HISOBLAGICH = re.compile(r"\b(\d+)\s*/\s*\d+\b")


class Grid:
    """Sahifadagi ro'yxat. DOM ga faqat `driver` selektorlari orqali murojaat qiladi."""

    def __init__(self, page, driver):
        self.page = page
        self.driver = driver

    # ---------------------------------------------------------------- asos
    @property
    def main(self):
        loc = self.page.locator(self.driver.main)
        return loc.last if self.driver.main_last else loc.first

    def rows(self):
        return self.main.locator(self.driver.rows)

    def first_row(self):
        return self.rows().first

    def row(self, text):
        """Matni `text` bo'lgan qator. «birinchi qator» — birinchisini beradi."""
        if BIRINCHI_QATOR.match(str(text)):
            return self.first_row()
        tozalangan = str(text).replace("«", "").replace("»", "").strip()
        return self.rows().filter(has_text=tozalangan).first

    # ---------------------------------------------------------------- amallar
    def click_row(self, text):
        """Qatorni bosadi — shundan keyin amal tugmalari ko'rinadi."""
        qator = self.row(text)
        qator.click()
        return qator

    def row_action(self, text):
        """Bosilgan qator ostidagi amal tugmasi (Просмотр, Изменить, Удалить...)."""
        find_button(self.page, self.driver, text).click()

    def search(self, text):
        maydon = self.main.locator(self.driver.search_input).first
        maydon.fill(str(text))
        maydon.press("Enter")

    # ---------------------------------------------------------------- so'rovlar
    def columns(self):
        xom = self.main.locator(self.driver.header).all_inner_texts()
        return [x.strip() for x in xom if x.strip()]

    def expect_columns(self, *names):
        bor = self.columns()
        yoq = [n for n in names if n not in bor]
        assert not yoq, "Ustunlar yo'q: %s · mavjud: %s" % (", ".join(yoq), ", ".join(bor))

    def count(self):
        """Ro'yxatdagi yozuvlar soni «N/M» hisoblagichidan. Hisoblagich yo'q → None.

        None «bo'sh» degani EMAS — hisobot sahifalarida hisoblagich bo'lmaydi.
        """
        matn = self.main.inner_text()
        m = HISOBLAGICH.search(matn or "")
        return int(m.group(1)) if m else None
```

- [ ] **Qadam 5: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_components_grid.py -v && .venv/bin/pytest -q
```

Kutilgan: `10 passed`; butun to'plam `118 passed`.

- [ ] **Qadam 6: Commit**

```bash
git add pages/components tests/test_components_grid.py
git commit -m "$(cat <<'EOF'
feat(faza1): find_button (ALIAS bilan) va Grid komponenti

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Vazifa 6: `Form` komponenti

**Fayllar:**
- Create: `3_Avtotest/Avtotest_POM/pages/components/form.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_components_form.py`

**Interfeyslar:**
- Consumes: Vazifa 3 dan `UiDriver`/`A2`; Vazifa 5 dan `find_button`
- Produces: `Form(page, driver)` metodlari:
  `field(label)`, `fill(label, value)`, `fill_date(label, value)`, `select(label, value)`,
  `multiselect(label, values)`, `toggle(label, on)`, `radio(label, value)`,
  `save(button="Сохранить")`, `expect_field(label, value)`, `labels() -> list[str]`

**Maydonni topish mantig'i.** SmartUp formalarida maydonning `id`/`name` atributlari
barqaror emas, lekin **yorliq (`label`) matni barqaror** — qo'lda yozilgan 858 case ham
yorliq nomlari bilan yozilgan. Shuning uchun: yorliqni matn bo'yicha topib, undan
`driver.field_ancestor` xpath bilan input/select/switch saqlovchi eng yaqin ajdodga chiqiladi.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_components_form.py`:

```python
import pytest

from pages.components.form import Form
from pages.ui.a2 import A2
from tests.fake_page import FakePage

def _konteyner(yorliq):
    """`Form.field(yorliq)` yasaydigan `FakePage` kaliti.

    Yorliq har testda boshqa bo'lishi mumkin, shuning uchun kalit QATTIQ YOZILMAYDI —
    aks holda test boshqa yorliqli chaqiruvni tekshirib, jimgina yiqiladi (30.09 da
    aynan shunday bo'lgan: sana testi «Дата» ni chaqirib «Наименование» ni tekshirgan).
    """
    return "label >> filter(has_text=%r) >> first >> %s" % (yorliq, A2.field_ancestor)


KONTEYNER = _konteyner("Наименование")


def test_field_yorliqdan_konteynerga_chiqadi():
    page = FakePage()

    loc = Form(page, A2).field("Наименование")

    assert loc.key == KONTEYNER


def test_field_yulduzcha_va_qavsni_tashlaydi():
    """Case'larda yorliq «Наименование *» yoki «Код (авто)» ko'rinishida yozilgan."""
    page = FakePage()

    a = Form(page, A2).field("Наименование *")
    b = Form(page, A2).field("Наименование (авто)")

    assert a.key == KONTEYNER
    assert b.key == KONTEYNER


def test_fill_input_ga_yozadi():
    page = FakePage()

    Form(page, A2).fill("Наименование", "QA-tovar-1")

    assert (KONTEYNER + " >> input, textarea >> first", "QA-tovar-1") in page.filled()


def test_fill_date_ketma_ket_yozadi():
    """Sana maydoni maskali — fill() ishlamaydi, bosib-tozalab yozish kerak."""
    page = FakePage()

    Form(page, A2).fill_date("Дата", "01.10.2026")

    kalit = _konteyner("Дата") + " >> input >> first"
    assert ("click", kalit) in page.calls
    assert ("fill", kalit, "01.10.2026") in page.calls
    assert ("press", kalit, "Tab") in page.calls


def test_select_variant_panelidan_tanlaydi():
    page = FakePage(counts={".cdk-overlay-pane >> filter(has_text='Наличные') >> first": 1})

    Form(page, A2).select("Тип оплаты", "Наличные")

    bosilgan = page.clicked()
    assert any(A2.select_trigger in k for k in bosilgan)
    assert any(".cdk-overlay-pane" in k and "Наличные" in k for k in bosilgan)


def test_toggle_holat_mos_bolsa_bosmaydi():
    page = FakePage(attrs={(KONTEYNER + " >> " + A2.switch + " >> first", "aria-checked"): "true"})

    Form(page, A2).toggle("Наименование", on=True)

    assert page.clicked() == []


def test_toggle_holat_mos_kelmasa_bosadi():
    page = FakePage(attrs={(KONTEYNER + " >> " + A2.switch + " >> first", "aria-checked"): "false"})

    Form(page, A2).toggle("Наименование", on=True)

    assert page.clicked() == [KONTEYNER + " >> " + A2.switch + " >> first"]


def test_save_tugmani_bosadi():
    page = FakePage(counts={"button:visible, a:visible, [role=menuitem]:visible, "
                            "[role=option]:visible >> filter(has_text='Сохранить') >> first": 1})

    Form(page, A2).save()

    assert any("Сохранить" in k for k in page.clicked())


def test_labels_royxatini_qaytaradi():
    page = FakePage(lists={"main >> last >> label": [" Код ", "Наименование *", ""]})

    assert Form(page, A2).labels() == ["Код", "Наименование *"]
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_components_form.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'pages.components.form'` — FAIL.

- [ ] **Qadam 3: `pages/components/form.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Forma komponenti: maydonlarni yorliq matni bo'yicha topib to'ldiradi.

SmartUp da maydon `id`/`name` atributlari barqaror emas, yorliq matni esa barqaror —
858 ta qo'lda yozilgan case ham yorliq nomlari bilan yozilgan.
"""
import re

from pages.components.buttons import find_button

TOZALA = re.compile(r"\s*\*\s*$|\s*\([^)]*\)\s*$")


class Form:
    def __init__(self, page, driver):
        self.page = page
        self.driver = driver

    @property
    def main(self):
        loc = self.page.locator(self.driver.main)
        return loc.last if self.driver.main_last else loc.first

    # ---------------------------------------------------------------- maydon
    def field(self, label):
        """Yorliqqa tegishli maydon konteyneri (input/select/switch saqlovchi ajdod)."""
        toza = TOZALA.sub("", str(label)).strip()
        return (self.page.locator("label").filter(has_text=toza).first
                .locator(self.driver.field_ancestor))

    def labels(self):
        xom = self.main.locator("label").all_inner_texts()
        return [x.strip() for x in xom if x.strip()]

    # ---------------------------------------------------------------- yozish
    def fill(self, label, value):
        self.field(label).locator("input, textarea").first.fill(str(value))

    def fill_date(self, label, value):
        """Sana maydoni maskali: bosib, tozalab, yozib, Tab bilan tasdiqlanadi."""
        maydon = self.field(label).locator("input").first
        maydon.click()
        maydon.fill(str(value))
        maydon.press("Tab")

    def select(self, label, value):
        """Ochiluvchi ro'yxatdan tanlaydi: triggerni bosib, variant panelidan bosadi."""
        self.field(label).locator(self.driver.select_trigger).first.click()
        self.page.locator(self.driver.option_pane).filter(has_text=str(value)).first.click()

    def multiselect(self, label, values):
        for qiymat in values:
            self.select(label, qiymat)

    def toggle(self, label, on):
        """Switch/checkbox ni kerakli holatga keltiradi. Holat mos bo'lsa bosmaydi."""
        element = self.field(label).locator(self.driver.switch).first
        hozir = element.get_attribute("aria-checked") == "true"
        if bool(on) != hozir:
            element.click()

    def radio(self, label, value):
        self.field(label).locator("label, [role=radio]").filter(has_text=str(value)).first.click()

    # ---------------------------------------------------------------- saqlash
    def save(self, button="Сохранить"):
        find_button(self.page, self.driver, button).click()

    def expect_field(self, label, value):
        matn = self.field(label).inner_text()
        assert str(value) in (matn or ""), (
            "«%s» maydonida «%s» yo'q · hozir: %r" % (label, value, matn))
```

- [ ] **Qadam 4: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_components_form.py -v && .venv/bin/pytest -q
```

Kutilgan: `9 passed`; butun to'plam `127 passed`.

- [ ] **Qadam 5: Commit**

```bash
git add pages/components/form.py tests/test_components_form.py
git commit -m "$(cat <<'EOF'
feat(faza1): Form komponenti — maydonlar yorliq matni bo'yicha

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Vazifa 7: `Dialog`, `Menu`, `Report` komponentlari

**Fayllar:**
- Create: `3_Avtotest/Avtotest_POM/pages/components/dialog.py`
- Create: `3_Avtotest/Avtotest_POM/pages/components/menu.py`
- Create: `3_Avtotest/Avtotest_POM/pages/components/report.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_components_dialog_menu.py`

**Interfeyslar:**
- Consumes: Vazifa 3 (`UiDriver`), Vazifa 5 (`find_button`)
- Produces:
  - `Dialog(page, driver)`: `visible() -> bool`, `text() -> str`, `has_error() -> bool`,
    `error_text() -> str`, `confirm(contains, button="Да")`, `close(button="Закрыть")`
  - `FilialNotSwitched(RuntimeError)`
  - `Menu(page, driver)`: `nav(path)`, `menu_plus(name)`, `current_filial() -> str`,
    `switch_filial(name) -> str`
  - `Report(page, driver)`: `generate(button="Сформировать")`, `required_errors() -> int`

**«Да» tugmasi haqida.** Ma'lum bug (SPR-003/OBR-001/PRZ-003): ba'zi tasdiq oynalarida
tugma «Да» emas, «Вкл.» deb yozilgan. Shuning uchun `confirm` ikkala variantni ham
qabul qiladi — bu `smt.js` dagi `YES` regexi.

**Filial almashtirish — Faza 0 nuqsoni.** `switch_filial` natijani TEKSHIRADI va mos
kelmasa `FilialNotSwitched` tashlaydi. Eski JS kodi buni qilmagan va butun yugurish
noto'g'ri filialda ketgan.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_components_dialog_menu.py`:

```python
import pytest

from pages.components.dialog import Dialog
from pages.components.menu import FilialNotSwitched, Menu
from pages.components.report import Report
from pages.ui.a2 import A2
from tests.fake_page import FakePage


# ---------------------------------------------------------------- Dialog
def test_dialog_korinadi():
    page = FakePage(counts={"[role=dialog]": 1})

    assert Dialog(page, A2).visible() is True


def test_dialog_xato_matnini_aniqlaydi():
    page = FakePage(counts={"[role=dialog]": 1},
                    texts={"[role=dialog] >> first": "Ошибка ORA-00001: unique constraint"})

    d = Dialog(page, A2)

    assert d.has_error() is True
    assert "ORA-00001" in d.error_text()


def test_dialog_oddiy_tasdiq_xato_emas():
    page = FakePage(counts={"[role=dialog]": 1},
                    texts={"[role=dialog] >> first": "Сохранить?"})

    assert Dialog(page, A2).has_error() is False


def test_dialog_confirm_da_tugmasini_bosadi():
    page = FakePage(counts={"[role=dialog]": 1})

    Dialog(page, A2).confirm("Сохранить")

    assert any("[role=dialog]" in k and "button" in k for k in page.clicked())


def test_dialog_confirm_oyna_yoq_bolsa_xato():
    """Tasdiq oynasi chiqmasa jimgina o'tib ketilmaydi."""
    page = FakePage(counts={})

    with pytest.raises(AssertionError) as xato:
        Dialog(page, A2).confirm("Сохранить")

    assert "Сохранить" in str(xato.value)


# ---------------------------------------------------------------- Menu
def test_menu_nav_ikki_bosqichli_yolni_bosadi():
    page = FakePage(counts={"button:visible, a:visible, [role=menuitem]:visible, "
                            "[role=option]:visible >> filter(has_text='Склад') >> first": 1,
                            "button:visible, a:visible, [role=menuitem]:visible, "
                            "[role=option]:visible >> filter(has_text='Закупки') >> first": 1})

    Menu(page, A2).nav("Склад > Закупки")

    bosilgan = " | ".join(page.clicked())
    assert "Склад" in bosilgan and "Закупки" in bosilgan


def test_menu_current_filial_matndan_ajratadi():
    page = FakePage(texts={"app-project-filial-selector button >> first": "TRADE Toshkent"})

    assert Menu(page, A2).current_filial() == "Toshkent"


def test_switch_filial_allaqachon_kerakli_bolsa_bosmaydi():
    page = FakePage(texts={"app-project-filial-selector button >> first": "TRADE Toshkent"})

    assert Menu(page, A2).switch_filial("Toshkent") == "Toshkent"
    assert page.clicked() == []


def test_switch_filial_almashmasa_xato_tashlaydi():
    """Faza 0: eski kod natijani tekshirmagan va butun yugurish noto'g'ri
    filialda ketgan — endi xato tashlanadi."""
    page = FakePage(counts={".cdk-overlay-pane >> filter(has_text='Toshkent') >> first": 1},
                    texts={"app-project-filial-selector button >> first": "TRADE Администрирование"})

    with pytest.raises(FilialNotSwitched) as xato:
        Menu(page, A2).switch_filial("Toshkent")

    assert "Toshkent" in str(xato.value) and "Администрирование" in str(xato.value)


# ---------------------------------------------------------------- Report
def test_report_generate_tugmani_bosadi():
    page = FakePage(counts={"button:visible, a:visible, [role=menuitem]:visible, "
                            "[role=option]:visible >> filter(has_text='Сформировать') >> first": 1})

    Report(page, A2).generate()

    assert any("Сформировать" in k for k in page.clicked())


def test_report_required_errors_sanaydi():
    page = FakePage(counts={"main >> last >> [class*=outline-error]": 3})

    assert Report(page, A2).required_errors() == 3
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_components_dialog_menu.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'pages.components.dialog'` — FAIL.

- [ ] **Qadam 3: `pages/components/dialog.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Tasdiq va xato oynalari."""
import re

# Ma'lum bug (SPR-003/OBR-001/PRZ-003): ba'zi tasdiq oynalarida tugma «Да» emas, «Вкл.».
HA = re.compile(r"^\s*(Да|Вкл\.)\s*$", re.IGNORECASE)


class Dialog:
    def __init__(self, page, driver):
        self.page = page
        self.driver = driver

    def _dialog(self):
        return self.page.locator(self.driver.dialog).first

    def visible(self):
        return self.page.locator(self.driver.dialog).count() > 0

    def text(self):
        return self._dialog().inner_text() if self.visible() else ""

    def has_error(self):
        return bool(re.search(self.driver.error_text, self.text() or "", re.IGNORECASE))

    def error_text(self):
        matn = self.text()
        return re.sub(r"\s+", " ", matn).strip() if self.has_error() else ""

    def confirm(self, contains, button="Да"):
        """Matni `contains` ni o'z ichiga olgan oynada `button` ni bosadi.

        Oyna chiqmasa AssertionError — jimgina o'tib ketilmaydi.
        """
        assert self.visible(), "Tasdiq oynasi chiqmadi: «%s» kutilgan edi" % contains
        kutilgan = HA if re.match(r"^\s*да\s*$", button, re.IGNORECASE) else \
            re.compile(r"^\s*%s\s*$" % re.escape(button), re.IGNORECASE)
        self._dialog().locator("button").filter(has_text=kutilgan).first.click()

    def close(self, button="Закрыть"):
        if self.visible():
            self._dialog().locator("button").filter(has_text=button).first.click()
```

- [ ] **Qadam 4: `pages/components/menu.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Yuqori menyu, menyu yonidagi «+», filial almashtirish."""
import re

from pages.components.buttons import find_button

# 29.09 da aniqlangan: eski `.dropdown-locations-custom` a2 da YO'Q.
FILIAL_TUGMA = "app-project-filial-selector button"
FILIAL_MATN = re.compile(r"TRADE\s*\n?\s*(\S+)")


class FilialNotSwitched(RuntimeError):
    """Filial almashtirilmadi — natija tekshirilib, mos kelmasligi aniqlandi."""


class Menu:
    def __init__(self, page, driver):
        self.page = page
        self.driver = driver

    def nav(self, path):
        """«Склад > Закупки» ko'rinishidagi yo'l bo'yicha o'tadi."""
        for bolak in [x.strip() for x in str(path).split(">") if x.strip()]:
            find_button(self.page, self.driver, bolak).click()

    def menu_plus(self, name):
        """Menyu bandi yonidagi «+» tugmasi."""
        self.page.locator('button[aria-label="%s"]' % name).first.click()

    def current_filial(self):
        matn = self.page.locator(FILIAL_TUGMA).first.inner_text() or ""
        m = FILIAL_MATN.search(matn)
        return m.group(1) if m else ""

    def switch_filial(self, name):
        """Filialni almashtiradi va NATIJANI TEKSHIRADI.

        Faza 0: eski JS kodi tekshirmagan va chaqiruv `.catch()` da edi — butun
        yugurish «Администрирование» filialida ketib, ombor sahifalari 403 qaytargan.
        """
        if self.current_filial() == name:
            return name
        self.page.locator(FILIAL_TUGMA).first.click()
        self.page.locator(self.driver.option_pane).filter(has_text=name).first.click()
        hozir = self.current_filial()
        if hozir != name:
            raise FilialNotSwitched(
                "Filial almashmadi: kutilgan «%s», hozir «%s»" % (name, hozir))
        return hozir
```

- [ ] **Qadam 5: `pages/components/report.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Hisobot formalari: generatsiya va majburiy maydon xatolari."""
from pages.components.buttons import find_button


class Report:
    def __init__(self, page, driver):
        self.page = page
        self.driver = driver

    @property
    def main(self):
        loc = self.page.locator(self.driver.main)
        return loc.last if self.driver.main_last else loc.first

    def generate(self, button="Сформировать"):
        find_button(self.page, self.driver, button).click()

    def required_errors(self):
        """To'ldirilmagan majburiy maydonlar soni (qizil ramka)."""
        return self.main.locator("[class*=outline-error]").count()
```

- [ ] **Qadam 6: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_components_dialog_menu.py -v && .venv/bin/pytest -q
```

Kutilgan: `11 passed`; butun to'plam `138 passed`.

- [ ] **Qadam 7: Commit**

```bash
git add pages/components/dialog.py pages/components/menu.py pages/components/report.py \
        tests/test_components_dialog_menu.py
git commit -m "$(cat <<'EOF'
feat(faza1): Dialog, Menu (filial tekshiruvi bilan) va Report komponentlari

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Vazifa 8: `BasePage`, `PageFactory`, `GenericPage`

**Fayllar:**
- Create: `3_Avtotest/Avtotest_POM/pages/base_page.py`
- Create: `3_Avtotest/Avtotest_POM/pages/factory.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_base_page.py`

**Interfeyslar:**
- Consumes: Vazifa 3–7 (barcha komponentlar, `detect`)
- Produces:
  - `BasePage(page, driver=None)` — xossalar: `ui`, `main`, `grid`, `form`, `dialog`,
    `menu`, `report`; metodlar: `open(route)`, `heading()`, `expect_no_error()`
  - `GenericPage(BasePage)` — `route: str | None`
  - `PageFactory(page)` — `register(module, form, cls)`, `for_form(module, form) -> BasePage`

**`BasePage` 100 qatordan oshmaydi** — bu spec ning muvaffaqiyat mezoni (legacy
`base_page.py` 791 qator edi). Mantiq komponentlarda, `BasePage` faqat yig'uvchi.

**`PageFactory` nega kerak.** Faza 2 da 858 JSON case yuriladi, lekin 198 forma uchun
alohida Page klassi yozib chiqish shart emas: klass topilmasa `GenericPage` beriladi va
case komponentlar ustida ishlaydi. Aniq klasslar Faza 3–4 da qo'lda yozilgan testlar
uchun bosqichma-bosqich qo'shiladi.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_base_page.py`:

```python
import pytest

from pages.base_page import BasePage
from pages.factory import GenericPage, PageFactory
from pages.ui.a2 import A2
from pages.ui.detect import UiNotDetected
from tests.fake_page import FakePage


def test_drayver_berilsa_aniqlash_qilinmaydi():
    page = FakePage()

    p = BasePage(page, driver=A2)

    assert p.ui is A2
    assert page.calls == []          # detect chaqirilmadi


def test_drayver_berilmasa_aniqlanadi():
    page = FakePage(counts={".smt-data-row": 4})

    assert BasePage(page).ui is A2


def test_aniqlanmasa_xato_tashlanadi():
    page = FakePage(counts={})

    with pytest.raises(UiNotDetected):
        BasePage(page).ui


def test_komponentlar_yigiladi():
    p = BasePage(FakePage(), driver=A2)

    assert p.grid.driver is A2
    assert p.form.driver is A2
    assert p.dialog.driver is A2
    assert p.menu.driver is A2
    assert p.report.driver is A2


def test_heading_birinchi_qatorni_qaytaradi():
    page = FakePage(texts={"main >> last": "  Организации  \n7/7\nСоздать"})

    assert BasePage(page, driver=A2).heading() == "Организации"


def test_expect_no_error_xato_oynasi_bolsa_yiqiladi():
    page = FakePage(counts={"[role=dialog]": 1},
                    texts={"[role=dialog] >> first": "Ошибка ORA-00001"})

    with pytest.raises(AssertionError) as xato:
        BasePage(page, driver=A2).expect_no_error()

    assert "ORA-00001" in str(xato.value)


def test_open_route_ga_otadi():
    page = FakePage()

    BasePage(page, driver=A2).open("/xtrade/a2/anor/mr/filial_list")

    assert ("goto", "/xtrade/a2/anor/mr/filial_list") in page.calls


def test_factory_royxatdan_otgan_klassni_qaytaradi():
    class OrderPage(BasePage):
        route = "/xtrade/a2/trade/tvt/order_list"

    fabrika = PageFactory(FakePage(counts={".smt-data-row": 1}))
    fabrika.register("Продажа", "Заказы", OrderPage)

    p = fabrika.for_form("Продажа", "Заказы")

    assert isinstance(p, OrderPage)


def test_factory_topilmasa_generic_page_beradi():
    fabrika = PageFactory(FakePage(counts={".smt-data-row": 1}))

    p = fabrika.for_form("Склад", "Hech qachon ro'yxatdan o'tmagan forma")

    assert isinstance(p, GenericPage)
    assert p.route is None
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_base_page.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'pages.base_page'` — FAIL.

- [ ] **Qadam 3: `pages/base_page.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Barcha sahifalarning asosi. Faqat YIG'UVCHI — mantiq komponentlarda.

Spec muvaffaqiyat mezoni: bu fayl 100 qatordan oshmaydi (legacy `base_page.py` 791 qator
edi va shu sababli hech kim unga tegishga jur'at qilmagan).
"""
from pages.components.dialog import Dialog
from pages.components.form import Form
from pages.components.grid import Grid
from pages.components.menu import Menu
from pages.components.report import Report
from pages.ui.detect import detect


class BasePage:
    route = None

    def __init__(self, page, driver=None):
        self.page = page
        self._driver = driver

    # ---------------------------------------------------------------- UI qatlami
    @property
    def ui(self):
        """Sahifaning `UiDriver` i. Berilmagan bo'lsa bir marta aniqlanib keshlanadi."""
        if self._driver is None:
            self._driver = detect(self.page)
        return self._driver

    @property
    def main(self):
        loc = self.page.locator(self.ui.main)
        return loc.last if self.ui.main_last else loc.first

    # ---------------------------------------------------------------- komponentlar
    @property
    def grid(self):
        return Grid(self.page, self.ui)

    @property
    def form(self):
        return Form(self.page, self.ui)

    @property
    def dialog(self):
        return Dialog(self.page, self.ui)

    @property
    def menu(self):
        return Menu(self.page, self.ui)

    @property
    def report(self):
        return Report(self.page, self.ui)

    # ---------------------------------------------------------------- amallar
    def open(self, route=None):
        """Sahifani ochadi. `route` berilmasa klassning `route` i ishlatiladi."""
        manzil = route or self.route
        assert manzil, "%s uchun route berilmagan" % type(self).__name__
        self.page.goto(manzil)
        return self

    def heading(self):
        """Sahifa sarlavhasi — asosiy konteynerning birinchi bo'sh bo'lmagan qatori."""
        matn = self.main.inner_text() or ""
        for qator in matn.split("\n"):
            if qator.strip():
                return qator.strip()
        return ""

    def expect_no_error(self):
        """Xato oynasi bo'lmasligini tekshiradi. Bo'lsa — matni bilan yiqiladi."""
        d = self.dialog
        assert not d.has_error(), "Xato oynasi: %s" % d.error_text()
        return self
```

- [ ] **Qadam 4: `pages/factory.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Forma nomi bo'yicha Page klassini beradi.

Faza 2 da 858 JSON case yuriladi, lekin 198 forma uchun alohida klass yozish shart emas:
ro'yxatdan o'tmagan forma `GenericPage` oladi va case komponentlar ustida ishlaydi.
Aniq klasslar Faza 3–4 da qo'lda yozilgan testlar uchun qo'shiladi.
"""
from pages.base_page import BasePage


class GenericPage(BasePage):
    """Aniq klassi yozilmagan forma uchun — faqat komponentlar."""
    route = None


class PageFactory:
    def __init__(self, page):
        self.page = page
        self._registry = {}

    def register(self, module, form, cls):
        self._registry[(module, form)] = cls
        return self

    def for_form(self, module, form):
        cls = self._registry.get((module, form), GenericPage)
        return cls(self.page)
```

- [ ] **Qadam 5: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_base_page.py -v && .venv/bin/pytest -q
echo "--- BasePage hajmi (100 dan oshmasligi kerak) ---"
wc -l pages/base_page.py
```

Kutilgan: `9 passed`; butun to'plam `147 passed`; `pages/base_page.py` ≤ 100 qator.
Oshgan bo'lsa TO'XTA va ayt — bu spec mezonini buzadi.

- [ ] **Qadam 6: Commit**

```bash
git add pages/base_page.py pages/factory.py tests/test_base_page.py
git commit -m "$(cat <<'EOF'
feat(faza1): BasePage (yig'uvchi), PageFactory va GenericPage

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Vazifa 9: `SoftAssert` porti, `page`/`ui` fixture'lari va jonli tekshiruv

**Fayllar:**
- Create: `3_Avtotest/Avtotest_POM/utils/__init__.py`
- Create: `3_Avtotest/Avtotest_POM/utils/soft_assert.py`
- Modify: `3_Avtotest/Avtotest_POM/conftest.py`
- Create: `3_Avtotest/Avtotest_POM/tests/test_soft_assert.py`
- Create: `3_Avtotest/Avtotest_POM/tests/live/__init__.py`
- Create: `3_Avtotest/Avtotest_POM/tests/live/test_live_smoke.py`

**Interfeyslar:**
- Consumes: Vazifa 1 dan `load_env`; Vazifa 3–8 dan `A2`, `BIRUNI`, `BasePage`
- Produces:
  - `SoftAssert()` — `check(condition, message)`, `failures: list[str]`, `assert_all()`
  - `conftest` fixture'lari: `browser_page` (jonli, `--live`), `soft`
  - 2 ta jonli test: a2 ro'yxati va eski UI formasi

**`SoftAssert` porti.** Manba `Smartupauto/utils/soft_assert.py` (113 qator) — eng to'lig'i.
Undan **Telegram bog'liqligi olib tashlanadi** (`from utils.telegram_reporter import
_session_soft_failures` — modullar orasida yashirin global holat) va `except Exception: pass`
bloklari **olib tashlanadi** (Faza 0 qoidasi). Allure biriktirish qoladi, lekin xatosi
yutilmaydi — `logger` ga yoziladi.

**Jonli tekshiruv — Faza 1 ning chiqish mezoni.** Spec: *«bitta qo'lda yozilgan smoke testi
a2 da yashil o'tadi; bitta eski-UI testi `BiruniDriver` bilan yashil o'tadi»*.

- [ ] **Qadam 1: `SoftAssert` uchun yiqiladigan testni yozish**

`tests/test_soft_assert.py`:

```python
import pytest

from utils.soft_assert import SoftAssert


def test_check_xatoni_yigadi_lekin_toxtatmaydi():
    soft = SoftAssert()

    soft.check(False, "birinchi xato")
    soft.check(True, "bu yozilmaydi")
    soft.check(False, "ikkinchi xato")

    assert soft.failures == ["birinchi xato", "ikkinchi xato"]


def test_assert_all_hammasini_bitta_xatoda_chiqaradi():
    soft = SoftAssert()
    soft.check(False, "A yo'q")
    soft.check(False, "B yo'q")

    with pytest.raises(AssertionError) as xato:
        soft.assert_all()

    matn = str(xato.value)
    assert "A yo'q" in matn and "B yo'q" in matn
    assert "2" in matn                 # nechta xato borligi ko'rinadi


def test_assert_all_xato_yoq_bolsa_jim():
    SoftAssert().assert_all()


def test_assert_all_ikki_marta_chaqirilsa_takrorlamaydi():
    """Fixture teardown ham chaqiradi — ikki marta yiqilmasligi kerak."""
    soft = SoftAssert()
    soft.check(False, "A yo'q")

    with pytest.raises(AssertionError):
        soft.assert_all()
    soft.assert_all()
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_soft_assert.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'utils.soft_assert'` — FAIL.

- [ ] **Qadam 3: `utils/soft_assert.py` yozish**

```bash
mkdir -p utils tests/live
touch utils/__init__.py tests/live/__init__.py
```

```python
# -*- coding: utf-8 -*-
"""Soft assertion — bitta testda bir nechta tekshiruvni yig'ib, oxirida birga chiqaradi.

Manba: `Smartupauto/utils/soft_assert.py`. Ikki narsa OLIB TASHLANDI:
  1. `utils.telegram_reporter` dan yashirin global ro'yxatga yozish — modullar orasidagi
     ko'rinmas bog'liqlik edi;
  2. `except Exception: pass` bloklari — Faza 0 uchta nuqsonni aynan shu naqshda topdi.
Allure biriktirish ixtiyoriy: paket bo'lmasa `attach` shunchaki bajarilmaydi, lekin
bu holat `notes` ga yoziladi va yashirin qolmaydi.
"""


class SoftAssert:
    def __init__(self, page=None):
        self.failures = []
        self.notes = []
        self._page = page
        self._raised = False

    def check(self, condition, message):
        """Shart bajarilmasa xatoni yig'adi va davom etadi."""
        if condition:
            return
        self.failures.append(message)
        self._attach(message)

    def _attach(self, message):
        try:
            import allure
        except ImportError:
            self.notes.append("allure paketi yo'q — biriktirish qilinmadi")
            return
        allure.attach(message, name="soft-fail",
                      attachment_type=allure.attachment_type.TEXT)
        if self._page is not None:
            allure.attach(self._page.screenshot(full_page=True),
                          name="soft-fail: %s" % message[:50],
                          attachment_type=allure.attachment_type.PNG)

    def assert_all(self):
        """Yig'ilgan xatolarni bitta AssertionError qilib chiqaradi.

        Bir marta chiqargandan keyin takrorlamaydi — fixture teardown ham chaqiradi.
        """
        if not self.failures or self._raised:
            return
        self._raised = True
        raise AssertionError(
            "%d ta soft tekshiruv yiqildi:\n- %s" % (len(self.failures),
                                                     "\n- ".join(self.failures)))
```

- [ ] **Qadam 4: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_soft_assert.py -v
```

Kutilgan: `4 passed`.

- [ ] **Qadam 5: `conftest.py` ga fixture'larni qo'shish**

`conftest.py` oxiriga:

```python
@pytest.fixture
def soft():
    """Soft assertion. Test oxirida yig'ilgan xatolar birga chiqariladi."""
    from utils.soft_assert import SoftAssert

    s = SoftAssert()
    yield s
    s.assert_all()


@pytest.fixture(scope="session")
def _playwright():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        yield p


@pytest.fixture
def browser_page(_playwright, request):
    """Jonli brauzer sahifasi. Faqat `live` markerli testlar uchun.

    Sessiya `SmartUp_Autotest/.auth/admin.json` dan olinadi — u Faza 0 da yaratilgan
    va filial «Toshkent» bilan saqlangan. Parol bu yerda ISHLATILMAYDI.
    """
    auth = (Path(__file__).resolve().parents[1]
            / "SmartUp_Autotest" / ".auth" / "admin.json")
    if not auth.exists():
        pytest.skip("sessiya fayli yo'q: %s (avval `npm run setup` yuritilsin)" % auth)
    # Sukut bo'yicha headless. Brauzerni ko'rish uchun: HEADED=1 pytest ... --live
    brauzer = _playwright.chromium.launch(headless=not os.environ.get("HEADED"))
    ctx = brauzer.new_context(storage_state=str(auth), locale="ru-RU",
                             viewport={"width": 1600, "height": 1000})
    page = ctx.new_page()
    page.set_default_navigation_timeout(90_000)
    page.set_default_timeout(30_000)
    yield page
    ctx.close()
    brauzer.close()
```

`conftest.py` boshiga `from pathlib import Path` allaqachon bor — takrorlanmasin.

- [ ] **Qadam 6: Jonli testlarni yozish**

`tests/live/test_live_smoke.py`:

```python
# -*- coding: utf-8 -*-
"""Faza 1 ning chiqish mezoni: poydevor real ilovada ishlaydi.

Yuritish:  .venv/bin/pytest tests/live -v --live
"""
import pytest

from pages.base_page import BasePage
from pages.ui.a2 import A2

BASE = "https://app3.greenwhite.uz"

pytestmark = pytest.mark.live


def test_a2_organizatsiyalar_royxati_ochiladi(browser_page):
    """a2 UI: sahifa ochiladi, UI avtomatik aniqlanadi, ustunlar mavjud."""
    p = BasePage(browser_page).open(BASE + "/xtrade/a2/anor/mr/filial_list")
    browser_page.wait_for_load_state("networkidle")

    assert p.ui is A2, "a2 aniqlanmadi, aniqlangan: %s" % p.ui.name
    p.expect_no_error()
    assert p.heading(), "sarlavha bo'sh"
    assert p.grid.columns(), "ustun sarlavhalari topilmadi"


def test_filial_toshkent_ekanini_tekshiradi(browser_page):
    """Faza 0 nuqsoni qaytmasligi uchun: sessiya «Toshkent» filialida bo'lishi shart."""
    p = BasePage(browser_page).open(BASE + "/xtrade/a2/anor/mr/filial_list")
    browser_page.wait_for_load_state("networkidle")

    assert p.menu.current_filial() == "Toshkent", (
        "filial «Toshkent» emas: %r — ombor sahifalari 403 qaytaradi"
        % p.menu.current_filial())


def test_eski_ui_formasi_biruni_drayveri_bilan_ochiladi(browser_page):
    """Eski AngularJS da qolgan forma: `detect` BIRUNI ni tanlashi kerak.

    Route foydalanuvchi bilan tasdiqlanadi (order formasi eski UI da qolgan deb aytilgan).
    Sahifa a2 da chiqsa test SKIP bo'ladi — bu nuqson emas, forma ko'chirilgan degani.
    """
    from pages.ui.biruni import BIRUNI

    p = BasePage(browser_page).open(BASE + "/xtrade/#/!trade/tvt/order_list")
    browser_page.wait_for_load_state("networkidle")

    if p.ui is not BIRUNI:
        pytest.skip("forma endi a2 da — eski UI adapteri bu yerda kerak emas")
    p.expect_no_error()
    assert p.grid.columns(), "eski UI da ustun sarlavhalari topilmadi"
```

- [ ] **Qadam 7: Brauzersiz to'plamni yuritish**

```bash
.venv/bin/pytest -q
```

Kutilgan: `151 passed, 3 skipped` — jonli 3 test `--live` bo'lmagani uchun skip.

- [ ] **Qadam 8: Jonli tekshiruvni yuritish**

```bash
cd /Users/superuser/Desktop/Cowork/SmartUp_QA/3_Avtotest/Avtotest_POM
set -a; . ../.env; set +a
.venv/bin/pytest tests/live -v --live
```

Kutilgan: `test_a2_organizatsiyalar_royxati_ochiladi` va
`test_filial_toshkent_ekanini_tekshiradi` — PASS.
`test_eski_ui_formasi_biruni_drayveri_bilan_ochiladi` — PASS yoki SKIP.

**Agar a2 testi yiqilsa:** xato matnini hisobotga yoz va TO'XTA. Sabab `pages/ui/a2.py`
dagi biror selektor bo'lishi mumkin — Faza 0 da `search_input`, `switch`, `select_trigger`
va `error_text` O'LCHANMAGAN edi, aynan shu vazifa ularni birinchi marta sinaydi.

- [ ] **Qadam 9: Commit**

```bash
git add utils conftest.py tests/test_soft_assert.py tests/live
git commit -m "$(cat <<'EOF'
feat(faza1): SoftAssert porti, browser_page fixture va jonli tekshiruv

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Vazifa 10: `logger`, `code` va `save_data`/`load_data` fixture'lari

**Fayllar:**
- Create: `3_Avtotest/Avtotest_POM/utils/logger.py`
- Modify: `3_Avtotest/Avtotest_POM/conftest.py`
- Test: `3_Avtotest/Avtotest_POM/tests/test_logger_va_data.py`

**Interfeyslar:**
- Consumes: Vazifa 1 dan `conftest`
- Produces:
  - `TestLogger(name: str, out_dir: Path)` — `step(msg)`, `fail(msg)`, `lines: list[str]`,
    `write()` → `<out_dir>/<name>.log`
  - `conftest` fixture'lari: `code` (sessiya bo'yicha noyob qo'shimcha), `save_data(key, value)`,
    `load_data(key, default=None)`, `logger`

**Nega kerak.** Faza 3–4 da port qilinadigan legacy testlar zanjir bo'lib ishlaydi:
`test_company` kompaniya yaratadi, `test_filial` uni ishlatadi. Ular `code` (noyob
qo'shimcha, masalan `pw7431`) va `save_data`/`load_data` (zanjir orasida qiymat uzatish)
ga tayanadi — `smartup_reg/tests/regression/conftest.py` da xuddi shunday. Ularsiz
Faza 3 ning birinchi kuni to'xtaydi.

`code` **sessiya bo'yicha bir marta** hisoblanadi: bir yugurishda yaratilgan barcha
`QA-` yozuvlar bitta qo'shimcha oladi, shuning uchun keyin ularni topish va o'chirish oson.

- [ ] **Qadam 1: Yiqiladigan testni yozish**

`tests/test_logger_va_data.py`:

```python
import json

from utils.logger import TestLogger


def test_logger_qadamlarni_yigadi_va_faylga_yozadi(tmp_path):
    log = TestLogger("test_order", tmp_path)

    log.step("Заказы ro'yxati ochildi")
    log.fail("«Создать» tugmasi topilmadi")

    assert log.lines == ["QADAM: Заказы ro'yxati ochildi",
                         "XATO: «Создать» tugmasi topilmadi"]

    yol = log.write()

    assert yol == tmp_path / "test_order.log"
    matn = yol.read_text(encoding="utf-8")
    assert "QADAM: Заказы" in matn and "XATO: «Создать»" in matn


def test_logger_bosh_bolsa_ham_fayl_yoziladi(tmp_path):
    yol = TestLogger("bosh", tmp_path).write()

    assert yol.exists()
    assert yol.read_text(encoding="utf-8") == ""


def test_code_fixture_barqaror(code):
    """Bir sessiyada `code` o'zgarmaydi — zanjirdagi barcha yozuvlar bitta qo'shimcha oladi."""
    assert isinstance(code, str) and code
    assert code.isalnum()


def test_save_va_load_data(save_data, load_data):
    save_data("client_name", "QA-mijoz-1")

    assert load_data("client_name") == "QA-mijoz-1"
    assert load_data("yoq_kalit") is None
    assert load_data("yoq_kalit", "sukut") == "sukut"
```

- [ ] **Qadam 2: Testni yuritib yiqilishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_logger_va_data.py -v
```

Kutilgan: `ModuleNotFoundError: No module named 'utils.logger'` — FAIL.

- [ ] **Qadam 3: `utils/logger.py` yozish**

```python
# -*- coding: utf-8 -*-
"""Test qadamlarining oddiy jurnali.

Manba: `Smartupauto/utils/logger.py` (127 qator) — undan Telegram va global holat
bog'liqliklari olib tashlandi. `except Exception: pass` ishlatilmaydi (Faza 0 qoidasi):
faylga yozish muvaffaqiyatsiz bo'lsa xato ko'rinadi.
"""
from pathlib import Path


class TestLogger:
    def __init__(self, name, out_dir):
        self.name = name
        self.out_dir = Path(out_dir)
        self.lines = []

    def step(self, message):
        self.lines.append("QADAM: %s" % message)

    def fail(self, message):
        self.lines.append("XATO: %s" % message)

    def write(self):
        """Jurnalni `<out_dir>/<name>.log` ga yozadi va yo'lni qaytaradi."""
        self.out_dir.mkdir(parents=True, exist_ok=True)
        yol = self.out_dir / ("%s.log" % self.name)
        yol.write_text("\n".join(self.lines), encoding="utf-8")
        return yol
```

- [ ] **Qadam 4: `conftest.py` ga fixture'larni qo'shish**

`conftest.py` oxiriga (import blokiga `import uuid` qo'shilsin):

```python
@pytest.fixture(scope="session")
def code():
    """Bir yugurish uchun noyob qo'shimcha (masalan `pw7f3a91`).

    Zanjirdagi barcha `QA-` yozuvlar bitta qo'shimcha oladi — keyin ularni topish
    va o'chirish oson bo'ladi. Sessiya bo'yicha BIR MARTA hisoblanadi.
    """
    return "pw" + uuid.uuid4().hex[:6]


@pytest.fixture(scope="session")
def _data_store():
    return {}


@pytest.fixture
def save_data(_data_store):
    """Zanjirdagi keyingi testlar uchun qiymat saqlaydi."""
    def saqla(key, value):
        _data_store[key] = value
        return value
    return saqla


@pytest.fixture
def load_data(_data_store):
    """Oldingi test saqlagan qiymatni o'qiydi."""
    def oqi(key, default=None):
        return _data_store.get(key, default)
    return oqi


@pytest.fixture
def logger(request, tmp_path):
    """Test qadamlari jurnali. Test tugagach faylga yoziladi."""
    from utils.logger import TestLogger

    log = TestLogger(request.node.name, tmp_path)
    yield log
    log.write()
```

- [ ] **Qadam 5: Testni yuritib o'tishini tasdiqlash**

```bash
.venv/bin/pytest tests/test_logger_va_data.py -v && .venv/bin/pytest -q
```

Kutilgan: `4 passed`; butun to'plam `155 passed, 3 skipped`.

- [ ] **Qadam 6: Commit**

```bash
git add utils/logger.py conftest.py tests/test_logger_va_data.py
git commit -m "$(cat <<'EOF'
feat(faza1): TestLogger va code/save_data/load_data fixture'lari

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
)"
```

---

## Spec dan ongli chetlanishlar

Spec `§5 Faza 1` uchta narsani ham sanaydi, lekin ular bu rejaga KIRMAYDI — sababi bilan:

| Spec bandi | Qaror | Sabab |
|---|---|---|
| `utils/telegram.py` porti | **Faza 5 ga** | Hozir uni chaqiradigan hech narsa yo'q. Tungi zanjir Faza 5 da quriladi; xabar formati o'sha paytdagi natija tuzilmasiga bog'liq. Hozir port qilsak, ikki marta yozamiz (YAGNI). |
| `utils/allure_helper.py` porti | **Faza 2 ga** | Allure biriktirish `SoftAssert` ichida allaqachon bor. Alohida yordamchi 858 JSON case'ning qadam-qadam biriktirishi uchun kerak bo'ladi — o'sha paytda talab aniq bo'ladi. |
| `utils/run_logger.py` porti | **Faza 5 ga** | U yugurish darajasidagi jurnal (tungi zanjir uchun). `TestLogger` test darajasida yetarli. |
| `data/` ni `Avtotest_POM/data/` ga ko'chirish | **Faza 5 ga** | Hozir `baseline.py` va `bug_report.py` ularni `SmartUp_Autotest/data/` dan **o'qiyapti**. Nusxa olsak ikki manba paydo bo'ladi va JS to'plami hali ishlayotgani uchun ular ajralib ketadi. Ko'chirish JS to'plami arxivlanadigan paytda — Faza 5 da — bir martada qilinadi. |

Bu chetlanishlar Faza 1 ning chiqish mezonlariga ta'sir qilmaydi.

---

## Faza 1 chiqish mezonlari

Spec `§5 Faza 1` bo'yicha tekshiriladi:

| Mezon | Qanday tasdiqlanadi |
|---|---|
| Poydevor qurilgan | `pages/ui/`, `pages/components/`, `base_page.py`, `factory.py` mavjud |
| `BasePage` 100 qatordan oshmaydi | `wc -l pages/base_page.py` |
| Brauzersiz testlar | `.venv/bin/pytest -q` → `155 passed, 3 skipped` |
| a2 da jonli smoke yashil | `pytest tests/live --live` → 1-test PASS |
| Eski UI adapteri ishlaydi | 3-test PASS yoki SKIP (forma ko'chirilgan bo'lsa) |
| Filial nazorati | 2-test PASS — `Toshkent` |
| Jimgina yutish yo'q | `grep -rn "except Exception: *pass" pages utils` → bo'sh |

## Faza 2 ga qoldiriladigan ishlar (bu rejada YO'Q)

- 858 JSON case ijrochisi (`tests/json_driven/`) va 28 ta action ni POM ga bog'lash
- Yetishmayotgan 5 action: `menu_plus` (Menu da bor, lekin case bilan bog'lanmagan),
  `remove_tag`, `assert_download`, `assert_no_request`, `manual`
- Assert'siz 245 case ga `expected` matnidan assert generatsiya qilish
- `known_bugs.json` bilan `xfail` bog'lanishi
- Faza 0 da aniqlangan 5 ta «qator bor, amal chiqmadi» sahifasini qo'lda tekshirish:
  Главное→Состояния задач · Справочники→Типы фото-отчетов · Оборудование→Неисправности
  оборудовния · Склад→product_serials · Торговый маркетинг→tpl
