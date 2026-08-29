# The map inversion — 29 August 2026

**The two renderers swapped roles. Neither was deleted.** Stewart's call, made after
using the live board, and it is also the sign-off `tools/l0_patches.py` had been
waiting for since 25 August — arriving in the opposite direction from what was built.

| | before | after |
|---|---|---|
| `NETWORK` "Network map" | packed L0 map at rest, full graph only while a path or frame was live | the force-directed full graph, always, 964 nodes |
| `PROGRAM` "Program map" | did not exist | Design's packed cells, 110 nodes, the whole map |

The rail builds itself from `VIEWS`, so the tab appeared with no markup change. It sits
second, next to the map it used to be.

---

## 1. What the inversion actually fixed, which is more than a preference

Stewart's complaint was that clicking a node left him unable to see its connections.
The cause was not taste. `selectNode` forced `S.view = 'NETWORK'` and then did **not**
swap the renderer, because `renderSurface` refuses to re-mount the map while it is
already the current view:

```js
if (S.view === 'NETWORK' && MAP && mountedView === 'NETWORK'){ renderNetworkChrome(); return; }
```

So every command that worked by setting a path or a frame — `highlightPath`,
`focusCluster`, `frameNodes`, and the insight callout's "Show me on the map" — worked
from every view **except the one it targeted**. `runtime_check.js` had already recorded
this, in the check name itself: *"S.l0full=true after frameNodes from another view"*,
with a comment noting that three earlier attempts to reach the renderer failed because
they called those commands while already on NETWORK.

Making the full graph unconditional removes that whole class of dead command. It is
not a side effect of the inversion; it is most of the reason the inversion reads as a
fix rather than a swap.

## 2. The six patches

All in `tools/l0_patches.py`. Adding a view costs four string patches on this shell —
the `VIEWS` array, `VIEW_LABEL`, the dispatch map, and the function — and the
inversion cost two more.

| | what | why it is not optional |
|---|---|---|
| a | `viewNetwork` mounts the full graph unconditionally | the change itself |
| b | `PROGRAM` added to `VIEWS`, `VIEW_LABEL`, the dispatch map, and `viewProgramMap()` written | the change itself |
| c | `renderSurface` will not re-mount `PROGRAM` while it is alive | without it every `paint()` rebuilds the canvas and throws away the reader's pan — the map would read as refusing to be moved |
| d | `PROGRAM` excluded from the `pad` class | a map fills its host; `pad` is for the document views |
| e | the number keys read `VIEWS.length` instead of a literal `7` | the literal already undercounted — REPORT has never been reachable by key — and a hardcoded bound silently drops whatever is added after it |
| f | `paint()`'s camera step names **both** map views | see below |

**(f) is the one that would have gone quiet.** The camera step read
`if (S.view === 'NETWORK' && MAP)`, which was right while the packed map *was* the
network rest state. Moving it to a view of its own without widening that guard would
have stopped every repaint on the new tab: breadcrumb, ledgers and register panel
frozen at whatever they said when the tab was opened, while the canvas kept drawing.
Nothing would have thrown.

Four commands also named the wrong view. `showPathOnly`, `showUnattached` and
`showEntry` set `S.view = 'NETWORK'` and draw surfaces that only the packed map has;
after the inversion they would have sent the reader to the force-directed graph and
then rendered nothing, which is the shape of bug that looks like a dead button.
`openPath` set no view at all, so typed at the analyst from elsewhere it lit cells on
a map that was not mounted. All four now name `PROGRAM`.

## 3. The one rule that was deliberately narrowed, not dropped

`l0_patches.py` carried: *"selectNode deliberately does NOT trigger the swap — the
ledger is a table of contents for the dock, and the dock opening must not move the
map."*

That rule survives, narrowed to where it was always aimed:

```js
if (S.view !== 'NETWORK' && S.view !== 'PROGRAM') S.view = 'NETWORK';
```

A reader standing **on the program map** stays there when the dock opens. From
anywhere else a selection goes to the network map, which can answer "what does this
connect to" — the question Stewart was asking when the old behaviour failed him.

## 4. The particle hazard, which is now the default surface

`l0_patches.py` fixed the inherited renderer's particle layer: it drew a particle on
every visible edge, steered by `new Date(s.date) > new Date(t.date)`. Claude Design
named and rejected exactly that — *"a moving dot is a far stronger implication than a
static line"* — and the fix was to draw a particle **only on the selected node's
edges, running away from the reader**, never along the time axis.

**Nothing about that rule changed here, and its importance did.** It used to govern a
fallback that took three attempts to reach. It now governs the first thing every
reader sees. `e.pair.flip` is still in the source for the tick layer and must never
again steer a particle. Both runtime checks that hold the line —
`the full graph asserts no time direction at rest` and
`the full graph moves on the selected node's edges` — still pass, and the comment
above them now says why the block matters more than it did.

## 5. The checks: navigated, not weakened

**`tools/test_packed_layout.js` — 30 canvas assertions, all 30 still pass, none
touched.** One line changed: `page.click('[data-view="NETWORK"]')` became
`'[data-view="PROGRAM"]'`. Not one threshold, expectation or poison was relaxed.
`--self-test` still shows every check rejecting its poison, including the tenth, which
moves every chip 60px on the real page and requires the match to collapse.

**`tools/runtime_check.js` gained three checks and a poison.** The new ones assert the
inversion itself, through the DOM rather than through `S.l0full`, because the flag is
what the code sets and the wrapper is what the reader gets:

| check | reads |
|---|---|
| `network map is the full graph at rest` | no `.l0wrap`, no `.l0crumb`, a canvas over 200px |
| `the full graph keeps its own hop and legend chrome` | `#netchrome` is not empty |
| `the program map tab draws the packed map` | `.l0wrap` and `.l0crumb` both present |
| `the two map views draw different renderers` | the two samples disagree |

**The failure they are aimed at is silent.** If `VIEWS` gains `PROGRAM` but the
dispatch map does not, `[S.view] || viewNetwork` catches the miss and the new tab
renders **the network map** — a "Program map" button showing the wrong map, no error,
nothing in the console. So the check is not "PROGRAM draws something"; it is that the
two views draw *different* renderers and each draws the right one.

`POISON=inversion` navigates to NETWORK where the check expects PROGRAM, so both
samples come from the same renderer. It poisons the page state the check reads, not
the predicate. Demonstrated collapsing:

```
FAIL  the program map tab draws the packed map :: l0wrap=false crumb=false canvas=true [POISON=inversion]
FAIL  the two map views draw different renderers :: POISON=inversion: both samples taken from NETWORK, must collapse
```

`POISON=head` and `POISON=clicks` still fire correctly against the new tab.

**`tools/capture_strip.js` was the quiet one.** It never navigated — it captured on
boot, and on boot the packed map was on screen. After the inversion `.l0crumb` is not
there at rest, and the file's own behaviour was to push the crumb only `if (crumb)`.
Left alone it would not have failed: the crumb would have dropped out of the strip and
`audit_independent.py` would have skipped `breadcrumb object count` **in silence**,
which is the exact failure the comment in that file already warns about. It now
navigates to the tab and **exits non-zero** if the crumb is absent.

`tools/look.js`, `tools/walk.js` and `tools/shoot.js` are cameras, not checks. All
three now know about the tab.

## 6. Dead code removed

The packed map's breadcrumb carried
`if (S.l0full) h += '<span class="l0chip" data-full="0">FULL GRAPH ×</span>'`, and a
click handler for it. That chip **has never rendered**: it is drawn by the packed map's
own `renderChrome()`, which only runs while the packed map is mounted, and that is
exactly the state in which `S.l0full` is false. After the inversion it is not merely
unreached but impossible — the two renderers are on separate views and neither is the
other's fallback. Chip and handler both removed.

## 7. What I looked at, and one defect that is NOT mine

Both views screenshotted at 1600x1000 and read. The network map opens on the full
graph with its hop controls, legend and the STRONGEST PAIR callout; the program map
opens fitted at 0.59x showing all seven bands, with its own breadcrumb, control row,
era heads and START HERE callout. Stewart's "its own tab that's just the whole map" is
what it does.

**A real reading defect is visible on the program map, and it predates this change.**
The rail's vertical `FILTERS — CLICK TO CLOSE` fold tab is an opaque DOM strip that
prints over the map's left gutter and covers the first two characters of exactly two
band labels:

| band | renders as |
|---|---|
| RESEARCH | `SEARCH` |
| OVERSIGHT | `ERSIGHT` |

Both node counts go with them: `30 nodes · mean C 0.87` reads `nodes · mean C 0.87`.
`SEARCH` is not a truncation a reader can decode — it is a different word, and it is
also the name of another view on this board.

**Measured, not assumed.** The same probe run against the pre-inversion build
(`9553d1a`) reports the identical overlap at the identical canvas offset: `.rail-fold`
over the canvas's left 21px, `canvasLeft` 202 in both. So this is inherited, and it is
fixed in its own commit rather than inside the inversion.

No existing check could have caught it. `no DOM overlay covers the map controls` looks
at the control row. `the gutter labels do not scale away with the world` asserts that
ink is present — and ink *is* present, it is simply the wrong ink.

## 8. Gate

Green on all ten steps including `--idempotent`. `l0_nodes` stayed at 110 and no count
moved: this changed where the map lives, not what is on it.

## 9. For Claude Design

**This reverses their spec and they should see it.** The packed layout was Design's,
built to it, with 30 canvas assertions behind it, and it is now a secondary tab while
the inherited renderer is primary. Two things worth their eye specifically:

1. **The motion rule in §4 is theirs**, and it has been promoted from governing a
   fallback to governing the default surface.
2. **A bridge between the two maps was considered and not built.** With a node
   selected on the program map, a control reading "see connections" that switched to
   the network map framed on that node is the literal shape of Stewart's complaint.
   It is an addition to the spec, so it is left as a question rather than built —
   which is the mistake this file's own docstring records having made once already.
