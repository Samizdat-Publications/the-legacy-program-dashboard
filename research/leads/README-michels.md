# The Jesse Michels catalogue: what we have, and what the first pull actually was

## The correction that matters

**The first pull was not his catalogue.** 24 transcripts came back and **11 of them
belong to other channels entirely** — they are videos linked from his show notes.
`tools/fetch_transcripts.py` was taking the first YouTube id inside each RSS
`<item>`, and a show-notes block links sponsors, references and the guest's own
channel.

Every id has since been resolved through YouTube's oEmbed endpoint, which answers
from the cloud container even though the transcript endpoint is IP-blocked. The
resolved list is `cached-transcripts.json`. Highlights of what the feed pairing had
claimed versus what the videos are:

| id | feed pairing claimed | actually is |
|---|---|---|
| `h7CJoGKvx3U` | a Michels episode | **Joe Rogan Experience #1945 - Eric Weinstein**, PowerfulJRE |
| `23b44fxvz8I` | "The CIA Scientist Who Cracked Antigravity (Townsend Brown Documentary)" | **Oke Shannon \| Los Alamos Labs, Admiral Wilson Leaks**, Project Unity |
| `R9Yn0hgbVA0` | a Michels episode | **"The Garment of God"**, Lucis Trust |
| `d68a1JfwVsE` | a Michels episode | **DEBRIEFED ep. 45**, Area52 |

**The four mapping agents identified every one of these correctly from transcript
content alone**, before any of them were resolved — including spotting that the
Area52 file was not a Michels episode because the ad read says "Area 52 viewers".
Content beat metadata, which is the argument for having read them.

`catalog_feed` now resolves every candidate id through oEmbed and keeps it only
where the video's real title matches the feed item's. A mismatch is recorded with
its reason rather than silently kept or dropped.

## What the catalogue tells us

`michels-episodes.json` — **140 episodes, 2 October 2024 to 29 August 2026**, with
title, publication date and duration. **Only 2 carry a verifiable YouTube id**,
because the feed links an episode's own video only occasionally. Ids for the rest
need `yt-dlp` against the channel; it is not installed in the cloud container.

## The finding: the Townsend Brown thread is older than the window

The owner asked to pull back to the start of 2025 because "his main thing he
addresses in like 5 different episodes is how all of this ties to Townsend Brown and
electrogravitics". **Those episodes are just outside that window:**

| date in feed | episode |
|---|---|
| 2024-10-05 | **The CIA Scientist Who Cracked Antigravity (Townsend Brown Documentary)** |
| 2024-10-05 | **Is Aerospace Hiding Antigravity From US? (ft. Nick Cook)** |
| 2024-11-15 | Matthew Pines: Anti-Gravity Tech & Inter-Dimensional Aliens |
| 2025-01-24 | Navy Scientist Holds Patents for UFO Technology |
| 2025-04-02 | Senate Staffer Thinks Tesla & Nazi Technology is Being Hidden (ft. Kirk McConnell) |
| 2026-03-30 | NASA Chief: "We Just Built Antigravity Propulsion!" |

The Townsend Brown documentary and the Nick Cook episode are the two the Gerb corpus
points at: `gerb-corpus-25-35.md` records Gerb declining to make electrogravitics
claims himself and sending viewers to **Michels's Townsend Brown video**, and Gerb
separately cites Nick Cook's *The Hunt for Zero Point*. Neither is in the first pull.

Several 2024-10 items share a publication date, which usually means a backfill; treat
these dates as the feed's, not as broadcast dates.

**So the pull should go back to 1 October 2024, not 1 January 2025.** That is 140
episodes rather than 85, and it is the difference between having the thread and
having everything except the thread.

## Why nothing is currently a lead from these files

`data/the-program.json` carries **zero** occurrences of Thomas Townsend Brown,
Biefeld, Babson, the Gravity Research Foundation, Bahnson, RIAS, Louis Witten, Glenn
L. Martin, Bryce DeWitt or Project Winterhaven. "Electrogravitics" appears twice in
6.9MB, both inside the 2017 TTSA node. Four independent agents confirmed this by
direct grep.
