# Blind critic, phase 11, round 3

26 September 2026. Read only `tools/critic/BRIEF.md` and the 36 screenshots in `dist/critic/p11-round-3/`.
All captures are one viewport at 1x. Anything below the fold was not seen. `1920-node.png` and
`1920-person.png` show the same page (Grusch), and so do the 1366 and 375 pairs.

## The five worst problems

### 1. Places map: labels are separated from their dots, so readers cannot tell which dot is which

**Files:** `1366-places.png`, `1920-places.png`

**What is wrong:** At 1366 the label "Area 51 (Homey Airport / Groom Lake operating location)" sits at the
right-hand end of the Aztec, New Mexico row. Its leader runs about 330px left to a Nevada dot, and passes
directly over the Aztec marker. Read the row left to right and it says "Aztec, New Mexico ■ Area 51".
"Stanford, California" sits about 135px above its dot on a long vertical leader. Another leader from "SRI
International" crosses it to reach a dot in the same spot. At 1920, "Area 51" and "Kirtland Air Force Base
and Albuquerque" have no leader at all: each sits under a dot that belongs to another label (Groom Lake,
Albuquerque). The dot directly above "Edwards Air Force Base, California" is Vandenberg's, and Edwards' own
dot is off to the right.

**Why a reader cares:** The map has one job: to show where each place is. Here a reader can come away
thinking Area 51 is in New Mexico, or that Edwards is on the coast. Places that share coordinates (Groom
Lake and Area 51, Albuquerque and Kirtland, Stanford and SRI) get one dot and two labels, with nothing to
say the dot is shared.

**Severity:** major

### 2. "Tier 1" is given to sworn testimony and to AARO statements, which the key says are Tier 2

**Files:** `1920-home.png`, `1366-home.png`, `1920-node.png`, `1920-report.png`, `1920-evidence.png`

**What is wrong:** The home key defines T2 as "testimony, an allegation, an official statement". The intro
says AARO and DoD statements are "capped at Tier 2". Yet the Grusch report shows seven "Sworn: ..." quotes as
**T1**, and the evidence table shows AARO's own claims as **T1**. The only thing reconciling them is a small
amber chip ("said on the record", "the office's own account") with a two-line footnote. That footnote has to
be repeated at the top of every surface, which suggests the design already knows readers miss it.

**Why a reader cares:** Grading is the board's central promise. A reader who skims the headline counts
("16 at Tier 1" for Grusch, "T1 3,786" on home) will count testimony and interested-party statements as
documented fact. That is exactly the reading the board says it prevents. The big T1 badge wins over the
small qualifier every time.

**Severity:** major

### 3. Neighbourhood: the denials, the family that matters most, give the least explanation, and the tap cue points at the wrong words

**Files:** `1920-hood.png`, `1366-hood.png`, `1920-hood2.png`

**What is wrong:** In Grusch's DENIALS panel, seven of eight entries are a bare verb and a name: "was denied
by Mark A. Milley", "was denied by Susan Gough", "is disputed by AARO Memorandum ...", "was refused by New
York Times, 'Glowing Auras ...'". Nothing says what was denied, refused or disputed. The one entry with a
sentence ("linked through a denial to DoD SAPCO") describes what SAPCO is, not what it denied. AARO's panel
does the same ("refused AARO Historical Record Report, Volume II", "leaves out Immaculate Constellation
disclosure"). The header says to "tap the words", but the dotted underline, the only visible link cue, is on
the vague fallback phrases ("linked by a role to", "linked through testimony to"). Those already show their
sentence. The specific verbs that hide their sentence look like plain coloured labels.

**Why a reader cares:** The owner's rule is that every connection says why it exists. On this view the case
against says it least. A reader sees "was refused by" a 2017 newspaper article with no explanation and
either mistrusts the link or skips it. The inverted affordance means most readers will never find the hidden
sentences. The node page shows a sentence under every link, so the neighbourhood is the weaker of the two
views of the same data.

**Severity:** major

### 4. Node page: the case against is a separate list, tied to no claim and carrying no source links

**Files:** `1920-node.png`, `1366-node.png`, `375-node.png`

**What is wrong:** "THE CASE AGAINST" is its own column: a middle column at 1920, the right column at 1366,
and a block before the claims on the phone. None of its 4 conflicts or 9 "not verified" items says which of
the 32 claims it answers. None carries a cyan source link. Every claim beside it does carry one. For example,
"AARO's Historical Record Report Volume I (8 March 2024) states ..." names its source in prose, but the name
cannot be opened.

**Why a reader cares:** The owner's rule is that the case against a claim sits beside that claim. Here the
reader has to match conflicts to claims by hand, across columns. A checker can open the source for Grusch's
claims in one click but cannot do the same for the evidence against him, so the page looks one-sided even
though it is not.

**Severity:** major

### 5. Timeline 2017-2026: a chip's text does not start at its date, and lanes hold events from other eras

**Files:** `1920-timeline.png`, `1366-timeline.png`

**What is wrong:** A chip either starts at its date (bar on the left) or ends there (bar on the right), and
both kinds are mixed in the same lane. In "The early record, 1944-1969" lane, four 2026 events have their text
laid across 2022 to 2025. In the secrecy lane, left-anchored and right-anchored chips interleave in the same
rows. The rule is given once, in a 400-character run-on sentence at the top. The "2029" amber tick runs down
every lane but no lane on screen shows an event at it.

**Why a reader cares:** A reader scanning down one year column reads the wrong events as belonging to that
year. That undermines the only thing a timeline is for. The mechanism can only be learned by reading the dense
legend first, and this audience is patient with density but not with confusion.

**Severity:** major

## What works best

On the node page, every entry in the sourced-connections column states the relation in words and names the
counterpart, then gives a sentence, a date span, a tier and a source count. Every link visibly explains
itself there, and the neighbourhood view should match it.

## Disposition (the phase 11 session; the third and last round)

| # | Finding | In scope? | What was done |
|---|---|---|---|
| 1 | Places: names read as the wrong dot's (Area 51 beside Aztec; names with no leader under another dot; shared points unmarked) | yes | Places at the same point share one block of names, one per line, and each name's hover says which place it shares the point with; a spot whose leader passes through another marker, or that sits nearer another marker than its own, is priced out; the search tries 24 directions at 17 distances. Looked at 1366 and 1920 after the fix: the Nevada and New Mexico clusters still need long leaders at 1920. **Remaining, minor**: a cited basemap and a zoomed inset for the dense south-west are phase R |
| 2 | T1 on sworn testimony and AARO statements against Home's key | no | Phase 10 |
| 3 | Neighbourhood denials give the least explanation; the tap cue is on the wrong words | yes | Every denial row now shows its sentence open (the case against must say what was denied); the dotted underline now marks the words that hide a sentence, and goes when it is open. Denial sentences that describe the target rather than the denial are data, for phase R |
| 4 | Node page: the case against is not tied to claims and has no source links | no | An earlier phase's surface (phase 10 ties claims to claimants; phase R) |
| 5 | Timeline chips anchored at either end; lanes by section | no | Phase 9's surface |

No fourth round (the loop's cap is three). The worst in-scope item left is the places grid's crowding in the south-west at 1920, judged minor after the fix: every name is whole and on no other name (C71 holds both), and a name away from its own marker is now the exception, priced rather than forbidden.
