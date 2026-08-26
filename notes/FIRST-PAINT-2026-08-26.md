# First paint: 12,452ms to 144ms, and it was never the payload

26 August 2026.

## What the previous session concluded, and why it was wrong

The open item read *"split the payload so the board paints fast"*, on the strength of
this measurement:

```
unthrottled   transfer 13557KB  decoded 13557KB  FCP 12576ms  domInteractive 13072ms
fast 3G-ish   transfer 13557KB  decoded 13557KB  FCP 12728ms  domInteractive 67223ms
```

and this reading of it, written in chat: *"12.6s to first paint on localhost, 67s on a
throttled connection. That's pure parse cost, not transfer."*

**Both halves of that sentence were wrong.** It is not parse cost and, on localhost, it
was not any kind of cost the page controls. Three probes settled it.

**A CPU profile of the load.** 13,004ms sampled, of which **11,835ms is `(idle)`** — no
JavaScript on the stack at all. If 13MB of object literals were being parsed, that time
would be attributed to V8, not to idle.

**A trace by event category.** Total main-thread `RunTask` across the whole load: **2,276ms**.
`V8.ParseProgram` 180ms. `V8.CompileScript` 127ms. There is no ten-second parse anywhere
in the trace, because there is no ten-second parse.

**A control page.** A 12.7MB HTML file whose entire body is one padded `<script>`, served
from the same server: **FCP 56ms**. Size, on its own, does nothing.

## What it actually was

Line 9 of the built file, inherited verbatim from `ref/the-vanishing-v2.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

A stylesheet blocks first paint. The board — 956 nodes, 4,513 claims, a canvas map — drew
nothing until a Google server answered, and in a network that stalls that request it drew
nothing for as long as the stall lasted.

| | FCP | domInteractive | usable |
|---|---|---|---|
| font link present | 12,452ms | 13,038ms | 13,139ms |
| same page, request aborted | **132ms** | **1,052ms** | **1,117ms** |

**Be precise about what that 12.4s is and is not.** It is this container: `curl` fetches
the same stylesheet in 427ms, so the stall is how Chromium's request goes through the
agent proxy here, not a property of Stewart's machine or of Cloudflare. The defect is not
the twelve seconds. **The defect is that a file whose stated premise is "single
self-contained HTML file, no server, no runtime deps" could not draw a pixel without a
third party**, and nobody had looked, because the page did eventually render and heavy
pages are expected to be slow.

This is CLAUDE.md §8's inherited-surface trap in a position nobody thought to sweep. The
25 August sweep diffed *prose string literals* against the parent board and found 177
survivors. It never looked at `<head>`.

## The fix

The six latin and latin-ext faces are inlined as `data:` URIs. 86KB of woff2 against a
13.5MB page.

- `assets/fonts/` holds the woff2 files, the `OFL.txt`, and the exact css2 stylesheet
  Google served. `README.md` there records provenance and how to refresh them.
- Licence checked at the source rather than assumed: SIL OFL 1.1, copyright 2017 IBM Corp
  with Reserved Font Name "Plex", fetched from `google/fonts/ofl/ibmplexmono/OFL.txt`. Its
  PERMISSION & CONDITIONS clause names `embed` explicitly.
- `build_dashboard.embed_fonts()` **reads the `unicode-range` and `font-weight` out of the
  served stylesheet** rather than carrying a transcription of 500 codepoints, and exits if
  the stylesheet names a face the repo has no file for. A page with a hole in its typeface
  should not build.
- `mountL0` now repaints once on `document.fonts.ready`. Chip labels are fitted with
  `ctx.measureText`, so a first paint landing against fallback metrics would truncate
  harder than necessary and never correct itself. Data URIs need no network but decode is
  still async, so the window is small and real.

Two gate checks, both self-tested:

| check | poison |
|---|---|
| the built page fetches nothing at runtime | the exact `fonts.googleapis.com` link that shipped for six sessions |
| the typeface ships with the page, at every weight it draws | one weight deleted — page still renders, 600-weight labels quietly mis-fitted |

The first screens **resource-loading positions only** — `href`/`src`/`srcset` attributes
and CSS `url()`. The page carries 2,888 citation URLs as data and every one belongs there;
a check that grepped for `https://` would fire on the entire point of the board.

## Where the time goes now

Measured with gzip, which is what Cloudflare will serve and what `http-server` does not:

| | transfer | FCP | usable |
|---|---|---|---|
| broadband | 3,447KB | 140ms | 1,677ms |
| fast-3G | 3,447KB | 720ms | 17,959ms |

13,672KB decodes from 3,447KB gzipped. The 67s in the original measurement was
`http-server` sending 13.6MB uncompressed at 1.6Mbps — an artefact of the test rig, not a
number any reader will see.

## So: is the payload split still worth doing?

**No, on the evidence, and the item should be closed rather than carried.**

- Paint is 140ms. Parse-to-interactive is ~1.1s for 13.6MB. Neither is a problem.
- What is left is **transfer**, not parse: 18s on fast-3G is 3.4MB moving at 1.6Mbps.
  On LTE that is ~1.4s. The audience is family clicking a link, mostly on wifi.
- Deferring the dossier half of `L0DATA` would cut the initial payload, and it would also
  make a synchronous boot asynchronous underneath 128 assertions that assume otherwise.
  That trade is bad at 140ms paint.

There is a cheap contained variant — emitting the three big literals as `JSON.parse('…')`,
which parses faster than an object literal — and it is **also not worth doing**, because
the thing it improves is the 1.1s to interactive, and the trace says the whole compile and
parse budget inside that is ~310ms.

If the 3G case ever becomes real, the lever is transfer: split `L0DATA.dossiers` into a
second file fetched on first node open. Write it down; do not build it speculatively.

## The generalisable bit

The failure here was not the measurement. It was reading a number and supplying a cause
for it in the same breath — *"12.6s, that's parse cost"* — when nothing in the measurement
said parse. One CPU profile falsified it in ninety seconds.

CLAUDE.md §5 says a check never shown to fail is indistinguishable from a broken one. This
is the sibling: **a number without a mechanism is indistinguishable from a guess**, and it
is more dangerous than a guess because it arrives wearing units.
