// Umumiy sozlamalar: rollar, natija papkasi, RUN id, parolni Keychain'dan olish.
// Parol hech qachon log/hisobotga yozilmaydi.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CFG = JSON.parse(fs.readFileSync(process.env.ROLES_FILE || path.join(ROOT, 'config', 'roles.json'), 'utf8'));
const today = () => {
  const d = new Date(Date.now() + 5 * 3600 * 1000); // Toshkent (UTC+5)
  return d.toISOString().slice(0, 10);
};
const RESULTS_DIR = process.env.RESULTS_DIR || path.resolve(ROOT, '..', 'Tungi_natijalar', today());
const SIM_RUN = process.env.SIM_RUN || today().slice(2).replace(/-/g, ''); // 260929
const AUTH_DIR = path.join(ROOT, '.auth');

function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); return p; }
function appendJsonl(name, obj) {
  ensureDir(RESULTS_DIR);
  fs.appendFileSync(path.join(RESULTS_DIR, name), JSON.stringify({ ts: new Date().toISOString(), ...obj }) + '\n');
}
function writeJson(name, obj) {
  ensureDir(RESULTS_DIR);
  fs.writeFileSync(path.join(RESULTS_DIR, name), JSON.stringify(obj, null, 1));
}

function getPassword(role) {
  const r = CFG.roles.find((x) => x.role === role);
  if (!r) throw new Error(`rol topilmadi: ${role}`);
  const env = process.env['SMARTUP_PW_' + role.toUpperCase()];
  if (env) return env;
  if (process.platform === 'darwin') {
    try {
      return execFileSync('security', ['find-generic-password', '-s', CFG.keychainService, '-a', r.login, '-w'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    } catch (e) {
      throw new Error(`Keychain'da parol yo'q: service=${CFG.keychainService}, account=${r.login} (scripts/add_password.sh ${role})`);
    }
  }
  throw new Error(`Parol topilmadi: SMARTUP_PW_${role.toUpperCase()} muhit o'zgaruvchisi yoki macOS Keychain kerak`);
}

function authFile(role) { return path.join(AUTH_DIR, `${role}.json`); }
function authOk(role) {
  try { return JSON.parse(fs.readFileSync(path.join(RESULTS_DIR, 'auth.json'), 'utf8'))[role]?.ok === true && fs.existsSync(authFile(role)); } catch { return fs.existsSync(authFile(role)); }
}

// Sessiya tugagan bo'lsa (SmartUp sessiya limiti) — shu rol bilan qayta login va storageState yangilash
async function relogin(page, role) {
  const S = require('./smt');
  const r = CFG.roles.find((x) => x.role === role);
  await S.login(page, CFG.baseURL, r.login, getPassword(role));
  await page.goto(CFG.baseURL + '/xtrade/a2/trade/tvt/plan/room_list'); await S.idle(page, 2500);
  await S.switchFilial(page, CFG.filial).catch(() => {});
  await page.context().storageState({ path: authFile(role) });
  appendJsonl('relogin.jsonl', { role });
}

module.exports = { relogin, ROOT, CFG, RESULTS_DIR, SIM_RUN, AUTH_DIR, ensureDir, appendJsonl, writeJson, getPassword, authFile, authOk, today };
