# Video-transcript corpus — group D (tail), triage and structural extraction

**Source:** `research/.transcripts/`, nine cached transcripts assigned as "group D".
**Extracted:** 30 August 2026.

**Status of everything below: UNVERIFIED LEAD MATERIAL.** Nothing here is asserted as
true. Every line records what a *named speaker claims*, with a file + timestamp pointer so
the claim can be re-read at source. Nothing here is graded and nothing here is board
content.

**`CLAUDE.md` §2 applies to every proper noun on this page.** Most of these are
auto-generated captions, which corrupt proper nouns silently and plausibly. The corruption
is *not uniform across the nine files* and that matters:

| file | caption quality | evidence |
|---|---|---|
| `kwsWAQ9sJZE` | **best** — punctuated, speaker-aware, near certainly human-checked | renders `Dr. Garry Nolan` correctly; still gets `David Grush` wrong |
| `23b44fxvz8I` | moderate auto | `Oak Shannon`, `Ferris Williams`, `Halputoff`, `Macdonald Douglas` |
| `SZBI85yvV5A` | moderate auto | `Towns and Brown`, `Beatatric Valale`, `Jacqu Valet` |
| `vUnKRknLVSA` | **worst** — live broadcast caption stream | one man's surname renders as GRESH, GRESTE, GRACE, GRAPES, BRUSH, CRUSH |

Names are marked:

- **[CONF]** — spelled consistently and matches a well-attested public figure or body.
- **[PHON?]** — phonetically corrupted; best reconstruction given, raw caption in
  `backticks`. **Treat as a search string, not a fact.**
- **[UNRESOLVED]** — could not be reconstructed with confidence. Recorded raw. **Must not
  reach the board under the spelling in the transcript.**

The transcripts carry **no metadata** — the cache holds only an id and timed segments. Every
show and participant identification below is from **internal evidence only** and is labelled
with its confidence.

Timestamps are the START of the caption block containing the statement. Citation form is
`file @ HH:MM:SS`, abbreviated by the file key below. **Every one of the 128 timestamps below
was machine-checked against the cache** and lands on a real position: 60 on a canonical block
start, 68 on a segment start, none orphaned.

**A property of `tools/read_transcript.py` worth knowing before you scrub to one of these.**
It flushes a block "roughly every 30 seconds" measured from wherever the *window* begins, so
`--from 20` and `--from 22` fold the same speech into different blocks with different start
times. A citation here is therefore good to about **plus or minus 30 seconds**, not to the
second. Scrub to the timestamp and read forward; do not conclude the line is missing because
it is not the first sentence you see.

**File key**

| # | id | what it is |
|---|---|---|
| **D1** | `kwsWAQ9sJZE` | Yes Theory, "Close Encounters of the Humankind" |
| **D2** | `23b44fxvz8I` | interview with Oke Shannon [PHON?] |
| **D3** | `SZBI85yvV5A` | American Alchemy, golf episode |
| **D4** | `vUnKRknLVSA` | NewsNation special report on the House Oversight UAP hearing |
| **D5** | `R9Yn0hgbVA0` | esoteric lecture — OFF-TOPIC, two salvaged items |
| — | `PEe72Nj-AW0` | Graham Hancock — OFF-TOPIC |
| — | `4U3JaHp2B5Y` | American Alchemy, venture capital — OFF-TOPIC |
| — | `OB8CsDl9_XU` | American Alchemy, Jake Paul — OFF-TOPIC |
| — | `tybOi4hjZFQ` | guided breathing session — OFF-TOPIC |

---

## 0. TRIAGE — all nine files

**Four of nine are on-topic. One is off-topic with a narrow salvage. Four are off-topic
outright.** The corpus was pulled from a mixed podcast feed; three of the four outright
off-topic files are episodes of the same show as D3 (American Alchemy, host **Jesse
Michels** [CONF] — the captions render him `Jesse Michaels`), which explains the mix.

| # | id | show and participants, from internal evidence | conf. | ruling |
|---|---|---|---|---|
| D1 | `kwsWAQ9sJZE` | **Yes Theory**, "A Human Experience", directed by **Ammar Kandil** [CONF], "in collaboration with **Jesse Michels**" — end credit @ 01:07:39. Subjects: **David Grusch** [PHON? `Grush`] around the House Oversight hearing, and **Dr. Garry Nolan** [CONF] at Stanford | high | **ON-TOPIC** |
| D2 | `23b44fxvz8I` | Interviewer **unnamed**, show **unnamed**; British-inflected, works with a second person the guest calls a "tag team", met the guest and wife **Linda** for a three-hour lunch in Florida. Guest: **Oke Shannon** [PHON? `Oak Shannon`], ex-USN, ex-Los Alamos | high on guest, **[UNRESOLVED]** on host | **ON-TOPIC — the strongest file in the group** |
| D3 | `SZBI85yvV5A` | **American Alchemy**, host Jesse Michels, with **Jamie Vernon** [CONF] (Joe Rogan Experience producer, "Young Jamie") and golfer **Viktor Hovland** [PHON? `Victor Havlin`], at Barton Pitch and Putt, Austin. Opens with a promo montage from Michels's own JRE appearance | high | **ON-TOPIC** |
| D4 | `vUnKRknLVSA` | **NewsNation** special report, anchor **Brian Entin** [CONF]. Panel: **Ross Coulthart** [PHON? `Ross Cold Heart`], **Nick Pope** [CONF], **Ben Hansen** [CONF], Rep. **Tim Burchett** [CONF], **Ryan Graves** [CONF]. Hearing footage of Grusch, Graves and **David Fravor** [PHON? `Faber`/`Favor`] | high | **ON-TOPIC — but largely already on the board; see §5** |
| D5 | `R9Yn0hgbVA0` | Lecture on **Alice Bailey**'s *A Treatise on Cosmic Fire* and the "garment of God"; theosophy, light and electromagnetism, consciousness, near-death experience. Speaker unnamed (introduced off-camera by "Lawrence"), self-describes as a **former Lockheed Martin VP** who retired c. 2011 | speaker **[UNRESOLVED]** | **OFF-TOPIC** — c. 95% esoteric philosophy, zero UAP-programme content. **Two items salvaged, §0a** |
| — | `PEe72Nj-AW0` | **Graham Hancock** [CONF] delivering a written rebuttal to archaeologist **Flint Dibble** [CONF] after their Joe Rogan debate. Shipwreck counts, Göbekli Tepe, the Sphinx, accusations of race science | high | **OFF-TOPIC.** Archaeology and a personal dispute. Two irrelevant hits on "secret" and "Nazi archaeologists" |
| — | `4U3JaHp2B5Y` | American Alchemy: Jesse Michels interviews **Justin Mateen** [PHON? `Justin Matine`/`Batine`], Tinder co-founder, on venture investing | high | **OFF-TOPIC.** A VC interview. One passing B-roll line about Lockheed Martin selecting a small-launch provider; nothing programme-related |
| — | `OB8CsDl9_XU` | American Alchemy: Jesse Michels interviews **Jake Paul** [CONF] in Dorado, Puerto Rico; **Eric Weinstein** [CONF] on the phone | high | **OFF-TOPIC.** Boxing, brand-building and fighter pay |
| — | `tybOi4hjZFQ` | A guided breathing session — three rounds of circular breathing with breath holds, closing "All the love. All the power." and a free-app plug | high on content, inference on identity | **OFF-TOPIC.** A breathing exercise. The sign-off phrasing is characteristic of the Wim Hof Method, but the speaker is never named and that identification is inference, not evidence |

### 0a. The two items salvaged from D5, and why the file is still off-topic

D5 contains no UFO, UAP, crash, retrieval or reverse-engineering content of any kind — a
keyword sweep of the full file returns zero hits. It is a lecture on esoteric philosophy.
Two passages are nonetheless worth a line, and both are about the *speaker*, not the
subject:

1. **[D5 @ 00:54:36 – 00:56:54]** The speaker says a friend "still at Lockheed Martin" sent
   him a spiral-bound compilation titled *ESP Wars* through the speaker's daughter, who he
   says also works at Lockheed Martin. He states the material "was put together when **I was
   the VP there**", dates that to roughly two years before his retirement, and says
   **Russell Targ** [CONF] "had a lot of input" — followed immediately by a broken clause,
   `doctor thought of did I get to say this`, which is very likely **Puthoff** [PHON?] and
   which the file's later, clearer mentions support. He describes the compilation as senior
   Soviet and US general officers publishing psi research because neither side found a
   military advantage in it.
2. **[D5 @ 00:39:02]** He describes **Hal Puthoff** [PHON? `dr hal put off`] as "a physicist
   in Austin" and credits him with a published **polarizable-vacuum** model in which the
   vacuum is an electrically polarised medium and gravity is electromagnetic, dating the
   publication to 2018. He names **Wal Thornhill** [PHON? `wall thornhill`] as the author of
   a rival proposal.

**Neither item makes the file on-topic.** They are a claimed biography and a physics
name-check inside an hour of theosophy. The claimed Lockheed VP role is unattached to any
programme claim, and the speaker is never named in the transcript. Recorded so a later
session does not have to re-read the file to find out; **not** recommended as a research
target on this evidence alone.

---

## 1. ENTITIES

### 1a. Government bodies, offices and oversight

| Name | Role the speaker assigns it | cite |
|---|---|---|
| **Defense Intelligence Agency** [CONF] | Shannon says its then-Director, Adm. Thomas R. Wilson, telephoned him to ask whether Eric Davis could be trusted | D2 @ 00:26:48 |
| **Los Alamos National Laboratory** [CONF] | Shannon's employer. He held **deputy group leader for special projects**, then **program manager for special projects** | D2 @ 00:15:43 |
| **Sandia National Laboratories** [CONF] | Named with Los Alamos as the two labs whose nuclear-yield figures Pharis Williams is said to have overturned before Navy brass in Albuquerque | D2 @ 00:11:39 |
| **Naval Postgraduate School, Monterey** [CONF] | Where Shannon took an MS in physics and met Williams; he says he watched Williams derive the Dynamic Theory there over three years | D2 @ 00:04:10, 00:12:48 |
| **Department of Energy** [CONF] | Michels's claim: the DOE, not DARPA, is where "the most secret science" sits, on the strength of its nuclear-security regime; he adds it funded the human genome work and so holds genomic data other departments do not | D3 @ 00:41:30, 00:42:04 |
| **National Geospatial-Intelligence Agency** [CONF] | Grusch: colleagues "shut the door in my office at the NGA" c. 14 years earlier and showed him intelligence reports | D1 @ 00:30:05 |
| **DOPSR — DoD Pre-Publication and Security Review** [CONF] | Grusch's account of why he could say "biologics" publicly: everything he says must clear DOPSR, and a refusal would force the objecting agency to self-identify, which he would then publish | D1 @ 00:45:37 |
| **AARO** [CONF] | Its then-director's post-hearing statement is read on air as pushback; Pope calls it "the Empire strikes back" | D4 @ 01:03:18, 01:20:14 |
| **House Oversight subcommittee** [CONF] | The hearing itself. Members appearing on tape: **Burchett**, **Luna**, **Mace**, **Gaetz**, **Ocasio-Cortez**, **Garcia**, **Moskowitz** [all CONF] | D1 @ 00:15:19; D4 throughout |
| **FAA** [CONF] | Burchett: he wrote a bill requiring pilot UAP reports to the FAA be forwarded to Congress, and says he was told by leadership it "was blocked by the intelligence community" | D4 @ 00:38:45 |
| **Nuclear Regulatory Commission / nuclear-plant incident** | Referred to obliquely by Burchett as a US parallel to the Russian missile-base claim; he cannot recall the site name on air | D4 @ 00:46:36 |

### 1b. Contractors, laboratories and private institutions

| Name | Role the speaker assigns it | cite |
|---|---|---|
| **Battelle Memorial Institute** [CONF] | Jamie Vernon: Battelle "manages all the nuclear sites across the US" and is close to Wright-Patterson. Offered as his own Ohio-local observation | D3 @ 00:08:58 |
| **Wright-Patterson AFB** [CONF] | Named in the same breath as Battelle; "a lot of stuff has happened there supposedly" | D3 @ 00:08:58 |
| **Lockheed Martin / Skunk Works** [CONF] | Michels says he knows a man who worked at Skunk Works c. 30 years who believes UFO sightings are real but that recovered craft are **human technology** built "at Locked and other places" — a named dissent from the retrieval thesis, worth recording as such | D3 @ 00:43:44 – 00:44:52 |
| **Northrop** [CONF] | Named with Lockheed as the two firms Michels reads into the two crates at the end of *Close Encounters of the Third Kind* | D3 @ 00:37:44 |
| **McDonnell Douglas** [PHON? `Macdonald Douglas`] | The employer attached to "Bob Wood" on the meeting list Shannon is shown | D2 @ 00:50:56 |
| **Brookhaven National Laboratory** [CONF] | Michels: the largest US particle accelerator, "called Cosmatron" [PHON? — Brookhaven's **Cosmotron**], offered as an example of secret science at DOE sites. **The claim as stated is wrong on the facts** and should be recorded as a claim, not carried | D3 @ 00:42:38 |
| **Anduril** [CONF] | Noted as having moved to Ohio, alongside an Intel plant and data centres; a passing geography remark, no programme claim | D3 @ 00:08:27 |
| **Boeing** [CONF] | Ocasio-Cortez presses Graves on his naming Boeing contractors in the Virginia Beach cube incident; Grusch answers only in general terms | D4 @ 00:30:43 |
| **Nolan Laboratory, Stanford School of Medicine** [CONF] | Filmed on site. Nolan shows an instrument that "reads metals... it's in a vacuum", developed by a postdoc | D1 @ 00:51:47 |
| **Skywatcher** [CONF] | Michels says he interviewed them; they claim a frequency "dog whistle" that attracts UAP, plus sensors and human "neuritators" [PHON?], and are trying to summon "the egg" | D3 @ 00:09:32 – 00:11:13 |

### 1c. Programmes, operations and named events

| Name | What is claimed | cite |
|---|---|---|
| **The multi-decade crash-retrieval and reverse-engineering programme** | Grusch's sworn formulation, delivered under oath on tape in both D1 and D4 | D1 @ 00:15:19; D4 @ 00:01:44 |
| **Manhattan Project secrecy, overlaid** | Grusch's account of the mechanism: they "took the Manhattan Project secrecy and overlaid it", motivated by military potential and by fear of religious "ontological shock", and no disclosure plan was ever written | D1 @ 00:22:06 |
| **"Magenta, Italy, 1933"** | Michels: the first European recovery; Mussolini's regime documented it, moved it to a secure air base until 1944–45, **Pope Pius XII** back-channelled it and "we ended up scooping it". He says **Richard Bissell** independently mentioned "the 1933 magenta" to Harald Malmgren, and treats that as corroboration of Grusch | D3 @ 00:05:43 – 00:06:17, 00:23:22 – 00:24:34 |
| **Swedish ghost rockets, 1946** | Michels: over a thousand objects resembling modified V-2s but manoeuvring and far faster; Eisenhower sent **Gen. James Doolittle** [PHON? `James Dittle`] to investigate | D3 @ 00:06:50 |
| **Bluegill Triple Prime** [CONF as a test name] | Michels: "probably involving some sort of anomalous object", researched in depth by a person the caption renders `Jeffrey Kruchank` **[UNRESOLVED]** | D3 @ 00:24:01 |
| **The Eglin incident** | Gaetz on tape: a protected disclosure from an Air Force base, initial refusal of access to images, radar and flight crew, then partial access; four craft in diamond formation over the Gulf of Mexico, a large object, radar and FLIR both failing, a manually taken image | D4 @ 00:21:51 – 00:24:03 |
| **The Berkshires, September 1969** | D1's origin story: over 300 people across neighbouring Massachusetts towns; the film's central witness is **Melanie** [first name only] | D1 @ 00:04:37, 01:04:16 |
| **Council Bluffs** [CONF] | Nolan: a molten-metal fall witnessed by many including police; the subject of what he calls the first peer-reviewed paper of its kind | D1 @ 00:57:35 |
| **Stargate-lineage remote viewing** | Michels mentions interviewing **Joseph McMoneagle** [PHON? `McGonagle`, then self-corrected to `McMonagle` on tape], who showed him Mars imagery; Michels says he **debunked some of the images himself** | D3 @ 00:32:16 |

### 1d. People, and the role each is given

| Name | Role | cite |
|---|---|---|
| **Oke Shannon** [PHON? `Oak Shannon`] | The D2 guest. See §3 | D2 throughout |
| **Pharis Williams** [PHON? `Ferris Williams`, called "Willie"] | Shannon's Naval Postgraduate School colleague, later a Los Alamos collaborator; author of the five-dimensional "Dynamic Theory". Said to be deceased | D2 @ 00:08:11 – 00:14:31 |
| **Adm. Thomas R. Wilson** [CONF] | Called Shannon to vet Eric Davis | D2 @ 00:26:48 |
| **Dr. Eric W. Davis** [CONF] | Shannon: "I did work with him... I know him fairly well", and vouched for him to Wilson | D2 @ 00:23:19, 00:27:25 |
| **Harald Malmgren** [PHON? `Harold Maldgren`] | Michels: an interview subject with "unimpeachable" credentials as a top aide across four presidencies; Michels says Malmgren's Wikipedia entry was rewritten to "American writer and lobbyist" shortly afterwards. Malmgren is said to have survived throat cancer, leaving his voice hard to hear, so the key line was recovered by transcription after the fact | D3 @ 00:22:18 – 00:25:40 |
| **Richard Bissell** [CONF] | Michels: "the designer of Area 51", said to have briefed Malmgren on "other world technologies" and to have mentioned the 1933 Magenta case | D3 @ 00:23:22, 00:25:40 |
| **Thomas Townsend Brown** [PHON? `Towns and Brown`, `Townson Brown`] | See §4 | D3 @ 00:02:17, 00:28:23, 00:36:36, 00:37:10 |
| **Dr. Garry Nolan** [CONF — note the board's spelling is *Garry*, two Rs] | Stanford immunologist; analysing claimed recovered materials. See §3 | D1 @ 00:51:12 – 01:01:16 |
| **Jacques Vallée** [PHON? `Jacqu Valet` in D3; spoken as "Jacques" in D1] | Nolan: the chain-of-custody source for "mostly all" the samples in his lab. Separately, Michels claims Vallée worked with **Doug Engelbart** [CONF] on early internet work in the 1970s | D1 @ 00:56:27; D3 @ 00:43:44 |
| **Jake Barber** [CONF] | Michels: first met him at Disneyland; describes his interview as combining psychic recruitment and craft retrieval, and reports Barber saying a retrieved "egg" may be of little interest because they have too many | D3 @ 00:38:16, 00:39:52 |
| **George Knapp** [CONF] | Named as the source of the Sokolov letter entered into the congressional record, and as a personal friend by Burchett | D4 @ 00:43:15 – 00:45:00 |
| **Col. Boris Sokolov** [CONF] | The Russian officer whose claims the letter conveys | D4 @ 00:43:49 |
| **Harry Reid** [CONF] | Named as a prior source to Knapp for the Russian missile-base material | D4 @ 00:45:31 |
| **Dr. John Mack** [CONF] | Named by Kandil as the intellectual model for D1's method — approaching witnesses "from a lens of empathy" | D1 @ 01:01:51 |
| **Rep. Mike Gallagher** [CONF] | The interviewer's framing: Nolan briefed Gallagher on the Wilson–Davis transcript, and Gallagher brought it to a hearing | D2 @ 00:22:46 |
| **Grant Cameron** [CONF] | The interviewer's framing: an early recipient of the Wilson material, and the person who published the attendee list shown to Shannon | D2 @ 00:50:22 |

---

## 2. DOCUMENTS AND PRIMARY RECORDS NAMED

Ranked by how pullable each is.

| # | Record | What is claimed about it | cite |
|---|---|---|---|
| **1** | **The handwritten attendee/working-group list published by Grant Cameron** | The interviewer reads it aloud: "**me** — Los Alamos National Labs" at the top, then **Bill Wilkinson** (CIA), **McConnell** (NSA, no first name), **John Alexander**, **Halputoff** [PHON? = Hal Puthoff], **Ed Speakman**, **Jake Stewart** [PHON?], **Ralph Freeman** [PHON?], **Bob Wood** (McDonnell Douglas). Cameron asserts Shannon wrote it. **Shannon's answer is "Somewhat"** — then that it is "conceivable that that list was made by me", and that he recognised the names and "worked closely with some of them". He does not confirm authorship outright | D2 @ 00:50:22 – 00:51:28 |
| **2** | **The Wilson–Davis memo / notes** | Described by the interviewer as a private transcript of notes found among Edgar Mitchell's papers. He states it is "download off of the US Congress's own website" — a specific, checkable assertion about a public record | D2 @ 00:21:06 – 00:23:19 |
| **3** | **The George Knapp letter, entered into the congressional record after the hearing** | Conveys Sokolov's claims: **45 incidents** in which Russian aircraft chased or fired on objects; **3 incidents** in which warplanes crashed and **2 pilots were killed**; a subsequent nationwide order to leave the objects alone. A second passage describes an object over a **missile base** during which launch systems powered up and control codes were entered | D4 @ 00:43:15 – 00:46:04 |
| **4** | **The peer-reviewed materials paper** | Nolan: "I published the first ever peer-reviewed paper on that", on the Council Bluffs molten metal | D1 @ 00:57:35 |
| **5** | **Pharis Williams's Dynamic Theory** | A five-dimensional formulation from three postulates — conservation of energy, the second law of thermodynamics, and a means of comparing the entropy of one system to another — with **mass density** as the fifth dimension, said to reproduce special and general relativity. Shannon says it has been "essentially ignored". Williams was at Los Alamos, so a **Los Alamos technical report is the thing to look for; do not assume a report number** | D2 @ 00:12:48 – 00:14:31 |
| **6** | **The 1933 Italian secret-service memo** | Described in a clip inside D3 as an internal memo including "crude drawings of the UAPs" | D3 @ 00:06:17 |
| **7** | **Grusch's promised witness list** | On tape, Mace asks which agencies and contractors should be called; Grusch offers "a cooperative and hostile witness list" after the hearing. Panellists in D4 return to it as the single most valuable unreleased item | D4 @ 00:20:07, 01:08:33 |
| **8** | **The *ESP Wars* spiral-bound compilation** | D5's speaker's claim; dated by him to 2009 and said to be on Amazon. **Off-topic file — recorded for completeness only** | D5 @ 00:54:36 |

---

## 3. WHO IS SPEAKING AND HOW THEY KNOW

The board grades on this distinction, so it is stated per speaker.

| Speaker | File | Standing | What is FIRST-HAND | What is SECOND-HAND | What is READ or INFERRED |
|---|---|---|---|---|---|
| **Oke Shannon** [PHON?] | D2 | Naval Academy at 17; 22 years commissioned, cruisers and destroyers; a year on Vietnam river patrol boats; MS physics, Naval Postgraduate School; Los Alamos, deputy group leader then program manager, special projects; medically retired after a 1999 heart attack | **The Wilson phone call** — he received it and answered it. **Working with Eric Davis** and knowing Wilson. Watching Williams derive the Dynamic Theory over three years. A 1970s bridge-watch misidentification he debunked himself. **A 1980s Los Alamos sighting** with his wife and three sons: a stingray-shaped object with a central ridge and circular glowing areas underneath, silent, seeming to flex, passing over the house and away over a canyon. His own near-death experience | The interdimensional conclusion he and Williams reached "in the mid to late 80s" — reasoned from reports, not from access. Colleagues' UFO interest at Los Alamos, which he says was **personal interest, not an official working group** | The Wilson–Davis transcript, which he and Linda read on their own initiative. He is explicit that he **cannot say whether it is true** and that he was **not read in** to the programmes it describes. **He does not claim access** at any point |
| **David Grusch** | D1, D4 | Former intelligence officer; under oath in D4's hearing footage | His own reprisal experience; handling the PDB; the DOPSR submission mechanics; **interviewing over 40 witnesses over four years**; one Navy witness interview described in detail — a ~300ft triangular craft, and afterwards milky paint and clouded headlights on the upward-facing surfaces of the man's car | **Everything about the programme itself.** He states plainly he has **not personally seen** craft or bodies. His method claims are worth recording: he sought out people who did not know each other, had colleagues interview people he had not met, and put every intermediary in front of the Inspector General to guard against circular reporting | His reasoning about why secrecy held — the Manhattan Project overlay, low institutional trust in change, adversary denial |
| **Dr. Garry Nolan** | D1 | Stanford immunologist, filmed in his own laboratory | The instrumentation and the analyses. He shows samples on camera and states results: one sample with natural magnesium isotope ratios, another "so far off Earth normal" that he reads it as engineered or industrial | **Provenance of every sample.** He is explicit that the chain of custody is Vallée's work, not his: "these are all mostly through Jacques". Countries of origin given as Brazil, the United States, France, plus an Australian and a Californian sample | His stated position is deliberately narrow: "I'm not going to say this proves anything" |
| **Jesse Michels** | D3 | Interviewer and investor; not a claimed insider | His own interviews — Malmgren, Barber, McMoneagle, Skywatcher — and one specific act of verification: he says he **debunked some of the Mars images himself**. Also the Malmgren transcription recovery | Nearly all substantive content: Magenta 1933, the ghost rockets, Bissell's remarks to Malmgren, the Skunk Works engineer's dissent | The DOE-as-custodian thesis and the Atomic Energy Act reasoning are his own inference, presented as such. Historical claims (Doolittle, Pope Pius XII) are read, not sourced on air |
| **Jamie Vernon** | D3 | Podcast producer, Columbus Ohio native | Nothing programme-related | — | The Battelle / Wright-Patterson proximity remark is offered as local knowledge and framed by Michels as "conspiracy theories" |
| **Viktor Hovland** [PHON?] | D3 | Professional golfer | Nothing | — | An interested reader. His contribution is the arc — Pentagon videos, then Lazar on Rogan, then finding the accounts corroborate — and an honest complaint that "you don't really have anything concrete" |
| **Ammar Kandil** | D1 | Documentary maker | Meeting the Berkshires witnesses in 2020; the access to Grusch during hearing week | — | Explicit that his conclusion is a judgement of character, not of evidence: he describes going "90% to 100%" on Grusch from time spent with him. **That is the file's own framing, and it is the right thing to record about it** |
| **Brian Entin and panel** | D4 | Broadcast journalism | — | The whole file is reportage of the hearing plus commentary | Ben Hansen's own line is the useful one: "a lot of this is rumour that we can't document" |
| **D5 speaker** | D5 | **[UNRESOLVED]** — never named | Claims a Lockheed Martin vice-presidency and personal acquaintance with Targ, Radin and Puthoff | — | Everything else |

---

## 4. THE 1940s–1980s THREAD

**Present, and D3 is the only file that carries it.** A clean statement of where it is and
where it is not:

**Thomas Townsend Brown — present, and the substance is elsewhere.**

- **[D3 @ 00:02:17]** In the promo montage from Michels's Joe Rogan appearance, he names
  "the legendary Thomas Towns and Brown" and says Brown's **biographer** has him on record
  in a recorded phone call, near the end of his life, saying the tests were tricky "but in
  the end, we got it to work". **The biographer is not named in this file.** Identifying him
  is step one of verifying this.
- **[D3 @ 00:28:23]** Michels's own physics position: he prefers to start from "the initial
  effect that was like an anomaly that got classified", and says **Brown "figured out
  basically a way to manipulate gravity with electromagnetism"**, from which more
  sophisticated work stems.
- **[D3 @ 00:28:55]** A texture claim worth recording because it is falsifiable in
  principle: he says "aerospace gray beards" respond to Brown either with "we can't say" or
  with unprompted aggression.
- **[D3 @ 00:36:36, 00:37:10]** Vernon and Michels on *Back to the Future*: Doc **Emmett
  Brown**, the drive to **Pasadena**, and the **flux capacitor** as an echo of **Brown's
  capacitor experiments in Pasadena**. Presented as synchronicity, not evidence. Michels
  says it was this exchange that first connected him and Vernon.

**Manhattan Project lineage and the AEC — present, in one strong passage and one weak one.**

- **[D1 @ 00:22:06]** Grusch, under his own name: the secrecy regime was built by taking
  **Manhattan Project secrecy and overlaying it** on this subject, with trust in government
  high "back in the forties post-war" and society less secular, hence the fear of religious
  shock. **This is the single most useful 1940s statement in the group.**
- **[D3 @ 00:42:38]** Michels on the **Atomic Energy Act of 1954**: the special definition of
  nuclear material means anything emitting alpha, beta or gamma radiation is "born secret",
  restricted data on discovery — so a contractor stumbling onto something is classified
  automatically. Offered as his own reading of the statute.

**Early aerospace contractors — thin and modern.** Lockheed, Northrop, Skunk Works, Boeing
and McDonnell Douglas all appear, but every appearance is contemporary or 1990s-onward. No
speaker in this group names a 1940s–1960s contractor programme.

**ABSENT — say so plainly:**

- **Electrogravitics as a term: zero occurrences across all nine files.** Michels describes
  the mechanism (gravity manipulated by electromagnetism) without ever using the word.
- **Project Winterhaven: absent.**
- **The 1956 electrogravitics survey literature: absent.**
- **The AEC by name: absent** — the Atomic Energy *Act* appears, the Commission does not.
- **Glenn L. Martin, Convair, Bahnson: absent.**
- **The Manhattan Project appears exactly once per file in D1 and D3 and nowhere else.**

**How this sits against work already in the repo.** `research/leads/gerb-corpus-25-35.md`
§3.1 covers Townsend Brown and electrogravitics from a different source and records that
Gerb **defers to Jesse Michels's Townsend Brown video** rather than making claims himself.
D3 is the Michels side of that deferral — but **the video Gerb defers to is not in this
corpus.** What D3 contains is Michels's summary of his own position plus a teaser for the
JRE appearance. **If the owner wants the Townsend Brown thread properly, the target is
Michels's dedicated Townsend Brown video, which is not among these nine files.** That is the
most actionable single sentence in this document.

---

## 5. TOP CHECKABLE LEADS

Ranked. Each row says what would verify it and whether the board already carries it. Board
status came from `tools/corpus_crosscheck.py` plus direct greps of `data/the-program.json`.

| # | Lead | Board status | What would verify it |
|---|---|---|---|
| **1** | **Oke Shannon dates Adm. Wilson's vetting call to 1999, not 2001–02.** Asked directly whether Wilson contacted him "in 2001 or 2002", he answers **"Uh, earlier than that"**, then fixes the period by his own medical history: heart attack May 1999, recuperating at home, and he was writing when the call came. Linda, off-mic, confirms the year | **`Oke Shannon` is ABSENT — zero occurrences of "Shannon" anywhere in `data/the-program.json`.** The board carries `wilson-davis-memo` and `eric-davis`, both of which the memo's own text ties to Shannon | The memo is dated 2002. A vetting call three years earlier either lengthens the arc or contradicts the account. Compare Shannon's stated chronology against the memo text the board already holds, and against Davis's and Wilson's public statements. **This is a first-hand recollection from a named participant and it is the highest-value item in the group** |
| **2** | **The attendee list Shannon half-confirms.** Nine names, one employer each, "me — Los Alamos" at the top | Wilkinson, Speakman, Stewart and Freeman are all **ABSENT**. `John B. Alexander`, `Robert M. Wood`, `Harold Puthoff`, `McDonnell Douglas Corporation` and `Grant Cameron` are all **existing nodes** | Locate Cameron's published image. Then adjudicate each name: `Ed Speakman` [PHON?] and `Jake Stewart` [PHON?] and `Ralph Freeman` [PHON?] are all single-pass caption reads with no corroboration. **`McConnell` has no first name in the transcript and must not be resolved by guessing** |
| **3** | **Pharis Williams and the Dynamic Theory.** A named Los Alamos physicist, a named formalism, and Shannon's claim that he and Williams suspected the work had been "advanced much further" by better-funded parties | **ABSENT** — zero occurrences of "Pharis". The near miss the crosscheck reports is a different J. Williams in the AAWSAP DIRD series | Find the Los Alamos report. It is a document with a title, an author and a number, which makes it the most cleanly pullable item here. **Do not assume the report number.** The name is `Ferris Williams` in the captions and Williams is called "Willie" throughout |
| **4** | **Harald Malmgren and Richard Bissell.** Michels claims Bissell told Malmgren about "the 1933 magenta", and treats it as independent corroboration of Grusch's Italy claim | **Both ABSENT** — zero occurrences of "Malmgren" or "Bissell" | Malmgren was a real and documentable presidential aide; Bissell a documentable CIA officer. Two checks, in order: (a) does the Malmgren interview recording contain the words attributed to him, given Michels says his voice was weak and the line was recovered by later transcription; (b) the claimed Wikipedia rewrite is checkable in page history, and Michels's account of it is checkable independently of whether the underlying claim is true |
| **5** | **The George Knapp / Boris Sokolov letter in the congressional record** | The board carries **Sokolov** via the SETKA material and `yury-platov`, and carries `hearing-2023-07-26`. **The 2023 letter itself does not appear** | It is a document entered into the record of a named hearing and should be retrievable as such. The specific numbers to check: 45 incidents, 3 crashes, 2 pilots killed, and the missile-base launch-code episode |
| **6** | **Thomas Townsend Brown** | **ABSENT — zero occurrences of "Townsend Brown".** "electrogravit" appears **twice** in the whole board, both inside the 2017 TTSA launch node's list of announced divisions. `Thomas Townsend Brown` and `Project Winterhaven` are already **candidates** in `research/leads/gerb-candidates.txt` from the Gerb corpus | See §4. The next step is not this corpus — it is Michels's dedicated Townsend Brown video, plus identifying the biographer he cites. **Two corpora have now independently surfaced Brown as a gap; note that both are YouTube captions read the same way, so this is convergent surfacing, not corroboration of any claim** |
| **7** | **Nolan's magnesium isotope result and its chain of custody** | **`Garry Nolan` IS a node** (see the crosscheck caveat below), as are `stanford-nolan-lab`, `paper-nolan-vallee-2022`, `jacques-vallee` and the Council Bluffs event | The published paper the board already cites is the anchor. What D1 adds is Nolan **on camera in his own lab**, stating the provenance limit himself — "these are all mostly through Jacques" — and naming Brazil, the United States, France, Australia and California as origins. That attribution is worth pinning to the existing node |
| **8** | **Michels's named Skunk Works dissenter** | — | A ~30-year Skunk Works engineer who accepts anomalous sightings but attributes recovered hardware to human programmes. Unnamed, so unverifiable as stated, **but recorded because a board that only collects affirmative claims is a board with a selection problem** |

**Leads this group does NOT yield, stated so nobody re-reads the files looking:**

- **D4 yields almost nothing the board lacks.** It is broadcast coverage of a hearing the
  board already carries as `hearing-2023-07-26`, down to `ch-2023-07-26d`, "Gaetz: the Eglin
  radar sequence", and `l-eglin`. Its only incremental item is lead 5.
- **D5 yields no programme lead** (see §0a).
- The four outright off-topic files yield **nothing**.

### A defect found in `tools/corpus_crosscheck.py` while using it

The tool reported two **false ABSENT** verdicts in this run, which is the error class its own
README names as the expensive one:

- **`Gary Nolan` → ABSENT**, but the board carries the node `garry-nolan`, **Garry Nolan**.
  The NODE matcher missed a one-letter spelling difference.
- **`Mike Gallagher` → ABSENT**, but the board carries the node `mike-gallagher` — and the
  tool's own NEAR MISS block prints that node's narrative while still ruling ABSENT.

Both were caught only because the ABSENT verdicts looked implausible and were re-checked by
grep. **Every ABSENT verdict in the table above was re-checked against
`data/the-program.json` directly.** The false ABSENT on Gallagher is the more diagnostic of
the two: the near-miss machinery found the right node and the verdict logic did not use it.

---

## 6. CORRUPTION WATCHLIST

**Nothing in the "unresolved" block may reach the board under the spelling given.**

### 6a. Resolved with confidence, but the caption is wrong

| Raw caption | Reading | conf. | cite |
|---|---|---|---|
| `Jesse Michaels` | **Jesse Michels** | high — an existing board node | D3, D5-adjacent files |
| `David Grush` / `GRESH` / `GRESTE` / `GRACE` / `GRAPES` / `BRUSH` / `CRUSH` | **David Grusch** | high | D1 @ 00:02:44; D4 throughout |
| `David Faber` / `DAVID FAVOR` | **David Fravor** | high — D4 also gives "Black Aces squadron commander", which fixes it | D4 @ 00:01:44, 00:15:40 |
| `Ross Cold Heart` / `Ross Cold Hard` | **Ross Coulthart** | high | D4 @ 00:01:09, 00:15:07 |
| `Gary Nolan` | **Garry Nolan** — the board's spelling, two Rs. D1's own on-screen caption gets it right at 00:51:12 and wrong elsewhere | high | D1 |
| `Halputoff` / `how put off` / `dr hal put off` | **Hal Puthoff** | high | D2 @ 00:27:25, 00:50:56; D5 @ 00:39:02 |
| `Macdonald Douglas` | **McDonnell Douglas** | high | D2 @ 00:50:56 |
| `Luis Alzando` | **Luis Elizondo** | high | D2 @ 00:40:13 |
| `Jacqu Valet` | **Jacques Vallée** | high | D3 @ 00:43:44 |
| `Beatatric Valale` | **Beatriz Villarroel** — described as a Swedish astronomer prominent in the subject; **the board already carries `beatriz-villarroel`**, which is what makes the reconstruction safe | high, **but only because the board corroborates it** | D3 @ 00:07:23 |
| `Tom Deong` | **Tom DeLonge** | high | D3 @ 00:37:10 |
| `a lobe` / `Obby` | **Avi Loeb** | high | D3 @ 00:29:28 |
| `Zahi Haw` | **Zahi Hawass** | high | D3 @ 00:18:56 |
| `Cosmatron` | **Cosmotron**, Brookhaven | high on the name; **the surrounding claim is false as stated** | D3 @ 00:42:38 |

### 6b. [PHON?] — best reconstruction only. Search strings, not facts

| Raw caption | Reconstruction | conf. | cite | note |
|---|---|---|---|---|
| `Oak Shannon` | **Oke Shannon** | medium-high | D2 | Named in the Wilson–Davis material; the interviewer addresses him as "Oak" throughout, so the caption may simply be phonetic |
| `Ferris Williams`, "Willie" | **Pharis Williams** | medium | D2 @ 00:08:11 | Verify via the Los Alamos report, not via the caption |
| `Harold Maldgren` | **Harald Malmgren** | medium-high | D3 @ 00:22:18 | Both given name and surname are corrupted |
| `Towns and Brown` / `Townson Brown` | **Thomas Townsend Brown** | high | D3 | The *Back to the Future* passage independently supplies "Emmett", which supports the reading |
| `James Dittle` | **James Doolittle** | medium | D3 @ 00:06:50 | The board carries one "Doolittle" occurrence; check it before relying on this |
| `Victor Havlin` | **Viktor Hovland** | medium-high | D3 | Norwegian golfer, top-10, playing Philadelphia then Charlotte then the Memorial — enough to fix identity, none of it programme-relevant |
| `Justin Matine` / `Justin Batine` | **Justin Mateen** | high | off-topic file | Off-topic; listed only so nobody re-derives it |
| `McGonagle` / `McMonagle` | **Joseph McMoneagle** | medium-high | D3 @ 00:32:16 | The speaker corrects himself on tape, and still lands short |
| `Barty Cyrell` | **Bart Sibrel** | medium | D3 @ 00:33:54 | Off-topic content (moon landing); listed for completeness |
| `Dan Berish` | **Dan Burisch** | medium | D3 @ 00:27:17 | Named in a list with Lazar |
| `Randall Clyer` | **Randal Kleiser** | medium | D3 @ 00:38:16 | *Flight of the Navigator*; no programme claim attached |
| `high mesh` | **Haim Eshed** | medium | D3 @ 00:30:36 | Described as having run the Israeli space programme |
| `Chris Ramsey` | **Chris Ramsay** | low-medium | D3 @ 00:29:28 | Spelling unverified |
| `doctor thought of` | **Puthoff** | low-medium | D5 @ 00:54:36 | A broken clause, not a name. Supported only by the same speaker naming Puthoff clearly at 00:39:02 |
| `wall thornhill` | **Wal Thornhill** | medium | D5 @ 00:39:02 | Off-topic file |

### 6c. [UNRESOLVED] — must not reach the board under these spellings

| Raw caption | Where | Why it is unresolved |
|---|---|---|
| `Jeffrey Kruchank` | D3 @ 00:24:01 | Named as the researcher who "went really deep into" Bluegill Triple Prime. No second mention, no affiliation, no work named. **The test name itself is stable and checkable; the researcher's is not** |
| `Ed Speakman` | D2 @ 00:50:56 | Read aloud once from a list. No affiliation given |
| `Jake Stewart` | D2 @ 00:50:56 | Read aloud once. No affiliation given |
| `Ralph Freeman` | D2 @ 00:50:56 | Read aloud once. No affiliation given |
| `Bill Wilkinson` | D2 @ 00:50:22 | Read aloud once, with "CIA" attached. Common surname, single pass |
| `McConnell` | D2 @ 00:50:56 | **The transcript itself says there is no first name on the list.** Any resolution would be a guess. Record as surname-plus-NSA and nothing more |
| `Jake Jo` | D3 @ 00:10:06 | Given as a Skywatcher figure who preceded Barber by four years. Unreconstructable |
| `neuritators` | D3 @ 00:10:06 | The speaker's own hedge is "or whatever". A term, not a name, and possibly not the real one |
| `Finley Mountain Range` | D3 @ 00:11:13 | Given as a west Texas operating site. No such range is confidently identifiable from the caption |
| `Lawrence` (D3) | D3 @ 00:25:40 | Michels names "Lawrence" in the same breath as a claim that **Jeff Bezos's grandfather gave him UAP material**. The fragment is too broken to attach a surname. **Record the claim, not the identification** |
| `Lawrence` (D5) | D5 @ 00:00:00 | The person who introduced the D5 speaker. Different person, same first name, equally unresolvable |
| **The D2 host and show** | D2 | Never named across 55 minutes. Internal evidence only: British-inflected, works with a second interviewer, met Shannon and Linda in Florida, previously interviewed Elizondo, references a British Admiral of the Fleet |
| **The D5 speaker** | D5 | Never named. Claims a Lockheed Martin vice-presidency, retirement c. 2011, a daughter at Lockheed Martin, and that Dean Radin lives "not too far north" of him. **A claimed senior contractor executive is exactly the kind of name that must not be guessed at** |

---

## 7. What this group is worth, honestly

**One file carries the group.** D2 is a first-hand account from a named participant in the
Wilson–Davis chain who is **absent from a board that already carries the memo, Davis, Wilson
and Mitchell**. Its date correction on the Wilson call is the single most checkable new
claim in the nine files.

D1 and D3 are worth a pass each — D1 for Nolan on camera stating his own provenance limit
and for Grusch's Manhattan-Project-overlay formulation, D3 for the Townsend Brown pointer
and the Malmgren/Bissell claim.

**D4 is on-topic and nearly redundant**, and saying so is the useful result: a session that
reads it hoping for new material will spend eighty-three minutes recovering a hearing the
board already holds.

**Five of nine files yield nothing.** Four are a breathing exercise, a boxing interview, a
venture-capital interview and an archaeology dispute. The fifth is an hour of theosophy with
two biographical fragments attached.
