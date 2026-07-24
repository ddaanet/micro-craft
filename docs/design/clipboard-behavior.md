---
description: >
  Why copy/paste in micro behaves differently locally vs. over ssh, how the
  internal/external/terminal clipboard backends and Ctrl-C vs Ctrl-Shift-C
  selections relate, and where maintainers draw the line between a micro bug
  and a terminal-emulator limitation.
---

# Clipboard behavior

## FR

1. **clipboard-behavior.FR1** — Micro supports three configurable clipboard
   backends selected by the `clipboard` option (settable globally or per
   buffer, e.g. `setlocal clipboard terminal` from the command bar):
   `internal` (an editor-local buffer with no external dependency, used
   automatically when no clipboard tool is found), `external` (the system
   clipboard via `xclip`/`xsel`, using the X `clipboard` selection rather
   than `PRIMARY`), and `terminal` (OSC52 escape sequences, which reach the
   local terminal's clipboard even when micro is running on a remote host
   over ssh).
   — zyedidia (owner), #93 2016-08-31: identifies the backing package uses
   `xsel --clipboard`; zyedidia (owner), #93 2016-09-01: "Copying within
   micro with Ctrl-C and Ctrl-V should work if you don't have xclip or xsel
   installed" (internal fallback); Andriamanitra (established contributor,
   14 accepted PRs), #93 2025-10-30: recommends `set clipboard terminal` for
   OSC52-capable terminals, noting "that feature didn't exist in 2016."

2. **clipboard-behavior.FR2** — Micro's Copy/Paste actions (Ctrl-C/Ctrl-V by
   default) operate on micro's own internal selection, a distinct entity
   from the terminal emulator's own selection/clipboard (reached via
   Ctrl-Shift-C/Ctrl-Shift-V or the terminal's native context menu). When
   the `mouse` option is enabled, mouse-drag selections are captured by
   micro rather than the terminal, so only the micro-side shortcut can copy
   them.
   — zyedidia (owner), #93 2019-02-06: full explanation of the two
   independent selection models and how terminal key delivery routes
   between them; Andriamanitra (established contributor), #93 2025-10-30:
   reaffirms "Micro's internal selections are not the same as the selection
   in the terminal."

3. **clipboard-behavior.FR3** — Over ssh, micro's default clipboard actions
   read/write the *remote* host's clipboard, not the local desktop's. A
   terminal-passthrough paste, bound to Cmd-V (macOS) / Ctrl-Shift-V
   (Linux), was added specifically so ssh users can paste from their local
   terminal's clipboard into micro without going through the remote
   clipboard.
   — zyedidia (owner), #93 2016-08-31 14:45: "If you are using ssh, micro
   will copy and paste from the server's clipboard, not from your desktop's
   clipboard... I'll close this issue once I implement that Cmd-V paste
   workaround"; zyedidia (owner), #93 2016-08-31 14:49: "Alright that should
   do it. You can paste using Cmd-V when over ssh."

## NFR

1. **clipboard-behavior.NFR1** — Micro's clipboard functionality is scoped
   to what the terminal emulator actually forwards to it; a gap caused by
   the terminal not sending an event, or not supporting a mechanism (X11,
   OSC52), is treated as outside micro's power to fix, not as a defect in
   micro. Maintainers require a reporter to name the exact behavior and
   compare it against another terminal program before accepting it as a
   micro-side problem.
   — dmaluka (maintainer since ~2024, 78 merges), #93 2025-10-13: "Micro
   does what the terminal allows it to do," and, pressing a vague report for
   specifics, "what exact problems with copy/paste exist in micro but don't
   exist in nano?"

## Limitations

- The `external` backend (`xclip`/`xsel`) requires a running X server; it
  does not work over a plain ssh session without X11 forwarding. The owner's
  only offered workaround at the backend level is `ssh -X`.
  — zyedidia (owner), #93 2016-08-31 14:51: "xclip needs an X window server
  to be running to work. I think you can use `ssh -X`... and maybe it would
  work then."

- Terminal-level selections (the Ctrl-Shift-C path) see only raw screen
  contents, not micro's buffer structure, so they can copy line numbers, the
  ruler, or other UI chrome along with the text — something a micro-native
  selection (Ctrl-C) never does because micro excludes those regions from
  its own selection model.
  — zyedidia (owner), #93 2019-02-06: "since the terminal has no idea the
  type of content it is displaying, terminal selections will copy line
  numbers or other UI elements... micro will not allow you to select line
  numbers or the status line."

- Rebinding a terminal emulator's own copy shortcut onto Ctrl-C (instead of
  the terminal's usual Ctrl-Shift-C) changes which of the two independent
  selection systems receives the keystroke, which can present as micro
  "breaking" when it is in fact a config collision between the terminal and
  micro's default bindings — inherent to how terminal key delivery works,
  not a micro defect to patch around.
  — zyedidia (owner), #93 2019-02-06: explains that when a terminal handles
  a key combination itself (as it does by default for Ctrl-Shift-C), it
  never sends micro that event, and that rebinding a terminal's copy
  shortcut onto Ctrl-C changes which program receives it.

## Open questions

- Is there any concrete, reproducible clipboard defect left in current
  (OSC52-era) micro, or has the remaining volume on this thread become
  purely terminal/configuration confusion? As of the most recent activity,
  dmaluka (maintainer) asked two 2025 reporters (atlas-eric, orazdow) to
  specify an exact failure and how it differs from another terminal
  program's behavior; neither supplied a reproducible counter-example in
  this thread. Andriamanitra (established contributor) holds that the
  system "has changed *a lot* since [2016]" and "should just work now" on a
  terminal with OSC52 support if `clipboard terminal` is set, and asked
  anyone still stuck to open a fresh issue against latest/nightly with
  environment details rather than continuing on #93. No maintainer has
  closed or otherwise resolved the thread since; it remains open with the
  front line at "show a reproducible gap on a current build," per dmaluka
  (#93 2025-10-13) and Andriamanitra (#93 2025-10-30).

## History

- 2016-05: #93 opened against copy/paste not working at all outside micro.
  zyedidia (owner) separates "internal-only" failures from cross-app
  failures and points to the Ctrl-V vs. Ctrl-Shift-V confusion already
  fixed once in #61.
- 2016-05-19: aerth (established contributor, 11 accepted PRs) notes
  shift+insert as an X11-native paste path that needs no `xclip`, an early
  sign that the "one true clipboard mechanism" framing was already too
  narrow.
- 2016-07-01: zyedidia closes the issue for lack of reproduction.
- 2016-08-31: reopened after several independent ssh-related reports.
  zyedidia diagnoses a primary-vs-clipboard X selection ambiguity in the
  underlying `clipboard` package, clarifies that ssh sessions target the
  *remote* clipboard by default, and ships the Cmd-V/Ctrl-Shift-V
  terminal-passthrough paste so ssh users can reach their local clipboard
  (FR3).
- 2019-02-06: zyedidia writes the canonical explanation of micro's dual
  selection model — terminal selection vs. micro selection, and which key
  combination reaches which depending on what the terminal forwards — which
  becomes the standing reference the rest of the thread gets pointed back
  to (FR2, both Limitations above).
- 2019 – 2024: a long tail of environment-specific reports and workarounds
  (installing or removing `xclip`, WSL/Windows Terminal keybinding clashes,
  discovering the `clipboard` setting via a third-party blog post,
  toggling the `ruler`). None of these carry maintainer standing; they are
  recorded here as community lore, not project policy, and none of them
  produced a new maintainer-level design statement.
- 2025-10-13: a fresh "copy/paste doesn't work" report from atlas-eric
  prompts dmaluka (maintainer) to push back for specifics rather than
  accept the complaint at face value (NFR1).
- 2025-10-30: Andriamanitra (established contributor) documents that OSC52
  terminal-clipboard support now exists and is the recommended `clipboard
  terminal` setting for capable terminals (e.g. iTerm2 ≥3.5.0), superseding
  much of the pre-2019 xclip/xsel-centric advice in this thread; asks
  anyone still affected to file a new, detailed issue against a current
  build. The thread stays open with no further maintainer resolution
  recorded.
- Related threads cross-referenced from #93 but not covered by this
  corpus snapshot: #61 (paste into micro from X11), #305 (clipboard over
  ssh), #2238 (Clipboard from SSH) — candidates for folding in in a future
  synthesis pass if they get routed here.
