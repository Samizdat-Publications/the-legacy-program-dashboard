#!/usr/bin/env python3
"""edge_packets.py: the input the phase 7 classifiers read, one packet per edge.

Redesign phase 7 (notes/plans/P7-relationship-vocabulary.md), tasks 1 and 3. Each
packet carries only what the edge itself says: its stable id, both ends (id, label,
class), its type, its sentence (the edge's `label`), its note, the authored verb
phase 3 kept, its claim tier, and for a denial the adjudicated `denialKind` and
`denier`. Nothing else, on purpose: a classifier that reads more than the edge
brings outside knowledge into a field that must restate the edge.

  python tools/predicates/edge_packets.py --sample 200 [--seed 7]   print a sample
  python tools/predicates/edge_packets.py --batches 18 --out DIR     write DIR/batch-NN.json
  python tools/predicates/edge_packets.py --ids FILE --out PATH       packets for listed ids

Batches are a deterministic shuffle (seeded) so each batch mixes types, and every
edge is in exactly one batch.
"""
import json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOARD = os.path.join(ROOT, "data", "the-program.json")


def packets(board=None):
    b = board or json.load(open(BOARD, encoding="utf-8"))
    nodes = {n["id"]: n for n in b["people"] + b["entities"]}
    out = []
    for e in b["edges"]:
        a, z = nodes[e["a"]], nodes[e["b"]]
        p = {"id": e["id"],
             "a": {"id": a["id"], "label": a["label"], "cls": a["cls"]},
             "b": {"id": z["id"], "label": z["label"], "cls": z["cls"]},
             "type": e["type"],
             "sentence": e.get("label") or "",
             "note": e.get("note") or "",
             "tier": e.get("claimTier")}
        if e.get("authoredVerb"):
            p["authoredVerb"] = e["authoredVerb"]
        if e["type"] == "denial":
            p["denialKind"] = e.get("denialKind")
            p["denier"] = e.get("denier")
        out.append(p)
    out.sort(key=lambda p: p["id"])
    return out


def show(p):
    s = [f"{p['id']}  [{p['type']}] T{p['tier']}"
         + (f"  verb={p['authoredVerb']}" if p.get("authoredVerb") else "")
         + (f"  denialKind={p.get('denialKind')} denier={p.get('denier')}" if p["type"] == "denial" else ""),
         f"  a: {p['a']['label']} ({p['a']['cls']}, {p['a']['id']})",
         f"  b: {p['b']['label']} ({p['b']['cls']}, {p['b']['id']})",
         f"  sentence: {p['sentence']}"]
    if p["note"]:
        s.append(f"  note: {p['note'][:400]}")
    return "\n".join(s)


def main():
    args = sys.argv[1:]
    seed = int(args[args.index("--seed") + 1]) if "--seed" in args else 7
    ps = packets()
    if "--sample" in args:
        n = int(args[args.index("--sample") + 1])
        rnd = random.Random(seed)
        for p in sorted(rnd.sample(ps, n), key=lambda p: (p["type"], p["id"])):
            print(show(p))
            print()
        return 0
    if "--batches" in args:
        k = int(args[args.index("--batches") + 1])
        out = args[args.index("--out") + 1]
        os.makedirs(out, exist_ok=True)
        rnd = random.Random(seed)
        order = ps[:]
        rnd.shuffle(order)
        for i in range(k):
            chunk = sorted(order[i::k], key=lambda p: p["id"])
            with open(os.path.join(out, f"batch-{i + 1:02d}.json"), "w", encoding="utf-8") as fh:
                json.dump(chunk, fh, indent=1, ensure_ascii=False)
            print(f"batch-{i + 1:02d}.json  {len(chunk)} edges")
        return 0
    if "--ids" in args:
        want = set(json.load(open(args[args.index("--ids") + 1], encoding="utf-8")))
        out = args[args.index("--out") + 1]
        sel = [p for p in ps if p["id"] in want]
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(sel, fh, indent=1, ensure_ascii=False)
        print(f"{out}  {len(sel)} edges")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
