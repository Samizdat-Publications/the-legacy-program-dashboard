# The packed-cell layout: what is done, what is left, and what I cannot verify

**25 August 2026.** `CLAUDE.md` §9 item 5 is the biggest open piece of work. This is the
cost analysis, done rather than guessed. **I did not build it**, and the last section says
why that was the right call for an unattended session rather than caution for its own sake.

## The good news: the model is finished

`tools/build_l0_layout.mjs` already emits the whole packed-cell layout to
`data/l0-layout-model.json`, 462KB, well under the read cap. It is not a sketch. For both
datasets it carries:

| | `current` | `legacy` |
|---|---|---|
| nodes with final `x`, `y`, `w`, `h` | 110 | 96 |
| edges with `rest`, `role`, `kind` | 326 | 246 |
| bands (rows) | 7 | — |
| era columns + a NO DATE column | 4 + 1 | — |
| world | 2200 × 912 | — |

Every node carries `col`, `band`, `cell` and `slot` as well as its pixel position. Chip
geometry is uniform at 205 × 20, matching `config.geo`. All positions are integers inside
the world bounds. As of this session all nine of Design's checks assert against this file
and all nine are self-tested, so **the model cannot silently drift while the renderer is
built against it.** That was the right order to do the work in.

## The positions are mechanically swappable

`L0DATA.l0` and `layout.current.nodes` are the same 110 ids, both with integer `x`/`y`:

| | source | x range | y range |
|---|---|---|---|
| `L0DATA.l0` (what ships) | force layout | 177 – 1889 | 339 – 1324 |
| `layout.current.nodes` | packed cells | 148 – 2198 | 46 – 912 |

Copying one set of coordinates over the other is a few lines in `build_l0.py`. **That part
is not the work.**

## The work is that `mountL0` is a canvas renderer built for a point cloud

`mountL0` in `tools/l0_patches.py` is **421 lines and 80 `ctx.` calls**. It draws to a
`<canvas>`, not to DOM. Its geometry assumes points, not cells, in at least four places:

1. **`mark()`** draws a 13px glyph (`L0_MARK`) centred on the node. A packed cell is a
   205 × 20 chip with a label inside it. Different primitive, different hit target.
2. **`fitScale()`** computes the fit from point extents plus `+132` for label width and
   `+46` for the mark and label line. A grid already knows its own extent — `worldW` and
   `worldH` — and those two constants become wrong rather than merely unnecessary.
3. **`centreOn()`** centres on the midpoint of the point cloud. A banded grid wants to
   open at the top-left of the first band, because the bands are ordered by measured mean
   C and the order is the argument.
4. **`stack()`** offsets two copies behind a mark to signal an aggregate. Behind a chip
   that is a different shape entirely.

Nothing here is hard. But it is a **rewrite of the primary visual surface**, not a patch,
and Design's §6 flagged this as the one open item that could change the whole approach.
`CLAUDE.md` item 5 records that Design's 24 August response settled it — `mountL0` is ours
end to end, so it is a direct build. That settles *ownership*. It does not reduce the size.

Add to that what does not exist yet in the model and would have to be drawn: band row
labels, era column headers, the NO DATE column header, and the `×` marker for the three
isolated nodes.

## Why I stopped here

**The renderer is canvas, and `tools/runtime_check.js` reads the DOM.** Everything it
asserts today — no `undefined` in the page, no raw slugs in links, chain steps carrying
real dates — it asserts by reading text nodes. It cannot read a canvas. So for a
canvas-drawn packed layout, from this session:

| property | who could catch it |
|---|---|
| positions, bands, columns, chip size, budget | **Design's nine checks — all self-tested, all green** |
| the model going stale under the renderer | **the nine checks** |
| chips overlapping each other | nothing here |
| a band row taller than its cell, clipping | nothing here |
| labels unreadable at the opening fit | nothing here |
| the map opening on empty space | nothing here |
| any of it at 900px wide | nothing here |

That bottom half is most of what makes a layout good or bad, and it is exactly the
complaint that started this work — Stewart, on seeing the board cold: *"way too busy ...
no opportunity for discovery."* Shipping a blind rewrite of the surface he complained
about, on a night when he cannot look at it, risks replacing a hairball he has seen with a
grid nobody has.

`CLAUDE.md` §3 says a cloud session should ship the work, say plainly that visual
properties are unverified, and hand Stewart the artifact. That rule is right for an
incremental change. For a 421-line rewrite of the one surface the whole redesign is about,
the honest reading is that "unverified" would be doing too much work in that sentence.

## What to do with this

The decision is Stewart's and it is a small one to make:

- **If he wants it built blind**, say so and it gets built — the model is ready, the checks
  are in place, and the plan above is the plan. He would be reviewing pixels first, not
  code.
- **If he would rather see it first**, the cheap intermediate is a static comp: render the
  packed model to a standalone page from `l0-layout-model.json` and hand him the link,
  with the live map untouched. That is a self-contained artifact, costs nothing if he
  hates it, and answers the only question that matters — does position now mean something.

I would do the comp. It is the same drawing code either way, and it gets a look at the
thing before it replaces the map.


---

## The comp exists. Here it is.

**https://claude.ai/code/artifact/afb7293f-6051-4686-b308-b68996f50ce9**

Rendered from `data/l0-layout-model.json` as generated, with no position adjusted.
Source kept at `tools/l0_comp.html`. The live map is untouched.

It is drawn as **SVG rather than canvas**, which matters for more than convenience: it
means the geometry could actually be verified from this session, where the real canvas
renderer could not be. Measured headless at 1600x1000:

| property | result |
|---|---|
| chips rendered | 110 |
| **chips overlapping another chip** | **0** |
| chips outside the world bounds | 0 |
| distinct chip sizes | **1** (205 x 20) |
| labelled chips | 110 |
| lines drawn at rest | 103 — matches `figures.restDrawn` |
| start-here pointers | 14 |
| nodes marked with an absent-link cross | 3 |
| band rows / column headers | 7 / 5 |
| page scrolls sideways | no |
| JavaScript errors | none |

Zero overlapping plates is the single property the eye cannot forgive, and it is the one
the QA checklist puts first. On this layout it is structurally guaranteed rather than
hoped for, because cells are packed rather than settled.

### What I can see in it, having looked

- **Position does mean something.** The 2017-2026 column is dense and THROUGH 1969 is
  sparse, which is the disclosure record showing up as shape — the same point the
  timeline's standing caveat makes in words.
- **The `disclosure` band draws 3.** Design predicted this in §6 and read it as the
  structure appearing rather than a fault. It is visible and it does look thin.
- **Labels truncate hard.** At 205px with 9.5px mono a label gets about 37 characters, so
  most read like "Advanced Aerospace Weapon System Ap…". Faithful to Design's chip size,
  and the full name is on hover, but on a board whose node labels are legal citations and
  document titles it is the first thing worth arguing about.
- **The lines at rest are very faint** against the band fills. Pixel polish, not layout.

### The one thing this comp does NOT settle

It is SVG. The real map is canvas, and a canvas rewrite of `mountL0` is still 421 lines
with its own hit-testing, panning, zoom and label-drop logic. The comp proves the
**arrangement** is sound. It does not prove the **implementation** will be, and nothing
available to this session would.

---

## OUTCOME: built, 25 August 2026

Stewart signed the comp off and asked for the build with all three options on. It is done
and the whole gate is green -- `notes/PACKED-LAYOUT-BUILD-2026-08-25.md`.

**The "who could catch it" table above was wrong in its bottom half, and this is the useful
correction.** It said nothing in a cloud session could catch chips overlapping, a band
clipping, or the map opening on empty space, because the renderer is canvas and
`runtime_check.js` reads the DOM. `runtime_check.js` cannot, but `getImageData` can, in the
same headless browser. `tools/test_packed_layout.js` reads the pixels back and checks all
110 chips against the coordinates `data/l0-layout-model.json` states independently.

It found two real defects that reading the source would not have: the pinned column head
painting over six chips at 12% opacity, and a map you could pan off into empty world.

What genuinely remains out of reach is narrower than the table claimed: **whether a
truncated label is still a useful label, and whether it looks good.** Those need eyes, and
nobody has looked at this on a screen.
