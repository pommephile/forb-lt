#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D10 の台帳（一次資料の取得状況）。v8 の T1・T2 で実際に開いたものだけを「取得」とする。"""
ITEMS = [
 dict(id="KS1981", name="Ketonen–Solovay 1981, Rapidly growing Ramsey functions, Ann. of Math. 113",
      status="未取得", note="Annals の PDF は 404、JSTOR は paywall。内容は Kirby–Paris 1982 の Thm 4 と Paris–Harrington 1977 の Thm 3.2 の引用で確認"),
 dict(id="FRS1987", name="Friedman–Robertson–Seymour 1987, The metamathematics of the graph minor theorem",
      status="未取得", note="AMS の章ページは 403。有限形の正確な形は確認できず"),
 dict(id="SY2007", name="Sakamoto–Yokoyama 2007, The Jordan curve theorem and the Schönflies theorem in weak second-order arithmetic",
      status="未取得", note="Springer は closed。Semantic Scholar の abstract も publisher により削除。Tohoku のページは 404"),
 dict(id="Mahler-e", name="Mahler, Zur Approximation der Exponentialfunktion und des Logarithmus (Crelle 166, 1932), Satz 3",
      status="取得", note="Mahler Archive の PDF（carmamaths.org/docs/011.pdf）を取得。式は Fischler–Rivoal (arXiv:2502.17992) が p.135 Satz 3 として引用: |Σ a_k e^k| ≥ c·H^{-(δ+ln(δ+1))}"),
 dict(id="Shepherdson+BO", name="Shepherdson 1964 と Berarducci–Otero 1996 の本文",
      status="取得", note="Berarducci–Otero の本文（matematicas.uam.es の PDF）と、Biljakovic–Kochetov–Kuhlmann「Primes and Irreducibles in Truncation Integer Parts of Real Closed Fields」§0 の記述（Shepherdson モデルの既約元は Z の元だけ）。Shepherdson 1964 の原本は未取得"),
 dict(id="Simpson1985", name="Simpson 1985, Nonprovability of certain combinatorial properties of finite trees（Kruskal 有限形）",
      status="未取得", note="ScienceDirect の PDF は 403。Simpson の論文リストも本文へのリンクを与えない"),
 dict(id="HP-II", name="Hájek–Pudlák, Metamathematics of First-Order Arithmetic, 第 II 章",
      status="未取得", note="Springer のプレビュー（48ページ）で目次だけ取得。CHAPTER II の節構成と定理 1.5〜1.10 の存在は確認したが、II.1.9 の本文は未取得"),
]
