# The Legacy Program Dashboard

A network board mapping the legacy UAP recovery and reverse-engineering program and the
modern disclosure movement, 1944–2026.

**968 nodes · 279 people · 2,160 hand-written sourced links · 4,431 tiered claims ·
2,825 unique source URLs · 858 timeline events · 82 years.**

*Counts as of 24 August 2026. They move every research pass — regenerate rather than
trusting them. See `CLAUDE.md` for how.*

Open `dist/the-program.html` by double-clicking it. No server, no build step, no
dependencies. It is a single self-contained file.

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

**59% of 4,431 claims rest on a primary record.** That number is the product. The design's
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
dist/the-program.html    the board — open this
data/                    the merged dataset (the-program.json is the whole board)
research/                per-domain source research
tools/                   the build pipeline and the verification gate
notes/                   research log, QA reports, design briefs
ref/                     the parent board — a BUILD INPUT, never edited
```

## Building

```bash
python3 tools/merge.py            # research/*.json -> data/*
python3 tools/regrade.py          # tiers, dates, coordinates -> research/_remediation.json
python3 tools/merge.py            # re-merge so the overlay lands
python3 tools/build_dashboard.py  # data + parent board -> dist/the-program.html
python3 tools/verify.py --idempotent
```

`verify.py` passing is the definition of shippable. It asserts facts and fails the build,
and **every check is itself tested** — `--self-test` feeds each one input it must reject.
Three of the first eight checks were born broken and silently passing, which is the whole
reason that rule exists.

## Provenance

Built on the engine, schema and design system of *The Vanishing*, a companion board with a
different subject. `ref/the-vanishing-v2.html` is a build input and is never edited; all
divergence lives in `tools/build_dashboard.py` as named patches that fail loudly by name.

## Licence

Not yet chosen. The research is compiled from public records; the source URLs are on the
board and in `data/the-program.json`.
