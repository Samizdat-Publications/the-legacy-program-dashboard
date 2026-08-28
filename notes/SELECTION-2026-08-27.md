# Selection: one panel, no breath, and the half of the particle layer that was missing

**27 August 2026, third shell pass.** Three reports from Stewart on the live board, all
about the state after a chip is clicked.

---

## 1. Two panels for one node, and one of them sat on the map

Clicking a chip called **both** `CMD.expand()` and `CMD.selectNode()`. The first drew the
floating member ledger over the map; the second opened the dossier. Stewart: *"it spawns the
panel on the right plus the panel that says the specifics about that node that floats ...
but then it blocks the map."*

The floating card was also the **worse** of the two. The dossier already lists the same
members through `renderConnections`, and lists them with tier, direction and the reason each
link exists, which the card does not. `L0_CSS2`'s own header has said since 25 August that
*"the entity dossier is now the PRIMARY content and the member ledger is secondary"*; the
click handler had never been told.

**One array meant two things**, which is why this could not just be deleted. `S.l0open`
lights the chip, lights its edges, feeds `lit0` and drives the CLEAR chip — *and* drew the
card. Anything that lit a node covered the map as well. Split: `S.l0open` keeps every
lighting job, a new `S.l0card` drives the floating card, and only `CMD.expand(id)` writes to
it. Selection lights; nothing floats.

`S.l0card` is initialised lazily rather than declared in `S`, because `S`'s literal is
rewritten by three separate `must_replace` patches and a fourth owner of it is how this file
gets bitten.

The close gestures moved with it: clicking the same chip again, and clicking empty canvas,
are keyed on `S.sel` now, because the selection is what a second click is undoing.

## 2. The breath kept pulsing over the thread being read

`bAlpha` ran `l0Breath(animT)` whenever BREATH was on, regardless of selection. So a reader
who had chosen a node had to read its thread through fourteen amber cells fading in and out
behind it. Stewart: *"the entire map and yellow part is fading in and out of the background
rendering it illegible."*

The start-here layer is an **offer**. Once it is taken it should stop asking. `bAlpha` is
held at zero while a selection or an entry path is active. Measured, pixels changing between
frames: **5.5% at rest → 0% selected** for the wash, leaving only the particle layer moving.

## 3. The particle layer was half-built, and the missing half was the direction

Stewart: *"we STILL have not implemented the color and particle system for the lines showing
which way the connection goes that design gave us."*

Half right, and the half that was missing is the one that matters. Design gives motion two
licences and only two:

| case | treatment |
|---|---|
| **directed denial** — the record names the denier | arrowhead **+ travelling particle** |
| **selection** — which end of the edge you are standing on | travelling particle, outward from the reader |

The selection half shipped. The denial half did not, and the renderer says why in its own
comment: *"A directed denial, where the record names the issuer — none yet, so none draw."*
**That was true when it was written and stopped being true the same week.** The denial
adjudication landed 174 verdicts, and **38 directed denials now reach the page** with a
`denier` matching one end. The arrowhead drew for them from the first build. The particle
never did.

So Design's treatment had been shipping as half of itself, with the moving half — the half
that actually carries direction — absent, on the one channel Design said is *"the last unused
channel, which makes it the easiest to spend badly."*

Now: a directed denial carries a particle whether or not anything is selected, running from
the **denier** toward the subject, in the denial red already used for its arrowhead. A
selection still wins where both apply, in cyan, because the reader's own end is the stronger
reference and asserts nothing about the record. Two motions, two colours, never one channel.

`animating()` and the `once` early-return both had to learn about denials, or the loop would
stop and freeze them the moment BREATH was switched off.

## 4. The check that had to change, and why that is not weakening it

`motion-only-where-attested` asserted `stillFrames === 1` — **nothing moves at rest**. That
was a correct proxy for exactly as long as no denial was directed. Design's rule is not
"nothing moves at rest"; it is *"a path carries a particle only if it is a denial or belongs
to the selected node."* Motion at rest became correct, and a proxy that cannot tell correct
motion from the flow-on-every-line treatment Design rejected is worse than no check.

It asserts the real property in three parts now:

| | measured |
|---|---|
| directed denials on the page | 38 |
| distinct frames at STILL, nothing selected | 4 — the map moves |
| **distinct frames once every `denier` is stripped from the page** | **1 — it goes still** |
| distinct frames with a node selected | 5 |

The middle row is load-bearing and is a **page poison**: it nulls `denier` and `denialKind`
on every edge of the live page and requires the motion to collapse. That is what separates
"38 attested denials are moving" from "everything is drifting", and the old assertion could
not have told them apart.

Gate: verify 46 + self-test, capture_strip, audit 40, runtime 28, canvas 30 + every poison,
analyst 15, `--idempotent`. All green.
