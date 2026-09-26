# Phase 11, detailed: graph views rebuilt; the L0 map retired; places; phones everywhere

Written 26 September 2026 from `notes/PLAN-2026-09-24.md` section "Phase 11" and the critic's standing
findings: the 1366 map shows unnamed "+N" chips and no links; the neighbourhood ring names only a family
where the predicate is hidden, and names two steps out give no "via whom". Branch
`redesign/p11-graph-views`. Opus 5.5, high. Subagent concurrency at most 2.

## Decisions made here

- **The node tier letter stays in the data, and leaves the UI entirely.** `regrade.py` keeps computing it
  (verify, GOLDEN and the analyst read it); no page prints A, B or C, and nothing sorts a reader-facing list
  by it. Dropping the regrade itself is not worth the churn now.
- **Places: no downloaded basemap.** Fetching a gazetteer or a Natural Earth file is a download this
  session will not make unattended. `research/_places.json` takes the coordinates already authored in
  `regrade.py` (the 76-entry table), each marked `coordSource: "board table"`, plus any a location node
  carries itself. `#/places` draws them on a plain longitude/latitude graticule (no coastlines), beside a
  list grouped by country and region, each place with its events and topics. Replacing the graticule with
  a cited basemap is recorded for phase R.

## Tasks

1. **The grouped neighbourhood** replaces the ring: the entity in the centre, its families in labelled
   columns, every neighbour named with the link's reading (predicate phrase where shown, the authored
   sentence on hover and on tap), the orthogonal lines kept; two steps out opens one family at a time and
   says "via <name>". C10 retires with the ring, replaced by a check on the grouped view (every neighbour
   named once, grouped by its family, the via-name present for two-step nodes), with poisons.
2. **The L0 map retires** in one commit: `tools/build_l0_layout.mjs`, the L0 selection and budget, the
   force-layout bake, `map.json`'s cells, the map page and its checks (C2 to C6, C11's map half, C12's chip
   half), with their replacements already on the Atlas. `#/map` redirects to `#/atlas`. Keep what other
   surfaces still read (dossiers ship through `build_app_data.py`; move their source to research, not to
   `l0-model.json`, if it still routes through it). GOLDEN loses the l0 counts, explained. The deferrals
   recorded in phase 2 (the bake, the dossier copy) close here.
3. **Places** as decided above: side-car, event-to-place links from existing edges and dates, `#/places`
   with the graticule plot and the list, a check with a poison (every place with coordinates is plotted
   and listed once).
4. **Phones everywhere:** every page works at 375 wide; C26 covers every route in the app.
5. **The blind critic loop** (`notes/critic/p11-round-N.md`).
