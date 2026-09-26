#!/usr/bin/env python3
"""The whole build, in the one order that produces a correct board.

    python tools/build.py

Stops at the first step that fails and says which one. Prints how long each step
took. Every step is a script that can also be run on its own.

THE ORDER, AND WHY IT IS THIS ORDER

  merge                 research/*.json -> data/the-program.json
  regrade               reads the merged board, writes research/_remediation.json
  merge                 AGAIN, on purpose: _remediation.json is itself an input to
                        merge, so one pass would ship the board regrade was about to fix
  build_foia_links      data/foia-links.json, from the FOIA letters, the board and
                        the entity dossiers (tools/dossiers.py)
  build_source_registry research/_sources.json and _claim_sources.json (phase 8): every
                        source the board cites, and each claim's sources, from the
                        merged board and research/_source_decisions.json
  build_app_data        app/public/data/, what the shipped app reads. It reads
                        everything above it
  propose_members       research/topics/_proposals.json, the topic membership
                        proposals (redesign phase 4). Last, because it reads the
                        shipped board that build_app_data has just written

Until 25 September 2026 this was tools/build.sh, which ended in build_dashboard.py:
the old single-file shell, which also ran the FOIA step inside itself. The old shell
is retired and the FOIA step is a step of its own.

Until 26 September 2026 (redesign phase 11) three more stages ran between the second
merge and build_foia_links: build_l0 (data/l0-model.json, the L0 program map model
and its dossiers), build_design_extract (data/design-extract.json) and
build_l0_layout.mjs (data/l0-layout-model.json, the packed map layout). The map
retired and they went with it; the dossiers load through tools/dossiers.py.
"""

import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STEPS = (
    ("merge", ["merge.py"]),
    ("regrade", ["regrade.py"]),
    ("merge (again)", ["merge.py"]),
    ("build_foia_links", ["build_foia_links.py"]),
    ("build_source_registry", ["build_source_registry.py"]),
    ("build_app_data", ["build_app_data.py"]),
    ("propose_members", ["topics/propose_members.py"]),
)


def command(script):
    path = os.path.join(ROOT, "tools", script)
    if script.endswith((".mjs", ".js")):
        return ["node", path]
    return [sys.executable, path]


def main(argv):
    if argv:
        print(__doc__)
        return 0 if argv[0] in ("-h", "--help") else 2
    rows = []
    failed = None
    t_all = time.time()
    for name, (script,) in STEPS:
        print(f"== {name}", flush=True)
        t0 = time.time()
        r = subprocess.run(command(script), cwd=ROOT)
        dt = time.time() - t0
        rows.append((name, "ok" if r.returncode == 0 else f"FAIL ({r.returncode})", dt))
        if r.returncode != 0:
            failed = name
            break
    print()
    print(f"{'step':<24} {'result':<10} {'seconds':>8}")
    for name, res, dt in rows:
        print(f"{name:<24} {res:<10} {dt:>8.1f}")
    print(f"{'total':<24} {'':<10} {time.time() - t_all:>8.1f}")
    if failed:
        print(f"\nbuild FAILED at {failed}; later steps did not run", file=sys.stderr)
        return 1
    print("\nbuild ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
