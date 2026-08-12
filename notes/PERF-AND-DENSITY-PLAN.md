# Load time and density — measurement, root cause, plan

**12 August 2026.** Written after profiling the shipped board, not after reading it.

---

## Part 1 — why the process missed four BROKEN bugs

The board had been "verified". The verification was `shoot.js`: open every view, collect
console errors, report zero. That answers one question — *did anything throw?* — and every
defect found on 12 August answered it "no":

| defect | threw? | rendered? | correct? |
|---|---|---|---|
| 35 dates nulled on every rebuild | no | yes | **no** |
| five people on the board twice | no | yes | **no** |
| thirteen plates reading `JR., J.` | no | yes | **no** |
| DETAIL panel stating the wrong class count | no | yes | **no** |

**A board can be entirely wrong and entirely quiet.** No check asserted that anything was
*true*. That is the whole root cause, and it is not a diligence problem — no amount of
careful looking reliably catches 35 nulls inside a 6.8 MB file.

There was a second, nastier failure. `shoot.js` had one check that could in principle catch
something real: `canvasInk`, meant to detect a blank map. It reported `canvasInk: 0` on a
canvas that was visibly drawing, because the renderer is WebGL and `getImageData` returns
empty without `preserveDrawingBuffer`. **It had never once fired.** A check that always
passes and a check that is broken are indistinguishable from the outside, and the broken one
is worse than nothing because it reads as evidence.

### The gate

`tools/verify.py`. Two rules, both learned from the above:

1. **Every check asserts a fact and exits non-zero when it is false.** Reporting is not
   verifying.
2. **Every check is itself tested.** `--self-test` feeds each check input it must reject.
   A check that cannot be shown to fail is not evidence.

Rule 2 paid for itself on first run: the UI-copy check silently no-opped and the self-test
caught it. The `built file contains the data` check then failed twice for two different
wrong reasons (a count heuristic that also matched timeline ids; a pattern that only knew
the person serialization) before it was right. **Three of eight checks were born broken.**
That is the expected rate, and it is exactly why canvasInk sat dead.

Current checks — all self-tested, all passing:

```
ids are canonical                          duplicate-person bug
no label is its own id                     the slug-as-name symptom
person plate names are meaningful          the JR., J. bug
no dangling references                     edges/timeline pointing at nothing
claim tiers valid and Tier 1 is sourced    the credibility rule that matters most
UI copy agrees with the data               the "Five entity classes" bug
built file contains the data it claims     a build that silently drops records
counts match the golden manifest           drift tripwire; --update-golden to accept
pipeline is idempotent (--idempotent)      the lost-dates bug, and its whole class
```

The idempotency check was regression-tested by reverting the fix: it correctly reports
`pipeline is NOT idempotent` and names the two differing hashes. It catches a *class* of
bug — any pass that reads its own output back in — not one instance.

**New rule: `verify.py` passing is the definition of shippable.** `shoot.js` is demoted to
what it actually is — a screenshotter. Its `canvasInk` field should be deleted rather than
fixed; a check nobody can trust should not be in the output.

### Still not covered, honestly

`verify.py` checks data and copy. It cannot see layout. Plate overlap, clipping, and
anything about how the thing looks still need eyes or a pixel-diff harness. That gap is
real and it is where the remaining known defects live.

---

## Part 2 — where the load time actually goes

Profiled with the V8 sampling profiler over a cold load, 1600×1000, headless. Your machine
is slower again: WebGPU, a larger viewport, more earned plates.

```
wall load 19,779 ms

 51.7%  13,356ms  step              force-layout integration
 23.7%   6,118ms  (program)         V8 parse + compile of the 6.84 MB file
 13.7%   3,538ms  build             layout driver
  6.4%   1,648ms  applyRepulsion    Barnes-Hut traversal
  1.2%     301ms  garbage collector
  1.1%     285ms  insert            quadtree build
  0.5%     127ms  quadFor
  0.3%      80ms  drawParticle2D    ← all rendering, together, is under 1%
```

**Layout is ~60%. Parsing the file is ~24%. Drawing is under 1%.**

Two things follow, and both contradict what I would have guessed:

- **Rendering is not the load problem.** It is the *frame rate* problem (5–8 fps), but at
  load it is noise. Cutting nodes drawn will not meaningfully fix the wait on its own.
- **Barnes-Hut is already implemented** and the layout is O(n log n). It is still 15 s
  because it runs **900 integration steps over 970 nodes before the first paint**. The cost
  is the step count, not the algorithm.

### An incidental finding the profiler settled

There are two `build()` functions in the file — the legacy map and the live one. The
handoff warns about this and says the legacy one is dead code. The profile shows
`build @L106461` consuming time, which is the **900-step** one. The patch in
`build_dashboard.py` that raised the step count 900 → 1600 was applied to the **other**,
dead implementation.

Nobody was going to catch that by reading. One profiling run settled it. Worth generalising:
**measure before optimising, and measure before believing a comment.**

---

## Part 3 — the plan, in payoff order

### 1. Precompute the layout at build time — removes ~60%

Run the force simulation in `build_dashboard.py` and bake final `x, y` into every node. The
board opens already settled and runs **zero** steps before first paint.

This is not only a speed fix. A precomputed layout is **stable** — the map looks the same
every time you open it, on every machine. For a research instrument that is a credibility
property: positions become citable, screenshots stay valid, and "the node in the upper left"
means something across sessions. The current board rearranges itself on every load.

Resize still needs relaxation, but that is 220 steps against an already-settled graph, not
900 from a cold start.

*Risk:* the Python and JS force implementations must agree, or the baked layout will not
match what the JS reflow does on resize. Mitigation: port the JS `step()` verbatim and add a
verify check that a JS reflow of the baked layout moves no node more than N px.

**Estimated: 19.8 s → ~4.5 s.**

### 2. Defer the dossier payload — attacks most of the remaining 24%

6.84 MB is parsed as JavaScript object literals before anything runs. The map needs about
200 KB of it: id, label, class, tier, degree, x, y. The other ~6.6 MB is narrative, claims
and sources — needed only when a dossier opens.

Keep the single-file constraint. Emit the heavy fields as **one JSON string literal** and
`JSON.parse` it on first dossier open. V8 parses a string literal far faster than the
equivalent object literal, and the parse cost moves off the critical path entirely.

**Estimated: ~4.5 s → ~1.5 s.** Combined with (1), roughly a 13× improvement.

### 3. Open on a subgraph — fixes the tangle and the frame rate

This is the design question, not the performance one, and it is addressed below.

### 4. Viewport culling and level-of-detail — frame rate only

Do not draw what is off-screen. Do not draw plates below a zoom threshold. This is the fps
fix; it is worth doing after 1–3 and not before, because 1–3 change what "at rest" means.

---

## Part 4 — what the board should open on

The brief asks whether progressive disclosure should key off era, cluster, or claim tier
rather than degree, and whether the map should open focused on something.

**The case against degree.** Degree is a proxy for importance and on this graph it is a bad
one. It surfaces `aaro` and `dod` — hubs that touch everything and therefore say little —
and buries a contractor named once, in sworn testimony, as having held material. The second
node is the more load-bearing one and degree ranks it near the bottom. A density slider
inherits the same flaw and additionally asks the reader to tune a number they have no basis
for choosing.

**Proposal: open on the argument, then let the reader add strata.**

Rest state = the **spine**: every node on a `custody` edge, plus every node holding a
`denial` edge against one of those, plus the oversight nodes that legislated on them. That
is the thesis in one picture — *here is the chain of custody, here is who denied it, here is
who finally got to ask* — and it is roughly 100–150 nodes, which is legible.

Then additive strata, each a labelled control with its own count:

- `+ witness chain` — the testimony layer
- `+ research & media` — who investigated
- `+ everything (970)` — explicitly labelled as the full corpus, with its cost stated

Orthogonally, an **era band** (1944–69 / 1970–2000 / 2001–16 / 2017–now), because 82 years
is the board's other axis and the 79-year oversight gap is its strongest structural claim.

Each stratum is a *question*, not a threshold. That is the difference from a slider, and it
is why this survives the reader asking "why am I looking at these nodes and not those."

Alternatives worth weighing, and I do not think this is obvious:

- **Open on the witness chain** — more immediately human, more legible to a newcomer, but it
  leads with testimony, which is the weaker evidence tier. It would make the board look more
  like advocacy and less like an audit.
- **Open on Tier A only (146 nodes)** — cheap to implement, defensible, but tier is a
  computed composite; opening on it makes the board's own scoring the first thing you see
  rather than the evidence.
- **Open on the current era, 2017–now** — the live fight, best for a returning reader,
  worst for the argument that this is 82 years old.

---

## Sequencing

1. `verify.py` in the loop — **done**
2. Precompute the layout — the 60%, no design decisions needed
3. Defer the dossier payload — the 24%, no design decisions needed
4. Entry view + strata — needs the decision above
5. Culling and LOD — frame rate
6. Plate collision — folds into 4, since it is a density problem first

2 and 3 are pure engineering and can start immediately. They are also independent of
whatever is decided about 4.
