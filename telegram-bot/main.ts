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
//   LOCAL_AGENT_SECRET        — «🖥 Local run»: Mac agenti (scripts/localagent.py) kaliti (Bearer)
//
// «🖥 Local run» (CODE-028): Mac'dagi testlarni yurgizish. Server Mac'ga ulana olmaydi, shuning uchun Mac agenti
// GET /local/next ni kutib turadi (long poll ≤ 25 s); tugma bosilsa buyruq Deno KV navbatidan shu so'rovga qaytadi.
// Agent POST /local/ack bilan qabul qilganini (va javob matnini) bildiradi. Buyruqlar — qat'iy ro'yxat (LOCAL_CMDS).
// Faqat lokal sinov uchun (Deploy'da qo'yilmaydi): TELEGRAM_API_BASE, LOCAL_KV_PATH.
// =====================================================================================================================

const TG_TOKEN = Deno.env.get("TELEGRAM_BOT_TOKEN") ?? "";
const ALLOWED = new Set(
  (Deno.env.get("TELEGRAM_ALLOWED_CHAT_IDS") ?? "")
    .split(",").map((s) => s.trim()).filter(Boolean),
);
const GH_TOKEN = Deno.env.get("GITHUB_TOKEN") ?? "";
const GH_REPO = Deno.env.get("GITHUB_REPO") ?? "";
const WEBHOOK_SECRET = Deno.env.get("WEBHOOK_SECRET") ?? "";
const LOCAL_SECRET = Deno.env.get("LOCAL_AGENT_SECRET") ?? "";
const TG_API = (Deno.env.get("TELEGRAM_API_BASE") ?? "https://api.telegram.org").replace(/\/+$/, "");

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
  const r = await fetch(`${TG_API}/bot${TG_TOKEN}/${method}`, {
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
// Doimiy (persistent) tugma — har safar /run yozmaslik uchun. Chat ostida turadi.
const runKeyboard = () => ({
  keyboard: [[{ text: "🚀 Run test" }, { text: "🖥 Local run" }]],
  resize_keyboard: true,
  is_persistent: true,
});

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

const localKeyboard = () => ({
  inline_keyboard: [
    [{ text: "▶️ Hammasi (kz + xs)", callback_data: "loc:all" }],
    [
      { text: "Кадры (kz)", callback_data: "loc:kz" },
      { text: "Xarid-sotuv (xs)", callback_data: "loc:xs" },
      { text: "Smoke", callback_data: "loc:smoke" },
    ],
    [
      { text: "📊 Holat", callback_data: "loc:status" },
      { text: "📄 Oxirgi natija", callback_data: "loc:natija" },
    ],
    [{ text: "⏹ To'xtatish", callback_data: "loc:stop?" }],
  ],
});

const stopConfirmKeyboard = () => ({
  inline_keyboard: [[
    { text: "⏹ Ha, to'xtat", callback_data: "loc:stop" },
    { text: "✖️ Bekor", callback_data: "cxl" },
  ]],
});

// ---------------------------------------------------------------------------------------------------------------------
// «🖥 Local run» — Mac agenti uchun buyruq navbati (Deno KV)
// ---------------------------------------------------------------------------------------------------------------------
// Qat'iy ro'yxat: agent ham faqat shularni qabul qiladi (boshqasi — rad). Matn hech qachon shell'ga berilmaydi.
const LOCAL_CMDS: Record<string, string> = {
  all: "▶️ Hammasi (kz + xs)",
  kz: "Кадры (kz)",
  xs: "Xarid-sotuv (xs)",
  smoke: "Smoke",
  status: "📊 Holat",
  natija: "📄 Oxirgi natija",
  stop: "⏹ To'xtatish",
};
const LOCAL_POLL_MS = 25_000;             // long poll davomiyligi
const LOCAL_OFFLINE_MS = 60_000;          // agent shuncha vaqt ulanmasa — «oflayn»
const LOCAL_TTL_MS = 12 * 60 * 60 * 1000; // eski buyruq bekor qilinadi
const LOCAL_REDELIVER_MS = 60_000;        // ack kelmasa qayta beriladi
const Q_PREFIX = ["local", "q"];
const SIGNAL_KEY = ["local", "signal"];
const AGENT_KEY = ["local", "agent"];

interface LocalItem { id: string; cmd: string; chat: string; ts: number; delivered?: number }

let _kv: Deno.Kv | null = null;
async function kv(): Promise<Deno.Kv> {
  return _kv ??= await Deno.openKv(Deno.env.get("LOCAL_KV_PATH") || undefined);
}

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

async function agentOnline(): Promise<boolean> {
  const seen = (await (await kv()).get<{ seen: number }>(AGENT_KEY)).value?.seen ?? 0;
  return Date.now() - seen <= LOCAL_OFFLINE_MS;
}

async function touchAgent(): Promise<void> {
  await (await kv()).set(AGENT_KEY, { seen: Date.now() });
}

async function enqueueLocal(cmd: string, chat: string): Promise<void> {
  const db = await kv();
  const ts = Date.now();
  const id = `${ts}-${crypto.randomUUID().slice(0, 8)}`;
  const item: LocalItem = { id, cmd, chat, ts };
  await db.set([...Q_PREFIX, ts, id], item);
  await db.set(SIGNAL_KEY, ts);           // kutib turgan /local/next ni uyg'otadi
}

/** Navbatdagi (eng eski, berilmagan yoki ack'siz qolgan) buyruq. 12 soatdan eskisi bekor qilinadi. */
async function takeNextLocal(): Promise<LocalItem | null> {
  const db = await kv();
  const now = Date.now();
  for await (const e of db.list<LocalItem>({ prefix: Q_PREFIX })) {
    const item = e.value;
    if (now - item.ts > LOCAL_TTL_MS) {
      await db.delete(e.key);
      await send(item.chat, `⌛ Local run buyrug'i bekor qilindi (12 soat ichida Mac ulanmadi): <b>${esc(LOCAL_CMDS[item.cmd] ?? item.cmd)}</b>`);
      continue;
    }
    if (item.delivered && now - item.delivered < LOCAL_REDELIVER_MS) continue;
    await db.set(e.key, { ...item, delivered: now });
    return item;
  }
  return null;
}

async function ackLocal(id: string, text: string): Promise<boolean> {
  const db = await kv();
  for await (const e of db.list<LocalItem>({ prefix: Q_PREFIX })) {
    if (e.value.id !== id) continue;
    await db.delete(e.key);
    if (text) await send(e.value.chat, `🖥 ${esc(text.slice(0, 3500))}`, runKeyboard());
    return true;
  }
  return false;
}

function agentAuthorized(req: Request): boolean {
  if (!LOCAL_SECRET) return false;         // kalit sozlanmagan — hech kim kira olmaydi
  const got = new TextEncoder().encode(req.headers.get("authorization") ?? "");
  const want = new TextEncoder().encode(`Bearer ${LOCAL_SECRET}`);
  let diff = got.length ^ want.length;     // doimiy vaqtli solishtirish
  for (let i = 0; i < want.length; i++) diff |= (got[i] ?? 0) ^ want[i];
  return diff === 0;
}

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });

/** GET /local/next — buyruq bo'lsa darhol, bo'lmasa ≤ 25 s kutib bo'sh javob ({}). */
async function localNext(): Promise<Response> {
  await touchAgent();
  const reader = (await kv()).watch([SIGNAL_KEY]).getReader();
  let timer: ReturnType<typeof setTimeout> | undefined;
  try {
    await reader.read();                   // birinchi o'qish — joriy qiymat (darhol)
    let item = await takeNextLocal();
    if (!item) {
      await Promise.race([
        reader.read(),                     // enqueueLocal signal'ni o'zgartirsa uyg'onadi
        new Promise((resolve) => { timer = setTimeout(resolve, LOCAL_POLL_MS); }),
      ]);
      await touchAgent();
      item = await takeNextLocal();
    }
    return json(item ? { id: item.id, cmd: item.cmd } : {});
  } finally {
    clearTimeout(timer);
    reader.cancel().catch(() => {});
  }
}

/** POST /local/ack {id, text?} — agent buyruqni oldi; text bo'lsa buyruq bergan chatga yuboriladi. */
async function localAck(req: Request): Promise<Response> {
  let body: any;
  try { body = await req.json(); } catch { return json({ error: "bad json" }, 400); }
  const id = typeof body?.id === "string" ? body.id : "";
  const text = typeof body?.text === "string" ? body.text : "";
  if (!id) return json({ error: "id kerak" }, 400);
  return json({ ok: await ackLocal(id, text) });
}

async function onLocalCommand(chat: string, cmd: string) {
  if (!LOCAL_CMDS[cmd]) { console.warn("local: noma'lum buyruq", cmd); return; }
  if (!LOCAL_SECRET) {
    await send(chat, "❌ Local run sozlanmagan (LOCAL_AGENT_SECRET yo'q).");
    return;
  }
  const online = await agentOnline();
  await enqueueLocal(cmd, chat);
  await send(
    chat,
    online
      ? `📨 <b>${esc(LOCAL_CMDS[cmd])}</b> — Mac'ga yuborildi.`
      : `💤 Mac hozir oflayn — yoqilganda boshlanadi.\n<b>${esc(LOCAL_CMDS[cmd])}</b> navbatda (12 soatgacha).`,
    runKeyboard(),
  );
}

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
      runKeyboard(),
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
  if (cmd === "/start") {
    // Doimiy "🚀 Run test" tugmasini o'rnatamiz (bir marta — keyin chat ostida turaveradi).
    await send(
      chat,
      "🧪 <b>Smartup Autotest bot</b>\n\nTest ishga tushirish: pastdagi <b>🚀 Run test</b> tugmasi (yoki /run).\n" +
        "Mac'dagi testlar: <b>🖥 Local run</b> (yoki /local).",
      runKeyboard(),
    );
  } else if (cmd === "/run" || text === "🚀 Run test") {
    await send(chat, "🧪 Qaysi serverda test run qilamiz?", serverKeyboard());
  } else if (cmd === "/local" || text === "🖥 Local run") {
    await send(chat, "🖥 <b>Local run</b> — Mac'dagi testlar. Nima qilamiz?", localKeyboard());
  } else if (cmd === "/id") {
    await send(chat, `Chat ID: <code>${chat}</code>`);
  } else if (cmd === "/help") {
    await send(chat, "🚀 Run test (yoki /run) — test ishga tushirish\n🖥 Local run (yoki /local) — Mac'dagi testlar\n/id — chat id\nTestlar GitHub Actions'da ishlaydi, natija + Allure link shu yerga keladi.");
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

  // «🖥 Local run» menyusi
  if (data.startsWith("loc:")) {
    const cmd = data.slice(4);
    if (cmd === "stop?") {
      await send(chat, "⏹ Mac'dagi joriy run to'xtatilsinmi? (navbatdagi run'lar ham bekor bo'ladi)", stopConfirmKeyboard());
    } else {
      await onLocalCommand(chat, cmd);
    }
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
    const parts = data.split(":");
    const runId = Number(parts[1]);
    const server = parts[2];
    const login = parts[3] ?? "";   // bo'sh = default
    // Eski run'ni to'xtatamiz (allaqachon tugagan bo'lsa — zararsiz, e'tiborsiz qoldiramiz).
    if (runId) await cancelRun(runId);

    if (login) {
      // Custom login edi — parolni qayta so'raymiz (parol hech qayerda saqlanmaydi).
      await send(
        chat,
        `♻️ Eski run to'xtatildi. ${server} uchun login va parolni qayta yuboring:\n<code>login parol</code>\n\n${REPLY_MARKER(server)}`,
        { force_reply: true, input_field_placeholder: "login parol" },
      );
    } else {
      // Default edi — konfliktni qayta tekshirmay to'g'ridan-to'g'ri dispatch (loop bo'lmasin).
      const ok = await dispatch(server, "", "", chat);
      await send(
        chat,
        ok
          ? `♻️ <b>Qaytadan boshlandi</b> (default)\n🌐 Server: <b>${server}</b>\n🔗 ${runsUrl()}`
          : `❌ Dispatch xatosi.`,
        runKeyboard(),
      );
    }
    return;
  }
}

// ---------------------------------------------------------------------------------------------------------------------
// HTTP (Telegram webhook)
// ---------------------------------------------------------------------------------------------------------------------
Deno.serve(async (req) => {
  // Mac agenti (Bearer LOCAL_AGENT_SECRET) — Telegram webhook'idan oldin
  const path = new URL(req.url).pathname;
  if (path === "/local/next" || path === "/local/ack") {
    if (!agentAuthorized(req)) return json({ error: "unauthorized" }, 401);
    try {
      if (path === "/local/next" && req.method === "GET") return await localNext();
      if (path === "/local/ack" && req.method === "POST") return await localAck(req);
    } catch (e) {
      console.error("local endpoint error:", e);
      return json({ error: "internal" }, 500);
    }
    return json({ error: "method not allowed" }, 405);
  }

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
