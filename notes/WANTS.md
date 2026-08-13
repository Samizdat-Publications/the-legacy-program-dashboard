# Wants — parked ideas, not scheduled

Things Stewart has asked for that are not in the current work. Kept here so they do not get
lost in a chat log.

---

## Public README and landing page — POST-1.0, do not start early

**Asked 13 Aug 2026.** A full README and a visually impressive landing page: screenshots
pulled from the running app, a display that shows what the board actually does.

**Explicitly gated on reaching 1.0.** The reason to hold it is not effort, it is that a
landing page is a *claim about a finished thing*. Screenshots taken now would show the
970-node tangle, the plate overlap and the pre-L0 map, and every one of them would be stale
the moment the design work lands. Shipping a polished front door onto a board mid-surgery
also invites exactly the hostile read this project is built to survive.

What it should include when it is time:

- Screenshots per view, captured from the real board via `tools/shoot.js` so they cannot
  drift from what ships
- The numbers as the headline — claim-tier split, source count, span of years — because that
  is the product, not the visuals
- An honest "what this is not" section. A board that oversells itself loses the argument
  before anyone reads a claim.

**Definition of 1.0 is not yet agreed.** Proposed: L0 map landed, `TESTING-CHECKLIST.md`
worked end to end including the §12 source spot-checks, and `verify.py --idempotent` green.

---

## GitHub ownership — blocked on connector authorisation

**Asked 13 Aug 2026.** Stewart wants Claude to own all GitHub work: publishing, version
control, branches, releases, the eventual landing page.

**Blocked:** the `plugin:engineering:github` connector is present but unauthorised, and a
non-interactive session cannot run the OAuth flow. There is no `gh` CLI, no `GH_TOKEN` and
no credential helper in the sandbox. Verified by tool search on 13 Aug, not assumed.

**Unblock:** authorise the GitHub connector in claude.ai connector settings, or `/mcp` in an
interactive session. After that this is fully delegable.

Repo is publish-ready as of `52a01c6`: 95 files, 9 commits, secret-scanned (only match is
the literal string `sk-ant-` in the Set-API-key placeholder). Intended name:
**the-legacy-program-dashboard**, "The Legacy Program Dashboard".

---

## Craft catalogue with 3D or sprite representations

**Asked 12 Aug 2026.** A visual representation of each craft that has been catalogued —
the Lazar "sport model" being the obvious first one, alongside the tic-tac, the Rendlesham
object, the flying-disc morphology from the 1947 reports, and so on.

**Preference: build these in Claude Design rather than generating them.** Stewart's stated
reason to prefer design over image generation is right, and it is the same reason the rest
of this board refuses to round anything off:

- A **generated** image is a plausible-looking picture with no stated provenance. On a board
  whose entire product is "59% of 4,108 claims rest on a primary record", an unsourced
  render of a craft is the single most discrediting object that could be put on it. A
  hostile reader would go straight to it.
- A **drawn** schematic can carry the thing every other object here carries: a source, a
  claim tier, and a description of *whose account it depicts*. The Lazar sport model is not
  a craft — it is **a diagram of one man's description of a craft, from 1989**, and the
  illustration has to say so.

So the requirement is not "make pictures of UFOs". It is:

> A schematic per catalogued craft morphology, each attributed to the specific testimony or
> document it derives from, each carrying a claim tier, each visually distinguishable from a
> photograph so it can never be mistaken for evidence.

Line-art / blueprint / orthographic-projection treatment fits the phosphor-terminal language
and does the credibility work at the same time — it reads as "this is a reconstruction",
which is exactly true.

**Open questions for when this is picked up:**

- Does a craft become a **node class** (a ninth) with its own edges to witnesses, locations
  and programs? Probably yes — it would make "which witnesses describe the same morphology"
  a query the board can answer, which is a genuinely new capability rather than decoration.
- 3D or 2D? 3D costs a renderer and a lot of load budget on a board already fighting for it.
  Orthographic 2D sprites at a few angles get most of the value for a fraction of the cost.
  Recommend starting 2D.
- Where does it live — a new CRAFT view, or inside the dossier of the witness who described
  it? Probably both, with the dossier as the primary home.

**Not started. Do not begin before the load-time work lands** — this adds weight to the one
budget currently in trouble.
