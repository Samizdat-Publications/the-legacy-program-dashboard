#!/usr/bin/env python3
"""apply_chair_rule.py: the orchestrator's chair tie-breaker (phase 7, 26 September 2026).

"A chair or head of a body is `led`; `member_of` is plain membership." The round-2
brief carried two tie-breakers that both covered a committee chair, so the
classifiers split. This is the targeted pass that settles it, decided edge by edge
by the coordinator from each edge's own sentence (the full candidate list was every
member_of, held_post, led or oversaw edge whose sentence says chair, preside, head or
seat; the rest already read correctly):

- a chair of the body at the far end -> `led`
- a vice chair or seat on a body -> `member_of`
- chairing a HEARING (an event, not a body) -> `oversaw`, which the vocabulary gives
  for presiding over a hearing, so every chaired hearing reads one way
- chairing a team inside a larger body, where the edge's far end is the larger body
  -> `held_post` (the edge does not name the body that was chaired)

A seat on the Waived SAP Notification Group held BY VIRTUE of chairing another
committee stays `member_of`: the group is not what they chair.

  python tools/predicates/apply_chair_rule.py      rewrites research/_predicates.json
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "research", "_predicates.json")
BY = "opus-5.5 coordinator, chair rule, 2026-09-26"

DECISIONS = {
    "e-213bf86c7d": ("led", "a"),        # Mace: "Chairwoman" of the subcommittee
    "e-3abfb450e2": ("member_of", "a"),  # Rubio: Vice Chairman of SSCI
    "e-8ffb2d99eb": ("oversaw", "a"),    # Grothman chaired the 26 July 2023 hearing
    "e-60f84097b9": ("oversaw", "a"),    # Luna chaired the 9 September 2025 hearing
    "e-9050616f60": ("held_post", "a"),  # Spergel chaired a NASA team; far end is NASA
}


def main():
    doc = json.load(open(PATH, encoding="utf-8"))
    rows = doc["predicates"]
    for eid, (pred, subj) in DECISIONS.items():
        r = rows[eid]
        if (r["predicate"], r["subject"]) != (pred, subj):
            r.update(predicate=pred, subject=subj, by=BY, confidence="high")
            print(f"{eid}: -> {pred}/{subj}")
    with open(PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
