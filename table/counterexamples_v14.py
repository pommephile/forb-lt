#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v1.4 の式の修正を、反例と条件の存在で確かめる（外部査読 2026-11-06 の 2 巡目）。
usage: counterexamples_v14.py
- #44: AP⊆A が無いと、A={1}⊆[3] でも AP={1,2,3} を証人にできてしまう（A の中に AP が無いのに真）。
- #10: 実行不能な入力を許すと「∀入力∃解」は偽（x≤0 ∧ x≥1）。
- #65: 結論が「X は非特異」だと、入力の性質を結論にしている（X=Spec ℚ[x,y]/(y²−x³) は特異）。
- #17 / #47 / #72 / #46 / #73 / cal:C2 / cal:C6: 条件が式に入っているかを文字列で確認。
"""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data, data_cal

ROWS = {r["id"]: r for r in data_cal.ROWS}

def aps(n, k, d=1):
    """[n] の k 項等差数列（公差 d）の全体。"""
    return [tuple(range(a, a + d * k, d)) for a in range(1, n - d * (k - 1) + 1)]

def main():
    fails = []
    print("== #44: AP⊆A が無い旧形の自明化 ==")
    n = k = 3; delta = 1/3
    A = {1}
    in_a = [ap for ap in aps(n, k) if set(ap) <= A]
    in_n = aps(n, k)
    print("  N=k=3, δ=1/3, A=%s: |A|=%d ≥ δN=%d" % (sorted(A), len(A), int(delta * n)))
    print("  [3] の公差 1 の 3 項 AP: %s（A に含まれるもの: %s）" % (in_n, in_a))
    print("  → 旧形（AP⊆A が無い）は A=%s で真。A の中に AP が無いのに真なので、Szemerédi の内容になっていない" % sorted(A))
    if in_a:
        fails.append("#44 の例で A に含まれる AP が出てしまう")
    new44 = data.H[44][1]
    print("  新形:", new44[:120])
    if "AP⊆A" not in new44:
        fails.append("#44 に AP⊆A が無い")

    print("== #10: 実行不能入力 ==")
    new10 = data.H[10][1]
    print("  新形:", new10[:110])
    for tok in ("実行不能", "非有界", "最適解"):
        if tok not in new10:
            fails.append("#10 に「%s」が無い" % tok)

    print("== #65: 非特異は Y の性質 ==")
    new65 = data.H[65][1]
    print("  新形:", new65[:120])
    if "列の終端 Y は非特異" not in new65:
        fails.append("#65 が Y の非特異性を書いていない")
    # 「旧形は『X は非特異』」という注記は残してよい。式本体だけを見る。
    body65 = new65.split("（旧形")[0]
    if "X は非特異" in body65:
        fails.append("#65 の式本体に「X は非特異」が残っている")

    print("== 条件の存在 ==")
    checks = [("#17", data.H[17][1], ["共形的", "定数"]),
              ("#47", data.H[47][1], ["Ric", "[ω′]=[ω]", "c₁"]),
              ("#72", data.H[72][1], ["ゲージ群", "Yang–Mills"]),
              ("#46", data.H[46][1], ["d≥1", "1≤i≤n"]),
              ("#73", data.H[73][1], ["射影多様体", "regular", "smooth"])]
    for name, txt, toks in checks:
        for t in toks:
            ok = t in txt
            print("  %s 「%s」: %s" % (name, t, ok))
            if not ok:
                fails.append("%s に「%s」が無い" % (name, t))

    print("== 校正表 C2 / C6 ==")
    c2 = ROWS["C2"]["prenex"]; c2a = ROWS["C2"]["src_a"]; c6a = ROWS["C6"]["src_a"]
    print("  C2 prenex に card(H)=min(H):", "card(H)=min(H)" in c2)
    if "card(H)=min(H)" in c2:
        fails.append("C2 の prenex に旧記述が残っている")
    if "≥ min(H)" not in c2:
        fails.append("C2 の prenex が ≥ 形でない")
    if "OCR" in c2a:
        fails.append("C2 の src_a が OCR のまま")
    print("  C6 src_a に「類推（未検証）」:", "類推（未検証）" in c6a)
    if "類推（未検証）" not in c6a:
        fails.append("C6 に未検証の注記が無い")

    print("")
    print("違反: %d 件" % len(fails))
    for f in fails:
        print("  -", f)
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
