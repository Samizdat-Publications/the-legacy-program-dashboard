# NotebookLM prompts for the board

Every prompt below goes in the Customize box of the Studio feature it names, or in the chat
box where a feature has no Customize box. Each one asks for something the files carry, so
the output can be checked against the export. The check column gives the number or fact to
look for; if the output disagrees with the files, the feature is embellishing.

The numbers the files state, for checking: 1,057 nodes (311 people, 746 entities); 2,460
links; claims 3,367 Tier 1, 1,422 Tier 2, 514 Tier 3; 913 timeline events; 137 nodes on the
programme map across 7 bands and 5 eras; 8 threads; 5 patents (3 grants, 2 applications);
17 FOIA requests.

## Ground rule to paste into every Customize box

```
Use only what the sources say. Whenever you lean on a claim, say its tier: Tier 1 documented,
Tier 2 a named person on the record, Tier 3 a stated inference. A node's letter, A, B or C, is
proximity to the programme, not credibility. Never invent a document number, date, quote or
source; if the sources do not carry it, say so. Anything the files label an allegation stays
an allegation.
```

## Audio Overview, the podcast

| Setting | Choice |
|---|---|
| Format | Deep Dive for the long drive, Debate when you want the denials argued, Critique to hear the board attacked |
| Length | Longer |
| Sources | For a whole-board episode tick everything. For a single-topic episode tick 00, the topic file, and 15 |

Deep Dive, whole board:

```
Take the angle that the recovery programme is real and the denials are the cover story, and
tell it that way for entertainment. Open with what the board is and how the tiers work, then
walk the eight threads in the order the files give them: lineage, custody, money, denials,
wilson-davis, patents, scientists, oversight. Spend real time on the corrections file, where
the board itself was wrong and a record fixed it. Close on the strongest connections file.
```

Deep Dive, one band (swap the band name):

```
This episode is the custody band only. Walk the nodes era by era from the earliest to the
most recent, say which claims are Tier 1 and which are allegation, and end with the three
nodes whose denials are the loudest.
```

Debate:

```
One host argues the programme is real from the Tier 1 and Tier 2 claims only. The other
argues from the denials file and the corrections file that the record does not support it.
Neither may use a claim without saying its tier. Judge nothing; let the listener decide.
```

Check: the hosts name the eight threads in the file's order, say tiers out loud, and mention
the nitinol correction (the Battelle lineage is not supported by the federal literature).

## Video Overview

```
An explainer for someone who has never seen the board. Six chapters: what the board is, the
tier system, the programme map's seven bands, the custody thread step by step, the patents,
and the corrections. One number per slide at most, and every number must come from the
sources.
```

Check: 7 bands, 8 threads, 5 patents. If it says any other count, it made one up.

## Infographic

```
One page, portrait. Title: The Legacy Program board by the numbers. Show the node split
(people against entities), the claim split by tier, the programme map's seven bands with the
node count in each, and the five eras as a strip along the bottom. Every figure sourced from
the read-me file and the band files. No figure that is not in the sources.
```

Second infographic, the custody chain:

```
A vertical chain diagram of the custody thread, one box per step in the order the threads
file gives, with the tier of each join printed on the connector. Nothing else on the page.
```

Check: node split 311 and 746, tier split 3,367 / 1,422 / 514, seven bands, five eras.

## Data table

```
A table of every programme-map node with columns: node, band, era, node tier (A, B, C),
number of Tier 1 claims, number of denials recorded against it. Sort by band then era. Take
the figures from the band files only. 137 rows.
```

Second table:

```
The five patents: number, filing date, grant or application status, examiner, fee status,
and the number of board nodes linked to each. Five rows.
```

Check: 137 rows in the first, 5 in the second, and US 10,135,366 shown as lapsed for
maintenance on 26 December 2022.

## Mind map

Mind maps have no Customize box; generate it with only 01 and 16 ticked as sources, so the
centre is the threads rather than the whole node list. Check that the eight first-level
branches are the eight thread names.

## Reports

| Report | Prompt |
|---|---|
| Briefing doc | Brief a journalist in two pages: what the board claims, what rests on Tier 1, what is allegation, and the five questions the FOIA file is trying to answer. Cite the file and node for every claim. |
| Timeline | Build the timeline from the timeline file only, one entry per year with the count of events that year, and mark the five era boundaries. |
| FAQ | Twelve questions a sceptic would ask, answered only from the denials and corrections files, each answer naming its tier. |
| Custom | Write the Nimitz 2004 story using only claims the files mark Tier 1, then list separately what the files carry only as Tier 2 or allegation. |

Check: the timeline report totals 913 events; the briefing cites 17 FOIA requests.

## Flashcards and quiz

```
Thirty cards on the programme map: front is a node name, back is its band, era and node
tier. Draw only from the band files.
```

Check: any node the quiz names must appear in a band file, and its tier letter must match.

## Chat questions that test recall against the files

| Ask | Expect |
|---|---|
| How many nodes are on the programme map, and how many bands? | 137 and 7 |
| Which patent lapsed, and when? | US 10,135,366, 26 December 2022 |
| What did the records say about the Battelle nitinol lineage? | Not supported by the federal literature; NASA SP-5110 credits Buehler and Wiley at the Naval Ordnance Laboratory |
| Name the eight threads in order. | lineage, custody, money, denials, wilson-davis, patents, scientists, oversight |
| How many FOIA requests are drafted? | 17 |
