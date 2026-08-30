# Video-transcript corpus, group B — structural extraction

**Extracted:** 30 August 2026. **Source:** four cached transcripts under `research/.transcripts/`
(gitignored, not committed, not published).

**Status of everything below: UNVERIFIED LEAD MATERIAL.** Every line records *what a named
speaker claims*, attributed, with a file + timestamp pointer. Nothing here is asserted as true
and nothing here is graded. No quotation exceeds a short phrase; where the wording matters the
pointer is given instead so the claim can be re-read at source.

**CLAUDE.md §2 applies here more sharply than anywhere else in the repo.** These are
auto-generated YouTube captions with heavy proper-noun corruption. Inside these four files the
same person's surname renders as `grush`, `gresh`, `garoosh`, `garage`, `Crush`, `grosh` and
`Gresham`; another as `fravor`, `favor`, `fraber`, `freyjer`, `Fiverr` and `braver`. The
governing precedent is HoloChron LLC, which a prior session chased as "Holocron Engineering".
Names below are marked:

- **[CONF]** — spelled consistently and matches a well-attested public figure or organisation.
- **[PHON?]** — phonetically corrupted; my best reconstruction, with the raw caption in
  `backticks`. **Treat as a search string, not a fact.**
- **[UNRESOLVED]** — could not be reconstructed with confidence. Recorded raw.
  **Must not reach the board under the transcript spelling.**

## File key

| code | id | length | what it is |
|---|---|---|---|
| **SNg** | `SNgoul4vyDM` | 138 min | **A congressional hearing.** Identified below as 26 July 2023, House Oversight, Subcommittee on National Security, the Border and Foreign Affairs. Sworn testimony. |
| **BEW** | `BEWz4SXfyCQ` | 135 min | Bob Lazar and Jeremy Corbell interviewed by Joe Rogan. Podcast; no oath. Internally dated to 2019 (Corbell's Netflix documentary is "out right now"; a LIGO lookup lands on 2016 as "four years ago"). |
| **TNt** | `TNtlzEnl8rA` | 156 min | Jesse Michels (American Alchemy) interviewing **Dr. Gregory Rogers**, retired USAF/NASA chief flight surgeon. Podcast; no oath. Post-dates his 30 April retirement and a 4 May Daily Mail piece. |
| **JE1** | `JE1oM89dpBc` | 127 min | Jesse Michels interviewing the musician **Flying Lotus** (Steven Ellison). Podcast; no oath. **Structurally thin — see §9.** |

Timestamps are the start of the caption **segment** carrying the phrase, `[code @ HH:MM:SS]`,
resolved directly out of the cached segment list rather than read off a paged printout —
`tools/read_transcript.py` flushes blocks roughly every 30 seconds and its printed block start
shifts with the `--from` window, so a pointer read that way can sit up to 30 seconds early.
Scrub to the timestamp, then read forward.

---

## 1. THE HEARING (SNg) — identification and what it adds

### 1a. Which hearing it is

Identified from internal evidence alone, then checked against the board.

| evidence | timestamp |
|---|---|
| "subcommittee on National Security ... of the board in foreign affairs" (caption garble of *the Border and Foreign Affairs*) | SNg @ 00:00:16 |
| Members waived on, named by the chair: Burchett (TN), Luna (FL), Gaetz (FL), Burlison (MO), Ocasio-Cortez (NY), Ogles (TN) | SNg @ 00:00:03 |
| Chair addressed as `Rothman` / `groffman` — Rep. **Glenn Grothman** [PHON?] | SNg @ 01:24:55, 02:10:59 |
| Ranking member Garcia; full-committee chair Comer yields his five minutes to Burchett | SNg @ 00:12:12, 01:18:55 |
| Three witnesses sworn: Ryan Graves, David Grusch, Cdr. David Fravor (Ret.) | SNg @ 00:22:58 |
| Grusch: NGA 2021–2023, GS-15; UAPTF 2019–2021; whistleblower filing "May 2022" | SNg @ 00:29:05, 00:29:21 |
| Garcia calls himself "a freshman member ... only been here for seven months" (118th Congress convened Jan 2023) | SNg @ 02:11:32 |
| Contemporary references: Chinese balloon "earlier this year"; Kirkpatrick's April testimony "on the 19th of April" | SNg @ 00:03:24, 01:01:06 |

**Verdict: this is `hearing-2023-07-26`, which the board already holds** — the House Committee
on Oversight and Accountability, Subcommittee on National Security, the Border and Foreign
Affairs, 26 July 2023, "Unidentified Anomalous Phenomena: Implications on National Security,
Public Safety, and Government Transparency", Serial No. 118-53 / CHRG-118hhrg53022. It is
**not** a new hearing. The board's other congressional-hearing event nodes are
`hearing-1966-04-05`, `hearing-2023-04-19`, `hearing-2024-11-13`, `hearing-2024-11-19`,
`hearing-2025-09-09` and `hearing-2026-06-30`; none of them matches.

### 1b. What the board already has (do not re-derive)

The node is unusually complete, and there are **thirteen member↔Grusch edges** carrying the
individual exchanges as notes. Already captured, verified by reading the board: the Mace
biologics exchange and witness-list offer; the AOC IR&D / Periodic Program Review /
notification-loophole line; the Moskowitz misappropriation-and-overcharging line; the Garcia
"40 witnesses over 4 years" and protected-disclosure chain; the Burchett harm/injury/murder
answers and the SCIF denial; the Luna April-2022 Kirkpatrick conversation and the DOPSR
clearance; the Biggs Phoenix Lights exchange naming Luke and the Barry Goldwater Range; Gaetz's
full Eglin account including the four-craft diamond formation and the "subpoenaed if necessary"
recommendation; Grusch on 10 U.S.C. §119, the Gang of Eight and E.O. 13526; Grusch's admission
that he helped author the 2019 UAPTF security classification guide; Grusch's FAR-violation
answer; Fravor's "never investigated ... tapes were never taken"; Graves' W-72 cube-in-sphere
and the AIAA integration committee; Luna's cease-and-desist questioning; Grothman's opening.

### 1c. What the transcript contains that the node does NOT — checked line by line

Each of these was grep-tested against the whole 6.9MB board and returns nothing.

| # | what was said | who | where |
|---|---|---|---|
| **H1** | Asked when the US government first became aware, Grusch answers **"1930s"**, and prefaces it by saying he prefers "non-human" because it "keeps the aperture open" | Grusch to Burchett | SNg @ 01:19:47 |
| **H2** | Grusch cites, by name, the **1971 US–USSR Agreement on Measures to Reduce the Risk of Outbreak of Nuclear War**, "unclassified treaty publicly available", says its **Article 3** and a "situation two" provision govern **red-line flash message traffic**, that the specific codes were **declassified in 2013** and sit in the **George Washington University National Security Archive**, and that he sought the incidents in which that traffic was actually used and "got a wall of Silence at the White House" | Grusch to Luna | SNg @ 02:01:57–02:02:36 |
| **H3** | "I spent **11 and a half hours** with both Intel committees" | Grusch to Burchett | SNg @ 01:23:32 |
| **H4** | Asked whether any activity had been hostile, Grusch says he knows of **multiple colleagues physically injured** and, asked to distinguish, answers that the injuries came from UAPs **and** from **people within the federal government** — "both". He then says what he "personally witnessed myself and my wife was very disturbing" | Grusch to Burlison | SNg @ 01:35:30–01:36:15 |
| **H5** | Answering the hypothesis that recovered craft are misidentified US contractor programmes, Grusch: not to my knowledge, **"the recoveries predate a lot of our advanced programs that I previously ... am witting of"** | Grusch to Burlison | SNg @ 01:39:07 |
| **H6** | Grusch offers the **holographic principle** as his theoretical framework for multidimensionality, derived from general relativity and quantum mechanics — and, pressed, states plainly that he has seen **no documentation** that this is what is occurring, "only a theoretical framework discussion" | Grusch to Burlison | SNg @ 01:37:56–01:38:30 |
| **H7** | Fravor: the radar tape recording the jamming **"was never released and we don't know where it's at"** | Fravor, opening statement | SNg @ 00:35:51 |
| **H8** | Fravor: on a large screen the FLIR video shows **two small objects coming out of the bottom** of the Tic Tac | Fravor to Moskowitz | SNg @ 01:07:03 |
| **H9** | Fravor names the jammed radar as the **AN/APG-73**, a mechanically scanned set, and says the jamming defeated "range, velocity, aspect" and broke the lock — experienced by the crew that launched *after* he landed. Board carries APG-79 but not this | Fravor to Burchett | SNg @ 00:54:38 |
| **H10** | Asked directly whether there is "any indication that Department of Energy is involved in UAP data collection and housing", Grusch answers **"I can't confirm or deny that in a public setting"** and then **"yes"** to whether he could in a secure one. Fravor: "no, I don't know." The board's DOE-custody thread has no sworn item pointing at it | Ogles to Grusch | SNg @ 01:57:41 |
| **H11** | Rep. Ogles states he will personally **"initiate the Holman rule"** against any personnel, programme or agency that denies Congress access | Ogles | SNg @ 01:58:37 |
| **H12** | Grusch on the whistleblower routing failure: PPD-19 or **ICD-120** sends it to the Intel committees, and "there's not a good way" for the ICIG to pass it onward. He **asked** for his information to go to House and Senate **Armed Services** "because there are title 10 equities at play" and there was **no smooth process to do so** | Grusch to Burchett | SNg @ 02:00:07 |
| **H13** | Grusch: he **personally reviewed overhead collection** and other strategic/tactical platform imagery he "could not even explain prosaically", says he has a physics degree, and states his information cut-off is **April [2023]** when he left NGA. He adds that Congress has not seen those reports and he does not know why | Grusch to Moskowitz | SNg @ 01:09:41 |
| **H14** | Grusch: Kirkpatrick told Congress about **~30 individuals** who had come to AARO; **a few of those same people** Grusch had also interviewed, so he could evaluate what they gave AARO | Grusch to Mace | SNg @ 01:12:01 |

### 1d. The one that matters most — a two-witness Vandenberg

**`vandenberg-2003` on the board is sourced entirely to Jeffrey Nuccetelli's written testimony
of 9 September 2025.** At SNg @ 01:03:06–01:03:54, **two years earlier and under oath**,
**Ryan Graves gave Rep. Luna an account of the same class of event**, relayed from a witness who
came to Americans for Safe Aerospace:

- "a large group of **Boeing contractors**" near one of the **launch facilities at Vandenberg**;
- **2003 time frame**, a **~100-yard-sided red square** (caption `100 yard sided uh ready Square` [PHON?]) approached
  **from the ocean** and hovered
  at low altitude over a launch facility for **~45 seconds** before darting off over the
  mountains;
- at "8:45 in the morning";
- a **second set of sightings the same evening, post-sunset**, on base, including **objects
  approaching security guards at rapid speeds**;
- asked whether it was documented, Graves: **yes**, the witnesses "had official documentation and
  records from the event."

**What this is worth, and what it is not.** Graves gives no date beyond "2003 time frame" and
does not name his witness, so I am **not** asserting this is the 14 October 2003 event or that
his witness is Nuccetelli. What is checkable, and worth checking, is exactly that: whether the
2023 and 2025 accounts are one event and one witness or two. The details diverge — Graves says
*one* launch facility, Nuccetelli says *two missile defense sites*; Graves adds the ~45-second
duration, the ~08:45 timing and the same-evening guard approaches, none of which the node
carries. Graves' independent documentation claim is also a separate FOIA hook from Nuccetelli's
"held by AARO and the FBI".

### 1e. Two smaller board-accuracy notes

- **Attribution check.** The board records the SCIF denial as Burchett's ("Members were denied
  access to a SCIF for the hearing, per Rep. Burchett"). In the transcript that sentence falls in
  **Luna's** opening statement at SNg @ 00:11:42, immediately after the chair recognises her, and
  reads "we were even denied access to a classified briefing in a skiff prior to this hearing."
  Auto-captions carry **no speaker labels**, so this is a discrepancy to adjudicate against the
  printed record (CHRG-118hhrg53022), **not** a correction. Burchett may well have said it too.
- The chair opens by naming a 1966 book, `flying saucers serious business`, as what got him
  interested (SNg @ 00:01:30). Frank Edwards published *Flying Saucers — Serious Business* in
  1966; the chair does not name the author, so the attribution is mine and unverified.

---

## 2. ENTITIES

Nothing in these tables is a fact about the world. Each row records the role **the named speaker
assigns** the entity.

### 2a. Contractors and private institutions

| Name | Role the speaker assigns it | File | TS |
|---|---|---|---|
| **EG&G** [CONF] (`EGNG`, `EG`, `egng`) | The spine of both interview files. **Rogers:** prime contractor for **all** of Cape Canaveral Air Force Station — grounds, buildings, roads, traffic lights, the health clinics — and every other contractor there "leased their housing, their support, everything" from it. **Lazar:** recruited and interviewed at "EG&G Special Projects ... at McCarran airport"; his security clearance ran through it | TNt, BEW | TNt @ 00:20:41, 00:21:53, 01:10:54; BEW @ 00:03:23 |
| **EG&G — host narration** (Michels, **not** the witness) | A standalone history the witness explicitly declined to give: founded by MIT's Harold "Doc" Edgerton `Edertton` [PHON?], associate of **Vannevar Bush** `Vanavar` [PHON?]; stroboscopic cameras into the **Manhattan Project**; **AEC** prime contractor and later **DOE**; ran the **Nevada Test Site**; worked "side by side with Los Alamos, Livermore and Sandia"; **held the Q clearances**; ran Area 51 personnel screening, site access, badge office and the commuter flights | TNt | TNt @ 00:22:30–00:31:18 |
| **Martin Marietta** [CONF] | Rogers: leased the specific building he was in at Cape Canaveral from EG&G. He twice stresses it was **separate from Lockheed until 1995** | TNt | TNt @ 00:21:38, 00:45:40 |
| **Lockheed** `Locked`, `Loheed` [PHON?] / **Skunk Works** | Rogers' first-named candidate owner of the craft he says he saw, and his top guess for where the feed came from. His analogy is Have Blue: the airframe carried USAF markings while still contractor-owned | TNt | TNt @ 00:45:44, 00:46:52, 00:57:59 |
| **Northrop** `Northrup` [PHON?] | Rogers' second-named candidate owner | TNt | TNt @ 00:45:44 |
| **Raytheon** `Rathon` [PHON?] | Rogers: "a little bit of a big thing for Rathon by themselves, but ... in partnership with the consortium" | TNt | TNt @ 00:45:44 |
| **Boeing** [CONF] | (a) Rogers names it among Cape Canaveral tenants; (b) **Graves, under oath**, attributes the Vandenberg 2003 sighting to Boeing contractors — see §1d | TNt, SNg | TNt @ 00:22:00; SNg @ 01:03:06 |
| **Bechtel** `Becktell` [PHON?] | Host narration only, in a list of "private entities working on UFO technology" | TNt | TNt @ 00:29:53 |
| **Reynolds Electrical & Engineering Co. (REECo)** `Reynolds Electronics` [PHON?] | Host narration: an EG&G subsidiary named by a 1991 Las Vegas radio caller who claimed he was hired through it to run electricity 3,000 ft underground at a test site. **Second-hand, uncorroborated, and the host says so** | TNt | TNt @ 00:29:53 |
| **Robert Bigelow** [CONF] / **NIDS** [CONF] | Corbell: the person who met Adm. Wilson was "an employee of at the time Robert Bigelow"; NIDS studied Skinwalker Ranch; the $22m went to the "mother program", not to AATIP | BEW | BEW @ 01:11:42, 01:15:01 |
| **Northrop Grumman** `north of Grman` [PHON?] | Host: named by Edgar Fouché as the origin of the TR-3A/B series. **Third-hand** | TNt | TNt @ 01:58:14 |
| **TRW** and **Skunk Works** [CONF] | Michels: crates so labelled appear in *Close Encounters of the Third Kind*, which he offers as evidence Spielberg had sources. **This is film criticism, not a custody claim** | JE1 | JE1 @ 00:27:22 |

### 2b. Government bodies and military units

| Name | Role the speaker assigns it | File | TS |
|---|---|---|---|
| **45th Space Wing** [CONF] | Rogers' command. He says it "owned everything at the Cape" — Patrick AFB, Cape Canaveral AFS, the Eastern Space and Missile Center, "and some other things that we won't be discussing" | TNt | TNt @ 00:04:36, 00:18:21 |
| **45th Medical Group** [CONF] | The subordinate unit; Rogers was Chief of Aerospace Medicine and Chief Flight Surgeon within it | TNt | TNt @ 00:18:56 |
| **Cape Canaveral Air Force Station** [CONF] | Rogers' central structural claim: a facility whose **space-programme cover story absorbs unrelated projects**. "If you put project X in New Mexico they're going to wonder what it is. If you put project X on Cape Canaveral ... oh well it's just related to the space program" | TNt | TNt @ 01:14:31 |
| **AFTAC — Air Force Technical Applications Center** [CONF] | A tenant unit Rogers supported and deployed with to the South Atlantic and South America; he calls it "a whole other story" and does not elaborate | TNt | TNt @ 00:05:07 |
| **9th Strategic Reconnaissance Wing** [CONF] | Another tenant; U-2s | TNt | TNt @ 00:05:07 |
| **DDMS — DoD Manned Space Flight Support Office** `Department of Defense Man Space Support Office` [PHON?] | The office running the astronaut rescue exercises; headed by a **Colonel Shokitis** [UNRESOLVED] | TNt | TNt @ 00:08:04 |
| **DOE** [CONF] | **Grusch, under oath**, will neither confirm nor deny DOE involvement in UAP data collection and housing in open session, and says yes to doing so in a secure one | SNg | SNg @ 01:57:41 |
| **AEC** [CONF] | Host narration only: EG&G as the AEC's prime contractor, "woven into the fabric of the Atomic Energy Commission itself" by the 1950s | TNt | TNt @ 00:24:22 |
| **AARO** [CONF] (`aarro`, `Arrow`, `Aero`) | Named throughout SNg. The board holds this fully | SNg | throughout |
| **NSWC Crane, Indiana** [CONF] | Michels relays a witness account of a deep underground facility there — see §8, lead 4 | JE1 | JE1 @ 00:48:07 |
| **Indian Springs AFAF** [CONF] | Lazar: where he was taken for his post-surveillance debriefing, and where the transcript of his wife's phone calls was produced | BEW | BEW @ 00:55:19 |
| **Tonopah Test Range** `tonopod`, `toenap` [PHON?] / "Area 52" | Lazar and Corbell: the stealth-programme site; Corbell says the hand-geometry readers were used there too, sourced to Tyler Rogoway | BEW | BEW @ 00:04:41, 02:02:15 |

### 2c. Programmes and code names

| Name | Role | File | TS |
|---|---|---|---|
| **"Project Galileo", "Project Sidekick", "Project Looking Glass"** [UNRESOLVED as claims] | Lazar names three S4 side-programmes he says he read one- or two-page overview briefings on: Sidekick for **weapon applications** of the craft, Looking Glass for **effects of the craft on time** ("small distortions ... part of a weapon program"), Galileo unspecified. He immediately adds he does not like discussing them because he has no information on them. **The board's `The Galileo Project` node is Avi Loeb's Harvard programme and is a different thing entirely — do not merge** | BEW | BEW @ 01:50:54 |
| **AAWSAP** `awsap`, `ossap`, `awesap`, `asap` [PHON?] | Corbell: "the mother program", the $22m recipient, distinct from AATIP which he calls "an auxiliary kind of program of military settings" | BEW | BEW @ 01:00:34, 01:16:40 |
| **AATIP** `atip`, `a tip` [PHON?] | As above; Fravor separately says Jay Stratton contacted him in 2009 "unbeknownst to all he was part of the atip program" | BEW, SNg | BEW @ 01:00:34; SNg @ 00:36:12 |
| **Have Blue → F-117** (Rogers says `F-17` throughout) [PHON?/error] | Rogers' worked example of contractor-owned airframes carrying USAF markings before the Air Force buys them | TNt | TNt @ 00:46:12 |
| **Avrocar / Project Y / Project Silverbug** [CONF/PHON?] | **Host narration.** Michels' thesis: the Avrocar at Wright Field was "a cover for something deeper", a funnel to bring in German engineers while serious work went on elsewhere. Rogers' only contribution is "but that was a joke" | TNt | TNt @ 02:03:39–02:07:35 |
| **Immaculate Constellation** [CONF] | Michels: he "figured out" that Elizondo's name was tied to the programme, and that Elizondo testified alongside Shellenberger saying he could not confirm or deny being read in. The board holds an `immaculate-constellation` node | JE1 | JE1 @ 01:47:01 |
| **Skywatcher** `Skywasher` [PHON?] | Named in passing with Jake Barber. Board holds it | JE1 | JE1 @ 00:12:53 |

### 2d. People

| Name | Role the speaker assigns them | File | TS |
|---|---|---|---|
| **Dr. Gregory "Greg" Rogers** [CONF as caption-stable] | The witness of TNt. Retired chief flight surgeon (USAF/NASA); Chief of Aerospace Medicine, 45th Space Wing; senior flight surgeon for the astronaut rescue and recovery team at KSC; flew helicopters and F-16s; retired from DoD **30 April**. Says he has level-one autism and PTSD, and that he disclosed the PTSD pre-emptively because "someone's going to bring it out in a negative way" | TNt | TNt @ 00:04:36, 01:15:26, 01:28:12, 01:29:21 |
| **"the major"** [UNNAMED] | The officer Rogers says showed him the closed-circuit feed, locked the door and closed the blinds, and who said **"We got it from them"**. Rogers had done his flight physical "a year and a half before"; never saw him again | TNt | TNt @ 00:00:07, 00:47:28 |
| **Bob Lazar** [CONF] | The witness of BEW. **Has no node on the board** — he appears only in the prose of seven nodes (`klas-tv`, `eg-and-g`, `l-area51`, `l-las-vegas`, `l-lasvegas`, `george-knapp`, `jeremy-corbell`). A promotion question, not a discovery |  |  |
| **Edward Teller** [CONF] | Lazar's referral chain: met Teller at Los Alamos in **1982** the day Teller lectured there and the local paper front-paged Lazar's jet-engine Honda; years later sent Teller a résumé referencing the meeting; Teller "gave me a reference somebody to contact at EG&G" | BEW | BEW @ 00:01:47–00:03:23 |
| **"Barry"** [PARTIAL — first name only in this transcript] | Lazar's assigned lab partner at S4 under the buddy system; showed him the reactor; told him about the fatal earlier accident and about "the commies" at S4. Lazar has given a surname publicly elsewhere; **this transcript does not, and the board must not supply one from memory** | BEW | BEW @ 00:07:49, 01:24:28 |
| **Dennis Mariani** [CONF as caption-stable, unverified] | Lazar's named supervisor; "kind of a military looking guy"; the go-between who took findings upward; told them test flights were only on Wednesdays; made the final threatening phone call after the broadcast | BEW | BEW @ 00:38:35, 00:46:09, 01:18:53 |
| **Mike Thigpen** `mike fig pin`, `my big pin`, `mike thigpen's` [PHON?] | The clearance investigator Lazar named for 30 years. Corbell claims he located him via Facebook and reverse image search through his children, spoke to him **three times by phone**, that Thigpen **confirmed he did security clearances for the base in 1989 and remembered Lazar**, admitted he had been avoiding Knapp, and nearly went on camera. Corbell also says a friend of Lazar's holds a **handwritten note with Thigpen's signature** left during the clearance canvass | BEW | BEW @ 02:06:14–02:08:54 |
| **Gene Huff** [CONF] | Lazar's friend, present at the desert watch when they were caught | BEW | BEW @ 00:54:15 |
| **John Andrews** [CONF] / **Testors** `testers model corporation` [PHON?] | Lazar: after leaving, he and Andrews reconstructed the craft's dimensions from known-size references and arrived at **52 feet in diameter**. The board's `ben-rich` node already carries Andrews as a model-maker correspondent | BEW | BEW @ 00:35:40 |
| **"Dr. Krangle"** [UNRESOLVED — caption `dr krangle`] | Corbell: came forward on the record to say he was **in security briefings with Lazar** at Los Alamos. **Do not put this name on the board in this spelling.** The other corroborating witnesses, Corbell says, "are still working there" | BEW | BEW @ 02:05:52 |
| **George Knapp** [CONF] | Named in all three UFO files. In BEW he is the recipient of the original taped account, the man who physically took the tape to air, and the one who found the 1982 Los Alamos phone directory after the lab denied Lazar's employment | BEW | BEW @ 00:57:12, 01:17:47, 02:00:00 |
| **Jeremy Corbell** [CONF] | Present throughout BEW as the second guest; makes the Wilson-memo provenance claim in §4 | BEW | throughout |
| **Alfred O'Donnell** [CONF] | Host narration: told George Knapp `George Nap` [PHON?] in 2023 that a saucer was recovered in New Mexico with a live being with humanlike features. Board holds the node | TNt | TNt @ 00:30:54 |
| **Harold Malmgren** `Harold Malgren`, `Malmgrren` [PHON?] | Host narration: presidential adviser to JFK, LBJ, Nixon and Ford; his account is used to tie EG&G to the **Bluegill Triple Prime** test and the "tagalongs". Michels also quotes what he presents as Malmgren's father saying "we called it a tag along" | TNt | TNt @ 00:25:35, 00:26:51, 01:12:01 |
| **Eric Davis** [CONF] and **Adm. Thomas Wilson** [CONF] | Host narration and Corbell: the 2002 meeting, said to have taken place **outside EG&G Special Projects headquarters in Las Vegas** | TNt, BEW | TNt @ 00:30:07; BEW @ 01:10:11 |
| **Randy Anderson** [PHON? — spelling caption-derived] | See §8 lead 4. Michels: Green Beret, NSWC Crane, 2014, deep underground, "off-world/off-planet technology", a device emitting hieroglyphics; had spoken to Greer and to **UAP Gerb** before Michels; critics attack his service record; Michels cites his **DD-214** | JE1 | JE1 @ 00:48:07–00:49:38 |
| **Matthew Brown** [CONF] | Michels: the Immaculate Constellation source; met Shellenberger before Corbell; later tweeted a claim that the White House holds "some proprietary AI that predicts future timelines". Michels flags this as unfollowed-up | JE1 | JE1 @ 01:46:18, 01:47:49 |
| **Jesse Marcel Library**, Montana [CONF] | Rogers: has published an article about him; he was to speak to them by Zoom "on the 19th" | TNt | TNt @ 02:35:05 |
| **International UFO Bureau**, Oklahoma City [CONF] | Rogers discloses he **sits on its board** | TNt | TNt @ 01:16:34 |

---

## 3. DOCUMENTS AND PRIMARY RECORDS NAMED

Anything with a title, number, date or archive that could be independently pulled.

| # | record | named by | pointer |
|---|---|---|---|
| D1 | **Agreement on Measures to Reduce the Risk of Outbreak of Nuclear War**, US–USSR, signed **1971**, registered with the UN, unclassified — with **Article 3**, a "situation two" provision, and **red-line flash message traffic codes declassified in 2013**, held at the **George Washington University National Security Archive**. Grusch's single most pullable citation | Grusch, **under oath** | SNg @ 02:02:01 |
| D2 | **Defense Intelligence Reference Document, "Advanced Space Propulsion Based on Vacuum (Spacetime Metric) Engineering"** — entered into the hearing record by Burchett by unanimous consent. Board already carries this | Burchett, in session | SNg @ 00:05:48 |
| D3 | **Statement for the Record by George Knapp** and **Jeremy Corbell's written statement**, entered by unanimous consent. Board carries both | Burchett | SNg @ 00:05:48 |
| D4 | **NewsNation article and full Grusch interview**, submitted for the record by Luna | Luna | SNg @ 02:01:02 |
| D5 | **10 U.S.C. §119** — congressional oversight of SAPs, DepSecDef waiver authority, Gang of Eight notification. Board carries | Grusch | SNg @ 01:08:10 |
| D6 | **Executive Order 13526** — cited by Grusch to rebut "Above Top Secret". Board carries | Grusch | SNg @ 01:21:48 |
| D7 | **PPD-19** urgent-concern filing, **May 2022**, to the IC Inspector General; and **ICD-120** as the alternate route | Grusch | SNg @ 00:29:36, 01:59:48 |
| D8 | **The 2019 UAP Task Force Security Classification Guide** — Grusch says he helped author it. Board carries | Grusch | SNg @ 01:33:06 |
| D9 | **Vandenberg 2003 documentation** — Graves testifies his witnesses held "official documentation and records from the event". Independent of the Nuccetelli AARO/FBI custody claim | Graves | SNg @ 01:04:02 |
| D10 | **Eglin radar sequence and the manually-taken image** — Gaetz asks they be provided to the committee, subpoenaed if necessary. Board carries; **no evidence it ever happened** | Gaetz | SNg @ 01:44:59 |
| D11 | **Los Alamos internal telephone directory, 1982** — the document that placed Lazar at the lab after LANL denied it | Lazar / Corbell | BEW @ 02:00:03, and repeated in the TNt host narration @ 00:28:31 |
| D12 | **Front-page Los Alamos newspaper story, 1982**, on Lazar's jet-powered Honda, retrievable from archives | Lazar | BEW @ 00:01:47, 02:00:00 |
| D13 | **Handwritten clearance-canvass note bearing Mike Thigpen's signature**, said to be held by a friend of Lazar's | Corbell | BEW @ 02:07:35 |
| D14 | **The Wilson/Davis memo** — Corbell asserts on the record, in 2019, that it is genuine. See §4 | Corbell | BEW @ 01:10:11, 01:34:57 |
| D15 | **Bluegill Triple Prime**, October 1962, high-altitude nuclear test, Marshall Islands — host narration says EG&G crews aboard the filming aircraft. The test itself is a documented event with a documentary record | Michels (narration) | TNt @ 00:25:35 |
| D16 | **Rogers' own book, "We Got It From Them"** — self-described, contains the UFO account plus career material and a chapter on PTSD | Rogers | TNt @ 01:28:46 |
| D17 | **Josh Boswell, UK Daily Mail, 4 May** — the first published Rogers interview; plus a **Ty Roberts** [PHON?] interview for the International UFO Bureau and "Total Disclosure", and the **Chris Lehto** `Chris Leto`, `Le Letto Files` [PHON?] interview that led to this one | Rogers / Michels | TNt @ 01:16:21, 00:03:20 |
| D18 | **Randy Anderson's DD-214** — Michels says he has seen it and that it answers the "not a Green Beret" attacks | Michels | JE1 @ 00:49:34 |

**Two absences worth recording.** Nothing in BEW cites a document number for the S4 briefings
Lazar read; he is consistent that he retained no paper. And nothing in TNt cites any document at
all for the craft Rogers describes — he saw a screen, in a room, for about fifteen minutes, and
the screen carried **no classification marking, no location, no time**, which he says at the time
was the fact that decided him not to report it.

---

## 4. THE STRUCTURAL ARGUMENT

**The three files that argue anything at all argue the same shape from three different distances,
and the shape is custody-by-contractor.** The hearing states it as a legal architecture. Grusch's
account under oath is not that a secret exists but that a **funding and notification path exists
which makes a secret lawful to keep**: appropriated money is misappropriated; contractor
**IR&D** is internal to the firm, so as long as the money is profit or private investment there
is no notification duty at all; SAP and CAP equities move through the **Periodic Program Review**
to named committees while IR&D moves through nothing; DepSecDef can waive congressional reporting
under 10 U.S.C. §119 with only the Gang of Eight notified; and contractors have **no obligation
whatsoever** to report a UAP encounter. His remedy claim is that nothing sits above SAP —
E.O. 13526 sets the ceiling, "Above Top Secret" is a misnomer — so the failure is not
classification law but the **access-adjudication authority**, exercised by "a group of career
senior executive officials" who are "both in and out of government". The oversight gap he
describes most concretely is not about UAP at all: the ICIG has no clean route to send a Title 10
matter to the Armed Services committees, so his own complaint reached the wrong committees.

**Lazar's account is the same argument told from inside a cell, and its content is the
compartment rather than the craft.** He describes a project deliberately split "into many
different pieces", a two-man buddy system in which he could exchange ideas with exactly one
person, one-or-two-page overview briefings on adjacent projects issued only so a worker would
know an adjacent project *exists*, and a supervisor as the sole upward channel. He is explicit
that this is the failure mode, not the safeguard: "science is based on free discussion ...
everybody becomes stagnant", and he reads his own recruitment as an act of desperation after the
compartments produced a bottleneck. Corbell overlays the periodicity claim — that the material is
worked, shelved when material science runs out, and taken out again "every eight or ten years" —
and attaches it to the Wilson memo's admiral-denied-access story, drawing the same conclusion the
hearing draws by a different route: **it is held privately because the government "is just so
leaky."**

**Rogers argues the weakest and most specific version, and it is the one about cover stories
rather than compartments.** His structural point is not that a saucer exists but that **Cape
Canaveral launders classification**: put a project in New Mexico and people ask what it is; put
the same project on Cape Canaveral and "they say, oh well, it's just related to the space
program." He pairs this with a Pen-and-Teller misdirection thesis — a company's publicised
marvel is "to get the people's attention so they don't look at this other thing that they're
spending all the money on" — and with an ownership argument drawn from his own service:
umbilicals feeding power and control into the craft mean it is immature, and immature means
**contractor-owned, not in the Air Force inventory**, exactly as Have Blue wore USAF markings
while belonging to Skunk Works. He is emphatic that access is a two-key problem, clearance plus
need-to-know, and that seniority is not the same as access: "a tech sergeant is read into a
program, whereas the major is not." He also states plainly, on his own decision not to report,
that a reporting decision was a **career decision** — the same phenomenon Graves and Gaetz put on
the record for pilots at SNg @ 01:44:04.

---

## 5. THE 1940s–1980s THREAD — Thomas Townsend Brown, electrogravitics, the Manhattan lineage

**This thread is PRESENT, and it is the single most board-relevant thing in the group.** Two
qualifications up front, and they matter:

1. **Almost all of it comes from the host, not the witnesses.** In TNt the entire EG&G/AEC/
   Manhattan history is Jesse Michels' inserted narration and his own questions; Dr. Rogers'
   contribution is one sentence, "EGNG is all over the military", plus a refusal to speculate
   ("EGNG is a whole story unto itself, and I'm not going to touch that one," TNt @ 00:22:30).
   The Avrocar/Townsend Brown passage at TNt @ 02:03:39–02:08:45 is Michels talking almost
   uninterrupted; Rogers' only interjections are "but that was a joke" and a helicopter
   ground-effect aside.
2. **In the hearing (SNg) the thread is ABSENT.** No Townsend Brown, no electrogravitics, no AEC,
   no Manhattan Project, no early aerospace contractor by name. The furthest back anyone goes is
   Grusch's one-word "1930s" (H1) and his "the recoveries predate a lot of our advanced programs"
   (H5). **This is a clean negative and should be recorded as one.**

### 5a. What is actually said

| item | who | pointer |
|---|---|---|
| **Thomas Townsend Brown** `towns and brown`, `Towns and Brown` [PHON? — the caption reliably splits the surname into two words, so a grep for "Townsend" will MISS every occurrence] — described as "this anti-gravity amazing anti-gravity inventor", lifelong obsession with time travel, lived in Pasadena, died **1985**, "proved his experiment" in **1957**, and wanted his work powered by nuclear reactions because he needed megavolt-range electricity | Michels | JE1 @ 00:28:34–00:29:26; TNt @ 02:05:02, 02:08:45 |
| **The Biefeld–Brown effect** `Biffield Brown`, `Bfield Brown` [PHON?] — offered twice as the terrestrial alternative explanation for what Rogers saw, i.e. "maybe just some extremely exciting human propulsion breakthrough" | Michels to Rogers | TNt @ 01:46:37, 02:01:35 |
| **Agnew Bahnson** `Agny Bonson` [PHON?] — the North Carolina figure said to have written in diaries later found that "the space brothers came to me and said get me in touch with Townsend Brown ... I want to build a spaceship", and to have then hired Brown | Michels | TNt @ 02:04:49 |
| **Institute of Field Physics, University of North Carolina at Chapel Hill** [CONF as an institution] under **Bryce DeWitt** `Bryce Dit` [PHON?] — the theoretical-physics group Michels says Wright Field was simultaneously sponsoring while running the Avrocar | Michels | TNt @ 02:04:45 |
| **Joshua Goldberg** `Josh Goldberg` [PHON?] — named as running a "dedicated theoretical physics group" at Wright Field | Michels | TNt @ 02:05:02 |
| **Avrocar / Project Y / Silverbug**, Wright Field, "the 50s and 60s"; **John Frost** [CONF] running it in Canada; Michels asserts "British Aircraft and CIA were co-running this thing"; **Henri Coandă** `Henry Kanda` [PHON?] as a consultant on Project Y; **Richard Miethe** `Richard Meita` [PHON?] and **Viktor Schauberger** `Victor Shawberger` [PHON?] as recruitment targets; a "**Hansler**" [UNRESOLVED] named as whom they had worked under | Michels | TNt @ 02:03:39–02:07:35 |
| **Die Glocke / "the German bell"** `DLA` [PHON? — the caption renders it as an acronym, which will defeat a grep] and **spinning mercury**, tied by Michels to the Vedic vimanas and to **Edgar Fouché** `Edgar Fuche`, `Fuchsche` [PHON?] on the TR-3A/B. Michels states that **Kirk McConnell** [CONF], a Senate intelligence-committee staffer, raised the Die Glocke material with him "in your chair" | Michels | TNt @ 01:58:14–01:58:49 |
| **Nick Cook** [CONF] — named for his mid-century anti-gravity investigation | Michels | TNt @ 01:58:51 |
| **Aztec, March 1948** — an unnamed first-hand witness said to have worked at Wright Field on the Aztec-recovered craft, which was **hooked to extremely high-powered transformers and went translucent when powered up**. Michels ties this to Rogers' own description of an electrically charged craft fed by umbilicals | Michels | TNt @ 02:08:06 |
| **Edward Teller → EG&G**, and the **"Q clearance ... civilian top secret"** framing | Lazar, first-hand | BEW @ 00:02:24, 00:47:45 |
| **Russian scientists at S4 in the late 1980s** — Lazar says he did not meet them but Barry "would talk about the commies that were there"; that there was cooperation "even exchanging some ideas on nuclear weapons and EMP tests"; and that after "a big discovery" made between his visits, by a group that was not his, "the Russians were never allowed back on the base after that" | Lazar, second-hand via Barry | BEW @ 01:23:43–01:25:33 |
| **The archaeological-dig hint** — Lazar, hesitantly and explicitly at the limit of his memory, says something Barry said "left a seat in my mind ... at least one of them was part of an archaeological dig", i.e. one of the nine is ancient. He immediately says he cannot be sure what was said | Lazar | BEW @ 01:14:15 |

### 5b. Why this matters to the board specifically

Cross-checked against all 964 nodes and 2,172 edges:

- **"Thomas Townsend Brown" is ABSENT from the board.** So are **Biefeld**, **Agnew Bahnson**,
  **Bryce DeWitt**, **Joshua Goldberg**, **John Frost**, **Henri Coandă**, **Viktor Schauberger**,
  **Richard Miethe**, **Die Glocke**, **Nick Cook**, **Project Silverbug** and **Bluegill Triple
  Prime**.
- **"electrogravitics" appears exactly twice on the board**, both inside the To The Stars Academy
  node, as the name of one of TTSA's three announced 2017 divisions. There is no
  Townsend-Brown-era thread at all.
- **`Avrocar` does appear**, but the Institute-of-Field-Physics candidate matched only the board's
  `Propulsion & Field Physics` **domain label** — a false positive, not a node.
- **Edgar Fouché is already in board prose** (`gerb-sandia-investigation`,
  `manhattan-project-2--sandia`), so the TR-3B/Northrop Grumman claim is a promotion question,
  not a discovery.
- **`eg-and-g`, `alfred-o-donnell`, `manhattan-project-2`, `vannevar-bush`-in-prose and
  `l-groom-lake` already exist and are strong.** The TNt narration adds nothing to them that they
  do not already say better, **except** Bluegill Triple Prime and REECo.

**So: the honest reading is that this group supplies a genuinely new 1940s–1960s electrogravitics
lead-set, sourced entirely to a podcaster's narration and therefore Tier 3 at best in its present
form — but every name in it is a real, checkable archival subject** (Bahnson's papers, DeWitt's
papers, the UNC Institute of Field Physics records, the Avro Canada Project Y files) rather than a
claim that can only be adjudicated by asking the government.

---

## 6. TESTIMONY UNDER OATH vs CLAIMS IN AN INTERVIEW

**Only SNg is sworn.** Graves, Grusch and Fravor stood, raised their right hands and answered in
the affirmative at SNg @ 00:23:49. Everything in BEW, TNt and JE1 is a podcast statement.

The distinction is not cosmetic here, and three things in the files sharpen it:

| | sworn (SNg) | unsworn (BEW / TNt / JE1) |
|---|---|---|
| **What raises the floor** | Statements are made under 18 U.S.C. §1001 exposure, in a transcript printed by GPO. Grusch adds a second constraint the others lack: **DOPSR** `dobster` [PHON? — Defense Office of Prepublication and Security Review] pre-cleared what he could say, and he states he is "required by law to do that ... or I go to jail" (SNg @ 01:02:45) | Nothing. Rogers is a retiree describing a 1992 event from memory; Lazar is describing 1988–89 events with a migraine he references six times and repeatedly loses his train of thought (BEW @ 00:19:25, 00:26:03, 00:29:55) |
| **What lowers the ceiling** | The most load-bearing answers are explicitly **withheld**: names, facilities, SAP identities, whether imagery is of crash sites, whether contact was made, and where to look — all deferred to a SCIF that the record shows never convened | Nothing is withheld for classification, but nothing is constrained either. Corbell's assertions about the Wilson memo and Thigpen are the clearest case: they are more specific than anything in the hearing and carry no verification mechanism at all |
| **Hearsay structure** | Grusch is explicit that he is a **relay**: "I am speaking to the facts as I have been told them" (SNg @ 00:31:01), based on interviewing 40+ witnesses, and he says he had those witnesses file **their own** protected disclosures — which is what makes the chain more than hearsay | Rogers is **first-hand** on the screen but **second-hand** on everything the screen means: the entire "We got it from them" content is one sentence from one unnamed major. Lazar is first-hand on the reactor and the flight test, second-hand via Barry on the earlier death, the Russians and the archaeological dig |

**One item crosses the line in an interesting direction.** Rogers says he came forward
**specifically to convert Grusch's hearsay into first-hand testimony** — "I've got a 6:00
covered", and "next time David Grusch speaks, he can say ... Dr. Greg Rogers testified to it"
(TNt @ 01:26:01, 01:27:10). **He has not testified.** He gave a podcast interview and a
Daily Mail interview. That gap is the whole evidentiary point, and it should be recorded as the
gap it is rather than smoothed over.

---

## 7. INTERNAL CONTRADICTIONS AND FACTUAL ERRORS

**In the hearing (SNg):**

| # | what | pointer |
|---|---|---|
| C1 | **The chairman and Rep. Moskowitz both say the NDAA "of 2022" created AARO.** AARO was established by the **FY2023** NDAA (Pub. L. 117-263 §6802, Dec 2022); the FY2022 NDAA §1683 created AOIMSG. The board's own `ndaa-fy2023-sec-6802` edge has this right. A real, checkable imprecision spoken twice from the dais | SNg @ 00:02:36, 00:21:38 |
| C2 | **Rep. Ocasio-Cortez says the UAP Task Force was "created in the 2020 NDAA."** UAPTF was stood up by a DepSecDef memo in August 2020; the statutory instrument usually cited is the FY2021 IAA report language. Loose attribution, worth adjudicating against the record | SNg @ 01:24:55 |
| C3 | **Rep. Luna characterises Kirkpatrick's 19 April testimony as saying "he did not find any evidence of uaps."** Kirkpatrick's actual statement, quoted correctly by Rep. Mace later in the same hearing, was "no credible evidence ... of extraterrestrial activity or off-world technology." **The hearing contradicts itself on what the AARO director said**, and the accurate version is the one the board already quotes | SNg @ 01:01:35 vs 01:11:06 |
| C4 | **Rep. Burlison: "we are billions of light years away from any other system."** The nearest star system is 4.2 light years away. He builds his incredulity argument on this | SNg @ 01:37:04 |
| C5 | Grusch says "from 2021 to 2025 — or, excuse me, 2023" of his NGA tenure. **A self-correction, not an error**, recorded so a later pass does not mistake it for one | SNg @ 00:29:05 |
| C6 | Fravor: "the last what now 19, 16 years, 17 years" in the private sector. Caption garble; no substantive claim | SNg @ 01:51:05 |

**In BEW (Lazar / Corbell):**

| # | what | pointer |
|---|---|---|
| C7 | **Lazar dates the first synthesis of element 115 to "2004, Darmstadt, Germany"** `durhamstat` [PHON?], four atoms, 220 ms. Element 115 was first reported in **2003 at Dubna (JINR), Russia**, by a Russian–American team; the German centre (GSI, Darmstadt) figures in later confirmation. **A checkable factual error at the centre of his best-known corroboration claim** | BEW @ 00:25:47 |
| C8 | **Corbell gives three mutually inconsistent dates for the Wilson memo within four minutes**: "the document is from 2001", then "this is in 2002", then "they meet at EG&G special projects in **1989**". The board dates the meeting **16 October 2002** and the surfacing to 2019, which settles it — but the inconsistency is in the transcript and should be recorded | BEW @ 01:10:11, 01:15:01 |
| C9 | **The Operation Paperclip exchange is confused and wrong.** Corbell: "this was before Operation Paperclip became public", dated to "98"; then "actually it's about Russia, not Germany". Paperclip was German, and was publicly known decades before 1998. Lazar does not correct him and the exchange trails off | BEW @ 01:23:43 |
| C10 | **Rogan's Kaczynski claim** — that he "was part of the Harvard LSD studies", "proven" — is wrong; the Murray experiments were not LSD studies. Marginal to the subject but it is a factual assertion made as established | BEW @ 01:42:22 |
| C11 | Lazar says "it was 88 and 89 when I was there", after the interviewer confuses 1982 (Los Alamos) with the S4 period. **Resolved in the transcript**, recorded so it is not mis-flagged later | BEW @ 00:26:12 |

**In TNt (Rogers / Michels):**

| # | what | pointer |
|---|---|---|
| C12 | **Rogers says the aircraft lost searching for Flight 19 was a "PBY".** It was a **PBM Mariner**. Small, but it is in the part of his account he presents as insider knowledge from Flight Ops personnel | TNt @ 00:10:56 |
| C13 | **Rogers says "F-17" consistently** where he plainly means the **F-117** — he names Have Blue as its demonstrator in the same breath. Either a speech habit or a dropped digit in the captions; **do not quote him as saying F-17** | TNt @ 00:46:12, 02:02:36 |
| C14 | **Rogers: the Avrocar "couldn't get out of ground effect. That's the same thing that happened with Vanguard."** Vanguard was a launch vehicle; ground effect is not its failure mode. Probably a slip for another programme | TNt @ 02:03:39 |
| C15 | **Michels lists Malmgren's presidents twice and gets it wrong the first time** — "JFK, Nixon, Kennedy and Ford" — then corrects to "JFK, LBJ, Nixon and Ford" | TNt @ 01:12:09 |
| C16 | **Michels says Wilson was "head of J2 Joint Chiefs" in "1997"**; elsewhere in the same file the meeting is dated 2002. Wilson's DIA directorship ran 1999–2002. The 1997 date is loose | TNt @ 01:10:32 |
| C17 | **A dating problem in Rogers' own framing.** He says the event was 1992 and that he came forward after "almost 25 years"; but he also says the trigger sequence was the 2017 NYT article and then Grusch's 2023 testimony, and that he retired on 30 April before speaking. 1992→now is more than 30 years. Minor, but his own interval arithmetic does not close | TNt @ 01:15:42 |

**In JE1:** no structural claims are made that could contradict; see §9.

---

## 8. THE TOP 10 INDEPENDENTLY CHECKABLE LEADS

Ranked by *what a check would settle*, not by how interesting the claim is.

| # | lead | what would verify it |
|---|---|---|
| **1** | **The 1971 US–USSR nuclear-war-risk agreement, Article 3 and the 2013-declassified red-line traffic** (D1/H2). Grusch's only sworn citation to a document a researcher can pull without anyone's permission | The treaty text is public and UN-registered. Search the **National Security Archive** at GWU for the 2013 release of Article 3 red-line flash-message procedures, confirm whether "situation two" is a real provision, and then test Grusch's actual claim — that specific incidents invoked it. **The board has zero mentions of this agreement.** Highest ratio of checkability to current board coverage in the whole group |
| **2** | **Graves' sworn 2003 Vandenberg account vs Nuccetelli's 2025 account** (§1d) | Read the two hearing transcripts side by side (CHRG-118hhrg53022 and the 9 Sep 2025 record). Adjudicate: one event or two, one witness or two. Then pursue Graves' distinct claim that his witnesses held official documentation — a separate FOIA target from "held by AARO and the FBI" |
| **3** | **Thomas Townsend Brown / Agnew Bahnson / Institute of Field Physics / Bryce DeWitt** (§5) | Entirely archival and requires no government cooperation: UNC-Chapel Hill's Institute of Field Physics records, the Bahnson papers, DeWitt's papers, and the Wright Field sponsorship trail. **Note the grep trap: the captions render the surname as two words, `towns and brown`.** Verify the diary quotation before it is repeated anywhere |
| **4** | **"Randy Anderson" = the board's initialed witness "RA"** (JE1 @ 00:48:07). The board's `off-world-technologies-division` node names a Green Beret "identified only as 'RA'", NSWC Crane, 2013–2015, deep underground, a device projecting symbology, sourced to UAP Gerb, 17 July 2024. The JE1 account matches on **five** independent points: Green Beret, NSWC Crane Indiana, 2014, off-world/off-planet technology division, an object emitting symbology — and Michels says the man went to **UAP Gerb** before him | Michels never says "RA", so the identification is a strong inference, not a fact. Check the UAP Gerb episode of 17 July 2024 and Michels' own published interview for a full name, then verify the spelling. **This name must not reach the board in the caption spelling until that is done** |
| **5** | **Mike Thigpen** [PHON?] and the handwritten clearance-canvass note (D13) | Corbell claims three phone calls in which Thigpen confirmed he did clearances for the base in 1989 and remembered Lazar, plus a physical document held by a named third party. Both are testable. This is the strongest **corroborating** lead in BEW because it does not depend on Lazar |
| **6** | **Dr. Gregory Rogers' service record** (§2d) | Every element is a matter of public or FOIA-able record: Chief of Aerospace Medicine, 45th Space Wing; senior flight surgeon for the KSC astronaut rescue and recovery team; DoD retirement 30 April; board membership of the International UFO Bureau; the Jesse Marcel Library article. **He is entirely ABSENT from the board.** Establishing the credential is separable from, and prior to, assessing the 1992 claim |
| **7** | **Bluegill Triple Prime, October 1962, and EG&G's filming role** (D15) | The test is documented in the atmospheric-test record. What needs checking is the narration's specific claim that EG&G crews were aboard the filming aircraft, and whether "tagalong" is an attested contemporary term or a retrospective coinage. **ABSENT from the board**, and it would connect the existing `eg-and-g` node to the nuclear-test record with a dated event |
| **8** | **Grusch's "recoveries predate a lot of our advanced programs"** (H5) and **"1930s"** (H1) | Both are sworn, both are absent from the board, and together they are the only place in the hearing where the legacy-programme chronology is stated on the record. Verify the exact wording against CHRG-118hhrg53022 before quoting — the captions are unreliable at both points |
| **9** | **Alfred O'Donnell's 2023 statement to George Knapp** (§2d) | The board already carries the `alfred-o-donnell` node. The TNt narration adds a **2023** date to the Knapp conversation. Check that date against Knapp's own published account; a firmer date on an EG&G general manager's custody statement is worth having |
| **10** | **Reynolds Electrical & Engineering Co. as an EG&G subsidiary** (§2a) | The corporate relationship is a matter of public contracting record and is checkable in minutes. The 1991 radio-caller story attached to it is **not** checkable and should be left where it is. **ABSENT from the board**, and REECo is a real Nevada Test Site prime |

**Deliberately not on this list:** anything that can only be settled by asking the government to
open a compartment. Grusch's names, facilities and SAP identities are all withheld to a SCIF that
never convened; Lazar's nine craft, element 115 and Zeta Reticuli are unfalsifiable as stated;
Rogers' 1992 feed carried no identifying marks by his own account.

---

## 9. FILE JE1 (`JE1oM89dpBc`) — a thin file, said plainly

Roughly the first 55 minutes are a UFO conversation between Jesse Michels and the musician Flying
Lotus; **the remaining 70 minutes are about music, film-making, David Lynch and hip-hop
production** and contain nothing structural. Flying Lotus is a fan, not a witness — he says so
("I've never seen anything", JE1 @ 00:52:18) — and his most-quoted contribution is that the
"Skinny Bob" video is obvious CGI.

Three things justify its inclusion at all, and only three:

1. **The "Randy Anderson" identification** (lead 4) — genuinely valuable.
2. **The Townsend Brown material** at JE1 @ 00:28:34–00:29:26, which is where Michels states the
   Brown biography he only alludes to in TNt: Pasadena, died 1985, the 1957 experiment, the
   megavolt power requirement.
3. **A dated provenance datum on the Wilson memo**, from BEW rather than JE1, recorded here
   because it sits with the same cluster: Corbell states on the record in 2019 that he knows the
   memo is real **because of Dr. Edgar Mitchell** — "that's how I know; I don't want any
   journalists thinking I got it from anywhere else" (BEW @ 01:35:03). The board's Davis node
   already says the notes "surfaced in 2019 among the papers of the late Edgar Mitchell." The two
   agree, and Corbell's version is a **named person, dated, on camera, in the same year**. There
   are currently **zero** mentions of Rogan or of a Corbell–Mitchell provenance link on the board.

Everything else in JE1 — Ross Coulthart's buried-UFO claim, Eric Hecker, Jaime Maussan's tridactyl
mummies, Steven Greer, the Art Bell caller audio, Matthew Brown's "White House crystal ball"
tweet — is second-hand commentary on claims the board already holds or has deliberately excluded.
**None of it is worth a research pass on the strength of this file.**

---

## 10. CORRUPTION WATCHLIST

Every flagged name, with the raw caption and my confidence. **The right-hand column is the only
thing that matters: it says what may be written down.**

### 10a. UNRESOLVED — must not reach the board in this spelling

| raw caption | file @ TS | note |
|---|---|---|
| `dr krangle` | BEW @ 02:05:52 | A corroborating witness who "came forward" on Lazar's Los Alamos security briefings. No reconstruction attempted. **Blocking: this is a claim about a named living person.** |
| `Colonel Shokitis` | TNt @ 00:08:04 | Head of DDMS in Rogers' account. Peripheral |
| `Hansler` | TNt @ 02:07:19 | The German figure Miethe and Schauberger are said to have worked under. Could be several people; do not guess |
| `TLI` (in "Dougway proving grounds or TLI") | TNt @ 00:58:36 | A facility name Rogers offers as a possible craft location. Unrecoverable from context |
| `modata exercises` | TNt @ 00:08:04 | The astronaut bail-out exercise name |
| `Ty Roberts` | TNt @ 01:16:34 | Interviewer for the International UFO Bureau / "Total Disclosure". Plausible as spelled but unverified |
| `Randy Anderson` | JE1 @ 00:48:07 | **Not unresolved as a reconstruction — the caption is clean — but unverified as a spelling, and it names a living person making a criminal-adjacent claim.** Treat as blocking until lead 4 is run |

### 10b. PHON? — reconstruction offered, treat as a search string

| my reconstruction | raw caption(s) | file @ TS |
|---|---|---|
| Rep. Glenn **Grothman** | `Rothman`, `groffman` | SNg @ 01:24:55, 02:10:59 |
| Rep. Tim **Burchett** | `burchard`, `Bircher`, `Merchant`, `Burton` | SNg, throughout |
| Rep. Matt **Gaetz** | `getza`, `Gates` | SNg @ 00:00:03, 01:21:40 |
| Rep. Eric **Burlison** | `Burleson` | SNg @ 00:00:03 |
| Rep. Andy **Ogles** | `ogles`, `drawless` | SNg @ 01:55:17, 01:58:40 |
| Rep. Nancy **Mace** | `Ms Mason` | SNg @ 01:45:07 |
| **David Grusch** | `grush`, `gresh`, `garoosh`, `garage`, `Crush`, `grosh`, `Gresham`, `garoosh`, `Gush` | all four files |
| Cdr. David **Fravor** | `fravor`, `favor`, `fraber`, `freyjer`, `Fiverr`, `braver`, `frever` | SNg, BEW |
| **Ryan Graves** | `Ryan fobs Graves` — the middle element is unverified and should be dropped, not reproduced | SNg @ 01:24:55 |
| **DOPSR** (Defense Office of Prepublication and Security Review) | `dobster`, `DOD pre-publication and Security review` | SNg @ 01:02:45 |
| **IR&D** | `irad`, `irap`, `ired`, `I read programs` | SNg @ 01:08:58 ff |
| the **Holman Rule** | `Holmen rule` | SNg @ 01:58:37 |
| Warning Area **W-72** | `morning area whiskey 72` | SNg @ 00:26:26 |
| the **Kármán line** | `Carmen line` | SNg @ 00:27:37 |
| **VACAPES** | `vacapes` | SNg @ 01:33:59 |
| **range fouler** report | `range Fowler report` | SNg @ 01:31:49 |
| **John Ratcliffe** | `John Radcliffe` | SNg @ 00:09:28, 00:20:31 |
| **Ralph** Blumenthal | `Rob Blumenthal` — the caption gives the wrong first name | SNg @ 00:36:45 |
| Leslie **Kean** | `Leslie Keane`, `Leslie Kane` | SNg @ 00:36:45, 00:55:04 |
| **To The Stars Academy** | `two stars Academy` | SNg @ 00:36:45 |
| **SASC** | `SAS` | SNg @ 01:27:44 |
| **Carrier Air Wing 11** | `carrier airing 11` | SNg @ 00:33:16 |
| **DepSecDef** | `depth sect deaf` | SNg @ 00:31:01 |
| **EG&G** | `egng`, `EGNG`, `eg g`, `EG` | BEW, TNt |
| **Tonopah** Test Range | `tonopod`, `toenap` | BEW @ 00:04:41, 00:37:10 |
| **Q clearance** | `queue clearance` | BEW @ 00:47:49 |
| **moscovium** | `muscovium` | BEW @ 00:25:47 |
| **Darmstadt**, Germany | `durhamstat germany` — *and see error C7: the first synthesis was Dubna, not Darmstadt* | BEW @ 00:25:47 |
| **Identimat** (hand-geometry reader) | `identity mats` | BEW @ 02:03:09 |
| **Testors** model company | `testers model corporation` | BEW @ 00:35:40 |
| **AAWSAP** | `awsap`, `ossap`, `awesap`, `asap` | BEW @ 01:00:34 |
| **AN/SPY-1** radar | `spy 1 radar` | BEW @ 01:02:45, 01:53:20 |
| **Tyler Rogoway** | `tyler rogoway` — clean caption, unverified spelling | BEW @ 02:02:17 |
| Harold **Edgerton** | `Doc Edertton` | TNt @ 00:23:01 |
| **Vannevar** Bush | `Vanavar Bush` | TNt @ 00:23:01 |
| Harold **Malmgren** | `Harold Malgren`, `Malmgrren` | TNt @ 00:25:35, 01:12:01 |
| **REECo** / Reynolds Electrical & Engineering | `Reynolds Electronics` | TNt @ 00:29:53 |
| George **Knapp** | `George Nap` | TNt @ 00:30:54 |
| **Lockheed** | `Locked`, `Loheed` | TNt @ 00:21:38 |
| **Raytheon** | `Rathon` | TNt @ 00:22:00 |
| **Northrop** | `Northrup` | TNt @ 00:45:44 |
| **Bechtel** | `Becktell` | TNt @ 00:29:53 |
| **Livermore** | `Liverour` | TNt @ 00:24:49 |
| **Beale** AFB | `Beal Air Force Base` | TNt @ 00:09:54 |
| John Young and Robert **Crippen** | `Young and Krippen` | TNt @ 00:09:54 |
| **Chris Lehto** / Lehto Files | `Chris Leto`, `Le Letto Files` | TNt @ 00:03:52 |
| **Erich von Däniken** | `Eric von Donakin` | TNt @ 01:17:16 |
| **Rhine** River valley | `Ry River Valley` | TNt @ 01:21:44 |
| Thomas **Monheim** (IC IG) | `Thomas Mannheim` | TNt @ 01:27:25 |
| **Thomas Townsend Brown** | `towns and brown`, `Towns and Brown` | TNt @ 02:05:02; JE1 @ 00:28:34 |
| the **Biefeld–Brown** effect | `Biffield Brown`, `Bfield Brown` | TNt @ 01:46:37, 02:01:35 |
| **Agnew Bahnson** | `Agny Bonson` | TNt @ 02:04:49 |
| **Bryce DeWitt** | `Bryce Dit` | TNt @ 02:04:45 |
| **Joshua Goldberg** | `Josh Goldberg` | TNt @ 02:05:02 |
| **Henri Coandă** / Coandă effect | `Henry Kanda`, `kanda effect` | TNt @ 02:07:19 |
| **Viktor Schauberger** | `Victor Shawberger` | TNt @ 02:07:19 |
| **Richard Miethe** | `Richard Meita` | TNt @ 02:06:51 |
| **Die Glocke** | `DLA`, `German bell` | TNt @ 01:58:14 |
| **Edgar Fouché** | `Edgar Fuche`, `Edgar Fuchsche` | TNt @ 01:58:14 |
| **Northrop Grumman** | `north of Grman` | TNt @ 01:58:14 |
| **Göbekli Tepe** | `Gabbec`, `Templey` | TNt @ 02:00:26 |
| the **Antikythera** mechanism | `antic theorem mechanism` | TNt @ 02:00:26 |
| **Aristarchus** | `Aristarkus` | TNt @ 02:17:53 |
| **Nick Bostrom** | `Nick Bostonramm` | TNt @ 01:53:38 |
| **Alice Coltrane** | `Alice Col Train` | JE1 @ 00:00:36 |
| **Luis Elizondo** | `Lou Alzando`, `louisando`, `lewd` | JE1 @ 00:03:04; BEW @ 00:36:06 |
| **Ross Coulthart** | `Ross Khart`, `Ross Kohhard`, `Ross Colter`, `Ross Cohart` | JE1 @ 00:12:53 ff |
| **Jaime Maussan** | `Haimeme Mousan`, `Haime` | JE1 @ 00:11:00 |
| **John Greenewald** | `John Greenwald` | JE1 @ 00:06:19 |
| **Michael Shellenberger** | `Shelonburgger`, `Michael Shaenberger` | JE1 @ 01:46:18 |
| **Diana Walsh Pasulka** | `Diana Pulka` | JE1 @ 00:35:00 |
| **Paul Bennewitz** | `Paul Benowitz` | JE1 @ 00:35:00 |
| **Ariel School** | `aerial school` | JE1 @ 01:49:16 |
| **Rick Strassman** | `Rick Straman` | JE1 @ 00:36:30 |
| **Denis Villeneuve** | `Denny Villanu` | JE1 @ 00:32:34 |
| **Garry Nolan** | `Gary Nolan` | JE1 @ 00:28:04 |
| **Christchurch** earthquake | `Christ Church earthquake` | JE1 @ 00:04:49 |

### 10c. CONF — caption-stable and matching a well-attested subject

Ryan Graves · David Fravor · David Grusch · Sean Kirkpatrick · Glenn Grothman · Robert Garcia ·
Jamie Raskin · Alexandria Ocasio-Cortez · Jared Moskowitz · Anna Paulina Luna · Andy Biggs ·
James Comer · Nick Langworthy · Maxwell Frost · Alex Dietrich · Jay Stratton · Chad Underwood
(named only as "Chad", BEW/SNg — treat the surname as supplied by the board, not the transcript) ·
George Knapp · Jeremy Corbell · Tom DeLonge · Chris Mellon · Steve Justice · Helene Cooper ·
Bill Nelson · Edward Teller · Robert Bigelow · NIDS · Skinwalker Ranch · Harry Reid ·
Adm. Thomas Wilson · Eric Davis · Edgar Mitchell · Alfred O'Donnell · Kirk McConnell ·
Nick Cook · John Frost · Martin Marietta · Boeing · Papoose Lake · McCarran · Janet flights ·
Indian Springs AFAF · Los Alamos · Sandia · AFTAC · 45th Space Wing · Cape Canaveral AFS ·
Patrick AFB · Eglin AFB · Dugway Proving Ground · Groom Lake · Wright-Patterson ·
Barry Goldwater Range · Luke AFB · NSWC Crane · VFA-11 "Red Rippers" · VFA-41 "Black Aces" ·
NAS Oceana · USS Nimitz · USS Princeton · AN/APG-73 · AN/APG-79 · E-2 · Mick West ·
James Fox · Art Bell · Steven Greer · Jake Barber · Chris Bledsoe · Barney Hill · Mike Pompeo ·
Julian Assange · Jesse Marcel Library · International UFO Bureau · Josh Boswell · Kip Thorne ·
LIGO · Virgo · Marshall McLuhan · Carl Sagan · Boston Dynamics.

---

## 11. WHAT IS THIN — stated plainly

- **JE1 is thin.** See §9. Three usable items in 127 minutes.
- **TNt's structural content is the host's, not the witness's.** Rogers' own testimony is one
  fifteen-minute event in 1992 with no document, no location, no classification marking and one
  sentence of interpretation from an unnamed major. Everything about EG&G, the AEC, the Manhattan
  Project, Townsend Brown and the Avrocar is Jesse Michels narrating over him, and twice Rogers
  actively declines to endorse it.
- **BEW adds little to the board's existing Lazar prose except detail and colour.** The genuinely
  new items are narrow: the Teller referral chain, the Q-clearance framing, the Russians at S4,
  the Identimat, the three named side-projects and the archaeological-dig hint — and the last of
  those is offered by Lazar himself as an unreliable memory.
- **SNg is the opposite: dense, sworn, and mostly already on the board.** Fourteen genuine gaps in
  a 138-minute hearing the board has worked hard on is a *good* result for the board, not a poor
  one for the transcript. The Vandenberg finding (§1d) and the 1971 agreement (H2) are the two
  worth a research pass; the rest are additions to an already-strong node.
- **No file in this group produces a new event, a new contractor relationship, or a new custody
  claim that the board does not already hold in some form** — with the single exception of the
  Townsend Brown / electrogravitics lead-set in §5, which is entirely absent from the board and
  entirely unsourced beyond one podcaster's narration.
