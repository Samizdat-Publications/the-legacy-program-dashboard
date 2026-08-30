# Jesse Michels catalogue: triage

**140 episodes, 2 October 2024 to 29 August 2026, 285 hours.** Source:
`michels-episodes.json`, built from the podcast feed and committed.

**This triage is on TITLES ONLY and is therefore provisional.** The corpus already
proved metadata loses to content: four mapping agents identified all 24 files of the
first pull correctly from transcript text, while the feed's own pairing was wrong for
11 of them. Titles are the right signal for deciding *what to pull*; they are not
evidence of what an episode contains. Bias toward pulling.

| tier | n | hours | what it is |
|---|---|---|---|
| **1 — pull first** | 7 | 15 | the 1940s–80s technical thread: Townsend Brown, electrogravitics, antigravity, patents, Nazi/Tesla, Oppenheimer, reverse engineering |
| **2 — pull next** | 119 | 268 | everything else on subject |
| **3 — off topic by title** | 14 | 5 | Lyme disease, a goat farm, surfing, sperm counts, a breathing exercise |

## Tier 1, in date order

| date | mins | episode |
|---|---|---|
| 2024-10-05 | 112 | **The CIA Scientist Who Cracked Antigravity (Townsend Brown Documentary)** |
| 2024-10-05 | 84 | **Is Aerospace Hiding Antigravity From US? (ft. Nick Cook)** |
| 2024-10-05 | 33 | The 26 Year Old Prodigy Reverse Engineering UFOs \| Deep Prasad |
| 2024-10-19 | 46 | **Did Oppenheimer Work on UFOs?** |
| 2024-11-15 | 261 | Matthew Pines: Anti-Gravity Tech & Inter-Dimensional Aliens |
| 2025-01-24 | 122 | Navy Scientist Holds Patents for UFO Technology |
| 2025-04-02 | 133 | Senate Staffer Thinks Tesla & Nazi Technology is Being Hidden (ft. Kirk McConnell) |
| 2026-03-30 | 158 | NASA Chief: "We Just Built Antigravity Propulsion!" |

**Four of these are dated before 1 January 2025**, which is why the pull window
should start 1 October 2024. The Townsend Brown documentary and the Nick Cook episode
are the two the UAP Gerb corpus explicitly points at.

`Did Oppenheimer Work on UFOs?` matters for a reason the title does not show:
**Oppenheimer is absent from this board**, and a mapping agent recorded Grusch stating
on the record that Oppenheimer authored the classification covering UFO material.

## How tier 2 was ranked

Each title was matched against the surname of every person node on the board. That
found the episodes featuring people already carried — Grusch, Elizondo, Vallée,
Puthoff, Nolan, Shellenberger, Graves, Eric Davis, Coulthart, Salas, Greer, Barber,
Corbell — which are the ones most likely to add claims to existing nodes rather than
new ones.

**Surname matching produces collisions and they are recorded, not hidden.** "Kirk
McConnell" matched Mitch McConnell, "Richard Dolan" matched Charles A. Richard, "Paul
Smith" matched Wilbert Smith, "Greg Rogers" matched Mike D. Rogers, "Alex Jones"
matched Rob Jones. Treat a `boardNames` entry as a hint to check, never as an
identification.

## The two-step rule

Do not pull 285 hours and then triage. The first pull spent a residential connection
on a guided Wim Hof breathing session, a Tinder co-founder interview and a Jake Paul
retrospective, none of which are Michels episodes at all. Enumerate, triage, then
fetch only the selection.
