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

## 0. Get the latest

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
git checkout claude/claud-md-compacting-vs9o9j
git pull origin claude/claud-md-compacting-vs9o9j
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
hashed preview subdomain — while `the-program.pages.dev`, the link you actually send
people, keeps serving whatever was deployed last. A deploy that looks completely
successful and does not update the live board.

The Pages branch is a label on an upload, not a claim about git: pinning it to
`master` means every deploy lands on the clean URL no matter which branch is checked
out. `tools\build_site.py` prints the command with the flag already in it.

It prints the live URL when it finishes. Every later deploy is the same three lines.

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
