# Lead maps from source corpora

**These files are NOT board content and nothing in them is asserted as true.**
They record what a named source *claims*, so that a later research pass can go
and check it. Every proper noun in them is a lead to verify, not a fact.

`CLAUDE.md` §2 applies here more sharply than anywhere else in the repo, not
less: these are built from **auto-generated YouTube captions**, which corrupt
proper nouns silently and plausibly. A prior session on the sibling board chased
"Holocron Engineering" for some time before it turned out to be **HoloChron
LLC**. Each map therefore opens with a corruption key, and any name that could
not be resolved is marked unresolved and **must not reach the board under the
spelling in the transcript**. Named unresolved at the time of writing:
"Sand Corp.", "SGA", "Eric Tabor", "Charles Ethan Ray", "Special Project Astra".

The transcripts themselves are not committed and are not published. They are
cached under `research/.transcripts/`, which is gitignored.

## The maps

| file | corpus | slice |
|---|---|---|
| `gerb-corpus-01-12.md` | UAP Gerb | files 01-12 |
| `gerb-corpus-13-24.md` | UAP Gerb | files 13-24 |
| `gerb-corpus-25-35.md` | UAP Gerb | files 25-35 |

## The cross-check

`gerb-candidates.txt` is the curated entity list -- confidently resolved names
only. `tools/corpus_crosscheck.py` classifies each against the board's 964 nodes
and 8,086 prose fields:

| verdict | meaning |
|---|---|
| `NODE` | already a node. Nothing to do. |
| `PROSE` | named in some node's narrative but not a node itself. A promotion question, not a discovery. |
| `ABSENT` | the board has never heard of it. **These are the leads.** |

An `ABSENT` row carrying a **NEAR MISS** is one where a rare token from the name
does appear somewhere in the board's prose. Those are printed with their context
because a false `ABSENT` is the expensive error: it sends a researcher after
something the board already carries.

Re-run after any research wave -- the answers move as nodes are added:

```
python3 tools/corpus_crosscheck.py research/leads/gerb-candidates.txt
python3 tools/corpus_crosscheck.py --self-test
```

## What the cross-check already established

**The board is not starting from zero on this source.** It carries nine UAP Gerb
nodes already, including his MITRE, NRO, Hidden Wing, Northrop/TRW, Battelle and
Sandia investigations and the January 2026 American Alchemy episode. What these
maps add is *transcript-level* detail: the entities named **inside** those
videos, which the video-level nodes do not enumerate.

**Nothing in the ABSENT list appears in the parent board** (`ref/the-vanishing-v2.html`),
checked directly. There is no double-work with the-vanishing here.
