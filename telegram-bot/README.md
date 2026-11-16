# Telegram Autotest Bot — Deno Deploy

Bu bot Telegramdan test run qilish uchun. Testlar **GitHub Actions**'da ishlaydi; bot faqat
buyruqni qabul qilib GitHub'ga `repository_dispatch` yuboradi (stateless, doim onlayn).

## Imkoniyatlar
- `/run` → server tanlash (online/xtrade) → **default** yoki **vaqtinchalik login/parol**
- Bir nechta odam o'z Telegramida run qila oladi (natija run qilgan odamga keladi)
- **Per-login konflikt**: bir xil login bilan allaqachon ishlayotgan bo'lsa — "to'xtatib qaytadan?" so'raydi;
  boshqa login bo'lsa — parallel ishlaydi
- Parol GitHub Actions UI'da **ko'rinmaydi** (`client_payload` ichida)
- Tugagach natija + **Allure HTML link** + Actions link Telegramga keladi

## Deploy (Deno Deploy — bepul)

1. https://dash.deno.com → **New Project** → GitHub repo'ni ulang yoki "Playground" orqali `main.ts` ni joylang.
   - Entrypoint: `telegram-bot/main.ts`
2. **Settings → Environment Variables** ga qo'shing:

   | Variable | Qiymat |
   |----------|--------|
   | `TELEGRAM_BOT_TOKEN` | bot tokeni |
   | `TELEGRAM_ALLOWED_CHAT_IDS` | ruxsat berilgan chat id'lar, vergul bilan (masalan `6847971883,12345678`) |
   | `GITHUB_TOKEN` | fine-grained PAT — **Contents: Read and write** + **Actions: Read and write** (shu repo uchun) |
   | `GITHUB_REPO` | `egasi/repo` (masalan `MohirxojaUsmonxojayev/SmartupAvtotest`) |
   | `WEBHOOK_SECRET` | ixtiyoriy tasodifiy satr (webhook himoyasi) |
   | `LOCAL_AGENT_SECRET` | «🖥 Local run»: Mac agenti kaliti (uzun tasodifiy satr; Mac'dagi `.env` da ham shu) |

3. Deploy bo'lgach URL olasiz: `https://<project>.deno.dev`

4. Telegram webhook'ni ulang (tokeningiz bilan):
   ```
   https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<project>.deno.dev&secret_token=<WEBHOOK_SECRET>
   ```
   (brauzerda ochsangiz ham bo'ladi — `{"ok":true}` qaytishi kerak)

## 🖥 Local run (Mac'dagi testlar)
Pastki menyuda «🚀 Run test» yonida **«🖥 Local run»**: Hammasi (kz + xs) · Кадры · Xarid-sotuv · Smoke · Holat ·
Oxirgi natija · To'xtatish. Buyruq Deno KV navbatiga yoziladi; Mac'dagi agent (`scripts/localagent.py`, repo `main`)
`GET /local/next` (long poll ≤ 25 s) bilan oladi va `POST /local/ack` bilan javob beradi — ikkalasi
`Authorization: Bearer <LOCAL_AGENT_SECRET>` (noto'g'ri kalit → 401). Agent 60 s ulanmagan bo'lsa bot
«Mac hozir oflayn — yoqilganda boshlanadi» deydi; 12 soatdan eski buyruq bekor qilinadi. Qo'llanma: `docs/local_run.md`.

## Buyruqlar
- `/run` — test ishga tushirish
- `/local` — Mac'dagi testlar menyusi
- `/id` — chat id (ruxsat ro'yxatiga qo'shish uchun)
- `/help`

## Eslatma (xavfsizlik)
- Vaqtinchalik parol: Telegram chatida va `client_payload`'da bo'ladi; Actions UI inputlarida ko'rinmaydi,
  loglarda `::add-mask::` bilan yashiriladi. Login esa run nomida ko'rinadi (konflikt aniqlash uchun).
