#!/usr/bin/env python3
"""review_sample.py: pick the edges the phase 7 reviewers re-derive, and split them.

Every edge a classifier marked `low`, plus a seeded 10% random sample of the rest,
split into N reviewer packet files. The packets are the classifiers' own inputs
and nothing else: a reviewer never sees the classifier's answer or reason.

  python tools/predicates/review_sample.py --classified DIR --out DIR [--n 2] [--seed 26]
"""
import glob, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edge_packets  # noqa: E402


def main():
    a = sys.argv[1:]
    get = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    n, seed = int(get("--n", 2)), int(get("--seed", 26))
    answers = []
    for f in sorted(glob.glob(os.path.join(get("--classified"), "*.json"))):
        answers.extend(json.load(open(f, encoding="utf-8")))
    low = sorted(r["id"] for r in answers if r["confidence"] == "low")
    rest = sorted(r["id"] for r in answers if r["confidence"] != "low")
    rnd = random.Random(seed)
    sample = sorted(rnd.sample(rest, round(len(rest) * 0.10)))
    pick = set(low) | set(sample)
    packets = [p for p in edge_packets.packets() if p["id"] in pick]
    rnd.shuffle(packets)
    out = get("--out")
    os.makedirs(out, exist_ok=True)
    for i in range(n):
        part = sorted(packets[i::n], key=lambda p: p["id"])
        with open(os.path.join(out, f"review-{i + 1}.json"), "w", encoding="utf-8") as fh:
            json.dump(part, fh, indent=1, ensure_ascii=False)
        print(f"review-{i + 1}.json  {len(part)} edges")
    with open(os.path.join(out, "selection.json"), "w", encoding="utf-8") as fh:
        json.dump({"low": low, "sample": sample, "seed": seed}, fh, indent=1)
    print(f"low {len(low)} + sample {len(sample)} of {len(rest)} = {len(pick)}")


if __name__ == "__main__":
    main()
