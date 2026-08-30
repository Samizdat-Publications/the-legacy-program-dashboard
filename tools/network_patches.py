"""The force-directed network map, which is the board's primary surface since
29 August 2026.

Its own module for the reason `l0_patches.py` and `patents_patches.py` are their
own modules: this renderer is INHERITED from `ref/the-vanishing-v2.html` and every
change to it is a patch against somebody else's code, so keeping those patches in
one place is the only way the next session can see what this board has changed and
what it merely accepted.

WHAT IS IN HERE
---------------
Claude Design's response of 30 August 2026 (`notes/DESIGN-BRIEF-2026-08-30-STANDALONE.md`
asked; their README answered). Changes 1, 2, 3 and the network half of 5:

  1. the map label carries the NAME only; date and status are dossier facts
  2. the drawn label set is chosen by available SPACE, never by rank
  3. pointer proximity raises labels, and nothing else moves
  5. the two bridge controls, which are not symmetric and are not one control

Change 4 is the packed map's warm arrival and lives in `l0_patches.py`, because that
is the renderer it belongs to.

THE RULE THAT SHAPES ALL OF THIS, and it is `CLAUDE.md` section 4: **size must never
encode importance.** Design spends most of change 2 on it. The obvious way to choose
which labels to draw is greedy by degree -- label the most connected first -- and
degree runs 6 to 62 across the L0 set alone. That makes prominence a function of
connectivity, which is the size rule wearing different clothes: the permanently
labelled node would be the biggest one. It is rejected outright, not deferred.
"""

import json as _json
import os


def apply(s, must_replace, model=None):
    """Patch the inherited network renderer.

    `must_replace` is build_dashboard's helper, so a failed anchor reports through the
    same channel as every other patch and the build says "SOME PATCHES FAILED" rather
    than emitting a quietly different board.
    """
    ok = True

    # ---------------------------------------------------------------- change 1
    # THE MAP LABEL CARRIES THE NAME ONLY.
    #
    # The person plate drew three facts stacked -- `GROTHMAN, G.` / `2023.07.26` /
    # `ACT` -- in a 100x40 box. Design: "Height is what collides in a dense field,
    # and this doubles the height of every label while tripling the ink."
    #
    # Date and status do not leave the board; they move to where a reader asks for
    # them. The plate keeps them under selection and hover, which is the state a
    # reader enters deliberately, and drops them at rest, which is the state 964
    # nodes are in at once.
    #
    # The plate SHRINKS with them. Leaving a 40px box around one line of text would
    # keep the collision footprint that made the change worth doing -- the ink would
    # improve and the density would not.
    # ANCHORED ON THE POST-PATCH TEXT, not on ref/. build_dashboard's own
    # `drawNode plate gate` patch has already rewritten this line by the time this
    # module runs -- it drops the photo-width branch and adds the PLATE_DEGREE gate.
    # Anchoring on ref/ here failed loudly, which is what must_replace is for.
    s, o = must_replace(s,
        "  const hasPhoto = !!n.photo;\n"
        "  const w = 100, h = 40, x = n.x - w / 2, y = n.y - h / 2;",
        "  const hasPhoto = !!n.photo;\n"
        "  /* CHANGE 1, Design 30 August 2026: at rest the plate carries the NAME\n"
        "     only. Date and status are dossier facts. They are still drawn under\n"
        "     selection and hover -- states a reader enters on purpose -- and the box\n"
        "     shrinks with them, because keeping a 40px plate around one line of text\n"
        "     would improve the ink and leave the collision footprint exactly where\n"
        "     it was. Height is what collides in a dense field. */\n"
        "  const full = sel || hov;\n"
        "  const w = 100, h = full ? 40 : 24,\n"
        "        x = n.x - w / 2, y = n.y - h / 2;",
        "network: plate is name-only at rest", 1); ok &= o

    # the photo slot is sized off the plate height, so it follows h rather than
    # keeping a 40px-tall crop inside a 24px box
    s, o = must_replace(s,
        "    const px = x + 9, py = y + 7, pw = 26, ph = h - 14;",
        "    const px = x + 9, py = y + (full ? 7 : 4), pw = 26, ph = h - (full ? 14 : 8);",
        "network: photo slot follows the plate height", 1); ok &= o

    # the name baseline, and the two facts that now only draw when asked for
    # The status chip is a nine-state map by the time this runs, not ref/'s
    # three-way ternary: `build_dashboard` rewrote it when the board gained
    # classified / denied / disputed. Anchored on what ships.
    STATUS_CHIP = (
        "  ctx.fillText(({ active:'ACT', former:'FMR', dead:'DEC', missing:'MIS', resolved:'CLD',\n"
        "    disbanded:'END', classified:'CLS', denied:'DEN', disputed:'DSP' })[n.status] || 'ACT', x + w - 8, y + 31);")
    s, o = must_replace(s,
        "  ctx.fillText(n.short || n.label.toUpperCase(), tx, y + 18);\n"
        "  ctx.fillStyle = PALETTE.faint;\n"
        "  ctx.font = '400 8.5px \"IBM Plex Mono\", monospace';\n"
        "  ctx.fillText(n.date.replace(/-/g, '.'), tx, y + 31);\n"
        "  ctx.fillStyle = col;\n"
        "  ctx.font = '600 8px \"IBM Plex Mono\", monospace';\n"
        "  ctx.textAlign = 'right';\n"
        + STATUS_CHIP,
        "  ctx.fillText(n.short || n.label.toUpperCase(), tx, y + (full ? 18 : 16));\n"
        "  if (full){\n"
        "    ctx.fillStyle = PALETTE.faint;\n"
        "    ctx.font = '400 8.5px \"IBM Plex Mono\", monospace';\n"
        "    ctx.fillText(n.date.replace(/-/g, '.'), tx, y + 31);\n"
        "    ctx.fillStyle = col;\n"
        "    ctx.font = '600 8px \"IBM Plex Mono\", monospace';\n"
        "    ctx.textAlign = 'right';\n"
        "  " + STATUS_CHIP.replace("\n  ", "\n    ") + "\n"
        "  }",
        "network: date and status draw only on selection or hover", 1); ok &= o


    # ---------------------------------------------------------------- change 2
    # THE DRAWN LABEL SET IS CHOSEN BY AVAILABLE SPACE, NEVER BY RANK.
    #
    # THE RULE DESIGN REJECTS, AND WHY IT MATTERS HERE MORE THAN THEY KNEW.
    # Greedy by degree -- label the most connected first -- makes prominence a
    # function of connectivity, which is `CLAUDE.md` section 4's "size must never
    # encode importance" wearing different clothes. Design says do not implement it
    # even as an interim step.
    #
    # **The board was already doing it.** `build_dashboard`'s own `PLATE_DEGREE = 5`
    # gate decides which PEOPLE get a plate at all, by degree, and a plate is how a
    # person is named on this map. So the most-connected people were the named ones
    # and the rest were anonymous dots. That is not a hypothetical Design was warning
    # against; it was the shipped behaviour, and the label pass below replaces it.
    #
    # THREE THINGS THIS CHANGES, and the second is a judgement beyond the letter of
    # the spec, flagged as such:
    #
    #   1. Labels move to SCREEN space. Design: "labels stay one size at every scale,
    #      consistent with the one-chip-size rule on the packed map. What zoom changes
    #      is how many are drawn." Inside the world transform the font scaled with the
    #      camera, so it could not be one size. The marks stay in world space; only the
    #      type leaves it.
    #   2. A person at rest is a DOT plus a name, exactly like an entity. The full
    #      plate -- photo, stripe, date, status -- draws under selection and hover.
    #      This follows from change 1 rather than being stated by it: once the plate
    #      carries only a name, a scaled box around one line of screen-space type is
    #      two treatments for one job. It also makes the collision problem uniform
    #      across all 964 nodes instead of two-tier.
    #   3. Truncation is MIDDLE, not right. Design: the force graph truncated
    #      `NATIONAL ARCHIVES UNIDE...`, which discards the discriminating tail. The
    #      packed map solved this already; this borrows the rule, not the code, because
    #      l0Fit is inside the other module's closure.
    #
    # ORDERING. Outward from the pointer, or from the viewport centre when the pointer
    # is off-canvas. The 14 signed-off START HERE highlights get first claim, and
    # nothing else jumps the queue -- that is an editorial flag Stewart approved by
    # hand, which is a defensible reason for one node to be named while its neighbour
    # is not. Degree is never consulted.
    # ANCHORED ON WHAT SHIPS, and what ships is the finding. build_dashboard had
    # already gated this label on `(n.deg || 0) >= LABEL_DEGREE`, with
    # LABEL_DEGREE = 12 -- entity labels chosen by degree, exactly the rule Design
    # rules out, in the second of two places. It also truncated from the RIGHT at 24
    # characters, which is the `NATIONAL ARCHIVES UNIDE...` Design screenshotted.
    # All three go: the gate, the right-truncation, and the world-space draw.
    s, o = must_replace(s,
        "    if (sel || hov || near || (scale > 0.62 && (n.deg || 0) >= LABEL_DEGREE)) {\n"
        "      ctx.fillStyle = dim ? PALETTE.faint : (sel || hov ? PALETTE.text : PALETTE.dim);\n"
        "      ctx.font = `${sel || hov ? 600 : 400} 9px \"IBM Plex Mono\", monospace`;\n"
        "      ctx.textAlign = 'center'; ctx.textBaseline = 'top';\n"
        "      const full = n.label.toUpperCase();\n"
        r"      const lbl = (sel || hov) ? full : (full.length > 24 ? full.slice(0, 23) + '\u2026' : full);" "\n"
        "      ctx.fillText(lbl, n.x, n.y + r + 5);\n"
        "    }",
        "  /* CHANGE 2: the label is no longer drawn here. drawNode draws the MARK;\n"
        "       the label is offered to the screen-space pass, which decides whether\n"
        "       there is room for it. Drawing it here would put it inside the world\n"
        "       transform, where it cannot be one size at every scale. */\n"
        "    if (st && st.labels) st.labels.push({ n, text: n.label.toUpperCase(),\n"
        "                                          rw: r, sel, hov, dim, con: near });",
        "network: entity label defers to the space pass", 1); ok &= o

    # the person plate: a dot at rest, the full plate when asked for. The name goes
    # to the same screen-space pass as every entity's, so one budget governs all 964.
    s, o = must_replace(s,
        "  const full = sel || hov;\n"
        "  const w = 100, h = full ? 40 : 24,\n"
        "        x = n.x - w / 2, y = n.y - h / 2;",
        "  const full = sel || hov;\n"
        "  /* CHANGE 2: at rest a person is a mark and a name, like everything else on\n"
        "     the board. PLATE_DEGREE used to decide who got a plate, and a plate is how\n"
        "     a person is named -- so the most-connected people were named and the rest\n"
        "     were anonymous. That is selection by rank, which is the one rule Design\n"
        "     rules out. The plate is now a state, not a rank. */\n"
        "  if (!full){\n"
        "    ctx.fillStyle = col;\n"
        "    ctx.beginPath(); ctx.arc(n.x, n.y, 4.5, 0, Math.PI * 2); ctx.fill();\n"
        "    if (st && st.labels) st.labels.push({ n, text: n.short || n.label.toUpperCase(),\n"
        "                                          rw: 4.5, sel, hov, dim, con: near });\n"
        "    ctx.globalAlpha = 1; return;\n"
        "  }\n"
        "  const w = 100, h = 40,\n"
        "        x = n.x - w / 2, y = n.y - h / 2;",
        "network: a person at rest is a mark and a name", 1); ok &= o


    # ---- the pass itself, in screen space, after the world transform is gone ----
    #
    # THE ALGORITHM IS DESIGN'S, VERBATIM IN SHAPE:
    #   1. walk candidates outward from the pointer, or the viewport centre when the
    #      pointer is off-canvas
    #   2. compute the label's bounding box at the fixed label size
    #   3. draw it if the box does not collide with any box already drawn this frame;
    #      otherwise SKIP THE NODE ENTIRELY -- do not shrink, do not truncate to fit
    #   4. stop at the frame budget
    #
    # WHAT IS PUBLISHED AND WHY. `MAP.labelBoxes()` returns the boxes actually drawn
    # on the last frame. A check reads it rather than re-deriving the layout, for the
    # same reason `l0Fit` is exposed to the packed map's checks: a check that
    # reimplements the thing it is checking passes when the renderer diverges. The
    # check binds that list back to pixels by sampling ink inside a sample of the
    # boxes, so a renderer that published boxes it did not draw would still fail.
    s, o = must_replace(s,
        "    const order = [...nodes].sort((a,b)=>(a.cls==='person'?1:0)-(b.cls==='person'?1:0));\n"
        "    for (const n of order){\n"
        "      if (n.alpha < 0.02) continue;\n"
        "      let st = 'default';\n"
        "      if (active) st = n.id === S.sel ? 'selected' : (active.has(n.id) ? 'connected' : 'dimmed');\n"
        "      if (hover && hover.id === n.id && st !== 'selected') st = 'hover';\n"
        "      ctx.save();\n"
        "      ctx.globalAlpha = n.alpha;\n"
        "      drawNode(ctx, n, { scale:cam.k, state:st });\n"
        "      ctx.restore();\n"
        "    }\n"
        "    ctx.restore();",
        "    const order = [...nodes].sort((a,b)=>(a.cls==='person'?1:0)-(b.cls==='person'?1:0));\n"
        "    const cand = [];\n"
        "    for (const n of order){\n"
        "      if (n.alpha < 0.02) continue;\n"
        "      let st = 'default';\n"
        "      if (active) st = n.id === S.sel ? 'selected' : (active.has(n.id) ? 'connected' : 'dimmed');\n"
        "      if (hover && hover.id === n.id && st !== 'selected') st = 'hover';\n"
        "      ctx.save();\n"
        "      ctx.globalAlpha = n.alpha;\n"
        "      drawNode(ctx, n, { scale:cam.k, state:st, labels:cand });\n"
        "      ctx.restore();\n"
        "    }\n"
        "    ctx.restore();\n"
        "    drawLabelPass(ctx, cand, W, H);",
        "network: the node pass collects labels and hands them to the space pass",
        1); ok &= o

    # the pass, plus its state, mounted alongside the renderer
    s, o = must_replace(s,
        "  function loop(){ if (dead) return; try{ draw(); }catch(e){ /* keep the loop alive */ } raf = requestAnimationFrame(loop); }",
        NETWORK_LABEL_PASS
        + "  function loop(){ if (dead) return; try{ draw(); }catch(e){ /* keep the loop alive */ } raf = requestAnimationFrame(loop); }",
        "network: the label pass", 1); ok &= o


    # ---------------------------------------------------------------- change 3
    # POINTER PROXIMITY, AND NOTHING ELSE.
    #
    # The standing rule is reaffirmed, not relaxed: at rest with nothing selected
    # the primary map is completely static, and the two checks that hold that line
    # stay unmodified. Motion is a claim about direction and on most of this board's
    # 2,172 edges no such claim is made.
    #
    # What the pointer changes is TYPOGRAPHY, never geometry. `ptr` is screen-space
    # and feeds only the label pass's ordering and its draw-anyway rule. Nothing
    # reads it for position, size or opacity of a node or an edge.
    #
    # `onLeave` clears it, which is what makes "pointer parked off-canvas" a real
    # rest state rather than a stale one: without that the map would keep favouring
    # wherever the cursor was when it left.
    s, o = must_replace(s,
        "    const mx = e.clientX-r.left, my = e.clientY-r.top;\n"
        "    const h = hitTest(mx,my);",
        "    const mx = e.clientX-r.left, my = e.clientY-r.top;\n"
        "    ptr = { x: mx, y: my };   /* change 3: live typography, static geometry */\n"
        "    const h = hitTest(mx,my);",
        "network: the pointer feeds the label pass", 1); ok &= o
    s, o = must_replace(s,
        "  const onLeave = () => { hover = null; tip.classList.remove('on'); if (drag) onUp(); };",
        "  const onLeave = () => { hover = null; ptr = null;   /* a real rest state */\n"
        "    tip.classList.remove('on'); if (drag) onUp(); };",
        "network: leaving the canvas restores the rest state", 1); ok &= o

    # ---- publish what was actually drawn -------------------------------------
    # For the reason l0Fit is exposed to the packed map's checks: so a check reads
    # the renderer's OWN result rather than a copy of the layout. A check that
    # reimplements what it checks passes when the renderer diverges. The check binds
    # this back to pixels by sampling ink inside these boxes, so publishing a box
    # that was never drawn still fails.
    s, o = must_replace(s,
        "  return {\n"
        "    get pairs(){ return pairs; },\n"
        "    get nodes(){ return nodes; },",
        "  return {\n"
        "    get pairs(){ return pairs; },\n"
        "    get nodes(){ return nodes; },\n"
        "    /* The label boxes drawn on the last frame, and the pointer that ordered\n"
        "       them. Read by tools/runtime_check.js. */\n"
        "    labelBoxes(){ return lastBoxes.map(b => ({ ...b })); },\n"
        "    labelPointer(){ return ptr ? { ...ptr } : null; },\n"
        "    /* The camera, so a check can ask whether a node is on screen without\n"
        "       re-deriving the transform. A check that recomputes the camera passes\n"
        "       when the renderer's camera drifts away from it. */\n"
        "    cam(){ return { x: cam.x, y: cam.y, k: cam.k }; },\n"
        "    setLabelPointer(p){ ptr = p ? { x:p.x, y:p.y } : null; },",
        "network: publish the drawn label boxes", 1); ok &= o


    # ---------------------------------------------------------------- change 5
    # THE REVERSE BRIDGE. Network map -> program map.
    #
    # NOT THE MIRROR OF THE FORWARD ONE, and Design is explicit that building them
    # as one control would be wrong. The forward trip always resolves. This one is
    # available on 110 nodes out of 964.
    #
    # It names the COORDINATES the destination has: `PLACE · CUSTODY · 2000-2016`.
    # The reverse trip's whole value is that the program map has coordinates and the
    # force graph does not -- so naming them means a reader who declines the trip has
    # still learned the answer.
    #
    # ABSENT, NOT DISABLED, on the other 854. Design's call, held loosely, and
    # Stewart's to confirm -- he confirmed it on 30 August. The argument: a control
    # that is visible and does nothing teaches a reader the board is broken; an
    # absent control teaches them this node is not one of the 110, which is true and
    # is itself information.
    #
    # KNOWN ASYMMETRY, not smoothed over: the six entry paths do not cover the two
    # maps evenly. `Start from a witness` has 0 of its 7 nodes on the packed map;
    # `The legal mechanism` has 10 of 10. So this control is systematically absent
    # along one path and universal along another. That absence is a fact about the
    # node, and it must not read as a click that failed.
    s, o = must_replace(s,
        "    +   '<button class=\"hopb\" data-zoom=\"reset\" title=\"Reset view. Double click the map does the same\">reset</button>'\n"
        "    + '</div>';",
        "    +   '<button class=\"hopb\" data-zoom=\"reset\" title=\"Reset view. Double click the map does the same\">reset</button>'\n"
        "    + '</div>'\n"
        "    + (function(){\n"
        "        /* CHANGE 5, REVERSE BRIDGE. Absent on the 854, by design. */\n"
        "        if (!S.sel) return '';\n"
        "        const L = ((typeof L0DATA !== 'undefined' && L0DATA.l0) || [])\n"
        "          .find(x => x.id === S.sel);\n"
        "        if (!L) return '';\n"
        "        const era = ((typeof L0DATA !== 'undefined' && L0DATA.packed\n"
        "          && L0DATA.packed.eras) || []).find(e => e.id === L.col);\n"
        "        const where = [String(L.band || '').toUpperCase(),\n"
        "                       (era && era.label) || L.col || ''].filter(Boolean).join(' \\u00b7 ');\n"
        "        return '<div class=\"toprog\"><button class=\"hopb\" data-toprog=\"1\" '\n"
        "          + 'title=\"Open the program map on this node, at its band and era.\">'\n"
        "          + 'PLACE \\u00b7 ' + esc(where) + '</button></div>';\n"
        "      })();",
        "network: the reverse bridge, absent on the 854", 1); ok &= o

    s, o = must_replace(s,
        "    if (ev.target.closest('[data-clearpath]')) return CMD.clearPath();",
        "    if (ev.target.closest('[data-toprog]')) return CMD.showInProgramMap();\n"
        "    if (ev.target.closest('[data-clearpath]')) return CMD.clearPath();",
        "network: the reverse bridge handler", 1); ok &= o

    s, o = must_replace(s, "</style>", NETWORK_CSS + "</style>",
                        "network: bridge styles", s.count("</style>")); ok &= o

    return s, ok


NETWORK_LABEL_PASS = r"""
  /* ---- CHANGE 2 + 3: the screen-space label pass -------------------------
     Design's response of 30 August 2026. Labels are chosen by the space that
     exists, never by rank, and they are one size at every scale.

     POINTER PROXIMITY (change 3) rides on the same pass, because it is the same
     decision made with a different origin. Within POINTER_R of the cursor a label
     raises in priority AND draws regardless of the budget, which is what makes a
     deliberately sparse centre navigable rather than empty.

     WHAT DOES NOT HAPPEN HERE, all of it hard: nothing changes position, no edge
     animates, no node changes size. Static geometry, live typography. At rest with
     the pointer off-canvas this pass is a pure function of the camera, so two
     successive frames are identical and the map is still. */
  const LABEL_FONT = '400 9px "IBM Plex Mono", monospace';
  const LABEL_FONT_ON = '600 9px "IBM Plex Mono", monospace';
  const LABEL_PAD = 3;        /* half-gutter around a box, so labels do not touch */
  const LABEL_BUDGET = 220;   /* frame budget; the cap is drawn labels, not candidates */
  const POINTER_R = 190;      /* change 3: the proximity radius, in screen px */
  const LABEL_MAX = 37;       /* the packed map's own ceiling, borrowed deliberately */
  let lastBoxes = [];
  let LABEL_HL = null;
  let ptr = null;             /* screen-space pointer, or null when off-canvas */

  /* MIDDLE truncation, so the distinguishing tail survives. The packed map settled
     this: `NATIONAL ARCHIVES UNIDE...` discards the part that tells you which
     archive. The rule is borrowed rather than the code, because l0Fit lives in
     another module's closure and a second copy of a renderer's own truncation is
     the thing this repo has been bitten by. */
  function labelFit(t){
    t = String(t || '');
    /* A TRAILING PARENTHETICAL IS DISAMBIGUATION, NOT A NAME, and it is the first
       thing to go. `ttsa` ships as "To The Stars Academy of Arts & Science Inc.
       (later To The Stars Inc.)" -- 69 characters, of which 26 are a rename note.
       Middle-truncating that whole string produced "TO THE STARS…STARS INC.)",
       which is not a label, it is two halves of the same three words. Dropping
       the parenthetical first leaves a name that survives truncation. The
       parenthetical is still in the dossier, which is where it belongs. */
    const cut = t.replace(/\s*\([^()]*\)\s*$/, '');
    if (cut.length >= 8) t = cut;
    if (t.length <= LABEL_MAX) return t;
    const keep = LABEL_MAX - 1, head = Math.ceil(keep / 2), tail = keep - head;
    return t.slice(0, head) + '…' + t.slice(t.length - tail);
  }

  function drawLabelPass(ctx, cand, W, H){
    lastBoxes = [];
    if (!cand.length) return;
    /* THE ORIGIN OF THE OUTWARD WALK. Design's algorithm walks candidates outward
       from the pointer, or the viewport centre when the pointer is off-canvas.
       A selection is a third origin and it outranks the centre: the reader has
       said which node they care about, so the labels that matter are the ones
       nearest THAT node, not the ones nearest the middle of the window.

       Without this the neighbours were ordered by their distance from the viewport
       centre, so on tom-delonge the wide `ttsa` label -- 69 characters, the widest
       in that cluster -- lost its box to two shorter neighbours that happened to
       sit closer to the middle of the screen. TTSA is the organisation DeLonge
       founded and the first line of his dossier; losing it to a coin-flip on
       viewport geometry is the defect wearing a smaller hat.

       The origin is read from S.sel and the node list, NOT from the candidates.
       A selected person draws as a full plate and returns before the label push,
       so it is never a candidate -- taking the origin from `cand.find(c => c.sel)`
       found nothing and fell back to the viewport centre without saying so, which
       is a silent no-op of exactly the kind this repo keeps paying for. */
    let sel0 = null;
    if (typeof S !== 'undefined' && S.sel)
      sel0 = (nodes || []).find(n => n.id === S.sel) || null;
    const cx = ptr ? ptr.x : (sel0 ? cam.x + sel0.x * cam.k : W / 2);
    const cy = ptr ? ptr.y : (sel0 ? cam.y + sel0.y * cam.k : H / 2);

    /* Screen position, and the highlight flag. HIGHLIGHTS FIRST is the one
       exception Design allows, and it is editorial rather than structural: these
       fourteen are Stewart's signed-off START HERE flags. Degree is never read. */
    const HL = LABEL_HL || (LABEL_HL = new Set(
      (((typeof L0DATA !== 'undefined' && L0DATA.highlights) || {}).flags || [])
        .map(f => f.id)));
    /* PAGE POISON, the _LAYOUT_OVERRIDE pattern. tools/runtime_check.js sets this
       to make the pass forget which nodes are adjacent to the selection -- the
       exact state the board shipped in until 30 August. It corrupts the real
       renderer on a real frame, not the probe that reads it, so the neighbour
       check has to collapse when it is set or that check is not looking at
       anything. */
    const NOCON = typeof window !== 'undefined' && !!window.__LABEL_NO_CON;
    for (const c of cand){
      if (NOCON) c.con = false;
      c.sx = cam.x + c.n.x * cam.k;
      /* the mark scales with the camera and the label does not, so the offset
         that clears it is the mark's SCREEN radius plus a fixed gap. */
      c.sy = cam.y + c.n.y * cam.k + (c.rw || 0) * cam.k + 5;
      c.hl = HL.has(c.n.id);
      c.d2 = (c.sx - cx) * (c.sx - cx) + (c.sy - cy) * (c.sy - cy);
      c.near = c.d2 <= POINTER_R * POINTER_R;
    }
    /* THE SELECTION'S NEIGHBOURS ARE THE POINT OF SELECTING. Reported from the
       live board on 30 August 2026: clicking Tom DeLonge lit his edges and named
       none of the nodes at the far end of them. "This defeats the purpose", and it
       did.

       Two causes, both here. `drawNode` computes state === 'connected' and then
       dropped it -- the push carried sel, hov and dim, so by the time the pass ran
       a neighbour was indistinguishable from any of the other 900 nodes and was
       ordered purely on its distance from the screen centre. And the dimmed
       remainder competed for the same budget and the same collision boxes while
       being drawn at 0.16 alpha in PALETTE.faint, which is to say illegibly: a
       label nobody can read was suppressing one they had just asked for.

       So `con` now rides on the candidate, ranks directly behind the selection
       itself, and draws regardless of the budget. And while a selection is
       active a dimmed node is not a candidate at all.

       THIS IS NOT SELECTION BY RANK and does not reopen what Design ruled out.
       Degree is a global property -- it names the same nodes for every reader, on
       every frame, which is why it may not decide who gets a name. Adjacency to
       the selection is the reader's own action, scoped to the node they clicked,
       and it is the same category as `sel` and `hov`, which have always jumped the
       queue. With nothing selected `active` is null, no node is connected or
       dimmed, and this ordering is byte-for-byte the one that shipped -- which is
       what keeps the two rest-state checks meaning what they meant. */
    cand.sort((a, b) =>
      (b.hl - a.hl) || ((b.sel || b.hov) - (a.sel || a.hov))
      || ((b.con | 0) - (a.con | 0)) || (a.d2 - b.d2));

    ctx.save();
    ctx.textAlign = 'center'; ctx.textBaseline = 'top';
    let drawn = 0;
    /* A selection is live iff something in this frame is dimmed. Read off the
       candidates rather than off S.sel, so the pass stays a pure function of what
       the node loop actually drew. */
    const picking = !NOCON && cand.some(c => c.dim);
    for (const c of cand){
      /* An illegible label is not worth a collision box. */
      if (picking && c.dim) continue;
      if (drawn >= LABEL_BUDGET && !c.near && !c.sel && !c.hov && !c.con) continue;
      const text = labelFit(c.text);
      ctx.font = (c.sel || c.hov || c.near || c.con) ? LABEL_FONT_ON : LABEL_FONT;
      const w = ctx.measureText(text).width, h = 11;
      const rw = (c.rw || 0) * cam.k;
      /* MORE THAN ONE PLACE TO PUT IT, for the selection's neighbours only.
         Still choosing by space and never by rank, and still one size -- this
         offers a label a second and third slot before giving up on it, rather
         than making it smaller. It is scoped to `con` because that is where a
         reader has explicitly asked for coverage; extending it to the whole map
         would densify the rest state, which Design deliberately kept sparse.

         Below first, so the common case is unchanged and the map still reads as
         "name under mark". `ttsa` and `steve-justice` sit at the SAME screen
         point on tom-delonge -- the force layout put them there -- so with one
         slot each only one of them could ever be named. */
      const up = -(rw + 5) - h - LABEL_PAD * 2, dn = rw + 5;
      const side = w / 2 + rw + 6;
      const slots = c.con
        ? [[0, dn], [0, up], [side, -h / 2], [-side, -h / 2],
           [side, dn], [-side, dn], [side, up], [-side, up]]
        : [[0, dn]];
      const baseY = cam.y + c.n.y * cam.k;
      let box = null, off = null;
      for (const sl of slots){
        const bx = c.sx + sl[0] - w / 2 - LABEL_PAD, by = baseY + sl[1] - LABEL_PAD;
        const cand2 = { x: bx, y: by, w: w + LABEL_PAD * 2, h: h + LABEL_PAD * 2, id: c.n.id };
        if (cand2.x + cand2.w < 0 || cand2.x > W || cand2.y + cand2.h < 0 || cand2.y > H) continue;
        /* SKIP, do not shrink and do not truncate to fit. A label that has to be
           made smaller to survive is a label the map does not have room for, and
           shrinking it would make size mean something again. */
        let hit = false;
        for (const b of lastBoxes){
          if (cand2.x < b.x + b.w && cand2.x + cand2.w > b.x &&
              cand2.y < b.y + b.h && cand2.y + cand2.h > b.y){ hit = true; break; }
        }
        if (!hit){ box = cand2; off = sl; break; }
        if (!box){ box = cand2; off = sl; }   /* remember the first, for sel/hov */
      }
      if (!box) continue;
      let hit = false;
      for (const b of lastBoxes){
        if (box.x < b.x + b.w && box.x + box.w > b.x &&
            box.y < b.y + b.h && box.y + box.h > b.y){ hit = true; break; }
      }
      if (hit && !c.sel && !c.hov) continue;
      c.sx = c.sx + off[0];
      c.sy = baseY + off[1];
      ctx.globalAlpha = c.dim ? 0.16 : (c.near || c.sel || c.hov || c.con ? 1 : 0.72);
      ctx.fillStyle = c.dim ? PALETTE.faint
                    : (c.sel || c.hov) ? PALETTE.text
                    : (c.near || c.con) ? PALETTE.text : PALETTE.dim;
      ctx.fillText(text, c.sx, c.sy);
      lastBoxes.push(box);
      drawn++;
    }
    ctx.restore();
    ctx.globalAlpha = 1;
  }
"""


NETWORK_CSS = r"""
/* ---- the reverse bridge, network map -> program map --------------------- */
/* Sits under the zoom cluster on the right, which is where the map's own camera
   controls already are: this is a camera action too, just one that changes which
   renderer the camera belongs to. Amber, not cyan, for the same reason the FOIA
   chips are amber -- it is a pointer to somewhere else, not a statement about
   this node. */
.toprog{position:absolute;right:12px;top:74px;z-index:5}
.toprog .hopb{border-color:#3a2f1c;color:#efb555;background:#191510;
  max-width:280px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.toprog .hopb:hover{border-color:#efb555;color:#f4d59a}
"""
