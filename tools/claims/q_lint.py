"""q_lint.py: run only verify.py's question checks, for a drafter at work.

    python tools/claims/q_lint.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import verify  # noqa: E402

b = json.load(open(os.path.join(ROOT, "data", "the-program.json"), encoding="utf-8"))
bad = 0
for name, fn in verify.CHECKS_RUN:
    if "question" not in name:
        continue
    got = fn(b)
    print(("FAIL  " if got else "ok    ") + name)
    for g in got[:40]:
        print("        " + g)
    bad += bool(got)
sys.exit(1 if bad else 0)
