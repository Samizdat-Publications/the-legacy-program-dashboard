# Claude Design's spec against the build, item by item

**26 August 2026.** Stewart: *"make sure ALL of claude designs stuff it designed is
implemented"*. This is the audit. Source is `notes/design-2026-08-24/DESIGN-RESPONSE-LAYOUT-2026-08-24.md`,
**now synced to the newer revision from Stewart's zip** (the repo held an older copy: the
patch question was still open in it and the rarity-pin answer was missing).

`verified` means I ran it or looked at it. `read` means I read the implementation and did
not exercise it.

---

## 0. Progress since this audit was written

Design answered the four open questions (`notes/design-2026-08-24/`, synced to that
revision). **Batch 1 is built:**

- **Middle truncation**, head 62% / tail rest, never end truncation. 50 labels fit whole,
  60 middle-truncate, 0 end-truncate. The distinguishing tails survive: `AARO Historical
  Re…, Volume II`, `Sec. 6802, James M…L. 117-263)`, `STAR GATE and pred…, 1970-1995`.
- **The class glyph**, 11px, `I P E L D p`, in the slot an image will take.
- **The start-here rank numeral**, amber, 1 to 14.
- **Denial three states.** Design's correction to my "switch it off": arrowhead where the
  denier is named, a **perpendicular red bar** at the midpoint where it is an act with no
  established direction, and no denial styling at all for an association. `denialKind` is
  plumbed end to end and degrades to `undirected`, which claims the least.
- **Design corrected its own channel table**: class keeps the left rule and tier keeps the
  stroke, which is what the build already did. No change needed. The reason is the image
  slot: once a node carries a photo the glyph is gone, so class needs the rule.

Gate: **40 verify checks, 13 canvas assertions**, all self-tested. New: `a denial that is
not a directed act carries no denial styling`, `no chip label is cut off at its end`.

**Batch 2 is built: the dense occupancy mode.** Below the label threshold the chips
collapse and every occupied cell prints its count. The edge layer is switched off
entirely, the rows go equal-height, and the axis type stays at its authored size. The
rendered matrix matches the model exactly, 110 of 110, and the structural claims Design
named read straight off the screen: retrieval has nothing in 2000-2016, oversight is 13
of 17 in the last era, disclosure is 3.

Design also caught two bugs in its own comp after the first download and both are
recorded here because one of them applies to any reimplementation:

- **One row set, computed before anything consumes it.** Deriving the equal-height rows
  for some consumers and leaving others on the model's chip-derived bands puts two
  contradictory geometries on the same canvas. This build routes stripes, gutter labels
  and cells through a single memoised `bandRows()`, so it never had the bug, and the
  memoisation now makes that explicit.
- **The start-here wash is fit-width only.** In dense mode the flagged cell already
  carries its own amber background, so a wash would be a duplicate mark. **Gate the wash
  on `!dense` when it is built** (task 5).

One defect the dense mode exposed and that Design's answer already covers: at 0.23x the
era column heads collided with each other, because the head is drawn at an authored size
while the column shrinks with the world. They now budget against the smaller of the
column's rendered width and the gap to the next head.

Gate: **40 verify checks, 16 canvas assertions.** New: `overview_is_never_anonymous`,
`overview_draws_no_orphan_edges` (tested by difference -- toggling LINES AT REST cannot
change a pixel in dense mode, and must change many where chips draw),
`axis_type_readable_at_every_scale`.

**Batches 3 and 4 are built, and every item that does not need research is now done.**

- **The start-here legend**, ranked, with each flag's reason. Collapsible and collapsed
  by default, which is a divergence: Design's legend sits beside the canvas and this
  board's map fills its host, so an always-open one covered the NO DATE column.
- **The cell wash**, fit-width only, deduped by cell.
- **The breath cycle**, 7s, in sync rather than staggered. BREATH / ONCE / STILL.
- **`prefers-reduced-motion`** as a hard override the control cannot undo.
- **Selection particles**, outward from the node the reader is standing on, 74px/s,
  deterministic per-edge phase. Denial particles remain blocked on authoring `denier`.
- **The search grammar**, all of it, `via:` included. The no-result state names what it
  did not search.
- **The backfill queue** grew to Design's nine rows.

### All seventeen of Design's checks now exist

| | |
|---|---|
| built before this session | 9 |
| built this session | 8: `no_unsourced_arrowhead`, `overview_is_never_anonymous`, `overview_draws_no_orphan_edges`, `axis_type_readable_at_every_scale`, `labels_truncate_in_the_middle`, `no_two_channels_on_one_property`, `rarity_order_matches_the_pin`, `queue_covers_every_field_read` |

Plus four this build added that Design did not name: `head-row-clear`, `denial direction
is published only where the record names a denier`, `a denial that is not a directed act
carries no denial styling`, and a **render-level** `motion_only_where_attested` (Design's
own guards the model's flags and passed for the whole first build while nothing moved).

**Gate: 42 verify checks · 40 audit re-derivations · 23 runtime assertions · 18 canvas
assertions.** Nine of nine steps green.

## 10. What is genuinely left, and none of it is code

| | why it is not code |
|---|---|
| `denialKind` on the 11 non-acts, `denier` on the 12 directed denials | reading 174 labels one at a time. Deriving them from the label text automatically is the same move as the convention that was "CONFIRMED" against one agreeing sample |
| 46 `short` values over 37 characters | authoring |
| `members[]`, the direct/routed split, `dateEnd` | pipeline backfill |
| the photo tile itself | the register is empty on purpose, and a render branch with no data to exercise it is untested code. The **slot is reserved** and the class letter fills it |
| image sourcing | licensing judgement about real people's faces. Must not run unattended |

One thing remains unresolved rather than deferred: the inherited `mountNetwork` renderer
carries a time-direction particle flow, the exact treatment Design rejected. It mounts on
`S.l0full`, and three attempts to reach that state failed.

---

## 1. Layout and edge budget — done

| Design item | state | how |
|---|---|---|
| packed cells, 7 bands x 5 columns, 110 chips | **built** | verified on screen |
| bands ordered by measured mean C, descending | **built** | verified, model + gutter labels |
| eras across, NO DATE column for undated | **built** | verified |
| one chip size, 205x20 | **built** | gate check `no_size_channel` |
| edge budget, 103 of 326 at rest | **built** | gate check, verified |
| rarity order pinned and recomputed | **built** | generator emits `rarityDrift`; snapshot reports it |

## 2. Channel assignment — mostly done, two gaps

| channel | Design says | state |
|---|---|---|
| position | band x era | **built** |
| size | nothing | **built** (guarded by a check) |
| chip left rule | entity tier A/B/C | **built** |
| **chip glyph / image slot** | **class letter, or the node's image** | **NOT BUILT** |
| line colour | relationship kind | **built** |
| line dash | claim tier | **built** |
| line width | structural vs anchor, two steps | **built** |
| arrowhead | denial direction | **built, then switched off** — see `notes/DENIAL-DIRECTION-2026-08-26.md`. It was drawing from `[a,b].sort()`. Now draws only with an attested `denier`, and none is authored yet |
| numeral chip | shared-member count | **built** |
| **motion** | **attested direction only** | **NOT BUILT** |
| amber, offset | the start-here pointer | **built** |

## 3. Motion — not built at all

The program map is provably static: three identical canvas frame hashes over 1.8s, twice.
No particle code, no breath cycle, no `prefers-reduced-motion` in `mountL0`.

| Design item | state |
|---|---|
| particles on denial edges, direction attested | **NOT BUILT**, and **blocked**: no edge names its denier yet |
| particles on the selected node's edges | **NOT BUILT** |
| all motion stops under `prefers-reduced-motion` | **NOT BUILT** |
| rejected: time-direction flow on every line | correctly absent from `mountL0` |

**Worth knowing:** the inherited parent-board renderer `mountNetwork` *does* carry a
time-direction particle flow (`p.flip = new Date(s.date) > new Date(t.date)`), which is
precisely the treatment Design rejected. It mounts when `S.l0full` is set. I could not
trigger that state in three attempts, so I cannot say whether it is reachable. **Unresolved.**

## 4. The start-here layer — the pointer only

| Design item | state |
|---|---|
| amber, dashed, offset from the chip, never a property of it | **built**, verified |
| 14 flags, signed off, under the 16 cap | **built** |
| **rank numeral on the chip** | **NOT BUILT** |
| **cell wash so the region reads at fit-width** | **NOT BUILT** |
| **legend carrying the reason for each flag** | **NOT BUILT on the map**. `why` is authored for all 14 and reaches the analyst's "where do I start" branch, not the board |
| breath cycle at rest, BREATH / ONCE / STILL | **NOT BUILT** |

Design's line on this: *"A pointer without its reason is the thing this board exists not to
do."* The reasons exist and are good. They are just not on the map.

## 5. Search — free text only

`via:bigelow` returns **"0 of 956 entities. No entity matches that query."** The grammar is
read as free text.

| Design item | state |
|---|---|
| space-separated tokens ANDed, free text over label/id/roles/cluster/class | **built** |
| `band: era: cls: tier: cluster: role: id: flag: isolated:` filters | **NOT BUILT** |
| numeric `deg: claims: denials:` with `>` / `<` | **NOT BUILT** |
| **`via:` reaching off-map shared members** | **NOT BUILT** — Design called this one out specifically |
| matches dim the map and take a solid cyan outline | **NOT BUILT** |
| no-result state names what it did *not* search (the 858 below the floor) | **NOT BUILT** — it says "No entity matches that query" |

## 6. One image per node — register empty AND slot absent

`data/l0-images.json` is empty on purpose, which is correct and is CLAUDE.md §2. But the
renderer has no image or glyph branch at all, so populating the register would change
nothing on screen. Both halves are outstanding, and the slot half is pure code with no
sourcing risk.

Design's five rules (square never round; greyscale at rest, colour on selection or search
hit; `portrait` crops to fill and `mark` fits inside; `ask` renders a dashed frame with its
reason; missing falls back to the class letter) are all unimplemented, as is the class
letter fallback itself.

## 7. Backfill queue (§4) — five of seven landed

| field | state |
|---|---|
| `via[]` on summarised pairs | **done**, 109 of 109 |
| `C` / `A` / `D` | **done**, 110 of 110 |
| `short` | **done**, 110 of 110 populated, 60 genuinely shorter than the label. **46 still exceed 37 characters**, so truncation persists |
| denial `a`/`b` pairs | **plumbed today**, all 47 carry raw pairs; `denier` still unauthored on all 174 |
| `members[]` and the direct/routed split | **not landed** (0 of 110 carry `members`) |
| `dateEnd` | **not landed** (0 of 110) |
| `photo` / `photoCredit` / `photoKind` | **not landed**, and no slot to receive it |

## 8. Design's ten checks (§5) — nine and a half

All present in `tools/verify.py` except `rarity_order_matches_the_pin`, which exists as a
**report** (the generator emits `figures.rarityDrift`, `state_snapshot.py` prints it) but
not as a gate check. Design's "must reject" column says the check should fire on a research
pass that inverts a near-tie. It reports; it does not fire.

Two checks added since, not Design's: `head-row-clear` (canvas) and `denial direction is
published only where the record names a denier` (verify). Gate is 39 verify checks, 40
audit re-derivations, 12 canvas assertions.

---

## 9. What is left, ranked by cost against value

| # | item | blocked by |
|---|---|---|
| 1 | class letter / image slot in chip and dossier | nothing. Pure code |
| 2 | start-here rank numeral + legend with reasons | nothing. Reasons already authored |
| 3 | search grammar, `via:` included | nothing |
| 4 | selection motion (particles on the selected node's edges) | nothing. Direction is the reader's own act, not an assertion |
| 5 | `prefers-reduced-motion` | comes with any motion work |
| 6 | breath cycle + cell wash | nothing |
| 7 | denial particles | **`denier` on 174 raw edges**. Research, not code |
| 8 | `members[]`, direct/routed split, `dateEnd` | pipeline work |
| 9 | image sourcing | licensing judgement about real people. Must not run unattended |
| 10 | `rarity_order_matches_the_pin` as a gate check | nothing |

Items 1 to 6 and 10 are buildable now and none of them needs a decision from anybody.
