#!/bin/bash
# Rol parolini macOS Keychain'ga saqlash (parol ekranda ko'rinmaydi, faylga yozilmaydi).
# Ishlatish: bash scripts/add_password.sh admin      (rollar: config/roles.json)
set -e
cd "$(dirname "$0")/.."
ROLE="${1:?rol nomini bering: admin | kladovshik | buxgalter | agent}"
LOGIN=$(node -e "const c=require('./config/roles.json');const r=c.roles.find(x=>x.role==='$ROLE');if(!r){process.exit(2)};console.log(r.login)") || { echo "Rol topilmadi: $ROLE"; exit 1; }
SERVICE=$(node -e "console.log(require('./config/roles.json').keychainService)")
echo "Rol: $ROLE   Login: $LOGIN   (Keychain service: $SERVICE)"
read -r -s -p "SmartUp paroli: " PW; echo
security add-generic-password -U -s "$SERVICE" -a "$LOGIN" -w "$PW" -T /usr/bin/security
unset PW
echo "Saqlandi. Tekshirish: security find-generic-password -s $SERVICE -a $LOGIN >/dev/null && echo bor"
