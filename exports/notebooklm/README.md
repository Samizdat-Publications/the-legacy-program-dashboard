# NotebookLM export

Generated files. Do not edit them by hand: they are rebuilt from the board's data every
time the script runs, and any edit made here is lost on the next rebuild.

## What is in here

- `00-read-me-first.md` what the board is, the tiers, the axes, how to read the rest
- `01-the-eight-threads.md` the eight authored threads, step by step
- `02` to `08` the programme map, one file per band
- `09-the-people.md` and `10-the-entities-below-the-floor.md` the most connected nodes below the map
- `11-denials.md` every denial, grouped by who denied it
- `12-timeline.md` every dated event, by era and year
- `13-patents.md` the five patents in full prosecution detail
- `14-foia.md` the drafted FOIA requests and the questions behind them
- `15-what-the-records-corrected.md` where the board was wrong and what the record said
- `16-strongest-connections.md` the hundred strongest links, told as short stories

## Regenerate after every board rebuild

```powershell
cd "C:\Users\stewa\ClaudeProjects\Missing individuals connected to defense contractors\the-program"
python tools/build_notebook_export.py
python tools/build_notebook_export.py --check
```

## Load them into NotebookLM

1. Go to notebooklm.google.com and click Create new notebook.
2. Click Add source, then Upload.
3. Multi select every numbered `.md` file in this folder. Skip this README.
4. Wait for them all to finish processing, then open Audio Overview and click Customize.

## Audio Overview customize prompt

```
Take the angle that the recovery programme is real and the denials are the cover story, and
tell it that way for entertainment. Two hard rules you never break. First, whenever you lean
on a claim, say its tier out loud: Tier 1 documented, Tier 2 a named person on the record,
Tier 3 a stated inference. Say a node's board tier, A, B or C, as proximity to the programme
rather than as credibility. Second, never invent a document number, a date, a quote or a
source. If the sources do not carry it, say the record does not carry it. Anything the files
label as an allegation stays an allegation out loud. Spend real time on the corrections file:
the places the board got it wrong are the most interesting part of the story.
```
