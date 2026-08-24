# Design brief — make position mean something

**For:** Claude Design
**From:** the implementation session, 14 August 2026
**Repo:** `Samizdat-Publications/the-legacy-program-dashboard` (private, you have read access)
**Board state:** commit on `master`, 968 nodes · 110 on the map · 2,160 hand-written
sourced edges · 4,431 tiered claims

---

## 0. Read this first: the last handoff's figures did not reproduce

The previous package (`design_handoff_l0_program_map`) specified a floor of degree >= 6
producing **107 L0 nodes**. Running **its own reference generator** against **the source
it named** produced **96**. The cause: `data/l0-extract.json` carried a `deg` field that
was an edge-instance count, not a degree — 94 node pairs carry more than one hand-written
edge. The generator recomputed degree correctly from distinct neighbours and carried a
comment saying it did so *precisely because* a stale `deg` "silently changes the L0 set."
The published figures used the stale field anyway.

Nothing was wrong with the design. The numbers describing it were wrong, and a worked
example in the README (`usaf`) referred to a node that the correct floor removes from the
map entirely.

**So the one process ask: every figure you publish must be reproducible by a generator
you ship, run against a file that exists in the repo, and the two must agree.** If they
disagree, say which is authoritative. This cost a full session to unpick.

---

## 1. What the problem actually is

The map draws 110 nodes and 313 edges. Stewart's assessment, and I agree: *"way too busy
... no opportunity for discovery, nothing visually identifying what the important
connections are."*

**The diagnosis is not node count. It is that position carries no information.** X and Y
are force-layout output — physics. Every node is the same size by deliberate rule (see
§4), arrives in no order, and sits in an undifferentiated field. 313 orthogonal traces
crossing that field is the symptom.

Two dimensions exist in the data and are currently unused.

---

## 2. The measured distributions — build on these, not on assumptions

All figures below are from `data/l0-model.json` at the current commit and reproduce with
`python3 tools/build_l0.py`.

**Era.** 105 of 110 L0 nodes carry a `dateStart`.

```
1940-1969    21
1970-1999    24
2000-2016    16
2017-2026    44        <- 40% of the map is the last decade
```

**Function.** Every dossier carries a `roles` array. These are **tags, not a partition** —
they overlap heavily, so a banded layout needs a rule for picking a primary.

```
concealment          79        custody              48        funding              27
disclosure           74        research             46        reverse-engineering  17
oversight            68                                       retrieval            10
```

**Cluster.** The inherited dimension, and it is not usable as-is: **52 of 110 are
`other`**, including AARO. The previous design correctly gave up on cluster wells for
this reason.

```
other 52 · oversight 18 · research 14 · ic 10 · witness 6 · contractor 3 · legacy 3 · media 2 · ffrdc 2
```

**Degree.** min 6 · median 10 · max 64. **16 nodes sit at exactly 6**; 28 at >= 15.

**Edge tiers — this kills the obvious idea.** Filtering by tier does not thin the map:

```
direct edges      204   tier 1: 134   tier 2: 39   tier 3: 36
summarised edges  109   tier 1: 108   tier 2: 1
```

242 of 313 edges are Tier 1. **An edge budget has to be built on something other than
tier.**

---

## 3. What we are asking for

### A. A layout where position means something

Our working hypothesis is **X = era, Y = functional band**, so a node's location tells a
reader *when* and *what role* before they read a word. We are not attached to it. If
there is a better organising principle in this data, take it.

Specific questions we cannot answer well:

1. **How do you pick a primary function** when 79 nodes are tagged `concealment` and 74
   `disclosure` and most carry both? Is the answer a rule, a manual pass over 110 nodes,
   or a different set of bands entirely?
2. **What happens to a node that spans eras?** AAWSAP runs 2008-2012 but its
   consequences run to 2024. Is it placed at its start, its centre, or drawn as an extent?
3. **How do you label bands without stealing the space you just freed?**
4. **How do you stop it reading as a Gantt chart?** This is a network, and the edges are
   the argument. A time axis must not imply the edges are chronological.
5. **The 2017-2026 band holds 40% of the map.** Even spacing wastes three quarters of the
   width. Do you compress early eras, or is uneven density itself the finding?

### B. An edge budget for the rest state

313 edges at rest is too many and tier will not reduce it (see §2). Options we see:
draw only edges between high-degree nodes; draw only edges that cross a band or an era;
draw a spine and reveal the rest on selection. **Tell us the rule and why.**

Note one measured constraint: the previous package asserted shared-member counts run 2-5,
so a five-tick vocabulary fits with "no overflow and no numeral case". **That is no longer
true** — `dia~dird-series` now shares 18 members, and the renderer has a numeral fallback
(divergence D6). Whatever you specify has to survive counts up to 18.

---

## 4. Constraints that do not bend

**Size must not encode importance.** The previous package established this and it stands:
size reads as authority, and the largest node is AARO, which this board treats as
**implicated, not authoritative**. AARO is the most connected node because it genuinely
is central; it does not get to look like the most credible one. Any proposal that scales
a node by member count, degree or claim count is rejected on arrival. **Position is
available. Size is not.**

**AARO is not a neutral source.** Claims sourced to aaro.mil or defense.gov cap at Tier 2
unless the claim is about *what they said*.

**No invented sources, URLs, document numbers or quotes.** Ever, anywhere, including in
mockup copy. If you need placeholder text in a comp, mark it clearly as placeholder.

**The shell is inherited from *The Vanishing* and is not in scope**: four-row layout, left
rail, dossier dock, analyst bar, phosphor-terminal language, the seven credibility rules.
Two exceptions we have already made and would keep: tier now takes the dash channel on
the map (D1), and denial edges are drawn directional (D3).

---

## 5. What is already being built, so you do not duplicate it

In flight this session, landing before you respond:

- **An entry surface** with six curated ways in: Follow the money · The custody chain ·
  Who denied what · The legal mechanism · The foreign counter-examples · Start from a
  witness. Each seeds the map filtered. Verified against the data — the six paths return
  7, 38, 36, 10, 11 and 7 nodes respectively.
- **Focus on select**: clicking a node dims to its one-hop neighbourhood.
- Node click now loads the dossier (it did not), KPI cells filter, both panes collapse.

**Please design A and B assuming those exist.** If the entry surface changes what the
rest state needs to do, say so.

---

## 6. What you have access to

```
data/l0-model.json      the map model: 110 nodes with baked coords, full dossiers,
                        4,320 connection rows, the authority layer, both registers
data/the-program.json   the full board (6MB+)
tools/build_l0.py       the model + layout bake. Read the DEGREE section at the top.
tools/l0_patches.py     the renderer, as injected JS/CSS
notes/L0-IMPLEMENTATION-2026-08-13.md   everything done and every mistake made
notes/ANALYST-PASS-2026-08-14.md        what the board found when an agent traversed it
```

`dist/the-program.html` is 13MB and will not render on GitHub. Clone and open it.

---

## 7. The three failure modes this board keeps hitting

Offered so you can design against them rather than rediscover them.

1. **A check that always passes is indistinguishable from a broken one.** `canvasInk`
   reported zero ink on a visibly drawing canvas and had never once fired. Six of six new
   checks this session were born broken and silently passing.
2. **Reading the source is not verification.** Three times this session a check agreed
   with the implementation and a screenshot disagreed. Most recently the dossier panel
   clipped every line at both edges while a programmatic overflow test returned zero,
   because the panel fitted its element and the element did not fit its grid track.
3. **Two agents agreeing is not corroboration when they share a method.** Two independent
   research passes both "corrected" a statutory citation that was already right.

If your package includes checks, state for each one the input it must reject.
