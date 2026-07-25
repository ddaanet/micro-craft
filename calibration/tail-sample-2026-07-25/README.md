# Tail sample, 2026-07-25

Raw material behind `docs/ghmem-tail-sample.md`, kept because
subproject 4 will want to re-derive the curve rather than trust the
write-up.

`heat.csv` is the ranking as it stood on the day, snapshotted because
heat moves with every `ghmem sync` and the strata are defined against
it. Everything here replays from that file plus the sqlite mirror.

| file                | what it is                                          |
|---------------------|-----------------------------------------------------|
| `heat.csv`          | the ranking the strata were cut from                 |
| `draw.py`           | stratified draw, seed 20260725 → `sample.json`       |
| `sample.json`       | the 54 items: stratum, rank, heat, blind slot, size  |
| `measure.py`        | renders each item, records its size                  |
| `split.py`          | 3-way rater split → `worklist-{A,B,C}.md`            |
| `verdicts-{A,B,C}.md` | what the three raters returned, verbatim           |
| `rubric.md`         | the signal/no-signal rubric they were given          |
| `analyse.py`        | verdicts → the per-stratum curve and CAL check       |
| `truncate.py`       | batch packing → spawn cost per truncation point      |
| `robustness.py`     | does the dropped set survive reweighting?            |
| `discriminate.py`   | which heat metrics actually separate signal          |

`measure.py` writes a `renders/` directory of `ghmem show` output. It is
not kept here — it is 394k characters of GitHub content that regenerates
from the corpus, and `sample.json` already records each item's size.

Rerun order: `draw` → `measure` → `split` → (rate) → `analyse`,
`truncate`. `draw.py` is seeded, so it reproduces the same 54 items
against the same `heat.csv`.

The raters are the one part that does not replay. Re-rating gives
different verdicts, which is the honest situation — the CAL stratum in
`sample.json` carries `truth` labels from the pilot precisely so a fresh
rating can be scored rather than assumed.
