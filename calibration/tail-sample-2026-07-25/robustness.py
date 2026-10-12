"""How much of the truncation recommendation survives recalibration?

`HEAT_WEIGHTS` is provisional, so a threshold stated in score units is
not durable. This asks the question that is: under a wide range of
alternative weight vectors, does the *set* of items a 2601-item budget
drops stay the same set?
"""

import csv
import random
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
CORPUS = HERE.parents[1] / "corpus"
BASE = {
    "comments": 1.0,
    "reactions": 0.5,
    "participants": 2.0,
    "related_items": 3.0,
    "span_years": 1.0,
}
KEEP = 2601
METRICS = list(BASE)

rows = list(csv.DictReader(open(HERE / "heat.csv")))
con = sqlite3.connect(CORPUS / "cache.sqlite")
routed = {n for (n,) in con.execute("select i.number from route r join issue_or_pr i on i.id = r.item_id")}
items = [
    (int(r["number"]), {m: float(r[m]) for m in METRICS})
    for r in rows
    if int(r["number"]) not in routed
]


def top(weights: dict[str, float], k: int = KEEP) -> set[int]:
    scored = sorted(
        items, key=lambda it: (-sum(weights[m] * it[1][m] for m in METRICS), it[0])
    )
    return {n for n, _ in scored[:k]}


base_keep = top(BASE)
base_drop = {n for n, _ in items} - base_keep
print(f"baseline: keep {len(base_keep)}, drop {len(base_drop)}\n")

# The structural floor: an item with no comments, no reactions and no
# cross-refs cannot be lifted by any non-negative reweighting of those
# three. Only participants and span can move it, and both are tiny here.
inert = [
    n
    for n, m in items
    if m["comments"] == 0 and m["reactions"] == 0 and m["related_items"] == 0
]
print(f"items with 0 comments, 0 reactions, 0 related_items: {len(inert)}")
print(f"  ... of which the baseline already drops: {len(set(inert) & base_drop)}\n")

named = {
    "all metrics equal": dict.fromkeys(METRICS, 1.0),
    "comments only": {**dict.fromkeys(METRICS, 0.0), "comments": 1.0},
    "participants only": {**dict.fromkeys(METRICS, 0.0), "participants": 1.0},
    "reactions only": {**dict.fromkeys(METRICS, 0.0), "reactions": 1.0},
    "related_items only": {**dict.fromkeys(METRICS, 0.0), "related_items": 1.0},
    "span only": {**dict.fromkeys(METRICS, 0.0), "span_years": 1.0},
    "discussion-heavy": {"comments": 3.0, "reactions": 1.0, "participants": 3.0, "related_items": 0.5, "span_years": 0.5},
    "demand-heavy": {"comments": 0.5, "reactions": 3.0, "participants": 0.5, "related_items": 0.5, "span_years": 0.5},
}
print(f"{'weight vector':22} {'kept-set overlap':>17} {'newly kept':>11}")
for name, w in named.items():
    k = top(w)
    print(f"  {name:20} {len(k & base_keep) / KEEP:>16.0%} {len(k - base_keep):>11}")

# Random perturbation: each weight independently scaled over [1/4, 4].
rng = random.Random(20260725)
overlaps = []
for _ in range(200):
    w = {m: BASE[m] * 4 ** rng.uniform(-1, 1) for m in METRICS}
    overlaps.append(len(top(w) & base_keep) / KEEP)
overlaps.sort()
print(
    f"\n200 random reweightings (each weight scaled over [1/4, 4]):\n"
    f"  kept-set overlap  min {overlaps[0]:.0%}  "
    f"p05 {overlaps[10]:.0%}  median {overlaps[100]:.0%}  max {overlaps[-1]:.0%}"
)

# The decision-relevant question: could a reweighting promote items the
# sample never looked at into the kept set, in bulk?
union_kept: set[int] = set()
for _ in range(200):
    w = {m: BASE[m] * 4 ** rng.uniform(-1, 1) for m in METRICS}
    union_kept |= top(w)
print(
    f"  items kept under at least one reweighting: {len(union_kept)} "
    f"({len(union_kept) - KEEP} beyond the baseline set)"
)
print(f"  items dropped under every reweighting:    {len({n for n, _ in items} - union_kept)}")
