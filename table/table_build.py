#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一覧表を生成する。usage: table_build.py <v4.1.md> <t.json> [cal.json] [校正表名]
表・分布・集計はすべてここから出す。
"""
import sys, re, json, os, collections
sys.path.insert(0, ".")
from data import H, A, B1, ORDER_A, ORDER_B, GRZ_ROW, SYSTEM_NOTE, JUST, T1_CONFIRMED, T2_A_SEARCH

MD, T5 = sys.argv[1], sys.argv[2]
CAL_JSON = sys.argv[3] if len(sys.argv) > 3 else None
CAL_NAME = sys.argv[4] if len(sys.argv) > 4 else "Forb-LT校正表.md"
t5 = json.load(open(T5, encoding="utf-8"))

names, old_level, ps_old, b_v0, status = {}, {}, {}, {}, {}
in_tbl = False
for ln in open(MD, encoding="utf-8").read().splitlines():
    if ln.startswith("## 2."):
        in_tbl = True; continue
    if in_tbl and ln.startswith("## "):
        break
    if not in_tbl or not re.match(r"^\|\s*\d+\s*\|", ln):
        continue
    c = [x.strip() for x in re.split(r"(?<!\\)\|", ln.strip()[1:-1])]
    if len(c) == 13:
        n = int(c[0])
        names[n] = c[1]; old_level[n] = c[3]; ps_old[n] = c[4]; b_v0[n] = c[8]; status[n] = c[11]

def a_cell(n):
    if n not in A:
        return ("未記入", "—")
    lo, up, src = A[n]
    return ("[%s, %s]" % (lo, up), src)

def b_cell(n):
    if n not in B1:
        return ("—", "—", "Π₂ でない（対象外）")
    lo, up, src = B1[n]
    grz = "%s/%s" % GRZ_ROW.get(n, ("—", "—"))
    return ("[%s, %s]" % (lo, up), grz, src)

hier = collections.Counter(v[0] for v in H.values())
d4 = sum(c for k, c in hier.items() if k != "未分類")
d4x = sum(c for k, c in hier.items() if k not in ("未分類", "Π¹₂", "算術(階未定)"))
d1 = sum(1 for n, (lo, up, _s) in B1.items() if up != "—" or lo != "—")
d3 = sum(1 for n, (lo, up, _s) in A.items() if lo != "—" or (up not in ("ZFC", "—")))
pi1 = sorted(n for n, (hh, _) in H.items() if hh == "Π₁")
pi2 = sorted(n for n, (hh, _) in H.items() if hh == "Π₂")

out = []
out.append("# Forb-LT 一覧表 — 命題ごとの証明論的強さ・算術の階層・証人の増え方（出典つき）\n")
out.append("この表は、82 の命題について既知の結果を整理したものである。列は3つある。軸A は、その命題を証明できる体系と証明できない体系を、文献にある区間で書いたもの。階層は、命題の冠頭形を式で書き、算術の階層に置いたもの。軸B は、Π₂ の命題について、証人の増え方を F_α の区間で書いたもの。値はすべて出典つきで、出典の無い欄は空欄にしてある。\n")
out.append("この表は予測を主張しない。軸A と軸B の関係について定理として言えるのは次のことだけである: 体系 T が Π₂ 文 φ を証明するなら、φ の証人は T で全域と証明できる関数で抑えられる。表の検査 (i) はこれを確かめている。逆は成り立たない（付録の対照 N1）。\n")
out.append("**版**: 1.8（公開版。1.0〜1.7 は公開しない。理由は README） / **日付**: 2026-11-06 / **生成**: `table_build.py`（表・分布・集計は生成器の出力）")
out.append("**入力**: v6.1 を元に、v9・v9.1・v9.2 で出典の文と式を書き換えた（#6・#7・#34・#40・#70 は `data_base.py`、#29 は `data_v61.py`。値は不変）＋ v7 の T1・T2 ＋ 監査側の修正 v7.1・v9.1・v9.2（#36・#49・#60・#61・#65・#73・#20・#40・#70）")
out.append("**軸B**: `LT計測手順_v1.2.md`（Π₂ のみ）。尺度は F_α と Grzegorczyk を別の列に書く。\n")
out.append("---\n")
out.append("## 1. 一覧表（82行）\n")
out.append("| # | 問題 | 旧層 | 階層 | 冠頭形 | Π₁の扱い | 軸A区間 | A出典 | B_v0 | B_v1 (F_α) | B_v1 (Grz) | B v1 参照文献 | 状態 |")
out.append("|---|------|------|------|--------|----------|---------|-------|------|------------|------------|---------------|------|")
for n in sorted(H):
    ac, asrc = a_cell(n)
    bc, grz, bsrc = b_cell(n)
    pi1c = "記述的（予測対象外）" if H[n][0] == "Π₁" else "—"
    row = [str(n), names.get(n, ""), old_level.get(n, ""), H[n][0], H[n][1], pi1c, ac, asrc,
           b_v0.get(n, "—"), bc, grz, bsrc, status.get(n, "")]
    out.append("| " + " | ".join(x.replace("|", "\\|") for x in row) + " |")
out.append("")
out.append("---\n")
out.append("## 2. 分布と集計\n")
out.append("### 2.1 階層（D4）\n")
out.append("| 階層 | 行数 |")
out.append("|---|---|")
for k in ["Π₁", "Σ₁", "Π₂", "Σ₂", "Π₃", "Σ₃", "Π₄", "算術(階未定)", "Π¹₁", "Π¹₂", "実閉体", "算術外", "未分類"]:
    out.append("| %s | %d |" % (k, hier.get(k, 0)))
out.append("| **計** | **%d** |" % sum(hier.values()))
out.append("")
out.append("**D4（未分類を除く）= %d/82**\n" % d4)
out.append("**D4確定（Π¹₂ の概略と階未定を除く）= %d/82**（目標 ≥60。T1 で %d 行を確定、#36 は監査 v7.1 で Π₂）\n"
           % (d4x, len(T1_CONFIRMED)))
out.append("> 二階（Π¹₂）の冠頭形は**概略**である。一階の算術文への翻訳ではない（指示書 T1 の扱い）。\n")
out.append("### 2.2 軸B v1（D1）\n")
out.append("| 項目 | 値 |")
out.append("|---|---|")
out.append("| Π₂ の行 | %d |" % len(pi2))
out.append("| うち B v1 を記入 | **%d** |" % d1)
out.append("| 空欄（証人の上界の出典が無い） | %d |" % (len(pi2) - d1))
out.append("")
out.append("**D1 = %d/82**（目標 ≥12。#65 を T2 で追加）\n" % d1)
out.append("### 2.3 軸A（D3）\n")
out.append("| 項目 | 値 |")
out.append("|---|---|")
out.append("| A を記入 | %d |" % len(A))
out.append("| うち ZFC より細かい境界 | **%d** |" % d3)
out.append("")
out.append("**D3 = %d/82**（報告のみ）\n" % d3)
out.append("### 2.4 T5 照合と D5・D6\n")
out.append("| 項目 | 値 |")
out.append("|---|---|")
out.append("| (i) 定理による検査の違反 | **%d件** |" % len(t5["violations"]))
out.append("| 軸A 区間の不健全（下界 > 上界） | %d件 |" % len(t5["bad_intervals"]))
out.append("| (ii) 対象行 | %d |" % len(t5["rows"]))
out.append("| 比較できる組 | %d（C=%d, D=%d） |" % (t5["comparable"], t5["C"], t5["D"]))
out.append("| 比較不能 (a) A が重なる | %d |" % t5["incomparable_a"])
out.append("| 比較不能 (b) A が分離し B が重なる/未取得 | %d |" % t5["incomparable_b"])
out.append("| **D5 命題の数（本文で確認したもの）** | **%d** |" % t5["d5_statements"])
out.append("| **D6 軸A と軸B v1 の両方がある行** | **%d** |" % t5["d6"])
out.append("")
out.append("D5 の理由: " + t5["d5_note"] + "\n")
out.append("比較不能 (b) の内訳（予測の未確認に当たる組）:\n")
nb = [p for p in t5["pairs"] if p["verdict"].startswith("比較不能(b)")]
if nb:
    for p in nb:
        out.append("- #%s と #%s" % (p["i"], p["j"]))
else:
    out.append("- なし")
out.append("")
out.append("### 2.5 Π₁ の行と二階・一階の対応\n")
out.append("Π₁ の行は **%d行**（#%s）。いずれも `Π₁の扱い` 列が「記述的（予測対象外）」で、B v1 を持たない。\n"
           % (len(pi1), ", #".join(map(str, pi1))))
out.append("| 二階の体系 | 一階部分 | 備考 |")
out.append("|---|---|---|")
for a, b, c in SYSTEM_NOTE:
    out.append("| %s | %s | %s |" % (a, b, c))
out.append("")
out.append("### 2.6 階未定だった9行（T1）\n")
out.append("| # | 命題 | 階 | 冠頭形 | 閉じた文か | 量化の範囲を抑えるもの |")
out.append("|---|---|---|---|---|---|")
for n in T1_CONFIRMED + [36]:
    cn, bound, hh = JUST[n]
    out.append("| %d | %s | %s | %s | %s | %s |" % (n, names.get(n, ""), H[n][0], H[n][1], cn, bound))
out.append("")
out.append("### 2.7 T2 の軸A 上界の探索（Avigad 2003）\n")
out.append("| # | 結果 |")
out.append("|---|---|")
for n in sorted(T2_A_SEARCH):
    out.append("| %d | %s |" % (n, T2_A_SEARCH[n]))
out.append("")
out.append("---\n")
out.append("## 3. 検証記録\n")
out.append("| 項目 | 値 |")
out.append("|---|---|")
out.append("| データ | `data.py`（`data_v61.py` を import し、T1・T2 の上書きだけを行う。v6.1 からの差は出典の文と式だけで、値は不変） |")
out.append("| 生成器 | `table_build.py` / 照合: `compare.py` → `t.json` / 検査: `check.py` |")
out.append("| 行数 | %d |" % len(H))
out.append("| 自己試験 | 3件（#75 上界・#45 区間逆転・B 欄の尺度外の値） |")
out.append("")
out.append("---\n")
out.append("## 付録 — 校正表と P-v7 の観察\n")
import data_cal as CALD
cal = json.load(open(CAL_JSON, encoding="utf-8")) if CAL_JSON else None
out.append("付録の校正表は、独立性が文献で知られている命題を、値を記入する前に凍結した規則で選び、軸A と軸B を並べたものである。"
           "事前登録した観察 P-v7 は「自然な命題では、T で証明できない命題の証人は、T で全域と証明できる関数より速く増える」である。"
           "比較の結果は［下の表（`compare.py --cal` の出力）］のとおりである。\n")
if cal:
    out.append("| 組（i, j） | 判定 |")
    out.append("|---|---|")
    for q in cal["pairs"]:
        if q["verdict"] in ("一致", "逆順"):
            out.append("| %s, %s | %s |" % (q["i"], q["j"], q["verdict"]))
    out.append("")
    out.append("比較できる組は %d（C=%d, D=%d）、うち**自然な命題どうしは %d 組**。比較不能は %d（(a) A が重なる %d / (b) A が分離し B が重なる・未取得 %d）。\n"
               % (cal["comparable"], cal["C"], cal["D"], cal["pairs_natural"], cal["incomparable"], cal["incomparable_a"], cal["incomparable_b"]))
n2 = [r for r in CALD.ROWS if r["id"] == "N2"][0]
out.append("この観察は定理ではない。対照 N1 は、証人が定数でも PA で証明できない Π₂ 文がある例である。"
           "また、校正表の独立性の証明のほとんどは証人の増え方そのものを使っている。"
           "増え方を使わない証明が本文で確認できたのは Paris–Harrington（C2）だけである。"
           "したがって、一致は独立な証拠としては弱い。弱い体系の例として、対照 N2（IOpen と素数の無限性）の判定は"
           "［" + n2["n2_verdict"] + "、根拠: Biljakovic–Kochetov–Kuhlmann「Primes and Irreducibles in Truncation Integer Parts of Real Closed Fields」§0 p.2（本文）／Berarducci–Otero 1996 の Abstract（本文）］である。"
           + ("事前登録どおり、これは P-v7 の反例に数える（T = IOpen。#2 は IOpen で証明できないが、証人は線形）。" if n2["n2_verdict"] == "成り立つ" else "")
           + "\n")
out.append("校正表そのものは `%s`（82行の表とは別ファイル）。\n" % CAL_NAME)
out.append("")
out.append("---\n")
out.append("## 付録2 — 式の検査（F、全 92 行）\n")
out.append("82 行と校正表 10 行のすべてについて、(a) 自明な証人（0・1・空・公差 0・総当たり）/"
           "(b) 命題より弱い形への潰れ / (c) 原典との一致 を記録した。"
           "式の文字列は `formula_smoke.py --write` が出力したものをそのまま載せる。\n")
if os.path.exists("formula_check.json"):
    fc = json.load(open("formula_check.json", encoding="utf-8"))
    out.append("F = %d/%d（(a) の根拠: 計算 %d・文字列 %d・概略 %d）。自己試験 F' = %d 件（条件を外すと検出）。\n"
               % (fc["f"], fc["total"], fc["kinds"].get("計算", 0), fc["kinds"].get("文字列", 0),
                  fc["kinds"].get("概略", 0), fc["fprime"]))
    out.append("| 行 | 階層 | (a) 計算 | (a) 範囲条件（文字列） | (b) 弱い主張への潰れ | (c) 原典 | 判定 |")
    out.append("|---|---|---|---|---|---|---|")
    for r in fc["rows"]:
        a_calc = r["a"] if r.get("a_kind") != "文字列" else "—"
        a_str = r["a"] if r.get("a_kind") == "文字列" else "—"
        out.append("| %s | %s | %s | %s | %s | %s | %s |"
                   % (r["key"], r.get("hier", ""), a_calc, a_str, r["b"], r["c"], r["verdict"]))
    out.append("")
else:
    out.append("（式の検査の表は入っていない。`formula_smoke.py --write` を先に実行する。）\n")
print("\n".join(out))
sys.stderr.write("emit: rows=%d d1=%d d3=%d d4=%d d4x=%d D=%d d5s=%d d6=%d pi1=%d inc_a=%d inc_b=%d\n"
                 % (len(H), d1, d3, d4, d4x, t5["D"], t5["d5_statements"], t5["d6"], len(pi1),
                    t5["incomparable_a"], t5["incomparable_b"]))
