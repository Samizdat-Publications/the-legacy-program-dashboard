# Session Handoff: The Program

**Handoff date:** August 12, 2026
**From:** Cowork cloud session
**To:** Cowork local session (running on Stewart's computer)

**If you are a fresh Claude session picking this up, read this file first, then `PROJECT.md`,
then `TESTING-CHECKLIST.md` — which is your first job.**

---

## Your first job

**Do not write new research. Do not add features. Open the dashboard and use it.**

`TESTING-CHECKLIST.md` is a written QA pass. Work through it in a real browser, clicking
real things, and log what breaks. The board was built and screenshot-verified in a headless
container at two resolutions — which is not the same as a person using it, and the gap
between those two things has already produced four bugs that shipped.

Skip everything involving the **analyst** for now. Stewart does not have the API key in
place yet, and the analyst's no-key state is a first-class scripted mode that is already
working. Everything else is in scope.

Report findings as a numbered list with severity, then fix in severity order. Rebuild and
re-verify after each fix rather than batching them.

---

## Where everything lives

This project is a **companion board to The Vanishing**, and it is designed to sit inside
the same repository:

```
<repo root>/                        the-vanishing (master branch)
  the-vanishing-v2.html             THE PARENT BOARD — this is a BUILD INPUT, do not edit
  the-program/                      <- everything in this package goes here
    SESSION-HANDOFF.md              this file
    PROJECT.md                      what the board is, the stance, the state
    SCHEMA.md                       the data spec and how it extends the parent's
    TESTING-CHECKLIST.md            your first job
    CLAUDE-DESIGN-PROMPT.md         design brief, if Stewart wants a redesign pass
    dist/the-program.html           THE DASHBOARD — 6.5 MB, self-contained, open by double-click
    data/                           merged dataset: the-program.json + the JS modules
    research/                       per-domain raw research (23 files) + overlays
    tools/                          the build pipeline (see below)
    notes/                          research log, wave queues, the build plan
```

**`the-vanishing-v2.html` is the build input.** `tools/build_dashboard.py` reads it, splices
in this board's data, and applies ~30 named patches. It looks for the file in the repo root,
one level up, or `ref/`, and honours `VANISHING_SRC` as an override. If the parent board is
updated, re-run the build and every patch that no longer matches will fail loudly by name —
that is deliberate, and it is the mechanism that keeps the two boards in sync.

## Rebuilding

```bash
cd the-program
python3 tools/merge.py             # research/*.json      -> data/*
python3 tools/regrade.py           # tier re-grade, dates, coordinates -> research/_remediation.json
python3 tools/merge.py             # re-merge so the overlay lands
python3 tools/build_dashboard.py   # data + parent board  -> dist/the-program.html
node   tools/shoot.js              # render, capture console errors, screenshot all 8 views
```

`shoot.js` needs Playwright. It captures every JS error and writes a PNG per view into
`dist/shots/`. **Run it after every change.** It is the only thing standing between a patch
that "applied cleanly" and a board that actually renders.

`build_dashboard.py` prints `all patches applied` or names the ones that failed. Never ship
a build that printed a failure.

---

## What this project is

A network board mapping the legacy UAP recovery and reverse-engineering program and the
modern disclosure movement, 1940s through August 2026. It reuses The Vanishing's engine,
schema and design system with a different subject.

**Current state: 976 nodes · 1,788 hand-written sourced links · 4,037 tiered claims ·
857 timeline events · 954 unique source URLs.**

Nodes: 251 people, 198 documents, 162 institutions, 102 locations, 75 events, 68 programs,
60 legislation, 60 research domains.

## Editorial stance — read before writing anything

*The Vanishing* holds a case open and lets a prosaic explanation stand where it holds.
**This board does not.** It is built from the premise that a legacy recovery and
reverse-engineering program exists, has existed since the 1940s, and has been deliberately
concealed from Congress and the public. The research question is not *whether* — it is
**who, where, under what authority, and paid for how.**

Do not write balanced both-sides prose. Do not append skeptical disclaimers.

Official denials **are** recorded, in full and sourced — as **artifacts of the concealment
effort**, not as counterweights. A denial is a dated, signed, attributable statement, which
makes it evidence about the denier. That is what the `denial` edge type and THE COVER-UP
view exist for.

**The one thing that does not bend: no invented sources, no invented URLs, no invented
document numbers, no invented quotes.** Unsourceable material goes in `unverified[]` or
becomes a Tier 3 inference with the reasoning stated. `tools/merge.py` runs an automatic
honesty pass on every build that demotes any Tier 1 claim not backed by a primary-record
URL — 207 claims are currently demoted and logged in `tools/DEMOTIONS.json`. **A claim
cannot be promoted back to Tier 1 without adding a real primary URL to the node; the
demotion re-runs on every merge and will simply reverse you.**

## The scoring model

Three axes, 0–3, **never summed** — an entity can sit at the centre of the custody chain and
be entirely absent from the disclosure fight, and collapsing that into one number destroys
the information.

| Axis | Question |
|---|---|
| **C** Custody proximity | How close is this entity to alleged possession of recovered material or craft? |
| **A** Access level | What special access — SAP, USAP, waived unacknowledged — did it hold? |
| **D** Disclosure role | How central is it to forcing the record into the open? |

Entity tiers: **A** named in sworn testimony or primary documents as directly inside the
program · **B** documented channel and capability, role indicated · **C** contextual.
Currently 146 / 341 / 488, re-graded globally by `tools/regrade.py` against a composite of
degree, program-type edges, denial count, claim weight and the axes. Any node with no
sourced URL has its score cut by 65%, so nothing unsourced can hold Tier A.

Claim tiers (carried over from the parent board unchanged): **1** documented ·
**2** sourced claim · **3** inference.

---

## Known problems, in priority order

These are mine, found and not yet fixed. Verify each against the real browser before
trusting this list — some may be worse or better than I think.

1. **Map density in the upper-left.** The witness, oversight and IC clusters carry most of
   the Tier A nodes and they crowd. It is a legible network now rather than a mat, but it is
   not good. The next lever is a **rail slider** exposing `PLATE_DEGREE`, `LABEL_DEGREE`,
   `EDGE_MIN_DEG` and `NODE_MIN_DEG` so density is dialled by hand rather than guessed by me.
   All four are `let` bindings and `window.__board.setPlateDegree(n)` already exists.
2. **Frame rate.** Better since the budget landed, but not smooth at 976 nodes. The parent
   board's own design doc says production should not be canvas 2D for this.
3. **Analysis view** beyond the institutional-overlap chart is still partly the parent
   board's furniture. The four INSIGHTS cards are rewritten and correct; what sits under
   them needs a look.
4. **CASES view** is 251 cards with no virtualisation.
5. **Report view** has not been reviewed at all against the new data.
6. **6.5 MB single file.** Opens fine locally, parses in ~300ms, awkward over a network.
7. **27 location nodes still have no coordinates**; 76 do. Geography flags this inline.
8. **65 structural stubs** carry `desc: null` deliberately — the dock prints them as a
   stated gap. They are honest placeholders, not bugs, and they are queued in
   `notes/WAVE3_QUEUE.md`.

## Working rules

- **The parent board is a build input, never edited.** All divergence lives in
  `tools/build_dashboard.py` as named patches.
- **Patches are scoped to the code region**, not the whole file. The data block is 6 MB of
  research prose and URLs, and a literal `p.P` inside a citation once silently broke a patch
  count. `build_dashboard.py` slices at `function explainEdge` before applying vocabulary
  patches — keep that.
- **There are two map implementations in the parent file.** The legacy one
  (`drawEdgesCircuit`, the older `mountMap`) is dead code at runtime. The live one is the
  three-layer host that funnels every edge through `edgeInstances()`. **Patching the wrong
  one costs a full build cycle — it has already happened once.**
- Run `node tools/shoot.js` after every change.
- Research agents write to `research/` and will create subdirectories there. Build tooling
  lives in `tools/` deliberately — an agent deleted the build directory mid-run once.

### Adversarial review protocol (Stewart's standing instruction)

At the end of each deliverable that feels final, ask: **"Do you want to run adversarial
review audit?"** Do not run it unprompted; it burns context. When Stewart says yes, act as
his managers — the management this gets turned in to — and pick apart anything that looks
wrong, doesn't make sense at first glance, or is visually broken. Actually look at the
output. If it is a slide, check that things line up and nothing overlaps.

---

## Environment notes

- **Web search budget is 200 calls per session.** Wave 1 consumed all of it and wave 2 ran
  degraded on WebFetch alone. Raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` before
  starting any research wave.
- **The TinyFish skill is installed but its MCP server is not connected** — invoking it
  prints docs for a tool that does not exist. Ignore it.
- The cloud session's `GH_TOKEN` was scoped to pre-configured repos and returned 403 for
  `the-vanishing`. Running locally against the real checkout removes that problem entirely.
- Agent concurrency in the cloud container capped at 2, so a 14-agent wave took ~6 hours.
  Local should be better.

## Where the research goes next

`notes/WAVE3_QUEUE.md` is the authoritative pickup list and ends with **115 verbatim gap
reports** from the wave-2 researchers — named FOIA targets, specific archives, and yes/no
questions a committee could demand an answer to. The highest-value single item:

> **The Immaculate Constellation document.** Entered into the Congressional Record on
> 13 Nov 2024 and listed in the hearing's Index of Documents, but no retrievable file at a
> stable public URL. Pulling the submitted-materials section of GPO `CHRG-118hhrg57440`
> is the highest-value next move on the board.

Also standing: **`william-mccasland`, `david-grusch` and `pursue-releases` now exist on
both boards.** If the two share an id space this becomes one graph with two views, which is
considerably more powerful than two graphs. That is a decision for Stewart.
