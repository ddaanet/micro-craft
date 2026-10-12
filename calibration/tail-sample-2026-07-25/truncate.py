"""Price each candidate truncation point.

Packs the untriaged ranking into batches the way `triage` would
(BATCH_ITEMS items or BATCH_CHARS of rendered thread, whichever binds
first) and reports spawns saved against signal forgone. Item size is
estimated from heat metrics, calibrated against the 54 items whose real
rendered size the sample measured.
"""

import csv
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
CORPUS = HERE.parents[1] / "corpus"
BATCH_ITEMS = 12
BATCH_CHARS = 200_000

rows = list(csv.DictReader(open(HERE / "heat.csv")))
con = sqlite3.connect(CORPUS / "cache.sqlite")
routed = {n for (n,) in con.execute("select i.number from route r join issue_or_pr i on i.id = r.item_id")}
untriaged = [r for r in rows if int(r["number"]) not in routed]

# Calibrate chars ~= a + b*comments from the 54 measured renders, so the
# packing runs on the whole corpus rather than on the sample alone.
measured = json.loads((HERE / "sample.json").read_text())
by_num = {int(r["number"]): r for r in rows}
xs = [(int(by_num[m["number"]]["comments"]), m["chars"]) for m in measured]
n = len(xs)
mx = sum(x for x, _ in xs) / n
my = sum(y for _, y in xs) / n
b = sum((x - mx) * (y - my) for x, y in xs) / sum((x - mx) ** 2 for x, _ in xs)
a = my - b * mx
print(f"size model: chars ~= {a:.0f} + {b:.0f} * comments  (n={n})")


def spawns(items: list[dict[str, str]]) -> int:
    count, cur_items, cur_chars = 1, 0, 0.0
    for r in items:
        size = max(500.0, a + b * int(r["comments"]))
        if cur_items + 1 > BATCH_ITEMS or cur_chars + size > BATCH_CHARS:
            count += 1
            cur_items, cur_chars = 0, 0.0
        cur_items += 1
        cur_chars += size
    return count


full = spawns(untriaged)
print(f"full sweep: {len(untriaged)} items, {full} spawns\n")

# Signal rate per stratum, as measured.
rates = [0.50, 0.67, 0.33, 0.83, 0.33, 0.0, 0.0, 0.0]
band = len(untriaged) / 8
total_signal = sum(r * band for r in rates)

print(f"{'cut at':>14} {'items':>6} {'spawns':>7} {'saved':>7}  {'signal kept':>12}")
for thresh in [24, 15, 11, 9, 8, 7, 6, 5, 4, 3, 2]:
    kept = [r for r in untriaged if float(r["score"]) >= thresh]
    if not kept:
        continue
    s = spawns(kept)
    # Which strata does this cut fall inside?
    frac = len(kept) / len(untriaged)
    got, acc = 0.0, 0.0
    for i, rate in enumerate(rates):
        lo, hi = i / 8, (i + 1) / 8
        overlap = max(0.0, min(frac, hi) - lo)
        got += rate * overlap * len(untriaged)
    print(
        f"  score >= {thresh:>3} {len(kept):>6} {s:>7} {full - s:>6}  "
        f"{got / total_signal:>11.0%}"
    )
