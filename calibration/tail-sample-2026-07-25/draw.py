"""Draw the read-only stratified tail sample.

Reads the heat ranking (CSV) and the sqlite mirror's route table.
Writes sample.json: the stratum assignment plus a blind, shuffled
presentation order. Touches no ledger and no dispatch state.
"""

import csv
import json
import random
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
CORPUS = HERE.parents[1] / "corpus"
SEED = 20260725
STRATA = 8
PER_STRATUM = 6
CALIBRATION = 6

rows = list(csv.DictReader(open(HERE / "heat.csv")))

con = sqlite3.connect(CORPUS / "cache.sqlite")
routed = {
    num: verdict
    for num, verdict in con.execute(
        "select i.number, r.verdict from route r join issue_or_pr i on i.id = r.item_id"
    )
}

untriaged = [r for r in rows if int(r["number"]) not in routed]
assert len(untriaged) + len(routed) == len(rows), (len(untriaged), len(routed))

rng = random.Random(SEED)
picked = []

band = len(untriaged) / STRATA
for s in range(STRATA):
    lo, hi = int(s * band), int((s + 1) * band)
    for r in rng.sample(untriaged[lo:hi], PER_STRATUM):
        picked.append(
            {
                "number": int(r["number"]),
                "title": r["title"],
                "score": float(r["score"]),
                "rank": rows.index(r),
                "stratum": f"S{s + 1}",
                "band": [lo, hi],
                "truth": None,
            }
        )

# Calibration: known verdicts from the pilot, mixed in blind. All three
# known no-signal items plus three routed ones, so both directions are
# tested.
no_sig = sorted(n for n, v in routed.items() if v == "no-signal")
sig = sorted(n for n, v in routed.items() if v != "no-signal")
cal = no_sig[:3] + rng.sample(sig, CALIBRATION - 3)
by_num = {int(r["number"]): r for r in rows}
for n in cal:
    r = by_num[n]
    picked.append(
        {
            "number": n,
            "title": r["title"],
            "score": float(r["score"]),
            "rank": rows.index(r),
            "stratum": "CAL",
            "band": None,
            "truth": "no-signal" if routed[n] == "no-signal" else "signal",
        }
    )

order = list(range(len(picked)))
rng.shuffle(order)
for slot, i in enumerate(order):
    picked[i]["slot"] = slot + 1
picked.sort(key=lambda p: p["slot"])

out = HERE / "sample.json"
out.write_text(json.dumps(picked, indent=2) + "\n")
print(f"{len(picked)} items -> {out}")
for s in [f"S{i + 1}" for i in range(STRATA)] + ["CAL"]:
    grp = [p for p in picked if p["stratum"] == s]
    lo = min(p["rank"] for p in grp)
    hi = max(p["rank"] for p in grp)
    print(
        f"  {s:4} n={len(grp)} ranks {lo}-{hi} "
        f"scores {min(p['score'] for p in grp):.1f}-{max(p['score'] for p in grp):.1f}"
    )
