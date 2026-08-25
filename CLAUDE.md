# The Program — working instructions

**Read this before touching anything.** It is the authoritative entry point. Where any
other document in this repo disagrees with this file, this file wins and the other one is
stale — several of them are, and they are named in §8.

**Repo:** `Samizdat-Publications/the-legacy-program-dashboard` (private), branch `master`.
It is its own repository. `PROJECT.md` says it lives inside the-vanishing; that is no
longer true.

**Owner:** Stewart.

**Do not trust any figure in this file, or in any other document here.** Run
`python3 tools/state_snapshot.py --gate` — it derives every number from source and runs
the gate. The counts below are a sanity anchor, not a source of truth.

**Starting a fresh session?** Read `notes/HANDOFF-2026-08-25-claude-code.md` after this.

---

## 1. What this is

A research board mapping the alleged legacy UAP recovery and reverse-engineering
programme, 1944–2026. Single self-contained HTML file, no server, no runtime deps.

| | |
|---|---|
| nodes | 968 (279 people · 689 entities) |
| hand-written sourced edges | 2,160 |
| tiered claims | 4,431 — T1 2,596 · T2 1,342 · T3 493 |
| unique source URLs | 2,825 |
| timeline events | 858 |
| program map (L0) | 110 nodes, all with dossiers |
| built artifact | `dist/the-program.html`, 13.2 MB |

Regenerate these numbers rather than trusting them; they move every research pass:
`python3 tools/state_snapshot.py`.

---

## 2. THE ONE RULE THAT NEVER BENDS

**No invented sources, URLs, document numbers or quotes. Ever, anywhere, including in
mockup copy, placeholder text and example data.**

If you need a placeholder, mark it unmistakably as one. If you cannot verify a citation,
say so and leave it out. This rule has no exceptions and no "just for now" case.

Corollaries that have already cost real time:

- **AARO is not a neutral source.** Claims sourced to `aaro.mil` or `defense.gov` cap at
  **Tier 2** unless the claim is about *what they said*.
- **An image URL is a sourcing claim.** `data/l0-images.json` is empty on purpose. A record
  there asserts an image exists at a URL under a licence. That needs verification, not a
  plausible-looking guess.
- **Two agents agreeing is not corroboration when they share a method.** Two independent
  research passes both "corrected" a statutory citation that was already right, and the
  correction had to be reverted.

---

## 3. How to build and check

Run from the repo root. **Order matters** — later stages consume earlier output.

```
python3 tools/merge.py
python3 tools/regrade.py
python3 tools/merge.py
python3 tools/build_l0.py
python3 tools/build_design_extract.py
node    tools/build_l0_layout.mjs
python3 tools/build_dashboard.py
```

Then the gate:

```
python3 tools/state_snapshot.py --gate  # state + the whole gate below, in one command
python3 tools/verify.py                 # 36 checks
python3 tools/verify.py --self-test     # every check shown rejecting bad input
node    tools/capture_strip.js          # writes tools/runtime-strip.txt from a real DOM
python3 tools/audit_independent.py      # 38 checks, deliberately independent
node    tools/runtime_check.js          # 16 DOM assertions in a real browser
node    tools/test_scripted_analyst.mjs # 15 branch assertions
python3 tools/verify.py --idempotent    # slow: builds twice, requires identical output
```

The two `node` steps need the board served over HTTP -- `file://` does not work for a
13MB page. Run `node /opt/node22/lib/node_modules/http-server/bin/http-server dist -p 8899
--silent &` first, or point `BOARD_URL` at wherever you are serving it.

**Run `capture_strip.js` BEFORE `audit_independent.py`, every time.** Six of the audit's
checks compare the figures a reader actually sees against an independent re-derivation, and
they read those figures out of `tools/runtime-strip.txt`. That file is a capture, not a
source. A stale one makes the audit report a defect that is not there: on 25 August a
capture left over from a different build reported the duplicate collapse as two count
errors, and cost a handoff two findings that did not exist.

**All of these must be green before a push.** `--idempotent` is the one that catches a
whole class of bug: any pass that reads its own previous output back in.

### Where you are running

This project is worked on from three places and they are not interchangeable:

| | can build & test | can push | can **look** at the dashboard |
|---|---|---|---|
| **cloud session** (web) | yes | yes, via the GitHub connection | **no** |
| **local Claude Code** | yes | yes | yes |
| Stewart, by hand | yes | yes | yes |

**If you are a cloud session, you cannot see the rendered output.** That matters more here
than in most projects, because §5 below is a list of times a check said one thing and the
screen said another. Ship visual work, but **never report a visual property as verified**.
Say "built, gate green, unverified on screen" and hand Stewart the thing to look at. Writing
"confirmed the labels no longer overlap" when nothing rendered is the same failure as the
checks that passed while broken.

### Windows notes — for commands you hand Stewart, not for your own shell

A cloud session runs Linux and should use `python3` and forward slashes for itself.
This section applies only to commands written **for Stewart to paste**. He runs
**PowerShell 5.1**:

- `&&` is a **syntax error**. One command per line.
- Always include the `cd`, quoted, so the block is copy-pasteable:
  ```
  cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
  python tools\verify.py
  ```
- The interpreter may be `python`, not `python3`. Check once, then be consistent.
- The repo path contains **three spaces**. This has already broken a build script that used
  `new URL(...).pathname`, which percent-encodes them. Use `fileURLToPath`.

---

## 4. Working agreements with Stewart

- **Clamp responses.** What you did, why, what you need from him. Detail goes in a repo note,
  not in chat.
- **No em dashes** in prose written for him. Tables are preferred over long lists. Charts get
  data labels.
- **Adversarial review is opt-in.** When a deliverable is finished, ask *"Do you want to run
  adversarial review audit?"* and then **wait**. Do not run it unprompted; it burns context.
  When he says yes, act like his managers — hostile management reading it cold — and
  actually look at the output rather than reasoning about it.
- **He cannot read JSON.** When a JSON file needs his decision, render it as a table in chat
  and let him edit by line.
- **Never paste the GitHub token into chat.** It lives in `.gh-token`, gitignored.
- **Size must never encode importance** anywhere in the visual language. The largest node is
  AARO, which this board treats as implicated, not authoritative. Position is available;
  size is not.

---

## 5. The failure mode this repo keeps hitting

Stated four times in the notes in four different costumes. It is the single most useful
thing to internalise before working here:

> **A check that has never been shown to fail is indistinguishable from a broken one.**

Concrete instances, all real:

- `canvasInk` reported zero ink on a visibly drawing canvas and had never once fired.
- Six of six new verify checks were born broken and silently passing, because the poisoned
  fixture was built from a source that already contained the thing being tested for.
- A programmatic overflow test returned zero while the dossier panel visibly clipped every
  line at both edges — the panel fitted its element, and the element did not fit its grid
  track.
- The scripted-analyst test passed while **six of seven** suggestion chips routed to the
  wrong branch, because it asserted only that a long answer came back with valid commands.
  A check that cannot name the branch it expected cannot detect a wrong one.

**Therefore: every check you add must be demonstrated rejecting the input it must reject.**
`verify.py --self-test` enforces this and will flag any check that lacks a poison.

And its sibling rule: **reading the source is not verification.** Three times this session a
check agreed with the implementation and a screenshot disagreed. For anything visual, look
at it.

---

## 6. Two grading systems, and do not confuse them

They share three colours, which is a known weakness in the design.

- **Claim tiers 1-3 — evidence strength. 1 is strongest.** Ammunition grading. T1 documented,
  T2 a named person on the record, T3 stated inference. T3 is flagged by the file rather than
  by a critic, and is where research goes next.
- **Node tiers A/B/C — proximity to the programme.** Not credibility. A Tier A node carrying
  only T3 claims is not a contradiction; it is the definition of where to look next.

---

## 7. Where things are

```
data/the-program.json        6.9MB  the full board          } over GitHub's ~1MB
data/l0-model.json           5.7MB  map model + dossiers    } API read cap: they
dist/the-program.html         13MB  the built dashboard     } read as ABSENT
data/design-extract.json     285KB  purpose-built, readable — hand this to Design
data/l0-layout-model.json    461KB  Design's layout output
data/l0-highlights.json             14 editorial start-here flags, DRAFT
data/l0-images.json                 image register, plumbed and deliberately empty
research/dossiers/                  per-node research
research/_authority.json            12 offices, each naming its instrument
research/_removed.json              approved removals + alias map
tools/                              the pipeline and the gate
notes/                              every session's findings and mistakes
ref/the-vanishing-v2.html           the parent board. build_dashboard.py patches THIS.
```

**The 1MB read cap is trap #7 and it has bitten twice.** A tracked, pushed, present file
over 1MB reads as *absent* to anything using the GitHub API. When briefing Claude Design,
cite `data/design-extract.json` and never the big three.

---

## 8. Stale documents — do not trust these

Fixed on 24 August but listed so you know the pattern:

- `PROJECT.md` — said the repo lives inside the-vanishing. It does not.
- `README.md` — carried counts from an earlier research wave.
- `TESTING-CHECKLIST.md` — asserted the no-key analyst was "already working as designed".
  It was answering questions about a different project entirely.
- `SESSION-HANDOFF.md` — dated 13 August, written *into* the session that ended on the 24th.
  Superseded by this file plus `notes/ANALYST-NOKEY-2026-08-24.md`.
- `WAVE3_QUEUE.md`, `CLAUDE-DESIGN-PROMPT.md` — historical. Useful as record, not as
  instruction.

**General principle: this board was built by porting a shell from a sibling project. Assume
every inherited surface is answering about the wrong project until someone has read it.**
Two were found on 24 August by accident, while looking for something else.

---

## 9. What is next, in priority order

> **0. DONE, 25 August 2026.** `origin/claude/status-update-bewtdk` was merged into this
> line with Stewart's approval. `research/` did not conflict; both hand-edited tools
> auto-merged; every generated file was resolved by rebuilding. The two "genuine audit
> failures" the handoff reported were neither genuine nor failures -- both came from a
> stale `tools/runtime-strip.txt` captured off a different build. See
> `notes/AUDIT-STRIP-2026-08-25.md`. `tools/capture_strip.js` now generates that file.


1. ~~**The COVER-UP view still carries the sibling board's skeptical record.**~~ **DONE,
   25 August 2026.** Three inherited surfaces found and removed, only one of which was
   the COVER-UP view. See `notes/INHERITED-SURFACES-2026-08-25.md`. Two gate checks now
   guard the class: `every edge type has a caption written for this board` and
   `no parent-board editorial content ships`.

2. ~~**Sweep every remaining inherited surface.**~~ **DONE, 25 August 2026.** Done by
   construction rather than by grep: diffing prose string literals between
   `ref/the-vanishing-v2.html` and the built file showed 177 that survived the port
   verbatim. Five rendered as false copy, and the analyst system prompt was inherited
   whole -- including a HARD RULE naming the axes **S, P and I** when this board scores
   on **C, A and D**. All fixed; `notes/INHERITED-SURFACES-2026-08-25.md` has the list.
   Three gate checks guard the class now, the third being
   `the analyst system prompt describes this board`. **Re-run the literal diff after any
   change to `ref/`** -- it is four lines of Python and it found what six sessions of
   reading did not.

3. ~~**The last 23 unsourced edges are an ACCESS problem, not a research problem.**~~
   **DONE, 25 August 2026, and the diagnosis was wrong.** They were not an access
   problem. `norm_source()` in `merge.py` silently discarded any source written as a
   bare string, and 732 sources across `research/` went that way -- 236 unique URLs, 76
   of which reached the board by no other route. Several sat on exactly those 23 edges,
   so a previous pass recorded them as UNSOURCED and went hunting for citations that
   were already in the file. **All 2,159 edges now carry a source.**

   That fix then exposed something worse, and it is the reason to read
   `notes/EDGE-TIERS-2026-08-25.md` before touching tiers: `remediate_tiers()` walks
   people and entities, and **edges were never in it**. Edge `claimTier` was whatever
   the research authored, merged by `min()`, audited by nothing, while rendering to the
   reader as "Tier 1 - documented". 93 edges held that grade on a Wikipedia article, a
   YouTube video or a blogspot post. 91 are now Tier 2; two gained the real document.
   A self-tested gate check and `edge_tiers` in the golden manifest stop it recurring.

   **The access facts in `notes/SOURCING-2026-08-25.md` still hold and still matter.**
   `web.archive.org` is unreachable from this environment entirely, so the board's many
   Wayback URLs cannot be verified from here and the usual fallback for a 403 does not
   exist. `govinfo.gov`, `archive.org` (including `archive.org/details/DTIC_*`, the
   Defense Technical Information Center mirror), `theblackvault.com` and `irp.fas.org`
   all answer. `dia.mil` and `aaro.mil` refuse curl but serve WebFetch. The govinfo
   search API answers with `DEMO_KEY` and rate-limits after roughly a dozen queries.

4. **`data/l0-highlights.json` needs Stewart's sign-off.** 14 draft flags, each with a
   stated reason. Cap is 16, so there are 2 slots. **The table is built and waiting for
   him:** https://claude.ai/code/artifact/ecc7053d-63f5-4d6b-9de4-8e101048671e — all
   fourteen with their reasoning, tier, and node id, in reading order, with keep/cut
   marks he can set as he goes. His marks live in his browser only; he reads the summary
   line back and someone edits the JSON. Do not rebuild this table from scratch; if the
   flags change, republish that same artifact URL.
5. **Implement Design's packed-cell layout and edge budget** in `tools/l0_patches.py`.
   **Cost analysed and a comp built, 25 August:** `notes/PACKED-LAYOUT-COST-2026-08-25.md`.
   The model is finished and all nine of Design's checks guard it. The work left is a
   canvas rewrite of `mountL0` (421 lines, 80 `ctx.` calls) whose geometry assumes a
   point cloud. **See the comp before building:**
   https://claude.ai/code/artifact/afb7293f-6051-4686-b308-b68996f50ce9 — 110 chips,
   zero overlaps, measured. It answers whether position means something; it does not
   answer whether the canvas implementation will hold, and nothing in a cloud session
   can. Stewart's call.
   Design's response of 24 August confirms `mountL0` is ours end to end, so this is a direct
   build and not a patch against the parent renderer. Package in `notes/design-2026-08-24/`.
6. ~~**Add Design's nine checks** from §5 of their response, each self-tested.~~ **DONE,
   25 August 2026.** All nine, each demonstrated rejecting the exact input Design named
   in the "must reject" column. They assert against `data/l0-layout-model.json`, which
   is a build product on disk rather than something embedded in the page, so they get
   their own poison channel in `--self-test`: `_LAYOUT_OVERRIDE`, the same pattern as
   the analyst check's `BREAK=1`. Note the model is generated but **not yet rendered** -
   the checks guard the spec, and item 5 is still to build against it.
7. **The image sourcing pass** for `data/l0-images.json`. Federal works are the strongest
   candidates (17 U.S.C. 105) but must trace to a `.gov` original, not an aggregator.
   Witnesses default to the class letter — a private person who testified has not licensed
   their likeness.
8. **`notes/REQUEST-QUEUE.md`** — 35 logged actions, and the FOIA queue.
9. ~~**TESTING-CHECKLIST.md §12 source spot-checks**~~ **DONE for the mechanical half,
   25 August 2026.** `tools/spot_check.py` asserts that every claim quoting a phrase of
   four or more words has that phrase in the document it cites -- 604 claims qualify.
   **No fabricated source was found.** 278 of the 283 adjudicable claims quote their
   source correctly; five real citation defects were found and fixed and eight rotted
   `gov.br` URLs repointed. `notes/SPOT-CHECK-2026-08-25.md`.
   **The aaro.mil block is now done too:** all 24 quotes against the FY2025 and FY2023
   annual reports and HRR Volume I verify, fetched with WebFetch and adjudicated
   mechanically via `tools/spot_cache_put.py`. Two misquotes were found there and fixed,
   one of which mattered -- AAWSAP's purpose was quoted as assessing "long-range
   aerospace threats" where the HRR says "long-term and over-the-horizon foreign
   advanced aerospace threats".

   **What is left is item 10.** The tool is deliberately not in the build gate -- it
   depends on the network, and a check that fails because a host is throttling is a
   check people learn to ignore.

10. ~~**181 claims cite a DIA reading-room URL that no longer resolves.**~~ **43 of 46
    REPAIRED, 25 August 2026.** DIA renumbered its reading room and the old
    `FileId/1700xx/` ids now render the INDEX rather than a document -- `FileId/999999999/`
    returns the same page, so DIA falls back silently and a stale citation looks live.
    Every repair was verified by opening the document and reading its own title page,
    document number and page count, never by trusting a listing.

    **Three are deliberately still on the dead id and should stay there until someone
    can settle them:** `170051` (its quote is the header common to all four Contract
    Status Briefs), `170052` (its quote appears in two of them), and `170018` (carries
    no quoted claim to match on). Guessing between near-identical briefs would put a
    citation on the board that nobody could re-derive.

    `tools/spot_cache_put.py` is the tool for this: it puts a WebFetch-obtained file
    into `spot_check.py`'s cache so verification stays a substring test rather than a
    model's opinion. See `notes/SPOT-CHECK-2026-08-25.md`.
