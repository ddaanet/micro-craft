"""Which heat metrics actually separate signal from no-signal?

The sample is 54 items carrying both a full metric vector and a signal
label produced without routing, which makes it the first evidence in
the project that could speak to the heat weights themselves rather than
to a threshold on them. n=54 is thin — this is a direction check, not a
fit.
"""

import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
METRICS = ["comments", "reactions", "participants", "related_items", "span_years"]

rows = {int(r["number"]): r for r in csv.DictReader(open(HERE / "heat.csv"))}
items = {p["slot"]: p for p in json.loads((HERE / "sample.json").read_text())}

labels: dict[int, str] = {}
for rater in "ABC":
    for chunk in re.split(r"\n(?=slot:)", (HERE / f"verdicts-{rater}.md").read_text()):
        m = re.search(r"slot:\s*(\d+).*?verdict:\s*(signal|no-signal)", chunk, re.S)
        if m:
            labels[items[int(m.group(1))]["number"]] = m.group(2)

sig = [rows[n] for n, v in labels.items() if v == "signal"]
non = [rows[n] for n, v in labels.items() if v == "no-signal"]
print(f"signal {len(sig)}  no-signal {len(non)}\n")


def med(group: list[dict[str, str]], metric: str) -> float:
    vals = sorted(float(r[metric]) for r in group)
    return vals[len(vals) // 2] if vals else 0.0


print(f"{'metric':16} {'median signal':>14} {'median no-signal':>17} {'separation':>11}")
for m in METRICS:
    a, b = med(sig, m), med(non, m)
    ratio = f"{a / b:.1f}x" if b else ("inf" if a else "—")
    print(f"  {m:14} {a:>14.1f} {b:>17.1f} {ratio:>11}")

# Single-metric ranking quality: if we sorted the 54 by one metric alone,
# how much signal lands in the top half? A metric that cannot beat the
# 39% base rate is not earning its weight.
print(f"\nbase rate: {len(sig) / (len(sig) + len(non)):.0%} signal")
print(f"{'sort by':16} {'signal in top half':>19}")
for m in METRICS + ["current heat score"]:
    key = "score" if m == "current heat score" else m
    ranked = sorted(labels, key=lambda n: -float(rows[n][key]))
    half = ranked[: len(ranked) // 2]
    hits = sum(labels[n] == "signal" for n in half)
    print(f"  {m:14} {hits}/{len(half)} = {hits / len(half):>11.0%}")
