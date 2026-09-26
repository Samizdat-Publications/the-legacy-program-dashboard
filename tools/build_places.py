#!/usr/bin/env python3
"""The board's places, as the app ships them: app/public/data/places.json.

    python tools/build_places.py            build
    python tools/build_places.py --check    re-derive and fail if the shipped file differs

Redesign phase 11, task 3 (notes/plans/P11-graph-views-places.md). One record per
location node on the merged board, in id order:

  label           the node's own label
  lat, lon, loc   from research/_places.json, and ONLY from there. A place the side-car
                  does not carry has none, and the page says so rather than guessing
  coordSource     which source in the side-car's `_sources` the coordinates came from
  country, region read off the side-car's `loc` ("Roswell, New Mexico, USA": country
                  USA, region New Mexico; "Paris, France": country France, no region).
                  Nothing is inferred from the node's name
  events          the event nodes a board edge ties to the place, with their start
                  dates, and the timeline entries filed under the place itself
  topics          the topics whose members hold the place, primary first, read from
                  app/public/data/topics.json (so this step runs after build_app_data)

Nothing here invents a coordinate, a country or a link: every value is copied from
a file above or counted from the board. The output is a function of its inputs'
content only, written with sorted keys, so a rebuild is byte-identical.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(ROOT, "data", "the-program.json")
PLACES = os.path.join(ROOT, "research", "_places.json")
TOPICS = os.path.join(ROOT, "app", "public", "data", "topics.json")
OUT = os.path.join(ROOT, "app", "public", "data", "places.json")


def rd(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def split_loc(loc):
    """(country, region) from a side-car `loc`, by its commas and nothing else."""
    if not loc:
        return None, None
    parts = [x.strip() for x in loc.split(",") if x.strip()]
    country = parts[-1] if parts else None
    region = parts[-2] if len(parts) >= 3 else None
    return country, region


def build():
    board = rd(BOARD)
    side = rd(PLACES)
    table = side.get("places") or {}
    topics = rd(TOPICS)
    title = {t["id"]: t["title"] for t in topics.get("topics") or []}
    appears = topics.get("appearsIn") or {}
    nodes = board["people"] + board["entities"]
    byid = {n["id"]: n for n in nodes}
    locs = sorted((n for n in nodes if n.get("cls") == "location"), key=lambda n: n["id"])

    out = []
    for n in locs:
        pid = n["id"]
        rec = table.get(pid) or {}
        lat, lon = rec.get("lat"), rec.get("lon")
        has = isinstance(lat, (int, float)) and isinstance(lon, (int, float))
        country, region = split_loc(rec.get("loc")) if has else (None, None)
        evs = {}
        for e in board["edges"]:
            other = e["b"] if e["a"] == pid else e["a"] if e["b"] == pid else None
            if not other or other == pid:
                continue
            o = byid.get(other)
            if not o or o.get("cls") != "event":
                continue
            evs[other] = {"id": other, "label": o["label"], "date": o.get("dateStart") or None, "kind": "node"}
        for t in board.get("timeline") or []:
            if t.get("node") == pid:
                evs[t["id"]] = {"id": t["id"], "label": t["label"], "date": t.get("date") or None, "kind": "timeline"}
        events = sorted(evs.values(), key=lambda x: (x["date"] or "9999", x["label"], x["id"]))
        tops = [{"id": a[0], "title": title.get(a[0], a[0])} for a in appears.get(pid) or [] if a and a[0] in title]
        out.append({
            "id": pid, "label": n["label"],
            "lat": lat if has else None, "lon": lon if has else None,
            "loc": rec.get("loc") if has else None,
            "coordSource": rec.get("coordSource") if has else None,
            "country": country, "region": region,
            "events": events, "topics": tops,
        })
    return {
        "generated": board.get("generated"),
        "coordSources": {k: v for k, v in (side.get("_sources") or {}).items()},
        "places": out,
    }


def text(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def main(argv):
    got = build()
    if argv and argv[0] == "--check":
        have = open(OUT, encoding="utf-8").read().replace("\r\n", "\n") if os.path.exists(OUT) else ""
        if have != text(got):
            print("places.json differs from a fresh derivation: run python tools/build_places.py", file=sys.stderr)
            return 1
        print("places.json ok: %d places, %d with coordinates"
              % (len(got["places"]), sum(1 for p in got["places"] if p["lat"] is not None)))
        return 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text(got))
    print("places.json: %d places, %d plotted, %d with events"
          % (len(got["places"]), sum(1 for p in got["places"] if p["lat"] is not None),
             sum(1 for p in got["places"] if p["events"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
