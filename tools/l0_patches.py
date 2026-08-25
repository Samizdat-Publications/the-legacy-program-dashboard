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

So: L0 owns the rest state, and the legacy full-graph map mounts in its place while
a path or a frame is active, with a FULL GRAPH breadcrumb chip and CLEAR returning
to L0. `selectNode` deliberately does NOT trigger the swap — the ledger is a table
of contents for the dock, and the dock opening must not move the map.

This is an addition to the spec, not an implementation of it. Flagged for sign-off.
"""

# --------------------------------------------------------------------------- CSS
L0_CSS = """
/* ---- L0 program map ---------------------------------------------------- */
.l0wrap{position:absolute;inset:0;overflow:hidden;
  background:linear-gradient(160deg,#161a20 0%,#11141a 100%)}
.l0wrap canvas{position:absolute;inset:0;width:100%;height:100%;display:block}
.l0crumb{position:absolute;left:12px;top:10px;z-index:4;display:flex;flex-wrap:nowrap;
  gap:6px;align-items:center;max-width:calc(100% - 24px);pointer-events:auto;
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
.l0ctl{position:absolute;right:12px;top:10px;z-index:4;display:flex;gap:6px}
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
.l0reg{position:absolute;left:0;top:44px;z-index:5;width:396px;max-height:calc(100% - 56px);
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
  colHead:'#8d97a4', colNote:'#5c6672', colRule:'#262e36',
  restLine:'#2f3a45', restAnchor:'#2a3b44', restDenial:'#5a3f3c',
  pointer:'#efb555', iso:'#e8705f', ink:'#e6e9ee', ink2:'#b9c2cd',
};
/* Three view options, all ON by default. Stewart's call, 25 August 2026, having
   looked at the comp with all three on: "want all 3 options turned on". They are
   controls rather than constants because each one answers a different question and
   a reader who wants the arrangement alone should be able to get it. */
const L0_OPT = { rest:true, flags:true, labels:true };

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
  const PAD = { l: GEO.gutter || 148, t: GEO.headRow || 46 };
  const REST = new Set(PK.rest || []);
  const FLAG = new Set(PK.flags || []);
  const opt = Object.assign({}, L0_OPT);
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
      ctx.font = "400 " + (9.5*view.k).toFixed(2) + "px 'IBM Plex Mono',monospace";
      ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
      /* The cross below is drawn INSIDE the chip at a fixed right inset, so the
         label's room has to account for it or the two land on top of each other.
         They did: "University at Albany (SUNY), Dep" lost its ellipsis to the
         mark and read as if the cross were part of the name. Reserve the cross's
         own width plus a gap, and only when there is a cross to reserve for. */
      const room = w - 12*view.k - (n.iso ? 11*view.k : 0);
      let t = n.short || n.label || n.id;
      if (ctx.measureText(t).width > room){
        while (t.length > 2 && ctx.measureText(t + '\u2026').width > room) t = t.slice(0, -1);
        t += '\u2026';
      }
      ctx.fillStyle = on ? L0_PACK.ink : (n.tier === 'A' ? L0_PACK.ink : L0_PACK.ink2);
      ctx.fillText(t, x + 7*view.k, y + h/2 + 0.5);
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
  function bands(){
    (PK.bands||[]).forEach((b, i) => {
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
    (PK.bands||[]).forEach(b => {
      const y = SY(b.y), h = b.h*view.k;
      if (y > H || y + h < PAD.t) return;
      const ty = Math.max(y, PAD.t);      /* a row scrolled half off still names itself */
      ctx.font = "600 9px 'IBM Plex Mono',monospace";
      ctx.fillStyle = L0_PACK.bandLabel;
      ctx.fillText(String(b.id).toUpperCase().slice(0, 20), 10, ty + 13);
      ctx.font = "400 9px 'IBM Plex Mono',monospace";
      ctx.fillStyle = L0_PACK.bandN;
      ctx.fillText(b.n + ' \u00b7 mean C ' + b.meanC, 10, ty + 25);
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
    (PK.eras||[]).forEach(c => {
      const x = SX(c.x);
      if (x > W || x + c.w*view.k < PAD.l) return;
      const cx = Math.max(PAD.l, Math.min(W - 150, x));
      /* Baselines sit in the LOWER part of the strip, below the DOM control row
         that overlays it at top:10px. Derived from PAD.t rather than written as
         constants, so a future change to geo.headRow moves the text with it
         instead of quietly re-creating the overprint. */
      ctx.font = "600 9px 'IBM Plex Mono',monospace";
      ctx.fillStyle = L0_PACK.colHead;
      ctx.fillText(c.label, cx, PAD.t - 22);
      if (c.note){
        ctx.font = "400 8.5px 'IBM Plex Mono',monospace";
        ctx.fillStyle = L0_PACK.colNote;
        ctx.fillText(c.note, cx, PAD.t - 9);
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
    /* D3: denial edges are the first asymmetric edge the engine has had, and
       direction is the whole instrument. Undirected, AARO's own historical record
       and Grusch look alike.

       Which is exactly why it may not be guessed. This head used to draw on EVERY
       denial edge, pointing at `e.b`, where a/b comes from [a,b].sort() in the
       generator. Alphabetical order. It disagreed with the board's own records on
       22 of 47, and the records do not carry a consistent issuer-first convention
       either. So the head now draws only where an edge NAMES its denier, and it
       points at the OTHER end, the subject. No edge names one yet, so none draw.
       Author `denier` and the instrument comes back. */
    const dnr = e.denier;
    if (!summarised && (e.types||[]).indexOf('denial') >= 0 && dnr &&
        (dnr === e.a || dnr === e.b)){
      const tx = dnr === e.a ? x2 : x1, ty = dnr === e.a ? y2 : y1;
      const fx = dnr === e.a ? cx : x2, fy = dnr === e.a ? cy : y2;
      const ang = Math.atan2(ty-fy, tx-fx);
      const hx = tx - Math.cos(ang)*10, hy = ty - Math.sin(ang)*10;
      ctx.beginPath();
      ctx.moveTo(tx - Math.cos(ang)*11*view.k, ty - Math.sin(ang)*11*view.k);
      ctx.lineTo(hx - Math.sin(ang)*3.2, hy + Math.cos(ang)*3.2);
      ctx.lineTo(hx + Math.sin(ang)*3.2, hy - Math.cos(ang)*3.2);
      ctx.closePath(); ctx.fill();
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

    const dim = S.l0open.length ? 0.16 : 1;
    const lit = new Set(S.l0open);
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
    const es = D.summarised.map(e=>({e,s:true})).concat(D.directEdges.map(e=>({e,s:false})));
    es.sort((p,q)=>(p.e.n||1)-(q.e.n||1));   /* weakest first, strong claims on top */
    for (const {e,s:sm} of es){
      const touched = lit.has(e.a) || lit.has(e.b);
      const atRest = opt.rest && REST.has(ekey(e, sm));
      if (idle ? !atRest : !(touched || atRest)) continue;
      ctx.globalAlpha = (idle || touched) ? 1 : dim;
      trace(e, sm);
    }
    ctx.globalAlpha = 1;

    for (const n of D.l0){
      const x = SX(n.x), y = SY(n.y);
      if (x + n.w*view.k < -20 || x > W+20 || y + n.h*view.k < -20 || y > H+20) continue;
      ctx.globalAlpha = (idle || lit.has(n.id)) ? 1 : dim;
      chip(n, hover === n.id || S.l0open.indexOf(n.id) >= 0, lit);
      if (opt.flags && FLAG.has(n.id)) pointer(n);
      ctx.globalAlpha = 1;
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
    let c = host.querySelector('.l0crumb');
    if (!c){ c = el('div','l0crumb'); host.appendChild(c); }
    let h = '<span class="l0chip root">PROGRAM MAP</span>';
    for (const id of S.l0open){
      const n = byId[id];
      if (!n) continue;
      h += '<span class="l0chip" data-close="'+esc(id)+'">'+esc(n.short)
         + ' <span class="n">'+(n.direct.length+n.routed.length)+'</span>'
         + ' <span class="x">&times;</span></span>';
    }
    if (S.l0full) h += '<span class="l0chip" data-full="0">FULL GRAPH <span class="x">&times;</span></span>';
    if (S.l0open.length) h += '<span class="l0chip" data-clear="1">CLEAR</span>';
    h += '<span class="l0meta">' + D.counts.l0 + ' nodes · '
       + (opt.rest ? (PK.rest||[]).length : 0) + ' of '
       + (D.counts.directEdges + D.counts.summarisedEdges) + ' links at rest · '
       + view.k.toFixed(2) + 'x</span>';
    c.innerHTML = h;

    let z = host.querySelector('.l0ctl');
    if (!z){ z = el('div','l0ctl'); host.appendChild(z); }
    /* Three options, all on by default, each with a control -- so a reader who
       wants the bare arrangement can get it and, per the "drive the whole app from
       the chat input" requirement, the analyst can operate them too (CMD.l0opt). */
    z.innerHTML = '<button class="hopb" data-fit="1">OVERVIEW</button>'
                + '<button class="hopb" data-one="1">1:1 READ</button>'
                + '<button class="hopb'+(opt.rest?' on':'')+'" data-opt="rest">LINES AT REST</button>'
                + '<button class="hopb'+(opt.flags?' on':'')+'" data-opt="flags">START HERE</button>'
                + '<button class="hopb'+(opt.labels?' on':'')+'" data-opt="labels">LABELS</button>';
  }

  function renderLedgers(){
    for (const e of [...host.querySelectorAll('.l0ledger')]) e.remove();
    for (const id of S.l0open){
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
          ? 'click opens the member ledger'
          : 'click refused — '+mem+' member, no aggregate') + '</span>';
    t.style.left = Math.min(W-300, mx+14)+'px';
    t.style.top  = Math.min(H-110, my+14)+'px';
  }

  function repaint(){ paintMap(); renderChrome(); renderLedgers(); renderRegister(); }

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
    view.k = k2; clampView(); repaint();
  }, { passive:false });
  host.addEventListener('click', ev => {
    const c = ev.target.closest('[data-close]');
    if (c) return CMD.collapse(c.getAttribute('data-close'));
    if (ev.target.closest('[data-clear]')) return CMD.clearExpansions();
    if (ev.target.closest('[data-fit]')){ centreOn(fitScale()); repaint(); return; }
    if (ev.target.closest('[data-one]')){ cornerOn(1); repaint(); return; }
    const o = ev.target.closest('[data-opt]');
    if (o){ const k = o.getAttribute('data-opt'); opt[k] = !opt[k]; repaint(); return; }
    const p = ev.target.closest('[data-panel]');
    if (p){ S.l0panel = p.getAttribute('data-panel') || null; renderRegister(); return; }
    const f = ev.target.closest('[data-full]');
    if (f){ S.l0full = false; paint({ full:true }); return; }
    const r = ev.target.closest('[data-node]');
    /* The ledger is a table of contents, not a replacement for the dock. */
    if (r) return CMD.selectNode(r.getAttribute('data-node'));
  });

  measure();
  const fk = fitScale();
  /* Fitted if the fit keeps labels; otherwise the top-left corner at 1:1, because
     on a banded grid the first band is where the argument starts. The old code
     centred at 1.0 instead, which on a 2200x912 world opens on the middle of the
     funding band with no column head and no band label in view. */
  if (fk >= L0_LABEL_DROP) centreOn(fk); else cornerOn(1);
  repaint();
  const ro = new ResizeObserver(() => { measure(); clampView(); repaint(); });
  ro.observe(host);
  return {
    repaint, pairs: [],   /* INSIGHTS() reaches for this; see renderNetworkChrome */
    opt,
    destroy(){ dead = true; ro.disconnect(); if (raf) cancelAnimationFrame(raf); },
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
    paint({ map:'l0' });
  },
  collapse(id){
    const i = S.l0open.indexOf(id);
    if (i < 0) return warn('"'+id+'" is not open');
    S.l0open.splice(i,1); paint({ map:'l0' });
  },
  clearExpansions(){ S.l0open = []; paint({ map:'l0' }); },
  showPathOnly(){ S.l0panel = 'path'; S.view = 'NETWORK'; paint({ full:true }); },
  showUnattached(){ S.l0panel = 'un'; S.view = 'NETWORK'; paint({ full:true }); },
"""


# ---------------------------------------------------------------------- apply
# ------------------------------------------------------------- packed geometry
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

    # Edge budget. `rest` says which edges draw with nothing selected; `role` says
    # why each one earned the space. Keyed a|b|kind because a pair can carry both a
    # direct edge and a summarised one and they are different objects.
    rest, roles = [], {}
    for e in cur.get("edges", []):
        k = e["a"] + "|" + e["b"] + "|" + ("direct" if e["kind"] == "direct" else "shared")
        if e.get("rest"):
            rest.append(k)
        if e.get("role"):
            roles[k] = e["role"]

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

    # -- mount. L0 owns the rest state. The legacy full-graph map still mounts
    #    while a path or a frame is active, so setHops / highlightPath /
    #    focusCluster / frameNodes and the insight callout's "Show me on the map"
    #    keep working. selectNode deliberately does NOT trigger the swap: the dock
    #    opening must not move the map.
    s, o = must_replace(s,
        "  MAP = mountNetwork(wrap);\n  renderNetworkChrome();",
        "  S.l0full = !!(S.path || (S.frame && S.frame.length));\n"
        "  if (S.l0full){ MAP = mountNetwork(wrap); renderNetworkChrome(); }\n"
        "  else { wrap.className = 'cwrap l0wrap'; MAP = mountL0(wrap); }",
        "L0 mount", 1); ok &= o

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
    s, o = must_replace(s,
        "    if (S.l0open.indexOf(id) < 0) S.l0open.push(id);\n    paint({ map:'l0' });",
        "    S.l0open = [id];\n    if (MAP && MAP.focus) MAP.focus(id);\n"
        "    paint({ map:'l0' });",
        "single selection on expand", 1); ok &= o

    # selectNode drives the map too, so the dock never describes a node the reader
    # cannot see. It only moves the camera when the target IS on the L0 map.
    s, o = must_replace(s,
        "    S.sel = id; S.tab = 'DOSSIER'; S.path = null; S.frame = null;\n"
        "    if (S.view !== 'NETWORK') S.view = 'NETWORK';\n    paint({ map:'select' });",
        "    S.sel = id; S.tab = 'DOSSIER'; S.path = null; S.frame = null;\n"
        "    if (S.view !== 'NETWORK') S.view = 'NETWORK';\n"
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
        "  const grip = '<div class=\"dock-grip\" title=\"Drag to resize. Double click to reset\"></div>'\n"
        "    + '<button class=\"dock-toggle\" data-dockw=\"1\" title=\"Widen or collapse the dossier\">'\n"
        "    + (S.dockCollapsed ? '&lsaquo;' : '&rsaquo;') + '</button>';",
        "dock collapse control", 1); ok &= o

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
        "    /* zoom in enough that the node and its label are readable, then\n"
        "       centre it. The reader asked for the node they clicked, not a\n"
        "       field of 96. */\n"
        "    view.k = Math.max(view.k, 1.15);\n"
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
        "  return {\n    repaint, focus, pairs: [],",
        "MAP.focus", 1); ok &= o

    s, o = must_replace(s,
        "    const n = at(ev.clientX-b.left, ev.clientY-b.top);\n    if (!n) return;\n"
        "    CMD.expand(n.id);",
        "    const n = at(ev.clientX-b.left, ev.clientY-b.top);\n"
        "    /* empty canvas clears. Before this there was no way to unclick. */\n"
        "    if (!n){ if (S.l0open.length){ CMD.clearExpansions(); CMD.clearSelection(); } return; }\n"
        "    /* clicking the open node again closes it — the other half of the exit */\n"
        "    if (S.l0open.length === 1 && S.l0open[0] === n.id){\n"
        "      CMD.clearExpansions(); CMD.clearSelection(); return; }\n"
        "    /* Open the popover AND load the dossier. The DETAIL pane says 'click any\n"
        "       node on the map ... to open its dossier here'; it never did, because\n"
        "       this handler only ever called expand(). The copy was right and the\n"
        "       behaviour was wrong. */\n"
        "    CMD.expand(n.id);\n"
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
        "  if (ev.target.closest('[data-dockw]')){",
        "KPI + dock-collapse handlers", 1); ok &= o

    # the always-present collapse control, and the re-open tab when hidden
    s, o = must_replace(s,
        "    + (S.dockCollapsed ? '&lsaquo;' : '&rsaquo;') + '</button>';",
        "    + (S.dockCollapsed ? '&lsaquo;' : '&rsaquo;') + '</button>'\n"
        "    + '<button class=\"dock-hide\" data-dockoff=\"1\" title=\"Hide the detail pane\">&raquo;</button>';",
        "dock hide control", 1); ok &= o

    s, o = must_replace(s,
        "  d.classList.toggle('open', !!S.sel);\n  setDockOpen(!!S.sel && !S.dockCollapsed);",
        "  d.classList.toggle('open', !!S.sel);\n"
        "  setDockOpen(!!S.sel && !S.dockCollapsed && !S.dockOff);\n"
        "  let tab = document.querySelector('.dock-show');\n"
        "  if (S.dockOff && !tab){\n"
        "    tab = el('button','dock-show','&laquo;');\n"
        "    tab.setAttribute('data-dockoff','1');\n"
        "    tab.title = 'Show the detail pane';\n"
        "    document.body.appendChild(tab);\n"
        "  } else if (!S.dockOff && tab){ tab.remove(); }",
        "dock re-open tab", 1); ok &= o

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
        "  /* l0entry starts TRUE: a stranger should land on a question, not a\n"
        "     hairball. Once they have chosen a way in it stays down for the\n"
        "     session. */\n"
        "  l0entry:true, l0path:null, l0focus:null,\n};",
        "entry state", 1); ok &= o

    # the entry surface mounts over the map, and the map keeps running behind it
    s, o = must_replace(s,
        "  measure();\n  const fk = fitScale();",
        "  renderL0Entry(host);\n  measure();\n  const fk = fitScale();",
        "mount the entry surface", 1); ok &= o
    s, o = must_replace(s,
        "  function repaint(){ paintMap(); renderChrome(); renderLedgers(); renderRegister(); }",
        "  function repaint(){ paintMap(); renderChrome(); renderLedgers();\n"
        "    renderRegister(); renderL0Entry(host); }",
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
        "    if (S.l0full) h += '<span class=\"l0chip\" data-full=\"0\">FULL GRAPH",
        "    if (S.l0path){\n"
        "      const p = (L0DATA.entryPaths||[]).find(x=>x.id===S.l0path);\n"
        "      if (p) h += '<span class=\"l0chip path\" data-clearpath=\"1\">'\n"
        "        + esc(p.label) + ' <span class=\"n\">' + p.onMap + '</span>'\n"
        "        + ' <span class=\"x\">&times;</span></span>';\n"
        "    }\n"
        "    h += '<span class=\"l0chip\" data-entry=\"1\">START</span>';\n"
        "    if (S.l0full) h += '<span class=\"l0chip\" data-full=\"0\">FULL GRAPH",
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
    s, o = must_replace(s, "window.__board = { CMD, S,",
                        "window.__board = { CMD, S, L0DATA, mountL0,",
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
    s, o = must_replace(s,
        "  step('camera', () => {\n    if (S.view === 'NETWORK' && MAP){",
        "  step('camera', () => {\n    if (S.view === 'NETWORK' && MAP){\n"
        "      if (MAP.repaint && !S.l0full){ MAP.repaint(); return; }",
        "L0 repaint on paint()", 1); ok &= o
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
.dock{transition:width 260ms cubic-bezier(.2,0,0,1)}
.dock.dock-wide{max-width:none}
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
   selected. Half the viewport, floored at 560px so it does not collapse on a
   laptop, and animated on the shell's own curve rather than snapping. */
function setDockOpen(open){
  const d = document.getElementById('dock');
  if (!d) return;
  /* Set the width ON THE ELEMENT rather than through a CSS variable. --dock-w is
     already written to :root by the inherited resize grip, and racing two
     declarations of the same custom property through different owners is how the
     first attempt at this silently did nothing: the class landed, the width did
     not move, and nothing errored. */
  const wide = Math.max(560, Math.round(window.innerWidth * 0.5));
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
     actions were written to. All three ship ON. */
  l0opt(which, on){
    if (!MAP || !MAP.opt) return warn('the program map is not mounted');
    const K = { rest:'lines at rest', flags:'start-here pointers', labels:'chip labels' };
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
    S.l0entry = false;
    S.l0path = id;
    S.l0focus = new Set(p.ids);
    S.l0open = [];
    if (p.people && p.ids.length) { CMD.selectNode(p.ids[0]); return; }
    S.sel = null;
    paint({ map:'l0', full:true });
  },
  clearPath(){
    S.l0path = null; S.l0focus = null;
    paint({ map:'l0', full:true });
  },
  showEntry(){ S.l0entry = true; S.view = 'NETWORK'; paint({ full:true }); },
"""
