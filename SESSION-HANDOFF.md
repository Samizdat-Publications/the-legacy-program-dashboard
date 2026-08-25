# Session handoff — The Program

> **`CLAUDE.md` is the authoritative entry point.** It carries the build order, the gate,
> the constraints and the priority queue, and it is maintained. Read it first. This file is
> the narrative handoff that goes with it: why things are the way they are, and what bit
> previous sessions. Where the two disagree about a number, `CLAUDE.md` wins — and better
> still, trust neither and run `python3 tools/state_snapshot.py --gate`, which derives
> everything from source.

**Updated 25 August 2026**, on the merge of `claude/status-update-bewtdk` into `master`.
Supersedes the handoffs of 13 and 23 August, both preserved in git history. The 12 August
cloud-session handoff is at `notes/SESSION-HANDOFF-2026-08-12-cloud.md`. Counts in all
three are stale; ignore them.

---

## Repo

**https://github.com/Samizdat-Publications/the-legacy-program-dashboard** (private)

Work sits on `claude/status-update-bewtdk`, open as draft PR #1 against `master`. On
25 August 2026 `master` was merged into it, bringing the L0 program map, both of Design's
layout rounds, the no-key analyst rewrite and `tools/audit_independent.py` alongside this
branch's sourcing and reference-integrity work. `research/` did not conflict at all; the
generated files were resolved by rebuilding, never by picking a side.

**GitHub write access is solved and is no longer job zero.** The 13 August handoff opened with
a long section on getting it; that was a Cowork-session limitation. This repo is now worked
from a remote Claude Code session which has the GitHub MCP tools and a working git remote.
Commit, push and PR all work directly. Stewart does not need to run git commands.

---

## Current state

**278 people · 678 entities · 2,159 edges · 4,443 claims · 858 timeline events ·
110 L0 nodes, every one with a dossier · unattached 0 · 1,178 distinct source URLs.**

Claim tiers: T1 2,713 · T2 1,236 · T3 494. Entity tiers: A 142 · B 335 · C 479.

The gate is **21 checks, every one self-tested against input it must reject**, plus a golden
manifest as a drift tripwire. There is now also a **runtime check**, which is new and which
you should run.

---

## Editorial stance — read before writing anything

Built from the premise that a legacy recovery and reverse-engineering program exists and has
been concealed. The question is not *whether* but **who, where, under what authority, and
paid for how.** No balanced both-sides prose. No skeptical disclaimers.

**AARO is not a neutral authority.** Claims sourced to aaro.mil or defense.gov cap at Tier 2
unless the claim is *about what they said* — publishing a document makes it a primary record
**of the statement**, not of the fact asserted.

That exemption is wider than it was. It used to recognise speech verbs only, so a claim about
what a document *lists*, *contains*, *reads* or *publishes* was demoted anyway. 47 claims were
caught that way, including that HRR Volume I contains zero occurrences of the name 'Wilson'
across all 63 pages. A full-text negative finding about a document, sourced to that document,
is exactly what Tier 1 is for.

**Never bends: no invented sources, URLs, document numbers or quotes.** And a corollary
learned on 22 August: **do not widen a check until it accepts your own prose.** A claim of
mine was demoted because I had written "the Department issues releases under his name" and
the attribution vocabulary has no "issues". The fix was to rephrase the claim as the
attribution it actually is, not to loosen the rule for one sentence.

---

## Two gates, and why there are two

```bash
python3 tools/verify.py --self-test    # every check must prove it can fail
python3 tools/verify.py --idempotent   # full pipeline twice, identical output
```

`verify.py` asserts properties of the **data**. Both rules still hold and must be kept: every
check asserts a fact and exits non-zero when it is false, and every check is itself tested
against input it must reject.

```bash
node /opt/node22/lib/node_modules/http-server/bin/http-server dist -p 8899 --silent &
node tools/runtime_check.js
```

`tools/runtime_check.js` asserts what the **browser renders**, and it exists because on this
board the two came apart badly. All eleven sequence chains rendered the word "undefined"
under an undefined date — on Grusch, Elizondo, Davis, Puthoff, Marcel — while every count in
the gate was correct and nothing threw. Fifty-four affiliations printed raw slugs like
`dod-sapco` where an institution's name belonged. **Neither defect is visible to a check that
reads JSON.**

Two things about it worth knowing before you edit it:

- The board is wrapped in an **IIFE**, so `NODES`, `CMD`, `chainHtml` and `tabDossier` are
  module-private and cannot be reached from `page.evaluate`. That is correct design. Every
  assertion goes through the DOM and through real clicks, which is what a reader gets.
- **`file://` does not work.** A 13 MB document served over `file://` never finished parsing
  in this container. Serve it over HTTP.

Chromium is pre-installed at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` and
Playwright is global at `/opt/node22/lib/node_modules/playwright`. Do not run
`playwright install`. The 13 August handoff's `/tmp` recipe is obsolete.

**Headless fps here is measured under SwiftShader and is NOT a proxy for Stewart's machine.**
Never quote a headless fps number to him as if it were his.

---

## Rebuilding

```bash
python3 tools/merge.py            # research/*.json -> data/*
python3 tools/regrade.py          # tiers, dates, coords -> research/_remediation.json
python3 tools/merge.py            # re-merge so the overlay lands
python3 tools/build_l0.py         # the L0 model and its baked layout
python3 tools/build_dashboard.py  # data + parent board -> dist/the-program.html
python3 tools/verify.py --idempotent
```

`build_l0.py` **must run before** `build_dashboard.py`, and it is easy to forget: the L0
checks fail loudly if you do, which is the gate working. `build_dashboard.py` prints
`all patches applied` or names failures. **Never ship a build that printed a failure.**

`ref/the-vanishing-v2.html` is a **build input and is never edited.** All divergence lives in
`tools/build_dashboard.py` as named patches.

---

## What the 22-23 August session established

Full detail in PR #1 and in `notes/`. The load-bearing findings:

**Removal was never total.** `verify.py`'s dangling check walked edge endpoints and
`timeline.node` and nothing else, so when 30 locations were removed the fix dropped their
edges — because that is what the gate checked — and left 31 `person.locId` back-references
pointing at nodes that no longer existed. `deriveEdges()` turns every `locId` into a live edge,
so the board emitted 31 edges to nodes that were not on it. **Satisfying the gate had defined
the scope of the fix.** Removal now sweeps `locId`, `instId` and `domains`, and re-points
edges through the alias map — which recovered **27 edges the August collapses had silently
deleted**.

**Duplicate nodes.** The FY2024 NDAA sec. 1687 was on the board three times, the AARO FY2025
annual report three times, Jesse Marcel Sr. twice at two different tiers. Nine groups, 19
nodes. All collapsed with the losers' evidence carried onto the survivors first. Detection is
now a gate check; the six genuine non-duplicates live in `tools/DUPLICATES_ACCEPTED.json`
with a reason each.

**The dossiers said eight.** "12 seats, not 8" was established in August and stripped from the
board's node claims. The dossiers are a **parallel dataset** loaded separately and never got
the correction — 33 strings across seven files, including Tier 1 claims sourced to the very
statute that contradicts them. 10 U.S.C. 119(g) names six bodies; chairman plus ranking of six
is twelve. **When you correct a fact, grep `research/dossiers/` too.**

**Three independent narrowings of oversight**, each in a different instrument, none depending
on the others: congressional readership to twelve under 10 U.S.C. 119(e); ISOO access reducible
to **the Director alone** under EO 13526 sec. 4.3(b)(3); DCSA industrial-security oversight
removed entirely under **32 CFR 117.6(b)(3)** — which is codified regulation at 85 FR 83312,
not merely DoD policy, and the board did not have it. Closing any one leaves the other two.

---

## What is reachable from a session like this

Established by probing all 1,198 source URLs; see `notes/LINK-HEALTH-2026-08-22.md`.

| | |
|---|---|
| **Answer** | uscode.house.gov · govinfo.gov · archives.gov · federalregister.gov · senate.gov · oversight.house.gov · docs.house.gov · war.gov · history.defense.gov · theblackvault.com · gao.gov · sec.gov |
| **Refuse** | dia.mil · esd.whs.mil · dni.gov · congress.gov · bioguide.congress.gov · **web.archive.org** (blocked outright) |
| **Rate-limited, not blocked** | ecfr.gov — go slowly; the renderer API at `/api/renderer/v1/content/enhanced/...` is the reliable route for a whole CFR part |

Two cautions, both learned by getting them wrong first:

- **A status code from one client at one moment is evidence about that request, not about the
  document.** `gao.gov` and `war.gov` both returned 403 to curl while serving WebFetch in the
  same session.
- The sweep followed redirects, so 9 URLs that land on bot-block pages counted as reachable.
  The verified figure is **754 of 1,198**, and the rest are **unconfirmed, not dead**.

One genuine failure: `irp.fas.org/dia/aatip-list.pdf`, the DIA's January 2018 list and the
most-cited single URL behind the DIRD nodes, returns HTTP 202 with an empty body, and its
Wayback capture recorded the same 202. Use `https://fas.org/publication/aatip-list/`, which
works, and The Black Vault for the DIRDs themselves.

---

## Outstanding, in priority order

1. **340 unsourced edges, 25 unnoted.** 15 of the 340 are unsourced *twins* of edges that are
   already sourced — same node pair, two types, one Tier 1 and noted, one Tier 3 and bare
   (`unsourced_edge_with_sourced_twin` in INTEGRITY). Those are redundancy, not missing
   research, and are candidates for collapsing rather than sourcing. The genuine gap is ~325.
   Most of the remainder need `dni.gov` (ICD 906, CAPCO) or `esd.whs.mil` (the DoDD 5205.07
   pair), or are narrative rather than statutory (the AAWSAP/BAASS/Reid cluster).
2. **33 thinly-sourced people.** Blocked on retrieval, not effort: the natural second source
   is a member biography or the Congressional Directory, and `congress.gov`,
   `bioguide.congress.gov` and `web.archive.org` all refuse. **A source is never added unless
   it was opened.**
3. **Cross-board parity with The Vanishing.** Stewart wants the shared figures researched once,
   not twice. The design that works: **share id, narrative, claims, sources and chronology;
   keep tier, axes, cluster and sub board-local.** Tier is a rank within a population and the
   axes differ — C/A/D here against S/P/I there — so Grusch being Tier A on this board and not
   on that one is correct, not a conflict. **Blocked:** the only Vanishing available here is
   `ref/the-vanishing-v2.html`, a frozen 15-person copy that uses `mccasland` where this board
   uses `william-mccasland`. Align the id conventions first, as a separate small change, and
   that needs the live board.
4. **Defer the dossier payload** — roughly 6.6 MB parsed as JS object literals at load. Lower
   value now that load is fast.
5. **`notes/WANTS.md`** — craft-morphology schematics. Parked.
6. `TESTING-CHECKLIST.md` §0 still asserts pre-collapse counts and will fail its own check.

---

## Things that have already cost a full build cycle

- **There are two map implementations in the file.** The legacy one is dead at runtime. A
  patch raising the layout step count was applied to the *wrong* one, and reading the source
  did not reveal it — **the profiler did.** If you change map behaviour, verify at runtime.
- **The layout is baked at build time** by `tools/precompute_layout.py`. If you change the
  physics or anchors the bake picks it up, but check the wall-clamp figure stays near **3.6%**.
- **Measure before optimising, and measure before believing a comment.**
- **An edge key is `(a, b, type)`.** Writing an edge with a different `type` from the one you
  meant to source creates a SECOND edge instead of sourcing the existing one. That is also how
  98 node pairs ended up joined by more than one edge.

---

## Working rules

- **Adversarial review is opt-in.** At the end of a deliverable that feels final, ask Stewart:
  *"Do you want to run adversarial review audit?"* Do not run it unprompted.
- **Research agents write to `research/`.** Build tooling lives in `tools/` deliberately.
- **Stewart's stated preferences:** concise and direct, no em dashes, tables over prose for
  comparisons, complete code rather than fragments.
- A collapse or removal needs Stewart's approval and is recorded in `research/_removed.json`
  under `_approved_by`. He approved the nine of 22 August and delegated the choice of survivor.
