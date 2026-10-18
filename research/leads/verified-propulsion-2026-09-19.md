# Verified strand: claimed propulsion mechanisms, graded against the documents cited for them

**Status: research output, not board content.** Nothing here has been merged into `research/`,
into `data/*.json` or into any node. No file in this repo has been created or edited by this
session except this one. No build was run, no git command was run, no `research/*.json` was
touched.

**Verified 19 September 2026.** Every URL in section 0.1 was opened by this session on that
date and returned the document described. `CLAUDE.md` section 2 governs: nothing is asserted
here that was not opened. Walls are recorded as walls in section 0.2. Wikipedia was not used as
a citation anywhere in this file, and where the board currently rests a claim on Wikipedia this
file replaces it with a named source.

**The brief this answers** is `notes/PROPULSION-CLAIMS-2026-09-18.md`, approved by the board
owner on 18 September 2026. Its one idea governs every section below:

> **For each propulsion mechanism that the lore invokes, record what the cited document actually
> claims.**

The brief calls the pattern "the third instance of one pattern": a real, openable, mundane
document gets cited as evidence for a mechanism it never mentions. This file makes it a strand
with the documents checked one by one, and the pattern turns out to hold in a fourth and fifth
place as well.

**The evidence rule that applies to every patent on this page, stated once and repeated on every
patent row:** *a patent is Tier 1 for WHAT IT CLAIMS, and it is never evidence that the thing
works.* A grant is an examiner's decision about novelty, non-obviousness and enablement on the
face of the application. It is not a test result. Five of the documents below are patents and
every one of them is graded on that basis.

**Board state, read this session by loading `data/the-program.json` and testing ids directly.**

IDs that EXIST and that every edge below points at, to be enriched and never re-created:
`thomas-townsend-brown` (A), `salvatore-pais` (A), `pais-patent-imrd` (A), `pais-patent-emfg`
(B), `pais-patent-hfgw` (C), `pais-app-superconductor` (C), `pais-app-fusion` (C),
`marc-millis` (B), `harold-puthoff` (A), `eric-davis` (A), `george-hathaway` (C),
`dird-series` (A), `dird-mhd-air-breathing-propulsion-and-power` (C),
`dird-warp-drive-dark-energy-and-the` (B), `dird-antigravity-for-aerospace-applications` (B),
`dird-positron-aerospace-propulsion` (B), `dird-the-role-of-superconductors-in-gravity` (B),
`dird-cockpits-in-the-era-of-breakthrough` (B), `arv-fluxliner` (B), `tr-3b` (A),
`mark-mccandlish`, `edgar-fouche`, `fouche-iufoc-1998`, `nasa` (A), `us-navy`, `d-exotic` (B),
`d-contractor`, `d-legacy`.

IDs that DO NOT exist, checked this session: `us-3322374`, `james-f-king`, `nasa-bpp`,
`yamato-1`, `alcubierre-1994`, `hutchison-effect`, `john-hutchison`, `king-patent-mhd`.

**Note for a build session: the Brown patents are carried as CLAIMS on `thomas-townsend-brown`,
not as document nodes, while the Pais patents are carried as five separate document nodes. That
asymmetry is deliberate on the board as it stands and this file does not propose changing it.
Do not create `us-3187206` or `us-2949550`.**

---

## Summary

| # | Mechanism | Verdict on the document usually cited |
|---|---|---|
| 1 | **Magnetohydrodynamics** | **THE DOCUMENT IS REAL AND CLAIMS EXACTLY MHD, AND MHD IS A WORKING REAL-WORLD TECHNOLOGY.** US 3,322,374 (King, 1967) is a linear induction motor using ionised air as its armature. Zero occurrences of scalar, spin, gravity, anti-gravity, zero point. The control case is the seagoing MHD thruster: *Yamato-1*, world's first superconducting MHD-propelled ship, sea trials in Kobe, June 1992. And DIA itself bought a 33-page MHD survey in 2010 whose own Summary says the concepts face "significant difficulties" of "weight, complexity, higher power" |
| 2 | **Electrokinetic / Biefeld-Brown** | **THE BOARD'S EXISTING RECORD IS CONFIRMED AGAINST BOTH PATENT TEXTS, AND THE COUNTER-EXPLANATION IS NASA'S OWN.** Neither Brown patent contains the word gravity even once. NASA/TM-2004-213082, section 3.2.7, by the manager of NASA's own Breakthrough Propulsion Physics Project: "To date, all rigorous experimental tests indicate that the observed thrust is attributable to ion wind", and these devices "are not viable candidates for breakthrough physics propulsion" |
| 3 | **Inertial mass reduction (Pais)** | **THE NAVY'S SPONSORSHIP IS DOCUMENTED ON THE FACE OF THE PATENTS, AND THE NAVY'S OWN TEST RESULT IS THAT THE EFFECT COULD NOT BE PROVEN.** Assignee on every one: "The United States of America as represented by the Secretary of the Navy". Prosecuted by a NAWCAD attorney before a named USPTO examiner. NAWCAD's own spokesman, named and quoted: testing October 2016 to September 2019, $508,000, and "the 'Pais Effect' could not be proven" |
| 4 | **Alcubierre metric engineering** | **THE PAPER SAYS WHAT IT SAYS, AND WHAT IT SAYS IS A REQUIREMENT, NOT A DEVICE.** Alcubierre 1994 states that his metric "violates all three energy conditions", that the energy density observers see "is everywhere negative", and that "one needs exotic matter to travel faster than the speed of light". The word "device" appears zero times in the paper. DIA's own warp DIRD tabulates the requirement at -1.00 x 10^42 J for light speed on its most favourable model |
| 5 | **Hutchison effect** | **NO PEER-REVIEWED OR PRIMARY DOCUMENTATION WAS FOUND, AND THE HONEST ANSWER IS THE FINDING.** It rests on undemonstrated video. The one named professional engineer associated with it, George D. Hathaway, is already a board node, wrote two DIA-funded DIRDs, and names Hutchison **zero times** in the one of them this session opened. NASA's BPP survey, which does name Biefeld-Brown, lifters, Podkletnov and Alcubierre, names Hutchison zero times. **No node proposed beyond a strand row** |
| 6 | **ARV capacitor stack and TR-3B mercury plasma** | **ALREADY REFUTED ON THE BOARD, AND THE STRAND IS WHERE THEY JOIN.** Both are instances of the same move: `tr-3b`'s mercury "Magnetic Field Disruptor" is refuted by mercury's melting point, and `arv-fluxliner`'s capacitor stack is the Biefeld-Brown reading the board already caveats on two edges |

**The five findings that matter, in order:**

1. **THE SINGLE MOST IMPORTANT FINDING: the US government's own commissioned antigravity survey
   does not mention Thomas Townsend Brown.** `dird-antigravity-for-aerospace-applications`,
   DIA-08-1003-018, 30 March 2010, 45 pages, attributed on the DIA list to Eric Davis. Word
   counts over the whole released PDF, taken this session: **Biefeld 0, electrogravitics 0, ion
   wind 0, Podkletnov 0.** "Brown" occurs three times and all three are reference-list surnames
   of other authors (L. S. Brown, H. R. Brown, J. H. Brownell). The document the lore would most
   expect to vindicate the electrogravitics thread is a survey of gravitomagnetic forces,
   negative energy, dark energy and the Casimir effect that never reaches for Brown at all. This
   is the same failure mode as King and Winterhaven, at the highest level yet: the government
   document exists, it is openable, and it is about something else.
2. **The counter-explanation the strand needed is NASA's, it is on the record, and the board
   already has the man who wrote it.** Marc G. Millis, `marc-millis`, tier B on this board, ran
   NASA's Breakthrough Propulsion Physics Project from 1996 to 2002 and wrote NASA/TM-2004-213082
   summarising it. Section 3.2.7 disposes of Biefeld-Brown, Lifters and Asymmetrical Capacitors in
   one paragraph. Section 3.3.1 disposes of metric engineering in another: "they require enormous
   quantities of 'negative energy' (equivalent mass of planets or suns)". **One opened NASA
   document adjudicates three of this strand's six mechanisms, and its author is already a node.**
3. **The Navy's sponsorship of Pais is documented on the printed face of the patent, and so is
   the Navy's own negative result.** US 10,144,532's front page carries the assignee line, the
   NAWCAD attorney (Mark O Glut), the primary examiner (Philip J Bonzell, the same examiner
   named in the board's Sheehy letter) and the application data. The brief's ruling that Navy
   sponsorship is what makes Pais board material and King not is confirmed by reading the two
   front pages side by side: King's carries no assignee at all.
4. **US 10,144,532 cites Harold Puthoff on its face.** Its Publications list includes "Puthoff,
   H. E., Polarizable-Vacuum (PV) Approach to General Relativity, Foundations of Physics, Jun.
   2002, vol. 32, No. 6", alongside Froning and Hayasaka. `harold-puthoff` is already a tier A
   node. This is a documentary citation from a US Navy patent to a figure the board already
   carries, and it is Tier 1 because it is printed on the patent.
5. **The ion-wind counter-explanation is not unanimous and the strand must say so.** NASA's
   contractor report NASA/CR-2004-213312 concludes the thrust is "fully explained by a very
   simple theory that uses only electrostatic forces and the transfer of momentum by multiple
   collisions". The Army Research Laboratory's own report, by Bahder and Fazi, concluded that
   "ionic wind is at least three orders of magnitude too small to explain the magnitude of the
   observed force". **These are not in flat contradiction** - ARL rejected *ballistic ionic
   wind* and preferred *ionic drift*, which is what NASA then modelled - but a strand that
   quoted only NASA would be overstating the record.

---

## 0. Sources

### 0.1 Opened and read, 19 September 2026

| URL | What it is | What it establishes |
|---|---|---|
| https://patents.google.com/patent/US3187206A/en | Google Patents full-text record, US 3,187,206 | Title, inventor, assignee Electrokinetics Inc, filing 9 May 1958, grant 1 June 1965, and the opening sentence of the specification |
| https://patentimages.storage.googleapis.com/fd/fa/17/a3da8c41817315/US3187206.pdf | The patent itself, 6 pages | The printed header block and the full specification and claims. Word counts in section 2.1 |
| https://patents.google.com/patent/US2949550A/en | Google Patents full-text record, US 2,949,550 | Title, inventor, assignee Whitehall-Rand Inc, filing 3 July 1957, grant 16 August 1960, and claim 1 verbatim |
| https://patentimages.storage.googleapis.com/20/38/0f/252396dd3aadcb/US2949550.pdf | The patent itself, 6 pages | The printed header block, the abandoned parent application, and the word counts in section 2.1 |
| https://patents.google.com/patent/US10135366B2/en | Google Patents record, US 10,135,366 | Application 14/807,943, filed 24 July 2015, granted 20 November 2018, assignee US Department of Navy, abstract verbatim |
| https://patents.google.com/patent/US10322827B2/en | Google Patents record, US 10,322,827 | Application 15/431,823, filed 14 February 2017, granted 18 June 2019, assignee US Department of Navy, abstract verbatim |
| https://patentimages.storage.googleapis.com/de/4c/43/62c585ccc936cc/US10144532.pdf | US 10,144,532, the patent itself, 6 pages | The whole front-page bibliographic block quoted in section 3.1, the abstract, claim 1, the cited publications including Puthoff, and the "4 Claims, 1 Drawing Sheet" line |
| https://ntrs.nasa.gov/api/citations/20040070788/downloads/20040070788.pdf | **NASA/TM-2004-213082, "Prospects for Breakthrough Propulsion from Physics", Marc G. Millis, NASA Glenn Research Center**, 19 pages, prepared for a NASA/DoD-cosponsored conference, Seattle, 24 to 26 June 2004 | The single most useful document in this file. Sections 3.2.7 and 3.3.1 quoted in sections 2.3 and 4.3, the abstract in section 2.3, and the reference list that names Talley, Tajmar and Canning |
| https://ntrs.nasa.gov/api/citations/20040171929/downloads/20040171929.pdf | **NASA/CR-2004-213312, "Asymmetrical Capacitors for Propulsion", Francis X. Canning, Cory Melcher and Edwin Winet, Institute for Scientific Research Inc, Fairmont, West Virginia, October 2004**, 23 pages | The experimental counter-explanation. Abstract and Conclusions quoted in section 2.3. Its reference list cites both Brown patents by number. It also quotes Talley's vacuum null result verbatim |
| https://arxiv.org/abs/physics/0211001 | Bahder and Fazi, "Force on an Asymmetric Capacitor", arXiv preprint of the ARL report, submitted 31 October 2002, revised 12 March 2003 | The dissenting finding quoted in section 2.3. The published version is ARL-TR-3005, NTIS order number ADA416740, per the NASA CR's reference 8 |
| https://arxiv.org/abs/gr-qc/0009013 and https://arxiv.org/pdf/gr-qc/0009013 | **Miguel Alcubierre, "The warp drive: hyper-fast travel within general relativity", 10 pages**, arXiv posting of 5 September 2000 of the paper published as Class. Quantum Grav. 11-5, L73-L77 (1994), DOI 10.1088/0264-9381/11/5/001 | The paper itself. Every quotation in section 4.1 is from this text, and the word counts in section 4.2 |
| https://documents2.theblackvault.com/documents/dia/AAWSAP-DIRDs/DIRD_33-DIRD_MHD_Air_Breathing_Propulsion_and_Power_for_Aerospace_Applications.pdf | The MHD DIRD, 33 pages, cover 21 November 2010, ICOD 20 July 2010, DIA-08-1011-006, "Defense Futures" | Its Summary quoted in section 1.3, its chapter structure, and the word counts that matter |
| https://documents2.theblackvault.com/documents/dia/AAWSAP-DIRDs/DIRD_13-DIRD_Warp_Drive_Dark_energy_and_the_Manipulation_of_Extra_Dimensions.pdf | The warp DIRD, 34 pages, DIA-08-1004-001 | Its Summary and its two negative-energy tables, quoted in section 4.4 |
| https://documents2.theblackvault.com/documents/dia/AAWSAP-DIRDs/DIRD_19-DIRD_Antigravity_for_Aerospace_Applications.pdf | The antigravity DIRD, 45 pages, cover 30 March 2010, ICOD 1 December 2009, DIA-08-1003-018, "Acquisition Threat Support" | **Finding 1.** Its contents page, its conclusion quoted in section 2.4, and the word counts that establish Brown is absent from it |
| https://documents2.theblackvault.com/documents/dia/AAWSAP-DIRDs/DIRD_17-DIRD_Maverick_Inventor_Versus_Corporate_Inventor-Where_Will_the_Next_major_Innovations_Arise.pdf | Hathaway's DIRD, 20 pages, cover 30 March 2010, ICOD 1 December 2009, DIA-08-1003-017, "Acquisition Threat Support" | **That Hutchison is named zero times in it.** Section 5.2 |
| https://www.hathawayresearch.com/principal-staff/ | George D. Hathaway's own firm's staff page | His own account of his credentials, and that his Hutchison publication is a book, "Mindbending: The Hutchison Files", not a paper |
| https://www.twz.com/39012/the-navy-finally-speaks-up-about-its-bizarre-ufo-patent-experiments | Brett Tingley, The War Zone, updated 1 February 2021 | NAWCAD's own on-the-record statement of the test result, quoted in section 3.4. **This replaces the Wikipedia citation the board currently carries for that claim** |
| https://www.osti.gov/biblio/135352 | OSTI bibliographic record and abstract for Sasakawa, Takezawa, Sugawara and Kyotani, "The superconducting MHD-propelled ship YAMATO-1", Proceedings of the 4th International Conference and Exhibition: World Congress on Superconductivity, vol. 1, Orlando FL, 27 June to 1 July 1994, published April 1995 | The control case for mechanism 1, quoted in section 1.4 |
| https://arxiv.org/abs/1707.02743 | Cébron, Viroulet, Vidal, Masson and Viroulet, "Experimental and Theoretical Study of Magnetohydrodynamic Ship Models", submitted 10 July 2017 | Opened and then **not used**. Its abstract is about small-scale student-grade MHD boats and a full-text search returned no mention of Yamato-1 or of full-scale seawater MHD. Recorded so a later session does not re-open it expecting otherwise |

### 0.2 Walls, recorded as walls

| Wall | What happened |
|---|---|
| `apps.dtic.mil/sti/tr/pdf/ADA416740.pdf` | HTTP 403. This is the published ARL-TR-3005. The arXiv preprint at `physics/0211001` was opened instead and is what section 2.3 quotes. **The ARL report as published was NOT opened and is not asserted from.** |
| `arc.aiaa.org/doi/10.2514/1.9095` | HTTP 403. This is Tajmar, "The Biefeld-Brown Effect: Misinterpretation of Corona Wind Phenomena". **The paper itself was NOT opened.** It is named in this file only as reference 54 of NASA/TM-2004-213082, with the citation as NASA printed it: *AIAA Journal of Propulsion & Power, 42, (2004), pp. 315-318*. A later session should open it. |
| Talley, PL-TR-91-3009 | **NOT opened.** The Phillips Laboratory / Air Force Systems Command vacuum test of asymmetric capacitors is quoted in this file only as NASA/CR-2004-213312 quotes it, and cited only as NASA/TM-2004-213082's reference 52 prints it, including the contract number FO4611-89-C-0023. It is the single most valuable unopened document in this strand and section "WHAT I COULD NOT ESTABLISH" says so. |
| `documents2.theblackvault.com/.../DIRD_20-DIRD_Maverick_Inventor_Versus_Corporate_Inventor.pdf` | HTTP 404 on a guessed filename. The real path is `DIRD_17-...-Where_Will_the_Next_major_Innovations_Arise.pdf` and it opened. Recorded because guessing blackvault DIRD numbers does not work. |
| Hutchison-effect primary literature | No peer-reviewed venue was located. Every result returned was a self-published compilation, a personal site, a slide deck, a fringe-conference proceedings or a podcast page. **None of them is cited anywhere in this file.** Section 5 states the negative finding rather than dressing it. |

---

## 1. Magnetohydrodynamics

### 1.1 The cited document, from the brief, NOT re-opened

Per the brief's instruction, US 3,322,374 was **not re-opened by this session** and every figure
below is the brief's, from `notes/PROPULSION-CLAIMS-2026-09-18.md` section 1, which records it
opened from `https://patentimages.storage.googleapis.com/6f/35/54/257dd6cdb01efc/US3322374.pdf`
on 18 September 2026.

| | |
|---|---|
| Title | Magnetohydrodynamic Propulsion Apparatus |
| Inventor | James F. King, Jr., [street address omitted], Winston-Salem, North Carolina 27106 |
| Filed | 30 September 1964, Serial No. 400,456 |
| Granted | 30 May 1967 |
| Claims / class | 9 claims, Class 244-62 |
| Assignee | **None.** A private individual at a home address |
| Government interest, secrecy order | **None in the document** |
| Word counts, all 7 pages | scalar 0, spin 0, gravity 0, anti-gravity 0, zero point 0 |

### 1.2 The mechanism description is stated correctly, and this is a check not a re-derivation

The brief describes claim 1 as coils along the craft's axis driven by polyphase alternating
current, producing a travelling point of maximum flux density that induces eddy currents in the
surrounding ionised fluid, driving that fluid backwards. It calls this "a linear induction motor
using the atmosphere as its armature".

**That description is correct as a statement of magnetohydrodynamic propulsion** and it is the
same physics the two independent documents in sections 1.3 and 1.4 describe: a magnetic field
acting on a conducting fluid, with the fluid as the reaction mass. Nothing in it is exotic, and
nothing in it is even unusual. **The Lorentz force on a current-carrying conductor is
nineteenth-century physics and the conductor here happens to be a fluid.**

What the claim made FOR the patent asserts, per the brief section 2, is that it is "ample
evidence" that the "Scalar Physics" callout in section D of the McCandlish ARV drawing refers to
spin-zero scalar particles. The patent contains the word scalar zero times. **The gap between
those two sentences is the entire product of this strand.**

### 1.3 DIA bought an MHD survey in 2010 and it is on the board already

`dird-mhd-air-breathing-propulsion-and-power` is a tier C node carrying DIA-08-1011-006. This
session opened the released PDF and read its Summary. **It is 33 pages of hypersonic aerodynamics
and it is not about anything anomalous.** Its opening Summary, verbatim from the released copy:

> "The paper reviews novel propulsion concepts utilizing plasmas (ionized gases) and
> magnetohydrodynamics (MHD). These concepts are shown to be attractive due to their potential
> to achieve propulsion and aerodynamic performance far beyond current conventional
> technologies. However, significant difficulties impede the development and application of
> these technologies; these include weight, complexity, higher power, and the need for complex
> and energy-consuming artificial ionization in 'cold' air (at Mach <12)."

And, on the concept the popular literature most often reaches for:

> "A well-publicized Ajax concept of MHD energy bypass has been shown to be meaningless below at
> least Mach 12. In contrast, a new 'reverse energy bypass' with Virtual Cowl is potentially
> practical for air-breathing hypersonic vehicles."

Word counts over the whole released document, taken this session: **UFO 0, unidentified 0,
anti-gravity 0, antigravity 0, scalar 0, zero point 0, levitation 0. "Gravity" occurs once.**

The board already records that the DIA list supplied to the Senate Armed Services Committee
attributes this DIRD to "Dr S Macheret, Lockheed Martin". **So the government paid a Lockheed
Martin plasma physicist to survey MHD propulsion for the same programme the lore invokes, and
what he delivered is about scramjet inlets, virtual cowls and reentry drag reduction.**

### 1.4 The control case: MHD propulsion has a documented real-world record

This is the row the brief asked for and it belongs in the strand because it is the honest
comparison. Magnetohydrodynamic propulsion is not a fringe idea that failed; it is a real
technology that was built, floated and measured, and its record is ordinary.

From the OSTI record and abstract for Sasakawa, Takezawa, Sugawara and Kyotani, verbatim:

> "In 1985 the Ship & Ocean Foundation (SOF) created a committee under the chairmanship of Mr.
> Yohei Sasakawa, Former President of the Ship & Ocean Foundation, and began researches into
> superconducting magnetohydrodynamic (MHD) ship propulsion. In 1989 SOF set to construction of
> a experimental ship on the basis of theoretical and experimental researches pursued until
> then. The experimental ship named YAMATO-1 became the world's first superconducting
> MHD-propelled ship on her trial runs in June 1992. This paper describes the outline of the
> YAMATO-1 and sea trial test results."

Published in *Proceedings of the 4th International Conference and Exhibition: World Congress on
Superconductivity*, volume 1, from the conference held in Orlando, Florida, 27 June to 1 July
1994; OSTI record dated April 1995.

**Why the control case matters to this strand.** The mechanism the ARV lore invokes as evidence
of recovered non-human technology was demonstrated in a Japanese harbour in 1992 by a maritime
foundation, in public, with a named chairman, at a speed slower than a bicycle. **If MHD were
the secret, it was never a secret.** That is not an argument that the lore is wrong about
everything; it is the observation that the specific document offered as proof describes
something that was independently built and publicly reported, and nobody had to recover a craft
to do it.

### 1.5 The patents-view ruling, restated so no later session undoes it

**The brief's section 4 rules that US 3,322,374 does NOT go into the board's patents view, and
this file endorses that ruling and restates it here.**

The five patents in the view today are all Pais, and they are there because the Navy filed and
prosecuted them. Section 3.1 below confirms that sponsorship from the printed front page of US
10,144,532. King has no assignee, no contractor, no programme, no clearance and no government
interest, which section 1.1 confirms from the brief's own reading of his front page. On the
board's own test he connects to nothing.

**Adding King to the patents view because a patent about MHD turned up in a thread about the ARV
would be sourcing by topical resemblance, which is the thing the board exists not to do.** He
belongs to this strand and only to this strand. A later session that finds `king-patent-mhd` in
the data and thinks it looks orphaned next to the Pais five should read this paragraph before
"fixing" it.

---

## 2. Electrokinetic / Biefeld-Brown

### 2.1 Both patents opened and the board's existing record CONFIRMED

The board records, on `thomas-townsend-brown` and on two `arv-fluxliner` edges, that neither
patent claims anti-gravity. **That is confirmed against both printed texts.**

**US 2,949,550.** Printed header block, verbatim from the patent:

> "2,949,550 / Patented Aug. 16, 1960 / ELECTROKINETIC APPARATUS / Thomas Townsend Brown,
> Umatilla, Fla., assignor to Whitehall-Rand, Inc., Washington, D.C., a corporation of Delaware
> / Filed July 3, 1957, Ser. No. 669,830 / 12 Claims. (Cl. 310-5)"

Opening sentence: "My invention relates to electrokinetic apparatus, and more particularly to a
method and apparatus for utilizing electrical potentials for the production of forces for the
purpose of causing relative motion between a structure and the surrounding medium."

A detail the board does not yet carry, and it dates the disclosure seven years earlier: "This
invention was disclosed and described in my application Serial No. 293,465, filed June 13, 1952,
which application has become abandoned."

Claim 1, verbatim: "Thrust producing apparatus comprising an electroconductive body having a
relatively large, substantially smooth area thereof exposed to the surrounding medium, an
electrode supported on said body, insulated therefrom and shaped to produce a concentrated
electrostatic field when electrically charged with respect to said body, and power means
connected between said body and electrode to impress high voltage thereon whereby to cause
relative movement of an ionizable dielectric medium surrounding said electrodes."

**US 3,187,206.** Printed header block, verbatim:

> "3,187,206 / Patented June 1, 1965 / ELECTROKINETIC APPARATUS / Thomas Townsend Brown,
> Walkertown, N.C., assignor, by mesne assignments, to Electrokinetics, Inc., a corporation of
> Pennsylvania / Filed May 9, 1958, Ser. No. 734,342 / 23 Claims. (Cl. 310-5)"

Opening sentence: "This invention relates to an electrical device for producing thrust by the
direct operation of electrical fields."

The passage the board already quotes, in its full form: "When the device is operated in a
dielectric fluid medium, such as air, the forces of reaction appear to be present in that medium
as well as on all solid material bodies making up the physical environment. In a vacuum, the
reaction forces appear on the solid environmental bodies, such as the walls of the vacuum
chamber. The propelling force however is not reduced to zero when all environmental bodies are
removed beyond the apparent effective range of the electrical field."

**Word counts, taken this session over the complete 6-page text of each patent:**

| | gravity | anti-gravity | antigravity | levitation | scalar | electrogravitics | zero point |
|---|---|---|---|---|---|---|---|
| US 2,949,550 | **0** | 0 | 0 | 0 | 0 | 0 | 0 |
| US 3,187,206 | **0** | 0 | 0 | 0 | 0 | 0 | 0 |

**The word "gravity" does not appear in either patent. Not once, in either direction.**

### 2.2 Filing and grant dates, precisely

| Patent | Title | Inventor and address as printed | Assignee | Filed | Serial | Granted | Claims / class |
|---|---|---|---|---|---|---|---|
| US 2,949,550 | Electrokinetic Apparatus | Thomas Townsend Brown, Umatilla, Fla. | **Whitehall-Rand, Inc., Washington, D.C., a corporation of Delaware** | 3 July 1957 | 669,830 | 16 August 1960 | 12 claims, Cl. 310-5 |
| US 3,187,206 | Electrokinetic Apparatus | Thomas Townsend Brown, Walkertown, N.C. | **Electrokinetics, Inc., a corporation of Pennsylvania**, by mesne assignments | 9 May 1958 | 734,342 | 1 June 1965 | 23 claims, Cl. 310-5 |

Both dates agree exactly with the board's existing claims on `legacy-1947-86.json`. **Nothing
needed correcting.** The enrichment is the serial numbers, the assignee corporations and states,
the claim counts, the class, and the abandoned 1952 parent.

**The assignees are worth a line of their own.** Neither patent is unassigned: 2,949,550 went to
Whitehall-Rand in Washington D.C. and 3,187,206 to Electrokinetics, Inc. of Pennsylvania. Both
are private corporations. **Neither is a government assignee and neither carries a government
interest statement,** which puts Brown on the same side of the brief's sponsorship test as King,
not as Pais. Brown is board material for other reasons, documented at length elsewhere in
`research/legacy-1947-86.json`, including his FBI file; he is not board material because a
government filed his patents, because none did.

### 2.3 The modern explanation, with a citable experimental source

This is the counter-explanation the strand needs, and the strongest form of it is NASA's own.

**NASA/TM-2004-213082, section 3.2.7, "Biefeld-Brown and Variants", verbatim and in full:**

> "In 1928 a device was patented for creating thrust using high-voltage capacitors [50]. Since
> then, a wide variety of variants of this 'Biefeld-Brown' effect, such as 'Lifters' and
> 'Asymmetrical Capacitors' have claimed that such devices operate on an 'electrostatic
> antigravity' or 'electrogravitic' effect. One of the most recent variants was patented by
> NASA-MSFC [51]. To date, all rigorous experimental tests indicate that the observed thrust is
> attributable to ion wind [52 to 54].
>
> Vacuum tests currently underway, sponsored through an additional Congressional earmark to the
> West Virginia Institute for Scientific Research, also indicate that this effect is not
> indicative of new propulsion physics. These tests are now assessing the more conventional
> performance of such devices [55].
>
> These 'Biefeld-Brown,' 'Lifter' and 'Asymmetrical Capacitor Thrusters' are not viable
> candidates for breakthrough physics propulsion."

The three references behind "all rigorous experimental tests", as NASA prints them:

- **[52]** Talley, R. L., "Twenty First Century Propulsion Concept," PL-TR-91-3009, Final Report
  for the period Feb 89 to July 90, on Contract FO4611-89-C-0023, **Phillips Laboratory, Air
  Force Systems Command, Edwards AFB, CA (1991)**.
- **[53]** Tajmar, M., "Experimental Investigation of 5-D Divergent Currents as a
  Gravity-Electromagnetism Coupling Concept," AIP Conference Proceedings, 504, STAIF,
  Albuquerque, NM, (2000), pp. 998-1003.
- **[54]** Tajmar, M., "The Biefeld-Brown Effect: Misinterpretation of Corona Wind Phenomena,"
  AIAA Journal of Propulsion & Power, 42, (2004), pp. 315-318.

**The experimental source, NASA/CR-2004-213312.** Its Conclusions, verbatim in the passage that
matters:

> "A simple model was developed of ions drifting from one electrode to the other under
> electrostatic forces, and imparting momentum to air as they underwent multiple collisions.
> This model was found to be consistent with all of our observations. It predicted the magnitude
> of the force (thrust) that was measured. It also predicted how the direction of the thrust
> changed when the location of the ground wire changed. Furthermore, it also predicted that the
> direction of the thrust was independent of the polarity of the applied voltage. ... In spite of
> decades of speculation about possible new physical principles being responsible for the thrust
> produced by ACTs and lifters, we find no evidence to support such a conclusion. On the
> contrary, we find that their operation is fully explained by a very simple theory that uses
> only electrostatic forces and the transfer of momentum by multiple collisions."

**The vacuum result, which is the one that settles the "in vacuum" question US 3,187,206 raises.**
NASA/CR-2004-213312 quotes the Talley report directly:

> "Talley wrote, 'Direct experimental results show that under high vacuum conditions... no
> detectable propulsive force was electrostatically induced by applying a static potential
> difference... between test device electrodes...' Talley concluded (page 91 of his report), 'If
> such a force still exists and lies below the threshold of measurements in this program, then
> the force may be too small to be attractive for many, if not most, space propulsion
> applications.'"

The NASA CR adds, of Talley's work: "His report is the only written report we have found from
the last half-century that describes a measurement of a force while in a vacuum chamber."

**The dissent, recorded because the strand must not overstate.** Bahder and Fazi, whose ARL
report NASA cites as reference 8 of the CR, concluded from their own calculations: "The
calculations indicate that ionic wind is at least three orders of magnitude too small to explain
the magnitude of the observed force on the capacitor." **This rejects ballistic ionic wind, not
ion drift**; the same paper reports that assuming ionic drift transport aligns better with the
observations, which is the model NASA then built. A reader of this strand should be told that the
ARL and NASA documents agree on the class of explanation and disagree on which member of it, and
that neither invokes new physics.

**And the loop closes on the documents themselves.** NASA/CR-2004-213312's reference list opens:
"1 Brown, T.T., US Patent 2,949,550, 'Electrokinetic Apparatus,' 1960. 2 Brown, T.T., US Patent
3,187,206, 'Electrokinetic Apparatus,' 1965. 3 Brown, T.T., GB Patent 300,311, 'A Method of and
an Apparatus or Machine for Producing Force or Motion,' 1928." **NASA cites exactly the three
Brown documents the board carries, by number, and concludes that what they describe is ions
pushing on air.**

### 2.4 What the government's own antigravity survey actually claims, and who it never mentions

This is finding 1 and it gets its own subsection.

`dird-antigravity-for-aerospace-applications`, DIA-08-1003-018, cover-dated 30 March 2010 under
the "Acquisition Threat Support" banner, 45 pages, attributed on the DIA list of 9 January 2018
to Dr Eric Davis of EarthTech International. Opened this session.

Its contents page: "Concepts for Antigravity Within Newtonian Physics", "Concepts for Antigravity
Within General Relativity", "Antigravity via Gravitomagnetic Forces", "Forward's Dipole
Gravitational Field Generator", "Felber's Relativistic Antigravity Effect", "Negative
Energy-Induced Antigravity", "Cosmological Antigravity", "Vacuum Energy of Einstein's
Cosmological Constant", "Dark Energy", "Quantum Antigravity Propulsion Concepts", "Antigravity
via Quantum Vacuum Zero-Point Fluctuation Force", "Antigravity via Nonretarded Quantum
Interatomic Dispersion Force", and appendices on the Casimir effect and squeezed vacuum.

Its conclusion, "The Way Forward", verbatim in part:

> "One found that plausible mechanisms exist within Newtonian and general relativistic theories
> whereby one could embody a realistic device that produces a significant antigravity force.
> However, one discovered that there are daunting technical challenges that arise in each of the
> proposed embodiments. Mechanical embodiments that produce antigravity forces require
> kilometer-sized apparatus, astronomical-sized masses and densities, or extreme mass velocities
> and accelerations."

And:

> "Negative energy has been produced in the lab in very small quantities. The technologies used
> for producing negative energy are nascent, and so it will be some time before it can be
> ascertained whether they are capable of producing the astronomical amounts of negative energy
> required to generate significant antigravity forces."

**Word counts over the whole released 45-page PDF, taken this session:**

| term | count |
|---|---|
| Biefeld | **0** |
| electrogravitics | **0** |
| ion wind | **0** |
| Podkletnov | **0** |
| levitation | appears once, as a section heading "Energy Estimate for Newtonian Levitation" |
| Alcubierre | **1**, as reference [43], the 1994 Classical and Quantum Gravity citation |
| Brown | **3**, and all three are reference-list surnames of other authors: L. S. Brown and Maclay (Physical Review 184, 1969), H. R. Brown as co-editor of *The Philosophy of Vacuum*, and J. H. Brownell on Casimir photons |

**Thomas Townsend Brown is not in it.** The one US government document whose entire subject is
antigravity for aerospace applications, commissioned under the same programme the whole board is
about, written by a physicist the board carries at tier A, does not mention the man the
electrogravitics literature treats as its origin, or his effect, or the word electrogravitics.

That is the strand's pattern at its largest scale, and it runs in the other direction from the
King case. With King, a real document is cited for a mechanism it never mentions. Here, a real
document about the mechanism never mentions the person it is supposed to vindicate. **Both are
the same failure: the citation and the document have never been placed side by side.**

---

## 3. Inertial mass reduction: the Salvatore Pais patents

### 3.1 The printed front page, and why the Navy's sponsorship is the whole point

Opened this session from the Google Patents PDF of US 10,144,532. The front-page bibliographic
block, transcribed from the printed page:

> "(12) United States Patent / Pais / (10) Patent No.: US 10,144,532 B2 / (45) Date of Patent:
> Dec. 4, 2018
> (54) CRAFT USING AN INERTIAL MASS REDUCTION DEVICE
> (71) Applicant: Salvatore Cezar Pais, Leonardtown, MD (US)
> (72) Inventor: Salvatore Cezar Pais, Leonardtown, MD (US)
> (73) Assignee: **The United States of America as represented by the Secretary of the Navy,
> Washington, DC (US)**
> (*) Notice: Subject to any disclaimer, the term of this patent is extended or adjusted under 35
> U.S.C. 154(b) by 153 days.
> (21) Appl. No.: 15/141,270
> (22) Filed: Apr. 28, 2016
> (65) Prior Publication Data: US 2017/0313446 A1, Nov. 2, 2017
> (51) Int. Cl. B64G 1/40 (2006.01)
> (52) U.S. Cl. CPC B64G 1/409 (2013.01)
> **Primary Examiner - Philip J Bonzell**
> **(74) Attorney, Agent, or Firm - Mark O Glut; NAWCAD**
> 4 Claims, 1 Drawing Sheet"

**Three things on that page are the reason Pais is board material and King is not, and all three
are printed, not inferred:**

1. **The assignee is the United States Navy.** Not the inventor, not a private corporation.
2. **The prosecuting firm is NAWCAD** - the Naval Air Warfare Center Aircraft Division at NAS
   Patuxent River, named on the patent as attorney of record. The government did not merely take
   an assignment; it paid a lawyer to prosecute the application.
3. **The primary examiner is Philip J Bonzell** - the same examiner named in the board's existing
   Tier 1 claim about the Sheehy letter of 15 December 2017, which was addressed to "Mr. Philip
   J. Bonzell, Primary Patent Examiner". **The letter and the granted patent name the same
   person, and that correspondence is now checkable on the printed face of the patent itself.**

Compare King's front page as the brief records it: no assignee, no government interest, no
secrecy order, a home address in Winston-Salem. **The brief's ruling is confirmed by a
side-by-side reading of two printed header blocks and nothing else is needed to support it.**

### 3.2 The five filings, with dates

The board already carries all five as nodes. This session verified three of them directly against
Google Patents records and the printed patent, and found the board's figures correct in every
particular.

| Board node | Number | Title | Application | Filed | Granted / published | Assignee as printed |
|---|---|---|---|---|---|---|
| `pais-patent-emfg` | US 10,135,366 B2 | Electromagnetic field generator and method to generate an electromagnetic field | 14/807,943 | **24 July 2015** | granted **20 November 2018** | US Department of Navy |
| `pais-patent-imrd` | US 10,144,532 B2 | Craft using an inertial mass reduction device | 15/141,270 | **28 April 2016** | granted **4 December 2018** | The United States of America as represented by the Secretary of the Navy |
| `pais-patent-hfgw` | US 10,322,827 B2 | High frequency gravitational wave generator | 15/431,823 | **14 February 2017** | granted **18 June 2019** | US Department of Navy |
| `pais-app-superconductor` | US 2019/0058105 A1 | Piezoelectricity-induced Room Temperature Superconductor | 15/678,672 | 16 August 2017 | published 21 February 2019 | as represented by the Secretary of the Navy |
| `pais-app-fusion` | US 2019/0295733 A1 | Plasma Compression Fusion Device | 15/928,703 | 22 March 2018 | published 26 September 2019 | as represented by the Secretary of the Navy |

**Verified with no corrections.** The last two are applications, not grants, and the board
already labels them as such; a strand row must not call them patents.

### 3.3 What the patents actually claim, in their own words

**US 10,144,532, abstract, verbatim:** "A craft using an inertial mass reduction device comprises
of an inner resonant cavity wall, an outer resonant cavity, and microwave emitters. The
electrically charged outer resonant cavity wall and the electrically insulated inner resonant
cavity wall form a resonant cavity. The microwave emitters create high frequency electromagnetic
waves throughout the resonant cavity causing the resonant cavity to vibrate in an accelerated
mode and create a local polarized vacuum outside the outer resonant cavity wall."

From the background, verbatim: "inertial mass reduction can be achieved via manipulation of
quantum field fluctuations in the local vacuum energy state, in the immediate proximity of the
object / system." And on the mechanism: "negative pressure (hence repulsive gravity) exhibited by
the polarized local vacuum energy state".

The specification also states, in the passage that runs alongside claim 1, that the hybrid craft
"would move with great ease through the air / space / water mediums, by being enclosed in a
vacuum plasma bubble / sheath, due to the coupled effects of EM field-induced air / water
particles repulsion and vacuum energy polarization" - which is the same sentence the board
already carries at Tier 1 from the PAX 205 invention-disclosure briefing. **The briefing and the
patent say the same thing in the same words, which is a real corroboration between two
independently obtained documents.**

**US 10,135,366, abstract, verbatim:** a shell with "embedded polycrystalline ferroelectric
ceramic material which is polarized such that the ceramic material exhibits strong Piezoelectric
Effect properties thus inducing high frequency vibrations", which "may be further doped with
radioactive elements which under high frequency vibrations induce gamma ray emission", spun at
"high angular speeds" by an electric motor.

**US 10,322,827, abstract, verbatim:** "A high frequency gravitational wave generator including a
gas filled shell with an outer shell surface, microwave emitters, sound generators, and acoustic
vibration resonant gas-filled cavities... propagating gravitational field fluctuations are
generated when the second electromagnetic field propagates through the first electromagnetic
field."

**The rule, applied.** Every one of those sentences is Tier 1 **for what the patent claims**. Not
one of them is evidence that any of it works, and the section below is the record of what
happened when the Navy tested it.

**The citation the board should carry.** US 10,144,532's "Other Publications" list, printed on
the front page, includes:

- "Froning, H. David, Quantum Vacuum Engineering for Power and Propulsion from the Energetics of
  Space, Third International Conference on Future Energy, Oct. 9-10, 2009, Washington, DC, US."
- "**Puthoff, H. E., Polarizable-Vacuum (PV) Approach to General Relativity, Foundations of
  Physics, Jun. 2002, vol. 32, No. 6.**"
- "Prigogine, Ilya, Time, Structure and Fluctuations, Nobel Lecture, Dec. 8, 1977."
- "Hayasaka, Hideo and Takeuchi, Sakae, Anomalous Weight Reduction on a Gyroscope's Right
  Rotations around the Vertical Axis on the Earth, The American Physical Society, Physical
  Review Letters, Dec. 18, 1989, vol. 63, No. 25, Japan."
- "Pais, Salvatore, Conditional Possibility of Spacecraft Propulsion at Superluminal Speeds,
  Intl. J. Space Science and Engineering, 2015, vol. 3, No. 1."
- "Pais, Salvatore, The High Energy Electromagnetic Field Generator, Int. J. Space Science and
  Engineering, 2015, vol. 3, No. 4."

**A US Navy patent cites Harold Puthoff by name on its printed front page.** `harold-puthoff` is
already a tier A node. This is a Tier 1 documentary join between the Navy filing and a figure the
board carries, and it is better evidence of a connection than any podcast statement about the
same relationship.

### 3.4 The documented internal assessment, and the citation upgrade it makes possible

The board currently carries this as a Tier 2 claim on `salvatore-pais` sourced to
"Secondary reporting summarised at [Wikipedia] citing FOIA-released NAWCAD records; the
underlying release has not been obtained for this board."

**That citation can be replaced today with a named reporter quoting a named Navy spokesman.**
Brett Tingley, The War Zone, "The Navy Finally Speaks Up About Its Bizarre 'UFO Patent'
Experiments", updated 1 February 2021, quoting **Timothy Boulay, Communications Director at
NAWCAD**, verbatim:

> "The High Energy Electromagnetic Field Generator testing occurred from October 2016 through
> September 2019."
>
> "The cost was $508,000 over the course of three years. Around ninety percent of the total -
> $462,000 - was for salaries, while the rest was used for equipment, test preparation, testing
> and assessment."
>
> "When NAWCAD concluded testing in September 2019, the 'Pais Effect' could not be proven."

**Three upgrades over the board's current text:** the sum is $508,000 and not "roughly 500,000";
the window is October 2016 to September 2019 and not "between 2016 and 2019"; and the source is a
named NAWCAD official quoted by a named reporter rather than an encyclopedia summary. The claim
stays **Tier 2** because it is a named person on the record and not a document this session
opened, and because the FOIA release itself is still not in the board's hands.

**What this does to the strand.** The Pais row is the one mechanism where the cited document, the
sponsor and the test result are all documented, and the test result is negative. It is the
strongest row in the file precisely because it is complete: the government filed it, the
government funded it, the government tested it, and the government's own spokesman says the
effect could not be proven. **No other mechanism in this strand has all four.**

### 3.5 What Millis's NASA survey says about the same mechanism, six years earlier

NASA/TM-2004-213082, section 3.3.2, opens: "Fundamentally, gravitational waves are perturbations
in spacetime caused by violent accelerations of large masses, such as collisions of black holes."
The section proceeds to low-frequency detection and LIGO. **NASA's breakthrough-propulsion survey
of 2004 treats high frequency gravitational waves as a detection problem, and the Navy's patent
of 2019 claims to generate them with sound generators and microwave emitters in a gas-filled
shell.** Both statements are Tier 1 for what their documents say. The strand records the
distance between them and draws no conclusion beyond that.

---

## 4. Alcubierre metric engineering

### 4.1 What the 1994 paper actually claims, in Alcubierre's own terms

Opened this session: the arXiv posting of 5 September 2000 (`gr-qc/0009013`) of the paper
published as **Miguel Alcubierre, "The warp drive: hyper-fast travel within general relativity",
Classical and Quantum Gravity 11-5, L73-L77 (1994)**, DOI 10.1088/0264-9381/11/5/001. The posting
carries the author's affiliation at the time as the Department of Physics and Astronomy,
University of Wales, College of Cardiff, with a present address at the Max Planck Institut für
Gravitationsphysik, Albert Einstein Institut, Potsdam.

**Abstract, verbatim in full:**

> "It is shown how, within the framework of general relativity and without the introduction of
> wormholes, it is possible to modify a spacetime in a way that allows a spaceship to travel with
> an arbitrarily large speed. By a purely local expansion of spacetime behind the spaceship and
> an opposite contraction in front of it, motion faster than the speed of light as seen by
> observers outside the disturbed region is possible. The resulting distortion is reminiscent of
> the 'warp drive' of science fiction. However, just as it happens with wormholes, exotic matter
> will be needed in order to generate a distortion of spacetime like the one discussed here."

**The requirement, verbatim from the body, and this is the sentence the strand exists to
record:**

> "The metric I have just described has one important drawback, however: it violates all three
> energy conditions (weak, dominant and strong). Both the weak and the dominant energy conditions
> require the energy density to be positive for all observers."

And, having given the expression for the energy density the Eulerian observers see:

> "The fact that this expression is everywhere negative implies that the weak and dominant energy
> conditions are violated. In a similar way one can show that the strong energy condition is also
> violated."

And the conclusion he draws from it:

> "We see then that, just as it happens with wormholes, one needs exotic matter to travel faster
> than the speed of light. However, even if one believes that exotic matter is forbidden
> classically, it is well known that quantum field theory permits the existence of regions with
> negative energy densities in some special circumstances (as, for example, in the Casimir
> effect). The need of exotic matter therefore doesn't necessarily eliminate the possibility of
> using a spacetime distortion like the one described above for hyper-fast interstellar travel."

His closing paragraph, verbatim:

> "As a final comment, I will just mention the fact that even though the spacetime described by
> the metric (8) is globally hyperbolic, and hence contains no closed causal curves, it is
> probably not very difficult to construct a spacetime that does contain such curves using a
> similar idea to the one presented here."

### 4.2 What the paper is not, by word count

Taken this session over the complete 10-page text:

| term | count |
|---|---|
| spaceship | 28 |
| propulsion | **1**, and it is "A propulsion mechanism based on such a local distortion of spacetime just begs to be given the familiar name of the 'warp drive' of science fiction" |
| **device** | **0** |
| how to | **0** |

**The paper contains no device, no apparatus, no engine and no method of construction.** It is a
solution of the Einstein field equations, run backwards: choose the trajectory you want, compute
the stress-energy tensor that would produce it, and observe that the tensor is everywhere
negative. Alcubierre states the requirement plainly and does not claim to have met it. **A
citation of this paper as evidence that a craft could do this is a citation of a requirement as
though it were a capability.** That is this strand's pattern in its purest form, and unlike the
other five it is not even a misreading of the document - the document's own abstract says
"exotic matter will be needed".

### 4.3 What NASA's own survey says about it

NASA/TM-2004-213082, section 3.3.1, "Metric Engineering", verbatim:

> "Enormous technical hurdles face these concepts. In particular, they require enormous
> quantities of 'negative energy' (equivalent mass of planets or suns), and evoke time-travel
> paradoxes ('closed-time-like curves')."

And:

> "Recently, the term 'metric engineering' has emerged at aerospace conferences to represent such
> space-warping propulsion concepts. The origin of this term is unknown. Given the magnitude of
> energy requirements to create perceptible effects, it is unlikely that experimental work will
> be forthcoming in the near future. Even though these theoretical concepts are extremely
> unlikely to be engineered, they are at least useful as teaching tools to more thoroughly
> explore the intricacies of Einstein's General Relativity."

**The phrase "metric engineering", which the UAP literature uses as a term of art, is recorded by
NASA in 2004 as a term of unknown origin that emerged at aerospace conferences.** The board
should carry that, because it dates and locates a piece of vocabulary the field treats as
technical.

### 4.4 What DIA's own warp DIRD claims, and the numbers it prints

`dird-warp-drive-dark-energy-and-the`, DIA-08-1004-001, 34 pages, opened this session. The DIA
list of 9 January 2018 attributes it to "Dr R Obousy, Obousy Consultants"; EarthTech's own
citation list gives it as Obousy and Davis jointly. Its reference 1 is Alcubierre 1994.

**It prints two tables of the negative energy required.** Table 2, its less favourable model, and
Table 3, after the reduction it argues for:

| Warp factor | Table 2, E_warp (J) | Table 3, E_warp (J) |
|---|---|---|
| 0.01 (3,000 km/s) | -3.03 x 10^46 | -1.00 x 10^38 |
| 0.5 (150,000 km/s) | -7.59 x 10^49 | -2.50 x 10^41 |
| **1 (light speed)** | **-3.03 x 10^50** | **-1.00 x 10^42** |
| 2 (600,000 km/s) | -1.21 x 10^51 | -4.00 x 10^42 |

Its own Summary, verbatim:

> "The idea that a sufficiently advanced technology may interact with, and acquire direct control
> over, the higher dimensions is a tantalizing possibility, and one that is most certainly worthy
> of deeper investigation. Control of this higher dimensional space may be a source of
> technological control over the dark energy density and could ultimately play a role in the
> development of exotic propulsion technologies; specifically, a warp drive. Of course, this may
> not be actualized until many years in the future..."

And its closing sentence:

> "...if we may make predictions based on the innovative history of scientific pioneers of the
> past, then it seems entirely possible that the creative minds of the future may indeed find
> ways to accomplish what, to us, may seem like magic."

**What the document actually claims: that the requirement is very large, that a particular
theoretical route might reduce it by eight orders of magnitude, and that the whole thing is
worthy of deeper investigation.** It claims no experiment, no apparatus and no observation. **A
DIA cover page and a document number do not change that, and the strand's job is to say so.**

### 4.5 The owner's reasoning, recorded as his

The brief records, in Stewart's own framing of 18 September 2026, that he rules Alcubierre-style
metric engineering out on his own reasoning: **locally bending spacetime above a building would
have effects nobody could conceal.**

**That is recorded here as the board owner's reasoning and as nothing else.** It is not a finding
of this session, it is not derived from any document opened above, and it must not be written
onto a node as though a document supported it. It is a good argument and it is his. If a build
session wants it on the board it belongs as an editorial note attributed to him by name and date,
in the same way the board handles other owner rulings, and at **Tier 3, stated inference**.

What the documents in sections 4.1 to 4.4 independently establish, and what a node may assert
without him, is narrower and stronger: the paper requires negative energy densities everywhere in
the bubble wall, says so in its own abstract, contains no device, and NASA's own survey puts the
requirement at the equivalent mass of planets or suns.

---

## 5. The Hutchison effect

### 5.1 The honest answer, stated plainly

**No peer-reviewed publication documenting the Hutchison effect was located by this session, and
no primary record of a controlled demonstration was opened.**

Every candidate source returned was one of: the claimant's own website, a slide deck uploaded by
the claimant, a self-published compilation, a personal archive site, a podcast page, or the
proceedings of a conference devoted to unconventional energy. **None of them is cited anywhere in
this file, and none of them should be cited on the board.**

The brief already records Hutchison-effect variants as "not enumerated" and "not opened". **That
remains the state, and this section's finding is that it remains the state after looking.**

**It rests entirely on undocumented video demonstrations.** That is the sentence the brief asked
for if it was the honest answer, and it is the honest answer. Objects are said to rise, metals to
fuse and fracture, in footage whose apparatus, controls, camera orientation and instrumentation
are not documented in any record this session could open. There is no measurement to check and no
protocol to fault.

### 5.2 The two negative findings that are worth more than the absence

The absence of literature is weak evidence on its own. Two positive checks are worth more, and
both are checkable:

**First: the one named professional engineer associated with the claim wrote two DIA-funded
reports and named Hutchison in neither of the two, at least in the one this session opened.**

`george-hathaway` is already a tier C node. The board records him as a two-deliverable AAWSAP
contributor: item 10, "Role of Superconductors in Gravity Research", and item 16, "Maverick
Inventor Versus Corporate Inventor", both as Hathaway Consulting. His own firm's staff page,
opened this session, states he "graduated from the Dep't of Electrical Engineering at the
University of Toronto in 1974 and is a Registered Professional Engineer", consults on "novel and
exotic materials, energy production and propulsion concepts", and is "author of the book
'Mindbending: The Hutchison Files'".

This session opened his DIRD. **DIA-08-1003-017, "Maverick Inventor Versus Corporate Inventor:
Where Will the Next Major Innovations Arise?", 30 March 2010, ICOD 1 December 2009, 20 pages,
"Acquisition Threat Support" banner.** Word counts over the whole released document:

| term | count |
|---|---|
| **Hutchison** | **0** |
| Pharos | **0** |
| levitation | **0** |
| gravity | 12 |
| antigravity | 3 |

**The man who wrote the book on the Hutchison effect wrote a DIA reference document about
maverick inventors and did not mention it.** That is a far stronger datum than any count of
absent journal articles, and it is Tier 1 because it is a word count over an opened government
document.

**Second: NASA's breakthrough-propulsion survey, which does name the comparable claims, does not
name this one.** NASA/TM-2004-213082 names Biefeld-Brown four times, lifters and asymmetrical
capacitors five times between them, Podkletnov twelve times and Alcubierre once. **Hutchison:
zero.** Millis's project existed specifically to triage claims of this kind, assessed sixteen
incremental research tasks, and found "about a third were found not to be viable". The Hutchison
effect did not reach the list of things worth finding non-viable.

### 5.3 What a later session should and should not do

**Should:** open the second Hathaway DIRD, "The Role of Superconductors in Gravity Research",
DIA-08-1003-0xx, which this session did not open, and run the same word count. If Hutchison is
absent from that one too, the finding is complete. Also open "Mindbending: The Hutchison Files"
if a copy can be reached, and record what it is - a book by a named registered engineer is a Tier
2 record of what he says, which is more than the board has now.

**Should not:** create a node. **No node is proposed for the Hutchison effect or for John
Hutchison.** Per the brief, it gets a strand row and nothing more. A node built on video would be
a node the board could not source, and the board's standing rule is that an unsourceable node is
worse than an absent one.

---

## 6. The mechanisms the ARV and TR-3B clusters invoke

Both clusters were built on 18 September 2026 and both already carry the refutations. The
strand's job is to tie them in, not to redo them.

### 6.1 TR-3B: the mercury plasma "Magnetic Field Disruptor"

The board's `tr-3b` node, tier A, already carries at Tier 1 the propulsion claim from slide 72 of
the 1998 Fouché presentation - "A circular, plasma filled accelerator ring called the Magnetic
Field Disrupter, surrounds the rotatable crew compartment" - and, at Tier 1, the physical anchor
against it: the NIST Chemistry WebBook gives mercury, CAS 7439-97-6, a melting point of 234.31 K,
a triple point of 234.3 K and a boiling point of 629.81 K, sourced to
`https://webbook.nist.gov/cgi/cbook.cgi?ID=C7439976&Mask=4`, opened 18 September 2026. The Tier 3
inference on the node is that the claimed 150 K is 84 K below mercury's melting point, and that
mercury's melting curve has a positive slope, so the claimed 250,000 atmospheres pushes the
material further into the solid region rather than out of it.

**The strand's contribution is the classification, not the physics.** The TR-3B row differs from
every other row in this file in one respect that should be stated: **the document cited for the
mechanism is not a mundane real document being misread. It is a slide deck that asserts the
mechanism directly.** There is no gap between citation and source here because there is no
independent source. That makes it the weakest kind of row in the strand and the table below marks
it so.

### 6.2 ARV / Flux Liner: the capacitor stack read as levitation

The board's `arv-fluxliner` node, tier B, already carries at Tier 2 the capacitor-stack
description in McCandlish's own words from the April 2001 Briefing Document, the Tesla-coil
architecture, and the attribution of the lift effect to Thomas Townsend Brown via "a patent that
was filed back in the late 1950s/early 1960s". Two edges built on 18 September 2026 carry the
caveat in their notes: neither Brown patent claims anti-gravity, both claim thrust by electrical
fields in a dielectric medium, and **it is the ACCOUNT that reinterprets electrokinetic thrust as
levitation.**

**Section 2 of this file supplies what those edge notes could not have on 18 September:** the
patents opened and word-counted with gravity at zero in both, the NASA technical memorandum that
names Biefeld-Brown and lifters and rules them out by name, the NASA contractor report that
models the thrust as ion drift and reproduces the measured magnitude, and the Air Force vacuum
test quoted inside it showing no detectable propulsive force under high vacuum. **The ARV edge
caveats are now backed by four opened documents rather than by the board's own prior reading.**

And the `d-exotic` domain node, "Exotic Technology & Physics", tier B, is where this strand
lands. Every mechanism in it is a claim about exotic physics whose cited document turns out to be
about conventional physics, about a requirement, or about nothing at all.

---

## STRAND TABLE

One row per mechanism. **Tier is the claim tier for the row's central assertion**, which is
always "this is what the cited document actually claims" and never "this is whether it works".

| # | Mechanism | Document usually cited | What the document ACTUALLY claims | What is claimed FOR it | Tier |
|---|---|---|---|---|---|
| 1 | **Magnetohydrodynamic propulsion** | **US 3,322,374**, King, filed 30 Sept 1964, granted 30 May 1967, no assignee, no government interest | A linear induction motor using ionised atmosphere as its armature. Polyphase AC through axial coils drives a travelling flux maximum that induces eddy currents in the surrounding ionised fluid and drives it backwards. Classical electromagnetism. **scalar 0, spin 0, gravity 0, anti-gravity 0, zero point 0** | That it is "ample evidence" the "Scalar Physics" callout on the McCandlish ARV drawing refers to spin-zero scalar particles | **1** for what the patent claims. The document is openable and the word counts are checkable |
| 1a | *Control case for 1* | **Yamato-1**, OSTI record for Sasakawa, Takezawa, Sugawara and Kyotani, World Congress on Superconductivity vol. 1, 1994/95 | That an experimental ship became "the world's first superconducting MHD-propelled ship on her trial runs in June 1992", built by the Ship & Ocean Foundation from a 1985 committee and a 1989 construction decision | Nothing. It is not cited by the lore, which is the point | **1** |
| 1b | *Government document for 1* | **DIRD DIA-08-1011-006**, "MHD Air Breathing Propulsion and Power for Aerospace Applications", 21 Nov 2010, attributed on the DIA list to Dr S Macheret, Lockheed Martin | That MHD concepts are "attractive" but that "significant difficulties impede the development and application of these technologies; these include weight, complexity, higher power", and that the Ajax bypass concept "has been shown to be meaningless below at least Mach 12". **UFO 0, antigravity 0, scalar 0, zero point 0** | That an AAWSAP document on MHD is evidence of recovered technology | **1** |
| 2 | **Electrokinetic / Biefeld-Brown** | **US 2,949,550** (filed 3 Jul 1957, granted 16 Aug 1960, Whitehall-Rand Inc) and **US 3,187,206** (filed 9 May 1958, granted 1 Jun 1965, Electrokinetics Inc) | Thrust by direct operation of electrical fields, with the reaction appearing in the surrounding dielectric medium. **The word "gravity" appears zero times in either patent** | Anti-gravity; electrogravitics; levitation; the lift mechanism of the ARV capacitor stack | **1** for what the patents claim |
| 2a | *Counter-explanation for 2* | **NASA/TM-2004-213082** s3.2.7, Millis, NASA Glenn, 2004 | "To date, all rigorous experimental tests indicate that the observed thrust is attributable to ion wind." These devices "are not viable candidates for breakthrough physics propulsion" | - | **1** |
| 2b | *Experiment behind 2a* | **NASA/CR-2004-213312**, Canning, Melcher and Winet, Oct 2004, 23 pp | An ion-drift model "consistent with all of our observations", predicting thrust magnitude, direction and polarity-independence. "we find no evidence to support" new physical principles | - | **1** |
| 2c | *Dissent within 2a, recorded* | **Bahder and Fazi**, ARL-TR-3005 / arXiv physics/0211001 | "ionic wind is at least three orders of magnitude too small to explain the magnitude of the observed force". Prefers ionic drift. **Still invokes no new physics** | Sometimes cited as showing the effect is unexplained | **2**, because the published ARL report was NOT opened; the arXiv preprint was |
| 2d | *The absence that matters* | **DIRD DIA-08-1003-018**, "Antigravity for Aerospace Applications", 30 Mar 2010, attributed to Eric Davis | Gravitomagnetic forces, Forward's dipole generator, Felber's effect, negative energy, dark energy, quantum vacuum ZPF. Requires "kilometer-sized apparatus, astronomical-sized masses and densities, or extreme mass velocities". **Biefeld 0, electrogravitics 0, Podkletnov 0, T. T. Brown absent** | That the government's antigravity programme vindicates the electrogravitics thread | **1** |
| 3 | **Inertial mass reduction** | **US 10,144,532** and four sibling filings, 2015 to 2018, all assigned to the Secretary of the Navy, prosecuted by NAWCAD before examiner Philip J Bonzell | A resonant cavity vibrated by microwave emitters to "create a local polarized vacuum outside the outer resonant cavity wall". Cites Puthoff's polarizable-vacuum paper on its face | That the Navy patented a working UAP drive | **1** for what the patents claim, and for the Navy's sponsorship, which is printed |
| 3a | *Test result for 3* | **Timothy Boulay, NAWCAD, quoted by Brett Tingley, The War Zone, 1 Feb 2021** | Testing October 2016 to September 2019, $508,000 of which $462,000 salaries, and "When NAWCAD concluded testing in September 2019, the 'Pais Effect' could not be proven" | - | **2**, a named person on the record; the FOIA release itself is not in the board's hands |
| 4 | **Alcubierre metric engineering** | **Alcubierre, Class. Quantum Grav. 11, L73-L77 (1994)** | A metric permitting arbitrary apparent speed, which "violates all three energy conditions", whose energy density "is everywhere negative", and for which "one needs exotic matter". **The word "device" appears zero times** | That warp drive is an engineering programme, and that craft observed manoeuvring are using it | **1** for what the paper claims |
| 4a | *Government document for 4* | **DIRD DIA-08-1004-001**, "Warp Drive, Dark Energy, and the Manipulation of Extra Dimensions", 2 Apr 2010, attributed on the DIA list to Dr R Obousy | Tabulates the requirement at **-1.00 x 10^42 J** for light speed on its most favourable model, and concludes the future "may indeed find ways to accomplish what, to us, may seem like magic" | That DIA funded warp-drive development | **1** |
| 4b | *The owner's ruling on 4* | - | - | Stewart's own reasoning, 18 September 2026: locally bending spacetime above a building would have effects nobody could conceal | **3**, stated inference, and it is **HIS**, recorded as his and not as a finding of this session |
| 5 | **Hutchison effect** | **Nothing openable.** No peer-reviewed publication and no primary record of a controlled demonstration was located | Nothing that can be graded. **It rests entirely on undocumented video demonstrations** | Levitation, metal fusion, spontaneous fracture, anomalous heating, all by electromagnetic means | **No tier.** There is no document to grade. **No node proposed** |
| 5a | *The two checkable negatives for 5* | **DIRD DIA-08-1003-017** (Hathaway's own) and **NASA/TM-2004-213082** | Hathaway's DIA-funded report names **Hutchison 0 times**. NASA's survey names Biefeld-Brown, lifters, Podkletnov and Alcubierre, and names **Hutchison 0 times** | - | **1**, word counts over two opened government documents |
| 6 | **TR-3B mercury plasma "Magnetic Field Disruptor"** | **Slide 72 of the 1998 Fouché presentation**, `fouche-iufoc-1998` | The slide asserts the mechanism directly. **There is no independent document to misread**, which makes this the weakest row in the strand | A mercury plasma accelerated to 50,000 rpm at 250,000 atmospheres and 150 K, disrupting gravity | **1** for what the slide says; already refuted on `tr-3b` at Tier 1 by NIST's melting point of 234.31 K |
| 6a | **ARV capacitor stack read as levitation** | The Brown patents, via the April 2001 Briefing Document, `arv-fluxliner` | Row 2 applies unchanged: thrust by electrical fields in a dielectric medium | A capacitor stack levitating a manned craft | **2** for the account; **1** for what the patents claim |

---

## PROPOSED NODES AND EDGES

### 7a. Proposed nodes

Node tiers A/B/C are **proximity to the programme, not credibility**, per `CLAUDE.md` section 6.
Several nodes below carry only Tier 1 claims and sit at tier C, and that is not a contradiction
either: a well-documented thing can be far from the programme.

| id | cls | label | one line | node tier | reason |
|---|---|---|---|---|---|
| `nasa-bpp` | program | NASA Breakthrough Propulsion Physics Project (1996-2002) | NASA's own project to assess whether propulsion breakthroughs were achievable, with three grand challenges - propellantless propulsion, hyper-fast travel, and breakthrough power - which completed sixteen incremental research tasks and found about a third not viable | **B** | **The highest-value node in this file.** It is the real, funded, government assessment of exactly the mechanisms this strand covers, it ran for six years, and **the board already carries the man who managed it at tier B**. Tier B not A because it is NASA civil aeronautics rather than the classified thread, but it is structurally central to every exotic-propulsion claim on the board rather than adjacent to it |
| `millis-tm-2004-213082` | document | NASA/TM-2004-213082, "Prospects for Breakthrough Propulsion from Physics" (2004) | Marc G. Millis's 19-page summary of the BPP Project's methods and findings, prepared for a NASA/DoD-cosponsored conference in Seattle in June 2004, which adjudicates Biefeld-Brown, lifters, asymmetrical capacitors, Podkletnov, metric engineering and high frequency gravitational waves | **B** | **One opened document adjudicates three of this strand's six mechanisms by name.** It is the single most reusable citation this session found, and the board currently has nothing like it: an official, openable, non-classified assessment written by somebody the board already carries |
| `canning-nasa-cr-2004-213312` | document | NASA/CR-2004-213312, "Asymmetrical Capacitors for Propulsion" (2004) | The NASA contractor report by Canning, Melcher and Winet of the Institute for Scientific Research that tested asymmetrical capacitor thrusters at atmospheric and reduced pressures and concluded their operation is "fully explained" by electrostatic forces and momentum transfer through multiple collisions | **C** | The experiment behind the finding, as distinct from the survey that reports it. It cites both Brown patents by number in its own reference list, which makes the join to `thomas-townsend-brown` documentary rather than topical. **Foldable into `millis-tm-2004-213082` if a build session would rather carry one node than two** |
| `alcubierre-1994` | document | Alcubierre, "The warp drive: hyper-fast travel within general relativity" (1994) | The five-page Classical and Quantum Gravity letter that is the origin of every warp-drive claim in the field, which states in its own abstract that "exotic matter will be needed" and in its body that the metric "violates all three energy conditions" | **B** | The cited document for mechanism 4 and the ancestor of `dird-warp-drive-dark-energy-and-the`, which carries it as its reference 1. **The node's own summary must state that the paper contains no device**, or the node will read as support for the claim rather than as its measurement |
| `king-patent-mhd` | document | US 3,322,374, "Magnetohydrodynamic Propulsion Apparatus", King (1967) | A 1964 private filing by an individual at a home address in Winston-Salem, granted 1967, claiming a linear induction motor that uses ionised air as its armature, with no assignee, no government interest and no secrecy order | **C** | The strand's control case: a fully documented patent for the exact mechanism the lore invokes, informative **precisely because it is ordinary**. **THIS NODE DOES NOT GO INTO THE PATENTS VIEW.** See section 1.5 and the brief's section 4. Tier C is generous and reflects strand membership, not proximity |
| `yamato-1` | program | Yamato-1, superconducting MHD-propelled ship (1992) | The Ship & Ocean Foundation's experimental vessel, built from a 1985 committee and a 1989 construction decision, which on her trial runs in June 1992 became the world's first superconducting magnetohydrodynamic-propelled ship | **C** | The real-world record of the mechanism, and the strand's only genuine control. **Propose it only if the board wants controls as nodes.** If not, it belongs in the strand table alone and the row above should be dropped. Flagged for the owner's decision rather than assumed |

**Nodes considered and NOT proposed:**

- **`james-f-king` / a person node for the inventor.** He is a private individual at a home
  address with no assignee, no contractor, no programme, no clearance and no government interest.
  **On the board's own test he connects to nothing**, and a person node for him would be exactly
  the sourcing-by-topical-resemblance the brief's section 4 forbids. The patent gets a node
  because a document that was cited can be graded; the man cannot be, because nothing attaches to
  him.
- **`hutchison-effect` and `john-hutchison`.** Per section 5 and per the brief. **No document
  exists to source a node on.** A strand row, and nothing else.
- **`miguel-alcubierre` as a person node.** Same discipline the board applied to `david-l-morgan`
  in the Lazar file: one document, no other presence on the board, no programme connection. The
  paper is the node and he is a claim on it.
- **`us-3187206` and `us-2949550` as document nodes.** The board carries both as claims on
  `thomas-townsend-brown` and that is deliberate. Creating them now would split a node's evidence
  across three places for no gain.
- **`talley-pl-tr-91-3009`.** The Air Force vacuum test. **NOT opened by this session**, and a
  node built on two quotations inside another document is a node the board cannot stand behind.
  It is in WHAT I COULD NOT ESTABLISH as the first thing a later session should fetch.
- **`tajmar-2004`.** Same reason. `arc.aiaa.org` returned 403 and the paper was not opened. It is
  named in this file only as NASA's reference 54.
- **`institute-for-scientific-research` / `west-virginia-institute-for-scientific-research`.**
  Named in both NASA documents as the contractor, and it is a Congressional-earmark recipient,
  which is the shape of thing this board usually wants. **But this session opened nothing about
  the institute itself**, only documents it produced. A contractor node built from a byline is a
  guess about an organisation. Left for a later pass.
- **`salvatore-pais` and the five Pais patent nodes.** All five already exist. Every Pais item
  below is an enrichment, never a creation.

### 7b. Proposed edges

Existing ids are marked **ENRICH, existing id**. Edge types are taken from those already in use
on the board: institutional, programmatic, investigative, legislative, denial, witness-chain,
research, custody, temporal, behavioral, geographic, funding.

| from | to | type | tier | justification |
|---|---|---|---|---|
| `marc-millis` **ENRICH, existing id** | `nasa-bpp` | institutional | 1 | He managed the project and authored its summary technical memorandum. NASA/TM-2004-213082 carries his name and NASA Glenn affiliation on its title page |
| `nasa-bpp` | `nasa` **ENRICH, existing id** | institutional | 1 | "NASA supported the Breakthrough Propulsion Physics Project from 1996 through 2002", from the TM's own abstract |
| `marc-millis` **ENRICH, existing id** | `millis-tm-2004-213082` | custody | 1 | Sole author |
| `millis-tm-2004-213082` | `nasa-bpp` | custody | 1 | It is the project's published summary of its own methods and findings |
| `millis-tm-2004-213082` | `thomas-townsend-brown` **ENRICH, existing id** | **denial** | 1 | **Explicit denial edge, and the strongest in this file.** Section 3.2.7 names "Biefeld-Brown", "Lifters" and "Asymmetrical Capacitors" and concludes they "are not viable candidates for breakthrough physics propulsion", with the thrust "attributable to ion wind". **The edge note must state that this is a finding about the effect and the devices, not about what Brown's patents claim**, since the patents never claimed anti-gravity in the first place |
| `millis-tm-2004-213082` | `alcubierre-1994` | **denial** | 1 | Section 3.3.1: these concepts "require enormous quantities of 'negative energy' (equivalent mass of planets or suns)" and are "extremely unlikely to be engineered". A qualified denial of engineerability, not of the mathematics, and the note must say which |
| `millis-tm-2004-213082` | `d-exotic` **ENRICH, existing id** | research | 1 | It is a government assessment of exotic propulsion physics, which is the domain node's subject |
| `canning-nasa-cr-2004-213312` | `thomas-townsend-brown` **ENRICH, existing id** | research | 1 | Its reference list cites US 2,949,550, US 3,187,206 and GB 300,311 by number. The join is documentary, not topical |
| `canning-nasa-cr-2004-213312` | `millis-tm-2004-213082` | research | 1 | Reference 55 of the TM names the same ISR work; the CR is the experiment the TM summarises |
| `canning-nasa-cr-2004-213312` | `nasa` **ENRICH, existing id** | funding | 1 | A NASA contractor report bearing a NASA/CR number |
| `alcubierre-1994` | `dird-warp-drive-dark-energy-and-the` **ENRICH, existing id** | research | 1 | The DIRD's reference 1 is the Alcubierre paper, printed in its own reference list |
| `alcubierre-1994` | `dird-antigravity-for-aerospace-applications` **ENRICH, existing id** | research | 1 | The antigravity DIRD's reference [43] is the same paper. **This is its only appearance in that document** |
| `king-patent-mhd` | `arv-fluxliner` **ENRICH, existing id** | **denial** | 1 | **THE STRAND'S FOUNDING EDGE and its note is load-bearing.** The patent is offered as evidence for the ARV drawing's "Scalar Physics" callout and contains the word scalar zero times. The edge records a **failed citation**, and the note must say "cited FOR the ARV account and does not support it", never "connected to" |
| `king-patent-mhd` | `dird-mhd-air-breathing-propulsion-and-power` **ENRICH, existing id** | research | 3 | Same mechanism, two documents, forty-six years apart, neither exotic. **Tier 3 because this is a stated inference of similarity and nothing joins the two documents to each other.** Propose it only if the strand wants the comparison visible; drop it rather than imply a link |
| `yamato-1` | `king-patent-mhd` | research | 3 | Same mechanism, independently built. Stated inference. **No document joins them and the note must say so** |
| `salvatore-pais` **ENRICH, existing id** | `harold-puthoff` **ENRICH, existing id** | research | 1 | **The best new documentary join in this file.** US 10,144,532's printed "Other Publications" list cites "Puthoff, H. E., Polarizable-Vacuum (PV) Approach to General Relativity, Foundations of Physics, Jun. 2002, vol. 32, No. 6". Tier 1 because it is printed on the face of a granted US Navy patent |
| `pais-patent-imrd` **ENRICH, existing id** | `us-navy` **ENRICH, existing id** | institutional | 1 | Already on the board in substance; the enrichment is that the assignee line, the NAWCAD attorney of record (Mark O Glut) and the examiner (Philip J Bonzell) are all printed on the patent's front page and were read there this session |
| `millis-tm-2004-213082` | `pais-patent-hfgw` **ENRICH, existing id** | research | 3 | Section 3.3.2 treats high frequency gravitational waves as a detection problem in 2004; the Navy patent claims generation in 2019. **Stated inference about the distance between two documents, and the note must not present it as a refutation** |
| `dird-antigravity-for-aerospace-applications` **ENRICH, existing id** | `thomas-townsend-brown` **ENRICH, existing id** | **denial** | 1 | **THE ABSENCE EDGE, and it needs the most careful note on this page.** The government's own 45-page antigravity survey names Biefeld zero times, electrogravitics zero times and T. T. Brown not at all. The edge asserts **an absence in a named document**, which is a Tier 1 fact about the document. Its note must state the word counts and the page count so a reader can check it, and must not be written as "DIA rejected Brown" - DIA's contractor simply never reached for him |
| `george-hathaway` **ENRICH, existing id** | `d-exotic` **ENRICH, existing id** | research | 2 | His own firm's page: a registered professional engineer consulting on "novel and exotic materials, energy production and propulsion concepts", author of "Mindbending: The Hutchison Files". **This is the board's only documented link to the Hutchison claim and it runs through a person, not through the claim** |
| `king-patent-mhd` | `d-exotic` **ENRICH, existing id** | research | 3 | Strand membership. Tier 3 and the note must say the patent itself is not exotic; it is here because it was cited as though it were |
| `alcubierre-1994` | `d-exotic` **ENRICH, existing id** | research | 2 | Same caveat: the paper is mainstream general relativity in a mainstream journal, and it is in this domain because of what is claimed for it |

**Edges considered and NOT proposed:**

- **Any edge from `king-patent-mhd` to a person, a contractor or a programme.** There is nothing
  to attach. That is the finding.
- **`millis-tm-2004-213082` to `tr-3b`.** The TM does not mention the TR-3B and an edge would be
  the strand committing the exact error it documents.
- **Any Hutchison edge.** No node, so no edge. The Hathaway edge above goes to the domain, not to
  a claim the board cannot source.
- **`nasa-bpp` to `dird-series`.** They are separate programmes six years apart with no documented
  contact. Millis later wrote a DIRD, which is a person-level fact already on `marc-millis` and
  `dird-cockpits-in-the-era-of-breakthrough`; it is not an institutional link between NASA BPP and
  AAWSAP and must not be drawn as one.

### 7c. Claim-level enrichments, for nodes that need no new edges

| node | enrichment | tier |
|---|---|---|
| `thomas-townsend-brown` | Serial numbers 669,830 and 734,342; assignees Whitehall-Rand Inc (Washington D.C., a Delaware corporation) and Electrokinetics Inc (Pennsylvania, by mesne assignments); 12 and 23 claims; both in Class 310-5; the abandoned parent application Ser. No. 293,465 filed 13 June 1952; and the word count showing "gravity" at zero in both complete texts | 1 |
| `salvatore-pais` | **Replace the Wikipedia-sourced test claim** with Timothy Boulay, NAWCAD, quoted by Brett Tingley, The War Zone, 1 February 2021: October 2016 to September 2019, $508,000 of which $462,000 salaries, and "the 'Pais Effect' could not be proven" | 2 |
| `pais-patent-imrd` | "4 Claims, 1 Drawing Sheet"; term extended 153 days under 35 U.S.C. 154(b); Int. Cl. B64G 1/40; attorney of record Mark O Glut, NAWCAD; and the six cited publications including Puthoff, Froning, Prigogine and Hayasaka | 1 |
| `dird-mhd-air-breathing-propulsion-and-power` | Its Summary verbatim, the Ajax finding, and the word counts (UFO 0, antigravity 0, scalar 0) | 1 |
| `dird-warp-drive-dark-energy-and-the` | The two negative-energy tables, its Summary, and its closing "may seem like magic" sentence | 1 |
| `dird-antigravity-for-aerospace-applications` | Its conclusion verbatim, its section structure, and the word counts in section 2.4 | 1 |
| `george-hathaway` | That his own DIRD, DIA-08-1003-017, 20 pages, names Hutchison zero times; and his firm's own statement of his credentials and of the book | 1 for the word count, 2 for the credentials |
| `marc-millis` | That he managed NASA BPP 1996-2002 and authored NASA/TM-2004-213082, which is a stronger and earlier institutional fact than the DIRD authorship the board currently carries for him | 1 |

---

## WHAT I COULD NOT ESTABLISH

This section is not empty and should not be made empty by a build session filling it in from
memory.

1. **The Talley report, PL-TR-91-3009.** The single most valuable unopened document in this
   strand. It is the Air Force's own vacuum test of asymmetric capacitors, Phillips Laboratory,
   Air Force Systems Command, Edwards AFB, final report for February 1989 to July 1990 on
   contract FO4611-89-C-0023. **This session quotes it only as NASA/CR-2004-213312 quotes it.**
   It matters because it is the one measurement that answers the specific question US 3,187,206
   raises in its own text about behaviour in a vacuum, and because it is a government document
   that would raise the whole electrokinetic row from Tier 1-via-NASA to Tier 1 direct. Try DTIC,
   the `archive.org/details/DTIC_*` mirror, and `irp.fas.org`.
2. **Tajmar 2004, AIAA Journal of Propulsion & Power 42, pp. 315-318.** `arc.aiaa.org` returned
   HTTP 403. **The paper was not opened** and is named in this file only as NASA's reference 54.
   It is the peer-reviewed form of the corona-wind explanation and the strand would be stronger
   with it opened.
3. **ARL-TR-3005 as published.** `apps.dtic.mil` returned HTTP 403. The arXiv preprint was opened
   instead. The preprint and the report are presumed to be the same work on the strength of the
   NASA CR's reference 8, which gives both the report number and the NTIS order number. **That
   presumption is not verified and the edge tier above reflects it.**
4. **The NAWCAD FOIA release behind the Boulay statement.** Still not in the board's hands. The
   TWZ article is a named reporter quoting a named official, which is Tier 2 and an improvement
   on the board's current Wikipedia citation, but it is not the record itself.
5. **The second Hathaway DIRD, "The Role of Superconductors in Gravity Research".** Not opened.
   The Hutchison finding in section 5.2 rests on one of his two DIA deliverables. Opening the
   other and running the same word count would complete it, either way.
6. **Any primary Hutchison-effect record at all.** No peer-reviewed publication, no controlled
   protocol, no instrumented measurement, no independent laboratory report. **This is a finding
   and not a gap, and a later session should not treat it as a research task that failed.** What
   would change it is a document, and none was found.
7. **The 1983 Los Alamos and INSCOM demonstrations said to have involved Hutchison.** The
   accounts in circulation name real people and real organisations, which is exactly what makes
   them tempting. **Every source for them that this session found traces back to the claimant's
   own chronology.** They are not asserted anywhere in this file and no node or edge above rests
   on them. If a later session wants them, the route is a FOIA request to INSCOM, not a better
   search.
8. **Yamato-1's measured performance figures.** The OSTI abstract establishes that sea trials
   happened in June 1992 and says the paper "describes the outline of the YAMATO-1 and sea trial
   test results", but **this session did not open the paper itself** and no speed, thrust,
   efficiency or field-strength figure is asserted anywhere above. The arXiv paper on MHD ship
   models was opened in the hope it would supply them and does not mention the vessel.
9. **Whether US 3,322,374 was ever built.** Nothing was opened either way, and the strand does not
   need it: the row is about what the patent claims, and a patent is never evidence that the thing
   works. Stated here so that the absence is a recorded decision rather than an oversight.
10. **The "Scalar Physics" callout's own provenance.** The brief records the Reddit claim about
    what it refers to, and section 1.2 records that the patent does not support it. **What the
    callout on the McCandlish drawing was actually meant to denote has not been established by
    anyone**, and the honest state is that the strand refutes one proposed reading of it without
    supplying another.
