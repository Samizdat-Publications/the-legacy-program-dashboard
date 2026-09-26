# Phase 9, detailed: directories, facets, search everywhere, the timeline by section

Written 26 September 2026 from `notes/PLAN-2026-09-24.md` section "Phase 9" and the critic's timeline
findings (unnamed dots, same-day duplicates, an axis to 2029). Branch `redesign/p9-directories`. Opus 5.5,
high. Runs in parallel with phase 8; keep edits to `build_app_data.py`, `router.ts` and the bar small and
local so the two merge cleanly.

1. **`research/_person_facets.json`** (side-car, keyed by person id): `roles` from a closed list
   (official, military, intelligence, scientist, contractor, legislator, witness, claimant, researcher,
   journalist, media, counsel), `vitalStatus` (alive, dead, unknown) and `roleStatus` (current, former,
   unknown), each derived from the person's OWN record (desc, claims, affiliations, chronology), never
   from outside knowledge. Sonnet batches propose; an Opus reviewer checks every `dead`, every
   `claimant`, and a 10% sample; unknown is the honest answer when the record is silent. `status` stays as
   authored. A verify check keeps the vocabulary closed, with a poison.
2. **Directories:** `#/people`, `#/orgs`, `#/programmes`, `#/laws`, `#/places`, `#/events`: sortable tables
   with facets (role, vital status, era, topic, testified under oath, claimant), filters in the URL, every
   row linking its node; phone width as stacked cards. The bar's More menu gains a Directories entry. C
   checks with poisons (every node of the class appears once; facet counts equal the side-car).
3. **Search everywhere:** topics, sources (once phase 8 lands; build the hook now), directories, events,
   threads, nodes and claims in one ranked list with type badges; tier still dominates claims (C20 kept);
   keyboard navigation (arrows, enter, escape). A check with a poison.
4. **The timeline:** lanes become the ten topic sections (an event belongs to the section of its node's
   primary topic; an event with no topic goes in an "Other" lane), the four strands become a filter;
   every event is named (no unnamed dots: a dense year collapses to a counted, NAMED list on click, not
   anonymous marks); clicking an event shows its text, date, grade and its node; `?topic=` scope; same-day
   duplicates (same node, same date, near-identical label) are shown once with both sources; the axis
   ends at the last event year, and a scheduled future event is marked as such. C15 rewritten with its
   poison kept.
5. **The blind critic loop** until the worst in-scope issue is minor (`notes/critic/p9-round-N.md`),
   routes including `people=#/people,events=#/events,timeline=#/timeline`.
