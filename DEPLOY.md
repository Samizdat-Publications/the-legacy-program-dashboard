# Deploying the board

Two independent pieces. The **site** is the board itself on Cloudflare Pages. The
**worker** is the analyst endpoint. The site works without the worker; the analyst
just falls back to its scripted replies, exactly as it does from a local file.

Everything below is PowerShell 5.1, one command per line. `&&` is a syntax error in
PowerShell, and the repo path has three spaces in it, so keep the quotes.

**Every block below starts with its own `cd`, deliberately.** You should be able to
paste any one of them into a cold terminal without reading the ones above it. The
`wrangler secret put` failure on 26 August was exactly this: run from
`C:\Users\stewa`, no config in scope, nothing to attach a secret to.

---

## Automatic, and why you should prefer it

**Since 30 August 2026 a push to `master` deploys by itself**, via
`.github/workflows/deploy.yml`. **Since 1 September it waits for the gate**: the deploy
runs when `gate.yml` finishes on `master` and only if it passed, so a red gate no longer
ships. The manual route below still works and is still the fallback, but you should not
need it.

**What it deploys changed on 3 September 2026.** It now builds the app in `app/` --
`npm ci`, then `npm run build` -- and uploads **`app/dist`** to the `the-program` project.
Before that it ran `tools/build_site.py` and uploaded a copy of the single-file
`dist/the-program.html`. That old shell still builds and the gate still checks it, but it
is deployed nowhere.

A green tick on a deploy job is not evidence the site changed; fetching the site is.
The check is in "Did production actually move?" below.

It needs two repository secrets, set **once**, in
**Settings → Secrets and variables → Actions → New repository secret**:

| secret | what to put in it |
|---|---|
| `CLOUDFLARE_API_TOKEN` | a **Custom Token** with exactly one permission: **Account → Cloudflare Pages → Edit**, scoped to your account. Nothing else. |
| `CLOUDFLARE_ACCOUNT_ID` | the hex Account ID from the Cloudflare dashboard's right-hand rail |

Until both exist the workflow skips itself and posts a notice saying so, rather than
failing every push.

**Do not use the Global API Key.** It controls the entire account — every zone, DNS,
billing — it cannot be scoped down, and it cannot be rotated per-use. A Pages deploy
needs one permission. If a Global API Key is ever exposed anywhere, roll it
immediately with **Change** on the API Keys page.

**Paste the token straight into GitHub's secret field.** It should not go through
chat, a note, a commit, or a session. Nothing that can read this repository can read
a repository secret, which is the point.

`app/dist/` is gitignored, so the workflow builds it rather than serving a committed
artifact. What makes that safe is the gate: `gate.yml` has an `app` job that builds the
same tree, serves it, and runs the app's own seventeen checks and all seventeen poisons
against the real pages. Deploy waits on the whole workflow, so that job gates it.

It does **not** deploy the analyst worker; §2 below stays manual and stays yours, because
the worker holds an API key. It also does not deploy the review site
**https://the-program-next.pages.dev**, which stays a by-hand deploy. That is where a
build gets looked at before production.

---

## 0. Get the latest

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
git checkout master
git pull origin master
```

## 1. The site

**Deploy from a clean export of `master`, never from the working tree and never from the
repo's `dist/`.** First, in PowerShell, confirm the app's data is in step with the
research it is derived from:

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
python tools\build_app_data.py --check
```

Then, in **Git Bash**, export `master` and build it somewhere with a short path. Windows
refuses a worktree under the scratchpad path, and the repo path has three spaces in it:

```
rm -rf /c/w/next && mkdir -p /c/w/next && git archive master app | tar -x -C /c/w/next
cd /c/w/next/app && npm ci && npm run build && test ! -d dist/transcripts
npx wrangler pages deploy dist --project-name the-program --branch master --commit-dirty=true
```

For the **review site**, the same three lines with `--project-name the-program-next`.
Production is `the-program`; review is `the-program-next`. Nothing else.

**`test ! -d dist/transcripts` is the guard and it is not decoration.** On 2 September a
first attempt chained `cd` into a worktree that had failed to create, so `npx wrangler
pages deploy dist` ran from the repo root and uploaded the OLD `dist/` -- which holds the
transcript exports -- to the review project for about a minute. The project was deleted
outright, recreated, and the transcript path confirmed to serve only the app's page.
**Never deploy the repo's `dist/`.** It is the old shell's build directory and the
transcripts live in it.

### The two prompts on the first deploy

| prompt | answer |
|---|---|
| *"The project you specified does not exist: the-program. Would you like to create it?"* | **Create a new project.** Expected — the project does not exist on Cloudflare until this makes it. |
| *"Enter the production branch name"* | **`master`.** |

**`--branch master` is not optional, and this is the trap.** On a direct upload the
branch defaults to the **current git branch**, and Cloudflare treats any branch that
is not the project's production branch as a **preview**. Work here happens on feature
branches, so without the flag the deploy succeeds, reports a URL, and that URL is a
hashed preview subdomain — while `the-program-zxz.pages.dev`, the link you actually send
people, keeps serving whatever was deployed last. A deploy that looks completely
successful and does not update the live board.

The Pages branch is a label on an upload, not a claim about git: pinning it to
`master` means every deploy lands on the clean URL no matter which branch is checked
out. It is in every recipe above and in `.github/workflows/deploy.yml`; do not drop it.

### Three lines in the output that look wrong and are not

Every later deploy is the same three lines of command. Three lines of *output* have
each raised a false alarm already:

| what it prints | what it means |
|---|---|
| `Warning: Your working directory is a git repo and has uncommitted changes` | Wrangler stamps the deployment with the current commit and says this whenever anything is modified. It does not stop or change the upload. That is what `--commit-dirty=true` acknowledges. |
| `Success! Uploaded 0 files (N already uploaded)` | Cloudflare already holds those exact files, so there was nothing new to send. Two deploys of the same build in a row produce this on the second. It is a successful deploy, not a skipped one. |
| `Deployment complete! Take a peek over at https://<hash>.the-program-zxz.pages.dev` | The per-deployment alias. Wrangler prints one for **every** deploy, production included. Seeing a hashed address here does **not** mean the upload went to preview. |

### Did production actually move?

Because of that last row the printed URL cannot tell you. **Fetch the production
hostname**, which is a job for a session rather than for you:

```
curl -s https://the-program-zxz.pages.dev/ | grep -o '<title>[^<]*'
```

The app's `index.html` is a small shell that fetches its data at runtime, so there is no
large file to hash any more and the old CRLF trap is gone with it. A wrong or missing
title means the upload did not land where you think it did.


**The live board is https://the-program-zxz.pages.dev** — first deployed 26 August
2026. Cloudflare appended `-zxz` because `the-program.pages.dev` was already taken by
someone else's project; the `pages.dev` namespace is global, not per-account. The
project itself is still named `the-program`, which is what `--project-name` refers to.
A cleaner address is a custom domain (Workers & Pages -> the-program -> Custom
domains), not a rename.

Each deploy also prints a `<hash>.the-program-zxz.pages.dev` alias. That is the
immutable snapshot of that one upload — useful for checking a deploy before it
matters, but **never the link to send anyone**, because it will not move when the
board is updated.

**The app's own links are hash routes**: `#/n/<id>`, `#/t/<thread>`, `#/map`,
`#/timeline`, `#/patents/<n>`, `#/evidence`. They need nothing from Pages to work.

The **old shell's path deep links** are a different matter. `/node/aawsap`,
`/path/aawsap/aaro`, `/band/custody`, `/era/nd` and `/q/via:bigelow` were handed out
while the old board was live, and after the cutover those paths are not routes at all.
`app/public/_redirects` sends them into the app rather than to a 404: `/node/` and
`/path/` to their hash equivalents, `/era/` to the timeline for that era, `/band/` to the
map, `/q/` to home. Two of those are approximations rather than matches, and a `/path/`
link carrying two node ids lands on the app's not-found page, because the app's threads
are eight authored chains rather than routes between arbitrary nodes. Cloudflare's
`_redirects` documentation is explicit that a destination may carry a fragment, which is
what makes the whole scheme possible.

## 2. The worker, and the API key

**Deploy the worker before putting the secret.** A secret cannot be attached to a
worker that does not exist yet.

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program\worker"
npm install
npx wrangler deploy
npx wrangler secret put ANTHROPIC_API_KEY
```

The last line prompts for the value and sends it straight to Cloudflare. **The key
never touches this repo, this chat, or your disk.** Get one at
console.anthropic.com under API Keys.

Then route the site's `/api/*` at the worker, so the board reaches it on its own
origin and no CORS is involved. In the Cloudflare dashboard: Workers & Pages ->
the-program -> Settings -> Functions, or simply add a route on the worker for
`<your-pages-domain>/api/*`.

Check it:

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
curl https://<your-domain>/api/analyst/health
```

`{"ok":true,"live":true,...}` means the board will show "analyst live on this
deployment. No key needed." Anything else and it keeps the scripted replies.

## 3. What the worker will and will not do

It pins the model, the token ceiling, the effort and the history depth **server
side**. The client sends only the system prompt and the conversation. This matters
because the URL is public and the tokens are yours: a proxy that forwarded `model`
and `max_tokens` from the request body would be an open account.

**The rate limit is in code, since 1 September 2026.** `worker/wrangler.toml` declares
an `ANALYST_LIMITER` binding at 20 requests per minute per IP, and `src/index.ts`
answers 429 above it. It is the same infrastructure as a dashboard WAF rule, but it is
in version control where a reader of the repo can see it exists. The worker also
answers CORS only to the live board's origin (and a local preview on port 8899), so a
third-party page can no longer spend the account from its visitors' browsers.

Both need a `npx wrangler deploy` from `worker\` to take effect; the secret survives
a redeploy.

## 4. A reader's own key still wins

If someone has set their own key in the board's settings, the board uses it and
never touches the worker. That is deliberate: it is their key and their choice, and
it keeps the offline file behaving exactly as it always has.
