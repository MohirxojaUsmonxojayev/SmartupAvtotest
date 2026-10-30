# Faza 2 natijasi — JSON case'larni POM ijrochisida yuritish

**Sana:** 2026-10-04 · **Reja:** `2026-09-30-faza2-json-ijrochi-reja.md`
**Natija papkasi:** `Tungi_natijalar/2026-10-03_faza2_pom_final/`

## Nima qurildi

858 ta qo'lda yozilgan test case'ni (JSON) real brauzerda yurituvchi ijrochi.
Case'lar O'ZGARMADI — o'zgargani ijrochi: eski JavaScript o'rniga POM arxitekturali
Python.

    data/regression_cases.json  →  runner/cases.py     (o'qish, tartiblash)
                                →  tests/test_regression.py  (sessiya, dalil, yozuv)
                                →  runner/actions.py   (31 action → POM)
                                →  pages/              (POM, ikki UI adapteri)
                                →  runner/record.py    (natija, Faza 0 formati)
                                →  scripts/bug_report.py  (Jira hisoboti)

Brauzersiz testlar: **676 o'tadi** (`python -O` bilan ham).

## Yugurish natijasi

| | Son |
|---|---|
| Jami case | 858 |
| `auto=true` bajarildi | **548 / 548** |
| O'tdi | 134 (24%) |
| Yiqildi | 414 |
| `auto=false` (qo'lda) | 310 |
| **Tarmoq sababli yo'qolgan** | **0** |

## Baza (2026-09-29) bilan taqqoslash

| Guruh | Son | Ma'nosi |
|---|---|---|
| Bir xil | 654 | Bazada ham shunday natija |
| **Yangi assert topdi** | **67** | Generatsiya qilingan tekshiruv muammo topdi — yutuq |
| Yaxshilandi | 6 | Bazada yiqilgan, endi o'tadi |
| Yangi yiqilish | 36 | Tekshirish kerak |

## Yiqilishlar toifasi

| Toifa | Son | Nima qilinadi |
|---|---|---|
| MALUM | 179 | Ma'lum bug takrorlandi — yangi emas |
| TRIAJ | 165 | Triaj kerak; regressiya nomzodlariga to'liq hisobot |
| AVTOTEST | 61 | Selektor/navigatsiya — bug EMAS |
| **ILOVA_BUG** | **9** | **Yangi ilova bug'i — Jira'ga tayyor** |
| BUZILGAN | 0 | Qayta yuritish kerak bo'lganlar yo'q |

## Yetkazilgan dalil

- **170 ta to'liq hisobot** + **170 skrinshot**, modul bo'yicha
  (`Buglar/<NN_Modul>/hisobotlar/*.md`, qo'lda yozilgan konvensiyaga mos)
- 80 ta Playwright trace (chegara: 40; qolganini `--cases <ID>` bilan olish mumkin)
- Har case uchun qadam jurnali

Har hisobotda: raqamlangan qadamlar jadvali, yiqilgan qadam **qalin va ❌** bilan,
kutilgan va haqiqiy natija, tarmoq so'rovlari, muhit, skrinshot havolasi.

## Topilgan haqiqiy server xatolari (namunalar)

    HTTP 500  /xtrade/b/trade/tr/plugin:get_survey_data      (5 case, Продажа)
    HTTP 400  /xtrade/b/biruni/ms/report_list:executive      (Главное)
    Ошибка    /xtrade/b/anor/mrf/van+add:save — dublikat     (Склад)
    Ошибка    /xtrade/b/anor/mhr/division+add:save           (Справочники)

Bular xato oynasi tekshiruvi tufayli ko'rindi. U ulanmagan bo'lsa, bu case'lar
«Pass» deb yozilardi.

## Chiqish mezoni — qisman bajarildi

| Mezon | Holat |
|---|---|
| 548 auto case yuritiladi | ✅ bajarildi |
| Assert'li case ulushi 100% | ✅ 547/548 (99.8%) |
| Bazaga nisbatan Fail oshmagan | ❌ 36 ta yangi yiqilish |

Uchinchi mezon bajarilmadi. Lekin uni to'g'ri o'qish kerak: case'larga **1182 ta
yangi tekshiruv qadami** qo'shilgan va xato oynasi qo'riqchisi ulangan, shuning uchun
yangi yiqilish qisman TABIIY. Taqqoslash vositasi ularni ajratadi: 67 tasi
generatsiya qilingan assert topgan muammo (yutuq), 36 tasi tekshirish kerak.

## Jarayon davomida topilgan nuqsonlar

Har vazifada sharh kamida bitta haqiqiy nuqson topdi. Eng muhimlari:

| Nuqson | Qanday topildi |
|---|---|
| 7 assert action'ni o'chirsa ham to'plam yashil qolardi | Mutatsiya tekshiruvi |
| 8 yalang'och `assert` — `python -O` bilan 10 qo'riqchi yo'qolardi | Mutatsiya tekshiruvi |
| Xato oynasi tekshiruvi ijrochiga ulanmagan | Yakuniy sharh |
| Qayta logindan keyin filial tiklanmas edi | **Jonli yugurish** (skrinshot) |
| `confirm`/`row_action`/`tab` — manbadagi ishlaydigan yo'llar olib tashlangan | **Jonli yugurish** |
| Playwright Python API metod emas, property | Sharh |
| Tarmoq uzilishi butun yugurishni yo'q qiladi | **Jonli yugurish** (ikki marta) |

Oxirgi to'rttasi FAQAT real serverda ko'rindi — 676 brauzersiz test ularni tuta
olmadi va tuta olmasdi ham.

## Faza 3 ga ochiq masalalar

1. **`assert_buttons` 83 yiqilish** — eng katta guruh. Faza 0 da ham eng zaif amal
   edi (21%). Case ma'lumotidagi tugma ro'yxatlari eskirgan bo'lishi mumkin —
   qo'lda ko'rib chiqish kerak.
2. **58 timeout** — sabab aniqlanmagan: sekin sahifa, noto'g'ri selektor yoki
   ilova nuqsoni bo'lishi mumkin.
3. **56 «kutilgan matn yo'q»** — generatsiya qilingan `assert_text` lar sifati.
4. `TC-SKL-FMR-005` — yagona assert'siz case (`data/QOLDA_KORISH.md`).
5. `TC-TM-RZ-003` — case faylida qo'lda yozilgan shablonli assert, har yugurishda
   yiqiladi (hujjatlashtirilgan).
6. Disk: har yugurish ~100 MB. Eski natijalarni arxivlash tartibi kerak.
