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

---

# The systematic sweep, and the two it found that reading did not

Added later the same day, after the three above were fixed. `CLAUDE.md` §9 item 2 asked
for the sweep to be done "systematically rather than by accident". The method that
worked is four lines:

```python
pat  = re.compile(r"'((?:[^'\\\n]|\\.){40,400})'")   # JS string literals, prose-length
refs  = {m.group(1) for m in pat.finditer(open('ref/the-vanishing-v2.html').read())}
dists = {m.group(1) for m in pat.finditer(open('dist/the-program.html').read())}
survived = sorted(refs & dists, key=len, reverse=True)   # 177 of them
```

Any prose literal present in both files survived the port unmodified. Most of the 177
are UI chrome and are fine. Sorting by length puts the subject-specific ones near the
top, where they are obvious on sight.

## Five that rendered as false copy

| surface | what it said | why it is wrong here |
|---|---|---|
| SEARCH view header | "Fifty-two entities across five classes." | 956 nodes across 8 classes. A hardcoded count from the parent's dataset, and the first sentence of the view. Computed now. |
| Artifacts empty state | example question: "who disappeared within three months of McCasland" | McCasland is on this board but did not disappear from it, and there are no disappearance dates to compute against |
| `location` class note | "Locations are derived from the case records. A shared cluster produces a geographic connection automatically." | half true, and the misleading half. This board carries 61 hand-written geographic edges, every one sourced, alongside the derived ones. It told readers researched work was produced by rule. |
| `domain` class note | same claim for research domains | same: 138 hand-written research edges |
| TIMELINE standing caveat | "The density of entries after April 2026... Cases that occurred in 2021 through 2025 entered the public record only once the story broke... five years of quiet accumulation against four months of coverage." | the parent's press-break story. This board runs 1944 to 2029. Restated rather than deleted, because the reporting-attention point is real here too, for a different reason. |

## And the system prompt, which is the one that matters

`SYSTEM_PROMPT()` is what the model is told it is before it answers anything, and
nothing had ever checked it. `test_scripted_analyst.mjs` covers the no-key path only,
so the path that runs when a reader supplies an API key was the untested one.

It opened:

> "You are the analyst inside The Program, a research dashboard **tracking deaths and
> disappearances of US scientists and defense-connected individuals since 2021**."

That is the sibling board's mission statement with the name swapped. The same fault as
the scripted analyst, one path over, and missed precisely because the scripted path had
just been fixed and looked like the whole problem.

The expensive line was numbered:

> **HARD RULE 4.** "The three axes S, P and I are never summed."

This board scores every entity on **C** (custody proximity), **A** (access level) and
**D** (disclosure role). The model was holding the wrong names for the board's primary
scoring scheme, as a hard rule, so every answer it gave about scoring was fluent
reasoning over letters that do not exist here. A wrong axis name cannot throw.

Also inherited: `selectNode("leblanc")`; the parent's three geographic clusters in
`focusCluster`; a scatter example plotting S against P; a rule about the families of
the dead; and a WORKED EXAMPLE instructing the model to chart "Disappearances within
three months of McCasland" with dates for two people who are not in this data — that
is, an instruction to fabricate, sitting inside a prompt whose HARD RULE 2 is "never
invent a fact, a date, a source or a person."

All rewritten. The worked example now walks the November 2009 refusal of Reid's request
to make AAWSAP a Special Access Program, using only entities and dates that are on this
board and sourced, and it carries the AARO interested-party caveat so the model sees
the grading convention demonstrated rather than described.

## One mistake worth recording

The first poison written for the new system-prompt check appended a second
`SYSTEM_PROMPT` to the clean fixture. The check reads the first one in the file, so the
clean prompt stayed in front of the poisoned one and the check passed on poisoned input
— reported by `--self-test` as "did NOT reject poisoned input, this check is dead".

That is the duplicate-`L0DATA` trap the fixture's own comment warns about, hit again,
about forty lines below the warning. The poison now replaces rather than appends.
`--self-test` caught it immediately, which is the entire argument for having it.
