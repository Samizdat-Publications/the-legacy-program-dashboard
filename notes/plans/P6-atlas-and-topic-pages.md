# Phase 6, detailed: the Atlas, topic pages, the front door

Written 26 September 2026 from `notes/PLAN-2026-09-24.md` section "Phase 6". Branch
`redesign/p6-atlas`, worktree `C:\Users\stewa\ClaudeProjects\tp-p6`. Opus 5.5, high.

**Review, changed by Stewart (25 September 2026).** The plan said "merge only after Stewart's look".
Stewart has since asked for the redesign to run to the end autonomously and will review at the end; the
blind critic (`tools/critic/BRIEF.md`, CLAUDE.md section 3) is the neutral reviewer in the meantime. So
this phase merges on a green gate plus critic rounds until the worst in-scope issue is minor, and the
branch is also deployed to the review site so Stewart can compare.

Input: `app/public/data/topics.json` (sections, 93 rows with lead, status, counts, span, focusEra) and
`app/public/data/topics/<id>.json` (the record with every cite resolved), from phase 5.

## Tasks (each page test-first: a C-series check with a poison on the real page)

1. **`#/topic/<id>`.** Title, kind, section, span; the lead; the summary; three blocks, **What the record
   shows**, **What is claimed**, **What is contested**, each item with its cites rendered as numbered links
   to the claim or edge (tier, the "said on the record" mark from P5b where it applies, source words or
   link, the node it belongs to); members grouped by role, each linking to its node; open questions;
   related topics; a research-gap topic says so plainly. Phone width. Checks: every cited id in the record
   renders exactly once per citing item, with its tier; members by role equal the record; the three blocks
   are present when the record has items; research gaps are labelled; no horizontal overflow at 375.
   Poisons: drop a cite; change a tier; move a member to a wrong role.
2. **`#/atlas`.** Sections as rows, the four eras (index.json's eras) as columns, one chip per topic in
   its focus era with a thin tail across its span; chips one height, one label size (11px), labels never
   shrunk or truncated (a chip wraps its words onto two lines rather than cut them, or the cell grows);
   no lines at rest; focusing a chip (hover or keyboard) draws its related-topic links; filters for kind,
   contested (has contested items) and has open questions. Crowded cells (Congress 2017 to 2026 holds
   about 10) grow in height rather than overflow. Phone: stacked per-section lists. Checks: every topic
   has exactly one chip; every label is drawn in full at 1366x768 AND 1920x950 with no cell mode; no two
   chips overlap; chip height constant; phone stacked lists name every topic. Poisons: drop a chip; shrink
   a label; grow one chip by its member count.
3. **Home, rebuilt around topics.** Search; what this is plus how to read a tier (including the "said on
   the record" mark); **Start here**: the 14 flags as a tour of their topics in the signed-off order (C11
   rewritten to check the tour order against `highlights.json`); the ten sections, each with its topics as
   links; the counts panel (C27 keeps re-deriving it, now with topics). Big questions arrive in phase 10.
4. **The entity page:** an **Appears in** row of topic chips above About (primary topic first: the one
   where the node is an anchor, then by role), equal to the topic membership records; a check with a
   poison.
5. **Navigation:** HOME, ATLAS, TIMELINE, EVIDENCE, PATENTS, plus search and the analyst; MAP, THREADS
   and NEIGHBOURHOOD under a "More" menu until phase 11; `#/map` still works. C9 learns the new routes;
   C17 still passes.
6. **Domain nodes:** a node with `absorbedBy` opens with a clear link to its topic at the top of its page
   (the redirect the plan intends, done as a visible pointer so a shared old link still shows the node).
7. **Look:** the blind critic loop at 1920, 1366 and 375, adding `atlas` and two topic pages
   (`--routes atlas=#/atlas,topic=#/topic/roswell-1947,topic2=#/topic/grusch-allegations`), until the
   worst in-scope issue is minor. Reports in `notes/critic/p6-round-N.md`.

## Acceptance

All checks and poisons green; the critic's worst in-scope issue minor or cosmetic; the branch on the
review site (`DEPLOY.md`), then merged and deployed to production.
