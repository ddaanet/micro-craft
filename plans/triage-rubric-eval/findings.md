# Triage rubric eval — findings so far

## What prompted it

`docs/ghmem-design.md` Open questions carried "the triage rubric's
no-signal rate": the observed rate ran far under the 36.5% base rate
measured on the corpus, so either the rubric had drifted toward routing
everything or the routed sample was unrepresentative.

That framing cannot settle anything. It compares a single aggregate
rate against another single aggregate rate, and both readings produce
the same number — the "when accuracy is the wrong metric" failure. A
classification task with asymmetric error costs needs precision and
recall separately.

Worse, neither figure is ground truth. All 198 labels behind the 36.5%
are Sonnet raters (`docs/ghmem-heat-weights.md:35-37`), chosen because
that is `ghmem-triage`'s own tier. The one non-rater anchor was the
triage pilot's verdicts, which `docs/ghmem-tail-sample.md:91` concludes
are "not trustworthy". `ghmem-heat-weights.md:291` already names them
proxy labels. Nothing in the chain has ever been checked by a human, so
the denominator is not more reliable than the numerator.

## Pass 1 — note quality, no ground truth required

Each route carries a note naming the decision signal seen. That makes
the verdict evidence-anchored and checkable without re-reading any
thread: does the note cite a specific ruling, rationale or contested
position, or does it gesture? A route whose note cannot name what was
decided is a manufactured route by the rubric's own standard.

Graded against the 95 traces in `routes-snapshot.jsonl`, sampled
deliberately toward the weak end — the 10 shortest singleton notes, all
4 `no-signal` notes, and the first 14 singletons by number, 26 in all.

**Result: no manufactured routes found.** Note density is high (median
523 characters for the withdrawn singletons, 322 for the kept
multi-item routes), and every one of the ten *shortest* singleton notes
still names a specific decision with an actor and often a date. The
`no-signal` notes are the strongest in the set: two of the four
volunteer their own epistemic limits rather than asserting a clean
verdict.

**This does not vindicate the rubric.** It bounds one direction only.

- It grades the note, not the verdict. A note can accurately cite a
  real decision that still is not worth its own topic doc — the #3783
  dilution mode the tail sample adjudicated against the rater.
- It is circular in one respect: the note was written by the pass that
  made the verdict, so a confidently wrong triager writes a confident
  note.
- **Recall is structurally invisible to it.** You cannot grade a note
  that was never written. The under-harvesting failure the rubric was
  revised to fix — #1445, the forty-comment flamewar ending in an owner
  ruling that the pilot called `no-signal` — is exactly a recall
  failure, and only re-rating items that were *not* routed can measure
  it.

## What this redirects

The over-routing hypothesis is the weaker of the two readings on this
evidence. The withdrawn singletons were not junk; they carried real
institutional knowledge and each got its own topic name. That points
the defect at the *second* classifier, not the first.

Triage makes two decisions — signal vs `no-signal`, then which topic —
and every metric discussed so far grades only the first. The singleton
problem was a failure of the second, and no no-signal rate can see it.

## State change

The 57 items that were the only route to their topic have been
unrouted, on my human partner's instruction. `total=3877 triaged=38
routed=34 no_signal=4`; 71 topics down to 14, all multi-item, all
dirty. `unroute` appends rather than edits, so all 95 original verdicts
and notes remain in `corpus/routing.jsonl`, and `routes-snapshot.jsonl`
here holds them in read-ready form.

`docs/design/file-tree-sidebar.md` and `docs/design/lsp-support.md`
were the only synthesized singletons and are now orphaned — their
`Topic` rows are gone. The files were left in place: the content is
real, and their items may re-route to the same name.

## Pass 2 — recall, against a hand-labelled slice

Ground truth came from my human partner, blind to the Sonnet
verdicts: 24 slots drawn from the seven-rater calibration pool
(`tools/ghmem/calibration/weights-2026-07-25`) — 16 single-rater
`no-signal`, 6 single-rater `signal`, 2 where the raters split —
worksheet in `worksheet.md`, key in `slice.json`, drawn by
`draw_pass2.py`. `#1445` excluded as contaminated (named in both
rubrics as the canonical miss).

**What population this measures.** The 24 slots' verdicts in
`slice.json` come from the seven-rater calibration run
(`tools/ghmem/calibration/weights-2026-07-25/rubric.md`), not from
`ghmem-triage` itself — checked directly: zero of the 24 item numbers
appear in `routes-snapshot.jsonl`. That rubric is not independent of
the triage agent's judgment logic, though: its "hard cases" section
names the identical precedent that drove the Judgment-section revision
at `.claude/agents/ghmem-triage.md:98-120` — "a previous run got this
wrong on a forty-comment flamewar ... the owner settling a
filetype-precedence question" — and carries the matching
resolution-independence rule ("signal does not require resolution").
The two documents' judgment content matches regardless of which
commit landed first (`a09d19a`, the volume-is-not-content fix, predates
the calibration commit `349b25f` same day; `df4c955`, the
resolution-independence fix, postdates it — the content, not the
timestamp order, is what ties them). So the 24 verdicts measure a
rubric that already carries this revision's judgment logic, not a
pre-revision baseline — the gap below is the revision's residual, not
evidence against having made it.

**The no-signal bucket has a real recall hole.** Of the 16 items a
rater called `no-signal`, the hand label disagreed on 3 — `#1410`
(small feature request "accepted on first read", confidence medium),
`#2101` (bug attributed to another component, "verdict comes from
maintainer", high), `#51` (owner names the project's Gitter channel in
response to a request, "still current", high). That is an 18.75%
recall-failure rate in the cell built to detect exactly this failure
mode, against a rubric already carrying the under-harvesting fix. My
own observation, not a correction to the hand label: `#51` reads as
the softest of the three against the rubric's own
decision/rationale/contested-position test — a channel pointer rather
than a ruling — worth flagging separately rather than averaged in
silently.

**The signal bucket leaked one false positive.** `#3069`: a
contributor's bugfix merged with "no normative conversation beyond
code" — labelled `signal` by the rater, `no-signal` by the hand label.
Mechanical-change-only threads are where the *other* classifier edge
leaks.

**The two split slots: the human broke the tie, with real
reservations on both sides.** `#632`: hand label sided with rater D
(`no-signal`) over C (`signal`), but the `why` is three unanswered
questions about the closing chain ("is it unclear why the bug was
closed, did PR #1981 get merged, and issue #631 closed as fixed?"),
not confident rejection. `#3281`: hand label sided with rater D
(`signal`) over F (`no-signal`) at confidence `low` — "could be a
starting point for anyone interested in Carbon." Both `why`s also
complain the render didn't show who closed the item or what merged —
a `ghmem show` completeness gap worth a look, separate from this eval.
Read generously: a human given an ambiguous pair still landed on a
side rather than "genuinely unclear" both times, so rater disagreement
doesn't by itself mean an item is unlabelable — but neither case was a
clean call.

**Topic field, as a loose sanity check on the second classifier.** The
worksheet asked for a free-text topic description, not a fit judgment
against the 22-name taxonomy the raters saw — so this cannot test
topic-assignment the way pass 1 needed, only suggest where to look. Of
the 6 slots where hand label and rater agreed `signal` (`#3160`,
`#1115`, `#3993`, `#1451`, `#3281`, `#3096`), the subject matches in
4; it diverges in framing on 2 — `#3993` (human: "nerdfont file
icons"; rater: `new:core-vs-plugin-scope`) and `#3281` (human: "carbon
syntax"; rater: `new:syntax-highlighter-acceptance-policy`). Both
divergences are the same shape: the rater generalized a concrete
feature thread to a cross-cutting governance topic the human didn't
name. Suggestive of the pass-1 topic-assignment concern, not
conclusive.

**Overall**, 18/22 definite-key slots matched (81.8%); all 4
mismatches were in the two single-verdict buckets the recall question
was built to probe, none in the split pair.

### What this settles

The under-harvesting hypothesis is real, not just the single `#1445`
anecdote — a blind sample, rated under a rubric that already carries
that fix, still finds a comparable miss: point estimate 1-in-5 to
1-in-8 of sampled no-signal routes, but at n=16 with 2–3 hits the
interval is wide (roughly 4%–46% on the harder 2/16 reading) — enough
to call the failure mode real, not enough to call its rate settled.
Combined with pass 1 (no manufactured routes found among *made*
routes), the picture is: the rubric's note-writing discipline is sound
once it decides to route, but the signal/no-signal gate — even
post-revision — still passes some real maintainer rulings through as
if they were inert. That reopens the question pass 1 closed
provisionally — the defect is not purely in topic-assignment; the
first classifier has a measurable residual recall gap too, and the
topic field above hints the second classifier still has one as well.

## Open — needs my human partner

- Whether to revert the triage rubric revision
  (`.claude/agents/ghmem-triage.md:98-120`) no longer turns on missing
  evidence — pass 2 found the failure mode it targets is real and
  still present after the revision, though the rate is not pinned down
  at this sample size. The decision is now about the fix, not the
  diagnosis: sharpen the revision further (e.g. an explicit
  "maintainer ruling on a bug's cause/ownership counts as
  signal" rule), accept the residual as the price of not over-routing,
  or treat 24 slots as too few to act on without a larger confirmatory
  sample.
- The agreed pass-2 shape also called for an Opus judge grading the
  remainder of the 95-trace sample against this slice. Not run.
  Reason to consider skipping rather than doing it: the human slice is
  the ground truth this eval was built to get outside the
  Sonnet-judging-Sonnet loop, and an Opus judge grading the untouched
  remainder would extend sample size under Opus's own judgment, not
  under the human's — it answers "does Opus agree with itself more
  broadly", not "is the recall gap this large across more items". If
  the real goal is a bigger confirmatory sample, more human-labelled
  slots are the fix, not an Opus pass.
