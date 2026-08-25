# Probable duplicate nodes, 22 August 2026

Found while wiring the three underconnected Tier A nodes. `ndaa26-uap-provisions`
sits at degree 1 not because it is peripheral but because **it is one of three
nodes for the same statute**, and its edges are split across all three.

This is the failure that already cost this board once. From the 13 August handoff:
*"Five people were on the board twice, splitting their edges and sources, with the
twin rendering its own slug as its name."* That was fixed for people by unifying
the id rules. Nothing ever detected it for entities.

A duplicate is worse than a missing node. Both copies look sourced, each carries a
fraction of the evidence, and they can hold different tiers — so the board grades
the same object two different ways at once.

## Detection

`tools/INTEGRITY.json` -> `probable_duplicate_node`, generated on every merge.
The test is deliberately narrow: same class, at least one shared source URL, and
label token-sets overlapping by 60% after dropping structural words. Pairs whose
labels carry different years are excluded, which is what separates the AARO
FY2023/FY2024/FY2025 annual reports from real duplicates.

18 pairs reported. 12 of them are the 9 real groups below; 6 are false positives
that are listed and explained at the end.

**This is a report, not a gate check.** A collapse deletes a node, and this repo
requires that to be approved and recorded — `research/_removed.json` carries
`_approved_by`. The gate check goes in once the collapses below are approved;
adding it now would turn the gate red on a condition nobody has authorised anyone
to fix.

## The nine groups, with what each collapse would recover

| group | nodes | tiers | degree | claims | note |
|---|---|---|---|---|---|
| **FY2024 NDAA sec. 1687** | `ndaa-fy2024-1687`, `ndaa-fy2024-sec1687`, `ndaa24-sec1687` | A / B / B | 4 + 4 + 3 | 11 + 6 + 7 | The board's own desc calls this "the most important single provision on this board". It is here three times. |
| **AARO FY2025 annual report** | `aaro-fy2025-annual-report`, `aaro-fy2025-report`, `aaro-fy2025-report-2026` | A / B / B | 14 + 4 + 3 | 30 + 6 + 5 | The three subs disagree on the release date: 21 July, 20 July, 21 July 2026. That conflict has to be resolved in the collapse. |
| **FY2026 NDAA UAP provisions** | `fy2026-ndaa-uap-provisions`, `ndaa-fy2026-uap-provisions`, `ndaa26-uap-provisions` | B / B / A | 4 + 2 + 1 | 10 + 7 + 10 | This is why `ndaa26-uap-provisions` reads as an underconnected Tier A node. |
| **UAP Science Advisory Council** | `uap-science-advisory-council`, `uap-science-advisory-council-2026` | A / C | 14 + 8 | 19 + 4 | Same body graded Tier A and Tier C simultaneously. |
| **PURSUE** | `pursue-releases`, `pursue-programme-2026` | A / A | 38 + 14 | 19 + 4 | Both Tier A. The larger is already the 6th most connected node on the board. |
| **UAPDA FY2027 Burlison amendment** | `uapda-fy2027-house-adopted`, `burlison-uapda-fy2027-ndaa-amendment` | C / C | 7 + 5 | 4 + 4 | Subs disagree on adoption date: "23 July 2026" vs "22-23 July 2026". |
| **Burlison MITRE production demand** | `burlison-mitre-letter-2026`, `burlison-mitre-demand-2026` | A / B | 9 + 3 | 10 + 4 | Same 10-page letter of 22 May 2026. |
| **Kirkpatrick SciAm op-ed** | `kirkpatrick-sciam-oped-2024`, `kirkpatrick-sciam-oped` | C / C | 4 + 2 | 3 + 2 | Same op-ed, 19 January 2024. |
| **Jesse Marcel Sr.** | `jesse-marcel`, `jesse-marcel-sr` | A / B | 4 + 4 | 4 + 3 | A **person**, twice, at two tiers. This is the exact class the August fix was supposed to have closed. |

Collapsing all nine takes 19 nodes to 9 and consolidates roughly 70 edges and 130
claims that are currently split.

**Do not collapse mechanically.** Three of these groups contain factual conflicts
between the copies (two release dates, two adoption dates). Whichever copy
survives, the conflict is a finding and belongs on the survivor, not in a diff.

## Six false positives, and why each is real

| pair | why they are distinct |
|---|---|
| `dird-aneutronic-fusion-propulsion` / `-2` | Two real DIRDs. Both PDFs were downloaded and read: DIA-08-1011-003 at 50 pages and DIA-08-1011-004 at 37 pages, both dated 1 November 2010. **Both cover pages carry the identical title "Aneutronic Fusion Propulsion"** and the DIA list distinguishes them as I and II. A reader of this board cannot tell them apart either, so their labels should carry the document numbers. |
| `dodm-5205-07-series` / `dodm-5205-07-v1` | The four-volume series and its Volume 1. |
| `gimbal-video` / `gofast-video` | Two Navy ATFLIR videos of January 2015. |
| `house-armed-services` / `senate-armed-services` | Two chambers. |
| `l-skinwalker` / `l-utah` | The ranch and the region containing it. |
| `earthtech-international` / `institute-advanced-studies-austin` | Related Puthoff entities; the first's label already names the second, which is worth tidying but they are not one node. |

## Next

1. Stewart approves or rejects the nine collapses, naming the survivor in each.
2. Collapses land through `research/_removed.json` with `alias` entries, so every
   reference re-points instead of orphaning — the sweep added on 22 August now
   covers `locId`, `instId` and `domains` as well as the timeline.
3. The duplicate check moves from the integrity report into `verify.py` as a gate
   check with a self-test, so this cannot silently accumulate again.


---

# Resolved, 22 August 2026

Stewart approved all nine collapses the same day and delegated the choice of
survivor. **19 nodes to 9.** Recorded in `research/_removed.json` under
`_approved_by`.

| survivor | absorbed | claims carried | sources carried |
|---|---|---|---|
| `ndaa-fy2024-1687` | `ndaa-fy2024-sec1687`, `ndaa24-sec1687` | 7 | 2 |
| `aaro-fy2025-annual-report` | `aaro-fy2025-report`, `aaro-fy2025-report-2026` | 11 | 2 |
| `ndaa26-uap-provisions` | `fy2026-ndaa-uap-provisions`, `ndaa-fy2026-uap-provisions` | 9 | 1 |
| `uap-science-advisory-council` | `uap-science-advisory-council-2026` | 4 | 0 |
| `pursue-releases` | `pursue-programme-2026` | 4 | 0 |
| `uapda-fy2027-house-adopted` | `burlison-uapda-fy2027-ndaa-amendment` | 4 | 1 |
| `burlison-mitre-letter-2026` | `burlison-mitre-demand-2026` | 4 | 0 |
| `kirkpatrick-sciam-oped-2024` | `kirkpatrick-sciam-oped` | 2 | 0 |
| `jesse-marcel` | `jesse-marcel-sr` | 3 | 2 |

48 claims and 8 sources carried onto survivors; the rest were already duplicated
there and were deduplicated by normalised text and by URL.

## What consolidation was worth

| node | edges before → after | claims before → after |
|---|---|---|
| `ndaa-fy2024-1687` | 4 → 11 | 11 → 18 |
| `aaro-fy2025-annual-report` | 14 → 19 | 30 → 42 |
| `ndaa26-uap-provisions` | 1 → 6 | 10 → 19 |
| `pursue-releases` | 38 → 47 | 19 → 23 |
| `jesse-marcel` | 4 → 8 | 4 → 7 |
| `uap-science-advisory-council` | 14 → 17 | 19 → 23 |

`ndaa26-uap-provisions` was one of the three underconnected Tier A nodes. It was
never underconnected; it was one of three. `tierA_underconnected` fell 3 → 2 on
the collapse alone.

## Two things the collapse itself fixed

**Collapse no longer deletes edges.** `merge.py` re-points an edge through the
alias map onto the survivor, merging it where one already exists and discarding
the self-edges a collapse creates. Applying that to the aliases already in
`_removed.json` **recovered 27 edges the August collapses had silently dropped.**

**The check is now in the gate.** `no unapproved duplicate nodes` computes the
groups from the board itself rather than reading `INTEGRITY.json`, so it is a
property of what shipped and is self-tested. The six genuine non-duplicates live
in `tools/DUPLICATES_ACCEPTED.json`, each with a reason saying what distinguishes
them. Anything unlisted fails the build.

## Conflicts preserved rather than resolved away

Two groups disagreed with themselves, and the disagreement is now a claim on the
survivor:

- The AARO FY2025 report's three copies gave **21 July, 20 July and 21 July 2026**
  as the release date. Two of three say 21 July, which is retained, but three
  independent passes over one document disagreeing is itself a finding.
- The UAPDA amendment's two copies gave **23 July** and **22-23 July 2026** for
  House adoption. The range is retained as the wider statement.
