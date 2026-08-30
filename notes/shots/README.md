# Screenshot history

**One dated folder per session that changed something visible.** Stewart, 30 August 2026:
*"keep a history of our progress by keeping the screenshots as we go."*

## Why this exists, and why it did not before

`dist/shots/` is in `.gitignore`, and `tools/look.js` and `tools/walk.js` both write there.
So **every screenshot this project has ever taken was thrown away** — including the ones
that found the four defects on 26 August and the two that `test_packed_layout.js` was
written to guard. The finding survived in a note; the picture did not.

That is the wrong way round for this board specifically. `CLAUDE.md` §5 says it four times:
reading the source is not verification, and for anything visual the pixels are the evidence.
A note saying "the era heads were printing under the control row" is a claim. The capture is
the proof, and it is what makes a later "is this still true?" answerable in ten seconds
instead of a rebuild.

## The convention

```
notes/shots/YYYY-MM-DD/<n>-<surface>.png
```

- **Dated, not versioned.** The date is what lets a reader line a capture up against the
  handoff and the commit from the same day.
- **1920×1080 at `deviceScaleFactor: 1`.** Not 2. `CLAUDE.md` §3 records why: a 2× capture
  viewed scaled-to-fit shows small text *larger* than a real monitor does, and this board has
  8px labels whose legibility is a real question. 1× is the honest representation.
- **Numbered in reading order**, so the folder is a tour rather than a pile.
- **Keep the old ones.** A before is worth as much as an after; that is the whole point of a
  history. Do not tidy a previous session's folder away.

Roughly 3MB per session at five surfaces. The repo already carries a 15MB built artifact and
3MB of patent drawings, so this is not the binding constraint — but do not capture every
state, only the ones a later session would want to compare against.

## Sessions

| date | what it shows |
|---|---|
| `2026-08-30` | The map inversion, the patents tab and the FOIA layer, as built. The first captures ever kept. `2-program-map.png` is also the after-shot for the gutter fix: RESEARCH and OVERSIGHT read in full, where they had rendered as "SEARCH" and "ERSIGHT". |
