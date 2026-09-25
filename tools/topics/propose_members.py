#!/usr/bin/env python3
"""Proposed topic membership, by script (redesign phase 4, task 4).

    python tools/topics/propose_members.py            # writes research/topics/_proposals.json
    python tools/topics/propose_members.py --check    # rebuilds in memory, compares, writes nothing
    python tools/topics/propose_members.py --report   # also prints coverage and per-topic counts

WHAT IT READS
  research/topics/_sections.json and research/topics/<id>.json   the authored stubs
  app/public/data/index.json, edges.json                           the shipped board
  app/public/data/nodes/<id>.json                                  sourceFiles, person domain tags
  app/public/data/threads.json, highlights.json                    the curated structure
  schema/vocab.json                                                which edge types are BACKBONE

It runs after build_app_data.py in tools/build.py, because everything it reads about the
board is what that step writes. Its output is GENERATED: phase 5 turns it into authored
membership, and nobody edits it by hand. `verify.py` regenerates it and compares.

WHAT A PROPOSAL IS
A node proposed for a topic, with every signal that supports it and a score. The score is a
sum of capped signal weights (the table below); a node at or above THRESHOLD is a candidate
member, which is the count Stewart's table shows. A proposal is evidence for a drafter, not
membership: phase 5 decides.

  signal        weight                                               cap
  anchor        the stub names it                                    10
  absorbed      a domain node the stub absorbs                        8
  hop1          a BACKBONE edge to an anchor (0.5 if the anchor is a hub)       2.0
  domainEdge    any edge to an absorbed domain node (its edges are membership)  1.5
  hop1Other     a non-backbone edge to an anchor (0.25 from a hub)              1.0
  hop2          two BACKBONE steps to an anchor through a non-hub, non-domain
                intermediate, 0.25 per anchor reached                          0.75
  community     0.75 x (share of the topic's anchors in the node's community)
                x min(1, 50 / community size): a big community is weak evidence
                for any one topic inside it
  tags          a person's `domains` tag naming an absorbed domain node,
                0.6 x min(1, 15 / people carrying that tag)                     0.9
  file          0.75 x the best research file the node shares with the anchors:
                (share of anchors in that file) x min(1, 30 / nodes in the file)
  thread        the node is a step of a thread holding 2+ of the anchors        0.4
  highlight     the node is a start-here flag, and some other signal holds      0.25

A hub is a node with HUB or more distinct neighbours; only a CONNECTOR hub (fewer than
PROVINCIAL of its neighbours in its own community) is damped as an anchor, because a
provincial hub's neighbours are its topic (Appendix B, section 2). A domain node (class
`domain`) is a candidate only for the topic that absorbs it: domain nodes are editorial,
not entities.

A candidate also needs one LINKED signal (anchor, absorbed, hop1, hop1Other, hop2,
domainEdge, tags or thread). Community and research file are correlated, since one
research pass tends to write one community, so the two together never make a member on
their own; below the threshold, or without a link, a proposal scoring NEAR or more is
listed under `near`.

COVERAGE is reported in the file: the share of nodes and of people that are a candidate
of at least one topic, against the targets (90% and 95%), the degree-30 hubs with the
number of topics each is proposed for, and every uncovered node grouped by community.

COMMUNITIES are recomputed here, the same way tools/analysis/structure/ computes them
(the hub-damped weighting, 30 Louvain seeds, consensus at co-association 0.5), with
`louvain` and `weights` imported from that code rather than copied. Everything is seeded,
so two runs on one board give the same file byte for byte (`verify.py --idempotent`).
The communities are named C0, C1 ... by size, and the file lists their members.
"""
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOPICS_DIR = os.path.join(ROOT, "research", "topics")
OUT = os.path.join(TOPICS_DIR, "_proposals.json")
APPDATA = os.path.join(ROOT, "app", "public", "data")

sys.path.insert(0, os.path.join(ROOT, "tools", "analysis", "structure"))
from g import louvain, weights  # noqa: E402

THRESHOLD = 1.0
NEAR = 0.6            # proposals between NEAR and THRESHOLD are listed as near misses
HUB = 30
PROVINCIAL = 0.5      # a hub with at least this share of neighbours in its own community
SEEDS = 30
TAU = 0.5

W = {"anchor": 10.0, "absorbed": 8.0, "hop1": 1.0, "hop1_hub": 0.5, "hop1_cap": 2.0,
     "domainEdge": 1.0, "domainEdge_cap": 1.5, "hop1Other": 0.5, "hop1Other_hub": 0.25,
     "hop1Other_cap": 1.0, "hop2": 0.25, "hop2_cap": 0.75, "community": 0.75,
     "community_size": 50.0, "tags": 0.6, "tags_ref": 15.0, "tags_cap": 0.9,
     "file": 0.75, "file_ref": 30.0, "thread": 0.4, "highlight": 0.25}

TARGETS = {"nodes": 0.90, "people": 0.95}

# A candidate needs at least one of these: something that ties it to the topic itself.
# Community and research file alone do not make a member. They are correlated (a
# research pass tends to write one community), so two of them together are one piece
# of evidence counted twice; they strengthen a link, they never replace one.
LINKED = {"anchor", "absorbed", "hop1", "hop1Other", "hop2", "domainEdge", "tags", "threads"}


def rd(*p):
    with open(os.path.join(*p), encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- inputs

def load_topics():
    sections = rd(TOPICS_DIR, "_sections.json")
    topics = []
    for f in sorted(os.listdir(TOPICS_DIR)):
        if f.endswith(".json") and not f.startswith("_"):
            topics.append(rd(TOPICS_DIR, f))
    return sections, topics


class Board:
    def __init__(self):
        idx = rd(APPDATA, "index.json")
        self.nodes = {n["id"]: n for n in idx["nodes"]}
        self.ids = sorted(self.nodes)
        self.edges = rd(APPDATA, "edges.json")
        vocab = rd(ROOT, "schema", "vocab.json")
        self.backbone = {t["id"] for t in vocab["edgeTypes"] if t.get("layer") == "backbone"}
        self.adj = defaultdict(set)
        self.bb = defaultdict(set)            # backbone adjacency
        for e in self.edges:
            a, b = e["a"], e["b"]
            if a == b:
                continue
            self.adj[a].add(b)
            self.adj[b].add(a)
            if e["t"] in self.backbone:
                self.bb[a].add(b)
                self.bb[b].add(a)
        for i in self.ids:
            self.adj.setdefault(i, set())
        self.deg = {i: len(self.adj[i]) for i in self.ids}
        self.files = {}
        self.tags = {}
        for i in self.ids:
            n = rd(APPDATA, "nodes", i + ".json")
            self.files[i] = sorted(n.get("sourceFiles") or [])
            self.tags[i] = sorted(n.get("domains") or []) if n.get("cls") == "person" else []
        th = rd(APPDATA, "threads.json")
        self.threads = {t["id"]: sorted({s["node"] for s in t["steps"]}) for t in th["threads"]}
        hl = rd(APPDATA, "highlights.json")
        self.flags = {f["id"]: f["rank"] for f in hl["flags"]}

    def is_domain(self, i):
        return self.nodes[i]["cls"] == "domain"

    def year(self, i):
        s = self.nodes[i].get("dateStart")
        try:
            y = int(str(s)[:4])
        except (TypeError, ValueError):
            return None
        return y if 1000 < y < 2200 else None


# ---------------------------------------------------------------- communities

def _canonical(part):
    first = {}
    for k in sorted(part):
        first.setdefault(part[k], k)
    return tuple(first[part[k]] for k in sorted(part))


def _coassoc(runs):
    D = Counter()
    for p in runs:
        groups = defaultdict(list)
        for k, v in p.items():
            groups[v].append(k)
        for mem in groups.values():
            mem.sort()
            for x in range(len(mem)):
                for y in range(x + 1, len(mem)):
                    D[(mem[x], mem[y])] += 1
    return {k: v / len(runs) for k, v in D.items()}


def communities(B):
    """Hub-damped consensus communities, as in tools/analysis/structure/s2 and s3,
    except that consensus is declared when all re-runs give the identical partition
    (s3 uses NMI > 0.999, which needs math.log; exact agreement needs nothing)."""
    Wt = weights(B, "hubdamp")
    runs = [louvain(B.ids, Wt, seed=s)[0] for s in range(SEEDS)]
    part = runs[0]
    for _ in range(10):
        Wc = {k: v for k, v in _coassoc(runs).items() if v >= TAU}
        new = [louvain(B.ids, Wc, seed=1000 + s)[0] for s in range(SEEDS)]
        part = new[0]
        runs = new
        canon = [_canonical(p) for p in new]
        if all(c == canon[0] for c in canon):
            break
    groups = defaultdict(list)
    for k, v in part.items():
        groups[v].append(k)
    order = sorted(groups.values(), key=lambda m: (-len(m), min(m)))
    return {f"C{i}": sorted(m) for i, m in enumerate(order)}


# ---------------------------------------------------------------- scoring

def _cap(x, c):
    return x if x < c else c


def propose(B, topic, comm_of, comm_size, tag_count, file_size):
    anchors = list(topic.get("anchors") or [])
    absorbed = list(topic.get("absorbs") or [])
    seeds = anchors + [d for d in absorbed if d not in anchors]
    missing = [i for i in seeds if i not in B.nodes]
    if missing:
        raise SystemExit(f"propose_members: topic {topic['id']} names ids not on the board: "
                         f"{missing}")
    aset, dset = set(anchors), set(absorbed)
    # A CONNECTOR hub is damped; a PROVINCIAL hub is not (Appendix B, section 2): when
    # most of a hub's neighbours sit in its own community, they are its topic, and a
    # seat on the waived-SAP notification group is a member of the reporting topic.
    hub = {a for a in anchors if B.deg[a] >= HUB
           and sum(1 for n in B.adj[a] if comm_of[n] == comm_of[a]) < PROVINCIAL * B.deg[a]}

    # topic profiles
    comm_share = Counter(comm_of[s] for s in seeds)
    n_seeds = len(seeds) or 1
    file_share = Counter(f for s in seeds for f in B.files[s])
    threads = sorted(t for t, mem in B.threads.items() if len(aset & set(mem)) >= 2)
    tagged = set(dset)

    sig = defaultdict(dict)
    for a in anchors:
        sig[a]["anchor"] = True
    for d in absorbed:
        sig[d]["absorbed"] = True
    for a in anchors:
        for n in sorted(B.adj[a]):
            if B.is_domain(n) and n not in dset:
                continue
            key = "hop1" if n in B.bb[a] else "hop1Other"
            sig[n].setdefault(key, []).append(a)
        for m in sorted(B.bb[a]):
            if B.deg[m] >= HUB or B.is_domain(m):
                continue
            for n in sorted(B.bb[m]):
                if n == a or (B.is_domain(n) and n not in dset):
                    continue
                lst = sig[n].setdefault("hop2", [])
                if a not in lst:
                    lst.append(a)
    for d in absorbed:
        for n in sorted(B.adj[d]):
            if B.is_domain(n) and n not in dset:
                continue
            sig[n].setdefault("domainEdge", []).append(d)
    for t in threads:
        for n in B.threads[t]:
            sig[n].setdefault("threads", []).append(t)
    # tag and community and file signals only strengthen nodes the topic already reaches
    # OR sit in its communities; walk every node once, cheaply
    seed_comms = set(comm_share)
    for n in B.ids:
        if B.is_domain(n) and n not in dset:
            continue
        tg = [d for d in B.tags[n] if d in tagged]
        if tg:
            sig[n]["tags"] = tg
        if comm_of[n] in seed_comms:
            sig[n]["community"] = comm_of[n]
        best, bestf = 0.0, None
        for f in B.files[n]:
            v = (file_share[f] / n_seeds) * min(1.0, W["file_ref"] / file_size[f])
            if v > best + 1e-12:
                best, bestf = v, f
        if bestf is not None and best > 0:
            sig[n]["file"] = bestf

    out = []
    for n, s in sig.items():
        if not s:
            continue
        score = 0.0
        if s.get("anchor"):
            score += W["anchor"]
        if s.get("absorbed"):
            score += W["absorbed"]
        if "hop1" in s:
            score += _cap(sum(W["hop1_hub"] if a in hub else W["hop1"] for a in s["hop1"]),
                          W["hop1_cap"])
        if "hop1Other" in s:
            score += _cap(sum(W["hop1Other_hub"] if a in hub else W["hop1Other"]
                              for a in s["hop1Other"]), W["hop1Other_cap"])
        if "hop2" in s:
            score += _cap(W["hop2"] * len(s["hop2"]), W["hop2_cap"])
        if "domainEdge" in s:
            score += _cap(W["domainEdge"] * len(s["domainEdge"]), W["domainEdge_cap"])
        if "community" in s:
            c = s["community"]
            score += W["community"] * (comm_share[c] / n_seeds) * min(
                1.0, W["community_size"] / comm_size[c])
        if "tags" in s:
            score += _cap(sum(W["tags"] * min(1.0, W["tags_ref"] / tag_count[d])
                              for d in s["tags"]), W["tags_cap"])
        if "file" in s:
            f = s["file"]
            score += W["file"] * (file_share[f] / n_seeds) * min(1.0, W["file_ref"] / file_size[f])
        if "threads" in s:
            score += W["thread"]
        other = score
        if n in B.flags and other > 0:
            s["highlight"] = B.flags[n]
            score += W["highlight"]
        score = round(score, 3)
        if score >= NEAR:
            out.append((n, score, s))
    out.sort(key=lambda r: (-r[1], r[0]))
    members = [r for r in out if r[1] >= THRESHOLD and LINKED & set(r[2])]
    near = [r for r in out if not (r[1] >= THRESHOLD and LINKED & set(r[2]))]
    years = sorted(y for y in (B.year(r[0]) for r in members) if y is not None)

    def pct(p):
        if not years:
            return None
        return years[min(len(years) - 1, int(p * (len(years) - 1) + 0.5))]

    return {
        "candidates": len(members),
        "communities": {c: comm_share[c] for c in sorted(comm_share)},
        "threads": threads,
        "memberYears": {"dated": len(years), "p10": pct(0.1), "p50": pct(0.5), "p90": pct(0.9)},
        "members": [[n, sc, s] for n, sc, s in members],
        "near": [[n, sc, s] for n, sc, s in near],
    }


def build():
    B = Board()
    sections, topics = load_topics()
    comms = communities(B)
    comm_of = {i: c for c, mem in comms.items() for i in mem}
    comm_size = {c: len(m) for c, m in comms.items()}
    tag_count = Counter(t for i in B.ids for t in B.tags[i])
    file_size = Counter(f for i in B.ids for f in B.files[i])

    per = {}
    for t in sorted(topics, key=lambda t: t["id"]):
        per[t["id"]] = propose(B, t, comm_of, comm_size, tag_count, file_size)

    in_topics = defaultdict(list)
    for tid, p in per.items():
        for n, _sc, _s in p["members"]:
            in_topics[n].append(tid)
    people = [i for i in B.ids if B.nodes[i]["cls"] == "person"]
    covered = [i for i in B.ids if in_topics.get(i)]
    uncovered = [i for i in B.ids if not in_topics.get(i)]
    groups = defaultdict(list)
    for i in uncovered:
        groups[comm_of[i]].append(i)

    def comm_name(c):
        top = sorted(comms[c], key=lambda i: (-B.deg[i], i))[:3]
        return ", ".join(top)

    hubs = sorted((i for i in B.ids if B.deg[i] >= HUB), key=lambda i: (-B.deg[i], i))
    coverage = {
        "threshold": THRESHOLD,
        "targets": TARGETS,
        "nodes": {"covered": len(covered), "total": len(B.ids),
                  "share": round(len(covered) / len(B.ids), 4)},
        "people": {"covered": sum(1 for i in people if in_topics.get(i)), "total": len(people),
                   "share": round(sum(1 for i in people if in_topics.get(i)) / len(people), 4)},
        "hubs": [{"id": h, "degree": B.deg[h], "topics": len(in_topics.get(h, []))} for h in hubs],
        "uncoveredGroups": [
            {"community": c, "around": comm_name(c), "uncovered": len(m),
             "people": sum(1 for i in m if B.nodes[i]["cls"] == "person"),
             "ids": sorted(m)}
            for c, m in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))],
    }
    return {
        "_what": ("GENERATED by tools/topics/propose_members.py from the topic stubs and the "
                  "shipped board. Do not edit by hand: verify.py regenerates it and compares. "
                  "A proposal is evidence for the phase 5 drafters, not membership."),
        "method": {"threshold": THRESHOLD, "near": NEAR, "hub": HUB, "weights": W,
                   "communities": {"weighting": "hubdamp", "seeds": SEEDS, "consensus": TAU},
                   "backbone": sorted(B.backbone)},
        "coverage": coverage,
        "communities": comms,
        "topics": per,
    }


def dumps(doc):
    """Stable, diffable, compact: one member per line."""
    lines = ["{"]
    keys = list(doc)
    for k_i, k in enumerate(keys):
        comma = "," if k_i < len(keys) - 1 else ""
        v = doc[k]
        if k == "topics":
            lines.append(f' "topics": {{')
            tids = list(v)
            for t_i, tid in enumerate(tids):
                p = v[tid]
                lines.append(f'  {json.dumps(tid)}: {{')
                pk = list(p)
                for p_i, kk in enumerate(pk):
                    c2 = "," if p_i < len(pk) - 1 else ""
                    if kk in ("members", "near"):
                        if not p[kk]:
                            lines.append(f'   {json.dumps(kk)}: []{c2}')
                            continue
                        lines.append(f'   {json.dumps(kk)}: [')
                        for m_i, m in enumerate(p[kk]):
                            c3 = "," if m_i < len(p[kk]) - 1 else ""
                            lines.append("    " + json.dumps(m, ensure_ascii=False, sort_keys=True,
                                                             separators=(",", ":")) + c3)
                        lines.append(f'   ]{c2}')
                    else:
                        lines.append(f'   {json.dumps(kk)}: '
                                     + json.dumps(p[kk], ensure_ascii=False, sort_keys=True,
                                                  separators=(",", ":")) + c2)
                lines.append("  }" + ("," if t_i < len(tids) - 1 else ""))
            lines.append(" }" + comma)
        elif k in ("communities",):
            lines.append(f' "communities": {{')
            cs = list(v)
            for c_i, c in enumerate(cs):
                lines.append(f'  {json.dumps(c)}: ' + json.dumps(v[c], separators=(",", ":"))
                             + ("," if c_i < len(cs) - 1 else ""))
            lines.append(" }" + comma)
        else:
            lines.append(f' {json.dumps(k)}: '
                         + json.dumps(v, ensure_ascii=False, sort_keys=True, indent=None,
                                      separators=(",", ":")) + comma)
    lines.append("}")
    return "\n".join(lines) + "\n"


def report(doc):
    cov = doc["coverage"]
    print(f"nodes  {cov['nodes']['covered']}/{cov['nodes']['total']} "
          f"= {cov['nodes']['share']:.1%} (target {cov['targets']['nodes']:.0%})")
    print(f"people {cov['people']['covered']}/{cov['people']['total']} "
          f"= {cov['people']['share']:.1%} (target {cov['targets']['people']:.0%})")
    thin = [h for h in cov["hubs"] if h["topics"] < 3]
    print(f"hubs (degree {HUB}+) in fewer than 3 topics: "
          + (", ".join(f"{h['id']}({h['topics']})" for h in thin) or "none"))
    for g in cov["uncoveredGroups"][:10]:
        print(f"  uncovered {g['uncovered']:3d} ({g['people']} people) in {g['community']} "
              f"around {g['around']}")
    for tid, p in doc["topics"].items():
        print(f"  {tid:32s} {p['candidates']:4d}  years {p['memberYears']}")


def main(argv):
    doc = build()
    text = dumps(doc)
    if "--check" in argv:
        try:
            with open(OUT, encoding="utf-8") as fh:
                have = fh.read().replace("\r\n", "\n")
        except OSError:
            have = None
        if have != text:
            print("propose_members --check: research/topics/_proposals.json is not what the "
                  "script produces; run python tools/topics/propose_members.py")
            return 1
        print("propose_members --check: _proposals.json reproduces")
        return 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"wrote research/topics/_proposals.json: {len(doc['topics'])} topics, "
          f"{len(text.encode('utf-8'))} bytes; nodes covered "
          f"{doc['coverage']['nodes']['share']:.1%}, people {doc['coverage']['people']['share']:.1%}")
    if "--report" in argv:
        report(doc)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
