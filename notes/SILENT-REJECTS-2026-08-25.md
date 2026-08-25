# Nothing was reading REJECTS.json, and it had been dropping the board's best statutory research

**25 August 2026.** Found by accident, while auditing something else.

## What happened

`merge.py` writes every record it cannot place to `tools/REJECTS.json` with a reason.
The file has existed and worked correctly the whole time. **Nothing read it.** The build
exits 0, the gate passes, and the record is simply not on the board.

I found it because I made the same mistake myself: I added eight entity records without a
`cls` field, rebuilt, watched the gate pass, and then discovered none of them had landed.
Checking `REJECTS.json` showed my eight — and **eight more that had been there all along.**

## What it cost

`research/w11-statutory.json` carried four entity records whose `cls` values were
`"provision"`, `"statute"` and `"mechanism"`. None of those are in `VALID_CLS`. All four
were rejected on every build since the file was written.

| node | intended `cls` | claims carried | claims on the board by any route |
|---|---|---|---|
| `usc-10-119` | `statute` | 5 | 1 |
| `waived-usap-mechanism` | `mechanism` | 10 | **0** |
| `waived-sap-notification-group` | `mechanism` | 7 | **0** |
| `iaa-fy2024-sec-1102` | `provision` | 8 | 3 |

**30 claims dropped, 26 of which reached the board by no other route.** Among them:

- the verbatim text of the **10 U.S.C. 119(e)(1) waiver authority**, the provision the
  entire concealment argument turns on;
- the recipient set fixed by subsection (g), verbatim;
- **"the waiver has been exercised, and the Department of Defense says so in a currently
  effective instruction"** — a verdict on the board's own standing question;
- the DoDI 5205.11 paragraphs cutting **professional staff out of waived programs
  entirely**, gating even GAO's access through the same two seats;
- the finding that the statutory notification group and the Department's are **not the
  same, and the Department's is wider**.

Two of those four nodes — `usc-10-119` and `waived-sap-notification-group` — are
**start-here flags**, numbers 2 and 3 in the fourteen the reader is told to open first.
The board pointed a stranger at them and then showed them the thin version.

A fifth record, `nara-uap-collection` in `grusch.json`, used `cls: "entity"` and was
dropped the same way.

After the fix: **claim tiers 2,715 → 2,744 at Tier 1**, and the four nodes go from
8/13/18/22 claims to 18/21/23/29.

## The three that were correctly rejected

`w2-2025-2026.json` and `w2-international.json` wrote `keyFindings`, `coreDocuments` and
`archives` under `entityInfo`, which `merge.py` reads as `{entityId: {desc, sources}}`. A
list keyed by a section name is not an entity record, so the rejection was right. These are
research notes, not node content, and they are moved to underscore-prefixed keys — merge
ignores those, the notes stay in the file, and the list goes clean.

## The fix that matters

```
@check("no research record is silently dropped")
```

Asserts `tools/REJECTS.json` is empty. Demonstrated rejecting a poisoned list, like every
other check.

**Deliberately NOT an accepted-rejects list.** The obvious next move is to add one, the way
`DUPLICATES_ACCEPTED.json` works for duplicate nodes. Do not. A duplicate is a judgement
call about two real records; a reject is a record that failed to parse into the schema, and
there is no legitimate reason for one to persist. An accepted-rejects list is a place for
the next silent drop to hide, and it would have hidden this one — four entries added years
apart, each individually explicable, none of them ever looked at again. If a record cannot
be placed, fix the record or move it out of the merged keys.

## The general shape

This is the same failure the analyst had, the same failure `explainEdge` had, and the same
failure the QA checklist had:

> **A pipeline that reports success while discarding input is indistinguishable from one
> that worked.**

`REJECTS.json` was not a missing feature. It was a working diagnostic with no consumer,
which is the same thing as no diagnostic. The lesson is not "write the file" — someone did
— it is that **a diagnostic nothing asserts on is decoration.**

## Worth checking next

The four rejected records were found because I tripped the same wire. Nobody knows what
else in `research/` is shaped wrongly in a way that parses but does not merge — a claim
with no `text`, a source with neither `name` nor `url`, an edge naming an id that does not
exist. `norm_claims` and `norm_source` both drop malformed entries and neither reports it.
Those are silent in a way `REJECTS.json` is not.
