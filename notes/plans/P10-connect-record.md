# Phase 10, task 4: Connect, the weights and the eight test pairs

Written 26 September 2026. The page is `app/src/pages/connect.ts`; its check is C62 in `app/checks/run.mjs`.

## The test pairs

From `notes/redesign-2026-09-24/B-GRAPH-STRUCTURE.md` section 7 (present, so nothing was derived):
Grusch to Lockheed Skunk Works; AAWSAP to the UAP Disclosure Act; Roswell 1947 to the July 2023 hearing;
Bob Lazar to AARO; Project Blue Book to AARO; Salvatore Pais to Skunk Works; Robert Salas to AARO; Eric Davis
to Lockheed Martin. AARO's Historical Record Volume I (`aaro-historical-record-vol1`) lay on a shortest path
for seven of them and was the whole middle of two.

## The weights, and why they are these

A link costs 1, plus its tier (T1 0, T2 0.75, T3 2), plus its family (backbone families 0; a denial, the
board's own analysis or a shared place or time 1; every other family 0.5). Passing through a node costs
`2 x max(0, log2(1 + distinct neighbours) - 3)`. Domain nodes are never passed through. Up to three routes;
each later route may not pass through an earlier route's nodes.

Measured on the board of 26 September 2026 (the prototype is reproduced by the page itself):

| weights tried | first route through AARO Volume I |
|---|---|
| hub penalty `w x log2(1 + deg)` for w = 0.75, 1.0, 1.25, 1.5, 2.0, lighter tier and family costs | AAWSAP to UAPDA and Roswell to the hearing, at every w: raising w penalises every node of the longer alternatives too, so the two-hop route through Volume I keeps winning |
| the same with T3 at 2 and denial / analysis at 1 | Roswell to the hearing still |
| the penalty shifted so a node of seven neighbours or fewer costs nothing (w 2, free below log2 8) | none |

The shift is what the plan asks for in words: prefer specific nodes over connector hubs. A penalty on every
node punishes route length, not hubs.

## The first route found for each pair (board of 26 September 2026, as C62 read it off the page)

| pair | route 1 | through a top-20 hub |
|---|---|---|
| Grusch to Skunk Works | Leslie Kean > Bob Fish > the 2016 Podesta-DeLonge-McCasland email | no |
| AAWSAP to UAPDA | Harry Reid > Chuck Schumer (the appendix's "better story") | no |
| Roswell to the July 2023 hearing | 509th Bomb Group > the House > House Oversight > its subcommittee | no |
| Lazar to AARO | The Black Vault > John Greenewald > Enigma Labs | no |
| Blue Book to AARO | Project Stork > Battelle > AARO's metallic specimen analysis | no |
| Pais to Skunk Works | Puthoff > TTSA > DeLonge > the 2016 email | no |
| Salas to AARO | Malmstrom Oscar Flight > Hastings > the NORAD 1975 log > NORAD-NORTHCOM > the FY2026 NDAA provisions | no |
| Eric Davis to Lockheed Martin | the antigravity DIRD > T. Townsend Brown | no |

Volume I appears in none of the 24 routes drawn for the eight pairs (three each). None of the eight
pairs is joined only through a hub. Several first routes are associations rather than stories (Roswell to the
hearing runs through the House's own structure), which is the appendix's warning: every step prints its
sentence and tier so the reader can see that for themselves, and the method line says a route is a chain of
recorded links, not a finding.
