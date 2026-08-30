# Brief for Claude Design — 30 August 2026

**We reversed one of your decisions and we want you to look at the result.**

You specified the packed-cell program map and we built it, with 31 canvas assertions behind
it. It is no longer the board's primary map. This brief says what changed, why, what we did
NOT decide without you, and the four questions worth your time.

---

## 0. Read these, in this order, and not the other three

| | |
|---|---|
| `CLAUDE.md` | the authoritative entry point. §2 is the rule that never bends |
| `data/design-extract.json` | 285KB, purpose-built for you |
| `notes/MAP-INVERSION-2026-08-29.md` | what changed and why. §9 is addressed to you |
| `notes/shots/2026-08-30/` | five captures at 1920×1080, `deviceScaleFactor: 1` |

**Trap #7, and it has bitten twice.** `data/the-program.json` (7.5MB),
`data/l0-model.json` (5.9MB) and `dist/the-program.html` (15.6MB) are tracked and pushed,
and **they read as ABSENT over the GitHub API** because of its ~1MB cap. They are not
missing. Cite `data/design-extract.json` and `data/l0-layout-model.json` (461KB) instead.

---

## 1. What changed

Stewart, after using the live board:

> "I clicked on grusch or someone and instead of our orthogonal map it gave me this which is
> I think the style from the vanishing. I actually think I like this better ... it shows the
> connections better than the orthogonal one which I like but **when a subject is clicked you
> can't see all the connections like you can here**"
>
> "Maybe the orthogonal map becomes its own tab that's just the whole map so you can see it
> while our primary map is in the style in the screenshots below"

So the two renderers **swapped roles**. Neither was deleted.

| | before | after |
|---|---|---|
| `NETWORK` "Network map" | your packed map at rest; the force-directed graph only while a path or frame was live | the force-directed full graph, always, all 964 nodes |
| `PROGRAM` "Program map" | did not exist | your packed cells, 110 nodes, its own tab, always the whole map |

**One thing worth knowing before you judge the decision.** He hit that fallback *by accident*,
and the reason he could not see connections was a bug, not a property of your layout:
`selectNode` forced the NETWORK view and then did **not** swap the renderer, because
`renderSurface` refuses to re-mount the map while it is already current. So every command
that framed or pathed — `highlightPath`, `focusCluster`, `frameNodes`, "Show me on the map" —
worked from every view *except* the one it targeted. That is fixed independently of the
inversion.

**We are telling you this because it means the comparison he made was not quite the one he
thought he was making.** He compared your map with a selection that could not light up
against a force graph that could. That does not make his preference wrong — he has used both
and we are not relitigating his call — but the underlying defect is gone now, and that is a
fact you should have when you answer question 1.

## 2. What we did NOT decide without you

**A bridge between the two maps.** With a node selected on the program map, a control reading
something like "see connections" that switches to the network map framed on that node is the
literal shape of his complaint. It is four lines. We did not build it, because it is an
addition to your spec and this file's own docstring records having made exactly that mistake
once before. It is question 2.

## 3. The four questions

**1. Does the packed map want re-shaping now that it is a destination rather than a rest
state?** It was designed as the thing you land on. It is now the thing you go to, deliberately,
having already seen the network map. Different job, possibly different opening state. It
currently opens fitted at 0.59× at 1920 — see `notes/shots/2026-08-30/2-program-map.png`.

**2. The bridge in §2 — build it, and in which direction?** Program map → network map framed
on the selection is the obvious one. The reverse (network map → "show this in the programme")
may matter more and is not obviously the same control.

**3. Your motion rule now governs the default surface.** You named and rejected the inherited
particle treatment: *"It states that the relationship runs from the earlier node to the later
one, and for most of these edges the board makes no such claim. A moving dot is a far stronger
implication than a static line."* The fix draws a particle **only on the selected node's edges,
running away from the reader**, never along the time axis. That governed a fallback almost
nobody reached. It now governs the first thing every reader sees. Consequence: **at rest, with
nothing selected, the primary map is completely static.** Two gate checks hold that line. Is
that still the right answer when it is the default, or does the primary surface want something
you have not specified yet?

**4. The one we would most want you on: label density on the full graph.** 964 nodes at rest,
and in the centre the labels overlap heavily — `notes/shots/2026-08-30/1-network-map.png`.
That was inherited from The Vanishing and was tolerable for a fallback. As the primary surface
it may not be. We have not touched it, because "make the labels better" is a design problem
and we would rather have your answer than our guess.

## 4. What is not on the table

- **The rule in `CLAUDE.md` §2.** No invented sources, URLs, document numbers or quotes,
  including in mockup copy and placeholder text. If you need a placeholder, mark it
  unmistakably as one.
- **Size as a channel.** Size must never encode importance anywhere in the visual language.
  The largest node would be AARO, which this board treats as implicated, not authoritative.
  Position is available; size is not.
- **The two grading systems.** Claim tiers 1–3 are evidence strength (1 strongest). Node tiers
  A/B/C are proximity to the programme, not credibility. They share three colours, which is a
  known weakness in the design and one you may reopen if you want to.
- **`test_packed_layout.js`.** 31 canvas assertions guarding your spec. It reads pixels with
  `getImageData` and it found two defects on the day it was written that reading the source
  did not. Anything you specify has to survive it, or has to change it deliberately.

## 5. Two other surfaces exist now, and neither needs you

Mentioned only so you are not surprised by the rail going from eight items to ten.

- **PATENTS.** Stewart signed off a mockup and we built to it.
  `notes/PATENTS-TAB-BUILD-2026-08-29.md`.
- **The FOIA layer.** An open question in a dossier now names the request that would close it.
  `notes/FOIA-LAYER-2026-08-29.md`. **If anything here wants your eye it is this**, and only
  as a question: 17 requests already map to 121 open questions across 42 nodes, and right now
  that only shows as a chip on a question. Whether the request queue deserves a surface of its
  own is genuinely open, and we have not designed one.
