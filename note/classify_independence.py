#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""独立性の2型（成長型 / 存在型）を、公開版のデータ（既定 1.2）で分類する。（監査側の修正 fix/analysis.1、fix/analysis.2 で既定の場所と題を直した）
usage: classify_independence.py [--selftest]

規則（本文の補題 4 による）:
  T = A の下限（証明できない体系）、c = CEIL[T]（T で全域と証明できない最初の水準の添字）
  - B の下界 >= c                     → 成長型（f_ℕ は T のどの可証全域関数でも抑えられない）
  - B の上界 <  c                     → 存在型（f_ℕ ≤ F_{上界}、これは T で可証全域）
  - それ以外（区間が c をまたぐ・B が空） → 判定不能
  - Π₁ の行 ∀x θ(x) は ∀x∃y (y=0 ∧ θ(x)) と読み、証人は定数 → A の下限があれば存在型
v1（実行側）からの変更:
  1. 存在型の判定に B の上界を使う（v1 は下界だけを見ていたので、区間が c をまたぐ行も存在型にしていた）
  2. Π₁ の行を母集団に入れる（v1 は Π₂ だけを見ていたので #3 が落ちていた）
  3. 母数（判定できた行の数）を出力する
  4. T が IΔ₀ を含まない行（IOpen）に「補題 1・4 の前提外」と書く
  5. --selftest: 変異 6 件。1 件でも期待と違えば exit 1
"""
import sys, os
sys.dont_write_bytecode = True
BASE = os.path.dirname(os.path.abspath(__file__))
REL = os.environ.get("FORB_REL", os.path.join(BASE, "..", "release", "v1.2"))
sys.path.insert(0, REL)
import data, data_cal

# 82 行の上限の表（release/v1.2/compare.py:32 と同じ値。compare.py は関数の中に置いていて import できない）
CEIL82 = {"IΔ₀": 2, "EFA": 3, "RCA₀": 4, "WKL₀": 4, "PRA": 4, "ACA₀": 5, "PA": 5}
WEAKER_THAN_IDELTA0 = {"IOpen"}
ARITH = {"Π₁", "Π₂"}

def classify(a_lo, b_lo, b_hi, cal, pi1=False):
    if a_lo == "—":
        return "判定不能", "A の下限が無い（独立が示されていない）"
    note = "；T⊉IΔ₀（補題1・4 の前提外）" if a_lo in WEAKER_THAN_IDELTA0 else ""
    if pi1:
        return "存在型", "Π₁：証人は定数（y=0）" + note
    O = data_cal.ORDER_B if cal else data.ORDER_B
    ceil = (data_cal.CEIL_CAL if cal else CEIL82).get(a_lo)
    if ceil is None:
        return "判定不能", "CEIL[%s] が尺度の外" % a_lo
    lo = O.index(b_lo) if b_lo != "—" else None
    hi = O.index(b_hi) if b_hi != "—" else None
    if lo is not None and lo >= ceil:
        return "成長型", "B_lo=%s(%d) ≥ CEIL[%s]=%d%s" % (b_lo, lo, a_lo, ceil, note)
    if hi is not None and hi < ceil:
        return "存在型", "B_hi=%s(%d) < CEIL[%s]=%d%s" % (b_hi, hi, a_lo, ceil, note)
    return "判定不能", "B=[%s,%s] が CEIL[%s]=%d をまたぐか空%s" % (b_lo, b_hi, a_lo, ceil, note)

def rows():
    out = []
    for n in sorted(data.H):
        h = data.H[n][0]
        if h not in ARITH:
            continue
        A = data.A.get(n); B = data.B1.get(n)
        if h == "Π₁":
            if not A or A[0] == "—":
                continue           # 独立の主張が無い Π₁ 行は母集団の外（数だけ数える）
            k, why = classify(A[0], "F_0", "F_0", False, pi1=True)
            out.append(("82", "#%d" % n, data.H[n][1][:26], A[0], A[1], "F_0〜F_0（定数）", k, why))
        else:
            if not A or not B:
                continue
            k, why = classify(A[0], B[0], B[1], False)
            out.append(("82", "#%d" % n, data.H[n][1][:26], A[0], A[1], B[0] + "〜" + B[1], k, why))
    for r in data_cal.ROWS:
        k, why = classify(r["A"][0], r["B"][0], r["B"][1], True)
        out.append(("cal", r["id"], r["name"][:26], r["A"][0], r["A"][1], r["B"][0] + "〜" + r["B"][1], k, why))
    return out

def selftest():
    cases = [  # (説明, 引数, 期待)
        ("N1 の B を [F_0,F_ε₀] に（区間が CEIL をまたぐ）", ("PA", "F_0", "F_ε₀", True), "判定不能"),
        ("N2 の B を [F_1,F_3] に（同上）", ("IOpen", "F_1", "F_3", True), "判定不能"),
        ("C1 の B を [F_0,F_ε₀] に", ("PA", "F_0", "F_ε₀", True), "判定不能"),
        ("C4 の B を [F_0,F_3] に（上界 < CEIL[PRA]=4）", ("PRA", "F_0", "F_3", True), "存在型"),
        ("#75 の A 下限を — に", ("—", "F_ε₀", "F_ε₀", False), "判定不能"),
    ]
    bad = 0
    for d, a, exp in cases:
        got = classify(*a)[0]
        ok = got == exp
        bad += not ok
        print("%s %s → %s（期待 %s）" % ("OK " if ok else "NG ", d, got, exp))
    # #3 が母集団に入り存在型になること
    r3 = [r for r in rows() if r[1] == "#3"]
    ok = len(r3) == 1 and r3[0][6] == "存在型"
    bad += not ok
    print("%s #3（Π₁, IOpen）が存在型として数えられる" % ("OK " if ok else "NG "))
    print("selftest: NG %d 件" % bad)
    return 1 if bad else 0

def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    R = rows()
    print("# 独立性の2型の分類（Forb-LT %s のデータから機械生成、fix/analysis.2）\n" % os.path.basename(os.path.normpath(REL)).lstrip("v"))
    for tag, title in [("82", "## 82 行の表（算術の Π₁・Π₂ で、A の主張がある行）"), ("cal", "## 校正表（10 行）")]:
        print(title + "\n\n| 行 | 命題 | A 下限 | A 上限 | B | 型 | 判定の根拠 |\n|---|---|---|---|---|---|---|")
        for r in R:
            if r[0] == tag:
                print("| %s |" % " | ".join(r[1:]))
        print("")
    n_p1 = sum(1 for n in data.H if data.H[n][0] == "Π₁"); n_p2 = sum(1 for n in data.H if data.H[n][0] == "Π₂")
    print("母数: 82 行のうち Π₁ %d 行・Π₂ %d 行。分類の対象（Π₂ で A・B がある行＋Π₁ で A 下限がある行）は %d 行、校正表 %d 行"
          % (n_p1, n_p2, sum(1 for r in R if r[0] == "82"), len(data_cal.ROWS)))
    for k in ["成長型", "存在型", "判定不能"]:
        ks = [r[1] for r in R if r[6] == k]
        print("%s %d 行: %s" % (k, len(ks), ", ".join(ks)))
    print("82 行の表のうち存在型: %d 行（%s）" % (sum(1 for r in R if r[0] == "82" and r[6] == "存在型"),
          ", ".join(r[1] for r in R if r[0] == "82" and r[6] == "存在型")))

if __name__ == "__main__":
    main()
