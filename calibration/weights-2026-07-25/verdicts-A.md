slot: 1
number: 3509
verdict: no-signal
topic: -
confidence: high
why: Bare bug report fixed by a follow-up PR; only maintainer text is "Right." confirming the fix, no rationale.

slot: 9
number: 2569
verdict: signal
topic: new:root-process-terminal-close-cpu
confidence: medium
why: Owner diagnoses root cause (terminal can't SIGKILL a root-owned micro process) and states the fix applied.

slot: 17
number: 1416
verdict: no-signal
topic: -
confidence: medium
why: Merged PR but no maintainer rationale; just two contributors comparing UX of two overlapping multicursor features.

slot: 26
number: 326
verdict: no-signal
topic: -
confidence: high
why: Unreproducible crash report; no maintainer position on cause or expected behavior, thread just fizzles.

slot: 36
number: 2691
verdict: no-signal
topic: -
confidence: high
why: Support question answered by a non-maintainer pointing to custom bindings.json config; no maintainer engagement.

slot: 37
number: 2891
verdict: no-signal
topic: -
confidence: medium
why: Non-maintainer explains no built-in file browser exists and suggests a plugin; no maintainer decision recorded.

slot: 49
number: 537
verdict: no-signal
topic: -
confidence: medium
why: Closed via "Closed with #626" with no stated reasoning, despite an unaddressed suggestion to change defaults.

slot: 58
number: 3946
verdict: signal
topic: new:open-command-quoting
confidence: high
why: Merged PR removing double-parsing of open-command args; reviewer explains the old quoting behavior was broken and why.

slot: 67
number: 3780
verdict: no-signal
topic: -
confidence: medium
why: Feature request answered by community Lua workaround and closed as not-planned by the reporter, no maintainer input.

slot: 75
number: 2410
verdict: signal
topic: autocompletion
confidence: high
why: Owner agrees discoverability is a valid gap and the issue is later closed by a PR adding filetype completion.

slot: 76
number: 3016
verdict: signal
topic: atomic-file-save
confidence: medium
why: Reproducible case of symlinks being replaced by regular files on save, cross-referenced to an atomic-save-safety fix.

slot: 84
number: 2710
verdict: no-signal
topic: -
confidence: medium
why: Support answer: feature already achievable via custom binding, plus generic caveats about terminal key-sequence quirks.

slot: 86
number: 1051
verdict: signal
topic: new:terminal-keycode-limitations
confidence: low
why: Reporter self-diagnoses a tcell/terminal limitation preventing certain Ctrl-bindings, no maintainer engagement though.

slot: 97
number: 2613
verdict: signal
topic: new:shell-signal-handling
confidence: medium
why: Author explains a Go stdlib limitation (linked upstream bug) blocking a cleaner SIGINT fix, documents the tradeoff chosen.

slot: 107
number: 239
verdict: signal
topic: new:default-keybindings-scope
confidence: high
why: Owner explicitly declines to change default Ctrl-W/Ctrl-Q bindings, adds QuitAll instead, states reasoning.

slot: 111
number: 3229
verdict: no-signal
topic: -
confidence: high
why: New syntax file PR; review comments are purely mechanical (typo, unnecessary regex parens).

slot: 118
number: 3783
verdict: signal
topic: new:option-toggle-command-design
confidence: high
why: Long review debates toggle scope (boolean vs 2-choice options), terminology, and settings-code confusion, with maintainer rationale.

slot: 126
number: 3872
verdict: no-signal
topic: -
confidence: high
why: Bare bug report on multi-cursor commenting with an immediate linked fix PR; no discussion of design.

slot: 129
number: 3072
verdict: no-signal
topic: -
confidence: high
why: Reproducible tabmove/split bug report closed by a fix PR; no design discussion in the item itself.

slot: 132
number: 3352
verdict: signal
topic: new:action-chaining-return-values
confidence: high
why: Maintainer explains scoping rules for action return values and explicitly defers extending them to cursor actions, with reasoning.

slot: 140
number: 1115
verdict: signal
topic: new:regex-replace-capture-groups
confidence: high
why: Contributors dissect two real causes (shell-var expansion, missing capture expansion) and debate the $ escaping design.

slot: 150
number: 63
verdict: signal
topic: clipboard-behavior
confidence: high
why: Years-long contested debate over Ctrl-K conflating cut with delete and overwriting the system clipboard; maintainer offers workaround.

slot: 161
number: 1108
verdict: no-signal
topic: -
confidence: medium
why: Recurring "scrolling is slow" reports across years with no root-cause analysis or maintainer position offered.

slot: 168
number: 2383
verdict: no-signal
topic: -
confidence: low
why: Single unengaged report; reporter's own claim that regex highlighting can't handle nested emphasis, no verification or response.
