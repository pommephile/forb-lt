#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v1.6 の式の修正を確かめる（外部査読 2026-11-06 の 4 巡目）。
#20: 滑らかな射影多様体への制限（反例 X=G_m を注記に記載）。
#21: 半径 1（距離 >=2 に対応）。#23: 24 次元の出典。/#62: 3-CNF と n の定義。
#77: n^c + c と「時間切れを含めない」。#82: q>=1。#49: 向き付け可能。
"""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data

def main():
    fails = []
    checks = [("#20", 20, ["滑らかな射影", "X̄", "G_m", "q^{i/2}"]),
              ("#21", 21, ["半径 1", "距離 ≥ 2"]),
              ("#23", 23, ["Cohn–Kumar"]),
              ("#62", 62, ["3-CNF", "変数の個数"]),
              ("#77", 77, ["|x|^c + c", "時間切れ"]),
              ("#82", 82, ["q≥1"]),
              ("#49", 49, ["向き付け可能", "素分解"])]
    for name, n, toks in checks:
        txt = data.H[n][1]
        print("== %s ==" % name); print("  " + txt[:130])
        for t in toks:
            ok = t in txt
            print("  「%s」: %s" % (t, ok))
            if not ok: fails.append("%s に「%s」が無い" % (name, t))
    if "半径 1/2" in data.H[21][1]:
        fails.append("#21 に「半径 1/2」（誤った対応）が残っている")
    if "∀p,q Σ₁" in data.H[82][1]:
        fails.append("#82 に旧形（∀p,q）が残っている")
    print(""); print("違反: %d 件" % len(fails))
    for f in fails: print("  -", f)
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
