#!/usr/bin/env python3
"""Print a cached transcript as plain text with timestamps.

The cache stores {"id": ..., "segments": [{"t": seconds, "text": ...}]}, which is
the right shape to keep but the wrong shape to read. This folds the segments into
timestamped paragraphs so a reader can cite a position in the video.

    python3 tools/read_transcript.py <video-id> [--from MIN] [--to MIN]
    python3 tools/read_transcript.py --list

Timestamps are the START of each block, printed as [HH:MM:SS], so a citation
points at something a person can scrub to. Auto-generated captions carry no
speaker labels; do not invent them.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "research", ".transcripts")


def hms(t):
    t = int(t)
    return "%02d:%02d:%02d" % (t // 3600, (t % 3600) // 60, t % 60)


def main():
    args = sys.argv[1:]
    if not args or "--list" in args:
        for f in sorted(glob.glob(os.path.join(CACHE, "*.json"))):
            d = json.load(open(f, encoding="utf-8"))
            segs = d.get("segments", [])
            w = sum(len(s.get("text", "").split()) for s in segs)
            print("%-14s %7d words  %6.1f min" %
                  (d.get("id"), w, (segs[-1]["t"] / 60.0) if segs else 0))
        return 0

    vid = args[0]
    lo = hi = None
    if "--from" in args:
        lo = float(args[args.index("--from") + 1]) * 60
    if "--to" in args:
        hi = float(args[args.index("--to") + 1]) * 60

    path = os.path.join(CACHE, vid + ".json")
    if not os.path.exists(path):
        print("no such transcript: %s" % vid, file=sys.stderr)
        return 1
    d = json.load(open(path, encoding="utf-8"))

    buf, start = [], None
    for s in d.get("segments", []):
        t, txt = s.get("t", 0), (s.get("text") or "").strip()
        if not txt:
            continue
        if lo is not None and t < lo:
            continue
        if hi is not None and t > hi:
            break
        if start is None:
            start = t
        buf.append(txt)
        # Flush roughly every 30 seconds, so a block is a citable unit.
        if t - start >= 30:
            print("[%s] %s\n" % (hms(start), " ".join(buf)))
            buf, start = [], None
    if buf:
        print("[%s] %s" % (hms(start or 0), " ".join(buf)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
