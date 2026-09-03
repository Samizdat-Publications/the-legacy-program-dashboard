"""Merge per-batch candidate lists and split a cross-check's ABSENT verdicts into triage groups.

Two subcommands, reconstructing what the Area 52 chain did by hand on 2 September 2026:

  python tools/corpus_absent_groups.py merge research/leads/dannyjones-candidates 1 35 \
      research/leads/dannyjones-candidates.txt "Danny Jones corpus: ..."
  python tools/corpus_absent_groups.py split research/leads/dannyjones-crosscheck.json \
      research/leads/dannyjones-candidates.txt research/leads/dannyjones-absent 01-05,06-10

`merge` reads `<prefix>-NN.txt` for NN in the range, keeps the first spelling of each name
(case-insensitive, the same rule as corpus_crosscheck.read_candidates) and writes the merged
list, one clean name per line under a comment header. The batch each name was first seen in
goes to a sidecar, `<merged>.batches.tsv` (name<TAB>batch), so the merged list stays a valid
cross-check input.

`split` reads the cross-check JSON, the sidecar, and a group spec of batch ranges, and writes
`group-G.tsv` per range in the format the triage brief expects:
`name<TAB>batch<TAB>near-miss note` under a one-line comment header.

No em dashes. Self-test: `python tools/corpus_absent_groups.py --self-test`.
"""
import json
import os
import sys
import tempfile


def read_batch_file(path):
    names = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            names.append(line)
    return names


def merge(prefix, lo, hi, out_path, header):
    seen = {}
    order = []
    missing = []
    for n in range(lo, hi + 1):
        p = "%s-%02d.txt" % (prefix, n)
        if not os.path.exists(p):
            missing.append(p)
            continue
        for name in read_batch_file(p):
            key = name.lower()
            if key not in seen:
                seen[key] = (name, "%02d" % n)
                order.append(key)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# %s\n" % header)
        fh.write("# Input to tools/corpus_crosscheck.py. Batches %02d to %02d, deduplicated (%d). Batch per name in %s.batches.tsv\n"
                 % (lo, hi, len(order), os.path.basename(out_path)))
        for key in order:
            fh.write(seen[key][0] + "\n")
    with open(out_path + ".batches.tsv", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# name<TAB>batch first seen in\n")
        for key in order:
            fh.write("%s\t%s\n" % seen[key])
    return len(order), missing


def parse_groups(spec):
    groups = []
    for part in spec.split(","):
        a, b = part.split("-")
        groups.append((int(a), int(b)))
    return groups


def split(json_path, merged_path, out_dir, spec):
    with open(json_path, encoding="utf-8") as fh:
        results = json.load(fh)["results"]
    batches = {}
    with open(merged_path + ".batches.tsv", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            name, batch = line.rstrip("\n").split("\t")
            batches[name.lower()] = batch
    absent = [r for r in results if r["verdict"] == "ABSENT"]
    unplaced = [r["candidate"] for r in absent if r["candidate"].lower() not in batches]
    os.makedirs(out_dir, exist_ok=True)
    counts = []
    for g, (lo, hi) in enumerate(parse_groups(spec), start=1):
        rows = []
        for r in absent:
            b = batches.get(r["candidate"].lower())
            if b is None or not (lo <= int(b) <= hi):
                continue
            near = " ".join("~%s %s.%s" % (h["token"], h["id"], h["field"]) for h in (r.get("near") or []))
            rows.append((r["candidate"], b, near))
        rows.sort(key=lambda t: (t[1], t[0].lower()))
        p = os.path.join(out_dir, "group-%d.tsv" % g)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# ABSENT candidates from batches %02d-%02d: name<TAB>batch<TAB>near-miss note\n" % (lo, hi))
            for row in rows:
                fh.write("%s\t%s\t%s\n" % row)
        counts.append((p, len(rows)))
    return counts, len(absent), unplaced


def self_test():
    """Each branch shown rejecting the input it must reject (CLAUDE.md section 5)."""
    fails = []
    d = tempfile.mkdtemp()
    pre = os.path.join(d, "x-candidates")
    with open(pre + "-01.txt", "w", encoding="utf-8") as fh:
        fh.write("# batch 1\nAlpha\nBeta\n")
    with open(pre + "-02.txt", "w", encoding="utf-8") as fh:
        fh.write("beta\nGamma\n")
    merged = os.path.join(d, "x-candidates.txt")
    n, missing = merge(pre, 1, 3, merged, "test")
    if n != 3:
        fails.append("merge kept %d names, expected 3 (Beta deduplicated case-insensitively)" % n)
    if len(missing) != 1:
        fails.append("merge did not report the missing batch 03")
    names = read_batch_file(merged)
    if names != ["Alpha", "Beta", "Gamma"]:
        fails.append("merge order or spelling wrong: %r" % names)
    side = {}
    with open(merged + ".batches.tsv", encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("#"):
                k, v = line.rstrip("\n").split("\t")
                side[k] = v
    if side.get("Beta") != "01":
        fails.append("Beta first seen in 01, sidecar says %r" % side.get("Beta"))
    js = os.path.join(d, "cc.json")
    with open(js, "w", encoding="utf-8") as fh:
        json.dump({"counts": {}, "results": [
            {"candidate": "Alpha", "verdict": "ABSENT", "near": []},
            {"candidate": "Beta", "verdict": "NODE"},
            {"candidate": "Gamma", "verdict": "ABSENT", "near": [{"token": "gam", "id": "n1", "field": "claim", "context": ""}]},
            {"candidate": "Delta", "verdict": "ABSENT", "near": []},
        ]}, fh)
    out = os.path.join(d, "absent")
    counts, n_abs, unplaced = split(js, merged, out, "01-01,02-03")
    if n_abs != 3:
        fails.append("split counted %d ABSENT, expected 3" % n_abs)
    if unplaced != ["Delta"]:
        fails.append("a name with no batch must be reported unplaced, got %r" % unplaced)
    if [c for _, c in counts] != [1, 1]:
        fails.append("group sizes %r, expected [1, 1] (Beta is NODE and must not appear)" % [c for _, c in counts])
    with open(os.path.join(out, "group-2.tsv"), encoding="utf-8") as fh:
        g2 = fh.read().splitlines()
    if g2[1] != "Gamma\t02\t~gam n1.claim":
        fails.append("near-miss note wrong: %r" % g2[1])
    if fails:
        print("SELF-TEST FAILED")
        for f in fails:
            print("  " + f)
        return 1
    print("self-test ok")
    return 0


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    if a[0] == "--self-test":
        return self_test()
    if a[0] == "merge":
        prefix, lo, hi, out, header = a[1], int(a[2]), int(a[3]), a[4], a[5]
        n, missing = merge(prefix, lo, hi, out, header)
        print("merged %d names -> %s" % (n, out))
        for m in missing:
            print("  missing batch file: %s" % m)
        return 0
    if a[0] == "split":
        js, merged, out_dir, spec = a[1], a[2], a[3], a[4]
        counts, n_abs, unplaced = split(js, merged, out_dir, spec)
        print("%d ABSENT split into %d groups" % (n_abs, len(counts)))
        for p, c in counts:
            print("  %-48s %d" % (p, c))
        for u in unplaced:
            print("  UNPLACED (no batch): %s" % u)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
