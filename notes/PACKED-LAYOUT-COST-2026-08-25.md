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
