---
description: >
  Why micro has no built-in Language Server Protocol client, the owner's 2020
  "next after the keybinding rework" roadmap statement that never landed, the
  out-of-core AndCake/micro-plugin-lsp Lua client (`micro --plugin install
  lsp`, gopls/pylsp/clangd/zls, alt-K hover / alt-D definition), and the
  reporter-initiated Won't Do close of the project's most-reacted feature
  request.
---

# LSP support

## FR

None. No in-core LSP client, and no LSP-specific plugin API, has ever been
merged; every LSP capability micro users have runs in ordinary Lua plugin
space. There is accordingly no shipped behavior in this corpus for a
functional requirement to describe.

## NFR

1. **language-server-protocol.NFR1** — Accumulated demand is not a scheduling input.
   Interest is expressed through reactions on the opening post, and repeat
   "+1"/bump comments that carry no new information are explicitly
   unwelcome; volume of either kind confers no claim on maintainer time.
   The project demonstrated this over the full life of #1138: 432 reactions
   (145 THUMBS_UP thread-wide), 40 comments and 20 participants across five
   years produced no core work, and the single owner-level roadmap
   statement in the thread was made in response to a *pessimistic* comment
   rather than to the demand.
   — Calinou (established contributor, 8 accepted PRs at time of comment),
   #1138 2019-06-09: "Please don't bump issues without contributing
   significant new information; use the :+1: reaction button on the first
   post instead"; zyedidia (owner), #1138 2020-04-25, replying to a "this
   will never happen" comment rather than to any of the preceding bumps;
   #1138 closed 2023-09-19 with no core implementation.

## Limitations

- A plugin-space LSP client is confined to micro's existing UI surfaces. The
  external plugin renders completions and hover output in the terminal's
  bottom status bar, because that is what the plugin API exposes — there is
  no popup or temporary-buffer surface for a plugin to draw a completion
  list into, as VSCode, Vim and Helix do.
  — raidenXR (established contributor, 1 accepted PR at time of comment),
  #1138 2022-07-29: "Lsp plugin might get a temp buffer for showing
  autocomplete, same as VSCode or Vim, Helix, instead of the bottom bar of
  the term?"

## Open questions

- **Should micro ship an LSP client, in core or bundled by default, and what
  would qualify the external plugin for official status?** The last position
  held by anyone with merge power is zyedidia's (owner) 2020-04-25 statement
  that LSP is "next on the list of things to do after a better keybinding
  system" — never retracted and never delivered in core. ShalokShalom
  (newcomer) asked the owner directly on 2022-04-09 whether it could be
  delivered by default, and again on 2022-07-07 ("What are the requirements
  for the lsp plugin to become an offical part of micro?", 4 EYES
  reactions); neither question drew a reply from anyone with standing. The
  only answer on the thread came from terokarvinen (newcomer, no standing),
  arguing bundling would be premature and would not solve the real cost
  since micro cannot install the language servers themselves. The front line
  is therefore unmoved since 2020: an owner intent on record, no maintainer
  restatement, and no stated bar for endorsement.

- **Does the Won't Do close stand as a project decision?** #1138 was closed
  2023-09-19 by glennsarti — the original reporter, standing newcomer — not
  by a maintainer, and the close drew 15 CONFUSED reactions. No one with
  standing ratified it, contested it, or reopened the issue in the roughly
  two years of subsequent activity (last active 2025-06-18). The live venue
  moved to discussion #3231, cross-linked 2024-04-17.

## History

- 2018-06-28: glennsarti (newcomer) opens #1138, split out of the
  auto-completion thread #174 (see the `autocompletion` topic), asking for an
  in-built LSP client for hover and completion.
- 2018 – 2020: steady demand with no maintainer engagement. On 2019-06-09
  Calinou (established contributor) tells a bumper to use reactions instead
  of comments, establishing the norm in NFR1; the bumper's objection that
  the issue would then "get forgotten" itself draws 5 THUMBS_UP.
- 2020-04-25: ShalokShalom (newcomer) declares the feature will never happen
  and points at Kate's new LSP client. zyedidia (owner) replies with the
  only maintainer-level roadmap statement on the thread: "I wouldn't say
  this will never happen. I think it will be next on the list of things to
  do after a better keybinding system. So hopefully we can have LSP support
  by the fall or the end of the year." It becomes the most-reacted comment
  in the thread (49 THUMBS_UP, 21 HEART, 12 HOORAY). No later owner or
  maintainer statement on LSP appears in this corpus, and no core client
  shipped.
- 2020-09-20: tobias1012 (newcomer) argues an LSP plugin "should be
  possible", qualified by needing better autocompletion integration — the
  first framing of the out-of-core path that the topic actually took.
- 2021-02-11: terokarvinen (newcomer) documents a stopgap that avoids LSP
  entirely: bind a key to `fexec gopls definition {f}:#{o}` via the quickfix
  plugin, exploiting the fact that some language servers also ship a CLI.
  Jump-to-definition only; no protocol client, no hover, no completion.
- 2022-03-08: AndCake (newcomer) publishes AndCake/micro-plugin-lsp, a
  third-party Lua LSP client, self-described as a proof of concept with
  hover and definition lookup, written without prior Lua or LSP experience.
  The most positively received comment on the thread after zyedidia's (24
  THUMBS_UP, 18 HEART). This, not core, is where LSP support for micro
  actually landed.
- 2022-04: independent community validation and hardening. terokarvinen
  confirms hover (alt-K), definition (alt-D), formatting (alt-F) and later
  references (alt-R) working against gopls and pylsp, contributes the
  plugin's help file and default settings so it works without editing
  `settings.json`, and by 2022-04-08 it is installable as `micro --plugin
  install lsp`. frak0d gets C/C++ working via clangd; raidenXR reports Zig
  (zls) working for everything except Ctrl-Space completion.
- 2022-04-13 – 2022-04-15: the first substantive defect list, all from
  frak0d (newcomer) — completion confirmed by arrow keys, completion
  insertion clobbering the rest of the line, hover output too wide for the
  screen on C++ signatures, backspace throttled to a few characters per
  second, and a redundant completion bar duplicating micro's built-in one.
  These are routed to the plugin's own tracker rather than pursued on
  #1138; the boundary is kept in practice even though no maintainer states
  it as policy.
- 2022-04-09 and 2022-07-07: ShalokShalom (newcomer) twice asks whether the
  plugin can become part of micro proper. Unanswered by anyone with
  standing (see Open questions).
- 2023-06-13: nandgator (newcomer) observes plugin development stalled a
  year earlier and asks whether interest has died; ShalokShalom attributes
  the stall to the plugin never being officially endorsed and recommends
  Helix instead. berkeleynerd (newcomer) pushes back that Helix's modal
  design targets a different audience than micro's, while conceding its
  zero-configuration LSP and treesitter integration is what micro lacks (7
  THUMBS_UP).
- 2023-09-14: ShalokShalom reports AndCake resumed plugin development.
- 2023-09-19: five days later, glennsarti (newcomer, the original reporter)
  closes #1138 himself — "Been over 5 yrs now... I think I can safely close
  this as - Won't Do." 15 CONFUSED reactions; no maintainer involvement in
  the close, before or after.
- 2024-02-23 – 2025-06-18: post-close tail. gabemeola (newcomer) muses about
  a "macro" fork with rich LSP and file-tree support (see the
  `file-browser-sidebar` topic); dev-nicolaos (newcomer) cross-links discussion
  #3231 for visibility, which is where the conversation now lives. No
  maintainer statement in this period.
