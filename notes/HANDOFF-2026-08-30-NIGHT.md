# Handoff — 30 August 2026, night

**Supersedes `notes/HANDOFF-2026-08-30-EVENING.md`**, which is still accurate on the
sixteen-node research pass, the Design hand-over and Stewart's backlog. Everything below
happened after it.

**`git fetch --all` before you read another word.** Then:

```
cd /path/to/the-legacy-program-dashboard
python3 tools/state_snapshot.py --gate
```

---

## 0. Two hand-overs, unchanged from the evening handoff

| to | give them |
|---|---|
| **the next Claude Code session** | this file |
| **Claude Design** | `notes/DESIGN-BRIEF-2026-08-30-NETWORK.md` — **not** this file |

Design still has **not** been sent anything. Section 0 of the evening handoff lists what
they need in full. Everything they need is on `master`.

---

## 1. State

| | |
|---|---|
| `master` | PRs #16-#19 merged: 16 nodes, CI deploy, podcast tooling, transcript exporter |
| **PR #20** | **OPEN, and it is the important one.** The network-map zoom floor + windowed audio decoding. Merge it |
| live board | https://the-program-zxz.pages.dev — deploys itself on every push to `master` |
| board | 980 nodes · 2,194 edges · 4,728 claims · L0 112 |
| transcripts | 26 of 140 Michels, in `research/.transcripts/` (gitignored, **lost when this container dies**) |

---

## 2. The label bug — FIXED, in PR #20

Stewart reported it twice: *"not a single node is named… the white text scales as you zoom
and never lands on anything."*

**What it was.** Labels draw at a fixed 9px on SCREEN while the field shrinks with the
camera. Measured at 1920 after seven clicks of zoom-out: 980 nodes in a cluster ~250px
wide, carrying 17 labels each 100–300px wide, one rendering entirely *below* the field.
Each anchored to a two-pixel dot among hundreds.

The collision system was not failing — it had already dropped 104 labels to 17. Seventeen
unattributable labels is still wrong, because at that scale the problem is attribution.

**The fix.** `LABEL_ZOOM_FLOOR = 0.62` in `tools/network_patches.py` — the same number
Design gave the packed map on 26 August. Selection, its neighbours and the 14 highlights
stay exempt at every zoom. Result: 17 ambient labels → 0. Rest state untouched at 115.

**Self-tested**: `POISON=floor node tools/runtime_check.js` disables the floor on a real
frame and requires 33 ambient labels to reappear.

### Three things that cost hours here, all worth knowing

1. **`MAP` is a SHARED variable.** `mountL0()` and `mountNetwork()` both assign it, so it
   points at whichever map mounted last — usually the PROGRAM map. Every
   `MAP.zoom('out')` in a probe zooms an invisible map while the network map sits still.
   **Drive the real UI controls.** This made a bisect "prove" a correct fix was wrong.
2. **Wrap `CanvasRenderingContext2D.fillText` and capture a stack** when you need to know
   what draws something. It named the function in one run after three wrong diagnoses
   from reading source.
3. **A camera-moving check must run LAST.** `runtime_check.js` says this twice above the
   `mark` check. A third camera-mover added mid-file left the zoom easing running and the
   stillness check failed, correctly. Ordering is the fix.

---

## 3. The transcript OOM — FIXED, and the real lesson is about committing

`fetch_podcast.py` was OOM-killed **three times**, exit 137, always on a long episode.
**Two theories were written down and both were wrong** — contention with the browser
checks, and a leak across whisper calls. Neither survived measurement.

**The real cause: the fix was written and measured three hours earlier and never reached a
commit.** A branch-reset one-liner ran `git stash pop --quiet 2>/dev/null`, which failed
silently, and the `git add -A && git commit` right after committed the file *without* the
fix. `git log -S iter_windows` found it in zero commits. The commit message asserted
measurements for code that was not in the commit.

**So: after any commit that matters, verify the code is IN it.**

```
git show HEAD:path/to/file | grep -c the_thing_you_added
```

Measured on the episode that killed all three runs (4h12, 44.1kHz stereo, 243MB):

| | peak |
|---|---|
| whole file, as shipped | **12.37 GB**, exit 137 |
| decode alone, windowed | 0.24 GB, flat over 12 windows |
| one 20-min window + model | 1.52 GB |
| the real tool, windowed | **0.53–0.70 GB steady** |

---

## 4. Transcripts — where to pick up

**Tooling is complete and on `master`.** Three feeds resolved, all reachable from any IP:

| show | episodes | hours | back to |
|---|---|---|---|
| `michels` | 140 | 285 | Oct 2024 |
| `area52` | 107 | 185 | Sep 2023 |
| `dannyjones` | 426 | 1,068 | **Nov 2018** |

```
python3 tools/fetch_podcast.py --show michels --max-hours 8     # fetch + transcribe
python3 tools/export_transcripts.py --out <somewhere>           # -> readable .md per episode
```

**Do not run it alongside the browser checks** — both are memory-hungry; the docstring
says so. **UAP Gerb has no podcast feed** (three Apple searches); he is YouTube-only, so
the 35-episode corpus in `research/leads/` is all of him reachable.

**This container's transcripts are disposable.** `research/.transcripts/` is gitignored
and the container is reclaimed without warning. The durable copy is Stewart running the
same tool on his own machine. Do NOT commit transcripts.

### What to DO with them, which is Stewart's actual ask

Not "read them" — mine them for gaps:

1. **Extract** every name, document number, date, programme and company mentioned
2. **Cross-check** against the 980 nodes with `tools/corpus_crosscheck.py`, which
   classifies each as NODE / PROSE / ABSENT
3. **Triage** — ABSENT + a document is a candidate; ABSENT + an anecdote is noise
4. **Verify** by opening the document, then build

That is exactly the pipeline that turned 35 Gerb episodes into today's 16 sourced nodes.
The part Stewart cannot do by hand is names recurring across *different* hosts and guests.

**Already found, unadjudicated:** the first exported episode has a host saying NASA's term
for UFOs in space is "fast walkers… a code word." The `afit-townsend-2008` node added
today contradicts that from a primary document — AFIT/GA/ENY/08-M06 defines *fastwalker*
as ordinary space-surveillance vocabulary, uses it 34 times, and never says *UFO* in 112
pages. **That adjudication is not on the board yet.**

---

## 5. Eric Davis — do not change the node yet

Stewart's framing: Davis "came out and said the Wilson-Davis memos were all true." The
record is more interesting than that:

- Davis has been forthcoming in 2026 — a detailed March interview, and on **18 August
  2026** on NewsNation said he has "seen the evidence" and "seen the records"
- **No government body has authenticated the memo**
- **Admiral Wilson has not confirmed the meeting.** Stewart's added context: Wilson was
  originally more open, then quickly began denying and has maintained that since

So Davis endorsing **his own memo** is not authentication — he is its author, and the
other named party disputes it. That is a Tier 2 claim, not a confirmation.

**Nothing from the above is on the board**: those are search-result summaries, not
documents opened. §2 requires opening the source. The pass worth doing is the NewsNation
segment, the March interview, and Wilson's own words — and if the *shift* in his posture
is documentable with dates, that is a stronger claim than either half alone.

Stewart accepts the current classification and notes the UFO community treats it as
all but confirmed. That gap is worth carrying explicitly.

---

## 6. Still open

| | |
|---|---|
| **Merge PR #20** | the label fix and the OOM fix are both in it |
| **Send Design the brief** | nothing has been sent |
| Restart the transcription run | `python3 tools/fetch_podcast.py --show michels --max-hours 8` |
| Stewart's backlog | patent drawings not clickable; Analysis panel squished left; more than 34 analysis examples; label treatment (Design Q2); filters are additive reveals (Design Q3/Q4) |
| `spot_check.py --links` | not re-run since the research pass added ~100 URLs |

**Not verified on screen:** thirteen of the sixteen new nodes, and no dossier has been
opened by hand for any of them.
