# L0 program map — implementation record, 13 August 2026

Implements the Claude Design handoff `design_handoff_l0_program_map`. Read alongside
its `SPEC.md`. This file records what was built, what was corrected, and what is
still open.

Gate at time of writing: **15 checks pass, including `--self-test` and
`--idempotent`.** Two consecutive full builds are byte-identical.

---

## 1. The correction: the floor produces 96 nodes, not 107

The handoff's figures do not reproduce. Running its own reference generator,
`build-l0-data.mjs`, against the source it names, `data/l0-extract.json` at `9ccc25d`:

| Figure | FIGURES.md | Generator output |
|---|---|---|
| L0 nodes | 107 | **96** |
| Ledger | 695 | 706 |
| Direct edges | 191 | 170 |
| Summarised edges | 82 | 76 |
| Primitives | 380 | 342 |
| Path only / Unattached | 55 / 113 | 55 / 113 |

**Cause.** The extract's `deg` field is an edge-instance count, not a degree. 94 of
the 1,685 node pairs carry more than one hand-written edge, up to three, so those
nodes are counted two and three times toward the floor. The published figures used
that field. The generator itself does not: line 60 recomputes degree from a set of
distinct neighbours, and carries the comment *"Degree is recomputed rather than
trusted — a stale `deg` field silently changes the L0 set."* It did exactly that.

**Resolution: distinct neighbours.** Accepted by Stewart on 13 Aug. The renderer
settles it — patch P2 aggregates every hand-written edge on a pair into one drawn
line, so a map that draws a pair once cannot let that pair count three times toward
a *connectivity* floor.

**Eleven nodes leave the map:** `atic`, `cfr-32-117`, `dhs`, `dodd-5205-07-2010`,
`dodig-2023-109`, `eo-13526`, `icd-906`, `oak-ridge-national-laboratory`,
`uap-nda-waiver-directive-2026`, `usaf`, `uss-princeton`.

**Downstream corrections to the handoff's prose**, which should be applied there
rather than only here:

- Class composition is institution 32 · document 23 · program 21 · event 12 ·
  legislation 8.
- The "three inert nodes" become **one**: `ndaa-fy2023-sec-6802`. `usaf` and
  `blue-book-special-report-14` are no longer on the map. The README uses `usaf`
  as its worked example of the single-member refusal; that example needs replacing.
- `aaro` carries 52 members, not 49. `pursue-releases` 29, not 27.
- Unclustered L0 nodes: 49 of 96, not 57 of 107.
- Shared-count distribution `{2:62, 3:11, 4:1, 5:2}`. Still within the five-tick
  vocabulary, so no numeral case is introduced.
- Wall-clamp measures **3.1%** in this Python bake, against the handoff's 6.5% for
  its JS bake at 107 nodes. Label overlaps at the true 68x20 box: **0**, which is
  the figure that actually matters.

## 2. Denial direction — confirmed, nothing inverts

SPEC open question 3. The convention is `a` = issuer, `b` = subject, confirmed
against the merged board rather than inferred from a sample. Representative edge:
`susan-gough -> luis-elizondo`, "no assigned responsibilities for AATIP". Issuer
totals reproduce exactly: `aaro-historical-record-vol1` 10 issued / 8 received,
`susan-gough` 8 / 0, `david-grusch` 3 issued / 7 received. The §08 argument stands
as written.

## 3. SPEC §7 — the rest state opens at 1.0, and now for a measured reason

The handoff's argument was that at 107 nodes a fitted view lands at 0.60, below the
0.62 label-drop threshold, so a fitted rest state is a field of unlabelled marks. At
96 nodes the extent shrinks to 1574x1030 and the question had to be re-asked.

Measured at runtime rather than argued: on a 1600x1000 shell the view surface is
1092x549 and **fit-zoom is 0.466**. Well below 0.62. On a 1440 shell it is lower
still. The conclusion holds with room to spare, and `mountL0` now *measures* it on
mount instead of hard-coding the decision — if a future shell makes the fit clear
the threshold, the map opens fitted on its own. `OVERVIEW` remains an explicit
control either way.

## 4. What was built

| Item | Where |
|---|---|
| P1 register partition, routing, member lists | `tools/build_l0.py` |
| P2 direct-edge aggregation per pair | `tools/build_l0.py` + `l0_patches.py` |
| P3 shared-member edges, gate >= 2 | `tools/build_l0.py` |
| P4 tier in the dash channel (D1) | `l0_patches.py` |
| P5 directional denial edges (D3) | `l0_patches.py` |
| P6 five CMD actions, each with a control | `l0_patches.py` |
| P7 member ledger | `l0_patches.py` |
| P8 the L0 bake | `tools/build_l0.py` |
| D4 marks/colours for document, event, legislation | `l0_patches.py` |
| Six verify checks, each self-tested | `tools/verify.py` |

`tools/build_l0.py` joins the documented pipeline **before** `build_dashboard.py`,
and is inside the idempotency gate, because a bake seeded from anything
non-deterministic would drift there and nowhere else.

`GOLDEN.json` gains `l0_nodes`, `l0_edges_direct`, `l0_edges_summarised`, `ledger`,
`path_only`, `unattached`. Accepted deliberately; nothing else in the manifest moved.

## 5. The self-test earned its keep again

All six new checks were **born broken and silently passing.** The fixture built each
poisoned HTML from a `good_html` that had already had a valid model appended, so
every poison carried two `L0DATA` literals and the parser read the clean one first.
Six checks reporting `ok` while asserting nothing.

That is the `canvasInk` failure exactly, reproduced in the fixture instead of the
check. It is also the third time on this board that roughly half the new checks were
dead on arrival. **Rule 2 is not optional and the rate is not improving.**

A seventh defect surfaced the same way: `UI copy agrees with the register counts`
originally matched a string literal that my own rail patch did not emit. It now
asserts something worth asserting — that both register controls exist and that their
counts are derived from `L0DATA.counts` rather than typed.

## 6. Additions to the spec, needing sign-off

**Full-graph fallback.** The handoff specifies the NETWORK *rest state* and does not
say what becomes of the inherited commands that operate on the full graph:
`setHops`, `highlightPath`, `focusCluster`, `frameNodes`, and the insight callout's
"Show me on the map". Replacing the surface outright breaks all five silently. So L0
owns the rest state, and the legacy full-graph map mounts in its place while a path
or a frame is active, with a `FULL GRAPH` breadcrumb chip and `CLEAR` returning to
L0. `selectNode` deliberately does **not** trigger the swap: the ledger is a table of
contents for the dock, and opening the dock must not move the map.

This is an addition, not an implementation of the spec. It is the only place I
invented behaviour rather than following it.

**Legacy chrome suppressed.** `renderNetworkChrome` returns early under L0. Its
`INSIGHTS()` reads `MAP.pairs`, which the L0 map does not have; unguarded it threw
inside `paint()`, and because `paint` catches per surface, the ledger and the
register panel simply never appeared while the console stayed quiet. Found at
runtime, not by reading the diff.

## 7. Still open

1. **`dird-series` is the third-largest node at 32 members, all documents.** A
   filing convention for the DIRD papers, not a claim about the program. The design's
   recommendation on file is to promote named documents individually. Unchanged.
2. **D4 marks and colours** still need sign-off. `document` is `#f0d264`.
3. **D2 is a rule bent, not met.** The class ledger bar carries its mix in hue alone.
   The tooltip names every segment; that mitigates, it does not comply.
4. **The stats strip still reads CONFIDENCE KEY.** The handoff's shell spec calls for
   the claim-tier key. Not implemented; one line, deferred rather than guessed.
5. **`FIGURES.md`, `SPEC.md`, `l0-data.js` and the prototype all still encode 107.**
   They should be regenerated by the design session rather than hand-patched here.

---

# Stage 2 — entity dossiers and selection, 14 August 2026

Stewart's review of the first build overrode three things the handoff specified.
The overrides are right and are now implemented.

## Entity dossiers — the new primary content

25 L0 nodes, **345 sourced claims**, researched and written this session by four
parallel agents against live sources. Clicking MITRE now gives you the argument for
why MITRE is on the map, with the member ledger underneath it as a table of
contents. That inverts the handoff's emphasis, on purpose: the argument is the
product.

Shape per entity: `whatItIs`, `whyImplicated` (the load-bearing paragraph),
`roles`, a 700-1100 word narrative, tiered claims with sources, `denialPosture`,
and `openQuestions`.

They live in `research/dossiers/` as a **parallel dataset**, not merged into the
board's nodes. Two reasons. `merge.py` globs `research/*.json` and expects node
documents, so they broke the pipeline where they were. More importantly, merging
345 claims onto 25 nodes would move every claim count, tier mix and GOLDEN entry,
and it would conflate two different objects: a node claim is a fact about the
entity, an entity dossier is the argument for why the entity is on this map.

**Research honesty, carried through rather than smoothed over.** The agents flagged
their own thin spots instead of writing around them:

- `cia` is Tier 1 on Robertson Panel and U-2 material and Tier 3 on anything modern;
  the retrieval allegation rests on one reporter with no document.
- `yankee-blue` rests on a paywalled WSJ piece that could not be fetched. What is
  Tier 1 there is entirely negative-finding material: the OSD no-records
  determination, Gough's 1 Oct 2025 non-confirmation, the 12 Dec 2025 appellate
  remand. The AFOSI case number is explicitly marked not independently verified.
- `uap-science-advisory-council` has no published charter, FACA notice or roster.
- The PURSUE executive release channel has no primary; `war.gov/ufo` would not return
  content.
- Public Law 118-31 dropping the Review Board and eminent domain is sourced to NARA's
  description, not the enrolled text, because every full-NDAA fetch truncated.

Three findings worth promoting into the board's argument: the DHS-MITRE HS SEDI
sponsoring agreement excepts §9(g)(2), the clause preserving disclosure to Congress,
for subcontractors while MITRE staff keep it; DoDD 5205.07 §3.1.g is an unclassified
standing prior-restraint on giving SAP material to any member of Congress without
DoD SAPCO approval; and the AAWSAP DD-254 was amended before award to drop the
requirement that the contractor hold a TS facility clearance prior to implementation.
One correction for the existing board: Loeb's first UAPSAC post is dated 13 June 2026,
not 29 June.

## Selection is now single and global

The handoff's additive-ledger model ("comparison is the point") failed in use: no way
to unclick, no visible exit, and a second click took you nowhere. Now one selection,
obeyed everywhere.

- Clicking a node selects it, zooms to it at >= 1.15 and opens its dossier.
- Clicking it again clears. Clicking empty canvas clears.
- `selectNode` from the timeline, a case card or a search result clears prior
  selections, lights the node on the map and moves the camera to it. Previously the
  map kept the old selection and the reader could not tell which node the dock
  described.
- Multi-open survives only on the CMD line, where an analyst who genuinely wants two
  ledgers can still ask.

## The dock reads like a document

306px is not a reading measure. On selection it animates to half the viewport,
floored at 560px, on a 260ms cubic curve. One always-present chevron collapses it.

**Two silent failures found by measuring rather than reading**, both worth recording
because they are the same class of bug this board keeps hitting:

1. Setting the width through the `--dock-w` custom property did nothing. The
   inherited resize grip already writes that property to `:root`, and two owners
   racing one custom property produced no error, no console output, and no movement.
   Fixed by setting the width on the element.
2. The open condition read `S.dockWide !== false`, and `setDockOpen` writes
   `S.dockWide`. The first paint at rest set it to `false`, which permanently
   falsified the condition that was supposed to open it. A flag that the reader sets
   and a flag the renderer sets must not be the same flag.

Both looked correct in the diff. Both were caught by asserting a measured width in
the browser.

## Still open

1. Entity dossiers exist for 25 of 96 L0 nodes. The other 71 have none, and the dock
   falls through to the inherited node dossier for them. A `verify.py` check that
   every L0 node has a dossier should wait until the rest are written, or it will
   fail by design.
2. No verify check yet asserts that every dossier claim carries a tier and a source.
   That should exist before the next research wave lands.
3. The stats strip still reads CONFIDENCE KEY where the handoff calls for the
   claim-tier key.
4. D4 marks and colours still need sign-off; D2 is still a rule bent.

---

# Stage 3 — all 96 L0 nodes have a dossier, 14 August 2026

Twelve research agents in two waves covered the remaining 71 nodes.

```
L0 nodes            96
with a dossier      96      (was 25)
dossier claims   1,361      Tier 1 968 · Tier 2 344 · Tier 3 49
claims with no source  0
```

Every claim carries a tier and a source, and `verify.py` now asserts both. Two new
checks, both self-tested: `every L0 node carries an entity dossier` and `every
dossier claim is tiered and sourced`. `GOLDEN.json` gains `l0_with_dossier` and
`l0_dossier_claims`, because coverage moving is either research landing or a
regression and the two look identical in a diff.

A `connections` field was added to the schema for this wave and is rendered in the
dock. It is written for the downstream analyst agent rather than a human reader:
plain-language notes naming who links to whom, so a later pass can find joins the
research never made explicit. 71 of 96 carry it; the first 25 predate the field.

## The tiering held up under scale

`manhattan-project-2` renders with **zero Tier 1 claims and two Tier 3**. That is
the system working: the label has no primary document behind it, and the agent
tiered it as an allegation with named proponents rather than dressing it up.
Likewise `stringfield-status-reports` has no Tier 1 at all and its substantive
abstracts were pushed to `openQuestions` by design, and `gerb-mitre-investigation`
carries the batch's only Tier 3 weight because Gerb's identity is unknown.

## Corrections the research surfaced, for the next wave

1. **`iaa-fy2024-sec-1102` is misnumbered on the board.** In S.2103 as reported
   22 Jun 2023 the contractor turn-in provision is **Sec. 1104**; Sec. 1102 is an
   unrelated defense-sensitive-support provision. The enacted text is **Sec. 7343 of
   Division G, P.L. 118-31**. The node id and label should be corrected.
2. **The AARO FY2025 report contradicts itself.** §IV.C says 44 satellite-flaring
   resolutions; §VI and the executive summary say 238. Worth a claim of its own.
3. **Loeb's first UAPSAC post is 13 June 2026, not 29 June.** 29 June is the second.
4. **10 U.S.C. 119(a)-(b) annual SAP reporting terminated 31 Dec 2021** (Pub. L.
   114-328 §1061). Several board claims state the duty in the present tense.
5. **AARO Historical Record Report Volume I contains zero occurrences of "Wilson."**
   It disposes of the reverse-engineering allegations as "circular reporting"
   without engaging the document sitting in a congressional hearing file.

## Recurring research obstacles, so the next wave does not rediscover them

`congress.gov`, `nytimes.com` and `web.archive.org` will not fetch. Full NDAA text
truncates on every attempt. Several agents exhausted a 200-search budget mid-task;
raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` before the next wave. Sibling
agents in the same session deduplicate identical fetches, so two agents needing the
same PDF will find the second request blocked.

## Still open

1. The 874 non-L0 nodes have no entity dossier. The register is total and they are
   all reachable, but the analyst layer stops at the map.
2. Corrections 1 through 5 above are logged, not applied.
3. Stats strip still reads CONFIDENCE KEY; D4 and D2 still need sign-off.

---

# Stage 4 — the analyst layer and the unattached wave, 14 August 2026

## The next wave was the wrong job, and measuring said so

The plan was entity dossiers for the 874 non-L0 nodes. Measuring first killed it:
those nodes are not empty. Median narrative runs 113-213 words by class, **zero are
empty**, and only 26 are thin — of which 24 are bare city locations at degree zero,
where the work is wiring them, not describing them. Writing 874 dossiers would have
been an expensive restatement of prose already on the board.

## What was actually missing: the connection layer

Every node now carries an explicit connection list **projected** from the board's own
hand-written edges: neighbour, class, type, tier, direction, plus the `why` and
`note` the researcher already wrote. 1,771 of 1,786 edges carried a label and 1,712 a
note, so this is a reformatting of sourced research into a shape an agent can
traverse. Nothing is generated, and a new self-tested check rejects any row without a
hand-written edge behind it — a generated connection on this board would be a
fabricated claim.

The dock renders it for **any** selected node, not just the ones on the map, and each
row clicks through.

## The unattached wave

Four agents were sent at the 90 degree-zero nodes with a simple brief: wire them with
sourced edges, or say honestly that no connection exists.

```
                before   after
unattached        113      64
ledger            706     755
path only          55      54
hand-written edges 1786   1893      (+107)
summarised edges    76      86
L0 nodes            96      97
```

**49 nodes came off the unattached register.** Three were judged unwireable and said
so: `izmiran` (its SETKA-AN role is attested but no source connects it to any node on
this board), `peru-uap-office` (AARO's own foreign-engagement section documents
London and Uruguay, not Peru), and `soyuzufotsentr` (the obvious KLAS-TV link is
actively contradicted — Knapp's documents came from the MoD via Col. Boris Sokolov,
not the KGB "Blue Folder"). Those three refusals are worth more than three invented
edges.

**31 locations are recommended for removal** as incidental biography — congressional
home towns and researcher home bases that fail the test "does something that matters
to this subject demonstrably happen here". Not actioned; it is a deletion and Stewart
should approve it. Seven more (`l-aztec`, `l-france`, `l-paris`, `l-brazil`,
`l-brasilia`, `l-santiago`, `l-moscow`) are recommended for KEEPING but stay unwired
because the partner nodes they need (aztec-1948, geipan, cometa, cefaa, setka) do not
exist on the board yet. That is a research finding: the board has no European or
South American UAP-office nodes.

`langley-2023-incursions` crossed the floor onto the map as a result of the wiring
and was given a dossier immediately, because the coverage check failed the build and
would not let it ship otherwise. That is the gate doing exactly what it is for.

## Corrections and cautions the wave produced

- **`iaa-fy2024-sec-1102` is misnumbered**, now confirmed twice independently. The
  contractor turn-in provision is Sec. 1104 of S.2103 as reported; the enacted text is
  Sec. 7343 of Division G, P.L. 118-31.
- **Gen. Mark Kelly (ACC commander, the Langley eyewitness) is not Sen. Mark Kelly
  (D-AZ).** Secondary coverage conflates them.
- The AARO "has not yet received a report" statement on Langley is the most
  load-bearing concealment artifact in that dossier and the weakest-sourced. It needs
  a FOIA.
- `steve-feinberg` has **no** sourced UAP or AARO role: his SASC advance policy
  questions and nomination transcript contain zero hits. He is wired only as Deputy
  Secretary of Defense, and that absence is itself worth noting.

## Still open

1. The 31 recommended location deletions need a decision.
2. Five European and South American UAP-office nodes do not exist and should.
3. 64 nodes remain unattached, 3 of them demonstrably unwireable.
4. Corrections logged in Stage 3 remain unapplied.

---

# Stage 5 — structural authority, 14 August 2026

## The instrument had a shape, and Feinberg showed it

The board grades nodes on connections. That grades **people on what they said** and
on what documents they generated. It is a good instrument for witnesses,
whistleblowers, journalists and FOIA requesters, and a bad one for officials whose
relevance is *positional*: someone who can approve a compartment, relieve an
oversight function or compel records, and who has never spoken publicly, scores
near zero and sinks.

Stephen Feinberg surfaced it. Three of the four Deputy Secretaries of Defense on
this board have a documented UAP decision attached to the office — Lynn received
the 2009 Reid SAP packet, Norquist established the UAP Task Force, Hicks signed the
AARO establishment memo. The incumbent has none, and on connection count he ranked
in the 300s while sitting in the chair the other three used.

That is a shape in the instrument, not a fact about him. **The empty evidence column
is the finding, and a scoring system that buries it is the wrong instrument.**

## What was built

`research/_authority.json` — a curated rule set. An office qualifies only if a
**citable instrument** grants it authority to DO something to this subject: approve
or disapprove a SAP, relieve an oversight function, compel or withhold records, or
direct a component that does. Seniority is not authority. Speaking for the
Department is not authority. Twelve offices, each naming its instrument (DoDD
5205.07, 32 CFR 117.6, 10 U.S.C. 119, 50 U.S.C. 3373, E.O. 13526, P.L. 118-31).

**21 nodes flagged. 7 of them hold top-weight authority with two or fewer
connections**: Feinberg, Gabbard, Lukas, Norquist, Haines, Mattis, IC SAPCO.

The dock renders the authority, its instruments, and — where the record is thin —
states plainly that the office could answer from position alone and the record is
nearly empty.

`held` and `holds` are distinguished. A former holder's authority is history; the
incumbent's is live, and the board must not blur the two.

## The matcher went loose once, exactly as expected

The first pass flagged **45** nodes including hearings and letters that merely
*cited* an office in their subtitle, plus `donald-kerr` and `sue-gordon`, which the
rules file explicitly excludes. Substring matching against the whole subtitle
catches mentions, not offices.

Fixed by matching only the **role descriptor** — the leading clause of `sub` before
the first semicolon — and only for people and institutions. 45 became 21.

The check now asserts the exclusions by name: `susan-gough` and
`christopher-sherwood` speak for a decision and do not make one;
`donald-kerr` and `sue-gordon` advise a corporation, not a compartment. If any of
the four reappears, the matcher has gone loose again and the build fails.

Also asserted: every flagged node must cite an instrument, because an uncited
authority is an assertion, and tense must be `holds` or `held`.

## Verified at runtime

`/tmp` was wiped between calls and Playwright had to be reinstalled — the documented
gotcha, and worth the reinstall. Confirmed in the browser: Feinberg renders the
badge **and** the thin-record warning; Kirkpatrick renders the badge and **not** the
warning, correctly, because he has 18 connections; Gough renders no badge at all.

## Still open

1. The authority list is 12 offices. The waived-SAP notification recipients — the
   eight members of Congress — are not on the board as a set and should be.
2. `dird-series`, D4 sign-off, D2, and the CONFIDENCE KEY label remain from Stage 1.
3. 27 nodes remain unattached, 3 demonstrably unwireable.

---

# Stage 6 — corrections verified, and the DIRD star broken up, 14 August 2026

## One of the five corrections was itself wrong

All five proposed corrections were verified against primary sources **before any
was applied**, and the one two independent agents were most confident about was
refuted.

Both claimed `iaa-fy2024-sec-1102` was misnumbered and should be Sec. 1104. They had
conflated two bills. The provision **is** Sec. 1102 of Division M of S. 2226 as
passed by the Senate on 27 July 2023, **and** Sec. 1104 of S. 2103 as reported by
SSCI on 22 June 2023. Both citations are correct, to different vehicles. The board
was right and the correction would have introduced an error.

Two agents agreeing is not corroboration when they share a method.

The verification also found something the correction would have buried: **the
turn-in mandate did not survive conference.** Enacted Sec. 7343 of Division G,
P.L. 118-31 contains only definitions, a funding limitation and an IR&D limitation.
"Non-earth origin", "exotic", "in their possession" and the 60-day deadline appear
nowhere in the enacted text. Three new Tier 1 claims record that, with 7343(b)
quoted in full.

Four confirmed and applied: the AARO FY2025 satellite-flaring contradiction (44 at
§IV.C against 238 at §I and §VI, with the separate §III.A "44 in the space domain"
named so a reviewer is not ambushed by it); the termination of 10 U.S.C. 119(a) and
(b) on 31 December 2021 with (c) through (g) surviving; the total absence of
"Wilson" and "Davis" from all 63 pages of AARO HRR Vol I; and Loeb's post dates.

## The DIRD star, and what breaking it cost

`dird-series` was the third-largest node on the map with 32 members, and **31 of
those 32 documents had degree 1** — they connected to the hub and to nothing else.
A star whose centre exists only because nothing else connects to its spokes is a
filing artefact, not a finding.

Four agents wired each DIRD to its author, its commissioning programme and its
institution, working from the DIA letter to SASC of 9 January 2018 that lists all 38
by title and author.

```
DIRD degree      before: 31 nodes at 1      after: 17 at 4, 15 at 5, 2 at 3
largest node     dird-series (3rd)          aawsap, 82 members
edges            1,909                      2,030
people           246                        266
```

`aawsap` becoming the largest node is the **correct** outcome. It genuinely
commissioned all 38 deliverables, so its footprint is a fact about the programme,
where `dird-series` was a fact about a shelf.

**20 new authors** joined the board — Winterberg, Millis, Leonhardt, Miley, Baker,
Genik, Hathaway, Obousy, Cramer, Czysz, Towe, Teofilo, Culbreth, Maccone, McCarthy
and others. Two popular attributions were corrected against the DIA list: the
warp-drive DIRD is credited to **R. Obousy**, not Eric Davis, who is a co-author;
and the superconductors DIRD to **George Hathaway**, not the academics it reviews.

Every released DIRD redacts its author under (b)(6), so no attribution rests on a
cover page — all rest on the DIA congressional list. That is stated in the
unresolved log rather than smoothed over.

The `aneutronic-fusion-propulsion` pair is **not** a duplicate: two physically
distinct documents, DIA-08-1011-003 (50pp) and -004 (37pp), same date and ICOD. The
board label is missing the "II".

## Divergence D6 — I broke the tick vocabulary myself

The design package asserted that shared-member counts run 2 to 5, "so the parent
board's five-weight tick vocabulary fits exactly, with no overflow and no numeral
case." That was true of the graph as it stood. Densifying it made it false:
`dia~dird-series` now shares **18** members.

Five ticks cannot carry 18, and drawing five for both 5 and 18 would be a channel
that silently saturates — the same failure class as a check that always passes.
Beyond five, the marks now give way to a numeral. **This is the numeral case the
design said did not exist. It exists now, and it exists because of my change.**

The check that caught it asserted a design constraint rather than a property, so it
became false the moment the data moved. It now asserts what still holds: that the
renderer has an overflow path. Verified in the browser — three pairs render numerals.

## Also closed

D4 approved as built. D2 accepted as a recorded exception. Both were Stewart's
calls, both now closed rather than open.

## Still open

1. **The eight members of Congress who receive waived-SAP notification** are still
   not on the board as a set. Next deep pass.
2. `dird-vacuum-engineering` remains at degree 1 and was not in any batch.
3. `dird-series` and `dird-collection` are two nodes describing the same thing.
   Worth collapsing, but it is a deletion and needs approval.
4. 23 nodes unattached, 3 demonstrably unwireable.

---

# Stage 7 — collapses, and the waived-SAP notification group, 14 August 2026

## Two duplicate pairs collapsed

`dird-collection` and `dird-series` described the same object. `dird-series`
survives (degree 34 against 7) and takes the more precise label; its seven edges
were re-pointed first. `dird-vacuum-engineering` was a second node for Puthoff's
vacuum/spacetime metric DIRD, which is why it sat at degree 1 after the DIRD wiring.

The first attempt orphaned a timeline event — `verify.py` caught `tl-2019-dirds`
still pointing at the removed node. **A collapse is not a deletion.**
`research/_removed.json` now carries an alias map and `merge.py` re-points
references at the survivor. The 31 removed locations deliberately have no alias,
because nothing should point at them.

## The waived-SAP notification group

The board argued that a waived unacknowledged SAP is concealable because
notification runs to a handful of members, without ever naming them. Now it does.

**The governing provision is 10 U.S.C. 119(e)(2), not the Gang of Eight.** These
are routinely conflated and they are different mechanisms. 119(e)(2) routes withheld
information and the waiver justification "jointly to the chairman and ranking
minority member of each of the defense committees", and 119(g) defines those as six
bodies — SASC, SAC, SAC-Defense, HASC, HAC, HAC-Defense — which is **twelve seats,
not eight**. Note that §119 uses its own definition rather than the narrower
10 U.S.C. 101(a)(16).

12 current office-holders sourced from .gov committee pages, plus the 2009, 2020 and
2023 rosters. 28 edges. Six gaps logged rather than guessed.

### The finding that changes the argument

**The waiver mechanism has quietly lost most of its subject matter.** Pub. L. 114-328
§1061(c)(4) terminated 10 U.S.C. 119(a) and (b) after 31 December 2021, and §119(e)(1)
can only waive requirements "under subsection (a), (b), or (c)". So the waiver now
bites only on subsection (c), classification-change reports.

Two corollaries the board should carry:

1. §119(f)'s 30-day pre-initiation notice to the **full** defense committees was
   never waivable.
2. Unlike 50 U.S.C. 3093, §119 has **no 180-day sunset and no duty to tell the rest
   of the committee that a limited notification even occurred.** That makes the DoD
   SAP channel the more opaque of the two, which is the opposite of the usual
   assumption that covert action is the darker one.

Separately: DoDD 5205.07 as reissued 12 September 2024 no longer uses the words
"acknowledged", "unacknowledged" or "waived" anywhere.

## Still open

1. Six office-holder gaps in the notification group.
2. 23 nodes unattached, 3 demonstrably unwireable.
3. The stats strip still reads CONFIDENCE KEY.

---

# Stage 8 — the backlog closed, 14 August 2026

Everything outstanding was worked in one pass: the CONFIDENCE KEY label, the six
office-holder gaps, and the 23 remaining unattached nodes.

```
                  session start    now
unattached             113           3
L0 nodes                96         107
ledger                 706         818
dossier claims       1,361       1,527
```

**Only three nodes remain unattached**: `soyuzufotsentr` (demonstrably unwireable —
the obvious KLAS-TV link is contradicted), `university-at-albany` and `l-albany`.

## What the waves found

**The Brazilian cluster** was 13 nodes talking only to each other. Now wired, and
the outward links are the interesting part. Operação Prato material reached US hands
three times over — Bob Pratt's dossier, Vallee being shown the military file by
Hollanda in 1988, and AAWSAP/BAASS building a 346-record "Project Colares" database
inside CAPELLA with two 2009 collection trips to Brazil. **Every channel is private.
None is state to state.** Set against that: AARO's FY2025 Foreign Partner Engagement
section is two sentences naming one London conference briefing, and the Sky Canada
report contains zero occurrences of "Brazil". Both negatives are on the board as
labelled comparison edges.

**The domain nodes** were orphaned at degree 1-2 when they should be among the
best-connected. 55 edges across seven domains, which also fixed `ndaa-fy2025`,
`iaa-2023`, `raytheon` and the AAWSAP contract node.

**Four of six office-holder gaps closed.** Two corrections came with them: Tom Cole
did **not** hold a 119(e)(2) seat on the Grusch testimony date — Granger did — and
DoDI 5205.11 para 7.2.a(3) admits committee **staff directors and a security
manager** to waived SAPs, so the earlier "no staff who can read the material" line
was wrong as a matter of DoD policy.

## Five collapses

`d-money` into `d-funding` (a facet, not a peer — its own description said it
"narrows d-funding to a single question"), `dod-sapco-arch` into `dod-sapco`,
`varginha-1996` into `ev-varginha-1996`, plus the two from Stage 7.

`d-legislative` and `d-legislation` were **not** collapsed. Their membership sets
came out fully disjoint, and proposal-versus-enactment is the board's central
substantive finding — the Review Board and eminent domain provisions passed the
Senate and were stripped in conference. Collapsing them would erase the finding.
`d-legislative` is relabelled "Legislative Process (proposed and pending)" instead.

## Three errors caught, one of them mine

1. **12 seats, not 8.** Two agents disagreed on the size of the waived-SAP
   notification group. I read 10 U.S.C. 119(g) directly: it defines its own six
   bodies, including **both** Appropriations Defense subcommittees, so chair plus
   ranking is twelve. §119 does not use the narrower 10 U.S.C. 101(a)(16)
   definition. The "eight members" assertion was stripped before it entered the board.
2. **RQS 193/2022 is not a records-seeking instrument.** It is a request for a
   commemorative special session under Art. 199 RISF, approved 16 March 2022, held
   24 June 2022. The Brazil pass built twelve edges on the assumption that it
   compelled disclosure. Its durable value is the content of its justificação, which
   names Operação Prato, the 1986 night, SIOANI and the archive code BR DFANBSB ARX.
3. **My own over-correction.** Having found error 2, I tiered down all twelve edges
   at once. Wrong in the other direction: most of them assert what the document
   **names**, which is verifiable in its text and unaffected by its procedural
   nature. Tiers restored, note kept. A correction applied by regex across a set is
   the same failure as the over-broad matcher in Stage 5.

## Still open

1. Three unattached nodes, one of them demonstrably unwireable.
2. `operacao-prato` and `ev-noite-ovnis-1986` are Tier 1 poor — no SIAN item numbers,
   no press-conference transcript, no primary FAB order. A Brazilian archive request
   would close it.
3. Arquivo Nacional says its UFO fund ends at 2016; the FAB says transfers run to
   2025, and 2025 records are demonstrably being released. Unresolved contradiction.
4. Whether a §119(e)(1) waiver was ever exercised over UAP activity. No document
   class exists in which the answer would appear.

---

# Stage 9 — research backlog closed, 14 August 2026

**Unattached is 0.** Every one of the 968 nodes is reachable. 110 L0 nodes, all with
dossiers, 1,563 dossier claims, 4,320 connection rows.

## Two claims got WEAKER, and that is the result

**The Sec. 1102 turn-in language has never been read.** Six primary vehicles were
tried — govinfo HTML and PDF of S.2226es and S.2103rs, SSCI's engrossed PDF, and both
formats of the Congressional Record granule — and all die at the same ~92-145k
character extraction ceiling, always from file start, with no range access. The
nearest miss reached Title IX, about two printed pages short.

So the 60-day deadline, the "non-earth origin or exotic" language and the
make-available-to-AARO mandate rest on a secondary source describing **reported Sec.
1104**, not engrossed Sec. 1102. That is a downgrade of the board's prior confidence
and it is recorded as a Tier 2 claim rather than buried. What was established: Title
XI of Division M contains exactly two sections, confirmed against a second
independent primary copy; the full text was printed as **SA 1053 at 169 Cong. Rec.
S3628-S3642**, which is the citation vehicle a future pass should use; reported Sec.
1103, "Modification of congressional oversight of special access programs", was
dropped between committee and floor.

**The twelve-seat argument is narrower than it looked.** DoDI 5205.11 §7.2.a(3)
extends waived-SAP access **beyond** the statute's twelve seats to committee staff
directors, a security manager, and the intelligence committees, while §7.2.h routes
justification materials "only to the committee staff directors". The board should not
claim that twelve people are the whole readership.

## The waiver: affirmative at the mechanism level, negative at the instance level

DoDI 5205.11 (12 Sep 2024, public) says the Secretary "may designate select
unacknowledged SAPs as 'waived' … pursuant to Section 119 of Title 10", defines a
waived SAP in its glossary, and requires the SAPOC's annual review to assess "All
waived DoD SAPs to determine the need for continued waived status" — **an agenda item
nobody drafts for an empty set.**

But no public document names a single exercise, date, programme or count, and none
links a waived SAP to UAP. The absence is by design: §119 requires no public reporting
of waiver use, GAO's access is gated through the defense committee chairs, and the
Moynihan Commission recorded that waived-programme notification was given "only
orally". Note also that §119(a) and (b) terminated 31 Dec 2021 and DoD **still**
designates waived SAPs "pursuant to Section 119".

## Brazil: hardened where the record allowed, and honest where it did not

17 Tier 1 claims added from two primary records — the federal court judgment in
Recurso Cível 5002417-48.2022.4.04.7200/SC and Câmara RIC 679/2011.

**The archive contradiction is resolved: it is a catalogue-description lag.** The
"743 registros / 1952-2016" text sits on an Arquivo Nacional news item stamped
13/09/2018 and never revised. Portaria 551/GC3 Art. 3 obliges CENDOC to send
originals "periodicamente", so the fund is structurally open; the FAB's August 2026
note gives 1952-2025 and 2025 dossiers are being served. The stale figure propagated
into COMAER's own 2022 court filing.

Also settled: **"Juniti Saito" is correct** — his own signed Ordem do Dia reads
"Tenente-Brigadeiro-do-Ar JUNITI SAITO". "Junichi" originates in Senado RQS 193/2022,
which also miscalls the Portaria a "decreto". The 743 and 758 figures **count
different things**: 743 is the 2018 fund description, 758 is a 2022 SIAN search-hit
count. Portaria 551/GC3's DOU publication is now attested independently of the FAB.

**No SIAN item numbers were obtained and none were invented.** sian.an.gov.br and
dibrarq return anti-bot CAPTCHA pages and SIAN consultation requires gov.br
authentication. The Arquivo Nacional's own statement that a SIAN search on "operação
prato" returns six documents, none audiovisual, is on the board; the item numbers are
not. No primary FAB order establishing Operação Prato exists in any accessible
official source — only ufology blogs assert one, and they were rejected.

## Four errors in my own brief, found by the agent I briefed

I told the dossier agent that Condign was a four-volume report, that Volume 3 was
titled "Potential for Exploitation", that its preface was dated December 2000, and
that Knuth's page lists UAP as a research interest. **All four were wrong.** It is a
three-volume report, Volume 3 is "Miscellaneous Related Studies", the preface is
February 2000, and it is Szydagis's departmental page that carries the declaration,
not Knuth's. The centre's name is also SOYUZUFO**S**ENTR in the document, not
Soyuzufotsentr.

Corrections recorded. An agent that contradicts its own brief is the system working.

Two finds worth carrying: UAlbany's 5 Nov 2025 release states **Eric W. Davis joined
the physics department as visiting adjunct faculty**, and FOI review file DEFE
24/2090/1 shows a still-redacted **"CIA desk officer"** reference at Condign Vol 3,
Ch 4, p3, para 12.

## Collapses this stage

`setka` into `setka-program` (the survivor's `program` class is correct for a research
programme; `setka` was mis-classed as an institution). `l-albany` removed under the
criterion already approved for 31 other locations — its entire content is the
university's mailing address.

## Genuinely blocked, not deferred

1. Verbatim text of engrossed Sec. 1102 and enacted §7343. Extraction ceiling.
2. Any identified instance or count of a §119(e)(1) waiver. No public document class
   exists in which the answer would appear.
3. SIAN item numbers for Operação Prato. CAPTCHA and gov.br authentication.
4. The 1986 press coverage at memoria.bn.gov.br. Empty body returned.

---

# Stage 10 — adversarial review, 14 August 2026

Run at Stewart's request against the finished board. Three layers.

## Layer 1 — Jess: independent numeric re-derivation

`tools/audit_independent.py`, which **deliberately does not import `verify.py` or
`build_l0.py`.** Running the author's own gate proves the author is self-consistent,
not that the deliverable is right. This file reimplements the floor, the BFS
registers, the edge aggregation and the shared-member gate from scratch and compares
against both the model and the figures a reader actually sees.

**38 checks, 0 failures.** Every rendered figure ties: ENTITIES 968, SOURCED LINKS
2,160, TIER A 144, DOCUMENTED 59% of 4,431, DENIALS 174, CUSTODY 119, map 428
objects. The L0 set was compared by **exact membership**, not just count.

**The audit script's own first run had two failures, and both were the script's
fault, not the board's.** It scraped the built HTML for the stats strip, but the
strip is computed at runtime, so it matched `5205` out of "DoDD 5205.07" for CUSTODY
and could not find ENTITIES at all. Fixed to read the rendered DOM. Where the runtime
capture is absent the checks now **fail loudly rather than skip silently** — the
canvasInk lesson, applied to the auditor.

## Layer 2 — Justin: fresh-eyes visual pass

Run in a subagent given only the screenshots and told to ignore the data entirely.
It found eight things, six of them real.

**The one that mattered: the dossier panel was clipping every line at both edges.**
The panel the entire board exists to deliver, losing the end of every sentence.

The cause is worth recording because my own instrumented check **passed while it was
broken.** The shell is a CSS grid and the dock is a grid child whose track is sized by
`--dock-w`. I was setting `width` on the *element*, which made the element wider than
its track, so it overflowed to the right and off-screen. A programmatic "does any
child overflow its parent" test returned zero overflowing elements — because the
children fitted the element fine. It was the element that did not fit the grid.
Measuring `dock.right` against `window.innerWidth` is what caught it.

That is the third time this session that a check I wrote agreed with me and the
screenshot disagreed. **The visual pass is not optional and it has to be a subagent.**

Also fixed:
- The register panel rendered as a 400x700 black void when empty, which reads as a
  failed load rather than a zero-result state. It now collapses and says so.
- The register covered the breadcrumb, leaving an orphan "cts · 1.15x" fragment.
  Re-positioned below the chrome.
- The member popover ran past the canvas bottom with no scrollbar: a header reading
  "PERSON · 6" rendered one row. The count and the content disagreed and the reader
  had no way to tell. Now clamped and scrolls.
- The object count sat directly on live map content. Given a backing plate.

**Kept as inherited template, deliberately:** the KPI strip's trailing dead space and
uneven cell widths, the nav dot leaders that terminate in nothing for views with no
count, and the rail clipping at the analyst bar. All three are parent-board shell
behaviour, unchanged from *The Vanishing*, and changing them here would fork the
shared design system for cosmetic reasons.

## Layer 3 — the CEO gate: what could still be wrong

1. **The Sec. 1102 turn-in language has never been read verbatim.** Tier 2, recorded.
   If challenged, the board cannot produce the bill text — only a secondary source
   describing a differently-numbered section of a different bill.
2. **"Twelve seats" is the statutory floor, not the readership.** DoDI 5205.11
   §7.2.a(3) admits staff directors, a security manager and the intelligence
   committees. Any framing that says twelve people is the whole readership overclaims.
3. **`operacao-prato` and `ev-noite-ovnis-1986` are Tier 1 poor.** No SIAN item
   numbers, no primary FAB order, no press-conference transcript. Fragile to a single
   challenge.
4. **`manhattan-project-2` has zero Tier 1 claims** and rests on named proponents.
   Correctly tiered, but it is on the map and will be asked about.
5. **`gerb-mitre-investigation` rests on one podcast** whose speaker's identity is
   unknown.
6. **Single-event sensitivity:** the floor is degree >= 6. Ten L0 nodes sit at exactly
   6. One retracted edge drops any of them off the map and takes its dossier with it.
7. **The 2026-dated material is the freshest and the thinnest.** PURSUE, the ODNI NDA
   waiver memo and the FY2027 amendment all rest substantially on secondary reporting
   because the primary channels do not render.
8. **59% DOCUMENTED is 58.59% rounded.** Correct, but a tie-out question waiting to
   happen if someone recomputes from the claim table.

---

# Stage 11 — the analyst pass and the request queue, 14 August 2026

## The board was used for the thing it was built for

`notes/ANALYST-PASS-2026-08-14.md`. An analyst agent traversed the 4,320 connection
rows, the 110 dossiers and the 674 open questions looking for joins that no single
node states. **7 finds: 5 STRONG, 1 PLAUSIBLE, 1 mixed**, plus four sub-threshold
items and a negative-results section.

**The strongest is a genuine novel join.** John Schuessler appears **twice inside the
same $22M DIA/AAWSAP contract** — as the named author of the BAASS March 2009 monthly
report on Colares, and as the source of Appendix A, the "Schuessler Catalog of
UFO-Related Human Physiological Effects", in the AAWSAP human-effects DIRD whose
stated Hypothesis One is that human injury can be reverse-engineered into propulsion
physics.

His node has **two neighbours** — `betty-cash` and `mufon` — and mentions neither
AAWSAP, BAASS, DIA, Kit Green nor Colares. The board contained every fact needed to
see it and nobody had crossed them. That is the payoff the connection layer was built
for, and it worked on first use.

The finds are **not yet wired as edges.** They are inferences from existing claims and
should be reviewed before they mutate the board.

## The request queue

`notes/REQUEST-QUEUE.md`. 674 open questions triaged into what a person can actually
execute.

```
FOIA / records requests   18   closing ~95 open questions across 45 nodes
archive + manual          11   including all four items automation could not reach
paywalled / purchasable    6   + 1 time-locked (Rice MS 0672, opens 2031)
permanently blocked       11   clusters, each with the reason no document class exists
```

**Highest value: NARA Office of General Counsel, the RG 615 compliance register under
sections 1841-1843 of P.L. 118-31.** Purely administrative records with no
classification equity of their own, closing 14 open questions across 8 nodes. And the
null return is itself the finding: Congress built a records collection with a deadline
and no enforcement instrument.

## The agent corrected me again

I handed it two FOIA case numbers from my own working memory —
`DODOIG-2021-000806` and `APP-00031-2022` — and it refused both, because **neither
appears anywhere in the board data.** The DoD IG case the board actually records is
`DODOIG-2025-000932`. Citing a case number that does not exist in a FOIA request is
exactly the fabricated-source failure this project treats as unforgivable, and it
would have been mine.

Fourth time this session an agent has contradicted its own brief and been right.
