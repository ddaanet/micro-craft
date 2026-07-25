"""Fold the three raters' verdicts into the no-signal-versus-heat curve.

Reads verdicts-{A,B,C}.md (the raters' blocks, pasted verbatim) and
sample.json. Prints the per-stratum signal rate, the calibration check
against the pilot's known verdicts, and the projected yield of
truncating the sweep at each stratum boundary.
"""

import json
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
items = {p["slot"]: p for p in json.loads((HERE / "sample.json").read_text())}

BLOCK = re.compile(
    r"slot:\s*(\d+).*?verdict:\s*(signal|no-signal).*?"
    r"topic:\s*(\S+).*?confidence:\s*(high|medium|low).*?why:\s*(.+?)$",
    re.S | re.M,
)


def parse(rater: str) -> dict[int, dict[str, str]]:
    text = (HERE / f"verdicts-{rater}.md").read_text()
    out = {}
    for chunk in re.split(r"\n(?=slot:)", text):
        m = BLOCK.search(chunk)
        if m:
            slot, verdict, topic, conf, why = m.groups()
            out[int(slot)] = {
                "verdict": verdict,
                "topic": topic,
                "confidence": conf,
                "why": why.strip().splitlines()[0],
                "rater": rater,
            }
    return out


calls: dict[int, dict[str, str]] = {}
for r in "ABC":
    got = parse(r)
    print(f"rater {r}: {len(got)} verdicts")
    calls.update(got)

missing = sorted(set(items) - set(calls))
if missing:
    print(f"!! missing verdicts for slots {missing}")

by_stratum = defaultdict(list)
for slot, call in calls.items():
    by_stratum[items[slot]["stratum"]].append((slot, call))

print("\n== calibration (CAL, truth from the pilot) ==")
hits = 0
cal = by_stratum.get("CAL", [])
for slot, call in sorted(cal):
    truth = items[slot]["truth"]
    ok = truth == call["verdict"]
    hits += ok
    print(
        f"  #{items[slot]['number']:<5} truth={truth:<9} called={call['verdict']:<9} "
        f"{'ok' if ok else 'MISS'}  ({call['confidence']})"
    )
if cal:
    print(f"  agreement {hits}/{len(cal)}")

print("\n== signal rate by stratum ==")
print(f"  {'stratum':8} {'ranks':>13} {'score':>12}  {'signal':>7}  rate")
strata = [s for s in sorted(by_stratum) if s != "CAL"]
for s in strata:
    grp = by_stratum[s]
    n = len(grp)
    sig = sum(c["verdict"] == "signal" for _, c in grp)
    ranks = [items[slot]["rank"] for slot, _ in grp]
    scores = [items[slot]["score"] for slot, _ in grp]
    bar = "#" * sig + "." * (n - sig)
    print(
        f"  {s:8} {min(ranks):5}-{max(ranks):<7} "
        f"{min(scores):5.1f}-{max(scores):<5.1f}  {sig}/{n:<5}  {bar} {sig / n:.0%}"
    )

print("\n== low-confidence calls by stratum ==")
for s in strata:
    grp = by_stratum[s]
    low = sum(c["confidence"] == "low" for _, c in grp)
    print(f"  {s:8} {low}/{len(grp)}")

print("\n== truncation: cut the sweep after stratum N ==")
total_untriaged = 3847
band = total_untriaged / len(strata)
cum_sig = 0.0
all_sig = sum(
    sum(c["verdict"] == "signal" for _, c in by_stratum[s]) / len(by_stratum[s]) * band
    for s in strata
)
for i, s in enumerate(strata, 1):
    grp = by_stratum[s]
    rate = sum(c["verdict"] == "signal" for _, c in grp) / len(grp)
    cum_sig += rate * band
    items_swept = int(i * band)
    print(
        f"  after {s}: sweep {items_swept:>5} items ({items_swept / total_untriaged:>4.0%}), "
        f"harvest ~{cum_sig:>5.0f} signal items "
        f"({cum_sig / all_sig if all_sig else 0:>4.0%} of total signal)"
    )

print("\n== proposed new topics ==")
new = defaultdict(list)
for slot, call in calls.items():
    if call["topic"].startswith("new:"):
        new[call["topic"][4:]].append(items[slot]["number"])
for name, nums in sorted(new.items(), key=lambda kv: -len(kv[1])):
    print(f"  {name:40} {nums}")
