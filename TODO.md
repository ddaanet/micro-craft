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

- [ ] Add a README and editor configs.
- [ ] `memory/MEMORY.md` is past the loader cutoff (~24,985 bytes), mostly
  the `ddaanet` tier's own block. Curate with `/gitlore:index-audit`.
