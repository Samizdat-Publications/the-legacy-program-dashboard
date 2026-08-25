# The two "audit failures" on this branch were a stale file

**25 August 2026.** `notes/HANDOFF-2026-08-25-claude-code.md` §2b reports that
`tools/audit_independent.py` finds two real defects in this branch's data:

```
stats strip TIER A:      rendered/model 144 vs independently derived 142
breadcrumb object count: rendered/model 428 vs independently derived 436
```

and warns, correctly in principle, not to paper over them by regenerating
`tools/GOLDEN.json`.

They are not defects. Both numbers on the left came out of
`tools/runtime-strip.txt`, which is a **capture of a browser DOM**, hand-pasted
from `master`'s build. `audit_independent.py` reads it because the stats strip is
assembled by script at runtime and so cannot be read out of the built HTML.

`master`'s capture records `master`'s board: 968 entities, 4,431 claims, TIER A 144.
This branch collapsed nine duplicate groups, so its board is 956 entities, 4,445
claims, TIER A **142**. Comparing a merged model against `master`'s capture reports
the collapse as a defect. The independently derived figure was right both times.

Captured from this branch's own build and re-run:

```
ENTITIES 956 across 8 classes   SOURCED LINKS 2159 hand-written   TIER A 142
DOCUMENTED 61% of 4445 claims   DENIALS 174 on the record         CUSTODY 119 chain links

  checks run 37 / failed 0
```

## What changed so it cannot happen again

`tools/capture_strip.js` now writes `tools/runtime-strip.txt` off a real DOM. The
file is a build product, not a source. **Recapture it whenever the board is rebuilt.**
A stale capture makes an independent audit report a data defect that is not there,
which is the more dangerous direction for this particular tool to fail in: it spends
a reader's trust on a phantom and trains them to discount the next real finding.

At merge time this file will conflict with `master`'s. Resolve it the way the handoff
says to resolve every generated file: **rebuild, then recapture.** Do not pick a side.
