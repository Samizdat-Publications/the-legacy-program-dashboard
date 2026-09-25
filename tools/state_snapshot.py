#!/usr/bin/env python3
"""Print the board's current state, derived from source. Nothing is hardcoded.

WHY THIS EXISTS
---------------
Every handoff document this project has written has gone stale, and none of them
looked stale. On 24 August a fresh-session audit found README.md advertising
counts from an earlier research wave, PROJECT.md naming a repository the project
had left, and TESTING-CHECKLIST.md asserting that a component was "already
working as designed" when it was answering questions about a different project
entirely. All three read as current and confident.

So the handoff does not state figures. It tells the reader to run this, and this
derives them. A number that cannot drift out of sync with the thing it describes
cannot mislead the next session.

USAGE
    python3 tools/state_snapshot.py            # human-readable
    python3 tools/state_snapshot.py --json     # machine-readable
    python3 tools/state_snapshot.py --gate     # then run tools/gate.py (slow); its
                                               # --quick, --no-build, --no-app and
                                               # --idempotent pass straight through

Read CLAUDE.md first. This tells you WHAT is here; CLAUDE.md tells you the rules.
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _p(*parts):
    return os.path.join(ROOT, *parts)


def _load(rel):
    path = _p(*rel.split("/"))
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _mb(rel):
    path = _p(*rel.split("/"))
    return round(os.path.getsize(path) / 1e6, 2) if os.path.exists(path) else None


def collect():
    out = {}

    board = _load("data/the-program.json") or {}
    people = board.get("people", [])
    entities = board.get("entities", [])
    nodes = people + entities

    tiers = {1: 0, 2: 0, 3: 0}
    sources = set()
    claims = 0
    for n in nodes:
        for c in n.get("claims", []):
            claims += 1
            t = c.get("tier")
            if t in tiers:
                tiers[t] += 1
            if c.get("source"):
                sources.add(c["source"])

    cls = {}
    for n in entities:
        cls[n.get("cls", "?")] = cls.get(n.get("cls", "?"), 0) + 1

    out["board"] = {
        "nodes": len(nodes),
        "people": len(people),
        "entities": len(entities),
        "entityClasses": dict(sorted(cls.items(), key=lambda kv: -kv[1])),
        "edges": len(board.get("edges", [])),
        "timeline": len(board.get("timeline", [])),
        "claims": claims,
        "claimTiers": {"T1": tiers[1], "T2": tiers[2], "T3": tiers[3]},
        "primaryRecordShare": (round(tiers[1] / claims * 100) if claims else None),
        "uniqueSourceUrls": len(sources),
    }

    model = _load("data/l0-model.json") or {}
    l0 = model.get("l0", [])
    out["programMap"] = {
        "l0Nodes": len(l0),
        "withDossier": sum(1 for n in l0 if n.get("dossier")),
        "floor": (model.get("config") or {}).get("floor"),
        "degreeIs": (model.get("config") or {}).get("degreeIs"),
        "entryPaths": {p["id"]: len(p["ids"]) for p in model.get("entryPaths", [])},
    }

    layout = _load("data/l0-layout-model.json") or {}
    cur = layout.get("current") or {}
    fig = cur.get("figures") or {}
    out["layout"] = {
        "generated": layout.get("generated"),
        "l0": fig.get("l0"),
        "edgesAtRest": fig.get("restDrawn"),
        "edgesBeforeBudget": fig.get("drawnBeforeBudget"),
        "restPct": fig.get("restPct"),
        "bandOrderBasis": fig.get("bandOrderBasis"),
        # These live under `figures`, not at the top of `current`. Reading them
        # from the wrong path reported "no residual bands" and "no drift" on a
        # model that carries two of the first and, on the legacy dataset, two of
        # the second. A snapshot that quietly says "none" when it means "I looked
        # in the wrong place" is the exact failure this script exists to prevent.
        "rarityDrift": fig.get("rarityDrift"),
        "residualBands": fig.get("residualBands"),
        "legacyRarityDrift": ((layout.get("legacy") or {}).get("figures") or {}).get("rarityDrift"),
        "highlightsFlagged": fig.get("flagged"),
        "photoClears": fig.get("photoClears"),
        "photoAsk": fig.get("photoAsk"),
        "photoMissing": fig.get("photoMissing"),
    }

    hl = _load("data/l0-highlights.json") or {}
    out["highlights"] = {
        "count": len(hl.get("flags", [])),
        "authoredFor": hl.get("authoredFor"),
        "status": "DRAFT, needs Stewart's sign-off"
        if "DRAFT" in str(hl.get("_status", ""))
        else "signed off",
        "ids": [f["id"] for f in hl.get("flags", [])],
    }

    img = _load("data/l0-images.json") or {}
    _recs = img.get("images", {})
    _clears = sum(1 for v in _recs.values() if v.get("clearance") == "clears")
    _ask = sum(1 for v in _recs.values() if v.get("clearance") == "ask")
    # The note was a HARDCODED "empty on purpose" and stayed that way through nine
    # records and then twelve, in the one tool whose whole purpose is that a number
    # cannot drift out of sync with the thing it describes. Derived now, like
    # everything else here.
    out["images"] = {
        "records": len(_recs),
        "clears": _clears,
        "ask": _ask,
        "note": ("empty on purpose -- an image URL is a sourcing claim"
                 if not _recs else
                 f"{_clears} clear, {_ask} ask -- every record names a URL that was opened"),
    }

    out["artifacts"] = {
        "data/the-program.json": _mb("data/the-program.json"),
        "data/l0-model.json": _mb("data/l0-model.json"),
        "data/design-extract.json": _mb("data/design-extract.json"),
        "data/l0-layout-model.json": _mb("data/l0-layout-model.json"),
    }
    out["overGithubReadCap"] = sorted(
        k for k, v in out["artifacts"].items() if v and v > 1.0
    )

    try:
        out["git"] = {
            "head": subprocess.run(
                ["git", "log", "--oneline", "-1"],
                capture_output=True, text=True, cwd=ROOT).stdout.strip(),
            "dirty": bool(subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=ROOT).stdout.strip()),
        }
    except Exception as exc:                                  # pragma: no cover
        out["git"] = {"error": str(exc)}

    return out


GATE_FLAGS = ("--quick", "--no-build", "--no-app", "--idempotent")


def run_gate(args, capture):
    """tools/gate.py, with the gate flags passed through. Returns (exit, output).

    This used to hold the gate itself: a list of commands that drove the old
    single-file shell, three of them needing it served on port 8899. The old
    shell is retired and the gate is tools/gate.py; this only calls it."""
    cmd = [sys.executable, _p("tools", "gate.py")] + [a for a in args if a in GATE_FLAGS]
    if capture:
        r = subprocess.run(cmd, capture_output=True, cwd=ROOT)
        out = (r.stdout or b"").decode("utf-8", "replace")
        return r.returncode, out
    return subprocess.run(cmd, cwd=ROOT).returncode, None


def main():
    args = sys.argv[1:]
    state = collect()

    if "--json" in args:
        rc = 0
        if "--gate" in args:
            rc, out = run_gate(args, capture=True)
            state["gate"] = {"exit": rc, "tail": out.strip().splitlines()[-24:]}
        print(json.dumps(state, indent=2))
        return 1 if rc else 0

    def head(t):
        print("\n" + t + "\n" + "-" * len(t))

    print("THE PROGRAM -- state derived from source, %s" % state["layout"].get("generated"))
    print("Read CLAUDE.md for the rules. This file only reports what is here.")

    head("board")
    b = state["board"]
    print("  %d nodes (%d people, %d entities) - %d edges - %d timeline events"
          % (b["nodes"], b["people"], b["entities"], b["edges"], b["timeline"]))
    print("  %d claims: T1 %d / T2 %d / T3 %d  (%s%% rest on a primary record)"
          % (b["claims"], b["claimTiers"]["T1"], b["claimTiers"]["T2"],
             b["claimTiers"]["T3"], b["primaryRecordShare"]))
    print("  %d unique source URLs" % b["uniqueSourceUrls"])

    head("program map (L0)")
    m = state["programMap"]
    print("  %d nodes above a floor of %s (%s), %d with dossiers"
          % (m["l0Nodes"], m["floor"], m["degreeIs"], m["withDossier"]))
    print("  entry paths: " + " · ".join("%s %d" % kv for kv in m["entryPaths"].items()))

    head("layout")
    ly = state["layout"]
    print("  %s edges at rest of %s (%s%%), bands by %s"
          % (ly["edgesAtRest"], ly["edgesBeforeBudget"], ly["restPct"], ly["bandOrderBasis"]))
    print("  rarity drift on current data: %s"
          % ("none" % () if not ly["rarityDrift"] else ly["rarityDrift"]))
    if ly.get("legacyRarityDrift"):
        print("  rarity drift on the superseded legacy snapshot: %s"
              % ", ".join("%s observed %d / pinned %d"
                          % (d["tag"], d["observedRank"], d["pinnedRank"])
                          for d in ly["legacyRarityDrift"]))
        print("    ^ this is the pin WORKING, not failing. Do not edit RARITY_PIN to silence it.")
    print("  residual bands: %s" % (", ".join(ly["residualBands"]) if ly["residualBands"] else "none"))
    if ly.get("residualBands"):
        print("    ^ a tag held by more than half the map. Its row is a residual, not a")
        print("      category, and Design's answer is: do NOT promote it by hand.")
    print("  images: %s clear, %s ask, %s falling back to the class letter"
          % (ly["photoClears"], ly["photoAsk"], ly["photoMissing"]))

    head("editorial layers")
    h = state["highlights"]
    print("  highlights: %d flags, authored for `%s` -- %s"
          % (h["count"], h["authoredFor"], h["status"]))
    print("  images register: %d records (%s)"
          % (state["images"]["records"], state["images"]["note"]))

    head("artifacts")
    for k, v in state["artifacts"].items():
        cap = "  <-- OVER the ~1MB GitHub API read cap" if v and v > 1.0 else ""
        print("  %-32s %6s MB%s" % (k, v, cap))

    head("git")
    print("  %s" % state["git"].get("head"))
    print("  working tree: %s" % ("DIRTY" if state["git"].get("dirty") else "clean"))

    if "--gate" in args:
        head("gate (tools/gate.py)")
        sys.stdout.flush()
        rc, _ = run_gate(args, capture=False)
        if rc:
            print("\n  NOT GREEN. Do not build on this until it is.")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
