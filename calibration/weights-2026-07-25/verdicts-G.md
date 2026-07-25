slot: 7
number: 3507
verdict: no-signal
topic: -
confidence: medium
why: Community workaround discussion (preOpenFile, NewTabCmd) but no maintainer ruling or resolution.

slot: 16
number: 1053
verdict: signal
topic: new:default-keybindings-policy
confidence: medium
why: Owner rules default keybindings won't mimic bash/vim/emacs; users should rebind themselves.

slot: 20
number: 826
verdict: signal
topic: new:terminal-translucency
confidence: medium
why: Owner explains micro can't detect terminal translucency and compares to Vim's same limitation.

slot: 24
number: 2101
verdict: no-signal
topic: -
confidence: high
why: Root cause was docker's Ctrl-p/Ctrl-q detach sequence, not a micro design issue.

slot: 34
number: 1248
verdict: no-signal
topic: -
confidence: high
why: Bug traced to Terminal.app's missing shift-arrow escape sequences, a user config fix.

slot: 46
number: 992
verdict: no-signal
topic: -
confidence: medium
why: Long debugging thread finds a plugin-callback ordering bug but reaches no decision or rationale.

slot: 54
number: 3096
verdict: signal
topic: settings-reload-semantics
confidence: high
why: Maintainer explains settings.json is regenerated at startup and can't change due to plugin compatibility.

slot: 56
number: 684
verdict: no-signal
topic: -
confidence: high
why: Bug reproduced and acknowledged but no design rationale or decision recorded.

slot: 66
number: 2356
verdict: no-signal
topic: -
confidence: high
why: Support question answered by pointing to the existing tabstospaces option.

slot: 74
number: 2121
verdict: no-signal
topic: -
confidence: high
why: Bare bug report; owner asks for repro info, no resolution or rationale given.

slot: 78
number: 2471
verdict: no-signal
topic: -
confidence: high
why: Bug report with code pointer but zero maintainer engagement or response.

slot: 83
number: 930
verdict: no-signal
topic: -
confidence: high
why: Windows path-completion bug tracked and eventually fixed with no design discussion.

slot: 95
number: 2444
verdict: signal
topic: clipboard-behavior
confidence: medium
why: Detailed investigation of tmux/OSC52 clipboard delay behavior across terminals, durable evidence for an open problem.

slot: 104
number: 1617
verdict: no-signal
topic: -
confidence: high
why: Recurring bug reports over years with no maintainer position or fix confirmed.

slot: 106
number: 587
verdict: no-signal
topic: -
confidence: high
why: Crash reproduced and fixed with no design rationale discussed.

slot: 115
number: 3795
verdict: signal
topic: new:tab-bar-mouse-interactions
confidence: high
why: Maintainer and author iterate to concrete design decisions on tab-drag state and click behaviors.

slot: 121
number: 3765
verdict: signal
topic: highlighter-performance
confidence: medium
why: Maintainer diagnoses regression cause and explicitly deprioritizes a fix pending the parser rewrite (#3127).

slot: 124
number: 771
verdict: no-signal
topic: -
confidence: high
why: Merged bugfix PR with no discussion explaining a design choice.

slot: 125
number: 407
verdict: signal
topic: new:line-move-actions
confidence: medium
why: Owner requires implementation via Insert/Remove so line-move actions participate in undo/redo.

slot: 139
number: 1473
verdict: signal
topic: multi-cursor-support
confidence: low
why: Contested rationale on why Ctrl+D conflicts with duplicate-line in other editors but not micro; no maintainer weighed in.

slot: 147
number: 3005
verdict: signal
topic: settings-reload-semantics
confidence: high
why: Maintainer diagnoses settings.json persistence bug and discusses needed refactor of settings state model.

slot: 160
number: 1227
verdict: no-signal
topic: -
confidence: high
why: Mechanical syntax-file addition with no discussion.

slot: 163
number: 3219
verdict: no-signal
topic: -
confidence: high
why: Typo fix plus obvious defensive validation, no design discussion.

slot: 167
number: 1825
verdict: no-signal
topic: -
confidence: high
why: Straightforward display-positioning bugfix with no rationale discussion.
