# Brief for Claude Design — 30 August 2026

**Self-contained. You need no repo access to answer this.** Everything you need is in this
document plus five screenshots and one data file, all attached. Read this first; the data
file is for when you want to check a number.

---

## 1. What the project is

**The Program** is a research board mapping the alleged legacy UAP recovery and
reverse-engineering programme, 1944–2026. One self-contained HTML file, no server, no
runtime dependencies. Owner: Stewart.

| | |
|---|---|
| nodes | 964 — 279 people, 685 entities |
| hand-written sourced edges | 2,172 |
| tiered claims | 4,614 — Tier 1 2,855 · Tier 2 1,257 · Tier 3 502 |
| views | 10, in a left rail |
| built artifact | a single 15.6 MB HTML file |

**Two maps exist**, and you designed one of them:

- **The packed program map (yours).** 110 nodes — the subset with six or more distinct
  neighbours — laid out in your packed cells: 7 bands down by measured mean C, 5 era columns
  across, every chip at one size, 103 of 326 links drawn at rest by your own edge budget.
  Orthogonal, arranged, deliberate. `2-program-map.png`.
- **The force-directed full graph (inherited).** All 964 nodes, WebGPU, settled rather than
  arranged. Ported in from a sibling board called The Vanishing. `1-network-map.png`.

**Terms you will meet.** *C, A, D* are the three axes the board scores on. *Claim tiers 1–3*
are evidence strength, 1 strongest. *Node tiers A/B/C* are proximity to the programme, not
credibility — a Tier A node carrying only Tier 3 claims is not a contradiction, it is the
definition of where to look next. The two systems share three colours, which is a known
weakness in the design and one you may reopen.

## 2. What we changed, and why you are being asked

**Until 29 August your packed map was the board's primary surface.** It is now a secondary
tab. The force-directed full graph is primary.

Stewart's words, after using the live board:

> "I clicked on grusch or someone and instead of our orthogonal map it gave me this which is
> I think the style from the vanishing. I actually think I like this better ... it shows the
> connections better than the orthogonal one which I like but **when a subject is clicked you
> can't see all the connections like you can here**"
>
> "Maybe the orthogonal map becomes its own tab that's just the whole map so you can see it
> while our primary map is in the style in the screenshots below"

So the two renderers swapped roles. Neither was deleted. Your layout is intact, still gated
by 31 canvas assertions that read pixels out of the canvas with `getImageData`.

**One fact you should have before you answer.** He hit that force-directed view *by accident*,
and the reason he could not see connections on your map was a **bug**, not a property of your
layout. Selecting a node forced the network view and then failed to swap the renderer, because
the view refuses to re-mount a map that is already current. So every command that framed or
traced a path worked from every view *except* the one it targeted. That is fixed now,
independently of the inversion.

We are telling you this because the comparison he made was not quite the one he thought he was
making: your map with a selection that could not light up, against a force graph that could.
**That does not make his preference wrong** — he has used both, the call is his, and we are not
relitigating it. But it is a fact you should have.

## 3. What we did NOT decide without you

**A bridge between the two maps.** With a node selected on your packed map, a control reading
something like "see connections" that switches to the force graph framed on that node is the
literal shape of his complaint. It is about four lines of work. We did not build it, because
it is an addition to your spec — and the module's own documentation records having made
exactly that mistake once before, which is how this whole reversal came about. It is question 2.

## 4. The four questions

**1. Does the packed map want re-shaping now that it is a destination rather than a rest
state?** You designed it as the thing you land on. It is now the thing you go to deliberately,
having already seen the network map. Different job, possibly a different opening state. It
currently opens fitted at 0.59× on a 1920px window — `2-program-map.png`.

**2. The bridge in §3 — build it, and in which direction?** Packed map → force graph framed on
the selection is the obvious one. The reverse ("show this one in the programme") may matter
more, and is not obviously the same control.

**3. Your motion rule now governs the default surface.** You named and rejected the inherited
particle treatment: *"It states that the relationship runs from the earlier node to the later
one, and for most of these edges the board makes no such claim. A moving dot is a far stronger
implication than a static line."* The fix draws a particle **only on the selected node's edges,
running away from the reader**, never along the time axis. That governed a fallback almost
nobody reached. It now governs the first thing every reader sees. The consequence: **at rest,
with nothing selected, the primary map is completely static.** Two automated checks hold that
line. Is that still right when it is the default, or does the primary surface want something
you have not specified yet?

**4. The one we would most want you on: label density on the full graph.** 964 nodes at rest,
and in the centre the labels overlap heavily — `1-network-map.png`. That was inherited and was
tolerable for a fallback. As the primary surface it may not be. We have not touched it, because
"make the labels better" is a design problem and we would rather have your answer than our guess.

## 5. Constraints that are not on the table

- **No invented sources, URLs, document numbers or quotes. Ever, anywhere — including in
  mockup copy, placeholder text and example data.** If you need a placeholder, mark it
  unmistakably as one. This is the board's one unbendable rule.
- **Size must never encode importance**, anywhere in the visual language. The largest node
  would be AARO, which this board treats as implicated, not authoritative. Position is
  available; size is not.
- **The 31 canvas assertions.** They read real pixels and they found two defects on the day
  they were written that reading the source did not. Anything you specify has to survive them,
  or has to change them deliberately.

## 6. Two other surfaces exist now, and neither needs you

Mentioned only so the rail going from eight items to ten is not a surprise.

- **PATENTS** — `3-patents-top.png`, `4-patents-lower.png`. Stewart signed off a mockup and we
  built to it. Five Navy patent filings, two prosecutions compared on one time axis.
- **The FOIA layer** — `5-foia-layer.png`. An open question in a node's dossier now names the
  FOIA request that would close it. **If anything here wants your eye it is this**, and only as
  a question: 17 requests already map to 121 open questions across 42 nodes, and that currently
  shows only as a chip on a question. Whether the request queue deserves a surface of its own is
  genuinely open, and we have not designed one.

## 7. The attachments

| file | what it is |
|---|---|
| `1-network-map.png` | the new primary map, at rest, 1920×1080 |
| `2-program-map.png` | your packed map on its own tab, fitted |
| `3-patents-top.png`, `4-patents-lower.png` | the patents tab |
| `5-foia-layer.png` | the FOIA chips in a dossier |
| `design-extract.json` | 280KB, purpose-built for you: the board's structure, the layout model, the counts. Every figure above is derivable from it |

All screenshots are 1920×1080 at `deviceScaleFactor: 1` — not 2 — because a 2× capture viewed
scaled-to-fit shows small text *larger* than a real monitor does, and this board has 8px labels
whose legibility is a live question.
