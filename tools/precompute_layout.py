#!/usr/bin/env python3
"""
precompute_layout.py — run the force layout at BUILD time and bake the result.

WHY
---
Profiling a cold load on 2026-08-12:

    51.7%  13,356ms  step             force-layout integration
     6.4%   1,648ms  applyRepulsion
     1.1%     285ms  insert
    23.7%   6,118ms  (program)        V8 parse of the 6.84 MB file
     0.3%      80ms  drawParticle2D   <- all rendering, together, under 1%

The layout is ~60% of a 19.8-second load. Barnes-Hut is already implemented and the
physics is O(n log n); the cost is that **900 integration steps over 970 nodes run
before the first paint**. Moving that to build time removes it entirely.

It also makes the map STABLE. The board currently rearranges itself on every load,
because the layout is seeded and settled fresh each time. A baked layout looks the
same on every machine and in every session, which for a research instrument is a
credibility property: positions become citable and screenshots stay valid.

HOW — and why it is extracted rather than ported
------------------------------------------------
The obvious implementation is to reimplement the force simulation in Python. That
creates two implementations of the same physics which must agree forever, and they
will not: the JS `reflow()` still runs on resize, so any drift shows up as the map
visibly jumping the first time the window changes size.

So this does not port anything. It **slices the simulation source straight out of
the freshly built HTML** and runs that exact text in Node. There is one
implementation. If someone edits the physics, this picks the edit up on the next
build with no action required.

Coordinates are baked NORMALISED (fraction of the content box) because the layout
is sized to the viewport. At runtime `initLayout` maps them into whatever box the
canvas actually is, so the bake is resolution-independent.
"""

import json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The slice: from the inset constant through the end of makeSim. Anchored on text
# that must exist, so a rename fails loudly here rather than silently degrading.
SLICE_START = "const DEFAULT_INSET"
SLICE_END = "function aggregatePairs"

# Reference content box. Bigger than any real viewport on purpose: the physics has
# absolute pixel constants (node radii, minimum separation), so a small box makes the
# graph fight its own walls and the clamp pins the overflow to the edges. Measured
# share of nodes pinned to a wall, at 900 steps: 1600x1000 -> 46%, 2400x1500 -> 31%,
# 3200x2000 -> 24%, 5000x3100 -> 20%. Coordinates are normalised out afterwards, so a
# large box costs nothing at runtime. Diminishing past ~3200 and the layout gets
# airier than the real canvas, which wastes screen.
REF_W, REF_H = 3200, 2000
STEPS = 900                 # what the live build() ran before first paint


def extract_sim(html):
    i = html.find(SLICE_START)
    j = html.find(SLICE_END)
    if i < 0 or j < 0 or j <= i:
        raise RuntimeError(
            f"cannot locate the simulation slice ({SLICE_START!r} .. {SLICE_END!r}). "
            "The map source was restructured; precompute_layout.py must be re-anchored.")
    return html[i:j]


def compute(html, nodes, edges):
    """Run the board's own layout in Node and return {id: [nx, ny]} normalised."""
    sim_src = extract_sim(html)
    harness = sim_src + """
const DATA = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
const nodes = DATA.nodes, edges = DATA.edges;
const W = %d, H = %d, ins = DEFAULT_INSET;
initLayout(nodes, W, H, ins);
const sim = makeSim(nodes, edges, W, H, ins);
for (let i = 0; i < %d; i++) sim.step();
const uw = W - ins.l - ins.r, uh = H - ins.t - ins.b;
const out = {};
for (const n of nodes) out[n.id] = [ (n.x - ins.l) / uw, (n.y - ins.t) / uh ];
process.stdout.write(JSON.stringify(out));
""" % (REF_W, REF_H, STEPS)

    with tempfile.TemporaryDirectory() as td:
        js = os.path.join(td, "layout.js")
        data = os.path.join(td, "data.json")
        open(js, "w", encoding="utf-8").write(harness)
        json.dump({"nodes": nodes, "edges": edges}, open(data, "w", encoding="utf-8"))
        r = subprocess.run(["node", js, data], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("node failed running the extracted layout:\n"
                               + r.stderr[:1200])
        return json.loads(r.stdout)


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


def layout_for(board, html):
    """Build the minimal node/edge shape the simulation needs, and run it."""
    nodes = [{"id": n["id"], "cls": n["cls"], "label": n.get("label") or n["id"],
              "cluster": n.get("cluster") or "other"}
             for n in board["people"] + board["entities"]]
    edges = [{"a": e["a"], "b": e["b"], "type": e["type"]} for e in board["edges"]]
    return compute(html, nodes, edges)


if __name__ == "__main__":
    board = json.load(open(os.path.join(ROOT, "data", "the-program.json"), encoding="utf-8"))
    html = open(os.path.join(ROOT, "dist", "the-program.html"), encoding="utf-8").read()
    xy = layout_for(board, html)
    out = os.path.join(ROOT, "data", "layout.json")
    json.dump(xy, open(out, "w", encoding="utf-8"))
    xs = [v[0] for v in xy.values()]
    ys = [v[1] for v in xy.values()]
    print(f"baked {len(xy)} positions -> {out}")
    print(f"  x range {min(xs):+.3f} .. {max(xs):+.3f}   y range {min(ys):+.3f} .. {max(ys):+.3f}")
