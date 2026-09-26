# Phase 9 blind critic: what was fixed and what was recorded

Three rounds (`p9-round-1.md` to `p9-round-3.md`), routes: the ten standard surfaces plus `#/people`,
`#/events` and `#/orgs`, at 1920, 1366 and 375.

## Fixed (in scope: directories, search, the timeline, person facets)

| round | finding | fix |
|---|---|---|
| 1 | four 2026 events of a lane shown as a bare "+4" | a chip that would run past the column ends at its date instead (colour bar on the right); eight chip rows a lane |
| 1 | directory dates read as spans ("1946-01-22 · THROUGH 1969") | ranges read "A to B"; the era left the cell (it is a filter) |
| 1 | a garbled separator on every phone people card | a NUL byte in the CSS, replaced |
| 1 | claim counts with no key on the phone | the card label reads "claims T1 · T2 · T3" |
| 2 | chips that end at their date not explained; the axis jumps 2026 to 2029 unmarked | the header says how a chip sits on its date; the jump is marked on the axis and the gridlines |
| 2 | Events directory (93) against the timeline (1,076) unexplained | every directory says what it holds; Events points to the timeline's dated entries |
| 2 | a person's date means different things on different rows | the People directory says so under its title |
| 3 | "+N" counts do not say which year | a count reads "2024 +15" where its year has room |
| 3 | "not stated" in the Under Oath column against "unknown" in its filter | one word, "unknown" |
| 3 | the phone header explained chips it does not draw | a phone header of its own |
| 3 | lane names with dates hold later events; chip colours unexplained | the header says an event sits in its node's primary topic's section, and what the colour is |

## Recorded, not fixed here

| finding | where it belongs |
|---|---|
| the open era still counts about half its events at 1366 and 1920 (a +N opens their named list) | a later timeline pass: a denser era may want years opened by default, or a list view |
| the program map at 1366 draws no links and ends cells in "+N" | phase 11 (the map's future) |
| neighbourhood ring labels that give only a family ("conduct link", "two steps") | phase 11 |
| the evidence explorer's FOIA and "node denied" columns have no key; a domain chip breaks mid-word at 1366 | a later evidence pass |
| no directory for documents (231 nodes) | not in the phase 9 spec; add with phase 8's source library, which is the documents' natural home |
| odd primary topics (ONI under "FFRDCs and the 2026 contractor probes") | topic membership, phase R |
| 123 people with vital status unknown | the rule working: the record does not state it (see `notes/plans/P9-facets-record.md`) |

The worst in-scope issue after round 3 is the share of the open era behind counts: major by the critic's
grading, but every counted event is named one click away, and nothing on the timeline is drawn unnamed.
