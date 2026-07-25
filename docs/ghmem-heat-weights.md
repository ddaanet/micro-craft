# Heat weights: a wider draw, and a negative result

A second read-only stratified sample of the untriaged corpus, run
2026-07-25 to fit `HEAT_WEIGHTS` before the triage sweep spends 219
spawns under them.

The answer is that they do not need fitting. The installed provisional
vector ranks as well as anything this evidence can produce, and the tail
sample's case against it does not survive a design that is not
stratified on the score.

Nothing was routed. Verified against a pre-run snapshot: `routing.jsonl`
and `fetch.jsonl` byte-identical, `pending=3847`, `dispatched=0`.

## Why this had to come before the sweep

Heat order is load-bearing beyond truncation. The hottest item in a
theme mints the topic name, later items join it, and `record_verdict`
refuses a second verdict for a routed item — so a name assigned under
wrong weights is permanent. The tail sample found the weights looked
wrong and stopped, which was the right place to stop.

That gate is now cleared, and cleared by a negative result: the ranking
does not change, so the sweep can run under the weights already
installed.

## Method

168 rating slots over 162 distinct items, plus the tail sample's 54
labels pooled forward. The fresh `ghmem heat` snapshot is byte-identical
to the tail sample's, so a run-1 label attaches to the same feature row
a run-2 label would, and reusing them costs nothing. That gives 198
labelled items against five parameters.

Seven Sonnet raters, 24 slots each — Sonnet because that is the tier
`ghmem-triage` runs at, so the labels price the real sweep rather than
an idealised one. Every rater saw a mix of all five blocks, so no
block's rate rests on one rater's leniency.

### Not stratified on heat

The tail sample cut eight rank-uniform strata out of the composite
score, and flagged in its own write-up that this handicapped the
composite in any comparison against single metrics.

That caveat turns out to understate one thing and overstate another.
Selecting on covariates leaves logistic-regression slopes unbiased —
only the intercept moves — so run 1's design was never disqualifying for
a fit. But the handicap on the *comparison* was real, and it is the
reason its headline claim about `comments` does not replicate below.

This run spends its budget on spread through metric space instead. The
corpus makes that worth doing: 3847 untriaged items occupy only 1917
distinct metric vectors, and one vector alone — no comments, no
reactions, one participant, nothing related — holds 611 of them. A
uniform draw spends a sixth of its budget re-measuring a single point.

| block     |   n | what it buys                                        |
|-----------|-----|-----------------------------------------------------|
| CONTRAST  | 110 | distinct metric vectors drawn uniformly, then one item inside the class — spread, for the fit |
| PLATEAU   |  24 | the six largest degenerate classes, four each: 1131 items no reweighting can reorder |
| UNIFORM   |  16 | a plain uniform draw — a base rate that leans on no inverse-probability weights |
| CAL       |   6 | the pilot's own verdicts, mixed in blind            |
| REPLICATE |  12 | six run-1 items re-rated, six fresh draws shown twice |

Each item records the inclusion probability that drew it, so a block's
weights sum to the population it covers — 3847 for CONTRAST and UNIFORM,
1131 for PLATEAU. The blocks are separate estimators of overlapping
populations and are never pooled into one weighted total.

### The fit

Logistic regression, linear in raw metric counts, ridge 1.0. Linear in
raw counts because the scorer is: ranking by a logistic model's linear
predictor and ranking by a weighted sum are the same ordering, so the
coefficients drop into `heat.py` without touching the SQL in
`heat_query.py`. Any better-conditioned transform would produce numbers
that cannot be installed.

Slopes come from the unweighted fit, which is the efficient choice given
that the draw selected on features and never on labels. The
inverse-probability fit runs alongside as a check that the design is not
producing the answer.

The estimator was checked against synthetic data with known
coefficients, two of them true zeros, before being pointed at real
labels — `check_logistic.py`. A hand-rolled IRLS that quietly converges
to the wrong place would have produced a plausible weight vector and no
error.

## What the fit says

| metric          |   coef | stderr | boot 95%         | ipw coef | current |
|-----------------|--------|--------|------------------|----------|---------|
| comments        | +0.107 |  0.050 | +0.008 to +0.299 |   +0.067 |     1.0 |
| reactions       | −0.015 |  0.037 | −0.125 to +0.154 |   −0.075 |     0.5 |
| participants    | +0.270 |  0.170 | −0.110 to +0.740 |   +0.830 |     2.0 |
| related_items   | +0.243 |  0.132 | −0.043 to +0.570 |   +0.526 |     3.0 |
| span_years      | +0.036 |  0.110 | −0.263 to +0.328 |   +0.110 |     1.0 |

Rescaled to the installed vector's total, so the two read side by side:

| metric        | current | fitted |
|---------------|---------|--------|
| comments      |     1.0 |   1.22 |
| reactions     |     0.5 |   0.00 |
| participants  |     2.0 |   3.09 |
| related_items |     3.0 |   2.78 |
| span_years    |     1.0 |   0.41 |

Which is close. `reactions` goes to zero, `participants` gains a third,
`span_years` loses half, and the two headline numbers — `comments` at 1.0
and `related_items` at 3.0 — barely move.

### Only one coefficient is resolved

Standard errors are set mostly by the design, so what this draw could
have detected is knowable independently of what it found. Per standard
deviation of the metric, so the five compare:

| metric        | log-odds / sd | min detectable |          |
|---------------|---------------|----------------|----------|
| comments      |        +0.518 |         +0.475 | resolved |
| participants  |        +0.386 |         +0.476 | under-powered |
| related_items |        +0.359 |         +0.384 | under-powered |
| reactions     |        −0.082 |         +0.397 | under-powered |
| span_years    |        +0.063 |         +0.377 | under-powered |

`comments` clears its own detection threshold. The other four do not,
and two of them — `participants` and `related_items` — miss by a hair.
A coefficient inside its minimum detectable effect is not evidence of no
effect, only of an effect this draw cannot see, so the four zeros in the
sparse column of any weight table are an artifact of n and not findings.

## The decisive table

Whether to install a vector is not a question about coefficients. It is
a question about whether the new ordering ranks signal above no-signal
better than the old one, on the corpus rather than on the sample. The
same items score every candidate, so the paired difference is far better
determined than either AUC alone.

Corpus-weighted AUC, paired against the installed vector at 0.841:

| candidate                    |   AUC |   diff | boot 95%         |         |
|------------------------------|-------|--------|------------------|---------|
| current, reactions dropped   | 0.839 | −0.002 | −0.016 to +0.012 | no difference |
| fitted                       | 0.843 | +0.002 | −0.022 to +0.037 | no difference |
| comments only                | 0.818 | −0.022 | −0.105 to +0.046 | no difference |
| current on log1p scale       | 0.827 | −0.013 | −0.035 to +0.012 | no difference |
| fitted coefs on log1p scale  | 0.834 | −0.006 | −0.037 to +0.032 | no difference |

Nothing clears zero. And under ten-fold cross-validation the fitted
vector is actively worse than the installed one — 0.718 against 0.753 —
because at n=198 the estimation noise in five coefficients costs more
than the reallocation gains. The installed vector needs no
cross-validating: it was never fitted to anything.

So the recommendation is to change nothing.

## The tail sample's two claims

Both were stated as directions rather than fits, and the wider draw
splits them.

**`related_items` carries weight 3.0 and discriminates at the base
rate.** Half right. As a lone ranker it is the weakest of the five —
AUC 0.595, barely above a coin, which is what run 1 measured. But its
fitted coefficient is +0.243, the second largest in the vector, and
zeroing it costs corpus-weighted AUC (0.818 against 0.843). A metric can
be useless alone and useful conditionally; the inference from "weak
marginally" to "misweighted" does not hold.

**`comments` is the best single predictor and beats the composite it
feeds.** This was the artifact its own caveat predicted. On the sample
`comments` alone scores 0.755 against the composite's 0.753 — a dead
heat. Weighted back to the corpus it loses, 0.818 against 0.841. Run 1's
strata fixed the composite's spread by construction and let the
individual metrics vary freely, which is exactly the comparison that
flatters a part over the whole.

There is a third finding that survives on likelihood and dies on
ranking. A log1p-scale model fits the labels better than the raw-count
scale the scorer uses — log-likelihood −111.0 against −115.6, same
number of parameters. It does not rank better (0.827 against 0.841), so
the case for rewriting the SQL in `heat_query.py` is not there. Worth
recording as the one place a real functional-form defect might hide.

## The plateau, which is the run's strongest number

PLATEAU drew four items from each of the six largest degenerate metric
classes. Those classes hold 1131 items — 29% of the untriaged corpus —
and no non-negative reweighting can reorder any of them, because they
are tied on every metric.

**One of 24 carried signal.**

The tail sample reached the same conclusion from 18 items spread across
its three coldest rank strata, and worried that the 0-for-18 rested on a
boundary the sample could not resolve. This block does not depend on a
boundary at all. It samples named points in metric space that a budget
cut will always drop, and it finds them close to empty.

That is the answer to the tail sample's open question about the 415
boundary-sensitive items: recalibration does resolve it, by making it
moot. The top 2601 under the installed vector and under the fitted
vector overlap by 97% — 67 items swapped each way. The set the sweep
drops is not sensitive to a reweighting that does not happen.

## What the labels are worth

Replicate agreement was 10 of 12, and both disagreements ran the same
way — a second rater finding signal where the first found none, on #632
(softwrap scrolling) and #3281 (a syntax file deferred pending language
stability). Label noise attenuates coefficients toward zero, so 83%
agreement is part of why four of five coefficients sit inside their
detection thresholds.

CAL agreement was 3 of 6 against the pilot's verdicts and 5 of 6 against
the tail sample's adjudication of them — the same split run 1 found, and
for the same reason: all three of the pilot's `no-signal` calls are in
the block, and two of them were wrong.

The rubric change worked. #1445 is the forty-comment argument about
whether V is a scam that ends with the owner ruling on `.v` filetype
precedence, and the pilot called it no-signal. Rater B called it signal
and said why: "off-topic flamewar, but owner ends it ruling to merge and
keep .v precedence over Verilog for now." The one remaining miss is
#3783, where the tail sample leaned toward the pilot and a rater
disagreed — a genuinely fuzzy PR-review thread, not a prompt defect.

## One correction to the tail sample's cost table

Its yield column said a top-2601 budget forgoes nothing the sample could
detect — 100% of measured signal kept. That came from a cell containing
zero items of signal, not from a true zero.

A fitted model gives cold items a low but nonzero probability, and
integrating it over the ranking puts a top-2601 budget at **82% of
expected signal**, against an estimated 1419 signal items in the whole
untriaged corpus at a corpus-calibrated base rate of 36.5%.

| budget | spawns | expected signal kept |
|--------|--------|----------------------|
|    385 |     34 |                  22% |
|    914 |     78 |                  42% |
|   1491 |    126 |                  58% |
|   1849 |    156 |                  67% |
|   2139 |    180 |                  73% |
|   2269 |    191 |                  75% |
| **2601** | **219** | **82%**          |
|   3000 |    252 |                  88% |
|   3847 |    323 |                 100% |

The size model behind the spawn counts now rests on 162 measured renders
rather than 54: `chars ≈ 1233 + 548 × comments`.

This does not change the recommendation — the curve is smooth, so no
budget is a natural stopping point, and 2601 remains a defensible one.
It changes what the recommendation claims. Truncating at 2601 forgoes
about a fifth of the expected signal rather than none of it, and that
should be said plainly before the spawns are spent.

## What this settles, and what it does not

It settles the weights: leave them. They are no longer provisional in
the sense of untested — they were tested against 198 labels and nothing
beat them. They remain uncertain in the sense that four of five
coefficients are unresolved, and a draw two or three times wider could
still find a reallocation worth making.

It settles the sweep's gate. The reason to calibrate before sweeping was
that a wrong ranking mints permanent topic names; the ranking is not
wrong, or at least is not improvable on this evidence, so the sweep is
unblocked.

It does not settle whether five metrics is the right set. Everything
here reweights the metrics `heat_query.py` already computes. Nothing
tested a metric the corpus could carry and does not — whether an item is
closed, whether a maintainer commented at all, whether the thread's last
word came from someone with commit access. `participants` at AUC 0.709
is the best of the four weak metrics, and "a maintainer participated" is
plausibly a sharper version of the same idea.

It does not license a third draw on this design. The returns are visible
in the numbers: 198 labels resolved one coefficient. Getting the other
four inside their thresholds needs roughly four times the data for twice
the precision, which is 600-plus items and most of a sweep's budget spent
on measurement rather than on triage. If the weights matter more later —
after the sweep, with real routing outcomes to fit against instead of
proxy labels — that evidence arrives free.

## Reference tables

Kept so a later reader can check a claim above without rerunning
anything. Every number here comes out of `profile.py`, `fit.py`,
`evaluate.py` or `compare.py` in
`tools/ghmem/calibration/weights-2026-07-25/`.

### Observed signal rate by block

| block    |   n | signal |  rate | what it covers            |
|----------|-----|--------|-------|---------------------------|
| CONTRAST | 110 |     50 |  45%  | 3847 items, weighted      |
| PLATEAU  |  24 |      1 |   4%  | 1131 items, six classes   |
| UNIFORM  |  16 |      8 |  50%  | 3847 items, weighted      |
| RUN1     |  48 |     16 |  33%  | run 1's eight rank strata |

CONTRAST and UNIFORM are separate estimators of the same population, and
their rates are not meant to agree closely at these sizes. UNIFORM's 16
items put a wide interval on 50%; CONTRAST's inverse-probability weights
are high-variance by design. The corpus-calibrated base rate the model
settles on is 36.5%.

### Single-metric ranking quality

| ranking by         | AUC on sample | AUC corpus-weighted |
|--------------------|---------------|---------------------|
| current weights    |         0.753 |               0.841 |
| fitted weights     |         0.753 |               0.843 |
| comments alone     |         0.755 |               0.818 |
| participants alone |         0.709 |               0.794 |
| span_years alone   |         0.652 |               0.730 |
| reactions alone    |         0.611 |               0.678 |
| related_items alone|         0.595 |               0.678 |

The two columns disagreeing is the whole point. On the sample `comments`
alone edges the composite; weighted back to the corpus it loses by 2.3
points. Any claim that a part beats the whole has to say which column it
came from.

### The metric space the design was built around

3847 untriaged items, 1917 distinct metric vectors. The six largest
classes, which PLATEAU samples:

| comments | reactions | participants | related | span | items |
|----------|-----------|--------------|---------|------|-------|
|        0 |         0 |            1 |       0 |    0 |   611 |
|        0 |         0 |            1 |       1 |    0 |   166 |
|        2 |         0 |            2 |       0 |    0 |   120 |
|        1 |         0 |            2 |       0 |    0 |   113 |
|        0 |         1 |            1 |       0 |    0 |    61 |
|        1 |         0 |            2 |       1 |    0 |    60 |

Marginal shape over the untriaged corpus:

| metric        | zero |  p50 |  p90 |  p99 |  max |
|---------------|------|------|------|------|------|
| comments      |  972 |  2.0 |  8.0 | 35.0 | 65.0 |
| reactions     | 2510 |  0.0 |  3.0 | 14.0 | 71.0 |
| participants  |    0 |  2.0 |  4.0 |  7.0 | 15.0 |
| related_items | 2125 |  0.0 |  2.0 |  6.0 | 19.0 |
| span_years    | 1891 |  0.0 |  1.4 |  6.5 |  9.8 |

No item has zero participants — the author always counts, so the metric
is at least 1 everywhere and its spread is the narrowest of the five.

Pairwise Pearson correlation runs 0.13 to 0.53, highest between
`participants` and `span_years` (0.53) and between `comments` and
`participants` (0.50). Moderate rather than collinear, which is what
makes a five-parameter fit worth attempting at all — and also why the fit
carries a ridge penalty rather than none.
