#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校正表 v7 の情報源（凍結文書 Forb-LT校正表_凍結_v7_2026-11-05.md の後に記入）。
凍結した選定規則と事前登録は変えない。ここに書くのは A・B・論法・出典だけである。
"""
# 監査 v7.1: "PA+TI(ω^ω)" を除いた（PA は ω^ω までの TI を証明するので PA と同じで、PA より上に置くのは誤り）。
#            "PA+1-Con(PA)" を加えた（PH の上界。PA+Con(PA) では PH は証明できない）。
ORDER_CAL = ["IOpen", "IΔ₀", "EFA", "PRA", "IΣ_2", "IΣ_3", "PA",
             "PA+Con(PA)", "PA+1-Con(PA)", "PA+TI(ε₀)", "ATR₀", "Π¹₁-CA₀", "ZFC"]
# 監査 v7.1: IΣ_2・IΣ_3 の上限を表せるよう尺度に F_{ω^ω}・F_{ω^ω^ω} を加えた（Löb–Wainer: IΣ_n の全域関数は F_α, α<ω_n）。
ORDER_B = ["F_0", "F_1", "F_2", "F_3", "F_ω", "F_ω^ω", "F_ω^ω^ω", "F_ε₀"]
# T で全域と証明できる関数の上限 = 「T で全域と証明できない最初の水準」の ORDER_B での添字（82行の 98 の CEIL と同じ意味）。
# 判定は B の下界の添字 >= CEIL で違反。len(ORDER_B)=8 は「尺度の中に上限が無い」。
# PA+Con(PA) は PA と同じ全域関数を持つ（真な Π₁ 文を足しても全域関数は増えない）。
CEIL_CAL = {"IOpen": 2, "IΔ₀": 2, "EFA": 3, "PRA": 4, "IΣ_2": 5, "IΣ_3": 6, "PA": 7,
            "PA+Con(PA)": 7, "PA+1-Con(PA)": 8, "PA+TI(ε₀)": 8, "ATR₀": 8, "Π¹₁-CA₀": 8, "ZFC": 8}

def a_lo_rank(s): return -10**6 if s == "—" else ORDER_CAL.index(s) + 1
def a_up_rank(s): return 10**6 if s == "—" else ORDER_CAL.index(s)
def b_lo_rank(s): return -10**6 if s == "—" else ORDER_B.index(s)
def b_up_rank(s): return 10**6 if s == "—" else ORDER_B.index(s)

# 列: id, name, prenex, A=(下界,上界), src_a, method（A下界の論法）, confirmed（本文で確認したか）,
#     B=(下界,上界,F_α,Gr), src_b, natural（自然な命題か）
ROWS = [
 dict(id="C1", name="Goodstein の定理（全 m）",
      prenex="∀n ∃k (Goodstein 列 (n, base 2) は k で 0)",
      A=("PA", "PA+TI(ε₀)"),
      src_a="下界: Kirby–Paris 1982, Thm 1(ii)（本文で確認）。上界: 同論文の注（本文）: h-Goodstein 列の停止は TI(ε₀) と同値で、固定 base はその特別の場合",
      method="増え方を使う", confirmed=True,
      B=("F_ε₀", "F_ε₀", "非PR", "非PR"),
      src_b="Cichoń 1983（本文で確認）: 停止までの長さ = H_α(x+1)−1（Hardy 階層）。H_ε₀ は PA で全域と証明できない",
      natural=True),
 dict(id="C2", name="Paris–Harrington の定理",
      prenex="∀k,m,n≥1 ∃N ∀c:[N]^k→m ∃H⊆[N] (H は c で同次 ∧ |H| ≥ n ∧ |H| ≥ min H)（PH 1977 §1.1 の定義は card(H) ≥ min(H)。式は原典と同じ形）",
      A=("PA", "PA+1-Con(PA)"),
      src_a="下界: Paris–Harrington 1977, §2（原典 PDF p.1134 で確認）: Con(T)→Con(PA) と 1.2→Con(T)。上界: PA+1-Con(PA)（監査 v7.1 で訂正。PH は PA 上で 1-Con(PA) と同値。PA+Con(PA) は PA と同じ全域関数しか持たないので PH を証明しない）",
      method="使わない", confirmed=True,
      B=("F_ε₀", "F_ε₀", "非PR", "非PR"),
      src_b="Paris–Harrington 1977, Thm 3.2（本文）: f(e) は PA で全域と証明できる任意の g を支配する。Ketonen–Solovay 1981 が同種の分類を与える",
      natural=True),
 dict(id="C3", name="Kirby–Paris の hydra",
      prenex="∀H ∃k (KP の戦略 τ での H との battle が k で終わる)（τ は KP 1982 が Theorem 2(ii) の証明で作る再帰的戦略：「we shall produce a recursive strategy τ」「in P we cannot prove that τ is a winning strategy」。B はこの τ での battle の長さ。「every recursive strategy」の形は φ_e の全域性を仮定に置くので Π₃ で、Π₂ の行には書かない。v1.0 は H の量化が無く、v1.1 は ∀σ（再帰的戦略）で Π₂ でなかった）",
      A=("PA", "PA+TI(ε₀)"),
      src_a="下界: Kirby–Paris 1982, Thm 2(ii)（本文で確認）。上界: 同 Thm 2(i) の ordinal 割当（TI(ε₀)）",
      method="増え方を使う", confirmed=True,
      B=("F_ε₀", "F_ε₀", "非PR", "非PR"),
      src_b="Kirby–Paris 1982, Remark（p.293、本文）: 「the function giving the lengths of battles for hydras of height 2 with strategy τ is not provably total in IΣ₁ and hence is not primitive recursive」。高さ k+1 では IΣ_k。（旧版が引いた Prop 8 は Goodstein 列の停止時刻の命題で、hydra の battle 長ではない）",
      natural=True),
 dict(id="C4", name="弱い Goodstein（Process 1、通常の基数表示）",
      prenex="∀N ∀x ∃k (Process 1 が k で 0)",
      A=("PRA", "PA"),
      src_a="下界: Cichoń 1983, Thm 1（本文で確認）: PRA では証明できない。上界: PA（監査 v7.1 で訂正。停止は TI(ω^ω) から出て、PA は ε₀ 未満の TI を証明する）。v8: IΣ_2 まで下げる出典は見つからなかった（IΣ_2 の全域関数の水準と TI(ω^ω) の関係を示す文献を特定できず）",
      method="増え方を使う", confirmed=True,
      B=("F_ω", "F_ω", "非PR", "非PR"),
      src_b="Cichoń 1983（本文）: Process 1 の順序数は ω^ω 未満で、H_{ω^ω} は Ackermann の一版（PRA で全域と証明できない）。H_{ω^α} = F_α なので F_ω（監査 v8.1 で出典の文を本文どおりに直した。値は変わらない）",
      natural=True),
 dict(id="C5", name="Goodstein（塔に制限: m < n^{n^n}、KP Thm 1' の k=2）",
      prenex="∀n>1 ∀m < n^{n^n} ∃k (Goodstein 列 (m, base n) は k で 0)（n が3回の塔）",
      A=("IΣ_2", "IΣ_3"),
      src_a="Kirby–Paris 1982, Thm 1'（本文で確認）: (ii) IΣ_k は n が k+1 回の塔の場合を証明しない、(i) IΣ_k は n が k 回の塔（の上に p）の場合を証明する。"
            "n が3回の塔なので、k=2 で下界、k=3（p=1）で上界（監査 v8.1: v7・v8 の「塔の高さ2」と m<n↑↑↑2・m<n^n は、この A と別の命題だった）",
      method="増え方を使う", confirmed=True,
      B=("F_ω^ω", "F_ω^ω", "非PR", "非PR"),
      src_b="Cichoń 1983 の等式 長さ = H_{o_n(m)}(n+1) − 1（本文）。m < n^{n^n} なら o_n(m) < ω^{ω^ω} で上界 H_{ω^{ω^ω}} = F_{ω^ω}。"
            "m = n^{n^{n−1}} では o_n(m) = ω^{ω^{n−1}} で長さ = F_{ω^{n−1}}(n+1) − 1 なので、証人関数は F_{ω^ω} の水準に達する（等式なので下界も出る）。"
            "H_{ω^α} = F_α を使う（Cichoń: H_{ω^ω} は Ackermann。監査 v8.1 で v8 の [—, F_ω^ω]（m<n^n の値）から訂正）",
      natural=True),
 dict(id="C6", name="hydra（高さ 3 に固定）",
      prenex="∀H（高さ 3 の hydra）∃k (KP の戦略 τ での battle が k で終わる)（KP 1982 の Remark: 高さ k+1 の hydra では IΣ_k で証明できない。k=2 の行。「the function giving the lengths of battles for hydras of height 2 with strategy τ is not provably total in IΣ₁」と同じく τ で書く。v1.0 は戦略の指定が無く、v1.1 は ∀σ（再帰的戦略）で Π₂ でなかった）",
      A=("IΣ_2", "IΣ_3"),
      src_a="下界: Kirby–Paris 1982, Thm 2 の後の注（本文の末尾）: 高さ k+1 の hydra では IΣ_k で証明できない。k=2 の行。"
            "上界 IΣ_3: 本文に記述なし（IΣ_n が ω_{n+1} 未満の TI を証明するという標準的事実から。要出典）。注: KP が τ を明記するのは高さ 2 の battle 長についてなので、高さ 3 への移し替えは類推（未検証）",
      method="増え方を使う", confirmed=True,
      B=("—", "F_ω^ω", "—", "非PR"),
      src_b="Kirby–Paris 1982 の ordinal 割当で、高さ3の hydra の ordinal は ω^{ω^ω} 未満。battle の長さ ≤ H_{ω^{ω^ω}}(n) = F_{ω^ω}(n)。上界のみ"
            "（監査 v8.1 で v8 の F_ω^ω^ω から訂正: H_{ω^α} = F_α。KP 本文「高さ2 の battle の長さは原始再帰でない」= H_{ω^ω} = F_ω と整合）",
      natural=True),
 dict(id="C7", name="グラフマイナー定理の有限形",
      prenex="∀k ∃N（有限形は ∀k∃N の形。正確な形は本文未取得）",
      A=("Π¹₁-CA₀", "ZFC"),
      src_a="Friedman–Robertson–Seymour 1987（文献はあるが本文未取得）: Π¹₁-CA₀ では証明できない",
      method="未確認", confirmed=False,
      B=("—", "—", "—", "—"),
      src_b="未取得（証人の増え方の上界の出典が無い）",
      natural=True),
 dict(id="C8", name="Kruskal の定理の有限形",
      prenex="∀c ∃n ∀T₁…T_n（各 T_i は頂点数 ≤ i+c の有限木 → ∃i<j で T_i は T_j に inf を保って埋め込める）（Friedman, FOM 289, 2006 の FFF の形。v9.1 までの「頂点 ≤k」の形は同型類が有限個なので鳩の巣で自明に成り立ち、ATR₀ の下界は当てはまらなかった）",
      A=("ATR₀", "ZFC"),
      src_a="FOM 289 の下界は個別の FFF(5)・FFF(6) の証明の長さ（A(10) 記号）の話で、∀c の文の ATR₀ 下界ではない。投稿には FFF(6) を FFF(5) と書いた添字の誤記がある。∀c の ATR₀ 下界は Simpson 1985（未取得）に拠る",
      method="未確認", confirmed=False,
      B=("—", "—", "—", "—"),
      src_b="未取得（同上）",
      natural=True),
 dict(id="N1", name="∀x∃y (y=0 ∧ ¬Prf_PA(x,⌜⊥⌝))",
      prenex="∀x ∃y (y=0 ∧ ¬Prf_PA(x,⌜⊥⌝))",
      A=("PA", "PA+Con(PA)"),
      src_a="PA では証明できない（第二不完全性定理）。PA+Con(PA) では証明できる。論法は増え方と無関係",
      method="使わない", confirmed=True,
      B=("F_0", "F_0", "E¹", "E¹"),
      src_b="証人は定数 y=0。対照（自然な命題ではない）",
      natural=False),
 dict(id="N2", name="#2（素数無限）と IOpen",
      prenex="∀n ∃p>n Prime(p)",
      A=("IOpen", "EFA"),
      src_a="下界: Shepherdson のモデルでは、Z に入る既約元は Z の元だけ（Biljakovic–Kochetov–Kuhlmann, 「Primes and Irreducibles in Truncation Integer Parts of Real Closed Fields」§0 p.2、本文で確認）。Berarducci–Otero 1996 本文も同じモデルを扱う。上界: Paris–Wilkie–Woods 1988",
      method="使わない", confirmed=True,
      B=("F_0", "F_1", "E¹", "E¹"),
      src_b="証人は n+1 以上（線形）。Bertrand で n<p≤2n。対照（#2 の Prime は既約元の形）",
      natural=False,
      n2_verdict="成り立つ",
      n2_src="Biljakovic–Kochetov–Kuhlmann §0 p.2: 「Shepherdson ... constructed an IP of this field in which the only irreducible elements are those in Z」（本文）。Berarducci–Otero 1996 の Abstract: 「His model is not normal and does not have any infinite prime elements」（本文）"),
]

D5_NOTE = ("判定: 「j の軸A 下界に、増え方の下界を使わない公刊の証明があり、それを本文で確認したか」。"
           "校正表では C2（Paris–Harrington）だけが該当する。C1・C3・C4 は Hardy 階層／indicator を使うため数えない。"
           "N1 は対照（自然な命題でない）、N2 も対照（自然な命題でない）なので数えない。N2 の判定は本文で確認済み。")
