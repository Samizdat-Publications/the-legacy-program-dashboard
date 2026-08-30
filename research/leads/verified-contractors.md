# Verified leads: the contractor and oversight layer

**Status: research output, NOT board content.** Nothing here has been merged into
`research/*.json`. Each entry records what was actually opened and read, and says plainly
where a claim could not be verified.

Written 30 August 2026. Source corpus: transcript claims extracted from the UAP Gerb video
corpus (`research/leads/gerb-corpus-*.md`). Every claim below arrived as an unverified
transcript assertion.

**Method note, per `CLAUDE.md` §2.** Every URL listed under "opened" was fetched by this
session and its content read. Document numbers and quotations are transcribed off the
document, not reconstructed from memory or pattern. Where a document could not be opened,
that is stated rather than papered over.

**Environment limits hit during this pass** (worth recording for the next one):

| host | result |
|---|---|
| `gao.gov` | 403 to curl; **serves WebFetch**, including the scanned PDFs |
| `repository.aip.org`, `vault.fbi.gov` | 403 to BOTH curl and WebFetch. Nothing readable from here |
| `patents.google.com` | 503 to curl; **serves WebFetch** |
| `api.govinfo.gov` | `OVER_RATE_LIMIT` on `DEMO_KEY` for this container's whole session |
| `search.worldcat.org` | serves curl; results render client-side but the "No results" string is in the HTML |
| `archive.org` | serves curl, including `advancedsearch.php` (which searches **full text**, not just metadata) and `metadata/<id>` |
| `sec.gov` / `data.sec.gov` | serves curl **only with a descriptive User-Agent**; plain curl gets 403 |

**Tooling note.** GAO's 1986 scans have no raw text layer (`CCITTFaxDecode` + `LZWDecode`
images, zero `Tj` operators in the decodable streams) so the first probe reported them as
unreadable. They *do* carry an OCR layer reachable through PyMuPDF, which `pip install
pymupdf` supplies. `poppler-utils` is not installable here (apt 404s), so the `Read` tool
cannot render PDFs; PyMuPDF `get_text()` is the working channel, and
`get_pixmap()` is the fallback for pages that OCR poorly.

---

## 1. GAO testimony, 24 July 1986 — Lockheed special-access-program document control

**VERDICT: CONFIRMED, with one number contradicted.**

The document is real, the date is exact, the committee is exact, and the two headline
figures are verbatim. One element of the transcript claim is wrong: the 17 transferred
documents were **accounted for**, not lost. The genuinely unaccounted-for total is 11, not
17 plus 46. GAO also states the Defense Investigative Service exclusion as a standing 1965
policy decision, and the companion report says in terms that the failure might not have
happened had DIS been permitted to inspect.

### What was opened

| URL | what is at it |
|---|---|
| `https://www.gao.gov/products/130581` | GAO product record: "Controls Over Classified Documents for a Special Access Program at Lockheed Corporation", published and publicly released 24 July 1986 |
| `https://www.gao.gov/assets/130581.pdf` | the 14-page scan of the testimony itself (13 numbered pages). Read in full |
| `https://www.gao.gov/products/nsiad-86-191` | GAO product record: "Information Security: Need for DOD Inspections of Special Access Contracts", NSIAD-86-191, 7 August 1986 |
| `https://www.gao.gov/assets/nsiad-86-191.pdf` | the 16-page scan of the companion letter report to the Secretary of Defense, which reprints the testimony as Appendix I. Read in full |
| `http://gao.justia.com/department-of-defense/1986/7/controls-over-classified-documents-for-a-special-access-program-at-lockheed-corporation-130581/` | Justia's mirror of the GAO summary for product 130581. Same summary text as GAO's own page |

### The document, off its own cover page

> FOR RELEASE ON DELIVERY EXPECTED AT 10:00 A.M. Thursday, July 24, 1986
> UNITED STATES GENERAL ACCOUNTING OFFICE Washington, D. C.
> STATEMENT OF MARTIN M FERBER, ASSOCIATE DIRECTOR
> NATIONAL SECURITY AND INTERNATIONAL AFFAIRS DIVISION
> BEFORE THE SUBCOMMITTEE ON OVERSIGHT AND INVESTIGATIONS
> HOUSE COMMITTEE ON ENERGY AND COMMERCE
> ON CONTROLS OVER CLASSIFIED DOCUMENTS FOR A SPECIAL ACCESS PROGRAM AT LOCKHEED CORPORATION

The GAO accession number `130581` is printed on that cover page. The subcommittee is the
**House Committee on Energy and Commerce**'s Subcommittee on Oversight and Investigations,
not a defence committee — worth carrying, because it is an unexpected venue.

### Claim-by-claim adjudication

| transcript claim | verdict | what the document says |
|---|---|---|
| ~1,460 discrepancies | **CONFIRMED** | "The current inventory of all 53 document control substations has been completed, and Lockheed has reported 1,460 discrepancies." |
| in 40,000 documents | **CONFIRMED** | "the inventory consists of about 40,000 secret and top-secret items." |
| 46 documents destroyed | **CONFIRMED, but scoped** | "--46 documents had been destroyed, with destruction receipts reportedly on file." This is one of four dispositions of the **224 resolved** cases, not of all 1,460 |
| 17 transferred and never found | **CONTRADICTED on "never found"** | "--17 documents had been transferred out of the company." The 17 sit inside the 224 that "were later accounted for." Nothing says they were not found |
| DIS barred from inspections | **CONFIRMED in substance** | "In 1965, DOD decided that special access programs, because of their especially sensitive nature and small number, would be excluded from supervision by the Defense Investigative Service." |

**The figure the transcript should have used.** The truly unaccounted-for total is 11:

> "As of July 19, 1986, Lockheed was still investigating 1,225 of the 1,460 discrepancies,
> and had completed investigation on 235 of them. Lockheed's reported results --which we
> have not yet had the opportunity to verify-- are that 224 documents were later accounted
> for, and 11 were unresolved. Unresolved is defined as 'all logical leads have been
> exhausted and the documents remain out of accountability and referred to DOD for
> resolution.' Lockheed says 7 of the 11 unresolved documents were inadvertently destroyed
> and it could not locate the other 4."

Full disposition of the 224: 111 later located at substations, 50 removed from
accountability by DOD, 46 destroyed with receipts, 17 transferred out of the company.

### The carve-out mechanism, in GAO's words

> "The number of special access contracts, or carve-out contracts-- as they are sometimes
> called because they are carved out of the Defense Investigative Service's periodic
> inspection program --has grown substantially since 1965. In 1983, we estimated that
> there probably were several thousand such contracts."

And the closing:

> "In summary, it appears inconsistent to us to establish a special access program because
> of security considerations and then afford it less document protection than normal
> classified programs."

### The sharper sentence is in the companion report

GAO/NSIAD-86-191 is a letter report, B-223830, 7 August 1986, addressed to
"The Honorable Caspar W. Weinberger, The Secretary of Defense", signed **Frank C. Conahan,
Director**. It states:

> "the deterioration of document accountability for the special access contract at Lockheed
> may not have occurred if the Defense Investigative Service had been permitted to conduct
> semiannual inspections of the contract, as it does with other contracts at Lockheed."

That report also names the plant — **"the Lockheed/Burbank plant"** — which the testimony
itself does not. The testimony carries a footnote explaining why:

> "As part of DOD granting us access to the special access program to respond your request,
> we agreed not to identify the nature of the program or the specific DOD component or
> military service involved."

### Onward document leads (named in the documents, NOT opened by this session)

- **GAO/GGD-83-43, 18 February 1983**, "Further Improvements Needed in Department of Defense
  Oversight of Special Access (Carve-Out) Contracts" — GAO's earlier recommendation, which
  DOD refused. The testimony gives DOD's three main stated reasons, including that
  "access by Service inspectors would proliferate access beyond the minimum number of
  persons necessary."
- **"Keeping The Nation's Secrets: A Report to the Secretary of Defense by the Commission
  to Review DOD Security Policies and Practices," 19 November 1985** — cited in
  NSIAD-86-191's footnote 1.
- **GAO/NSIAD-88-2BR**, "Information Security: Actions Taken To Improve Lockheed's Special
  Access Document Accountability" — appeared in a search result only. **Not opened. Do not
  cite until someone reads it.**

**Claim tier: T1.** Two primary GAO documents read end to end.

**BOARD RECOMMENDATION: yes, and it is the strongest item in this slice.** The board already
models GAO products as nodes (`gao-nsiad-95-187`, `gao-04-332`, `gao-roswell-report-1995`,
`gao-high-risk-dod-fm`) hanging off a `gao` node, so this is a **new node in an existing
family**, not a new pattern: it is a documented, dated, congressionally-requested finding
that a prime contractor's SAP document control failed while the inspection body was
statutorily carved out — which is the exact structural argument the board makes about
custody. Edge it to `lockheed-martin` and to `lockheed-skunk-works` (the companion report
names Burbank), and add `Defense Investigative Service` as a new entity node, since the
board currently has none.

---

## 2. Research Institute for Advanced Studies (RIAS), Louis Witten, George Trimble

**VERDICT: PARTLY CONFIRMED.** Witten at RIAS is confirmed from a 1957 primary. Trimble's
authorship of the RIAS idea and its gravity-directed purpose are confirmed from his own
dated letter. **The specific claim that Trimble recruited Witten is NOT confirmed** — the
one source I could open says the traffic ran the other way, and the AIP oral history that
would settle it is unreachable from this container.

### What was opened

| URL | what is at it |
|---|---|
| `https://edition-open-sources.org/sources/5/` | Edition Open Sources title page: *The Role of Gravitation in Physics: Report from the 1957 Chapel Hill Conference*, eds. Dean Rickles and Cécile M. DeWitt, Max-Planck-Gesellschaft, 2011, ISBN 978-3-945561-29-4, CC BY-NC-SA 3.0 DE. The report's official designation is **WADC Technical Report 57-216** |
| `https://edition-open-sources.org/sources/5/6/index.html` | the conference participants list |
| `https://edition-open-sources.org/sources/5/3/index.html` | the chapter "The Chapel Hill Conference in Context" |
| `https://physics.unc.edu/home/department-history/section-ii/` | UNC Physics & Astronomy department history, "History of the Institute of Field Physics (1955-1959) by Dean Rickles" — the page states "[published in: www.edition-open-sources.org]", i.e. it is the same text on a university host. Read in full via curl |
| `https://history.aip.org/catalog/icos/36985.html` | AIP catalog record for the Louis Witten oral history |

### Established

**Witten was at RIAS in January 1957.** The participants list of the Chapel Hill conference
(18-23 January 1957) prints:

> Witten, L. | RIAS, Inc., Baltimore
> Bass, R.W. | RIAS , Inc., Baltimore

Witten's conference contribution is "Some Remarks on Cosmological Models", with R. W. Bass.
Note the institutional style there is **"RIAS, Inc."** — a corporate entity, Baltimore.
Note also the funding chain: the report exists at all because of "a conference funding
agreement with the Wright Air Development Center", i.e. an Air Force body.

**RIAS was Trimble's idea and gravity was explicitly its subject.** From Trimble's letter to
Bryce DeWitt, dated 10 June 1955, quoted in the Rickles chapter:

> "During a recent conversation with Mr. George Rideout, president of Roger Babson's Gravity
> Research Foundation, we were commiserating on the unfortunate state of the affairs that
> knowledgable folks do not wish to get 'mixed up' in the field of gravity research."

> "It occurred to us some time ago that our industry was vitally concerned with gravity. As
> time goes on we become more and more concerned because we feel certain that sooner or
> later man will invade space and we see it as our job to do everything possible to speed
> this event. At least one category of the things one must study, when he desires to bring
> space flight to reality, is the laws of nature surrounding the force of gravity."

Trimble described the proposed body as an **"industrial version of the Institute for
Advanced Study"**. Rickles adds that Trimble "bemoans the fact that most of those working on
gravitation are 'madmen and quacks'", and that Martin's own space-flight work "had been
contracted out to German scientists working within Germany."

**Witten was RIAS's first hire.**

> "Louis Witten (the father of Ed Witten, and participant in the Chapel Hill conference) was
> the first researcher hired by RIAS, of the Glenn Martin Company."

**Martin money reached the university side too.** Trimble and the Glenn Martin Company
bought a "'Founder's Membership' for the Institute of Field Physics, for the considerable
sum of $5000", and offered to help solicit further funding.

**The industrial/academic split is stated in the source and matters.** The Glenn L. Martin
Company "was setting up its own research institute that would do work for the U.S. National
Defense Service ... industry-sponsored, and not ensconced in a university", while the IOFP
was deliberately placed inside UNC "so as to avoid the conflict that physicists felt working
in an industrial setting."

### NOT established — and these are the load-bearing gaps

1. **That Trimble recruited Witten.** The only source I could open says the opposite
   direction of travel: Witten "approached DeWitt in a bid to have him join RIAS". Nothing
   I read states who hired Witten. The AIP oral history with Louis Witten (17 March 2011,
   interviewers Dean Rickles and Donald C. Salisbury, Niels Bohr Library & Archives) lists
   "George Trimble" and "Research Institute for Advanced Study (RIAS)" among its topics, but
   `repository.aip.org` returned **403 to both curl and WebFetch**, so the transcript was
   not read. **Do not put a Trimble-recruited-Witten edge on the board on this pass.**
2. **RIAS's founding date and founder.** A "1955, by George Bunker, president of Martin"
   attribution appears in search summaries of Wikipedia. I did not open a primary for it and
   it is not in anything I read. Trimble's June 1955 letter describes the institute as still
   proposed, which is consistent with 1955 but does not establish it.
3. **Any anti-gravity work product.** Nothing I read shows RIAS producing gravity-control
   results. Witten's documented output is classical general relativity — AIP's own abstract
   describes his work as "centered around classical gravitation, including the discovery of
   certain exact electrovacuum solutions to the Einstein field equation." The Rickles chapter
   records the participants' concern about "the absolute necessity to avoid identification
   with so-called 'anti-gravity research.'"

**Claim tier: T1** for the participants list (a reproduction of the 1957 report itself).
**T2** for the Trimble letter quotations and the "first researcher hired" statement — a named
historian on the record, quoting dated archival correspondence, in a peer-published edition.

**BOARD RECOMMENDATION: yes — three new nodes.** `RIAS, Inc.` (entity), `Louis Witten`
(person), `George S. Trimble` (person). None of the three is on the board; a name search of
all 964 nodes returns nothing for RIAS, Witten, Trimble, Martin Marietta or Glenn L. Martin.
RIAS edges to the existing `lockheed-martin` node through Martin Marietta, which makes this
the cleanest documented 1950s-gravity-research-to-current-prime chain in the slice. Grade it
honestly: this is a corporate research institute that studied gravitation, not evidence of
recovered material, and the file should say so.

---

## 3. Project Winterhaven, the 1956 "Electrogravitics Systems" report, Thomas Townsend Brown

**VERDICT: PARTLY CONFIRMED.** Project Winterhaven is confirmed as a real proposal Brown was
shopping in Washington in 1953 — from an FBI record, which also frames it as the subject of
a fraud investigation. The 1956 Aviation Studies report is **NOT independently locatable**:
it survives only as a reprint whose provenance rests on one compiler's account, and it has
no library catalogue record.

### What was opened

| URL | what is at it |
|---|---|
| `https://archive.org/metadata/tt-brown` and `https://archive.org/download/tt-brown/E65ffaeec360d48a08a97fb70305b58f18aac8f13_Q104175_R432679_D2722930_20231226_132723_djvu.txt` | OCR text of a 263KB FBI file on Thomas Townsend Brown, carrying the FBI's own FOIA cover sheet: "FEDERAL BUREAU OF INVESTIGATION FOI/PA DELETED PAGE INFORMATION SHEET FOI/PA# 1496195-000". Read in full |
| `https://patents.google.com/patent/US2949550A/en` | US Patent 2,949,550, "Electrokinetic Apparatus", inventor Thomas Townsend Brown |
| `https://archive.org/metadata/projectwinterhaven` | archive.org item record for a scan titled "Project Winterhaven: A Proposal For Joint Services Research And Development Contract", creator "T Townsend Brown" |
| `https://archive.org/download/thomas-valone-electrogravitics-systems/Thomas%20Valone%20-%20Electrogravitics%20Systems_djvu.txt` | OCR text of Thomas Valone's anthology, which reprints the 1956 report |
| `https://search.worldcat.org/search?q=ti%3Aelectrogravitics` | WorldCat title search. **Returns "No results"** |

`vault.fbi.gov` is 403 from this container, so the file could not be confirmed against the
FBI's own server. Its provenance is: a scan uploaded to archive.org on 28 December 2023 by a
private account, subsequently carried in the `nationalsecurityarchive`, `usgovernmentmirrors`
and `government-documents` collections, bearing the standard FBI FOI/PA release apparatus.

### Established — Project Winterhaven

The FBI file contains an investigative report whose **LEADS** section directs the Washington
Field Office:

> "At Washington, D. C.: As indicated in the details of this repat and in the enclosed report
> from Cincinnati, THOMAS TOWNSEND BROWN is apparently in Washington attempting to obtain a
> research and development contract for his so-called 'Project Winterhaven'. BROWN apparently
> anticipates a contract of approximately a million dollars.
> Your office should therefore ascertain from appropriate defense agencies the nature of any
> overtures made by BROWN, and should determine any possible violation of the [F]AG
> Statute in this matter."

The same passage names **the Townsend Brown Foundation, 16 Bowen Building, 8[15] 15th
Street, Washington 5, D. C.**, and instructs:

> "at the Patent Office, review patents No. 1,974,483 (U. S. Electrostatic motor) and No.
> 2,207,576 (electric perception method) to determine exactly what it is BROWN has patented
> which is pertinent to this matter."

That referral cites "Page 12, report of SA RICHA[R]D C. HOTOMAN, 3/25/53, Cincinnati" (OCR
of the surname is uncertain). So: **Winterhaven was real, it was a funding proposal of about
$1M, Brown was pitching it to defence agencies in 1953, and the FBI was investigating him
for possible Fraud Against the Government while he did it.** All four facts come off the
same page.

### Established — other Brown material that IS documentable

- **US 2,949,550, "Electrokinetic Apparatus"**, inventor Thomas Townsend Brown, filed
  3 July 1957, granted 16 August 1960. First claim, verbatim: "Thrust producing apparatus
  comprising an electroconductive body having a relatively large, substantially smooth area
  thereof exposed to the surrounding medium, an electrode supported on said body, insulated
  therefrom and shaped to produce a concentrated electrostatic field when electrically
  charged with respect to said body, and power means connected between said body and
  electrode to impress high voltage thereon whereby to cause relative movement of an
  ionizable dielectric medium surrounding said electrodes."
- **An instrument of Brown's was installed at the Naval Research Laboratory.** The FBI file
  reproduces a letter dated 23 December 1948 from the head of the Photometry Section, Optics
  Division, Naval Research Laboratory: "The radiation recorder of THOMAS TOWNSEND BROWN. . .
  was installed in this laboratory about 1931." The writer adds "I did not attend it or
  attempt to analyze the results."
- **A 1950 federal loyalty check.** A 6 December 1950 memorandum from "J. Edgar Hoover,
  Director" to the Chief, Investigations Division, U.S. Civil Service Commission, subject
  "THOMAS TOWNSEND BROWN", records him as an appointee to the "Industrial Relations
  Department, Pearl Harbor Naval Shipyard, Pearl Harbor, T. H., Department of the Navy" and
  notes a 1943 Navy resignation "accepted for the good of the service", with "no information
  of disloyal nature."
- **An ONR visit, on the Navy Secretary's orders, reported second-hand.** A named witness
  (JOHNSON) told the FBI "that the chief physicist of the Office of Naval Research,
  Washington, D.C., visited at the Foundation laboratory about ten months ago on orders from
  Secretary of the Department of Navy KIMBALL", and "it was his observation that the
  physicist sat in disbelief through the demonstration."

### NOT established — and the file is candid about the other side

The same FBI file carries multiple named informants characterising Brown's demonstrations as
a relabelled earlier device. A former president of Lake States Securities Corporation stated
the "flying saucers" apparatus "was identical to the old stock market predicting machine
except that it operated in the atmosphere rather than in an oil bath and it was much
larger", and said he was "confident this flying saucer thing is a phony." **Any board node
on Brown must carry this alongside the patents, or the node is not honest.**

### The 1956 "Electrogravitics Systems" report — NOT independently locatable

The Valone anthology reproduces a title page reading, verbatim:

> ELECTROGRAVITICS SYSTEMS
> An examination of electrostatic motion, dynamic counterbary and barycentric control.
> AVIATION STUDIES (INTERNATIONAL) LTD.
> Prepared by: Gravity Research Group, Special Weapons Study Unit,
> Aviation Studies (International) Limited, London.
> 29-31 Cheval Place, Knightsbridge, London, S,W,7 England
> Report GRG-013/56 February 1956

Its opening argument is that all aircraft to date, "including the supersonic jets of the
nineteen-fifties", are "powered gliders", and that the alternative is to "discover the nature
of gravity from cosmic or quantum theory".

**But the provenance is a single unverifiable chain.** Valone's own introduction states that
"Dr. Paul LaViolette notes that the Electrogravitics Systems report may be obtained from the
Wright-Patterson AFB technical library, even though it is not actually listed on their
library computer. He found that it is not available from any other library in the U.S." A
WorldCat title search for `electrogravitics` returns **No results** — there is no catalogue
record for the original anywhere WorldCat indexes. So the document's existence rests on the
compiler's and LaViolette's account of retrieving an unlisted item from one base library.
That is not verification.

The `projectwinterhaven` scan on archive.org is in the same position: a private upload from
27 December 2024 with no institutional holding named.

**Claim tier: T1** for the FBI file and for US 2,949,550. **T3** for the contents of the
1956 report — a reprint of an original nobody has independently located.

**BOARD RECOMMENDATION: yes for Brown, qualified for the rest.** `Thomas Townsend Brown` is
a **new person node** (no match among the 964). Winterhaven attaches to him as a T1 claim
sourced to the FBI file, phrased as what the FBI recorded — that he was seeking a ~$1M
contract — not as a programme that existed. The 1956 report should go on the board **only**
as a T3 claim whose text says the original has no catalogue record; the board already
carries 2 mentions of "Electrogravitics" in prose, so check for duplication first. Do **not**
create an "Aviation Studies (International) Ltd." node on this evidence.

---

## 4. BDM International, McLean VA, and the 1985 "Advanced Theoretical Physics" meeting

**VERDICT: PARTLY CONFIRMED.** The company is confirmed to the level of an SEC filing. The
1985 meeting **is** documentable from a source other than the transcript, but that source is
private papers republished on a blog, not an archive or a government record.

### What was opened

| URL | what is at it |
|---|---|
| `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=BDM&type=10-K&...&output=atom` | EDGAR company index: BDM INTERNATIONAL INC /DE, CIK 0000870763 |
| `https://www.sec.gov/Archives/edgar/data/870763/0000950112-96-000762.txt` | BDM International's Form 10-K for FY1995, filed 12 March 1996. Read |
| `https://ufos-scientificresearch.blogspot.com/2019/06/the-advanced-theoretical-physics.html` | a blog post reproducing scans said to be from the ATP group's first meeting |

### Established — the company, from its own SEC filing

- **BDM INTERNATIONAL INC /DE**, CIK 0000870763, SEC file number 000-23966, SIC 7373.
- Registered address in the filing: **1501 BDM Way, McLean, Virginia 22102-3201**; the
  business section gives "1501 BDM Way, McLean, Virginia 22102-3204" and telephone
  (703) 848-5000.
- Verbatim: "The Company was formed in 1959 by Drs. Joseph V. Braddock, Bernard J. Dunn, and
  Daniel F. McDonald as 'Braddock, Dunn & McDonald, Incorporated,' which was later
  reorganized as BDM International, Inc."
- Ownership chain, verbatim: public 1980-1988; "when Ford Aerospace Corporation ('Ford
  Aerospace'), then a wholly owned subsidiary of Ford Motor Company ('Ford'), acquired all of
  the outstanding stock of the Predecessor Company"; then "In October 1990, on behalf of
  certain investors, The Carlyle Group, L.P. ... formed BDM Holdings, Inc." which acquired
  substantially all the assets.
- Business mix in 1995: "Department of Defense ('DOD') (approximately 37% of total revenue in
  1995), international defense agencies (approximately 25%), civil government agencies
  (approximately 23%), and commercial clients (approximately 15%)". Subsidiaries named
  include **Vinnell Corporation**.

### The ATP meeting — what the non-transcript source actually is

The blog post reproduces a set of scans. Its stated provenance is that researcher Melinda
Leslie obtained them from **Jack Houck's private files after Houck's death in 2013**. The
item that names the venue is described on the page as "a booking 'slip' for the 'BDM McLean
Secure Facility' for the dates of 20-25 May 1985". Other items are an undated May 1985
agenda and presentation transparencies annotated in Houck's hand and dated 21 May 1985,
bearing phrases including "Threat", "Abduction data base", "Obtain technology spinoffs" and
"Have airtight security".

**So the answer to the question as posed is yes — there is a documentary source other than
the transcript — but the chain is private papers → researcher → blog.** No institutional
repository, no government record, no BDM record. I did not locate the underlying scans in
any archive, and I did not open any account by a named participant (John B. Alexander and
Jacques Vallée have both published on the ATP group; **neither was read on this pass**).

**Claim tier: T1** for BDM the company. **T3** for the May 1985 meeting.

**BOARD RECOMMENDATION: yes for the company, cautiously.** `BDM International` is a **new
entity node** — no match among the 964, and it closes a real gap, because BDM went to TRW in
1997 and TRW to the existing `northrop-grumman` node in 2002, so BDM is an unrepresented
predecessor of a node the board already carries. The ATP meeting should be a **T3 claim on
that node**, worded as "papers from Jack Houck's estate, published by a researcher, include
a booking slip for BDM's McLean secure facility for 20-25 May 1985" — which is what is
actually supportable. Next step before promoting it: read John B. Alexander's own published
account, since a named participant in print would move it to T2.

---

## 5. Sperry Rand Corporation — MacArthur's chairmanship and the 1986 end

**VERDICT: CONFIRMED, with a naming correction the transcript gets wrong.**

MacArthur's chairmanship is confirmed twice over, from a company publication and a
government-archived contemporaneous press document. The dissolution is confirmed from SEC's
own records. **But the company was not called "Sperry Rand" in 1986** — it had been Sperry
Corporation since 1979, and it was Sperry Corporation that Burroughs absorbed.

### What was opened

| URL | what is at it |
|---|---|
| `https://archive.org/download/this-is-sperry-rand-1956/This-Is-Sperry-Rand-1956_djvu.txt` | OCR text of *This Is Sperry Rand 1956*, creator "Sperry-Rand Corporation" |
| `https://archive.org/download/cia-readingroom-document-cia-rdp68-00046r000200010025-0/cia-rdp68-00046r000200010025-0_djvu.txt` | OCR text of CIA Reading Room document **CIA-RDP68-00046R000200010025-0**, "Declassified in Part - Sanitized Copy Approved for Release @ 50-Yr 2014/03/19": a New York Journal-American clipping dated 17 January 1957 |
| `https://data.sec.gov/submissions/CIK0000746838.json` | SEC's submissions record for UNISYS CORP |
| `https://www.sec.gov/Archives/edgar/data/746838/0000746838-94-000005.txt` | Unisys Corporation Form 10-K filed 29 March 1994, including SEC's own IMS header. Read |

### Established — MacArthur

**From the company's own 1956 publication**, a signed statement attributed to:

> "General of the Army Douglas MacArthur, Chairman of the Board, Sperry Rand Corporation."

**From the CIA-archived clipping**, Bob Considine's "Generals Don't Fade Away" column, New
York Journal-American, 17 January 1957:

> "Gen. Douglas MacArthur, who will be 77 next week, is active as chairman of the board of
> Sperry Rand."

The same column is a useful artefact in its own right: it inventories the general-officer-to-
prime-contractor pipeline of the mid-1950s in one paragraph — Halsey at International Tel and
Tel, Lucius Clay at Continental Can, Ira Eaker at Hughes Tool, Doolittle at Shell Oil plus
the Air Force Scientific Advisory Board and the President's Foreign Intelligence Board,
Ennis Whitehead at "Northrup", J. B. Montgomery at General Electric.

### Established — the end of the company

SEC's own IMS header on the Unisys 10-K records:

> FORMER COMPANY:
> FORMER CONFORMED NAME: BURROUGHS CORP /DE/
> DATE OF NAME CHANGE: 19861204

So **CIK 0000746838 is Burroughs Corporation, renamed Unisys, with SEC recording the name
change on 4 December 1986.** The same filing shows Unisys carrying Sperry's obligations:
exhibit 10.17 is the "Sperry Corporation Pension Plan for Outside Directors of the Board of
Directors, as amended, incorporated by reference to Exhibit 10-J to the Annual Report of
Sperry Corporation on Form 10-K for the fiscal year ended March 31, 1984 (File No. 1-3908)",
and the notes discuss "its sale of the Sperry Aerospace Group in December 1986".

### The correction, and what remains unverified

The transcript says "Sperry Rand ... dissolution circa 1986". What is primary-verified is:
Sperry **Corporation** existed under that name and filed a 10-K for FY ending 31 March 1984;
Burroughs became Unisys on 4 December 1986; Unisys inherited Sperry's plans and sold the
Sperry Aerospace Group in December 1986. **The 1979 Sperry Rand → Sperry Corporation rename
is NOT verified from a primary here** — secondary sources give 1 August 1979 and I did not
open a document for it. Nor did I open a merger agreement or proxy; EDGAR does not reach
back to 1986 filings.

**Claim tier: T1** for the MacArthur chairmanship and for the Burroughs→Unisys name change.
**T3** for the 1979 rename until someone opens a document.

**BOARD RECOMMENDATION: yes, one new node, and it is a smaller item than the others.**
`Sperry Rand Corporation` is a **new entity node** (no match among the 964). Its value to
this board is narrow but real: it is a clean, cheaply-documented instance of the pattern the
board is built to show — a five-star officer chairing a defence prime while the programme
period is running — and the Considine column gives thirteen more instances of the same
pattern in one citable document. Do **not** attach any UAP claim to it; there is none in
anything I read.

---

## 6. The "Aurora" budget line, FY1986-FY1987

**VERDICT: CONFIRMED as to the figures and their source, with the underlying procurement
document itself NOT read.**

The figures are exactly right and the framing in the transcript is better than the popular
one: this was public in **February 1985**, from the Pentagon's own unclassified procurement
list, five years before the Aviation Week story that usually gets the credit.

### What was opened

| URL | what is at it |
|---|---|
| `https://archive.org/metadata/cia-readingroom-document-cia-rdp90-00965r000807470050-4` and `https://archive.org/download/cia-readingroom-document-cia-rdp90-00965r000807470050-4/cia-rdp90-00965r000807470050-4_djvu.txt` | CIA Reading Room document **CIA-RDP90-00965R000807470050-4**, "Declassified in Part - Sanitized Copy Approved for Release 2012/01/12": the full text of a Washington Post article of 8 February 1985. Read in full |

`www.cia.gov/readingroom/...` itself redirect-loops for WebFetch from this container; the
archive.org mirror of the CIA Reading Room (`ciareadingroom` collection) is the working
route and carries the document number and release stamp.

### The document, verbatim

> WASHINGTON POST
> 8 February 1985
> Pentagon Seeks Billions For 'Classified' Plane
> Secrecy Cloak Slips Off Mystery Craft
> By George C. Wilson, Washington Post Staff Writer

> "The Pentagon has said in a public document that it wants $2.3 billion for an Air Force
> plane called Aurora but responded yesterday that the plane—if it really is a plane—is
> 'classified.'"

> "The secrecy cloak slipped off the spending plans for Aurora when the Pentagon compiled its
> unclassified shopping list, known as the P1 document, The P stands for procurement."

> "Spending for Aurora, according to this public document, shoots up from zero this fiscal
> year to $80 million in fiscal 1986 to $2.27 billion in fiscal 1987. Reminded that Aurora
> has been put in the public domain by the Pentagon, an Air Force spokesman said his orders
> still were to say only: 'It's a classified program.'"

> "Other Pentagon sources, however, said that Aurora may have some connection with the
> Stealth plane—to be designed to hide from enemy radar—but that the really big money for
> Stealth is held in a different secret account and goes far beyond $2.3 billion a year when
> it enters the production stage."

### Adjudication

| transcript claim | verdict |
|---|---|
| DoD procurement documents show a project named Aurora | **CONFIRMED** — named as the "P1 document", the Pentagon's unclassified procurement list |
| $80 million in FY1986 | **CONFIRMED exactly** |
| rising to $2.3 billion in FY1987 | **CONFIRMED to the article's own rounding.** The precise figure in the body is **$2.27 billion**; the article's lede rounds it to $2.3 billion. Use $2.27bn on the board and note the rounding |

**NOT established: the P-1 document itself.** I did not find or read it. `api.govinfo.gov`
returned `OVER_RATE_LIMIT` for this container's whole session on `DEMO_KEY`, and govinfo's
collections do not in any case reach 1985 procurement justification books. So the chain is:
a named Washington Post defence correspondent, in a dated contemporaneous article, preserved
in a US government declassified collection, reporting what the P-1 said.

**Claim tier: T1** for the CIA document (a primary document read end to end). The claim
*about the P-1's contents* is **T2** — a named reporter on the record.

**BOARD RECOMMENDATION: yes, but as a budget-mechanics claim, not a UAP claim.** `Aurora` is
not among the 964 nodes. Its value here is that it is a documented instance of a classified
programme becoming visible through a budget-document error and then being denied on the
record by the service that published it — which is a mechanism the board argues about
elsewhere. It should carry no craft claim and no recovery claim; the Post article itself
points at Stealth, not at anything anomalous. Attach it to `lockheed-martin` and
`northrop-grumman` only through what the article says (Northrop is named as "builder of
Stealth"), never by inference.

---

## Summary table

| # | lead | verdict | tier | board |
|---|---|---|---|---|
| 1 | GAO 130581 / NSIAD-86-191, Lockheed SAP document control | **CONFIRMED**, one number contradicted | T1 | new node in the existing GAO family + new `Defense Investigative Service` node |
| 2 | RIAS / Louis Witten / George Trimble | **PARTLY CONFIRMED** — Trimble-recruited-Witten NOT confirmed | T1 / T2 | three new nodes |
| 3 | Project Winterhaven, Electrogravitics Systems, T. T. Brown | **PARTLY CONFIRMED** — 1956 report has no catalogue record anywhere | T1 for FBI file + patent; T3 for the report | new `Thomas Townsend Brown` node |
| 4 | BDM International + 1985 ATP meeting | **PARTLY CONFIRMED** — company T1, meeting from private papers only | T1 / T3 | new node; ATP as a T3 claim |
| 5 | Sperry Rand — MacArthur, 1986 end | **CONFIRMED**, naming corrected | T1 | new node, no UAP claim |
| 6 | Aurora budget line | **CONFIRMED** as to figures; P-1 itself not read | T1 / T2 | new node, budget mechanics only |

## What a next pass should pick up

1. **`repository.aip.org` and `vault.fbi.gov` are both 403 here.** The Louis Witten oral
   history would settle the Trimble recruitment question in one read. Try from a different
   network, or request the transcript from AIP.
2. **GAO/GGD-83-43 (18 Feb 1983) and GAO/NSIAD-88-2BR.** Both are named in documents already
   read; neither was opened. GGD-83-43 is the report DOD refused, and NSIAD-88-2BR is the
   follow-up on whether Lockheed fixed it. Both should be reachable by WebFetch on gao.gov,
   which serves scans this session read successfully.
3. **John B. Alexander's own published account of the ATP group.** A named participant in
   print moves lead 4's meeting from T3 to T2.
4. **A primary for the 1979 Sperry Rand → Sperry Corporation rename.**
5. **The FY1986/FY1987 P-1 itself.** `api.govinfo.gov` needs a real API key rather than
   `DEMO_KEY`; the rate limit here was hit before a single useful query landed.
