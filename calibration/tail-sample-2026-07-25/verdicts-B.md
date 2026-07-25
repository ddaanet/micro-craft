slot: 6
number: 1373
verdict: no-signal
topic: -
confidence: high
why: Bare regex bug report, no maintainer engagement or explanation of intended behavior.

slot: 9
number: 1365
verdict: signal
topic: clipboard-behavior
confidence: medium
why: Maintainer explains why WSL clipboard detection is hard and why OSC52/`clipboard terminal` is the workaround.

slot: 10
number: 1136
verdict: no-signal
topic: -
confidence: medium
why: Bug + contributor's yaml fix suggestion, but no maintainer decision or general rationale.

slot: 11
number: 691
verdict: signal
topic: new:keybinding-terminal-collisions
confidence: medium
why: Maintainer explains terminal-level CtrlSlash/CtrlUnderscore keycode collision and proposes an alias fix.

slot: 13
number: 3848
verdict: no-signal
topic: -
confidence: high
why: Trivial regex-typo fix to filetype detection, no design discussion beyond "seems like a mistake".

slot: 15
number: 3736
verdict: signal
topic: settings-reload-semantics
confidence: high
why: Maintainers debate remote-reload approaches (socket, busy loop, fsnotify) and explain why each is risky.

slot: 19
number: 2616
verdict: signal
topic: statusline-indicators
confidence: medium
why: Maintainer accepts a new `cols` directive and flags an unresolved modified/readonly coupling question.

slot: 22
number: 1861
verdict: no-signal
topic: -
confidence: high
why: Pure syntax-file diff with no accompanying discussion or rationale.

slot: 24
number: 1877
verdict: no-signal
topic: -
confidence: high
why: One-line doc typo fix (info.json to repo.json), mechanical.

slot: 26
number: 331
verdict: no-signal
topic: -
confidence: high
why: Unanswered user question about custom colorschemes, no maintainer response.

slot: 30
number: 3623
verdict: signal
topic: new:replace-selection-adjustment
confidence: medium
why: Contributor and maintainer weigh deferring selection-adjustment logic pending a broader search-API rework.

slot: 32
number: 4102
verdict: no-signal
topic: -
confidence: high
why: Mechanical syntax-rule removal; brief reviewer question resolved trivially, no design rationale.

slot: 38
number: 1445
verdict: signal
topic: filetype-detection
confidence: medium
why: Maintainer decision to give `.v` extension to V over Verilog, with stated rationale and future-change caveat.

slot: 43
number: 4128
verdict: no-signal
topic: -
confidence: high
why: Large AI-autocomplete PR closed with zero discussion or stated rationale in the record.

slot: 44
number: 3295
verdict: no-signal
topic: -
confidence: medium
why: Long troubleshooting thread pinpoints a config bug but yields no maintainer design position.

slot: 45
number: 3131
verdict: signal
topic: new:syntax-highlighting-engine-limits
confidence: high
why: Maintainer explains why region-based syntax defs can't handle self-referential regex and why a Sublime-style rewrite isn't planned.

slot: 46
number: 2940
verdict: no-signal
topic: -
confidence: high
why: Bug traced to a duplicate/terminal-shortcut conflict, no design position taken.

slot: 47
number: 3957
verdict: no-signal
topic: -
confidence: high
why: Mechanical build-tooling cleanup removing an archive made obsolete by an external project change.
