#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公開ディレクトリのファイル一覧 = SHA256SUMS に載る一覧 ＋ SHA256SUMS、を確かめる。
usage: filelist_check.py [ディレクトリ]（既定はこのスクリプトのあるディレクトリ）
余計なファイル（__pycache__、古いログなど）があれば exit 1。
"""
import os, sys, hashlib

BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
SUMS = os.path.join(BASE, "SHA256SUMS")
listed = []
for line in open(SUMS, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line.strip():
        continue
    listed.append(line.split("  ", 1)[1])
actual = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [x for x in dirs if not x.startswith(".") and x != "__pycache__"]
    for f in files:
        if f.startswith("."):
            continue
        actual.append(os.path.relpath(os.path.join(root, f), BASE))
extra = sorted(set(actual) - set(listed) - {"SHA256SUMS"})
missing = sorted(set(listed) - set(actual))
print("== ファイル一覧（公開ディレクトリ = SHA256SUMS ＋ SHA256SUMS） ==")
print("SHA256SUMS に載る: %d / 実際: %d（SHA256SUMS を除く）" % (len(listed), len(actual) - 1))
print("余計なファイル: %d 件" % len(extra))
for x in extra:
    print("  +", x)
print("載っているが無い: %d 件" % len(missing))
for x in missing:
    print("  -", x)
bad = len(extra) + len(missing)
print("違反: %d 件" % bad)
return_code = 0 if bad == 0 else 1
sys.exit(return_code)
