#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""index.html の `const DATA = {...};` を data.json で置き換える（自己完結のまま）。
usage: embed_data.py <index.html>
"""
import sys, json, os

def main(p):
    h = open(p, encoding="utf-8").read()
    d = open(os.path.join(os.path.dirname(p), "data.json"), encoding="utf-8").read()
    d = json.loads(d)
    i = h.index("const DATA = ")
    j = h.index(";\n", i)
    h = h[:i] + "const DATA = " + json.dumps(d, ensure_ascii=False) + h[j:]
    open(p, "w", encoding="utf-8").write(h)
    print("embedded: %d rows, %d cal" % (len(d["rows"]), len(d["cal"])))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
