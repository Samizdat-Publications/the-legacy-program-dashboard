# The Air Force enters RG 615, and the lead undercounts it by a factor of ten

**28 August 2026.** Stewart brought a news item: the National Archives had quietly added
**three** Air Force records to the UAP records collection, a 1947 correspondence file on
unidentified flying objects and two wing histories from 1960 and 1964, unrestricted, PDFs
attached.

The lead is real. The count is wrong, and the thing it undercounts is the most consequential
event in RG 615 since the collection opened.

---

## 1. What actually landed

**Thirty records, not three, in one accession, on one morning.**

| | |
|---|---|
| series | Records from the Department of the Air Force Relating to Unidentified Anomalous Phenomena |
| catalog id | 656595571 |
| accession | TR-0615-2026-0003 |
| described from | `NAC_2026-08-27_23.116_DESC_0001.xml` |
| indexed | 2026-08-28 08:30:32 UTC |
| items | 30, extent "30 Portable Document Format (PDF) files" |
| inclusive dates | 25 October 1945 to 31 December 1969 |
| access / use | Unrestricted / Unrestricted |
| disposition authority | DAA-GRS-2024-0002-0001 |
| creators | War Department, Army Air Forces (1941-1947), predecessor; Department of the Air Force (1947- ), most recent |

The three records in the news item are items 26, 14 and 13 of the thirty:
`342UAP00026` Correspondence Regarding Unidentified Flying Objects, 1947; `342UAP00014`
95th Bombardment Wing History, March 1960; `342UAP00013` 78th Fighter Wing, December 1964.
The other twenty-seven include two further UFO correspondence files (1949 and 1952), the
4602d Air Intelligence Service Squadron histories for 1955 and 1956, AFR 200-2 of 20 July
1962, a Curtis LeMay collection, and A Survey of Exobiology, March 1963.

All thirty share the same accession number and the same ingest minute. There was no
three-record addition; there was one transfer, and the report saw a fraction of it.

## 2. Why this matters more than the count

The board carried, on two Tier A nodes, a load-bearing argument that **no military department
had complied**. `nara-rg615` said in terms: "no separate Army, Navy or Air Force series -- the
services appear, if at all, inside OSD." `nara-uap-collection` said "the Departments of the
Army, Navy and Air Force are absent, which means the services that ran Project SIGN, Project
GRUDGE, Project Blue Book and Project Moon Dust have not appeared in the collection created to
hold that history," and closed on "Seven agencies have delivered."

That was accurate when written and is now overtaken. It is corrected in place with both dates
kept, because the correction is the finding: the argument was never that compliance was
impossible, it was that nobody with custody proximity had done it. **One now has.** CIA, DIA,
DOE, NASA, NRO, NGA, DHS, the Army and the Navy still have not, and the Air Force transfer
costs them the structural excuse.

It also half-closes a logged open question. `nara-rg615` asked "whether the Department of
Energy, CIA, DIA, NRO, NGA and the military departments have transferred anything into
RG 615." Half of that is answered, with a date and an accession number.

## 3. Two things in the transfer worth more than the headline

**The declassification block dates the decision fifteen months before the accession.** The
cover sheet of `342UAP00005` carries, printed by the Air Force Declassification Office:

> Authority: FY24 NDAA, now codified at 44 U.S.C. 2107
> Date: 5/05/2025
> Declassified in Full: X
> Case Number: 342UAP00005

Three things follow. The Air Force ran this as a declassification action under the UAP records
statute, not as a FOIA release. The UAP Record Identifier **is** the declassification case
number, so `342UAP00001` to `342UAP00030` is a docket and its contiguity means this is the
whole docket, not a sample. And the decision was taken in May 2025, before the statutory
30 September 2025 transfer deadline, while the records reached NARA in August 2026. Fifteen
months separate the adjudication from the accession, and whatever occupied them was not
review. That is a new open question and it is worth a request.

**The catalog titles cannot be trusted, and one of them is a trap.** Item `342UAP00005` is
catalogued as "Estimate of the Situation, September 8, 1948". Anyone who knows the literature
reads that as the Air Materiel Command estimate that Ruppelt described, the one Vandenberg is
said to have ordered burned, whose non-existence is a fixed point in the field.

It is not that document. Opened, it is **Headquarters Fifth Air Force, Office of the AC of S,
A-2, APO 710**, a 21-page periodic Far East theatre intelligence estimate covering 7 August to
4 September 1948, published for Fifth Air Force Division and Wing-Base Commanders, stamped
SECRET and downgraded under EO 11652. Its table of contents runs Japan, Korea, China,
Philippines, Malaya: Japanese mail reflecting a war scare, a Soviet espionage ring in Tokyo,
the typhoon season forecast, offence rates in the occupation zone. The two coincidences are
the phrase "Estimate of the Situation" and the month.

Eighteen of the thirty items are unit or installation histories of the same shape, where any
UAP content is a passage inside a monthly wing or division history rather than the subject of
the record. **A citation built from this series' catalog titles will misdescribe it.** Read
the PDFs.

*What was read to establish this: the cover, the warning page, the table of contents and
pages 6 and 7 of `342UAP00005`. The remaining pages have not been read, so this note says
what the document is and does not claim what it does or does not contain.*

## 4. What was verified, and how

Everything above comes from NARA's own catalog and from the PDFs, not from the news item and
not from the archives.gov prose.

- `catalog.archives.gov` serves the SPA shell for every `/api/v2/...` and `/id/...` path from
  this environment, so the documented API is unreachable here. **The working channel is
  `https://catalog.archives.gov/proxy/records/search?q=<naid>&limit=50`**, which returns the
  catalog's own JSON, series and items together, with digital object URLs. Worth keeping.
- All 30 PDF URLs were probed with a **ranged GET**, not a HEAD, per the rule in CLAUDE.md §9
  that a HEAD-only probe already hid a dead link once. All 30 returned 206 with `%PDF` magic.
  Zero dead.
- `342UAP00005` was downloaded in full (9.4 MB, 48 scanned pages, no OCR layer) and rendered
  to PNG to be read. There is no text layer in this series; anyone planning to search it will
  need to OCR it first.
- The three-record claim was tested rather than assumed: it fails because all thirty items
  carry one accession number and ingest timestamps inside two seconds of each other.

## 5. What changed in the repo

| file | what |
|---|---|
| `research/w2-2025-2026.json` | `nara-rg615` desc corrected; the "seven agencies" claim becomes eight; the T3 absence claim re-dated and narrowed to Army and Navy; 7 new T1 claims; the `tl-nara-deadline` timeline event re-dated; a new `tl-af-rg615-transfer` event for 28 August 2026; the 2026 thesis in `entityInfo` corrected |
| `research/dossiers/w5-batch-09.json` | `nara-rg615` dossier: whyImplicated and narrative corrected, three new paragraphs on the transfer, open question 5 marked half-closed, two new open questions, 7 new claims |
| `research/dossiers/w4-entity-dossiers-1.json` | `nara-uap-collection` dossier: whyImplicated, the absences paragraph and the closing line corrected; open question 1 re-counted; 7 new claims |
| `research/w2-agencies.json` | `nara-uap-collection` entity: 7 new claims |
| `tools/GOLDEN.json` | deliberately re-baselined: timeline 858 -> 859, T1 claims 2772 -> 2786, unique source URLs 1225 -> 1227, L0 dossier claims 1548 -> 1562. Nothing else moved |
| `notes/NARA-AIRFORCE-2026-08-28.md` | this file |

The golden manifest caught this before it shipped, which is the tripwire doing its job: the
first gate run after the edit came back `verify FAIL`, `runtime_check FAIL`, `--idempotent
FAIL`, all three naming the same four counts. Every one of the four moved by exactly the
amount the edit accounts for, so `--update-golden` was the right answer rather than a bug.
Anyone re-running this should check that arithmetic before accepting a new baseline.

The patch script asserted on every replacement and refused to run on a miss or an ambiguous
match, which is the same discipline as a self-tested check: a replacement that silently
matched nothing is the failure this repo keeps hitting.

## 6. One side effect worth Stewart's eye, not a fix from here

Adding seven claims to `nara-rg615` moved it from **B to A**, and moved `pete-hegseth` from
**A to B**. Neither was intended and neither is a bug.

`tools/regrade.py` grades on a global ranked pass with fixed proportions:
`TARGET = {"A": 0.15, "B": 0.35, "C": 0.50}`, so at 956 nodes the A band is exactly ranks 1
to 143. The bands are zero-sum. Part of a node's score is claim weight -- three points per
Tier 1 claim, capped at 45 -- so `nara-rg615` climbed from below the line to rank 123 on the
strength of the new research, and the node that had been sitting at rank 143 was pushed to
144. That node was Hegseth, at score 47 against the new occupant's 54.

| node | before | after | rank | score |
|---|---|---|---|---|
| `nara-rg615` | B | **A** | 123 | 54 |
| `pete-hegseth` | A | **B** | 144 | 47 |

The mechanical part is unarguable. The question it raises is not, and it belongs to Stewart:
**CLAUDE.md §6 says node tier is proximity to the programme, not credibility and not
prominence -- but claim weight means a node also rises because somebody wrote about it.** A
session that spends an afternoon on one node can promote it past a node nobody has worked on
lately, and at the boundary that demotes a real third party. Hegseth did not become less
proximate to the programme today; a NARA node got seven new citations.

Three things could be true and this note does not choose between them: the claim-weight term
is doing legitimate work, because a node with more documented links to the programme probably
is more proximate; or the cap at 45 is too loose and research effort is leaking into a
proximity measure; or the fixed proportions should be a score threshold instead, so a rise
does not have to displace anybody. **No tier was hand-edited to avoid this**, because the
repo's standing rule is not to silence a pin that is working. It is reported instead.

## 7. What is left

1. **The other 29 PDFs have not been read.** Eighteen are unit histories and the UAP passage
   inside each is the actual content; nobody has located those passages. This is the research,
   and it is now available without a FOIA request.
2. **Fifteen months between declassification and accession.** `notes/REQUEST-QUEUE.md` §1 item
   1 is already a NARA request for the RG 615 compliance register. This transfer gives it a
   concrete hook: ask for the transmittal correspondence for TR-0615-2026-0003 and the dates
   of the Air Force's section 1842(c)(1) certification.
3. **Whether thirty is the whole Air Force return.** The docket is contiguous, which suggests
   it is complete as a docket, but AFOSI and AFHRA Maxwell hold more. REQUEST-QUEUE §1 items
   10, 15 and 18 all target the Air Force and should be re-read against this.
4. **No image work was done here.** Several of these are scanned federal works and would clear
   17 U.S.C. 105 for `data/l0-images.json`, but that is the image pass, not this one.
