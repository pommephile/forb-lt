#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T4 の文言チェック: 指示書 v8 の題・前書き・付録の観察が、表にそのまま載っているか。
`［ ］` の中だけが埋まっていることを、前後の文字列一致で確かめる。
usage: verify_t4.py <指示書.md> <表.md>
"""
import sys, re

directive = open(sys.argv[1], encoding="utf-8").read()
table = open(sys.argv[2], encoding="utf-8").read()

def quote_block(marker):
    i = directive.index(marker) + len(marker)
    out, started = [], False
    for ln in directive[i:].splitlines():
        if ln.startswith(">"):
            started = True
            out.append(ln[1:].lstrip(" ").rstrip())
        elif started and ln.strip() == "":
            continue
        elif started:
            break
    return [x for x in out if x.strip()]

title = quote_block("**題**:")[0]
pre = quote_block("**前書き**:")
app = quote_block("**付録の観察（P-v7）**:")

errs = []
if title not in table:
    errs.append("題が一致しない: " + title)
for p in pre:
    if p not in table:
        errs.append("前書きの段落が一致しない: " + p[:40] + "…")

# 付録: ［ ］ の前後で分けて一致を見る
for p in app:
    m = re.search(r"［([^］]*)］", p)
    if not m:
        if p not in table:
            errs.append("付録の段落が一致しない: " + p[:40] + "…")
        continue
    head, tail = p[:m.start()], p[m.end():]
    idx = table.find(head)
    if idx < 0:
        errs.append("付録の段落（前半）が一致しない: " + head[:40] + "…")
        continue
    seg = table[idx:idx + len(p) + 400]
    if tail and tail[:30] not in seg:
        errs.append("付録の段落（後半）が一致しない: " + tail[:40] + "…")
    # ［ ］ の中が空でないこと
    m2 = re.search(r"［([^］]*)］", seg)
    if not m2 or m2.group(1).strip() == "" or m2.group(1) == p[m.start()+1:m.end()-1]:
        errs.append("［ ］ が埋まっていない: " + p[m.start():m.end()][:40])

print("題: %s" % ("一致" if title in table else "不一致"))
print("前書き: %d段落 / 一致 %d" % (len(pre), sum(1 for p in pre if p in table)))
print("付録の観察: %d段落" % len(app))
print("違反: %d件" % len(errs))
for e in errs:
    print("  -", e)
sys.exit(0 if not errs else 1)
