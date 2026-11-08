#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v1.7 の式の修正を確かめる（外部査読 2026-11-06 の 5 巡目）。
#77: 時間切れを含める（含めないと総当たり機械で証人不在＝偽）。
#62: 有限個の例外を ∀m ∃φ で吸収し、時間切れを含める。
"""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data

def main():
    fails = []
    t77 = data.H[77][1]; t62 = data.H[62][1]
    print("== #77 =="); print("  " + t77[:130])
    for tok in ("正しく判定しない", "時間切れを含める"):
        print("  「%s」: %s" % (tok, tok in t77))
        if tok not in t77: fails.append("#77 に「%s」が無い" % tok)
    if "時間切れは誤りに含めない" in t77:
        fails.append("#77 に旧記述（時間切れを除く）が残っている")
    print("== #62 =="); print("  " + t62[:140])
    for tok in ("∀m", "|φ|>m", "正しく判定しない", "2^{δn}"):
        print("  「%s」: %s" % (tok, tok in t62))
        if tok not in t62: fails.append("#62 に「%s」が無い" % tok)
    print("")
    print("判定: %s / %s" % (data.H[77][0], data.H[62][0]))
    if data.H[77][0] != "Π₂": fails.append("#77 の階層が Π₂ でない")
    if data.H[62][0] != "Σ₃": fails.append("#62 の階層が Σ₃ でない")
    print("")
    print("違反: %d 件" % len(fails))
    for f in fails: print("  -", f)
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
