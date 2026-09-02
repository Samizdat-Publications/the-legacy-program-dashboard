# Section C verification, agent 4 (Michels corpus, 2 September 2026)

**Rows assigned:** row C6 of section C in `michels-triage-4.md`, and the thirteen rows of
section C2 in `michels-triage-5.md` that agent 3's summary table does not list (rows 2 to 14).
Agent 3 handled row 1 of triage-5 C2 (`mit-lincoln-laboratory`) and I have not revisited it.

**Status: nothing was added to the board.** No file under `research/*.json`, `tools/`, `data/`
or `dist/` was touched and no git command was run. Everything below is a draft for Stewart to
accept or reject. Every URL here was opened from this machine. Every timestamp was re-read in
the transcript file rather than taken from the lead map's paraphrase, and in two cases that
re-reading is the finding: the lead map attributes to one speaker what a different speaker
says.

**One node overlaps agent 3.** `william-mccasland` is triage-4 C1 (agent 3, ATTRIBUTE on the
disappearance details) and triage-5 C2 row 6 (mine, the SAPOC placement). The two drafts do
not overlap in content. Read them together; section 2 below carries a warning that agent 3's
section 1 does not.

---

## Summary

| # | Node id | Verdict | Reason |
|---|---|---|---|
| 5.C2 r14 | `stargate-program` | RECORD | The 1995 AIR evaluation was opened in full. It confirms the sentence the node already quotes and supplies the document number and a URL the node lacks. Utts is a reviewer, not an author |
| 5.C2 r6 | `william-mccasland` | ATTRIBUTE | **The SAPOC placement is Michels', not Burlison's**, and is hedged in one of the two episodes. Burlison on the record declines the gun detail. Three speakers decline to corroborate |
| 5.C2 r2 | `sean-kirkpatrick` | ATTRIBUTE | Fugal names a date, a duration and a photograph he says he published, against a denial the board carries nowhere. The board has no Kirkpatrick pre-2022 denial and no Fugal rebuttal |
| 4.C6 | `italo-venturelli` | ATTRIBUTE | A named forensic physician describing an autopsy he says he performed and a pending court exhumation request. **Every proper noun in the passage is caption-corrupted and none may be carried** |
| 5.C2 r9 | `tim-gallaudet` | NO ACTION | False ABSENT, and the board is more precise. The board carries the council as announced by ODNI on 22 June 2026 reporting to an interagency UAP Governance Board. Gallaudet's on-air "reports to the ODNI" is the looser form |
| 5.C2 r3 | `battelle` | NO ACTION | NOT OPENED. `battelle.org` is behind a Cloudflare bot wall to both curl and WebFetch. A wall is not a document |
| 5.C2 r4 | `immaculate-constellation` | NO ACTION | The row records that Brown states the whole account as his own inference and says so on air. An attributed inference about cognizance is not a source the node otherwise refuses to name |
| 5.C2 r10 | `robert-hastings`, `robert-salas` | NO ACTION | Agent 3 adjudicated the same instability at 4.C8. Recording one of the four numbers would assert precision the corpus does not have. I concur and add nothing |
| 5.C2 r5, r7, r8, r11, r12, r13 | see NOT REACHED | NOT REACHED | Six rows not adjudicated |

Counts: **1 RECORD, 3 ATTRIBUTE, 4 NO ACTION, 6 NOT REACHED.**

The RECORD does not contradict its transcript. The two contradictions in this pass are both
against the **lead maps**, not against a document: the SAPOC attribution in triage-5 C2 row 6,
and the "no such general" characterisation in the same row. Both are in section 2.

---

## 1. `stargate-program` (triage-5 C2 row 14) - RECORD

The row says the 1995 evaluation is "a document behind it that the board does not appear to
name". That premise is wrong: the node's `desc` already names the American Institutes for
Research, both reviewers, and the finding, and its third claim already quotes the conclusion.
What the node lacks is a document number and a URL, so the claim reads as Tier 1 with nothing
a reader can open. That is worth fixing and it is why this is a RECORD rather than a NO
ACTION.

I opened the report. Its title page reads:

| field | what the title page says |
|---|---|
| title | AN EVALUATION OF REMOTE VIEWING: RESEARCH AND APPLICATIONS |
| prepared by | THE AMERICAN INSTITUTES FOR RESEARCH |
| authors | MICHAEL D. MUMFORD, PHD; ANDREW M. ROSE, PHD; DAVID A. GOSLIN, PHD |
| date | SEPTEMBER 29, 1995 |
| document number | CIA-RDP96-00791R000200180006-4 |

**Utts and Hyman are the two expert reviewers, not the report's authors.** The table of
contents puts them in Chapter Three: "Review 1 (Dr. Jessica Utts)" at 3-2, "Review 2 (Ray
Hyman)" at 3-43, "The Reply (Dr. Jessica Utts)" at 3-79. The triage row's "one of two named
assessors" is right in substance and the distinction is worth keeping in the claim text.

**The sentence the node already quotes verifies**, across a page break in the Executive
Summary. Two things did **not** verify against this file and should not be inferred from it:

| item the node carries | what the opened file shows |
|---|---|
| the Hyman phrase "the overwhelming amount of data generated by the viewers is vague, general, and way off target" | Not found anywhere in the OCR full text. It is not sourced to the AIR evaluation in the node's claims, only in the narrative, and it should stay out of any claim until it is opened in Hyman's own review |
| "the roughly $20 million programme" | No dollar figure was found in this file. The node sources that to the AIR evaluation nowhere, and it should not be moved onto this document |

Access note: `cia.gov/readingroom` did **not** reach on 2 September 2026. Both the document
page and the PDF answer HTTP 302 to `https://www.cia.gov/readingroom` in an unbounded loop, to
curl with a cookie jar and to WebFetch alike. The archive.org mirror of the reading room is the
route that worked, and it is the same technique agent 3 used on the Brown FBI file.

```json
{
 "id": "stargate-program",
 "cls": "event",
 "claims": [
  {"tier": 1, "text": "The 1995 evaluation that closed the programme is titled 'AN EVALUATION OF REMOTE VIEWING: RESEARCH AND APPLICATIONS', was prepared by the American Institutes for Research and is dated September 29, 1995; it is released as CIA-RDP96-00791R000200180006-4. Its authors are Michael D. Mumford, Andrew M. Rose and David A. Goslin. Jessica Utts and Ray Hyman are the two expert reviewers rather than authors: Chapter Three carries 'Review 1 (Dr. Jessica Utts)', 'Review 2 (Ray Hyman)' and 'The Reply (Dr. Jessica Utts)'.", "source": "American Institutes for Research, 'An Evaluation of Remote Viewing: Research and Applications', 29 September 1995, CIA-RDP96-00791R000200180006-4, title page and table of contents https://archive.org/download/cia-readingroom-document-cia-rdp96-00791r000200180006-4/cia-rdp96-00791r000200180006-4_djvu.txt"},
  {"tier": 1, "text": "The report's Executive Summary states: 'Most importantly, the information provided by remote viewing is vague and ambiguous, making it difficult, if not impossible, for the technique to yield information of sufficient quality and accuracy for actionable intelligence.' It adds that in no case had the information provided ever been used to guide intelligence operations, and concludes that 'continued use of remote viewing in intelligence gathering operations is not warranted.'", "source": "American Institutes for Research, 'An Evaluation of Remote Viewing: Research and Applications', 29 September 1995, CIA-RDP96-00791R000200180006-4, Executive Summary pages E-4 to E-5 https://archive.org/download/cia-readingroom-document-cia-rdp96-00791r000200180006-4/cia-rdp96-00791r000200180006-4_djvu.txt"}
 ],
 "sources": [
  {"name": "American Institutes for Research, 'An Evaluation of Remote Viewing: Research and Applications', 29 September 1995, CIA-RDP96-00791R000200180006-4, full text via the archive.org mirror of the CIA reading room", "url": "https://archive.org/download/cia-readingroom-document-cia-rdp96-00791r000200180006-4/cia-rdp96-00791r000200180006-4_djvu.txt", "date": "2026-09-02"}
 ]
}
```

No `desc` replacement is proposed. The node's third claim, currently sourced to "American
Institutes for Research evaluation, 1995" with no URL, is superseded in content by the second
claim above and could be retired rather than kept alongside it. That is Stewart's call, not
mine, and it is a deletion rather than an addition so it is not drafted here.

---

## 2. `william-mccasland`, the SAPOC placement (triage-5 C2 row 6) - ATTRIBUTE, and the row's attribution is wrong

The row reads: "Against that, Burlison places him on SAPOC and at AFRL and details the REI
medical kit and absent ring-camera footage." I re-read both passages. **Burlison does not make
the SAPOC claim in either of them.** Michels does, and in the episode where Burlison is the
guest he hedges it.

| what the row says | what the transcript says |
|---|---|
| Burlison places McCasland on the Special Access Program Oversight Committee | At 1:28:33 in the 2 July 2026 Burlison episode it is **Michels** who says it, hedged: "I believe he was on the special access program oversight committee which Lou was as well." Burlison's reply does not take up the placement. In the 9 July 2026 Shermer episode, at 1:15:12, it is again **Michels**, this time unhedged |
| Burlison details the absent ring-camera footage | Michels raises the ring cameras, in both episodes (2 July 1:30:24; 9 July 1:16:50) |
| Burlison flags his own uncertainty on the gun | Correct, and it is a correction rather than a flag: "Well they don't know that he took a gun... Maybe missing. It's not confirmed." He is correcting Michels' "he leaves everything but it takes a gun" |
| Burlison details the REI medical kit | Correct. "the latest information is he went to REI and purchased a medical kit" |
| Corbell "says flatly there is no such general" | **He does not.** He says the DeLonge contact "was an op", and the caption "because no general like that" is the head of an argument about what a general of that generation would do, not a denial of the man's existence. Corbell says of him in the same breath: "he's fucking missing right now" |

**Therefore: do not add a SAPOC claim to `william-mccasland`.** The board carries none today,
and the corpus does not supply one. What the corpus supplies is a podcast host's assertion,
hedged once, repeated once, in front of two guests neither of whom adopts it.

What is worth carrying is the reverse: the three declines, and Burlison's own on-record
account of his contact attempts, which is narrower and more checkable than the row suggests.
Read at 2:14:52 in
`dist/transcripts/md/2026-05-28 i-saw-a-mantis-alien-at-this-american-military-base-army-sergeant-lyn.md`,
1:56:41 in
`dist/transcripts/md/2026-06-07 if-you-knew-what-i-knew-jeremy-corbell-unleashes-on-jesse-michels-earl.md`,
1:14:21 to 1:20:51 in
`dist/transcripts/md/2026-07-09 i-debated-ufos-with-americas-top-skeptic-it-got-ugly.md`,
and 1:28:33 to 1:31:18 in
`dist/transcripts/md/2026-07-02 congressman-president-trump-was-briefed-on-alien-hybrids.md`.

```json
{
 "id": "william-mccasland",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 2 July 2026, Rep. Eric Burlison said of McCasland that 'I know he was on my list of people to talk to', that David Grusch had sent someone to interview him without getting much out of him, and that in Burlison's view McCasland knew inquiries were being made. Asked about a missing firearm Burlison corrected the host: 'they don't know that he took a gun... Maybe missing. It's not confirmed.' He said the latest information was that McCasland had bought a medical kit at REI (1:28:33 to 1:31:18).", "source": "American Alchemy with Jesse Michels, 'Congressman: \"President Trump Was Briefed On Alien Hybrids!\"', 2 July 2026, 1:28:33 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3"},
  {"tier": 2, "text": "The claim that McCasland sat on a Special Access Program Oversight Committee and ran the Air Force Research Laboratory at Wright-Patterson is made in this corpus by Michels, not by any guest: hedged as 'I believe he was on the special access program oversight committee' to Rep. Burlison on 2 July 2026 (1:28:33), and stated flatly to Michael Shermer on 9 July 2026 (1:15:12). Neither guest adopts it.", "source": "American Alchemy with Jesse Michels, 'Congressman: \"President Trump Was Briefed On Alien Hybrids!\"', 2 July 2026, 1:28:33 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3"},
  {"tier": 2, "text": "Three speakers in the same corpus decline to corroborate. Asked directly by Michels on 28 May 2026 whether he had come across 'General William Neil McCaslin', former Army remote viewer Lyn Buchanan answered 'No', and to the follow-up naming Wright-Patterson, 'No, I didn't know that' (2:14:52). On 7 June 2026 Jeremy Corbell characterised the reported McCasland-to-Tom DeLonge contact as an operation, saying 'I said it's part of an op', while acknowledging that McCasland is missing (1:56:41 to 1:59:32). On 9 July 2026 Michael Shermer argued the disappearance against base rates, asking 'How many people go missing? It's thousands' and 'why aren't all the heads of all the nuclear sites or the generals... all going missing', while conceding it 'should be investigated. Obviously' by the family, local police or the FBI (1:14:21 to 1:20:51).", "source": "American Alchemy with Jesse Michels: '\"I Saw a Mantis Alien At THIS American Military Base!\" -Army Sergeant Lyn Buchanan', 28 May 2026, 2:14:52 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6048917608.mp3 ; '\"If You Knew What I Knew!\" -Jeremy Corbell UNLEASHES On Jesse Michels | EARLY RELEASE', 7 June 2026, 1:56:41 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1864048266.mp3 ; 'I Debated UFOs With America's Top Skeptic (It Got Ugly...)', 9 July 2026, 1:14:21 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL4216664886.mp3"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Congressman: \"President Trump Was Briefed On Alien Hybrids!\"', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3", "date": "2026-07-02"},
  {"name": "American Alchemy with Jesse Michels, '\"I Saw a Mantis Alien At THIS American Military Base!\" -Army Sergeant Lyn Buchanan', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6048917608.mp3", "date": "2026-05-28"},
  {"name": "American Alchemy with Jesse Michels, '\"If You Knew What I Knew!\" -Jeremy Corbell UNLEASHES On Jesse Michels | EARLY RELEASE', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1864048266.mp3", "date": "2026-06-07"},
  {"name": "American Alchemy with Jesse Michels, 'I Debated UFOs With America's Top Skeptic (It Got Ugly...)', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL4216664886.mp3", "date": "2026-07-09"}
 ]
}
```

**One item deliberately not drafted.** Two speakers, Shermer at 1:16:02 and Burlison at
1:31:18, describe McCasland's wife as having said before or during the 911 call that he was
unwell or had been depressed. That is an unverified statement about a missing man's health,
relayed second hand through machine captions, and it would sit on the board as a Tier 2 claim
about a private person's medical state. It belongs in a Bernalillo County Sheriff's Office or
911 record if it belongs anywhere. **Do not carry it off a podcast.**

---

## 3. `sean-kirkpatrick` (triage-5 C2 row 2) - ATTRIBUTE

The board carries Kirkpatrick across six research files and none of them carries the denial
this rebuts: there is no claim on the board that he had no pre-2022 UAP involvement, and
"Fugal" appears in `data/the-program.json` only as the 2016 purchaser of Skinwalker Ranch. So
this is not a correction to something the board says; it is a dated, first-hand counter to a
public denial the board is silent on, and it names an artifact that exists or does not.

The value is entirely in the specificity: April 2018, two and a half hours, a keynote
presentation with video, and a photograph Fugal says he posted to four platforms. Read at
2:39:07 to 2:41:12 in
`dist/transcripts/md/2026-07-26 theres-a-ufo-under-the-ranch-skinwalker-owner-breaks-silence.md`.

```json
{
 "id": "sean-kirkpatrick",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 26 July 2026, Skinwalker Ranch owner Brandon Fugal said that Kirkpatrick 'claimed that before 2022 he had no interest in these topics, that he'd never attended a briefing on Skinwalker Ranch', and that he had never met Fugal. Fugal said Kirkpatrick sat across from him for two and a half hours at a confidential briefing in April 2018 devoted to the investigation and findings at the ranch, and that after being challenged by Steven Greenstreet of the New York Post he published a photograph of Kirkpatrick in attendance to Twitter, LinkedIn, Instagram and Facebook (2:39:07 to 2:41:12).", "source": "American Alchemy with Jesse Michels, '\"There's A UFO Under the Ranch!\" - Skinwalker Owner Breaks Silence', 26 July 2026, 2:39:07 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9910649891.mp3"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, '\"There's A UFO Under the Ranch!\" - Skinwalker Owner Breaks Silence', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9910649891.mp3", "date": "2026-07-26"}
 ]
}
```

The photograph itself was **not** opened. Fugal names four platforms and no post; a later pass
that finds the post can upgrade this to Tier 1 on the image and its date, and that is the only
thing that would move it. Until then the claim states what he said, not that the briefing
happened. The Kirkpatrick denial it answers is likewise not opened here and is carried only as
Fugal's characterisation of it.

---

## 4. `italo-venturelli` (triage-4 C6) - ATTRIBUTE, with a hard caution

**The caption warning is confirmed and it is stronger than agent 3's carry-forward states.**
The phrase "Vargem Grande do Sul" appears **nowhere in the transcript**. It is the batch-17
mapper's own reconstruction, recorded in that file as `[PHON? caption varies Vajian, Vajina,
Vajigin, Virginia]`. The words "Varginha" and "Vargem" do not occur in the episode at all. So
there is no second location in the source to mistake for one, and **no location node may be
created from this row.**

The material itself is real and the board carries none of it: "Chereze" is zero occurrences in
`data/the-program.json`, and the `italo-venturelli` node's chronology stops at the January 2026
Capitol Hill briefing. Batch 17 file 4 adds a second physician, a second procedure and a
pending court application.

**What cannot be carried, and why.** Every proper noun in the passage is destroyed. The soldier
is rendered "Makshet Izi", "Marc Guilicheriz", "Marco Chirreci", "Marco Iliche Nese", "Elie
Shirdiz" and "Marco Chirreisi" within seven minutes. The pathologist who wrote the tissue
report is rendered only as "Dódo Jainini" and "Torontonubacistamaku Guginini", which is not
reconstructible. Minas Gerais is "Minajir Ais" and "minigetized". **No name from this passage
may reach the board**, and the claim below therefore names roles rather than people except for
Fortunato himself, who is named in the episode's own guest billing. Read at 3:09:19 to 3:15:48
in
`dist/transcripts/md/2026-01-31 i-spent-4-minutes-with-a-living-alien-top-neurosurgeon-exclusive-inter.md`.

```json
{
 "id": "italo-venturelli",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 31 January 2026, forensic physician Dr Armando Fortunato said he performed the autopsy on the state military police soldier whose death followed the 1996 Varginha events, that the body arrived with no mention of extraterrestrial contact and was referred by the commanding colonel as a possible professional-error inquiry, and that the only lesion found was a drainage incision in the left armpit. He said tissue and blood samples went to a pathologist whose report gave death as a pulmonary infection causing septicaemia. Fortunato's stated position is that 'the first diagnostic hypothesis is still a secondary effect of surgery', with post-contact contamination a second hypothesis that 'shouldn't be ruled out' (3:09:19 to 3:15:48).", "source": "American Alchemy with Jesse Michels, '\"I Spent 4 Minutes With A Living Alien!\" -Top Neurosurgeon [Exclusive Interview]', 31 January 2026, 3:09:19 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL5466696236.mp3?updated=1769887132"},
  {"tier": 2, "text": "In the same passage Fortunato said the pathologist has recently stated that the bacteria found was not common in Brazil and extremely virulent, and is now applying to the court for authorisation to exhume the soldier's remains for DNA testing, which Fortunato said requires both the court's approval and the family's agreement. No case number, court or filing date is given (3:12:14 to 3:13:06).", "source": "American Alchemy with Jesse Michels, '\"I Spent 4 Minutes With A Living Alien!\" -Top Neurosurgeon [Exclusive Interview]', 31 January 2026, 3:12:14 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL5466696236.mp3?updated=1769887132"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, '\"I Spent 4 Minutes With A Living Alien!\" -Top Neurosurgeon [Exclusive Interview]', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL5466696236.mp3?updated=1769887132", "date": "2026-01-31"}
 ]
}
```

The claim says "the state military police soldier" rather than a name because the board's
`hospital-regional-varginha` and `italo-venturelli` records do not carry the soldier at all,
and this transcript cannot supply the spelling. A pass that opens the Brazilian record can add
the name and the exhumation docket in one move; both belong to the same search.

The row's second half, the CIA exemption response to James Fox's FOIA for USAF Campinas flight
records (batch 16, file 4, 1:24:27), is **not drafted**. Fox describes a forwarding and an
exemption citing a "1949" secrecy provision, with no case number, no date and no statute number
given. That is a FOIA-log entry for `notes/REQUEST-QUEUE.md`, not a claim, and the tempting
identification of the 1949 statute is exactly the inference `CLAUDE.md` section 2 forbids
without the letter in hand.

---

## 5. `tim-gallaudet` (triage-5 C2 row 9) - NO ACTION, false ABSENT

The row says he "sits on a UAP Science Advisory Council that reports to ODNI, not to the White
House". The transcript supports the first half: at 0:30:56 in
`dist/transcripts/md/2026-08-24 top-navy-admiral-the-ocean-is-full-of-ufos.md` he says "the
uap science advisory council that i'm on now that reports to the od and i". There is no
correction of the host in the passage; he simply states it.

**The board already carries the council and carries it more precisely.**
`data/the-program.json` records that on 22 June 2026 ODNI, with FBI support, announced a UAP
Science Advisory Council led by Avi Loeb and reporting to an interagency UAP Governance Board,
formed at the request of the White House in coordination with AARO, ODNI and the FBI, and it
names Gallaudet as one of the members. Gallaudet's on-air phrase is the looser statement of
what the board already has, and adopting it would blur a governance structure the board states
correctly. Nothing is drafted.

The row's second half, the Bluegill Triple Prime deck logs, is **deliberately not touched**.
`CLAUDE.md` section 9 records Bluegill's date and contents as already contradicted by the
opened record and instructs that the node must not be moved toward the podcast. That
instruction is followed here.

---

## 6. `battelle` (triage-5 C2 row 3) - NO ACTION, NOT OPENED

The row correctly identifies the 2020 Battelle release as a document to open rather than an
attribution. It could not be opened from this machine. `battelle.org` answers HTTP 403 with a
Cloudflare "Attention Required" interstitial to curl with a full browser user agent, and
WebFetch receives the same 403. A bot wall is a NOT OPENED, not a guess, and no claim is
drafted from the search-result snippet describing the release.

The press-release path for a later pass, which was found but not opened, is
`https://www.battelle.org/insights/newsroom/press-release-details/battelle-neuro-team-advances-to-phase-ii-of-darpa-n3-program`.
Whatever a later pass opens must be the release itself.

---

## NOT REACHED

| Row | Node | What remains |
|---|---|---|
| 5.C2 r5 | `dylan-borland`, `jon-kosloski` | The unsigned Memorandum for Record allegation and the original-classification-authority argument. Transcript not re-read |
| 5.C2 r7 | `glenn-gaffney`, `george-knapp`, `bigelow-aerospace` | Agent 3 adjudicated the 2008/2010 blocking at 4.C9 as NO ACTION. Burlison naming Gaffney his top subpoena target is a separate, checkable item and is not adjudicated |
| 5.C2 r8 | `l-skinwalker`, `skinwalkers-at-the-pentagon` | Travis Taylor's concurrent UAP Task Force role. Not re-read |
| 5.C2 r11 | `salvatore-pais` | Burlison's in-person account near Pax River with AARO's director present. Not re-read |
| 5.C2 r12 | `eric-burlison` | The FFRDC letter campaign beyond MITRE, to Aerospace Corporation, RAND and IDA. Not re-read |
| 5.C2 r13 | `thomas-townsend-brown` | The Teller-to-Odlum introduction and the Stevenson telegram. Agent 3 also left these unopened; they remain the two sub-items of that node nobody has reached |

---

## Access notes from this pass

To add to the reach facts in `VERIFY-BRIEF-2026-09-02.md` and to agent 3's list:

- **`cia.gov/readingroom` does not reach, 2 September 2026.** Both
  `/readingroom/docs/<DOCNUM>.pdf` and `/readingroom/document/<docnum>` answer HTTP 302 to
  `https://www.cia.gov/readingroom` and loop. curl with a cookie jar and a browser user agent
  gets the same loop; WebFetch reports "Too many redirects". The brief's line that the CIA
  reading room answers WebFetch is stale as of today.
- **The archive.org mirror of the reading room is the working route.** Items are named
  `cia-readingroom-document-<docnum lowercased>`, and
  `https://archive.org/download/<item>/<docnum lowercased>_djvu.txt` returns the OCR full text
  to plain curl. That is how the 434KB AIR report above was read. `archive.org/metadata/<item>`
  confirms an item exists before you fetch it. `archive.org/advancedsearch.php` with
  `output=json` finds items by title.
- **`battelle.org` is behind a Cloudflare bot wall** to both curl and WebFetch.
- OCR is not a source. Two phrases the `stargate-program` narrative carries were absent from
  the OCR text and are reported above as not found rather than as absent from the document.
