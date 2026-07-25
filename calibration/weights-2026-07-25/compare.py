"""Is any candidate weight vector better than the installed one?

`evaluate.py` shows the fitted vector matching the installed one on AUC
and losing to it under cross-validation, which is an argument for
changing nothing. An argument that specific deserves a paired interval
rather than two point estimates side by side: the same items score both
vectors, so the difference is far better determined than either AUC.

Also tests the functional form. `fit.py` reports a log1p-scale model
fitting the labels better than the raw-count scale the scorer uses. If
that survives here it is a finding about `heat_query.py`'s SQL, not
about the constants in `heat.py`.
"""

import json
import random
from math import log1p
from pathlib import Path

from labels import METRICS, load

HERE = Path(__file__).parent
BOOTSTRAP = 600
CURRENT = {
    "comments": 1.0,
    "reactions": 0.5,
    "participants": 2.0,
    "related_items": 3.0,
    "span_years": 1.0,
}

rows, _, _ = load()
res = json.loads((HERE / "fit.json").read_text())
y = [r.y for r in rows]
w = [r.weight for r in rows]


def auc(scores: list[float], idx: list[int]) -> float:
    """Corpus-weighted AUC over the rows named by `idx`."""
    pos = [i for i in idx if y[i]]
    neg = [i for i in idx if not y[i]]
    num = den = 0.0
    for i in pos:
        for j in neg:
            m = w[i] * w[j]
            den += m
            num += (
                m
                if scores[i] > scores[j]
                else (0.5 * m if scores[i] == scores[j] else 0.0)
            )
    return num / den if den else 0.5


def linear(weights: dict[str, float]) -> list[float]:
    return [
        sum(weights[m] * v for m, v in zip(METRICS, r.x, strict=False)) for r in rows
    ]


def logscale(weights: dict[str, float]) -> list[float]:
    return [
        sum(weights[m] * log1p(v) for m, v in zip(METRICS, r.x, strict=False))
        for r in rows
    ]


log_coef = {m: res["coef"][m] for m in METRICS}
candidates: dict[str, list[float]] = {
    "current (installed)": linear(CURRENT),
    "current, reactions dropped": linear({**CURRENT, "reactions": 0.0}),
    "fitted": linear(res["fitted_weights"]),
    "comments only": linear({m: 1.0 if m == "comments" else 0.0 for m in METRICS}),
    "current on log1p scale": logscale(CURRENT),
    "fitted coefs on log1p scale": logscale(log_coef),
}

whole = list(range(len(rows)))
base = auc(candidates["current (installed)"], whole)
print("== corpus-weighted AUC, paired against the installed vector ==")
print(f"  {len(rows)} items, {sum(y)} signal.  installed vector: AUC {base:.3f}\n")
print(f"  {'candidate':30}{'AUC':>7}{'diff':>9}{'boot 2.5%':>11}{'boot 97.5%':>12}")

rng = random.Random(99)
draws = [[rng.randrange(len(rows)) for _ in rows] for _ in range(BOOTSTRAP)]
draws = [d for d in draws if len({y[i] for i in d}) > 1]

for name, s in candidates.items():
    if name == "current (installed)":
        continue
    diffs = []
    for d in draws:
        diffs.append(auc(s, d) - auc(candidates["current (installed)"], d))
    diffs.sort()
    lo = diffs[int(0.025 * len(diffs))]
    hi = diffs[int(0.975 * len(diffs))]
    verdict = "" if lo > 0 else ("   worse" if hi < 0 else "   no difference")
    print(
        f"  {name:30}{auc(s, whole):>7.3f}{auc(s, whole) - base:>+9.3f}"
        f"{lo:>+11.3f}{hi:>+12.3f}{verdict}"
    )

print(
    "\n  A candidate has to clear zero on the low side to be worth\n"
    "  installing. Heat order mints topic names permanently, so a change\n"
    "  that cannot be shown to help is a change that cannot be undone."
)
