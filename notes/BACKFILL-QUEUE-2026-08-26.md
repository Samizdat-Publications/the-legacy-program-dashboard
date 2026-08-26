# Auditing the backfill queue against the data instead of against the queue

26 August 2026.

## What the queue is for

`data/l0-layout-model.json` carries a `gaps` array: every field the design reads that the
data does not yet supply, with where to pull it from. It is the mechanism by which the
board degrades honestly rather than guessing — a field that is absent is a **named task**,
not a silent hole. `verify.py` guards it.

## What was wrong with it

**The check only ever asserted one direction.** It asked whether every missing field was
named in the queue. It never asked whether a **named field was still missing**.

So when the pipeline started supplying a field, the row stayed, and the check went on
passing — because the row was present, which was all it looked for. Audited row by row
against the data:

| row | data says | verdict |
|---|---|---|
| `via[]` | 109 of 109 `kind: shared` edges carry the id array | **stale** |
| `members[]` | 110 of 110 carry full member records | **stale** |
| `C / A / D` | 110 of 110 | **stale** |
| `members direct/routed` | 0 of 110 on the model | open — and fixable in code |
| `dateEnd` | 46 of 110 arrive, as `y1` | row was **wrong about the cause** |
| `denial a/b`, `denialKind` | 0 of 110 | open, research |
| `photo` | 0 of 110 | open, deliberately |
| `short ≤ 37` | 64 of 110 conform | open, authoring |

**A stale backfill row is not harmless.** It is a standing instruction to redo finished
work, and it makes the file and the data disagree — the same drift class the row-shape half
of the check was written to catch.

## The one real bug underneath it

The `dateEnd` row said the field was not carried. It is. What was actually broken was one
line in `normaliseCurrent`:

```js
roles: n.roles || [], y0: yearOf(n.dateStart), span: 0,
```

**`span: 0` — the literal**, while `normaliseLegacy`, two hundred lines further down,
computed the same field properly from the same pair of years:

```js
span: (ys != null && ye != null && ye > ys) ? ye - ys : 0,
```

So the row's own stated purpose — *"brief question 2: how many nodes could carry an extent
at all"* — had an answer the whole time, and the pipeline was reporting **0** to it.

**It is 24.** `yankee-blue` runs 1980–2023. AAWSAP 2007–2012. KONA BLUE 2011–2012. ADAM
Research Project 2018–2021.

A hardcoded zero is indistinguishable from a measured one. That is CLAUDE.md §5's rule
about checks, applied to data: `canvasInk` reported zero ink on a visibly drawing canvas,
and `span` reported zero extent on a board with 24 dated programmes.

**And I got this wrong once on the way in.** I first measured `dateEnd` on the model, found
0 of 110, and said `build_l0_layout.mjs` was dropping it. It was not — the field is
projected as `y1` and 46 arrive. Measuring a field by the name it has upstream, in a stage
that renames it, is the same error as reading one artifact and inferring about another.

## What changed

- `span` computed from `y0`/`y1` rather than hardcoded. 24 nodes gain a real extent.
- `membersDirect` / `membersRouted` projected through — the extract carried both counts and
  `normaliseCurrent` flattened them into `memberCount`.
- Three stale rows retired, with the retirement recorded in the file rather than silently
  deleted.
- The `dateEnd` row rewritten as `dateEnd coverage`: what is left is research, not
  plumbing, and 64 nodes having no end year for a programme never acknowledged to have
  ended is a finding rather than a hole.

## And the check asserts both directions now

Plus a harness change: **a check may carry several poisons, and every one must be
rejected.** One poison per check is only enough when the check asserts one thing. This one
asserts two opposite things, and a single poison would leave whichever half it did not
touch untested — which is exactly how the second half came to be missing.

Demonstrated: adding a no-op to the poison list makes the runner report
`did NOT reject poisoned input — this check is dead`.

| poison | direction |
|---|---|
| drop the `denialKind` row | a withheld field with no row naming it |
| append a `C / A / D` row | a row naming work the data has already done |
