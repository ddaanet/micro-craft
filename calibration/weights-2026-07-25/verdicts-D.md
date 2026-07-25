slot: 4
number: 3430
verdict: signal
topic: new:fastdirty-modified-detection
confidence: high
why: dmaluka calls md5 hashing a costly workaround for missing undo-stack-based modification detection and plans to replace it.

slot: 12
number: 126
verdict: signal
topic: terminfo-detection
confidence: medium
why: zyedidia states rxvt keybindings fail because his tcell fork lacks rxvt support — a stated platform constraint.

slot: 21
number: 632
verdict: no-signal
topic: -
confidence: high
why: Long frustrated complaint about softwrap scrolling with no maintainer engagement or stated rationale in this render.

slot: 29
number: 2472
verdict: no-signal
topic: -
confidence: high
why: Bare freeze reports on Termux, no reproduction detail beyond symptoms and no maintainer response.

slot: 30
number: 307
verdict: signal
topic: no-vi-mode
confidence: high
why: zyedidia explicitly declines a Vi mode, reasoning that users wanting Vi behavior should just use Vim.

slot: 35
number: 3069
verdict: signal
topic: new:pane-gutter-width-calculation
confidence: medium
why: PR explains and fixes flawed gutter/bufWidth/scrollbar arithmetic that let the ruler overwrite neighboring split panes.

slot: 40
number: 1410
verdict: no-signal
topic: -
confidence: high
why: Merged feature PR with only casual approval comments, no discussion of design rationale or alternatives.

slot: 42
number: 3281
verdict: signal
topic: new:syntax-highlighter-acceptance-policy
confidence: low
why: Maintainer defers merging a syntax file until the underlying language stabilizes, a small scoping rationale.

slot: 52
number: 2086
verdict: signal
topic: new:toggle-command
confidence: medium
why: dmaluka gives a full Lua toggle workaround and agrees native support is desirable; later closed once shipped.

slot: 59
number: 3034
verdict: no-signal
topic: -
confidence: high
why: Bug report with no discussion, resolved entirely by a separate cross-referenced PR.

slot: 62
number: 1061
verdict: no-signal
topic: -
confidence: high
why: Platform-specific FreeBSD/kbdcontrol bug resolved by user's own terminal config, not a micro design question.

slot: 70
number: 2553
verdict: no-signal
topic: -
confidence: medium
why: Non-maintainer opinion rejects the request; no maintainer weighed in and no real argument developed.

slot: 80
number: 2601
verdict: signal
topic: new:command-action-parity
confidence: medium
why: Maintainer asks why a quitall command is needed alongside the QuitAll action, an open design question.

slot: 91
number: 148
verdict: no-signal
topic: -
confidence: high
why: Rendering glitch fixed by an untraced commit; no discussion of cause or design.

slot: 101
number: 3984
verdict: signal
topic: new:delete-word-selection-semantics
confidence: high
why: Extended thread resolves selection-vs-deletion semantics, naming a new DeleteSelections action after debating cursor and direction edge cases.

slot: 105
number: 2877
verdict: no-signal
topic: -
confidence: high
why: Support question answered by quoting existing colors.md documentation on how skip works.

slot: 113
number: 980
verdict: no-signal
topic: -
confidence: high
why: Trivial typo/duplicate-line report in lua.go with no discussion.

slot: 114
number: 1021
verdict: no-signal
topic: -
confidence: medium
why: Scrollbar-dragging PR with only a crash bug report; no design rationale discussed.

slot: 128
number: 1540
verdict: signal
topic: new:markdown-embedded-syntax-highlighting
confidence: medium
why: zyedidia weighs scope tradeoffs for embedding language highlighters in markdown: capping languages vs. a runtime-loading plugin.

slot: 133
number: 3612
verdict: signal
topic: new:keybinding-action-separator-escaping
confidence: medium
why: PR fixes and documents that quoting/escaping lets keybinding command arguments contain reserved separator characters (&|,).

slot: 141
number: 3511
verdict: no-signal
topic: -
confidence: high
why: Small mechanical extension of textfilter to multicursors, approved without discussion or rationale.

slot: 144
number: 2973
verdict: signal
topic: line-wrap-options
confidence: medium
why: dmaluka analyzes Lua-based cursor-wrap prevention, noting softwrap/logical-line edge cases and CLI-toggle limitations for plugin options.

slot: 156
number: 2948
verdict: no-signal
topic: -
confidence: high
why: Reporter supplies a one-line theme patch, accepted and merged without any design discussion.

slot: 165
number: 1666
verdict: no-signal
topic: -
confidence: high
why: Feature request with no maintainer engagement, answered only by a pointer to an unofficial third-party plugin.
