#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T4: (i) 定理による検査 / (ii) 区間比較（比較不能を (a)(b) に分割）/ D5（命題の数）/ 自己試験3件。
usage: compare.py <v4.1.md> <out.json> [--cal] [--selftest]
  --cal を付けると校正表（data_cal）を対象にする。
"""
import sys, json, itertools, re
sys.path.insert(0, ".")

CAL = "--cal" in sys.argv
SELFTEST = "--selftest" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("--")]
MD = args[0] if args else None
OUT = args[1] if len(args) > 1 and args[1] != "/dev/null" else None

if CAL:
    import data_cal as D
    ROWS_IN = D.ROWS
    ORDER_A = D.ORDER_CAL
    ORDER_B = D.ORDER_B
    D5_CONFIRMED_NOTE = D.D5_NOTE
else:
    sys.path.insert(0, ".")
    import data as D
    ORDER_A = D.ORDER_A
    ORDER_B = D.ORDER_B

# ---------------------------------------------------------------- 82行の表
if not CAL:
    H, A, B1, GRZ = D.H, D.A, D.B1, D.GRZ_ROW
    EXTRA_A = {"PA+TI(ε₀)": 9.5, "PA+1-Con(PA)": 9.5}
    CEIL = {"IΔ₀": 2, "EFA": 3, "RCA₀": 4, "WKL₀": 4, "PRA": 4, "ACA₀": 5, "PA": 5}
    names = {}
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
            names[int(c[0])] = c[1]

    # D5: 上側の行 j の軸A 下界に、増え方の下界を使わない公刊の証明があるか（本文で確認したものだけ「別」）
    D5_ROUTE = {
        75: ("増え方", "Kirby–Paris 1982, Thm 1(ii) の証明は Ketonen–Solovay の indicator（α-large 集合）を使う（本文で確認）"),
        76: ("別", "Paris–Harrington 1977, §2: Con(T)→Con(PA) と「1.2 が Con(T) を含意」。増え方は §3.2 で系として出るだけ（本文 OCR で確認）"),
    }

    def arank(s):
        return EXTRA_A[s] if s in EXTRA_A else float(ORDER_A.index(s))
    def a_lo_rank(s): return -10**6 if s == "—" else arank(s) + 1
    def a_up_rank(s): return 10**6 if s == "—" else arank(s)
    def b_lo_rank(s): return -10**6 if s == "—" else ORDER_B.index(s)
    def b_up_rank(s): return 10**6 if s == "—" else ORDER_B.index(s)

    def check(A_tbl, B_tbl):
        viol, bad_iv = [], []
        for n, (hh, _) in H.items():
            if hh != "Π₂" or n not in B_tbl or n not in A_tbl:
                continue
            alo, aup, _ = A_tbl[n]
            blo, bup, _ = B_tbl[n]
            if aup in CEIL and blo != "—" and b_lo_rank(blo) >= CEIL[aup]:
                viol.append({"num": n, "A_up": aup, "B_lo": blo,
                             "why": "#%d: B の下界 %s は %s で全域と証明できる関数の上限（F_%d）以上なのに、軸A の上界が %s"
                                    % (n, blo, aup, CEIL[aup], aup)})
        for n, (lo, up, _) in A_tbl.items():
            if lo != "—" and up != "—" and a_lo_rank(lo) > a_up_rank(up):
                bad_iv.append({"num": n, "lo": lo, "up": up,
                               "why": "#%d: 軸A の下界 %s が上界 %s を超えている（下界 > 上界）" % (n, lo, up)})
        return viol, bad_iv

    def rows_of(A_tbl, B_tbl):
        rows = []
        for n, (hh, _) in H.items():
            if hh != "Π₂" or n not in A_tbl or n not in B_tbl:
                continue
            alo, aup, _ = A_tbl[n]
            blo, bup, _ = B_tbl[n]
            rows.append({"num": n, "name": names.get(n, ""), "a": "[%s, %s]" % (alo, aup),
                         "a_lo": a_lo_rank(alo), "a_up": a_up_rank(aup),
                         "b": "[%s, %s]（%s/%s）" % (blo, bup, GRZ.get(n, ("—", "—"))[0], GRZ.get(n, ("—", "—"))[1]),
                         "b_known": blo != "—" or bup != "—",
                         "b_lo": b_lo_rank(blo), "b_up": b_up_rank(bup)})
        return rows

    viol, bad_iv = check(A, B1)
    rows = rows_of(A, B1)
    def scan_bad_b(B_tbl):
        return sorted({n for n, (lo, up, _s) in B_tbl.items() for v in (lo, up) if v != "—" and v not in ORDER_B})
    bad_b = scan_bad_b(B1)
    D5_LABEL = "82行の表"

# ---------------------------------------------------------------- 校正表
else:
    rows = []
    for r in ROWS_IN:
        rows.append({"num": r["id"], "name": r["name"], "a": "[%s, %s]" % (r["A"][0], r["A"][1]),
                     "a_lo": D.a_lo_rank(r["A"][0]), "a_up": D.a_up_rank(r["A"][1]),
                     "b": "[%s, %s]（%s/%s）" % (r["B"][0], r["B"][1], r["B"][2], r["B"][3]),
                     "b_known": (r["B"][0] != "—" or r["B"][1] != "—"),
                     "b_lo": D.b_lo_rank(r["B"][0]), "b_up": D.b_up_rank(r["B"][1]),
                     "method": r["method"], "confirmed": r["confirmed"], "natural": r["natural"]})
    # (i) 校正表版（監査 v7.1）: 上限は data_cal.CEIL_CAL。82行の表と同じく「B の下界 >= 上限」で違反とする。
    #     v7 は ">" に変え、C2 の上界の誤り（PA+Con(PA)）を素通りさせていた。
    CEIL_CAL = D.CEIL_CAL
    viol = []
    bad_iv = []
    viol_ge = []
    for r in ROWS_IN:
        up = r["A"][1]; blo = r["B"][0]
        if up in CEIL_CAL and blo != "—":
            if ORDER_B.index(blo) >= CEIL_CAL[up]:
                viol.append({"num": r["id"], "why": "%s: B の下界 %s は %s で全域と証明できる関数の上限以上なのに、軸A の上界が %s" % (r["id"], blo, up, up)})
                viol_ge.append(r["id"])
    for r in rows:
        if r["a"] != "[—, —]" and r["a_lo"] > r["a_up"]:
            bad_iv.append({"num": r["num"], "why": "A 区間が逆転: %s" % r["a"]})
        if r["b_known"] and r["b_lo"] > r["b_up"]:
            bad_iv.append({"num": r["num"], "why": "B 区間が逆転: %s" % r["b"]})
    def scan_bad_b(rows_in):
        return sorted({r["id"] for r in rows_in for v in (r["B"][0], r["B"][1]) if v != "—" and v not in ORDER_B})
    bad_b = scan_bad_b(ROWS_IN)
    D5_LABEL = "校正表"

# ---------------------------------------------------------------- 比較
C = Dd = inc_a = inc_b = 0
pairs = []
for p, q in itertools.combinations(rows, 2):
    if p["a_up"] < q["a_lo"]:
        i, j = p, q
    elif q["a_up"] < p["a_lo"]:
        i, j = q, p
    else:
        inc_a += 1
        pairs.append({"i": p["num"], "j": q["num"], "verdict": "比較不能(a) Aが重なる"})
        continue
    if i["b_known"] and j["b_known"] and i["b_up"] < j["b_lo"]:
        C += 1; pairs.append({"i": i["num"], "j": j["num"], "verdict": "一致"})
    elif i["b_known"] and j["b_known"] and j["b_up"] < i["b_lo"]:
        Dd += 1; pairs.append({"i": i["num"], "j": j["num"], "verdict": "逆順"})
    else:
        inc_b += 1
        pairs.append({"i": i["num"], "j": j["num"], "verdict": "比較不能(b) Aが分離しBが重なる/未取得"})

# D5（命題の数）
if not CAL:
    d5_ok = sorted({p["j"] for p in pairs if D5_ROUTE.get(p["j"], ("未確認",))[0] == "別"})
    d5_rows = D5_ROUTE
else:
    d5_ok = sorted({r["num"] for r in rows if r.get("natural") and r["method"] == "使わない" and r["confirmed"]})
    d5_rows = {r["id"]: (r["method"], r["src_a"]) for r in ROWS_IN if r.get("natural")}

NAT = {r["num"]: bool(r.get("natural", True)) for r in rows}
pairs_natural = sum(1 for p in pairs if p["verdict"] in ("一致", "逆順") and NAT.get(p["i"]) and NAT.get(p["j"]))

D5_NOTE = ("判定: 「j の軸A 下界に、増え方の下界を使わない公刊の証明があり、それを本文で確認したか」。"
           "82行の表では #76 のみ該当（Paris–Harrington 1977 の §2。増え方は §3.2 で系として出る）。"
           "#75 は Kirby–Paris 1982 の証明が Ketonen–Solovay の indicator を使うため数えない。")

d = {"table": D5_LABEL, "rows": rows, "C": C, "D": Dd,
     "comparable": C + Dd, "incomparable": inc_a + inc_b,
     "incomparable_a": inc_a, "incomparable_b": inc_b,
     "pairs": pairs, "violations": viol, "bad_intervals": bad_iv,
     "d5_statements": len(d5_ok), "d5_list": d5_ok, "d5_note": D5_NOTE,
     "d6": sum(1 for r in rows if r["b_known"]),
     "d5_rows": {str(k): v for k, v in d5_rows.items()},
     "pairs_natural": (pairs_natural if CAL else None),
     "bad_b_values": bad_b, "order_a": ORDER_A,
     "viol_ge_boundary": (viol_ge if CAL else [])}

if SELFTEST:
    if CAL:
        # 校正表の自己試験は2件（v8 指示書の合格基準6）
        print("== 自己試験1: C2 の上界を v7 の値 PA+Con(PA) に戻す（v7 で素通りした誤りの回帰）==")
        c2 = [r for r in ROWS_IN if r["id"] == "C2"][0]
        hit = [c2["id"]] if ORDER_B.index(c2["B"][0]) >= D.CEIL_CAL["PA+Con(PA)"] else []
        print("検出 %d 件: %s（PA+Con(PA) の上限 %d、C2 の B 下界 %d）"
              % (len(hit), hit, D.CEIL_CAL["PA+Con(PA)"], ORDER_B.index(c2["B"][0])))
        d["selftest_c2_v7"] = hit
        print("== 自己試験2: B 欄に尺度外の値（E²）を入れる ==")
        bad3 = scan_bad_b([dict(ROWS_IN[0], B=("E²", "E²", "—", "自己試験用"))])
        print("検出 %d 件: E² は F_α の尺度に無い（該当 %s）" % (len(bad3), bad3))
        d["selftest_b_scale"] = bad3
    else:
        print("== 自己試験1: #75 の軸A 上界を PA に改変 ==")
        A_bad = dict(A); A_bad[75] = ("PA", "PA", "自己試験用の作為的な値")
        v2, _ = check(A_bad, B1)
        print("検出 %d 件" % len(v2))
        for v in v2: print("  " + v["why"])
        d["selftest_viol_75"] = v2
        print("== 自己試験2: 軸A 区間の逆転 ==")
        A_bad2 = dict(A); A_bad2[45] = ("ZFC", "Π¹₁-CA₀", "自己試験用の逆転")
        _, iv2 = check(A_bad2, B1)
        print("検出 %d 件" % len(iv2))
        for v in iv2: print("  " + v["why"])
        d["selftest_interval_45"] = iv2
        print("== 自己試験3: B 欄に尺度外の値（E²）を入れる ==")
        B_bad = dict(B1); B_bad[65] = ("E²", "E²", "自己試験用の尺度外の値")
        bad3 = scan_bad_b(B_bad)
        print("検出 %d 件: E² は F_α の尺度に無い（該当 %s）" % (len(bad3), bad3))
        d["selftest_b_scale"] = bad3

if OUT:
    open(OUT, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))

print("== (i) 定理による検査 ==")
print("違反 %d 件 / 区間の不健全 %d 件" % (len(viol), len(bad_iv)))
for v in viol: print("  " + v["why"])
for v in bad_iv: print("  " + v["why"])
print("== (ii) 区間比較 ==")
print("対象行 %d / 比較できる組 %d（C=%d, D=%d）／比較不能 %d（(a) A が重なる %d / (b) A が分離し B が重なる %d）"
      % (len(rows), C + Dd, C, Dd, inc_a + inc_b, inc_a, inc_b))
for r in rows:
    print("  #%-4s %-26s A=%-24s B=%s" % (r["num"], str(r["name"])[:26], r["a"], r["b"]))
print("== 比較できる組の一覧 ==")
for p in pairs:
    if p["verdict"] in ("一致", "逆順"):
        print("  %s - %s : %s" % (p["i"], p["j"], p["verdict"]))
print("  自然な命題どうしの組: %s" % (pairs_natural if CAL else "（82行の表では区別しない）"))
print("== D5 ==")
print("増え方を使わない証明がある命題: %d 件 %s ／ B の尺度外の値: %d 件" % (len(d5_ok), d5_ok, len(bad_b)))
