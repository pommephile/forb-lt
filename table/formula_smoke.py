#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""式の検査（v11 T1）。usage: formula_smoke.py [--selftest] [--write]
82 行と校正表 10 行のすべてに (a) 自明な証人 / (b) 弱い主張への潰れ / (c) 原典との一致 を記録する。
- (a) は計算できる行（NUMERIC）は小さな n で計算し、それ以外は範囲条件を文字列で確かめる。Π¹₂ は概略。
- (b) は命題より弱い形（o(x)・有限個・十分大）を含まないことを文字列で確かめる。
- (c) は原典の 1 句（QUOTES）、原典未取得（D10_ROWS）、出典欄の形のいずれか。
--write で formula_check.md / formula_check.json を書く。--selftest は REQ の条件を外して検出を確かめる。
"""
import sys, json, re
sys.path.insert(0, ".")
import data, data_cal
from data_formula_v11 import REQ, QUOTES, D10_ROWS, NOTE

# ------------------------------------------------ 計算で確かめる行
def sieve(n):
    s = [True] * (n + 1); s[0] = s[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i): s[j] = False
    return s

S = sieve(20000)

def is_prime(n):
    return 0 <= n < len(S) and S[n]

def n_prime_inf():
    return all(any(S[p] for p in range(n + 1, 20000)) for n in range(0, 200))

def n_sqrt2():
    return not any(p * p == 2 * q * q for p in range(-60, 61) for q in range(-60, 61) if q != 0)

def n_dirichlet():
    for a, d in [(1, 1), (3, 4), (5, 6), (2, 3)]:
        for n in range(0, 60):
            if not any(S[p] and p > n and p % d == (a % d) for p in range(n + 1, 5000)): return False
    return True

def n_catalan():
    hits = [(a, b, x, y) for a in range(2, 9) for b in range(2, 9)
            for x in range(2, 40) for y in range(2, 40) if x ** a - y ** b == 1]
    return hits == [(2, 3, 3, 2)]

def n_flt():
    return not any(a ** n + b ** n == c ** n for n in range(3, 7)
                   for a in range(1, 26) for b in range(1, 26) for c in range(1, 26))

def n_twin():
    return all(any(S[p] and is_prime(p + 2) for p in range(n + 1, 5000)) for n in range(0, 200))

def n_goldbach():
    return all(any(is_prime(p) and is_prime(n - p) for p in range(2, n + 1)) for n in range(4, 200, 2))

def n_collatz():
    for n in range(1, 2001):
        x, k = n, 0
        while x != 1 and k < 10000:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            k += 1
        if x != 1: return False
    return True

def n_egyptian():
    for n in range(2, 11):
        if not any(4 * x * y * z == n * (x * y + y * z + z * x)
                   for x in range(1, 120) for y in range(x, 120) for z in range(y, 120)):
            return False
    return True

NUMERIC = {
    "82:2": (n_prime_inf, "n=0..199 で p>n の素数あり（sieve 20000）"),
    "82:3": (n_sqrt2, "|p|,|q|≤60, q≠0 で p²=2q² の解なし"),
    "82:27": (n_dirichlet, "a=1,3,5,2 / d=1,4,6,3、n=0..59 で素数あり"),
    "82:30": (n_catalan, "a,b≤8, x,y≤39 の解は (2,3,3,2) のみ"),
    "82:39": (n_flt, "n=3..6, a,b,c≤25 で解なし"),
    "82:69": (n_twin, "n=0..199 で双子素数あり（予想なので反例なしの確認まで）"),
    "82:70": (n_goldbach, "偶数 n=4..198 で p+q=n の素数対あり"),
    "82:71": (n_collatz, "n=1..2000 で 1 に到達"),
    "82:81": (n_egyptian, "n=2..10 で 1≤x≤y≤z≤119 の解あり"),
}

WEAK = ["o(x)", "o(", "有限個", "十分大きい"]

def strip_parens(s):
    """（…）の注記を外す。(b) は式そのものを見る（注記の中の「自明」「弱い」は対象外）。"""
    out, depth = [], 0
    for ch in s:
        if ch == "（": depth += 1; continue
        if ch == "）":
            if depth: depth -= 1
            continue
        if depth == 0: out.append(ch)
    return "".join(out)
RANGE = [">1", "≥1", ">0", "≥2", "1≤", "⊆[N]", "∈ℤ", "有限", "n>", "k>", "≤n", "N="]

def row(key, hier, prenex):
    """1 行分の (a)(b)(c) と判定を返す。"""
    fails = []
    if key in NUMERIC:
        fn, note = NUMERIC[key]
        ok = fn()
        a, a_kind = "計算: " + note, "計算"
        if not ok: fails.append("%s (a) 計算で反例" % key)
    elif hier.startswith("Π¹₂"):
        a, a_kind = "概略（函数・集合の量化）。恒真の二分（P ∨ ¬P）を含まない（文字列）", "概略"
        if re.search(r"∨\s*¬", prenex): fails.append("%s (a) 恒真の二分" % key)
    else:
        toks = [t for t in RANGE if t in prenex]
        a = ("範囲条件 " + "・".join(toks) + " がある（0・1・空は範囲外）") if toks else "範囲条件なし（0 を代入する形ではない）"
        a_kind = "文字列"
    if key in NOTE: a = NOTE[key][0]

    b = "弱い形（o(x)・有限個・十分大）を含まない"
    body = strip_parens(prenex)
    for w in WEAK:
        if w in body:
            b = "弱い形「%s」を含む（要確認）" % w
            fails.append("%s (b) 弱い形" % key)
    if key in NOTE: b = NOTE[key][1]

    if key in QUOTES: c = "引用: " + QUOTES[key]
    elif key in D10_ROWS: c = "原典の本文は未取得（D10）"
    else: c = "出典欄の記載の形（句の引用なし）"

    for tok in REQ.get(key, []):
        if tok not in prenex:
            fails.append("%s 条件「%s」が式に無い" % (key, tok))

    # 判定: 式の条件が欠けていれば「要修正」。(a)(b)(c) のどれかが未確認なら「要確認」。
    # 「要確認」の行を「OK」と書かない（v12 T1）。
    unresolved = any(w in (a + b + c) for w in ("要確認", "未取得", "未特定"))
    if fails: verdict = "要修正"
    elif unresolved: verdict = "要確認"
    else: verdict = "OK"
    return dict(key=key, hier=hier, a=a, a_kind=a_kind, b=b, c=c,
                verdict=verdict, fails=fails)

def all_rows():
    out = []
    for n in sorted(data.H):
        h, p = data.H[n]
        out.append(row("82:%d" % n, h, p))
    for r in data_cal.ROWS:
        out.append(row("cal:" + r["id"], "Π₂（校正表）", r["prenex"]))
    return out

def source_of(key):
    if key.startswith("82:"):
        return data.H[int(key.split(":")[1])]
    return ("Π₂（校正表）", next(r["prenex"] for r in data_cal.ROWS if "cal:" + r["id"] == key))

def main():
    rows = all_rows()
    # F は「式の検査を記録した行」＝ (a)(b)(c) がすべて埋まっている行。判定とは別に数える。
    f_ok = sum(1 for r in rows if r["a"] and r["b"] and r["c"])
    vd = {}
    for r in rows:
        vd[r["verdict"]] = vd.get(r["verdict"], 0) + 1
    kinds = {}
    for r in rows:
        kinds[r["a_kind"]] = kinds.get(r["a_kind"], 0) + 1
    fails = [f for r in rows for f in r["fails"]]

    print("== 式の検査（F） ==")
    print("| 行 | 階層 | (a) 自明な証人 | (b) 弱い主張への潰れ | (c) 原典 | 判定 |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        print("| %s | %s | %s | %s | %s | %s |" % (r["key"], r["hier"], r["a"], r["b"], r["c"], r["verdict"]))
    print("")
    print("F 式の検査を記録した行 = %d / %d（(a) の根拠: 計算 %d・文字列 %d・概略 %d）"
          % (f_ok, len(rows), kinds.get("計算", 0), kinds.get("文字列", 0), kinds.get("概略", 0)))
    print("判定の内訳: " + " / ".join("%s %d" % (k, v) for k, v in sorted(vd.items())))
    print("違反: %d 件" % len(fails))
    for f in fails:
        print("  -", f)

    fprime = 0
    if "--selftest" in sys.argv:
        print("== 自己試験（条件を外すと検出するか） ==")
        for key, toks in REQ.items():
            hier, prenex = source_of(key)
            bad = prenex.replace(toks[0], "")
            if bad == prenex:
                print("自己試験 %s: 変異が当たっていない" % key); continue
            r2 = row(key, hier, bad)
            hit = bool(r2["fails"])
            fprime += 1 if hit else 0
            print("自己試験 %s（「%s」を外す）: %s"
                  % (key, toks[0], ("検出 1 件（%s）" % r2["fails"][0]) if hit else "検出できず"))
        print("F' 自己試験 = %d / %d 検出" % (fprime, len(REQ)))

    if "--write" in sys.argv:
        open("formula_check.md", "w", encoding="utf-8").write(
            "\n".join(["| 行 | 階層 | (a) 計算 | (a) 範囲条件（文字列） | (b) 弱い主張への潰れ | (c) 原典 | 判定 |",
                       "|---|---|---|---|---|---|---|"] +
                      ["| %s | %s | %s | %s | %s | %s | %s |" %
                       (r["key"], r["hier"],
                        (r["a"] if r["a_kind"] != "文字列" else "—"),
                        (r["a"] if r["a_kind"] == "文字列" else "—"),
                        r["b"], r["c"], r["verdict"])
                       for r in rows]) + "\n")
        json.dump(dict(total=len(rows), f=f_ok, fprime=fprime, kinds=kinds,
                       rows=[dict(key=r["key"], hier=r["hier"], a=r["a"], b=r["b"], c=r["c"],
                                  verdict=r["verdict"], a_kind=r["a_kind"]) for r in rows]),
                  open("formula_check.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
