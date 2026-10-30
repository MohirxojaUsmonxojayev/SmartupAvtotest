# CLAUDE.md — SmartUp avtotest

Bu papka faqat avtotest kodi va natijalari uchun (PyCharm + Claude Code). Javoblar o'zbek tilida, qisqa.

## Qoidalar
1. Maxfiy ma'lumotlar faqat `3_Avtotest/.env` da (ruxsat 600; namuna `.env.example`). Parol/token kod, hujjat, log yoki commit'ga yozilmaydi; `.env` repo ichiga ko'chirilmaydi. Yuritishdan oldin: `set -a; . ../.env; set +a`. Login avtomatik: `lib/env.js` → `SMARTUP_PW_<ROL>`, topilmasa macOS Keychain (service `smartup-xtrade`).
2. Test serveri: https://app3.greenwhite.uz/xtrade, foydalanuvchi mohir@xan, filial Toshkent.
3. Foydalanuvchi/huquq/sozlamalar o'zgartirilmaydi. Faqat o'z QA-/SIM- yozuvlari o'chiriladi. Begona hujjat o'tkazilmaydi/o'chirilmaydi. Tashqi tizimlarga (WMS, Soliq, Faktura, Telegram, CRPT) yuborilmaydi.
4. «Test/Deploy Flow» Google Sheet faqat o'qiladi.
5. Qo'lda test case'lar (md/xlsx) bu yerda emas: ular `../Smoke/` va `../Regression/` da. Bu papkada faqat avtotest (json/js/py) fayllari.
6. Ma'lum buglar: `SmartUp_Autotest/data/known_bugs.json` — asosiy reyestrning nusxasi (asosiysi `../_Claude/buglar/registry.json`, uni Cowork'dagi Claude yuritadi). Bu nusxani qo'lda tahrirlamang.
7. Tungi natijalar: `Tungi_natijalar/<sana>/`, tahlil `SmartUp_Autotest/scripts/analyze.py <kun_papkasi>`. Natijalar `../Smoke`, `../Regression` papkalariga yozilmaydi.
8. POM birlashtirish rejasi: `Hujjatlar/2026-09-29-pom-birlashtirish-design.md`. Eski loyihalar (`../SmartupAuto_repo`, `../Smartupauto`, `../playwright_original`, `../smartup_reg`) — 3/4-faza manbalari, o'zgartirilmaydi.
