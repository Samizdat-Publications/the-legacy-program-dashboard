# Design brief — the surface nobody designed

**For:** Claude Design
**From:** the implementation session, 26 August 2026
**Repo:** `Samizdat-Publications/the-legacy-program-dashboard` (private, you have read access)
**Attach:** `data/design-extract.json` (285KB). **Do not try to read `data/the-program.json`,
`data/l0-model.json` or `dist/the-program.html`** — all three are over GitHub's ~1MB API read
cap and come back as ABSENT, which has cost this project two sessions already.

---

## 0. Your packed-cell layout is built, and everything you specified is in

Batches shipped 25 and 26 August. All seventeen of your named checks now exist, plus five
this build added. The gate is 42 verify checks, 40 audit re-derivations, 26 runtime
assertions and 18 canvas assertions, each demonstrated rejecting the input it must reject.

Three of your answers changed what we built, and all three were right:

- **Denial in three states.** We had switched the arrowhead off entirely after finding it
  drew from `[a,b].sort()`. You said that overpays, and it did. The bar is in.
- **Class keeps the left rule, tier keeps the stroke.** You corrected your own channel
  table against the build. No change was needed.
- **The dense occupancy mode.** OVERVIEW was 110 anonymous rectangles. It is now the
  occupancy matrix, and the rendered counts match the model exactly, 110 of 110.

**One number to reconcile:** your package says 45 denial edges, the board says 47. Same 110
nodes. Your extract is a slightly older snapshot. Nothing is broken; flagging it so a figure
mismatch does not cost another session.

---

## 1. What changed on our end, and why it matters to you

The board is moving off the single self-contained HTML file onto Cloudflare Pages, with a
Worker. Three things follow:

| | |
|---|---|
| **Payload can be split** | The map's 110 nodes can load first and the full 956-node board on demand. First paint stops being a 13MB parse. |
| **Deep links become real** | `/node/aawsap` and `/path/money` become addresses that can be sent to one person. |
| **The analyst can be live** | It currently runs fifteen scripted branches behind "no API key configured". A Worker holding the key makes it answer for real. |

**What did NOT change: the 1MB read cap.** Keep publishing a model under it, and keep
briefing off `design-extract.json`. That constraint is about how you read the repo, not
about how the board ships.

---

## 2. THE ASK: the FULL GRAPH view, which has never been designed for this board

This is the real reason for the brief.

The board has **two renderers**. `mountL0` is yours, specified end to end. The other is
`mountNetwork`, **inherited verbatim from the sibling project The Vanishing**, and it is
what a reader gets whenever `S.path` or `S.frame` is set — that is, whenever they open one
of the six entry paths, focus a cluster, trace a path between two nodes, or click through
from an insight. It is not a rare fallback. It is where the curated entry paths land.

Nobody has ever designed it for this subject. It is running another project's visual
language over this project's data, and last night it was still doing something you had
explicitly rejected in writing:

> **It drew a travelling particle on every visible edge, with the direction flipped by
> `new Date(source.date) > new Date(target.date)`.**

A time-direction flow on every line. Your §Motion says: *"It states that the relationship
runs from the earlier node to the later one, and for most of these edges the board makes no
such claim. A moving dot is a far stronger implication than a static line."* We fixed it to
your rule — a particle only on the selected node's own edges, running away from the end the
reader is standing on — but the fix was a patch on someone else's design, not a design.

**What we need:** the full-graph view specified the way you specified the packed map.
Concretely:

1. **What is this view FOR, given the packed map exists?** The map answers "where does this
   sit". What question does the graph answer that the grid cannot? If the answer is "none,
   and it should be retired", that is a legitimate finding and we would act on it.
2. **Channel assignment**, same discipline as your §3 table: what carries position, what
   carries colour, what carries motion, and what may never carry anything. It currently
   inherits a force layout, bundled edges and cluster tints from a different project.
3. **How it relates to the packed map.** Does a reader move between them, and does anything
   survive the transition? Today it is a hard swap with no shared vocabulary.
4. **Node count.** 956 nodes against the map's 110. Your one-chip-size rule and your edge
   budget both assumed 110. Neither obviously survives 956.

---

## 3. SECOND ASK: the entry surface question you could not settle

From your §6, verbatim:

> *"With six curated paths returning 7 to 38 nodes each, the honest default may be no map at
> all until a path is chosen — in which case this budget is what the map falls back to when a
> path is cleared, not what a stranger meets first. That is a product call."*

You could not settle it because there was no way to arrive at a path directly. **With deep
links there is.** `/path/money` becomes something a reader lands on without ever meeting the
entry surface. That changes the question from abstract to concrete:

- If every path is addressable, is the entry surface still the front door, or is it one of
  several equal entrances?
- What does a reader who arrives at `/node/aawsap` cold see — the map centred on it, the
  dossier, or something else?
- Does the map still need a rest state that a stranger meets first?

---

## 4. THIRD ASK, only if it interests you: the analyst

Your §7 lists the analyst bar as *not in scope, not touched*. It has been fifteen scripted
branches ever since. If the Worker lands, it becomes a real analyst with the whole board in
context.

That is a genuine design surface nobody has looked at: what an analyst that can actually
answer should be able to do on a board whose entire premise is graded evidence. The obvious
risk is that it launders Tier 3 inference into confident prose, which is the one thing this
board exists not to do. Take it or leave it.

---

## 5. What has not changed, and please keep holding us to it

- **No invented sources, URLs, document numbers or quotes.** Anywhere, including mockup copy
  and placeholder data.
- **Size never encodes importance.** The largest node would be AARO, which this board treats
  as implicated rather than authoritative.
- **Every check demonstrated rejecting the input it must reject.** Your "must reject" column
  is the most useful thing in your packages; keep writing it.
- **Every figure you publish reproducible by a generator you ship**, run against a file that
  exists in the repo.
