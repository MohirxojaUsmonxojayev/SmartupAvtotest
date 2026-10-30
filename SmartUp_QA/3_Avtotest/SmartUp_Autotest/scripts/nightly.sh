#!/bin/bash
# Tungi yugurish: launchd har kuni 04:00 da ishga tushiradi (launchd/uz.smartup.nightly.plist).
# Natija: ../Tungi_natijalar/<YYYY-MM-DD>/ (SmartUp_QA/3_Avtotest/Tungi_natijalar) — ertalab Claude shu papkani tahlil qiladi.
set -u
cd "$(dirname "$0")/.."
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.nvm/versions/node/$(ls $HOME/.nvm/versions/node 2>/dev/null | tail -1)/bin:$PATH"
DATE=$(TZ=Asia/Tashkent date +%F)
export RESULTS_DIR="$(cd .. && pwd)/Tungi_natijalar/$DATE"
export SIM_RUN=$(TZ=Asia/Tashkent date +%y%m%d)
mkdir -p "$RESULTS_DIR"
LOG="$RESULTS_DIR/run.log"
{
  echo "START $(date '+%F %T')  node=$(node -v 2>/dev/null)  run=$SIM_RUN"
  # Mac uxlab qolmasligi uchun yugurish davomida
  caffeinate -dimsu -w $$ &
  # Tartib qat'iy: 1) login  2) SMOKE (health)  3) REGRESSION  4) rollar matritsasi  5) biznes-simulyatsiya.
  # Har bosqich alohida ishga tushadi (--no-deps): smoke'da bug chiqsa ham regression baribir yuradi.
  CODE=0
  for PH in setup health regression access sim; do
    [ -n "${ONLY_PHASES:-}" ] && [[ " $ONLY_PHASES " != *" $PH "* ]] && continue
    echo "== PHASE $PH $(date '+%T')"
    PHASE=$PH npx playwright test --project=$PH --no-deps; RC=$?
    echo "== PHASE $PH exit=$RC $(date '+%T')"
    [ $RC -ne 0 ] && CODE=$RC
    if [ "$PH" = setup ] && ! grep -q '"ok": true' "$RESULTS_DIR/auth.json" 2>/dev/null; then echo "login bo'lmadi — to'xtatildi"; break; fi
  done
  echo "END $(date '+%F %T')  exit=$CODE"
  echo "{\"finished\":\"$(date -u +%FT%TZ)\",\"exit\":$CODE,\"run\":\"$SIM_RUN\"}" > "$RESULTS_DIR/DONE.json"
} >> "$LOG" 2>&1
