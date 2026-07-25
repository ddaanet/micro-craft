"""Render every sampled item once and record its size.

Read-only: `ghmem show` only. Renders are keyed by item number rather
than by slot, because REPLICATE shows six items to a second rater and
the two slots must read the identical bytes — a replicate that re-runs
`ghmem show` would be measuring the renderer as well as the rater.
"""

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
items = json.loads((HERE / "sample.json").read_text())
renders = HERE / "renders"
renders.mkdir(exist_ok=True)

sizes: dict[int, int] = {}
for p in items:
    num = int(p["number"])
    if num not in sizes:
        out = subprocess.run(
            ["ghmem", "show", str(num)], capture_output=True, text=True, check=False
        )
        if out.returncode:
            print("FAIL", num, out.stderr[:200])
            continue
        (renders / f"{num}.md").write_text(out.stdout)
        sizes[num] = len(out.stdout)
    p["chars"] = sizes[num]

(HERE / "sample.json").write_text(json.dumps(items, indent=2) + "\n")

by_block: dict[str, list[int]] = {}
for p in items:
    by_block.setdefault(str(p["block"]), []).append(int(p["chars"]))

grand = 0
for b in sorted(by_block):
    v = sorted(by_block[b])
    grand += sum(v)
    print(
        f"{b:10} n={len(v):<4} total={sum(v):>8} min={v[0]:>6} "
        f"med={v[len(v) // 2]:>6} max={v[-1]:>7}"
    )
print(f"GRAND {grand} chars over {len(sizes)} renders ~= {grand // 4} tokens")
