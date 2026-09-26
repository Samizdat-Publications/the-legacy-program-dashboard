#!/usr/bin/env python3
"""validate_batch.py: check one classifier's answers against its packets and the vocabulary.

Redesign phase 7 task 3. A classifier (or reviewer) runs this on its own output
before handing back, and the coordinator runs it again on everything it merges:

  python tools/predicates/validate_batch.py PACKETS.json ANSWERS.json

ANSWERS is a JSON list of {id, predicate, subject: "a"|"b", confidence:
"high"|"medium"|"low", reason}. It fails (exit 1, one line per fault) on: an id
missing, extra or twice; a predicate not in schema/vocab.json; a subject other
than a or b; a symmetric predicate whose subject is not a; an end whose class the
predicate does not allow (domain nodes are allowed anywhere); a confidence outside
the three words; and a denial-family predicate whose subject is not the edge's
adjudicated denier.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def vocab():
    v = json.load(open(os.path.join(ROOT, "schema", "vocab.json"), encoding="utf-8"))
    return {p["id"]: p for p in v["predicates"]}


def allowed(spec, cls):
    return cls == "domain" or spec == "any" or cls in spec


def problems(packets, answers, preds=None):
    preds = preds or vocab()
    byid = {p["id"]: p for p in packets}
    bad, seen = [], set()
    for r in answers:
        i = r.get("id")
        if i not in byid:
            bad.append(f"{i}: not an edge in the packets")
            continue
        if i in seen:
            bad.append(f"{i}: answered twice")
        seen.add(i)
        p, pr = byid[i], preds.get(r.get("predicate"))
        if pr is None:
            bad.append(f"{i}: predicate {r.get('predicate')!r} is not in schema/vocab.json")
            continue
        s = r.get("subject")
        if s not in ("a", "b"):
            bad.append(f"{i}: subject {s!r} must be 'a' or 'b'")
            continue
        if pr.get("symmetric") and s != "a":
            bad.append(f"{i}: {pr['id']} is symmetric, so its subject is recorded as 'a'")
        subj, obj = (p["a"], p["b"]) if s == "a" else (p["b"], p["a"])
        if not allowed(pr["subject"], subj["cls"]):
            bad.append(f"{i}: {pr['id']} does not allow a {subj['cls']} as subject ({subj['id']})")
        if not allowed(pr["object"], obj["cls"]):
            bad.append(f"{i}: {pr['id']} does not allow a {obj['cls']} as object ({obj['id']})")
        if r.get("confidence") not in ("high", "medium", "low"):
            bad.append(f"{i}: confidence {r.get('confidence')!r} must be high, medium or low")
        den = p.get("denier")
        if pr["family"] == "denial" and den in (p["a"]["id"], p["b"]["id"]) and subj["id"] != den:
            bad.append(f"{i}: {pr['id']} makes {subj['id']} the denier, but the adjudicated denier is {den}")
    for i in byid:
        if i not in seen:
            bad.append(f"{i}: no answer")
    return bad


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    packets = json.load(open(sys.argv[1], encoding="utf-8"))
    answers = json.load(open(sys.argv[2], encoding="utf-8"))
    bad = problems(packets, answers)
    for b in bad:
        print(b)
    print(f"{len(answers)} answers for {len(packets)} edges: "
          + ("OK" if not bad else f"{len(bad)} problem(s)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
