# Weight calibration, 2026-07-25

Raw material behind `docs/ghmem-heat-weights.md`. The tail sample's
54 labels said the installed `HEAT_WEIGHTS` were wrong — `related_items`
carried the heaviest weight and discriminated at exactly the base rate —
but n=54 fits a direction, not five parameters. This run draws wider,
against the same corpus snapshot, and fits them.

`heat.csv` is byte-identical to `../tail-sample-2026-07-25/heat.csv`, so
the two runs rank the same corpus and run 1's labels pool forward into
this fit rather than being re-measured.

| file                  | what it is                                          |
|-----------------------|-----------------------------------------------------|
| `heat.csv`            | the ranking, with each item's metric vector         |
| `profile.py`          | metric-space profile: degeneracy, correlation       |
| `pool_prior.py`       | run-1 verdicts → `prior-labels.json`                |
| `draw.py`             | five-block draw, seed 202607252 → `sample.json`     |
| `measure.py`          | renders each item once, records its size            |
| `split.py`            | 7-way rater split → `worklist-{A..G}.md`            |
| `rubric.md`           | the signal/no-signal rubric the raters were given   |
| `verdicts-{A..G}.md`  | what the seven raters returned, verbatim            |
| `labels.py`           | shared loader: verdicts + run-1 labels → feature rows |
| `logistic.py`         | ridge logistic regression by IRLS, pure Python      |
| `check_logistic.py`   | recovers known coefficients from synthetic data     |
| `fit.py`              | the fit → `fit.json`, and the weight vectors        |
| `evaluate.py`         | AUC, label noise, re-priced sweep → `evaluate.json` |

`measure.py` writes a `renders/` directory of `ghmem show` output, keyed
by item number. It is not kept here — 662k characters of GitHub content
that regenerates from the corpus, and `sample.json` records each item's
size.

Rerun order: `profile` → `pool_prior` → `draw` → `measure` → `split` →
(rate) → `fit` → `evaluate` → `compare`. Everything but the rating step
replays: `draw.py` is seeded against the snapshotted `heat.csv`.

These scripts are outside `just green`'s reach on purpose. `ruff check`
used to lint them — it was the one check in the gate taking no path
argument — while `gate-inputs-hash` hashes only `src` and `tests`, so a
calibration script could turn the gate red without invalidating its
cache. The tail-sample scripts did exactly that and nobody saw it for
days. `calibration` now sits in ruff's `exclude` beside
`plans/prototypes`, which is the honest scope for one-off analysis code.
The consequence for anyone editing these files: nothing formats or lints
them, so match the surrounding style by hand.

## Why the draw is not stratified on heat

Run 1 cut eight rank-uniform strata out of the composite score, which
was right for a question about where to truncate it. For a question
about the weights it fixes the spread of the very quantity under test,
and run 1's own write-up flagged that as the reason its
single-metric-versus-composite table handicapped the composite.

Selecting on a covariate does not bias logistic-regression slopes — only
the intercept — so run 1's design was not disqualifying for a fit. The
objection is about efficiency and about what can honestly be compared.
This run spends its budget on spread through metric space instead:

- **CONTRAST** (110) draws distinct metric *vectors* uniformly, then one
  item inside the chosen class. 3847 untriaged items occupy only 1917
  distinct vectors, and one vector alone — no comments, no reactions, one
  participant, nothing related — holds 611 of them. Drawing items
  uniformly spends a sixth of the budget re-measuring that single point.
- **PLATEAU** (24) takes the six largest degenerate classes, four each.
  Those 1131 items are 29% of the corpus and no non-negative reweighting
  can reorder them, so their conditional signal rate is exactly what a
  truncation budget turns on.
- **UNIFORM** (16) is a plain uniform draw: a design-free base-rate
  estimate that leans on no inverse-probability weights.
- **CAL** (6) mixes in the pilot's own verdicts blind, as run 1 did.
- **REPLICATE** (12) re-rates six run-1 items and shows six fresh draws
  to a second rater. Label noise attenuates coefficients toward zero, so
  its size has to be measured — run 1's 3/6 CAL agreement said it is not
  small.

Every item carries the `weight` its block's inclusion probability
implies, so a block's weights sum to the population it covers: 3847 for
CONTRAST and UNIFORM, 1131 for PLATEAU. The blocks are separate
estimators of overlapping populations and are never pooled into one
weighted total. CONTRAST's realized weight sum falls short of 3847 —
uniform-over-classes is a high-variance population estimator, which is
the price of buying contrast — so population statements lean on UNIFORM
and PLATEAU while the slopes come from every row unweighted.

## Read-only, and how much weaker that is than run 1

Nothing was routed. Verified against a pre-run snapshot: `routing.jsonl`
byte-identical, `pending=3847`, `dispatched=0`.

Run 1's raters had file reads and no shell, so read-only was structural.
This run's raters are `Explore` subagents, which cannot Write or Edit
but do carry Bash — a purpose-built agent definition would need a Claude
Code restart to become visible, and the run was not worth deferring for
it. Two things stand in for the missing restriction: the prompt forbids
shell outright, and `ghmem route` rejects any item not currently
dispatched to a live session token, so writing a verdict would take an
affirmative `ghmem triage` call that the snapshot comparison would catch.
