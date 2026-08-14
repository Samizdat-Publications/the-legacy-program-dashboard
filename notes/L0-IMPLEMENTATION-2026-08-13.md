# L0 program map — implementation record, 13 August 2026

Implements the Claude Design handoff `design_handoff_l0_program_map`. Read alongside
its `SPEC.md`. This file records what was built, what was corrected, and what is
still open.

Gate at time of writing: **15 checks pass, including `--self-test` and
`--idempotent`.** Two consecutive full builds are byte-identical.

---

## 1. The correction: the floor produces 96 nodes, not 107

The handoff's figures do not reproduce. Running its own reference generator,
`build-l0-data.mjs`, against the source it names, `data/l0-extract.json` at `9ccc25d`:

| Figure | FIGURES.md | Generator output |
|---|---|---|
| L0 nodes | 107 | **96** |
| Ledger | 695 | 706 |
| Direct edges | 191 | 170 |
| Summarised edges | 82 | 76 |
| Primitives | 380 | 342 |
| Path only / Unattached | 55 / 113 | 55 / 113 |

**Cause.** The extract's `deg` field is an edge-instance count, not a degree. 94 of
the 1,685 node pairs carry more than one hand-written edge, up to three, so those
nodes are counted two and three times toward the floor. The published figures used
that field. The generator itself does not: line 60 recomputes degree from a set of
distinct neighbours, and carries the comment *"Degree is recomputed rather than
trusted — a stale `deg` field silently changes the L0 set."* It did exactly that.

**Resolution: distinct neighbours.** Accepted by Stewart on 13 Aug. The renderer
settles it — patch P2 aggregates every hand-written edge on a pair into one drawn
line, so a map that draws a pair once cannot let that pair count three times toward
a *connectivity* floor.

**Eleven nodes leave the map:** `atic`, `cfr-32-117`, `dhs`, `dodd-5205-07-2010`,
`dodig-2023-109`, `eo-13526`, `icd-906`, `oak-ridge-national-laboratory`,
`uap-nda-waiver-directive-2026`, `usaf`, `uss-princeton`.

**Downstream corrections to the handoff's prose**, which should be applied there
rather than only here:

- Class composition is institution 32 · document 23 · program 21 · event 12 ·
  legislation 8.
- The "three inert nodes" become **one**: `ndaa-fy2023-sec-6802`. `usaf` and
  `blue-book-special-report-14` are no longer on the map. The README uses `usaf`
  as its worked example of the single-member refusal; that example needs replacing.
- `aaro` carries 52 members, not 49. `pursue-releases` 29, not 27.
- Unclustered L0 nodes: 49 of 96, not 57 of 107.
- Shared-count distribution `{2:62, 3:11, 4:1, 5:2}`. Still within the five-tick
  vocabulary, so no numeral case is introduced.
- Wall-clamp measures **3.1%** in this Python bake, against the handoff's 6.5% for
  its JS bake at 107 nodes. Label overlaps at the true 68x20 box: **0**, which is
  the figure that actually matters.

## 2. Denial direction — confirmed, nothing inverts

SPEC open question 3. The convention is `a` = issuer, `b` = subject, confirmed
against the merged board rather than inferred from a sample. Representative edge:
`susan-gough -> luis-elizondo`, "no assigned responsibilities for AATIP". Issuer
totals reproduce exactly: `aaro-historical-record-vol1` 10 issued / 8 received,
`susan-gough` 8 / 0, `david-grusch` 3 issued / 7 received. The §08 argument stands
as written.

## 3. SPEC §7 — the rest state opens at 1.0, and now for a measured reason

The handoff's argument was that at 107 nodes a fitted view lands at 0.60, below the
0.62 label-drop threshold, so a fitted rest state is a field of unlabelled marks. At
96 nodes the extent shrinks to 1574x1030 and the question had to be re-asked.

Measured at runtime rather than argued: on a 1600x1000 shell the view surface is
1092x549 and **fit-zoom is 0.466**. Well below 0.62. On a 1440 shell it is lower
still. The conclusion holds with room to spare, and `mountL0` now *measures* it on
mount instead of hard-coding the decision — if a future shell makes the fit clear
the threshold, the map opens fitted on its own. `OVERVIEW` remains an explicit
control either way.

## 4. What was built

| Item | Where |
|---|---|
| P1 register partition, routing, member lists | `tools/build_l0.py` |
| P2 direct-edge aggregation per pair | `tools/build_l0.py` + `l0_patches.py` |
| P3 shared-member edges, gate >= 2 | `tools/build_l0.py` |
| P4 tier in the dash channel (D1) | `l0_patches.py` |
| P5 directional denial edges (D3) | `l0_patches.py` |
| P6 five CMD actions, each with a control | `l0_patches.py` |
| P7 member ledger | `l0_patches.py` |
| P8 the L0 bake | `tools/build_l0.py` |
| D4 marks/colours for document, event, legislation | `l0_patches.py` |
| Six verify checks, each self-tested | `tools/verify.py` |

`tools/build_l0.py` joins the documented pipeline **before** `build_dashboard.py`,
and is inside the idempotency gate, because a bake seeded from anything
non-deterministic would drift there and nowhere else.

`GOLDEN.json` gains `l0_nodes`, `l0_edges_direct`, `l0_edges_summarised`, `ledger`,
`path_only`, `unattached`. Accepted deliberately; nothing else in the manifest moved.

## 5. The self-test earned its keep again

All six new checks were **born broken and silently passing.** The fixture built each
poisoned HTML from a `good_html` that had already had a valid model appended, so
every poison carried two `L0DATA` literals and the parser read the clean one first.
Six checks reporting `ok` while asserting nothing.

That is the `canvasInk` failure exactly, reproduced in the fixture instead of the
check. It is also the third time on this board that roughly half the new checks were
dead on arrival. **Rule 2 is not optional and the rate is not improving.**

A seventh defect surfaced the same way: `UI copy agrees with the register counts`
originally matched a string literal that my own rail patch did not emit. It now
asserts something worth asserting — that both register controls exist and that their
counts are derived from `L0DATA.counts` rather than typed.

## 6. Additions to the spec, needing sign-off

**Full-graph fallback.** The handoff specifies the NETWORK *rest state* and does not
say what becomes of the inherited commands that operate on the full graph:
`setHops`, `highlightPath`, `focusCluster`, `frameNodes`, and the insight callout's
"Show me on the map". Replacing the surface outright breaks all five silently. So L0
owns the rest state, and the legacy full-graph map mounts in its place while a path
or a frame is active, with a `FULL GRAPH` breadcrumb chip and `CLEAR` returning to
L0. `selectNode` deliberately does **not** trigger the swap: the ledger is a table of
contents for the dock, and opening the dock must not move the map.

This is an addition, not an implementation of the spec. It is the only place I
invented behaviour rather than following it.

**Legacy chrome suppressed.** `renderNetworkChrome` returns early under L0. Its
`INSIGHTS()` reads `MAP.pairs`, which the L0 map does not have; unguarded it threw
inside `paint()`, and because `paint` catches per surface, the ledger and the
register panel simply never appeared while the console stayed quiet. Found at
runtime, not by reading the diff.

## 7. Still open

1. **`dird-series` is the third-largest node at 32 members, all documents.** A
   filing convention for the DIRD papers, not a claim about the program. The design's
   recommendation on file is to promote named documents individually. Unchanged.
2. **D4 marks and colours** still need sign-off. `document` is `#f0d264`.
3. **D2 is a rule bent, not met.** The class ledger bar carries its mix in hue alone.
   The tooltip names every segment; that mitigates, it does not comply.
4. **The stats strip still reads CONFIDENCE KEY.** The handoff's shell spec calls for
   the claim-tier key. Not implemented; one line, deferred rather than guessed.
5. **`FIGURES.md`, `SPEC.md`, `l0-data.js` and the prototype all still encode 107.**
   They should be regenerated by the design session rather than hand-patched here.

---

# Stage 2 — entity dossiers and selection, 14 August 2026

Stewart's review of the first build overrode three things the handoff specified.
The overrides are right and are now implemented.

## Entity dossiers — the new primary content

25 L0 nodes, **345 sourced claims**, researched and written this session by four
parallel agents against live sources. Clicking MITRE now gives you the argument for
why MITRE is on the map, with the member ledger underneath it as a table of
contents. That inverts the handoff's emphasis, on purpose: the argument is the
product.

Shape per entity: `whatItIs`, `whyImplicated` (the load-bearing paragraph),
`roles`, a 700-1100 word narrative, tiered claims with sources, `denialPosture`,
and `openQuestions`.

They live in `research/dossiers/` as a **parallel dataset**, not merged into the
board's nodes. Two reasons. `merge.py` globs `research/*.json` and expects node
documents, so they broke the pipeline where they were. More importantly, merging
345 claims onto 25 nodes would move every claim count, tier mix and GOLDEN entry,
and it would conflate two different objects: a node claim is a fact about the
entity, an entity dossier is the argument for why the entity is on this map.

**Research honesty, carried through rather than smoothed over.** The agents flagged
their own thin spots instead of writing around them:

- `cia` is Tier 1 on Robertson Panel and U-2 material and Tier 3 on anything modern;
  the retrieval allegation rests on one reporter with no document.
- `yankee-blue` rests on a paywalled WSJ piece that could not be fetched. What is
  Tier 1 there is entirely negative-finding material: the OSD no-records
  determination, Gough's 1 Oct 2025 non-confirmation, the 12 Dec 2025 appellate
  remand. The AFOSI case number is explicitly marked not independently verified.
- `uap-science-advisory-council` has no published charter, FACA notice or roster.
- The PURSUE executive release channel has no primary; `war.gov/ufo` would not return
  content.
- Public Law 118-31 dropping the Review Board and eminent domain is sourced to NARA's
  description, not the enrolled text, because every full-NDAA fetch truncated.

Three findings worth promoting into the board's argument: the DHS-MITRE HS SEDI
sponsoring agreement excepts §9(g)(2), the clause preserving disclosure to Congress,
for subcontractors while MITRE staff keep it; DoDD 5205.07 §3.1.g is an unclassified
standing prior-restraint on giving SAP material to any member of Congress without
DoD SAPCO approval; and the AAWSAP DD-254 was amended before award to drop the
requirement that the contractor hold a TS facility clearance prior to implementation.
One correction for the existing board: Loeb's first UAPSAC post is dated 13 June 2026,
not 29 June.

## Selection is now single and global

The handoff's additive-ledger model ("comparison is the point") failed in use: no way
to unclick, no visible exit, and a second click took you nowhere. Now one selection,
obeyed everywhere.

- Clicking a node selects it, zooms to it at >= 1.15 and opens its dossier.
- Clicking it again clears. Clicking empty canvas clears.
- `selectNode` from the timeline, a case card or a search result clears prior
  selections, lights the node on the map and moves the camera to it. Previously the
  map kept the old selection and the reader could not tell which node the dock
  described.
- Multi-open survives only on the CMD line, where an analyst who genuinely wants two
  ledgers can still ask.

## The dock reads like a document

306px is not a reading measure. On selection it animates to half the viewport,
floored at 560px, on a 260ms cubic curve. One always-present chevron collapses it.

**Two silent failures found by measuring rather than reading**, both worth recording
because they are the same class of bug this board keeps hitting:

1. Setting the width through the `--dock-w` custom property did nothing. The
   inherited resize grip already writes that property to `:root`, and two owners
   racing one custom property produced no error, no console output, and no movement.
   Fixed by setting the width on the element.
2. The open condition read `S.dockWide !== false`, and `setDockOpen` writes
   `S.dockWide`. The first paint at rest set it to `false`, which permanently
   falsified the condition that was supposed to open it. A flag that the reader sets
   and a flag the renderer sets must not be the same flag.

Both looked correct in the diff. Both were caught by asserting a measured width in
the browser.

## Still open

1. Entity dossiers exist for 25 of 96 L0 nodes. The other 71 have none, and the dock
   falls through to the inherited node dossier for them. A `verify.py` check that
   every L0 node has a dossier should wait until the rest are written, or it will
   fail by design.
2. No verify check yet asserts that every dossier claim carries a tier and a source.
   That should exist before the next research wave lands.
3. The stats strip still reads CONFIDENCE KEY where the handoff calls for the
   claim-tier key.
4. D4 marks and colours still need sign-off; D2 is still a rule bent.
