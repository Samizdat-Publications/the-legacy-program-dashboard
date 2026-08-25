#!/bin/sh
# The whole pipeline, in the one order that produces a correct board.
#
# merge runs TWICE on purpose: regrade reads the merged board to decide tiers,
# dates and coordinates and writes research/_remediation.json, which is itself
# an input to merge. One pass would ship the board that regrade was about to fix.
set -e
cd "$(dirname "$0")/.."
python3 tools/merge.py            "$@"
python3 tools/regrade.py          "$@"
python3 tools/merge.py            "$@"
python3 tools/build_l0.py         "$@"
python3 tools/build_dashboard.py  "$@"
