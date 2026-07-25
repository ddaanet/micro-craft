slot: 1
number: 724
verdict: no-signal
topic: -
confidence: high
why: Feature request declined with a pointer to existing docs on writing syntax files, no design rationale.

slot: 2
number: 192
verdict: no-signal
topic: -
confidence: high
why: Unrelated stray post, self-closed, asserts nothing about micro.

slot: 3
number: 828
verdict: signal
topic: new:default-help-keybinding
confidence: medium
why: Maintainer explains F1 conflicts with terminal emulators and disables it as default, directing users to CtrlG.

slot: 4
number: 1617
verdict: no-signal
topic: -
confidence: high
why: Open bug report on background process, no maintainer diagnosis or accepted fix.

slot: 5
number: 1677
verdict: no-signal
topic: -
confidence: high
why: Reproducible crash report fixed quickly; no discussion of intended behavior or design tradeoff.

slot: 7
number: 3273
verdict: signal
topic: atomic-file-save
confidence: high
why: Extensive maintainer debate settles the atomic-save algorithm, symlink handling, and backup/overwrite fallback rationale.

slot: 8
number: 1451
verdict: signal
topic: new:openbsd-pledge-sandboxing
confidence: medium
why: Owner raises unresolved concern about pledge() breaking micro via unknown syscalls; contributor adds threat-model considerations.

slot: 14
number: 372
verdict: signal
topic: no-vi-mode
confidence: medium
why: Contested back-and-forth on why micro doesn't need vim-style modal editing, with users arguing both sides.

slot: 18
number: 3900
verdict: no-signal
topic: -
confidence: high
why: Mechanical build-script logging tweak with no discussion of behavior or design.

slot: 20
number: 422
verdict: no-signal
topic: -
confidence: high
why: Feature PR posted with no maintainer engagement or discussion recorded.

slot: 21
number: 3999
verdict: signal
topic: new:command-arg-quoting-escaping
confidence: low
why: Contributor explains double-escaping is required due to command-prompt parsing plus regex parsing.

slot: 29
number: 23
verdict: signal
topic: mouse-escape-sequences
confidence: high
why: Owner diagnoses SGR vs X11 mouse-reporting offset difference and fixes it upstream in tcell.

slot: 31
number: 1
verdict: signal
topic: debian-packaging
confidence: high
why: Years-long thread with maintainer/packager rationale on dependency vendoring, licensing, and Debian NEW-queue process.

slot: 35
number: 2168
verdict: no-signal
topic: -
confidence: high
why: Crash traced to user running an outdated pre-2.0 build; no design discussion.

slot: 36
number: 1825
verdict: no-signal
topic: -
confidence: high
why: Straightforward display-positioning bugfix with no contested design rationale.

slot: 37
number: 4120
verdict: no-signal
topic: -
confidence: medium
why: Merged PR implements an already-decided option; review discussion is only about commit hygiene, not design.

slot: 39
number: 940
verdict: no-signal
topic: -
confidence: high
why: One-word typo fix in documentation.

slot: 40
number: 2903
verdict: signal
topic: new:alternating-line-colors
confidence: medium
why: Reviewer identifies correctness bugs (visual vs logical line, override interactions) and a cleaner refactor is adopted.
