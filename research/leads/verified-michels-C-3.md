# Section C verification, agent 3 (Michels corpus, 2 September 2026)

**Rows assigned:** all of section C in `michels-triage-4.md`; sections C2, C3, C4 and C5 of
`michels-triage-6.md`; section C2 of `michels-triage-5.md`. The C1 false-ABSENT lists in
triage-5 and triage-6 were NO ACTION by instruction and are not treated per row.

**Status: nothing was added to the board.** No file under `research/*.json`, `tools/`, `data/`
or `dist/` was touched and no git command was run. Everything below is a draft for Stewart to
accept or reject. Every URL here was opened from this machine, and every timestamp was re-read
in the transcript file rather than taken from the lead map's paraphrase.

**Three rows concern the same node.** `thomas-townsend-brown` is row 2 of triage-4 section C,
the whole of triage-6 C2, and one row of triage-5 C2. They are handled together in section 2
below.

---

## Summary

| # | Node id | Verdict | Reason |
|---|---|---|---|
| 4.C1 | `william-mccasland` | ATTRIBUTE | The board carries the disappearance at month precision. The episode gives 27 February 2026 with the hour of the 911 call |
| 4.C2 / 6.C2 / 5.C2 | `thomas-townsend-brown` | RECORD + ATTRIBUTE | The FBI file the node already cites was opened. It does **not** contain the radar superlative three maps attribute to it. The NRL appraisal and its denial are carried as attribution |
| 4.C3 | Ning Li (prose only) | NO ACTION | No `ning-li` node exists; "Ning Li" appears 3 times in `data/the-program.json` as prose. Creating one is section A/B promotion work, not a correction to a node the board carries |
| 4.C4 | `george-trimble` | RECORD | The UNC department history the node already cites names the Air Force funding route, and it is **not** the Wright Air Development Center the transcript names |
| 4.C5 | `oni` | ATTRIBUTE | McKinnon on the record naming ONI as the holder of his seized drives and the investigation as open. The node carries nothing on this |
| 4.C6 | `italo-venturelli` / `hospital-regional-varginha` | NOT REACHED | See NOT REACHED. The caption-corruption warning stands: "Vargem Grande do Sul" is Varginha and must not become a second location node |
| 4.C7 | `robert-salas` | ATTRIBUTE | A SAC write-up on Echo Flight that the node does not name. The node carries the 17 March 1967 teletype, a different paper |
| 4.C8 | `robert-hastings` | NO ACTION | Triage-5 C2 records the same count as unstable across three episodes and two corpora (167 against "12 to 15"; 400-800 against "a couple hundred"). Recording one number would assert precision the corpus does not have |
| 4.C9 | `glenn-gaffney` | NO ACTION | The node already carries Knapp naming Gaffney on the congressional record and AARO's own account of a former senior CIA official quashing the removal in 2009-2010. "Twice, in 2008 and 2010" rests on an unidentified witness and the map says so |
| 4.C10 | `donald-kerr` | NO ACTION | The appointment chain is already on the node, recited at his own 1 August 2007 SSCI confirmation hearing: Los Alamos, DOE, FBI Laboratory Division, CIA DS&T, NRO. The Oke Shannon gloss adds no checkable link the node lacks |
| 4.C11 | `steven-schiff` | NO ACTION | The route runs through J. Andrew Kissner, whom the map itself marks UNRESOLVED. A route through an unresolved name is a search string, not a claim |
| 6.C3 | Winterhaven | **NO ACTION, deliberately** | The 30 August correction holds and must not be re-corrected. See section 6 |
| 6.C4 | `aurora-budget-line` | NO ACTION | The node already carries $80M FY86 and $2.27bn FY87 off CIA-RDP90-00965R000807470050-4 and says in its own text that $2.3 billion is the article's rounding. Two more speakers repeating the rounded, mis-dated form changes nothing |
| 6.C5 | `edward-condon` | RECORD | Los Alamos National Laboratory's own account of LA-1 contradicts the three speakers who say Condon wrote the Primer. The other five sub-items were not opened |
| 5.C2 row 1 | `mit-lincoln-laboratory` | NO ACTION | Already carried, and carried more precisely: the board names the recording 'AF-ATIC-FILM, 03/52', the briefer as Ruppelt, the audience as the Beacon Hill Study, and Lincoln Laboratory's 25 June 2026 agreement to make it available |
| 5.C2 rows 2-14 | see NOT REACHED | NOT REACHED | Thirteen rows not adjudicated |

Counts: **3 RECORD, 4 ATTRIBUTE, 9 NO ACTION, 14 NOT REACHED.**

---

## 1. `william-mccasland` (triage-4 C1) - ATTRIBUTE

The node's chronology carries `2026-02-01` with `"precision": "month"` and its claims say
"vanished in February 2026", sourced to Fox News of 21 April 2026. The episode gives the day,
the hour of the missing-person report and the agencies that joined the search. Read at
0:05:16 to 0:09:04 in
`dist/transcripts/md/2026-04-21 why-americas-top-scientists-are-going-missing-they-knew-too-much.md`.

This is attribution, not correction. Nothing was opened that dates the disappearance, so the
node's own `2026-02-01` month-precision entry stays as it is until a Bernalillo County
Sheriff's Office or silver-alert record is opened. **Do not overwrite the chronology date on
the strength of a podcast.**

The corpus spells him "Neil McCaslin" throughout, which is why the cross-check reported him
ABSENT. That is a note for `research/_removed.json`, not a claim.

```json
{
 "id": "william-mccasland",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 21 April 2026, Michels dated the disappearance to Friday 27 February 2026 at Quail Run Court, Albuquerque: a repairman saw McCasland at the house around 10am, his wife left at about 11:10am and returned at 12:04pm to find him gone, and she reported him missing at 3:07pm. He said the prescription glasses, a switched-off phone and a smartwatch were left behind, and that a red backpack, the wallet and a .38-calibre revolver with its holster were missing (0:05:16 to 0:06:12).", "source": "American Alchemy with Jesse Michels, 'Why America's Top Scientists Are Going Missing [They Knew Too Much...]', 21 April 2026, 0:05:16 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3303927368.mp3?updated=1776795850"},
  {"tier": 2, "text": "In the same episode Michels said that within a week the search had grown from the Bernalillo County Sheriff's Office to the FBI's Albuquerque Field Office, the Air Force Office of Special Investigations, New Mexico State Search and Rescue and Albuquerque Mountain Rescue, and that no camera footage of McCasland ever surfaced (0:09:04).", "source": "American Alchemy with Jesse Michels, 'Why America's Top Scientists Are Going Missing [They Knew Too Much...]', 21 April 2026, 0:09:04 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3303927368.mp3?updated=1776795850"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Why America's Top Scientists Are Going Missing [They Knew Too Much...]', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3303927368.mp3?updated=1776795850", "date": "2026-04-21"}
 ]
}
```

---

## 2. `thomas-townsend-brown` (triage-4 C2, triage-6 C2, triage-5 C2) - RECORD and ATTRIBUTE

Three triage files send material at this node. The single most-repeated item across them is
the claim that a **1942 or 1943 FBI file** describes Brown as knowing more about radar
detection than any individual in the US Navy. The node already cites Brown's released FBI
file, FOI/PA# 1496195-000, as a full-text file on archive.org. I opened that file, all 263,609
bytes of it, and searched it.

**The record contradicts the transcript.** "Radar" occurs twice in the whole file and neither
occurrence is the sentence three maps attribute to it:

| what the maps say the file says | what the opened file actually says |
|---|---|
| the FBI file states Brown knew more about radar detection than any individual in the US Navy | no such statement anywhere in the released file |
| a 1942 FBI file placing him in Laurel Canyon and pointing to the Navy exit | the file records his 1942 Navy exit in the opposite register: he "was dismissed from the U. S. Navy Reserve in 1942 'for the good of the Service and to escape general court martial'" |
| Brown ran the Atlantic Fleet Radar School | the file carries this only at two removes: a Los Angeles Times article of 4 July 1948 saying so, and an informant reporting that "BROWN claims to have been a lieutenant commander in the Navy during the war, one of his principal jobs being the administration of the Atlantic Fleet Radar School" |

The transcript's file and the released file may not be the same file, and this record cannot
prove that a 1942-43 FBI file does not exist somewhere. What it establishes is that **the FBI
file this board cites does not support the claim, and says something materially less
flattering about the same year.** That is the finding.

"Biefeld" appears zero times in the FBI file, as it does zero times on the board. Nothing
opened here supports adding Paul Alfred Biefeld, and the Glenn L. Martin employment stays
uncorroborated: "Martin" appears nowhere in the FBI file, the node already grades the
Winterhaven biography's Martin line as a self-description, and map 30 corrupts it as "Martin
Vega Corporation". **Do not resolve the Martin item off these transcripts.**

The Naval Research Laboratory appraisal is different in kind. It is a named document plus a
named denial, and the denial is the checkable half. Read at 0:22:15 in
`dist/transcripts/md/2024-10-05 the-cia-scientist-who-cracked-antigravity-townsend-brown-documentary.md`.

```json
{
 "id": "thomas-townsend-brown",
 "cls": "person",
 "claims": [
  {"tier": 1, "text": "The released FBI file on Brown, FOI/PA# 1496195-000, contains no statement that Brown knew more about radar detection than any individual in the US Navy. Its only two references to radar are a Los Angeles Times article of 4 July 1948 reporting that 'During World War II he headed the U. S. Navy's Atlantic Fleet Radar School', and an informant's account that 'BROWN claims to have been a lieutenant commander in the Navy during the war, one of his principal jobs being the administration of the Atlantic Fleet Radar School.' Three American Alchemy episodes attribute the radar superlative to a 1942 or 1943 FBI file; it is not in the file this board cites.", "source": "FBI file on Thomas Townsend Brown, FOI/PA# 1496195-000, full-text search https://archive.org/download/tt-brown/E65ffaeec360d48a08a97fb70305b58f18aac8f13_Q104175_R432679_D2722930_20231226_132723_djvu.txt"},
  {"tier": 1, "text": "The same file summarises the 1942 Navy separation as follows: 'The current investigation has developed much information on BROWN, including that he was dismissed from the U. S. Navy Reserve in 1942 \"for the good of the Service and to escape general court martial\".'", "source": "FBI file on Thomas Townsend Brown, FOI/PA# 1496195-000, investigative summary https://archive.org/download/tt-brown/E65ffaeec360d48a08a97fb70305b58f18aac8f13_Q104175_R432679_D2722930_20231226_132723_djvu.txt"},
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 5 October 2024, the narration of the Townsend Brown documentary said that when Tom Valone of the Integrity Research Institute tried to locate a copy of a 1952 Naval Research Laboratory appraisal of Brown's experiments titled 'The TT Brown Electrogravity Device', the laboratory no longer had it (0:22:15).", "source": "American Alchemy with Jesse Michels, 'The CIA Scientist Who Cracked Antigravity (Townsend Brown Documentary)', 5 October 2024, 0:22:15 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4979487868.mp3?updated=1751926015"}
 ],
 "sources": [
  {"name": "FBI file on Thomas Townsend Brown, FOI/PA# 1496195-000, full text", "url": "https://archive.org/download/tt-brown/E65ffaeec360d48a08a97fb70305b58f18aac8f13_Q104175_R432679_D2722930_20231226_132723_djvu.txt", "date": "2026-09-02"},
  {"name": "American Alchemy with Jesse Michels, 'The CIA Scientist Who Cracked Antigravity (Townsend Brown Documentary)', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4979487868.mp3?updated=1751926015", "date": "2024-10-05"}
 ]
}
```

No `desc` replacement is proposed. The node's narrative already separates what Brown patented
from what was written about him, and nothing opened here contradicts a sentence of it.

Not carried, and why: the 1968 Northrop electro-aerodynamics paper said to have vanished from
the AIAA record (0:26:29) is a second-hand account of an absence, attributed to a pseudonymous
source, "Dan Marcus", named as a primary source for another author's book. An absence reported
by a pseudonym is not a record. The Borderland Sciences correspondence shipped to Norrkoping
(triage-4 C2b) and the Teller-to-Odlum introduction (triage-5) were not opened and are in
NOT REACHED.

---

## 3. `george-trimble` (triage-4 C4) - RECORD

The map claims the Institute of Field Physics was funded by the **Wright Air Development
Center**. The node already cites the UNC Physics and Astronomy department history. I opened it.

The page names the Air Force as a funder of general relativity research, and names the office:
the "modern physics research branch" at the **Aeronautical Research Laboratory, Wright-Patterson
Air Force Base**, run for these purposes by Joshua Goldberg. The page does not use the words
"Wright Air Development Center" or "WADC" anywhere. The transcript names the wrong organisation
on the same base.

This matters because the contractor-to-service link the triage row wants to close runs through
whichever office actually held the money, and the two are different bodies.

```json
{
 "id": "george-trimble",
 "cls": "person",
 "claims": [
  {"tier": 1, "text": "The UNC Physics and Astronomy department history names the Air Force route into the Institute of Field Physics as the Aeronautical Research Laboratory at Wright-Patterson Air Force Base, not the Wright Air Development Center: 'Joshua Goldberg was, at the time of the establishment of the IOFP and the conference, in charge of aspects of the Air Force's funding of general relativity, in the \"modern physics research branch\" (based at the Aeronautical Research Laboratory at Wright Patterson Air Force Base).' The page uses neither 'Wright Air Development Center' nor 'WADC'.", "source": "History of the Institute of Field Physics (1955-1959), UNC Physics and Astronomy department history https://physics.unc.edu/home/department-history/section-ii/"}
 ],
 "sources": [
  {"name": "History of the Institute of Field Physics (1955-1959), UNC Physics and Astronomy department history", "url": "https://physics.unc.edu/home/department-history/section-ii/", "date": "2026-09-02"}
 ]
}
```

The row also asks that the Institute of Field Physics be promoted to a node of its own. That is
a new node and therefore section A/B work, not a section C correction, and it is not drafted
here. The page also names Agnew Bahnson as the Institute's primary funder, which is consistent
with triage-6's observation that Bahnson is the best-supported name in the held-back group.

---

## 4. `oni` (triage-4 C5) - ATTRIBUTE

The node carries ONI's self-description, its listing in the 2021 ODNI Preliminary Assessment,
and its FOIA refusals on Nimitz material. It carries nothing about McKinnon; "McKinnon" is zero
occurrences in `data/the-program.json`. This is a named agency described by the affected party
as holding named seized material in an open investigation, which the node can carry as
attribution independent of anything McKinnon says he found. Read at 0:56:22 in
`dist/transcripts/md/2026-03-01 the-man-that-hacked-nasa-and-found-ufos-interview-w-gary-mckinnon.md`.

```json
{
 "id": "oni",
 "cls": "institution",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 1 March 2026, Gary McKinnon said that on his arrest 'all my data was taken to O&I, Office of Naval Intelligence', that ONI still holds his hard drives, and that he has tried to recover them for years and been told it is an ongoing investigation (0:56:22).", "source": "American Alchemy with Jesse Michels, 'The Man That Hacked NASA and Found UFOs [Interview w/ Gary McKinnon]', 1 March 2026, 0:56:22 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6287765066.mp3?updated=1772392329"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'The Man That Hacked NASA and Found UFOs [Interview w/ Gary McKinnon]', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6287765066.mp3?updated=1772392329", "date": "2026-03-01"}
 ]
}
```

---

## 5. `robert-salas` (triage-4 C7) - ATTRIBUTE

The node carries an Air Force teletype of 17 March 1967 reporting loss of strategic alert at
Malmstrom. It does not name any Strategic Air Command report. The value of this row is that it
points a later pass at a different service document. The claim is written as a
characterisation, because that is all the transcript gives: no number, no date, no addressee.
Read at 0:19:06 in
`dist/transcripts/md/2026-02-09 meet-the-nuclear-missile-guard-abducted-by-aliens.md`.

```json
{
 "id": "robert-salas",
 "cls": "person",
 "claims": [
  {"tier": 2, "text": "On American Alchemy with Jesse Michels, 9 February 2026, Michels said that Strategic Air Command 'wrote up a whole write up saying we're baffled and confused' about the Echo Flight incident, which he placed eight days before the Oscar Flight shutdown, and that targeting officer Bob Jamison went in to check why the ten missiles went down (0:19:06). No document number, date or addressee is given for the SAC write-up.", "source": "American Alchemy with Jesse Michels, 'Meet the Nuclear Missile Guard Abducted by Aliens', 9 February 2026, 0:19:06 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9102178952.mp3?updated=1770679988"}
 ],
 "sources": [
  {"name": "American Alchemy with Jesse Michels, 'Meet the Nuclear Missile Guard Abducted by Aliens', episode audio", "url": "https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9102178952.mp3?updated=1770679988", "date": "2026-02-09"}
 ]
}
```

Note the internal tension the node already records: its own open question is whether Salas was
at Echo Flight on 16 March or Oscar Flight on 24 March 1967. The transcript's "eight days
before" is a third interval and does not settle it.

---

## 6. Winterhaven (triage-6 C3) - NO ACTION, and this is the point

**The 30 August correction holds. Do not re-correct it.** The board's claim is narrow: the
words saucer, interceptor, Mach and Air Force appear zero times in the 66-page Project
Winterhaven proposal, and the saucer-as-USAF-interceptor framing comes from the 1956 Aviation
Studies report. Map 32 describes the proposal as containing barium-motor gravitator discs and
"novel communications". That is a claim about different content and does not touch the board's
claim. There is no tension to resolve, and resolving one would be another instance of the
`CLAUDE.md` section 2 corollary about two passes correcting something that was already right.

Nothing is drafted for this row and nothing should be.

---

## 7. `edward-condon` (triage-6 C5) - RECORD

Three maps say Condon wrote the Los Alamos Primer. I re-read the clearest of them, batch 30
file 02, at 0:06:46 in
`dist/transcripts/md/2024-10-05 how-i-know-david-grusch-is-not-lying.md`: Michels says Condon
"helped pick Los Alamos as the location for the Manhattan Project, even writing the Los Alamos
primer, a document that all employees had to read upon arrival."

Los Alamos National Laboratory's own account says otherwise, and the difference is the whole of
the claim: Serber gave the lectures, Condon transcribed and compiled them.

```json
{
 "id": "edward-condon",
 "cls": "person",
 "claims": [
  {"tier": 1, "text": "Los Alamos National Laboratory's own account of the Los Alamos Primer states: 'Physicist Edward Condon transcribed the lectures and compiled the notes into the first official Los Alamos technical report, or LA-1.' The lectures were Robert Serber's, given in April 1943, and LA-1 was declassified in 1965. Three American Alchemy episodes describe Condon as having written the Primer; the laboratory's account gives him the transcribing and compiling role and gives the lectures to Serber.", "source": "Los Alamos National Laboratory, 'The Los Alamos Primer', National Security Science https://www.lanl.gov/media/publications/national-security-science/0723-the-los-alamos-primer"}
 ],
 "sources": [
  {"name": "Los Alamos National Laboratory, 'The Los Alamos Primer', National Security Science", "url": "https://www.lanl.gov/media/publications/national-security-science/0723-the-los-alamos-primer", "date": "2026-09-02"}
 ]
}
```

The other five sub-items of triage-6 C5 (Col. Robert Hippler, Guy Hottel's
loyalty-investigation dossier, Lewis Branscomb as the 1966 clearance route, the Leslie Groves
clash, Max Born at Gottingen) were **not opened** and are listed under NOT REACHED. Two of them
name where the paper is: the University of Colorado UFO Project records and NARA RG 77. Neither
reaches from here without a finding aid.

---

## NOT REACHED

Rows I did not adjudicate to the standard, with what is left to do on each.

| Row | Node | What remains |
|---|---|---|
| 4.C6 | `italo-venturelli` / `hospital-regional-varginha` | The Fortunato autopsy hypothesis and the exhumation request are a fresh full-length interview I did not re-read at 17 / 3:09:19. **The caption warning stands and is the load-bearing part: "Vargem Grande do Sul" is a corruption of Varginha, and no second location node may be created** |
| 6.C5 | `edward-condon` | Hippler, Hottel, Branscomb, Groves, Max Born: five sub-items, none opened |
| 5.C2 | `sean-kirkpatrick`, `l-skinwalker` | Fugal's dated photograph rebutting Kirkpatrick's pre-2022 denial. Transcript not re-read |
| 5.C2 | `battelle` | The DARPA N3 Phase 2 team claim cites Battelle's own 2020 release, which is a document to open rather than an attribution. Not opened |
| 5.C2 | `immaculate-constellation` | Brown's NSC-cognizance and Sentient-integration account, which he states as his own inference |
| 5.C2 | `dylan-borland`, `jon-kosloski` | The unsigned Memorandum for Record allegation and the original-classification-authority argument |
| 5.C2 | `william-mccasland` (SAPOC) | Three independent non-corroborations against Burlison's SAPOC placement. This is the most valuable unreached row in triage-5: it is evidence **against** a claim, which the board under-collects |
| 5.C2 | `glenn-gaffney`, `george-knapp`, `bigelow-aerospace` | Handled only as far as 4.C9 goes; Burlison naming him a subpoena target is not adjudicated |
| 5.C2 | `l-skinwalker`, `skinwalkers-at-the-pentagon` | Travis Taylor's concurrent UAP Task Force role |
| 5.C2 | `tim-gallaudet` | The advisory council reporting to ODNI rather than the White House, and the Bluegill Triple Prime deck logs. **Note `CLAUDE.md` section 9: Bluegill's date and contents are already recorded as contradicted by the opened record. Do not move that node toward the podcast** |
| 5.C2 | `robert-hastings`, `robert-salas` | Treated as 4.C8 NO ACTION on the count; the underlying instability is worth a note somewhere, not a claim |
| 5.C2 | `salvatore-pais` | Burlison's in-person account near Pax River |
| 5.C2 | `eric-burlison` | The FFRDC letter campaign beyond MITRE, to Aerospace Corporation, RAND and IDA |
| 5.C2 | `stargate-program` | The 1995 commissioned evaluation naming Jessica Utts as one of two assessors. This is the cleanest RECORD candidate left in the whole assignment: a named, dated, findable document |

---

## Access notes from this pass

To add to the reach facts in `VERIFY-BRIEF-2026-09-02.md`:

- `fas.org` and `sgp.fas.org` returned **HTTP 202 with a zero-byte body** to curl for a PDF,
  and WebFetch received empty content from the same URL. That is a challenge page, not a
  document. LA-1 itself was therefore **not** opened; the LANL publication page was.
- `lanl.gov` answers WebFetch.
- `physics.unc.edu` answers WebFetch.
- `archive.org/download/...djvu.txt` answers curl directly and is the cheapest way to full-text
  search a file the board already cites. It is how the Brown FBI finding above was reached, and
  it took under a minute.
