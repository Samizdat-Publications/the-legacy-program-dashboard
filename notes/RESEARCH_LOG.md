# THE PROGRAM — Research Log

**A companion board to *The Vanishing*** (`Samizdat-Publications/the-vanishing`)
**Owner:** Stewart
**Started:** 2026-08-12

---

## What this is

*The Vanishing* tracks deaths and disappearances of scientists and defence-adjacent
technical staff. This board reuses its engine and schema to track a different subject:
**the legacy UAP recovery and reverse-engineering program, and the disclosure movement
fighting to expose it** — 1940s through 2026.

Nodes: people, institutions, FFRDCs, programs, contractors, locations, research domains,
legislation, documents, events. Edges: who worked where, who funded whom, who told whom,
who holds what, and who denied it.

## Editorial stance — the thing that most distinguishes this board

*The Vanishing* holds a case open and lets a prosaic explanation stand where it holds.
**This board does not.** It is built from the premise that a legacy recovery and
reverse-engineering program exists, has existed since the 1940s, and has been deliberately
concealed from Congress and the public. The research question is not *whether* — it is
**who, where, under what authority, and paid for how.**

Official denials are recorded in full, with sources, but as **artifacts of the concealment
effort** — not as counterweights. That is what the `coverup` strand and the `denial` edge
type exist for. A denial is data about the denier.

The one thing that does not bend: **no invented sources, no invented URLs, no invented
document numbers.** Unsourceable material goes in `unverified[]` or becomes a tier-3
inference with the reasoning stated. The tier system is **ammunition grading, not hedging** —
Tier 1 is what survives a hostile audit, Tier 3 is where the research goes next.

---

## Schema

Full spec in `SCHEMA.md`. It records the parent board's schema verbatim, then defines
the deltas. Summary of what changed:

| | The Vanishing | The Program |
|---|---|---|
| **Axes** | S sequence anomaly · P program proximity · I institutional channel | **C** custody proximity · **A** access level · **D** disclosure role |
| **Tier A** | contains a specific unexplained fact | named in sworn testimony or primary docs as directly inside the program |
| **Tier B** | unresolved, prosaic explanation not ruled out | documented channel and capability, program role indicated |
| **Tier C** | conventional explanation documented and holds | contextual, no direct program linkage on record yet |
| **Clusters** | california · new-mexico · huntsville · northeast | legacy · contractor · ffrdc · ic · oversight · witness · research · media |
| **Strands** | cases · oversight · skeptical | program · witness · oversight · **coverup** |
| **Edge types** | + | added `custody`, `funding`, `denial`, `legislative` |
| **Node classes** | person · institution · program · location · domain | + `legislation`, `document`, `event` |

Unchanged and preserved: `P_()` / `other()` / `E()` helpers, the numeric claim tiers
(1 documented / 2 sourced claim / 3 inference), `{name, url, date}` source records,
`chronology[]` with `precision`, `ENTITY_INFO` / `ENTITY_SOURCES` side tables, and the
rule that **derived edges come from rules and program edges are hand-written and sourced**.

---

## Session history

### Session 1 — 2026-08-12

**False start, corrected.** Located a public repo (`ginkgoplicata/missing-scientists`)
by search and read its schema before confirming ownership. Stewart flagged it — not his.
The real repo is `Samizdat-Publications/the-vanishing`; he supplied a zip.
*Lesson for future sessions: confirm repo ownership before reading a schema off it.*
Note: this session's `GH_TOKEN` authenticates as **Samizdat-Publications** but is scoped
to pre-configured repos only — it returns 403 uniformly, so it cannot be used to
discover repo names. Ask for the URL.

**Also corrected mid-session:** the initial research brief was written balanced/both-sides.
Stewart redirected to the pro-disclosure stance above. Wave 1 was killed and relaunched.

Completed:
- Read the real schema out of `the-vanishing-v2.html` (PEOPLE, INSTITUTIONS, PROGRAMS,
  LOCATIONS, DOMAINS, ENTITY_INFO, ENTITY_SOURCES, PROGRAM_EDGES, EDGE_TYPES, TIERS,
  AXES, CLUSTERS, TIMELINE, STRANDS, PRECEDENT, the P_/other/E helpers).
- Wrote `SCHEMA.md` v2.
- Launched wave-1 research across 14 domains:

| slug | domain |
|---|---|
| `grusch` | The central witness node — ICIG complaint, testimony, the ~40 referred witnesses |
| `elizondo-ttsa` | Elizondo, TTSA, the Dec 2017 break, the Gough reversal |
| `aawsap-aatip` | The money trail: Reid earmark → DIA AAWSAP → BAASS → the 38 DIRDs |
| `uaptf-aaro` | UAPTF → AOIMSG → AARO, read as containment; the Yankee Blue admission |
| `ffrdcs` | **MITRE priority** + Aerospace, RAND, APL, Sandia, Battelle, IDA — the legal seam |
| `primes-custody` | **Priority.** Lockheed/Skunk Works, EG&G, SAIC et al. and the custody chain |
| `congress-house` | The Oversight hearings, the caucus, the stonewalling record |
| `congress-senate-legislation` | UAPDA and its eminent-domain provision; what Turner/Rogers stripped |
| `history-1940s-1960s` | Roswell → Twining → Blue Book → Robertson Panel → JANAP 146 → Bolender memo |
| `history-1970s-2000s` | Moon Dust, Rendlesham, Bennewitz/Doty, SRI, Rockefeller, Wilson-Davis |
| `releases-2023-2026` | **Priority.** The PURSUE tranches, AARO reports, the NARA collection |
| `media-structure` | **Priority.** Jesse Michels' structural model; UAP Herb on MITRE |
| `aviators-incidents` | Nimitz, Roosevelt, the incursions, the confiscated data |
| `scientists-technical` | Puthoff, Davis, Nolan, Vallee — and the material custody chains |

- Queued a completeness critic to write `notes/WAVE2_WORKORDER.md`.

**Environment note:** agent concurrency in this container caps at 2, so a 14-agent wave
runs mostly serially. Budget hours, not minutes, for a full wave.

### Session 1 — wave 2 and remediation (same day)

Wave 2 ran 8 tasks against what wave 1's critic exposed, rather than more of the same:
`w2-agencies` · `w2-places-events` · `w2-sap-architecture` · `w2-black-budget` ·
`w2-international` · `w2-retrieval-literature` · `w2-taxonomy` · `w2-2025-2026`.

Then a remediation pass:

- **Tier honesty check, now automatic.** `merge.py` demotes any Tier 1 claim whose node
  carries no primary-record URL, or which is cited to an encyclopedia, video or blog.
  209 claims demoted, flagged in place, logged to `tools/DEMOTIONS.json`. This re-runs on
  every merge, so a claim cannot be promoted back to Tier 1 without a real primary URL
  being added to the node — the promotion would simply be reversed.
- **Structural stubs.** 77 ids were referenced but never defined. The 12 research domains
  carrying the most references got real hand-written descriptions, since the scoring axes
  hang off them. The remaining 65 got stubs with `desc: null` — the parent board's own
  convention for printing a stated gap rather than empty space. Dangling references: 0.

Final session-1 state: **249 people · 662 entities · 1,553 edges · 3,311 claims
(T1 1,781 / T2 1,094 / T3 436) · 749 timeline events · 801 unique source URLs.**

All six generated JS modules import clean under Node.

Pickup list: `notes/WAVE3_QUEUE.md`.

---

## Where to go next

`notes/WAVE2_WORKORDER.md` is regenerated each wave and is the authoritative pickup list.
Standing gaps to keep pressure on regardless of what it says:

1. **Dangling edge endpoints.** Every edge whose `a`/`b` has no node is someone named but
   never given a dossier. Highest value per unit of effort.
2. **The SAP/USAP legal architecture.** How waived-unacknowledged programs are created,
   funded and reported, the Gang of Eight convention, DoD SAPCO, the CAPCO marking system.
   This is the mechanism the entire thesis rests on and — unlike the claims themselves —
   it is fully documentable from statute and DoD directives. Underweighted so far.
3. **Black budget mechanics.** How money reaches a program that does not appear in a
   budget line, and the specific allegation of funds moving to private custody.
4. **International.** UK MoD and the 2000 Condign report; France's 1999 COMETA report and
   GEIPAN; Brazil's Operação Prato and the 1986 Night of the UFOs; Chile's CEFAA;
   Canada's Project Magnet and Second Storey; Japan; Russia.
5. **Crash retrieval literature.** Leonard Stringfield's status reports, Ryan Wood's
   Majic Eyes Only, the Del Rio and Aztec cases — as a sourced claim layer, tiered honestly.
6. **2025–2026.** Always the thinnest part of any model's memory. Re-search every session;
   never write it from recall. The PURSUE tranches especially.
