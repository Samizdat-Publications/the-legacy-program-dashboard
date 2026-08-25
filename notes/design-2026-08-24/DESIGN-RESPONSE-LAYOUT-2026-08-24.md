# Design response — make position mean something

**For:** the implementation session
**From:** Claude Design, 24 August 2026
**Answers:** `notes/DESIGN-BRIEF-LAYOUT-2026-08-14.md` §3A (layout) and §3B (edge budget)
**Ships:** `tools/build_l0_layout.mjs` · `data/l0-layout-model.json` · `L0 Positional Layout.dc.html`

---

## 0. The reproduction correction — read this first

The brief asked that every published figure be reproducible by a shipped generator run
against a file that exists in the repo. My first pass reported that the brief's own
sources were **absent**. That was wrong, and the correction is more useful than the
original claim.

`data/the-program.json` (6.9MB) and `data/l0-model.json` (5.7MB) are tracked and pushed.
The read API caps around 1MB, so they returned as *missing* rather than as *too large*.
**An unreadable file and a missing file produce an identical symptom, and a reader that
cannot distinguish them will report the wrong fault confidently.** I did.

`data/design-extract.json` (122KB) fixes it. Every figure in the brief reproduces from it:

| | brief said | this run | |
|---|---|---|---|
| board nodes | 968 | **968** | agrees |
| L0 nodes on the map | 110 | **110** | agrees |
| edges drawn before budget | 313 | **318** | moved — 209 direct + 109 summarised |
| largest shared-member count | 5 | **18** | the case that killed the tick vocabulary is live |

One trap survives and is worth restating in any future brief: `data/l0-extract.json` is
readable and accurate for the graph, but its `deg` field is an **edge-instance count**.
Using it moves the L0 set from 96 to 107. Degree in the shipped generator is always
recomputed from distinct neighbours, for both datasets.

**Every number in this document and on the comp is read from
`data/l0-layout-model.json`.** There is one number, in one place. Re-run the generator
and the page follows; hand-edit a figure and the page contradicts the file it cites.

---

## 1. A — the layout

**X is era. Y is function. A node's cell states when it starts and what the board says it
did, before the reader reads a word of it.**

- **X** — four era columns, **equal width**, keyed on `dateStart`. Undated nodes get a
  labelled `NO DATE` column of their own.
- **Y** — one band per role tag, assigned by **rarest tag wins**, ordered top to bottom by
  the band's **measured mean C**.
- **Cell** — chips packed by degree, one uniform size. Position is a pure function of
  `(era, band, degree, id)`. **No physics, no seed, no wall clamp, no label-overlap
  figure to watch** — a packed grid cannot overlap, so those metrics stop existing rather
  than getting better.

Geometry: world 2200×937 (the same `WORLD_W` the existing bake uses), 148px label gutter,
chips a fixed 205×20.

### The five questions

**1 · How do you pick a primary function when the tags overlap?**
Rarest tag on the map wins. Rarity is a usable proxy for specificity — the tag fewest
nodes claim is the most particular thing the board says this node did. One line, no manual
pass over 110 dossiers, and it re-derives itself when the research moves. 369 tags across
110 nodes, mean 3.35. `concealment` is claimed by 79 and is therefore **never** a band: it
is the field, not a row.

On the legacy board, where `C` exists, the rule checks out against the board's own
scoring — ordering bands by measured mean C puts reverse-engineering at 2.50 and
disclosure at 0.71 without being told to. That is the validation, and it needs C/A/D in
the extract to run on current data.

**⚠ One fragility, found by running both datasets — now handled.** Two tags with
near-equal counts can swap rarity rank between research passes and take every node
carrying both with them. `oversight` (68) and `disclosure` (74) are 8% apart on the
current board and **inverted** on the legacy one, which moves fourteen nodes between two
bands.

**Answer to "pin the rank or let it re-derive?": neither, quite. Pin it AND recompute it,
and report the disagreement instead of obeying it.**

Pure re-derivation is unsafe now that position carries information — six tags landing in a
research pass would silently relocate fourteen nodes, and a reader who saw the map last
month would have no way to see that it happened. Pure pinning is also unsafe: it goes stale
and stops describing the board. So `RARITY_PIN` in the generator is the rule, the observed
order is recomputed every run, and `figures.rarityDrift` reports every disagreement. Moving
a node between bands becomes a decision someone makes with a diff in front of them. Same
discipline that caught 107-vs-96: state the invariant, make the violation loud.

Pinned 24 August against `design-extract.json`. Current data: **zero drift**. Legacy data:
**reports the oversight/disclosure inversion** rather than acting on it — which is the check
working, not failing. Re-pin deliberately; do not edit the constant to silence a warning.
Three adjacent pairs were within 10% at pin time (research/custody, oversight/disclosure,
disclosure/concealment) and are the ones to watch.

**2 · What happens to a node that spans eras?**
It sits at its start, and the span is not drawn. On the legacy board only 40 of 96 nodes
carried a `dateEnd` and only 20 of those ran longer than a year, so an extent channel
would be absent for two thirds of the map and would print an absent end date as a closed
one. Consequence, not duration, is what AAWSAP-type cases actually want — and that is an
edge, not a bar.

**3 · How do you label bands without stealing the space you just freed?**
A 148px left gutter, once, outside the plot: band name, node count, mean C. Nothing is
labelled inside a cell and no legend sits on the canvas. The gutter costs 7% of the world
and replaces the label-collision problem entirely.

**4 · How do you stop it reading as a Gantt chart?**
The X axis is four **discrete columns**, not a continuous scale. No position within a
column means a year, so no horizontal run can be read as a duration and no crossing as a
sequence. The orthogonal traces reinforce it: a leg turns into a gutter and leaves, which
is wiring, not a bar. 21 direct edges join nodes in the *same cell* and are suppressed
precisely because they say nothing position has not already said.

**5 · The last decade holds nearly half the map. Compress or accept?**
Accept, and keep the columns equal. 42% of dated nodes start in 2017–2026. Widening that
column to fit its contents, or narrowing the early ones to their thin population, is
exactly the finding erased. Equal columns make the pile-up the first thing the eye gets,
and the crowding stays bounded — the busiest cell holds 13, which packs into two columns
without shrinking a chip.

### What the matrix says, before any node is drawn

```
                       ≤1969  70-99  00-16  17-26  ND   total
retrieval                  5      3      0      2   0      10
reverse-engineering        2      3      5      4   1      15
funding                    4      7      3      5   0      19
research                   7      5      5     11   3      31
custody                    2      2      3      8   0      15
oversight                  1      2      0     13   1      17
disclosure                 0      2      0      1   0       3
```

Retrieval is a first-two-era activity with **nothing** in 2000–2016. Oversight is 13 of
17 in the last decade. That is the 79-year gap stated by position instead of left for the
reader to notice, and it is the strongest argument this layout makes.

---

## 2. B — the edge budget

Tier cannot thin this map and degree should not: **134 of 209** direct edges are Tier 1,
and gating on degree keeps **33** while stripping the periphery the floor already earned.
The budget comes out of the layout instead. Position now states era and band, so a short
edge largely restates where its endpoints sit; a long one asserts something position
cannot.

- **Clause 1 · structural** — draw an edge if it crosses **≥2 bands and ≥1 era**. → 50
- **Clause 2 · anchor** — every node keeps its **single strongest** edge regardless
  (lowest claim tier, then longest span, then id). Nothing sits on this map unexplained. → +46
- **Rest** — summarised shared-member edges are **off**, except where one is a node's
  anchor. They are the closest thing to what the bands already say, and there are 109.

**= 96 lines at rest, 30% of the 318 the map can draw.** The other 222 appear on
selection.

```
 209  100%  every hand-written L0-L0 edge (today's rest state)
 318  100%  + summarised shared-member edges
 134   64%  claim tier 1 only
  33   16%  both endpoints degree >= 15
 145   69%  crosses >= 1 function band
 101   48%  crosses >= 1 era
  89   43%  crosses >= 2 bands
  50   24%  crosses >= 2 bands AND >= 1 era      [clause 1]
  96   30%  + one anchor per node                [clause 2] = THE RULE
```

Three nodes have **no L0-level relationship of any kind**, so no budget could draw one.
They carry an explicit `×` rather than looking like a rendering failure. That is different
from an orphan — a node whose every edge the budget dropped — which is a bug and fails the
build.

### The count vocabulary

The five-tick vocabulary is dead, as the brief said. A shared-member count draws as a
**numeral in a bordered chip** at the line's midpoint: no ceiling, no overflow case, 18 and
180 render the same way. Select either end and the chip carries the **names** instead —
two names, then one name and a remainder, then the numeral past four. `dia~dird-series`
sharing 18 is in this data and renders correctly.

---

## 3. Channel assignment — the whole map, one line each

| channel | carries | never |
|---|---|---|
| **position** | era × function band | anything else |
| **size** | nothing | importance, degree, claims, members — §4, non-negotiable |
| chip left rule | entity tier A/B/C | |
| chip glyph / image slot | class, or the node's image | |
| line colour | relationship kind — cyan structural, grey anchor, violet shared, red denial | |
| line dash | claim tier (divergence D1) | anything else |
| line width | structural vs anchor, two steps only | any weight-by-count |
| arrowhead | denial direction (divergence D3) | |
| numeral chip | shared-member count | |
| **motion** | **attested direction only** | a time-direction flow |
| **amber, offset** | the start-here pointer | anything that means credibility |

### Motion — and the two treatments rejected

Motion is the last unused channel, which makes it the easiest to spend badly. It carries
direction the record establishes: denials (`a` issued it, `b` is the subject) and, on
selection, which end of an edge you are standing on. **If something moves, the direction
is attested.**

- **Rejected: particles flowing along every line in the direction of the time axis.** It
  states that the relationship runs from the earlier node to the later one, and for most
  of these edges the board makes no such claim. An institutional edge between a 1947 node
  and a 2024 node has no direction at all, and brief question 4 is explicit that a time
  axis must not imply the edges are chronological. A moving dot is a far stronger
  implication than a static line.
- **Rejected: line weight by member count, claim count or degree.** That is the size
  channel wearing a different coat, and it would put the most ink on AARO.
- **Rejected: a scan bar traversing the map left to right.** It pulls the eye along the
  time axis — the one reading this layout must not imply. Stewart objected to it on sight
  and he was right.

All motion stops dead under `prefers-reduced-motion`.

### The start-here layer

An editorial pointer is **not** a property of the record, so it takes amber — the board's
open/missing hue — drawn as a dashed box **offset from** the chip rather than a fill
inside it. It reads as a mark laid on the board. Nothing about the node's own body
changes, so it can never be mistaken for a tier, and **AARO cannot be promoted by being
pointed at**.

Two scales, because it has to survive both: the cell takes a wash so at fit-width the
*region* reads before any label does; the chip takes the outline and a rank numeral so the
set is enumerable and the legend can carry a reason for each. **A pointer without its
reason is the thing this board exists not to do.**

At rest it **breathes**: all flagged cells surface together over ~1s, hold ~2s, fade, and
the board sits clean ~2.5s before the next. In sync, not staggered — the board raising its
hand once reads better than nine separate events. Between breaths only the rank numeral
stays, so the set is findable and the highlight is never permanently on the map.
`ONCE` does it exactly once on load in rank order; `STILL` disables it.

**Which nodes are interesting is not a design decision.** Drop
`data/l0-highlights.json`:

```json
{ "rule": "one sentence on how these were chosen",
  "flags": [ { "id": "aawsap", "why": "short reason, shown in the legend" } ] }
```

Order is the rank. The generator refuses ids not on the map and refuses more than 15% of
the map — a pointer at everything points at nothing. Absent, it derives a clearly-labelled
**placeholder** set by a stated rule so the design language has something real to draw.

### Search

One field, space-separated tokens ANDed. A bare token is free text over label, id, roles,
cluster and class. `key:value` filters: `band: era: cls: tier: cluster: role: id: flag:
isolated:` and numeric `deg: claims: denials:` with `>` or `<`. **`via:` reaches the
off-map shared members**, so `via:bigelow` returns the map nodes joined by Robert Bigelow
without him ever being drawn.

Matches dim the map and take a solid cyan outline: **the result set is a shape in the
matrix**, and the list is a shortcut rather than the answer. The no-result state says what
it did **not** search — the 858 nodes below the degree floor.

On the board this has to be a `CMD` action to satisfy constraint 4 of the parent brief.

### One image per node

Field names inherited from the sibling board rather than invented — `photo`,
`photoCredit`, `assets/photos/<id>.jpg`, and PHOTOS.md's four-state clearance. One
addition: **`photoKind`**, `portrait` or `mark`.

1. **Square, never round.** A circular crop is an avatar; this is an intelligence product.
   16px in the chip, 64px in the dossier, no other size.
2. **Greyscale at rest, full colour on selection or a search hit.** Not styling: 110
   institutional logos in brand colour would take over a palette that spends colour on
   claim tier and edge kind.
3. **`portrait` crops to fill, `mark` fits inside.** A cropped logo is a broken logo and a
   letterboxed face wastes the slot, so the kind is a field, not a guess.
4. **An image is a claim.** It carries its credit and its clearance; the credit prints in
   the dossier. Only `clears` and `ask` are ever drawn, and `ask` renders a dashed frame
   with the reason. A photograph of the wrong person is a factual error no framing fixes.
5. **Missing is not broken.** The class letter is the answer — it says what the node *is*
   rather than implying a face nobody found. On a load error the record drops to null and
   the letter returns.

The slot occupies the space the class letter already had, so **images cost no chip width
and removing them loses no information**.

*Implementation note worth carrying:* never route an image URL through an `src` attribute
hole in a streaming template. `src` is fetched eagerly, so the browser requests the
literal unresolved hole text once per placeholder row. Compute the whole
`background-image` value instead — an unresolved style hole renders nothing and requests
nothing, and `background-size: cover|contain` maps one-to-one onto the portrait/mark rule.

---

## 4. Backfill queue — what to pull

Each row is a task. The design degrades honestly until it lands rather than guessing.

| field | what it is | where to pull it | what the design cannot say without it |
|---|---|---|---|
| `via[]` | which members each summarised pair shares | `build_l0.py` P3 already builds it as `via` on each summarised edge — emit the id array, not just the count | a shared line can name "Puthoff · Bigelow" instead of printing `2` |
| `members[]` | the off-map neighbours of each L0 node | for each L0 node, its adjacent non-L0 nodes with label, class, connection type and claim tier — `build_l0.py` has this as `members.direct` | the dossier can answer "which people?" |
| `members` direct/routed split | the P1 split | `build_l0.py` computes `members.direct` and `members.routed` separately; the extract flattens them | without it `members` is a roll-up to depth 3, so "5 on the map, 14 held back" cannot be made to sum to the degree |
| `C` / `A` / `D` | the three scored axes | straight off the node records — every node already carries them | band order is the measured mean C, which is what makes the vertical axis mean distance from the material |
| denial `a`/`b` | which end issued it | the merged board's edge records; aggregating a pair loses it, so carry the pairs for denial edges | motion carries attested direction and nothing else, so the particle layer has nothing it may say at rest |
| `dateEnd` | the end of a span where the record has one | the same node documents `dateStart` comes from | brief question 2 — how many nodes could carry an extent at all |
| `photo` / `photoCredit` / `photoKind` | one image per node | `data/l0-images.json` keyed by node id, per §3 above; only `clears` and `ask` ship, and `ask` carries its reason | the chip slot and dossier tile are built and waiting |

**Standing rule:** any new field the design reads gets a row here stating what to pull and
where from, so this session never has to re-derive the ask.

Both datasets are baked side by side (`current` from design-extract.json, `legacy` from
l0-extract.json) so the cost of each gap is **visible in the comp rather than argued**.
Switch the dataset in §00. Nothing is mixed — every figure comes from one dataset and the
header says which.

---

## 5. Checks, and the input each must reject

A check that has never failed is indistinguishable from a broken one.

| check | asserts | must reject |
|---|---|---|
| `degree_is_distinct_neighbours` | the L0 set from distinct neighbours equals the shipped model's node list | a model baked from the extract's `deg` field — it reports 107 against 96 |
| `figures_match_model` | every number rendered is read from `l0-layout-model.json`, not recomputed | any hand-edited figure in the write-up |
| `no_node_without_a_line` | after the budget, every node with any L0-level edge has one drawn at rest | clause 1 shipped without clause 2 — it reaches 50 of 110 nodes, leaving 60 bare |
| `absent_prints_as_absent` | undated nodes sit in a labelled `NO DATE` column; nodes with no L0-level link carry `×` | placing an undated node in an era column; an `isolated` count dropping to 0 without those nodes gaining a real edge |
| `no_size_channel` | every chip is 205×20 | any model where the set of distinct chip widths or heights has more than one member |
| `layout_is_deterministic` | two runs over identical inputs give byte-identical positions | a re-introduced force pass |
| `rarity_order_matches_the_pin` | the rank the board's tag counts imply equals `RARITY_PIN` | a research pass that inverts a near-tie — legacy data drifts on oversight/disclosure and the check fires |
| `motion_only_where_attested` | a path carries a particle only if it is a denial or belongs to the selected node | a time-direction flow on every line |
| `highlights_are_a_pointer` | flags name ids on the map, stay under 15%, and change no channel that means credibility | a flag naming an id the floor excluded; flagging more than 16 of 110 |
| `model_under_read_cap` | the emitted model is under ~1MB | the thing this whole correction was about — the generator exits non-zero |

---

## 6. What I could not settle

- **Whether this can be a patch.** ✅ **Answered by the implementation session: `mountL0` is
  theirs end to end, so this is not a patch against the parent renderer and §4.1 of the
  parent brief does not bind it.** The packed-cell layout can be built directly. This was
  the one open item that could have changed the approach; it does not.
- **The date axis rests on merge precedence, not on me.** On the legacy corpus 21 ids
  carried conflicting `dateStart` values, 14 on the map, and exactly **one** changed an era
  column — `yankee-blue`, dated to both 1980 and 2023, marked `?` on the chip. If
  `merge.py`'s precedence rule is not the one the axis should follow, the axis is wrong for
  that node and no layout fixes it.
- **Two of the eight bands are residuals, and that is now labelled.** A tag claimed by more
  than half the map can only win when a node carries nothing rarer, so its population is a
  **residual rather than a category**. `concealment` (79) never wins and draws no row;
  `disclosure` (74) draws 3; `oversight` (68) draws 17. So `disclosure` at 3 is not a
  finding about disclosure's role on this board — it is a mechanical consequence of being
  the second-most-universal tag. **Accept it, do not promote a band by hand.** The gutter
  now marks both rows `residual`, which is the difference between a thin row that is honest
  and a thin row that looks broken. Merging them would be worse: `oversight` at 13 of 17 in
  the last decade is the 79-year gap made visible, and collapsing it into a shared residual
  row destroys the strongest thing the layout says. Note also that whether a node lands in
  oversight or disclosure is *exactly* what the 68/74 near-tie governs — the pin above is
  what makes that population stable and explainable rather than accidental.
- **The entry surface may want to own the rest state.** With six curated paths returning 7
  to 38 nodes each, the honest default may be no map at all until a path is chosen — in
  which case this budget is what the map falls back to when a path is *cleared*, not what a
  stranger meets first. That is a product call.

---

## 7. Not in scope, not touched

The four-row shell, the left rail, the dossier dock, the analyst bar, the seven
credibility rules, node size as a channel, and the two kept divergences D1 and D3. This
proposal changes **where a node sits** and **which lines are drawn at rest**. Nothing else.
