#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L（文書の記述と実際の食い違い）を機械で数える。usage: lint_docs.py
1) 古い文字列が残っていないこと（(file, 文字列) の一覧）
2) README に貼った 2 つの差分が `diff -u` の出力と一致すること
違反 0 なら L = 0。
"""
import sys, os, re, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(BASE))

STALE = [
    ("data_v61.py", "出典の文だけ書き換えた"),
    ("LT計測手順_v1.2.md", "線形（〜多項式の低次）"),
    ("LT計測手順_v1.2.md", "多項式は `F_1`〜`F_2` の間"),
    ("LT計測手順_v1.2.md", "data_v6.py"),
    ("LT計測手順_v1.2.md", "data_cal_v7.py"),
    ("LT計測手順_v1.2.md", "97_gen_v7"),
    ("LT計測手順_v1.2.md", "98_t7"),
    ("Forb-LT一覧表.md", "97_gen_v7"),
    ("Forb-LT一覧表.md", "99_check_v7"),
    ("Forb-LT一覧表.md", "LT計測手順_v1.1"),
    ("check.py", "usage: check.py <v7"),
    ("build_release.sh", "python3 table_build"),
    ("README.md", "# Forb-LT 一覧表 v1.0（2026-11-05）"),
]

def read(f):
    return open(os.path.join(BASE, f), encoding="utf-8").read()

def diff_block(doc, label):
    i = doc.find(label)
    if i < 0: return None
    j = doc.find("```diff", i)
    k = doc.find("```", j + 7)
    return doc[j + 7:k].strip("\n")

def check():
    fails = []
    for f, s in STALE:
        if s in read(f):
            fails.append("%s に古い文字列「%s」" % (f, s))
    readme = read("README.md")
    # 比較の基準は同梱の ref/（fix/v6.1 と v5.1 の原本のバイト一致の写し）。
    # クリーンな複製（一時ディレクトリ）でも同じ検査が走る。
    d1 = subprocess.run(["diff", "-u", "--label", "fix/v6.1/data_v6.py", "--label", "v1.8/data_v61.py",
                         os.path.join(BASE, "ref", "v6.1_data_v6.py"), os.path.join(BASE, "data_v61.py")],
                        capture_output=True, text=True).stdout.rstrip("\n")
    d2 = subprocess.run(["diff", "-u", "--label", "v5.1/src_v5_1.py", "--label", "v1.8/data_base.py",
                         os.path.join(BASE, "ref", "v5.1_src_v5_1.py"), os.path.join(BASE, "data_base.py")],
                        capture_output=True, text=True).stdout.rstrip("\n")
    b1 = diff_block(readme, "`fix/v6.1/data_v6.py` と `data_v61.py`:")
    b2 = diff_block(readme, "`src_v5_1.py`（v5.1 の原本）と")
    if b1 != d1: fails.append("README の 1 つ目の差分が diff -u と一致しない")
    if b2 != d2: fails.append("README の 2 つ目の差分が diff -u と一致しない")
    return fails

def main():
    fails = check()
    print("== L（文書と実際の食い違い） ==")
    print("L = %d 件（検査 %d 項目＋差分 2 件）" % (len(fails), len(STALE)))
    for f in fails:
        print("  -", f)
    return 0 if not fails else 1

if __name__ == "__main__":
    sys.exit(main())
