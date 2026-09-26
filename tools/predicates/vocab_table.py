#!/usr/bin/env python3
"""vocab_table.py: print schema/vocab.json's predicates as a Markdown table.

Used to paste the vocabulary into the phase 7 classifier and reviewer briefs, so
the brief is rendered from the one vocabulary rather than retyped.

  python tools/predicates/vocab_table.py > table.md
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    v = json.load(open(os.path.join(ROOT, "schema", "vocab.json"), encoding="utf-8"))
    fam = {f["id"]: f for f in v["predicateFamilies"]}
    out = ["| predicate | family | forward (read from subject) | inverse (read from object) "
           "| subject classes | object classes | refines type | use when |",
           "|---|---|---|---|---|---|---|---|"]
    for p in v["predicates"]:
        cl = lambda x: "any" if x == "any" else ", ".join(x)
        out.append("| `%s` | %s | %s | %s | %s | %s | %s | %s%s |" % (
            p["id"], fam[p["family"]]["label"], p["forward"], p["inverse"],
            cl(p["subject"]), cl(p["object"]), p["refines"] or "(none)", p["use"],
            " (symmetric)" if p.get("symmetric") else ""))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
