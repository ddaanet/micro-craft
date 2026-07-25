"""Fit the heat weights from the labelled draw.

The scorer is linear in raw metric counts, so the fit is too: a
logistic regression's slopes drop straight into `HEAT_WEIGHTS` because
ranking by the linear predictor and ranking by the weighted sum are the
same ordering. Fitting some better-conditioned transform would produce
numbers that cannot be installed without changing the SQL.

Slopes come from the unweighted fit. The draw selected on the metrics
and never on the label, which leaves logistic slopes unbiased — only
the intercept moves — and the unweighted fit is the more efficient of
the two. The inverse-probability fit runs alongside as a check that the
design is not driving the answer.
"""

import json
import random
from math import log1p
from pathlib import Path

from labels import METRICS, load
from logistic import fit

HERE = Path(__file__).parent
RIDGE = 1.0
BOOTSTRAP = 400
CURRENT = {
    "comments": 1.0,
    "reactions": 0.5,
    "participants": 2.0,
    "related_items": 3.0,
    "span_years": 1.0,
}

rows, _, _ = load()
if not rows:
    raise SystemExit("no labelled rows yet — the raters have not returned")

x = [r.x for r in rows]
y = [r.y for r in rows]
w = [r.weight for r in rows]

by_block: dict[str, list[int]] = {}
for r in rows:
    by_block.setdefault(r.block.split("-")[0], []).append(r.y)
print(f"== dataset: {len(rows)} labelled items, {sum(y)} signal ==")
for b in sorted(by_block):
    v = by_block[b]
    print(
        f"  {b:10} n={len(v):<4} signal {sum(v):>3}/{len(v):<4} = {sum(v) / len(v):>4.0%}"
    )

plain = fit(x, y, ridge=RIDGE)
ipw = fit(x, y, ridge=RIDGE, weights=w)

rng = random.Random(20260725)
boot: list[list[float]] = []
for _ in range(BOOTSTRAP):
    idx = [rng.randrange(len(rows)) for _ in rows]
    if len({y[i] for i in idx}) < 2:
        continue
    try:
        boot.append(fit([x[i] for i in idx], [y[i] for i in idx], ridge=RIDGE).coef)
    except ValueError:
        continue


def pct(vals: list[float], p: float) -> float:
    v = sorted(vals)
    return v[min(len(v) - 1, int(p * len(v)))]


print(f"\n== fitted coefficients (ridge={RIDGE}, {len(boot)} bootstrap resamples) ==")
print(
    f"  {'metric':16}{'coef':>8}{'stderr':>8}{'boot 2.5%':>11}"
    f"{'boot 97.5%':>12}{'ipw coef':>10}{'current':>9}"
)
signs: dict[str, str] = {}
for j, m in enumerate(METRICS):
    lo = pct([b[j] for b in boot], 0.025)
    hi = pct([b[j] for b in boot], 0.975)
    signs[m] = "+" if lo > 0 else ("-" if hi < 0 else "0")
    print(
        f"  {m:16}{plain.coef[j]:>+8.3f}{plain.stderr[j]:>8.3f}"
        f"{lo:>+11.3f}{hi:>+12.3f}{ipw.coef[j]:>+10.3f}{CURRENT[m]:>9.1f}"
    )
print(f"  intercept {plain.intercept:+.3f}   loglik {plain.loglik:.1f}")
print("\n  sign at 95%: " + "  ".join(f"{m}={signs[m]}" for m in METRICS))

# A coefficient per raw unit is not comparable across metrics that
# differ by an order of magnitude in spread, and it says nothing about
# what this sample could have detected. Both columns below fix that:
# effect per standard deviation puts the five on one scale, and the
# minimum detectable effect says which zeros are findings and which are
# just an underpowered draw.
sd = []
for j in range(len(METRICS)):
    vals = [row[j] for row in x]
    mean = sum(vals) / len(vals)
    sd.append((sum((v - mean) ** 2 for v in vals) / len(vals)) ** 0.5)
print("\n== effect size and what the sample could detect ==")
print("  both effect columns are per standard deviation, so they compare")
print(f"  {'metric':16}{'sd in sample':>14}{'log-odds / sd':>16}{'min detectable':>16}")
for j, m in enumerate(METRICS):
    mde = 1.96 * plain.stderr[j] * sd[j]
    effect = plain.coef[j] * sd[j]
    mark = "" if abs(effect) > mde else "   under-powered"
    print(f"  {m:16}{sd[j]:>14.2f}{effect:>+16.3f}{mde:>+16.3f}{mark}")
print(
    "\n  A coefficient inside its own minimum detectable effect is not\n"
    "  evidence of no effect — only of an effect this draw cannot see."
)

# The scorer's weights are a direction, not a probability model: only
# the ratios between them affect the ranking. Rescaling to the current
# vector's total keeps the heat numbers in a familiar range, so a
# truncation table under new weights reads beside the old one.
CLAMP_NOTE = "clamped at 0 — a negative weight would rank a busier thread colder"
scale = sum(CURRENT.values())
pos = {m: max(plain.coef[j], 0.0) for j, m in enumerate(METRICS)}
norm = sum(pos.values())
fitted_weights = {m: round(v / norm * scale, 3) for m, v in pos.items()}

# The parsimonious alternative: zero every metric whose bootstrap
# interval straddles zero, rather than installing a number the sample
# cannot distinguish from nothing.
kept = {m: (pos[m] if signs[m] == "+" else 0.0) for m in METRICS}
knorm = sum(kept.values()) or 1.0
sparse_weights = {m: round(v / knorm * scale, 3) for m, v in kept.items()}

print("\n== weight vectors ==")
print(f"  {'metric':16}{'current':>9}{'fitted':>9}{'sparse':>9}")
for m in METRICS:
    print(
        f"  {m:16}{CURRENT[m]:>9.1f}{fitted_weights[m]:>9.3f}{sparse_weights[m]:>9.3f}"
    )
for j, m in enumerate(METRICS):
    if plain.coef[j] < 0:
        print(f"  note: {m} {CLAMP_NOTE}")

# Functional form. The scorer is linear in counts, which lets one
# 70-reaction thread outweigh forty two-reaction ones. If a log1p score
# ranks better out of sample, the defect is the shape and not just the
# weights — worth reporting even though acting on it means changing SQL.
logx = [[log1p(v) for v in row] for row in x]
log_fit = fit(logx, y, ridge=RIDGE)
print(f"\n  log1p-scale loglik {log_fit.loglik:.1f} vs raw {plain.loglik:.1f}")

out = {
    "n": len(rows),
    "signal": sum(y),
    "ridge": RIDGE,
    "coef": {m: plain.coef[j] for j, m in enumerate(METRICS)},
    "stderr": {m: plain.stderr[j] for j, m in enumerate(METRICS)},
    "boot_ci": {
        m: [pct([b[j] for b in boot], 0.025), pct([b[j] for b in boot], 0.975)]
        for j, m in enumerate(METRICS)
    },
    "ipw_coef": {m: ipw.coef[j] for j, m in enumerate(METRICS)},
    "sign95": signs,
    "fitted_weights": fitted_weights,
    "sparse_weights": sparse_weights,
    "loglik": {"raw": plain.loglik, "log1p": log_fit.loglik},
}
(HERE / "fit.json").write_text(json.dumps(out, indent=2) + "\n")
print(f"\nwrote {HERE / 'fit.json'}")
