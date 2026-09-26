# Brief: classify board links into controlled predicates

You are one of several classifiers working in parallel. This brief is self-contained. (Round 2: the vocabulary and the tie-breakers below were revised after round 1.)

## What the board is

A research board mapping the alleged legacy UAP recovery programme. It is a graph: nodes (people,
institutions, programmes, locations, legislation, documents, events, and "domain" nodes that stand
for a topic) joined by edges. Each edge has one of twelve coarse types (institutional, funding,
custody, programmatic, legislative, research, investigative, witness-chain, behavioral, denial,
temporal, geographic), a short **sentence** saying what the link is, a longer **note**, and a
claim **tier** (1 documented, 2 a named person on the record, 3 an inference).

The board is adding a controlled verb, a **predicate**, to every edge, plus a **direction**: which
end the verb reads from. A reader on a node's page will see links as sentences, for example
"Harry Reid **sponsored** AAWSAP" from one end and "AAWSAP **was sponsored by** Harry Reid" from the
other. Your answers become those sentences, so they must be true restatements of the edge.

## Your input

A JSON file of edge packets. Each packet:

```
{"id": "e-0123456789",
 "a": {"id": "...", "label": "...", "cls": "person"},
 "b": {"id": "...", "label": "...", "cls": "document"},
 "type": "research", "sentence": "authored by", "note": "...", "tier": 1,
 "authoredVerb": "authorship"            (only on some edges: the verb the researcher wrote)
 "denialKind": "directed", "denier": "..." (only on denial-type edges)}
```

## The rules

1. **Choose the most specific predicate the edge's own sentence supports.** Read the sentence
   first; use the note for context and to settle direction. If the sentence is empty, use the note.
2. **Direction.** `subject` is `"a"` or `"b"`: the end the predicate's FORWARD label reads from.
   Test every answer by reading it aloud: `<subject label> <forward label> <object label>` must be
   a true restatement of the edge. The record order (a, b) often does NOT match the natural
   direction: "Pulsed High-Power Microwave (a) / James Wells (b): authored by" is
   `wrote` with subject `"b"` (James Wells wrote the document). For symmetric predicates
   (same_as, worked_with, in_contact_with, parallels, alleged_tie, concurrent_with, connected_to) the subject is always `"a"`.
3. **Classes.** The subject's class must be in the predicate's subject classes and the object's
   class in its object classes. A `domain` node is allowed at either end of every predicate. If
   your first choice does not fit the classes, choose the best one that does.
4. **The type is a hint, not a rule.** Prefer a predicate that refines the edge's own type, but
   when the sentence plainly says something else, follow the sentence (an `institutional` edge
   saying "Low wrote the memo" is `wrote`). Do not force a sentence into its type.
5. **Denials.** Where the packet names a `denier` (a node id equal to `a` or `b`), a predicate from
   the Denials family (denied, refused, disputed, explained_away, omitted) MUST have the denier as its
   subject. Never make the adjudicated denier the object of a Denials predicate. If the sentence is
   really about something else, choose the predicate that says so. Where `denialKind` is
   `association` or `undirected`, or `denier` is null, nobody is adjudicated as the denier: read
   the direction from the sentence, and prefer `disputed`, `contradicts` or `parallels` for two
   positions in conflict.
6. **Allegation stays allegation.** Do not upgrade a claim into a fact. If the sentence says a
   thing is alleged, claimed or said, choose a predicate that keeps that (alleged_to_hold,
   made_claims_about, witnessed which reads "gave a first-hand account of") rather than one that
   asserts the thing (holds, ran, funded). The tier itself does not decide the predicate.
7. **`connected_to` only when nothing fits.** It should be rare: under 3% of edges. The Board's
   reading family (exemplifies, parallels, affects) exists for the board's own analytic links,
   and `concerns` for a document about something; use those before `connected_to`.
8. **No outside knowledge.** Use only the packet: the two labels and classes, the type, the
   sentence, the note and the verb. Do not look anything up and do not use what you know about
   these people or events.
9. **Confidence, honestly.** `high`: the sentence states the relation plainly and the direction
   is clear. `medium`: a reasonable reading, but another predicate is close or the direction takes
   some inference. `low`: a guess; the sentence is ambiguous, analytic or unclear. Low answers are
   all re-checked by a reviewer, so do not inflate.

## Worked examples

- a Harold Puthoff (person), b SRI International (institution), institutional: "Puthoff founded and
  led the SRI psychoenergetics programme" -> `led`, subject a, medium (founded is close; the
  object here is SRI, where he led a programme).
- a AAWSAP (program), b a DIRD (document), programmatic: "AAWSAP deliverable" -> `produced`, subject a, high.
- a Foreign Technology Division, b NASIC, institutional: "NASIC is the later name" -> `succeeded`,
  subject b (NASIC succeeded FTD), high.
- a Roger Ramey (person), b RAAF Press Release (document), denial, denier roger-ramey: "Ramey
  retracted the disc announcement the same day" -> `denied`, subject a, high.
- a Paul Bennewitz (person), b AARO historical record Vol I (document), denial, denier
  aaro-historical-record-vol1: "AARO's review makes no mention of Bennewitz" -> `omitted`,
  subject b, high.
- a Langley AFB (location), b Langley 2023 incursions (event), geographic: "site of the incursions"
  -> `occurred_at`, subject b, high.
- a SASC (institution) is one of the committees in b's group: `member_of` with the committee as subject.
- a d-contracting-style domain node at either end with an analytic sentence ("a company stood up
  to hold a single government contract") -> `exemplifies`, subject = the non-domain end, high.

## Tie-breakers between close predicates (read before classifying)

A first round with two independent classifiers disagreed on about a third of edges, almost all between
near-synonyms. These rules settle the common pairs. Apply them exactly.

- **Seats vs jobs.** A seat on a committee, board, panel, caucus, council, task force or group,
  including chair and ranking-member seats of a committee, is `member_of`. A job, office, rank or
  post in an organisation is `held_post`. Heading the whole body (director, commander, chair of a
  body that is itself the object) is `led`. A founding director is `led` unless the sentence says
  founded.
- **Stated exclusion.** "not a member", "outside the reach of", "not covered by", "no entitlement
  under", "never reported by" -> `outside_of`, with the excluded thing as subject. Never
  `connected_to` or `affects` for an exclusion.
- **Making public.** The subject issued it as its own publication or broadcast -> `published`. The
  subject was the first route by which something reached the public or the record (leaked,
  surfaced, obtained by FOIA, entered into the Congressional Record, printed in facsimile, issued a
  press release carrying a claim) -> `brought_to_record`. Journalism or broadcast coverage about
  something -> `reported_on`. An agency releasing its own holdings -> `released`. "published and
  holds" -> `published`. Use `holds` only when the sentence is about custody.
- **About vs asserting vs citing.** A document or event that is about, names, lists or records the
  object, asserting nothing contested -> `concerns`. A subject that asserts, alleges, argues a
  thesis or names someone as involved -> `made_claims_about` (or `alleged_tie` when a third party's
  allegation links the two ends without saying how). A document that explicitly references, quotes
  or relies on another document -> `cites`.
- **Research vs inquiry.** Scientific or technical research on a phenomenon, material or field ->
  `studied`. An inquiry into a case, an event, records or conduct (including a field investigation
  of a sighting, an audit, a records search) -> `investigated`. A comparative assessment of another
  body's model -> `cites`.
- **Passing an account.** One person telling, showing or briefing another something -> `told`.
  Meetings, calls or correspondence where no account is said to pass -> `in_contact_with`. A
  recorded interview conducted by the subject -> `interviewed`.
- **Rules vs requirements.** A text requiring the object to do or produce something specific ->
  `mandated`. A text setting rules, defining, restricting, exempting or conditioning -> `governs`.
- **Answering a claim.** Says it did not happen or does not exist, or retracts -> `denied`. Argues
  it is wrong -> `disputed`. Offers a prosaic explanation -> `explained_away`. Declines, withholds,
  blocks -> `refused`. Does not mention it -> `omitted`. Confirms it (even while dismissing it) ->
  `acknowledged`. Two records that cannot both stand, with no adjudicated denier -> `contradicts`.
- **The board's own reading.** The sentence places the subject as a case of a mechanism, pattern or
  domain (most edges to a domain node) -> `exemplifies`. The sentence compares two like things ->
  `parallels`. The sentence infers a consequence -> `affects`. Same time or same place with no order
  -> `concurrent_with`. Only when none of these fits -> `connected_to`.
- **Direction for succession and sequence.** `succeeded`: the LATER body is the subject.
  `preceded`: the EARLIER one is the subject. `led_to`: the cause is the subject.

## Output

Write ONE JSON file, a list with one object per input packet, in the same order:

```
[{"id": "e-0123456789", "predicate": "wrote", "subject": "b", "confidence": "high",
  "reason": "sentence: authored by; b is the author"}, ...]
```

`reason` is under 15 words. Then validate it (it checks ids, predicates, classes, the denial rule):

```
python "C:/Users/stewa/ClaudeProjects/tp-p7/tools/predicates/validate_batch.py" <your packets file> <your output file>
```

Fix every problem it prints and re-run until it prints OK. Work in the directory
`C:/Users/stewa/ClaudeProjects/tp-p7`, write nothing else, change no other file, run no git
command. Reply with the validator's last line, your counts of high/medium/low, and your
`connected_to` count, in under 10 lines.

## The vocabulary

| predicate | family | forward (read from subject) | inverse (read from object) | subject classes | object classes | refines type | use when |
|---|---|---|---|---|---|---|---|
| `held_post` | Roles | held a post at | had in a post | person | institution, program, location, document, event | institutional | employment, office, rank, command, a named role (director, principal investigator, co-host, officer), at any date |
| `led` | Roles | led | was led by | person, institution | institution, program, event, location, document | institutional | headed, directed, chaired, commanded, managed as the one in charge |
| `appointed` | Roles | appointed | was appointed by | person, institution, legislation, document | person | institutional | named, appointed, nominated or confirmed someone to a post |
| `member_of` | Roles | was a member of | had as a member | person, institution, program | institution, program, event | institutional | a seat, a membership, a place on a board, panel, caucus, task force or committee |
| `founded` | Roles | founded | was founded by | person, institution, program | institution, program, document | institutional | founded, co-founded, stood up, formed (not by statute: that is created) |
| `worked_with` | Roles | worked with | worked with | person, institution, program | person, institution, program | institutional | collaborators, partners, co-investigators, joint venturers, neither under the other (symmetric) |
| `part_of` | Organisation | is part of | includes | institution, program, location, document, legislation, event | institution, program, location, document, legislation, event | institutional | a unit of a parent body, a section of a statute, a volume or item of a series, a site within a larger site, a body placed under another, a company acquired by another |
| `outside_of` | Organisation | falls outside | does not include | any | any | legislative | a stated exclusion: the subject is not a member of, not covered by, or outside the reach of the object (a person outside a group, a body outside a statute's reach) |
| `succeeded` | Organisation | succeeded | was succeeded by | institution, program, document, legislation, event | institution, program, document, legislation, event | programmatic | the later body, programme or instrument that replaced, renamed, reissued or continued the earlier; the subject is the LATER one |
| `ran` | Organisation | ran | was run by | person, institution, program | institution, program, event, location | programmatic | operated, administered, managed or hosted a programme, facility, series or effort |
| `produced` | Organisation | produced | was produced by | person, institution, program, event, document | document, event, program | programmatic | a programme's deliverables, a report a process produced, a tranche of a release programme, an outcome made by the subject |
| `same_as` | Organisation | is the same as | is the same as | any | any | institutional | two names or records for one thing (symmetric) |
| `funded` | Money | funded | was funded by | person, institution, program, legislation, document | person, institution, program, event, document, location | funding | paid for, appropriated, sponsored with money, granted |
| `contracted` | Money | contracted | was contracted by | person, institution, program, document | person, institution, program, document | funding | awarded or let a contract, solicitation or agreement to; the subject is the buyer |
| `holds` | Custody | holds | is held by | person, institution, program, location, document | document, event, program, location, institution, person | custody | documented custody of records, files, recordings or collections |
| `alleged_to_hold` | Custody | is alleged to hold material from | is alleged to have material held by | person, institution, program, location, document, event | program, event, document, location, institution | custody | an allegation that the subject holds or held recovered or exotic material; the subject is the alleged holder |
| `transferred` | Custody | passed records or material to | received records or material from | person, institution, program, event, location, document | person, institution, location, program, document | custody | handed on, moved, shipped, transferred holdings; the subject is the giver |
| `analysed_material` | Custody | analysed material from | had material analysed by | person, institution, program, document | event, program, document, location, institution | investigative | laboratory or technical analysis of physical specimens or sensor data |
| `created` | Law | created | was created by | legislation, document, person, institution | institution, program, legislation, document | legislative | established by statute, order, directive or decision; enacted |
| `governs` | Law | governs | is governed by | legislation, document, institution, program | any | legislative | regulates, defines, codifies, restricts, exempts, conditions funding on, sets rules for |
| `amended` | Law | amended | was amended by | legislation, document | legislation, document | legislative | a later text changing an earlier one (a text that replaces another outright is succeeded) |
| `implements` | Law | implements | is implemented by | legislation, document, institution, program, person | legislation, document, program | legislative | a regulation, manual, instruction or office putting a higher instrument into effect |
| `mandated` | Law | requires | is required by | legislation, document, institution | any | legislative | a statute or order requiring a report, review, briefing or action |
| `sponsored_law` | Law | sponsored | was sponsored by | person, institution | legislation, document | legislative | sponsored, cosponsored or introduced a bill or amendment |
| `oversaw` | Oversight | oversaw | was overseen by | person, institution, program | institution, program, event, location, document | legislative | oversight authority over a body or programme; presided over, convened or forced a hearing |
| `investigated` | Oversight | investigated | was investigated by | person, institution, program, document, event | any | investigative | examined, reviewed, audited, probed, searched records on |
| `questioned` | Oversight | questioned | was questioned by | person, institution | person, institution | investigative | asked questions of a witness or official, typically at a hearing |
| `reports_to` | Oversight | reports to | receives reports from | person, institution, program, document, event | person, institution, program | legislative | must notify, report to or brief; briefed; a report submitted to |
| `requested` | Oversight | made a request of | received a request from | person, institution, document | person, institution, program, document | investigative | a letter, demand, FOIA request, referral or tasking addressed to the object |
| `testified_at` | Testimony | testified at | heard testimony from | person, institution | event, institution, document | witness-chain | a witness appearance, sworn or not, at a hearing or before a body |
| `witnessed` | Testimony | gave a first-hand account of | has a first-hand account from | person, institution | event, program, location, document | witness-chain | the subject says, or a record shows, they were present at, saw, handled or worked on the object |
| `made_claims_about` | Testimony | made claims about | is the subject of claims by | person, institution, program, document, event | any | witness-chain | asserted, alleged or named something about the object without first-hand presence |
| `corroborated` | Testimony | corroborates | is corroborated by | person, institution, document, event | any | witness-chain | supports another account or claim independently |
| `contradicts` | Testimony | contradicts | is contradicted by | any | any | witness-chain | an account, record or finding that conflicts with another; not a denial by an interested party |
| `brought_to_record` | Testimony | brought to the record | was brought to the record by | person, institution, document, event, program | any | witness-chain | entered, named, leaked, circulated or first made public an account, document or person |
| `told` | Testimony | passed an account to | received an account from | person, institution | person, institution | witness-chain | one person telling, showing or briefing another privately; a named source of someone else's account |
| `acknowledged` | Testimony | acknowledged | was acknowledged by | person, institution, document, program | any | witness-chain | an official or attributable statement confirming that the object exists, happened or is so (the counterpart of denied) |
| `alleged_tie` | Testimony | is alleged to be tied to | is alleged to be tied to | any | any | witness-chain | an alleged connection between the two that the sentence does not specify further, asserted by someone other than either end (symmetric) |
| `denied` | Denials | denied | was denied by | person, institution, document, program, event | any | denial | a dated, attributable statement that the object is not so, did not happen or does not exist; a retraction |
| `refused` | Denials | refused | was refused by | person, institution, program, document, event | any | denial | declined, withheld, blocked or did not act on a request, a case or access |
| `disputed` | Denials | disputes | is disputed by | person, institution, program, document, event | any | denial | argues against, rejects or finds wrong the object's claim or work |
| `explained_away` | Denials | gave a conventional explanation for | was given a conventional explanation by | person, institution, program, document, event | any | denial | an official or skeptical explanation in prosaic terms (a balloon, a misidentification, a test) |
| `omitted` | Denials | leaves out | is left out of | document, institution, person, program, event | any | denial | a report, review or response that does not mention or address the object |
| `wrote` | Documents | wrote | was written by | person, institution | document, legislation, program | research | authored, signed, drafted, formulated, named inventor of |
| `published` | Documents | published | was published by | person, institution, program | document, event | research | issued or broadcast as its own publication |
| `released` | Documents | released | was released by | person, institution, program, event | document, event, program, institution, location | custody | declassified, released under FOIA or a release programme, made public from holdings |
| `concerns` | Documents | concerns | is the subject of | document, legislation, event | any | research | a document, record or event that is about, names or records the object, with no stronger relation stated |
| `cites` | Documents | cites | is cited by | document, person, institution, legislation, program | any | research | refers to, quotes, relies on or incorporates by reference |
| `studied` | Documents | studied | was studied by | person, institution, program, document | any | research | scientific or scholarly research on the object; a technical interest in it |
| `reported_on` | Media | reported on | was reported on by | person, institution, program, document | any | investigative | journalism, broadcast coverage, an article or episode about the object |
| `appeared_on` | Media | appeared on | featured | person, institution | program, institution, event, document | witness-chain | a guest or interviewee appearance on a programme, broadcast or channel |
| `interviewed` | Media | interviewed | was interviewed by | person, institution, program | person | witness-chain | conducted an interview with the object |
| `located_at` | Place and time | is located at | is the location of | person, institution, program, location, document | location, institution | geographic | sited at, based at, headquartered at, lies within, was stationed at (a post held there is held_post) |
| `occurred_at` | Place and time | happened at | was the scene of | event, program | location, institution | geographic | where an event or incident took place |
| `preceded` | Place and time | came before | came after | any | any | temporal | a sequence in time with no causal link stated; the subject is the EARLIER one |
| `concurrent_with` | Place and time | happened alongside | happened alongside | any | any | temporal | at the same time or in the same place, with no order or cause stated (co-occurrence, adjacency) (symmetric) |
| `led_to` | Place and time | led to | followed from | any | any | temporal | prompted, caused, triggered or resulted in |
| `responded_to` | Place and time | responded to | drew a response from | any | any | temporal | answered, acted on, rebutted in time (a rebuttal by an interested party is a denial predicate) |
| `supported` | Conduct | supported | was supported by | person, institution, program, document | any | behavioral | backed, endorsed, advocated for or lobbied for something other than a bill it sponsored |
| `acted_against` | Conduct | took action against | was the target of action by | person, institution, program, document | person, institution, program | behavioral | reprisal, removal, surveillance, disinformation or pressure directed at the object |
| `in_contact_with` | Conduct | was in contact with | was in contact with | person, institution, program | person, institution, program | behavioral | documented meetings, correspondence or dealings between parties (symmetric) |
| `exemplifies` | The board's reading | is an instance of | has as an instance | any | any | institutional | the board places the subject as a case of a mechanism, pattern or domain (most edges to domain nodes) |
| `parallels` | The board's reading | parallels | parallels | any | any | research | the board compares two things: a like case, a pattern repeated, or opposite answers to one problem (symmetric) |
| `affects` | The board's reading | affects | is affected by | any | any | temporal | the board's inference that the subject has consequences for, constrains or bears on the object |
| `connected_to` | Other links | is connected to | is connected to | any | any | (none) | ONLY when no predicate above fits the sentence (symmetric) |
