#!/bin/bash
# Papka ko'chirilgandan keyin tungi 04:00 launchd vazifasini yangi yo'l bilan qayta o'rnatadi.
set -e
cd "$(dirname "$0")/.."
DIR="$(pwd)"
PL="$HOME/Library/LaunchAgents/uz.smartup.nightly.plist"
sed "s#__DIR__#$DIR#g; s#__HOME__#$HOME#g" launchd/uz.smartup.nightly.plist > "$PL"
launchctl bootout gui/$(id -u) "$PL" 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$PL"
launchctl list | grep uz.smartup.nightly && echo "launchd OK: $DIR/scripts/nightly.sh"
