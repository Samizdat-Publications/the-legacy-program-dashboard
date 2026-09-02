# Section C verification, agent 1 (Michels corpus, 2 September 2026)

**Written:** 2 September 2026, against `research/leads/VERIFY-C-BRIEF-2026-09-02.md`.
**Rows held:** all of section C of `research/leads/michels-triage-1.md` (11 rows), and
section C1 of `research/leads/michels-triage-3.md` (25 rows).
**Nothing below has been added to the board.** Every draft is an additive
`_corrections.json` record for Stewart to accept or refuse. No `research/*.json`,
`tools/`, `data/` or `dist/` file was touched and no git command was run.

**What was actually opened.** Eight episode transcripts in `dist/transcripts/md/`, each
read at the timestamp the triage row names, plus its header for the audio URL. Node
records were loaded out of `research/*.json` by id before any verdict. **No external
document was opened in this pass**, so there is no RECORD verdict here: every actionable
row resolved to "a named person said this on this show", which is the ATTRIBUTE case.
That is a real result rather than a shortfall, but it does mean nothing here upgrades
past Tier 2.

**Six nodes appear in both triage files** (`thomas-townsend-brown`, `robert-sarbacher`,
`eric-wang`, `edward-condon`, `lincoln-lapaz`, `jon-kosloski`). Each is handled once,
under a single heading, and the heading says which two rows it answers.

**One triage row is wrong on its face and the correction travels with it.** The
`thomas-townsend-brown` row asserts that "Northrop Grumman is said to have paid him a
small retainer for life". The token `retainer` occurs exactly once in the whole 141-file
transcript corpus, in an unrelated 2024 Danny Sheehan episode about CIA counsel. What the
corpus carries at the pointers the row gives is a 1968 Northrop paper. The retainer claim
is not drafted below and should not be carried.

---

## Summary

| Node id | Verdict | One-line reason |
|---|---|---|
| `thomas-townsend-brown` | ATTRIBUTE | Michels names Gunston, *Air International*, 2000 as the B-2 source, and Guidance Technologies; the node names neither. The Northrop retainer is not in the corpus |
| `robert-sarbacher` | ATTRIBUTE | Michels, attributing to Grusch, puts Sarbacher with Oppenheimer behind the 1954 AEC secrecy overlay; the node adjudicates only the 1983 letter |
| `eric-wang` | ATTRIBUTE | Pines names William Steinman's Aztec book as the sole source of the Wright-Patterson story, and flags the Kissinger read as his own inference |
| `robert-hastings` | ATTRIBUTE | The node says "over 150"; the corpus carries 167, "almost 200", "170 total", and a correction from Hastings himself to 12 to 15 radar operators |
| `pais-app-superconductor` | NO ACTION | The row says so itself: the board carries the file wrapper in more detail than the transcript. Lakhno was not opened |
| `edward-condon` | ATTRIBUTE | Two speakers, two episodes: the McMahon Act authorship and Hippler memo, and the Hoover letter and clearance sequence. Neither name is on the board |
| `david-grusch` | ATTRIBUTE | Davis separates three harassment events with three different actors in one breath; the node carries none of them |
| `glenn-gaffney` | ATTRIBUTE | Davis gives Gaffney a title and a second blocked transfer the node does not have |
| `kirk-mcconnell` | ATTRIBUTE | Hastings names him as the person who brokered AARO's 2023 interviews of 11 veterans; the node's chronology stops at his retirement |
| `jon-kosloski` | NO ACTION | Caption corruption only. The brief classes this as at most a note |
| `lincoln-lapaz` (triage-1 row) | NO ACTION | "Dan Wilson" is not fixable from a caption; the row itself declines to promote it |
| `malmstrom-echo-flight-1967` | ATTRIBUTE | Four triage-3 rows, one episode. The Boeing bench-test result is the strongest thing in the passage and the node has none of it |
| `robert-low` | ATTRIBUTE | Salas says he holds a handwritten Low note recording the EMP explanation; the node carries only the 1966 trick memo |
| `condon-committee` | ATTRIBUTE | Salas reads from the 19 October 1967 Craig interview of Chase; the node has the report, not the interview |
| `robert-salas` | ATTRIBUTE | The 1996 Meiwald call is the artefact that explains the Echo/Oscar discrepancy the node already notes |
| triage-3 C2 (26 rows) | NO ACTION | Spot-checked; they are false ABSENT rows as the file says. See the NO ACTION table |

Counts: **12 ATTRIBUTE**, **4 NO ACTION** (three named rows plus the C2 block), **0 RECORD**.

---

## `thomas-townsend-brown` (triage-1 C row 1)

Opened: "Did Oppenheimer Work on UFOs?", 19 October 2024, at 0:24:12 and 0:27:32;
"Navy Fighter Pilots Witness UFO Mid Flight (Ft. Ryan Graves)", 6 December 2024, at
0:29:08; "CIA Contractor: 'Obama Received An Alien Prophecy' (ft. Bob McGwire)",
14 December 2024, at 0:52:55. The McGwire Rickover passage is at 0:52:55, not the
1:16:58 the triage row gives; 1:16:58 in that file is a hypergraph digression.

The node's whole argument is that none of the five patents claims gravity control, and it
is right. What it does not do is name whose claim the B-2 story is. Michels names him:
Bill Gunston, writing in *Air International* in 2000. That is a dated, published,
attributable source for a claim the board otherwise refuses anonymously, which is exactly
the case the brief describes. Gunston is also quoted on air saying he had no wish to
reside in the Tower of London, which tells a reader the character of the source.

Not drafted: the Northrop lifetime retainer (not in the corpus, see above); the 1943 FBI
document said to call Brown the Navy's top radar expert (no identifier given on air, so
there is nothing to open).

```json
{
 "id": "thomas-townsend-brown",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 19 October 2024, Michels said at 0:27:32 that the British aerospace journalist Bill Gunston, writing in Air International magazine in 2000, stated he was very sure Brown's work made it into the B-2 stealth bomber, and that Gunston added he had no wish to reside in the Tower of London. This is the named, dated source for the B-2 attribution the board otherwise carries without an author.", "source": "American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:27:32, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004"},
  {"tier": 2, "text": "In the same episode at 0:24:12 Michels named Brown's Santa Monica operation of the 1950s as 'guidance technologies' and placed Bill Lear's office across the street from it. Neither the operation's name nor the Santa Monica location appears in the board's record of Brown.", "source": "American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:24:12, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004"},
  {"tier": 2, "text": "Two speakers on separate episodes tell the same Rickover anecdote. On 6 December 2024 at 0:29:08 Michels, citing the writer Paul LaViolette, said Brown went to Hyman Rickover and Rickover told him to stop wasting his time. On 14 December 2024 at 0:52:55 Bob McGwire gave the same story with Rickover answering 'don't waste your time. We're already on it.' Neither speaker cites a document.", "source": "American Alchemy with Jesse Michels, 'Navy Fighter Pilots Witness UFO Mid Flight (Ft. Ryan Graves)', 6 December 2024, 0:29:08, and 'CIA Contractor: Obama Received An Alien Prophecy (ft. Bob McGwire)', 14 December 2024, 0:52:55"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004", "date": "2024-10-19"},
  {"name": "American Alchemy with Jesse Michels, 'Navy Fighter Pilots Witness UFO Mid Flight (Ft. Ryan Graves)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE5314927973.mp3?updated=1752173951", "date": "2024-12-06"},
  {"name": "American Alchemy with Jesse Michels, 'CIA Contractor: Obama Received An Alien Prophecy (ft. Bob McGwire)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE8690011428.mp3?updated=1752173727", "date": "2024-12-14"}
 ]
}
```

---

## `robert-sarbacher` (triage-1 C row 2; triage-3 C1 row on the 1987 letters)

Opened: "Did Oppenheimer Work on UFOs?", 19 October 2024, at 0:33:16.

The node adjudicates the 29 November 1983 Steinman letter carefully and rules out the
Wright Field meeting. The AEC-1954 attribution is a different claim about a different
year, and the node does not address it, which leaves a reader who has heard the podcast
with no way to see that the board has considered it. It is drafted as what it is: Michels
relaying Grusch.

**Not reached within this row:** the Graves rendering at batch 03 (the "Harvard Undersea
Observatory" detail) and the 1987 letters to Steinman at batch 14. Both need episodes I
did not open. They stay open.

```json
{
 "id": "robert-sarbacher",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 19 October 2024, at 0:33:16, Michels said that David Grusch identifies the people who set up the secrecy protocols for UFOs as Robert J. Oppenheimer and Sarbacher, and that the two are 'responsible for the 1954 Atomic Energy Commission which overlaid nuclear secrecy on top of UFO secrecy'. The claim is Michels relaying Grusch, it concerns 1954 rather than the period the 1983 letter covers, and no document is cited for it on air.", "source": "American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:33:16, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004", "date": "2024-10-19"}
 ]
}
```

---

## `eric-wang` (triage-1 C row 3 and triage-3 C1 row, together)

Opened: "Matthew Pines: Anti-Gravity Tech & Inter-Dimensional Aliens", 15 November 2024,
at 2:46:17 and 2:47:06.

Both triage files say the same thing from different corpora and both are right: the node's
caution is correct and now has a named single source. Pines says on air that he read a
book by "a UFO researcher, William Steinman, about the Aztec Crash in 1948", that the book
names "Eric Henry Wang" as head of special projects at Wright-Patterson who came over with
Operation Paperclip, and that Steinman writes he could get nothing on him. Pines then reads
Steinman's "H-A-K" as Henry A. Kissinger and says plainly that this is his own inference.
The node's job here is to say whose story it declines, and to record that the Kissinger
link rests on a listener's reading of two initials.

```json
{
 "id": "eric-wang",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 15 November 2024, at 2:46:17, Matthew Pines named the source of the Wright-Patterson story about Wang: a book by the UFO researcher William Steinman on the 1948 Aztec crash, which Pines says describes 'Eric Henry Wang' as head of special projects at Wright-Patterson who came over with Operation Paperclip. This identifies the single secondhand source behind the story the board's existing caution declines.", "source": "American Alchemy with Jesse Michels, 'Matthew Pines: Anti-Gravity Tech & Inter-Dimensional Aliens', 15 November 2024, 2:46:17, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4097453442.mp3?updated=1751923843"},
  {"tier": 2, "text": "At 2:47:06 in the same episode Pines said Steinman's text refers to Wang's boss only as 'H-A-K', and that he himself concluded 'oh, Henry A. Kissinger'. Pines states the identification as his own inference from the initials, not as something Steinman wrote. Any Wang-to-Kissinger link would rest on that inference and on nothing else.", "source": "American Alchemy with Jesse Michels, 'Matthew Pines: Anti-Gravity Tech & Inter-Dimensional Aliens', 15 November 2024, 2:47:06, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4097453442.mp3?updated=1751923843"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Matthew Pines: Anti-Gravity Tech & Inter-Dimensional Aliens' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4097453442.mp3?updated=1751923843", "date": "2024-11-15"}
 ]
}
```

---

## `robert-hastings` (triage-1 C row 4)

Opened: "Did Oppenheimer Work on UFOs?", 19 October 2024, at 0:34:57; "UFOs Are
Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)", 24 December 2024, at 2:07:40;
"UFO Believer vs. UFO Skeptic" (ft. Mick West and Marik von Rennenkampff), 27 January
2025, at 3:07:08.

The triage row is right that the instability is the finding. The node says "over 150
military veterans". Across three episodes in fifteen weeks the same host says 167, then
"almost 200", then that he had overstated it and that Hastings corrected him by email. The
correction is the valuable half, because it is not a smaller number, it is a different
population: most of the witnesses are ICBM security personnel, not radar operators.

```json
{
 "id": "robert-hastings",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 19 October 2024, at 0:34:57, Michels gave Hastings's figure as '167 UFO sighting cases at nuclear bases', and in the same breath as '167 ICBM security personnel, radar operators, people who work at these nuclear sites'. On 24 December 2024 at 2:07:40, with Hastings present, he described the same body of testimony as 'almost 200 stand-up patriots'.", "source": "American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:34:57, and 'UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)', 24 December 2024, 2:07:40"},
  {"tier": 2, "text": "On the same show on 27 January 2025 at 3:07:08 Michels said he had overstated the case and that Hastings emailed him a correction: 'it was only like 12 to 15. I don't remember the exact number. But radar operators, the rest were ICBM security personnel'. In the same passage he gives the overall total as 170. The correction concerns the composition of the witness population, not only its size.", "source": "American Alchemy with Jesse Michels, 'UFO Believer vs. UFO Skeptic: Are Aliens Visiting Earth?' (ft. Mick West and Marik von Rennenkampff), 27 January 2025, 3:07:08, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE9180015195.mp3?updated=1738087523"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004", "date": "2024-10-19"},
  {"name": "American Alchemy with Jesse Michels, 'UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4049919963.mp3?updated=1752173281", "date": "2024-12-24"},
  {"name": "American Alchemy with Jesse Michels, 'UFO Believer vs. UFO Skeptic: Are Aliens Visiting Earth?' (ft. Mick West and Marik von Rennenkampff) (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE9180015195.mp3?updated=1738087523", "date": "2025-01-27"}
 ]
}
```

---

## `edward-condon` (triage-1 C row 6 and triage-3 C1 row, together)

Opened: "Did Oppenheimer Work on UFOs?", 19 October 2024, at 0:39:03 and 0:39:52;
"Air Force Officer: 'A UFO Shut Down 10 Nukes in Seconds...' (ft. Bob Salas)",
12 July 2025, at 1:07:14, 1:08:25 and 1:09:15 to 1:10:08.

Two speakers, two years apart, on two different biographical threads, and neither
"McMahon" nor "Hippler" nor "Hoover" appears in the node. The Hippler memo is the same
document the `robert-low` row below reaches from the other side, which is worth saying in
the record: one memo, two witnesses, two episodes, and nobody has produced it.

**One correction to the triage-3 paraphrase.** That row says Salas describes "the Groves
clash six weeks into the Manhattan Project". He does not. At 1:08:25 he says only that
Condon "was asked to resign for the Manhattan Project because of some security issue" and
adds "I don't know the details of that". Groves is not named. The claim below says what
was said.

```json
{
 "id": "edward-condon",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 19 October 2024, at 0:39:03, Michels said Condon 'wrote the McMahon Secrecy Act of 1946, which is the precursor to the Atomic Energy Act of 1954'. The authorship attribution is the speaker's own and is offered without a citation. Neither the McMahon Act nor an authorship claim about it is on this board.", "source": "American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:39:03, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004"},
  {"tier": 2, "text": "At 0:39:52 in the same episode Michels said Condon was 'in close coordination with Air Force kernels like Robert Hippler', and that a written memo exists in which Hippler tells Condon to show that UFO research was a waste of money. On 12 July 2025 at 0:37:53 Robert Salas independently described letters between an Air Force colonel, rendered by the caption as 'Robert Hitler', and Condon to the same effect. Two speakers, two episodes, one alleged memo, which neither of them produces.", "source": "American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:39:52, and 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:37:53"},
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 12 July 2025, at 1:07:14 and 1:08:25, Robert Salas said that in 1949 J. Edgar Hoover wrote a letter to Congress identifying Condon as, in Salas's own paraphrase, nothing less than a Russian spy; that he holds a copy; that Condon had earlier been asked to resign from the Manhattan Project over an unspecified security issue; and, at 1:09:15 to 1:10:08, that Lewis Branscomb urged Condon in about 1966 to take the Air Force UFO study as a route back to a security clearance. Salas twice says he does not know the details.", "source": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 1:07:14 to 1:10:08, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004", "date": "2024-10-19"},
  {"name": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599", "date": "2025-07-12"}
 ]
}
```

---

## `david-grusch` (triage-1 C row 7)

Opened: "CIA Scientist: 'George Bush Was Briefed on UFOs' (ft. Eric Davis)",
13 December 2024, at 0:07:12 and 0:08:08.

The lead map's warning is the value of the row. Davis names three separate events in one
sentence and they have three different actors: a person in the NRO, unknown people at
Grusch's home and vehicles, and whoever accessed his medical file. Merged into one
"harassment" claim, the board would lose the only institutional name in the set.

```json
{
 "id": "david-grusch",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 13 December 2024, at 0:07:12, Eric Davis described three separate acts against Grusch after his whistleblower complaint and before his testimony: he 'got harassed by, by someone in the National Reconnaissance Office', then 'got physically harassed at his home and in his vehicles by people unknown', then somebody leaked a PTSD episode from his private medical files. Davis names an institution only for the first. The three have three different actors and should not be merged.", "source": "American Alchemy with Jesse Michels, 'CIA Scientist: George Bush Was Briefed on UFOs (ft. Eric Davis)', 13 December 2024, 0:07:12 to 0:08:08, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7341687364.mp3?updated=1752173868"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'CIA Scientist: George Bush Was Briefed on UFOs (ft. Eric Davis)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7341687364.mp3?updated=1752173868", "date": "2024-12-13"}
 ]
}
```

---

## `glenn-gaffney` (triage-1 C row 8)

Opened: "CIA Scientist: 'George Bush Was Briefed on UFOs' (ft. Eric Davis)",
13 December 2024, at 0:19:28, 0:20:19 and 0:22:48.

The node is careful and says outright that it is "a research thread with a name attached,
not a finding". This adds a second, differently dated blocked transfer and a claimed
title, both from a named speaker who says in the same passage that he never dealt with
the man directly. The title is the checkable part and is the obvious next document to
open.

```json
{
 "id": "glenn-gaffney",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 13 December 2024, at 0:22:48, Eric Davis said of Gaffney 'I think his title was deputy director of the CIA over the directorate of science and technology. And that's where the UAP portfolio is held.' Davis hedges the title himself. No record opened in this pass establishes either the title or the portfolio placement.", "source": "American Alchemy with Jesse Michels, 'CIA Scientist: George Bush Was Briefed on UFOs (ft. Eric Davis)', 13 December 2024, 0:22:48, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7341687364.mp3?updated=1752173868"},
  {"tier": 2, "text": "At 0:19:28 and 0:20:19 in the same episode Davis said he had no direct interaction with Gaffney but that the aerospace defence firm involved, and that firm's senior and executive vice presidents, did; and that Gaffney was 'very antagonistic' about that company releasing to them, under DIA classification, a collection of crash retrieval materials held by Bigelow Aerospace Advanced Space Studies and EarthTech since the 1989 shutdown. This is a second blocked transfer, distinct from the Lockheed to Bigelow transfer the node already carries.", "source": "American Alchemy with Jesse Michels, 'CIA Scientist: George Bush Was Briefed on UFOs (ft. Eric Davis)', 13 December 2024, 0:19:28 to 0:20:19"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'CIA Scientist: George Bush Was Briefed on UFOs (ft. Eric Davis)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7341687364.mp3?updated=1752173868", "date": "2024-12-13"}
 ]
}
```

---

## `kirk-mcconnell` (triage-1 C row 9)

Opened: "UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)",
24 December 2024, at 1:49:10 and 1:51:51.

The node's chronology runs to his March 2024 retirement and his Sol Foundation work. This
is a specific operational role thirteen months before that retirement, told by the man on
the other end of the phone call, and it is the hinge of the "AARO as Condon Committee 2.0"
framing. The caption renders him "Kurt McConnell" throughout; the triage file already
flags that, and it is not a board defect.

```json
{
 "id": "kirk-mcconnell",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 24 December 2024, at 1:49:10, Robert Hastings said that in January 2023 McConnell, whom he describes as 'a retired Senate Armed Service Committee investigator', contacted him and asked him to gather veterans with experiences at nuclear weapons sites for AARO to interview, and at 1:51:51 that 'it was 11 of roughly 20 who agreed to speak' with the office. The transcript renders the name Kurt McConnell throughout.", "source": "American Alchemy with Jesse Michels, 'UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)', 24 December 2024, 1:49:10 and 1:51:51, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4049919963.mp3?updated=1752173281"},
  {"tier": 2, "text": "In the same passage Hastings said McConnell emailed him in about March 2023 saying he had driven a veteran to that veteran's AARO interview, and relayed what the veteran said he had told AARO's then director about where a particular film was held. Hastings gives the account at two removes and names no document.", "source": "American Alchemy with Jesse Michels, 'UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)', 24 December 2024, 1:49:10"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4049919963.mp3?updated=1752173281", "date": "2024-12-24"}
 ]
}
```

---

## `malmstrom-echo-flight-1967` (triage-3 C1, four rows, handled as one)

Opened: "Air Force Officer: 'A UFO Shut Down 10 Nukes in Seconds...' (ft. Bob Salas)",
12 July 2025, at 0:28:33, 0:39:39, 0:44:54, 0:45:48, 0:46:36 and 0:47:25.

All four triage-3 rows are the same episode and the same witness, so they are one record.
The triage file is right that the Boeing bench-test result is the strongest technical
material in the passage: on Salas's account the contractor could reproduce a single
shutdown by injected signal, could not reproduce ten within seconds, and could not explain
a path through triply shielded cable. That is an exclusion stated by the party paid to
find a prosaic explanation, and the node has none of it.

The Sylvania row at 12 / 2 / 0:32:01 was not reached and is under NOT REACHED; the triage
file itself routes it to its own section A row 5.

```json
{
 "id": "malmstrom-echo-flight-1967",
 "cls": "event",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 12 July 2025, at 0:28:33, Robert Salas said one of the documents received from the Air Force is a telex about the Echo Flight shutdown which names by name two individuals working for Boeing, in which SAC headquarters demanded a complete investigation and used the words 'this is of grave concern'. Salas says 'I've got that telex.' This is a different document from the 17 March 1967 Air Force teletype the board already cites.", "source": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:28:33, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599"},
  {"tier": 2, "text": "At 0:44:54 to 0:47:25 Salas described the Boeing bench-test result: an injected electrical signal of a given frequency, voltage and duration could make one guidance and control system shut down, but the testers 'had no idea on how that could be injected into this each missile separately within seconds'; the cable run was about eight to nine inches in diameter and 'triply shielded against EMI'; the report concluded an external signal caused the shutdowns while stating they could not explain how it got in; and Salas says he and James Klotz later reached the two named testers, who repeated that they could not explain it.", "source": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:44:54 to 0:47:25"},
  {"tier": 2, "text": "At 0:39:39 Salas said he and James Klotz checked with the Department of Energy, cognizant of nuclear testing in Nevada, and that 'There were no nuclear tests on March 16th or March 24th', which on his account removes the nuclear-EMP explanation on the government's own records. He names no document number for the check.", "source": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:39:39"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599", "date": "2025-07-12"}
 ]
}
```

---

## `robert-low` (triage-3 C1)

Opened: the same episode at 0:37:53, 0:38:48 and 0:42:21.

The triage row's reconstruction of the caption can be checked inside the transcript
itself: the same speaker uses "Hitler" for a serving Air Force colonel corresponding with
Condon about Blue Book, which is Hippler. The node carries Low's 9 August 1966 trick memo
and nothing else; this is a second Low artefact, held by a named living witness.

```json
{
 "id": "robert-low",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 12 July 2025, at 0:38:48 and 0:42:21, Robert Salas said he holds a handwritten note by Low recording that Low had spoken to the Air Force colonel the caption renders as 'Hitler', and that the colonel said the Air Force thought EMP from nuclear testing caused the Malmstrom shutdowns and that the matter was probably too highly classified for the Colorado project to look at. Salas says twice 'I've got it in writing'. The note is not published and was not opened here.", "source": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:38:48 and 0:42:21, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599", "date": "2025-07-12"}
 ]
}
```

---

## `condon-committee` (triage-3 C1)

Opened: the same episode at 0:33:36 and 0:34:29.

Salas reads on air from what he presents as the transcript of Roy Craig's interview of
Lt. Col. Lewis D. Chase, and gives it a date. The node carries the report and the contract
and not this interview, and the interview is where the denial happens.

```json
{
 "id": "condon-committee",
 "cls": "program",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 12 July 2025, at 0:33:36, Robert Salas read on air from what he presents as the Colorado project's own record: 'The following interview conducted by Roy Craig, was Lieutenant Colonel Lewis D. Chase, who is chief of the operations division at Malstrom Air Force Base, Montana. The interview is being conducted at Malmstrom on October 19, 1967.' Salas says Chase had earlier confirmed in writing that he coordinated on the UFO activity and then denied the connection to Craig in this interview.", "source": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:33:36 and 0:34:29, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599", "date": "2025-07-12"}
 ]
}
```

---

## `robert-salas` (triage-3 C1)

Opened: the same episode at 0:58:13.

The node already notes the Echo/Oscar discrepancy. This is Salas saying where the
correction came from and when, in his own voice, which turns a noted discrepancy into a
dated account of how it arose.

```json
{
 "id": "robert-salas",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 12 July 2025, at 0:58:13, Salas said he did not learn his own incident was at Oscar Flight rather than Echo Flight until 1996, when he reached his former commander Fred Meiwald, who told him 'we were not at Echo Flight. We were at Oscar flight'. Salas says he had spoken of the Echo Flight incident as his own because it was so similar to what he recalled. This is his own account of the discrepancy the board's node already records.", "source": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:58:13, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio)", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599", "date": "2025-07-12"}
 ]
}
```

---

## NO ACTION, with the reason

| Row | Reason |
|---|---|
| `pais-app-superconductor` (triage-1) | The triage row states it itself: the board carries the file wrapper in more detail than the transcript does, including the examiner by name. The only new name is Lakhno, and the Lakhno paper was not opened, so there is nothing to draft that would not be an assertion about a document nobody here has read |
| `jon-kosloski` (triage-1 and triage-3) | Both rows are caption corruption only, and both say so. The brief classes caption corruption as NO ACTION with at most a note. Recorded here so a later corpus pass does not build a duplicate node out of `John Colosky`, `Kozlowski`, `Lasky` or `John Kozlowski` |
| `lincoln-lapaz`, triage-1 row | "Dan Wilson" is too generic to reconstruct from a machine caption and the row itself declines to promote it. The separate triage-3 LaPaz row (Tombaugh, and the August 1954 *Aviation Week* reversal) is a genuine lead and is under NOT REACHED, not here |
| triage-3 section C2, 26 rows | Checked as the brief directs, looking only for a row that plainly is not a false ABSENT. None found. Every node id in the table was grepped against `research/*.json` and every one resolves. One row is worth Stewart's eye but is not a section C correction: the `FBI` row says there is no FBI institution node and calls that "a real gap". Confirmed, there is no `"id": "fbi"` anywhere in `research/*.json`. That is a section A question |

---

## NOT REACHED

Time, not judgement. Listed so the next pass does not re-derive what I did reach.

**Sub-items inside rows I did answer:**

- `robert-sarbacher`: the "Harvard Undersea Observatory" detail (batch 03) and the 1987
  letters to Steinman said to name Bush and von Neumann (batch 14). Different episodes.
- `edward-condon` and `robert-low`: nobody has opened the Hippler memo itself. Two
  witnesses now describe it from opposite ends and neither produces it. This is the best
  RECORD candidate left in my rows.
- `malmstrom-echo-flight-1967`: the Sylvania row at 12 / 2 / 0:32:01.
- `thomas-townsend-brown`: the Gunston *Air International* 2000 article. If it can be
  found and read, the ATTRIBUTE claim above becomes Tier 1 and the board stops attributing
  the B-2 story to a podcast.

**Whole triage-3 C1 rows not opened:** `susan-gough`, `eg-and-g`, `alfred-odonnell`,
`david-spergel` (flagged by the triage author as the strongest corroboration signal in
that group, three speakers across three episodes), `beatriz-villarroel` with
`paper-villarroel-bruehl-2025`, `jacques-vallee`, `richard-doty`, `paul-bennewitz`,
`battelle` with `howard-c-cross`, the `thomas-townsend-brown` / `louis-witten` /
`george-trimble` Wright Field group row, `tom-delonge`, `harold-puthoff`, `lincoln-lapaz`
(the Tombaugh and *Aviation Week* row), and `nnsa` with `d-foia`.
