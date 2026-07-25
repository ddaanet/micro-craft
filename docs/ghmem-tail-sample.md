# Tail sample: no-signal rate as a function of heat

A read-only stratified sample of the untriaged corpus, run 2026-07-25 to
decide where — or whether — to truncate the full triage sweep.

Nothing was routed and no ledger was written. That is the design, not an
incidental property: the items were rendered to disk up front with
`ghmem show`, and the classifiers were given file reads and no shell, so
read-only is structural rather than a promise in a prompt. Verified
after the run: `pending=3847`, `dispatched=0`, `routing.jsonl` unchanged.

## Method

Eight rank-uniform strata over the 3847 untriaged items, six items each,
drawn with a fixed seed. S1 covers ranks 34–431 (heat 23–86); S8 covers
ranks 3460–3873, entirely inside the flat heat-2.0 plateau that the
bottom tenth of the ranking collapses into.

A ninth stratum, CAL, holds six items with known verdicts from the
triage pilot — all three of its `no-signal` calls plus three routed
ones — mixed in unlabelled. Its job is to catch a classifier whose low
tail no-signal rate reflects its own leniency rather than the corpus.

Three Sonnet raters, two items per stratum each, so every rater saw the
whole heat range and no stratum's rate rests on a single rater. Sonnet
because that is the tier `ghmem-triage` runs at; the curve is meant to
price the real sweep, not an idealised one.

## The curve

| stratum | ranks     | heat      | signal | rate |
|---------|-----------|-----------|--------|------|
| S1      | 34–431    | 23.3–85.9 | 3/6    | 50%  |
| S2      | 638–929   | 15.0–19.0 | 4/6    | 67%  |
| S3      | 1021–1469 | 11.0–14.0 | 2/6    | 33%  |
| S4      | 1570–1820 | 9.0–10.1  | 5/6    | 83%  |
| S5      | 1988–2390 | 6.1–8.0   | 2/6    | 33%  |
| S6      | 2565–2853 | 5.0–6.0   | 0/6    | 0%   |
| S7      | 2916–3357 | 2.0–5.0   | 0/6    | 0%   |
| S8      | 3460–3873 | 2.0–2.0   | 0/6    | 0%   |

The head is noisy and the tail is not. S1 through S5 scatter between 33%
and 83% with no trend — at n=6 those differences are indistinguishable
from noise, and the honest reading of the head is a flat ~53% (16/30).

S6 through S8 are 0 for 18. That is the result. Eighteen consecutive
items below heat 6, none carrying anything a topic doc would use. A true
signal rate of 20% would produce a clean sweep of 18 only 1.8% of the
time; the 95% upper bound on the cold-tail rate is about 15%.

The cliff falls between S5 and S6 — between rank 2390 and 2565, and in
heat terms almost exactly at 6.0.

## What the calibration says

CAL agreement was 3/6, and every miss ran the same way: the raters
called `signal` on items the pilot had called `no-signal`. Perfect
agreement on the three the pilot routed, zero on the three it rejected.

The pilot left no note on any of its three `no-signal` calls, so the
ledger cannot adjudicate. Reading them directly:

- **#1445 "Added V syntax support"** — the pilot was **wrong**. Buried
  under forty comments of flamewar about whether V is a scam, the owner
  rules that `.v` detects as V despite conflicting with Verilog, says he
  may reverse it because Verilog is more widely used, and notes users
  can set precedence themselves. That is a `filetype-detection` standing
  position, and a triager skimming the thread would see only noise.
- **#3795 "Enhance Tab Bar"** — leaning **rater**. A week of maintainer
  review on drag-versus-click semantics, what a click past the last tab
  should do, and dragging from a bufpane onto the tabbar. Behavioural,
  not stylistic.
- **#3783 "Add toggle & togglelocal"** — leaning **pilot**. Mostly
  wording and code nitpicks around one thin scoping rule (`toggle`
  applies to boolean options only). The rater minted a whole new topic
  for it, which is the dilution the rubric warns against.

So the boundary is genuinely fuzzy on long, dense PR-review threads, and
both judges are noisy there — not a clean one-directional leniency. The
uniform direction of the CAL misses is partly an artifact: only three
items in the whole pilot carry `no-signal`, and all three were drawn.

Two things follow. First, **the cliff is robust to the calibration
failure**. Whatever leniency the raters have biases them toward calling
signal, and they still found none in 18 cold items; a lenient rater
finding zero bounds the true rate from above. The disagreement is also
confined to exactly the kind of item the tail does not contain — the
cold strata are one-line bug reports and mechanical syntax files, where
judgment is easy.

Second, **the pilot's own `no-signal` calls are not trustworthy**, and
#1445 shows the miss mode is under-harvesting: a real decision buried in
a noisy thread. That is a triage-prompt problem, not a sweep-scope
problem, and it is worth fixing before spending 200+ spawns.

## Cost of truncating

Packing the untriaged ranking the way `triage` would (`BATCH_ITEMS=12`
or `BATCH_CHARS=200_000`, whichever binds first, with per-item size
modelled as `1693 + 571 × comments`, fitted on the 54 measured renders)
reproduces the full sweep at **323 spawns**, against the pilot's
independent estimate of ~331.

| cut at    | items | spawns | saved | measured signal kept |
|-----------|-------|--------|-------|----------------------|
| heat ≥ 24 | 385   | 34     | 289   | 15%                  |
| heat ≥ 15 | 914   | 78     | 245   | 41%                  |
| heat ≥ 11 | 1491  | 127    | 196   | 60%                  |
| heat ≥ 9  | 1849  | 156    | 167   | 83%                  |
| heat ≥ 8  | 2139  | 181    | 142   | 93%                  |
| heat ≥ 7  | 2269  | 191    | 132   | 97%                  |
| **heat ≥ 6** | **2601** | **219** | **104** | **100%** |
| heat ≥ 2  | 3847  | 323    | 0     | 100%                 |

The "signal kept" column reads 100% at heat 6 because the cold strata
contained no signal items, not because the true rate there is zero. A
fitted model puts a top-2601 budget at 82% of expected signal; see
`ghmem-heat-weights.md`.

Cutting at heat 6 drops a third of the sweep — 1246 items, 104 spawns —
and forgoes nothing the sample could detect. Everything below it is the
long flat plateau where heat stops discriminating anyway: 3266 of 3847
items sit at heat ≤ 2, tie-broken by issue number, which means the
ordering down there is close to arbitrary.

## The threshold is in provisional units

> Superseded. The wider draw in `ghmem-heat-weights.md` fitted the
> weights and kept the installed ones — the ranking does not change, so
> the rescaling this section anticipates never happens, and the 415
> boundary-sensitive items below are moot. What follows is what n=54
> said.

`HEAT_WEIGHTS` is marked PROVISIONAL, to be calibrated in subproject 4.
So "heat ≥ 6" is a number in units that do not exist yet: recalibration
rescales the score and reorders the ranking, and the threshold does not
survive either. The durable question is not where the cut sits but
whether the *set* of items it drops is stable.

Holding the budget fixed at the top 2601 items and reweighting:

| weight vector             | kept-set overlap | newly kept |
|---------------------------|------------------|------------|
| all five metrics equal    | 97%              | 77         |
| discussion-heavy          | 94%              | 144        |
| demand-heavy              | 94%              | 168        |
| comments only             | 91%              | 240        |
| participants only         | 91%              | 233        |
| span only                 | 79%              | 536        |
| related_items only        | 75%              | 641        |
| reactions only            | 70%              | 782        |

Across 200 random reweightings, each weight independently scaled over
[¼×, 4×], the kept set overlaps the baseline by a median of 96% and
never below 89%. The ranking is not fragile.

But the aggregate hides the part that matters. Of the 1246 items the
baseline drops, only **831 are dropped under every reweighting** — the
other 415 sit close enough to the boundary that some plausible weight
vector promotes them. And 611 items carry zero comments, zero reactions
and zero related items, which no non-negative reweighting of those three
can lift; they are cold by construction, not by calibration.

So the recommendation has a robust core and a soft edge:

- **~831 items** are outside any plausible sweep. Skipping them needs no
  calibration.
- **~415 items** are boundary-sensitive — and they sit exactly where the
  sample is weakest, in the S5/S6 transition where the measured rate
  goes 33% → 0% on six items a side.

## The weights themselves look wrong

> Superseded, and this section is where the caveat in its last paragraph
> proved decisive. At n=198, drawn without stratifying on the score,
> `related_items` is weak alone but earns its weight conditionally, and
> `comments` alone loses to the composite once weighted back to the
> corpus. See `ghmem-heat-weights.md`.

The 54 items carry both a full metric vector and a signal label produced
without routing, which makes this the first evidence in the project that
can speak to the weights rather than to a threshold on them. Sorting the
sample by one metric at a time and asking how much signal lands in the
top half, against a 41% base rate:

| sort by            | signal in top half | weight |
|--------------------|--------------------|--------|
| comments           | 70%                | 1.0    |
| current heat score | 67%                | —      |
| participants       | 63%                | 2.0    |
| reactions          | 59%                | 0.5    |
| span_years         | 56%                | 1.0    |
| **related_items**  | **41%**            | **3.0**|

`related_items` carries the heaviest weight in the vector and does
nothing — 41% is the base rate exactly, which is what a coin looks like.
`comments` carries the lightest non-trivial weight and is the best single
predictor in the set, beating the composite score it feeds.

Read this as a direction, not a fit. n=54, and the sample was stratified
on the current score, which controls the score's own spread by design
while letting individual metrics vary freely — that handicaps the
composite in this particular comparison. What survives the caveat is the
`related_items` result, because a metric weighted 3.0 landing on the base
rate is not a subtle effect.

## Recommendation

**Sweep the top ~2600 untriaged items, but recompute the boundary after
the weights are calibrated rather than freezing "heat ≥ 6".**

Cutting harder is unsupported. The head rates are flat within noise, so
there is no measured basis for preferring heat ≥ 9 (63 more spawns
saved, a nominal 17% of signal forgone) — the sample cannot resolve
differences that fine.

Three caveats on the boundary. It rests on 18 items. It lands where heat
is least informative, since 3266 of 3847 items sit at heat ≤ 2
tie-broken by issue number, so an item at 5 is not meaningfully colder
than one at 6. And the cold tail is where renders are smallest, so those
104 spawns are the cheapest in the sweep — the saving is spawn count and
wall-clock, not tokens proportional to items dropped.

**Sequencing.** Heat order is load-bearing beyond truncation: the
hottest item in a theme mints the topic name and later items join it,
and `record_verdict` refuses a second verdict for a routed item, so a
name assigned under wrong weights is permanent. That argues for
calibrating the weights *before* the sweep, not after — and it is the
truncation decision's cheapest dependency, since the sweep is what would
otherwise have to be redone.

The apparent circularity — calibrate heat from triage outcomes, but
triage order depends on heat — is what a read-only sample breaks. This
one already produced 54 labelled metric vectors at a cost of zero routed
items. A larger draw on the same design would produce enough to fit the
weights properly, and nothing about it consumes the corpus.

## What this settles, and what it does not

It settles the full-versus-partial question, and it settles it as
*partial*. A truncated sweep is a partial sweep, so a synthesis run's
byproduct worklist now has somewhere to go — interleaving becomes
coherent rather than redundant.

It does not settle the cold-first serving mode. That question was about
throughput on cold batches, and the recommendation is to not triage most
of them at all.

It does not license freezing a numeric threshold. The cut is stated in
provisional units, a third of the dropped set is boundary-sensitive to
reweighting, and the weights show a concrete defect — so the boundary
should be recomputed once calibration lands.

It raises one thing that was not on the list: the triage prompt misses
decisions buried in noisy threads. #1445 was found only because
calibration forced a second look at an item the pilot had already
closed. Before committing 219 spawns, the prompt should say that a
thread's noise is not evidence of its emptiness, and that a maintainer
ruling late in a long argument is exactly the kind of thing worth
routing.
