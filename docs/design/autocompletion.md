---
description: >
  What "autocomplete" means in micro — Tab-driven command-bar completion,
  buffer-word completion and the core completion framework — why
  language-aware completion is pushed out to plugins (Jedi, gocode, LSP)
  rather than built into core, and why the plugin-facing completion API
  promised in 2019 still has not arrived.
---

# Autocompletion

## FR

1. **autocompletion.FR1** — The command bar completes commands, filenames,
   and option names on Tab, presenting the candidate list in the status
   line. This predates the feature request thread and was already shipped
   when users started asking for it.
   — zyedidia (owner), #174 2016-09-01: "There is in fact autocompletion for
   commands... Just press tab and it should give you a list of suggestions
   in the statusline. It will also autocomplete filenames, and options when
   appropriate," adding "Maybe I should say that somewhere in the docs
   though."

2. **autocompletion.FR2** — Auto-closing of brackets, quotes and
   parentheses is treated as a distinct, far simpler feature than code
   completion, and was implemented first, within days of the request.
   — zyedidia (owner), #174 2016-06-20: "auto closing brackets, quotes,
   parentheses etc... is different from autocompletion for actual code
   keywords (and far easier to implement so that will probably get done
   first)"; shipped and confirmed working by the reporter, janniscx
   (newcomer), #174 2016-06-24: "Thanks for the new autoclose feature, it
   works very well." Tracked separately as #176.

3. **autocompletion.FR3** — Micro core provides simple buffer
   autocompletion — completing any word already present in the current
   buffer — bound to Tab, plus an in-core framework on which richer
   completion is meant to be built. This is the language-agnostic fallback
   the owner planned from the start, and it is what actually landed.
   — zyedidia (owner), #174 2016-06-20: "in that case micro can just fall
   back to simple buffer completion (where it will auto complete any word
   that is already used in the current file)"; zyedidia (owner), #174
   2019-12-27: "Simple buffer autocompletion (based on words in the current
   buffer) is now supported. The framework for autocompletion is also
   implemented."

## NFR

1. **autocompletion.NFR1** — Language knowledge does not live in micro's
   core. The committed architecture is a generic completion core in micro
   plus per-language completion supplied by plugins delegating to existing
   external engines (Jedi, gocode, later LSP servers); core never encodes
   what `def` means in Python.
   — zyedidia (owner), #174 2016-06-20: "I think it would be best to have an
   autocompletion core in micro, and implement specific completion for each
   language in plugins. Micro can't magically know that `def` is a Python
   statement, and instead can use a code completion engine built for
   Python, such as Jedi." Borne out by what shipped in 2019: a
   language-agnostic buffer-word completer and a framework (FR3), not any
   language-specific completer, and by the fact that the Go-specific core
   implementation offered in #977 is not what landed.

2. **autocompletion.NFR2** — Snippets are a separate feature from
   autocompletion and are kept on their own axis rather than folded into
   this design. A proposal to model completion on micro's syntax-file
   approach — regex patterns plus predefined insert actions — was
   reclassified by the owner as snippets and split off.
   — CamilleScholtz (established contributor, 13 accepted PRs at time of
   comment), #174 2016-06-20, proposes "simple files with regex patterns,
   and some pre-defined actions"; zyedidia (owner), #174 2016-06-21: "what
   you're looking for here is snippets... I think this is a separate issue
   from snippets" — split out as #175.

## Limitations

- There is no plugin-facing API for contributing completion candidates. The
  2019 framework is internal; the owner stated the plugin interface was
  still future work, and no maintainer statement since records it arriving.
  Users who want to complete from a non-buffer source (email addresses, a
  custom word list, a language server) have no supported hook.
  — zyedidia (owner), #174 2019-12-27: "hopefully soon we can have support
  for more complex autocompletion and a plugin interface" — stated as not
  yet done. Requested concretely and unanswered afterwards by Anachron
  (newcomer), #174 2020-04-16 (email-address completion) and, earlier in the
  same direction, jantb (newcomer), #174 2016-11-24 ("once it is exposed to
  plugins").

- The accepted cost of NFR1 is that anything beyond buffer-word completion
  requires a third-party plugin that the project does not own, review, or
  maintain. In practice this has meant several competing, partly-working
  LSP plugins rather than one supported path — a quality and support gap
  the project has chosen to live with rather than absorb language tooling
  into core.
  — zyedidia (owner), #174 2016-06-20 (the plugins-not-core split, NFR1);
  the resulting ecosystem is visible on-thread in #174 2022-04-08 through
  2024-03-06 (AndCake's micro-plugin-lsp, Andriamanitra's mlsp), but note
  that the quality assessments there come from participants without
  maintainer standing.

- Buffer-word completion is only as good as the current buffer: it cannot
  offer API members, function signatures, or symbols from other files. This
  is inherent to the fallback the owner specified, not an unimplemented
  part of it.
  — zyedidia (owner), #174 2016-06-20 and 2019-12-27 (both scope it
  explicitly to "words in the current buffer").

## Open questions

- **When, if ever, does the plugin completion interface land?** The last
  maintainer word is zyedidia (owner), #174 2019-12-27, "hopefully soon."
  Every subsequent status request on the thread — theAkito (newcomer)
  2020-02-18, Titaniumtown (newcomer) 2020-07-06, informeai (newcomer)
  2021-07-23, baris-inandi (newcomer) 2021-12-06, Yu-Vitaqua-fer-Chronos
  (newcomer) 2022-04-08 — went unanswered by anyone with standing. The
  front line is a stated intention with no owner follow-up in over five
  years; the thread's ~295 reactions are evidence of demand only, not of a
  commitment.

- **Does micro ever get first-party LSP support, or does LSP stay
  permanently in plugin territory?** Proposed by mikamiel (newcomer)
  2016-10-26 and seconded heavily (TobiaszCudnik (newcomer) 2018-02-22,
  "Definitive +1... Looks like a quick win," the single most-upvoted comment
  on the thread). njskalski (newcomer) offered to write the client in
  Go, #174 2017-11-30, and asked whether it would be welcome; no maintainer
  answered on this thread. zyedidia (owner) has never taken a position
  against LSP here — his only adjacent remark is #174 2020-08-09, that
  tabnine "looks like it could be a good as a solution to more advanced
  autocompletion than what currently exists" — but neither has he taken one
  for it. The substantive debate lives in #1138 (see the `language-server-protocol`
  topic); the front line here is silence from standing, against sustained
  demand.

- **Are buffer-completion word boundaries filetype-configurable?** szw
  (newcomer), #174 2020-08-01, asked how to make completion work for Lisp,
  Clojure and Scheme identifiers containing `-`. No maintainer or
  contributor replied; whether the fixed word-character class is intended
  policy or an unaddressed gap is unresolved.

- **Should #174 still be open?** The original reporter offered to close it
  as soon as autoclose shipped — janniscx (newcomer), #174 2016-06-24: "you
  can close this issue of course if you want to" — and the concrete asks it
  named were all satisfied by FR1–FR3. zyedidia (owner) declined to close
  it and never restated its remaining scope, so it has run since 2016 as a
  catch-all for "autocomplete like other editors," accumulating LSP,
  snippet, tabnine and plugin-API traffic that belongs to other threads.

## History

- 2016-06-20: #174 opened by janniscx (newcomer) asking for bracket and
  keyword completion. zyedidia (owner) answers the same day with the design
  that still governs the topic: core framework, per-language completion in
  plugins via external engines, buffer-word completion as the universal
  fallback, and autoclose first because it is a different and easier problem
  (NFR1, FR2, FR3).
- 2016-06-20/21: CamilleScholtz (established contributor, 13 accepted PRs)
  proposes a syntax-highlighting-style solution — regex pattern files with
  predefined insert actions. **Not adopted as autocompletion**: zyedidia
  (owner) reclassifies it as snippets and splits it to #175, pointing at the
  existing vim-snippets/UltiSnips corpora as a source. janniscx pushes back
  on snippet-file readability (the `substitute(vim_snippets#Filename()...)`
  form) and on the scope being far larger than requested; the split stands
  (NFR2).
- 2016-06-24: autoclose ships and is confirmed working (FR2).
- 2016-09-01: niieani (newcomer) asks for command autocompletion and is told
  it already exists on Tab (FR1). He then asks for fish-style inline
  ghost-text suggestion with arrow-key cycling and right-arrow accept; **no
  maintainer response** — the interaction model has never been taken up.
- 2016-10-26: mikamiel (newcomer) introduces LSP to the thread. janniscx
  (newcomer) objects on maturity grounds (2016-10-29), citing the Rust
  server's own "not yet ready for real use" warning. The objection is from a
  newcomer, not a policy statement, but it is the only recorded reasoning
  against LSP in this thread.
- 2016-11-24 / 2018-01-01: two independent requests that the completion UI
  be plugin-reachable — jantb (newcomer), and sum01 (established
  contributor, 3 accepted PRs), "Hopefully you made sure to expose the
  proper functions so plugins can easily add onto it." The theme predates
  the 2019 framework and outlives it.
- 2017-11-30: njskalski (newcomer) offers to implement an LSP client in Go
  and asks whether it would be welcome, plus how to shape it. **Stalled** —
  no reply from anyone with standing; nothing came of it.
- 2017-12-30 – 2018-01-03: a-h (newcomer) prototypes gocode completion as a
  Lua plugin driving `io.popen("gocode -f=json ...")`, hits the absence of a
  way to draw a candidate list from Lua, and concludes that the language-
  server route "doesn't need to be a plugin and could be added to the core."
  He then implements a working in-core completion popup with selection
  (well received on-thread: 19 👍 on the selection demo) and opens **PR #977,
  "Added autocomplete for Go, based on gocode, fixes #174."** a-h himself
  flags the problem with it — "Apologies for the Go-specific nature of the
  above. I appreciate that it's not a globally useful solution." **The PR
  did not become micro's completion implementation**: what landed two years
  later (2019-12) was language-agnostic buffer-word completion plus a
  framework, exactly per NFR1. No maintainer rejection rationale is recorded
  on this thread; the rationale that fits the outcome is the owner's
  standing no-language-knowledge-in-core position.
- 2018-02-22: TobiaszCudnik (newcomer) posts the thread's most-endorsed
  comment (+36) arguing LSP is "a quick win" now that servers exist for most
  languages. No maintainer reply.
- 2019-12-27: zyedidia (owner) ships simple buffer autocompletion and the
  completion framework, and states the plugin interface is still to come
  (FR3, and the first Limitation). This is the last substantive maintainer
  statement on the thread.
- 2020-02-18 – 2022-04-08: a five-year run of unanswered status pings and
  feature asks (per-filetype word boundaries, email-address completion,
  a tabnine port, "will native autocomplete be implemented?"). The only
  owner utterance in this stretch is 2020-08-09 on tabnine, which
  acknowledges the idea without committing to anything. Recorded as demand,
  not as project direction.
- 2022-04-08: terokarvinen (newcomer) reports that his own gopls-driving
  experiment has been superseded by AndCake's micro-plugin-lsp, a real
  JSON-RPC LSP plugin with rudimentary completion, installable in two lines;
  rochacbruno (newcomer) posts a working demo. This becomes the de-facto
  answer the thread gives to LSP requests — a third-party plugin, not a core
  feature (second Limitation).
- 2024-03-06: ryan-caesar-ramos (newcomer) cannot reproduce that demo —
  settings silently reverting, completions unrelated to the prefix,
  `ctrl+space` deleting the partial word. Andriamanitra (newcomer at time of
  comment; later an established contributor elsewhere in the corpus)
  redirects him off the micro tracker — "micro-plugin-lsp is a 3rd party
  plugin so a better place for the discussion would be its own repository"
  — judges its completion "too buggy to be usable," and points at his own
  alternative, mlsp. Last activity on the thread; no maintainer
  participation. The boundary being drawn here matches NFR1's consequence
  but carries no maintainer standing as stated, so it is recorded as
  history rather than as policy.
- Cross-referenced from #174 and not covered by this snapshot: #175
  (Snippets), #176 (Autoclose), #251 and #977 (gocode), #463 (Autocomplete
  box), #494 (Word tab completion), #794 (auto-complete from open buffers),
  #1138 (LSP support), #2199 (IPython autocompletion), #4009 (Code
  Completion). #4009 in particular suggests the request recurs on fresh
  threads a decade after #174 opened.
