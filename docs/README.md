# docs/ — ブラウザ版

`app/index.html` の写しです（データ埋め込みの自己完結 1 枚なので、そのまま配れます）。
GitHub Pages は `main` の `/docs` を配信元にしています。

更新するとき:

```
cp app/index.html docs/index.html && git add docs && git commit -m "docs: sync browser build" && git push
```
