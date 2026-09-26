# Blind critic, phase 7 round 3

Judged from the 30 screenshots in `dist/critic/p7-round-3/` and the brief only. The node and person
captures are identical at every width (both show David Charles Grusch).

## The five worst problems, worst first

### 1. Sworn testimony is badged T1, against the site's own definition of the tiers

- **Screenshots:** 1920-node.png, 1920-person.png, 1366-node.png, 1920-report.png, 1366-report.png,
  375-report.png, 1920-evidence.png
- **What is wrong:** The home page defines Tier 2 as "a named person on the record". On the Grusch page,
  claims 6 onward are his own sworn statements ("Sworn: 'I was informed...'", "'biologics came with some
  of these recoveries'"), and every one is labelled **T1** with a small "said on the record" chip. The
  header counts them as "16 at Tier 1". The Evidence explorer's T1 filter (3,780) includes AARO's own
  statements in the same way, with a "the office's own account" chip.
- **Why a reader would care:** A reader who skims the tier column, or who filters Evidence to T1, sees the
  most contested allegations on the board graded "documented". The chip's explanation ("Tier 1 here
  means it is documented that this was said") redefines the tier for each claim, so a single grade now
  carries two meanings. That weakens the grading the whole board rests on.
- **Severity:** major (close to blocker for anyone who filters by tier)

### 2. The case against sits in its own column, not beside the claim it answers, and it cites no sources

- **Screenshots:** 1920-node.png, 1366-node.png, 375-node.png, 375-person.png
- **What is wrong:** "The case against" is one block for the whole node: a middle column at 1920, a right
  column at 1366, and above all the claims on a phone. For example, the first conflict (AARO's Volume I
  contradicting "his sworn account of over 40 witnesses") answers claim 7, but the two are in different
  columns at different heights, and nothing links one to the other. The conflict and not-verified cards
  have no source line, while every claim has one. One card, "The direct NewsNation URL for the 9 June
  2026 report (cited here via the Wikipedia footnote)", is a research to-do note, not a counter-argument.
- **Why a reader would care:** This breaks the owner's rule that the case against sits beside the claim.
  The rebuttals are the board's strongest material, and a reader cannot see which claim each one answers
  or what document it rests on. The to-do card also tells the reader that the board's own sourcing runs
  through Wikipedia.
- **Severity:** major

### 3. Many neighbourhood links name a category, not a reason

- **Screenshots:** 1920-hood.png, 1366-hood.png
- **What is wrong:** Around the Grusch ring, many edge labels are generic: "The Boeing Company place or
  time link T3", "Booz Allen Hamilton conduct link T3", "IAA FY2024 Sec. 1102 link T3", "Waived SAP
  Notification Group testimony link T3", "UAP Disclosure Act of 2023 board inference link T3", "Luis D.
  Elizondo board inference link T1", "Burlison to MITRE document link T3". Others are real verbs
  ("questioned", "denied", "had in a post").
- **Why a reader would care:** The board promises that every connection says why it exists. "Place or
  time link" and a bare "link" do not. A reader sees Grusch tied to Boeing and has to open something else
  to learn why. "Board inference link T1" also reads as a contradiction in terms.
- **Severity:** major

### 4. The same record appears twice, sometimes at two different tiers

- **Screenshots:** 1920-node.png (connections column), 375-hood.png, 375-timeline.png,
  1920-timeline.png
- **What is wrong:** Grusch's connections list the UAP Task Force twice with the same text ("NRO
  representative to the UAP Task Force, 2019-2021"): once as "held a post at", graded T2, and once as
  "was a member of", graded T1. The timeline repeats events on the same day: "To The Stars Academy formed"
  and "To The Stars Academy launches" (2017-10-11), and "NYT reveals AATIP" and "New York Times breaks
  AATIP" (2017-12-16).
- **Why a reader would care:** When one fact carries two grades, the grading looks arbitrary. Duplicate
  events inflate the headline counts (1,076 events, 2,788 edges) that the home page leads with, and an
  informed reader who notices one duplicate will doubt every other count.
- **Severity:** major

### 5. Marks without names: "+N" chips on the 1366 map and hundreds of dots on the timeline

- **Screenshots:** 1366-map.png, 1920-timeline.png, 1366-timeline.png, 1920-home.png
- **What is wrong:** At 1366 the map header says "0 links". Every cell ends in a dashed "+4", "+1",
  "+2" or "+8", and some cells hold nothing else: Disclosure through 1969 is "+4", No date for reverse
  engineering and oversight is "+1", Disclosure 2000-2016 is "+2". Each cell also repeats "click to
  expand". On the timeline, each strand shows about 10 to 30 labels over a band of hundreds of unnamed
  coloured squares. The labels are packed in a stack that does not line up with the year axis, so a
  reader cannot tell a labelled event's year. That axis also jumps from 2026 to "2029", highlighted in
  amber. On the home page, the "Start from a witness" card says "7 nodes · 0 on the map" but its
  link is marked MAP.
- **Why a reader would care:** This breaks the rule that nothing is drawn without a name. At the laptop
  width many readers use, the map loses all of its links and much of its content. On the timeline, most
  events cannot be read without clicking, and the ones that are named have no readable date. A 2029 tick
  on a record of past events looks like an error.
- **Severity:** major

## Also noticed (not in the five)

- The Grusch claim list includes two definitions from the UAP Disclosure Act (claims 3 and 4) that are
  about the statute, not the person. They pad his count and his printed brief (minor).
- Thread 1: step 1 (Harry Reid) is dated 2009 in the timeline slice, although the thread's own text says
  July 2008 and step 2 is dated 2007. The reading order and the dates disagree (minor). Step 2's text,
  "He is the reason the money existed", sits under the AAWSAP heading, so "He" has nothing to refer to
  (cosmetic).
- Patents: the drawing-sheet grid for the selected filing (10,135,366) opens on another filing's sheet
  (10,144,532 FIG 1). Several "FIG 1" thumbnails are text pages with no figure (minor).
- 375-thread.png: step 2 is cut off at the bottom edge, showing only a coloured square. This is probably
  the capture boundary, not a defect (ambiguous).
- 375-home.png: two search boxes stacked one above the other (cosmetic).

## What works best

The Grusch page's "Sourced connections" column at 1920 is the best thing on the site. Each link gives a
verb, a named counterpart, a one-line reason, a date span, a tier and a source count. That is the
board's promise, kept.
