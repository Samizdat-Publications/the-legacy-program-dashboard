# Image sourcing, second pass: 9 to 12

**27 August 2026.** Follows `notes/IMAGE-SOURCING-2026-08-26.md`, which took the register
from 0 to 9 and explained why the other 30 institutions did not ship.

**The unattended rule was lifted this session** by Stewart: *"licensing is for me to deal
with on my end. You're just collecting the pictures for our project."* `CLAUDE.md` §9 item 7
records the lift and restates what does not change: an image URL is still a sourcing claim,
so every record names a URL that was opened and a licence basis that was read.

The first pass's finding still governs everything here: **there are no PERSON nodes on the
L0 map.** All 110 are documents, institutions, programmes, legislation and events, so this
is a seals-and-marks problem and never a faces problem.

---

## Three added

| node | mark | why it clears |
|---|---|---|
| `aaro` | AARO seal | US federal work, 17 U.S.C. 105. Commons flags `insignia`, the same generic notice already carried by the DoD, CIA and DIA seals here. No statute names AARO. Credit traces to a `science.nasa.gov` original. |
| `afosi` | AFOSI shield | US federal work. 18 U.S.C. 701 reaches the manufacture and sale of *physical* insignia, not depiction in research. Credit traces to an `af.mil` original. |
| `nro` | NRO seal | US federal work. **10 U.S.C. § 425 names NRO explicitly**, alongside DIA and NGA, and reaches only merchandise, impersonation, solicitation or commercial activity conveying endorsement. That is the identical statute and identical scope already read for the DIA seal, which ships as `clears`. |

**AARO had been dropped on 26 August for an opaque white background** — "verified at the
pixel: would draw a white box". That was a different file. This one samples `[0,0,0,0]` at
the corner: genuinely transparent. Re-testing a rejection rather than inheriting it is what
found it, and it is the same lesson as the hosts recorded as blocked on 25 August that came
back when re-tested.

All three were checked the way the first pass checked its nine: corner alpha sampled on the
original, then contain-fitted into an **11px** box on the real chip fill `#12171d` and looked
at, upscaled.

| | ink at 11px | mean luminance |
|---|---|---|
| AARO | 74% | 74 |
| AFOSI | 87% | 134 |
| NRO | 90% | 132 |

AARO is the darkest of the three and reads as a light ring around a dark centre, which is
what its seal *is*. It clears `battelle`'s failure mode (black on transparent, invisible on a
dark board) because of its white outer ring.

---

## Three rejected, and the search is still dangerous

| node | what came back |
|---|---|
| `mitre-corporation` | `Mitre Corporation logo.svg`, 512x146, **aspect 3.51**. Lockheed's exact failure: the slot is an 11px square and a mark is contain-fitted, never cropped, so a wordmark becomes a 2px sliver. |
| `senate-armed-services` | **No committee seal exists on Commons.** The query returned six photographs of Senate hearings, including named living people — Adm. Kilby, Sen. Gillibrand, Sean Kirkpatrick. |
| `ttsa` | "Little Stars Academy", "Stars Academy" — **wrong entities entirely**, and CC BY-SA. |

And the AARO query itself returned `Jon T. Kosloski.jpg` — a photograph of AARO's serving
director. **An institution query returning a named individual's face, ranked alongside the
correct seal and looking exactly as authoritative.** The first pass documented this and it
has not improved; it is why every candidate here was opened and looked at rather than
accepted on its title.

---

## One stale string, in the tool that exists to prevent stale strings

`state_snapshot.py` reported the register as *"empty on purpose -- an image URL is a
sourcing claim"*. That was hardcoded, and it stayed true through zero records, then false
through nine, then false through twelve — in the one tool whose stated purpose is that
"a number that cannot drift out of sync with the thing it describes cannot mislead the next
session". It now derives the line, and prints the clears/ask split.

---

## Where it stands

**12 of 39 institutions**, 11 `clears` and 1 `ask` (RAND). The remaining 27 are mostly not a
search problem:

- several would wear a **parent body's mark**, which asserts an identity the record does not
  support (`dod-sapco` is not DoD; the `waived-sap-notification-group` certainly is not);
- several are **abstractions with no mark at all** — `oversight-congress` is a concept;
- the foreign bodies (`fab`, `geipan`, `cefaa`, `senado-brasil`, `arquivo-nacional-ufo`) are
  not covered by 17 U.S.C. 105 and each needs its own jurisdiction's rule read before
  anything ships;
- the private ones (`ttsa`, `sol-foundation`, `earthtech-international`, `eg-and-g`,
  `baass`) are trademarks where a free-licensed own-mark generally does not exist.

Gate: verify 46 + self-test, capture_strip, audit 40, runtime 28, canvas 30 + every poison,
analyst 15, `--idempotent`. All green.
