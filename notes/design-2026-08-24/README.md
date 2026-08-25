# Handoff — L0 positional layout

Read `DESIGN-RESPONSE-LAYOUT-2026-08-24.md` first. It is the whole argument.

## Contents

| file | what it is |
|---|---|
| `DESIGN-RESPONSE-LAYOUT-2026-08-24.md` | the design response: layout, edge budget, channel assignment, backfill queue, checks |
| `tools/build_l0_layout.mjs` | the generator. Reads design-extract.json (+ the legacy inputs if present) and emits the model. Every published figure comes from its output |
| `data/l0-layout-model.json` | the emitted model, both datasets. 349KB, under the read cap by design |
| `L0 Positional Layout.dc.html` | the interactive comp. Needs `data/l0-layout-model.js` beside it — regenerate with the generator |

## To run

```bash
node tools/build_l0_layout.mjs
```

Reads, all optional except the first:

    data/design-extract.json     authoritative — 110 L0 nodes
    data/l0-extract.json         legacy comparison — 96 L0 nodes
    research/dossiers/*.json     legacy roles
    research/*.json              legacy dates
    data/l0-highlights.json      the start-here editorial pass (absent -> placeholder)
    data/l0-images.json          one image per node (absent -> class letters)

Writes `data/l0-layout-model.json` and `.js`. Exits non-zero on: a node the budget
left bare, a highlight naming an id not on the map, more than 15% of the map flagged,
or a model over the ~1MB read cap.

## The three things to do next

1. **Answer the patch question** — §6. Whether a packed-cell layout can be a named
   patch against the parent board's canvas renderer. This is the one item that could
   change the approach.
2. **Work the backfill queue** — §4. Seven fields, each with what to pull and where from.
   `C`/`A`/`D` and `via[]` buy the most for the least.
3. **Write `data/l0-highlights.json`** — the editorial pass on which nodes are worth
   opening. The design language is built and waiting; the judgement is not a design
   decision.
