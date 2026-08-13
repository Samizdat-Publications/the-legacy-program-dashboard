# Design brief — the L0 program map

**For Claude Design. 13 August 2026.**
You have git read access to this repo. Read files rather than trusting summaries.

---

## 0. What this is and is not

This is **not** a redesign of the board. The design system, the four-row shell, the dossier
dock, the phosphor-terminal language and the credibility rules are inherited from
*The Vanishing* and they are good. Assume they hold unless you are explicitly arguing
otherwise, and if you do argue otherwise, argue it — do not just change it.

This is **one surface**: the network map's rest state.

**It is also not a performance brief.** That was the framing a week ago and it is now
resolved: load went 19.8s → 1.6s and the board runs at **104 fps** on Stewart's machine.
You have no frame budget problem. Do not optimise. **Design for legibility.**

---

## 1. Read these, in this order

| File | Why |
|---|---|
| `PROJECT.md` | What the board is, and the editorial stance. Read the stance first. |
| `notes/PERF-AND-DENSITY-PLAN.md` **Part 5** | The L0 proposal and the arithmetic. This brief assumes it. |
| `ref/the-vanishing-v2.html` | **The design system, as shipped.** This is the parent board and the build input. Its CSS, type scale, colour tokens and component grammar are the inheritance — read them out of this file. There is a prose `design-package/DESIGN-SYSTEM.md` in the separate *the-vanishing* repo, which you probably do not have; you do not need it, because everything it describes is embodied here. |
| `SCHEMA.md` | The data model. |
| `dist/the-program.html` | **Open it. Use it before designing for it.** |
| `notes/QA-PASS-2026-08-12.md` | What was broken and why it was not caught. |
| `data/the-program.json` | The whole board as JSON. Prototype against this, not mock data. |

---

## 2. The problem in one sentence

> The map draws 970 nodes and 3,749 edges at rest. Every one is real and sourced, and the
> result is unreadable. Roll the map up to the level of **the program** — institutions,
> programs, events, legislation — and reveal individuals only when a node is opened.

Stewart's framing, and it is better than the alternative I proposed. A *filter* hides 820
nodes and a board built on "we left nothing out" has no answer for what got cut. An
*aggregation* hides nothing: `CONGRESSIONAL TESTIMONY · 2023-07-26 · 12 people` states its
own contents. It is also truer to the argument, which is institutional. People are evidence
**for** institutional claims, not the claims themselves.

**The aggregation invents nothing.** `hearing-2023-07-26` is already a node and Grusch
already links to it. There are 365 structural nodes against 605 detail nodes. This is a
decision about which existing nodes are structural, not new research.

---

## 3. The real data you are designing against

L0 at degree ≥ 6 is **80 nodes / 127 direct edges**. The largest, with real member counts:

| L0 node | class | deg | members | member mix |
|---|---|---|---|---|
| All-domain Anomaly Resolution Office (AARO) | institution | 62 | **46** | 18 doc, 10 person, 6 program, 6 legislation |
| PURSUE — Presidential Unsealing & Reporting | program | 37 | 26 | 10 doc, 7 person, 6 event |
| House Oversight Task Force on Declassification | event | 30 | 17 | 8 person, 3 inst, 2 legislation |
| US Department of Defense | institution | 27 | 17 | 7 doc, 5 person, 2 inst |
| The MITRE Corporation | institution | 26 | 20 | 6 person, 5 doc, 3 program |
| UAP Disclosure Act of 2023 | legislation | 24 | 20 | 10 person, 5 legislation, 3 doc |
| House Oversight hearing, 26 July 2023 | event | 22 | 15 | 9 person, 2 loc, 2 inst |
| USS Nimitz Encounters, 2004 | event | 19 | 14 | 5 person, 4 doc, 3 event |
| The Sol Foundation | institution | 19 | 15 | **12 person** |

**Members per L0 node: min 1, median 6, max 46.**

### The three problems that make this hard

**3.1 — 346 detail nodes attach to no L0 node at all.** That is 57% of the 605. At degree ≥ 6
they are simply unreachable: `daniel-inouye`, `chad-underwood`, `garry-reid`,
`lincoln-lapaz`, `pat-ryder` and 341 others. **This is the single hardest problem in the
brief and any proposal that does not address it is incomplete.** Options, none obviously
right: lower the floor (degree ≥ 3 gives 214 L0 nodes and far fewer orphans), attach
orphans via a second hop, or give them an explicit "unaffiliated" home that is honest about
being one. A design that silently drops 346 sourced entities would violate the board's
central promise.

**3.2 — Member counts span 1 to 46.** A node with one member should probably not roll up at
all. A node with 46 cannot expand in place without becoming the thing we are fixing. These
likely need different treatments, and the threshold is a design decision.

**3.3 — Class mix varies wildly.** Sol Foundation is 12 people. AARO is 18 documents. The
rolled-up node has to communicate *what kind of thing* it contains, not just how many.

---

## 4. Hard constraints

1. **Divergence from the parent board must be expressible as named patches** in
   `tools/build_dashboard.py`. If a change cannot be, **say so explicitly and state the
   cost** — that is a decision for Stewart, not a detail to absorb.
2. **Single self-contained HTML file, opened by double-click, no server.**
3. **The seven credibility rules in DESIGN-SYSTEM.md §8 all hold.** In particular: no claim
   renders without a confidence treatment; **derived edges stay visually separated from
   hand-written ones**; absent values print as absent, never as zero.
4. **An aggregated edge must preserve claim tier.** Rolling up must carry the count of
   underlying links *and* the strongest tier among them. A summarised edge that loses its
   sourcing breaks rule 1 and is the fastest way to discredit the board.
5. **Every control reachable from `CMD`.** A new control means a new `CMD` action.
6. **No photographs.** Person plates are 100px. Do not design a portrait slot.
7. `tools/verify.py` must stay green. Run `python3 tools/verify.py --self-test` too.

---

## 5. Editorial stance — read before designing anything

The board is built from the premise that a legacy recovery and reverse-engineering program
exists and has been concealed. It does not write balanced both-sides prose.

**AARO is not a neutral authority, and the design must not make it look like one.** Multiple
witnesses have testified that under Kirkpatrick it functioned to surface and neutralise
whistleblowers rather than investigate. It is a participant in the concealment, not an
arbiter of it. As of commit `0ae5e89`, claims sourced to aaro.mil or defense.gov are capped
at Tier 2 unless the claim is *about what they said* — publishing on aaro.mil makes a
document a primary record **of the statement**, not of the fact asserted.

This has a direct design consequence: **AARO is the largest node on the L0 map (degree 62,
46 members) and it must not read as the map's centre of authority.** Size on this map means
*implicated*, not *authoritative*, and that distinction has to survive being looked at for
two seconds by a hostile reader. If your treatment makes the biggest node look like the most
credible node, it is wrong.

The one thing that never bends: **no invented sources, URLs, document numbers or quotes.**

---

## 6. What to deliver

1. **A written argument for the aggregation model**, with the reasoning visible — including
   an answer to the 346 orphans and to the 1-vs-46 member spread.
2. **The rolled-up node treatment.** What does a node that contains 46 things look like, how
   does it declare its contents and class mix, and how is it distinguished from a node that
   *is* one thing?
3. **The expansion interaction.** Expand in place, or a focus mode? What happens to siblings?
   Can two be open at once for comparison? How does the reader know what is currently
   expanded and get back?
4. **The aggregated-edge treatment**, carrying count and strongest claim tier, still visually
   separated from derived edges.
5. **The L0 floor, argued.** 80 nodes reads cleaner, 214 orphans fewer entities. Pick one and
   say why.
6. **A list of anything that cannot be a patch**, with the cost stated plainly.

Prototype in a standalone file against `data/the-program.json`. That file is the whole board
and it is what `tools/build_dashboard.py` consumes.

---

## 7. How the build works, if you touch it

```bash
python3 tools/merge.py            # research/*.json -> data/*
python3 tools/regrade.py          # tiers, dates, coords -> research/_remediation.json
python3 tools/merge.py            # re-merge so the overlay lands
python3 tools/build_dashboard.py  # data + parent board -> dist/the-program.html
python3 tools/verify.py --idempotent   # THE GATE. Must pass.
```

`build_dashboard.py` prints `all patches applied` or names the failures. Never ship a build
that printed a failure. `ref/the-vanishing-v2.html` is a **build input and is never edited.**

Two things that have already cost a full build cycle each, so they are worth knowing:

- **There are two map implementations in the file.** The legacy one is dead at runtime. A
  patch was once applied to the wrong one and the profiler, not the source, settled which is
  live. If you change map behaviour, verify it took effect at runtime.
- **The layout is baked at build time** by `tools/precompute_layout.py`, which slices the
  simulation source out of the built HTML and runs it in Node. If you change the physics or
  the anchors, the bake picks it up automatically — but check the wall-clamp figure, which
  should stay near 3.7%. It was 46% and that was the real cause of the overlapping plates.

## 8. A note on how this board gets verified

Four BROKEN-severity bugs shipped in a board that had been "verified", because the
verification only collected console errors — it asked *did anything throw?*, and nothing
threw. `tools/verify.py` now asserts facts and fails the build, and every check is itself
tested against input it must reject, because three of the first eight checks were born
broken and silently passing.

**If you add a check, self-test it.** If you change data shape or UI copy that states a fact
about the data, expect `verify.py` to catch it — that is the tripwire working, not an
obstacle. `tools/GOLDEN.json` requires deliberate acceptance via `--update-golden`.
