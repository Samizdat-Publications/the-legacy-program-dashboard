# Handoff — the shell is usable, and the deploy is the only thing outstanding

**27 August 2026, end of session.** Read `CLAUDE.md` first, then this. Everything in
`notes/` older than today is record.

**Do not trust any figure below.** Run `python3 tools/state_snapshot.py --gate`.

---

## 1. Four PRs merged today, in this order

| PR | what |
|---|---|
| **#6** | cell mode becomes an explicit opt, the map is what loads, the dossier starts folded and slides, the analyst sizes to its content, no era head under the controls, `tools/walk.js` |
| **#7** | the register stops printing on the controls; the dock becomes a capped reading measure |
| **#8** | the left rail gets the dock's fold, both directions, and `foldPanels` stops leaving its chrome stale |
| **#9** | image register 9 → 12 |

**Everything is on `master`.** This morning's lesson was that an unmerged PR is invisible to
the next session; PR #5 had held the whole of 26 August as an open draft. Nothing is held
back now.

## 2. The one thing outstanding is not code

**The live board at https://the-program-zxz.pages.dev has not been redeployed since the
26th.** Every fix above is invisible there. A cloud session **cannot** run the deploy — there
is no `CLOUDFLARE_API_TOKEN` in the environment, no wrangler config, and the connected
Cloudflare MCP server exposes D1, KV, R2 and Workers but no Pages deploy. It is Stewart's,
and `DEPLOY.md` §0 and §1 are the two blocks.

**A deploy that succeeds and changes nothing is the failure mode to watch for**, and it
already happened once today: Stewart ran both blocks while PR #6 was unmerged, so
`git pull` fetched the same build and wrangler cheerfully redeployed it. The printed URL
cannot tell you whether production moved. Verify by fetching the production hostname and
grepping for a marker the new build has and the old one does not — `@property --dock-w`,
`dockSpine`, `--rail-w`:

```
curl -sS -L https://the-program-zxz.pages.dev/the-program.html | grep -c -- '--rail-w'
```

## 3. What is genuinely still open

**One question for Stewart, and it needs his eyes on a real monitor.** Under about 1750px of
window width the map draws the lattice unlabelled: at 1600 the fit lands at 0.587 against a
0.62 label threshold. Lowering the threshold looked obviously right and was **not** done —
measured on the page, `devicePixelRatio` is 1 and the label at that scale is **4.69 CSS px**.
The render that made it look fine was captured at `deviceScaleFactor: 2`. This is the limit
`CLAUDE.md` §3 names and it cannot be settled from here.

| viewport | fit | label type | labels |
|---|---|---|---|
| 1366 | 0.45 | 3.6px | dropped |
| 1600 | 0.59 | 4.7px | dropped |
| 1920 | 0.74 | 5.9px | kept |
| 2560 | 1.06 | 8.4px | kept |

**Research, in rough order of value:**

1. `notes/REQUEST-QUEUE.md` — 35 logged actions and 18 drafted FOIA requests. Untouched.
2. Image register, 12 of 39. `notes/IMAGE-SOURCING-2026-08-27.md` explains why most of the
   remaining 27 are not a search problem. The foreign bodies (`fab`, `geipan`, `cefaa`,
   `senado-brasil`, `arquivo-nacional-ufo`) are the real remaining work and each needs its
   own jurisdiction's rule read — 17 U.S.C. 105 does not reach them.
3. `person_single_nonprimary_source` is at 5. Four of the five are thin because the record is
   thin; `yury-platov` is the only one open on the merits and needs an environment with
   **Wayback access**, which this one does not have.

## 4. Three things worth knowing before touching the shell

**The panels are one idea in two mirrors.** `--dock-w` and `--rail-w` are both **registered**
via `@property` so they have a `<length>` type and can interpolate; the tracks always exist;
the folded state is a 30px spine that names itself, never `display:none`. If you add a third
panel, copy this and do not invent a fourth mechanism.

**Sample the animation, do not read the CSS.** Three separate slides shipped or nearly
shipped that did not animate: `.dock{transition:width}` on a grid child (never ran), an
unregistered custom property (30px → 762px in one frame with a polite 140ms settle), and the
rail's `display:none`. All three read as correct in the source. `both-drawers-fold-on-a-curve`
counts distinct widths across the transition and poisons the page with `transition:none`.

**`applyChrome` is the single owner of the rail's chrome.** `foldPanels()` used to set the
class and the flag by hand, so FIT ALL and every entry path left the "CLICK TO CLOSE" tab on
screen pointing at an already-closed pane. Nothing in the source said so; the check said so by
measuring one distinct width on a fold.

## 5. State

Derived, 27 August: 956 nodes · 2159 edges · 4513 claims · 2888 unique URLs · 110 L0 nodes,
all with dossiers · 103 of 326 edges at rest · 14 highlights signed off · **12 image records
(11 clear, 1 ask), 98 nodes on the class letter**.

Gate: verify 46 + self-test · capture_strip · audit 40 · runtime 28 · **canvas 30** + every
poison · analyst 15 · `--idempotent`. All green on `master`.
