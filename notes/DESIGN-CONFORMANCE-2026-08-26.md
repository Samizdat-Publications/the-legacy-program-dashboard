# Claude Design's spec against the build, item by item

**26 August 2026.** Stewart: *"make sure ALL of claude designs stuff it designed is
implemented"*. This is the audit. Source is `notes/design-2026-08-24/DESIGN-RESPONSE-LAYOUT-2026-08-24.md`,
**now synced to the newer revision from Stewart's zip** (the repo held an older copy: the
patch question was still open in it and the rarity-pin answer was missing).

`verified` means I ran it or looked at it. `read` means I read the implementation and did
not exercise it.

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
