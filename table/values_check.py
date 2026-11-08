#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""値の不変（V）。A・B・Grz の区間の欄だけを 1.0 の写し（ref/v1.0_values.json）と比べる。
usage: values_check.py        # 差が 1 件以上なら exit 1
バイト一致は要求しない（出典の文と式は変えてよい）。
"""
import json, os, sys
sys.dont_write_bytecode = True

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import data, data_cal


def pair(v):
    return [v[0], v[1]] if isinstance(v, (tuple, list)) and len(v) >= 2 else None


def diffs():
    """(差の一覧, 比べた数) を返す。ダッシュボードからも使う。"""
    ref = json.load(open(os.path.join(BASE, "ref", "v1.0_values.json"), encoding="utf-8"))
    ref["H"] = {k: [v[0]] for k, v in ref["H"].items()}          # 階層は「階」の欄だけ
    cur = dict(
        A={str(k): pair(v) for k, v in data.A.items()},
        B={str(k): pair(v) for k, v in data.B1.items() if isinstance(v, tuple) and len(v) >= 2},
        H={str(k): [v[0]] for k, v in data.H.items()},
        CAL=[dict(id=r["id"], a=pair(r["A"]), b=pair(r["B"]),
                  grz=[r["B"][2] if len(r["B"]) > 2 else None,
                       r["B"][3] if len(r["B"]) > 3 else None]) for r in data_cal.ROWS],
    )
    out = []
    for field in ("A", "B", "H"):
        for k in sorted(set(cur[field]) | set(ref[field]), key=lambda x: int(x)):
            if k not in ref[field]:
                out.append("%s %s: 1.0 に無い" % (field, k))
            elif k not in cur[field]:
                out.append("%s %s: 消えた" % (field, k))
            elif cur[field][k] != ref[field][k]:
                out.append("%s %s: %r → %r" % (field, k, ref[field][k], cur[field][k]))
    rcal = {r["id"]: r for r in ref["CAL"]}
    for r in cur["CAL"]:
        if r["id"] not in rcal:
            out.append("CAL %s: 1.0 に無い" % r["id"]); continue
        for f in ("a", "b", "grz"):
            if r[f] != rcal[r["id"]][f]:
                out.append("CAL %s 欄 %s: %r → %r" % (r["id"], f, rcal[r["id"]][f], r[f]))
    shape = (len(cur["A"]), len(cur["B"]), len(cur["H"]), len(cur["CAL"]))
    return out, shape


def main():
    out, shape = diffs()
    print("== V（値の不変: A・B・Grz の区間） ==")
    print("比べたもの: 82行 A %d・B %d・階層 %d ／ 校正表 %d 行（A・B・Grz）"
          % (shape[0], shape[1], shape[2], shape[3]))
    print("V = %d 件（値の差）" % len(out))
    for x in out[:40]:
        print("  -", x)
    return 0 if not out else 1


if __name__ == "__main__":
    sys.exit(main())
