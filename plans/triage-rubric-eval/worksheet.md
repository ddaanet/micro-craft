# Pass 2 worksheet — hand-labelled ground truth

Read each thread to its end and record a verdict. The Sonnet rater's own
verdict is deliberately withheld; it is in `slice.json`, which is the key.

The rubric is `tools/ghmem/calibration/weights-2026-07-25/rubric.md` —
the same one the raters saw. In short: **would a triage pass extract
anything a topic doc would use?** A decision, a rationale, a contested
position, or durable evidence for an open question is `signal`. A bare
bug report, a mechanical change, a support question, a dead one-liner,
or an unengaged feature request is `no-signal`.

Fill in the `verdict:` and `why:` lines below each thread. Leave
`confidence:` as one of high / medium / low — a slot full of `low` is
itself a finding.

---

## slot 1 — #632

# #632 View doesn't center on cursor/current line with softwrap

- state: CLOSED
- kind: issue
- author: GeigerCounter (established contributor; 4 accepted PRs at time of comment)
- created: 2017-04-19T20:40:31+00:00
- updated: 2021-04-07T20:18:51+00:00

When using softwrapping, if the line wraps more than a few times the view can lose track of the cursor and center in the wrong place. This also causes a stuttering effect for particularly long lines and/ or lines at the end of the file. Worst case scenario and the line currently being edited can be hidden off-screen. Moreover it would be useful to be able to remap the arrow keys to move up and down the lines of the softwrapping - that is rows of the view - rather than moving up and down lines of the buffer.

Commit hash: 8524cbc
OS: Ubuntu 14.04
Terminal: ConnectBot + screen


## Timeline

### 2019-02-16T02:59:36+00:00 — frabjous (newcomer)

The poor implementation of soft wrapping (and nonexistence of word wrapping) is certainly the biggest flaw in micro. In addition to the problems mentioned above, there is really bad interplay between the scrollmargin setting and softwrap. If scrollmargin is set to anything above 0, and lines are (soft)wrapped enough that only a couple lines fit in the view, the scrollmargin will simply push the line currently being edited out of view. Moreover, if the line is wrapped so long it takes up more than the current screen height, even with scrollmargin at 0, it is impossible to see part of the line. You can move the cursor past the edge of the screen and edit stuff technically, but you cannot see what you are editing. 

I can't believe this bug, and the number of bugs associated with, have gone unaddressed for so long. Tempts me to try to learn Go so I can address them myself. I'm working on my own plugin to make up and down arrows just navigate screenw-wise rather than document-wise in lua, but these things really need to be fixed at the Go-level. Otherwise, micro is just not up to many text editing tasks, period.

## Cross-references

- #1981: Fix softwrap scrolling issues (closes)
- #1657: Soft wrap scrolling issue (cross_referenced)
- #1981: Fix softwrap scrolling issues (cross_referenced)

## Reactions

- THUMBS_UP×4

```
slot: 1
number: 632
verdict: no-signal
topic: softwrap bugs
confidence: high
why: the comments describe bugs that have been fixed, there is no reusable knowledge in the thread. It's unclear why the bug was closed, did pr#1981 got merged, and issue#631 closed as fixed? Was something else merged?
```

---

## slot 2 — #1410

# #1410 Add textfilter command

- state: MERGED
- kind: pull_request
- author: serge-v (newcomer)
- created: 2019-11-06T04:33:06+00:00
- updated: 2019-12-20T00:27:55+00:00

Please consider merging textfilter command.
It is similar to vim filter command: http://vimdoc.sourceforge.net/htmldoc/change.html#filter.
Example usage:
In micro make a selection, press Ctrl+E, type `textfilter sort`.
Selection will be sorted.


## Timeline

### 2019-11-06T10:06:19+00:00 — kseistrup (newcomer)

Looks like a highly useful approach that will expand what you can do in `micro` tremendously.


### 2019-12-20T00:27:55+00:00 — dullbananas (newcomer)

great

## Reactions

- THUMBS_UP×1

## Diff

- cmd/micro/command.go +2 -0
- cmd/micro/textfilter.go +35 -0

```diff
diff --git a/cmd/micro/command.go b/cmd/micro/command.go
index 976880d7a1..f3a1b26ad1 100644
--- a/cmd/micro/command.go
+++ b/cmd/micro/command.go
@@ -58,6 +58,7 @@ func init() {
 		"MemUsage":   MemUsage,
 		"Retab":      Retab,
 		"Raw":        Raw,
+		"TextFilter": TextFilter,
 	}
 }
 
@@ -117,6 +118,7 @@ func DefaultCommands() map[string]StrCommand {
 		"memusage":   {"MemUsage", []Completion{NoCompletion}},
 		"retab":      {"Retab", []Completion{NoCompletion}},
 		"raw":        {"Raw", []Completion{NoCompletion}},
+		"textfilter": {"TextFilter", []Completion{NoCompletion}},
 	}
 }
 
diff --git a/cmd/micro/textfilter.go b/cmd/micro/textfilter.go
new file mode 100644
index 0000000000..ec4c91e8ec
--- /dev/null
+++ b/cmd/micro/textfilter.go
@@ -0,0 +1,35 @@
+package main
+
+import (
+	"bytes"
+	"os/exec"
+	"strings"
+)
+
+// TextFilter command filters the selection through the command.
+// Selection goes to the command input.
+// On successfull run command output replaces the current selection.
+func TextFilter(args []string) {
+	if len(args) == 0 {
+		messenger.Error("usage: textfilter arguments")
+		return
+	}
+	v := CurView()
+	sel := v.Cursor.GetSelection()
+	if sel == "" {
+		v.Cursor.SelectWord()
+		sel = v.Cursor.GetSelection()
+	}
+	var bout, berr bytes.Buffer
+	cmd := exec.Command(args[0], args[1:]...)
+	cmd.Stdin = strings.NewReader(sel)
+	cmd.Stderr = &berr
+	cmd.Stdout = &bout
+	err := cmd.Run()
+	if err != nil {
+		messenger.Error(err.Error() + " " + berr.String())
+		return
+	}
+	v.Cursor.DeleteSelection()
+	v.Buf.Insert(v.Cursor.Loc, bout.String())
+}

```

```
slot: 2
number: 1410
verdict: signal
topic: textfilter
confidence: medium
why: the timeline shows no informative comment or normative information, but it's a small feature yet useful feature that was accepted on first read.
```

---

## slot 3 — #731

# #731 Feature Request: Display number of lines

- state: CLOSED
- kind: issue
- author: ghost (established contributor; 5 accepted PRs at time of comment)
- created: 2017-07-11T05:06:35+00:00
- updated: 2017-08-01T16:36:54+00:00

Preferably in JumpLine prompt, i.e.

```
Jump to line (1 - 1337) # 
```

## Timeline

### 2017-07-11T09:29:01+00:00 — X-Ryl669 (newcomer)

Or also, in the bottom summary line (don't know the name, sorry):
`/path/to/your/file.cpp (1 of 1023, 4) c++`

### 2017-08-01T14:44:42+00:00 — yannicka (newcomer)

I did a pull request: #762.

## Cross-references

- #762: Display number of lines in the JumpLine prompt (cross_referenced)
- #762: Display number of lines in the JumpLine prompt (cross_referenced)

## Reactions

- THUMBS_UP×2

```
slot: 3
number: 731
verdict: no-signal
topic: line count
confidence: medium
why: The timeline does not show the PR and associated conversation, and does not show who closed the issue and why.
```

---

## slot 4 — #2101

# #2101 Find-previous (C-p) only catches the first match per line

- state: CLOSED
- kind: issue
- author: slowpeek (newcomer)
- created: 2021-05-13T13:13:54+00:00
- updated: 2021-08-23T21:23:13+00:00

## Description of the problem or steps to reproduce
Type in such text:
```
a a a
a a a
a a a
```
Type `C-f`, enter "a".
Press and keep `C-n` to see how it walks through the matches.
Now press and keep `C-p` to see the bug.

## Specifications

Version: 2.0.9-dev.70
Commit hash: 346c10f
Compiled on May 12, 2021

The bug is present in 2.0.8 btw.

**Upd**: fixed with 2.0.10.


## Timeline

### 2021-08-22T08:18:04+00:00 — slowpeek (newcomer)

Just tried it in new releases:
- 2.0.9 :: same behaviour
- 2.0.10 :: it is partially fixed: the cursor internally moves as it should with `C-p` (if I type `a`, it appears where it should) but the highlighted region is only updated once per two `C-p`.

Edit: typo

### 2021-08-23T00:53:01+00:00 — zyedidia (owner)

I can't reproduce this issue on v2.0.10. Could you provide a short example that I could try which would demonstrate the problem?

### 2021-08-23T19:49:00+00:00 — slowpeek (newcomer)

About reproducing the mentioned behaviour in 2.0.10.

It looks like it only happens under docker. I tried it in docker under ubuntu 20.04 and in docker under ubuntu 21.04 under virtualbox. It is the same in konsole and gnome terminal.

Steps to reproduce:

- start a container `sudo docker run -it --rm --init ubuntu:focal`
- while in the container, install and start micro
  ```bash
  apt update && apt install wget -y
  wget https://github.com/zyedidia/micro/releases/download/v2.0.10/micro-2.0.10-amd64.deb
  dpkg -i micro-2.0.10-amd64.deb
  micro
  ```
- while in the editor

  - type in:

  ```
  a a a a a
  a a a a a
  a a a a a
  ```
  - type `C-f`, enter `a`
  - type `C-n` a few times to see the highlighted region moves each time
  - type `C-p`. Notice the highlighted region doesnt move
  - type `C-p`. Notice the highlighted region moves 2 'steps'
  - type `C-p`. Notice the highlighted region doesnt move
  - type in `z`. Notice it appeared where it should be even though the highlighted region is away
  - type `C-p` more times

Screencast

https://user-images.githubusercontent.com/83845566/130508452-d5f64a1b-ea67-42c2-9e94-28fc3ad1e5ff.mp4



### 2021-08-23T20:33:20+00:00 — zyedidia (owner)

Thanks for the details, I was able to debug and have found the cause of your problem (it is docker, not micro). It appears docker uses `<Ctrl-p><Ctrl-q>` to detach from a container, so docker will wait after you press Ctrl-p until you press another key before sending the event to the terminal/micro (if the second keypress is Ctrl-q, it will detach). So when you press the second Ctrl-p (or `<Ctrl-p><z>`, or anything else), docker sends both keypresses.

Here's a stackoverflow post detailing how to change this behavior if you'd like: https://stackoverflow.com/questions/20828657/docker-change-ctrlp-to-something-else.

You can also observe this within docker at the shell (outside micro). Usually Ctrl-p is like up-arrow, but within docker it requires two presses, and then it goes up the history twice.

### 2021-08-23T21:22:49+00:00 — slowpeek (newcomer)

Thanks for looking into it! The one who decided on the detach sequence in docker is clearly a emacs hater.

I'm closing the issue because the original problem (not docker related, you can still reproduce it in 2.0.9) is fixed with 2.0.10.

## Reactions

- THUMBS_UP×2

```
slot: 4
number: 2101
verdict: signal
topic: ctrl-p binding
confidence: high
why: describes behaviour that looks like a micro bug but is actually caused by caused by another component, the verdict comes from maintainer.
```

---

## slot 5 — #3160

# #3160 nzw 

- state: OPEN
- kind: issue
- author: TLX542 (newcomer)
- created: 2024-03-01T16:19:33+00:00
- updated: 2024-03-03T17:50:54+00:00

## Description of the problem or steps to reproduce
if you split the terminal and Unsplit with the original terminal being split first, then unsplit again, the next action will make micro crash

Micro encountered an error: runtime.errorString runtime error: invalid memory address or nil pointer dereference
/usr/lib/golang/src/runtime/panic.go:260 (0x5605f04b7a9d)
	panicmem: panic(memoryError)
/usr/lib/golang/src/runtime/panic.go:259 (0x5605f04b7a6d)
	panicmem: panicCheck2("invalid memory address or nil pointer dereference")
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/internal/views/splits.go:460 (0x5605f090a8b9)
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/internal/action/actions.go:1619 (0x5605f09283dd)
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/internal/action/bufpane.go:466 (0x5605f092e4d7)
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/internal/action/bufpane.go:149 (0x5605f092d1b6)
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/internal/action/bufpane.go:31 (0x5605f092bd1d)
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/internal/action/bufpane.go:449 (0x5605f092e219)
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/internal/action/bufpane.go:365 (0x5605f092dda5)
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/internal/action/tab.go:254 (0x5605f093d70e)
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/internal/action/tab.go:136 (0x5605f093d07c)
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/cmd/micro/micro.go:445 (0x5605f096ac30)
/builddir/build/BUILD/micro-2.0.11/_build/src/github.com/zyedidia/micro/cmd/micro/micro.go:382 (0x5605f096a68a)
/usr/lib/golang/src/runtime/internal/atomic/types.go:194 (0x5605f04a3f72)
	(*Uint32).Load: return Load(&u.value)
/usr/lib/golang/src/runtime/asm_amd64.s:1598 (0x5605f04d4481)
	goexit: BYTE	$0x90	// NOP

## Specifications

Commit hash: 59dda01cb7ad92a069068b3aa93abc7ff04cc935
OS: Fedora 38
Terminal: zsh


## Timeline

### 2024-03-03T17:37:23+00:00 — dmaluka (established contributor; 38 accepted PRs at time of comment)

I can't reproduce this crash, but I'm not sure what do you mean by "Unsplit with the original terminal being split first". Could you describe your precise steps to reproduce it?

Also:

> Commit hash: [59dda01](https://github.com/zyedidia/micro/commit/59dda01cb7ad92a069068b3aa93abc7ff04cc935)

[59dda01](https://github.com/zyedidia/micro/commit/59dda01cb7ad92a069068b3aa93abc7ff04cc935) is the current newest top-of-tree, but from your log it looks like the crash happened on v2.0.11. Right?

### 2024-03-03T17:50:53+00:00 — dmaluka (established contributor; 38 accepted PRs at time of comment)

So, I haven't been able reproduce this crash (with either newest micro or v2.0.11). But I can see other problems with the `Unsplit` action:

- It closes the split without asking the user to save the changes.
- It closes the current (active) split, which is completely different from what is described in its documentation:
```
// Unsplit closes all splits in the current tab except the active one
func (h *BufPane) Unsplit() bool {
```

So with its current (not documented) behavior, this `Unsplit` action looks completely useless: the `Quit` action also closes the current split pane, and does it more correctly.

```
slot: 5
number: 3160
verdict: signal
topic: unsplit
confidence: high
why: established contributor identifies documentation/implementation mismatch, and apparent redundancy in the command set.
```

---

## slot 6 — #1115

# #1115 Regex capture groups not working in replace command

- state: CLOSED
- kind: issue
- author: dwu (newcomer)
- created: 2018-05-24T19:35:37+00:00
- updated: 2020-02-13T21:09:23+00:00

## Description of the problem or steps to reproduce
Looking through the docs I couldn't find any information whether the `replace` command regex supports capture groups as defined e.g. in [Regexp.ReplaceAllString](https://golang.org/pkg/regexp/#Regexp.ReplaceAllString) and [Regexp.Expand](https://golang.org/pkg/regexp/#Regexp.Expand). So depending on this, this might be more of a feature request than a bug report. 

When executing the command ```replace "(foo)" "$1$1"```
on a buffer with content ```foobar```
I would have expected the replace operation to result in ```foofoobar```.

However, the result in version ae9bb76 is ```bar```.

## Specifications
Commit hash:  ae9bb76
OS: Linux64
Terminal: xfce4-terminal / xterm


## Timeline

### 2018-06-27T05:28:08+00:00 — phil294 (newcomer)

`\1` also does not work. If this functionality is not *intended* to be working right now, it should be stated in the documentation. Applying regex options (dotall, case-insensitive etc.) would also be helpful. I'm not sure what is implemented right now.

### 2018-08-19T09:09:41+00:00 — supbish (established contributor; 3 accepted PRs at time of comment)

Two issues here:

One, all commands undergo a shell-like processing step, where strings that look like `$foo` or `${foo}` are replaced with the corresponding environment variable. This happens before the command actually fires, blocking the functionality you want.

Two, the replacement routine currently doesn't attempt to do any capture expansion.

Proposed fix: make a slight change to shellwords.go, so that single-quoted strings don't do environment variable replacement. This is more in line with how shells work anyway. Then strings like `$foo` will make it through to the command, and the replacement command can be altered to do capture expansion.

@zyedidia, what do you think of this proposed fix? If it sounds good to you, I can put a PR together soon (if nobody else gets to it first).

reactions: THUMBS_UP×1

### 2018-08-19T20:52:09+00:00 — supbish (established contributor; 3 accepted PRs at time of comment)

Interestingly, with or without the proposed fix, there's no way to replace text with anything that looks like an environment variable. So that's another issue, especially considering languages that use $ as a sigil (perl) or to identify variables (php), or where it's just fashionable to stick dollar signs on the front of variables (js)...

What should probably happen, since shellwords.go is trying to do what a shell does, is "\\$foo" should literally mean "$foo" and not represent something to be replaced. Unfortunately shellwords.go just doesn't work this way; slash-escapes happen pretty much immediately and the replacement happens afterwards. Fixing this would require fairly major changes to it (and still doesn't address capture expansion, which obviously needs to happen even farther down the line).

---

Edit: ok, so with proposed fix, it looks like we can use golang's regex expand thing to escape $ by doubling it up... so: 
- `'$$foo'` would give the string "$foo"
- `'$foo'` would give the *capture group* named "foo"
- `"$foo"` or `$foo` would give the *environment variable* named "foo"

reactions: THUMBS_UP×1

### 2018-08-24T05:37:11+00:00 — supbish (established contributor; 4 accepted PRs at time of comment)

Added this to the search-goodies branch of my [fork](https://github.com/supbish/micro).
Please try it out and let me know if you find any issues.
👍

## Cross-references

- #1159: Search and replace improvements (closes)
- #1159: Search and replace improvements (cross_referenced)

## Reactions

- THUMBS_UP×1

```
slot: 6
number: 1115
verdict: signal
topic: replace capture groups
confidence: high
why: Design conversation. Was merged in a fork. Unclear whether issue was closed as fixed or wontfix.
```

---

## slot 7 — #1881

# #1881 Is integration with select-editor planned any time soon?

- state: CLOSED
- kind: issue
- author: Kayli (newcomer)
- created: 2020-10-03T00:51:51+00:00
- updated: 2021-11-17T23:51:41+00:00

I would like to use select-editor command to choose micro as a default editor. 


## Timeline

### 2020-10-03T05:47:05+00:00 — zyedidia (owner)

I haven't looked into select-editor much but I presume it can be configured to support any editor. Possibly a simpler method of making micro the default editor would be to put `export VISUAL=micro` in your `~/.bashrc` file.

### 2020-12-11T10:52:21+00:00 — hhromic (newcomer)

This is implemented in #1935 

### 2021-01-18T07:13:48+00:00 — pabloab (newcomer)

[I added](https://askubuntu.com/a/1207615/349837)
```
sudo update-alternatives --install /usr/bin/editor editor /home/$USER/.linuxbrew/bin//micro 50
```
[and selected](https://askubuntu.com/a/615181/349837) (unsure why `select-editor` wasn't working)
```
sudo update-alternatives --config editor
```


## Cross-references

- #1935: Add support for alternatives system in Debian package (closes)
- #1935: Add support for alternatives system in Debian package (cross_referenced)
- #1935: Add support for alternatives system in Debian package (cross_referenced)

## Reactions

- THUMBS_UP×1

```
slot: 7
number: 1881
verdict: no-signal
topic: debian select-editor
confidence: low
why: Issue seems about packaging on debian/ubuntu, it's unclear what was fixed. Without reading pr#1935 it's hard to understand.
```

---

## slot 8 — #1412

# #1412 Add windows .bat syntax highlighting file #1388

- state: MERGED
- kind: pull_request
- author: tommyshem (established contributor; 17 accepted PRs at time of comment)
- created: 2019-11-14T01:13:04+00:00
- updated: 2019-12-30T19:20:14+00:00



## Diff

- runtime/syntax/bat.yaml +58 -0

```diff
diff --git a/runtime/syntax/bat.yaml b/runtime/syntax/bat.yaml
new file mode 100644
index 0000000000..e6077a57ea
--- /dev/null
+++ b/runtime/syntax/bat.yaml
@@ -0,0 +1,58 @@
+filetype: batch
+
+detect:
+  filename: "(\\.bat$)"
+  # header: ""
+
+rules:
+  # Numbers
+  - constant.number: "\\b[0-9]+\\b"
+  # Brackets and symbols
+  - special: "(\\{|\\}|\\(|\\)|\\;|\\]|\\[|`|\\\\|\\$|<|>|!|=|&|\\|)"
+  # Conditionals and control flow
+  # note (?i) means case insensitive match
+  - type: "\\b(?i)(case|do|done|elif|else|esac|exit|fi|for|function|if|in|local|read|return|select|then|until|while)\\b"
+  - type: "\\b(?i)(equ|neq|lss|leq|gtr|geq|on|off)\\b"
+  - type: "\\b(?i)(goto|for|in|do|call|exit|not|exist|errorlevel|defined)\\b"
+  - type: "\\b(?i)(prn|nul|lpt3|lpt2|lpt1|con|com4|com3|com2|com1|aux)\\b"
+  # keywords
+  - statement: "\\b(?i)(adprep|append|arp|assoc|at|atmadm|attrib|auditpol|autochk|autoconv|autofmt|bcdboot|bcdedit|bdehdcfg|bitsadmin|bootcfg|break|brea)\\b"
+  - statement: "\\b(?i)(cacls|cd|certreq|certutil|chcp|change|choice|cipher|chdir|chkdsk|chkntfs|chglogon|chgport|chgusr|clip|cls|clscluadmin|cluster|cmd|cmdkey|cmstp|color)\\b"
+  - statement: "\\b(?i)(comp|compact|convert|copy|cprofile|cscript|csvde|date|dcdiag|dcgpofix|dcpromo|defra|del|dfscmd|dfsdiag|dfsrmig|diantz|dir|dirquota|diskcomp|diskcopy|diskpart|diskperf|diskraid|diskshadow|dispdiag|doin|dnscmd|doskey|driverquery|dsacls|dsadd|dsamain|dsdbutil|dsget|dsmgmt|dsmod|dsmove|dsquery|dsrm)\\b"
+  - statement: "\\b(?i)(echo|edit|endlocal|erase|esentutl|eventcreate|eventquery|eventtriggers|evntcmd|expand|extract)\\b"
+  - statement: "\\b(?i)(fc|filescrn|find|findstr|finger|flattemp|fonde|forfiles|format|freedisk|fs|fsutil|ftp|ftype|fveupdate|getmac|gettype|gpfixup|gpresult|gpupdate|graftabl)\\b"
+  - statement: "\\b(?i)(hashgen|hep|help|helpctr|hostname|icacls|iisreset|inuse|ipconfig|ipxroute|irftp|ismserv|jetpack|keyb|klist|ksetup|ktmutil|ktpass|label|ldifd|ldp|lodctr|logman|logoff|lpq|lpr|macfile)\\b"
+  - statement: "\\b(?i)(makecab|manage-bde|mapadmin|md|mkdir|mklink|mmc|mode|more|mount|mountvol|move|mqbup|mqsvc|mqtgsvc|msdt|msg|msiexec|msinfo32|mstsc|nbtstat|net computer|net group)\\b"
+  - statement: "\\b(?i)(net localgroup|net print|net session|net share|net start|net stop|net use|net user|net view|net|netcfg|netdiag|netdom|netsh|netstat|nfsadmin|nfsshare|nfsstat|nlb)\\b"
+  - statement: "\\b(?i)(nlbmgr|nltest|nslookup|ntackup|ntcmdprompt|ntdsutil|ntfrsutl|openfiles|pagefileconfig|path|pathping|pause|pbadmin|pentnt|perfmon|ping|pnpunatten|pnputil|popd)\\b"
+  - statement: "\\b(?i)(powercfg|powershell|powershell_ise|print|prncnfg|prndrvr|prnjobs|prnmngr|prnport|prnqctl|prompt|pubprn|pushd|pushprinterconnections|pwlauncher|qappsrv|qprocess)\\b"
+  - statement: "\\b(?i)(query|quser|qwinsta|rasdial|rcp|rd|rdpsign|regentc|recover|redircmp|redirusr|reg|regini|regsvr32|relog|ren|rename|rendom|repadmin|repair-bde|replace|reset|restore)\\b"
+  - statement: "\\b(?i)(rxec|risetup|rmdir|robocopy|route|rpcinfo|rpcping|rsh|runas|rundll32|rwinsta|scp|sc|setlocal|session|schtasks|scwcmd|secedit|serverceipoptin|servrmanagercmd|serverweroptin|set|setspn)\\b"
+  - statement: "\\b(?i)(setx|sfc|shadow|shift|showmount|shutdown|sort|ssh|start|storrept|subst|sxstrace|ysocmgr|systeminfo|takeown|tapicfg|taskkill|tasklist|tcmsetup|telnet|tftp|time)\\b"
+  - statement: "\\b(?i)(timeout|title|tlntadmn|tpmvscmgr|tpmvscmgr|tacerpt|tracert|tree|tscon|tsdiscon|tsecimp|tskill|tsprof|type|typeperf|tzutil|uddiconfig|umount|unlodctr|ver|verify)\\b"
+  - statement: "\\b(?i)(verifier|verif|vol|vssadmin|w32tm|waitfor|wbadmin|wdsutil|wecutil|wevtutil|where|whoami|winnt|winnt32|winpop|winrm|winrs|winsat|wlbs|mic|wscript|xcopy)\\b"
+  # / Flags
+  - constant: "(/\\w+)"
+  # Variables
+  - special: "(%%\\w+)"
+  - special: "(%\\w+%)"
+  # Conditional flags
+  - type: "--[a-z-]+"
+  - type: "\\ -[a-z]+"
+
+  - identifier: "\\$\\{?[0-9A-Z_!@#$*?-]+\\}?"
+  - identifier: "\\$\\{?[0-9A-Z_!@#$*?-]+\\}?"
+  # "" String
+  - constant.string:
+      start: \"
+      end: \"
+      skip: \.
+      rules:
+        - constant.specialChar: (\\0|\\\\|\\t|\\n|\\r|\\"|\\')
+        - constant.unicode: \\u\{[[:xdigit:]]+}
+  # '' string
+  - constant.string: "(\\'.+\\')"
+  # rem as comment
+  - comment.rem: "(?i)(rem\\s.*)"
+  # :: as comment
+  - comment.rem: "(?i)(\\:\\:\\s.*)"

```

```
slot: 8
number: 1412
verdict: no-signal
topic: .bat syntax
confidence: medium
why: Merged with no comment, but it's literally just one syntax file. Nothing not apparent in the code.
```

---

## slot 9 — #51

# #51 Create a Chat Room

- state: CLOSED
- kind: issue
- author: abhisekp (newcomer)
- created: 2016-04-21T15:47:56+00:00
- updated: 2016-04-21T16:45:33+00:00

Can you please create a chat room in [![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg?maxAge=2592000)](https://gitter.im) where users can chat?


## Timeline

### 2016-04-21T15:53:12+00:00 — mbndr (newcomer)

like it


### 2016-04-21T16:27:45+00:00 — bentranter (newcomer)

You could also make a channel in the [Gophers](https://blog.gopheracademy.com/gophers-slack-community/) Slack if anyone is opposed to using Gitter


### 2016-04-21T16:45:28+00:00 — zyedidia (owner)

I think it should be working [here](https://gitter.im/zyedidia/micro) now. Let me know if there's an issue.

```
slot: 9
number: 51
verdict: signal
topic: gitter channel
confidence: high
why: User asks for gitter channer. Owner gives gitter channel. Still current.
```

---

## slot 10 — #3069

# #3069 Fix ruler overwriting neighboring split pane + fix crash #3052

- state: MERGED
- kind: pull_request
- author: dmaluka (established contributor; 37 accepted PRs at time of comment)
- created: 2023-12-03T00:31:22+00:00
- updated: 2024-03-13T20:11:04+00:00

When we resize a split pane to a very small width, so that the ruler does not fit in the pane, it overwrites the sibling split pane.

To fix it, clean up the calculation of gutter width, buffer width and scrollbar width, so that they add up exactly to the window width, and ensure that we don't draw the gutter beyond this calculated gutter
width (gutterOffset).

As a bonus, this also fixes the crash #3052 (observed when resizing a split pane to a very small width, if wordwrap is enabled), by ensuring that bufWidth is never negative.

Fixes #3052 

## Cross-references

- #3052: Crash when pane/(v)split widthe is smaller than ruler size (closes)
- #3036: termwindow: Show cursor only when his X and Y axis is smaller than the window size (cross_referenced)
- #3052: Crash when pane/(v)split widthe is smaller than ruler size (cross_referenced)
- #3056: bufwindow: Fix slice creation with wordwrap active in case of zero size split (cross_referenced)

## Diff

- internal/display/bufwindow.go +28 -17

```diff
diff --git a/internal/display/bufwindow.go b/internal/display/bufwindow.go
index fde209695a..a440dcd07b 100644
--- a/internal/display/bufwindow.go
+++ b/internal/display/bufwindow.go
@@ -129,6 +129,11 @@ func (w *BufWindow) updateDisplayInfo() {
 		w.bufHeight--
 	}
 
+	scrollbarWidth := 0
+	if w.Buf.Settings["scrollbar"].(bool) && w.Buf.LinesNum() > w.Height && w.Width > 0 {
+		scrollbarWidth = 1
+	}
+
 	w.hasMessage = len(b.Messages) > 0
 
 	// We need to know the string length of the largest line number
@@ -146,13 +151,13 @@ func (w *BufWindow) updateDisplayInfo() {
 		w.gutterOffset += w.maxLineNumLength + 1
 	}
 
-	prevBufWidth := w.bufWidth
-
-	w.bufWidth = w.Width - w.gutterOffset
-	if w.Buf.Settings["scrollbar"].(bool) && w.Buf.LinesNum() > w.Height {
-		w.bufWidth--
+	if w.gutterOffset > w.Width-scrollbarWidth {
+		w.gutterOffset = w.Width - scrollbarWidth
 	}
 
+	prevBufWidth := w.bufWidth
+	w.bufWidth = w.Width - w.gutterOffset - scrollbarWidth
+
 	if w.bufWidth != prevBufWidth && w.Buf.Settings["softwrap"].(bool) {
 		for _, c := range w.Buf.GetCursors() {
 			c.LastVisualX = c.GetVisualX()
@@ -277,13 +282,17 @@ func (w *BufWindow) drawGutter(vloc *buffer.Loc, bloc *buffer.Loc) {
 			break
 		}
 	}
-	screen.SetContent(w.X+vloc.X, w.Y+vloc.Y, char, nil, s)
-	vloc.X++
-	screen.SetContent(w.X+vloc.X, w.Y+vloc.Y, char, nil, s)
-	vloc.X++
+	for i := 0; i < 2 && vloc.X < w.gutterOffset; i++ {
+		screen.SetContent(w.X+vloc.X, w.Y+vloc.Y, char, nil, s)
+		vloc.X++
+	}
 }
 
 func (w *BufWindow) drawDiffGutter(backgroundStyle tcell.Style, softwrapped bool, vloc *buffer.Loc, bloc *buffer.Loc) {
+	if vloc.X >= w.gutterOffset {
+		return
+	}
+
 	symbol := ' '
 	styleName := ""
 
@@ -319,26 +328,28 @@ func (w *BufWindow) drawLineNum(lineNumStyle tcell.Style, softwrapped bool, vloc
 	} else {
 		lineInt = bloc.Y - cursorLine
 	}
-	lineNum := strconv.Itoa(util.Abs(lineInt))
+	lineNum := []rune(strconv.Itoa(util.Abs(lineInt)))
 
 	// Write the spaces before the line number if necessary
-	for i := 0; i < w.maxLineNumLength-len(lineNum); i++ {
+	for i := 0; i < w.maxLineNumLength-len(lineNum) && vloc.X < w.gutterOffset; i++ {
 		screen.SetContent(w.X+vloc.X, w.Y+vloc.Y, ' ', nil, lineNumStyle)
 		vloc.X++
 	}
 	// Write the actual line number
-	for _, ch := range lineNum {
-		if softwrapped {
+	for i := 0; i < len(lineNum) && vloc.X < w.gutterOffset; i++ {
+		if softwrapped || (w.bufWidth == 0 && w.Buf.Settings["softwrap"] == true) {
 			screen.SetContent(w.X+vloc.X, w.Y+vloc.Y, ' ', nil, lineNumStyle)
 		} else {
-			screen.SetContent(w.X+vloc.X, w.Y+vloc.Y, ch, nil, lineNumStyle)
+			screen.SetContent(w.X+vloc.X, w.Y+vloc.Y, lineNum[i], nil, lineNumStyle)
 		}
 		vloc.X++
 	}
 
 	// Write the extra space
-	screen.SetContent(w.X+vloc.X, w.Y+vloc.Y, ' ', nil, lineNumStyle)
-	vloc.X++
+	if vloc.X < w.gutterOffset {
+		screen.SetContent(w.X+vloc.X, w.Y+vloc.Y, ' ', nil, lineNumStyle)
+		vloc.X++
+	}
 }
 
 // getStyle returns the highlight style for the given character position
@@ -609,7 +620,7 @@ func (w *BufWindow) displayBuffer() {
 		wordwidth := 0
 
 		totalwidth := w.StartCol - nColsBeforeStart
-		for len(line) > 0 {
+		for len(line) > 0 && vloc.X < maxWidth {
 			r, combc, size := util.DecodeCharacter(line)
 			line = line[size:]
 

```

```
slot: 10
number: 3069
verdict: no-signal
topic: split pane bugs
confidence: medium
why: contributor posts bugfix, bugfix is merged, no normative conversation beyond code.
```

---

## slot 11 — #980

# #980 lua.go: Typo in `func importFilePath()`

- state: CLOSED
- kind: issue
- author: GoLangsam (newcomer)
- created: 2018-01-05T03:16:11+00:00
- updated: 2018-01-05T03:29:28+00:00

## Description of the problem or steps to reproduce

in `func importFilePath()` the definion `L.SetField(pkg, "Clean", luar.New(L, filepath.Join))` on line # 419 seems to be a mistaken duplicate.
The intended one is three lines below.

Plse consider to remove.

btw: Mircro is *Great* - I like it a lot :1st_place_medal:

```
slot: 11
number: 980
verdict: no-signal
topic: none
confidence: medium
why: janitorial bug reported, and closed, no information on whether it was rejected (then that would be signal) or merged (then it's a just a typo fix, no signal). Missing: who closed the issue.
```

---

## slot 12 — #576

# #576 FindNext and FindPrevious don't work when finding special regex characters

- state: CLOSED
- kind: issue
- author: GeigerCounter (newcomer)
- created: 2017-03-03T09:55:01+00:00
- updated: 2017-03-05T16:21:07+00:00

## Description of the problem or steps to reproduce
Use find, type in `\(` to find opening parenthesis. ( Or any other regex special character for that matter. ) Find will find the first one correctly. Then when using Ctrl+P and Ctrl+N to find previous/next instance of the find, it fails. The gutter reads `Finding: (` and it is unable to find it because an unescaped `(` is not valid regex.

Also I tried `'('` and `"("` and `"\("` and `'\('`, the search attempt included the opening quote - but not the end quote - and still on find next and previous would find `'(` and `"(` respectively.

Proposed fixes:

- Add and implement a "simple find" that does not use regex syntax and automatically escapes any regex syntax and special characters in the find query.
- Move current regex based find to `findregex` accessed by pressing Ctrl+F twice or by running `findregex` in micro's prompt.
- Have the backslash forcibly kept in the find query for use by find previous and find next.

Commit hash: 9b51069
OS: Ubuntu 14.04.3 LTS 
Terminal: puTTY + screen

```
slot: 12
number: 576
verdict: no-signal
topic: find regex metacharacters
confidence: low
why: unclear whether if any answer was provided
```

---

## slot 13 — #3993

# #3993 Feature Request: Native Nerd Fonts support for Statusline and Filemanager

- state: OPEN
- kind: issue
- author: brunohcorreia (newcomer)
- created: 2026-02-03T18:44:28+00:00
- updated: 2026-02-04T15:52:38+00:00

Currently, Micro feels visually "plain" compared to other modern terminal editors (like Helix or Neovim configurations) when it comes to file identification. I would like to request native support for Nerd Fonts icons within Micro core and its default plugins. This would greatly improve visual navigation and UI aesthetics.

**Implementation suggestions:**

1. **Statusline**: Display the file type icon next to the filename or filetype indicator.
2. **Filemanager**: Display folder icons (open/closed) and file type icons next to items in the tree view.
3. **Configuration**: Introduce a global option (e.g., `nerdfonts`) to control this.

Crucially, this option should be `false` (disabled)by default. This ensures that Micro remains lightweight and compatible with standard terminals/fonts out of the box. Only users with patched fonts who explicitly want this feature would enable it (e.g., `set nerdfonts true`).

## Timeline

### 2026-02-03T20:36:51+00:00 — Andriamanitra (established contributor; 15 accepted PRs at time of comment)

I think the best way to experiment with this would be to implement it as a plugin. The status line is entirely customizable and the whole file manager is a 3rd party plugin, so there's nothing you need from micro's side to implement the suggestions. Check out [the built-in status plugin](https://github.com/micro-editor/micro/tree/master/runtime/plugins/status) if you need help getting started.

If the feature gains popularity as a plugin it would be a good sign that this feature is something users want.

### 2026-02-03T22:40:21+00:00 — Neko-Box-Coder (established contributor; 20 accepted PRs at time of comment)

Whether it should be built-in or not is another question, but there are existing plugins that already do this, for anyone interseted:

https://github.com/Neko-Box-Coder/filemanager2
https://github.com/Neko-Box-Coder/git-status

reactions: THUMBS_UP×1

### 2026-02-04T15:52:38+00:00 — JoeKar (maintainer since ~2024; 176 merges at time of comment)

> https://github.com/Neko-Box-Coder/filemanager2

Cool to see. I currently plan to extract all the plugins bundled in [micro-editor/updated-plugins](https://github.com/micro-editor/updated-plugins) into their own repositories within the organization[^1][^2].
This makes it easier to release single plugins, when the responsible [channel.json](https://github.com/micro-editor/plugin-channel/blob/master/channel.json) is updated once to point to the new `repo.json` location.

Then we can "upstream" your improvements from [filemanager2](https://github.com/Neko-Box-Coder/filemanager2).

But we definitely need someone who is responsible for the plugin management. It is currently just too much to take care of.

Besides of that, do we need this feature request to stay open?

[^1]: https://github.com/micro-editor/updated-plugins/pull/27#pullrequestreview-3647594052
[^2]: https://github.com/micro-editor/updated-plugins/pull/27#issuecomment-3819715357

```
slot: 13
number: 3993
verdict: signal
topic: nerdfont file icons
confidence: high
why: directs a user request to  plugins
```

---

## slot 14 — #867

# #867 Output pane

- state: OPEN
- kind: issue
- author: ghost (established contributor; 5 accepted PRs at time of comment)
- created: 2017-10-06T14:06:14+00:00
- updated: 2018-01-03T22:45:27+00:00

I like how Zachary solved [showing keybindings](https://github.com/zyedidia/micro/issues/829) using Alt+G shortcut. Not because I need these shortcuts, but it reminds me the output window in Sublime Text. What if micro would have such output pane? Where command outputs by example build results instead of switching to terminal?

I have something like "runner" plugin, this is part of it:
```
function mode1()
    local buf = CurView().Buf -- The current buffer
    if buf:FileType() == "go" then
        HandleShellCommand("go run " .. buf.Path, true, true)
    elseif buf:FileType() == "php" then
        HandleShellCommand("php " .. buf.Path, true, true)
    elseif buf:FileType() == "tcl" then
        HandleShellCommand("jimsh " .. buf.Path, true, true)
    elseif buf:FileType() == "lisp" then
        HandleShellCommand("newlisp " .. buf.Path, true, true)
    elseif buf:FileType() == "lua" then
        HandleShellCommand("lua " .. buf.Path, true, true)
    end
end
```
Than I run appropriate program using shortcut:
`"Alt-r": 		"Save,runner.mode1"`

Having scrollable output directly in micro pane would be perfect. It works particularly when I set openTerm param to false but whole output is in single line (in command line)

As a bonus horizontal or vertical orientation of the output pane would be configurable.

## Timeline

### 2018-01-03T22:45:26+00:00 — ghost (established contributor; 6 accepted PRs at time of comment)

[something along those lines is now in the making](https://github.com/zyedidia/micro/issues/974#issuecomment-355128950)

> I like how Zachary solved showing keybindings using Alt+G shortcut. Not because I need these shortcuts, but it reminds me the output window in Sublime Text.

this is actually already working 



## Cross-references

- #829: Feature request: show top keybindings at the bottom (cross_referenced)
- #974: Keybindings mostly not working (cross_referenced)

```
slot: 14
number: 867
verdict: no-signal
topic: none
confidence: medium
why: I cannot tell what's being asked.
```

---

## slot 15 — #1451

# #1451 Use pledge(2) on OpenBSD

- state: OPEN
- kind: pull_request
- author: estrogently (newcomer)
- created: 2020-01-04T16:57:22+00:00
- updated: 2021-01-13T21:09:25+00:00

[`pledge(2)`](https://man.openbsd.org/pledge.2) restricts which system calls can be called, terminating the process on a violation.

Probably not very essential for micro, but nice to have.

## Timeline

### 2020-02-08T00:59:59+00:00 — zyedidia (owner)

What sort of system calls does this disallow and how are you sure that micro doesn't violate the pledges? Sorry I'm just worried that this could cause a crash because micro pledges the wrong set of system calls.

### 2021-01-13T21:09:25+00:00 — deliciouslytyped (newcomer)

I like the idea here.

FWIW, if you're considering adding something like this, you might want to abstract it a bit or something to add multi-platform capability because stuff like seccomp on linux might be interesting.

But then you kind of have to start thinking about "what should be the threat model for a text editor?" and I don't know.

You might also want to make the call list flexible depending on what someone is doing with their plugins, but then at that point a question is how do you secure the configuration?

And if you allow exec, can't someone just run an executable that has less restrictions?

Disclaimer: I am an armchair security engineer.

## Reactions

- HEART×2

## Diff

- cmd/micro/micro.go +5 -0
- go.mod +1 -0
- go.sum +4 -2

```diff
diff --git a/cmd/micro/micro.go b/cmd/micro/micro.go
index 3e2f95fa20..45b0d830e6 100644
--- a/cmd/micro/micro.go
+++ b/cmd/micro/micro.go
@@ -8,6 +8,7 @@ import (
 	"runtime"
 	"sort"
 
+	"github.com/estrogently/puffy"
 	"github.com/go-errors/errors"
 	isatty "github.com/mattn/go-isatty"
 	"github.com/zyedidia/micro/internal/action"
@@ -151,6 +152,10 @@ func main() {
 
 	var err error
 
+	if err = puffy.PledgePromises("stdio rpath wpath cpath tty proc exec"); err != nil {
+		screen.TermMessage(err)
+	}
+
 	InitFlags()
 
 	InitLog()
diff --git a/go.mod b/go.mod
index 1df1d91a42..1dabef8cc3 100644
--- a/go.mod
+++ b/go.mod
@@ -3,6 +3,7 @@ module github.com/zyedidia/micro
 require (
 	github.com/blang/semver v3.5.1+incompatible
 	github.com/dustin/go-humanize v1.0.0
+	github.com/estrogently/puffy v1.0.0
 	github.com/go-errors/errors v1.0.1
 	github.com/kballard/go-shellquote v0.0.0-20180428030007-95032a82bc51
 	github.com/mattn/go-isatty v0.0.11
diff --git a/go.sum b/go.sum
index cd432bdc07..45dff730f2 100644
--- a/go.sum
+++ b/go.sum
@@ -8,6 +8,8 @@ github.com/davecgh/go-spew v1.1.1 h1:vj9j/u1bqnvCEfJOwUhtlOARqs3+rkHYY13jYWTU97c
 github.com/davecgh/go-spew v1.1.1/go.mod h1:J7Y8YcW2NihsgmVo/mv3lAwl/skON4iLHjSsI+c5H38=
 github.com/dustin/go-humanize v1.0.0 h1:VSnTsYCnlFHaM2/igO1h6X3HA71jcobQuxemgkq4zYo=
 github.com/dustin/go-humanize v1.0.0/go.mod h1:HtrtbFcZ19U5GC7JDqmcUSB87Iq5E25KnS6fMYU6eOk=
+github.com/estrogently/puffy v1.0.0 h1:BcBaLdGQdOCo7VR4NjXO8+wyTrzivSls/R+9KLA0JSs=
+github.com/estrogently/puffy v1.0.0/go.mod h1:JOpxfeUu8MMOq86Lb1uRmkWVAwRrKJCbxt11ilT/ans=
 github.com/gdamore/encoding v1.0.0 h1:+7OoQ1Bc6eTm5niUzBa0Ctsh6JbMW6Ra+YNuAtDBdko=
 github.com/gdamore/encoding v1.0.0/go.mod h1:alR0ol34c49FCSBLjhosxzcPHQbf2trDkoo5dl+VrEg=
 github.com/go-errors/errors v1.0.1 h1:LUHzmkK3GUKUrL/1gfBUxAHzcev3apQlezX/+O7ma6w=
@@ -50,8 +52,6 @@ github.com/zyedidia/poller v1.0.1 h1:Tt9S3AxAjXwWGNiC2TUdRJkQDZSzCBNVQ4xXiQ7440s
 github.com/zyedidia/poller v1.0.1/go.mod h1:vZXJOHGDcuK08GXhF6IAY0ZFd2WcgOR5DOTp84Uk5eE=
 github.com/zyedidia/pty v2.0.0+incompatible h1:Ou5vXL6tvjst+RV8sUFISbuKDnUJPhnpygApMFGweqw=
 github.com/zyedidia/pty v2.0.0+incompatible/go.mod h1:4y9l9yJZNxRa7GB/fB+mmDmGkG3CqmzLf4vUxGGotEA=
-github.com/zyedidia/tcell v1.4.0 h1:uhAz+bdB3HHlVP2hff3WURkI+pERNwgVfy27oi1Gb2A=
-github.com/zyedidia/tcell v1.4.0/go.mod h1:HhlbMSCcGX15rFDB+Q1Lk3pKEOocsCUAQC3zhZ9sadA=
 github.com/zyedidia/tcell v1.4.1 h1:zLci8cg1SLINjwSePZ1yUWnYOnZXMyr4h+zaOvhu5K8=
 github.com/zyedidia/tcell v1.4.1/go.mod h1:HhlbMSCcGX15rFDB+Q1Lk3pKEOocsCUAQC3zhZ9sadA=
 github.com/zyedidia/tcell v1.4.2 h1:JWMDs6O1saINPIR5M3kNqlWJwkfnBZeZDZszEJi3BW8=
@@ -62,6 +62,8 @@ golang.org/x/sys v0.0.0-20190204203706-41f3e6584952/go.mod h1:STP8DvDyc/dI5b8T5h
 golang.org/x/sys v0.0.0-20190626150813-e07cf5db2756/go.mod h1:h1NjWce9XRLGQEsW7wpKNCjG9DtNlClVuFLEZdDNbEs=
 golang.org/x/sys v0.0.0-20191026070338-33540a1f6037 h1:YyJpGZS1sBuBCzLAR1VEpK193GlqGZbnPFnPV/5Rsb4=
 golang.org/x/sys v0.0.0-20191026070338-33540a1f6037/go.mod h1:h1NjWce9XRLGQEsW7wpKNCjG9DtNlClVuFLEZdDNbEs=
+golang.org/x/sys v0.0.0-20200117145432-59e60aa80a0c h1:gUYreENmqtjZb2brVfUas1sC6UivSY8XwKwPo8tloLs=
+golang.org/x/sys v0.0.0-20200117145432-59e60aa80a0c/go.mod h1:h1NjWce9XRLGQEsW7wpKNCjG9DtNlClVuFLEZdDNbEs=
 golang.org/x/text v0.3.0/go.mod h1:NqM8EUOU14njkJ3fqMW+pc6Ldnwhi/IjpwHt7yyuwOQ=
 golang.org/x/text v0.3.2 h1:tW2bmiBqwgJj/UpqtC8EpXEZVYOwU0yG4iWbprSVAcs=
 golang.org/x/text v0.3.2/go.mod h1:bEr9sfX3Q8Zfm5fL9x+3itogRgK3+ptLWKqgva+5dAk=

```

```
slot: 15
number: 1451
verdict: signal
topic: bsd pledges
confidence: high
why: not entirely unreasonable feature offer, but did not address maintainer concerns.
```

---

## slot 16 — #2759

# #2759 Goto next/previous diff commands + minor cleanups

- state: MERGED
- kind: pull_request
- author: ilyagr (newcomer)
- created: 2023-02-27T00:20:11+00:00
- updated: 2023-05-05T03:43:33+00:00

These commands will work in `git` repositories or whenever `set diff on` is
working. They are bound to `Alt-[` and `Alt-]` by default. I would prefer
`Alt-Up` and `Alt-Down`, but that's already taken. Perhaps we could take
over `Ctrl-Up` and `Ctrl-Down` that are currently the same as `Ctrl-Home` and
`Ctrl-End`. `Alt-n` and `Alt-p` are also possibilities, though inside
`defaults_other.go` they seem to be reserved for CursorUp/Down in the future, maybe.

There are no tests at the moment; I'm looking into writing some since that will
be needed for the rest of the plan to make
https://github.com/zyedidia/micro/discussions/2753 a reality. I'm not sure how
difficult that will be.

This PR also includes a couple of minor cleanups in separate commits. Let me know
if you prefer those as separate PRs.


## Timeline

### 2023-04-20T22:23:28+00:00 — zyedidia (owner)

Looks good, thanks!

### 2023-04-21T00:57:24+00:00 — ilyagr (newcomer)

Good to hear, pleasant surprise. Thanks for the review and for maintaining `micro`! 

## Diff

- internal/action/actions.go +23 -1
- internal/action/bufpane.go +2 -0
- internal/action/defaults_darwin.go +2 -0
- internal/action/defaults_other.go +3 -0
- internal/buffer/buffer.go +36 -1
- runtime/help/keybindings.md +34 -29

```diff
diff --git a/internal/action/actions.go b/internal/action/actions.go
index b5d7f768b0..2b36795a96 100644
--- a/internal/action/actions.go
+++ b/internal/action/actions.go
@@ -1027,6 +1027,28 @@ func (h *BufPane) FindPrevious() bool {
 	return true
 }
 
+// DiffNext searches forward until the beginning of the next block of diffs
+func (h *BufPane) DiffNext() bool {
+	cur := h.Cursor.Loc.Y
+	dl, err := h.Buf.FindNextDiffLine(cur, true)
+	if err != nil {
+		return false
+	}
+	h.GotoLoc(buffer.Loc{0, dl})
+	return true
+}
+
+// DiffPrevious searches forward until the end of the previous block of diffs
+func (h *BufPane) DiffPrevious() bool {
+	cur := h.Cursor.Loc.Y
+	dl, err := h.Buf.FindNextDiffLine(cur, false)
+	if err != nil {
+		return false
+	}
+	h.GotoLoc(buffer.Loc{0, dl})
+	return true
+}
+
 // Undo undoes the last action
 func (h *BufPane) Undo() bool {
 	h.Buf.Undo()
@@ -1311,7 +1333,7 @@ func (h *BufPane) OpenFile() bool {
 	return true
 }
 
-// OpenFile opens a new file in the buffer
+// JumpLine asks the user to enter a line number to jump to
 func (h *BufPane) JumpLine() bool {
 	InfoBar.Prompt("> ", "goto ", "Command", nil, func(resp string, canceled bool) {
 		if !canceled {
diff --git a/internal/action/bufpane.go b/internal/action/bufpane.go
index 847f56416f..f9da9b3aa3 100644
--- a/internal/action/bufpane.go
+++ b/internal/action/bufpane.go
@@ -708,6 +708,8 @@ var BufKeyActions = map[string]BufKeyAction{
 	"FindLiteral":               (*BufPane).FindLiteral,
 	"FindNext":                  (*BufPane).FindNext,
 	"FindPrevious":              (*BufPane).FindPrevious,
+	"DiffNext":                  (*BufPane).DiffNext,
+	"DiffPrevious":              (*BufPane).DiffPrevious,
 	"Center":                    (*BufPane).Center,
 	"Undo":                      (*BufPane).Undo,
 	"Redo":                      (*BufPane).Redo,
diff --git a/internal/action/defaults_darwin.go b/internal/action/defaults_darwin.go
index bae699100f..24b1f06060 100644
--- a/internal/action/defaults_darwin.go
+++ b/internal/action/defaults_darwin.go
@@ -41,6 +41,8 @@ var bufdefaults = map[string]string{
 	"Alt-F":          "FindLiteral",
 	"Ctrl-n":         "FindNext",
 	"Ctrl-p":         "FindPrevious",
+	"Alt-[":          "DiffPrevious|CursorStart",
+	"Alt-]":          "DiffNext|CursorEnd",
 	"Ctrl-z":         "Undo",
 	"Ctrl-y":         "Redo",
 	"Ctrl-c":         "CopyLine|Copy",
diff --git a/internal/action/defaults_other.go b/internal/action/defaults_other.go
index 39a9e0e3dd..2edc48e019 100644
--- a/internal/action/defaults_other.go
+++ b/internal/action/defaults_other.go
@@ -1,3 +1,4 @@
+//go:build !darwin
 // +build !darwin
 
 package action
@@ -43,6 +44,8 @@ var bufdefaults = map[string]string{
 	"Alt-F":          "FindLiteral",
 	"Ctrl-n":         "FindNext",
 	"Ctrl-p":         "FindPrevious",
+	"Alt-[":          "DiffPrevious|CursorStart",
+	"Alt-]":          "DiffNext|CursorEnd",
 	"Ctrl-z":         "Undo",
 	"Ctrl-y":         "Redo",
 	"Ctrl-c":         "CopyLine|Copy",
diff --git a/internal/buffer/buffer.go b/internal/buffer/buffer.go
index 56302e9dc5..38461fbf0c 100644
--- a/internal/buffer/buffer.go
+++ b/internal/buffer/buffer.go
@@ -474,7 +474,7 @@ func (b *Buffer) GetName() string {
 	return name
 }
 
-//SetName changes the name for this buffer
+// SetName changes the name for this buffer
 func (b *Buffer) SetName(s string) {
 	b.name = s
 }
@@ -1211,6 +1211,41 @@ func (b *Buffer) DiffStatus(lineN int) DiffStatus {
 	return b.diff[lineN]
 }
 
+// FindNextDiffLine returns the line number of the next block of diffs.
+// If `startLine` is already in a block of diffs, lines in that block are skipped.
+func (b *Buffer) FindNextDiffLine(startLine int, forward bool) (int, error) {
+	if b.diff == nil {
+		return 0, errors.New("no diff data")
+	}
+	startStatus, ok := b.diff[startLine]
+	if !ok {
+		startStatus = DSUnchanged
+	}
+	curLine := startLine
+	for {
+		curStatus, ok := b.diff[curLine]
+		if !ok {
+			curStatus = DSUnchanged
+		}
+		if curLine < 0 || curLine > b.LinesNum() {
+			return 0, errors.New("no next diff hunk")
+		}
+		if curStatus != startStatus {
+			if startStatus != DSUnchanged && curStatus == DSUnchanged {
+				// Skip over the block of unchanged text
+				startStatus = DSUnchanged
+			} else {
+				return curLine, nil
+			}
+		}
+		if forward {
+			curLine++
+		} else {
+			curLine--
+		}
+	}
+}
+
 // SearchMatch returns true if the given location is within a match of the last search.
 // It is used for search highlighting
 func (b *Buffer) SearchMatch(pos Loc) bool {
diff --git a/runtime/help/keybindings.md b/runtime/help/keybindings.md
index 8d14da7d12..f4aba70f74 100644
--- a/runtime/help/keybindings.md
+++ b/runtime/help/keybindings.md
@@ -30,8 +30,8 @@ following in the `bindings.json` file.
 
 ```json
 {
-	"Ctrl-y": "Undo",
-	"Ctrl-z": "Redo"
+    "Ctrl-y": "Undo",
+    "Ctrl-z": "Redo"
 }
 ```
 
@@ -200,6 +200,8 @@ Find
 FindLiteral
 FindNext
 FindPrevious
+DiffPrevious
+DiffNext
 Undo
 Redo
 Copy
@@ -461,29 +463,31 @@ conventions for text editing defaults.
     "Alt-{":          "ParagraphPrevious",
     "Alt-}":          "ParagraphNext",
     "Enter":          "InsertNewline",
-    "Ctrl-h":          "Backspace",
+    "Ctrl-h":         "Backspace",
     "Backspace":      "Backspace",
     "Alt-CtrlH":      "DeleteWordLeft",
     "Alt-Backspace":  "DeleteWordLeft",
     "Tab":            "Autocomplete|IndentSelection|InsertTab",
     "Backtab":        "OutdentSelection|OutdentLine",
-    "Ctrl-o":          "OpenFile",
-    "Ctrl-s":          "Save",
-    "Ctrl-f":          "Find",
-    "Alt-F":           "FindLiteral",
-    "Ctrl-n":          "FindNext",
-    "Ctrl-p":          "FindPrevious",
-    "Ctrl-z":          "Undo",
-    "Ctrl-y":          "Redo",
-    "Ctrl-c":          "CopyLine|Copy",
-    "Ctrl-x":          "Cut",
-    "Ctrl-k":          "CutLine",
-    "Ctrl-d":          "DuplicateLine",
-    "Ctrl-v":          "Paste",
-    "Ctrl-a":          "SelectAll",
-    "Ctrl-t":          "AddTab",
-    "Alt-,":           "PreviousTab",
-    "Alt-.":           "NextTab",
+    "Ctrl-o":         "OpenFile",
+    "Ctrl-s":         "Save",
+    "Ctrl-f":         "Find",
+    "Alt-F":          "FindLiteral",
+    "Ctrl-n":         "FindNext",
+    "Ctrl-p":         "FindPrevious",
+    "Alt-[":          "DiffPrevious|CursorStart",
+    "Alt-]":          "DiffNext|CursorEnd",
+    "Ctrl-z":         "Undo",
+    "Ctrl-y":         "Redo",
+    "Ctrl-c":         "CopyLine|Copy",
+    "Ctrl-x":         "Cut",
+    "Ctrl-k":         "CutLine",
+    "Ctrl-d":         "DuplicateLine",
+    "Ctrl-v":         "Paste",
+    "Ctrl-a":         "SelectAll",
+    "Ctrl-t":         "AddTab",
+    "Alt-,":          "PreviousTab",
+    "Alt-.":          "NextTab",
     "Home":           "StartOfText",
     "End":            "EndOfLine",
     "CtrlHome":       "CursorStart",
@@ -492,17 +496,17 @@ conventions for text editing defaults.
     "PageDown":       "CursorPageDown",
     "CtrlPageUp":     "PreviousTab",
     "CtrlPageDown":   "NextTab",
-    "Ctrl-g":          "ToggleHelp",
+    "Ctrl-g":         "ToggleHelp",
     "Alt-g":          "ToggleKeyMenu",
-    "Ctrl-r":          "ToggleRuler",
-    "Ctrl-l":          "command-edit:goto ",
+    "Ctrl-r":         "ToggleRuler",
+    "Ctrl-l":         "command-edit:goto ",
     "Delete":         "Delete",
-    "Ctrl-b":          "ShellMode",
-    "Ctrl-q":          "Quit",
-    "Ctrl-e":          "CommandMode",
-    "Ctrl-w":          "NextSplit",
-    "Ctrl-u":          "ToggleMacro",
-    "Ctrl-j":          "PlayMacro",
+    "Ctrl-b":         "ShellMode",
+    "Ctrl-q":         "Quit",
+    "Ctrl-e":         "CommandMode",
+    "Ctrl-w":         "NextSplit",
+    "Ctrl-u":         "ToggleMacro",
+    "Ctrl-j":         "PlayMacro",
     "Insert":         "ToggleOverwriteMode",
 
     // Emacs-style keybindings
@@ -526,6 +530,7 @@ conventions for text editing defaults.
     "MouseMiddle":    "PastePrimary",
     "Ctrl-MouseLeft": "MouseMultiCursor",
 
+    // Multi-cursor bindings
     "Alt-n":        "SpawnMultiCursor",
     "AltShiftUp":   "SpawnMultiCursorUp",
     "AltShiftDown": "SpawnMultiCursorDown",

```

```
slot: 16
number: 2759
verdict: no-signal
topic: diff-wise navigation
confidence: medium
why: It's the PR that introduced the feature. No normative conversation beyond code. It would have help readability if the pr commits were displayed separately, each which its commit message.
```

---

## slot 17 — #1660

# #1660 You can open files under directories that don't exist, without errors

- state: CLOSED
- kind: issue
- author: makew0rld (newcomer)
- created: 2020-05-17T04:25:38+00:00
- updated: 2025-06-09T07:28:51+00:00

## Description of the problem or steps to reproduce
I can open files that are inside non-existent directories. For example, running `micro /tmp/fake/place/test.txt` will open and work fine. I can even "save", but the file doesn't go anywhere of course.

The behaviour I would expect is an error message, and not getting an editor window open.

## Specifications
Commit hash: `f594686` - version 2.0.3
OS: Linux


## Timeline

### 2020-05-17T20:08:28+00:00 — zyedidia (owner)

When I try this, micro correctly gives the following error message:

```
Parent dirs don't exist, enable 'mkparents' for auto creation
```

reactions: THUMBS_UP×2

### 2020-05-17T20:27:40+00:00 — makew0rld (newcomer)

That's strange. Are you on Linux too? The only plugin I have installed is the Go one.

### 2020-05-29T23:16:08+00:00 — semilin (newcomer)

I tried using the same path that you did and this occurred for me. I also tested other directories that don't exist and got the same issue. I am also on Linux.

### 2020-07-17T00:16:58+00:00 — esa1975 (newcomer)

There are local and global settings. You can use either `set` or `setlocal` within micro to change options. Using `set` will make it a permanent global options and using `setlocal` only changes it for the current buffer. The option in this case is `mkparents` which is `false` by default. Using `set` adds the option to the settings.json file. On Linux, this is located at `~/.config/micro`.

More info on settings at https://github.com/zyedidia/micro/blob/master/runtime/help/options.md

reactions: THUMBS_UP×1

### 2020-07-17T15:18:58+00:00 — makew0rld (newcomer)

@esa1975 The issue is that I am not getting the popup saying `Parent dirs don't exist, enable ...`.

### 2020-07-17T15:20:16+00:00 — makew0rld (newcomer)

However, I have just tested and now I am getting the message, everything seems to be working correctly.
```
Version: 2.0.6
Commit hash: 60846f5
Compiled on June 24, 2020
```

### 2023-09-29T18:30:54+00:00 — smac89 (newcomer)

This option needs to be improved to also use `sudo` when attempting to create directories if needed

reactions: THUMBS_UP×2

### 2025-06-09T07:28:50+00:00 — landNull (newcomer)

> This option needs to be improved to also use `sudo` when attempting to create directories if needed

**For any others looking for a solution to have micro auto create directories that do not exist for files and saves the file as root using sudo.**

1. $ sudo micro /DirectoryDoesNotExistYet/YourRootTextFile
2. Ctrl+e
3. > set autosu true
4. > set mkparents true
5. Save the file: Ctrl+s
7. Quit micro: Ctrl+q 

Now whenever I edit root files, it auto creates directories and saves the file as root using sudo. 
$ micro YourRootTextFile

**### micro is kind of a big deal!**

reactions: EYES×1, THUMBS_UP×4

```
slot: 17
number: 1660
verdict: no-signal
topic: mkparents, autosu
confidence: high
why: user asking for what is already present when enabled
```

---

## slot 18 — #3281

# #3281 Carbon syntax highlighter

- state: CLOSED
- kind: pull_request
- author: RohanVashisht1234 (newcomer)
- created: 2024-05-02T17:35:58+00:00
- updated: 2024-05-02T18:53:24+00:00



## Timeline

### 2024-05-02T18:48:09+00:00 — Andriamanitra (established contributor; 5 accepted PRs at time of comment)

Merging this should probably wait until [Carbon](https://github.com/carbon-language/carbon-lang) is no longer considered "experimental". As far as I can tell the language is still going through major changes, and is not ready to be used anywhere yet.

### 2024-05-02T18:51:31+00:00 — RohanVashisht1234 (newcomer)

Ok

## Diff

- runtime/syntax/carbon.yaml +60 -0

```diff
diff --git a/runtime/syntax/carbon.yaml b/runtime/syntax/carbon.yaml
new file mode 100644
index 0000000000..a257bfc780
--- /dev/null
+++ b/runtime/syntax/carbon.yaml
@@ -0,0 +1,60 @@
+filetype: carbon
+
+detect:
+    filename: "\\.carbon$"
+
+rules:
+    # function definition
+    - identifier: "fn [a-z0-9_]+"
+      # Reserved words
+    - statement: "\\b(impl|Main|extend|partial|Self|Int|UInt|Base|template|as|library)\\b"
+      # Constants
+    - constant: "\\b[A-Z][A-Z_0-9]+\\b"
+      # Numbers
+    - constant.number: "\\b[0-9]+\\b"
+      # Booleans
+    - constant: "\\b(true|false)\\b"
+      # Traits/Enums/Structs/Types/etc.
+    - type: "\\b[A-Z]+[a-zA-Z_0-9]*[a-z]+[a-zA-Z_0-9]*\\b"
+      # Builtin types that start with lowercase.
+    - type: "\\b(package|import|fn|var|for|return|class|api|i8|i16|i32|i64|i128|i256|u8|u16|u32|u64|u128|u256|f8|f16|f32|f64|f128|if|else|auto|let|File|while|match|case|default|returned|base|bool|virtual|abstract|String)\\b"
+
+    - constant.string:
+        start: "\""
+        end: "\""
+        skip: '\\.'
+        rules:
+            - constant.specialChar: '\\.'
+
+    - constant.string:
+        start: "\""
+        end: "\""
+        rules: []
+
+    - constant.string:
+        start: "\"\"\""
+        end: "\"\"\""
+        rules: []
+
+    # Character literals
+    # NOTE: This is an ugly hack to work around the fact that rust uses
+    # single quotes both for character literals and lifetimes.
+    # Match all character literals.
+    - constant.string: "'(\\\\.|.)'"
+    # Match the '"' literal which would otherwise match
+    # as a double quoted string and destroy the highlighting.
+    - constant.string:
+        start: "'\""
+        end: "'"
+        rules: []
+
+    - comment:
+        start: "//"
+        end: "$"
+        rules:
+            - todo: "(TODO|XXX|FIXME):?"
+
+    - special:
+        start: "#!\\["
+        end: "\\]"
+        rules: []

```

```
slot: 18
number: 3281
verdict: signal
topic: carbon syntax
confidence: low
why: PR appears valid was closed (by whom?) with no apparent feedback. Could be a starting point for anyone interested in Carbon.
```

---

## slot 19 — #3096

# #3096 Micro do not save file and reopen old file

- state: OPEN
- kind: issue
- author: bloodofdracula (newcomer)
- created: 2023-12-15T20:44:19+00:00
- updated: 2023-12-23T19:07:58+00:00

Linux desktop Zorin Pro 16.3

Micro is not saving file and when opening the same file, after closing and reopening it with micro give the msg

The file on disk has changed. Reload file (y,n,esc)

Closing micro, starting vim, deleting a line with vim for testing...cat file to verify

Micro is loading the old file again (from WHERE ???) deleting a line with micro, saving the file C-s, C-q restart micro file IS NOT updated (Did a check by using vim).

Package from Zorin distribution. Did install a snap version, same result.

Standard installation at ~/.config/micro

Apparently it is happening with the configuration files (in this case bindings.json)

NO automatic saving

![Screenshot from 2023-12-15 12-14-38](https://github.com/zyedidia/micro/assets/153940864/2ce8363b-96c0-4c44-a0f8-b068112b1bae)



## Timeline

### 2023-12-16T02:47:52+00:00 — niten94 (newcomer)

A line can usually be added again in `bindings.json` because a key binding is being tried to be set in a plugin when micro is opened. I think you were trying to delete a line so that nothing would happen when pressing a key, but the action can be set as `None` so that nothing would happen.

For example, the file would be like this when setting the action of `Alt-/` as `None`:
```js
{
    "Alt-/": "None",
    "Ctrl-F2": "command:toggleBookmark",
    "CtrlShift-F2": "command:clearBookmarks",
    "F2": "command:nextBookmark",
    "Shift-F2": "command:prevBookmark"
}
```

### 2023-12-16T07:28:47+00:00 — ghost (established contributor; 21 accepted PRs at time of comment)

Micro writes `bindings.json` before opening anything. So you start micro. Micro starts plugins. Plugins register bindings. Micro rewrites `bindings.json`. Micro finishes initialization and starts to open file you wanted to open. It looks to already overwritten `bindings.json`...

You can even delete the line. Open any file but not `bindings.json`. Close micro. Open `bindings.json` via vim and see that it was rewritten


`The file on disk has changed. Reload file (y,n,esc)` is partially solved by https://github.com/zyedidia/micro/pull/3009 but IIUC only for `settings.json`

### 2023-12-16T13:49:19+00:00 — bloodofdracula (newcomer)

Sorry. I stand my ground.

Start with a small bindings built with vim

Here;

{
    "Alt-/": "lua:comment.comment",
    "Ctrl-F2": "command:toggleBookmark"
}

:wq!

cat .config/micro/bindings.json shows the file (4 lines) as before.

micro .config/micro/bindings.json

Got msg The file on disk has changed. Reload file (y,n,esc)

Did not reply. Did a cat on another terminal for .config/micro/bindings.json and the file has ALREADY BEEN CHANGED by starting micro. It is.

$ cat .config/micro/bindings.json
{
    "Alt-/": "lua:comment.comment",
    "Ctrl-F2": "command:toggleBookmark",
    "CtrlShift-F2": "command:clearBookmarks",
    "F2": "command:nextBookmark",
    "F5": "lua:wc.wordCount",
    "Shift-F2": "command:prevBookmark"
}

Reply n to micro; Exit micro

micro .config/micro/bindings.json

Got the OLD file !!!

From WHERE ?
So ?

Easy to reproduce.






### 2023-12-16T13:52:34+00:00 — ghost (established contributor; 21 accepted PRs at time of comment)

>Got the OLD file !!!
>From WHERE ?
>So ?

Because micro at start regenerates that file!

reactions: THUMBS_UP×1

### 2023-12-16T13:54:38+00:00 — ghost (established contributor; 21 accepted PRs at time of comment)

It doesn't open `old` version. It generates it each time you run micro. You can open **ANY** file with micro and it will regenerate the bindings file

### 2023-12-16T13:57:08+00:00 — bloodofdracula (newcomer)

Sorry you are wrong. THERE IS NO reason fro micro to reinstate configuration lines suppressed by user with the user file at .config/micro/bindings.json

They are user bindings NOT system bindings.

On top micro is adding old user bindings (suppressed by me...).

### 2023-12-16T13:58:49+00:00 — ghost (established contributor; 21 accepted PRs at time of comment)

They are the bindings set by plugins. 

### 2023-12-16T14:02:50+00:00 — ghost (established contributor; 21 accepted PRs at time of comment)

You don't believe me. Just disable your bookmark plugin `Ctrl+e` and then type`> set bookmark off` after it you can again edit your file to:

```
{
"Alt-/": "lua:comment.comment",
"Ctrl-F2": "command:toggleBookmark"
}
```

Micro won't add the lines that was configured by bookmark plugin

### 2023-12-16T14:06:34+00:00 — bloodofdracula (newcomer)

The bindings for bookmarks were set BY ME NOT by the plugin for a start.

From bookmarks plugin page...

How to use:

While editing, press the default key (F11) to set a bookmark at the current line.
You can also use the command toggle_bookmark from the (Ctrl+E) prompt
Press the default key (F10) to loop through all the bookmarks
You can also use the command next_bookmark from the (Ctrl+E) prompt
To remove a bookmark, press the default key again while the cursor is on the bookmarked line

### 2023-12-16T16:58:51+00:00 — JoeKar (established contributor; 10 accepted PRs at time of comment)

> The bindings for bookmarks were set BY ME NOT by the plugin for a start.

https://github.com/haqk/micro-bookmark/blob/baca5fdd6a6475c3b8f9b1bb08192044ffcfff81/bookmark.lua#L401-L405

The plugin tells me something different...

### 2023-12-16T18:16:05+00:00 — bloodofdracula (newcomer)

You were right and it is a strange design for configuration files. I did a check within the bookmark plugin before reading your last msg.

        config.TryBindKey("Ctrl-F2", "command:toggleBookmark", false)
	config.TryBindKey("CtrlShift-F2", "command:clearBookmarks", false)
	config.TryBindKey("F2", "command:nextBookmark", false)
	config.TryBindKey("Shift-F2", "command:prevBookmark", false)


In fact I did not know the bindings..and took the same I was using with Sublime-Text...I was convinced I did it.

It can be confusing. If you start like this

micro .config/micro/bindings.json

micro load the old bindings.json (modified using vim) and after loading plugins (and adjusting bindings.json) tell you file has been changed...

If you start like this

micro and after opening .config/micro/bindings.json no msg of course.

Thanks anyway.

### 2023-12-21T23:01:52+00:00 — dmaluka (established contributor; 37 accepted PRs at time of comment)

> it is a strange design for configuration files.

Yes, it is. If I was @zyedidia I would design it differently.

But we can't just change it now, since we need to preserve compatibility with existing plugins and so on, so...

Anyway, @niten94 has already [mentioned](https://github.com/zyedidia/micro/issues/3096#issuecomment-1858690477) the solution for preventing a plugin from forcing its default binding for a key when there is no user-defined binding: bind this key to `None`.

### 2023-12-22T15:31:15+00:00 — ghost (established contributor; 21 accepted PRs at time of comment)

> But we can't just change it now, since we need to preserve compatibility with existing plugins and so on, so...

As a partial workaround we can (can we?) not to rewrite `bindings.json` if nothing differs so if bindings weren't changed by plugin, user at least won't see annoying "file is changed"...




### 2023-12-23T13:56:31+00:00 — dmaluka (established contributor; 37 accepted PRs at time of comment)

> As a partial workaround we can (can we?) not to rewrite bindings.json if nothing differs so if bindings weren't changed by plugin, user at least won't see annoying "file is changed"...

Isn't that how it already works? (Unless the last argument to `TryBindKey` is true, which I also mentioned in #2647, but that's not a very common case.)

### 2023-12-23T16:49:01+00:00 — ghost (established contributor; 21 accepted PRs at time of comment)

Yeah, you are right it is a last argument of `TryBindKey` in one of my test plugins

### 2023-12-23T18:48:26+00:00 — bloodofdracula (newcomer)

Yes a solution is to bind some keys to None if you do want plugins to populate keys definition (or to change plugins yourself...).
I was using vi (yep..), vim, neovim, emacs, Sublime-Text, gedit, kate NOT a single editor or plugin's editor is changing configuration files during start.
Plugins are offering sometime default key not anything else. You can of course replace the default.
At least emacs has a discovery help..C-h k to discover if a key sequence is used and vim/neovim have plugin(s) to do it.

### 2023-12-23T19:07:57+00:00 — ghost (established contributor; 21 accepted PRs at time of comment)

Currently we have `

> At least emacs has a discovery help..C-h k to discover if a key sequence is used and vim/neovim have plugin(s) to do it.

Now we have `showkey` command that do the same

## Cross-references

- #2647: settings.json is needlessly written every time micro is started (cross_referenced)
- #3009: Fix unneeded rewriting of settings.json (cross_referenced)

```
slot: 19
number: 3096
verdict: signal
topic: bindings.json overwrite
confidence: high
why: Discusses confusing behaviour that is not a bug.
```

---

## slot 20 — #2168

# #2168 Crash when copying and pasting line

- state: CLOSED
- kind: issue
- author: ibrokemypie (newcomer)
- created: 2021-07-23T04:53:19+00:00
- updated: 2021-07-23T05:21:41+00:00

## Description of the problem or steps to reproduce
Go to the start of a line, press control+c, go somewhere else, press control+v
Micro crashes entirely with the following output:
```
Micro encountered an error: runtime error: index out of range
runtime.errorString runtime error: index out of range
/usr/lib/go/src/runtime/panic.go:513 (0x42c789)
	gopanic: // to have been called by the caller of deferreturn at the point
/usr/lib/go/src/runtime/panic.go:44 (0x42b5ca)
	panicindex: // Same as above, but calling from the runtime is allowed.
/home/conor/go/src/github.com/zyedidia/micro/cmd/micro/cellview.go:171 (0x87ce4b)
/home/conor/go/src/github.com/zyedidia/micro/cmd/micro/view.go:845 (0x8d688f)
/home/conor/go/src/github.com/zyedidia/micro/cmd/micro/view.go:1099 (0x8d8b53)
/home/conor/go/src/github.com/zyedidia/micro/cmd/micro/micro.go:245 (0x8a03dd)
/home/conor/go/src/github.com/zyedidia/micro/cmd/micro/micro.go:500 (0x8a1eaf)
/usr/lib/go/src/runtime/proc.go:201 (0x42e5c7)
	main: }
/usr/lib/go/src/runtime/asm_amd64.s:1333 (0x45a211)
	goexit: DATA shifts<>+0x88(SB)/8, $0xffffffffffffffff
```


## Specifications

<!-- You can use `micro -version` to get the commit hash. -->

Commit hash:de35d00
OS:arch linux
Terminal:foot


## Timeline

### 2021-07-23T05:00:59+00:00 — zyedidia (owner)

I recommend updating to the latest stable version because this error message indicates that you are using a pre-2.0 version.

### 2021-07-23T05:21:41+00:00 — ibrokemypie (newcomer)

Ahh so sorry, I had changed my path and was running an older version of go from my gopath rather than my system version.

```
slot: 20
number: 2168
verdict: no-signal
topic: none
confidence: high
why: user reporting fixed bug from old release
```

---

## slot 21 — #3848

# #3848 make arduino filetype detection less aggressive

- state: MERGED
- kind: pull_request
- author: Andriamanitra (established contributor; 13 accepted PRs at time of comment)
- created: 2025-09-01T04:03:02+00:00
- updated: 2025-09-01T18:46:10+00:00

The `?` seems to be there purely by mistake, "ino" without a dot does not even seem to be a convention or anything. [^1]

closes #3847 


[^1]: https://sourcegraph.com/search?q=file:%5B%5E.%5Dino%24&patternType=keyword&sm=0

## Timeline

### 2025-09-01T18:44:58+00:00 — review by JoeKar (maintainer since ~2024; 147 merges at time of comment) [APPROVED]



## Cross-references

- #3847: Shell script named "wino" misdetected as an arduino file (closes)
- #3847: Shell script named "wino" misdetected as an arduino file (cross_referenced)

## Diff

- runtime/syntax/arduino.yaml +1 -1

```diff
diff --git a/runtime/syntax/arduino.yaml b/runtime/syntax/arduino.yaml
index cfa8e4ff98..35a0480f5f 100644
--- a/runtime/syntax/arduino.yaml
+++ b/runtime/syntax/arduino.yaml
@@ -1,7 +1,7 @@
 filetype: ino
 
 detect:
-    filename: "\\.?ino$"
+    filename: "\\.ino$"
 
 rules:
     - identifier: "\\b[A-Z_][0-9A-Z_]+\\b"

```

```
slot: 21
number: 3848
verdict: no-signal
topic: arduino file pattern
confidence: high
why: One char typo bugfix.
```

---

## slot 22 — #742

# #742 Micro encountered an error: runtime error: index out of range

- state: CLOSED
- kind: issue
- author: ibrokemypie (newcomer)
- created: 2017-07-16T12:22:24+00:00
- updated: 2024-04-21T20:49:03+00:00

## Description of the problem or steps to reproduce
Open certain files and begin scrolling down, or open a binary file (stupid I know)

```
Micro encountered an error: runtime error: index out of range
runtime.errorString runtime error: index out of range
/usr/lib/go/src/runtime/panic.go:489 (0x42a66f)
	gopanic: reflectcall(nil, unsafe.Pointer(d.fn), deferArgs(d), uint32(d.siz), uint32(d.siz))
/usr/lib/go/src/runtime/panic.go:28 (0x4292ee)
	panicindex: panic(indexError)
/extra/home/thingo/go/src/github.com/zyedidia/micro/cmd/micro/cellview.go:136 (0x84f4b5)
	(*CellView).Draw: c.lines[viewLine][viewCol] = &Char{Loc{viewCol, viewLine}, Loc{colN, lineN}, char, char, curStyle, 1}
/extra/home/thingo/go/src/github.com/zyedidia/micro/cmd/micro/view.go:723 (0x8a0917)
	(*View).DisplayView: v.cellview.Draw(v.Buf, top, height, left, width-v.lineNumOffset)
/extra/home/thingo/go/src/github.com/zyedidia/micro/cmd/micro/view.go:977 (0x8a2fcb)
	(*View).Display: v.DisplayView()
/extra/home/thingo/go/src/github.com/zyedidia/micro/cmd/micro/micro.go:218 (0x866ed1)
	RedrawAll: v.Display()
/extra/home/thingo/go/src/github.com/zyedidia/micro/cmd/micro/micro.go:428 (0x868756)
	main: RedrawAll()
/usr/lib/go/src/runtime/proc.go:185 (0x42c45a)
	main: fn()
/usr/lib/go/src/runtime/asm_amd64.s:2197 (0x4574c1)
	goexit: BYTE	$0x90	// NOP
```

example file here: https://ptpb.pw/AAAOLGDLbll_zykmGEmi8CfDgQv1

## Specifications

Version: 1.2.1-54
Commit hash: e6f24b0
Compiled on July 16, 2017

OS: arch linux
Terminal: xiate


## Timeline

### 2017-07-18T16:53:14+00:00 — zyedidia (owner)

I could not reproduce this error. Are you able to consistently reproduce it? Maybe things like terminal size, whether softwrap is enabled, or the filetype would help me reproduce the issue?

### 2017-07-23T06:43:56+00:00 — ibrokemypie (newcomer)

hmm, getting the error when opening fstab with a horizontal terminal, but no vertical
```
Micro encountered an error: runtime error: index out of range
runtime.errorString runtime error: index out of range
/usr/lib/go/src/runtime/panic.go:489 (0x42a66f)
	gopanic: reflectcall(nil, unsafe.Pointer(d.fn), deferArgs(d), uint32(d.siz), uint32(d.siz))
/usr/lib/go/src/runtime/panic.go:28 (0x4292ee)
	panicindex: panic(indexError)
/extra/home/thingo/go/src/github.com/zyedidia/micro/cmd/micro/cellview.go:155 (0x84efdd)
	(*CellView).Draw: c.lines[viewLine][viewCol] = &Char{Loc{viewCol, viewLine}, Loc{colN, lineN}, char, ' ', curStyle, 1}
/extra/home/thingo/go/src/github.com/zyedidia/micro/cmd/micro/view.go:723 (0x8a0917)
	(*View).DisplayView: v.cellview.Draw(v.Buf, top, height, left, width-v.lineNumOffset)
/extra/home/thingo/go/src/github.com/zyedidia/micro/cmd/micro/view.go:977 (0x8a2fcb)
	(*View).Display: v.DisplayView()
/extra/home/thingo/go/src/github.com/zyedidia/micro/cmd/micro/micro.go:218 (0x866ed1)
	RedrawAll: v.Display()
/extra/home/thingo/go/src/github.com/zyedidia/micro/cmd/micro/micro.go:428 (0x868756)
	main: RedrawAll()
/usr/lib/go/src/runtime/proc.go:185 (0x42c45a)
	main: fn()
/usr/lib/go/src/runtime/asm_amd64.s:2197 (0x4574c1)
	goexit: BYTE	$0x90	// NOP

```

this was with a 153x23 terminal, with soft wrap.

### 2017-08-09T14:26:22+00:00 — RS-X (newcomer)

I'm able to reproduce this every time just by navigating through the directories in the tree.

### Version
$ micro -version
Version: 1.3.1
Commit hash: dd5afc0
Compiled on August 08, 2017

This is the _micro-1.3.1-linux64.tar.gz_ binary.

### System
Ubuntu 14.04 64 bit

### How to reproduce
// start micro
$ micro

// Open tree
Ctrl+E
\> tree

// Just keep jumping around some directories, certain directories does trigger this error every single time.

### Log

> Micro encountered an error: runtime error: index out of range
> runtime.errorString runtime error: index out of range
> /home/zbyedidia/go/src/runtime/panic.go:489 (0x42a63f)
> /home/zbyedidia/go/src/runtime/panic.go:28 (0x4292be)
> /home/zbyedidia/gopath/src/github.com/zyedidia/micro/cmd/micro/cellview.go:79 (0x84b9cd)
> /home/zbyedidia/gopath/src/github.com/zyedidia/micro/cmd/micro/view.go:723 (0x89d107)
> /home/zbyedidia/gopath/src/github.com/zyedidia/micro/cmd/micro/view.go:977 (0x89f7bb)
> /home/zbyedidia/gopath/src/github.com/zyedidia/micro/cmd/micro/micro.go:216 (0x8630c1)
> /home/zbyedidia/gopath/src/github.com/zyedidia/micro/cmd/micro/micro.go:426 (0x864946)
> /home/zbyedidia/go/src/runtime/proc.go:185 (0x42c42a)
> /home/zbyedidia/go/src/runtime/asm_amd64.s:2197 (0x457411)




### 2017-08-17T18:11:07+00:00 — tommyshem (established contributor; 10 accepted PRs at time of comment)

### Bug in plugin
There is a bug in the filemanager plugin, (tree)
When you go forward in to a folder from the current location, then open a file it will crash. If you go up a folder from the current location then it will open files with out crashing. But soon as you get back to the current location and go into a folder it will crash.
I have put a patch in to micro editor to stop this happening and the plugin will have to be updated if the patch goes in to micro editor. #788
### Problem
It's to do with the current path, it does not get it correctly.
### Not sure about the other files, if a could get a sample of the file to download I could take a look. (not pasted in issues as encoding could be changed by github)

### 2017-09-03T14:56:48+00:00 — zyedidia (owner)

Is this solved? It seems like this isn't really a problem with the editor but rather with the filemanager plugin (which I have removed from the official plugin list due to bugs).

### 2017-09-03T18:21:10+00:00 — tommyshem (established contributor; 13 accepted PRs at time of comment)

`RS-X` - problem should be solved with plugin updating - I will send patch Monday when I get time.
`ibrokemypie` - problem might still be there as he as not said he is using the filemanager plugin to load the file. Need sample of the file causing the problems, not pasted in github issues as text encoding could be changed by github. Need problem file up loading to github repo or dropbox so it can be tested with micro editor with the orignal encoding of the file.

### 2017-11-05T06:06:59+00:00 — parke (newcomer)

I can reproduce this bug fairly consistently (half the time or more) with Micro version 1.3.3.

```
Micro encountered an error: runtime error: index out of range
runtime.errorString runtime error: index out of range
/home/zbyedidia/go/src/runtime/panic.go:491 (0x42b9d3)
/home/zbyedidia/go/src/runtime/panic.go:28 (0x42a6ae)
/home/zbyedidia/gopath/src/github.com/zyedidia/micro/cmd/micro/cellview.go:136 (0x895d1a)
/home/zbyedidia/gopath/src/github.com/zyedidia/micro/cmd/micro/view.go:732 (0x8f21a8)
/home/zbyedidia/gopath/src/github.com/zyedidia/micro/cmd/micro/view.go:986 (0x8f4759)
/home/zbyedidia/gopath/src/github.com/zyedidia/micro/cmd/micro/micro.go:224 (0x8b8e16)
/home/zbyedidia/gopath/src/github.com/zyedidia/micro/cmd/micro/micro.go:460 (0x8ba6d4)
/home/zbyedidia/go/src/runtime/proc.go:185 (0x42d7dd)
/home/zbyedidia/go/src/runtime/asm_amd64.s:2337 (0x45aad1)
```

Softwrap is true.  My terminal size (not that it matters) is 172 by 59.

To attempt to reproduce:
1.  Run ./micro
2.  Type "hello world" (without the quotes, no newline)
3.  Hold down shift and press the left arrow key to highlight all the text.
4.  Press Ctrl+C
5.  Press and hold Ctrl+V to repeatedly paste the text.

At least 50% of the time, within 5-20 lines of "hello world", I will get the above error.

Version: 1.3.3
Commit hash: a02ae3c
Compiled on September 28, 2017


### 2017-11-25T17:45:07+00:00 — sum01 (newcomer)

@parke The branch isn't done (one minor bug atm), but I have a fix for the index out of range bug here https://github.com/sum01/filemanager-plugin/commit/838a3a8d42b99dd3dd1da6a37c789b7246975656

The minor bug is that CursorDown on the file browser moves two spaces, and I'm not really sure why.

### 2024-01-25T11:21:42+00:00 — zipproth (newcomer)

If Micro has a file open that is modified by another process, and the user clicks back into the Micro terminal window, a prompt to reload the file appears (provided the `reload` setting is set to `prompt`). However, if the user's click lands within a region that falls outside the bounds of the file after the reload (because the external modification reduced its size), a crash occurs.

```bash
Micro encountered an error: runtime.boundsError runtime error: index out of range [9255] with length 8321
runtime/panic.go:114 (0x55c53d11411c)
github.com/zyedidia/micro/v2/internal/buffer/line_array.go:395 (0x55c53d54b5d2)
github.com/zyedidia/micro/v2/internal/buffer/buffer.go:1262 (0x55c53d56a079)
github.com/zyedidia/micro/v2/internal/display/bufwindow.go:494 (0x55c53d56a038)
github.com/zyedidia/micro/v2/internal/display/bufwindow.go:717 (0x55c53d568c87)
github.com/zyedidia/micro/v2/internal/display/bufwindow.go:788 (0x55c53d56b299)
github.com/zyedidia/micro/v2/cmd/micro/micro.go:407 (0x55c53d5cfd1c)
github.com/zyedidia/micro/v2/cmd/micro/micro.go:394 (0x55c53d5cfa8c)
runtime/internal/atomic/types.go:194 (0x55c53d119172)
runtime/asm_amd64.s:1650 (0x55c53d14a6e1)
```

```bash
❯ micro --version        
Version: 2.0.13
Commit hash: 68d88b57
Compiled on October 22, 2023
```

### 2024-04-14T22:24:52+00:00 — dmaluka (maintainer since ~2024; 25 merges at time of comment)

> If Micro has a file open that is modified by another process, and the user clicks back into the Micro terminal window, a prompt to reload the file appears (provided the `reload` setting is set to `prompt`). However, if the user's click lands within a region that falls outside the bounds of the file after the reload (because the external modification reduced its size), a crash occurs.

Thanks for reporting. Fixed in #3250.

Regarding the earlier reported crashes in the earlier comments, they are probably not relevant anymore: Micro's code base was nearly entirely rewritten during the refactoring in 2019-2020, and I've never reproduced those crashes in the described scenarios. So I think that once we merge #3250, we can close this issue.

## Cross-references

- #3250: Relocate buffer view when reloading file (closes)
- #788: add comment and let multi values to the log to make it easy to log. (cross_referenced)
- #3250: Relocate buffer view when reloading file (cross_referenced)
- #3250: Relocate buffer view when reloading file (cross_referenced)

```
slot: 22
number: 742
verdict: no-signal
topic: none
confidence: high
why: most of conversation is outdated, what is not was a straightforward bug report and fix
```

---

## slot 23 — #509

# #509 SaveAs function does not exist

- state: CLOSED
- kind: issue
- author: gjelsas (newcomer)
- created: 2016-12-27T12:05:11+00:00
- updated: 2017-01-04T18:52:17+00:00

Commit hash: 67ac3f1
OS: Arch Linux
Terminal: zsh, guake


When I try to add the SaveAs Command to my ~/.config/micro/bindings.json file Iget the following error: 

"function does not exist: Saveas"


% cat ~/.config/micro/bindings.json
{
    "Alt-s": "SaveAs"
}

## Timeline

### 2017-01-04T18:32:45+00:00 — zyedidia (owner)

The `SaveAs` function actually doesn't exist. Internally it does exist, but currently you can bind a key to it. I'll fix this shortly.

### 2017-01-04T18:45:42+00:00 — gjelsas (newcomer)

Thanks for addressing this issue! 

So how can I bind a key to it? Is there antother way for doing it? 

### 2017-01-04T18:52:17+00:00 — zyedidia (owner)

You should be able to bind it now just as you had been. I must have just forgotten to put the function in the list of bindable actions.

```
slot: 23
number: 509
verdict: no-signal
topic: none
confidence: high
why: outdated bug, fixed by owner from initial report, nothing normative
```

---

## slot 24 — #992

# #992 Files opened with VSplitIndex don't load correctly

- state: CLOSED
- kind: issue
- author: sum01 (established contributor; 5 accepted PRs at time of comment)
- created: 2018-01-13T18:33:17+00:00
- updated: 2018-02-04T05:03:55+00:00

## Description of the problem or steps to reproduce
When opening files with `VSplitIndex` (via plugins), block comments don't load, and the file is loaded in some sort of "changed" state. 

What I mean is that if you open with `VSplitIndex` then immedietly try to close it, it thinks it's changed and asks to save.

The comments correctly parse once the file is saved, or if you move the cursor (either with keyboard or by clicking) to the Y position one below it's starting point.
## Specifications
I haven't tried duplicating the issue with `HSplitIndex` or the non-index calls.

Version: 1.4.1-dev.15
Commit hash: aa81cf5
Compiled on February 03, 2018

<details> 
  <summary>Old description</summary>

## Description of the problem or steps to reproduce
I noticed that, when opening large files with block comments, they don't highlight as a comment block until you touch it with the cursor.
## Specifications
This only seems to happen if you open a file via a plugin. 

Specifically noticed from the filemanager-plugin, which uses `CurView:VSplitIndex(NewBuffer("", pathhere), 1)`. Unsure if it matters, but when opening files in this manner, it puts the cursor on the bottom of the file.

Version: 1.3.5-dev.68
Commit hash: 7e3aa33
Compiled on January 11, 2018

</details>


## Timeline

### 2018-01-14T00:22:56+00:00 — zyedidia (owner)

Could you give some instructions to reproduce this? I tested with an xml file with a 50,000 line block comment and didn't experience the issue.

### 2018-01-14T00:52:57+00:00 — sum01 (established contributor; 5 accepted PRs at time of comment)

1. Open a file (containing block comments and whatever else) with `CurView:VSplitIndex(NewBuffer("", pathhere), 1)`. The cursor loads on the bottom, and block comments are fully or partially un-highlighted.
2. Move cursor through block comment. It usually highlights once you get to the first line, but I also noticed c++ files triggering on the second to first line.

I've tried on both Lua and C++ files, and both have the same issue.

### 2018-01-21T23:39:53+00:00 — sum01 (established contributor; 7 accepted PRs at time of comment)

I've noticed that it will also correctly highlight once saved (assuming opened the previously mentioned way), instead of having to move the cursor over it.

### 2018-02-04T02:44:49+00:00 — sum01 (established contributor; 7 accepted PRs at time of comment)

Updated OP with hopefully more helpful description & some things I noticed about it.

### 2018-02-04T03:30:47+00:00 — zyedidia (owner)

I'm a bit confused because you use `NewBuffer("", pathhere)` to create the buffer which will create a new empty buffer with that path. 

If you want to open a file, you should either read the file first pass that as the string or use `NewBufferFromFile` (new since 1.4.0).

### 2018-02-04T04:14:18+00:00 — sum01 (established contributor; 7 accepted PRs at time of comment)

Just tried using `VSplitIndex(NewBufferFromFile(pathhere), 1)` and while comment blocks do show as commented without having to save, it still has the issue of asking if I want to save before closing, even though nothing has changed.

Also, any file opened has a single tab inserted at the very beginning of the file. I'm guessing this weirdly inserted tab is causing the "do you want to save" question.

The only idea I have is that maybe the tab button pressed to open a file highlighted in the filemanager-plugin is getting inserted after loading the file?

edit: This is the callback to tab
```lua
-- Tab
function preIndentSelection(view)
	if view == tree_view then
		-- Open the file
		-- Using tab instead of enter, since enter won't work with Readonly
		try_open_at_y(tree_view.Buf.Cursor.Loc.Y)
		-- Don't actually insert a tab
		return false
	end
end
```
so the tab shouldn't actually be inserted.

### 2018-02-04T04:39:44+00:00 — zyedidia (owner)

Ah I think the issue is the ordering of the actions. Tab is bound to `IndentSelection,InsertTab` so `IndentSelection` fails because you returned false and then `InsertTab` happens and a tab gets inserted into the current view. I'll think a little about how this could be fixed.

### 2018-02-04T04:46:20+00:00 — sum01 (established contributor; 7 accepted PRs at time of comment)

I actually already have a catch for `IndentTab` as well
```lua
function preIndentTab(view)
	return false_if_tree(view)
end
```

edit: Ah, I see what you mean.

### 2018-02-04T04:58:35+00:00 — zyedidia (owner)

One problem is that it should be `preInsertTab` instead of `preIndentTab`. But this doesn't completely fix the issue because the second action is executed in the next view that was opened (see #1015) which is no longer the tree view.

### 2018-02-04T05:02:28+00:00 — sum01 (established contributor; 7 accepted PRs at time of comment)

Just whipped up a little workaround now that I know I had the callback name wrong.
```lua
local tab_pressed = false

-- Tab
function preIndentSelection(view)
	if view == tree_view then
		tab_pressed = true
		-- Open the file
		-- Using tab instead of enter, since enter won't work with Readonly
		try_open_at_y(tree_view.Buf.Cursor.Loc.Y)
		-- Don't actually insert a tab
		return false
	end
end
function preInsertTab(view)
	if tab_pressed then
		tab_pressed = false
		return false
	end
end
```

I'll patch, tag, and push to filemanager-plugin in a little bit.

## Cross-references

- #1015: Error on setting keybinding 'CtrlO' : "AddTab, OpenFile"  (cross_referenced)

```
slot: 24
number: 992
verdict: no-signal
topic: 
confidence: high
why: debugging filemanager plugin, no normative conversation
```
