// =====================================================================================================================
// Smartup Autotest — Telegram webhook bot (Deno Deploy)
//
// Vazifa: Telegramdan test run qilish. Testlar GitHub Actions'da ishlaydi (bu bot faqat
// buyruqni qabul qilib, GitHub'ga repository_dispatch yuboradi — stateless, doim onlayn).
//
// Oqim:
//   /run  → server tugmalari (online/xtrade)
//         → "Default" yoki "Login/parol kiritish"
//         → (custom bo'lsa) "login parol" ni reply qilib yuborasiz
//         → per-login konflikt tekshiruvi:
//              • boshqa login  → parallel dispatch
//              • bir xil login → "To'xtatib qaytadan?" so'raydi
//
// Parol GitHub Actions UI'da ko'rinmaydi (client_payload ichida ketadi).
//
// Kerakli ENV (Deno Deploy sozlamalarida):
//   TELEGRAM_BOT_TOKEN        — bot tokeni
//   TELEGRAM_ALLOWED_CHAT_IDS — ruxsat berilgan chat id'lar (vergul bilan)
//   GITHUB_TOKEN              — PAT (fine-grained: Contents RW + Actions RW)
//   GITHUB_REPO               — "egasi/repo" (masalan MohirxojaUsmonxojayev/SmartupAvtotest)
//   WEBHOOK_SECRET            — (ixtiyoriy) Telegram webhook secret_token
// =====================================================================================================================

const TG_TOKEN = Deno.env.get("TELEGRAM_BOT_TOKEN") ?? "";
const ALLOWED = new Set(
  (Deno.env.get("TELEGRAM_ALLOWED_CHAT_IDS") ?? "")
    .split(",").map((s) => s.trim()).filter(Boolean),
);
const GH_TOKEN = Deno.env.get("GITHUB_TOKEN") ?? "";
const GH_REPO = Deno.env.get("GITHUB_REPO") ?? "";
const WEBHOOK_SECRET = Deno.env.get("WEBHOOK_SECRET") ?? "";

const SERVERS: Record<string, string> = {
  online: "smartup.online",
  xtrade: "app3.greenwhite.uz/xtrade",
};

// Custom login/parol so'ralganda force_reply xabariga qo'yiladigan marker (reply'ni tanish uchun).
const REPLY_MARKER = (server: string) => `#autotest-creds:${server}`;

// Aktiv (tugamagan) run statuslari.
const ACTIVE_STATUSES = new Set(["queued", "in_progress", "waiting", "requested", "pending"]);

// ---------------------------------------------------------------------------------------------------------------------
// Telegram API
// ---------------------------------------------------------------------------------------------------------------------
async function tg(method: string, payload: unknown): Promise<any> {
  const r = await fetch(`https://api.telegram.org/bot${TG_TOKEN}/${method}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  return await r.json().catch(() => ({}));
}

function send(chat: string | number, text: string, keyboard?: unknown) {
  const payload: Record<string, unknown> = {
    chat_id: chat, text, parse_mode: "HTML", disable_web_page_preview: true,
  };
  if (keyboard) payload.reply_markup = keyboard;
  return tg("sendMessage", payload);
}

function answer(cbId: string, text = "") {
  return tg("answerCallbackQuery", { callback_query_id: cbId, text });
}

// ---------------------------------------------------------------------------------------------------------------------
// GitHub API
// ---------------------------------------------------------------------------------------------------------------------
async function gh(path: string, method = "GET", body?: unknown): Promise<Response> {
  return await fetch(`https://api.github.com${path}`, {
    method,
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${GH_TOKEN}`,
      "X-GitHub-Api-Version": "2022-11-28",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
}

/** Berilgan server+login uchun aktiv run bo'lsa uning id'sini qaytaradi (yo'q bo'lsa null). */
async function findActiveRun(server: string, login: string): Promise<number | null> {
  const r = await gh(`/repos/${GH_REPO}/actions/runs?per_page=40`);
  if (!r.ok) return null;
  const data = await r.json();
  const needle = `· ${server} · ${login || "default"}`;
  for (const run of data.workflow_runs ?? []) {
    if (!ACTIVE_STATUSES.has(run.status)) continue;
    const title = String(run.display_title ?? run.name ?? "");
    if (title.includes(needle)) return run.id;
  }
  return null;
}

async function cancelRun(runId: number): Promise<void> {
  await gh(`/repos/${GH_REPO}/actions/runs/${runId}/cancel`, "POST");
}

/** repository_dispatch — testni GitHub Actions'da ishga tushiradi. Parol client_payload'da (UI'da ko'rinmaydi). */
async function dispatch(server: string, login: string, password: string, chatId: string): Promise<boolean> {
  const r = await gh(`/repos/${GH_REPO}/dispatches`, "POST", {
    event_type: "autotest",
    client_payload: { server, login, password, chat_id: chatId },
  });
  return r.status === 204;
}

const runsUrl = () => `https://github.com/${GH_REPO}/actions`;

// ---------------------------------------------------------------------------------------------------------------------
// Keyboards
// ---------------------------------------------------------------------------------------------------------------------
const serverKeyboard = () => ({
  inline_keyboard: [[
    { text: "🟢 online", callback_data: "srv:online" },
    { text: "🔵 xtrade", callback_data: "srv:xtrade" },
  ]],
});

const credKeyboard = (server: string) => ({
  inline_keyboard: [[
    { text: "✅ Default login/parol", callback_data: `cred:${server}:def` },
    { text: "✍️ Login/parol kiritish", callback_data: `cred:${server}:cus` },
  ]],
});

const conflictKeyboard = (server: string, login: string, runId: number) => ({
  inline_keyboard: [[
    { text: "♻️ To'xtatib qaytadan", callback_data: `rst:${runId}:${server}:${login}` },
    { text: "✖️ Bekor", callback_data: "cxl" },
  ]],
});

// ---------------------------------------------------------------------------------------------------------------------
// Biznes-mantiq
// ---------------------------------------------------------------------------------------------------------------------

/** Konfliktni tekshirib, kerak bo'lsa so'raydi, aks holda dispatch qiladi. */
async function startRun(chat: string, server: string, login: string, password: string) {
  const activeId = await findActiveRun(server, login);
  if (activeId !== null) {
    const who = login || "default";
    await send(
      chat,
      `⚠️ <b>${server}</b> serverida <code>${who}</code> login bilan avtotest allaqachon ishlamoqda.\n\n` +
        `Eskisini to'xtatib qaytadan boshlaymi, yoki boshqa login/parol bilan run qiling.`,
      conflictKeyboard(server, login, activeId),
    );
    return;
  }
  const ok = await dispatch(server, login, password, chat);
  if (ok) {
    await send(
      chat,
      `🚀 <b>Run boshlandi</b> (GitHub Actions)\n🌐 Server: <b>${server}</b>\n👤 Login: <code>${login || "default"}</code>\n` +
        `🔗 ${runsUrl()}\n\nTugagach natija + Allure link shu yerga keladi.`,
    );
  } else {
    await send(chat, `❌ Dispatch xatosi. GITHUB_TOKEN/ GITHUB_REPO sozlamalarini tekshiring.`);
  }
}

// ---------------------------------------------------------------------------------------------------------------------
// Update handlerlar
// ---------------------------------------------------------------------------------------------------------------------
async function onMessage(msg: any) {
  const chat = String(msg.chat?.id ?? "");
  if (!ALLOWED.has(chat)) {
    if (chat) await send(chat, "⛔ Bu chatga ruxsat yo'q.");
    return;
  }
  const text = String(msg.text ?? "").trim();

  // Custom login/parol reply'si (force_reply bilan so'ralgan).
  const replyText = String(msg.reply_to_message?.text ?? "");
  const markerMatch = replyText.match(/#autotest-creds:(\w+)/);
  if (markerMatch) {
    const server = markerMatch[1];
    const parts = text.split(/\s+/);
    if (parts.length < 2) {
      await send(chat, "❌ Format: <code>login parol</code> (bitta qatorda, probel bilan).");
      return;
    }
    const login = parts[0];
    const password = parts.slice(1).join(" ");
    await startRun(chat, server, login, password);
    return;
  }

  const cmd = text.split(/\s+/)[0].split("@")[0].toLowerCase();
  if (cmd === "/start" || cmd === "/run") {
    await send(chat, "🧪 Qaysi serverda test run qilamiz?", serverKeyboard());
  } else if (cmd === "/id") {
    await send(chat, `Chat ID: <code>${chat}</code>`);
  } else if (cmd === "/help") {
    await send(chat, "/run — test ishga tushirish\n/id — chat id\nTestlar GitHub Actions'da ishlaydi, natija + Allure link shu yerga keladi.");
  }
}

async function onCallback(cb: any) {
  const cbId = String(cb.id ?? "");
  const chat = String(cb.message?.chat?.id ?? "");
  const data = String(cb.data ?? "");
  if (!ALLOWED.has(chat)) { await answer(cbId, "Ruxsat yo'q"); return; }
  await answer(cbId);

  if (data === "cxl") {
    await send(chat, "✖️ Bekor qilindi.");
    return;
  }

  // Server tanlandi → login rejimini so'raymiz
  if (data.startsWith("srv:")) {
    const server = data.slice(4);
    if (!SERVERS[server]) return;
    await send(chat, `Server: <b>${server}</b> (${SERVERS[server]})\nLogin/parol?`, credKeyboard(server));
    return;
  }

  // Credential rejimi
  if (data.startsWith("cred:")) {
    const [, server, mode] = data.split(":");
    if (!SERVERS[server]) return;
    if (mode === "def") {
      await startRun(chat, server, "", "");
    } else {
      // force_reply bilan login/parol so'raymiz (marker reply'ni tanish uchun)
      await send(
        chat,
        `✍️ ${server} uchun login va parolni bitta qatorda yuboring:\n<code>login parol</code>\n\n${REPLY_MARKER(server)}`,
        { force_reply: true, input_field_placeholder: "login parol" },
      );
    }
    return;
  }

  // Konflikt: to'xtatib qaytadan
  if (data.startsWith("rst:")) {
    const [, runIdStr, server, login] = data.split(":");
    const runId = Number(runIdStr);
    if (runId) await cancelRun(runId);
    await send(chat, `♻️ Eski run to'xtatildi.`);
    if (login) {
      // Custom login edi — parolni qayta so'raymiz (parol hech qayerda saqlanmaydi)
      await send(
        chat,
        `✍️ ${server} uchun login va parolni qayta yuboring:\n<code>login parol</code>\n\n${REPLY_MARKER(server)}`,
        { force_reply: true, input_field_placeholder: "login parol" },
      );
    } else {
      // Default edi — darhol qayta dispatch
      await startRun(chat, server, "", "");
    }
    return;
  }
}

// ---------------------------------------------------------------------------------------------------------------------
// HTTP (Telegram webhook)
// ---------------------------------------------------------------------------------------------------------------------
Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("Smartup Autotest bot", { status: 200 });

  if (WEBHOOK_SECRET && req.headers.get("X-Telegram-Bot-Api-Secret-Token") !== WEBHOOK_SECRET) {
    return new Response("forbidden", { status: 403 });
  }

  let update: any;
  try { update = await req.json(); } catch { return new Response("ok"); }

  try {
    if (update.message) await onMessage(update.message);
    else if (update.callback_query) await onCallback(update.callback_query);
  } catch (e) {
    console.error("handler error:", e);
  }
  return new Response("ok");
});
