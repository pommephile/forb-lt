# Forb-LT — proof-theoretic strength, arithmetic hierarchy, and witness growth

A table of **known results** for 82 propositions, organised along three axes.

| Axis | What is recorded |
|---|---|
| **Axis A** | which theories prove the proposition, and which provably do not (an interval from the literature) |
| **Hierarchy** | the prenex form placed in the arithmetic hierarchy (Π₁, Π₂, Π¹₂, …) |
| **Axis B** | for Π₂ propositions, how the witness grows (an interval in the F_α hierarchy) |

**The table claims no new mathematics.** It transcribes published results, attributes each value, and marks what is unresolved. Empty cells mean "no value obtained", not "not applicable".

## Contents

```
table/   the table (82 rows) + a 10-row comparison table + generators and checkers (44 files)
note/    "Two types of independence" v2.2 — a short note splitting independence of Π₂
         statements into a growth type and an existence type
app/     Proposition Database — a macOS app (search, reverse lookup, draft checker)
audit/   seven rounds of external review (verdicts and history)
```

## Numbers

| Item | Value |
|---|---|
| Propositions | 82 (plus 10 comparison rows) |
| Hierarchy settled | 61 / 82 |
| Axis A upper bound known | 23 / 82 |
| Axis A lower bound known | 7 / 82 |
| Axis B upper bound (of 22 Π₂ rows) | 12 / 22 |
| Axis B lower bound | 8 / 22 |
| Both A and B known | 5 |
| Changes to any value, 1.0 → 1.8 | **0** |

## How to read Axis A

Intervals have the form `[lower, upper]`.

| Interval | Meaning |
|---|---|
| `[PA, PA+TI(ε₀)]` | unprovable in PA, provable in PA+TI(ε₀) — **independence established** |
| `[—, EFA]` | provable in EFA; whether a weaker theory proves it is open — **this is not independence** |
| `[IOpen, IΔ₀]` | not provable in IOpen; upper bound unknown |
| `未記入` | no value obtained from the literature |

Reading `[—, X]` as "independent" is the most common mistake. An upper bound alone proves nothing about independence. The draft checker in the app flags exactly this.

## Browser version

<https://pommephile.github.io/forb-lt/> — same single-file app, no install.

## macOS app

```
cd app
bash build_app.sh          # builds ~/Applications/Forb-LT.app (needs swiftc)
open -a ~/Applications/Forb-LT.app
```

A thin WKWebView shell around `app/index.html`. The page itself is self-contained, so it also runs from the file system.

- **List** — search by name, formula or source; filter by hierarchy and by Axis A status
- **Reverse lookup** — ten slices ("not provable in PA", "independence established", "upper bound only", …)
- **Draft check** — paste a draft; it finds the propositions you mention and warns when a sentence claims independence that the table does not support

## Verification

```
cd table && shasum -a 256 -c SHA256SUMS.published   # 44/44 OK
cd note  && shasum -a 256 -c SHA256SUMS             # 3/3 OK
```

`table/SHA256SUMS` is the freeze-time manifest. Two internal work orders had a local absolute path redacted for publication, so that manifest reports 2 FAILED; `table/PUBLISHED.md` lists both hashes (before and after).

## External review

Before publication the table went through seven rounds of external review (Codex CLI, `gpt-6.1-sol`, read-only). Six rounds returned "stop"; the seventh returned "proceed" with zero blockers. Every finding was reproduced locally before being fixed, and **no value was changed** across 1.2 → 1.8.

| Round | Target | Findings | Fixed in |
|---|---|---|---|
| 1 | 1.2 | 5 | 1.3 |
| 2 | 1.3 | 9 | 1.4 |
| 3 | 1.4 | 4 | 1.5 |
| 4 | 1.5 | 6 | 1.6 |
| 5 | 1.6 | 2 | 1.7 |
| 6 | 1.7 | 1 | 1.8 |
| 7 | 1.8 | **0 (proceed)** | — |

The verdict texts are in `audit/`.

## Known limitations

1. **Rows not fully reviewed**: about 50 of the 82 have been checked against the original sources for self-trivialisation, weakening and quantifier scope; the rest have only been read.
2. **C6** (hydra, height 3, fixed strategy τ): the source states the all-strategies version; transferring it to a fixed τ is unverified.
3. **C8** ATR₀ lower bound: Simpson 1985 not obtained.
4. Five primary sources were never obtained (Ketonen–Solovay 1981, Friedman–Robertson–Seymour 1987, Sakamoto–Yokoyama 2007, Simpson 1985, Hájek–Pudlák ch. II).
5. No new theorem is claimed, and no prediction is made.

## License

- Text, tables and data (`table/`, `note/`, `audit/`): **CC BY 4.0**
- Code (`app/`, `table/*.py`): **MIT**

Quoted definitions and theorem statements remain with their respective copyright holders. See `LICENSE`.

## Cite

```
Shin Uota, "Forb-LT: a table of proof-theoretic strength, arithmetic hierarchy,
and growth of witnesses for 82 propositions", version 1.8, 2026-11-06.
```
