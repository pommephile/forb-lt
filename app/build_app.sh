#!/bin/bash
# 命題データベース.app を作り直す（表の版を上げたらこれを走らせる）
#   bash app/build_app.sh            → ~/Applications/Forb-LT.app を上書き
#   bash app/build_app.sh 1.9        → 版表記を変える
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REL="$HERE/../release/v1.8"
APP="$HOME/Applications/Forb-LT.app"
VER="${1:-1.8}"

echo "[1/4] 表 → data.json"
python3 -I -B "$HERE/make_data.py" "$REL" "$HERE/data.json"

echo "[2/4] data.json → index.html"
python3 -I -B "$HERE/embed_data.py" "$HERE/index.html"

echo "[3/4] .app を組み立て"
rm -rf "$APP"; mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$HERE/Info.plist" "$APP/Contents/Info.plist"
/usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString $VER" "$APP/Contents/Info.plist"
/usr/libexec/PlistBuddy -c "Set :CFBundleVersion $VER" "$APP/Contents/Info.plist"
cp "$HERE/index.html" "$HERE/data.json" "$APP/Contents/Resources/"
if [ -d "$HERE/AppIcon.iconset" ]; then
  iconutil -c icns "$HERE/AppIcon.iconset" -o "$APP/Contents/Resources/AppIcon.icns"
fi

echo "[4/4] コンパイル"
swiftc -O -framework AppKit -framework WebKit -o "$APP/Contents/MacOS/ForbLT" "$HERE/ForbLT.swift"
codesign --force --deep --sign - "$APP" >/dev/null 2>&1 || true
echo "できた: $APP"
echo "起動: open -a \"$APP\""
