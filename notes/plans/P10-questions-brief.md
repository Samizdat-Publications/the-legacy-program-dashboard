# Phase 10: brief for the question drafter and the question verifier

Written 26 September 2026 for redesign phase 10, task 3 (`notes/plans/P10-claimants-questions-connect.md`).
The drafter is one Opus agent; the verifier is a second, separate Opus agent working from the cites alone.

## The rule that never bends

No invented sources, URLs, document numbers or quotes, anywhere. A question cites only claim ids (`c-...`)
and edge ids (`e-...`) that are already on the board. Every sentence rests on what it cites and says no
more than its cites say. Testimony is testimony: "Grusch testified that...", never "the programme exists".
AARO and the Department of Defense are interested parties: what they say is "AARO says" or "the office
concluded", never the finding of fact. Two sources that share a method (one interviewer, one packet, one
podcast) are not two independent sources, and where a question leans on such a cluster it says so.

## What a question is

`research/questions/<id>.json`, one file per question, the file name the id:

```json
{
  "id": "recovered-craft",
  "order": 1,
  "title": "Has the US recovered non-human craft?",
  "status": "drafted",
  "lead": {"text": "One or two sentences: the answer so far, as the record stands.", "cite": ["c-..."]},
  "answer": [{"text": "Three to six sentences, each an item, saying what the board can and cannot show.", "cite": ["c-...", "e-..."]}],
  "for": [{"text": "The evidence for, strongest first, each graded honestly in words.", "cite": ["..."]}],
  "against": [{"text": "The evidence against, and the denials, strongest first.", "cite": ["..."]}],
  "open": ["An open question in words, ending with a question mark?"],
  "threads": [{"id": "custody", "text": "How this authored chain of evidence bears on the question.", "cite": ["..."]}],
  "topics": ["roswell-1947", "grusch-allegations"]
}
```

- `lead`, every `answer`, `for`, `against` and `threads` item is `{text, cite}` with at least one id. A double-quoted
  run of four characters or more must appear letter for letter in a claim or edge the same item cites.
  No URL and no em dash (U+2014) anywhere; use a comma, colon or spaced hyphen.
- `for` and `against` each hold 3 to 8 items. The case against is never empty, and never weaker in wording
  than the case for.
- `open`: 2 to 6 open questions in words. Prefer the board's own (the topic files' `questions`, a node's open
  questions) and do not invent new facts inside them.
- `threads`: the board's eight authored threads are `lineage`, `custody`, `money`, `denials`, `wilson-davis`,
  `patents`, `scientists`, `oversight` (`app/public/data/threads.json`). EVERY thread must be folded into at
  least one question, as the chain of evidence it is for that question.
- `topics`: 2 to 8 topic ids the question draws on (`research/topics/*.json`), most relevant first.
- `order` is the reading order on `#/questions`, 1 upward, unique.

## The questions

From the redesign's section 5. Draft 10 of these 11, or all 11 if the board carries material for each; the
floor is 8. If you drop one, say why in your report.

1. Has the US recovered non-human craft?
2. How could a programme be hidden from Congress?
3. Who has testified under oath, and what corroborates them?
4. Where would the money come from?
5. What does the government deny, and how?
6. What physical evidence is claimed?
7. Which famous documents are genuine?
8. What happened at nuclear sites?
9. What do other governments say?
10. Where does the popular story go beyond the record?
11. What would settle it?

## Where the material is (read, never edit, anything but `research/questions/`)

- `app/public/data/topics.json` (every topic, section and lead) and `app/public/data/topics/<id>.json`: each
  verified topic's lead, summary, record, claimed and contested items, with `cites` RESOLVED to the claim or
  edge text, tier and source. This is the richest verified material on the board: re-use its cites.
- `app/public/data/threads.json`: the eight threads and their steps.
- `app/public/data/nodes/<id>.json`: a node's `claims` (with `id`, `tier`, `text`, `source`), `connections`
  (with `edgeId`, `edgeLabel`, `note`, `claimTier`, `sources`), `conflicts`, `unverified`, `denials`.
- `app/public/data/claims.json` (4 MB, every claim; search it with Grep, do not read it whole).
- `python tools/topics/topic_packet.py <topic id>` prints a topic's full packet of claims.

## Checking your work

`python tools/claims/q_lint.py` runs the board's question checks in two seconds (ignore the two lines about
FOIA and authored notes). `the app ships every question` needs `python tools/build_app_data.py` first; run it
once at the end. Every check about questions must pass before you report.

## The verifier (a separate pass)

For every item of every question: open each cited claim or edge (in the resolved `cites` of
`app/public/data/questions/<id>.json` after `python tools/build_app_data.py`) and confirm the sentence says no
more than its cites; that testimony reads as testimony and an interested party's word as that party's; that
quotations are verbatim; that the case against is fair and as strong as the record makes it. Fix what fails
in place (rewording, re-citing, or removing), then set `status` to `verified`. Report every change in a table
(question, item, the problem, the fix).
