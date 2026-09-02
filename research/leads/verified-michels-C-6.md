# Section C verification, agent 6 (Michels corpus, 2 September 2026)

**Rows assigned:** section C2 of `research/leads/michels-triage-5.md`, rows 5, 7, 8, 11, 12
and 13. Agents 3 and 4 hold the rest of that table; I read both summary tables first and have
not revisited a row either of them adjudicated.

**Status: nothing was added to the board.** No file under `research/*.json`, `tools/`, `data/`
or `dist/` was touched and no git command was run. Everything below is a draft for Stewart to
accept or reject. Every timestamp was re-read in the transcript file rather than taken from
the lead map's paraphrase, and in three cases that re-reading is the finding: the lead map
attributes to one speaker what a different speaker says, or states a fact the passage does not
carry.

**One row overlaps agent 3.** Row 13 is `thomas-townsend-brown`, which agent 3 handled at
4.C2 / 6.C2 / 5.C2. Agent 3 explicitly left the Teller-to-Odlum introduction and the Stevenson
telegram in NOT REACHED, and those two items are all I treat here. Nothing below revisits the
FBI radar finding, which stands.

---

## Summary

| # | Node id | Verdict | Reason |
|---|---|---|---|
| 5.C2 r5 | `dylan-borland` | ATTRIBUTE | Borland on the record alleging AARO transmitted to ODNI a Memorandum for Record other than the corrected one he signed. **The lead map says he did not sign it; he says he did sign a corrected version and that a different one was sent.** The board carries nothing on this |
| 5.C2 r7 | `glenn-gaffney` | ATTRIBUTE | A sitting member of Congress names Gaffney, unprompted, as his first choice of subpoena or SCIF target. The node's only naming is Knapp's. This is a second, independent naming from a different kind of speaker |
| 5.C2 r8 | `travis-taylor` | ATTRIBUTE | The row's headline fact is a **false ABSENT**: the board already carries the UAPTF chief-scientist role and the overlap. What is new is Fugal's account of the arrangement itself, and his statement that the ranch work was the reason Taylor was called to the post |
| 5.C2 r11 | `salvatore-pais` | ATTRIBUTE | **The fear, the motel interview and the refused topic are Michels', not Burlison's.** Burlison's own account is an official Pax River meeting with Kosloski present, at which the Navy conceded one device was built and tested. That corroborates a claim the node currently rests on secondary reporting for |
| 5.C2 r12 | `eric-burlison`, `aerospace-corporation` | ATTRIBUTE (two drafts) | The letter campaign beyond MITRE is **already on the board** in Burlison's own X quote. What is new is the Aerospace Corporation SCIF meeting, which lands directly on a Tier 3 claim saying no one has addressed the corporation's knowledge publicly. **IDA is not a letter recipient in the passage** |
| 5.C2 r13 | `thomas-townsend-brown` | NO ACTION | Both leftover items are second-hand descriptions of private documents, spoken as the host's own synthesis. The FBI file the board cites was full-text searched and contains none of the three names. See section 6 |

Counts: **0 RECORD, 5 ATTRIBUTE, 1 NO ACTION, 0 NOT REACHED.**

No RECORD contradicted a transcript, because no row here had a document to open that was not
already opened by agent 3. The three contradictions in this pass are all against the **lead
maps**: the Borland MFR signature, the Pais attribution, and the IDA letter. All three are
stated in the sections below.

---

## 1. `dylan-borland` (triage-5 C2 row 5) - ATTRIBUTE

Read at 1:56:39 to 2:04:40 and 2:21:37 to 2:23:27 in
`dist/transcripts/md/2026-08-05 i-saw-a-triangle-shaped-ufo-at-a-nasa-hangar-dylan-borland-tells-all.md`.

**The lead map's paraphrase is wrong on the load-bearing detail.** It says Borland alleges
AARO sent ODNI "a Memorandum for Record he did not sign". What he says is the opposite and
sharper: AARO sent him a version he told them was wrong, AARO acknowledged that in an email
and asked him to write the corrections, he made them, signed, and returned them with
confirmation of receipt, and then a different, uncorrected version reached ODNI. The
signature is the whole point of the allegation, not its absence.

The transcript renders the AARO director's surname as "Kozloski", "Kosloski", "Loski" and
"Lasky" in the space of two minutes. The board's spelling is `jon-kosloski`. **Do not carry
any of the caption forms**, and note that Borland says of him "I never talked to him", so the
allegation is against the office and its transmission, not against a conversation.

Two further things in the passage that are not in the claim below and should not be added
without their own sourcing: the "fourth drawing" allegation, which Borland attributes
entirely to what Jeremy Corbell was told; and the assertion that a leak of classified
information and medical records to Corbell and Knapp was a felony, which is his
characterisation. The passage is also where he explains why he refused to give AARO the
names of people or the programme name, which is his stated reason for going to Congress.

The original-classification-authority argument is the second half and it is the more
checkable one, because it is an argument about a rule rather than about an event: AARO holds
no original classification authority, so a classification decision on his account had to be
referred out to the IC and to the private companies, and the fact that his triangle account
came back unclassified while other drawings did not is therefore, on his reading, itself
documentary. **Nothing was opened that establishes AARO's classification authority either
way**, so the claim below states it as his argument and not as a fact about AARO.

Placement: on `dylan-borland` only. The allegation names Kosloski, but an unadjudicated
allegation by one witness belongs with the witness who makes it; putting it on
`jon-kosloski` would read as the board asserting it.

```json
{
 "id": "dylan-borland",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 5 August 2026, Dylan Borland said that AARO sent him a Memorandum for Record of his interview that he told them was wrong, that AARO acknowledged the error in an email and asked him to write corrections, that he made and signed the corrections and kept his email confirming their receipt, and that when he went to ODNI on 10 September 2025 the version AARO had transmitted was not the corrected one: 'Arrow had sent over a false MFR, said that was the true one.' He says he retained the corrected document (1:58:28 to 1:59:26).", "source": "American Alchemy with Jesse Michels, 'I Saw a Triangle Shaped UFO At a NASA Hangar!' -Dylan Borland Tells All, 5 August 2026, 1:58:28 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3402784095.mp3"},
  {"tier": 2, "text": "In the same episode Borland argued that because AARO holds no original classification authority it had to refer his account out to the intelligence community and to private companies for a classification determination, and that his triangle account coming back unclassified while other drawings were classified is therefore itself evidence about what was seen: 'they would have to be classified' (2:23:27). Nothing opened for this board establishes AARO's classification authority either way; this is recorded as his argument.", "source": "American Alchemy with Jesse Michels, 'I Saw a Triangle Shaped UFO At a NASA Hangar!' -Dylan Borland Tells All, 5 August 2026, 2:23:27 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3402784095.mp3"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'I Saw a Triangle Shaped UFO At a NASA Hangar!' -Dylan Borland Tells All, episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3402784095.mp3", "date": "2026-08-05"}
 ]
}
```

---

## 2. `glenn-gaffney` (triage-5 C2 row 7) - ATTRIBUTE

Read at 1:48:44 in
`dist/transcripts/md/2026-07-02 congressman-president-trump-was-briefed-on-alien-hybrids.md`.

The node's own text says Gaffney "appears on this board for a single reason and the board does
not stretch it", that reason being George Knapp naming him to the committee on 9 September
2025. This adds a second naming of a different kind. Michels asks whom Burlison would pick to
subpoena or get unlimited SCIF time with, and Burlison answers first and by name.

Two names travel with the answer and neither should be carried further than the passage
supports. **Steve Cantrell**, described only as "former Air Force" and "senior intelligence
from the Air Force", has zero occurrences in `data/the-program.json` and is a section A or B
question for a later pass, not a correction. **General McCasland** is named third, "sadly",
which is consistent with the disappearance the board already carries and with agent 4's
finding that the SAPOC placement is not Burlison's. Burlison also names a fourth person, since
deceased, whose name he could not recall on air; that is a blank and must stay one.

Agent 3 adjudicated the triage-4 Gaffney row at 4.C9 as NO ACTION on the "twice, in 2008 and
2010" material. This draft does not touch that and does not assert the transfer-veto claim.

```json
{
 "id": "glenn-gaffney",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 2 July 2026, Rep. Eric Burlison was asked whom in government he would most want to subpoena or question at length in a SCIF about UAP and named Gaffney first: 'I would say probably Glenn Gaffney who is you know former CIA a lot of people I talked to you say that this is somebody that we need to talk to.' He then named Steve Cantrell, described only as former Air Force senior intelligence, and General McCasland (1:48:44).", "source": "American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 1:48:44 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3", "date": "2026-07-02"}
 ]
}
```

---

## 3. `travis-taylor` (triage-5 C2 row 8) - ATTRIBUTE

Read at 2:16:52 to 2:19:37 in
`dist/transcripts/md/2026-07-26 theres-a-ufo-under-the-ranch-skinwalker-owner-breaks-silence.md`.

The row is keyed to `l-skinwalker` and `skinwalkers-at-the-pentagon`, but every fact in it is
about a person who has his own node, so the draft goes there.

**Half the row is a false ABSENT.** `travis-taylor` already carries the UAPTF chief-scientist
role as Tier 2 off Science magazine, and already carries the overlap as a Tier 3 inference.
What the board does not have is any account of how the two roles sat together, and that Tier 3
claim says so in terms: "with no public account of what, if anything, crossed between them."

Fugal's account does not disturb that sentence and I am not proposing a change to it. He says
explicitly that Taylor disclosed nothing: the ranch team had no idea, Taylor was under
national security oaths, and "he didn't breach that not even once". What he adds is the shape
of the arrangement and one causal claim the board does not have anywhere: that Taylor was
called to the post in large part because of the ranch work. He also says Taylor had no UFO
experience before the ranch and was "a vocal skeptic", and that members of his own team,
including his head of security, felt betrayed when the role came out.

**The Tier 3 claim's wording survives and should not be softened on the strength of this.** An
account of the arrangement is not an account of what crossed between the two roles, and Fugal
is asserting that nothing did.

```json
{
 "id": "travis-taylor",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 26 July 2026, Brandon Fugal said the Skinwalker Ranch team did not know Taylor had been made chief scientist of the UAP Task Force while he was returning seasonally to work on the ranch investigation, that Taylor was under national security oaths and confidentiality and 'didn't breach that not even once', and that the team learned only once he had authorisation to disclose it. Fugal said members of his team, including his head of security, initially felt betrayed (2:17:46 to 2:18:44).", "source": "American Alchemy with Jesse Michels, 'There's A UFO Under the Ranch!' - Skinwalker Owner Breaks Silence, 26 July 2026, 2:17:46 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9910649891.mp3"},
  {"tier": 2, "text": "In the same episode Fugal stated the direction of the connection: that the reason Taylor 'was called in and called to that position in large part was was really because of uh the work at' Skinwalker Ranch, and that before being brought to the ranch Taylor had no experience of the subject and was a vocal skeptic (2:16:52, 2:19:37).", "source": "American Alchemy with Jesse Michels, 'There's A UFO Under the Ranch!' - Skinwalker Owner Breaks Silence, 26 July 2026, 2:19:37 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9910649891.mp3"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'There's A UFO Under the Ranch!' - Skinwalker Owner Breaks Silence, episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9910649891.mp3", "date": "2026-07-26"}
 ]
}
```

---

## 4. `salvatore-pais` (triage-5 C2 row 11) - ATTRIBUTE

Read at 0:35:56 to 0:39:35 in
`dist/transcripts/md/2026-07-02 congressman-president-trump-was-briefed-on-alien-hybrids.md`.

**The lead map merges two speakers into one and attributes the wrong half to the congressman.**
The transcript carries no speaker labels, and the row reads as though Burlison described Pais
as fearful and refused an on-record topic. He did not. The passage splits cleanly:

| what is said | who says it | how you can tell |
|---|---|---|
| an official visit to Pax River, requested and greenlit, at which he asked to meet Pais and did | Burlison | "when I made that request, they, once they greenlit that venue"; a congressional site-visit request |
| Pais seems fearful, communication is cloak and dagger, an interview in a motel near Pax River where a camera failed, and Pais stopping the science questions | **Michels** | Pais addresses the speaker by name: "Jesse, stop right there" |
| Kosloski present and the only other person in the room following the physics | Burlison | "the only person in the room", "everybody else that was in that room walked out" |

The half that belongs to Burlison is the more valuable half and it is not on the node. The
node's Tier 2 claim that NAWCAD funded testing and could not demonstrate the effect currently
rests on secondary reporting summarised at Wikipedia. Burlison is a named person on the record
saying the Navy told him, at Pax River, that one of the devices had been built and tested
without a definitive result, and adding Pais's own position that it was not built to his
specifications. That second part is nowhere on the node and is the kind of thing the file
wrapper cannot supply, because it is about what the builder said afterwards.

**Do not let the synthesis travel with it.** Burlison says in the same breath "I'm not putting
words in his mouth, but I picked up that" a faithful build would probably have given a more
definitive result. That is his inference and it is excluded from the draft. The claim below
also does not say which patent was tested: Burlison says "I believe the anti-gravitic one",
and a hedge is not an identification.

```json
{
 "id": "salvatore-pais",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 2 July 2026, Rep. Eric Burlison described an official visit to NAS Patuxent River at which he asked for and was granted a meeting with Pais, went down the list of the patents, and was told that one of them had been built and tested but that no definitive result was obtained. Burlison said Pais's position was 'that was not built to his specifications', and that Dr. Jon Kosloski was present and was the only other person in the room following the physics (0:36:49 to 0:39:35). Burlison hedged which patent was tested, saying only 'I believe the anti-gravitic one'.", "source": "American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 0:36:49 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3"},
  {"tier": 2, "text": "In the same episode Jesse Michels, not Burlison, described Pais as fearful and hard to reach, said he had interviewed him in a motel near Pax River during which a camera failed, and said Pais stopped him at a point in the science with 'Jesse, stop right there' and declined to discuss it further (0:37:47 to 0:38:43). The lead map for this corpus attributes this account to Burlison; the transcript attributes it to Michels.", "source": "American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 0:37:47 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3", "date": "2026-07-02"}
 ]
}
```

---

## 5. `eric-burlison` and `aerospace-corporation` (triage-5 C2 row 12) - ATTRIBUTE, two drafts

Read at 0:18:53 to 0:21:35 and at 2:11:52 in
`dist/transcripts/md/2026-07-02 congressman-president-trump-was-briefed-on-alien-hybrids.md`.

**The row's headline is already on the board.** `eric-burlison` carries his own X quote naming
RAND, MITRE, Aerospace Corp, MIT Lincoln Labs and Northrop Grumman, and `aerospace-corporation`
carries the same statement as Tier 2. The transcript's 2:11:52 line ("whether it's MITRE or
RAND or MIT Lincoln Labs") is the same campaign in the speaker's own voice and adds nothing.

**IDA is not a letter recipient in this passage.** The lead map lists "Aerospace Corporation,
RAND and IDA". The Institute for Defense Analyses is named by Michels, at 0:18:53, as
historical context for Harald Malmgren, not by Burlison as a body he has written to. I opened
`burlison.house.gov/media/press-releases` and it lists no release naming RAND, Aerospace
Corporation or IDA; the four UAP releases on that page are the NDA directive memorandum of
1 August 2026, the NDA directive statement of 29 July 2026, the disclosure-framework amendment
of 22 July 2026, and a 8 July 2026 press on CIA and FBI records for the 1996 Brazil incident.
**A letter to RAND or IDA is therefore not documented from here and must not be asserted.**

What is genuinely new is the Aerospace Corporation meeting, and it lands on a specific hole.
The `aerospace-corporation` node's Tier 3 claim reads that no public document establishes
whether the corporation had any institutional role in or knowledge of the retrievals Eric
Davis described, "and the corporation has not addressed it publicly". Burlison says a letter
went to Aerospace early, from his Oversight role, that Aerospace responded by sending two
people from its executive team, that the meeting took place in a SCIF under the Biden
administration, and that they knew nothing. That is the corporation putting people in a room
and answering, and it is the first such account the board would carry.

His reading of the answer is in the same passage and is his own: that compartmentation and
staff turnover mean people now in those roles will not find the material unless they dig, which
is why he says the work has to be crowdsourced and handed to them as a named file and a date.
That reading is recorded as his, not as a finding.

```json
{
 "id": "eric-burlison",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 2 July 2026, Rep. Eric Burlison said his office sent an early letter to The Aerospace Corporation from his House Oversight role, that Aerospace responded by sending two people from its executive team, that the meeting was held in a SCIF during the Biden administration, and that 'they knew nothing' about UAP or reverse engineering. He said he expects to go back to them with more specific and detailed questions (0:19:48).", "source": "American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 0:19:48 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3"},
  {"tier": 2, "text": "In the same episode Burlison gave his reading of that answer and of the structure generally: that a programme is 'probably organized from the ffrdc level' because an FFRDC can create the programme and the funding justification and then report upward only what it must, and that turnover and compartmentation mean current officeholders will not find decades-old material unless outsiders hand them a named file and a date (0:20:42, 1:50:35). He states this as his own inference.", "source": "American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 1:50:35 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3", "date": "2026-07-02"}
 ]
}
```

```json
{
 "id": "aerospace-corporation",
 "cls": "institution",
 "claims": [
  {"tier": 2, "text": "The corporation has now been questioned by Congress on the subject, on one member's account. On American Alchemy with Jesse Michels, 2 July 2026, Rep. Eric Burlison said his office wrote to The Aerospace Corporation from the House Oversight Committee, that the corporation sent two members of its executive team, that the interview took place in a SCIF during the Biden administration, and that they had no knowledge of UAP or reverse engineering: 'they knew nothing' (0:19:48). No document of that meeting has been opened for this board.", "source": "American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 0:19:48 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3", "date": "2026-07-02"}
 ]
}
```

**A note on the Tier 3 claim, not a proposed change.** If Stewart takes the second draft, the
`aerospace-corporation` Tier 3 sentence "and the corporation has not addressed it publicly"
becomes arguable, because sending two executives into a SCIF is a form of addressing it, even
if the answer was nothing. It is still true that the corporation has issued no public
statement. I would leave the Tier 3 wording alone and let the two claims sit next to each
other, which is what the board does elsewhere.

---

## 6. `thomas-townsend-brown` (triage-5 C2 row 13) - NO ACTION

The two items agent 3 left: the Teller-to-Odlum introduction and the Stevenson telegram.

**Both are the host speaking, and both describe documents nobody has produced.** The Odlum
item is at 2:26:29 in
`dist/transcripts/md/2026-07-20 proof-that-nasa-censored-moon-photos-and-the-astronauts-knew.md`,
inside a run of Michels' own Teller synthesis ("thing after thing after thing"), and the
caption renders the name "Floyd O'Lum". The telegram is at 1:29:23 to 1:30:18 in
`dist/transcripts/md/2026-07-14`, described as a wartime message from William Stevenson to
Brown's wife saying her husband was safe after a technology-retrieval mission behind enemy
lines. No archive, collection or repository is named for either.

I did the one cheap check available. Agent 3 established that
`archive.org/download/tt-brown/...djvu.txt` full-text searches the FBI file the node already
cites. I pulled the same 263,609 bytes and searched it:

| term | occurrences in the released FBI file |
|---|---|
| Odlum | 0 |
| Teller | 0 |
| Stevenson | 0 |
| Stephenson | 0 |
| Northrop | 0 |
| Atlas | 0 |
| Josephine | 2 |

The two Josephine hits are "Josephine Beale Brown" in the subject data and an address
furnished for "Mrs. JOSEPHINE BROWN". So the wife's name in the telegram story is the only
element of either item that the file corroborates, and a wife's name is not evidence of a
telegram.

**This is a weak absence and I am not proposing it as a claim.** The released file is a
partial release of one Fraud Against the Government inquiry; it is not a complete record of
who funded Brown. What it does establish is that the contemporaneous federal investigation
into exactly the question of who was backing Winterhaven names none of these three men, which
is a reason not to carry the patronage story on this board rather than a finding against it.

Two further reasons to leave it alone, both from the triage file itself:

- Section D5 records that `William Stephenson` in map 21 and `William Stevenson` in map 24 are
  the same man under two spellings, and that a second, differently spelled William Stevenson
  wrote the biography. Michels says so on air and says it confused him. Carrying a telegram
  attributed to a name with a live spelling collision is how a board acquires a wrong node.
- Section D7 carries Floyd Odlum out of the noise pile as an "exception" purely on adjacency
  to Brown. Adjacency to a node is not a record. "Odlum" has zero occurrences in
  `data/the-program.json` and creating him would be section A promotion work, not a correction.

Nothing here disturbs agent 3's FBI radar finding or the 30 August Winterhaven correction.

---

## NOT REACHED

None. All six assigned rows were adjudicated.

---

## Access notes from this pass

To add to the reach facts:

- `burlison.house.gov` answers WebFetch. The press-release index returns only the most recent
  page, so a release from May 2026 is not on it and a member's older correspondence has to be
  reached another way.
- `archive.org/download/...djvu.txt` answers curl directly, as agent 3 recorded. Confirmed
  again here: the Brown FBI file came down in one request and full-text searching it costs
  nothing. This is the cheapest test available for "does the file the board already cites
  actually say this", and it should be the first thing tried on any Brown row.
- The Michels transcripts carry **no speaker labels**. Two of the three contradictions in this
  pass exist because a lead map assigned a passage to the guest when the interviewer was
  speaking. The reliable tell is a vocative: when a third party in the story addresses the
  speaker as "Jesse", the speaker is Michels. **A later pass should treat every single-speaker
  attribution in the lead maps as unverified until the passage is re-read.**
