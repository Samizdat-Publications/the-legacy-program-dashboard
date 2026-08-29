# Handoff — 29 August 2026, the map inversion, the patents tab, and the FOIA layer

**Read `CLAUDE.md` first, then this. This supersedes `notes/HANDOFF-2026-08-29.md`,
which is still accurate on everything it lists as done.**

**`git fetch --all` BEFORE you read any handoff.** That cost this session forty minutes.

**Do not trust any figure here.** Run `python3 tools/state_snapshot.py --gate`.

---

## 1. THE DECISION: the two maps swap roles

Stewart, 29 August, after using the live board:

> "I clicked on grusch or someone and instead of our orthogonal map it gave me this
> which is I think the style from the vanishing. I actually think I like this better
> ... it shows the connections better than the orthogonal one which I like but when a
> subject is clicked you can't see all the connections like you can here"
>
> "Maybe the orthogonal map becomes its own tab that's just the whole map so you can
> see it while our primary map is in the style in the screenshots below, where the
> analysis tab sends you"

**So: the force-directed full graph becomes the PRIMARY network map. The orthogonal
packed L0 map becomes its own tab showing the whole program map.**

This is a reversal of roles, not a deletion. Both survive.

**It is also the sign-off that `tools/l0_patches.py:47` has been waiting for since
25 August**, where the current arrangement is described in the file's own words as
"an addition to the spec, not an implementation of it. Flagged for sign-off." He has
now signed off, in the opposite direction from what was built.

## 2. How the two maps actually relate, precisely

There is **one view** with **two renderers**, not two views. Nothing is people-vs-program.

| | packed L0 map | full graph |
|---|---|---|
| nodes | 110 (the program map, degree >= 6) | all 964 |
| layout | Design's packed cells, 7 bands x 5 columns, orthogonal | force-directed, WebGPU |
| origin | built for this board | inherited from The Vanishing |
| edges at rest | 103 of 326, by the model's own budget | all, with 1/2/3-hop controls |

The switch, patched in at **`tools/l0_patches.py` around line 2049**:

```js
S.l0full = !!(S.path || (S.frame && S.frame.length));
if (S.l0full){ MAP = mountNetwork(wrap); renderNetworkChrome(); }
// else mountL0(...)
```

**No path and no frame -> packed L0. A path or a frame -> full graph.** Stewart reached
it by pressing **"Show me on the map"** in the STRONGEST PAIR insight callout, which sets
`S.frame`. `selectNode` deliberately does NOT swap, per the comment at `l0_patches.py:43`:
"the ledger is a table of contents for the dock, and the dock opening must not move the
map." That is exactly the behaviour he is complaining about.

## 3. The shell's view system, which is where all three builds land

All line numbers are `ref/the-vanishing-v2.html`, which `l0_patches.py` patches.

| what | where |
|---|---|
| `const VIEWS = [...]` | 2063 |
| `VIEW_LABEL` map | immediately after 2063 |
| `renderSurface()` dispatch | 3265 — `({NETWORK:viewNetwork, ...}[S.view] \|\| viewNetwork)(v)` |
| shortest view template | `viewCounterargs`, 3785, about 23 lines |
| `viewNetwork` | 3283 |
| `mountNetwork` | 2764 |

**A view is one function `viewXxx(v)` that builds an HTML string and assigns
`v.innerHTML`.** It uses existing classes: `view-head`, `pcards`, `pcard`, `eyebrow`,
`sec`, `block b-claim`, and `esc()`. Adding a view is four string patches: the `VIEWS`
array, `VIEW_LABEL`, the dispatch map, and the function itself. That is genuinely small.
`l0_patches.py` already renames `COUNTERARGS` to `COVERUP` this way.

## 4. What the inversion touches, and the one real hazard

Mechanically small; the risk is all in the gate.

- `viewNetwork` patch, `l0_patches.py` ~2049 — make the full graph unconditional.
- New view for the packed map: `VIEWS`, `VIEW_LABEL`, dispatch, and a `viewProgramMap(v)`
  that calls the existing `mountL0`.
- **`tools/test_packed_layout.js` is 30 canvas assertions that drive the L0 map and
  sample pixels at each of the 110 chips.** They currently assume L0 is the NETWORK rest
  state. They must navigate to the new tab first. **Do not weaken them to make them
  pass** — they found two defects nothing else could, and the tenth poison moves every
  chip 60px on the real page and requires the match to collapse.
- `tools/runtime_check.js`, 28 DOM assertions, likely assumes L0 at rest.
- The L0 repaint hook, `l0_patches.py` ~2414, keys on `!S.l0full`.
- L0-specific chrome: the measured `--l0-ctl` control row, era heads, `clampView()`.

**THE HAZARD, and it is a real one.** `l0_patches.py` ~2418 records that the inherited
full-graph renderer drew a particle on every visible edge, flipped by
`new Date(s.date) > new Date(t.date)` — a time-direction flow on every line. Claude
Design named and rejected exactly that: *"It states that the relationship runs from the
earlier node to the later one, and for most of these edges the board makes no such claim.
A moving dot is a far stronger implication than a static line."* It was fixed so a
particle draws **only on the selected node's edges, running away from the reader**, and
never along the time axis.

That rule currently governs a fallback. **Making the full graph primary promotes it to
the default surface every reader sees.** Re-read it before touching the renderer, and do
not let a refactor restore `e.pair.flip` as a particle steer.

## 5. The patents tab: approved, and the mockup is signed off

Stewart answered all four questions on `notes/PATENTS-TAB-MOCKUP-2026-08-29.md` §5:

| | answer |
|---|---|
| 1. Comparison-led shape? | "for now this is fine" |
| 2. Spine fold at 1366? | "for now this is fine" |
| 3. Observables on this tab? | Reference how the patents pertain to them here, **and reuse the five observables elsewhere** — he suggested a craft-types surface, "call it observables or something" |
| 4. Drawings? | "Thumbnails I think. Do whatever you think would look best." |

**Build sources are in `notes/design-2026-08-29-patents-tab/`**: three `.dc.html`
artboards, `canvas.json`, and a 1:1 PNG of each at 1366 / 1920 / 2560. Canvas:
https://claude.ai/code/artifact/55c66b23-1605-4d6c-a8c8-b17db470c400

Every value in them is lifted from `l0_patches.py`, not eyeballed: 22px chip, 25px
button, 44px selection bar, 396px rail, the text ramp, the three accents.

**Suggested data route**, not yet built: an authored `research/patents-view.json` on the
`data/l0-highlights.json` precedent (authored editorial data, gate-checked), emitted into
the page the way `L0DATA` is, so `viewPatents(v)` stays a renderer and the content stays
checkable. Do not hand-type the content into `l0_patches.py`.

## 6. The FOIA layer: integrate, do not just store

Stewart: *"The FOIA will have to happen way later but keep them there and ready. In fact
integrate them into the board somehow."*

`notes/FOIA-LETTERS-2026-08-29.md` has 17 filing-ready letters, generated from
`notes/REQUEST-QUEUE.md` so the two cannot drift. **The integration is already latent in
the data**: every F-section names the nodes and the numbered open questions it would
close — F1 alone closes fourteen across eight nodes.

So the natural shape is a node -> request link: a dossier showing "the record that would
close this open question is F1, NARA, not yet filed." That makes the queue part of the
argument instead of a document beside it. **Not designed yet.** Ask Design if it needs a
surface of its own.

## 7. Should Design be asked?

**Yes, for the inversion — and this is the one worth spending a Design cycle on.** The
packed layout was Design's spec, built to it, with 30 canvas assertions behind it. Making
it a secondary tab and promoting the inherited renderer reverses that decision. Design
should at least see it, and the motion rule in §4 is theirs.

The patents tab does **not** need Design: Stewart has signed off the mockup.

## 8. State as of this handoff

`master` at `e04b705`. Everything below is pushed and CI green.

| | |
|---|---|
| PRs #12 and #13 | merged |
| Production | deployed, verified, `the-program-zxz.pages.dev` |
| `<title>` fix | committed, **not yet deployed** — rides with the next deploy |
| Link sweep | zero dead citations across 1,350 URLs |
| Elizondo testimony | read; does NOT state the five observables |
| ISOO seal | found on a .gov original, rejected on pixels, flagged for Stewart |
| Image register | 13, at its ceiling |

**Nothing in this handoff has been started.** All three builds — the inversion, the
patents tab, the FOIA layer — are unbuilt.
