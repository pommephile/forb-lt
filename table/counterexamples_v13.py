#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v1.3 の式の修正を、反例で確かめる（外部査読 2026-11-06 の 3 行）。
usage: counterexamples_v13.py
- #11 旧形は p=q=3 で偽（左辺 0・右辺 −1）。新形は p≠q を条件に持つ。
- #18 旧形は定数写像で自明。新形は「ホモトピック」と曲率の条件を持つ。
- #73 旧形は体を量化しており Spec K で空列。新形は「射影多様体」を量化する。
- PH の引用が ≥ になっている（旧版は OCR で = と読んでいた）。
"""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data
from data_formula_v11 import QUOTES

def legendre(a, p):
    """平方剰余記号（p は奇素数）。"""
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1

def check_11():
    old_holds_at_p_eq_q = []
    for p in (3, 5, 7):
        lhs = legendre(p, p) * legendre(p, p)
        rhs = (-1) ** ((p - 1) * (p - 1) // 4)
        old_holds_at_p_eq_q.append((p, lhs, rhs, lhs == rhs))
    return old_holds_at_p_eq_q

def main():
    fails = []
    print("== #11: p=q での反例（旧形は p≠q が無い） ==")
    for p, lhs, rhs, ok in check_11():
        print("  p=q=%d: (p/q)(q/p)=%d, (-1)^((p-1)(q-1)/4)=%d → 旧形 %s" % (p, lhs, rhs, "成り立つ" if ok else "偽（反例）"))
        if ok:
            fails.append("#11 の反例が出ない（p=q=%d）" % p)
    new11 = data.H[11][1]
    print("  新形:", new11)
    if "p≠q" not in new11:
        fails.append("#11 に p≠q が無い")

    print("== #18: 定数写像での自明化 ==")
    new18 = data.H[18][1]
    print("  新形:", new18)
    for tok in ("ホモトピック", "断面曲率", "∃h"):
        if tok not in new18:
            fails.append("#18 に「%s」が無い" % tok)

    print("== #73: 体を量化すると空列で済む ==")
    new73 = data.H[73][1]
    print("  新形:", new73)
    if "射影多様体" not in new73:
        fails.append("#73 が多様体を量化していない")
    if "有限生成の体" in new73.split("（")[0]:
        fails.append("#73 の式本体が「体」を量化している")

    print("== PH の引用 ==")
    q1, q2 = QUOTES["82:76"], QUOTES["cal:C2"]
    for name, q in (("82:76", q1), ("cal:C2", q2)):
        # 82:76 は定義の文を、cal:C2 は同じ定義を引く §1.1 の第 2 文を引く。
        has_ge = ("card(H) ≥ min(H)" in q) or ("relatively large" in q and "card(H)=min(H)" not in q)
        print("  %s: ≥ を含む = %s" % (name, has_ge))
        if not has_ge:
            fails.append("%s の引用が ≥ でない" % name)

    print("")
    print("違反: %d 件" % len(fails))
    for f in fails:
        print("  -", f)
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
