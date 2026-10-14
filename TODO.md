# TODO

## Carried from micro (repo-split 5.3, 2026-10-14)

- [ ] `docs/design/file-tree-sidebar.md` and `docs/design/lsp-support.md` are
  orphaned: no topic is named after either. Check whether each should merge
  into the `file-browser-sidebar` and `language-server-protocol` topics
  rather than be resynthesized. ghmem's planned orphan sweep would find them
  mechanically.
- [ ] Make micro-craft a Claude plugin pairing with the sibling `craft` plugin
  at `/Users/david/code/craft`, by the route ghmem took (Phase 3 of
  `/Users/david/code/micro/plans/repo-split/plan.md`). Waits on ghmem's
  `docs/design/` → `skills/<name>/SKILL.md` change, which decides the layout.

## Repo setup (repo-split 5.1–5.2)

- [ ] Tell micro's session that `ghmem-operating-the-pipeline` has landed
  once the commit is in. micro removes its own `ghmem-project`,
  `ghmem-ongoing-sync-not-snapshot` and `sqlalchemy-uow-hides-mutations`
  only after this fact and ghmem's both exist.
- [ ] Enable `ghmem@ddaanet` in `.claude/settings.json` (`enabledPlugins`; the
  auto-mode classifier refuses the write, so it is `/plugin install` from
  the user's own shell).
- [ ] Probe containment from the marketplace install (plan line 284 of
  micro's repo-split plan): method and expected verdicts are in
  `inbox/brief-memory-and-containment-probe.md` §2. Dispatch no ghmem
  worker here until it passes.
- [ ] Add a README and editor configs.
- [ ] `memory/MEMORY.md` is past the loader cutoff (~24,985 bytes), mostly
  the `ddaanet` tier's own block. Curate with `/gitlore:index-audit`.
