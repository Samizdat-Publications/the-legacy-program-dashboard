# Handoff, 19 September 2026, late (THE CURRENT ONE)

Supersedes `notes/HANDOFF-2026-09-19.md` and its UPDATE block entirely. One continuous
Opus 5 session from the evening of 18 September through the night of 19 September.

`git fetch --all` first. Then read section 2, then section 6.

---

## 1. What is where

**Master is `c1af3a8`: green, pushed, deployed.** Board 1,125 nodes, L0 135.

**The nuclear cluster is NOT on master.** It is on branch `nuclear-2026-09-19` at
`359958f`, pushed to origin, and it is complete and good work: 19 people, 29 entities, 77
edges, 192 claims, four L0 dossiers, the Mansmann fix. It takes the board to 1,159 nodes.

**It is off master because it turns `test_packed_layout` red**, at class-ink chips 30
against cells 18, needing 36 < 30. Cell ink rose from 12 to 18 because the cluster's base
hubs and `strategic-air-command` opened new band-and-class cells: L0 now occupies 28 of
them. **This is exactly the first-of-kind cost that `notes/PACKED-LAYOUT-INK-2026-09-19.md`
predicted would recur, and it recurred within one build.** Nothing in the cluster is wrong;
the map cannot currently carry a new kind of object.

**Do not "fix" this by trimming the nuclear cluster.** The base hubs are the structure that
makes the register answer Stewart's question, and shaping research to fit a display measure
is backwards. This is Design's item 2 (section 7) and it is now blocking real work rather
than being theoretical.

Board across the whole run: 1,057 to 1,125 on master, 1,159 with the nuclear branch. Edges
2,460 to 2,738, timeline 913 to 1,067, Tier 3 claims 514 to 613, Tier A 172, denials 226.

| built | what |
|---|---|
| **The centrality fix** | `witness-chain` out of `PROGRAM_EDGES`. Claim-tier weighting measured and REJECTED |
| **ARV cluster, re-graded** | Graded once under the new rule instead of twice under two |
| **Congressional witnesses** | The 17 May 2022 House Intelligence hearing, which the board was missing entirely, plus both its witnesses |
| **TR-3B** | Hub, with the Library of Congress cataloguing Fouche's book as science fiction |
| **Lazar / S-4** | Hub, anchored on the 1991 Huff tape and the 1990 court record |
| **Disclosure Project** | 68 witnesses graded against the one document that anchors them |
| **Propulsion strand** | Four documents opened, each saying less than is claimed for it |
| **Dulce / Bennewitz** | Castello as a confessed fabrication |
| **Nuclear witnesses** | 47-name register, seven base hubs, the 1975 documentary seam. **ON BRANCH `nuclear-2026-09-19`, NOT master. See section 1** |
| **The notability triage rule** | CLAUDE.md section 2a |
| **The L0 budget** | `build_l0.py`, with `audit_independent.py` taught to match |
| **Two video triages** | Gerb's 80-year timeline and the Michels Ellsworth episode |

Canon passes 1, 2, 3 and 4 are built AND ON MASTER. Pass 5, nuclear, is built and on its
own branch, blocked by the map. Passes 6 to 15 remain.

**TO RESTORE PASS 5 once Design answers:** `git merge nuclear-2026-09-19`.

---

## 2. THE FIRST THING THE NEXT SESSION SHOULD DO

**Audit `tier` and the C/A/D axes for silent overwrite.** Section 6a explains the defect.
The `cluster` version of it moved sixteen nodes to the wrong map band and nothing caught
it. `tier` and the axes run the identical code path and have NOT been checked.

The method that found it: build the board, then diff it against the last known-good commit
looking for fields that moved without any build intending to move them.

```
git show <good-commit>:data/the-program.json > /tmp/old.json
# then compare field by field for entities present in both
```

---

## 3. Stewart's standing instructions, as given this run

- **19 September, on scope:** "this is literally the most secret program since the
  Manhattan project... we have to find a way to document even loose evidence like
  testimonies just to make sure we are documenting the programs history, including claims
  made about it." Adopted as CLAUDE.md section 2a. **Admission widened; grading untouched.**
- **19 September, on the map:** it "is mostly a cool visual at this point but with how
  dense this will eventually get I feel like we'll have to rethink it at some point
  anyways. Perhaps there is a better way to display or group it." The L0 budget is a
  STOPGAP and `build_l0.py` says so in its own comment.
- **Standing since 18 September:** full authority on research and tier decisions. Decide,
  record the reasoning in a note, tell him after.

---

## 4. Decisions taken in his absence, all recorded in the repo

| decision | where |
|---|---|
| Lever 2 only for centrality; claim-tier weighting rejected on measurement | `notes/CENTRALITY-2026-09-18.md` |
| Denial weighting measured and NOT changed; the obvious fix drops 8 documented nodes | `notes/DENIAL-WEIGHT-2026-09-19.md` |
| Rarity pin re-pinned deliberately, with a caution against doing it again on a 2-count margin | `tools/build_l0_layout.mjs` comment |
| Notability adopted as a second admission criterion | `notes/TRIAGE-RULE-2026-09-19.md`, CLAUDE.md 2a |
| L0 becomes a budget of 135, highlights by right | `tools/build_l0.py` comment |
| Ryan Graves held at Tier B, with his argument recorded | `notes/CENTRALITY-2026-09-18.md` section 5 |
| Jason Sands built despite thin sourcing, for defensive value | commit `7a1c6df` |
| Michael Johnson built with the cold-call prompt recorded, not smoothed | nuclear cluster |

---

## 5. THE LESSONS. This is the section that matters most

### 5a. Mechanism defects found, NOT fully fixed

1. **`_corrections.json` silently no-ops.** It loads at position 1 of 104 and filters the
   claims accumulated SO FAR. Any entity declared later, which is nearly every entity, is
   never touched. The Mansmann correction was written correctly, merged correctly, and did
   nothing. Fixed at source instead. **Corrections have presumably been failing quietly
   for a long time; someone should audit which ones ever took effect.**
2. **A thin entity enrichment overwrites `cluster` with a default.** `merge.py` builds a
   complete record from every entry and `merge_entity` only fills a falsy field, and
   `"other"` is truthy, so the alphabetically first file wins. Sixteen nodes were moved to
   the wrong band before it was caught by accident. **`tier` and the axes are unaudited.**
3. **The L0 budget caps node count but not label width.** C5 headroom at 1920 fell from
   56px to 20px on the nuclear build with L0 unchanged at 135, because rows depend on both.
   The budget is a partial control and is roughly one row from red.

### 5b. Process lessons that cost real time

| | |
|---|---|
| **`state_snapshot.py --gate` is NOT the gate** | CI's `app` job runs C1-C21 separately, from `app/`: `npm run build`, `npx vite preview --port 4173 --strictPort`, `npm run check`, `npm run check:poison`. Skipping them put a red commit on master |
| **`capture_strip.js` runs immediately before `audit_independent.py`, every time** | Running the audit alone reports six stale-strip failures that are not real |
| **Never merge a branch's own reverted history back into it** | `git merge master` fast-forwarded and re-applied the revert, deleting all seven research files. Recovered only because the branch was already pushed. Revert the revert on the target instead |
| **Denial metadata cannot be set from a research file** | `denialKind` and `denier` come from `data/denial-adjudication.json`, keyed `a|b`. Writing them into an edge is inert |
| **An independent check must stay independent** | `audit_independent.py` caught the L0 budget immediately. The fix is to RESTATE the rule there, never to import it |

### 5c. Three conclusions I stated too confidently and had to correct

These are in the repo as corrections rather than only here, because the wrong versions were
written into notes other people would act on.

1. **"You cannot reach the layout threshold by building more."** Wrong. Building more fixed
   it. Cell ink FELL from 16 to 12; I had read three flat chip-ink points as saturation.
   Two flat points are not saturation.
2. **"`runtime_check` is not really a flake."** Wrong. I had three consecutive failures and
   generalised. It passed, then failed again. It is intermittent.
3. **"L0 held at 137, so `arv-fluxliner` survives."** That was L0 on master, which carries
   no ARV nodes. The conclusion was right and the evidence for it was worthless.

**The pattern in all three is the same: a confident generalisation from two or three data
points.** The measurements were fine every time. The inferences from them were not.

---

## 6. Where the research stands

### 6a. The strongest material found

- **26 of 47 nuclear-facility witnesses reached the record through contemporaneous official
  paper**, not through any interview programme. This is the one seam in the subject that is
  documented rather than attested, and it is an explicit claim on `d-nuclear`.
- **The Library of Congress catalogues Fouche's *Alien Rapture* as "Science fiction."**
- **Thomas Castello is a confessed fabrication**, with the fabricator describing mailing a
  hundred identical packets to manufacture apparent corroboration.
- **DIA's own antigravity survey never mentions Thomas Townsend Brown.**
- **The JAL 1628 case has a 1,500-page NARA file owing Greer nothing**, while Callahan's
  claimed title rests on a form he supplied himself.

### 6b. Circular reporting, now documented from both directions

Deliberate: Levesque's hundred packets. Structural and unintended: the Disclosure Project's
68 testimonies all collected by one interviewer who cross-references his own witnesses in
editorial notes. Under the old triage rule this was theoretical. Under section 2a it is
load-bearing, which is why every node admitted on notability must record how the claim
reached us.

### 6c. Next research, in order

1. The `tier`/axes audit (section 2).
2. Canon passes 6 to 15.
3. The Gerb triage's ~100 absent candidates, especially **the National Security Council,
   which the board has no node for**, and the EO/statute spine: NSC 10/2, EO 10501, NSC
   5412, AEA 1954, NSAM 303, EO 11652, EO 12036, EO 12356, NSDD 159. All public primary
   documents and the cheapest documented gap available.
4. The denial weighting, with the 22 remaining unclassified edges classified first.
5. Retire the old shell. Kills the `runtime_check` flake.
6. Tier option C.

### 6d. Open documents that would move things most

- **Col. Frederick Meiwald's letter to Salas, 1 October 1996.** Two incompatible
  characterisations circulate. Highest-value unopened document in the nuclear cluster.
- "Report of Engineering Investigation of Echo Flight Incident, 16 Mar 67", 23 March 1967.
- Michael Johnson's DD-214 or OMPF, and the Article 15 record.
- The remaining ~449 pages of the OASD FOIA compilation behind the NORAD log.
- The Air Force history of the Office of the Administrative Assistant to the Secretary,
  its SAF/AA section, from the Gerb triage at `[01:21:12]`.

---

## 7. Design's queue, and it is now three items

1. **`fitChipInk`**, `notes/PACKED-LAYOUT-INK-2026-09-19.md`, with a correction block at
   its top because its original conclusion was wrong.
2. **The map at density.** Stewart's own view is that it needs rethinking. The budget is a
   stopgap and label width is uncontrolled.
3. **L0 and the hub rule.** `arv-fluxliner` and `tr-3b` are on the map; `s-4-papoose-lake`
   and `dulce-base` are not. Two of five hubs built under the rule reach the top-level map,
   so the convergence the rule exists to show is invisible for three clusters.
