#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""#36 の量化子の構成を機械的に確かめる。
rank≥r（Σ₁）と ord≥r（Π₁）の 2 つの連言項の前綴りを、量化子の交代の規則で計算し、Π₂ になることを示す。
"""
S1, P1 = ["∃"], ["∀"]          # Σ₁ = ∃、Π₁ = ∀（内側は判定可能）
SUB = {1: "₁", 2: "₂", 3: "₃", 4: "₄"}

def impl(a, b):
    """a → b の前綴り: a の量化子を反転して前に出し、b の量化子を続ける"""
    flip = {"∃": "∀", "∀": "∃"}
    return [flip[q] for q in a] + b

def forall(prefix):
    return ["∀"] + prefix

def klass(prefix):
    if not prefix:
        return "Δ₀"
    runs = 1
    for i in range(1, len(prefix)):
        if prefix[i] != prefix[i - 1]:
            runs += 1
    return ("Π" if prefix[0] == "∀" else "Σ") + SUB.get(runs, str(runs))

terms = {"rank≥r → ord≥r": impl(S1, P1), "ord≥r → rank≥r": impl(P1, S1)}
for name, pre in terms.items():
    print("%-18s 前綴り %s → ∀r で %s" % (name, "".join(pre), klass(forall(pre))))
first, second = (klass(forall(terms[k])) for k in ["rank≥r → ord≥r", "ord≥r → rank≥r"])
result = "Π₂" if {first, second} <= {"Π₁", "Π₂"} else "?"
print("連言の階級 = %s（Π₁ ∧ Π₂ は Π₂）" % result)
ok = (first == "Π₁" and second == "Π₂" and result == "Π₂")
print("結論: #36 の量化子の構成は Π₂（第1項 Π₁・第2項 Π₂）。%s" % ("OK" if ok else "NG"))
