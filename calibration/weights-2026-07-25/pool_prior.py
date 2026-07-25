"""Pool the tail sample's 54 labels forward into this run.

Legitimate because the heat CSV is byte-identical between the two runs
— same ranking, same metric vectors — so a run-1 label attaches to the
same feature row a run-2 label would. The two draws used different
schemes, which the fit handles through each item's recorded `weight`
rather than by pretending one scheme produced both.

Run-1 CAL items are dropped: they are routed, so they are not part of
the untriaged population being modelled, and their labels are what
run 2's own CAL block re-measures.

Writes prior-labels.json, which draw.py reads for its REPLICATE block
and fit.py reads as extra rows.
"""

import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
PRIOR = HERE.parent / "tail-sample-2026-07-25"
METRICS = ["comments", "reactions", "participants", "related_items", "span_years"]

rows = {int(r["number"]): r for r in csv.DictReader(open(HERE / "heat.csv"))}
items = {p["slot"]: p for p in json.loads((PRIOR / "sample.json").read_text())}

BLOCK = re.compile(
    r"slot:\s*(\d+).*?verdict:\s*(signal|no-signal).*?"
    r"topic:\s*(\S+).*?confidence:\s*(high|medium|low)",
    re.DOTALL,
)

out: dict[str, dict[str, object]] = {}
for rater in "ABC":
    text = (PRIOR / f"verdicts-{rater}.md").read_text()
    for chunk in re.split(r"\n(?=slot:)", text):
        m = BLOCK.search(chunk)
        if not m:
            continue
        slot, verdict, topic, conf = m.groups()
        p = items[int(slot)]
        if p["stratum"] == "CAL":
            continue
        r = rows[p["number"]]
        # Run 1 drew eight rank-uniform strata of six from 3847 items,
        # so every item in it stood for 3847/48 of the corpus.
        out[str(p["number"])] = {
            "verdict": verdict,
            "topic": topic,
            "confidence": conf,
            "rater": rater,
            "stratum": p["stratum"],
            "weight": 3847 / 48,
            **{k: float(r[k]) for k in METRICS},
            "score": float(r["score"]),
        }

(HERE / "prior-labels.json").write_text(
    json.dumps(out, indent=2, sort_keys=True) + "\n"
)
sig = sum(1 for v in out.values() if v["verdict"] == "signal")
print(f"{len(out)} run-1 labels pooled ({sig} signal, {len(out) - sig} no-signal)")
