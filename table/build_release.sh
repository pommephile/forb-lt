#!/bin/bash
# Forb-LT 一覧表 v1.8 — 生成から検査までの一括実行。
# パッケージを一時ディレクトリに複製し、そこで作り直して、SHA256SUMS と一致することを示す。
set -euo pipefail
ORIG="$(cd "$(dirname "$0")" && pwd)"
cd "$ORIG"
W="$(mktemp -d)"
cp -R . "$W/pkg"
cd "$W/pkg"

echo "== 1. 生成（比較 → 表 → 校正表） =="
python3 -I compare.py 'Forb-LT難易度一覧表_v4.1_2026-10-28.md' t_built.json
python3 -I compare.py x cal_built.json --cal
python3 -I formula_smoke.py --write --selftest > formula_check_log.txt
python3 -I table_build.py 'Forb-LT難易度一覧表_v4.1_2026-10-28.md' t_built.json cal_built.json 'Forb-LT校正表.md' > 'Forb-LT一覧表.md'
python3 -I table_build_cal.py cal_built.json > 'Forb-LT校正表.md'

echo "== 2. 生成物の一致（クリーンな複製で同じものが出るか） =="
cmp t_built.json t.json && echo "t.json: 一致" || { echo "t.json: 不一致（停止）"; exit 1; }
cmp cal_built.json cal.json && echo "cal.json: 一致" || { echo "cal.json: 不一致（停止）"; exit 1; }
echo "（表の md は手順 8 のハッシュで照合する）"

echo "== 2b. 値の不変（V: A・B・Grz の欄を 1.0 と比べる） =="
if ! python3 -I values_check.py t_built.json cal_built.json; then
  echo "V: 値が変わった（停止）"; exit 1
fi

echo "== 3. 検査 =="
python3 -I check.py 'Forb-LT一覧表.md' t_built.json

echo "== 4. 自己試験（82行3件・校正表2件） =="
python3 -I compare.py 'Forb-LT難易度一覧表_v4.1_2026-10-28.md' /dev/null --selftest | sed -n '1,8p'
python3 -I compare.py x /dev/null --cal --selftest | sed -n '1,4p'

echo "== 4b. 注記の自己試験（notes 1件） =="
python3 -I notes.py 'Forb-LT一覧表.md' 'Forb-LT校正表.md' --selftest | tail -1

echo "== 4c. 式の自明性（formula_smoke 1件） =="
python3 -I formula_smoke.py --selftest

echo "== 4d. 式の検査（F・F'） =="
python3 -I formula_smoke.py --selftest | grep -E "^(F 式|違反|F' 自己試験)"

echo "== 4e. L（文書と実際の食い違い） =="
python3 -I lint_docs.py

echo "== 5. T4 の文言照合 =="
python3 -I verify_wording.py 'Forb-LT_指示書_v8_2026-11-05.md' 'Forb-LT一覧表.md'

echo "== 6. 注記の残り（D11） =="
python3 -I notes.py 'Forb-LT一覧表.md' 'Forb-LT校正表.md' | tail -4

echo "== 7. ダッシュボード =="
python3 -I dashboard.py t_built.json cal_built.json 'Forb-LT一覧表.md' 'Forb-LT校正表.md'

echo "== 8. ファイル一覧とハッシュ =="
if ! python3 -I "$ORIG/filelist_check.py" "$ORIG"; then
  echo "ファイル一覧: 余計なファイルか欠落がある（停止）"; exit 1
fi
shasum -a 256 -c SHA256SUMS
