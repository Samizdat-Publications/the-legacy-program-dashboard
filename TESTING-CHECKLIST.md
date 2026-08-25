# The Program — QA pass

**Historical framing, still-useful checklist.** Written as the first job of the 13 August
local session; §12 source spot-checks were never started and remain outstanding.
Open `dist/the-program.html` by
double-clicking it. Work through this in a real browser. Click real things.

Skip everything marked **[ANALYST]** — no API key yet.

> **CORRECTION, 24 August 2026.** This section used to say the scripted no-key mode was
> "already working as designed". It was not. `scriptedReply()` had been inherited from the
> sibling board with a single string swapped, so a reader with no API key was answered
> about JPL headcount and two missing scientists — confidently, at length, with real
> figures, from a different project. Rewritten and now covered by
> `tools/test_scripted_analyst.mjs`. **Do not skip the analyst rows on the assumption they
> are fine.** See `notes/ANALYST-NOKEY-2026-08-24.md`.

Log findings as: **`#n · severity · view · what you did · what happened · what should have
happened`**. Severity is `BROKEN` (unusable or wrong data) · `UGLY` (works, looks bad) ·
`NIT`. Fix in that order, rebuild and re-verify after each one rather than batching.

Two things worth knowing before you start:

- The board was verified headless at 1600×1000 and 2550×1465. **Anything a person does that
  a screenshot script does not — hovering, dragging, resizing, scrolling a long list,
  clicking twice, using the keyboard — is untested.** That is where the bugs are.
- The board was ported from a design tuned for **52 nodes**. It now carries **976**. Where
  something looks wrong, ask whether it is broken or merely never designed for this scale.
  Both are worth logging; they get fixed differently.

---

## 0. Load

- [ ] Opens from a double-click with no server, no console errors *other than* a font CDN
      failure if offline. Open devtools and check.
- [ ] Time from open to a settled map. Note it. It runs 1,600 layout steps before first paint.
- [ ] Top bar reads `The Program`, `Program map live`, `PURSUE release 5 · 2026.08.07`.
- [ ] Stats strip: ENTITIES 976 / SOURCED LINKS 1788 / TIER A 146 / DOCUMENTED 59% of 4037
      claims / DENIALS 172 / CUSTODY 102. Anything else means the merge and the build
      disagree — rebuild.
- [ ] Resize the window from wide to ~900px and back. The four-row shell should never
      scroll as a whole; only the view surface scrolls.

## 1. Network map — the highest-risk surface

- [ ] Node plates are readable and **do not overlap each other**. Overlapping plates is the
      one thing the eye cannot forgive; log any you find with names.
- [ ] Labels on non-person nodes are truncated to ~24 chars. Full name should appear on
      hover and in the dock.
- [ ] **Hover** a node: tooltip appears, border and glow come up.
- [ ] **Click** a node: dock opens, neighbourhood computes, non-members dim, edge hue
      switches from strength to type. Time it — this is where the freeze used to be.
- [ ] Click a node with very high degree (`david-grusch`, `aaro`, `dod`). Does it stall?
- [ ] **1 hop / 2 hops / 3 hops.** Each should grow the neighbourhood outward. 3 hops on
      `david-grusch` is the worst case on the board — try it deliberately.
- [ ] **clear** returns to the full rest state.
- [ ] **Drag** empty canvas to pan. **Wheel** to zoom about the cursor. The page must not
      scroll under the map. A drag that ends on empty space must **not** clear the selection.
- [ ] `+` / `−` / `reset` buttons.
- [ ] Zoom out far: person plates should drop to dots. Zoom in: labels return.
- [ ] The insight callout (STRONGEST PAIR) — `Show me on the map`, `Last pattern`,
      `Next pattern`, and the `×`. All four patterns should be reachable and all four should
      frame something real on the map.
- [ ] Toggle each of the 12 **connection types** in the rail. Removing all of them should
      not throw. Custody, denial, funding and legislative should each be visibly distinct —
      they had no entry in `dominantType` until recently and rendered as fallback grey.
- [ ] Note the fps badge at rest and while dragging.

## 2. Rail filters

- [ ] Each **Status** chip (Active / Former / Deceased / Classified / Denied / Disputed).
- [ ] Each **Tier** chip. Tier A should return ~146 nodes, not almost everything.
- [ ] Each of the nine **Cluster** chips.
- [ ] The four **Axis** chips (Custody 3, Custody 2+, Access 3, Disclosure 3).
- [ ] **Compose** filters: within a group behaves as OR, across groups as AND. Verify with a
      combination you can count by hand.
- [ ] A combination that matches **zero** nodes — does the map empty gracefully or throw?
- [ ] Filters must reflect in the stats strip.
- [ ] Collapse and expand the rail.

## 3. Detail dock

- [ ] Click a **person** (`david-grusch`), an **institution** (`mitre-corporation`), a
      **program** (`aawsap`), a **location** (`l-wright-patterson`), a **document**
      (`aaro-historical-record-vol1`), an **event** (`nimitz-2004`), a **legislation** node,
      and a **research domain**. All eight classes must open a dossier, not a blank.
- [ ] Header: class eyebrow, status badge, name, affiliation, location, date.
- [ ] Assessment block: tier badge with its note, and the **three axes as 3-pip meters**
      labelled Custody proximity / Access level / Disclosure role. Never a sum, never a
      rating out of ten.
- [ ] The re-grade rationale should read like *"Re-graded A on a global pass (rank 1 of 975,
      score 208). 71 connections, 37 of them custody/witness/funding/programmatic, 10 official
      denials recorded against it."* — verify the numbers are plausible for the node.
- [ ] All four tabs: **DOSSIER / CHAIN / LINKS / SOURCES**.
- [ ] **CHAIN** on a node with no sequence chain should explain why that is a finding rather
      than render empty.
- [ ] **LINKS** — every connection with a plain-language sentence explaining *why*, strongest
      first. Check a custody edge and a denial edge specifically.
- [ ] **SOURCES** — claims grouped Tier 1 / 2 / 3, each with attribution. Find a demoted
      claim (they carry `DEMOTED from Tier 1 … needs primary replacement`) and confirm it
      reads honestly rather than looking like a bug.
- [ ] A node with **no sources** must say `No attributed source on file for this entity.`
- [ ] One of the **65 stubs** (`pogo`, `l-paris`, `509th-bomb-group`) — `desc: null` should
      print as a stated gap, not as empty space.
- [ ] Absent values print `NOT REPORTED` / `NOTHING RECORDED`, never blank, never zero.
- [ ] **Drag the dock's left edge** to resize. Reload — width should persist.

## 4. Timeline

- [ ] **Four** columns: THE PROGRAM / WITNESS CHAIN / OVERSIGHT / THE COVER-UP. The grid was
      hard-coded to three and the fourth collapsed to a ~30px gutter — confirm that is gone.
- [ ] Scroll the full 857 entries. Note where it gets slow.
- [ ] Year gutter is sticky and prints only when the year changes.
- [ ] Each card: title, one sentence, and a stamp with the formatted date **plus its
      precision** (`day-precise` / `month-precise` / `year-precise` / `ranged`). Precision is
      rendered, never smoothed.
- [ ] Click a card with a `node` — does it drive the map?
- [ ] `year` / `quarter` / `month` zoom.
- [ ] The four overlay toggles.
- [ ] Narrow the window until the columns stack; each entry should then carry its strand as a chip.
- [ ] Read the header copy. It should argue the 79-year gap between the program starting and
      oversight arriving. If it still says "Three strands", the build is stale.

## 5. Geography

- [ ] Nine cluster cards, each with people and entity counts. If you see only
      "Unclustered", the build is stale.
- [ ] The ranked **sites with coordinates** chart — 76 of 102 locations. Bars proportional,
      counts labelled, names clickable through to the map.
- [ ] The closing note about coordinates locating an installation and asserting nothing
      about what is inside it. That distinction is load-bearing.
- [ ] Clusters with more than 26 members show an *N more* line rather than truncating silently.

## 6. Case files

- [ ] 251 cards. Note scroll performance — there is no virtualisation.
- [ ] Collapsed face carries status stripe, name, affiliation, status badge, **tier badge**,
      date and the **three axis meters**.
- [ ] Expand a card: full narrative, records, sources, and **`Open on map`**.
- [ ] **`Open on map` was freezing.** Test it on several cards including a high-degree one.
      This is the single most important regression check in this document.
- [ ] `+` becomes `−` on expand.
- [ ] Sort controls.

## 7. Analysis

- [ ] Four computed pattern cards: strongest pair, custody concentration, denial density,
      evidence base. Each with a working `show →` that drives the map.
- [ ] **Institutional overlap chart** — the top row was literally `null` at 26. Confirm it is
      gone, that labels are readable rather than truncated to nothing, and that the table is
      not wider than its container.
- [ ] Every chart carries data labels.
- [ ] Anything below the chart that is still the parent board's furniture — log it.

## 8. The cover-up

- [ ] Header counts match the stats strip (172 denials).
- [ ] **Denial density** rows render as dot-leaders with clickable names — not as raw
      `<a href=...>` text. That was a real bug caused by an escaping helper.
- [ ] Denial cards: parties, date, label, note, claim-tier block, sources, `Open on map`.
- [ ] Cards with no source say so explicitly.
- [ ] The `Showing the 60 most recent of N` line appears and is accurate.
- [ ] Precedent section renders plainer than the denial cards — it is establishing that a
      mechanism has history, not making a claim about this program.

## 9. Search

- [ ] Empty state shows the first nine entities rather than nothing.
- [ ] Search a person, an institution, a document, an acronym (`AATIP`), and a partial word.
- [ ] Result rows: `class · label · meta`, class in its node colour.
- [ ] Click a result → dock opens.
- [ ] **Query and filter state belong in the URL.** Copy the URL mid-search, open it in a new
      tab, confirm the view is restored. This is specified in the design system and may not
      have survived the port.

## 10. Report

- [ ] Renders at all. It has had **no review** against the new data — assume it is wrong and
      look properly.

## 11. Keyboard and accessibility

- [ ] `/` focuses the analyst input. `1`–`8` switch views.
- [ ] Tab through the rail — is anything focusable that should not be, or vice versa?
- [ ] Set `prefers-reduced-motion` and reload: the ambient sweep, the missing pulse and the
      caret blink should stop; state transitions should shorten to ~100ms.

## 12. Data spot-checks — do at least five

Pick five claims at random from five different views and verify against the source. You are
checking two things: that the URL resolves, and that the claim says what the source says.

- [ ] Open five source links. Note any that 404 — `.mil` and `war.gov` links are known to be
      fragile and 130 were bot-blocked at verification time.
- [ ] Find a **Tier 1** claim and confirm a genuine primary record sits behind it.
- [ ] Find a **Tier 3** claim and confirm it states its reasoning rather than asserting.
- [ ] Confirm a **denial** edge names who denied it and when.
- [ ] Confirm no claim anywhere reads as if the board is asserting something it has not sourced.

**If a source is fabricated, stop and report immediately.** That is the one failure mode that
discredits the entire board, and it outranks every visual bug in this document.
