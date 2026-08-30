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

**Live and working since 30 August 2026.** Run 1 of the workflow deployed
`the-program-zxz.pages.dev` in 41 seconds -- 3.78s to upload, and the deployed page
was checked afterwards rather than trusted: 15.85 MB, the right `<title>`, and all
six spot-checked new node ids present in the served HTML. A green tick on a deploy
job is not evidence the site changed; fetching the site is.

**Since 30 August 2026 a push to `master` deploys the site by itself**, via
`.github/workflows/deploy.yml`. The manual route below still works and is still the
fallback, but you should not need it.

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

The workflow deliberately deploys the **committed** `dist/the-program.html` rather
than rebuilding, so what goes live is the artifact the gate proved reproduces from
source. It does **not** deploy the analyst worker; §2 below stays manual and stays
yours, because the worker holds an API key.

---

## 0. Get the latest

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
git checkout master
git pull origin master
```

## 1. The site

`site/` is a build product and is gitignored, so regenerate it after every pull:

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
python tools\build_site.py
npx wrangler pages deploy site --project-name the-program --branch master
```

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
out. `tools\build_site.py` prints the command with the flag already in it.

### Three lines in the output that look wrong and are not

Every later deploy is the same three lines of command. Three lines of *output* have
each raised a false alarm already:

| what it prints | what it means |
|---|---|
| `Warning: Your working directory is a git repo and has uncommitted changes` | Wrangler stamps the deployment with the current commit and says this whenever anything is modified. It does not stop or change the upload. `site/` is gitignored, so it is never the cause. |
| `Success! Uploaded 0 files (1 already uploaded)` | Cloudflare already holds that exact file, so there was nothing new to send. Two deploys of the same build in a row produce this on the second. It is a successful deploy, not a skipped one. |
| `Deployment complete! Take a peek over at https://<hash>.the-program-zxz.pages.dev` | The per-deployment alias. Wrangler prints one for **every** deploy, production included. Seeing a hashed address here does **not** mean the upload went to preview. |

Because of that last row the printed URL cannot tell you whether production moved.
**The only reliable check is to fetch the production hostname and compare it to the
build**, which is a job for a session rather than for you:

```
curl -sS -L https://the-program-zxz.pages.dev/the-program.html | tr -d '\r' | sha256sum
sha256sum site/index.html
```

`tr -d '\r'` is not optional. A build made on Windows carries CRLF line endings, so the
live file is larger than the local one by exactly its line count and hashes differently
while being the same page. On 26 August that difference was 124,802 bytes against
124,802 lines, and the two matched once the carriage returns were stripped.


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

Deep links work immediately: `/node/aawsap`, `/path/aawsap/aaro`, `/band/custody`,
`/era/nd`, `/q/via:bigelow`. `site/_redirects` is what stops those 404ing, and it
names the routes rather than blanket-rewriting `/*`, so the data files stay
reachable if a payload split ever lands.

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

It is still worth adding a Cloudflare rate-limiting rule on `/api/analyst` in the
dashboard under Security -> WAF -> Rate limiting rules. Something like 20 requests
per minute per IP is generous for a human reader and useless to anyone else.

## 4. A reader's own key still wins

If someone has set their own key in the board's settings, the board uses it and
never touches the worker. That is deliberate: it is their key and their choice, and
it keeps the offline file behaving exactly as it always has.
