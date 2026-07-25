"""Draw the read-only weight-calibration sample.

Five blocks, each earning its keep, and every item's draw probability
recorded so the analysis can weight back to the corpus:

- CONTRAST: uniform over *distinct metric vectors*, then one item
  uniform inside the chosen class. The corpus holds 3847 untriaged
  items across only 1917 distinct vectors, so drawing items uniformly
  spends a sixth of the budget re-measuring one point in metric space.
  Drawing vectors uniformly spends it on spread instead, which is what
  a five-parameter fit is short of.
- PLATEAU: the six largest degenerate classes, four draws each. Those
  1131 items are 29% of the corpus and no non-negative reweighting can
  reorder them, so their conditional signal rate is exactly what the
  truncation decision turns on — and it is what the tail sample
  measured with only 18 items.
- UNIFORM: plain uniform over the untriaged corpus. A design-free
  reference: it estimates the base rate without leaning on the
  inverse-probability weights the other two blocks need.
- CAL: the pilot's own verdicts, mixed in blind, as in the tail sample.
- REPLICATE: six tail-sample items re-rated, and six fresh draws shown
  twice. Label noise attenuates fitted coefficients, so its size has to
  be measured rather than assumed — the tail sample's 3/6 CAL agreement
  said it is not small.

Deliberately *not* stratified on the composite score. Stratifying on a
covariate leaves logistic-regression slopes unbiased, so the tail
sample's design was not wrong for a fit — but it fixes the spread of
the score itself, which is the one quantity whose ranking quality we
want to compare against its parts.

Read-only: reads the heat CSV and the sqlite mirror's route table,
writes only sample.json. Touches no ledger and no dispatch state.
"""

import csv
import json
import random
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
CORPUS = HERE.parents[3] / "corpus"
PRIOR = HERE.parent / "tail-sample-2026-07-25"
SEED = 202607252
METRICS = ["comments", "reactions", "participants", "related_items", "span_years"]

CONTRAST = 110
PLATEAU_CLASSES, PLATEAU_EACH = 6, 4
UNIFORM = 16
CAL = 6
REPLICATE_PRIOR, REPLICATE_FRESH = 6, 6

# The tail sample's adjudication of the pilot's three `no-signal` calls,
# from docs/ghmem-tail-sample.md. #1445 is a confirmed pilot error: an
# owner ruling on `.v` detection buried under forty comments of flamewar.
# Carried alongside the pilot's verdict, not instead of it, so a rater
# disagreeing with the pilot can be scored against both readings.
ADJUDICATED = {1445: "signal", 3795: "signal", 3783: "no-signal"}

rows = list(csv.DictReader(open(HERE / "heat.csv")))
by_num = {int(r["number"]): r for r in rows}

con = sqlite3.connect(CORPUS / "cache.sqlite")
routed = dict(
    con.execute(
        "select i.number, r.verdict from route r join issue_or_pr i on i.id = r.item_id"
    )
)
untriaged = [r for r in rows if int(r["number"]) not in routed]
assert len(untriaged) + len(routed) == len(rows), (len(untriaged), len(routed))

classes: dict[tuple[float, ...], list[dict[str, str]]] = {}
for r in untriaged:
    classes.setdefault(tuple(round(float(r[m]), 3) for m in METRICS), []).append(r)
ranked_classes = sorted(classes, key=lambda k: (-len(classes[k]), k))

rng = random.Random(SEED)
picked: list[dict[str, object]] = []
taken: set[int] = set()


def add(row: dict[str, str], block: str, inclusion: float, **extra: object) -> None:
    """Record one drawn item with the probability of its being drawn.

    `inclusion` is this item's probability of landing in the sample at
    all under its block's scheme — not the per-draw probability — so
    `weight`, its reciprocal, is the number of corpus items the draw
    stands for and a block's weights sum to the population it covers.
    That is 3847 for CONTRAST and UNIFORM, and 1131 for PLATEAU, which
    covers only its six classes; the blocks are therefore separate
    estimators of overlapping populations, never pooled into one
    weighted total.
    """
    num = int(row["number"])
    taken.add(num)
    picked.append(
        {
            "number": num,
            "title": row["title"],
            "score": float(row["score"]),
            "rank": rows.index(row),
            **{m: float(row[m]) for m in METRICS},
            "block": block,
            "inclusion": inclusion,
            "weight": 1.0 / inclusion,
            "truth": None,
            **extra,
        }
    )


# CONTRAST — uniform over distinct vectors, then uniform within class.
for key in rng.sample(ranked_classes, CONTRAST):
    members = [r for r in classes[key] if int(r["number"]) not in taken]
    add(
        rng.choice(members),
        "CONTRAST",
        CONTRAST / len(ranked_classes) / len(classes[key]),
        cls_size=len(classes[key]),
    )

# PLATEAU — the largest degenerate classes, four items each.
for key in ranked_classes[:PLATEAU_CLASSES]:
    members = [r for r in classes[key] if int(r["number"]) not in taken]
    for r in rng.sample(members, PLATEAU_EACH):
        add(r, "PLATEAU", PLATEAU_EACH / len(classes[key]), cls_size=len(classes[key]))

# UNIFORM — design-free reference over the whole untriaged corpus.
pool = [r for r in untriaged if int(r["number"]) not in taken]
for r in rng.sample(pool, UNIFORM):
    add(r, "UNIFORM", UNIFORM / len(untriaged))

# CAL — known verdicts from the pilot, mixed in blind.
no_sig = sorted(n for n, v in routed.items() if v == "no-signal")
sig = sorted(n for n, v in routed.items() if v != "no-signal")
for n in no_sig[:3] + rng.sample(sig, CAL - 3):
    add(
        by_num[n],
        "CAL",
        1.0,
        truth="no-signal" if routed[n] == "no-signal" else "signal",
        adjudicated=ADJUDICATED.get(n),
    )

# REPLICATE — six tail-sample items carrying run-1 labels, plus six of
# this run's own draws shown a second time. Both halves measure label
# noise; the first also checks the two runs against each other.
prior = json.loads((PRIOR / "sample.json").read_text())
prior_labels = json.loads((HERE / "prior-labels.json").read_text())
eligible = [p for p in prior if str(p["number"]) in prior_labels]
for p in rng.sample(eligible, REPLICATE_PRIOR):
    add(
        by_num[p["number"]],
        "REPLICATE",
        1.0,
        run1=prior_labels[str(p["number"])],
        run1_stratum=p["stratum"],
    )
fresh = [p for p in picked if p["block"] in ("CONTRAST", "PLATEAU", "UNIFORM")]
for p in rng.sample(fresh, REPLICATE_FRESH):
    picked.append({**p, "block": "REPLICATE", "replicate_of": p["number"]})

order = list(range(len(picked)))
rng.shuffle(order)
for slot, i in enumerate(order):
    picked[i]["slot"] = slot + 1
picked.sort(key=lambda p: p["slot"])

out = HERE / "sample.json"
out.write_text(json.dumps(picked, indent=2) + "\n")
distinct = len({p["number"] for p in picked})
print(f"{len(picked)} slots over {distinct} distinct items -> {out}")
print(f"corpus: {len(untriaged)} untriaged across {len(ranked_classes)} metric vectors")
for b in ("CONTRAST", "PLATEAU", "UNIFORM", "CAL", "REPLICATE"):
    grp = [p for p in picked if p["block"] == b]
    if not grp:
        continue
    ranks = [p["rank"] for p in grp]
    scores = [p["score"] for p in grp]
    print(
        f"  {b:10} n={len(grp):<4} ranks {min(ranks):>4}-{max(ranks):<4} "
        f"score {min(scores):>5.1f}-{max(scores):<6.1f} "
        f"weight {min(p['weight'] for p in grp):>6.1f}-"
        f"{max(p['weight'] for p in grp):<7.1f}"
    )
