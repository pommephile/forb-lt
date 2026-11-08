#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校正表の表を出力する。usage: table_build_cal.py <cal.json>
凍結文書（Forb-LT校正表_凍結_v8_2026-11-05.md）の後に実行する。
"""
import sys, json
sys.path.insert(0, ".")
import data_cal as D

cal = json.load(open(sys.argv[1], encoding="utf-8"))

# 上限は data_cal.CEIL_CAL から取る（compare.py と同じ表。判定に使う表は1つだけ置く）
T_SUP = {T: (D.CEIL_CAL[T], D.ORDER_B[D.CEIL_CAL[T]] if D.CEIL_CAL[T] < len(D.ORDER_B) else "尺度の外")
         for T in ["PA", "PRA", "IΣ_2", "IOpen"]}
ORDER_CAL = D.ORDER_CAL
N2 = [r for r in D.ROWS if r["id"] == "N2"][0]

def verdict(T):
    out = []
    for r in D.ROWS:
        lo, up = r["A"]
        if lo == "—":
            continue
        # A の下界 = 「その体系では証明できない」。したがって lo = T の行も T を超える
        if ORDER_CAL.index(lo) >= ORDER_CAL.index(T):
            blo = r["B"][0]
            if blo == "—":
                out.append((r["id"], "未確認（B の下界の出典が無い）"))
            else:
                ok = D.ORDER_B.index(blo) >= T_SUP[T][0]
                tag = "成り立つ" if ok else "成り立たない"
                if r["id"] == "N1":
                    tag += "（対照 N1。P-v7 の例外なので反例に数えない）"
                elif r["id"] == "N2":
                    tag += "（対照 N2。判定は「%s」なので、事前登録どおり P-v7 の反例に数える）" % N2["n2_verdict"]
                out.append((r["id"], "%s（B の下界 %s、T の上限 %s）" % (tag, blo, T_SUP[T][1])))
    return out

o = []
o.append("# Forb-LT 校正表 v8（2026-11-05）\n")
o.append("**82行の表とは別の表。** 凍結: `Forb-LT校正表_凍結_v8_2026-11-05.md`（同梱、sha256 `781ce338…`、記入はその後）")
o.append("**生成**: `table_build_cal.py`（値は `data_cal.py`）。v8 で C5・C6 の B と N2 の判定を記入した。\n")
o.append("---\n")
o.append("## 1. 校正表（10行。対照 N1・N2 を含む）\n")
o.append("| # | 命題 | Π₂ の形 | 軸A区間 | A 下界の論法 | A の出典 | 軸B（F_α） | 軸B（Grzegorczyk） | B の出典 |")
o.append("|---|---|---|---|---|---|---|---|---|")
for r in D.ROWS:
    o.append("| %s | %s | %s | [%s, %s] | %s | %s | [%s, %s] | %s/%s | %s |"
             % (r["id"], r["name"], r["prenex"], r["A"][0], r["A"][1], r["method"], r["src_a"],
                r["B"][0], r["B"][1], r["B"][2], r["B"][3], r["src_b"]))
o.append("")
o.append("---\n")
o.append("## 2. 照合（`compare.py --cal` の出力）\n")
o.append("| 項目 | 値 |")
o.append("|---|---|")
o.append("| (i) 定理による検査の違反 | **%d件** |" % len(cal["violations"]))
o.append("| 区間の不健全 | %d件 |" % len(cal["bad_intervals"]))
o.append("| 比較できる組 | %d（C=%d, D=%d） |" % (cal["comparable"], cal["C"], cal["D"]))
o.append("| うち自然な命題どうし | **%d** |" % (cal["pairs_natural"] if cal["pairs_natural"] is not None else -1))
o.append("| 比較不能 (a) A が重なる | %d |" % cal["incomparable_a"])
o.append("| 比較不能 (b) A が分離し B が重なる/未取得 | %d |" % cal["incomparable_b"])
o.append("| **D5 命題の数** | **%d** |" % cal["d5_statements"])
o.append("")
o.append("**判定の向き**: (i) は82行の表と同じく `>=`（B の下界が上限以上なら違反）。上限は `data_cal.CEIL_CAL` の1つの表を使う。\n")
o.append("### 2.1 比較できる組の一覧\n")
o.append("| 組（i, j） | 判定 |")
o.append("|---|---|")
for p in cal["pairs"]:
    if p["verdict"] in ("一致", "逆順"):
        o.append("| %s, %s | %s |" % (p["i"], p["j"], p["verdict"]))
o.append("")
o.append("比較不能 (b) の内訳（A が分離し B が重なる・未取得の組）:\n")
nb = [p for p in cal["pairs"] if p["verdict"].startswith("比較不能(b)")]
if nb:
    for p in nb:
        o.append("- %s と %s" % (p["i"], p["j"]))
else:
    o.append("- なし")
o.append("")
o.append("---\n")
o.append("## 3. 事前登録 P-v7 の判定（結果のみ。結論文は書かない）\n")
for T in ["PA", "PRA", "IΣ_2", "IOpen"]:
    o.append("**T = %s**（T で全域と証明できない最初の水準 = %s）\n" % (T, T_SUP[T][1]))
    o.append("| 行 | 判定 |")
    o.append("|---|---|")
    for rid, v in verdict(T):
        o.append("| %s | %s |" % (rid, v))
    o.append("")
o.append("---\n")
o.append("## 4. N2 の判定（T2）\n")
o.append("**判定: %s**\n" % N2["n2_verdict"])
o.append(N2["n2_src"] + "\n")
o.append("- 表の #2 の `Prime(p)` は既約元の形（p>1 ∧ p=yz → y=1 ∨ z=1）。文献の「prime」は環論的な素元で、両者は一般には一致しない。"
         "Kuhlmann らの論文は **既約元** について「Z の元だけ」と明記しており、#2 の形にそのまま当たる。\n")
o.append("---\n")
o.append("## 5. 外した候補と理由（凍結文書 §4 のとおり）\n")
o.append("| 候補 | 理由 |")
o.append("|---|---|")
o.append("| PH の次元固定列（Hájek–Pudlák 定理 II.1.9） | 一次資料の本文が未取得（v8 で取得したのは目次まで）。C5・C6 が同じ階段を Kirby–Paris の本文で与える |")
o.append("| Ackermann 関数の全域性 | 軸A の下界が無い（PA で証明できる） |")
o.append("| #31 van der Waerden、#32 Ramsey | 軸A の下界が文献に無い |")
o.append("| Szemerédi、Green–Tao | 同上 |")
print("\n".join(o))
