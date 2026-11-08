#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""式の検査（F: 全 92 行）の台帳。
- REQ: 式に必ず含まれる条件（文字列）。外すと自己試験で検出される（F'）。
- QUOTES: 原典の文を 1 句引ける行（(c) の根拠）。
- NOTE: (a)(b)(c) の個別の注記（規則で書けない行だけ）。
"""

# (a)(b) を計算で確かめる行の個別注記 / (c) の引用
REQ = {
    "82:27": ["d≥1"],
    "82:31": ["d≥1"],
    "82:42": ["種数 ≥2"],
    "82:43": ["d≥1"],
    "82:44": ["d≥1"],
    "82:58": ["a+b=c", "gcd(a,b)=1"],
    "82:59": ["|x|^c"],
    "82:67": ["r 元", "指数 n"],
    "82:70": ["Prime(p)", "Prime(q)"],
    "82:71": ["n≥1"],
    "82:78": ["σ(n)", "H_n"],
    "82:79": ["Fefferman (A)", "f=0"],
    "82:81": ["1≤x,y,z≤2n⁴"],
    "cal:C3": ["∀H", "戦略 τ"],
    "cal:C6": ["高さ 3", "戦略 τ"],
    "cal:C8": ["i+c"],
    "82:76": ["|H| ≥ min H", "|H| ≥ n", "同次"],
    "cal:C2": ["|H| ≥ min H", "|H| ≥ n", "同次"],
}

QUOTES = {
    "82:6": "Buss, Handbook of Proof Theory ch. II, p.90: 「In particular, it proves that if x is prime and x|ab then x|a or x|b.」",
    "82:7": "Buss, ch. II, p.90: 「The sequence coding tools developed below will enable I∆0 to prove the unique factorization theorem」",
    "82:29": "Mahler 1953, Remarks 2（p.41）: 「|π−w| > exp{−γν(1+ν log ν + log a) log(2 + ν log ν + log a)}」（Fel'dman 1951 の式を引く）",
    "82:34": "Smith, Gödel Without (Too Many) Tears, ch.16 Theorem 59: 「No consistent p.r. axiomatized theory T which contains Q can define truth for its own language.」",
    "cal:C1": "Kirby–Paris 1982, p.288（Thm 1 の証明の後）: h-Goodstein 列の停止は TI(ε₀) と同値",
    "cal:C3": "Kirby–Paris 1982, Theorem 2(ii) の証明: 「For (ii) we shall produce a recursive strategy τ」「in P we cannot prove that τ is a winning strategy」",
    "cal:C5": "Kirby–Paris 1982, Theorem 1': 「(i) For each fixed p∈N, IΣ_k ⊢ ∀m,n>1 (if m < n↑↑↑p [where n occurs k times] then the Goodstein sequence for m starting at n eventually hits zero)」「(ii) IΣ_k ⊬ ∀m,n>1 (if m < n↑↑↑ [where n occurs k+1 times] then the Goodstein sequence for m starting at n eventually hits zero)」",
    "cal:C6": "Kirby–Paris 1982, Remark（Thm 2 の後）: 「if we restrict ourselves in Theorem 2 to hydras of height k+1 (i.e. no node is more than k+1 segments away from the root) then we cannot prove that “every recursive strategy is a winning strategy” using just IΣ_k.」",
    "82:76": "Paris–Harrington 1977, §1.1 Definition と 1.2 Theorem（原典 PDF p.1134）: 「We call a finite set H of natural numbers relatively large if card(H) ≥ min(H).」／「For all natural numbers e,r and k there is an M such that M → (k)^e_r」（同次で relatively large な H の存在）",
    "cal:C2": "Paris–Harrington 1977, §1.1 Definition と 1.2 Theorem（原典 PDF p.1134）: 「for every partition P:[M]^e → r there is a relatively large H⊆M which is homogeneous for P and of cardinality at least k」",
    "cal:C8": "Friedman, FOM 289（2006）: 「FFF. For all c >= 0 there exists n so large that the following holds. For all trees T1,...,Tn with each |Ti| <= i+c, there exists 1 <= i < j <= n such that Ti is inf preserving embeddable into Tj.」",
}

# 原典の本文が未取得の行（(c) は「未取得」と書く）
D10_ROWS = {"82:24", "82:45", "cal:C7"}

# 規則で書けない行の個別注記
NOTE = {
    "82:13": ("(a) n≥2 でないと n! の評価が自明（0! = 1）", "(b) 下界を深さで書いており、比較の主張は弱めていない"),
    "82:20": ("(a) q は素数冪（q=0 は体でない）", "(b) 概略でない（Z の零点・極の絶対値の形）"),
    "82:46": ("(a) ∀x∈{±1}^N の後は有界（旧形は自明に真だった）", "(b) discrepancy の定義を式に含む"),
    "82:81": ("(a) 1≤x,y,z≤2n⁴ で 0 を排除（n=5 で旧上界 n の反例あり）", "(b) 等式 4xyz = n(xy+yz+zx) をそのまま書く"),
    "82:79": ("(a) f=0・滑らか・有限エネルギーを式に含む（「大域解 or 爆発」は恒真）", "(b) Fefferman (A) の形"),
    "cal:C3": ("(a) ∀H と戦略 τ を書く（どちらかが無いと battle が定義できない）", "(b) τ を固定した Π₂ 形（∀σ 再帰的は Π₃）"),
    "cal:C6": ("(a) 高さ 3 と戦略 τ を書く", "(b) τ を固定した Π₂ 形（∀σ 再帰的は Π₃）"),
}
