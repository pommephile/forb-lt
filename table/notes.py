#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D11: 注記の残りを数え、処置の台帳と突き合わせる。
usage: notes.py <82行の表.md> <校正表.md> [--selftest]
- 表に注記（要検算・要確認・未確認・未取得・要出典・標準的）が残る行を数える（D11）
- 台帳の全行に処置があること、処置「解消」の行に注記が残っていないことを検査する
- --selftest: 「解消」の行の本体に注記の語を書き込み、違反として検出することを示す
"""
import sys, re, os, tempfile
sys.path.insert(0, ".")
from data_notes import NOTES

R = re.compile("要検算|要確認|未確認|未取得|要出典|標準的")

def rows82(path):
    # v9.1（監査）: 同じ行番号の行が後ろの節（§2・§3）にもあるので、行を上書きせず連結する。
    # 以前は最後の行だけが残り、#29（§3 の「該当なし」の行）で本体の注記を見落とした。
    out = {}
    for ln in open(path, encoding="utf-8").read().splitlines():
        if re.match(r"^\| *\d+ \|", ln):
            c = [x.strip() for x in re.split(r"(?<!\\)\|", ln.strip()[1:-1])]
            out[c[0]] = out.get(c[0], "") + "\n" + ln
    return out

def rows_cal(path):
    out, inside = {}, False
    for ln in open(path, encoding="utf-8").read().splitlines():
        if ln.startswith("## 1."): inside = True; continue
        if inside and ln.startswith("## "): break
        if inside and re.match(r"^\| *(C|N)\d+ \|", ln):
            c = [x.strip() for x in re.split(r"(?<!\\)\|", ln.strip()[1:-1])]
            out[c[0]] = ln
    return out

def analyze(md82, mdcal):
    t82, tcal = rows82(md82), rows_cal(mdcal)
    cur = {}
    for n, ln in t82.items():
        if R.search(ln): cur["82:" + n] = True
    for n, ln in tcal.items():
        if R.search(ln): cur["cal:" + n] = True
    errs = []
    for rec in NOTES:
        k = rec["key"]
        if rec["status"] == "解消" and k in cur:
            errs.append("%s は「解消」なのに注記が残っている" % k)
        if rec["status"] == "残存" and k not in cur:
            errs.append("%s は「残存」なのに注記が消えている" % k)
    for k in cur:
        if k not in {r["key"] for r in NOTES}:
            errs.append("%s が台帳に無い（処置が未記入）" % k)
    return cur, errs

def main():
    md82, mdcal = sys.argv[1], sys.argv[2]
    cur, errs = analyze(md82, mdcal)
    print("| 行 | 注記（v8.1） | 処置 | 状態 | 内容 |")
    print("|---|---|---|---|---|")
    for rec in NOTES:
        print("| %s | %s | %s | %s | %s |" % (rec["label"], rec["was"], rec["action"], rec["status"], rec["detail"]))
    print("")
    print("D11 注記の残り = %d（82行 %d / 校正表 %d）"
          % (len(cur), sum(1 for k in cur if k.startswith("82:")), sum(1 for k in cur if k.startswith("cal:"))))
    print("処置の内訳: 出典 %d / 取れない %d / 検算 %d"
          % (sum(1 for r in NOTES if r["action"] == "出典"), sum(1 for r in NOTES if r["action"] == "取れない"),
             sum(1 for r in NOTES if r["action"] == "検算")))
    print("違反: %d件" % len(errs))
    for e in errs:
        print("  -", e)
    if "--selftest" in sys.argv:
        # 「解消」にした行の本体に注記の語を書き込み、違反として検出されるか
        target = next((r for r in NOTES if r["status"] == "解消" and r["key"].startswith("82:")), None)
        if target is None:
            print("自己試験: 対象（82行の解消行）が無く、検査の前提が壊れている")
            return 1
        num = target["key"].split(":")[1]
        lines = open(md82, encoding="utf-8").read().splitlines()
        hit = False
        for i, ln in enumerate(lines):
            if re.match(r"^\| *%s \|" % num, ln):
                lines[i] = ln[:-1] + " 要確認 |"; hit = True
        if not hit:
            print("自己試験: #%s の行が見つからず、変異が当たっていない" % num)
            return 1
        fd, tmp = tempfile.mkstemp(suffix=".md"); os.close(fd)
        open(tmp, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        _, errs2 = analyze(tmp, mdcal)
        os.unlink(tmp)
        got = [e for e in errs2 if target["key"] in e]
        print("自己試験（#%s に「要確認」を書き込む）: 検出 %d 件 %s"
              % (num, len(got), ("（%s）" % got[0]) if got else "（検出できず）"))
        return 0 if got else 1
    return 0 if not errs else 1

if __name__ == "__main__":
    sys.exit(main())
