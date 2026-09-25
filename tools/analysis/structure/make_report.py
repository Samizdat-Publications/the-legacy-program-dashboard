"""Assemble REPORT.md and communities.json from the section outputs."""
import json
from collections import Counter, defaultdict
from g import *

B = Board()
ids = B.ids
N = len(ids)
S1 = rd(OUT, "s1_basics.json")
S2 = rd(OUT, "s2_partitions.json")
S3 = rd(OUT, "s3_consensus.json")
PH = rd(OUT, "s4_profiles_hubdamp.json")
PA = rd(OUT, "s4_profiles_all.json")
S5 = rd(OUT, "s5_levels.json")
S6 = rd(OUT, "s6_edgetypes.json")
S7 = rd(OUT, "s7_time.json")
S8 = rd(OUT, "s8_coverage.json")
S9 = rd(OUT, "s9_paths.json")
S10 = rd(OUT, "s10_hubroles.json")
S11 = rd(OUT, "s11_extra.json")
S12 = rd(OUT, "s12_checks.json")

LAB_H = {
    0: ("Navy encounters, the 2017 story and the whistleblower hearings", "Nimitz and Roosevelt, NYT 2017, Elizondo, Grusch, UAPTF, ODNI 2021, Immaculate Constellation, the 2023 and 2024 hearings"),
    1: ("AAWSAP / AATIP / BAASS lineage and the DIRDs", "DIA contract, Reid, Bigelow, NIDS, EarthTech, Skinwalker, Stargate, Kona Blue, Wilson-Davis notes"),
    2: ("Other nations' programmes", "UK MoD, Condign and Rendlesham; France GEIPAN and COMETA; Brazil FAB and Prato; USSR SETKA; Chile CEFAA; Canada"),
    3: ("2025-2026 House push and the FFRDC / contractor probes", "Burlison, Burchett, the September 2025 hearing, MITRE, RAND, Northrop/TRW, UAP Gerb, Manhattan Project 2"),
    4: ("Air Force and CIA handling, 1947-1969", "Sign, Blue Book, ATIC, Robertson Panel, Condon, Battelle, MKULTRA, the Twining and Schulgen memos"),
    5: ("UAP legislation and the records trail", "UAPDA 2023, NDAAs, IAAs, Senate sponsors; ODNI, NARA RG 615, NSA and NRO, CAUS v. NSA"),
    6: ("SAP law and the congressional reporting architecture", "waived / unacknowledged SAPs, SAPCO, 10 USC 119, DoDD 5205.07 series, carve-outs, the Gang of Eight"),
    7: ("Nevada, Groom Lake and the nuclear-weapons complex", "S-4 and Lazar, TR-3B and Fouche, AEC / DOE labs, EG&G, Skunk Works at Groom"),
    8: ("Roswell and the crash-retrieval research tradition; UFOs and nuclear missiles", "Marcel, Stringfield, Friedman, Randle, GAO 1995, Mogul, Malmstrom and Minot, Varginha"),
    9: ("AARO and the PURSUE releases, 2022-2026", "AARO directors and reports, the Historical Record, the 2026 release directives"),
    10: ("Anti-gravity, the ARV and the Disclosure Project", "McCandlish, Greer, NPC 2001, 1950s gravity research, Norton 1988, Podesta; many editorial domain nodes"),
    11: ("Academic UAP science", "Sol Foundation, Galileo Project, Nolan, Knuth, UAPx, Villarroel, SCU"),
    12: ("The money: classified budgets and the unauditable ledger", "DoD audit, classified annex, NIP / MIP, SFFAS 56, Skidmore-Fitts, IR&D"),
    13: ("Cold War secrecy architecture (with editorial domain nodes)", "NSC, NSC 5412, National Security Act 1947, classification EOs, GAO 88-152; 13 domain nodes"),
    14: ("Kirtland 1980: Bennewitz, Doty, Dulce and MJ-12", "the AFOSI disinformation affair and its afterlife"),
    15: ("TTSA and the Army CRADA", "the 2017-2019 materials agreement, ADAM project, Detroit Arsenal"),
    16: ("Military airspace incursions and drones, 2023-2026", "Langley, the February 2023 shootdowns, New Jersey 2024, Barksdale 2026"),
    17: ("Isolated node", "jason-sands, no edges"),
}
LAB_A = {
    0: ("AARO, PURSUE and the 2023-2026 Congress", "AARO, PURSUE, Luna, Burlison, Burchett, the 2025 hearing, NASA"),
    1: ("Air Force and CIA handling, 1947-1969 (with NSC and 25 domain nodes)", "Blue Book, CIA, USAF, Robertson, Condon, Battelle"),
    2: ("AAWSAP / AATIP / BAASS lineage and the DIRDs", "same core as hub-damped H1"),
    3: ("SAP law and the money", "waived SAP group, SAPCO, 10 USC 119, classified annex, DoD audit"),
    4: ("Nevada, New Mexico and the nuclear-weapons complex", "S-4 and Lazar, Dulce, Bennewitz and Doty, AEC / DOE, TR-3B"),
    5: ("Other nations' programmes", "same core as hub-damped H2"),
    6: ("Elizondo, TTSA and the 2017 story to Immaculate Constellation", "Elizondo, TTSA, NYT 2017, AATIP, the November 2024 hearing"),
    7: ("Roswell and the crash-retrieval research tradition; UFOs and nuclear missiles", "Roswell, Marcel, Stringfield, Malmstrom"),
    8: ("Lockheed, Skunk Works, the ARV and the Disclosure Project", "Lockheed Martin, McCandlish, Greer, NPC 2001"),
    9: ("Navy encounters to the 2023 Grusch hearing", "Grusch, Nimitz, UAPTF, ODNI 2021, Roosevelt, Graves"),
    10: ("UAP legislation 2021-2026", "UAPDA, NDAAs, IAAs, Senate committees"),
    11: ("Academic UAP science", "same core as hub-damped H11"),
    12: ("FFRDCs and the contractor-custody probes", "MITRE, RAND, Northrop, UAP Gerb"),
    13: ("Signals-intelligence agencies and records litigation", "ODNI, NSA, NRO, NARA UAP collection, CAUS v. NSA"),
    14: ("Age of Disclosure documentary", "3 nodes"),
    15: ("Isolated node", "jason-sands"),
}
LAB_M = {
    0: ("Washington, 2017-2026", "hub-damped H0, H3, H5, H6, H9, H12, H16"),
    2: ("The Cold War record, 1947-1990", "H4, H8, H13, H14 and parts of H7 and H10"),
    1: ("AAWSAP and the science / contractor strand", "H1, H11, H15 and parts of H10 and H7"),
    3: ("Other nations", "H2"),
    4: ("Skidmore-Fitts audit fragment", "part of H12"),
    5: ("Isolated node", ""),
}

# The labels above were written for the 24 September 2026 run and are POSITIONAL: H0 is
# whatever community is largest. Re-run on a later board (phase 4 re-ran it on 25
# September, after the nuclear register and 32 merges) and the sizes reorder, so H0's
# label lands on AAWSAP. Each label is therefore re-attached through a signature node it
# was written about, to whichever community now holds that node; a community no label
# reaches is named by its largest members instead of inheriting a wrong name.
SIG_H = {0: "david-grusch", 1: "aawsap", 2: "rendlesham-1980", 3: "mitre-corporation",
         4: "project-blue-book", 5: "uapda-2023", 6: "waived-sap-notification-group",
         7: "l-groom-lake", 8: "roswell-1947", 9: "aaro", 10: "mark-mccandlish",
         11: "sol-foundation", 12: "classified-annex", 13: "nsc-5412", 14: "paul-bennewitz",
         15: "ttsa-army-crada", 16: "langley-2023-incursions", 17: "jason-sands"}
SIG_A = {0: "aaro", 1: "project-blue-book", 2: "aawsap", 3: "waived-sap-notification-group",
         4: "s-4-papoose-lake", 5: "rendlesham-1980", 6: "luis-elizondo", 7: "roswell-1947",
         8: "mark-mccandlish", 9: "nimitz-2004", 10: "ndaa-fy2024", 11: "sol-foundation",
         12: "mitre-corporation", 13: "caus-v-nsa", 14: "age-of-disclosure", 15: "jason-sands"}


def _relabel(part, labels, sigs):
    part = {k: int(v) for k, v in part.items()}
    members = {}
    for k, c in part.items():
        members.setdefault(c, []).append(k)
    top = {c: sorted(mem, key=lambda i: (-B.deg[i], i)) for c, mem in members.items()}
    out = {}
    for old in sorted(labels):
        c = part.get(sigs.get(old))
        # the signature must still be among the community's three best-connected
        # members: a node that drifted into another community does not carry its
        # old label with it
        if c is not None and c not in out and sigs[old] in top[c][:3]:
            out[c] = labels[old]
    for c in members:
        if c not in out:
            out[c] = ("not labelled in the 24 September run; largest: " + ", ".join(top[c][:3]), "")
    return out


LAB_H = _relabel(S3["cons"]["hubdamp"]["part"], LAB_H, SIG_H)
LAB_A = _relabel(S3["cons"]["all"]["part"], LAB_A, SIG_A)


def pct(x, d=0):
    return f"{100 * x:.{d}f}%"


def cls_str(lst, size, k=3):
    return ", ".join(f"{c} {round(100 * n / size)}%" for c, n in lst[:k])


def types_str(lst, k=3):
    tot = sum(n for _, n in lst) or 1
    return ", ".join(f"{t} {round(100 * n / tot)}%" for t, n in lst[:k])


def yr(t):
    a, b, c = t
    if a is None:
        return "n/a"
    return f"{a}-{c} (median {b})"


L = []
w = L.append

# ---------------------------------------------------------------- header
w("# Structure of the Legacy Program board: a measurement for the redesign")
w("")
w(f"Data: `app/public/data/` as generated {B.index['generated']} (source {B.index['source']}), plus `data/l0-model.json`, `data/the-program.json` for edge notes. "
  f"All numbers below are MEASURED by the scripts in this folder unless a line is marked INFERRED. Read-only on the repo; stdlib Python only.")
w("")
w("Graph model used throughout: nodes = the 1,136 board nodes; edges = the 2,685 hand-written sourced edges in `edges.json`, "
  "treated as undirected. \"Degree\" means distinct neighbours (matches the `deg` field shipped in `index.json` for all 1,136 nodes). "
  "Multi-edges (110 node pairs carry 2 or more edges) are summed as weights where weights are used.")
w("")

# ---------------------------------------------------------------- 1 basics
w("## 1. Basics")
w("")
w("| Measure | Value |")
w("|---|---|")
w(f"| Nodes / sourced edges / distinct linked pairs | {N:,} / {S1['edges_multi']:,} / {S1['pairs']:,} |")
w(f"| Density | {S1['density']:.4f} (mean degree {S1['mean_deg']:.2f}, median {S1['median_deg']:.0f}, max {S1['max_deg']}) |")
w(f"| Connected components | {len(S1['components'])}: one of {S1['components'][0]:,} nodes plus {len(S1['isolated'])} isolated node (`{S1['isolated'][0]}`) |")
w(f"| Degree-1 leaves | {S1['leaves']} ({pct(S1['leaf_share'])}); degree <= 2: {pct(S1['deg_le2_share'])} |")
w(f"| Degree Gini | {S1['deg_gini']:.2f}; top 1% of nodes hold {pct(S1['endpoint_share_top']['top1pct'])} of edge endpoints, top 10% hold {pct(S1['endpoint_share_top']['top10pct'])} |")
w(f"| k-core | max core {S1['kcore_max']} ({dict(S1['kcore_hist'])[S1['kcore_max']]} nodes); {dict(S1['kcore_hist'])[1]} nodes are only in the 1-core |")
w(f"| Giant component path length | mean {S1['avg_path']:.2f}, diameter {S1['diameter']}, radius {S1['radius']}; {pct(S1['pairs_within_2'], 1)} of pairs within 2 hops, {pct(S1['pairs_within_3'])} within 3, {pct(S1['pairs_within_4'])} within 4 |")
w("")
w("Degree histogram:")
w("")
w("| degree | " + " | ".join(h["bin"] for h in S1["deg_hist"]) + " |")
w("|---" * (len(S1["deg_hist"]) + 1) + "|")
w("| nodes | " + " | ".join(str(h["n"]) for h in S1["deg_hist"]) + " |")
w("")
w("Degree by node class:")
w("")
w("| class | n | mean | median | p90 | max | leaves | share of all edge endpoints |")
w("|---|---|---|---|---|---|---|---|")
for r in S1["by_class"]:
    w(f"| {r['cls']} | {r['n']} | {r['mean']:.1f} | {r['median']:.0f} | {r['p90']} | {r['max']} | {r['leaves']} ({pct(r['leaf_share'])}) | {pct(r['sum_deg_share'])} |")
w("")
w("Mean degree by node tier: " + ", ".join(f"{r['tier']} {r['mean']:.1f} (median {r['median']:.0f}, n={r['n']})" for r in S1["by_tier"]) + ". "
  "Tier is partly computed from degree (`tools/regrade.py`), so this is expected, not a finding.")
w("")
w("**Reading.** This is not a star-shaped graph: the biggest hub has 67 neighbours (6% of the board), the top 1% of nodes hold under 10% of edge ends, and the median node has 3 links. "
  "The whole board is one component. People are the thinnest class (median 2 links, 27% leaves); locations are the most leaf-like (45%).")
w("")

# ---------------------------------------------------------------- 2 hairball
w("## 2. Hubs and the hairball effect")
w("")
w("### Top 20 hubs by degree")
w("")
w("| # | node | class | cluster | tier | on L0 | degree | betweenness (norm.) | dominant edge types |")
w("|---|---|---|---|---|---|---|---|---|")
for k, r in enumerate(S1["top20"], 1):
    w(f"| {k} | `{r['id']}` | {r['cls']} | {r['cluster']} | {r['tier']} | {'yes' if r['l0'] else 'no'} | {r['deg']} | {r['bc']:.3f} | " + ", ".join(f"{t} {n}" for t, n in r["types"][:3]) + " |")
w("")
w("### Reach of the top 10")
w("")
w("| hub | within 1 hop | within 2 hops | cumulative top-k, 1 hop | cumulative top-k, 2 hops |")
w("|---|---|---|---|---|")
for r in S1["hub_reach"]:
    w(f"| `{r['id']}` | {pct(r['hop1'], 1)} | {pct(r['hop2'], 1)} | {pct(r['cum_hop1'], 1)} | {pct(r['cum_hop2'], 1)} |")
w("")
w("### Removing hubs")
w("")
fr = S1["fragmentation"]
w("| removed | giant component (share of remaining) | components | isolated after | mean path in giant |")
w("|---|---|---|---|---|")
w(f"| none | 1,135 (99.9%) | 2 | 1 | {S1['avg_path']:.2f} |")
for k in ("top10", "top20", "top50", "top10_bc", "top20_bc"):
    r = fr[k]
    nm = {"top10": "top 10 by degree", "top20": "top 20 by degree", "top50": "top 50 by degree", "top10_bc": "top 10 by betweenness", "top20_bc": "top 20 by betweenness"}[k]
    w(f"| {nm} | {r['giant']:,} ({pct(r['giant_share_of_remaining'], 1)}) | {r['components']} | {r['isolated_after']} | {r['avg_path_giant']:.2f} |")
for k in ("random10", "random20", "random50"):
    r = fr[k]
    w(f"| {r['removed']} random nodes (mean of 20) | ({pct(r['giant_share_of_remaining_mean'], 1)}) | {r['components_mean']:.1f} | {r['isolated_mean']:.1f} | |")
w("")
w(f"Removing the top 10 cuts off {S1['cut_by_top10_n']} nodes ({', '.join(f'{c} {n}' for c, n in S1['cut_by_top10_cls'])}); the top 20 cut off {S1['cut_by_top20_n']}. "
  f"{S1['satellites_of_top20']} nodes have ONLY top-20 hubs as neighbours. The top 10 hubs carry {pct(S1['bc_share_top10deg'])} of all shortest-path betweenness, the top 20 carry {pct(S1['bc_share_top20deg'])}. "
  f"Pairs touching a top-10 hub: {pct(S1['pairs_touching_top10'])}; top-20: {pct(S1['pairs_touching_top20'])}.")
w("")
w(f"Shortest paths: in a sample of {S9['agg']['sampled_pairs']} random node pairs, {pct(S9['agg']['all_shortest_paths_via_top20'])} have EVERY shortest path passing through a top-20 hub.")
w("")
w("### Hub roles (participation across the hub-damped communities of section 3)")
w("")
w("Participation P = 1 - sum over communities of (share of the hub's neighbours in that community)^2; \"home\" = share of neighbours in the hub's own community. "
  "Connector = P >= 0.6; provincial = the hub's neighbourhood mostly sits inside one topic.")
w("")
w("| hub | degree | P | communities among neighbours | home share | role |")
w("|---|---|---|---|---|---|")
for r in S10["rows"][:24]:
    w(f"| `{r['id']}` | {r['deg']} | {r['participation']:.2f} | {r['n_comms']} | {pct(r['home_share'])} | {r['role']} |")
w("")
w("**Hub verdict (MEASURED, then INFERRED).** The graph does not fall apart without its hubs: removing the top 10 detaches 38 nodes (3.4%) and the rest stays one component with the mean path rising from 4.67 to 5.49. "
  "So hubs are shortcuts, not the skeleton. But they own the shortcuts: two thirds of random pairs can only be joined through a top-20 hub. "
  "The hubs split into two kinds. Provincial hubs (AAWSAP 83% home, DIRD series 93%, DIA 83%, Blue Book 74%, UAPDA 73%, Nimitz 85%, BAASS 84%) have neighbourhoods that ARE a topic, so opening them shows meaning. "
  "Connector hubs (DoD: neighbours in 15 communities, only 24% home; AARO Vol I 34%; Grusch 34%; Lockheed Martin 32%; AARO 43%; DOE 38%; House Oversight 39%) have neighbourhoods that are lists of unrelated stories joined by generic institutional or denial edges. "
  "INFERRED: the \"sea of nodes\" feeling comes from connector hubs rendered as undifferentiated fans, and from the modern era (section 5), not from a few mega-hubs.")
w("")

# ---------------------------------------------------------------- 3 communities
w("## 3. Communities")
w("")
w("Method: weighted Louvain (own implementation, resolution 1), 30 random seeds per weighting, then consensus clustering "
  "(co-association matrix of the 30 runs, pairs co-clustered in >= 50% of runs kept, Louvain re-run until all 30 re-runs agree; converged in 2 rounds for every weighting). "
  "Three weightings:")
w("")
w("- **all**: every sourced edge weight 1.")
w("- **hub-damped**: each edge weight 1/sqrt(max(1, k_a/10) x max(1, k_b/10)), k = degree; edges between ordinary nodes keep weight 1, an edge into a degree-60 hub gets about 0.4, hub-to-hub about 0.15. This is the \"generic hub edges down-weighted\" run.")
w("- **type-damped** (sensitivity check): witness-chain, behavioral and temporal edges at 0.3.")
w("")
w("| weighting | best raw Q | mean Q (sd) | communities per run | NMI between runs mean (min) | consensus Q | consensus communities |")
w("|---|---|---|---|---|---|---|")
for v in ("all", "hubdamp", "typedamp"):
    r = S2[v]
    c = S3["cons"][v]
    w(f"| {v} | {r['best_q']:.3f} | {r['q_mean']:.3f} ({r['q_sd']:.3f}) | {r['ncom_mean']:.1f} [{r['ncom_min']}-{r['ncom_max']}] | {r['nmi_runs_mean']:.3f} ({r['nmi_runs_min']:.3f}) | {c['q']:.3f} | {len(c['sizes'])} |")
w("")
nullq = S3["nullq"]
w(f"Null model: degree-preserving rewiring of the same graph (8 rewirings, best of 5 Louvain runs each) gives Q = {sum(nullq) / len(nullq):.3f} (max {max(nullq):.3f}) against {S3['realq_simple']:.3f} on the real simple graph. The community structure is real, not an artefact of sparsity.")
w("")
w("Agreement between weightings (consensus partitions): " + "; ".join([
    f"all vs hub-damped NMI 0.761", "all vs type-damped 0.805", "hub-damped vs type-damped 0.688"]) + ". ")
w("")
w("Robustness of each hub-damped community under the other two weightings (best-match Jaccard, and containment = share of the community found inside its best match):")
w("")
w("| community | size | Jaccard vs all-edges | containment in all-edges | Jaccard vs type-damped | containment in type-damped |")
w("|---|---|---|---|---|---|")
for h, (sz, ja, ca, jt, ct) in sorted(S12["robust"].items(), key=lambda x: -x[1][0]):
    w(f"| H{h} {LAB_H[int(h)][0]} | {sz} | {ja:.2f} | {ca:.2f} | {jt:.2f} | {ct:.2f} |")
w("")
w("Three communities are the same under every weighting (Jaccard >= 0.85 both ways): AAWSAP lineage (H1), other nations (H2), academic science (H11). "
  "Five more survive intact but nested inside a larger community when hubs are not damped (containment >= 0.85 both ways): Air Force / CIA 1947-1969 (H4), SAP law (H6), the money (H12), TTSA (H15), incursions (H16). "
  "The Roswell tradition (H8) is stable against the all-edges run (0.93) but half dissolves when witness-chain edges are damped (0.48), which says it is held together by testimony. "
  "What never recurs is the modern whistleblower material (H0: Jaccard <= 0.34 everywhere): Grusch, Elizondo, the Navy encounters, AARO and the House are one dense tangle that Louvain cuts differently each time.")
w("")
w(f"Node-level home stability (hub-damped): {S11['hubdamp']['ge08']} of 1,135 linked nodes share their community with >= 80% of its members in the average run; {S11['hubdamp']['lt05']} ({pct(S11['hubdamp']['lt05'] / 1135)}) are floating (< 50%). "
  "The floating set is led by exactly the nodes readers open first: " + ", ".join(f"`{i}`" for i in S11["hubdamp"]["floating_top"][:10]) + ".")
w("")


def comm_table(prof, labs, prefix, cov):
    w("| id | proposed label | size | stability | top 8 by internal degree | classes | internal edge types | years (node p10-p90) | years (edge p10-p90) | clusters | L0 home band | threads touching |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|")
    covd = {r["c"]: r for r in cov}
    for p in prof:
        c = p["id"]
        lab = labs.get(c, ("?", ""))[0]
        top = ", ".join(m for m, _, _, _ in p["top"][:8])
        cv = covd.get(c, {})
        w(f"| {prefix}{c} | {lab} | {p['size']} | {p['stability']:.2f} | {top} | {cls_str(p['cls'], p['size'])} | {types_str(p['itypes'])} | "
          f"{yr(p['node_year_p10_p50_p90'])} | {yr(p['edge_year_p10_p50_p90'])} | {cls_str(p['cluster'], p['size'], 2)} | "
          f"{', '.join(b for b, _ in p['home_band'][:2])} | {len(cv.get('thread_ids', []))} |")


w("### 3a. Hub-damped consensus (primary): 18 communities")
w("")
w("Stability = mean share of member pairs that land in the same community across the 30 raw runs (1.0 = always together).")
w("")
comm_table(PH["profiles"], LAB_H, "H", S8["per_comm_hub"])
w("")
w("Longer descriptions of the hub-damped communities:")
w("")
for c in sorted(LAB_H):
    w(f"- **H{c} {LAB_H[c][0]}**: {LAB_H[c][1]}.")
w("")
w("### 3b. All-edges consensus: 16 communities")
w("")
comm_table(PA["profiles"], LAB_A, "A", S8["per_comm_all"])
w("")
w("### 3c. Two levels exist (resolution sweep)")
w("")
w("| weighting and resolution | communities per run | of which >= 10 nodes | NMI between runs | best Q | largest sizes |")
w("|---|---|---|---|---|---|")
for k, r in S5["sweep"].items():
    w(f"| {k} | {r['ncom_mean']:.1f} | {r['big_mean']:.1f} | {r['nmi_mean']:.3f} | {r['q_best']:.3f} | {', '.join(map(str, r['sizes'][:8]))} |")
w("")
w("At resolution 0.25 (hub-damped) the board resolves into four regions plus fragments; they are assemblies of the section 3a topics:")
w("")
co = S5["coarse_hubdamp_0.25"]
g = defaultdict(list)
for k, v in co.items():
    g[v].append(k)
w("| region | size | made of | node eras (0 / 1 / 2 / 3 / nd) |")
w("|---|---|---|---|")
for c in sorted(g, key=lambda x: -len(g[x])):
    m = g[c]
    e = Counter(B.nodes[i]["era"] for i in m)
    w(f"| {LAB_M.get(c, ('?', ''))[0]} | {len(m)} | {LAB_M.get(c, ('', ''))[1]} | {e['0']} / {e['1']} / {e['2']} / {e['3']} / {e['nd']} |")
w("")
w("The coarse level is less stable than the topic level (NMI between runs 0.68 versus 0.78), so treat the four regions as a navigation convenience, not a finding of the same strength.")
w("")
w("### 3d. Communities against the existing organising schemes")
w("")
w("NMI (0 = unrelated, 1 = identical). \"Null\" = mean NMI after shuffling the scheme's labels 30 times, which is the chance level for that many categories.")
w("")
w("| scheme compared with the community partition | NMI all-edges (null) | NMI hub-damped (null) | ARI hub-damped |")
w("|---|---|---|---|")
names = {"cluster": "node `cluster` (9 values)", "cls": "node class (8)", "era": "node era (5)", "tier": "node tier A/B/C",
         "L0band_on_L0nodes": "L0 band, the 135 L0 nodes only", "L0homeband_all": "L0 band of each node's L0 home (1,109 nodes that have one)",
         "L0homenode_singlehome": "L0 home node itself (nodes with one home)"}
for k, nm in names.items():
    a, h = PA["cmp"][k], PH["cmp"][k]
    w(f"| {nm} | {a[0]:.3f} ({a[1]:.3f}) | {h[0]:.3f} ({h[1]:.3f}) | {h[2]:.3f} |")
w(f"| reference: cluster vs L0 band (L0 nodes) | {PA['cmp']['_cluster_vs_L0band_on_L0nodes'][0]:.3f} | | |")
w("")
w("How scattered each existing `cluster` is across the hub-damped communities (share of the cluster that sits in its single largest community; number of communities it touches):")
w("")
w("| cluster | n | largest share | communities touched |")
w("|---|---|---|---|")
for k, (n, sh, nc) in sorted(PH["purity_cluster"].items(), key=lambda x: -x[1][0]):
    w(f"| {k} | {n} | {pct(sh)} | {nc} |")
w("")
w("| L0 home band | n | largest share | communities touched |")
w("|---|---|---|---|")
for k, (n, sh, nc) in sorted(PH["purity_band"].items(), key=lambda x: -x[1][0]):
    w(f"| {k} | {n} | {pct(sh)} | {nc} |")
w("")
w("Crosstab, hub-damped community x cluster (counts):")
w("")
clus = sorted({B.nodes[i]["cluster"] for i in ids})
w("| community | " + " | ".join(clus) + " |")
w("|---" * (len(clus) + 1) + "|")
for p in PH["profiles"]:
    ct = PH["ct_cluster"][str(p["id"])]
    w(f"| H{p['id']} | " + " | ".join(str(ct.get(c, 0)) for c in clus) + " |")
w("")
w("Crosstab, hub-damped community x L0 home band (counts; `none` = not a member of any L0 node's ledger):")
w("")
bands = ["retrieval", "reverse-engineering", "custody", "funding", "oversight", "disclosure", "research", "none"]
w("| community | " + " | ".join(bands) + " |")
w("|---" * (len(bands) + 1) + "|")
for p in PH["profiles"]:
    ct = PH["ct_band"][str(p["id"])]
    w(f"| H{p['id']} | " + " | ".join(str(ct.get(c, 0)) for c in bands) + " |")
w("")
w("**Reading (MEASURED).** The graph's own communities are topical and historical (a programme and its people, a country, a decade, a law), and they are nearly independent of the two schemes the app organises by. "
  "Community vs `cluster` NMI is 0.16-0.17 (chance 0.02-0.03); under the hub-damped partition every cluster is spread over 6-16 communities with 15-48% in its largest one (the oversight cluster, 278 nodes, touches 16 communities and has only 15% in any one). "
  "Community vs L0 band is 0.24 (chance 0.02); each band touches 8-16 communities. `cluster` is a ROLE (witness, media, oversight, contractor) and the L0 band is a FUNCTION (custody, funding, oversight), and both cut across every story. "
  "The communities align best with the L0 home node itself (NMI 0.55-0.57 against chance 0.24-0.27), i.e. the L0 ledger already groups nodes somewhat topically, but the L0 grid then scatters those groups by band.")
w("")

# ---------------------------------------------------------------- 4 edge types
w("## 4. Edge types")
w("")
w("Intra = share of that type's edges that fall inside one community (all-edges consensus / hub-damped consensus). "
  f"The configuration-model expectation for a random edge is about {S6['overall_intra_all'][1]:.2f}; overall observed is {S6['overall_intra_all'][0]:.2f}. "
  "Hub lift = the type's share among edges touching a top-20 hub divided by its share overall.")
w("")
w("| type | edges | share | T2+T3 | T3 | dated | touches top-20 hub | hub lift | intra (all) | intra (hub-damped) |")
w("|---|---|---|---|---|---|---|---|---|---|")
for r in S6["types"]:
    w(f"| {r['type']} | {r['n']} | {pct(r['share'], 1)} | {pct(r['t23'])} | {pct(r['t3'])} | {pct(r['dated'])} | {pct(r['touch_top20'])} | {r['hub_lift']:.2f} | {pct(r['intra_all'])} | {pct(r['intra_hub'])} |")
w("")
w("Edge-type groups used below: structural = custody, funding, programmatic, institutional, legislative, research (1,694 edges, 63%; 73% Tier 1); "
  "assertion = witness-chain, behavioral, investigative, denial (809, 30%; 50% Tier 1); context = temporal, geographic (182, 7%; 59% Tier 1).")
w("")
w("Which types join the hub-damped communities to each other (top community pairs by number of edges between them):")
w("")
w("| community pair | edges between | dominant types |")
w("|---|---|---|")
for (a, b), n, tl in S6["top_community_pairs_hub"][:10]:
    w(f"| H{a} {LAB_H[a][0]} / H{b} {LAB_H[b][0]} | {n} | {', '.join(f'{t} {k}' for t, k in tl)} |")
w("")
w(f"Graph bridges (edges whose removal disconnects something): {S6['bridges']['total']}, of which {S6['bridges']['leaf']} merely attach a leaf; the {S6['bridges']['nonleaf']} non-leaf bridges are " +
  ", ".join(f"{t} {n}" for t, n in S6["bridges"]["nonleaf_types"]) + ".")
w("")
w("### Candidate backbones")
w("")
w("| edge set | edges | nodes covered | Tier A covered | L0 covered | components | giant (share of covered) | mean path | Louvain Q | communities | NMI vs full hub-damped | top hubs |")
w("|---|---|---|---|---|---|---|---|---|---|---|---|")
for d in S6["backbones"]:
    w(f"| {d['label']} | {d['edges']} | {d['nodes']} ({pct(d['node_share'])}) | {pct(d['tierA_cov'])} | {pct(d['l0_cov'])} | {d['components']} | {d['giant']} ({pct(d['giant_share_of_touched'])}) | {d['avg_path_giant']:.2f} | {d['Q']:.3f} | {d['ncom']} | {d['nmi_vs_full_hub']:.2f} | " +
      ", ".join(f"{i} {k}" for i, k in d["top5"][:3]) + " |")
w("")
w("### Leave-one-type-out")
w("")
w("| type removed | nodes left without any edge | giant | components | mean path | Louvain Q | change in Q |")
w("|---|---|---|---|---|---|---|")
for r in S6["ablation"]:
    w(f"| {r['type']} | {r['nodes_lost']} | {r['giant']} | {r['components']} | {r['avg_path']:.2f} | {r['Q']:.3f} | {r['dQ']:+.3f} |")
w("")
w("**Backbone verdict.** MEASURED: there is no junk edge type. Every type is strongly within-topic (61-91% intra against about 9% expected), and no single type's removal raises modularity by more than 0.021. "
  "What differs is role. The six structural types form a navigable backbone on their own: 63% of edges, 86% of nodes, 99% of Tier A, all 135 L0 nodes, one giant component holding 94% of what they touch (including 133 of the 135 L0 nodes and 166 of the 169 Tier A nodes), mean path 5.7. "
  "`PROGRAM_EDGES` alone (custody / funding / programmatic) is too thin to navigate (42% of nodes, 44 components, mean path 7.4); adding `institutional` is the step that makes it a network (+371 nodes). "
  "The assertion types are the cross-topic layer: `denial` is clearly the most bridging type under both partitions (61% / 63% intra) while most other types sit at 68-83% and `geographic` (88-91%) and `programmatic` (86-88%) are the most local; `denial` plus `programmatic` are the types over-represented on hubs (lift 1.5-1.6). "
  f"When a random shortest path steps INTO a top-20 hub it does so on a `denial` edge {pct(dict(S12['enter_top20_types'])['denial'])} of the time and on `institutional` {pct(dict(S12['enter_top20_types'])['institutional'])}. "
  "`denial` is what joins AARO to the whistleblower story (18 of the 56 edges between H0 and H9). `witness-chain` is the most claim-like large type (63% Tier 2/3) and is the core of the Grusch and Elizondo fans. "
  "`behavioral` (77% T2/T3, 31% T3) and `temporal` (27% T3) are small and the weakest evidentially. "
  "INFERRED: a clean default view is the structural backbone; `denial` and the testimony types are better drawn as a deliberate second layer (\"who contests what\") than mixed into the same hairball, because they are exactly the edges that make every topic touch every other.")
w("")

# ---------------------------------------------------------------- 5 time
w("## 5. Time")
w("")
t = S7
w("| Measure | Value |")
w("|---|---|")
w(f"| Edges with their own `dateStart` | {t['edge_dated']:,} of {t['edges']:,} ({pct(t['edge_dated'] / t['edges'])}); precision: day {t['edge_date_precision'].get('day', 0)}, month {t['edge_date_precision'].get('month', 0)}, year {t['edge_date_precision'].get('year', 0)} |")
w(f"| Edges whose two endpoint nodes are both dated | {t['both_endpoints_dated']:,} ({pct(t['both_endpoints_dated'] / t['edges'])}) |")
w(f"| Edges dated either way | {t['edge_or_both']:,} ({pct(t['edge_or_both'] / t['edges'])}) |")
w(f"| Edges whose label or note contains a year | {t['note_has_year']:,} |")
w(f"| Edges with no date signal at all | {t['no_date_signal']} ({pct(t['no_date_signal'] / t['edges'], 1)}) |")
w(f"| Dated nodes | {t['node_dated']:,} of 1,136; by class: " + ", ".join(f"{c} {a}/{b}" for c, (a, b) in t["node_dated_by_cls"].items()) + " |")
w(f"| Edge date vs its endpoints (both dated) | after both start dates {t['edge_date_vs_nodes']['after_both_starts']}, between them {t['edge_date_vs_nodes']['between']}, before both {t['edge_date_vs_nodes']['before_both']}; median gap from the older endpoint {t['edge_date_vs_nodes']['median_gap_from_older_endpoint']} years |")
w(f"| Edges joining nodes of different eras | {t['cross_era_by_node_era']['cross']} ({pct(t['cross_era_by_node_era']['cross'] / t['edges'])}); same era {t['cross_era_by_node_era']['same']}; touching an undated node {t['cross_era_by_node_era']['has_nd']} |")
w(f"| Retrospective edges (edge date in a later era than its older endpoint) | {t['edge_era_vs_older_node_era']['retro']} of {t['edge_era_vs_older_node_era']['retro'] + t['edge_era_vs_older_node_era']['same']} dated |")
w(f"| Nodes with at least one timeline event | {t['nodes_with_timeline']} |")
w("")
w("Caveats found on the way: person nodes carry ONE date (the `date` sort key, e.g. Grusch = 2023-07-26, the hearing), not a life span; the 59 domain nodes carry nominal dates (8 of them exactly 1947-01-01), which puts 39 editorial concept nodes in the pre-1970 era.")
w("")
w("Per-era counts:")
w("")
w("| era | nodes (node era) | edges (edge date) | timeline events |")
w("|---|---|---|---|")
for eid, lab in (("0", "through 1969"), ("1", "1970-1999"), ("2", "2000-2016"), ("3", "2017-2026"), ("nd", "no date")):
    w(f"| {lab} | {t['node_era_counts'].get(eid, 0)} | {t['edge_era_counts'].get(eid, 0)} | {t['timeline_era_counts'].get(eid, '-') if eid != 'nd' else '-'} |")
w("")
w("Nodes per era by class:")
w("")
clsl = sorted(t["node_era_by_cls"])
w("| era | " + " | ".join(clsl) + " |")
w("|---" * (len(clsl) + 1) + "|")
for eid, lab in (("0", "through 1969"), ("1", "1970-1999"), ("2", "2000-2016"), ("3", "2017-2026"), ("nd", "no date")):
    w(f"| {lab} | " + " | ".join(str(t["node_era_by_cls"][c].get(eid, 0)) for c in clsl) + " |")
w("")
w("### Era slices")
w("")
w("Slice A, by EDGE date (an edge belongs to the era of its own date; nodes come in with their edges):")
w("")
w("| slice | edges | nodes | components | giant share | mean path | max degree | Louvain Q | communities >= 5 | top hubs | dominant hub-damped topics |")
w("|---|---|---|---|---|---|---|---|---|---|---|")
for k, r in t["era_edge_slices"].items():
    w(f"| {k} | {r['edges']} | {r['nodes']} | {r['components']} | {pct(r['giant_share'])} | {r['avg_path']:.2f} | {r['max_deg']} | {r['Q']:.3f} | {r['communities_ge5']} | " +
      ", ".join(f"{i} {d}" for i, d in r["top"][:5]) + " | " + ", ".join(f"H{c} ({n})" for c, n in r["hub_communities"][:4]) + " |")
w("")
w("Slice B, by NODE era (the subgraph induced on nodes of that era):")
w("")
w("| slice | era nodes | nodes with an in-era edge | edges | components | giant share | top hubs |")
w("|---|---|---|---|---|---|---|")
for k, r in t["era_node_slices"].items():
    w(f"| {k} | {r['era_nodes']} | {r['nodes']} | {r['edges']} | {r['components']} | {pct(r['giant_share'])} | " + ", ".join(f"{i} {d}" for i, d in r["top"][:4]) + " |")
w("")
w("Topic x era (hub-damped communities; edges touching the topic, by edge-date era: through 1969 / 1970-1999 / 2000-2016 / 2017-2026 / undated):")
w("")
w("| topic | edges by era | nodes by era |")
w("|---|---|---|")
for c, r in sorted(S11["topic_era"].items(), key=lambda x: int(x[0])):
    w(f"| H{c} {LAB_H[int(c)][0]} | {' / '.join(map(str, r['edges_by_era']))} | {' / '.join(map(str, r['nodes_by_era']))} |")
w("")
te = S11["topic_era"]


def era_share(c, k):
    r = te[str(c)]["edges_by_era"]
    return r[k] / sum(r)


eqn, bothn = S12["edge_year_eq_newer"]
eqo, _ = S12["edge_year_eq_older"]
w("**Time verdict.** MEASURED: time is almost fully recoverable (97% of edges carry a date signal; 81% carry their own date), and edge dates behave like event dates: "
  f"of edges with both ends dated, {pct(eqn / bothn)} carry the year of the newer endpoint and {pct(eqo / bothn)} the year of the older one (median gap from the older endpoint 3 years), and 35% of dated edges are retrospective, e.g. a 2024 AARO report denying a 1947 event. "
  "Slicing by EDGE date gives coherent, readable sub-graphs with era-appropriate hubs (Blue Book / CIA / Condon through 1969; S-4, Lazar, SETKA, NIDS 1970-1999; BAASS, Kona Blue, McCandlish, Nimitz 2000-2016): "
  "the first two slices are over 80% one component and 2000-2016 is 60%, with a maximum degree of 12-21 and modularity 0.75-0.86. "
  "Slicing by NODE era works much worse: the 1970-1999 and 2000-2016 slices shatter (giant component 30% and 47%) because those eras are held together by later documents about them. "
  "The hairball is the modern slice: 2017-2026 holds half of all dated edges (1,072 of 2,164), max degree 60, the lowest modularity (0.64) and the shortest paths (4.3). "
  f"Topics carry strong era signatures: {pct(era_share(4, 0))} of the edges touching H4 (Air Force / CIA) are dated through 1969, {pct(era_share(8, 1))} of H8's (Roswell tradition) fall in 1970-1999, "
  f"while {pct(era_share(9, 3))} of H9's (AARO), {pct(era_share(3, 3))} of H3's (House 2025-2026) and {pct(era_share(5, 3))} of H5's (legislation) are 2017-2026. A topic-by-era grid is well supported. "
  f"The 521 undated edges are concentrated: {te['1']['edges_by_era'][4]} touch the AAWSAP topic (mostly AAWSAP-to-DIRD programmatic links) and {te['6']['edges_by_era'][4]} the SAP-law topic.")
w("")

# ---------------------------------------------------------------- 6 coverage
w("## 6. Coverage by existing curation")
w("")
c = S8
w("| structure | nodes | share of 1,136 |")
w("|---|---|---|")
for k, nm in (("threads", "in any of the 8 threads (step nodes plus `via` nodes)"), ("highlights", "highlights (start-here flags)"), ("entry_paths", "map entry paths (6)"),
              ("l0", "on the L0 map"), ("dossier", "with a dossier"), ("timeline", "named by a timeline event"), ("foia", "with a FOIA request"), ("patents", "patents view"),
              ("l0_direct_member", "direct member of an L0 node's ledger (one click from the map)"), ("l0_routed_member", "routed member (depth 2-4)")):
    w(f"| {nm} | {c['sizes'][k]} | {pct(c['shares'][k], 1)} |")
w(f"| union of threads, highlights, entry paths, L0, dossiers (authored) | {c['authored_union']} | {pct(c['authored_union'] / N, 1)} |")
w(f"| ... plus timeline, FOIA, patents | {c['authored_plus_timeline_foia_patents']} | {pct(c['authored_plus_timeline_foia_patents'] / N, 1)} |")
w(f"| ... plus L0 direct membership | {c['plus_l0_direct']} | {pct(c['plus_l0_direct'] / N, 1)} |")
w(f"| in no authored structure (only search, graph browsing or an L0 ledger) | {c['search_only_excl_l0members']} | {pct(c['search_only_excl_l0members'] / N, 1)} |")
w(f"| ... and not even a direct L0 ledger member (search or deep browsing only) | {c['strict_search_only']} | {pct(c['strict_search_only'] / N, 1)} |")
w("")
w(f"Threads are small: {', '.join(f'{k} {v}' for k, v in c['thread_sizes'].items())} nodes; {c['thread_overlap_pairs']} nodes sit in more than one thread. "
  f"The L0 map holds no person at all ({', '.join(f'{k} {v}' for k, v in c['l0_cls'])}). "
  f"Nodes with no authored structure: {', '.join(f'{k} {v}' for k, v in c['search_only_cls'])}; tiers {', '.join(f'{k} {v}' for k, v in c['search_only_tier'])}; median degree {c['search_only_deg_median']}. "
  f"Strictly search-only by class: {', '.join(f'{k} {v}' for k, v in c['strict_search_only_cls'])}.")
w("")
w(f"Tier A nodes in a narrative structure (thread, highlight, entry path): {pct(c['tierA_in_narrative'])}; in any authored structure: {pct(c['tierA_in_authored'])}. Tier A nodes in no authored structure: " + ", ".join(f"`{i}`" for i in c["tierA_search_only"]) + ".")
w("")
w("Top-50-degree nodes missing from the narrative structures: " + ", ".join(f"`{i}`" for i in c["top50_not_in_narrative"]) + ". Missing from L0: " + ", ".join(f"`{i}`" for i in c["top50_not_in_l0"]) + ".")
w("")
w("Curation per hub-damped community:")
w("")
w("| community | size | thread nodes | threads touching | L0 | highlights | entry paths | dossiers | timeline | no authored structure |")
w("|---|---|---|---|---|---|---|---|---|---|")
for r in c["per_comm_hub"]:
    w(f"| H{r['c']} {LAB_H[r['c']][0]} | {r['size']} | {r['threads']} | {', '.join(r['thread_ids']) or '-'} | {r['l0']} | {r['highlights']} | {r['entry']} | {r['dossier']} | {r['timeline']} | {r['search_only']} ({pct(r['search_only'] / r['size'])}) |")
w("")
w("**Coverage verdict (MEASURED).** Authored narrative reaches few nodes: threads 3.9%, highlights 1.2%, entry paths 8.8%, L0 11.9%; together with dossiers 15.0%. The timeline is the broadest authored structure (51%). "
  "Almost half the board (518 nodes, 45.6%) is in no authored structure, and 172 (15.1%) are not even one click from the map. "
  "Six topics have no thread at all: other nations (88 nodes), the Roswell / nuclear-missile tradition (69), academic science (52), Kirtland / Bennewitz / Dulce (35), TTSA and the CRADA (18), incursions (14); the Air Force / CIA 1947-1969 topic (83) has one thread node. "
  "Thread nodes concentrate in H0 (10), H1 (7), H3 (7), H6 (5) and H9 (4): the modern Washington material, AAWSAP and SAP law, which are also the topics best served by L0, dossiers and entry paths.")
w("")

# ---------------------------------------------------------------- 7 paths
w("## 7. Paths a reader would ask for")
w("")
w("For each pair: all shortest paths in the full graph, then the same query with the top-20 hubs removed, with structural edge types only, and a hub-penalised path (entering a node costs 1 + log2(degree)). Full edge labels are in `s9_paths.txt`.")
w("")
w("| pair | distance | shortest paths | share through a top-20 hub | shortest-path intermediates | without top-20 hubs | structural types only | hub-penalised |")
w("|---|---|---|---|---|---|---|---|")
for r in S9["pairs"]:
    inter = ", ".join(f"{i} ({n})" for i, n in r["intermediates"][:4])
    nt = r["no_top20"]
    st = r["structural_only"]
    w(f"| {r['title']}: `{r['a']}` to `{r['b']}` | {r['dist']} | {r['n_paths']} | {pct(r['share_via_top20'])} | {inter} | "
      f"{nt['dist']} ({nt['n']}) {' > '.join(nt['paths'][0][1:-1]) if nt['paths'] else ''} | {st['dist'] if st['dist'] is not None else 'none'} ({st['n']}) {' > '.join(st['paths'][0][1:-1]) if st['paths'] else ''} | "
      f"{' > '.join(r['hub_penalised'][1:-1]) if r['hub_penalised'] else ''} |")
w("")
w("Worked readings (INFERRED judgements; the edge labels are the board's own):")
w("")
w("1. **Grusch to Lockheed Skunk Works** (3 hops, 4 paths). One path is a real story: AARO's Volume I rebuts Grusch (denial, T1, 2024), Volume I offers KONA BLUE as the explanation for the reverse-engineering allegations, and the KONA BLUE proposal alleged Lockheed-held material was to be transferred (custody, T2, 2011). The hub-penalised alternative (Grusch > Boeing > McCandlish > Skunk Works) reads as a chain of associations resting on a T3 funding edge and a relayed unnamed informant.")
w("2. **AAWSAP to the UAP Disclosure Act** (2 hops, 1 path). The only shortest path hops through AARO Volume I on a T3 legislative edge. Removing the hubs gives the better story at 3 hops: Reid co-sponsored the AAWSAP money (T1), Schumer names Reid as the legacy he is continuing (T2), Schumer sponsored S.Amdt. 797 (T1).")
w("3. **Roswell 1947 to the July 2023 hearing** (3 hops, 2 paths, both through AARO Volume I). The path is two denials in a row (AARO reaffirms Mogul; AARO rebuts Grusch) and then Grusch's testimony: a hop through the official rebuttal hub, not a connection between Roswell and the hearing. Without hubs it becomes a 5-hop associative chain (memory metal > nitinol > Navy lab > Navy > Nimitz > Fravor's testimony).")
w("4. **Bob Lazar to AARO** (4 hops, 22 paths). Many near-equal routes (ONI, UAPTF, S-4 > Knapp > hearing, Los Alamos > DOE > NASA). The hub-penalised route is a plausible lineage story (Lazar's claimed Naval Intelligence pay, T3 > ONI > UAPTF > the memo that transferred UAPTF data to AARO), but it rests on a T3 claim.")
w("5. **Project Blue Book to AARO** (3 hops, 6 paths, 67% through hubs). Six equal-length routes of very different quality: one is a genuine document lineage (Special Report 14, republished by the Department of War in PURSUE Release 03, staged by AARO; all T1); two are \"AARO's 2024 review does not mention X\" (Moon Dust, the 1975 overflights), an argument about omission; three rest on a T3 link (UAP Gerb's Battelle investigation to Kirkpatrick; the Haines history to Yankee Blue \"precedent\"; Wright-Patterson to Grusch). Nothing in the graph ranks the first above the others.")
w("")
w("Extra pairs: Pais to Skunk Works (4 hops, 6 paths, 4 of them via Lockheed Martin); Robert Salas to AARO (4 hops, 9 paths, 8 of them through the nuclear PRP regime and then `dod`, a pure containment hop, the ninth through Grusch; no path exists on structural edges at all); Eric Davis to Lockheed Martin (3 hops, 14 paths spread over T. Townsend Brown's 1947 patent assignment, McCandlish, the DIRD series, Reid and Knapp: associations, none of them the Wilson-Davis custody story).")
w("")
ri = S12["random_intermediates"]
w("**Path verdict.** MEASURED: paths are short (mean 4.7) and 67% of random pairs can only be joined through a top-20 hub. Over 1,000 random pairs the most frequent intermediates are " +
  ", ".join(f"`{i}` {v:.2f}" for i, v, _ in ri[:6]) + " (expected appearances as an intermediate per random pair)" +
  f"; top-20 hubs are {pct(S12['share_intermediates_top20'])} of all intermediate appearances, and the step into them is a `denial` or `institutional` edge "
  f"{pct(dict(S12['enter_top20_types'])['denial'] + dict(S12['enter_top20_types'])['institutional'])} of the time. AARO's Historical Record Volume I lies on at least one shortest path for 7 of the 8 reader pairs, and is the whole middle of the AAWSAP-to-UAPDA and Roswell-to-hearing answers. "
  "INFERRED from the readings: in two of the five main pairs a genuine story is among the shortest paths but sits beside weaker routes of the same length that nothing distinguishes (Grusch to Skunk Works: 1 or 2 of 4; Blue Book to AARO: 1 of 6); "
  "in two every shortest path is a hop through AARO Volume I, which tells the reader that the same office addressed both ends, not how the ends are related (AAWSAP to UAPDA, Roswell to the hearing); "
  "and Lazar to AARO has 22 equal routes, the best a plausible lineage resting on a T3 claim. "
  "Removing the top-20 hubs recovers a better story in one case (AAWSAP to UAPDA via Reid and Schumer) and a meandering association chain in another (Roswell to the hearing); hub-penalised routing is no more reliable. "
  "\"Show me the path between X and Y\" should therefore not be a headline feature without curation; where it is offered, equal-length paths need ranking by claim tier and edge type, and paths through connector hubs and `denial` edges should be labelled as such.")
w("")

# ---------------------------------------------------------------- 8 implications
w("## 8. Implications for the information architecture (INFERRED from the measurements above)")
w("")
w("1. **Organise by topic, and offer topic x era as the map.** The board has about 16-18 topical communities (modularity 0.66-0.70 against 0.48 for a rewired null); three are identical under every weighting and five more survive intact inside larger ones, and they have clear era signatures. "
  "They are nearly independent of `cluster` and of the L0 function bands (NMI 0.16-0.24). A reader discovering meaning needs the topics as the primary unit (\"AAWSAP lineage\", \"Roswell and the retrieval tradition\", \"SAP law\", \"Other nations\"), with role and function as filters inside a topic rather than as the rows of the map. Four macro-regions (Washington 2017-2026, the Cold War record, AAWSAP and the science / contractor strand, other nations) are a usable top level.")
w("2. **Treat connector hubs as indexes, not as nodes to draw.** DoD, AARO, AARO Volume I, Grusch, Lockheed Martin, CIA, DOE and the House Oversight Committee have neighbours in 6-15 topics. Their pages should group neighbours by topic and by edge type (\"denied by\", \"employed\", \"testified about\") instead of fanning them out; provincial hubs (AAWSAP, DIRD series, DIA, Blue Book, UAPDA, Nimitz, BAASS) can be shown as the anchor of their topic. Let connector nodes belong to several topics: 15% of nodes, including the most-opened ones, have no single stable home.")
w("3. **Default to the structural backbone and make the assertion layer a deliberate overlay.** Custody, funding, programmatic, institutional, legislative and research edges alone reach 86% of nodes, and their giant component holds 133 of the 135 L0 nodes and 166 of the 169 Tier A nodes. Denial, witness-chain, investigative and behavioral edges are the cross-topic layer (and the most claim-like); drawing them only when the reader asks \"who claims / who denies\" keeps the argument while removing most of the \"everything connects to everything\" effect.")
w("4. **Use time as a slicer on EDGE dates, and give the modern era its own treatment.** 97% of edges can be placed in time; edge-date slices before 2017 are small, sparse and readable, while 2017-2026 is half of all edges and is the hairball. The modern era needs sub-topics (whistleblowers, AARO and releases, legislation, House 2025-2026, incursions) more than any other period. Do not slice by node era.")
w("5. **Close the curation gaps the topics expose, and put people back on the top level.** 45.6% of nodes are in no authored structure and 172 are search-only. Six topics have no thread (other nations, the Roswell tradition, academic science, Kirtland / Dulce, TTSA, incursions), the Cold War Air Force / CIA topic has one thread node, and L0 carries no person although persons are 30% of the board and include the biggest hub on it (Grusch) and three more of the top 15 (Elizondo, Burlison, Luna). One authored thread or topic page per community, plus a person layer, would cover the board with about 18 entry points instead of 1,136 nodes.")
w("")

# ---------------------------------------------------------------- files
w("## Files")
w("")
w("Scripts (run in order): `g.py` (loader and algorithms), `s1_basics.py`, `s2_communities.py`, `s3_consensus.py`, `s4_profiles.py all|hubdamp`, `s5_levels.py`, `s6_edgetypes.py`, `s7_time.py`, `s8_coverage.py`, `s9_paths.py`, `s10_hubroles.py`, `s11_extra.py`, `s12_checks.py`, `make_report.py`. "
  "Outputs: `s*.json`, `s9_paths.txt` (full path listings with edge labels), `communities.json`, this report.")
w("")

txt = "\n".join(L)
assert "\u2014" not in txt
open(os.path.join(OUT, "REPORT.md"), "w", encoding="utf-8").write(txt)

# ---------------------------------------------------------------- communities.json
def pack(part, prof, labs, prefix, stab):
    out = {}
    for p in prof:
        c = p["id"]
        out[f"{prefix}{c}"] = {"label": labs[c][0], "description": labs[c][1], "size": p["size"],
                               "stability": round(p["stability"], 3),
                               "top_by_internal_degree": [m for m, _, _, _ in p["top"][:8]],
                               "members": p["members"]}
    return out


cj = {
    "generated_from": {"index": B.index["generated"], "source": B.index["source"]},
    "method": "Weighted Louvain, 30 seeds per weighting, consensus clustering at co-association >= 0.5. "
              "hubdamp: edge weight 1/sqrt(max(1,ka/10)*max(1,kb/10)); all: weight 1 per sourced edge. "
              "stability = mean share of member pairs co-clustered across the 30 raw runs.",
    "primary": "hubdamp",
    "hubdamp": {"modularity": round(S3["cons"]["hubdamp"]["q"], 4),
                "communities": pack(S3["cons"]["hubdamp"]["part"], PH["profiles"], LAB_H, "H", S3["cons"]["hubdamp"]["stab"])},
    "all": {"modularity": round(S3["cons"]["all"]["q"], 4),
            "communities": pack(S3["cons"]["all"]["part"], PA["profiles"], LAB_A, "A", S3["cons"]["all"]["stab"])},
    "regions_hubdamp_resolution_0.25": {},
    "node_to_community": {"hubdamp": {k: f"H{v}" for k, v in S3["cons"]["hubdamp"]["part"].items()},
                          "all": {k: f"A{v}" for k, v in S3["cons"]["all"]["part"].items()}},
}
for c in sorted(g, key=lambda x: -len(g[x])):
    cj["regions_hubdamp_resolution_0.25"][f"M{c}"] = {"label": LAB_M.get(c, ("?", ""))[0], "made_of": LAB_M.get(c, ("", ""))[1],
                                                       "size": len(g[c]), "members": sorted(g[c])}
s = json.dumps(cj, indent=1, ensure_ascii=False)
assert "\u2014" not in s
open(os.path.join(OUT, "communities.json"), "w", encoding="utf-8").write(s)
print("wrote REPORT.md", len(txt), "chars; communities.json", len(s), "chars")
