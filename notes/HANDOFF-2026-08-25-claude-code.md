# Handoff to Claude Code — and your first task

**Written 25 August 2026** at commit `a1d041b`, by the Cowork session that did the
L0 map, the research backfill, Design's two layout rounds and the no-key analyst rewrite.

**Your first task is not to build anything. It is to read the repo and propose a phase
plan.** The brief for that is §6. Everything before it is what you need to do it well.

---

## 1. Read these, in this order

1. **`CLAUDE.md`** — authoritative. Rules, build order, gate, constraints, priorities.
2. **This file** — why things are the way they are, and what to be careful of.
3. **`notes/ANALYST-NOKEY-2026-08-24.md`** — the most recent session's findings, and the
   clearest single statement of the failure mode that keeps recurring here.
4. **`notes/design-2026-08-24/DESIGN-RESPONSE-LAYOUT-2026-08-24.md`** — Design's spec for
   the work that is next. Long, and worth all of it.

Then, before forming any opinion about state:

```
python3 tools/state_snapshot.py --gate
```

**Do not take any figure in any document, including this one, as current.** That script
derives everything from source and runs the gate. It exists because every handoff this
project has written went stale while continuing to read as confident. Three were found
doing exactly that on 24 August, one of which told the reader to skip testing the component
that was broken.

---

## 2. What state you are inheriting

Green. Working tree clean, everything pushed to `master`.

- **Gate:** 18 verify checks (each demonstrated rejecting bad input), 38 independent audit
  checks, 15 analyst branch assertions, and a two-build idempotency check.
- **Board:** run the snapshot. Roughly a thousand nodes, a couple of thousand hand-written
  sourced edges, and every L0 node carries a researched dossier.
- **The map:** 110 nodes, all dossiered, six curated entry paths, focus-on-select working.
- **Design:** both open questions answered, §6.1 unblocked. The layout is specified and
  **not yet built** — that is the biggest open piece of work.

---

## 2b. THERE IS AN UNMERGED BRANCH WITH 19 COMMITS ON IT

**Read this before you plan anything. It changes the plan.**

```
origin/claude/status-update-bewtdk
```

An earlier Claude Code session did substantial work that **never reached `master`**. It is
not lost, it is not broken, and it has not been overwritten. It has diverged:

| | |
|---|---|
| merge-base | `3d633f9`, 21 August |
| commits only on the branch | 19 |
| commits only on `master` | 11 |

### What is on it

Data-integrity and sourcing work, and it is good:

- 88 broken reference fields found and fixed; every reference field now checked
- Tier 1 claims carrying no URL: **90 to 0**, and the sourcing rule stopped being US-only
- Duplicate-node detection — the FY2024 sec. 1687 statute was on the board **three times**;
  nine duplicate groups collapsed, 19 nodes to 9, and a twelve-seat error fixed
- A link sweep of all 1,198 source URLs
- `edge_without_note` **74 to 0** — every edge now says what it asserts
- Roughly 250 edges sourced: DIRD series and authors, congressional, Brazil, SAP statutory
- 32 CFR 117.6(b)(3), EO 13526 and Sec. 6802 read from primary text
- `tools/runtime_check.js` — **runtime verification in a real browser**, which is precisely
  the gap a cloud session has
- Four more verify checks: person back-references, duplicates, affiliations, chain shape
- Affiliations render as names and navigate; 54 slugs stopped leaking to readers

`master`, meanwhile, has the L0 program map, the research backfill, both Design layout
rounds, the highlights and image layers, the no-key analyst rewrite, and
`tools/audit_independent.py`.

**Neither side is a superset. Both are worth keeping.**

### The merge was tested, and it is far easier than the diff suggests

The raw diff is ~61,000 lines, which is alarming and misleading. Almost all of it is
generated. A test merge was run in a throwaway worktree on 25 August:

| | |
|---|---|
| files auto-merging cleanly | 23, including **both** hand-edited tools |
| genuine conflicts | **3** |
| of those, generated (resolve by rebuilding) | `data/l0-model.json`, `dist/the-program.html` |
| of those, needing a human | **`SESSION-HANDOFF.md`, and only that** |

`tools/verify.py` and `tools/build_dashboard.py` **auto-merged with no conflict** — the
branch added four checks and an affiliation renderer, `master` added one check and the
analyst rewrite, and they touch different regions.

**`research/` does not conflict at all**, which is the fact that makes this tractable.
`research/` is the source of truth; `data/` and `dist/` are derived from it. So the
procedure is: take both sides of `research/`, resolve the generated files by **rebuilding
rather than by choosing a side**, and hand-merge one markdown file.

After rebuilding, on the merged tree:

- `verify.py` — **22 checks, all passing**, all self-tested (18 + the branch's 4)
- `test_scripted_analyst.mjs` — 15 branch assertions, passing
- `audit_independent.py` — **2 failures**, and they are real

### The two failures are a find, not a merge artifact

```
stats strip TIER A:      rendered/model 144 vs independently derived 142
breadcrumb object count: rendered/model 428 vs independently derived 436
```

`tools/audit_independent.py` is master-only — it does not exist on the branch, so **the
branch's data has never been subjected to it.** The branch's own gate passes cleanly. Two
counts on that branch disagree with an independent derivation, most plausibly because the
duplicate collapse updated one code path and not another.

This is the repo's whole thesis arriving on schedule: a suite that passes is not evidence
until something independent has tried to break it. **Do not paper over these by
regenerating `tools/GOLDEN.json`.** The manifest exists to catch exactly this. Find out
which of the two numbers is right and why they differ.

### What NOT to do

- **Do not `git push --force` anything.** The branch is the only copy of that work.
- **Do not resolve a generated file by picking a side.** Rebuild it. Picking a side bakes
  in one branch's stale derivation.
- **Do not merge before Stewart says so.** It is his call, and the audit failures should be
  understood first.

---

## 3. What is deliberately unfinished, and why

Do not "fix" these without reading the reasoning. Each is a decision, not an oversight.

| Thing | State | Why |
|---|---|---|
| `data/l0-images.json` | plumbed, validating, **empty** | A record asserts an image exists at a URL under a licence. That is a sourcing claim and needs verification, not a plausible guess. All 110 nodes draw the class letter, which is a supported state. |
| `data/l0-highlights.json` | 14 flags, **DRAFT** | Editorial judgement. Needs Stewart's sign-off, and he cannot read JSON — show a table. |
| `disclosure` band at 3 nodes | left thin | Design's explicit answer: it is a *residual*, not a category. Promoting it by hand would destroy what the layout says. |
| `RARITY_PIN` legacy drift | reported every run | The pin working, not failing. Editing the constant to quiet it is the failure it exists to prevent. |
| Tier 3 claims | 493 of them, kept | Not padding. The board labels its own weakest claims so a critic does not have to. |

---

## 4. The failure mode — read this twice

`CLAUDE.md` §5 states it. Here is why it deserves the space:

> **A check that has never been shown to fail is indistinguishable from a broken one.**

The most recent instance, from 24 August, is the cleanest illustration this project has
produced. The scripted analyst — the only voice a reader without an API key ever hears —
had been inherited from a sibling board with **one string swapped**. It answered questions
about this board with confident, well-sourced, correctly-formatted answers about a
different project entirely. Nothing errored.

It was rewritten. A test was written. **The test passed while six of the seven suggestion
chips routed to the wrong branch**, because it asserted that a long answer came back
carrying valid commands — which any well-formed wrong answer satisfies. Only when it was
changed to assert *which branch fired* did it catch all six at once. One of them:
`tell me about AAWSAP` hit the legal-mechanism topic, because `/sap/` matches inside the
word `aawsap`.

**The operational rule:** every check you add must be demonstrated rejecting the input it
must reject. `verify.py --self-test` enforces this and will flag a check with no poison.
And its sibling: **reading the source is not verification.** Three times in one session a
check agreed with the implementation and the screen disagreed.

If you are a cloud session you cannot look at the screen. See `CLAUDE.md` §3 — ship the
work, be explicit that visual properties are unverified, and hand Stewart the artifact.

---

## 5. Traps that have already cost real time

1. **The ~1MB GitHub API read cap.** `data/the-program.json` (6.9MB), `data/l0-model.json`
   (5.7MB) and `dist/the-program.html` (13MB) are tracked, pushed, present — and read as
   **absent** over the API. Claude Design correctly refused to reproduce figures it could
   not read, and was right to. Hand out `data/design-extract.json` (285KB) instead.
2. **Degree means distinct neighbours, not edge instances.** 94 node pairs carry more than
   one hand-written edge. Counting instances published "107 L0 nodes" when the answer was
   96, and cost a session to unpick.
3. **Three spaces in the repo path.** A file URL percent-encodes them, so
   `new URL(...).pathname` yields `Missing%20individuals...` and every read ENOENTs on a
   path that plainly exists. Use `fileURLToPath`.
4. **`build_dashboard.py` patches a file it does not own.** It applies ~30 named string
   patches to `ref/the-vanishing-v2.html`. Patches are scoped to the code region from
   `explainEdge` onward, so **a patch targeting markup above that point silently finds
   zero occurrences**. That is exactly how the analyst placeholder fix failed first time.
5. **A global rename runs over the whole file.** Writing the sibling board's title in a
   comment gets it rewritten into nonsense. It happened, in a comment explaining the
   rename.
6. **Two agents agreeing is not corroboration when they share a method.** Two research
   passes both "corrected" a statutory citation that was already right.

---

## 6. YOUR FIRST TASK — propose a phase plan

Read the repo, run the snapshot, then come back with a proposed plan for the next few
phases. **Do not start building.** Stewart wants to see the shape before you commit to it.

### What the plan must cover

`CLAUDE.md` §9 carries a nine-item priority queue. It is a *list*, not a plan — it has no
sequencing argument, no sizing, and no view about what depends on what. Turn it into
phases, and feel free to disagree with its order if you can say why.

The known work, unsequenced:

- **The remaining inherited surfaces.** The COVER-UP view still carries the sibling board's
  skeptical record. Two such surfaces were found on 24 August *by accident*, while looking
  for something else. Nobody has swept for the rest. Candidates: the system prompt, the
  report view, insight strings, empty states, chart captions.
- **Design's packed-cell layout and edge budget.** Specified in full, unbuilt. `mountL0` is
  ours end to end, so this is a direct build.
- **Design's nine checks** from §5 of their response, each self-tested.
- **Highlights sign-off** — a table for Stewart, 2 slots spare of 16.
- **The image sourcing pass** — federal works are strongest (17 U.S.C. 105) but must trace
  to a `.gov` original, not an aggregator. Witnesses default to the class letter.
- **`notes/REQUEST-QUEUE.md`** — 35 logged actions plus the FOIA queue.
- **`TESTING-CHECKLIST.md` §12 source spot-checks** — never started. 25 ad-hoc spot-checks
  found zero fabricated sources; the systematic pass is outstanding.

### What a good plan looks like here

- **Phases with a stated goal**, not a list of tickets. What is true at the end that is not
  true now.
- **Sequencing argument.** What must come first and why. Some of this is genuinely
  ordered — a systematic sweep for inherited content should probably precede building new
  surfaces on top of it — and some is not.
- **A sizing estimate you are willing to be wrong about**, with what would make it wrong.
- **Explicitly name what you would NOT do**, and why. This project has more possible work
  than value in doing it.
- **Say what needs Stewart's decision** rather than deciding it. Editorial calls, anything
  touching the credibility rules, and anything that changes what the board claims.
- **Flag anything you cannot verify from a cloud session**, so it can be routed to a local
  session or to Stewart.

**Phase zero is now most likely the branch merge**, not the inherited-surface sweep. Nearly
every estimate below is affected by whether that branch is in or out, so resolving it first
removes an unknown from everything else. Say so explicitly if you agree, and argue it if
you do not.

### Two questions worth answering in the plan

1. **Is the inherited-surface problem bounded?** Nobody has established how much of this
   shell is answering about the wrong project. Until someone does, every estimate in every
   other phase has an unknown attached. Consider whether a scoped audit should be phase
   zero — and if you think not, say why.
2. **What is this board actually for next?** It is a working research instrument now. The
   original intent was that an analyst agent could mine it for novel connections, and one
   pass has been run (`notes/ANALYST-PASS-2026-08-14.md`, seven finds). Whether the next
   phases serve *readers*, serve *the analyst*, or harden *the record* is a genuine fork
   and Stewart has not been asked to choose.

### How to deliver it

Write it to `notes/PHASE-PLAN-<date>.md`, and give Stewart a short version in chat —
clamped, per `CLAUDE.md` §4. Tables over prose. He will tell you which phase to start.

---

## 7. Working with Stewart

Covered in `CLAUDE.md` §4; the two most easily forgotten:

- **Adversarial review is opt-in.** When something is finished, ask *"Do you want to run
  adversarial review audit?"* and then wait. It burns context and he wants it on his call.
- **Clamp responses.** What you did, why, what you need. Detail belongs in a repo note.

He is technical, direct, and reads carefully. He will catch a claim you cannot support, and
he would rather hear that something is unverified than be told it is fine.
