# THE PROGRAM

**A companion board to *The Vanishing*.** Same engine, same schema, same design system,
different subject: the legacy UAP recovery and reverse-engineering program, and the modern
disclosure movement. 1940s through August 2026.

**Started:** 12 August 2026, in a Cowork cloud session
**Owner:** Stewart
**Repo:** `Samizdat-Publications/the-legacy-program-dashboard` (private), branch `master`.
Its own repository since 13 August 2026. It no longer sits inside `the-vanishing`.

> **This file is historical.** It records how the project started. For current state,
> rules and priorities read `CLAUDE.md`, which is authoritative where the two disagree.

---

## State as it stood on 13 August 2026

**These figures are a snapshot, not a status.** They are kept because this file
records how the project started, and they were accurate when written. They are not
accurate now and are not maintained. For current state run:

```
python3 tools/state_snapshot.py
```

which derives every figure from source. Nothing in this table should be quoted
anywhere, and a check that disagrees with it is right.

| | as of 13 Aug 2026 |
|---|---|
| Nodes | **976** |
| People | 251 |
| Documents | 198 |
| Institutions | 162 |
| Locations | 102 (76 with coordinates) |
| Events | 75 |
| Programs | 68 |
| Legislation | 60 |
| Research domains | 60 |
| Hand-written sourced edges | **1,788** |
| Graded claims | **4,037** — T1 2,391 · T2 1,147 · T3 499 |
| Timeline entries | **857** across 4 strands |
| Unique source URLs | **954** |
| Dangling references | **0** |

Tier distribution as of 13 August 2026: **A 146 · B 341 · C 488** (15 / 35 / 50).

---

## Editorial stance

*The Vanishing* holds a case open and lets a prosaic explanation stand where it holds.
**This board does not.**

It is built from the premise that a legacy recovery and reverse-engineering program exists,
has existed since the 1940s, and has been deliberately concealed from Congress and the
public. The research question is not *whether* — it is **who, where, under what authority,
and paid for how.**

No balanced both-sides prose. No skeptical disclaimers appended to entries.

Official denials **are** recorded, in full and sourced — as **artifacts of the concealment
effort**, not as counterweights. A denial is a dated, signed, attributable statement by a
named party, which makes it evidence about the denier and about the shape of what is being
denied. That is what the `denial` edge type and THE COVER-UP view exist for. 172 denials are
on the board.

### The line that does not move

**No invented sources. No invented URLs. No invented document numbers. No invented quotes.**

Unsourceable material goes in `unverified[]` or becomes a Tier 3 inference with the
reasoning stated. `tools/merge.py` runs an automatic honesty pass on every build: any Tier 1
claim whose node carries no primary-record URL, or which is cited to an encyclopedia, video
or blog, is demoted to Tier 2 and flagged in place. **207 claims are currently demoted**, all
logged in `tools/DEMOTIONS.json`.

The demotion re-runs on every merge, so a claim cannot be promoted back to Tier 1 without a
real primary URL being added to the node — the promotion would simply be reversed.

### A correction, logged in full — read this as the worked example

On 12 August 2026 a re-sourcing agent ran a full-text search of the AARO Historical Record
Report Volume I looking for **YANKEE BLUE** — the alleged Air Force programme that briefed
its own officers into a fake UFO recovery effort. **The term does not appear in it**, nor in
the FY2023, FY2024 or FY2025 annual reports. Two FOIA cases (OSD 25-F-3514 and AFOSI
2025-06002-F) returned no responsive records.

This board had asserted the opposite, repeatedly, and treated it as the strongest documented
item in the coverup strand. It was wrong. The node is now Tier B, the allegation is graded
Tier 3, and the negative FOIA findings are graded Tier 1 — because a negative primary finding
is itself a documented fact and belongs on a board about concealment. It is a finding about
the *absence* of a record, not a record.

`research/_corrections.json` is an authoritative overlay that beats the merge's normal
"longest prose wins" rule, precisely so a correction can never be silently outvoted by the
older, wronger text. **When something on this board turns out not to survive a check, that is
where it goes.**

**The tiers are ammunition grading, not hedging.** Tier 1 is what survives a hostile audit.
Tier 3 is where the research goes next. Keeping them separate is what makes the board usable
against a skeptic rather than dismissible by one.

---

## The scoring model

Three axes, 0–3, **never summed**. An entity can sit at the centre of the custody chain and
be entirely absent from the disclosure fight; collapsing that into one number destroys the
information.

| Axis | Question |
|---|---|
| **C** Custody proximity | How close is this entity to alleged possession of recovered material or craft? |
| **A** Access level | What special access — SAP, USAP, or waived unacknowledged — did it hold? |
| **D** Disclosure role | How central is it to forcing the record into the open? |

### Entity tiers

| | Meaning |
|---|---|
| **A** | Named in sworn testimony or primary documents as directly inside the program |
| **B** | Documented channel and capability; program role indicated but not yet nailed to a primary source |
| **C** | Contextual — real and relevant, no direct program linkage on the record yet |

Tiers are assigned globally by `tools/regrade.py`, against a composite of degree,
program-type edge count, **denial count** (an entity a government body bothered to deny
scores *higher* on this board — the stance encoded as arithmetic), claim weight and the three
axes. Any node with no sourced URL has its score cut by 65%, so nothing unsourced can hold
Tier A. Every graded node carries a rationale showing its rank and inputs.

The first pass by the research agents produced **553 of 911 nodes at Tier A** — 61%, which
made the badge meaningless. Fourteen agents each graded within their own domain, where their
subject genuinely was central, and nobody graded across the whole board. The global re-grade
fixed it to 15/35/50.

### Claim tiers

Carried over from the parent board unchanged: **1** documented · **2** sourced claim ·
**3** inference.

---

## How it differs from The Vanishing

| | The Vanishing | The Program |
|---|---|---|
| Axes | S sequence · P program proximity · I institutional channel | **C** custody · **A** access · **D** disclosure |
| Clusters | 4 geographic | **9 functional** — legacy · contractor · ffrdc · ic · oversight · witness · research · media · other |
| Strands | cases · oversight · skeptical | **program · witness · oversight · coverup** |
| Edge types | 8 | **12** — added custody, funding, denial, legislative |
| Node classes | 5 | **8** — added legislation, document, event |
| Eighth view | COUNTERARGUMENTS | **THE COVER-UP** |

Unchanged and preserved: the `P_()` / `other()` / `E()` helpers, the numeric claim tiers,
`{name, url, date}` source records, `chronology[]` with `precision`, the `ENTITY_INFO` /
`ENTITY_SOURCES` side tables, and the rule that **derived edges come from rules while program
edges are hand-written and sourced**.

Full spec: `SCHEMA.md`.

---

## How the dashboard is built

`dist/the-program.html` is not written by hand. `tools/build_dashboard.py` reads
`the-vanishing-v2.html`, splices in this board's data, and applies ~30 named patches.
The CSS, the four-row shell, the canvas renderer, the dossier dock, the analyst and every
view function carry over byte for byte.

Every patch fails **loudly by name** if its anchor moves. That is deliberate: when the parent
board is updated, re-running the build tells you exactly what diverged.

```bash
python3 tools/merge.py             # research/*.json -> data/*
python3 tools/regrade.py           # tiers, dates, coordinates -> research/_remediation.json
python3 tools/merge.py             # re-merge so the overlay lands
python3 tools/build_dashboard.py   # -> dist/the-program.html
node   tools/shoot.js              # render, capture errors, screenshot all 8 views
```

### What scale broke, and what was done

1. **Force layout** — 928 nodes × 900 pre-paint steps was ~387M operations. Replaced with a
   **Barnes–Hut quadtree** at θ=0.9; same force law and constants, ~45× fewer evaluations.
2. **Derived edges** — the parent board's rules generated **18,491** at this scale, burying
   the 1,788 hand-written ones. Added **cardinality gates**: an attribute only generates
   pairwise edges while its membership stays small. Two people sharing a niche specialism is
   a finding; 95 people sharing "oversight" is noise.
3. **Plate density** — 251 plates would tile 89% of the canvas. **Semantic zoom**: a plate is
   earned at degree ≥5 of hand-written links (~46, against the original's 52). Everything
   else is a dot that promotes on selection.
4. **The render path** — the parent file contains **two map implementations**. The legacy one
   (`drawEdgesCircuit`, the older `mountMap`) is dead code at runtime; the live one funnels
   every edge through `edgeInstances()`. Patching the wrong one cost a full build cycle.
5. **Labels** — the parent board's entity names were `LANL`. These are
   `OFFICE OF THE DIRECTOR OF NATIONAL INTELLIGENCE`. Truncated on canvas only.

---

## How the research was done

Two waves of parallel agents, then a remediation pass.

**Wave 1 — 14 domains:** grusch · elizondo-ttsa · aawsap-aatip · uaptf-aaro · ffrdcs ·
primes-custody · congress-house · congress-senate-legislation · history-1940s-1960s ·
history-1970s-2000s · releases-2023-2026 · media-structure · aviators-incidents ·
scientists-technical.

**Wave 2 — 8 tasks**, aimed at what a completeness critic found wave 1 had missed:
agencies · places-events · **sap-architecture** · **black-budget** · international ·
retrieval-literature · taxonomy · 2025-2026.

The SAP/USAP architecture domain is the spine: 10 U.S.C. §119 including the subsection (e)
waiver language, DoDD/DoDM 5205.07, the Gang of Eight notification convention, DoD SAPCO, and
the NISPOM carve-out that lets a contractor SAP escape normal DCSA oversight. Unlike the
claims themselves, the *mechanism* is fully documentable from statute — which is what lets
the board argue **how**, not merely assert **that**.

**Wave 3A — remediation:** global tier re-grade, ID normalisation, 34 recovered dates,
76 location coordinates, and six agents re-sourcing demoted claims from constructable
primary URLs (congress.gov, govinfo.gov, esd.whs.mil, law.cornell.edu, the Wayback
availability API).

Full history: `notes/RESEARCH_LOG.md`. Next steps: `notes/WAVE3_QUEUE.md`, which ends with
**115 verbatim gap reports** from the wave-2 researchers — named FOIA targets and specific
archives, not vague suggestions.

---

## Standing instructions

**Adversarial review.** At the end of each deliverable that feels final, ask
*"Do you want to run adversarial review audit?"* Do not run it unprompted. When Stewart says
yes, act as his managers — the management this gets turned in to — and pick apart anything
that looks wrong, doesn't make sense at first glance, or is visually broken. Actually look at
the output.

**Cross-board reconciliation, open question.** `william-mccasland`, `david-grusch` and
`pursue-releases` now exist on both boards. If the two share an id space this becomes one
graph with two views, which is considerably more powerful than two graphs. Stewart's call.
