#!/usr/bin/env python3
"""merge_answers.py: fold the classifiers' and reviewers' answers into research/_predicates.json.

Redesign phase 7 task 3. Inputs, all JSON lists of {id, predicate, subject,
confidence, reason}:

  --classified DIR   the classifiers' answers, one file per batch (every edge once)
  --reviewed FILE..  the reviewers' independent answers for the edges they took
  --by-classifier S  provenance string for classifier answers
  --by-reviewer S    provenance string for reviewer answers
  --stats FILE       where to write the agreement statistics (JSON)
  --write            write research/_predicates.json (otherwise only the stats)

A reviewed edge AGREES when the predicate matches and, for a directed predicate,
the subject matches too. On disagreement the reviewer's answer wins; every reviewed
edge is marked `reviewed: true`. Every answer is validated against the packets and
the vocabulary first (tools/predicates/validate_batch.py); a single fault stops the
merge.
"""
import collections, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edge_packets  # noqa: E402
import validate_batch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "research", "_predicates.json")

WHAT = ("Redesign phase 7: one controlled predicate per board edge, keyed by the edge's "
        "stable id (phase 4). `predicate` is an id in schema/vocab.json `predicates`; "
        "`subject` is the end (a or b, in the edge's record order) the forward label reads "
        "from; `by` records who classified it; `confidence` is high, medium or low; "
        "`reviewed` is true where a second, independent reviewer re-derived it (the "
        "reviewer's answer stands on disagreement). build_app_data.py joins this onto "
        "edges.json and every node's connections; verify.py holds that every edge has "
        "one, that no key is orphaned, that classes hold and that a denial predicate "
        "reads from the adjudicated denier. A predicate never changes a type or a tier. "
        "How it was made: notes/plans/P7-classification-record.md.")


def arg(args, k, default=None):
    return args[args.index(k) + 1] if k in args else default


def multi(args, k):
    if k not in args:
        return []
    out = []
    for a in args[args.index(k) + 1:]:
        if a.startswith("--"):
            break
        out.append(a)
    return out


def load_list(paths):
    rows = []
    for p in paths:
        rows.extend(json.load(open(p, encoding="utf-8")))
    return rows


def agree(c, r, vocab):
    if c["predicate"] != r["predicate"]:
        return False
    return bool(vocab[c["predicate"]].get("symmetric")) or c["subject"] == r["subject"]


def main():
    args = sys.argv[1:]
    packets = edge_packets.packets()
    vocab = validate_batch.vocab()
    cls_files = sorted(glob.glob(os.path.join(arg(args, "--classified"), "*.json")))
    classified = load_list(cls_files)
    bad = validate_batch.problems(packets, classified, vocab)
    if bad:
        print("\n".join(bad[:30]))
        sys.exit(f"merge_answers: {len(bad)} fault(s) in the classifiers' answers")
    reviewed = load_list(multi(args, "--reviewed"))
    byid = {p["id"]: p for p in packets}
    rv_packets = [byid[r["id"]] for r in reviewed if r.get("id") in byid]
    bad = validate_batch.problems(rv_packets, reviewed, vocab)
    if bad:
        print("\n".join(bad[:30]))
        sys.exit(f"merge_answers: {len(bad)} fault(s) in the reviewers' answers")

    cmap = {r["id"]: r for r in classified}
    rmap = {r["id"]: r for r in reviewed}
    fam = lambda pid: vocab[pid]["family"]
    stats = {"edges": len(packets), "reviewed": len(rmap), "disagreements": 0,
             "byFamily": collections.defaultdict(lambda: {"reviewed": 0, "disagree": 0}),
             "byConfidence": collections.defaultdict(lambda: {"reviewed": 0, "disagree": 0}),
             "predicateOnly": 0, "directionOnly": 0, "pairs": collections.Counter(),
             "examples": []}
    out = {}
    for p in packets:
        c = cmap[p["id"]]
        row = {"predicate": c["predicate"], "subject": c["subject"],
               "by": arg(args, "--by-classifier", "classifier"),
               "confidence": c["confidence"], "reviewed": False}
        r = rmap.get(p["id"])
        if r:
            f = stats["byFamily"][fam(c["predicate"])]
            k = stats["byConfidence"][c["confidence"]]
            f["reviewed"] += 1
            k["reviewed"] += 1
            if not agree(c, r, vocab):
                stats["disagreements"] += 1
                f["disagree"] += 1
                k["disagree"] += 1
                if c["predicate"] == r["predicate"]:
                    stats["directionOnly"] += 1
                else:
                    stats["predicateOnly"] += 1
                    stats["pairs"][f"{c['predicate']} -> {r['predicate']}"] += 1
                if len(stats["examples"]) < 60:
                    stats["examples"].append({"id": p["id"], "type": p["type"],
                                              "sentence": p["sentence"][:100],
                                              "classifier": [c["predicate"], c["subject"]],
                                              "reviewer": [r["predicate"], r["subject"]],
                                              "why": r.get("reason", "")})
                row.update(predicate=r["predicate"], subject=r["subject"],
                           by=arg(args, "--by-reviewer", "reviewer"))
            row["confidence"] = r["confidence"]
            row["reviewed"] = True
        out[p["id"]] = row
    stats["rate"] = round(stats["disagreements"] / max(1, stats["reviewed"]), 4)
    stats["pairs"] = stats["pairs"].most_common(40)
    fc = collections.Counter(fam(r["predicate"]) for r in out.values())
    pc = collections.Counter(r["predicate"] for r in out.values())
    stats["final"] = {"families": dict(fc.most_common()), "predicates": dict(pc.most_common()),
                      "confidence": dict(collections.Counter(r["confidence"] for r in out.values())),
                      "connected_to": pc.get("connected_to", 0),
                      "crossings": sum(1 for p in packets
                                       if vocab[out[p["id"]]["predicate"]]["refines"] not in (None, p["type"]))}
    if arg(args, "--stats"):
        with open(arg(args, "--stats"), "w", encoding="utf-8") as fh:
            json.dump(stats, fh, indent=1, ensure_ascii=False)
    print(f"reviewed {stats['reviewed']}, disagree {stats['disagreements']} ({stats['rate']:.1%}): "
          f"predicate {stats['predicateOnly']}, direction only {stats['directionOnly']}")
    print(f"connected_to {pc.get('connected_to', 0)} of {len(out)}")
    if "--write" in args:
        with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"_what": WHAT, "edges": dict(sorted(out.items()))}, fh, indent=1,
                      ensure_ascii=False, sort_keys=True)
            fh.write("\n")
        print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
