#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""release/vX.Y の一覧表 md から app 用の data.json を作る。release は読むだけ。
usage: make_data.py <release_dir> <out.json>
"""
import sys, re, json, os

def main(rel, out):
    md = open(os.path.join(rel, "Forb-LT一覧表.md"), encoding="utf-8").read()
    rows = []
    for l in md.splitlines():
        if not l.startswith("| "): continue
        c = [x.strip() for x in re.split(r"(?<!\\)\|", l)[1:-1]]
        if len(c) != 13 or not re.fullmatch(r"\d+", c[0]): continue
        rows.append({"id": int(c[0]), "name": c[1], "tier": c[3], "prenex": c[4].replace("\\|", "|"),
                     "pi1": c[5], "A": c[6], "A_src": c[7], "b_fa": c[9], "b_grz": c[10],
                     "b_src": c[11], "status": c[12].replace("✅", "記入済")})
    cm = open(os.path.join(rel, "Forb-LT校正表.md"), encoding="utf-8").read()
    cal = []
    for l in cm.splitlines():
        if not l.startswith("| "): continue
        c = [x.strip() for x in re.split(r"(?<!\\)\|", l)[1:-1]]
        if len(c) < 9 or not re.fullmatch(r"C\d+|N\d+", c[0]): continue
        cal.append({"id": c[0], "name": c[1], "prenex": "|".join(c[2:-6]), "A": c[-6],
                    "method": c[-5], "A_src": c[-4], "B": c[-3], "B_grz": c[-2], "B_src": c[-1]})
    sums = open(os.path.join(rel, "SHA256SUMS"), "rb").read()
    import hashlib
    data = {"version": os.path.basename(rel.replace("v", "")), "date": "2026-11-06",
            "sha256": hashlib.sha256(sums).hexdigest(), "rows": rows, "cal": cal}
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("rows=%d cal=%d → %s" % (len(rows), len(cal), out))
    return 0 if len(rows) == 82 and len(cal) == 10 else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
