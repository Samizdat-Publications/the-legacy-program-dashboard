# The FOIA layer — integrated, not stored

Stewart, 29 August 2026: *"The FOIA will have to happen way later but keep them there and
ready. In fact integrate them into the board somehow."*

---

## 1. The linkage was already in the data

Nothing had to be authored. Every letter in `notes/FOIA-LETTERS-2026-08-29.md` already
carries a line of this shape:

```
**Closes on the board.** `yankee-blue` Q0, Q4; partially Q3.
```

`Q0` and `Q4` index into that node's dossier `openQuestions`. So the integration is a
**read**, not a new dataset: `tools/build_foia_links.py` parses those lines into
`data/foia-links.json`, and the dossier draws the inverse index.

**17 requests · 42 nodes · 121 open questions · every node id resolves · every index in
range.** F1 alone names fourteen questions across eight nodes.

**The chain has no hand-kept link in it, and that is the point.** The letters are
generated from `notes/REQUEST-QUEUE.md`; the linkage is generated from the letters; the
page is built from the linkage. A hand-maintained third copy of the mapping would be a
third thing to keep in step, and this repo has already paid for that twice.

## 2. What it looks like

An open question that a request would close carries an amber chip: `F3 · OSD`. Hovering
gives the full title and the status. The section header says **"4 of 7 answerable by
request"**.

Amber because it is a **pointer** — the role the start-here flags carry — and not cyan,
which on this board means something established. Nothing here is established:

**WOULD, NOT WILL.** None of the seventeen has been filed, and the status says so on every
chip. A chip reading `F1 · NARA` with no status would read as a request in flight, which
would be a claim about the world that is not true.

## 3. The distinction the letters make, kept

The letters do not claim uniform strength. Three say something weaker in prose:

| letter | line |
|---|---|
| F3 | `` `yankee-blue` Q0, Q4; partially Q3 `` |
| F4 | `` `langley-2023-incursions` Q3, and materially advances Q6 and Q11 `` |
| F16 | `` `nimitz-2004` Q0, Q2, Q4, Q5; partially Q1 `` |

Those render as a **dashed grey chip marked "bears on"**, not an amber one. Flattening the
two would have the board assert that a request settles a question its own letter says it
only advances — and "closes" versus "bears on" is exactly the distinction this board grades
everywhere else.

## 4. The parser bug that reported success

**The first cut of `build_foia_links.py` silently dropped all four of those weaker
claims.** It matched `` `id` `` followed by a run of Q-numbers and stopped at the first
word it did not expect, so `partially Q3`, `materially advances Q6 and Q11` and
`partially Q1` were read, discarded, and reported as a clean parse:

```
17 requests · 42 nodes · 117 open questions linked
```

117 was wrong and looked right. This is `CLAUDE.md` §5 in its purest form — a pass that
succeeds while not doing its job — and it was caught only by reading the output against the
letters rather than trusting the summary line.

The rewrite splits on semicolons, treats a clause naming no id as continuing the previous
node, and **counts every `Q\d+` in the line against the number attributed**. A mismatch
raises and names the line. The count is now 121.

## 5. Two derived numbers that had to mean what they say

- **The header counts DISTINCT questions**, not links. Three of YANKEE BLUE's questions are
  named by two requests each; counting links would have the header claim more of the node's
  questions are answerable than the node has.
- **The agency comes from the letter's heading, not its postal address.** `**Send to.**`
  gives "Office of the Secretary of Defense / Joint Staff FOIA Requester Service Center
  (FOID)", which is what a letter needs and about four times what a chip can carry. The
  heading already names it the way a reader wants — `F3. OSD - the YANKEE BLUE remand
  search result` — so the chip says `F3 · OSD` and the full destination is the tooltip.

## 6. The checks

**`verify.py` — `every FOIA request points at a question that is actually open`**, against
three silent rot paths and shown rejecting each:

| poison | the rot it stands for |
|---|---|
| a node id in the linkage that is not on the board | a node renamed while the letters keep the old id, so the chip stops drawing and the dossier looks untouched by any request |
| a question index past the end of a node's list | a research pass removes a question and the indices shift under a letter written against the old numbering |
| a status the board cannot draw | the honesty of "not filed" |
| `requests: []` | the parser reading nothing and reporting a clean run — §4, mechanised |

**`runtime_check.js` — six assertions** that it reaches the reader. The silence they guard
is specific: `FOIADATA.byNode` is keyed by node id, and if the key never matches, **every
dossier renders exactly as it did before the layer existed**. No error, no gap, nothing to
see. So the checks require chips on a node whose linkage is known, require the weaker claim
to be drawn differently, require the header count to equal the distinct count computed
independently from the data, and require a chip to stay narrower than the dock it annotates.

Getting those written surfaced one real thing: `FOIADATA` is inside the page's IIFE and
`window.FOIADATA` is undefined. That is the file's own documented constraint — the board is
module-private and every assertion goes through the DOM or through `window.__board`. It is
on the debug surface now, beside `L0DATA`, for the reason that export exists: so a check
reads the renderer's own data rather than a copy of it.

## 7. What is not built

`data/foia-links.json` carries a `status` field per request with a vocabulary of five —
not filed, filed, acknowledged, responded, appealed — and everything is at the first. When
Stewart files, editing that field is the whole change; the chip and the check already
understand the rest.

**A surface of its own was not built.** The handoff suggested asking Design whether the
queue deserves one. The node → request link is the part that makes the queue part of the
argument, and it needed no new surface. A request-side view — seventeen requests, what each
would close, filed state — is a reasonable next thing and is Design's to shape.
