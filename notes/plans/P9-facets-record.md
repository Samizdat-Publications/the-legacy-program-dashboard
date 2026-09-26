# Phase 9 task 1: the person facets, as they were made

26 September 2026. The side-car is `research/_person_facets.json`, shipped as `app/public/data/facets.json`.
Its rules are written into the file itself (`_rules`); this note records how the values were reached.

## Method

1. Every person's OWN record (sub, narrative, affiliations, chronology, claims, conflicts, unverified, and
   the board's edges with their predicates and sentences) went to one of twelve Sonnet 5 batches of about
   30 people (a first run of six batches of 60 stalled on a connection outage and was re-cut smaller).
   The authored `status` was withheld from the batches on purpose: it carried a truthy default for part of
   its history, so it was used afterwards as a cross-check, not as evidence.
2. An Opus 5.5 reviewer, in six packets of about 30, checked 184 of the 351: every `dead` (40), every
   `claimant` (96), every `underOath: yes` (21), every person whose authored status is dead or deceased but
   whose batch said otherwise (37), and a seeded 10% sample of the rest (35). What the reviewer wrote is what
   ships, marked `reviewed`.
3. One coordinator override: `vladimir-azhazha` stays vital status unknown, because his record's own
   unverified note says the authored "dead" requires confirmation.

## What the review changed (111 of 184 rows; 66 in basis wording only)

| change | rows |
|---|---|
| vital status unknown to dead (a stated death, or the authored status dead with nothing later) | 36 |
| vital status unknown to alive (a dated act in 2020 or later) | 4 |
| claimant removed (general statements, calls for disclosure, sightings, criticism of an inquiry) | 14 |
| claimant added | 2 |
| military removed where the record says no service record was produced | 9 |
| intelligence removed on the same ground | 4 |
| witness removed (the record never says what the person saw) | 5 |
| roles added from the stated career (official 5, contractor 4, researcher 4, scientist 3, others 6) | 22 |
| role status changed | 25 |
| under oath unknown to yes (a chronology entry "testifies under oath") | 1 |

## The result

| facet | count |
|---|---|
| dead / alive / unknown | 76 / 152 / 123 |
| claimant | 84 |
| witness (first-hand account) | 63 |
| testified under oath | 22 |
| no role the record states | 3 (one of them `thomas-castello`, the persona the record shows was invented) |

## Found on the way

- **A merge defect.** Four people (`thomas-townsend-brown`, `robert-sarbacher`, `louis-witten`,
  `george-trimble`) carried their one authored `unverified` sentence as about 300 one-character items:
  `merge.py` kept a bare string and its list union iterated it. Fixed in `merge.py`; a verify check with a
  poison now refuses a field of single characters. No golden count moved.
- **Judgement calls the reviewers flagged and kept**, for phase R if anyone wants them reopened: an
  affidavit counts as sworn even where the record does not say "sworn" (Jamison, Salas, Fenstermacher,
  Halt, McDonough); a person keeps `former` role status where the record calls them retired although the
  service itself is unverified (Barber, Sands, Jamison); Ben Rich stays a claimant on a Tier 3 attributed
  remark because the board's own edge is typed `made_claims_about`.
- Historical figures whose records never state a death stay `unknown` unless the authored status says
  dead (Gerald Ford and Hillenkoetter were reached that way, in review). That is the rule working: the
  directory says what the record says, and a death the record does not carry is a research gap.
