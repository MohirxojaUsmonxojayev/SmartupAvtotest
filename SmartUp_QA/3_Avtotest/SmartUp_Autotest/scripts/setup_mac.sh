#!/bin/bash
# Bir martalik o'rnatish (Terminal'da): bash scripts/setup_mac.sh
set -e
cd "$(dirname "$0")/.."
DIR="$(pwd)"
command -v node >/dev/null || { echo "Node.js yo'q: brew install node"; exit 1; }
echo "1) Paketlar va Chromium"
npm install --no-audit --no-fund
npx playwright install chromium
echo "2) Admin paroli Keychain'ga (boshqa rollar: bash scripts/add_password.sh kladovshik ...)"
security find-generic-password -s smartup-xtrade -a "$(node -e "console.log(require('./config/roles.json').roles[0].login)")" >/dev/null 2>&1 || bash scripts/add_password.sh admin
echo "3) Login sinovi"
RESULTS_DIR="$DIR/../Tungi_natijalar/_setup_test" npx playwright test --project=setup && echo "   login OK"
echo "4) launchd — har kuni 04:00"
PL="$HOME/Library/LaunchAgents/uz.smartup.nightly.plist"
sed "s#__DIR__#$DIR#g; s#__HOME__#$HOME#g" launchd/uz.smartup.nightly.plist > "$PL"
launchctl bootout gui/$(id -u) "$PL" 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$PL"
launchctl list | grep uz.smartup.nightly && echo "   launchd OK"
echo "5) Mac 03:55 da o'zi uyg'onishi uchun (parol so'raydi):"
sudo pmset repeat wakeorpoweron MTWRFSU 03:55:00 && pmset -g sched
cat <<'TXT'

Qo'lda qiladigan 1 ta ish:
  Tizim sozlamalari → Maxfiylik va xavfsizlik → Diskka to'liq kirish (Full Disk Access) → «+»:
    /bin/bash   va   $(which node) natijasidagi fayl   (Cmd+Shift+G bilan yo'lni yozing)
  (launchd Desktop papkasiga yozishi uchun kerak.)
Hozir sinab ko'rish: launchctl kickstart -k gui/$(id -u)/uz.smartup.nightly
TXT
