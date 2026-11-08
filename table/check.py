#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""検査器。usage: check.py <表.md> <t.json>
見るもの: 表の形・階層と B v1 の対応・集計の一致・T4 の数字の一致・§2.6 の行数。
値の正しさは見ない（それは compare.py の (i) と監査の仕事）。
式が命題を正しく表しているかは検査しない（v9.2 で #40・#70 の式を直した。式の自明性は formula_smoke.py が見る）。
"""
import sys, re, json, collections

MD, T5 = sys.argv[1], sys.argv[2]
t5 = json.load(open(T5, encoding="utf-8"))
txt = open(MD, encoding="utf-8").read()
ALLOWED = {"Π₁", "Σ₁", "Π₂", "Σ₂", "Σ₃", "Π₃", "Π₄", "算術(階未定)", "Π¹₁", "Π¹₂", "実閉体", "算術外", "未分類"}

rows = []
in_tbl = False
for ln in txt.splitlines():
    if ln.startswith("## 1."):
        in_tbl = True; continue
    if in_tbl and ln.startswith("## "):
        break
    if not in_tbl or not re.match(r"^\|\s*\d+\s*\|", ln):
        continue
    c = [x.strip() for x in re.split(r"(?<!\\)\|", ln.strip()[1:-1])]
    rows.append(c)

errs = []
def chk(cond, msg):
    if not cond:
        errs.append(msg)

chk(len(rows) == 82, "行数が82でない: %d" % len(rows))
chk([int(c[0]) for c in rows] == list(range(1, 83)), "番号が1..82でない")
for c in rows:
    if len(c) < 13:
        errs.append("#%s の列数が13未満: %d" % (c[0], len(c))); continue
    n = int(c[0]); hier, pi1c, b1 = c[3], c[5], c[9]
    chk(hier in ALLOWED, "#%d 階層が規格外: %s" % (n, hier))
    if hier == "Π₂":
        chk(b1 != "—", "#%d Π₂ なのに B_v1 が —" % n)
    else:
        chk(b1 == "—", "#%d Π₂ でないのに B_v1 がある: %s" % (n, b1))
    if hier == "Π₁":
        chk(pi1c == "記述的（予測対象外）", "#%d Π₁ なのに扱いの記載がない: %s" % (n, pi1c))
    else:
        chk(pi1c == "—", "#%d Π₁ でないのに扱いが入っている: %s" % (n, pi1c))

cnt = collections.Counter(c[3] for c in rows if len(c) >= 13)
for k in sorted(ALLOWED):
    m = re.search(r"^\| %s \| (\d+) \|$" % re.escape(k), txt, re.M)
    chk(m and int(m.group(1)) == cnt.get(k, 0), "§2.1 の %s が不一致（実測 %d）" % (k, cnt.get(k, 0)))
d4 = sum(v for k, v in cnt.items() if k != "未分類")
chk(("D4（未分類を除く）= %d/82" % d4) in txt, "D4 が不一致（実測 %d）" % d4)
d4x = sum(v for k, v in cnt.items() if k not in ("未分類", "Π¹₂", "算術(階未定)"))
chk(("D4確定（Π¹₂ の概略と階未定を除く）= %d/82" % d4x) in txt, "D4確定 が不一致（実測 %d）" % d4x)
chk(not t5.get("bad_b_values", ["キーなし"]), "B v1 に尺度外の値がある: %s" % t5.get("bad_b_values"))
pi2 = [c for c in rows if c[3] == "Π₂"]
d1 = sum(1 for c in pi2 if c[9] not in ("—", "[—, —]"))
chk(("**D1 = %d/82**" % d1) in txt, "D1 が不一致（実測 %d）" % d1)
chk(("| Π₂ の行 | %d |" % len(pi2)) in txt, "Π₂ の行数が不一致（実測 %d）" % len(pi2))
pi1n = sum(1 for c in rows if c[3] == "Π₁")
chk(("Π₁ の行は **%d行**" % pi1n) in txt, "Π₁ の行数が不一致（実測 %d）" % pi1n)

chk(("**%d件**" % len(t5["violations"])) in txt, "T5 (i) の違反件数が不一致")
chk(("| 比較できる組 | %d（C=%d, D=%d） |" % (t5["comparable"], t5["C"], t5["D"])) in txt, "T5 (ii) が不一致")
chk(("| 比較不能 (a) A が重なる | %d |" % t5["incomparable_a"]) in txt, "比較不能 (a) が不一致")
chk(("| 比較不能 (b) A が分離し B が重なる/未取得 | %d |" % t5["incomparable_b"]) in txt, "比較不能 (b) が不一致")
chk(("**%d** |" % t5["d5_statements"]) in txt, "D5 が不一致")
chk(("**%d** |" % t5["d6"]) in txt, "D6 が不一致")
chk(txt.count("\n| # | 命題 | 階 | 冠頭形 |") == 1, "§2.6 の表が無い")
sec26 = re.search(r"### 2\.6.*?(?=\n### |\n---)", txt, re.S)
chk(sec26 and len(re.findall(r"^\| \d+ \|", sec26.group(0), re.M)) == 9, "§2.6 の行数が9でない")
chk(not any(ln.startswith("||") for ln in txt.splitlines()), "行頭 '||' の崩れた行がある")

print("=" * 68)
print("検査: 一覧表 %d行 / Π₂ %d行（記入 %d） / Π₁ %d行" % (len(rows), len(pi2), d1, pi1n))
print("階層:", dict(cnt))
print("D4=%d  D4確定=%d  D1=%d  D5=%d命題  D6=%d  T5(i)=%d件  比較不能(a)=%d (b)=%d"
      % (d4, d4x, d1, t5["d5_statements"], t5["d6"], len(t5["violations"]), t5["incomparable_a"], t5["incomparable_b"]))
print("違反: %d件" % len(errs))
for e in errs[:30]:
    print("  -", e)
print("=" * 68)
sys.exit(0 if not errs else 1)
