---
description: >
  Whether micro's core should ship a file-tree sidebar / file browser /
  project pane, why six years of demand was routed to the filetree and
  filemanager plugins instead, the plugin-API limits (no mouse input to
  plugins, per-buffer scope) that keep those plugins from feeling native,
  and the recurring "terminal editor, not an IDE" scope line.
---

# File-tree sidebar

## FR

*(none — no file-browsing functionality has ever been merged into micro's
core for this request; the delivered capability lives entirely in plugins.
See NFR1 and NFR2.)*

## NFR

1. **file-tree-sidebar.NFR1** — A file browser / tree sidebar is outside
   the scope of micro's core. Micro is positioned as a lean terminal text
   editor competing with nano rather than with Atom/Sublime/VS Code, and
   the project treats "make it a file manager" as scope creep to be
   declined even when demand is large and sustained.
   — Enforced by behavior: #249 was opened 2016-08-31 and remained open
   and unimplemented in core through its last activity 2022-08-26, across
   339 reactions and 21 participants, with no core sidebar ever merged.
   Articulated by CamilleScholtz (established contributor, 17 accepted PRs
   at time of comment), #249 2016-08-31: "I've always been a fan of the
   'unix philosophy' (especially the do one thing and do it well rule),"
   preferring an external split (tmux + ranger) over an in-editor browser.
   The opposing framing was raised first by Hunter-Github (newcomer),
   #249 2016-08-31 — "Making it a file manager will lead to scope creep &
   bloat" — which is community sentiment, not standing, and is recorded
   here only because the standing-holder's statement echoes it.

2. **file-tree-sidebar.NFR2** — The sanctioned answer to this class of
   request is a plugin, and the project backs that route by hosting the
   resulting plugin under its own organization and distributing it through
   the plugin channel rather than folding it into core.
   — Enforced by behavior: the filetree plugin was developed outside core
   and taken into the micro-editor organization, cited in-thread as
   `micro-editor/filetree-plugin#2` by NicolaiSoeborg (newcomer at time of
   that comment; established contributor, 6 accepted PRs, by 2017-01-30),
   #249 2016-12-12. The `filemanager` plugin is subsequently reachable
   from micro's own plugin installer (`plugin install filemanager`),
   reported working by datdinhquoc (newcomer), #249 2018-10-09 — user
   confirmation of the distribution path, not a policy statement.

## Limitations

- Plugins could not receive mouse input from micro, so a plugin-provided
  file tree could not be clicked to open a file; navigation had to be
  keyboard-driven. This was the state of the code base as of early 2017
  and was given as the reason the requested click-to-open could not be
  built.
  — NicolaiSoeborg (established contributor, 6 accepted PRs), #249
  2017-01-30, answering DanielPower (established contributor, 1 accepted
  PR), #249 2017-01-24: "I can't see any obvious way to do it, in the
  current code base."

- A plugin's reach is practically confined to the current buffer, so a
  sidebar can be opened and closed as a split within one buffer's view but
  cannot cleanly persist as the same pane across every buffer — the exact
  property ("keeps open on the side, like sublime does it") that users
  asking for a sidebar want. This is a structural consequence of the
  plugin/view model, acknowledged as such rather than treated as a plugin
  bug.
  — ghost (established contributor, 7 accepted PRs), #249 2018-11-30: "any
  modifications plugins can do practically restricted to the current
  buffer, so split-view can be used to open/close pane since it is in the
  same buffer, but maintaining the same pane across all buffers just feels
  wrong."

## Open questions

- **Does a minimal file *listing* — as opposed to a file *manager* —
  belong in core?** The two standing-holders in this thread point in
  different directions and neither is the owner or a current maintainer.
  CamilleScholtz (established contributor, 17 accepted PRs) argued for
  keeping it out entirely and composing with external tools (#249
  2016-08-31). ghost (established contributor, 7 accepted PRs) argued the
  opposite for a reduced version: "simple file choosing (not managing)
  like that would be appropriate enough to not call this bloat but also
  convenient enough to be integrated as a standard feature. Maybe not as a
  side-bar (although possible) but maybe on another tab/split" (#249
  2018-11-14). No owner or maintainer comment appears anywhere in this
  thread, so the scope line here rests on contributor opinion plus six
  years of non-action, and has never been stated authoritatively.

- **What exactly is being asked for — file browser, or project pane?** The
  demand splits and the split was never resolved. handicraftsman
  (newcomer) asked for Atom-style Projects (#249 2016-08-31); 0-st
  (newcomer) voted explicitly ":-1: for the idea of integrating a file
  manager / :+1: for the idea of adding a project panel" (#249
  2018-10-09); mame98 (newcomer) framed it as a hidden-by-default,
  shortcut-toggled panel (#249 2016-09-01). All newcomer positions, so
  this is a live ambiguity in the request rather than a live design
  decision — but it means "add a file tree" has never had one agreed
  meaning in the thread.

- **Is the last argument on the thread answered?** The most recent
  comment, senotrusov (newcomer), #249 2022-08-26, attacks the IDE framing
  directly — proposing that features be judged on implementation and
  maintenance cost against fraction of users served, that a file list
  scores nothing like a debugger on that test, and that micro's
  install-anywhere-in-one-command value proposition is undercut by
  requiring a ranger/tmux workflow. It also floats ripgrep-backed
  content-based file listing as a second navigation axis. No one with
  standing has responded; the thread's last standing-holder statement
  dates to 2018-11-30. The front line is therefore unattended rather than
  contested.

## History

- 2016-08-31: dbkaplun (newcomer) opens #249 asking for a tree-view file
  browser sidebar. Within hours Hunter-Github (newcomer) posts the
  scope-creep objection (25 thumbs-down / 21 thumbs-up on that comment
  alone — the community is split, not aligned), noting micro's existing
  file/path autocompletion already covers much of the need and pointing at
  #243 (terminal panel) as related.
- 2016-08-31: CamilleScholtz (established contributor, 17 accepted PRs)
  gives the position the topic's scope norm rests on — do one thing well,
  compose with tmux + ranger instead (NFR1).
- 2016-09-01: the counter-framing lands and dominates on reactions:
  mame98's hidden-by-default toggleable panel (13 thumbs-up) and niieani's
  "micro is a new niche, a very light version of VS Code/Atom/Sublime, not
  a full-blown IDE" (49 thumbs-up, the single most-upvoted comment in the
  thread). Evidence of interest only; nothing was merged on the strength
  of it, which is precisely what NFR1 records.
- 2016-10-14: gordonbrander (newcomer) proposes the escape hatch — "Could
  this be done as a plugin? That would be a neat way to sidestep the above
  debate" (15 thumbs-up). This is the path the project actually took.
- 2016-12-12: NicolaiSoeborg announces a working filetree plugin with a
  screenshot, linking the micro-editor-org-hosted `filetree-plugin#2`
  (29 thumbs-up, 14 hooray). This is the de-facto resolution of the
  request (NFR2), even though the issue is never closed.
- 2017-01-24 – 2017-01-30: DanielPower asks for click-to-open on tree
  entries; NicolaiSoeborg answers that plugins have no route to mouse
  input in the current code base (Limitation 1). The request stalls there
  — no plugin-facing mouse API is proposed or landed in this thread.
- 2017-12-03 – 2018-06-26: the philosophical argument re-runs without
  standing on either side. id777 (newcomer) argues micro should be
  "command-line sublime text ... something nice out of box" (16
  thumbs-up); vviikk (newcomer) argues the opposite and votes to close,
  recommending `EDITOR` + ranger, tmux panes, or fzf (4 thumbs-down). No
  maintainer adjudicates.
- 2018-10-09: the plugin route becomes the thread's practical answer —
  `plugin install filemanager` plus a `filemanager.toggle_tree()` line in
  `init.lua`. Immediately, community lore about its rough edges
  accumulates: 0-st reports the toggle hijacks focus from the editor;
  datdinhquoc posts an `onViewOpen` workaround setting
  `tabs[curTab+1].CurView = 1` and links the upstream plugin issue
  (`filemanager-plugin#32`). All newcomer-level; recorded as lore, not as
  a project-accepted limitation.
- 2018-11-14: ghost (established contributor, 7 accepted PRs) cites
  mle/eon shelling out to `tree` as precedent and argues a minimal file
  *chooser* would be acceptable in core, possibly in a tab or split rather
  than a sidebar — the one standing-backed pro-core position in the thread
  (Open questions).
- 2018-11-30: franzflasch (newcomer) asks for a persistent sublime-style
  pane, noting slap has been dead since 2016. ghost answers with the
  structural blocker — plugin edits are effectively current-buffer-scoped,
  so a pane persisting across all buffers "just feels wrong" — and points
  at a third alternative plugin (`rvi64/files-plugin`) (Limitation 2).
  This is the last comment from anyone with standing.
- 2022-08-26: senotrusov (newcomer) reopens the argument on cost/benefit
  rather than category grounds, and adds a ripgrep-backed
  content-search-as-navigation idea. Unanswered; the issue remains open
  with no core implementation (Open questions).
- Cross-referenced from #249 but not in this corpus snapshot: #243
  (terminal panel), #285 (browse directory support), #320 (project pane),
  #461 (file navigation panel), #515 (View/Buffer refactor — the piece
  most likely to bear on Limitation 2), #823 (open directories), #1278
  (file explorer). Candidates for folding in if they get routed here.
