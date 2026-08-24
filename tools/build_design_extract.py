#!/usr/bin/env python3
"""
build_design_extract.py -- a purpose-built extract for Claude Design, UNDER 1MB.

WHY THIS EXISTS
---------------
GitHub's file read caps around 1MB. `data/the-program.json` is 6.9MB and
`data/l0-model.json` is 5.7MB. Both are tracked and pushed, but to anything
reading the repo over the API they appear ABSENT -- which is exactly what
happened: the design brief cited both, and Design correctly reported that
neither was in the repo at HEAD and refused to reproduce figures it could not
read. It was right to refuse.

This is the same trap the original handoff recorded as its seventh build trap,
and I failed to carry it into the brief I wrote. So: one file, under the cap,
carrying exactly what the layout work needs and nothing else.

Everything here is DERIVED at build time. No figure is typed.
"""
import json, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "design-extract.json")
CAP = 1_000_000


def main():
    b = json.load(open(os.path.join(ROOT, "data", "the-program.json"), encoding="utf-8"))
    m = json.load(open(os.path.join(ROOT, "data", "l0-model.json"), encoding="utf-8"))
    N = {n["id"]: n for n in b["people"] + b["entities"]}

    def era(ds):
        if not ds or not str(ds)[:4].isdigit():
            return None
        y = int(str(ds)[:4])
        return ("1940-1969" if y < 1970 else "1970-1999" if y < 2000
                else "2000-2016" if y < 2017 else "2017-2026")

    l0 = []
    for n in m["l0"]:
        src = N.get(n["id"], {})
        d = n.get("dossier") or {}
        l0.append({
            "id": n["id"], "label": n["label"], "short": n["short"],
            "cls": n["cls"], "cluster": n["cluster"], "tier": n["tier"],
            "deg": n["deg"], "x": n["x"], "y": n["y"],
            "members": len(n["direct"]) + len(n["routed"]),
            "mix": n["mix"], "di": n["di"], "dr": n["dr"],
            "claims": n["claims"], "t1": n["t1"],
            # the two dimensions the layout work turns on
            "dateStart": src.get("dateStart") or src.get("date"),
            "era": era(src.get("dateStart") or src.get("date")),
            "roles": d.get("roles") or [],
            "whyImplicated": (d.get("whyImplicated") or "")[:400],
        })

    dist = {
        "era": dict(Counter(x["era"] for x in l0 if x["era"])),
        "eraMissing": sum(1 for x in l0 if not x["era"]),
        "roles": dict(Counter(r for x in l0 for r in x["roles"])),
        "rolesPerNode": dict(Counter(len(x["roles"]) for x in l0)),
        "cluster": dict(Counter(x["cluster"] for x in l0)),
        "cls": dict(Counter(x["cls"] for x in l0)),
        "degree": {"min": min(x["deg"] for x in l0),
                   "median": sorted(x["deg"] for x in l0)[len(l0)//2],
                   "max": max(x["deg"] for x in l0),
                   "atFloor": sum(1 for x in l0 if x["deg"] == 6),
                   "atLeast15": sum(1 for x in l0 if x["deg"] >= 15)},
        "edgeTier": {"direct": dict(Counter(e["tier"] for e in m["directEdges"])),
                     "summarised": dict(Counter(e["tier"] for e in m["summarised"]))},
        "sharedMemberCounts": dict(Counter(e["n"] for e in m["summarised"])),
    }

    out = {
        "_what": "Purpose-built extract for the layout design work. Under GitHub's "
                 "~1MB read cap, which is why it exists: the full board and the L0 "
                 "model are both tracked but far over the cap and read as absent.",
        "_source": "derived from data/the-program.json and data/l0-model.json at this commit",
        "generated": m["generated"],
        "config": m["config"],
        "counts": m["counts"],
        "distributions": dist,
        "l0": l0,
        "directEdges": [{"a": e["a"], "b": e["b"], "n": e["n"], "tier": e["tier"],
                         "types": e["types"]} for e in m["directEdges"]],
        "summarised": [{"a": e["a"], "b": e["b"], "n": e["n"], "tier": e["tier"]}
                       for e in m["summarised"]],
        "entryPaths": m.get("entryPaths", []),
        "authority": {k: {"weight": v["weight"], "tense": v["tense"],
                          "connections": v["publicRecord"]["connections"]}
                      for k, v in (m.get("authority") or {}).items()},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), separators=(",", ":"))
    size = os.path.getsize(OUT)
    print(f"design-extract.json  {size:,} bytes  ({size/CAP*100:.0f}% of the 1MB cap)")
    print(f"  L0 {len(l0)} · era {dist['era']} · missing {dist['eraMissing']}")
    print(f"  roles {dist['roles']}")
    if size >= CAP:
        sys.exit(f"FATAL: {size:,} bytes is over the {CAP:,} read cap. The whole "
                 f"point of this file is that Design can read it.")


if __name__ == "__main__":
    main()
