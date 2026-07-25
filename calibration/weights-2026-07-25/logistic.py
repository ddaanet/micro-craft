"""Ridge logistic regression by IRLS, in pure Python.

Five features and a couple of hundred rows means the normal equations
are a 6x6 solve, so this is a few dozen lines of arithmetic rather than
a reason to add numpy to a locked dependency set that the `just green`
cache is keyed on.

Features are standardized inside `fit`, which makes the ridge penalty
scale-fair across metrics that differ by an order of magnitude, and the
coefficients are handed back on the raw-count scale — the scale
`HEAT_WEIGHTS` has to be expressed in.
"""

from dataclasses import dataclass
from math import exp, log, sqrt

Matrix = list[list[float]]


def _log(v: float) -> float:
    """`log` with the argument floored, so a saturated fit cannot blow up."""
    return log(max(v, 1e-12))


@dataclass
class Fit:
    """A fitted model on the raw-count scale."""

    intercept: float
    coef: list[float]
    stderr: list[float]
    iters: int
    loglik: float

    def score(self, x: list[float]) -> float:
        """The linear predictor, which is what ranking sorts on."""
        return self.intercept + sum(c * v for c, v in zip(self.coef, x, strict=False))


def solve(a: Matrix, b: list[float]) -> list[float]:
    """Solve `a x = b` by Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [[*row[:], b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            raise ValueError(f"singular at column {col}")
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r == col:
                continue
            f = m[r][col] / m[col][col]
            for c in range(col, n + 1):
                m[r][c] -= f * m[col][c]
    return [m[i][n] / m[i][i] for i in range(n)]


def inverse(a: Matrix) -> Matrix:
    """Invert `a` column by column, for the coefficient covariance."""
    n = len(a)
    cols = []
    for j in range(n):
        e = [1.0 if i == j else 0.0 for i in range(n)]
        cols.append(solve(a, e))
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def _sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + exp(-z))
    e = exp(z)
    return e / (1.0 + e)


def fit(
    x: list[list[float]],
    y: list[int],
    ridge: float = 1.0,
    weights: list[float] | None = None,
    iters: int = 60,
) -> Fit:
    """Fit ridge logistic regression, returning raw-scale coefficients.

    `ridge` penalizes the standardized slopes and never the intercept.
    A small default rather than zero: the corpus holds metric pairs
    correlated at 0.5, and an unpenalized fit on a couple of hundred
    rows lets that collinearity throw individual coefficients around
    far more than the data supports.

    `weights` are observation weights — the inverse-probability weights
    when a population-representative fit is wanted. Left out, every row
    counts once, which is the right choice for the slopes: sampling that
    depends on the features and not on the label leaves them unbiased,
    and unweighted fitting is the more efficient of the two.
    """
    n, k = len(x), len(x[0])
    w = weights or [1.0] * n
    mean = [sum(row[j] for row in x) / n for j in range(k)]
    sd = [sqrt(sum((row[j] - mean[j]) ** 2 for row in x) / n) or 1.0 for j in range(k)]
    z = [[1.0] + [(row[j] - mean[j]) / sd[j] for j in range(k)] for row in x]

    beta = [0.0] * (k + 1)
    prev = None
    used = 0
    for used in range(1, iters + 1):
        eta = [sum(b * v for b, v in zip(beta, row, strict=False)) for row in z]
        p = [_sigmoid(e) for e in eta]
        # Floor the IRLS weight: a fitted probability at 0 or 1 makes
        # p(1-p) vanish and the working response diverge.
        wt = [max(pi * (1 - pi), 1e-6) * w[i] for i, pi in enumerate(p)]
        work = [eta[i] + (y[i] - p[i]) / max(p[i] * (1 - p[i]), 1e-6) for i in range(n)]
        hess = [
            [sum(wt[i] * z[i][a] * z[i][b] for i in range(n)) for b in range(k + 1)]
            for a in range(k + 1)
        ]
        for j in range(1, k + 1):
            hess[j][j] += ridge
        rhs = [sum(wt[i] * z[i][a] * work[i] for i in range(n)) for a in range(k + 1)]
        beta = solve(hess, rhs)
        ll = sum(
            w[i] * (y[i] * _log(p[i]) + (1 - y[i]) * _log(1 - p[i])) for i in range(n)
        )
        if prev is not None and abs(ll - prev) < 1e-9:
            break
        prev = ll

    cov = inverse(hess)
    coef = [beta[j + 1] / sd[j] for j in range(k)]
    stderr = [sqrt(max(cov[j + 1][j + 1], 0.0)) / sd[j] for j in range(k)]
    intercept = beta[0] - sum(beta[j + 1] * mean[j] / sd[j] for j in range(k))
    return Fit(intercept, coef, stderr, used, prev or 0.0)
