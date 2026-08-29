# The image register hits its ceiling at 13, and the remaining 26 are the finding

**28 August 2026.** Third pass. Follows `notes/IMAGE-SOURCING-2026-08-26.md` (0 to 9) and
`notes/IMAGE-SOURCING-2026-08-27.md` (9 to 12).

One record added, and the more useful result is the negative one: **the remaining 26
institutions on the L0 map are not a backlog. They are a wall, and there are three distinct
reasons for it.** A future session should not re-run this search expecting a different answer
without first reading the three categories below.

---

## The one added

| node | mark | why it clears |
|---|---|---|
| `nara-rg615` | NARA seal | Record Group 615 is a National Archives record group. The custodian's seal is the honest mark, exactly as it already is for `nara-uap-collection`. US federal work, 17 U.S.C. 105. |

Both NARA nodes now point at the same asset, and the file was renamed from
`assets/marks/nara-uap-collection.png` to `assets/marks/nara.png` so the sharing is visible
rather than looking like a mistake. The record carries a `note` saying the reuse is deliberate
and why. **No new pixel verification was needed**: this is the identical file the 26 August
pass contain-fitted at 11px and looked at.

## The three reasons the other 26 do not ship

**1. No mark exists.** Searched this session and confirmed absent from Wikimedia Commons:

| node | what the query actually returned |
|---|---|
| `ousdi` | Seven PDFs of intelligence-law syllabi, and a 4000x2652 CIA photograph of a Situation Room meeting |
| `isoo` | Three 4256x2848 photographs of the ISOO 2005 Annual Conference |
| `house-oversight-committee` | `HOUSE OVERSIGHT 037548 Redacted - Copy.jpg`, a scan of a redacted document |
| `senate-armed-services` | Confirmed absent on 27 August; six hearing photographs including named living people |

**The hazard the previous two passes documented has not improved.** Every one of these queries
returned photographs ranked as confidently as a seal would be, and the ISOO and SASC results
contain identifiable faces. A pass that accepted results on their titles would have put a
photograph of a named private individual on this board under an institution's name.

**2. The mark exists but is a wordmark.** `mitre-corporation` (aspect 3.51) and
`lockheed-martin` were both rejected on 27 August for this and the reason is geometric, not
legal: the slot is an 11px square and a mark is contain-fitted, never cropped, so a wide
wordmark renders as a two-pixel sliver. Re-testing these is pointless until the chip geometry
changes.

**3. The organisation is private, foreign, or not an organisation at all.**

| category | nodes |
|---|---|
| private bodies with copyrighted logos | `sol-foundation`, `ttsa`, `earthtech-international`, `baass`, `americans-for-safe-aerospace`, `cometa`, `battelle`, `wayne-state-university`, `university-at-albany` |
| foreign agencies, licence not US federal | `geipan`, `fab`, `cefaa`, `senado-brasil`, `arquivo-nacional-ufo` |
| abstractions with no mark to find | `waived-sap-notification-group`, `oversight-congress`, `congressional-uap-caucus`, `uap-science-advisory-council`, `dod-sapco` |

The third row is the one worth pausing on. `waived-sap-notification-group` is the
highest-degree node without an image on the whole map, and it has no seal because **it is not a
body that has one** — it is the set of members of Congress entitled to waived-SAP notification.
Looking for its logo is a category error, and the class letter is the correct rendering.

## What would actually move this

Not another Commons sweep. The realistic routes, in order of expected yield:

1. **Agency websites directly.** AFOSI and AARO both cleared on 27 August via credits tracing to
   `af.mil` and `science.nasa.gov` originals. `ousdi` and `isoo` may have seals on their own
   `.gov` pages that were never uploaded to Commons.
2. **Foreign public-domain rules, read individually.** Brazil and France have their own rules for
   government works and at least `fab`, `geipan` and `senado-brasil` are plausible. This is
   licence research, not image search, and it should not be guessed at.
3. **Accepting that 26 nodes draw a class letter**, which is what the fallback is for and what it
   already does correctly.

**Do not treat the count as a target.** 13 of 39 with every record traceable to an opened URL
and a read licence basis is worth more to this board than 39 of 39 with a dozen guesses in it.
