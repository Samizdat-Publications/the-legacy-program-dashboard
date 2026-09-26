# Blind critic, phase 11, round 1

26 September 2026. I read only the brief and the 36 screenshots in `dist/critic/p11-round-1/`. Each screenshot shows one viewport, not the full page. `node` and `person` are the same page (David Charles Grusch) at all three widths, so no screenshot shows the node page for a document, programme or institution.

## The five worst problems, worst first

### 1. The places map cannot be read: overprinted axes and a tangle of crossing leader lines
- **Files:** `1366-places.png` (worst), `1920-places.png`. `375-places.png` has no grid and says "The grid needs a wider screen", which is honest.
- **What is wrong:** At 1366 the US plot is a box of about 320 by 130 px. Its longitude labels print on top of each other in one unreadable string ("125°120°115°110°105°100°95°..." and "85° 80° 75° 70° 65°" run together). The 35° N label sits under a data dot. About 31 leader lines fan out from the dots to name columns on the left and right, and many of them cross, so you cannot follow one line from its dot to its name. At 1920 the plot is larger but the lines still cross (the Huntsville, Fort Meade and Washington lines cross each other, and the western lines form a fan), and the left label "Nevada Test and Training Range" runs into the "125° W" tick.
- **Why a reader cares:** A map exists to show where a place is. A reader cannot tell which dot is Aztec and which is Los Alamos, which breaks the "nothing overlaps" rule. The only reliable route is the list on the right, so the map adds nothing and makes the page look broken.
- **Severity:** blocker at 1366, major at 1920.

### 2. The neighbourhood's link words often do not say why the link exists
- **Files:** `1920-hood.png`, `1920-hood2.png`, `1366-hood.png`, `1366-hood2.png`, `375-hood.png`, `375-hood2.png`
- **What is wrong:** On many rows the only link text is the family name plus "link", in grey italic: "Garry Nolan *role link*", "Wright-Patterson Air Force Base, Ohio *testimony link*", "10 U.S.C. 119 ... *testimony link*", "The Boeing Company *place or time link*", "Booz Allen Hamilton *conduct link*", "Susan Gough *role link*", "GREMLIN *organisation link*", "Vandenberg AFB Incidents *custody link*". The Grusch view has at least 16 such rows. The other rows use a verb with no object, and the reader has to supply the centre node: "The Sol Foundation had in a post", "Jay Stratton made a request of", "House Oversight hearing ... heard testimony from". The node page for the same person does give the reason (for example, for Garry Nolan: "Sol Foundation co-founder; Grusch served as chief operating officer"), but the neighbourhood hides it behind a tap.
- **Why a reader cares:** The board promises that every link says in words why it exists, and the neighbourhood is where a reader goes to test that. A statute, a USAF base and Boeing sitting in a whistleblower's "testimony" or "place" family with no reason suggest guilt by association, and that is exactly what a sceptical reader is watching for.
- **Severity:** major.

### 3. "Tier 1" means two different things, and the home page's own definitions contradict what the pages show
- **Files:** `1920-home.png`, `1366-home.png`, `375-home.png`, `1920-node.png`, `1920-report.png`, `1366-report.png`, `1920-evidence.png`, `1366-evidence.png`
- **What is wrong:** The home legend says T2 is "a named person on the record says so: testimony, an allegation". Yet on the node page and in the report, Grusch's sworn testimony is graded **T1** with a "said on the record" badge. The home prose says AARO and DoD statements are "capped at Tier 2 unless the claim is about what they said". The evidence table then shows AARO's substantive statements as **T1** "the office's own account" (for example, "AAWSAP/AATIP was terminated in 2012 upon the completion of its deliverables"). A two-line disclaimer explaining the redefinition is repeated at the top of the home, node, evidence and report surfaces.
- **Why a reader cares:** The tier is the board's core trust signal. The T1 filter (3,786) mixes "a record proves X" with "a record proves someone said X". A reader who takes "T1 documented" at face value will overrate testimony and AARO's position. A reader who notices the contradiction will stop trusting the counts ("16 at Tier 1, 13 at Tier 2").
- **Severity:** major.

### 4. The places page shows build notes to the reader and admits unsourced coordinates without showing which ones they are
- **Files:** `1920-places.png`, `1366-places.png`, `375-places.png`
- **What is wrong:** The grey paragraph above the map reads, in part: coordinates marked "board table" were "typed into tools/regrade.py's GAZETTEER by an earlier research session, with no source recorded for any value", and replacing them "is a phase R item". None of the list rows in view carries a "board table" mark, so the reader cannot tell which coordinates are unsourced.
- **Why a reader cares:** A journalist should not meet a source-code file name and an internal work-phase label. The paragraph also admits unsourced data on a board whose promise is that nothing is invented, and it does not let the reader separate those values from sourced ones. The honesty is right. The wording and the missing marker undercut it.
- **Severity:** major.

### 5. Home-page copy says size carries meaning, against the site's own rule
- **Files:** `1920-home.png`, `1366-home.png`
- **What is wrong:** Start-here card 1 (AAWSAP) calls it "the largest node on the map at 82 members". Card 5 (AARO) says "Size here means implicated, not authoritative". Neither the atlas nor the neighbourhood sizes anything, and no screenshot shows the sized map these cards refer to.
- **Why a reader cares:** The first thing a reader is told to read describes a visual encoding the site does not show, which breaks the "size never encodes importance" rule. The reader goes looking for a map that is not there, or concludes that some view ranks nodes by size.
- **Severity:** major.

## What works best

The node page puts "The case against" (red "conflict on the record" and amber "not verified" cards) in a column directly beside the claims at 1920 and 1366, so each objection sits next to what it objects to.

## Disposition (the phase 11 session)

| # | Finding | In scope? | What was done |
|---|---|---|---|
| 1 | Places grid unreadable at 1366: longitude labels overprinted, leader lines crossing | yes | Below 1600 wide the grid takes the page's width and the list follows it; longitude labels thin out until they fit; latitude labels sit inside the grid where no marker is under them; leaders run level from each marker to the grid's edge and then straight to their name, with the names in the markers' top-to-bottom order, so no two leaders cross; the two name columns take the western and eastern halves of the markers |
| 2 | Neighbourhood rows say only "role link", or a verb with no object | yes | Rows now read from the centre, which the header names ("held a post at National Reconnaissance Office"); a link with no precise predicate shows the family's phrase and its authored sentence open, so every row says why without a tap |
| 3 | "Tier 1" means two things; Home's key contradicts the pages | no | Phase 10 (claims that know who said them) fixes the key's wording; no tier is moved by presentation |
| 4 | Places page shows a file name and a phase label; unsourced coordinates not marked | yes | The note is plain words; every coordinate in the list is marked "uncited" |
| 5 | Home's start-here copy says a node is "the largest on the map" | no | The start-here texts are Stewart's signed-off wording; raised with him, since the map they describe is now retired |
