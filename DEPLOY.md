# Deploying the board

Two independent pieces. The **site** is the board itself on Cloudflare Pages. The
**worker** is the analyst endpoint. The site works without the worker; the analyst
just falls back to its scripted replies, exactly as it does from a local file.

Everything below is PowerShell 5.1, one command per line. `&&` is a syntax error in
PowerShell, and the repo path has three spaces in it, so keep the quotes.

---

## 0. Once

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
git checkout claude/claud-md-compacting-vs9o9j
git pull origin claude/claud-md-compacting-vs9o9j
```

## 1. The site

`site/` is a build product and is gitignored, so regenerate it after every pull:

```
python tools\build_site.py
npx wrangler pages deploy site --project-name the-program
```

The first deploy asks to create the project and to log in through the browser. It
prints the live URL when it finishes. Every later deploy is the same two lines.

Deep links work immediately: `/node/aawsap`, `/path/aawsap/aaro`, `/band/custody`,
`/era/nd`, `/q/via:bigelow`. `site/_redirects` is what stops those 404ing, and it
names the routes rather than blanket-rewriting `/*`, so the data files stay
reachable when the payload split lands.

## 2. The worker, and the API key

**Deploy the worker first.** A secret cannot be attached to a worker that does not
exist yet, which is why `wrangler secret put` failed from the home directory: there
was no config in scope and no worker to attach to.

```
cd worker
npm install
npx wrangler deploy
npx wrangler secret put ANTHROPIC_API_KEY
```

The last line prompts for the value and sends it straight to Cloudflare. **The key
never touches this repo, this chat, or your disk.** Get one at
console.anthropic.com under API Keys.

Then route the site's `/api/*` at the worker, so the board can reach it on its own
origin and no CORS is involved. In the Cloudflare dashboard: Workers & Pages ->
the-program -> Settings -> Functions -> or simply add a route on the worker for
`<your-pages-domain>/api/*`.

Check it:

```
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
