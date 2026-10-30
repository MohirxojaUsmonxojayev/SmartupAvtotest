# Faza 0 natijasi — dalil yig'ish

**Sana:** 2026-09-29 (yakunlandi 2026-09-30)
**Reja:** `2026-09-29-faza0-dalil-yigish-reja.md`
**Spetsifikatsiya:** `2026-09-29-pom-birlashtirish-design.md`

## Maqsad

POM loyihasini qurishdan OLDIN bilish: mavjud avtotestning qaysi qismi
haqiqatan ishlaydi. Faraz bilan emas, o'lchov bilan. Shusiz yangi loyihaga
ishlamaydigan selektorlar ko'chirilar edi.

## Nima o'lchandi

858 ta noyob regression case va 226 ta health sahifasi:

| Natija | Son |
|---|---|
| Fail | 317 |
| Pass | 231 |
| Skip | 310 |
| **Jami** | **858** |

Tarmoq/brauzer xatosi: 0 (birinchi yugurishda internet uzilib 157 case yiqilgan edi —
qayta yuritildi). Buzuq qator: 0. Hisobga olinmagan: 3 qator (`failed_step` qadamlar
sonidan katta) — ular jadvallarga hech narsa qo'shmadi, ko'rinarli qilib belgilandi.

## Asosiy xulosa: muammo selektorlarda emas, action qatlamida

Selektorlar sog'lom:

| Selektor | Ishonch |
|---|---|
| `main` | 100% |
| `button:visible` | 98% |
| `label` (forma maydoni) | 98% |
| `.smt-data-row` | 95% |
| `smt-cell-header` | 93% |

Action'lar esa emas:

| Action | Muvaffaqiyat |
|---|---|
| `grid_fill` | 0% |
| `menu_plus` | 0% (umuman yozilmagan) |
| `assert_field` | 22% |
| `assert_buttons` | 21% |
| `assert_api` | 34% |
| `select` | 73% |
| `row_click` | 76% |
| `click` | 91% |
| `nav` | 98% |

Shuning uchun Faza 1 da selektorlar ko'chirildi, action mantiqi esa qayta yozildi.

## Topilgan 6 ta nuqson — hammasi bir turda

Hech biri xato tashlamagan, hech biri logga yozmagan va **hammasi natijani optimistik
tomonga og'dirgan**. Bu Faza 1 ning «jimgina yutuvchi kod taqiqlanadi» qoidasining sababi.

| # | Nuqson | Ta'siri |
|---|---|---|
| R12 | `expect.soft` istisno tashlamaydi — test «Pass» deb yozilgan | 548 tadan 173 tasi (32%) noto'g'ri; 18 ta case hech qachon Fail yoza olmasdi. Tuzatilgandan keyin `assert_buttons` 100% dan **21%** ga tushdi |
| R18 | `.smt-data-row` o'lchovi aslida «qator amallari chiqdimi» ni o'lchagan | 44% ko'rsatgan, aslida **95%** |
| R9 | `failed_step` siz Fail qatori har bir qadamni «ok» deb sanagan | Muvaffaqiyat sun'iy ko'tarilgan |
| R22 | `analyze.py` URL ni faqat bir tomonda normallashtirgan | 48 ta ma'lum bug «YANGI» deb ko'rsatilgan (61 → 109 moslik) |
| R23 | `analyze.py` takroriy qatorlarni birlashtirmagan | Sonlar ikki hisoblangan |
| — | `switchFilial` o'lik selektorlarga murojaat qilgan (`.dropdown-locations-custom` — 0 ta) | Butun sessiya «Администрирование» filialida ketgan, 7 sahifa **soxta 403** qaytargan |

Uchtasi tuzatildi (`smt.js`, `regression.spec.js`, `analyze.py`) — har biri zaxira nusxa bilan.

## Yetkazilgan artefaktlar

- `Avtotest_POM/scripts/baseline.py` — o'lchov vositasi, natija `Tungi_natijalar/2026-09-29/BASELINE.md` va `baseline.json`
- `Avtotest_POM/scripts/bug_report.py` — yiqilishlardan Jira'ga tayyor hisobot yasaydi, 5 toifaga ajratadi
- `Tungi_natijalar/2026-09-29/Buglar/` — **116 ta to'liq hisobot, har biri skrinshot bilan**:

| Toifa | Son | Nima qilinadi |
|---|---|---|
| ILOVA_BUG | 5 | To'liq hisobot — Jira'ga ochish mumkin |
| TRIAJ | 114 | Regressiya nomzodlariga to'liq hisobot |
| MALUM | 147 | Ma'lum bug takrorlandi — qisqa yozuv |
| AVTOTEST | 51 | Avtotest muammosi, bug EMAS — alohida ro'yxat |
| BUZILGAN | 0 | Tarmoq uzilgan — qayta yuritish |

Bu tasniflash bo'lmasa, 317 ta yiqilishning hammasiga hisobot yozilib, Jira soxta bug
bilan to'lar va developer ishonchi yo'qolardi.

## Faza 5 ga qolgan ochiq masala

`retries: 0` va tarmoq uzilishiga qarshi himoya yo'q — qisqa uzilish butun tungi
yugurishni bekor qiladi (29.09 da aynan shunday bo'ldi, 157 case yo'qoldi).
