# Three inherited surfaces, and the one a reader could see

**25 August 2026.** `CLAUDE.md` §9 item 1 said the COVER-UP view still carried the
sibling board's skeptical record and called it "the same class of bug as the scripted
analyst, different surface, not yet touched." It was right that the class was still
live, and wrong about where. The COVER-UP view itself had already been rebuilt. Three
other surfaces were still carrying The Vanishing.

Found by reading the built file rather than the source, which is the only way any of
these show up: every one of them is well-formed, well-set, and throws nothing.

## 1. explainEdge — the worst of the three, and the least visible

`explainEdge()` writes the caption under every connection in every node dock. It is
the most-read sentence on the board after the labels. It shipped from the parent
unpatched and was wrong in two independent ways.

**Wrong meanings for two types this board shares:**

| type | what it said | what the type means here |
|---|---|---|
| `behavioral` (77 edges) | "Both left the same category of personal item behind." | how a party conducted itself: DIA redacting a PM's name it had already published; a solicitation written to a capability one bidder held |
| `temporal` (76 edges) | "Dates fall within sixty days of each other." | succession between documents: Volume I defining what Volume II must contain |

**No caption at all for four types**, which fell through to `default: 'Connected.'`:

| type | edges |
|---|---|
| legislative | 192 |
| denial | 174 |
| custody | 119 |
| funding | 69 |

That is 554 edges, a quarter of the board, explained with one word. **Custody is one
of the three axes this board scores every entity on.**

Rewritten for all twelve types. The gate check `every edge type has a caption written
for this board` now asserts coverage and screens for the parent's vocabulary. It was
demonstrated rejecting both a removed case and a reintroduced parent sentence.

## 2. COUNTERS — 3KB of another project's editorial judgement, shipping

`viewCounterargs` was rebuilt from this board's own denial edges by an earlier pass,
which left the parent's `COUNTERS` array declared and referenced by nothing. Dead code
is usually harmless. This was not: it is Novella on JPL headcount ("JPL at roughly
4,500 employees would expect about 164 all-cause deaths over four years; this list has
five"), Shermer on excluded cells, and corrections about Casias, Chavez, Hicks and
Grillmair — a confident skeptical record for a dataset that is not here, inside a
published artifact about the UAP legacy programme.

Removed. Nothing referenced it; the assertion in the patch checks that before cutting.

## 3. The "Left behind" section of THE ANALYSIS — the one a reader could see

THE ANALYSIS view printed a section headed **Left behind**, which on this board reads
`NOTHING RECORDED` because no person here has a `leftBehind` list. Underneath it, a
styled definitional block:

> The "left everything behind" thread means a record left BOTH the phone and the
> wallet and did not carry a departure kit. That is narrower than a non-empty list,
> and it excludes Chavez, who owned no cell phone at all, and McCasland, who
> deliberately took a wallet, boots, a .38 revolver and a distinctive red backpack.
> **0 clean members: .**

A missing-persons methodology note, naming two people, standing under an empty
section, on a board about a recovery and reverse-engineering programme — and ending in
a count of zero followed by an empty list. Removed, along with its helper
`leftEverythingBehind()` and the four-line comment above it.

The helper had already been stubbed to return `[]` by a previous pass, honestly, with
a comment saying the fields do not exist here. That was a half-fix: it stopped the
function lying while leaving its caller rendering, and left the vocabulary in the
shipped file.

## What guards this now

Two gate checks, both self-tested:

- **`every edge type has a caption written for this board`** — every type present in
  the data must have its own `explainEdge` case, and no case may carry the parent's
  wording.
- **`no parent-board editorial content ships`** — screens the built file for strings
  specific to the sibling board's subject.

The second one earned its place immediately: it was added while the COUNTERS array was
being removed, and it caught surface 3, which I had not yet gone looking for.

**What it deliberately does NOT screen for:** `Ning Li` and `JPL` both appear on this
board for good reasons — the AAWSAP superconductor DIRD reviews Ning Li's work and
Hathaway's failed replications of it. Screening on those would fire on real content,
and a check that cries wolf gets disabled. `grep -i neurologica` is the same trap in
miniature: it matches the word "neurological", which is all over the AAWSAP biomedical
material. I made that mistake mid-pass and briefly believed the removal had failed.

## The general lesson, restated

`CLAUDE.md` §8 already says it: assume every inherited surface is answering about the
wrong project until someone has read it. What this pass adds is where to look. All
three of these were **below** `explainEdge` in the file, which is the region
`build_dashboard.py` patches — so they were reachable by the patcher the whole time.
Nobody had read them.

The remaining candidates named in §9 item 2 — the system prompt, the report view, the
insight strings — are still unread.
