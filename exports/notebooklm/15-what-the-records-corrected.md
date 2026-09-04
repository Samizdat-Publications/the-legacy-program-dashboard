# What the records corrected

This is the file that keeps the rest honest. It is the board's own record of the places where the research was wrong, thin or malformed, and what the documents actually said when somebody went and checked. Read against the confident prose in the other files, this is the correction the material deserves.

One thing to be clear about, because the export will not pretend otherwise: the corrections file stores the corrected value and the reasoning for it. In most cases it does not store the superseded wording, so these entries say what the record now says and why, rather than quoting what the board used to say. Where the file does carry the replaced sentence, it is quoted here in full and marked as the replaced text.

## The reasoning, in the board's own words

Each of these is the written justification for one pass of corrections. They are reproduced whole because the reasoning is the evidence.

### affiliations why

affiliations is a PROSE field upstream: The Vanishing writes 'NASA Jet Propulsion Laboratory (1998-2022)' into it and renders it verbatim. The research on this board wrote node ids into it instead, so 54 entries reached the dossier as raw slugs - a reader saw 'dod-sapco', 'uk-mod-ufo-desk' and 'skidmore-fitts-report' where a name belonged. 46 of them name a real node and the renderer now resolves those to the node's label and makes them navigable, which keeps the link rather than throwing it away. The eight below name an institution that is not on the board, so they are written out as the prose this field has always held, using the name each person's own sub field already gives.

### dannyjones 2026 09 03 why

Section C of research/leads/CANDIDATES-2026-09-03-DANNYJONES.md, applied 3 September 2026. Eighteen additive records: five people and thirteen entities. All are additions of claims and sources except wilson-davis-memo, where the decision list calls for a field replacement and the record carries the whole desc with exactly one sentence swapped, the replaced sentence quoted verbatim in _replacement. The four nitinol nodes (uap-gerb, battelle, l-columbus-oh, gerb-battelle-investigation, found by grepping the board for 'nitinol') each gain the same Tier 1 record claim about what the federal literature says; the Bragalia allegation is deliberately NOT removed and is labelled unsupported inside the new claim.

### dates congress why

Ten members of the 10 U.S.C. 119(e)(2) notification group carried no date, so the board could not place them in time at all. Each takes the convening date of the Congress in which that member first held the seat their own sub and Tier 1 claims name - not a date invented for them, and not the date a committee web page was read. Convening dates verified against the Senate's own table: 111th 6 January 2009, 118th 3 January 2023, 119th 3 January 2025. That table is added as a source on each of the ten, because it is what the date rests on.

### dates researched why

Two dates could not be derived from the board and were researched. Levy takes 2025-06-01, the publication month of the UAPx field-expedition paper in Progress in Aerospace Sciences 156:101099 - the same date her first author Szydagis already carries on this board for the same paper. Powers takes 2026-05-20, the date the OSD Historical Office's Key Officials list of 7 July 2026 gives for his assumption of the acting Comptroller role. Checking it turned up a live contradiction between two Department pages: the comptroller site's leadership page still names Hurst, while war.gov's biography of Powers says Powers. The Historical Office list dates the handover and settles it, and the contradiction is recorded as a claim rather than quietly resolved.

### dates why

34 people carried no date. An undated person is invisible to the timeline and to the temporal edge derivation, so the board simply did not connect them. 20 are settled here from the board's own sourced claims. Seven AAWSAP DIRD authors get the exact publication date their own Tier 1 claim states - Towe 31 Mar 2010, Miley 10 Mar 2010, Baker 6 Apr 2010, Leonhardt 2 Mar 2010, Millis 1 Nov 2010, Culbreth 20 Nov 2010, Genik 15 Dec 2010. Thirteen more are DIRD authors whose delivery date this board has not established; they take 2010-01-01, which is the marker already used on Puthoff, Davis and Green for precisely that. It denotes the AAWSAP delivery period and is not a claim about a known day. McKeon and Cole take the seat dates their own claims state. NOT set here: the DIA list date of 9 January 2018 was rejected as a date for these authors. It is when DIA transmitted the title list to the Senate Armed Services Committee, eight years after the work, and using it would place every DIRD author in 2018 and cluster them temporally with the disclosure fight rather than with the programme that commissioned them.

### dird label why

Two distinct DIRDs carried the identical label 'Aneutronic Fusion Propulsion', so the board showed a reader two nodes it could not tell apart. They are genuinely different documents and both were downloaded and their covers read on 22 August 2026: DIA-08-1011-003 at 50 pages, authored by Culbreth, and DIA-08-1011-004 at 37 pages, authored by Teofilo, both dated 1 November 2010. Both cover pages carry the same title, so the ambiguity is in the source documents, not in this board's transcription of them. The document number is appended to each label because that is what actually distinguishes them and it was read directly off the covers. NOT asserted: which of the two the DIA's 9 January 2018 list calls 'Aneutronic Fusion Propulsion II'. Culbreth's own claim on this board says list item 30 carries that title and is credited to him, which would make DIA-08-1011-003 the 'II' despite the lower document number. The list itself could not be retrieved to check - irp.fas.org returns HTTP 202 with an empty body - so the roman numeral is left off both labels rather than guessed onto one.

### sequence chain why

chainHtml() reads s.date, s.event, s.source and s.isAnomalous off every chain step. All 11 sequenceChains on this board held bare node-id strings or free prose instead, so every one rendered an undefined event under an undefined date - on Grusch, Elizondo, Davis and Marcel among others. Nothing threw and no count moved, so nothing caught it. The renderer is inherited from The Vanishing, where a chain step is an ordered, dated, individually sourced link; the research wrote program lineages and shorthand labels into the same field. Each chain below is rebuilt from that person's own on-board chronology, and each step's source is the claim on the same person that covers it. Steps the old chain asserted but the record here does not carry were dropped rather than written from memory. Where no claim on the node covers a step, the source is null and the dock prints 'No attributed source on file', which is the true statement. uap-gerb is set empty: its old chain pointed at Burlison letters that are not on that node, and it has no ordered chain of individually documented links. The dock prints the 'No sequence chain' block, which says that is a finding rather than a gap.

### thin sourcing why

The thin-sourcing backlog is worked source by source, and a source is not added here unless it was opened. Parnell is done: the Department's own release of 18 March 2026 carries the attribution 'Chief Pentagon Spokesman Sean Parnell', which is the Department attributing the role to him rather than a report of it. The rest stalled on retrieval, not on effort. The natural second source for the congressional figures is the Congressional Directory or a member biography, and congress.gov and bioguide.congress.gov both refuse this session; for the historical committee roles - Raskin as Oversight ranking member in the 118th, Gallagher's select-committee chair - the tool is an archived committee page, and web.archive.org is blocked outright here. What IS reachable is recorded in notes/LINK-HEALTH-2026-08-22.md: govinfo.gov, oversight.house.gov, the committee sites, war.gov and theblackvault.com all answer, so this work is resumable rather than blocked, and the route is written down. One note on phrasing. The first draft of the Parnell claim was demoted by the interested-party rule, because it said the Department 'issues releases under his name' and the attribution vocabulary does not contain 'issues' or 'titled'. The fix was to phrase the claim as the attribution it actually is - the release NAMES him - rather than to widen the rule again to fit one sentence. Widening a check until it accepts your own prose is fitting the test to the answer.

## Corrections to the people

86 records in the people set were changed by what the documents said.

### Adam Smith

Fields the record forced a change to: date, sources.

Its date is now set to 2023-01-03, derived from the record rather than assigned.

Sources added to it: U.S. Senate, Dates of Sessions of the Congress (convening dates: 111th 6 Jan 2009, 118th 3 Jan 2023, 119th 3 Jan 2025), https://www.senate.gov/legislative/DatesofSessionsofCongress.htm, dated 2026-08-22.

### Beatriz Villarroel

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 25 October 2025, at 0:22:14 to 0:23:09, Beatriz Villarroel said that since about the early 1960s there have been objects called uncorrelated targets, seen once or a few times on radar or optical sensors and then untrackable, and that these are subtracted from the background when the number of objects in space is calculated. She said the subtraction is not done by NASA or ESA themselves. Source: American Alchemy with Jesse Michels, 'Top Astronomer: I Found 100,000 UFOs Above Earth! (ft. Beatriz Villarroel)', 25 October 2025, 0:22:14, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1307454785.mp3?updated=1761413167
- **Tier 2 named person on the record.** At 0:24:04 in the same episode Villarroel said the lists are held by the Space Force and are classified, including the earliest from the 1960s, and that what she wants is one such list of coordinates so she can test whether the objects vanish in the Earth's shadow. Asked how she knows, she answered 'I think that's what I heard from someone on the inside, yes.' The sourcing limit is hers, stated in the passage. Source: American Alchemy with Jesse Michels, 'Top Astronomer: I Found 100,000 UFOs Above Earth! (ft. Beatriz Villarroel)', 25 October 2025, 0:24:04

Sources added to it: American Alchemy with Jesse Michels, 'Top Astronomer: I Found 100,000 UFOs Above Earth! (ft. Beatriz Villarroel)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1307454785.mp3?updated=1761413167, dated 2025-10-25.

### Général Bernard Norlain

Fields the record forced a change to: affiliations.

Affiliations rewritten as prose rather than as raw identifiers: ihedn, cometa, Armée de l'Air (French Air Force).

### Betty McCollum

Fields the record forced a change to: date, sources.

Its date is now set to 2023-01-03, derived from the record rather than assigned.

Sources added to it: U.S. Senate, Dates of Sessions of the Congress (convening dates: 111th 6 Jan 2009, 118th 3 Jan 2023, 119th 3 Jan 2025), https://www.senate.gov/legislative/DatesofSessionsofCongress.htm, dated 2026-08-22.

### Adm. Bobby Ray Inman

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** He is not among the directors of The Wackenhut Corporation in any proxy statement EDGAR holds. The proxy for the annual meeting of 7 May 1999 lists twelve directors by name, age and year of first election, among them Julius W. Becton Jr., Benjamin R. Civiletti, Paul X. Kelley, Thomas P. Stafford and George R. Wackenhut, and the name Inman appears nowhere in it. It appears nowhere in the proxy for the 1998 annual meeting or in the 2002 merger proxy either. The corporation reported under CIK 0000104030, SIC 7381; its earliest filing of any kind is dated 24 March 1994 and its earliest proxy statement is a preliminary 14A of 24 March 1997, so no proxy exists on EDGAR for any earlier year and the board's composition before 1997 is unestablished in either direction. Source: SEC EDGAR company filing index, CIK 0000104030, https://data.sec.gov/submissions/CIK0000104030.json ; The Wackenhut Corporation DEF 14A filed 31 March 1999, https://www.sec.gov/Archives/edgar/data/0000104030/000095014499003822/0000950144-99-003822.txt ; DEF 14A for the 1998 annual meeting and DEFM14A filed 10 April 2002, https://www.sec.gov/Archives/edgar/data/0000104030/000095014498003074/0000950144-98-003074.txt
- **Tier 2 named person on the record.** On the Danny Jones Podcast, episode 320, 4 August 2025, at 2:06:30, the guest who identifies himself only as UAP Gerb said Bobby Ray Inman was a Wackenhut board member. The corporation's own proxy statements for 1997 to 2002 do not name him. Source: Danny Jones Podcast, ep. 320, 4 August 2025, 2:06:30, mapped at research/leads/dannyjones-corpus-20.md
- **Tier 2 named person on the record.** This node's unresolved line on a National Underwater Reconnaissance Office stays as written. A third corpus running has failed to open any record of the office: nro.gov and nsa.gov returned HTTP 403, irp.fas.org has no NURO page, the govinfo search API returned a count of zero for the phrase, and the strings NURO and National Underwater Reconnaissance occur nowhere in the fifty released pages of the CIA's own AZORIAN history. Source: PROJECT AZORIAN: THE STORY OF THE HUGHES GLOMAR EXPLORER, CIA reading-room document 0005301269, searched in full, https://archive.org/download/cia-readingroom-document-0005301269/0005301269_djvu.txt

Sources added to it: SEC EDGAR company filing index, CIK 0000104030 (The Wackenhut Corporation), https://data.sec.gov/submissions/CIK0000104030.json, dated 2026-09-03; The Wackenhut Corporation, DEF 14A filed 31 March 1999, https://www.sec.gov/Archives/edgar/data/0000104030/000095014499003822/0000950144-99-003822.txt, dated 1999-03-31; The Wackenhut Corporation, DEF 14A for the 1998 annual meeting, https://www.sec.gov/Archives/edgar/data/0000104030/000095014498003074/0000950144-98-003074.txt, dated 1998-03-31.

### Bruce C. Towe

Fields the record forced a change to: date.

Its date is now set to 2010-03-31, derived from the record rather than assigned.

### Howard P. "Buck" McKeon

Fields the record forced a change to: date.

Its date is now set to 2009-06-16, derived from the record rather than assigned.

### Cecilia Levy

Fields the record forced a change to: date.

Its date is now set to 2025-06-01, derived from the record rather than assigned.

### Christopher A. Coons

Fields the record forced a change to: date, sources.

Its date is now set to 2025-01-03, derived from the record rather than assigned.

Sources added to it: U.S. Senate, Dates of Sessions of the Congress (convening dates: 111th 6 Jan 2009, 118th 3 Jan 2023, 119th 3 Jan 2025), https://www.senate.gov/legislative/DatesofSessionsofCongress.htm, dated 2026-08-22.

### Claudio Maccone

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### Colm A. Kelleher

Fields the record forced a change to: sequenceChain.

The rebuilt sequence chain:

- 1996-01-01, Begins leading the NIDS science team at Skinwalker Ranch. Source: Kelleher's own accounts in 'Hunt for the Skinwalker' (2005) and 'Skinwalkers at the Pentagon' (2021).
- 2005, Publishes 'Hunt for the Skinwalker' with George Knapp. Source: Kelleher's own accounts in 'Hunt for the Skinwalker' (2005) and 'Skinwalkers at the Pentagon' (2021).
- 2008-09-01, AAWSAP contract awarded to Bigelow Aerospace Advanced Space Studies; Kelleher serves as deputy administrator. Source: Reported consistently in the AAWSAP record and in Kelleher's own co-authored account with the programme manager.
- 2021, Publishes 'Skinwalkers at the Pentagon' with James Lacatski and George Knapp. Source: Kelleher's own accounts in 'Hunt for the Skinwalker' (2005) and 'Skinwalkers at the Pentagon' (2021).

### Dr David Clarke

Fields the record forced a change to: affiliations.

Affiliations rewritten as prose rather than as raw identifiers: sheffield-hallam, The National Archives, Kew.

### David Charles Grusch

Fields the record forced a change to: claims, cls, sequenceChain, sources.

The rebuilt sequence chain:

- 2021-07-01, First protected disclosure of classified UAP concealment information to the DoD Inspector General. Source: House Oversight hearing transcript, 26 July 2023.
- 2022-05-25, PPD-19 urgent-concern complaint filed with the ICIG by counsel Charles McCullough III. Source: no attributed source on file.
- 2022-07-01, ICIG finds the complaint credible and urgent. Source: no attributed source on file.
- 2023-04-04, DOPSR clears first submission for open publication. Source: DoD FOIA case 23-F-0946 release, OSD/JS Executive Services Directorate reading room; analysis by The Black Vault.
- 2023-06-05, The Debrief publishes Kean and Blumenthal's account of his allegations. Source: Kean and Blumenthal, The Debrief, 5 June 2023.
- 2023-07-26, Testifies under oath before the House Oversight Committee. Source: CHRG-118hhrg53022 CONTENTS; docs.house.gov EventID 116282.
- 2023-08-09, The Intercept publishes his 2014 and 2018 police and psychiatric records obtained by FOIA from Loudoun County. The board marks this step as the anomalous one. Source: no attributed source on file.
- 2025-07-24, Rep. Eli Crane writes DoD on his behalf citing clearance removal, denied promotion, lost medical retirement. The board marks this step as the anomalous one. Source: Rep. Eli Crane, letter to the Department of Defense dated 24 July 2025, entered into the record of the 9 September 2025 Task Force hearing.
- 2026-06-09, Speaks at a Capitol-steps press conference organised with Rep. Luna; describes a continuum of alleged non-human life and references four species. Source: Grusch at the Capitol press conference hosted by the House Task Force on the Declassification of Federal Secrets, 9 June 2026; Fox News, 10 June 2026.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 13 December 2024, at 0:07:12, Eric Davis described three separate acts against Grusch after his whistleblower complaint and before his testimony: he 'got harassed by, by someone in the National Reconnaissance Office', then 'got physically harassed at his home and in his vehicles by people unknown', then somebody leaked a PTSD episode from his private medical files. Davis names an institution only for the first. The three have three different actors and should not be merged. Source: American Alchemy with Jesse Michels, 'CIA Scientist: George Bush Was Briefed on UFOs (ft. Eric Davis)', 13 December 2024, 0:07:12 to 0:08:08, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7341687364.mp3?updated=1752173868

Sources added to it: American Alchemy with Jesse Michels, 'CIA Scientist: George Bush Was Briefed on UFOs (ft. Eric Davis)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7341687364.mp3?updated=1752173868, dated 2024-12-13.

### David N. Spergel

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 13 June 2025, at 0:15:15, Michels said a Wall Street Journal journalist he names only as Lena told him that Spergel 'is their de facto advisor on UFOs' and that on his account the objects are all space trash, light reflections and temperature inversions. Michels retold the same anecdote to Ross Coulthart on 21 June 2025 at 0:43:31 and to Richard Dolan on 28 June 2025 at 1:42:04. All three are the same speaker relaying the same unnamed journalist, not three independent sources, and Michels says in the first telling 'I have no smoking gun'. Source: American Alchemy with Jesse Michels, 'The Wall Street Journal Is Gaslighting You On UFOs', 13 June 2025, 0:15:15 and 0:16:09, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL4839772690.mp3?updated=1750950332

Sources added to it: American Alchemy with Jesse Michels, 'The Wall Street Journal Is Gaslighting You On UFOs' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL4839772690.mp3?updated=1750950332, dated 2025-06-13; American Alchemy with Jesse Michels, 'Ross Coulthart: I Located A UFO Base In Arizona!' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3194990234.mp3?updated=1752180278, dated 2025-06-21; American Alchemy with Jesse Michels, 'The UFO Kill List: Who Paid the Price? (Ft. Richard Dolan)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9096049904.mp3?updated=1752180025, dated 2025-06-28.

### Général Denis Letty

Fields the record forced a change to: affiliations.

Affiliations rewritten as prose rather than as raw identifiers: cometa, ihedn, Armée de l'Air (French Air Force).

### Dylan Borland

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 5 August 2026, Dylan Borland said that AARO sent him a Memorandum for Record of his interview that he told them was wrong, that AARO acknowledged the error in an email and asked him to write corrections, that he made and signed the corrections and kept his email confirming their receipt, and that when he went to ODNI on 10 September 2025 the version AARO had transmitted was not the corrected one: 'Arrow had sent over a false MFR, said that was the true one.' He says he retained the corrected document (1:58:28 to 1:59:26). Source: American Alchemy with Jesse Michels, 'I Saw a Triangle Shaped UFO At a NASA Hangar!' -Dylan Borland Tells All, 5 August 2026, 1:58:28 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3402784095.mp3
- **Tier 2 named person on the record.** In the same episode Borland argued that because AARO holds no original classification authority it had to refer his account out to the intelligence community and to private companies for a classification determination, and that his triangle account coming back unclassified while other drawings were classified is therefore itself evidence about what was seen: 'they would have to be classified' (2:23:27). Nothing opened for this board establishes AARO's classification authority either way; this is recorded as his argument. Source: American Alchemy with Jesse Michels, 'I Saw a Triangle Shaped UFO At a NASA Hangar!' -Dylan Borland Tells All, 5 August 2026, 2:23:27 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3402784095.mp3

Sources added to it: American Alchemy with Jesse Michels, 'I Saw a Triangle Shaped UFO At a NASA Hangar!' -Dylan Borland Tells All, episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3402784095.mp3, dated 2026-08-05.

### Edward U. Condon

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 19 October 2024, at 0:39:03, Michels said Condon 'wrote the McMahon Secrecy Act of 1946, which is the precursor to the Atomic Energy Act of 1954'. The authorship attribution is the speaker's own and is offered without a citation. Neither the McMahon Act nor an authorship claim about it is on this board. Source: American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:39:03, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004
- **Tier 2 named person on the record, allegation shaped wording as stored.** At 0:39:52 in the same episode Michels said Condon was 'in close coordination with Air Force kernels like Robert Hippler', and that a written memo exists in which Hippler tells Condon to show that UFO research was a waste of money. On 12 July 2025 at 0:37:53 Robert Salas independently described letters between an Air Force colonel, rendered by the caption as 'Robert Hitler', and Condon to the same effect. Two speakers, two episodes, one alleged memo, which neither of them produces. Source: American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:39:52, and 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:37:53
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 12 July 2025, at 1:07:14 and 1:08:25, Robert Salas said that in 1949 J. Edgar Hoover wrote a letter to Congress identifying Condon as, in Salas's own paraphrase, nothing less than a Russian spy; that he holds a copy; that Condon had earlier been asked to resign from the Manhattan Project over an unspecified security issue; and, at 1:09:15 to 1:10:08, that Lewis Branscomb urged Condon in about 1966 to take the Air Force UFO study as a route back to a security clearance. Salas twice says he does not know the details. Source: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 1:07:14 to 1:10:08, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599
- **Tier 1 documented.** Los Alamos National Laboratory's own account of the Los Alamos Primer states: 'Physicist Edward Condon transcribed the lectures and compiled the notes into the first official Los Alamos technical report, or LA-1.' The lectures were Robert Serber's, given in April 1943, and LA-1 was declassified in 1965. Three American Alchemy episodes describe Condon as having written the Primer; the laboratory's account gives him the transcribing and compiling role and gives the lectures to Serber. Source: Los Alamos National Laboratory, 'The Los Alamos Primer', National Security Science https://www.lanl.gov/media/publications/national-security-science/0723-the-los-alamos-primer
- **Tier 1 documented.** Lt Col Robert R. Hippler of the Science Division, Directorate of Science and Technology, Headquarters USAF, wrote to Condon on 16 January 1967: 'When you have looked into some sightings and examined some Blue Book records and become acquainted with the true state of affairs, you must consider the cost of the Air Force program on UFOs, and determine if the taxpayer should support this for the next decade.' The letter calls itself informal, says it expresses Hippler's own opinion and 'is not binding on you', and names its second subject as 'an apparently obscure understanding of what the Air Force wants'. Two Michels speakers describe this memo from memory without producing it; this is the document. Source: Lt Col Robert R. Hippler to Dr Edward U. Condon, 16 January 1967, Headquarters United States Air Force, pages 1 and 2, https://www.nicap.org/docs/HipplerLetters.pdf

Sources added to it: American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004, dated 2024-10-19; American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599, dated 2025-07-12; Los Alamos National Laboratory, 'The Los Alamos Primer', National Security Science, https://www.lanl.gov/media/publications/national-security-science/0723-the-los-alamos-primer, dated 2026-09-02; Hippler to Condon, 16 January 1967, with Low to Hippler, 27 January 1967 (NICAP document archive scan), https://www.nicap.org/docs/HipplerLetters.pdf, dated 1967-01-16.

### Eric Burlison

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 2 July 2026, Rep. Eric Burlison said his office sent an early letter to The Aerospace Corporation from his House Oversight role, that Aerospace responded by sending two people from its executive team, that the meeting was held in a SCIF during the Biden administration, and that 'they knew nothing' about UAP or reverse engineering. He said he expects to go back to them with more specific and detailed questions (0:19:48). Source: American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 0:19:48 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3
- **Tier 2 named person on the record.** In the same episode Burlison gave his reading of that answer and of the structure generally: that a programme is 'probably organized from the ffrdc level' because an FFRDC can create the programme and the funding justification and then report upward only what it must, and that turnover and compartmentation mean current officeholders will not find decades-old material unless outsiders hand them a named file and a date (0:20:42, 1:50:35). He states this as his own inference. Source: American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 1:50:35 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3

Sources added to it: American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3, dated 2026-07-02.

### Eric W. Davis

Fields the record forced a change to: sequenceChain.

The rebuilt sequence chain:

- 1996-01-01, Works with NIDS as a staff scientist under Bigelow. Source: no attributed source on file.
- 2002-10-16, Date attributed to the meeting with Vice Adm. Thomas R. Wilson recorded in the notes later known as the Wilson-Davis memo. The board marks this step as the anomalous one. Source: House Permanent Select Committee on Intelligence, Counterterrorism, Counterintelligence and Counterproliferation Subcommittee hearing, 17 May 2022; contemporaneous reporting.
- 2008-01-01, Authors Defense Intelligence Reference Documents for the DIA-funded AAWSAP effort through BAASS. Source: no attributed source on file.
- 2019-10-21, Gives a classified briefing on retrievals of unexplained objects to Senate Armed Services Committee staff. Source: Ralph Blumenthal, The New York Times, 23 July 2020, quoting Davis on the record.

### Eric H. Wang

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 15 November 2024, at 2:46:17, Matthew Pines named the source of the Wright-Patterson story about Wang: a book by the UFO researcher William Steinman on the 1948 Aztec crash, which Pines says describes 'Eric Henry Wang' as head of special projects at Wright-Patterson who came over with Operation Paperclip. This identifies the single secondhand source behind the story the board's existing caution declines. Source: American Alchemy with Jesse Michels, 'Matthew Pines: Anti-Gravity Tech & Inter-Dimensional Aliens', 15 November 2024, 2:46:17, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4097453442.mp3?updated=1751923843
- **Tier 2 named person on the record.** At 2:47:06 in the same episode Pines said Steinman's text refers to Wang's boss only as 'H-A-K', and that he himself concluded 'oh, Henry A. Kissinger'. Pines states the identification as his own inference from the initials, not as something Steinman wrote. Any Wang-to-Kissinger link would rest on that inference and on nothing else. Source: American Alchemy with Jesse Michels, 'Matthew Pines: Anti-Gravity Tech & Inter-Dimensional Aliens', 15 November 2024, 2:47:06, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4097453442.mp3?updated=1751923843
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 17 April 2025, Michels said at 0:03:33 that Eric Wang was 'the head of the Special Studies Department at Wright-Patterson', that attempts to verify his background lead to 'no biographical details, no employment records, no published research', and at 0:04:25 that the researcher William Steinman found an obituary giving Dr. Eric H. Wang as born in 1906, originally from Vienna and a graduate of the Vienna Technical Institute, a contemporary of Viktor Schauberger, and that in 1956 Wang's department was relocated to the Sandia complex at Kirtland Air Force Base. No document supporting any of this was opened, and the board's own reading of DTIC ADA073468, ADA073475 and AD0460283 located no Austrian birth. Source: American Alchemy with Jesse Michels, 'Henry Kissinger & UFO Secrecy: The Dark Connection', published 17 April 2025, at 0:03:33 and 0:04:25
- **Tier 2 named person on the record.** In the same episode, at 0:05:17, Michels said that Steinman tracked down Wang's widow, Maria Wang, and that she said her husband had reported directly to Henry Kissinger and that Kissinger had visited their home. The account is given by Michels as Steinman's. The board holds no record of Maria Wang, of any Kissinger connection, or of Steinman's correspondence. Source: American Alchemy with Jesse Michels, 'Henry Kissinger & UFO Secrecy: The Dark Connection', published 17 April 2025, at 0:05:17
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 21 February 2025, at 1:33:30, the guest Sammy, known as UAP Gerb, said that 'Eric Henry Wang, who ran special projects at Wright-Patterson, or Wright Airfield at the time, was taken to Kirtland Air Force Base', and that 'Wang was also talked about by primary Kingman witness, Arthur Stancil Jr.' The board's own DTIC reading establishes Wang's move to Kirtland and names Arthur Stansel as his colleague; it establishes nothing about Kingman. Source: American Alchemy with Jesse Michels, 'The Most Knowledgeable UFO Researcher In The World', published 21 February 2025, at 1:33:30
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 17 April 2025, at 0:01:44 and 0:02:38, Michels said that Arthur Stansell, described as a consultant on blast effects of atom bombs, was flown to a classified location near Kingman, Arizona, told a secret test vehicle had crashed, and saw a craft roughly thirty feet in diameter and, in a nearby tent, four-foot humanoid figures. Michels said a declassified Operation Upshot-Knothole report confirms Stansell was on site for the nuclear testing there. The board's copy of that report series names Arthur Stansel and carries no Kingman material. Source: American Alchemy with Jesse Michels, 'Henry Kissinger & UFO Secrecy: The Dark Connection', published 17 April 2025, at 0:01:44 to 0:02:38

Sources added to it: American Alchemy with Jesse Michels, 'Matthew Pines: Anti-Gravity Tech & Inter-Dimensional Aliens' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4097453442.mp3?updated=1751923843, dated 2024-11-15; American Alchemy with Jesse Michels, 'Henry Kissinger & UFO Secrecy: The Dark Connection' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9751630361.mp3?updated=1751925715, dated 2025-04-17; American Alchemy with Jesse Michels, 'The Most Knowledgeable UFO Researcher In The World' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE8993457707.mp3?updated=1751590849, dated 2025-02-21; Blast Effects on Existing Upshot-Knothole and Teapot Structures, DTIC AD0460283, full text, https://archive.org/stream/DTIC_AD0460283/DTIC_AD0460283_djvu.txt, dated 1960-05-06.

### Friedwardt Winterberg

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### Gary Anthony

Fields the record forced a change to: affiliations.

Affiliations rewritten as prose rather than as raw identifiers: British UFO Research Association (BUFORA).

### George D. Hathaway

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### George H. Miley

Fields the record forced a change to: date.

Its date is now set to 2010-03-10, derived from the record rather than assigned.

### George S. Trimble

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The UNC Physics and Astronomy department history names the Air Force route into the Institute of Field Physics as the Aeronautical Research Laboratory at Wright-Patterson Air Force Base, not the Wright Air Development Center: 'Joshua Goldberg was, at the time of the establishment of the IOFP and the conference, in charge of aspects of the Air Force's funding of general relativity, in the "modern physics research branch" (based at the Aeronautical Research Laboratory at Wright Patterson Air Force Base).' The page uses neither 'Wright Air Development Center' nor 'WADC'. Source: History of the Institute of Field Physics (1955-1959), UNC Physics and Astronomy department history https://physics.unc.edu/home/department-history/section-ii/

Sources added to it: History of the Institute of Field Physics (1955-1959), UNC Physics and Astronomy department history, https://physics.unc.edu/home/department-history/section-ii/, dated 2026-09-02.

### George S. Trimble

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** In November 1955 he was a vice-president of Martin, not its chief executive, and the atom-bomb comparison he made was about time and not about money. Ansel Talbert's Herald Tribune series identifies him as 'vice-president in charge of advanced design planning of Martin Aircraft Corp.' and as 'organizing a new Research Institute for Advanced Study', and quotes him: 'I think we could do the job in about the time that it actually required to build the first atom bomb if enough trained scientific brain-power simultaneously began thinking about and working towards a solution.' Source: Ansel E. Talbert, New York Herald Tribune, 20 November 1955 caption and continuation p. 36 and 22 November 1955 continuation p. 10, page images at https://archive.org/download/talbert1ny/talbert1ny_djvu.txt and https://archive.org/download/talbert3ny/talbert3ny_djvu.txt

Sources added to it: Ansel E. Talbert, 'Conquest of Gravity Aim Of Top Scientists in U. S.', New York Herald Tribune, 20 November 1955, page image, https://archive.org/download/talbert1ny/talbert1ny_djvu.txt, dated 1955-11-20; Ansel E. Talbert, 'New Air Dream, Planes Flying Outside Gravity', New York Herald Tribune, 22 November 1955, page image, https://archive.org/download/talbert3ny/talbert3ny_djvu.txt, dated 1955-11-22.

### Gerald A. Smith

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### Glenn Gaffney

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 13 December 2024, at 0:22:48, Eric Davis said of Gaffney 'I think his title was deputy director of the CIA over the directorate of science and technology. And that's where the UAP portfolio is held.' Davis hedges the title himself. No record opened in this pass establishes either the title or the portfolio placement. Source: American Alchemy with Jesse Michels, 'CIA Scientist: George Bush Was Briefed on UFOs (ft. Eric Davis)', 13 December 2024, 0:22:48, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7341687364.mp3?updated=1752173868
- **Tier 2 named person on the record.** At 0:19:28 and 0:20:19 in the same episode Davis said he had no direct interaction with Gaffney but that the aerospace defence firm involved, and that firm's senior and executive vice presidents, did; and that Gaffney was 'very antagonistic' about that company releasing to them, under DIA classification, a collection of crash retrieval materials held by Bigelow Aerospace Advanced Space Studies and EarthTech since the 1989 shutdown. This is a second blocked transfer, distinct from the Lockheed to Bigelow transfer the node already carries. Source: American Alchemy with Jesse Michels, 'CIA Scientist: George Bush Was Briefed on UFOs (ft. Eric Davis)', 13 December 2024, 0:19:28 to 0:20:19
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 2 July 2026, Rep. Eric Burlison was asked whom in government he would most want to subpoena or question at length in a SCIF about UAP and named Gaffney first: 'I would say probably Glenn Gaffney who is you know former CIA a lot of people I talked to you say that this is somebody that we need to talk to.' He then named Steve Cantrell, described only as former Air Force senior intelligence, and General McCasland (1:48:44). Source: American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 1:48:44 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3

Sources added to it: American Alchemy with Jesse Michels, 'CIA Scientist: George Bush Was Briefed on UFOs (ft. Eric Davis)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7341687364.mp3?updated=1752173868, dated 2024-12-13; American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3, dated 2026-07-02.

### Harold E. Puthoff

Fields the record forced a change to: claims, cls, sequenceChain, sources.

The rebuilt sequence chain:

- 1972, Begins SRI International remote-viewing/psychoenergetics programme with Russell Targ under CIA and later DIA sponsorship. Source: CIA STARGATE declassified collection.
- 1978-01-01, Army/DIA effort formalised as GRILL FLAME. Source: no attributed source on file.
- 1995-01-01, CIA declassifies and releases the STARGATE corpus following the AIR evaluation; programme terminated. Source: CIA STARGATE declassified collection.
- 1995-01-01, Becomes a consultant to Robert Bigelow's newly founded National Institute for Discovery Science. Source: no attributed source on file.
- 2008-01-01, Principal investigator on Defense Intelligence Agency-funded advanced aerospace work through Bigelow's BAASS under AAWSAP. Source: no attributed source on file.
- 2017-10-11, Co-founds To The Stars Academy of Arts & Science with Tom DeLonge, Jim Semivan and Steve Justice. Source: no attributed source on file.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 22 November 2025, at 3:56:16 to 3:58:57, Peter Levenda said he spent a full day in a conference room in Austin, arranged by Tom DeLonge, with Chris Mellon, Harold Puthoff and Jacques Vallee. He said that when the group asked about a specific matter concerning Skinwalker Ranch, the equipment used there and the data collected, all three fell silent, and that Puthoff then said 'we need a skiff for this one' and would not say why. Levenda gives the account in the first person as a participant and says he took contemporaneous notes. Source: American Alchemy with Jesse Michels, 'CIA Historian: Aliens Control Our Government (ft. Peter Levenda)', 22 November 2025, 3:56:16 to 3:58:57, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1108723055.mp3?updated=1763834387

Sources added to it: American Alchemy with Jesse Michels, 'CIA Historian: Aliens Control Our Government (ft. Peter Levenda)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1108723055.mp3?updated=1763834387, dated 2025-11-22.

### Howard C. Cross

Fields the record forced a change to: sequenceChain.

The rebuilt sequence chain:

- 1952-01-01, Battelle running Project Stork analytical work for the Air Force on Blue Book data. Source: no attributed source on file.
- 1953-01-09, Writes the memorandum to Miles E. Goll at Wright-Patterson AFB, ref. G-1579-4, classified SECRET. Source: Text and provenance published by the Computer UFO Network (CUFON); Jacques Vallee, Forbidden Science.
- 1953-01-14, Robertson Panel convenes; per Vallee, it is not briefed on the Pentacle proposals. The board marks this step as the anomalous one. Source: Jacques Vallee, Forbidden Science (1992) and subsequent correspondence quoted by CUFON.
- 1967-06-18, Jacques Vallee finds the memo among J. Allen Hynek's papers and records it in his journal. Source: Text and provenance published by the Computer UFO Network (CUFON); Jacques Vallee, Forbidden Science.
- 1992-01-01, Vallee publishes an account in Forbidden Science, using the codename 'Pentacle'. Source: Text and provenance published by the Computer UFO Network (CUFON); Jacques Vallee, Forbidden Science.

### Dr Ítalo Venturelli

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 31 January 2026, forensic physician Dr Armando Fortunato said he performed the autopsy on the state military police soldier whose death followed the 1996 Varginha events, that the body arrived with no mention of extraterrestrial contact and was referred by the commanding colonel as a possible professional-error inquiry, and that the only lesion found was a drainage incision in the left armpit. He said tissue and blood samples went to a pathologist whose report gave death as a pulmonary infection causing septicaemia. Fortunato's stated position is that 'the first diagnostic hypothesis is still a secondary effect of surgery', with post-contact contamination a second hypothesis that 'shouldn't be ruled out' (3:09:19 to 3:15:48). Source: American Alchemy with Jesse Michels, '"I Spent 4 Minutes With A Living Alien!" -Top Neurosurgeon [Exclusive Interview]', 31 January 2026, 3:09:19 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL5466696236.mp3?updated=1769887132
- **Tier 2 named person on the record.** In the same passage Fortunato said the pathologist has recently stated that the bacteria found was not common in Brazil and extremely virulent, and is now applying to the court for authorisation to exhume the soldier's remains for DNA testing, which Fortunato said requires both the court's approval and the family's agreement. No case number, court or filing date is given (3:12:14 to 3:13:06). Source: American Alchemy with Jesse Michels, '"I Spent 4 Minutes With A Living Alien!" -Top Neurosurgeon [Exclusive Interview]', 31 January 2026, 3:12:14 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL5466696236.mp3?updated=1769887132

Sources added to it: American Alchemy with Jesse Michels, '"I Spent 4 Minutes With A Living Alien!" -Top Neurosurgeon [Exclusive Interview]', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL5466696236.mp3?updated=1769887132, dated 2026-01-31.

### J. Golightly

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### Jacques F. Vallee

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 25 October 2025, at 1:16:06 and 1:18:41, Michels said in narration that on 11 July 1961 Vallee, then working on the Paris Observatory's satellite tracking programme, and colleagues observed an object in retrograde orbit, and that his superior at the observatory, named as Paul Mueller, confiscated the tape the next morning and destroyed it. The narration also quotes Vallee from an unspecified later interview saying other observatories made the same observation and that American tracking stations photographed it and could not identify it either. No book, interview or archive is cited on air for either element. Source: American Alchemy with Jesse Michels, 'Top Astronomer: I Found 100,000 UFOs Above Earth! (ft. Beatriz Villarroel)', 25 October 2025, 1:16:06 and 1:18:41, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1307454785.mp3?updated=1761413167

Sources added to it: American Alchemy with Jesse Michels, 'Top Astronomer: I Found 100,000 UFOs Above Earth! (ft. Beatriz Villarroel)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1307454785.mp3?updated=1761413167, dated 2025-10-25.

### Jake Barber

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 30 January 2025, at 0:32:53, Jake Barber said that after 2001 he worked as a contractor for the intelligence community and that 'we had a cover contract through the BIA, which is the Bureau of Indian Affairs at a sovereign nation close to White Sands Missile Range in New Mexico'. He gives no contract number and names no company. Source: American Alchemy with Jesse Michels, 'UFO Crash Retrieval: Jake Barber's FIRSTHAND Account', published 30 January 2025, at 0:32:53
- **Tier 2 named person on the record.** In the same episode, between 0:54:51 and 0:55:41, Barber said that everything he was describing had been given to AARO and that it 'has been shared with Congress in a SCIF, in a top secret SCI environment, where I've given testimony'. He does not name the committee in this passage. Source: American Alchemy with Jesse Michels, 'UFO Crash Retrieval: Jake Barber's FIRSTHAND Account', published 30 January 2025, at 0:54:51 to 0:55:41
- **Tier 2 named person on the record.** In the same episode, between 2:04:48 and 2:06:33, Barber said that he and colleagues wrote a 120,000 word historical-fiction manuscript with a hired ghost writer and submitted it to the DOPSR review process in pieces, beginning with the first twenty pages, in order to 'red team the DOPSR process to expose who subject matter experts are' and to map who controls which information. He describes seeding the manuscript with four deliberately chosen categories of information as the probe. Source: American Alchemy with Jesse Michels, 'UFO Crash Retrieval: Jake Barber's FIRSTHAND Account', published 30 January 2025, at 2:04:48 to 2:06:33

Sources added to it: American Alchemy with Jesse Michels, 'UFO Crash Retrieval: Jake Barber's FIRSTHAND Account (ft. Logan Paul and Ammar Kandil)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE9340057376.mp3?updated=1751590405, dated 2025-01-30.

### James Wells

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### Jesse A. Marcel Sr.

Fields the record forced a change to: sequenceChain.

The rebuilt sequence chain:

- 1947-07-07, Travels to the Foster ranch with CIC Capt. Sheridan Cavitt and collects debris. Source: USAF, 'The Roswell Report: Fact vs. Fiction in the New Mexico Desert' (1995), which reproduces the Ramey office photographs and the Cavitt interview.
- 1947-07-08, Photographed in Gen. Roger Ramey's Fort Worth office with balloon and radar-target debris. Source: USAF, 'The Roswell Report: Fact vs. Fiction in the New Mexico Desert' (1995), which reproduces the Ramey office photographs and the Cavitt interview.
- 1978-02-20, Tells Stanton Friedman the balloon story was a cover and the material was unidentifiable. The board marks this step as the anomalous one. Source: Jesse Marcel Sr., interview with Stanton T. Friedman, February 1978.

### J. Albertine

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### John G. Cramer

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### John M. McHugh

Fields the record forced a change to: date, sources.

Its date is now set to 2009-01-06, derived from the record rather than assigned.

Sources added to it: U.S. Senate, Dates of Sessions of the Congress (convening dates: 111th 6 Jan 2009, 118th 3 Jan 2023, 119th 3 Jan 2025), https://www.senate.gov/legislative/DatesofSessionsofCongress.htm, dated 2026-08-22.

### Ken Calvert

Fields the record forced a change to: date, sources.

Its date is now set to 2023-01-03, derived from the record rather than assigned.

Sources added to it: U.S. Senate, Dates of Sessions of the Congress (convening dates: 111th 6 Jan 2009, 118th 3 Jan 2023, 119th 3 Jan 2025), https://www.senate.gov/legislative/DatesofSessionsofCongress.htm, dated 2026-08-22.

### Kirk McConnell

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 24 December 2024, at 1:49:10, Robert Hastings said that in January 2023 McConnell, whom he describes as 'a retired Senate Armed Service Committee investigator', contacted him and asked him to gather veterans with experiences at nuclear weapons sites for AARO to interview, and at 1:51:51 that 'it was 11 of roughly 20 who agreed to speak' with the office. The transcript renders the name Kurt McConnell throughout. Source: American Alchemy with Jesse Michels, 'UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)', 24 December 2024, 1:49:10 and 1:51:51, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4049919963.mp3?updated=1752173281
- **Tier 2 named person on the record.** In the same passage Hastings said McConnell emailed him in about March 2023 saying he had driven a veteran to that veteran's AARO interview, and relayed what the veteran said he had told AARO's then director about where a particular film was held. Hastings gives the account at two removes and names no document. Source: American Alchemy with Jesse Michels, 'UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)', 24 December 2024, 1:49:10
- **Tier 2 named person on the record.** McConnell is a primary source in this board's Michels corpus as well as a node in it. He gave a two-hour interview on American Alchemy with Jesse Michels published 2 April 2025, in which he supplies the account of AARO's advisory-group contract being let through Oak Ridge (1:09:33), the report of Puthoff's and Davis's scepticism about Tesla and Thomas Townsend Brown (0:19:36), and his own disagreement with the account that the FBI seized all of Tesla's papers, 'I don't think all of it did' (0:18:40). Claims elsewhere on this board sourced to that episode are sourced to him. Source: American Alchemy with Jesse Michels, 'Senate Staffer Thinks Tesla and Nazi Technology is Being Hidden (ft. Kirk McConnell)', published 2 April 2025, at 0:18:40, 0:19:36 and 1:09:33

Sources added to it: American Alchemy with Jesse Michels, 'UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4049919963.mp3?updated=1752173281, dated 2024-12-24; American Alchemy with Jesse Michels, 'Senate Staffer Thinks Tesla and Nazi Technology is Being Hidden (ft. Kirk McConnell)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9058812583.mp3?updated=1752174755, dated 2025-04-02.

### Lincoln LaPaz

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 25 October 2025, at 0:26:46 and 0:27:36, Michels said in narration that a military-funded project to search for small natural satellites of the Earth began at White Sands Missile Range in 1953, that LaPaz and Clyde Tombaugh were the two scientists in charge of it, and that LaPaz came to it from Project Twinkle. Neither Tombaugh nor the White Sands satellite search appears anywhere in the board's research files. Source: American Alchemy with Jesse Michels, 'Top Astronomer: I Found 100,000 UFOs Above Earth! (ft. Beatriz Villarroel)', 25 October 2025, 0:26:46, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1307454785.mp3?updated=1761413167
- **Tier 2 named person on the record.** In the same narration at 0:28:29 Michels said that on 23 August 1954 Aviation Week and Space Technology published a statement from LaPaz confirming two unknown objects in low Earth orbit while simultaneously describing them as fully identified natural asteroids captured by the Earth's gravity. The magazine issue was not opened in this pass, so the date and the wording are the speaker's and not the record's; the issue is named here so a later pass can pull it. Source: American Alchemy with Jesse Michels, 'Top Astronomer: I Found 100,000 UFOs Above Earth! (ft. Beatriz Villarroel)', 25 October 2025, 0:28:29

Sources added to it: American Alchemy with Jesse Michels, 'Top Astronomer: I Found 100,000 UFOs Above Earth! (ft. Beatriz Villarroel)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1307454785.mp3?updated=1761413167, dated 2025-10-25.

### Louis Witten

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 31 August 2025, at 2:07:12 and 2:08:06, Michels said that at the time of the Avro car project Wright Field also had 'a dedicated theoretical physics group' headed by a man the caption renders as 'Josh Goldberg', and that Agnew Bahnson, who ran the University of North Carolina's Institute of Field Physics with Bryce DeWitt, recorded in diaries found years later that he had been told to get in touch with Townsend Brown because he wanted to build a spaceship. Neither Goldberg nor Bahnson appears anywhere in the board's research files, the caption spells Bahnson 'Bonson', and no diary, archive or document is named on air. Source: American Alchemy with Jesse Michels, 'NASA Doctor: I Saw A UFO Hovering In THIS Secret Hangar (Ft. Greg Rogers)', 31 August 2025, 2:07:12, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2173204669.mp3?updated=1757589247

Sources added to it: American Alchemy with Jesse Michels, 'NASA Doctor: I Saw A UFO Hovering In THIS Secret Hangar (Ft. Greg Rogers)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2173204669.mp3?updated=1757589247, dated 2025-08-31.

### Louis Witten

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The January 1957 Chapel Hill conference had one sponsor and four funders, and the Air Force was not the sponsor. The report's title page reads: 'UNDER THE SPONSORSHIP OF THE International Union of Pure and Applied Physics, with financial support from UNESCO / National Science Foundation / Wright Air Development Center, U.S. Air Force / Office of Ordnance Research, U.S. Army'. The Foreword gives the reason the report exists at all: 'The present report was undertaken as a necessary requirement to obtain conference funds.' WADC's imprint is on the cover because the report was the condition of the money, not because the Air Force convened the meeting. Source: The Role of Gravitation in Physics: Report from the 1957 Chapel Hill Conference, WADC Technical Report 57-216, title page and Foreword by Cecile M. DeWitt, 15 March 1957, https://edition-open-sources.org/sources/5/5/index.html

Sources added to it: The Role of Gravitation in Physics: Report from the 1957 Chapel Hill Conference, the Edition Open Sources reissue of WADC Technical Report 57-216, Max Planck Institute for the History of Science, 2011, title page and Foreword, https://edition-open-sources.org/sources/5/5/index.html, dated 1957-03-01.

### Luis D. Elizondo

Fields the record forced a change to: sequenceChain.

The rebuilt sequence chain:

- 2017-08-09, Submits DD Form 1910 seeking public-release clearance for three .mpg files: 'GoFast', 'Gimbal' and 'FLIR'. Source: DD Form 1910 released via FOIA, published by Blue Blurry Lines, 17 August 2019.
- 2017-08-24, DD Form 1910 approved. Source: DD Form 1910 released via FOIA, published by Blue Blurry Lines, 17 August 2019.
- 2017-10-03, Submits first resignation letter as Director, National Programs Special Management Staff, requesting deferred retirement. Source: Elizondo resignation letter dated 3 October 2017, released in OSD/JS FOIA case 18-F-0324 (final response 17 August 2022).
- 2017-10-04, Resignation effective; hand-delivers second letter addressed 'Mr. Secretary' protesting Departmental inaction on UAP. Source: Elizondo resignation letter dated 3 October 2017, released in OSD/JS FOIA case 18-F-0324 (final response 17 August 2022).
- 2017-10-11, Announced as Director of Global Security & Special Programs at To The Stars Academy launch. Source: no attributed source on file.
- 2017-12-16, Named in the New York Times 'Glowing Auras and Black Money' as the official who ran AATIP. Source: Elizondo statements to the New York Times, 16 December 2017, and subsequently.

### Marc G. Millis

Fields the record forced a change to: date.

Its date is now set to 2010-11-01, derived from the record rather than assigned.

### Michael Powers

Fields the record forced a change to: claims, date, sources.

Its date is now set to 2026-05-20, derived from the record rather than assigned.

Claims the record added:

- **Tier 1 documented.** The OSD Historical Office's Key Officials list of 7 July 2026 records Michael Powers as Acting Under Secretary of War (Comptroller)/Chief Financial Officer from 20 May 2026 to present, succeeding Jules W. Hurst III, who performed the duties of the office from 5 September 2025 to 20 May 2026. Source: OSD Historical Office, Key Officials September 1947-July 2026 (7 July 2026), https://history.defense.gov/Portals/70/Documents/key_officials/KeyOfficials-2026-07-07.pdf
- **Tier 1 documented.** The same list records Powers as Deputy Under Secretary of Defense (Comptroller) from 23 December 2025 to present, so he holds the deputy office and the acting principal office at once. Source: OSD Historical Office, Key Officials September 1947-July 2026 (7 July 2026), https://history.defense.gov/Portals/70/Documents/key_officials/KeyOfficials-2026-07-07.pdf
- **Tier 1 documented.** Two Department pages disagree on who holds the office. The Department of War comptroller site's leadership page names Jules W. Hurst III as Under Secretary of War (Comptroller)/CFO, while war.gov's own biography of Powers opens 'The Honorable Michael Powers currently serves as the Acting Under Secretary of War (Comptroller) and Chief Financial Officer (CFO).' The Historical Office list dates the handover to 20 May 2026, which makes the comptroller site's leadership page the stale one. Source: comptroller.war.gov leadership page and https://www.war.gov/About/Biographies/Biography/Article/4503523/michael-t-powers/, both read 22 August 2026, against the Key Officials list of 7 July 2026

Sources added to it: OSD Historical Office, 'Department of Defense Key Officials, September 1947 - July 2026' (7 July 2026), Under Secretaries of Defense (Comptroller), https://history.defense.gov/Portals/70/Documents/key_officials/KeyOfficials-2026-07-07.pdf, dated 2026-07-07; Department of War, official biography of Michael T. Powers, https://www.war.gov/About/Biographies/Biography/Article/4503523/michael-t-powers/, dated 2026-08-22.

### Mike Rogers (Alabama)

Fields the record forced a change to: date, sources.

Its date is now set to 2023-01-03, derived from the record rather than assigned.

Sources added to it: U.S. Senate, Dates of Sessions of the Congress (convening dates: 111th 6 Jan 2009, 118th 3 Jan 2023, 119th 3 Jan 2025), https://www.senate.gov/legislative/DatesofSessionsofCongress.htm, dated 2026-08-22.

### Brigadeiro Octávio Júlio Moreira Lima

Fields the record forced a change to: affiliations.

Affiliations rewritten as prose rather than as raw identifiers: fab, Ministério da Aeronáutica.

### Patty Murray

Fields the record forced a change to: date, sources.

Its date is now set to 2023-01-03, derived from the record rather than assigned.

Sources added to it: U.S. Senate, Dates of Sessions of the Congress (convening dates: 111th 6 Jan 2009, 118th 3 Jan 2023, 119th 3 Jan 2025), https://www.senate.gov/legislative/DatesofSessionsofCongress.htm, dated 2026-08-22.

### Paul Frederick Bennewitz

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 5 July 2025, at 0:36:14, Greg Bishop said that Doty told him, and he thinks Moore told him, that the Air Force flew Bennewitz by helicopter from Kirtland to Archuleta Mesa on the Jicarilla Apache reservation and showed him a site, and that jeeps, water tanks 'and all kind of stuff' had been placed there as props so his attention would move away from Kirtland. At 0:37:25 he said something did later crash there, that Bennewitz reached the site only after it had been cleaned up, and that what was found was burned ground, broken brush and a pen marked US government property. Nothing in the board's files mentions Archuleta. Source: American Alchemy with Jesse Michels, 'Fake Alien Signals Drove Him Insane... (ft. Greg Bishop)', 5 July 2025, 0:36:14 and 0:37:25, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6921419786.mp3?updated=1752608918
- **Tier 2 named person on the record.** At 0:34:30 in the same episode Bishop said that in his own reading Bennewitz 'was his own worst enemy' and that the specific thing he knows Bill Moore did was to be told to give Bennewitz the Aquarius document, in which two of Bennewitz's own films are mentioned. The author of the standard account is on the record limiting what he says was actually done to the man. Source: American Alchemy with Jesse Michels, 'Fake Alien Signals Drove Him Insane... (ft. Greg Bishop)', 5 July 2025, 0:34:30

Sources added to it: American Alchemy with Jesse Michels, 'Fake Alien Signals Drove Him Insane... (ft. Greg Bishop)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6921419786.mp3?updated=1752608918, dated 2025-07-05.

### Paul A. Czysz

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### Brigadeiro do Ar José Pessoa Cavalcanti de Albuquerque

Fields the record forced a change to: affiliations.

Affiliations rewritten as prose rather than as raw identifiers: fab, Brazilian Air Defence Command (COMDA).

### General de Brigada Aérea (A) Ricardo Bermúdez Sanhueza

Fields the record forced a change to: affiliations.

Affiliations rewritten as prose rather than as raw identifiers: cefaa, dgac-chile, Fuerza Aérea de Chile (FACh).

### Richard C. Doty

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 5 July 2025, at 0:23:44 to 0:24:30, the episode describes the 1977 Ellsworth Air Force Base case of missile security officer Mario Woods and cuts in Woods's own voice saying of his debrief 'Next to him was this new OSI guy named Rick Doty', and later that when he saw him again on television he thought 'I know that guy. He was at my debrief.' Michels and Greg Bishop then date it to a year or two before the Bennewitz operation. The transcript renders the name Dodi and Dodie throughout. Source: American Alchemy with Jesse Michels, 'Fake Alien Signals Drove Him Insane... (ft. Greg Bishop)', 5 July 2025, 0:23:44 to 0:24:30, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6921419786.mp3?updated=1752608918

Sources added to it: American Alchemy with Jesse Michels, 'Fake Alien Signals Drove Him Insane... (ft. Greg Bishop)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6921419786.mp3?updated=1752608918, dated 2025-07-05.

### Richard J. Genik II

Fields the record forced a change to: date.

Its date is now set to 2010-12-15, derived from the record rather than assigned.

### Richard K. Obousy

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### Robert M. L. Baker, Jr.

Fields the record forced a change to: date.

Its date is now set to 2010-04-06, derived from the record rather than assigned.

### Robert T. Bigelow

Fields the record forced a change to: sequenceChain.

The rebuilt sequence chain:

- 1995-01-01, Founds the National Institute for Discovery Science. Source: Gideon Lewis-Kraus, The New Yorker, 10 May 2021, quoting NIDS' own description.
- 1996-01-01, Purchases the 480-acre Sherman ranch in Uintah County, Utah, with non-disclosure conditions on the sellers. Source: Gideon Lewis-Kraus, The New Yorker, 10 May 2021, quoting NIDS' own description.
- 2008-09-22, BAASS awarded DIA contract HHM402-08-C-0072. Source: DIA contract release FOIA-00349-2018, released 13 Oct 2022.
- 2009-07-01, BAASS delivers the 494-page Ten Month Report to DIA. Source: no attributed source on file.

### Robert L. Hastings

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 19 October 2024, at 0:34:57, Michels gave Hastings's figure as '167 UFO sighting cases at nuclear bases', and in the same breath as '167 ICBM security personnel, radar operators, people who work at these nuclear sites'. On 24 December 2024 at 2:07:40, with Hastings present, he described the same body of testimony as 'almost 200 stand-up patriots'. Source: American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:34:57, and 'UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)', 24 December 2024, 2:07:40
- **Tier 2 named person on the record.** On the same show on 27 January 2025 at 3:07:08 Michels said he had overstated the case and that Hastings emailed him a correction: 'it was only like 12 to 15. I don't remember the exact number. But radar operators, the rest were ICBM security personnel'. In the same passage he gives the overall total as 170. The correction concerns the composition of the witness population, not only its size. Source: American Alchemy with Jesse Michels, 'UFO Believer vs. UFO Skeptic: Are Aliens Visiting Earth?' (ft. Mick West and Marik von Rennenkampff), 27 January 2025, 3:07:08, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE9180015195.mp3?updated=1738087523

Sources added to it: American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004, dated 2024-10-19; American Alchemy with Jesse Michels, 'UFOs Are Monitoring Nuclear Weapons GLOBALLY (ft. Robert Hastings)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4049919963.mp3?updated=1752173281, dated 2024-12-24; American Alchemy with Jesse Michels, 'UFO Believer vs. UFO Skeptic: Are Aliens Visiting Earth?' (ft. Mick West and Marik von Rennenkampff) (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE9180015195.mp3?updated=1738087523, dated 2025-01-27.

### Robert J. Low

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 12 July 2025, at 0:38:48 and 0:42:21, Robert Salas said he holds a handwritten note by Low recording that Low had spoken to the Air Force colonel the caption renders as 'Hitler', and that the colonel said the Air Force thought EMP from nuclear testing caused the Malmstrom shutdowns and that the matter was probably too highly classified for the Colorado project to look at. Salas says twice 'I've got it in writing'. The note is not published and was not opened here. Source: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:38:48 and 0:42:21, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599
- **Tier 1 documented.** Low replied to Hippler on 27 January 1967, copying Condon: 'On the second page, you indicate what you believe the Air Force wants of us, and I am very glad to have your opinion.' He adds that Hippler has 'answered quite directly the question that I asked' and that he had come back to that question a couple of times at their meeting on Thursday evening, 12 January. The project coordinator who wrote the 9 August 1966 trick memo is on the record five months later asking the Air Force what it wanted and thanking it for the answer. Source: Robert J. Low to Lt Col Robert Hippler, 27 January 1967, University of Colorado, page 2, https://www.nicap.org/docs/HipplerLetters.pdf

Sources added to it: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599, dated 2025-07-12; Hippler to Condon, 16 January 1967, with Low to Hippler, 27 January 1967 (NICAP document archive scan), https://www.nicap.org/docs/HipplerLetters.pdf, dated 1967-01-27.

### Capt. Robert L. Salas

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 12 July 2025, at 0:58:13, Salas said he did not learn his own incident was at Oscar Flight rather than Echo Flight until 1996, when he reached his former commander Fred Meiwald, who told him 'we were not at Echo Flight. We were at Oscar flight'. Salas says he had spoken of the Echo Flight incident as his own because it was so similar to what he recalled. This is his own account of the discrepancy the board's node already records. Source: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:58:13, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 9 February 2026, Michels said that Strategic Air Command 'wrote up a whole write up saying we're baffled and confused' about the Echo Flight incident, which he placed eight days before the Oscar Flight shutdown, and that targeting officer Bob Jamison went in to check why the ten missiles went down (0:19:06). No document number, date or addressee is given for the SAC write-up. Source: American Alchemy with Jesse Michels, 'Meet the Nuclear Missile Guard Abducted by Aliens', 9 February 2026, 0:19:06 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9102178952.mp3?updated=1770679988

Sources added to it: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599, dated 2025-07-12; American Alchemy with Jesse Michels, 'Meet the Nuclear Missile Guard Abducted by Aliens', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9102178952.mp3?updated=1770679988, dated 2026-02-09.

### Robert I. Sarbacher

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 19 October 2024, at 0:33:16, Michels said that David Grusch identifies the people who set up the secrecy protocols for UFOs as Robert J. Oppenheimer and Sarbacher, and that the two are 'responsible for the 1954 Atomic Energy Commission which overlaid nuclear secrecy on top of UFO secrecy'. The claim is Michels relaying Grusch, it concerns 1954 rather than the period the 1983 letter covers, and no document is cited for it on air. Source: American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:33:16, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 23 April 2025, at 0:23:09, Michels said that Sarbacher told Stanton Friedman that MIT president Karl Compton 'was briefed on UFO technology at Wright Airfield in 1950', and at 0:24:00 that when John Greenewald used the Freedom of Information Act to retrieve Compton's records he received a reply in April 2014 stating that 'records which may have been responsive to your request were destroyed August 30th, 2006'. The FOIA response letter itself was not opened from this environment. Source: American Alchemy with Jesse Michels, 'Presidential Advisor: I Directly Handled UFO Material (Ft. Harald Malmgren)', published 23 April 2025, at 0:23:09 and 0:24:00
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 7 February 2025, between 0:13:20 and 0:14:59, Whitley Strieber said that Stanton Friedman introduced him to Sarbacher, that Sarbacher asked him to write his experience down and send it, that he did so by UPS overnight in 1986, and that the next morning the UPS driver told him 'we can't deliver it. The recipient has expired.' At 0:15:49 Strieber adds that he was told Sarbacher fell off his boat and that the death certificate says natural causes. This is Strieber's first-hand account of his own correspondence and no record of the letter or its return was opened. Source: American Alchemy with Jesse Michels, 'Whitley Strieber: Aliens Live Among Us (Exclusive Interview)', published 7 February 2025, at 0:13:20 to 0:15:49
- **Tier 2 named person on the record.** In the same episode, at 0:18:16, Michels said that when Thomas Townsend Brown 'finally achieved positive result with his anti-gravity experiments, this was in Paris', Brown flew back to the United States and 'Robert Sarbacher picks him up in his big Cadillac', attributing the account to Brown's daughter Linda and to the biographer Paul Shatzkin. This is a second-hand attribution, and neither the daughter's account nor the biography was opened. Source: American Alchemy with Jesse Michels, 'Whitley Strieber: Aliens Live Among Us (Exclusive Interview)', published 7 February 2025, at 0:18:16

Sources added to it: American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004, dated 2024-10-19; American Alchemy with Jesse Michels, 'Presidential Advisor: I Directly Handled UFO Material (Ft. Harald Malmgren)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1090282889.mp3?updated=1752180350, dated 2025-04-23; American Alchemy with Jesse Michels, 'Whitley Strieber: Aliens Live Among Us (Exclusive Interview)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE6390612252.mp3?updated=1751926843, dated 2025-02-07.

### Rosa L. DeLauro

Fields the record forced a change to: date, sources.

Its date is now set to 2023-01-03, derived from the record rather than assigned.

Sources added to it: U.S. Senate, Dates of Sessions of the Congress (convening dates: 111th 6 Jan 2009, 118th 3 Jan 2023, 119th 3 Jan 2025), https://www.senate.gov/legislative/DatesofSessionsofCongress.htm, dated 2026-08-22.

### Roscoe H. Hillenkoetter

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The founding proposal for Project BLUEBIRD went to him as Director of Central Intelligence. The memorandum of 5 April 1950 from the Chief of the CIA's Inspection and Security Staff is addressed to the Director of Central Intelligence and says on its face: 'In view of the extreme sensitivity of this project and its covert nature, it is deemed advisable to submit this project directly to you, rather than through the channel of the Projects Review Committee. Knowledge of this project should be restricted to the absolute minimum number of persons.' It asks him for approval and for an allocation of $65,515. Source: Chief, Inspection and Security Staff, CIA, to the Director of Central Intelligence, 'Project Bluebird', Top Secret, 5 April 1950, CIA-RDP83-01042R000800010003-1, National Security Archive John Marks Collection Box 9, https://nsarchive.gwu.edu/sites/default/files/documents/1950-04-05%20JM%20Box%209%20F5%20Replacement%20CIA%20FOIA-ocr.pdf
- **Tier 2 named person on the record.** The Director on that date was Hillenkoetter. The memorandum itself names only the office; the National Security Archive's catalogue record for it names him as the recipient, and this node already dates his tenure as DCI from May 1947 to October 1950 on a CIA-held clipping. The identification is Tier 2 because the document does not make it. Source: National Security Archive catalogue record for the 5 April 1950 Project Bluebird memorandum, https://nsarchive.gwu.edu/document/32717-document-02-chief-inspection-and-security-staff-us-central-intelligence-agency

Sources added to it: Chief, Inspection and Security Staff to the Director of Central Intelligence, 'Project Bluebird', Top Secret, 5 April 1950 (CIA-RDP83-01042R000800010003-1), https://nsarchive.gwu.edu/sites/default/files/documents/1950-04-05%20JM%20Box%209%20F5%20Replacement%20CIA%20FOIA-ocr.pdf, dated 1950-04-05; National Security Archive catalogue record for the 5 April 1950 Project Bluebird memorandum, https://nsarchive.gwu.edu/document/32717-document-02-chief-inspection-and-security-staff-us-central-intelligence-agency, dated 2026-09-03.

### Salvatore Cezar Pais

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 2 July 2026, Rep. Eric Burlison described an official visit to NAS Patuxent River at which he asked for and was granted a meeting with Pais, went down the list of the patents, and was told that one of them had been built and tested but that no definitive result was obtained. Burlison said Pais's position was 'that was not built to his specifications', and that Dr. Jon Kosloski was present and was the only other person in the room following the physics (0:36:49 to 0:39:35). Burlison hedged which patent was tested, saying only 'I believe the anti-gravitic one'. Source: American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 0:36:49 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3
- **Tier 2 named person on the record.** In the same episode Jesse Michels, not Burlison, described Pais as fearful and hard to reach, said he had interviewed him in a motel near Pax River during which a camera failed, and said Pais stopped him at a point in the science with 'Jesse, stop right there' and declined to discuss it further (0:37:47 to 0:38:43). The lead map for this corpus attributes this account to Burlison; the transcript attributes it to Michels. Source: American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 0:37:47 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3

Sources added to it: American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3, dated 2026-07-02.

### Sean M. Kirkpatrick

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record, allegation shaped wording as stored.** On American Alchemy with Jesse Michels, 30 January 2025, at 1:28:12, Jake Barber said that the Michael Herrera incident and his own additional information were presented to AARO under Sean Kirkpatrick, that Kirkpatrick 'patently denied it and wrote it off', and that 'I know for a fact that Sean Kirkpatrick has admitted outside of the office of AARO directly to members of the Senate Intelligence Committee that it did in fact happen exactly as reported by Michael Herrera'. This is a claim about what an AARO director is said to have said in private, not a claim sourced to AARO, and no record of either the denial or the private confirmation was opened. Source: American Alchemy with Jesse Michels, 'UFO Crash Retrieval: Jake Barber's FIRSTHAND Account', published 30 January 2025, at 1:28:12
- **Tier 2 named person on the record, allegation shaped wording as stored.** On American Alchemy with Jesse Michels, 2 April 2025, at 1:09:33, Kirk McConnell said that Kirkpatrick 'created an advisory group' at AARO and that 'the contract for that, for the formation of that group to advise him at AARO, well, the contract was let through Oak Ridge', and that after retiring from government Kirkpatrick is 'working with, for Oak Ridge under contract now'. Asked whether that looked like a conflict of interest, McConnell answered at 1:10:25 that 'conflicts of interest or allegations are easy to make, but not so easy to sort out. But it is certainly worth taking note of if nothing else.' He does not allege wrongdoing and does not name the advisory group. Source: American Alchemy with Jesse Michels, 'Senate Staffer Thinks Tesla and Nazi Technology is Being Hidden (ft. Kirk McConnell)', published 2 April 2025, at 1:09:33 to 1:10:25
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 26 July 2026, Skinwalker Ranch owner Brandon Fugal said that Kirkpatrick 'claimed that before 2022 he had no interest in these topics, that he'd never attended a briefing on Skinwalker Ranch', and that he had never met Fugal. Fugal said Kirkpatrick sat across from him for two and a half hours at a confidential briefing in April 2018 devoted to the investigation and findings at the ranch, and that after being challenged by Steven Greenstreet of the New York Post he published a photograph of Kirkpatrick in attendance to Twitter, LinkedIn, Instagram and Facebook (2:39:07 to 2:41:12). Source: American Alchemy with Jesse Michels, '"There's A UFO Under the Ranch!" - Skinwalker Owner Breaks Silence', 26 July 2026, 2:39:07 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9910649891.mp3

Sources added to it: American Alchemy with Jesse Michels, 'UFO Crash Retrieval: Jake Barber's FIRSTHAND Account (ft. Logan Paul and Ammar Kandil)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE9340057376.mp3?updated=1751590405, dated 2025-01-30; American Alchemy with Jesse Michels, 'Senate Staffer Thinks Tesla and Nazi Technology is Being Hidden (ft. Kirk McConnell)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9058812583.mp3?updated=1752174755, dated 2025-04-02; American Alchemy with Jesse Michels, '"There's A UFO Under the Ranch!" - Skinwalker Owner Breaks Silence', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9910649891.mp3, dated 2026-07-26.

### Sean Parnell

Fields the record forced a change to: claims, sources.

Claims the record added:

- **Tier 1 documented.** A Department of War release dated 18 March 2026 names Sean Parnell as 'Chief Pentagon Spokesman' in its own title: 'Statement by Chief Pentagon Spokesman Sean Parnell on ‘Strengthening the Effectiveness of Our Senior Service Colleges’'. Source: https://www.war.gov/News/Releases/Release/Article/4437252/statement-by-chief-pentagon-spokesman-sean-parnell-on-strengthening-the-effecti/

Sources added to it: Department of War release, 'Statement by Chief Pentagon Spokesman Sean Parnell on ‘Strengthening the Effectiveness of Our Senior Service Colleges’', 18 March 2026, https://www.war.gov/News/Releases/Release/Article/4437252/statement-by-chief-pentagon-spokesman-sean-parnell-on-strengthening-the-effecti/, dated 2026-03-18.

### Sergey O. Macheret

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### Steven H. Schiff

Fields the record forced a change to: sequenceChain.

The rebuilt sequence chain:

- 1993-01-01, Begins seeking Roswell records from the Department of Defense after constituent inquiries. Source: no attributed source on file.
- 1994-03-01, Directs GAO to conduct a records search; GAO work begins. Source: GAO/NSIAD-95-187, letter of transmittal and scope section.
- 1994-09-08, Air Force issues its report attributing the Roswell debris to Project MOGUL. Source: no attributed source on file.
- 1995-07-28, GAO/NSIAD-95-187 issued, reporting the destruction of RAAF records without disposition authority. The board marks this step as the anomalous one. Source: GAO/NSIAD-95-187, p.3.

### Susan M. Collins

Fields the record forced a change to: date, sources.

Its date is now set to 2023-01-03, derived from the record rather than assigned.

Sources added to it: U.S. Senate, Dates of Sessions of the Congress (convening dates: 111th 6 Jan 2009, 118th 3 Jan 2023, 119th 3 Jan 2025), https://www.senate.gov/legislative/DatesofSessionsofCongress.htm, dated 2026-08-22.

### Susan Gough

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record, allegation shaped wording as stored.** On American Alchemy with Jesse Michels, 13 June 2025, at 0:00:49, Michels said Gough was one of the primary sources of the Wall Street Journal article on Pentagon disinformation and UFO mythology, and alleged that her own LinkedIn profile 'along with independent sources' confirms a lead role in Booz Allen Hamilton's psychological operations consulting practice for the Department of Defense, her self-professed skills including strategic communication and psychological operations. The allegation rests on the speaker's reading of a profile page. No employment record was opened in this pass and nothing in the board's files corroborates it. Source: American Alchemy with Jesse Michels, 'The Wall Street Journal Is Gaslighting You On UFOs', 13 June 2025, 0:00:49, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL4839772690.mp3?updated=1750950332
- **Tier 2 named person on the record.** AARO is examining over 2,000 UAP cases; approximately 1,000 reports lack sufficient data for analysis and remain in AARO's Active Archive for potential future review. Source: Sue Gough, quoted by DefenseScoop, 25 February 2026
- **Tier 2 named person on the record.** The Department stated it has no record of a programme called Immaculate Constellation. Source: DoD statements attributed to Sue Gough in UAP coverage following the November 2024 hearing
- **Tier 3 stated inference.** A holding in which roughly half the reports are unanalysed for want of data is a holding that cannot support the department's own repeated negative finding, since the negative finding is drawn only from the analysed half. Source: Inference from Gough's February 2026 figures set against the FY2024 and FY2025 report conclusions

Sources added to it: American Alchemy with Jesse Michels, 'The Wall Street Journal Is Gaslighting You On UFOs' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL4839772690.mp3?updated=1750950332, dated 2025-06-13; DefenseScoop - Hegseth doubles down on Trump's UAP disclosure promise as AARO's caseload exceeds 2,000, https://defensescoop.com/2026/02/25/hegseth-ufo-disclosure-trump-aaro-uap-caseload/, dated 2026-02-25; AARO - FY2025 Consolidated Annual Report on UAP (PDF), https://documents2.theblackvault.com/documents/osd/AARO_FY2025_Consolidated_Annual_Report_on_UAP.pdf, dated 2026-07-21.

### Thad Cochran

Fields the record forced a change to: date, sources.

Its date is now set to 2009-01-06, derived from the record rather than assigned.

Sources added to it: U.S. Senate, Dates of Sessions of the Congress (convening dates: 111th 6 Jan 2009, 118th 3 Jan 2023, 119th 3 Jan 2025), https://www.senate.gov/legislative/DatesofSessionsofCongress.htm, dated 2026-08-22.

### Thomas Townsend Brown

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 19 October 2024, Michels said at 0:27:32 that the British aerospace journalist Bill Gunston, writing in Air International magazine in 2000, stated he was very sure Brown's work made it into the B-2 stealth bomber, and that Gunston added he had no wish to reside in the Tower of London. This is the named, dated source for the B-2 attribution the board otherwise carries without an author. Source: American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:27:32, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004
- **Tier 2 named person on the record.** In the same episode at 0:24:12 Michels named Brown's Santa Monica operation of the 1950s as 'guidance technologies' and placed Bill Lear's office across the street from it. Neither the operation's name nor the Santa Monica location appears in the board's record of Brown. Source: American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?', 19 October 2024, 0:24:12, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004
- **Tier 2 named person on the record.** Two speakers on separate episodes tell the same Rickover anecdote. On 6 December 2024 at 0:29:08 Michels, citing the writer Paul LaViolette, said Brown went to Hyman Rickover and Rickover told him to stop wasting his time. On 14 December 2024 at 0:52:55 Bob McGwire gave the same story with Rickover answering 'don't waste your time. We're already on it.' Neither speaker cites a document. Source: American Alchemy with Jesse Michels, 'Navy Fighter Pilots Witness UFO Mid Flight (Ft. Ryan Graves)', 6 December 2024, 0:29:08, and 'CIA Contractor: Obama Received An Alien Prophecy (ft. Bob McGwire)', 14 December 2024, 0:52:55
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 2 April 2025, at 0:19:36, the retired Senate Armed Services Committee staffer Kirk McConnell said of his own field: 'my science friends in the UAP field, like Dr. Harold Puthoff and Eric Davis, I'm sure if they're watching this, they're very upset with me because I don't think they believe that Tesla, nor Thomas Townsend Brown or others like them' achieved what is claimed of them. This is a report of scepticism from inside the advocate circle rather than from an interested official source, and neither Puthoff nor Davis is quoted directly. Source: American Alchemy with Jesse Michels, 'Senate Staffer Thinks Tesla and Nazi Technology is Being Hidden (ft. Kirk McConnell)', published 2 April 2025, at 0:19:36
- **Tier 1 documented.** The released FBI file on Brown, FOI/PA# 1496195-000, contains no statement that Brown knew more about radar detection than any individual in the US Navy. Its only two references to radar are a Los Angeles Times article of 4 July 1948 reporting that 'During World War II he headed the U. S. Navy's Atlantic Fleet Radar School', and an informant's account that 'BROWN claims to have been a lieutenant commander in the Navy during the war, one of his principal jobs being the administration of the Atlantic Fleet Radar School.' Three American Alchemy episodes attribute the radar superlative to a 1942 or 1943 FBI file; it is not in the file this board cites. Source: FBI file on Thomas Townsend Brown, FOI/PA# 1496195-000, full-text search https://archive.org/download/tt-brown/E65ffaeec360d48a08a97fb70305b58f18aac8f13_Q104175_R432679_D2722930_20231226_132723_djvu.txt
- **Tier 1 documented.** The same file summarises the 1942 Navy separation as follows: 'The current investigation has developed much information on BROWN, including that he was dismissed from the U. S. Navy Reserve in 1942 "for the good of the Service and to escape general court martial".' Source: FBI file on Thomas Townsend Brown, FOI/PA# 1496195-000, investigative summary https://archive.org/download/tt-brown/E65ffaeec360d48a08a97fb70305b58f18aac8f13_Q104175_R432679_D2722930_20231226_132723_djvu.txt
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 5 October 2024, the narration of the Townsend Brown documentary said that when Tom Valone of the Integrity Research Institute tried to locate a copy of a 1952 Naval Research Laboratory appraisal of Brown's experiments titled 'The TT Brown Electrogravity Device', the laboratory no longer had it (0:22:15). Source: American Alchemy with Jesse Michels, 'The CIA Scientist Who Cracked Antigravity (Townsend Brown Documentary)', 5 October 2024, 0:22:15 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4979487868.mp3?updated=1751926015

Sources added to it: American Alchemy with Jesse Michels, 'Did Oppenheimer Work on UFOs?' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE7249545573.mp3?updated=1751915004, dated 2024-10-19; American Alchemy with Jesse Michels, 'Navy Fighter Pilots Witness UFO Mid Flight (Ft. Ryan Graves)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE5314927973.mp3?updated=1752173951, dated 2024-12-06; American Alchemy with Jesse Michels, 'CIA Contractor: Obama Received An Alien Prophecy (ft. Bob McGwire)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE8690011428.mp3?updated=1752173727, dated 2024-12-14; American Alchemy with Jesse Michels, 'Senate Staffer Thinks Tesla and Nazi Technology is Being Hidden (ft. Kirk McConnell)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9058812583.mp3?updated=1752174755, dated 2025-04-02; FBI file on Thomas Townsend Brown, FOI/PA# 1496195-000, full text, https://archive.org/download/tt-brown/E65ffaeec360d48a08a97fb70305b58f18aac8f13_Q104175_R432679_D2722930_20231226_132723_djvu.txt, dated 2026-09-02; American Alchemy with Jesse Michels, 'The CIA Scientist Who Cracked Antigravity (Townsend Brown Documentary)', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE4979487868.mp3?updated=1751926015, dated 2024-10-05.

### Timothy Gallaudet

Fields the record forced a change to: sequenceChain.

The rebuilt sequence chain:

- 2015-01-01, Receives the 'URGENT SAFETY OF FLIGHT ISSUE' email from the Fleet Forces Command operations officer carrying the GO FAST video. Source: Tim Gallaudet, written testimony, House Oversight joint subcommittee hearing, 13 November 2024.
- 2015-01-02, Says the email vanished from his and other recipients' accounts the following day. The board marks this step as the anomalous one. Source: Tim Gallaudet, written testimony, House Oversight, 13 November 2024.
- 2024-11-13, Testifies to House Oversight joint subcommittees about the recalled email. Source: Tim Gallaudet, written testimony, House Oversight joint subcommittee hearing, 13 November 2024.

### Tom Cole

Fields the record forced a change to: date.

Its date is now set to 2024-04-10, derived from the record rather than assigned.

### Travis S. Taylor

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 26 July 2026, Brandon Fugal said the Skinwalker Ranch team did not know Taylor had been made chief scientist of the UAP Task Force while he was returning seasonally to work on the ranch investigation, that Taylor was under national security oaths and confidentiality and 'didn't breach that not even once', and that the team learned only once he had authorisation to disclose it. Fugal said members of his team, including his head of security, initially felt betrayed (2:17:46 to 2:18:44). Source: American Alchemy with Jesse Michels, 'There's A UFO Under the Ranch!' - Skinwalker Owner Breaks Silence, 26 July 2026, 2:17:46 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9910649891.mp3
- **Tier 2 named person on the record.** In the same episode Fugal stated the direction of the connection: that the reason Taylor 'was called in and called to that position in large part was was really because of uh the work at' Skinwalker Ranch, and that before being brought to the ranch Taylor had no experience of the subject and was a vocal skeptic (2:16:52, 2:19:37). Source: American Alchemy with Jesse Michels, 'There's A UFO Under the Ranch!' - Skinwalker Owner Breaks Silence, 26 July 2026, 2:19:37 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9910649891.mp3

Sources added to it: American Alchemy with Jesse Michels, 'There's A UFO Under the Ranch!' - Skinwalker Owner Breaks Silence, episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9910649891.mp3, dated 2026-07-26.

### 'UAP Gerb' (Sam)

Fields the record forced a change to: sequenceChain.

### 'UAP Gerb' (Sam)

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented, allegation shaped wording as stored.** The federal literature on nitinol, one report of it written by Battelle itself, does not support a Battelle 1948-49 lineage for the alloy. NASA SP-5110, prepared for NASA by Battelle Memorial Institute in 1972, opens: 'Some 10 years ago, Buehler and Wiley of the U.S. Naval Ordnance Laboratory developed a series of engineering alloys that possess a unique mechanical (shape) memory. The generic name of the series of alloys is 55-Nitinol, where Nitinol stands for Nickel Titanium Naval Ordnance Laboratory.' The earliest Naval Ordnance Laboratory nitinol report cited anywhere in its reference list is NOLTR 61-75 of 3 August 1961; US Patent 3,174,851 was filed on 1 December 1961; and NASA CR-1433 of September 1969 records Battelle's own role as a subcontractor to Goodyear Aerospace which 'processed the basic Nitinol rod'. The allegation that Wright-Patterson-sponsored Battelle reports on nickel-titanium alloy from 1948-49 are missing from Air Force and Battelle archives is kept on this board as the allegation it is, and is unsupported by the federal literature opened here. Source: NASA SP-5110, 55-Nitinol: The Alloy With a Memory, Battelle Memorial Institute for NASA, 1972, chapter 1 p. 1 and references 12 and 74, https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf ; NASA CR-1433, Nitinol Characterization Study, September 1969, foreword p. iii and p. 2, https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf ; US Patent 3,174,851, https://patents.google.com/patent/US3174851A/en

Sources added to it: NASA SP-5110, 55-Nitinol: The Alloy With a Memory, C. M. Jackson, H. J. Wagner and R. J. Wasilewski, Battelle Memorial Institute for the NASA Technology Utilization Office, 1972, https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf, dated 1972-01-01; NASA CR-1433, Nitinol Characterization Study, Goodyear Aerospace Corporation report GER 14188 under contract NAS 1-7522 for NASA Langley Research Center, September 1969, https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf, dated 1969-09-01; US Patent 3,174,851, Nickel-base alloys, William J. Buehler and Raymond C. Wiley, assigned to the United States as represented by the Secretary of the Navy, filed 1 December 1961, granted 23 March 1965, https://patents.google.com/patent/US3174851A/en, dated 1965-03-23.

### Ulf Leonhardt

Fields the record forced a change to: date.

Its date is now set to 2010-03-02, derived from the record rather than assigned.

### Capitão Uyrangê Bolívar Soares Nogueira de Hollanda Lima

Fields the record forced a change to: affiliations.

Affiliations rewritten as prose rather than as raw identifiers: fab, Serviço Nacional de Informações (SNI).

### Vincent L. Teofilo

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### Wil McCarthy

Fields the record forced a change to: date.

Its date is now set to 2010-01-01, derived from the record rather than assigned.

### William Culbreth

Fields the record forced a change to: date.

Its date is now set to 2010-11-20, derived from the record rather than assigned.

### William L. Moore

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** Moore publicly admitted at the 1989 MUFON symposium that he had cooperated with US Air Force counterintelligence and had knowingly passed false information to Paul Bennewitz. Source: William L. Moore, address to the MUFON Symposium, Las Vegas, July 1989
- **Tier 1 documented.** Moore and Shandera published 'The MJ-12 Documents: An Analytical Report' as Fair-Witness Project Publication Number 1500 in 1990, and Moore and Friedman published 'Philip Klass and MJ-12: What are the Facts' as Publication Number 1290 in 1988 - both cited in CIA's own 1997 history of the Agency's UFO role. Source: Gerald K. Haines, 'CIA's Role in the Study of UFOs, 1947-90', endnote 93

Sources added to it: Gerald K. Haines, 'CIA's Role in the Study of UFOs, 1947-90', Studies in Intelligence (CIA), archived copy, https://www.theblackvault.com/documentarchive/cias-role-in-the-study-of-ufos-1947-90/, dated 1997-01-01; Philip J. Klass, 'The MJ-12 Crashed-Saucer Documents', Skeptical Inquirer, https://skepticalinquirer.org/1988/01/the-mj-12-crashed-saucer-documents/, dated 1988-01-01; FBI Records: The Vault - 'Majestic 12', https://vault.fbi.gov/Majestic%2012, dated 2011-04-01.

### William Neil McCasland

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 21 April 2026, Michels dated the disappearance to Friday 27 February 2026 at Quail Run Court, Albuquerque: a repairman saw McCasland at the house around 10am, his wife left at about 11:10am and returned at 12:04pm to find him gone, and she reported him missing at 3:07pm. He said the prescription glasses, a switched-off phone and a smartwatch were left behind, and that a red backpack, the wallet and a .38-calibre revolver with its holster were missing (0:05:16 to 0:06:12). Source: American Alchemy with Jesse Michels, 'Why America's Top Scientists Are Going Missing [They Knew Too Much...]', 21 April 2026, 0:05:16 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3303927368.mp3?updated=1776795850
- **Tier 2 named person on the record.** In the same episode Michels said that within a week the search had grown from the Bernalillo County Sheriff's Office to the FBI's Albuquerque Field Office, the Air Force Office of Special Investigations, New Mexico State Search and Rescue and Albuquerque Mountain Rescue, and that no camera footage of McCasland ever surfaced (0:09:04). Source: American Alchemy with Jesse Michels, 'Why America's Top Scientists Are Going Missing [They Knew Too Much...]', 21 April 2026, 0:09:04 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3303927368.mp3?updated=1776795850
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 2 July 2026, Rep. Eric Burlison said of McCasland that 'I know he was on my list of people to talk to', that David Grusch had sent someone to interview him without getting much out of him, and that in Burlison's view McCasland knew inquiries were being made. Asked about a missing firearm Burlison corrected the host: 'they don't know that he took a gun... Maybe missing. It's not confirmed.' He said the latest information was that McCasland had bought a medical kit at REI (1:28:33 to 1:31:18). Source: American Alchemy with Jesse Michels, 'Congressman: "President Trump Was Briefed On Alien Hybrids!"', 2 July 2026, 1:28:33 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3
- **Tier 2 named person on the record.** The claim that McCasland sat on a Special Access Program Oversight Committee and ran the Air Force Research Laboratory at Wright-Patterson is made in this corpus by Michels, not by any guest: hedged as 'I believe he was on the special access program oversight committee' to Rep. Burlison on 2 July 2026 (1:28:33), and stated flatly to Michael Shermer on 9 July 2026 (1:15:12). Neither guest adopts it. Source: American Alchemy with Jesse Michels, 'Congressman: "President Trump Was Briefed On Alien Hybrids!"', 2 July 2026, 1:28:33 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3
- **Tier 2 named person on the record.** Three speakers in the same corpus decline to corroborate. Asked directly by Michels on 28 May 2026 whether he had come across 'General William Neil McCaslin', former Army remote viewer Lyn Buchanan answered 'No', and to the follow-up naming Wright-Patterson, 'No, I didn't know that' (2:14:52). On 7 June 2026 Jeremy Corbell characterised the reported McCasland-to-Tom DeLonge contact as an operation, saying 'I said it's part of an op', while acknowledging that McCasland is missing (1:56:41 to 1:59:32). On 9 July 2026 Michael Shermer argued the disappearance against base rates, asking 'How many people go missing? It's thousands' and 'why aren't all the heads of all the nuclear sites or the generals... all going missing', while conceding it 'should be investigated. Obviously' by the family, local police or the FBI (1:14:21 to 1:20:51). Source: American Alchemy with Jesse Michels: '"I Saw a Mantis Alien At THIS American Military Base!" -Army Sergeant Lyn Buchanan', 28 May 2026, 2:14:52 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6048917608.mp3 ; '"If You Knew What I Knew!" -Jeremy Corbell UNLEASHES On Jesse Michels | EARLY RELEASE', 7 June 2026, 1:56:41 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1864048266.mp3 ; 'I Debated UFOs With America's Top Skeptic (It Got Ugly...)', 9 July 2026, 1:14:21 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL4216664886.mp3

Sources added to it: American Alchemy with Jesse Michels, 'Why America's Top Scientists Are Going Missing [They Knew Too Much...]', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3303927368.mp3?updated=1776795850, dated 2026-04-21; American Alchemy with Jesse Michels, 'Congressman: "President Trump Was Briefed On Alien Hybrids!"', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3, dated 2026-07-02; American Alchemy with Jesse Michels, '"I Saw a Mantis Alien At THIS American Military Base!" -Army Sergeant Lyn Buchanan', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6048917608.mp3, dated 2026-05-28; American Alchemy with Jesse Michels, '"If You Knew What I Knew!" -Jeremy Corbell UNLEASHES On Jesse Michels | EARLY RELEASE', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1864048266.mp3, dated 2026-06-07; American Alchemy with Jesse Michels, 'I Debated UFOs With America's Top Skeptic (It Got Ugly...)', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL4216664886.mp3, dated 2026-07-09.

## Corrections to the entities

46 records in the entities set were changed by what the documents said.

### AARO FY2025 Consolidated Annual Report on UAP

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The report contradicts itself on satellite flaring. Section IV.C states that AARO resolved 44 UAP-related events as attributable to satellite flaring during the reporting period, while Section I (Executive Summary) and Section VI state that new capability enabled analysts to resolve 238 reported UAP as satellite flaring. Note that a separate figure of 44 UAP reports 'in the space domain' appears at Section III.A and is a different 44. Source: https://www.aaro.mil/Portals/136/PDFs/FY25%20UAP%20Annual%20Report/AARO_FY2025_Consolidated_Annual_Report_on_UAP.pdf

Sources added to it: https://www.aaro.mil/Portals/136/PDFs/FY25%20UAP%20Annual%20Report/AARO_FY2025_Consolidated_Annual_Report_on_UAP.pdf

### AARO Report on the Historical Record of U.S. Government Involvement with UAP, Volume I

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented, allegation shaped wording as stored.** The report contains ZERO occurrences of the name 'Wilson' and zero of 'Davis' across all 63 pages including endnotes 1-200. It names no private individuals, referring instead to 'Person 1' and 'the named former CIA official'. It disposes of the reverse-engineering allegations without ever engaging the Wilson-Davis memorandum, a document that sits in a congressional hearing file. Source: https://media.defense.gov/2024/Mar/08/2003409233/-1/-1/0/AARO_Historical_Record_Report_Vol_1_2024.pdf
- **Tier 1 documented.** The disposal is by attribution to circular reporting: 'AARO assesses that the inaccurate claim that the USG is reverse-engineering extraterrestrial technology and is hiding it from Congress is, in large part, the result of circular reporting from a group of individuals who believe this to be the case, despite the lack of any evidence.' Source: https://media.defense.gov/2024/Mar/08/2003409233/-1/-1/0/AARO_Historical_Record_Report_Vol_1_2024.pdf

Sources added to it: https://media.defense.gov/2024/Mar/08/2003409233/-1/-1/0/AARO_Historical_Record_Report_Vol_1_2024.pdf

### The Aerospace Corporation

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** The corporation has now been questioned by Congress on the subject, on one member's account. On American Alchemy with Jesse Michels, 2 July 2026, Rep. Eric Burlison said his office wrote to The Aerospace Corporation from the House Oversight Committee, that the corporation sent two members of its executive team, that the interview took place in a SCIF during the Biden administration, and that they had no knowledge of UAP or reverse engineering: 'they knew nothing' (0:19:48). No document of that meeting has been opened for this board. Source: American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', 2 July 2026, 0:19:48 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3

Sources added to it: American Alchemy with Jesse Michels, 'Congressman: President Trump Was Briefed On Alien Hybrids!', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2654068830.mp3, dated 2026-07-02.

### Armed Forces Special Weapons Project

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** Groves held the command for one year to the day. The Defense Threat Reduction Agency's chronology of its own lineage reads: 'Feb. 28, 1947. Maj Gen Groves becomes first Chief AFSWP, serving for one year, until his retirement on February 29, 1948; he is promoted to Lt. General on January 24, 1948.' The same history records that the command stood empty when it was created: 'between the beginning of January and the end of February 1947, there was no officially appointed chief of AFSWP. During this period, Groves' aide, Colonel Hasbrouck, assumed Headquarters command in Washington as the senior officer of the organization.' Source: Defense's Nuclear Agency 1947-1997, Defense Threat Reduction Agency, 2002, Appendix C: Chronology, DTIC ADA412977, https://archive.org/download/DTIC_ADA412977/DTIC_ADA412977_djvu.txt

Sources added to it: Defense's Nuclear Agency 1947-1997, Defense Threat Reduction Agency, 2002, DTIC ADA412977, https://archive.org/download/DTIC_ADA412977/DTIC_ADA412977_djvu.txt, dated 2002-01-01.

### Air Technical Intelligence Center

Fields the record forced a change to: claims, cls, desc, sources.

The board once carried a sentence that the record replaced. The corrections file states: Only one sentence of the desc changes. The exact sentence replaced is: ATIC became the Foreign Technology Division in 1961 and later the National Air and Space Intelligence Center, which remains at Wright-Patterson today.

Its description now reads: The Air Technical Intelligence Center, established in 1951 out of the Air Materiel Command intelligence organisation (T-2) at Wright Field, was the United States' centre for the exploitation of foreign aerospace technology. It was the organisation that processed the Operation Paperclip haul, that dismantled and reverse-engineered captured Soviet and German airframes, and that was institutionally designed to answer exactly one question: what is this thing and how does it work. Every official UFO project of the legacy era, SIGN, GRUDGE and Blue Book, was hosted here, which is a fact usually reported as an administrative detail and is in fact the central structural point of this domain. The United States did not assign unidentified flying objects to a science agency, an academic body or an air-defence command; it assigned them to the shop that takes recovered hardware apart. The Air Force organizational-history record gives a discontinuation and a new constitution rather than a renaming: the Air Technical Intelligence Center was redesignated Aerospace Technical Intelligence Center on 21 September 1959 and discontinued on 1 July 1961, and the Foreign Technology Division was constituted, activated and organized the same day, absorbing the mission and resources; FTD's own later name is the National Air and Space Intelligence Center, which remains at Wright-Patterson today. It also issued Blue Book Special Report No. 14 in 1955 and was the terminal analytical node under AFR 200-2. If a legacy recovery and exploitation effort existed, ATIC and its successors are the institutional address, and its 1947-1951 T-2 intelligence files have never been subject to a comprehensive declassification review.

Claims the record added:

- **Tier 2 named person on the record.** The lineage is a discontinuation and a new constitution, not a renaming: 'Air Technical Intelligence Center established 21 May 1951; redesignated Aerospace Technical Intelligence Center, 21 September 1959; discontinued 1 July 1961. Foreign Technology Division constituted, activated, and organized 1 July 1961', and 'On 1 July 1961, the organization was inactivated and the mission and resources absorbed by the Foreign Technology Division (FTD)'. Tier 2 because the compilation carrying this text is a private site citing the Air Force Historical Research Agency, and AFHRA's own pages return HTTP 403 from this environment. Source: AEROSPACE TECHNICAL INTELLIGENCE CENTER, Department of the Air Force Organizational Histories compilation, created 10 December 2025, sourced to the Air Force Historical Research Agency, https://www.usafunithistory.com/PDF/A-E/AEROSPACE%20TECHNICAL%20INTELLIGENCE%20CENTER.pdf

Sources added to it: AEROSPACE TECHNICAL INTELLIGENCE CENTER, Department of the Air Force Organizational Histories compilation (private site, sourced to AFHRA), https://www.usafunithistory.com/PDF/A-E/AEROSPACE%20TECHNICAL%20INTELLIGENCE%20CENTER.pdf, dated 2025-12-10.

### Atomic Energy Commission

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The Commission gains its first named chairman on this board. The CIA's own declassified chronology records under January 1961: '16 JAN. Dr. Glenn T. Seaborg named AEC chairman, succeeding John A. McCone (confirmed by Senate 24 Feb).' McCone went from the Commission to the Directorship of Central Intelligence, and two years later Seaborg was writing to him there on Commission letterhead. No end to the chairmanship is established by any record opened for this pass. Source: CIA Historical Staff Chronology 1946-65, Volume II 1956-65, June 1970, CIA-RDP85B00803R000200050003-5, declassified in part 8 July 2013, https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000200050003-5

Sources added to it: CIA Historical Staff Chronology 1946-65, Volume II 1956-65, CIA-RDP85B00803R000200050003-5, https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000200050003-5, dated 1970-06-01.

### Battelle Memorial Institute

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 13 March 2025, at 1:34:53, John Brandenburg said that 'there was a contract between Los Alamos and Battelle Memorial Institute in 1949 and it was around nitinol', that the work was 'declassified by Battelle in the 60s', and asked why Los Alamos had a contract with Battelle in 1949. The board's node dates the corresponding nickel-titanium work to 1948-49 under Wright-Patterson sponsorship. The two accounts name different sponsors for the same alloy in the same period, and no contract record was opened for either. Source: American Alchemy with Jesse Michels, 'Top Physicist: There Was A Nuclear Catastrophe On Mars (ft. Dr. John Brandenburg)', published 13 March 2025, at 1:34:53
- **Tier 2 named person on the record, allegation shaped wording as stored.** On American Alchemy with Jesse Michels, 5 July 2025 at 0:59:04 and again on 12 July 2025 at 1:00:44, Michels said that after Jacques Vallee found the Pentacle memo in the Blue Book files the memo could not be raised around the Robertson Panel: 'apparently you weren't allowed to mention the pentacle' and 'you were not supposed to bring this memo up'. Both tellings are the same speaker, neither cites a document for the instruction, and both describe Vallee putting it to J. Allen Hynek, who on Michels's account played dumb. The board carries the memo and Howard C. Cross's authorship but not this alleged instruction. Source: American Alchemy with Jesse Michels, 'Fake Alien Signals Drove Him Insane... (ft. Greg Bishop)', 5 July 2025, 0:59:04, and 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 1:00:44

Sources added to it: American Alchemy with Jesse Michels, 'Top Physicist: There Was A Nuclear Catastrophe On Mars (ft. Dr. John Brandenburg)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL3307125405.mp3?updated=1752179577, dated 2025-03-13; American Alchemy with Jesse Michels, 'Fake Alien Signals Drove Him Insane... (ft. Greg Bishop)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6921419786.mp3?updated=1752608918, dated 2025-07-05; American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599, dated 2025-07-12.

### Battelle Memorial Institute

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented, allegation shaped wording as stored.** The federal literature on nitinol, one report of it written by Battelle itself, does not support a Battelle 1948-49 lineage for the alloy. NASA SP-5110, prepared for NASA by Battelle Memorial Institute in 1972, opens: 'Some 10 years ago, Buehler and Wiley of the U.S. Naval Ordnance Laboratory developed a series of engineering alloys that possess a unique mechanical (shape) memory. The generic name of the series of alloys is 55-Nitinol, where Nitinol stands for Nickel Titanium Naval Ordnance Laboratory.' The earliest Naval Ordnance Laboratory nitinol report cited anywhere in its reference list is NOLTR 61-75 of 3 August 1961; US Patent 3,174,851 was filed on 1 December 1961; and NASA CR-1433 of September 1969 records Battelle's own role as a subcontractor to Goodyear Aerospace which 'processed the basic Nitinol rod'. The allegation that Wright-Patterson-sponsored Battelle reports on nickel-titanium alloy from 1948-49 are missing from Air Force and Battelle archives is kept on this board as the allegation it is, and is unsupported by the federal literature opened here. Source: NASA SP-5110, 55-Nitinol: The Alloy With a Memory, Battelle Memorial Institute for NASA, 1972, chapter 1 p. 1 and references 12 and 74, https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf ; NASA CR-1433, Nitinol Characterization Study, September 1969, foreword p. iii and p. 2, https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf ; US Patent 3,174,851, https://patents.google.com/patent/US3174851A/en

Sources added to it: NASA SP-5110, 55-Nitinol: The Alloy With a Memory, C. M. Jackson, H. J. Wagner and R. J. Wasilewski, Battelle Memorial Institute for the NASA Technology Utilization Office, 1972, https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf, dated 1972-01-01; NASA CR-1433, Nitinol Characterization Study, Goodyear Aerospace Corporation report GER 14188 under contract NAS 1-7522 for NASA Langley Research Center, September 1969, https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf, dated 1969-09-01; US Patent 3,174,851, Nickel-base alloys, William J. Buehler and Raymond C. Wiley, assigned to the United States as represented by the Secretary of the Navy, filed 1 December 1961, granted 23 March 1965, https://patents.google.com/patent/US3174851A/en, dated 1965-03-23.

### CENTER LANE

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The special access designation was the Secretary of the Army's, above INSCOM. The deactivation letter asks HQDA to take 'the necessary actions ... to officially discontinue CENTER LANE as a Secretary of the Army designated Special Access Program', and every page of the project's paperwork carries the warning notice 'CENTER LANE SPECIAL ACCESS PROGRAM RESTRICT DISSEMINATION TO THOSE WITH VERIFIED ACCESS TO CATEGORY THREE (3)'. Source: Letter, Deactivation of INSCOM CENTER LANE Project (ICLP) as a Special Access Program (SAP) (U), 2 March 1985, CIA-RDP96-00789R002100120002-4, https://archive.org/download/cia-readingroom-document-cia-rdp96-00789r002100120002-4/cia-rdp96-00789r002100120002-4_djvu.txt
- **Tier 1 documented.** The transfer to DIA was INSCOM's own recommendation, not a DIA rescue after a congressional petition. In July 1984 INSCOM's commanding general wrote that 'INSCOM ... should discontinue our involvement with psychoenergetic research and operations', intended 'to cease INSCOM CENTER LANE Project operations on 30 Sept 1984', and asked for authority to permit 'timely and undisrupted transfer of (1) ICLP operations to a national agency such as DIA or NSA'. The letter of 2 March 1985 then notified HQDA of 'the deactivation of the INSCOM CENTER LANE Project, the attachment OPCON of CENTER LANE assets and resources to the Defense Intelligence Agency, and the retirement of CENTER LANE as an active project nickname'. Nothing opened mentions Vorona or a petition to Congress. Source: Memorandum, INSCOM CENTER LANE Project (U), 17 July 1984, CIA-RDP96-00788R001500100011-4, https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001500100011-4/cia-rdp96-00788r001500100011-4_djvu.txt ; letter of 2 March 1985, CIA-RDP96-00789R002100120002-4, https://archive.org/download/cia-readingroom-document-cia-rdp96-00789r002100120002-4/cia-rdp96-00789r002100120002-4_djvu.txt
- **Tier 1 documented.** The security classification guide this node argues from is indexed and withheld. The reading-room item releases a human-use requirements annex and states 'Next 8 Page(s) In Document Exempt'; the guide's own text has not been released. Source: CENTER LANE security classification guide item, eight pages exempt, CIA-RDP96-00788R001500120046-4, https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001500120046-4/cia-rdp96-00788r001500120046-4_djvu.txt

Sources added to it: Deactivation of INSCOM CENTER LANE Project (ICLP) as a Special Access Program (SAP) (U), 2 March 1985, CIA-RDP96-00789R002100120002-4, https://archive.org/download/cia-readingroom-document-cia-rdp96-00789r002100120002-4/cia-rdp96-00789r002100120002-4_djvu.txt, dated 1985-03-02; INSCOM CENTER LANE Project (U), memorandum for ACSI, 17 July 1984, CIA-RDP96-00788R001500100011-4, https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001500100011-4/cia-rdp96-00788r001500100011-4_djvu.txt, dated 1984-07-17; CENTER LANE security classification guide item, eight pages exempt, CIA-RDP96-00788R001500120046-4, https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001500120046-4/cia-rdp96-00788r001500120046-4_djvu.txt, dated 2000-08-08.

### University of Colorado UFO Project (Condon Committee)

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 12 July 2025, at 0:33:36, Robert Salas read on air from what he presents as the Colorado project's own record: 'The following interview conducted by Roy Craig, was Lieutenant Colonel Lewis D. Chase, who is chief of the operations division at Malstrom Air Force Base, Montana. The interview is being conducted at Malmstrom on October 19, 1967.' Salas says Chase had earlier confirmed in writing that he coordinated on the UFO activity and then denied the connection to Craig in this interview. Source: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:33:36 and 0:34:29, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599
- **Tier 1 documented.** The Air Force put the answer it wanted to the project in writing three months into the contract. Hippler's letter to Condon of 16 January 1967 continues: 'It will be at least that long before another independent study can be mounted to see if the Air Force can get out from under this program.' It closes by telling Condon that if the contract expires before the groundwork for a recommendation is laid, extending the contract 'would be less costly than another decade of operating Project Blue Book.' Source: Lt Col Robert R. Hippler to Dr Edward U. Condon, 16 January 1967, page 2, https://www.nicap.org/docs/HipplerLetters.pdf

Sources added to it: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599, dated 2025-07-12; Hippler to Condon, 16 January 1967, with Low to Hippler, 27 January 1967 (NICAP document archive scan), https://www.nicap.org/docs/HipplerLetters.pdf, dated 1967-01-16.

### Legislative Process (proposed and pending)

Fields the record forced a change to: claims, cls, label, sources, sub.

Its label now reads: Legislative Process (proposed and pending).

Its one line summary now reads: Bills, amendments and the actors that move them. Deliberately distinct from d-legislation (Enacted Statute): the gap between what passed the Senate and what survived conference is one of this board's central substantive findings, and collapsing the two would erase it.

### Defense Advanced Research Projects Agency

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The agency has a founding instrument and a first Director, and this node has carried neither. DoD Directive 5105.15 of 7 February 1958, reproduced in full in the agency's own commissioned history, reads: 'In accordance with the provisions of the National Security Act of 1947, as amended, and Reorganization Plan No. 6 of 1953, there is established in the Office of the Secretary of Defense the Department of Defense Advanced Research Projects Agency.' Its mandate is open-ended by design: the Agency is responsible for 'the direction or performance of such advanced projects in the field of research and development as the Secretary of Defense shall, from time to time, designate by individual project or by category', and 'The Director of Advanced Research Projects shall report to the Secretary of Defense.' Source: The Advanced Research Projects Agency, 1958-1974, Richard J. Barber Associates, Inc., prepared for ARPA, Figure II-2, DTIC AD-A154 363, https://archive.org/download/DTIC_ADA154363/DTIC_ADA154363_djvu.txt
- **Tier 1 documented.** The first Director was Roy W. Johnson, not Herbert York. A second agency's record dates the founding and names the officer independently: the CIA Historical Staff Chronology under Jan-Apr 58 reads '7 FEB. Advanced Research Projects Agency (ARPA) established in DOD, Roy W. Johnson of General Electric named director, responsible for US space program, including missiles and anti-missiles.' Herbert York was ARPA's first Chief Scientist and was later elevated to first Director of Defense Research and Engineering. Source: CIA Historical Staff Chronology 1946-65, Volume II 1956-65, June 1970, CIA-RDP85B00803R000200050003-5, https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000200050003-5

Sources added to it: The Advanced Research Projects Agency, 1958-1974, Richard J. Barber Associates, Inc., DTIC AD-A154 363, https://archive.org/download/DTIC_ADA154363/DTIC_ADA154363_djvu.txt, dated 1975-12-01; CIA Historical Staff Chronology 1946-65, Volume II 1956-65, CIA-RDP85B00803R000200050003-5, https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000200050003-5, dated 1970-06-01.

### Aneutronic Fusion Propulsion (DIA-08-1011-003)

Fields the record forced a change to: cls, label.

Its label now reads: Aneutronic Fusion Propulsion (DIA-08-1011-003).

### Aneutronic Fusion Propulsion (DIA-08-1011-004)

Fields the record forced a change to: cls, label.

Its label now reads: Aneutronic Fusion Propulsion (DIA-08-1011-004).

### The 38 Defense Intelligence Reference Documents (DIRDs)

Fields the record forced a change to: claims, cls, label, sources, sub.

Its label now reads: The 38 Defense Intelligence Reference Documents (DIRDs).

Its one line summary now reads: AAWSAP contract deliverable set, 2008-2010. A DOCUMENT SERIES, not a programme, the individual papers are wired to their authors and to AAWSAP, and this node is the shelf they sit on. Absorbed the duplicate node dird-collection on 14 Aug 2026.

Claims the record added:

- **Tier 1 documented.** The board formerly carried two nodes for this object, dird-series and dird-collection, describing the same AAWSAP deliverable set. They were collapsed on 14 August 2026 and dird-collection's seven edges re-pointed here. Source: Board maintenance record, notes/L0-IMPLEMENTATION-2026-08-13.md

### Unidentified Aerial Phenomena in the UK Air Defence Region (DIS Scientific & Technical Memorandum 55/2/00)

Fields the record forced a change to: claims, cls, sources, sub.

Its one line summary now reads: THREE-volume UK Defence Intelligence Staff report (not four); the separately-released standalone Executive Summary is what has been miscounted as a fourth part. Volume 3 preface is dated February 2000. Released 15 May 2006 under FOI to David Clarke and Gary Anthony.

Claims the record added:

- **Tier 1 documented.** The report is a three-volume report, not four. The preface to Volume 3 states 'This is the third volume of a three-part report'. The commonly cited fourth part is the separately released standalone Executive Summary. Source: Project Condign, 'Unidentified Aerial Phenomena in the UK Air Defence Region', UK Defence Intelligence Staff; released 15 May 2006
- **Tier 1 documented.** Volume 3 is titled 'Miscellaneous Related Studies'. 'Potential for Exploitation of UAP-Associated Effects' is the title of its Chapter 3, and Chapter 4 is 'UAP Work in Other Countries'. These have been conflated with the volume title. Source: Project Condign, 'Unidentified Aerial Phenomena in the UK Air Defence Region', UK Defence Intelligence Staff; released 15 May 2006
- **Tier 1 documented.** Volume 3 Chapter 4 paragraph 1 records the Soviet centre's name as SOYUZUFOSENTR, not Soyuzufotsentr: 'an Inter-Industry Ufology Research Centre (SOYUZUFOSENTR) to co-ordinate records. This Centre had the rights of an Institute under the USSR Academy of Sciences, and was headed by V.G. AZAHAZHA (or AZHAZHA) an eminent researcher and former naval submariner.' Source: Project Condign, 'Unidentified Aerial Phenomena in the UK Air Defence Region', UK Defence Intelligence Staff; released 15 May 2006
- **Tier 2 named person on the record.** The FOI review file DEFE 24/2090/1 shows a still-redacted reference to a 'CIA desk officer' at Volume 3, Chapter 4, page 3, paragraph 12. Source: UK National Archives DEFE 24/2090/1, FOI review file

Sources added to it: Project Condign, 'Unidentified Aerial Phenomena in the UK Air Defence Region', UK Defence Intelligence Staff; released 15 May 2006.

### DoD special access programme governance change, 5 January 1994

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** A central Army special-access oversight office predates the 1994 reform by ten years. GAO/NSIAD-88-152 records: 'A DOD review of Army special access programs in 1983 revealed systemic weaknesses in various management areas, which resulted in establishment of a central oversight office in September 1984.' The same report states that in 1988 'The Deputy Under Secretary of Defense for Policy is required to maintain a listing of all special access programs, but does not do so because of security concerns', and that 'the Secretary's Office has no centralized office with cognizance of all special access programs'. The January 1994 dates this board carries stand; the Army aftermath began in 1983-84. Source: GAO/NSIAD-88-152, B-230522, 24 May 1988, Results in Brief and Recommendations, https://www.gao.gov/assets/nsiad-88-152.pdf

Sources added to it: GAO/NSIAD-88-152, Special Access Programs: DOD Criteria and Procedures for Creating Them Need Improvement, B-230522, 24 May 1988, https://www.gao.gov/assets/nsiad-88-152.pdf, dated 1988-05-24.

### EG&G (Edgerton, Germeshausen and Grier)

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 3 stated inference.** On American Alchemy with Jesse Michels, 21 February 2025, between 0:08:54 and 0:09:47, the guest Sammy, known as UAP Gerb, said of the retrieval teams described in the Jonathan Wigant account of Peru in 1997 and the Michael Herrera account of Indonesia in 2009 that 'I think this is likely a DOE NEST team, nuclear emergency search teams', which 'received help from contractors like EG&G'. Reasoning: he frames this explicitly as his own inference from the DOE-lettered rain jackets and hazmat suits the witnesses describe, not as a record. Source: American Alchemy with Jesse Michels, 'The Most Knowledgeable UFO Researcher In The World', published 21 February 2025, at 0:08:54 to 0:09:47
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 30 January 2025, at 1:30:12, Jake Barber said that 'the senior EG&G engineer described to my great uncle that it was egg shaped about the size of an SUV', that the team 'tried to penetrate the hull, tried to open it, they couldn't', and that from very small samples of the material they concluded the isotope ratio or mixture of elements was not of terrestrial manufacture. The account reaches Barber through his great uncle and the engineer is not named. Source: American Alchemy with Jesse Michels, 'UFO Crash Retrieval: Jake Barber's FIRSTHAND Account', published 30 January 2025, at 1:30:12
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 31 August 2025, at 0:46:20, Greg Rogers ruled EG&G out as the owner of the craft he describes at Cape Canaveral in 1992, naming instead 'something like Lockheed or Northrop, Boeing' or Raytheon, possibly in a consortium, and noting that Lockheed and Martin Marietta had not yet merged at that date. This is the same episode whose narration places EG&G at the centre of the story, and the two are recorded as they stand. Source: American Alchemy with Jesse Michels, 'NASA Doctor: I Saw A UFO Hovering In THIS Secret Hangar (Ft. Greg Rogers)', 31 August 2025, 0:46:20, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2173204669.mp3?updated=1757589247
- **Tier 2 named person on the record.** At 0:47:14 in the same episode Rogers gave his reason as a general rule about black-programme ownership, using Have Blue and the F-117: during the demonstrator phase 'the U.S. Air Force did not own that even though it had U.S. Air Force markings', and the Air Force took ownership only after it let the production contract. Air Force markings on an airframe are not, on this account, evidence of Air Force custody. Source: American Alchemy with Jesse Michels, 'NASA Doctor: I Saw A UFO Hovering In THIS Secret Hangar (Ft. Greg Rogers)', 31 August 2025, 0:47:14

Sources added to it: American Alchemy with Jesse Michels, 'The Most Knowledgeable UFO Researcher In The World' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE8993457707.mp3?updated=1751590849, dated 2025-02-21; American Alchemy with Jesse Michels, 'UFO Crash Retrieval: Jake Barber's FIRSTHAND Account (ft. Logan Paul and Ammar Kandil)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE9340057376.mp3?updated=1751590405, dated 2025-01-30; American Alchemy with Jesse Michels, 'NASA Doctor: I Saw A UFO Hovering In THIS Secret Hangar (Ft. Greg Rogers)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL2173204669.mp3?updated=1757589247, dated 2025-08-31.

### UAP Gerb - Battelle Memorial Institute investigation

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented, allegation shaped wording as stored.** The federal literature on nitinol, one report of it written by Battelle itself, does not support a Battelle 1948-49 lineage for the alloy. NASA SP-5110, prepared for NASA by Battelle Memorial Institute in 1972, opens: 'Some 10 years ago, Buehler and Wiley of the U.S. Naval Ordnance Laboratory developed a series of engineering alloys that possess a unique mechanical (shape) memory. The generic name of the series of alloys is 55-Nitinol, where Nitinol stands for Nickel Titanium Naval Ordnance Laboratory.' The earliest Naval Ordnance Laboratory nitinol report cited anywhere in its reference list is NOLTR 61-75 of 3 August 1961; US Patent 3,174,851 was filed on 1 December 1961; and NASA CR-1433 of September 1969 records Battelle's own role as a subcontractor to Goodyear Aerospace which 'processed the basic Nitinol rod'. The allegation that Wright-Patterson-sponsored Battelle reports on nickel-titanium alloy from 1948-49 are missing from Air Force and Battelle archives is kept on this board as the allegation it is, and is unsupported by the federal literature opened here. Source: NASA SP-5110, 55-Nitinol: The Alloy With a Memory, Battelle Memorial Institute for NASA, 1972, chapter 1 p. 1 and references 12 and 74, https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf ; NASA CR-1433, Nitinol Characterization Study, September 1969, foreword p. iii and p. 2, https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf ; US Patent 3,174,851, https://patents.google.com/patent/US3174851A/en

Sources added to it: NASA SP-5110, 55-Nitinol: The Alloy With a Memory, C. M. Jackson, H. J. Wagner and R. J. Wasilewski, Battelle Memorial Institute for the NASA Technology Utilization Office, 1972, https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf, dated 1972-01-01; NASA CR-1433, Nitinol Characterization Study, Goodyear Aerospace Corporation report GER 14188 under contract NAS 1-7522 for NASA Langley Research Center, September 1969, https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf, dated 1969-09-01; US Patent 3,174,851, Nickel-base alloys, William J. Buehler and Raymond C. Wiley, assigned to the United States as represented by the Secretary of the Navy, filed 1 December 1961, granted 23 March 1965, https://patents.google.com/patent/US3174851A/en, dated 1965-03-23.

### GRILL FLAME

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The programme's origin and its transfer are both dated in INSCOM's own history. The FY 1981 Annual Historical Review records that 'Project GRILL FLAME originated as a specially controlled and compartmented activity under the direct supervision of the ACSI, DA, and in coordination with other DOD agencies concerned with related activity. ACSI orally tasked HQ INSCOM to evaluate Project GRILL FLAME in October 1978', and that 'On 11 February 1981, ACSI formally transferred the GRILL FLAME program management responsibili[ty] to INSCOM where it was assigned to Detachment G, US Army Operational Group.' The section is partly withheld under 5 U.S.C. 552(b)(1) and (b)(3) and its source note names 'IA(HQ) Form 32, Formalization of Project GRILL FLAME (10 Sep 81) (S/NOFORN)'. Source: Annual Historical Review, US Army Intelligence and Security Command, FY 1981, pp. 89 to 90, released 11 September 2018, https://www.governmentattic.org/30docs/USAINSCOMhistoryFY_1981.pdf

Sources added to it: Annual Historical Review, US Army Intelligence and Security Command, FY 1981, INSCOM History Office, released 11 September 2018 after mandatory declassification review, https://www.governmentattic.org/30docs/USAINSCOMhistoryFY_1981.pdf, dated 2018-09-11.

### A Die-hard Issue: CIA's Role in the Study of UFOs, 1947-1990

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** 'This led the Air Force to make misleading and deceptive statements to the public in order to allay public fears and to protect an extraordinarily sensitive national security project. While perhaps justified, this deception added fuel to the later conspiracy theories and the coverup controversy of the 1970s.' Source: Gerald K. Haines, 'CIA's Role in the Study of UFOs, 1947-90', Studies in Intelligence (CIA)
- **Tier 1 documented.** 'Air Force BLUE BOOK investigators aware of the secret U-2 flights tried to explain away such sightings by linking them to natural phenomena such as ice crystals and temperature inversions... They were careful, however, not to reveal the true cause of the sighting to the public.' Source: Haines, 'CIA's Role in the Study of UFOs, 1947-90'
- **Tier 1 documented.** 'According to later estimates from CIA officials who worked on the U-2 project and the OXCART (SR-71, or Blackbird) project, over half of all UFO reports from the late 1950s through the 1960s were accounted for by manned reconnaissance flights (namely the U-2) over the United States.' Source: Haines, 'CIA's Role in the Study of UFOs, 1947-90'
- **Tier 1 documented.** CIA's Deputy Assistant Director of OSI, Philip Strong, refused to declassify the Robertson Panel report and 'the Agency prepared a sanitized version of the report which deleted any reference to CIA and avoided mention of any psychological warfare potential in the UFO controversy.' Source: Haines, 'CIA's Role in the Study of UFOs, 1947-90'

Sources added to it: Gerald K. Haines, 'CIA's Role in the Study of UFOs, 1947-90', Studies in Intelligence (CIA), archived copy, https://www.theblackvault.com/documentarchive/cias-role-in-the-study-of-ufos-1947-90/, dated 1997-01-01; National Archives, 'Project BLUE BOOK - Unidentified Flying Objects' reference report (incl. MJ-12 / Cutler-Twining findings), https://www.archives.gov/research/military/air-force/ufos, dated 2016-08-15.

### A Die-hard Issue: CIA's Role in the Study of UFOs, 1947-1990

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The article states its own trigger: 'In late 1993, after being pressured by UFOlogists for the release of additional CIA information on UFOs, DCI R. James Woolsey ordered another review of all Agency files on UFOs.' Source: Gerald K. Haines, 'CIA's Role in the Study of UFOs, 1947-90', Studies in Intelligence, mirrored full text, https://www.nicap.org/ciarole.htm
- **Tier 1 documented.** The article gives the Air Force's own unexplained residue as a falling figure: 'The percentage of what the Air Force considered unexplained UFO sightings fell to 5.9 percent in 1955 and to 4 percent in 1956.' On Area 52 (batch 07, file 04, 0:49:22) John Ramirez attributed to this article a figure of one in ten. The article does not carry that figure. Source: Gerald K. Haines, 'CIA's Role in the Study of UFOs, 1947-90', Studies in Intelligence, mirrored full text, https://www.nicap.org/ciarole.htm

Sources added to it: Gerald K. Haines, CIA's Role in the Study of UFOs, 1947-90, Studies in Intelligence, mirrored full text, https://www.nicap.org/ciarole.htm, dated 1997-01-01.

### House Oversight Task Force on the Declassification of Federal Secrets hearing, 9 September 2025 - 'Restoring Public Trust Through UAP Transparency and Whistleblower Protection'

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 11 April 2025, between 2:32:28 and 2:33:21, Steven Greer, showing a page of his own book on camera, named a witness he called Stephen Digna in connection with a triangular craft at Fort Irwin that Greer says is man-made. Greer said the witness saw more detail than intended because he used night-vision equipment he had been told not to use, that 'the men who took him there were Raytheon operatives', and that the witness and his wife were later abducted and that the episode 'ruined his life'. The board's prose for the 9 September 2025 hearing already carries the name Steven Digna without this account; the Raytheon attribution is Greer's and no record supporting it was opened. Source: American Alchemy with Jesse Michels, 'Steven Greer: UFO Secrets Are Held By A Global Cabal', published 11 April 2025, at 2:32:28 to 2:33:21

Sources added to it: American Alchemy with Jesse Michels, 'Steven Greer: UFO Secrets Are Held By A Global Cabal' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL5974189713.mp3?updated=1751479023, dated 2025-04-11.

### IAA FY2024 Sec. 1102, contractor turn-in of 'non-earth origin or exotic' UAP material

Fields the record forced a change to: claims, cls, label, sources, sub.

Its label now reads: IAA FY2024 Sec. 1102, contractor turn-in of 'non-earth origin or exotic' UAP material.

Its one line summary now reads: Division M (Intelligence Authorization Act for FY2024) of S. 2226 as passed by the Senate, 27 Jul 2023; the same text is Sec. 1104 of S. 2103 as reported by SSCI, 22 Jun 2023. Turn-in mandate STRIPPED in conference; enacted as Sec. 7343, Div. G, P.L. 118-31, a funding limitation only.

Claims the record added:

- **Tier 1 documented.** The turn-in provision is Sec. 1102 of Division M of S. 2226 as passed by the Senate on 27 July 2023. The Division M table of contents reads 'TITLE XI--OTHER MATTERS Sec. 1101. Modification of reporting requirement for All-domain Anomaly Resolution Office. Sec. 1102. Funding limitations relating to unidentified anomalous phenomena.' The same text appears as Sec. 1104 of S. 2103 as reported by SSCI on 22 June 2023; both citations are correct, to different vehicles. Source: https://www.govinfo.gov/content/pkg/BILLS-118s2226es/html/BILLS-118s2226es.htm
- **Tier 1 documented.** The turn-in mandate did not survive conference. Enacted Sec. 7343 of Division G, P.L. 118-31 contains only (a) definitions, (b) a funding limitation and (c) an IR&D limitation. The phrases 'non-earth origin', 'exotic', 'in their possession' and the 60-day deadline appear nowhere in the enacted text. Source: https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title50-section3373&num=0&edition=prelim
- **Tier 1 documented.** Enacted Sec. 7343(b) reads: 'None of the funds authorized to be appropriated or otherwise made available by this division may be obligated or expended in support of any activity involving unidentified anomalous phenomena protected under any form of special access or restricted access limitation unless the Director of National Intelligence has provided the details of the activity to the appropriate committees of Congress and congressional leadership, including for any activities described in a report released by the All-domain Anomaly Resolution Office in fiscal year 2024.' Source: https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title50-section3373&num=0&edition=prelim
- **Tier 2 named person on the record.** The operative text of Sec. 1102 of Division M has NEVER been read verbatim. Six primary vehicles - govinfo HTML and PDF of S.2226es and S.2103rs, SSCI's engrossed PDF, and both formats of the Congressional Record granule - all fail at the same extraction ceiling. The 60-day deadline, the 'non-earth origin or exotic' language and the make-available-to-AARO mandate therefore rest on a secondary source describing REPORTED Sec. 1104, not engrossed Sec. 1102. This is a downgrade of the board's prior confidence, recorded rather than buried. The text was printed in full as SA 1053 at 169 Cong. Rec. S3628-S3642, which is the citation vehicle a future pass should use. Source: 169 Cong. Rec. S3628-S3642 (26 July 2023), granule CREC-2023-07-26-pt1-PgS3627-2

Sources added to it: https://www.govinfo.gov/content/pkg/BILLS-118s2226es/html/BILLS-118s2226es.htm; https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title50-section3373&num=0&edition=prelim

### Immaculate Constellation 12-page report entered into the Congressional Record

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The report's own first page states who cleared the public version: 'This public version of the author's report was reviewed and approved for public release by the Department of State, Bureau of Global Public Affairs.' The bureau is Global Public Affairs. Source: Immaculate Constellation report as submitted to the House Oversight joint subcommittee hearing of 13 November 2024, committee repository document HHRG-118-GO12-20241113-SD003, page 1, https://www.congress.gov/118/meeting/house/117721/documents/HHRG-118-GO12-20241113-SD003.pdf
- **Tier 1 documented.** The introduction names the report's structure: 'In this public version of the report, information is organized into seven categories of evidence, including: an Unacknowledged Special Access Program (uSAP); Imagery Intelligence (IMINT); human intelligence (HUMINT); signals intelligence (SIGINT); USG bureaucratic records; USG historical records; and other sensitive sources.' The body runs as Sections 1 to 7 in that order, Section 7 'Sensitive Sources' consisting of the single sentence 'From mouth to ear.' Source: HHRG-118-GO12-20241113-SD003, pages 1 and 11, https://www.congress.gov/118/meeting/house/117721/documents/HHRG-118-GO12-20241113-SD003.pdf
- **Tier 1 documented.** Section 2, USG Imagery Intelligence, catalogues nine incidents, each headed by the combatant command it came from. Two are CENTCOM, headed 'CENTCOM Cuboid Formation of Metallic Orbs' and 'CENTCOM Fast Mover Observed Transiting Over Sensitive Facilities'; four are INDOPACOM, two NORTHCOM and one SOUTHCOM. The nine is the incident count; the seven elsewhere in the report is its count of evidence categories, not of incidents. Source: HHRG-118-GO12-20241113-SD003, pages 3 to 5, https://www.congress.gov/118/meeting/house/117721/documents/HHRG-118-GO12-20241113-SD003.pdf
- **Tier 1 documented.** The introduction names the mechanism under which the report reached Congress: the investigation was 'provided to Congress through the UAP whistleblower mechanisms established by the FY23 National Defense Authorization Act, and the FY23 National Intelligence Authorization Act.' The report names the two as separate authorities. Source: HHRG-118-GO12-20241113-SD003, page 1, https://www.congress.gov/118/meeting/house/117721/documents/HHRG-118-GO12-20241113-SD003.pdf
- **Tier 1 documented.** The document as submitted and published by the committee is twelve scanned pages with no text layer. Pages 1 to 11 run continuously from the heading 'Introduction' to the end of 'VI. Conclusion' and its closing line 'Scientia Igne Probata; Veritas Per Fidem'; page 12 is blank. No cover letter, transmittal, author name, classification marking or control number appears on any of the twelve pages. Source: HHRG-118-GO12-20241113-SD003, all twelve pages, https://www.congress.gov/118/meeting/house/117721/documents/HHRG-118-GO12-20241113-SD003.pdf
- **Tier 1 documented.** The hearing record gives the page count as twelve in the chair's own words, twice, and credits the delivery to Shellenberger: 'I will do it, to enter into the Congressional Record this 12-page document that Michael Shellenberger brought today that describes the Immaculate Constellation government program.' Earlier in the same session Mace said 'Mr. Burchett will enter it into the record, but 12 pages about this unacknowledged special access program that your government says does not exist.' Source: U.S. GPO, Hearing transcript, Serial No. 118-135 (CHRG-118hhrg57440), 13 November 2024, https://www.govinfo.gov/content/pkg/CHRG-118hhrg57440/pdf/CHRG-118hhrg57440.pdf
- **Tier 1 documented.** The report is not in the Congressional Record copy this node cites. The GPO hearing print CHRG-118hhrg57440 lists the report in its Index of Documents and then says 'The documents listed above are available at: docs.house.gov'; the words Global, CENTCOM, cover letter and signals intelligence occur nowhere in that print. The document itself is committee repository item HHRG-118-GO12-20241113-SD003. Source: U.S. GPO, Hearing transcript, Serial No. 118-135 (CHRG-118hhrg57440), 13 November 2024, https://www.govinfo.gov/content/pkg/CHRG-118hhrg57440/pdf/CHRG-118hhrg57440.pdf ; and the committee repository item, https://www.congress.gov/118/meeting/house/117721/documents/HHRG-118-GO12-20241113-SD003.pdf

Sources added to it: Immaculate Constellation report as submitted, House Oversight committee repository, HHRG-118-GO12-20241113-SD003, https://www.congress.gov/118/meeting/house/117721/documents/HHRG-118-GO12-20241113-SD003.pdf, dated 2024-11-13; U.S. GPO, Hearing transcript, Serial No. 118-135 (CHRG-118hhrg57440), PDF, https://www.govinfo.gov/content/pkg/CHRG-118hhrg57440/pdf/CHRG-118hhrg57440.pdf, dated 2024-11-13.

### Institute of Field Physics (UNC Chapel Hill)

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The January 1957 Chapel Hill conference had one sponsor and four funders, and the Air Force was not the sponsor. The report's title page reads: 'UNDER THE SPONSORSHIP OF THE International Union of Pure and Applied Physics, with financial support from UNESCO / National Science Foundation / Wright Air Development Center, U.S. Air Force / Office of Ordnance Research, U.S. Army'. The Foreword gives the reason the report exists at all: 'The present report was undertaken as a necessary requirement to obtain conference funds.' WADC's imprint is on the cover because the report was the condition of the money, not because the Air Force convened the meeting. Source: The Role of Gravitation in Physics: Report from the 1957 Chapel Hill Conference, WADC Technical Report 57-216, title page and Foreword by Cecile M. DeWitt, 15 March 1957, https://edition-open-sources.org/sources/5/5/index.html
- **Tier 1 documented.** Two different acts are recorded for the Institute and a node should not collapse them. The conference report's title page states: 'This conference was an activity of the North Carolina Project of the Institute of Field Physics, established in 1956 in the Department of Physics of the University of North Carolina, Chapel Hill.' The certificate of incorporation this node carries is dated 7 September 1955; the establishment inside the department is dated 1956 by the conference's own paper. Source: The Role of Gravitation in Physics: Report from the 1957 Chapel Hill Conference, WADC Technical Report 57-216, title page, https://edition-open-sources.org/sources/5/5/index.html
- **Tier 1 documented.** The press knew the Institute under a different name at its founding. Talbert's Herald Tribune series of 20 November 1955 reports: 'A proposal to establish at the University of North Carolina at Chapel Hill, N. C., an Institute of Pure Physics primarily to carry on theoretical research on gravity was approved earlier this month by the university's board of trustees. This had the approval of Dr. Gordon Gray, who has since retired as president of the university.' It names Agnew H. Bahnson jr. as the fundraiser and says the directorship had been offered to Bryce S. DeWitt. Source: Ansel E. Talbert, New York Herald Tribune, 20 November 1955, continuation p. 36, https://archive.org/download/talbert1ny/talbert1ny_djvu.txt

Sources added to it: The Role of Gravitation in Physics: Report from the 1957 Chapel Hill Conference, the Edition Open Sources reissue of WADC Technical Report 57-216, Max Planck Institute for the History of Science, 2011, title page and Foreword, https://edition-open-sources.org/sources/5/5/index.html, dated 1957-03-01; Ansel E. Talbert, 'Conquest of Gravity Aim Of Top Scientists in U. S.', New York Herald Tribune, 20 November 1955, page image, https://archive.org/download/talbert1ny/talbert1ny_djvu.txt, dated 1955-11-20.

### Columbus, Ohio

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented, allegation shaped wording as stored.** The federal literature on nitinol, one report of it written by Battelle itself, does not support a Battelle 1948-49 lineage for the alloy. NASA SP-5110, prepared for NASA by Battelle Memorial Institute in 1972, opens: 'Some 10 years ago, Buehler and Wiley of the U.S. Naval Ordnance Laboratory developed a series of engineering alloys that possess a unique mechanical (shape) memory. The generic name of the series of alloys is 55-Nitinol, where Nitinol stands for Nickel Titanium Naval Ordnance Laboratory.' The earliest Naval Ordnance Laboratory nitinol report cited anywhere in its reference list is NOLTR 61-75 of 3 August 1961; US Patent 3,174,851 was filed on 1 December 1961; and NASA CR-1433 of September 1969 records Battelle's own role as a subcontractor to Goodyear Aerospace which 'processed the basic Nitinol rod'. The allegation that Wright-Patterson-sponsored Battelle reports on nickel-titanium alloy from 1948-49 are missing from Air Force and Battelle archives is kept on this board as the allegation it is, and is unsupported by the federal literature opened here. Source: NASA SP-5110, 55-Nitinol: The Alloy With a Memory, Battelle Memorial Institute for NASA, 1972, chapter 1 p. 1 and references 12 and 74, https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf ; NASA CR-1433, Nitinol Characterization Study, September 1969, foreword p. iii and p. 2, https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf ; US Patent 3,174,851, https://patents.google.com/patent/US3174851A/en

Sources added to it: NASA SP-5110, 55-Nitinol: The Alloy With a Memory, C. M. Jackson, H. J. Wagner and R. J. Wasilewski, Battelle Memorial Institute for the NASA Technology Utilization Office, 1972, https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf, dated 1972-01-01; NASA CR-1433, Nitinol Characterization Study, Goodyear Aerospace Corporation report GER 14188 under contract NAS 1-7522 for NASA Langley Research Center, September 1969, https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf, dated 1969-09-01; US Patent 3,174,851, Nickel-base alloys, William J. Buehler and Raymond C. Wiley, assigned to the United States as represented by the Secretary of the Navy, filed 1 December 1961, granted 23 March 1965, https://patents.google.com/patent/US3174851A/en, dated 1965-03-23.

### Malmstrom AFB missile shutdowns, March 1967

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 12 July 2025, at 0:28:33, Robert Salas said one of the documents received from the Air Force is a telex about the Echo Flight shutdown which names by name two individuals working for Boeing, in which SAC headquarters demanded a complete investigation and used the words 'this is of grave concern'. Salas says 'I've got that telex.' This is a different document from the 17 March 1967 Air Force teletype the board already cites. Source: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:28:33, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599
- **Tier 2 named person on the record.** At 0:44:54 to 0:47:25 Salas described the Boeing bench-test result: an injected electrical signal of a given frequency, voltage and duration could make one guidance and control system shut down, but the testers 'had no idea on how that could be injected into this each missile separately within seconds'; the cable run was about eight to nine inches in diameter and 'triply shielded against EMI'; the report concluded an external signal caused the shutdowns while stating they could not explain how it got in; and Salas says he and James Klotz later reached the two named testers, who repeated that they could not explain it. Source: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:44:54 to 0:47:25
- **Tier 2 named person on the record.** At 0:39:39 Salas said he and James Klotz checked with the Department of Energy, cognizant of nuclear testing in Nevada, and that 'There were no nuclear tests on March 16th or March 24th', which on his account removes the nuclear-EMP explanation on the government's own records. He names no document number for the check. Source: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:39:39
- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 12 July 2025, at 0:32:01, Robert Salas said that Ray Fowler was a manager under Sylvania Corporation, which held the contract for the electrical systems at Malmstrom, that Fowler's own contractor staff reported seeing the objects and being involved in the missile shutdowns, and that Fowler passed this to Roy Craig, the Colorado project's chief investigator, with names, dates, places and telephone numbers. Salas presents this as the reason Craig travelled to Malmstrom, and says at 0:32:49 that he holds the Chase interview on audio tape. Source: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)', 12 July 2025, 0:32:01, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599

Sources added to it: American Alchemy with Jesse Michels, 'Air Force Officer: A UFO Shut Down 10 Nukes in Seconds (ft. Bob Salas)' (episode audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL8813107798.mp3?updated=1752514599, dated 2025-07-12.

### Malmstrom AFB missile shutdowns, March 1967

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented, allegation shaped wording as stored.** The unit history this node names as decisive is now open, and it states that the UFO reports were disproven. The 341st Strategic Missile Wing history for 1 January to 31 March 1967 records at page 38: 'Rumors of Unidentified Flying Objects (UFO) around the area of Echo Flight during the time of fault were disproven', and records that a Mobile Strike Team questioned about the morning of 16 March 1967 'stated that no unusual activity or sightings were observed'. It also records that the 801st Radar Squadron, Malmstrom AFB, 'gave a negative report on any radar or atmospheric interference problems related to Echo Flight', and that a comparable multi-facility shutdown had occurred at Alpha Flight on 19 December 1966 with the same capsule crew, adverse weather and a commercial power failure. Source: 341st Strategic Missile Wing History, 1 Jan to 31 Mar 1967, pp. 38 and 40, in the HQ 341st Space Wing FOIA release of 14 June 2001, https://documents.theblackvault.com/documents/ufos/malmstromufo.pdf
- **Tier 1 documented.** The same history records the shutdown itself: on 16 March 1967 at 0845 all sites in Echo Flight shut down with a No-Go indication of Channels 9 and 12 on the Voice Reporting Signal Assembly, all launch facilities in E Flight 'lost strategic alert nearly simultaneously', and no other Wing I configuration lost alert at that time. The section is footnoted throughout to a single classified engineering report of 23 March 1967, which is not in the release. Source: 341st Strategic Missile Wing History, 1 Jan to 31 Mar 1967, p. 32, https://documents.theblackvault.com/documents/ufos/malmstromufo.pdf
- **Tier 1 documented.** No launch control officer is named anywhere in the eighty-seven page release. The only officer named in the Echo Flight section is 'Capt. Bradshaw in the command post', and the names Figel, Salas and Carlson do not appear. Source: HQ 341st Space Wing FOIA release of 14 June 2001, full text searched, https://documents.theblackvault.com/documents/ufos/malmstromufo.pdf

Sources added to it: 341st Strategic Missile Wing histories, 1 Jan to 31 Mar 1967, in the HQ 341st Space Wing FOIA release of 14 June 2001 to John Greenewald Jr, https://documents.theblackvault.com/documents/ufos/malmstromufo.pdf, dated 2001-06-14.

### House Oversight probe into deaths and disappearances of scientists, April 2026

Fields the record forced a change to: claims, cls, desc, removeClaims, sources.

Its description now reads: On 20 April 2026 Oversight Chairman James Comer and Rep. Eric Burlison, chair of the Subcommittee on Economic Growth, Energy Policy and Regulatory Affairs, wrote effectively identical letters to NASA, the FBI, the Department of War and the Department of Energy asking about deaths and disappearances among people with access to sensitive US scientific information. The letters say 'at least ten individuals' and say the pattern 'began in 2023 with the death of Michael David Hicks'; the board previously carried eleven people since 2022, which is the Fox News figure of 21 April 2026 and not the Committee's. The letters also frame their own subject as recent unconfirmed public reporting and footnote every factual assertion in them to the Daily Mail of 11 April 2026 and to New York Post pieces of 9 April, 18 March and 21 March 2026. What they establish is that the Committee asked, and the deadline it set, 27 April 2026. The trigger was the disappearance in February 2026 of retired Air Force Maj. Gen. William Neil McCasland, former commander of the Air Force Research Laboratory at Wright-Patterson, from his Albuquerque home, leaving behind his phone, glasses, hiking boots, wallet and a .38-calibre revolver. Burlison revealed that his own staff had been trying to reach McCasland about a separate congressional investigation before he disappeared; reporting on 28 April indicated the deadline passed without FBI answers. This is the point at which The Program and The Vanishing become the same investigation: the House committee running the UAP inquiry is now also running the missing-scientists inquiry, and the two were connected by the same member and the same disappearance.

Claims the record added:

- **Tier 1 documented.** The Committee's own letters of 20 April 2026 say 'at least ten individuals', not eleven, and date the pattern to a year later than the board did: the letters carry the string 'began in 2023 with the death of Michael David Hicks'. Effectively identical letters went to NASA, the FBI, the Department of War and the Department of Energy over the signatures of Chairman James Comer and Subcommittee Chairman Eric Burlison, copied to Ranking Members Garcia and Frost, and set a response deadline of 27 April 2026. Source: Comer and Burlison to Administrator Jared Isaacman, NASA, 20 April 2026, https://oversight.house.gov/wp-content/uploads/2026/04/NASA-Missing-Scientists-Letter_4.20.26.pdf ; the identical letter to Director Kash Patel, FBI, https://oversight.house.gov/wp-content/uploads/2026/04/FBI-Missing-Scientists-Letter_4.20.26.pdf
- **Tier 1 documented.** The Committee does not adopt the reporting it relays. Its letters frame their own subject as 'recent unconfirmed public reporting' and footnote every factual assertion to the Daily Mail of 11 April 2026 and to New York Post pieces of 9 April, 18 March and 21 March 2026. They ask four agencies whether those reports are true. What the letters establish is that the Committee asked, and the deadline it set. Source: Comer and Burlison to Administrator Jared Isaacman, NASA, 20 April 2026, https://oversight.house.gov/wp-content/uploads/2026/04/NASA-Missing-Scientists-Letter_4.20.26.pdf
- **Tier 2 named person on the record.** Fox News reported on 21 April 2026 that Chairman Comer and Rep. Burlison had launched a congressional probe into eleven individuals in nuclear or rocket technology who had died or vanished since 2022, requesting briefings from the FBI, the Department of War, NASA and the Department of Energy by 27 April 2026. The Committee's own letters, opened on 2 September 2026, say 'at least ten individuals' and date the pattern to 2023; the eleven and the 2022 are what Fox reported. Source: Fox News, 21 April 2026, https://www.foxnews.com/politics/missing-scientists-probe-sparked-after-ufo-general-disappeared-republican-lawmaker-reveals ; checked against the Committee letters of 20 April 2026, https://oversight.house.gov/wp-content/uploads/2026/04/NASA-Missing-Scientists-Letter_4.20.26.pdf
- **Tier 1 documented, allegation shaped wording as stored.** The letters name one of the individuals and describe the reported McCasland link in the Committee's own words: 'Another JPL alum, Monica Reza, who served as the director of the NASA Lab's Materials Processing Group, disappeared while hiking in California in June 2025 and remains missing.' They add that accounts 'have even alleged a direct link between Ms. Reza and General McCasland, characterizing them as having a "close professional connection" through an Air Force-funded research program in the early 2000s.' The Committee attributes both to unconfirmed public reporting. Source: Comer and Burlison to Administrator Jared Isaacman, NASA, 20 April 2026, https://oversight.house.gov/wp-content/uploads/2026/04/NASA-Missing-Scientists-Letter_4.20.26.pdf

Claims the record removed:

- 

Sources added to it: Chairman James Comer and Subcommittee Chairman Eric Burlison to NASA Administrator Jared Isaacman, 20 April 2026, House Committee on Oversight and Government Reform, https://oversight.house.gov/wp-content/uploads/2026/04/NASA-Missing-Scientists-Letter_4.20.26.pdf, dated 2026-04-20; The same letter to FBI Director Kash Patel, 20 April 2026, https://oversight.house.gov/wp-content/uploads/2026/04/FBI-Missing-Scientists-Letter_4.20.26.pdf, dated 2026-04-20; Comer and Burlison Seek Information on Missing Nuclear and Rocket Scientists, press release carrying links to all four letters, https://burlison.house.gov/media/press-releases/comer-burlison-seek-information-missing-nuclear-and-rocket-scientists, dated 2026-04-20.

### National Archives Record Group 615 - UAP Records Collection

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The FAA series in this collection is withheld in part under a named statutory postponement code. The catalog's own metadata export for NAID 493468575 gives access restriction status 'Restricted - Partly' with the specific restriction 'UAP Records Collection Postponement Code 1843(a)(3)' and a use restriction of 'Unrestricted'. The series is titled 'Records from the Federal Aviation Administration Relating to Unidentified Anomalous Phenomena', carries accessions TR-0615-2025-0006 and TR-0615-2025-0008, an extent of 575 portable document files, and is held at the National Archives at College Park, Electronic Records. Source: National Archives Catalog metadata export for NAID 493468575, https://catalog.archives.gov/medialz/bulk-downloads/uaps/JSON/catalog-export-493468575.json

Sources added to it: National Archives Catalog metadata export for the FAA series, NAID 493468575, https://catalog.archives.gov/medialz/bulk-downloads/uaps/JSON/catalog-export-493468575.json, dated 2026-09-02; National Archives, Record Group 615: Unidentified Anomalous Phenomena Records Collection, https://www.archives.gov/research/topics/uaps/rg-615, dated 2026-08-28.

### National Nuclear Security Administration

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 23 April 2025, at 1:08:45, Michels said that a Freedom of Information Act request was sent to the National Nuclear Security Administration for all records that 'mention or relate to' Starfish Prime together with UFO, AP, UAV, AAV or any acronym used by the Atomic Energy Commission at the time for unidentified flying objects, and that the NNSA reply of June 2022 reads 'it was determined that an additional review of your case by the subject matter expert with jurisdiction regarding responsive records was required'. The response letter itself was not opened from this environment and no case number is given on air. Source: American Alchemy with Jesse Michels, 'Presidential Advisor: I Directly Handled UFO Material (Ft. Harald Malmgren)', published 23 April 2025, at 1:08:45

Sources added to it: American Alchemy with Jesse Michels, 'Presidential Advisor: I Directly Handled UFO Material (Ft. Harald Malmgren)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1090282889.mp3?updated=1752180350, dated 2025-04-23.

### Oak Ridge National Laboratory (UT-Battelle, LLC)

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 2 April 2025, at 1:09:33, the retired Senate Armed Services Committee staffer Kirk McConnell said that the contract forming AARO's advisory group 'was let through Oak Ridge' while Sean Kirkpatrick directed AARO. If such a task order exists it would carry a number and appear on USAspending; none was located here. Source: American Alchemy with Jesse Michels, 'Senate Staffer Thinks Tesla and Nazi Technology is Being Hidden (ft. Kirk McConnell)', published 2 April 2025, at 1:09:33

Sources added to it: American Alchemy with Jesse Michels, 'Senate Staffer Thinks Tesla and Nazi Technology is Being Hidden (ft. Kirk McConnell)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9058812583.mp3?updated=1752174755, dated 2025-04-02.

### Office of Naval Intelligence

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 1 March 2026, Gary McKinnon said that on his arrest 'all my data was taken to O&I, Office of Naval Intelligence', that ONI still holds his hard drives, and that he has tried to recover them for years and been told it is an ongoing investigation (0:56:22). Source: American Alchemy with Jesse Michels, 'The Man That Hacked NASA and Found UFOs [Interview w/ Gary McKinnon]', 1 March 2026, 0:56:22 https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6287765066.mp3?updated=1772392329

Sources added to it: American Alchemy with Jesse Michels, 'The Man That Hacked NASA and Found UFOs [Interview w/ Gary McKinnon]', episode audio, https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL6287765066.mp3?updated=1772392329, dated 2026-03-01.

### RAND Corporation

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 23 April 2025, at 0:57:51, Michels said that 'in 1961, the RAND Corporation wrote a report called Some New Considerations Concerning the Nuclear Test Ban, which highlighted the susceptibility of the US ICBM re-entry vehicles to high-energy X-rays', and that this insight fed the Operation Dominic tests. The report was not opened: rand.org answers 403 to this environment and a search on the exact title returned nothing. If it exists it would place RAND in this material seven years before the 1968 Kocher draft with which the node's UFO record currently opens. Source: American Alchemy with Jesse Michels, 'Presidential Advisor: I Directly Handled UFO Material (Ft. Harald Malmgren)', published 23 April 2025, at 0:57:51

Sources added to it: American Alchemy with Jesse Michels, 'Presidential Advisor: I Directly Handled UFO Material (Ft. Harald Malmgren)' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL1090282889.mp3?updated=1752180350, dated 2025-04-23.

### Special Access Program Oversight Committee (SAPOC)

Fields the record forced a change to: claims, cls, dateStart, desc, sources.

The board once carried a sentence that the record replaced. The corrections file states: dateStart moves from 2010-07-01 to 1994-01-05, and one sentence of the desc changes. The exact sentence replaced is: The SAPOC was established by DoD Directive 5205.07 on 1 July 2010 to 'advise and assist the Secretary of Defense (SecDef) and the Deputy Secretary of Defense with governance, management, and oversight of DoD SAPs', and it survives in the 12 September 2024 reissue as 'the senior governing body of the DoD SAP Enterprise'. merge.py's _corrections branch does not carry dateStart, so the same change is made at source in research/w2-sap-architecture.json, which is the only research file that declares it.

Its description now reads: The SAPOC was established on 5 January 1994, not in 2010. A Deputy Secretary of Defense information bulletin of November 1994 records that 'On January 5th, 1994, the Deputy Secretary of Defense (DEPSECDEF) significantly enhanced changes in the DoD Special Access Program (SAP) management and control structures' and that the plan 'standardized and formalized the SAP approval, termination, revalidation and restructuring process through the Special Access Program Oversight Committee (SAPOC). A Senior Review Group (SRG) was established to support the SAPOC principals'; the Joint Security Commission called it a 'recent formation' on 28 February 1994. DoD Directive 5205.07 of 1 July 2010 is therefore a later instrument that re-established a committee which had been running for sixteen years, and it survives in the 12 September 2024 reissue as 'the senior governing body of the DoD SAP Enterprise'. Under the 2013 instruction its chair is the Deputy Secretary of Defense, its vice-chair the Under Secretary of Defense for Acquisition, Technology and Logistics, and its executive secretary the Director of DoD SAPCO; its general membership is the Under Secretaries for Policy, Comptroller/CFO, Intelligence, and Personnel and Readiness, the Vice Chairman of the Joint Chiefs of Staff, the DoD Chief Information Officer, the General Counsel of the Department, the Director of Cost Assessment and Program Evaluation, the Under Secretaries of the Army, Navy and Air Force, the Vice Chiefs of Staff of the Army and Air Force, the Vice Chief of Naval Operations and the Assistant Commandant of the Marine Corps. Its three primary functions are to review issues on which the Senior Review Group could not reach unanimity, to ensure combatant command warfighting needs are reflected in SAP programmatics and budgets, and - the function that matters here - to 'Conduct an annual review and validation of SAP reports sent to the Congressional defense and intelligence committees'. In other words, the document Congress receives about special access programs is written and validated by a committee of roughly eighteen senior officials of the Department the report is about, chaired by the same official who signs the carve-outs. This is the body whose membership a witness alleging concealment would have to say was either complicit or itself deceived; DoD's own directive makes that a binary with no third option.

Claims the record added:

- **Tier 2 named person on the record.** The committee was established on 5 January 1994, sixteen years before the directive this node cites. A Deputy Secretary of Defense information bulletin of November 1994 states: 'On January 5th, 1994, the Deputy Secretary of Defense (DEPSECDEF) significantly enhanced changes in the DoD Special Access Program (SAP) management and control structures. ... The plan standardized and formalized the SAP approval, termination, revalidation and restructuring process through the Special Access Program Oversight Committee (SAPOC). A Senior Review Group (SRG) was established to support the SAPOC principals.' Tier 2 because the text opened is a transcription published by the Federation of American Scientists and no scan of the original bulletin was found from this environment. Source: Deputy Secretary of Defense, Special Access Program Oversight Committee, Information Bulletin, November 1994, as transcribed at https://sgp.fas.org/othergov/sapoc.html
- **Tier 2 named person on the record.** The annual review and validation function this node attributes to the 2010 directive is in the 1994 bulletin: 'All SAPs will be reviewed and validated annually for continued SAP status by the OSD SAPOC. ... The DEPSECDEF is the final decision maker in establishing, disestablishing or restructuring SAPs.' Source: Deputy Secretary of Defense, SAPOC Information Bulletin, November 1994, https://sgp.fas.org/othergov/sapoc.html
- **Tier 2 named person on the record.** The 1994 membership was five principals and an executive secretary, not the roughly eighteen of the later instruction: 'The SAPOC is chaired by the Honorable John Deutch, DEPSECDEF, with permanent members the Honorable Paul Kaminski USD(A&T), the Honorable Walter Slocombe USD(P), ADM William A. Owens, VCJCS, and the Honorable Emmett Paige Jr., ASD(C3I). BGEN Mike Kostelnik, OUSD(A&T), serves as both member and executive secretary to the SAPOC in his capacity as director of the SAPCO (SAP Coordinating Office). SAPOC membership is not further delegable.' The node's argument about a large in-house validating body describes the later era, not this one. Source: Deputy Secretary of Defense, SAPOC Information Bulletin, November 1994, https://sgp.fas.org/othergov/sapoc.html
- **Tier 1 documented.** A commission chartered by the Secretary of Defense and the Director of Central Intelligence corroborated the formation within two months: 'Until recently there has been no procedure for centralized assessment of special program proposals submitted directly to the Deputy Secretary of Defense by the military departments. The recent formation of the DoD Special Access Program Oversight Committee, which the Commission fully supports, will ensure that every program is reviewed by a panel of senior officials prior to its establishment, and annually thereafter, to determine whether compartmentation for each program is still required.' Source: Joint Security Commission, Redefining Security: A Report to the Secretary of Defense and the Director of Central Intelligence, 28 February 1994, chapter 2, https://sgp.fas.org/library/jsc/chap2.html

Sources added to it: Deputy Secretary of Defense, Special Access Program Oversight Committee Information Bulletin, November 1994 (FAS transcription), https://sgp.fas.org/othergov/sapoc.html, dated 1994-11-01; Joint Security Commission, Redefining Security, chapter 2, Classification Management, https://sgp.fas.org/library/jsc/chap2.html, dated 1994-02-28.

### Special Access Program Oversight Committee (SAPOC)

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** A central Army special-access oversight office predates the 1994 reform by ten years. GAO/NSIAD-88-152 records: 'A DOD review of Army special access programs in 1983 revealed systemic weaknesses in various management areas, which resulted in establishment of a central oversight office in September 1984.' The same report states that in 1988 'The Deputy Under Secretary of Defense for Policy is required to maintain a listing of all special access programs, but does not do so because of security concerns', and that 'the Secretary's Office has no centralized office with cognizance of all special access programs'. The January 1994 dates this board carries stand; the Army aftermath began in 1983-84. Source: GAO/NSIAD-88-152, B-230522, 24 May 1988, Results in Brief and Recommendations, https://www.gao.gov/assets/nsiad-88-152.pdf

Sources added to it: GAO/NSIAD-88-152, Special Access Programs: DOD Criteria and Procedures for Creating Them Need Improvement, B-230522, 24 May 1988, https://www.gao.gov/assets/nsiad-88-152.pdf, dated 1988-05-24.

### Skywatcher

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 28 May 2025, Michels introduces his guest at 0:02:33 with 'I'm here with James Fowler', and at 0:05:12 Fowler said he 'started out in the military', 'retired as a sergeant major, retired in 2020', spent 'about 23 years working for the government', and that after retiring he 'started several companies and some of my companies were contracted by the government to do different war game projects'. Source: American Alchemy with Jesse Michels, 'Meet The Startup Summoning UFOs: Skywatcher', published 28 May 2025, at 0:02:33 and 0:05:12
- **Tier 2 named person on the record.** In the same episode, at 0:05:12 and again at 0:08:35, Fowler said the effort began with an observation during a government war game he was running in 2021, whose deliverable was tactics, with a blue team fielding air-defence and counter-drone systems against a red team, and that on the last day of the event his camera operator showed him 'the class one formation of seven, the first sighting we had'. At 0:06:04 he said he is 'the lead operations guy' and not the discoverer, naming two colleagues only as Mr. K and Mr. D because they wish to remain anonymous. Source: American Alchemy with Jesse Michels, 'Meet The Startup Summoning UFOs: Skywatcher', published 28 May 2025, at 0:05:12 to 0:10:17

Sources added to it: American Alchemy with Jesse Michels, 'Meet The Startup Summoning UFOs: Skywatcher' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/HPL9721579354.mp3?updated=1752253202, dated 2025-05-28.

### Sperry Rand Corporation

Fields the record forced a change to: claims, cls, desc, sources.

Its description now reads: Sperry Rand is a narrow item and a clean one: a five-star officer chairing a defence prime while the alleged programme period runs. The company's own 1956 publication carries a signed statement attributed to 'General of the Army Douglas MacArthur, Chairman of the Board, Sperry Rand Corporation', and a New York Journal-American column of 17 January 1957, preserved in CIA records, reports that 'Gen. Douglas MacArthur, who will be 77 next week, is active as chairman of the board of Sperry Rand.'

That column is the more useful artefact, because it inventories the same pipeline in a single paragraph: Halsey at International Tel and Tel, Lucius Clay at Continental Can, Ira Eaker at Hughes Tool, Doolittle at Shell Oil and on the Air Force Scientific Advisory Board and the President's Foreign Intelligence Board, Ennis Whitehead at Northrop, J. B. Montgomery at General Electric. Thirteen further instances of the general-officer-to-prime-contractor movement, in one citable contemporaneous document held by CIA.

Two corrections travel with it. The company was not called Sperry Rand in 1986: it had been Sperry Corporation since 1979, and it was Sperry Corporation that Burroughs absorbed. SEC's own record shows CIK 0000746838 changing its conformed name from BURROUGHS CORP /DE/ on 4 December 1986, and Unisys carrying Sperry's obligations thereafter, including its sale of the Sperry Aerospace Group that same month. No UAP claim attaches to this node from any document opened for it; the only claim of that kind located is testimonial, and it is recorded below.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 21 February 2025, at 0:24:35, the guest Sammy, known as UAP Gerb, said that on Philip J. Corso's account Roswell-derived material was distributed for civil and commercial use through 'Bell Labs, Sperry Rand', and thence through its divisions to 'Northrop, Lockheed, Martin, Raytheon, and others'. This is a report of what Corso wrote, not a document, and no contemporaneous record naming Sperry Rand in that role was opened. Source: American Alchemy with Jesse Michels, 'The Most Knowledgeable UFO Researcher In The World', published 21 February 2025, at 0:24:35

Sources added to it: American Alchemy with Jesse Michels, 'The Most Knowledgeable UFO Researcher In The World' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE8993457707.mp3?updated=1751590849, dated 2025-02-21.

### STAR GATE and predecessor remote viewing programs, 1970-1995

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** On American Alchemy with Jesse Michels, 2 March 2025, between 1:13:18 and 1:49:19, Joseph McMoneagle described his own route into the programme as a chain of individual postings rather than a fixed bureaucratic assignment: a chance contact on an Army base, intelligence school, Vietnam service, a red-team task at an Allied intelligence facility in Germany, an order to headquarters by a three-star general, a diversion into Mandarin training at the Defense Language Institute, and an abrupt reassignment by a different general to look at Grill Flame at SRI before being absorbed at Fort Meade. He presents this as evidence that the programme moved by the personal patronage of particular general officers. Source: American Alchemy with Jesse Michels, 'CIA Psychic Spy: Mars Used To Have Alien Life', published 2 March 2025, at 1:13:18 to 1:49:19
- **Tier 1 documented.** The 1995 evaluation that closed the programme is titled 'AN EVALUATION OF REMOTE VIEWING: RESEARCH AND APPLICATIONS', was prepared by the American Institutes for Research and is dated September 29, 1995; it is released as CIA-RDP96-00791R000200180006-4. Its authors are Michael D. Mumford, Andrew M. Rose and David A. Goslin. Jessica Utts and Ray Hyman are the two expert reviewers rather than authors: Chapter Three carries 'Review 1 (Dr. Jessica Utts)', 'Review 2 (Ray Hyman)' and 'The Reply (Dr. Jessica Utts)'. Source: American Institutes for Research, 'An Evaluation of Remote Viewing: Research and Applications', 29 September 1995, CIA-RDP96-00791R000200180006-4, title page and table of contents https://archive.org/download/cia-readingroom-document-cia-rdp96-00791r000200180006-4/cia-rdp96-00791r000200180006-4_djvu.txt
- **Tier 1 documented.** The report's Executive Summary states: 'Most importantly, the information provided by remote viewing is vague and ambiguous, making it difficult, if not impossible, for the technique to yield information of sufficient quality and accuracy for actionable intelligence.' It adds that in no case had the information provided ever been used to guide intelligence operations, and concludes that 'continued use of remote viewing in intelligence gathering operations is not warranted.' Source: American Institutes for Research, 'An Evaluation of Remote Viewing: Research and Applications', 29 September 1995, CIA-RDP96-00791R000200180006-4, Executive Summary pages E-4 to E-5 https://archive.org/download/cia-readingroom-document-cia-rdp96-00791r000200180006-4/cia-rdp96-00791r000200180006-4_djvu.txt

Sources added to it: American Alchemy with Jesse Michels, 'CIA Psychic Spy: Mars Used To Have Alien Life' (audio), https://mgln.ai/e/1119/pscrb.fm/rss/p/traffic.megaphone.fm/TOE9049615871.mp3?updated=1751593011, dated 2025-03-02; American Institutes for Research, 'An Evaluation of Remote Viewing: Research and Applications', 29 September 1995, CIA-RDP96-00791R000200180006-4, full text via the archive.org mirror of the CIA reading room, https://archive.org/download/cia-readingroom-document-cia-rdp96-00791r000200180006-4/cia-rdp96-00791r000200180006-4_djvu.txt, dated 2026-09-02.

### STAR GATE and predecessor remote viewing programs, 1970-1995

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The CENTER LANE project office was the Security Support Detachment, not the Systems Exploitation Detachment. The memorandum submitting the CENTER LANE FY86 to FY90 General Defense Intelligence Program initiative is headed 'DEPARTMENT OF THE ARMY / SECURITY SUPPORT DETACHMENT / USAINSCOM, 902D MILITARY INTELLIGENCE GROUP / FORT GEORGE G. MEADE, MARYLAND 20755', office symbol IAGPA-F-SD, and is signed by a lieutenant colonel of Military Intelligence as CENTER LANE Project Manager. The same office symbol heads the July 1984 information paper on the project's cancellation. Source: Memorandum, CENTER LANE FY 86 - 90 GDIP Submission (U), 4 April 1984, CIA-RDP96-00788R001600450002-5, https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001600450002-5/cia-rdp96-00788r001600450002-5_djvu.txt
- **Tier 1 documented.** The Army staff started the work and paid for the first contract in 1978, and INSCOM dates its own entry to 1977. A talking paper records that 'ACSI & MG Rolya agreed that INSCOM would "check out" parapsychology phenomen[a], and that Army Intelligence would obligate $75 K to support an SRI Subject selection and training program for INSCOM personnel over the next year'. The 1984 GDIP memorandum states: 'Since the beginning of USAINSCOM's exploitation of psychoenergetics (PE) technology with Project GRILL FLAME in 1977 through the present effort under CENTER LANE, the project has been conducted on an ad hoc basis, using resources taken "out of hide."' Source: Talking paper, INSCOM Involvement in Remote Viewing (DoD Project GRILL FLAME), with milestone attachment dated 24 Nov 78, CIA-RDP96-00788R001200410023-0, https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001200410023-0/cia-rdp96-00788r001200410023-0_djvu.txt ; Memorandum, CENTER LANE FY 86 - 90 GDIP Submission (U), 4 April 1984, CIA-RDP96-00788R001600450002-5, https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001600450002-5/cia-rdp96-00788r001600450002-5_djvu.txt

Sources added to it: CENTER LANE FY 86 - 90 GDIP Submission (U), 4 April 1984, CIA-RDP96-00788R001600450002-5, https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001600450002-5/cia-rdp96-00788r001600450002-5_djvu.txt, dated 1984-04-04; INSCOM Involvement in Remote Viewing (DoD Project GRILL FLAME), talking paper, Nov 1978, CIA-RDP96-00788R001200410023-0, https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001200410023-0/cia-rdp96-00788r001200410023-0_djvu.txt, dated 1978-11-24.

### STAR GATE and predecessor remote viewing programs, 1970-1995

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** GRILL FLAME's transfer to INSCOM has a date and an office. The INSCOM Annual Historical Review for FY 1981 records: 'On 11 February 1981, ACSI formally transferred the GRILL FLAME program management responsibili[ty] to INSCOM where it was assigned to Detachment G, US Army Operational Group.' The same review's unit appendix for 30 September 1981 lists the US Army Operational Group and does not list any Intelligence Support Activity. Source: Annual Historical Review, US Army Intelligence and Security Command, FY 1981, pp. 89 to 90, released 11 September 2018, https://www.governmentattic.org/30docs/USAINSCOMhistoryFY_1981.pdf
- **Tier 1 documented.** A seventh cryptonym belongs in the sequence. The DIA SUN STREAK Project's FY 86 congressional budget justification book line is given as 'identified as DRAGOON ABSORB' in the memorandum of 8 April 1985 recommending a twelve-person prototype operational group. Source: Operational Readiness of the SUN STREAK Prototype Operational Group, 8 April 1985, CIA-RDP96-00789R002100130001-4, https://archive.org/details/cia-readingroom-document-cia-rdp96-00789r002100130001-4
- **Tier 1 documented.** The 1995 declassification review was the CIA's own, not the veterans'. An Office of Research and Development memorandum to CIA Public Affairs of 12 June 1995 answers 'Who is conducting the review?' with: 'The CIA's Office of Research and Development with the aid of a blue ribbon panel of experts in the behavioral sciences at the American Institutes for Research.' A second ORD paper of 20 June 1995 records the choice as deliberate: 'Our strategy was to ask the US Army and the National Research Council to form a blue ribbon panel similar to the group that completed a study for the Army in the late 1980's. We also proposed to declassify past CIA sponsorship and to further declassify other program material.' Source: CIA memorandum, 12 June 1995, CIA Remote Viewing Declassification, CIA-RDP96-00791R000100030062-7, https://archive.org/details/cia-readingroom-document-cia-rdp96-00791r000100030062-7 ; ORD-0289-95, 20 June 1995, Star Gate - Program Status, Proposed Options, CIA-RDP96-00791R000100160003-8, https://archive.org/details/cia-readingroom-document-cia-rdp96-00791r000100160003-8
- **Tier 1 documented.** The programme was six people at the end: 'The DIA program consists of three operational remote viewers and three management and support personnel. DIA also funded a related R&D effort with SAIC for several years, ending in 1994.' Source: ORD-0289-95, 20 June 1995, CIA-RDP96-00791R000100160003-8, https://archive.org/details/cia-readingroom-document-cia-rdp96-00791r000100160003-8
- **Tier 1 documented.** The release withholds the unit's people, so no claim that a named member appears in it can be checked from the collection itself. Session forms print labelled fields for Remote Viewer, Interviewer and Observer and leave all three blank, and narrative memoranda substitute CIA release codes (SG1A, SG1B, SG1I, SG1J, SGFOIA3) for personal names. Source: Remote Viewing Session Data, session of 15 December 1987, CIA-RDP96-00789R001600120001-1, https://archive.org/details/cia-readingroom-document-cia-rdp96-00789r001600120001-1

Sources added to it: Annual Historical Review, US Army Intelligence and Security Command, FY 1981, INSCOM History Office, released 11 September 2018 after mandatory declassification review, https://www.governmentattic.org/30docs/USAINSCOMhistoryFY_1981.pdf, dated 2018-09-11; CIA memorandum, 12 June 1995, CIA Remote Viewing Declassification, CIA-RDP96-00791R000100030062-7, https://archive.org/details/cia-readingroom-document-cia-rdp96-00791r000100030062-7, dated 1995-06-12; ORD-0289-95, 20 June 1995, Star Gate - Program Status, Proposed Options, CIA-RDP96-00791R000100160003-8, https://archive.org/details/cia-readingroom-document-cia-rdp96-00791r000100160003-8, dated 1995-06-20; Operational Readiness of the SUN STREAK Prototype Operational Group, 8 April 1985, CIA-RDP96-00789R002100130001-4, https://archive.org/details/cia-readingroom-document-cia-rdp96-00789r002100130001-4, dated 1985-04-08; Remote Viewing Session Data, session of 15 December 1987, CIA-RDP96-00789R001600120001-1, https://archive.org/details/cia-readingroom-document-cia-rdp96-00789r001600120001-1, dated 1987-12-15.

### uap-science-advisory-council-2026

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 2 named person on the record.** Avi Loeb's first Medium post on the UAP Science Advisory Council carries article:published_time 2026-06-13T16:20:50Z. His second post, 'More Details on the UAP Science Advisory Council', carries a byline of 16 June 2026; the 29 June 2026 date that has circulated is that post's republish timestamp, not its publication date. Source: https://avi-loeb.medium.com/a-uap-science-advisory-council-to-the-u-s-f7262e57b0df

Sources added to it: https://avi-loeb.medium.com/a-uap-science-advisory-council-to-the-u-s-f7262e57b0df

### 10 U.S.C. 119, Special Access Programs: Congressional Oversight

Fields the record forced a change to: claims, cls, sources.

Claims the record added:

- **Tier 1 documented.** The annual reporting requirements in subsections (a) and (b) TERMINATED effective 31 December 2021. The statutory note reads: 'For termination, effective Dec. 31, 2021, of provisions in subsecs. (a) and (b) of this section requiring submittal of annual report to Congress, see section 1061 of Pub. L. 114-328, set out as a note under section 111 of this title.' Subsections (c) through (g) survive, and (e)(1) still cross-references the terminated (a) and (b). Source: https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section119&num=0&edition=prelim

Sources added to it: https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section119&num=0&edition=prelim

### The Wilson-Davis Notes (16 October 2002)

Fields the record forced a change to: claims, cls, desc, sources.

The board once carried a sentence that the record replaced. The corrections file states: Only one sentence of the desc changes. The exact sentence replaced is: Fifteen pages of handwritten notes made by the astrophysicist Eric W. Davis on 16 October 2002, recording what retired Vice Admiral Thomas R. Wilson - former Joint Staff J-2 and, until months earlier, Director of the Defense Intelligence Agency - told him at a meeting reported to have taken place at an EG&G facility in Las Vegas.

Its description now reads: Fifteen typed pages headed 'EWD NOTES', made by the astrophysicist Eric W. Davis on 16 October 2002, recording what retired Vice Admiral Thomas R. Wilson - former Joint Staff J-2 and, until months earlier, Director of the Defense Intelligence Agency - told him at a meeting reported to have taken place at an EG&G facility in Las Vegas; two of the fifteen pages, numbered 3 and 4, are not Davis's notes at all but a paper-clipped letter from Will Miller on United States Navy letterhead dated 25 April 2002, flagged in the notes themselves at the foot of page 2 as '[paper-clipped letter here]'. The notes describe Wilson learning in 1997 of a special access programme holding recovered material of non-human origin in the custody of an aerospace contractor; obtaining a meeting with the programme's gatekeepers, described as a programme security officer, a contractor programme manager and a lawyer; and being refused the read-on because he lacked need-to-know. The notes surfaced publicly in 2019 from material connected to the estate of Apollo 14 astronaut Edgar Mitchell. Davis has confirmed the notes are his. Wilson denies the meeting and its substance. Members of the House Intelligence subcommittee raised the memo directly with Pentagon witnesses at the 17 May 2022 UAP hearing and were told the witnesses were unaware of it. No official US government publication - including AARO's 2024 Historical Record Report Volume I - has ever addressed the document. The board records it in full because its central mechanism (a cleared senior official refused access by contractor gatekeepers) is the same mechanism sworn to by David Grusch in July 2023, and because a document whose author is alive and identified and whose subject is alive and identified is a resolvable question that no institution has chosen to resolve.

Claims the record added:

- **Tier 1 documented.** The published document is typed, not handwritten, and two of its fifteen pages are somebody else's letter. The copy in public circulation is fifteen typed pages headed 'EWD NOTES', then '10/16/02', then 'Eric Davis Meeting with Adm. Wilson', numbered 1 to 15 at the foot. Pages 3 and 4 are a two page letter on United States Navy letterhead dated April 25, 2002, from Belleair Bluffs, Florida, to 'Dr. Eric W. Davis, CEO, Warp Drive Metrics', signed 'Will Miller'; the notes flag it at the foot of page 2 as '[paper-clipped letter here]'. Source: The Wilson-Davis notes as published, fifteen pages, read image by image, https://documents2.theblackvault.com/casefiles/wilsonleak.pdf
- **Tier 1 documented.** Brig. Gen. Steven Lovekin is not in the published notes. All fifteen pages were read image by image: Wilson, Davis, Steven Greer, Will Miller and Edgar Mitchell are in them and Lovekin is not. Source: The Wilson-Davis notes as published, all fifteen pages, https://documents2.theblackvault.com/casefiles/wilsonleak.pdf
- **Tier 1 documented.** The notes give the correspondent no rank, no service and no first name beyond 'Will', and his letter carries no rank block, so the 'Cdr. Willard Miller, USN' form used across the podcast corpus is not supported by the document it is drawn from. In the letter he writes: 'Although I have held a Top Secret (TS) clearance with access to Special Compartmented Information (SCI), and other "special" clearances for "other" programs, I currently do not work in the classified realm, nor do I hold those clearances.' Source: The Wilson-Davis notes as published, pp. 3 to 4, https://documents2.theblackvault.com/casefiles/wilsonleak.pdf

Sources added to it: The Wilson-Davis notes as published (EWD NOTES, 10/16/02, Eric Davis Meeting with Adm. Wilson), fifteen pages, The Black Vault case files, https://documents2.theblackvault.com/casefiles/wilsonleak.pdf, dated 2002-10-16.

### YANKEE BLUE (alleged AFOSI indoctrination program)

Fields the record forced a change to: claims, cls, cluster, desc, label, sources, sub, tier.

Its label now reads: YANKEE BLUE (alleged AFOSI indoctrination program).

Its one line summary now reads: Alleged USAF/AFOSI program.

Its description now reads: YANKEE BLUE is the allegation that the US Air Force ran a fake UFO reverse-engineering programme on its own personnel, briefing officers in classified units into believing they had been read on to a recovery effort, using fabricated material, as a counterintelligence or hazing exercise. If documented it would be the strongest single item in the coverup strand, because it is the government generating false UAP belief inside its own ranks. It is not documented. A full-text search of the released AARO Historical Record Report Volume I (63 pp., March 2024) finds no occurrence of the term, and it appears in none of the FY2023, FY2024 or FY2025 consolidated annual reports, which corrects a widely repeated claim, including one this board previously made, that AARO conceded the programme in Volume I. Two FOIA cases have returned negative: OSD case 25-F-3514 (September 2025) reported no responsive records after searches of the electronic and paper holdings, and AFOSI case 2025-06002-F reported no investigative reports, summaries or closure memoranda. On 1 October 2025 Pentagon spokesperson Susan Gough stated she could not confirm the alleged memorandum. The Department reportedly reopened the search in December 2025 with no published result. The programme is retained on the board at Tier B with the allegation graded Tier 3 and the negative FOIA findings graded Tier 1. A negative primary finding is itself a documented fact and belongs on a board about concealment, but it is a finding about the absence of a record, not a record.

Claims the record added:

- **Tier 1 documented.** A full-text search of the released AARO Historical Record Report Volume I returns no occurrence of 'Yankee Blue'. The term is likewise absent from the FY2023, FY2024 and FY2025 consolidated annual reports. Source: AARO HRR Vol I, March 2024, full text; AARO annual reports FY2023-FY2025
- **Tier 3 stated inference.** The claim that AARO acknowledged Yankee Blue in Volume I is widely repeated in reporting and was asserted on this board until 12 Aug 2026. It does not survive a full-text check of the document. Source: Correction logged 12 Aug 2026; see notes/WAVE3_QUEUE.md

Sources added to it: AARO, Report on the Historical Record of U.S. Government Involvement with UAP, Volume I (March 2024), https://media.defense.gov/2024/Mar/08/2003409233/-1/-1/0/DOPSR-CLEARED-508-COMPLIANT-HRRV1-08-MAR-2024-FINAL.PDF, dated 2024-03-08; Archived capture of HRR Volume I, https://web.archive.org/web/20260811042323id_/https://media.defense.gov/2024/Mar/08/2003409233/-1/-1/0/DOPSR-CLEARED-508-COMPLIANT-HRRV1-08-MAR-2024-FINAL.PDF, dated 2026-08-11; Joel Schectman and Aruna Viswanatha, 'The Pentagon Disinformation That Fueled America's UFO Mythology', The Wall Street Journal, 6 June 2025. The canonical address https://www.wsj.com/politics/national-security/ufo-us-disinformation-45376f7e is unreachable from this environment; the text was read in the To Vima republication at this URL., https://www.tovima.com/wsj/the-pentagon-disinformation-that-fueled-americas-ufo-mythology/, dated 2025-06-06; Robert Salas, 'OPINION | A Rebuttal from Robert Salas of Ojai to Wall Street Journal's June 6 article: America's UFO Mythology', Ojai Valley News, published 10 June 2025, https://www.ojaivalleynews.com/news/opinion-a-rebuttal-from-robert-salas-of-ojai-to-wall-street-journal-s-june-6/article_81c5493f-3c22-407f-ac1a-46b3009d1dea.html, dated 2025-06-10.

## What is still missing

The corrections pass also wrote down what it could not settle. These are open gaps, recorded rather than papered over.

- Yankee Blue: the alleged AFOSI memorandum remains unreleased. Wave 4 targets are the DoD FOIA case file for the reopened December 2025 search, AFOSI FOIA logs at osi.af.mil, and any SASC or House Oversight correspondence naming the programme.
- Sec. 1102 of S.2226 Div M: the section HEADING and placement are verified against the govinfo engrossed text, but web_fetch caps extraction at ~118,600 characters and the engrossed body (pages 2368-2374) could not be read verbatim. The make-available-to-AARO mandate is corroborated by a contemporaneous section-by-section locator, not read directly. This is the soft joint in the citation and should be closed with a direct read of the printed bill.
