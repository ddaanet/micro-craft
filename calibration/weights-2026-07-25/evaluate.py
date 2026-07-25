"""Score the fitted weights, and re-price the sweep under them.

Three questions, in order of what they decide:

- Do the fitted weights rank better than the installed ones, measured
  out of sample rather than on the rows that produced them?
- How noisy are the labels? Attenuation from label noise biases every
  coefficient toward zero, so the replicate blocks bound how much of a
  small coefficient could be measurement error.
- Where does the sweep boundary land once the ranking is recomputed —
  and does it still drop the 415 items the tail sample could not place?
"""

import json
import random
from math import exp
from pathlib import Path

from labels import METRICS, corpus_untriaged, load
from logistic import fit

HERE = Path(__file__).parent
RIDGE = 1.0
FOLDS = 10
BATCH_ITEMS = 12
BATCH_CHARS = 200_000
CURRENT = {
    "comments": 1.0,
    "reactions": 0.5,
    "participants": 2.0,
    "related_items": 3.0,
    "span_years": 1.0,
}
BASELINE_BUDGET = 2601  # the tail sample's recommended top-N

rows, sample, calls = load()
res = json.loads((HERE / "fit.json").read_text())
x = [r.x for r in rows]
y = [r.y for r in rows]
w = [r.weight for r in rows]


def auc(
    scores: list[float], labels: list[int], wts: list[float] | None = None
) -> float:
    """Weighted AUC: the chance a signal item outranks a no-signal one.

    Computed as a pair count rather than from a ROC curve, because ties
    are common here — the plateau puts hundreds of items on identical
    scores — and a tied pair has to count as half.
    """
    ww = wts or [1.0] * len(labels)
    num = den = 0.0
    pos = [i for i, v in enumerate(labels) if v]
    neg = [i for i, v in enumerate(labels) if not v]
    for i in pos:
        for j in neg:
            m = ww[i] * ww[j]
            den += m
            if scores[i] > scores[j]:
                num += m
            elif scores[i] == scores[j]:
                num += 0.5 * m
    return num / den if den else 0.5


def dot(weights: dict[str, float], row: list[float]) -> float:
    return sum(weights[m] * v for m, v in zip(METRICS, row, strict=False))


print(f"== ranking quality on {len(rows)} labelled items, {sum(y)} signal ==")
print(f"  {'ranking by':22}{'AUC':>7}{'AUC (corpus-weighted)':>24}")
candidates: dict[str, list[float]] = {
    "current weights": [dot(CURRENT, r) for r in x],
    "fitted weights": [dot(res["fitted_weights"], r) for r in x],
    "sparse weights": [dot(res["sparse_weights"], r) for r in x],
}
for m in METRICS:
    candidates[f"{m} alone"] = [row[METRICS.index(m)] for row in x]
for name, s in candidates.items():
    print(f"  {name:22}{auc(s, y):>7.3f}{auc(s, y, w):>24.3f}")

# The fitted vector was chosen on these rows, so its in-sample AUC is
# optimistic by construction. Cross-validation refits inside each fold
# and scores only held-out rows.
rng = random.Random(1)
order = list(range(len(rows)))
rng.shuffle(order)
held = [0.0] * len(rows)
for f in range(FOLDS):
    test = [order[i] for i in range(f, len(order), FOLDS)]
    train = [i for i in order if i not in set(test)]
    if len({y[i] for i in train}) < 2:
        continue
    model = fit([x[i] for i in train], [y[i] for i in train], ridge=RIDGE)
    for i in test:
        held[i] = model.score(x[i])
print(f"\n  fitted weights, {FOLDS}-fold cross-validated: AUC {auc(held, y):.3f}")
print(
    f"  current weights, no fitting to cross-validate:  AUC {auc(candidates['current weights'], y):.3f}"
)

print("\n== label noise ==")
reps = [p for p in sample if p["block"] == "REPLICATE" and "verdict" in p]
pairs: list[tuple[int, str, str]] = []
for p in reps:
    if "replicate_of" in p:
        orig = [q for q in sample if q["number"] == p["number"] and q is not p]
        for q in orig:
            if "verdict" in q:
                pairs.append(
                    (int(str(p["number"])), str(q["verdict"]), str(p["verdict"]))
                )
    elif "run1" in p:
        run1 = p["run1"]
        assert isinstance(run1, dict)
        pairs.append((int(str(p["number"])), str(run1["verdict"]), str(p["verdict"])))
same = sum(1 for _, a, b in pairs if a == b)
print(f"  replicate agreement {same}/{len(pairs)}")
for num, a, b in sorted(pairs):
    flag = "" if a == b else "   <- disagree"
    print(f"    #{num:<5} first={a:<9} second={b:<9}{flag}")

cal = [p for p in sample if p["block"] == "CAL" and "verdict" in p]
hits = sum(1 for p in cal if p["truth"] == p["verdict"])
adj = sum(1 for p in cal if (p.get("adjudicated") or p["truth"]) == p["verdict"])
print(f"\n  CAL vs the pilot's verdicts       {hits}/{len(cal)}")
print(f"  CAL vs the tail sample's reading  {adj}/{len(cal)}")
for p in sorted(cal, key=lambda q: int(str(q["number"]))):
    a = p.get("adjudicated")
    note = f" (adjudicated {a})" if a and a != p["truth"] else ""
    print(f"    #{p['number']:<5} pilot={p['truth']:<9} called={p['verdict']:<9}{note}")

# Re-price the sweep. The size model now rests on 162 measured renders
# rather than 54, and the yield curve is the fitted model's own
# predictions rather than an eight-step staircase — the model is what
# the extra labels bought.
corpus = corpus_untriaged()
measured = {int(p["number"]): int(str(p["chars"])) for p in sample}
heat_by_num = {int(r["number"]): r for r in corpus}
xs = [
    (float(heat_by_num[n]["comments"]), c)
    for n, c in measured.items()
    if n in heat_by_num
]
mx = sum(a for a, _ in xs) / len(xs)
my = sum(b for _, b in xs) / len(xs)
slope = sum((a - mx) * (b - my) for a, b in xs) / sum((a - mx) ** 2 for a, _ in xs)
base = my - slope * mx
print(
    f"\n== sweep cost ==\n  size model: chars ~= {base:.0f} + {slope:.0f} * comments (n={len(xs)})"
)


def spawns(items: list[dict[str, str]]) -> int:
    count, n_items, n_chars = 1, 0, 0.0
    for r in items:
        size = max(500.0, base + slope * float(r["comments"]))
        if n_items + 1 > BATCH_ITEMS or n_chars + size > BATCH_CHARS:
            count += 1
            n_items, n_chars = 0, 0.0
        n_items += 1
        n_chars += size
    return count


# Calibrate the intercept to the corpus. Unweighted slopes are unbiased
# under feature-dependent sampling; the intercept is not, so it is
# refitted by matching the model's weighted mean prediction to the
# weighted observed rate — a one-dimensional solve.
coef = [res["coef"][m] for m in METRICS]
target = sum(wi * yi for wi, yi in zip(w, y, strict=False)) / sum(w)
lo, hi = -20.0, 20.0
for _ in range(200):
    mid = (lo + hi) / 2
    pred = sum(
        wi / (1 + exp(-(mid + sum(c * v for c, v in zip(coef, xi, strict=False)))))
        for wi, xi in zip(w, x, strict=False)
    ) / sum(w)
    lo, hi = (mid, hi) if pred < target else (lo, mid)
intercept = (lo + hi) / 2
print(f"  corpus-calibrated base rate {target:.1%} at intercept {intercept:+.2f}")


def p_signal(r: dict[str, str]) -> float:
    eta = intercept + sum(res["coef"][m] * float(r[m]) for m in METRICS)
    return 1 / (1 + exp(-eta))


for label, weights in (
    ("current", CURRENT),
    ("fitted", res["fitted_weights"]),
    ("sparse", res["sparse_weights"]),
):
    ranked = sorted(
        corpus,
        key=lambda r: (-dot(weights, [float(r[m]) for m in METRICS]), int(r["number"])),
    )
    total = sum(p_signal(r) for r in ranked)
    print(f"\n  ranking by {label} weights — expected signal in the corpus {total:.0f}")
    print(f"    {'budget':>8}{'spawns':>8}{'expected signal kept':>22}")
    for n in (385, 914, 1491, 1849, 2139, 2269, 2601, 3000, len(ranked)):
        head = ranked[:n]
        got = sum(p_signal(r) for r in head)
        print(f"    {n:>8}{spawns(head):>8}{got / total:>21.0%}")
    if label == "fitted":
        fitted_top = {int(r["number"]) for r in ranked[:BASELINE_BUDGET]}

cur_ranked = sorted(
    corpus,
    key=lambda r: (-dot(CURRENT, [float(r[m]) for m in METRICS]), int(r["number"])),
)
cur_top = {int(r["number"]) for r in cur_ranked[:BASELINE_BUDGET]}
print(f"\n== does recalibration move the boundary? (top {BASELINE_BUDGET}) ==")
print(
    f"  overlap {len(cur_top & fitted_top)}/{BASELINE_BUDGET} = {len(cur_top & fitted_top) / BASELINE_BUDGET:.0%}"
)
print(
    f"  promoted into the sweep {len(fitted_top - cur_top)}   dropped out {len(cur_top - fitted_top)}"
)
union = cur_top | fitted_top
print(
    f"  swept under either vector: {len(union)} items, {spawns([r for r in cur_ranked if int(r['number']) in union])} spawns"
)

(HERE / "evaluate.json").write_text(
    json.dumps(
        {
            "auc": {k: auc(v, y) for k, v in candidates.items()},
            "auc_cv_fitted": auc(held, y),
            "replicate_agreement": [len(pairs), same],
            "cal_vs_pilot": [len(cal), hits],
            "size_model": {"base": base, "slope": slope, "n": len(xs)},
            "corpus_base_rate": target,
            "boundary_overlap": len(cur_top & fitted_top),
            "promoted": sorted(fitted_top - cur_top),
            "dropped": sorted(cur_top - fitted_top),
        },
        indent=2,
    )
    + "\n"
)
