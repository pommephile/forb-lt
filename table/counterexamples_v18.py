#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v1.8 の修正を確かめる（外部査読 2026-11-06 の 6 巡目）。
#62: 入力の正規化規約（変数名 1..n、重複節・パディングを除く）が式に入っているか。
"""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data

def main():
    t = data.H[62][1]; fails = []
    print("== #62 =="); print("  " + t[:170])
    for tok in ("正規化", "変数名は 1..n", "重複", "パディング", "∀m", "|φ|>m", "正しく判定しない"):
        ok = tok in t
        print("  「%s」: %s" % (tok, ok))
        if not ok: fails.append("#62 に「%s」が無い" % tok)
    if data.H[62][0] != "Σ₃": fails.append("#62 の階層が Σ₃ でない")
    print(""); print("違反: %d 件" % len(fails))
    for f in fails: print("  -", f)
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
