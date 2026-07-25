slot: 6
number: 1312
verdict: no-signal
topic: -
confidence: high
why: Bare UTF-16 support question closed by pointing at the existing `encoding` option.

slot: 14
number: 157
verdict: signal
topic: new:cursor-view-centering
confidence: medium
why: Owner rejects followview implementation, then closes it as obsolete once the built-in Center action covers the need.

slot: 15
number: 3281
verdict: no-signal
topic: -
confidence: medium
why: Mechanical syntax-file PR deferred one line because Carbon is still experimental; no lasting policy stated.

slot: 23
number: 1547
verdict: no-signal
topic: -
confidence: high
why: Mechanical colorscheme addition; feedback is cosmetic tweaks, no design rationale.

slot: 33
number: 2586
verdict: no-signal
topic: -
confidence: high
why: Unresolved SSH keybinding bug report, no maintainer engagement or explanation.

slot: 44
number: 394
verdict: signal
topic: new:unicode-character-width-rendering
confidence: medium
why: Contested, evidence-backed discussion of zero-width rune rendering and cursor placement, left unresolved.

slot: 47
number: 281
verdict: no-signal
topic: -
confidence: high
why: Mechanical syntax-file filename-pattern tweak, no discussion.

slot: 55
number: 2041
verdict: signal
topic: filetype-detection
confidence: high
why: Explains why *.h detection is nondeterministic/order-dependent between C, C++, and Objective-C; unresolved ambiguity.

slot: 65
number: 233
verdict: no-signal
topic: -
confidence: medium
why: Feature merges with only informal naming chatter; owner later replaced it with `-startpos` without stated rationale here.

slot: 72
number: 2807
verdict: no-signal
topic: -
confidence: high
why: Support question resolved by pointing at existing `clipboard`/OSC52 docs.

slot: 73
number: 44
verdict: no-signal
topic: -
confidence: high
why: Mechanical PR splitting stdout/stderr buffers, no discussion.

slot: 82
number: 309
verdict: signal
topic: new:keyboard-layout-input-handling
confidence: high
why: Owner gives durable technical rationale: terminals send characters not scancodes, so layout-dependent prompts can't be fixed.

slot: 85
number: 5
verdict: signal
topic: multi-cursor-support
confidence: high
why: Long-running feature thread with real design decisions on bindings, ctrl+d matching, and cursor-merge bugs.

slot: 94
number: 3189
verdict: signal
topic: indent-display-options
confidence: medium
why: Maintainers debate then decide to force-disable tab/space error highlighting in help buffers, with stated reasoning.

slot: 96
number: 3426
verdict: no-signal
topic: -
confidence: high
why: Support issue closed once explained the reporter was on an outdated release.

slot: 103
number: 2960
verdict: no-signal
topic: -
confidence: medium
why: Crash triage and root-cause trace for a nil-screen panic; implementation bug fix, not a design decision.

slot: 117
number: 377
verdict: no-signal
topic: -
confidence: high
why: One-line mechanical addition of a backtick pair to autoclose.

slot: 119
number: 3600
verdict: no-signal
topic: -
confidence: high
why: Mechanical dependency import-path swap, no discussion of behavior.

slot: 123
number: 2304
verdict: no-signal
topic: -
confidence: high
why: Feature-request list with no maintainer engagement in the thread itself.

slot: 138
number: 2102
verdict: no-signal
topic: -
confidence: high
why: User-to-user workaround thread (TERM=xterm-256color) with no maintainer position.

slot: 146
number: 4021
verdict: signal
topic: filetype-detection
confidence: high
why: Maintainer explains why a config-filetypes.json is redundant given existing detect/signature mechanism, citing related ambiguity issues.

slot: 151
number: 4067
verdict: no-signal
topic: -
confidence: high
why: Bug traced to an upstream gopher-lua dependency defect; no design discussion.

slot: 158
number: 3219
verdict: no-signal
topic: -
confidence: high
why: Obvious typo fix (filename→filetype) nobody would need documented.

slot: 159
number: 25
verdict: signal
topic: line-wrap-options
confidence: high
why: Owner commits to soft wrap, later ships `set softwrap on` and a toggle command; canonical feature history.
