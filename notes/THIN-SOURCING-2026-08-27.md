# The nine people resting on a single non-primary source

**27 August 2026.** `merge.py` reports `person_single_nonprimary_source`, split out from the
raw thin-sourcing count on purpose: a node resting on one primary record and a node resting
on one blog post are not the same risk, and counting them together made the queue useless.

Nine at the start of this pass. **Seven now.** The two that cleared did so on sources that
were opened and read, not on sources that looked plausible.

---

## Cleared

**`ben-rich`** — rested on the Internet Archive copy of his own memoir. Two institutional
records added, each checked against the claim it is being asked to carry:

| source | what it actually says |
|---|---|
| National Aviation Hall of Fame enshrinee record | *"Selected by Kelly Johnson (enshrined 1974) to be the new 'Chief Skunk' in 1975."* |
| Lockheed Martin corporate history, *Ben Rich: The Invisible Man* | Johnson *"planned to personally recommend Rich to take over as director of the Skunk Works"*; dates the retirement banquet to 1991 |

**A near-miss worth recording.** The Lockheed Martin page was the obvious citation for the
T1 claim *"directed Lockheed's Advanced Development Projects from 1975 to 1991"* and it
does **not** state the 1975 start date. It confirms the succession and the 1991 retirement
and stops there. Citing it alone for the date range would have been a source that does not
support its claim. The Hall of Fame record carries the 1975 date; the two together carry
the claim, and neither carries it alone.

The National Academy of Engineering memorial tribute (Memorial Tributes Vol. 8, 1996,
pp. 200-205) is the strongest candidate that was **not** used: the NAP copy is scanned
page images, so no quote can be substring-verified out of it and `spot_check.py` could not
adjudicate it. Left out rather than cited unread.

**`alejandro-rojas`** — rested on a DefenseScoop article quoting his assessment of PURSUE
Release 01. Added the release itself at `war.gov/UFO`, opened and confirmed to carry
*"The first tranche was released on May 8, 2026."* The claim is about what the release
contains, so the release is the right primary for it.

Note the golden manifest moved **1221 -> 1223** and not 1224 for three added source
entries: `war.gov/UFO` was already cited by twenty-five other nodes, so Rojas's entry adds
a citation and no new unique URL. Checked rather than assumed, per the standing caution.

---

## Still thin, and why

Five of the seven are thin for reasons no amount of searching will fix, and the board
already says so in its own narratives. Recording them here stops the next session
re-deriving it.

| id | why it stays thin |
|---|---|
| `jason-turner` | The narrative already states it: *"No FOIA release, deck-log entry, or Navy statement has yet confirmed any part of it."* The Navy's range-fouler FOIA releases document the 14 Nov 2004 **incident**, not the confiscation Turner describes. Citing them on this node would imply a corroboration that does not exist. **Deliberately not added.** |
| `jonathan-grey` | A pseudonym. The Debrief article is where the statement was made, so it is the primary by construction. A second source can only be someone quoting the first. |
| `tim-mcmillan` | The claim is that he co-founded The Debrief and the source is The Debrief's own masthead. That is the right source for that claim; it just does not match the primary-URL pattern. |
| `yury-platov` | The only cited copy is a `web.archive.org` capture, and **Wayback is unreachable from this environment entirely** (`notes/SOURCING-2026-08-25.md`). Cannot be re-verified from here at all, let alone thickened. Needs a session with Wayback access or a different host for the Stonehill/Mantle SETKA article. |
| `grant-cameron` | Rests on his own site. His underlying material is presidential-library FOIA correspondence, which would be the real primary — `presidentiallibraries.us` and `archives.gov` are both in the pattern. **This one is genuinely workable and is the best next target.** |

`thomas-crosson` and `italo-venturelli` are also workable and were not reached in this pass:

- **`thomas-crosson`** — currently a NICAP PDF scan of the 16 December 2017 New York Times
  story. The NYT original is the better citation; it is paywalled, which is why the scan
  was used. Worth one attempt at the canonical URL.
- **`italo-venturelli`** — his account was given to three members of Congress on
  15 January 2026. If that event produced any congressional record, `.house.gov` is in the
  pattern and would be a real primary.

---

## The thing not to do

The raw `person_thin_sourcing` count is 16 and chasing it means padding strong nodes with
whatever second link is nearest. That is why the two metrics are separate. Seven of nine
is the honest number for this pass, and five of the seven are thin because the record is
thin, which is a finding rather than a defect.

Gate green after the pass: verify 46 + self-test, capture_strip, audit 40, runtime 28,
canvas 29 + every poison, analyst 15, `--idempotent`.
