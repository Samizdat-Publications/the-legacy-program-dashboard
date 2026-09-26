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

    # The L0 program map, its model and its packed layout retired in redesign
    # phase 11 (26 September 2026). The entity dossiers outlived them: they ship on
    # each node's file in app/public/data/nodes/, loaded by tools/dossiers.py.
    sys.path.insert(0, _p("tools"))
    import dossiers  # noqa: E402
    ids = {n.get("id") for n in nodes}
    have = dossiers.dossier_ids()
    out["dossiers"] = {
        "authored": len(have),
        "onBoard": len(have & ids),
    }
    out["generated"] = board.get("generated")

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
        "app/public/data/index.json": _mb("app/public/data/index.json"),
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

    print("THE PROGRAM -- state derived from source, %s" % state.get("generated"))
    print("Read CLAUDE.md for the rules. This file only reports what is here.")

    head("board")
    b = state["board"]
    print("  %d nodes (%d people, %d entities) - %d edges - %d timeline events"
          % (b["nodes"], b["people"], b["entities"], b["edges"], b["timeline"]))
    print("  %d claims: T1 %d / T2 %d / T3 %d  (%s%% rest on a primary record)"
          % (b["claims"], b["claimTiers"]["T1"], b["claimTiers"]["T2"],
             b["claimTiers"]["T3"], b["primaryRecordShare"]))
    print("  %d unique source URLs" % b["uniqueSourceUrls"])

    head("entity dossiers")
    d = state["dossiers"]
    print("  %d authored in research/dossiers/, %d on nodes of this board"
          % (d["authored"], d["onBoard"]))

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
