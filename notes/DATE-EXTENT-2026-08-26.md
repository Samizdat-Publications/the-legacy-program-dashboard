# dateEnd: the row was a category error, and ten near-misses

26 August 2026. The last row of the backfill queue that looked like research.

## What the row asked for

> `dateEnd` — an end year for the 64 nodes that have none.

## Why that is the wrong question

Audited by class, the 64 overwhelmingly **should not have one**:

| class | n | why absence is correct |
|---|---|---|
| institution | 37 | CIA, DIA, NASA, DoD, RAND, MITRE, the House — **still extant** |
| legislation | 8 | a statute does not end unless repealed or sunset. 10 U.S.C. 119 is current law |
| document | 9 | published on a date; no span by nature |
| event | 1 | a point in time |
| program | 9 | every one ongoing, or alleged with no attested end |

Absence is the value, not a hole. A queue row that reads a correct empty field as
missing data is the same mistake as the three stale rows retired earlier today, in the
opposite direction: those listed work already done, this listed work that should never
be done.

## The ten near-misses

Searching every one of the 64 for end-language in its own record returned ten hits.
**Not one is an end for that node:**

| node | the language | what it actually refers to |
|---|---|---|
| `aaro` | "disestablished" | AARO **disestablished AOIMSG**. AARO is live. |
| `cia` | "terminated the programme" | CIA terminated **KONA BLUE** |
| `dia` | "terminated the effort" | DIA terminated **AAWSAP** |
| `fab` | "was shut down" | **Operação Prato** was shut down after four months |
| `ttsa` | "wound down" | the aerospace work wound down and the entity **renamed** itself To The Stars Inc. in 2022 |
| `usc-10-119` | "TERMINATED" | subsections (a) and (b) **reporting requirements** terminated 31 Dec 2021; the statute remains law |
| `cefaa` | "wound up in 1975" | a **predecessor** office. This node starts 1997 |
| `ndaa-fy2026` | "the repealed provision" | a provision it **replaced** |
| `waived-sap-notification-group` | "no sunset" | an **absence** of a sunset |
| `waived-usap-mechanism` | "sunset (eff. 31 Dec 2021)" | the annual **census** sunsetting, not the mechanism |

Pattern-matching would have written **ten false end dates**, each asserting that a live
agency, statute or company had ceased to exist. Three of them — CIA, DIA, the Brazilian
air force — would have been dated by the very act of *their* shutting something else down.

This is the board's own failure mode restated: the language that identifies a denial's
issuer and the language that identifies a node's end look identical from a distance, and
only reading the sentence tells them apart.

## And the 46 that do carry one

Checked for the same error. Most are defensible on inspection — Rendlesham 1980→1981 covers
the Halt memo of 13 January; the Stringfield **series** genuinely runs 1978–1994; BAASS is
effectively defunct. Two are semantically loose and are recorded here rather than silently
rewritten, because changing a date is a sourcing act:

- **`doc-condign-report` / `doc-condign-vol3`, 2000 → 2006-05-15.** The end is the
  **release** date, not an ending. "Written, then withheld, then released" is a real and
  interesting span, but it is not the same relation the other spans express.
- **`aztec-1948`, 1948-03 → 1953.** 1953 is when the claim was publicly exposed, not when
  the event ended.

## One scope correction

`y0`, `y1` and `span` **never reach the page.** They are layout-model fields feeding Design's
brief figures. So this morning's `span: 0` fix — the hardcoded literal that made the model
report zero nodes with an extent when 24 have one — corrected **a figure, not the board**.
Worth saying plainly: nothing a reader sees changed.
