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
.l0crumb{position:absolute;left:12px;top:10px;z-index:4;display:flex;flex-wrap:wrap;
  gap:6px;align-items:center;max-width:calc(100% - 24px);pointer-events:auto}
.l0chip{display:inline-flex;align-items:center;gap:6px;height:22px;padding:0 8px;
  background:#141920;border:1px solid #262e36;color:#b9c2cd;
  font:500 9px/1 'IBM Plex Mono',monospace;letter-spacing:.10em;text-transform:uppercase;
  cursor:pointer}
.l0chip.root{color:#8d97a4;cursor:default}
.l0chip .n{color:#5ed4e6}
.l0chip .x{color:#5c6672;font-size:11px}
.l0chip:hover .x{color:#e8705f}
.l0meta{color:#5c6672;font:400 9px/1 'IBM Plex Mono',monospace;letter-spacing:.10em}
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
.l0body{max-height:328px;overflow:auto;padding:4px 0}
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
.l0reg{position:absolute;left:0;top:0;bottom:0;z-index:7;width:396px;
  background:#12171d;border-right:1px solid #262e36;display:flex;flex-direction:column}
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
const L0_MARK = 13;

function mountL0(host){
  const D = L0DATA, byId = {};
  for (const n of D.l0) byId[n.id] = n;
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
  /* SPEC 7. Opening fitted is only correct if labels survive the fit. At this
     node count the fit lands within a few hundredths of the 0.62 drop threshold,
     so it is MEASURED here rather than decided at build time: if the fit keeps
     labels we open fitted, and if it does not we open at 1.0 and the reader pans.
     Either way OVERVIEW is an explicit control. */
  function fitScale(){
    const xs = D.l0.map(n=>n.x), ys = D.l0.map(n=>n.y);
    const w = Math.max(...xs)-Math.min(...xs) + 132;   /* label max-width  */
    const h = Math.max(...ys)-Math.min(...ys) + 46;    /* mark + label line */
    return Math.min((W-48)/w, (H-48)/h);
  }
  function centreOn(k){
    const xs = D.l0.map(n=>n.x), ys = D.l0.map(n=>n.y);
    const cx = (Math.max(...xs)+Math.min(...xs))/2, cy = (Math.max(...ys)+Math.min(...ys))/2;
    view.k = k; view.ox = W/2 - cx*k; view.oy = H/2 - cy*k;
  }
  const SX = x => x*view.k + view.ox, SY = y => y*view.k + view.oy;

  /* ---- marks ---------------------------------------------------------- */
  function mark(x, y, cls, colour, on){
    const s = L0_MARK, h = s/2;
    ctx.lineWidth = 1;
    ctx.strokeStyle = on ? colour : '#3b444f';
    ctx.fillStyle = '#12171d';
    const m = (L0_CLS[cls]||L0_CLS.person).mark;
    ctx.beginPath();
    if (m === 'circle'){ ctx.arc(x, y, h, 0, Math.PI*2); }
    else if (m === 'diamond'){
      const r = h*0.92*Math.SQRT2;
      ctx.moveTo(x, y-r); ctx.lineTo(x+r, y); ctx.lineTo(x, y+r); ctx.lineTo(x-r, y);
      ctx.closePath();
    }
    else if (m === 'bar'){ ctx.rect(x-3, y-7, 6, 14); }
    else { ctx.rect(x-h, y-h, s, s); }
    ctx.fill(); ctx.stroke();
    if (m === 'doc'){                       /* 3px top rule, the document tell */
      ctx.fillStyle = colour;
      ctx.fillRect(x-h, y-h, s, 3);
    }
  }
  /* Aggregate affordance: a FIXED stack, two offset copies behind the mark. It
     does not grow with the count, because a geometric channel that scaled with
     member count would read as authority — and on this board the biggest node is
     AARO, which is implicated rather than authoritative. */
  function stack(x, y, cls){
    for (const [d, col] of [[6,'#333c47'],[3,'#3b444f']]){
      ctx.strokeStyle = col; ctx.fillStyle = '#12171d'; ctx.lineWidth = 1;
      const h = L0_MARK/2;
      ctx.beginPath(); ctx.rect(x-h+d, y-h+d, L0_MARK, L0_MARK); ctx.fill(); ctx.stroke();
    }
  }

  /* ---- traces --------------------------------------------------------- */
  /* Right-angled with one mitred corner, long axis first. Ticks at the corner,
     one per underlying link (direct) or shared member (summarised). The counts
     top out at 5 on this data, so the five-tick vocabulary never overflows and
     there is no numeral case to design. */
  function trace(e, summarised){
    const a = byId[e.a], b = byId[e.b];
    if (!a || !b) return;
    const x1=SX(a.x), y1=SY(a.y), x2=SX(b.x), y2=SY(b.y);
    const t = L0_TIER[e.tier] || L0_TIER[3];
    const w = e.n || 1;
    ctx.globalAlpha = Math.min(0.92, 0.30 + (w-1)*0.15);
    ctx.strokeStyle = t.c;
    ctx.lineWidth = summarised ? 1 : 2;
    ctx.setLineDash(t.d);
    const horizFirst = Math.abs(x2-x1) >= Math.abs(y2-y1);
    const cx = horizFirst ? x2 : x1, cy = horizFirst ? y1 : y2;
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(cx,cy); ctx.lineTo(x2,y2); ctx.stroke();
    ctx.setLineDash([]);
    /* ticks */
    const n = Math.min(5, w);
    ctx.fillStyle = t.c;
    for (let i=0;i<n;i++){
      const off = (i - (n-1)/2) * 3.6;
      ctx.fillRect(cx + (horizFirst?off:-1.1), cy + (horizFirst?-1.1:off), 2.2, 2.2);
    }
    /* D3: denial edges are the first asymmetric edge the engine has had.
       Direction is the whole instrument — undirected, AARO's own historical
       record and Grusch look alike; split, one is the heaviest issuer on the
       board and the other is predominantly a recipient. */
    if (!summarised && (e.types||[]).indexOf('denial') >= 0){
      const ang = Math.atan2(y2-cy, x2-cx);
      const hx = x2 - Math.cos(ang)*10, hy = y2 - Math.sin(ang)*10;
      ctx.beginPath();
      ctx.moveTo(x2 - Math.cos(ang)*L0_MARK*0.8, y2 - Math.sin(ang)*L0_MARK*0.8);
      ctx.lineTo(hx - Math.sin(ang)*3.2, hy + Math.cos(ang)*3.2);
      ctx.lineTo(hx + Math.sin(ang)*3.2, hy - Math.cos(ang)*3.2);
      ctx.closePath(); ctx.fill();
    }
    ctx.globalAlpha = 1;
  }

  function draw(){
    raf = null;
    if (dead) return;
    ctx.clearRect(0,0,W,H);
    /* grid */
    ctx.strokeStyle = 'rgba(59,68,79,0.18)'; ctx.lineWidth = 1;
    const g = 44*view.k;
    if (g > 6){
      ctx.beginPath();
      for (let x = view.ox % g; x < W; x += g){ ctx.moveTo(x,0); ctx.lineTo(x,H); }
      for (let y = view.oy % g; y < H; y += g){ ctx.moveTo(0,y); ctx.lineTo(W,y); }
      ctx.stroke();
    }
    const dim = S.l0open.length ? 0.16 : 1;
    const lit = new Set(S.l0open);
    for (const id of S.l0open){
      const n = byId[id];
      if (n) for (const m of n.direct) lit.add(m);
    }
    /* weakest first, so the strong claims land on top */
    const es = D.summarised.map(e=>({e,s:true})).concat(D.directEdges.map(e=>({e,s:false})));
    es.sort((p,q)=>(p.e.n||1)-(q.e.n||1));
    for (const {e,s} of es){
      const on = !S.l0open.length || lit.has(e.a) || lit.has(e.b);
      ctx.globalAlpha = on ? 1 : dim;
      trace(e, s);
    }
    ctx.globalAlpha = 1;
    const showLabels = view.k >= L0_LABEL_DROP;
    for (const n of D.l0){
      const x = SX(n.x), y = SY(n.y);
      if (x < -80 || x > W+80 || y < -60 || y > H+60) continue;
      const on = !S.l0open.length || lit.has(n.id);
      ctx.globalAlpha = on ? 1 : dim;
      const col = (L0_CLS[n.cls]||L0_CLS.person).c;
      const mem = n.direct.length + n.routed.length;
      const active = hover === n.id || S.l0open.indexOf(n.id) >= 0;
      if (mem >= 2) stack(x, y, n.cls);
      mark(x, y, n.cls, col, active);
      if (showLabels){
        ctx.font = "500 9px 'IBM Plex Mono',monospace";
        ctx.textAlign = 'center'; ctx.textBaseline = 'top';
        let s = n.short, wpx = ctx.measureText(s).width;
        while (wpx > 132 && s.length > 4){ s = s.slice(0,-2); wpx = ctx.measureText(s+'…').width; }
        if (s !== n.short) s += '…';
        const ty = y + L0_MARK/2 + 5;
        ctx.fillStyle = 'rgba(15,18,22,0.88)';
        ctx.fillRect(x - wpx/2 - 3, ty - 1, wpx + 6, 12);
        ctx.fillStyle = active ? '#e6e9ee' : '#b9c2cd';
        ctx.fillText(s, x, ty);
        if (mem >= 2) drawLedgerBar(x, ty + 13, n);
      }
      ctx.globalAlpha = 1;
    }
  }
  /* D2, recorded as a rule BENT rather than met: the class mix is carried in hue
     alone. The design system forbids that. The tooltip names every segment, which
     mitigates it; it does not make it compliant. */
  function drawLedgerBar(x, y, n){
    const total = n.direct.length + n.routed.length;
    if (!total) return;
    const keys = Object.keys(n.mix);
    let px = x - 74/2;
    for (const k of keys){
      const w = Math.max(1, (n.mix[k]/total)*74 - 1);
      ctx.fillStyle = (L0_CLS[k]||L0_CLS.person).c;
      ctx.fillRect(px, y, w, 2);
      px += w + 1;
    }
    ctx.font = "500 9px 'IBM Plex Mono',monospace";
    ctx.textAlign = 'left'; ctx.fillStyle = '#8d97a4';
    ctx.fillText(String(total), x + 74/2 + 5, y - 3);
  }
  const paintMap = () => { if (!raf) raf = requestAnimationFrame(draw); };

  /* ---- hit test ------------------------------------------------------- */
  function at(mx, my){
    for (let i = D.l0.length-1; i >= 0; i--){
      const n = D.l0[i];
      const dx = mx - SX(n.x), dy = my - SY(n.y);
      if (Math.abs(dx) <= 11 && Math.abs(dy) <= 11) return n;
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
    h += '<span class="l0meta">' + (D.counts.l0 + D.counts.directEdges + D.counts.summarisedEdges)
       + ' objects · ' + view.k.toFixed(2) + 'x</span>';
    c.innerHTML = h;

    let z = host.querySelector('.l0ctl');
    if (!z){ z = el('div','l0ctl'); host.appendChild(z); }
    z.innerHTML = '<button class="hopb" data-fit="1">OVERVIEW</button>'
                + '<button class="hopb" data-one="1">1:1 READ</button>';
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
        + 'denials <span class="di">'+n.di+' issued</span> · '+n.dr+' received</div>'
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
      const sx = Math.max(8, Math.min(W-314, SX(n.x) + 18));
      const sy = Math.max(8, Math.min(H-120, SY(n.y) - 40));
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
    p.innerHTML = h + '</div>';
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
      + 'denials '+n.di+' issued · '+n.dr+' received<br>'
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
    view.k = k2; repaint();
  }, { passive:false });
  host.addEventListener('click', ev => {
    const c = ev.target.closest('[data-close]');
    if (c) return CMD.collapse(c.getAttribute('data-close'));
    if (ev.target.closest('[data-clear]')) return CMD.clearExpansions();
    if (ev.target.closest('[data-fit]')){ centreOn(fitScale()); repaint(); return; }
    if (ev.target.closest('[data-one]')){ centreOn(1); repaint(); return; }
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
  centreOn(fk >= L0_LABEL_DROP ? fk : 1);
  repaint();
  const ro = new ResizeObserver(() => { measure(); repaint(); });
  ro.observe(host);
  return {
    repaint, pairs: [],   /* INSIGHTS() reaches for this; see renderNetworkChrome */
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
def apply(s, model, must_replace):
    """Splice the L0 map into the built dashboard.

    `must_replace` is build_dashboard's own helper, passed in so a failed anchor
    reports through the same channel as every other patch and the build says
    "SOME PATCHES FAILED" rather than emitting a quietly broken file."""
    import json as _json
    ok = True

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
                        "  l0open:[], l0panel:null, l0full:false,\n};",
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
        "    view.ox = W/2 - n.x*view.k; view.oy = H/2 - n.y*view.k;\n"
        "    repaint();\n"
        "  }\n"
        "  return {\n    repaint, focus, pairs: [],",
        "MAP.focus", 1); ok &= o

    s, o = must_replace(s,
        "    const n = at(ev.clientX-b.left, ev.clientY-b.top);\n    if (!n) return;\n"
        "    CMD.expand(n.id);",
        "    const n = at(ev.clientX-b.left, ev.clientY-b.top);\n"
        "    /* empty canvas clears. Before this there was no way to unclick. */\n"
        "    if (!n){ if (S.l0open.length) CMD.clearExpansions(); return; }\n"
        "    /* clicking the open node again closes it — the other half of the exit */\n"
        "    if (S.l0open.length === 1 && S.l0open[0] === n.id) return CMD.clearExpansions();\n"
        "    CMD.expand(n.id);",
        "click to clear", 1); ok &= o

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
.dock-wide{--dock-w:var(--dock-w-open)}
.dock-toggle{position:absolute;left:-11px;top:50%;transform:translateY(-50%);
  z-index:32;width:22px;height:46px;background:#141920;border:1px solid #262e36;
  border-right:none;color:#8d97a4;cursor:pointer;font:500 11px/44px 'IBM Plex Mono',monospace;
  text-align:center;padding:0}
.dock-toggle:hover{color:#5ed4e6;border-color:#3b444f}
.edoss{padding:0 0 14px}
.edoss .why{margin:0 0 10px;padding:9px 11px;background:#141920;
  border-left:2px solid #5ed4e6;font:400 11px/1.65 'IBM Plex Mono',monospace;
  color:#dfe4ea}
.edoss .roles{display:flex;flex-wrap:wrap;gap:4px;margin:0 0 10px}
.edoss .role{padding:2px 6px;border:1px solid #333c47;color:#8d97a4;
  font:500 8.5px/1.5 'IBM Plex Mono',monospace;letter-spacing:.13em;text-transform:uppercase}
.edoss .narr{font:400 11.5px/1.75 'IBM Plex Mono',monospace;color:#b9c2cd;
  white-space:pre-wrap;margin:0 0 12px}
.edoss .dn{margin:0 0 12px;padding:8px 11px;border:1px solid #3b2b2b;
  background:#1a1416;font:400 10.5px/1.6 'IBM Plex Mono',monospace;color:#e8b0a6}
.edoss .cl{padding:6px 0;border-top:1px solid #1d242b;
  font:400 10.5px/1.6 'IBM Plex Mono',monospace;color:#b9c2cd}
.edoss .cl .t{display:inline-block;min-width:44px;font-size:8.5px;letter-spacing:.13em}
.edoss .cl a{color:#5c6672;font-size:9px;word-break:break-all;text-decoration:none}
.edoss .cl a:hover{color:#5ed4e6}
.t1{color:#5ed4e6}.t2{color:#efb555}.t3{color:#8d97a4}
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

function renderEntityDossier(id){
  const n = (L0DATA.l0||[]).find(x=>x.id===id);
  const d = (n && n.dossier) || (L0DATA.dossiers || {})[id];
  if (!d) return '<div class="edoss">' + renderConnections(id) + '</div>';
  const T = t => '<span class="t t'+t+'">TIER '+t+'</span>';
  let h = '<div class="edoss">';
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
  d.style.width = (open ? wide : (S.dockW || 306)) + 'px';
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
"""
