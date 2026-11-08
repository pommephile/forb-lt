# Forb-LT 校正表 v8（2026-11-05）

**82行の表とは別の表。** 凍結: `Forb-LT校正表_凍結_v8_2026-11-05.md`（同梱、sha256 `781ce338…`、記入はその後）
**生成**: `table_build_cal.py`（値は `data_cal.py`）。v8 で C5・C6 の B と N2 の判定を記入した。

---

## 1. 校正表（10行。対照 N1・N2 を含む）

| # | 命題 | Π₂ の形 | 軸A区間 | A 下界の論法 | A の出典 | 軸B（F_α） | 軸B（Grzegorczyk） | B の出典 |
|---|---|---|---|---|---|---|---|---|
| C1 | Goodstein の定理（全 m） | ∀n ∃k (Goodstein 列 (n, base 2) は k で 0) | [PA, PA+TI(ε₀)] | 増え方を使う | 下界: Kirby–Paris 1982, Thm 1(ii)（本文で確認）。上界: 同論文の注（本文）: h-Goodstein 列の停止は TI(ε₀) と同値で、固定 base はその特別の場合 | [F_ε₀, F_ε₀] | 非PR/非PR | Cichoń 1983（本文で確認）: 停止までの長さ = H_α(x+1)−1（Hardy 階層）。H_ε₀ は PA で全域と証明できない |
| C2 | Paris–Harrington の定理 | ∀k,m,n≥1 ∃N ∀c:[N]^k→m ∃H⊆[N] (H は c で同次 ∧ |H| ≥ n ∧ |H| ≥ min H)（PH 1977 §1.1 の定義は card(H) ≥ min(H)。式は原典と同じ形） | [PA, PA+1-Con(PA)] | 使わない | 下界: Paris–Harrington 1977, §2（原典 PDF p.1134 で確認）: Con(T)→Con(PA) と 1.2→Con(T)。上界: PA+1-Con(PA)（監査 v7.1 で訂正。PH は PA 上で 1-Con(PA) と同値。PA+Con(PA) は PA と同じ全域関数しか持たないので PH を証明しない） | [F_ε₀, F_ε₀] | 非PR/非PR | Paris–Harrington 1977, Thm 3.2（本文）: f(e) は PA で全域と証明できる任意の g を支配する。Ketonen–Solovay 1981 が同種の分類を与える |
| C3 | Kirby–Paris の hydra | ∀H ∃k (KP の戦略 τ での H との battle が k で終わる)（τ は KP 1982 が Theorem 2(ii) の証明で作る再帰的戦略：「we shall produce a recursive strategy τ」「in P we cannot prove that τ is a winning strategy」。B はこの τ での battle の長さ。「every recursive strategy」の形は φ_e の全域性を仮定に置くので Π₃ で、Π₂ の行には書かない。v1.0 は H の量化が無く、v1.1 は ∀σ（再帰的戦略）で Π₂ でなかった） | [PA, PA+TI(ε₀)] | 増え方を使う | 下界: Kirby–Paris 1982, Thm 2(ii)（本文で確認）。上界: 同 Thm 2(i) の ordinal 割当（TI(ε₀)） | [F_ε₀, F_ε₀] | 非PR/非PR | Kirby–Paris 1982, Remark（p.293、本文）: 「the function giving the lengths of battles for hydras of height 2 with strategy τ is not provably total in IΣ₁ and hence is not primitive recursive」。高さ k+1 では IΣ_k。（旧版が引いた Prop 8 は Goodstein 列の停止時刻の命題で、hydra の battle 長ではない） |
| C4 | 弱い Goodstein（Process 1、通常の基数表示） | ∀N ∀x ∃k (Process 1 が k で 0) | [PRA, PA] | 増え方を使う | 下界: Cichoń 1983, Thm 1（本文で確認）: PRA では証明できない。上界: PA（監査 v7.1 で訂正。停止は TI(ω^ω) から出て、PA は ε₀ 未満の TI を証明する）。v8: IΣ_2 まで下げる出典は見つからなかった（IΣ_2 の全域関数の水準と TI(ω^ω) の関係を示す文献を特定できず） | [F_ω, F_ω] | 非PR/非PR | Cichoń 1983（本文）: Process 1 の順序数は ω^ω 未満で、H_{ω^ω} は Ackermann の一版（PRA で全域と証明できない）。H_{ω^α} = F_α なので F_ω（監査 v8.1 で出典の文を本文どおりに直した。値は変わらない） |
| C5 | Goodstein（塔に制限: m < n^{n^n}、KP Thm 1' の k=2） | ∀n>1 ∀m < n^{n^n} ∃k (Goodstein 列 (m, base n) は k で 0)（n が3回の塔） | [IΣ_2, IΣ_3] | 増え方を使う | Kirby–Paris 1982, Thm 1'（本文で確認）: (ii) IΣ_k は n が k+1 回の塔の場合を証明しない、(i) IΣ_k は n が k 回の塔（の上に p）の場合を証明する。n が3回の塔なので、k=2 で下界、k=3（p=1）で上界（監査 v8.1: v7・v8 の「塔の高さ2」と m<n↑↑↑2・m<n^n は、この A と別の命題だった） | [F_ω^ω, F_ω^ω] | 非PR/非PR | Cichoń 1983 の等式 長さ = H_{o_n(m)}(n+1) − 1（本文）。m < n^{n^n} なら o_n(m) < ω^{ω^ω} で上界 H_{ω^{ω^ω}} = F_{ω^ω}。m = n^{n^{n−1}} では o_n(m) = ω^{ω^{n−1}} で長さ = F_{ω^{n−1}}(n+1) − 1 なので、証人関数は F_{ω^ω} の水準に達する（等式なので下界も出る）。H_{ω^α} = F_α を使う（Cichoń: H_{ω^ω} は Ackermann。監査 v8.1 で v8 の [—, F_ω^ω]（m<n^n の値）から訂正） |
| C6 | hydra（高さ 3 に固定） | ∀H（高さ 3 の hydra）∃k (KP の戦略 τ での battle が k で終わる)（KP 1982 の Remark: 高さ k+1 の hydra では IΣ_k で証明できない。k=2 の行。「the function giving the lengths of battles for hydras of height 2 with strategy τ is not provably total in IΣ₁」と同じく τ で書く。v1.0 は戦略の指定が無く、v1.1 は ∀σ（再帰的戦略）で Π₂ でなかった） | [IΣ_2, IΣ_3] | 増え方を使う | 下界: Kirby–Paris 1982, Thm 2 の後の注（本文の末尾）: 高さ k+1 の hydra では IΣ_k で証明できない。k=2 の行。上界 IΣ_3: 本文に記述なし（IΣ_n が ω_{n+1} 未満の TI を証明するという標準的事実から。要出典）。注: KP が τ を明記するのは高さ 2 の battle 長についてなので、高さ 3 への移し替えは類推（未検証） | [—, F_ω^ω] | —/非PR | Kirby–Paris 1982 の ordinal 割当で、高さ3の hydra の ordinal は ω^{ω^ω} 未満。battle の長さ ≤ H_{ω^{ω^ω}}(n) = F_{ω^ω}(n)。上界のみ（監査 v8.1 で v8 の F_ω^ω^ω から訂正: H_{ω^α} = F_α。KP 本文「高さ2 の battle の長さは原始再帰でない」= H_{ω^ω} = F_ω と整合） |
| C7 | グラフマイナー定理の有限形 | ∀k ∃N（有限形は ∀k∃N の形。正確な形は本文未取得） | [Π¹₁-CA₀, ZFC] | 未確認 | Friedman–Robertson–Seymour 1987（文献はあるが本文未取得）: Π¹₁-CA₀ では証明できない | [—, —] | —/— | 未取得（証人の増え方の上界の出典が無い） |
| C8 | Kruskal の定理の有限形 | ∀c ∃n ∀T₁…T_n（各 T_i は頂点数 ≤ i+c の有限木 → ∃i<j で T_i は T_j に inf を保って埋め込める）（Friedman, FOM 289, 2006 の FFF の形。v9.1 までの「頂点 ≤k」の形は同型類が有限個なので鳩の巣で自明に成り立ち、ATR₀ の下界は当てはまらなかった） | [ATR₀, ZFC] | 未確認 | FOM 289 の下界は個別の FFF(5)・FFF(6) の証明の長さ（A(10) 記号）の話で、∀c の文の ATR₀ 下界ではない。投稿には FFF(6) を FFF(5) と書いた添字の誤記がある。∀c の ATR₀ 下界は Simpson 1985（未取得）に拠る | [—, —] | —/— | 未取得（同上） |
| N1 | ∀x∃y (y=0 ∧ ¬Prf_PA(x,⌜⊥⌝)) | ∀x ∃y (y=0 ∧ ¬Prf_PA(x,⌜⊥⌝)) | [PA, PA+Con(PA)] | 使わない | PA では証明できない（第二不完全性定理）。PA+Con(PA) では証明できる。論法は増え方と無関係 | [F_0, F_0] | E¹/E¹ | 証人は定数 y=0。対照（自然な命題ではない） |
| N2 | #2（素数無限）と IOpen | ∀n ∃p>n Prime(p) | [IOpen, EFA] | 使わない | 下界: Shepherdson のモデルでは、Z に入る既約元は Z の元だけ（Biljakovic–Kochetov–Kuhlmann, 「Primes and Irreducibles in Truncation Integer Parts of Real Closed Fields」§0 p.2、本文で確認）。Berarducci–Otero 1996 本文も同じモデルを扱う。上界: Paris–Wilkie–Woods 1988 | [F_0, F_1] | E¹/E¹ | 証人は n+1 以上（線形）。Bertrand で n<p≤2n。対照（#2 の Prime は既約元の形） |

---

## 2. 照合（`compare.py --cal` の出力）

| 項目 | 値 |
|---|---|
| (i) 定理による検査の違反 | **0件** |
| 区間の不健全 | 0件 |
| 比較できる組 | 16（C=14, D=2） |
| うち自然な命題どうし | **9** |
| 比較不能 (a) A が重なる | 10 |
| 比較不能 (b) A が分離し B が重なる/未取得 | 19 |
| **D5 命題の数** | **1** |

**判定の向き**: (i) は82行の表と同じく `>=`（B の下界が上限以上なら違反）。上限は `data_cal.CEIL_CAL` の1つの表を使う。

### 2.1 比較できる組の一覧

| 組（i, j） | 判定 |
|---|---|
| C4, C1 | 一致 |
| C5, C1 | 一致 |
| C6, C1 | 一致 |
| N2, C1 | 一致 |
| C4, C2 | 一致 |
| C5, C2 | 一致 |
| C6, C2 | 一致 |
| N2, C2 | 一致 |
| C4, C3 | 一致 |
| C5, C3 | 一致 |
| C6, C3 | 一致 |
| N2, C3 | 一致 |
| C4, N1 | 逆順 |
| N2, C4 | 一致 |
| C5, N1 | 逆順 |
| N2, C5 | 一致 |

比較不能 (b) の内訳（A が分離し B が重なる・未取得の組）:

- C1 と C7
- C1 と C8
- C2 と C7
- C2 と C8
- C3 と C7
- C3 と C8
- C4 と C7
- C4 と C8
- C5 と C7
- C5 と C8
- C6 と C7
- C6 と C8
- C6 と N1
- N2 と C6
- N1 と C7
- N2 と C7
- N1 と C8
- N2 と C8
- N2 と N1

---

## 3. 事前登録 P-v7 の判定（結果のみ。結論文は書かない）

**T = PA**（T で全域と証明できない最初の水準 = F_ε₀）

| 行 | 判定 |
|---|---|
| C1 | 成り立つ（B の下界 F_ε₀、T の上限 F_ε₀） |
| C2 | 成り立つ（B の下界 F_ε₀、T の上限 F_ε₀） |
| C3 | 成り立つ（B の下界 F_ε₀、T の上限 F_ε₀） |
| C7 | 未確認（B の下界の出典が無い） |
| C8 | 未確認（B の下界の出典が無い） |
| N1 | 成り立たない（対照 N1。P-v7 の例外なので反例に数えない）（B の下界 F_0、T の上限 F_ε₀） |

**T = PRA**（T で全域と証明できない最初の水準 = F_ω）

| 行 | 判定 |
|---|---|
| C1 | 成り立つ（B の下界 F_ε₀、T の上限 F_ω） |
| C2 | 成り立つ（B の下界 F_ε₀、T の上限 F_ω） |
| C3 | 成り立つ（B の下界 F_ε₀、T の上限 F_ω） |
| C4 | 成り立つ（B の下界 F_ω、T の上限 F_ω） |
| C5 | 成り立つ（B の下界 F_ω^ω、T の上限 F_ω） |
| C6 | 未確認（B の下界の出典が無い） |
| C7 | 未確認（B の下界の出典が無い） |
| C8 | 未確認（B の下界の出典が無い） |
| N1 | 成り立たない（対照 N1。P-v7 の例外なので反例に数えない）（B の下界 F_0、T の上限 F_ω） |

**T = IΣ_2**（T で全域と証明できない最初の水準 = F_ω^ω）

| 行 | 判定 |
|---|---|
| C1 | 成り立つ（B の下界 F_ε₀、T の上限 F_ω^ω） |
| C2 | 成り立つ（B の下界 F_ε₀、T の上限 F_ω^ω） |
| C3 | 成り立つ（B の下界 F_ε₀、T の上限 F_ω^ω） |
| C5 | 成り立つ（B の下界 F_ω^ω、T の上限 F_ω^ω） |
| C6 | 未確認（B の下界の出典が無い） |
| C7 | 未確認（B の下界の出典が無い） |
| C8 | 未確認（B の下界の出典が無い） |
| N1 | 成り立たない（対照 N1。P-v7 の例外なので反例に数えない）（B の下界 F_0、T の上限 F_ω^ω） |

**T = IOpen**（T で全域と証明できない最初の水準 = F_2）

| 行 | 判定 |
|---|---|
| C1 | 成り立つ（B の下界 F_ε₀、T の上限 F_2） |
| C2 | 成り立つ（B の下界 F_ε₀、T の上限 F_2） |
| C3 | 成り立つ（B の下界 F_ε₀、T の上限 F_2） |
| C4 | 成り立つ（B の下界 F_ω、T の上限 F_2） |
| C5 | 成り立つ（B の下界 F_ω^ω、T の上限 F_2） |
| C6 | 未確認（B の下界の出典が無い） |
| C7 | 未確認（B の下界の出典が無い） |
| C8 | 未確認（B の下界の出典が無い） |
| N1 | 成り立たない（対照 N1。P-v7 の例外なので反例に数えない）（B の下界 F_0、T の上限 F_2） |
| N2 | 成り立たない（対照 N2。判定は「成り立つ」なので、事前登録どおり P-v7 の反例に数える）（B の下界 F_0、T の上限 F_2） |

---

## 4. N2 の判定（T2）

**判定: 成り立つ**

Biljakovic–Kochetov–Kuhlmann §0 p.2: 「Shepherdson ... constructed an IP of this field in which the only irreducible elements are those in Z」（本文）。Berarducci–Otero 1996 の Abstract: 「His model is not normal and does not have any infinite prime elements」（本文）

- 表の #2 の `Prime(p)` は既約元の形（p>1 ∧ p=yz → y=1 ∨ z=1）。文献の「prime」は環論的な素元で、両者は一般には一致しない。Kuhlmann らの論文は **既約元** について「Z の元だけ」と明記しており、#2 の形にそのまま当たる。

---

## 5. 外した候補と理由（凍結文書 §4 のとおり）

| 候補 | 理由 |
|---|---|
| PH の次元固定列（Hájek–Pudlák 定理 II.1.9） | 一次資料の本文が未取得（v8 で取得したのは目次まで）。C5・C6 が同じ階段を Kirby–Paris の本文で与える |
| Ackermann 関数の全域性 | 軸A の下界が無い（PA で証明できる） |
| #31 van der Waerden、#32 Ramsey | 軸A の下界が文献に無い |
| Szemerédi、Green–Tao | 同上 |
