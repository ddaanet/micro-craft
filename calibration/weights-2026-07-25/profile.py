"""Profile the metric space, to size the draw before drawing it.

The tail sample stratified on the composite score. That was right for a
question about where to truncate, and wrong for a question about the
weights: it fixes the spread of the very quantity under test. Choosing a
better design needs to know what the metric space actually looks like —
how degenerate it is, how correlated the metrics are, and how much of
the corpus carries no signal-bearing variation at all.
"""

import csv
import sqlite3
from itertools import combinations, pairwise
from pathlib import Path

HERE = Path(__file__).parent
CORPUS = HERE.parents[3] / "corpus"
METRICS = ["comments", "reactions", "participants", "related_items", "span_years"]

rows = list(csv.DictReader(open(HERE / "heat.csv")))
con = sqlite3.connect(CORPUS / "cache.sqlite")
routed = dict(
    con.execute(
        "select i.number, r.verdict from route r join issue_or_pr i on i.id = r.item_id"
    )
)
un = [r for r in rows if int(r["number"]) not in routed]
print(f"total {len(rows)}  routed {len(routed)}  untriaged {len(un)}")


def col(metric: str) -> list[float]:
    return [float(r[metric]) for r in un]


print("\n== marginal distribution over untriaged ==")
print(f"  {'metric':16}{'zero':>7}{'p50':>8}{'p75':>8}{'p90':>8}{'p99':>9}{'max':>9}")
for m in METRICS:
    v = sorted(col(m))
    z = sum(1 for x in v if x == 0)

    def q(p: float, v: list[float] = v) -> float:
        return v[min(len(v) - 1, int(p * len(v)))]

    print(
        f"  {m:14}{z:>7}{q(0.5):>8.1f}{q(0.75):>8.1f}"
        f"{q(0.90):>8.1f}{q(0.99):>9.1f}{v[-1]:>9.1f}"
    )

# Degeneracy. Weights can only order items that differ, so a metric
# space where thousands of items share one vector caps how much of the
# corpus any reweighting can rearrange.
vecs: dict[tuple[float, ...], list[int]] = {}
for r in un:
    vecs.setdefault(tuple(round(float(r[m]), 3) for m in METRICS), []).append(
        int(r["number"])
    )
print(f"\ndistinct metric vectors among untriaged: {len(vecs)}")
for k, v in sorted(vecs.items(), key=lambda kv: -len(kv[1]))[:6]:
    print(f"  {dict(zip(METRICS, k, strict=False))} -> {len(v)} items")

flat = [r for r in un if all(float(r[m]) == 0 for m in METRICS[:4])]
print(f"\nitems with comments=reactions=participants=related=0: {len(flat)}")


def pearson(a: list[float], b: list[float]) -> float:
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b, strict=False))
    da = sum((x - ma) ** 2 for x in a) ** 0.5
    db = sum((y - mb) ** 2 for y in b) ** 0.5
    return num / (da * db) if da and db else 0.0


print("\n== metric correlation over untriaged (Pearson) ==")
for a, b in combinations(METRICS, 2):
    print(f"  {a:15} {b:15} {pearson(col(a), col(b)):>6.2f}")

# The design will spread the draw over a coarse metric grid. How many
# items sit in each cell of a log-ish binning?
print("\n== items per coarse bin, per metric ==")
BINS = {
    "comments": [0, 1, 3, 8, 20, 10**9],
    "reactions": [0, 1, 3, 10, 40, 10**9],
    "participants": [0, 2, 3, 5, 9, 10**9],
    "related_items": [0, 1, 2, 4, 8, 10**9],
    "span_years": [0, 0.01, 0.5, 2, 5, 10**9],
}
for m, edges in BINS.items():
    v = col(m)
    counts = []
    for lo, hi in pairwise(edges):
        counts.append(sum(1 for x in v if lo <= x < hi))
    print(
        f"  {m:15} "
        + " ".join(
            f"[{lo:g},{hi:g})={c}"
            for (lo, hi, c) in zip(edges, edges[1:], counts, strict=False)
        )
    )
