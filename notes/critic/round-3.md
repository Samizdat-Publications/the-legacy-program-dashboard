# Blind critic, round 3 (25 September 2026)

Redesign phase 5b, after the round-2 fixes. 30 screenshots from
`node tools/look.js --critic --out dist/critic/round-3`; a separate Opus agent read `tools/critic/BRIEF.md`
and the PNGs and nothing else. Its report, verbatim. This is the last round of phase 5b: every in-scope
item it raises is minor or cosmetic; the major ones belong to later phases (triage below).

---

Blind critic, round 3. I read BRIEF.md and the 30 PNGs in dist/critic/round-3, and opened nothing else.

Ambiguity first: `*-node.png` and `*-person.png` are pixel-identical at all three widths (both show David Charles Grusch). So this round has no evidence on a non-person node page.

## The five worst problems

**1. Sworn testimony is graded Tier 1, but the site defines Tier 1 differently**
- **Files:** 1920-node.png, 1366-node.png, 1920-report.png, 1366-report.png, 375-report.png, 1920-evidence.png
- **What is wrong:** The home page defines Tier 2 as "a named person on the record". Yet Grusch's sworn hearing statements ("Sworn: 'I was informed...'", "Sworn, to Rep. Nancy Mace: 'biologics came with...'") each carry a T1 badge. The same goes for AARO's own statements. A small "said on the record" or "the office's own account" chip explains that T1 means something else here. The header count "16 at Tier 1" and the T1 filter chip in the evidence explorer (3,780) mix documents and allegations with no separation.
- **Why a reader cares:** Tier is the board's core trust signal. A journalist who scans the T1 column, or filters Evidence to T1, will take sworn allegations as documented fact. The legend asks the reader to hold two meanings of "Tier 1" in mind at once.
- **Severity:** major, bordering on blocker.

**2. Most links do not say why they exist**
- **Files:** 1920-hood.png, 1366-hood.png, 1920-map.png, 1366-map.png
- **What is wrong:**
  - On the neighbourhood ring, most direct links carry only a tier: "Garry Nolan T1", "Karl E. Nell T2", "Booz Allen Hamilton T3", "The Boeing Company T3", "Mark A. Milley T2". Only a minority carry a word such as "denial", "testimony" or "institutional ties".
  - The 60-odd outer labels all read the same "two steps", with no "via whom".
  - The legend line "a member too minor for the program map" describes a line style, which makes no sense to a reader.
  - At 1920 the map draws 118 lines with no words at all. They run along column gutters and behind chips (for example around the 2017-2026 oversight stack), and some end in empty space.
  - At 1366 the map draws "0 links" and hides nodes behind anonymous "+N" chips, even where there is room. "Disclosure / through 1969" shows only "+4". "Reverse engineering / no date" says "1 node" and shows only "+1". The same happens in "Oversight / no date" and "Disclosure / 2017-2026".
- **Why a reader cares:** The board promises that every connection explains itself and that nothing is drawn without a name. On the two relational views, the reader gets unnamed marks and bare tier numbers.
- **Severity:** major.

**3. The case against is not beside the claims it answers**
- **Files:** 1920-node.png, 1366-node.png, 375-node.png
- **What is wrong:**
  - On desktop, "THE CASE AGAINST" (4 conflicts, 9 not verified) is a separate column with nothing tying each item to a claim. The first conflict ("directly contradicting Grusch's sworn account of over 40 witnesses") answers the Garcia claim, which sits about 500px lower in another column.
  - On the phone, the whole case against comes before the claims.
  - None of the report screenshots shows a case-against section anywhere on screen.
- **Why a reader cares:** The owner's rule is that the case against sits beside the claim. Here the reader has to match conflicts to claims by hand. The report, the surface most likely to be forwarded, shows no case against in these screenshots at all.
- **Severity:** major.

**4. An internal bookkeeping note is published as a graded claim**
- **Files:** 1920-evidence.png, 1366-evidence.png
- **What is wrong:** Row 4 of the evidence explorer, under 509th Bomb Group, is a T3 "claim" reading "Referenced by the board but no dossier written yet. This node exists so the graph resolves ... see the wave-3 queue". Its source is "Board bookkeeping". It also contains an em dash.
- **Why a reader cares:** It is counted in the 6,099 claims and the 619 T3 figure the home page advertises. It exposes internal work-queue jargon and looks like padding. If one appears, a reader will assume there are more, and doubt every count on the home page.
- **Severity:** major.

**5. The thread's numbered steps contradict their own dates**
- **Files:** 1920-thread.png, 1366-thread.png, 375-thread.png
- **What is wrong:**
  - Step 1, Harry M. Reid, is dated 2009, but its text says he co-sponsored the July 2008 appropriation. Step 2 is dated 2007 and step 4 is dated 2008.
  - The timeline slice therefore runs 2 (2007), 4 (2008), then 1 and 3 (2009).
  - Orange "start here 1 / 10 / 4" tags sit next to the step numbers 2, 5 and 6, so two unrelated numbering schemes collide on the same line.
- **Why a reader cares:** A thread is the owner's authored argument, and this one is about who funded what, when. A date that contradicts its own sentence, in step 1, makes a careful reader stop trusting the chain.
- **Severity:** major.

## Also seen, not in the five
- **Timeline axis (1920/1366-timeline.png):** the 2017-2026 era axis ends in an orange "2029" tick, placed where 2027 would fall, with dots plotted past 2026.
- **Home (1920/1366-home.png):** the "Start from a witness" card is labelled MAP but reads "7 nodes · 0 on the map". The right half of the 1920 home page is empty beside the intro.
- **Patents (1920/1366-patent.png):** the "FIG 1" thumbnails for US 10,135,366 and US 10,322,827 are pages of text, not drawings.
- **Evidence at 1366:** the source-domain chip wraps mid-word ("documents2.theblackvau / lt.com").

## What works best
The Sourced Connections column on the node page (1920-node.png, and 375-hood.png on the phone): each link is grouped by relationship ("Custody", "Money", "Programme links") and carries a plain sentence, a year, a tier and a source count. That is the board's promise, kept.

---

## Triage (phase 5b, final)

| # | Problem | In 5b scope? | What was done |
|---|---|---|---|
| 1 | testimony and AARO statements at Tier 1 | no: 5b moves no tier; the mark and its key are what 5b could do | phase 10 (claimant attribution) decides whether a record of speech keeps T1 |
| 2 | ring and map links without words; map "+N" at 1366 | only the legend wording | legend rewritten ("part of this node, not on the map itself", "two steps away, via a shared member"); sentences on the ring and map lines: phase 11 |
| 3 | case against not tied to a claim; not in the report | no | claim-level links need data: phase 10; the report's case-against section: phase 11 |
| 4 | bookkeeping note counted as a claim | no | P5c (moves claim counts, after phase 5 merges) |
| 5 | thread step 1 dated 2009; "start here" numbers collide with step numbers | the collision: yes (cosmetic) | the tag reads "on the start-here list, no. 1"; the step's year is authored data: phase R |
| - | 2029 tick; "Start from a witness" 0 on the map; FIG 1 text pages; chip wraps mid-word | no (2029 holds a scheduled event and is marked as after the board's date) | phases 9, 8, 11 |
