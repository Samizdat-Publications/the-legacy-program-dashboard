# The analyst gets tools, 11 September 2026

Stewart, 11 September 2026, after reading `notes/HANDOFF-2026-09-04.md`:

> Right now the analyst is just used by me so for now I'm not worried about anything
> regarding restricting it too much. If I make it public it will be bring your own key.
> I want it to be basically able to answer any question I would ask here and be able to
> sift across the data to reason across the dataset, understand the timeline etc.

That answers three of the four open questions in `notes/ANALYST-PLAN-2026-09-03.md`
section 6 and raises the ambition well past what that plan was scoped for, so this
note records both: the plan's decisions 1 to 7, all built, and the thing the plan did
not have, which is the reason the rest of it was worth building.

## 1. The problem the plan did not solve

The plan moved the panel onto every route and made its chips route aware. It left
the analyst reading the same two blocks it always read: one line per node for all
1,057 nodes, plus whichever node the reader had open, in full. Everything else on
the board was invisible to it.

So a chip like "which band is thinnest on Tier 1 evidence" would have been offered
on the map page and answered from 1,057 one-line summaries, by eye. Every question
shaped like *how many*, *which of these*, *what changed between*, *trace this back
to* was a question the analyst could only guess at. That is not "answer any question
I would ask here". A session in this repo can grep, count and open files.

## 2. What was built

| | |
|---|---|
| Twelve tools | `app/src/analyst/tools.ts`. `overview` `find` `nodes` `node` `claims` `timeline` `edges` `path` `thread` `patent` `foia` `map` |
| Where they run | **In the reader's browser**, against the same `/data` files the pages read. The Worker relays a question and a set of results and still holds no copy of the board and still executes nothing |
| The loop | `app/src/analyst/client.ts`. Up to 14 tool rounds a question, parallel calls in one message, thinking blocks echoed back with their signatures, the wire history trimmed only at a plain question so half a tool exchange is never sent |
| Counting | Done by the tool, not by the model. Every filtering tool takes `count_only` and `group_by`, so "how many" is arithmetic over the file rather than a look at a list that was truncated at 40 rows |
| Tracing | `path` is a breadth-first walk of the 2,460 sourced edges and returns the shortest chains with every edge label and tier on the way. No path is an answer: it means the board does not join them |
| The dock | `app/src/analyst/panel.ts`. On every route. Closed, a 148 by 30 tab at the bottom left, in the map's band-label gutter, over nothing. Open, full width and up to 62vh, overlaying |
| The chips | `data/analyst-suggestions.json`, nine keys, 38 chips. `tools/build_app_data.py` reads it and fails the build on a missing key or fewer than three |
| The guard | Any node id the analyst writes in backticks is checked against the index. A real one becomes a link to that node; one the board does not carry is struck through and named. It flags, it never edits |
| Check C18 | The dock and its chips: seven assertions over nine route kinds, with a poison |
| Check C19 | The twelve tools themselves: nineteen assertions, every figure re-derived in the check from the same JSON the browser is reading, with a poison |
| The Worker's validators | `worker/test/validate.mjs`, 19 assertions. Every accepted shape paired with one that must be refused |

### Why the analyst is a tab, and where it is

This took three cuts and the last two were found by checks rather than by reading.

The plan said the panel should sit "below the page content, or in the place Home
shows it today, whichever the current layout takes without a redesign". Neither
works. `.map-root` is `position: fixed` from the bar to the foot of the window and
`.hood` is `height: 100vh`, so on two of the ten pages a panel in normal flow is
drawn underneath the page and cannot be reached at all. A screenshot showed it.

Cut two made it a full-width dock and reserved 30px of height for its closed strip
across the app, `.map-root` and `.hood` included. **CI went red on C5.** The map at
1920 uses the whole viewport, and on CI's fallback font it wraps 48 rows where this
machine wraps 46, which left about 7px between its lowest chip and its own legend.
Taking 30px put the chips 23px into the legend. The map has no 30px to give.

Cut three, which is what shipped: the map and the neighbourhood give up **no**
height. Closed, the dock is a 148 by 30 tab at the bottom left, which is the map's
band-label gutter: the first chip starts at x=158 and the legend's items start at
x=1515, so the tab is over nothing. Open, it is full width and overlays up to 62vh,
on purpose, because a map that re-lays-out every time somebody opens the analyst is
a map that moves under the reader. `#view` still pads its foot by `--dock-h` so a
scrolling page never ends underneath the tab.

C18 now asserts that, and it is scoped the way the reality is: **on a page that
cannot scroll, the tab covers nothing the page drew.** On a page that scrolls, a
reader can move anything out from under it, and the padding guarantees the page's
end is never trapped. That assertion found the evidence page's filter chips sitting
under the tab at scroll zero, which is the acceptable case, and it is the assertion
that would have caught cut two before CI did.

### What the model is told

The cached block carries the two grading systems, the rule that never bends, and an
instruction to use the tools rather than the index: count with `count_only`, reach
for `find` before guessing a node id, reach for `node` before saying anything
specific about a node, reach for `path` before asserting a connection, and report a
tool that returns nothing as an answer. It also asks for node ids in backticks,
which is what makes the guard and the links possible.

The uncached block is `app/src/analyst/state.ts`, built out of the same tools, so
there is one implementation of "what is in this cell" rather than two that drift.
What it buys over letting the model call the tool itself is one round trip on the
commonest question, the one about the thing the reader is looking at.

## 3. Stewart's four questions, answered

| Question | Answer, 11 September 2026 |
|---|---|
| A daily spend ceiling | None set. He is the only reader and said not to restrict it. The per-IP limit of 20 a minute and the global 60 a minute are unchanged and are still the only ceiling |
| Lower the effort or the global limit | Neither. Effort stays `high`, the global limit stays 60 |
| The cache at one hour | **Yes, and it now matters much more than it did.** A tool loop re-sends the whole prefix on every round trip, not once a question. The case index is about 120,000 characters, so an hour of cache is the difference between paying for it once and paying for it every five minutes. `cache_control: { type: 'ephemeral', ttl: '1h' }` |
| A custom domain | Not answered. `worker/src/index.ts` now carries a comment saying exactly where a custom domain goes, and it is a one-line edit plus a redeploy |

Cost is now visible in the panel rather than in a note: every answer prints its
round count and its input, cached and output tokens. No dollar figure is printed,
because this repo holds no price table and a number on the page would be a claim.

**Bring your own key** is in the Worker: an `x-analyst-key` header is used instead of
the account secret and skips the rate limits, because that caller is spending their
own money. The shipped app does not send one. The path exists so the board can go
public on that footing without another Worker change.

## 4. What Stewart has to run

The Worker must be redeployed or the analyst will not answer at all. That is
deliberate: the tool names are pinned in the Worker, `TOOLS_VERSION` is carried by
both sides, and the page refuses to ask a question when they disagree rather than
letting him find out one dead answer at a time.

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program\worker"
npx wrangler deploy
```

The secret survives a redeploy.

## 5. Gate

| | |
|---|---|
| `npm --prefix app run build` | green |
| `node app/checks/run.mjs` | 75 passed, 0 failed |
| `POISON=c18 node app/checks/run.mjs` | POISON c18 SEEN |
| `POISON=c19 node app/checks/run.mjs` | POISON c19 SEEN |
| `node worker/test/validate.mjs` | 19 passed, 0 failed |
| `python tools/build_app_data.py --check` | every count re-derives |

**C19 is the one that matters most**, and it exists because C18 cannot see it.
The tools draw nothing, so there is no DOM that says whether `claims` is
counting or guessing. So `window.__app.analyst` publishes them, on the pattern of
`window.__app.map` and `window.__app.timeline`, and C19 drives all twelve on a
cold page and compares every figure they print with one it derives itself from
the same JSON: 1,057 nodes, 311 people, 137 on the map, 5,303 claims, 3,367 at
Tier 1, 913 timeline events, 10 dated 2004, 2,460 edges, 61 touching AAWSAP,
seven band totals, eight thread ids, five patent numbers, 17 FOIA requests. It
also asserts the two refusals that keep the analyst honest: `path` says the
board does not join two nodes rather than inventing a chain, and `node` says an
id is not on the board rather than inventing a record. Its poison makes the page
fetch a `timeline.json` that is 100 events short, so the tools answer from real
but corrupted data.

C18's own first cut was wrong and the check caught it, which is the fifth or sixth
instance of section 5 of `CLAUDE.md` in these notes and worth writing down: the
sweep used `page.goto` between routes that differ only in their hash, which is a
same-document navigation, so the dock stayed open from the route before and every
second click **closed** it. Four routes were reported broken that were not. The
sweep opens a cold page per route now, which is also the honest case: a cold arrival
is what a shared deep link is.

## 6. Things a next session must not undo

- **The tools run in the browser.** Do not move them into the Worker. The Worker
  holding no copy of the board is the reason a public endpoint is not a liability,
  and the data is already in the reader's browser because the pages read it.
- **Thinking blocks are echoed back untouched.** `cleanBlock` in the Worker returns
  a `thinking` or `redacted_thinking` block as it arrived. Its signature covers its
  text; capping it invalidates the turn.
- **All tool results go back in ONE user message.** Splitting them across messages
  teaches the model to stop making parallel calls.
- **The map and the neighbourhood give the dock no height.** `.map-root` is
  `bottom: 0` and `.hood` is `height: 100vh`, and both must stay that way: the map
  has about 7px of clearance at 1920 on CI and 30px took C5 red. The tab overlays
  the band-label gutter instead, and C18 asserts it covers nothing there.
- **`TOOLS_VERSION` is in two files and they must match.** `app/src/analyst/tools.ts`
  and `worker/src/index.ts`. A tool added on one side is a deploy on both.
- **The cited-id guard flags, it never edits.** A wrong id stays visible and is
  labelled, because deleting it would hide the mistake.
- **`data/analyst-suggestions.json` is Stewart's.** Chips are edited through a table
  in chat, not by a session deciding the wording is better.

## 7. Still open

| | |
|---|---|
| Nobody has asked it a question yet | The Worker is not redeployed as this note is written, so the loop has never round-tripped with the live model. What HAS been exercised: every tool drives against the real data and its answers re-derive (C19), and the Worker's validators accept a real thinking + tool_use + tool_result exchange with the signature intact and refuse ten shapes that must be refused (`worker/test/validate.mjs`). What has NOT: the model choosing which tool to call, and the loop terminating on a real answer. **That is the first thing to do after the deploy.** The honest state until then is "built, gate green, unverified against the model" |
| A dollar figure | Round counts and token counts are on the page. Turning those into money needs a price table this repo does not have |
| The chips quote figures | Four of the 38 quote a count (913 events, 137 of 1,057, 514 Tier 3 claims, seven bands). A research pass that moves one of those has to move the chip. Nothing checks that today |
| Retiring the old shell | `build_app_data.py` no longer scrapes `tools/build_dashboard.py` for the suggestions, which was the dependency item 1 of the 4 September handoff had to clear first. That blocker is gone |
