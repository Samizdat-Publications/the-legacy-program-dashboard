# Verified leads: Michels corpus candidates 6 to 10 (verifier 2)

**Status: research output, not board content.** Nothing here has been merged into
`research/` or into any node. This is a verification pass over rows 6 to 10 of
`research/leads/CANDIDATES-2026-09-02-MICHELS-DRAFT.md`, which are unverified podcast
claims by construction.

**Verified 2 September 2026.** Every URL in the tables below was opened by this session
and returned the document described. Where a PDF had no usable text layer it is said so.
`CLAUDE.md` section 2 applies: nothing here is asserted that was not opened.

**None of the five is on the board.** Checked directly against `data/the-program.json`:
zero occurrences of "Manned Orbiting", "Defense Support Program", "Personnel Reliability",
"Dorian" and "KH-10"; one occurrence of "Invention Secrecy", inside the `d-secrecy`
description, which names the Act and carries no node for it; no `inman` node id (the 16
substring hits are all "Steinman").

## Summary

| # | Lead | Verdict | Board |
|---|---|---|---|
| 6 | Invention Secrecy Act, 35 U.S.C. 181-188 | CONFIRMED, the candidate's "of 1952" short title CONTRADICTED | new node |
| 7 | Personnel Reliability Program | PARTLY CONFIRMED | new node, on the 1993 directive only |
| 8 | Manned Orbiting Laboratory | CONFIRMED | new node |
| 9 | Defense Support Program and the Black Vault fastwalker FOIA | PARTLY CONFIRMED | new node for DSP; the FOIA denial is a claim on it |
| 10 | Bobby Ray Inman | CONFIRMED, the transcript's "headed SAIC" CONTRADICTED | new node |

**The four findings that matter most, in order:**

1. **The Act's own short title is "Invention Secrecy Act of 1951", printed in the margin
   of the Statutes at Large, and the Act was approved on 1 February 1952.** The candidate
   row and triage row 4.A4 say "of 1952"; triage row 5.A4 says "of 1951" and is right.
   The 1952 date belongs to a different statute, the Patent Act of 19 July 1952, which is
   where the current 35 U.S.C. 181-188 numbering comes from. Both facts are on opened
   pages and neither speaker had them straight.
2. **Inman was never head of SAIC.** SAIC's own proxy statement names him a Director since
   1982 and a part-time employee since 1990 advising on strategic planning, paid $132,129
   in fiscal 2003, while J.R. Beyster was Chairman, CEO and President. The transcript
   claim at corpus 12 file 3, 0:19:28 that Inman "headed it" is wrong on the record.
3. **A named service refused a named designation in writing, twice, and the 2013 letter
   is readable.** USNORTHCOM found two responsive documents on "fastwalkers" and
   "slowwalkers" and withheld both as properly classified, and separately declined to
   search NORAD holdings at all on the ground that NORAD is a bi-national organisation
   outside FOIA. That second sentence is the more useful of the two for this board.
4. **The board's `afit-townsend-2008` node already points at DSP without naming it.**
   Its quoted section 1.2 says Osedacz used "data from obtained ballistic missile early
   warning satellites in GEO". DSP is the constellation that phrase describes, and the
   board has no node for it. But no opened government document equates "fastwalker" with
   DSP by name; that equation is The Black Vault's own gloss.

**Reach notes for the next session.** `nro.gov` returned 403 to every request from here,
by WebFetch and by curl alike, including `/FOIA/MOL`, `/About-NRO/history/history-MOL/`
and the `Portals/135/documents/foia/declass/mol/` PDFs. `CLAUDE.md` section 9 lists
nro.gov as reachable; on 2 September 2026 it was not. The NRO's own MOL account was
obtained instead from the GPO copy of the NRO Center for the Study of National
Reconnaissance volume on govinfo. `esd.whs.mil` (403 on both the DoDM and DoDI paths),
`spaceforce.mil`, `losangeles.spaceforce.mil`, `buckley.spaceforce.mil`,
`nationalmuseum.af.mil` and `nsa.gov` all returned 403; `afspc.af.mil` and `au.af.mil`
fail at TLS and DNS respectively. `sec.gov` refuses WebFetch with 403 but answers curl
with a contact user-agent, which is how EDGAR was read.

---

## 6. Invention Secrecy Act, 35 U.S.C. 181-188

**VERDICT: CONFIRMED** for the statute, its mechanism and the published order counts.
**The candidate row's short title is CONTRADICTED**: the Act is the Invention Secrecy Act
of 1951, approved 1 February 1952.

### What was opened

| URL | What is at it |
|---|---|
| https://www.govinfo.gov/content/pkg/STATUTE-66/pdf/STATUTE-66-Pg3.pdf | Statutes at Large volume 66, page 3. "Public Law 256", "CHAPTER 4", "AN ACT To provide for the withholding of certain patents that might be detrimental to the national security, and for other purposes", "February 1, 1952 [H.R.4687]". The marginal note printed beside section 1 reads "Invention Secrecy Act of 1951." A second marginal note reads "Post, p. 815", pointing at the Patent Act later in the same volume. |
| https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title35-section181&num=0&edition=prelim | 35 U.S.C. 181 in full, with its source credit and Historical and Revision Notes. |
| https://uscode.house.gov/view.xhtml?req=granuleid%3AUSC-prelim-title35-chapter17&edition=prelim | Chapter 17 headings for sections 181 to 188. |
| https://sgp.fas.org/othergov/invention/index.html | "Invention Secrecy", Federation of American Scientists Project on Government Secrecy. States the Act was enacted in 1951 and is codified at 35 U.S.C. 181-188, and that a secrecy order can reach an application "generated and entirely owned by a private individual or company without government sponsorship". |
| https://sgp.fas.org/othergov/invention/stats.html | The FAS secrecy-order table, sourced to the Patent and Trademark Office. FY21 to FY25: new orders 61, 87, 125, 356, 102; rescinded 0, 6, 27, 40, 30; total in effect 5,976, 6,057, 6,155, 6,471, 6,543. |

### What the record establishes

The 1952 codification of Title 35 restates the 1951 Act. The Historical and Revision Notes
under section 181 read: "Based on Title 35, U.S.C., 1946 ed., §151 (Feb. 1, 1952, ch. 4,
§1, 66 Stat. 3, 4)." The section's own source credit is "July 19, 1952, ch. 950, 66 Stat.
805", the Patent Act. So the substance is 1951 Act and the numbering is 1952 Act, and the
candidate row has collapsed the two.

Section 181's second paragraph is the one that matters to a board with a patents tab. It
reaches inventions "in which the Government does not have a property interest", and on the
Commissioner of Patents' own opinion makes such an application "available for inspection
to the Atomic Energy Commission, the Secretary of Defense, and the chief officer of any
other department or agency of the Government designated by the President as a defense
agency". A secrecy order runs for one year, renewable annually without limit, and an order
in effect during war "shall remain in effect for the duration of hostilities and one year
following cessation of hostilities". Section 186 sets the penalty at a fine of not more
than $10,000, imprisonment for not more than two years, or both.

The chapter headings are: 181 secrecy and withholding, 182 abandonment for unauthorised
disclosure, 183 right to compensation, 184 filing abroad, 185 patent barred for filing
without licence, 186 penalty, 187 nonapplicability to certain persons, 188 rules and
delegation.

### What the transcripts claimed that the record does NOT establish

| Claim | Where | Status |
|---|---|---|
| Charles Buhler's first patent "may carry an undisclosed national-security hold" under the Act | corpus 20 file 01, 1:30;45 to 1:31;38 (S1) | NOT ESTABLISHED, and the speaker says on air that he does not know either way. No secrecy order on any Buhler application was sought or found in this pass. A secrecy order is not a public record, so absence of evidence here is expected and must not be written up as evidence of absence. |
| The Act is why classified inventions such as programmable matter "would never surface as patents" | corpus 21 file 4, 0:59:15 | The mechanism is real and documented. The application of it to any particular technology is the speaker's inference and is not gradeable above T3. |
| "Invention Secrecy Act of 1952" | candidate row 6, triage 4.A4 | CONTRADICTED by the Statutes at Large marginal title. |

### Draft node

```json
{
  "id": "invention-secrecy-act",
  "cls": "legislation",
  "label": "Invention Secrecy Act of 1951 (Pub. L. 82-256, 66 Stat. 3), codified at 35 U.S.C. 181-188",
  "cluster": "oversight",
  "sub": "Act of 1 February 1952, ch. 4; renumbered by the Patent Act of 19 July 1952, ch. 950, 66 Stat. 805",
  "tier": "B",
  "dateStart": "1952-02-01",
  "dateEnd": null,
  "desc": "The statute that lets the United States order an invention kept secret and withhold the patent, including an invention the government does not own and did not fund. It is the instrument the board's PATENTS tab is arguing around, and until now the board named it once in prose and carried no node for it. Its short title, printed in the margin of the Statutes at Large, is the Invention Secrecy Act of 1951, although the Act was approved on 1 February 1952; the familiar 35 U.S.C. 181-188 numbering comes from a different statute five months later, the Patent Act of 19 July 1952. Section 181's second paragraph routes a privately owned application to the Atomic Energy Commission and the Secretary of Defense for inspection before any order issues, which is the point at which the patent record and the weapons establishment touch. Orders run one year and renew annually without limit; the Patent and Trademark Office reported 6,543 in force at the end of fiscal 2025.",
  "claims": [
    {
      "tier": 1,
      "text": "The Act's own short title and date: the Statutes at Large prints the marginal note 'Invention Secrecy Act of 1951.' beside section 1 of 'Public Law 256', 'CHAPTER 4', an Act 'To provide for the withholding of certain patents that might be detrimental to the national security, and for other purposes', approved 'February 1, 1952 [H.R.4687]'.",
      "source": "66 Stat. 3, Statutes at Large volume 66, govinfo, https://www.govinfo.gov/content/pkg/STATUTE-66/pdf/STATUTE-66-Pg3.pdf"
    },
    {
      "tier": 1,
      "text": "The current codification descends from that Act by way of a second one. The Historical and Revision Notes to 35 U.S.C. 181 read: 'Based on Title 35, U.S.C., 1946 ed., §151 (Feb. 1, 1952, ch. 4, §1, 66 Stat. 3, 4).' The section's source credit is 'July 19, 1952, ch. 950, 66 Stat. 805'.",
      "source": "35 U.S.C. 181, Office of the Law Revision Counsel, https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title35-section181&num=0&edition=prelim"
    },
    {
      "tier": 1,
      "text": "The Act reaches inventions the government does not own. Section 181 second paragraph: where the Commissioner of Patents believes disclosure of an invention 'in which the Government does not have a property interest' might be detrimental to the national security, 'he shall make the application for patent in which such invention is disclosed available for inspection to the Atomic Energy Commission, the Secretary of Defense, and the chief officer of any other department or agency of the Government designated by the President as a defense agency of the United States.'",
      "source": "35 U.S.C. 181, Office of the Law Revision Counsel, https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title35-section181&num=0&edition=prelim"
    },
    {
      "tier": 1,
      "text": "An order is indefinite by renewal, and wartime orders outlast the war. Section 181: 'An invention shall not be ordered kept secret and the publication of the application or the grant of a patent withheld for a period of more than one year', renewable annually on an affirmative determination that 'the national interest continues so to require'; an order in effect during a time when the United States is at war 'shall remain in effect for the duration of hostilities and one year following cessation of hostilities.'",
      "source": "35 U.S.C. 181, Office of the Law Revision Counsel, https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title35-section181&num=0&edition=prelim"
    },
    {
      "tier": 1,
      "text": "The order count is published annually and is rising. The Federation of American Scientists' table, sourced to the Patent and Trademark Office, records secrecy orders in effect at fiscal year end of 5,976 (FY21), 6,057 (FY22), 6,155 (FY23), 6,471 (FY24) and 6,543 (FY25), with 356 new orders imposed in FY24 against 102 in FY25.",
      "source": "Invention Secrecy Statistics, FAS Project on Government Secrecy, https://sgp.fas.org/othergov/invention/stats.html"
    }
  ],
  "sources": [
    {"name": "66 Stat. 3, Act of February 1, 1952, ch. 4 (Public Law 82-256)", "url": "https://www.govinfo.gov/content/pkg/STATUTE-66/pdf/STATUTE-66-Pg3.pdf", "date": "1952-02-01"},
    {"name": "35 U.S.C. 181, Secrecy of certain inventions and withholding of patent", "url": "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title35-section181&num=0&edition=prelim"},
    {"name": "35 U.S.C. chapter 17, sections 181 to 188", "url": "https://uscode.house.gov/view.xhtml?req=granuleid%3AUSC-prelim-title35-chapter17&edition=prelim"},
    {"name": "Invention Secrecy, FAS Project on Government Secrecy", "url": "https://sgp.fas.org/othergov/invention/index.html"},
    {"name": "Invention Secrecy Statistics, FAS Project on Government Secrecy", "url": "https://sgp.fas.org/othergov/invention/stats.html"}
  ],
  "edges": [
    {"a": "invention-secrecy-act", "b": "d-secrecy", "type": "legislative", "claimTier": 1, "note": "The domain description already names this Act as one of the three statutory layers of the secrecy architecture and the board carried no node for it."},
    {"a": "invention-secrecy-act", "b": "fas", "type": "investigative", "claimTier": 1, "note": "FAS obtains and publishes the annual secrecy-order counts from the Patent and Trademark Office, which is the only public series on how often the Act is used."},
    {"a": "invention-secrecy-act", "b": "usc-50-3510", "type": "legislative", "claimTier": 2, "note": "Two statutory instruments of the same architecture, one hiding an invention and the other hiding an expenditure; the pairing is the board's argument, not either statute's text."},
    {"a": "invention-secrecy-act", "b": "pais-patent-imrd", "type": "programmatic", "claimTier": 2, "note": "A Navy-assigned propulsion patent that did issue is the control case for the tab: the Act is why an absence in the patent record is a legal artefact rather than evidence of nothing."}
  ]
}
```

---

## 7. Personnel Reliability Program

**VERDICT: PARTLY CONFIRMED.** The programme, its reliability standard, its disqualifying
categories and its medical-records regime are documented in a distribution-unlimited DoD
directive that was opened and read. What is not established is anything the transcripts
attach to it: the "167" figure, the ibuprofen detail, and any connection to reporting an
aerial sighting.

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/download/DTIC_ADA271698/DTIC_ADA271698_djvu.txt | OCR text of DTIC accession AD-A271698, "Department of Defense Directive Number 5210.42, May 25, 1993, ASD(C3I), SUBJECT: Nuclear Weapon Personnel Reliability Program (PRP)". Marked "approved for public release and sale; its distribution is unlimited". It reissues and cancels DoD Directive 5210.42 of 6 December 1985. |
| https://nuke.fas.org/guide/usa/doctrine/dod/dodd-5210_42.htm | FAS transcription of the same directive through Change 1 and Change 2 (15 December 1995). Used only as a cross-check on the alcohol and drug provisions; it is a transcription, not a scan. |

The current governing issuances, DoDM 5210.42 and DoDI 5210.42, were **NOT OPENED**.
Both live at `esd.whs.mil`, which returned 403 to WebFetch and to curl on
`/Portals/54/Documents/DD/issuances/dodm/521042m.pdf`,
`/Portals/54/Documents/DD/issuances/dodm/521042_vol1.pdf` and
`/Portals/54/Documents/DD/issuances/dodi/521042p.pdf`. The Air Force implementing
instruction AFI 91-115 at `static.e-publishing.af.mil` also returned 403. A node built
from this pass must be dated and worded to the 1993 directive and must not assert what
the 2015 manual says.

### What the record establishes

The directive applies to "DoD military and civilian personnel and contractor employees
assigned to PRP positions or in training leading to assignment to PRP positions". Its
purpose is to "ensure the highest possible standards of individual reliability in
personnel performing duties associated with nuclear weapons and critical components".

The reliability judgment is made by a certifying official on "the individual's personnel
security eligibility, physical and mental capability, personnel and medical records, and a
personal interview", to decide whether the individual "can be depended on to respond in a
reasonably stable manner" in a PRP position.

Two provisions carry the weight for this board. First, the disqualifying category
"Poor Attitude or Lack of Motivation" covers "aberrant attitude (arrogance, inflexibility,
or suspiciousness), behavior (impulsiveness, destructiveness, or suicide threats), or mood
(unusual happiness, sadness, or agitation)", and the "Medical Condition" category covers
any "characteristic of aberrant behavior considered by the certifying official to be
prejudicial to reliable performance". Second, the medical file is not private from the
chain: "medical records may be disclosed to reviewing and certifying officials for this
purpose without either a request from, or the consent of, the individuals to whom those
records pertain", and potentially disqualifying medical information is documented in the
health record, which is "marked to reflect assignment of an individual to a PRP position".
The personal interview informs the individual of "the individual's responsibility for
self-reporting and peer review of factors and situations that could adversely affect job
performance or reliability".

On medication the directive is narrower than the transcripts suggest. It says the
certifying official must be advised of any "medical condition, prescribed medication, or
treatment that could detract from the ability of an individual in the PRP to perform
assigned duties", as determined by the competent medical authority, and that it "is not
the intent of the PRP to automatically decertify an individual" for an illness requiring
hospitalisation unless the condition is long-term or permanent.

### What the transcripts claimed that the record does NOT establish

| Claim | Where | Status |
|---|---|---|
| Personnel must report "even taking ibuprofen" | corpus 05 files 01 and 02; corpus 20 file 03, 0:34;50 | NOT ESTABLISHED. The directive's medication rule is a competent-medical-authority determination about impairment, not a blanket duty to report an over-the-counter analgesic. The witnesses may be describing a service instruction rather than the directive; AFI 91-115 could not be opened. |
| "Roughly 167 people on the PRP program at U.S. nuclear sites" | corpus 20 file 03, 0:34;50 to 0:36;23 | CONTRADICTED as stated, on the corpus's own reading. Corpus 24 file 01 at 0:13:03 attributes the same number to Robert Hastings's 167 nuclear-base witnesses, who are PRP-cleared staff, not the size of the programme. The board carries no 167 figure and this pass found none in any opened record. |
| PRP is why a witness omitted what he saw from a written statement to his commander | triage 1.A12, corpus 05 file 02, 02;41 to 03;36 and 59;33 | NOT ESTABLISHED by any document. The directive contains no provision about reporting aerial phenomena. What it does supply is the mechanism a witness could reasonably fear: an "aberrant behavior" finding by a non-medical certifying official with unconsented access to his medical record. That is an inference and caps at T3. |

### Draft node

```json
{
  "id": "prp-nuclear-weapon",
  "cls": "program",
  "label": "DoD Nuclear Weapon Personnel Reliability Program (DoD Directive 5210.42)",
  "cluster": "oversight",
  "sub": "DoDD 5210.42, 25 May 1993, ASD(C3I); reissues the directive of 6 December 1985",
  "tier": "C",
  "dateStart": "1985-12-06",
  "dateEnd": null,
  "desc": "The published rule that decides whether a person on a nuclear weapons site keeps his access, and the reason the board can treat 'they were afraid to report' as something other than an anecdote. The directive opened here is the 25 May 1993 edition, distribution unlimited, which reissues an edition of 6 December 1985; the current manual could not be reached from this environment and nothing here should be read as describing it. Its force for this board is not what it says about UFOs, which is nothing, but what it says about who may find a person unreliable and on what evidence: a non-medical certifying official, with access to the individual's medical record without his consent, may act on 'aberrant behavior' or on mood described as unusual happiness, sadness or agitation. Every witness at a nuclear site whose testimony this board carries was subject to a rule of that shape.",
  "claims": [
    {
      "tier": 1,
      "text": "Scope and purpose: the directive applies to 'DoD military and civilian personnel and contractor employees assigned to PRP positions or in training leading to assignment to PRP positions', and exists to 'ensure the highest possible standards of individual reliability in personnel performing duties associated with nuclear weapons and critical components.'",
      "source": "DoD Directive 5210.42, 25 May 1993, sections A and B, DTIC AD-A271698"
    },
    {
      "tier": 1,
      "text": "Disqualification reaches demeanour, not only conduct. Under 'Poor Attitude or Lack of Motivation' the directive lists 'aberrant attitude (arrogance, inflexibility, or suspiciousness), behavior (impulsiveness, destructiveness, or suicide threats), or mood (unusual happiness, sadness, or agitation).'",
      "source": "DoD Directive 5210.42, 25 May 1993, enclosure 4, DTIC AD-A271698"
    },
    {
      "tier": 1,
      "text": "The medical file is open to the chain without consent: 'medical records may be disclosed to reviewing and certifying officials for this purpose without either a request from, or the consent of, the individuals to whom those records pertain', and the health record is 'marked to reflect assignment of an individual to a PRP position'.",
      "source": "DoD Directive 5210.42, 25 May 1993, enclosure 4, DTIC AD-A271698"
    },
    {
      "tier": 1,
      "text": "The programme runs on self-reporting and peer review. The certifying official's personal interview must inform the individual of 'the individual's responsibility for self-reporting and peer review of factors and situations that could adversely affect job performance or reliability.'",
      "source": "DoD Directive 5210.42, 25 May 1993, enclosure 4, DTIC AD-A271698"
    },
    {
      "tier": 2,
      "text": "Speakers on the American Alchemy corpus describe PRP as a reason nuclear-site personnel did not report what they saw, and attach a figure of 167 to it. The 167 is Robert Hastings's count of nuclear-base witnesses, not a count of PRP personnel; no opened record supports either the figure or the reporting claim.",
      "source": "American Alchemy, episode with Mario Woods, 02;41 to 03;36 and 59;33 to 1:00;25; and the Michael Shermer episode of 9 July 2026, 0:13:03"
    }
  ],
  "sources": [
    {"name": "DoD Directive 5210.42, Nuclear Weapon Personnel Reliability Program (PRP), 25 May 1993, DTIC accession AD-A271698", "url": "https://archive.org/download/DTIC_ADA271698/DTIC_ADA271698_djvu.txt", "date": "1993-05-25"},
    {"name": "DoD Directive 5210.42 through Change 2, FAS transcription", "url": "https://nuke.fas.org/guide/usa/doctrine/dod/dodd-5210_42.htm"}
  ],
  "edges": [
    {"a": "prp-nuclear-weapon", "b": "dod", "type": "institutional", "claimTier": 1, "note": "The directive is issued under the authority of the Assistant Secretary of Defense (C3I) and binds every DoD component."},
    {"a": "prp-nuclear-weapon", "b": "robert-salas", "type": "witness-chain", "claimTier": 3, "note": "Salas was a missile combat crew commander at a PRP site; the programme is the administrative regime his testimony was given against, which is an inference from the directive's scope and not a statement about him."},
    {"a": "prp-nuclear-weapon", "b": "l-malmstrom", "type": "geographic", "claimTier": 2, "note": "A nuclear weapons installation whose crews fall inside the directive's stated scope of personnel assigned to PRP positions."},
    {"a": "prp-nuclear-weapon", "b": "d-secrecy", "type": "programmatic", "claimTier": 3, "note": "The board's suppression argument usually runs through classification; PRP is the administrative alternative, a published rule that can remove a person from his job without any classification decision at all."}
  ]
}
```

---

## 8. Manned Orbiting Laboratory

**VERDICT: CONFIRMED**, on every element of the lead, from the NRO's own published account
and a NASA history article.

### What was opened

| URL | What is at it |
|---|---|
| https://www.govinfo.gov/content/pkg/GOVPUB-D-PURL-gpo123652/pdf/GOVPUB-D-PURL-gpo123652.pdf | "SPIES IN SPACE: Reflections on National Reconnaissance and the Manned Orbiting Laboratory", by Courtney V. K. Homer, Center for the Study of National Reconnaissance, May 2019, published by the National Reconnaissance Office, ISBN 978-1-937219-24-6, GPO PURL GOVPUB-D-PURL-gpo123652. 4.2MB PDF with a text layer, read from the front matter through chapter 4. |
| https://www.govinfo.gov/app/details/GOVPUB-D-PURL-gpo123652 | The govinfo catalogue record for the same item. |
| https://www.nasa.gov/history/55-years-ago-manned-orbiting-laboratory-cancellation/ | "55 Years Ago: Manned Orbiting Laboratory Cancellation", John Uri, NASA, 11 June 2024. |

`nro.gov` itself, where the 850 declassified Dorian documents sit, returned 403 to every
attempt. The declassified collection is therefore **NOT OPENED**; what is opened is the
NRO's own published description of it.

### What the record establishes

The NRO's foreword states that the programme's public face was announced by an Air Force
press release in December 1963 to "increase the Defense Department effort to determine
military usefulness of men in space", and that behind it sat "Dorian, a deeply classified
program managed by the then darkly hidden agency of the Intelligence Community, the
National Reconnaissance Office". The volume's own summary of the arrangement is that MOL
was "open 'white' world, but maintained a highly-classified 'black' mission", with the
reconnaissance mission "codenamed Dorian in the BYEMAN security system".

The declassification is dated and quantified in the NRO's own words: on 22 October 2015
the CSNR held a panel at the National Museum of the United States Air Force "on the
occasion of the NRO declassifying almost its entire collection of records on the Dorian
program. There were over 850 documents with some 22,000 pages and 280 photographs."
Line-by-line review took over a year, and the Information Review and Release Group posted
the collection on the NRO public web page the day after the panel.

On the hardware, the volume records a laboratory module 10 feet in diameter and 19 feet
long with a 1,000 cubic foot pressurised compartment for a two-man crew on a 30-day
mission, a Mission Payload System Segment 10 feet by 37 feet, and a camera-optical system
with a 70-inch aperture designed for "superior resolution photographs from an altitude of
80 nautical miles"; "In 1969, the Dorian camera system was designated KH-10 within the
Talent-Keyhole community." Seventeen individuals were astronaut-trained between 1965 and
1969 and none of them flew on the programme. On the day of termination, 10 June 1969,
"13,187 contractor personnel were cleared on MOL and faced reassignment".

The NASA article supplies the parts the NRO volume does not date directly: announcement by
Defense Secretary Robert S. McNamara in December 1963, formal approval by President Johnson
in August 1965, selections of eight, five and four pilots on 12 November 1965, 17 June 1966
and 30 June 1967, launch on the Titan-IIIM from Vandenberg Air Force Base into polar orbit,
cancellation on 10 June 1969, and that the programme was "not declassified by the NRO until
October 2015". It gives the imaging system as "a 72-inch diameter primary mirror".

**One numeric disagreement between two opened sources, recorded rather than resolved:**
the NRO volume says a 70-inch aperture and NASA says a 72-inch diameter primary mirror.
An aperture and a mirror diameter are not necessarily the same measurement. Do not average
them and do not pick one silently.

### What the transcripts claimed that the record does NOT establish

| Claim | Where | Status |
|---|---|---|
| MOL was cancelled "one month before Apollo 11 reached the moon" | corpus 18 file 2, throughout | Broadly right and not exactly one month: 10 June 1969 to the 20 July 1969 landing is forty days. The corpus's own section 4 already flagged this for checking. |
| MOL is "a precedent for a still-unaccounted-for classified space effort" | corpus 18 file 4, 1:18:20 to 1:20:09 | The precedent is real. The inference from it to a current unacknowledged programme is the speaker's and is not gradeable above T3. |
| MOL was "nominally canceled once NRO satellites were judged to image better than a person could" | corpus 24 file 03, 1:44:06 | Consistent with the NRO volume, which says it "was cancelled in favor of better unmanned photoreconnaissance satellites and the promise of near real-time electro-optical imagery". The word "nominally" is the speaker's and the record does not support it. |

### Draft node

```json
{
  "id": "manned-orbiting-laboratory",
  "cls": "program",
  "label": "Manned Orbiting Laboratory and the DORIAN / KH-10 reconnaissance payload",
  "cluster": "programs",
  "sub": "USAF programme with an NRO black mission; announced December 1963, cancelled 10 June 1969, declassified October 2015",
  "tier": "B",
  "dateStart": "1963-12",
  "dateEnd": "1969-06-10",
  "desc": "A fully documented case of a real programme carrying a second, classified programme inside it, closed by the government and then released by the agency that ran it. Publicly MOL was an Air Force laboratory to determine the military usefulness of men in space; inside it sat DORIAN, an NRO reconnaissance system handled in the BYEMAN control system and designated KH-10 in 1969. Seventeen officers were astronaut-trained between 1965 and 1969, on a modified Gemini-B with a hatch through the heat shield, for polar launches from Vandenberg on the Titan-IIIM. None of them flew. The programme was cancelled on 10 June 1969 with 13,187 cleared contractor personnel on it, and the NRO declassified almost the entire DORIAN collection in October 2015. It is the strongest available answer to a question this board is repeatedly asked, which is what a secret space programme actually looks like on the record.",
  "claims": [
    {
      "tier": 1,
      "text": "The cover and the mission are described by the agency itself. The NRO's volume says MOL was 'open \"white\" world, but maintained a highly-classified \"black\" mission', with the reconnaissance mission 'codenamed Dorian in the BYEMAN security system', and its foreword calls Dorian 'a deeply classified program managed by the then darkly hidden agency of the Intelligence Community, the National Reconnaissance Office'.",
      "source": "Spies in Space: Reflections on National Reconnaissance and the Manned Orbiting Laboratory, NRO Center for the Study of National Reconnaissance, May 2019, foreword and chapter 3"
    },
    {
      "tier": 1,
      "text": "The declassification is dated and quantified in the NRO's own words: on 22 October 2015 the CSNR held a panel at the National Museum of the United States Air Force 'on the occasion of the NRO declassifying almost its entire collection of records on the Dorian program. There were over 850 documents with some 22,000 pages and 280 photographs.'",
      "source": "Spies in Space, NRO CSNR, May 2019, foreword"
    },
    {
      "tier": 1,
      "text": "Seventeen officers were trained and none flew: 'Between 1965 and 1969, quietly and without fanfare, 17 non-NASA individuals were astronaut-trained in order to meet the reconnaissance needs of the United States.' The camera is dated and designated: 'In 1969, the Dorian camera system was designated KH-10 within the Talent-Keyhole community.'",
      "source": "Spies in Space, NRO CSNR, May 2019, introduction and chapter 3"
    },
    {
      "tier": 1,
      "text": "The scale of the clearance at termination: 'On 10 June 1969, 13,187 contractor personnel were cleared on MOL and faced reassignment.'",
      "source": "Spies in Space, NRO CSNR, May 2019, chapter 4"
    },
    {
      "tier": 1,
      "text": "NASA's history office dates the programme's public and classified halves: announced by Defense Secretary Robert S. McNamara in December 1963, formally approved by President Johnson in August 1965, 17 pilots selected in three groups on 12 November 1965, 17 June 1966 and 30 June 1967, flown on the Titan-IIIM from Vandenberg into polar orbit, cancelled 10 June 1969, and 'not declassified by the NRO until October 2015'.",
      "source": "John Uri, '55 Years Ago: Manned Orbiting Laboratory Cancellation', NASA, 11 June 2024, https://www.nasa.gov/history/55-years-ago-manned-orbiting-laboratory-cancellation/"
    }
  ],
  "sources": [
    {"name": "Spies in Space: Reflections on National Reconnaissance and the Manned Orbiting Laboratory, Courtney V. K. Homer, NRO Center for the Study of National Reconnaissance, May 2019 (GPO, GOVPUB-D-PURL-gpo123652)", "url": "https://www.govinfo.gov/content/pkg/GOVPUB-D-PURL-gpo123652/pdf/GOVPUB-D-PURL-gpo123652.pdf", "date": "2019-05-01"},
    {"name": "govinfo catalogue record for Spies in Space", "url": "https://www.govinfo.gov/app/details/GOVPUB-D-PURL-gpo123652"},
    {"name": "55 Years Ago: Manned Orbiting Laboratory Cancellation, NASA", "url": "https://www.nasa.gov/history/55-years-ago-manned-orbiting-laboratory-cancellation/", "date": "2024-06-11"}
  ],
  "edges": [
    {"a": "manned-orbiting-laboratory", "b": "nro", "type": "programmatic", "claimTier": 1, "note": "The NRO ran the DORIAN payload inside the Air Force programme and is the agency that declassified the collection in 2015."},
    {"a": "manned-orbiting-laboratory", "b": "usaf", "type": "institutional", "claimTier": 1, "note": "MOL was the Air Force's public programme and the service that selected and trained the seventeen officers."},
    {"a": "manned-orbiting-laboratory", "b": "l-vandenberg", "type": "geographic", "claimTier": 1, "note": "Polar launches were to fly from Vandenberg on the Titan-IIIM, per the NASA history article."},
    {"a": "manned-orbiting-laboratory", "b": "nasa", "type": "institutional", "claimTier": 1, "note": "After cancellation the younger MOL astronauts transferred to NASA, which is why an intelligence programme's people are traceable in a civil agency's record."},
    {"a": "manned-orbiting-laboratory", "b": "d-secrecy-architecture", "type": "programmatic", "claimTier": 2, "note": "A worked example of the compartmentation the domain describes: one workforce, two programmes, and a BYEMAN boundary running through the middle of it."}
  ]
}
```

---

## 9. Defense Support Program, and the Black Vault fastwalker FOIA

**VERDICT: PARTLY CONFIRMED.** DSP exists and is documented in federal records that were
opened. The 2013 NORTHCOM denial letter was opened in full and is the strongest item here.
The 2023 Space Force denial was **not** opened as a letter, only as The Black Vault's
account of it. And the proposition the candidate row rests on, that DSP is the system that
detects fastwalkers, is not stated by any government document opened in this pass.

### What was opened

| URL | What is at it |
|---|---|
| https://documents.theblackvault.com/documents/ufos/fastwalkers/FY14-19NOV2013-07.pdf | The USNORTHCOM FOIA response letter, HQ USNORTHCOM/CS, 250 Vandenberg Street, Peterson Air Force Base, case FY14-19NOV2013-07, on a request dated 19 November 2013. It has a text layer and was read in full. |
| https://www.theblackvault.com/documentarchive/fastwalkers-slowwalkers/ | The Black Vault's "Fastwalkers & Slowwalkers" archive page, John Greenewald, 3 March 2015, which hosts the letter above and gives its response date as 6 December 2013. |
| https://www.theblackvault.com/documentarchive/space-force-says-documents-on-fastwalkers-and-slowwalkers-all-exempt-from-disclosure/ | Greenewald's article of 22 December 2023 on the Space Force denial, describing a request filed July 2023 and a response dated 19 December 2023 withholding everything under FOIA Exemption 1 and section 1.1(a) of Executive Order 13526. |
| https://www.govinfo.gov/content/pkg/GAOREPORTS-GAO-03-825R/html/GAOREPORTS-GAO-03-825R.htm | GAO-03-825R, "Military Space Operations: Common Problems and Their Effects on Satellite and Related Acquisitions", 2 June 2003. |
| https://www.govinfo.gov/content/pkg/GAOREPORTS-NSIAD-94-253/html/GAOREPORTS-NSIAD-94-253.htm | GAO/NSIAD-94-253, "National Space Issues: Observations on Defense Space Programs and Activities", 16 August 1994. Thin on DSP; used only to confirm the replacement-programme history. |

The Air Force and Space Force DSP fact sheets could not be opened: `spaceforce.mil`,
`losangeles.spaceforce.mil`, `buckley.spaceforce.mil` and `nationalmuseum.af.mil` all
return 403, `afspc.af.mil` fails at TLS and `au.af.mil` does not resolve. Any first-launch
date of 6 November 1970 belongs to those fact sheets and is **NOT OPENED**; GAO's dates
are used instead.

### What the record establishes

GAO-03-825R describes DSP as "a strategic surveillance and warning satellite system with
an infrared capability to detect ballistic missile launches", says the programme commenced
in 1967 with the first operational satellite deployed in 1971 and the most recent launch in
August 2001, that it "provides near real-time detection information in support of DOD's
integrated tactical warning and attack assessment (ITW/AA) mission", and that "The
SBIRS-High program is focused on replacing DSP" after the earlier AWS, FEWS and ALARM
replacement attempts failed.

The NORTHCOM letter is the record for the denial, and its two operative sentences are
worth separating. On the documents: "After performing a search of our systems of records
we found two responsive USNORTHCOM documents. Upon review of the responsive documents we
have determined that they are currently and properly classified in accordance with
Executive Order 13526, section 1.4c and should remain exempt from public disclosure under
the FOIA exemption (b)(1)." On NORAD, which is the sentence nobody quotes: "Additionally,
NORAD is exempt from FOIA requests as a bi-national organization; therefore no search was
conducted for responsive NORAD documents." The request as restated in the letter asked for
"all Air Force Regulations, procedures, and manuals, either present or past, that reference
'Fastwalkers' and/or 'Slowwalkers'", clarified to NORAD and USNORTHCOM regulations.

### What the transcripts and the candidate row claimed that the record does NOT establish

| Claim | Where | Status |
|---|---|---|
| DSP is "the system that detects fast walkers" | corpus 16 file 4, 2:27:49; corpus 24 file 03, 1:12:46 | NOT ESTABLISHED by any government document opened here. The definition on The Black Vault's page, that a fastwalker is an object "sometimes captured on the Defense Support Program satellite system", is that site's own gloss and carries no citation. The board's own `afit-townsend-2008` node quotes the thesis saying Osedacz used "data from obtained ballistic missile early warning satellites in GEO", which describes DSP without naming it. Carry the association at T2 with the wording attributed, never at T1. |
| Space Force "confirmed records exist but declined to discuss them" | corpus 18 file 4, 0:45:32 | PARTLY. The confirmation-and-refusal shape is right for the 2013 NORTHCOM letter, which was opened. For the 2023 Space Force response only Greenewald's account was opened, so the wording of that letter is T2 at best. |
| The Podesta email describing fastwalkers moving through "our outer layer of defense, the defense support network" | corpus 02 file 02, 17;33; corpus 18 file 4, 0:44:40; corpus 23 file 04, 0:18:53 | NOT OPENED. Every account routes it through WikiLeaks and the Wayback Machine, and `web.archive.org` is unreachable from this environment entirely. The sender is rendered "Bob Fish" and is unresolved in the corpus. Do not put this on the board from this pass. |
| Lee Graham and Ron Regehr reviewed 1976/77 DSP printouts corroborating the Tehran incident | corpus 24 file 03, 1:17:20 to 1:18:16 | NOT OPENED. No printout, no request, no case number given by the speaker. |

### Draft node

```json
{
  "id": "defense-support-program",
  "cls": "program",
  "label": "Defense Support Program (DSP) missile early warning satellites",
  "cluster": "programs",
  "sub": "USAF and later US Space Force strategic surveillance constellation; programme commenced 1967, first operational satellite 1971",
  "tier": "C",
  "dateStart": "1967",
  "dateEnd": null,
  "desc": "The infrared early-warning constellation that the board's fastwalker material comes off, and which the board did not carry. GAO describes DSP as a strategic surveillance and warning satellite system with an infrared capability to detect ballistic missile launches, feeding the integrated tactical warning and attack assessment mission, begun in 1967 with the first operational satellite in 1971 and now being replaced by SBIRS-High. Its place here is documentary rather than anomalous: the board already carries the AFIT thesis that defines 'fastwalker' as ordinary space-surveillance vocabulary and cites a 1972-onward observation database drawn from ballistic missile early warning satellites in geosynchronous orbit, which is this constellation. What the popular literature adds, that DSP is the system that sees UFOs, is not stated by any government document opened for this node.",
  "claims": [
    {
      "tier": 1,
      "text": "GAO's description of the system and its dates: DSP is 'a strategic surveillance and warning satellite system with an infrared capability to detect ballistic missile launches', the programme commenced in 1967, the first operational satellite was deployed in 1971, the most recent launch was August 2001, and it 'provides near real-time detection information in support of DOD's integrated tactical warning and attack assessment (ITW/AA) mission'.",
      "source": "GAO-03-825R, Military Space Operations, 2 June 2003, govinfo"
    },
    {
      "tier": 1,
      "text": "Replacement history: 'The SBIRS-High program is focused on replacing DSP', after the earlier Advanced Warning System, Follow-On Early Warning System and Alert, Locate, and Report Missiles programmes were abandoned as too expensive or technologically immature.",
      "source": "GAO-03-825R, Military Space Operations, 2 June 2003, and GAO/NSIAD-94-253, 16 August 1994, govinfo"
    },
    {
      "tier": 1,
      "text": "A named command confirmed responsive records on the designation and withheld all of them: 'After performing a search of our systems of records we found two responsive USNORTHCOM documents. Upon review of the responsive documents we have determined that they are currently and properly classified in accordance with Executive Order 13526, section 1.4c and should remain exempt from public disclosure under the FOIA exemption (b)(1).'",
      "source": "USNORTHCOM FOIA response, case FY14-19NOV2013-07, on a request of 19 November 2013, The Black Vault"
    },
    {
      "tier": 1,
      "text": "The same letter refuses to search a second command's holdings on structural grounds: 'Additionally, NORAD is exempt from FOIA requests as a bi-national organization; therefore no search was conducted for responsive NORAD documents.'",
      "source": "USNORTHCOM FOIA response, case FY14-19NOV2013-07, The Black Vault"
    },
    {
      "tier": 2,
      "text": "The Black Vault reports that the US Space Force, responding on 19 December 2023 to a July 2023 request for all procedures and manuals referencing 'Fastwalkers' and 'Slowwalkers', withheld the material in full under FOIA Exemption 1 and section 1.1(a) of Executive Order 13526. The response letter itself was not opened for this record.",
      "source": "John Greenewald, 'Space Force Says Documents on \"Fastwalkers\" and \"Slowwalkers\" All \"Exempt from Disclosure\"', The Black Vault, 22 December 2023"
    }
  ],
  "sources": [
    {"name": "GAO-03-825R, Military Space Operations: Common Problems and Their Effects on Satellite and Related Acquisitions", "url": "https://www.govinfo.gov/content/pkg/GAOREPORTS-GAO-03-825R/html/GAOREPORTS-GAO-03-825R.htm", "date": "2003-06-02"},
    {"name": "GAO/NSIAD-94-253, National Space Issues: Observations on Defense Space Programs and Activities", "url": "https://www.govinfo.gov/content/pkg/GAOREPORTS-NSIAD-94-253/html/GAOREPORTS-NSIAD-94-253.htm", "date": "1994-08-16"},
    {"name": "USNORTHCOM FOIA response letter, case FY14-19NOV2013-07", "url": "https://documents.theblackvault.com/documents/ufos/fastwalkers/FY14-19NOV2013-07.pdf", "date": "2013-12-06"},
    {"name": "Fastwalkers & Slowwalkers, The Black Vault", "url": "https://www.theblackvault.com/documentarchive/fastwalkers-slowwalkers/", "date": "2015-03-03"},
    {"name": "Space Force Says Documents on Fastwalkers and Slowwalkers All Exempt from Disclosure, The Black Vault", "url": "https://www.theblackvault.com/documentarchive/space-force-says-documents-on-fastwalkers-and-slowwalkers-all-exempt-from-disclosure/", "date": "2023-12-22"}
  ],
  "edges": [
    {"a": "defense-support-program", "b": "afit-townsend-2008", "type": "research", "claimTier": 2, "note": "The thesis's cited Osedacz database is drawn from ballistic missile early warning satellites in geosynchronous orbit, which is what DSP is; the thesis does not name DSP, so the identification is attributed and not asserted."},
    {"a": "defense-support-program", "b": "norad-northcom", "type": "denial", "claimTier": 1, "note": "USNORTHCOM located two responsive documents on the fastwalker designation and withheld both, and declined to search NORAD's holdings on the ground that NORAD sits outside FOIA."},
    {"a": "defense-support-program", "b": "the-black-vault", "type": "investigative", "claimTier": 1, "note": "Both refusals on this designation, 2013 and 2023, were extracted by The Black Vault and are public only because of it."},
    {"a": "defense-support-program", "b": "eo-13526", "type": "legislative", "claimTier": 1, "note": "Both refusals rest on the same executive order, cited at section 1.4c in 2013 and at section 1.1(a) in 2023."},
    {"a": "defense-support-program", "b": "usaf", "type": "institutional", "claimTier": 1, "note": "DSP is described by GAO as a Department of Defense strategic surveillance system flown by the Air Force before the constellation passed to the Space Force."}
  ]
}
```

---

## 10. Bobby Ray Inman

**VERDICT: CONFIRMED** on the career and on the SAIC relationship, at primary-document
level. **The transcript's claim that he headed SAIC is CONTRADICTED** by SAIC's own proxy
statement. The three anecdotal claims attached to him in the corpus are NOT OPENED.

### What was opened

| URL | What is at it |
|---|---|
| https://www.intelligence.senate.gov/wp-content/uploads/2024/08/sites-default-files-hearings-97inman.pdf | "NOMINATION OF ADMIRAL B.R. INMAN, HEARING BEFORE THE SELECT COMMITTEE ON INTELLIGENCE OF THE UNITED STATES SENATE, NINETY-SEVENTH CONGRESS, FIRST SESSION ON NOMINATION OF ADMIRAL B. R. INMAN TO BE DEPUTY DIRECTOR OF CENTRAL INTELLIGENCE, FEBRUARY 3, 1981", GPO print 74-227 O. Read from the text layer. |
| https://www.sec.gov/Archives/edgar/data/353394/000104746903019902/a2110788zdef14a.htm | Science Applications International Corporation definitive proxy statement, EDGAR accession 0001047469-03-019902, filed 28 May 2003, CIK 0000353394. |
| https://www.sec.gov/Archives/edgar/data/353394/000108287503000004/inm259.htm | SEC Form 4 for INMAN, BOBBY R, statement for 10 April 2003, issuer Science Applications International Corporation, relationship box "Director" checked. |

### What the record establishes

Inman set out his own career on the record in 1981: "Subsequent assignments included
service as the fleet intelligence officer on the staff of the commander, 7th Fleet;
attendance at the National War College; executive assistant and senior aide to the Vice
Chief of Naval Operations; assistant chief of staff for intelligence to the commander in
chief, U.S. Pacific Fleet; Director of Naval Intelligence; and Vice Director for Plans,
Operations, and Support of the Defense Intelligence Agency." He dates the NSA post
himself: "since July 5, 1977, I have had the pleasure of serving as Director, National
Security Agency." The hearing was held on 3 February 1981 on his nomination to be Deputy
Director of Central Intelligence.

SAIC's own proxy is the record for the corporate half. It gives "B.R. Inman, age 72,
Director, Director since 1982", and states that he "joined the Company in 1990 as a
part-time employee and, in that capacity, advises the Company on a wide variety of
strategic planning issues"; that he was Chairman, President and CEO of Westmark Systems
from 1986 through 1989 and of Microelectronics and Computer Technology Corporation from
1983 to 1986; that he retired from the Navy in 1982; and that his government service
included "Director of the National Security Agency and Deputy Director of Central
Intelligence". The same document names him Chairperson of SAIC's Executive Committee, a
member of its Nominating Committee, and records that in fiscal 2003 he received $132,129
under the part-time employee arrangement, plus the use of an office and administrative
support valued at $916. It also lists his other boards: Fluor, Massey Energy, SBC
Communications and Temple-Inland.

The person who actually headed SAIC in that document is J.R. Beyster, "Chairman of the
Board, Chief Executive Officer and President", a director since 1969.

### What the transcripts claimed that the record does NOT establish

| Claim | Where | Status |
|---|---|---|
| "Bobby Ray Inman is named as having headed it [SAIC]" | corpus 12 file 3, 0:19:28 | CONTRADICTED. Director since 1982 and part-time employee since 1990; Beyster was Chairman, CEO and President. He did chair SAIC's Executive Committee, which is the nearest true thing and is not the same claim. |
| Inman spoke about UFOs with the researcher Bob Oechsler on a recorded call | corpus 14 file 4, 2:06:09; corpus 07 file 04 | NOT OPENED. No recording, no transcript, no date. The corpus itself renders the researcher's name three different ways. |
| Inman, cold-called by Greg Milazzi, denied knowledge of Andrija Puharich or Bob Beck | corpus 21 file 02 | NOT OPENED. This is a documentary-maker's account of his own phone call. It is the shape of denial the board grades, but there is no artefact to grade. |
| Inman refers on video to a National Underwater Reconnaissance Office | corpus 25 file 03, 1:18:07 to 1:19:55, per Tim Gallaudet | NOT OPENED. Triage row 5.A9 already says the recording "must be located, not assumed". It was not located in this pass. |
| SAIC "moved into psychotronic research and psychotronic weaponry" tied to SDI funding | corpus 14 file 4, 2:06:09 | NOT ESTABLISHED here. The board's existing `saic` node already carries the documented remote-viewing line from SRI in 1991; the SDI framing is the speaker's. |

### Draft node

```json
{
  "id": "bobby-ray-inman",
  "cls": "person",
  "label": "Adm. Bobby Ray Inman, USN (Ret.)",
  "cluster": "other",
  "sub": "Director, National Security Agency 1977-1981; Deputy Director of Central Intelligence 1981-1982; Director of SAIC from 1982",
  "tier": "B",
  "date": "1981-02-03",
  "desc": "The documented officeholder who joins three institutions the board already carries and nothing currently connects through a person: NSA, CIA and SAIC. He told the Senate Select Committee on Intelligence on 3 February 1981 that he had been Director of Naval Intelligence, Vice Director for Plans, Operations and Support of the Defense Intelligence Agency, and Director of the National Security Agency since 5 July 1977, and he was there to be confirmed as Deputy Director of Central Intelligence. He joined SAIC's board in 1982, the year he retired from the Navy, and from 1990 was also a paid part-time employee of the company advising it on strategic planning while chairing its Executive Committee. He is on the board for the career, which is a single traceable line from signals intelligence to the deputy directorship of the CIA to the boardroom of the government's most sensitive technical services house. He is not on it for the anecdotes attached to him in the podcast corpus, none of which produced an artefact.",
  "claims": [
    {
      "tier": 1,
      "text": "He gave his own career to the Senate: 'Subsequent assignments included service as the fleet intelligence officer on the staff of the commander, 7th Fleet; attendance at the National War College; executive assistant and senior aide to the Vice Chief of Naval Operations; assistant chief of staff for intelligence to the commander in chief, U.S. Pacific Fleet; Director of Naval Intelligence; and Vice Director for Plans, Operations, and Support of the Defense Intelligence Agency.'",
      "source": "Nomination of Admiral B.R. Inman, hearing before the Senate Select Committee on Intelligence, 97th Congress 1st session, 3 February 1981, GPO print 74-227 O"
    },
    {
      "tier": 1,
      "text": "He dates the NSA directorship himself and states the nomination: 'since July 5, 1977, I have had the pleasure of serving as Director, National Security Agency', and 'I have been nominated by the President to serve as the Deputy Director of Central Intelligence.'",
      "source": "Nomination of Admiral B.R. Inman, Senate Select Committee on Intelligence, 3 February 1981"
    },
    {
      "tier": 1,
      "text": "SAIC's own proxy records the relationship: 'B.R. Inman, age 72, Director, Director since 1982. Admiral Inman, USN (Ret.) joined the Company in 1990 as a part-time employee and, in that capacity, advises the Company on a wide variety of strategic planning issues.' He is listed as Chairperson of the Executive Committee and a member of the Nominating Committee, and received $132,129 of compensation under the part-time employee arrangement in fiscal 2003.",
      "source": "Science Applications International Corporation, DEF 14A filed 28 May 2003, SEC EDGAR accession 0001047469-03-019902"
    },
    {
      "tier": 1,
      "text": "He did not head SAIC. The same proxy names 'J.R. Beyster, age 78, Chairman of the Board, Chief Executive Officer and President, Director since 1969' and records that Beyster 'founded the Company in 1969 and has served as Chairman of the Board and Chief Executive Officer since that time'.",
      "source": "Science Applications International Corporation, DEF 14A filed 28 May 2003, SEC EDGAR accession 0001047469-03-019902"
    },
    {
      "tier": 1,
      "text": "The directorship is independently on file as a Section 16 insider report: SEC Form 4 for INMAN, BOBBY R, statement for 10 April 2003, issuer Science Applications International Corporation, with the 'Director' box checked and 'Form filed by One Reporting Person'.",
      "source": "SEC Form 4, EDGAR accession 0001082875-03-000004, filed 14 April 2003"
    }
  ],
  "sources": [
    {"name": "Nomination of Admiral B.R. Inman to be Deputy Director of Central Intelligence, Senate Select Committee on Intelligence, 3 February 1981", "url": "https://www.intelligence.senate.gov/wp-content/uploads/2024/08/sites-default-files-hearings-97inman.pdf", "date": "1981-02-03"},
    {"name": "Science Applications International Corporation definitive proxy statement (DEF 14A), 28 May 2003", "url": "https://www.sec.gov/Archives/edgar/data/353394/000104746903019902/a2110788zdef14a.htm", "date": "2003-05-28"},
    {"name": "SEC Form 4, Bobby R. Inman, Science Applications International Corporation, 10 April 2003", "url": "https://www.sec.gov/Archives/edgar/data/353394/000108287503000004/inm259.htm", "date": "2003-04-14"}
  ],
  "edges": [
    {"a": "bobby-ray-inman", "b": "nsa", "type": "institutional", "claimTier": 1, "note": "Director of the National Security Agency from 5 July 1977, stated by him under oath at his 1981 confirmation hearing."},
    {"a": "bobby-ray-inman", "b": "cia", "type": "institutional", "claimTier": 1, "note": "Nominated and heard on 3 February 1981 to be Deputy Director of Central Intelligence, the post SAIC's own proxy later lists among his government service."},
    {"a": "bobby-ray-inman", "b": "saic", "type": "institutional", "claimTier": 1, "note": "Director of SAIC since 1982 and a paid part-time employee advising on strategic planning since 1990, per the company's 2003 proxy statement."},
    {"a": "bobby-ray-inman", "b": "dia", "type": "institutional", "claimTier": 1, "note": "Vice Director for Plans, Operations and Support of the Defense Intelligence Agency before the NSA directorship, in his own testimony."}
  ]
}
```

---

## What a next session should not undo

1. **The Act is the Invention Secrecy Act of 1951 and it was approved on 1 February 1952.**
   Both halves of that sentence are on the opened Statutes at Large page and both look
   wrong on their own. `CLAUDE.md` section 2 records that two previous passes "corrected" a
   statutory citation that was already right; this is the same trap facing the other way.
   Do not "fix" the 1951 to 1952 and do not "fix" the 1952 approval date to 1951.
2. **The PRP node must be dated and worded to the 1993 directive.** The current manual was
   not reachable. A later session with access to `esd.whs.mil` should re-open DoDM 5210.42
   and DoDI 5210.42 and say what changed, including whether the programme is now called
   Personnel Reliability Assurance.
3. **DSP and "fastwalker" are associated, not equated, in anything opened here.** The
   equation comes from The Black Vault's own definition line. The board's existing
   `afit-townsend-2008` node is deliberately careful about exactly this, and a DSP node
   that is less careful would undo that work.
4. **Inman chaired SAIC's Executive Committee; he did not run SAIC.** The near-miss is the
   thing that will get restated as "headed SAIC" by the next pass that reads a summary
   instead of the proxy.

## Open items this pass could not close

| Item | What is needed |
|---|---|
| The NRO's declassified DORIAN collection, over 850 documents | `nro.gov` returns 403 from here. Either a session on a different network or a mirror. The NRO volume names the compendium: Outzen, J. D., ed. (2015), *The Dorian Files Revealed: A Compendium of the NRO's Manned Orbiting Laboratory Documents*, CSNR. |
| The Space Force FOIA response letter of 19 December 2023 | The Black Vault article embeds it but the page exposes no PDF link. Until the letter is opened, that denial stays T2. |
| DoDM 5210.42 and AFI 91-115 | `esd.whs.mil` and `static.e-publishing.af.mil` both 403. |
| The Podesta "fastwalkers" email | Routed through the Wayback Machine in every account, and `web.archive.org` is unreachable from this environment. |
| Osedacz 1989, the fastwalker database thesis | Already named as the next document to obtain on the `afit-townsend-2008` node; nothing in this pass moved it. |
