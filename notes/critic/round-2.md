# Blind critic, round 2 (25 September 2026)

Redesign phase 5b, after the round-1 fixes (commit 57782647). 30 screenshots from
`node tools/look.js --critic --out dist/critic/round-2`; a separate Opus agent read `tools/critic/BRIEF.md`
and the PNGs and nothing else. Its report, verbatim:

---

Blind critic, round 2. I read BRIEF.md and all 30 PNGs in dist\critic\round-2, and opened nothing else.

**1. Sworn testimony carries the Tier 1 badge, so the tier counts overstate the documentation**
- **Screenshots:** 1920-node.png, 1920-person.png, 1366-node.png, 1920-report.png, 1366-report.png, 1920-evidence.png, 1366-evidence.png, 375-evidence.png
- **What is wrong:** The brief and the home page define testimony as Tier 2. Yet Grusch's sworn answers ("biologics came with some of these recoveries", "Nonhuman") are badged **T1**, with only an amber "said on the record" chip to qualify them. That is how the node reaches "16 at Tier 1". AARO statements are also T1, flagged "the office's own account", although the home page says AARO is capped at Tier 2. In the printable report the chip is pale amber on cream and barely legible, and no legend explains it. On paper it reads "T1 Sworn: 'biologics came with...'". The evidence explorer also counts internal notes as claims: a T3 row with the source "Board bookkeeping" says "no dossier written yet ... see the wave-3 queue", which pads the T3 count and leaks internal jargon.
- **Why a reader cares:** The tier is the board's central promise. An informed reader who knows testimony is Tier 2 will stop trusting the "T1 3,780" headline and every T1 badge. The report is the page most likely to be forwarded, and it hides the qualifier.
- **Severity:** blocker

**2. Connection group headings claim relationships the links do not support**
- **Screenshots:** 1920-node.png, 1920-person.png, 375-hood.png
- **What is wrong:**
  - The group MONEY is defined as "who paid, contracted or was paid". It holds Alexandria Ocasio-Cortez and Jared Moskowitz, whose lines describe questions asked at a hearing, and The Boeing Company ("personnel named in the same hearing").
  - CUSTODY is defined as "who is said to hold material". It holds Wright-Patterson with a line about where a NASIC officer sits.
- **Why a reader cares:** The heading is the first "why" the reader sees for each link, and here it contradicts the line under it. It reads as the board asserting that members of Congress are in Grusch's money chain, which breaks the rule that every connection says in words why it exists.
- **Severity:** major

**3. At 1366 the program map shows no links and nameless "+N" chips**
- **Screenshots:** 1366-map.png, compared with 1920-map.png
- **What is wrong:** At 1366 the header reads "0 links". Most cells show two or three names and then a dashed "+4", "+6" or "+8". Several cells show nothing but a count chip: Disclosure through 1969 is only "+4", and Retrieval/No date and Disclosure 2000-2016 are the same.
- **Why a reader cares:** 1366 is a laptop width the audience uses. There the map loses its lines entirely and draws marks with no names, breaking two stated rules at once. A reader cannot see what is in a cell or how cells connect without clicking each one.
- **Severity:** major

**4. The thread's dates and placements contradict its own text and each other**
- **Screenshots:** 1920-thread.png, 1366-thread.png, 375-thread.png
- **What is wrong:**
  - Step 1, Harry M. Reid, is dated **2009**, while its text describes July 2008 language.
  - The timeline slice therefore places the "thread start" after steps 2 (2007) and 4 (2008). The steps are numbered 1 to 6 but dated 2009, 2007, 2009, 2008, 2011, 2024, and nothing explains what each date means.
  - In the small map, step 5 (KONA BLUE) sits in the reverse-engineering row at 1920 but in the custody row at 1366.
- **Why a reader cares:** A thread is sold as an authored chain. A date that disagrees with its own sentence, and a band that changes with window width, invite the reader to doubt the chain itself.
- **Severity:** major

**5. The timeline has duplicate events, an axis past its era, and unexplained dimmed labels**
- **Screenshots:** 1920-timeline.png, 1366-timeline.png, 375-timeline.png
- **What is wrong:**
  - The same event appears twice on the same day, under two names: "NYT reveals AATIP" and "New York Times breaks AATIP" (2017-12-16), and "To The Stars Academy formed" and "To The Stars Academy launches" (2017-10-11).
  - The era is labelled 2017-2026, but its axis runs on to a highlighted amber "2029".
  - Some labels are greyed out with no key, for example "The NISPOM is published as a federal rule", "Congress creates a no-waiver oversight regime..." and "Reissued ICD 906 posted".
  - Evidence explorer filter chips break a number across lines: "99 / 6" at 1920 and "10 / 1" at 1366.
- **Why a reader cares:** Duplicates inflate the event count (1,076) and suggest the data was not deduplicated. The 2029 tick and the unexplained grey labels make the reader wonder whether future or disputed items are mixed in. A broken number is read as two numbers.
- **Severity:** major

**What works best:** On the 1920 node page, "The case against" runs as its own column directly beside the claims. It holds 4 conflicts and 9 not-verified items, each specific, dated and attributed. It survives on the phone as the next section after the summary, above the claims.

---

## Triage (phase 5b)

| # | Problem | In 5b scope? | What was done |
|---|---|---|---|
| 1 | testimony and AARO statements at Tier 1; report chip illegible on paper, no key | the chip and the key: yes; the grading: no (5b moves no tier) | the mark is dark amber on paper; a key sits under the claims header on the node page, the report and the evidence explorer; the grading itself (testimony at T1): phase 10, claimant attribution; bookkeeping rows: P5c |
| 2 | wrong connection groups (members of Congress under Money) | no | phase 7 (predicates) |
| 3 | map at 1366: no links, "+N" chips | no | phase 11 |
| 4 | thread dates (step 1 dated 2009); small map puts step 5 in a different band at 1366 | the small map: yes (a defect in how a full cell wrapped); the dates: no (authored thread data) | a band row now grows to hold its fullest cell, so a chip never lands in the next band; thread step dates: phase R |
| 5 | duplicate timeline events, the 2029 year, grey labels; evidence chip counts broken "99 / 6" | the chip counts: yes (introduced in round 1); 2029: kept, it holds a scheduled event and is marked as after the board's date | a chip's count never wraps; duplicates and grey labels: phase 9 |
