# Adjudicating all 174 denials, and the three places the verdict nearly stopped

26 August 2026.

## The rule, fixed before reading anything

Set first so it could not be bent to fit a case:

| verdict | test |
|---|---|
| **directed** | the label names, or unambiguously identifies, the party that issued the denial, **and** that party is one of the edge's two ends. `denier` is that end. |
| **association** | not a denial *act*: a transmission, a naming, a structural or definitional relation, a scholarly dispute, a criticism *of* a denial. |
| **undirected** | a denial act whose issuer is not named, or is not one of the two ends. Claims the least, and every arguable reading went here rather than to a guessed direction. |

## The result

**174 read one at a time. 124 directed · 36 association · 14 undirected.**

Of the 124 directed, **90 are issued by the `a` end and 34 by the `b` end.**

The shipped convention was *"`a` issued it, `b` is the subject"*, recorded in `build_l0.py`
as **"CONFIRMED against the merged board"** on the strength of one agreeing sample. **It was
wrong on 34 of 124 — 27 per cent.**

On the 47 edges drawn on the map: 22 `a`, 16 `b`, 5 undirected, 4 association.

Nothing here adds a fact. Every verdict is a reading of the label and note already on the
edge; no new party, date or document is named. `data/denial-adjudication.json` is the record
and `merge.py` stamps it onto the board.

## What the ledgers say now

| node | issued | received |
|---|---|---|
| AARO Historical Record, Vol I | **15** | 1 |
| United States Department of Defense | 12 | 1 |
| National Archives UAP Collection | 0 | **7** |
| AARO FY2025 Annual Report | 6 | 0 |
| Immaculate Constellation, 2024 | 0 | 6 |

Those read true, and they are the argument: Volume I is the single largest issuer of
denials on this board, and the National Archives collection is the largest *recipient* —
seven agencies that produced nothing for the first statutory transfer.

## Three places the verdict nearly stopped, none of which any check would have caught

**1. The aggregation only knew one state.** `denialKind` returned `'association'` or `null`,
so an edge with a known issuer arrived with `denialKind: null` and `denier` set beside it —
the pair contradicting itself, and the renderer reading the null as "not adjudicated yet".
Also, `association` links carry no denier by definition, so counting them in
`every(e => e.denier)` vetoed directions that every real denial act in the bundle agreed on.

**2. `merge_packed` never carried the fields to the page.** The verdicts reached
`data/l0-layout-model.json` and stopped. The page reads `model["directEdges"]`, built by
`build_l0.py`, which carries `a, b, n, tier, types` and nothing else. So the renderer read
`e.denialKind` and got `undefined` for all 47, and **every denial on the map drew as
undirected** — the bar. That is a quieter failure than the wrong arrowheads it replaced: it
looks exactly like an adjudication that was simply cautious, rather than one that never
arrived.

**3. Two checks were written against the old state of the data, not the rule.**
`a denial that is not a directed act carries no denial styling` asserted `denialKind` was
only ever `'association'` or absent — true while association was the only verdict anyone had
recorded, and false the moment the other two existed. And the backfill-queue check carried a
**hardcoded list of six field names asserted to be missing**, so retiring the rows for fields
that had just been supplied made it go red on the work it exists to protect.

Both now assert the rule instead: the vocabulary and its internal consistency (a `directed`
edge must name a denier and that denier must be one of its own ends; an `undirected` or
`association` edge must not), and the withheld-field set is **measured** rather than listed.

**A check that hardcodes the state of the data rather than the rule about it has an expiry
date.** So does its poison: the queue check's poison dropped the `denialKind` row, and when
the denials were adjudicated, dropping that row became the *correct* state and the poison
silently stopped poisoning. Re-aimed at `photo`, which the register keeps deliberately empty.

## And a render check, with its limits stated

`denial-marks-follow-the-adjudication`: **27 denial marks drawn, 3 once every edge is told it
is an association.** The differential is the check — a renderer not reading `denialKind`
cannot pass both halves.

It counts draw calls rather than pixels, which is a step down from everything else in that
file and is worth naming. An arrowhead is a ~7px triangle at fit scale, the map redraws
continuously, and the denial red is also the absent-link cross colour, so a whole-canvas
colour count was dominated by crosses and never moved: instrumenting `ctx.fill` showed 1188
denial-coloured fills arriving while the pixel count sat at 25 and called the layer dead.

**What it proves is that the renderer emitted the marks and that the adjudication drives
them. It does not prove they are visible or correctly placed** — the screenshots and
`pointers-offset` carry that. Said here so nobody reads more into it than it supports.
