# The Legacy Program Dashboard

A network board mapping the legacy UAP recovery and reverse-engineering program and the
modern disclosure movement, 1944–2026.

**956 nodes · 278 people · 2,159 hand-written sourced links · 4,513 tiered claims ·
2,888 unique source URLs · 858 timeline events · 0 dead citations · 82 years.**

*Counts as of 25 August 2026. They move every research pass — regenerate rather than
trusting them: `python3 tools/state_snapshot.py`. See `CLAUDE.md` for the rest.*

The board is the app in `app/`, deployed at https://the-program-zxz.pages.dev. The
single-file shell that used to be the whole board, `dist/the-program.html`, was retired
on 25 September 2026.

---

## What it is

A research instrument, built on the premise that a legacy recovery and reverse-engineering
program exists, has existed since the 1940s, and has been deliberately concealed. The
research question is not *whether* — it is **who, where, under what authority, and paid for
how.**

Every claim on the board carries a tier:

| tier | meaning |
|---|---|
| **1** | Documented — a primary record exists |
| **2** | Sourced claim |
| **3** | Inference, with the reasoning stated |

**61% of 4,513 claims rest on a primary record.** That number is the product. The design's
job is to make it impossible to read the board without knowing which parts are documented
and which are testimony — not to make the testimony look more documented than it is.

Official denials are recorded in full and sourced, as **artifacts of the concealment
effort** rather than as counterweights. A denial is a dated, signed, attributable statement,
which makes it evidence about the denier.

Interested parties do not get to be their own best evidence: claims sourced to AARO or DoD
domains cap at Tier 2 unless the claim is *about what they said*, because publishing on
aaro.mil makes a document a primary record of the statement, not of the fact asserted.

**Nothing here is invented.** No fabricated sources, URLs, document numbers or quotes.
Unsourceable material is marked as such or stated as a Tier 3 inference with its reasoning.

## Scoring

Three axes, 0–3, **never summed** — an entity can sit at the centre of the custody chain and
be absent from the disclosure fight, and collapsing that into one number destroys the
information.

- **C** — custody proximity: how close to alleged possession of recovered material
- **A** — access level: what special access it held
- **D** — disclosure role: how central to forcing the record open

## Layout

```
app/                     the board: a Vite app, reading app/public/data/ at runtime
data/                    the merged dataset (the-program.json is the whole board)
research/                per-domain source research
tools/                   the build pipeline and the verification gate
notes/                   research log, QA reports, design briefs
```

## Building

```bash
python tools/build.py             # the whole pipeline, research/ -> app/public/data/
python tools/gate.py              # every check, the app's included
```

`verify.py` passing is the definition of shippable. It asserts facts and fails the build,
and **every check is itself tested** — `--self-test` feeds each one input it must reject.
Three of the first eight checks were born broken and silently passing, which is the whole
reason that rule exists.

## Provenance

Built on the engine, schema and design system of *The Vanishing*, a companion board with a
different subject. The first shell was that board's single file, patched; it was replaced
by the app in `app/` on 3 September 2026 and retired on 25 September 2026.

## Licence

Not yet chosen. The research is compiled from public records; the source URLs are on the
board and in `data/the-program.json`.
