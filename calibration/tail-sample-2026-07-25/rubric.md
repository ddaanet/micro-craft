# Signal rubric — read-only tail sample

You are classifying corpus items from the micro editor's GitHub history.
This is a **measurement run, not a triage run**. Nothing you say is
recorded as a verdict; you are estimating what a triage pass would
harvest from this part of the corpus.

## The question

For each item: **would a triage pass extract anything a topic doc would
use?**

A topic doc is a synthesized design document about one recurring concern
in micro — what was decided, by whom, and why. It is written for someone
who needs the project's standing position on that concern without
reading five years of threads.

## `signal`

The item carries at least one of:

- A **decision** — a maintainer accepting, rejecting, or scoping a
  behaviour. "Won't do, use a plugin" is a decision. So is a merged PR
  that changes user-visible behaviour and says why.
- A **rationale** — an explanation of why micro behaves as it does, or
  why an obvious alternative was not taken. Constraints count: "we can't,
  because tcell does X".
- A **contested position** — two or more people arguing a design
  question, even unresolved. The disagreement itself is the content.
- **Durable evidence** for an open question — a reproducible case, a
  platform matrix, a measurement — that a doc would cite.

Signal does not require resolution. An open, well-argued issue is signal.
Signal does not require length; a two-line maintainer ruling is signal.

## `no-signal`

The item is one of:

- A bare bug report or crash with no discussion of what the behaviour
  ought to be, and no maintainer position.
- A mechanical change: syntax-file addition or tweak, dependency bump,
  typo fix, README edit, CI plumbing, version bump.
- A support question answered by pointing at existing docs.
- A duplicate, a dead one-liner, spam, or a thread that never got a
  reply and asserts nothing beyond "this would be nice".
- A feature request with no engagement, no rationale beyond the request
  itself, and no maintainer response.

`no-signal` is the expected default for most of this corpus. Do not
manufacture signal to avoid it. A thin item routed into a topic dilutes
that topic; the cost of a false `signal` is real.

## The hard cases

- **Popular but empty**: many reactions, no argument. Reactions alone are
  demand, not rationale. Call `no-signal` unless something in the thread
  says why or why not.
- **Long but circular**: a hundred "+1"s and no position. `no-signal`.
- **Short but decisive**: closed by a maintainer with one sentence of
  reasoning. `signal`.
- **A PR that just does the thing**: if the diff changes behaviour and
  the thread explains the choice, `signal`. If it is an obvious fix
  nobody would document, `no-signal`.

## Existing topics

If an item has signal, say which of these it would feed, or propose a
new topic name. This is a judgment about fit, not a routing action.

atomic-file-save, autocompletion, backup-filename-encoding,
clipboard-behavior, debian-packaging, default-syntax-fallback,
file-tree-sidebar, filetype-detection, find-next-ux,
highlighter-performance, indent-display-options, line-wrap-options,
lsp-support, mouse-escape-sequences, multi-cursor-support, no-vi-mode,
project-governance, regex-search-line-boundary-matching,
scroll-input-lag, settings-reload-semantics, statusline-indicators,
terminfo-detection

## Output

One block per item, in slot order, nothing else:

```
slot: <n>
number: <item number>
verdict: signal | no-signal
topic: <existing topic name> | new:<proposed-name> | -
confidence: high | medium | low
why: <one sentence, under 25 words>
```

`topic:` is `-` when the verdict is `no-signal`. Use `confidence: low`
freely — it is data, and a stratum full of low-confidence calls is
itself a finding.
