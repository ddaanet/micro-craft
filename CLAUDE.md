# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A data and documentation repository, not a code project. It is the published output of a `ghmem` run over `micro-editor/micro` (GitHub issues, PRs, discussions, commits): a routing ledger, synthesized design-topic docs, and the calibration experiments that justified the pipeline's constants. There is no build, no test suite and no linter here.

`ghmem` itself is a separate project, installed at `~/.local/bin/ghmem`. Its source, its `just green` gate and `docs/ghmem-design.md` (cited by several docs here) are not in this repo. Run `ghmem --help` for the commands: `sync`, `rebuild`, `status`, `heat`, `show`, `triage`, `route`, `unroute`, `requeue`, `topic`, `close`, `index`.

## Pipeline and data flow

1. `ghmem sync` fetches the target repository into `corpus/fetch.jsonl`. The target comes from `corpus/target.toml`, not from the working directory.
2. `ghmem rebuild` builds `corpus/cache.sqlite` from the ledgers. `heat` ranks items from it, and `show` renders a thread from it.
3. `ghmem triage` mints a session token and serves packets. A worker classifies each item with `ghmem route`, which records a verdict (a topic name, or `no-signal`) and a mandatory note naming the decision signal seen.
4. `ghmem topic` assembles a topic's synthesis context. The synthesized doc is written to `docs/design/<topic>.md`. `ghmem close` records that synthesis as done.
5. `ghmem index` regenerates `docs/design/INDEX.md`. It lists every routed topic, with "not yet synthesized" where no doc exists yet.

Two things are not obvious from one file:

- **`corpus/routing.jsonl` is the source of truth and is committed.** It is an event log. Event types are `dispatched`, `route`, `unroute`, `snapshot`, `close` and `reenter`. Current state is derived by replaying it, so withdraw a verdict with `ghmem unroute` and never edit lines by hand. A fresh `ghmem rebuild` appends `reenter` events, and those are expected diffs, not corruption.
- **Gitignored on purpose** (`.gitignore`):
  - `fetch.jsonl` is raw third-party content and stays unpublished.
  - `cache.sqlite` is rebuilt from the ledgers.
  - `packets/` is scratch for served triage packets.

  A clean checkout therefore cannot run `ghmem show` or `heat` until it has run `ghmem sync` and `ghmem rebuild`.

Heat order is load-bearing. The hottest item in a theme mints the topic name, later items join it, and `route` refuses a second verdict for an already-routed item, so a wrongly named topic is permanent short of `unroute`. This is why the heat weights were calibrated before the sweep (see below).

## Topic docs (`docs/design/`)

Each topic doc has YAML front matter with a `description`, then the sections `FR`, `NFR`, `Limitations`, `Open questions` and `History`. Requirements are numbered `<topic>.FR<n>` and `<topic>.NFR<n>`, and each is followed by dated, attributed evidence (`— user (role), #issue date: …`). Attribution and standing (owner, maintainer, contributor) are part of the content, so keep them. When a topic is renamed, relabel its ids and cross-references, then regenerate `INDEX.md`. `INDEX.md` is generated ("Do not edit").

## Calibration and plans

- `calibration/tail-sample-2026-07-25/` and `calibration/weights-2026-07-25/` hold the raw material behind `docs/ghmem-tail-sample.md` and `docs/ghmem-heat-weights.md`. Each has a README with a file table and a rerun order, for example `profile → pool_prior → draw → measure → split → (rate) → fit → evaluate → compare`. Everything except the human or LLM rating step replays, because `draw.py` is seeded against the snapshotted `heat.csv`.
- The scripts are stdlib-only Python and run with `python3 <script>`. They are outside the lint and format gate (ruff excludes `calibration`), so nothing checks them; match the surrounding style by hand. `measure.py` writes a `renders/` directory of `ghmem show` output that is deliberately not committed.
- `verdicts-*.md` are what the raters returned, verbatim. Do not tidy them.
- Calibration runs are dated snapshots. Add a new dated directory for a new run instead of editing an old one. `heat.csv` is frozen on purpose, since heat moves with every `ghmem sync`.
- `plans/triage-rubric-eval/` is an evaluation of the triage rubric (`findings.md` is the write-up). It is frozen analysis, not a living doc.

## Commits

A gitmoji `commit-msg` hook is installed: conventional-commit prefixes (`feat:`, `fix:`, `docs:`, ...) are rewritten to emoji. Use the repo's existing style, e.g. `📝 regenerate the topic index`, `🔧 ghmem: land 22 triage routes ...`.

@memory/ddaanet/shared-claude.md
