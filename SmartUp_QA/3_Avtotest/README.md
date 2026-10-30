# 3_Avtotest — avtotest fayllari

| Papka | Nima |
|---|---|
| `SmartUp_Autotest/` | Playwright loyiha. `npm run smoke+regression` (login → smoke → regression), `npm run nightly` (to'liq tungi: setup → health → regression → access → sim). O'rnatish va parollar — `SmartUp_Autotest/README.md` |
| `Test_caselar_json/<NN_Modul>/<NN_Forma>/test_cases.json` | 28.09 test case'larining mashina formati (action/target/value) — qo'lda o'qiladigan nusxasi `../1_Smoke_2026-09-28/Test_caselar/` da |
| `Bug_test_caselar_json/` | Bug test case'lari JSON'da: 28.09 — modul bo'yicha; `Regression_<sana>/` — regressionda topilgan yangi buglar |
| `Lokatorlar/<NN_Modul>.md` | Selektorlar va API manzillari |
| `Ketma-ketlik/` | `run_order.json|xlsx` — case'lar bir-biriga xalaqit bermaydigan tartib (15 bosqich) |
| `Namuna_playwright/` | JSON runner skeleti (bitta `test_cases.json` ni yuritish) |
| `Tungi_natijalar/<sana>/` | `scripts/nightly.sh` natijalari (health/regression/access/sim .jsonl, shots, html, SUMMARY.md) |

Papka ko'chirilgandan keyin launchd (04:00) ni yangi yo'l bilan qayta o'rnating: `bash SmartUp_Autotest/scripts/launchd_install.sh`.
