# The patents tab, built — 29 August 2026

Built to `notes/PATENTS-TAB-MOCKUP-2026-08-29.md`, which Stewart signed off with all four
questions in its §5 answered. It is the third view in the rail, after the two maps.

---

## 1. The content is data, and that was the requirement

Nothing on this tab is typed into a renderer. Two authored files:

| file | what | emitted as |
|---|---|---|
| `research/patents-view.json` | filings, the two prosecution lanes, four quotations, the file wrapper, the maintenance-fee finding, the drawings, open questions | `PATDATA` |
| `research/observables-view.json` | the five observables, their published wordings, the PAX 205 mapping, the recorded gaps | `OBSDATA` |

`tools/patents_patches.py` holds a renderer, a stylesheet and four string patches, on the
`data/l0-highlights.json` precedent. The reason is §2 of `CLAUDE.md`: **content typed into
a renderer cannot be gate-checked**, and the one rule that never bends on this board is
about content.

**The observables are a separate file because Stewart asked for them to be reusable.** His
answer to question 3 was to reference how the patents pertain to them here "and reuse the
five observables elsewhere ... call it observables or something". A craft-types surface
built later reads `research/observables-view.json` directly. It must not have to read the
patents tab's data to find out what the five are, and two copies of a taxonomy is how the
two stop agreeing.

## 2. The mockup is a picture, and a picture is not a source

Every quotation was checked against the transcript under `research/patents/wrapper/`
before it shipped, and that check is now in the gate rather than in anyone's eye.

**Two things in the mockup did not survive the check.**

- **Its header strip reads `5 FILINGS · 2 GRANTED`. Three are granted** — US 10,135,366,
  US 10,144,532 and US 10,322,827. The tab now **derives** every figure in that strip from
  the arrays, exactly as `renderStats` derives the board strip, and prints
  `5 filings · 3 granted · 2 expired · 2 published as applications`.
- **Its rail says "Both patents lapsed".** Two of the three granted patents lapsed. The
  third, US 10,322,827, has **no maintenance-fee status on this board at all** — it is not
  established as in force, it is unchecked. That is now an open question on the tab and the
  filing card says so rather than leaving a reader to assume.

A near miss worth recording: verifying the Sheehy quotation from a shell one-liner
reported it **absent** from the letter. It is not — "beyond the state of / the possible"
is broken across a line in an 80-column transcript, and `grep -o` with a leading context
window missed it. **A check that reports a real quotation as fabricated is worse than no
check**, so the gate check flattens whitespace on both sides before the substring test.

## 3. The four gate checks, each shown failing

| check | poison |
|---|---|
| every patents-tab quotation is verbatim in the document it cites | one word changed in the Advisory Action quote — still plausible, still citing the same document, and not in it |
| no patents-tab quotation is edited by its own highlight | an emphasis phrase that does not occur in its own quotation |
| the five observables stay Tier 2, and the mapping stays separate | the taxonomy promoted to Tier 1; and the fifth row marked met, making it five of five |
| the patents tab prints what it does not have | the absent list emptied; EXPIRED asserted with no date; a status the renderer does not style |

The first is `tools/spot_check.py`'s job done for the tab's quotations. `spot_check.py` is
deliberately out of the gate because it depends on the network; **this one is in the gate
because the documents are transcribed in the repo — no network, no excuse.**

The self-test was itself verified rather than trusted: neutering one poison to a no-op
makes it report `did NOT reject poisoned input — this check is dead` and exit 1.

## 4. Two defects found by looking, neither visible to any data check

**Every quotation printed a stray box and a capital letter beside its quote marks.** The
stylesheet said `quotes:'\201C' '\201D'` and that is correct CSS. The Python module
carrying it used a **non-raw** string, so `\201` was read as a Python *octal* escape —
U+0081 — and the `C` survived as a literal. The CSS was right; the file that emitted it
was not. Both payload strings are raw now, and a runtime check asserts no C1 control
character reaches the rendered tab.

**The prosecution lane labels overprinted into a smear.** PAX 205 has ten events inside
three years and `NON-FINAL`, `ALLOWED — PRIOR ART` and `GRANTED` rendered as
`NON-ALLOWED — PRIORARTED`.

The two wrong fixes are worth naming, because both were available and both are lies:
spacing the events evenly would make the axis fiction, **and the axis is the argument** —
PAX 182 runs clean across seven years while PAX 205 is fought out inside thirteen months;
dropping labels would hide exactly the events that make the comparison.

So the dates stay put and the **labels** move. Each is given the first row on which it
clears the previous label's *measured* width — measured through `ctx.measureText` at the
face that actually resolved, because this board has been bitten by assumed monospace
metrics three times — with a leader from marker to label. Rows are assigned greedily left
to right, so the earliest event in a cluster keeps the top row and reading order stays
chronological.

`POISON=patents` returns every label to row 0, which is where they sat before the fix.
**0 overlaps honest, 14 poisoned.**

## 5. Drawings

Answer to question 4 was "thumbnails, do whatever you think would look best".

They ship as **facsimiles on their own white ground inside a frame**. Nothing is inverted,
keyed or recoloured. `research/patents/drawings/PROVENANCE.md` records that these are
document facsimiles rather than marks, and altering one makes it a different document —
the same argument `CLAUDE.md` §9 makes about seals, and the reason the ISOO seal was
rejected rather than keyed.

`PROVENANCE.md` also warns that the originals are 7112×9167 print renders, about 3MB, and
that shipping them whole would undo `notes/FIRST-PAINT-2026-08-26.md`. It says to generate
display derivatives at build time. They are generated **once and committed** instead, by
`tools/make_drawing_thumbs.mjs`, for three reasons: there is no PIL, ImageMagick or sharp
in this environment so the only resampler available is a browser; putting a browser in the
build would make `build_dashboard.py` need Chromium; and a re-encode through a canvas is
not guaranteed bit-identical run to run, which `--idempotent` would catch. **11 sheets,
130KB on disk, 174KB embedded — about 1.1% of the page.**

## 6. What it was checked against

Screenshotted and read at 1366 / 1920 / 2560, the three widths the mockup was signed off
at. No horizontal overflow at any of them; the tab scrolls vertically inside `.view`, like
every other document view.

One contrast fix came out of that pass: the Tier 3 reading under the observables table was
set at `#3b444f`, which is `bandN` — a **rule** colour, not a text colour, and below the
floor of this board's text ramp. Dimness carries the grade; it does not get to cost the
sentence. It is `#5c6672` now, the ramp's actual floor.

The honest limit is the one `CLAUDE.md` §3 already records: these are three states at
`deviceScaleFactor` 1, not every state, and the 8px `.13em` labels should be judged on a
real monitor rather than from a PNG.

## 7. Gate

Green on all ten steps including `--idempotent`. Four new verify checks, each self-tested;
eight new runtime assertions, one with a page poison.
