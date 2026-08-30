# Verified people — lead adjudication pass

**Date of pass:** 30 August 2026. **Slice:** six names from `gerb-candidates.txt`
that the cross-check returned as `ABSENT` or as near-miss prose mentions.

**What this file is.** Unlike the corpus maps in this directory, everything below is
asserted against a document that *this pass actually opened and read*. Every URL in the
"Source" rows was fetched in this session and returned the document described. Nothing here
was taken from a search-result snippet, a summarizer, or recall. Where a claim could not be
put against a document, it is recorded as not verified rather than softened.

**Two documents contradicted their own secondary literature in this pass**, which is the
reason for the rule. See Brown §4 (Project Winterhaven contains no "saucer interceptor")
and Corso §2 (the affidavit is dated May 1998, not July 1998).

Tier vocabulary is `CLAUDE.md` §6: **T1** a primary document read; **T2** a named person on
the record; **T3** stated inference. Node tiers A/B/C are proximity, not credibility, and are
not assigned here — that is Stewart's call.

---

## 1. Dr Robert I. Sarbacher

**VERDICT: PARTLY CONFIRMED.**

The man and his credentials are solidly documented. The 1983 letter exists as a signed
two-page facsimile that I opened and read. The 1950 Wilbert Smith memorandum could **not** be
reached in facsimile from this environment, and that gap is the one that matters.

Sarbacher was a real and conventionally distinguished microwave engineer: the title page of
his 1943 Wiley textbook names him "Robert I. Sarbacher, Sc.D., Associate Professor of
Electrical Engineering, Illinois Institute of Technology." Contemporary Georgia Tech press
clippings place him as Dean of the Graduate Division at Georgia Tech from 1 July 1945 and
describe him advising the Navy on instrumentation for the Operation Crossroads tests — but
that clipping file is a private upload with no institutional custody, so it carries less
weight than the book. What Sarbacher is **documented to have written himself** is the
29 November 1983 letter to William Steinman: two typed pages on Washington Institute of
Technology letterhead, signed, with Steinman's handwritten receipt note "Received 12-5-83".
In it he says John von Neumann and Vannevar Bush "definitely" were involved and "I think Dr.
Robert Oppenheimer also"; that he was **invited to but did not attend** any recovery meeting
("I could not personally attend the meetings"); that materials "reported to have come from
flying saucer crashes were extremely light and very tough"; and that he "got the impression
these 'aliens' were constructed like certain insects we have observed on earth." Everything
about a Wright Field meeting, and everything Eric Walker is said to have said, is **not** in
this letter — it reaches the corpus through Friedman's and Steinman's recollections and is
second-hand at best.

**Two problems with the letter, both read off the document itself.** First, Sarbacher writes
"My association with the Research and Development Board under Doctor Compton **during the
Eisenhower administration**." The RDB was a Truman-era body and Karl T. Compton chaired it in
the late 1940s; Eisenhower took office in January 1953. Sarbacher, then about 76, is
conflating administrations — a plain internal date error in the single most-quoted paragraph
of the document. (I did not verify Compton's RDB dates against a primary document in this
pass; the error is visible without doing so, because the letter's own two halves disagree.)
Second, his P.S. — "It occurs to me that Dr. Bush's name is inccorrect as you have it.
Please check the spelling" — is **omitted from the typed transcript** bound into the same PDF,
so anyone quoting the transcript rather than the scan is quoting an abridged document.

**Provenance caveat, and it is not small.** The only copy I could reach is hosted by
majesticdocuments.com (Ryan Wood's operation), an advocacy publisher, and the same PDF's last
page is a product order form. The scan looks like a genuine photocopy of a typed letter, but
no institutional archive holds a copy I could open from here, so the honest statement is
"a facsimile widely reproduced from Steinman's own file", not "an archived document".

**Sources opened:**

| URL | What is actually there |
|---|---|
| `https://ia802909.us.archive.org/9/items/majiall337/sarbacher-steinman-29nov83.pdf` | 5-page PDF. Pages 1–2: scanned facsimile of the signed 29 November 1983 Sarbacher-to-Steinman letter, Washington Institute of Technology letterhead, 500 Brazilian Avenue, Palm Beach FL. Pages 3–4: typed transcript (omits the P.S.). Page 5: a Majestic Documents order form. |
| `https://archive.org/details/dli.ernet.14512` | *Hyper and Ultrahigh Frequency Engineering*, Robert I. Sarbacher Sc.D. and William A. Edson Sc.D., John Wiley & Sons, copyright 1943, fourth printing September 1944. Title page gives both authors' rank at Illinois Institute of Technology. |
| `https://archive.org/details/robert-sarbacher-georgia-institute-technology-georgiatech` | OCR'd newspaper clippings said to be from Georgia Tech's archives. **Private upload, no institutional custody** — use as a pointer, not a citation. |

**What I could NOT reach.** The 21 November 1950 "Geo-Magnetics" memorandum. Library and
Archives Canada refuses this environment (403 / connection reset on every entry point), and
the archive.org item that one secondary page links as a scan (`Smithmemo.PDF`) **does not
exist** — its metadata endpoint returns an empty object. `web.archive.org` is unreachable per
`CLAUDE.md` §9.3. The board's own `research/w2-international.json` already flags this exact
gap under `unverified`, and this pass did not close it.

**Strongest supportable tier: T1** — for what the 1983 letter says, cited to the facsimile,
with the provenance caveat stated in the claim. The Smith-memorandum content stays at **T2**
(Smith on the record about what Sarbacher told him) until a facsimile is obtained.

**BOARD RECOMMENDATION: promote to its own node.** He is a real, credentialed figure who
authored a signed document that the board already leans on second-hand through
`wilbert-smith`, and a node is the only place the "invited but did not attend" distinction and
the Compton/Eisenhower date error can be carried where a reader will see them.

---

## 2. Lt. Col. Philip J. Corso

**VERDICT: PARTLY CONFIRMED — and this is the most productive entry in the slice.**
His service record is confirmed from his own Army form. The FBI-release claim is confirmed
by direct reading. The affidavit's date in the corpus is **wrong**.

**Service record, read off DA Form 66 (his Army Officer's Qualification Record).** The form
was released by U.S. Army Reserve Personnel Command, St. Louis, in April 1998 in response to a
23 February 1998 FOIA request — the cover letter is addressed to **John Greenewald, Jr.**, not
to Larry Bryant as The Black Vault's case-file page states. The Record of Assignments shows,
in his own file:

| Effective | Duty | Organization |
|---|---|---|
| 23 Feb 42 | Officer Candidate School, AA School | Cp Davis, NC |
| 21 Apr 47 | Dy Unasg, then Prep & Grader O, Spec Projects Br | The Ground Gen Sch, **Ft Riley, Kansas** |
| 11 Sep 50 | Intel Staff O, Plans & Estimates Br, Theater Intel Div, G2 | GHQ, FECOM |
| 24 Feb 54 – 1957 | Intelligence Staff O | 8720 DU, ArmySec, **Opr Coordinating Bd**, Wash DC |
| 31 Oct 57 | Battalion Commander | Hq Btry 552d AAA Msl Bn (NIKE), USAREUR |
| 11 May 59 / 1 May 60 | Inspector General | Hq Seventh US Army Support Command, USAREUR |
| 20 Jul 61 | Staff O, **Foreign Technology Div** | OCRD USA (8556) Wash DC |
| **18 Apr 62** | **Chief, Foreign Technology Div** | OCRD USA (8556) Wash DC |
| **18 Jul 62** | Staff O, Plans Div | OCRD USA (8556) Wash DC |
| 1 Mar 63 | Retired | |

So the Army Foreign Technology Division **is** in his own service record, in the Office of the
Chief of Research and Development — and he was its **Chief for three months**, 18 April to
18 July 1962, after a year on its staff. He was at Fort Riley from 21 April 1947, which covers
the alleged 6 July 1947 observation. Decorations on the form include the Legion of Merit,
Bronze Star Medal, Army Commendation Ribbon, Knight Officer of the Order of the Crown of
Italy and the Italian War Cross. The form is signed "Philip J. Corso, 20 Oct 66".

**The FBI release — the transcript's claim is CONFIRMED by direct reading, with corrections.**
The FOIPA cover letter is dated **12 April 2024** (July 2024 is when The Black Vault published
it) and states: "449 pages were reviewed and 313 pages are being released" and "Enclosed are
cross-references... Cross-references are defined as mentions of the subject of your request in
files to other individuals." I extracted the text of all 322 PDF pages and searched it: the
words *UFO*, *flying saucer*, *unidentified*, *Roswell*, *extraterrestrial* and *saucer* appear
**zero times**. (One case-insensitive "ufo" hit is an OCR artifact inside a garbled word.) The
files contain instead:

- A document stating plainly: *"Our files do not reveal that Corso has been investigated by
  this Bureau."*
- The Fabian Socialists episode, verbatim: in 1955 **Gen. Arthur S. Trudeau** gave the FBI a
  list of alleged "Fabian Socialists" in policy positions and said "Colonel Philip Corso,
  then assigned to the **Operations Coordinating Board**, would be in a position to elaborate...
  as he, Corso, had actually accumulated the information." The FBI reviewed its own files on
  the named individuals and found "insufficient evidence to prove the validity of the
  allegation." **This independently corroborates Corso's OCB assignment from an FBI record
  rather than from Corso.**
- His appearance before the Senate Internal Security Subcommittee on 15 May 1961, testimony
  which "consisted primarily of his reading into the Committee's records the entries from
  personal and private office diaries that he kept during his service with the Operations
  Coordinating Board **from 1953 to 1957**."
- The Oswald episode: in February 1964 a rumour that Lee Harvey Oswald had been a paid FBI
  informant was traced to Corso; interviewed, "Corso admitted that he had passed out
  information concerning Oswald's alleged connection with the FBI, stating his sources in CIA
  had merely presumed that Oswald was an FBI informant," refused to name them, and
  "emphasized the fact that his allegations had been strictly deductions and had no basis in
  fact."
- A 6 February 1965 letter to J. Edgar Hoover from **Rep. Michael A. Feighan (D-OH)**, Chairman
  of the Immigration and Nationality Subcommittee, enclosing material on Corso — the House
  subcommittee name check.

**The affidavit: the corpus date is wrong.** The CAUS press release announcing it is dated
**8 June 1998**, and the reproduced affidavit closes "Sworn before me this day of ___ **May,
1998**" — with the day left blank in the circulating copy. It is a **May 1998** affidavit, not
July 1998. Its content otherwise matches the corpus: NSC membership, head of the Foreign
Technology Desk at Army R&D, the 6 July 1947 Fort Riley observation, possession of the
"Roswell File" in 1961, autopsy reports performed at Walter Reed, the term "extraterrestrial
biological entity". **One line in it does not survive the DA Form 66**: the affidavit says he
"was a member of President Eisenhower's National Security Council". The form records him as an
Intelligence Staff Officer on the *Operations Coordinating Board*, which reported to the NSC
but was not the NSC. That is a documentable overstatement in a sworn document, and it is worth
carrying.

I did **not** open a signed original of the affidavit — only a reproduction of its text.

**Sources opened:**

| URL | What is actually there |
|---|---|
| `https://www.theblackvault.com/documents/ufos/corso/corso.pdf` | 7-page PDF: Black Vault cover sheet, the April 1998 Army FOIA release letter to John Greenewald Jr. signed by Ange F. Nash, and Corso's DA Form 66 (Record of Assignments, Awards, Details, signature 20 Oct 66). |
| `https://documents3.theblackvault.com/documents/fbifiles/1380241-001.pdf` | 322-page FBI release, FOIPA Request No. 1380241-001, subject CORSO, PHILIP JAMES, cover letter 12 April 2024. Cross-references only; no main file. NARA referral file numbers 62-HQ-109090-A, 63-HQ-5327, 100-HQ-420468. |
| `https://www.theblackvault.com/documentarchive/unreleased-fbi-documents-shed-light-on-lt-col-philip-corsos-controversial-claims/` | The Black Vault's 31 July 2024 article announcing the release. |
| `https://openminds.tv/corso-legacy/` | Maurizio Baiata article reproducing the CAUS press release of 8 June 1998 and the full affidavit text, ending "Sworn before me this day of ___ May, 1998." |
| `https://archive.org/details/dayafterroswell0000cors` | Library record: *The Day After Roswell*, Corso, Philip J., with William J. Birnes, New York: Pocket Books, 1997, ISBN 0671004611, LCCN 97208349, viii + 341 pp. |
| `https://archive.org/details/PhilipJ.Corso-DawnOfANewAge` | The 176-page *Dawn of a New Age* manuscript. **Contains no affidavit** — the words "affidavit", "sworn", "CAUS" and "Gersten" do not appear in it. Do not cite it for the affidavit. |

**Related court record (found, not read).** CourtListener's search API returns *Citizens
Against UFO Secrecy, Inc. v. United States Department of Defense*, 21 F. App'x 774 (9th Cir.,
14 November 2001), docket No. 00-16036, D.C. No. **CV-99-00108-SMM** (D. Ariz.). The opinion
body is behind authentication and I could not read it, so nothing about its holding is
asserted here — but the docket number is the handle for a later pass, and note it is a
**1999** district filing, not the March 1998 filing CAUS announced.

**Strongest supportable tier: T1** — for the service record (his own DA Form 66) and for what
the FBI cross-references do and do not contain (the released file itself).

**BOARD RECOMMENDATION: promote to its own node.** He is currently only a passing name in
`gerb-mitre-investigation`'s description, and there is now enough T1 material — a service
record confirming a three-month FTD chieftaincy, an FBI file confirming the OCB posting and
containing no UFO material at all, and a sworn statement that overstates his NSC role — for a
node that adjudicates rather than repeats.

---

## 3. Adm. Roscoe H. Hillenkoetter

**VERDICT: CONFIRMED, on both halves, and MJ-12 is not needed for either.**

This turned out to be the cleanest result in the slice, because the CIA's own reading room
holds the 1960 press coverage.

A Worcester (Mass.) *Gazette* clipping of **1 June 1960**, filed in CIA records and released in
2014, states that "Adm. R. H. Hillenkoetter, who headed the Central Intelligence Agency from
**May 1947 to October 1950**, recently declared, speaking about the so-called flying saucers:
'The unknown objects are operating under intelligent control. It is imperative that we learn
where the UFO's (unidentified flying objects) come from and what their purpose is.'" It quotes
him further, on the wartime and immediate post-war years: "I know that neither Russia nor this
country had anything even approaching such high speeds and maneuvers," and reports that
"Admiral Hillenkoetter wants a Congressional investigation of the UFOs." A second CIA-held
clipping, a *Enquirer* editorial of **4 March 1960**, independently records that "Admiral
Hillenkoetter, former director of the Central Intelligence Agency, is a board member of the
privately financed **NICAP**, the National Investigations Committee on Aerial Phenomena. As
such he has referred his conclusions to the **Senate Space Committee**, requesting an
investigation" — while itself disagreeing with him ("WE CANNOT wholly agree with the respected
Vice Adm. R. H. Hillenkoetter (ret.) that the Air Force is deceiving the public").

So both halves are documented from CIA-held records: his DCI dates, and his 1960 NICAP
board membership plus his public position that the Air Force was misleading the public and that
Congress should investigate.

**The MJ-12 question stays where it belongs, which is off this record.** The board's existing
`stanton-friedman` narrative already carries the finding that a purported 17 February 1948
Hillenkoetter-to-Truman memo was shown to be an emulation of a Marshall-to-Roosevelt letter —
that is a claim about a *document*, not about Hillenkoetter, and nothing above depends on it.

**Negative finding worth recording.** The National Security Archive's mirror of the FBI files
on Hillenkoetter (18 separate serials plus a main file) contains, across the sections I text-
searched, **zero** occurrences of NICAP, "flying saucer", "unidentified flying", Keyhoe, or
even the year 1960. His FBI file is not a UFO file. OCR quality on these scans is uneven, so
this is a strong indication rather than a proof, but it is the same shape of finding as the
Corso FBI release and points the same way.

**Sources opened:**

| URL | What is actually there |
|---|---|
| `https://archive.org/details/cia-readingroom-document-cia-rdp68-00046r000200090025-2` | **CIA-RDP68-00046R000200090025-2**, Worcester (Mass.) *Gazette*, 1 June 1960, "Congressional Action: Ex-C.I.A. Chief Wants UFO Probe" by Bulkley Griffin. "Declassified in Part - Sanitized Copy Approved for Release @ 50-Yr 2014/06/12". Carries a photo captioned "ADM. R. H. HILLENKOETTER Wants To Investigate U.F.O.'s". |
| `https://archive.org/details/cia-readingroom-document-cia-rdp68-00046r000200090028-9` | **CIA-RDP68-00046R000200090028-9**, *Enquirer*, 4 March 1960, editorial "Flying Saucers Again". Same release stamp. Names him as a NICAP board member and records the referral to the Senate Space Committee. |
| `https://archive.org/details/RoscoeH.Hillenkoetter` | FBI files on Hillenkoetter, National Security Archive mirror (collections `nsia-fbi-files`, `nationalsecurityarchive`). No NICAP or UFO content found in the sections searched. |

**Strongest supportable tier: T1** — a contemporaneous document held and released by CIA,
for both the DCI dates and the 1960 NICAP position.

**BOARD RECOMMENDATION: promote to its own node.** The first DCI publicly stating in 1960 that
the objects are "operating under intelligent control" and asking Congress to investigate is a
structural fact about the disclosure apparatus, it is T1, and it is currently reachable on this
board only through a sentence about a forged memo in someone else's narrative — which is
exactly backwards.

---

## 4. Thomas Townsend Brown

**VERDICT: PARTLY CONFIRMED. The patent record is real and I read all of it. The
"anti-gravity" framing is not in the patents, and Project Winterhaven does not say what the
secondary literature says it says.**

Brown's patents are genuine and I read the front matter of four of them off USPTO's own image
server. In his own words, in his own biographical sketch bound into the Project Winterhaven
proposal, he lists five patents; here are the four US ones as the patents themselves print them:

| Number | Title exactly as printed | Inventor line as printed | Filed | Issued |
|---|---|---|---|---|
| **1,974,483** | ELECTROSTATIC MOTOR | Thomas Townsend Brown, Zanesville, Ohio | Feb 7, 1930 (Ser. No. 426,738) | Sept 25, 1934 |
| **2,207,576** | METHOD AND APPARATUS FOR REMOVING SUSPENDED MATTER FROM GASES | Thomas Townsend Brown, Zanesville, Ohio | July 26, 1938 (Ser. No. 221,373) | July 9, 1940 |
| **2,417,347** | VIBRATION DAMPER | Thomas T. Brown, Laguna Beach, Calif., assignor by mesne assignments to **Lockheed Aircraft Corporation** | — | Mar 11, 1947 |
| **3,187,206** | ELECTROKINETIC APPARATUS | Thomas Townsend Brown, Walkertown, N.C., assignor by mesne assignments to **Electrokinetics, Inc.**, a corporation of Pennsylvania | May 9, 1958 (Ser. No. 734,342) | June 1, 1965 |

A fifth, **British Patent 300,311**, "Method and Apparatus for Producing Force or Motion", is
named twice in documents I read — in Brown's own Winterhaven biography and in the text of US
3,187,206, which says "my British Patent 300,311, issued August 15, 1927." **I did not open the
British patent.** Espacenet and the UK IPO both refuse this environment (403). The number and
date are therefore reported as *what two documents Brown authored say*, not as read off the
British grant. His Winterhaven list also names a **classified** "Buoyant Cable" patent assigned
to the U.S. Navy, with no number given.

**What the patents actually claim, which is the finding.** Neither 1,974,483 nor 3,187,206
claims gravity control. The 1934 patent claims "a method of producing force or motion by
applying and maintaining high potential electro-static charges in a system of chargeable
masses and associated electrodes", and says the motor "has been found to be useful, especially
in the operation of scientific instruments such as those used in observatories for recording
the movements of the earth, sun, moon, etc." The 1965 patent opens "This invention relates to
an electrical device for producing thrust by the direct operation of electrical fields", and
is explicit that the effect involves reaction against the environment: "When the device is
operated in a dielectric fluid medium, such as air, the forces of reaction appear to be
present in that medium as well as on all solid material bodies making up the physical
environment. In a vacuum, the reaction forces appear on the solid environmental bodies, such
as the walls of the vacuum chamber." That is an electrostatic-thrust claim, not an
anti-gravity claim. The word "electrogravitics" appears in neither.

**Project Winterhaven contradicts its own secondary literature.** The proposal is real: 66
pages, "PROJECT WINTERHAVEN — A PROPOSAL FOR JOINT SERVICES RESEARCH AND DEVELOPMENT CONTRACT,
THE TOWNSEND BROWN FOUNDATION, 416 Bowen Building, Washington 5, D.C.", and it contains an
enclosed **Franklin Institute letter dated 10 December 1952** addressed to Brown, which dates
the package to late 1952 / early 1953. It does propose research on "the control of
gravitation" and lists "electrified disc airfoils" among results to date. But I searched its
full text: the words **"saucer", "interceptor", "Mach" and "Air Force" appear zero times.**
The corpus's description — via the 1956 Aviation Studies (International) "Electrogravitics
Systems" report — of Winterhaven as "proposing construction of a saucer generating a local
gravitational field, designated as a USAF interceptor" is **not in the Winterhaven document**.
That framing belongs to the 1956 report, and any board claim must attribute it there.

Brown's own Winterhaven biography (which is a self-description, so T2 at best) gives: born
Zanesville, Ohio, 18 March 1905; Caltech, Kenyon, Denison; Naval Research Laboratory 1930-33;
staff physicist, International Gravity Expedition to the West Indies 1932; Johnson-Smithsonian
Deep Sea Expedition 1933; Bureau of Ships officer-in-charge of acoustic and magnetic
minesweeping 1940-41; Materials and Processes Engineer at Glenn L. Martin; radar consultant at
Lockheed; consulting physicist, Pearl Harbor Navy Yard. The **Lockheed** link is independently
corroborated by patent 2,417,347's assignment line, which is the one biographical item in that
list I can put against a second document.

**Provenance caveat on Winterhaven.** The only copy I could reach is a private upload to
archive.org's `opensource` collection with no institutional custody. The patents have no such
problem — they come from USPTO's own image server.

**Sources opened:**

| URL | What is actually there |
|---|---|
| `https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/1974483` | US 1,974,483, front page and full specification. |
| `https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/2207576` | US 2,207,576, front page and full specification. |
| `https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/2417347` | US 2,417,347, header page (inventor, assignee, issue date) and claims. |
| `https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/3187206` | US 3,187,206, header page, specification and claims, including the reference to British Patent 300,311. |
| `https://archive.org/details/projectwinterhaven` | 66-page *Project Winterhaven* proposal, Townsend Brown Foundation, with Brown's biographical sketch, patent list, table of contents and the Franklin Institute letter of 10 December 1952. **Private upload — no institutional custody.** |

**Strongest supportable tier: T1** — for the patents, each read off the USPTO document. The
Winterhaven proposal's *contents* are T1 for what the document says; its *authenticity as a
1952 artifact* is T2, resting on the uploader.

**BOARD RECOMMENDATION: promote to its own node.** He is the technical origin point the whole
electrogravitics thread is hung on, the board has no node for him at all, and the useful thing
a node can do here is exactly the separation this pass found — four verifiable patents, none
of which claims anti-gravity, against a 1956 secondary report that put a saucer interceptor
into a proposal that does not contain one.

---

## 5. Capt. Bradley R. Townsend, AFIT 2008

**VERDICT: CONFIRMED. Fully, at T1, including the abstract and the fastwalker material.**

The thesis is real, public, and says what the corpus says it says. Title page, verbatim:
**"Space Based Satellite Tracking and Characterization Utilizing Non-Imaging Passive
Sensors"**, THESIS, **Bradley R. Townsend, Captain, USA**, **AFIT/GA/ENY/08-M06**, Department
of the Air Force, Air University, Air Force Institute of Technology, Wright-Patterson Air
Force Base, Ohio, **APPROVED FOR PUBLIC RELEASE; DISTRIBUTION UNLIMITED**. Submitted for the
degree of Master of Science in Astronautical Engineering, **March 2008**; committee Dr. Ronald
F. Tuttle (chairman), Lt Col Nathan A. Titus, Lt Col Kerry D. Hicks. The SF 298 gives the
report date 10-03-2008 and the period covered as Sept 2007 – Mar 2008. Note he is a **US Army**
captain attending an Air Force school, not USAF.

**One correction to the corpus:** it lists him as "Air Force Institute of Technology" without
rank service — correct on the institution, but he is CPT, USA.

The abstract, verbatim in part: "A technique is developed to determine the orbit of a sunlight
illuminated satellite passing through the field-of-view of a sensor platform in a Highly
Elliptical Orbit (HEO) and Geosynchronous orbit (GEO)... In GEO test cases it proved impossible
to identify other objects in GEO given the limited data available... Over 82 percent of the
objects listed in the Air Force Space Command satellite catalog can be successfully identified
in orbit using this method."

**"Fastwalker" is used 34 times and is defined in the thesis's own words**, in §1.1: "Satellite
based sensors looking down at the Earth's surface occasionally observe reflected light from an
object passing through the image which is moving too fast relative to the background of the
image to be located within the atmosphere. **These objects are commonly called fastwalkers.
This term refers to any orbital object seen passing through the field of view of an Earth
observing sensor which is suspected of being in orbit.**" The words *UFO* and *unidentified* do
not appear anywhere in the 112 pages. The term is a piece of ordinary space-surveillance
vocabulary in this document, and the board should say so.

**The corpus's "1989 fastwalker paper" resolves.** §1.2 states: "In his thesis **Osedacz** [9]
states that a database of fastwalker observations exists with data from **as far back as 1972**.
He uses this data from obtained ballistic missile early warning satellites in GEO to attempt to
determine the orbit of these fastwalkers. His conclusion was that determining the orbit of
other fastwalkers in GEO was impossible. This supported the conclusions of an earlier work
conducted by **Lem Wong** on the inability to determine the orbit of these objects. The research
conducted by Wong is no longer available." Bibliography entry 9 reads: **"OSEDACZ, R. 'Orbit
determination of sunlight illuminated objects detected by overhead platforms (M. S. Thesis)'.
1989."** So the corpus's unresolved "Richard Postdocs" is **R. Osedacz**, and the 1972 database
claim and the "same inability to determine range" claim both come from a public AFIT thesis
citing another AFIT thesis. That is a genuinely strong lead: Osedacz 1989 is the next document
to obtain.

**Sources opened:**

| URL | What is actually there |
|---|---|
| `https://scholar.afit.edu/etd/2701` | AFIT Scholar landing page: title, author, March 2008, AFIT-GA-ENY-08-M06, abstract. (The `viewcontent.cgi` PDF link on that page returns 403 to this environment.) |
| `https://archive.org/details/DTIC_ADA478890` | The full 112-page thesis PDF, DTIC accession **ADA478890**, via the DTIC mirror. This is the copy I read. |

**Strongest supportable tier: T1** — a public, distribution-unlimited DoD thesis read in full.

**BOARD RECOMMENDATION: leave the person out; attach the DOCUMENT as a claim.** Capt. Townsend
is a student author with no other connection to this subject and does not deserve a node — but
the thesis does deserve a T1 claim on the fastwalker/NORAD/DSP material, because it is the
public document that defines the term, cites a 1972-onward detection database, and names the
1989 predecessor thesis. Attach it wherever the board carries the FASTWALKER designation.

---

## 6. Dr Eric Wang

**VERDICT: CONFIRMED for the institutional claim, at T1 — and this closes a corpus
inconsistency. NOT FOUND for anything UAP-related.**

The corpus was unsure about this name and the cross-check produced only a false-positive
near-miss ("Austin Wang" in an unrelated narrative). He is real, and he is named repeatedly
in the acknowledgments of the Operation UPSHOT-KNOTHOLE structures reports at DTIC. Verbatim
from the Project 3.1 final report:

> "Personnel of the Special Studies Section, who were intimately connected with the program,
> were **Eric H. Wang, Chief, Special Studies Office, who was the technical and scientific
> monitor for the Air Force Program**; **Arthur Stansel**; and Mrs. Maisie G. Ridgeway,
> secretary to Mr. Wang. Other members of the office who were associated with the program were
> R. R. Birukoff, P. A. Cooley, J. C. Noble, and Lt T. M. Murray and Lt G. A. Rockwell, USAF."

and:

> "Most of the introduction section of this report was taken from the preface of the
> Preliminary Report, Operation UPSHOT-KNOTHOLE, Project 3.1 **authored by Eric H. Wang and
> Bernard J. O'Brien**. The responsibility within the Air Force for execution of the six
> projects was transferred from the **Special Studies Office, Installations Division, Air
> Materiel Command** to Blast Effects Research, Mechanics Branch, Aeronautical Research
> Laboratory, Wright Air Development Center, on **15 November 1954**."

Four separate UPSHOT-KNOTHOLE reports carry the same passage. So: the office existed, Wang led
it, it sat in the Installations Division of Air Materiel Command, Arthur Stansel worked for
him, and the corpus's claim that Wang's role "is documented in the unclassified
Upshot-Knothole document itself" is **exactly right**.

**The relocation to Kirtland is confirmed too, from a later report.** A 1960 DTIC report
acknowledges "AFSWC personnel who were intimately connected with the project were **Eric H.
Wang, Chief, Structures Division**", at Headquarters Research Directorate, **Air Force Special
Weapons Center, Kirtland Air Force Base, New Mexico**. So he moved from AMC/Wright Field to
Kirtland and was still running a structures shop there in 1960.

**Three corrections the board must carry.**
1. It is the **"Special Studies Office"** / "Special Studies Section", inside the
   **Installations Division, Air Materiel Command**. The corpus's "Office of Special Studies"
   is close but not the printed name.
2. His middle initial is **H.** — Eric H. Wang.
3. The colleague is **Arthur Stansel**, not "Arthur Stancil". The Project 3.5 report even
   tracks him onward: "(now with Landing Gear Development Section, Equipment Laboratory,
   Wright Air Development Center)".

**What is NOT documented, and this is the important half.** Nothing in any of these reports
touches UAP, recovered materiel, reverse engineering, Kissinger, or Viktor Schauberger. Wang's
documented role is atomic blast effects on structures — which is a real and sensitive job at
Kirtland, and it is a job that explains his presence there without needing anything else. The
corpus itself flags the Kissinger and Schauberger links as needing work; this pass found no
document supporting either, and none supporting an Austrian birth. **Do not put the Kissinger
or Schauberger claims on the board at any tier.**

**Sources opened:**

| URL | What is actually there |
|---|---|
| `https://archive.org/details/DTIC_ADA073468` | *Operation Upshot-Knothole, Nevada Proving Grounds, March–June 1953. Project 3.1. Tests on the Loading of Building and Equipment Shapes*, DTIC ADA073468, dated 1955-07-01. Names Wang as Chief, Special Studies Office. |
| `https://archive.org/details/DTIC_ADA073475` | *Operation UPSHOT-KNOTHOLE... Project 3.5, Tests on the Response of Wall and Roof Panels...*, DTIC ADA073475, 1955-05-01. Same acknowledgment; tracks Stansel to WADC. |
| `https://archive.org/details/DTIC_AD0460283` | *Blast Effects on Existing Upshot-Knothole and Teapot Structures*, DTIC AD0460283, 1960-05-06. Names "Eric H. Wang, Chief, Structures Division" at AFSWC, Kirtland AFB. |

Two further reports carrying the identical Wang acknowledgment: DTIC ADA073476 (Project 3.4)
and DTIC ADA073477 (Project 3.3).

**Strongest supportable tier: T1** — unclassified DoD technical reports, read in full text.

**BOARD RECOMMENDATION: promote to his own node, scoped to what is documented.** A named,
documented Air Materiel Command office chief at Wright Field who moved to Kirtland is
substantive and T1, and a node is where the corrected spellings and the *absence* of any
Kissinger/Schauberger evidence can be stated. Promote the man; do not promote the story
attached to him.

---

## Summary table

| Person | Verdict | Best tier | Recommendation |
|---|---|---|---|
| Robert I. Sarbacher | PARTLY CONFIRMED | T1 (1983 letter facsimile) | Promote to node |
| Philip J. Corso | PARTLY CONFIRMED | T1 (DA Form 66; FBI release) | Promote to node |
| Roscoe H. Hillenkoetter | CONFIRMED | T1 (CIA-held 1960 clippings) | Promote to node |
| Thomas Townsend Brown | PARTLY CONFIRMED | T1 (four USPTO patents) | Promote to node |
| Bradley R. Townsend | CONFIRMED | T1 (AFIT thesis, full text) | Leave out; attach the thesis as a claim |
| Eric H. Wang | CONFIRMED (institutional) / NOT FOUND (UAP) | T1 (DTIC reports) | Promote to node, scoped to the documented role |

## Corrections this pass produced

| Where | Corpus / secondary says | Documents say |
|---|---|---|
| Corso affidavit | July 1998 | Sworn **May 1998**, day blank in the circulating copy; CAUS press release **8 June 1998** |
| Corso FBI release | July 2024 | FBI FOIPA cover letter **12 April 2024**; Black Vault published 31 July 2024 |
| Corso FBI release size | 321 pages | FBI letter: **449 reviewed, 313 released**; the posted PDF is 322 pages |
| Corso DA Form 66 requester | Larry Bryant (Black Vault case-file page) | Cover letter is addressed to **John Greenewald, Jr.** |
| Corso, Army FTD | "chief" (open-ended) | **Chief 18 Apr – 18 Jul 1962**; staff officer in the division from 20 Jul 1961 |
| Corso affidavit, NSC | "member of President Eisenhower's National Security Council" | DA Form 66: Intelligence Staff Officer, **Operations Coordinating Board**, 1954–57 |
| Project Winterhaven | proposes a saucer as a USAF interceptor | **No "saucer", "interceptor", "Mach" or "Air Force" anywhere in the document.** That framing is the 1956 Aviation Studies report's |
| Brown patents | "anti-gravity" | Titles and claims are **Electrostatic Motor** and **Electrokinetic Apparatus** — thrust by electrical fields, reacting against the environment |
| Eric Wang | "Office of Special Studies", "Arthur Stancil" | **Special Studies Office**, Installations Division AMC; **Arthur Stansel**; **Eric H. Wang** |
| Fastwalker 1989 paper | "Richard Postdocs" (unresolved) | **R. Osedacz**, M.S. thesis, 1989, *Orbit determination of sunlight illuminated objects detected by overhead platforms* |
| Bradley Townsend | Capt., AFIT | Captain, **USA** (Army officer at an Air Force school) |

## What could not be reached from this environment

| Target | Result |
|---|---|
| Wilbert Smith "Geo-Magnetics" memo, 21 Nov 1950, facsimile | **Not obtained.** Library and Archives Canada refuses this environment (403 / reset). The archive.org item a secondary page cites as a scan (`Smithmemo.PDF`) does not exist. |
| British Patent 300,311 | **Not opened.** Espacenet and UK IPO both 403. The number and 15 August 1927 date are reported only as what US 3,187,206 and Brown's own Winterhaven biography say. |
| *CAUS v. DoD*, 21 F. App'x 774, opinion text | **Not read.** CourtListener returns the citation and docket (No. 00-16036; D.C. No. CV-99-00108-SMM) through its search API but gates the opinion body behind authentication. |
| Signed original of the Corso affidavit | **Not opened.** Only a text reproduction. |
| `apps.dtic.mil` direct PDFs | 403 to both curl and WebFetch. The `archive.org/details/DTIC_*` mirror served every document needed. |
| `patents.google.com` | 503. USPTO's `image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/<number>` works and is the better source anyway — it returns the scanned grant. |

## Next documents to obtain

1. **Osedacz, R., M.S. thesis, 1989**, *Orbit determination of sunlight illuminated objects
   detected by overhead platforms* — AFIT. Named in a public thesis; would be the primary
   source for the 1972-onward fastwalker database claim.
2. **The 1950 Smith memorandum in facsimile** — Library and Archives Canada, or the University
   of Ottawa holdings a secondary source points at. Needs a requester outside this environment.
3. **Research and Development Board personnel records** (NARA RG 330) — the only way to settle
   whether Sarbacher's consultancy is documented anywhere but in his own 1983 recollection.
4. **British Patent GB 300,311** — from a reachable patent office mirror.
