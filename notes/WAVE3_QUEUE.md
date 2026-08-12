# Wave 3 queue — pick up here

Generated 2026-08-12 at the end of session 1, after waves 1 and 2 and the tier
remediation pass. Board state at handoff:

| | |
|---|---|
| people | 249 |
| entities | 662 (161 institution · 158 document · 95 location · 72 event · 70 program · 56 domain · 50 legislation) |
| edges | 1,553 |
| claims | 3,311 — **T1 1,781 · T2 1,094 · T3 436** |
| timeline | 749 events |
| unique source URLs | 801 |
| **dangling references** | **0** |

Everything the graph points at now resolves. What remains is depth, not coherence.

---

## Do these first

### 1. Re-source the 209 demoted Tier 1 claims — `tools/DEMOTIONS.json`

The merge now runs an automatic honesty pass: a Tier 1 claim promises a primary
record exists, so any Tier 1 claim whose node carries no primary-record URL, or
which is cited to an encyclopedia, video or blog, is demoted to Tier 2 and flagged
in place. 209 claims were demoted.

Split: **152** because the node carried no primary-record URL at all, **57**
because the citation was encyclopedic or secondary.

Worst offenders, and all of them are recoverable:

| node | demoted | where the primary record actually lives |
|---|---|---|
| `doc-cometa-report` | 8 | The 1999 COMETA report itself — find a hosted PDF and cite pages |
| `ttsa` | 6 | SEC filings (TTSA was a public reporting company — EDGAR has them) |
| `uap-science-advisory-council` | 6 | The chartering document, if one exists |
| `geipan` | 6 | CNES/GEIPAN's own case database, which is public |
| `kit-green` | 5 | The DIRDs themselves; his published papers |
| `ttsa-army-crada` | 5 | **Priority** — see item 2 |
| `yankee-blue` | 5 | AARO Historical Record Report Vol I, cite the page |
| `dird-green-clinical-medical` | 5 | The released DIRD PDF |

Rule to keep: never re-promote a claim to Tier 1 without pasting the primary URL
into the node's `sources[]`. The demotion logic re-runs on every merge, so a
promotion without a source will simply be reversed.

### 2. Two dead TTSA URLs under a custody claim

`dpo.tothestarsacademy.com` links return HTTP 000 and they are carrying the Army
CRADA custody chain — the single worst place on the board to have a dead link.
Replace with the Army's own CRADA announcement, the DEVCOM press release, or an
archive.org capture. Do this before showing the board to anyone hostile.

### 3. Archive the government URLs

~130 URLs were bot-blocked at verification time and could not be confirmed. Every
`.mil` and `war.gov` link in particular should be mirrored to archive.org and the
snapshot URL stored alongside the live one. Agency sites reorganise constantly and
`war.gov` is itself the product of a 2025 renaming — these links are fragile.

### 4. The 2026 presidential directives — resolve the instruments

`trump-uap-release-directive-2026` and `uap-nda-waiver-directive-2026` are sourced
to DefenseScoop, Fox News and a Burlison House press release. That is real
reporting, and the nodes are correctly Tier 2. What is missing is the **signed
instrument**. Search the Federal Register, whitehouse.gov/presidential-actions and
the DoD issuances site. If a signed instrument exists, these become the strongest
Tier 1 nodes on the current-events end of the board. If none exists, say so
explicitly in the desc — "reported by X, no signed instrument located as of
[date]" — because that absence is itself informative.

---

## Then these

### 5. 65 structural stubs need real dossiers — `tools/INTEGRITY.json` → `entity_without_desc`

These were created deliberately with `desc: null` so the graph resolves and the dock
prints them as a **stated gap** rather than as empty space — the parent board's own
convention. They are honest placeholders, not fake content. Highest value first:

- `ndaa-fy2023` — a statute, trivially sourced from congress.gov, referenced by 3 edges
- `pogo`, `the-intercept` — organisations doing real work in this space
- `saf-aaz` — the USAF declassification and special programs office; genuinely important
- `509th-bomb-group` — the Roswell unit; belongs in the legacy cluster properly
- `l-washington-dc` should be **merged into `l-dc`**, not written twice
- The foreign locations (`l-brasilia`, `l-paris`, `l-toulouse`, `l-ottawa`, `l-santiago`, `l-moscow`) attach to the international domain from wave 2
- The remaining ~45 single-reference US locations are low priority

### 6. 40 people with no `date`

`date` is the primary timeline sort key, so a person without one cannot be placed.
Includes `mark-skidmore`, `catherine-austin-fitts`, `laurence-kotlikoff`,
`steven-aftergood`, `steve-feinberg`. Also note the `p-` prefix on a few ids
(`p-alexandro-wiggins`, `p-jeffrey-nuccetelli`, `p-dylan-borland`, `p-joe-spielberger`) —
inconsistent with the rest of the board; normalise them.

### 7. 35 thin-sourced people (fewer than 2 sources)

`jason-turner`, `clay-higgins`, `jamie-raskin`, `mike-gallagher`, `william-mccasland`,
`thomas-crosson`, `joseph-gradisher`, `jeffery-langhout`, `donald-kerr`, `edward-teller`,
`jonathan-grey`. Most are trivially fixable — the legislators from congress.gov, the
DoD spokespeople from their own on-record statements.

Worth noting: **`william-mccasland` also appears in The Vanishing** as a MISSING case.
He is a genuine cross-board node and the two dossiers should be reconciled rather
than maintained separately.

### 8. 202 Tier A nodes with degree < 3

A Tier A node is one named in sworn testimony or primary documents as directly inside
the program. If it has fewer than three edges, either the tier is too generous or the
edges were never drawn. Both are worth finding out. Run a cross-domain edge sweep —
most of these are real hubs that individual domain agents saw in isolation.

---

## Still uncovered

Wave 2 closed international, SAP architecture, black budget and retrieval literature.
Still missing entirely:

1. **IC counterintelligence and the disinformation apparatus** as its own domain —
   the Bennewitz operation is in the board but the broader apparatus is not.
   `PRECEDENT` should be extended from here too.
2. **The aerospace-industry insider layer** — mid-level engineers and program managers,
   as distinct from the executives and the primes.
3. **Reconciliation with The Vanishing.** Both boards now contain `william-mccasland`,
   `david-grusch` and `pursue-releases`. Decide whether they share an id space. If they
   do, this becomes one graph with two views, which is considerably more powerful than
   two graphs.
4. **The FY2027 NDAA cycle** — will be live by the time anyone reads this.

---

## Environment notes for the next session

- **Web search budget is 200 calls per session and wave 1 consumed all of it.**
  Wave 2 agents fell back to WebFetch and the TinyFish search skill and still
  produced, but *discovery* was degraded — which matters most for 2025–2026 material.
  Raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` before starting a research wave.
- **Agent concurrency caps at 2** in this container. A 14-agent wave takes ~6 hours.
  Budget accordingly; it is not stuck.
- **Agents write to `research/` and will create subdirectories there.** One deleted the
  build directory mid-run. Build tooling now lives in `tools/`, deliberately separate.
- Tell research agents to **write their JSON incrementally**. Wave 1 agents accumulated
  650KB+ transcripts before writing; anything that ran out of context would have lost
  everything.

## Rebuilding

```bash
python3 tools/make_stubs.py   # only if new dangling refs appear; needs /tmp/missing.json
python3 tools/merge.py        # always — regenerates data/*.js and all reports
```

`merge.py` writes `tools/INTEGRITY.json`, `tools/DEMOTIONS.json`, `tools/REJECTS.json`
and `tools/GAPS.json` (329 gaps stated by the research agents themselves — a rich
source of wave-3 work in its own right).

---

# Appendix — wave-2 agent gap reports

These are the researchers' own stated gaps, verbatim. They are the richest lead list
on the board: named documents, FOIA targets, specific archives, and yes/no questions a
committee could actually demand an answer to without breaching a compartment.
Treat this as the wave-3 research backlog.

## `w2-agencies` — 2 people, 27 entities, 93 edges

- Names of the DHS Under Secretary for S&T who established KONA BLUE as a PSAP in 2011 and the DHS Deputy Secretary who terminated it ~6 months later — both withheld from the released AARO/DHS paper
- Identity of the current Director, DoD SAPCO and the office's org chart; no SAPCO director has ever appeared before Congress in open session
- Whether any UAP-related activity has ever been the subject of a 10 U.S.C. 119(e) waiver — a yes/no a committee could demand without breaching the program
- The complete list of programs AARO reviewed via the DoD/IC/DHS SAP control office partnership, and the criteria for 'pertinent'
- Whether DOE holds UAP material under Restricted Data authority; AARO's only documented DOE approach was a request for NDAs, and DOE sent nothing to NARA
- Findings of DODIG-2023-109 — classified in full; scope, components reviewed and SAP access all withheld
- NGA's UAP holdings: named a 2021 ODNI contributor, but no FOIA collection, no NARA transfer, no testimony, no litigation
- The unredacted Yeates affidavit and the count/nature of NSA documents withheld in CAUS v. NSA (Civil Action No. 80-1562)
- Whether AFOSI disinformation authority comparable to the 1980-83 Bennewitz operation has been exercised since; the YANKEE BLUE memo search was reopened Dec 2025 with no published result
- AFRL's UAP-relevant holdings at Wright-Patterson — no release, no testimony, no transfer, despite being the continuity organisation for foreign materiel exploitation
- NRO's own UAP records: named 2021 contributor and parent of the principal witness, yet nothing transferred or published
- Whether ISOO has ever examined UAP classification decisions or run any NISP review touching alleged contractor-held material
- Text of the February 2026 presidential UAP directive and the NDA-waiver directive, and whether either purports to reach Restricted Data or only EO 13526 information
- The DoD SAPCO congressional-engagement log: how many notifications of intent to brief Congress on UAP-adjacent SAP matters, and whether any briefing was blocked

## `w2-places-events` — 0 people, 39 entities, 93 edges

- THE TWELVE-PAGE DOCUMENT. The Immaculate Constellation report was entered into the Congressional Record on 13 Nov 2024 and appears in the hearing's Index of Documents, but no retrievable primary file at a stable public URL was located. Obtaining the submitted-materials section of GPO CHRG-118hhrg57440 is the highest-value next step.
- THE DEPARTMENT'S WRITTEN RESPONSE TO IMMACULATE CONSTELLATION. No written DoD, OUSD(I&S) or AARO response exists publicly; the 'no record' formulation is known only through press statements attributed to Sue Gough. FOIA for any records-search declaration or classification review would establish whether one was ever done.
- PRINCETON SENSOR DATA AND THE CONFISCATION. No FOIA release, visit log, deck-log entry or message traffic identifies the personnel who allegedly boarded USS Princeton c.15-16 Nov 2004 or their authority; the Navy has never produced SPY-1B/CEC data for 14 Nov 2004. Targets: Princeton deck logs 14-18 Nov 2004, CSG-11 message traffic, the Third Fleet reporting file.
- THE VANDENBERG RECORDS. Nuccetelli testified 9 Sept 2025 that official Air Force records for the 14 Oct 2003 and 2005 incidents are 'held by AARO and the FBI'. No FOIA production from either custodian has surfaced and Congress has not compelled one.
- WRIGHT-PATTERSON T-2 FILES, 1947-1951. The Air Materiel Command T-2 intelligence series has never been subject to an identified comprehensive declassification review or NARA accession; no finding aid located.
- AAWSAP/BAASS RESEARCH PAPERS. Three dozen preliminary reports, 100+ research papers and the 240,000-case Vallee-designed data warehouse remain unreleased by DIA; current custody of the warehouse is unestablished.
- GVSC/TTSA CORRESPONDENCE. Twenty-nine emails totalling 100 pages withheld in full under FOIA (b)(4) and (b)(5); no CRADA characterisation results ever published.
- NO 2026 UAP HEARING. None held between 9 Sept 2025 and 12 Aug 2026 despite the Feb 2026 release directive, five PURSUE tranches, the late FY2025 AARO report, the July 2026 NDA waiver and the Burlison FY2027 NDAA amendment.
- THE SCHRIEVER PROVENANCE CLAIM. The 2025 '2018 Schriever Wargame' folder assertion is from an unnamed self-identified whistleblower and addresses a later provenance story, not Shellenberger's sourcing; the claimant's identity and relationship to Shellenberger's source are unestablished.
- PROJECT TWINKLE AND THE LAND-AIR OBSERVATIONS. The White Sands cinetheodolite tracking-camera observations of 1948-1951 and the full Twinkle case file were not retrieved from a primary archive.
- HANGAR 18. No primary record establishes storage of recovered material at Wright-Patterson Area B; recorded as folklore, with the NASIC custody argument standing independently.
- JANET AND THE GROOM WORKFORCE. Contractor of record, headcount and contract vehicle for the Las Vegas-Groom Lake air shuttle are unpublished; the number would quantify how large a population has demonstrably kept a compartment quiet.

## `w2-sap-architecture` — 0 people, 37 entities, 77 edges

- Number of DoD SAPs currently designated waived under 10 U.S.C. 119(e) - a retrievable record, since DoDI 5205.11 Encl. 3 gives the Senior Review Group an annual review of all waived SAPs and requires it to certify the congressional SAP list
- The signed carve-out approvals and the DoD SAPCO-held list of carved-out contractor facilities, both required to exist by DoDI 5205.11 Enclosure 7 and Enclosure 2 para 2.k; never published or FOIA-released
- Identity of the current Director of DoD SAPCO and the office's org chart, staffing and budget; no SAPCO director has ever testified in open session
- DoDM 5205.07 Volumes 2, 3 and 4 - live esd.whs.mil URLs for all four volumes fail public retrieval as of 12 Aug 2026; only Volume 1 recovered, from a 2019 Internet Archive capture
- Exact signature date and signer of the reissued ICD 906 (PDF generated 19 Dec 2024, supersedes the version signed 17 Oct 2015; signature block is an unresolvable image)
- The classified addenda to the CAPCO markings register - the public register states on its title page that markings were removed for classification and compiled separately
- The 50 U.S.C. 3348 annual SAP reports owed by every non-DoD, non-NNSA, non-IC agency to congressional oversight committees expressly including House Oversight; none publicly identified and the entitlement appears never to have been invoked in the UAP context
- The FY2024 IAA sec. 7606(c) SAP access-population reports due 22 Dec 2024 from each of the six E.O. 13526 SAP-creating officials; none surfaced publicly
- Whether any 10 U.S.C. 119(e) waiver has ever been exercised for a UAP-related program, and whether FY2024 NDAA sec. 1687 / IAA sec. 7343 have ever been triggered or complied with
- GAO and DoD IG coverage of the SAP enterprise: the only located GAO product on contractor industrial security (GAO-04-332) expressly excluded SAPs by agreement with committee staff; no GAO product auditing SAP congressional reporting, carve-out administration or the waived list was located in govinfo's GAOREPORTS collection
- Total inventory of accredited SAP facilities (SAPFs), including contractor SAPFs, never published even in aggregate
- The Prospective SAP (PSAP) register - programs terminated as PSAPs before approval (as KONA BLUE was at DHS) never appear in any SAP report to Congress; no PSAP register released
- Named individuals occupying SAPOC and Senior Review Group seats on any given date - reconstructible from public appointment records since the seats are defined by position in DoDI 5205.11 Enclosure 3, but not yet reconstructed

## `w2-black-budget` — 9 people, 32 entities, 56 edges

- Contents of the classified annex to the annual Defense Appropriations Act and of the classified Schedule of Authorizations to the Intelligence Authorization Act - both given the force of law by public statute (Sec. 8006(a) of P.L. 119-75; Sec. 6102(a) of P.L. 119-60) while being unpublishable by statutory command.
- Whether any Inspector General has ever conducted a compliance review of NDAA FY2024 Sec. 1687(b), the permanent prohibition (50 U.S.C. 3373 note) on UAP-related independent research and development being an allowable indirect cost. No published DoD OIG, IC IG or DCAA product examines it. Most answerable open question on the board.
- Identity of contractors, if any, that have charged UAP-related work to IR&D accounts. DCAA audits IR&D cost allowability and its working papers are agency records; the DoDI 3204.01 technical interchange meeting record is also an agency record.
- Whether any UAP-related activity has been the subject of a 10 U.S.C. 119(e) waiver removing it from the annual SAP report to the defense committees, or of a Sec. 8009 thirty-day pre-initiation notice.
- The recipient of the $26.92 billion Other Procurement, Air Force 'CLASSIFIED PROGRAMS' line (FY2026 line 077A) and the content of the adjacent $1.178 billion 'SPECIAL UPDATE PROGRAM' line. Pass-through attribution to national reconnaissance is inference from account history and magnitude, not documentation.
- Reconciliation between the ~$95.9 billion of classified line items in the FY2026 defense funding tables and the $115.5 billion combined NIP+MIP request for the same year. No public document maps one onto the other or explains the gap.
- Names of the DoD officials who approached FASAB in August 2016 to request what became SFFAS 56, and the 17 comment letters received on the exposure draft (14 Dec 2017 - 16 Mar 2018). FASAB's deliberative record is public and has never been read against this question.
- Whether FASAB has issued any Interpretation of SFFAS 56 under paragraph 8(c), which authorises modifications beyond those listed in paragraph 9. Paragraph 13 forbids the government-wide report from identifying which Interpretations were applied.
- Which entities have actually applied SFFAS 56 and to what amounts - unknowable from financial statements by design, since paragraph 12 expressly forbids disclosure of application.
- Underlying journal voucher detail behind DODIG-2016-113's $2.8 trillion and $6.5 trillion figures and behind the FY2025 audit's $859 billion. The transaction-level records exist in DFAS systems and have never been sought by FOIA or subpoena in this connection.
- Which independent public accounting firm assumes the group auditor role for the Department's financial statements in FY2027, under what contract vehicle, and what happens to working-paper custody when the group auditor is a contractor rather than the OIG.
- The classified portion of David Grusch's testimony and of the ICIG's July 2022 credible-and-urgent determination, where the financial specifics he declined to give in open session reside.
- Whether the House Committee on Oversight and Government Reform has ever, in writing, connected its July 2023 UAP hearing to its May 2026 Department of War financial management hearing. Both are its own proceedings; no published question, letter or report joins them.
- Dates of Platte B. Moring III's assumption of office as Inspector General and of Michael Powers's acting service as Under Secretary (Comptroller), and whether either is Senate-confirmed. The Department's own biography pages do not state it.
- Any record of expenditure under 50 U.S.C. 3510(b), the CIA's unvouchered account, relating to material recovery or exploitation. By statute the Director's certificate is the entire accounting record and 'shall be deemed a sufficient voucher'.

## `w2-international` — 19 people, 39 entities, 65 edges

- Exact Library and Archives Canada file citation for Wilbert Smith's 21 November 1950 'Geo-Magnetics' memorandum unconfirmed — LAC's own exhibition quotes and dates the memo but cites only the DRB file (RG 24, acc. 83-84/167, box 7523, DRBS 3800-10-1 pt.1); the DOT file (commonly given as RG 97) must be confirmed before the 'higher than the H-bomb' four-point passage can be graded tier 1. Highest-value verification task on this board.
- The four redacted lines after Condign Vol.3 para 12's denial of any UK–US–Canada exchange 'of any sort', plus redacted para 7 'Related Military Applications' and para 6 'Radar Detection of Plasmas', have never been challenged by a fresh FOI review.
- The circulating English COMETA translation renders the key conclusion as 'The extraterrestrial hypothesis is far from the best scientific hypothesis', contradicting the paragraph above it and August 2026 press renderings of 'by far the best'. Original French text needed for collation.
- Nick Pope's precise MoD post title, grade and division designation never confirmed from a primary MoD document; he died 6 April 2026. Paywalled obituaries (Telegraph 10 Apr, Times 15 Apr, Economist 16 Apr, NYT 28 Apr 2026) unread; personal papers should be traced.
- Operação Prato file at the Arquivo Nacional not worked page by page. The official negative finding and Hollanda's 1997 interview cannot both be true. Hollanda's exact death date and any inquest also unestablished.
- The 30-day dossier promised by Brazilian Air Minister Moreira Lima on 23 May 1986 never appeared; whether one was written and withheld is answerable at the Arquivo Nacional.
- Adenir Britto's 19 May 1986 photographic negatives, taken by two CTA officers with James J. Hurtak on the stated basis that NASA would analyse them, were never returned — present location unknown, live custody question.
- Spain's 66 released MoD UFO files, recorded inside Condign Vol.3, not located or worked; Ejército del Aire archival references and release dates needed.
- No primary Russian-language citation obtained for the SETKA founding documents, the 18 October 1978 Academy of Sciences meeting minutes, or the Military-Industrial Commission order; the relationship between 'Institute 22', SETKA-AN/MO, Galaktika, Gorizont and military unit 67947 is unresolved.
- 'Thirteenth Department' could not be tied to any documented Soviet body and has deliberately not been asserted; military unit 67947 is the concrete lead.
- Japan's May 2026 statements rest on Kyodo/Japan Times headlines indexed via Google News — article bodies unreachable (paywall/bot protection). Japanese MoD primary statements needed.
- Peru's Air Force UAP office (OIFAA/DIFAA) is a placeholder: founding instrument, current name, reporting line and case output all unestablished.
- Argentina has no institutional entity beyond the 1995 Bariloche case; the Fuerza Aérea Argentina's CEFAe/CIAE lineage needs research.
- No NATO institutional position on UAP located — the alliance appears only indirectly via Condign's reference to 'other NATO nations' and member-state bilateral behaviour. Whether any NAC or Military Committee document exists is unanswered.
- Exact CEFAA case reference and the Chilean Navy's own report on the November 2014 FLIR case not located; account rests on January 2017 press reporting.
- Whether Canada has designated a lead department in response to the Sky Canada Project's June 2025 recommendations, as at August 2026, is unestablished.

## `w2-retrieval-literature` — 25 people, 28 entities, 68 edges

- The 341st Strategic Missile Wing unit history and launch-crew rosters for March 1967 have never been released — the single document that would settle Echo vs Oscar Flight, the 16 vs 24 March date, and the recorded cause of the Minuteman shutdown
- NASA's two missing boxes of Kecksburg-era records, testified to by liaison officer Steve McConnell in Kean v. NASA, were never located despite a 22-month court-supervised search; the joint status reports at docket entries 58-68 were not examined
- No document from the Defense Department's internal investigation into whether the Cash-Landrum object was a US military device has ever surfaced, although the investigation is referenced in the litigation record
- The Secretary of the Air Force's express written direction releasing former airmen and contract scientists from nondisclosure obligations (cited in the July 1994 Roswell report) has never been published and appears never to have been FOIA'd
- No Pennsylvania State Police or Army Corps of Engineers record of the December 1965 Kecksburg cordon exists in any release, despite the cordon being reported contemporaneously by the Greensburg Tribune-Review as ordered by Army and State Police officials
- Rodeghier and Whiting's 'The Plains of San Agustin Controversy' (1992) was read only as cited at note 123 of the 1997 Air Force report, not in the original
- No AFOSI record of the relationship William L. Moore described in July 1989 has ever been requested or released — the highest-value outstanding FOIA target, since it would establish whether the MJ-12 corpus entered via an official channel
- Stringfield's anonymised informants are coded by letter-number; whether his working files survive and whether any key mapping codes to names exists is unestablished, leaving six of seven Status Reports permanently uncheckable
- The Brazilian Army's 2010 Varginha inquiry explained the vehicle movements but did not publish the underlying unit movement logs for 20-21 January 1996
- Robert Willingham's Del Rio claims have been restated with materially different dates, locations and service roles, and his stated record is contested; no stable version exists to test
- The 108-document Blue Book file set and NARCAP's 141-document set on the 24 October 1968 Minot case were not read in the original; the internal routing of Blue Book's decision not to field-investigate is a reachable target

## `w2-taxonomy` — 0 people, 104 entities, 61 edges

- ALIAS PAIRS REQUIRING MERGE: five domain id pairs are near-synonyms and were both defined so no edge dangles - d-legislative/d-legislation, d-funding/d-money, d-secrecy/d-secrecy-architecture, d-contractor/d-contracting, d-ffrdc/d-ffrdc-mechanism. Each written with a deliberate division of labour so both survive if the board prefers granularity.
- FOUR DOMAINS ALREADY DEFINED ELSEWHERE, NOT REDEFINED HERE: d-ffrdc, d-structure, d-media (ffrdcs.json, media-structure.json) and d-custody (scientists-technical.json). d-materials WAS redefined because it is in the required list and must be reconciled with the scientists-technical.json version. media-structure.json also carries a bare id 'ffrdc-mechanism' while a record references 'd-ffrdc-mechanism' - a prefix inconsistency to normalise.
- NINE DOMAINS DEFINED FORWARD, NOT BACKWARD: d-intel, d-nuc, d-plasma, d-chem, d-consciousness, d-remote-viewing, d-signals, d-aerospace, d-counterintel are not yet referenced by any wave-1 person record. A backfill pass should add them to existing domains[] arrays - aviators almost certainly need d-signals, scientists need d-chem and d-astro.
- THE C AXIS IS UNDER-EVIDENCED WHERE IT MATTERS MOST: d-legacy, d-recovery, d-reverse-engineering and d-bio score C3 on sworn testimony (tier 2), not primary documents (tier 1). The board's central claim currently rests on one hearing. What would change it is contract and facility-clearance data, not more testimony.
- NO PRIMARY DOCUMENT CONNECTS A SPECIFIC DOLLAR TO A CONCEALED ACTIVITY. d-funding and d-money establish that the channels exist (transfer authority, MIPRs, IRAD, 50 U.S.C. 3510) and that the audit failure exists, but that is possibility, not fact, and the dossiers say so.
- SKIDMORE'S FIGURES ARE CITED AS GROSS ADJUSTMENTS, NOT MISSING MONEY - the distinction is load-bearing and stated explicitly in d-money. His published papers were not directly located; the citation currently rests on the underlying DoD OIG findings.
- ROSWELL 'FACT VS. FICTION' DATING UNRESOLVED: variously 1994 and 1995 across the corpus; the DTIC copy cited here is 1995. 'Case Closed' is firmly 24 June 1997. Needs pinning to a publication record.
- THE 1999 COMETA REPORT IS DESCRIBED IN PROSE IN l-paris AND l-france WITHOUT A VERIFIED URL - no authoritative online copy was confirmed this pass, so it appears in desc rather than in claims[] or sources[].
- TWENTY LOCATION DOSSIERS ARE THIN BY DESIGN: congressional home-district anchors carry minimal text because committee roles belong on the person records in congress-house.json. Where a member's specific committee role could not be verified, the dossier says 'in the period covered by this board's congressional dossier' rather than asserting one.
- THREE PURE LOCATION ALIASES TO COLLAPSE: l-washington-dc into l-dc (142 inbound refs vs 2), l-lasvegas into l-las-vegas, l-cambridge-ma into l-cambridge. Defined here only so no edge dangles before the merge pass.
- d-consciousness IS THE BOARD'S WEAKEST DOSSIER AND IS TIERED C DELIBERATELY. Its only tier-1 content is that Star Gate ran 23 years and that DIA commissioned Kit Green's neurological-effects DIRD. The substantive claim has no primary support and is recorded as a tier-3 personnel-continuity inference.
- NO CROSS-DOMAIN SCORING CALIBRATION EXISTS. Each dossier explains what a high score means for that domain in prose, but a C3 on d-materials and a C3 on d-bio are not guaranteed to mean the same distance from custody. Axis scores are ordinal within a domain, only roughly comparable across domains.
- AARO VOLUME II WAS NOT LOCATED THIS PASS. Volume I (Feb 2024) is cited throughout. NDAA FY2025 Sec. 6802 sunsets the audit requirements attached to the historical record report, implying the obligation's status changed after 2024; this should be established directly from AARO and the full text of P.L. 118-159.

## `w2-2025-2026` — 17 people, 28 entities, 80 edges

- No published charter, executive order, roster, chair, staff, budget or location for the PURSUE Task Force - a body ODNI ES 2026-00818 credits with declassification authority over all IC UAP holdings
- No signed executive order on UAP declassification exists in the public record despite Hegseth referring on 23 Feb 2026 to 'that executive order'; the originating instrument is a Truth Social post
- Signature date on ODNI ES 2026-00818 is illegible in the released copy, so its two 30-day clocks cannot be timed
- No manifest, index, metadata schema or provenance statement for any of the five PURSUE tranches; war.gov/UFO publishes only dates and bundle sizes, so every file count comes from third parties
- Why many PURSUE PDFs were password-protected against OCR is unexplained
- NARA publishes no RG 615 compliance list and no statement on agencies that did not transfer; CIA, DIA, NRO, NGA, DOE, NASA, DHS and the military departments have no series
- RG 615 bulk-download inventory last updated 24 April 2025, before the 30 Sept 2025 deadline and before the NSA/State/FBI catalog entries
- AARO Historical Record Report Volume II still unpublished: no date, no draft, no explanation since the November 2024 commitment
- Rep. Luna's April 2026 letter that PURSUE Release 02 is said to answer has never been published
- Whether MITRE produced anything responsive by its 45-day deadline (~6 July 2026), and whether the eleven named contractors were separately approached
- No public CIA or FBI response to Burlison's 8 July 2026 Varginha letters
- UAP Governance Board has no published charter, roster or meeting record; its relationship to the PURSUE Task Force is undocumented
- Conflict: DefenseScoop reports Avi Loeb formed and leads the UAP Science Advisory Council; the Sol Foundation says ODNI announced it with FBI support. FACA status and sponsoring agency unknown
- No case number, incident date, hull or unit public for the ~100 airborne UAP and two uncrewed surface systems reported off Virginia
- Provenance, unit, custody chain and declassification authority of the October 2024 MQ-9 Yemen Hellfire video are unstated and the Department has never confirmed it
- Whether the FY2026 NDAA-required NORAD/NORTHCOM UAP intercept briefing (since 2004) has been delivered, and whether any part will be public
- AARO's required accounting of UAP-related security classification guides has not surfaced
- Identity of the multi-witness event, specimen chain of custody and journal for Sol Foundation Briefing No. 3
- Whether Kirkpatrick's ORNL portfolio encompasses the laboratory's AARO specimen analyses
- Whether the FY2027 NDAA conference retains the House-adopted UAP Disclosure Act against a Senate base text (S. 4784) with zero UAP provisions
- No serving executive-branch official has testified under oath on UAP in the 119th Congress


---

# Appendix B — wave-3A re-sourcing gap reports

Appended 12 Aug 2026 after the wave-3A re-sourcing agents completed. These are named,
fetchable primary-record targets, not vague suggestions. Several are statutory compliance
questions with dates attached, which makes them checkable rather than arguable.

## `_rs-legislation` — 94 records, 15 URLs verified, 156 Tier 1 restored

- S.Amdt. 797 cosponsor detail: congress.gov's cosponsor tab is Cloudflare-blocked to non-browser clients and robots-disallowed to WebFetch; the five cosponsors were recovered from the Congressional Record entry (CREC-2023-07-13-pt1-PgS2953) instead. The congress.gov 'Actions (0)' field confirms the amendment was never proposed on the floor, so no roll-call exists for it — wave 4 should confirm via the conference report whether Division G was dropped by the conferees or in a manager's package.
- Conference report for the FY2024 NDAA (H.Rept. 118-301, joint explanatory statement to H.R. 2670) not fetched. That is the primary record of WHO removed the Review Board and eminent-domain sections and what reason was given. Wave 4: govinfo CRPT-118hrpt301.
- UAP Disclosure Act of 2024 (S.Amdt. 2610 to S. 4638, FY2025 NDAA) and the Burlison UAP Disclosure Act amendment to the FY2027 NDAA are referenced by existing nodes (uapda-2024-samdt-2610, burlison-uapda-fy2027-ndaa-amendment, ndaa-fy2027-s4784, uapda-fy2027-house-adopted) but were out of scope here and remain unnailed to primary text. Wave 4: CREC for the 2024 submission date; BILLS-119s4784rs and the FY2027 House-passed engrossed text.
- H.R. 2670 (118th) — the House vehicle actually enacted as PL 118-31 — was not separately fetched; all enacted text came from PLAW-118publ31 directly. A wave-4 diff of BILLS-118hr2670eh against BILLS-118s2226es would show which chamber's UAP text was the conference baseline.
- AARO/agency compliance with PL 118-31 secs. 1841-1843 is unverified: the sec. 1842(c)(1) 300-day agency review deadline fell around 16 October 2024 and the sec. 1841(b)(2) 30-day/180-day NARA public-availability clocks follow transmission. No primary record was fetched showing whether the Unidentified Anomalous Phenomena Records Collection was in fact established, what the required subject guidebook and index contain, or which agencies transmitted records. Wave 4: archives.gov.
- No Federal Register notices of continued postponement retrieved. Sec. 1842(g)(2)(B) requires an unclassified written description of the reason for each continued postponement to be published in the Federal Register — their presence or absence is a direct, checkable measure of whether the surviving statute is being complied with. Wave 4: federalregister.gov search on 'unidentified anomalous phenomena'.
- The 12-page 'Immaculate Constellation' document is confirmed entered into the record of the 13 November 2024 hearing by Chairwoman Mace, but CHRG-118hhrg57440 lists it under 'available at: docs.house.gov' rather than reproducing it. The docs.house.gov event ID for the 20241113 joint hearing was not resolved. Wave 4: locate the GO/GO12 or GO/GO06 event folder for 20241113.
- GAO products responsive to IAA FY2023 sec. 6803 and PL 118-159 sec. 6801 (Comptroller General review of AARO) were not fetched; no gao.gov product number verified. Wave 4: gao.gov/products search on AARO.
- FY2026 NDAA sec. 1673 required AARO to account for UAP security classification guides within 180 days of 18 December 2025 (roughly 16 June 2026) and to fold the result into the 2026 annual report under 50 U.S.C. 3373(k). As of 12 August 2026 no primary record of that accounting was located. Wave 4: aaro.mil and the FY2026 consolidated annual report.
- FY2026 NDAA sec. 1671(b) required the first post-enactment briefing to cover NORAD/USNORTHCOM UAP intercepts back to 1 January 2004 'not previously provided'. Whether that briefing occurred, and whether the sec. 1671(a)(C) failure-to-provide notification was ever triggered against either command, is unrecorded here. Wave 4: House and Senate Armed Services briefing records.

## `_rs-sap-docs` — 38 records, 29 URLs verified, 155 Tier 1 restored

- DoDM 5205.07 Volumes 1 and 3 are 404 at their historic esd.whs.mil URLs and were recovered only from Internet Archive captures; whether a post-2024 replacement or cancellation exists is unresolved. WAVE 4: esd.whs.mil issuance index and DoD Issuances cancellation list.
- No primary record establishes whether DoD continued producing the 10 U.S.C. 119(a) annual SAP report voluntarily after the sec. 1061 Pub. L. 114-328 sunset took effect 31 Dec 2021. Highest-value unresolved item on this layer. WAVE 4: HASC/SASC committee prints, DoD Comptroller congressional reports list, FY2022-FY2026 NDAA text for any reinstatement.
- No primary record located of any report submitted under FY2024 IAA sec. 7606(c) (agency review of SAP access populations, due 22 Dec 2024) or sec. 7606(a). WAVE 4: ODNI and DoD congressional report indexes, GAO report-compliance trackers.
- The reissued ICD 906 signature block extracts as garbled characters; only a PDF creation date of 19 Dec 2024 is recoverable. Exact signature date and signer (DNI or PDDNI) unresolved. WAVE 4: odni.gov/files/documents/ICD/ and the ODNI FOIA reading room.
- The 17 Oct 2015 ICD 906 recovered from Internet Archive is a scanned image PDF with no text layer; its provisions could not be quoted for comparison against the reissuance. WAVE 4: OCR the capture at web.archive.org/web/20160928160132/.
- GAO-04-332 was reachable only via its gao.gov product landing page; the full-report PDF returned 403 to direct fetch and 429 through the fetch proxy, so its Results in Brief and any language about facilities excluded from DSS oversight remain unquoted. WAVE 4: gao.gov/assets/240/241536.pdf or a Wayback capture.
- The number of DoD SAPs currently designated 'waived' appears in no public issuance located here; the DoDI 5205.11 para 3.5.a.(3)(d) SAPOC annual review of waived status produces no public output. Probably unresolvable from open primary records.
- E.O. 12829 was quoted only from the Cornell LII reproduction in the notes to 50 U.S.C. 3161; archives.gov/isoo/policy-documents/eo-12829.html returns 404 and the 1993 Federal Register text is outside govinfo's HTML range. Sections 102, 201, 202 unquoted. WAVE 4: archives.gov/federal-register/executive-orders/1993.html.
- DoDI 5205.11's governance enclosures (SAPOC/SRG/SSWG membership tables, prospective-SAP timeline, carve-out justification template) were read through a summarising fetch; paragraph-numbered verbatim text was obtained for Section 7 and paras 1.2.f, 1.2.i, 3.5, 4.1, 4.2, 5.1 only. WAVE 4: re-fetch 520511p.pdf targeting enclosures individually.
- No carve-out approval memorandum signed by a Secretary or Deputy Secretary of Defense was found released in any form, redacted or otherwise. WAVE 4: DoD FOIA reading room, DCSA FOIA library, OSD/JS FOIA request log for 'carve-out'.
- eCFR section-level URLs bot-block programmatic retrieval (302 to unblock.federalregister.gov); verbatim 32 CFR 117 text was pulled from the eCFR renderer API on 12 Aug 2026. Both the canonical section URLs and the API URL are recorded in sources[].

## `_rs-aaro-reports` — 12 records, 26 URLs verified, 75 Tier 1 restored

- AARO Historical Record Report VOLUME II: promised in Vol I pp.6 and 45; statutory deadline 15 June 2024 (Sec. 6802(j)(1)(A), 540 days after 23 Dec 2022 enactment). Still unpublished as of 12 Aug 2026 - ~26 months overdue. Not on AARO's index, not announced in FY2024 or FY2025 annual reports. Wave 4: FY26 NDAA/IAA conference language, any AARO or OUSD(I&S) letter to SASC/HPSCI explaining the delay.
- YANKEE BLUE has NO Tier 1 anchor. Full-text search proves it is absent from HRR Vol I and from the FY2023/FY2024/FY2025 annual reports. The alleged AFOSI/Kirtland memo is unreleased. Wave 4: the DoD FOIA case file (Pentagon reportedly denied the memo existed Sept 2025, reopened the search Dec 2025) - those response letters would be Tier 1; also AFOSI (osi.af.mil) FOIA logs and any SASC/House Oversight correspondence naming the program.
- Classified versions of DODIG-2023-109 (15 Aug 2023) and of each Consolidated Annual Report remain unreleased; only unclassified summaries are public. The ODNI 2022 report states outright that 'Additional information is provided in the classified version of this report.' Wave 4: MDR/FOIA targets.
- DODIG-2023-109 Recommendation 1 was left 'resolved but open' - the DoD policy OUSD(I&S) was to issue integrating UAP into intelligence/CI/force-protection policy. Wave 4: check whether that issuance ever appeared (esd.whs.mil DoDD/DoDI series) and whether DoD OIG has since closed the recommendation.
- Sec. 6802(k)(1)(A) requires the joint DNI/SECDEF annual report '180 days after enactment, and annually thereafter for four years' - that run arguably expires with FY2025. Wave 4: establish whether the mandate was reauthorised beyond FY2025, which decides whether FY2025 is the last statutorily required annual report.
- FY2025 report contains an unreconciled internal discrepancy on satellite-flaring resolutions: 238 (Executive Summary, p.2) vs 44 (Section C, p.8), and publishes no overall resolution rate. 238 exceeds the 284 in-period reports received, so the headline resolution rate cannot be reconstructed from the report's own numbers. Wave 4: AARO case-resolution dataset or a congressional QFR reconciling the figures.
- FY2025 Section F: 50 UAS incidents near U.S. nuclear infrastructure, weapons and launch sites reported by the NNSA Administrator and NRC Chairman - a 177.8% rise over 18 in FY2024 - expressly 'not reported as UAP'. Wave 4: pursue the underlying NNSA/NRC incident reports (NRC event notification reports are public); a primary-record thread independent of the UAP framing.
- Domain instability from the war.gov/Department of War rename: dni.gov now redirects assessment PDFs to archive.dni.gov and odni.gov; the FY2025 report is under Department of War branding; dodig.mil brands as the Department of War OIG. Live .mil/.gov URLs are unstable - Wayback snapshots recorded alongside every live URL in this overlay.
- media.defense.gov, aaro.mil and dodig.mil serve Akamai 'Access Denied' to non-browser clients (403). All PDFs here were retrieved through web.archive.org id_ snapshots. Caution: the 2026 Wayback capture of the DODIG-2023-109 PDF itself archived an Access Denied page - the citable capture is the 20240125210400 snapshot, not the latest one.
- AARO Historical Record Report Vol I references 'Roswell Investigations/Inquiries (1992-2001)' and a 1961 Special National Intelligence Estimate assessed 'Not Authentic' - the underlying AARO source footnotes (113-119 and the SNIE analysis) were not pulled in this pass. Wave 4: request AARO's reference list / footnote sourcing.

## `_rs-aawsap-dirds` — 109 records, 50 URLs verified, 177 Tier 1 restored

- 5 of the 37 DIRDs listed by DIA have no resolvable URL and were not retrieved: Biomaterials; Materials_For_Advanced_Aerospace_Platforms; Metallic_Glasses_For_Aerospace_Applications; Metallic_Spintronics; Metamaterials_For_Aerospace_Applications. Confirmed absent from the complete Wayback CDX index of dia.mil reading-room FileId URLs (3,536 unique FileIds), and the live page does not expose FileIds to a text fetcher. Wave 4 needs a JS-rendering fetch of the live reading room.
- The canonical '38 DIRD titles' list — the DIA letter to Sens. McCain and Reed (Jan 2018) — was NOT located at any primary URL. Note the reading room currently posts 37 DIRD files, not 38; the discrepancy is unresolved.
- The 2018 DoD letter on Luis Elizondo's role in AATIP was NOT located at a primary URL. Partial substitute obtained: AARO Vol. I's 'AATIP was never an official DoD program' language. Wave 4 should try the 26 July 2023 House Oversight hearing transcript on govinfo.
- DoD IG report DODIG-2023-109 unreachable: dodig.mil's audits/evaluations listing now surfaces only 2026 reports, and Wayback CDX for dodig.mil returns no URL containing 'DODIG-2023-109'.
- Author attribution for all 32 retrieved DIRDs is redacted under (b)(6). Puthoff / Davis / Green attributions remain Tier 3 against the primary record. Wave 4: unredacted copies, BAASS subcontract records, or sworn testimony.
- James Lacatski is not named in any primary document retrieved; the AAWSA Program Manager is redacted under (b)(3) 10 USC 424 and (b)(6) throughout. The post is documented, the incumbent is not.
- Confirm full names behind the two surnames that survived redaction in Info Memo U-429-09: 'Hathaway' and 'Tsoi'.
- Contract dollar values unobtainable: FPDS ATOM feed empty for PIID HHM402-08-C-0072, USAspending 404. Dollar line items on released modification P00001 are illegible/redacted. Wave 4: DIA congressional budget justifications.
- The AAWSAP Statement of Work ('Advanced_Aerospace_Weapon_Sytem_Applications_Program_SOW_Aerospace.pdf') is listed in the DIA reading room but its FileId was not resolved.
- DIRDs 170023 (Statistical Drake Equation) and 170026 (Anomalous Acute and Subacute Field Effects on Human Biological Tissues) carry NO DIA document number on their released cover pages, unlike the other 30. Unexplained.
- governmentattic.org was unreachable (robots.txt fetch failure), so that mirror was never checked for unredacted variants.

## `_rs-stubs-known` — 17 records, 28 URLs verified, 16 Tier 1 restored

- soyuzufotsentr left as an honest stub — not in the assignable set, no official site or primary Russian record reachable without web search; wave 4
- saf-aaz rests on AFI 16-701 (18 Feb 2014) retrieved via Internet Archive; current DAFI 16-701 unretrievable (static.e-publishing.af.mil 403s automated requests, safaa.hq.af.mil no longer resolves)
- No primary record links SAF/AAZ to any UAP-specific programme — AARO Historical Record Report Vol. I was searched in full text and does not mention SAF/AAZ; the node's relevance is structural, not evidenced
- 509th Bomb Group lineage fact sheet (AFHRA/DAF History article 434118) unretrievable — af.mil fact-sheet endpoints return a search interface; wave 4 = AFHRA lineage-and-honors sheet and the July 1947 unit history at NARA
- IZMIRAN's SETKA-AN role carried only by the Stonehill & Mantle secondary article; no primary Russian archival citation obtained
- No primary Senado Federal legislative instrument on UAP located — the palavraChave search API is deprecated (deactivated 2026-02-01) and the replacement /dadosabertos/processo endpoint ignores keyword filters (10,781-record dump, zero UAP ementas)
- Hospital Regional de Varginha: CNES registry confirms the facility (2761041) but no 1996 hospital, military or police document was obtained; custody sequence remains testimony-based
- Enigma Labs publishes no founder names, no team page (404) and no verification methodology; corpus figures are self-reported, so its claims are graded Tier 2 and it is the one node here without a Tier-1 claim
- med.wayne.edu unreachable to automated fetch (robots endpoint times out); no Wayne State institutional record of Christopher Green's appointment retrieved
- US Navy 2019 UAP reporting-guidance message and the OPNAV/Fleet Forces implementing instruction not retrieved as primary documents — only the 27 April 2020 DoD video-release statement
- POGO and The Intercept dossiers rest on their own About pages; neither has a documented UAP-specific publication or intake recorded here, so their board role is graded Tier 3 infrastructural

## `_rs-archive-mirror` — 233 records, 121 URLs verified, 2 Tier 1 restored

- NO WAYBACK SNAPSHOT EXISTS: https://media.defense.gov/2010/Oct/27/2001330256/-1/-1/0/AFD-101027-030.pdf -- checked https and http, anchored at 2024 and 2026; Wayback returns a save-page redirect, meaning zero captures. Live-URL-only citation, genuinely at risk; needs a substitute primary record.
- NO WAYBACK SNAPSHOT EXISTS: https://www.dia.mil/FOIA/FOIA-Electronic-Reading-Room/FOIA-Reading-Room-Advanced-Aerospace-Threat-Identification-Program/ -- the AATIP reading-room index page itself has never been captured (the 44 individual FileId PDFs beneath it ALL captured fine and are now mirrored). Needs a substitute or acceptance that only the child documents are durable.
- NO WAYBACK SNAPSHOT EXISTS: https://www.dodig.mil/About/Leadership/ -- checked https and http, with and without trailing slash, anchored 2024 and 2026. Zero captures. Live-URL-only.
- No Army-side primary URL exists for the TTSA / U.S. Army CCDC CRADA. Wayback CDX domain sweeps of army.mil, devcom.army.mil, ccdc.army.mil and arl.army.mil (filtered on stars/CRADA) returned no TTSA-related page - the Army never published its own release. WAVE 4: try DTIC, an Army CCDC/DEVCOM FOIA reading room, or the Federal Laboratory Consortium CRADA registry for the executed agreement text.
- https://www.arl.army.mil/business/technology-transfer/cradas/49/ (Wayback 2019-12-15) was fetched and inspected as a candidate ARL per-agreement CRADA registry entry; it is a generic paginated CRADA explainer page with no partner list. Not usable as a TTSA citation.
- METHOD WARNING for future mirroring passes: 14 of 121 resolved snapshots initially pointed at captures where the Wayback crawler had recorded the origin server's 403 (DoD bot-blocking) - a ~2KB error page, not the document. These were detected by fetching every snapshot and re-resolved via the CDX API with filter=statuscode:200. Capture existence is not capture validity on .mil hosts.
