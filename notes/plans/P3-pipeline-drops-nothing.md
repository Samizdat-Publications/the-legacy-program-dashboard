# Phase 3, detailed: the pipeline drops nothing

Written 25 September 2026 from `notes/PLAN-2026-09-24.md` section "Phase 3" and a read-only measurement of
today's data by an Opus agent (numbers below are measured, not copied from the appendices). Branch
`redesign/p3-pipeline-drops-nothing`, cut from master after phase 2 lands. Opus 5.5, high.

## Measured

| defect | today | where |
|---|---|---|
| entity fields dropped by merge | `conflicts` 22 items on 15 records, `unverified` 99 on 48, `openQuestions` 18 on 5 (all `w6-international`), `short` 1, `domains` 1 | `merge.py:465-477` builds the entity with a fixed field list; `merge_entity` 309-323 unions only claims, sources, `_domains`; the `_corrections` overlay (483) copies only label, desc, sub, cluster, tier. People lose nothing |
| singular edge keys | 62 records carry `source`, 62 `tier` (`_rs-aawsap-dirds` 42, `_rs-sap-docs` 20). 15 `source` values carry a URL no twin has; 2 `tier` values are stronger than what ships | merge reads only `sources`, `claimTier` (527-532) |
| unknown edge types | 89 records, 35 strings (`contains` 32, `testimony` 13, `authorship` 7, `oversight` 4, ...) all silently become `programmatic` | 522-523; type read from `type` or `rel` (518) |
| claim dedupe | key built from full text (226) but compared on the first 120 characters (228): 4 nodes ship a claim twice | anna-paulina-luna, eli-crane, hearing-2025-09-09, uap-nda-waiver-directive-2026 |
| person date conflicts | 33 people, first file wins silently | `merge_person` 290-293; `DATE-CONFLICTS.json` holds only 14 entity records |
| entity date corrections | overlay (483) has no dateStart/dateEnd | only `sapoc` today, already right at source |
| `_edge_tiers.json` | 16 records ingested as edges by the glob (367) | its reader is `load_edge_adjudications` (946-961) |
| orphan denial verdicts | 3, all keyed on collapsed ids (`cia-haines-1997` twice, `sue-gough`) | `emit()` 1235-1255 prints `!!` only |
| unadjudicated denials | 22 of 219 denial edges have no `denialKind`; `build_app_data.py:280` defaults the denier to end `a`, and `node.ts` prints "issued here/directed here" for them | |
| dossier claims | of 1,319 shipped T1 dossier claims, 40 match merge's `SECONDARY_PAT`, 22 match `INTERESTED_PARTY_PAT` without `ATTRIBUTION_PAT` | loaded raw by `build_l0.py:558-570`; the node rule is `remediate_tiers` (837-869) |
| timeline tier | one field, two vocabularies: A 568, B 232, C 81, and 165 numeric (ints and strings mixed), 13 none | passed through by `build_app_data.py` 418, 522; the analyst groups by it |
| em dashes in labels | 37 node labels, 2 edge labels, 4 timeline labels (13 more in timeline texts) | emitted by `build_app_data.py` |
| person status | active 198 (about 35 by default), dead 70, former 46, alive 10, unknown 7, deceased 4, missing 1, fabricated 1, resolved 1 | |
| `domains` | `build_app_data.py:458-459` replaces authored person topic tags with file provenance | |
| entityInfo | never aliased (566-580); keys that are not nodes: `dird-collection`, `dod-sapco-arch`, `cia-haines-1997`, `ndaa-fy2024-sec1687`, plus junk keys (`domain`, `title`, `scope`, `thesis`, `throughLine`, `counts`, `_note`, ...) | |

## Decisions (made here, so the executing session does not re-decide)

1. **Carry, do not drop.** Entities keep `conflicts`, `unverified`, `openQuestions`, `short`, `domains`
   (unioned across files like people's). The `_corrections` overlay also carries `dateStart`/`dateEnd`. The
   node page shows an entity's own `openQuestions` after its dossier's (C23 counts both).
2. **Singular edge keys are aliases**, merged into `sources` (union) and `claimTier` (strongest), and then
   the same caps apply as to any edge. Rejecting them would throw away 15 URLs.
3. **Unknown edge types are mapped explicitly, never coerced.** `schema/vocab.json` maps each of the 35
   authored verbs to one of the twelve types and the edge keeps `authoredVerb` for phase 7. A verb not in
   the map is a REJECT. Default mapping (the executing session reads each edge's own label and may move a
   verb to a better type, recording why): `contains`, `subsidiary-of`, `subordinate-to`, `managed`,
   `maintains`, `transfers-records-to`, `same-as` to institutional; `testimony` to witness-chain;
   `authorship`, `authored` to research; `oversight`, `implements`, `excludes`, `instrument`, `creates`,
   `defines`, `defines-audience`, `codifies`, `removes-oversight-by`, `reissues-and-cancels`,
   `incorporates-by-reference`, `establishes-role-of`, `amends`, `regulates-transfer-into`, `authorizes`,
   `falls-outside` to legislative; `sponsored`, `contracted`, `conditions-funding-on` to funding;
   `prompted` to temporal; `produced`, `produces`, `structural` to programmatic; `held-by` to custody;
   `denied-by` to denial with its ends swapped so the denier is `a`, and it joins the unadjudicated list.
   Moving edges between types changes `regrade.py`'s weighted degree, so node tiers may move: measure,
   and record every moved tier in the commit.
4. **Small fixes:** one dedupe key (the full normalised text) on both sides; person date conflicts are
   RECORDED in `DATE-CONFLICTS.json` (the choice itself does not change); `_edge_tiers.json` is skipped by
   `load()`; denial verdict keys map through `_removed.json`'s aliases, and a verdict that still matches no
   edge is a hard error; the unadjudicated denials are listed in `tools/UNADJUDICATED-DENIALS.json`, a
   report now, a failing check once phase R clears them.
5. **The sourcing rules reach dossier claims:** the same `remediate_tiers` caps as node claims, applied
   where `build_l0.py` loads dossiers, logged to `REGRADE_REPORT.json`. **Timeline:** `grade` (A/B/C) and
   `claimTier` (1/2/3) become two fields; `tier` is no longer shipped; the analyst tool's `group_by`
   follows in phase 12. **Denial direction:** `build_app_data.py` sets `by` only from an adjudicated
   `denier`; the node page prints "direction not adjudicated" for the rest.
6. **`schema/vocab.json`** holds classes, clusters, the twelve edge types with reader names, blurbs and
   layers (moved from `app/src/vocab.ts`, which then reads `/data/vocab.json`), the authored-verb map, person
   `status` values, strands, precisions and tier words. `merge.py`, `build_app_data.py` and `verify.py` read
   it; `audit_independent.py` and C22 restate it. `schema/research.schema.json` rejects unknown values of
   enumerated fields and warns on unknown fields.
7. **Display labels:** node `label`/`short`, edge labels and timeline labels have a spaced em dash replaced
   by " - " at build time, listed in `tools/DISPLAY-NORMALISED.json`. Claim texts, source strings and
   timeline texts are never touched (they may be quotations).
8. **Person `status`:** validated against the nine values in use; nothing renamed.
9. **Cleanup:** provenance ships as `sourceFiles`, authored topic tags stay `domains`; entityInfo keys are
   aliased, and keys that name no node are listed as rejects (junk keys dropped with the list recorded).
   **Deferred:** dropping build-date stamps. Home prints the board's generated date and nothing else can
   supply it reproducibly yet; it goes with phase 8's source registry.

## Checks (each with a poison; verify.py's `--self-test` pattern, or C-checks for the page)

- verify: authored conflict and unverified items on entities equal the shipped count; every authored
  edge verb is either one of the twelve types or in the verb map; no node carries a claim twice; no
  timeline event ships a `tier` mixing vocabularies; every denial edge without `denialKind` is in the
  report; no display label carries a spaced em dash.
- app: C23 already counts unverified notes and open questions on the page, and now sees more on
  `s-4-papoose-lake`, `dulce-base`, `tr-3b` (add one of them as a third C23 subject). A new C30: every
  denial row that the data does not adjudicate says so.

## Acceptance

Gate green; GOLDEN updated with every moved count explained; the restored items visible on S-4, Dulce and
TR-3B; `REJECTS.json` empty.
