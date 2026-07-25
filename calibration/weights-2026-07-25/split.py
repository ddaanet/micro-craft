"""Split the 168 slots across seven raters.

Round-robin within each block, so every rater sees CONTRAST, PLATEAU,
UNIFORM and CAL items and no block's rate rests on one rater's
leniency. The block offsets rotate, so the rater who leads one block
does not lead the next.

Then the one hard constraint: a REPLICATE slot must not land on the
rater holding its original. A replicate rated twice by the same rater
measures nothing — the point is between-rater disagreement.
"""

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
RATERS = "ABCDEFG"

items = json.loads((HERE / "sample.json").read_text())
by_block: dict[str, list[dict[str, object]]] = defaultdict(list)
for p in items:
    by_block[str(p["block"])].append(p)

owner: dict[int, str] = {}
assign: dict[str, list[dict[str, object]]] = defaultdict(list)
offset = 0
# REPLICATE last: its constraint reads the assignments of the blocks its
# originals came from, so those have to be settled first.
for block in ["CONTRAST", "PLATEAU", "UNIFORM", "CAL", "REPLICATE"]:
    group = sorted(by_block[block], key=lambda q: int(str(q["slot"])))
    for i, p in enumerate(group):
        rater = RATERS[(offset + i) % len(RATERS)]
        if block == "REPLICATE":
            # Skip forward past the rater already holding this item —
            # for a replicate-of-prior there is no such rater, since the
            # original was rated in run 1.
            held = owner.get(int(str(p["number"])))
            step = 0
            while RATERS[(offset + i + step) % len(RATERS)] == held:
                step += 1
            rater = RATERS[(offset + i + step) % len(RATERS)]
        else:
            owner[int(str(p["number"]))] = rater
        p["rater"] = rater
        assign[rater].append(p)
    offset = (offset + len(group)) % len(RATERS)

for p in items:
    if p["block"] != "REPLICATE":
        continue
    dup = [q for q in items if q["number"] == p["number"] and q is not p]
    for q in dup:
        assert q["rater"] != p["rater"], (p["number"], p["rater"])

(HERE / "sample.json").write_text(json.dumps(items, indent=2) + "\n")

for rater in RATERS:
    group = sorted(assign[rater], key=lambda p: int(str(p["slot"])))
    lines = [
        f"- slot {p['slot']}: item {p['number']} — renders/{p['number']}.md"
        for p in group
    ]
    (HERE / f"worklist-{rater}.md").write_text("\n".join(lines) + "\n")
    chars = sum(int(str(p["chars"])) for p in group)
    blocks = defaultdict(int)
    for p in group:
        blocks[str(p["block"])[:4]] += 1
    mix = " ".join(f"{k}={v}" for k, v in sorted(blocks.items()))
    print(
        f"{rater}: {len(group):>3} slots, {chars:>7} chars (~{chars // 4:>6} tok)  {mix}"
    )

(HERE / "assignment.json").write_text(
    json.dumps(
        {
            r: [
                int(str(p["slot"]))
                for p in sorted(assign[r], key=lambda q: int(str(q["slot"])))
            ]
            for r in RATERS
        },
        indent=2,
    )
    + "\n"
)
