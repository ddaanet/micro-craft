"""Render every sampled item and record its size, so the classifier's
context budget is known before dispatch. Read-only: `ghmem show` only."""

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
items = json.loads((HERE / "sample.json").read_text())
renders = HERE / "renders"
renders.mkdir(exist_ok=True)

tot: dict[str, list[int]] = {}
for p in items:
    out = subprocess.run(
        ["ghmem", "show", str(p["number"])], capture_output=True, text=True
    )
    if out.returncode:
        print("FAIL", p["number"], out.stderr[:200])
        continue
    (renders / f"{p['slot']:02d}-{p['number']}.md").write_text(out.stdout)
    p["chars"] = len(out.stdout)
    tot.setdefault(p["stratum"], []).append(p["chars"])

(HERE / "sample.json").write_text(json.dumps(items, indent=2) + "\n")

grand = 0
for s in sorted(tot):
    v = sorted(tot[s])
    grand += sum(v)
    print(f"{s:4} total={sum(v):>7} min={v[0]:>6} med={v[len(v) // 2]:>6} max={v[-1]:>7}")
print(f"GRAND {grand} chars ~= {grand // 4} tokens")
