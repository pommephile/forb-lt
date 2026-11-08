#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ダッシュボード（D1〜D11 と N2）。usage: dashboard.py <t.json> <cal.json>"""
import sys, os, json, re, collections
sys.path.insert(0, ".")
import data_cal as CAL
from data_sources import ITEMS
from data_d2 import ERRORS
from data_notes import NOTES
from data import H, A, B1

t8 = json.load(open(sys.argv[1], encoding="utf-8"))
cal = json.load(open(sys.argv[2], encoding="utf-8"))

# 82行の表の数字は t.json と data.py から再計算する（表の本文に依存しない）
hier = collections.Counter(v[0] for v in H.values())
d4x = sum(c for k, c in hier.items() if k not in ("未分類", "Π¹₂", "算術(階未定)"))
d1 = sum(1 for n, (lo, up, _s) in B1.items() if up != "—" or lo != "—")
d3 = sum(1 for n, (lo, up, _s) in A.items() if lo != "—" or (up not in ("ZFC", "—")))

# D8: 校正表の自然な命題で B が出典つきで入った行（上界か下界が入り、src_b が「未取得」でない）
d8_rows = [r["id"] for r in CAL.ROWS if r["natural"] and (r["B"][0] != "—" or r["B"][1] != "—") and not r["src_b"].startswith("未取得")]
# D9: 自然な命題どうしで比較できる組
d9 = cal["pairs_natural"]
# D10: 一次資料の未取得
d10_missing = [i["id"] for i in ITEMS if i["status"] != "取得"]
n2 = [r for r in CAL.ROWS if r["id"] == "N2"][0]

print("D1  軸B v1（出典つき）= %d" % d1)
print("D2  未修正の事実誤り（実行側の申告）= %d（監査の確認値ではない）" % len(ERRORS))
print("D3  ZFC より細かい境界 = %d" % d3)
print("D4確定 階が確定した行 = %d/82（Π¹₂ 21・階未定 0 を除く）" % d4x)
print("D5  命題の数（本文で確認）= %d %s" % (t8["d5_statements"], t8["d5_list"]))
print("D6  軸A と軸B の両方（82行）= %d" % t8["d6"])
print("D8  校正表の自然な命題で B が出典つき = %d %s" % (len(d8_rows), d8_rows))
print("D9  自然な命題どうしで比較できる組 = %d" % d9)
print("D10 一次資料の未取得 = %d / %d %s" % (len(d10_missing), len(ITEMS), d10_missing))
# D11: 注記の残り（表の本文から数える。md が渡されたときだけ）
if len(sys.argv) > 4:
    import re as _re
    R = _re.compile("要検算|要確認|未確認|未取得|要出典|標準的")
    cnt = 0
    seen = set()   # v9.1（監査）: 行番号で数える（§2 に同じ行の行があっても1回）
    for ln in open(sys.argv[3], encoding="utf-8").read().splitlines():
        m = _re.match(r"^\| *(\d+) \|", ln)
        if m and R.search(ln) and m.group(1) not in seen: seen.add(m.group(1)); cnt += 1
    inside = False
    for ln in open(sys.argv[4], encoding="utf-8").read().splitlines():
        if ln.startswith("## 1."): inside = True; continue
        if inside and ln.startswith("## "): break
        if inside and _re.match(r"^\| *(C|N)\d+ \|", ln) and R.search(ln): cnt += 1
    print("D11 注記の残り = %d（82行＋校正表）" % cnt)
    print("D11' 処置が書かれた行 = %d / %d（解消 %d・残存 %d）"
          % (len(NOTES), len(NOTES), sum(1 for r in NOTES if r["status"] == "解消"),
             sum(1 for r in NOTES if r["status"] == "残存")))
else:
    print("D11 注記の残り = （md を渡すと数える）")

if os.path.exists("formula_check.json"):
    _fc = json.load(open("formula_check.json", encoding="utf-8"))
    print("F   式の検査を記録した行 = %d/%d（自己試験 F' = %d 件）"
          % (_fc["f"], _fc["total"], _fc["fprime"]))
else:
    print("F   式の検査を記録した行 = （formula_check.json が無い）")
import lint_docs
print("L   文書と実際の食い違い = %d 件" % len(lint_docs.check()))
import values_check
_v, _sh = values_check.diffs()
print("V   値の不変（A・B・Grz の 1.0 との差）= %d 件（A %d・B %d・階層 %d・校正表 %d）"
      % (len(_v), _sh[0], _sh[1], _sh[2], _sh[3]))

print("N2  判定 = %s" % n2["n2_verdict"])
print("-- 参考: 校正表 (i) 違反 %d / 比較できる組 %d（C=%d, D=%d）" % (len(cal["violations"]), cal["comparable"], cal["C"], cal["D"]))
