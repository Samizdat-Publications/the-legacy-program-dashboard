# Handoff — 30 August 2026, evening

**This supersedes `notes/HANDOFF-2026-08-30.md`.** That one is the morning brief and is
still accurate on the map inversion, the patents tab and the FOIA layer. Everything below
happened after it.

**Run `git fetch --all` before you read another word of this.** `CLAUDE.md` §4 says so and
this project has paid twice for ignoring it.

Then, before you touch anything:

```
cd /path/to/the-legacy-program-dashboard
python3 tools/state_snapshot.py --gate
```

Do not trust a number in this file. It derives every one of them from source.

---

## 0. Two hand-overs, and they are not the same document

| to | give them | which is |
|---|---|---|
| **the next Claude Code session** | this file | the whole picture. A session on this repo loads `CLAUDE.md` automatically and `CLAUDE.md` points here, so the URL is belt-and-braces rather than strictly required |
| **Claude Design** | `notes/DESIGN-BRIEF-2026-08-30-NETWORK.md` | a different document, written for someone with no memory of this project. **Do not send them this handoff** — it is full of repo mechanics they cannot use and does not contain the brief |

**Both are on the branch until PR #16 merges, and a link to a branch is a link the next
session may never see.** `CLAUDE.md` §4 records what that cost when PR #5 held a day's work
as an open draft. Merge #16, then hand over `blob/master/...` URLs, not
`blob/claude/browser-env-tests-61xi1t/...`.

### What Design needs, in full

1. `notes/DESIGN-BRIEF-2026-08-30-NETWORK.md` — self-contained, figures current to 980 nodes
2. the repo and branch **named explicitly**: `Samizdat-Publications/the-legacy-program-dashboard`, branch `master`
3. the five screenshots at `notes/design-2026-08-30-network/` — under 1MB each, so the GitHub API can open them
4. `data/design-extract.json` (287KB) if they want the underlying data — **never** the big three
5. `notes/MAP-INVERSION-2026-08-29.md` §9, which carries the two questions they are still owed: the inversion reversed their own spec and they have not seen it

**Nothing has been sent to Design yet.** The brief is written and current; the hand-over is
an action nobody has taken.

---

## 1. State

| | |
|---|---|
| `master` | carries PR #15 (Design's five changes, the label pass, the shell fixes) |
| PR #16 | **OPEN DRAFT** — sixteen new nodes from the verified leads. Green. Merge it before handing off again |
| branch | `claude/browser-env-tests-61xi1t` |
| board | 980 nodes · 2,194 edges · 4,728 claims · 885 timeline events · L0 112 |
| gate | 52 verify + self-test · 40 audit · 46 runtime · 31 canvas · 15 analyst · `--idempotent` · `check_rebuild` run the way its docstring says — all green |
| **DEPLOY** | **still outstanding, and a cloud session still cannot run it.** No Cloudflare token in the environment |

---

## 2. What was built

### The node pass — PR #16

Section A and section B of `research/leads/CANDIDATES-2026-08-30.md`, which Stewart
approved with "Yes build it". Sixteen nodes in `research/legacy-1947-86.json`, two entity
dossiers in `research/dossiers/legacy-1947-86-l0.json`, 22 claims onto seven existing
nodes, 23 edges, 13 timeline events, 13 recorded gaps.

Two of the sixteen were **not** on the approved list of fourteen and are easy to cut:

| | why it is there |
|---|---|
| `defense-investigative-service` | the GAO 1986 evidence names it as the body carved out. The argument does not land without it |
| `afit-townsend-2008` | section B said to attach the fastwalker material "wherever FASTWALKER lives". It lived nowhere on the board, so the document became the node |

**Three things a next session must not undo.**

1. **The exclusions in section E of the candidates file are deliberate.** No edge from
   `robert-sarbacher` to `research-development-board` (the consultancy has no primary
   record and is carried at T3 on the person). No edge from `george-trimble` to
   `louis-witten` (the one openable source says the traffic ran the other way). No edge
   from `bdm-international` to `northrop-grumman` (the BDM → TRW → Northrop chain was
   never read off a document, so BDM connects only by its McLean address). Each of these
   looks like a missing edge and each is a decision.
2. **`sperry-rand` is deliberately unattached.** Its only documented link is Douglas
   MacArthur, who has no node. Inventing an institutional edge on the strength of the
   Considine column would be an inference, not a record. The board already carries 113
   unattached nodes; this is the 114th on purpose.
3. **The corrections in section D are load-bearing and easy to un-correct.** The Lockheed
   unaccounted-for total is **11**, not 17 plus 46. The Moon Dust 49/17 figures are
   **deorbit notifications received**, not objects recovered. JANAP 146 carries no dollar
   figure — 18 U.S.C. 793 does. Neither Brown patent claims anti-gravity. Project
   Winterhaven contains no saucer and no interceptor.

### What the map did about it

**L0 went 110 → 112.** `usaf` and `lockheed-skunk-works` crossed the degree floor of 6 on
the new edges. `CLAUDE.md` §9 records that under the corrected floor `usaf` was not on the
map at all. It is now. Both needed entity dossiers they did not have;
`lockheed-skunk-works` needed an authored short, because its derived one was 45 characters
against the 37 a chip holds.

**All 31 canvas assertions still pass at 112 chips.** The layout is grid-derived, so it
absorbed the two new nodes without a hand edit. That is the design working.

### Two defects, and the second one is the useful part of this session

**One. `merge.py` drops a research record with no `cls`, in silence.** The section B
records were authored with `id` + `claims` + `sources` only, so all seven were dropped and
22 claims never reached the board — with the build otherwise green and every other check
passing. `no research record is silently dropped` named all seven by id. That check exists
for exactly this and it earned its place.

**Two. `check_rebuild.py` could pass by proving nothing, and did.** This one is worth
reading properly, because it cost a red CI run and two commits.

`check_rebuild.py` **does not rebuild.** It diffs the working tree against HEAD, and its
own docstring says to run it "on an OTHERWISE-CLEAN tree, AFTER running the section 3
pipeline". It was run immediately after committing, on a clean tree, with no build in
between — so it compared a clean tree against HEAD, found nothing, and printed
**"committed artifacts match a fresh build"** over eleven artifacts that a fresh build does
not reproduce. That sentence then went into a commit message and a PR body.

The underlying miss: after fixing the `cls` bug, only `merge.py` was re-run, not
`merge → regrade → merge`. So `regrade.py` never scored the 22 new claims and everything
downstream of it was built from a board regrade had not seen. CI was right and the local
gate was wrong.

**`check_rebuild.py` now refuses to say it.** If no file the pipeline writes is newer than
`.git/index`, there was no build to compare, and it exits non-zero naming the pipeline. The
three flows it has to separate:

| | | |
|---|---|---|
| CI | checkout, build, then this | artifacts newer — passes |
| the documented local flow | build, then this | artifacts newer — passes |
| what happened here | build, **commit**, then this | index newer — **refused** |

Both directions are self-tested against real mtimes on real `BUILT` paths — the filesystem
is poisoned, not a stand-in predicate. §5's sibling rule.

**So: run the whole section 3 pipeline, every time, and run `check_rebuild.py` before you
commit rather than after.** Three instances of §5 in one session.

---

## 3. The Michels transcripts — BLOCKED, and it is not a code problem

**YouTube has durably blocked Stewart's home IP.** This is the state, established rather
than guessed:

| | |
|---|---|
| catalogue | 180 videos resolved and triaged. `research/leads/michels-catalog.json`, `michels-selected.txt`, `michels-triage.md` |
| already cached | 24 transcripts, in `research/.transcripts` — **gitignored on purpose, do not commit** |
| still wanted | ~156 |
| overnight run | 5 passes over 8 hours. **Every attempt 429.** The machine did not sleep; its sleep setting is Never and the log shows all five passes running |
| single-video probe, next morning | still 429, on the `--ytdlp` path |

**The fix is a different IP, not more waiting.** Phone hotspot or a VPN. The one-video
probe to test it, as a paste-ready block:

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
python tools\fetch_transcripts.py --ids RTEWLSTyUic --ytdlp
```

If that comes back with a transcript rather than a 429, the full sweep is:

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
python tools\fetch_transcripts.py --select research\leads\michels-selected.txt --ytdlp --until-done --sleep 8 --max-hours 6
```

**What NOT to do:** do not re-run against the blocked IP to confirm the block. That is what
burned it in the first place — 169 malformed requests, from a `--select` bug that read the
whole `ID # title` line as the id. The bug is fixed; the reputation damage is not.

**Cookies do not help and the failure is not a video failure.** Chrome 127+ App-Bound
Encryption means `--cookies-from-browser` fails with a DPAPI error whether or not Chrome is
running, and closing the browser does not change it. `_COOKIE_FAIL` in
`tools/fetch_transcripts.py` detects that and falls back rather than reporting 169
individual video failures.

---

## 4. Design — what is ready and how to hand it over

`notes/DESIGN-BRIEF-2026-08-30-NETWORK.md` is **written, self-contained and current.** Its
figures were updated tonight to the 980-node board.

**Read `CLAUDE.md` §4 on this before you send it.** A Design session starts with no memory
of this project and reads GitHub only when told the exact `owner/repo` AND the exact
branch. A brief that opens "read CLAUDE.md, then these three notes" is a brief Design
cannot act on — one was written that way on 30 August and it bounced.

### The screenshots — this is the part that is easy to get wrong

Five PNGs live at **`notes/design-2026-08-30-network/`**, committed and on `master`:

| file | what it shows |
|---|---|
| `1-rest-1920.png` | the map at rest, 1920 — the density problem |
| `2-selection-1920.png` | Tom DeLonge selected, all ten neighbours labelled, sourced drawn brighter than derived |
| `3-zoomed-out-1920.png` | zoomed out — labels hold their size, marks hold their floor |
| `4-rest-1366.png` | at rest, 1366 |
| `5-rest-2560.png` | at rest, 2560 |

Three rules for them:

1. **They are on `master` and under 1MB each, so Design can open them through the GitHub
   API.** Cite them by repo-relative path and name the branch. Never cite
   `data/the-program.json`, `data/l0-model.json` or `dist/the-program.html` — at 7MB, 6MB
   and 16MB the API reports them as **absent**, not as too large, which has misled two
   sessions.
2. **They were captured at 964 nodes and the board is now 980.** The brief says so in its
   own second paragraph. Do not quietly re-cut them and leave the figures behind, and do
   not leave the discrepancy unstated — that is the whole failure mode this repo keeps
   hitting.
3. **`data/design-extract.json` (287KB) is the data file for Design.** Purpose-built,
   readable, under the cap. Hand it to them; do not point at the repo and hope.

If you re-capture: `node tools/look.js` sweeps four viewport sizes into `dist/shots/`, and
`tools/walk.js` is the fuller instrument. Both are cameras, not checks — they assert
nothing and cannot fail. Report what you actually saw and nothing more.

### The open question Design still owes an answer on

The map inversion of 29 August **reverses Design's own spec**: the packed layout was
theirs, built to it, with 31 canvas assertions behind it, and it is now a secondary tab.
`notes/MAP-INVERSION-2026-08-29.md` §9 has the two questions worth their time.

---

## 5. Backlog Stewart reported from the live board, logged and not started

From his screenshots on 30 August, in his own framing:

| | |
|---|---|
| patent drawings | not clickable to full screen. He also wants Design to eventually recreate the schematics |
| Analysis panel | "the area in the white is squished to the left and doesn't make use of the blank space" |
| analysis examples | wants more than the current 34 |
| plain white labels | "I don't like the plain white labels we have everywhere" — needs a treatment, maybe a background. This is Q4 in the Design brief |
| filters | "clicking the various filters doesn't really materially change or highlight anything". **Measured**: 463 of 980 nodes sit at 0.01 opacity at rest; the filters are additive reveals, so clicking Tier A takes the map from 501 nodes at α≥0.5 to 956. It reveals rather than filters. This is Q3 in the Design brief |

Fixed on 30 August and already on `master`, so do not re-diagnose them: neighbour
labelling (was 1 of 10, now 10 of 10, 0 overlaps at four widths), the minimum mark size,
the fixed-size selection plate, hold-space-to-pan, sourced-vs-derived brightness, the
em-dash → C1 control character in `L0_CSS`, and the dossier "CLICK TO OPEN" spine, which
worked only on PROGRAM because its handler was registered inside the packed map's mount.

---

## 6. One outstanding research item with a source Stewart has and the board does not

Stewart, 30 August: Eric Davis **"has later/recently come out in interview and said the
Wilson-Davis memos were all true etc so we don't have to speculate anymore."**

The board's `eric-davis` node still carries the speculative framing. **Do not change it
without the interview.** §2 governs: that needs a citation someone has opened, not a
recollection of one. Ask Stewart which interview and where, then adjudicate it the way
the 30 August leads pass adjudicated everything else.

---

## 7. What is NOT verified

**Partly looked at.** Three of the sixteen were selected on the NETWORK map at 1920 and
captured to `notes/newnodes-2026-08-30/`. What those three captures actually show:

| | |
|---|---|
| the stats strip | reads 980 / 2194 / 62% of 4728 / TIER A 146 / DENIALS 175 / CUSTODY 121, and the rail reads Timeline 885, Case files 286 — all matching `state_snapshot.py` |
| renderer | `webgl2 · 980 nodes` |
| `gao-130581` selected | draws and labels all four authored neighbours: DEFENSE INVESTIGATIVE SERVICE, GOVERNMENT ACCOUNTABILITY OFFICE, LOCKHEED MARTIN CORPORATION, LOCKHEED MARTIN ADVANCED DEVELOPMENT PROGRAMS |
| `usaf-1127th-field-activities-group` selected | draws and labels all four: UNITED STATES AIR FORCE, PROJECT MOON DUST, OPERATION BLUE FLY, WRIGHT-PATTERSON AIR FORCE BASE, OHIO |

**Two things those captures do NOT establish, and the distinction matters.**

1. The probe set `S.sel` directly through `window.__board` rather than clicking, so the
   left rail still reads NOTHING SELECTED and the dossier never opened. **That is the
   probe, not the board.** The dossier path on both tabs was fixed earlier on 30 August
   and has its own runtime assertion. Nobody has yet opened a dossier for a new node by
   hand.
2. `gao-130581`'s label middle-truncates on the map to `GAO ACCESSION 130581,CKHEED
   CORPORATION`, which reads as garbage. **This is not a defect this pass introduced** —
   it is the network map's existing truncation, and `gao-04-332` has an even longer label
   already. It is **Q2** in the Design brief, where it is now written up as a concrete
   instance with the `data/l0-shorts.json` precedent beside it. Do not "fix" it by
   shortening the document's real title; the label is the document's own name.

The other thirteen new nodes have not been looked at, and no dossier has been opened.

`tools/spot_check.py --links` has not been re-run since the research pass. The board had
zero dead citations on 25 August; this pass added 3,042 − 2,941 ≈ 100 new unique URLs and
none of them has been through the sweep. It is deliberately not in the build gate because
it depends on the network. Run it before the next deploy:

```
cd /path/to/the-legacy-program-dashboard
python3 tools/spot_check.py --links
```
