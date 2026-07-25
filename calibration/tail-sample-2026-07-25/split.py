"""Split the sample across three classifiers, two items per stratum
each, so every rater sees the whole heat range and cross-stratum
comparison stays within one rater."""

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
items = json.loads((HERE / "sample.json").read_text())

by_stratum = defaultdict(list)
for p in items:
    by_stratum[p["stratum"]].append(p)

assign = defaultdict(list)
for stratum in sorted(by_stratum):
    for i, p in enumerate(sorted(by_stratum[stratum], key=lambda q: q["slot"])):
        assign["ABC"[i % 3]].append(p)

for rater in "ABC":
    group = sorted(assign[rater], key=lambda p: p["slot"])
    lines = []
    for p in group:
        lines.append(f"- slot {p['slot']}: item {p['number']} — renders/{p['slot']:02d}-{p['number']}.md")
    (HERE / f"worklist-{rater}.md").write_text("\n".join(lines) + "\n")
    chars = sum(p["chars"] for p in group)
    print(f"{rater}: {len(group)} items, {chars} chars (~{chars // 4} tokens)")

(HERE / "assignment.json").write_text(
    json.dumps({r: [p["slot"] for p in sorted(assign[r], key=lambda q: q["slot"])] for r in "ABC"}, indent=2) + "\n"
)
