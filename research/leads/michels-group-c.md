# Video-transcript corpus — structural extraction, group C (five files)

**Extracted:** 30 August 2026. **Source:** the cached transcripts under `research/.transcripts/`
(gitignored, not committed, not published).

**Status of everything below: UNVERIFIED LEAD MATERIAL.** Every line records *what a named
speaker says*, attributed, with a file + timestamp pointer. Nothing here is asserted as true
and nothing here is graded. No quotation exceeds a short phrase; where the wording matters the
pointer is given instead so the passage can be re-read at source.

**Auto-transcript warning applies to every proper noun below.** These are machine captions with
no speaker labels and heavy proper-noun corruption. Two demonstrations from inside this corpus:
the **Buga sphere** renders as `Boötes sphere` [D @ 00:02:12], and the guest in file A is
introduced as `James Valor` [A @ 00:02:17] and thanked at the close as `James Fowler`
[A @ 01:58:44] — the same person, two surnames, no third occurrence to break the tie. Names are
marked:

- **[CONF]** — spelled consistently across the file and matching a well-attested public figure
  or organisation.
- **[PHON?]** — phonetically corrupted; a reconstruction is offered with the raw caption form in
  `backticks`. **Treat as a search string, not a fact.**
- **[UNRESOLVED]** — could not be reconstructed with confidence. Recorded raw. **Must not reach
  the board under the spelling in the transcript.**

Timestamps are the START of the caption block containing the statement, `[file @ HH:MM:SS]`.

## File key

| # | id | who is speaking | length | channel evidence |
|---|---|---|---|---|
| **A** | `y_8IKKcTntQ` | Skywatcher operations lead, name **[UNRESOLVED]**, interviewed by Jesse Michels | 119 min | host called "Jesse"; American Alchemy ad reads |
| **B** | `d68a1JfwVsE` | **Paul Hynek**, son of J. Allen Hynek | 121 min | **NOT American Alchemy.** Host addressed as "Chris"; ad read says "Area 52 viewers"; Michels appears only as a submitted audience question [B @ 01:52:13] |
| **C** | `kRO5jOa06Qw` | **David Grusch**, interviewed by Jesse Michels, with a long scripted narration track | 112 min | "today's American Alchemist: David Grusch" |
| **D** | `V00WcEiKRAY` | **Ross Coulthart**, interviewed by Jesse Michels | 111 min | American Alchemy ad reads |
| **E** | `p0S0BfoZy0w` | **Dr John Brandenburg**, interviewed by Jesse Michels | 106 min | American Alchemy ad reads |

**Dating.** None of the five states its own date. Internal markers only: C is anchored to the
aftermath of the 26 July 2023 House hearing and an amendment expected "this fall" [C @ 00:13:49];
A refers to February and March observations and a hoped-for demonstration "within the first half
of 2025" [A @ 01:41:33]; D names Gabbard, Patel and Ratcliffe in post and the Buga sphere
[D @ 01:34:28, 00:03:51]. E is undated internally. **Do not date any of these from this file.**

**The title of file C is a news clip, not the episode.** The "three men who previously served in
the military" [C @ 00:00:01] is archival footage of the July 2023 hearing coverage (Grusch,
Graves, Fravor). The episode itself is a single-guest Grusch interview.

---

## 1. ENTITIES

Cross-check verdicts in the rightmost column are from `tools/corpus_crosscheck.py` run on
30 August 2026. **Read §7 first for the tool's known blind spot** — it scans narrative/desc/sub
fields only, so several rows it calls ABSENT are in fact present in claim text. Rows where I
checked `data/the-program.json` directly are marked `†`.

### 1a. Government bodies, offices and units

| Name | Role the speaker assigns it | Cite | X-check |
|---|---|---|---|
| **Manhattan Project** [CONF] | Grusch: the secrecy template the UFO programme was built on; "they were kind of the first blue book", and colleagues' grandparents were "the UFO report people on the Manhattan Project" | C @ 00:23:04, 00:23:35 | PROSE |
| **Atomic Energy Commission → DOE** [CONF] | Inserted Vallée clip: custody chain Manhattan Project → AEC → DOE, "which has its own line of clearances" | C @ 00:24:08 | node (DOE) |
| **4602d Air Intelligence Service Squadron** [CONF — Hynek says only "Air Intelligence Service Squadron"] | Paul Hynek's hypothesis for the identity of the Men in Black: a unit tasked to respond to any crash, terrestrial or extraterrestrial, within 6 hours in CONUS, carrying Russian speakers, whose mission included "contain[ing] information fallout" | B @ 01:14:04, 01:14:38 | PROSE |
| **Project Blue Book** [CONF] | B: a PR exercise, not a scientific effort; Hynek continued as consultant *past* the Dec 69/Jan 70 termination. C: "a propaganda mouthpiece for the Air Force" | B @ 00:10:44, 01:52:13; C @ 00:23:35 | NODE |
| **Condon Committee** [CONF] | C: Condon coordinated with Col. Robert Hippler, who wanted prior UFO research shown as wasted money | C @ 01:05:26 | NODE |
| **CIA Office of Global Access** [CONF] | Coulthart: the body that intervened to stop the Lockheed→Bigelow transfer, "the Office of Global Access as it was once known" | D @ 00:47:23 | PROSE |
| **Air Force Office of Special Investigations** [CONF] | C narration: showed up after missileer sightings, confiscated footage, swore witnesses to secrecy | C @ 00:33:27 | NODE |
| **Joint Intelligence Organisation (JIO), Australia** [CONF] | Coulthart: where Harry Turner worked after Maralinga; recipient of Turner's 1972 paper recommending an Australian "UFO flying squad" | D @ 00:51:15 | ABSENT |
| **ASIS (Australian Secret Intelligence Service)** [CONF] | Coulthart's 1994 story: performed "plausibly deniable favours" for the US and UK inside Five Eyes | D @ 00:53:28 | ABSENT (as ASIS) |
| **National Nuclear Security Administration** [CONF] | Michels: a FOIA for UFO-related acronyms around Starfish Prime returned a Glomar-style refusal | D @ 01:13:59 | NODE |
| **Space Command** [CONF] | Brandenburg's second confirmation source — an unnamed officer he cold-called | E @ 00:06:12 | node (USSPACECOM) |
| **Joint Chiefs of Staff (staff level)** [CONF] | Brandenburg's first source, an unnamed colonel: "Yes... the rest you can figure out for yourself" | E @ 00:05:38 | node |
| **FBI** | Coulthart: an ongoing FBI investigation; a congressional briefing that "really blew people away" | D @ 01:35:34 | node |
| **DOPSR** [CONF] | Grusch: everything he says publicly must clear DoD prepublication review | C @ 00:18:08 | NODE |

### 1b. Contractors, companies, laboratories and institutes

| Name | Role the speaker assigns it | Cite | X-check |
|---|---|---|---|
| **Skywatcher** [CONF] | The subject of file A. A private, non-government-funded technology company; the name was chosen as "my cover term for UAPs" for briefing VCs and government without saying UAP | A @ 00:28:31 | NODE |
| **Martin Company / Martin Corporation** [CONF] | C narration: employer of Townsend Brown from 1942; parent of RIAS; later half of Lockheed Martin | C @ 00:43:45, 00:51:17 | ABSENT |
| **Research Institute for Advanced Studies (RIAS)** [CONF] | C narration: Martin's antigravity research outfit; Louis Witten worked there under George Trimble | C @ 00:43:45 | ABSENT |
| **Institute of Field Physics** [CONF] | C narration: founded by Agnew Bahnson at North Carolina, dedicated to antigravity | C @ 00:42:38 | ABSENT (tool matched a domain label, not the institute) † |
| **Gravity Research Foundation** [CONF] | C: Roger Babson's essay contest. E: Brandenburg independently names "the Gravity Essay... from the Gravity Research Foundation in Boston" | C @ 00:42:38; E @ 00:15:35 | ABSENT † |
| **Guidance Technologies** [CONF] | C narration: Townsend Brown's 1960s company, invested in by Floyd Odlum | C @ 00:52:56 | ABSENT † |
| **Northrop Grumman** [CONF] | C narration: built the B-2; Odlum named as "major investor" | C @ 00:52:56 | node (Northrop) |
| **Lockheed Martin** [CONF] | Coulthart: an unnamed senior executive told him "It's not us... it's the agency", which Coulthart reads as an implicit acknowledgement of held technology | D @ 00:45:43, 00:46:18 | node |
| **Bigelow Aerospace** [CONF] | Coulthart: the intended recipient of a craft from Lockheed Martin; the 2017 NYT "metamaterials" framing was, he says, a cover for a spacecraft | D @ 00:46:51 | NODE |
| **Institute for Defense Analyses** [CONF] | Michels: an FFRDC used as cover; cites Malmgren's own 2024 statement that IDA was the cover while he assisted the Joint Chiefs | D @ 01:06:45, 01:07:17 | NODE |
| **Aerospace Corporation** [CONF] | Michels: where "Tim Taylor" worked besides NASA; also "saucers and hangers at Aerospace Corporation" as an example of what the public already tolerates | D @ 01:06:45; E @ 00:47:52 | NODE |
| **Battelle Memorial Institute** [CONF] | Michels: "a contract between Los Alamos and Battelle... around Nitinol", declassified in the 60s | E @ 01:33:54 | NODE — **and the board already contradicts the sponsor.** See §6. † |
| **Thunder Scientific Corporation** [PHON? caption `Thunder Corporation`] | Brandenburg: Bennewitz's remote-sensing company, which he drove past daily on the way into Sandia | E @ 01:39:24 | NODE |
| **Mission Research Corporation** [CONF] | Brandenburg's employer in Washington DC, "supporting the Pentagon and the agencies" | E @ 00:35:36 | ABSENT † |
| **SRI / Stanford Research Institute** [CONF] | Brandenburg: the Independent Mars Investigation was headquartered at SRI, and "the remote viewing program was just down the hall" | E @ 00:31:13 | NODE |
| **Momentus** [CONF] | Brandenburg: flew his water-based microwave electrothermal thruster; he consulted for them after his patent expired | E @ 01:01:32 | ABSENT † |
| **Simons Foundation** [CONF] | Michels: David Spergel runs it, chaired the NASA UAP panel, and is "very embedded in DOE research" | D @ 00:43:26 | NODE |
| **Monroe Institute** [CONF] | Paul Hynek is its **CFO**; states a goal of reaching 80 million people, 1% of the population | B @ 00:35:02, 00:38:24 | citation-only on the board (one source-name string) † |
| **Lawrence Livermore / Sandia / Los Alamos** [CONF] | Brandenburg worked at Livermore (fusion) then Sandia (directed-energy weapons) | E @ 00:03:20 | NODE |
| **Jet Propulsion Laboratory** [CONF] | Brandenburg: life on Mars is an "open secret" there; a manager allegedly said life on Mars means "death for JPL" (attributed via Whitley Strieber) | E @ 00:46:12, 00:58:14 | ABSENT † |

### 1c. Programmes, operations and instruments

| Name | Role assigned | Cite | X-check |
|---|---|---|---|
| **Atomic Energy Act of 1954** | Grusch: the "special nuclear material" definition is "a sneaky way" to capture retrieved crash material | C @ 00:21:23 | PROSE — **and his characterisation of the definition needs adjudicating; see §6** |
| **McMahon Act (Atomic Energy Act of 1946)** | C narration: Condon helped draft it; framed as the predecessor instrument | C @ 01:06:32 | ABSENT † |
| **Operation Paperclip** | C: 1,600+ German scientists; narration speculates a UFO motive behind the urgency | C @ 00:53:27 | PROSE |
| **Operation Fishbowl / Bluegill Triple Prime / Starfish Prime** | Coulthart's and Michels's shared subject: the claim that a UFO was engaged or retrieved during the 26 October 1962 Bluegill Triple Prime shot | D @ 01:00:06 ff, 01:13:26 | ABSENT † |
| **Golden Dome** | Skywatcher lead: "Skywatcher as part of the Golden Dome" | A @ 01:54:51 | ABSENT † |
| **Echelon / Five Eyes** | Coulthart: his own prior scoop; the tradecraft reason he approached UFO sources by **posted letter**, ~160–170 of them | D @ 00:20:33, 00:25:34 | Five Eyes PROSE; Echelon ABSENT † |
| **Stargate / Grill Flame** | Michels, in passing, on child recruitment into psi programmes | A @ 01:31:44 | NODE |
| **PPD-19** | Grusch's closing address to people still inside: the legal route | C @ 01:39:51 | NODE |

### 1d. Facilities and places

| Name | Role assigned | Cite | X-check |
|---|---|---|---|
| **Secret Mountain, Sedona AZ** [CONF] | Coulthart: he personally saw, through night-vision, a pulsing golden orb rise from behind it at ~01:30, escorted by Black Hawks | D @ 01:21:43, 01:23:24 | ABSENT † |
| **Bradshaw Ranch, AZ** [CONF] | Coulthart: fenced area, camera aimed at the spot Linda Bradshaw reported a portal; two humming three-phase power boxes feeding cable into the ground; GPR return of a 50-ft reinforced structure just under the road | D @ 01:25:36 – 01:27:13 | ABSENT † |
| **Clarkdale Cement Plant, AZ** [CONF] | Coulthart: alleged egress point, aligned with the Bradshaw tunnel bearing; locals report 20-year-old tunnelling and compensation for damage | D @ 01:27:46, 01:28:20 | ABSENT † |
| **Maralinga and Woomera, Australia** [CONF] | Coulthart: Turner was supervising physicist at Maralinga; Woomera is where "your dirty aerospace gets brought out"; Aboriginal communities report silent black triangles | D @ 00:49:03, 00:49:34 | ABSENT † |
| **Johnston Atoll / Marshall Islands** [CONF] | Bob Jacobs archival clip: stationed there, told a Soviet orbital nuke had been shot down and "something had been recovered" | D @ 01:11:41 – 01:12:51 | ABSENT † |
| **Manzano Mountain, Kirtland AFB** [CONF] | Brandenburg: nuclear storage; what Bennewitz was recording | E @ 01:39:56 | PROSE |
| **Vandenberg AFB** [CONF] | Bob Jacobs's 1964 case; he says he was officer in charge of optical instrumentation | C @ 00:31:49; D @ 01:11:09 | node (USAF) |
| **Naval Surface Warfare Center Crane** [CONF] | Michels: where **Randy Anderson** says he was taken underground and possibly shown off-world technology | D @ 00:04:58 | PROSE |
| **Ellsworth AFB, 1977** [CONF] | Michels: **Mario Woods** is a 1977 Ellsworth experiencer, and reacted to the Buga symbols | D @ 00:04:58 | node (USAF) |
| **Sierra Blanca / El Paso, TX** [CONF] | Skywatcher's operating area at the time; UAPs seen in the same airspace as transiting airliners at FL180 | A @ 00:57:47, 01:47:38 | ABSENT (Sierra Blanca) † |
| **Ariel School, Ruwa, Zimbabwe, 1994** [PHON? captions `Arial`, `Aeriel`] | C narration: 62 children; narration adds it "was near a uranium mining site" | C @ 00:30:44 | ABSENT † |
| **Cydonia Mensae, Mars** [CONF] | Brandenburg: face plus a five-sided pyramid ~5 miles apart, never shown together by NASA | E @ 00:26:47 | ABSENT † |

### 1e. People — the ones the board does not already carry

Only rows the cross-check returned as ABSENT or PROSE are listed; the ~79 NODE hits (Grusch,
Coulthart, Vallée, Hynek, Nolan, Elizondo, Doty, Bennewitz, Salas, Twining, Condon, Teller,
Marcel, Brazel, Arnold, Sarbacher, Friend, etc.) are already on the board.

| Name | Role assigned | Cite | X-check |
|---|---|---|---|
| **Thomas Townsend Brown** [CONF] | The load-bearing figure of C's narration. See §5 | C @ 00:47:30 ff | **ABSENT** † |
| **Linda Brown** [CONF] | Townsend Brown's daughter; recalls a black Cadillac driven by Robert Sarbacher; requested his Navy records | C @ 00:50:12 | ABSENT † |
| **Paul Schatzkin** [CONF] | Biographer, *The Man Who Mastered Gravity* | C @ 00:48:02 | ABSENT † |
| **George Trimble** [CONF] | Witten's boss at RIAS; the 1956 "cancel out gravity" quotation; Nick Cook's rebuffed approach | C @ 00:43:45, 00:44:50 | ABSENT † |
| **Louis Witten** [CONF] | Martin/RIAS physicist; Wright Field gravity contract; father of Ed Witten | C @ 00:43:12, 00:45:22 | ABSENT † |
| **Agnew Bahnson** [CONF] | Industrialist; Institute of Field Physics; 1957 Chapel Hill conference; also named as a Townsend Brown funder | C @ 00:42:38, 00:51:52 | ABSENT † |
| **Roger Babson** [CONF] | Gravity Research Foundation patron | C @ 00:42:38 | ABSENT † |
| **Floyd Odlum** [CONF] | Investor named as the link between Guidance Technologies and Northrop | C @ 00:52:56 | ABSENT † |
| **Nick Cook** [CONF] | Aviation journalist; *The Hunt for Zero Point*, named independently by Coulthart as the book that shaped his prior | C @ 00:44:50; D @ 00:22:45 | ABSENT † |
| **Robert Oppenheimer** [CONF] | Grusch: "created the classification that included the UFO stuff" | C @ 00:20:50 | **ABSENT** † |
| **Curtis LeMay** [CONF] | C: named as a Townsend Brown contact; archival Goldwater clip on being cussed out over the Wright-Patterson room | C @ 00:50:45, 00:25:46 | citation-only (RG-615 file name) † |
| **Harald Malmgren** [PHON? captions `Harold Momgren`, `Harold Malmgren`, and once `Harold Agnew`] | Coulthart's source for Bluegill Triple Prime; Michels says his diaries record meetings with Richard Bissell | D @ 01:00:37 ff, 01:15:05 | ABSENT † |
| **Pippa Malmgren** [CONF] | His daughter; both speakers defer to her over the Douglas Dean Johnson critique | D @ 01:05:06 | ABSENT † |
| **Richard Bissell** [CONF] | Michels: the person who, per the diaries, read Malmgren in | D @ 01:15:05 | ABSENT † |
| **Nat Kobitz** [CONF] | Former head of science and technology development, US Navy. Coulthart's breakthrough source | D @ 00:26:42 | ABSENT † |
| **Harry Turner** [CONF] | Australian physicist; Maralinga; JIO; 1972 paper | D @ 00:47:23 ff | ABSENT † |
| **Bill Chalker** [CONF] | Australian researcher who knew Turner | D @ 00:47:23 | ABSENT † |
| **Sir Robert Muldoon** [CONF] | Former NZ PM; Coulthart's Kaikoura remark | D @ 00:20:00 | ABSENT † |
| **Bruce Maccabee, Quentin Fogarty, Dennis Grant, John Cordy** [CONF] | Kaikoura 1978 principals | D @ 00:21:37, 00:16:11 | ABSENT † |
| **Robert Jacobs** [CONF] | The 1964 Vandenberg film witness; extensive archival audio in D | C @ 00:31:49; D @ 01:08:57 – 01:12:51 | ABSENT † |
| **Paul Hynek** [CONF] | Primary witness of file B | B, throughout | ABSENT † |
| **Neil Armstrong** [CONF] | Paul Hynek: shared all meals with the Hynek family on a 1973 eclipse cruise; discussed founding a new UFO research group | B @ 00:13:28, 00:14:32 | ABSENT † |
| **Robert Friend** [CONF] | Blue Book director; Paul Hynek's two anecdotes (Fort Hood; "Paul, yes") | B @ 01:28:02, 01:30:21 | PROSE |
| **Donald Menzel** [CONF] | B: a Harvard colleague, relations "more cordial than is widely purported". C: grouped with Condon and Robertson as atomic-programme debunkers | B @ 00:11:53; C @ 01:04:22 | ABSENT † |
| **Arthur C. Clarke** [CONF] | B: correspondence in which Clarke privately admired Hynek's position | B @ 00:12:25 | ABSENT † |
| **Philip Corso / William Birnes** [CONF / Michels blanks on Birnes's name] | E: Corso's account used as a source and simultaneously distrusted | E @ 01:21:34, 01:35:33 | ABSENT † |
| **Leonard Stringfield** [CONF] | Brandenburg: told him three versions of the Dulce clash, differing only in casualty counts | E @ 01:42:14 | NODE |
| **John Brandenburg** [CONF] | Primary witness of file E | E, throughout | ABSENT † |
| **Richard Hoagland** [CONF] | Named; Brandenburg explicitly rejects the *Dark Mission* occult-NASA thesis | E @ 00:57:42 | ABSENT † |
| **Haim Eshed** [CONF] | Michels: former head of Israel's space security programme, on a Galactic Federation | E @ 00:50:35 | ABSENT † |
| **Mario Woods, Randy Anderson, Patrick Jackson** | Buga-symbol reactors and sphere researcher | D @ 00:04:58, 00:10:35 | Woods/Jackson ABSENT; **Anderson is PROSE — see §7** † |
| **Jeremiah Hostetler and Alexandra Hostetler** [PHON?] | Sedona on-the-ground researchers | D @ 01:22:16 | ABSENT † |
| **Melinda Leslie** [CONF] | Sedona local with the night-vision optics | D @ 01:23:24 | ABSENT † |
| **Douglas Dean Johnson** [CONF] | Author of the critique of the Malmgren claims; Coulthart calls parts of it legitimate and the timing "heartless" | D @ 01:00:37, 01:05:06 | ABSENT per tool — **false; present in board source names** † |
| **Michael Kratsios** [CONF] | Coulthart quotes an official statement, "our technologies permit us to manipulate time and space" | D @ 01:48:18 | ABSENT † |
| **Ansel Talbert** [PHON? caption `The author was Talbot`] | Brandenburg: the newspaper series that exposed aerospace antigravity interest. See §6 for the paper | E @ 00:15:35 | ABSENT † |

---

## 2. WITNESSES AND THEIR CHAIN

The distinction the board's §6 grading turns on. **"First-hand"** below means the speaker
describes something he personally perceived. **"Hearsay"** means he is repeating what a named or
unnamed person told him. **"Read"** means he is reporting a document or book.

| Witness | The claim | Chain | What would corroborate it |
|---|---|---|---|
| **Skywatcher lead** [UNRESOLVED name] | 2021: at a government war-game event, his camera operator imaged seven "class one" objects in formation, invisible to observers on the roof | **First-hand** (perceived the footage; the sighting itself was the operator's) | The war-game contract, the event location and date, the operator's identity. He names none. A @ 00:08:20 |
| same | A UAP disabled three unconnected systems, screens to "off", the instant someone began to slew a high-power microwave antenna toward it | **First-hand** | Two independent participants; the equipment's own log. He dates it "around 2003", which is inconsistent — see §6. A @ 01:22:30 |
| same | A helicopter under his direction stopped moving in flight — engine running, blades turning, no translation | **Hearsay**, in part: he was not the pilot in that instance; audio from the aircraft is played | The airframe's recorded track. A @ 01:10:27 |
| same | Government meetings, in SCIFs, where the answer is always "nothing in inventory matches"; a participant said "maybe this is off planet" | **First-hand**, but every counterparty is unnamed | Nothing checkable is offered. A @ 00:41:16, 00:41:48 |
| same | Four UAP crashes observed 2023–24; searches found no wreckage | **First-hand** observation, **negative** result | He volunteers the null. A @ 01:43:45 – 01:46:31 |
| **Paul Hynek** | J. Allen Hynek held a wartime clearance from proximity-fuse work at APL/Johns Hopkins, which is why the Air Force picked him | **Family/read**; explicitly framed as his own Occam's-razor reconstruction | APL and Ohio State personnel records. B @ 00:10:08 |
| **Paul Hynek** | The Hynek family shared every meal for two weeks with Neil Armstrong's family on a 1973 eclipse cruise, and Armstrong discussed founding a research group with his father | **First-hand** (he was 11 and present) | The cruise manifest; he also cites a 2019 UK newspaper piece he read afterwards. B @ 00:13:28, 00:14:32 |
| **Paul Hynek** | Asked at his 99th birthday whether he ever saw anything convincing, Lt Col Robert Friend looked around and said "Paul, yes" | **First-hand** | Nobody else at the table is named. Filmed background interviews for the *Project Blue Book* TV show are said to exist. B @ 01:30:21 |
| **Paul Hynek** | Friend, on camera, said bodies would have gone not to Wright-Patterson but to Fort Hood, "a burn center" | **First-hand** hearing it; **Friend's own status is second-hand** — he is answering a hypothetical without violating his oath | The filmed interview. **The "burn center" detail is problematic; see §6.** B @ 01:28:38 |
| **Paul Hynek** | His father encountered Men in Black: a white sedan, two men in dark clothes, and a witness who then would not talk | **Hearsay**, and he cannot name the case | He says so himself: "I don't remember what case it was." B @ 01:14:38 |
| **David Grusch** | ~40 people, some previously unknown to each other, described a retrieval and reverse-engineering programme; he made the interviewers themselves testify to the IG | **Hearsay by design** — he is explicit that he is a conduit, never a participant | The ICIG file; the interviewers. C @ 00:11:09, 00:11:41 |
| **David Grusch** | Exotic-origin assessment rested on briefed isotopic ratios "that would have to be engineered" | **Read** (intel reports) plus **hearsay** | The reports. He names no document. C @ 00:08:57 |
| **David Grusch** | "Biologics came with some of these recoveries"; non-human, per people currently on the programme | **Hearsay**, twice removed, and pre-cleared through DOPSR | Nothing offered. C @ 00:16:33 |
| **Ross Coulthart** | Nat Kobitz, unprompted, said "why don't you ask me the question", then answered yes; described being flown to Wright-Patterson, taken underground, shown a bulkhead piece bonded "at the atomic level" | **First-hand** for the conversation (recorded, with permission, unreleased); **hearsay** for the artefact | The recording exists. Kobitz is deceased; family consent is the gate Coulthart names. D @ 00:30:36 – 00:36:14 |
| **Ross Coulthart** | A Lockheed Martin senior executive said "It's not us... it's the agency" | **First-hand**, source unnamed and unrecorded ("I promise you I'm not recording you") | Unverifiable as told. D @ 00:46:18 |
| **Ross Coulthart** | At Sedona he personally watched a large pulsing golden orb rise behind Secret Mountain at ~01:30, escorted by Black Hawks | **First-hand**, with a named companion (Melinda Leslie) and broadcast footage | The footage aired; the helicopters are the checkable part — see §7 lead 4. D @ 01:23:24 |
| **Ross Coulthart** | Ground-penetrating radar on the road by Bradshaw Ranch returned a 50-ft reinforced structure; two humming three-phase boxes feed cable into the ground | **First-hand** presence; the GPR reading is his operator's, named only as "my friend Paul" | The GPR trace, said to be in the long-form interview. D @ 01:26:41, 01:27:13 |
| **Ross Coulthart** | Australian special-forces veterans told him they took part in US retrieval operations, paid in cash US dollars, with the Australian government never briefed | **Hearsay**, sources unnamed | Nothing offered. D @ 00:56:16 |
| **Ross Coulthart** | Detained by CBP after the Grusch story; a flag on his file, too high-level for the officers to read | **First-hand** | A CBP/DHS records request in his own name. D @ 01:16:13 |
| **John Brandenburg** | A colonel on the Joint Chiefs' staff confirmed a UFO cover-up in one word | **First-hand** conversation, source unnamed, "a friend of a friend" | Unverifiable as told. E @ 00:05:38 |
| **John Brandenburg** | Carl Sagan telephoned him twice about the second Mars "face", ending with "it's very interesting" | **First-hand** | Sagan's Cornell correspondence files; the conference paper. E @ 00:32:20 – 00:38:23 |
| **John Brandenburg** | Xenon-129 and argon-40 superabundance in the Martian atmosphere have no accepted explanation | **Read**, and he is explicit it is his own literature review | The Viking atmospheric results and the SNC meteorite gas data are public. E @ 00:22:51 |
| **John Brandenburg** | He was present at a MUFON conference when Bill Moore confessed to monitoring Bennewitz for the government | **First-hand** attendance at a public, recorded event | The 1989 MUFON symposium record. Note he first says "Stan Moore" and self-corrects. E @ 01:40:31 |
| **John Brandenburg** | He spoke with Roswell veterans at a reunion-style conference; they described a red-haired colonel, deuce-and-a-half trucks, and a week-long takeover of the base | **Hearsay** at one remove, from **first-hand** conversations he had | The conference; the attendees. He names none of them. E @ 01:25:27 – 01:26:34 |
| **John Brandenburg** | He was recruited toward, then blackballed out of, a programme after an interrogation at an agency headquarters | **First-hand**; he declines to name the agency or the person | Unverifiable as told. E @ 01:12:37 – 01:14:16 |
| **Robert Jacobs** (archival audio inside D) | Stationed at Johnston Island in "November of 1963, not 62"; the island talk was that a Soviet orbital nuke had been shot down and "something had been recovered" | **First-hand** for being there; **explicitly scuttlebutt** for the content — he says so | Assignment records for the 1369th-series photographic unit; his own dating contradicts the Bluegill date Michels is asking about. D @ 01:11:41 |

---

## 3. DOCUMENTS AND PRIMARY RECORDS NAMED

Things with a title, number, date or archive that a later pass could pull.

| Record | As described | Cite |
|---|---|---|
| **Twining letter, 1947** | "something real and not visionary or fictitious"; and the passage the narration says matters more — that any US development along these lines would be "extremely expensive, time consuming" and should be set up independently of existing projects | C @ 00:21:59, 00:22:32 |
| **Atomic Energy Act of 1954, "special nuclear material" definition** | Grusch's paraphrase: "any material that releases any kind of atomic energy". **Adjudicate against 42 U.S.C. §2014 before using** | C @ 00:21:23 |
| **McMahon Atomic Energy Act of 1946** | Narration: Condon helped draft it | C @ 01:06:32 |
| **Los Alamos Primer** | Narration: Condon "wrote" it. The authorship is shared — see §6 | C @ 01:05:59 |
| **Aviation Week, March 1992** | Narration: reported the B-2 using an electrokinetic effect in its wings, "a Biefield-Brown effect" | C @ 00:52:24 |
| **Jane's Defence Weekly, 1956** | Narration: source of the Trimble "cancel out gravity" quotation. **The sourcing here is doubtful — see §6** | C @ 00:43:45 |
| **American Institute of Physics oral-history interview with Louis Witten** | Narration: contains Witten's "a guy named Townsend" bismuth remark and the Wright Field gravity contract | C @ 00:46:58, 00:45:54 |
| **Townsend Brown's US Navy personnel record** | Narration: terminated 1942 without explanation despite strong performance; family request met with hints of continuing classification | C @ 00:51:17, 00:50:12 |
| **Harry Turner's 1972 JIO paper** | A report to the chief of JIO recommending an Australian UFO investigation squad, arguing the Americans were lying; Michels says he will link it below the video | D @ 00:51:15, 00:59:32 |
| **Australian National Archives, Maralinga/Woomera UAP sighting reports** | Coulthart: "there are still reports in the archives", used in his book | D @ 00:50:07 |
| **New Zealand archives release, ~2011** | Coulthart: shows RNZAF pressure from the PM's office to produce the squid-boat explanation for Kaikoura | D @ 00:21:05 |
| **Harald Malmgren's diaries** | Michels: now backed up and in a safe place; record meetings with Richard Bissell | D @ 01:15:05 |
| **Douglas Dean Johnson's Malmgren critique, and a published rebuttal** | Both named; Coulthart had not yet read the rebuttal | D @ 01:00:37 |
| **NNSA FOIA response re: Starfish Prime** | Michels: refused to confirm or deny responsive records under UFO-related acronyms | D @ 01:13:59 |
| **JFK → John McCone letter, 12 November 1963** | Narration: released under FOIA in 2006; asks for full UFO data to coordinate with the Soviets. **Narration itself flags doubt** — the requester will not talk, an archivist notes anomalies | C @ 01:12:36, 01:13:07 |
| **Battelle / Los Alamos 1949 nitinol contract** | Michels; declassified by Battelle "in the 60s". **Sponsor conflicts with the board — §6** | E @ 01:33:54 |
| **ALH 84001** | Brandenburg: Antarctic Martian meteorite with carbonate vein and apparent bacterial fossils | E @ 00:42:51 |
| **Brandenburg's 1986 conference paper on the Martian paleo-ocean** | Given "to a room full of Mars scientists" | E @ 00:30:39 |
| **Brandenburg's patent, water-based microwave electrothermal thruster** | Says it has expired; flown by Momentus | E @ 01:01:32 |
| **CIA "gateway" documents in the CIA reading room** | Coulthart, on official interest in psionics | D @ 01:42:12 |
| **Books named as sources** | *The Man Who Mastered Gravity* (Schatzkin) C @ 00:48:02 · *The Hunt for Zero Point* (Cook) D @ 00:22:45 · *UFOs and Nukes* (Hastings) C @ 00:31:17 · *The Day After Roswell* (Corso) E @ 01:21:34 · *The Invisible College* (Vallée, 1975) C @ 01:15:16 · *American Cosmic* (Pasulka) C @ 00:56:47 · *Alien Information Theory* (Gallimore) B @ 00:44:59 · *Cosmic Awakening* (Brandenburg) E @ 01:30:00 | |

---

## 4. THE STRUCTURAL ARGUMENT

Across the four Michels files, one account is being assembled and it is not primarily about
craft. It is about **classification lineage**. The claim is that the machinery which hid the
atomic programme was extended, deliberately and by the same people, to cover retrieved material —
so that the custodial history runs Manhattan Project → Atomic Energy Commission → Department of
Energy, with a statutory hook in the Atomic Energy Act's definition of nuclear material, and a
personnel overlap in Oppenheimer, Condon, Sarbacher, Teller and Vannevar Bush. Grusch states the
Oppenheimer half directly [C @ 00:20:50]; an inserted Vallée clip states the custody chain
[C @ 00:24:08]; the narration then argues that the same atomic-programme figures who wrote the
secrecy also wrote the public debunking, naming Menzel, Condon and Robertson [C @ 01:04:22].
This is the part of the corpus with the most specific, checkable content, and it is also the part
where the narration is at its loosest with facts (§6).

The second argument is **the missing physics branch**. C's narration treats the 1950s antigravity
enthusiasm as a real research programme that either failed or went black, and prefers the second
reading: RIAS inside Martin, the Institute of Field Physics at Chapel Hill, the Gravity Research
Foundation essay prize, Wright Field contracting Louis Witten for gravity work, and Townsend Brown
moving between the Navy, Martin and a company financed by the same men. It then closes the loop by
proposing that the discipline which absorbed the talent — quantum gravity and eventually string
theory — was a cul-de-sac, with Ed Witten as the ironic hinge. Brandenburg arrives at the same
"either nobody got anywhere or it went black" formulation independently in file E, and attributes
it to Hal Puthoff [E @ 00:15:35, 00:16:42]. Two speakers converging is not corroboration when both
are reading the same secondary literature, and the corpus is candid enough about this that a
researcher should be too.

The third argument is about **why the reader cannot check any of it**, and here the corpus is at
its most self-aware. Grusch's ~40 witnesses are anonymous by his own design, and everything he says
has been through DOPSR, which he describes as a catch-22 that produces either approval or a citable
redaction [C @ 00:18:08]. Coulthart's method is explicitly built around producing records that do
not exist in electronic form — posted letters, not phone calls, because of Echelon-derived metadata
concerns [D @ 00:25:34] — with the result that his own best material is a recording he will not
release [D @ 00:32:19] and a Lockheed executive he promised not to record [D @ 00:46:18]. The
Skywatcher lead has terabytes of data and says analysis is too expensive to have done
[A @ 00:31:17]. In every file the strongest evidentiary object is one the speaker declines to
produce, for a reason he states clearly. That is a structural feature of this corpus and should be
recorded as one rather than argued about.

---

## 5. THE 1940s–1980s THREAD

**The owner asked about this thread by name. It is present, and it is the single most valuable
thing in this slice — but it is almost entirely confined to one file, and to a scripted narration
track rather than to a witness.**

Where it lives: **file C, roughly 00:41:31 to 00:55:03**, a producer-narrated segment inside the
Grusch interview. Grusch himself contributes to it only twice — the Sarbacher/Oppenheimer answer
[C @ 00:20:50] and a short acknowledgement of Townsend Brown at the end [C @ 00:51:52]. Everything
between is narration over archival clips. **Grade accordingly: the narration is not a witness.**

| Element the owner named | Present? | What is actually said |
|---|---|---|
| **Thomas Townsend Brown** | **Yes, extensively** | The gravitator resembling a saucer; NICAP founding; the two-charged-plates theory; terminated by the Navy in 1942 with no explanation and reappearing at Martin two weeks later; parachuted into Germany in 1944 for Donovan and Stephenson to investigate foo fighters; driven home in a black Cadillac by Robert Sarbacher; funded by Agnew Bahnson; met Teller and LeMay. C @ 00:47:30 – 00:52:24 |
| **Electrogravitics** | **Yes, by mechanism, once by name-adjacent term** | The word "electrogravitics" is never spoken in any of the five files. "Electrokinetic effect" and "Biefield-Brown effect" are, once each, in the B-2 / *Aviation Week* passage. C @ 00:52:24 |
| **Manhattan Project lineage** | **Yes, and it is the spine of file C** | Oppenheimer as author of the classification; Condon's Los Alamos and McMahon Act roles; "they were kind of the first blue book"; grandparents who were "the UFO report people on the Manhattan Project". C @ 00:20:50, 00:23:04, 00:23:35, 01:05:26 |
| **AEC** | **Yes, but only in an inserted Vallée clip** | Custody chain Manhattan Project → AEC → DOE. The acronym "AEC" is never spoken; the AEA of 1954 and the McMahon Act of 1946 are. C @ 00:24:08, 00:21:23, 01:06:32 |
| **Early aerospace contractors** | **Yes** | Martin Corporation, RIAS, Northrop Grumman/B-2, Lockheed's Skunk Works, Guidance Technologies, Floyd Odlum. C @ 00:43:45 – 00:52:56 |
| **Nazi-transfer thread** | Yes | Paperclip, von Braun, Arthur Rudolph, foo fighters, ghost rockets, Doolittle and the Lindbergh Foundation. C @ 00:48:35 – 00:55:03. Coulthart adds "Kammler stuff in Nazi Germany" in one clause, undeveloped. D @ 01:48:53 |
| **1980s** | Yes, in file E | Able Archer 1983 as classified, felt inside Sandia; the Bennewitz operation; the Dulce reports via Stringfield; Reagan-era Star Wars work. E @ 00:03:56, 01:39:24, 01:42:14 |

**Two clean negatives, stated explicitly because a negative is a result:**

1. **Wilbert Smith, the "Geo-Magnetics" memorandum and Canada's Project Magnet are never
   mentioned in any of the five files**, even though Sarbacher is named twice. The board's
   existing Sarbacher material sits entirely inside the Wilbert Smith node. This corpus reaches
   Sarbacher by a completely different route — Linda Brown's black-Cadillac recollection — and
   the two routes have never been joined on the board.
2. **"Electrogravitics" as a term, the 1956 Gravity Rand / Aviation Studies reports, and Project
   Winterhaven are absent.** The 1950s antigravity story is told here entirely through people and
   institutions, never through its documents.

---

## 6. INTERNAL CONTRADICTIONS AND FACTUAL ERRORS

Named plainly. Several of these are in the *narration*, which is the part of the corpus most
likely to be mistaken for verified fact.

| # | Where | The problem |
|---|---|---|
| 1 | C @ 00:51:17 | **Skunk Works is Lockheed's, not Martin's.** The narration places Brown at "Martin Corporation in Burbank", "50 miles from where Skunkworks is founded" a year later by Kelly Johnson, and calls Skunk Works "Martin's most advanced, secretive work". Kelly Johnson's Skunk Works was Lockheed's, in Burbank, from 1943; the Martin Company was in Baltimore. The "would later become Lockheed Martin" framing appears to have collapsed a 1995 merger backwards into 1943. **This invalidates the geographic-proximity inference the segment rests on.** |
| 2 | C @ 00:25:14, D @ 01:06:12 | **Two named debunk-worthy history errors in the same corpus.** C: the Roswell debris is said to have gone to Wright-Patterson, which the narration says had shortly before been used to "reverse engineer a German pulse jet engine" — a defensible claim, but stated as settled. D: Michels says Allen Dulles "was at the Brown Brothers Harriman" at the time of the JFK assassination. Dulles's firm was Sullivan & Cromwell, and in November 1963 he had been out of CIA for two years. |
| 3 | D @ 01:07:50 | **"Paul Mellon founded the CIA."** He did not. Mellon served in OSS. The sentence is used as a load-bearing step in an argument that Malmgren was CIA. |
| 4 | D @ 01:09:31 vs 01:11:09 | **Michels places Bob Jacobs's 1964 missile-film case at Edwards AFB; Jacobs, in the archival audio played seconds later, says Vandenberg.** Both are in the same passage. The unit is captioned "13th security night photo squadron", which is not a real designation. |
| 5 | C @ 00:31:49 | **"Atlas five missiles"** for the same 1964 case. Atlas V is a 21st-century launch vehicle. Caption or misspeak; either way not usable. |
| 6 | B @ 01:28:38 | **"Fort Hood, which was a burn center."** The US Army's burn centre is at Brooke Army Medical Center, Fort Sam Houston. Fort Hood appears in the nuclear-storage literature (Killeen Base), and C @ 00:33:27 names Fort Hood in exactly that role. Paul Hynek is reporting Friend's words, so the error may be Friend's, Hynek's or the caption's — but the detail cannot be carried forward as stated. |
| 7 | B @ 01:55:37 | **Schindele and Salas are conflated.** "Dave Schindler... was with Robert Salis", placed together at Air Force bases in Montana in 1967. Salas was at Malmstrom, Montana, March 1967; David Schindele's account is Minot AFB, North Dakota, 1966. Two incidents, two states, two years. |
| 8 | E @ 01:36:39 | **"James McDonald... this Arizona State physicist."** James E. McDonald was at the University of Arizona. The board already carries him under the correct affiliation. Michels also asserts McDonald "had his own UFO sighting at Savannah River Site" — unverified and not, to my knowledge, part of the standard McDonald record. |
| 9 | E @ 01:38:51 | **"Hynek provided the laptop to Paul Bennewitz."** The Bennewitz operation ran from about 1980. "Laptop" is anachronistic for the equipment involved, and the Hynek–Bennewitz link is asserted without a source in a passage Michels opens with "I just learned this". Treat as a rumour, not a lead. |
| 10 | E @ 01:31:08 | **"B-29 Black Widow."** The P-61 Black Widow was a night fighter; the B-29 was a bomber. Brandenburg's own preceding sentence [E @ 01:28:53] gets it right — "a night fighter... called the Black Widow" — so this is a slip inside one paragraph. |
| 11 | E @ 01:40:31 | **"Stan Moore... It was Bill Moore."** Self-corrected in the transcript within one sentence. Record only the corrected form. |
| 12 | A @ 01:22:30 | **"around 2003"** for an event that must be 2023. The speaker's own origin story dates Skywatcher's first sighting to 2021 [A @ 00:04:31] and the energy-weapon incident to a government event in the same programme. Almost certainly a spoken or captioned slip for 2023. |
| 13 | C @ 00:21:23 | **The AEA "special nuclear material" paraphrase.** Grusch says the definition "any material that releases any kind of atomic energy". The statutory definition is narrower and enumerates plutonium and enriched uranium plus a Commission-determination clause. **Do not correct the board from this, and do not correct Grusch from memory** — adjudicate against 42 U.S.C. §2014 and record what the statute says. CLAUDE.md §2 already records one statutory "correction" on this board that had to be reverted. |
| 14 | C @ 01:05:59 | **"wrote the Los Alamos Primer."** The lectures were Robert Serber's; Condon wrote them up. Both attributions circulate; the narration states only one and states it flatly. |
| 15 | E @ 00:15:35 | **The antigravity newspaper series.** Brandenburg says it "came out in the Miami Herald and other newspapers" and that "the author was Talbot". The series generally identified with this description is Ansel E. Talbert's, in the New York Herald Tribune, late 1955. Paper and author surname both need fixing before use. |
| 16 | C @ 00:52:56 | **Floyd Odlum as "major investor" in Northrop Grumman.** Odlum's Atlas Corp holdings are well documented in other airframe makers; the Northrop attribution as stated is the weakest link in the B-2 argument and should be checked before it is repeated. |
| 17 | C @ 00:50:12 | **"The National Secrecy Act."** No US statute of that name governs invention secrecy; the Invention Secrecy Act of 1951 does. Quoted as a caption from an archival clip, so the error may be the clip's. |
| 18 | C @ 01:04:54 | **"Edward Euler Condon."** Edward **Uhler** Condon. Caption corruption of a real middle name into a different famous one. |
| 19 | E @ 01:33:54 | **The Battelle contract's sponsor.** Michels says Los Alamos contracted Battelle in 1949 over nitinol. The board's existing Battelle node records **Air Force-sponsored** Battelle work on nickel-titanium alloys in 1948–49. These are different claims about the same research; one of them is wrong and the board's version is the one currently in production. **This is a live conflict, not a new lead.** |
| 20 | D @ 00:34:00 | **"the nose wheel for the C-47."** Kobitz's electron-beam-welding specialism is attributed to a C-47 nose-wheel programme. The C-47 is a 1930s design with a tailwheel. Probably a caption substitution for another aircraft designation. |

---

## 7. THE TOP 10 INDEPENDENTLY CHECKABLE LEADS

Ranked by (a) whether a document or record actually exists to be pulled and (b) how far the lead
moves the board.

> **A caveat on the cross-check verdicts, and it matters — this is a defect in the tool, not in
> the board.** `build_index()` in `tools/corpus_crosscheck.py` scans exactly four node fields
> (`narrative`, `desc`, `sub`, `label`), three edge fields and four timeline fields. It never
> reads `claims[].text`, `chronology[].event`, `sources[].name`, `timeline[].text`, or the
> top-level `entityInfo` block at all — and those are the fields most of this board's prose
> actually lives in. I re-ran the interesting rows directly against `data/the-program.json` and
> found **three false ABSENTs**:
> **Carl Sagan** (three hits, in `people[146].claims[0]`, `entities[389].claims[2]` and
> `timeline[75]`), **Randy Anderson** (`entityInfo.hearing-2025-09-09.desc`, named as a Greer
> witness) and **Douglas Dean Johnson** (13 hits, mostly source names). Every ABSENT below has
> been confirmed by direct grep, not by the tool alone. **A later pass should widen the tool's
> prose corpus before anyone trusts an ABSENT from it again** — a false ABSENT sends a researcher
> after something the board already carries, which `research/leads/README.md` already names as
> the expensive direction to be wrong in.

| # | Lead | What would verify it | X-check |
|---|---|---|---|
| **1** | **Louis Witten's American Institute of Physics oral history**, said to contain both the Wright Field gravity contract and the "a guy named Townsend" and "a type of bismuth that was repelled" exchange | The AIP Niels Bohr Library oral-history collection is public and indexed. This is the single most pullable document in the whole slice, and it would independently anchor the Martin/RIAS/Townsend Brown/Wright Field cluster without relying on Schatzkin's book. **C @ 00:45:54, 00:46:58** | **ABSENT** — Witten, RIAS, Trimble, Bahnson, Babson, Odlum, Guidance Technologies and Townsend Brown are all absent from the board. The entire 1950s antigravity complex is a hole. |
| **2** | **Harry Turner's 1972 paper to the chief of the Joint Intelligence Organisation**, recommending an Australian UFO investigation squad and arguing the Americans were withholding | Coulthart says he has written chapters on it and that Michels will link it. The Australian National Archives release path is the check. Turner's Maralinga role gives a second, personnel-record route. **D @ 00:51:15, 00:59:32** | **ABSENT** — Turner, JIO, Maralinga, Woomera, Bill Chalker all absent. A whole allied-nation branch the board does not have. |
| **3** | **Nathan Twining's 1947 letter, the "extremely expensive, time consuming" passage** | The board already has a Twining node and quotes the "real and not visionary" line. What is new here is the narration's insistence that the *cost/independence* passage is the load-bearing one. Pull the memo text and settle whether that passage says what the narration says. **C @ 00:22:32** | **NODE** — Twining and the memo are on the board; this is a claim about a passage of an existing document, which is cheap to adjudicate. |
| **4** | **The Sedona / Bradshaw Ranch physical claims**: a 50-ft reinforced structure on GPR just under the road, two humming three-phase power boxes feeding cable into the ground at a nominally deserted ranch, and a security camera aimed at the reported portal site | Unusually, three of these are checkable without any classified access: Arizona utility interconnection records for three-phase service to the parcel, the land-use / research-agreement paperwork with Northern Arizona University that Michels says is a cover story, and Coconino County permitting for the Clarkdale tunnelling that locals were compensated for. **D @ 01:25:36 – 01:28:20** | **ABSENT** — Sedona, Bradshaw Ranch, Secret Mountain, Clarkdale all absent. |
| **5** | **Robert Sarbacher's second route into this material.** The board reaches Sarbacher only through Wilbert Smith. Two speakers here reach him independently: Linda Brown's black-Cadillac recollection [C @ 00:50:45] and Coulthart's Australian "grey beards" who describe Sarbacher visiting them [D @ 00:52:21] | Sarbacher's own correspondence is partly published; the Australian claim is checkable against visit records for the period Turner and colleagues were at Maralinga/Woomera | **PROSE** — Sarbacher is named inside `wilbert-smith.narrative` but is not a node. This is a promotion question, and these two independent routes are the argument for it. |
| **6** | **Nat Kobitz.** Former head of science and technology development, US Navy; Coulthart holds an authorised recording of him answering "yes" and describing a Wright-Patterson underground viewing of an atomically bonded bulkhead | Kobitz's Navy career is a matter of public record — position, dates, and the electron-beam-welding programmes he ran are all documentable independently of the UFO claim. Establishing that the man held the job he is said to have held is the first, cheap half of this. **D @ 00:26:42 – 00:36:14** | **ABSENT** |
| **7** | **Harald Malmgren's diaries and the Richard Bissell meetings.** Michels says he has seen them and that they record meetings with Bissell | Malmgren's public career (USTR, White House) is heavily documented; Bissell's CIA calendar for the relevant period is partly declassified. The Douglas Dean Johnson critique and its published rebuttal are both named and both readable. **D @ 01:00:37, 01:15:05** | **ABSENT** for Malmgren and Bissell; **Johnson is already cited on the board as a source** (13 hits) — worth noting that the board already trusts his AARO analysis while this corpus is contesting his Malmgren analysis. |
| **8** | **The Bluegill Triple Prime / Operation Fishbowl file, and the NNSA FOIA refusal around Starfish Prime** | Operation Fishbowl is exhaustively documented in the open nuclear-testing literature (DASA/DNA reports, Johnston Island records). The NNSA response Michels describes — refusing even to confirm responsive records — is itself a document with a FOIA tracking number. Bob Jacobs's own dating ("November of 1963, not 62") is a check on the narrative, not a support for it. **D @ 01:00:06, 01:11:41, 01:13:59** | **ABSENT** — Fishbowl, Bluegill, Starfish, Johnston Atoll all absent. |
| **9** | **J. Allen Hynek's proximity-fuse clearance at the Applied Physics Laboratory**, offered by his son as the mundane explanation for the Air Force's choice of him | APL and Johns Hopkins wartime personnel records; Hynek's own Ohio State appointment. This is the least sensational lead in the list and probably the most likely to resolve cleanly, and it puts a 1940s date on an existing node. **B @ 00:10:08** | **NODE** for Hynek and APL; the proximity-fuse fact itself is absent from the board's Hynek material. |
| **10** | **The 1989 MUFON symposium at which Bill Moore stated he had worked with AFOSI against Bennewitz** — Brandenburg says he was in the room | The symposium proceedings and contemporaneous coverage are public. The board already carries Bennewitz, Doty and Moore, so this is a corroboration-of-an-existing-node task, and it converts a widely repeated story into a first-hand attendance claim by a named scientist. **E @ 01:40:31** | **NODE** — Bennewitz, Doty and William L. Moore are all on the board. Brandenburg is not. |

**Two leads deliberately left off the list**, with the reason:

- **The Buga sphere** [D @ 00:02:45 – 00:06:39]. Both speakers explicitly decline to endorse or
  debunk it, one of them has been shown a plausible fuel-tank visual match, and the provenance
  video has an unexplained gap. There is nothing here to check yet.
- **The Mars material** in file E. Brandenburg's isotope argument (Xe-129, Ar-40 superabundance)
  is genuinely checkable against the published Viking and SNC-meteorite literature, but it is not
  a claim about the legacy programme and does not belong on this board. Recorded, not ranked.

---

## 8. CORRUPTION WATCHLIST

Every name I flagged, with the raw caption form and a confidence. **Nothing in the UNRESOLVED
rows may reach the board under the spelling shown.**

| Raw caption | Reconstruction | Confidence | Cite |
|---|---|---|---|
| `James Valor` / `James Fowler` | — | **[UNRESOLVED]**. The two forms are the only two occurrences in a 119-minute file and they disagree. This is the primary witness of file A. **Do not put a surname on him.** He is describable without one: a retired Army sergeant major, ~23 years' service, retired 2020, operations lead at Skywatcher | A @ 00:02:17 / 01:58:44 |
| `Boötes sphere` | **Buga sphere** | **[PHON?] high** — the speaker uses "Buga" correctly moments later and names Buga, Colombia | D @ 00:02:12 vs 00:03:51 |
| `Harold Agnew` | **Harald Malmgren** | **[PHON?] medium.** The surrounding passage is entirely about Malmgren, his daughter Pippa, and Douglas Dean Johnson's critique of *his* claims. But Harold Agnew is a real Los Alamos figure, so this could be a genuine second name rather than a substitution. **Flag, do not resolve.** | D @ 01:00:37 |
| `Harold Momgren` | **Harald Malmgren** | [PHON?] high — "Harold Malmgren" appears correctly at 01:15:05 | D @ 01:05:38 |
| `Heinik` / `Heck` / `Heinekick` | **Hynek** | [PHON?] high | B, throughout |
| `Jacques Valet` / `Jacques Vallée` | **Jacques Vallée** | [CONF] | B @ 00:09:03 |
| `Charlie Hixon` / `Calvin Hixon` | **Charles Hickson** | [PHON?] high. Note the speaker also swaps the two men's given names once — "Charlie Parker and Calvin Hixon" — then self-corrects | B @ 01:10:42 |
| `Lonni Zamora` / `Lani Zamora` | **Lonnie Zamora** | [PHON?] high | B @ 00:01:05, 00:25:35 |
| `Sakuro` | **Socorro, New Mexico** | [PHON?] high — the 1964 Zamora case | B @ 00:01:05, 00:25:35 |
| `Pascula` | **Pascagoula** | [PHON?] high | B @ 00:00:33 |
| `Bllovadski` | **H. P. Blavatsky** | [PHON?] high | B @ 00:07:59 |
| `Alex Tannis` | **Alex Tanous** | [PHON?] medium | B @ 00:35:34 |
| `Olga Waral` | **Olga Worrall** | [PHON?] medium | B @ 00:35:34 |
| `Joseph McMongle` | **Joseph McMoneagle** | [PHON?] high | B @ 00:34:29 |
| `Andrew Gallmore` / `Gallamore` | **Andrew Gallimore** | [PHON?] high | B @ 00:45:32 |
| `Rick Stman` | **Rick Strassman** | [PHON?] high — *The Spirit Molecule* | B @ 00:47:52 |
| `Michael Shurmer` | **Michael Shermer** | [PHON?] high | B @ 01:00:41 |
| `Seth Shawstack` | **Seth Shostak** | [PHON?] high | B @ 01:00:41 |
| `Danny Sheen` / `Danny Shien` | **Danny Sheehan** | [PHON?] high | B @ 00:53:59, 01:17:27 |
| `Paula Harris` | **Paola Harris** | [PHON?] medium — named as a Hynek confidant | B @ 01:10:09 |
| `Philip Mantel` | **Philip Mantle** | [PHON?] high | B @ 01:11:14 |
| `Dave Schindler` | **David Schindele** | [PHON?] medium. **Compounded by the Salas/Minot conflation in §6 item 7** | B @ 01:55:37 |
| `Robert Salis` / `Bob Salis` | **Robert Salas** | [PHON?] high | B @ 01:55:37 |
| `Bet Sphere` / `Betsphere` | **Betz sphere** | [PHON?] medium — the 1974 Florida case | B @ 01:54:32 |
| `Paul Ciderella` / `Paul Cinderella` | — | **[UNRESOLVED]** — named as Monroe Institute CTO | B @ 00:35:02, 00:37:48 |
| `Alan Evans`, `Jamie Roorbeck` | — | **[UNRESOLVED]** — named as Monroe Institute CEO and controller. Common enough names that a plausible guess is worse than none | B @ 00:37:48, 00:39:29 |
| `EuoCon` | — | **[UNRESOLVED]** — a San Francisco conference | B @ 01:24:04 |
| `Mary and Rob` / `UAP PD` | — | **[UNRESOLVED]** — a group said to be formed by a former police officer for police witnesses | B @ 00:26:43 |
| `Marco Rodriguez` | — | **[UNRESOLVED]** — credited with a DMT proof protocol | B @ 01:00:07 |
| `Kufos` | **CUFOS** | [PHON?] high | B @ 00:15:07 |
| `new fork` / `muon` | **NUFORC** / **MUFON** | [PHON?] high | B @ 01:05:39 |
| `Lyn Molten` | **Linda Moulton Howe** | [PHON?] high | B @ 01:04:34 |
| `Edward Euler Condon` | **Edward Uhler Condon** | [PHON?] high | C @ 01:04:54 |
| `M262 jet fighter` | **Me 262** | [PHON?] high | C @ 00:53:59 |
| `Arial` / `Aeriel` School | **Ariel School, Ruwa** | [PHON?] high | C @ 00:30:44 |
| `Lino` (Japan, near Fukushima) | **Iino** | [PHON?] medium | C @ 00:30:44 |
| `Mike Masters` / `Michael Masters` | **Michael Masters** | [CONF] | C @ 01:17:30 |
| `13th security night photo squadron` | — | **[UNRESOLVED]** — not a valid USAF designation. The Big Sur film unit is documented elsewhere under a different numbering | D @ 01:11:09 |
| `Jeffrey Cruikshank` | — | **[PHON?] low** — named as Coulthart's co-researcher on Bluegill. The caption also renders a possessive as `Jifs`, which suggests the given name is not "Jeffrey" as heard | D @ 01:00:06, 01:00:37 |
| `Tom Farmer`, general counsel of the CIA | — | **[UNRESOLVED]** — offered as a Malmgren CIA-connection data point. The CIA's long-serving early general counsel was Lawrence Houston; do not assert either way | D @ 01:07:17 |
| `Ronnie Vernet` | — | **[UNRESOLVED]** — credited with the fuel-tank visual match to the Buga sphere | D @ 00:03:18 |
| `Jim Marrs` | — | **[PHON?] / collision risk.** Described as "a former rock promoter who worked with Willie Nelson" with a house in Texas. A well-known Texas UFO and conspiracy author of the same name died in 2017 and does not match that description. **Two different people or a corrupted name; do not merge them** | D @ 00:06:39 |
| `Rhys Dalton Moore` → `Rhys Dalton Morgan` | **Rhys Dalton Morgan** | [PHON?] medium — the speaker self-corrects on air | D @ 00:50:07 |
| `Larry Sanders` → `Richard Sauder` | **Richard Sauder** | [CONF] — self-corrected on air | D @ 01:30:01 |
| `Sand Corp`-style: `Thunder Corporation` | **Thunder Scientific Corporation** | [PHON?] high — matches the existing board node | E @ 01:39:24 |
| `the author was Talbot` | **Ansel E. Talbert** | [PHON?] medium. **See §6 item 15 — the newspaper is also wrong** | E @ 00:15:35 |
| `Saunders-Sakharov` | **Sakharov** | [PHON?] medium — probably caption noise on a single name | E @ 00:19:26 |
| `John Bletch` | — | **[UNRESOLVED]** — named as a DARPA program manager Michels interviewed | E @ 01:11:32 |
| `Galaxis Chaos` | **Galaxias Chaos** | [PHON?] medium — a Mars quadrangle feature name | E @ 00:38:23 |
| `Site 51` | **Area 51** | [PHON?] high — used interchangeably by the same speaker in the same passage | E @ 01:12:04 |
| `Stan Moore` → `Bill Moore` | **William L. Moore** | [CONF] — self-corrected on air | E @ 01:39:56 |
| `Fred Baker`, `Rory`, `Jordan`, `Mr. K`, `Mr. D`, `Mr. Ko` | — | **[UNRESOLVED] / deliberately anonymous.** Skywatcher personnel. "Mr. K" and "Mr. D" are stated to be anonymous by the speakers' own choice; the others are given names only | A @ 01:07:12, 01:13:15, 00:05:05 |

---

## What is thin here, stated plainly

- **File A contributes almost nothing structural.** It is a detailed observational taxonomy of nine
  UAP classes with no documents, no dates that can be pinned, no named counterparties in government,
  and a primary witness whose name the captions cannot resolve. Its one board-relevant contribution
  is negative and worth recording as such: the speaker states flatly that he is not a whistleblower,
  held no relevant clearance, and that everything Skywatcher has done is commercial [A @ 00:26:20].
- **File B is a family memoir, not an investigation.** Its value is three specific, datable,
  archive-checkable facts about J. Allen Hynek — the APL proximity-fuse clearance, the 1973 Armstrong
  cruise, and the post-1970 Blue Book consultancy — embedded in about 100 minutes of DMT, Monroe
  Institute and conference anecdote. It is also the one file in this group that is **not** from Jesse
  Michels's channel, which matters if this slice is being filed under his name.
- **The 1940s–1980s thread, which is the most valuable content here, is scripted narration, not
  testimony**, and it contains at least four checkable factual errors (§6 items 1, 3, 14, 16). It
  should be treated as a **bibliography of leads** — Witten's AIP interview, Schatzkin's book,
  the Brown Navy file, the 1992 *Aviation Week* piece — rather than as a source.
- **Nothing in this corpus corroborates anything else in it.** Where two speakers agree — Puthoff's
  "either it failed or it went black" appearing in both C and E, Sarbacher appearing in both C and D
  — they are reading the same small secondary literature. CLAUDE.md §2's third corollary applies
  directly: two agents agreeing is not corroboration when they share a method.
