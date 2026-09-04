# Analyst on every page, plan, 3 September 2026

Written for Stewart, and for the session that builds this. Every number below was
re-checked against `app/public/data/index.json` and the data files today.

## 1. What the analyst can do today

| | |
|---|---|
| Where it appears | The Home page only. `app/src/pages/home.ts:114` calls `analystPanel`, defined at `home.ts:141`. No other page imports it. |
| Is it live | Yes, model backed, through the Worker at `the-program-analyst.stewartgregerson.workers.dev`. The page tries its own address first, that fails on Pages, and it falls through to the Worker. |
| What it is sent | Two blocks. Block one is a one line summary of all 1,057 nodes, cached. Block two is the node you have open, in full: what it is, why implicated, denial posture, up to 40 claims, up to 60 edges, all denials (`app/src/analyst.ts:63-96`). |
| How it knows the node | One regular expression on the address bar, `home.ts:179`. It matches node pages and node reports and nothing else. |
| Chips | Seven, from `app/public/data/analyst.json`. |
| With no Worker | One sentence saying the endpoint is not reachable. There is no scripted fallback in the new shell. |

The seven chips today, word for word:

1. `Where should I start?`
2. `How did AAWSAP become AATIP, and then KONA BLUE?`
3. `What did the Nimitz pilots see in 2004, and what has the government confirmed?`
4. `Trace the custody chain from Grusch back to a named contractor`
5. `Show me every entity the government has formally denied`
6. `Follow the money: who paid, and where does the trail stop?`
7. `Which claims would collapse first under a hostile audit?`

## 2. What it cannot do

| Limit | Why |
|---|---|
| No web, no tools, no writes to the board | The Worker sends a plain message with no tools. The page only appends to a local list of turns. |
| Sees a node only on node pages and node reports | `home.ts:179`. On map, neighbourhood, thread, timeline, patents and evidence it is told nothing is open and gets the ten most connected nodes instead. |
| Never sees patents, FOIA, timeline, threads or the map | `analyst.ts` reads the index and one node file. Nothing else is ever sent. |
| Claims and edges are clipped | Claim text cut at 420 characters, dossier fields at 900, edges at 60, claims at 40. |
| Cited ids are not checked | Nothing verifies a node id in an answer actually exists. A wrong id reads exactly like a right one. |
| Answers are not stored anywhere | No log, no storage. |
| Locked to the current addresses | A custom domain would be refused by the Worker and the panel would say not reachable. |
| Cost is invisible | The Worker returns usage figures and the page shows none of them. |

## 3. Decisions

| # | Decision |
|---|---|
| 1 | The panel moves out of the Home page and renders on every route, including the not found page. It sits below the page content, or in the place Home shows it today, whichever the current layout takes without a redesign. Note for the builder: `renderFrame` paints only the top bar and `main.ts` clears `#view` on every route, so the straightforward mount is a third host element after `#view` in `app/index.html`, painted once and re-chipped on each route change. |
| 2 | Chips are keyed by route kind from `app/src/router.ts`, using `parseRoute(hash).kind`. Keys: home, node, map, hood, thread, timeline, patents, evidence, report. Anything else falls back to home. Three to five chips per key. |
| 3 | The chip wording lives in a new committed file, `data/analyst-suggestions.json`. It is edited only through Stewart's decisions, shown to him as a table in chat first. `tools/build_app_data.py` reads that file instead of scraping the old shell's HTML (`analyst_json`, lines 728 to 745 today), fails the build if any key is missing or has fewer than three strings, and writes `app/public/data/analyst.json` with the chips as a per key map plus a `shape: "per-route"` field. The page still accepts the old flat list, treating it as home only, so a stale data file can never render zero chips. |
| 4 | The block that says what is on screen becomes route aware, so a chip is answerable from what the model actually receives. Node and report routes send the node as today. Thread routes send the thread's steps and the nodes they join. Patents sends the patent in view. Timeline sends that era's events, capped. Map sends the open cell's members, or the band and era summary. Neighbourhood sends the ring members. Evidence sends the active filter and its counts. Each block is capped so the whole prompt stays under the Worker's 300,000 character ceiling. The cached case index block is not touched and stays byte stable. |
| 5 | The page adds a cited id guard. After an answer arrives, any word shaped like a node id that is not in the index is flagged in the transcript as "not a node on this board". It does not block or edit the answer. |
| 6 | The old shell's scripted branch engine is not ported. With no Worker the panel keeps the single "not reachable" line it shows today. |
| 7 | A new check in `app/checks/run.mjs`. For every key, visit a route of that kind and assert the chips on screen equal that key's strings exactly. It ships with a poison switch that forces the key to home on the real page, and the check must go red when the poison is on. A second assertion reads the health line: on a deployment where the Worker answers live it must say live, otherwise it must show the unreachable line. |

Route kinds map onto keys like this: `node-map` and `thread-map` use map,
`node-hood` uses hood, both report kinds use report, `notfound` uses home.

## 4. The chips, per key

Existing chips are marked **now**. Every number below was read out of the data today.

| Key | Chip | Draws on |
|---|---|---|
| home | **now** Where should I start? | index |
| home | **now** Follow the money: who paid, and where does the trail stop? | index, money thread |
| home | **now** Which claims would collapse first under a hostile audit? | claim tiers |
| node | What are this node's Tier 1 claims, and which one is weakest? | node file `claims[].tier` |
| node | Who denies this node, and on what grounds? | node file `denials[]` |
| node | Which of its neighbours sits one sourced edge from AAWSAP? | node file `connections[]`, AAWSAP has 59 neighbours |
| map | The map has seven bands, from reverse engineering to disclosure. Which band is thinnest on Tier 1 evidence? | `map.json` bands, 7 verified |
| map | What changed between the 2000 to 2016 AAWSAP era and the 2017 to 2026 post disclosure era? | `map.json` eras, labels verbatim |
| map | Only 137 of 1,057 nodes are on the program map. What is the strongest node that is not? | `counts.l0` 137, `counts.nodes` 1,057 |
| hood | Which neighbour here shares the most connection types with the node in view? | edges in the node file |
| hood | Is there a pair in this ring with no edge between them that the record says should have one? | ring members |
| hood | Which of these is Tier A on proximity but carries only Tier 3 claims? | node tier plus claim tiers |
| thread | **now** How did AAWSAP become AATIP, and then KONA BLUE? | lineage thread, 6 steps |
| thread | **now** Trace the custody chain from Grusch back to a named contractor | custody thread, 8 steps |
| thread | This thread is one of eight. Which of its steps rests on a single source? | `threads.json`, 8 threads verified |
| thread | The denials thread is eight steps, every join a denial edge. Does the record support all eight? | denials thread, 8 steps verified |
| timeline | **now** What did the Nimitz pilots see in 2004, and what has the government confirmed? | timeline events |
| timeline | 913 events are on the timeline. Which year is densest, and why? | `counts.timeline` 913 verified |
| timeline | What is on the record from 1984 or earlier that touches military intelligence? | earliest dated node is 902d MI Group, 1984-04-04 |
| patents | US 10,135,366 lapsed for maintenance on 26 December 2022. Who let it lapse, and does the board say why? | `patents.json` fee record, verified |
| patents | Docket PAX 182, examiner Thomas M. Dougherty. What does the prosecution history show? | `patents.json`, 6 prosecution entries verified |
| patents | Two of the five are applications, not grants. What happened to US 2019/0295733? | 5 patents, 3 grants and 2 applications verified |
| evidence | **now** Show me every entity the government has formally denied | denied filter |
| evidence | Filter to Tier 3 and tell me which of those 514 claims is load bearing anywhere. | `counts.claims["3"]` is 514 verified |
| evidence | Show me claims that are open questions on nodes with a drafted FOIA request. | 17 FOIA requests, 121 open questions, across 42 nodes |
| report | Summarise this report in five sentences a journalist could check. | the node behind the report |
| report | What in this report would not survive a hostile audit? | claims and tiers |
| report | List every source cited here that is a primary document. | node file `claims[].source` |

## 5. Build order for the next session

Do this in order. One phase per session if it runs long.

**Opus, the code and the check.** Write `data/analyst-suggestions.json` from the
table above. Move the panel out of `pages/home.ts` into its own module, mount it
on every route, key the chips off the route, add the home fallback, make the
state block route aware, and add the cited id guard. Then write the check with
its poison and prove it goes red.

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
npm --prefix app run build
```

**Sonnet, the data rebuild.** Point the generator at the new source file and
regenerate.

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
python tools/build_app_data.py
```

**Sonnet, the gate.** Run the checks with the poison off, then with the poison on
to prove the new check can fail.

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
node app/checks/run.mjs
```

**Sonnet, commit and deploy.** Only after the gate is green with the poison off
and red with it on.

## 6. Open questions for Stewart

| Question | Why it matters |
|---|---|
| What is an acceptable daily spend on the analyst? | There is a rate ceiling but no money ceiling. More chips on more pages means more first turns, and a first turn is the expensive one. |
| Should the Worker's effort setting or the global rate limit come down? | Both are levers on cost. Effort is set to high today and the global limit is 60 requests a minute. |
| Should the cache hold for one hour instead of five minutes? | A longer hold means fewer expensive first turns when a reader wanders between pages. |
| Is a custom domain coming? | If yes, the Worker must be told about it first, or the analyst goes quiet on the new address with no error a reader can see. |

## Not carried over from the scout report

The scout's dollar figures come from an older note about the old shell, and this
repo holds no price table, so no cost in dollars is stated here. The live Worker
health probe was not re-run. Two scout line references were wrong and are
corrected: the analyst lines in `app/checks/run.mjs` are at 976 to 996, not 892
to 901, and the evidence filter keys are in `app/src/evidence/model.ts:41`.
