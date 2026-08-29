L0_DEEPLINK_JS = '\n/* ---- deep links -----------------------------------------------------------\n   Query params already carried the whole state (`?sel=aawsap`), which was enough\n   for a file nobody could share. On a host the URL is the product: a path is what\n   you paste into a message, and `/node/aawsap` survives being read aloud where\n   `?sel=aawsap&v=NETWORK` does not.\n\n   Read accepts BOTH forms, so every link ever copied from the query-param era\n   keeps working. Write prefers the path form only for the plain single-selection\n   case -- the moment the state carries filters, a query, a traced path or a\n   non-default view, it falls back to query params, because a path that silently\n   drops half the state is worse than an ugly URL that keeps it. */\nconst L0_ROUTES = { node: \'sel\', band: \'band\', era: \'era\', q: \'q\' };\nfunction l0ReadPath(){\n  let segs;\n  try { segs = location.pathname.split(\'/\').filter(Boolean).map(decodeURIComponent); }\n  catch (e) { return null; }\n  if (!segs.length) return null;\n  const [head, ...rest] = segs;\n  if (head === \'path\' && rest.length === 2) return { kind: \'path\', from: rest[0], to: rest[1] };\n  if (L0_ROUTES[head] && rest.length >= 1) return { kind: head, value: rest.join(\'/\') };\n  return null;\n}\n'

L0_SEARCH_JS = '\n/* ---- the search grammar ---------------------------------------------------\n   Design specified one field, space-separated tokens ANDed, a bare token as free\n   text, and a set of key:value filters. What shipped was the parent board\'s plain\n   substring match, so `via:bigelow` returned "0 of 956 entities" -- read as free\n   text and found nowhere, which is the worst kind of nothing: it looks like an\n   answer about the board rather than about the query.\n\n   `via:` is the one Design called out, because it reaches the shared members who\n   are NOT on the map: `via:bigelow` returns the map nodes joined by Robert Bigelow\n   without him ever being drawn. */\nfunction l0SearchIndex(){\n  const D = window.L0DATA || (window.__board && window.__board.L0DATA) || {};\n  const byId = {};\n  for (const n of (D.l0 || [])) byId[n.id] = n;\n  const flags = new Set(((D.packed || {}).flags) || []);\n  /* via: the summarised edges name the off-map members they route through. */\n  const via = {};\n  for (const e of (D.summarised || [])){\n    for (const m of (e.via || [])){\n      const k = String(m).toLowerCase();\n      (via[k] || (via[k] = new Set())).add(e.a);\n      via[k].add(e.b);\n    }\n  }\n  const viaLabel = {};\n  for (const k of Object.keys(via)){\n    const meta = (D.nodes || {})[k];\n    viaLabel[k] = ((meta && meta.label) || k).toLowerCase();\n  }\n  return { byId, flags, via, viaLabel, l0n: (D.l0 || []).length };\n}\nfunction l0ParseQuery(q){\n  const out = { free: [], f: [] };\n  for (const t of String(q).trim().split(/\s+/)){\n    if (!t) continue;\n    const m = t.match(/^([a-z]+):(.*)$/i);\n    if (m && m[2] !== \'\') out.f.push({ k: m[1].toLowerCase(), v: m[2].toLowerCase() });\n    else out.free.push(t.toLowerCase());\n  }\n  return out;\n}\nfunction l0Search(pool, q){\n  const Q = l0ParseQuery(q);\n  if (!Q.free.length && !Q.f.length) return [];\n  const IX = l0SearchIndex();\n  const NUM = { deg:\'deg\', claims:\'claims\', denials:\'dnu\' };\n  const num = (n, key, v) => {\n    const L = IX.byId[n.id]; if (!L) return false;\n    let got = L[NUM[key]];\n    if (key === \'denials\') got = (L.di||0) + (L.dr||0) + (L.dnu||0);\n    got = Number(got || 0);\n    const m = v.match(/^([<>]=?)?\s*(-?\d+(?:\.\d+)?)$/);\n    if (!m) return false;\n    const want = parseFloat(m[2]);\n    switch (m[1]){\n      case \'>\':  return got >  want;\n      case \'>=\': return got >= want;\n      case \'<\':  return got <  want;\n      case \'<=\': return got <= want;\n      default:   return got === want;\n    }\n  };\n  const has = (s, v) => String(s || \'\').toLowerCase().indexOf(v) >= 0;\n  return pool.filter(n => {\n    const L = IX.byId[n.id];\n    for (const {k, v} of Q.f){\n      switch (k){\n        case \'id\':       if (!has(n.id, v)) return false; break;\n        case \'cls\':      if (!has(n.cls, v)) return false; break;\n        case \'cluster\':  if (!has(n.cluster, v)) return false; break;\n        case \'tier\':     if (!L || !has(L.tier, v)) return false; break;\n        case \'band\':     if (!L || !has(L.band, v)) return false; break;\n        case \'era\':      if (!L || !has(L.col, v)) return false; break;\n        case \'role\':     if (!L || !(L.roles || []).some(r => has(r, v))) return false; break;\n        case \'flag\':     if (!IX.flags.has(n.id)) return false; break;\n        case \'isolated\': if (!L || !L.iso) return false; break;\n        case \'via\': {\n          /* match the MEMBER by id or label, then keep the map nodes they join */\n          let ok = false;\n          for (const key of Object.keys(IX.via)){\n            if (key.indexOf(v) < 0 && (IX.viaLabel[key] || \'\').indexOf(v) < 0) continue;\n            if (IX.via[key].has(n.id)) { ok = true; break; }\n          }\n          if (!ok) return false;\n          break;\n        }\n        case \'deg\': case \'claims\': case \'denials\':\n          if (!num(n, k, v)) return false; break;\n        default:\n          /* an unknown key is not silently ignored: it becomes free text, so a\n             typo narrows the result rather than quietly widening it */\n          if (!has(n.label + \' \' + n.id, k + \':\' + v)) return false;\n      }\n    }\n    if (!Q.free.length) return true;\n    const hay = (n.label + \' \' + n.id + \' \' + (n.cls||\'\') + \' \' + (n.cluster||\'\') + \' \'\n      + (n.sub||\'\') + \' \' + (n.loc||\'\') + \' \' + (n.narrative||\'\') + \' \'\n      + ((L && (L.roles||[]).join(\' \')) || \'\')).toLowerCase();\n    return Q.free.every(t => hay.indexOf(t) >= 0);\n  });\n}\n'

#!/usr/bin/env python3
"""
l0_patches.py — the L0 program map, as injected JS and CSS.

Held in its own module because it is ~600 lines of surface that has NO upstream
equivalent in ref/the-vanishing-v2.html. Everything here is ours to maintain
forever (SPEC.md P7 says so in as many words), so it is kept separable rather than
smeared through build_dashboard.py's patch list.

WHAT IS HERE
------------
P2  direct-edge aggregation, drawn from the baked model rather than recomputed
P3  summarised shared-member edges, gated at >= 2
P4  tier takes the dash channel at rest (divergence D1)
P5  denial edges drawn directional (divergence D3)
P6  five CMD actions, each with a clickable control
P7  the member ledger
D4  marks and colours for document, event and legislation

WHAT IS NOT HERE
----------------
P8, the bake, is tools/build_l0.py. It is not a patch and could not be one: the
parent board has no baked L0 layout to patch.

P9 deletes the plate-earning rule at rest. No L0 node is a person, so the rule
never fires on this surface. It is left in place for the legacy full-graph map,
which is still reachable (see FULL-GRAPH FALLBACK), and that is the only reason it
survives at all.

FULL-GRAPH FALLBACK — a gap in the handoff, filled deliberately
----------------------------------------------------------------
The design package specifies the NETWORK **rest state** and says the shell, dock
and analyst bar are unchanged. It does not say what happens to the inherited
commands that operate on the full graph: `setHops`, `highlightPath`, `focusCluster`
and `frameNodes`. Replacing the view surface outright would silently break all four
plus the "Show me on the map" control in the insight callout.

SIGNED OFF, 29 August 2026, IN THE OPPOSITE DIRECTION FROM WHAT WAS BUILT.
--------------------------------------------------------------------------
The arrangement above shipped and Stewart used it. His verdict, after clicking a
node and landing on the inherited renderer by accident:

    "I clicked on grusch or someone and instead of our orthogonal map it gave me
    this which is I think the style from the vanishing. I actually think I like
    this better ... it shows the connections better than the orthogonal one which
    I like but when a subject is clicked you can't see all the connections like
    you can here"

    "Maybe the orthogonal map becomes its own tab that's just the whole map so you
    can see it while our primary map is in the style in the screenshots below,
    where the analysis tab sends you"

So the two renderers SWAP ROLES. Neither is deleted.

  NETWORK  "Network map"  the force-directed full graph, all 964 nodes, primary
  PROGRAM  "Program map"  Design's packed cells, the 110-node program map, its
                          own tab, always the whole map

What that fixes is the thing he actually hit: `selectNode` used to force
`S.view = 'NETWORK'` and then NOT swap the renderer, so a click from the dossier
or the ledger left him on the packed map with one chip outlined and no way to see
what it connects to. The full graph answers that question and the packed map does
not, so the full graph is where a selection now lands.

What the packed map keeps is the thing IT answers and the full graph does not:
what the programme looks like whole, arranged rather than settled. It is now
reached deliberately instead of by falling back into it.

The old rule "selectNode must not move the map" survives, narrowed to where it was
always aimed: a reader standing ON the program map stays there when the dock opens.
From anywhere else a selection goes to the network map.
"""

# --------------------------------------------------------------------------- CSS
L0_CSS = """
/* ---- L0 program map ---------------------------------------------------- */
.l0wrap{position:absolute;inset:0;overflow:hidden;
  background:linear-gradient(160deg,#161a20 0%,#11141a 100%)}
.l0wrap canvas{position:absolute;inset:0;width:100%;height:100%;display:block}
/* The head strip is ONE flex row. It used to be two absolutely positioned boxes
   fighting over the same line -- the crumb at left:12px with max-width:calc(100%
   - 24px), the controls at right:12px, both z-index:4 -- so the moment the dock
   narrowed the map the crumb ran the full width and printed straight under the
   buttons. Measured at 798px of map: all six overlapped.

   The fix is layout, not arithmetic. Reserving a fixed width for the controls
   would be the `w - 12*k` bug again: the control row's width is not constant
   (BREATH becomes STILL (SYSTEM) under prefers-reduced-motion, and the crumb
   grows a chip per open node), so any constant is wrong at some state. A flex
   row cannot overlap at any width, and the crumb truncates instead.

   pointer-events are off on the containers and on for their children, so a
   truncated-but-still-boxed crumb can never sit in front of a button. */
.l0head{position:absolute;left:12px;right:12px;top:10px;z-index:4;display:flex;
  align-items:flex-start;gap:12px;pointer-events:none}
.l0head > *{pointer-events:none}
.l0head > * > *{pointer-events:auto}
.l0crumb{flex:1 1 auto;min-width:0;display:flex;flex-wrap:nowrap;
  gap:6px;align-items:center;
  /* nowrap, not wrap: the head strip reserves ONE control row. A breadcrumb that
     wrapped to two would drop straight back onto the era labels. */
  overflow:hidden}
.l0crumb .l0meta{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.l0chip{display:inline-flex;align-items:center;gap:6px;height:22px;padding:0 8px;
  background:#141920;border:1px solid #262e36;color:#b9c2cd;
  font:500 9px/1 'IBM Plex Mono',monospace;letter-spacing:.10em;text-transform:uppercase;
  cursor:pointer}
.l0chip.root{color:#8d97a4;cursor:default}
.l0chip .n{color:#5ed4e6}
.l0chip .x{color:#5c6672;font-size:11px}
.l0chip:hover .x{color:#e8705f}
.l0meta{color:#5c6672;font:400 9px/1 'IBM Plex Mono',monospace;letter-spacing:.10em;
  background:rgba(15,18,22,0.88);padding:5px 7px;border:1px solid #1d242b}
.l0ctl{flex:0 1 auto;min-width:0;margin-left:auto;display:flex;gap:6px;
  flex-wrap:wrap;justify-content:flex-end}
/* The scale a fit button would produce, printed on the button. Dimmer than the
   label: it is the consequence, not the action. */
.l0ctl .hopb .sc{color:#5c6672;margin-left:5px;font-weight:400}
.l0ctl .hopb.on .sc{color:#5ed4e6}
/* AUTO / HELD. Not a button -- it reports which of the two the camera is in, and
   the way back to AUTO is to press a fit button, which is what its title says. */
.l0cam{align-self:center;padding:0 8px;font:500 8.5px/1 'IBM Plex Mono',monospace;
  letter-spacing:.13em;color:#5c6672;border:1px solid #262e36;height:25px;
  display:inline-flex;align-items:center;cursor:help}
/* A FOLDED PANEL IS A SPINE, NOT A NARROW PANEL. The first cut of FIT ALL simply
   set the dossier to 30px and left its contents in place, so the board grew a
   column of single letters stacked down the right edge -- unreadable, and it read
   as damage rather than as a folded panel. Design: "a folded panel keeps its label
   and one click restores it."
   So: hide the contents outright and print one rotated label that is the restore
   control. Nothing about the panel's state is lost, and the way back is the thing
   you are looking at. */
#dock.dock-spine{overflow:hidden;cursor:pointer;position:relative}
#dock.dock-spine > *{display:none}
#dock.dock-spine::after{content:'DOSSIER \2014 CLICK TO OPEN';position:absolute;
  left:50%;top:50%;transform:translate(-50%,-50%) rotate(180deg);
  writing-mode:vertical-rl;white-space:nowrap;
  font:500 8.5px/1 'IBM Plex Mono',monospace;letter-spacing:.18em;color:#8d97a4}
#dock.dock-spine:hover::after{color:#5ed4e6}
/* THE SELECTION BAR. Design §7 puts SHOW ON MAP and CLEAR on a bar "inset by the
   panel width and above both the dossier and the dim", because in their study the
   panels OVERLAY a full-width canvas and an un-inset bar would sit under one.
   Here the panels are grid columns and the map never extends beneath them, so the
   inset is unnecessary and the bar simply pins to the bottom of the map. Same
   intent -- the controls for the selected node stay visible while you read its
   dossier -- without carrying across an offset that would only push it off-centre.
   It appears only when something is selected: a permanent empty bar would spend
   map height on nothing. */
/* ONE BOTTOM COLUMN. The selection bar and the start-here legend were both
   position:absolute at bottom:12px, and they overlapped: every one of the bar's
   five buttons hit-tested to the legend instead of to itself. Measured -- SHOW ON
   MAP, CEDE, PORTHOLE, TETHER and CLEAR, all five dead.

   That is the FOURTH time this file has put two absolutely positioned things on
   one edge and let arithmetic decide whether they clear each other: `w - 12*k`
   reserving chip room whether or not a mark was drawn, the crumb's
   max-width:calc(100% - 24px) running under the control row, geo.headRow as a
   constant for a row whose width varies, and now this. Stacking them by hand --
   bumping the legend to bottom:68px -- would have been the fifth, because the bar
   is 44px only until someone changes it.
   So they share a flex column and the layout does it. */
.l0foot{position:absolute;left:12px;right:12px;bottom:12px;z-index:5;display:flex;
  flex-direction:column;align-items:flex-end;gap:8px;pointer-events:none}
.l0foot > *{pointer-events:auto}
.l0selbar{width:100%;box-sizing:border-box;height:44px;
  display:flex;align-items:center;gap:10px;padding:0 12px;
  background:rgba(15,18,22,0.94);border:1px solid #262e36}
.l0selbar .nm{flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;
  white-space:nowrap;font:500 10.5px/1 'IBM Plex Mono',monospace;color:#e6e9ee}
.l0selbar .nm .cl{color:#5c6672;letter-spacing:.13em;font-size:8.5px;margin-right:8px}
.l0selbar button{flex:0 0 auto;height:25px;padding:0 11px;background:transparent;
  border:1px solid #262e36;color:#8d97a4;cursor:pointer;
  font:500 9px/1 'IBM Plex Mono',monospace;letter-spacing:.13em}
.l0selbar button.pri{border-color:#5ed4e6;color:#5ed4e6}
.l0selbar button:hover{color:#e6e9ee}
.l0selbar .cho{display:flex;gap:0;margin-left:2px}
.l0selbar .cho button{border-left-width:0}
.l0selbar .cho button:first-child{border-left-width:1px}
.l0selbar .cho button.on{border-color:#5ed4e6;color:#5ed4e6;background:#12171d}
/* DIVERGENCE from the comp, and the reason is space. Design's legend sits in a
   panel beside the canvas; this board's map fills its host, so an always-open
   legend covered the NO DATE column and a third of 2017-2026. It is collapsible
   and starts collapsed: the rank numerals on the chips already make the set
   enumerable, and one click puts every reason on screen. A reason one click away
   is not the same as no reason, which is what shipped before today. */
.l0legend{width:330px;flex:0 0 auto;
  background:rgba(20,25,32,0.96);border:1px solid #3a2f1c}
.l0legend.open{max-height:52%;overflow:auto}
.l0legend:not(.open) .l0lg{display:none}
.l0legend h5{margin:0;padding:8px 10px;cursor:pointer;
  border-bottom:1px solid #3a2f1c;
  font:600 8.5px/1.3 'IBM Plex Mono',monospace;letter-spacing:.13em;
  text-transform:uppercase;color:#efb555;display:flex;justify-content:space-between}
.l0legend h5 .x{cursor:pointer;color:#5c6672;font-size:11px}
.l0lg{display:flex;gap:8px;padding:7px 10px;border-bottom:1px solid #22282f;cursor:pointer}
.l0lg:last-child{border-bottom:0}
.l0lg:hover{background:#182029}
.l0lg .r{flex:0 0 18px;font:600 9px/1.4 'IBM Plex Mono',monospace;color:#efb555}
.l0lg .t{font:500 9.5px/1.4 'IBM Plex Mono',monospace;color:#e6e9ee}
.l0lg .w{font:400 9px/1.5 'IBM Plex Mono',monospace;color:#8d97a4;margin-top:3px}
.l0ledger{position:absolute;z-index:6;width:306px;background:#141920;
  border:1px solid #262e36;box-shadow:0 10px 30px rgba(0,0,0,.6)}
.l0lh{display:flex;align-items:flex-start;gap:8px;padding:9px 10px;
  border-bottom:1px solid #1d242b}
.l0lh .mk{flex:0 0 13px;height:13px;margin-top:3px;border:1px solid}
.l0lh h4{margin:0;font:600 11.5px/1.25 'IBM Plex Mono',monospace;color:#e6e9ee}
.l0lh .eb{font:500 8.5px/1 'IBM Plex Mono',monospace;letter-spacing:.13em;
  text-transform:uppercase;color:#5c6672;margin-bottom:3px}
.l0lh .x{margin-left:auto;color:#5c6672;cursor:pointer;font-size:13px;line-height:1}
.l0lh .x:hover{color:#e8705f}
.l0sum{padding:7px 10px;border-bottom:1px solid #1d242b;
  font:400 9px/1.5 'IBM Plex Mono',monospace;letter-spacing:.10em;color:#8d97a4}
.l0sum b{color:#b9c2cd;font-weight:500}
.l0sum .di{color:#e8705f}
.l0body{flex:1 1 auto;min-height:0;overflow:auto;padding:4px 0}
.l0grp{padding:6px 10px 2px;font:500 8.5px/1 'IBM Plex Mono',monospace;
  letter-spacing:.13em;text-transform:uppercase;color:#5c6672}
.l0row{display:flex;align-items:baseline;gap:6px;padding:2px 10px;cursor:pointer;
  font:400 10.5px/1.5 'IBM Plex Mono',monospace;color:#b9c2cd}
.l0row:hover{background:#1a2027;color:#e6e9ee}
.l0row .ld{flex:1;border-bottom:1px dotted #333c47;transform:translateY(-3px)}
.l0row .dg{color:#5c6672;font-size:9px;letter-spacing:.10em}
.l0routed{border-left:2px dotted #8d97a4;margin:4px 0 0 10px}
.l0via{padding:0 10px 3px 10px;font:400 9px/1.4 'IBM Plex Mono',monospace;
  letter-spacing:.06em;color:#5c6672}
.l0tip{position:absolute;z-index:8;pointer-events:none;max-width:290px;
  background:#12171d;border:1px solid #262e36;padding:7px 9px;
  font:400 9px/1.55 'IBM Plex Mono',monospace;letter-spacing:.06em;color:#b9c2cd;
  box-shadow:0 8px 22px rgba(0,0,0,.55)}
.l0tip b{color:#e6e9ee;font-weight:500}
.l0tip .act{color:#5ed4e6}
/* TOP IS THE MEASURED CONTROL-ROW BOTTOM, NOT 44px. The constant cleared a
   single-line strip by 9px and nothing else. Open the dossier and the row wraps:
   measured, the register covered the controls by 22px at 2560, 53 at 1920 and
   1600, and 84 at 1366 -- and .l0reg is z-index 5 against .l0head's 4, so it
   covered them from ABOVE. Same mistake as the era heads, one surface along:
   a constant standing in for something that varies. --l0-ctl is published by
   measureHead, which is the one place the row is actually measured. */
.l0reg{position:absolute;left:0;top:var(--l0-ctl,44px);z-index:5;width:396px;
  max-height:calc(100% - var(--l0-ctl,44px) - 12px);
  background:#12171d;border:1px solid #262e36;display:flex;flex-direction:column}
.l0reg.empty{max-height:none}
.l0reg .none{padding:14px 12px 16px;font:400 10.5px/1.6 'IBM Plex Mono',monospace;
  color:#5c6672;border-top:1px solid #1d242b}
.l0reg h4{margin:0;padding:11px 12px 0;font:600 11.5px/1.25 'IBM Plex Mono',monospace;
  color:#e6e9ee}
.l0reg p{margin:6px 12px 9px;font:400 9px/1.6 'IBM Plex Mono',monospace;
  letter-spacing:.06em;color:#8d97a4}
.l0reg .rows{flex:1;overflow:auto;border-top:1px solid #1d242b}
.l0reg .x{position:absolute;right:10px;top:10px;color:#5c6672;cursor:pointer}
.l0reg .x:hover{color:#e8705f}
.l0zero{color:#e8705f}
"""

# ---------------------------------------------------------------------- the view
L0_JS = r"""
/* ==========================================================================
   THE L0 PROGRAM MAP — rest state of the NETWORK view

   The full graph is 970 nodes and ~3,700 edges at rest, which is not a reading
   surface. This draws the 96 nodes that clear the connectivity floor and rolls
   everything else into member ledgers that open on click.

   Nothing is hidden. Every one of the 970 nodes is in exactly one register and
   the last two are printed in full from the rail. build_l0.py asserts the sum.

   Positions are BAKED (tools/build_l0.py). Nodes never move. That is what makes
   two open ledgers comparable, and it is why a screenshot stays valid.
   ========================================================================== */
const L0_CLS = {
  institution:{ c:'#a795e8', mark:'square'  },
  document:   { c:'#f0d264', mark:'doc'     },   /* D4: new. NOT #c9d2dd — person */
  program:    { c:'#66d69f', mark:'diamond' },   /* owns that, and the two sit    */
  event:      { c:'#7fb4e8', mark:'circle'  },   /* side by side in every ledger  */
  legislation:{ c:'#e08ad0', mark:'bar'     },   /* class bar.                    */
  person:     { c:'#c9d2dd', mark:'square'  },
  location:   { c:'#7fb4e8', mark:'square'  },
  domain:     { c:'#e08ad0', mark:'square'  },
};
/* D1: tier takes the dash channel at rest. The dock has always used
   solid/dashed/dotted for confirmed/claim/open; the map used nothing, so
   credibility rule 1 was true in the prose and not on the canvas. The four new
   edge types' own dashes become selection-only. */
const L0_TIER = { 1:{c:'#5ed4e6',d:[]}, 2:{c:'#efb555',d:[6,4]}, 3:{c:'#8d97a4',d:[2,3]} };
const L0_LABEL_DROP = 0.62;      /* inherited LOD rule, unchanged */
/* Denials, said only as strongly as the record allows. `di`/`dr` count only edges
   that NAME their denier; `dnu` counts the rest. The board used to publish an
   issued/received split derived from the edge's a/b order, which does not encode
   who denied whom. See notes/DENIAL-DIRECTION-2026-08-26.md. Until `denier` is
   authored, a denial is an undirected link and the board says so. */
/* One character, because the chip has room for one. The image takes this slot when
   a node has one; the letter is the fallback, so class is readable on every chip at
   every zoom. Class keeps the LEFT RULE and tier keeps the stroke: Design's channel
   table originally said the reverse and corrected itself, because once a node
   carries a photo the glyph is gone and class would have nowhere persistent to
   live. Tier is three values and prints as text in the dossier; class is five and
   must survive on the chip. */
const L0_GLYPH = { institution:'I', program:'P', event:'E', legislation:'L',
                   document:'D', person:'p' };
/* Middle truncation, never end truncation. "AARO Historical Record Volume 1" and
   "... Volume 2" are identical under an end ellipsis, and the tail is exactly where
   this corpus puts its distinguishing token: volume numbers, years, Roman numerals,
   Sec. references. Head takes 62% of the budget, the tail takes the rest. */
function l0Fit(ctx, s, room){
  if (ctx.measureText(s).width <= room) return s;
  let lo = 1, hi = s.length;
  while (lo < hi){
    const mid = Math.ceil((lo + hi) / 2);
    const head = Math.ceil(mid * 0.62), tail = mid - head;
    const t = s.slice(0, head) + '\u2026' + s.slice(s.length - tail);
    if (ctx.measureText(t).width <= room) lo = mid; else hi = mid - 1;
  }
  const head = Math.ceil(lo * 0.62), tail = lo - head;
  return s.slice(0, head) + '\u2026' + s.slice(s.length - tail);
}
function l0Denials(n){
  if ((n.di||0) + (n.dr||0) > 0) return 'denials ' + (n.di||0) + ' issued \u00b7 ' + (n.dr||0) + ' received';
  const u = n.dnu || 0;
  if (!u) return 'no denial links';
  return u + ' denial link' + (u === 1 ? '' : 's') + ' \u00b7 direction not attested';
}
const L0_MARK = 13;              /* legacy point-cloud glyph. Still used by the
                                    FULL GRAPH fallback; the packed map draws chips. */
/* ---- packed-cell palette -------------------------------------------------
   Taken from the comp Stewart signed off (tools/l0_comp.html), which took them
   from this file in the first place. Chip fill is flat and identical for every
   node: SIZE AND FILL ARE NOT CHANNELS on this board, and the largest node is
   AARO, which it treats as implicated rather than authoritative. */
const L0_PACK = {
  chipFill:'#12171d', chipLine:'#3b444f', chipLineA:'#4a6b8f', chipLineFlag:'#efb555',
  bandFill:'#141920', bandAlt:'#12161c', bandLabel:'#5c6672', bandN:'#3b444f',
  colHead:'#8d97a4', colNote:'#5c6672', colRule:'#262e36', glyph:'#4f5964',
  restLine:'#2f3a45', restAnchor:'#2a3b44', restDenial:'#5a3f3c',
  pointer:'#efb555', iso:'#e8705f', denial:'#e8705f', ink:'#e6e9ee', ink2:'#b9c2cd',
};
/* Three view options, all ON by default. Stewart's call, 25 August 2026, having
   looked at the comp with all three on: "want all 3 options turned on". They are
   controls rather than constants because each one answers a different question and
   a reader who wants the arrangement alone should be able to get it. */
/* CELLS is the count matrix, and it is OFF by default and is never turned on by a
   scale. It used to be `view.k < L0_LABEL_DROP`, so ONE constant decided both
   "stop drawing labels" and "collapse every chip into a numeral" -- and every fit
   at a normal window size lands below 0.62, so every fit showed the matrix instead
   of the map. Stewart, 27 August: "it takes me to the view where there are numbers
   on the map instead of the map itself ... you have to zoom too far to get the map
   back."

   Splitting the constant is not enough. At 1366 the fit is 0.222, so ANY automatic
   threshold still ambushes a laptop. The matrix is now a mode the reader asks for
   and can always leave. notes/CELL-MODE-2026-08-27.md. */
const L0_OPT = { rest:true, flags:true, labels:true, cells:false };
/* BREATH / ONCE / STILL, per Design's start-here layer. At rest the flagged set
   surfaces together over about a second, holds, fades, and the board sits clean
   before the next: the board raising its hand ONCE reads better than fourteen
   separate events, so they are in sync, not staggered. ONCE does it a single time
   on load in rank order. Between breaths only the rank numeral stays, so the set
   is findable and the highlight is never permanently on the map. */
const L0_ATTN = ['breath', 'once', 'still'];
const L0_BREATH_MS = 7000;
/* The keyframe, restated as a function of time because this is a canvas: off
   until 12%, up to full by 40%, back to nothing by 64%, clean until the cycle
   turns over. */
function l0Breath(ms){
  const p = (ms % L0_BREATH_MS) / L0_BREATH_MS;
  if (p >= 0.64) return 0;
  if (p <= 0.12) return p / 0.12;
  if (p <= 0.40) return 1;
  return 1 - (p - 0.40) / 0.24;
}

/* ---- the image tile ------------------------------------------------------

   The chip's third slot is [rule][image|glyph][label][rank][mark]. Until now it
   always drew the class letter, because data/l0-images.json is deliberately empty
   -- a record there asserts that a specific image exists at a specific URL under a
   specific licence, which is a sourcing claim like any other and needs a research
   pass, not a plausible guess.

   The RENDER half does not need the data to exist, and leaving it unbuilt meant the
   sourcing pass would have landed on an untested branch. It is built and tested
   here against injected fixtures; the register stays empty until someone verifies
   real images.

   Three things the layout stage has already decided by the time we get here, and
   which this must not re-decide:
     - only `clears` and `ask` reach the model at all. An image that does not clear
       is not drawn, exactly as an unsourced claim is not printed.
     - `photoKind` is load-bearing. A portrait may be cropped to a circle. A MARK
       MAY NOT -- an institutional seal cropped to a circle is a different mark, and
       several of them carry statutory restrictions on alteration that are stricter
       than copyright. Marks are contain-fitted inside the slot, never cover-cropped.
     - `ask` ships WITH its reason. The reason is prose and belongs in the dossier;
       what the chip can carry is an amber ring, so the doubt is visible at a glance
       rather than only to a reader who opens the panel. */
const L0IMG = new Map();          /* url -> HTMLImageElement | 'failed' */
function l0Img(url, onLoad){
  if (!url) return null;
  const hit = L0IMG.get(url);
  if (hit) return hit === 'failed' ? null : (hit.complete && hit.naturalWidth ? hit : null);
  const im = new Image();
  im.decoding = 'async';
  /* A load failure is permanent and silent: the chip falls back to the class
     letter, which is a supported state and says what the node IS. A broken-image
     box would be worse than the letter it replaced. */
  im.onerror = () => { L0IMG.set(url, 'failed'); };
  im.onload  = () => { if (onLoad) onLoad(); };
  L0IMG.set(url, im);
  im.src = url;
  return null;
}
function l0DrawTile(ctx, im, n, x, y, size){
  const r = size/2, cx = x + r, cy = y + r;
  ctx.save();
  if (n.photoKind === 'mark'){
    /* contain: the whole mark, undistorted, inside the slot. No clip. */
    const sc = Math.min(size/im.naturalWidth, size/im.naturalHeight);
    const dw = im.naturalWidth*sc, dh = im.naturalHeight*sc;
    ctx.drawImage(im, cx-dw/2, cy-dh/2, dw, dh);
  } else {
    /* cover, circular: a portrait may be cropped. */
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI*2); ctx.clip();
    const sc = Math.max(size/im.naturalWidth, size/im.naturalHeight);
    const dw = im.naturalWidth*sc, dh = im.naturalHeight*sc;
    ctx.drawImage(im, cx-dw/2, cy-dh/2, dw, dh);
  }
  ctx.restore();
  if (n.photoClearance === 'ask'){
    ctx.strokeStyle = L0_PACK.pointer; ctx.lineWidth = 1;
    ctx.beginPath();
    if (n.photoKind === 'mark') ctx.rect(x+0.5, y+0.5, size-1, size-1);
    else ctx.arc(cx, cy, r-0.5, 0, Math.PI*2);
    ctx.stroke();
  }
}

function mountL0(host){
  const D = L0DATA, byId = {};
  for (const n of D.l0) byId[n.id] = n;
  /* The packed-cell layout, merged into the model at build time by
     l0_patches.merge_packed. There is no fallback branch: if this is missing the
     map has no geometry and the honest thing is to say so on the surface rather
     than draw 110 chips in a heap at 0,0. */
  const PK = D.packed;
  if (!PK || !PK.worldW){
    host.appendChild(el('div','l0meta'))
        .textContent = 'PROGRAM MAP UNAVAILABLE — no packed layout in the model. '
                     + 'Run node tools/build_l0_layout.mjs, then rebuild.';
    return { repaint(){}, pairs: [], destroy(){}, fitScale(){ return 1; }, view:{k:1,ox:0,oy:0} };
  }
  /* FROZEN CHROME. The model reserves geo.gutter (148) on the left and
     geo.headRow (46) on top for the row and column labels, and the packed cells
     start outside both. Those two strips are held in SCREEN space here rather
     than world space, and the map is clipped and pan-clamped to what is left.

     This is a divergence from tools/l0_comp.html, and it exists because the comp
     is one static full-view and the map pans. The first cut drew the labels
     pinned but not clipped, and tools/test_packed_layout.js caught six chips
     rendering UNDER the column-head plate at 12% opacity -- readable as a smear,
     invisible as a defect to anyone reading the source. Freezing the strips means
     no chip can ever be beneath them, and pan-clamping means the reader can never
     scroll the map off into empty world either.

     geo comes from the model: merge_packed copies config.geo onto L0DATA.packed,
     so PK.geo is populated and PAD tracks it. The fallbacks below are for the
     degenerate model only. headRow was 46 and that was simply too short -- see
     the note in tools/build_l0_layout.mjs. */
  const GEO = PK.geo || {};
  const PAD = { l: GEO.gutter || 148, t: GEO.headRow || 46, ctl: 10, gl: 10 };
  /* PAD.t IS MEASURED, not trusted. geo.headRow is a constant in the model -- 76,
     chosen when the control row was one line of six buttons -- and the era heads
     are drawn immediately below it. Adding the two fit scales and the AUTO/HELD
     chip made the row wider than the map at narrow widths, where it either
     overflowed under the dossier (measured: the BREATH button, 15 dead sample
     points, blocked by .dock-grip and .edoss) or, once allowed to wrap, would have
     dropped its second line straight onto the era labels.

     Both failures are the same mistake -- a constant standing in for something
     that varies -- and it is the `w - 12*k` chip bug for the third time in this
     file. So the strip reserves what the row actually occupies. Any future control
     can be added without anyone remembering to retune a number, and head-row-clear
     keeps guarding the result. */
  const HEAD_MIN = GEO.headRow || 46;
  /* The era band: one 9px label and one 8.5px note, with leading. Authored here
     once and consumed by both measureHead and columnHeads, so the reserve and the
     baselines can never disagree -- they used to, by 22px and 9px of hard-coded
     offset against a reserve computed somewhere else. */
  const ERA_BAND = 32;
  function measureHead(){
    const el = host.querySelector('.l0head');
    if (!el) { PAD.ctl = 10; PAD.t = HEAD_MIN; publishHead(); return; }
    /* THE BOTTOM EDGE OF THE CONTROL ROW, not its height.
       This is the 27 August fix and the arithmetic is worth writing down, because
       the previous version looks correct and is not. `.l0head` is pinned at
       top:10px, so its bottom is 10 + h. The reserve was `PAD.t = h + 20` and the
       era label was drawn at `PAD.t - 22`, i.e. at h - 2 -- twelve pixels ABOVE
       where the controls end, always, at every width.
       It only ever looked right because HEAD_MIN is 76 and a single-row control
       strip is about 25px tall, so the floor dominated and bought 19px of accidental
       clearance. Let the row WRAP to two lines -- which it does as soon as an entry
       path chip widens the left group -- and h jumps to ~58, the floor stops
       dominating, and the heads print under the buttons at partial opacity.
       That is exactly the screenshot Stewart sent: "2000-2016 / AAWSAP / AATIP"
       legible through the START HERE button.
       Measuring the bottom edge makes the clearance structural instead of lucky. */
    const r = el.getBoundingClientRect();
    const hb = host.getBoundingClientRect();
    PAD.ctl = Math.ceil(r.bottom - hb.top) + 8;
    PAD.t = Math.max(HEAD_MIN, PAD.ctl + ERA_BAND);
    publishHead();
  }
  /* THE LEFT EDGE HAS THE SAME PROBLEM THE TOP HAD, and it hid for longer because
     it does not look like a defect -- it looks like a shorter word.

     `.rail-fold` is the rail's fold tab: position:fixed at the rail's right edge,
     22px wide, deliberately hanging INTO the map the way `.dock-fold` hangs into it
     from the other side. The band labels are drawn at x=10 inside the canvas, so
     the tab prints over their first characters. Measured at 1600x1000: RESEARCH
     renders as "SEARCH" and OVERSIGHT as "ERSIGHT", and both node counts go with
     them -- "30 nodes . mean C 0.87" reads "nodes . mean C 0.87".

     "SEARCH" is not a truncation a reader can decode. It is a different word, and
     it is also the name of another view on this board. Only two of the seven bands
     are hit, because the tab is 150px tall and vertically centred, which is why it
     reads as two oddly-named rows rather than as an overlay.

     MEASURED, NOT CONSTANT, for exactly the reason PAD.t is: --rail-w changes when
     the rail folds, and the tab rides that edge on a 320ms curve. A constant would
     be right in one state and wrong in the other.

     AND CLAMPED BY THE TEXT, NOT BY A NUMBER. The gutter is 148px and the longest
     pair of lines is REVERSE-ENGINEERING over "15 nodes . mean C 2.6". Insetting
     past what those actually measure would trade a covered label for an overflowing
     one, which is the same defect pointing the other way -- and the chip field
     starts at PAD.l, so it would collide rather than merely look wrong. The widest
     label is measured through ctx, at the fonts bandLabels really uses. */
  let GUT_W = 0;
  function gutterTextWidth(){
    if (GUT_W) return GUT_W;
    let w = 0;
    ctx.save();
    for (const b of bandRows()){
      ctx.font = "600 9px 'IBM Plex Mono',monospace";
      w = Math.max(w, ctx.measureText(String(b.id).toUpperCase().slice(0, 20)).width);
      ctx.font = "400 9px 'IBM Plex Mono',monospace";
      w = Math.max(w, ctx.measureText(b.n + (b.n === 1 ? ' node' : ' nodes')
                 + ' \u00b7 mean C ' + b.meanC).width);
    }
    ctx.restore();
    GUT_W = Math.ceil(w);
    return GUT_W;
  }
  function measureGutter(){
    const tab = document.querySelector('.rail-fold');
    let over = 0;
    if (tab){
      const r = tab.getBoundingClientRect();
      const hb = host.getBoundingClientRect();
      /* Only what actually laps ONTO the map. A folded rail, a tab that has been
         removed, or a tab that sits clear all give 0 and the label stays at 10. */
      if (r.width > 0 && r.height > 0) over = Math.ceil(r.right - hb.left);
    }
    const room = PAD.l - gutterTextWidth() - 4;   /* what the gutter can spare */
    PAD.gl = Math.max(10, Math.min(over + 6, Math.max(10, room)));
  }

  /* The DOM overlays that sit on the map need the same reserve the canvas uses,
     and CSS cannot read PAD. Publishing it is what stops the next overlay being
     pinned to a fresh guess. .l0ledger already clamps to PAD.t + 6 in script and
     is why it was never the one printing on the chrome. */
  function publishHead(){
    host.style.setProperty('--l0-ctl', PAD.ctl + 'px');
    host.style.setProperty('--l0-pad-t', PAD.t + 'px');
  }
  const REST = new Set(PK.rest || []);
  const FLAG = new Set(PK.flags || []);
  /* PK.flags is already rank-ordered by merge_packed, so rank is position + 1. */
  const FLAGRANK = {};
  (PK.flags || []).forEach((id, i) => { FLAGRANK[id] = i + 1; });
  const FLAGSET = PK.flags || [];
  /* The reasons. Design: "A pointer without its reason is the thing this board
     exists not to do." All fourteen are authored in data/l0-highlights.json and
     until now reached the analyst's "where do I start" branch and nothing else. */
  const FLAGWHY = {};
  for (const f of ((D.highlights || {}).flags || [])) FLAGWHY[f.id] = f.why || '';
  const opt = Object.assign({}, L0_OPT);
  /* ALL MOTION STOPS DEAD under prefers-reduced-motion. Read once and treated as
     a hard override: the attention control cannot turn it back on, because a
     reader who has asked the operating system for no motion has not asked this
     board for an exception. */
  const REDUCED = !!(window.matchMedia
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  let attn = REDUCED ? 'still' : 'breath';
  let loop = null, tStart = 0;
  /* Motion runs for the breath OR for a selection. The selection case is not an
     assertion about the record -- it is the reader's own act, showing which end of
     each edge they are standing on -- so it does not need an attested direction
     the way a denial does. */
  /* Counted once. A directed denial animates whether or not anything is selected
     and whether or not BREATH is on, because its direction is a property of the
     record rather than of the reader -- so the loop has to stay alive for it. 38
     of them on the current data. */
  const DIRECTED_DENIALS = (D.directEdges || []).filter(e =>
       (e.types || []).indexOf('denial') >= 0
    && e.denialKind !== 'association'
    && (e.denier === e.a || e.denier === e.b)).length;
  const animating = () => !REDUCED && (
       (attn !== 'still' && FLAGSET.length > 0 && opt.flags)
    || S.l0open.length > 0
    || DIRECTED_DENIALS > 0);
  function stopLoop(){ if (loop) { cancelAnimationFrame(loop); loop = null; } }
  function startLoop(){
    if (loop || !animating()) return;
    tStart = 0;
    const step = ts => {
      loop = null;
      if (dead || !animating()) return;
      if (!tStart) tStart = ts;
      animT = ts - tStart;
      draw();
      /* ONCE runs a single pass and then leaves the flags at rest, which is the
         whole difference between it and BREATH. */
      if (attn === 'once' && !S.l0open.length && !DIRECTED_DENIALS
          && animT > 1400 + 14*130) return;
      loop = requestAnimationFrame(step);
    };
    loop = requestAnimationFrame(step);
  }
  let animT = 0;
  let lit0 = new Set();
  const ekey = (e, s) => e.a + '|' + e.b + '|' + (s ? 'shared' : 'direct');
  const cvs = document.createElement('canvas');
  host.appendChild(cvs);
  const ctx = cvs.getContext('2d');

  let W=0, H=0, dpr=1, raf=null, dead=false;
  const view = { k:1, ox:0, oy:0 };
  let hover=null, drag=null, moved=false;

  function measure(){
    const b = host.getBoundingClientRect();
    W = Math.max(320, b.width); H = Math.max(240, b.height);
    dpr = Math.min(window.devicePixelRatio||1, 2);
    cvs.width = W*dpr; cvs.height = H*dpr;
    ctx.setTransform(dpr,0,0,dpr,0,0);
  }
  /* SPEC 7, re-derived for the packed grid. The point cloud had to guess its own
     extent from node positions plus constants for label width and the label line.
     A grid knows its extent: the model states worldW and worldH, and the chip is
     inside it. So the two constants are gone rather than merely unused -- on a grid
     they were wrong, not redundant. */
  /* Which zoom the reader is in, so the fit buttons can show it. Cleared to null
     by any manual pan or wheel: once the camera has been moved by hand, neither
     button describes where you are, and lighting one up would be a claim the
     board cannot support. */
  let zoom = 'fit';
  /* AUTO until the reader's first gesture, then HELD. Design: "never move the
     camera under a hand that is already moving it". While AUTO, every change to
     the box -- a resize, the dossier opening, the rail folding -- re-fits. That
     was the real defect behind "the map is never able to fit": the ResizeObserver
     called measure() and clampView() and never re-fitted, so opening the dossier
     narrowed the map and left the camera exactly where it was, now showing less
     of the board than a moment earlier. */
  let camMode = 'auto';
  /* The node the camera is holding, if any. Set by focus(), cleared by a
     drag, a wheel or a cleared selection -- the three ways a reader says
     they are done looking at that node. */
  let focusId = null;
  function hold(){ camMode = 'held'; focusId = null; }

  /* Design asks for two fit buttons, each printing the scale it would produce, so
     the cost of an open dossier is a number on screen rather than a feeling.
     Their study overlays the panels on a full-width canvas, so their pair is "fit
     what is left" against "fit everything and let the panels cover the overlap".

     THIS BOARD IS BUILT DIFFERENTLY and the pair has to be re-derived rather than
     copied. The shell is `grid-template-columns: var(--rail-w) minmax(0,1fr)
     var(--dock-w)`, so the panels are grid COLUMNS: they take the map's width
     rather than covering it. There is no overlap here to fit under. Copying the
     labels would have shipped a FIT ALL that did the same thing as FIT ROOM and
     printed a second identical number for ever.

     Same information, honest for this layout: FIT fits the room there is, FIT ALL
     folds the panels away and fits the width that frees. The difference between
     the two numbers is still exactly the price of what is open. */
  function panelPx(){
    const cs = getComputedStyle(document.documentElement);
    const n = v => parseFloat(cs.getPropertyValue(v)) || 0;
    const app = document.getElementById('app');
    const railOff = !!(app && app.classList.contains('rail-off'));
    const dock = document.getElementById('dock');
    const dockW = dock ? dock.getBoundingClientRect().width : n('--dock-w');
    return { rail: railOff ? 0 : n('--rail-w'), dock: dockW };
  }
  /* The scale a given content width would produce. fitScale() is this at the
     width the map actually has. */
  function scaleFor(w, h){
    return Math.min((w - PAD.l - 16) / (PK.worldW - PAD.l),
                    (h - PAD.t - 16) / (PK.worldH - PAD.t));
  }
  function roomScale(){ return scaleFor(W, H); }
  function allScale(){
    const p = panelPx();
    /* Folding leaves a labelled spine, not nothing -- a panel that vanishes
       cannot be got back. */
    const SPINE = 30;
    const freed = Math.max(0, p.dock - SPINE) + Math.max(0, p.rail - SPINE);
    return scaleFor(W + freed, H);
  }
  function fitScale(){
    /* Fit the CELLS into the space left after the chrome, not the whole world
       into the whole canvas. Fitting the world would scale the reserved strips
       down along with everything else and then reserve them again at full size
       on top, which loses a chip row at every viewport size. */
    return Math.min((W - PAD.l - 16) / (PK.worldW - PAD.l),
                    (H - PAD.t - 16) / (PK.worldH - PAD.t));
  }
  /* Pan is clamped so the cells always fill the content rect: no scrolling the
     map away into blank world, and no cell ever hiding under the frozen chrome.
     Called from every place the camera moves -- drag, wheel, fit, focus, resize.
     Miss one and the map opens correctly and then drifts, which is worse than
     never clamping at all because it only shows up after an interaction. */
  function clampView(){
    const k = view.k;
    const cw = W - PAD.l, ch = H - PAD.t;              /* content rect */
    const ww = (PK.worldW - PAD.l) * k, wh = (PK.worldH - PAD.t) * k;
    const maxOx = PAD.l - PAD.l * k, maxOy = PAD.t - PAD.t * k;
    view.ox = ww <= cw ? maxOx : Math.min(maxOx, Math.max(W - PK.worldW * k, view.ox));
    view.oy = wh <= ch ? maxOy : Math.min(maxOy, Math.max(H - PK.worldH * k, view.oy));
  }
  function centreOn(k){
    view.k = k;
    view.ox = W/2 - (PK.worldW/2)*k; view.oy = H/2 - (PK.worldH/2)*k;
    clampView();
  }
  /* A grid does not want to open on its middle. The bands are ordered by measured
     mean custody proximity, descending, and THAT ORDER IS THE ARGUMENT -- so when
     the whole world does not fit, the map opens on the top-left corner where the
     argument starts, with the gutter and the column heads in view. */
  function cornerOn(k){
    view.k = k; view.ox = 0; view.oy = 0; clampView();
  }
  const SX = x => x*view.k + view.ox, SY = y => y*view.k + view.oy;
  /* Chip centre. Model positions are TOP-LEFT; edges, ledgers and focus all want
     the middle, and mixing the two is the whole bug class this comment prevents. */
  const CX = n => SX(n.x + n.w/2), CY = n => SY(n.y + n.h/2);

  /* ---- chips ---------------------------------------------------------- */
  /* ONE chip size for every node, 205 x 20, straight from the model. This is the
     load-bearing rule of the whole layout and the reason position can mean
     something: with size neutralised, the only things left saying anything are
     which column a node is in (era) and which row (band). Class keeps a channel --
     a 3px rule down the left edge, the same device the document mark used along
     its top -- because dropping it would lose information the board deliberately
     added, and a hue stripe is not a size. */
  function chip(n, on, lit){
    const x = SX(n.x), y = SY(n.y), w = n.w*view.k, h = n.h*view.k;
    ctx.fillStyle = L0_PACK.chipFill;
    ctx.fillRect(x, y, w, h);
    ctx.lineWidth = 1;
    ctx.strokeStyle = on ? '#5ed4e6'
                    : (FLAG.has(n.id) && opt.flags) ? L0_PACK.chipLineFlag
                    : n.tier === 'A' ? L0_PACK.chipLineA : L0_PACK.chipLine;
    ctx.strokeRect(x+0.5, y+0.5, w-1, h-1);
    ctx.fillStyle = (L0_CLS[n.cls]||L0_CLS.person).c;   /* class rule, left edge */
    ctx.fillRect(x, y, Math.max(1, 3*view.k), h);
    if (opt.labels && view.k >= L0_LABEL_DROP){
      /* Design's chip is [rule][image|glyph 11px][label][rank][mark], gaps of 5.
         Everything to the right of the label is reserved BEFORE the label is fitted,
         which is the bug the cross found: room used to be w-12 regardless of what
         else was going to be drawn inside the same chip, so the mark landed on top
         of the label and took its ellipsis with it. */
      const gap = 5*view.k;
      const rank = (opt.flags && FLAGRANK[n.id]) ? String(FLAGRANK[n.id]) : '';
      let right = 5*view.k;                                  /* padding-right */
      if (n.iso)  right += 8*view.k + gap;                   /* the absent-link mark */
      if (rank)   right += 8*view.k + gap;                   /* the start-here rank */
      const glyphW = 11*view.k;
      const lx = x + 7*view.k;                               /* content starts here */
      /* The class letter. An image will take this slot when data/l0-images.json is
         populated; the letter is the fallback and says what the node IS rather than
         implying a face nobody found. */
      const tile = n.photo ? l0Img(n.photo, () => { if (!dead) paintMap(); }) : null;
      if (tile){
        l0DrawTile(ctx, tile, n, lx, y + (h-glyphW)/2, glyphW);
      } else {
        ctx.font = "400 " + (8*view.k).toFixed(2) + "px 'IBM Plex Mono',monospace";
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillStyle = on ? L0_PACK.ink2 : L0_PACK.glyph;
        ctx.fillText(L0_GLYPH[n.cls] || '\u00b7', lx + glyphW/2, y + h/2 + 0.5);
      }

      ctx.font = "400 " + (9.5*view.k).toFixed(2) + "px 'IBM Plex Mono',monospace";
      ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
      const tx = lx + glyphW + gap;
      const room = (x + w - right) - tx;
      ctx.fillStyle = on ? L0_PACK.ink : (n.tier === 'A' ? L0_PACK.ink : L0_PACK.ink2);
      ctx.fillText(l0Fit(ctx, n.short || n.label || n.id, room), tx, y + h/2 + 0.5);

      /* The rank numeral, amber, right-aligned before the mark. Design: the set has
         to be enumerable, and the legend carries the reason for each. */
      if (rank){
        ctx.font = "400 " + (8*view.k).toFixed(2) + "px 'IBM Plex Mono',monospace";
        ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
        ctx.fillStyle = L0_PACK.pointer;
        ctx.fillText(rank, x + w - (n.iso ? 13*view.k + gap : 5*view.k), y + h/2 + 0.5);
      }
    }
    /* Absent prints as absent. Three nodes clear the connectivity floor on the
       full board and still have no link to any other node ON THE MAP, which is a
       finding about the map's own threshold rather than about them. */
    if (n.iso){
      const cx = x + w - 9*view.k, cy = y + h/2, r = 3.5*view.k;
      ctx.strokeStyle = L0_PACK.iso; ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(cx-r, cy-r); ctx.lineTo(cx+r, cy+r);
      ctx.moveTo(cx-r, cy+r); ctx.lineTo(cx+r, cy-r);
      ctx.stroke();
    }
  }
  /* One occupancy cell. Type here is sized in WORLD units but must be judged in
     RENDERED ones, which is the distinction that makes a "roomy" test against world
     height admit a sub-label that renders at 4px. Both the floor and the fit are
     computed through the scale: 9px rendered is the floor, and the annotation is
     dropped whenever the cell cannot hold the numeral plus 9px of it. The count is
     the statement; the annotation is not.

     `floor` is a LOWER bound and nothing else. Passing it through Math.min would
     make it a ceiling, which pins every numeral to 9px and leaves a tall cell
     rendering its digit at the floor. The numeral is sized from the CELL and only
     lifted to the floor when the cell is too short to reach it. */
  function cell(b, c, ids){
    const n = ids.length;
    if (!n) return;
    const x = SX(c.x + 10), y = SY(b.y + 10);
    const w = (c.w - 20)*view.k, h = (b.h - 20)*view.k;
    if (x + w < PAD.l || x > W || y + h < PAD.t || y > H) return;
    const flg = opt.flags ? ids.filter(id => FLAG.has(id)).length : 0;
    /* THE SELECTION SURVIVES CELL MODE. Below the label threshold there are no
       chips, so a fit used to lose the selected node outright: the reader picks a
       node, the map re-fits, and the thing they picked is simply not on screen any
       more. The cell it lives in now says "your node is in here, with N others".

       Design asked for the amber outline and an amber numeral. AMBER IS ALREADY
       TAKEN in this view -- it is the start-here flag, and a flagged cell already
       draws exactly that outline and numeral. Reusing it would have made a
       selected cell and a flagged cell indistinguishable, which is worse than not
       marking the selection at all: it would put a false start-here pointer on the
       board, and pointers here are editorial claims.
       So the selection uses #5ed4e6, which is what selection means everywhere else
       on this board -- the chip stroke, the crumb count, the lit controls. Same
       treatment as Design specified, in the colour this board already reserves for
       it, and it composes with the flag rather than overwriting it. */
    const selHere = S.sel && ids.indexOf(S.sel) >= 0;
    ctx.fillStyle   = selHere ? 'rgba(94,212,230,0.08)'
                    : flg ? 'rgba(239,181,85,0.06)' : L0_PACK.chipFill;
    ctx.strokeStyle = selHere ? '#5ed4e6'
                    : flg ? L0_PACK.pointer : L0_PACK.chipLine;
    ctx.lineWidth = selHere ? 2 : 1;
    ctx.fillRect(x, y, w, h);
    ctx.strokeRect(x+0.5, y+0.5, w-1, h-1);
    /* Rendered sizes throughout. The cell bound divides by the font's box ratio
       rather than subtracting a constant: an IBM Plex Mono glyph box runs about 15%
       past its line box, so a 22px numeral needs 25px of room. */
    const ch = h, floor = 9;
    const fs = Math.min((ch - 4)/1.2, Math.max(floor, Math.min(44, ch*0.45)));
    const roomy = fs >= floor*1.6 && fs + floor + 6 <= ch;
    /* The sub-line names the selection when there is one, and falls back to the
       flag count. "1 of these is open" is the sentence the reader needs; the flag
       count is still on the outline colour when the cell is also flagged. */
    const sub = roomy ? (selHere ? 'selection in here'
                       : flg ? flg + ' flagged' : '') : '';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const cy = y + h/2 - (sub ? (floor + 3)/2 : 0);
    ctx.font = "400 " + fs.toFixed(1) + "px 'IBM Plex Mono',monospace";
    ctx.fillStyle = selHere ? '#5ed4e6' : flg ? L0_PACK.pointer : L0_PACK.bandLabel;
    ctx.fillText(String(n), x + w/2, cy);
    if (sub){
      ctx.font = "400 " + floor + "px 'IBM Plex Mono',monospace";
      ctx.fillStyle = L0_PACK.colNote;
      ctx.fillText(sub, x + w/2, cy + fs/2 + 3 + floor/2);
    }
  }
  /* The start-here layer, drawn as an OFFSET pointer beside the chip and never as
     a property of it. That separation is the point: it can never be mistaken for a
     tier, and AARO cannot be promoted by being pointed at. */
  function pointer(n){
    const x = SX(n.x) - 4*view.k, y = CY(n);
    ctx.strokeStyle = L0_PACK.pointer; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(x - 9*view.k, y); ctx.lineTo(x, y); ctx.stroke();
    ctx.fillStyle = L0_PACK.pointer;
    ctx.beginPath(); ctx.arc(x - 11.5*view.k, y, Math.max(1.2, 2.2*view.k), 0, Math.PI*2);
    ctx.fill();
  }
  /* Band rows and era columns. Both are labelled, because in this layout the rows
     and columns ARE the claim -- an unlabelled grid is just a nicer hairball.
     DIVERGENCE from the comp, which is a single static full-view: here the labels
     are PINNED to the viewport edges rather than drawn at world x=10 / y=18, so
     they stay readable at any pan. geo.gutter (148) and geo.headRow (46) reserve
     exactly that space in the model, which is what makes pinning safe. */
  /* DENSE MODE. Below the label threshold a 9.5px chip label renders under 6px and
     the map was drawing 110 anonymous rectangles: no identity, AND they hid the one
     thing still legible at that size, which is how many nodes sit in each cell. So
     the chips collapse and every cell prints its COUNT -- the occupancy matrix, in
     place, at the size where it is the only honest statement.

     DENSE ROWS ARE EQUAL HEIGHT, and that is the fix rather than a workaround. A
     band's height is derived from how many chip rows its busiest cell needs, which
     is meaningful when chips render and meaningless when they do not: it left the
     single-row disclosure band 9px tall on screen. Dividing the same world height
     equally keeps the scale and the band order identical and removes an accidental
     channel.

     The start-here wash is deliberately NOT reused for this. It means "an editor
     pointed here", and a channel that also meant "too small to label" would stop
     meaning either. */
  /* Cell mode is a STATE, not a scale. L0_LABEL_DROP still governs labels at line
     ~628 and nothing else; the two jobs it used to share are now separate. */
  const dense = () => !!opt.cells;
  /* ONE row set per camera state, consumed by everything that draws a row: the
     stripes, the gutter labels and the count cells. Design hit the alternative and
     named it -- deriving the equal-height rows for some consumers and leaving the
     others on the model's chip-derived bands puts two contradictory geometries on
     the same canvas, and the visible symptom is fringes half a row above their
     cells. Memoised on view.k so a frame cannot disagree with itself. */
  let _rows = null, _rowsAt = NaN, _rowsCells = null;
  function bandRows(){
    /* Keyed on the mode as well as the camera. dense() used to BE a function of
       view.k, so view.k alone was a complete key; it is not any more, and a CELLS
       toggle at an unchanged zoom would otherwise hand back the other mode's
       geometry -- the "two contradictory geometries on one canvas" this memo was
       written to prevent, arriving through the memo itself. */
    if (_rows && _rowsAt === view.k && _rowsCells === dense()) return _rows;
    const bs = PK.bands || [];
    _rowsAt = view.k; _rowsCells = dense();
    if (!dense() || !bs.length) return (_rows = bs);
    const rowH = (PK.worldH - PAD.t - 10) / bs.length;
    return (_rows = bs.map((b, i) => ({ ...b, y: PAD.t + i*rowH, h: rowH })));
  }
  function bands(){
    bandRows().forEach((b, i) => {
      const y = SY(b.y), h = b.h*view.k;
      if (y > H || y + h < 0) return;
      ctx.fillStyle = i % 2 ? L0_PACK.bandAlt : L0_PACK.bandFill;
      /* Full width including the gutter, so the row striping runs behind its own
         label and a reader can see which row a label belongs to. */
      ctx.fillRect(0, y, W, h);
    });
  }
  function bandLabels(){
    ctx.save();
    ctx.beginPath(); ctx.rect(0, PAD.t, PAD.l, H - PAD.t); ctx.clip();
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    /* AXIS TYPE IS NEVER SCALED. These are already drawn at an authored px size and
       positioned at world x scale, which is what "outside the world transform"
       means on a canvas. Counter-scaling by 1/k would be the wrong fix: it inflates
       type against the 148px gutter and the band heights, which stay at model
       dimensions computed for authored type, so it overflows and collides with the
       row below. In dense mode the meta line is DROPPED rather than shrunk -- the
       count it carried is printed inside every cell now, so repeating it in the
       gutter buys nothing and costs the only vertical room a short row has. */
    const dn = dense();
    bandRows().forEach(b => {
      const y = SY(b.y), h = b.h*view.k;
      if (y > H || y + h < PAD.t) return;
      const ty = Math.max(y, PAD.t);      /* a row scrolled half off still names itself */
      /* Design's answer to the disclosure-band question Stewart was holding: keep
         the band, do not merge it and do not pad it, but MAKE THINNESS LEGIBLE.
         Every band prints its count, and under five it prints amber. "DISCLOSURE ·
         3 nodes" in amber is an argument -- the board saying the record is thin
         there. "DISCLOSURE" alone beside a nearly empty row is just a layout that
         looks broken, which is exactly how it read on screen.

         The count goes on the SECOND line, not appended to the name: Design's own
         example runs the two together, but "REVERSE-ENGINEERING · 15 nodes" is
         about 162px of 9px mono and the gutter holds 138. Appending it would have
         truncated the longest band names to make room for a number.

         And the second line now draws in dense mode too. It used to be suppressed
         there to save vertical room -- which meant the occupancy view, the one that
         exists to show the shape of the board, was the one view that would not say
         a band was nearly empty. */
      const thin = b.n < 5;
      ctx.font = "600 9px 'IBM Plex Mono',monospace";
      ctx.fillStyle = thin ? L0_PACK.pointer : L0_PACK.bandLabel;
      ctx.fillText(String(b.id).toUpperCase().slice(0, 20), PAD.gl, ty + 13);
      ctx.font = "400 9px 'IBM Plex Mono',monospace";
      ctx.fillStyle = thin ? L0_PACK.pointer : L0_PACK.bandN;
      ctx.fillText(b.n + (b.n === 1 ? ' node' : ' nodes')
                 + (dn ? '' : ' \u00b7 mean C ' + b.meanC), PAD.gl, ty + 25);
    });
    ctx.restore();
  }
  function columns(){
    ctx.strokeStyle = L0_PACK.colRule; ctx.lineWidth = 1;
    (PK.eras||[]).forEach(c => {
      if (!(c.x > 0)) return;
      const x = SX(c.x) - 5;
      if (x < 0 || x > W) return;
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    });
  }
  function columnHeads(){
    ctx.save();
    ctx.beginPath(); ctx.rect(0, 0, W, PAD.t); ctx.clip();
    ctx.fillStyle = '#11141a';                       /* the strip is chrome, opaque */
    ctx.fillRect(0, 0, W, PAD.t);
    ctx.strokeStyle = L0_PACK.colRule; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(0, PAD.t - 0.5); ctx.lineTo(W, PAD.t - 0.5); ctx.stroke();
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    const eras = PK.eras || [];
    eras.forEach((c, i) => {
      const x = SX(c.x);
      if (x > W || x + c.w*view.k < PAD.l) return;
      const cx = Math.max(PAD.l, Math.min(W - 150, x));
      /* BUDGET THE HEAD TO THE ROOM THAT EXISTS. The head is drawn at an authored
         px size and never scaled, which is right, but the COLUMN shrinks with the
         world: at 0.23x the columns are ~200px apart on screen while the head text
         still wants its full width, so "Estimate through Blue Book" ran straight
         into "Post-Blue Book". Budget against the smaller of this column's own
         rendered width and the gap to where the next head will actually be drawn,
         so two heads can never overlap however far the map is zoomed out. */
      const nx = i + 1 < eras.length
        ? Math.max(PAD.l, Math.min(W - 150, SX(eras[i+1].x)))
        : W;
      const budget = Math.max(28, Math.min(c.w*view.k, nx - cx) - 10);
      /* Baselines measured DOWN from the top of the era band, which starts where
         the control row ends. PAD.t - ERA_BAND is >= PAD.ctl by construction (see
         measureHead), so this cannot print on the controls however the row wraps.
         The old form counted UP from PAD.t by two hard-coded offsets, which is how
         the reserve and the baselines came to disagree. */
      const eraTop = PAD.t - ERA_BAND;
      ctx.font = "600 9px 'IBM Plex Mono',monospace";
      ctx.fillStyle = L0_PACK.colHead;
      ctx.fillText(l0Fit(ctx, c.label, budget), cx, eraTop + 13);
      if (c.note){
        ctx.font = "400 8.5px 'IBM Plex Mono',monospace";
        ctx.fillStyle = L0_PACK.colNote;
        ctx.fillText(l0Fit(ctx, c.note, budget), cx, eraTop + 26);
      }
    });
    ctx.restore();
  }

  /* ---- traces --------------------------------------------------------- */
  /* Right-angled with one mitred corner, long axis first. Ticks at the corner,
     one per underlying link (direct) or shared member (summarised). The counts
     top out at 5 on this data, so the five-tick vocabulary never overflows and
     there is no numeral case to design. */
  function trace(e, summarised){
    const a = byId[e.a], b = byId[e.b];
    if (!a || !b) return;
    const x1=CX(a), y1=CY(a), x2=CX(b), y2=CY(b);
    const t = L0_TIER[e.tier] || L0_TIER[3];
    const w = e.n || 1;
    /* MULTIPLY by the caller's alpha, do not overwrite it. The caller sets the
       focus dim before calling; setting globalAlpha outright here clobbered it,
       so nodes dimmed and the edge lattice stayed at full brightness — which is
       most of the ink, so the dim looked like it had barely worked. */
    const base = ctx.globalAlpha;
    ctx.globalAlpha = base * Math.min(0.92, 0.30 + (w-1)*0.15);
    ctx.strokeStyle = t.c;
    ctx.lineWidth = summarised ? 1 : 2;
    ctx.setLineDash(t.d);
    const horizFirst = Math.abs(x2-x1) >= Math.abs(y2-y1);
    const cx = horizFirst ? x2 : x1, cy = horizFirst ? y1 : y2;
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(cx,cy); ctx.lineTo(x2,y2); ctx.stroke();
    ctx.setLineDash([]);
    /* Ticks, with an overflow numeral. DIVERGENCE D6.

       The design package asserted that shared-member counts run 2-5, "so the
       parent board's five-weight tick vocabulary fits exactly, with no overflow
       and no numeral case". That was true of the graph as it stood. Wiring the
       DIRDs to their authors and to AAWSAP densified it, and dia~dird-series now
       shares 18 members. The claim is no longer true, and it was MY change that
       broke it.

       Five ticks cannot carry 18, and drawing five for both 5 and 18 would be a
       channel that silently saturates -- the reader would have no way to tell the
       difference. So beyond five the marks give way to a numeral. This is the
       numeral case the design said did not exist; it exists now. */
    const TICK_MAX = 5;
    ctx.fillStyle = t.c;
    if (w <= TICK_MAX){
      for (let i=0;i<w;i++){
        const off = (i - (w-1)/2) * 3.6;
        ctx.fillRect(cx + (horizFirst?off:-1.1), cy + (horizFirst?-1.1:off), 2.2, 2.2);
      }
    } else {
      ctx.font = "500 9px 'IBM Plex Mono',monospace";
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      const label = String(w);
      const tw = ctx.measureText(label).width;
      ctx.fillStyle = 'rgba(15,18,22,0.88)';
      ctx.fillRect(cx - tw/2 - 2, cy - 6, tw + 4, 12);
      ctx.fillStyle = t.c;
      ctx.fillText(label, cx, cy);
    }
    /* D3, and Design's correction to it: a denial has THREE states because the data
       has three, not one.

         directed     issuer named        arrowhead (and, later, a particle)
         undirected   an act, no issuer   a perpendicular BAR at the midpoint
         association  not a directed act  no denial styling at all

       The head used to draw on every denial edge, pointing at `e.b`, where a/b is
       [a,b].sort() in the generator. Alphabetical order rendered as attribution: it
       disagreed with the board's own records on 22 of 47, and the records carry no
       consistent issuer-first convention either. Switching the channel off entirely
       was the safe move and it overpaid, because it lost the ones that ARE attested
       and made a denial indistinguishable from an ordinary link. A bar is not a
       vector. It reads as contested, which is exactly what the record supports.

       Degrades to `undirected` when neither `denier` nor `denialKind` is present,
       because that claims the least. */
    const isDenial = !summarised && (e.types||[]).indexOf('denial') >= 0
                     && e.denialKind !== 'association';
    const dnr = e.denier;
    if (isDenial && !(dnr === e.a || dnr === e.b)){
      /* Undirected: a bar across the line at its midpoint, square to it. */
      const bx = (x1 + x2)/2, by = (y1 + y2)/2;
      const ang = Math.atan2(y2 - y1, x2 - x1) + Math.PI/2;
      const r = 4.5*view.k;
      /* Red is reserved for something somebody did, so the bar takes it and an
         `association` never reaches here. The line itself stays tier-coloured. */
      ctx.strokeStyle = L0_PACK.denial;
      ctx.lineWidth = 1.6;
      ctx.setLineDash([]);
      ctx.beginPath();
      ctx.moveTo(bx - Math.cos(ang)*r, by - Math.sin(ang)*r);
      ctx.lineTo(bx + Math.cos(ang)*r, by + Math.sin(ang)*r);
      ctx.stroke();
    }
    if (isDenial && dnr && (dnr === e.a || dnr === e.b)){
      const tx = dnr === e.a ? x2 : x1, ty = dnr === e.a ? y2 : y1;
      const fx = dnr === e.a ? cx : x2, fy = dnr === e.a ? cy : y2;
      const ang = Math.atan2(ty-fy, tx-fx);
      const hx = tx - Math.cos(ang)*10, hy = ty - Math.sin(ang)*10;
      ctx.fillStyle = L0_PACK.denial;
      ctx.beginPath();
      ctx.moveTo(tx - Math.cos(ang)*11*view.k, ty - Math.sin(ang)*11*view.k);
      ctx.lineTo(hx - Math.sin(ang)*3.2, hy + Math.cos(ang)*3.2);
      ctx.lineTo(hx + Math.sin(ang)*3.2, hy - Math.cos(ang)*3.2);
      ctx.closePath(); ctx.fill();
    }
    /* THE PARTICLE LAYER. Design: if something moves, the direction is attested.
       Two cases qualify and no others. A directed denial, where the record names
       the issuer -- none yet, so none draw. And an edge of the SELECTED node,
       running outward from the node the reader is standing on, which asserts
       nothing about the record because the reader chose the end.

       A time-direction flow on every line is the treatment Design rejected, and
       the inherited parent-board renderer still carries it: it flips by comparing
       node dates, which states that the relationship runs from the earlier node to
       the later one. For most of these edges the board makes no such claim. */
    /* THE SECOND QUALIFYING CASE, 27 August 2026. The comment above says a
       directed denial qualifies and then says "none yet, so none draw". That was
       true when it was written and stopped being true the same week: the
       adjudication landed 174 verdicts and 38 directed denials now reach the page
       with a `denier` matching one end. The arrowhead drew for them from the
       start; the particle never did, so Design's "arrowhead + travelling
       particle" shipped as half a treatment and the moving half was the half that
       carries the direction.

       Stewart, 27 August: "we STILL have not implemented the color and particle
       system for the lines showing which way the connection goes."

       Direction: from the DENIER toward the subject, which is the claim the
       adjudication actually makes. A selection still wins where both apply,
       because the reader's own end is the stronger reference and asserts nothing
       about the record. Colour separates them: the denial runs in the denial red
       already used for its arrowhead, the selection thread in the map's cyan, so
       the two motions never read as one channel. */
    const dirDenial = isDenial && (dnr === e.a || dnr === e.b);
    const selA = S.l0open.indexOf(e.a) >= 0;
    const selB = S.l0open.indexOf(e.b) >= 0;
    const selTouch = S.l0open.length > 0 && (lit0.has(e.a) || lit0.has(e.b));
    if (!REDUCED && ((selTouch && (selA || selB)) || dirDenial)){
      {
        const P = [[x1,y1],[cx,cy],[x2,y2]];
        const segs = [Math.hypot(cx-x1, cy-y1), Math.hypot(x2-cx, y2-cy)];
        const len = segs[0] + segs[1];
        if (len > 6){
          const vel = 74 * view.k;                  /* px per second, Design's default */
          const dur = Math.max(1600, len / Math.max(1, vel) * 1000);
          /* Deterministic per-edge phase, so nothing about a line depends on draw
             order and two runs of the same frame look identical. */
          let hsh = 0;
          const kstr = e.a + '|' + e.b;
          for (let i = 0; i < kstr.length; i++) hsh = (hsh*31 + kstr.charCodeAt(i)) >>> 0;
          let u = ((animT + (hsh % 100)/100 * dur) % dur) / dur;
          /* Outward from the reader's end when they picked one, otherwise from the
             denier. `fromA` is which end the dot leaves, and it is the only place
             this layer makes a claim. */
          const onSel = selA || selB;
          const fromA = onSel ? selA : (dnr === e.a);
          if (!fromA) u = 1 - u;
          const d = u * len;
          const i2 = d <= segs[0] ? 0 : 1;
          const t2 = i2 === 0 ? (segs[0] ? d/segs[0] : 0)
                              : (segs[1] ? (d - segs[0])/segs[1] : 0);
          const px0 = P[i2][0] + (P[i2+1][0] - P[i2][0]) * t2;
          const py0 = P[i2][1] + (P[i2+1][1] - P[i2][1]) * t2;
          ctx.globalAlpha = base * 0.75;
          ctx.fillStyle = (!onSel && dirDenial) ? L0_PACK.denial
                        : summarised ? '#a795e8' : '#5ed4e6';
          ctx.beginPath();
          ctx.arc(px0, py0, Math.max(1.1, 1.6*view.k), 0, Math.PI*2);
          ctx.fill();
        }
      }
    }
    ctx.globalAlpha = base;
  }

  function draw(){
    raf = null;
    if (dead) return;
    ctx.clearRect(0,0,W,H);
    ctx.save();
    ctx.beginPath(); ctx.rect(PAD.l, PAD.t, W - PAD.l, H - PAD.t); ctx.clip();
    bands();
    columns();

    /* THE START-HERE WASH. A fit-width device only: in dense mode the flagged cell
       already carries its own amber background at exactly the right position, so a
       second mark would be a duplicate, and routing it through a second band
       geometry is what put fringes half a row above their cells in Design's own
       comp. Deduped by cell, because two flags in one cell is one region. */
    /* THE OFFER IS WITHDRAWN ONCE IT IS TAKEN. The start-here layer exists to
       draw a first-time eye to somewhere worth starting; BREATH pulses it to do
       that. It kept pulsing after the reader had chosen, so a selected node's
       thread had to be read through fourteen amber cells fading in and out
       behind it. Stewart, 27 August: "the entire map and yellow part is fading
       in and out of the background rendering it illegible."

       Held at zero while a selection or an entry path is active, so the only
       thing moving is the selection's own particle layer -- which is the one
       motion Design licenses, because the reader chose the end it runs from. */
    const chosen = !!(S.sel || S.l0open.length || S.l0path);
    const bAlpha = attn === 'still' || REDUCED || chosen ? 0
                 : attn === 'once' ? Math.min(1, animT / 1100)
                 : l0Breath(animT);
    if (opt.flags && !dense() && bAlpha > 0.01){
      const rows = bandRows(), seen = {};
      for (const id of FLAGSET){
        const n = byId[id];
        if (!n) continue;
        const key = n.band + '|' + n.col;
        if (seen[key]) continue;
        seen[key] = 1;
        const b = rows.find(r => r.id === n.band);
        const c = (PK.eras||[]).find(e => String(e.id) === String(n.col));
        if (!b || !c) continue;
        const x = SX(c.x), y = SY(b.y), w = c.w*view.k, h = b.h*view.k;
        ctx.globalAlpha = bAlpha;
        ctx.fillStyle = 'rgba(239,181,85,0.045)';
        ctx.fillRect(x, y, w, h);
        ctx.strokeStyle = 'rgba(239,181,85,0.14)';
        ctx.lineWidth = 1;
        ctx.strokeRect(x+0.5, y+0.5, w-1, h-1);
        ctx.globalAlpha = 1;
      }
    }

    const dim = S.l0open.length ? 0.16 : 1;
    const lit = new Set(S.l0open);
    lit0 = lit;
    for (const id of S.l0open){
      const n = byId[id];
      if (n) for (const m of n.direct) lit.add(m);
    }
    const idle = !S.l0open.length && !focus;

    /* THE EDGE BUDGET. 103 of 326 draw at rest, chosen by the model's own rule
       (db>=2 && de>=1, plus one anchor per node) rather than by thinning here --
       so what a reader sees is auditable against data/l0-layout-model.json instead
       of being an artefact of the renderer. Selecting a node lifts the budget for
       that node's own edges: the budget governs the RESTING surface, and hiding an
       edge from someone who has asked for it would make the map lie. */
    /* NO EDGE LAYER BELOW THE THRESHOLD. Every line, bar and numeral chip is
       anchored to chip coordinates, so with the chips gone they terminate at
       nothing and lattice straight over the counts the mode exists to show. An
       edge pointing at an unrendered node is not a weaker version of the occupancy
       statement, it is noise on top of it. */
    const es = dense() ? []
      : D.summarised.map(e=>({e,s:true})).concat(D.directEdges.map(e=>({e,s:false})));
    es.sort((p,q)=>(p.e.n||1)-(q.e.n||1));   /* weakest first, strong claims on top */
    for (const {e,s:sm} of es){
      const touched = lit.has(e.a) || lit.has(e.b);
      const atRest = opt.rest && REST.has(ekey(e, sm));
      if (idle ? !atRest : !(touched || atRest)) continue;
      ctx.globalAlpha = (idle || touched) ? 1 : dim;
      trace(e, sm);
    }
    ctx.globalAlpha = 1;

    if (dense()){
      /* Cells, not chips. Same numbers as the occupancy table in the design note,
         printed on the map itself. */
      const rows = bandRows();
      const byCell = {};
      for (const n of D.l0){
        const k = n.band + '|' + n.col;
        (byCell[k] || (byCell[k] = [])).push(n.id);
      }
      for (const b of rows)
        for (const c of (PK.eras||[]))
          cell(b, c, byCell[b.id + '|' + c.id] || []);
    } else {
      for (const n of D.l0){
        const x = SX(n.x), y = SY(n.y);
        if (x + n.w*view.k < -20 || x > W+20 || y + n.h*view.k < -20 || y > H+20) continue;
        ctx.globalAlpha = (idle || lit.has(n.id)) ? 1 : dim;
        chip(n, hover === n.id || S.l0open.indexOf(n.id) >= 0, lit);
        if (opt.flags && FLAG.has(n.id)){
        pointer(n);
        /* The bloom rides an OUTLINE drawn outside the chip, never the chip's own
           stroke: the stroke carries entity tier, and a keyframe touching it would
           wipe that channel for most of the cycle. Two channels on one property is
           the failure Design named. */
        if (bAlpha > 0.01){
          ctx.globalAlpha = bAlpha * 0.95;
          ctx.strokeStyle = L0_PACK.pointer; ctx.lineWidth = 1;
          ctx.strokeRect(SX(n.x) - 1.5, SY(n.y) - 1.5, n.w*view.k + 3, n.h*view.k + 3);
          ctx.globalAlpha = 1;
        }
      }
        ctx.globalAlpha = 1;
      }
    }
    ctx.restore();
    /* Pinned last, so the furniture that says what the rows and columns MEAN is
       never painted over by a chip that happens to sit under it. */
    ctx.save();
    ctx.beginPath(); ctx.rect(0, PAD.t, PAD.l, H - PAD.t); ctx.clip();
    ctx.fillStyle = '#11141a';
    ctx.fillRect(0, PAD.t, PAD.l, H - PAD.t);
    ctx.strokeStyle = L0_PACK.colRule; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(PAD.l - 0.5, PAD.t); ctx.lineTo(PAD.l - 0.5, H); ctx.stroke();
    ctx.restore();
    bandLabels();
    columnHeads();
  }
  /* D2 is no longer bent, and it was the packed layout that unbent it. The point
     cloud drew each node's member class mix as a 74px hue-only bar under its label,
     which the design system forbids and which the old comment here recorded as a
     rule broken rather than met. A chip has no room under it and does not want one:
     the mix is named in words in the tooltip and grouped by class in the ledger,
     both of which carry the same information without asking hue to do it alone. */
  const paintMap = () => { if (!raf) raf = requestAnimationFrame(draw); };

  /* ---- hit test ------------------------------------------------------- */
  /* The chip IS the hit target, so this is a rect test against the drawn bounds
     rather than a radius around a point. The two must not drift: a target that is
     not the thing you can see is the class of defect where the map looks right and
     does not respond where the reader clicks. Cells are packed and never overlap,
     so first hit wins and order does not matter. */
  function at(mx, my){
    if (mx < PAD.l || my < PAD.t) return null;   /* the chrome is not the map */
    for (let i = D.l0.length-1; i >= 0; i--){
      const n = D.l0[i], x = SX(n.x), y = SY(n.y);
      if (mx >= x && mx <= x + n.w*view.k && my >= y && my <= y + n.h*view.k) return n;
    }
    return null;
  }

  /* ---- surfaces ------------------------------------------------------- */
  function renderChrome(){
    let head = host.querySelector('.l0head');
    if (!head){ head = el('div','l0head'); host.appendChild(head); }
    let c = head.querySelector('.l0crumb');
    if (!c){ c = el('div','l0crumb'); head.appendChild(c); }
    let h = '<span class="l0chip root">PROGRAM MAP</span>';
    for (const id of S.l0open){
      const n = byId[id];
      if (!n) continue;
      h += '<span class="l0chip" data-close="'+esc(id)+'">'+esc(n.short)
         + ' <span class="n">'+(n.direct.length+n.routed.length)+'</span>'
         + ' <span class="x">&times;</span></span>';
    }
    if (S.l0open.length) h += '<span class="l0chip" data-clear="1">CLEAR</span>';
    h += '<span class="l0meta">' + D.counts.l0 + ' nodes · '
       + (opt.rest ? (PK.rest||[]).length : 0) + ' of '
       + (D.counts.directEdges + D.counts.summarisedEdges) + ' links at rest · '
       + view.k.toFixed(2) + 'x</span>';
    c.innerHTML = h;

    let z = head.querySelector('.l0ctl');
    if (!z){ z = el('div','l0ctl'); head.appendChild(z); }
    /* Three options, all on by default, each with a control -- so a reader who
       wants the bare arrangement can get it and, per the "drive the whole app from
       the chat input" requirement, the analyst can operate them too (CMD.l0opt). */
    /* FIT / 1:1 as a pair, which is Design's own grouping and its own labels.
       They were OVERVIEW and 1:1 READ, and OVERVIEW read as a separate mode
       rather than as the zoom it is -- CLAUDE.md recorded a reader finding "the
       one control that shows the whole map" hard to identify. */
    /* Each fit button prints the scale it would produce. With nothing open the two
       numbers are identical, and that is the point: the difference IS the cost of
       the dossier. The state chip says whether the camera is still following the
       box or has been taken over by hand. */
    const rs = roomScale(), as = allScale();
    const x2 = v => v.toFixed(2) + '\u00d7';
    z.innerHTML = '<button class="hopb'+(zoom==='fit'?' on':'')+'" data-fit="1">'
                +   'FIT <span class="sc">'+x2(rs)+'</span></button>'
                + '<button class="hopb'+(zoom==='all'?' on':'')+'" data-fitall="1" '
                +   'title="Fold the rail and the dossier to labelled spines and fit '
                +   'the width that frees. One click restores them.">'
                +   'FIT ALL <span class="sc">'+x2(as)+'</span></button>'
                + '<button class="hopb'+(zoom==='one'?' on':'')+'" data-one="1">1:1</button>'
                + '<span class="l0cam" title="'
                +   (camMode === 'auto'
                       ? 'The map re-fits whenever the box changes -- a resize, the '
                         + 'dossier opening, the rail folding.'
                       : 'You have moved the camera, so nothing moves it under you. '
                         + 'Press a fit button to re-arm.')
                +   '">' + (camMode === 'auto' ? 'AUTO' : 'HELD') + '</span>'
                + '<button class="hopb'+(opt.rest?' on':'')+'" data-opt="rest">LINES AT REST</button>'
                + '<button class="hopb'+(opt.flags?' on':'')+'" data-opt="flags">START HERE</button>'
                + '<button class="hopb'+(opt.labels?' on':'')+'" data-opt="labels">LABELS</button>'
                + '<button class="hopb'+(opt.cells?' on':'')+'" data-opt="cells" title="'
                +   'Collapse every chip into its cell count. A density read for a '
                +   'deliberate zoom-out -- no fit will ever put you here.">'
                +   'CELLS</button>'
                + '<button class="hopb'+(attn!=='still'?' on':'')+'" data-attn="1" title="'
                + (REDUCED ? 'the system asks for reduced motion' : 'start-here attention')
                + '">' + (REDUCED ? 'STILL (SYSTEM)' : attn.toUpperCase()) + '</button>';
  }

  function renderLedgers(){
    for (const e of [...host.querySelectorAll('.l0ledger')]) e.remove();
    /* THE CARD READS S.l0card, NOT S.l0open. Stewart, 27 August: clicking a node
       "spawns the panel on the right plus the panel that says the specifics about
       that node that floats ... but then it blocks the map".

       Both were true because one array meant two things. S.l0open lights the chip,
       lights its edges and drives the CLEAR chip; it ALSO drew the floating member
       card, so anything that lit a node covered the map with a card as well. The
       dossier already carries the same members through renderConnections, and
       carries them better -- with tier, direction and the reason the link exists.

       Splitting the two keeps every lighting behaviour and makes the card an
       explicit ask: CMD.expand(id) opens one, selection does not. */
    for (const id of (S.l0card || [])){
      const n = byId[id];
      if (!n) continue;
      const p = el('div','l0ledger');
      const col = (L0_CLS[n.cls]||L0_CLS.person).c;
      const mem = n.direct.length + n.routed.length;
      let h = '<div class="l0lh"><span class="mk" style="border-color:'+col+'"></span>'
        + '<div><div class="eb">'+esc(n.cls)+' · tier '+esc(n.tier)
        + ' · C'+n.C+' A'+n.A+' D'+n.D+'</div>'
        + '<h4>'+esc(n.label)+'</h4></div>'
        + '<span class="x" data-close="'+esc(id)+'">&times;</span></div>'
        + '<div class="l0sum"><b>'+mem+'</b> members · <b>'+n.deg+'</b> links · <b>'
        + n.claims+'</b> claims, <b>'+n.t1+'</b> tier 1<br>'
        + esc(l0Denials(n))+'</div>'
        + '<div class="l0body">';
      const groups = {};
      for (const m of n.direct){
        const meta = D.nodes[m];
        if (!meta) continue;
        (groups[meta[1]] = groups[meta[1]] || []).push([m, meta]);
      }
      for (const k of Object.keys(groups).sort()){
        h += '<div class="l0grp">'+esc(k)+' · '+groups[k].length+'</div>';
        for (const [mid, meta] of groups[k])
          h += '<div class="l0row" data-node="'+esc(mid)+'"><span>'+esc(l0Short(meta[0], meta[1]))
             + '</span><span class="ld"></span><span class="dg">deg '+meta[2]+'</span></div>';
      }
      if (n.routed.length){
        h += '<div class="l0routed"><div class="l0grp">routed · '+n.routed.length+'</div>';
        for (const r of n.routed){
          const meta = D.nodes[r.id];
          if (!meta) continue;
          h += '<div class="l0row" data-node="'+esc(r.id)+'"><span>'+esc(l0Short(meta[0], meta[1]))
             + '</span><span class="ld"></span><span class="dg">deg '+meta[2]+'</span></div>'
             + '<div class="l0via">via '+r.via.map(v=>esc(l0Short((D.nodes[v]||['?','x'])[0],(D.nodes[v]||['?','x'])[1]))).join(' → ')+'</div>';
        }
        h += '</div>';
      }
      h += '</div>';
      p.innerHTML = h;
      /* Clamp into the visible canvas. Previously the card was positioned from
         the node and allowed to run past the bottom edge, so a header reading
         "PERSON - 6" could render one row with no scrollbar and no "+5 more":
         the count and the content disagreed and the reader had no way to tell. */
      const CARD_H = Math.min(430, H - 24);
      const sx = Math.max(PAD.l + 6, Math.min(W - 314, SX(n.x) + n.w*view.k + 10));
      const sy = Math.max(PAD.t + 6, Math.min(H - CARD_H - 8, CY(n) - 40));
      p.style.maxHeight = CARD_H + 'px';
      p.style.display = 'flex';
      p.style.flexDirection = 'column';
      p.style.left = sx+'px'; p.style.top = sy+'px';
      host.appendChild(p);
    }
  }

  function renderRegister(){
    const old = host.querySelector('.l0reg');
    if (old) old.remove();
    if (!S.l0panel) return;
    const isPath = S.l0panel === 'path';
    const rows = isPath ? D.pathOnly : D.unattached;
    const p = el('div','l0reg');
    let h = '<span class="x" data-panel="">&times;</span>'
      + '<h4>' + (isPath ? 'Path only · '+rows.length : 'Unattached · '+rows.length) + '</h4>'
      + '<p>' + (isPath
          ? 'Reachable from the map, but at four hops or more. Too far to be claimed as a member of anything, so they are listed here rather than attributed to a node they barely touch.'
          : 'No path to the map at any depth. '+D.unattached.filter(r=>r.deg===0).length
            + ' of them carry no hand-written edge at all, which is a research finding rather than a display problem.')
      + '</p><div class="rows">';
    for (const r of rows){
      const meta = D.nodes[r.id] || ['?','?',0,'?'];
      const right = isPath ? ('depth '+r.depth)
        : ('<span class="'+(r.deg===0?'l0zero':'')+'">deg '+r.deg+'</span>');
      h += '<div class="l0row" data-node="'+esc(r.id)+'"><span>'+esc(l0Short(meta[0],meta[1]))
         + '</span><span class="ld"></span><span class="dg">'+right+'</span></div>';
    }
    /* A zero-result register must SAY it is zero. An empty panel reads as one
       that failed to load, which is indistinguishable from broken from the
       outside -- the same class of defect as a check that always passes. */
    if (!rows.length){
      p.className = 'l0reg empty';
      p.innerHTML = h + '</div><div class="none">No entities in this register. '
        + 'Every node on the board is reachable from the map.</div>';
    } else {
      p.innerHTML = h + '</div>';
    }
    host.appendChild(p);
  }

  function tip(n, mx, my){
    let t = host.querySelector('.l0tip');
    if (!n){ if (t) t.remove(); return; }
    if (!t){ t = el('div','l0tip'); host.appendChild(t); }
    const mem = n.direct.length + n.routed.length;
    const mix = Object.keys(n.mix).map(k=>n.mix[k]+' '+k.slice(0,4)).join(' · ');
    t.innerHTML = '<b>'+esc(n.cls.toUpperCase())+' · '+esc(n.label)+'</b><br>'
      + mem + ' members' + (mix ? ' — '+esc(mix) : '') + '<br>'
      + 'degree '+n.deg+' · '+n.claims+' claims, '+n.t1+' tier 1<br>'
      + esc(l0Denials(n))+'<br>'
      + '<span class="act">' + (mem >= 2
          ? 'click opens the dossier'
          : 'click opens the dossier — '+mem+' member, no aggregate to list') + '</span>';
    t.style.left = Math.min(W-300, mx+14)+'px';
    t.style.top  = Math.min(H-110, my+14)+'px';
  }

  /* THE LEGEND. Design: "A pointer without its reason is the thing this board
     exists not to do." Fourteen reasons are authored in data/l0-highlights.json
     and until now reached the analyst's scripted branch and nothing else, so the
     map carried fourteen amber pointers and no account of why any of them was
     pointed at. Ranked, clickable, and gone when START HERE is off. */
  let legendOpen = false;
  function renderLegend(){
    const f = foot();
    const old = f.querySelector('.l0legend');
    if (old) old.remove();
    if (!opt.flags || !FLAGSET.length) return;
    const p = el('div','l0legend' + (legendOpen ? ' open' : ''));
    let h = '<h5 data-legend="toggle"><span>' + (legendOpen ? '\u25be' : '\u25b8')
          + ' START HERE \u00b7 ' + FLAGSET.length + (legendOpen ? '' : ' \u00b7 why')
          + '</span><span class="x" data-opt="flags">&times;</span></h5>';
    FLAGSET.forEach((id, i) => {
      const n = byId[id];
      if (!n) return;
      h += '<div class="l0lg" data-node="'+esc(id)+'">'
         + '<span class="r">'+String(i+1).padStart(2,'0')+'</span>'
         + '<span><span class="t">'+esc(n.short || n.label || id)+'</span>'
         + '<div class="w">'+esc(FLAGWHY[id] || 'no reason given in the highlights file')+'</div>'
         + '</span></div>';
    });
    p.innerHTML = h;
    /* First in the column, so the legend sits ABOVE the selection bar: the bar is
       the control for what you just picked and belongs nearest the thumb. */
    f.insertBefore(p, f.firstChild);
  }
  /* SHOW ON MAP. Design gives three choreographies and recommends CEDE as the
     default, with the choice a PREFERENCE rather than a mode -- so the reader is
     never in a state they have to get out of.

       CEDE      panels fold to labelled spines, the map re-fits to the room it
                 gains, the target arrives outlined. For a first look at where a
                 node sits.
       PORTHOLE  nothing moves but light: the layout holds and the camera does not
                 move, so the paragraph you are reading stays where it is.
       TETHER    camera only: the target is panned into the room there is. For
                 scanning several nodes in a row.

     Stored per reader, defaulting to CEDE. */
  const CHO = ['cede', 'porthole', 'tether'];
  let choreo = 'cede';
  try { const v = localStorage.getItem('program.choreo');
        if (CHO.indexOf(v) >= 0) choreo = v; } catch(e){}

  function showOnMap(){
    const id = S.sel; if (!id || !byId[id]) return;
    if (choreo === 'cede'){
      /* Fold, then let the box change do the fit -- one path for the camera, the
         same reason foldPanels() does not fit for FIT ALL. The selection stays
         outlined by the chip and cell renderers, so "the target arrives outlined"
         needs no extra drawing. */
      focusId = null; camMode = 'auto'; zoom = 'all';
      foldPanels();
      repaint();
    } else if (choreo === 'porthole'){
      /* Layout holds and the camera stays put. The board is already dimmed to the
         selection's thread by the focus layer, so what porthole guarantees is the
         thing the reader asked for: nothing moves. */
      repaint();
    } else {
      focus(id);
    }
  }

  /* The column both bottom overlays live in. Created on demand and reused, so the
     legend and the bar never race to append themselves to the host. */
  function foot(){
    let f = host.querySelector('.l0foot');
    if (!f){ f = el('div','l0foot'); host.appendChild(f); }
    /* INSET BY WHATEVER OVERLAYS THE MAP'S RIGHT SIDE, MEASURED.
       Design §7 says to inset the selection bar by the panel width. I skipped it
       on the reasoning that this board's dossier is a grid column and never covers
       the map -- true of the dossier, and wrong: .l0ledger is z-index 6, position
       absolute, and sits ON the map. Four of the bar's five buttons hit-tested to
       .l0row inside it. Design was right and the reasoning that dismissed them was
       checking the wrong panel.
       Measured rather than given the ledger's 306px, because that width is a CSS
       constant that has already changed once and this file has been bitten four
       times by exactly that. */
    let inset = 0;
    for (const el2 of host.querySelectorAll('.l0ledger, .l0reg')){
      const r = el2.getBoundingClientRect();
      if (!r.width) continue;
      const hb = host.getBoundingClientRect();
      /* only what actually overlaps the foot's own band, at the bottom */
      if (r.bottom < hb.bottom - 120) continue;
      inset = Math.max(inset, Math.ceil(hb.right - r.left) + 10);
    }
    f.style.right = (12 + inset) + 'px';
    return f;
  }
  function renderSelBar(){
    const f = foot();
    let bar = f.querySelector('.l0selbar');
    const n = S.sel && byId[S.sel];
    if (!n){ if (bar) bar.remove(); return; }
    if (!bar){ bar = el('div','l0selbar'); f.appendChild(bar); }
    const lbl = n.short || n.label || n.id;
    bar.innerHTML = '<div class="nm"><span class="cl">'
      + esc(String(n.cls||'').toUpperCase()) + '</span>' + esc(lbl) + '</div>'
      + '<button class="pri" data-showmap="1">SHOW ON MAP</button>'
      + '<span class="cho">'
      + CHO.map(k => '<button class="'+(choreo===k?'on':'')+'" data-choreo="'+k+'" '
                   + 'title="' + (k === 'cede'
                        ? 'Fold the panels and fit the whole board, with this node outlined.'
                        : k === 'porthole'
                        ? 'Change nothing -- keep this paragraph and its node where they are.'
                        : 'Pan this node into the room there is, without folding anything.')
                   + '">' + k.toUpperCase() + '</button>').join('')
      + '</span>'
      + '<button data-selclear="1">CLEAR</button>';
  }

  function repaint(){
    /* renderChrome first, then measure what it produced, and only then paint the
       map -- the map's top reserve depends on the height the control row actually
       took. Painting first would draw one frame against the previous reserve, and
       on a width change that frame is the one the reader sees. */
    renderChrome();
    const t0 = PAD.t;
    measureHead();
    /* The left inset costs nothing to re-measure and must be re-measured: the fold
       tab moves whenever the rail does, on a curve, and every frame of that curve
       is a frame the reader sees. Unlike PAD.t it changes no reserve, so it needs
       no clampView(). */
    measureGutter();
    if (PAD.t !== t0) clampView();
    paintMap(); renderLedgers(); renderRegister(); renderLegend();
    renderSelBar(); startLoop();
  }

  /* FIT ALL folds the rail and the dossier to spines and lets the box change do
     the work: the ResizeObserver is already the one path that reacts to the box,
     so this deliberately does NOT fit here. Fitting here as well would run two
     fits against two different measurements of the same moment, which is the
     drift clampView() exists to prevent. */
  /* FIT ALL, as a function rather than as three statements inside a click handler,
     because CMD.openPath needs exactly this gesture and inlining it there would be
     the second copy of a camera path -- the thing clampView() exists to prevent.
     Deliberately does NOT fit: foldPanels changes the box and the ResizeObserver is
     the one path that reacts to the box. */
  function fitAll(){ camMode = 'auto'; zoom = 'all'; foldPanels(); }
  function foldPanels(){
    const app = document.getElementById('app');
    if (app) app.classList.add('rail-off');
    if (typeof S !== 'undefined') S.railOpen = false;
    /* THROUGH applyChrome, not around it. Setting the class and the flag by hand
       left the rail's own chrome stale: the "CLICK TO CLOSE" tab stayed on screen
       pointing at a rail that was already shut, and the toolbar button kept saying
       Collapse. FIT ALL and openPath both come through here, so both showed it.
       Caught by both-drawers-fold-on-a-curve on its first run -- the fold sampled
       one distinct width because the pane it was told to close was closed already.
       applyChrome is the single owner of that chrome; this is now its caller. */
    if (typeof applyChrome === 'function') applyChrome();
    /* Through the same state the tabs use. FIT ALL folding by hand while
       renderDock folded by rule was two owners of one panel. */
    if (typeof S !== 'undefined') S.dockSpine = true;
    if (typeof setDockOpen === 'function') setDockOpen(false);
    const dock = document.getElementById('dock');
    if (dock){
      dock.classList.add('dock-spine');
      dock.classList.remove('dock-wide');
      dock.style.width = '30px';
      document.documentElement.style.setProperty('--dock-w', '30px');
    }
  }
  /* One click anywhere on the spine puts it back. Bound on the document rather
     than on the element because renderDock rebuilds the dock's insides. */
  document.addEventListener('click', ev => {
    const sp = ev.target.closest('#dock.dock-spine');
    if (!sp) return;
    /* RECORD THE INTENT, do not just change the class. renderDock re-applies the
       fold from S.dockSpine on its next run, so a handler that only stripped the
       class would have the panel snap shut again the moment anything re-rendered
       the dock -- open, then closed, with no error and no obvious cause. */
    if (typeof S !== 'undefined') S.dockSpine = false;
    sp.classList.remove('dock-spine');
    sp.style.width = '';
    document.documentElement.style.removeProperty('--dock-w');
    if (typeof renderDock === 'function') renderDock();
    else if (typeof setDockOpen === 'function') setDockOpen(!!(typeof S !== 'undefined' && S.sel));
  });

  /* Chip labels are fitted with ctx.measureText, so the geometry the map draws
     depends on which font is actually resolved at draw time. The faces are
     inlined as data: URIs and so resolve without a network round trip, but
     decode is still asynchronous: a first paint can land against the fallback
     metrics and then never be corrected, which shows up as labels truncated
     harder than they need to be. One repaint when the real font is ready costs
     nothing and closes the window. */
  if (document.fonts && document.fonts.ready){
    document.fonts.ready.then(() => { if (!dead) repaint(); });
  }

  /* ---- events --------------------------------------------------------- */
  host.addEventListener('mousedown', ev => {
    if (ev.target !== cvs) return;
    drag = { x:ev.clientX, y:ev.clientY, ox:view.ox, oy:view.oy }; moved = false;
  });
  window.addEventListener('mousemove', ev => {
    if (dead) return;
    const b = host.getBoundingClientRect(), mx = ev.clientX-b.left, my = ev.clientY-b.top;
    if (drag){
      const dx = ev.clientX-drag.x, dy = ev.clientY-drag.y;
      if (Math.abs(dx)+Math.abs(dy) > 3) moved = true;
      view.ox = drag.ox+dx; view.oy = drag.oy+dy;
      if (moved){ zoom = null; hold(); }   /* taken by hand */
      clampView();
      paintMap(); renderChrome(); renderLedgers();
      return;
    }
    if (mx<0||my<0||mx>W||my>H){ if (hover){ hover=null; tip(null); paintMap(); } return; }
    const n = at(mx,my);
    const id = n ? n.id : null;
    if (id !== hover){ hover = id; paintMap(); }
    tip(n, mx, my);
  });
  window.addEventListener('mouseup', () => { drag = null; });
  cvs.addEventListener('click', ev => {
    if (moved) { moved = false; return; }
    const b = host.getBoundingClientRect();
    const n = at(ev.clientX-b.left, ev.clientY-b.top);
    if (!n) return;
    CMD.expand(n.id);
  });
  cvs.addEventListener('wheel', ev => {
    ev.preventDefault();
    const b = host.getBoundingClientRect(), mx = ev.clientX-b.left, my = ev.clientY-b.top;
    const k2 = Math.max(0.18, Math.min(2.2, view.k * (ev.deltaY < 0 ? 1.12 : 1/1.12)));
    view.ox = mx - (mx-view.ox)*(k2/view.k); view.oy = my - (my-view.oy)*(k2/view.k);
    view.k = k2; zoom = null; hold(); clampView(); repaint();
  }, { passive:false });
  host.addEventListener('click', ev => {
    const c = ev.target.closest('[data-close]');
    if (c) return CMD.collapse(c.getAttribute('data-close'));
    if (ev.target.closest('[data-clear]')) return CMD.clearExpansions();
    /* A fit button RE-ARMS the camera. That is the way back from HELD, and it is
       the only one: nothing else silently takes the camera off the reader. */
    if (ev.target.closest('[data-fit]')){
      camMode='auto'; zoom='fit'; centreOn(roomScale()); repaint(); return; }
    if (ev.target.closest('[data-fitall]')){ fitAll(); return; }
    if (ev.target.closest('[data-one]')){
      hold(); zoom='one'; cornerOn(1); repaint(); return; }
    if (ev.target.closest('[data-showmap]')){ showOnMap(); return; }
    const ch = ev.target.closest('[data-choreo]');
    if (ch){
      choreo = ch.getAttribute('data-choreo');
      try { localStorage.setItem('program.choreo', choreo); } catch(e){}
      /* A preference, not a mode: picking one runs it straight away rather than
         arming it for next time, so the reader sees what they chose. */
      renderSelBar(); showOnMap(); return;
    }
    if (ev.target.closest('[data-selclear]')){ CMD.clearSelection(); return; }
    if (ev.target.closest('[data-legend]')){
      legendOpen = !legendOpen; renderLegend(); return;
    }
    if (ev.target.closest('[data-attn]')){
      if (REDUCED) return;                      /* the override is not negotiable */
      attn = L0_ATTN[(L0_ATTN.indexOf(attn) + 1) % L0_ATTN.length];
      stopLoop(); animT = 0;
      renderChrome(); startLoop(); repaint();
      return;
    }
    const o = ev.target.closest('[data-opt]');
    if (o){
      const k = o.getAttribute('data-opt'); opt[k] = !opt[k];
      if (k === 'flags'){ stopLoop(); animT = 0; startLoop(); }
      renderChrome(); repaint(); return;
    }
    const p = ev.target.closest('[data-panel]');
    if (p){ S.l0panel = p.getAttribute('data-panel') || null; renderRegister(); return; }
    const r = ev.target.closest('[data-node]');
    /* The ledger is a table of contents, not a replacement for the dock. */
    if (r) return CMD.selectNode(r.getAttribute('data-node'));
  });

  measure();
  const fk = fitScale();
  /* Open FITTED, at every width. Design's comp states this outright -- its root
     state is `zoom: 'fit'` -- and this build diverged from it for a long time:
     below the label threshold it gave up on fitting and opened at 1:1 in the
     top-left corner, which on any screen under about 1944px is three of seven
     bands. Reported from a real screen as "the map is never able to fit", which
     is exactly what it was.

     THE JUSTIFICATION FOR FITTING CHANGED ON 27 AUGUST and the old one is left
     here because it reads as current and is not. It used to be: below the
     threshold the chips drew as 110 anonymous rectangles, and the dense occupancy
     mode redeemed that by printing a count in every cell, so a fitted opening was
     the occupancy matrix and still said something. That is no longer what a fitted
     opening is. Cell mode is an explicit opt now and nothing automatic reaches it,
     so the fitted view is the real lattice -- chips, rules and edges -- unlabelled
     below 0.62 and labelled above it. Which is what was wanted all along, and what
     Stewart asked for: "nobody ever gets to see the map in its normal form and
     it's central to it, as it shows how robust our connections are." */
  centreOn(fk);
  zoom = 'fit';
  repaint();
  startLoop();
  /* One path for every change to the box, and while AUTO it RE-FITS rather than
     merely clamping. Clamping alone was the defect behind "the map is never able
     to fit": open the dossier, the map narrows, the camera stays put and shows
     less of the board than it did a second earlier.
     The window listener is a fallback -- ResizeObserver covers the element, but a
     zoom change or a devicePixelRatio flip can move the box without the observer
     firing on some engines, and a fit that silently stops fitting is the whole
     failure mode of this file. */
  function boxChanged(){
    measure();
    if (camMode === 'auto'){
      centreOn(zoom === 'all' ? allScale() : roomScale());
    } else if (focusId && byId[focusId]){
      /* HELD on a node: keep THAT node centred in whatever box there now is,
         rather than re-fitting the board or leaving the camera where a smaller
         box put it. Selecting a node opens the dossier, which changes the box a
         frame later, so this is the common path and not an edge case. */
      const n = byId[focusId];
      view.ox = W/2 - (n.x + n.w/2)*view.k;
      view.oy = H/2 - (n.y + n.h/2)*view.k;
    }
    clampView();
    repaint();
  }
  const ro = new ResizeObserver(boxChanged);
  ro.observe(host);
  window.addEventListener('resize', boxChanged);
  return {
    repaint, pairs: [],   /* INSIGHTS() reaches for this; see renderNetworkChrome */
    opt,
    destroy(){ dead = true; ro.disconnect(); stopLoop(); if (raf) cancelAnimationFrame(raf); },
    fitScale, view,
  };
}

/* SURNAME, I. for persons with suffixes preserved; everything else truncates at a
   stated width. This is the site of the JR., J. bug — five different people once
   rendered as the same string because a label was split on the first space. It is
   also why a routed row must never print `via AARO` for a FOIA memorandum. */
function l0Short(label, cls){
  const s = String(label||'');
  if (cls !== 'person') return s.length > 34 ? s.slice(0,33)+'…' : s;
  const parts = s.replace(/,/g,' ').split(/\s+/).filter(Boolean);
  if (parts.length < 2) return s;
  const SUFFIX = /^(jr|sr|ii|iii|iv|v)\.?$/i;
  let last = parts.length-1, suf = '';
  while (last > 0 && SUFFIX.test(parts[last])){ suf = ' '+parts[last].toUpperCase().replace(/\.$/,'')+'.'; last--; }
  const surname = parts[last].toUpperCase();
  const initial = parts[0][0] ? parts[0][0].toUpperCase()+'.' : '';
  return surname + suf + ', ' + initial;
}
"""

# ------------------------------------------------------------------ CMD actions
VIEW_PROGRAM_JS = r"""/* --- PROGRAM MAP ------------------------------------------------------------
   Design's packed-cell map of the 110-node programme, on a tab of its own.

   The scaffolding is deliberately identical to viewNetwork's: the same absolute
   host, the same `.cwrap`, the same sweep overlay and the same `#netchrome`
   element. renderNetworkChrome() reads that element and, under `!S.l0full`,
   empties it -- the packed map draws its own breadcrumb, ledgers and controls, and
   the inherited hop/legend chrome reads MAP.pairs, which the packed map does not
   have. Leaving the element out instead of emptying it would make that function
   return early on a missing node, which is a silence rather than a fix.

   `S.l0full` is the flag every downstream surface keys on: the chrome suppressor,
   paint()'s repaint branch, and the breadcrumb. It is set here rather than left to
   the previous view, because a view that inherits a flag is a view that renders
   differently depending on where the reader came from. */
function viewProgramMap(v){
  v.style.cssText = 'position:absolute;inset:0;overflow:hidden';
  const wrap = el('div','cwrap l0wrap');
  v.appendChild(wrap);
  v.appendChild(el('div','sweep'));
  const chrome = el('div'); chrome.id = 'netchrome'; v.appendChild(chrome);
  S.l0full = false;
  MAP = mountL0(wrap);
  renderNetworkChrome();
}
"""

L0_CMD = r"""
  /* ---- L0 program map. Five actions, each with a clickable control. If a
     control exists with no CMD entry the analyst cannot operate it, and the
     "drive the whole app from the chat input" requirement is broken. ------- */
  expand(id){
    const n = (L0DATA.l0||[]).find(x=>x.id===id);
    if (!n) return warn('no L0 node with id "'+id+'". It may be in the ledger, path-only or unattached register.');
    const mem = n.direct.length + n.routed.length;
    if (mem < 2) return warn('expand("'+id+'") — refused: '+mem+' member, no aggregate to open');
    if (S.l0open.indexOf(id) < 0) S.l0open.push(id);
    /* expand() is the ONLY thing that opens the floating card. Lazily initialised
       rather than declared in S, because S's literal is rewritten by three
       separate patches and a fourth owner of it is how this file gets bitten. */
    if (!S.l0card) S.l0card = [];
    if (S.l0card.indexOf(id) < 0) S.l0card.push(id);
    paint({ map:'l0' });
  },
  collapse(id){
    const i = S.l0open.indexOf(id);
    if (i < 0) return warn('"'+id+'" is not open');
    S.l0open.splice(i,1);
    const j = (S.l0card || []).indexOf(id);
    if (j >= 0) S.l0card.splice(j,1);
    paint({ map:'l0' });
  },
  clearExpansions(){ S.l0open = []; S.l0card = []; paint({ map:'l0' }); },
  /* The two registers and the entry surface are drawn by the packed map, so they
     name the view that mounts it. They said NETWORK while the packed map WAS the
     network rest state; after the inversion that would have sent the reader to the
     force-directed graph and then rendered nothing, which is the shape of bug that
     looks like a dead button. */
  showPathOnly(){ S.l0panel = 'path'; S.view = 'PROGRAM'; paint({ full:true }); },
  showUnattached(){ S.l0panel = 'un'; S.view = 'PROGRAM'; paint({ full:true }); },
"""


# ---------------------------------------------------------------------- apply
# ------------------------------------------------------------- packed geometry
def _repo_root():
    """The repo root, derived from this file rather than from the caller's cwd —
    build_dashboard.py may be invoked from anywhere."""
    import os
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def merge_packed(model, layout):
    """Fold the packed-cell layout into the L0 model, in place.

    Design's layout (`tools/build_l0_layout.mjs` -> `data/l0-layout-model.json`)
    is the arrangement that ships. build_l0.py's force layout is kept alongside as
    `fx`/`fy` rather than thrown away, because build_l0.py still reports on it and a
    number that describes a layout nobody draws is exactly the kind of quiet lie
    CLAUDE.md section 5 is about. Nothing reads `fx`/`fy` at runtime.

    Every id must be present on both sides. A partial merge would put some chips on
    the grid and leave the rest at force coordinates, which renders as a plausible
    mess rather than an error -- so this raises instead.
    """
    cur = layout.get("current") or {}
    lay = {n["id"]: n for n in cur.get("nodes", [])}
    ids = {n["id"] for n in model.get("l0", [])}
    missing = sorted(ids - set(lay))
    extra = sorted(set(lay) - ids)
    if missing or extra:
        raise SystemExit(
            "l0_patches.merge_packed: the layout model and the L0 model disagree "
            "on which nodes are on the map.\n"
            f"  missing from the layout: {missing[:8]}\n"
            f"  absent from the L0 model: {extra[:8]}\n"
            "  Re-run tools/build_l0.py then node tools/build_l0_layout.mjs.")

    for n in model["l0"]:
        L = lay[n["id"]]
        n["fx"], n["fy"] = n["x"], n["y"]      # force layout, kept, not drawn
        n["x"], n["y"] = L["x"], L["y"]        # packed chip, TOP-LEFT not centre
        n["w"], n["h"] = L["w"], L["h"]
        n["band"], n["col"] = L["band"], L["col"]
        n["iso"] = bool(L.get("isolated"))
        # role tags, for the search grammar's `role:` filter. They are the basis
        # for band assignment, so a reader who can see the band should be able to
        # ask for the tag behind it.
        n["roles"] = L.get("roles") or []
        # The mark, if this node has one. Set on the LAYOUT's nodes by
        # build_l0_layout.mjs from data/l0-images.json, and copied here because
        # the renderer reads model["l0"]. Without this the register populated
        # cleanly, the layout model carried all eleven records, and the page drew
        # 110 class letters -- the register working and the board not showing it,
        # which is the same shape as the denial verdicts stopping at the layout
        # model earlier today.
        for k in ("photo", "photoCredit", "photoKind", "photoClearance", "photoNote"):
            if L.get(k):
                n[k] = L[k]

    # Edge budget. `rest` says which edges draw with nothing selected; `role` says
    # why each one earned the space. Keyed a|b|kind because a pair can carry both a
    # direct edge and a summarised one and they are different objects.
    rest, roles = [], {}
    # The adjudication travels with the edge. data/denial-adjudication.json is
    # stamped onto the board by merge.py and aggregated per pair by
    # build_l0_layout.mjs, but the page reads model["directEdges"], which is
    # built by build_l0.py and carries only a/b/n/tier/types. So the verdicts
    # reached the layout model and stopped there: the renderer read e.denialKind
    # and got undefined for all 47, and every denial on the map drew as
    # undirected -- the bar -- no matter what the record said. That is a quieter
    # failure than the arrowheads it replaced, and it would have looked like the
    # adjudication was simply cautious rather than not arriving at all.
    dn_by_pair = {}
    for e in cur.get("edges", []):
        k = e["a"] + "|" + e["b"] + "|" + ("direct" if e["kind"] == "direct" else "shared")
        if e.get("rest"):
            rest.append(k)
        if e.get("role"):
            roles[k] = e["role"]
        if e.get("denialKind") or e.get("denier") or e.get("dn"):
            dn_by_pair["|".join(sorted((e["a"], e["b"])))] = {
                "denialKind": e.get("denialKind"),
                "denier": e.get("denier"),
                "dn": e.get("dn") or [],
            }
    # ---- the marks, inlined -------------------------------------------
    # data/l0-images.json holds a repo PATH in `photo`; the page needs bytes.
    # Inlining happens HERE and not in build_l0_layout.mjs because that file is
    # read through the GitHub API and has a ~1MB cap: putting 695KB of base64
    # into it -- twice, since `current` and `legacy` both carry nodes -- took it
    # from 490KB to 1836KB and its own guard refused the build. The description
    # of the page stays small; the page carries the bytes, where 520KB against
    # 14MB is noise.
    #
    # And it MUST be bytes rather than a URL: `the built page fetches nothing at
    # runtime` is a gate check, and a remote mark would break it while making
    # first paint depend on someone else's server.
    import base64, os
    _MIME = {".svg": "image/svg+xml", ".webp": "image/webp", ".jpg": "image/jpeg",
             ".jpeg": "image/jpeg", ".png": "image/png"}
    for n in model.get("l0", []):
        rel = n.get("photo")
        if not rel or str(rel).startswith("data:"):
            continue
        abs_ = os.path.join(_repo_root(), rel)
        if not os.path.exists(abs_):
            raise SystemExit(
                f"data/l0-images.json: {n['id']} points at {rel}, which does not "
                f"exist. Add the file or remove the record -- a missing mark must "
                f"not degrade silently into the class letter.")
        ext = os.path.splitext(abs_)[1].lower()
        with open(abs_, "rb") as fh:
            n["photo"] = ("data:" + _MIME.get(ext, "image/png") + ";base64,"
                          + base64.b64encode(fh.read()).decode("ascii"))

    for e in model.get("directEdges", []):
        r = dn_by_pair.get("|".join(sorted((e["a"], e["b"]))))
        if not r:
            continue
        if r["denialKind"]:
            e["denialKind"] = r["denialKind"]
        if r["denier"]:
            e["denier"] = r["denier"]
        if r["dn"]:
            e["dn"] = r["dn"]

    flags = [f["id"] for f in sorted(
        (cur.get("highlights") or {}).get("flags", []),
        key=lambda f: f.get("rank", 999))]

    model["packed"] = {
        "worldW": cur.get("worldW"), "worldH": cur.get("worldH"),
        "geo": (cur.get("config") or {}).get("geo", {}),
        "bands": [{k: b[k] for k in ("id", "y", "h", "rows", "n", "meanC", "residual")
                   if k in b} for b in cur.get("bands", [])],
        "eras": [{k: c[k] for k in ("id", "label", "note", "kind", "x", "w") if k in c}
                 for c in cur.get("eras", [])],
        "flags": flags,
        "rest": rest,
        "roles": roles,
        "bandOrder": (cur.get("config") or {}).get("bandOrder"),
        "edgeRule": (cur.get("config") or {}).get("edgeRule"),
    }
    # The analyst's "where do I start" already reached for L0DATA.highlights.flags
    # and got nothing, because build_l0.py never wrote it. It is written here.
    model["highlights"] = cur.get("highlights") or {}
    return model


def apply(s, model, must_replace, layout=None):
    """Splice the L0 map into the built dashboard.

    `must_replace` is build_dashboard's own helper, passed in so a failed anchor
    reports through the same channel as every other patch and the build says
    "SOME PATCHES FAILED" rather than emitting a quietly broken file.

    `layout` is data/l0-layout-model.json. It is not optional in the build -- the
    default exists so a caller in a test can splice the module without it -- and
    when it is absent the map has no geometry to draw, so say so and stop."""
    import json as _json
    ok = True

    if layout is not None:
        merge_packed(model, layout)
    elif "packed" not in model:
        raise SystemExit("l0_patches.apply: no packed layout. mountL0 draws chips "
                         "at model positions and there are none.")

    # -- the model. Serialised compactly: it is ~500KB and every byte of it is
    #    parsed at load, which is the cost the dossier-payload item is about.
    block = "const L0DATA = " + _json.dumps(model, separators=(",", ":")) + ";\n"
    s, o = must_replace(s, "const CMD = {", block + "\n" + L0_JS + "\nconst CMD = {",
                        "L0 model + view module", 1); ok &= o

    # -- five CMD actions
    s, o = must_replace(s, "const CMD = {\n  selectNode(id){",
                        "const CMD = {" + L0_CMD + "  selectNode(id){",
                        "L0 CMD actions", 1); ok &= o

    # -- state
    s, o = must_replace(s, "  turns:[], narrow:false,\n};",
                        "  turns:[], narrow:false,\n"
                        "  l0open:[], l0panel:null, l0full:false, dockOff:false,\n};",
                        "L0 state", 1); ok &= o

    # -- styles
    s, o = must_replace(s, "</style>", L0_CSS + "</style>", "L0 styles",
                        s.count("</style>")); ok &= o

    # -- THE INVERSION, 29 August 2026. See this module's docstring for the call
    #    and the reasoning. Six patches, and the risk in all of them is that a
    #    surface goes quiet rather than red.
    #
    # (a) NETWORK mounts the full graph unconditionally. It used to mount it only
    #     when a path or a frame was live, which meant the commands that set those
    #     -- highlightPath, focusCluster, frameNodes, the insight callout's "Show me
    #     on the map" -- worked from every view EXCEPT the one they targeted, where
    #     renderSurface's own re-mount guard returned before the swap could happen.
    #     Making it unconditional removes that whole class of dead command.
    s, o = must_replace(s,
        "  MAP = mountNetwork(wrap);\n  renderNetworkChrome();",
        "  S.l0full = true;\n"
        "  MAP = mountNetwork(wrap);\n  renderNetworkChrome();",
        "NETWORK mounts the full graph unconditionally", 1); ok &= o

    # (b) the packed map becomes a view. Four string patches, which is what a view
    #     costs on this shell: the VIEWS array, VIEW_LABEL, the dispatch map, and
    #     the function. The rail builds itself from VIEWS, so the tab appears with
    #     no markup change. Second in the order, next to the map it used to be.
    s, o = must_replace(s,
        "const VIEWS = ['NETWORK','TIMELINE',",
        "const VIEWS = ['NETWORK','PROGRAM','TIMELINE',",
        "VIEWS gains PROGRAM", 1); ok &= o
    s, o = must_replace(s,
        "  NETWORK:'Network map', TIMELINE:'Timeline',",
        "  NETWORK:'Network map', PROGRAM:'Program map', TIMELINE:'Timeline',",
        "VIEW_LABEL gains PROGRAM", 1); ok &= o
    s, o = must_replace(s,
        "  ({ NETWORK:viewNetwork, TIMELINE:viewTimeline,",
        "  ({ NETWORK:viewNetwork, PROGRAM:viewProgramMap, TIMELINE:viewTimeline,",
        "view dispatch gains PROGRAM", 1); ok &= o
    s, o = must_replace(s,
        "/* --- NETWORK ---------------------------------------------------------------- */\n"
        "function viewNetwork(v){",
        VIEW_PROGRAM_JS
        + "/* --- NETWORK ---------------------------------------------------------------- */\n"
        "function viewNetwork(v){",
        "viewProgramMap", 1); ok &= o

    # (c) the packed map is stateful in exactly the way the comment above
    #     renderSurface's NETWORK guard describes -- it owns a canvas, a camera and
    #     a draw loop -- so it needs the same protection. Without this every paint()
    #     rebuilds it and throws away the reader's pan and zoom, which reads as the
    #     map refusing to be moved.
    s, o = must_replace(s,
        "  if (S.view === 'NETWORK' && MAP && mountedView === 'NETWORK')"
        "{ renderNetworkChrome(); return; }",
        "  if (S.view === 'NETWORK' && MAP && mountedView === 'NETWORK')"
        "{ renderNetworkChrome(); return; }\n"
        "  /* Same rule for the packed map. Its own surfaces -- breadcrumb, ledgers,\n"
        "     register panel -- are repainted by paint()'s camera step below, not by\n"
        "     remounting, because nodes never moving is the property that makes two\n"
        "     open ledgers comparable. */\n"
        "  if (S.view === 'PROGRAM' && MAP && mountedView === 'PROGRAM') return;",
        "the program map is never re-mounted while it is alive", 1); ok &= o

    # (d) a map fills its host. `pad` is for the document views.
    s, o = must_replace(s,
        "  const v = el('div','view'+(S.view==='NETWORK'?'':' pad'));",
        "  const v = el('div','view'+(S.view==='NETWORK'||S.view==='PROGRAM'?'':' pad'));",
        "the program map is a map, not a padded document", 1); ok &= o

    # (e) the number keys read the array rather than a literal 7. They already
    #     undercounted -- REPORT, the eighth, has never been reachable by key -- and
    #     a hardcoded bound silently drops whatever is added after it.
    s, o = must_replace(s,
        "  if (n >= 1 && n <= 7) CMD.setView(VIEWS[n-1]);",
        "  if (n >= 1 && n <= VIEWS.length) CMD.setView(VIEWS[n-1]);",
        "number keys cover every view there is", 1); ok &= o

    # (f) the analyst is meant to be able to operate every control on the board. A
    #     view it is not told about is a view it cannot send anyone to.
    s, o = must_replace(s,
        'setView("NETWORK"|"TIMELINE"|"GEOGRAPHY"|"CASES"|"ANALYSIS"|"COVERUP"|'
        '"SEARCH"|"REPORT")',
        'setView("NETWORK"|"PROGRAM"|"TIMELINE"|"GEOGRAPHY"|"CASES"|"ANALYSIS"|'
        '"COVERUP"|"SEARCH"|"REPORT")',
        "the analyst is told about the program map", 1); ok &= o

    # -- rail: the two registers, reachable with their full contents listed. This
    #    is what makes "nothing was left out" auditable rather than asserted.
    s, o = must_replace(s,
        "  if (S.filters.size || S.edgeTypes.size !== ALL_EDGE_TYPES.length || S.query)",
        "  h += '<div class=\"eyebrow\" style=\"margin:12px 0 6px\">Registers</div>';\n"
        "  h += '<button class=\"chip\" data-l0reg=\"path\">Path only '\n"
        "     + (L0DATA.counts.pathOnly) + '</button>'\n"
        "     + '<button class=\"chip\" data-l0reg=\"un\">Unattached '\n"
        "     + (L0DATA.counts.unattached) + '</button>';\n"
        "  if (S.filters.size || S.edgeTypes.size !== ALL_EDGE_TYPES.length || S.query)",
        "L0 rail registers", 1); ok &= o

    # ---- stage 2: selection, sliding dock, entity dossier -----------------
    s, o = must_replace(s, "</style>", L0_CSS2 + "</style>", "L0 stage-2 styles",
                        s.count("</style>")); ok &= o
    s, o = must_replace(s, "const CMD = {", L0_JS2 + "\nconst CMD = {",
                        "L0 stage-2 module", 1); ok &= o
    s, o = must_replace(s, "const CMD = {" + L0_CMD, "const CMD = {" + L0_CMD + L0_CMD2,
                        "focusL0 command", 1); ok &= o

    # SINGLE selection. The handoff's additive model left no way to unclick and no
    # visible exit; this replaces it. An analyst can still open two from the CMD
    # line, which is where comparison actually belongs.
    # Anchored on the push alone rather than on push+paint: expand() gained the
    # card list between them, and a patch keyed to two lines that are no longer
    # adjacent fails loudly, which is how this was caught.
    s, o = must_replace(s,
        "    if (S.l0open.indexOf(id) < 0) S.l0open.push(id);",
        "    S.l0open = [id];\n    if (MAP && MAP.focus) MAP.focus(id);",
        "single selection on expand", 1); ok &= o

    # selectNode drives the map too, so the dock never describes a node the reader
    # cannot see. focusL0 is still called for a node that is on the packed map, so
    # that tab is already lit correctly when the reader switches to it.
    s, o = must_replace(s,
        "    S.sel = id; S.tab = 'DOSSIER'; S.path = null; S.frame = null;\n"
        "    if (S.view !== 'NETWORK') S.view = 'NETWORK';\n    paint({ map:'select' });",
        "    S.sel = id; S.tab = 'DOSSIER'; S.path = null; S.frame = null;\n"
        "    /* A selection lands on the NETWORK map, which can answer 'what does\n"
        "       this connect to'. The one exception is a reader already standing on\n"
        "       the program map: there the ledger is a table of contents for the\n"
        "       dock, and opening the dock must not move the map out from under\n"
        "       them. That was the original rule; this is the whole of what is left\n"
        "       of it. */\n"
        "    if (S.view !== 'NETWORK' && S.view !== 'PROGRAM') S.view = 'NETWORK';\n"
        "    if ((L0DATA.l0||[]).some(x=>x.id===id)) CMD.focusL0(id);\n"
        "    else S.l0open = [];\n"
        "    paint({ map:'select' });",
        "selectNode syncs the map", 1); ok &= o

    # the dock opens wide on selection and collapses on clear, with one control
    s, o = must_replace(s,
        "function renderDock(){\n  const d = $('#dock');\n  d.classList.toggle('open', !!S.sel);",
        "function renderDock(){\n  const d = $('#dock');\n  d.classList.toggle('open', !!S.sel);\n"
        "  setDockOpen(!!S.sel && !S.dockCollapsed);",
        "dock opens on selection", 1); ok &= o

    # the entity dossier goes ABOVE the inherited node dossier: on this board the
    # argument for why an entity is implicated is the product, and the member list
    # is the table of contents for it
    s, o = must_replace(s,
        "  const grip = '<div class=\"dock-grip\" title=\"Drag to resize. Double click to reset\"></div>';",
        "  const grip = '<div class=\"dock-grip\" title=\"Drag to resize. Double click to reset\"></div>';",
        "dock collapse control", 1); ok &= o
    # ONE CONTROL ON THAT EDGE, NOT THREE. 27 August.
    # The dossier grew a `.dock-toggle` chevron (widen/narrow) and a `.dock-hide`
    # chevron (hide entirely), each an 11px glyph on the panel's left edge. The
    # labelled fold tab added today sits on the same edge and covered both --
    # tools/walk.js reported the two overlaps on its first clean run, which is
    # exactly the job it was built for.
    # They are not merely moved out of the way, they are retired. Both duplicate
    # what the fold now does, and Stewart asked for the affordance the spine
    # already had -- "that nice tab you click" -- not a third glyph beside two
    # others. `dock-hide` in particular collapsed the panel to zero width, which
    # is strictly worse than the spine: no width back that the spine does not
    # also give, and nothing left on screen to click. S.dockCollapsed and
    # S.dockOff stay in state and stay handled; nothing reaches them now.

    s, o = must_replace(s, "  const n = NODES.find(x=>x.id===S.sel);",
        "  const _ed = renderEntityDossier(S.sel);\n"
        "  const n = NODES.find(x=>x.id===S.sel);",
        "entity dossier lookup", 1); ok &= o

    # the entity dossier renders FIRST in the dock body
    s, o = must_replace(s,
        "  d.innerHTML = grip + ((n.cls === 'person') ? personDock(n) : otherDock(n));",
        "  d.innerHTML = grip + _ed + ((n.cls === 'person') ? personDock(n) : otherDock(n));",
        "entity dossier into the dock body", 1); ok &= o

    # the collapse control, and an obvious way out of a selection
    s, o = must_replace(s,
        "function renderDock(){\n  const d = $('#dock');",
        "document.addEventListener('click', ev => {\n"
        "  if (ev.target.closest('[data-dockw]')){\n"
        "    S.dockCollapsed = !S.dockCollapsed;\n"
"    setDockOpen(!!S.sel && !S.dockCollapsed); renderDock();\n"
        "  }\n});\n"
        "function renderDock(){\n  const d = $('#dock');",
        "dock toggle handler", 1); ok &= o

    # MAP.focus: move the camera to a node and light it. Clicking empty canvas
    # clears, which is the exit the first build did not have.
    s, o = must_replace(s,
        "  return {\n    repaint, pairs: [],",
        "  function focus(id){\n"
        "    const n = byId[id];\n"
        "    if (!n) return;\n"
        "    /* A PICK TAKES THE CAMERA. Design lists drag, wheel and pick as the\n"
        "       gestures that flip AUTO to HELD, and pick is the one that is easy\n"
        "       to miss: without it, selecting a node zoomed to 1.15 and then the\n"
        "       dossier opened, the box changed, and the AUTO re-fit threw the\n"
        "       focus away. Measured before this line existed: pick a node at a\n"
        "       1920 window and the map settled at k=0.289 with the node nominally\n"
        "       on screen and nothing on it readable.\n"
        "       focusId is remembered so a later box change RE-CENTRES on the node\n"
        "       instead of re-fitting the board -- the dossier opening must not\n"
        "       lose the thing the dossier is about. */\n"
        "    focusId = id; camMode = 'held'; zoom = null;\n"
        "    /* KEEP THE READER'S SCALE. This used to force `view.k = max(view.k,\n"
        "       1.15)` on the reasoning that the reader asked for the node they\n"
        "       clicked rather than a field of 96 -- but the node they clicked is\n"
        "       one they could already see, and taking the camera to 1.15 throws\n"
        "       away the overview they were reading it from. Stewart, 27 August:\n"
        "       \"you have to zoom too far to get the map back\". The dossier\n"
        "       carries everything the label cannot at this scale, so centring is\n"
        "       the whole of what a pick owes the reader. At a fitted camera the\n"
        "       clamp makes this very nearly a no-op, which is the point. */\n"
        "    /* n.x/n.y are the chip TOP-LEFT in the packed layout, so centring on\n"
        "       them would put the chip down-right of the middle by half its size --\n"
        "       102px of a 205px chip, which reads as the camera missing. */\n"
        "    view.ox = W/2 - (n.x + n.w/2)*view.k;\n"
        "    view.oy = H/2 - (n.y + n.h/2)*view.k;\n"
        "    clampView();   /* a node near an edge of the world must not drag the\n"
        "                      camera off it -- the clamp is what keeps the cells\n"
        "                      filling the content rect. */\n"
        "    repaint();\n"
        "  }\n"
        "  return {\n    repaint, focus, fitAll, pairs: [],",
        "MAP.focus", 1); ok &= o

    s, o = must_replace(s,
        "    const n = at(ev.clientX-b.left, ev.clientY-b.top);\n    if (!n) return;\n"
        "    CMD.expand(n.id);",
        "    const n = at(ev.clientX-b.left, ev.clientY-b.top);\n"
        "    /* empty canvas clears. Before this there was no way to unclick. */\n"
        "    if (!n){ if (S.sel || S.l0open.length){ CMD.clearExpansions(); CMD.clearSelection(); } return; }\n"
        "    /* clicking the open node again closes it — the other half of the exit.\n"
        "       Keyed on S.sel rather than S.l0open now that a click no longer opens\n"
        "       a card: the selection IS what a second click is undoing. */\n"
        "    if (S.sel === n.id){ CMD.clearExpansions(); CMD.clearSelection(); return; }\n"
        "    /* THE DOSSIER, AND ONLY THE DOSSIER. This used to call expand() as well,\n"
        "       so one click produced two panels about the same node and the floating\n"
        "       card sat on the map -- Stewart, 27 August: it \'blocks the map\'. The\n"
        "       dossier already lists the same members through renderConnections, with\n"
        "       tier, direction and the reason each link exists, which the card does\n"
        "       not. CMD.expand(id) still opens the card for anyone who wants it. */\n"
        "    CMD.selectNode(n.id);",
        "click to clear", 1); ok &= o

    # The stats strip key describes the CLAIM TIER, not a confidence score. The
    # parent board graded confidence; this board grades evidence, and the two are
    # different claims about the same colour. Last item from the handoff's shell
    # spec.
    s, o = must_replace(s, "Confidence key", "Claim tier", "claim-tier key label",
                        s.count("Confidence key")); ok &= o

    # ---- the KPI cells are the most-looked-at thing on the page and were inert
    # Each maps to the filter a reader would otherwise have to hunt for in the rail.
    s, o = must_replace(s,
        "k.map(([l,v,u,c])=>'<div class=\"kpi\">",
        "k.map(([l,v,u,c])=>'<div class=\"kpi\"'+(KPI_FILTER[l]?' data-kpi=\"'+KPI_FILTER[l]"
        "+'\"'+(S.filters.has(KPI_FILTER[l])?' class=\"kpi on\"':''):'')+'>",
        "clickable KPI cells", 1); ok &= o

    s, o = must_replace(s, "function renderStats(){",
        "/* Which rail filter each KPI cell stands for. A reader who clicks the big\n"
        "   number expects it to do what the number describes; leaving it inert makes\n"
        "   the most prominent element on the page the only dead one. */\n"
        "const KPI_FILTER = { 'TIER A':'tier-A', 'CUSTODY':'C3', 'DENIALS':'denied' };\n"
        "function renderStats(){", "KPI filter map", 1); ok &= o

    # ---- pane collapse. The rail already has one; the dock did not.
    s, o = must_replace(s,
        "document.addEventListener('click', ev => {\n"
        "  if (ev.target.closest('[data-dockw]')){",
        "document.addEventListener('click', ev => {\n"
        "  const kp = ev.target.closest('[data-kpi]');\n"
        "  if (kp){ CMD.toggleFilter(kp.getAttribute('data-kpi')); return; }\n"
        "  if (ev.target.closest('[data-dockoff]')){\n"
        "    S.dockOff = !S.dockOff;\n"
        "    document.getElementById('app').classList.toggle('dock-off', S.dockOff);\n"
        "    renderDock(); return;\n"
        "  }\n"
        "  /* The open state's way back to the spine. Its twin is the spine\n"
        "     itself, which is one big click target -- see the #dock.dock-spine\n"
        "     handler in the map module. */\n"
        "  if (ev.target.closest('[data-dockfold]')){\n"
        "    S.dockSpine = true; renderDock(); return;\n"
        "  }\n"
        "  if (ev.target.closest('[data-dockw]')){",
        "KPI + dock-collapse handlers", 1); ok &= o

    # (the dock-hide chevron used to be appended here; see the note above)

    s, o = must_replace(s,
        "  d.classList.toggle('open', !!S.sel);\n  setDockOpen(!!S.sel && !S.dockCollapsed);",
        "  d.classList.toggle('open', !!S.sel);\n"
        "  /* THE RULE, 27 August 2026. The dossier is OUT when there is\n"
        "     something to read and folded to its spine otherwise. Stewart:\n"
        "     \"the bar popping up if something is clicked on the map. This way\n"
        "     the right bar retracts and we get to see the whole map up front.\"\n"
        "     Before this the dock shipped OPEN with nothing selected, showing a\n"
        "     paragraph of placeholder prose in ~290px the map wanted.\n"
        "     Keyed on a CHANGE of selection, not on its value, so either tab\n"
        "     overrides the rule and the override survives until the reader\n"
        "     picks something else. */\n"
        "  if (S.sel !== S._dockLastSel){ S.dockSpine = !S.sel; S._dockLastSel = S.sel; }\n"
        "  const spined = !!S.dockSpine && !S.dockOff;\n"
        "  setDockOpen(!spined && !!S.sel && !S.dockCollapsed && !S.dockOff);\n"
        "  /* AFTER setDockOpen, which writes --dock-w itself. Two owners of one\n"
        "     custom property is how the first fold silently did nothing. */\n"
        "  d.classList.toggle('dock-spine', spined);\n"
        "  d.style.width = '';\n"
        "  if (spined) document.documentElement.style.setProperty('--dock-w','30px');\n"
        "  let tab = document.querySelector('.dock-show');\n"
        "  if (S.dockOff && !tab){\n"
        "    tab = el('button','dock-show','&laquo;');\n"
        "    tab.setAttribute('data-dockoff','1');\n"
        "    tab.title = 'Show the detail pane';\n"
        "    document.body.appendChild(tab);\n"
        "  } else if (!S.dockOff && tab){ tab.remove(); }\n"
        "  let fold = document.querySelector('.dock-fold');\n"
        "  if (!spined && !S.dockOff){\n"
        "    if (!fold){\n"
        "      fold = el('button','dock-fold','<b>DOSSIER \\u2014 CLICK TO CLOSE</b>');\n"
        "      fold.setAttribute('data-dockfold','1');\n"
        "      fold.title = 'Fold the dossier back to its spine';\n"
        "      document.body.appendChild(fold);\n"
        "    }\n"
        "  } else if (fold){ fold.remove(); }",
        "dock re-open tab", 1); ok &= o

    # ---- the analyst fold, on the dossier's curve.
    # `display:none` is not an interpolable property, so the analyst console
    # vanished between two frames while the dossier beside it slid on a 320ms
    # ease. One shell, two manners. Stewart, 27 August: "Add the same animation
    # curve etc to collapsing the analyst".
    s, o = must_replace(s,
        "  $('#anscroll').style.display = S.anOpen ? '' : 'none';\n"
        "  $('#ansugg').style.display = S.anOpen ? '' : 'none';",
        "  /* A CLASS, so the fold can be animated. Setting display back to '' here\n"
        "     would also defeat the transition -- a display change forces the new\n"
        "     box immediately and there is nothing to interpolate from. The two\n"
        "     children keep their boxes and lose their height instead. */\n"
        "  const anEl = document.querySelector('.analyst');\n"
        "  if (anEl) anEl.classList.toggle('an-collapsed', !S.anOpen);",
        "analyst fold as a class", 1); ok &= o

    # ---- stage 3: entry surface (C) and focus on select (D) ---------------
    s, o = must_replace(s, "</style>", L0_CSS3 + "</style>", "L0 stage-3 styles",
                        s.count("</style>")); ok &= o
    s, o = must_replace(s, "const CMD = {", L0_JS3 + "\nconst CMD = {",
                        "L0 stage-3 module", 1); ok &= o
    # Anchor on stable text inside L0_CMD rather than composing the block as a
    # literal: an earlier patch rewrites expand()'s body, so L0_CMD no longer
    # matches the file it was inserted into.
    s, o = must_replace(s, "  showPathOnly(){", L0_CMD3 + "  showPathOnly(){",
                        "entry path commands", 1); ok &= o
    s, o = must_replace(s,
        "  l0open:[], l0panel:null, l0full:false, dockOff:false,\n};",
        "  l0open:[], l0panel:null, l0full:false, dockOff:false,\n"
        "  /* l0entry starts FALSE, changed 27 August 2026. It started TRUE on the\n"
        "     reasoning that a stranger should land on a question rather than a\n"
        "     hairball -- but the board is no longer a hairball, it is a packed\n"
        "     grid, and Design settled this on 26 August: \"Entry is therefore\n"
        "     'here is all of it', not 'here is where we think you should\n"
        "     start'. The 14 start-here flags stay available, but as an offer\n"
        "     inside a board you have already seen whole.\"\n"
        "\n"
        "     Stewart, 27 August, on the live deploy: \"It loads to this screen\"\n"
        "     -- the screen being the six cards, with the map behind them unseen.\n"
        "     The cards are one click away on the START chip and CMD.showEntry();\n"
        "     nothing is lost by not showing them first. */\n"
        "  l0entry:false, l0path:null, l0focus:null,\n"
        "  /* The dossier starts folded. See renderDock for the rule. */\n"
        "  dockSpine:true, _dockLastSel:null,\n};",
        "entry state", 1); ok &= o

    # the entry surface mounts over the map, and the map keeps running behind it
    s, o = must_replace(s,
        "  measure();\n  const fk = fitScale();",
        "  renderL0Entry(host);\n  measure();\n  const fk = fitScale();",
        "mount the entry surface", 1); ok &= o
    s, o = must_replace(s,
        "    renderSelBar(); startLoop();",
        "    renderSelBar(); renderL0Entry(host); startLoop();",
        "repaint includes the entry surface", 1); ok &= o

    # card + skip clicks
    s, o = must_replace(s,
        "  host.addEventListener('click', ev => {\n    const c = ev.target.closest('[data-close]');",
        "  host.addEventListener('click', ev => {\n"
        "    const pc = ev.target.closest('[data-path]');\n"
        "    if (pc) return CMD.openPath(pc.getAttribute('data-path'));\n"
        "    if (ev.target.closest('[data-skip]')){ S.l0entry = false; repaint(); return; }\n"
        "    const c = ev.target.closest('[data-close]');",
        "entry card clicks", 1); ok &= o

    # D: focus. A selected node dims everything not on its thread; an open path
    # dims everything outside the path.
    s, o = must_replace(s,
        "    const dim = S.l0open.length ? 0.16 : 1;\n    const lit = new Set(S.l0open);",
        "    /* Focus (D). Selection dims to the one-hop thread; an entry path dims\n"
        "       to the path. Without it, following a connection means tracing one\n"
        "       orthogonal line across a field of 313 others. */\n"
        "    const focus = S.l0focus || (S.sel && byId[S.sel] ? l0FocusSet(S.sel) : null);\n"
        "    const dim = (S.l0open.length || focus) ? 0.16 : 1;\n"
        "    const lit = focus ? new Set(focus) : new Set(S.l0open);",
        "focus set drives the dim", 1); ok &= o

    # the breadcrumb gains the path chip and a way back to the entry surface
    s, o = must_replace(s,
        "    if (S.l0open.length) h += '<span class=\"l0chip\" data-clear=\"1\">CLEAR",
        "    if (S.l0path){\n"
        "      const p = (L0DATA.entryPaths||[]).find(x=>x.id===S.l0path);\n"
        "      if (p) h += '<span class=\"l0chip path\" data-clearpath=\"1\">'\n"
        "        + esc(p.label) + ' <span class=\"n\">' + p.onMap + '</span>'\n"
        "        + ' <span class=\"x\">&times;</span></span>';\n"
        "    }\n"
        "    h += '<span class=\"l0chip\" data-entry=\"1\">START</span>';\n"
        "    if (S.l0open.length) h += '<span class=\"l0chip\" data-clear=\"1\">CLEAR",
        "path chip + START", 1); ok &= o
    s, o = must_replace(s,
        "    if (ev.target.closest('[data-clear]')) return CMD.clearExpansions();",
        "    if (ev.target.closest('[data-clearpath]')) return CMD.clearPath();\n"
        "    if (ev.target.closest('[data-entry]')) return CMD.showEntry();\n"
        "    if (ev.target.closest('[data-clear]')) return CMD.clearExpansions();",
        "path chip handlers", 1); ok &= o

    # -- expose the model on the debug surface the screenshotter already uses, so
    #    the L0 checks can be made AT RUNTIME. This board has been bitten twice by
    #    patches that read correctly and did not take effect.
    # l0Fit is exposed for the same reason CMD and L0DATA are: so a check can call
    # the renderer's OWN truncation rather than a copy of it. A check that
    # reimplements the thing it is checking passes when the renderer diverges.
    s, o = must_replace(s, "window.__board = { CMD, S,",
                        "window.__board = { CMD, S, L0DATA, mountL0, l0Fit,",
                        "L0 debug export", 1); ok &= o

    # -- the inherited hop/legend chrome belongs to the full-graph map, and its
    #    INSIGHTS() reads MAP.pairs. The L0 map draws its own chrome (breadcrumb,
    #    registers, view controls), so the old one is suppressed rather than left
    #    to throw inside paint() -- which took the ledger and the register panel
    #    down with it, silently, because paint catches.
    s, o = must_replace(s,
        "function renderNetworkChrome(){\n  const c = $('#netchrome'); if (!c) return;",
        "function renderNetworkChrome(){\n  const c = $('#netchrome'); if (!c) return;\n"
        "  if (!S.l0full){ c.innerHTML = ''; return; }",
        "suppress legacy network chrome under L0", 1); ok &= o

    # -- paint() routes map work through its 'camera' step. The L0 surfaces
    #    (ledgers, breadcrumb, register panel) are repainted there rather than by
    #    remounting, because remounting would rebuild the canvas and lose the
    #    reader's pan -- and because nodes never moving is the property that makes
    #    two open ledgers comparable.
    #
    #    AND THE GUARD NAMES BOTH MAP VIEWS. It said NETWORK only, which was right
    #    while the packed map WAS the network rest state. Moving it to a view of its
    #    own without widening this would have stopped every repaint on that tab: the
    #    breadcrumb, the ledgers and the register panel would have frozen at whatever
    #    they said when the tab was opened, while the canvas kept drawing. Nothing
    #    would have thrown.
    s, o = must_replace(s,
        "  step('camera', () => {\n    if (S.view === 'NETWORK' && MAP){",
        "  step('camera', () => {\n"
        "    if ((S.view === 'NETWORK' || S.view === 'PROGRAM') && MAP){\n"
        "      if (MAP.repaint && !S.l0full){ MAP.repaint(); return; }",
        "L0 repaint on paint()", 1); ok &= o
    # -- THE FULL GRAPH'S PARTICLE LAYER, which is an inherited surface asserting
    #    something this board does not claim. mountNetwork mounts when S.path or
    #    S.frame is set and the NETWORK view is CONSTRUCTED -- reachable from any
    #    other view via highlightPath, focusCluster, frameNodes or showInsight --
    #    and it drew a particle on every visible edge, flipped by
    #    `new Date(s.date) > new Date(t.date)`.
    #
    #    That is a time-direction flow on every line, the exact treatment Claude
    #    Design named and rejected: "It states that the relationship runs from the
    #    earlier node to the later one, and for most of these edges the board makes
    #    no such claim. A moving dot is a far stronger implication than a static
    #    line." The L0 map was built to that rule; the inherited renderer never was.
    #
    #    Same rule as mountL0 now: a particle only where the direction is attested.
    #    On the full graph the one attested case is an edge of the SELECTED node,
    #    running away from the end the reader is standing on. No selection, no
    #    motion.
    s, o = must_replace(s,
        "function drawParticle2D(ctx, e, t){\n"
        "  if (e.alpha < 0.25) return;",
        "function drawParticle2D(ctx, e, t){\n"
        "  if (e.alpha < 0.25) return;\n"
        "  /* MOTION ONLY WHERE ATTESTED. See tools/l0_patches.py. */\n"
        "  const sel = S.sel;\n"
        "  if (!sel) return;\n"
        "  const pa = e.pair && e.pair.s && e.pair.s.id, pb = e.pair && e.pair.t && e.pair.t.id;\n"
        "  if (pa !== sel && pb !== sel) return;",
        "full graph: particles only on the selected node's edges", 1); ok &= o
    s, o = must_replace(s,
        "  const [px,py] = walk(e.pts, e.pair.flip ? 1-u : u);",
        "  /* Away from the reader, never along the time axis. e.pair.flip is left\n"
        "     in place for the tick layer but must never steer a particle. */\n"
        "  const [px,py] = walk(e.pts, pa === sel ? u : 1-u);",
        "full graph: particle direction is the reader's end, not the date", 1); ok &= o

    # -- THE SEARCH GRAMMAR. Design specified key:value filters and `via:`; the
    #    parent board shipped a plain substring match, so `via:bigelow` came back
    #    "0 of 956 entities" -- an answer about the board rather than about the
    #    query. The no-result state also never said what it had NOT searched.
    s, o = must_replace(s, "function viewSearch(v){",
        L0_SEARCH_JS + "function viewSearch(v){",
        "search grammar helper", 1); ok &= o
    s, o = must_replace(s,
        "  const hits = q\n"
        "    ? pool.filter(n => (n.label+' '+(n.sub||'')+' '+(n.loc||'')+' '+"
        "(n.narrative||'')).toLowerCase().includes(q))\n"
        "    : pool.slice(0, 9);",
        "  const hits = q ? l0Search(pool, S.query.trim()) : pool.slice(0, 9);",
        "search uses the grammar", 1); ok &= o
    s, o = must_replace(s,
        "'<div style=\"font-size:11.5px;color:var(--text-dim);padding:14px 0\">"
        "No entity matches that query.</div>'",
        "'<div style=\"font-size:11.5px;color:var(--text-dim);padding:14px 0\">"
        "No entity matches that query.<br><span style=\"color:var(--text-faint)\">"
        "Searched all ' + pool.length + ' entities. '"
        " + ((((window.__board&&window.__board.L0DATA)||{}).l0||[]).length"
        "     ? 'Filters that name a place on the map \u2014 band: era: flag: isolated: role: '"
        "     + '\u2014 only reach the ' + (((window.__board&&window.__board.L0DATA)||{}).l0||[]).length"
        "     + ' nodes above the connectivity floor, not the '"
        "     + (pool.length - (((window.__board&&window.__board.L0DATA)||{}).l0||[]).length) + ' below it.' : '')"
        " + '</span></div>'",
        "no-result state names what it did not search", 1); ok &= o
    # -- DEEP LINKS. `?sel=aawsap` already carried the state; a path is what
    #    survives being pasted into a message. Read accepts both so nothing that
    #    was ever copied breaks; write prefers the path only when the state is a
    #    plain single selection, because a path that drops half the state is
    #    worse than an ugly URL that keeps it.
    s, o = must_replace(s, "let urlSyncable = true;",
        L0_DEEPLINK_JS + "let urlSyncable = true;",
        "deep link helpers", 1); ok &= o
    s, o = must_replace(s,
        "  const s = q.toString();\n"
        "  try {\n"
        "    history.replaceState(null, \'\', s ? \'?\' + s : location.pathname);",
        "  const s = q.toString();\n"
        "  /* The plain single-selection case, and only that one. */\n"
        "  const bare = S.sel && S.view === \'NETWORK\' && !S.query && !S.path\n"
        "    && S.hops === 1 && !S.filters.size && S.tab === \'DOSSIER\'\n"
        "    && S.edgeTypes.size === ALL_EDGE_TYPES.length;\n"
        "  try {\n"
        "    history.replaceState(null, \'\',\n"
        "      bare ? \'/node/\' + encodeURIComponent(S.sel)\n"
        "           : (s ? \'/?\' + s : \'/\'));",
        "writeUrl emits a path for a bare selection", 1); ok &= o
    s, o = must_replace(s,
        "  const p = q.get(\'p\');\n"
        "  if (p && p.includes(\'>\')){\n"
        "    const [a,b] = p.split(\'>\');\n"
        "    if (NODES.some(n=>n.id===a) && NODES.some(n=>n.id===b)) S.path = computePath(a,b,4);\n"
        "  }\n"
        "  urlLock = false;",
        "  const p = q.get(\'p\');\n"
        "  if (p && p.includes(\'>\')){\n"
        "    const [a,b] = p.split(\'>\');\n"
        "    if (NODES.some(n=>n.id===a) && NODES.some(n=>n.id===b)) S.path = computePath(a,b,4);\n"
        "  }\n"
        "  /* A path segment is more explicit than a query param, so it wins. */\n"
        "  const R = l0ReadPath();\n"
        "  if (R){\n"
        "    if (R.kind === \'path\'){\n"
        "      if (NODES.some(n=>n.id===R.from) && NODES.some(n=>n.id===R.to))\n"
        "        S.path = computePath(R.from, R.to, 4);\n"
        "    } else if (R.kind === \'node\'){\n"
        "      if (NODES.some(n=>n.id===R.value)){ S.sel = R.value; S.view = \'NETWORK\'; }\n"
        "    } else if (R.kind === \'q\'){\n"
        "      S.query = R.value; S.view = \'SEARCH\';\n"
        "    } else {\n"
        "      /* band: and era: are search filters, so route them through the grammar\n"
        "         rather than inventing a second way to express the same thing. */\n"
        "      S.query = R.kind + \':\' + R.value; S.view = \'SEARCH\';\n"
        "    }\n"
        "  }\n"
        "  urlLock = false;",
        "readUrl accepts path segments", 1); ok &= o
    # -- THE ANALYST, VIA THE WORKER. The board called api.anthropic.com straight
    #    from the browser with the reader's own key in localStorage, which is right
    #    for a file you double-click and wrong for a URL you send to someone: none
    #    of them has a Console key, so every one of them gets the scripted branches
    #    and the line "no API key configured".
    #
    #    So: a reader's own key still wins where they have set one, because it is
    #    their key and their choice. Otherwise the board asks the same origin, and
    #    only falls back to scripted replies when there is no endpoint either.
    s, o = must_replace(s,
        "  const key = store.get('program.apiKey');\n"
        "  if (!key){ scriptedReply(text); return; }",
        "  const key = store.get('program.apiKey');\n"
        "  if (!key && !S.analystEndpoint){ scriptedReply(text); return; }",
        "analyst falls back to scripted only when there is no endpoint either", 1); ok &= o
    s, o = must_replace(s,
        "    const r = await fetch('https://api.anthropic.com/v1/messages', {\n"
        "      method:'POST',\n"
        "      headers:{ 'content-type':'application/json', 'x-api-key':key,\n"
        "                'anthropic-version':'2023-06-01', "
        "'anthropic-dangerous-direct-browser-access':'true' },\n"
        "      body: JSON.stringify(body),\n"
        "    });",
        "    /* The Worker pins the model, the ceiling and the effort itself, so it\n"
        "       is sent only what it needs and cannot be talked into more. */\n"
        "    const viaWorker = !key && S.analystEndpoint;\n"
        "    const r = viaWorker\n"
        "      ? await fetch(S.analystEndpoint, {\n"
        "          method:'POST',\n"
        "          headers:{ 'content-type':'application/json' },\n"
        "          body: JSON.stringify({ system: body.system, messages: body.messages }),\n"
        "        })\n"
        "      : await fetch('https://api.anthropic.com/v1/messages', {\n"
        "          method:'POST',\n"
        "          headers:{ 'content-type':'application/json', 'x-api-key':key,\n"
        "                    'anthropic-version':'2023-06-01', "
        "'anthropic-dangerous-direct-browser-access':'true' },\n"
        "          body: JSON.stringify(body),\n"
        "        });",
        "analyst routes through the Worker when the reader has no key", 1); ok &= o
    # discover the endpoint once, on load, so the status line tells the truth
    s, o = must_replace(s,
        "S.hasKey = !!store.get('program.apiKey');",
        "S.hasKey = !!store.get('program.apiKey');\n"
        "/* Ask once whether this deployment has a live analyst. A file opened from\n"
        "   disk has no origin to ask, so this fails fast and the board keeps its\n"
        "   scripted behaviour -- the offline artifact must never regress. */\n"
        "S.analystEndpoint = null;\n"
        "if (location.protocol === 'http:' || location.protocol === 'https:'){\n"
        "  fetch('/api/analyst/health').then(r => r.ok ? r.json() : null).then(j => {\n"
        "    if (j && j.live){ S.analystEndpoint = '/api/analyst';\n"
        "      if (typeof renderAnalystChrome === 'function') renderAnalystChrome(); }\n"
        "  }).catch(() => {});\n"
        "}",
        "discover the analyst endpoint on load", 1); ok &= o
    s, o = must_replace(s,
        "    st.textContent = 'no API key configured -- running scripted replies. "
        "The dashboard stays fully usable by hand.';",
        "    st.textContent = S.analystEndpoint\n"
        "      ? 'analyst live on this deployment. No key needed.'\n"
        "      : 'no API key configured -- running scripted replies. "
        "The dashboard stays fully usable by hand.';",
        "status line reflects a live endpoint", 1); ok &= o

    # ---- the left rail gets the dock's two-directional fold -------------------
    # Stewart, 27 August: "same with the left pane, then I should be able to open
    # the closed drawer by clicking it to expand". applyChrome is the one place
    # that knows the rail's state, so the tab is owned here rather than by a
    # second listener guessing at it -- two owners of one piece of chrome is the
    # bug the dock's --dock-w comment already records.
    s, o = must_replace(s,
        "  rb.title = (S.railOpen ? 'Collapse' : 'Expand') + ' the left rail';\n"
        "}",
        "  rb.title = (S.railOpen ? 'Collapse' : 'Expand') + ' the left rail';\n"
        "  /* THE TAB ON THE OPEN STATE. The collapsed spine is one big click\n"
        "     target and carries its own label in CSS; the open state had only the\n"
        "     toolbar button, which is nowhere near the edge the reader is looking\n"
        "     at. Same component as .dock-fold, mirrored across the window. */\n"
        "  let rf = document.querySelector('.rail-fold');\n"
        "  if (S.railOpen && !rf){\n"
        "    rf = document.createElement('button');\n"
        "    rf.className = 'rail-fold';\n"
        "    rf.innerHTML = '<b>FILTERS \\u2014 CLICK TO CLOSE</b>';\n"
        "    rf.title = 'Collapse the left rail';\n"
        "    rf.setAttribute('data-railfold', '1');\n"
        "    document.body.appendChild(rf);\n"
        "  } else if (!S.railOpen && rf){ rf.remove(); }\n"
        "}",
        "rail fold tab on the open state", 1); ok &= o

    # Both directions, on the document, because the rail's insides are rebuilt by
    # renderRail and a handler bound to a child would not survive it.
    s, o = must_replace(s,
        "function applyChrome(){",
        "document.addEventListener('click', ev => {\n"
        "  if (ev.target.closest('[data-railfold]')){\n"
        "    S.railOpen = false; applyChrome(); return;\n"
        "  }\n"
        "  /* The spine itself, anywhere on it. Guarded on rail-off so a click in\n"
        "     the open rail's empty space does not fold it under the reader. */\n"
        "  const app = document.getElementById('app');\n"
        "  if (app && app.classList.contains('rail-off') && ev.target.closest('.rail')){\n"
        "    S.railOpen = true; applyChrome(); return;\n"
        "  }\n"
        "});\n"
        "function applyChrome(){",
        "rail spine and tab click handlers", 1); ok &= o
    return s, ok


# ===========================================================================
# Stage 2 — selection, the sliding dock, and the entity dossier.
#
# Stewart's review of the first build overrode three things the design handoff
# specified, and the overrides are right:
#
#   * Multi-open ledgers were the handoff's model ("comparison is the point").
#     In use it means you cannot unclick, there is no visible way out, and
#     clicking a second node does not take you anywhere. Selection is now SINGLE
#     and global. Multi-open survives only on the CMD line, where an analyst who
#     actually wants two ledgers can still ask for them.
#   * The dossier dock was a 306px strip, which is not a reading measure. It now
#     animates out to half the viewport on selection.
#   * L0 nodes had no dossier of their own, so clicking MITRE gave you a list of
#     its members and no argument. The entity dossier is now the PRIMARY content
#     and the member ledger is secondary. That inverts the handoff's emphasis on
#     purpose.
# ===========================================================================

L0_CSS2 = """
/* dock: a reading measure on selection, a strip otherwise ------------------ */
/* THE SLIDE, ON THE THING THAT ACTUALLY MOVES.
   `.dock{transition:width}` sat here since the fold landed and never once ran. The
   dock is a grid CHILD: its width comes from the `.body` track `var(--dock-w)`, so
   the element's own width property is never what changes and there is nothing for a
   width transition to interpolate. The panel snapped, every time.

   Transitioning `.body{grid-template-columns}` instead got closer and was still
   wrong, and this is the part worth remembering: an UNREGISTERED custom property
   has no type, so `--dock-w` flips 30px -> 800px discretely and the track it feeds
   has nothing to interpolate between. Measured, sampling every frame: 30 -> 762 in
   one frame, then 762 -> 800 over the following 140ms. A 95% jump with a polite
   settle on the end is not a slide, and it would have shipped looking like one had
   nobody sampled it.

   @property gives the custom property a <length> type, and a typed custom property
   animates. Then the track follows it, the map's right edge follows the track, and
   the whole shell moves as one thing. easeOutQuint: leaves fast, arrives soft. */
@property --dock-w { syntax:'<length>'; inherits:true; initial-value:306px; }
:root{transition:--dock-w 320ms cubic-bezier(.22,1,.36,1)}
.dock.dock-wide{max-width:none}
/* THE TAB ON THE OPEN STATE. The spine has carried "DOSSIER - CLICK TO OPEN" since
   the fold landed, but the open state had only an 11px chevron, so the way back was
   invisible. Stewart, 27 August: "that tab needs to exist on the open version too
   so you can click it and it slides back in." Same type, same letter-spacing, same
   rotation as the spine label -- one visual idea in two directions.
   position:FIXED and pinned to --dock-w rather than absolute inside the dock,
   because `.dock{overflow-x:hidden}` would clip a child hanging off its left edge.
   It transitions `right` on the same curve, so the tab rides the panel instead of
   teleporting to meet it. */
.dock-fold{position:fixed;right:calc(var(--dock-w) - 1px);top:50%;
  transform:translateY(-50%);z-index:33;width:18px;height:168px;
  background:#141920;border:1px solid #262e36;border-right:none;
  border-radius:3px 0 0 3px;color:#8d97a4;cursor:pointer;padding:0;
  display:flex;align-items:center;justify-content:center;
  transition:color 140ms linear,border-color 140ms linear}
.dock-fold b{writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;
  font:500 8.5px/1 'IBM Plex Mono',monospace;letter-spacing:.18em;font-weight:500}
.dock-fold:hover{color:#5ed4e6;border-color:#3b444f}
#dock{transition:none}
/* THE ANALYST FOLD, on the dossier's curve and duration, so the two panels that
   frame the map behave like one shell. max-height rather than height because the
   transcript has no fixed height -- it grows with the conversation, which is the
   whole point of it -- and max-height interpolates from a number to zero without
   anyone having to measure the content first. The generous open value on the
   suggestion row is the standard max-height trick: it only ever clips if the chips
   need more than 400px, and it reaches full size early rather than late. */
#anscroll,#ansugg{overflow:hidden;
  transition:max-height 320ms cubic-bezier(.22,1,.36,1),
             opacity 170ms linear,
             padding-top 320ms cubic-bezier(.22,1,.36,1),
             padding-bottom 320ms cubic-bezier(.22,1,.36,1)}
#ansugg{max-height:400px}
.analyst.an-collapsed #anscroll,
.analyst.an-collapsed #ansugg{
  max-height:0;opacity:0;padding-top:0;padding-bottom:0;border-top-width:0}
@media (prefers-reduced-motion:reduce){
  :root,.dock-fold,#anscroll,#ansugg{transition:none}
}
.dock-toggle{position:absolute;left:-11px;top:50%;transform:translateY(-50%);
  z-index:32;width:22px;height:46px;background:#141920;border:1px solid #262e36;
  border-right:none;color:#8d97a4;cursor:pointer;font:500 11px/44px 'IBM Plex Mono',monospace;
  text-align:center;padding:0}
.dock-toggle:hover{color:#5ed4e6;border-color:#3b444f}
.edoss{padding:0 12px 14px;max-width:100%;box-sizing:border-box;overflow-wrap:break-word;word-break:break-word}
.dock{overflow-x:hidden}
.dock>*{max-width:100%;box-sizing:border-box}
.edoss *{max-width:100%;box-sizing:border-box;overflow-wrap:break-word}
.edoss .why{margin:0 0 10px;padding:9px 11px;background:#141920;
  border-left:2px solid #5ed4e6;font:400 11px/1.65 'IBM Plex Mono',monospace;
  color:#dfe4ea}
.edoss .roles{display:flex;flex-wrap:wrap;gap:4px;margin:0 0 10px}
/* The image block. A portrait crops to a circle; a MARK does not -- it is
   contain-fitted in a square with a hairline, because an institutional seal
   cropped to a circle is a different mark and several carry statutory
   restrictions on alteration stricter than copyright. Same rule as the chip. */
.edoss .edossimg{margin:0 0 12px;display:flex;align-items:flex-start;gap:10px}
.edoss .edossimg img{width:72px;height:72px;flex:0 0 72px;object-fit:cover;
  border-radius:50%;border:1px solid #333c47;background:#141920}
.edoss .edossimg.mark img{object-fit:contain;border-radius:2px;padding:4px}
.edoss .edossimg figcaption{font:400 9px/1.55 'IBM Plex Mono',monospace;
  color:#8d97a4;letter-spacing:.04em;padding-top:2px}
.edoss .edossimg .ask{margin-top:6px;padding:6px 8px;border:1px solid #4a3c1c;
  background:#1a1710;font:400 9.5px/1.6 'IBM Plex Mono',monospace;color:#c9b880}
.edoss .edossimg .ask .eyebrow{color:#efb555}
.edoss .role{padding:2px 6px;border:1px solid #333c47;color:#8d97a4;
  font:500 8.5px/1.5 'IBM Plex Mono',monospace;letter-spacing:.13em;text-transform:uppercase}
.edoss .narr{font:400 11.5px/1.75 'IBM Plex Mono',monospace;color:#b9c2cd;
  white-space:pre-wrap;overflow-wrap:break-word;word-break:break-word;margin:0 0 12px}
.edoss .dn{margin:0 0 12px;padding:8px 11px;border:1px solid #3b2b2b;
  background:#1a1416;font:400 10.5px/1.6 'IBM Plex Mono',monospace;color:#e8b0a6}
.edoss .cl{padding:6px 0;border-top:1px solid #1d242b;
  font:400 10.5px/1.6 'IBM Plex Mono',monospace;color:#b9c2cd}
.edoss .cl .t{display:inline-block;min-width:44px;font-size:8.5px;letter-spacing:.13em}
.edoss .cl a{color:#5c6672;font-size:9px;word-break:break-all;text-decoration:none}
.edoss .cl a:hover{color:#5ed4e6}
.t1{color:#5ed4e6}.t2{color:#efb555}.t3{color:#8d97a4}
.kpi[data-kpi]{cursor:pointer}
.kpi[data-kpi]:hover{background:#141920}
.kpi[data-kpi].on{background:#141920;box-shadow:inset 0 -2px 0 #5ed4e6}
.dock-hide{position:absolute;left:-11px;top:calc(50% + 52px);transform:translateY(-50%);
  z-index:32;width:22px;height:46px;background:#141920;border:1px solid #262e36;
  border-right:none;color:#8d97a4;cursor:pointer;font:500 11px/44px 'IBM Plex Mono',monospace;
  text-align:center;padding:0}
.dock-hide:hover{color:#5ed4e6;border-color:#3b444f}
.dock-off .dock{width:0 !important;border-left:none;overflow:hidden}
.dock-show{position:fixed;right:0;top:50%;transform:translateY(-50%);z-index:33;
  width:22px;height:46px;background:#141920;border:1px solid #262e36;border-right:none;
  color:#8d97a4;cursor:pointer;font:500 11px/44px 'IBM Plex Mono',monospace;text-align:center}
.dock-show:hover{color:#5ed4e6}
.auth{margin:0 0 10px;padding:9px 11px;background:#141920;border-left:2px solid #a795e8;
  font:400 10.5px/1.65 'IBM Plex Mono',monospace;color:#dfe4ea}
.auth .eb{font:500 8.5px/1 'IBM Plex Mono',monospace;letter-spacing:.13em;
  text-transform:uppercase;color:#a795e8;display:block;margin-bottom:5px}
.auth .ins{color:#5c6672;font-size:9px;display:block;margin-top:5px}
.auth .thin{color:#efb555;display:block;margin-top:6px}

/* ---- THE LEFT RAIL, AS THE DOCK'S TWIN ---------------------------------------
   Stewart, 27 August: "same with the left pane, then I should be able to open the
   closed drawer by clicking it to expand."

   The rail had none of it. `#app.rail-off .rail{display:none}` is the analyst-fold
   mistake for the third time in this shell: display is NOT interpolable, so the
   pane vanished between frames however good the easing on either side of it. And
   `#app.rail-off .body` dropped the rail TRACK entirely, so even a width animation
   would have had nothing to run against -- the grid went from three columns to two
   in one step.

   So the rail now does exactly what the dock does: the track always exists, the
   width is a REGISTERED length that animates, and the collapsed state is a 30px
   spine carrying its own label rather than an absence. Same curve, same 30px, same
   two-directional affordance -- the shell should not have two ideas about what a
   folded panel is. */
@property --rail-w { syntax:'<length>'; inherits:true; initial-value:202px; }
#app{transition:--rail-w 320ms cubic-bezier(.22,1,.36,1)}
/* Beat ref's `display:none` and its two-column override. Same selectors, later in
   the cascade, so the track survives and the pane has something to animate. */
#app.rail-off{--rail-w:30px}
#app.rail-off .rail{display:grid;overflow:hidden;cursor:pointer;position:relative;
  border-right:1px solid #262e36}
#app.rail-off .rail > *{display:none}
#app.rail-off .rail::after{content:'FILTERS \2014 CLICK TO OPEN';position:absolute;
  left:50%;top:50%;transform:translate(-50%,-50%) rotate(180deg);writing-mode:vertical-rl;
  white-space:nowrap;font:500 9px/1 'IBM Plex Mono',monospace;letter-spacing:.16em;
  color:#8d97a4;pointer-events:none}
#app.rail-off .rail:hover::after{color:#5ed4e6}
#app.rail-off .body{grid-template-columns:var(--rail-w) minmax(0,1fr) var(--dock-w)}
@media (max-width:1179px){
  #app.rail-off .body{grid-template-columns:var(--rail-w) minmax(0,1fr)}
}
/* THE TAB ON THE OPEN STATE, mirroring .dock-fold across the window. Fixed and
   pinned to --rail-w for the same reason the dock's is pinned to --dock-w: a child
   hanging off the pane's edge gets clipped by its own overflow. It transitions
   `left` on the panel's curve so the tab rides the edge instead of teleporting. */
.rail-fold{position:fixed;left:calc(var(--rail-w) - 1px);top:50%;
  transform:translateY(-50%);z-index:32;width:22px;height:150px;
  background:#141920;border:1px solid #262e36;border-left:none;color:#8d97a4;
  cursor:pointer;padding:0;display:flex;align-items:center;justify-content:center;
  transition:left 320ms cubic-bezier(.22,1,.36,1),color 120ms linear,
             border-color 120ms linear}
.rail-fold b{writing-mode:vertical-rl;white-space:nowrap;font:500 9px/1 'IBM Plex Mono',monospace;
  letter-spacing:.16em;font-weight:500}
.rail-fold:hover{color:#5ed4e6;border-color:#3b444f}
@media (prefers-reduced-motion:reduce){
  #app,.rail-fold{transition:none}
}
"""

L0_JS2 = r"""
/* Render an entity dossier. This is the argument for why the node is on the map,
   and on this board that argument is the product. The member ledger that used to
   be the whole of a node's content is now the table of contents underneath it. */
/* The derived connection layer. Projected from the board's own hand-written edges
   in build_l0.py, so every row here is a link somebody sourced by hand — nothing
   is generated. Rendered for EVERY node, including the 874 that are not on the
   map, because an agent hunting a join nobody made needs the adjacency stated with
   its tier and its reason attached. */
function renderConnections(id){
  const rows = (L0DATA.connections || {})[id] || [];
  if (!rows.length) return '';
  let h = '<div class="eyebrow" style="margin:12px 0 4px">Connections · ' + rows.length + '</div>';
  for (const r of rows){
    h += '<div class="cl l0row" data-node="'+esc(r.id)+'">'
       + '<span class="t t'+r.tier+'">TIER '+r.tier+'</span> '
       + '<b>'+esc(r.label)+'</b> <span class="dg">'+esc(r.type)
       + (r.dir === 'out' ? ' &rarr;' : ' &larr;') + '</span>'
       + (r.why ? '<br>'+esc(r.why) : '')
       + (r.note ? '<br><span class="dg">'+esc(r.note)+'</span>' : '')
       + '</div>';
  }
  return h;
}

/* Structural authority. The board grades on connections, which grades people on
   what they SAID. This states what the office can DO, with the instrument that
   grants it, so an officer with real authority and no public record stops reading
   as unimportant. The empty evidence column is the finding, not a low score. */
function renderAuthority(id){
  const a = (L0DATA.authority || {})[id];
  if (!a) return '';
  const p = a.publicRecord || {};
  const thin = a.weight >= 3 && (p.connections || 0) <= 2;
  return '<div class="auth"><span class="eb">Structural authority · '
    + (a.tense === 'held' ? 'held' : 'holds') + '</span>'
    + esc(a.authority)
    + '<span class="ins">' + a.instruments.map(esc).join(' · ') + '</span>'
    + (thin ? '<span class="thin">Public UAP record: '
        + (p.connections||0) + ' connection(s), ' + (p.denialsIssued||0)
        + ' denial(s) issued on the record'
        + ((p.denialsUndirected||0) ? ' and ' + p.denialsUndirected
             + ' denial link(s) whose direction is not attested' : '')
        + '. This office could answer from position alone, and the '
        + 'record is nearly empty. That absence is the finding, not a low score.</span>' : '')
    + '</div>';
}

function renderEntityDossier(id){
  const n = (L0DATA.l0||[]).find(x=>x.id===id);
  const d = (n && n.dossier) || (L0DATA.dossiers || {})[id];
  if (!d) return '<div class="edoss">' + renderAuthority(id) + renderConnections(id) + '</div>';
  const T = t => '<span class="t t'+t+'">TIER '+t+'</span>';
  let h = '<div class="edoss">' + renderAuthority(id);
  /* The image, and everything the reader is owed about it. Credit is not optional
     decoration -- it is the attribution the licence is conditional on. And an `ask`
     image ships with the specific reason it is ambiguous, printed here rather than
     dropped, so the doubt travels with the picture instead of being resolved
     silently in its favour. The chip carries an amber ring for the same state; this
     is where the sentence lives. */
  if (n && n.photo){
    h += '<figure class="edossimg' + (n.photoKind === 'mark' ? ' mark' : '') + '">'
       + '<img src="' + esc(n.photo) + '" alt="' + esc(n.label || id) + '">'
       + (n.photoCredit ? '<figcaption>' + esc(n.photoCredit) + '</figcaption>' : '')
       + (n.photoClearance === 'ask'
            ? '<div class="ask"><span class="eyebrow">CLEARANCE: ASK</span><br>'
              + esc(n.photoNote || 'clearance ambiguous') + '</div>'
            : '')
       + '</figure>';
  }
  if (d.whatItIs) h += '<div class="narr">'+esc(d.whatItIs)+'</div>';
  if (d.whyImplicated) h += '<div class="why">'+esc(d.whyImplicated)+'</div>';
  if (d.roles && d.roles.length)
    h += '<div class="roles">'+d.roles.map(r=>'<span class="role">'+esc(r)+'</span>').join('')+'</div>';
  if (d.narrative) h += '<div class="narr">'+esc(d.narrative)+'</div>';
  if (d.denialPosture)
    h += '<div class="dn"><span class="eyebrow">DENIAL POSTURE</span><br>'+esc(d.denialPosture)+'</div>';
  if (d.claims && d.claims.length){
    h += '<div class="eyebrow" style="margin:12px 0 4px">Claims · '+d.claims.length+'</div>';
    for (const c of d.claims){
      const src = String(c.source||'');
      const link = /^https?:\/\//.test(src)
        ? '<a href="'+esc(src)+'" target="_blank" rel="noopener">'+esc(src)+'</a>'
        : '<a>'+esc(src)+'</a>';
      h += '<div class="cl">'+T(c.tier)+' '+esc(c.text)+'<br>'+link+'</div>';
    }
  }
  if (d.connections && d.connections.length){
    /* The connection notes are written for the analyst agent, not primarily for a
       human reader: they name who links to whom in plain language so a downstream
       pass can find joins the research never made explicit. */
    h += '<div class="eyebrow" style="margin:12px 0 4px">Connections</div>';
    for (const c of d.connections) h += '<div class="cl">'+esc(c)+'</div>';
  }
  if (d.openQuestions && d.openQuestions.length){
    h += '<div class="eyebrow" style="margin:12px 0 4px">Open questions</div>';
    for (const q of d.openQuestions) h += '<div class="cl">'+esc(q)+'</div>';
  }
  h += renderConnections(id);
  return h + '</div>';
}

/* The dock is a 306px strip at rest and a reading measure when something is
   selected. Floored at 560px so it does not collapse on a laptop, CAPPED at 640
   so it stays a measure, and animated on the shell's own curve rather than
   snapping.

   THE CAP IS THE 27 AUGUST FIX AND HALF THE VIEWPORT WAS NEVER RIGHT.
   Measured, at 11.5px IBM Plex Mono with a 6.9px advance, the running prose ran:

     window   dock    chars/line   map share
     1366     683      95           37%
     1600     800     112           37%
     1920     960     135           39%
     2560    1280     182           42%

   Comfortable measure is 45-75 characters and about 90 is the ceiling for
   sustained reading, so every size busted it and the BIGGER the monitor the
   worse the dossier read -- a proportional width doing the job of a measure.
   That is also the whole of Stewart's "the right bar expands to half the screen
   and you never get to see the full map": the panel was not wide because the
   prose needed it.

   Capping at 640 holds the measure at about 89 characters everywhere and gives
   the map back 40 / 47 / 56 / 67 percent at the four sizes. Both surfaces win,
   which is why this is not the analyst/dossier swap and does not need it. */
function setDockOpen(open){
  const d = document.getElementById('dock');
  if (!d) return;
  /* Set the width ON THE ELEMENT rather than through a CSS variable. --dock-w is
     already written to :root by the inherited resize grip, and racing two
     declarations of the same custom property through different owners is how the
     first attempt at this silently did nothing: the class landed, the width did
     not move, and nothing errored. */
  const wide = Math.min(640, Math.max(560, Math.round(window.innerWidth * 0.5)));
  /* The shell is a CSS GRID and the dock is a grid child whose track is sized by
     --dock-w. Setting width on the ELEMENT makes it wider than its track, so it
     overflows to the right and off-screen: the panel looked wide but every line
     was guillotined at the viewport edge, on both sides. A programmatic
     "does any child overflow its parent" check passed, because the children fit
     the element fine -- it was the element that did not fit the grid.
     Write the custom property the grid actually reads. This is the same owner
     the resize grip uses, which is why it takes. */
  document.documentElement.style.setProperty('--dock-w',
    (open ? wide : (S.dockW || 306)) + 'px');
  d.style.width = '';
  d.classList.toggle('dock-wide', !!open);
  S.dockWide = !!open;
}
"""

L0_CMD2 = r"""
  /* One selection, obeyed everywhere. Selecting from the timeline, a case card or
     a search result clears whatever was open, lights the node on the map, moves the
     camera to it and opens its dossier. Before this, the map kept the previous
     selection and the reader had no way to tell which node the dock was describing. */
  focusL0(id){
    S.l0open = [id];
    S.l0panel = null;
    if (MAP && MAP.focus) MAP.focus(id);
  },
  /* The three packed-layout options, drivable from the chat input. Every control
     on this surface must have a CMD entry or the "drive the whole app from the
     chat input" requirement is broken for it -- the same rule the five original L0
     actions were written to. The first three ship ON; `cells` ships OFF and is the
     only way into the count matrix -- no fit and no zoom will put a reader there. */
  l0opt(which, on){
    if (!MAP || !MAP.opt) return warn('the program map is not mounted');
    const K = { rest:'lines at rest', flags:'start-here pointers', labels:'chip labels',
                cells:'the cell count matrix' };
    if (!K[which]) return warn('l0opt("'+which+'") — options are: '+Object.keys(K).join(', '));
    MAP.opt[which] = (on === undefined) ? !MAP.opt[which] : !!on;
    MAP.repaint();
    pushTurn({ role:'ANALYST',
               text: K[which] + ' ' + (MAP.opt[which] ? 'on' : 'off') + '.' });
  },
"""


# ===========================================================================
# Stage 3 — the entry surface (C) and focus on select (D).
#
# Stewart, on seeing the board cold: "way too busy ... no opportunity for
# discovery, nothing visually identifying what the important connections are."
# He is right, and the cause is that position on this map carries no
# information: x and y are force-layout output, so every node looks equally
# important and arrives in no order.
#
# The real fix is a layout where position means something. It is BUILT, as of
# 25 August 2026: Design's packed-cell layout, signed off by Stewart from the comp
# and drawn by mountL0 above -- eras across, bands down, one chip size for
# everything. These two came first because they needed no design decision, and
# they still earn their place:
#
#   C  an entry surface with six curated ways in, so a stranger lands on a
#      question rather than a hairball
#   D  focus on select, so following a thread dims everything that is not on it
# ===========================================================================

L0_CSS3 = """
/* ---- entry surface ------------------------------------------------------ */
.l0entry{position:absolute;inset:0;z-index:9;overflow:auto;
  background:linear-gradient(160deg,#161a20 0%,#11141a 100%);padding:26px 30px 30px}
.l0entry h2{margin:0 0 4px;font:600 15px/1.3 'IBM Plex Mono',monospace;color:#e6e9ee}
.l0entry .sub{margin:0 0 20px;font:400 11px/1.7 'IBM Plex Mono',monospace;
  color:#8d97a4;max-width:760px}
.l0entry .sub b{color:#b9c2cd;font-weight:500}
.l0cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));
  gap:12px;max-width:1180px}
.l0card{background:#141920;border:1px solid #262e36;padding:13px 14px 12px;
  cursor:pointer;display:flex;flex-direction:column;gap:7px;text-align:left}
.l0card:hover{border-color:#5ed4e6;background:#1a2027}
.l0card h3{margin:0;font:600 12px/1.3 'IBM Plex Mono',monospace;color:#e6e9ee}
.l0card p{margin:0;font:400 10.5px/1.6 'IBM Plex Mono',monospace;color:#8d97a4}
.l0card .n{margin-top:auto;font:500 9px/1 'IBM Plex Mono',monospace;
  letter-spacing:.10em;text-transform:uppercase;color:#5ed4e6}
.l0entry .skip{margin:20px 0 0;font:400 10.5px/1.6 'IBM Plex Mono',monospace;color:#5c6672}
.l0entry .skip button{background:none;border:none;color:#5ed4e6;cursor:pointer;
  font:inherit;padding:0;text-decoration:underline}
.l0chip.path{border-color:#5ed4e6;color:#e6e9ee}
"""

L0_JS3 = r"""
/* The entry surface. Six questions, not six categories: a reader wants to
   "follow the money", not to "filter by funding domain". Counts come from the
   model, computed at build time from the graph, so a card can never advertise
   a number different from what it opens. */
function renderL0Entry(host, onPick){
  const D = L0DATA;
  let e = host.querySelector('.l0entry');
  if (!S.l0entry){ if (e) e.remove(); return; }
  if (!e){ e = el('div','l0entry'); host.appendChild(e); }
  let h = '<h2>The Program</h2>'
    + '<p class="sub">A network of <b>' + D.counts.total + '</b> entities and <b>'
    + (L0DATA.counts.connectionRows/2|0) + '</b> hand-written, individually sourced '
    + 'connections, mapping the legacy recovery and reverse-engineering programme and '
    + 'the modern disclosure movement, 1944-2026. '
    + '<b>' + D.counts.l0 + '</b> of those entities clear the connectivity floor and '
    + 'sit on the map; the rest are reachable by opening one. Pick somewhere to start.</p>'
    + '<div class="l0cards">';
  for (const p of (D.entryPaths||[])){
    h += '<button class="l0card" data-path="'+esc(p.id)+'">'
       + '<h3>'+esc(p.label)+'</h3><p>'+esc(p.blurb)+'</p>'
       + '<span class="n">'+(p.people ? p.total+' people' : p.onMap+' on the map')
       + (p.total > p.onMap && !p.people ? ' · '+p.total+' in all' : '')
       + '</span></button>';
  }
  h += '</div><p class="skip">Or <button data-skip="1">open the whole map</button> '
     + '— ' + (D.counts.l0 + D.counts.directEdges + D.counts.summarisedEdges)
     + ' objects at once, which is a lot to arrive at cold.</p>';
  e.innerHTML = h;
}

/* Focus. Selecting a node dims everything that is not on its thread. Without
   this, following a connection means tracing one orthogonal line across a field
   of 313 others, which is the thing that makes the map feel unusable. */
function l0FocusSet(id){
  const D = L0DATA, keep = new Set([id]);
  for (const r of (D.connections||{})[id] || []) keep.add(r.id);
  for (const e of D.directEdges) {
    if (e.a === id) keep.add(e.b);
    if (e.b === id) keep.add(e.a);
  }
  for (const e of D.summarised) {
    if (e.a === id) keep.add(e.b);
    if (e.b === id) keep.add(e.a);
  }
  return keep;
}
"""

L0_CMD3 = r"""
  /* Each entry path is a real command, so the analyst can take the same route
     from the chat line that a reader takes by clicking a card. */
  openPath(id){
    const p = (L0DATA.entryPaths||[]).find(x=>x.id===id);
    if (!p) return warn('no entry path named "'+id+'"');
    /* An entry path lights cells on the packed map. Typed at the analyst from any
       other view it used to light them on a map that was not mounted. */
    S.view = 'PROGRAM';
    S.l0entry = false;
    S.l0path = id;
    S.l0focus = new Set(p.ids);
    S.l0open = [];
    /* A people path has no cells to light -- its members are witnesses, and the
       map carries 110 entities. Opening the first dossier is the whole gesture. */
    if (p.people && p.ids.length) { CMD.selectNode(p.ids[0]); return; }
    S.sel = null;
    paint({ map:'l0', full:true });
    /* AND THEN FIT. Stewart, 26 August: "when I click a starting point I want it
       to select the relevant cells but then fit to screen." Before this line the
       path lit up wherever the camera happened to be standing, so picking a path
       from a zoomed-in board highlighted seven chips the reader could not see. */
    if (MAP && MAP.fitAll) MAP.fitAll();
  },
  clearPath(){
    S.l0path = null; S.l0focus = null;
    paint({ map:'l0', full:true });
  },
  showEntry(){ S.l0entry = true; S.view = 'PROGRAM'; paint({ full:true }); },
"""
