# Silent defaults, and a fade that never ended. 19 September 2026

Answers item 2 of `notes/HANDOFF-2026-09-19-LATE.md`, "the first thing the next session
should do": audit `tier` and the C/A/D axes for the silent-overwrite defect that had
already moved sixteen nodes through `cluster`.

Short version, and the second line is the one nobody was looking for.

| | |
|---|---|
| **`tier` and the axes are NOT affected** | and they never could have been. Measured, not argued. Section 2 |
| **Person `status` IS affected, and nobody knew** | 24 people shipped as `active` while a research file said otherwise. Harry Reid, Gerald Ford, Kenneth Arnold, Nathan Twining and Edward Condon were all on the board as `active` and all authored `dead`. Section 3 |
| **`cluster` was worse than recorded** | 267 nodes, not the sixteen found by accident on 19 September. Section 3 |
| **`runtime_check` is not a flake** | it is a fade that never terminates, at a rate that is per frame rather than per second. Three sessions have now called this intermittent. Section 6 |
| **`_corrections.json` is healthy** | 53 of 53 field corrections took. The handoff's diagnosis of it was wrong in both halves. Section 7 |

---

## 1. The defect class, stated once

`tools/merge.py` builds a COMPLETE record from every research entry, defaulting anything
the entry omits, and then merges records for the same id. Different fields merge by
different rules, and only one of those rules is order-dependent:

| rule | fields | order matters? |
|---|---|---|
| fill-if-falsy, so the FIRST truthy value wins | person: `loc locId instId sub cluster status date age photoCredit unexplainedResidual`; entity: `cluster sub dateStart dateEnd` | **YES** |
| strongest wins | `tier` | no |
| max | `C` `A` `D` | no |
| longest wins | `desc` `narrative` `tierRationale` | no |

A fill-if-falsy field is safe **only while its absent-value is falsy**. Where the default
is truthy, the record arrives already holding a value that is indistinguishable from an
authored one, the merge therefore never fills it, and the first file to so much as mention
the node has decided the field for good. Research files load alphabetically.

Two fields had a truthy default. Both were wrong on the shipped board.

---

## 2. `tier` and the axes: not affected, and here is the measurement

The handoff's expectation was that `tier` and the axes "run the identical code path". They
are defaulted by the identical code path and they are **merged by a different one**, which
is the half that decides it:

- `tier` defaults to `"C"`, the WEAKEST value, and `_merge_common` takes the STRONGEST.
  A thin entry can only ever lose.
- `C`/`A`/`D` default to `0` via `clamp_axis`, and `_merge_common` takes the `max`.
  A thin entry can only ever lose.

Neither is order-dependent, so neither can be pinned by load order. That is an argument,
so it was checked against the board: the pipeline was rebuilt with the fix in section 4 and
the result diffed field by field against the pre-fix board.

| field | nodes moved |
|---|---|
| `tier` | **0** |
| `C`, `A`, `D` | **0** |
| `cluster` | 267 |
| person `status` | 24 |

Nodes, edges and timeline counts were byte-identical either side: 338 people, 787
entities, 2,661 edges, 1,050 timeline rows. `GOLDEN.json` does not move.

**The audit is closed. Do not re-open it without a new mechanism**, and note that the
question was worth asking even though the answer was no: it is what found `status`.

---

## 3. What is actually affected

### 3a. Person `status`, which was not on anyone's list

`"status": p.get("status") or "active"`. The board is a register of people who have died
or disappeared, and `status` is the field that says which. It had no validation of any
kind: eight distinct values are in use, including `dead` (57) beside `deceased` (4), and
`active` (222) beside `alive` (10).

24 people shipped as `active` while another research file authored something else. The
unambiguous ones, where no file said `active` at all:

| authored `dead` | andre-lebeau, carroll-bolender, daniel-inouye, edward-condon, gerald-ford, harry-reid, jim-ragsdale, john-lear, kenneth-arnold, lincoln-lapaz, nathan-twining, paul-bennewitz, stanton-friedman |
|---|---|
| **authored `former`** | avril-haines, david-norquist, garry-reid, jay-stratton, kathleen-hicks, marco-rubio, sean-kirkpatrick, susan-gough, tim-phillips, william-l-moore |
| **authored `resolved`** | gerald-anderson |

Four more (dylan-borland, jeffrey-nuccetelli, kirk-mcconnell, luis-elizondo) had files
disagreeing with each other, `active` among them, and correctly did not move; they are a
research question, not a mechanism one.

**How visible was it.** Latent, not on screen. The production shell carries `status` in
`nodes.json` and renders it nowhere; the retired shell drew it as a DEC/MIS/CLD badge and
is deployed nowhere. But it is in the data the analyst reads in the reader's browser, so
the board would have answered "active" for Gerald Ford if asked.

### 3b. `cluster`, which is 267 nodes rather than sixteen

`"cluster": e.get("cluster") if e.get("cluster") in VALID_CLUSTER else "other"`. Two
defects in one expression: `"other"` is both the default AND a real band, and an
out-of-vocabulary value is coerced to it in silence.

The coercion is the bigger half. **132 entries across the research files carry a `cluster`
value that is not a band at all**: `aaro`, `aawsap-dird`, `science`, `legislation`,
`registry`, `mechanism`. The `_rs-*` source-set files use `cluster` as their own
provenance tag. Those files begin with an underscore, so they sort FIRST, so their tag
became `"other"` and pinned it before any file with a real band was read.

`aaro` is the clean example: `_rs-aaro-reports` tagged it `"aaro"`, which became `"other"`,
and `aawsap-aatip` (`oversight`), `releases-2023-2026` (`ic`) and `uaptf-aaro` (`ic`) all
lost to a file that was not expressing an opinion about the map.

This is the 208-entity figure in the older memory note, now measured properly at 267 and
fixed rather than recorded.

---

## 4. The fix, in `tools/merge.py`

Default LATE, once, after every file has been read, so load order cannot reach the
decision.

| change | |
|---|---|
| `_valid_cluster()` | returns the band, or `None` when absent, and RECORDS out-of-vocabulary values instead of coercing them silently |
| `"status": p.get("status") or None` | absence is absence |
| `finalise_defaults(people, entities)` | runs immediately before `load()` returns. Fills `cluster` to `"other"` and person `status` to `"active"`, and enforces the band vocabulary on values an overlay set directly, which `_valid_cluster` never sees |

Nothing else in `merge.py` reads either field during the load loop, so there is no window
in which `None` is observable. Everything downstream sees a string, as before.

The build prints what it did: `defaults applied after merge: cluster=N status=N coerced=N`,
and names the out-of-vocabulary values.

---

## 5. The check that would have caught it

Added to `tools/audit_independent.py`, which is Layer 1 and deliberately imports nothing
from the build. Following the handoff's own lesson, the rule is **RESTATED there, not
imported**: the check re-reads `research/*.json` itself and asks one question of the
shipped board. Does any node carry the default for `cluster` or `status` while a research
file authored a real value for it?

It is poisoned rather than trusted. Forcing `aaro.cluster` back to `other` and
`harry-reid.status` back to `active` in the board makes it fail and name both nodes:

```
FAIL  no authored cluster or status was lost to a default:
      ["aaro.cluster ships 'other', authored ['ic', 'oversight']",
       "harry-reid.status ships 'active', authored ['dead']"]
```

Layer 1 is now 41 checks.

---

## 6. `runtime_check` is not a flake. It is an animation with no last frame

The data fix turned `runtime_check` red, on `the network map is still at rest :: went quiet
and then started moving again`. Six runs, six failures, so the documented flake was not the
explanation. The same commit's shell on the same port passed three of three.

**What it actually is.** The inherited renderer eases the camera and every node's alpha
with `v += (target - v) * 0.12`, once per frame, with no snap. That is two defects:

| | |
|---|---|
| **It never arrives** | the gap shrinks by 12 per cent a frame and reaches zero at no frame at all. "At rest" was an asymptote, and the map only LOOKED still once the residual fell under one quantisation step of the canvas |
| **Its duration is frame rate** | 0.12 a frame is the half-second fade Design specified, at 60fps. The gate's swiftshader browser draws this 18MB page at about **11fps**, where the identical constant takes **four seconds**. Nobody chose a four-second fade |

Measured on the gate's own browser, after a select-then-clear: the node alphas were still
moving 4.8 seconds later, decaying by ever smaller amounts and never arriving. The check
samples at about 2.1s. So whether it passed depended on how much total fade the board
happened to have and how fast the frames happened to be, which is exactly the shape of an
intermittent failure that never reproduces on demand.

**The data change did not cause it.** It moved 267 nodes, so more nodes had a new alpha
target, so more residual was left at 2.1s. It made a standing defect visible.

**The fix**, `tools/network_patches.py` change 12: rescale the rate by elapsed time against
the 60fps frame the constant was written for, and snap when the remaining gap cannot be
seen. The epsilons are chosen so the snap is invisible by construction, not for
convenience: `1/255` for alpha is one step of the 8-bit alpha channel, `1e-4` for `cam.k`
is under 0.14px of travel at the far edge of a 1,368px canvas, `0.02` for `cam.x/y` is a
fiftieth of a CSS pixel. It changes when the motion stops and nothing about how it looks.

| | before | after |
|---|---|---|
| fade complete | never; still moving at 4.8s | 800ms, then exactly at rest |
| `runtime_check` on this board | 0 of 6 | **5 of 5** |

This retires section 5c item 2 of the late handoff. `runtime_check` was intermittent, the
session that called it a flake was right about the symptom, and the cause was not in the
check.

---

## 7. `_corrections.json` is healthy, and the handoff's diagnosis of it was wrong

Section 5a item 1 recorded that corrections "silently no-op", that the file "loads at
position 1 of 104 and filters the claims accumulated SO FAR", and that someone should audit
which ones ever took effect. Both halves check out false.

**The load order.** `rank = lambda f: (3 if "_corrections" in f else ...)` sorts ascending,
so `_corrections.json` loads **103rd of 103**, dead last, after `_remediation`. That lambda
is unchanged since the initial import. What loads first is the ten OTHER underscore files
(`_authority`, `_rs-*` and friends), which rank 0 and sort ahead of everything on the
underscore alone. That is a real hazard, and it is the one in section 3b, but it is not
this file.

**The efficacy audit, which is what was actually asked for.** Every field a correction
sets, checked against the shipped board:

| | |
|---|---|
| field corrections that took | **53 of 53** |
| field corrections that did not | 0 |
| `removeClaims` rules honoured | 1 of 1 |

Two entries looked wrong on a first pass and are not:

- `missing-scientists-probe-2026` still carries a claim matching its own `removeClaims`
  rule, because the correction REPLACES an unattributed assertion with an attributed one
  that necessarily repeats the phrase. The unattributed original is gone and
  `tools/REMOVED-CLAIMS.json` records why.
- `uap-science-advisory-council-2026` is a correction aimed at an id that
  `research/_removed.json` removed and aliased to `uap-science-advisory-council`. Its one
  claim is on the alias target regardless, so nothing is lost. The entry is dead weight and
  could be re-pointed.

The Mansmann correction that started this presumably failed for a reason specific to it.
Nothing supports the general alarm.

---

## 8. Still open, and none of it blocks

| | |
|---|---|
| **`status` has no vocabulary** | eight values, with `dead`/`deceased` and `active`/`alive` as unmerged synonyms. It should be an enum with a rejection, the way `cls` is. Not done here because collapsing the synonyms is an editorial call on 1,125 nodes |
| **Dates lose precision to load order** | `dateStart`/`dateEnd` default to `None`, so they are not this defect, but they are still first-wins. 20 entities ship a coarser date than a later file authored: `hearing-2023-07-26` ships `2023` where `w2-places-events` says `2023-07-26`. 7 more on `dateEnd`. The rule should prefer the more precise value when one is a prefix of the other |
| **`entity.sub` is two fields wearing one name** | 164 entities have conflicting authored values, and the conflict is usually a type token (`report`, `registry`, `mechanism`) against a sentence of prose. Which one is `sub` supposed to be? |
| **The 132 out-of-vocabulary cluster tags** | now ignored rather than coerced, and counted at build time. The `_rs-*` files should use a field of their own |

The first three are separate commits and separate decisions. None of them is reached by
the fix here, and all four are visible now rather than silent, which was the point.
