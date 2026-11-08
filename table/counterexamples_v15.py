#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v1.5 の式の修正を確かめる（外部査読 2026-11-06 の 3 巡目）。
#20: 次数 i ごとの |α|=q^{i/2}。#49: 素分解。#21-23: 非重複（距離 ≥2）。#22-23: 最適値を値に。
"""
import sys, os, re
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data

def main():
    fails = []
    checks = [("#20", (20,), ["H^i_ét", "q^{i/2}", "∀i", "∀α"]),
              ("#49", (49,), ["素分解", "JSJ", "M₁#…#M_n"]),
              ("#21", (21,), ["距離 ≥ 2", "π/√18"]),
              ("#22", (22,), ["距離 ≥ 2", "π⁴/384"]),
              ("#23", (23,), ["距離 ≥ 2", "π¹²/12!"])]
    for name, ids, toks in checks:
        txt = data.H[ids[0]][1]
        print("== %s ==" % name); print("  " + txt[:150])
        for t in toks:
            ok = t in txt
            print("  「%s」: %s" % (t, ok))
            if not ok:
                fails.append("%s に「%s」が無い" % (name, t))
    for name, n in (("#22", 22), ("#23", 23)):
        body = data.H[n][1].split("（", 1)[0]   # 注記の「『最適値』を置き換えた」は除く
        if "最適値" in body:
            fails.append("%s に「最適値」が残っている" % name)
    if "w は整数" in data.H[20][1]:
        fails.append("#20 に旧形（w は整数）が残っている")
    print("")
    print("違反: %d 件" % len(fails))
    for f in fails: print("  -", f)
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
