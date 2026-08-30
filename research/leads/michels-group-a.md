# Michels corpus, group A: structural extraction

**Source:** `research/.transcripts/`, six cached auto-transcripts pulled from the Jesse Michels
feed (`tools/fetch_transcripts.py`). Read in full, 30 August 2026.

**Status of everything below: UNVERIFIED LEAD MATERIAL.** Every line records what a named
speaker *claims*, attributed, with a file id and timestamp. Nothing here is asserted as
true and nothing here is graded. Citations are `[<id> @ HH:MM:SS]`, the start of the caption
block containing the statement. No quotation exceeds a short phrase; where wording matters
the pointer is given so the claim can be re-read at source.

**Treat every timestamp as a scrub position, plus or minus about thirty seconds.**
`tools/read_transcript.py` flushes a block roughly every 30 seconds counted **from the first
segment inside the requested range**, so the printed block start moves by up to half a minute
depending on the `--from` value used. These were read in 25-minute windows starting at
multiples of 25, so `--from 0 --to 25`, `--from 25 --to 50` and so on will reproduce them
exactly; any other window will land a few seconds off. Do not treat a timestamp here as an
exact offset, and do not "correct" one against a differently windowed read.

**Auto-transcript warning applies to every proper noun in this file.** These are machine
captions with heavy proper-noun corruption. In one file the same person renders as
`Kutoff`, `Halpoff` and `put off`. The governing precedent is the sibling board's
"Holocron Engineering", which was **HoloChron LLC**. Names below are marked:

- **[CONF]**: spelled consistently and matches a well-attested public figure or organisation.
- **[PHON?]**: phonetically corrupted; my reconstruction is given with the raw caption form
  in `backticks`. **Treat as a search string, not a fact.**
- **[UNRESOLVED]**: I could not reconstruct it. Recorded raw. **Must not reach the board
  under the spelling in the transcript.**

Section 7 is the full watchlist. Six names in it were resolved against the open web during
this pass and are marked **[SPELLING CHECKED]**; that means the spelling was checked and
**nothing else was**. The claims attached to them remain unverified.

---

## 0. FILE IDENTIFICATION

| id | show | participants | my confidence | dating |
|---|---|---|---|---|
| `h7CJoGKvx3U` | The Joe Rogan Experience | Joe Rogan + **Eric Weinstein** | **high**, both named on air, Rogan's own intro, Weinstein names his own work (geometric unity, the portal) | **~21-22 February 2023.** Internal: Putin's public exit from the nuclear treaty "today"; Biden's Kyiv visit; "February 1st of 2023 is the exact 50th anniversary"; Jeff Beck's death spoken of as recent |
| `yGtVzBbUvx4` | American Alchemy | Jesse Michels + **Matthew Brown** | **high**, Brown named repeatedly on air, host addressed as Jesse | **2026.** Internal: "White Sands in February of 2026"; "Department of War" video drops; the Sept 2025 hearing discussed in past tense |
| `qAou_h1POWs` | American Alchemy | Jesse Michels + **Deep Prasad** | **high**, both named on air | **~2021-2022.** Internal: Prasad "26 years old", the $15M raise spoken of as current |
| `dzTZbSNsKV8` | American Alchemy | Jesse Michels + **Dr Gary Nolan** | **high**, named in the cold open, Stanford lab named, sign-off names the show | undated internally. Vallée/Pasulka *Trinity* thesis referenced as current |
| `LGQkkHuwm6w` | "On the Record", a Las Vegas broadcast programme | host addressed only as **"George"** + **John Lear** | show title **stated**; Lear **named**; host identity is **INFERENCE**, see below | **~28 September 1987.** Internal: Reagan's address to the 42nd UN General Assembly "one week ago", 21 September; London Evening News of 21 July 1987 held up as recent |
| `sF03FN37i5w` | a recorded lecture, not an interview | **Rupert Sheldrake** (self-identified by book and hypothesis) | **high** | undated internally |

**On the `LGQkkHuwm6w` host.** The only internal evidence is the first name "George", the
programme name "On the Record", a Las Vegas setting and a UFO brief. That is consistent with
one well-known Las Vegas broadcast journalist the board already carries, but the transcript
never says a surname and **I did not confirm it**. Record the file as "host: George
[surname unestablished]" until someone checks the broadcast itself.

### The off-topic file

**`sF03FN37i5w`, Rupert Sheldrake, "The Science Delusion" lecture. NOT ON TOPIC.** It is a
philosophy-of-science talk on ten materialist dogmas, morphic resonance, and the constants
of nature. It contains **zero** UAP content, zero programme content, zero institutions
relevant to this board. It is thematically adjacent to `yGtVzBbUvx4`'s "suppression of
science" frame and nothing more. Do not manufacture a link. Two checkable items it does
contain, offered only so nobody has to read it again:

- Sheldrake claims the measured speed of light **dropped ~20 km/s between 1928 and 1945**,
  that he found this in old physics handbooks at a patent office library in London, and
  that the head of metrology at the **National Physical Laboratory, Teddington** [CONF]
  called it "intellectual phase locking" `[sF03FN37i5w @ 00:11:15]`.
- He says the speed of light was "fixed by definition in **1972**" `[sF03FN37i5w @ 00:11:15]`.
  **That date needs checking**; the SI redefinition of the metre in terms of *c* is normally
  dated later. This is the single checkable factual claim in the file.

Everything from here on excludes `sF03FN37i5w`.

---

## 1. ENTITIES

### 1a. Government offices, programmes and oversight bodies

| Name | Role the speaker assigns it | Cite |
|---|---|---|
| **Immaculate Constellation** [CONF] | Brown: an **operational, unacknowledged SAP** governing ISR of UAP worldwide, using tasked and untasked collection. He saw a ~12-15 slide senior-leadership capabilities brief, drafted around 2018 | `yGtVzBbUvx4 @ 00:10:01, 00:12:49, 00:22:15` |
| **National Security Council** [CONF] | Brown's central custody claim: the briefing presented MCON as a **DoD** programme, but he says he "came to learn later" it is **owned and run out of the NSC**, with a specific director as cognizant authority | `yGtVzBbUvx4 @ 00:20:02, 01:34:35` |
| **OSD Policy / USD(P)** [CONF] | Brown's own posting: contractor policy adviser on the counter-WMD mission under the Under Secretary of Defense for Policy | `yGtVzBbUvx4 @ 00:07:48` |
| **SAPCO** (Special Access Program Coordinating Office) [CONF] | The third rung of Brown's spillage-reporting chain. He says he was told to sign nothing and go away | `yGtVzBbUvx4 @ 00:57:46` |
| **Schriever AFB, Colorado** [PHON? caption `Shrivever`] | Named in Brown's cleared report as at least one hub of the MCON mission | `yGtVzBbUvx4 @ 00:16:41` |
| **NRO "Sentient"** [CONF] | Brown: an enabler integrated with MCON; AI-driven cueing and, in his word, compartmentalisation of collection events | `yGtVzBbUvx4 @ 00:59:25` |
| **NGA "Marsupial"** [UNRESOLVED as a programme] | Asked directly whether it relates; Brown answers **"no comment"**. The no-comment is the datum | `yGtVzBbUvx4 @ 00:59:59` |
| **CIA Office of Global Access / Rapid Response** [CONF] | Brown: no exposure of his own, but "all the public reporting" on it is plausible | `yGtVzBbUvx4 @ 01:00:33` |
| **AFOSI** [CONF] | Brown: an AFOSI officer was proven to be interfering with another (non-public) UAP whistleblower and family | `yGtVzBbUvx4 @ 03:12:17` |
| **Office of Net Assessment / Andrew Marshall** [CONF] | Brown places his own skill set under net assessment and names Marshall and ONA | `yGtVzBbUvx4 @ 00:52:18` |
| **AATIP** [PHON? caption `ATIP`, `OAP`] | Michels: "$22 million budget", offered as too small to house a global collection network. Brown: the briefing's claim that MCON was created *in response to* the 2017 Elizondo disclosure is a **half-truth planted as a counterintelligence marker** | `dzTZbSNsKV8 @ 00:04:28`; `yGtVzBbUvx4 @ 00:36:42, 00:40:37` |
| **AARO** [CONF] | Michels and Brown both treat it as either suppression or a flytrap. Michels raises AARO's **Latin motto**, glossed on air as "our life is what our thoughts make it", as a tell | `yGtVzBbUvx4 @ 01:28:25` |
| **UAP Task Force** [CONF] | Nolan cites "the five observables of the UAP task force" | `dzTZbSNsKV8 @ 00:12:19` |
| **Project Blue Book** [CONF] | Lear's 1987 framing: government scientists who worked on it are "ready to talk" | `LGQkkHuwm6w @ 00:00:35` |
| **MJ-12** [CONF as a term] | Lear: the controlling body; a president takes 3-4 months to be cleared; part of MJ-12 wants release and part does not | `LGQkkHuwm6w @ 00:11:45, 00:24:39` |
| **Project Preserve Destiny** [CONF as a term] | Michels, relaying Dan Sherman: a 1960 genetic-management project; **a FOIA to the Air Force is forwarded to NSA**, which Michels reads as a tell that it exists | `yGtVzBbUvx4 @ 01:17:13` |
| **Stargate** [CONF] | Michels: CIA remote viewing, 1970s to 1990s, on the record | `yGtVzBbUvx4 @ 01:23:18` |
| **Department of Energy / national labs** [CONF] | Brown: reverse engineering reverse engineering "is ran out of our national labs", and the defence contractors "most probably"; national labs are where exotic samples are stored | `yGtVzBbUvx4 @ 01:01:44, 02:27:54` |
| **Los Alamos National Laboratory** [CONF] | Brown ties anomalous interest at White Sands to nearby Los Alamos; separately places Paperclip "true believers" there | `yGtVzBbUvx4 @ 02:24:32, 02:28:27` |
| **Redstone Arsenal, Huntsville** [CONF] | Brown's other Paperclip grouping, the "Nazis in name only" | `yGtVzBbUvx4 @ 02:28:27` |
| **Mansfield Amendment** [CONF] | Weinstein: **discontinued DoD "blue sky" funding inside universities**, and is the mechanism that ends the 1953-73 period. He dates it **1973** and attributes it to Mike Mansfield of Montana | `h7CJoGKvx3U @ 01:06:56` |
| **Bayh-Dole** [PHON? caption `B Dole Amendment`], **1980** | Weinstein: one of a chain of instruments devitalising American science | `h7CJoGKvx3U @ 01:10:54` |
| "**the eberg amendment 1973**" and "**the ation Act of 1990**" | [UNRESOLVED] Two instruments Weinstein names in the same breath as Mansfield and Bayh-Dole. **Neither is reconstructible from the caption.** Do not guess | `h7CJoGKvx3U @ 01:10:54` |
| **Institute for Advanced Study, Princeton** [CONF] | Weinstein: a directorate and faculty dominated by string theory; also the body Oppenheimer invoked when he told GRF prize winners to return the money | `h7CJoGKvx3U @ 01:01:16, 01:17:11` |
| **Case Explorer / RISS Safe / "Safety Net"** [PHON? captions `case Explorer`, `RS safe`, `safety net`] | Weinstein: three law-enforcement **deconfliction** systems. He says he phoned the South Florida one, talked for half an hour, asked about Epstein and was cut off | `h7CJoGKvx3U @ 02:53:27, 02:55:03` |

### 1b. Contractors, companies and private institutes

| Name | Role the speaker assigns it | Cite |
|---|---|---|
| **Amentum Corporation** [CONF, **SPELLING CHECKED**] | Brown's tweet to Elon Musk directs him to **Pax River special project hangars "owned by Amentum"**. Brown adds: "they own parts of EG&G" | `yGtVzBbUvx4 @ 01:52:17, 01:57:22, 01:58:33` |
| **EG&G** [CONF] | Michels: filmed atomic tests, therefore first access to detonation imagery; Lazar's employer of record | `yGtVzBbUvx4 @ 01:58:33` |
| **Northrop Grumman** [CONF] | Brown: has been given authority to run **programme security through its corporate security forces**, including deniable retribution against people who speak. Also his revolving-door example: a Northrop president becoming USD(P) needs no read-in | `yGtVzBbUvx4 @ 01:37:30, 01:40:37` |
| **TRW** [CONF] | Brown's FOIA advice: search **"advanced reconnaissance vehicle"** rather than "alien reproduction vehicle", and "you'll find some things from TRW" | `yGtVzBbUvx4 @ 00:33:51` |
| **Glenn L. Martin Company → Martin Marietta → Lockheed Martin** [CONF] | Weinstein: Babson got the Glenn L. Martin company to hire Louis Witten and stand up an anti-gravity-inspired research institute | `h7CJoGKvx3U @ 01:05:16` |
| **Research Institute for Advanced Study (RIAS), Baltimore** [CONF] | Weinstein's central undocumented institution. Formed by Louis Witten under Martin. Names attached: **Solomon Lefschetz** [PHON? `Solomon lefet`], **Rudolf Kalman** [PHON? `Rudolph Colman of Colman filtering`], **Sheldon Glashow**. He says Brown University's Center for Nonlinear Dynamics is a spin-out of Lefschetz's RIAS work | `h7CJoGKvx3U @ 01:05:48, 01:06:21` |
| **Gravity Research Foundation**, New Boston, New Hampshire [CONF] | Founded by Roger Babson; funds the **annual essay competition**; Weinstein describes stone monuments placed at US universities and reads the Tufts one aloud on air | `h7CJoGKvx3U @ 01:03:33, 01:05:16` |
| **Institute of Field Physics, UNC Chapel Hill** [CONF] | Weinstein: funded by Bahnson through Bryce DeWitt; the sponsor of the conference Feynman's "It's Greek to Me" story is about | `h7CJoGKvx3U @ 01:16:06` |
| **Curtiss-Wright, Buffalo** [PHON? caption `Curtis Wright`] | Weinstein reads a Feynman anecdote about lecturing aerospace engineers in Buffalo as pointing at Curtiss-Wright | `h7CJoGKvx3U @ 01:15:33` |
| **Renaissance Technologies / Medallion** [CONF] | Weinstein relays Isadore Singer calling it "the world's greatest mathematics and physics department"; groups it with Brookhaven National Laboratory and SUNY Stony Brook as a possible Manhattan-Project-in-plain-sight | `h7CJoGKvx3U @ 01:30:44, 01:31:18` |
| **Quantum Generative Materials (GenMat)** [CONF, **SPELLING CHECKED**] | Prasad's company. **$15 million raised**, mission stated as reverse-engineering UAP materials via quantum simulation of the many-body Schrödinger equation | `qAou_h1POWs @ 00:00:00, 00:06:39` |
| **Lockheed "Dark Ice" magnetometer** [CONF, **SPELLING CHECKED**] | Prasad: Lockheed observed the robin cryptochrome mechanism and built a quantum magnetometer giving GPS-grade navigation without satellites, "as of six years ago" | `qAou_h1POWs @ 00:14:55` |
| **Prometheus Entertainment / Skinwalker Ranch** [CONF] | Weinstein: the show "looks incredibly junky", but he knows **Brandon Fugal** and speaks regularly with **Erik Bard** [PHON? `Eric Bard`], whom he calls the only other person out there who speaks tensor analysis | `h7CJoGKvx3U @ 02:46:50` |
| **EcoHealth Alliance** [CONF] | Weinstein: "wildly overpowered" board including his old mentor, the head of the Sloan Foundation, and a former head of NSF. Offered as an example of a statecraft workaround, not a UAP claim | `h7CJoGKvx3U @ 02:57:52` |
| **Vanguard Enterprise** [CONF] | Brown's new nonprofit for UAP whistleblowers, with **Dylan Borland** and **Jeffrey Nuccetelli**. He gives the domain on air | `yGtVzBbUvx4 @ 03:16:17` |
| **World Commerce Corporation** and "the Maynard Corporation" | [UNRESOLVED as characterised] Michels attributes a Caribbean shell-company constellation to a researcher's analysis and to Tom DeLonge's book. **This is Michels talking, not Brown**; Brown says only that Nazi networks persisted | `yGtVzBbUvx4 @ 02:30:00` |

### 1c. People, and the role assigned

| Name | Role assigned | Cite |
|---|---|---|
| **Matthew Brown** [CONF] | Self: contractor policy adviser, OSD Policy, counter-WMD; found the MCON brief while cleaning a classified file system; reported it up three rungs; became a congressional whistleblower years later, **after being asked to** | `yGtVzBbUvx4 @ 00:07:48, 00:10:35, 00:55:37` |
| **Eric W. Davis** [CONF] | Weinstein: **the only person he can find who speaks the physics**, other than possibly Puthoff. Davis allegedly told him "the three most technical people on this" | `h7CJoGKvx3U @ 01:22:12` |
| **Hal Puthoff** [PHON? captions `Hal Kutoff`, `Halpoff`, `put off`] | Nolan: sourced the bismuth sample and supplied the terahertz waveguide claim. Michels: laser physicist, SRI, started the psychic spy programme, has briefed multiple presidents. Weinstein: an uncomfortable interview; he pressed Puthoff on why remote viewing was used to raise a fixed sum for a school rather than repeatedly | `dzTZbSNsKV8 @ 00:21:03`; `h7CJoGKvx3U @ 03:11:08` |
| **Louis Witten** [PHON? caption `Lewis Whitten`] | Weinstein: hired out of Johns Hopkins by the Martin company to run RIAS; father of Edward Witten; "still alive now 101 years old" | `h7CJoGKvx3U @ 00:59:34, 01:05:16` |
| **Edward Witten** [PHON? caption `Edward Whitten`, `Ed Wht`] | Weinstein: the dominant mind in theoretical physics; son of the most prominent anti-gravity researcher of the 1950s; the person whose 1984 ruling for string theory Weinstein blames for the stagnation | `h7CJoGKvx3U @ 00:48:03, 01:00:08` |
| **Bryce DeWitt** [PHON? caption `Bryce dwit`, "formerly Bryce Seligman"] and **Cécile DeWitt-Morette** [PHON? `Cecil dit Moret`] | Weinstein: the husband-and-wife half of the two families quantum gravity descends from; DeWitt **repurposed the Gravity Research Foundation essay competition** away from anti-gravity devices toward quantum gravity | `h7CJoGKvx3U @ 00:59:34, 01:16:06` |
| **Roger Babson** [CONF] | Weinstein: made a fortune predicting the 1929 crash, founded the Gravity Research Foundation after a sister drowned, formed a collective with **Edison** and **Clarence Birdseye** | `h7CJoGKvx3U @ 01:02:23` |
| **Agnew Bahnson** [PHON? caption `agnu banson`] | Weinstein: the other money; funded the Institute of Field Physics through Bryce DeWitt | `h7CJoGKvx3U @ 01:00:08, 01:16:06` |
| **Richard Arnowitt and Stanley Deser** [PHON? caption `arit and deser`] | Weinstein: entered and won the Gravity Research Foundation competition; **Oppenheimer told them to return the money** for using the Institute's name on pseudoscience; they kept it, and afterwards Penrose, Witten and Martin Perl entered | `h7CJoGKvx3U @ 01:17:11` |
| **Hermann Bondi** [CONF] | Weinstein: his paper at the 1957 Chapel Hill conference is **on negative mass in general relativity**, which Weinstein reads as the respectable face of the same question | `h7CJoGKvx3U @ 01:41:09` |
| **Thomas Townsend Brown** | **Named by Michels, endorsed as a thread by Matthew Brown.** Michels asks whether the non-chemical propulsion "roots back to Thomas Townsend Brown"; Brown answers that it is "a really interesting thread to pull" and says he learned of the electrogravitics association only later | `yGtVzBbUvx4 @ 01:55:42` |
| **Dan Sherman** [CONF] | Michels: USAF electronic intelligence; *Above Black*; Project Preserve Destiny; binaural tones and sine-wave collapse; posted at **San Vito dei Normanni** [PHON? `San Vito denormy`] and **Offutt** [PHON? `off it`] | `yGtVzBbUvx4 @ 01:17:13` |
| **Andrija Puharich** [PHON? caption `Andre Puharic`, `Buharic`] | Michels: MK-Ultra-adjacent, hypnotised "space kids" at **Ossining, New York** [PHON? `Austining`], channelling "the Nine"; documentary *Mind Traveler* by **Greg Malazi** [PHON?] | `yGtVzBbUvx4 @ 01:21:38` |
| **Kit Green** and **"K. Randall May[hew]"** [PHON?] | Michels: a leaked phone call between them about field checks on contactees feeding back to CIA | `yGtVzBbUvx4 @ 01:20:30` |
| **Jake Barber** [CONF] | Brown/Michels: the "egg" retrieval account; book *Sentinels of Ether*, first chapter published with 7 of 20 pages redacted by subject-matter experts | `yGtVzBbUvx4 @ 01:44:29, 02:46:14` |
| **Michael Herrera** [PHON? caption `Michael Herreras`] | Michels: Indonesia, a ~300 ft craft, an intercepting American-accented force, now believed by him to have been moving human cargo | `yGtVzBbUvx4 @ 02:44:31` |
| **Kirk McConnell** [CONF] | Brown: names him unprompted on **extended electrodynamics**, and says "no accident Kirk came to this show first". Michels places him on Senate Armed Services under **Jack Reed** | `yGtVzBbUvx4 @ 03:00:36` |
| **Thomas Bearden** [CONF] | Brown: "a limited hangout mixed with disinformation" covering a core truth about scalar/longitudinal propagation | `yGtVzBbUvx4 @ 03:03:23` |
| **John Lear** [CONF] | Self, 1987: airline captain, 17 world speed records, Lear family, former state senate candidate; father and brother both saw objects | `LGQkkHuwm6w @ 00:01:09` |
| **Gen. Gordon Williams** [CONF as spoken] | Lear: Wing Commander at Bentwaters, allegedly approached by three occupants, witnessed by a security policeman Lear says he met | `LGQkkHuwm6w @ 00:02:17` |
| **Leonard Stringfield** [CONF] | Lear: worked for the Air Force in the early 1950s on a secret UFO-reporting project, then privately; the autopsy drawing shown on air came **from his collection** | `LGQkkHuwm6w @ 00:08:57` |
| **Bruce Maccabee** [CONF] | Lear: physicist at the "Naval Surface weapons laboratory"; author of a **26-page report** on the JAL incident containing ATC transcript, FAA radar plots and Air Force plots | `LGQkkHuwm6w @ 00:20:06` |
| **Linda Moulton Howe** [CONF] | Lear: made *A Strange Harvest* for the Denver CBS affiliate; his source for a 9,000-mutilation figure, 1975-1980 | `LGQkkHuwm6w @ 00:05:05` |
| **Gary Nolan** [CONF] | Self: Stanford; the CIA came to his office because of a tool he built, rendered `SaitTo` [PHON? almost certainly CyTOF]; shown MRIs of DoD and IC personnel with UFO interactions | `dzTZbSNsKV8 @ 00:05:02` |
| **Jacques Vallée** [PHON? caption `Jacques Valet`, `Jacqu Valet`] | Nolan: collects and forwards materials to him. Michels' framing: computerised map of Mars at NASA, ARPANET work with **Doug Engelbart**, the model for the French scientist in *Close Encounters* | `dzTZbSNsKV8 @ 00:09:32` |
| **Diana Pasulka** [PHON? caption `Diana Pulka`] | Nolan: co-author of the thesis he "likes best", that Roswell 1947 is a dividing line in what witnesses report | `dzTZbSNsKV8 @ 00:15:33` |
| **Robert Bigelow** [PHON? `Bigalow`], **Colm Kelleher** [PHON? `Col Kellaher`], **Eric Davis** | Nolan: the "invisible college" he was introduced to | `dzTZbSNsKV8 @ 00:05:35` |
| **Deep Prasad** [CONF] | Self: quantum computing founder; cites **Eric Weinstein** as "my colleague" twice and recounts a joint conversation with Puthoff | `qAou_h1POWs @ 00:00:33, 00:04:23` |

### 1d. Facilities and places

| Name | Role assigned | Cite |
|---|---|---|
| **Patuxent River (Pax River)** [CONF] | Brown: "special project hangers owned by Amentum"; notes that a congressman got a tour and was shown nothing exotic, which Brown reads as evidence about candour to elected officials | `yGtVzBbUvx4 @ 01:57:22` |
| **Vandenberg** [CONF] | Nuccetelli's triangle over the runway | `yGtVzBbUvx4 @ 00:28:52` |
| **Langley, 2012** [CONF] | Borland's ~100 ft equilateral triangle from near a NASA hangar | `yGtVzBbUvx4 @ 00:29:24` |
| **White Sands, February 2026** [CONF as an event claim] | Michels: TFRs, FAA airspace closure, and a 10-day El Paso airport closure for "special security reasons". **Brown does not confirm it**; he says only that White Sands generally draws anomalous interest | `yGtVzBbUvx4 @ 02:23:59` |
| **Malmstrom, Oscar Flight, 1967** [CONF] | Michels, relaying Salas: a red orb, nine of ten missiles to no-go | `yGtVzBbUvx4 @ 01:41:44` |
| **Bentwaters, 1980** [CONF] | Lear's entry point into the subject, via a retiring Air Force friend | `LGQkkHuwm6w @ 00:02:17` |
| **Nevada Test Site / Nellis** [CONF] | Lear: at least one intact craft there, "being flown as of 1981" | `LGQkkHuwm6w @ 00:24:05` |
| **SUNY Stony Brook / Brookhaven / Simons Center** [CONF] | Weinstein: where he would site a Manhattan Project in plain sight | `h7CJoGKvx3U @ 01:29:36, 01:31:18` |
| **UT Austin gravitational group** [CONF] | Weinstein's other candidate; successor to the Institute of Field Physics; names **John Archibald Wheeler**, **Steven Weinberg**, **Bryce DeWitt** | `h7CJoGKvx3U @ 01:29:01` |
| **Colorado Springs** [CONF] | Weinstein: where the people promising him disclosure kept saying they would fly him, blindfolded, for three years. It never happened | `h7CJoGKvx3U @ 01:18:52, 01:19:26` |
| **Ubatuba, Brazil** [PHON? caption `Uba Tuba`] | Nolan: the magnesium sample provenance, via a fisherman and an exploding orb | `dzTZbSNsKV8 @ 00:10:05` |

---

## 2. DOCUMENTS AND PRIMARY RECORDS NAMED

Anything below could in principle be pulled by someone else. **Nothing below has been pulled.**

| Record | As described | Cite |
|---|---|---|
| **The Immaculate Constellation capabilities brief** | PowerPoint, ~12-15 slides, drafted ~2018, placeholder slides for SAP insert, **no proper portion markings**, edit history readable in file metadata. **Deleted after Brown reported it.** He never removed a copy | `yGtVzBbUvx4 @ 00:12:14, 00:35:35, 00:58:18` |
| **Brown's report to Congress**, and the separate **State Department cleared public version** | Seven categories of evidence, only one of which is MCON. He is explicit that the public version is narrower than what he wrote, and that what he wrote is narrower than what he saw | `yGtVzBbUvx4 @ 00:17:47, 03:08:25` |
| Named entries inside that report | CENTCOM: FMV/FLIR of **12 metallic orbs** skimming the ocean then dispersing. INDOPACOM: **large disc emerging from cloud**, OPIR. NORTHCOM: **"jellyfish" crossing the US-Mexico border**. SOUTHCOM: a **tic tac near a vessel, with correlated MASINT electromagnetic signatures**. Plus a geometry taxonomy (Table 2 = disc/saucer) | `yGtVzBbUvx4 @ 00:41:13, 00:43:31` |
| **Congressional hearing exchange with Luis Elizondo** | Asked whether he was read into Immaculate Constellation; answers that he is not authorised to confirm or deny, "by name or trigraph". Michels reads that as a yes | `yGtVzBbUvx4 @ 00:37:16` |
| **The "NID study"** [PHON? caption `NID`] on triangles | Late 1990s / early 2000s; correlates triangle sightings to **US naval bases** | `yGtVzBbUvx4 @ 00:28:19` |
| **The 1971 US-USSR notification agreement** | Michels calls it "that 1970 something outer space treaty" and "1971 SALT talks". **Both labels are wrong; the instrument is real.** See §5 and §6 | `yGtVzBbUvx4 @ 01:08:59` |
| **The Podesta / "Bob Fish" email on fast walkers** | Michels: a leaked email about DSP geostationary sensors detecting fast walkers; **John Greenwald** filed on it and got nothing back. Brown does not confirm the term from the inside | `yGtVzBbUvx4 @ 02:11:09` |
| **Trevor Paglen's black-project patch compilation** [PHON? caption `Trevor Pagglin`] | Brown cites it approvingly as evidence that programme people signal in plain sight | `yGtVzBbUvx4 @ 01:29:31` |
| **Bluegill Triple Prime footage** | Michels: EG&G film from aircraft "Kettle One" and "Kettle Two" showing an object leaving the plume; **Tim Gallaudet** [PHON? `Tim Galedet`] says the **Navy deck logs** around it read as a radioactive retrieval | `yGtVzBbUvx4 @ 01:58:33` |
| **Brown's Elon Musk tweet**, read out in full | Contains: a White House predictive AI claim; "Amentum Corp" and Pax River hangars; "Department of Energy and Propulsion"; **SIRIUS** spelled out as a star system and asserted to also be a programme name; "rockets feel so 1947"; and the sign-off `MMTU` [UNRESOLVED, he refuses to gloss it] and `ABORYMON`, which he glosses as an **Enochian angel from the Sigillum Dei Aemeth** | `yGtVzBbUvx4 @ 01:52:17, 02:00:50` |
| **"Introductory Space Science, Volume II", Department of Physics, USAF Academy** | Lear reads the alien-description passage aloud on air and says it is **"chapter 13"**. **The UFO chapter is Chapter XXXIII (33)**, checked. Either Lear misspoke or the caption garbled it; the document is real and pullable | `LGQkkHuwm6w @ 00:06:13` |
| **The Halt memo and the Halt tape** | Lear: the memo came out under FOIA and omits the landing; the tape runs about eight hours and he has a 20-minute segment | `LGQkkHuwm6w @ 00:02:51` |
| **An autopsy drawing by an Army surgeon**, Roswell 1947 | Shown on air; Lear reads a list of findings from it; provenance given as **Leonard Stringfield's private collection** | `LGQkkHuwm6w @ 00:07:52, 00:08:57` |
| **Reagan, White House speech text, 4 December 1985** | Lear holds up a copy and reads the "threat from another planet" passage | `LGQkkHuwm6w @ 00:12:18` |
| **Reagan, address to the 42nd UN General Assembly, 21 September 1987** | Read aloud: the "alien threat from outside this world" passage, followed by Reagan's own gloss that war is the alien force | `LGQkkHuwm6w @ 00:13:26` |
| **Carter campaign statement on UFO disclosure** | Read aloud | `LGQkkHuwm6w @ 00:13:59` |
| **Maccabee's 26-page JAL report** | ATC transcript, FAA radar plots, Air Force plots, and the captain's own scale drawing, which is shown on air | `LGQkkHuwm6w @ 00:20:06` |
| **A 150-page report on the 1975 SAC overflights** | Lear says he holds it; describes interceptors, helicopters, notification of Canadian authorities, and security patrols sent to the perimeter | `LGQkkHuwm6w @ 00:23:32` |
| **London Evening News, 21 July 1987** | Read aloud: Vatican theologians on extraterrestrial life and training missionaries; the Vatican Observatory is placed at "frascati near Rome" [PHON? / geographically doubtful] | `LGQkkHuwm6w @ 00:22:22` |
| **Prasad's blog posts, by title** | "The Evolution of Science and the Interactive Universe"; "Curiosity as a Time Capsule"; and one titled as resolving quantum mechanics while debunking every UFO case, **which he says was an April Fool's prank** | `qAou_h1POWs @ 00:16:34, 00:23:18, 00:23:53` |
| **The Stanford NanoSIMS measurements on the Ubatuba magnesium** | Secondary ion mass spectrometry in the engineering department; isotope ratios reported as anomalous. **No paper is named** | `dzTZbSNsKV8 @ 00:10:39` |
| **Jake Barber, *Sentinels of Ether*** | First chapter released; **7 of 20 pages redacted** by subject-matter experts | `yGtVzBbUvx4 @ 02:46:14` |
| **Dan Sherman, *Above Black*** | Michels: recommended to him by insiders as a credible disclosure | `yGtVzBbUvx4 @ 01:17:13` |

---

## 3. THE STRUCTURAL ARGUMENT

**Two incompatible accounts of the programme are being advanced across these files, and the
corpus does not reconcile them.**

Matthew Brown's account (`yGtVzBbUvx4`) is the one with an institutional shape, and it is
notable for what it does **not** claim. Brown separates a **collection** function from a
**custody** function and says he only ever touched the first. On collection, his claim is
that UAP ISR is not a niche office but a global, long-established mission riding on the
existing national collection architecture: space, terrestrial, airborne and seaborne
sensors, IMINT plus MASINT, with the returns collated and, on his reading, cued and
compartmented by AI. The organisational punch line is a custody claim: the briefing he saw
presented it as DoD, and he now says it is **owned by the National Security Council**, with
a named director as cognizant authority, DoD merely implementing. That inverts the usual lore
in which the president is a transient outsider. On the second function, reverse engineering,
Brown says he had **no direct exposure**, and attributes it to the national labs and defence
contractors on the strength of what he was told afterwards. His mechanism for how a
cross-agency secret survives is threefold: a **Nixon-to-Ford decision to privatise custody**,
so that a Northrop president moving into an under-secretary chair needs no read-in and simply
aligns resources; the **military tradition of silence**, which he says makes leaks unlikely
rather than merely punishable; and security through **trusted family lineages** traced back to
the Manhattan Project, borrowing a known intelligence-community practice. Oversight, in this
account, does not fail by accident. It fails because the programme was deliberately moved
somewhere oversight does not reach, and because the history stopped being briefed to new
entrants at all, leaving an **oral tradition** in place of a record. Funding is the one leg he
does not build: he explicitly declines the money question, saying it "kind of doesn't matter
what the numbers are" next to the capabilities and the long-term contracts.

Eric Weinstein's account (`h7CJoGKvx3U`) is not about custody at all. It is an argument
about **where the competence went**, and it is the only file in the group that offers a
falsifiable structural test. His premise is a fifty-year stagnation in fundamental physics,
dated from 1973, bracketed by a genuinely productive 1953-1973 period in general relativity.
His discovery is that the productive period's two founding families, the DeWitts and the
Wittens, were both funded out of the 1950s **anti-gravity** money: Roger Babson's Gravity
Research Foundation and Agnew Bahnson's patronage, running through the Glenn L. Martin company
into RIAS and into the Institute of Field Physics at Chapel Hill. His claim is that the
respectable field, quantum gravity, is the laundered form of the disreputable one,
electrogravitics, and that the official story ("we defrauded the cranks to fund real work") is
a face-saving reconstruction. From there he derives the test: **if there were a real
post-Einsteinian programme, it would consume differential geometers, particle theorists and
relativists**, and you could find it the way you can infer NSA from where number theorists
disappear to. He runs that test, names Stony Brook, Brookhaven, Renaissance Technologies and
UT Austin as the only plausible sites, and reports the opposite of what a programme would
predict: after three years he cannot find **one** person who speaks tensor analysis attached
to the subject. His conclusion is therefore an oversight and competence claim, not a custody
one: either the phenomenon is a deception whose designers would specifically exclude
physicists, or the responsible bureaucracy is pathologically incompetent, or a real programme
exists and is invisible to a test that should detect it. He does not choose.

The two accounts share almost nothing except a compartmentalisation complaint, and they point
research in opposite directions. Brown's model predicts that the trail runs through corporate
custody, contract vehicles and family lineage; Weinstein's predicts that it runs through
doctoral pipelines and funding instruments, and that the absence of physicists is itself the
finding. Prasad's file adds a third, weaker frame that sits closer to Weinstein: he asserts,
without evidence and with an emphatic "I know it's true", that **aerospace companies hold
basic scientific knowledge withheld from academia**, specifically in materials and topological
physics. Nolan's file is the only one that engages custody empirically, and it does so by
showing how thin it gets: his best physical samples come to him through a fisherman in Brazil
and an anonymous package with a grandfather's diary, while the material he says would matter
sits behind national-security sensitivity he cannot pierce. Lear's 1987 file is the fossil
record of the same argument sixty years earlier, and it is entirely custody: recovered craft,
stored bodies, a controlling committee, presidents briefed on a delay. What is absent from
Lear and present in Brown is any institutional plumbing at all.

---

## 4. THE 1940s-1980s THREAD

**This is the strongest result in the group, and it is concentrated in one file.**

### `h7CJoGKvx3U` (Weinstein): the thread is the spine of the episode

Weinstein delivers a continuous, named, dated account of the 1950s electrogravitics funding
network and its capture by mainstream physics, roughly `01:00:00` to `01:18:00`, with a
second pass at `01:41:00`. The chain as he gives it:

1. **Roger Babson** and **Agnew Bahnson** are "the money", both "deep into anti-gravity"
   `[@ 01:00:08]`.
2. Babson founds the **Gravity Research Foundation** at **New Boston, New Hampshire**, funded
   from a fortune he made calling the 1929 crash, with **Edison** and **Clarence Birdseye**
   in the same collective `[@ 01:02:23, 01:05:16]`.
3. GRF places **stone monuments at US universities**; Weinstein has the Tufts one pulled up
   on screen and reads its dedication aloud `[@ 01:03:33]`.
4. Babson gets the **Glenn L. Martin Company** (which he traces forward to Martin Marietta and
   then Lockheed Martin) to **hire Louis Witten out of Johns Hopkins**, who forms the
   **Research Institute for Advanced Study** in **Baltimore** `[@ 01:05:16]`.
5. Names attached to RIAS: **Solomon Lefschetz**, out of retirement; **Rudolf Kalman**, of
   Kalman filtering; **Sheldon Glashow** `[@ 01:05:48]`. Brown University's Center for
   Nonlinear Dynamics is named as a RIAS spin-out `[@ 01:06:21]`.
6. **Bahnson** funds the **Institute of Field Physics at UNC Chapel Hill** through **Bryce
   DeWitt**, who "repurposed" the GRF essay competition from anti-gravity devices to
   **quantum gravity** `[@ 01:16:06]`.
7. The **1957 Chapel Hill conference** is placed as the hinge: DeWitts, Wittens, **Feynman**
   and **Wheeler** in attendance; **Hermann Bondi's** paper there is on **negative mass in
   general relativity** `[@ 01:41:09]`.
8. **Arnowitt and Deser** win the GRF prize; **Oppenheimer** demands the money be returned for
   attaching the Institute's name to pseudoscience; they keep it, and afterwards **Penrose**,
   **Witten** and **Martin Perl** enter `[@ 01:17:11]`.
9. The period ends in **1973** with the **Mansfield Amendment**, which he says killed DoD
   blue-sky funding in universities `[@ 01:06:56]`, preceded in **1965** by Robert Maxwell's
   **Pergamon Press** and the spread of peer review `[@ 01:09:49]`, and followed by
   **Bayh-Dole (1980)** and two instruments the captions destroy `[@ 01:10:54]`.

He names the low-brow vocabulary explicitly, in a single breath: **"anti-gravity, gravity
shielding, electrogravitics, gravitodynamics"** `[@ 01:42:52]`, and states his thesis that the
high-prestige version of the same programme is quantum gravity.

**Manhattan Project lineage** is also present and heavily worked: Chadwick and the neutron
(1932), Meitner, **Chicago Pile-1** under the Chicago stands, Trinity 1945, **Ivy Mike 1952**
and the **Teller-Ulam design**, Castle Bravo, Starfish, and the Shelter Island conference of
1947 as the model for what happens when you convene the people the Manhattan Project proved
were good `[@ 00:16:17, 00:17:26, 02:05:00]`. **Feynman's** own stories are read as pointers
at the same milieu: a Buffalo lecture series to aerospace engineers, which Weinstein reads as
**Curtiss-Wright**, and a request for nuclear patents on fission-driven aircraft
`[@ 01:15:33]`.

**The AEC is not named.** Weinstein's institutional chain runs through GRF, Martin, RIAS,
Chapel Hill, IAS and the DoD funding instruments, not through the Atomic Energy Commission.

### `yGtVzBbUvx4` (Brown): the thread is present, brief, and explicitly endorsed

- **Thomas Townsend Brown is named directly by Michels and treated as a live thread by
  Brown.** Asked what propulsion a catch-up programme would be using, Brown answers
  **"Electromagnetic. Electrogravitic."** Michels then asks whether it roots back to Thomas
  Townsend Brown; Brown says it is "a really interesting thread to pull", that Michels knows
  more about him than he does, and that he learned the electrogravitics association after
  going public `[yGtVzBbUvx4 @ 01:55:42]`.
- **Bluegill Triple Prime (Operation Fishbowl, 1962)**, EG&G film, aircraft named as Kettle
  One and Kettle Two, plus Gallaudet's deck-log reading `[@ 01:58:33]`.
- **EG&G to Amentum** as a corporate custody lineage `[@ 01:57:22, 01:58:33]`.
- **Operation Paperclip split** between Redstone Arsenal and Los Alamos, with a genetics
  rider `[@ 02:28:27]`.
- **A Truman-to-Eisenhower-era "agreement"** as the oral tradition's founding event; Brown
  distances himself from the Greada version and from Michels' 1954 Palm Springs dating
  `[@ 01:11:13, 01:12:54]`.
- **Nixon-to-Ford privatisation** of custody `[@ 01:36:54]` and **family lineages traced to
  the Manhattan Project** `[@ 01:38:37]`.
- Also 1940s-adjacent: **Robert Maxwell / Pergamon / peer review** appears again here,
  independently of Weinstein, with Epstein, PROMIS and Sandia attached `[@ 02:37:44]`.

### The other three on-topic files

- **`dzTZbSNsKV8` (Nolan): thin, and mostly rhetorical.** Fermi, the Manhattan Project and
  Los Alamos appear only as an argument that a serious physicist once thought about aliens
  in his off hours `[@ 00:18:17]`. The two 1940s items of substance are **provenance claims**:
  a bismuth/magnesium sample said to have come anonymously from someone claiming to be an
  army officer who found it in a grandfather's archive with a diary entry saying **Roswell**
  `[@ 00:21:03]`, and Michels asserting **"Trinity, that crash was 1945"** as the source of a
  larger sample `[@ 00:25:10]`. **No Townsend Brown, no electrogravitics, no AEC, no early
  aerospace contractor.**
- **`qAou_h1POWs` (Prasad): ABSENT. A clean negative.** The only pre-1980 history in the file
  is 1911 superconductivity and 1860s black-body radiation, used as analogies. There is one
  sentence adjacent to the thread, that **aerospace companies hold materials and topological
  physics knowledge withheld from academia**, asserted with no name, date, company or
  document `[@ 00:04:23]`. **No Townsend Brown, no electrogravitics, no Manhattan Project, no
  AEC, no named contractor.**
- **`LGQkkHuwm6w` (Lear, 1987): the 1940s-1960s are everywhere as *lore* and absent as
  *institutions*.** Roswell 1947, MJ-12, Blue Book, the 1968 Air Force Academy text, the 1975
  SAC overflights, the Nevada Test Site. But **no Thomas Townsend Brown, no electrogravitics,
  no Manhattan Project lineage, no AEC by name** (he says "the test site"), **and not one
  early aerospace contractor named**. For a 1987 primary source on the recovery programme
  that is itself a result: the electrogravitics thread and the contractor thread were not
  part of this teller's account at that date.

### Why this matters to the board

I checked these names against `data/the-program.json`. **The board carries none of the
following: Townsend (0 hits), Biefeld (0), Winterhaven (0), Whitehall Rand (0), Babson (0),
Bahnson (0), Gravity Research Foundation (0), Research Institute for Advanced Study (0),
Witten (0), Glenn L. Martin (0), Mansfield Amendment (0), Amentum (0), Bluegill (0).**
"electrogravit*" appears **twice** in the entire 6.9MB file. Martin Marietta appears twice.
The board is strong on Malmstrom, Salas, Puthoff, Bigelow, Kelleher, Elizondo, Grusch,
Immaculate Constellation, Schriever, Borland, Barber, Kirk McConnell and Gallaudet, and it
carries Stringfield and Ubatuba. **The 1944-1980 institutional layer of this thread is a
genuine hole**, and `h7CJoGKvx3U` is a single named source who fills a large part of it with
checkable names.

---

## 5. INTERNAL CONTRADICTIONS AND FACTUAL ERRORS

### The one that matters most

**Brown's documentary basis says the opposite of his current position, on his own account.**
The briefing he saw stated that Immaculate Constellation was **established in response to the
2017 Elizondo disclosure** `[yGtVzBbUvx4 @ 00:36:42]`. Brown now says it is "a relatively old
program" run out of the NSC, and explains the discrepancy by saying the briefing's own
history was a **counterintelligence canary** planted so leaks could be traced `[@ 00:38:24]`.
The same explanation is applied to the expansion of **ARV** as "alien reproduction vehicle"
`[@ 00:32:44]`. This is internally coherent but epistemically load-bearing: **every element of
the document that contradicts his current thesis is classified by him as disinformation, and
every element that supports it is treated as reportage.** He is candid that he is doing this
("we're in the hall of mirrors"), and he does not claim the later information is documentary.
It rests on unnamed sources with "placement and access". Record it that way.

Related and unresolved in the same file: he says the ARV term is a plant, then advises
FOIA-ing the closely related **"advanced reconnaissance vehicle"** and says it will return
TRW material `[@ 00:33:51]`.

### Checkable errors, by file

**`yGtVzBbUvx4`**

| Claim | Problem |
|---|---|
| "that 1970 something outer space treaty" / "1971 SALT talks" where the US and USSR agree to notify each other about UFOs `[@ 01:08:59]` | **Wrong label, real instrument.** Checked: the **Agreement on Measures to Reduce the Risk of Outbreak of Nuclear War**, signed **Washington, 30 September 1971**; **Article 3** covers immediate notification on detection by missile warning systems of **unidentified objects**. It is not the Outer Space Treaty (1967) and it is not SALT. **This is a lead, not just a correction. See §6.** |
| "Rosemary Clooney, this remote viewer in 1979" finding a "TU22 Russian cargo plane" during Carter's presidency "from 1976 to 1980" `[@ 01:23:52]` | **Three errors in one sentence.** Rosemary Clooney is a singer; the remote viewer usually named in this story is a different Rosemary. The Tu-22 is a bomber, not a cargo aircraft. Carter's term ran 1977-1981. Michels is speaking, not Brown. |
| "before the U2 spy plane was created in 1954" `[@ 02:25:09]` | Loose. The programme dates from 1954; first flight was 1955. |
| Hitler's regime "arms and training and arms intelligence" to Zionist groups `[@ 02:32:12]` | Brown is gesturing at a real 1930s emigration arrangement, but the description overshoots it. **No instrument is named.** Do not carry this without one. |
| The Wall Street Journal / Northrop Grumman VP sibling allegation `[@ 01:41:44]` | An unverified allegation about **named private individuals** and their family relationships. It is Michels who makes it. **This must not reach the board without documentary support.** |
| `Otto Scorzani was president... of this world commerce corporation`, attributed to "Tom Dong... secret machines" `[@ 02:30:00]` | Two corrupted names and a hedged attribution stacked on each other. Michels, not Brown. |

**`h7CJoGKvx3U`**

| Claim | Problem |
|---|---|
| Lise Meitner "figures out the Chain Reaction by 38" `[@ 00:16:52]` | Meitner and Frisch interpreted **fission** at that date. The chain reaction is a separate step. **Weinstein himself contradicts this later**, saying "wasn't Lise Meitner who figured out the chain reaction" `[@ 02:36:08]`. Two incompatible versions in one episode. |
| "Glashow who discovers spontaneous symmetry breaking" `[@ 01:05:48]` | Glashow was Schwinger's student, but spontaneous symmetry breaking is not his result and is not what he was recognised for. |
| "1928 when Dirac came up with... quantum electrodynamics" `[@ 00:07:20]` | Conflates the 1928 relativistic electron equation with the founding of QED. Minor. |
| "Francis Crick physicist discovering the three-dimensional structure of DNA" `[@ 00:18:39]` | Elides Watson, Franklin and Wilkins. He gives a fuller and fairer version later `[@ 02:21:09]`. |
| **Louis Witten "101 years old"** `[@ 00:59:34]` and **C. N. Yang "101 years old"** `[@ 01:29:36]` | Two different men given the same age in the same episode, in February 2023. At most one can be right. **Both dates are trivially checkable and both matter, because Witten's age is load-bearing for whether he can still be interviewed.** |
| The Mansfield Amendment dated **1973** `[@ 01:06:56]` | The amendment is usually associated with an earlier authorisation act. **The date is the first thing to pin down**, because his whole 1973 stagnation thesis hangs on it. |
| "the eberg amendment 1973", "the ation Act of 1990" `[@ 01:10:54]` | [UNRESOLVED]. Not reconstructible. |
| The Bernie Madoff front-running theory `[@ 01:31:51]` | Included because **he corrects himself in real time**: "I got that wrong... shame on me." It is the only self-correction in the corpus and worth noting as a calibration signal. |
| "there is no one" who speaks physics on the subject, then immediately "I don't quite mean no one", then names Davis and Puthoff, then reports Davis calling him one of the three most technical people, then says "I'm not even on this" `[@ 01:21:39 - 01:22:46]` | A four-step retreat inside ninety seconds. His headline claim is much stronger than the version he ends up defending. |
| "90% no" on human-derived technology `[@ 02:00:13]`, alongside "we may be faking a UFO situation" `[@ 02:00:13]` and his Operation Fortitude hypothesis `[@ 01:13:49]` | Not a contradiction if read as branches of a decision tree, and he presents it that way. But **the "90%" figure is quoted around, and it does different work at different moments in the episode.** |

**`dzTZbSNsKV8`**

| Claim | Problem |
|---|---|
| Michels states as fact that the parts contain "isotope ratios that do not exist naturally on Earth" `[@ 00:19:24]` | **Nolan's own account undercuts it within two minutes.** Nolan says the other piece "the same event had exactly the correct isotope ratios" `[@ 00:20:30]`. The companion sample is not treated as evidence against the inference. This is the sharpest overstatement in the group. |
| Jacques Vallée "early versions of the internet called Arpanet" `[@ 00:09:32]` | Overstated. Vallée's association with Engelbart's group is real; "developed ARPANET" is not the same claim. |
| AATIP as "the main UFO program over the last 15 years", with "a $22 million budget" `[@ 00:04:28]` | Conflates a total figure for a bounded contract period with an annual budget over fifteen years, then compares it against an F-35 **programme** cost. Also renders the acronym as "ATIP". |
| "Trinity, that crash was 1945" `[@ 00:25:10]` | Stated by Michels as a date, not as a contested claim from a specific book. |
| The bismuth sample provenance: anonymous sender, self-described army officer, grandfather's archive, diary entry `[@ 00:21:03]` | Nolan flags it himself ("true or not"). **This chain is unverifiable in principle** and should be recorded as such rather than as weak evidence. |

**`qAou_h1POWs`**

| Claim | Problem |
|---|---|
| The Tic Tac "at least 31 times the speed of sound" `[@ 00:03:18]` | Presented as an established figure. It is not one. |
| "in 1911 when doctor ohm's discovered the first superconductor" `[@ 00:04:58]` | Caption corruption of the discoverer's name. The date and the fact are right. |
| `as paul drake said... everything we want to know about materials` `[@ 00:07:11]` | Caption corruption plus paraphrase of a well-known 1929 remark. The paraphrase is in the right spirit; the attribution as spoken is unusable. |
| Lockheed "observed these birds... can we replicate this" `[@ 00:14:55]` | **Checked and split.** The Dark Ice magnetometer is real and Lockheed's; it is a diamond-based quantum magnetometer. The bird-cryptochrome-to-Lockheed **origin story** is Prasad's narrative bridge and is not established by the sources that describe the device. |
| "aerospace companies as holders of basic scientific knowledge", withheld from academia, and "I know it's true" `[@ 00:04:23]` | The strongest structural claim in the file, offered with **no name, no company, no date and no document**. |

**`LGQkkHuwm6w`**

| Claim | Problem |
|---|---|
| Reagan's 4 December 1985 remarks made "just before he went over to Iceland" `[@ 00:12:18]` | **Sequence wrong.** The 1985 summit with Gorbachev was in Geneva; the Iceland summit was in 1986, after. |
| "chapter 13" of *Introductory Space Science, Vol II* `[@ 00:06:13]` | **Checked: the UFO chapter is Chapter XXXIII (33).** |
| Humans "invented the wheel, invented fire" between 4,000 and 8,000 BC `[@ 00:14:31]` | Plainly wrong on fire by hundreds of thousands of years. |
| "the f-16s that were sent out to chase him" in the 1975 SAC overflights `[@ 00:23:32]` | **Anachronism.** The F-16 was not in service in 1975. Whatever the 150-page report says, it does not say F-16. |
| Bruce Maccabee at "the Naval Surface weapons laboratory" `[@ 00:20:06]` | The organisation's actual name needs getting right before anything is cited to it. |
| "the Myers incident... the visitors from Pleiades" `[@ 00:19:02]` | Caption corruption of a well-known claimant's surname. Lear is **dismissing** these photographs as unsupported, which is worth recording. |
| "Bona Hopkins" and "Budd Hopkins" in the same passage `[@ 00:17:24, 00:17:58]` | Same person, two renderings. |
| The Vatican Observatory placed "in frascati near Rome" `[@ 00:22:22]` | Geographically doubtful. Check against the 1987 article itself. |
| **Internal:** 10-15 recovered craft, one flown, one "being flown as of 1981" `[@ 00:04:32, 00:24:05]`, alongside a scripted presidential statement that "we are unable to duplicate any of the metals" and "no closer to answers today" `[@ 00:09:30]` | Lear asserts operational flight and total failure to reverse-engineer in the same interview without reconciling them. |
| **Internal:** the press will not touch it `[@ 00:03:23]` versus "a lot of them have come forward" `[@ 00:03:23]` | Stated within seconds of each other. |
| **Internal:** "at least 90% of them are hostile", then "a completely different set of morals" `[@ 00:10:37]` | The definition is withdrawn as soon as it is given. |

### Across files

- **Prasad and Nolan advance incompatible research strategies and neither acknowledges it.**
  Prasad's entire thesis is that UAP materials can be derived by simulation from the
  *observables* without possessing anything `[qAou_h1POWs @ 00:01:07]`. Nolan's entire thesis
  is that **possession of physical samples** is the bottleneck and that the analysis
  instrument is the constraint `[dzTZbSNsKV8 @ 00:10:39]`. Same show, same host.
- **Weinstein and Brown give opposite answers to whether competent physics is being done.**
  Weinstein reports three years of failing to find anyone on the subject who speaks the
  language `[h7CJoGKvx3U @ 01:23:20]`. Brown asserts a large, well-resourced, technically
  sophisticated effort in the national labs and contractors `[yGtVzBbUvx4 @ 01:01:44]`.
  These are separated by roughly three years and by clearance, so both can be true; but
  **anyone using both files must state which one they are relying on.**

---

## 6. THE TOP 10 INDEPENDENTLY CHECKABLE LEADS

Ranked by the ratio of what it would settle to what it would cost.

**1. The Gravity Research Foundation to RIAS to Institute of Field Physics chain.**
Named: Roger Babson, Agnew Bahnson, Louis Witten, Bryce DeWitt, Cécile DeWitt-Morette,
Solomon Lefschetz, Rudolf Kalman, Sheldon Glashow, Hermann Bondi, Richard Arnowitt, Stanley
Deser, J. Robert Oppenheimer. `[h7CJoGKvx3U @ 00:59:34 - 01:06:21, 01:16:06 - 01:17:11,
01:41:09]`
*Verify by:* the GRF essay competition's own published winner list, which is a continuous
public record; the proceedings of the January 1957 Chapel Hill conference on the role of
gravitation in physics, which were issued as a technical report; RIAS's incorporation and
Baltimore address; Louis Witten's own published recollections of the period.
*Why first:* the board has zero of these names, the sources are institutional rather than
testimonial, and it is the only part of the corpus where a single check disposes of a whole
structural claim.

**2. The 1971 US-USSR notification agreement, Article 3.** `[yGtVzBbUvx4 @ 01:08:59]`
*Verify by:* the treaty text. Signed Washington, 30 September 1971; registered in the UN
Treaty Series; also carried at the Yale Avalon collection and by the State Department.
*What it settles:* it converts "there are agreements about unidentified objects" from lore
into a matter of published treaty law, **and it corrects the transcript's own mislabelling**
of the instrument as the Outer Space Treaty or SALT. Cheap, decisive, and directly relevant
to Brown's agreements argument.

**3. Amentum's EG&G lineage and its Patuxent River footprint.** `[yGtVzBbUvx4 @ 01:57:22,
01:58:33]`
*Verify by:* Amentum's own SEC filings, which set out the corporate lineage; the federal
contract record for Patuxent River. **Partially checked already:** the AECOM Management
Services to Amentum rebrand and the URS acquisition of EG&G Technical Services are on the
public record, so Brown's "they own parts of EG&G" is directionally right as corporate
lineage even though the phrasing is loose. What is **not** checked is anything about the
hangars.
*Why high:* the board has EG&G and Pax River and **not Amentum**. This is a named, currently
active contractor with a traceable paper trail.

**4. Immaculate Constellation: the NSC custody claim specifically.** `[yGtVzBbUvx4 @ 00:20:02,
01:34:35]`
*Verify by:* Brown's State Department cleared report as released, against the hearing record
in which it was entered. The report is the only documentary artefact; **the NSC ownership
claim is not in it**, by Brown's own statement, and rests on later unnamed sources. The
verifiable question is narrow and worth asking: does the cleared text say DoD?
*Why high:* the board already carries MCON heavily. The NSC claim is the new element and it
inverts the custody model.

**5. USAF Academy, *Introductory Space Science, Volume II*, Chapter XXXIII, "Unidentified
Flying Objects" (1968).** `[LGQkkHuwm6w @ 00:06:13]`
*Verify by:* the scanned document, which circulates widely. Lear reads two passages aloud on
a 1987 broadcast; both are checkable word for word.
*What it settles:* a genuine federal primary record, a fixed date, and a correction to the
chapter number a 1987 source gave on air.

**6. The Halt memorandum and the Halt tape, Bentwaters/Rendlesham, December 1980.**
`[LGQkkHuwm6w @ 00:02:51]`
*Verify by:* the released memorandum, which Lear says came out under FOIA, and the audio
recording he says runs about eight hours. Both are the sort of thing the board's FOIA layer
can name a request against.
*The unsupported part:* Lear's claim that a security policeman within ten feet saw three
occupants approach the Wing Commander. That has **one teller and no document**, and it is the
part that should be flagged if the node is built.

**7. Bruce Maccabee's 26-page report on the JAL incident of 17 November 1986.**
`[LGQkkHuwm6w @ 00:20:06]`
*Verify by:* the FAA records released on the case, including the ATC transcript and radar
data. Lear specifies contents (ATC transcript, FAA plots, Air Force plots, the captain's
drawing) that can be checked item by item against the report.
*Note:* get the employing organisation's name right before citing it.

**8. Project Preserve Destiny and the FOIA referral behaviour.** `[yGtVzBbUvx4 @ 01:17:13]`
*Verify by:* filing the request with the Air Force and **keeping the referral letter**. The
claim Michels makes is not that documents are released but that the Air Force **forwards the
request to NSA**, which he treats as evidence the programme name is real. That is a testable
administrative behaviour, and the referral letter is itself the artefact. Also checkable: Dan
Sherman's stated postings at San Vito dei Normanni and Offutt against his service record.
*Why included:* the board has **zero** on Sherman or Preserve Destiny, and this is a request
the FOIA layer can carry.

**9. The Ubatuba NanoSIMS work and the bismuth/magnesium waveguide claim.**
`[dzTZbSNsKV8 @ 00:10:39, 00:20:30, 00:22:12]`
*Verify by:* any published or preprint write-up of the Stanford secondary-ion measurements.
Two specific, testable numbers are on the record: the magnesium isotope ratios, and Puthoff's
claim that the layered bismuth reduces the required terahertz waveguide to about **one
thirtieth** of the wavelength.
*Verify also, and this is the point:* the **companion sample with terrestrial ratios**
`[@ 00:20:30]`. Any node built from this must carry that fact, because the episode does not.
*Do not attempt to verify:* the bismuth provenance chain. It is anonymous by construction.

**10. The Mansfield Amendment date, and the funding-instrument chain around it.**
`[h7CJoGKvx3U @ 01:06:56, 01:09:49, 01:10:54]`
*Verify by:* the statute. Weinstein dates it 1973; it is usually associated with an earlier
military authorisation act, and **the date is the whole load-bearing point** of his 1973
stagnation thesis. Bayh-Dole is a named public law and trivially checkable. The Pergamon and
peer-review claim is checkable against publishing history. The two garbled instruments
`[@ 01:10:54]` are not recoverable and should be dropped rather than guessed.

**Just below the line**, and worth naming so they are not lost: the NIDS triangle study
correlating sightings to US naval bases `[yGtVzBbUvx4 @ 00:28:19]`; the Podesta / fast walkers
email and the FOIA that returned nothing `[@ 02:11:09]`; Bluegill Triple Prime and the Navy
deck logs `[@ 01:58:33]`; and Reagan's 42nd UNGA address of 21 September 1987, which is a
fully citable public text and which Lear reads with its own self-deflating final line intact
`[LGQkkHuwm6w @ 00:13:26]`.

---

## 7. CORRUPTION WATCHLIST

Every name I flagged, with the raw caption form. **Confidence is about the spelling, not the
claim.** Six rows are marked SPELLING CHECKED, meaning the name was resolved against the open
web on 30 August 2026; nothing attached to those names was checked.

### Resolved during this pass

| Reported as | Raw caption | File | Status |
|---|---|---|---|
| **Jeffrey Nuccetelli** | `Jeff Nusatelli`, `Jeffrey Nusatelli` | `yGtVzBbUvx4` | **SPELLING CHECKED.** This is the Holocron/HoloChron case again: neither caption spelling would have found him. |
| **Amentum** | `Amentum Core`, `Amentum Corporation` | `yGtVzBbUvx4` | **SPELLING CHECKED.** Real contractor; EG&G lineage runs through URS and AECOM. |
| **Quantum Generative Materials / GenMat** | as spoken | `qAou_h1POWs` | **SPELLING CHECKED.** Prasad's $15M figure matches the public announcement. |
| **Lockheed "Dark Ice" magnetometer** | `dark ice magnetometer` | `qAou_h1POWs` | **SPELLING CHECKED.** Device is real; the bird-biomimicry origin story is not established. |
| **USAF Academy chapter number** | `chapter 13` | `LGQkkHuwm6w` | **CHECKED: Chapter XXXIII (33).** |
| **1971 agreement** | `1970 something outer space treaty`, `1971 salt talks` | `yGtVzBbUvx4` | **CHECKED: Agreement on Measures to Reduce the Risk of Outbreak of Nuclear War, 30 Sept 1971, Art. 3.** |

### Phonetically corrupted, reconstruction offered

| Reported as | Raw caption | File | Confidence |
|---|---|---|---|
| **Thomas Townsend Brown** | `Thomas Towns and Brown`; and `electrogravidics` for electrogravitics | `yGtVzBbUvx4` | high, **but recorded here deliberately**: the caption splits the surname into three words. A grep of this transcript for "Townsend" returns nothing. This is the exact shape of the failure the corpus keeps producing. |
| Hal Puthoff | `Hal Kutoff`, `Dr. Halpoff`, `how put off`, `hal put off` | `dzTZbSNsKV8`, `h7CJoGKvx3U`, `qAou_h1POWs` | high (four renderings, one person) |
| Louis Witten / Edward Witten | `Lewis Whitten`, `Edward Whitten`, `Ed Wht` | `h7CJoGKvx3U` | high |
| Agnew Bahnson | `agnu banson`, `banson` | `h7CJoGKvx3U` | **medium.** The reconstruction fits the GRF context; the given name is a guess from one caption. **Search string, not a fact.** |
| Bryce DeWitt / Cécile DeWitt-Morette | `Bryce dwit`, `Cecil dit Moret`, `the DTs` | `h7CJoGKvx3U` | high |
| Solomon Lefschetz | `Solomon lefet`, `Solomon Lett` | `h7CJoGKvx3U` | medium-high (the "great topologist" gloss constrains it) |
| Rudolf Kalman | `rud Rudolph Colman of Colman filtering` | `h7CJoGKvx3U` | high (the filtering gloss is decisive) |
| Arnowitt and Deser | `arit and deser` | `h7CJoGKvx3U` | **medium.** Reconstructed from the GR context. |
| Curtiss-Wright | `Curtis Wright Aerospace` | `h7CJoGKvx3U` | medium-high |
| Schriever | `Shrivever Air Force Base` | `yGtVzBbUvx4` | high (board already carries it) |
| Michael Shellenberger | `Michael Shelonburgger` | `yGtVzBbUvx4` | high (board already carries it) |
| Robert Salas | `Robert Salis`, `Bob Salace` | `yGtVzBbUvx4` | high (board already carries it) |
| Mark McCandlish | `Mark Mlan Mckish`, `Mandlish`, `Macandlish` | `yGtVzBbUvx4` | high (three renderings in one exchange, self-corrected on air) |
| Michael Herrera | `Michael Herreras` | `yGtVzBbUvx4` | high |
| Tim Gallaudet | `Tim Galedet` | `yGtVzBbUvx4` | high (board already carries it) |
| Trevor Paglen | `Trevor Pagglin` | `yGtVzBbUvx4` | high |
| Andrija Puharich | `Andre Puharic`, `Buharic` | `yGtVzBbUvx4` | medium-high |
| Ossining, New York | `Austining New York` | `yGtVzBbUvx4` | medium |
| Robert Boyle | `Sir Robert Bole` | `yGtVzBbUvx4` | medium |
| John Dee / Enochian / Sigillum Dei Aemeth | `John D`, `Anakian`, `In Nokian`, `sigil sigilum de ament` | `yGtVzBbUvx4` | medium-high (Brown says on air his own pronunciation is probably wrong) |
| Abramelin | `Abramlin`, `Abramalin`, `Abramelon` | `yGtVzBbUvx4` | medium-high |
| Otto Skorzeny | `Otto Scorzani` | `yGtVzBbUvx4` | medium |
| Reinhard Gehlen | `Reinhard Gellen`, `Reinhardt Gill` | `yGtVzBbUvx4` | medium |
| Tom DeLonge, *Sekret Machines* | `Tom Dong writes about in secret machines` | `yGtVzBbUvx4` | medium |
| Erik Bard | `Eric Bard` | `h7CJoGKvx3U` | medium |
| Jacques Vallée | `Jacques Valet`, `Jacqu Valet` | `dzTZbSNsKV8` | high |
| Diana Pasulka | `Diana Pulka` | `dzTZbSNsKV8` | high |
| Robert Bigelow | `Robert Bigalow` | `dzTZbSNsKV8` | high |
| Colm Kelleher | `Col Kellaher` | `dzTZbSNsKV8` | high |
| caudate nucleus / putamen | `codate nucleus`, `patamon`, `potato`, `epitamin`, `codate impetamin` | `dzTZbSNsKV8`, `yGtVzBbUvx4` | high (five renderings of two structures) |
| CyTOF | `SaitTo` | `dzTZbSNsKV8` | **medium.** Reconstructed from "the best tool" + Nolan's known instrument. **Do not print this without checking.** |
| NanoSIMS | `nano sims` | `dzTZbSNsKV8` | high |
| Ubatuba | `Uba Tuba`, `Uba tuba` | `dzTZbSNsKV8` | high (board already carries it) |
| Heike Kamerlingh Onnes | `doctor ohm's` | `qAou_h1POWs` | **medium.** The 1911 date and "first superconductor" constrain it, the caption does not. |
| Paul Dirac | `paul drake` | `qAou_h1POWs` | medium |
| many-body Schrödinger equation | `antibody schrodinger equation`, `many bodies shown in your equation` | `qAou_h1POWs` | high |
| cryptochrome CRY4 | `cry4` | `qAou_h1POWs` | high |
| Billy Meier | `the Myers incident` | `LGQkkHuwm6w` | medium-high (the Pleiades gloss constrains it) |
| Budd Hopkins | `Bona Hopkins`, `Budd Hopkins` | `LGQkkHuwm6w` | high |
| Naval Surface Weapons organisation | `Naval Surface weapons laboratory` | `LGQkkHuwm6w` | **medium.** The exact organisational name must be established before it is cited. |
| San Vito dei Normanni / Offutt | `San Vito denormy`, `off it` | `yGtVzBbUvx4` | medium |
| Greg Malazi (documentarian, *Mind Traveler*) | `Greg Malazi` | `yGtVzBbUvx4` | **low.** Single rendering, no cross-check. |
| K. Randall Mayhew | `K. Randall May` | `yGtVzBbUvx4` | **low.** |
| NIDS | `that famous NID study` | `yGtVzBbUvx4` | medium |

### UNRESOLVED: must not reach the board under these spellings

| Raw caption | File | Cite | Note |
|---|---|---|---|
| `the eberg amendment 1973` | `h7CJoGKvx3U` | `@ 01:10:54` | An instrument named alongside Mansfield and Bayh-Dole. Not reconstructible. |
| `the ation Act of 1990` | `h7CJoGKvx3U` | `@ 01:10:54` | Same sentence. The caption has eaten the first syllables. |
| `case Explorer`, `RS safe`, `safety net` | `h7CJoGKvx3U` | `@ 02:53:27, 02:55:03` | Three law-enforcement deconfliction systems. One is partly legible on screen in the episode as an "officer safety event deconfliction system"; the other two are not. |
| `MMTU` | `yGtVzBbUvx4` | `@ 02:00:11` | Brown is asked directly and **refuses to gloss it**: "the hint would give it away." Record the refusal, not a guess. |
| `Marsupial` (as an NGA programme) | `yGtVzBbUvx4` | `@ 00:59:59` | The word is clear; the programme is not established. Brown answers "no comment", which is not confirmation. |
| `nonstructured light energy craft`, `go at cardinals` | `yGtVzBbUvx4` | `@ 01:56:47` | Michels reads these from Brown's tweet. Brown says only that it is "a very specific term" and declines to source it. |
| `the Maynard Corporation` | `yGtVzBbUvx4` | `@ 02:30:00` | Michels says it is a pseudonym used in a book. A pseudonym cannot be a node. |
| `Jason Samosa` | `yGtVzBbUvx4` | `@ 02:30:32` | Researcher credited with an analysis Michels relays. Single rendering. |
| `Rosemary Clooney` as a remote viewer | `yGtVzBbUvx4` | `@ 01:23:52` | Almost certainly the wrong surname for the person in the story. See §5. |
| `frascati near Rome` as the Vatican Observatory's location | `LGQkkHuwm6w` | `@ 00:22:22` | Check against the 1987 article rather than reconstructing. |

---

## What is thin

Stated plainly, because the sections above are long and could read as more than they are.

- **`qAou_h1POWs` (Prasad) contributes almost nothing structural.** It is a good explainer on
  quantum simulation and it contains exactly one programme-relevant assertion, unsupported.
  Its main value to this board is as a **negative** on the 1940s-1980s thread and as a
  named company that is currently absent from it.
- **`dzTZbSNsKV8` (Nolan) is thinner than its reputation.** The institutional content is one
  sentence about the CIA visiting his office and a list of the people he was introduced to.
  Everything else is materials and neuroanatomy, and the materials story is weaker inside the
  episode than the episode's own framing claims.
- **`sF03FN37i5w` is off topic and should not be worked further.**
- **`LGQkkHuwm6w` is a 1987 primary source and should be treated as one**, which cuts both
  ways: it is a genuine dated artefact of what was being said then, and it is riddled with
  errors that a modern reader would not make. Its chief value is the documents Lear physically
  holds up, not the claims he makes about them.
- **`yGtVzBbUvx4` is the densest file and the hardest to use.** Brown is careful about the
  boundary between what he saw and what he was told, and he flags his own speculation
  repeatedly, which is a genuine mark in his favour. But **almost every load-bearing element
  of his current model sits on the told side of that boundary**, and the one document he
  actually saw is deleted, was seen once, years ago, and says something he now says is false.
  The interview also contains extended allegations about human trafficking of "psionic
  assets" `[@ 02:44:31 - 02:53:31]` that **Brown himself declines to support** ("I've only
  heard those allegations, so I can't support them"; "I have no evidence for that"). Anyone
  drawing on this file must carry those disclaimers with the claims.
- **`h7CJoGKvx3U` is the most valuable file in the group for this board**, and its value is
  almost entirely in the ninety minutes between `00:59:00` and `01:18:00` plus the passage at
  `01:41:00`. Roughly the last forty minutes of the episode are not about this subject at all.
