# Audit -- 1 September 2026 (Fable 5.1, read-only review)

**What this is.** A fresh-eyes review of the whole repo at `master` = `3ebe145`, done from a
session rooted one folder up, with no prior context beyond `CLAUDE.md`, the three 30 August
handoffs and the git history. Nothing below was fixed. Every item is meant to be handed to
the building session as a work order.

**How it was done.** Three parallel reviews (Python pipeline; dashboard build + embedded JS;
worker, CI, network tools, secrets), then every finding that mattered was re-verified by
hand against the source or the built file. Where a finding could be confirmed from the
artifact itself it says so. Where it rests on reading the code, it says that instead.

**Overall.** This is an unusually disciplined codebase. The self-test rule in `CLAUDE.md` §5
is real and it works: three reviewers hunted for vacuous checks and swallowed exceptions in
`runtime_check.js` and `verify.py` and found almost none. The findings below are mostly the
places where the project's own conventions were not applied to themselves.

---

## 0. Repo state found on Stewart's machine, and what was done about it

This is the part that was not a code defect and had to be resolved before anything else.

| found | meaning | done |
|---|---|---|
| `.git/MERGE_HEAD` present since 30 Aug 13:20 | a merge of origin's branch into the local branch was started and never finished; one file conflicted (`notes/DESIGN-BRIEF-2026-08-30-NETWORK.md`) | aborted, because by the time it was examined origin had been force-rewritten and squash-merged to `master`, so the merge was against dead history |
| local branch 26 ahead / 10 behind origin, then origin force-updated | the cloud session rewrote `claude/browser-env-tests-61xi1t` and merged PRs #16 to #20 into `master` while this audit ran | local `master` now points at `origin/master` (`3ebe145`). Nothing local was lost: the local tree was a strict subset of what landed |
| 18 tracked files missing from the working tree but intact in git (`data/foia-links.json`, four notes, the Design screenshots) | cause unknown; the timestamps point at the interrupted merge, OneDrive is the other suspect. This is why `verify.py` was red locally: `every FOIA request points at a question that is actually open` failed on the missing file | restored from the `master` tree |
| a stash from 24 Aug, 51 files, on a detached HEAD | stale WIP from the idempotency-hash work | left alone. Almost certainly droppable; Stewart's call |
| `.git` is 435 MB; 463 blobs over 1 MB, 127 commits touching `dist/the-program.html` | every build commits a 16 MB HTML file, so history grows ~16 MB per build | see finding 14 |

**Process finding.** Two sessions (this machine's and the cloud one) both wrote
`.github/workflows/deploy.yml` and `tools/set_repo_secret.py` byte-for-byte identically on
30 August without knowing it. The unmerged-PR lesson in `CLAUDE.md` §4 has a sibling: the
same work done twice because the branch was not fetched before starting.

---

## 1. Findings, by severity

Severity: **P0** wrong on the live board or a real exposure. **P1** a check that cannot do
its job, or a rule the board states and does not enforce. **P2** latent, will bite on a
future change. **P3** tidy-up.

### P0

**1. The timeline breakpoint patch has never applied.** `tools/build_dashboard.py:2146`
```python
s = s.replace("820", "1040") if ".tl-narrow" in s and s.count("820") == 1 else s
```
The guard is false: `ref/the-vanishing-v2.html` contains `820` seven times. So the line
silently does nothing, and both `getBoundingClientRect().width < 820` checks survive
unchanged in `dist/the-program.html` (lines 127322 and 129278 of the built file). The
four-column timeline stacks at the three-column threshold on every reader's screen. Every
other patch in the file goes through `must_replace()` and fails the build by name on a
miss; this one bypasses it. **Confirmed in the built artifact.**
Fix: route through `must_replace()`, anchored on the full `width < 820` expression.

**2. Tier-1 edges sourced only to interested-party domains.** `tools/merge.py:731`
`remediate_edge_tiers()` deliberately does not apply the AARO / DoD cap that
`remediate_tiers()` applies to node claims (its docstring at line 750 says so). `CLAUDE.md`
§2 states the cap with no carve-out for edges. Measured on `data/the-program.json`: **82
edges carry `claimTier: 1` with every source on `aaro.mil`, `defense.gov` or `war.gov`.**
They render as "Tier 1 - documented". Some may be legitimately "what AARO said" edges; the
point is that nothing has adjudicated them. **Confirmed by counting the data.**
Fix: either apply the cap to edges with the same attribution exemption, or narrow §2 to say
it is a node rule and record why. Then a `verify.py` check for whichever was chosen.

**3. Public, wildcard-CORS proxy to Opus 5 with no rate limit in code.**
`worker/src/index.ts:36` sets `Access-Control-Allow-Origin: *`; nothing in the worker or
`wrangler.toml` limits calls per IP. `DEPLOY.md` §3 describes a dashboard rate-limiting rule
as "worth adding", which means it is not in version control and may not exist. Any page on
the internet can `fetch()` the endpoint from its visitors' browsers and spend the account.
Fix: a Workers rate limiter binding or a KV token bucket per IP, in code; restrict the
origin to the Pages domain; confirm the WAF rule exists and record it in `DEPLOY.md` as done.

### P1

**4. `check_rebuild.py` diffs against the index, not HEAD.** `tools/check_rebuild.py:114`
runs `git diff --name-only` with no ref. A built artifact that was `git add`-ed before the
check runs is never passed to `compare()` and reads as matching. The mtime guard usually
catches this first, but with the message "nothing was rebuilt", which misdescribes what
happened. Fix: `git diff HEAD --name-only`.

**5. Windows builds emit CRLF and `check_rebuild.py` compares raw bytes.**
`tools/build_dashboard.py:1045` and `:2470` open without `newline=`; `DEPLOY.md` §1 already
records that a Windows build carries CRLF. `check_rebuild.py` normalises only the date
stamp, so a build run from PowerShell fails the reproducibility check for a reason unrelated
to content. `core.autocrlf=true` on this machine means the committed blob is still LF, so
the damage is a false red, not a bad commit. There is no `.gitattributes`.
Fix: `newline=""` on read and `newline="\n"` on write in every writer the pipeline uses,
plus a `.gitattributes` pinning `eol=lf` on `data/*` and `dist/*`.

**6. `deploy.yml` does not wait for `gate.yml`.** Both trigger on `push: master`
independently (`deploy.yml:28`). A push whose gate goes red still deploys. The file's own
header says "after the gate is green"; it is not. Fix: trigger deploy on
`workflow_run: [gate]` with `conclusion == success`.

**7. Claims, sources and chronology entries are dropped without a `reject()` call.**
`tools/merge.py:121` `norm_claim` returns `None` on a missing `text`; `:82` `norm_source`
returns `None` with no `name` or `url`; `:154` `norm_chron` skips entries missing `date` or
`event`. None of these reach `tools/REJECTS.json`, so the check named `no research record
is silently dropped` (`verify.py:1875`) cannot see them. This is the `cls` bug from 30
August one level down. Fix: `reject()` in each branch, and let the existing check cover it.

**8. `regrade.py` says "cannot be Tier A" and then only discounts.** `tools/regrade.py:136`
multiplies the score by 0.35 for a node with no sourced URL. A high-degree unsourced node can
still clear the top-15% cut. No check asserts "every Tier A node has a sourced URL". Fix:
make the exclusion absolute and add the check.

**9. `verify.py` "UI copy agrees with the data" passes vacuously at 6, 7, 10 or 11 entity
classes.** `tools/verify.py:541` maps only {3,4,5,8,9,12} to words; any other count makes
`want` None and the check returns clean. The board has 8 today, so it works by
coincidence, and the self-test fixture always builds 8, so the gap is never poisoned. Fix:
compute the word, and add a poison at an unmapped count.

**10. `MAX_TOKENS = 4000` with `EFFORT = "high"` on Opus 5.** `worker/src/index.ts:30-31`.
Thinking tokens count against `max_tokens`; at high effort the model can spend the whole
budget thinking and return `stop_reason: max_tokens` with little or no text. The board
does not handle that stop reason. Fix: raise the ceiling (16000 is the documented shape
for this configuration) or lower effort, and surface `max_tokens` in the client.

**11. Unescaped SVG `fill` attribute in the inherited chart code.**
`ref/the-vanishing-v2.html:3417` `chartColor()` returns `p.color` verbatim and the four chart
renderers splice it into `fill="..."`. Every other point field goes through `esc()`. A chart
spec reaches this through the analyst's `:: renderChart` command, which is now served by a
shared worker to every visitor. A model reply that puts a `"` in a colour is markup
injection in the reader's session. Fix: a patch in `build_dashboard.py` that escapes or
allow-lists the colour; `ref/` stays untouched per the project rule.

### P2

**12. Two more unguarded `s.replace()` calls.** `tools/build_dashboard.py:1336-1337`, the
top-bar chrome copy. They applied this time (the built file has "Program map live") but a
future `ref/` change would silently ship the parent board's text. Same fix as finding 1.

**13. `js()` does not neutralise `</script`, `<!--`, U+2028 or U+2029 inside inlined
strings.** `tools/build_dashboard.py:406`. Research text is quoted verbatim by rule, so a
claim quoting a document that contains a literal `</script>` would truncate the page's
script. No `verify.py` check screens for it. Fix: escape `<` as `\x3c` and the two Unicode
separators; add a regression check.

**14. History bloat.** 16 MB `dist/the-program.html` in 127 commits; `.git` at 435 MB and
growing about 16 MB per build. CI already proves the artifact reproduces from source, and
`deploy.yml` could build it rather than serve the committed copy. Options, in order of
disruption: stop committing `dist/` and let CI build and deploy it; or Git LFS for `dist/`
and the two big JSON files; or leave it and accept a 1 GB repo by October. Stewart's call.

**15. `.gitignore` misses `.wrangler/` at the root and under `dist/`.** Only
`worker/.wrangler/` is ignored. Both untracked caches hold the Cloudflare account id and
the account email today, and a `git add -A` would stage them. Fix: `**/.wrangler/`.
(History was scanned: no credential file or key-shaped string has ever been committed.)

**16. `verify.py` "the built page fetches nothing at runtime" no longer verifies that.**
`tools/verify.py:416` scans declarative `href`/`src`/`url()` only. Since 29 August the board
fires `fetch('/api/analyst/health')` on every http(s) load and `fetch()` to the worker or to
`api.anthropic.com` from the analyst. The check is still correct for what it scans, but its
name and docstring state a property that is no longer true. Fix: rename it to what it
checks, and add a check that the only `fetch(` literals are the two intended endpoints.

**17. A typo'd id in `_corrections.json` or `_remediation.json` creates a phantom node.**
`tools/merge.py:302-330` and `:354-371` fall through to the generic create branch when the
target id does not exist. Fix: reject by id when the target is absent.

**18. Claim dedup key truncates at 120 characters.** `tools/merge.py:183`. Two long claims
that share a 120-character opening collapse to one, silently. Fix: hash the full text.

**19. A hardcoded claim filter lives in code.** `tools/merge.py:364` drops any Tier-1 claim
containing "yankee blue" on every build, for any entity referenced by `_corrections.json`,
with no log and no reviewable record. This contradicts the project's own rule that removals
are recorded with reasons. Fix: move it to `research/_corrections.json` as an explicit
claim removal with a reason.

**20. `spot_check.py --links` writes to `/dev/null`.** `tools/spot_check.py:349`. Native
Windows `curl.exe` cannot open that path, so the link sweep, deliberately kept out of CI so
a person runs it, fails on the one machine a person runs it from. Fix: pick `NUL` on
`os.name == "nt"`, or use `tempfile`.

### P3

**21.** `tools/build_dashboard.py:413` emits Python `nan`/`inf` as bare identifiers; one
bad number anywhere in `research/` would break the whole page at parse time. Raise instead.
**22.** `tools/merge.py:625` `INTERESTED_PARTY_PAT` anchors `defense.gov` but not
`war.gov`, `pentagon.mil`, `dvidshub`. Over-caps, which is the safe direction, but tidy it.
**23.** `tools/merge.py:77` `reject()` has a ternary whose precedence does not do what it
reads as; inert today because every caller passes a dict.
**24.** `tools/build_design_extract.py:92` has no guard for an empty L0 list.
**25.** `package.json` at the repo root pins `playwright ^1.62.1` while `gate.yml` installs
`1.56.1`. One of them is wrong; the tools were written against 1.56.
**26.** `verify.py` prints em dashes, which the PowerShell 5.1 console renders as `�`.
Cosmetic, but it is the console Stewart reads.
**27.** `CLAUDE.md` is 44 KB and loads into every session. Most of §9 is a done-log. Moving
the done items to a `notes/DONE.md` would cut the per-session cost by more than half
without losing anything.

---

## 2. Things that were checked and are fine

- `worker/src/index.ts` request shape (`thinking: adaptive`, `output_config.effort`) is
  the current API for `claude-opus-5`. The worker pins model, ceiling, turns and chars
  server-side and validates the conversation shape. Good.
- No `eval`, `Function` or string `setTimeout` anywhere in the reviewed surface. Deep-link
  segments are validated against node ids before use. `runCommandLine` dispatches through a
  whitelist.
- `fetch_transcripts.py` and `fetch_podcast.py` never use `shell=True`; ids are regex-checked
  before reaching a subprocess or a path. The `--select` comment-stripping bug is fixed.
- `corpus_crosscheck.py` and `check_rebuild.py` self-tests exercise the exact failures they
  were written for. `verify.py`'s poison plumbing is per-check and a check without a poison
  fails loudly.
- Every `open()` in the pipeline passes `encoding="utf-8"`.
- `Cache-Control: no-cache` on the 16 MB index is not "re-download every visit": Pages sets
  an ETag, so a repeat visit is a conditional GET. Worth confirming with two `curl -I`
  calls, but not a defect.
- Git history: no credential file or key-shaped string was ever committed.

---

## 2a. Fixed the same day (branch `fix/p0-2026-09-01`)

| finding | what was done |
|---|---|
| 1, 12 | all three bare `replace()` calls routed through `must_replace()`; the timeline threshold now applies at both sites. New verify check `the timeline stacks at the four-column threshold`, poisoned with the historical bug |
| 2 | the cap now runs on edges in `merge.py`, with `research/_edge_tiers.json` carrying 16 per-edge decisions (10 keep Tier 1 as self-publication or attribution, 2 to Tier 2, 4 domain-to-domain inferences to Tier 3). New verify check re-derives it independently. Also fixed `acknowledg\b`, which could never match "acknowledges" |
| 3, 10 | worker: per-IP rate limit binding in code (20/min), CORS restricted to the board's origin and a local preview, `max_tokens` 16000; deployed. SDK upgraded to 0.123 so the request shape typechecks; the pinned `workers-types` version did not exist, so `npm install` had never worked in `worker/` |
| 5 | `build_dashboard.py` reads and writes with explicit newlines; a Windows build is now byte-identical to a Linux one |
| 6 | `deploy.yml` fires on the gate workflow completing on master, and only on success |
| 15 | `.gitignore` covers `**/.wrangler/`, the local Claude settings file, and tool logs |
| 20 | `spot_check.py` uses `os.devnull` |
| new | **the analyst was never live on the deployed site.** Pages cannot route `/api/*` to a Worker on a `pages.dev` host and answers the health probe with the board itself (200, text/html), so the same-origin probe never returned JSON. The client now falls back to the Worker's own hostname. Separately the Worker has no `ANTHROPIC_API_KEY` secret set (its health endpoint reports `live: false`), which only Stewart can put |
| new | `fetch_podcast.py`: stdout re-encoded to UTF-8 so a title with a character outside cp1252 no longer kills a run hours in (found on Area52); `--match` and `--select` filters so a 427-episode feed can be taken by subject; `--list` prints ids |
| new | `l0_patches.py` line 3 had five invalid escape sequences that Python 3.14 warns on and a future version will refuse |
| new | `CLAUDE.md` pointed at the EVENING handoff a day after NIGHT was written |

Golden manifest updated: edge tiers 1408/586/200 -> 1402/588/204, which is exactly the
16 adjudications (2 down to Tier 2, 4 down to Tier 3, the rest held). Full gate green
locally on Windows, Python 3.14: all ten steps including `--idempotent`.

## 3. Suggested order of work

| # | finding | why first |
|---|---|---|
| 1 | 1, 12 (route the three bare `replace()` calls through `must_replace()`) | one-line fixes, and one of them is live |
| 2 | 2 (adjudicate the 82 edges) | the board's own rule, visibly not applied |
| 3 | 3 (rate limit + origin on the worker) | the only finding that costs money while it waits |
| 4 | 4, 5, 6 (the reproducibility and deploy gates) | the gate is the product's credibility |
| 5 | 7, 8, 9 (the three checks that cannot fire) | §5 in three costumes |
| 6 | 10, 11 | analyst correctness and safety |
| 7 | the rest | as time permits |

Each fix should come with the poison that shows it failing, per §5. Finding 1 in particular
should get a `verify.py` check that greps the built file for `width < 820`, because that is
the check that would have caught it a month ago.
