# The gate could only ever run in one container, and nobody had noticed

**28 August 2026.** Stewart asked whether it matters that this repo has no CI, whether it
is a problem, and whether it is easy to fix.

Short answer: **the missing CI was the symptom. The gate was not portable, and that is the
problem.** It is fixed, and CI is now possible as a consequence rather than as the point.

---

## 1. What was actually wrong

Four of the nine gate steps opened with two absolute paths baked into the source:

```
require('/opt/node22/lib/node_modules/playwright')
executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
```

Those are facts about **one container**, not about this project. `capture_strip`,
`runtime_check` and both `test_packed_layout` runs carried them, as did the `look` and
`walk` cameras. Three consequences, and the first had already been paid before anybody
looked:

**`tools/shoot.js` was already dead.** It pinned `/opt/pw-browsers/chromium/chrome-linux/chrome`,
without the build number. That path does not exist -- `/opt/pw-browsers/chromium` is not a
directory. The tool could not start, and nothing said so. It is the CLAUDE.md section 5
failure one rung further out: not a check that passes while broken, a check that never
begins. It had a `.catch(() => chromium.launch())` fallback, which is why it failed silently
rather than loudly.

**`chromium-1194` is a pinned Playwright build number.** The day this image ships 1200, four
gate steps stop starting *at the same moment*, and the gate reports an environment problem
in the shape of a board problem.

**Nothing outside this container could run the gate.** Not GitHub Actions. Not Stewart on
Windows -- and CLAUDE.md section 3's table says he can build and test, which was true for
`verify.py`, `audit_independent.py` and the analyst test, and false for the four browser
steps. That matters more than it looks, because `capture_strip` must run **before**
`audit_independent` or the audit reads a stale `tools/runtime-strip.txt` and reports
defects that are not there. That has already cost a handoff two phantom findings once.
So the half of the gate Stewart could run was the half that silently depends on the half
he could not.

Net effect: "the gate is green" was a sentence exactly one kind of actor could say. A gate
that only one participant can run is not a shared standard, it is a bottleneck with good
manners.

## 2. The fix

`tools/browser_env.js`. A tool may depend on Chromium **existing**; it may not depend on
where. Resolution runs most-explicit to most-automatic, and every step is a real filesystem
check:

| order | source | notes |
|---|---|---|
| 1 | `CHROMIUM_PATH` | ignored unless the file actually exists |
| 2 | `PLAYWRIGHT_BROWSERS_PATH` | globs `chromium-<n>`, takes the highest build |
| 3 | `/opt/pw-browsers` | same glob, so a container image bump is survived |
| 4 | `undefined` | hand Playwright the decision -- this is the CI path |

Step 4 is the one that matters and the one that is easy to get wrong. Returning `undefined`
and letting `launchOptions()` **omit the key entirely** is what makes `chromium.launch()`
resolve Playwright's own downloaded browser. Passing a guessed path would fail; passing
`executablePath: undefined` explicitly is fine, but omitting it is cleaner and is what the
code does.

Playwright itself is resolved the same way: local `node_modules` first so a contributor's
own install wins, container copy second.

## 3. The check, and the part of it this machine cannot see

`tools/test_browser_env.js`, 13 assertions, now the **first** gate step -- it needs no
browser and no server, so it is the cheapest place to learn whether the browser steps can
start at all. It runs on Windows.

The interesting case cannot be observed on the machine that needs it least. In this
container `/opt/pw-browsers` always exists, so the "nothing installed anywhere" branch --
the CI branch, the Stewart's-laptop branch -- never fires here. Hoping is not a test. The
check reaches it by **hiding the directory from `fs.readdirSync`**, which is what being off
this container actually looks like:

```
ok  no browser anywhere resolves to undefined, not to a guess
ok  launchOptions omits executablePath entirely when nothing resolved
```

`--self-test` then poisons four ways, each of which must break a specific assertion above:
a resolver that ignores `CHROMIUM_PATH`, one that takes the lowest build number, one that
trusts a `CHROMIUM_PATH` that does not exist, and one that invents a path when nothing is
installed. All four are caught. Per CLAUDE.md section 5, that is the difference between a
check that is self-tested and a check that is known to be looking at the thing.

## 4. Only then, CI

`.github/workflows/gate.yml`. It is short because the portability work is what made it
short. Build, then serve, then `state_snapshot.py --gate`, then upload `look.js`
screenshots as an artifact so a human can see the board a run produced.

One step is new rather than ported, and it is the one worth keeping:

> **The build must be reproducible from what is committed.** Rebuild from `research/`,
> then fail if `git diff` is non-empty.

This repo commits its build products -- `dist/the-program.html` at 15MB, `data/` at 13MB.
So a push can carry edited sources and a stale build, and the board a reader sees would not
be the board the sources describe. `--idempotent` proves the build is deterministic; it does
not prove the committed artifacts came from the committed source. Nothing did. Verified
before shipping: after a full rebuild, `data/` and `dist/` are byte-identical to `HEAD`, so
this step passes today rather than going red on its first run.

**Costs, plainly.** The repo is private, so these are billed Actions minutes. A run is
roughly 12-15 minutes, most of it `--idempotent` building the board twice. At a handful of
pushes a day that is comfortably inside the 2,000 free private-repo minutes, but it is not
free, and **if it is not wanted the file can be deleted with no other consequence** -- the
gate still runs locally and nothing depends on the workflow.

No pip step: everything the gate runs is Python standard library plus this repo's own
modules. `pypdf` appears only in `tools/spot_check.py`, which is deliberately outside the
gate because a check that fails when a host is throttling is a check people learn to
ignore.

The workflow does **not** deploy. Cloudflare Pages stays manual and stays Stewart's.

## 5. What this changes for Stewart

He can now run the whole gate, which he could not before. On a machine with Node and
Playwright installed:

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
npm install playwright http-server
npx playwright install chromium
```

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
node tools\test_browser_env.js --self-test
```

If that second block prints `browser env ok`, the browser steps will start. That is the
whole point of putting it first.

## 6. Verified

Full gate green on the patched tools, all ten steps including the new one, with
`--idempotent`:

```
browser_env --self-test  PASS      test_packed_layout       PASS
verify                   PASS      test_packed_layout --self-test PASS
verify --self-test       PASS      test_scripted_analyst    PASS
capture_strip            PASS      verify --idempotent      PASS
audit_independent        PASS      runtime_check            PASS
```

The workflow itself has **not** run -- it cannot until the branch is pushed and Actions is
enabled. So: the tools are proven portable here, and the YAML is unproven until GitHub runs
it. Stated rather than glossed, because "it should work in CI" is the same sentence as "the
check should catch that".

## 7. Left undone

- `CLAUDE.md` section 3's environment table still says what it said. It is now wrong in a
  new direction: Stewart *can* run the browser steps, given an install. Worth a correction
  next time that file is touched, but not worth a drive-by edit in a research PR.
- The repo grows about 30MB of committed build products per commit and `.git` is already
  146MB. Not urgent, not this PR, and the fix is a policy decision about whether `dist/`
  belongs in git at all.
