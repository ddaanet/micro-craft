---
description: >
  How micro got into apt — the seven-year path from "add to apt" to official
  Debian/Ubuntu repos, why upstream delegates distro packaging to volunteer
  Debian maintainers instead of running its own PPA or apt repo, how Debian's
  one-source-package-per-upstream rule collided with micro's vendored
  git-submodule dependencies, why the Debian build uses debian/rules rather
  than micro's makefile, and why distro versions lag upstream releases.
---

# Debian packaging

## FR

1. **debian-packaging.FR1** — Micro's README documents third-party
   package-manager install routes as they become available, rather than
   pointing users only at the project's own binary tarballs. The owner
   treats a working distro/package-manager formula as something to
   advertise upstream once it is stable enough to be worth advertising.
   — zyedidia (owner), #1 2016-09-07: "Yes I've added the instructions to
   the readme now. I didn't have them before because the brew formula
   didn't work so well with the nightly binaries, but it's fine now that
   there are released versions"; zyedidia (owner), #1 2016-09-09: "Micro is
   now in the official brew repository."

2. **debian-packaging.FR2** — The micro tree carries its own package-build
   scripts, independent of any distro's native packaging: `tools/build-deb.sh`,
   `tools/build-rpm.sh`, `tools/build-packages.sh`, `tools/micro.spec`, and a
   root `snapcraft.yaml`. These produce artifacts for direct distribution
   (release tarballs, .deb/.rpm, snap) and are what the owner points a
   would-be packager at first.
   — zyedidia (owner), #1 2018-01-29: "I have no experience in debian
   packaging but you may find the `build-deb.sh` script in the `tools/`
   directory useful"; tree listing in rajudev's #1 2018-02-03 comment
   confirming those files in `tools/` and `snapcraft.yaml` at the root;
   kyrofa (newcomer), #1 2019-09-04, pointing at the published snap while
   the Debian package sat in the NEW queue.

## NFR

1. **debian-packaging.NFR1** — Distribution through system package managers
   is downstream volunteer work. Upstream does not take on distro
   maintainership, and over seven years never adopted any of the
   self-hosted alternatives repeatedly proposed in the thread (a PPA, a
   project-run apt repository, openSUSE Build Service, fpm/debpkg-generated
   multi-distro packages). The owner's consistent posture is
   encouragement plus upstream unblocking, not ownership.
   — zyedidia (owner), #1 2018-01-29, on a volunteer offering to do it: "I
   don't believe anyone is currently working on this. I would really
   appreciate if you could get micro into apt though"; zyedidia (owner), #1
   2019-12-28, after acceptance: "What's the method for maintaining the
   version of micro distributed and updating it? ... is it something that a
   non-maintainer like myself could handle?" — the owner's self-description
   as a non-maintainer of the package is the standing position. None of the
   fpm (#1 2016-09-01, 2017-03-29), debpkg (#1 2017-03-29), PPA (#1
   2018-05-16), openSUSE Build Service (#1 2018-05-16) or self-hosted-repo
   (#1 2019-11-06) proposals drew an owner response or an upstream change.

2. **debian-packaging.NFR2** — Downstream packaging requests that are
   metadata or dependency-hygiene changes get honored upstream, usually
   within days. Licensing precision, vendoring a missing test dependency,
   dropping an unnecessary dependency, and merging a compile fix in a
   forked library were all done on request to unblock the Debian package.
   — zyedidia (owner), #1 2018-02-04: added goconvey to the vendor folder so
   the packager would not have to package it separately (commit
   1d24609e, acknowledged by rajudev #1 2018-02-04); zyedidia (owner), #1
   2018-02-04: published a per-file license breakdown for Debian's
   `debian/copyright` requirement after rajudev explained the policy;
   zyedidia (owner), #1 2018-02-08: "I have hopefully removed the need for
   `atotto/clipboard`"; zyedidia (owner), #1 2018-07-18: "I have updated the
   readme and license for zyedidia/clipboard"; zyedidia (owner), #1
   2019-02-12: merged zyedidia/tcell#11 on the packager's behalf.

3. **debian-packaging.NFR3** — Upstream does not restructure its dependency
   model to satisfy a distro's policy. Micro's dependencies are pinned as
   git submodules under `cmd/micro/vendor` for reproducibility, and that
   stayed true through the whole Debian effort; Debian absorbed the cost by
   packaging roughly fifteen dependencies separately instead.
   — zyedidia (owner), #1 2018-02-03: "All of micro's dependencies ... are
   stored as git submodules in `cmd/micro/vendor` so they can be pinned to
   the correct versions (Go's dependency management has issues)"; zyedidia
   (owner), #1 2018-02-04, pushing back on the de-vendoring requirement:
   "The vendor directory is supposed to make things simpler so the
   dependencies can just be provided with micro ... I don't really see why
   all the Go dependencies need to be packaged before/separately from
   micro. These libraries are being statically linked and are some closely
   coupled to micro." The rule was explained by stapelberg (newcomer), #1
   2018-02-10 — "In Debian, one upstream project maps to one Debian package
   ... Hence, we cannot use the vendor/ directory" — and upstream still did
   not change.

4. **debian-packaging.NFR4** — The supported build entry point is the
   makefile. Subdirectories of the tree are not standalone Go packages and
   are not meant to be built by a blanket `go install ./...`; `tools/`
   holds several independent `main` programs that the makefile invokes to
   stamp build date and version. A packaging build that bypasses the
   makefile is outside what upstream vouches for.
   — zyedidia (owner), #1 2019-02-12, on the Debian build failing with
   "main redeclared in this block" for `tools/` and `runtime/syntax`: "The
   tools directory should not be built as a go package, if you want to use
   the files there they should be built individually. Ideally you would use
   the `make install` command which will handle building and using the
   tools to set the date and build version"; zyedidia (owner), #1
   2020-05-28: "is there any reason why the makefile can't be used to
   package the debian version? This way I can make sure that the build tags
   and commands are correct if that ever gets updated again in the future."

## Limitations

- The in-tree `tools/build-deb.sh` is not a route into Debian and was not
  maintained as one. It produces an unofficial .deb at best; when the
  Debian packager tried it, it would not even execute (`Exec format error`,
  then `Syntax error: "(" unexpected` under `sh`), and upstream did not fix
  it in the thread. The package that reached Debian was built with
  `dh-make-golang` and the Go team's toolchain instead.
  — rajudev (newcomer; later a Debian maintainer of the micro package), #1
  2018-02-03, reporting both failures and noting "I am not packaging that
  way"; zyedidia (owner), #1 2018-02-03, replying on the goconvey question
  without addressing the script.

- The Debian package is built by `debian/rules`, not by micro's makefile,
  so upstream build details — build tags (including the `v2` module path
  from 2.0.4 on), build date and version stamping — have to be re-derived
  downstream and can drift. The shipped Ubuntu 20.04 package had exactly
  that class of defect.
  — zyedidia (owner), #1 2020-05-28: "I think the current version has
  problems with log.txt and version information. If building 2.0.4, also
  note that the build tags need to be updated to include a `v2` in the
  path"; utkarsh2102 (newcomer; Debian Developer and maintainer of the
  micro package), #1 2020-05-29: "The workflow and the build is different
  from how it works with Makefile. `debian/rules` ... is a Makefile but
  different than what the usual ones look like."

- Upstream has no upload rights and no direct lever on what version users
  get. Fixing a shipped distro version depends on the Debian maintainers'
  availability, and for an already-released stable distro the only path is
  backports. Push access was offered to the owner and never taken up,
  because it comes with the Debian packaging workflow attached.
  — zyedidia (owner), #1 2020-05-28, having to ask whether the Ubuntu 20.04
  version can be updated at all; utkarsh2102 (newcomer; Debian maintainer),
  #1 2019-12-29: "If you want to help, I can add you to the repository and
  give you push access there. However, there's a particular workflow that
  we follow"; utkarsh2102, #1 2020-05-29, concluding that backports were
  the only way to reach focal.

- Entry into Debian is gated on the whole dependency closure being packaged
  first, then on manual FTP-master review in the NEW queue, then on release
  freezes. Micro's own upload sat in NEW from 2019-02-23 to 2019-12-27 —
  ten months during which upstream had nothing to do and nothing to push
  on. This is the cost the project accepted by choosing the official-repos
  route over a self-hosted one (NFR1).
  — thread record: rajudev (newcomer), #1 2019-02-23 (in NEW), #1
  2019-02-12 (missed the buster freeze); jmkim (newcomer), #1 2019-09-03,
  linking the still-pending NEW entry; j-rivero (newcomer), #1 2019-10-28:
  "I can help with packaging or maintenance but once it is in the NEW queue
  I'm afraid that we need to wait."

## Open questions

- What triggers a Debian package update after an upstream release? No
  mechanism was ever established on the upstream side. rajudev (newcomer;
  Debian maintainer) proposed, #1 2020-02-11, that the owner "ping me and
  @utkarsh2102 on this issue after each release"; utkarsh2102 (newcomer;
  Debian maintainer) framed it the other way round, #1 2019-12-29, asking
  upstream to "make a release often. Then I can do timely updates."
  zyedidia (owner) asked how updating works three separate times (#1
  2019-12-28, 2020-02-10, 2020-05-28) and never got a process he could
  drive himself. The last recorded activity on the thread is that gap
  showing: a user asking for 2.0.11 on bullseye (#1 2022-08-20, trolzen,
  newcomer) and utkarsh2102 answering "Yes! I'll get to it in a bit.
  @gabrielapivetta, would you be interested in taking this, though?" with
  no recorded completion. Stale since 2022-08-20.

- Can `debian/rules` be made to drive micro's makefile, so upstream build
  tags and version stamping stay correct across distro rebuilds? Raised by
  zyedidia (owner), #1 2020-05-28. utkarsh2102 (newcomer; Debian
  maintainer) answered that the Debian workflow differs and pointed at the
  existing `debian/rules`, but neither converged on a change and neither
  side closed the question (NFR4, second Limitation).

## History

- 2016-04-17: #1 opened by earthboundkid (newcomer) — "It would be more
  convenient to install micro on servers if you could just run `apt-get
  install micro`." aerth (established contributor, 1 accepted PR), #1
  2016-04-18, calls getting new software into `jessie` tough and suggests a
  standalone .deb as the near-term answer, plus a wget/tar/install.sh
  recipe.
- 2016-09: the thread's first actual win is Homebrew, not apt.
  CamilleScholtz (established contributor, 17 accepted PRs) points at the
  wiki, Rowno (newcomer) asks for it in the README, and zyedidia (owner)
  adds it and then announces micro in the official brew repo (FR1).
  fpm-based "package everything painlessly" proposals from niieani
  (newcomer) and later xor-gate/rikvdh (newcomers, 2017-03-29) draw no
  owner response and go nowhere (NFR1).
- 2016-12: techtonik (newcomer) does the first real reconnaissance —
  Debian's Go packaging guidelines and `dh-make-golang` — and hits an
  unknown-hoster failure on `layeh.com`. zyedidia (owner) reproduces it
  past that point with `-allow_unknown_hoster` and reports eight
  build-dependencies missing from Debian, concluding "it shouldn't be too
  hard to fix the TODOs." That estimate turns out to be off by three years.
- 2017-03: GeigerCounter (newcomer) reports a tentative effort toward a deb
  and a PPA via PR #563 ("Debian package script"), with "no ETA." The
  thread records no further progress on that route, and the package that
  eventually reached Debian did not come from it.
- 2017 – 2018-01: a demand phase with no work in it — "Please work on this
  - I suspect that adoption could multiply by 10" (danmaz74, newcomer, 11
  thumbs-up), "The day I will be able to just `apt install micro` I'll do
  it on all my servers" (ziggy42, newcomer, 6 thumbs-up). techtonik
  (newcomer), #1 2017-10-08, names the actual blocker correctly: "The only
  way for this to be fixed is for somebody who uses Debian derived OS daily
  to step up to be Debian maintainer." The thread's 201 reactions and 33
  participants never moved this; one volunteer with Debian standing did.
- 2018-01-29/30: rajudev (newcomer here, an existing Debian contributor)
  volunteers, explicitly scoping the goal past "make a deb" to `apt install
  micro`. zyedidia (owner) welcomes it. The Debian ITP bug (#888813) is
  filed the next day.
- 2018-02: the vendoring collision. rajudev explains Debian's rule that
  every dependency must be packaged separately; zyedidia adds goconvey to
  vendor and produces a per-file license breakdown (NFR2) but pushes back
  on de-vendoring — "I don't really see why all the Go dependencies need to
  be packaged before/separately" (NFR3). stapelberg (newcomer) gives the
  authoritative reason: one upstream project maps to one Debian package, so
  security fixes have exactly one update point. Upstream did not change;
  Debian absorbed the cost, and a dependency tree of ~15 packages became
  the critical path.
- 2018-05-16: the self-hosting alternatives surface and die in one
  exchange. marco-lavagnino (newcomer) suggests a PPA "rather than wait for
  Debian Mantainers"; oct2pus (newcomer) counters that a PPA only helps
  Ubuntu and that "working on getting it in the official Debian
  repositories would be more beneficial than doing that anyways" (4
  thumbs-up); simoniz0r (newcomer) offers openSUSE Build Service. No owner
  engagement, no adoption (NFR1).
- 2018-07 – 2018-10: dependency grind. Roughly half the tree packaged;
  upstream fixes licensing metadata on zyedidia/clipboard and is asked to
  do the same for zyedidia/pty (NFR2).
- 2019-02: the build-failure cluster. The Debian build fails first on a
  stale `zyedidia/tcell` (missing `EscSeq`/`EventRaw`), which zyedidia
  merges a fix for while correctly diagnosing that the packager's tcell
  checkout is simply out of date, then on `main redeclared` in `tools/` and
  `runtime/syntax` — the makefile-vs-`go install ./...` mismatch (NFR4).
  The buster freeze lands on 2019-02-12, so micro misses that release.
  2019-02-23: micro reaches the Debian NEW queue.
- 2019-02 – 2019-12: ten months in NEW. Periodic "any news?" traffic, a
  snap suggested as a stopgap (kyrofa, newcomer) and rejected as
  impractical inside Docker (damien-git, newcomer), a self-hosted apt repo
  floated (sbrl, newcomer) and ignored, and j-rivero (newcomer) confirming
  nobody can accelerate NEW.
- 2019-12-27: utkarsh2102 (newcomer here, a Debian Developer) announces
  micro accepted into Debian unstable. rajudev is credited with the bulk of
  the work; both become maintainers of the Debian package.
- 2020-01 – 2020-02: migration to testing/bullseye (2020-01-14, delayed by
  a piuparts bug), buster-backports (2020-01-21, requiring all build
  dependencies backported too), Ubuntu 20.04 focal (2020-01-26), and micro
  2.0.0 uploaded to the archive (2020-02-12). rajudev opens #1506 to add
  Debian/Ubuntu install instructions and a Debian version badge to the
  README. The owner asks how updates work; the answer is "it's the
  maintainer's work" plus an offer of push access under the Debian
  workflow (Limitations, Open questions).
- 2020-05: the first staleness bite. zyedidia (owner) reports that the
  version shipped in Ubuntu 20.04 has log.txt and version-information
  problems, flags the `v2` build-tag change needed for 2.0.4, and asks
  whether the makefile could drive the Debian build. utkarsh2102 explains
  `debian/rules` is a different build script, backports tcell and micro
  2.0.4, and the makefile question is left unresolved (NFR4, Open
  questions).
- 2022-08-20: the last recorded activity — a request to update bullseye to
  2.0.11, answered with an intent and a re-delegation, no completion in the
  record. The issue is closed.
- Cross-referenced from #1 but not covered by this corpus snapshot: #562
  ("Why there is no deb file for debian based distros"), #563 ("Debian
  package script"), #583 ("Can I install Micro ... using APT"), #1093
  ("Terminal entry not found", which pravi flagged as affecting the
  packaged build), #1506 (README update). Candidates for folding in if
  they get routed here.
