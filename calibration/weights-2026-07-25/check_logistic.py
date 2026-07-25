"""Recover known coefficients from synthetic data.

A hand-rolled IRLS that silently converges to the wrong answer would
produce a plausible-looking weight vector and no error, so the
estimator gets checked against a generating process whose coefficients
are known before it is pointed at the real labels. Two of the five
metrics are given a true coefficient of zero, which is the specific
claim the run has to be able to make about `related_items`.
"""

import random
from math import exp

from logistic import fit

TRUE = [0.30, 0.00, 0.45, 0.00, 0.12]
N = 4000
rng = random.Random(7)

x, y = [], []
for _ in range(N):
    row = [
        float(rng.randint(0, 40)),
        float(rng.randint(0, 30)),
        float(rng.randint(1, 12)),
        float(rng.randint(0, 10)),
        rng.random() * 9,
    ]
    eta = -3.0 + sum(t * v for t, v in zip(TRUE, row, strict=False))
    x.append(row)
    y.append(int(rng.random() < 1 / (1 + exp(-eta))))

# Ridge shrinks toward zero, so the recovery check runs unpenalized;
# the real fit's penalty is a variance choice, not a correctness one.
f = fit(x, y, ridge=0.0)
print(
    f"n={N} signal={sum(y)} iters={f.iters} intercept={f.intercept:+.2f} (true -3.00)"
)
print(f"{'metric':6}{'true':>8}{'fitted':>9}{'stderr':>9}{'z vs true':>11}")
worst = 0.0
for j, t in enumerate(TRUE):
    z = (f.coef[j] - t) / f.stderr[j]
    worst = max(worst, abs(z))
    print(f"  x{j:<4}{t:>8.2f}{f.coef[j]:>9.3f}{f.stderr[j]:>9.3f}{z:>+11.2f}")
print(f"\nworst |z| against truth: {worst:.2f}")
assert worst < 3.0, f"IRLS did not recover the generating coefficients ({worst:.2f})"

# And the mutation that matters: if the solver were ignoring a column,
# dropping a true-zero metric would change nothing while dropping a
# true-nonzero one must move the fit a long way.
drop2 = fit([r[:2] + r[3:] for r in x], y, ridge=0.0)
print(f"dropping x2 (true 0.45): loglik {f.loglik:.1f} -> {drop2.loglik:.1f}")
assert drop2.loglik < f.loglik - 20, "dropping a strong predictor barely hurt the fit"
print("\nok — IRLS recovers known coefficients and responds to the design matrix")
